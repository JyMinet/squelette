> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Rapport de construction — chantier P21 « Tableau des clés » — 3.21.0

Date : 2026-09-28, 18:55–20:45 (Europe/Zurich). Auteur : Claude. Mandat : `TPL-D-080` — « Construire » (18:27), double arrêt du dossier de chantier (STOP 1 « Je suis ok », 18:32 ; STOP 2, 18:33). Références : `FICHE-CADRAGE-TABLEAU-DES-CLES-V3.md` (dossier de relecture) ; `RAPPORT-MESURE-P21.md` (phase 0, à côté de ce rapport).

## Résumé en trois points

1. **Ce qui s'est passé.** La 3.21.0 est construite. L'atelier tient désormais le registre de ses copies : chacune a un ticket, un sort, une date de retour et une fiche de sortie ; rendre se prouve ; et l'effacement passe par un script que tu lances, qui vérifie chaque dossier juste avant de l'effacer. Avant de la montrer à la seconde IA, je l'ai fait attaquer par un agent séparé, qui n'avait pas vu la construction. Il a trouvé dix trous ; la plupart menaient au même accident : le script aurait effacé du travail qui n'était pas revenu, ou un autre dossier que celui qu'il avait contrôlé. Les dix sont fermés, plus deux trouvés en les fermant ; chacun a son essai, rouge sur le code d'avant et vert après. Les 211 essais passent, dans ma copie de travail et sur ton Mac (dans l'espace de travail de Claude).
2. **Ce que ça change.** Rien encore pour l'atelier : tout est sur la branche `claude/p21-tableau-des-cles` du dossier de chantier, et l'atelier n'a été que lu. Essai grandeur nature, en lecture seule : l'inventaire du dossier de chantier lui-même ne bute sur rien et liste exactement ce qu'il faudra rendre ou abandonner (section F). Un accroc de ma part : une commande de vérification a laissé un fichier verrou vide dans le dossier de chantier (section F) ; il ne gêne rien de la suite et partira avec le dossier.
3. **Ce qu'il doit faire.** Donner à la seconde IA le mandat `MANDAT-RELECTURE-CODE-P21.md` (à côté de ce rapport ; le texte à coller est à sa fin). Viendront ensuite, chacun sur ta décision : la livraison dans l'atelier (double arrêt), la promotion, puis le retour et l'effacement du dossier de relecture et du dossier de chantier.

Verdict : `P21_BUILD_DONE_READY_FOR_CODE_REVIEW`

## A — Ce qui est construit

| Pièce | Ce qu'elle fait |
|---|---|
| Registre | `provenance/copies-state.v1.json` (template), `project_control/copies-state.v1.json` (projet) ; absent = vide ; schéma `copies-state.v1` ; hors de l'export public et de la copie d'essai. |
| `copy open` | Enregistre la copie **avant** qu'elle existe, depuis la canonique (`main` pour le template), et imprime la fiche de sortie à jeton. Refuse : l'original, dedans ou autour ; un chevauchement avec une autre copie ; un chemin par un lien ou sur un volume absent ; un chemin écrit de deux façons ; un nom hors de la règle `<dépôt>-<usage>-<référence>[-rang]` ; un ticket invalide ou dont le `Folder scope` ne couvre pas le dossier ; une cible déjà close. |
| `copy return` | Inventaire complet de la copie, sans l'écrire ; chaque élément est dans l'original (commit sur une branche ou un tag ; fichier committé à l'octet) ou abandonné par son nom ; une revue revient avec son mandat ; empreinte du contenu et commit de l'original enregistrés ; transaction groupée pour réparer des copies en faute. |
| `copy check` | Lecture seule. Dans l'ordre : l'original qui juge, l'état et le lien au script, le contenu, ce que l'original garde encore, puis la place — chemin et fiche de sortie — en dernier. |
| `copy cleanup` | Écrit le script (hors du dépôt) que tu lances ; n'efface rien lui-même. |
| `copy move`, `copy close` | Déplacement enregistré (les vieux scripts cessent de passer) ; `ERASED` seulement quand le dossier n'existe plus, `KEPT` par décision. |
| Garde-fous | Audits `COPIES_REGISTER` et `COPIES_RETURNED` ; `close WI-NNN` refuse avec une copie ouverte ; le registre du template ne se modifie que sur `main` ; `status` et la vue affichent les copies ; dans une copie, `status` commence par sa fiche de sortie. |

Écarts assumés à la fiche V3 (écrits aussi dans le CHANGELOG) : identité par jeton de fiche de sortie (A-01) ; preuves par un fichier JSON ; `copy move` n'exige pas un contenu inchangé (un déplacement n'autorise rien, `copy check` compare avant tout effacement) ; pas de message « ce dossier n'a pas de ticket » ; une décision de garde prise pendant une faute se committe sous `PROJECT_CONTROL_HOOK_OVERRIDE`.

