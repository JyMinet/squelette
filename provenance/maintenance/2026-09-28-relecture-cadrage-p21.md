> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

## Résumé en trois points

1. **Ce qui s’est passé.** La reprise dispose maintenant d’une référence vérifiée : les 138 fichiers correspondent au manifeste, les 24 fichiers du core sont alignés, et l’arbre Git recalculé correspond à celui annoncé. Onze sondes ciblées et un test existant ont été exécutés dans `runs/`. Le premier constat reste inchangé.
2. **Ce que ça change.** Le tableau proposé aide réellement à retrouver les copies et leurs preuves, mais il n’est pas prêt à être construit tel quel. Le contrôle des branches oublie le travail non committé ; les anciennes preuves ne protègent pas contre une reprise après retour ; un chemin parent de l’original n’est pas exclu de l’effacement. La reconnaissance des exports et l’ordre entre retour et promotion demandent aussi une correction. Bilan : un constat BLOCKER, quatre MAJOR et deux MINOR.
3. **Ce qu’il faut faire.** Corriger les sept points de la section E avant de lancer la construction, puis trancher les sept questions de la fiche avec les avis de H. La promotion sans commit de fusion reste possible : l’essai l’a confirmé. Rien n’est à supprimer ni à transférer à ce stade ; aucun travail d’implémentation n’a été entrepris.

# Relecture indépendante — Tableau des clés V1 — révision liée V2

Date : 2026-09-28. Révision du constat `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V1.md`, conservé octet pour octet. La V2 lève son blocage matériel d’entrée manquante et fournit la relecture de fond ; elle ne réécrit ni son verdict historique ni l’écart de lecture qui y était déclaré.

Posture : `READ_ONLY / REPORT_ONLY`. Les propositions de la fiche sont des objets de relecture, pas des instructions de construction ou de sortie du dossier. Aucune autre relecture n’a été consultée. Les références de lignes ci-dessous visent les fichiers immuables de ce dossier ; « fiche » désigne le document de la racine. Les sondes testent des primitives existantes ou les conditions écrites de la proposition : elles ne simulent pas l’existence d’une commande `copy` implémentée.

## A — Preflight

### A.1 — Périmètre et pièces retenues

Dossier accordé : `~/Projets/squelette-revue-tableau-des-cles/`, exclusivement. La demande de reprise autorise le présent fichier V2 et les essais dans `runs/`. L’export `source/`, les deux papiers, la note de provenance, le manifeste et le premier constat restent en lecture seule. Aucun accès à l’atelier, aux archives, à un autre dépôt ou à Downloads pendant cette reprise.

La note `SOURCE-PROVENANCE.md` tranche l’ancien écart de noms : les papiers de la racine sont ceux initialement joints sous le suffixe V1_1. Ils gardent ici leurs noms V1 et comportent **sept** questions. Le mandat et la fiche ont été lus à ces emplacements, sans revenir aux pièces jointes externes.

Le fichier V2 était absent au preflight ; `runs/` était vide. Aucun obstacle `OUTPUT_ALREADY_EXISTS`.

### A.2 — Vérification de la référence

Contrôle initial, puis contrôle rejoué et consigné à `2026-09-28T15:12:14.638495+00:00` :

| Contrôle | Résultat |
|---|---|
| Manifeste externe | 138 entrées, 138 fichiers présents, zéro absent, zéro supplémentaire, zéro empreinte divergente |
| Liens et historique dans `source/` | Aucun lien symbolique ; aucun `.git` |
| Version du manifeste core | `3.20.2` |
| Intégrité du core | 24 entrées, zéro dérive ; normalisation de FIRST_START conforme à `core_digest` |
| Arbre Git recalculé depuis fichiers et modes | `fb1390aa83d1c4472d7e742afc62a79580d4d38e`, identique à la note |
| Commit déclaré par la note | `9b8792e1ef453869105bd0edc2cc085120bbf404` pour `v3.20.2` |
| Premier constat | 12135 octets, empreinte inchangée |

Limite précise : les octets et l’arbre de l’export ont été vérifiés indépendamment dans le dossier accordé. Le lien **tag → commit → arbre** est celui déclaré par la note ; l’objet commit, le tag et leur historique ne sont pas fournis dans cet export. Aucun accès à l’atelier n’a été effectué pour les consulter. Cette limite ne rend pas l’export incomplet au sens du mandat, qui demande précisément une archive sans `.git`.

Le SHA-256 de `SOURCE-MANIFESTE.sha256` est `a0c1ea0d49c0741e23b427d427630569b2478e8a8ed250cc8d971dbd5891f102`, conforme à la note. Le manifeste contient l’inventaire exhaustif des empreintes des 138 fichiers contrôlés ; `runs/results.json`, entrée `preflight.source_sha256`, conserve le résultat recalculé.

### A.3 — Empreintes des pièces et des lectures principales

| Fichier | Octets | SHA-256 |
|---|---:|---|
| `FICHE-CADRAGE-TABLEAU-DES-CLES-V1.md` | 23252 | `d1b3df340e21c0e7dee80ee170f4cbb131e2f4041092717c1db9d6556d111e50` |
| `MANDAT-RELECTURE-TABLEAU-DES-CLES-V1.md` | 5770 | `76c9fa90aafac2d0c87873152aaae66976aa4fbbd9a37a44b6f4e66c0c4e277c` |
| `SOURCE-PROVENANCE.md` | 2171 | `ac97eb57b0f6059e5d3e2913ccd39f24487e659b183e4752fe17bd2fd990f931` |
| `SOURCE-MANIFESTE.sha256` | 15648 | `a0c1ea0d49c0741e23b427d427630569b2478e8a8ed250cc8d971dbd5891f102` |
| `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V1.md` | 12135 | `da5c28e91decba6598b13578c92c51bac92c5635748945f14bc3ca29ceccf11f` |

Les chemins du tableau suivant sont relatifs à `source/`. Les lectures de fond ont été ciblées sur les textes de doctrine, les fonctions du contrôleur pertinentes et les tests associés. Le contrôle cryptographique exhaustif de l’export ne doit pas être présenté comme une lecture intégrale des 394650 octets du contrôleur ou des 415294 octets de la suite de tests.

