from __future__ import annotations

from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .types import CandidateClip, TimeWindow


def compute_scores(prompt: str, windows: List[TimeWindow]) -> List[CandidateClip]:
    texts = [w.text or "" for w in windows]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=20000)
    X = vectorizer.fit_transform([prompt] + texts)
    sims = cosine_similarity(X[0:1], X[1:]).ravel()
    candidates: List[CandidateClip] = []
    for window, score in zip(windows, sims):
        candidates.append(CandidateClip(source_url="", start_s=float(window.start_s), end_s=float(window.end_s), text=window.text, score=float(score)))
    return candidates


def suppress_overlaps(candidates: List[CandidateClip], max_clips: int = 8, min_gap_s: float = 1.0) -> List[CandidateClip]:
    def iou(a: CandidateClip, b: CandidateClip) -> float:
        inter = max(0.0, min(a.end_s, b.end_s) - max(a.start_s, b.start_s))
        union = (a.end_s - a.start_s) + (b.end_s - b.start_s) - inter
        return inter / union if union > 0 else 0.0

    selected: List[CandidateClip] = []
    for c in sorted(candidates, key=lambda x: x.score, reverse=True):
        if len(selected) >= max_clips:
            break
        if any(iou(c, s) > 0.3 for s in selected):
            continue
        if selected and (c.start_s - selected[-1].end_s) < min_gap_s and c.start_s < selected[-1].end_s:
            continue
        selected.append(c)
    return selected



