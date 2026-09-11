> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

1. Les 141 tests livrés réussissent et les corrections ciblées tiennent dans les scénarios rejoués. Le contrôle indépendant démontre néanmoins deux défauts majeurs : l’histoire déclarée figée peut être réécrite, et des transactions concurrentes peuvent laisser des records incohérents.
2. Un troisième défaut, modéré, concerne la création d’un projet : l’absence de `.gitignore` n’est pas signalée pendant l’initialisation, mais fait ensuite échouer une opération normale de génération de la vue de suivi.
3. Aucun correctif produit n’a été apporté. Les preuves, scénarios refusés et copies sont conservés dans `runs/`. La source est inchangée. Aucune action supplémentaire du propriétaire n’est nécessaire pour consulter le rapport.

# Contrôle du squelette 3.16.2 — troisième passe

## 1. État exact et périmètre

Contrôle du 10 septembre 2026. Racine accordée : `~/Projets/squelette-controle-3.16.2/`. Tous les chemins relatifs cités partent de cette racine. Les lectures de projet, expériences, temporaires et journaux ont été confinés à ce dossier ; `source/` a servi uniquement de référence en lecture.

La source est propre sur `main`, au commit `98c186b3ac74ff37ea5736cdf9ffa15b9bb3b270`. Le tag `v3.16.2` désigne `f3c1f57af3ab07393312cc189240d82bfbcf3fff`. Leur seule différence est une régénération de `provenance/ROADMAP_VIEW.md` ; le cœur testé est celui du tag. Le véritable tag `v3.6.1`, utilisé pour le parcours historique, désigne `0d5d86f5960aadbb27b333fced41f6b1b4b0a37d`. Les tags intermédiaires résolus sont enregistrés dans `runs/control/meta/refs.json`. L’audit, le statut et le contrôle du manifeste de la copie de référence passent (`runs/control/preflight.log:1–124`).

La source compte **119 fichiers hors `.git` et 1 060 fichiers dans `.git`**. Les deux inventaires ont le même SHA-256 : `2490b14cfbfa91e6a70af3b9e31e1b0f45f879fc23f679de0a2ad92a74a392e7`. Les 1 179 chemins, contenus, tailles et permissions comparés sont identiques (`runs/control/meta/source-verification.json:1–8`). Les premières lectures et inspections Git précèdent cet inventaire ; les dates d’accès et les effets internes des runtimes ne sont pas attestés.

Le contrôleur 3.16.2 a pour SHA-256 `8b812c8ea6fcb663ab3984c07d175f96a32dfe5488628855e2c34c97641e72f0`. Les **1 094 comparaisons de fichiers core dans 46 arbres** contrôlés ne montrent aucune dérive. La comparaison normalise uniquement le premier marqueur de statut de FIRST_START, conformément au manifeste ; les archives et les générations historiques utilisent leur propre version (`runs/control/meta/core-copies.json:1–278`).

## 2. Méthode, privilèges et écarts au protocole

Les deux rapports précédents et le `MANDAT.md` local ont été consultés avant les essais. La pièce jointe avait été lue dans Downloads avant que l’utilisateur confirme l’exécution du mandat ; aucun autre projet n’a ensuite été consulté. Aucun accès réseau. Les configurations Git globales/système sont neutralisées, les identités locales sont fictives, le bytecode Python est désactivé et les temporaires sont dans `runs/control/tmp`. Les exécutables et bibliothèques système restent nécessaires à l’exécution.

Le dossier 3.16.2 n’était pas initialement ouvert en écriture par l’environnement. L’escalade d’accès pour créer `runs/control/` a été acceptée, ainsi que les exécutions suivantes. **Aucun rejet de l’approbation automatique et aucun contournement d’un refus d’outillage.** Les refus du contrôleur et de son hook sont des résultats des expériences autorisées.

Les helpers livrés servent à préparer les fixtures d’initialisation, certains records et les arguments CLI ; ils ne constituent pas une preuve indépendante. Leur `WI-000` DONE est synthétique. Les créations, démarrages, intégrations, commits et clôtures qui fondent les constats passent par les vraies commandes du produit. T-10 emploie les deux exports réels décrits ci-dessous, puis des valeurs d’interview fictives préparées par helper : aucun onboarding humain aveugle n’est revendiqué.

Les exceptions utilisées sont explicites : préparation initiale des déclarations d’adoption en T-08 ; construction d’un commit volontairement invalide pour isoler l’exemption de lecture ; clôtures FIRST_START de T-10 ; adoption historique du core en T-11 sur la canonique. Le scénario de mandat REJECT est construit avant installation de la gate. **Les mesures de réécriture/réouverture après retrait gouverné des baselines, les courses T-09 et les preuves T-11 n’emploient aucune dérogation au hook.** Les décisions sont des données de test, sans autorité réelle hors de ces copies.

T-09 utilise deux processus du contrôleur sur le même checkout, pas deux personnes ni deux modèles autonomes. Trois courses sont lancées sans instrumentation. Les autres imposent un ordonnancement par une trace Python externe et des signaux SIGSTOP/SIGCONT, avec SIGINT dans le cas d’interruption. La trace suspend l’exécution ; elle ne remplace aucune méthode du produit. Les arrêts précis et les commandes sont conservés.