## B — Revue indépendante du code

Un agent séparé, lancé sans le contexte de la construction, a attaqué la 3.21.0 de bout en bout sur des copies d'essai (scénarios rejoués, pas raisonnés). Chaque trou ci-dessous a été reproduit, puis fermé ; chaque essai a été vérifié **rouge sur le code d'avant** et vert après.

| # | Trou démontré | Conséquence | Fermeture | Essai |
|---|---|---|---|---|
| 1 | Fichiers modifiés cachés à Git (drapeaux d'index `assume-unchanged`, `skip-worktree` ; cache de dates réglé pour s'y fier) | un retour à preuves vides passait, le script effaçait le travail | l'inventaire parcourt le dossier et compare chaque fichier, octet par octet, à ce que `HEAD` enregistre | `test_the_inventory_walks_the_folder_and_nothing_git_hides_escapes_it` |
| 2 | Dépôt imbriqué committé comme lien (gitlink) | son contenu n'était pas inventorié | refusé ; un conflit non résolu aussi | `test_an_embedded_repository_and_an_unresolved_conflict_are_refused` |
| 3 | Commit couvert par une référence de suivi ou un reflog de l'original | il pouvait disparaître (remote retiré, ménage de Git) avant l'effacement | seules les branches et les tags couvrent ; `copy check` refait la couverture (`COPY_COVERAGE`), fichiers rendus compris, au commit enregistré au retour (`original_head`) | `test_only_the_branches_and_tags_of_the_original_keep_what_a_copy_held`, `test_a_file_proof_holds_while_the_original_keeps_the_commit_it_was_proven_on` |
| 4 | Script écrit depuis une copie, sur son registre périmé | effaçait une copie que l'original avait décidé de garder | les commandes `copy` ne tournent que dans l'original (`COPY_ORIGINAL`) ; l'audit d'une copie ne juge pas les copies | `test_copy_commands_run_in_the_original_and_nowhere_else` |
| 5 | Table de correspondance des chemins (`PROJECT_CONTROL_PATH_MAP`) | le script contrôlait un dossier et en effaçait un autre | le script tourne sans table | `test_the_erasure_script_runs_without_a_path_map_and_carries_no_name` |
| 6 | Nom enregistré contenant un saut de ligne | devenait une commande du script, avant tout contrôle | chemins, noms, identifiants et jetons validés en entier ; le script ne porte plus aucun nom venu du registre | idem |
| 7 | Point de montage, tube, dossier illisible dans la copie | l'effacement aurait traversé le montage ; le contrôle restait bloqué | refusés | `test_a_copy_holding_what_an_erasure_cannot_answer_for_is_refused` |
| 8 | Copie enregistrée par un autre original, logée dans celle-ci | partait avec elle | refusée | idem |
| 9 | `core.worktree` pointant ailleurs | la lecture regardait un autre dossier | Git est lancé avec le dépôt et le dossier de travail nommés | essai n° 1 |
| 10 | La place regardée avant le long parcours | un dossier glissé à la place pendant le parcours aurait été effacé | la place est regardée avant (pour ne jamais parcourir un autre dossier) **et après** | `test_the_check_looks_at_the_place_before_the_walk_and_again_after_it` |
| + | Lire une copie lançait la commande `core.fsmonitor` que sa configuration nomme | une copie pouvait faire exécuter une commande au contrôleur | coupé pour toute lecture d'une copie | `test_reading_a_copy_runs_no_command_its_configuration_names` |
| + | Un lien glissé plus haut dans le chemin, entre le contrôle et l'effacement | l'effacement suivait le lien (démontré : « Effacé » sur l'autre dossier) | le script se place dans le dossier parent, vérifie qu'il est physiquement celui contrôlé, et efface la copie par son nom depuis là | `test_the_script_erases_from_the_parent_folder_it_pinned` |

Non corrigé, écrit comme limite : le rôle d'un fichier rendu (`mandat`, `livrable`…) est déclaré par qui rend ; le contrôleur prouve des octets, pas un sens. Ajout mineur : les fichiers `.DS_Store` que le Finder écrit en montrant un dossier ne comptent plus (sinon, regarder une copie rendue la rendait « changée »).

## C — Essais et contrôles

| Lieu | Python | Git | Résultat |
|---|---|---|---|
| Copie de travail de la session (clone de la branche) | 3.11.15 | 2.43.0 | 211 essais, OK (756 s) |
| Ton Mac, espace de travail de Claude (machine virtuelle), clone du dossier de chantier hors du dossier monté | 3.10.12 | 2.34.1 | 211 essais, OK (161 s, par tranches) ; `audit`, `bootstrap-audit`, `core-manifest` PASS ; démo et transcript à jour ; vue à jour |

Autres contrôles sur la branche : manifeste `3.21.0`, 25 fichiers core ; export public sans erreur et sans registre ; les dix nouveaux essais relancés contre le code d'avant : tous rouges.

## D — Limites assumées

- Une copie jamais déclarée reste invisible ; le registre ne voit pas ce qui a été envoyé depuis une copie, seulement ce qui n'est pas revenu.
- Quelques instants séparent le contrôle de l'effacement ; condition écrite en tête du script : personne n'écrit dans les dossiers pendant qu'il tourne.
- Un contenu transformé à l'extraction (Git LFS, fins de ligne converties, filtres) diffère de ce que `HEAD` enregistre : il apparaît comme un élément, à rendre ou à abandonner.
- L'original reste là où ses copies ont été enregistrées : déplacé, ses effacements sont refusés.
- Les dossiers internes de Git (`objects`, `refs`, `logs`) sont lus comme Git les tient, pas fichier par fichier.

## E — Commits de la branche `claude/p21-tableau-des-cles` (base `b9fe0e7`)

| Commit | Objet |
|---|---|
| `0da7a90` | le tableau des clés (3.21.0) |
| `6993f8e` | vue régénérée |
| `1afd8ba` | le rapport de mesure ne nomme plus un autre projet |
| `ff4bc85` | la revue indépendante du code : dix trous fermés |
| `0ecb546` | vue régénérée |

Tous sous `PROJECT_CONTROL_HOOK_OVERRIDE="TPL-D-080"` (le squelette est en mode amorçage). Transfert : `transfert/p21-branche-3.bundle` (23 225 octets, SHA-256 `c56237ca878e4f62620487b8ea1d6485d959dcbcde895bb473460ebe52362cfd`), vérifié puis récupéré dans la branche.

## F — État du dossier de chantier

- `main` à `b9fe0e7` (inchangé, c'est lui qui est extrait) ; branche `claude/p21-tableau-des-cles` à `0ecb546` ; `git fsck` sans erreur.
- À la racine, hors suivi : `RAPPORT-MESURE-P21.md`, ce rapport, `MANDAT-RELECTURE-CODE-P21.md`, et `transfert/` (quatre fichiers de transfert).
- **Essai grandeur nature, en lecture seule** : l'inventaire de la 3.21.0 lancé sur le dossier de chantier lui-même, depuis l'espace de travail de ton Mac, en 0,2 s, sans aucun refus. 44 éléments : `main` et les 37 tags, que l'atelier garde déjà, et la branche, couverte dès que l'atelier l'aura ; `RAPPORT-MESURE-P21.md`, à l'octet près identique à `provenance/maintenance/2026-09-28-rapport-mesure-phase-0-p21.md` de la branche (il se rendra par une preuve de fichier) ; les quatre fichiers de `transfert/` (à abandonner). Aucune clé de configuration, aucun hook ni fichier caché de `.git` à rendre.
- **Accroc** : en vérifiant la branche, j'ai lancé un `git status` sans l'option qui l'empêche d'écrire ; Git a posé un fichier verrou vide, `.git/index.lock` (0 octet, 20:34), et n'a pas pu le retirer, l'effacement n'étant pas permis dans le dossier monté. Il ne gêne ni les transferts, ni la relecture (qui travaille sur son propre clone), ni le retour (un verrou est un fichier technique de Git). Il partira avec le dossier. Pour le retirer avant, une seule ligne à lancer toi-même — uniquement ce fichier temporaire de Git, jamais le dossier :

```bash
rm ~/Projets/squelette-chantier-p21/.git/index.lock
```

- Atelier : `main` à `b9fe0e7`, arbre propre, relu en lecture seule. Alpha : non touché depuis la mesure. Aucun envoi.

## G — Suite

1. **Relecture du code par la seconde IA** — mandat `MANDAT-RELECTURE-CODE-P21.md` ; livrable `RELECTURE_CODE_P21.md` à la racine du dossier de chantier.
2. Corrections éventuelles, dans le même dossier de chantier.
3. **Livraison dans l'atelier** — double arrêt séparé : la branche récupérée dans l'atelier, avec ce rapport, le mandat et la relecture rangés tels quels sous `provenance/maintenance/`.
4. **Promotion** — décision séparée (tag `v3.21.0`, vue).
5. **Premières clés rendues** — le dossier de relecture et le dossier de chantier (tickets manuels, annexe A de la fiche V3) : papiers rendus dans l'atelier, le reste abandonné par son nom, puis effacement par ton script.
