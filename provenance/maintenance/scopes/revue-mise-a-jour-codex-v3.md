> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Contre-revue indépendante — mise à jour Codex du squelette V3

Date : 2026-09-06 · Reviewer : Claude (session Cowork) · Posture : `READ_ONLY` / `REPORT_ONLY`
Objet : les deux commits déposés par Codex (GPT) sur le dépôt `Squelette V3 -runtime-proof`, branches `codex/v3-fiabilite-simplicite` et `codex/v3-retour-v8`.
Question posée : « GPT a mis une mise à jour, te convient-elle ? »

Précision préalable : `codex/v3-fiabilite-simplicite` n'est pas un dossier mais une **branche Git**. Il y en a deux, empilées : `codex/v3-retour-v8` (commit `811b63b`, **actuellement checkout**) est construite par-dessus `codex/v3-fiabilite-simplicite` (commit `c98a94a`). Promouvoir la seconde emporte la première ; la première peut être promue seule.

---

## A. Preflight — état exact de l'objet revu

| Élément | Valeur constatée |
|---|---|
| Dépôt | `~/Projets/Squelette V3 -runtime-proof` |
| HEAD | `811b63bbf72f52329848fdcfec8e1ea73855afd8` sur `codex/v3-retour-v8` |
| Refs | `main` = `35da2a2d82520cd735f5c1884fdc5f185254e8f6` (baseline que j'ai établie le 2026-09-05) ; `codex/v3-fiabilite-simplicite` = `c98a94a5009b9ffe2591fcaf89288998f96a982b` ; `codex/v3-retour-v8` = `811b63b…` |
| Chaîne | `35da2a2` → `c98a94a` (2026-09-06 00:11 +0200) → `811b63b` (2026-09-06 00:35 +0200) |
| Working tree | propre (`git status --porcelain=v2` vide), aucun stash, aucun remote |
| Auteur des commits | `Jeoffrey <<adresse retirée>>`, messages d'une ligne, sans trailer d'agent ni référence de session |

SHA-256 des fichiers pivots à HEAD (identiques sur la machine et dans la copie de travail du reviewer) :

```text
85fd3a458825bf373a2ba332e03e1aa915d1307a97c90093155a768cf48523e0  scripts/project_control.py   (2 990 lignes, blob 278cc79)
1faad87b68464bf29760b75dcf7f67bcd9b75dfa6530bfe6587c4bb86925a3c5  tests/test_template.py       (2 728 lignes, blob e424a40)
52423cacc127ccb60bb8ffd638172033d9b4251b6be08f587f4f0e685f09afd0  project_control/schemas/work-item.v1.schema.json
b3a755c106cea6790c61adfa98b36de86d48d4200d5d8f58f03e05f12e851cc2  project_control/schemas/evidence.v1.schema.json
242de70fa8c9cf8c90151532c878bc9a18979ee0a2638c209523970ea2fd9d22  AGENTS.md
```

Méthode : lecture des diffs sur la machine (`GIT_OPTIONAL_LOCKS=0`), contrôles read-only exécutés sur place, puis copie des 78 fichiers suivis dans un bac à sable isolé pour rejouer la suite de tests et des scénarios adversariaux. **Aucune écriture dans le dépôt** ; état Git vérifié identique avant et après (§ J).

## B. Inventaire de la mise à jour

| Commit | Fichiers | Lignes | Contenu annoncé |
|---|---|---|---|
| `c98a94a` « fiabiliser le cycle et simplifier la reprise du projet » | 18 (1 ajouté : `evidence.v1.schema.json` ; 1 rapport : `reports/V3_MAINTENANCE_2026-09-06.md`) | +1 425 / −238 | `status`, `start_head`, preuves JSON vérifiées par SHA-256, niveaux runtime, validation stricte des schémas, README raccourci |
| `811b63b` « reprendre les chantiers bloqués avec leur provenance » | 7 (1 rapport : `reports/V3_RETOUR_EXPERIENCE_20260906.md`) | +2 773 / −37 | `block` / `resume`, `block_records`, audit métier selon le mode, immutabilité des preuves, branche canonique déclarée |

Mandats invoqués par Codex (cités dans ses rapports) : « donc regarde pour ameliorer notre version V3 ! » puis « ok go ! Et mettre a jour V3 en fonctions des connaissance ce V8 !? ». Les deux rapports déclarent explicitement : FIRST_START reste `NOT_STARTED`, aucune promotion de `main`, mécanismes « adaptés depuis le contrôleur générique du projet consommateur » (`d4d7b5ad…`, non vérifiable d'ici), aucune règle de domaine reprise — confirmé par grep : aucune occurrence de `crypto`, `tactique`, `bitcoin`, `treasur` hors le test `test_m` qui l'interdit.

Tests : 28 (`main`) → 45 (`c98a94a`) → 69 (`811b63b`), aucun test supprimé (comparaison des noms).

## C. Ce que change la mise à jour, par thème

1. **Preuves de clôture** — `close` n'accepte plus un texte libre (`--test-evidence "unit-test report"` passait à `main`). Il exige un rapport JSON sous `reports/evidence/<WI>/`, conforme à `evidence.v1.schema.json`, suivi dans Git et identique à HEAD, avec artefacts hashés SHA-256, `subject_commit` compris entre `start_head` et la baseline de clôture, refus si un chemin métier a changé depuis `subject_commit`, immutabilité après premier commit (`git log --full-history --simplify-merges`), rapports `FAIL` historiques conservés, `close_head` figé. C'est la correction la plus importante de la livraison, et elle ferme un trou que ma revue du 05/09 n'avait pas relevé.
2. **Provenance de démarrage** — `start` exige d'être sur la branche canonique déclarée à son tip, capture `start_head`, exige `base_head` ancêtre, refuse une branche WI préexistante à un autre tip, restaure branche et records en cas d'échec. Branche canonique lue dans `REPOSITORY_STATUS.md` (`` `CANONICAL BRANCH: x` `` exactement une fois) ; `main` n'est plus codé en dur.
3. **Niveaux runtime** — `runtime_target` (`NOT_APPLICABLE` | `CONTROLLED_NON_PRODUCTION_RUNTIME` | `PRODUCTION`) ; DoD étendue à 9 niveaux (`DEPLOYED_IN_CONTROLLED_ENVIRONMENT`, `RUNTIME_PROVEN` ajoutés) ; `RUNTIME_PROVEN` ≠ `PRODUCTION_VERIFIED` contrôlé par le moteur.
4. **Validation de schémas** — `schema_record_errors` exécute le sous-ensemble JSON Schema utilisé par le core ; tout record mal formé échoue proprement (plus de traceback), `start_head` et `runtime_target` deviennent obligatoires.
5. **`status` / `status --json`** — vue calculée, read-only, avec prochaine action et gates manquantes.
6. **Audit en `NORMAL_MODE`** — `NO_ACTIVE_BUSINESS_CAPABILITY` remplacé par `BUSINESS_CHANGE_AUTHORIZATION` : à `main`, tout projet initialisé contenant un fichier autre que `README.md` sous `applications/`, `modules/` ou `shared/` échouait `audit` quel que soit le mode (`35da2a2:scripts/project_control.py:724-725`, contrôle inconditionnel ; idem `:983-984` dans `closeout_readiness`) ; c'est un blocage réel du squelette que Codex a levé.
7. **`block` / `resume`** — dépendance externe enregistrée par décision humaine structurée (`Project Control action: BLOCK|RESUME`, `Block reason code`, `Resume condition recorded|confirmed`), Agent Run clos `BLOCKED`, `BLOCKED` non actif, reprise avec nouvel Agent Run et alignement fast-forward uniquement.
8. **Doctrine** — nouvelle section AGENTS.md « Reprise et charge administrative » (« une autorisation humaine déjà donnée couvre les étapes ordinaires dans son périmètre ») ; ADOPTION.md réécrit sans registre ON/OFF ni règle `OMIT > ACTIVATE WITHOUT NEED` ; README réduit de 91 à 49 lignes (`wc -l` ; Codex annonce 99 → 57) ; correction « sept → six champs » de l'orchestrateur dans la carte d'architecture (exact : `job_id`, `dependencies`, `order`, `timeout`, `status`, `result`).

## D. Rejeu des contrôles et scénarios

Sur la machine (dépôt réel, HEAD `811b63b`) : `audit` **PASS** (13 contrôles), `bootstrap-audit` **PASS** (17), `status` **PASS** (`UNKNOWN | BOOTSTRAP_MODE`, prochaine action = initialiser), `check_git_traceability` **PASS**, `git diff --check 35da2a2 811b63b` **propre**, aucun `__pycache__` ni fichier résiduel après exécution.

Dans le bac à sable (copie bit-à-bit, Python 3.11, git 2.43) : `python3 -B -m unittest discover -s tests -v` → **69 tests, OK, 71,4 s** (Codex annonçait 69 PASS en 175 s sur Mac).

Scénarios adversariaux ajoutés par le reviewer (hors suite Codex) :

| # | Scénario | Résultat |
|---|---|---|
| E1 | WI sans `reports/evidence/<WI>` dans `authorized_paths` ; brouillon de preuve non commité puis `preflight` | `FAIL: AUTHORIZED_PATHS — path outside Work Item authorization: reports/evidence/WI-001/note.txt` ; le `close` passe ensuite si les preuves sont commitées avant tout preflight (→ F-05) |
| E2 | `--deployment APPLICABLE --runtime-proof NOT_APPLICABLE --runtime-target PRODUCTION` | refusé : `runtime_target=PRODUCTION requires runtime_proof=APPLICABLE` ; idem cible `NOT_APPLICABLE` + déploiement applicable (→ F-02) |
| E3 | déclaration canonique sans backticks dans `REPOSITORY_STATUS.md` | `audit` s'arrête globalement : `FAIL: INVALID_RECORDS — canonical branch declaration must appear exactly once; found 0` (fail-closed, libellé trompeur → O-03) |
| E4 | WI-001 avec un commit propre non intégré, `block`, WI-002 démarré et intégré dans `main`, puis `resume` WI-001 | **refusé** : `declared Work Item branch diverges from canonical head; resume refuses rebase or cherry-pick`. Remède manuel (merge de `main` dans la branche WI) : **conflit sur `docs/governance/roadmap-state.v1.json`** (→ F-01) |
| E4c | même séquence, WI-001 bloqué **sans** commit propre | `resume` **PASS** (fast-forward) — la limite exacte est donc « aucun commit non intégré sur la branche bloquée » |
| E6 | record Work Item d'une V3 antérieure (sans `start_head` / `runtime_target`) dans un projet initialisé | `audit` FAIL explicite `missing start_head; missing runtime_target` ; `status` → `INVALID`, exit 1 (incompatibilité documentée, fail-closed → O-06) |
| E7 | latence d'`audit` avec N Work Items `DONE` portant 2 rapports vérifiés | 0,13 s (0) · 0,21 s (1) · 0,42 s (4) · 0,80 s (8) · 1,14 s (12) : **linéaire, ≈ 80 ms par WI** dans le conteneur ; `close` ≈ 2,3 × audit (→ O-07) |

## E. Findings

Standard appliqué : sans scénario d'échec démontré, pas de redline.

### F-01 — `resume` refuse la reprise dans son cas d'usage ordinaire — sévérité **MAJEURE** (objet : `811b63b`)

- **Scénario reproductible** (E4) : un Work Item démarre, commite du travail partiel sur sa branche, est bloqué (`block`) ; comme promis (« `BLOCKED` est non actif : un autre Work Item peut démarrer », `AGENTS.md:103-104`), un second Work Item est démarré, intégré et clos ; `resume` du premier est refusé (`scripts/project_control.py:2306`). Le seul alignement admis est le fast-forward (`:2321`, `:2401`), possible uniquement si la branche bloquée n'a **aucun** commit non intégré (E4c). Le remède manuel — merge de la branche canonique dans la branche WI — produit un conflit sur les records administratifs (`roadmap-state.v1.json`), car ces fichiers sont modifiés sur les deux branches par les cycles de vie respectifs.
- **Cause** : l'état administratif (records, roadmap, registre) vit dans l'arbre, donc de façon **locale à chaque branche** jusqu'à intégration ; l'entrelacement de deux Work Items — précisément ce que `BLOCKED` non actif autorise — fait diverger ces fichiers. Le test `test_block_resume_08` ne couvre que le cas où la branche a été fast-forwardée dans `main` **avant** le blocage (`tests/test_template.py:1225-1245`), c'est-à-dire du travail partiel déjà intégré dans la branche canonique.
- **Impact** : la promesse fonctionnelle de la branche (« reprendre les chantiers bloqués avec leur provenance ») ne tient que dans une fenêtre étroite (blocage avant tout commit, ou après intégration complète). Aucune corruption : refus atomique, rollback vérifié, `status` reste juste. Le problème est le dead-end, pas la sécurité.
- **Correction proposée** (décision humaine D4) : soit (a) documenter la limite exacte et interdire `block` d'un Work Item portant des commits non intégrés sans intégration préalable ; soit (b) fournir une procédure d'alignement explicite (merge de la canonique dans la branche WI, résolution des fichiers administratifs par la version canonique, puis `resume`) et la tester ; soit (c) sortir les records administratifs de la branche WI (ils ne vivraient que sur la canonique), ce qui règle aussi la cause racine mais dépasse ce lot.
- **Statut** : `OPEN`.

### F-02 — Contradiction entre la DoD (« déclare séparément ») et le couplage imposé par le contrôleur — sévérité **MINEURE** (objet : `c98a94a`)

- **Scénario** (E2) : un Work Item « campagne de preuve runtime sur un déploiement existant » déclare `deployment=NOT_APPLICABLE`, `runtime_proof=APPLICABLE`, `runtime_target=PRODUCTION` → refusé (`scripts/project_control.py:682-683`) ; symétriquement un déploiement sans preuve runtime est impossible. L'owner doit soit déclarer une gate de déploiement fictive — et produire un rapport de déploiement pour un déploiement qui n'a pas eu lieu dans ce Work Item, ce qui contredit la doctrine « une preuve manquante ne peut pas être transformée en réussite » — soit dégrader la cible.
- **Preuve documentaire** : `docs/governance/DEFINITION_OF_DONE.md:19` « Chaque Work Item déclare **séparément** `code`, `tests`, `integration`, `deployment` et `runtime_proof` » et `project_control/README.md:75` ; aucun des deux ne mentionne le couplage.
- **Correction proposée** (D2) : trancher la règle. Si le couplage est voulu (tout déploiement se prouve ; toute preuve suppose un déploiement du même Work Item), l'écrire dans la DoD et le README ; sinon relâcher le code : cible `NOT_APPLICABLE` ⇒ les deux gates `NOT_APPLICABLE`, cible runtime ⇒ **au moins une** des deux gates applicable.
- **Statut** : `OPEN`.

### F-03 — Perte de la règle `OMIT > ACTIVATE WITHOUT NEED` et affaiblissement de la gate d'activation — sévérité **MINEURE** (objet : `c98a94a`)

- **Scénario** : la skill `squelette-projet` validée le 05/09 et les mandats Alpha citent `OMIT > ACTIVATE WITHOUT NEED` comme règle commune non négociable. Un agent chargé de l'appliquer cherche la règle dans les autorités du dépôt : elle n'existe plus (présente à `35da2a2:ADOPTION.md:7`, absente de tout l'arbre à `811b63b`) → autorité ambiguë → `STOP`. Par ailleurs `ADOPTION.md:8-9` dit désormais « décision existante ou nouvelle **si nécessaire** » là où `AGENTS.md:166` exige « une décision humaine documentée … pour … activation » ; or `AGENTS.md:3` interdit à une instruction locale d'affaiblir la règle.
- **Correction proposée** : rétablir la ligne `REUSE > ADAPT > REIMPLEMENT` **et** `OMIT > ACTIVATE WITHOUT NEED` dans ADOPTION.md, et aligner la phrase d'activation sur AGENTS.md (« décision humaine documentée »). La suppression du registre ON/OFF peut être conservée : la justification de Codex (pas de second registre parallèle à `runtime_target`) est cohérente.
- **Statut** : `OPEN`.

### F-04 — Historique de maintenance du template déposé dans des documents de projet — sévérité **MINEURE** (objets : `c98a94a`, `811b63b`)

- **Scénario** : FIRST_START prescrit d'« exporter l'arbre suivi » pour créer un projet ; le nouveau projet hérite alors de `docs/governance/WORKTREE_REGISTRY.md:31-78` (deux sections « Maintenance du template » avec `/private/tmp/squelette-v3-improvement-20260906` et `~/Projets/Squelette V3 -runtime-proof`, `:39-40`, `:62`) et de deux rapports `reports/V3_*.md` qui ne le concernent pas — alors que le registre affirme en `:5` « Aucun worktree de projet n'est préchargé » et README `:40` « Aucun projet, domaine, Work Item ou décision humaine n'est préchargé ». `provenance/TEMPLATE_PROVENANCE.md`, seul document conçu pour l'histoire du template, n'est pas touché.
- **Impact** : fuite de chemins locaux et d'histoire du template dans chaque projet dérivé ; le moteur n'est pas affecté (le registre ne parse que les blocs `PROJECT_CONTROL:WI-NNN`).
- **Correction proposée** (D5) : déplacer ces deux sections et les deux rapports vers `provenance/` (par exemple `provenance/CHANGELOG.md` — c'était l'action P2 de ma revue) et laisser le registre et `reports/` vierges. C'est aussi l'illustration concrète de l'angle mort P1 §4 : sans mode `TEMPLATE_MAINTENANCE`, chaque maintenance du core improvise où elle se documente.
- **Statut** : `OPEN`.

### F-05 — Autorisation du dossier de preuves non documentée — sévérité **MINEURE** (objet : `c98a94a`)

- **Scénario** (E1) : `project_control/README.md:81,107` prescrit de préparer les preuves sous `reports/evidence/<WI>/` puis de les enregistrer dans Git, sans dire que ce dossier doit figurer dans `authorized_paths`. Un agent qui écrit ses preuves puis relance `preflight` avant de commiter obtient `FAIL: AUTHORIZED_PATHS` (`scripts/project_control.py:370`). Les tests contournent le problème en ajoutant systématiquement `--path reports/evidence/<WI>` (`tests/test_template.py:439`).
- **Correction proposée** : soit `create-work-item` ajoute automatiquement `reports/evidence/<WI>` aux chemins autorisés, soit `normal_path_errors` exempte ce préfixe pour le Work Item concerné (cohérent avec `validate_evidence`, qui l'exempte déjà du contrôle de fraîcheur), soit, a minima, le documenter.
- **Statut** : `OPEN`.

### Observations (sans scénario d'échec — ne bloquent rien)

- **O-01** Nouvelle doctrine « une autorisation humaine déjà donnée couvre les étapes ordinaires dans son périmètre » (`AGENTS.md:11-16`, reprise dans `README.md:18`, `ADOPTION.md:5-6`, `project_control/README.md:35`) : absente de `main`, introduite par un agent sous mandat général, classée par Codex « clarification ». C'est une règle d'autorité nouvelle ; elle mérite une ratification explicite (D1), pas une redline — elle répond au vrai problème de charge administrative.
- **O-02** Clé dupliquée `"BLOCKED": "BLOCKED"` (`scripts/project_control.py:1279-1280`) : inoffensif en Python, à nettoyer.
- **O-03** Une déclaration canonique illisible interrompt tout l'audit sous le libellé `INVALID_RECORDS` (`:2985`) au lieu d'un contrôle nominatif ; fail-closed, mais le message oriente mal (E3).
- **O-04** Le flux de preuves implique de commiter les rapports sur la branche canonique après intégration (c'est ce que font les fixtures : `tests/test_template.py:490-532`). `AGENTS.md:150` n'interdit que de « développer » sur la canonique ; cohérent, mais à dire explicitement dans le README des preuves.
- **O-05** `test_definition_of_done_keeps_levels_distinct` (`tests/test_template.py:2713-2721`) ne vérifie pas les deux nouveaux niveaux ; les rapports Codex portent deux conventions de nommage (`2026-09-06` vs `20260906`) ; numérotation des tests `foundation_02..04` sans `01`.
- **O-06** Incompatibilité avec les records d'une V3 antérieure (`start_head`, `runtime_target` obligatoires) : documentée et fail-closed (E6), mais toujours sans mécanisme de migration — l'action P2 de ma revue reste entière.
- **O-07** Coût d'`audit` linéaire en nombre de Work Items `DONE` avec preuves (≈ 80 ms/WI ici, E7), chaque mutation rejouant l'audit deux à trois fois ; sur Mac le facteur est plus élevé (la suite y prend 175 s contre 71 s ici). Pas de défaillance, mais un mur prévisible vers 100–200 Work Items : à surveiller, ou mettre en cache les preuves déjà validées par `close_head`.
- **O-08** Les commits Codex ne portent ni trailer d'agent ni référence de session ; la traçabilité d'auteur repose sur les rapports.
- **O-09** Le nouveau contrôle `BUSINESS_CHANGE_AUTHORIZATION` ne voit que les changements **non commités** : un commit métier direct hors Work Item sur la canonique reste indétectable par `audit`. Limite préexistante à `main`, non aggravée.

## F. Redlines

| Redline | Finding | Objet | Nature |
|---|---|---|---|
| R1 | F-01 | `811b63b` | décision de conception + documentation + test du cas E4 |
| R2 | F-02 | `c98a94a` | décision sur la règle, puis code **ou** DoD/README |
| R3 | F-03 | `c98a94a` | une ligne dans ADOPTION.md + alignement sur AGENTS.md |
| R4 | F-04 | les deux | déplacement de contenu vers `provenance/` |
| R5 | F-05 | `c98a94a` | code (auto-autorisation) ou documentation |

## G. Blockers

- Pour `c98a94a` seul : aucun blocker ; R2–R5 sont exécutables en une passe courte.
- Pour `811b63b` : R1 avant toute promotion de la fonctionnalité `block`/`resume` telle qu'annoncée.

## H. Conflits d'autorité relevés

1. Nouvelle doctrine d'autorisation (O-01) introduite dans `AGENTS.md` sans décision humaine enregistrée.
2. `ADOPTION.md` affaiblit `AGENTS.md:166` sur l'activation (F-03), contre `AGENTS.md:3`.
3. DoD « séparément » contre couplage du contrôleur (F-02).
4. La maintenance du core s'est faite « hors moteur » (Codex : « refus attendu de `BOOTSTRAP_CHANGE_SCOPE` ; la maintenance repose sur le mandat explicite ») — conforme à `AGENTS.md:26`, mais l'angle mort P1 §4 (mode `TEMPLATE_MAINTENANCE` absent) est maintenant exercé deux fois.

## I. Matrice de décisions humaines

| # | Décision | Options |
|---|---|---|
| D1 | Ratifier ou non la doctrine « autorisation déjà donnée couvre les étapes ordinaires » | ratifier par `HD` ; amender ; retirer |
| D2 | Règle de couplage `deployment` ↔ `runtime_proof` | couplage documenté ; relâchement « au moins une gate » |
| D3 | Stratégie de promotion | `c98a94a` seul après R2–R5 ; les deux après R1–R5 ; aucune |
| D4 | Politique d'entrelacement des Work Items bloqués (F-01) | (a) limite documentée ; (b) procédure d'alignement testée ; (c) records hors branche WI |
| D5 | Emplacement de l'histoire du template | `provenance/CHANGELOG.md` ; conserver dans `reports/` |
| D6 | Suite de ma revue du 05/09 : P3 (preuve de lecture), P4 (capability adversariale), P5 (objet `PHASE`), P7 (Definition of Ready) — non traités par Codex, toujours ouverts | prioriser ; différer |

## J. État Git final

Inchangé : HEAD `811b63bbf72f52329848fdcfec8e1ea73855afd8` sur `codex/v3-retour-v8`, `main` à `35da2a2…`, working tree propre, aucun fichier créé ou modifié dans le dépôt par cette revue (vérifié par `git status --porcelain=v2 --untracked-files=all` après chaque exécution).

## K. Verdicts

- `CODEX_V3_FIABILITE_SIMPLICITE_REQUIRES_MINOR_REDLINE` (commit `c98a94a`) — R2, R3, R4, R5.
- `CODEX_V3_RETOUR_V8_REQUIRES_MAJOR_REDLINE` (commit `811b63b`) — R1, plus héritage des précédentes.

## Réponse à la question posée

Sur le fond, **oui pour `c98a94a`**, et c'est une bonne livraison : elle ferme un trou que ma propre revue n'avait pas vu (une clôture acceptait n'importe quel texte comme preuve), lève un blocage réel d'`audit` sur tout projet initialisé contenant du code, ancre la provenance de démarrage dans Git, et couvre mon point P6 (guide de continuité) par une vue calculée plutôt que par un document de plus — meilleur choix que le mien. Les redlines sont courtes et ne remettent pas la conception en cause. La perte de `OMIT > ACTIVATE WITHOUT NEED` et la doctrine d'autorisation nouvelle sont des choix qui t'appartiennent : à ratifier explicitement plutôt qu'à laisser passer.

**Pas en l'état pour `811b63b`** : `block`/`resume` est bien construit et bien testé dans sa fenêtre, mais sa promesse centrale — parquer un chantier, en mener un autre, revenir — échoue dès que le chantier parqué porte un commit non intégré, et le remède manuel bute sur un conflit de records. Ce n'est pas un défaut de sécurité, c'est un dead-end ; il faut décider (D4) avant de promouvoir.

Enfin, la mise à jour ne traite pas P3, P4, P5 et P7 de ma revue : ce n'est pas un reproche — Codex a travaillé sur d'autres axes, issus de l'expérience Alpha — mais ces points restent ouverts au même titre.

---

## Suite — corrections des redlines (révision liée, 2026-09-06)

Mandat : « ok corrigeons les lignes rouges ! » ; décisions prises par le Project Owner : D4 = alignement automatique, D2 = couplage à sens unique, D5 = `provenance/CHANGELOG.md`, Git = branche dédiée. Posture : contributeur sous mandat explicite (maintenance du core du template), aucune promotion de `main`.

| Redline | Correction livrée |
|---|---|
| R1 (F-01) | `resume` aligne une branche divergée par un commit de merge de la canonique dans la branche du Work Item ; les records administratifs sont pris de la canonique ; un conflit métier annule le merge et refuse la reprise avec la liste des chemins ; un échec ultérieur ramène le tip (`update-ref` CAS). Tests `test_resume_aligns_diverged_branch_by_merge_and_closes` (scénario E4 jusqu'à la clôture) et `test_resume_refuses_business_conflict_and_restores_git_state`. Le rapport de `resume` nomme le mode d'alignement et le commit. |
| R2 (F-02) | Couplage à sens unique dans `validate_work_item` : cible `NOT_APPLICABLE` ⇒ deux gates `NOT_APPLICABLE` ; cible runtime ⇒ `runtime_proof` obligatoire, `deployment` libre. DoD, `project_control/README.md`, `AGENTS.md`, `ADOPTION.md` alignés. Test `test_runtime_target_requires_runtime_proof_but_deployment_stays_separate` (campagne de preuve sur déploiement existant clôturée `PRODUCTION_VERIFIED`, déploiement sans preuve refusé). |
| R3 (F-03) | `ADOPTION.md` : `OMIT > ACTIVATE WITHOUT NEED` rétabli ; « décision humaine documentée, comme l'exige AGENTS.md pour toute activation ». |
| R4 (F-04) | `provenance/CHANGELOG.md` créé (baseline `35da2a2`, `c98a94a`, `811b63b`, `claude/v3-redlines`) ; rapports Codex déplacés par `git mv` sous `provenance/maintenance/` ; sections de maintenance retirées de `WORKTREE_REGISTRY.md` ; `provenance/README.md` décrit le partage template / projet. |
| R5 (F-05) | `create-work-item` ajoute `reports/evidence/<WI-NNN>` aux `authorized_paths` ; documenté ; test `test_create_work_item_authorizes_its_evidence_directory`. |
| O-02, O-05 | Clé dupliquée supprimée ; le test de la DoD couvre les neuf niveaux. |

Livraison : branche `claude/v3-redlines`, commit `efdb7761b8114d8c9e6bf33eff5f1b19356ed335` (parent `811b63b`), 11 fichiers, +457 / −91, trailer `Co-Authored-By` et référence de session. `main` reste à `35da2a2`.

Vérification sur la machine après commit : `audit` PASS, `bootstrap-audit` PASS, `status` PASS, `check_git_traceability` PASS, `git diff --check` propre, `git fsck` propre, **73 tests OK en 28,9 s** ; même suite dans le bac à sable du reviewer : 73 OK en 95,8 s. Avant commit, `bootstrap-audit` refusait `BOOTSTRAP_CHANGE_SCOPE` sur les chemins core — refus attendu pour une maintenance du template hors Bootstrap Mode, identique à celui constaté par Codex. Hashes à HEAD : `scripts/project_control.py` `18021d01…d1cb` (blob `a1815cf`), `tests/test_template.py` `d80a9557…8c8cd` (blob `13271e9`).

Restent ouverts, hors redlines : O-01 (ratification de la doctrine « autorisation déjà donnée couvre les étapes ordinaires »), O-03, O-04, O-06 (migration des projets antérieurs), O-07 (coût linéaire de l'audit), O-08, O-09, et les points P3, P4, P5, P7 de la revue du 05/09. Une observation nouvelle issue de R1 : l'état administratif reste local à chaque branche jusqu'à intégration (le blocage doit être reporté sur la canonique avant `resume`, procédure documentée dans `project_control/README.md`) ; la cause racine — records administratifs portés par la branche du Work Item — relève d'une décision de conception à part.

---

## Promotion et baseline unique (2026-09-06, soir)

Décisions du Project Owner, enregistrées dans `provenance/CHANGELOG.md` de la baseline (commit `64a3cb1`) : `TPL-D-001` doctrine « autorisation déjà donnée couvre les étapes ordinaires » ratifiée telle quelle ; `TPL-D-002` promotion ; `TPL-D-003` baseline unique.

État final du dépôt `Squelette V3 -runtime-proof` : `main` = `64a3cb1d9281ee9e8d11277d84cd66a60d1f9aa2` (fast-forward de `claude/v3-redlines`, aucun merge à résoudre), tags annotés `v3.0.0` → `35da2a2` et `v3.1.0` → `64a3cb1`, checkout sur `main`, working tree propre. Après promotion : `audit`, `bootstrap-audit`, `status`, traçabilité, `git fsck` PASS, 73 tests OK (28,7 s). Les branches `codex/v3-fiabilite-simplicite`, `codex/v3-retour-v8` et `claude/v3-redlines` sont entièrement contenues dans `main` et conservées comme histoire.

Copies archivées (marqueur `ARCHIVED.md` commité + tag `archived-2026-09-06`, aucune autre modification) : `squelette-projet-gouverne` (`730a2a5` sur `feat/adoption-and-runtime-proof-v3`) et `squelette-decision-projet` (`3f6b1b0` sur `refactor/generalize-project-skeleton-v2`).

Constat : aucun des trois dépôts n'a de remote configuré ; le bare NAS mentionné pour les projets n'est relié à aucune copie du squelette. Le push de `main` et des tags reste à faire depuis le Mac, une fois le bare choisi.
