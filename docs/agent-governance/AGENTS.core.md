# AGENTS.core.md — Autorité opérationnelle des agents (core du squelette)

Portée : tout le dépôt. Ce document est le core commun à tous les projets dérivés du squelette : il est versionné par `provenance/core-manifest.v1.json` et mis à jour par `template-upgrade`, jamais édité dans un projet dérivé. `AGENTS.md`, à la racine, appartient au projet : il inclut ce core et peut le renforcer, jamais l’affaiblir. Autorité ambiguë ou contradictoire : `STOP` et décision humaine.

## Reprise et charge administrative

Après lecture de FIRST_START, utiliser `python3 -B scripts/project_control.py status`
pour retrouver l’objectif, l’état et la prochaine action. Cette vue est en lecture
seule ; elle ne remplace ni les autorités applicables ni le preflight.

L’agent tient à jour les records nécessaires et utilise les commandes de
synchronisation existantes. Une autorisation humaine déjà donnée couvre les étapes
ordinaires dans son périmètre. Demander une nouvelle décision seulement lorsqu’un
nouveau périmètre, risque ou enjeu d’autorité l’exige, notamment les gates humains
énumérés ci-dessous. Ne pas créer de suivi parallèle ni demander une validation
pour chaque opération administrative déjà autorisée.

## Sélection fail-closed du mode

Lire `FIRST_START.md` avant toute écriture.

- `INITIALIZATION_STATUS: NOT_STARTED` → `BOOTSTRAP_MODE` uniquement ;
- `INITIALIZATION_STATUS: COMPLETE` → `NORMAL_MODE` uniquement ;
- statut absent, contradictoire ou invalide → `STOP`.

Bootstrap Mode n’est ni un contournement ni un preflight normal assoupli. C’est le preflight limité de l’initialisation. Une maintenance du core du template n’est jamais autorisée par Bootstrap Mode : elle exige un mandat humain explicite, une branche dédiée et les contrôles du dépôt source, et elle régénère le manifeste du core (`core-manifest --write --version`).

## Preflight Bootstrap Mode

Avant toute écriture d’initialisation :

1. lire les autorités routées par `docs/agent-governance/mandatory-documents.v1.json` ;
2. inspecter `git status --short --branch`, la branche et `git rev-parse HEAD` ;
3. produire l’Impact Map et appliquer le Conflict Gate ;
4. déclarer chaque chemin prévu avec :

```bash
python3 -B scripts/project_control.py bootstrap-preflight \
  --path docs/governance/PROJECT_CHARTER.md
```

5. ne modifier que les chemins acceptés ;
6. relancer `bootstrap-audit` après les écritures et avant commit.

Allowlist : FIRST_START, identité/README, Charter, Human Decisions, roadmap humaine et machine, repository/storage/migration/worktree policies, architecture initiale, ADR initiaux, Project State, records Work Item, Conversation et Agent Run, provenance nécessaire.

Interdit en Bootstrap Mode : code de domaine, modules ou applications actifs, shared code, contrats de domaine actifs, données/runtime, déploiement, activation, dépendance externe, scripts/core du contrôleur, tests/core du template et templates optionnels.

Un chemin absent de l’allowlist est refusé. Une modification bootstrap non classée ou un `bootstrap-audit` en échec interdit le commit.

## Clôture FIRST_START

Avant `NOT_STARTED → COMPLETE`, exécuter :

```bash
python3 -B scripts/project_control.py bootstrap-closeout \
  --path FIRST_START.md \
  --path project_control/project-state.v1.json
```

La clôture requiert Charter, architecture et Anti-Octopus Review validés, Human Decision enregistrée, roadmap synchronisée, premier Work Item autorisé, Conversation référencée, audit valide et preuve de closeout dans Project State. Le changement de statut est explicite, conjoint dans FIRST_START et Project State, puis versionné dans Git.

Après `COMPLETE`, toute commande bootstrap est refusée. Aucun retour silencieux à `NOT_STARTED` n’est autorisé.

## Preflight Normal Mode

Une décision humaine explicite autorise `create-work-item` à exécuter en une seule
transaction ses conséquences administratives : Human Decision si nouvelle,
Work Item, Conversation, roadmap, registre de branche et classification des
records générés. Ces écritures administratives ne sont pas du travail métier et
ne demandent aucune exception humaine supplémentaire.

