> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

1. Les trois corrections ciblées de la 3.15.3 tiennent, et les 136 tests livrés réussissent. Le contrôle indépendant démontre cependant trois défauts du garde-fou de commit et une régression de cohérence des preuves.
2. Un projet réellement construit avec le tag 3.6.1 a vécu quatre chantiers jusqu’à DONE, puis a été monté vers 3.15.3. Ses clôtures historiques restent intactes. La procédure publiée ne suffit pas à terminer la montée : des fichiers obligatoires et leur ordre d’introduction doivent être ajoutés au parcours. La récupération assistée est distinguée du parcours documentaire.
3. Aucun correctif n’a été apporté au produit. Les copies, commandes, journaux, témoins et empreintes restent dans `runs/`. La source est conservée. Aucune nouvelle action du propriétaire n’est nécessaire pour consulter ce rapport.

# Contrôle du squelette 3.15.3 — seconde passe

## 1. État exact et périmètre

Contrôle exécuté le 10 septembre 2026. Racine accordée : `~/Projets/squelette-controle-3.15.3/`. Tous les chemins relatifs de ce rapport partent de cette racine. `source/` est en lecture seule ; les expériences et leurs temporaires sont dans `runs/` ; les trois pushes de campagne ont pour unique destination `runs/remote.git`.

La source est un dépôt Git complet sur `main`, au HEAD `777ef0feaa4e5ff73976236c49b4e4121df9662b`. Les 23 tags fournis sont présents. Les objets utilisés sont :

| Référence | Commit vérifié |
|---|---|
| `v3.6.1` | `0d5d86f5960aadbb27b333fced41f6b1b4b0a37d` |
| `v3.15.1` | `49bdb1ddb8b52a249f6cf8e2b21a2e7408ae2e1c` |
| `v3.15.2` | `e7747d97d7049ad76df436f102752d13113fa8a9` |
| `v3.15.3` | `ed7494b587c211663cc86487ad93e3f4ccc17645` |

`v3.6.1` est un tag annoté : son objet de référence est `78b25637b65703a720f36f2b19f4204df5696675`, distinct du commit résolu ci-dessus. Les trois autres références du tableau pointent directement vers leurs commits. Cette distinction est enregistrée dans `runs/control/meta/resolved-tags.json`.

Le HEAD source est un commit après `v3.15.3`, avec pour seule différence `provenance/ROADMAP_VIEW.md`. Le cœur du produit est identique au tag. Les 24 fichiers du manifeste 3.15.3 ont été vérifiés par empreinte ; `FIRST_START.md` utilise la normalisation du premier marqueur en `INITIALIZATION_STATUS: <PROJECT>`. Le contrôleur a pour SHA-256 `f7b5348f1a283d373866e5dbc46051196c2b473c5c6c95c434b8ef9316f6b869`, le hook `e6e5908ae426ed2857e026736434e34e9e193c32bf7af2495d30f287d32d8516`, le manifeste `9e7a77e94aefca6d6906ccd05aeca2c8ef0f8a81aecc36ed424aa8470fc0e850`.

La copie de référence passe `status --json`, `audit` et `core-manifest` avant la campagne. Cela décrit l’entrée fournie, sans remplacer les expériences adversariales. L’environnement mesuré est Python 3.14.0 et Git 2.50.1, Apple Git-155. Détails : `runs/control/meta/environment.json`, `runs/control/reference-checks.log` et `runs/control/meta/core-independent.json`.

## 2. Méthode, privilèges et écarts au protocole

Le rapport de première passe fourni dans `source/provenance/maintenance/2026-09-10-controle-independant-3.15.2.md` a été lu avant les campagnes. T-04, T-05 et T-07 ont été conduits en parallèle dans des dossiers distincts, puis leurs preuves décisives ont été relues. Les revues croisées sont conservées dans `runs/t05/REVIEW_T07.md`, `runs/t07/REVIEW_T05.md` et `runs/t07/REVIEW_T04.md`. Les 100 empreintes des registres des trois campagnes ont également été recalculées par l’assemblage principal, sans écart (`runs/control/agent-proof-checks.json`).

Les STOP 1 et STOP 2 accordés dans la session couvrent les écritures, exécutions, commits, installations de gate et pushes locaux mesurés. Aucun refus d’approbation automatique n’est survenu ; aucun contournement de l’outillage n’a été tenté. Les refus du produit sont des résultats de test, conservés avec leurs codes retour. Les scénarios ne confèrent aucune autorité réelle aux décisions humaines fictives.

**Lecture de la pièce jointe.** Le texte explicitement joint par l’utilisateur a été lu à `~/.codex/attachments/c4277305-6a14-4efa-8e7f-a7c9fb2a5e56/pasted-text.txt`, hors racine, avant utilisation du `MANDAT.md` local. C’est la seule lecture de contenu de tâche hors du dossier accordé. Aucun autre projet n’a été ouvert. Les exécutables et bibliothèques système ont servi de runtime ; le contrôle ne prétend pas enfermer leurs accès internes dans le seul dossier de projet.

Les configurations Git globales et système sont neutralisées, les identités Git sont locales et fictives, le bytecode Python est désactivé et les temporaires sont dirigés vers chaque campagne. Aucun réseau n’est utilisé. Les chemins indexés sont explicites. Aucun `--no-verify`, force push ou correctif produit. Les overrides historiques de préparation T-04 sont déclarés ci-dessous ; T-05/T-07 n’en utilisent aucun pour les mesures.

T-04 utilise l’historique réel, les documents, les schémas et les commandes, sans helpers de construction de la suite ni lecture de la logique du contrôleur pour résoudre le parcours. Les journées narratives sont simulées : tous les programmes ont réellement tourné le jour du contrôle. T-05/T-07 réutilisent des helpers livrés pour construire leurs fixtures initialisées et certains records. Leur `WI-000` DONE de préparation est écrit par helper ; il ne compte pas comme un cycle indépendant. Les transitions et commits qui fondent leurs constats sont, eux, exécutés par le produit intact.

