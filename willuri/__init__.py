"""willuri: Natural Language to specialized URI process router with domain-specific small LLMs."""
from .domains import DOMAIN_REGISTRY, DomainProfile, classify_domain
from .router import UriRouter
from .client import query_ollama

__version__ = "0.1.0"
__all__ = ["UriRouter", "classify_domain", "DOMAIN_REGISTRY", "DomainProfile", "query_ollama"]
