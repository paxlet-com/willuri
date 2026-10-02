"""Unit tests for willuri DSL, models, and semantic matching."""
import pytest
from willuri import (
    parse_uri,
    with_params,
    format_uri,
    validate_uri,
    MODEL_SPECS,
    get_model_for_domain,
    generate_modelfile,
    SemanticMatcher,
)


def test_dsl_with_params_and_parse():
    base = "willman://operation/git.status"
    params = {"path": "/home/tom/github/willman", "short": True}
    uri = with_params(base, params)
    assert uri.startswith("willman://operation/git.status?")
    assert "path" in uri

    parsed_base, parsed_params = parse_uri(uri)
    assert parsed_base == base
    assert parsed_params["path"] == "/home/tom/github/willman"
    assert parsed_params["short"] is True


def test_dsl_format_and_validate():
    uri = format_uri("dockuri", "container", "redis", {"port": 6379})
    assert uri == "dockuri://container/redis?port=6379"
    assert validate_uri(uri) is True
    assert validate_uri("invalid://something#frag") is False


def test_model_specs():
    coder = MODEL_SPECS["qwen2.5-coder:3b"]
    assert coder.parameters == "3B"
    assert coder.context_tokens == 8192
    assert "code" in coder.domains

    model = get_model_for_domain("code")
    assert model == "qwen2.5-coder:3b"

    modelfile = generate_modelfile(model)
    assert "FROM qwen2.5-coder:3b" in modelfile
    assert "num_ctx 8192" in modelfile


def test_semantic_matcher():
    catalog = [
        {"uri": "willman://operation/git.status", "description": "Sprawdź status repozytorium git i zmodyfikowane pliki"},
        {"uri": "willman://operation/dockuri.run", "description": "Uruchom kontener dockuri w środowisku sandbox"},
    ]
    matcher = SemanticMatcher(catalog)
    results = matcher.match("jaki jest git status plikow?")
    assert len(results) > 0
    assert results[0][0]["uri"] == "willman://operation/git.status"
