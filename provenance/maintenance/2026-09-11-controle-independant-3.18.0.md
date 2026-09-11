> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

1. La protection du passé reste contournable : un retrait de baseline ajouté pendant une fusion est committé sans la décision requise. Un chantier réellement terminé et figé peut ensuite être réécrit ; l'audit final passe.
2. Les contre-exemples anciens sont refusés dans leurs formes directes, mais trois autres anomalies sont démontrées : mise à jour saine du garde-fou refusée, répétition exécutant l'ancien contrôleur, fichier temporaire laissé par SIGINT qui bloque la reprise.
3. Aucun correctif produit. La source est conservée, les scénarios et journaux restent dans `runs/`. Les résultats de la suite livrée et ceux des expériences indépendantes sont distingués ci-dessous.

# Contrôle du squelette 3.18.0 — quatrième passe

## 1. État exact et périmètre

Contrôle exécuté le 11 septembre 2026. Racine accordée : `~/Projets/squelette-controle-3.18.0/`. Tous les chemins relatifs de ce rapport partent de cette racine. `source/` a servi uniquement à la lecture et au clonage ; les expériences, temporaires et journaux sont dans `runs/`. Le seul livrable à la racine est `CONTROLE_SQUELETTE_3.18.0.md`.

La source est propre sur `main`, au commit `4b44cc85a000cd5c4a2ea278c2f2d420c478dddb`. Le tag `v3.18.0` désigne `df551cc9ebe1973c0ee3286aa2a15a0a68be42c4`. Les deux fichiers qui diffèrent entre tag et HEAD sont `provenance/ROADMAP_VIEW.md` et `provenance/roadmap-template.v1.json`, hors core. Les 24 fichiers core correspondent au manifeste 3.18.0. Les 29 tags sont disponibles, dont `v3.6.1` = `0d5d86f5960aadbb27b333fced41f6b1b4b0a37d` et `v3.17.1` = `d437c1665c1410d73e261df0c522e81dbb2bd16c`.

`status`, `audit` et `core-manifest` passent sur la copie de référence avant les essais (`runs/control/preflight.log`). Environnement : Python 3.14.0, Git 2.50.1 Apple Git-155, macOS 26.6.2 arm64. Il s'agit d'un seul environnement, pas d'une validation multi-OS.

L'inventaire de source contient **1 283 fichiers, dont 121 hors `.git` et 1 162 dans `.git`**. Contenus, tailles et permissions sont identiques avant/après ; les deux inventaires ont le SHA-256 `60d859586e373ea44af612e4342ae810da1f87ba6fd85bc993b65359704fee51`. Les dates d'accès et caches système ne sont pas attestés. Les lectures initiales précèdent l'inventaire ; aucun changement source n'a été effectué entre elles et lui.

La vérification d'assemblage compare les core dans 68 arbres actuels (soit 1632 comparaisons avec la source), sans divergence. Elle complète le registre T13 des sources historiques et artificielles, comparées à leur version attendue. Les 1310 entrées de registres relues par l'assemblage ont toutes l'empreinte annoncée (`runs/control/evidence-verification.json`).

## 2. Méthode, privilèges et écarts au protocole

Les trois rapports précédents et la fiche P17 ont été lus avant les expériences. Les contrats FIRST_START, ADOPTION, AGENTS.core, README Project Control et CHANGELOG ont ensuite été confrontés aux comportements. Quatre campagnes sont isolées : baselines (`t12`), montée (`t13`), garde-fou/concurrence (`t14-hooks`), preuves/bootstrap (`t14-local`). Un complément `t15-docs` examine séparément le parcours depuis les seuls documents et diagnostics. Leurs rapports détaillés conservent les recettes ; le présent rapport retient les preuves décisives.

Les autorisations du mandat couvrent les clones, écritures, exécutions, commits, installations de gate et push local. **Aucun refus de l'outillage ni contournement d'un tel refus.** Les refus du produit constituent les résultats des essais. Aucun accès réseau. Le seul push est celui du test de sauvegarde livré, vers `runs/remote.git` ; aucun push vers un autre dépôt.

La première lecture du fichier explicitement désigné par l'utilisateur a eu lieu à son chemin hors racine : `~/Projets/Squelette V3 -runtime-proof/Claude outputs/MANDAT-CONTROLE-SQUELETTE-3.18.0-passe-4.md`. C'est l'entrée autorisée nécessaire pour connaître le mandat. Après cette lecture, aucun autre projet extérieur n'a été consulté. Les exécutables et bibliothèques système sont utilisés ; le contrôle ne prétend pas enfermer leurs caches ou accès internes dans ce dossier.

Les configurations Git globale/système sont neutralisées dans les lanceurs et les identités de commits sont fictives ; TMPDIR reste dans chaque campagne et le bytecode Python est désactivé. **Exception observable : le contrôleur enlève les variables `GIT_*` de l'environnement du sous-processus de répétition.** L'isolation par ces variables n'est donc pas héritée par ce sous-processus ; aucune absence absolue d'influence d'une configuration système n'est revendiquée.

Les helpers livrés servent à préparer certaines initialisations et certains arguments/records. Leur WI-000 DONE est synthétique : il ne compte jamais comme cycle indépendant. Les créations, démarrages, intégrations, clôtures et commits invoqués comme preuves passent par le produit intact. Les programmes ERROR/traceback/unittest sont réellement exécutés ; les variantes d'encodage sont des octets synthétiques. Les décisions sont des fixtures sans autorité réelle hors des copies. L'authenticité humaine, expressément exclue par le mandat, n'est pas attaquée.

Les dérogations de préparation sont déclarées : passage FIRST_START à COMPLETE, préparation de certaines déclarations historiques et adoption canonique d'un ancien core. **Aucune dérogation au hook ni plomberie Git de contournement ne fonde le défaut de fusion, les refus de montée ou le défaut SIGINT.** Les tests livrés qui vérifient eux-mêmes l'override restent des tests livrés. Le commit jetable de répétition utilise l'exemption interne prévue par le produit, pas un contournement ajouté par le contrôle.

