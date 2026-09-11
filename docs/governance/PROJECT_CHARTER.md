# Project Charter

Status: `DRAFT — PROJECT_OWNER_VALIDATION_REQUIRED`

> À la clôture de l'initialisation, le contrôleur exige exactement `` Status: `VALIDATED` `` sur la ligne ci-dessus, et plus aucun marqueur de tâche laissé au propriétaire dans ce document.

`PROJECT_OWNER: UNKNOWN`

Ce Charter est l’autorité supérieure sur la finalité, le périmètre et l’autorité humaine du projet. Il ne doit pas contenir de détails d’implémentation volatils.

## Purpose and Expected Outcome

`TODO(PROJECT_OWNER)`

Décrire le problème réel, le résultat attendu et la valeur recherchée sans présupposer une solution technique ou un type d’application.

## Users and Consumers

`TODO(PROJECT_OWNER)`

Identifier utilisateurs, opérateurs, décideurs éventuels, systèmes consommateurs et personnes affectées, avec leurs besoins et droits.

## Scope

`TODO(PROJECT_OWNER)`

Définir les capacités, domaines, données éventuelles, environnements et étapes explicitement inclus.

## Non-Goals

`TODO(PROJECT_OWNER)`

Énoncer ce que le projet ne doit pas faire afin d’empêcher l’expansion implicite du périmètre.

## Inputs, Outputs and Sources

`TODO(PROJECT_OWNER)`

Décrire les inputs, outputs, consommateurs et sources applicables. Écrire `NOT_APPLICABLE` lorsque le projet n’utilise pas de données ou sources externes, et `UNKNOWN` lorsque l’information n’est pas établie.

## Principles

- Explicit contracts between producers and consumers.
- Human authority for promotions, activation and irreversible change.
- `REUSE > ADAPT > REIMPLEMENT`.
- Unknown information remains `UNKNOWN`.
- Shared infrastructure contains no domain rules.
- When data is applicable: facts before interpretation, primary sources before secondary convenience, provenance before publication.
- When durable records are applicable: corrections create linked revisions instead of silent rewrites.

Adapter ou compléter ces principes exige une décision humaine structurante.

## Human Authority

`TODO(PROJECT_OWNER)`

Nommer les rôles pouvant valider l’architecture, autoriser un Work Item, rendre un artefact canonique, activer une automatisation, autoriser un cutover ou accepter un risque.

Par défaut, une validation humaine explicite est obligatoire pour : changement d’autorité, activation, promotion canonique, production cutover, suppression de données irremplaçables, changement irréversible, conflit architectural et automatisation sensible.

## Success Criteria

`TODO(PROJECT_OWNER)`

Définir des critères observables adaptés au projet : exactitude, délai, disponibilité, adoption, qualité, sécurité ou recovery.

## Risk Tolerance

`TODO(PROJECT_OWNER)`

Préciser les erreurs acceptables/interdites, impacts maximaux, exigences fail-closed et risques nécessitant un GO humain.

## Authority hierarchy

1. Project Owner et décisions humaines explicitement enregistrées ;
2. ce Project Charter ;
3. ADR `ACCEPTED` et documents d’architecture ;
4. contrats versionnés ;
5. roadmap validée et Work Items autorisés ;
6. procédures opérationnelles et implémentation.

Une autorité inférieure ne peut contredire une autorité supérieure. En cas d’ambiguïté : `STOP`.