| Fichier | Octets | SHA-256 |
|---|---:|---|
| `AGENTS.md` | 802 | `7988c37fde271411896963a81c9c2f20aa2657252bef9efac2400450d5047b49` |
| `FIRST_START.md` | 7394 | `fd16f922c0ed1c737f7025ae2443c93c72c233cd4eb0c0853d22e702fcad5eb3` |
| `docs/agent-governance/AGENTS.core.md` | 31212 | `bc82f3f502949dd6c407f94493bd0d1b6a801d47b55e1d784fd08e927a89fa6f` |
| `docs/agent-governance/mandatory-documents.v1.json` | 2750 | `4e0edab1fc1e131d4a6435a42bc1ccbf54baa86ee1e072269cd0be7501445923` |
| `docs/governance/HUMAN_DECISIONS.md` | 3365 | `6b68b10e82216de9cd69b65929c1a3057d86c198eaa6118f56b51beb24dc9f08` |
| `docs/governance/REPOSITORY_STATUS.md` | 1270 | `55630b3da9021602951aa67fb649c72bdd5fcaae651c97e70c1047a5859d3f54` |
| `docs/governance/STORAGE_POLICY.md` | 1246 | `9e9f4fa6636a834569138e54a62fb124e64b9b39b61770e5df447282870c7d43` |
| `docs/governance/RECOVERY.md` | 1544 | `349802175c70c8817f341b05eef28d644bf2f36ce5bb4c81d8ca7edfa8caedde` |
| `docs/agent-governance/ROADMAP_VIEW.md` | 6649 | `c825b3c0e8adf7685078ca2f30667a913722e31fe589f81c9f170ad2f19e6a96` |
| `scripts/project_control.py` | 394650 | `21294605fd1e396adeb12077a945ee42c9754f0ee39d45c3d458f280ca30e080` |
| `project_control/README.md` | 46189 | `59c86a5dd93944ed8a0d649c2ba3e69267337f3cb37e178a67e6d20a15caf653` |
| `provenance/core-manifest.v1.json` | 2821 | `8f5bd4239766ad7c15d87ee281ec34f775d73c8ddd22a473a10ada8654d07a36` |
| `provenance/CHANGELOG.md` | 228044 | `a8f51401f525d2ba06785700757767c0ac49ee4c333d8a70a2821276d12f90be` |
| `tests/test_template.py` | 415294 | `3d86e3552089e1c5c0ed87da1969a058293d8563a4a76e9021416b2ccb010426` |

Les autres fichiers lus automatiquement par le contrôleur dans sa copie d’essai, et les fixtures existantes lues par le test, sont couverts par le manifeste exhaustif vérifié. Aucune autre relecture sous `provenance/maintenance/` n’a été ouverte pour en utiliser les conclusions.

### A.4 — Exécution et preuve

`runs/replay_review.py` conserve dix sondes P01–P10 ; `runs/promotion_order.py` et `runs/promotion-order.json` ajoutent la sonde P11 sur l’état figé par le tag ; `runs/commands.json` conserve les commandes Git locales et leurs sorties ; `runs/results.json` conserve les mesures. `runs/supplement_review.py` et `runs/supplement-results.json` conservent le contrôle de routage et l’exécution d’un test existant, dont le journal est `runs/existing-test.txt`.

Tout le matériel de rejeu est identifié « FIXTURE DE RELECTURE — FICTIF, N’AUTORISE RIEN ». Les trois petits dépôts Git créés sont synthétiques, sans remote configuré ; les transferts entre eux sont locaux, dans `runs/`. Leurs branches de travail sont `codex/fixture-review` et `codex/fixture-promotion`. Les tags `v0.0.1`, `v0.0.2`, `fixture-before-return` et `fixture-after-return` sont des valeurs fictives locales. Ces dépôts minimaux servent à vérifier la topologie Git ; ils ne sont pas des projets initialisés avec une gate Project Control. Aucun commit, tag, branche, installation de hook ou changement de source n’a eu lieu dans `source/`.

La suite complète n’a pas été lancée : la proposition n’est pas implémentée. Le test existant exécuté est `test_out_of_folder_decision_requires_two_distinct_confirmations` : **1 test réussi**, sans création de décisions réelles. Les autres résultats sont des sondes de relecture, pas onze tests d’acceptation de la future fonctionnalité.

## B — Inventaire et cohérence avec l’existant

### B.1 — Ce qui existe et doit être réutilisé (T-02)

| Besoin de la fiche | Existant vérifié | Conséquence |
|---|---|---|
| Records canoniques, transaction, rollback, concurrence | `AGENTS.core.md:73–81` ; contrôleur `544–555`, `645–698`, `4490–4498`, `4566–4618` | Étendre la classification des deux chemins ; réutiliser le verrou pris avant la lecture et le commit explicite. Ne pas écrire un deuxième moteur de transactions. |
| Ticket HD et double arrêt | Contrôleur `997–1008`, `1080–1176`, `6006–6017` ; test `4785–4820` | Résoudre la décision dans les deux volumes, puis vérifier son admissibilité ; l’existence et un chemin ne suffisent pas à transformer un refus en autorisation. |
| Restriction de branche | Contrôleur `4095–4140`, `6588–6598` ; test `5268–5287` | La règle vise les **changements administratifs** sur la branche, pas la simple présence d’un record hérité de la canonique. |
| Empreintes et ancêtres Git | `file_sha256`, `blob_digest`, `run_git` ; clôture `6434–6459` | Réutilisables ; la portée des preuves reste à définir pour toutes les données à sauver. |
| Vue et identification du rôle template | Contrôleur `2451–2475`, `2516–2525` ; README `228–230` | Le template et un projet dérivé ont déjà des sources de vue distinctes. Ajouter le registre aux sources qui rendent la vue périmée. |
| Lecture des autorités | Contrôleur `113–123`, `3546–3577` ; README `101–105` | Un registre non routé n’ajoute pas de document à la preuve. Les décisions humaines et la doctrine restent lues. |
| Adoption sans reconstruction du passé | Core `387–400`, README `243–245`, montée `3929–3944` | Registre absent traité comme vide ; ne pas l’ajouter aux fichiers obligatoires ni recopier le registre du template dans un projet. |
| Nettoyage protégé | Storage Policy `5–14` ; README `312` ; contrôleur `645–655` | Préserver ce qui est unique ou inconnu. Le contrôleur sait déjà nettoyer ses propres worktrees jetables prouvés siens : leur régime doit rester séparé des copies déclarées par le propriétaire. |

« Jamais de suppression » est ici la préférence de la fiche pour ces copies et l’autorité du geste humain. Ce n’est pas une description littérale de tout le contrôleur 3.20.2, qui retire déjà ses worktrees techniques temporaires. Il n’y a pas à reconstruire ce nettoyage ni à le faire entrer de force dans les nouveaux tickets.

### B.2 — Adaptations nécessaires, sans les confondre avec des bugs actuels

Les quatre verbes `copy`, le registre et `COPIES_RETURNED` n’existent pas dans 3.20.2. Leur absence n’est pas une redline : c’est précisément l’objet proposé.