Erreurs de montage conservées, sans les imputer au produit : la première déclaration de baseline sur main a été refusée par la protection canonique ; le premier ordonnanceur de T-09 n’a pas reconnu le nom relatif du fichier et n’a donc pas suspendu A ; le premier essai de réouverture n’avait pas indexé le retrait du Run ; le premier audit d’upgrade précédait l’indexation des nouveaux fichiers. Chaque point a été isolé puis rejoué. Les scripts sont un carnet d’expériences avec reprises, **pas un lanceur global idempotent** : les destinations existantes ne doivent pas être écrasées.

## 3. Vérifications thème par thème

### T-08 — Baselines et réouverture de l’histoire

| Essai exécuté | Résultat et portée |
|---|---|
| Réécrire l’objectif d’un WI DONE toujours figé | Audit et vrai commit refusés. |
| Retirer directement `legacy_baseline` sur main | L’audit accepte l’état, mais le commit de Project State est protégé. Ce seul essai ne prouve pas un contournement du hook. |
| Retirer la baseline par un WI autorisé pour Project State, puis modifier l’ancien record sur main | Changement de baseline intégré, ancien record modifié et committé, audit PASS ; F-08. |
| Refixer l’histoire sur le nouveau commit avec la même HD-105 | Nouveau WI, intégration et clôture acceptés ; l’ancienne décision continue pourtant de nommer l’ancien SHA. |
| `start` direct d’un DONE figé | Refus attendu : le retrait d’une baseline ne constitue pas, à lui seul, une commande de réouverture. |
| Retirer les deux baselines par un WI, reconstruire le record AUTHORIZED et retirer son ancien Run | Vrai commit accepté, nouveau `start`, nouveau travail, intégration et deuxième `close` DONE ; audit PASS. |
| Run récent dont `authorities_read` a été retiré | Audit et commit normal refusés. Après préparation administrative du commit invalide, avancer seulement `authorities_baseline` avec la vieille HD-107 fait passer l’audit. Ce cas exige une construction privilégiée de l’état historique. |
| Baseline citant `Chosen option: REJECT`, ou une décision relative à la couleur d’une icône | Audit accepté pour les deux types de baseline. Les commits directs sur main restent protégés. |
| Décision ajoutée après le commit qu’elle désigne, datée artificiellement de 2031 | Acceptée par l’audit. La chronologie narrative n’est pas contrôlée dans cet essai. |
| Commit d’une autre branche, non ancêtre de main | Refus sur main pour les deux types de baseline. Sur la branche qui en descend, audit accepté : la condition contrôlée est l’ascendance de HEAD courant. |
| Legacy baseline plus récente que authorities baseline | Audit accepté. Les deux mécanismes sont distincts ; leur ordre seul ne constitue pas une contradiction démontrée. |
| Avancer les deux baselines en réutilisant les anciennes décisions | Audit accepté ; commit direct refusé par protection de Project State. Le parcours gouverné de F-08 établit séparément l’enregistrement possible du déplacement. |

Matrice et journaux : `runs/t08/results.json:1–76`. Les décisions invalides ou sans rapport sont documentées par `runs/t08/logs/0043-python3.14.log:1–32`, `runs/t08/logs/0046-python3.14.log:1–32`, `runs/t08/authorities-unrelated/docs/governance/HUMAN_DECISIONS.md:1–58` et `runs/t08/logs/0052-python3.14.log:1–32`. La contre-épreuve d’ascendance est `runs/t08/logs/0065-python3.14.log:1–32` / `runs/t08/logs/0069-python3.14.log:1–32`. L’exemption du Run récent est `runs/t08/logs/0142-python3.14.log:1–32` / `runs/t08/logs/0147-python3.14.log:1–32`. Le comportement sur l’autre branche suit la formulation `HEAD` du README ; il n’est pas classé comme un défaut supplémentaire de la canonique.

### T-09 — Deux sessions simultanées

Trois lancements sans instrumentation créent WI-001 et WI-002 depuis la même copie propre. Les deux commandes refusent dans les trois cas ; **deux copies restent cohérentes, la troisième garde une entrée de roadmap et de registre sans Work Item correspondant** (`runs/t09/logs/0031-python3.14.log:1–12` à `runs/t09/logs/0033-python3.14.log:1–32`). Trois répétitions ne donnent pas une fréquence statistique de panne.

Dans la course ordonnancée, A s’arrête après mémorisation des anciens octets de HUMAN_DECISIONS, avant sa première écriture. B crée WI-002 et committe avec succès. A reprend, échoue et restaure les anciens octets : HD-103 manque désormais dans le dossier de travail alors qu’elle existe dans le commit de B. L’audit échoue (`runs/t09/logs/0037-python3.14.log:1–12` à `runs/t09/logs/0041-python3.14.log:1–32`). SIGINT envoyé à A après le succès de B reproduit la perte sur disque (`runs/t09/scheduled-interruption-2-agent-A.log:1–38` / `runs/t09/logs/0049-python3.14.log:1–32`).

Deux créations du même identifiant ont aussi été amenées ensemble au point de commit. Une rencontre le verrou d’index Git, l’autre ne trouve plus rien à committer après la restauration concurrente ; les deux refusent et l’audit final constate un WI sans décision (`runs/t09/commit-agent-B.log:1–17` / `runs/t09/logs/0088-python3.14.log:1–32`). Le verrou propre à Git n’assure donc pas, dans ce scénario, la restauration cohérente des fichiers du contrôleur.

