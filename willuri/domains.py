"""Specialized domain definitions and model bindings for URI routing."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class DomainProfile:
    name: str
    description: str
    preferred_models: List[str]
    uri_prefixes: List[str]
    keywords: List[str]


DOMAIN_REGISTRY: Dict[str, DomainProfile] = {
    "code": DomainProfile(
        name="code",
        description="Software code synthesis, syntax verification, refactoring, and AST transformations.",
        preferred_models=["qwen2.5-coder:3b", "willman-nlp:qwen2.5-3b"],
        uri_prefixes=[
            "willman://operation/code.",
            "willman://operation/python.",
            "willman://operation/git.resolve_conflicts",
            "willman://operation/patch.",
        ],
        keywords=["kod", "funkcja", "refaktoryzacja", "błąd", "python", "rust", "skrypt", "code", "bug", "patch"],
    ),
    "api_ops": DomainProfile(
        name="api_ops",
        description="Structured API calls, GitHub issue tracking, Dockuri containers, Thunderbird mail, and filesystem operations.",
        preferred_models=["willman-nlp:qwen2.5-3b", "granite4.1:3b"],
        uri_prefixes=[
            "willman://operation/github.",
            "willman://operation/dockuri.",
            "willman://operation/files.",
            "willman://operation/thunderbird",
            "dockuri://",
        ],
        keywords=["github", "issue", "zgłoszenie", "plik", "dockuri", "kontener", "katalog", "read", "view", "email", "mail", "thunderbird", "poczta", "wiadomości"],
    ),
    "planning": DomainProfile(
        name="planning",
        description="Sprint planning, ticket decomposition, subtask scheduling, and DAG dependencies.",
        preferred_models=["willman-nlp:qwen2.5-3b", "qwen3.5:2b", "llama3.2:3b"],
        uri_prefixes=[
            "willman://operation/koru.",
            "willman://operation/planfile.",
            "willman://operation/schedule.",
        ],
        keywords=["ticket", "zadanie", "plan", "sprint", "koru", "zależności", "podzadanie", "split", "board"],
    ),
    "text": DomainProfile(
        name="text",
        description="Fast natural language text transformations, string normalization, whitespace, formatting.",
        preferred_models=["willman-nlp:qwen2.5-3b", "willman-nlp:qwen2.5-1.5b"],
        uri_prefixes=[
            "willman://operation/text.",
        ],
        keywords=["tekst", "odstępy", "wielkie", "litery", "normalize", "format", "string", "whitespace"],
    ),
}


def classify_domain(instruction: str, catalog_uris: Optional[List[str]] = None) -> DomainProfile:
    """Classify the target domain from natural language instruction and optional URI catalog."""
    lowered = instruction.lower()

    # Keyword and prefix matching score
    best_domain = DOMAIN_REGISTRY["text"]
    best_score = -1

    for domain in DOMAIN_REGISTRY.values():
        score = 0
        for kw in domain.keywords:
            if kw in lowered:
                score += 2
        if catalog_uris:
            for uri in catalog_uris:
                if any(uri.startswith(prefix) for prefix in domain.uri_prefixes):
                    score += 1
        if score > best_score:
            best_score = score
            best_domain = domain

    return best_domain


def recommend_model(instruction: str, catalog_uris: Optional[List[str]] = None) -> str:
    """Recommend the best specialized model for an instruction."""
    profile = classify_domain(instruction, catalog_uris)
    return profile.preferred_models[0]