Le « même précédent que les idées » doit être nuancé. Le template stocke ses idées dans `provenance/roadmap-template.v1.json` ; `idea` vise les records de projet et ne committe automatiquement qu’en `NORMAL_MODE` (contrôleur `2376–2431`). Le template exporté porte `NOT_STARTED`, `PROJECT_TEMPLATE` et une branche canonique `UNKNOWN` dans ses documents vierges. P01 confirme que `canonical_branch()` refuse, et que **les deux nouveaux chemins** ne sont pas encore administratifs. La vue possède déjà un cas particulier `main` pour le template (`2664–2672`), pas un protocole universel utilisable sans adaptation.

Le futur cahier d’implémentation doit donc prévoir le chemin template, le chemin projet, leur branche de référence et leurs contrôles respectifs. Il ne faut pas initialiser artificiellement le template comme un projet pour obtenir `NORMAL_MODE`. Le test 11 devra couvrir les deux rôles ; l’interdiction générique actuelle n’est pas déjà la protection des nouveaux chemins.

## C — Rejeu des scénarios et analyse des six thèmes

### C.1 — Résultats des sondes

| Sonde | Résultat observé | Portée exacte |
|---|---|---|
| P01 — Décisions et chemins administratifs | Une HD fictive bien formée donne son `Folder scope` et aucune erreur ; `TPL-D-075` donne `null` ; zéro ligne structurée `^Folder scope:` dans CHANGELOG. Les deux nouveaux chemins sont non administratifs actuellement. | Le parseur HD est réutilisable ; un lecteur TPL-D structuré reste à définir. Aucun journal de projet réel extérieur n’a été lu. |
| P02 — Export sans Git | `status --json` exécuté sur une copie de l’export dans `runs/` : code 1, `root=UNKNOWN`, `head=UNBORN`, erreurs `GIT_REPOSITORY` et `GIT_TRACEABILITY`, aucun champ copies. | Comportement actuel normal pour une archive sans historique. Ce n’est ni une erreur du preflight de la revue ni une preuve que la future bannière serait impossible. |
| P03 — Réparation après audit rouge | Une erreur `COPIES_RETURNED` injectée **en mémoire** dans le helper existant fait refuser `validate_clean_administrative_baseline`. | Prouve le problème d’une réutilisation inchangée du pré-audit. Ce n’est pas l’exécution d’un futur `copy return`. |
| P04 — Export d’un ancien tag | Un enregistrement d’ouverture symbolique committé après un tag existe à HEAD mais pas dans l’archive de ce tag. | Prouve qu’enregistrer avant de copier ne fait pas entrer le ticket dans un ancien tag. |
| P05 — Retour après tag et fast-forward | Livraison locale, `merge --ff-only`, tag, puis commit symbolique de retour : succès, zéro commit de merge, tag ancêtre de main. | La topologie Git n’oblige pas à une fusion. Les contraintes de l’audit et les écritures ultérieures dans l’original sont un sujet distinct. |
| P06 — Branches rendues, contenu restant | Tous les tips de branches sont contenus dans l’original ; pourtant `M delivered.txt` et `?? unique-note.md` restent uniquement dans la copie. | Les prédicats de branches de §5.5 ne couvrent pas le contenu non committé. |
| P07 — Reprise après retour | Ancien commit toujours présent et ancienne empreinte toujours exacte dans l’original ; nouveau commit de la copie absent de l’original. | Les seules anciennes preuves de §5.8 ne détectent pas cette reprise. Aucun effacement exécuté. |
| P08 — Fichier suivi mais nouvelle version non committée | Fichier présent, suivi et empreinte du worktree exacte ; HEAD ne contient pas ces octets. | « Suivi par Git » n’est pas « version sauvegardée dans Git ». Le prérequis de checkout propre, s’il est réutilisé, ferme déjà ce cas : observation D-O2, pas redline autonome. |
| P09 — Chemin ancêtre | Le chemin cible n’est ni égal à l’original ni contenu dans lui ; l’original est contenu dans la cible. | Les exclusions écrites en §5.3 ne rejettent pas ce cas. Aucun dossier dangereux créé ou supprimé. |
| P10 — Événement de clôture | La règle écrite vaut FAIL pour `OPEN` + cible déjà close, PASS pour `RETURNED`/`KEPT`. | Table de vérité de la proposition, pas résultat d’un audit futur. Éclaire le cas d’une décision déjà enregistrée et la fenêtre après tag. |
| P11 — État figé au tag | Dans un troisième dépôt fictif, le tag avant retour contient `OPEN`, le tag après retour contient `RETURNED`, zéro commit de merge. | Démonstration Git sur un texte symbolique, pas sur un registre implémenté. Le premier tag conserverait l’incohérence du prédicat de §5.7 même après réparation de main. |

Rejeux conservés, non nettoyés : le script principal refuse naturellement de recréer ses répertoires déjà présents. Pour une nouvelle exécution, un autre sous-dossier `runs/` devra être choisi ; il n’existe aucun nettoyage automatique de ces preuves.

### C.2 — Chaque règle ferme-t-elle un scénario réel ? (T-01)

| Règle | Scénario visé et gain réel | Chemin qui reste ouvert |
|---|---|---|
| 5.1 — Registre | S1 : inventaire, responsabilité, sort et échéance deviennent retrouvables. S3 : conservation des preuves de retour. | Copies non déclarées invisibles ; le registre ne protège pas à lui seul un dossier contre des changements ultérieurs. Champs de provenance à préciser pour identifier l’original et la copie. |
| 5.2 — Nom | S1 : réduit les ambiguïtés de classement. | Ne ferme mécaniquement aucun cas de perte ou de second original ; c’est une convention ergonomique. L’annexe ne respecte pas la référence fermée (R06). |
| 5.3 — Ouverture | S1/S0 : rattache le dossier à un ticket et annonce son sort avant usage. | Ancêtres, chevauchements et identité réelle insuffisamment exclus (R01). Admissibilité du ticket à réutiliser en entier ; le contrôle TPL-D reste à définir. |
| 5.4 — Bannière | S2 : signale l’identité de copie lorsqu’un registre approprié a effectivement été emporté. | Export historique sans ticket, archive imbriquée dans `source/`, déplacement et état local périmé (R04). Une bannière n’interdit pas de travailler. |
| 5.5 — Retour | S3 : vérifie les commits déclarés et les papiers de revue, mandate explicitement conservé. | Fichiers non committés, branches/états non inventoriés, papier de chantier livré ou de répétition non déclaré (R02). |
| 5.6 — Fin | S1 : distingue rendu, conservé et dossier absent au chemin enregistré. | Chemin absent ne prouve pas effacement après renommage ou démontage ; un chemin réutilisé ne désigne plus nécessairement la même copie. `KEPT` doit rester incompatible avec un ancien script d’effacement (R03). |
| 5.7 — Clôture | S1/S3 : refuse un WI fini avec clés encore ouvertes et détecte une cible déjà close. | Retour après tag contraire à l’ordre annoncé et réparation non définie ; cible décision déjà existante (R05). Pas de surveillance : un tag créé directement n’est détecté qu’au prochain contrôle. |
| 5.8 — Script humain | S1 : donne un chemin concret de rangement ; S3 : revalide les preuves connues. | Les preuves anciennes peuvent rester vraies alors que le contenu ou le sort de la copie a changé (R03). Un script lancé par l’humain peut quand même effacer la mauvaise portée (R01). |
| 5.9 — Adoption | Évite le blocage rétroactif d’un projet et la reconstruction de fausses preuves. | Les copies existantes restent un inventaire humain, pas un problème résolu automatiquement. L’import volontaire de copies conservées et celui de l’annexe doivent avoir une règle explicite. |

