import os
import re


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "run"


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)



