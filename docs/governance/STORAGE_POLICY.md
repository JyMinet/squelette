# Storage Policy

Status: `CONVENTION — APPLICABILITY_DEFINED_DURING_INITIALIZATION`

Toute donnée utilisée doit être classée avant migration, backup ou suppression. Un projet sans données déclare cette politique `NOT_APPLICABLE`. `UNKNOWN` est valide et bloquant, jamais un raccourci.

| Classe | Critères | Exigence minimale |
|---|---|---|
| `STATIC_REFERENCE` | Référence stable et versionnée | owner, version, source et mise à jour explicites |
| `RUNTIME_MUTABLE` | État modifiable par un runtime autorisé | mutation authority, concurrence, backup et rollback définis |
| `GENERATED_REBUILDABLE` | Reproductible depuis inputs et processus/version connus | préserver inputs, version, manifest et validation |
| `IRREPLACEABLE_PROTECTED` | Unique, humain ou non reconstruisible | copie indépendante, accès minimal, restauration testée; suppression avec GO humain |
| `TEST_FIXTURE` | Synthétique ou figé pour tests | aucun usage runtime/canonique implicite |
| `UNKNOWN` | Classe, owner ou reconstructibilité non établis | préserver; interdire migration, promotion et suppression |

Les emplacements, formats, rétention, chiffrement et accès restent `TODO(PROJECT_OWNER)` ou `NOT_APPLICABLE` jusqu’à validation.
