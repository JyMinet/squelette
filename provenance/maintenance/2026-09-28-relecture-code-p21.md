> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Relecture du code P21 — Tableau des clés — 3.21.0

1. **Ce qui s’est passé.** La relecture du commit demandé a établi six constats : trois scénarios où le script efface du travail que l’original ne conserve pas durablement, et trois garanties non tenues concernant la lecture, le lieu d’exécution et les copies imbriquées. Les essais ont porté uniquement sur des copies fictives dans le dossier accordé.
2. **Ce que ça change.** La version ne peut pas être déclarée prête à livrer en l’état. Les protections de chemin, de guillemets et de dossier parent résistent aux scénarios rejoués ; les pertes démontrées viennent de l’inventaire et de la couverture des données, avant l’effacement.
3. **Ce que Jeoffrey doit faire.** Faire corriger les constats de la section B dans ce chantier, puis faire rejouer ces reproductions et la suite complète avant livraison. Aucun correctif, aucune livraison, aucune promotion ni aucun envoi n’a été effectué par cette relecture.

## A — Preflight et vérifications

Date : 2026-09-28. Mandat : `MANDAT-RELECTURE-CODE-P21.md`, lu avec `AGENTS.md`, le core qu’il désigne, `FIRST_START.md`, les rapports de construction et de mesure, la fiche V3, `TPL-D-080`, l’entrée de maintenance et la doctrine/guide de la branche relue. Les décisions 1 à 8 et les écarts assumés sont conservés comme données ; aucune nouvelle décision ni aucun Work Item réel n’a été créé.

**Périmètre :** `~/Projets/squelette-chantier-p21/`. Le dépôt préexistant et son `.git` sont restés en lecture seule. Travail et essais dans `revue-code/` ; livrable créé exclusivement à la racine. Les décisions, commits et preuves générés pour les essais sont fictifs et vivent uniquement dans leurs dépôts d’essai ; le marquage est « FIXTURE DE RELECTURE — FICTIF, N’AUTORISE RIEN ». Aucun commit du code relu.

| Vérification | Résultat |
|---|---|
| Branche demandée | `claude/p21-tableau-des-cles` |
| Commit relu | `0ecb5464fdd1e03534dbb32ffc1d487907e4da14` |
| Base `main` | `b9fe0e7bd91ab02a9cda967fdddd6c51b56d13c8` |
| SHA-256 `scripts/project_control.py` | `e07444e75e36174511e0e6f888e18f6b0e9d7c5ea756399f1881b950f7eef141` — conforme |
| SHA-256 `tests/test_template.py` | `1500f3c4cb1f3dd819eb440fbc88e2f9f68dc89f3550230385b43ec338173f06` — conforme |
| Python | `3.14.7` |
| Git | `2.50.1 (Apple Git-155)` |
| Livrable avant travail | Absent ; aucun fichier existant remplacé |
| Remote du dépôt accordé | Aucun |
| Suite complète | **211/211 tests distincts PASS**, après rejeu standard d’un test affecté par une erreur du lanceur de relecture ; détail ci-dessous |

Clone de relecture créé par la commande prescrite :

```sh
git clone --no-local --branch claude/p21-tableau-des-cles \
  ~/Projets/squelette-chantier-p21 revue-code/clone
```

Pour toutes les exécutions d’essais et sondes :

```sh
export TMPDIR=~/Projets/squelette-chantier-p21/revue-code/tmp
export PYTHONDONTWRITEBYTECODE=1
export GIT_OPTIONAL_LOCKS=0
```

La suite utilise les tests exacts de `revue-code/clone/tests/test_template.py`. Le lanceur de relecture maintient les temporaires dans le périmètre et suspend les scripts d’effacement pour lecture avant leur exécution. Exécution : 57 tests réussis en séquentiel, puis trois tranches disjointes de 52, 51 et 51 tests. Le premier test suspendu pour lecture de son script a été interrompu volontairement puis rejoué intégralement dans une tranche ; il ne compte qu’une fois. Les quatre scripts d’effacement effectivement lancés par la suite ont été lus avant exécution. Un seul résultat initial `ERROR` provenait du lanceur de tranches : import dynamique non inscrit dans `sys.modules`, alors que le test `test_the_suite_still_runs_from_a_derived_project_that_bound_its_volume` consulte `sys.modules[__name__]` à la ligne 3058. Son rejeu standard, depuis le clone, a donné `Ran 1 test in 4.428s; OK`, code 0 :