Les témoins séquentiels tiennent : deux WI peuvent être autorisés ; démarrer le second alors que le premier est actif est refusé sans mutation des fichiers, du HEAD, de la branche ou du statut observés. Les deux intégrations et clôtures, exécutées ensuite successivement, passent (`runs/t09/results.json:1–70`).

Enfin, un `start` suspendu après capture du HEAD, puis repris après un `idea add` concurrent committé, réussit avec l’ancien `start_head`. Les deux transitions et l’audit passent (`runs/t09/more-results.json:1–22`). Cela démontre une capture au début de la transition, sans actualisation au dernier tip avant son commit. L’écriture intercalée est administrative ; aucune omission de changement métier n’a été démontrée par ce témoin.

### T-10 — Export suivi et sélection visible

Le premier projet provient d’un vrai `git archive` du HEAD source, extrait sans `.git`. Le second est copié depuis les seules entrées visibles au premier niveau, en conservant intégralement les répertoires sélectionnés. **C’est une reproduction de la sélection visible, pas une manipulation du Finder par l’interface.** Le premier export contient 119 fichiers, le second 118 ; le seul perdu est `.gitignore`. Les 118 fichiers communs gardent les mêmes octets et les mêmes bits d’exécution (`runs/t10/copy-comparison.json:1–962`).

Les deux projets reçoivent une baseline Git autonome et une gate installée. Ils passent tous deux bootstrap-audit, bootstrap-closeout, le passage explicite à COMPLETE et l’audit normal. Dans le second, bootstrap-preflight refuse cependant `.gitignore` : l’initialisation ne peut pas le rétablir par son allowlist (`runs/t10/logs/0035-python3.14.log:1–35` à `runs/t10/logs/0042-python3.14.log:1–32`).

Après COMPLETE, `roadmap-view --write` réussit avec l’export complet, mais échoue sans `.gitignore` parce que son propre HTML est un chemin inexpliqué. Ce HTML reste sur disque ; l’audit suivant échoue également (`runs/t10/logs/0047-python3.14.log:1–18` à `runs/t10/logs/0024-python3.14.log:1–11`). `git check-ignore` confirme séparément la perte des règles pour `.env`, `.DS_Store` et la vue HTML ; aucun secret ni fichier personnel n’a été utilisé.

Le README décrit l’intention « exporter l’arbre suivi », sans fournir dans « Try it » une commande d’export directement exécutable. Cela explique le choix technique de `git archive` dans ce contrôle, sans prétendre prouver le comportement de toutes les configurations du Finder.

### T-11 — Corrections et comportements adjacents

| Scénario rejoué | Résultat indépendant en 3.16.2 |
|---|---|
| Architecture DRAFT / ADR PROPOSED avec notices de validation | Closeout refusé ; documents effectivement validés acceptés. |
| WI encore ouvert sous une décision REJECT figée | Audit, actualisation de lecture et clôture refusés. |
| Programme sortant réellement code 1 avec seulement ERROR | Sa preuve PASS est refusée. |
| Assertion réellement échouée avec traceback | Sa preuve PASS est refusée. |
| Unittest réellement réussi avec ERROR et `errors=1` attendus | Code 0, clôture et audit acceptés. |
| Unittest réellement échoué avec FAILED | Clôture refusée. |
| FAILED puis OK dans une seule pièce / dans deux pièces | Une pièce refusée ; deux pièces acceptées, conformément au contrat actuel. |
| Installation depuis un worktree lié sans hook commun préalable | Hook installé au chemin que Git consulte ; vrai commit interdit refusé, HEAD conservé. |
| Index invalide masqué par un disque honnête, snapshot disponible puis indisponible | Vrais commits refusés dans les deux cas ; HEAD conservé dans la panne injectée. |
| Passager de fusion visible, puis indexé mais absent du disque | Deux vrais commits refusés ; fusion propre acceptée après retrait du passager. |
| Fichier supplémentaire seulement sur disque pendant la fusion | Commit refusé aussi : le changement de comparaison vers l’index n’efface pas ce contrôle. |

Les sorties, codes retour et témoins sont dans `runs/t11/results.json:1–141` ; les preuves décisives sont détaillées au registre ci-dessous. Un audit PASS après un `close` refusé laisse le WI IN_PROGRESS : **il ne valide pas la preuve refusée**.

**Montée historique.** Un projet autonome est réellement créé depuis `v3.6.1`. Deux WI documentaires vivent chacun création, démarrage, travail committé, intégration et clôture, avec gates techniques explicitement NOT_APPLICABLE. WI-000 reste la fixture synthétique d’initialisation ; ce ne sont pas trois cycles indépendants. La baseline est déclarée puis la procédure spéciale d’adoption sur la canonique est suivie : ancien `--apply`, nouveau `--seed-required`, langue/style et installation de gate. L’ancienne version refuse naturellement `--seed-required` avant la montée. Les deux cycles sont plus petits que les quatre cycles métier de la seconde passe : leur résultat ne reproduit pas toute cette ancienne campagne.

Le premier audit avant indexation refuse les nouveaux chemins non suivis. Une contre-épreuve indexe explicitement les fichiers comme le prévoit le README : **l’audit passe avant le commit**, sans override de cet audit. Le commit d’adoption du core réclame le mandat canonique documenté ; il réussit avec cette dérogation explicite. L’audit et le manifeste passent après adoption, les cinq anciens records WI/Run conservent leurs empreintes et un nouveau WI-003 est réellement démarré puis clos sous 3.16.2. L’ancienne impasse de fichiers requis n’est pas retrouvée (`runs/t11-upgrade/results.json:1–27` à `runs/t11-upgrade/logs/0063-python3.14.log:1–32` ; détails de la contre-épreuve dans `runs/t11-upgrade/staging-results.json`).

