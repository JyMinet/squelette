# Worktree Registry

`MAX_ACTIVE_INTEGRATION_CANDIDATES = 1`

Ce registre décrit les worktrees actifs ou récemment clos. Aucun worktree de projet n’est préchargé.

## Modèle obligatoire

Ce bloc est le texte que le contrôleur accepte, à recopier tel quel en remplaçant `NNN` par le
numéro. Les deux balises en font partie : ce sont elles que le contrôleur cherche, et sans elles
l'entrée est déclarée manquante alors qu'elle est là. En Normal Mode, `create-work-item` écrit ce
bloc lui-même ; il ne se rédige à la main que pour le premier Work Item, pendant l'initialisation.

```text
<!-- PROJECT_CONTROL:WI-NNN START -->
WORK_ITEM_ID: WI-NNN
DISPLAY_REFERENCE: WI-NNN
BASE_HEAD: <commit de 40 caractères>
START_HEAD: UNKNOWN
AUTHORIZED_SCOPE: <chemins et comportements autorisés, séparés par des virgules>
BRANCH: work/wi-nnn-<intitulé court>
STATUS: DECLARED
CLOSE_CONDITION: <condition de fusion, d'archivage ou de suppression>
<!-- PROJECT_CONTROL:WI-NNN END -->
```

`DISPLAY_REFERENCE` vaut `WI-NNN` tant qu'aucune clé de projet n'est déclarée, sinon
`<CLÉ>-NNN`. `START_HEAD` vaut `UNKNOWN` avant le démarrage, puis le commit capturé par `start`.

`DECLARED` réserve la branche administrative sans prétendre qu’une implémentation
a commencé. `start` passe l’entrée à `ACTIVE` seulement après checkout et
preflight. `close` la passe à `CLOSED`.
`block` la passe à `BLOCKED`, état non actif, et `resume` la repasse à `ACTIVE`
après résolution autorisée, alignement de la branche sur la canonique (fast-forward
ou commit de merge, jamais de réécriture) et preflight. `START_HEAD` garde le
premier démarrage ; les démarrages suivants figurent dans les Agent Runs, sans
réécriture de provenance. L’historique de maintenance du template lui-même est
tenu dans `provenance/CHANGELOG.md`, jamais dans ce registre.

Un worktree est court, rattaché à un seul Work Item et fermé dès que sa condition
est satisfaite. Deux candidats actifs ou deux scopes `OVERLAPPING` exigent une
décision humaine.
