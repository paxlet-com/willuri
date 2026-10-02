"""willuri: Universal NL, URI, and specialized LLM router SSOT for Paxlet / Willman."""
from .domains import DOMAIN_REGISTRY, DomainProfile, classify_domain
from .router import UriRouter
from .client import query_ollama
from .dsl import parse_uri, with_params, format_uri, validate_uri
from .models import MODEL_SPECS, get_model_for_domain, generate_modelfile
from .prompts import build_routing_prompt, build_decomposition_prompt
from .semantic import SemanticMatcher, compute_similarity, tokenize

__version__ = "0.2.0"
__all__ = [
    "UriRouter",
    "classify_domain",
    "DOMAIN_REGISTRY",
    "DomainProfile",
    "query_ollama",
    "parse_uri",
    "with_params",
    "format_uri",
    "validate_uri",
    "MODEL_SPECS",
    "get_model_for_domain",
    "generate_modelfile",
    "build_routing_prompt",
    "build_decomposition_prompt",
    "SemanticMatcher",
    "compute_similarity",
    "tokenize",
]
