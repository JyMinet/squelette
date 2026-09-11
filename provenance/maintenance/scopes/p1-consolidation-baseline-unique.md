> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# P1 — Consolidation vers une baseline unique du squelette

Statut : `PARTIELLEMENT EXÉCUTÉ — HUMAN_DECISION_REQUIRED pour la suite`
Mandat d'écriture accordé le 2026-09-05 : mise en conformité de V3, puis portage dans `gouverne`. Exécuté ; voir § 8.

## 1. État constaté (2026-09-05, avant intervention)

| Copie | Git | Écart | Audit |
|---|---|---|---|
| `squelette-decision-projet` | `main` `bede17a`, `refactor` | contrôleur 36 Ko, tests 8 Ko, pas de `project-state.v1.json` ni de schéma roadmap | non exécuté |
| `squelette-projet-gouverne` | `main` `b565130`, `fix` `becc60f` | contrôleur 85 Ko, tests 35 Ko, socle complet | `bootstrap-audit` PASS (16), `audit` PASS (13) |
| `Squelette V3 -runtime-proof` | **aucun dépôt** | = `gouverne@becc60f` + `ADOPTION.md` + `runtime_proof/` (22 fichiers ajoutés) | `bootstrap-audit` **FAIL** : `GIT_REPOSITORY`, `BOOTSTRAP_CHANGE_SCOPE` |

## 2. Ascendance — vérifiée, contrairement à la déclaration

Comparaison des hashes d'objets Git, fichier par fichier :

- V3 contre `becc60f` (gouverne) : **50 des 52 fichiers communs identiques** ; écarts = `README.md` et `data/README.md` ; 22 fichiers ajoutés.
- V3 contre `bede17a` (decision-projet) : 17 fichiers identiques sur 74. **Ascendance directe exclue.**

`TEMPLATE_PROVENANCE.md` de V3 n'était donc pas faux mais **périmé** : hérité verbatim de `gouverne`, il décrivait l'origine de *gouverne*. Chaîne réelle : `bede17a → becc60f → V3`, avec un maillon non enregistré.

## 3. Défaut central

Le squelette impose `ONE_CANONICAL_BASELINE`, `CANONICAL REPOSITORY` et l'interdiction de déduire un HEAD canonique d'un checkout non versionné. Sa version la plus avancée violait les trois.

## 4. Angle mort identifié — mode `TEMPLATE_MAINTENANCE` manquant

Le template ne peut pas se modifier lui-même sous ses propres règles. En `NOT_STARTED`, il est en Bootstrap Mode, dont l'allowlist ne couvre ni `CLAUDE.md`, ni `provenance/`, ni le core. `AGENTS.md` exige pour la maintenance du core « un mandat humain explicite, une branche dédiée et les contrôles du dépôt source », mais ce régime n'est formalisé nulle part et n'est pas contrôlé par le moteur. Il manque un troisième mode, avec sa propre allowlist.

## 5. Cible

Un dépôt unique, portant `main` comme branche canonique, des tags de version, un `REPOSITORY_STATUS.md` renseigné pour le template lui-même, un `CHANGELOG.md`, et une provenance vérifiée.

## 6. Gates humaines restantes

- fusion de `feat/adoption-and-runtime-proof-v3` vers `main` — promotion canonique ;
- classement des deux branches `fix/…` non fusionnées de `gouverne` ;
- sort de `squelette-decision-projet` et de la copie V3 devenue redondante ;
- pose des tags de version ;
- push éventuel vers le bare NAS.

## 7. Risques restants

- `main` de `gouverne` est **2 commits en retard** (`b565130`) : la branche canonique du template ne porte pas le contenu audité. Tant que c'est vrai, toute copie faite depuis `main` produit un projet sur un socle périmé.
- Les branches `fix/governed-bootstrap-architecture` et `fix/project-control-simplification-v3` ne sont pas fusionnées.

## 8. État d'exécution (2026-09-05)

### Étape A — V3 rendu conforme et versionné

- dépôt Git autonome initialisé, branche `main`, commit `35da2a2`, 75 fichiers suivis ;
- `provenance/TEMPLATE_PROVENANCE.md` : chaîne d'ascendance complète, maillon `becc60f` enregistré avec sa vérification, énoncé d'origine conservé et erratum `ERR-01` — révision liée, pas réécriture silencieuse ;
- `CLAUDE.md` ajouté : point d'entrée agent renvoyant à `AGENTS.md`, sans autorité propre ;
- aucun changement du core, des schémas, du contrôleur ni des tests.

Vérification : `bootstrap-audit` **PASS (16/16)**, `audit` **PASS**, `check_git_traceability` **PASS**, **28 tests OK**.

### Étape B — Portage dans `gouverne`

- branche dédiée `feat/adoption-and-runtime-proof-v3`, créée depuis `becc60f`, commit `510b09e` ;
- 25 fichiers : `ADOPTION.md`, `CLAUDE.md`, `README.md`, `data/README.md`, `runtime_proof/` (21) ;
- `provenance/TEMPLATE_PROVENANCE.md` **non porté** — celui de `gouverne` décrit l'origine de `gouverne` ;
- diff contre la base : 25 fichiers, +347 / −11.

Vérification : `bootstrap-audit` PASS, `audit` PASS, traçabilité PASS, 28 tests OK.
Écart résiduel V3 ↔ branche de portage : **1 fichier sur 75**, la provenance, écart voulu.

**Aucune fusion vers `main`.** La promotion canonique reste une décision humaine.

### Incident d'exécution

Git n'a pas pu supprimer ses fichiers temporaires (suppression désactivée sur les dossiers connectés) : `.git/HEAD.lock`, `maintenance.lock` et 112 objets `tmp_obj_*` sont restés dans V3, et un `index.lock` obsolète bloquait déjà `gouverne`. Nettoyés après autorisation explicite ; `git fsck` sain, écriture Git revérifiée sur les deux dépôts.
