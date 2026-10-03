---
{
  "schema": "wellmanifest.docs/document/v2",
  "id": "willuri-overview",
  "kind": "information",
  "version": 1,
  "title": "Narzędzia Operacyjne, Prowizjonowanie i Utrzymanie Usług Willman",
  "status": "active",
  "owner": "paxlet-com/willuri",
  "scope": "repository",
  "updated": "2026-10-02",
  "priority": "P2",
  "evidence": [
    "pyproject.toml"
  ]
}
---

# Narzędzia Operacyjne, Prowizjonowanie i Utrzymanie Usług Willman

<!-- docs:section summary -->
## Podsumowanie

Automatyzacja wdrożeń produkcyjnych, konfiguracja usług systemd, orkiestracja kontenerów i monitorowanie telemetryczne klastra.

<!-- docs:section details -->
## Architektura i integracja

Moduł stanowi wydzieloną, wyspecjalizowaną składową ekosystemu `paxlet-com`, realizującą zadania w architekturze wielopakietowej.
Integracja ze standardami Wellmanifest:
- **`wellmanifest/docs` v2**: dokumentacja modułu wersjonowana w Git z jawnym indeksem i nagłówkami metadanych.
- **`wellmanifest/worktrees` v1**: izolacja przestrzeni roboczych agentów za pomocą `worktree-guard.yaml`.
- **`wellmanifest/logs` v1**: rejestracja zdarzeń operacyjnych i katalog runbooków błędów w `errors/`.
- **`wellmanifest/wellman`**: zgodność ze standardem rejestracji i orkiestracji operacji.