```sh
python3 -B -m unittest -v tests.test_template.GeneralProjectSkeletonTests.test_the_suite_still_runs_from_a_derived_project_that_bound_its_volume
```

La trace conserve les 210 PASS et l’ERROR initiaux, la cause du lanceur et ce rejeu réussi : `suite-211-results.json`, `suite-summary.log`, `retry-import-standard.log`. Aucun test manquant, doublon ou test ignoré dans le résultat final. Les journaux et le décompte nominatif sont dans `revue-code/regression/`. Aucun test ni code produit n’a été corrigé pour obtenir un résultat.

**Non-régression indépendante, en plus de la suite :** montée réelle d’un projet dérivé fictif extrait de la base 3.20.2 vers 3.21.0, avec plan, répétition et application ; audit, `status` et vue acceptés sans registre ; schéma nouveau ajouté ; worktrees de répétition retirés. Le refus initial du schéma non indexé a disparu après son indexation explicite dans la fixture. Export public exécuté avec un registre suivi contenant une sentinelle privée : registre et sentinelle absents de l’export, 25 fichiers core et manifeste identiques. Preuves : `revue-code/regression/c06-final.log`, `upgrade-dry-run.log`, `upgrade-apply.log`, `export.log`.

## B — Constats, reproductions et corrections proposées

Les lignes ci-dessous se rapportent au commit relu, donc aux fichiers de `revue-code/clone/`, et non aux fichiers de la branche `main` extraite à la racine. Les scripts de sondes conservent leur marquage fictif. Les commandes de reproduction partent de la racine accordée, avec l’environnement de la section A. Les scripts d’effacement ont été lus avant lancement et n’ont visé que des copies d’essai sous `revue-code/`.

### P21-R01 — BLOCKER — Un commit encore récupérable par le reflog disparaît de l’inventaire

**Code :** `scripts/project_control.py:1615–1618`, dans `clone_inventory`. **Périmètre : C-01, C-02, C-07.**

**Scénario.** Dans un clone fictif déclaré, créer et committer `unique.txt`, revenir au commit précédent avec `git reset --mixed`, puis retirer le fichier de l’arbre. Supprimer les anciennes entrées des reflogs de `HEAD` et `refs/heads/main` avec `git reflog delete`, sans `--rewrite`, en gardant l’entrée du retour arrière. Son ancien OID désigne toujours le commit unique. Git le retrouve par `git rev-list --reflog --not --all`, mais `git reflog show --all --format=%H` n’affiche que les nouveaux OID. L’intersection des deux listes écarte donc ce travail récupérable.

**Reproduction conservée :**

```sh
python3 -B revue-code/inventory/probe.py reflog
```

La sonde imprime toutes les commandes Git, la fixture et le script à lire. Pour rejouer aussi l’effacement : conserver sa sortie dans `revue-code/inventory/reflog.log`, lire intégralement le script indiqué, puis exécuter `python3 -B revue-code/inventory/erase_reviewed_fixture.py reflog`. Exécution observée : `revue-code/inventory/tmpeqr119ug/`. Le script `cleanup.sh` de cette fixture a ensuite été lu et exécuté avec `bash`.

**Preuve observée :**

```text
git rev-list --reflog --not --all
6f4b530aa62fa6cb59cc36eb055b1ff6b13df3bf
INVENTORY {"ref:refs/heads/main": "commit:02ba68b9f516a454d3a7f62fc068444595f7badf"}
REFUSALS []
copy return : RC 0, PROJECT_CONTROL: PASS (aucune preuve ni aucun abandon)
copy check : RC 0, COPY_CONTENT PASS, COPY_COVERAGE PASS
BEFORE_UNIQUE_IN_COPY RC 0
BEFORE_ABSENT_IN_ORIGINAL RC 1
CLEANUP RC 0
COPY_EXISTS_AFTER_CLEANUP False
AFTER_ABSENT_IN_ORIGINAL RC 1
```

