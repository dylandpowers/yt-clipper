import argparse
import json
import os
from datetime import datetime, timezone
from typing import List

from .utils import ensure_dir, slugify
from .search import search_youtube
from .download import download_video
from .transcribe import transcribe_video
from .segment import rolling_windows_from_transcript
from .select import compute_scores, suppress_overlaps
from .trim import trim_clip
from .types import SourceVideo, ClipResult, CandidateClip


def main() -> None:
    parser = argparse.ArgumentParser(description="yt-clipper – YouTube Highlight Clipper")
    parser.add_argument("--prompt", required=True, help="Prompt describing desired highlights")
    parser.add_argument("--max-source-videos", type=int, default=6)
    parser.add_argument("--max-clips", type=int, default=8)
    parser.add_argument("--target-clip-len-s", type=int, default=12)
    parser.add_argument("--min-clip-len-s", type=int, default=6)
    parser.add_argument("--max-clip-len-s", type=int, default=20)
    parser.add_argument("--workdir", default="outputs")
    parser.add_argument("--datadir", default="data")
    parser.add_argument("--use-vad-filter", action="store_true")
    args = parser.parse_args()

    run_id = slugify(args.prompt)
    run_dir = os.path.join(args.workdir, run_id)
    clips_dir = os.path.join(run_dir, "clips")
    ensure_dir(clips_dir)

    data_dir = os.path.join(args.datadir, run_id)
    ensure_dir(data_dir)

    # 1) Search
    search_results = search_youtube(args.prompt, max_results=args.max_source_videos)

    # 2) Download
    sources: List[SourceVideo] = []
    for r in search_results:
        dl = download_video(r.url, data_dir)
        sources.append(SourceVideo(url=r.url, title=r.title, path=dl.filepath, duration=r.duration))

    # 3) Transcribe + 4) Windows
    all_candidates = []
    for s in sources:
        segments = transcribe_video(s.path, use_vad_filter=args.use_vad_filter)
        windows = rolling_windows_from_transcript(
            segments,
            window_s=args.target_clip_len_s,
            min_s=args.min_clip_len_s,
            max_s=args.max_clip_len_s,
        )
        cands = compute_scores(args.prompt, windows)
        for c in cands:
            c.source_url = s.url
        all_candidates.extend(cands)

    # 5) Select
    selected = suppress_overlaps(all_candidates, max_clips=args.max_clips)

    # 6) Trim
    clip_results: List[ClipResult] = []
    for idx, c in enumerate(selected, start=1):
        # Find the source path
        src = next((s for s in sources if s.url == c.source_url), None)
        if src is None:
            continue
        clip_name = f"clip_{idx:03d}.mp4"
        out_path = os.path.join(clips_dir, clip_name)
        trim_clip(src.path, c.start_s, c.end_s, out_path)
        clip_results.append(
            ClipResult(
                file=f"clips/{clip_name}",
                source_url=c.source_url,
                start_s=c.start_s,
                end_s=c.end_s,
                score=c.score,
                transcript_excerpt=(c.text[:200] + ("…" if len(c.text) > 200 else "")),
                confidence=max(0.0, min(1.0, c.score)),
            )
        )

    # 7) Manifest
    manifest_path = os.path.join(run_dir, "manifest.json")
    manifest = {
        "prompt": args.prompt,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "clips": [c.__dict__ for c in clip_results],
        "sources": [{"url": s.url, "title": s.title, "path": s.path, "duration": s.duration} for s in sources],
        "disclaimer": "Use only content you have rights to use. Respect YouTube ToS.",
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Wrote {len(clip_results)} clips to {clips_dir}")



