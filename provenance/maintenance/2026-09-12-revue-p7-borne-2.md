> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# REVUE_P7_BORNE-2 — Revue indépendante : le choix de la borne d'éligibilité (P7 étape 1)

**Verdict : `P7_BORNE_REVUE_REQUIRES_MAJOR_REDLINE`**

*Second contrôleur. Squelette 3.19.1, copie `source/` du dossier accordé. Revue rendue le 12 septembre 2026, 14 h (Europe/Zurich). Mandat : `MANDAT-REVUE-P7-BORNE.md`. Posture : lecture seule, rapport seul. Le livrable du premier contrôleur (`REVUE_P7_BORNE-1.md`, apparu à la racine pendant cette revue) et son dossier `runs/revue-1/` n'ont pas été ouverts.*

---

## 1. Résumé en trois points, pour le Project Owner

1. **Les mesures tiennent, à un détail près, mais elles ont laissé passer un caillou dans la chaussure.** Les sept mesures prises avant la revue sont justes dans leur conclusion. En rejouant la situation « un chantier est en attente, on monte de version, on le reprend », j'ai découvert que l'outil actuel refuse déjà cette reprise, quelle que soit l'option choisie, dès que le chantier en attente a produit au moins un commit et qu'un autre chantier a été clos entre-temps. Ce n'est pas la faute du nouveau champ : c'est un défaut de l'outil tel qu'il est aujourd'hui. Mais la promesse « un chantier ancien qui reprend reste ancien » ne pourra pas être tenue tant qu'il n'est pas corrigé, parce que la reprise elle-même ne passe pas.

2. **Parmi les trois façons de dater l'arrivée de la version, une seule tient debout dans la vie de tous les jours.** Marquer chaque nouvelle fiche à sa création (option A) donne la bonne réponse partout où j'ai regardé, avec une seule faiblesse : une fiche recopiée à la main d'un autre projet n'a pas la marque et passe entre les mailles — ce que l'outil accepte déjà aujourd'hui. Faire signer une décision par projet (option B) coûte onze gestes par projet existant, ne peut pas se faire dans un projet neuf avant la fin de son initialisation, et une décision oubliée ne se voit nulle part. Deviner la date dans l'historique (option C) change de réponse dès qu'on regroupe des commits, qu'on recrée le dépôt ou qu'on en prend une copie légère — j'ai montré les trois cas. Une quatrième voie, proche de A, est décrite pour mémoire.

3. **Ce qu'il vous reste à décider avant la construction.** D'abord, faire corriger la reprise refusée (ou accepter que la promesse ne soit testée que sur le cas simple). Ensuite, dire ce que « chantier ouvert » veut dire : créé, ou démarré. Enfin, dire comment la réponse entre dans la fiche : par la commande de création, ou par une commande à part, plus tard. Le mandat de construction ne le dit pas, et ce choix change deux des dix comportements attendus. Le reste — la forme du champ, les trous à boucher — est écrit plus bas, sans code.

---

## 2. Préflight

| | |
|---|---|
| Dossier accordé | `~/Projets/squelette-revue-p7` |
| `source/` | 125 fichiers, **sans `.git`** (copie exportée) : le commit d'origine n'est pas vérifiable depuis la copie ; le manifeste annonce `skeleton_version 3.19.1` |
| `core-manifest` sur une copie de lecture | `PASS: CORE_MANIFEST — skeleton_version 3.19.1, 24 core file(s)` ; `PASS: CORE_ALIGNED — tree matches the manifest` |
| Note | l'empreinte brute de `FIRST_START.md` (`fd16f922…`) diffère de celle du manifeste (`c83e2351…`) : le contrôleur normalise le marqueur `INITIALIZATION_STATUS` avant de hasher (`core_digest`, l. 144-153). Ce n'est pas un écart. |
| `scripts/project_control.py` | 6 514 lignes — SHA-256 `3d3e76de08d347467a8843930ac53066f74f37baa783384fbd1c6f10e4d349f0` — **identique à ce qu'annonce E2 § A** |
| `project_control/schemas/work-item.v1.schema.json` | SHA-256 `52423cacc127ccb60bb8ffd638172033d9b4251b6be08f587f4f0e685f09afd0` — identique à E2 |
| E1 `entrees/mandat-construction-p7-etape-1.md` | SHA-256 `832cba09e5487ff4d24ca874877ead307b71b6c67631f0f7ebd954b369995a2f` |
| E2 `entrees/D1-rapport-mesure-phase-0-P7-etape-1.md` | SHA-256 `ae2ef9efe66b911d5a9905b66c4cf908d43daafd403ec5212936dcc7c0f570fd` |
| `MANDAT-REVUE-P7-BORNE.md` | SHA-256 `3dc14ae0cef2e95525e3ab9c96903bb7668b914c4f0aa51a4555563fd1a60046` |
| Empreinte de `source/` avant | liste triée `chemin sha256` des 125 fichiers : SHA-256 de la liste `6e97fe91388b93877bd1221eccecfb6320e5bdcbd53be4617541fac6d32eba03` (`runs/revue-2/preflight/source-hashes-avant.txt`) |
| Empreinte de `source/` après | identique, `6e97fe91…` (`runs/revue-2/preflight/source-hashes-apres.txt`, `cmp` : aucune différence) |
| Suite d'essais | 164 essais joués sur la copie : **162 verts, 2 en échec parce que la copie n'a pas de `.git`** (`git ls-files`, `git archive`) — cohérent avec « 164 verts » annoncé par E2 sur un clone. Sortie : `runs/revue-2/transcriptions/tests-3.19.1-sur-copie-sans-git.txt` |
| Livrable | `REVUE_P7_BORNE-2.md` n'existait pas au début ; écrit une fois, à la fin |

