from __future__ import annotations

from typing import List

from .types import TranscriptSegment, TimeWindow


def rolling_windows_from_transcript(segments: List[TranscriptSegment], window_s: int = 12, min_s: int = 6, max_s: int = 20) -> List[TimeWindow]:
    windows: List[TimeWindow] = []
    buf_text = []
    if not segments:
        return windows
    i = 0
    while i < len(segments):
        start = segments[i].start_s
        end = start
        buf_text.clear()
        j = i
        while j < len(segments) and (end - start) < window_s:
            end = segments[j].end_s
            buf_text.append(segments[j].text)
            j += 1
        # Adjust to bounds
        length = end - start
        if length < min_s:
            # try to extend one more segment if available
            if j < len(segments):
                end = segments[j].end_s
                buf_text.append(segments[j].text)
            length = end - start
        if length > max_s:
            end = start + max_s
        windows.append(TimeWindow(start, end, " ".join(buf_text).strip()))
        i = max(i + 1, j - 1)
    return windows