Les faux rapports PASS, décisions historiques modifiées et mutations d’index sont intentionnels et confinés aux copies jetables. Les JSON stricts, octets exacts de journaux et métadonnées Git gardent leur syntaxe ; leur caractère fictif est établi par les dossiers, scripts et notices de campagne, sans préfixe qui fausserait les essais.

Les interruptions utilisent des signaux réels déclenchés à des points déterminés par un harnais externe, sans patch du produit. Elles ne valent pas simulation de toutes les pannes. Les erreurs de montage sont conservées : première normalisation d’empreinte FIRST_START erronée dans le harnais principal, essais de format du registre historique et injections T-04 initialement mal ciblées. Elles ne sont pas imputées à la version contrôlée.

## 3. Vérifications thème par thème

### T-04 — Projet ancien, montée et interruptions

Le tag historique a été cloné puis exporté en un dépôt autonome, sans ancêtre du squelette. Le projet conservé dans `runs/t04/project/` compte 32 commits, quatre WI DONE, seize essais arithmétiques réellement exécutés et six décisions fictives. WI-002 est bloqué après un commit de code ; WI-003 est réalisé pendant ce blocage ; WI-002 est repris par merge divergent ; WI-004 dépend de WI-002. Les registres et cinq Agent Runs ont réellement servi. Les dates Git simulent le 1er au 28 août 2026, sans prétendre qu’un mois s’est écoulé.

Le prérequis 3.6.1 a demandé les aides déclarées : schémas et modèles JSON pour le brouillon initial, génération administrative par CLI, notices actuelles pour les statuts, override documenté de clôture FIRST_START et override explicite du défaut historique de reprise. Les audits de repos et les quatre clôtures passent ensuite sous le vrai contrôleur 3.6.1. Cette préparation n’est pas qualifiée de parcours intégral sans aide.

La montée directe du cœur 3.6.1 vers 3.15.3 annonce PASS. Après réinstallation de la gate et renseignement des choix humains de langue/style, l’audit et le commit restent bloqués par trois nouveaux fichiers de projet absents. Les commandes documentées ne les amorcent pas ; les copier après la montée fait passer l’audit mais pas le commit sur la branche WI : F-T04-01. Les états avant et après cette copie sont conservés séparément dans `upgrade-documented-stopped/` et `upgrade-direct/`.

Une récupération assistée, repartant de l’état antérieur et préparant les trois modèles avant remplacement du contrôleur, termine l’upgrade sans override du commit ni de la clôture. Quatre tests fonctionnels sont exécutés après la montée ; WI-005 devient DONE, `main` est propre au commit `185632ba071d545521198edfca172d16fcf21529`, et audit/core-manifest passent.

Les quatre anciens WI sont lus `LEGACY_PRESERVED`. Les **19 fichiers historiques** — quatre WI, cinq Runs, huit rapports/pièces et deux README — gardent exactement leurs empreintes. Une contre-épreuve ajoute un seul saut de ligne à un WI figé : l’audit le refuse. Une variante écrit et committe `Chosen option: APPROVED` dans HD-001 sous 3.6.1, après le DONE de WI-001 mais avant la baseline ; l’audit 3.15.3 conserve ce bloc, le WI, son Run et ses preuves sans requalification. La modification après DONE est une construction explicite, pas un vocabulaire prétendument présent lors de la clôture initiale.

| Essai de version ou d’interruption | Résultat mesuré |
|---|---|
| Saut exact 3.15.1 → 3.15.3, en omettant 3.15.2 | Apply, installation de gate, commit, audit et contrôle du cœur réussis. |
| SIGINT après remplacement effectif du premier core, exécutant 3.15.1 vers 3.15.3 | Les core, le manifeste, HEAD et le statut Git reviennent exactement au snapshot ; la même commande reprend, puis commit/audit réussissent. |
| SIGINT pendant réinstallation automatique du hook, cœur déjà remplacé | Relance de la même commande : aucun core à réécrire, gate réinstallée, audit et commit réussis. |
| SIGKILL au milieu du remplacement depuis 3.15.1 | Contrôleur neuf, manifeste ancien ; divergence détectée par core-manifest, reprise directe refusée. Audit général reste PASS selon la doctrine de dérive locale. |
| SIGINT au milieu du remplacement exécuté par 3.6.1 | État partiel, audit et contrôle du cœur en échec ; reprise directe refusée. Limite de l’ancien exécutant, séparée de la correction actuelle. |

Le saut et la variante APPROVED gardent leur WI d’upgrade actif ; ils ne comptent pas comme deux clôtures supplémentaires. La clôture complète après montée est celle de `upgrade-recovered/`. Les 267 journaux et le registre de 317 pièces sont conservés dans `runs/t04/REPORT.md`, `runs/t04/results.json` et `runs/t04/EVIDENCE_INDEX.tsv`.

### T-05 — Garde-fou de commit

Onze configurations adversariales ou témoins, dans 16 copies comprenant les worktrees liés, ont été mesurées avec de vrais commits. Le contrôleur et le hook restent identiques à la source, sauf la référence volontairement retirée dans le cas dédié. Le détail est dans `runs/t05/REPORT.md`, les commandes dans les trois campagnes et les empreintes dans `runs/t05/proof-manifest.json`.

| Configuration | Résultat indépendant |
|---|---|
| Référence versionnée retirée | Audit et commit refusés ; HEAD conservé. |
| Copie installée retirée explicitement | Commit possible ; absence correctement signalée. Limite administrative documentée. |
| Worktree lié, hook commun absent | Installation PASS, CLI de contrôle FAIL, vrai commit accepté ; faux état installé. Reproduit sur branche nommée. |
| Worktree lié, hook commun présent | Vrai commit interdit refusé. |
| Index invalide masqué par le disque honnête | Refus normal ; acceptation quand la copie de contrôle de l’index est rendue indisponible. |
| Passager de fusion visible puis masqué | Refus visible ; acceptation masquée, y compris hors scope du WI ; audit final propre PASS. |
| Première installation interrompue | Hook non exécutable, commit possible, MISMATCH signalé ; réinstallation réussie. |
| Exécution du hook interrompue | Vrai commit refusé, HEAD conservé, reprise du contrôle efficace ; worktree temporaire orphelin. |
| Remote local | Sauvegarde normale reconnue ; index invalide encore refusé localement. Un commit déjà entré par le défaut worktree est reçu par le dépôt nu. |