**Environnement de rejeu.** Le dossier accordé est monté sans droit de suppression dans la VM de session : Git ne peut pas y effacer ses verrous (`index.lock`) ni ses objets temporaires (`tmp_obj_*`) et s'arrête au deuxième commit (constaté sur `runs/revue-2/t01/`). Ma demande de droit de suppression a été bloquée par un filtre automatique. Sur double arrêt du Project Owner (STOP 1 puis « Confirmé : bac à sable de session, transcriptions dans ~/Projets/squelette-revue-p7/runs/revue-2/, source/ intouché, pas de push. »), les dépôts jetables ont tourné dans l'espace temporaire de la session (`$HOME/atelier-revue-2/` de la VM, hors de tout dossier de l'utilisateur), sans `push`, `fetch`, `tag` ni accès à un autre dépôt ; **chaque commande et sa sortie sont recopiées** dans `runs/revue-2/transcriptions/`, et les scripts dans `runs/revue-2/outils/bac-a-sable/`. Toutes les décisions, fiches et commits inventés portent la marque « EXEMPLE DE REVUE — FICTIF, N'AUTORISE RIEN ».

**Base de rejeu.** Un projet gouverné est construit en rejouant la démo `examples/hello-squelette/demo.py` depuis la copie (initialisation, interview, WI-001 créé, démarré, intégré, clos : dix commits, `status` PASS, garde-fou installé hors de l'arbre). Puis une chronologie « chrono » : WI-003 (fiche écrite à la main) démarré, un commit, bloqué ; WI-006 démarré et bloqué sans commit ; WI-004 = montée vers une 3.20.0 fictive (`ADOPTION.md` retouché, manifeste réécrit par `core-manifest --write`, `template-upgrade --apply` sous Work Item, fusion, preuve, clôture) ; reprises ; WI-005 créé après la montée. Repères : `runs/revue-2/transcriptions/chrono-reperes.json`.

---

## 3. T-01 — Les sept mesures tiennent-elles ?

Rejeu : `runs/revue-2/t01/mesures_t01.txt` (mesures sans Git, script `runs/revue-2/outils/mesures_t01.py`) et `runs/revue-2/transcriptions/t01-git.txt`.

| Mesure | Résultat | Preuve |
|---|---|---|
| B.1 — le record n'entre pas dans l'empreinte | **Confirmée dans la configuration standard, fausse dans une configuration que le projet peut choisir** (constat C-03) | routage : 37 chemins, aucun sous `project_control/work-items/` ; `MANIFEST_EXCLUDED_PATHS` (l. 93-103) n'exclut pas les records ; rejeu pour `scripts/`+`project_control/` → 22 documents, `docs/governance/` → 12, `applications/` → 12, sans record. Le schéma `work-item` est bien routé (scope `development`). |
| B.2 — emplacement et schéma | **Partiellement confirmée** : `additionalProperties: false` exact, lignes exactes (l. 1236, 1388, 2090, 2984, 6189-6228) ; mais **31** champs `required` et **33** propriétés, pas 30 et 32 (les deux en trop sont bien `close_head` et `block_records`) | `mesures_t01.txt` § B.2 |
| B.3 chemin 2 — le champ doit rester facultatif | **Confirmée, et incomplète** : le schéma n'est pas le seul endroit (constat C-05) | record ancien + `prior_art` → `unexpected property prior_art` ; ancien + optionnel → aucune erreur ; ancien + requis → `missing prior_art` |
| B.3 chemin 1 — aucune baseline ne date une version | **Confirmée** | `BASELINE_DECISION_FIELDS` l. 37-40 (deux entrées) ; `legacy_baseline` l. 5565, `authorities_baseline` l. 5633, `legacy_records` l. 5709, `frozen_decision_refs` l. 5590 ; `template_upgrade` (l. 3820-3980) n'écrit ni date, ni repère, ni commit : `now_iso`, `commit_records`, `today_iso` absents de son corps |
| B.4 — `status` et l'emplacement de la ligne | **Confirmée** | boucle l. 6429-6442 ; catalogue `SPEECH` l. 307-321 (`status.missing` l. 310, `status.authorities` l. 312) |
| B.5 — pas de contrôle d'audit nommé nouveau | **Confirmée** | `require_authorities_digest` l. 3498 ; la forme des Agent Runs est revérifiée par `agent_run_authority_errors` (l. 3572) via `project_control_errors` (l. 3018) → `SCHEMA_VALIDATION` |
| B.6 — convention de nommage | **Confirmée sur la forme, chiffre différent** : **64** noms distincts (E2 : 58), tous `MAJUSCULES_SOULIGNÉ` ; `PRIOR_ART_DECLARED` s'y inscrit | liste complète dans `mesures_t01.txt` § B.6 (les six de plus viennent de `template-upgrade`, `install-gate`, `pre-commit`) |
| B.7 — 0 chantier dans la copie | **Confirmée** | `project_control/work-items/` = `README.md` seul ; `legacy_baseline: null`, `authorities_baseline: null`, `NOT_STARTED` |

### 3.1 Le point B.1 : existe-t-il une configuration où le record entrerait dans l'empreinte ? — Oui

`docs/agent-governance/mandatory-documents.v1.json` **n'est pas un fichier core** (`CORE_ROOTS`, l. 72-77) : il appartient au projet, qui peut y router ce qu'il veut. Le contrôle `DOCUMENT_ROUTING` (l. 2055-2072) exige seulement que chaque chemin routé soit un fichier existant hors `templates/`. Un projet qui route `project_control/work-items/WI-002.json` obtient `PASS: DOCUMENT_ROUTING`, et le record entre dans l'empreinte (`t01-git.txt`, S1.2 : `AUTHORITY: project_control/work-items/WI-002.json sha256=…`). Conséquences mesurées dans cette configuration :

- écrire une réponse dans le record après `context-manifest` périme l'empreinte : `start` refuse (`authorities digest does not match`) — c'est le serpent qui se mord la queue que le § 3 de E1 redoutait ;
- pire, et **indépendamment de `prior_art`** : après recalcul, `start` échoue quand même — il écrit `status`, `start_head`, `agent_run_refs` dans le record **avant** son preflight, qui trouve l'autorité changée (`start preflight failed: AUTHORITY_MANIFEST_CURRENT … ['project_control/work-items/WI-002.json']`). Le chantier ne peut jamais démarrer ; la transaction est bien annulée (record revenu à `AUTHORIZED`, arbre propre).

La conclusion de E2 est donc vraie **par construction du routage par défaut**, pas par construction du contrôleur. Constat C-03.

### 3.2 Le point B.3 : un autre endroit que le schéma refuserait-il un record ancien ? — Oui, deux

1. `validate_work_item()` (l. 1388) porte **sa propre liste `required`** (l. 1393-1400, 29 champs, indépendante du schéma) lue par `required_field_errors` (l. 1292). Ajouter `prior_art` à cette liste ferait tomber tous les anciens records avec `Work Item: missing prior_art` (rejoué, `mesures_t01.txt` § B.3), le schéma fût-il facultatif.
2. `records()` (l. 2007-2016) valide chaque record au chargement et **lève** `invalid record` : une forme refusée ne produit pas un `FAIL: SCHEMA_VALIDATION` isolé, elle casse `status`, `audit`, `preflight` et toute transition d'un coup (`t01-git.txt`, S1.1 : `Project: UNKNOWN | INVALID … Error: invalid record: work-item: unexpected property prior_art`). Toute erreur de forme de `prior_art` sur un record touché à la main aura le même effet.

À noter aussi pour le constructeur : `status_payload` (l. 5843-5876) et `preflight_findings` lisent les champs du record par indexation directe (`item["applicability"]`) ; une ligne B10 écrite `item["prior_art"]` casserait `status` sur tout record ancien. Observation O-01.

---

## 4. T-02 — Option A (la marque voyage dans la fiche) en usage courant

Rejeu : `t02-chrono.txt`, `t02-contre-epreuve.txt`. L'option est une intention ; ce qui est démontré, c'est ce que le contrôleur d'aujourd'hui fait des situations qu'elle devra traverser.

| Situation | Ce que donne A | Démonstration |
|---|---|---|
| Montée de version alors qu'un chantier est ouvert, puis reprise | **Réponse juste** (pas de marque → pas de question) — **mais la reprise elle-même est refusée aujourd'hui** dès que la branche du chantier porte un commit et qu'un autre chantier a été clos sur la canonique entre-temps | S2.4 : `resume WI-003` → `cannot commit alignment merge … SCHEMA_VALIDATION: WI-004: close_head is missing or not in current history`. Contre-épreuve S2.6 sans fiche à la main, sans montée : `resume WI-006` → même refus (`WI-005: close_head …`). Constat **C-01** |
| Chantier créé, bloqué, repris des semaines plus tard | **Juste** : `block` (l. 5083) et `resume` (l. 5290) recopient le record par aller-retour JSON ; une marque posée à la création y survit comme `title` et `close_condition` y survivent | S2.2 → S2.4 bis : `WI-006` bloqué puis repris (fast-forward), champs inchangés (`[après resume — WI-006]`) |
| Fiche recopiée d'un autre projet ou écrite à la main | **Fausse (chantier neuf épargné)** : la fiche n'a pas de marque, et le contrôleur ne peut pas distinguer « ancienne » de « sans marque » | S2.1 : `WI-003` écrit à la main (fixture recopiée) + décision, conversation, roadmap, registre écrits à la main → commit accepté sur `main` (chemins administratifs, audit indexé PASS) → `start WI-003` PASS. Constat **C-06** |
| Projet neuf créé à partir du modèle | **Juste pour tout chantier créé par `create-work-item`** ; `WI-000` (fiche d'initialisation, écrite à la main en Bootstrap Mode comme dans la démo, l. 338-398 de `demo.py`) n'aura pas de marque — sans effet, il ne passe jamais par `start` | démo rejouée : `WI-000` clos à la main à la clôture de l'initialisation |
| Montée interrompue puis relancée | **Juste** : `template-upgrade --apply` écrit le core dans une transaction à annulation (l. 3953-3964) ; entre l'application et le commit, `create-work-item` exécute déjà le nouveau script sur le disque, donc marque | lecture du code ; non rejoué (une interruption au milieu d'une transaction ne se pilote pas par commande) — observation |

Point non couvert par A comme par les autres : **« ouvert » n'est pas défini** (créé ou démarré ?). Une fiche créée avant la montée et démarrée après n'a pas de marque : A la traite en ancienne. B7 parle de « repris », ce qui suppose démarré avant. Si l'intention est « démarré après la montée = éligible », A répond faux sur ce cas ; si c'est « créé après », A répond juste. Constat **C-08**.

---

## 5. T-03 — Option B (la borne signée par décision) en usage courant

Rejeu : `t03-option-b.txt`, sur le modèle exact des deux baselines existantes.

| Situation | Ce que donne B | Démonstration |
|---|---|---|
| Décision absente | **Indécidable sans casser un comportement attendu.** Le précédent `authorities_baseline` lit `null` comme « la règle vaut pour tous » : un run ancien sans preuve met l'audit en échec (S3.4). Transposé : `null` = tous éligibles → un projet existant qui oublie la décision interroge ses chantiers anciens (B7 cassé) ; `null` = personne → la règle est éteinte dans tout projet neuf. Et **l'oubli est invisible** : l'audit ne peut pas exiger la réponse (B10 tolère `UNKNOWN`), donc la répétition de montée (`UPGRADE_REHEARSAL`) ne peut pas le voir. | S3.4 : `FAIL: SCHEMA_VALIDATION — Agent Run RUN-WI-001-001: authorities_read is required after the adoption baseline; … exempt only through authorities_baseline` |
| Décision écrite après coup | Acceptée : rien ne rattache la décision au moment de la montée ; entre la montée et la décision, la règle s'est appliquée (ou non) selon le sens donné à `null` | S3.2 |
| Décision nommant un commit qui n'est pas celui de la montée | **Acceptée en silence** : le contrôleur vérifie que le commit existe, est ancêtre de HEAD et est nommé par la décision (`require_baseline_named`, l. 5533) — jamais qu'il correspond à un changement de manifeste | S3.2 : baseline déclarée au commit du blocage de WI-006 (`3911fca…`, antérieur à la montée) → `audit` PASS, `status --json` l'affiche |
| Commit hors de l'histoire de la canonique | Refusée (juste) | S3.3 : `authorities baseline 5b8b27f… is missing or not in current history` |
| Projet sans baseline d'adoption préalable | Sans effet : la troisième baseline est indépendante des deux autres (champs séparés) | lecture, `BASELINE_DECISION_FIELDS` |
| Projet neuf, sans montée à dater | **Impossible avant la clôture de l'initialisation** : `NOT_STARTED cannot declare …` (l. 1366-1369) | S3.1 : `bootstrap-audit` → `FAIL: SCHEMA_VALIDATION — project-state: NOT_STARTED cannot declare an authorities_baseline` |

**Coût réel d'adoption, mesuré (S3.2).** L'état du projet n'est pas un chemin administratif : le committer directement sur `main` est refusé (`CANONICAL_BRANCH_PROTECTED`). La chaîne qui passe, geste par geste : (1) écrire la décision à la main avec son champ `… baseline commit:`, (2) la committer, (3) `create-work-item` autorisé sur `project_control/project-state.v1.json`, (4) `context-manifest`, (5) `start`, (6) éditer l'état, (7) committer sur la branche, (8) revenir sur `main`, (9) fusionner, (10) écrire et committer la preuve d'intégration, (11) `close`. **Onze gestes par projet existant**, deux de moins si la déclaration monte dans le chantier de montée lui-même (qui doit alors ajouter l'état du projet à ses chemins autorisés). **Projet neuf : zéro geste si `null` signifie « tous éligibles », sinon les mêmes onze après la clôture de l'initialisation.**

**Le « modèle exact » n'existe pas.** La doctrine des baselines actuelles dit l'inverse de B7 : « Un Work Item non clos à la baseline (`AUTHORIZED`, `BLOCKED`, `IN_PROGRESS`) suit le contrat courant à sa prochaine clôture … Ni le numéro du Work Item ni l'absence d'un champ ne donnent d'exemption » (`project_control/README.md` l. 261). Une borne « sur le modèle exact » exempterait donc seulement les chantiers **clos** avant elle. Pour tenir B7, il faut écrire une règle d'exemption nouvelle (« record présent dans l'arbre au commit de la borne », comme `legacy_records()` lit les records au commit de la baseline) et amender la phrase de doctrine. Constat **C-04**.

---

## 6. T-04 — Option C (la borne déduite de l'historique) en usage courant

Rejeu : `t04-option-c.txt`. Déduction utilisée : premier commit dont le manifeste porte la nouvelle version (`git log --reverse -S '"skeleton_version": "3.20.0"' -- provenance/core-manifest.v1.json`), records « avant » = présents dans l'arbre à ce commit.

| Situation | Ce que donne C | Démonstration |
|---|---|---|
| Histoire intacte | **Deux bornes candidates** : le commit d'application sur la branche (`7f7afd2…`) si l'on parcourt toute l'histoire, le commit de fusion (`ec68085…`) si l'on suit la première parenté. Ici le même ensemble de records ; en général, tout record créé sur la canonique entre l'ouverture de la branche de montée et sa fusion est absent du premier et présent au second | S4.1 |
| Historique regroupé (squash) | **Fausse (chantier neuf épargné)** : la borne devient le commit regroupé, dont l'arbre contient déjà `WI-005`, créé après la montée | S4.2 : records à la borne `['WI-000','WI-001','WI-003','WI-004','WI-005','WI-006']` |
| Dépôt recréé sans son historique | **Fausse pour tout le monde** : un seul commit porte la version, tous les records y sont, tous exempts | S4.3 |
| Copie de travail sans les objets Git (`clone --depth 1`) | **Fausse pour tout le monde**, comme ci-dessus ; et les vérifications d'ascendance des baselines actuelles échouent déjà sur une telle copie (`cat-file -e` → `Not a valid object name`) | S4.4 |
| Cœur installé sans son manifeste | Sans objet : l'audit échoue avant (`MANDATORY_FILES`, `CORE_MANIFEST`), aucune transition — comme pour A et B | S4.5 |
| Version montée puis ramenée en arrière, puis remontée | **Fausse dans un sens ou dans l'autre** : trois commits touchent la version (arrivée, retrait, seconde arrivée). « Première arrivée » interroge `WI-007`, né pendant le retour en 3.19.1 ; « dernière arrivée » l'épargne mais épargne aussi tout chantier né entre la première arrivée et le retrait | S4.6 |

Constat **C-07**.

---

## 7. T-05 — Une seule frontière, et les dix comportements

### 7.1 Unicité de la frontière

- **A** : une frontière — la marque dans le record — lue à l'identique par `start`, par `validate_work_item` (audit) et, pour la forme du champ, par le schéma. Le schéma ne peut pas exprimer « marque ⇒ réponse exigée » (T-06, S6.5) : ce n'est pas une seconde frontière, c'est une lecture de moins ; l'éligibilité vit dans le validateur, comme aujourd'hui les règles conditionnelles de `validate_work_item`.
- **B** : le commit est unique, sa **lecture** ne l'est pas tant qu'elle n'est pas écrite : « record présent dans l'arbre à la borne » (le modèle de `legacy_records()`) et « commit de création du record ancêtre de la borne » divergent pour un record créé sur la canonique pendant la vie de la branche de montée. Avec la lecture « présent à la borne », la frontière est unique, au prix de la règle nouvelle de C-04.
- **C** : **deux frontières apparaissent et divergent**, démontrées : toute l'histoire contre première parenté (S4.1), première contre dernière arrivée (S4.6) ; et la frontière change d'une copie à l'autre du même projet (S4.2, S4.3, S4.4).

### 7.2 Les dix comportements

| | A — marque | B — décision | C — historique |
|---|---|---|---|
| B1 champ absent → refus | tenu tel quel | tenu tel quel | tenu tel quel |
| B2 FOUND sans candidat / sans chemin / sans point d'entrée | tenu tel quel | tenu tel quel | tenu tel quel |
| B3 chemin inexistant | tenu tel quel | tenu tel quel | tenu tel quel |
| B4 NONE_FOUND incomplet | tenu tel quel | tenu tel quel | tenu tel quel |
| B5 REIMPLEMENT sans justification | tenu tel quel | tenu tel quel | tenu tel quel |
| B6 complet → `declared_at` posé | tenu tel quel | tenu tel quel | tenu tel quel |
| **B7** ouvert avant, repris après | **tenu tel quel** (pas de marque) — sous réserve de C-01, qui refuse la reprise par fusion pour toutes les options | **au prix d'une règle** : exemption « présent à la borne », contraire à la doctrine actuelle des baselines (C-04) ; plus le sens de `null` | **au prix d'une règle** (la même) **et impossible à garantir** : la borne bouge (S4.2, S4.6) ou disparaît (S4.3, S4.4) |
| **B8** audit vert sur un dépôt de records anciens | tenu tel quel (aucun record marqué, aucun contrôle de présence) | tenu tel quel **si** `null` = tous éligibles et si l'audit n'exige jamais la réponse ; au prix d'une règle sinon | tenu tel quel (dépôt sans montée : rien à déduire) |
| **B9** déclaration figée, chemin déplacé | tenu tel quel (existence vérifiée au démarrage seulement, B.5) | tenu tel quel | tenu tel quel |
| **B10** `status` : ligne `UNKNOWN` sur un éligible sans réponse | tenu tel quel (la marque et la réponse sont deux choses ; il faut une marque distincte de la réponse, puisque E1 refuse une troisième valeur) | au prix d'une lecture Git par record dans `status` (`ls-tree` à la borne) et du sens de `null` | au prix d'un parcours d'historique dans `status`, faux ou vide sur les copies de S4.3/S4.4 |

B1 à B6 ne dépendent que de la validation de la réponse au démarrage, une fois l'éligibilité connue ; B7, B8 et B10 sont ceux qui séparent les options, comme le mandat l'annonçait. B9 ne sépare rien.

---

## 8. T-06 — La forme du champ

Rejeu : `t06-forme-du-champ.txt` (validateur `schema_record_errors`, l. 1236).

Ce qui franchirait un schéma écrit au plus près de E1 § 4 sans rien dire d'utile — chacun rejoué :

| Réponse creuse | Le schéma la laisse passer ? | Pourquoi |
|---|---|---|
| `capability: " "`, `"\t"`, `"\n"` | oui | `minLength: 1` compte les blancs (S6.1) |
| `terms: ["a"]`, `justification: "x"` | oui | rien ne mesure un contenu |
| `paths: [" "]` | oui | `minItems: 1` + `minLength: 1` (S6.3) |
| `candidates: [{"path": "README.md", "entry_point": "-", "note": ""}]` | oui | le chemin existe, le point d'entrée est un tiret (S6.6) |
| `searched.paths: ["docs"]` ou `["modules"]` | oui | un dossier existe — et vaut « j'ai cherché partout » |
| `searched.paths: ["."]` | non | `safe_relative_path(".")` répond `None` (S6.4) : seule protection existante, involontaire |
| `FOUND` **et** `searched`, `NONE_FOUND` **et** `candidates` | oui | le validateur ne connaît ni `if/then`, ni `oneOf`, ni `dependentRequired` (S6.5) : les exigences conditionnelles de E1 § 4 **ne s'écrivent pas dans le schéma**, elles se codent dans `validate_work_item` — E1 ne le dit pas |
| `declared_at` déjà écrit à la main avant le démarrage | oui | rien n'interdit de le poser soi-même (S6.6) ; « posé par le contrôleur au démarrage, figé ensuite » n'est vérifié nulle part |
| `external` seul, sans candidat | oui | aucun contrôle, ce que E1 veut — mais alors `FOUND` avec `external` seul et `candidates: []` doit être dit refusé (E1 exige « au moins un » candidat : oui, mais `external` n'est pas un candidat) |

« Une chaîne non vide ne vaut pas réponse » : E1 le dit une fois, en fin de § 4, sans dire ce qui vaut réponse. Ce n'est pas suffisant pour un constructeur, ni pour un relecteur. **Formulation proposée, à insérer sous la forme du § 4 (sans code) :**

> Une réponse est **complète** quand, une fois les blancs retirés du début et de la fin, aucun texte exigé n'est vide ; quand chaque liste exigée a au moins un élément, lui-même complet ; quand chaque chemin cité est relatif au dépôt, sûr (ni absolu, ni `..`, ni la racine), et existe au démarrage — un chemin de `candidates` désigne un fichier, un chemin de `searched.paths` peut désigner un dossier ; quand `FOUND` porte `candidates` et `reuse_decision`, et ne porte pas `searched` ; quand `NONE_FOUND` porte `searched` et ne porte ni `candidates`, ni `reuse_decision`, ni `justification` ; quand `justification` est présente si et seulement si `reuse_decision` vaut `REIMPLEMENT` ; et quand `declared_at` est **absent** avant le démarrage — le contrôleur le pose, et refuse une déclaration qui l'a déjà. Le contrôleur ne juge ni le sens de `capability`, ni la pertinence d'un candidat, ni la longueur d'une justification : il constate la complétude, rien de plus. Ces règles conditionnelles vivent dans le validateur du contrôleur ; le schéma ne décrit que la forme de chaque champ, avec un motif « au moins un caractère non blanc » pour chaque texte exigé.

Le validateur supporte `pattern` (S6.2 : `"\S"` refuse `" "` et `"\t\n"`), ce qui rend la première règle applicable dès le schéma. Constat **C-09**.

---

## 9. T-07 — L'angle retenu : par quel geste la réponse entre-t-elle dans la fiche ?

Pourquoi celui-là : aucune question du mandat ne le pose, E1 ne le dit pas, et il décide de deux comportements attendus et d'un des trous de T-02.

**Ce que le contrôleur permet aujourd'hui.** Une fiche naît par `create-work-item`, dont chaque champ est une option de ligne de commande (l. 6189-6228), plusieurs `required=True`. Ensuite, **aucune commande ne modifie un champ d'un Work Item** en dehors des transitions (`start`, `block`, `resume`, `acknowledge-authorities` — sur l'Agent Run —, `close`). Les records sont « ceux de Project Control », committés par lui sur la canonique (`commit_records`, l. 4449). Pourtant, le garde-fou accepte un commit humain de chemins administratifs sur la canonique dès que l'audit de l'état indexé passe : démontré deux fois — une fiche entière écrite à la main (S2.1), un champ modifié à la main (`objective`, `t01-git.txt` S1.2, commit accepté). La voie de fait pour remplir `prior_art` entre la création et le démarrage serait donc **l'édition à la main d'un record sur `main`**, précisément ce que la doctrine dit ne jamais arriver.

**Les deux choix possibles, et ce qu'ils changent.**

1. *La réponse est donnée à la création* (nouvelles options de `create-work-item`). Alors B1 à B5 deviennent des refus **à la création**, pas « au démarrage » comme E1 § 5 l'écrit ; B10 (éligible sans réponse) ne peut plus se produire, puisqu'une fiche éligible naît avec sa réponse ; `declared_at` devrait être posé à la création ou rester posé au démarrage — E1 doit trancher. Plus simple, une seule transaction, aucun record à retoucher. Coût : pour une correction d'une ligne, la réponse est exigée avant même que la fiche existe — c'est l'esprit du point 2 de E1 § 2.
2. *La réponse est donnée après la création, avant le démarrage* (nouvelle commande, par exemple `declare-prior-art WI-NNN …`, exécutée depuis la canonique, committée par le contrôleur comme une transition). Alors B10 a un sens, les refus B1-B5 restent au démarrage, `declared_at` est posé au démarrage comme E1 le dit ; et la déclaration ne passe jamais par une édition à la main. Coût : une commande et une transition de plus, et une fiche peut vivre « éligible sans réponse » — état que `status` doit montrer (B10).

Dans les deux cas, la règle « l'existence des chemins se vérifie une fois, au démarrage » (E1 § 2.6) demande que la vérification soit faite par `start`, même si la réponse est écrite plus tôt.

**Lien avec la borne.** Sous A, le geste 1 fait naître marque et réponse ensemble ; le geste 2 exige une marque distincte de la réponse (sinon « pas de réponse » et « pas éligible » se confondent — la troisième valeur que E1 refuse reviendrait par la bande). Sous B et D (§ 11), la fiche écrite à la main de S2.1 est jugée par la borne, pas par sa marque : le trou C-06 se ferme. Constat **C-10**.

---

## 10. Constats, du plus grave au moins grave

Chaque constat : identifiant, sévérité, objet, situation reproductible, preuve, conséquence, correction suggérée. Les observations (sans situation démontrée) suivent.

### C-01 — majeur — La reprise d'un chantier bloqué est refusée dès qu'un autre chantier a été clos sur la canonique (contrôleur 3.19.1, sur le chemin de B7)

- **Objet** : `resume_work_item` (l. 5156) → `merge_canonical_into_branch` (l. 4631) → commit de la fusion d'alignement sous le garde-fou → `MODE_AUDIT` → `done_evidence_errors` (l. 5795), `merge-base --is-ancestor close_head HEAD` (l. 5808), HEAD étant la pointe de la branche du chantier pendant la fusion.
- **Situation** : (1) WI-A démarré, un commit sur sa branche, `block` ; (2) WI-B créé, démarré, fusionné, clos sur `main` ; (3) `resume WI-A` avec décision et empreinte valides.
- **Preuve** : `t02-chrono.txt` S2.4 (WI-003 / WI-004, avec montée) et `t02-contre-epreuve.txt` S2.6 (WI-006 / WI-005, fiches créées par le contrôleur, sans montée) : `FAIL: TRANSACTION — cannot commit alignment merge: … FAIL: MODE_AUDIT — SCHEMA_VALIDATION: WI-005: close_head is missing or not in current history`. L'annulation est propre : record `BLOCKED`, arbre propre, `main` extrait, `audit` PASS ensuite.
- **Conséquence** : un chantier bloqué qui a déjà travaillé ne peut plus reprendre une fois qu'un autre chantier a été clos — c'est-à-dire dans le cas courant. Pour P7 : B7 (« chantier ouvert avant adoption, repris après ») n'est exerçable que dans la variante sans commit (fast-forward, S2.4 bis) ; un essai B7 vert ne prouvera que ce cas.
- **Correction suggérée** : pendant une fusion (`MERGE_HEAD` présent), juger `close_head` contre `HEAD` **et** `MERGE_HEAD` (ou contre l'arbre que le commit va écrire, comme le garde-fou le fait déjà pour l'état indexé) ; un essai rouge sur 3.19.1 avec le scénario S2.6. Hors périmètre P7 par sa cause, dans son périmètre par son effet : à corriger avant ou avec P7, et à dire dans le rapport de construction.

### C-02 — majeur — L'option C (borne déduite) répond faux ou ne répond pas dans quatre situations ordinaires

- **Situation / preuve** : `t04-option-c.txt` S4.2 (squash : `WI-005`, créé après la montée, présent à la borne → épargné), S4.3 (dépôt recréé : tous épargnés), S4.4 (clone superficiel : tous épargnés, et `cat-file -e` échoue), S4.6 (retour arrière puis remontée : trois commits candidats), S4.1 (deux parcours, deux commits).
- **Conséquence** : la frontière n'est pas unique (point 5 de E1 § 2 violé par construction) et change d'une copie à l'autre du même projet.
- **Correction suggérée** : écarter l'option, ou ne la garder que comme *indication* affichée, jamais comme frontière.

### C-03 — modéré — La conclusion B.1 dépend d'un fichier que le projet contrôle ; dans une configuration permise, `start` est impossible

- **Objet** : `DOCUMENT_ROUTING` (l. 2055-2072) accepte de router un record ; `MANIFEST_EXCLUDED_PATHS` (l. 93-103) n'exclut pas `project_control/work-items/` ; `start` écrit le record avant son preflight (l. 4989-5000).
- **Situation** : router `project_control/work-items/WI-002.json` dans `mandatory-documents.v1.json` (commit sous mandat), `context-manifest WI-002`, `start WI-002 --authorities-digest <empreinte>`.
- **Preuve** : `t01-git.txt` S1.2 : `PASS: DOCUMENT_ROUTING` ; le record dans le manifeste ; `start` → `authorities digest does not match` après une réponse écrite dans le record ; après recalcul, `start preflight failed: AUTHORITY_MANIFEST_CURRENT … ['project_control/work-items/WI-002.json']`.
- **Conséquence** : E2 § B.1 est vrai par le routage par défaut, pas par le contrôleur ; un projet peut se mettre lui-même dans le cercle vicieux, `prior_art` ou non.
- **Correction suggérée** : exclure `project_control/work-items/`, `agent-runs/`, `conversations/` de l'empreinte par construction (préfixes dans l'exclusion, comme `project-state.v1.json` l'est déjà), ou refuser leur routage dans `DOCUMENT_ROUTING`. À écrire dans la fiche de P7 comme hypothèse rendue vraie, pas mesurée.

### C-04 — modéré — « Sur le modèle exact des baselines existantes » contredit B7 ; l'option B exige une règle nouvelle et une phrase de doctrine amendée

- **Objet** : `project_control/README.md` l. 261 (« Un Work Item non clos à la baseline … suit le contrat courant à sa prochaine clôture … Ni le numéro du Work Item ni l'absence d'un champ ne donnent d'exemption ») ; `legacy_done` (l. 5791) n'exempte que les `DONE` à la baseline ; `frozen_decision_refs` exempte des décisions, pas des chantiers ouverts.
- **Situation** : un chantier `BLOCKED` à la borne, repris après : sous le modèle exact, il « suit le contrat courant » → interrogé → B7 cassé.
- **Preuve** : lecture (l. 261, 5791-5793, 1696-1706) ; la mécanique existante ne connaît aucune exemption d'un chantier ouvert.
- **Correction suggérée** : si B est retenue, écrire l'exemption « record présent dans l'arbre au commit de la borne », et amender la phrase de doctrine pour dire que la borne P7 fait exception à « suit le contrat courant ».

### C-05 — modéré — E2 § B.3 ne mesure que le schéma ; deux autres endroits refuseraient un record ancien

- **Objet / preuve** : liste `required` propre de `validate_work_item` (l. 1393-1400) — `mesures_t01.txt` § B.3 (`Work Item: missing prior_art`) ; `records()` (l. 2007-2016) lève sur toute forme refusée — `t01-git.txt` S1.1 (`status` → `INVALID`, `audit` → trois `FAIL`, `preflight` → `INVALID_RECORDS`).
- **Conséquence** : le constructeur qui suit E2 à la lettre (« le champ entre dans `properties` et jamais dans `required` ») peut tout de même casser tous les anciens records par la seconde liste, et une seule fiche mal formée arrête tout le projet.
- **Correction suggérée** : compléter E2 § B.3 ; ajouter à la liste des essais « anciens records intacts avec le nouveau validateur » (B8 le couvre si l'essai passe par `audit` complet, pas par le schéma seul).

### C-06 — modéré — Sous l'option A, une fiche écrite à la main ou recopiée d'un autre projet échappe à la question

- **Situation / preuve** : `t02-chrono.txt` S2.1 — fiche recopiée de la fixture, décision, conversation, roadmap et registre écrits à la main, commit accepté sur `main` (`MODE_AUDIT — audit PASS on the working tree and the staged state`), puis `start WI-003` PASS.
- **Conséquence** : « sans marque » et « ancienne » sont indistinguables pour A ; un chantier neuf recopié n'est pas interrogé (réponse fausse par omission).
- **Correction suggérée** : soit accepter le risque en le nommant dans la fiche de P7 (les records écrits à la main sont déjà hors doctrine, et déjà acceptés aujourd'hui pour tout le reste), soit fermer la porte en amont pour tout le monde : refuser dans le garde-fou un record `AUTHORIZED` qui n'a pas été écrit par une transition de Project Control (par exemple une trace de création dans le record, vérifiée à l'audit) — ce qui est un chantier à part.

### C-07 — modéré — Sous l'option B, une décision oubliée ne se voit nulle part, et le sens de `null` n'a pas de valeur juste pour les deux populations

- **Situation / preuve** : S3.4 (précédent : `null` = règle pour tous, audit rouge) ; S3.1 (projet neuf : déclaration impossible avant la clôture) ; B10 (l'audit ne peut pas exiger la réponse, donc pas voir l'oubli) ; S3.2 (onze gestes, commit arbitraire accepté).
- **Conséquence** : `null` = tous éligibles trahit B7 dans un projet existant qui oublie ; `null` = personne éteint la règle dans tout projet neuf ; aucune répétition de montée ne peut le rattraper.
- **Correction suggérée** : si B est retenue, `null` = « aucune borne, rien d'ancien » (tous éligibles), et la clôture de l'initialisation ou la montée doit écrire la borne **mécaniquement** — ce qui n'est plus B, c'est D (§ 11).

### C-08 — modéré — « Chantier ouvert » n'est pas défini : créé, ou démarré ?

- **Objet** : E1 § 2.5 (« chantiers ouverts après l'adoption »), B7 (« repris »), option A (« marque chaque fiche qu'elle **crée** »).
- **Situation** : fiche créée avant la montée (S2.5 inversé : `WI-005` créé avant, démarré après) — A l'épargne, une lecture « démarré après » l'interroge.
- **Preuve** : lecture croisée de E1 et du § 5 du mandat ; l'état `AUTHORIZED` non démarré existe bien entre les deux (`start_head: UNKNOWN`, `t02-chrono.txt` `[après création — WI-005]`).
- **Correction suggérée** : une ligne dans E1 § 2.5 : « ouvert = créé (record présent) », ou « ouvert = démarré (premier Agent Run) » ; la première est la seule que A, B et D lisent sans Git.

### C-09 — modéré — La forme du champ laisse passer des réponses creuses et ne dit pas où vivent ses règles conditionnelles

- **Situation / preuve** : `t06-forme-du-champ.txt` S6.1 à S6.6 (blancs acceptés, dossier accepté comme chemin cherché, `FOUND` + `searched` accepté, `declared_at` forgeable, `if/oneOf/dependentRequired` refusés par le validateur).
- **Conséquence** : le refus « réponse incomplète » de E1 § 4 n'est pas spécifié assez pour être construit ni relu.
- **Correction suggérée** : la formulation du § 8 ci-dessus.

### C-10 — modéré — E1 ne dit pas par quel geste la réponse entre dans la fiche ; ce choix change B1-B5 et B10

- **Situation / preuve** : § 9 ; `t01-git.txt` S1.2 et `t02-chrono.txt` S2.1 (édition à la main acceptée par le garde-fou).
- **Correction suggérée** : trancher entre « à la création » et « commande dédiée avant le démarrage », et réécrire B10 et la colonne « Attendu » de B1-B5 en conséquence.

### C-11 — mineur — Chiffres de E2 à corriger

- 31 champs `required` et 33 propriétés (E2 : 30 et 32) ; 64 noms de contrôles distincts (E2 : 58) ; parseur `create-work-item` l. 6189-6228 (E2 : 6189-6226). Sans conséquence sur les conclusions. Preuve : `mesures_t01.txt` § B.2, B.6.

### Observations (sans situation démontrée, ne bloquent rien)

- **O-01** — `status_payload` et `preflight_findings` indexent les records directement ; une ligne B10 doit lire `prior_art` avec une valeur par défaut, sinon `status` casse sur tout record ancien.
- **O-02** — Montée interrompue puis relancée (T-02) : la transaction de `template-upgrade --apply` s'annule d'un bloc ; non rejouable par commande ; jugée sans effet sur A.
- **O-03** — Sous B et C, `status` devrait interroger Git pour chaque record (B10) ; coût et fragilité non mesurés.
- **O-04** — `WI-000`, fiche d'initialisation écrite à la main en Bootstrap Mode, ne portera jamais de marque sous A ; sans effet tant qu'elle ne passe pas par `start`.

---

## 11. Classement motivé des trois options — une recommandation, la décision appartient au Project Owner

**1. Option A — la marque voyage dans la fiche.** La seule des trois qui tient B7, B8, B9 et B10 tels quels, sans lecture de Git, sans décision par projet, sans distinction entre projet neuf et projet monté (§ 7.2). Sa frontière est unique et lue au même endroit par le démarrage et l'audit. Ses faiblesses sont nommées et bornées : la fiche recopiée à la main (C-06, un trou qui existe déjà pour tout le reste du contrôleur), la définition de « ouvert » (C-08, commune à toutes les options), et la nécessité d'une marque distincte de la réponse si celle-ci est écrite après la création (C-10). Elle demande au constructeur trois précautions : exclure les records de l'empreinte par construction (C-03), ne pas toucher à la liste `required` interne (C-05), lire la marque avec une valeur par défaut (O-01).

**2. Voie D — l'inventaire figé à la montée** (quatrième voie, apparue en cours de revue). Au moment où la nouvelle version arrive, le contrôleur écrit **une fois** dans l'état du projet la liste des fiches présentes (« nées avant ») ; tout ce qui n'y est pas est éligible ; un projet neuf a une liste vide. C'est le point 5 de E1 § 2 pris au pied de la lettre, sans décision humaine à écrire et sans lecture d'historique. **Démonstration** : la liste est un fichier, elle survit là où C se trompe — dans les copies S4.2, S4.3 et S4.4, `project_control/project-state.v1.json` est octet pour octet celui du projet d'origine tandis que la borne déduite y change ou disparaît (`t04-option-c.txt`) ; et elle juge la fiche de S2.1 par son absence de la liste, ce qui ferme C-06. **Ce qu'elle coûte** : une commande ou un moment d'écriture qui n'existe pas (la montée est exécutée par l'*ancien* contrôleur, qui ignore la règle — `project_control/README.md` l. 289-296 ; l'audit est en lecture seule), l'état du projet n'est pas un chemin administratif (S3.2 : refus sur la canonique), et la liste devrait entrer dans `BASELINE_CHANGE_MANDATED` (l. 4272-4325, qui ne connaît que deux champs) pour ne pas bouger en silence. Et elle ressemble beaucoup à « une seconde baseline à côté de la première », que E1 § 3 interdit d'inventer : c'est au Project Owner de dire si une liste mécanique, sans décision, tombe sous cette interdiction. Classée seconde pour cette raison, devant B parce qu'elle n'a ni le coût ni l'angle mort de la décision oubliée.

**3. Option B — la borne signée par décision.** Conforme à la doctrine en apparence, mais pas « sur le modèle exact » : le modèle existant exempte les chantiers clos et soumet les chantiers ouverts au contrat courant, l'inverse de B7 (C-04). Onze gestes par projet existant, impossible avant la clôture d'un projet neuf (S3.1), commit arbitraire accepté (S3.2), et surtout une décision oubliée invisible avec un `null` qui n'a pas de bonne valeur (C-07). À retenir seulement si le Project Owner veut que chaque projet **signe** sa frontière, et accepte d'écrire la règle d'exemption nouvelle et le sens de `null`.

**4. Option C — la borne déduite de l'historique.** À écarter : deux frontières dès l'histoire intacte, une frontière qui bouge ou disparaît sur quatre accidents ordinaires (C-02). E2 la donnait déjà comme la plus fragile ; la mesure confirme, et va plus loin : ce n'est pas fragile, c'est indéterminé.

**Quelle que soit l'option** : C-01 doit être corrigé (ou son effet assumé par écrit) pour que B7 soit une promesse testée et non un essai qui passe sur le cas simple ; C-08 et C-10 doivent être tranchés dans E1 avant la construction ; C-09 donne la formulation manquante de la forme du champ.

---

## 12. État final

| | |
|---|---|
| `source/` | **intact** : 125 fichiers avant et après ; liste d'empreintes identique, SHA-256 `6e97fe91388b93877bd1221eccecfb6320e5bdcbd53be4617541fac6d32eba03` (`runs/revue-2/preflight/source-hashes-avant.txt` = `…-apres.txt`, `cmp` sans différence) ; `diff -rq source runs/revue-2/copie-lecture` sans différence après les mesures |
| `entrees/`, `MANDAT-REVUE-P7-BORNE.md`, `LISEZ-MOI.md` | non modifiés (empreintes du § 2) |
| Créé sous `runs/revue-2/` | `README-REVUE-2.md` (marqué) ; `preflight/` (deux listes d'empreintes) ; `copie-lecture/` (copie de `source/`, identique) ; `outils/` (`atelier.py`, `mesures_t01.py`, `bac-a-sable/` : `outils_revue.py`, `s_t01.py`, `s_t02.py`, `s_t02b.py`, `s_t03.py`, `s_t04.py`, `s_t06.py`, `LISEZ-MOI.md`) ; `t01/` (`mesures_t01.txt`, plus une copie `hello-squelette/` arrêtée au premier commit par le verrou Git, laissée telle quelle) ; `transcriptions/` (`t01-git.txt`, `t02-chrono.txt`, `t02-contre-epreuve.txt`, `t03-option-b.txt`, `t04-option-c.txt`, `t06-forme-du-champ.txt`, `tests-3.19.1-sur-copie-sans-git.txt`, `chrono-reperes.json`) ; `_a_supprimer/` (un fichier d'essai vide et un record temporaire `WI-777.json` déplacés là faute de droit de suppression — à jeter avec le dossier) |
| Hors du dossier accordé | le bac à sable de session `$HOME/atelier-revue-2/` de la VM, sur double arrêt (§ 2) ; il disparaît avec la session ; rien n'a été poussé, tagué, ni lu ailleurs sur la machine |
| Non ouverts | `REVUE_P7_BORNE-1.md`, `runs/revue-1/` |
| Écrit à la racine | ce fichier, une fois |

---

## 13. Verdict

```
P7_BORNE_REVUE_REQUIRES_MAJOR_REDLINE
```

Le majeur est C-01 : la reprise par fusion d'un chantier bloqué est refusée par le contrôleur 3.19.1 dès qu'un autre chantier a été clos, ce qui rend B7 intestable sur son chemin réel, quelle que soit la borne choisie ; C-02 écarte l'option C. Les redlines modérées (C-03 à C-10) portent sur les entrées E1 et E2 et sur les précautions de construction ; aucune ne remet en cause les huit points fixés du § 4 du mandat. Le classement du § 11 est une recommandation : A, puis D si le Project Owner ne la tient pas pour une seconde baseline interdite, puis B, C écartée.
