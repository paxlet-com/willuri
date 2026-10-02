# willuri

Natural language to specialized process URI router powered by domain-specific lightweight LLMs.

## Overview

In the Paxlet / Willman ecosystem, every capability is addressed by an explicit process URI (`willman://operation/...`, `dockuri://...`). 
`willuri` maps natural language user instructions or tickets from the board to specialized process URIs using small, fast, domain-targeted LLMs instead of a monolithic general-purpose model.

### Specialized Domain Models

| Domain | Process URI Scope | Primary Model | Alternative | Focus |
| :--- | :--- | :--- | :--- | :--- |
| **`code`** | `willman://operation/code.*`, `git.resolve_conflicts` | `qwen2.5-coder:3b` | `willman-nlp:qwen2.5-3b` | Code synthesis, AST edits, diffs, bug repairs |
| **`api_ops`** | `willman://operation/github.*`, `dockuri.*`, `files.*` | `granite4.1:3b` | `willman-nlp:qwen2.5-3b` | Structured API tools, JSON schema, enterprise ops |
| **`planning`** | `willman://operation/koru.*`, `planfile.*`, `schedule.*` | `llama3.2:3b` | `willman-nlp:qwen2.5-3b` | Ticket decomposition, sprint planning, DAG subtasks |
| **`text`** | `willman://operation/text.*` | `willman-nlp:qwen2.5-1.5b` | `willman-nlp:qwen2.5-3b` | String normalization, fast formatting, prose |

## Usage

### Python API
```python
from willuri.router import UriRouter

router = UriRouter()
router.add_operation("willman://operation/text.normalize/v1", "Normalize whitespace")
router.add_operation("willman://operation/git.resolve_conflicts/v1", "Resolve git merge conflicts")

result = router.route("Rozwiąż konflikty git w repozytorium")
print(result["uri"])
# => "willman://operation/git.resolve_conflicts/v1"
print(result["model_used"])
# => "qwen2.5-coder:3b"
```

### CLI
```bash
willuri classify "Popraw błąd w funkcji liczącej sumę"
willuri route "Znormalizuj odstępy w tekście 'Ala   ma   kota'"
```

## Verification
```bash
python3 -m unittest discover -s tests -v
```
