"""Central model catalog and configuration templates for small specialized LLMs."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ModelSpec:
    name: str
    family: str
    parameters: str
    vram_mb: int
    context_tokens: int
    domains: List[str]
    description: str
    system_prompt: str


MODEL_SPECS: Dict[str, ModelSpec] = {
    "qwen2.5-coder:3b": ModelSpec(
        name="qwen2.5-coder:3b",
        family="qwen2.5",
        parameters="3B",
        vram_mb=2100,
        context_tokens=8192,
        domains=["code"],
        description="High-precision code synthesis, AST analysis, Git conflicts, and automated patches.",
        system_prompt="You are a code synthesis and AST transformation specialist. Return structured code or JSON.",
    ),
    "willman-nlp:qwen2.5-3b": ModelSpec(
        name="willman-nlp:qwen2.5-3b",
        family="qwen2.5",
        parameters="3B",
        vram_mb=2100,
        context_tokens=8192,
        domains=["code", "api_ops", "planning", "text"],
        description="Paxlet tuned generalist model for NL routing, URI parameter extraction, and operations.",
        system_prompt="You are the Paxlet Willman NL-to-URI routing engine. Return exact JSON operations.",
    ),
    "granite4.1:3b": ModelSpec(
        name="granite4.1:3b",
        family="granite",
        parameters="3B",
        vram_mb=1900,
        context_tokens=8192,
        domains=["api_ops"],
        description="Enterprise tool-calling and structured API operations (GitHub, Dockuri, filesystem).",
        system_prompt="You are an API operations specialist. Generate exact JSON API parameters and URI targets.",
    ),
    "llama3.2:3b": ModelSpec(
        name="llama3.2:3b",
        family="llama",
        parameters="3B",
        vram_mb=2200,
        context_tokens=8192,
        domains=["planning"],
        description="Sprint ticket decomposition, dependency DAG planning, and agile backlog management.",
        system_prompt="You are a planning and sprint scheduling specialist. Break tasks into structured DAG steps.",
    ),
    "qwen2.5:1.5b": ModelSpec(
        name="qwen2.5:1.5b",
        family="qwen2.5",
        parameters="1.5B",
        vram_mb=1100,
        context_tokens=4096,
        domains=["text"],
        description="Ultra-lightweight text normalization, string formatting, and fast status checks.",
        system_prompt="You are a fast text transformer. Clean, normalize, and format text strings concisely.",
    ),
}


def get_model_for_domain(domain: str) -> str:
    """Return the primary recommended model for a given domain."""
    for name, spec in MODEL_SPECS.items():
        if domain in spec.domains:
            return name
    return "willman-nlp:qwen2.5-3b"


def generate_modelfile(model_name: str, context_tokens: int = 8192) -> str:
    """Generate an Ollama Modelfile content string for a model."""
    spec = MODEL_SPECS.get(model_name)
    base_from = model_name
    system = spec.system_prompt if spec else "You are an autonomous engineering operations agent."
    return f"""FROM {base_from}
PARAMETER num_ctx {context_tokens}
PARAMETER temperature 0.1
SYSTEM \"\"\"{system}\"\"\"
"""