La promesse générale de §3 doit être lue comme « toute copie **déclarée** ». La limite de §6 le reconnaît déjà ; aucun contrôle ne rendra universel un inventaire déclaratif sans inventaire supplémentaire.

### C.3 — Configurations dégradées (T-04)

| Cas demandé | Ce que dit la fiche | Jugement et traitement nécessaire |
|---|---|---|
| Export sans `.git` | L’annexe en fait le premier cas ; §5.4 suppose pourtant un registre dans le dossier exécutant `status`. | Insuffisant, R04. Retour documentaire possible depuis l’original, mais bannière et origine doivent distinguer dossier de revue et export intact. |
| Copie déplacée ou renommée | Perte de bannière reconnue ; ancienne entrée fermée, nouvelle ouverte. | Acceptable comme limite d’affichage, insuffisant pour appeler l’ancienne copie `ERASED`. Il manque un lien de relocation ou une correction d’emplacement préservant la provenance. Le script ne doit pas se fier au seul ancien nom. |
| Deux copies pour un ticket | Suffixes `-2`, `-3` prévus. | Acceptable si deux identifiants COPY et deux retours indépendants ; la clôture doit examiner toutes les copies de la cible. Le principe « une copie = un ticket » ne doit pas être interprété comme unicité inverse. |
| Copie contenant ses clones de rejeu | `runs/` part avec la revue. | Acceptable pour des fixtures explicitement jetables ; rapports et papiers uniques doivent être extraits avant le retour. Un clone d’un vrai chantier ne devient pas jetable par simple emplacement dans `runs/`. |
| Chemin sur un autre volume | §6 déclare que l’outil ne voit pas d’autre disque. | Ambigu pour un volume monté accessible par chemin absolu. Décider support ou refus à l’ouverture. Un volume démonté est indisponible, pas une preuve d’effacement. Aucun accès à un autre volume pendant cette revue. |
| Dossier humain accordé plus large | §6 admet un parent, alors que §5.3 parle d’exactitude. | Peut être acceptable avec un périmètre humain explicite et une vraie comparaison de chemins résolus ; ni sous-chaîne ni parent supposé. Harmoniser la prose. Cela ne dispense jamais d’exclure un ancêtre de l’original (R01). |
| Projet adoptant avec copies existantes | Registre vide et non-reconstruction ; choix humain. | Bon principe. Maintenir absence=vide et séparer toute entrée volontaire `KEPT` de l’invention d’un retour historique. Non qualifié de bout en bout sur un vrai projet dans ce mandat. |

### C.4 — Faisabilité mécanique dans 3.20.2 (T-03)

**Lire une HD et son dossier : oui**, à partir d’un bloc `## HD-NNN` puis d’un champ unique (`human_decision_field`, `1144–1161`). `decisions_text`, `6006–6017`, résout les deux volumes. Le test existant du double arrêt a réussi. Le modèle livré est vierge : aucune affirmation n’est faite sur les décisions d’un projet réel non fourni.

**Lire un TPL-D comme une HD : non.** Le journal porte des puces `- TPL-D-NNN`, en prose (`CHANGELOG.md:17–40`, `803–814`), pas les blocs/champs du parseur HD. P01 trouve zéro ligne structurée `Folder scope:` dans tout le journal. Des chemins et confirmations sont présents dans la prose (`924–928`) : leur présence n’est pas un format de champ fiable. Il faut un format futur structuré et un lecteur dédié, ou une décision explicite sur une capacité dégradée honnêtement nommée ; pas une prétendue vérification déjà existante.

**Lire des branches et vérifier l’ascendance : oui**, avec les primitives Git existantes, sans réseau. `run_git` fixe le répertoire (`2035–2036`) ; `for-each-ref` est déjà employé (`2611–2622`) et `merge-base --is-ancestor` est courant (`6434–6459`). P05–P07 en font usage dans deux dépôts locaux. Un objet absent ou un dépôt inaccessible doit rester un refus, pas une branche considérée rendue par omission.

**Enregistrer après un tag en gardant un fast-forward : oui pour la topologie Git.** P05 a un historique linéaire et `main` un commit après le tag. Un précédent réel est décrit dans le journal exporté : `CHANGELOG.md:796–798`, vue régénérée après tag. Cela ne résout ni R05, ni une autre écriture canonique intervenue pendant le chantier : ouvrir une seconde copie dans l’original pendant que la première travaille peut faire diverger les branches. La promesse « ticket avant copie » ne porte que sur cet enregistrement initial.

**Bannière depuis le chemin réel : réalisable, non existante.** `ProjectControl.__init__` résout déjà sa racine (`2021`), et `status_payload` expose contexte et erreurs (`6313–6391`). La donnée `<original>` et l’identification du dossier de revue doivent toutefois être disponibles ; un `root_commit` partagé par des clones ne fournit ni chemin original ni identité physique de la copie. R04 décrit le cas que le seul registre hérité ne couvre pas.

### C.5 — Coût (T-05)

« Aucun nouveau document Markdown à lire » (§3) est compatible avec le routage actuel. La sonde supplémentaire donne **sept autorités de base**, dont `HUMAN_DECISIONS.md`, et aucun registre `copies-state`. Le registre proposé peut rester hors de cette preuve.

« Zéro lecture supplémentaire » ou « il ne coûte rien au démarrage » est trop large : `status` doit lire le nouveau registre pour le compter ; l’agent doit assimiler la nouvelle doctrine ajoutée au core ; les tickets ajoutés au carnet humain restent dans l’autorité lue, et peuvent rendre périmée une preuve de lecture en cours (core `123–141`). Il n’y a pas nécessairement un nouveau fichier à lire par l’agent, mais il y a du texte et du traitement supplémentaires. Le journal du template, lui, n’est pas routé : cette limite existante demeure.