**Limite restante de lecture des preuves.** Un programme imprime `OK: configuration chargée`, puis lève une exception réelle et termine code 1. La seule sortie de ce programme, citée exactement avec son empreinte dans une preuve PASS, permet DONE et audit PASS (`runs/t11/logs/0058-python3.14.log:1–10` / `runs/t11/logs/0064-python3.14.log:1–12`). Le contrôleur interprète le OK de préparation comme un verdict de réussite. Cette ambiguïté suit la reconnaissance textuelle annoncée ; elle est conservée comme limite non bloquante, pas comme réouverture du défaut exact « diagnostic sans aucun OK » ni comme preuve d’une authentification d’exécution promise.

### Suite livrée, séparée du contrôle indépendant

**141 tests exécutés, 141 réussis, aucun ignoré**, en 575,307 secondes : `runs/control/suite.log:1–194`. Le lanceur importe les tests inchangés d’une copie. Il adapte uniquement la destination du test de sauvegarde : initialisation du bare et ajout du remote pointent vers `runs/remote.git`, seul push autorisé. Les substitutions sont imprimées dans le journal. Il s’agit de la suite entière avec cette adaptation de confinement, pas d’une invocation strictement inchangée de la commande du mandat.

Le dépôt nu a reçu la branche `main` de cette fixture (`runs/control/remote-final.log:1–3`). Aucun push d’un scénario défectueux, aucune destination distante et aucune protection serveur n’ont été testés. Une suite verte n’annule pas les scénarios indépendants ci-dessus.

## 4. Constats classés par gravité

### F-08 — Majeur, P1 : l’histoire figée peut être défigée, réécrite et réutilisée

**Promesse mise en défaut :** les clôtures antérieures à une baseline déclarée restent figées octet pour octet, jamais reconstruites. L’essai concerne une clôture réellement effectuée sous le produit.

**Scénario exécuté :**

1. Clore WI-001 puis le figer par HD-105. Modifier son objectif sans retirer la baseline : audit et commit refusés (`runs/t08/logs/0055-python3.14.log:1–32`).
2. Créer/démarrer WI-003 avec `project_control/project-state.v1.json` dans ses chemins autorisés ; y mettre `legacy_baseline` à null, committer, intégrer et clore ce WI.
3. Sur main, modifier seulement l’objectif du WI-001 anciennement figé. Le vrai commit passe, avec gate active et audit du disque **et de l’index** (`runs/t08/logs/0113-git.log:1–15`).
4. Par WI-004, réassigner la baseline au commit réécrit, en gardant HD-105. Cette décision nomme toujours la première baseline ; l’audit et la clôture passent (`runs/t08/logs/0126-python3.14.log:1–32` à `runs/t08/governed-unfreeze/project_control/project-state.v1.json:1–27`).
5. Dans une autre copie, retirer les deux baselines par WI-005. Remettre WI-001 dans son état AUTHORIZED précédemment committé, déclarer une nouvelle branche, synchroniser roadmap/registre et retirer l’ancien Run. Une fois ce retrait correctement indexé, le vrai commit passe (`runs/t08/logs/0170-git.log:1–16`).
6. Exécuter `start WI-001`, un autre changement autorisé, son intégration puis `close WI-001` : deuxième DONE, audit final PASS (`runs/t08/logs/0172-python3.14.log:1–12` à `runs/t08/logs/0180-python3.14.log:1–32`).

**Privilèges et limites :** il faut pouvoir faire autoriser un WI qui écrit Project State et éditer les records administratifs sur la canonique. Le scénario ne traverse pas des permissions système. Les nouvelles décisions autorisent un périmètre de fichier ; aucun contrôle ne les lie ici à une autorisation explicite de refaire la clôture historique. Après préparation initiale des baselines, aucune dérogation au hook, aucun patch du contrôleur ni réécriture de l’historique Git n’est employé. Les anciens commits restent récupérables ; c’est leur statut de référence intangible dans le contrôle courant qui est perdu. La commande `start` seule refuse correctement un DONE (`runs/t08/logs/0149-python3.14.log:1–12`).

L’avancement d’`authorities_baseline` sur un Run privé de sa preuve illustre la même absence d’ancrage de la déclaration, mais son état initial a été fabriqué avec une dérogation administrative ; il ne reçoit pas la portée du parcours gouverné ci-dessus.

### F-09 — Majeur, P1 : la restauration d’une transaction concurrente corrompt l’état courant

**Promesse mise en défaut :** les conséquences administratives sont committées atomiquement, et un échec restaure l’état sans conséquences partielles.

**Scénario minimal sans instrumentation :** partir d’une copie propre initialisée, gate active ; lancer ensemble deux `create-work-item` avec des WI et HD distincts. Dans la troisième copie, les deux processus sortent en erreur, sans avancer HEAD, mais la roadmap et le registre gardent WI-001 dont le fichier n’existe plus. L’audit refuse cet état (`runs/t09/logs/0031-python3.14.log:1–12` à `runs/t09/logs/0033-python3.14.log:1–32`).

