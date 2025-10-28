from __future__ import annotations

from typing import List

from faster_whisper import WhisperModel

from .types import TranscriptSegment


def transcribe_video(path: str, use_vad_filter: bool = False) -> List[TranscriptSegment]:
    model = WhisperModel(model_size_or_path="base", device="cpu")
    segments_iter, _info = model.transcribe(path, vad_filter=use_vad_filter)
    segments = []
    for seg in segments_iter:
        segments.append(
            TranscriptSegment(start_s=float(seg.start), end_s=float(seg.end), text=(seg.text or "").strip())
        )
    return segments