Les signaux sont réels. Une trace Python externe suspend le contrôleur intact aux fenêtres précisées, puis le harnais envoie SIGINT/SIGCONT, SIGTERM ou SIGKILL. Elle ne remplace ni fonction ni donnée du contrôleur. Les scénarios de fusion et les deux anomalies de montée sont d'abord reproduits sans instrumentation. Les sources fictives 3.18.1 de T13 injectent un commentaire de hook, un changement documentaire, un crash ou une attente ; elles ne sont pas des versions publiées ni des correctifs proposés.

**Erreurs de préparation conservées.** Un script de fixture nommé `traceback.py` a masqué la bibliothèque Python lors des deux premiers essais unittest ; les reprises `-I` fournissent les mesures valides. Les cinq premières variantes encodées portaient un horodatage futur et n'ont donc testé que son refus ; leurs reprises utilisent l'heure courante. L'ancien 3.6.1 ne connaît pas `install-gate` : après ce refus de saisie, son installation documentée par `core.hooksPath scripts/hooks` a été utilisée. Ces traces ne sont pas attribuées au produit. Aucun journal n'est supprimé pour embellir les résultats.

Le harnais de finalisation T14-hooks cherchait la clé `files` au lieu de `core` dans le manifeste : `runs/t14-hooks/verification.json` contient donc zéro comparaison de core. La mention contraire de son sous-rapport n'est pas retenue comme preuve. La vérification indépendante d'assemblage compare effectivement les 13 arbres concernés, soit 312 fichiers, sans divergence (`runs/control/core-copies.json`).

Les harnais sont des carnets exploratoires avec destinations conservées, pas des lanceurs globaux idempotents. Rejouer une expérience exige une nouvelle copie nommée ; relancer `close` sur un WI déjà DONE ne rejoue pas sa création. Les commandes, répertoires, sorties et codes retour sont conservés par campagne. Les tableaux d'empreintes et rapports sont des index ; les journaux d'exécution restent les preuves primaires.

## 3. Vérifications thème par thème

### T-12 — Protection du passé

| Attaque ou témoin | Résultat indépendant |
|---|---|
| Champ de décision absent, mauvaise famille, duplicata non vide identique ou contradictoire, champ dans une autre décision, ancrage réécrit vers un autre SHA | Audit et vrais commits refusés. |
| Champ exact, ligne vide supplémentaire ou champ dans un bloc de code | Acceptés ; les deux derniers sont des tolérances de parsing. |
| Décision REJECT, DEFER ou REJECT puis AUTHORIZE avec ancrage exact | Audit et commits acceptés ; portée précisée en section 5. |
| Retraits/malformations : null, chaîne, liste, objet vide, head invalide, false, champ absent, pour chaque baseline | 14 vrais commits refusés ; HEAD conservé. |
| Déplacement en arrière vers un ancêtre | Audit seul accepté, commit ordinaire refusé. |
| Branche latérale non intégrée, commit orphelin, chaîne littérale HEAD | Audits et commits refusés. |
| Avance canonique sous nouvelle décision exacte | Audit et commit acceptés. |
| Branche précréée au mauvais tip / au tip canonique attendu | Start refusé sans mutation / start réussi. |
| Project State ajouté comme nouveau chemin pendant fusion | Vrai commit refusé. |
| Contenu de Project State déjà touché par la branche, puis retrait ajouté pendant fusion | Vrai merge accepté ; historique devenu réinscriptible. |
| Même voie de fusion pour recul ; authorities seule depuis worktree lié | Vrais commits et audits acceptés. |
| Nouvelle décision dite de confirmation nommant un autre commit exact | Audit et commit acceptés ; l'égalité avec l'ancienne cible citée en prose n'est pas vérifiée. |

Les matrices se trouvent dans `runs/t12/matrix-result.json`, `ancestry-result.json`, `extra-paths-result.json` et `preexisting-branch-result.json`. Les recettes et leurs limites sont détaillées dans `runs/t12/REPORT.md`.

Le scénario décisif concerne **un vrai DONE**, obtenu par création, start, écriture documentaire, commit, merge et close de WI-002. Une décision HD-205 nomme ensuite son commit exact ; WI-003 avance légitimement la baseline et se clôt. WI-004, autorisé sur Project State, est refusé lorsqu'il retire directement la baseline. Il committe alors seulement un changement de langue, puis le retrait est ajouté pendant sa fusion. Le vrai merge accepte, ainsi que la réécriture ultérieure de l'objectif de WI-002 sur main. `authorities_baseline` reste présente dans cette version renforcée du contre-exemple. F12-01 détaille les preuves.

### T-13 — Répétition de montée

| Scénario | Résultat indépendant |
|---|---|
| Source identique ; source documentaire écrivant effectivement deux core | Répétition/application réussies. |
| Seul hook actualisé par un commentaire | Refus erroné sur projet équipé ; même source acceptée sur fixture jamais équipée. F13-01. |
| Nouveau contrôleur qui plante | Refus, core cible intact, worktree de répétition retiré. |
| Nouveau contrôleur qui attend | Refus après le délai réel de 600,270 secondes ; fichiers, HEAD, index et liste de worktrees identiques avant/après. |
| Dépôt sans HEAD | Refus explicite avant application. |
| Index principal verrouillé | Répétition/application possibles via index distinct ; verrou initial conservé. Cela ne prouve pas que le commit final soit possible tant que ce verrou reste présent. |
| Index du worktree de répétition verrouillé | Refus, aucun résidu de worktree ni du verrou injecté. |
| Métadonnées worktrees indisponibles ; chemin de répétition occupé | Refus, pas de core cible écrit ; nettoyage de la répétition. |
| Worktree lié préexistant ; commande depuis worktree lié | Répétition réussie, worktree préexistant conservé. |
| Fichier requis amorcé mais non committé, même indexé | Répétition refusée : HEAD reste la frontière annoncée. |
| Nouvelle commande après ancien apply, avant commit | Elle annonce l'audit du nouveau contrôleur mais exécute encore l'ancien HEAD. F13-02. |
| SIGINT durant audit de répétition | Worktree retiré ; reprise possible. |
| SIGTERM du groupe pendant répétition | Worktree orphelin ; core cible intact ; nouvelle commande possible, orphelin conservé. |
| SIGINT entre écriture de core et manifeste | Restauration exacte, reprise réussie. |
| SIGKILL à la même fenêtre | État partiel, divergence de core détectée, reprise directe refusée. Limite d'arrêt non interceptable. |
| Répétition sans apply | Fichiers, index, HEAD et refs conservés ; objet de commit jetable encore retrouvable par `fsck`. |

