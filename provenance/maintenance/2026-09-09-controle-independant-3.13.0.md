> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Revue indépendante du squelette 3.13.0

Revue du 9 septembre 2026 — copie du tag `v3.13.0`, commit `ad95129206f3f31d3c7e7a80e9aa2e89ac6563d3`.

## 1. Résumé en trois points

1. **Le parcours nominal fonctionne et les 119 tests fournis passent.** La démonstration se rejoue en environ 14 secondes ; deux parcours complets, en français et en anglais, vont de l’initialisation à la clôture. Un petit projet préexistant, sans tests et avec un historique irrégulier, peut conserver son passé et obtenir son premier chantier autorisé.
2. **Deux garanties centrales restent incomplètes en utilisation standard.** Une création de chantier refusée à cause d’un `.gitignore` large laisse un index Git partiellement modifié, que le garde-fou accepte ensuite de committer. Par ailleurs, un commit antérieur à l’autorisation du chantier peut satisfaire sa preuve de développement et permettre `DONE`. Ces constats justifient des corrections majeures.
3. **L’adoption et la langue demandent aussi des précisions.** L’import d’un projet non gouverné n’est pas une procédure publiée complète et bloque si son code préexistant se trouve sous `modules/`. Le choix FR/EN fonctionne, mais un indicateur anglais inverse la couleur d’une sauvegarde à jour ; un ancien réglage et deux textes restent à aligner. Aucun de ces écarts linguistiques ne bloque le cycle anglais testé.

## 2. Méthode

### Périmètre et précautions

`source/` est resté le matériau de lecture. Les essais ont été exécutés dans des copies neuves sous `runs/`. Les réexécuteurs y placent aussi les répertoires temporaires, avec `TMPDIR` et Python `-B`. Aucun accès au dépôt original, aucune publication, aucun service externe ; la sauvegarde du scénario linguistique est un dépôt Git nu local dans `runs/`.

Les décisions, Work Items, conversations, exécutions et idées construits pour les essais sont explicitement marqués **JEU D’ESSAI — FICTIF, SANS VALEUR D’AUTORISATION** dans les fichiers ; les réexécuteurs utilisent la chaîne exacte du mandat avec apostrophes ASCII. La suite et la démonstration officielles ont également été rejouées sans modifier leurs fixtures fournies. Ces records restent dans `runs/` et ne valent aucune autorisation réelle.

**Standard** désigne ici l’opération étudiée avec `install-gate`, un core intact et les transitions administratives effectuées par le contrôleur. La préparation d’initialisation écrit les documents et records que FIRST_START demande précisément d’écrire, après preflight puis audit ; elle utilise pour la transition COMPLETE le mandat fictif d’override montré par la démo officielle. Cet amorçage est signalé, pas assimilé à une transition intégralement automatisée. Aucun override ni édition manuelle des records n’intervient dans les deux opérations standard défectueuses F-01 et F-02. Les greffes initiales non documentées, simulations de vieux records, lectures d’états fabriqués et récupérations manuelles sont explicitement qualifiées de **dégradées** ou de préparation hors procédure.

La revue antérieure a seulement été consultée pour identifier les dix-huit sujets à ne pas rouvrir. La suite de régression obligatoire les contient ; ils n’ont pas été transformés en nouvelles campagnes d’attaque. Les nouveaux essais portent sur les parcours du présent mandat.

### Environnement et contrôles de départ

Environnement : **macOS 26.6.2, arm64 ; Python 3.14.0 ; Git 2.50.1, Apple Git-155**. Les commandes de départ ont été exécutées dans `runs/initial/repo`, copie comprenant `.git`, et non dans `source/`, conformément à la règle « chaque essai dans une copie » :

```sh
cd ~/Projets/squelette-revue-2/runs/initial/repo
python3 -B scripts/project_control.py status
python3 -B scripts/project_control.py bootstrap-audit
TMPDIR=~/Projets/squelette-revue-2/runs/initial/tmp python3 -B -m unittest tests.test_template
```

Configuration du diagnostic initial : **dégradée**, sans garde-fou, telle que la copie du tag est fournie. La suite unitaire emploie ses propres fixtures et configurations ; son succès seul n’est jamais qualifié de preuve en configuration standard.

`status` et `bootstrap-audit` : **exit 0**, core aligné, mode bootstrap. La gate absente de la copie du tag est annoncée avec la commande d’installation ; les essais standard l’installent ensuite. Le HEAD détaché du tag n’a pas été pris pour la branche canonique d’un projet.

La suite obligatoire termine sans échec :

```text
Ran 119 tests in 478.079s

OK
EXIT: 0
```

Soit environ huit minutes, en parallèle des autres essais ; ce temps ne mesure pas la durée d’un parcours utilisateur. Aucun constat d’échec environnemental de la suite n’est donc retenu.

Les journaux de départ sont [status](~/Projets/squelette-revue-2/runs/initial/02.log), [bootstrap-audit](~/Projets/squelette-revue-2/runs/initial/03.log) et [suite complète](~/Projets/squelette-revue-2/runs/initial/04.log). Git a aussi émis deux avertissements macOS de cache/événements lors de sa première identification, avec exit 0 ; ils ne sont pas attribués au produit.

Contrôle final d’intégrité : **empreintes SHA-256 comparées pour 855 fichiers, `.git` compris : aucun contenu modifié, ajouté ou supprimé dans `source/`** entre le relevé initial et la fin des essais. Les dates d’accès ne sont pas comparées. [Preuve du contrôle](~/Projets/squelette-revue-2/runs/initial/source-integrity.json).

### Parcours d’adoption et coût observé

Les projets d’essai ont un code Python déjà committé, aucun test, des messages `ok`, `wip`, `hmm`, une branche abandonnée et des fichiers à la racine. Une variante conserve `*.json` dans son `.gitignore` ; une autre place une capacité existante dans `modules/legacy/existing.py`.

Point de portée essentiel : le README vise explicitement un **projet déjà initialisé avec une ancienne V3**, et Project Control parle d’un **historique de Work Items**. `legacy_baseline` n’est pas un importateur de tout historique Git. `ADOPTION.md` explique le choix du socle et des options, sans décrire la greffe sur un dépôt jusque-là non gouverné. Pour tenter cette greffe, il a donc fallu ajouter un geste non fourni : exporter le template en préservant les fichiers existants en collision, puis préparer l’entretien. Les résultats ne prouvent pas l’existence d’une procédure générale d’import.

| Parcours | Résultat observé | Ce qui est préservé / limite |
|---|---|---|
| Code historique `app.py`, pas de tests | Initialisation et premier WI utile autorisé ; audit PASS | Commits antérieurs encore ancêtres, contenu consultable par `git show`, branche abandonnée conservée |
| Même projet, ignore `*.json` | Refus du premier `create-work-item`, puis résidus d’index ; F-01 | Pas de réécriture du passé ; récupération ciblée réussie dans un essai séparé, annoncée dégradée |
| Code historique sous `modules/legacy/` | Blocage dès `bootstrap-audit` ; F-03 | Aucun fichier historique effacé ni déplacé pour « réussir » l’essai |
| Ancien WI DONE synthétique avec baseline explicite | Audit PASS, `LEGACY_PRESERVED`, octets conservés | Préparation dégradée ; contrôle de lisibilité du gel, pas migration réelle d’une ancienne version |

Le parcours réussi compte **15 commandes Git/contrôleur depuis l’import de gouvernance jusqu’au premier WI utile autorisé, en 3,191 secondes de parcours scripté**. Ce chiffre **n’est pas un temps d’adoption humain** : il exclut la fabrication du passé, la préparation du script, la lecture et les réponses d’un véritable propriétaire. Le chronomètre inclut les écritures automatisées de greffe, d’entretien et de transition ; le décompte des 15 commandes n’inclut pas ces trois lots d’écriture. Douze fichiers d’entretien sont préparés, puis six fichiers de transition. Le commit de clôture avec l’override documenté est déjà compris dans les 15 commandes. Les 15 commandes comprennent aussi un diagnostic volontaire de `template-upgrade`, refusé avant initialisation. La greffe, les collisions et les réponses sont déjà résolues par le script. Le temps honnête « je découvre le modèle → j’autorise mon premier chantier » n’a donc pas été mesuré auprès d’un novice ; aucun chiffre en minutes ne serait défendable ici. L’exécution est rapide, la préparation reste substantielle.

