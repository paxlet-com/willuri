"""Core URI Router converting Natural Language into targeted URI operations."""
from __future__ import annotations
import json
import time
from typing import Any, Dict, List, Optional

from .domains import classify_domain, DOMAIN_REGISTRY, DomainProfile
from .client import query_ollama


class UriRouter:
    """Specialized NL-to-URI process router selecting domain-specific models."""

    def __init__(self, catalog: Optional[List[Dict[str, Any]]] = None, ollama_host: str = "http://127.0.0.1:11434"):
        self.catalog = catalog or []
        self.ollama_host = ollama_host

    def add_operation(self, uri: str, description: str, input_schema: Optional[Dict[str, Any]] = None):
        self.catalog.append({
            "uri": uri,
            "description": description,
            "input_schema": input_schema or {},
        })

    def route(
        self,
        instruction: str,
        input_data: Optional[Dict[str, Any]] = None,
        model_override: Optional[str] = None,
        timeout: float = 20.0,
    ) -> Dict[str, Any]:
        """Route an NL instruction to the best URI operation using a domain-specialized small LLM."""
        start_time = time.monotonic()
        catalog_uris = [op["uri"] for op in self.catalog]
        domain: DomainProfile = classify_domain(instruction, catalog_uris)

        selected_model = model_override or domain.preferred_models[0]

        # Build compact catalog prompt
        ops_text = []
        for op in self.catalog:
            ops_text.append(f"- {op['uri']}: {op.get('description', '')}")
        catalog_str = "\n".join(ops_text) if ops_text else "No predefined operations; synthesize best URI."

        prompt = f"""You are a specialized URI Router for domain '{domain.name}'.
Given the following available process URIs:
{catalog_str}

User Instruction: {instruction}
Input context: {json.dumps(input_data or {}, ensure_ascii=False)}

Respond ONLY with a JSON object containing:
- "uri": the exact matched or generated process URI
- "input": dictionary of extracted arguments matching the operation parameters
- "domain": "{domain.name}"
"""
        response = query_ollama(
            model=selected_model,
            prompt=prompt,
            timeout=timeout,
            host=self.ollama_host,
        )

        duration_ms = round((time.monotonic() - start_time) * 1000, 2)
        return {
            "status": "routed" if "uri" in response else "unsupported",
            "uri": response.get("uri"),
            "input": response.get("input", {}),
            "domain": domain.name,
            "model_used": selected_model,
            "duration_ms": duration_ms,
            "raw": response,
        }