**Scénario déterministe :** suspendre A à `FileTransaction.write_bytes`, après capture de l’original HUMAN_DECISIONS et avant écriture ; laisser B créer et committer WI-002 ; reprendre A. B avait annoncé un commit atomique. L’échec de A rétablit le texte antérieur à B, retirant HD-103 sur disque ; le commit de B est toujours HEAD et le WI de B existe encore (`runs/t09/logs/0037-python3.14.log:1–12` à `runs/t09/logs/0041-python3.14.log:1–32`). Une interruption SIGINT à la même fenêtre et une collision au point de commit produisent aussi des états incohérents.

**Impact et limites :** un succès annoncé par une session n’assure plus que le checkout reste cohérent après l’arrêt de l’autre. Les commandes suivantes sont bloquées par l’audit. Le commit de B conserve la décision, donc aucune perte irréversible de son historique Git n’est affirmée. Le scénario ordonnancé explique l’interférence des restaurations ; le scénario sans instrumentation établit que le défaut n’est pas créé par la trace du laboratoire. Aucun contenu d’entrée invalide ni privilège d’administration de `.git` n’est requis dans les trois courses libres.

### F-10 — Modéré, P2 : l’initialisation accepte l’absence d’un fichier nécessaire au parcours normal

**Scénario exécuté :** copier les entrées visibles du squelette, créer Git, installer la gate et effectuer toutes les étapes de FIRST_START. `.gitignore` est absent, mais bootstrap-closeout et l’audit COMPLETE passent (`runs/t10/logs/0037-python3.14.log:1–36` / `runs/t10/logs/0042-python3.14.log:1–32`). L’écriture de ce fichier est refusée par bootstrap-preflight (`runs/t10/logs/0035-python3.14.log:1–35`). La première génération de la vue échoue ensuite parce que son HTML n’est pas ignoré, laisse le HTML sur disque et rend l’audit suivant négatif (`runs/t10/logs/0047-python3.14.log:1–18` / `runs/t10/logs/0048-python3.14.log:1–32`). Le même parcours fonctionne avec l’export complet (`runs/t10/logs/0024-python3.14.log:1–11`).

**Portée :** défaut de détection précoce et de robustesse du démarrage, sans perte de données démontrée. Le geste de sélection visible est reproduit par copie de fichiers ; les interactions du Finder et ses attributs étendus ne sont pas attestés. Ce constat ne prétend pas que l’export Git documenté perd lui-même `.gitignore`.

## 5. Observations non bloquantes et hypothèses restantes

- Le contrôle de baseline vérifie un commit existant et son ascendance de HEAD, ainsi que la présence d’une décision structurée ; les essais montrent qu’il ne lie pas la déclaration au SHA, à l’intention ni au choix AUTHORIZE de cette décision. L’interprétation historique et la protection du fichier Project State sont deux contrôles différents.
- L’ordre chronologique des deux baselines ne suffit pas à démontrer une contradiction : elles couvrent des objets distincts. Les états testés sont explicités, sans inventer une obligation d’égalité entre elles.
- Le `start_head` resté ancien après un ajout d’idée concurrent est observé ; aucun faux résultat métier n’en a été déduit. Une modification métier intercalée n’a pas été exécutée dans ce scénario.
- Un OK de préparation peut neutraliser la lecture du diagnostic d’un crash. Ce contrôle reste une heuristique sur le texte ; il ne valide pas l’exécution ni la portée sémantique de la ligne OK.
- La vue refusée sans `.gitignore` annonce `READ_ONLY: true` alors qu’un HTML demeure sur disque. C’est une conséquence observée de F-10 ; le contrôle n’a pas recherché toutes les autres fenêtres d’échec de génération.
- Les refus retrouvés en T-11 et les témoins positifs ne démontrent pas une absence de tout défaut adjacent dans les fusions, l’adoption ou les autres gates de preuve.

Aucune hypothèse non reproduite ne fonde le verdict. Aucun correctif ni proposition de code produit n’est inclus.

## 6. Ce qui n’a pas été vérifié, et pourquoi

- Le Finder lui-même : sélection visible reproduite au niveau des fichiers, sans pilotage graphique. Les préférences d’affichage, métadonnées macOS, ACL, quarantaine et attributs étendus ne sont pas mesurés. L’intégrité comparée porte sur les octets et bits d’exécution des fichiers communs.
- Une utilisation durable par deux humains ou deux LLM : les processus concurrents exécutent les commandes du contrôleur, avec un nombre borné de courses. Il n’y a ni mesure probabiliste de fiabilité ni exploration de tous les ordonnancements.
- Toute la matrice des transitions sous concurrence : créations distinctes et identiques, conflits de commit, second start actif, start intercalé, deux intégrations successives et interruption sont couverts ; pas toutes les combinaisons block/resume/close entre worktrees distincts ni toutes les pannes OS.
- L’authenticité humaine des décisions, des horodatages et des témoignages : fixtures déclarées, sans authentification externe.
- La répétition intégrale de la seconde campagne historique à quatre chantiers métier : T-11 crée deux vrais cycles documentaires sous 3.6.1, conserve cinq records et termine un nouveau cycle sous 3.16.2. Aucun test métier de production ni ancien mois d’usage réel n’est prétendu.
- Les gates de déploiement et de runtime, encodages multiples, épuisement mémoire, réseau et environnements de production : hors des expériences exécutées. La lecture indépendante de preuves vise la gate tests.
- L’absence absolue d’effets internes aux runtimes et caches système, ou l’identité des dates d’accès : non observables par les inventaires retenus.