La documentation annonce la frontière des fichiers **committés** dans le paragraphe de répétition et demande de committer les fichiers amorcés avant apply. Les refus du fichier seulement présent/indexé sont conformes. Elle présente néanmoins la répétition assez globalement dans ADOPTION ; le README explique ensuite la procédure depuis une ancienne version. Le vrai 3.17.1 et le vrai 3.6.1 ne répètent pas : cette limite connue est confirmée, sans être transformée en nouvelle anomalie.

Un projet autonome né du tag 3.6.1 a terminé WI-001, puis suivi l'adoption canonique publiée : ancien apply, nouveau seed-required, choix langue/style, installation, indexation explicite, audit et commit. Les deux baselines avaient été déclarées avec leurs SHA exacts avant la montée, sous décisions fictives préparatoires. WI-002 est ensuite réellement terminé sous 3.18.0. Les trois records anciens comparés restent identiques, dont WI-001 et son Run réellement exécutés ; WI-000 demeure synthétique. Ce parcours est plus petit que les quatre chantiers métier de la seconde passe et ne prétend pas les répliquer intégralement.

### T-14 — Les onze corrections ensemble

| Correction antérieure | Reproduction en 3.18.0 et portée |
|---|---|
| Brouillons validés par leurs notices | DRAFT/PROPOSED refusés au closeout ; documents réellement validés acceptés. |
| Close relisant mal un mandat figé | REJECT figé : audit, actualisation de lecture et close refusent expressément l'autorisation ; WI reste IN_PROGRESS. |
| Vrai test positif avec diagnostic ERROR refusé | Unittest réellement code0, ERROR et errors=1 attendus : DONE et audit PASS. |
| Preuve PASS citant un programme mort | ERROR seul et traceback réellement code1 : close refuse. Unittest FAILED : refus également. |
| Ancienne montée sans issue administrative | Parcours réel 3.6.1 → 3.18.0 terminé avec la procédure d'amorçage actuelle, puis nouveau cycle terminé. |
| Installation au mauvais endroit en worktree | Hook installé au chemin commun effectivement consulté ; vrai commit interdit refusé. |
| Snapshot d'index indisponible laissant passer | Index invalide/disque honnête : vrais commits refusés avec snapshot disponible puis indisponible. |
| Passager masqué dans une fusion | Nouveau chemin hors scope, indexé puis absent du disque : refus ; fusion propre acceptée. |
| Sessions perdant les écritures de l'autre | Deux créations concurrentes réussissent, checkout cohérent. Un concurrent attend bien le verrou pendant l'interruption de l'autre. Défaut distinct de temporaire : F14-01. |
| Projet privé de `.gitignore` | Absence refusée avant closeout ; écriture permise en bootstrap ; rétablissement suivi d'une vue et d'un audit réussis. |
| Ligne du passé retirée puis refixée | Forme directe arrêtée au retrait, mauvais ancrage refusé. Variante par contenu ajouté pendant fusion encore acceptée : F12-01. |

Les deux sessions qui committent depuis deux worktrees voient leurs décisions locales dans HEAD : A, mandaté pour le retrait, committe ; B, sans mandat, est refusé par `BASELINE_CHANGE_MANDATED`. Pour construire cet état par les transitions réelles, A avait été bloqué sur main avant le démarrage de B ; son worktree garde son ancien IN_PROGRESS. Aucun mélange de décisions ni deux candidats actifs dans l'état canonique ne sont démontrés. L'acceptation du commit A n'est pas une intégration de sa branche bloquée.

**Autre test dépendant d'un dossier ignoré : oui.** Dans un clone intact, `test_a_new_not_started_copy_passes_bootstrap_audit` et `test_all_json_and_schema_documents_parse` passent. Ajouter seulement `Claude outputs/incomplete-download.json`, contenant `{"download":`, laisse Git propre et le fichier ignoré. Les deux tests inchangés échouent ; le premier a recopié le fichier par `make_copy` et échoue à JSON_SYNTAX. Retirer ce seul fichier fait repasser le premier test. C'est une dépendance démontrée de la fabrique de fixtures et du scan JSON, distincte de la correction particulière du `.gitignore`.

**Suite livrée, résultat séparé.** **149 tests exécutés, 149 réussis, aucun ignoré**, en 652.678 secondes : `runs/control/suite.log`. Les assertions et fichiers produit sont inchangés.

Le lanceur importe les tests inchangés d'une copie. Seules les destinations du `git init --bare` et du `remote add backup` du test de sauvegarde sont remplacées par `runs/remote.git` ; le push reste réellement exécuté et sa destination est vérifiée. Les substitutions sont imprimées aux lignes 59–61 de `runs/control/suite.log`. C'est toute la suite avec adaptation de confinement, pas la commande de découverte strictement inchangée. Une suite verte ne réfute aucun des contre-exemples indépendants.

### T-15 — Reprise des anciens « non vérifié »

Un agent de contrôle distinct a construit un export réel `git archive` de 121 fichiers, `.gitignore` inclus, puis un dépôt Git autonome. À partir des documents Markdown, de l'aide CLI, des diagnostics et de ses propres records générés, il a terminé FIRST_START puis le premier WI documentaire : create, start, commit, merge, close DONE ; audit, status et core-manifest passent, main est propre.

Aucun schéma, modèle de fixture, helper de tests ni logique Python du produit n'a été lu par ce volet. Le routage `mandatory-documents.v1.json` a été consulté, et il exige justement des schémas pour le scope gouvernance. Le succès est donc celui d'un **parcours technique Markdown + CLI + diagnostics**, sans modèles annexes ; il ne prouve ni un parcours strictement limité aux fichiers `.md`, ni le respect de toute la lecture prescrite, ni un onboarding humain aveugle. Cette limite ne doit pas être effacée par le succès technique.

Le rapport `runs/t15-docs/REPORT.md` conserve les diagnostics de préparation et l'ambiguïté du message de create-work-item en bootstrap : la commande annonce un commit atomique, mais les records restent alors non committés comme le prévoit son mode. Ce message imprécis est séparé des quatre anomalies retenues.

