# Project Architecture Map

Status: `INITIAL_TEMPLATE — PROJECT_OWNER_VALIDATION_REQUIRED`

> À la clôture de l'initialisation, le contrôleur exige exactement `` Status: `VALIDATED` `` sur la ligne ci-dessus.

Cette carte devient l’autorité sur les composants, owners, dépendances et mutations seulement après initialisation. Aucun composant, domaine, runtime ou type d’application n’est présupposé.

Principe d’intégration : `PRODUCER → VERSIONED CONTRACT → CONSUMER`.

Un consumer connaît la version du contrat public, jamais les chemins, tables, classes, fichiers ou stores internes du producer.

## Component Map

Ajouter un bloc par composant réellement nécessaire :

```text
COMPONENT_ID: UNKNOWN
OWNER: UNKNOWN
PURPOSE: UNKNOWN
INPUTS: UNKNOWN
OUTPUTS: UNKNOWN
CONTRACTS: UNKNOWN
DEPENDENCIES: UNKNOWN
CONSUMERS: UNKNOWN
MUTATION AUTHORITY: UNKNOWN
MUST NOT DO: UNKNOWN
RUNTIME: UNKNOWN | NOT_APPLICABLE
```

Une ligne `UNKNOWN` bloque l’implémentation qui en dépend. `NOT_APPLICABLE` exige une décision explicite, jamais une supposition.

## Shared technical services

Un service partagé peut fournir transport, primitives de stockage, hashing, scheduling, logging, métriques techniques, identité technique ou notifications. Il ne possède aucune règle d’un domaine.

Un orchestrateur ne connaît que :

```text
job_id
dependencies
order
timeout
status
result
```

Le contenu du `result` est opaque à l’orchestrateur et validé par le domaine ou contrat propriétaire.

## Anti-Octopus Review

À compléter et faire valider avant tout Work Item d’implémentation :

| Question | Initial status | Required evidence |
|---|---|---|
| Chaque règle ou capacité de domaine a-t-elle un seul owner ? | UNKNOWN | owner map |
| Les dépendances passent-elles uniquement par contrats publics versionnés ? | UNKNOWN | dependency map |
| Un shared service connaît-il une règle, un seuil ou un calcul de domaine ? | UNKNOWN | service review |
| Un domaine lit-il les internes d’un autre domaine ? | UNKNOWN | access map |
| L’orchestrateur est-il limité aux six champs techniques autorisés ? | UNKNOWN | orchestration contract |
| Une interface recalcule-t-elle une valeur autoritative ? | UNKNOWN | output trace |
| Une abstraction est-elle créée sans deux besoins compatibles prouvés ? | UNKNOWN | reuse analysis |
| Les autorités de mutation et human gates sont-elles explicites ? | UNKNOWN | mutation matrix |

Un `UNKNOWN`, chevauchement ou owner ambigu bloque la validation. Résultat final attendu : `ANTI_OCTOPUS_REVIEW: APPROVED_BY_PROJECT_OWNER`, associé à un `HD-NNN`.
