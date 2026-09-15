# Project Control

Project Control relie le travail autorisé à sa conversation, sa décision humaine, sa branche, ses commits et ses preuves. L’agent tient ces records à jour ; le propriétaire du projet tranche les décisions qui engagent le périmètre, le risque ou l’autorité.

## Se repérer

```bash
python3 -B scripts/project_control.py status
python3 -B scripts/project_control.py status --json
```

`status` est une vue en lecture seule, calculée depuis les records existants. Sa première ligne après le projet rappelle le style de retour choisi par le Project Owner (`reporting_style`, voir [AGENTS.core](../docs/agent-governance/AGENTS.core.md#retours-au-project-owner)) : l’agent le lit avant son premier retour. Elle présente l’objectif connu, le mode d’initialisation, la branche et le HEAD courant, l’état des travaux, les éléments manquants et la prochaine action. Elle inclut le résultat de l’audit (`audit_status`) et sort avec un code non nul en cas d’invalidité. Elle ne modifie aucun record, n’autorise aucune écriture et ne remplace pas le preflight.

Une copie neuve suit [FIRST_START](../FIRST_START.md). Un projet initialisé peut rester au repos, sans Work Item actif : aucun chantier permanent n’est exigé.

## Cycle de travail

```bash
python3 -B scripts/project_control.py audit
python3 -B scripts/project_control.py create-work-item WI-NNN ...
python3 -B scripts/project_control.py context-manifest WI-NNN
python3 -B scripts/project_control.py start WI-NNN --authorities-digest <MANIFEST_DIGEST>
python3 -B scripts/project_control.py preflight WI-NNN --path <path>
python3 -B scripts/project_control.py close WI-NNN \
  --test-evidence reports/evidence/WI-NNN/tests.json \
  --integration-evidence reports/evidence/WI-NNN/integration.json
```

L’exemple de clôture convient lorsque seuls tests et intégration sont applicables. Ajouter `--deployment-evidence` et `--runtime-evidence` pour les gates correspondantes ; les options sont répétables. Chaque valeur désigne un rapport JSON, jamais un simple commentaire. Consulter `<commande> --help` pour les paramètres complets.

- Les records administratifs vivent sur la branche canonique uniquement : `create-work-item`, `start`, `block`, `resume` et `close` s’exécutent depuis son checkout, à son tip, sur un worktree propre, et committent eux-mêmes leurs records avec des chemins explicites (`chore(project-control): <transition> WI-NNN`). Une décision humaine rédigée à la main se committe avant la transition qui la consomme. La branche d’un Work Item ne porte jamais de changement administratif ; `preflight` et le hook le refusent (`WORK_BRANCH_RECORDS_READ_ONLY`). En Bootstrap Mode, les records de l’initialisation sont committés avec elle par l’agent.
- `audit`, `preflight` et `pre-commit` sont en lecture seule sur le projet : ils n'écrivent ni record ni fichier de l'arbre de travail. Pour juger l'état indexé, `pre-commit` l'extrait dans un checkout jetable hors de l'arbre de travail, qu'il retire en terminant — et au démarrage, il retire aussi un checkout jetable qu'une commande tuée a laissé, le sien seulement, prouvé par sa marque (voir « La montée se répète avant de s'écrire »). `pre-commit` est la gate exécutée par le hook installé hors de l’arbre de travail (installation et mise à jour : `python3 -B scripts/project_control.py install-gate`, qui copie le fichier versionné `scripts/hooks/pre-commit` dans le dossier des hooks de Git ; l’audit refuse une copie qui diverge de sa référence) : audit du mode courant sur le worktree (tout changement présent, indexé ou non) et protection de la branche canonique sur l’état indexé ; `PROJECT_CONTROL_HOOK_OVERRIDE="<mandat>"` la contourne explicitement, le mandat étant imprimé dans le rapport. Une **fusion d'intégration** n'est pas du développement et passe — à condition de n'emporter que ce que sa branche a produit : aucun chemin que la branche n'a pas touché, et pour chaque chemin qu'elle a touché, **le contenu de la branche** (le résultat d'une fusion peut être édité avant son commit ; un chemin modifié des deux côtés depuis la base est une résolution, jugée par l'audit comme tout état — un renommage compte pour ses deux noms, si bien qu'un changement canonique de l'ancien nom est une résolution dans le nouveau). Les chemins sont lus tels que les fichiers sont nommés, accents, espaces et tabulations compris, et non tels que Git les cite ; un chemin dont le contenu ne peut pas être lu est refusé, jamais comparé. La règle des baselines (`BASELINE_CHANGE_MANDATED`) s'applique partout où l'état du projet entre dans un commit, fusion comprise.
- `create-work-item` exige une Human Decision existante ou son texte explicite ; il crée les records et synchronise roadmap, registre et classification en une transaction.
- `start` exige la branche canonique déclarée et la [preuve de lecture](#preuve-de-lecture-des-autorités) des autorités du Work Item (`--authorities-digest`). Il conserve `base_head`, baseline d’autorisation, capture le HEAD canonique courant dans `start_head`, committe les records du démarrage sur la canonique, puis crée la branche déclarée depuis ce commit (ou avance par fast-forward une branche préexistante située à `start_head`). `base_head` doit être un ancêtre de `start_head` ; l’égalité est admise. Une divergence ou une branche WI préexistante à un autre tip est refusée. Le Work Item passe à `IN_PROGRESS` seulement après un preflight complet réussi, sur la canonique puis sur la branche ; un échec annule le commit de records.
- `close` s’exécute depuis la canonique après intégration, exige chaque preuve applicable, vérifie l’intégration de la branche et des commits déclarés à la baseline courante, conserve les anciennes références de preuve en ajoutant les nouvelles, clôt l’Agent Run, passe le Work Item à `DONE` et committe la clôture.

Une autorisation déjà donnée couvre les conséquences administratives et les étapes ordinaires de son périmètre. Les nouveaux périmètres, risques et décisions d’autorité suivent les règles d’[AGENTS](../AGENTS.md).

Une décision humaine qui autorise une action hors du dépôt courant (`Folder scope:` renseigné) n’est valide qu’avec deux confirmations distinctes enregistrées (`Confirmation 1:`, `Confirmation 2:`) : `preflight`, `create-work-item`, `block`, `resume` et la baseline d’adoption la refusent sinon, avec le motif. C’est la forme mécanique du double arrêt d’`AGENTS.core.md`.

Les mutations portent seulement sur les chemins administratifs explicites. Un échec restaure les fichiers concernés ; un échec de `start` restaure aussi la branche. Project Control n’effectue aucun ajout global Git, push, force ou travail métier.

## Blocage et reprise

Lorsqu’une dépendance externe empêche de poursuivre, conserver le travail et ses
preuves en `BLOCKED`. Ce statut libère le chantier actif sans déclarer une
réussite. Il ne réclame aucun suivi parallèle : `status` et les records existants
présentent le blocage.

```bash
python3 -B scripts/project_control.py block WI-NNN \
  --human-decision HD-NNN --reason-code EXTERNAL_ACCESS_REQUIRED \
  --resume-condition "Accès externe autorisé disponible"
python3 -B scripts/project_control.py resume WI-NNN --human-decision HD-NNN --authorities-digest <MANIFEST_DIGEST>
```

Chaque transition exige une nouvelle décision humaine enregistrée. Elle déclare
exactement une fois `Chosen option: AUTHORIZE`, `Related Work Item: WI-NNN` et
`Project Control action: BLOCK` ou `RESUME`. La décision de blocage contient aussi
`Block reason code` et `Resume condition recorded`, identiques aux paramètres. La
décision de reprise contient `Resume condition confirmed`, identique à la
condition enregistrée. Les placeholders `HD-NNN` de l’exemple désignent donc deux
décisions différentes.

`block` et `resume` s’exécutent depuis la branche canonique, à son tip, sur un
worktree propre, et committent eux-mêmes leurs records. `block` accepte
`AUTHORIZED` ou `IN_PROGRESS`, ajoute un `block_records` de type
`EXTERNAL_DEPENDENCY` et clôt l’Agent Run courant s’il existe ; le travail déjà
committé sur la branche du Work Item reste en place. `resume` exige la preuve de lecture
courante comme `start`, résout le blocage, crée un nouvel Agent Run, committe, puis aligne la branche du Work Item sur le tip
canonique avant le preflight. `base_head` reste la baseline d’autorisation ; le
`start_head` du Work Item reste son premier démarrage, chaque Agent Run porte celui
de sa propre exécution. Le premier démarrage peut aussi suivre un blocage intervenu
avant tout Agent Run.

L’alignement ne réécrit jamais l’histoire : ni rebase, ni cherry-pick, ni reset.
Si la branche est en retard, elle est avancée par fast-forward. Si elle a divergé —
elle porte des commits non intégrés et la branche canonique a avancé entre-temps —
`resume` crée un commit de merge de la canonique dans la branche du Work Item.
Les changements métier sont fusionnés par Git ; les records administratifs
(Human Decisions, roadmap, registre, classifications, Work Items, Conversations,
Agent Runs) ne vivent que sur la canonique et ne peuvent donc pas conflicter. Un
conflit sur un chemin non administratif est un conflit métier : le merge est annulé,
`resume` est refusé avec la liste des chemins, et l’alignement se fait alors sous
l’autorité du Work Item avant une nouvelle reprise. Un échec ultérieur de la
transaction ramène la branche à son tip antérieur et annule le commit de records ;
aucun commit historique n’est perdu.

Un statut de preuve `FAILED` reste `FAILED` après blocage et reprise. Pour clôturer,
il faut de nouveaux rapports réussis couvrant la nouvelle exécution.

## Preuve de lecture des autorités

```bash
python3 -B scripts/project_control.py context-manifest WI-NNN
python3 -B scripts/project_control.py context-manifest WI-NNN --scope security --json
python3 -B scripts/project_control.py start WI-NNN --authorities-digest <MANIFEST_DIGEST>
python3 -B scripts/project_control.py acknowledge-authorities WI-NNN --authorities-digest <MANIFEST_DIGEST>
```

`context-manifest` est en lecture seule. Il liste les autorités du Work Item — les documents de base routés par `docs/agent-governance/mandatory-documents.v1.json` plus ceux des scopes déduits de ses `authorized_paths` (`applications/`, `modules/`, `shared/`, `scripts/`, `tests/`, `project_control/` → `development` ; `contracts/` → `contracts` ; `data/` → `data` ; `docs/governance/`, `docs/adr/`, `docs/agent-governance/` → `governance` ; `docs/architecture/` → `architecture` ; `runtime_proof/`, `project_control/deployments/` → `runtime`) — avec le SHA-256 de chaque fichier tel qu’il est dans le worktree, puis `MANIFEST_DIGEST`, empreinte SHA-256 des lignes `chemin sha256` triées. Sans Work Item, il liste les autorités de base ; `--scope` ajoute un scope à la lecture (`security`, `recovery` n’ont pas de préfixe de chemin) sans changer l’empreinte exigée pour le Work Item, qui est celle de `context-manifest WI-NNN` seul. Les records tenus par Project Control (`ROADMAP.md`, `roadmap-state.v1.json`, `WORKTREE_REGISTRY.md`, `git-path-classifications.v1.json`, `project-state.v1.json`) sont routés pour la lecture mais exclus de l’empreinte ; `HUMAN_DECISIONS.md` en fait partie. `HUMAN_DECISIONS_VOLUME_1.md`, quand il existe, n’est routé nulle part : il n’entre dans aucun manifeste et ne périme aucune preuve (voir [Deux volumes](#deux-volumes--carnet-vivant-et-volume-relié)). Une autorité routée absente du dépôt est une erreur, pas une omission.

`start` et `resume` refusent sans `--authorities-digest`, et refusent une empreinte différente de l’empreinte courante, sans jamais afficher celle-ci : c’est l’agent qui la présente après lecture. L’Agent Run créé enregistre `authorities_read` (`manifest_digest`, `generated_at`, `head`, `scopes`, `entries[{path, sha256}]`). Le preflight d’un Work Item démarré vérifie `AUTHORITY_MANIFEST_PRESENT` (le dernier Agent Run porte la preuve), `AUTHORITY_MANIFEST_COMPLETE` (chaque autorité du Work Item y figure) et `AUTHORITY_MANIFEST_CURRENT` (aucune autorité n’a changé depuis) ; `status` résume ce point par `authorities: CURRENT`, `STALE` ou `MISSING`. Une autorité modifiée depuis la lecture met le preflight en échec avec le chemin concerné, et `close` est refusé (`AUTHORITY_MANIFEST_AT_CLOSE`) ; une autorité comprise dans les `authorized_paths` du Work Item fait exception, ses propres écritures ne périment pas sa preuve. `acknowledge-authorities`, depuis la canonique, sur un worktree propre, enregistre la nouvelle lecture sur le dernier Agent Run et committe (`chore(project-control): acknowledge authorities WI-NNN`) ; une empreinte stale y est refusée de la même façon. Depuis la branche du Work Item : committer le travail en cours, revenir sur la canonique, `acknowledge-authorities`, puis réaligner la branche sur la canonique (fast-forward ou merge).

L’audit exige `authorities_read` sur tout Agent Run absent de la baseline d’adoption (`legacy_baseline`) et de la baseline de preuve de lecture (`authorities_baseline`, voir [Compatibilité](#compatibilité--baseline-dadoption)) ; les Agent Runs présents à l’une de ces baselines restent valides sans preuve, à l’état où ils ont été gelés. Une mise à niveau vers une version qui introduit la preuve de lecture, sur un projet ayant déjà des Agent Runs après sa baseline d’adoption, déclare donc `authorities_baseline` dans le Work Item de mise à niveau, par sa décision humaine ; sans cette déclaration, l’audit refuse ces Agent Runs (`AUTHORITIES_BASELINE`, `SCHEMA_VALIDATION`) et aucune transition n’est plus possible.

## Deux volumes : carnet vivant et volume relié

```bash
python3 -B scripts/project_control.py decision bind --human-decision HD-NNN
python3 -B scripts/project_control.py decision show HD-NNN
```

Le registre des décisions est lu à chaque `start`, chaque `resume` et chaque `acknowledge-authorities`, et ne fait que grossir. `decision bind` le coupe en deux à la ligne déjà déclarée par le projet, sa baseline d’adoption : les décisions figées par elle partent dans `docs/governance/HUMAN_DECISIONS_VOLUME_1.md`, **texte identique à l’octet près**, et `HUMAN_DECISIONS.md` reçoit un sommaire — une ligne par décision reliée (numéro, date, `Decision`, première ligne de `Chosen option`), entre les marqueurs `<!-- decision-volume-1:summary:start -->` et `<!-- decision-volume-1:summary:end -->`. Le carnet vivant reste l’autorité routée ; le volume relié n’est routé nulle part, donc un agent ne le lit plus, tandis que le contrôleur continue d’y résoudre, d’y auditer et d’y afficher chaque décision. Relier ne réécrit rien, ne résume rien et ne requalifie rien : l’exemption de vocabulaire des décisions figées suit la décision dans son volume.

`decision bind` s’exécute depuis la canonique, sur un worktree propre, exige une décision humaine valide comme mandat (`--human-decision`) et committe lui-même le résultat (`chore(project-control): bind N frozen Human Decision(s) into volume 1 (HD-NNN)`). Il refuse, sans rien écrire, dans cinq cas : `NO_ADOPTION_BASELINE` (aucune ligne de coupe déclarée), `BLOCK_CHANGED_SINCE_BASELINE` (un bloc figé a été réécrit depuis la baseline — il repasse sous la règle courante et ne peut pas être relié), `NOTHING_TO_BIND`, `REFERENCES_WOULD_BREAK` (une référence `human_decision_refs` cesserait de se résoudre), et un volume déjà présent — relier de nouveau est une décision humaine, pas une répétition. La coupe est réversible par Git. `decision show` est en lecture seule et affiche une décision de l’un ou l’autre volume, en nommant celui qui la porte.

Une décision neuve est toujours enregistrée dans le carnet vivant : `create-work-item` n’écrit jamais dans un volume relié.

Le volume nomme, sur sa propre ligne `Adoption baseline: <commit 40 caractères>`, l’origine à laquelle il a été relié. C’est **cette** origine qui sert de terme de comparaison, jamais la baseline déclarée aujourd’hui : une déclaration peut légitimement avancer, et le texte figé appartient à la ligne où il a été relié. `status` et l’audit signalent l’écart quand les deux diffèrent.

`DECISION_VOLUMES_CONSISTENT` vérifie à chaque audit, dans cet ordre : **qu’aucune décision n’a disparu** — chaque décision enregistrée à l’origine de la reliure est encore dans l’un des deux volumes, même si aucun record ne la cite (sans ce contrôle, une décision que personne ne cite pourrait être retirée avec sa ligne de sommaire sans que rien ne s’en aperçoive) ; que chaque bloc relié est identique à sa forme à cette origine ; que le sommaire est **complet et fidèle**, c’est-à-dire une ligne par décision reliée et chaque ligne exactement celle que le contrôleur écrirait aujourd’hui pour la décision qu’elle nomme ; qu’aucune décision n’est enregistrée dans les deux volumes ; et qu’aucune décision postérieure à la ligne de coupe n’a été reliée. Une origine non nommée, illisible, ou une déclaration d’adoption retirée produisent un échec explicite.

Trois propriétés restent distinctes : une référence **retrouvée** n’est pas une référence **admissible**, et une référence admissible n’est pas un texte **lu**. Vivre dans un volume ne crée aucune exemption — `create-work-item`, `block`, `resume` et `close` lisent leur mandat en entier, où qu’il soit enregistré — et la preuve de lecture n’atteste que ce que le manifeste énumère : le carnet vivant et son sommaire, jamais le texte du volume. Les lignes de sommaire sont des repères de recherche, pas des énoncés de décision : coupées, elles ne disent pas ce qui suit, et deux décisions peuvent partager le même début ; l’identifiant est ce qui les distingue.

Un bloc va de son titre `## HD-NNN` au titre suivant ou à la fin du fichier, lignes vides comprises ; c’est ce texte qui est comparé. La reliure est une transaction administrative ordinaire : écriture, vérification, commit, et retour complet à l’état antérieur si l’une des trois échoue — un refus ne laisse jamais une demi-reliure. Sans volume, le contrôle passe en une ligne et rien ne change dans le projet — `status` n’ajoute sa ligne « Décisions : N vivantes | M reliées » que lorsqu’un volume existe.

Le contrôleur rappelle et ne relie jamais seul. Tant qu’aucun volume n’existe, qu’une baseline d’adoption est déclarée et que les décisions figées occupent **au moins un tiers** du registre, `status` le signale et nomme la commande. La grandeur mesurée est la **part brute occupée par les blocs figés**, pas l’économie nette : le sommaire qui les remplace garde un peu de place. Le rappel annonce donc un potentiel, sous réserve des contrôles de la commande — laquelle peut refuser, par exemple si un bloc figé a été réécrit depuis la baseline. Le rappel n’apparaît que là où la commande existe : une fois la reliure faite, il cède la place au décompte des deux volumes. Deux dettes sont assumées et écrites dans la feuille de route : le carnet vivant se remplit à nouveau et relier une seconde fois exigerait de déplacer la ligne de coupe, ce que cette version ne construit pas ; et le journal du squelette lui-même n’est routé nulle part.

## Applicabilité et cible runtime

Chaque Work Item déclare `code`, `tests`, `integration`, `deployment` et `runtime_proof`. `UNKNOWN` peut décrire une préparation, mais bloque le preflight et `DONE`. Une gate non applicable exige `NOT_APPLICABLE`.

`runtime_target` vaut `NOT_APPLICABLE`, `CONTROLLED_NON_PRODUCTION_RUNTIME` ou `PRODUCTION`. À la création, utiliser `--runtime-target` pour une cible runtime applicable. Les niveaux de déploiement et de preuve requis dépendent de cette cible : voir la [Definition of Done](../docs/governance/DEFINITION_OF_DONE.md). Les tests et l’intégration exigent respectivement `TESTED` et `INTEGRATED`.

Le couplage entre la cible et les gates runtime est à sens unique. Sans cible runtime, `deployment` et `runtime_proof` sont `NOT_APPLICABLE`. Avec une cible runtime, `runtime_proof` est obligatoirement `APPLICABLE` ; `deployment` reste déclaré séparément : `APPLICABLE` lorsque le Work Item installe lui-même le commit ou l’artefact, `NOT_APPLICABLE` pour une preuve runtime sur un déploiement préexistant. Un déploiement sans preuve runtime est refusé.

## Format des preuves

Les rapports et leurs artefacts résident dans `reports/evidence/<WI-NNN>/`. Ce dossier fait toujours partie des chemins autorisés du Work Item : `create-work-item` l’ajoute à `authorized_paths`, de sorte qu’un rapport en préparation ne fait pas échouer le preflight. Les chemins sont relatifs à la racine du dépôt. Le [schéma des preuves](schemas/evidence.v1.schema.json) définit ces champs obligatoires, sans champ supplémentaire :

| Champ | Valeur |
|---|---|
| `schema_version` | `1.0.0` |
| `work_item_id` | Identifiant du Work Item concerné |
| `gate` | `tests`, `integration`, `deployment` ou `runtime_proof` |
| `result` | `PASS` ou `FAIL` ; seule une réussite satisfait la gate |
| `level` | Niveau attendu pour cette gate et cette cible |
| `subject_commit` | SHA Git de 40 caractères du commit testé ou observé |
| `runtime_target` | Même cible explicite que le Work Item |
| `recorded_at` | Date et heure ISO avec fuseau horaire, jamais dans le futur |
| `summary` | Résumé non vide des vérifications et résultats |
| `artifacts` | Liste non vide d’objets `{ "path": "reports/evidence/<WI-NNN>/…", "sha256": "…" }` |

Exemple complet, directement recopiable — les deux pièges du format sont l'horodatage, qui doit
porter son fuseau, et le chemin des artefacts, qui doit être sous `reports/evidence/<WI-NNN>/` :

```json
{
  "schema_version": "1.0.0",
  "work_item_id": "WI-001",
  "gate": "tests",
  "result": "PASS",
  "level": "TESTED",
  "subject_commit": "0000000000000000000000000000000000000000",
  "runtime_target": "NOT_APPLICABLE",
  "recorded_at": "2026-01-31T14:05:00+01:00",
  "summary": "29 essais unittest sur le module et son point d'entrée ; tous réussis.",
  "artifacts": [
    {"path": "reports/evidence/WI-001/sortie-tests.txt", "sha256": "<empreinte SHA-256 du fichier>"}
  ]
}
```

**Une preuve ne peut pas contredire tout ce qu'elle montre.** Quand `result` vaut `PASS`, le
contrôleur lit les artefacts texte et refuse la preuve **si tous** rapportent un échec. Une pièce
rapporte un échec dans deux cas, et le contrôleur les lit dans cet ordre :

1. **elle porte un verdict d'échec** — une ligne commençant par `FAILED`, un résumé pytest
   annonçant des échecs ou des erreurs. Un verdict tranche, quoi que la pièce contienne par
   ailleurs : une campagne ratée suivie d'une relance verte dans le *même* fichier reste refusée,
   la relance verte se cite dans sa propre pièce ;
2. **elle porte un diagnostic sans verdict de réussite** — une ligne commençant par `FAIL:` ou
   `ERROR:`, un `Traceback (most recent call last):`, un décompte `failures=` ou `errors=` non
   nul, alors que rien dans la pièce n'annonce une réussite (`OK`, `PASS`, un résumé pytest
   entièrement vert). Un diagnostic seul, c'est tout ce qu'un programme mort a eu le temps de
   dire ; le même diagnostic à côté d'un `OK`, c'est ce qu'imprime un essai qui vérifie qu'une
   entrée invalide est refusée, et il ne fait pas d'une preuve une contradiction.

Le contrôle est volontairement étroit. Une preuve **peut** porter le journal d'une campagne ratée à côté de ce qui a
réussi — c'est même ce que la doctrine demande : la campagne ratée reste visible, expliquée dans le
résumé, et l'historique la conserve. Seule une preuve dont **chaque** pièce lisible rapporte un
échec se contredit elle-même, et c'est ce cas-là qui est refusé : celui de l'auteur qui recopie une
sortie sans la lire. Le contrôle n'exécute rien et ne juge pas la campagne ; les pièces binaires ne
sont pas lues et ne témoignent de rien. Une campagne qui a échoué peut aussi s'enregistrer comme sa
propre preuve avec `result: FAIL`.

Un artefact contient par exemple le résultat des tests ou les observations runtime ; son empreinte SHA-256 doit correspondre au fichier. À la clôture, le rapport et chaque artefact doivent être suivis dans Git et identiques à leur version dans HEAD. Ce HEAD est conservé dans `close_head` pour les audits ultérieurs. `subject_commit` doit descendre de `start_head` et être un ancêtre de cette baseline ; l’égalité est admise. Seuls des changements administratifs ou de preuves sont admis depuis le commit concerné. Un changement métier ultérieur exige une nouvelle preuve.

Pour une preuve de réussite après `resume`, cette borne basse est le `start_head`
du dernier Agent Run. Les rapports historiques, notamment `FAIL`, restent reliés
au démarrage initial et conservent leurs fichiers et empreintes ; les changements
ultérieurs ne les effacent pas et ils ne satisfont pas la nouvelle gate.

Un rapport ou artefact devient immuable dès son premier commit. Une correction
utilise un nouveau chemin et conserve l’original ; réécrire le fichier puis le
committer à nouveau est refusé, même avec une empreinte recalculée.

Préparer les preuves après les vérifications, enregistrer les rapports et artefacts dans Git avec des chemins explicites, puis lancer `close`. Le contrôleur refuse un rapport absent, mal formé, incohérent avec la gate ou la cible, périmé par un changement métier, ou dont les fichiers ne correspondent plus à Git et aux empreintes. L’historique peut conserver un rapport `FAIL` ; la dernière preuve retenue pour chaque gate doit être `PASS`.

Ces contrôles vérifient la cohérence des déclarations et des références. Ils n’attestent pas indépendamment que l’exécution décrite a réellement eu lieu. Les décisions humaines requises pour promotion, activation ou production restent obligatoires.

## Vue ROADMAP et idées du Project Owner

```bash
python3 -B scripts/project_control.py roadmap-view                 # la vue se calcule-t-elle ? rien n’est écrit
python3 -B scripts/project_control.py roadmap-view --json          # le modèle de la vue
python3 -B scripts/project_control.py roadmap-view --write         # écrit la page et la vue Markdown
python3 -B scripts/project_control.py roadmap-view --write --style TECHNICAL   # force ponctuellement l’autre style
python3 -B scripts/project_control.py idea add --quote "<mots du Project Owner>" --source "<discussion, date>" [--state EVOKED] [--target WI-NNN|HD-NNN|<texte>] [--note "…"]
python3 -B scripts/project_control.py idea set ID-NNN --state PLANNED --target WI-NNN [--note "…"]
```

`roadmap-view` calcule la vue d’avancement depuis les fichiers du dépôt — roadmap et records de Work Items, décisions humaines, idées, Project State, manifeste du core, remotes et tags — et la rend dans une forme stable : bandeau de vérification, chiffres clés, versions, « Maintenant », « Ce qui t’attend » (actions du Project Owner), « Prochaines étapes », « Plus loin », les idées et ce qu’elles sont devenues, le passé replié, un repli technique. Le style suit `reporting_style` (`roadmap-view.v1.json` : `FOLLOW_REPORTING_STYLE`, `PLAIN` ou `TECHNICAL`) ; `--style` force l’autre forme pour une exécution sans rien changer au projet. `--write` produit `reports/roadmap/ROADMAP.html` (non suivi par Git) et `docs/governance/ROADMAP_VIEW.md` (committé ; sa première ligne porte `sources_digest`, l’empreinte des fichiers sources) ; `--html` et `--markdown` choisissent d’autres chemins dans le dépôt. La vue montre, elle ne décide rien : chaque ligne cite sa source, et rien n’est complété.

`status` affiche « Vue roadmap : à jour | périmée | absente » ; l’audit (`ROADMAP_VIEW`) vérifie seulement les réglages — une vue périmée n’est jamais une erreur, seulement une régénération à faire. Les réglages (`project_control/roadmap-view.v1.json`) sont `style`, `zoom` (passé replié ou déployé, futur lointain en titres ou en détail), `language`, `regeneration` (`OFF`, `HOURLY`, `EVERY_4_HOURS`, `DAILY` : le rythme demandé à l’outil qui régénère, que le contrôleur affiche sans le planifier) et `mirrors` (adresses des pages publiées qui reflètent la vue).

`idea` enregistre une idée du Project Owner dans ses mots, datée, avec sa source et un état fermé (`EVOKED`, `TO_CLARIFY`, `TO_SET`, `SCOPED`, `PLANNED`, `IN_PROGRESS`, `REALIZED`, `APPLIED`, `INTEGRATED`, `LATER`, `DISCARDED`), en deux formes synchronisées : `docs/governance/IDEAS.md` (table gérée) et `ideas-state.v1.json`. La cible est libre ; si elle est un `WI-NNN` il doit être dans la roadmap, si elle est une `HD-NNN` elle doit être enregistrée ; `DISCARDED` exige la cible qui nomme la décision. En `NORMAL_MODE`, `idea` s’exécute depuis la branche canonique sur un worktree propre et committe lui-même les deux formes (`chore(project-control): idea ID-NNN <état>`) ; en `BOOTSTRAP_MODE`, il écrit sans committer. L’audit (`IDEAS`) vérifie la synchronisation, l’unicité des identifiants, les états et les cibles. Enregistrer une idée n’autorise rien.

Dans le squelette lui-même (`repository_role` = `PROJECT_TEMPLATE`), les sources sont `provenance/roadmap-template.v1.json` (versions, chantiers et leurs fiches sous `provenance/maintenance/scopes/`, idées, passé) et `provenance/roadmap-view.v1.json` ; les sorties vont sous `provenance/roadmap/ROADMAP.html` et `provenance/ROADMAP_VIEW.md`. Ces fichiers décrivent le template et ne servent jamais à un projet dérivé, qui ne les lit pas.

## Où sont les records ?

- `project-state.v1.json` : identité, style de retour et langue choisis par le Project Owner (`reporting_style` : `TECHNICAL` ou `PLAIN` ; `language` : `FR` ou `EN` — `UNKNOWN` tant que la question n’a pas été posée, et la clôture de l’initialisation les exige tous deux), transition FIRST_START, baseline d’adoption (`legacy_baseline`) et baseline de preuve de lecture (`authorities_baseline`).
- `work-items/` : objectif, scope, impacts, dépendances, applicabilité et preuves.
- `conversations/` : référence de conversation et résumé ; aucun secret ni copie intégrale obligatoire.
- `agent-runs/` : exécutions, scope, branche, commits, résultat et preuve de lecture des autorités (`authorities_read`).
- `deployments/` : records de déploiement lorsqu’ils sont applicables.
- `schemas/` : contrats des records et preuves.

L’identifiant interne est `WI-NNN`. Une clé facultative construit seulement l’affichage : `ALPHA` + `WI-001` donne `ALPHA-001`. Aucun fournisseur de conversation ou d’agent n’est imposé.

## Compatibilité : baseline d’adoption

Un projet qui adopte ce contrôleur avec un historique de Work Items ne migre pas ses records : il fige son histoire à un commit d’adoption et applique le contrat courant à tout ce qui suit. Le contrôleur ne devine ni `close_head`, ni cible, ni niveau de preuve pour une clôture passée, et ne substitue jamais `HEAD` à la baseline déclarée.

`project-state.v1.json` porte la déclaration, `null` pour un projet sans histoire antérieure :

```json
"legacy_baseline": {"head": "<commit d’adoption, 40 caractères>", "human_decision_ref": "HD-NNN"}
```

Le commit doit exister et être un ancêtre de `HEAD` ; la décision humaine doit être enregistrée dans `HUMAN_DECISIONS.md` **et nommer ce commit**, dans un champ propre à la baseline qu'elle déclare :

```
Legacy baseline commit: <le même commit, 40 caractères>
```

Une déclaration est ancrée à sa décision : le contrôleur refuse une baseline dont le commit n'est pas celui que sa décision cite, si bien qu'une décision qui a autorisé la ligne A ne peut pas servir à déclarer la ligne B — déplacer la ligne exige une nouvelle décision, qui dit où et pourquoi. Une décision dont l'option choisie est `REJECT` ne déclare rien, et une décision choisit une fois : deux lignes `Chosen option`, quelles qu'elles soient, ne déclarent rien non plus. Une baseline absente, divergente, sans décision ou dont la décision ne la nomme pas bloque l’audit. Deux contrôles l’appliquent :

- `LEGACY_RECORDS_PRESENT` : chaque Work Item enregistré à la baseline existe toujours au même chemin.
- `LEGACY_EVIDENCE_FROZEN` : un Work Item `DONE` à la baseline conserve exactement ses octets (`status --json` le présente en `LEGACY_PRESERVED`) ; pour les autres, les références de preuve enregistrées à la baseline restent un préfixe inchangé de chaque gate.
- Les Agent Runs présents à la baseline restent valides sans `authorities_read` ; tout Agent Run créé après elle porte la preuve de lecture.
- Les décisions humaines enregistrées à la baseline et inchangées depuis sont lues dans leur vocabulaire d'origine : le contrôle `Chosen option: AUTHORIZE`, introduit par une version postérieure, ne leur est pas appliqué. Le reste est exigé d'elles comme de toute décision — `Decision`, `Authorized by`, et les deux confirmations d'un `Folder scope`. L'exemption suit l'état et non le nom : une décision dont le texte change depuis la baseline repasse sous la règle courante. Les transitions du jour (`create-work-item`, `block`, `resume`, `close`) lisent toujours leur mandat en entier, et un refus enregistré n'autorise jamais un travail nouveau.

La preuve de lecture des autorités a sa propre baseline, `authorities_baseline`, sur le même modèle et obligatoire (`null` sans Agent Run antérieur à la preuve de lecture) :

```json
"authorities_baseline": {"head": "<commit, 40 caractères>", "human_decision_ref": "HD-NNN"}
```

Sa décision la nomme de la même façon, dans son propre champ — `Authorities baseline commit: <commit>` ; une décision peut porter les deux champs si elle déclare les deux lignes. Elle sert au projet qui a adopté le contrôleur avant la preuve de lecture (squelette antérieur à 3.6) et qui monte de version : ses Agent Runs enregistrés entre `legacy_baseline` et cette adoption n’ont pas de `authorities_read` et, une fois clos, ne peuvent plus en recevoir (`acknowledge-authorities` n’accepte qu’un Agent Run en cours). Le commit déclaré fige ces Agent Runs — ceux présents dans l’arbre à ce commit sont exempts (`AUTHORITIES_BASELINE` en rend compte) — et tout Agent Run créé ensuite porte la preuve. Le Work Item de mise à niveau déclare cette baseline par sa décision humaine, typiquement au commit de son propre démarrage ; son Agent Run en cours enregistre ensuite sa lecture par `acknowledge-authorities` depuis la canonique avant `close`. Même règles de validité que `legacy_baseline` : commit existant et ancêtre de `HEAD`, décision enregistrée, `HEAD` jamais substitué ; `NOT_STARTED` ne peut pas la déclarer.

**Une baseline ne se retire et ne se déplace que sur décision.** Le fichier d'état reste ouvert aux chantiers — la langue et le style y vivent — mais ses deux lignes de baseline changent de régime. Partout où l'état du projet entre dans un commit — branche de chantier, canonique, fusion d'intégration —, le garde-fou de commit compare l'état indexé à celui de `HEAD` (`BASELINE_CHANGE_MANDATED`) :

- une baseline **retirée** (`null`) exige qu'une décision du chantier en cours, enregistrée sur la branche canonique avant le travail, porte `Legacy baseline removed: <commit retiré>` (ou `Authorities baseline removed:`) ; une décision seulement sur le disque ne mandate rien ;
- une baseline **déplacée** doit descendre de celle qu'elle remplace — la ligne du passé avance, elle ne recule jamais ; la décision qui nomme le nouveau commit est vérifiée par l'audit de l'état indexé ;
- une baseline **déclarée** là où il n'y en avait pas passe, et son ancrage est vérifié par le même audit.

Ce que ces règles ferment : le scénario où un chantier autorisé sur l'état du projet retirait la ligne, où l'on modifiait ensuite une clôture figée sur la branche canonique, puis où l'on redéclarait la ligne sur le commit réécrit en citant la vieille décision — le tout par la voie normale. Les travaux figés eux-mêmes n'ont pas besoin d'une mémoire séparée : le contrôleur les relit **tels que Git les tient au commit de la baseline**, et l'historique n'est pas ce qu'un chantier peut effacer. Ce qui manquait, c'était que la ligne ne bouge pas en silence. Un humain peut toujours la retirer ou la déplacer : par une décision qui dit ce qu'elle fait.

**Projet dont les baselines sont antérieures à cette règle.** Les décisions qui les ont déclarées ne nomment pas leur commit ; elles ne sont pas réécrites — une décision figée reste ce qu'elle est. Le projet enregistre, pour chaque baseline, une décision de confirmation qui nomme le commit exact (`Legacy baseline commit:` / `Authorities baseline commit:`) et cite la décision d'origine — le commit nommé est ce que le contrôleur vérifie, à l'octet ; la citation de l'origine est une obligation de rédaction, qu'il ne vérifie pas —, puis un chantier autorisé sur `project_control/project-state.v1.json` fait citer ces décisions par `human_decision_ref`. Cela se fait **avant** la montée vers la version qui porte cette règle : la répétition de la montée (`UPGRADE_REHEARSAL`, ci-dessous) la refuse tant que ce n'est pas fait.

Un Work Item non clos à la baseline (`AUTHORIZED`, `BLOCKED`, `IN_PROGRESS`) suit le contrat courant à sa prochaine clôture : nouvelles preuves vérifiables après le préfixe historique, `close_head`, niveaux selon sa cible. Ni le numéro du Work Item ni l’absence d’un champ ne donnent d’exemption. Les records existants sans `block_records` restent valides tant qu’ils ne déclarent pas `BLOCKED`.

Le validateur exécute le sous-ensemble de JSON Schema utilisé par le core (types, propriétés, champs requis, constantes, valeurs admises, motifs, tailles et unicité). Un mot-clé non pris en charge dans un schéma de record est refusé ; il ne prétend pas implémenter tout JSON Schema.

## Version du squelette et mise à jour du core

Le core du squelette — contrôleur, traçabilité Git, hook, tests du template et fixtures, schémas, ce document, la Definition of Done, `CLAUDE.md`, `FIRST_START.md`, `ADOPTION.md`, `docs/agent-governance/AGENTS.core.md` et `docs/agent-governance/ROADMAP_VIEW.md` — est décrit par `provenance/core-manifest.v1.json` : version du squelette (`skeleton_version`) et empreinte SHA-256 de chaque fichier core. Le manifeste voyage avec le core ; il est régénéré par chaque maintenance du template (`core-manifest --write --version MAJOR.MINOR.PATCH`, réservé au template) et jamais édité dans un projet dérivé. `FIRST_START.md` est hashé avec son marqueur `INITIALIZATION_STATUS` normalisé : initialiser un projet ne modifie pas le core.

`audit` vérifie que le manifeste est présent et bien formé, que chaque fichier core listé existe, et qu’`AGENTS.md` déclare le core (`` `AGENTS_CORE: docs/agent-governance/AGENTS.core.md` ``, une seule fois). `status` affiche la version et tout écart local (`core_drift` : `MODIFIED_LOCALLY`, `MISSING`). Un fichier core modifié localement n’est pas une erreur d’audit : c’est un écart signalé, que `template-upgrade` refuse d’écraser sans décision explicite, et qu’une amélioration générique doit faire remonter au template.

```bash
python3 -B scripts/project_control.py core-manifest                      # le manifeste décrit-il cet arbre ?
python3 -B scripts/project_control.py template-upgrade --source <arbre du template>          # rapport, rien n’est écrit
python3 -B scripts/project_control.py template-upgrade --source <arbre du template> --apply  # mise à jour
```

`template-upgrade` compare le manifeste local au manifeste de la source (un checkout ou une archive extraite du template, dont le core doit être intact) et classe chaque fichier core : `IDENTICAL`, `UPDATED` (intact localement, différent en amont), `ADDED` (absent localement), `REMOVED_UPSTREAM` (listé localement, absent en amont : signalé, jamais supprimé), `MODIFIED_LOCALLY` (différent du manifeste local : refusé, sauf `--overwrite <chemin>` explicite par fichier). Sans `--apply`, rien n’est écrit dans le projet — la répétition décrite plus bas écrit et committe dans un checkout jetable hors de l'arbre de travail, qu'elle retire ; et le contrôleur peut, au démarrage, retirer un checkout jetable qu'une de ses commandes tuées a laissé. Avec `--apply`, en `NORMAL_MODE` seulement, les fichiers intacts ou absents sont écrits avec leurs droits d’exécution, le marqueur d’initialisation de `FIRST_START.md` est conservé, le manifeste de la source devient celui du projet, et l’ensemble est vérifié avant validation ; un échec restaure tout. Un retour vers une version antérieure est refusé. Aucun record n’est touché.

**Les fichiers que la nouvelle version exige et que le core ne porte pas.** Une version plus récente peut rendre obligatoires des fichiers qui appartiennent au projet — sa liste d'idées, ses réglages de vue : `audit` les exige, mais `template-upgrade` ne les écrit pas avec le core, parce qu'ils ne sont pas au core. Absents, ils font échouer l'audit, et les commandes censées les créer les exigent elles aussi : le projet ne peut plus ni auditer ni committer. Ce sont des records administratifs, donc ils vivent sur la branche canonique, pas sur la branche du Work Item qui porte le core.

`template-upgrade` les nomme dans son rapport (`REQUIRED_FILES`) et `--apply` refuse tant qu'ils manquent, plutôt que de laisser le projet dans cet état. La commande qui les écrit, sur la branche canonique et nulle part ailleurs :

```bash
python3 -B scripts/project_control.py template-upgrade --source <arbre du template> --seed-required
```

Elle n'écrit que ces fichiers-là, vierges comme le template les tient, jamais par-dessus un fichier existant. On les committe sur la canonique comme un changement administratif, puis on applique le core normalement.

**La montée se répète avant de s'écrire.** La commande qui monte un projet s'exécute sous *son* contrôleur, qui ignore les règles que la nouvelle version apporte — un fichier qu'elle exige désormais, un champ qu'elle demande à une décision. Appliquée à l'aveugle, une telle montée se terminait et laissait derrière elle un projet refusé par son propre audit. `template-upgrade` la répète donc d'abord (`UPGRADE_REHEARSAL`) : `HEAD` est extrait dans un worktree jetable, le core prévu y est écrit et committé, et l'audit **du nouveau contrôleur** y est lancé. Ce qu'il refuse est rapporté, et `--apply` refuse tant qu'il refuse. La répétition est mesurée contre `HEAD`, quel que soit l'état du dossier de travail : chaque fichier core dont la version committée diffère de la nouvelle est écrit dans la copie jetable — un core déjà écrit sur le disque mais non committé ne la dispense de rien. Elle porte sur ce que le projet tient dans Git — un fichier amorcé mais non committé n'y est pas — et le garde-fou de commit en est exempt, puisque l'application le réinstalle elle-même : un audit qui n'échoue que sur lui est lu comme une réussite, son code de sortie compris. Le worktree est retiré quand la commande se termine, quelle qu'en soit l'issue, une exception comprise. Une commande **tuée** — signal, limite de temps d'un outil — ne retire rien : son checkout reste, enregistré dans la liste des worktrees du dépôt. Le garde-fou en crée un à chaque commit et la répétition à chaque montée ; au démarrage suivant, le contrôleur retire ceux qu'il **prouve** siens. La preuve est une marque, `PROJECT_CONTROL_THROWAWAY`, écrite dans le dossier porteur du checkout à sa création — elle nomme le dépôt et le checkout — et que la commande tient verrouillée tant qu'elle tourne : un verrou libre appartient à une commande morte, le système d'exploitation ne le rend qu'à sa fin. Ce qui est retiré : ce checkout, la marque, et le dossier porteur s'il est vide. Un worktree sans marque n'est jamais touché, quel que soit le nom de son dossier ou son âge ; un checkout dont le verrou est tenu reste, même vieux, parce qu'une commande suspendue n'est pas morte ; un fichier posé à côté d'un checkout n'est jamais retiré.

**Depuis une version trop ancienne pour connaître cette commande.** Un projet qui monte depuis une version antérieure exécute *son* contrôleur, qui ignore `--seed-required`. L'ordre qui marche, sur la branche canonique, sous le mandat qui autorise déjà l'adoption du core :

1. `template-upgrade --source <template> --apply` — le projet exécute désormais le nouveau contrôleur ;
2. `template-upgrade --source <template> --seed-required` — les fichiers manquants sont écrits ;
3. renseigner ce que la nouvelle version demande au Project Owner (langue, style de retour) ;
4. `audit`, puis committer l'ensemble sur la canonique comme adoption du core.

Vérifié de bout en bout sur un projet réel monté de la `3.6.1` à la `3.16.0`.

L’exécution s’inscrit dans un Work Item dont les `authorized_paths` couvrent les chemins core et `provenance/core-manifest.v1.json` : `preflight`, la traçabilité Git et le hook s’appliquent tels quels, et les fichiers ajoutés sont indexés explicitement (`git add -- <chemin>`). Une copie `NOT_STARTED` ne se met pas à jour : elle se remplace par une copie neuve du template.