Le remote contient `main` pour la suite, `t05/normal` et `t05/linked-invalid` pour les expériences. La réception du commit invalide établit la portée locale du hook ; aucune protection serveur n’était promise ou installée. Le constat de passager porte sur une entrée dans l’historique et un audit propre, avec WI encore IN_PROGRESS ; il ne prétend pas avoir produit DONE.

### T-07 — Corrections et régressions adjacentes

Les vrais tags 3.15.2 et 3.15.3 servent de témoins. La campagne comprend 48 observations CLI et 641 commandes ; ses 960 comparaisons de fichiers core, dans 40 arbres, sont alignées sur le tag correspondant. Le détail est dans `runs/t07/REPORT.md` et `runs/t07/results.json`.

| Contre-exemple initial | 3.15.2 | 3.15.3 |
|---|---|---|
| Architecture DRAFT et ADR PROPOSED avec notices des statuts attendus | Clôture bootstrap acceptée | Refus explicite ; documents validés et ADR non applicable acceptés |
| WI ouvert à la baseline, mandat REJECT | Clôture DONE après actualisation de lecture | Audit, actualisation et clôture refusés ; refus également avec une empreinte courante préparée pour isoler le mandat |
| Vrai unittest OK, code 0, avec diagnostic ERROR attendu | Preuve refusée | Clôture DONE et audit PASS |

Le témoin WI ouvert sous AUTHORIZE se clôture. Le témoin déjà DONE à la baseline conserve son vocabulaire historique et ses octets. La fixture de relecture fraîche sous REJECT est préparée manuellement avant installation de la gate : elle n’est pas présentée comme une commande d’actualisation réussie contre un refus.

Les vrais échecs unittest et les résumés négatifs FAILED/pytest restent refusés. En revanche, un programme réellement terminé en erreur avec une sortie limitée à ERROR ou à un traceback est désormais accepté comme pièce unique d’une preuve PASS : F-07-01 ci-dessous.

### Suite livrée — résultat séparé

**136 tests exécutés, 136 réussis, aucun ignoré : `Ran 136 tests in 549.080s`, puis `OK`.** Journal `runs/control/suite.log:184–186`, bilan `runs/control/suite-summary.json`.

Les fichiers de test, contrôleur et hook sont inchangés par rapport à la source, vérifiés après exécution. Le lanceur `runs/control/run_suite.py` charge tous les tests livrés sans modifier leurs assertions. Il remplace seulement la destination temporaire du test de sauvegarde par `runs/remote.git` dans les appels d’initialisation du bare et d’ajout du remote. Le push réel reste exécuté ; les deux substitutions et sa destination sont journalisées aux lignes 47–49. Il s’agit donc de la suite entière avec cette adaptation de confinement, pas d’une invocation strictement inchangée de la commande de découverte. Aucun test n’a été exclu comme lors de la première passe.

Une suite verte n’annule pas les contre-exemples indépendants. Elle ne vaut ni couverture exhaustive des configurations Git ni conformité du parcours d’adoption historique.

## 4. Constats classés par gravité

### F-T05-01 — Majeur : installation annoncée au mauvais emplacement dans un worktree lié

Créer un worktree lié depuis un dépôt bootstrap valide dont les hooks communs sont absents, puis y exécuter `install-gate`. La commande écrit sous `.git/worktrees/<nom>/hooks/pre-commit` et retourne PASS. Git indique pourtant, par `rev-parse --git-path hooks/pre-commit`, qu’il consultera `.git/hooks/pre-commit` dans le dépôt commun. Après indexation de `modules/t05/forbidden.py`, la commande de contrôle refuse mais le vrai commit réussit : `c2c11a58173cc837801ed8d8d21dd02ab2026602`.

L’audit suivant refuse le code actif en bootstrap, tout en annonçant le garde-fou installé. La protection absente n’est donc pas correctement diagnostiquée. Le témoin avec hook commun installé refuse le commit ; la réplication sur branche nommée `t05-worktree` exclut une dépendance au HEAD détaché. Aucune suppression de hook, panne injectée, dérogation ou modification du produit n’est requise. Preuves : journaux T05 `04-linked-no-main-hook`, `05-linked-with-main-hook` et `11-linked-named-branch` au registre ci-dessous.

### F-T05-03 — Majeur : un fichier hors scope entre dans une fusion et n’est plus signalé ensuite

Créer et démarrer réellement WI-001 pour `modules/allowed`, y committer `feature.py`, revenir sur `main` et préparer une fusion sans commit. Ajouter et indexer `modules/not-authorized/passenger.py`, absent de la branche fusionnée et hors scope du WI. Visible sur disque, il est refusé par la CLI et le vrai commit. Retirer uniquement ce fichier du disque tout en gardant son blob dans l’index rend la CLI PASS et permet le vrai merge commit `689e583957e4be5a06c2aec823b1dd905ca0f494`.

Le rapport annonce avoir audité le disque et l’état indexé. Le passager se trouve pourtant dans HEAD. Remettre sur disque ses octets exacts depuis HEAD rend l’arbre propre et l’audit/status PASS. Le différentiel propre à la branche montre uniquement `feature.py`, celui du merge ajoute aussi le passager ; le WI committé exclut son dossier. Cela nécessite des écritures et une indexation ordinaires, sans administration directe de `.git`, override, panne ni modification du produit. Le WI reste IN_PROGRESS. Preuve décisive : `runs/t05/run-003/logs/12-outside-scope-passenger.log:95–259,288–292`, avec reproduction préalable dans le cas 07.

### F-T05-02 — Majeur sous condition administrative : l’impossibilité de contrôler l’index autorise le commit

Dans un projet normal valide avec gate installée, indexer une roadmap contenant WI-999 sans record correspondant, puis remettre sur disque la roadmap honnête. La copie de contrôle de l’index disponible fait refuser la CLI et le vrai commit. Remplacer temporairement le chemin `.git/worktrees` par un fichier empêche sa création. Sans toucher au hook ni au contrôleur, la CLI et le vrai commit passent ; `56cd306b35fd0a64c1a19cc5ba0d21dae8021a0f` contient réellement la roadmap invalide.

