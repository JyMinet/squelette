<!-- ROADMAP_VIEW sources_digest=b7987e8418c5a66f32eef194830834a2c6ba8b594a0b2a769ec2fec1f7136b89 generated_at=2026-09-11T13:59:40Z head=40a13677a363b80aff4640fd62f4288d76be9998 -->
# ROADMAP SQUELETTE

Vue générée par `roadmap-view` depuis les fichiers du projet ; elle montre, elle ne décide rien. Ne pas éditer à la main : relancer la commande.

## Vérification

- Vérifié le : 11 sept. 2026, 13:59 UTC
- Comment : le dossier du projet a été lu par le contrôleur, sans rien y modifier
- Version : 3.19.1, la dernière promue — le commit courant n’est pas tagué
- Sauvegardes : en retard : origin, nas
- Vérifications : les contrôles du dossier passent · 164 essais automatiques présents, non exécutés par cette vue
- Mise à jour : chaque jour ; à la demande dans la discussion ROADMAP

## Maintenant

- La version 3.19.1 est la dernière promue ; le dossier n’est pas sur elle. _(source : dossier du squelette (tags))_
- Des sauvegardes distantes sont en retard sur la branche principale : origin, nas. _(source : dossier du squelette (remotes))_
- Les contrôles du dossier passent tous ; les essais automatiques, eux, ne sont pas exécutés par cette vue. _(source : contrôleur, audit du dossier)_
- Aucune branche de travail ouverte : tout est intégré. _(source : dossier du squelette (branches))_
- Le squelette est en 3.19.1 ; Alpha en 3.18.1 (montée du 11 septembre, WI-066), ses deux baselines confirmées par décision (HD-074, HD-075) et la protection de son passé ancrée. Non vérifié par ce tableau : il ne regarde que le squelette. _(source : journal du squelette (TPL-D-057, TPL-D-059, TPL-D-065) ; décisions HD-074 à HD-077 d'Alpha)_
- Cinq passes de contrôle indépendant depuis le 10 septembre : vingt et un défauts démontrés, tous corrigés avec leur essai. La cinquième a trouvé que le rangement des copies jetables de la 3.18.2 pouvait effacer le worktree d'un autre, et qu'un nom accentué échappait à la règle de contenu des fusions — fermés en 3.19.1. Reste une contre-vérification ciblée de ces six corrections, puis une pause sans nouvelle règle. La première copie publique est produite (3.19.1, nom « squelette ») ; la mettre en ligne est un geste du Project Owner. _(source : rapports sous provenance/maintenance/ ; journal du squelette (TPL-D-059, TPL-D-065))_
- 164 essais, chacun né d'un défaut démontré ou d'un usage réel. Deux projets réels vivent sur le squelette en plus du template : Alpha, adopté avec son histoire figée, et « Coût moyen crypto », né gouverné. _(source : journal du squelette ; note de test du 9 sept.)_

## Ce qui t’attend

1. **Publier le miroir : renommer, créer, pousser** la première copie publique (3.19.1) est produite dans ~/Projets/squelette, vérifiée, un commit et un tag, rien d'envoyé. Tes gestes, dans l'ordre : renommer le dépôt privé en squelette-atelier sur GitHub et mettre à jour son adresse origin ; créer le dépôt public squelette, vide ; pousser main et le tag depuis ~/Projets/squelette ; About, Topics, release. Et toujours : l'envoi de la 3.19.0 et de la 3.19.1 du privé vers origin et le NAS, plus leurs releases. _(source : journal du squelette (TPL-D-063 à TPL-D-067))_
2. **Contre-vérification ciblée de la 3.19.1** par le même contrôleur, ses journaux de la cinquième passe en main : les six corrections (F-01 à F-06) et les six phrases de doctrine, rien d'autre — court. Puis une pause sans nouvelle règle : laisser vivre la 3.19 sur Alpha (à monter en 3.19.1, WI à part) et sur le projet neuf. La prochaine passe générale, avec des yeux neufs, juste avant la 4.0.0 publique. _(source : journal du squelette (TPL-D-065))_
3. **Publier les releases GitHub 3.14.0 → 3.16.1** main et les tags sont partis sur origin et nas ; il ne reste que les releases à créer sur GitHub. Les textes sont écrits, un fichier par version dans « Claude outputs ». _(source : journal du squelette (TPL-D-034 à TPL-D-045))_
4. **Décider de la suite après la seconde revue** la seconde revue est rendue et ses sept constats sont corrigés en 3.14.0, avec un huitième trouvé en les vérifiant. Restent à trancher : l'étape 2 de la langue (documents de gouvernance en anglais, une seule langue faisant foi par document), l'ouverture d'une procédure d'adoption pour un dépôt jamais gouverné, et la mise à niveau d'Alpha. _(source : contre-revue de la seconde revue ; journal du squelette (TPL-D-031))_
5. **Approuver la carte de la mise à jour automatique de la ROADMAP** c'est cette approbation qui donne à la tâche du matin l'accès en lecture au dossier ; sans elle, chaque matin dira « non vérifié ». Pour changer le rythme : « RÉGLAGE : regeneration = 4h » (ou off, 1h, daily). _(source : premier passage de la tâche automatique, 7 sept. 23:47 ; fiche P12)_
6. **Enregistrer les deux consignes proposées dans des cartes** « roadmap-squelette » (celle du tableau) et la mise à jour de « squelette-projet » (style de retour et preuve de lecture, pour la 3.7.0). _(source : fiches P12, P11 et P3)_
7. **Alpha : en dernier** sa mise à niveau clôturera la série (« on terminera par la mise à jour Alpha ») : après la 3.8.0 et le challenge de Codex, il montera en une fois vers la version stabilisée, avec le style « simple » — deux confirmations avant, dans une autre discussion. Sa sauvegarde NAS reste à envoyer. _(source : décisions des 7 et 8 sept. ; fiches P11 et P2)_

## Prochaines étapes

- **Après la 3.14.0 :** la mise à niveau d'Alpha, qui adoptera la version stabilisée ; puis l'étape 2 de la langue et, si tu le décides, une procédure d'adoption pour un dépôt jamais gouverné. _(source : décisions du 9 sept.)_
- **Vitrine GitHub, après la promotion :** release GitHub sur la version 3.9.0 (notes depuis le journal), About et Topics (gestes du Project Owner) ; à décider plus tard : messages du contrôleur en anglais (O-11), clôture de l'initialisation sans mandat d'override (O-12). _(source : fiche P10 § 13.4 et § 13.5)_
- **Après la promotion de la 3.8.0 :** republier la page Claude depuis la commande roadmap-view (elle devient un miroir), remplacer les fiches du projet Claude par des pointeurs vers provenance/maintenance/scopes/, mettre à jour les deux consignes (roadmap-squelette, squelette-projet) avec les commandes idea et roadmap-view. _(source : fiche P12 § 12 (plan de migration))_
- **Challenge du squelette par Codex :** après la 3.8.0, en lecture seule sur une version taguée, avec un mandat au format P4 (verdicts fermés, pas de ligne rouge sans scénario d'échec démontré) ; rapport rangé dans provenance/maintenance/. _(source : idée du Project Owner, 8 sept.)_
- **Consignes :** « squelette-projet » (3.7.0) et « roadmap-squelette » proposées ; à enregistrer par le Project Owner ; puis première mise à jour du tableau depuis une autre discussion pour vérifier que la forme reste la même. _(source : fiches P3 et P12)_
- **Documents annexes du squelette** (registre des branches, état du dépôt, README) : à revoir dans une version suivante — même sujet que l'étape 2. _(source : décision du 7 sept. (« plus tard »))_
- **Langue au choix (P14) :** cadrer le périmètre avec le Project Owner, puis livrer comme le style de retour — un choix enregistré à l'initialisation, respecté par le contrôleur et les vues. _(source : son message du 8 sept.)_

## Plus loin

- Revue contradictoire en option (fiche prête, pas lancée)
- Travailler par phases, au-dessus des chantiers
- Critères d'entrée d'un chantier
- Petits points restants : profil d'adoption vérifié, exercice réel de restauration
- Publication, étape 2 (dépôt public, annonce) et extension Claude (plugin) — après un second vrai projet
- Documents de gouvernance en anglais (P14, étape 2)
- Corriger `idea add` dans le squelette lui-même (O-15)

## Tes idées, et ce qu’elles sont devenues

| Quand | Ton idée | Ce qu’elle est devenue | État | Source |
|---|---|---|---|---|
| 2026-09-05 | « Une revue indépendante du squelette, et comment l'intégrer côté Claude » | Revue du 5 sept. (huit axes d'amélioration), consigne « squelette-projet », le projet Claude « Squelette ». → 3.0.0 | réalisée | discussion du 5 sept. |
| 2026-09-05 | « Établir une trame, un suivi efficace, une roadmap » | La ROADMAP en est la première forme ; la fiche P12 la cadre ; la 3.8.0 la met dans le dossier (promue le 8 sept.) ; reste la page Claude en miroir. → P12 | en cours | but du projet Claude, 5 sept. |
| 2026-09-06 | « Faire travailler Codex sur V3, et vérifier si ça me convient » | Contre-revue, corrections, version 3.1.0. → 3.1.0 | réalisée | discussion du 6 sept. |
| 2026-09-07 | « Une sauvegarde sur GitHub (puis le NAS aussi) » | Dépôt privé sur GitHub et copie sur le NAS ; c'est toujours le Project Owner qui envoie. → TPL-D-004 | réalisée | discussion du 7 sept. |
| 2026-09-07 | « L'anglais devra être saisi (un paragraphe en anglais dans le README) » | Version 3.3.0. → 3.3.0 | réalisée | discussion du 7 sept. |
| 2026-09-07 | « Mettre à niveau Alpha vers le squelette enrichi » | Répétition sur une copie, puis mise à niveau réelle vers 3.6.1 (WI-061 d'Alpha). → 3.6.1 | réalisée | discussion du 7 sept. |
| 2026-09-07 | « Jamais le vrai projet comme terrain d'essai : une copie ; deux stop si la consigne fait sortir du dossier » | Règle des deux confirmations (TPL-D-011), version 3.5.0 ; répétitions sur copie. → 3.5.0 | réalisée | discussion du 7 sept. |
| 2026-09-07 | « On ne supprime pas V3, c'est un projet source ! » | Règle : jamais de suppression dans un dossier source ; seuls les fichiers temporaires de Git, et on dit lesquels. | appliquée | discussion du 7 sept. |
| 2026-09-07 | « Proposer le squelette comme extension Claude (plugin) » | Après la publication, elle-même après un second vrai projet. → P10 | plus tard | discussion du 7 sept. |
| 2026-09-07 | « Le style de retour, technique ou simple : ce doit être le choix de l'utilisateur » | Version 3.7.0, promue le 7 sept. : chaque projet retient le choix, la question est posée à la création. → 3.7.0 | réalisée | discussion du 7 sept. |
| 2026-09-07 | « Une discussion dédiée, le tableau de bord de l'avancement, nommée ROADMAP SQUELETTE » | Fiche P12 ; la page publiée en est la première version ; la 3.8.0 met la ROADMAP dans le dossier. → P12 | en cours | discussion ROADMAP, 7 sept. |
| 2026-09-07 | « Régénération automatique toutes les x minutes, l'utilisateur choisira » | Mise à jour automatique chaque jour à 8 h (tâche planifiée, carte à approuver), en plus de la mise à jour à la demande ; modifiable par « RÉGLAGE : … ». → P12 | intégrée | discussion ROADMAP, 7 sept. |
| 2026-09-07 | « Changer certains réglages en faisant appel au squelette ; si risque, on bloque » | Réglages de la vue permis ; tout ce qui touche au projet lui-même est bloqué depuis la discussion ROADMAP. → P12 | intégrée | discussion ROADMAP, 7 sept. |
| 2026-09-07 | « Un tableau simple, lisible par tous, pas pour un ingénieur IT ; et on doit y voir les idées évoquées » | Le tableau suit le style de retour du projet ; le bloc des idées est obligatoire. → P12 | intégrée | discussion ROADMAP, 7 sept. |
| 2026-09-07 | « On va attendre car le squelette se développe, j'ai rajouté encore une fonction » | La mise à niveau d'Alpha est reportée : il montera en une fois vers une version stabilisée, en dernier. | appliquée | discussion P11, 7 sept. |
| 2026-09-08 | « Toutes les infos dans le dossier physique du projet. Format JSON ? » | Fiche P12 étape 2 (fusionnée avec P6) ; recommandations validées ; version 3.8.0 livrée puis promue le 8 sept. → 3.8.0 | réalisée | discussion ROADMAP, 8 sept. |
| 2026-09-08 | « Quand squelette est terminé, on va faire un challenge à Codex » | Revue menée le 8 sept. sur une copie du tag 3.9.0, en lecture seule, mandat au format des revues indépendantes ; rapport rangé dans le dossier (provenance/maintenance/). Deux constats graves reproduits et corrigés en 3.9.1 ; le reste à trancher. | réalisée | discussion ROADMAP, 8 sept. |
| 2026-09-08 | « On terminera par la mise à jour Alpha ! » | La mise à niveau d'Alpha clôt la série : 3.8.0 → challenge Codex → correctifs éventuels → Alpha. | appliquée | discussion ROADMAP, 8 sept. |
| 2026-09-08 | « Améliore le github avec ces remarques de gpt […] Qu'en penses tu ? » | Cadrée comme P10 étape 1 ; quatre décisions le 8 sept. (après la 3.8.0 et avant le challenge Codex ; anglais puis français dans le même README ; démo rejouable vérifiée par un test ; licence MIT) ; 3.9.0 livrée puis promue le 8 sept. L'annonce publique reste pour plus tard, après un second vrai projet. → 3.9.0 | réalisée | discussion « vitrine GitHub », 8 sept. (remarques de GPT sur la présentation du dépôt) |
| 2026-09-08 | « on veut donner la possibilité que le squelette parle anglais et français ! Faut rajouter l'anglais ! Choix de l'utilisateur ! » | Même principe que le style de retour : la langue est un choix du Project Owner, pas une décision de l'agent. Périmètre tranché le 8 sept. : ce que l'IA dit au Project Owner — messages du contrôleur (situation, refus, audits) et vue roadmap ; les documents de gouvernance, les commits, les tags et le journal restent en français. Le choix se fait par une question à l'initialisation, enregistrée dans le projet ; en changer sera une décision humaine. Les documents de gouvernance en anglais sont prévus pour plus tard (étape 2). Chantier P14, à cadrer puis à livrer. | à régler | discussion « vitrine GitHub », 8 sept. |
| 2026-09-09 | « Ok pour la concurrence ! » | Deux agents qui travaillent en même temps sur le même dépôt : jamais essayé. À cadrer comme une revue ou comme un chantier. | évoquée | discussion squelette, 9 sept. |
| 2026-09-09 | « j'ai d'autres projets plus ou moins aboutis, essayer squelette sur un projet déjà lancé est-il ok ? » | La seconde revue a établi la limite : un dépôt jamais gouverné n'a pas de procédure d'import, et l'initialisation refuse le code métier déjà présent sous applications/, modules/ ou shared/. Un projet dont le code est ailleurs passe. À cadrer : ouvrir une vraie voie d'adoption. | évoquée | discussion squelette, 9 sept. |

## Les chantiers du squelette

| N° | Chantier | État | Où en est-on | Fiche |
|---|---|---|---|---|
| P1 | Un seul squelette de référence | Fait | Un seul dossier versionné, dix versions numérotées, anciennes copies archivées, sauvegardé à deux endroits. | fiche de cadrage dans le dossier |
| P2 | Mettre à niveau un projet quand le squelette évolue | Fait | Chaque projet sait quelle version il utilise et peut se mettre à niveau sans réécrire son histoire ; prouvé sur une copie d'Alpha, puis fait pour de vrai (3.6.1). | fiche de cadrage dans le dossier |
| P3 | Prouver que l'IA a lu les règles avant d'agir | Fait | L'IA doit présenter une empreinte des documents lus avant de commencer ; corrigé pour les projets qui ont déjà un historique. | fiche de cadrage dans le dossier |
| P4 | Revue contradictoire en option | Cadré | Fiche prête ; pas encore autorisée ; désactivée par défaut. | fiche de cadrage dans le dossier |
| P5 | Travailler par phases | À cadrer | Un niveau au-dessus des chantiers, avec ouverture, vérification de clôture et gel. Pas encore de fiche. | — |
| P6 | Guide de reprise dans le dossier | Fait | Fusionné avec l'étape 2 de la ROADMAP : la vue est générée par le contrôleur dans le dossier (où on en est, prochaine étape, ce qui attend le Project Owner). Livré et promu en 3.8.0 (8 sept.). | fiche de cadrage dans le dossier |
| P7 | Critères d'entrée d'un chantier | À cadrer | Pas encore de fiche. | — |
| P8 | Petits points | Partiel | Garde-fou Git : fait (3.2.0). Restent : profil d'adoption vérifié, exercice réel de restauration. | — |
| P9 | Un seul état de suivi | Fait | Les fiches de suivi ne vivent que sur la branche principale ; le contrôleur les enregistre lui-même (3.2.0). | fiche de cadrage dans le dossier |
| P10 | Publication — étape 1 : la vitrine GitHub | En cours | Étape 1 promue en 3.9.0 (8 sept.) : README problème → solution → démo → fonctionnement, en anglais puis en français ; exemple hello-squelette rejouable dont la sortie réelle alimente le README et est vérifiée par un test ; CONTRIBUTING ; licence MIT. Reste à faire par le Project Owner : envoi sur GitHub et le NAS, release GitHub, About et Topics. Étape 2 (dépôt public, annonce) après un second vrai projet. | fiche de cadrage dans le dossier |
| P11 | Style de retour au choix | Fait | Livré et promu le 7 sept. (3.7.0, 94 tests) après deux confirmations ; sauvegardé sur GitHub et le NAS. Alpha suivra en dernier, en une fois. | fiche de cadrage dans le dossier |
| P12 | ROADMAP — discussion dédiée et tableau de bord | En cours | Étape 1 faite : page publiée, mise à jour quotidienne, consignes proposées. Étape 2 promue en 3.8.0 (8 sept.) : idées, réglages et vue générés depuis les fichiers du projet, fiches de cadrage dans le dossier. Reste : la page Claude en miroir de la vue générée, les consignes mises à jour. | fiche de cadrage dans le dossier |
| P13 | Revue de robustesse indépendante et correctifs | Fait | Revue du tag 3.9.0 confiée à Codex (lecture seule, sur une copie) : 18 constats, 2 graves, verdict « corrections majeures demandées ». Les deux graves ont été corrigés en 3.9.1 ; les quinze restants, contre-vérifiés un par un le 9 sept. (tous confirmés, aucun rejeté), l'ont été en trois lots : A — les autorisations (3.10.0), B — ce que le squelette affirme (3.11.0), C — la robustesse d'exécution (3.12.0). Les dix-huit constats sont traités. Une seconde revue, sur le tag 3.13.0 et sous des angles neufs (adoption, première lecture, cohérence doctrine ↔ mécanique, langue), a rendu sept constats — tous confirmés par contre-vérification, plus un huitième trouvé en la faisant : le garde-fou jugeait le dossier de travail et non ce qui allait être enregistré. La 3.14.0 les corrige. | fiche de cadrage dans le dossier |
| P14 | Langue au choix : anglais et français | Partiel | Étape 1 livrée en 3.13.0 : le Project Owner choisit la langue à l'initialisation, comme le style de retour, et le contrôleur s'y tient pour tout ce qui lui est adressé — status et vue roadmap. Les noms de vérifications et les messages de refus restent en anglais : ce sont des identifiants. Étape 2, plus tard : les documents de gouvernance en anglais. Commits, tags et journal restent en français. | fiche de cadrage dans le dossier |
| P15 | Amorçage outillé | Fait | Clos par le Project Owner le 10 sept. sans avoir été ouvert : « on a déjà clôturé l'affaire, c'est allé très vite en réalité ». La fiche lisait les six minutes d'initialisation du second projet réel comme une douleur d'adoption ; ce sont du temps machine et du travail de l'agent, pas le sien — il avait qualifié l'essai de totalement réussi. Ce qui manquait vraiment avait déjà été livré en 3.15.0 : modèles copiables, refus qui nomment le format attendu, mandat écrit dans FIRST_START, porte d'entrée d'un projet neuf dans ADOPTION. La commande d'amorçage n'est pas nécessaire. | fiche de cadrage dans le dossier |
| P16 | Le garde-fou de commit | Fait | Trois façons démontrées de faire entrer dans l'historique un commit que l'audit aurait refusé, trouvées par la seconde passe de contrôle indépendant. Lots A et B livrés en 3.16.1 : le garde-fou est installé là où Git le cherche vraiment, et un état indexé illisible est refusé au lieu d'être accepté sur le seul audit du disque. Lot C livré en 3.16.2 : la vérification des fusions lit l'index, ce que le commit emporte, et non le dossier de travail, d'où un fichier hors périmètre pouvait disparaître. Les cinq constats de la seconde passe sont traités ; reste une troisième passe de contrôle. | fiche de cadrage dans le dossier |
| P17 | L'histoire figée qui peut être défigée | Fait | La troisième passe de contrôle a montré qu'un chantier autorisé sur l'état du projet pouvait retirer la baseline d'adoption, modifier une clôture figée, puis redéclarer la baseline sur le commit réécrit en citant la vieille décision — par la voie normale. Quatre questions tranchées par le Project Owner. Livré en 3.18.0 : une décision qui déclare une baseline nomme son commit ; retirer une baseline exige une décision qui le dit ; une baseline ne recule jamais ; et toute montée de version est répétée sur un worktree jetable avec l'audit du nouveau contrôleur avant d'être écrite. Alpha a confirmé ses deux baselines et adopté la 3.18.0 le jour même. La quatrième passe de contrôle a trouvé la porte restée ouverte — le résultat d'une fusion édité avant son commit — et trois anomalies modérées ; la 3.18.1 les ferme toutes. | fiche de cadrage dans le dossier |
| P18 | Publication : le squelette sait se publier | Partiel | Le dépôt public sera un miroir produit par un script depuis le dépôt privé, jamais édité à la main : l'arbre suivi à un tag, l'adresse retirée, les chemins de la machine neutralisés, le projet adopté renommé « Alpha », le dépôt de sauvegarde anonymisé, le prénom conservé, les rapports de contrôle gardés et marqués comme copies. Le script refuse de finir s'il reste un mot interdit et ne touche jamais au core. Livré en 3.19.0 : le script, son essai, la fiche. Reste : la publication elle-même (dépôt public à nommer, première version publique en 4.0.0 après la cinquième passe), le rendu public comme geste du Project Owner. | fiche de cadrage dans le dossier |

## Ce qui est derrière nous

- **5 sept. — Revue indépendante du squelette ; V3 mise sous version** (3.0.0)
  - Trois copies du squelette existaient ; la plus avancée n'était même pas versionnée. Revue en lecture seule : 8,5 sur 10 comme moteur de gouvernance, huit axes d'amélioration (P1 à P8).
  - La copie V3 est mise sous Git, avec sa provenance corrigée : c'est le point de départ, version 3.0.0.
  - _Sources : revue du 5 sept., fiche P1, journal du squelette_
- **6 sept. — Codex améliore V3 ; contre-vérification ; corrections ; trois décisions** (3.1.0)
  - Codex ajoute la commande qui résume la situation, des preuves de fin de chantier vérifiables, et la reprise des chantiers mis en pause.
  - La contre-revue trouve une impasse (la reprise refusée dès qu'un chantier avait avancé) ; corrigée, avec quatre autres points.
  - Décisions du Project Owner : la doctrine « une autorisation donnée couvre les étapes ordinaires » est ratifiée ; promotion ; un seul squelette de référence, les deux anciennes copies archivées.
  - _Sources : compte rendu de la contre-revue, journal du squelette (TPL-D-001 à 003)_
- **6 sept. — Garde-fous Git ; fiches de suivi centralisées ; sauvegarde GitHub** (3.2.0)
  - Un garde-fou vérifie chaque enregistrement avant de l'accepter et protège la branche principale.
  - Les fiches de suivi ne vivent plus que sur la branche principale, et le contrôleur les enregistre lui-même (chantier P9).
  - GitHub devient la sauvegarde de référence ; c'est toujours le Project Owner qui envoie.
  - _Sources : fiche P9, journal du squelette (TPL-D-004 à 006)_
- **6 sept. — Reprendre un projet existant sans réécrire son histoire** (3.3.0)
  - Alpha lu sans rien y toucher : le squelette accepte l'historique d'un projet tel quel (59 chantiers reconnus, 0 erreur) et n'est strict que pour la suite.
  - Le README gagne son paragraphe en anglais.
  - _Sources : fiche P2, journal du squelette (TPL-D-007, 008)_
- **6 sept. — Le squelette sait quelle version un projet utilise, et le met à niveau** (3.4.0)
  - Liste officielle des dix-neuf fichiers du modèle (décision du Project Owner) ; commande de mise à niveau ; les règles du modèle séparées de celles du projet.
  - Plan de mise à niveau calculé pour Alpha, sans rien y écrire.
  - _Sources : fiche P2, journal du squelette (TPL-D-009)_
- **7 sept. — Tests rendus indépendants du projet ; répétition sur une copie d'Alpha** (3.4.1)
  - La répétition sur une copie jetable révèle que les tests du modèle dépendaient du contenu du projet ; corrigé ; tout est vert sur la copie.
  - _Sources : fiche P2, journal du squelette (TPL-D-010)_
- **7 sept. — Dérive : la mise à niveau lancée dans le vrai Alpha ; retour arrière ; règle des deux confirmations** (3.5.0)
  - La question « sur l'original ou sur une copie ? » n'avait jamais été posée. Le mandat est retiré, le Project Owner remet Alpha dans son état d'avant, vérifié en lecture seule.
  - Règle du Project Owner : si une consigne fait sortir du dossier accordé, deux arrêts et deux confirmations qui nomment le dossier. Le squelette la fait respecter mécaniquement.
  - Répétition sur une copie d'Alpha, après deux confirmations : tout est vert ; trois petites corrections notées pour le jour où on le fera pour de vrai.
  - _Sources : fiche P2 (§ 13 à 15), journal du squelette (TPL-D-011, 012)_
- **7 sept. — Preuve que l'IA a lu les règles avant d'agir** (3.6.0)
  - Deux choix du Project Owner : l'IA présente elle-même l'empreinte des documents lus (le contrôleur ne la lui souffle jamais) ; seuls les documents de référence comptent.
  - Sans cette empreinte, impossible de démarrer un chantier ; si un document change en cours de route, il faut le relire avant de clore.
  - _Sources : fiche P3, journal du squelette (TPL-D-013, 014)_
- **7 sept. — Impasse pour les projets qui ont déjà un historique ; correctif** (3.6.1)
  - Sur une copie d'Alpha, la 3.6.0 bloquait tout : elle exigeait la preuve de lecture même pour des chantiers clos avant qu'elle existe. Correctif : une date de départ pour la preuve de lecture, déclarée par le Project Owner lors de la mise à niveau.
  - Livré après deux confirmations et le feu vert sur les fichiers temporaires de Git ; « promouvoir ».
  - Alpha passe au squelette 3.6.1, dans l'original, après deux confirmations : mise à niveau réelle réussie, toutes vérifications au vert ; sauvegarde sur le NAS à envoyer par le Project Owner (non vérifié par ce tableau).
  - _Sources : fiches P2 (§ 16 à 18) et P3 (§ 8), journal du squelette (TPL-D-015)_
- **7 sept. — Le style de retour au choix, et la précision sur les confirmations** (3.7.0)
  - Chaque projet retient désormais le choix du Project Owner (technique ou simple) ; la question est posée à la création d'un projet ; la vue de situation le rappelle en première ligne ; l'IA doit s'y tenir. La règle des deux confirmations se note aussi quand le travail a lieu dans le dossier du projet lui-même.
  - Version d'essai préparée hors du dossier, vérifiée sur une copie d'Alpha, puis livrée après deux confirmations ; décision « simple et promouvoir » ; promue le 7 sept. à 23:34 ; sauvegardée sur GitHub et le NAS le soir même.
  - _Sources : fiche P11, journal du squelette (TPL-D-016)_
- **7 sept. — Deux idées cadrées : le style de retour (P11), la ROADMAP dédiée (P12) ; première page ROADMAP**
  - Style de retour : fiche prête ; décisions prises le soir même ; livrée et promue dans la foulée (3.7.0).
  - ROADMAP : fiche prête ; page publiée en trois versions le soir même (technique, puis simple avec le bloc des idées, puis à jour de la 3.7.0) ; mise à jour quotidienne réglée ; premier passage automatique à 23:47, sans accès au dossier.
  - Le 8 sept. : « toutes les infos dans le dossier physique, format JSON ? » → étape 2 cadrée et validée ; la ligne « pas obligé d'avoir un dépôt » retirée à la demande du Project Owner.
  - _Sources : fiches P11 et P12_
- **8 sept. — La ROADMAP dans le dossier : idées, réglages, vue générée, fiches rapatriées** (3.8.0)
  - Les idées du Project Owner vivent en deux formes synchronisées dans le dossier (commande idea) ; les réglages de la vue dans un fichier ; la vue elle-même est générée par le contrôleur (roadmap-view), en page et en Markdown, dans une forme stable, chaque ligne avec sa source ; la situation dit si elle est à jour.
  - Le squelette a sa propre roadmap sous provenance/ et les fiches de cadrage (revues, scopes, mandats) sont rangées dans le dossier ; la page Claude devient un miroir.
  - Version d'essai préparée hors du dossier, vérifiée (suite de tests complète), livrée sur une branche après deux confirmations (trois commits, 97 tests au vert sur le poste), promue le 8 sept. sur « promouvoir » (TPL-D-018, tag v3.8.0), puis envoyée par le Project Owner sur GitHub et le NAS le soir même.
  - Idée nouvelle notée le même jour : un challenge du squelette par Codex quand il sera terminé, avant la mise à niveau finale d'Alpha.
  - _Sources : fiche P12 § 12 et § 13, journal du squelette (TPL-D-017)_
- **8 sept. — La vitrine GitHub : le problème avant le mécanisme, une démo qui ne peut pas mentir** (3.9.0)
  - Sur les remarques de GPT (8 sept.), le premier écran du README est refait : le problème (les projets menés avec des IA dérivent), la solution (un contrôleur qui refuse), un tableau sans / avec, une démo, comment essayer — en anglais puis en français, la documentation existante inchangée ensuite.
  - L'exemple hello-squelette rejoue en quelques secondes un changement gouverné complet dans une copie temporaire ; sa sortie réelle alimente le README et un test échoue si le README s'en écarte.
  - Guide de contribution court et bilingue ; licence MIT. Version d'essai préparée hors du dossier sur la 3.8.0, 98 tests OK, livrée sur branche après deux confirmations (deux commits), puis promue le 8 sept. après intégration d'un commit de provenance arrivé sur main entre-temps.
  - _Sources : fiche P10 (provenance/maintenance/scopes), journal du squelette (TPL-D-019)_
- **8 sept. — Une revue extérieure trouve deux passages ouverts, la 3.9.1 les ferme** (3.9.1)
  - Le squelette a été soumis à une revue indépendante, en lecture seule, sur une copie de la version publiée : dix-huit constats, dont deux graves.
  - Le premier : en déplaçant un fichier, un agent pouvait le retirer d'un endroit qu'il n'avait pas le droit de toucher, sans que rien ne le signale. Le second : le garde-fou de commit ne surveillait que le code métier, si bien qu'un fichier refusé par la vérification pouvait quand même être enregistré.
  - En les vérifiant, une troisième faille est apparue : le garde-fou pouvait être déplacé, donc désactivé, par le même moyen. La 3.9.1 ferme les deux premières, rend la troisième impossible à faire passer inaperçue, et le dit franchement dans la doctrine.
  - Trois nouveaux essais automatiques, vérifiés rouges avant correction et verts après, empêchent le retour des trois cas.
  - Version promue le soir même ; le dossier où l'application dépose les fichiers téléchargés est désormais ignoré par le dépôt, sans rien supprimer.
  - _Sources : rapport de revue et son mandat (provenance/maintenance/), journal du squelette (TPL-D-021)_
- **9 sept. — Les quinze constats restants sont tous confirmés ; le premier lot ferme la brèche du garde-fou** (3.10.0)
  - Les quinze constats que la 3.9.1 n'avait pas traités ont été repris un par un, sans faire confiance au rapport : huit rejoués sur une copie neuve, sept établis en lisant le code. Tous confirmés, aucun rejeté à tort.
  - Les correctifs sont découpés en trois lots, du plus proche de l'autorisation au plus lointain. Ce premier lot traite qui a le droit d'écrire quoi : une décision qui enregistre un refus n'autorise plus rien ; un champ laissé vide ne va plus chercher sa valeur à la ligne suivante ; un lien symbolique enregistré puis effacé de l'arbre reste refusé ; autoriser un dossier oblige désormais à lire les autorités de ses sous-dossiers.
  - La brèche assumée en 3.9.1 est fermée : le garde-fou exécutable est maintenant installé hors de l'arbre de travail, le fichier versionné n'en est plus que la référence, et le contrôleur vérifie que les deux sont identiques. Déplacer ou supprimer le fichier versionné ne désarme plus rien.
  - Ce qui reste possible, et qui est écrit noir sur blanc : effacer soi-même la copie installée, au terminal, hors du cadre. Le contrôle suivant le voit et le dit.
  - Cinq nouveaux essais automatiques, chacun vérifié rouge avant correction et vert après.
  - _Sources : contre-revue des quinze constats, journal du squelette (TPL-D-023)_
- **9 sept. — Le squelette cesse d'affirmer plus qu'il ne vérifie** (3.11.0)
  - Le tableau de bord annonçait « toutes réussies » pour les essais automatiques alors qu'il n'en avait lancé aucun : il lisait le résultat de l'audit et en tirait une conclusion qui ne lui appartenait pas. La démonstration a été faite sur une copie : un essai volontairement cassé, tout committé proprement, et le tableau affichant « toutes réussies · 107 tests ».
  - Désormais il dit ce qu'il a vraiment contrôlé, et compte les essais présents sans se prononcer sur leur issue. Lancer la suite reste un geste séparé.
  - Il se déclarait aussi à jour tout en affichant une version dépassée : poser un nouveau tag changeait ce qu'il montrait sans qu'il s'en aperçoive. Les tags entrent maintenant dans son calcul de fraîcheur.
  - Le contrôle qui garantit que le README ne ment pas se laissait désactiver en retirant deux commentaires. Leur absence est maintenant une erreur.
  - Et la vitrine promettait qu'un agent qui n'a pas lu ne peut pas démarrer. C'est faux, et c'est écrit franchement : ce que la preuve établit, c'est que le travail est parti du texte courant des règles, et qu'y toucher invalide la preuve. Aucune mécanique ne prouve qu'un esprit a lu.
  - Cinq nouveaux essais automatiques, chacun vérifié rouge avant correction et vert après.
  - _Sources : contre-revue des quinze constats, journal du squelette (TPL-D-025)_
- **9 sept. — Le dernier lot : ce qui tient quand quelque chose se passe mal** (3.12.0)
  - Un Ctrl-C au mauvais moment laissait un travail à moitié fait : les fiches enregistrées, une branche créée, et rien pour revenir en arrière. Le filet ne rattrapait que les pannes ordinaires, pas l'interruption au clavier. Démontré sur une copie, puis corrigé : tout revient à l'état d'avant.
  - Une mise à niveau pouvait écraser un fichier du projet, sans un mot, quand la nouvelle version du modèle revendiquait le même emplacement. Démontré aussi : le fichier remplacé, la commande annonçant un succès. Elle refuse maintenant, et demande une décision explicite.
  - Un merge d'intégration était refusé alors que la règle promet qu'il passe. Il passe désormais — et au passage, un fichier glissé en douce dans un commit de merge est refusé en étant nommé, ce que rien ne vérifiait avant.
  - Le gel d'un historique adopté protégeait par le nom : réécrire une vieille fiche lui faisait emporter sa dispense vers du travail fait aujourd'hui. Il protège maintenant par le contenu.
  - Et le tableau de bord ne réécrit plus sa page avant de refuser en annonçant qu'il n'a rien écrit.
  - En prime : après une montée de version, le garde-fou se réinstalle tout seul — un projet n'est plus à une commande oubliée d'un enregistrement non gardé.
  - Cinq nouveaux essais automatiques, chacun vérifié rouge avant correction et vert après. Les dix-huit constats de la revue extérieure sont désormais tous traités.
  - _Sources : contre-revue des quinze constats, journal du squelette (TPL-D-027)_
- **9 sept. — Le squelette parle la langue qu'on lui demande** (3.13.0)
  - En mesurant le terrain avant de commencer, une surprise : le squelette était déjà bilingue par accident. Tout ce qui parle à une machine — les refus, les noms de vérifications — était déjà en anglais ; le français ne vivait que dans les deux endroits qui s'adressent à toi, la commande status et le tableau de bord.
  - Le choix se fait maintenant à l'initialisation, comme le style de retour, et il est enregistré dans le projet. Tant que la question n'a pas été posée, rien n'est supposé : la clôture de l'initialisation est refusée.
  - Ce qui ne change pas de langue, et c'est voulu : les noms de vérifications et les messages de refus. Ce sont des identifiants, pas du texte — les traduire casserait les essais, le garde-fou et tout outil qui lit la sortie.
  - Et le tableau ne traduit jamais tes mots : tes idées, tes résumés, tes sources restent tels que tu les as écrits.
  - Effet de bord : la démo choisit l'anglais, donc le bloc de sortie du README — le dernier français de la vitrine — est désormais entièrement en anglais.
  - Trois nouveaux essais automatiques, chacun vérifié rouge avant correction et vert après.
  - _Sources : fiche P14, journal du squelette (TPL-D-029)_
- **9 sept. — Une seconde revue extérieure, et un garde-fou qui ne regardait pas au bon endroit** (3.14.0)
  - Une seconde revue indépendante a été menée sur des angles jamais explorés : peut-on adopter le squelette sur un vrai projet mal tenu, quelqu'un qui découvre comprend-il quoi faire, chaque promesse écrite est-elle tenue par du code, et la langue au choix tient-elle sa frontière. Sept constats, tous confirmés par contre-vérification, aucun rejeté.
  - En vérifiant le premier, un huitième est apparu, plus grave que tous les autres : le garde-fou de commit annonçait avoir vérifié ce qui allait être enregistré, alors qu'il regardait les fichiers du dossier. On pouvait donc préparer un enregistrement falsifié, remettre le fichier sain dans le dossier, et le garde-fou laissait passer. Un chantier fantôme, marqué terminé, entrait dans l'historique avec son accord.
  - Il vérifie maintenant les deux : ce qui va être enregistré, et l'état du dossier. Les deux sont nécessaires — l'un voit le contenu, l'autre voit les changements en attente — et le message dit lequel a été contrôlé.
  - Deuxième défaut sérieux : n'importe quel vieux commit du dépôt valait preuve de développement. Le commit initial, antérieur de tout l'historique, clôturait un chantier. Il faut désormais un commit postérieur au démarrage du chantier et qui touche son périmètre.
  - Troisième : un .gitignore un peu large faisait échouer la création d'un chantier en laissant l'enregistrement à moitié fait. Les fiches du contrôleur sont maintenant enregistrées quoi que le projet ignore.
  - Quatre des sept constats étaient des défauts introduits le jour même par les deux versions précédentes. Ils sont corrigés avec le reste, et le journal le dit.
  - Cinq nouveaux essais automatiques, chacun vérifié rouge avant correction et vert après.
  - _Sources : seconde revue indépendante et sa contre-revue, journal du squelette (TPL-D-031)_

## Pour les techniciens

- généré le 2026-09-11T13:59:40Z · style PLAIN · rôle PROJECT_TEMPLATE
- branch `main` · HEAD `40a13677a363b80aff4640fd62f4288d76be9998` · tag `none`
- audit PASS · skeleton 3.19.1 · core aligné · hook INSTALLED
- remotes: `origin` `bd9ded19092fc4f9fe4bb3455677ef0380db3faf` · `nas` `bd9ded19092fc4f9fe4bb3455677ef0380db3faf`
- fiches de cadrage: P1 `provenance/maintenance/scopes/p1-consolidation-baseline-unique.md` · P2 `provenance/maintenance/scopes/p2-scope-template-upgrade.md` · P3 `provenance/maintenance/scopes/p3-scope-preuve-lecture-autorites.md` · P4 `provenance/maintenance/scopes/p4-scope-capability-adversarial-review.md` · P6 `provenance/maintenance/scopes/p12-scope-roadmap-dediee.md` · P9 `provenance/maintenance/scopes/p9-scope-records-administratifs-et-branches.md` · P10 `provenance/maintenance/scopes/p10-scope-publication-vitrine-github.md` · P11 `provenance/maintenance/scopes/p11-scope-style-de-retour.md` · P12 `provenance/maintenance/scopes/p12-scope-roadmap-dediee.md` · P13 `provenance/maintenance/scopes/mandat-codex-revue-robustesse-squelette-3.9.0.md` · P14 `provenance/maintenance/scopes/p14-scope-langue-au-choix.md` · P15 `provenance/maintenance/scopes/p15-scope-amorcage-outille.md` · P16 `provenance/maintenance/scopes/p16-scope-garde-fou-de-commit.md` · P17 `provenance/maintenance/scopes/p17-scope-baseline-defigeable.md` · P18 `provenance/maintenance/scopes/p18-scope-publication.md`
- sources_digest `b7987e8418c5a66f32eef194830834a2c6ba8b594a0b2a769ec2fec1f7136b89`
- `provenance/CHANGELOG.md` sha256=`5da544d0f176572fc472b0e89513f78d7258f381e3dd303e4fd2d430713723c8`
- `provenance/core-manifest.v1.json` sha256=`0452ae375694efdc483bb9eb74c264f29609da34d55a798f97daf6065d23a202`
- `provenance/roadmap-template.v1.json` sha256=`3a0919af1edb50d1a74c37f1a09376ea468f075e89bfe805e2de0abf3fff4e7c`
- `provenance/roadmap-view.v1.json` sha256=`e882d6fd32842655e80204edbbf0a4721a60e1cd31b5b1abb5cda00b25f2a0ea`
- `(versions taguées du dépôt)` sha256=`8b3662ae071f66d7b1b0f2efe5613df481789bbbadbdb9e1de7a12c768144a2f`
