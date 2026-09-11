> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# P2 — Scope Definition V1 : `skeleton_version` et `template-upgrade`

Statut : `SCOPE_DEFINITION_V11 — STEP_2_DONE_ON_REAL_Alpha (WI-061, v3.6.1) — NAS_PUSH_BY_PROJECT_OWNER_PENDING` (V1 à V10 conservées ci-dessous ; étape 1 promue en v3.3.0 § 10 ; étape 1b promue en v3.4.0 § 11 ; correctif v3.4.1 promu § 12 ; dérive et retour arrière § 13 ; retour arrière vérifié § 14 ; répétition sur copie avec v3.5.0 verte § 15 ; impasse 3.6.0 et redline RL-T-01 § 16 ; correctif 3.6.1 et routine verte dans la copie § 17 ; étape 2 exécutée dans le vrai Alpha § 18)
Nature : définition de périmètre. Aucun code n'est produit. L'entrée manquante est l'inspection en lecture seule d'un projet dérivé réel (`alpha`) pour établir comment son core a divergé ; les points marqués `UNKNOWN` en dépendent.
Baseline examinée : `Squelette V3 -runtime-proof`, `main` = `64a3cb1` (`v3.1.0`).

## 1. Problème

Un projet dérivé emporte une copie du core du template (contrôleur, tests du template, schémas, `AGENTS.md`, routage des autorités, Definition of Done). Quand le template corrige son core — `v3.1.0` a changé le contrat des preuves et rendu `start_head` et `runtime_target` obligatoires — rien ne porte la correction vers les projets dérivés, et rien ne dit de quelle version chacun dérive. À l'inverse, les améliorations génériques nées dans un projet (le « retour d'expérience V8 » de Codex) remontent à la main, sans trace de ce qui est core et de ce qui est projet. À cinq projets, chacun est un fork silencieux.

## 2. Scénarios d'échec démontrés

**S-01 — Contrôleur neuf sur records anciens.** Un projet dérivé de `v3.0.0` remplace son `scripts/project_control.py` par celui de `v3.1.0` : `audit` échoue (`missing start_head; missing runtime_target`) sur tous ses Work Items (reproduit le 2026-09-06, scénario E6). L'incompatibilité est documentée, sans chemin de migration.

**S-02 — Core modifié localement, écrasé.** Un projet a adapté son contrôleur (Alpha en est un : Codex y décrit « le contrôleur générique présent dans le projet consommateur »). Une mise à jour par copie écrase ces adaptations sans les voir.

**S-03 — Version inconnue.** `provenance/TEMPLATE_PROVENANCE.md` donne le commit d'origine, pas la version du template ni la liste des fichiers core à cette version. Impossible de calculer un diff « core attendu / core présent » sans le dépôt du template sous la main.

## 3. Objectif

Qu'un projet dérivé puisse constater son écart au core du template, l'absorber quand ses fichiers core sont intacts, refuser quand ils ont été modifiés localement, et migrer ses records explicitement — sans dépendance externe et sans deviner.

## 4. Non-objectifs

- Ne pas synchroniser automatiquement les projets (pas de push du template vers les projets).
- Ne pas fusionner des modifications locales du core : refuser et lister.
- Ne pas migrer les records sans décision humaine par version.
- Ne pas imposer un dépôt distant : la source est un chemin ou une archive du template.

## 5. Contrat proposé

### 5.1 Identité de version

- `project_control/project-state.v1.json` gagne `skeleton_version` (`"3.1.0"`), obligatoire dès l'initialisation, et `skeleton_core_manifest` (chemin du manifeste, voir 5.2).
- Le template porte sa version dans `provenance/CHANGELOG.md` (déjà) et dans un tag Git (`v3.1.0`, déjà).

### 5.2 Manifeste du core

`provenance/core-manifest.v1.json`, généré par le template à chaque version : liste close des fichiers core avec leur SHA-256. Ensemble core proposé : `AGENTS.md`, `CLAUDE.md`, `FIRST_START.md`, `ADOPTION.md`, `scripts/`, `tests/test_template.py`, `tests/fixtures/project_control/`, `project_control/schemas/`, `project_control/README.md`, `docs/agent-governance/`, `docs/governance/DEFINITION_OF_DONE.md`. Hors core : Charter, roadmap, décisions, architecture, records, `applications/`, `modules/`, `shared/`, `contracts/`, `data/`, `reports/`, `runtime_proof/` (pack optionnel, à trancher).

Un projet dérivé emporte le manifeste de sa version d'origine : le diff local est calculable hors ligne.

### 5.3 Commande `template-upgrade`

```text
python3 -B scripts/project_control.py template-upgrade --source <chemin du template> [--to <version>] [--dry-run]
```