Journaux : `revue-code/inventory/reflog.log`, `reflog-erasure.log`. La perte a été exécutée, pas seulement déduite. Le commit était encore récupérable par Git avant l’effacement ; la limite admise « les dossiers internes de Git sont lus comme Git les tient » ne justifie pas de le filtrer.

**Correction proposée.** Inventorier l’ensemble des commits que `rev-list --reflog --not --all` retourne, sans intersection avec les seules nouvelles cibles affichées par `reflog show`. Refuser aussi une erreur de cette commande au lieu d’utiliser sa sortie comme une liste vide. Ajouter un essai avec l’ancien OID seul dans l’entrée conservée ; retour sans preuve refusé, puis retour/effacement accepté seulement après conservation ou abandon explicite.

### P21-R02 — BLOCKER — L’origine d’un export n’est pas protégée contre la disparition de sa dernière branche

**Code :** `scripts/project_control.py:3319–3339`, `:1672–1698`, `:3365–3394`. **Périmètre : C-01, C-02, C-07.**

**Scénario.** Une branche fictive `export-data` porte un fichier unique `reports/unique-export.txt`. En faire un export déclaré, intact dans `source/`, puis `copy return`. Supprimer la branche `export-data` dans l’original. Le commit n’est plus joignable par une branche ou un tag ; il subsiste temporairement comme objet Git. L’export intact produit un inventaire vide. `copy check` peut encore lire son arbre avec `ls-tree` et annonce à tort que tout est conservé par une branche ou un tag.

**Reproduction conservée :**

```sh
python3 -B revue-code/inventory/probe.py export
```

Fixture observée : `revue-code/inventory/tmpulmtzam_/`. Pour rejouer toute la preuve, conserver la sortie dans `revue-code/inventory/export.log`, lire intégralement le script indiqué, puis lancer `python3 -B revue-code/inventory/erase_reviewed_fixture.py export`. Après lecture, son `cleanup.sh` a été exécuté. Un ménage Git a ensuite été effectué **uniquement dans l’original fictif** :

```sh
git -C revue-code/inventory/tmpulmtzam_/project reflog expire --expire=now --all
git -C revue-code/inventory/tmpulmtzam_/project prune --expire=now
```

**Preuve observée :**

```text
ORIGIN cd9b60056acccb080c6a3ff275d2a9a913325c55 KEPT? False
copy check : RC 0
PASS: COPY_CONTENT — the folder holds exactly what was returned
PASS: COPY_COVERAGE — everything it held is still kept by a branch or a tag ...
CLEANUP RC 0
COPY_EXISTS_AFTER_CLEANUP False
AFTER_ORIGIN_LOST : git cat-file -e <origin> RC 1
ORIGINAL_WORKTREE_UNIQUE_FILE_EXISTS False
```

Journaux : `revue-code/inventory/export.log`, `export-erasure.log`. L’objet existe encore au moment du contrôle ; le script supprime la dernière copie de fichiers protégée de ce ménage, puis expiration/purge achèvent la perte. Aucune écriture concurrente pendant l’effacement n’est nécessaire.

**Correction proposée.** Faire de la révision d’origine d’un export une obligation de couverture explicite, au retour et à chaque contrôle. Elle doit rester joignable par une branche ou un tag de l’original ; l’existence temporaire de l’objet ne suffit pas. Si son abandon est permis, il doit être nommé dans les preuves. Ajouter l’essai « origine couverte au retour, dernière branche supprimée avant contrôle ».

### P21-R03 — BLOCKER — Deux inventaires différents ont exactement la même sérialisation

**Code :** `scripts/project_control.py:1379–1388`, `:1701–1704`, `:3388–3389`. **Périmètre : C-01, C-02, C-03.**

**Scénario.** L’empreinte est calculée sur des lignes `nom<TAB>valeur<LF>` sans échappement. La valeur d’un lien symbolique contient sa cible littérale, qui peut elle-même contenir tabulations et retours à la ligne. Au retour, le clone contient seulement un lien `a` dont la cible vaut `cible-inexistante\nworktree:secret.txt\t<H>`, où `<H>` est le SHA-256 du futur fichier. Son inventaire est abandonné par le préfixe `worktree:`. Après le retour, remplacer cette cible par `cible-inexistante` et ajouter `secret.txt` avec les octets correspondant à `<H>`. Les deux dictionnaires sont différents, mais la chaîne passée à SHA-256 est identique. L’abandon par préfixe couvre alors aussi le fichier ajouté ; aucun nouveau retour n’est exigé.

