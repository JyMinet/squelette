# Architecture Decision Records

Les ADR conservent les décisions techniques/architecturales durables : contexte, options, choix et conséquences. Les Human Decisions conservent l’autorisation ou l’arbitrage propriétaire ; un changement peut nécessiter les deux.

## Convention

- ID : `ADR-NNNN`, stable, croissant, jamais réutilisé.
- Statuts : `PROPOSED`, `ACCEPTED`, `SUPERSEDED`, `REJECTED`.
- Un ADR accepté n’est jamais réécrit pour cacher l’ancien choix ; une nouvelle décision le supersede.
- Un ADR n’autorise pas un Work Item, un artefact canonique ou un cutover sans décision humaine associée.

## Modèle

```markdown
# ADR-NNNN — Title
Status:
Date:
Owners:
Related Human Decision:
Related Roadmap Item:

## Context
## Decision
## Options considered
## Consequences
## Validation and rollback
```