Le tableau de la section 6 reprend les trois listes antérieures point par point, en regroupant seulement leurs recouvrements explicites. Les nouvelles mesures comprennent aussi deux gates de preuve locales supplémentaires : `runtime_proof` et `deployment` en cible contrôlée refusent une sortie ERROR réelle, puis acceptent la preuve de copie/relecture locale réussie. Il s'agit du traitement de preuves et de niveaux par le contrôleur, sans déploiement de production.

## 4. Constats classés par gravité

### F12-01 — Majeur, P1 : une fusion permet de retirer ou reculer la baseline sans le contrôle prévu

**Promesse affectée :** la ligne du passé ne quitte ou ne déplace sa référence que sur la décision requise ; les travaux terminés à la baseline restent figés. Le défaut porte sur le contenu d'un chemin déjà inclus dans la fusion. L'ancien test de passager ferme l'ajout d'un nouveau chemin, mais pas cette modification supplémentaire de contenu.

Scénario exécuté dans `runs/t12/real-history/` :

1. Terminer réellement WI-002 (`close` : `runs/t12/logs/0081-python3.14.log`). Son commit DONE est `f32225881aeac8c48f80b7db60e9335fa987ce51`.
2. Enregistrer HD-205 nommant ce commit, avancer la legacy baseline par WI-003 autorisé sur Project State, intégrer et clore ce chantier. Il s'agit d'une déclaration/avance légitime avec gate active.
3. Démarrer WI-004 autorisé sur le même fichier. Le retrait direct `legacy_baseline=null` est refusé sur sa branche (0100), puis sur la canonique (0106). Ces témoins n'avancent pas HEAD.
4. Repartir du même état et committer sur la branche uniquement `language: FR → EN` (0103). Le fichier Project State fait désormais partie des chemins de cette branche.
5. Sur main, préparer `git merge --no-ff --no-commit <branche WI-004>`. Ajouter dans le résultat `legacy_baseline=null`, sans champ `Legacy baseline removed` dans une décision du chantier. Indexer explicitement Project State puis effectuer le vrai commit.
6. Le merge est accepté (0110), commit `3a1a640f046e36b766384e89bcd0c34d24642bb7`. Audit PASS (0112).
7. Modifier sur main seulement l'objectif de WI-002 anciennement figé. Le vrai commit est accepté (0114), HEAD `d24f0af8b1b69b47a595466c77f6ed009ebbb13b` ; audit final PASS (0115).

Le SHA-256 du WI historique passe de `11ceaa53a2043c9db03da7cd48c493e4257baa35669ad19a2327d842592e71d7` à `df0a610f324e180a2138b459c3d2399d0a28b1958f65090c1426f61223376852`. L'authorities baseline est conservée ; seule legacy est retirée dans cette reproduction renforcée. Le contrôle est également reproduit avec les deux baselines puis avec authorities seule depuis un worktree lié. Une variante de fusion fait **reculer** la legacy baseline : même absence de comparaison au moment du merge.

Privilèges : contributeur autorisé à écrire Project State et à intégrer son chantier, capable de modifier le résultat de la fusion. Gate active, core intact, aucun override, aucune réécriture de l'historique Git. Les commits anciens demeurent récupérables : la perte concerne leur statut de référence intouchable dans le contrôle courant. Cette preuve ne prétend pas avoir clos une seconde fois WI-002 ; sa réécriture après vrai DONE suffit au constat. La variante qui ajoutait Project State comme un **nouveau** chemin de fusion est correctement refusée.

### F13-01 — Modéré, P2 : une mise à jour saine du hook est refusée par la répétition

Depuis un projet normal 3.18.0 audité et équipé, une source fictive 3.18.1 ne change qu'un commentaire du hook et son manifeste. Son contrôleur reste identique. `template-upgrade --apply` classe le hook UPDATED, puis refuse la répétition (code1), tout en conservant les fichiers, HEAD et index du projet.

Le même upstream passe sur une fixture qui n'a jamais eu de hook installé ; l'installation puis l'audit réussissent. Il n'a pas été nécessaire de retirer une protection pour préparer ce témoin. L'audit interne isolé expose un seul FAIL, `COMMIT_GATE` : nouvelle référence contre ancienne copie installée. La répétition filtre ce FAIL mais réinterprète son code retour1 en échec générique, citant même une ligne PASS de traçabilité. L'exemption annoncée, destinée à permettre la réinstallation après apply, ne produit donc pas l'effet promis.

Preuves : `runs/t13/logs/0029-changed-hook-python3.14.log`, `boundary-logs/0018-changed-hook-diagnostic-python3.14.log`, témoins `extra-logs/0032-changed-hook-never-installed-python3.14.log` et `0038-changed-hook-never-installed-python3.14.log`. Impact : montée légitime bloquée, pas corruption ni acceptation indue.

### F13-02 — Modéré, P2 : une nouvelle répétition annonce le nouveau contrôleur mais exécute l'ancien HEAD

Un projet 3.17.1 contient une baseline valide selon son ancien contrat, sans confirmation au format nouveau. Son ancien apply vers 3.18.0 réussit sans répétition : c'est la limite connue, pas le défaut. Le nouvel audit refuse ensuite la baseline comme attendu.

Sans committer la montée, relancer maintenant le **vrai contrôleur 3.18.0** avec le même `template-upgrade --apply`. Il annonce `UPGRADE_REHEARSAL PASS` et `APPLY PASS`. Le nouvel audit réel refuse toujours le même état. Les 24 core sont déjà IDENTICAL sur le disque, donc la liste de fichiers à copier dans le worktree est vide ; HEAD contient toujours le contrôleur 3.17.1, que le sous-processus exécute. Le manifeste neuf seul ne rend pas ce contrôleur neuf.

Preuves successives : `runs/t13/extra-logs/0013-historical-3.17.1-python3.14.log` (ancien apply), `0017-historical-3.17.1-python3.14.log` (nouveau refus), `0021-historical-3.17.1-python3.14.log` (nouvelle répétition faussement positive), `0025-historical-3.17.1-python3.14.log` (nouvel audit encore refusé).