**Reproduction conservée :**

```sh
python3 -B revue-code/registry/probe_digest.py
```

La sonde écrit `revue-code/registry/digest-latest.json` et imprime `SCRIPT_TO_READ`. Fixture observée : `revue-code/tmp/tmpxb2h_qe_/`. Son script a été lu intégralement, puis lancé avec `bash`. Aucune modification n’a eu lieu pendant ce lancement.

**Preuve observée :**

```text
DISTINCT_INVENTORIES True
DIGEST_BEFORE b79f29febb44287a96ebf1b65bb87a823272abb0ceb5343f82c72b2306f0b028
DIGEST_AFTER  b79f29febb44287a96ebf1b65bb87a823272abb0ceb5343f82c72b2306f0b028
copy check : RC 0, COPY_CONTENT PASS, COPY_COVERAGE PASS
UNRETURNED_BYTES_EXIST_BEFORE True
NOT_IN_ORIGINAL True
SCRIPT_RC 0
UNRETURNED_BYTES_EXIST_AFTER False
```

Journaux : `revue-code/registry/probe_digest.log`, `probe_digest-erasure.log`. Il s’agit d’une **collision de sérialisation**, pas d’une collision cryptographique. Le mécanisme doit détecter tout changement dans un dossier abandonné en bloc ; cette promesse est explicitement celle de l’empreinte, indépendamment du préfixe choisi.

**Correction proposée.** Hacher une représentation non ambiguë : par exemple un tableau de paires triées encodé en JSON canonique avec échappement ASCII, ou un encodage avec longueurs. Prévoir la transition des empreintes déjà enregistrées. Couvrir les noms et cibles de liens comportant tabulation, LF, CR et caractères non ASCII ; vérifier que le nouveau fichier force `COPY_CONTENT FAIL`.

### P21-R04 — MAJOR — Lire un clone partiel exécute encore une commande de sa configuration

**Code :** `scripts/project_control.py:1345–1355`, puis appel `ls-tree` à `:1619`. **Périmètre : C-01, C-05, C-07, C-08.**

**Scénario.** Une fixture déclare un dépôt partiel/promisor ; un objet arbre est absent. Sa configuration nomme un faux programme SSH local dans `core.sshCommand`. Ce programme écrit seulement un marqueur sous `revue-code/`, puis échoue : il ne tente aucune connexion. Lorsque `copy return` demande l’arbre, Git lance ce programme pour essayer de récupérer l’objet manquant. Désactiver `core.fsmonitor` n’empêche pas cette autre exécution.

**Reproduction conservée :**

```sh
python3 -B revue-code/inventory/probe_config.py
```

Fixture : `revue-code/inventory/tmpxc8hmvmm/`. Configurations utilisées : `extensions.partialClone=origin`, `remote.origin.promisor=true`, URL fictive `ssh://example.invalid/fiction`, `core.sshCommand=<fixture>/fake-ssh.sh`. Objet arbre retiré seulement dans la fixture.

**Preuve observée :**

```text
copy return : RC 1, PROJECT_CONTROL: FAIL
cannot read the copy (ls-tree HEAD): fatal: Could not read from remote repository.
CONFIG_EXECUTED True
MARKER FAKE SSH: no network operation
FAKE SSH: no network operation
```

Journal : `revue-code/inventory/config.log`. Le retour est finalement refusé, mais la commande configurée a déjà tourné deux fois et écrit un fichier hors du registre. Aucun trafic réseau réel ni perte de travail n’est revendiqué dans cette sonde. La doctrine (`AGENTS.core.md:342–348`) et le guide promettent une lecture sans exécution d’une commande nommée par la copie.

**Correction proposée.** Refuser les dépôts incomplets/promisor avant toute lecture susceptible de récupérer un objet, ou garantir techniquement l’interdiction de récupération paresseuse et de tout transport lors des lectures. Cette protection doit rester effective avec les versions Git supportées ; ne pas conserver une promesse universelle fondée sur le seul réglage `core.fsmonitor`. Ajouter un essai qui vérifie à la fois le refus d’objet absent et l’absence totale du marqueur d’exécution.

