from __future__ import annotations

import os
from dataclasses import dataclass

from yt_dlp import YoutubeDL
from .utils import ensure_dir, slugify


@dataclass
class DownloadedVideo:
    source_url: str
    filepath: str


def download_video(url: str, dest_dir: str) -> DownloadedVideo:
    ensure_dir(dest_dir)
    out_tmpl = os.path.join(dest_dir, "%(title).80s-%(id)s.%(ext)s")
    
    ydl_opts = {
        'format': 'bv*[height<=360]+ba/b[height<=360]/best',
        'merge_output_format': 'mp4',
        'outtmpl': out_tmpl,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)
        # Handle merged formats - the actual file has the extension from merge_output_format
        if os.path.exists(filepath):
            return DownloadedVideo(source_url=url, filepath=filepath)
        # If file doesn't exist, try to find it
        for ext in ['mp4', 'mkv', 'webm']:
            candidate = filepath.rsplit('.', 1)[0] + '.' + ext
            if os.path.exists(candidate):
                return DownloadedVideo(source_url=url, filepath=candidate)
        raise RuntimeError("Download failed: no output file found")