- lit `skeleton_version` du projet et le manifeste de la source ;
- classe chaque fichier core : `UNCHANGED_LOCALLY` (hash = manifeste d'origine) → mis à jour ; `MODIFIED_LOCALLY` → refusé, listé ; `ABSENT` → ajouté ; `REMOVED_UPSTREAM` → signalé ;
- refuse globalement si un fichier `MODIFIED_LOCALLY` existe et qu'aucune décision `--accept-local <path>` / `--overwrite <path>` n'est fournie ;
- ne touche jamais un record ; met à jour `skeleton_version` seulement si tous les fichiers core sont alignés ;
- `--dry-run` est la sortie par défaut du premier appel : rapport, aucune écriture.

En Normal Mode, l'exécution s'inscrit dans un Work Item dont les `authorized_paths` couvrent les chemins core (`scripts/`, `tests/`, `project_control/schemas/`, …) : aucun nouveau mode n'est nécessaire, `preflight` et le hook de commit s'appliquent tels quels. En Bootstrap Mode, une mise à jour du core reste interdite (allowlist), conformément à `AGENTS.md`.

### 5.4 Migration des records

`migrate-records --from 3.0.0 --to 3.1.0`, une transformation explicite par saut de version, refusant toute inférence : `start_head` absent → `UNKNOWN` pour un Work Item `AUTHORIZED`, refus pour un Work Item déjà démarré (le démarrage réel n'est pas reconstructible) ; `runtime_target` absent → `NOT_APPLICABLE` seulement si les deux gates runtime sont `NOT_APPLICABLE`, refus sinon ; `close_head` absent sur un `DONE` → refus, décision humaine (`HD`) qui fixe le commit ou reclasse le Work Item. Chaque refus est nominatif.

## 6. Impacts

- `DIRECT` : `project-state.v1.schema.json` (nouveau champ), `scripts/project_control.py` (deux commandes), `provenance/core-manifest.v1.json` (généré), `FIRST_START.md`, `project_control/README.md`, tests.
- `INDIRECT` : tous les projets dérivés existants — Alpha d'abord — qui doivent recevoir `skeleton_version` par une migration initiale ; leur core diverge peut-être déjà.
- `AUTHORITY` : la définition de « core » devient un contrat versionné (autorité nouvelle) ; décision humaine requise sur l'ensemble core (5.2).
- `CONCURRENT` : P9 modifie le contrôleur en profondeur — livrer P2 après P9 pour que le manifeste `v3.2.0` capture le core stabilisé. P3 ajoute des champs aux Agent Runs : à inclure dans la même version.

## 7. Points non tranchés

- Ensemble exact des fichiers core, et statut de `runtime_proof/` : `UNKNOWN`.
- Écart réel du core d'Alpha par rapport à `v3.0.0`/`v3.1.0` (fichiers modifiés, dans quel sens) : `UNKNOWN` — exige la lecture du dépôt `alpha`.
- Faut-il un `--accept-local` (le projet garde sa version et la déclare comme divergence enregistrée) : `UNKNOWN`.
- Sens montant : comment un projet propose une amélioration générique au template (retour d'expérience) — hors périmètre de V1, à noter.

## 8. Critères de fermeture proposés

1. Sur une copie neuve `v3.1.0`, `template-upgrade --dry-run` vers la même version rapporte zéro écart.
2. Sur une copie `v3.0.0` intacte, l'upgrade vers `v3.1.0` met à jour le core, refuse les records non migrés, puis `migrate-records` les migre ou les refuse nominativement ; `audit` PASS ensuite.
3. Un fichier core modifié localement est refusé et listé ; rien n'est écrit.
4. `skeleton_version` ne change que si le core est intégralement aligné.
5. Acceptation réelle : `template-upgrade --dry-run` exécuté sur `alpha` (lecture seule) produit un rapport exploitable par le Project Owner.
6. Suite complète verte ; aucune dépendance hors bibliothèque standard.

---

## 9. Révision V2 — constats de l'inspection de `alpha` (2026-09-07, lecture seule)

Méthode : lecture des métadonnées Git et des fichiers (`git ls-tree`, `git show`, `git log`), comparaison des blobs core avec `bede17a`, `becc60f`, `v3.0.0`, `v3.1.0` ; aucune écriture, aucune commande Git modifiante, aucun script du dépôt exécuté ; `git status` vierge avant et après.

**État.** `main` = `8038b78` (2026-09-06), propre ; remote `nas` = `/Volumes/SAUVEGARDE/alpha.git` ; 60 Work Items (59 `DONE`, 1 `BLOCKED`), 60 Agent Runs, une branche par Work Item ; initialisé le 2026-08-21 (`baseline_head` `c5efb29`, `HD-002`).

**Origine.** `TEMPLATE_PROVENANCE.md` déclare `bede17a` (première génération, `squelette-decision-projet`). Or plusieurs fichiers core sont identiques à `becc60f` et suivants (`check_git_traceability.py`, schémas `project-state`, `roadmap-state`, `conversation-reference`, fixture conversation) : le projet a absorbé des éléments de la génération suivante sans que la provenance le dise — S-03 confirmé sur un cas réel.

**Écart du core.** Tous les fichiers core pilotés — `AGENTS.md` (133 lignes différentes sur 188), `FIRST_START.md`, `README.md`, `project_control/README.md`, `scripts/project_control.py` (618 lignes différentes sur ~3 200), `tests/test_template.py` (1 703 lignes différentes), schémas `work-item` et `agent-run`, fixtures, `mandatory-documents.v1.json`, DoD — diffèrent de **toutes** les versions du template ; chacun porte 5 commits locaux entre le 2026-08-20 et le 2026-09-06. `MODIFIED_LOCALLY` est donc la règle, non l'exception : un `template-upgrade` qui refuse tout fichier modifié refuserait tout, sur ce projet.

**Convergence récente.** Le Work Item `WI-060` (« Project Control : reprise V3 et compatibilité historique », clos le 2026-09-06 par Codex) a appliqué au contrôleur V8 `status`, la validation stricte et les preuves vérifiables de V3, puis « alimenté V3 avec les acquis génériques de V8 » (blocage/reprise, provenance des runs). Les deux contrôleurs sont aujourd'hui à 618 lignes l'un de l'autre ; `evidence.v1.schema.json` est **le même blob** (`638a1f8`) des deux côtés. Les fonctions présentes d'un seul côté : côté V8, `legacy_records`, `legacy_record`, `legacy_evidence_prefixes`, `migration_errors` ; côté template, les ajouts de `claude/v3-redlines` (`merge_canonical_into_branch`, `latest_run_start_head`, `evidence_directory`) et du hook.

**Le modèle de compatibilité historique de V8, à réutiliser.** Les 59 Work Items historiques portent des preuves en texte libre (« `python3 -B -m unittest … : 36/36 PASS at <sha>` ») et aucun `close_head` ; seul `WI-060` est clos sous le nouveau contrat. V8 ne les a pas migrés : il fixe une **baseline d'adoption** (`LEGACY_EVIDENCE_BASELINE = d4d7b5a…`, constante du contrôleur), lit les records tels qu'ils étaient à ce commit, exige qu'ils soient toujours présents et que leur historique de preuves n'ait pas changé (`migration_errors`, `legacy_evidence_prefixes`), et n'applique la validation stricte qu'au travail postérieur. Un test dédié (`tests/test_evidence_migration.py`) rejoue cette politique sur un clone historique. C'est exactement la réponse à S-01 : **figer l'histoire à un commit d'adoption, être strict vers l'avant**, sans inventer de `close_head`. Les champs `start_head` et `runtime_target` sont par ailleurs déjà présents sur les 60 records (posés lors de WI-060).

### Points tranchés par l'inspection

- Écart réel du core d'Alpha : global, cinq commits locaux par fichier, convergence récente vers v3.1 ; la constante `LEGACY_EVIDENCE_BASELINE` et `AGENTS.md` sont les seules divergences de fond après WI-060.
- Migration des records : **ne pas migrer** ; adopter le modèle de baseline d'adoption de V8, porté dans `project-state.v1.json` (`legacy_baseline`) plutôt qu'en constante du contrôleur, avec `migration_errors` intégré à `audit`. Le 5.4 de V1 est remplacé.
- `--accept-local` : inutile si le core absorbe d'abord les divergences génériques de V8 (`REUSE > ADAPT`) ; le seul fichier légitimement local est `AGENTS.md`.

### Contrat V2 (remplace 5.3 et 5.4 sur ces points)

1. **Sens de la première synchronisation : template ← V8, puis V8 ← template.** Étape 1 : le template absorbe le modèle de baseline d'adoption (champ `legacy_baseline`, contrôles `LEGACY_RECORDS_PRESENT` et `LEGACY_EVIDENCE_FROZEN` dans `audit`, test rejouant un clone historique) — livrable `v3.2.x`. Étape 2 : Alpha remplace son core par celui du template dans un Work Item dont les `authorized_paths` couvrent le core ; après quoi ses fichiers core sont `UNCHANGED_LOCALLY` et `template-upgrade` devient applicable en routine.
2. **`AGENTS.md` scindé.** Le core template vit dans `docs/agent-governance/AGENTS.core.md` (fichier core, versionné par le manifeste) ; `AGENTS.md` à la racine reste au projet, commence par une inclusion de référence au core et ne peut que renforcer (`AGENTS.md:3`, règle existante) ; `audit` vérifie que le core référencé est celui du manifeste. Sans cela, `AGENTS.md` serait `MODIFIED_LOCALLY` à vie.
3. **Manifeste et `skeleton_version`** inchangés par rapport à V1 (5.1, 5.2) ; `runtime_proof/` hors core (pack optionnel).
4. **`template-upgrade`** inchangé dans son principe (5.3) : mise à jour des fichiers intacts, refus nominatif des fichiers modifiés, `skeleton_version` seulement si tout est aligné, `--dry-run` par défaut. Critère d'acceptation réel : `--dry-run` sur Alpha après l'étape 2 rapporte zéro écart hors `AGENTS.md`.

### Impacts révisés

- `CONCURRENT` : l'étape 1 modifie `audit` et le validateur ; P9 (option A retenue) modifie `start`/`block`/`resume`/`close`. Ordre : P9 → P2 étape 1 → P3, dans une même série `v3.2.x`, puis P2 étape 2 sur Alpha sous Work Item.
- `INDIRECT` : Alpha gagne à l'étape 2 le hook de commit, l'alignement de reprise et l'auto-autorisation du dossier de preuves, et perd sa constante locale au profit d'un champ de record.

### Points restant non tranchés

- Faut-il exposer `legacy_baseline` aussi par Work Item (un projet peut adopter par vagues) : `UNKNOWN`.
- Format de l'inclusion du core dans `AGENTS.md` (ligne de référence + hash, ou copie contrôlée) : `UNKNOWN`.

---

## 10. V3 — étape 1 livrée : baseline d'adoption (2026-09-07)

Statut : `SCOPE_DEFINITION_V3 — STEP_1_IMPLEMENTED_ON_BRANCH — NOT_PROMOTED`

### Mandat et livraison

- Mandat : « ok je te suis ! » (2026-09-07), sur la proposition « promouvoir `v3.2.0` puis ouvrir P2 étape 1 ». `v3.2.0` promu et poussé (GitHub `origin` et NAS `nas`, tous deux à `713e472`).
- Branche `claude/v3.3-legacy-baseline`, deux commits depuis `main` (`713e472`, `v3.2.0`) : `5dc21a0` README bilingue (mandat « L'anglais devra être saisi ! » ; commits et tags restent en français) ; `f156786` baseline d'adoption. Non promu.
- `alpha` : lecture seule respectée — inspection par `git show` / `git archive` du template, aucun script d'Alpha exécuté, `git status` vierge avant et après (`8038b78`).

### Ce qui est implémenté

- `project-state.v1.json` : `legacy_baseline` obligatoire, `null` sans histoire antérieure, sinon `{"head": <commit 40>, "human_decision_ref": "HD-NNN"}`. Schéma mis à jour ; `NOT_STARTED` ne peut pas déclarer de baseline.
- `audit` : `LEGACY_RECORDS_PRESENT` (chaque Work Item enregistré à la baseline existe toujours) et `LEGACY_EVIDENCE_FROZEN` (un `DONE` à la baseline conserve exactement ses octets ; pour les autres, les références de preuve de la baseline restent un préfixe inchangé de chaque gate). Baseline absente, hors historique, mal formée ou sans décision enregistrée : audit et `status` en échec, sans traceback, message nominatif ; `HEAD` n'est jamais substitué.
- `done_evidence_errors` : un `DONE` antérieur à la baseline n'est ni reconstruit ni requalifié ; un `DONE` postérieur exige `close_head` dans l'historique et de nouvelles preuves structurées après le préfixe historique. L'exigence `close_head` quitte le validateur pur pour ce contrôle Git (seul endroit qui connaît la baseline).
- `status` : `legacy_baseline` dans la charge JSON ; `evidence_validation` par Work Item (`LEGACY_PRESERVED`, `STRUCTURED_VERIFIED`, `PENDING`, `INVALID`, mêmes valeurs qu'Alpha pour ne pas changer ses lecteurs) ; vue texte « dont N figés avant la baseline d'adoption ».
- Documents : `AGENTS.md` (autorité : clôtures antérieures figées, jamais reconstruites), `DEFINITION_OF_DONE.md` (section « Clôtures antérieures à la baseline d'adoption »), `project_control/README.md` (« Compatibilité : baseline d'adoption » remplace la migration explicite de records), `FIRST_START.md`, `MIGRATION_RULES.md` (l'adoption n'est pas une migration), `provenance/CHANGELOG.md`.
- Tests : 79 (deux nouveaux) — `test_legacy_baseline_freezes_history_and_requires_new_proof_forward` (clôture historique sans `close_head` refusée sans baseline, acceptée et figée avec ; octets modifiés ou record supprimé refusés ; reprise d'un bloqué historique : préfixe conservé, texte libre refusé à la clôture, preuve structurée acceptée, préfixe non supprimable) et `test_legacy_baseline_must_be_declared_by_a_recorded_decision_in_current_history` (commit hors historique, décision non enregistrée, tête mal formée, déclaration manquante ; déclaration valide acceptée telle quelle ; aucun champ additionnel n'exempte un record).

### Acceptation sur données réelles (Alpha, lecture seule)

Contrôleur du template (extrait de la branche par `git archive`, exécuté hors d'Alpha) appliqué aux records d'Alpha à `8038b78`, avec `legacy_baseline` = `d4d7b5ad…` / `HD-065` injecté en mémoire :

- `project-state` non modifié : une seule erreur, nominative — `missing legacy_baseline`. C'est le seul changement de record que l'étape 2 demandera à Alpha.
- `legacy_audit` : 59 Work Items figés à `d4d7b5ad`, 0 erreur de présence, 0 erreur de gel.
- `validate_work_item` (validateur du template) : 60/60 records valides.
- `done_evidence_errors` : 0 erreur — 58 `DONE` historiques préservés, WI-060 (structuré) vérifié par le contrôleur du template.
- `validate_record_links` : 0 erreur.

Le critère 5 de V1 (« rapport exploitable sur Alpha ») est rempli pour l'étape 1 : le core du template accepte l'historique d'Alpha sans migration.

### Points tranchés

- `legacy_baseline` par projet, pas par Work Item : une seule baseline suffit à Alpha ; l'adoption par vagues n'a pas de cas réel. (Point non tranché de V2, clos par `OMIT > ACTIVATE WITHOUT NEED`.)
- Champ obligatoire plutôt qu'optionnel : un projet déclare explicitement qu'il n'a pas d'histoire (`null`) ; la seule casse est une ligne à ajouter, signalée nominativement.

### Observations

- O-08 — Le hook décrit son audit comme « sur l'état indexé » ; en Bootstrap Mode le contrôle `BOOTSTRAP_CHANGE_SCOPE` porte sur tout le worktree (indexé ou non). Fail-closed, pas un défaut, mais la formulation de `project_control/README.md` et de `AGENTS.md` mérite une correction d'un mot lors d'une prochaine maintenance.

### Suite

1. Décision du Project Owner : promotion de `claude/v3.3-legacy-baseline` sur `main` (fast-forward, tag proposé `v3.3.0`), push `origin` et `nas` par lui.
2. P2 étape 1b (template) : `skeleton_version` et manifeste du core — exige la décision humaine sur l'ensemble core (5.2) ; `runtime_proof/` hors core.
3. P2 étape 2 (Alpha, sous Work Item) : ajout de `legacy_baseline` à son `project-state`, remplacement du core par celui du template, scission `AGENTS.md` core/projet ; `LEGACY_EVIDENCE_BASELINE` disparaît du contrôleur.
4. P3 (preuve de lecture des autorités), puis publication et plugin (P5) après un second projet réel.

---

## 11. V4 — étape 1b livrée, scope de l'étape 2 (2026-09-07)

Statut : `SCOPE_DEFINITION_V4 — STEP_1B_IMPLEMENTED_ON_BRANCH — STEP_2_SCOPED — NOT_PROMOTED`

### Décisions et livraison

- `v3.3.0` promu (`285b56c`, TPL-D-008) et poussé par le Project Owner sur GitHub et NAS.
- `TPL-D-007` — ensemble core retenu : `CLAUDE.md`, `FIRST_START.md`, `ADOPTION.md`, `scripts/` (contrôleur, traçabilité, hook), `tests/test_template.py` + `tests/fixtures/project_control/`, `project_control/schemas/` + `project_control/README.md`, `docs/governance/DEFINITION_OF_DONE.md`, `docs/agent-governance/AGENTS.core.md` — 19 fichiers. Hors core : `AGENTS.md`, `README.md`, documents de gouvernance du projet, records, métier, `runtime_proof/`, `provenance/`.
- Branche `claude/v3.4-template-upgrade`, commit `ecde6d2` depuis `main` (`285b56c`, `v3.3.0`). 84 tests OK sur le Mac (cinq nouveaux), audits PASS, `core-manifest` aligné. Non promue.

### Ce qui est implémenté (1b)

- `provenance/core-manifest.v1.json` : `skeleton_version` + SHA-256 des 19 fichiers core ; `core-manifest` (lecture) et `core-manifest --write --version` (réservé au template, `repository_role = PROJECT_TEMPLATE`). `FIRST_START.md` est hashé avec `INITIALIZATION_STATUS` normalisé : initialiser un projet ne « modifie » pas le core, et `template-upgrade` conserve le marqueur du projet à l'écriture. C'est l'unique exception, documentée.
- `AGENTS.md` scindé : `docs/agent-governance/AGENTS.core.md` (core, routé en base par `mandatory-documents.v1.json`) ; `AGENTS.md` racine appartient au projet, déclare `` `AGENTS_CORE: docs/agent-governance/AGENTS.core.md` `` et ne peut que renforcer. `CLAUDE.md` pointe les deux.
- `audit` : `CORE_MANIFEST` — manifeste présent et bien formé, chaque fichier core présent, core déclaré par `AGENTS.md`. Un fichier core **modifié localement n'est pas une erreur d'audit** (choix délibéré : ne pas paralyser un projet pendant qu'il travaille sur une divergence, ni le template pendant sa propre maintenance) ; il est signalé par `status` (`core_drift`), refusé par `template-upgrade` et détecté par le test `test_core_manifest_describes_the_tree_and_the_decided_core_set` dans la suite du template.
- `template-upgrade --source <arbre> [--apply] [--overwrite <chemin>]` : classification `IDENTICAL` / `UPDATED` / `ADDED` / `REMOVED_UPSTREAM` (signalé, jamais supprimé) / `MODIFIED_LOCALLY` (refusé sans `--overwrite` nominatif) ; source dont le core n'est pas intact refusée ; retour de version refusé ; `--apply` en `NORMAL_MODE` seulement, jamais sur le template lui-même ; écriture transactionnelle avec droits d'exécution, manifeste de la source adopté, vérification avant validation, rollback complet ; aucun record touché. S'exécute sous un Work Item dont les `authorized_paths` couvrent le core et le manifeste ; les fichiers ajoutés sont indexés explicitement.
- Points tranchés en cours de route : pas de `skeleton_version` dans `project-state` (il vivrait sur la canonique seule depuis P9-A et ne pourrait pas être écrit par un upgrade sur branche) — le manifeste est la seule source de version ; pas de `--accept-local` (confirmé).

### Critères de fermeture de V1 — état après 1b

1. Copie neuve, `template-upgrade --dry-run` vers la même version : zéro écart (`identical 19`). **Rempli** (test).
2. Copie intacte, upgrade vers une version supérieure : fichiers intacts mis à jour, ajoutés, retirés en amont signalés ; records intouchés ; `audit` PASS ensuite. **Rempli** (test) — la partie « migre ou refuse les records » est remplacée par la baseline d'adoption (V2).
3. Fichier core modifié localement : refusé, listé, rien d'écrit ; `--overwrite` explicite par fichier. **Rempli** (test).
4. La version ne change que si le core est intégralement aligné : le manifeste n'est adopté qu'après vérification post-écriture. **Rempli** (test).
5. Rapport sur Alpha : voir ci-dessous. **Rempli.**
6. Suite verte, bibliothèque standard seule. **Rempli.**

### Rapport `template-upgrade` sur Alpha (lecture seule, 2026-09-07)

Logique `template-upgrade` du template (`ecde6d2`, extraite par `git archive`, exécutée hors d'Alpha) appliquée à Alpha `8038b78`, avec un manifeste local synthétique déclarant le core actuel d'Alpha intact (Alpha n'a pas encore de manifeste) ; `git status` vierge avant et après, aucun script d'Alpha exécuté :

```
UPGRADE_PLAN — 3.1.0 -> 3.4.0: identical 5, updated 10, added 4, removed upstream 0, modified locally 0
  ADDED     ADOPTION.md, CLAUDE.md, docs/agent-governance/AGENTS.core.md, scripts/hooks/pre-commit
  UPDATED   FIRST_START.md, DEFINITION_OF_DONE.md, project_control/README.md,
            schemas agent-run / project-state / work-item, scripts/project_control.py,
            fixtures agent-run / work-item, tests/test_template.py
  IDENTICAL schemas conversation-reference / evidence / roadmap-state,
            scripts/check_git_traceability.py, fixture conversation
```

C'est le plan exact de l'étape 2. Hors core, donc hors de ce plan et à traiter dans le Work Item : `tests/test_evidence_migration.py` (référence la constante `LEGACY_EVIDENCE_BASELINE`, qui disparaît), `AGENTS.md` d'Alpha (ajout de la ligne `AGENTS_CORE:` ; ses règles projet restent), `project-state.v1.json` (ajout de `legacy_baseline`), `docs/governance/MIGRATION_RULES.md` (document projet, inchangé).

### Scope definition — étape 2 (Alpha, lecture seule pour Claude)

Nature : Work Item dans `alpha`, sous sa gouvernance (Human Decision, branche dédiée, preflight, `authorized_paths`), comme WI-060. Aucune écriture par Claude sans mandat explicite levant la lecture seule ; l'exécutant est au choix du Project Owner (Claude sous mandat, ou Codex).

Objectif : le core d'Alpha devient celui du template `v3.4.0` (ou de la version promue), vérifiable par `template-upgrade --dry-run` = zéro écart, sans migration de records.

Séquence proposée (une seule branche, un seul Work Item) :

1. Human Decision (`HD-066`) : autorité pour le Work Item ; baseline d'adoption fixée à `d4d7b5ad8108646139c155a8ca198e699eda7645` (déjà l'autorité de `HD-065`).
2. `project-state.v1.json` : `"legacy_baseline": {"head": "d4d7b5ad…", "human_decision_ref": "HD-065"}` — records sur la canonique (P9-A du template ne s'applique pas encore à Alpha ; suivre le flux Alpha en vigueur).
3. Écriture du manifeste initial d'Alpha : `provenance/core-manifest.v1.json` = manifeste `v3.4.0` du template copié (et non généré : `core-manifest --write` est réservé au template) après remplacement des 19 fichiers core par ceux du template (copie explicite, chemin par chemin, droits d'exécution du hook), `FIRST_START.md` en conservant `INITIALIZATION_STATUS: COMPLETE`.
4. `AGENTS.md` d'Alpha : ajout de `` `AGENTS_CORE: docs/agent-governance/AGENTS.core.md` `` en tête ; ses règles projet restent, à relire une fois contre le core (elles ne peuvent que renforcer).
5. `tests/test_evidence_migration.py` : supprimer (couvert par `test_legacy_baseline_*` du template) ou réécrire contre `legacy_baseline` ; `LEGACY_EVIDENCE_BASELINE` et `migration_errors` disparaissent avec l'ancien contrôleur.
6. `git config core.hooksPath scripts/hooks` sur le checkout.
7. Vérification : `python3 -B scripts/project_control.py audit` PASS (attendu d'après l'acceptation de l'étape 1 : 59 WI figés, 0 erreur), suite du template verte sur Alpha, `template-upgrade --source <template v3.4.0>` → `identical 19`, `status` : `Squelette : 3.4.0 | core aligné`, `evidence_validation` `LEGACY_PRESERVED` sur les 58 clôtures historiques.
8. Clôture du Work Item avec preuves structurées ; promotion `main` et push NAS par le Project Owner.

Risques identifiés : (a) règles projet d'`AGENTS.md` Alpha en conflit avec le core — à lister avant, décision humaine si besoin ; (b) `mandatory-documents.v1.json` d'Alpha (hors core) doit router `AGENTS.core.md` en base ; (c) le flux P9-A (records committés par les transitions) change la routine quotidienne d'Alpha — à annoncer dans la Human Decision.

### Suite

1. Décision du Project Owner : promotion de `claude/v3.4-template-upgrade` (fast-forward, tag proposé `v3.4.0`), push `origin` + `nas`.
2. Étape 2 sur Alpha : mandat explicite (levée de la lecture seule ou exécution par Codex) sur la base de la séquence ci-dessus.
3. P3 (preuve de lecture des autorités), puis publication et plugin (P5) après un second projet réel.

---

## 12. V5 — v3.4.0 promue, répétition générale de l'étape 2, correctif v3.4.1 (2026-09-07)

Statut : `SCOPE_DEFINITION_V5 — STEP_2_REHEARSED_GREEN — V3.4.1_ON_BRANCH — MANDATE_DRAFTED`

- `v3.4.0` promue (`b50228a`, TPL-D-009) et poussée sur GitHub et NAS. Décision « promouvoir » et question « dans l'ordre je dois soumettre à Codex en premier ? » → non : une mise à niveau part d'une version promue et taguée, jamais d'une branche.
- **Répétition générale de l'étape 2** sur un clone jetable d'Alpha (`git clone` local dans l'espace de session, Alpha lui-même intouché — `git status` vierge avant et après, HEAD `8038b78` ; aucun script d'Alpha exécuté, seuls les scripts du squelette après remplacement). Avec le core `v3.4.0` : `audit` PASS (15 contrôles, 59 WI figés), `status` exact (« Squelette : 3.4.0 | core aligné », 59 terminés dont 58 figés, 1 bloqué), `core-manifest` aligné, `template-upgrade --dry-run` = `identical 19` — mais la suite du template échouait **65 fois** : les fixtures `NOT_STARTED` copiaient tout l'arbre du projet, dont ses 242 fichiers métier sous `modules/`, et `NO_ACTIVE_BUSINESS_CAPABILITY` refusait chaque copie. Un test core ne doit dépendre d'aucun contenu du projet — défaut du template, pas d'Alpha.
- **Correctif `v3.4.1`**, branche `claude/v3.4.1-project-agnostic-suite` (`69c5424` + `84ac679`) : la fixture `NOT_STARTED` est un squelette vierge (`applications/`, `modules/`, `shared/`, `contracts/`, `data/`, `reports/` ramenés à leur `README.md` avant `git init`, `.DS_Store` ignoré) ; la source synthétique de `template-upgrade` dans les tests se déclare `PROJECT_TEMPLATE` (seul le squelette régénère un manifeste) ; test dédié ; manifeste régénéré (`3.4.1`, seul `tests/test_template.py` change). 85 tests OK sur le squelette. Répétition rejouée avec ce core : **85/85 sur le clone d'Alpha**, audit/status/core-manifest/template-upgrade inchangés. Non promue.
- **Mandat Codex rédigé** : `claude/mandat-codex-alpha-wi-061.md` — préalables, règles, séquence en onze points, cinq vérifications attendues (valeurs constatées en répétition), critère de fin, notes au Project Owner. Source du mandat : `v3.4.1`, donc à promouvoir avant de le soumettre.

### Suite

1. Décision : promotion de `claude/v3.4.1-project-agnostic-suite` (tag `v3.4.1`), push `origin` + `nas`.
2. Soumettre le mandat à Codex (ou le confier à Claude avec levée de la lecture seule sur Alpha pour `WI-061`).
3. Après `WI-061` : P3, puis P5 (publication, plugin) après un second projet réel.

---

## 13. V6 — dérive constatée : l'étape 2 visait l'original d'Alpha ; retour arrière (2026-09-07)

Statut : `SCOPE_DEFINITION_V6 — STEP_2_WRONG_TARGET — ROLLBACK_PROCEDURE_ISSUED — STEP_2_RESCOPED_TO_A_COPY`

### Analyse de la dérive

- Le Project Owner avait accordé, pour le squelette, un accès **en lecture seule** à `alpha` — contrainte respectée par Claude à chaque instant (inspections `git show`/`git archive`, clones jetables dans l'espace de session).
- Mais dès la révision V2 (§ 9), l'étape 2 a été définie comme « Alpha remplace son core par celui du template dans un Work Item », c'est-à-dire **dans le dépôt original**, par un autre exécutant (Codex) ou sous levée de la contrainte. La question « sur l'original ou sur une copie ? » n'a jamais été posée au Project Owner : le choix a été fait implicitement par Claude, et confirmé de proche en proche (« Étape 1 et après on passe à la deux ? », « dans l'ordre je dois soumettre à Codex en premier ? », promotion de `v3.4.1`, mandat « Tu interviens dans le dépôt `~/Projets/alpha` »). C'est une décision d'autorité qui appartenait au Project Owner ; l'erreur est celle de Claude.
- Règle posée par le Project Owner le 2026-09-07 : **le vrai Alpha ne sert jamais directement de terrain d'essai ; une copie dont l'original n'est pas impacté est acceptable.**

### État exact de l'original au moment du retour arrière (lecture seule, 2026-09-07)

- `main` = `8038b78` = `nas/main` ; arbre de `main` identique à celui du NAS ; aucun push, aucune fusion.
- Traces de WI-061 dans l'original : la branche `codex/wi-061-adoption-core-v3-4-1` (`fa7fa32`, `28900ad`, `8395edc` ; 45 fichiers par rapport à `main`) ; le checkout laissé sur cette branche ; la clé locale `core.hooksPath=scripts/hooks`. Rien d'autre : pas de stash, un seul worktree, aucun fichier non suivi hors caches `__pycache__` (ignorés par Git, régénérables).
- Hors WI-061 : des refs d'outil `refs/codex/turn-diffs/checkpoints/…` (points de contrôle internes de Codex, dont plusieurs datés des sessions du 6–7 septembre ; ils pointent l'arbre de `main`) — à ne pas supprimer sans décision humaine, elles ne font pas partie des changements de WI-061.

### Procédure de retour arrière (gestes du Project Owner ; Claude ne modifie pas Alpha)

```bash
cd ~/Projets/alpha
export GIT_OPTIONAL_LOCKS=0
# 0. (optionnel) conserver le travail de Codex hors du dépôt, sous forme de fichier
git bundle create ~/Desktop/alpha-wi-061.bundle main..codex/wi-061-adoption-core-v3-4-1
# 1. revenir sur main (l'arbre de travail redevient celui de 8038b78)
git switch main
# 2. retirer le réglage local du hook ajouté pour WI-061
git config --unset core.hooksPath
# 3. supprimer la branche (les trois commits deviennent inaccessibles ; le reflog les garde 90 jours, invisibles)
git branch -D codex/wi-061-adoption-core-v3-4-1
# 4. (optionnel) supprimer les caches Python ignorés par Git
find . -name __pycache__ -type d -prune -exec rm -rf {} +
# 5. vérifier : aucune sortie, puis PASS (ancien contrôleur, 13 contrôles)
git status --porcelain=v1 --ignored
python3 -B scripts/project_control.py audit
```

Attendu après 5 : `git branch --show-current` → `main`, `git rev-parse HEAD` → `8038b78…`, `git config --get core.hooksPath` → rien, `git branch --list 'codex/wi-061*'` → rien. Claude vérifie ensuite ces quatre points en lecture seule.

### Ce qui n'est pas affecté

- Le squelette (`Squelette V3 -runtime-proof`, `main` = `44905d1`, `v3.4.1`, GitHub et NAS à jour) : tout le travail P9, P2 étapes 1 et 1b reste valide et promu ; rien n'y dépend d'Alpha.
- Le NAS d'Alpha : inchangé (`8038b78`).
- Les rapports de fermeture globale A–I d'Alpha : jamais touchés.

### Étape 2, re-cadrée

L'étape 2 ne pourra viser qu'un **clone** d'Alpha (`git clone` local, remote retiré pour interdire tout push, dossier connecté à la session), sur décision explicite du Project Owner ; l'original n'est ni lu pour écrire, ni modifié. La procédure et les cinq vérifications du mandat retiré restent valables sur la copie. Sans cette décision, l'étape 2 attend un autre projet dérivé.

---

## 14. V7 — retour arrière vérifié ; question de la mise à niveau d'Alpha vers `v3.5.0` (2026-09-07, soir)

Statut : `SCOPE_DEFINITION_V7 — ROLLBACK_VERIFIED — STEP_2_AWAITING_TARGET_DECISION`

### Vérification du retour arrière (lecture seule, 2026-09-07)

Commandes read-only seulement (`GIT_OPTIONAL_LOCKS=0`), aucun script d'Alpha exécuté :

- `git branch --show-current` → `main` ; `HEAD` = `8038b78a720a38c374cc179f3406a3d6474bc44f` = `nas/main` ; `git status --porcelain=v1 --untracked-files=all` vide ; `core.hooksPath` non défini ; aucune branche `codex/wi-061*` ; aucun Work Item `IN_PROGRESS` ; dernière décision enregistrée `HD-065`. Les quatre points attendus par § 13 sont vérifiés.
- Inchangé, comme prévu : sept refs d'outil `refs/codex/turn-diffs/checkpoints/…` — à ne pas supprimer sans décision humaine, elles ne relèvent pas de WI-061.
- Core d'Alpha tel qu'avant WI-061 : absents `provenance/core-manifest.v1.json`, `CLAUDE.md`, `ADOPTION.md`, `docs/agent-governance/AGENTS.core.md`, `scripts/hooks/pre-commit` ; `LEGACY_EVIDENCE_BASELINE` toujours constante du contrôleur (`scripts/project_control.py`, ligne 29) ; `tests/test_evidence_migration.py` présent ; `project-state.v1.json` sans `legacy_baseline` ; `TEMPLATE_PROVENANCE.md` déclare toujours `bede17a`. Alpha n'a donc aucune version de squelette déclarée.

### Question du Project Owner : mettre à niveau Alpha vers le squelette enrichi

- Réponse : possible, c'est l'objet même de P2. Mais la première mise à niveau d'Alpha est l'**adoption initiale** (étape 2 : remplacement des 19 fichiers core, manifeste copié, `legacy_baseline`, scission `AGENTS.md`, quatre points hors core, introduction du registre), pas un `template-upgrade` de routine : sans manifeste, `template-upgrade` n'a rien à comparer. Après l'étape 2, chaque version suivante du squelette s'applique par `template-upgrade` sous Work Item.
- Source : une version promue et taguée uniquement — `v3.5.0` (`855558d`, TPL-D-012). Push `origin` + `nas` de `v3.5.0` à vérifier par le Project Owner avant toute exécution.
- La répétition générale du § 12 a été jouée avec `v3.4.1`. `v3.5.0` change le contrôleur (refus mécanique du double arrêt), `AGENTS.core.md`, `CLAUDE.md`, la suite (87 tests) et le manifeste : la répétition est à **rejouer avec `v3.5.0`** sur une copie avant toute exécution réelle. Plan attendu, à recalculer sur la copie : 4 ajouts, 10 mises à jour, 5 identiques (§ 11), plus les points hors core du mandat retiré et la réconciliation de l'introduction de `WORKTREE_REGISTRY.md` (amendement 1).
- Écart exact `v3.5.0` ↔ Alpha non recalculé ce soir : la demande d'accès en lecture au dossier `Squelette V3 -runtime-proof` a expiré sans réponse ; aucune valeur n'a été supposée à la place.

### Décision attendue — STOP 1 (règle TPL-D-011)

- Cible de la répétition : un **clone** d'Alpha dans un dossier à nommer par le Project Owner, hors de `~/Projets/alpha`, remote retiré (aucun push possible), connecté à la session. Action : `git clone` local puis étape 2 sur la copie, avec les cinq vérifications du mandat retiré. L'original n'est ni écrit ni modifié ; le lire pour le cloner n'est pas en sortir.
- La mise à niveau **réelle** d'Alpha, si elle est décidée après une répétition verte, reste un Work Item d'Alpha sous sa gouvernance (`HD-066`, `WI-061`, branche dédiée), exécuté par le Project Owner lui-même ou par un agent sous mandat explicite avec levée nommée de la lecture seule (deux confirmations nommant le dossier). Le mandat retiré et son amendement 1 servent de check-list, réédités pour `v3.5.0` ; la décision sur l'introduction du registre (« fast-forward strict » → alignement par merge) appartient au Project Owner.
- Alternative dans le périmètre : rapport seul, rien n'est lancé.

---

## 15. V8 — répétition de l'étape 2 sur une copie d'Alpha, core `v3.5.0` : PASS (2026-09-07)

Statut : `SCOPE_DEFINITION_V8 — STEP_2_REHEARSED_ON_COPY_PASS_V3_5_0 — REAL_UPGRADE_AWAITING_PROJECT_OWNER`

### Autorisation (double arrêt, TPL-D-011)

- `STOP 1` → « ok repetition sur une copie » ; `STOP 2` → « Confirmé : répétition dans ~/Projets/alpha-copie-repetition-20260907, original et squelette en lecture seule. » Les deux citations sont dans `HD-066` de la copie (`Folder scope`, `Confirmation 1`, `Confirmation 2`) ; le contrôleur v3.5.0 les a acceptées.
- Périmètre tenu : original lu une fois (clone) puis contrôlé en lecture seule avant et après (`main` = `8038b78` = `nas/main`, propre, hook absent, 62 branches, reflog sans entrée nouvelle) ; squelette lu seulement (`git archive v3.5.0`) ; aucun remote, aucun push. Une permission de suppression limitée à la copie a été nécessaire (Git ne pouvait pas retirer `.git/config.lock` dans la VM de session).

### Résultat

- Copie : 9 commits au-dessus de `8038b78` (HD-066 ; introduction du registre réconciliée ; `create-work-item` et `start WI-061` par l'ancien contrôleur ; adoption du core `4c3e8bb` acceptée par le hook v3.5.0 ; preuves `tests` et `integration` ; deux fast-forward de `main` ; `close WI-061` committé par le nouveau contrôleur, `cb068a8` ; rapport `c667cc4`). `main` final = `c667cc4`, branche `work/wi-061-adoption-core-v3-5-0` intégrée.
- Les cinq vérifications, sur la branche puis sur `main` : `audit` PASS (16 contrôles, 59 Work Items figés à `d4d7b5ad`, `CORE_MANIFEST 3.5.0`), `status` « Squelette : 3.5.0 | core aligné », 60 terminés dont 58 figés, `core-manifest` `CORE_ALIGNED`, `template-upgrade --source <archive v3.5.0>` `identical 19`, suite du template `87/87 OK` (56 s) deux fois.
- Plan constaté : 4 ajoutés, 10 mis à jour, 5 identiques, manifeste copié ; hors core : `project-state` (+`legacy_baseline`), `AGENTS.md` scindé (règles Alpha conservées : HD-006, HD-065/HD-066 ; ancien core supprimé, dont le paragraphe `resume` « fast-forward strict »), `mandatory-documents` (+`AGENTS.core.md`), `tests/test_evidence_migration.py` supprimé, introduction du registre (amendement 1).
- Voie de routine démontrée : le checkout du squelette est passé à `v3.6.0` (`8ea4aec`, TPL-D-014) pendant la répétition ; le dry-run depuis la copie donne `3.5.0 -> 3.6.0 : identical 12, updated 7, modified locally 0`, rien écrit. La source de la répétition était figée par l'archive du tag — d'où RL-R-01.
- Rapport complet : `reports/WI-061-REPETITION-ADOPTION-CORE-V3.5.0.md` dans la copie (committé sur `main`, sha256 `8acdae95…`), aussi livré dans la conversation.

### Redlines pour le mandat réel et observations

- RL-R-01 (MINOR) : source = `git archive <tag>` vers un dossier temporaire, jamais le checkout vivant du squelette (il a changé de version en cours de route).
- RL-R-02 (MINOR) : écrire toute sortie JSON (`status --json`) hors du dépôt puis la copier — la redirection tronque le fichier que l'audit interne de `status` relit (`status.json` de la copie porte `audit_status: FAIL` ; corrigé par `status-2.json`, original conservé, immuable).
- RL-R-03 (MINOR) : `docs/governance/MIGRATION_RULES.md` d'Alpha dit « déclarée dans le core » — une phrase à corriger, chemin à ajouter aux `authorized_paths`.
- O-10 (squelette) : `Folder scope` dans la décision du dépôt cible — le modèle le réserve aux actions hors dépôt, le contrôleur accepte le chemin du dépôt lui-même avec deux confirmations ; à clarifier d'une phrase dans `HUMAN_DECISIONS.md` du template.
- O-11 à O-16 : fichiers core ajoutés `UNEXPLAINED` jusqu'à indexation (documenté, à écrire dans la séquence) ; records de `start` committés sur la branche par l'ancien contrôleur (dernier cas, P9-A ensuite) ; `ADOPTION.md` non routé par Alpha (optionnel) ; scope historique de WI-060 cite le test supprimé (figé) ; identité Git de l'exécutant à fixer ; suppression à autoriser dans la VM de session.

### Décisions du Project Owner pour la mise à niveau réelle de `alpha`

Rien n'est décidé par ce rapport : version source (`v3.6.0` promue et taguée, push `origin`/`nas` à faire) ; réconciliation de l'introduction du registre et disparition du paragraphe `resume` de l'ancien `AGENTS.md` ; sémantique de `Folder scope` (O-10) ; redlines RL-R-01…03 dans le mandat réédité ; exécutant et identité Git ; moment (le dossier pré-freeze A–I est indépendant). Option ouverte sur la copie : jouer la première mise à niveau de routine `3.5.0 → 3.6.0` (`template-upgrade --apply` sous Work Item) — hors du périmètre confirmé, donc sur décision.

---

## 16. V9 — mise à niveau de routine `3.5.0 → 3.6.0` : mécanique prête, adoption bloquée par la rétroactivité de P3 (2026-09-07)

Statut : `SCOPE_DEFINITION_V9 — ROUTINE_UPGRADE_TO_3_6_0_BLOCKED_BY_P3_RETROACTIVITY — TEMPLATE_3_6_1_REQUIRED`

### Mandat et méthode

- « dans l ordre que tu préconises! » (Project Owner, 2026-09-07) sur la proposition de jouer la première mise à niveau de routine sur la copie. La lecture d'`AGENTS.core.md` 3.6.0 (« tout Agent Run postérieur [à `legacy_baseline`] sans `authorities_read` met l'audit en échec ») a fait prévoir un refus : démonstration conduite dans un **clone jetable de la copie** (espace de session, aucun remote, supprimé ensuite) ; la copie reste à `main` = `9d24dce` (rapports committés), propre, sans HD-067 ni WI-062 ; original `8038b78` intouché ; squelette lu seulement (`git archive v3.6.0`).
- Rapport : `reports/WI-062-DEMONSTRATION-MISE-A-NIVEAU-3.6.0.md` + journal `.journal.txt` dans la copie, aussi livrés dans la conversation.

### Ce qui marche

- Flux P9-A observé de bout en bout avec le contrôleur 3.5.0 : `create-work-item WI-062` et `start WI-062` committent eux-mêmes sur `main` ; la branche ne porte que le travail.
- `template-upgrade --source <archive v3.6.0>` : `UPGRADE_PLAN — 3.5.0 -> 3.6.0: identical 12, updated 7, modified locally 0` ; `--apply` : `7 core file(s) written, manifest now 3.6.0` ; `core-manifest` (3.6.0) `CORE_ALIGNED` ; `template-upgrade` ensuite `identical 19`. La voie de routine promise par P2 est mécaniquement prête.
- `context-manifest WI-062` (3.6.0) calcule le `MANIFEST_DIGEST` sur les 15 autorités réelles d'Alpha : P3 fonctionne dans un projet dérivé.

### Scénario d'échec démontré — RL-T-01 (squelette, MAJOR)

Après `--apply`, le contrôleur 3.6.0 rend `audit` FAIL : `Agent Run RUN-WI-060-001 / RUN-WI-061-001 / RUN-WI-062-001: authorities_read is required after the adoption baseline` ; le hook refuse le commit (`MODE_AUDIT`) ; `preflight` FAIL ; `acknowledge-authorities` (seule commande capable d'enregistrer une preuve) est refusée par le même audit et n'accepte de toute façon qu'un run `IN_PROGRESS` — les runs clos ne sont jamais réparables. Impasse. Cause : `legacy_agent_run_refs()` n'exempte que les runs présents dans l'arbre au commit `legacy_baseline`. **L'original Alpha est concerné à l'identique** (`RUN-WI-060-001` absent de l'arbre à `d4d7b5ad`, vérifié en lecture seule) : une adoption directe de la 3.6.0 par Alpha échouerait au même endroit. La 3.6.0 n'est adoptable que par une copie neuve ou un projet sans run postérieur à sa baseline.

Correction proposée (`REUSE > ADAPT`) : une **baseline de preuve de lecture** dans `project-state`, déclarée par la décision humaine de la mise à niveau (`{"head": <commit>, "human_decision_ref": "HD-NNN"}`, `null` pour un projet né en 3.6.x) ; les Agent Runs présents dans l'arbre à ce commit sont exempts de `authorities_read`, exactement comme `legacy_agent_run_refs` le fait pour `legacy_baseline` ; test sur clone historique (runs post-baseline sans preuve → `--apply` 3.5.0 → 3.6.x → audit PASS avec la baseline déclarée, FAIL sans). Version cible `3.6.1`. Observation O-18 : même corrigé, le run de la mise à niveau elle-même (démarré en 3.5.x sans digest) doit être couvert par cette baseline ou par `acknowledge-authorities` depuis la canonique avant `close`.

### Ordre préconisé, révisé

1. Squelette : maintenance `3.6.1` (RL-T-01 + O-10) — hors des dossiers accordés de cette session : STOP 1 posé au Project Owner (dossier `Squelette V3 -runtime-proof`, branche dédiée, aucune promotion) ; alternative : exécution par lui ou par Codex.
2. Copie : rejouer `3.5.0 → 3.6.1` (WI-062) avec la baseline déclarée.
3. Original : mandat réel réédité (source `3.6.1`, RL-R-01…03, décisions § 15) — rédigé seulement après décision explicite sur la cible (double arrêt).
4. Pushes `origin`/`nas` : geste du Project Owner ; v3.6.0 comme sauvegarde, pas comme version à adopter dans un projet avec historique.

---

## 17. V10 — correctif 3.6.1 promu, mise à niveau de routine `3.5.0 → 3.6.1` verte dans la copie (2026-09-07)

Statut : `SCOPE_DEFINITION_V10 — ROUTINE_UPGRADE_3_5_0_TO_3_6_1_ON_COPY_PASS — REAL_Alpha_AWAITING_PROJECT_OWNER`

- Squelette : correctif RL-T-01 livré sur `claude/v3.6.1-authorities-baseline` (double arrêt confirmé, puis feu vert sur le droit de suppression limité aux verrous Git) et **promu** (« promouvoir », TPL-D-015) : `main` = tag `v3.6.1` = `0d5d86f`, 93 tests, audits PASS ; `origin` et `nas` poussés par le Project Owner. Détails : `claude/p3-scope-preuve-lecture-autorites.md` § 8.
- Copie d'Alpha (« ok go ») : WI-062 joué pour de vrai dans la copie — HD-067, `create-work-item`/`start` par le contrôleur 3.5.0 (P9-A), `template-upgrade --apply` depuis l'archive du tag v3.6.1 (`identical 10, updated 9, modified locally 0`), refus nominatif `missing authorities_baseline` puis déclaration au commit de démarrage (`e90f0e6`, HD-067) → audit PASS (`AUTHORITIES_BASELINE — 62 Agent Run(s) exempt`), commit accepté par le hook 3.6.1, 93/93 tests, `Squelette : 3.6.1 | core aligné`, `identical 19`, ff `main`, `acknowledge-authorities WI-062` (15 autorités), `close` par le contrôleur 3.6.1 → `WI-062 DONE`, 61 terminés dont 58 figés. Copie : `main` = `f3735d6` (rapport `reports/WI-062-MISE-A-NIVEAU-ROUTINE-3.6.1.md` committé), propre. Original `8038b78` jamais écrit.
- Note : l'application a déposé dans l'original Alpha un dossier `Claude outputs/` (deux copies de fichiers livrés dans la conversation, 09:48 UTC) — non suivi, à retirer ou déplacer par le Project Owner ; l'audit d'Alpha le signalerait sinon.
- Ce que P2 a maintenant prouvé sur données réelles : adoption initiale (WI-061, 3.5.0) puis mise à niveau de routine (WI-062, 3.6.1) — la promesse de la scope definition est tenue. Le mandat réel pour `alpha` reste une décision du Project Owner (cible = original → double arrêt avant toute rédaction) : source 3.6.1 directe possible (`legacy_baseline` et `authorities_baseline` dans le même Work Item) ; redlines RL-R-01…03 à intégrer ; O-10 à trancher.

---

## 18. V11 — étape 2 exécutée dans le vrai `alpha` : WI-061, core v3.6.1 (2026-09-07)

Statut : `SCOPE_DEFINITION_V11 — STEP_2_DONE_ON_REAL_Alpha — NAS_PUSH_BY_PROJECT_OWNER_PENDING`

- Autorisation : double arrêt — « Tu le fais! » (choix de l'exécutant) puis « Confirmé : mise à niveau vers 3.6.1 dans ~/Projets/alpha, WI-061, pas de push. » ; droit de suppression accordé sur Alpha (verrous Git ; dossier `Claude outputs` déposé par l'application effacé à sa demande). Les deux confirmations sont dans `HD-066` (`Folder scope` = le dépôt).
- Exécution (auteur Jeoffrey + trailers Claude, convention du dépôt) : `HD-066` → introduction du registre réconciliée → `create-work-item` / `start WI-061` (ancien contrôleur ; commit de démarrage `15ad8f9` = `authorities_baseline`) → core v3.6.1 depuis l'archive du tag (4 ajoutés, 15 mis à jour/identiques, manifeste), `legacy_baseline` + `authorities_baseline`, `AGENTS.md` scindé (HD-006, HD-065/HD-066 conservées ; ancien core dont le paragraphe `resume` supprimé), `AGENTS.core.md` routé, `MIGRATION_RULES.md` corrigé (RL-R-03), test de migration retiré, hook — commit `5ec3f8a` accepté par le hook 3.6.1 → preuves → ff `main` → `acknowledge-authorities` (15 autorités) → preuve d'intégration révision 2 → `close WI-061` par le contrôleur 3.6.1 → rapport `reports/WI-061-ADOPTION-CORE-SQUELETTE-3.6.1.md`.
- Vérifications : audit PASS (17 contrôles : 59 WI figés, 61 Agent Runs exempts à `15ad8f9`, CORE_MANIFEST 3.6.1), `status` « Squelette : 3.6.1 | core aligné », 60 terminés dont 58 figés, `core-manifest` aligné, `template-upgrade` `identical 19`, 93/93 sur le core et sur `main` clos.
- État : `main` = `a31faa9` (11 commits au-dessus de `8038b78`), propre, hook actif ; `nas/main` = `8038b78` → `git push nas main` = geste du Project Owner (jusque-là le NAS est la sauvegarde de l'état antérieur). Squelette (`0d5d86f`) et copie (`f3735d6`) non modifiés.
- Incident : premier `acknowledge-authorities` refusé (« Author identity unknown » : pas d'identité Git dans l'environnement de session, aucune dans le dépôt), annulé proprement par le contrôleur ; identité fournie ensuite par variables d'environnement (`GIT_AUTHOR_*`/`GIT_COMMITTER_*`), sans toucher la configuration du dépôt. `integration.json` annonçait l'acquittement trop tôt → conservé (immuable), remplacé par `integration-2.json`. Leçon pour le mandat type (RL-R-04, MINOR) : fixer l'identité Git de l'exécutant avant toute commande du contrôleur qui committe.
- P2 est clos sur son objectif : adoption initiale prouvée sur copie puis exécutée sur l'original ; mises à niveau suivantes = routine (`template-upgrade` sous Work Item, `authorities_baseline` déjà en place). Reste : O-10 (`Folder scope` in-repo) et O-09 (docs hors core porteurs de doctrine) pour une maintenance ultérieure du template ; idée du Project Owner : style de retour (technique / simple) choisi à la configuration du projet — à cadrer (P11).