Par copie, le parcours normal ajoute au moins : `open` et ses **six arguments nommés**, `return` avec les commits ou papiers/empreintes nécessaires, `close` ; s’y ajoutent la génération groupable du script et son exécution humaine pour les copies à effacer. Le nombre de preuves et de branches à justifier varie. Aucune nouvelle approbation humaine ordinaire n’est nécessaire si le ticket existant couvre déjà l’action, mais le travail de preuve n’est pas contenu dans les seuls arguments de `open` (R07).

### C.6 — Options écartées (T-06)

| Option | Scénario ou préférence ? | Avis |
|---|---|---|
| Branches seules | S0 : pas de séparation des dossiers. | Écart pertinent pour isoler le terrain de travail. Une copie n’empêche physiquement une écriture dans l’original que si les permissions/outils la limitent effectivement : le simple fait de copier ne retire aucun accès. |
| Worktrees Git | Partage d’objets, de configuration commune et de remotes. | Écart cohérent pour les copies humaines devant être autonomes. Les worktrees jetables internes du contrôleur restent un autre cas déjà qualifié, à conserver. |
| Fichier marqueur | Réduction des écritures et réutilisation du registre. | Préférence de conception ; un marqueur créé dans le cadre déjà accordé de la copie n’exige pas automatiquement une nouvelle autorisation. L’alternative par registre hérité doit réellement couvrir les exports (R04). |
| Jumeau Markdown | Coût de synchronisation et de lecture. | Préférence raisonnable ; `status` et vue générée peuvent suffire. |
| Effacement par l’outil | Maintien du geste humain demandé. | Choix cohérent avec l’autorité de la fiche. Le script fourni doit rester techniquement sûr ; la main humaine ne ferme pas R01–R03. |
| Retard en échec d’audit | S1 sans incohérence de données. | Bon rejet : un retard ne doit pas bloquer les commits qui permettent de le traiter. |
| Inventaire automatique du disque | Complexité et périmètre de lecture. | Bon rejet pour le mécanisme de base. Un scan à la demande peut signaler des candidats, pas prouver l’identité par le seul `root_commit`, ni découvrir tous les exports sans Git. |

## D — Constats

Toutes les redlines ci-dessous sont **OUVERTES** : la revue ne corrige pas la fiche. Les scénarios sont ceux permis par ses conditions écrites ; l’absence de commande `copy` n’est jamais présentée comme un défaut d’implémentation déjà livré.

### R01 — Un dossier contenant l’original peut être déclaré puis proposé à l’effacement

- **Sévérité : BLOCKER.** Objet : fiche §5.3 et §5.8, lignes 118–122 et 153.
- **Scénario reproductible :** prendre un original fictif dans `runs/squelette-chantier-wi-999/original` et déclarer comme copie son parent `runs/squelette-chantier-wi-999`. La cible respecte la forme d’un nom de chantier ; elle n’est ni égale à l’original ni située dans lui. Un ticket autorisant ce chemin ne transforme pas ce contenant en copie sûre. Une fois un retour déclaré, effacer récursivement la cible emporterait l’original.
- **Preuve :** P09 : `target_equal_original=false`, `target_inside_original=false`, `original_inside_target=true`. C’est un contre-exemple aux exclusions listées, sans créer ni supprimer ces dossiers. La règle actuelle ne refuse pas non plus explicitement le contenant d’une autre copie ; seul le sens « contenu dans » est écrit.
- **Impact :** perte possible de l’original ou d’une autre copie, alors que l’opération est présentée comme nettoyage d’une copie rendue.
- **Correction proposée :** exiger des périmètres réellement disjoints, dans les deux sens, entre cible et original et entre copies concernées ; revalider la cible résolue au moment d’exécuter le script. Refuser toute ambiguïté de lien, d’identité ou de disponibilité au lieu de déduire une autorisation d’effacer.
- **Statut : OUVERT — condition impérative avant tout script destructif.**

### R02 — Les branches ne couvrent pas tout ce qui peut être perdu

- **Sévérité : MAJOR.** Objet : fiche §5.5, lignes 134–137 ; scénarios S2/S3.
- **Scénario reproductible :** livrer tous les commits et branches, puis laisser une note non suivie et une modification non committée dans la copie avant `return`. Les vérifications de branches restent vraies. Pour un chantier normalement livré, la fiche ne demande les papiers uniques que dans le cas spécial du chantier arrêté ; une répétition admet même « rien à rendre » sans inventaire préalable.
- **Preuve :** P06 : tous les tips sont contenus dans l’original ; le statut de la copie affiche ` M delivered.txt` et `?? unique-note.md` ; la note n’existe pas dans l’original et les octets du fichier modifié diffèrent. Ces objets ne sont pas couverts par l’ascendance Git.
- **Impact :** la phrase « Rien ne reste dans la copie sans qu’on l’ait dit » n’est pas établie, et des papiers uniques peuvent partir malgré un retour validé.
- **Correction proposée :** distinguer retour des commits et inventaire du contenu à préserver, pour tous les usages. Traiter modifications indexées/non indexées, fichiers non suivis ou ignorés, HEAD détachée et références de travail pertinentes ; exiger sauvegarde vérifiée ou abandon explicite de ce qui n’est pas rendu. Déclarer les zones réellement reconstructibles, plutôt que les assimiler à des données sauvées. Le mandat doit avoir un rôle explicite parmi les pièces déclarées, pas être reconnu par un nom deviné.
- **Statut : OUVERT.** Les cas ignorés, stash et HEAD détachée sont des extensions d’acceptation proposées ; ils n’ont pas été rejoués ici. Le contre-exemple suffisant non suivi/modifié a été rejoué.

### R03 — Un retour ancien n’autorise pas un effacement futur sans relecture de la copie

- **Sévérité : MAJOR.** Objet : fiche §5.6–5.8, lignes 143, 147–153 ; scénarios S2/S3.
- **Scénario reproductible :** rendre la copie, poursuivre le travail dedans, puis exécuter un script qui revérifie seulement les commits et empreintes enregistrés dans l’original. Les anciennes preuves restent bonnes. Variante déductible des transitions : générer le script lorsque la copie est `RETURNED`, puis la passer `KEPT` avant son exécution ; les empreintes peuvent encore être identiques.
- **Preuve :** P07 : `recorded_work_still_present=true`, `recorded_file_hash_still_matches=true`, alors que le nouveau commit `e9129fda24c1502d3ef792fb0f6e17b05e312a9f` est absent de l’original. Aucun effacement n’a été exécuté. La variante `KEPT` découle des états de §5.6 et de l’absence de relecture explicite du registre courant en §5.8.
- **Impact :** reprise perdue, dossier conservé supprimé, ou ancien chemin réutilisé traité comme l’ancienne copie. Le choix de garder la copie peut être contredit par un script devenu périmé.
- **Correction proposée :** à l’exécution, relire l’état canonique courant, l’identité et le contenu de la cible, vérifier qu’elle est encore `RETURNED` avec sort d’effacement, et comparer son inventaire actuel à celui justifié au retour. Refuser toute nouveauté, cible remplacée ou source indisponible. Coordonner l’absence d’écritures concurrentes pendant la dernière vérification et l’effacement ; ne pas promettre que relire seulement l’original ferme cette fenêtre. Définir une nouvelle validation du retour si la copie a changé.
- **Statut : OUVERT.**