Ce constat démontre un faux succès lors d'une relance avant commit. Il **ne démontre pas** qu'une première montée propre exécutée par 3.18.0 a créé cette baseline invalide : elle était déjà refusée après l'ancienne commande. C'est précisément la promesse d'exécuter l'audit du nouveau contrôleur que la relance viole ; aucun record non committé ne distingue ici les deux audits.

### F14-01 — Modéré, P2 : SIGINT laisse un temporaire qui bloque la reprise

Dans une copie propre et équipée, lancer `create-work-item`, puis suspendre juste avant `os.replace`, après écriture, fsync et fermeture du temporaire de HUMAN_DECISIONS. Envoyer SIGINT puis SIGCONT. Le contrôleur est intact, la trace externe n'a fait que placer le signal dans cette fenêtre.

Le processus termine par KeyboardInterrupt. HEAD, index et fichiers préexistants sont conservés, mais `docs/governance/.HUMAN_DECISIONS.md.<aléa>` reste non suivi. Audit et nouvelle création refusent ce chemin inexpliqué. Le scénario est reproduit avec un concurrent puis sans concurrent. Dans le premier, B attend correctement le verrou de A, puis refuse le temporaire ; aucun succès B n'est écrasé.

Témoin : interrompre après la première écriture complète, avant celle de Conversation. Cette fois le snapshot est identique, audit et nouvelle création réussissent. Le défaut se situe dans le nettoyage du temporaire d'écriture, pas dans la libération du verrou ni dans une perte de records.

Preuves : `runs/t14-hooks/logs/interrupt-single-A.log`, `0133-python3.14.log`, `0134-python3.14.log` ; témoins `interrupt-after-write-A.log`, `0158-python3.14.log`, `0159-python3.14.log`. Impact borné : checkout sale et reprise bloquée ; aucune perte irréversible ni autorisation indue.

## 5. Observations non bloquantes et hypothèses restantes

- L'ancrage d'une baseline valide l'égalité d'un champ avec le SHA et sa famille. Les essais acceptent néanmoins une décision de baseline portant REJECT, DEFER ou des choix contradictoires dès que le champ est exact ; un champ placé dans un bloc de code est également lu. DEFER et les choix contradictoires ont été testés par réécriture d'une décision déjà citée ; une nouvelle déclaration effective sous REJECT a aussi été acceptée. Ces observations de parsing restent distinctes de l'exigence AUTHORIZE des transitions. Elles ne sont pas présentées comme une preuve d'authenticité humaine.
- La confirmation d'une ancienne baseline ne vérifie pas sémantiquement sa citation d'origine : une prose disant confirmer l'ancienne cible avec un champ exact visant une cible plus récente est acceptée. L'avancement a bien un champ qui nomme son SHA ; l'identité sémantique de « confirmation de l'ancienne » n'est pas attestée.
- Le recul vers un ancêtre est acceptable pour l'audit pris isolément, qui juge l'état courant ; le commit ordinaire le refuse en comparant HEAD. La variante de fusion de F12-01 met en défaut cette seconde barrière. Les deux contrôles ne doivent pas être confondus.
- Un OK de préparation suivi d'un crash réel peut encore être cité comme pièce unique d'une preuve PASS et permettre DONE. Limite textuelle déjà publiée, distincte du défaut ancien ERROR sans aucune réussite. UTF-16, UTF-8 invalide et binaires testés conservent aussi leurs limites de lecture.
- Un fichier ignoré peut influer sur la suite par `make_copy` et le scan JSON. La preuve A/B/A ne dit rien sur les performances de tous les dossiers ignorés ni sur toutes leurs sortes de contenus.
- Après répétition, le commit jetable reste retrouvable comme objet Git sans branche/tag. SIGTERM pendant répétition et SIGKILL pendant vraie gate peuvent laisser un worktree orphelin. Les reprises testées restent possibles. « Retiré quoi qu'il arrive » et « rien n'est écrit » doivent donc être compris avec ces limites, sans les transformer en garanties de nettoyage forensique.
- SIGKILL pendant l'application laisse une mise à jour partielle détectée comme dérive ; aucun rétablissement automatique n'est démontré. SIGINT au même point restaure correctement. Aucun test d'épuisement par accumulation d'orphelins n'a été exécuté.

Aucune hypothèse sans scénario exécuté ne fonde les quatre constats. Les extensions à tous les hooks tiers, sources malveillantes, configurations Git, signaux et ordonnancements restent des hypothèses ou limites de couverture. Aucun correctif ni proposition de code produit n'accompagne ce rapport.

## 6. Ce qui n'a pas été vérifié, et pourquoi

Les références A, B et C désignent respectivement les listes des rapports 3.15.2, 3.15.3 et 3.16.2. « Vérifié » signifie une mesure dans cette passe, avec ses limites ; un ancien résultat n'est pas recompté comme une nouvelle exécution.