Les records administratifs vivent sur la **branche canonique uniquement**. Les
transitions `create-work-item`, `start`, `block`, `resume` et `close` s’exécutent
depuis son checkout, à son tip, sur un worktree propre, et **committent elles-mêmes
leurs records** (message `chore(project-control): <transition> WI-NNN`). Une décision
humaine rédigée à la main est committée avant la transition qui la consomme. La
branche d’un Work Item ne porte jamais de changement administratif : `preflight` et
le hook de commit le refusent (`WORK_BRANCH_RECORDS_READ_ONLY`). Un merge
d’intégration ne peut donc pas conflicter sur un record, et l’unicité du chantier
actif se vérifie depuis la canonique.

Avant toute écriture métier :

1. inspecter Git ;
2. créer le Work Item autorisé avec `create-work-item` ;
3. obtenir la liste des autorités du Work Item et leur empreinte :

```bash
python3 -B scripts/project_control.py context-manifest WI-NNN
```

4. lire réellement chaque autorité listée, dans la version affichée ;
5. présenter la preuve de lecture au démarrage :

```bash
python3 -B scripts/project_control.py start WI-NNN --authorities-digest <MANIFEST_DIGEST>
```

6. vérifier le preflight et déclarer au besoin les chemins prévus avec :

```bash
python3 -B scripts/project_control.py preflight WI-NNN --path <path>
```

### Preuve de lecture des autorités

Les autorités d’un Work Item sont les documents de base routés par
`docs/agent-governance/mandatory-documents.v1.json` plus ceux des scopes que ses
`authorized_paths` touchent (`development`, `contracts`, `data`, `governance`,
`architecture`, `runtime`, déduits des préfixes de chemin). `context-manifest` en
calcule l’empreinte SHA-256 fichier par fichier, puis une empreinte globale,
`MANIFEST_DIGEST`. `--scope` élargit la lecture à un scope sans préfixe propre
(`security`, `recovery`) ou jugé applicable ; l’empreinte exigée par `start` reste
celle du Work Item seul, telle que `context-manifest WI-NNN` l’affiche sans `--scope`.
Les records tenus par Project Control lui-même (roadmap, registre de branches,
classifications, Project State) n’en font pas partie : ils changent à chaque
transition sans porter d’autorité nouvelle. `HUMAN_DECISIONS.md` en fait partie : une
décision enregistrée est une autorité. Quand le registre a été coupé en deux volumes
(voir plus bas), c’est le **carnet vivant** qui est routé, sommaire compris ; le volume
relié ne l’est pas et n’entre donc dans aucune empreinte.

`start` et `resume` refusent sans `--authorities-digest` égal à l’empreinte courante,
et ne l’affichent jamais : l’agent la présente après avoir lu, le contrôleur ne la
fournit pas. L’Agent Run créé enregistre `authorities_read` — empreinte, liste des
fichiers et de leurs SHA-256, scopes, HEAD, horodatage — comme preuve versionnée.
Le preflight vérifie ensuite `AUTHORITY_MANIFEST_PRESENT`, `_COMPLETE` et `_CURRENT` ;
une autorité modifiée depuis la lecture (Charter amendé, nouvelle décision, ADR
accepté) met le preflight en échec, `status` signale `authorities: STALE`, et `close`
refuse (`AUTHORITY_MANIFEST_AT_CLOSE`). Une autorité que le Work Item est lui-même
autorisé à écrire (`authorized_paths`) fait exception : l’agent en est l’auteur sous
autorisation, ses propres écritures ne périment pas sa preuve. Le travail reprend
seulement après une nouvelle lecture, enregistrée depuis la canonique :

```bash
python3 -B scripts/project_control.py acknowledge-authorities WI-NNN --authorities-digest <MANIFEST_DIGEST>
```

Depuis la branche d’un Work Item, cela signifie : committer le travail en cours,
revenir sur la canonique, `acknowledge-authorities`, puis réaligner la branche sur la
canonique (fast-forward ou merge, comme `resume` le fait) ; à la clôture, l’agent est
déjà sur la canonique.

**Portée exacte de cette preuve, à ne pas dépasser en la présentant.** Elle établit que
le travail a démarré depuis le texte courant de chaque autorité, et qu’une modification
ultérieure de l’une d’elles invalide la preuve jusqu’à une nouvelle lecture enregistrée.
Elle n’établit pas qu’un agent a compris, ni même qu’il a lu : un agent peut appeler
`context-manifest` et reprendre l’empreinte sans lire une ligne. Ce que la mécanique
ferme, c’est la dérive silencieuse — travailler sur une version périmée des règles, ou
prétendre après coup les avoir eues sous les yeux. Aucun document du squelette, aucune
vitrine, ne doit promettre davantage.

