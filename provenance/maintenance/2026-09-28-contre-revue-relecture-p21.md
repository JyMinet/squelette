> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Contre-revue — Relecture V2 de la fiche « Tableau des clés » V1

Date : 2026-09-28. Auteur : Claude (auteur de la fiche contre-revue ; conflit d'intérêt déclaré : chaque constat vise un texte de Claude, d'où la vérification par preuve plutôt que par argument). Lecture seule du dossier `~/Projets/squelette-revue-tableau-des-cles/` ; rien n'y a été écrit.

## Résumé en trois points

1. **Ce qui s'est passé.** Les sept constats de Codex ont été repris un par un. Aucun n'est rejeté : les quatre graves et le bloquant visent de vrais trous de la fiche, dont deux contradictions internes que j'avais écrites moi-même.
2. **Ce que ça change.** La fiche V1 ne se construit pas. Une fiche V2 corrige les sept points ; elle change surtout trois choses : la frontière entre la copie et l'original, ce que « rendre » veut dire, et l'ordre de la promotion.
3. **Ce que Jeoffrey doit faire.** Répondre aux huit questions de la fiche V2 ; décider si la V2 repasse chez Codex (proposé, relecture courte ciblée sur les sept corrections).

## A — Preflight

| Objet | Constat |
|---|---|
| `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V1_V2.md` | 332 lignes, lu en entier |
| `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V1.md` | `da5c28e9…f11f`, inchangé |
| `source/` | 138 fichiers, `sha256sum -c` OK après la relecture |
| `runs/` | présent, fixtures marquées ; non modifié par cette contre-revue |

## B — Vérifications faites

| Constat | Vérification | Résultat |
|---|---|---|
| R01 BLOCKER — cible parente de l'original | Relecture de la fiche §5.3 l. 121 : seuls « égal » et « contenu dans l'original / dans une autre copie » sont refusés ; le sens inverse n'est pas écrit. `runs/results.json` : entrée `P09_ancestor_path` présente. | CONFIRMÉ. Sévérité juste : un effacement récursif d'un contenant emporte l'original. |
| R02 MAJOR — contenu hors branches | Fiche §5.5 l. 134 : seules les branches sont examinées ; l. 137 : la répétition n'a « rien à rendre » sans inventaire. `P06_return_blind_spots` présent. | CONFIRMÉ. La phrase « rien ne reste sans qu'on l'ait dit » était fausse. |
| R03 MAJOR — preuve ancienne au moment d'effacer | Fiche §5.8 : le script revérifie les preuves du registre, pas la copie actuelle ni l'état actuel du registre. `P07_after_return` présent. | CONFIRMÉ, variante `KEPT` comprise. |
| R04 MAJOR — export d'un tag sans ticket | Principe 5 (« la copie emporte son ticket ») contre annexe A (« export du tag v3.20.2 ») : un ticket écrit après le tag n'est pas dans l'export. Ce dossier en est l'exemple même. | CONFIRMÉ. |
| R05 MAJOR — ordre de clôture | Fiche l. 77 (« aucune promotion tant que non rendue ») contre l. 148 (« `copy return` juste après le tag ») : contradiction interne. Contrôleur `source/scripts/project_control.py` l. 4566–4570 : `validate_clean_administrative_baseline` refuse toute transition dès qu'un FAIL d'audit existe — un `copy return` bâti dessus refuserait l'état qu'il doit réparer. | CONFIRMÉ, relu dans le code. |
| R06 MINOR — nom de l'annexe | `tableau-des-cles` n'est ni un chantier, ni une version, ni un ticket (règle l. 110). | CONFIRMÉ. |
| R07 MINOR — coût | La fiche confondait « aucun nouveau document à lire » et « aucun coût ». | CONFIRMÉ. |
| C.4 — `Folder scope` des TPL-D | `grep -c '^Folder scope:' provenance/CHANGELOG.md` = 0 ; 9 mentions en prose. Parseur HD `human_decision_field` l. 1144. | CONFIRMÉ : la vérification du ticket n'existe que pour les HD. |

Observations D-O1 à D-O5 : toutes reçues. D-O5 (« physiquement » : une copie ne retire aucun accès à l'original) et la nuance sur « jamais de suppression » (le contrôleur retire déjà ses propres worktrees jetables) corrigent deux formulations trop fortes de la V1.

## C — Désaccords

Aucun sur le fond. Une précision : l'avis H.2 de Codex (structurer les TPL-D futurs) est retenu comme proposition par défaut dans la fiche V2, la décision restant à Jeoffrey.

## D — Suite

Fiche V2 émise (`FICHE-CADRAGE-TABLEAU-DES-CLES-V2.md`), avec une table « constat → correction ». La relecture et son dossier restent en place tant que Jeoffrey n'a pas décidé de leur rapatriement (double arrêt séparé).

## Verdict

`CADRAGE_TABLEAU_DES_CLES_V1_REVIEW_OF_RELECTURE_V2_PASS`