### P21-R05 — MAJOR — Un clone au registre hérité peut enregistrer une fausse clôture

**Code :** `scripts/project_control.py:3040–3051`, `:3396–3427`, `:3748–3774`. **Périmètre : C-04, C-05, C-07, C-08.**

**Scénario.** Un original fictif ouvre `COPY-001`. Un autre clone, sans fiche de sortie, hérite de son registre, qui indique pourtant explicitement le chemin du véritable original. Depuis ce clone, `copy close COPY-001 --state KEPT --decision TPL-D-990` est accepté et crée un commit. L’entrée du clone devient `KEPT` tandis que celle de l’original reste `OPEN`.

**Reproduction conservée :**

```sh
python3 -B revue-code/cleanup/probe_stray.py
```

Fixture : `revue-code/cleanup/stray-5rbgim7u/`. Journal : `revue-code/cleanup/probe_stray.log`.

```text
copy close : RC 0
PASS: TRANSACTION — KEPT by TPL-D-990
stray_commit_created: true
stray_state: KEPT
original_state: OPEN
original_register_unchanged: true
```

Le contrôle commun des mutations ne regarde que la fiche de sortie. `check` et `cleanup` utilisent en plus `origin.original_path` ; les mutations ne le font pas. La limitation admise « une copie sans fiche est indiscernable » ne s’applique pas à cette donnée déjà disponible dans le registre. La conséquence démontrée est un faux succès administratif, pas un effacement de l’original.

**Correction proposée.** Avant toute mutation d’un registre hérité, comparer la provenance des entrées au chemin déclaré de l’original, comme le font déjà `check` et `cleanup`, et refuser une entrée provenant d’un autre original. Étendre l’essai `test_copy_commands_run_in_the_original_and_nowhere_else` aux mutations dans le clone sans fiche : il ne vérifie actuellement que `check`/`cleanup` dans ce cas.

### P21-R06 — MAJOR — Une autre copie enregistrée sous `.git/hooks` ne déclenche pas le refus

**Code :** `scripts/project_control.py:1548–1557`, à comparer aux appels de `nested_slip_refusal` à `:1651` et `:1685`. **Périmètre : C-01, C-03, C-07, C-08.**

**Scénario.** Un premier original fictif ouvre son clone. Un second original fictif distinct ouvre réellement, par `copy open`, une autre copie dans `.git/hooks/project-chantier-p2` du premier clone. La seconde copie est clonée et reçoit la fiche produite par son propre original ; elle contient `unique.txt` et reste `OPEN` chez celui-ci. Le premier inventaire parcourt les hooks mais ne leur applique pas le détecteur de fiches imbriquées. Un abandon `git:hooks/project-chantier-p2/` permet de rendre la copie englobante, puis de faire accepter son effacement.

**Reproduction conservée :**

```sh
python3 -B revue-code/registry/probe_nested_registered.py
```

Fixture englobante : `revue-code/tmp/tmpz0ic3jiu/`. Second original : `revue-code/tmp/tmp6ud1vmnx/project/`. Contrairement à la première sonde exploratoire, ce scénario possède deux registres effectivement créés par les commandes publiques ; la fiche imbriquée n’est pas fabriquée à la main.

**Preuve observée :**

```text
INVENTORY_ITEMS 391 REFUSALS []
RETURN_RC 0 — PROJECT_CONTROL: PASS
CHECK_RC 0 — COPY_CONTENT PASS, COPY_COVERAGE PASS, COPY_FRONTIER PASS
SECOND_REGISTER_STATE OPEN
NESTED_UNIQUE_FILE_STILL_PRESENT True
```

Journal : `revue-code/registry/probe_nested_registered.log`. Aucun script d’effacement n’a été lancé dans ce scénario : la gravité retenue est `MAJOR`, pour le refus inconditionnel promis mais absent. La doctrine et le guide exigent de refuser une autre copie enregistrée à l’intérieur, même si un abandon en bloc est fourni.

**Correction proposée.** Appliquer la détection de fiches imbriquées à tous les parcours admis, y compris `hooks/`, `info/` et `branches/`, avant de rendre leurs fichiers abandonnables. Ajouter un essai avec deux originaux réels de fixture et vérifier que le refus demeure avec un abandon préfixé. Examiner également les chemins classés techniques sans les transformer silencieusement en refuges pour une copie imbriquée.