Un Agent Run antérieur à la baseline d’adoption (`legacy_baseline`) est exempt, de même
qu’un Agent Run présent à la baseline de preuve de lecture (`authorities_baseline` dans
Project State, déclarée par décision humaine quand un projet adopte la preuve de lecture
avec des Agent Runs déjà enregistrés : l’histoire est figée à ce commit, jamais
reconstruite) ; tout
Agent Run postérieur sans `authorities_read` met l’audit en échec.

`base_head` conserve la baseline contre laquelle le Work Item a été autorisé.
`start` doit être lancé depuis la branche canonique déclarée : il capture son HEAD
courant dans `start_head`, exige que `base_head` en soit un ancêtre (égalité admise),
écrit et committe les records du démarrage sur la canonique, puis crée la branche
déclarée depuis ce commit — ou avance par fast-forward une branche préexistante
située à `start_head`. Il ne réécrit jamais `base_head`. Une ascendance invalide, une
branche canonique divergente ou une branche WI préexistante à un autre tip est
refusée.

`start` ne passe le Work Item à `IN_PROGRESS` qu’après le preflight complet, vérifié
sur la canonique avant le commit puis sur la branche après le checkout. Le Work Item
doit être autorisé, relié à une Human Decision et une Conversation, porter sa
branche/base/start/scope, déclarer l’applicabilité de chaque gate et son
`runtime_target`, et avoir toutes ses dépendances `DONE`. Un échec restaure la
branche, annule le commit de records et interdit l’écriture métier. Une écriture
métier exige ensuite cette branche, ce statut et un chemin inclus dans
`authorized_paths`.

`block` s’exécute depuis la canonique, accepte un Work Item `AUTHORIZED` ou
`IN_PROGRESS` et une nouvelle Human Decision. Il enregistre une dépendance externe,
un `reason_code` et une condition explicite de reprise ; il passe le Work Item et le
registre à `BLOCKED`, clôt l’Agent Run courant avec `result=BLOCKED` s’il existe, et
committe ces records. Les preuves et leurs statuts, y compris `FAILED`, restent
inchangés ; le travail déjà committé sur la branche du Work Item reste en place.
`BLOCKED` est non actif : un autre Work Item peut démarrer.

`resume` exige un Work Item `BLOCKED`, une nouvelle décision confirmant exactement
la condition de reprise et un checkout propre sur la branche canonique déclarée.
Il résout le block record sans le supprimer, conserve `base_head` et le
`start_head` initial du Work Item, crée un nouvel Agent Run avec son propre
`start_head` (le HEAD canonique au moment de la reprise) et committe ces records
sur la canonique. La branche est ensuite alignée sur le tip canonique sans
réécriture d’histoire : fast-forward si elle est en retard, sinon commit de merge
de la canonique dans la branche. Un conflit métier annule le merge et refuse la
reprise ; rebase, cherry-pick et perte d’un commit historique restent exclus. Un
échec restaure les records, annule le commit de records et l’état Git de la
transaction.