Le commit annonce explicitement le contrôle réduit au disque dans une ligne PASS. Audit/status restent PASS tant que le disque présente les octets honnêtes, avec un checkout sale. Une fois le mécanisme de snapshot rétabli, le prochain pre-commit refuse ; une fois le disque aligné sur HEAD, l’audit refuse également. Le résultat contredit la garantie de refus lorsque l’état à committer ne peut être vérifié. Il exige, dans le scénario exécuté, un accès administratif aux métadonnées Git ; aucune panne de permissions OS spontanée n’est démontrée. Preuve : `runs/t05/run-001/logs/06-snapshot-unavailable.log:109–175,177–283,297–398`.

### F-T04-01 — Modéré, P2 : la montée documentée réclame des fichiers et un ordre de préparation non annoncés

Partir du projet 3.6.1 à quatre DONE, avec cœur intact, gate installée et WI-005 autorisé pour le cœur, le manifeste et les futurs fichiers de projet. Déclarer la baseline d’adoption et les choix humains requis. Le plan puis `template-upgrade --apply` réussissent. Après installation de la gate, choix de langue/style et indexation explicite, l’audit refuse l’absence de `docs/governance/IDEAS.md`, `docs/governance/ideas-state.v1.json` et `project_control/roadmap-view.v1.json`.

`idea add` et `roadmap-view --write` refusent faute de ces mêmes fichiers. Le vrai commit est refusé. Dans une expérience supplémentaire, copier les trois modèles fournis fait passer l’audit, mais le commit est encore refusé par `WORK_BRANCH_RECORDS_READ_ONLY` : le nouveau contrôleur réserve ces records à la canonique, même s’ils figurent dans les chemins autorisés du WI d’upgrade.

La procédure publiée décrit le remplacement du cœur sans modification de records, mais ne décrit ni cet amorçage ni son ordre. La préparation des modèles avec l’ancien contrôleur, avant le remplacement, permet ensuite de finir le parcours assisté. Le constat est donc une procédure incomplète démontrée, sans prétendre à une corruption des anciennes clôtures ou à une récupération absolument impossible. Aucun override de commit ne fonde cette démonstration. Preuves : `runs/t04/logs/0132-python3_14.log:13–17`, `0138-python3_14.log:14–20`, `0139-python3_14.log:14`, `0140-python3_14.log:13`, `0141-git.log:14–18`, `0143-python3_14.log:8–35` et `0144-git.log:15–18` ; tous ces journaux sont sous `runs/t04/logs/`.

### F-07-01 — Modéré, P2 : une preuve PASS accepte désormais l’unique sortie d’un programme échoué

Sur un WI réellement démarré et intégré, tests APPLICABLE, exécuter le script de fixture qui imprime `ERROR: campagne échouée : contrôle 2 + 2 == 5 refusé` puis termine avec code 1. Citer exactement cette sortie comme unique artefact d’un rapport déclaré PASS, avec empreinte et références Git correctes. La gate accepte le commit de preuve ; `close` produit DONE ; l’audit final passe. Le même artefact, SHA-256 `9c06b496549a62f3e9634399208f892d998cb1a0e4c90109369d7350e3ce83f5`, est refusé par la 3.15.2.

Une variante exécute effectivement une assertion arithmétique fausse et termine code 1 avec traceback/AssertionError. La 3.15.3 l’accepte aussi ; une contre-épreuve 3.15.2 refuse exactement les mêmes octets. Aucun artefact positif ou neutre supplémentaire, baseline modifiée, index masqué, override ou correctif produit n’intervient. Le privilège est celui de fournir une preuve dans son dossier autorisé. Le rapport PASS est intentionnellement mensonger pour mesurer le refus annoncé.

Le contrat `source/project_control/README.md:152–164` énumère encore ERROR et Traceback parmi les marqueurs refusés lorsque toutes les pièces annoncent un échec. La correction retire ces marqueurs pour accepter le diagnostic attendu d’un test réussi, mais les deux programmes réellement échoués n’impriment aucun des marqueurs restants. Le constat porte sur cette régression textuelle précise, pas sur l’authentification générale des exécutions. Preuves principales : journaux T07 `0454`, `0463`, `0467` et témoin `0156` ; variante `0438`, `0447`, `0451`, `0624`.

## 5. Observations non bloquantes et hypothèses restantes

- Retirer la référence versionnée ne désarme pas la copie installée : refus effectif. Retirer explicitement cette copie désarme la protection, mais l’absence est signalée ; c’est la limite administrative annoncée par le produit, distincte du faux succès d’installation.
- Tuer la première installation après écriture, avant mise en exécution, laisse un hook non exécutable. Git l’ignore avec avertissement ; l’audit signale MISMATCH et une réinstallation rétablit la gate. L’installation n’avait pas annoncé de réussite : cette observation n’est pas classée comme un quatrième défaut majeur du garde-fou.
- Tuer la gate après création du snapshot refuse le commit et conserve HEAD. Un worktree temporaire reste orphelin, sans neutraliser le prochain contrôle. L’épuisement par interruptions répétées n’a pas été testé.
- Les statuts contradictoires restent sensibles à leur ordre : une première valeur VALIDATED suivie de DRAFT passe ; DRAFT suivi de VALIDATED refuse. Un champ Status vide avant une valeur validée passe. Ces comportements ne sont pas une nouvelle régression démontrée de 3.15.3.
- Un vrai unittest OK imprimant un diagnostic attendu `errors=1` reste refusé. Une pièce unique réunissant FAILED puis OK est refusée sur les deux versions, alors que deux pièces séparées échec/réussite passent. Ces limites préexistantes sont distinguées de F-07-01.
- Le remote nu accepte un commit invalide déjà produit localement. Cela n’établit pas un contournement de gate serveur : aucune telle gate n’était installée ou promise.

