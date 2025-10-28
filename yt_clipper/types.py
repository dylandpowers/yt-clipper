from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SourceVideo:
    url: str
    title: str
    path: str
    duration: Optional[float]


@dataclass
class TranscriptSegment:
    start_s: float
    end_s: float
    text: str


@dataclass
class CandidateClip:
    source_url: str
    start_s: float
    end_s: float
    text: str
    score: float


@dataclass
class ClipResult:
    file: str
    source_url: str
    start_s: float
    end_s: float
    score: float
    transcript_excerpt: str
    confidence: float


@dataclass
class TimeWindow:
    start_s: float
    end_s: float
    text: str



