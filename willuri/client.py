"""Specialized LLM inference client for URI parameter extraction and routing."""
from __future__ import annotations
import json
import os
import urllib.request
from typing import Any, Dict, List, Optional


def query_ollama(
    model: str,
    prompt: str,
    schema: Optional[Dict[str, Any]] = None,
    timeout: float = 30.0,
    host: str = "http://127.0.0.1:11434",
) -> Dict[str, Any]:
    """Execute a structured generation query against local Ollama endpoint."""
    url = f"{host.rstrip('/')}/api/generate"
    payload: Dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    if schema:
        payload["format"] = schema
    else:
        payload["format"] = "json"

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        result = json.loads(response.read().decode("utf-8"))

    raw_response = result.get("response", "").strip()
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        return {"raw": raw_response}
