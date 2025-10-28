from __future__ import annotations

from dataclasses import dataclass
from typing import List

from yt_dlp import YoutubeDL


@dataclass
class SearchResult:
    title: str
    url: str
    duration: float | None


def search_youtube(prompt: str, max_results: int = 6, suffix: str = " highlights") -> List[SearchResult]:
    query = f"ytsearch{max_results}:{prompt}{suffix}"
    
    ydl_opts = {
        'quiet': True,
        'flat_playlist': True,
        'extract_flat': True,
    }
    
    results: List[SearchResult] = []
    
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(query, download=False)
        
        if not info_dict:
            return results
        
        entries = info_dict.get('entries', [])
        for entry in entries:
            if not entry:
                continue
            
            url = entry.get("url", "")
            webpage_url = entry.get("webpage_url") or entry.get("url")
            if not webpage_url and url:
                webpage_url = f"https://www.youtube.com/watch?v={url}"
            
            title = entry.get("title", "")
            duration = entry.get("duration")
            
            if webpage_url:
                results.append(SearchResult(title=title, url=webpage_url, duration=duration))
    
    return results