| Point de l'ancienne liste | Vérifiable aujourd'hui / traitement et limite restante |
|---|---|
| A1 — Historique réel, tags et HEAD absents ; montée ancienne impossible | Entrée historique désormais présente, tags/HEAD vérifiés. Projet autonome 3.6.1 → cible actuelle 3.18.0 avec cycles avant/après exécuté. Le saut exact vers l'ancienne cible 3.15.2 n'est pas présenté comme rejoué. |
| A2 — Essais indépendants de garde-fou bloqués par l'outillage | Les trois trous, snapshot, worktree et interruption de gate sont maintenant essayés par vrais commits autorisés ; aucun refus d'outillage. L'interruption d'installation est vérifiée par audit MISMATCH, réinstallation et commit interdit après réinstallation ; aucun commit n'a été tenté pendant la fenêtre où le hook n'était pas exécutable. |
| A3 — Test de push exclu de la suite | Tous les 149 tests exécutés ; push réel vers le bare autorisé. L'adaptation de destination interdit de qualifier l'invocation de strictement identique à l'ancienne commande brute. |
| A4 — Tous formats et épuisement mémoire | UTF-16, UTF-8 invalide, ANSI précis, binaire, vide et sortie de 2,85 Mo vérifiés. Exhaustivité et saturation non établies : cet échantillon ne les représente pas. |
| A5 — Runtime/déploiement, production, réseaux, authenticité, signatures | Gates runtime/déploiement contrôlées avec sous-processus et copie/relecture locale ; aucune preuve de production. Réseau interdit et aucune cible externe fournie. Identité humaine, signatures et vérité métier ne sont pas attestables par fixtures. |
| A6 — Initialisation sans modèles annexes | Parcours technique sans schémas ni helpers réalisé par un volet séparé ; routage JSON et diagnostics utilisés. Strict Markdown seul et onboarding humain restent non démontrés ; le routage exige lui-même des schémas. |
| A7 — Toute écriture interne Git d'une commande lecture seule | status/audit/core-manifest comparés sur 1 379 fichiers, `.git` compris : aucun contenu ni mode changé. Répétition : objet Git résiduel démontré. Dates d'accès, écritures transitoires et caches OS non observés. |
| A8 — Préfixes d'avertissement, JSON/binaires et ancien écart hors dossier | Cette exigence de préfixe pour chaque fichier n'est pas reprise dans le présent mandat. Fixtures identifiées dans scripts/dossiers, formats bruts conservés. Les anciens incidents ne sont pas des événements que cette passe peut réexécuter ou effacer. Lecture initiale du mandat hors racine déclarée en section 2. |
| B1 — Exploitation réelle sur plusieurs jours/personnes | Toujours non attestée : les cycles et dates de fixture ne représentent pas un mois d'usage. Aucun projet métier réel extérieur n'est accessible dans le périmètre. |
| B2 — Onboarding humain aveugle et consentement réel | Parcours indépendant assisté par documents/CLI, pas une interview humaine. Les décisions fictives ne prouvent aucun consentement extérieur. |
| B3 — Toutes interruptions et pannes OS | SIGINT, SIGTERM et SIGKILL ciblés, pendant transaction, installation, gate, répétition et application, sont couverts. Coupure de courant, saturation disque et toutes fenêtres possibles ne le sont pas ; les signaux ne leur sont pas assimilés. |
| B4 — Toutes configurations hooksPath/worktrees/snapshots | Mode historique dans l'adoption 3.6.1, mode installé actuel, hook commun, branche liée nommée, tip incorrect et obstacle worktrees vérifiés. Tous hooks tiers, signatures, ACL et topologies ne sont pas épuisés par ces configurations. |
| B5 — Runtime/déploiement et authenticité métier | Même extension locale et mêmes limites que A5. Aucun niveau PRODUCTION_VERIFIED issu de ces fixtures locales n'est revendiqué comme preuve de production. |
| B6 — Matrice UTF-16/ANSI/binaires et anciens thèmes | Matrice bornée A4 ; les onze corrections et interactions demandées sont reprises en T14. Les thèmes sans lien avec T12–T15 ne sont pas redémontrés. |
| B7 — Effets internes des runtimes et caches | Mêmes observations et limites que A7 ; les inventaires n'attestent pas les dates d'accès ni chaque écriture transitoire. |
| B8 — Toutes versions intermédiaires, quatre chantiers métier et scripts anciens | Les tags existent, mais les anciens dossiers runs et programmes métier exacts ne sont pas fournis ici. Le parcours actuel recrée un cycle documentaire avant/après ; il ne réplique ni les quatre programmes de l'ancienne campagne ni chaque saut de version. |
| C1 — Finder, préférences d'affichage, ACL/quarantaine/xattrs | Le vrai export Git et son `.gitignore` sont vérifiés. L'interface Finder et les métadonnées spécifiques macOS n'ont pas été pilotées/mesurées ; aucune session graphique confinée ni sélection humaine n'entre dans les preuves. La reproduction au niveau des fichiers ne vaut pas validation du Finder. |
| C2 — Usage durable à deux humains ou LLM, probabilités de course | Deux processus, deux worktrees et des ordonnancements bornés testés. Pas de mesure statistique ni d'usage humain de longue durée. |
| C3 — Toutes combinaisons concurrentes block/resume/close et pannes | Créations simultanées, SIGINT/rollback, blocage réel séquentiel préparatoire et deux commits de retrait avec/sans mandat couverts. La matrice complète des transitions entre worktrees ne l'est pas ; le nombre borné de courses ne démontre pas tous les ordonnancements. |
| C4 — Authenticité humaine et horodatages de témoignages | Limite connue expressément exclue par le mandat ; pas de tentative de la redémontrer. Les refus d'horodatage futur de préparation sont conservés, sans prétendre authentifier un auteur. |
| C5 — Répétition intégrale des quatre cycles métier anciens | Même limite que B8 ; un cycle ancien réel, un nouveau réel, préservation de trois records, dont WI-000 synthétique clairement distingué. |
| C6 — Déploiement/runtime, encodages, épuisement mémoire, réseau/production | Traitement A4/A5 : extension locale réalisée ; saturation, réseau interdit et production restent exclus. |
| C7 — Effets internes système, caches et dates d'accès | Même traitement A7. |

Autres limites propres à cette passe : aucune seconde clôture du même ancien WI n'a été exécutée après F12-01 ; sa réécriture après vrai DONE est, elle, prouvée. Une baseline visant le commit qui contient son propre SHA n'a pas été construite : cela demanderait un auto-référencement de l'identifiant cryptographique, contrairement au simple SHA d'un HEAD déjà connu qui a été testé. Aucune confirmation réelle d'Alpha n'a été lue hors périmètre. Aucune source malveillante, panne matérielle ni généralisation à tous les systèmes n'est homologuée.

Les copies refusées, les merges volontairement non terminés, les obstacles injectés et les worktrees orphelins restent des preuves. Ils ne sont pas nettoyés pour améliorer artificiellement les états finaux.

## 7. Registre des preuves décisives

Les lignes sont physiques, comptées depuis 1 ; les SHA-256 portent sur le fichier entier. Les registres détaillés de `runs/t12/`, `runs/t13/`, `runs/t14-hooks/`, `runs/t14-local/` et `runs/t15-docs/` complètent cette sélection. Les sorties qui indiquent un échec sont conservées, ainsi que les erreurs de préparation identifiées en section 2.