Pour T-04, la restauration complète a été mesurée avec SIGINT lors de la montée exécutée par 3.15.1. SIGKILL n’est pas interceptable : il laisse une mise à jour partielle, signalée comme divergence, et aucun mécanisme de reprise après crash n’a été démontré. Aucun `--overwrite` n’a été essayé pour effacer cet état. L’ancien exécutant 3.6.1 ne restaure pas non plus complètement le cœur après le SIGINT testé. Ces deux résultats sont conservés comme limites de reprise ; ils ne sont pas ajoutés aux défauts majeurs de 3.15.3.

Aucune hypothèse de code non reproduite ne fonde le verdict. Les explications par les fonctions du contrôleur servent à comprendre les scénarios exécutés ; elles n’étendent pas leurs garanties à d’autres systèmes, commandes ou formats.

## 6. Ce qui n’a pas été vérifié, et pourquoi

- Une véritable exploitation pendant plusieurs jours par plusieurs personnes : le projet ancien est une fixture à histoire Git réelle et cycles exécutés, avec chronologie narrative simulée. Il n’est pas un projet métier ancien retrouvé sur la machine.
- Un onboarding humain aveugle : T-04 a consulté schémas et aide CLI ; T-05/T-07 utilisent les helpers de préparation déclarés. Les décisions fictives ne prouvent ni identité ni consentement humains réels.
- L’exhaustivité des interruptions : les signaux et points précis testés ne représentent pas toutes les fenêtres d’arrêt, pannes de courant, saturations disque, réinstallations interrompues au milieu des octets ou permissions sur d’autres OS.
- Toutes les configurations `core.hooksPath`, toutes les topologies de worktrees et toutes les pannes de snapshot. La manipulation de `.git/worktrees` reproduit une indisponibilité déterminée, pas toutes ses causes possibles.
- Clôtures runtime/déploiement, production, réseau et authenticité métier des preuves : hors périmètre. La gate de preuve mesurée indépendamment en T-07 est `tests` ; toute généralisation aux autres gates serait une inférence.
- Une nouvelle matrice exhaustive d’encodages UTF-16/ANSI/binaires, ou la répétition des quatre autres thèmes de la première passe : non demandées, sauf interactions précisément décrites.
- Une absence absolue d’effets internes des runtimes système : les empreintes attestent le contenu et les permissions des fichiers source, pas leurs dates d’accès ni les caches OS. Les snapshots de refus mesurent les états annoncés, sans prétendre prouver qu’aucun objet Git temporaire n’a été écrit.

Le parcours principal d’adoption avec les seules étapes publiées a été exécuté et refusé : il n’est pas présenté comme réussi grâce à la récupération assistée. Toutes les versions intermédiaires n’ont pas été montées ; le saut exact testé est celui de deux versions correctives, 3.15.1 vers 3.15.3. La variante de vocabulaire ancien est écrite sous 3.6.1 après une clôture déjà acquise, avant adoption ; elle ne remplace pas un entretien ou une décision humaine réellement ancienne. Les scripts T-04 sont un carnet exploratoire amendé, pas un lanceur intégral idempotent ; les commandes enregistrées et copies figées sont les points de reprise. Le clone initial et les lectures exploratoires précèdent son pilote de journalisation et ne sont pas tous consignés dans ses 267 logs.

## 7. Registre des preuves décisives et conservation

Les lignes sont physiques, comptées depuis 1 ; chaque SHA-256 porte sur le fichier entier. Les journaux contiennent commandes, répertoires de travail, sorties et codes retour. Les registres détaillés des trois campagnes complètent cette sélection ; une référence à un rapport de campagne ne remplace pas la preuve d’exécution citée ici.

