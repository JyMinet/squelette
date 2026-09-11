> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Fiches de cadrage du template

Ce dossier conserve, dans le dépôt du squelette lui-même, les fiches qui ont cadré
chaque chantier de maintenance du template : revues indépendantes, scope
definitions, mandats. Elles vivaient auparavant dans le projet Claude « Squelette »
et n'étaient donc lisibles que depuis cet outil ; depuis la version 3.8.0 le dépôt
est la source (`TPL-D-017`), le projet Claude n'en garde que des pointeurs.

Règles :

- une fiche par chantier, nommée d'après son identifiant (`pN-…`) ou sa nature
  (`revue-…`, `mandat-…`) ; append-only : une évolution ajoute une section datée ou
  une version (`V2`), jamais une réécriture silencieuse ;
- chaque chantier de `provenance/roadmap-template.v1.json` pointe vers sa fiche par
  le champ `scope` ; la vue ROADMAP (`roadmap-view`) refuse un chemin qui n'existe pas ;
- ces fiches décrivent le template, jamais un projet dérivé. Un projet dérivé hérite
  de ce dossier comme trace de l'ascendance de son template et n'y écrit pas ; ses
  propres cadrages vont sous `docs/` ou `reports/`.

| Fiche | Chantier | Nature |
|---|---|---|
| `revue-squelette-v3.md` | revue initiale (2026-09-05) | revue indépendante, origine des chantiers P1 à P8 |
| `revue-mise-a-jour-codex-v3.md` | mise à jour Codex, redlines, promotion 3.1.0 | contre-revue, corrections, décisions TPL-D-001 à 003 |
| `p1-consolidation-baseline-unique.md` | P1 | scope definition |
| `p2-scope-template-upgrade.md` | P2 | scope definition (V1 à V11) |
| `p3-scope-preuve-lecture-autorites.md` | P3 | scope definition |
| `p4-scope-capability-adversarial-review.md` | P4 | scope definition (non autorisée à ce jour) |
| `p9-scope-records-administratifs-et-branches.md` | P9 | scope definition |
| `p11-scope-style-de-retour.md` | P11 | scope definition (V2) |
| `p12-scope-roadmap-dediee.md` | P12 | scope definition (V2, étapes 1 et 2) |
| `p14-scope-langue-au-choix.md` | P14 | scope definition |
| `p15-scope-amorcage-outille.md` | P15 | fiche de cadrage, close sans être ouverte (TPL-D-048) |
| `p16-scope-garde-fou-de-commit.md` | P16 | fiche de cadrage, livrée en 3.16.1 et 3.16.2 |
| `p17-scope-baseline-defigeable.md` | P17 | fiche de cadrage, réponses du Project Owner et livraison 3.18.0 |
| `p18-scope-publication.md` | P18 | fiche de cadrage : le squelette sait se publier (script d'export anonymisé, 3.19.0) |
| `mandat-codex-alpha-wi-061.md` | P2, étape 2 (Alpha) | mandat retiré, conservé comme trace |
| `roadmap-squelette-memoire-claude.md` | P12, étape 1 | mémoire de la discussion ROADMAP côté Claude, figée à la migration |
