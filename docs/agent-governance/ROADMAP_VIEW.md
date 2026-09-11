# Vue ROADMAP — consigne des agents

Ce document est core (manifeste du squelette). Il fixe la conduite d’un agent dans la discussion dédiée « ROADMAP <NOM DU PROJET> » et la manière dont la vue d’avancement est produite. La vue **montre, elle ne décide rien**.

## Ce que la vue est

- Une page (`roadmap-view --write` → `reports/roadmap/ROADMAP.html`) et une vue Markdown committée (`docs/governance/ROADMAP_VIEW.md`), **générées par le contrôleur** à partir des fichiers du projet : roadmap et records de Work Items, décisions humaines, idées du Project Owner (`docs/governance/IDEAS.md` + `ideas-state.v1.json`), état du projet, manifeste du core, réglages de la vue (`project_control/roadmap-view.v1.json`). Dans le squelette lui-même, les sources sont `provenance/roadmap-template.v1.json` et `provenance/roadmap-view.v1.json`, et les sorties vont sous `provenance/`.
- Une forme **stable** d’une génération à l’autre : bandeau de vérification ; chiffres clés ; versions dans l’ordre ; « Maintenant » et « Ce qui t’attend » (actions du Project Owner) ; « Prochaines étapes » et « Plus loin » (titres seulement) ; « Tes idées, et ce qu’elles sont devenues » ; les chantiers ; « Ce qui est derrière nous » (replié) avec un repli « Pour les techniciens » ; règles et réglages.
- Le **style suit `reporting_style`** (Project State). `PLAIN` : la vue **n’ajoute d’elle-même** aucun identifiant technique (commit, empreinte, chemin, commande) hors du repli technique, qui les porte tous ; le texte cité des fichiers du projet est montré **tel que le Project Owner l’a écrit** — la vue montre, elle ne réécrit pas ses mots. Sources nommées simplement. `TECHNICAL` : identifiants et empreintes dans la lecture. `--style` force ponctuellement l’autre forme sans rien changer au projet.
- Chaque ligne cite sa source ; ce qui n’a pas de source est marqué inconnu ou non vérifié. Rien n’est inventé, rien n’est complété.
- Idempotence : le bandeau porte `sources_digest` — empreinte des fichiers sources **et des versions taguées du dépôt**, puisque la vue nomme la version promue d’après les tags et non d’après un fichier. Le commit courant et les sauvegardes distantes en sont volontairement exclus : les y mettre rendrait la vue périmée à l’instant même où on la committe, sans fin. `status` affiche « Vue roadmap : à jour | périmée | absente » ; une vue périmée n’est jamais une erreur d’audit, seulement une régénération à faire.

## Les idées du Project Owner

Une idée est une phrase du Project Owner, **citée dans ses mots**, datée, avec sa source et un état fermé : `EVOKED`, `TO_CLARIFY`, `TO_SET`, `SCOPED`, `PLANNED`, `IN_PROGRESS`, `REALIZED`, `APPLIED`, `INTEGRATED`, `LATER`, `DISCARDED`. Une idée ne quitte la liste que par `REALIZED` ou `DISCARDED` (la cible nomme alors la décision qui l’écarte) — jamais par oubli.

- L’agent qui entend une idée l’enregistre **dans la session même** : `idea add --quote "<mots du Project Owner>" --source "<discussion, date>"`, puis `idea set ID-NNN --state … --target …` quand elle évolue. Enregistrer une idée n’autorise rien : l’autorisation reste une décision humaine et un Work Item.
- En `NORMAL_MODE`, `idea` s’exécute depuis la branche canonique, worktree propre, et committe lui-même les deux formes (`chore(project-control): idea ID-NNN <état>`). En `BOOTSTRAP_MODE`, il écrit sans committer : les records de l’initialisation sont committés avec elle.
- L’audit (`IDEAS`) vérifie la synchronisation Markdown / JSON, l’unicité des identifiants, les états admis et l’existence des cibles (`WI-NNN` dans la roadmap, `HD-NNN` enregistrée).

## Dans la discussion « ROADMAP <PROJET> »

1. **Tout message = une régénération.** Lire la mémoire de la vue si elle existe, relire les sources **à chaque fois** (un autre agent a pu livrer entre-temps), `roadmap-view --write`, puis répondre en une ligne : « Régénéré le … — N changements : … » ou « Rien n’a changé depuis le … ». Un miroir hébergé (page publiée par l’outil de l’agent) est republié **à la même adresse**, jamais recréé ; son adresse figure dans `mirrors` des réglages.
2. **Deux exceptions.** Une phrase qui commence par `RÉGLAGE :` change un réglage de la vue (`regeneration`, `style`, `zoom`, `mirrors`) dans `roadmap-view.v1.json`. La **langue** n'en fait pas partie : elle vit dans Project State (`language`), avec le style de retour, et en changer est une décision humaine, pas un réglage d'affichage, datée, puis régénère. Une phrase qui commence par `STOP ROADMAP` met fin à la convention pour la suite de la discussion.
3. **Tout le reste est renvoyé** vers une autre discussion, en une phrase, sans exécution ni débat : question, tâche, décision, écriture.
4. **Interdit depuis cette discussion** : écrire dans un dépôt (fichier, branche, commit, tag, push) au-delà des sorties de `roadmap-view --write` et du réglage de la vue, toute commande Git modifiante, tout script qui écrit, toute décision de projet (`HD-NNN`, `TPL-D-NNN`), création ou modification de Work Item, changement d’autorité, de version ou de gouvernance, rédaction de mandat, demande de permission d’écriture ou de suppression. Le double arrêt n’a jamais lieu d’ici : rien n’en sort.
5. **Dossier inaccessible** (par exemple une tâche automatique sans accès) : régénérer quand même à partir du dernier état connu, en marquant « non vérifié depuis <date> » les lignes issues du dossier ; ne jamais supposer une valeur.

## Ce que la vue n’affirme pas

La vue rapporte ce que le **contrôleur** a vérifié : ses propres contrôles (`audit`, `bootstrap-audit`). Elle **n’exécute jamais la suite de tests** et ne dit donc jamais que les essais ont réussi. Elle peut compter les essais présents dans le dossier — c’est un dénombrement, pas un résultat — et elle l’écrit ainsi : « N essais automatiques présents, non exécutés par cette vue ». Lancer la suite est un geste séparé, dont le résultat se consigne dans un rapport de maintenance ou un message de commit, jamais déduit d’un audit.

## Limites

La convention « tout message est ignoré » est tenue par cette consigne, pas par une serrure : un agent la tient sans exception. La vue vaut ce que valent ses sources : une fiche en retard s’y voit comme un écart signalé, pas corrigé. Le contrôleur garantit la forme, les sources et la cohérence ; il ne peut pas entendre une idée à la place de l’agent.