Preuves : [parcours réussi](~/Projets/squelette-revue-2/runs/adoption/root-history.log), [mesure](~/Projets/squelette-revue-2/runs/adoption/root-history.json), [lisibilité historique](~/Projets/squelette-revue-2/runs/adoption/legacy-readability.log).

### Première lecture et premier refus

Le premier écran du README donne bien la fonction, les destinataires et le problème traité : gouverner des projets menés avec des agents IA sur la durée, en gardant objectif, autorité, périmètre et preuves. Sa formulation n’exige pas de connaître déjà les formats internes. La version française arrive après la présentation anglaise, avec un lien dès le haut. **Aucun défaut de goût n’est retenu sur cette organisation.**

FIRST_START fournit un entretien par thèmes, des documents à produire et des conditions de clôture. Avec des réponses préétablies, les parcours FR/EN sont conduisibles. Ce n’est toutefois ni un questionnaire séquencé, ni une commande d’initialisation qui fabrique les premiers records : l’agent doit relier les réponses aux documents, compléter les structures et expliquer les choix. Les sujets « rôles », « owners » et « validations humaines » se recoupent sans être identiques ; « systèmes externes » et « dépendances » recouvrent plusieurs niveaux. Aucun n’est prouvé impossible à trancher pour un projet neuf : l’exemple minimal accepte des non-applicabilités explicites. En revanche, une architecture/Anti-Octopus encore UNKNOWN bloque effectivement la clôture ; elle ne doit pas être inventée pour la faire passer. Il n’y a pas eu d’entretien humain à l’aveugle, donc pas de conclusion sur son ergonomie en situation réelle.

Les refus relevés, en configuration standard sur un checkout neuf, montrent une orientation inégale :

| Commande | Sortie utile exacte, toutes exit 1 | Orientation |
|---|---|---|
| `preflight WI-001` avant initialisation | `FAIL: NORMAL_MODE — FIRST_START=NOT_STARTED; expected COMPLETE` ; `FAIL: WORK_ITEM_EXISTS — unknown Work Item: WI-001` | Décrit l’état, ne renvoie pas à une prochaine commande |
| `start WI-001` avant initialisation | `FAIL: TRANSACTION — start is available only after bootstrap COMPLETE` | Décrit le préalable, sans procédure de clôture |
| `bootstrap-preflight --path modules/app.py` | `FAIL: BOOTSTRAP_CHANGE_SCOPE — bootstrap-forbidden path: modules/app.py` | Chemin fautif précis, aucune étape suivante |
| `bootstrap-closeout --path FIRST_START.md --path project_control/project-state.v1.json` | `closeout requires a validated Project Charter with no owner TODO` ; `closeout requires the Project Owner's language (FR or EN) in project-state` | Livrables manquants explicites, mais une longue ligne agrège dix raisons |
| `start WI-001` autorisé, sans empreinte | ``FAIL: TRANSACTION — start requires --authorities-digest: run `context-manifest WI-001`, read every listed authority, then pass its MANIFEST_DIGEST`` | Prochaine commande et action de lecture explicites |

`status`, lu comme demandé par le README, donne bien « Initialiser le projet avec FIRST_START.md et valider le périmètre avec le propriétaire. » Ce filet d’orientation existe ; les messages de refus ne le rappellent pas tous. Ce relevé décrit une limite de guidage, sans la transformer en blocage du produit. [Journaux de première lecture](~/Projets/squelette-revue-2/runs/lecture/rejouer.py), notamment [premier preflight](~/Projets/squelette-revue-2/runs/lecture/06-preflight.log), [clôture prématurée](~/Projets/squelette-revue-2/runs/lecture/08-closeout.log).

L’exemple `hello-squelette` a été rejoué deux fois sur deux copies neuves : **13,781 s** pour le cycle et **14,549 s** pour `--check`, tous deux exit 0. Le second dit exactement :

```text
hello-squelette: TRANSCRIPT.md and the README block match the controller's output.
```

La promesse pratique « deux minutes » est tenue sur cet environnement, même pendant les travaux parallèles. Le temps de l’interview est simulé, pas mesuré. [Cycle](~/Projets/squelette-revue-2/runs/lecture/11-demo.log), [comparaison au README](~/Projets/squelette-revue-2/runs/lecture/12-demo-check.log).

### Lecture de doctrine et langues

Les énoncés comportementaux des quatre documents prescrits ont été regroupés par promesse pour éviter de compter plusieurs fois la même règle. La matrice en section 4 distingue essais neufs, tests fournis, lecture du code et obligations de l’agent que le contrôleur ne peut pas vérifier. Les résultats positifs d’un exemple ne sont pas étendus à toutes les combinaisons possibles.

Pour les langues : deux cycles standard complets FR/EN ; sauvegarde Git locale réelle dans chaque langue ; états complémentaires sur copies dégradées ; inventaire syntaxique de **233 paires FR/EN** (155 dans `SPEECH`, 78 dans `TEXT`), sans traduction ni paramètre de format manquant. La lecture des paires examinées n’a pas révélé d’autre changement substantiel de sens ; ce n’est pas une validation linguistique exhaustive de chaque contexte. Onze états de Work Item ont été inspectés en configuration dégradée pour leur présentation, sans prétendre avoir exécuté onze transitions autorisées.

## 3. Constats

### F-01 — Un `.gitignore` large laisse une transaction partielle que le hook accepte de committer

**Thèmes : T-A, T-C. Sévérité : MAJOR. Configuration : standard pour `create-work-item`, sa répétition et le commit ; import/amorçage préalables explicités en méthode.**

**Énoncé.** Le refus de `create-work-item` sur des nouveaux records ignorés restaure les fichiers mais pas l’index Git ; le hook accepte ensuite cet index, où la roadmap référence un Work Item absent.

Promesses concernées : création en une transaction, échec qui restaure les fichiers et commit soumis aux mêmes contrôles (`project_control/README.md`, cycle de travail ; `AGENTS.core.md`, Git Safety). Le cas est un incident d’adoption ordinaire, sans signal injecté ni montage manuel d’un index incohérent.

**Reproduction complète depuis le dossier accordé :**

```sh
TMPDIR="$PWD/runs/adoption/tmp" python3 -B runs/adoption/replay_adoption.py
```

Le script crée des dépôts neufs à chaque lancement. Dans `broad-ignore-commit`, l’ancien ignore `*.json` est conservé ; les JSON initiaux ont été importés explicitement, mais les futurs records restent ignorés. La commande complète de création — autorisation HD-002, chemin `app.py`, tests non applicables, intégration applicable — est dans le [journal exact](~/Projets/squelette-revue-2/runs/adoption/broad-ignore-commit.log). Extraits successifs :

