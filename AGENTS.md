# AGENTS.md — Autorité opérationnelle des agents

`AGENTS_CORE: docs/agent-governance/AGENTS.core.md`

Le core déclaré ci-dessus est l’autorité opérationnelle commune à tous les projets
dérivés du squelette. Il est versionné par `provenance/core-manifest.v1.json` et mis à
jour par `template-upgrade` ; `audit` vérifie que ce fichier le déclare et qu’il est
présent. Lire le core intégralement avant toute écriture : ses règles s’appliquent
telles quelles. Ce fichier appartient au projet et ne peut que les renforcer, jamais
les affaiblir. Autorité ambiguë ou contradictoire : `STOP` et décision humaine.

## Règles propres au projet

Aucune. Un projet dérivé ajoute ici ses règles, chacune avec l’autorité qui la fonde
(Charter, ADR ou décision humaine `HD-NNN`).