Les décisions de transition contiennent une seule occurrence de `Chosen option:
AUTHORIZE`, `Related Work Item: WI-NNN` et `Project Control action: BLOCK` ou
`RESUME`. Le blocage porte aussi `Block reason code` et `Resume condition recorded` ;
la reprise porte `Resume condition confirmed`, avec la condition exacte. Voir les
[commandes et champs](project_control/README.md#blocage-et-reprise).

### Langue

Le Project Owner choisit aussi la **langue** dans laquelle le contrôleur s’adresse à lui — `FR` ou `EN`, enregistrée dans `language` (Project State), demandée par l’interview `FIRST_START` au même titre que le style de retour, `UNKNOWN` tant qu’elle n’a pas été posée, et exigée pour clore l’initialisation. Elle gouverne la **prose destinée à un humain** : `status` et la vue roadmap. Elle ne gouverne pas les noms de vérifications (`PASS: CORE_ALIGNED`), les lignes de rapport ni les messages de refus : ce sont des identifiants d’un vocabulaire fermé, sur lesquels s’appuient la suite de tests, la gate de commit et tout outil qui lit la sortie — les traduire les rendrait instables. La vue montre en outre les mots du Project Owner **tels qu’il les a écrits** : elle ne les traduit jamais. En changer plus tard est une décision humaine, comme pour le style de retour.

## Impact Map obligatoire

Chaque Work Item documente :

- `DIRECT IMPACT` : chemins, contrats et comportements modifiés ;
- `INDIRECT IMPACT` : consommateurs, données éventuelles, opérateurs et recovery affectés ;
- `AUTHORITY IMPACT` : Charter, architecture, roadmap, ADR, Human Decisions ou contrats touchés ;
- `CONCURRENT WORK IMPACT` : branches, worktrees et modifications préexistantes pouvant interagir.

## Conflict Gate

- `INDEPENDENT` → continuer dans le scope autorisé ;
- `DEPENDENT` → documenter et vérifier les dépendances ;
- `OVERLAPPING` → résolution explicite avant implémentation ;
- `CONFLICTING` → `STOP` et décision humaine.

## Reuse Policy

`REUSE > ADAPT > REIMPLEMENT`

Rechercher l’existant avant de créer script, schéma, contrat, ADR, service ou composant transversal. Aucune duplication silencieuse.

Les fichiers core du squelette (listés par `provenance/core-manifest.v1.json`) ne se modifient pas dans un projet dérivé : une amélioration générique remonte au template, puis revient par `template-upgrade`. `status` signale tout écart local ; `template-upgrade` refuse d’écraser un fichier core modifié sans décision explicite.

## Discipline branches et worktrees

- `ONE_CANONICAL_BASELINE`
- `ONE_WORK_ITEM_ONE_BRANCH`
- `MAX_ACTIVE_INTEGRATION_CANDIDATES = 1`
- `SHORT_LIVED_WORKTREES`

Chaque branche déclarée et worktree actif est inscrit dans
`docs/governance/WORKTREE_REGISTRY.md`. Ne pas développer directement sur la
branche canonique sauf autorisation humaine explicite. Ne pas mélanger plusieurs
Work Items dans un commit. Un projet en `NORMAL_MODE` peut rester au repos avec
zéro Work Item `AUTHORIZED` ou `IN_PROGRESS`.
Un Work Item `BLOCKED` est non actif et reste reprenable avec sa provenance.

## Git Safety et traçabilité

Interdit : `git add .`, `git add -A`, `git reset --hard`, `git clean`, force push et nettoyage global d’un checkout. Ajouter uniquement des chemins explicites. Préserver les modifications préexistantes. Tout chemin changé doit être suivi, ignoré intentionnellement ou explicitement classé.

Ces règles sont rendues mécaniques par la gate de commit, installée une fois par checkout
avec `python3 -B scripts/project_control.py install-gate` : la commande copie le fichier
versionné `scripts/hooks/pre-commit` **hors de l’arbre de travail**, là où Git l’exécute.
Le fichier versionné reste la référence — il voyage avec le template, `template-upgrade`
le met à jour, et `install-gate` se relance après chaque montée de version pour que la
copie lui reste identique ; `status` dit d’où la gate s’exécute et l’audit refuse une copie
qui diverge de sa référence. Avant chaque commit, il exécute l’audit du mode courant sur
le worktree — `bootstrap-audit` en Bootstrap Mode, `audit` en Normal Mode, donc
allowlist d’initialisation, chemins autorisés du Work Item actif et traçabilité, sur
tout changement présent, indexé ou non — et, en Normal Mode, refuse sur la branche
canonique tout chemin indexé autre que records administratifs, `reports/` et
`provenance/`. Un merge d’intégration n’est pas un
développement et passe. Une maintenance du core du template ou une écriture
directement autorisée sur la canonique s’exécute avec
`PROJECT_CONTROL_HOOK_OVERRIDE="<mandat humain>"`, qui est le mandat explicite exigé
plus haut, rendu visible dans la commande elle-même.

Un renommage compte des deux côtés : déplacer un fichier autorise son emplacement
d'arrivée **et** son retrait de l'emplacement de départ. Le preflight, l'audit et la gate
de commit classent donc l'origine comme la destination ; sortir un fichier de son
emplacement exige que cet emplacement soit lui aussi dans les `authorized_paths`.

Sur la branche d'un Work Item, la gate applique les `authorized_paths` du Work Item actif à
**tout** chemin indexé, et pas seulement au code métier : un chemin refusé par le preflight
est refusé au commit. Elle exige pour cela exactement un Work Item `IN_PROGRESS`.

Un commit ne peut pas emporter la gate : ce que Git exécute n'est pas dans l'arbre qu'un
commit écrit. Retirer le fichier versionné reste possible et ne désarme rien — la copie
tourne toujours et refuse. L'ancien mode (`core.hooksPath scripts/hooks`, la gate dans
l'arbre) fonctionne encore et reste signalé comme tel par `status` et l'audit : il expose
au retrait par un simple commit.

Limite résiduelle, assumée : qui dispose d'un terminal peut effacer la copie installée. Ce
n'est plus un commit déguisé en travail autorisé, c'est un geste explicite hors du projet,
qu'aucune tâche légitime n'exige et que `status` et l'audit constatent au contrôle suivant.
Un agent qui constate une gate absente, modifiée, ou seulement dans l'arbre, la rétablit
(`install-gate`) avant toute autre écriture et le signale au Project Owner ; il ne poursuit
pas son travail.

## Dossier accordé — double arrêt

Le dossier accordé est le dépôt courant, racine du checkout, et lui seul. Une consigne
— ou un plan, un mandat, une scope definition que l’agent rédige lui-même — dont
l’exécution sortirait de ce dossier (écrire dans un autre dépôt ou un autre dossier,
y créer une branche, y committer, y exécuter des scripts, pousser vers un remote)
n’est jamais exécutée d’un trait, même si un document ou une décision antérieure
semble la couvrir. Lire un autre dossier n’est pas en sortir. Elle exige deux arrêts
distincts :

1. `STOP 1 — SORTIE DE PÉRIMÈTRE` : avant toute écriture, l’agent nomme le dossier
   cible exact, l’action prévue et ce qu’elle modifierait, propose l’alternative qui
   reste dans le périmètre — copie, clone jetable, rapport — et attend une réponse
   humaine.
2. `STOP 2 — CONFIRMATION DU PÉRIMÈTRE` : après une première réponse positive,
   l’agent reformule le périmètre exact (dossier, branche, actions autorisées, actions
   qui restent interdites, réversibilité) et attend une seconde confirmation explicite
   qui nomme le dossier. Un « ok », un « go », une confirmation groupée avec une autre
   décision ou déduite d’un accord général ne valent pas.

La décision humaine qui en résulte porte `Folder scope:` et deux lignes
`Confirmation 1:` / `Confirmation 2:` distinctes ; le contrôleur refuse toute
autorisation hors dossier qui ne les porte pas (`HUMAN_AUTHORIZATION`). Par défaut,
l’original d’un projet réel ne sert jamais de terrain d’essai : la voie normale est une
copie dont l’original n’est pas impacté.

`Folder scope` se renseigne aussi lorsque la décision est enregistrée dans le dépôt cible
lui-même : dès qu’un agent a dû franchir un double arrêt pour venir y travailler, la
décision de ce dépôt nomme le dossier et cite les deux confirmations — c’est la trace,
vérifiée par son propre contrôleur, que l’entrée a été confirmée deux fois. Une décision
qui n’autorise qu’un travail interne, sans sortie de périmètre, porte `NOT_APPLICABLE`.

## Copies du dépôt — le tableau des clés

Une copie faite pour protéger l’original (chantier, revue, répétition) a une naissance **et
une fin**. L’original tient le registre de ses copies ; chacune y a un **ticket** — la
décision que le double arrêt a produite, dont l’unique ligne `Folder scope:` nomme le dossier
de la copie ou un dossier qui le contient —, un sort décidé au départ (`RETURN_THEN_ERASE`,
`ERASE`, `KEEP`), une date de retour, et ce avec quoi elle se ferme : un Work Item ou une
version. Dans le template, le ticket est une décision `TPL-D-NNN` qui porte, sur ses propres
lignes, `Folder scope:`, `Confirmation 1:` et `Confirmation 2:`.

1. **Le ticket avant la voiture.** `copy open` enregistre la copie avant qu’elle existe, depuis
   la canonique (`main` pour le template), et imprime sa **fiche de sortie**. Le geste de copie
   la dépose dans `.git/copie.json` (clone) ou dans `copie.json` à la racine du contenant
   (export d’une révision, laissée intacte dans `source/`). Une copie n’est jamais l’original,
   ni dedans, ni autour ; elle ne chevauche aucune autre copie ; son nom suit la règle
   `<dépôt>-<usage>-<référence>[-rang]`.
2. **Une copie n’est jamais un second original** : ni version, ni tag, ni lien vers un remote.
   Elle protège par séparation, pas par interdiction : les droits de l’agent restent ceux de
   son mandat. Dans une copie, `status` commence par sa fiche de sortie ; les commandes `copy`
   n’y tournent pas — elle porte une page périmée du registre — et son audit ne juge pas les
   copies ; un clone sans fiche, qui hérite du registre, n’y écrit rien non plus. Elles tournent
   dans l’original, qui reste là où ses copies ont été enregistrées.
3. **Rendre se prouve.** `copy return` lit **tout** ce que la copie contient — le dossier
   parcouru fichier par fichier et comparé octet par octet à ce que `HEAD` enregistre (aucun
   drapeau d’index, cache de dates ni dossier de travail déclaré ailleurs ne cache rien),
   dossiers ignorés compris, index, références, stash, commits que seul un reflog atteint (des
   deux côtés de ses entrées), et ce que `.git` garde du propriétaire, par liste fermée ; pour
   un export, la révision exportée elle-même — sans lancer aucune commande que la copie
   configure (un clone partiel est refusé avant toute lecture). Chaque élément doit être dans
   l’original — un commit sur **une branche ou un tag** (une référence de suivi, un reflog, une
   tête détachée ne gardent rien longtemps), un fichier **committé** avec les mêmes octets — ou
   abandonné par son nom, avec sa raison. Une revue revient avec son mandat. Ce que le
   contrôleur ne sait pas classer bloque, jamais compté comme vide : opération en cours,
   conflit, dépôt imbriqué, point de montage, fichier spécial (jamais ouvert), autre copie
   enregistrée à l’intérieur, où qu’elle se cache, `.git` compris. Le retour enregistre l’empreinte du contenu,
   sans ambiguïté possible, et le commit de l’original où ses fichiers sont prouvés ; une copie
   retravaillée se rend de nouveau.
4. **Rendre les clés avant de fermer.** `close WI-NNN` refuse tant qu’une copie du Work Item est
   ouverte ; pour une version, l’ordre est rapatrier, intégrer, `copy return`, **puis** le tag,
   puis la vue. `COPIES_RETURNED` échoue quand une copie reste ouverte après que sa cible s’est
   fermée : le garde-fou refusant tout commit dont l’audit échoue, la réparation est **une**
   transaction qui couvre toutes les copies en faute, rendues ou gardées par décision. Le
   retard n’est qu’un avertissement de `status`.
5. **Jamais d’effacement sur une preuve ancienne.** Le contrôleur n’efface rien. `copy cleanup`
   écrit le script que le Project Owner lance, depuis l’original et sans table de
   correspondance : pour chaque copie, `copy check` avec le chemin et l’empreinte de ce qu’il va
   effacer, juste avant de l’effacer. Le contrôle juge le contenu, puis ce que l’original garde
   **encore** (une branche supprimée ou un historique réécrit depuis le retour, et rien n’est
   effacé), puis la place en dernier ; un déplacement (`copy move`), un nouveau retour, une
   garde, un contenu changé ou un autre dossier à la même place le font refuser. `copy close`
   dit `ERASED` quand le dossier n’existe plus, `KEPT` par décision.

Limites assumées : une copie jamais déclarée reste invisible ; le registre ne voit pas ce qui a
été envoyé depuis une copie, seulement ce qui n’est pas revenu ; quelques instants séparent le
contrôle de l’effacement, pendant lesquels personne n’écrit dans la copie ; le rôle d’un fichier
rendu (mandat, livrable…) est déclaré, pas vérifié — le contrôleur prouve des octets, pas un
sens ; un contenu transformé à l’extraction (Git LFS, fins de ligne, filtres) apparaît comme un
élément à rendre ou abandonner ; un simple fichier glissé dans les dossiers que Git tient pour
lui (`objects`, `refs`, `logs`) n’est pas inventorié. Commandes et fichier de preuves :
[Project Control](project_control/README.md#copies-du-dépôt--le-tableau-des-clés).

## Retours au Project Owner

Le Project Owner choisit, à l’initialisation, la forme des retours qui lui sont faits :
`reporting_style` dans Project State, affiché par `status` en première ligne. L’agent le lit
avant son premier retour de la session et s’y tient jusqu’au bout.

- `TECHNICAL` : les retours dans la conversation peuvent porter le détail complet —
  chemins, lignes, octets, SHA-256, verdicts à vocabulaire fermé, sections lettrées.
- `PLAIN` : chaque retour est en langage courant et répond, dans l’ordre, à trois questions
  — **ce qui s’est passé**, **ce que ça change**, **ce qu’il doit faire** (rien, ou une action
  nommée). Pas de terme technique sans une explication d’une ligne ; le détail (chemins,
  empreintes, sorties de commandes) va dans un rapport ou un fichier, pas dans la réponse.
  Un `STOP`, un refus, un incident se disent aussi simplement, sans les minimiser. Toute
  demande de permission dit en une phrase ce qui sera exactement touché ou effacé, et ce
  qui ne le sera pas.

Dans les deux styles, les records, preuves, rapports, messages de commit et décisions
humaines gardent leur forme normative : le style ne s’applique qu’à ce qui est dit au
Project Owner. En `PLAIN`, un rapport commence par un résumé en trois points. Le Project
Owner peut demander ponctuellement l’autre forme sans que le record change ; changer le
style du projet est une décision humaine enregistrée qui met à jour Project State — jamais
une initiative de l’agent. Le contrôleur garantit que le choix existe et est affiché
(`REPORTING_STYLE`) ; le respecter relève de la doctrine, comme la lecture effective des
autorités.

## Vue ROADMAP et idées du Project Owner

L’avancement du projet se lit dans une vue **générée par le contrôleur** depuis les
fichiers du dépôt (`roadmap-view --write` : page HTML non suivie, vue Markdown committée),
jamais rédigée à la main : elle montre, elle ne décide rien, et chaque ligne cite sa source.
Sa forme est stable, son style suit `reporting_style`. Une idée du Project Owner est
enregistrée dans la session où elle est dite, dans ses mots, avec un état fermé
(`idea add` / `idea set`, deux formes synchronisées vérifiées par l’audit `IDEAS`) ; elle ne
quitte la liste que réalisée ou écartée par décision, et l’enregistrer n’autorise rien.
Dans une discussion « ROADMAP <PROJET> », tout message est une régénération, tout le reste
est renvoyé ailleurs, rien n’y est décidé ni écrit au-delà de la vue et de ses réglages.
Détail : [Vue ROADMAP](docs/agent-governance/ROADMAP_VIEW.md).

## Anti-Octopus

Un shared service reste technique. Un orchestrateur ne connaît que `job_id`, `dependencies`, `order`, `timeout`, `status` et `result`. Les échanges suivent `PRODUCER → VERSIONED CONTRACT → CONSUMER`. Ambiguïté d’ownership : `STOP`.

## Autorité humaine, provenance et DONE

Une décision humaine documentée est requise pour promotion, activation, canonicalisation, cutover, irréversibilité, conflit architectural et risque accepté. `UNKNOWN` reste `UNKNOWN` jusqu’à preuve ou décision.

Ne pas confondre `DONE` avec les niveaux de preuve de la
[Definition of Done](docs/governance/DEFINITION_OF_DONE.md). Chaque Work Item déclare
`runtime_target` : `NOT_APPLICABLE`, `CONTROLLED_NON_PRODUCTION_RUNTIME` ou
`PRODUCTION`. Une cible runtime rend `runtime_proof` obligatoire ; `deployment`
reste déclaré séparément. `RUNTIME_PROVEN` ne vaut jamais `PRODUCTION_VERIFIED`.

Toute applicabilité `UNKNOWN` bloque `DONE`. Une gate applicable exige le statut
correspondant à sa cible et un rapport JSON local vérifiable selon
[Project Control](project_control/README.md) ; une gate non applicable est
explicitement `NOT_APPLICABLE`. Le contrôleur vérifie les déclarations, références
Git et empreintes, pas la vérité indépendante d’une exécution décrite dans un
rapport. Une preuve manquante ou échouée ne peut pas être transformée en réussite. Une preuve qui
annonce `PASS` alors que **toutes** les pièces qu'elle cite rapportent un échec est refusée : le
contrôleur n'exécute pas la campagne, mais il lit ce que la preuve donne à lire, et une preuve ne
peut pas contredire tout ce qu'elle montre. Garder le journal d'une campagne ratée à côté de ce qui
a réussi reste la bonne conduite, et ne fait pas échouer la clôture.
Après une reprise, la preuve de réussite doit couvrir au moins le `start_head` du
nouvel Agent Run. Les rapports historiques restent vérifiables et conservés ; ils
ne remplacent pas cette nouvelle preuve. Seul `close` peut produire `DONE`.

Un projet qui adopte le contrôleur avec un historique déclare une baseline
d’adoption par décision humaine (`legacy_baseline` dans Project State) : les
clôtures antérieures restent figées et vérifiées octet pour octet, jamais
reconstruites ni requalifiées ; tout le travail postérieur suit les règles de preuve
courantes. Le contrôleur ne substitue jamais `HEAD` à cette baseline.

Cette promesse couvre aussi le **vocabulaire** des décisions. Une décision enregistrée avant
la baseline, et inchangée depuis, est lue telle qu'elle a été écrite : une règle de forme
introduite par une version ultérieure du squelette ne la requalifie pas. Ce qu'une décision
doit porter reste exigé d'elle — son objet, son autorisation, et ses deux confirmations si
elle sort du dossier accordé. L'exemption suit l'état et non le nom : une décision réécrite
depuis la baseline repasse sous la règle courante. Aucune transition d'aujourd'hui n'en
bénéficie : `create-work-item`, `block`, `resume` et `close` lisent leur mandat en entier,
si bien qu'un refus enregistré ne peut jamais autoriser un travail nouveau.

### Deux volumes : le carnet vivant et le volume relié

Le registre des décisions est lu à chaque démarrage et ne fait que grossir. Un projet peut
le couper en deux, **sur décision humaine et par le contrôleur seul** :

- le **carnet vivant**, `docs/governance/HUMAN_DECISIONS.md`, garde les décisions
  postérieures à la baseline d’adoption et reçoit un **sommaire** — une ligne par décision
  reliée : numéro, date, `Decision`, première ligne de `Chosen option`, recopiées telles
  qu’elles ont été écrites. Il reste l’autorité routée, lue à chaque `start` ;
- le **volume relié**, `docs/governance/HUMAN_DECISIONS_VOLUME_1.md`, garde les décisions
  figées par la baseline d’adoption, **à l’octet près**. Il n’est pas routé : on ne le lit
  pas au démarrage, on l’ouvre au besoin avec `decision show HD-NNN`.

La ligne de coupe est la baseline d’adoption déjà déclarée : aucun objet nouveau, aucune
troisième baseline. La promesse « jamais reconstruites ni requalifiées » s’étend au
déplacement — relier une décision ne la réécrit pas, ne la résume pas et ne lui retire pas
l’exemption de vocabulaire ci-dessus : le contrôleur résout, audite et affiche une décision
dans l’un ou l’autre volume, indifféremment.

`decision bind --human-decision HD-NNN` exécute la coupe depuis la canonique, sur un
worktree propre, et committe lui-même le résultat. Il **refuse** et n’écrit rien si le projet
ne déclare pas de baseline d’adoption, si un seul bloc figé diffère de sa forme à la
baseline, si une seule référence cesserait de se résoudre, ou si un volume existe déjà :
relier de nouveau est une décision humaine, pas une répétition. Une décision neuve est
toujours enregistrée dans le carnet vivant, jamais dans un volume. `decision show HD-NNN`
est en lecture seule.

Le volume **nomme le commit auquel il a été relié** (`Adoption baseline:`), et c’est à ce
commit-là que l’audit compare — jamais à la baseline que le projet déclare aujourd’hui, qui peut
légitimement avancer. Le contrôle `DECISION_VOLUMES_CONSISTENT` vérifie à chaque audit, dans cet
ordre : **qu’aucune décision n’a disparu** — chaque décision enregistrée à cette origine est
encore dans l’un des deux volumes, même si aucun record ne la cite ; que chaque bloc relié est
identique à sa forme à cette origine ; que le sommaire est **complet et fidèle** — une ligne par
décision reliée, et chaque ligne exactement celle que le contrôleur écrirait aujourd’hui pour la
décision qu’elle nomme ; qu’aucune décision n’est dans les deux volumes ; et qu’aucune décision
postérieure à la ligne de coupe n’a été reliée. Vérifier seulement l’intégrité de ce qu’on
retrouve laisserait une décision que personne ne cite disparaître avec sa ligne de sommaire.
Origine illisible, origine non nommée, déclaration d’adoption retirée : échec explicite, jamais
substitution silencieuse. Un projet qui n’a rien relié se comporte exactement comme avant : le
volume n’existe pas, et rien ne change.

Un bloc va de son titre `## HD-NNN` au titre suivant, ou à la fin du fichier ; les lignes vides
qui l’entourent lui appartiennent, et l’égalité se juge sur ce texte. La reliure est une
transaction comme les autres écritures administratives : elle écrit, vérifie, committe, et
défait tout si l’une des trois échoue — un refus ne laisse jamais une demi-reliure.

Trois choses restent distinctes, et une décision reliée n’en franchit aucune : **retrouvée** n’est
pas **admissible**, et **admissible** n’est pas **lue**. Vivre dans un volume ne crée aucune
exemption : une transition d’aujourd’hui lit son mandat en entier, où qu’il soit enregistré. Et la
preuve de lecture atteste ce que le manifeste énumère — le carnet vivant et son sommaire — jamais
le texte conservé dans le volume : `decision show` donne accès au texte, il ne fabrique pas une
preuve de lecture.

Les lignes de sommaire sont des **repères**, pas des énoncés de décision : coupées, elles ne
disent pas ce qui vient après, et deux décisions peuvent partager le même début. Seul le texte
conservé dans le volume énonce le choix humain ; l’identifiant est ce qui permet de le retrouver.

Le contrôleur **rappelle, il ne relie jamais de lui-même**. Tant qu’aucun volume n’existe, qu’une
baseline d’adoption est déclarée et que les décisions figées pèsent au moins un tiers du registre,
`status` le dit en une ligne et nomme la commande. Une fois la reliure faite, cette ligne cède la
place au décompte des deux volumes. Deux limites assumées : le carnet vivant se remplit à nouveau,
et relier une seconde fois demanderait de déplacer la ligne de coupe — une décision humaine et une
mécanique que cette version ne construit pas ; le journal du squelette lui-même n’est routé nulle
part, si bien qu’un chantier sur le squelette n’est pas tenu de le lire. Les deux sont inscrites
comme dettes connues dans la feuille de route.