### R04 — Le registre emporté ne couvre pas la copie de revue par export d’un tag

- **Sévérité : MAJOR.** Objet : fiche §4.5, §5.4, annexe A, lignes 78, 128 et 223–226.
- **Scénario reproductible :** ouvrir une revue d’une version déjà taguée dans l’original, puis exporter exactement ce tag, comme le prévoit l’annexe et comme le présent dossier a été préparé. Le ticket, enregistré après le tag, n’est pas dans l’export. En outre, le dossier de revue est le parent de `source/`, alors que le contrôleur résout sa racine à l’intérieur de l’export.
- **Preuve :** P04 : le fichier symbolique d’ouverture est présent à HEAD mais absent de l’archive du tag précédent. P02 : un export sans Git n’a pas le contexte de dépôt de `status`. La source actuelle a précisément cette forme autorisée ; elle n’est pas une entrée défectueuse.
- **Impact :** la première catégorie de copie de la fiche ne peut pas bénéficier de la garantie « la copie sait qu’elle est une copie » par la seule mécanique annoncée. Le `root_commit` n’est ni accessible dans toute archive ni l’adresse de l’original. Un registre initial emporté reste par ailleurs un instantané, pas l’état actuel de l’original.
- **Correction proposée :** définir séparément copie Git de HEAD et dossier de revue contenant un export immuable. Prévoir un contexte/ticket de revue dans le contenant, fourni lors du geste humain de préparation déjà autorisé, ou limiter explicitement la garantie de bannière. Ne pas modifier l’archive historique ni déplacer le tag pour y introduire un ticket. Nommer l’original dans la provenance, et préciser que l’état local affiché peut être périmé.
- **Statut : OUVERT.**

### R05 — L’ordre de clôture et sa réparation sont contradictoires

- **Sévérité : MAJOR.** Objet : fiche §4.4, §5.7, §9, lignes 77, 148 et 199 ; contrôleur `4566–4570`.
- **Scénario reproductible :** suivre §5.7 : promouvoir/taguer avec une copie encore `OPEN`, puis rendre. L’audit devient alors FAIL, alors que §4.4 interdit justement de promouvoir avant le retour. Si `copy return` reprend le pré-audit des transitions administratives, il refuse l’état qu’il devrait corriger. Même après un retour réussi sur main, une relecture du commit tagué retrouve le registre `OPEN` hérité par la branche : l’audit de cette référence immuable rencontrerait encore la condition d’échec. Avec `closes_with` égal à une décision déjà enregistrée, l’ouverture produit immédiatement la même incohérence.
- **Preuve :** contradiction d’ordre explicite entre lignes 77 et 148 ; P03 : le helper actuel refuse la mutation lorsque l’unique erreur injectée est `COPIES_RETURNED`. P10 confirme la condition logique. P05 montre que le problème n’est **pas** l’impossibilité d’un fast-forward. P11 montre les états symboliques figés au tag avant et après retour ; l’échec du futur `COPIES_RETURNED` sur le premier est une déduction du prédicat écrit, pas un audit nouveau exécuté.
- **Impact :** la phase de retour peut exiger un contournement global du contrôle, ou laisser un état rouge sans voie normale de réparation. Un main réparé ne répare pas les octets déjà tagués. La présence d’un identifiant de décision ne dit pas à elle seule qu’un chantier futur est clos.
- **Correction proposée :** fixer un ordre unique et distinguer intégration autorisée et promotion achevée. Une séquence à cadrer est : rapatrier et vérifier, intégrer par fast-forward sous le mandat de promotion, enregistrer le retour sur la canonique, puis figer le tag de la promotion achevée sur un état aux clés rendues. P11 démontre que cet ordre reste linéaire. Il demande de reformuler §4.4, pas de prétendre que déplacer main est sans enjeu d’autorité. Écrire le retour dans l’ancien main avant son fast-forward créerait au contraire une divergence avec la branche : ce n’est pas la solution proposée. Si le retour après tag est conservé, résoudre explicitement aussi l’audit de la référence taguée, et définir une voie de réparation limitée avec validation de l’état résultant. Distinguer ticket d’ouverture et événement de clôture ; rejeter à l’ouverture une cible déjà close, ou définir expressément le cas de régularisation. Préserver les refus d’audit sans rapport avec la réparation.
- **Statut : OUVERT.** La commande future n’existe pas : le refus montré concerne le helper actuel sous injection, pas une implémentation supposée.

### R06 — La première copie de l’annexe ne satisfait pas la règle de nommage

- **Sévérité : MINOR.** Objet : fiche §5.2, §5.3, annexe A, lignes 110, 122, 223–226.
- **Scénario reproductible :** tenter de convertir la ligne `squelette-revue-tableau-des-cles` en entrée créée par `copy open` suivant la grammaire écrite. `tableau-des-cles` n’est ni numéro de chantier, ni version, ni identifiant de ticket. Pourtant l’annexe annonce que ses lignes deviennent les premières entrées du registre.
- **Preuve :** comparaison directe de la référence fermée de la ligne 110 avec le nom de l’annexe ; aucun parseur futur n’a été inventé pour prétendre à un refus d’exécution.
- **Impact :** l’adoption par ce chantier demande une exception non définie ou une donnée réécrite a posteriori ; la traçabilité des premières copies peut être trompeuse.
- **Correction proposée :** nom conforme pour les ouvertures futures ; pour cette copie déjà autorisée, règle explicite d’import historique sous décision, conservant son nom et sa provenance réels, sans inventer un ticket numérique antérieur. Aucune proposition de renommage ou d’écriture ailleurs n’est exécutée par la revue.
- **Statut : OUVERT.**

### R07 — Le coût annoncé omet une partie du parcours