```text
$ /opt/homebrew/opt/python@3.14/bin/python3.14 -B scripts/project_control.py create-work-item WI-001 --title 'Documenter app.py — JEU D'"'"'ESSAI — FICTIF, SANS VALEUR D'"'"'AUTORISATION' --objective 'Ajouter une docstring sans changer le comportement — JEU D'"'"'ESSAI — FICTIF, SANS VALEUR D'"'"'AUTORISATION' --owner 'Project Owner' --human-decision HD-002 --decision 'Autoriser uniquement la documentation dans app.py — JEU D'"'"'ESSAI — FICTIF, SANS VALEUR D'"'"'AUTORISATION' --authorized-by 'Project Owner' --branch work/wi-001-docstring --path app.py --conflict-gate INDEPENDENT --direct-impact app.py --indirect-impact NONE --authority-impact NONE --concurrent-work-impact NONE --code APPLICABLE --tests NOT_APPLICABLE --integration APPLICABLE --deployment NOT_APPLICABLE --runtime-proof NOT_APPLICABLE --runtime-target NOT_APPLICABLE --close-condition 'Docstring relue et branche intégrée'
FAIL: TRANSACTION — cannot stage records: The following paths are ignored by one of your .gitignore files:
project_control/conversations/CONV-WI-001.json
project_control/work-items/WI-001.json
hint: Use -f if you really want to add them.
[exit 1]

$ git status --short
MM docs/governance/HUMAN_DECISIONS.md
MM docs/governance/ROADMAP.md
MM docs/governance/WORKTREE_REGISTRY.md
MM docs/governance/git-path-classifications.v1.json
MM docs/governance/roadmap-state.v1.json
[exit 0]

$ python3 -B scripts/project_control.py pre-commit
PASS: STAGED_PATHS — 5 staged path(s)
PASS: MODE_AUDIT — audit PASS on the staged state
[exit 0]
```

La répétition exacte de `create-work-item` est refusée pour worktree sale. Pourtant, sans éditer ni ajouter aucun fichier, un vrai `git commit` des résidus passe avec la gate installée, **sans override**. Le commit résultant contient la roadmap WI-001, sans son record :

```text
$ git show HEAD:project_control/work-items/WI-001.json
fatal: path 'project_control/work-items/WI-001.json' does not exist in 'HEAD'
[exit 128]
```

Après réalignement explicite des cinq fichiers de travail sur ce commit, l’audit voit enfin :

```text
FAIL: WORKTREE_REGISTRY — registry entries without Work Item: ['WI-001']
FAIL: SCHEMA_VALIDATION — roadmap/record Work Item mismatch: roadmap=['WI-000', 'WI-001'] records=['WI-000']
[exit 1]
```

**Effet concret.** Le projet n’arrive pas à autoriser son premier chantier et peut enregistrer une gouvernance incohérente produite par le contrôleur lui-même. La récupération a réussi dans un essai indépendant par désindexation ciblée et exceptions d’ignore ; elle est manuelle et annoncée dégradée, donc ne répare pas la promesse transactionnelle.

**Cause corroborée par lecture :** `commit_records`, [contrôleur](~/Projets/squelette-revue-2/source/scripts/project_control.py:3579), peut recevoir un échec de `git add` après ajout partiel ; la restauration d’index ne couvre que l’échec ultérieur de `git commit`. Le hook audite ici le worktree restauré, malgré le texte « staged state ». **Correction proportionnée :** restaurer aussi l’index en cas d’échec de l’ajout et vérifier la cohérence de l’arbre effectivement committé ; anticiper les ignores sur les chemins administratifs créés.

### F-02 — Un commit antérieur au chantier satisfait sa preuve de développement

**Thème : T-C. Sévérité : MAJOR. Configuration : standard, gate installée ; aucun record de cycle retouché et aucun override à la clôture.**

**Énoncé.** `close` accepte le commit initial du dépôt, antérieur à l’autorisation et au démarrage, comme référence de code pour produire `DEVELOPED`, `DONE` et `STRUCTURED_VERIFIED`.

La DoD définit `DEVELOPED` par l’implémentation du scope autorisé, avec diff, revue de scope et version. Project Control promet de relier le travail autorisé à ses commits. Le problème observé est **le lien Git entre la preuve et le chantier**, pas la capacité du contrôleur à juger le sens du code.

**Reproduction, dans deux copies neuves :**

```sh
DOCTRINE_RUN_SUFFIX=-replay-1 python3 -B runs/doctrine/replay.py old-commit unintegrated-witness
```

Dans les deux cas, le contrôleur crée puis démarre un WI avec `code=APPLICABLE` et les autres gates `NOT_APPLICABLE`. Un fichier autorisé est réellement écrit, préflighté et committé sur sa branche. On revient sur `main`. Le témoin qui fournit le véritable commit du travail non intégré reçoit :

```text
FAIL: TRANSACTION — commit is not integrated in current HEAD: a7f3b238a31dd07a426ef65fcbc0c903754c94ec
[exit 1]
```

L’autre cas fournit le commit initial :

```text
$ python3 -B scripts/project_control.py close WI-001 --commit 2bdd39a853d51eeb18cac20a84b0325dd9744696
PASS: TRANSACTION — applicable evidence records and Git references validated; Work Item DONE
[exit 0]
```

Le record porte alors `development_status: DEVELOPED`, `status: DONE`, et ce seul ancien commit. `status --json` affiche `evidence_validation: STRUCTURED_VERIFIED` ; `audit` retourne PASS. Le commit métier `85ed429505b906525e8e01c6e0016ca9b1791074` n’est pas ancêtre du HEAD canonique : `git merge-base --is-ancestor … HEAD` retourne 1.

**Effet concret.** Un mauvais SHA copié depuis une ancienne baseline produit une clôture réussie et rompt la traçabilité du code de ce chantier. L’absence d’intégration de la branche n’est **pas** retenue comme défaut autonome : cette gate était expressément non applicable. Le contrôleur refuse bien le vrai commit non intégré ; il ne vérifie pas que le commit accepté appartient au travail autorisé.

**Cause corroborée par lecture :** [lignes de contrôle des commits](~/Projets/squelette-revue-2/source/scripts/project_control.py:4948) : existence et ascendance vers HEAD seulement ; [attribution DEVELOPED](~/Projets/squelette-revue-2/source/scripts/project_control.py:4986) dès qu’un commit existe. **Correction proportionnée :** exiger une référence reliée au chantier et à son démarrage, avec le périmètre Git correspondant, avant d’attribuer la gate code. Il n’est pas nécessaire d’imposer des tests ou une intégration à tous les WI.

[Journal du défaut](~/Projets/squelette-revue-2/runs/doctrine/C01-old-commit.log), [témoin refusé](~/Projets/squelette-revue-2/runs/doctrine/C04-unintegrated-witness.log).

### F-03 — L’adoption d’un dépôt non gouverné n’a pas de procédure complète et dépend de l’emplacement du code existant

**Thèmes : T-A, T-B. Sévérité : MINOR, limite de couverture et de documentation. Configuration : greffe initiale dégradée faute de procédure ; diagnostics suivants avec gate installée et core intact.**

**Énoncé.** Une greffe conservant du code historique à la racine aboutit, mais le même amorçage bloque sur du code déjà committé sous `modules/`, sans indiquer une voie d’adoption qui le conserve.

Reproduction : même réexécuteur d’adoption que F-01, scénario `legacy-modules`. `install-gate` passe ; worktree propre :

```text
$ python3 -B scripts/project_control.py bootstrap-audit
FAIL: NO_ACTIVE_BUSINESS_CAPABILITY — active paths: ['modules/legacy/existing.py']
[exit 1]

$ python3 -B scripts/project_control.py status
Erreur : NO_ACTIVE_BUSINESS_CAPABILITY: active paths: ['modules/legacy/existing.py']
Prochaine action : Corriger les erreurs d'audit avant toute écriture.
[exit 1]

$ python3 -B scripts/project_control.py template-upgrade --source ~/Projets/squelette-revue-2/source --apply
FAIL: APPLY — template-upgrade --apply requires NORMAL_MODE; a NOT_STARTED copy is replaced by a fresh copy of the template
[exit 1]
```

**Effet concret.** Un adoptant ne peut pas suivre FIRST_START tel quel sur ce dépôt et n’a pas d’instruction expliquant quoi conserver, classifier ou importer. `legacy_baseline` ne résout pas ce bootstrap : il concerne des Work Items historiques, pas une exemption générale du code préexistant. Le passé reste intact, mais l’adoption n’aboutit pas dans le parcours essayé.

