"""Universal URI DSL for Paxlet / Willman ecosystem."""
from __future__ import annotations
import json
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from typing import Any, Dict, Tuple, Set

SUPPORTED_SCHEMES: Set[str] = {"willman", "proc", "dockuri", "paxlet"}


def with_params(uri: str, params: Dict[str, Any]) -> str:
    """Encode query parameters onto a base URI with deterministic JSON encoding."""
    if urlsplit(uri).query:
        raise ValueError("Base URI already has query parameters")
    if not isinstance(params, dict):
        raise ValueError("URI parameters must be a JSON object")
    query = urlencode([
        (str(key), json.dumps(value, ensure_ascii=False, separators=(",", ":")))
        for key, value in sorted(params.items())
    ])
    return uri + ("?" + query if query else "")


def parse_uri(uri: str) -> Tuple[str, Dict[str, Any]]:
    """Parse a URI into base URI and decoded parameter dictionary."""
    parsed = urlsplit(uri)
    if parsed.scheme not in SUPPORTED_SCHEMES or not parsed.netloc or parsed.fragment:
        raise ValueError(f"Expected valid URI scheme in {SUPPORTED_SCHEMES} without fragment, got: {uri}")
    values: Dict[str, Any] = {}
    for key, raw in parse_qsl(parsed.query, keep_blank_values=True, strict_parsing=True):
        if key in values:
            raise ValueError(f"Duplicate URI parameter: {key}")
        try:
            values[key] = json.loads(raw)
        except json.JSONDecodeError:
            values[key] = raw
    base = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
    return base, values


def format_uri(scheme: str, entity_type: str, path: str, params: Dict[str, Any] | None = None) -> str:
    """Construct a canonical URI for an operation, container, or task."""
    clean_path = path.lstrip("/")
    base = f"{scheme}://{entity_type}/{clean_path}"
    return with_params(base, params) if params else base


def validate_uri(uri: str) -> bool:
    """Check whether a URI is syntactically valid."""
    try:
        parse_uri(uri)
        return True
    except Exception:
        return False