- **Sévérité : MINOR.** Objet : fiche §5.1/§5.10, lignes 86 et 161.
- **Scénario reproductible :** parcourir les verbes requis pour une copie rendue puis effacée. En plus des arguments de `open`, il faut les preuves de `return`, la génération et l’exécution du script, puis `close`. L’ouverture de session via `status` doit lire le registre nouvellement affiché.
- **Preuve :** commandes et arguments de §§5.3, 5.5, 5.6 et 5.8 ; `status_payload` exécute l’audit (`6313–6315`) ; le manifeste supplémentaire de la revue montre sept autorités de base, dont le carnet humain, sans registre de copies.
- **Impact :** une décision de cadrage peut sous-estimer le travail administratif et confondre absence de nouveau document obligatoire avec absence de coût.
- **Correction proposée :** annoncer « aucun nouveau fichier d’autorité routé ; une lecture automatique du registre et trois transitions par copie, plus les preuves et le nettoyage humain ». Distinguer le coût du registre, celui des décisions déjà exigées et celui de la doctrine ajoutée.
- **Statut : OUVERT.**

### Observations sans redline autonome

- **D-O1 — Cas template :** adaptations concrètes décrites en B.2. Ce sont des travaux nécessaires, pas la preuve que le nouveau mécanisme serait irréalisable. Les placer dans les essais d’acceptation.
- **D-O2 — Fichier suivi versus version sauvegardée :** P08 le distingue. La reprise exacte de la règle de checkout propre de `AGENTS.core.md:75` et du helper `require_clean_worktree` ferme déjà le contre-exemple pour un retour dans le dépôt. Il faut l’écrire dans le contrat de preuve et l’essayer ; pas réinventer une autorité. Un archivage externe ne bénéficie pas de cette protection Git et doit annoncer sa garantie plus faible.
- **D-O3 — Provenance du registre :** `origin` ne nomme pas explicitement le chemin de l’original, alors que la bannière veut l’afficher. Des clones partagent le même commit racine ; ce n’est pas une identité physique. Précision à intégrer dans R03/R04, sans multiplier les constats.
- **D-O4 — Imports et relocalisations :** `KEPT` pour les copies antérieures et fermeture de l’ancienne entrée après déplacement demandent un protocole qui conserve l’histoire. Ne pas qualifier « effacé » un dossier simplement déplacé ou momentanément inaccessible. Pas de constat sur un autre disque effectivement observé : aucun n’a été consulté.
- **D-O5 — Droits de la copie :** le registre indique, il ne révoque pas l’accès à l’original, au réseau ou aux remotes. La limite d’envoi de §6 est honnête ; la même précision doit accompagner le mot « physiquement » de §7.

## E — Redlines proposées et critères de fermeture

Ces redlines sont des corrections textuelles proposées dans ce rapport, non des edits de la fiche.

| ID | Texte/règle à ajouter ou rectifier | Preuve attendue pour fermer |
|---|---|---|
| R01 | « La cible est disjointe de l’original et des autres copies protégées ; l’égalité et l’inclusion sont refusées dans les deux sens, sur chemins résolus. Ces contrôles sont répétés avant effacement. » | Cas égal, enfant, parent, chevauchement inverse, lien et cible remplacée ; aucun scénario ne produit de suppression de l’original. |
| R02 | « Un retour justifie le contenu utile complet de la copie, pour tous les usages, y compris ce qui n’est pas dans les branches. Un abandon identifie ce qui est abandonné. » | P06 refusé tant que les deux différences ne sont ni sauvegardées ni abandonnées ; cas chantier livré/arrêté, revue et répétition avec papier unique. |
| R03 | « Le script consulte l’état courant et la copie courante ; une preuve ancienne, un changement de sort ou un contenu nouveau invalide l’autorisation de nettoyage. » | P07, script devenu périmé après `KEPT`, contenu non committé apparu après retour, indisponibilité et identité remplacée ; refus avant suppression. |
| R04 | « Une revue par export garde sa source intacte ; son contenant porte le contexte de copie, ou l’absence de bannière est une limite explicite. » | Archive d’un tag antérieur à l’ouverture, export sans Git, `source/` imbriqué, dossier déplacé ; aucune mutation du tag/export. |
| R05 | Un seul ordre retour/clôture/promotion, un événement de clôture typé et une réparation limitée des états incohérents. | Promotion normale et interrompue, audit du commit tagué, reprise après tag si admise, décision déjà enregistrée, cible inconnue ; historique linéaire sans override global pour corriger les seules clés. |
| R06 | Exceptions historiques de nom explicites, ou annexe limitée à des tickets manuels ne prétendant pas satisfaire rétroactivement `copy open`. | Le cas réel de l’annexe possède une voie d’import fidèle et testée, distincte d’une nouvelle ouverture mal nommée. |
| R07 | Coût décrit par acteur : documents d’autorité, lecture automatique, commandes, preuves et geste humain. | Le texte correspond au parcours complet ; aucune promesse de zéro traitement ou de seules options à fournir. |

Ajouter à la campagne prévue : deux rôles template/projet, décisions rejetées/dupliquées/inconnues et HD reliées, registre absent à l’adoption, deux copies pour une même cible, rollback et accès concurrents. Ce sont des extensions des mécanismes existants ; la relecture ne prescrit pas une nouvelle infrastructure.

Les treize essais de la fiche restent utiles. Ils ne suffisent pas à couvrir R01–R05. Les qualifier tous de « rouges sur 3.20.2 » est impropre pour des cas de compatibilité déjà vrais, comme audit sans nouveau registre : séparer les tests de nouvelle fonction, attendus absents avant construction, des tests de non-régression à garder verts.

## F — Blockers et portée du verdict

**R01 est le blocker de sécurité de conception :** la liste de refus ne protège pas l’original lorsqu’il se trouve sous la cible d’effacement. **R02 à R05 sont des redlines majeures :** elles touchent la conservation effective du travail, la reconnaissance des exports et un cycle de clôture exécutable sans contournement.

Aucun blocker d’entrée : la source demandée est présente et vérifiée. Aucune impossibilité générale de Git : le fast-forward suivi d’un commit de retour est démontré. La correction du format TPL-D reste une décision de cadrage à prendre avant d’annoncer une vérification automatique du ticket pour le template.

La phase 0 prévue par la fiche peut donc mesurer utilement, mais ses trois arrêts ne suffisent pas à autoriser la construction de cette V1 : le fait que HD soit lisible n’efface pas le besoin de traiter TPL-D, et la réussite Git ne ferme pas les pertes ou ambiguïtés de cycle constatées ici. Le rapport n’autorise aucun chantier, aucune promotion et aucune sortie de périmètre.

## G — Conflits d’autorité

La demande de reprise fixe le périmètre effectif. `source/AGENTS.md` et son core ont été lus comme doctrine à laquelle comparer le cadrage, sans déclencher une initialisation, une installation de gate ou des écritures administratives dans l’export. Les étapes de la fiche concernant l’atelier, d’autres projets et les archives n’ont pas été exécutées.

