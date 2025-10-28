from __future__ import annotations

import os
import subprocess
from typing import List

from .utils import ensure_dir


def trim_clip(src_path: str, start_s: float, end_s: float, out_path: str) -> None:
    ensure_dir(os.path.dirname(out_path))
    duration = max(0.01, end_s - start_s)
    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start_s),
        "-i",
        src_path,
        "-t",
        str(duration),
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        out_path,
    ]
    subprocess.run(cmd, check=True)



