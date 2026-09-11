# Provenance

Conserver ici les références d’origine, manifests, hashes et notes nécessaires pour expliquer comment le projet ou ses artefacts ont été obtenus. Aucun fichier de provenance ne devient une autorité métier ou runtime par sa seule présence.

- `TEMPLATE_PROVENANCE.md` : ascendance vérifiée de la baseline du template ;
- `CHANGELOG.md` : journal des maintenances du template lui-même ;
- `maintenance/` : rapports détaillés de ces maintenances, et sous `maintenance/scopes/` les fiches qui les ont cadrées (revues, scope definitions, mandats) ;
- `roadmap-template.v1.json` et `roadmap-view.v1.json` : la roadmap du squelette lui-même (versions, chantiers, décisions, idées du Project Owner sur le template) et les réglages de sa vue ; `ROADMAP_VIEW.md` et `roadmap/ROADMAP.html` (non suivie) en sont la vue générée par `roadmap-view --write` ;
- `core-manifest.v1.json` : version du squelette et empreintes SHA-256 des fichiers core, régénéré par chaque maintenance du template (`core-manifest --write --version`) et lu par `template-upgrade` dans les projets dérivés.

Ces éléments décrivent le template, jamais le projet dérivé : les records de projet vivent dans `project_control/` et les rapports de projet dans `reports/`. Le manifeste est le seul d’entre eux qu’un projet dérivé met à jour, et seulement par `template-upgrade`.
