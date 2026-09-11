# Initial Architecture

Status: `DRAFT — PROJECT_OWNER_VALIDATION_REQUIRED`

> À la clôture de l'initialisation, le contrôleur exige exactement `` Status: `VALIDATED` `` sur la ligne ci-dessus.

Ce document enregistre les choix initiaux sans imposer une architecture logicielle, data, automation, API, application ou documentaire.

## Architecture style

`ARCHITECTURE_STYLE: UNKNOWN`

Monolithe, services, tâches, bibliothèque, pipeline, documents ou autre : le choix doit suivre les besoins établis.

## Runtime

`RUNTIME: UNKNOWN`

Valeurs possibles après validation : description du runtime cible ou `NOT_APPLICABLE`.

## Domains and bounded contexts

`UNKNOWN`

Définir seulement les bounded contexts nécessaires, leurs owners et leurs interdictions. Aucun dossier du squelette ne prouve qu’un domaine existe.

## Data and state

`UNKNOWN`

Décrire les états, sources, classifications et autorités de mutation applicables, ou `NOT_APPLICABLE`.

## External systems

`UNKNOWN`

Lister APIs, services, fichiers, personnes ou autres systèmes externes, ou `NOT_APPLICABLE`.

## Contracts and compatibility

Tout échange inter-composants suit `PRODUCER → VERSIONED CONTRACT → CONSUMER`, avec compatibilité et contract tests. Aucun consumer ne lit les internes d’un producer.

## Security, recovery and operations

`UNKNOWN`

Définir accès, secrets, observabilité, backup, recovery, déploiement et preuve runtime selon leur applicabilité.

## Anti-Octopus Review

Compléter `PROJECT_ARCHITECTURE_MAP.md` et obtenir `ANTI_OCTOPUS_REVIEW: APPROVED_BY_PROJECT_OWNER` avant le premier Work Item d’implémentation.
