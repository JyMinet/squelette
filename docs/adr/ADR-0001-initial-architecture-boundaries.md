# ADR-0001 — Initial architecture boundaries

Status: `PROPOSED — PROJECT_OWNER_ACCEPTANCE_REQUIRED`

> À la clôture de l'initialisation, le contrôleur exige exactement `` Status: `ACCEPTED` `` ou `` Status: `NOT_APPLICABLE — PROJECT_OWNER_VALIDATED` `` sur la ligne ci-dessus.

Date: `UNKNOWN`

Owners: `TODO(PROJECT_OWNER)`

Related Human Decision: `UNKNOWN`

Related Work Item: `UNKNOWN`

## Context

Le projet n’est pas encore initialisé. Ses composants, domaines, runtime, données et interfaces restent `UNKNOWN`.

## Decision

Définir les frontières initiales à partir du Charter et de l’interview. Chaque composant aura un owner, des responsabilités, des interdictions et des contrats publics versionnés. Les shared services resteront techniques et les human gates externes à toute automatisation.

## Options considered

1. structure imposée par le squelette : rejetée, car elle présuppose le projet ;
2. absence de frontières explicites : rejetée, car ownership et changements deviennent ambigus ;
3. frontières minimales validées pendant l’initialisation : option proposée.

## Consequences

- aucun Work Item d’implémentation avant architecture et Anti-Octopus Review validées ;
- `PRODUCER → VERSIONED CONTRACT → CONSUMER` ;
- aucune lecture directe des internes d’un autre owner ;
- toute exception durable exige un ADR et, si elle change l’autorité, une Human Decision.

## Validation and rollback

Validation : architecture initiale complétée, owner map, Anti-Octopus Review approuvée et audit passant. Rollback : superseder cet ADR avant toute implémentation dépendante, sans effacer le document.