**Contrôles sans nouveau constat.** Les sondes de `revue-code/cleanup/probe_tags_unicode.py` ont vérifié un tag annoté : retour refusé quand il manque dans l’original, retour et contrôle acceptés après fetch exclusivement local, puis `COPY_COVERAGE FAIL` après retrait du tag. Trois fichiers aux noms Unicode (suivi modifié, non suivi, ignoré ; écritures NFC/NFD) sont inventoriés et empêchent le retour sans preuve ; journal `probe_tags_unicode.log`. Les sondes indépendantes ont aussi accepté un parent contenant apostrophe, espaces, `$HOME` littéral et `;`, sans exécuter ces caractères ; une table de correspondance hostile n’a pas détourné l’effacement. Un dossier étranger à la place de la copie est refusé avant parcours ; un remplacement après parcours est refusé par le second contrôle d’identité. Un parent remplacé par un lien après un véritable `copy check PASS` est refusé, avec conservation des deux dossiers. Les mutations depuis une branche de travail sont refusées ; un `copy check` en lecture seule sur cette branche lit correctement le registre de référence. Preuves : `revue-code/cleanup/prepare_cleanup.log`, `execute_cleanup.log`, `prepare_parent_probe.log`, `execute_parent_probe.log`.

**Limites de la relecture.** Aucun montage réel n’a été créé ou démonté ; l’essai de montage interne de la suite simule un changement de device. La fenêtre de concurrence déclarée entre contrôle et effacement n’est pas rediscutée. Les pertes R01–R03 n’en dépendent pas. Les choix de jeton, fichier JSON de preuves, déplacement sans comparaison de contenu, absence de bannière sans fiche et override pour la décision de garde restent ceux du mandat. Les contrôles ordinaires du registre, de réparation groupée, de schéma et du garde-fou sont couverts par la suite ; cela ne constitue pas une preuve générale d’absence de défaut hors scénarios.

## C — Les dix trous annoncés et les deux ajouts

`FERMÉ` signifie que le mécanisme annoncé existe dans le code et tient les scénarios indiqués ; cela ne signifie pas que toute la fonction est sûre. Les essais cités appartiennent à la suite complète exacte ; les sondes supplémentaires sont distinguées.

| Trou du rapport de construction | Verdict | Vérification et chemin restant |
|---|---|---|
| 1. Fichiers cachés par drapeaux d’index/cache de dates | **FERMÉ** | Parcours direct et comparaison des octets à l’arbre de HEAD ; essai `test_the_inventory_walks_the_folder_and_nothing_git_hides_escapes_it` (ligne 7505). R03 porte sur l’encodage de l’inventaire, pas sur ces drapeaux. |
| 2. Dépôt imbriqué comme gitlink / conflit | **FERMÉ** | Modes `160000` refusés dans arbre et index ; stages de conflit refusés ; essai ligne 7551. |
| 3. Couverture par référence de suivi/reflog, couverture réévaluée | **PARTIEL** | Branches/tags seuls et nouvelle validation des fichiers correctement ajoutés ; essais lignes 7593/7625. L’origine de l’export n’entre pas dans la couverture (R02) ; le travail du reflog peut manquer dès l’inventaire (R01). |
| 4. Commandes depuis copie au registre périmé | **PARTIEL** | Fiche bloquante ; `check` et `cleanup` vérifient aussi l’original. L’ancien accident d’effacement depuis copie est fermé, mais une mutation depuis clone sans fiche au registre hérité reste acceptée (R05). |
| 5. Table de correspondance détourne l’effacement | **FERMÉ** | Variable supprimée dans le script ; essai ligne 7688 et sonde indépendante avec voisin préservé. |
| 6. Saut de ligne dans un nom exécuté par le shell | **FERMÉ** | Validation entière des identifiants/noms/chemins, citations shell ; essai ligne 7688 et sondes caractères de contrôle/métacaractères. R03 concerne des données de liens internes, pas une injection shell. |
| 7. Montage interne, tube, dossier illisible | **FERMÉ** | Refus des devices différents, fichiers spéciaux et erreurs de parcours ; essai ligne 7740. Montage testé par simulation, pas par montage réel. |
| 8. Autre copie enregistrée à l’intérieur | **PARTIEL** | Détecteur présent dans le worktree et l’export, essai ligne 7740 ; absent du parcours des hooks. Deux originaux de fixture et deux copies réellement ouvertes reproduisent le passage indu (R06). |
| 9. `core.worktree` détourne la lecture | **FERMÉ** | Git reçoit explicitement `GIT_DIR` et `GIT_WORK_TREE`, avec environnement Git externe retiré ; essai ligne 7505. |
| 10. Place contrôlée seulement avant inventaire | **FERMÉ** | Contrôles avant et après ; essai ligne 7774 et sonde de remplacement après inventaire réel, refus d’identité observé. |
| Ajout 1. Exécution de `core.fsmonitor` | **FERMÉ** pour ce mécanisme | `-c core.fsmonitor=` neutralise cette commande ; essai ligne 7578. La garantie plus large « aucune commande configurée » reste violée par récupération d’objet d’un clone partiel (R04). |
| Ajout 2. Lien glissé plus haut dans le chemin | **FERMÉ** | Effacement depuis parent physique vérifié ; essai ligne 7804 et sonde avec véritable contrôle puis substitution du parent, script refusé et deux dossiers préservés. |

