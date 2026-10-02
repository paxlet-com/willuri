"""Standard system prompt templates and structured JSON schemas for willuri."""
from __future__ import annotations
import json
from typing import Any, Dict, List, Optional


def build_routing_prompt(
    domain_name: str,
    catalog: List[Dict[str, Any]],
    instruction: str,
    input_data: Optional[Dict[str, Any]] = None,
) -> str:
    """Build a deterministic routing prompt for small LLMs."""
    ops_lines = []
    for op in catalog:
        uri = op.get("uri", "")
        desc = op.get("description", "")
        ops_lines.append(f"- {uri}: {desc}")
    catalog_str = "\n".join(ops_lines) if ops_lines else "No predefined operations; synthesize best URI."

    return f"""You are a specialized URI Router for domain '{domain_name}'.
Available target process URIs:
{catalog_str}

User Instruction: {instruction}
Input context: {json.dumps(input_data or {}, ensure_ascii=False)}

Respond ONLY with a JSON object conforming to this schema:
{{
  "uri": "exact target operation URI",
  "input": {{ "param1": "value1" }},
  "domain": "{domain_name}",
  "reasoning": "brief justification"
}}
"""


def build_decomposition_prompt(ticket_title: str, ticket_description: str, catalog: List[Dict[str, Any]]) -> str:
    """Build a prompt for breaking down a high-level sprint ticket into discrete operations."""
    ops_lines = [f"- {op.get('uri')}: {op.get('description', '')}" for op in catalog]
    catalog_str = "\n".join(ops_lines)

    return f"""You are a sprint ticket decomposition specialist.
Break down the following ticket into an ordered sequence of discrete URI operation steps.

Available operations:
{catalog_str}

Ticket: {ticket_title}
Description: {ticket_description}

Respond ONLY with a JSON object:
{{
  "subtasks": [
    {{
      "title": "Subtask title",
      "uri": "willman://operation/...",
      "input": {{}}
    }}
  ]
}}
"""
