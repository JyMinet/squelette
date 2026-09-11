> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# P3 — Preuve de lecture des autorités

Statut : `SCOPE_DEFINITION_V3 — PROMOTED (v3.6.1, TPL-D-015) — RL-T-01_CLOSED_BY_3_6_1 — PUSH_BY_PROJECT_OWNER_PENDING`
Révision : V3 (2026-09-07, § 8) ajoute le défaut démontré sur un projet dérivé réel et son correctif prototypé ; V2 (2026-09-07) remplace la V1 du 2026-09-05, conservée en fin de document. La V2 enregistre les décisions du Project Owner et l'implémentation livrée ; elle ne modifie pas rétroactivement la V1.

## 0. Décisions du Project Owner (2026-09-07)

Mandat : « alors p3 ? ou il faut un second projet ? » → P3 se conduit dans le template lui-même, sans second projet (le contrôleur, ses tests et sa doctrine suffisent ; un second projet réel reste nécessaire pour P5, pas pour P3).

Deux options tranchées (`TPL-D-013`, consignée dans `provenance/CHANGELOG.md`) :

1. **Mécanisme : empreinte présentée par l'agent.** `start` et `resume` exigent `--authorities-digest`, égal à l'empreinte courante des autorités du Work Item ; le contrôleur ne l'affiche jamais dans un refus. L'alternative « le contrôleur enregistre l'empreinte lui-même au `start` » prouvait seulement qu'un état existait, pas qu'un agent l'avait obtenu.
2. **Périmètre : autorités routées seulement.** Documents de base de `docs/agent-governance/mandatory-documents.v1.json` plus les scopes déduits des `authorized_paths` du Work Item. Les records tenus par Project Control sont exclus ; `HUMAN_DECISIONS.md` est inclus. L'alternative « tout `docs/` » aurait périmé la preuve à chaque écriture documentaire et brouillé la notion d'autorité.

## 1. Ce qui est livré

Branche `claude/v3.6-proof-of-reading` du dépôt `Squelette V3 -runtime-proof`, depuis `main` à `855558d` (`v3.5.0`) :

- `8594c86` — `feat(v3): preuve de lecture des autorités (P3, TPL-D-013)` ;
- `de151e5` — `fix(v3): libellé de context-manifest sans Work Item` ;
- `8ea4aec` — `docs(provenance): enregistrer la décision du Project Owner TPL-D-014`.

Manifeste du core `skeleton_version` `3.6.0`. Suite : 92 tests OK (sandbox 200 s, Mac 44–49 s). `audit`, `bootstrap-audit`, `check_git_traceability` PASS.

**Promotion (2026-09-07, « promouvoir », `TPL-D-014`)** : `main` avancé par fast-forward à `8ea4aec`, tag annoté `v3.6.0` ; tags `v3.0.0` → `v3.6.0` ; suite rejouée sur `main` (92/92). Push `origin` et `nas` par le Project Owner.

Fichiers : `scripts/project_control.py`, `project_control/schemas/agent-run.v1.schema.json`, `tests/test_template.py`, `tests/fixtures/project_control/agent-run.valid.json`, `docs/agent-governance/AGENTS.core.md`, `project_control/README.md`, `CLAUDE.md`, `provenance/CHANGELOG.md`, `provenance/core-manifest.v1.json`.

## 2. Contrat implémenté

### 2.1 `context-manifest [WI-NNN] [--scope S]... [--json]` (lecture seule)

```text
CONTEXT_MANIFEST: WI-012 | scopes: development
HEAD: <40>
AUTHORITY: AGENTS.md sha256=<64>
AUTHORITY: docs/agent-governance/AGENTS.core.md sha256=<64>
...
MANIFEST_DIGEST: <64>
```