Couverture du mandat : C-01/R01, R03, R04, R06 et essais d’inventaire ; C-02/R01–R03, preuves de fichiers et références ; C-03/R03, R06 et sondes de chemin/parent ; C-04/R05 et refus de branche/copie ; C-05/R04–R05 et essais de registre/réparation/garde-fou ; C-06/montée et export indépendants, suite et vue ; C-07/table ci-dessus ; C-08/promesses précises confrontées aux constats B. Les deux écarts de doctrine supplémentaires démontrés, lecture sans commande configurée et refus de toute copie imbriquée, ne sont pas traités comme de simples problèmes de formulation.

## D — État du dossier en fin de mandat

- **Écritures : uniquement `revue-code/` et le présent livrable.** Aucun correctif, commit ou changement de branche dans le dépôt préexistant ; aucune suppression hors de `revue-code/` ; aucun accès aux autres dossiers de projets interdits, aucun envoi en ligne. Les commits, changements de branches, suppressions de références et purges décrits en B concernent exclusivement les fixtures.
- **Intégrité du préexistant :** comparaison SHA-256 et modes de 1 647 fichiers, `.git` compris, hors chemins d’écriture autorisés : zéro fichier modifié, ajouté ou retiré. Preuves : `revue-code/original-before.json`, `original-final-verification.json`, script de vérification `verify_original.py`. Les fichiers hors suivi présents à l’arrivée — mandat, deux rapports et `transfert/` — sont préservés.
- **Clone relu :** aucun écart de fichier suivi ; empreintes du contrôleur et des tests toujours conformes. Les sondes n’ont pas modifié les sources du clone.
- **Références originales :** commande de lecture finale, mêmes valeurs qu’à l’arrivée :

```sh
git -C ~/Projets/squelette-chantier-p21 rev-parse main claude/p21-tableau-des-cles
```

```text
b9fe0e7bd91ab02a9cda967fdddd6c51b56d13c8
0ecb5464fdd1e03534dbb32ffc1d487907e4da14
```

Le dépôt reste sur `main`, sans remote. `git status` a toujours été appelé avec `GIT_OPTIONAL_LOCKS=0` dans ce dépôt. Les deux seuls ajouts de la relecture à sa racine sont `revue-code/` et `RELECTURE_CODE_P21.md`. Le rapport a été créé en mode exclusif, sans remplacer de livrable existant. `revue-code/` reste jetable, à la disposition de Jeoffrey selon le mandat ; il n’a pas été nettoyé globalement.

## E — Verdict terminal

**CODE_P21_REQUIRES_MAJOR_REDLINE**

Trois constats `BLOCKER` démontrent une perte après autorisation d’effacement ; trois constats `MAJOR` démontrent des garanties écrites non tenues. Les 211 tests existants passent après le rejeu décrit en A ; les scénarios supplémentaires montrent les garanties qu’ils ne couvrent pas encore. Le verdict ne réouvre aucune décision du Project Owner : il demande que l’implémentation tienne les garanties retenues avant sa livraison.
