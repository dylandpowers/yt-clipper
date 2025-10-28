import os
import re
from datetime import datetime, timezone
import uuid


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    now = datetime.now().strftime("%Y-%m-%d")
    text += "-" + now
    if os.path.exists(text):
        text = text + "-" + str(uuid.uuid4())
    return text

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)