**Limite du constat.** Ce n’est ni une régression prouvée de la mise à niveau entre anciennes V3, ni la preuve qu’aucune migration manuelle ne serait possible. Les documents publiés limitent déjà leur promesse aux projets gouvernés ; l’attente plus large du mandat dépasse cette couverture. La sévérité reste donc MINOR. **Correction proportionnée :** annoncer clairement ce prérequis dans le point d’entrée et fournir, si cette population est visée, un parcours d’import conservant le code existant. [Journal exact](~/Projets/squelette-revue-2/runs/adoption/legacy-modules.log).

### F-04 — La version anglaise marque en alerte une sauvegarde à jour

**Thème : T-D. Sévérité : MINOR. Configuration : standard, sauvegarde Git locale réelle.**

**Énoncé.** Une sauvegarde identique à la branche principale reçoit `ko` en EN et `ok` en FR, alors que son texte et son état Git sont équivalents.

Reproduction complète, suffixe neuf :

```sh
LANGUES_RUN_SUFFIX=-replay-1 python3 -B runs/langues/reproduce.py EN
LANGUES_RUN_SUFFIX=-replay-1 python3 -B runs/langues/reproduce.py FR
```

Chaque cycle crée ensuite un dépôt nu local, lui associe le remote `backup`, pousse `main`, puis lit `roadmap-view --json`. Le [journal anglais exact](~/Projets/squelette-revue-2/runs/langues/standard-en-v2/commands-exact.log) conserve les commandes et leurs sorties. Triples du bandeau :

```text
EN backup banner = ['Backups', 'identical (up to date)', 'ko']
EN audit = PASS
FR backup banner = ['Sauvegardes', 'identiques (à jour)', 'ok']
FR audit = PASS
```

La section des faits de la même vue anglaise affiche pourtant « The remote backups match the main branch (up to date). » avec `tone: good`. Le HTML utilise la classe d’alerte `ko` pour le premier indicateur.

**Effet concret.** Signal visuel contradictoire destiné au propriétaire ; pas de perte de sauvegarde ni de blocage. **Cause et correction :** [construction du bandeau](~/Projets/squelette-revue-2/source/scripts/project_control.py:2258) déduit la réussite du préfixe textuel français `identiques` ou anglais `The remote`, alors que le libellé traduit commence par `identical`. Utiliser l’état booléen indépendant de la langue. [Résultats EN](~/Projets/squelette-revue-2/runs/langues/EN-v2.log), [FR](~/Projets/squelette-revue-2/runs/langues/FR-v2.log).

### F-05 — Un réglage de langue encore proposé dans la doctrine est devenu sans effet

**Thèmes : T-C, T-D. Sévérité : MINOR. Configuration : établi par lecture, corroboré par essais dégradés.**

**Énoncé.** La consigne ROADMAP propose de modifier `roadmap-view.v1.json.language`, mais la vue suit exclusivement `project-state.v1.json.language`.

[La consigne](~/Projets/squelette-revue-2/source/docs/agent-governance/ROADMAP_VIEW.md:26) cite `language` parmi les réglages `RÉGLAGE :` ; [Project Control](~/Projets/squelette-revue-2/source/project_control/README.md:160) et le schéma continuent à l’exposer. Le test fait des copies neuves des cycles FR/EN, retire leur gate et édite le seul réglage de vue avant les lectures. Il n’est pas présenté comme une transition standard :

```sh
LANGUES_RUN_SUFFIX=-replay-1 python3 -B runs/langues/matrix.py EN
LANGUES_RUN_SUFFIX=-replay-1 python3 -B runs/langues/matrix.py FR
```

```text
project_language=EN, view_setting_language=fr -> rendered_language=EN, label=english (EN)
project_language=EN, view_setting_language=en -> rendered_language=EN, label=english (EN)
project_language=FR, view_setting_language=fr -> rendered_language=FR, label=français (FR)
project_language=FR, view_setting_language=en -> rendered_language=FR, label=français (FR)
```

**Effet concret.** Un agent suit une consigne valide, enregistre un choix, puis n’obtient aucun changement. Le choix principal dans Project State fonctionne exactement comme annoncé en 3.13.0. **Correction proportionnée :** retirer ou expliquer le réglage devenu désuet, sans réintroduire deux autorités de langue. [Matrice EN](~/Projets/squelette-revue-2/runs/langues/matrix-EN-v2.log), [FR](~/Projets/squelette-revue-2/runs/langues/matrix-FR-v2.log) ; cause : `roadmap_view_model` appelle `self.speech()`.

### F-06 — Une source ajoutée par le contrôleur reste en français dans la vue anglaise

**Thème : T-D. Sévérité : MINOR. Configuration : standard.**

**Énoncé.** Le repli technique de la roadmap anglaise affiche `(versions taguées du dépôt)`, prose produite par le contrôleur et non citation du propriétaire.

Le cycle EN de F-04 exécute réellement `roadmap-view --write`. Sa [vue Markdown enregistrée](~/Projets/squelette-revue-2/runs/langues/standard-en-v2/work/hello-squelette/docs/governance/ROADMAP_VIEW.md) contient :