| Objet | Chemin | Lignes | SHA-256 du fichier entier |
|---|---|---|---|
| Références Git résolues | `runs/control/meta/resolved-tags.json` | 1–26 | `065ebe29d13550cf1827d761f57a6a4686cc5bfcf258c00caa77a12c203249b4` |
| Référence audit et core | `runs/control/reference-checks.log` | 6–32,39–66 | `29a7a468f6773fb2312e36ffaec956cc96b05a70196deda27dd840649cb273b0` |
| Intégrité avant | `runs/control/meta/source-before.json` | 1–7 | `904405bbdd7c52a85a9c84caca627f0dec99590f1876961fd20ae5649d7e5730` |
| Intégrité après | `runs/control/meta/source-after.json` | 1–7 | `904405bbdd7c52a85a9c84caca627f0dec99590f1876961fd20ae5649d7e5730` |
| Comparaison source complète | `runs/control/meta/source-verification.json` | 1–35 | `da000894ee69915079b6d13fdf7ddbf4bc8c3bf51e85d01d5297bbe554f46397` |
| Suite complète / push autorisé | `runs/control/suite.log` | 3,47–49,184–186 | `d6ce021b57bc08cc5294c147bc7b8937b830b3ea95e4b3cff11481870e9c0f7d` |
| Refs reçues et commit invalide reçu | `runs/control/remote-final.log` | 1–10 | `3d188db12bceabb5b743c456211fedcf8826025b9edefd6f04d6bb8125cfe600` |
| Contrats preuves et montée | `source/project_control/README.md` | 152–164,240–252 | `ec44e4742c6974d4a3f51fec8d0d813a3a7aa92a654021a3c4fb09b07d876a78` |
| T04 — Tag historique, commits réellement présents | `runs/t04/logs/0267-git.log` | 8–10 | `1c105851dd04a0c2cadab6c6e1fbefef0293f9fa143724aedf6da48aa6ee9bbc` |
| T04 — Première clôture réelle DONE | `runs/t04/logs/0056-python3_14.log` | 6–14 | `d578f698ae7e5aee3edc9f1e2e63054be8fec14798d898aaa4f8da76e94e6bbe` |
| T04 — Blocage réel | `runs/t04/logs/0067-python3_14.log` | 6–14 | `c1b8e7fd1338d6bc2edc84f2ba217d3876aa0114706f437bc2bb3c67a3a03285` |
| T04 — Refus historique reprise 3.6.1 | `runs/t04/logs/0087-python3_14.log` | 14–20 | `06b79d47c8aca9a9483725355e14821e10ecbf300d551efae85c3c9eb3558afa` |
| T04 — Reprise historique sous override déclaré | `runs/t04/logs/0090-python3_14.log` | 5–14 | `7560b93249c40ed372004677165128524d69728a021a4b8fa8aca39121ff85b6` |
| T04 — Quatrième clôture et baseline | `runs/t04/logs/0111-python3_14.log` | 6–14 | `0c5047812646f1b632e5e5af62909d4c40adedbc9c13ee6f5749e965554b7e2c` |
| T04 — Audit historique 4 DONE | `runs/t04/logs/0112-python3_14.log` | 8–32 | `5092d00c6ea4bf99a8934cc0066fcbf4763ce4b261a9f286869f4ab02af1312a` |
| T04 — 32 commits autonomes | `runs/t04/logs/0247-git.log` | 8 | `fa948d1a573bd8a795765c11853d0a097699ea4ff55daacb2b2badd9547c479d` |
| T04 — F-T04-01 remplacement core réussi | `runs/t04/logs/0132-python3_14.log` | 13–17 | `9fbe302b3b8834c6a42c3bc5cf36cf6b6bd7b10f0235331bc87929d81abef8cc` |
| T04 — F-T04-01 nouveaux records manquants | `runs/t04/logs/0138-python3_14.log` | 14–20 | `87bd70551e26cbf0c054ac8b0d2c9b08a4f755901c02b10b313a96213a7fb880` |
| T04 — F-T04-01 commande idées ne les crée pas | `runs/t04/logs/0139-python3_14.log` | 14 | `6855d2abc42bc11ef9055a7a539b18efd0ed5fcaeecd2bc11edd7fb86c481b11` |
| T04 — F-T04-01 commande vue ne les crée pas | `runs/t04/logs/0140-python3_14.log` | 13 | `e9afc0e49e301be7afb6fd4bd95e721b7614fbe40e773fa6f46d73a6b2664d31` |
| T04 — F-T04-01 commit refusé avant modèles | `runs/t04/logs/0141-git.log` | 14–18 | `bbfc0d4028e7fd147679ba89ca253b65661809056237b35bb0dad7a7b5595021` |
| T04 — F-T04-01 audit après modèles | `runs/t04/logs/0143-python3_14.log` | 8–35 | `f405b59b9e870395a8407fab2a71d3932ea0b56b3a5adb727c73384774b17446` |
| T04 — F-T04-01 commit refusé après modèles | `runs/t04/logs/0144-git.log` | 15–18 | `163f7077468c54af3194791c5e6c9dcac51453d8accc2aa9facfd749c198fbf9` |
| T04 — Récupération expérimentale préparatoire | `runs/t04/logs/0146-git.log` | 6–12 | `e7c61e60fb5ed8972d9493bda977d50567a6f8adc07766779ba477428e094c42` |
| T04 — Core monté et committé sans override | `runs/t04/logs/0152-git.log` | 5–15 | `20f8a63c426976dad221ff991c0976ac360b2f534c3ae6d61594e2bf405f6cc1` |
| T04 — Régression fonctionnelle réellement exécutée | `runs/t04/logs/0155-python3_14.log` | 14–26 | `425debe9b2db2c2a2c5218c8cd0209749a003ca6b39ea3abe36da5ae65eb006e` |
| T04 — Clôture WI005 sous contrôleur 3.15.3 | `runs/t04/logs/0160-python3_14.log` | 6–14 | `8f79e7b5fa132db7f13123abd2b9db65b5ec616e2f086b65fcbe61eb742bc3b3` |
| T04 — Audit final | `runs/t04/logs/0161-python3_14.log` | 8–34 | `dfbc20be2e7745909dc3cafd11cb55e072914ef5af5c312720677033527c346e` |
| T04 — Quatre clôtures LEGACY_PRESERVED | `runs/t04/logs/0162-python3_14.log` | 36,50,64,78 | `6f4dc2059c122d51c36456453120ac7776993afde8c501bd628ccf4680d5dff9` |
| T04 — Préservation 19 fichiers | `runs/t04/evidence/historical-preservation.json` | 1–6 | `c2389910df96154501c782e155f2128bc6bc4ee91a7a5fd542c788a821b5ec7f` |
| T04 — Contre-épreuve modification historique refusée | `runs/t04/logs/0246-python3_14.log` | 24 | `fa2d0d86d005bca83d71102d0a109b54bc39a8cc13e2e47c8282c2ed1a690982` |
| T04 — Saut exact 3.15.1 à 3.15.3 | `runs/t04/logs/0179-python3_14.log` | 13–18 | `6aa5d87d30ffde8db9addd7e5ae7af01622f4d54cd889636a4a692a9862b2139` |
| T04 — Audit après saut exact | `runs/t04/logs/0183-python3_14.log` | 8–34 | `c2e45411f5a792b90e1a09735469e7ba3f980c2d9417f354741c9606ecc8bb66` |
| T04 — Interruption pendant réinstallation gate | `runs/t04/logs/0189-python3_14.log` | 6–8 | `92fc386de5eec5f44afe13a9c1d8934422dfb0f18f376fd8c18bc600c8dd1b50` |
| T04 — Reprise après réinstallation interrompue | `runs/t04/logs/0193-python3_14.log` | 13–18 | `758899671d16ffcde3727fab3760ddc1225e750bf7ad0de5d96e881244bf16d1` |
| T04 — SIGINT effectif après changement core | `runs/t04/logs/0219-python3_14.log` | 6–8 | `4267fae894882d429a5aa68c5f08a3cf7edfaded28cf972c759786ebcab2041c` |
| T04 — Rollback SIGINT intégral | `runs/t04/evidence/interrupt-watch-3.15.1-int-comparison.json` | 1–5 | `8863103d0a669718180830b66c445da115d4de8495350bc349aa6fac2e4cbe81` |
| T04 — Reprise SIGINT commande normale | `runs/t04/logs/0224-python3_14.log` | 13–18 | `1f91d803bfa5cd9e78e71643e330cf7a831b8e72339e0f6395c1463c456f2e72` |
| T04 — Reprise SIGINT audit/commit | `runs/t04/logs/0244-git.log` | 5–12 | `5ce58335fbaa83ff19ea87a404399229c79e61c7644efeec89dfd34b66e0ab57` |
| T04 — SIGKILL effectif | `runs/t04/logs/0227-python3_14.log` | 6–8 | `ccb431ae24568659d259acf756ea6ae2135a6e2776dadbc93cc649bb5fb29b18` |
| T04 — SIGKILL dérive détectée | `runs/t04/logs/0230-python3_14.log` | 13–14 | `e17f89ac693a3b313ad808fcee934c7df3afdf5dc7ef427baa8574c24a207661` |
| T04 — SIGKILL audit général reste PASS | `runs/t04/logs/0231-python3_14.log` | 8–34 | `48cecc3c209a758bebdbe260f38a3d5188bf4c570ee51056b1891927c3052779` |
| T04 — SIGKILL reprise refusée | `runs/t04/logs/0232-python3_14.log` | 15–17 | `d67b94d0eda4ba1b90b87ae707319b859b917fe9102389bd938568685da1f429` |
| T04 — SIGINT historique 3.6.1 effectif | `runs/t04/logs/0235-python3_14.log` | 6–8 | `c8163002a1eb9a32c594801cf1695ca3ab32db3a643e1239a832b1193a3a03e4` |
| T04 — SIGINT historique reprise refusée | `runs/t04/logs/0240-python3_14.log` | 15–17 | `1492df3561b533dac327b3596861733e09c5df542cd262c909b236e70abd3dfd` |
| T04 — Vocabulaire APPROVED lu sous 3.6.1 | `runs/t04/logs/0252-python3_14.log` | 6–32 | `b153e77d716d12da650f7a8eef820bfae9ba1021cd96b7bc15412a552fce3387` |
| T04 — Vocabulaire APPROVED audit sous 3.15.3 | `runs/t04/logs/0265-python3_14.log` | 8–34 | `d4536c86c8e788bdea86d390adf31bb798a47022e65ed0f5d917eece37d9fde7` |
| T04 — Vocabulaire et clôture bytes conservés | `runs/t04/evidence/legacy-vocabulary-preservation.json` | 1–13 | `91092bc24c84d26bf95e951e442343b2be5082ef7c1d216114246b8a2b3e3016` |
| T04 — clôture WI003 | `runs/t04/logs/0082-python3_14.log` | 6–14 | `0400a609659ea89facdb42a3213b5961f9def53b56dc77b3e0e7197be32df342` |
| T04 — clôture WI002 après reprise | `runs/t04/logs/0097-python3_14.log` | 6–14 | `69c2da5478bd9500dab7069607e1b9cf4657496f7cde41a7a7dad4b99e951eb1` |
| T05 — Référence retirée refusée | `runs/t05/run-001/logs/02-reference-removed.log` | 47,94–110 | `49c41c69108d356276de516abc71870c18f9f1261a83c41d912b5b159a50b5d0` |
| T05 — Copie absente signalée | `runs/t05/run-001/logs/03-installed-removed.log` | 64–70,103–120 | `e60b7dd713b2887ee4abd44896e94c9aa28f2b3b21042079959a3c2c694ce261` |
| T05 — F-T05-01 | `runs/t05/run-001/logs/04-linked-no-main-hook.log` | 12–39,46–71,103–121 | `bfee8d663d0a0f2499d19f57c3a2638bb8deb23a93387237e434350d5cf58552` |
| T05 — Témoin hook commun | `runs/t05/run-001/logs/05-linked-with-main-hook.log` | 1–156 | `742719f62c4cd2c84f24ed160a6c25637a301ccf8fe813a9e91b5952d862c80d` |
| T05 — F-T05-02 | `runs/t05/run-001/logs/06-snapshot-unavailable.log` | 109–175,177–283,297–398 | `33424c5de026474322628a830450f1aa375506618a6081d7922bbe8b4b8b8ef0` |
| T05 — F-T05-03 | `runs/t05/run-002/logs/07-masked-merge-passenger.log` | 136–207,223–323 | `70be2bcc62ab80dac38d35169c96bd42a273a05ad388e492a0474dc43a27fa42` |
| T05 — Installation interrompue | `runs/t05/run-002/logs/08-install-interrupted.log` | 5–11,60–68,140–161 | `dfd33baa36e89c19ea9a589fe56195aa8471b3ea15ad7bfc78d24a0379a3654d` |
| T05 — Gate interrompue | `runs/t05/run-002/logs/09-gate-interrupted.log` | 86–143,159 | `689ea1d64aaf5e8817cd31fa598e2679a557a11b5e5bd12d75b0daf73b7eab15` |
| T05 — Remote local | `runs/t05/run-002/logs/10-local-remote.log` | 156–185 | `c083711250f67ebdb3b4d0c71994a9070682b0de9f1052fb492fa4aa0c5818ed` |
| T05 — Réplication branche liée nommée | `runs/t05/run-003/logs/11-linked-named-branch.log` | 19,43–59,92,109 | `abce4ff2201b1e4631c3a0dc5fda0616c9c1d26351b55a9c6df608764b27cbfb` |
| T05 — Réplication passager hors scope | `runs/t05/run-003/logs/12-outside-scope-passenger.log` | 95–175,183–259,288–292 | `82ce26fc037ed20d4156869cebd5962231c3f8cfbc865b0896779842dc11f9c7` |
| T07 — Ancien brouillon accepté | `runs/t07/logs/0021-status-3.15.2-python3.14.log` | 1–36 | `72a37d6144532bdd775fbb3e4b69bbf2ecc8c6f8da995495f164258bf71214b7` |
| T07 — Brouillon 3.15.3 refusé | `runs/t07/logs/0328-status-3.15.3-python3.14.log` | 1–36 | `1c08df86a97bc50656e9357ce4259e863431c5c011631157169e0643ce2d4913` |
| T07 — Ancien REJECT clos | `runs/t07/logs/0267-open-frozen-reject-3.15.2-python3.14.log` | 1–12 | `5b4bc0f27ae02de29a6d60d060ba2a3be3a536640d7a326bedea32b5657c74a0` |
| T07 — REJECT frais refusé | `runs/t07/logs/0585-open-frozen-reject-fresh-3.15.3-python3.14.log` | 1–12 | `67061871b605543d03129398eb5c2abd3132f07e50487fbe94453cc513ad3bfc` |
| T07 — AUTHORIZE témoin clos | `runs/t07/logs/0597-open-frozen-authorize-3.15.3-python3.14.log` | 1–12 | `5fe1e69c7f306b014a5c942d2f8ba3806c9bcdf35e8a5af2a5ba884826d42b4c` |
| T07 — DONE figé témoin préservé | `runs/t07/logs/0611-closed-frozen-reject-3.15.3-python3.14.log` | 1–32 | `3c3bd3525216d35a85cf4a145fdfe1635e9809b0f2a1a996948f158972207494` |
| T07 — Ancien vrai OK + ERROR refusé | `runs/t07/logs/0108-actual_pass_expected_error-3.15.2-python3.14.log` | 1–12 | `a30e8fe3d0f51c589e4032b667c89a2b2b5b7c81457358ef5718dea66864a21f` |
| T07 — Vrai OK + ERROR exécuté | `runs/t07/logs/0406-actual_pass_expected_error-3.15.3-python3.14.log` | 1–13 | `41f309a754430a1993c5de08857e5e130fc627b6f3581c632ca490239c1d0763` |
| T07 — Vrai OK + ERROR clos | `runs/t07/logs/0415-actual_pass_expected_error-3.15.3-python3.14.log` | 1–12 | `2e4fc570b05037545c719fe13dd9dfe7b7095d4e619d7a2b952262ad236fd65e` |
| T07 — F-07-01 vrai exit 1 | `runs/t07/logs/0454-actual_error_exit_one-3.15.3-python3.14.log` | 1–6 | `2f31773890782529d2b920356e9e2dd210e46d05acd76f44137b213b01a2e0c9` |
| T07 — F-07-01 DONE accepté | `runs/t07/logs/0463-actual_error_exit_one-3.15.3-python3.14.log` | 1–12 | `a8684edf94deda3ad568f2d541e349da01ae93a9affc9d2dcb9743446ce7bb29` |
| T07 — F-07-01 audit final PASS | `runs/t07/logs/0467-actual_error_exit_one-3.15.3-python3.14.log` | 1–32 | `94a3f01d370f3a952a7adfa946a05e1b6a901855435e307cf941998331637c60` |
| T07 — F-07-01 même ERROR ancien refusé | `runs/t07/logs/0156-actual_error_exit_one-3.15.2-python3.14.log` | 1–12 | `fed52a333cdcce04d5536bf32dc22cc9a352a11ad1a184c7dcc0d411fef3b4ab` |
| T07 — F-07-01 assertion réellement échouée | `runs/t07/logs/0438-actual_python_assertion_failure-3.15.3-python3.14.log` | 1–13 | `a3753c3403dfcd8325fcc709c9580303aebf0dec40eaa57ba3760140b011bfc7` |
| T07 — F-07-01 traceback clos | `runs/t07/logs/0447-actual_python_assertion_failure-3.15.3-python3.14.log` | 1–12 | `6a46c8af1e2ecb34bddb1ab346b39ce310a966a180d5c09d6053e9dfa5b60b34` |
| T07 — F-07-01 même traceback ancien refusé | `runs/t07/logs/0624-identical-python-crash-3.15.2-python3.14.log` | 1–12 | `dd399cea8932c409ae2d035c315ff9e2393486d312c27b209d94fa3a5b6fd939` |
| T07 — Vrai OK avec errors=1 refusé | `runs/t07/logs/0638-actual-pass-expected-counter-3.15.3-python3.14.log` | 1–12 | `859b8ea77a3ed7ed2ca53ea39127915976bc4bb249b3d502c14aa2be14b79c4c` |
| F-07-01 rapport à pièce unique | `runs/t07/actual_error_exit_one-3.15.3/reports/evidence/WI-001/tests.json` | 1–17 | `dcf9f398436ca432289f77b7b97406e20dcbc666c46970585ef9260a392d2a4c` |
| F-07-01 pièce ERROR | `runs/t07/actual_error_exit_one-3.15.3/reports/evidence/WI-001/tests.txt` | 1 | `9c06b496549a62f3e9634399208f892d998cb1a0e4c90109369d7350e3ce83f5` |
| F-07-01 pièce traceback | `runs/t07/actual_python_assertion_failure-3.15.3/reports/evidence/WI-001/tests.txt` | 1–8 | `5194ba9a9f519c88a6491dd5097f85ec555e10721e2175f92548e1ffabde650c` |