Les copies incohérentes sont laissées volontairement en l’état. Leurs refus ne sont pas corrigés pour embellir le résultat. Tous les processus de campagne sont terminés à la livraison.

## 7. Registre des preuves décisives

Les lignes sont physiques, comptées depuis 1. Chaque empreinte SHA-256 porte sur le fichier entier ; les plages ci-dessous permettent de relire les commandes, sorties et codes retour sans dépendre d’un résumé. `runs/control/meta/log-index.json` indexe en complément les 617 journaux recensés lors de la vérification. Les matrices de résultats sont des aides à la navigation ; les logs d’exécution restent les pièces primaires.

| ID | Objet | Fichier et lignes | SHA-256 du fichier entier |
|---|---|---|---|
| S-01 | État de départ, tags, audit et manifeste | `runs/control/preflight.log:1–124` | `3d31ed390ca129edecf3984700e067d06bef869e92d543fd31dccefde04db866` |
| S-02 | Source avant/après, contenu et permissions | `runs/control/meta/source-verification.json:1–8` | `af834f7b5de9f239f3a108c93ba1b0aade76446f7357b34496b71b84d2b89f08` |
| S-03 | Intégrité de 46 arbres de contrôle | `runs/control/meta/core-copies.json:1–278` | `dd1473ada20a0ade0ba8fe4e28a185ecbe8efca3e9809a6adaf9a224fe0b0147` |
| S-04 | Suite livrée complète | `runs/control/suite.log:1–194` | `19573f3c94138a5b6773cea75579500ea3211b8fcb99c8e946c400d7c9b3ac70` |
| S-05 | Remote local final | `runs/control/remote-final.log:1–3` | `c34210340cfaa22b64c2d42e03d9780e322067e4f901b1e130930255e46487ee` |
| 08-01 | Réécriture figée refusée par audit | `runs/t08/logs/0055-python3.14.log:1–32` | `cfdfbb70762fc1d016927e743ddca41e8033b83bc24572d70ce0845a4abd3ff5` |
| 08-02 | Refus du commit direct de Project State | `runs/t08/logs/0060-git.log:1–13` | `3894fcdb0059cc2e416fb5df36e3cfa657f7248d86b038dbc55778c227e91cbd` |
| 08-03 | Changement gouverné de baseline, commit accepté | `runs/t08/logs/0106-git.log:1–16` | `f33fa69e4876b9527dd3487ddce04b6c3515f9322ebb0ad9f4eacc47fda07333` |
| 08-04 | Ancien record réécrit et réellement committé | `runs/t08/logs/0113-git.log:1–15` | `fc6680712c39aa7854a1c8c178042f2a7d316bf99492053d8703d72baacf67a7` |
| 08-05 | Nouvelle baseline sous ancienne décision, audit PASS | `runs/t08/logs/0126-python3.14.log:1–32` | `ef3a73f701916bbc88905ff8e29e91e4c96b324a26a9225fdd73eb9113d220ba` |
| 08-06 | Décision historique HD-105 conservée | `runs/t08/governed-unfreeze/docs/governance/HUMAN_DECISIONS.md:1–81` | `8df8a05ad65e63a82aabb386dfe6904719e35185ab3e223b3e028c271757e384` |
| 08-07 | État refixé sur un nouveau commit | `runs/t08/governed-unfreeze/project_control/project-state.v1.json:1–27` | `99bebcc333a249094bf454517c60b7f374a735e1c18c1cb54d2fece8c476e0fe` |
| 08-08 | Réutilisation de WI-001 et retrait de son ancien Run, vrai commit | `runs/t08/logs/0170-git.log:1–16` | `cbe5dfb4bbafbcf922f4d37759a83873d192c94ae3de7defd0cbabef485770a8` |
| 08-09 | Nouveau démarrage du même WI-001 | `runs/t08/logs/0172-python3.14.log:1–12` | `17423b205c699b21d11fc7c7cb8287d30eac0404b11ac8434ae9e9e5a67f7840` |
| 08-10 | Deuxième clôture DONE de WI-001 | `runs/t08/logs/0179-python3.14.log:1–12` | `50b47ab441cc3f3ba48c0cbe9d76108fed58491c42527ed485c99f21e2afe0be` |
| 08-11 | Audit final après deuxième clôture | `runs/t08/logs/0180-python3.14.log:1–32` | `9dd1425890b0c71139d1ff7e0df6a75b448a14c98b6311f8a2c101267bb73e9a` |
| 08-12 | Refus du start direct sur DONE | `runs/t08/logs/0149-python3.14.log:1–12` | `a29ca91195cd8cd8a84758f55f739df11cbcc8a8112aaf3ff820e8f29ab4153c` |
| 08-13 | Run récent sans lecture, audit refusé | `runs/t08/logs/0142-python3.14.log:1–32` | `fc2bc79403c09bc8d0375f4394df763071d476ae9bcd3933e00a19d713e41cde` |
| 08-14 | Même Run exempt après déplacement de baseline | `runs/t08/logs/0147-python3.14.log:1–32` | `ecb24f9a5dd9cea53b06a16df450377505808e660d30d88cd48997f48b6a2813` |
| 08-15 | Legacy baseline citant REJECT, audit accepté | `runs/t08/logs/0043-python3.14.log:1–32` | `3d1740a20012e1825623a813d9a0ed76088e5eb3b740db36907090210e56eeb9` |
| 08-16 | Authorities baseline citant REJECT, audit accepté | `runs/t08/logs/0046-python3.14.log:1–32` | `55faeedd00311f3e69fa6e604be872d5e2ab89751b868cb7eb16ec12cb092f4d` |
| 08-17 | Décision sans rapport avec adoption | `runs/t08/authorities-unrelated/docs/governance/HUMAN_DECISIONS.md:1–58` | `5435b62e7631280c613e87fb1e2191bb418db37c8722c72eb15cca8701072411` |
| 08-18 | Baseline sans autorisation pertinente, audit accepté | `runs/t08/logs/0052-python3.14.log:1–32` | `4b390102a89a73926365f474281e9e1b6adad4da16e4900c800b6f3db1d6c368` |
| 08-19 | Baseline non ancêtre de main, refus | `runs/t08/logs/0065-python3.14.log:1–32` | `772f0c5eee986602e2c7c3007a6a67f0da3ac5d2fe52b7353d1436e69deffbce` |
| 08-20 | Même baseline sur autre branche, acceptation | `runs/t08/logs/0069-python3.14.log:1–32` | `9b935db011c1d0f70b964607169590d24d69fd273cc530d1ae129e45806f6292` |
| 08-21 | Matrice des deux baselines | `runs/t08/results.json:1–76` | `20e97591b140af11d57820ef4c0b712bd123a68ad3a61eea5ecd97b2378398ed` |
| 09-01 | Création simultanée A, sans instrumentation | `runs/t09/logs/0031-python3.14.log:1–12` | `5af63a1035c0d60ff381b2857de89857143cb722b3751ed5d2bf2770d9adfab9` |
| 09-02 | Création simultanée B, sans instrumentation | `runs/t09/logs/0032-python3.14.log:1–12` | `a393ca9aa911aabade3133d2ba0773aef9cee8c29f50d76b7a80e592574e68cc` |
| 09-03 | État incohérent après les deux refus | `runs/t09/logs/0033-python3.14.log:1–32` | `01dfc047e8f705770896b51b0407f9c2b805a2bd9395681d787d4142858817e5` |
| 09-04 | B réussit et annonce son commit atomique | `runs/t09/logs/0037-python3.14.log:1–12` | `52e3afab8203dbb4874a03705febb3b7db06f1784a7c99dea454cb3fca38a58e` |
| 09-05 | A échoue après B et restaure ses anciens octets | `runs/t09/scheduled-rollback-2-agent-A.log:1–11` | `0f0ec22eb88f7d2c315a04fe5c643d0afc52c0e0a933639e38b851c5c0fee220` |
| 09-06 | HD-103 perdue sur disque après rollback de A | `runs/t09/logs/0041-python3.14.log:1–32` | `1f66e35bf6fa67cc807fbdb5575ece2550868a51d9578687eb9c53c3bf2fd538` |
| 09-07 | Interruption réelle de A | `runs/t09/scheduled-interruption-2-agent-A.log:1–38` | `99fbf42a79f1386c50712561f4a648c68b1d4acbbc6c5cbaa2833639e7a19fd9` |
| 09-08 | État incohérent après interruption concurrente | `runs/t09/logs/0049-python3.14.log:1–32` | `c9c78b6b2a8a40fe44dd9f60bcdcc9edfcb6e4945c3207446f8b2cc8fc642138` |
| 09-09 | Deux transitions arrivant ensemble au commit | `runs/t09/commit-agent-B.log:1–17` | `b549c3a39f847e1dac2a3f08632a331f914e8ddce7aa7ec64b1df98810d36e01` |
| 09-10 | État après collision de commits | `runs/t09/logs/0088-python3.14.log:1–32` | `decd6ed41f972d70f318bbf67c0e4ec16b7fe6fd124d079fa66f98000a329649` |
| 09-11 | Deuxième chantier actif refusé sans mutation | `runs/t09/results.json:1–70` | `6b3d57901971c8f454acd4187a402306e5a435a001e90bdde0e1e85006dae243` |
| 09-12 | Démarrage concurrent, start_head et état final | `runs/t09/more-results.json:1–22` | `368acd458950dff02a6e9afac2d77297aa343b881ad25908d311403574203cdd` |
| 10-01 | Comparaison des deux modes de copie | `runs/t10/copy-comparison.json:1–962` | `8d1d82d7a34339a27ea09ae2ec9c4f78ffd45e08872da3a489df0681c01dc031` |
| 10-02 | Écriture bootstrap de .gitignore interdite | `runs/t10/logs/0035-python3.14.log:1–35` | `68ff97b34e913219f19b416f163678aa5460e7f4910dc5d91d61e351296b9925` |
| 10-03 | Closeout accepté sans .gitignore | `runs/t10/logs/0037-python3.14.log:1–36` | `6fa2117aaffbfbb6418e02a5f834c8b454093c1b38e09b3bd944e1c56fd64bfa` |
| 10-04 | Audit COMPLETE accepté sans .gitignore | `runs/t10/logs/0042-python3.14.log:1–32` | `b666ac32e3796de5128effd70047f622f985bbd5ac29b6c249b93ff8fa3baa2c` |
| 10-05 | Vue de suivi refusée sans .gitignore | `runs/t10/logs/0047-python3.14.log:1–18` | `117e6d21dcf69f7df7455d55a85bb23639b529314ad067194c44a4e7564ba5b0` |
| 10-06 | Audit ensuite refusé, fichier HTML résiduel | `runs/t10/logs/0048-python3.14.log:1–32` | `9a3480c6dcdef3f318d2f96dd86e7db64ddcec9cde4fd5285bfd1d2cad262339` |
| 10-07 | Vue de suivi acceptée pour export complet | `runs/t10/logs/0024-python3.14.log:1–11` | `8a195eb3aeb63855fbebd8382d532e888489526532bb78936d15fd4736fa8d04` |
| 11-01 | Brouillons avec notices refusés | `runs/t11/logs/0096-python3.14.log:1–36` | `e33b155f8cf8deb436e6b4deb6ef21c29ceb8cae616e94e2e87ff0e42aa2b9f9` |
| 11-02 | Clôture sous REJECT refusée | `runs/t11/logs/0135-python3.14.log:1–12` | `e62eb615c00b4943d4c58ab8a21d998d5b706434f2fe23af54712c8a1bb7cd7b` |
| 11-03 | Programme ERROR terminé code 1 | `runs/t11/logs/0026-python3.14.log:1–6` | `14c5213c32362461dad743b09cb3ea44f7bb633b30fb1238727f8cbcf80c4a77` |
| 11-04 | Sa preuve PASS refusée | `runs/t11/logs/0032-python3.14.log:1–12` | `c8ac3255df693d699623bb39085f97c615320060524676da26219da176d597ee` |
| 11-05 | Test réussi malgré ERROR et errors=1 | `runs/t11/logs/0042-python3.14.log:1–12` | `965ebe242eaa85902836ecec824f6cb0106b37060b7991fc93c2c12a5a129215` |
| 11-06 | Sa clôture acceptée | `runs/t11/logs/0048-python3.14.log:1–12` | `5873651a291ddf3ea1aca186d70b0ee002182ec2175ede70262d5441e8aa4a11` |
| 11-07 | Installation en worktree, commit interdit refusé | `runs/t11/logs/0147-git.log:1–12` | `b16b9000930c0d93e258574664c0ef00f11cac092173c12348d049974a0cc1ef` |
| 11-08 | Snapshot indisponible, vrai commit refusé | `runs/t11/logs/0167-git.log:1–13` | `37c7635bfa753d690c719f9fdcf39aef983faddc83bec9ab4e8d0231e9aef93e` |
| 11-09 | Passager indexé mais absent du disque, fusion refusée | `runs/t11/logs/0197-git.log:1–12` | `a4f4f3959e0523241733257a2c8ef86795a5c56ba3634cbf366b9dce7add6cb6` |
| 11-10 | Fusion propre acceptée | `runs/t11/logs/0201-git.log:1–13` | `cf311aa141a8fe3626d4bc5f8f953f7bd5b2db30ef4bb3265360e8a60a3c2b9d` |
| 11-11 | Montée historique, étapes exécutées | `runs/t11-upgrade/results.json:1–27` | `118d224c5b35d8691b4eeea3406de8b4ec453b252934348bab13ba2e4623e8bc` |
| 11-12 | Cinq records anciens inchangés | `runs/t11-upgrade/historical-preservation.json:1–10` | `b02c71f786064ee59e55f2de042c055f3f29f803aa6cc3d91788bbb7ebe8c5ad` |
| 11-13 | Audit avant commit après indexation explicite | `runs/t11-upgrade/logs/0073-python3.14.log:1–32` | `ca8adc20e40fc091153e76c2bd7c1e8076a7a26ebb9ee4f2f5c3c1ac82cd75b7` |
| 11-14 | Nouveau chantier clos après montée | `runs/t11-upgrade/logs/0063-python3.14.log:1–32` | `f750c37d61c3832e9434a7ab7380f401aa7f9b0090bdfda1925157643babbf21` |
| 11-15 | OK de préparation suivi d’un crash, code 1 | `runs/t11/logs/0058-python3.14.log:1–10` | `311c919f3933462f06d2580d15598c551e9c138acfae3ab5b514cce6608088cd` |
| 11-16 | Cette pièce unique permet pourtant DONE | `runs/t11/logs/0064-python3.14.log:1–12` | `b253634403fcb161e4a70bc156c4a2256e4143fc9f7c3731d9817ad0c0df865d` |
| 11-17 | Résultats détaillés et témoins T-11 | `runs/t11/results.json:1–141` | `a2a585857feddd65865677dafed0d0b96a9c93d9c8ad3b76176c66bc89ef2fe5` |

Les copies principales sont `runs/t08/`, `runs/t09/`, `runs/t10/`, `runs/t11/` et `runs/t11-upgrade/`. `runs/control/` contient les copies de référence et de suite, les inventaires, les dispositifs d’essai et la vérification finale. Pour reproduire une transition, repartir d’une nouvelle copie de sa baseline de préparation ; exécuter de nouveau `close` sur un état déjà DONE ne reproduit pas son histoire. Les commandes exactes et leurs répertoires sont dans les journaux. Les scénarios F-08 à F-10 décrivent les ordres de manipulation ; les ordonnanceurs T-09 conservent les fenêtres de pause utilisées.

## 8. Verdict

SQUELETTE_3.16.2_REQUIRES_MAJOR_REDLINE