- Scopes déduits des `authorized_paths` par préfixe (`PATH_SCOPES`) : `applications/`, `modules/`, `shared/`, `scripts/`, `tests/`, `project_control/` → `development` ; `contracts/` → `contracts` ; `data/` → `data` ; `docs/governance/`, `docs/adr/`, `docs/agent-governance/` → `governance` ; `docs/architecture/` → `architecture` ; `runtime_proof/`, `project_control/deployments/` → `runtime`.
- `--scope` ajoute un scope à la lecture (`security`, `recovery` n'ont pas de préfixe) sans changer l'empreinte exigée pour le Work Item, qui reste celle de `context-manifest WI-NNN` seul.
- Exclus de l'empreinte (`MANIFEST_EXCLUDED_PATHS`) : `ROADMAP.md`, `roadmap-state.v1.json`, `WORKTREE_REGISTRY.md`, `git-path-classifications.v1.json`, `project-state.v1.json` — routés pour la lecture, mais réécrits par chaque transition sans porter d'autorité nouvelle.
- `MANIFEST_DIGEST` = SHA-256 des lignes `chemin sha256\n` triées par chemin. Une autorité routée absente du dépôt est une erreur.
- Sans Work Item : `CONTEXT_MANIFEST: NO_WORK_ITEM | scopes: base only`.

### 2.2 Champ Agent Run

`agent-run.v1.schema.json`, champ optionnel `authorities_read` : `manifest_digest`, `generated_at`, `head`, `scopes`, `entries[{path, sha256}]` (`schema_version` inchangé, `1.0.0`). La V1 prévoyait une applicabilité `NOT_APPLICABLE` pour un Agent Run purement administratif : non retenue, tout Agent Run est créé par `start` ou `resume`, donc porte la preuve.

### 2.3 Points de contrôle

| Contrôle | Où | Règle |
|---|---|---|
| `--authorities-digest` | `start`, `resume`, `acknowledge-authorities` | absent → refus « requires --authorities-digest » ; différent de l'empreinte courante → refus « does not match » ; l'empreinte attendue n'est jamais imprimée ; records intacts |
| `AUTHORITY_MANIFEST_PRESENT` | `preflight` (Work Item démarré), `status` | le dernier Agent Run porte `authorities_read` non vide |
| `AUTHORITY_MANIFEST_COMPLETE` | idem | chaque autorité routée du Work Item figure dans la preuve |
| `AUTHORITY_MANIFEST_CURRENT` | idem | aucune autorité lue n'a changé, **sauf** celles comprises dans les `authorized_paths` du Work Item (voir 2.4) |
| `AUTHORITY_MANIFEST_AT_CLOSE` | `close` | les trois contrôles ci-dessus, sinon refus |
| `authorities_read` requis | `audit` | tout Agent Run absent de la baseline d'adoption doit porter une preuve cohérente (`manifest_digest` = hash des `entries`) |

`status --json` expose `authorities` : `CURRENT`, `STALE`, `MISSING` (ou `UNKNOWN` si le manifeste ne peut pas être calculé) ; texte : « Autorités lues : … ».

`acknowledge-authorities WI-NNN --authorities-digest <…>` : depuis la canonique, worktree propre, Work Item `IN_PROGRESS`, Agent Run en cours ; enregistre la nouvelle lecture sur ce run et committe (`chore(project-control): acknowledge authorities WI-NNN`). Depuis la branche du Work Item : committer le travail en cours, revenir sur la canonique, `acknowledge-authorities`, réaligner la branche (fast-forward ou merge, comme `resume`).

### 2.4 Règle ajoutée pendant l'implémentation : l'autorité autorisée en écriture

Constatée sur le test de `template-upgrade` : un Work Item de mise à jour du core réécrit `project_control/README.md` et `AGENTS.core.md`, qui sont des autorités de base ; sans exception, sa propre écriture périmait sa preuve et bloquait son preflight jusqu'à l'intégration. Même situation pour un Work Item qui amende le Charter. Règle retenue : une autorité comprise dans les `authorized_paths` du Work Item ne périme pas sa propre preuve (l'agent en est l'auteur sous autorisation humaine) ; toute autre autorité modifiée exige la relecture. Limite assumée : une modification de ce même fichier par un tiers, pendant le Work Item, n'est pas distinguée de l'écriture autorisée — bornée aux chemins que l'humain a déjà ouverts à l'écriture. Promue avec la version (`TPL-D-014`).

### 2.5 Compatibilité

Les Agent Runs présents au commit `legacy_baseline` (`legacy_agent_run_refs`) restent valides sans `authorities_read`. Tout Agent Run créé ensuite porte la preuve : un projet dérivé adopte P3 par `template-upgrade` sans migration de records — point 7.2 de la V1 (« tolérance pour les projets dérivés antérieurs : UNKNOWN ») tranché par le mécanisme de P2.

**Réfuté le 2026-09-07 sur un projet dérivé réel — voir § 8.** Cette compatibilité ne tient que pour un projet sans Agent Run entre sa `legacy_baseline` et l'arrivée de P3 ; tout autre projet est bloqué.

## 3. Scénarios de la V1 et tests

| Scénario V1 | Test |
|---|---|
| S-01 autorité non lue | `test_start_and_resume_require_the_current_authorities_digest` — `start` refusé sans empreinte ou avec `0×64`, aucune fuite (`[0-9a-f]{64}` absent du refus), records inchangés ; `start` avec l'empreinte enregistre `authorities_read` identique au manifeste |
| S-02 autorité périmée | `test_changed_authority_blocks_preflight_and_close_until_reacknowledged` — Charter amendé sur la canonique et intégré à la branche → preflight `FAIL: AUTHORITY_MANIFEST_CURRENT` nommant le Charter, `status` `STALE`, `close` refusé (`AUTHORITY_MANIFEST_AT_CLOSE`), empreinte stale refusée à l'acquittement, acquittement correct committé, `close` puis `audit` PASS |
| S-03 reprise aveugle | même test que S-01, seconde partie — `resume` refusé sans empreinte ; le nouvel Agent Run porte une empreinte différente (nouvelles décisions lues) |
| déterminisme et périmètre | `test_context_manifest_is_deterministic_and_follows_the_work_item_scopes` — deux appels identiques, base + `development`, exclusions vérifiées, `--json` cohérent avec `manifest_digest()`, `--scope runtime` ajoute `runtime_proof/README.md` |
| autorité autorisée en écriture | `test_an_authority_the_work_item_is_authorized_to_write_does_not_stale_its_own_proof` — Charter dans les `authorized_paths` modifié → preflight PASS ; DoD modifiée → `FAIL` nommant la DoD seule |
| baseline d'adoption | `test_agent_runs_before_the_adoption_baseline_are_exempt_from_the_proof_of_reading` — Agent Run sans preuve → audit FAIL ; déclaré à la baseline → PASS |

Les 23 appels `start` préexistants de la suite passent désormais par `start_command` (context-manifest → empreinte → `start --authorities-digest`), c'est-à-dire par le chemin exact d'un agent.

## 4. Critères de fermeture de la V1

1. S-01 à S-03 refusés par le contrôleur, un test chacun : **oui** (plus trois tests).
2. Tests existants verts : **oui**, 92/92 (28 à l'époque de la V1, 87 à `v3.5.0`).
3. `audit` et `bootstrap-audit` PASS sur une copie neuve : **oui** (branche puis `main`, Mac).
4. Aucune dépendance hors bibliothèque standard : **oui** (`hashlib`, `json`).
5. Projet dérivé antérieur auditable : **oui**, par la baseline d'adoption (2.5). — **Non tenu sur Alpha (§ 8) ; rétabli par le correctif 3.6.1.**

## 5. Points de la V1 tranchés ou restés ouverts

- Manifeste dans le record Work Item en plus de l'Agent Run : **non** — l'Agent Run est l'unité d'exécution, c'est lui qui lit ; `status` remonte l'état au niveau du Work Item.
- Tolérance projets antérieurs : **tranchée** (2.5).
- ADR `ACCEPTED` du scope hors routage explicite : **ouvert**, inchangé — un ADR n'est une autorité pour P3 que s'il est routé par `mandatory-documents.v1.json` ; un projet qui veut ses ADR dans la preuve les route (fichier projet, hors core). À revoir avec O-09 (docs hors core porteurs de doctrine).

## 6. Limites assumées

- L'empreinte prouve que l'agent a obtenu la version exacte des autorités au moment du démarrage ou de l'acquittement ; elle ne prouve ni la lecture effective ni la compréhension. Un agent peut présenter l'empreinte sans lire : la doctrine (`AGENTS.core.md`, skill) porte ce point, le contrôleur rend seulement l'oubli et la péremption détectables.
- Une consigne orale, hors dépôt, reste hors de portée — c'est le domaine du double arrêt (`TPL-D-011`).
- Toute décision humaine enregistrée après le démarrage, pour n'importe quel Work Item, périme la preuve des Work Items en cours à leur clôture (`HUMAN_DECISIONS.md` est une autorité) : un `acknowledge-authorities` avant `close`, après lecture des décisions ajoutées. Coût accepté, cohérent avec la hiérarchie d'autorité.

## 7. Suite

- Promotion `v3.6.0` : faite (`TPL-D-014`, `main` = `8ea4aec`) ; push par le Project Owner.
- Skill `squelette-projet` : ajouter la séquence `context-manifest` → lecture → `start --authorities-digest` et `acknowledge-authorities` à la section « Commandes » (proposition à faire après promotion).
- P4 (capability de revue adversariale) et P5 (publication) inchangés.

## 8. V3 — défaut démontré sur un projet dérivé réel et correctif 3.6.1 (2026-09-07)

### Scénario d'échec — RL-T-01 (MAJOR)

Démontré dans un clone jetable de la copie de répétition d'Alpha (`claude/p2-scope-template-upgrade.md` § 16, rapport `WI-062-DEMONSTRATION-MISE-A-NIVEAU-3.6.0.md` dans la copie) : projet à `legacy_baseline` = `d4d7b5ad`, Agent Runs `RUN-WI-060-001`, `RUN-WI-061-001` (clos, `SUCCEEDED`) et `RUN-WI-062-001` (en cours) enregistrés après cette baseline et avant P3, sans `authorities_read`. `template-upgrade --apply` vers 3.6.0 réussit (7 fichiers, `CORE_ALIGNED`), puis `audit` FAIL (`SCHEMA_VALIDATION` : « authorities_read is required after the adoption baseline » pour les trois runs), le hook refuse tout commit, `preflight` FAIL, et `acknowledge-authorities` — seule commande capable d'enregistrer une preuve — est refusée par ce même audit et n'accepte de toute façon qu'un run en cours : les runs clos ne sont jamais réparables. Impasse. Cause : `legacy_agent_run_refs()` n'exempte que les runs présents dans l'arbre à `legacy_baseline`. L'original Alpha est touché à l'identique (`RUN-WI-060-001` absent de l'arbre à `d4d7b5ad`). La 3.6.0 n'est adoptable que par une copie neuve.

### Correctif prototypé (hors du squelette, clone de travail en espace de session, `REUSE > ADAPT`)

- `project-state.v1.json` : `authorities_baseline`, obligatoire, `null` sans Agent Run antérieur à la preuve de lecture, sinon `{"head", "human_decision_ref"}` — modèle exact de `legacy_baseline` (commit existant et ancêtre de `HEAD`, décision humaine enregistrée, `HEAD` jamais substitué, refusé en `NOT_STARTED`). Schéma étendu.
- Contrôleur : `authorities_baseline()`, `agent_run_refs_at(head, label)`, `authorities_exempt_agent_run_refs()` = runs présents à `legacy_baseline` ∪ runs présents à `authorities_baseline` ; `agent_run_authority_errors` s'appuie dessus (message complété : « exempt only through authorities_baseline ») ; contrôle d'audit `AUTHORITIES_BASELINE` (déclaration valide, nombre de runs exempts, ou erreur nominative) ; `status --json` expose `authorities_baseline`.
- Docs : `AGENTS.core.md` (phrase d'exemption étendue), `project_control/README.md` (preuve de lecture, records, compatibilité : paragraphe et JSON), `FIRST_START.md` (`null` pour un projet neuf), `provenance/CHANGELOG.md` (entrée `claude/v3.6.1-authorities-baseline`), `project-state` du template (`null`), fixture `NOT_STARTED` des tests.
- Tests : `test_authorities_baseline_exempts_agent_runs_recorded_before_the_proof_of_reading` — run sans preuve après la baseline d'adoption → audit refusé, `acknowledge-authorities` impuissant ; baseline déclarée → `PASS: AUTHORITIES_BASELINE — N Agent Run(s) exempt…`, `status --json` ; le Work Item en cours ferme après `acknowledge-authorities` et pas avant (`AUTHORITY_MANIFEST_AT_CLOSE`) ; run postérieur toujours soumis ; déclarations invalides refusées sans traceback ni écriture ; `NOT_STARTED` refusé. Correction connexe : `test_context_manifest_is_deterministic_and_follows_the_work_item_scopes` attendait `runtime_proof/README.md` (routage du template) et échouait dans un projet dérivé — il suit désormais le routage de la copie testée (règle v3.4.1 : aucune dépendance au contenu du projet). Manifeste `3.6.1`. **93 tests OK** sur le prototype.
- Vérification sur données réelles (clone jetable de la copie d'Alpha, supprimé ensuite) : HD-067 ; `create-work-item`/`start WI-062` par le contrôleur 3.5.0 (P9-A) ; `template-upgrade --apply` depuis le prototype (`3.5.0 -> 3.6.1: identical 10, updated 9`) ; audit FAIL nominatif `missing authorities_baseline` tant que la déclaration manque ; `authorities_baseline` déclarée au commit de démarrage de WI-062 → `audit` PASS (`AUTHORITIES_BASELINE — 62 Agent Run(s) exempt…`, `CORE_MANIFEST 3.6.1`), commit accepté par le hook 3.6.1, **93/93 tests dans le clone d'Alpha**, `status` « Squelette : 3.6.1 | core aligné », `identical 19` ; `close` refusé tant que le run de la mise à niveau n'a pas lu (`AUTHORITY_MANIFEST_AT_CLOSE`), `acknowledge-authorities WI-062` (15 autorités) puis `close` → `WI-062 DONE`, audit PASS, 61 terminés dont 58 figés.
- Diff cumulé : 9 fichiers, +288/−21 (`$HOME/work/v3.6.1-authorities-baseline.diff`, sha256 `4bfe5d3ff60aacc0…`, deux commits dans le prototype).

### Ce qui reste au Project Owner

- **Livré** (2026-09-07, après STOP 2 « Confirmé : branche claude/v3.6.1-authorities-baseline dans ~/Projets/Squelette V3 -runtime-proof, main intouché, pas de push. » puis feu vert sur le droit de suppression limité aux verrous Git) : branche `claude/v3.6.1-authorities-baseline`, commit `14cf42d` au-dessus de `main` = `8ea4aec` (auteur Jeoffrey, trailers Claude, mandat dans `PROJECT_CONTROL_HOOK_OVERRIDE`), 93 tests OK dans le squelette, `bootstrap-audit` et `audit` PASS, checkout remis sur `main`, aucun tag, aucun push. **Promue** (« promouvoir », 2026-09-07, `TPL-D-015`) : `main` avancé par fast-forward à `0d5d86f`, tag annoté `v3.6.1`, 93/93 sur `main`, `bootstrap-audit` et `audit` PASS ; push `origin` et `nas` par le Project Owner (les remotes sont encore à `855558d` = v3.5.0 : v3.6.0 et v3.6.1 partiront ensemble).
- Incident de séance : le droit de suppression demandé pour les verrous Git a d'abord été lu comme une suppression du dossier V3 — refus, puis feu vert après explication simple. Leçon : dire en une phrase ce qui sera effacé exactement ; un fichier de test de 2 octets laissé par la vérification à blanc a été retiré.
- Décision O-10 (sémantique de `Folder scope` dans le dépôt cible), hors de ce correctif : variante A « `NOT_APPLICABLE` pour un travail interne au dépôt, confirmations citées dans `Context` », variante B « chemin + deux confirmations même dans le dépôt cible, trace vérifiée par son contrôleur ».
- Push `origin`/`nas` : v3.6.0 comme sauvegarde, v3.6.1 comme version adoptable.

---

# Annexe — P3 Scope Definition V1 (2026-09-05), conservée telle quelle

Statut : `SCOPE_DEFINITION_V1 — NOT_AUTHORIZED`
Nature : définition de périmètre. Aucun code n'est produit, aucun Work Item n'est créé. Toute implémentation exige un Work Item autorisé.

## 1. Problème

`docs/agent-governance/mandatory-documents.v1.json` route dix documents de base plus les autorités du scope concerné, et `AGENTS.md` en impose la lecture avant toute écriture. Cette obligation est **déclarative** : aucun contrôle ne vérifie qu'elle a été honorée, ni sur quel état des fichiers.

## 2. Scénarios d'échec démontrés

Trois scénarios justifient le travail. Sans eux, il n'y aurait pas lieu d'agir.

**S-01 — Autorité non lue, non détectable.** Un agent exécute `preflight WI-012 --path <p>`, obtient PASS et écrit, sans avoir ouvert le Charter ni la roadmap. Aucun contrôle existant ne l'établit, ni pendant, ni après. L'Agent Run enregistre le scope demandé, pas les autorités consultées.

**S-02 — Autorité périmée.** Un agent lit le Charter au début d'une session longue. Une décision humaine modifie le Charter en cours de session. L'agent poursuit sur l'ancienne version : ses écritures sont cohérentes avec une autorité qui n'existe plus, et l'audit final passe puisqu'il ne compare que l'état courant à lui-même.

**S-03 — Reprise de session aveugle.** Une nouvelle conversation reprend un Work Item `IN_PROGRESS`. Rien dans le record ne permet de savoir quelles autorités la session précédente avait lues, ni dans quel état. La reprise repart d'une base non établie tout en héritant d'un statut `IN_PROGRESS`.

## 3. Objectif

Transformer l'obligation de lecture en gate machine, sans introduire de dépendance externe ni de nouveau service.

## 4. Non-objectifs

- Ne pas archiver le contenu des autorités lues.
- Ne pas vérifier la compréhension : seule la lecture d'un état identifié est prouvée.
- Ne pas imposer un provider d'agent ni un format de transcript.
- Ne pas étendre la portée aux fichiers hors `mandatory-documents.v1.json`.

## 5. Contrat proposé

### 5.1 Commande `context-manifest`

Read-only. Entrée : le scope concerné (ou le Work Item, qui le porte déjà). Sortie déterministe et triée :

```text
CONTEXT_MANIFEST: <scope>
GENERATED_AT: <ISO-8601>
HEAD: <40 caractères | UNBORN>
AUTHORITY: AGENTS.md sha256=<64>
AUTHORITY: docs/governance/PROJECT_CHARTER.md sha256=<64>
...
MANIFEST_DIGEST: sha256=<64>
```

`MANIFEST_DIGEST` est le hash de la liste ordonnée `chemin+sha256`. Il donne un identifiant unique de l'état d'autorité.

### 5.2 Champ Agent Run

Ajout à `agent-run.v1.schema.json` :

```json
"authorities_read": {
  "manifest_digest": "<sha256>",
  "generated_at": "<ISO-8601>",
  "entries": [{ "path": "<chemin>", "sha256": "<64>" }]
}
```

Applicabilité : `APPLICABLE` par défaut, `NOT_APPLICABLE` seulement pour un Agent Run purement administratif généré par le contrôleur lui-même.

### 5.3 Points de contrôle ajoutés

| Contrôle | Commande | Règle |
|---|---|---|
| `AUTHORITY_MANIFEST_PRESENT` | `preflight`, `start` | `authorities_read` présent et non vide si applicable |
| `AUTHORITY_MANIFEST_CURRENT` | `preflight`, `start` | chaque `sha256` déclaré égale le hash courant du fichier |
| `AUTHORITY_MANIFEST_COMPLETE` | `preflight`, `start` | aucune autorité routée pour le scope n'est absente du manifeste |
| `AUTHORITY_MANIFEST_AT_CLOSE` | `close` | manifeste revalidé ; une autorité modifiée depuis exige une re-lecture explicite |

Comportement fail-closed : tout écart refuse l'opération et restaure l'état administratif, conformément à la sémantique actuelle de `start`.

## 6. Impacts

- `DIRECT` : `scripts/project_control.py`, `project_control/schemas/agent-run.v1.schema.json`, `tests/test_template.py`, `docs/agent-governance/mandatory-documents.v1.json` (version de schéma), `AGENTS.md` (procédure de preflight).
- `INDIRECT` : tout projet déjà dérivé du squelette — les Agent Runs existants n'ont pas le champ. Une migration ou une tolérance explicite par `schema_version` est requise.
- `AUTHORITY` : `AGENTS.md` change de nature sur ce point, d'obligation morale à contrôle exécutable. Décision humaine requise.
- `CONCURRENT` : recouvre P2 (`skeleton_version`), qui touche aussi les schémas. Ordonnancement à trancher.

## 7. Points non tranchés

- Faut-il inclure le manifeste dans le record Work Item en plus de l'Agent Run : `UNKNOWN`.
- Tolérance pour les projets dérivés antérieurs : `UNKNOWN`.
- Le manifeste doit-il couvrir les ADR `ACCEPTED` du scope, aujourd'hui hors routage explicite : `UNKNOWN`.

## 8. Critères de fermeture proposés

1. Les trois scénarios S-01 à S-03 sont refusés par le contrôleur, avec un test dédié chacun.
2. Les 28 tests existants restent verts.
3. `audit` et `bootstrap-audit` restent PASS sur une copie neuve.
4. Aucune dépendance hors bibliothèque standard n'est ajoutée.
5. Un projet dérivé antérieur reste auditable, ou son incompatibilité est explicite et documentée.