Les points à harmoniser sont explicites : « aucune promotion avant retour » contre « retour après tag » (R05) ; exactitude du dossier de §5.3 contre parent accordé en §6 ; héritage supposé du ticket contre export historique (R04) ; « rien ne reste » contre seule inspection des branches (R02). Ce sont des contradictions ou insuffisances **de la proposition**, corrigeables par redline et choix humain, pas une impossibilité de décider quelle autorité gouverne la présente revue.

Le double arrêt du core exige un dossier et deux confirmations (`289–319`) ; la vérification du ticket doit le respecter. Un TPL-D simplement cité ne doit jamais être présenté comme un dossier vérifié. La politique de conservation protège les objets uniques ou inconnus (`STORAGE_POLICY.md:5–14`) : R01–R03 sont nécessaires pour que le futur script respecte ce principe.

Le verdict retenu est une redline majeure, et non `CANONICAL_CONFLICT` : aucune autorité canonique n’a été modifiée, aucune exception au core n’a été décidée ici, et le mandat de relecture est exécutable dans le dossier fourni. L’écart de lecture du premier tour reste consigné dans V1 ; cette reprise n’a effectué aucun accès à l’atelier.

## H — Avis non liant sur les sept questions

1. **Retard : avertissement dans `status`.** Réserver l’échec d’audit à une incohérence démontrée. Afficher la date, les copies concernées et le nombre en retard sans interdire les gestes qui permettent leur retour.
2. **Ticket du template : structurer les nouvelles entrées avant de promettre la vérification.** Le constat n’est plus conditionnel : le journal fourni n’offre aucune ligne `Folder scope:` structurée pour ses TPL-D. Réutiliser le contenu humain et ajouter un format futur ou un complément append-only sous décision, sans réécrire les décisions historiques. Un mode « référence déclarée, chemin non vérifié » ne peut être accepté qu’en tant que garantie explicitement plus faible, et ne remplace pas le double arrêt. Mon avis est de corriger le format.
3. **Copies `KEPT` : oui, sous décision.** Elles restent visibles, exclues du nettoyage, et leur conservation ne signifie pas autorisation de reprendre le travail. Définir l’entrée des copies historiques et la transition si un dossier conservé doit ensuite être effacé ; le graphe actuel le déclare terminal.
4. **`copy scan` : plus tard.** Ce n’est pas nécessaire à la première mécanique fiable. Un inventaire humain ponctuel est possible sur mandat séparé. Un futur scan devra distinguer clones, exports, dossiers imbriqués et copies de même ascendance ; il fournit des candidats à examiner, pas des tickets ni des autorisations.
5. **Copies existantes : choix au cas par cas, sans reconstruction du passé.** Partir d’un registre vide est sain. Pour celles que le propriétaire choisit de conserver, enregistrer un constat présent sous décision et sans retour historique inventé. Toute suppression de ces dossiers reste une décision séparée ; aucun inventaire extérieur n’a été réalisé ici.
6. **Noms : conserver `copy open / return / close / cleanup`.** Ils correspondent aux actions. Rendre la sortie de `cleanup` explicite : il prépare un script, il ne l’exécute pas. Clarifier que `close --state ERASED` constate un effacement accompli, tandis que `KEPT` clôt le suivi actif avec conservation.
7. **Papiers : dépôt par défaut.** Préférer une version committée et identifiable des livrables et du mandat dans le dépôt ; c’est la voie la plus simple à vérifier et à retrouver. Si des archives externes sont admises plus tard sous décision, annoncer « présence et empreinte vérifiées à telle date », sans prétendre à une sauvegarde Git ou à la disponibilité future du volume. Ne pas construire deux garanties indistinctes sous un même mot « rendu ».

## I — État du dossier en fin de mandat

Seuls le présent livrable V2 et des fichiers/répertoires dans `runs/` ont été créés. Le premier constat, les deux papiers, la note de provenance et le manifeste ont conservé leurs empreintes. Les 138 fichiers de `source/` ont été revérifiés après les replays et lors de la remise : aucune différence, aucun fichier ajouté, aucun lien ni cache Python créé.

`runs/` conserve les scripts de sonde, leurs journaux, une copie jetable de l’export et trois dépôts Git fictifs. Les fichiers symbolisant une ouverture ou un retour sont de simples textes de fixture : ils ne sont ni objets Project Control ni décisions humaines. Les fichiers core et fixtures livrés dans la copie d’export sont des copies de l’entrée de test, sans autorité sur un projet réel. Aucun candidat de fonctionnalité `copy` n’a été produit.

Aucun effacement, aucun envoi en ligne, aucun accès à un autre dossier de travail, à l’atelier, aux archives ou à un projet dérivé. Les dépendances système nécessaires à Python et Git sont les seuls composants d’exécution extérieurs, sans lecture de données de projet. Aucun transfert du rapport vers l’atelier et aucune création de décision ou de Work Item réels.

Empreintes des preuves principales conservées :

| Fichier | Octets | SHA-256 |
|---|---:|---|
| `runs/replay_review.py` | 10958 | `afb95767180f610e6ab6a5cfb13dc6393ae43d957bae7782e0e3cd447a59da2f` |
| `runs/results.json` | 21893 | `4a6309f95a712fb5280eea0bf41fe4db33b1779e2b0c9fd2910e727c10c47ce2` |
| `runs/commands.json` | 70760 | `584dc09ead86f992b89bab6cc91b133d2f0f6cd277f033f78d9ea72a9dfac679` |
| `runs/export-status.json` | 698 | `4a59480de8041966c69e4a86cd2121bc9f1e2e16eea5674f0f9f69b4f27a8cd5` |
| `runs/supplement_review.py` | 2063 | `6f62066d6dabfe51fc2367f380295bc7ec6ed6c37e3202e900e02755a2c3dca9` |
| `runs/supplement-results.json` | 580 | `7070b58b7af622164e07d89a0fd6b380e52399deb354f39149242626d2ea8378` |
| `runs/existing-test.txt` | 333 | `ca870cd0746041be9bdbcf74f1058e0417534fdd0cfbca960fd1e000d402babc` |
| `runs/promotion_order.py` | 2379 | `3a788a5615bd2f2147ad13dfa0c8bb482297bf2203d25031f6572df549e4548e` |
| `runs/promotion-order.json` | 3926 | `22e1c2ad3f9facda3937753c8c293639da56a3337053eb192f3bc6a208d230c8` |

Le rapport V2 est publié une seule fois, en création exclusive. Toute correction ultérieure appelle une révision liée ou un erratum. Les fixtures restent disponibles pour vérification et ne sont pas supprimées par cette revue.

## J — Verdict terminal

`CADRAGE_TABLEAU_DES_CLES_V1_REQUIRES_MAJOR_REDLINE`