```text
- `(versions taguées du dépôt)` sha256=`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
```

**Effet concret.** Le partage annoncé entre prose traduite et vocabulaire invariant n’est pas entièrement tenu. L’effet est limité au détail technique. [Cause](~/Projets/squelette-revue-2/source/scripts/project_control.py:107) : nom français codé en dur pour une source virtuelle. **Correction proportionnée :** conserver sa clé d’empreinte et traduire son libellé de présentation.

### F-07 — Le README annonce encore un contrôleur uniquement francophone

**Thèmes : T-B, T-D. Sévérité : MINOR. Configuration : établi par lecture ; contre-exemple standard.**

**Énoncé.** La présentation anglaise nie encore une capacité que la nouvelle version implémente et que sa propre démo montre.

[README, ligne 99](~/Projets/squelette-revue-2/source/README.md:99) :

```text
The controller speaks French for now; commands, records, schemas and reports are language-neutral.
```

Le cycle officiel rejoué dans `runs/lecture/11-demo.log`, comme le cycle EN annoté, affiche notamment :

```text
Project: Hello Squelette | NORMAL_MODE
Language: english (EN)
Next action: Project at rest; wait for an authorized objective.
```

**Effet concret.** Le lecteur anglophone reçoit une fausse limitation et peut renoncer à un outil qui convient déjà à son usage. **Correction proportionnée :** remplacer cette phrase par le périmètre réel FR/EN et la distinction avec les identifiants/refus invariants.

## 4. Ce qui tient

### Vérifications positives nouvelles

- **Démonstration reproductible :** changement réel, refus de dérive, deux tests du module, intégration et clôture ; le transcript et le bloc README correspondent au contrôleur. Le décompte `Work Items done: 2` inclut le WI d’initialisation : il ne signifie pas deux changements métier.
- **Deux langues utilisables de bout en bout :** initialisation, autorisation, preuve d’autorités, démarrage, refus de scope, preuves et `close` passent dans les cycles FR/EN. Les captures distinguent BOOTSTRAP, AUTHORIZED, IN_PROGRESS et DONE. Les noms de contrôles et les refus restent anglais dans les deux langues.
- **Mots du propriétaire préservés :** un titre/objectif/idée français demeure français dans le projet EN ; l’inverse est vérifié dans le projet FR. Quatre états d’idées ont été utilisés par commandes réelles ; les notes et sources sont conservées. La mention fictive française du mandat n’est donc pas une fuite de traduction.
- **Projet imparfait, passé conservé :** le cas réussi n’exige ni messages de commits propres, ni suppression d’une branche abandonnée, ni fabrication de tests historiques. Les exemptions d’un ancien DONE ne deviennent pas des preuves actuelles : le statut `LEGACY_PRESERVED` le distingue.
- **Niveaux runtime séparés :** un WI dont la preuve runtime contrôlée est applicable et le déploiement non applicable refuse `close` sans rapport, puis accepte une preuve structurée `RUNTIME_PROVEN`. Le déploiement reste `NOT_APPLICABLE`, sans promotion automatique en production. [Essai C02](~/Projets/squelette-revue-2/runs/doctrine/C02-runtime-levels.log). C’est une preuve de traitement du contrat, pas une expérimentation d’un service réel.
- **Vues et lecture seules :** `status`, `audit`, `roadmap-view` et son JSON ne modifient pas les fichiers suivis dans l’essai C03. `--write` committe la vue depuis la canonique ; un second appel sans changement conserve HEAD. [Essai C03](~/Projets/squelette-revue-2/runs/doctrine/C03-view-readonly.log).
- **Limites des preuves correctement exposées dans les références :** le core précise qu’un digest ne prouve ni lecture mentale ni compréhension ; la DoD et Project Control distinguent la cohérence des rapports de l’attestation indépendante d’une exécution. Les politiques runtime optionnelles ne sont pas présentées comme des protections réseau automatiquement installées.

Le README rend moins visibles que les références détaillées plusieurs capacités utiles vérifiées : blocage/reprise en conservant le passé, distinction des anciennes preuves, commits administratifs automatiques, mise à jour du core sans reprendre les records. Ce sont des atouts peu mis en avant, pas des défauts de goût. L’anglais disponible est, lui, un véritable contre-exemple documentaire, traité en F-07.

### Matrice des promesses des quatre documents

A = [AGENTS.core.md](~/Projets/squelette-revue-2/source/docs/agent-governance/AGENTS.core.md), V = [ROADMAP_VIEW.md](~/Projets/squelette-revue-2/source/docs/agent-governance/ROADMAP_VIEW.md), D = [DEFINITION_OF_DONE.md](~/Projets/squelette-revue-2/source/docs/governance/DEFINITION_OF_DONE.md), P = [project_control/README.md](~/Projets/squelette-revue-2/source/project_control/README.md).

Les **70 familles** dédoublonnent les énoncés répétés. Tous les noms `test_…` renvoient aux méthodes effectivement exécutées dans [tests/test_template.py](~/Projets/squelette-revue-2/source/tests/test_template.py), avec la commande et la sortie globale données en section 2. C01/C04 sont les deux cas de F-02 ; C02/C03 sont les essais positifs ci-dessus. C00 est un refus correct de chemins bootstrap trop larges conservé au [journal](~/Projets/squelette-revue-2/runs/doctrine/C00-bootstrap-prefix-refusal.log).

« Tenue (suite) » signifie tenue **dans les cas du test cité**, jamais preuve universelle. « Tenue (lecture) » désigne explicitement une conclusion de code sans nouvel essai. « Non vérifiée — doctrine » concerne la conduite de l’agent ou de l’humain et ne signifie ni échec ni protection mécanique. Les conclusions partielles signalent une limite observée ou de couverture. La matrice ne prétend pas être une preuve formelle mot par mot ; certains champs et combinaisons ne sont vérifiés que par lecture, comme indiqué.

| ID | Source et énoncé comportemental | Conclusion | Preuve ou limite précise |
|---|---|---|---|
| C-01 | A introduction, P core : AGENTS déclare une seule autorité core présente ; manifeste présent, bien formé, fichiers présents. | Tenue (suite) | `test_audit_requires_core_manifest_and_agents_core_reference`, `test_core_manifest_describes_the_tree_and_the_decided_core_set`. |
| C-02 | A introduction/Reuse : le core ne se modifie jamais directement dans un projet dérivé ; AGENTS ne peut que renforcer ; ambiguïté → arrêt humain. | Non vérifiée — doctrine | La même documentation précise qu'une modification locale n'est pas une erreur d'audit ; ne pas inventer une garantie d'interdiction absolue. |
| C-03 | A reprise, P se repérer : `status` est en lecture seule, affiche objectif/mode/branche/HEAD/manques/prochaine action/audit, code non nul si invalide, aucune autorisation nouvelle. | Partiellement tenue (essai/suite/lecture) | C03 ; `test_status_json_reports_project_and_next_action_without_writing`, `test_status_json_reports_invalid_state_with_failure_exit`. État, erreurs et prochaine action présents ; en texte, seuls les objectifs des WI non terminés sont affichés, pas l’objectif du Charter au repos. Lecture `status_payload` et transcript de démo. |
| C-04 | A modes : NOT_STARTED → bootstrap seulement, COMPLETE → normal seulement, statut absent/invalide/contradictoire → arrêt. | Tenue (suite) | `test_a_new_not_started_copy_passes_bootstrap_audit`, `test_g_bootstrap_is_refused_after_complete`, tests validation project-state. L'ensemble des chaînes malformées n'a pas été énuméré. |
| C-05 | A bootstrap : seuls chemins d'initialisation listés ; code métier, runtime/déploiement, core/tests/scripts/templates optionnels interdits ; non classé ou audit échoué interdit commit. | Tenue (suite/essai) | `test_b_charter_write_is_allowed_in_bootstrap_mode`, `test_c_business_module_write_is_refused_in_bootstrap_mode`, `test_hook_gates_bootstrap_commits_and_needs_a_mandate_for_core_paths` ; C00 et bootstrap C01–04. |
| C-06 | A bootstrap : lire autorités et Git, Impact Map et Conflict Gate avant chaque écriture ; maintenance core exige mandat/branche/manifeste. | Non vérifiée — doctrine | Contrôles du périmètre ne certifient ni lecture réelle préalable ni réalité d'une revue d'impact. |
| C-07 | A clôture : Charter, architecture, Anti-Octopus, HD, roadmap, premier WI, Conversation, audit, preuve closeout requis ; transition explicite conjointe FIRST_START/Project State. | Tenue (suite/essai) | `test_f_closeout_requires_complete_deliverables`, `test_g_bootstrap_is_refused_after_complete` ; closeout C01–04. Les documents validés sont déclaratifs, conformément au modèle. |
| C-08 | A clôture : après COMPLETE toutes commandes bootstrap refusées, pas de retour silencieux à NOT_STARTED. | Tenue (suite) | `test_g_bootstrap_is_refused_after_complete`, validation de la transition dans `initialization_state_errors`. Le retour par intervention hors modèle n'est pas présenté comme impossible. |
| C-09 | A/P : autorisation humaine déjà donnée couvre conséquences administratives ordinaires ; ne pas redemander une autorisation par geste. | Non vérifiée — doctrine | La politique de conversation de l'agent n'est pas un résultat de CLI. |
| C-10 | A/P cycle : create exige HD existante valide ou texte explicite ; synchronise Work Item, Conversation, roadmap, registre et classification en transaction. | Partiellement tenue — F-01 | Création nominale réussie C01–04 et tests `test_p_create_work_item_breaks_preflight_creation_circularity`, `test_v_failed_creation_writes_no_administrative_consequence` ; le nouvel essai d’adoption montre une indexation partielle non restaurée après échec. L’atomicité universelle n’est pas tenue. |
| C-11 | A/P : transitions create/start/block/resume/close sur checkout canonique à son tip, propre ; records auto-committés ; branche WI refuse records administratifs. | Tenue (suite/essai) | `test_records_live_on_canonical_branch_only` ; commits et commandes C01–04. Les règles de préparation manuelle du bootstrap sont une exception documentée. |
| C-12 | A/P : un merge d'intégration ne peut pas conflicter sur les records exclusivement canoniques. | Tenue (suite dans ce périmètre) | `test_records_live_on_canonical_branch_only`, `test_resume_aligns_diverged_branch_by_merge_and_closes`. Pas une promesse sur des records modifiés hors commandes et hors gate. |
| C-13 | A/P : `context-manifest` lit autorités de base + scopes des chemins ; hash fichier + digest trié ; --scope étend lecture sans changer digest requis pour WI seul ; records cycliques exclus, HD incluse ; autorité absente est erreur. | Tenue (suite/lecture) | `test_context_manifest_is_deterministic_and_follows_the_work_item_scopes` ; lecture `authority_manifest` et `require_authorities_digest`. Les six catégories de scope sont celles de la doc. |
| C-14 | A/P : start/resume refusent digest absent ou différent sans afficher l'empreinte attendue ; l'Agent Run stocke liste/scopes/SHA/HEAD/date. | Tenue (suite/essai) | `test_start_and_resume_require_the_current_authorities_digest` ; C01/C02/C04 refus sans digest puis start accepté. |
| C-15 | A/P : preuve présente/complète/courante exigée ; autorité changée → preflight FAIL, status STALE, close FAIL ; nouvelle lecture sur canonique committe l'acknowledgment. | Tenue (suite) | `test_changed_authority_blocks_preflight_and_close_until_reacknowledged`. |
| C-16 | A/P : l'autorité incluse dans le scope autorisé ne périme pas la propre preuve du WI. | Tenue (suite) | `test_an_authority_the_work_item_is_authorized_to_write_does_not_stale_its_own_proof`. |
| C-17 | A/P : le digest ne prouve ni lecture ni compréhension ; pas d'affirmation plus forte. | Tenue (lecture) | Limite explicite A lignes 142–149 et P preuves ; ne pas reconduire ancien F-18. |
| C-18 | A/P : start conserve base_head, capture start_head, exige ascendance, canonique non divergente et branche nouvelle ou exactement à start_head, puis crée/avance la branche. | Tenue (suite) | `test_start_uses_committed_authorization_head_and_keeps_provenance`, `test_start_refuses_noncanonical_current_branch_without_mutation`, `test_start_refuses_base_outside_canonical_ancestry`, `test_start_refuses_preexisting_branch_at_another_tip`. |
| C-19 | A/P : IN_PROGRESS seulement après preflight complet avant/après checkout ; erreur restaure branche et commit de records. | Tenue (suite) | `test_start_rolls_back_its_records_commit_when_the_branch_preflight_fails`, `test_u_failed_start_rolls_back_branch_and_lifecycle_state`. |
| C-20 | A/P : WI autorisé, HD/Conversation/branche/base/start/scope/applicabilité/runtime et dépendances DONE requis ; écritures sur bonne branche, statut actif et chemins autorisés. | Tenue (suite) | `test_foundation_02_normal_mode_without_active_work_item_refuses_business_write`, `test_foundation_03_active_preflight_allows_business_write_in_work_item_scope`, `test_foundation_04_active_preflight_refuses_business_write_outside_work_item_scope`, `test_i_authorized_normal_work_item_passes_preflight`. |
| C-21 | A/P blocage : seulement AUTHORIZED ou IN_PROGRESS, nouvelle HD, dépendance externe/reason/condition, block record, clôture run BLOCKED, statut/registre BLOCKED commit. | Tenue (suite) | `test_block_resume_01_block_closes_active_or_partial_run_without_faking_runtime`, `test_block_resume_02_authorized_block_uses_separate_optional_external_history`, `test_block_resume_03_block_requires_new_existing_linked_human_decision`, `test_block_resume_04_block_requires_reason_code_and_resume_condition_atomically`. |
| C-22 | A/P blocage : historique preuves et FAILED inchangés, commits métier préservés, autre chantier possible. | Tenue (suite) | `test_block_resume_05_blocked_work_item_does_not_prevent_another_start`, `test_resume_requires_current_execution_evidence_and_preserves_failed_report`. |
| C-23 | A/P reprise : BLOCKED obligatoire, nouvelle HD et condition exacte, champ AUTHORIZE/action/WI unique, canonique propre ; record résolu conservé. | Tenue (suite) | `test_block_resume_06_resume_rejects_a_non_blocked_work_item_atomically`, `test_block_resume_07_resume_requires_new_existing_linked_human_decision`, `test_block_resume_17_duplicate_conflicting_lifecycle_field_is_refused`. |
| C-24 | A/P reprise : base_head et premier start_head conservés, nouveau run propre start_head, alignement FF ou merge sans réécriture ; conflit métier refusé et merge annulé ; rollback Git/records. | Tenue (suite) | `test_block_resume_08_resume_fast_forwards_branch_and_preserves_history`, `test_resume_aligns_diverged_branch_by_merge_and_closes`, `test_resume_refuses_business_conflict_and_restores_git_state`, `test_block_resume_13_resume_restores_git_when_file_rollback_raises`. |
| C-25 | A/P : aucune branche WI absente ou remaniée ne doit perdre le travail d'un run lors d'une reprise ; blocage avant premier run possible. | Tenue (suite) | `test_block_resume_12_resume_branch_absence_depends_on_prior_start`, `test_block_resume_15_resume_rejects_branch_that_lost_agent_run_commit`, `test_block_resume_16_authorized_resume_accepts_only_absent_or_canonical_tip_branch`. |
| C-26 | A Impact Map : quatre impacts documentés ; Conflict Gate INDEPENDENT/DEPENDENT/OVERLAPPING/CONFLICTING ; dépendances/résolution avant travail. | Partiellement tenue | Champs et valeurs/présence contrôlés (`validate_work_item`, tests create/start) ; pertinence des impacts et résolution substantielle restent doctrine. |
| C-27 | A reuse/Anti-Octopus : chercher existant, pas duplication silencieuse ; shared technique, orchestrateur limité, échanges par contrat, ownership ambigu → arrêt. | Non vérifiée — doctrine | Pas d'analyse sémantique du métier par le contrôleur ; aucun cas ne justifie un constat de défaut mécanique. |
| C-28 | A branches : baseline canonique unique, un WI/branche, max un candidat actif, registre synchronisé, repos à zéro actif, BLOCKED non actif. | Tenue (suite) | `test_custom_canonical_branch_allows_main_as_work_branch`, `test_records_live_on_canonical_branch_only`, `test_s_normal_mode_at_rest_accepts_only_done_work_items`, `test_block_resume_05_blocked_work_item_does_not_prevent_another_start`. Courte durée des worktrees : doctrine non chronométrée. |
| C-29 | A Git Safety : interdiction add global, reset hard, clean/force, préserver préexistant ; tout changement suivi/ignoré/classé. | Partiellement tenue | Traçabilité et gate vérifient l'état ; le terminal peut exécuter des commandes interdites. La CLI contrôleur n'appelle pas de git add global/push/force (lecture). Il ne faut pas présenter la gate comme interception de toutes les commandes du terminal. |
| C-30 | A/P gate : installation externe copie versionnée ; audit refuse divergence et signale absence ; hook audite changements indexés et non indexés, scope de WI et canonique ; mandat explicite visible ; merge d'intégration admis. | Partiellement tenue — F-01 | Installations C01–04 et tests de gate réussis. La divergence de copie est refusée ; l’absence est signalée avec install-gate, pas systématiquement refusée par audit. F-01 montre que l’audit du worktree restauré ne garantit pas la cohérence du contenu indexé qui sera committé. |
| C-31 | A gate : renommage deux côtés, tous chemins indexés sous authorized_paths, exactement un IN_PROGRESS ; retrait référence ne retire pas copie, ancien hooksPath signalé, suppression terminal détectée. | Tenue (suite) | `test_a_rename_out_of_the_authorized_scope_is_refused`, `test_commit_gate_applies_the_work_item_scope_to_every_staged_path`, `test_the_gate_survives_the_removal_of_its_versioned_reference`, `test_removing_the_commit_gate_cannot_stay_unnoticed`. Ancienne revue, non requalifiée en nouvelle. |
| C-32 | A double arrêt/P : deux confirmations distinctes et Folder scope exigés pour décisions hors dossier ; règle s'applique au dépôt cible ; NOT_APPLICABLE en interne. | Tenue (suite) pour la trace ; doctrine pour l'expérience humaine | `test_out_of_folder_decision_requires_two_distinct_confirmations`, `test_work_item_backed_by_an_out_of_folder_decision_fails_preflight_until_confirmed`. Ne prouve pas que l'humain a réellement répondu deux fois. |
| C-33 | A style/P état : TECHNICAL/PLAIN choisi par PO, UNKNOWN avant choix, requis closeout, affiché en tête de status ; autre style ponctuel ne modifie pas record. | Tenue (suite) | `test_reporting_style_is_chosen_by_the_project_owner_and_shown_first_by_status` ; C03. |
| C-34 | A style : PLAIN en prose, résumé trois points, détail en rapport, demander précisément permission ; changement style sur décision, jamais initiative agent. | Non vérifiée — doctrine | La documentation déclare elle-même que la fidélité conversationnelle relève de l'agent. |
| C-35 | A langue/P état : FR/EN, UNKNOWN avant question, langue requise au closeout, prose status et roadmap traduite, identifiants/refus non traduits, mots PO conservés. | Partiellement tenue — F-04 et F-06 | Tests langue de la suite et deux cycles standard FR/EN réussis, mots PO conservés et refus anglais. Indicateur backup EN incorrect et libellé français de source virtuelle reproduits. Aucun blocage du cycle anglais observé. |
| C-36 | A autorité : promotion, activation, canonicalisation, cutover, irréversibilité, conflit architecture, risque accepté exigent humain ; UNKNOWN reste UNKNOWN. | Non vérifiée — doctrine | Pas de commandes génériques pour toutes ces actions ; présence d'une HD ne certifie pas une décision humaine réelle. |
| C-37 | D/P : cinq applicabilités séparées, N/A explicite ; UNKNOWN interdit preflight et DONE. | Tenue (suite) | `test_done_with_unknown_applicability_is_refused`, `test_o_done_without_applicable_evidence_is_refused`, validation create ; C01/C02 utilisent des choix explicites. |
| C-38 | D/P/A : cible N/A → runtime N/A ; cible contrôlée/production → preuve runtime obligatoire, deployment indépendant ; déploiement sans preuve refusé. | Tenue (essai/suite) | C02 ; `test_runtime_target_requires_runtime_proof_but_deployment_stays_separate`. |
| C-39 | D/P : TESTED distinct INTEGRATED ; contrôlé = DEPLOYED_IN_CONTROLLED_ENVIRONMENT/RUNTIME_PROVEN ; production = DEPLOYED/PRODUCTION_VERIFIED ; pas d'escalade implicite. | Tenue (essai/suite) | C02 ; `test_controlled_runtime_closes_without_claiming_production`, `test_production_rejects_controlled_runtime_level`, `test_production_requires_and_accepts_explicit_production_evidence`. |
| C-40 | D : QUALIFIED et CANONICAL ont exigences propres, close ne les attribue pas ; tests seuls ne prouvent pas runtime ou production. | Tenue (lecture/suite) | `test_definition_of_done_keeps_levels_distinct` vérifie des textes ; lecture de `close_work_item` confirme absence d'attribution de ces niveaux ; C02 séparation observée. |
| C-41 | D DEVELOPED/P cycle : le développement clos est lié aux commits de son scope autorisé. | Partiellement tenue — F-02 | C01 et témoin C04 : existence/ascendance HEAD des commits contrôlées ; commit antérieur au chantier accepté pour DEVELOPED. Écart structurel, sans demander une validation sémantique du programme. |
| C-42 | D niveaux TESTED/INTEGRATED/runtime : descriptions de résultats réels, environnements, compatibilité consumers, rollback et sign-offs quand requis. | Non vérifiée — doctrine sur la réalité ; tenue sur structure | La doc exclut expressément une attestation indépendante de l'exécution. Aucun déploiement réel ni audit humain de consumers/rollback dans cette revue. |
| C-43 | P/D preuves : chaque gate applicable exige rapport JSON local et artefacts ; simple texte, absent, FAIL, niveau/cible/WI incohérents refusés. | Tenue (essai/suite) | C02 refus puis acceptation ; `test_close_refuses_nonexistent_evidence_and_preserves_lifecycle`, `test_close_rejects_failed_or_mismatched_evidence`, tests production ci-dessus. |
| C-44 | P preuves : schéma fermé/version, gates/results/niveaux, SHA40, date passée avec fuseau, résumé non vide, artefacts non vides path/SHA256. | Tenue (lecture), partiellement couverte par suite | `validate_evidence` et `core_schema_errors` : les branches date/résumé/champ supplémentaire ne sont pas toutes isolées par un nouveau cas ici. Ne pas annoncer couverture exhaustive des valeurs invalides. |
| C-45 | P preuves : dossier reports/evidence/WI ajouté automatiquement aux authorized_paths ; chemins relatifs dans ce dossier. | Tenue (suite/essai) | `test_create_work_item_authorizes_its_evidence_directory` ; C01/C02/C04 montrent ajout systématique, C02 commet ses rapports avec gate. |
| C-46 | P preuves : rapport/artefacts suivis et identiques à HEAD, hash exact ; close_head conservé pour audit ; subject entre start et baseline, aucun changement métier ultérieur. | Tenue (suite) | `test_close_rejects_uncommitted_report_and_artifact_changes`, `test_close_rejects_evidence_predating_a_business_change`, validation de `subject_commit`. |
| C-47 | P/A : reprise exige nouvelles preuves à partir du start_head du dernier run ; FAIL historique conservé, dernière preuve retenue PASS ; rapports immuables dès premier commit, correction nouveau chemin. | Tenue (suite) | `test_resume_requires_current_execution_evidence_and_preserves_failed_report`, `test_close_keeps_failed_history_before_a_later_successful_revision`, `test_close_refuses_recommitted_historical_failure_even_with_corrected_hashes`, `test_evidence_immutability_detects_rewrite_through_merge`. |
| C-48 | P close : branche intégrée quand gate integration applicable, commits déclarés ancêtres HEAD, clôture run SUCCEEDED, DONE et records committés, historiques preuves append. | Tenue dans le périmètre conditionnel | C02/C04 ; `test_close_requires_declared_canonical_branch_for_integration`, `test_t_end_to_end_two_work_items_and_two_idle_audits`. Formulation absolue « après intégration » à lire avec l'applicabilité déclarée. |
| C-49 | A « Seul close peut produire DONE ». | Partiellement tenue — exception bootstrap | Toutes les transitions normales essayées utilisent close ; l’exemple officiel complete_initialization écrit WI-000 DONE directement au bootstrap. La formule « seul close » n’explicite pas cette exception ; aucun nouveau contournement mécanique ni sévérité autonome n’en est déduit. |
| C-50 | V/P/A : vue générée depuis sources projet, jamais inventée/réécrite manuellement ; forme stable avec bandeau/stats/versions/maintenant/attentes/suite/loin/idées/chantiers/passé/technique/réglages. | Tenue (suite/essai) | `test_roadmap_view_is_generated_from_the_files_in_a_stable_sourced_form`, C03. Interdiction de réécriture manuelle = consigne ; `roadmap-view` ne certifie pas tous les éditeurs externes. |
| C-51 | V/P : PLAIN ne crée pas de chemins/commits/empreintes/commandes hors technique, citations PO intactes ; TECHNICAL les affiche ; --style ponctuel sans mutation style projet. | Tenue (suite dans ses cas) | `test_plain_style_adds_no_path_of_its_own_outside_the_technical_block`, `test_roadmap_view_of_a_project_is_committed_by_project_control_only_when_its_sources_change`. Ancien F-14 non rejoué comme attaque nouvelle. |
| C-52 | V/P : chaque ligne cite sa source ; inconnu/non vérifié si absent ; aucune valeur complétée. | Partiellement vérifiée | C03 et test de forme vérifient les sources centrales ; pas de preuve exhaustive de chaque ligne sous toutes les combinaisons de données. Formulation « chaque ligne » exige plus que nos échantillons. |
| C-53 | V/P : sources_digest fichiers et versions taguées ; HEAD/remotes exclus volontairement ; status à jour/périmée/absente ; vue périmée ne fait jamais échouer audit. | Tenue (suite/essai) | C03 idempotence ; `test_a_new_version_tag_makes_the_generated_view_stale`, test de vue générée. Ancien F-11 non réémis. |
| C-54 | V/P : --write HTML non suivi et Markdown committé ; choix autres chemins internes par --html/--markdown ; style forcé ponctuel ; regénération sans source modifiée ne crée pas commit sans fin. | Tenue (essai/suite) | C03 ; `test_roadmap_view_of_a_project_is_committed_by_project_control_only_when_its_sources_change`. Variantes arbitraires de chemins de sortie non essayées. |
| C-55 | V/P : style/zoom/language/regeneration/mirrors paramètres ; cadence affichée mais pas planifiée par contrôleur. | Partiellement tenue — F-05 ; reste partiellement vérifié | Cadence affichée et absence de planificateur établies par lecture. Le réglage language de la vue reste documenté mais ne commande plus sa langue (F-05). Toutes les combinaisons zoom/miroirs n’ont pas été essayées. |
| C-56 | V/P : rôles séparés : template lit provenance/roadmap-template et produit sous provenance ; projet dérivé ne lit pas ce contenu de template. | Tenue (suite/essai) | `test_roadmap_view_is_generated_from_the_files_in_a_stable_sourced_form` et C03 ; lecture de `repository_role`, `view_paths`, `load_template_roadmap`. |
| C-57 | V : la vue rapporte audit/bootstrap-audit mais n'exécute jamais tests ; peut compter essais sans déclarer leur succès. | Tenue (suite/lecture) | `test_the_view_never_claims_that_tests_passed` et lecture de roadmap model ; ancien F-12 non rejoué en nouvel adversarial. |
| C-58 | V/P/A idées : mots du PO, date/source/état fermé ; add/set synchronisent JSON/Markdown, canonique propre et auto-commit en normal, écriture sans commit bootstrap. | Tenue (suite) | `test_ideas_are_recorded_in_the_owners_words_in_two_synchronized_committed_forms`. Conservation typographique exacte de tout Unicode/multiligne non exhaustive. |
| C-59 | V/P : unicité idées, liste états, cibles WI existant roadmap/HD enregistrée ; DISCARDED doit nommer cible décision ; enregistrer idée n'autorise rien. | Tenue (suite dans ses cas), limite doctrinale | Même test des idées ; ancien F-15 exclu des nouvelles attaques. La réalité humaine de la décision n'est pas certifiée. |
| C-60 | V/A : idée enregistrée dans même session, ne disparaît que réalisée/écartée ; jamais oubli. | Non vérifiée — doctrine | Agent et historique conversationnel hors contrôleur ; aucune commande de suppression d'idée dans CLI (lecture), pas preuve d'impossibilité d'édition externe. |
| C-61 | V discussion : tout message régénère ; exceptions RÉGLAGE/STOP ; autres demandes renvoyées ; aucune commande Git/décision/WI/mandat/permission hors vue. | Non vérifiée — doctrine | V « Limites » dit explicitement convention et non serrure. Aucune session interactive d'agent ROADMAP ni miroir hébergé créée pour cet essai. |
| C-62 | V discussion : miroir republié même URL, sources relues à chaque fois ; inaccessible → dernier état connu marqué non vérifié depuis date, jamais supposer. | Non vérifiée — doctrine | Cache conversationnel, hébergement et accès externe non exercés ; pas d'API qui prétend les automatiser. |
| C-63 | P/A/D legacy : baseline commit réel ancêtre HEAD avec décision ; aucun HEAD implicite ; DONE anciens conservés mêmes octets et chemins, affichés LEGACY_PRESERVED, autres preuves gardées en préfixe. | Tenue dans les cas testés | `test_legacy_baseline_freezes_history_and_requires_new_proof_forward`, `test_legacy_baseline_must_be_declared_by_a_recorded_decision_in_current_history` ; essai neuf de lisibilité LEGACY_PRESERVED, préparation dégradée explicitée. Pas de migration complète d’une ancienne release exécutée dans cette revue. |
| C-64 | P/A : anciens runs legacy/authorities baselines exemptés, nouveaux doivent porter preuve ; baseline valide figée, absent/divergent/sans décision refusé, NOT_STARTED ne déclare pas authorities baseline. | Tenue (suite) | `test_agent_runs_before_the_adoption_baseline_are_exempt_from_the_proof_of_reading`, `test_authorities_baseline_exempts_agent_runs_recorded_before_the_proof_of_reading` ; anciennes régressions gel de run suite seulement. |
| C-65 | P legacy : WI non clos à baseline suit nouveau contrat, pas exemption par numéro/champ absent ; ancien record sans block_records valide sauf BLOCKED. | Tenue (suite/lecture) | Tests legacy ; `validate_work_item` et `validate_block_records`. Aucun nouvel essai d'anciens numéros individuels. |
| C-66 | P schémas : validateur stdlib exécute sous-ensemble déclaré, mot-clé inconnu refusé, n'affirme pas tout JSON Schema ; identifiants provider-agnostic et affichage clé facultative. | Tenue (suite/lecture) | `test_schema_rejects_invalid_version_and_null_required_text`, `test_provider_agnostic_conversation_and_agent_records`, `test_j_arbitrary_project_key_builds_display_reference`, `test_k_absent_project_key_uses_internal_reference`, lecture `core_schema_errors`. |
| C-67 | P/A core : manifeste SHA/version, FIRST_START normalisé ; status drift modified/missing, drift seul pas erreur audit ; core-manifest --write réservé template. | Tenue (suite) | `test_core_manifest_describes_the_tree_and_the_decided_core_set`, `test_core_manifest_write_is_reserved_to_the_template`, `test_audit_requires_core_manifest_and_agents_core_reference`. |
| C-68 | P/A upgrade : compare états IDENTICAL/UPDATED/ADDED/REMOVED_UPSTREAM/MODIFIED_LOCALLY ; rapport sans écriture, refus écraser local sans overwrite, supprimés amont jamais effacés. | Tenue dans les cas de la suite | `test_template_upgrade_reports_no_drift_on_a_fresh_copy_and_refuses_bootstrap_apply`, `test_template_upgrade_updates_intact_core_refuses_modified_files_and_never_touches_records`. L’adoption d’un dépôt non gouverné n’est pas équivalente à un upgrade du core (F-03). |
| C-69 | P upgrade : apply normal uniquement, pas downgrade, droits exécutables/initialization conservés, manifeste source installé/vérifié, rollback, records intouchés ; WI scope/preflight/trace/gate s'appliquent. | Tenue dans les cas de la suite ; limites précisées | Tests upgrade précédents ; l’essai d’adoption confirme le refus de apply en bootstrap, sans fichier core modifié. Pas de nouvelle migration réelle depuis une ancienne release et pas de démonstration d’atomicité universelle de toutes les pannes. |
| C-70 | P transactions : mutations uniquement admin explicites, erreur restaure fichiers/Git approprié ; pas ajout global/push/force/travail métier. | Partiellement tenue — F-01 | Les tests de rollback fournis passent et le contrôleur n’ajoute pas globalement ni ne pousse le travail (lecture). F-01 est un contre-exemple standard à la restauration transactionnelle Git lors d’un échec partiel de git add. |

Les garanties de qualité métier, compréhension d’une autorité, sincérité d’une validation humaine, temporalité d’une conversation et réalité d’un runtime restent distinctes des garanties structurelles vérifiées. Aucune expérience de production, de miroir hébergé ou d’agent interactif soumis à la convention ROADMAP n’a été menée. Aucune extension de périmètre n’a été inférée pour les tester.


## 5. Verdict

Deux constats MAJOR sont reproduits avec gate installée, indépendamment de toute modification manuelle des records du cycle. Les parcours réussis et la suite fournie n’annulent pas ces contre-exemples. Les cinq autres constats sont limités à l’adoption non documentée, à la présentation et à la cohérence documentaire ; aucun BLOCKER n’est établi dans le périmètre de cette revue.

SQUELETTE_3.13.0_REVUE_REQUIRES_MAJOR_REDLINE