| Objet | Chemin | Lignes | SHA-256 |
|---|---|---|---|
| État, tags, audit initial | `runs/control/preflight.log` | 1–136 | `d993fcd5690345e3d050f47f503704f875f255e83158fd503e995250f2919d79` |
| Source avant/après | `runs/control/source-verification.json` | 1–8 | `ec16fbea30ed978958387f35b4797c920713b0dd5092a35fc8d557dd4b92ea66` |
| Registres recroisés | `runs/control/evidence-verification.json` | 1–5 | `946db75a3511c236735bf57dfc8cc75232d0c93379ddde6a6ba4ba4ca55e342c` |
| Core des copies | `runs/control/core-copies.json` | 1–4 | `bcf3c7440d73f61ecdbd4642ba940988ccc7b55a33738fab1e6df32329fe346f` |
| Suite entière | `runs/control/suite.log` | 1, 59–61, 207–210 | `7803619e19f19ec3db0fe24ff1fccf943e7557aea9fc143cf226c8986db881b4` |
| Push unique / refs reçues | `runs/control/remote-final.log` | 1–6 | `4e7d755c6aa7899e6165f66066220e1fc896241ff3febb5b72b5a2fa0efef245` |
| F12 vrai DONE | `runs/t12/logs/0081-python3.14.log` | 1–15 | `4236c798fc30905dd2a9ed56584bd3f34a49807dc54b6ac99d9788b861953630` |
| F12 avance mandatée | `runs/t12/logs/0091-git.log` | 1–20 | `e7c71671a2800903a522cc83f1c90ba5782ce7b11f3a63dad39a021836dae0fd` |
| F12 refus branche | `runs/t12/logs/0100-git.log` | 1–18 | `2d7cfca5c59773787ea5616e6f7669b9707e4b33c7aa813bde0fbb0dc949d525` |
| F12 refus canonique | `runs/t12/logs/0106-git.log` | 1–16 | `f14fe5f08c26889c292160847e14012f432d71a5d21a5c7dd9e1801042c3817f` |
| F12 merge accepté | `runs/t12/logs/0110-git.log` | 1–16 | `91feafe3c06e05e2502878d924dfebbcdeb96d0628fa475a9e8a96191fdd56eb` |
| F12 histoire réécrite | `runs/t12/logs/0114-git.log` | 1–18 | `e801c29e038b93411c2a9c72ead8336dec72f39b2ee9fd3268551cba248d82b3` |
| F12 audit final PASS | `runs/t12/logs/0115-python3.14.log` | 1–35 | `74f079eb0c1329f7178af9b8ae75bb5bdb99a32bf41f257c26a8bb712003cce1` |
| F12 recul par merge | `runs/t12/logs/0348-git.log` | 1–16 | `5a753b424eb6c6ec168d71ff1583bb9519f244ea96021c0783b73e2d2188dbdb` |
| F12 worktree authorities | `runs/t12/logs/0400-git.log` | 1–16 | `96e404d0a373d27ab1b1817d9a28186e15a3e4d1b1b70434ef3861efeb994233` |
| F12 branche mauvais tip | `runs/t12/logs/0416-python3.14.log` | 1–15 | `9170c80f7e2d83b44707250693f98fbc31e026ab85fca4602035444f049472d7` |
| F12 branche tip correct | `runs/t12/logs/0434-python3.14.log` | 1–15 | `0c29bfca4bb2a93e7d4ce9f347f19c945113d91def19d7d0d84902a3a7d75c25` |
| F13 hook refusé | `runs/t13/logs/0029-changed-hook-python3.14.log` | 1–18 | `f3fbcfc8ba9b5d5511a9dc95737023224980634eea2b3df1a2b7272eb4ed1a7c` |
| F13 seul FAIL interne | `runs/t13/boundary-logs/0018-changed-hook-diagnostic-python3.14.log` | 1–47 | `932a505bc9e8dda8003ab4663a761c3d5ebdaf6b508f6fc028d5f9a6eb08f355` |
| F13 témoin jamais équipé | `runs/t13/extra-logs/0032-changed-hook-never-installed-python3.14.log` | 1–19 | `41ca3abdceb92416ca3c78bb0f9eb4dfdce47f5c8f4867685ecfb85f9ced8e63` |
| F13 ancien apply | `runs/t13/extra-logs/0013-historical-3.17.1-python3.14.log` | 1–18 | `f0fc9bee29cd7828453e0d4a8e33f933090e8e35260cda404fece5410af4b663` |
| F13 faux PASS répétition | `runs/t13/extra-logs/0021-historical-3.17.1-python3.14.log` | 1–19 | `7dcb5c3ae8622952554ae0800ba6a051c96a11ac470b0408b95a2326f95b7d44` |
| F13 audit réel refusé | `runs/t13/extra-logs/0025-historical-3.17.1-python3.14.log` | 1–33 | `a015028c3ed407d1c574802c41e3d0dc2dd8b02563ae21993073be7bd8e97ab7` |
| T13 timeout réel | `runs/t13/logs/0108-source-hang-timeout-python3.14.log` | 1–18 | `998f13f8cf8a50b6a7cac89f9004e0abc79ffae7410b9f08a81f13ed4051dfa4` |
| T13 cycle ancien clos | `runs/t13/history-resume-logs/0010-historical-cycle-python3.14.log` | 1–13 | `489d2c2d8ea07acbb8c013ecbab5c10e6539fa1079c50e39db738b146a603f3c` |
| T13 audit précommit adoption | `runs/t13/history-resume-logs/0028-historical-cycle-python3.14.log` | 1–33 | `dc750452b24a8a08986529ff0870ea5f8c24f147d67a05a41f87835ff78c2506` |
| T13 cycle après montée | `runs/t13/history-resume-logs/0040-historical-cycle-python3.14.log` | 1–13 | `7a4887d596154457f4162f516548c0687534ac8424f1a39bd6cbcc345a8ff0e7` |
| T13 histoire conservée | `runs/t13/historical-preservation.json` | 1–14 | `a2fd5a9050a37e7b3307de4c7ed373b3756f5ce6bd299d9eb252310c77ba9b6d` |
| T14 worktree installé | `runs/t14-hooks/logs/0014-git.log` | 1–16 | `cadc3bda79a3c6d78029ead822ad38afe63c90bf788686bca73c596167904333` |
| T14 snapshot indisponible | `runs/t14-hooks/logs/0036-git.log` | 1–17 | `8c20902ff003a0be998bb719ba0ac289852ff6ac12c3521cdc9aff9a64c071db` |
| T14 passager masqué | `runs/t14-hooks/logs/0065-git.log` | 1–16 | `49ec0289750b96e43c0cc9d526aaa97b0fa202fefd8c2a7662f3ec9dc5771f1d` |
| T14 audit deux créations | `runs/t14-hooks/logs/0086-python3.14.log` | 1–36 | `3fa977612ce386492d50c2672851acc8978757f4389c75af0258da14a08ab1ea` |
| F14 SIGINT seul | `runs/t14-hooks/logs/interrupt-single-A.log` | 1–40 | `833271c8c2cd4ce4cb5524575ade957a765f9efd29c133a3839233fc9480374f` |
| F14 audit après SIGINT | `runs/t14-hooks/logs/0133-python3.14.log` | 1–36 | `9b2a145b7dc8b7b53634f908240f8eba0613bca7cdec3d77515e279061fad2d5` |
| F14 reprise bloquée | `runs/t14-hooks/logs/0134-python3.14.log` | 1–16 | `f38bf747a606c1d35f1592bed2f75aa952e8f7e35f80f5acce681999ba5f9212` |
| F14 témoin reprise saine | `runs/t14-hooks/logs/0159-python3.14.log` | 1–16 | `4f6aad2fb8caca94d15ddcea29ed862edca96c599adc8a16bc62e84f96ce71fb` |
| T14 retrait mandaté A | `runs/t14-hooks/logs/0219-baseline-A.log` | 1–21 | `f29fbb9261a8836238028ba72e7e59be01ec3ea8390d16ac2a718f2248d55901` |
| T14 retrait sans mandat B | `runs/t14-hooks/logs/0220-baseline-B.log` | 1–19 | `bdcd64752a0ac69b68a5448d5a4df4bfd6619afc6399ffe2a840ffee22b5e5ba` |
| T14 brouillons refusés | `runs/t14-local/logs/0010.log` | 1–36 | `c9418c4ee3187c411c921c189d3e13d8e707ec33097b6b9d53483406980fc9ff` |
| T14 gitignore refusé | `runs/t14-local/logs/0014.log` | 1–35 | `71938f1d9c9e8f5bb38fa431e2334f09d53ae65ad2a599b6fd176b9ba1a01cbd` |
| T14 vue après rétablissement | `runs/t14-local/logs/0022.log` | 1–11 | `a7a874360c54d0a5376447434ac949b214f926c44a01312967aa67da350317cb` |
| T14 preuve ERROR refusée | `runs/t14-local/logs/0061.log` | 1–12 | `75789237f49392f2cae49342b5e7a6136bd24f3e8fd8a0a1abbcfe4a958385f3` |
| T14 vrai unittest réussi, DONE | `runs/t14-local/logs/0286.log` | 1–12 | `c5d1b109a0db0aea229d9654312cfd7cf48df05c2f6e818772aaf9a1cdcaac05` |
| T14 mandat figé REJECT refusé | `runs/t14-local/logs/0265.log` | 1–12 | `895bf33c7f6028aedaa2d895789fd6054ca19ef4586186cc68483ce40ed2ea60` |
| T14 ignored témoin A | `runs/t14-local/logs/0269.log` | 1–11 | `167dd6fee4b35723a3341578091314e74272cc334540868b92fc0ff8a7bb93b2` |
| T14 ignored échec B | `runs/t14-local/logs/0273.log` | 1–20 | `ecb5c95eee18ee7f53c3366b443caa7914ea582699014ece65919bdee7fec21f` |
| T14 ignored reprise A | `runs/t14-local/logs/0275.log` | 1–11 | `58743b32eb0408d531e0f04487b0fd20eba03505284e79981ec2edf3324f58e2` |
| T15 gate runtime refusée | `runs/t14-local/logs/0194.log` | 1–12 | `fec3dcec5ebe0e2eb187700a54754fa5a5a692aa52d0fe46dacebee99897dfe7` |
| T15 gate déploiement refusée | `runs/t14-local/logs/0228.log` | 1–12 | `34bb563b1ba5bbd79163e321156519f5d4782fe1cdb0931b4f5438f35926f9a6` |
| T15 gate runtime positive | `runs/t14-local/logs/0370.log` | 1–12 | `29c594ba5ab05b1ca369281b797f7e1d7caadca58b9071ab794255bf8e47cf5f` |
| T15 gate déploiement positive | `runs/t14-local/logs/0381.log` | 1–12 | `45c05416603feab65aa454f841326199bc041003cafbfea175e890c7c9fbb7c3` |
| T15 parcours documents | `runs/t15-docs/REPORT.md` | 1–102 | `9410f56c2e968e1c54089151a13011ef018c0f16c025c92203181a3c31e14b61` |
| T15 premier chantier DONE | `runs/t15-docs/logs/0063.log` | 1–13 | `2a14f4577875a94e3180e5593c66e5e27127cc7db6204d9a98830041d57c5c67` |
| T15 audit autonome final | `runs/t15-docs/logs/0064.log` | 1–33 | `e21bdacd1b381726fd0a1df832a51bb87c94043567fd2d56daecf32582243c7e` |
| T15 arbre source | `runs/t15-docs/logs/0069.log` | 1–7 | `c9d106674dfbbbcda0affde3d35cbe582a0c5cff985ddff03681a08580481dd6` |
| T15 arbre exporté | `runs/t15-docs/logs/0070.log` | 1–7 | `d0358f8aac6ea7d86baed9662348c8f6e4e45d2d18fcee410c17a73af4a3db66` |
| Unittest réel code0 | `runs/t14-local/logs/0280.log` | 1–12 | `1d8794661704cdef549b752199a7a8f4b6b77157d03b36210c24efcf1b66ce7f` |

Le contrôle a conservé les états dégradés et les témoins. Tous les processus de campagne et la suite sont terminés. Le dépôt nu autorisé et ses refs sont relevés dans `runs/control/remote-final.log`. `source/` est toujours identique à l'inventaire initial ; aucun correctif, commit ou écriture n'y a été fait. La conclusion repose sur F12-01, défaut majeur reproduit sur un véritable chantier clos ; les trois P2 restent distincts et documentés.

## 8. Verdict

SQUELETTE_3.18.0_REQUIRES_MAJOR_REDLINE