**État final de la source.** Les inventaires avant/après sont identiques pour les **1 082 fichiers**, dont 117 hors `.git` et 965 dans `.git` : mêmes chemins, tailles, contenus et permissions. Aucune différence ; source toujours propre sur `main`, au HEAD initial. Les deux inventaires ont le SHA-256 `904405bbdd7c52a85a9c84caca627f0dec99590f1876961fd20ae5649d7e5730`. La comparaison complète figure dans `runs/control/meta/source-verification.json`.

Le dossier conserve les rapports détaillés et toutes les expériences sous `runs/t04/`, `runs/t05/`, `runs/t07/`, la suite et les vérifications d’assemblage sous `runs/control/`, et le bare autorisé sous `runs/remote.git`. Les programmes d’essai ont terminé ; les worktrees laissés par les interruptions sont des états de preuve, pas des processus en cours. Le seul livrable final créé à la racine est `CONTROLE_SQUELETTE_3.15.3.md`.

Les recettes de reproduction figurent dans les rapports T-04, T-05 et T-07. Les copies réussies sont déjà closes ; relancer `close` dessus ne reproduit pas leur historique. Les recettes créent de nouvelles copies nommées, et les états refusés ainsi que les états partiels restent consultables. Aucun patch ni proposition de code produit n’accompagne ce rapport.

## 8. Verdict

SQUELETTE_3.15.3_REQUIRES_MAJOR_REDLINE
