"""Fast local semantic matcher and candidate ranker for operations."""
from __future__ import annotations
import math
import re
from typing import Any, Dict, List, Tuple


def tokenize(text: str) -> List[str]:
    """Tokenize text into lowercase alphanumeric keywords."""
    return [t for t in re.findall(r"\w+", text.lower()) if len(t) > 1]


def compute_similarity(tokens_a: List[str], tokens_b: List[str]) -> float:
    """Compute Jaccard token similarity with term frequency weighting."""
    if not tokens_a or not tokens_b:
        return 0.0
    set_a = set(tokens_a)
    set_b = set(tokens_b)
    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)
    return len(intersection) / len(union) if union else 0.0


class SemanticMatcher:
    """Ranks and pre-filters catalog operations against natural language instructions."""

    def __init__(self, catalog: List[Dict[str, Any]]):
        self.catalog = catalog

    def match(self, instruction: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Return the top_k most relevant operations with relevance scores."""
        inst_tokens = tokenize(instruction)
        scored: List[Tuple[Dict[str, Any], float]] = []

        for op in self.catalog:
            text = f"{op.get('uri', '')} {op.get('description', '')} {' '.join(op.get('aliases', {}).keys())}"
            op_tokens = tokenize(text)
            score = compute_similarity(inst_tokens, op_tokens)
            if score > 0.0:
                scored.append((op, round(score, 4)))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
