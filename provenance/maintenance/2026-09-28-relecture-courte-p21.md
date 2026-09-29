> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

## Résumé en trois points

1. **Ce qui s’est passé.** La V2 corrige les anciens exemples de la V1 : dossier parent refusé, fichiers non committés repérés, copie reprise refusée, fiche de sortie hors de l’export et tag après retour. Les 138 fichiers source sont inchangés. Les sondes demandées ont été rejouées uniquement dans `runs/v2/`.
2. **Ce que ça change.** Quatre constats sont fermés et trois restent partiels : l’inventaire oublie du contenu propre à `.git`, le déplacement n’est pas suffisamment lié à la cible du script de nettoyage, et la réparation après tag prématuré se bloque avec deux copies ouvertes. Le verdict reste **corrections majeures nécessaires**, sur ces points ciblés.
3. **Ce qu’il faut faire.** Compléter les trois contrats décrits en C, puis aligner les quelques mentions restées au stade « décision à prendre ». Les décisions de la section 11 sont acquises ; aucune nouvelle discussion de leurs options n’est demandée. Ce rapport n’autorise pas la construction.

# Relecture courte de la fiche « Tableau des clés » V2

Date : 2026-09-28. Mandat : `MANDAT-RELECTURE-TABLEAU-DES-CLES-V2.md`. Posture : `READ_ONLY / REPORT_ONLY`. Référence antérieure : `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V1_V2.md`. Les références de lignes ci-dessous désignent la fiche V2, sauf chemin explicitement indiqué.

## A — Preflight

**Périmètre :** `~/Projets/squelette-revue-tableau-des-cles/`, exclusivement. Au départ, `runs/v2/` et le livrable demandé étaient absents. Les pièces de ce tour, la contre-revue et les constats antérieurs pertinents ont été lus. Les décisions de §11 sont traitées comme prises. La contre-revue n’est pas utilisée comme preuve suffisante de fermeture : les scénarios ont été réévalués.

**Source :** 138 fichiers présents, 138 empreintes conformes à `SOURCE-MANIFESTE.sha256`, aucun fichier supplémentaire ou lien symbolique dans `source/`. La provenance est celle déjà établie au tour précédent : export déclaré de `v3.20.2`, commit déclaré `9b8792e1ef453869105bd0edc2cc085120bbf404`. Aucun accès à l’atelier pour revérifier ce lien. Les lectures du contrôleur sont limitées à l’exclusion de `.git`, aux hooks, à la fraîcheur de la vue et au refus des mutations après audit en échec ; aucune relecture complète ni suite générale exécutée.

Empreintes des pièces consultées ; chemins relatifs au dossier accordé :

| Pièce | Octets | SHA-256 |
|---|---:|---|
| `MANDAT-RELECTURE-TABLEAU-DES-CLES-V2.md` | 4423 | `c1456271b96094a8acc79c807742ea5c394e8dc81f05f914cab816bf330a0e7c` |
| `FICHE-CADRAGE-TABLEAU-DES-CLES-V2.md` | 23289 | `2e63588e754e9ce3ed757a61972657cd10d3af92d56a764fb57f1fb6d087df64` |
| `CONTRE-REVUE-RELECTURE-TABLEAU-DES-CLES-V2.md` | 4366 | `f2fed6d676eb6d7a9ca557ba90a30c3653ed5f53d03990d3c4b995bb285efdd7` |
| `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V1_V2.md` | 52801 | `f7eba9886549c7d58caece40db3a516e23906f7743ddcd7b8946ccbb00d388b3` |
| `SOURCE-PROVENANCE.md` | 2171 | `ac97eb57b0f6059e5d3e2913ccd39f24487e659b183e4752fe17bd2fd990f931` |
| `SOURCE-MANIFESTE.sha256` | 15648 | `a0c1ea0d49c0741e23b427d427630569b2478e8a8ed250cc8d971dbd5891f102` |
| `runs/results.json` | 21893 | `4a6309f95a712fb5280eea0bf41fe4db33b1779e2b0c9fd2910e727c10c47ce2` |
| `runs/promotion-order.json` | 3926 | `22e1c2ad3f9facda3937753c8c293639da56a3337053eb192f3bc6a208d230c8` |
| `source/scripts/project_control.py` | 394650 | `21294605fd1e396adeb12077a945ee42c9754f0ee39d45c3d458f280ca30e080` |
| `source/provenance/CHANGELOG.md` | 228044 | `a8f51401f525d2ba06785700757767c0ac49ee4c333d8a70a2821276d12f90be` |

**Preuves nouvelles :** `runs/v2/replay.py`, `results.json` et `commands.json`. Les fixtures portent « FIXTURE DE RELECTURE — FICTIF, N’AUTORISE RIEN ». Elles utilisent deux dépôts Git fictifs autonomes et sans remote, un petit export et deux dossiers servant au scénario de déplacement. Aucun effacement n’a été exécuté. La copie A a été renommée en B dans cette seule fixture, puis A recréé avec un autre contenu, conservé.

Les projections de règles V2 dans le script ne sont **pas une implémentation de `copy`**. Les résultats distinguent les faits Git/fichiers observés et les décisions que le texte V2 imposerait. Le retour multi-copies est une table de décision du texte ; le script périmé est un contre-exemple de contrat possible, pas un bug allégué dans un logiciel inexistant. Deux lectures ciblées complémentaires, en lecture seule dans ce même dossier, ont porté sur l’inventaire et le déplacement.

## B — Fermeture de R01 à R07

| Constat | État | Preuve et limite |
|---|---|---|
| **R01 — cible contenant l’original** | **FERMÉ** | §5.3 l.103 exclut l’inclusion dans les deux sens ; §5.8 l.158 la revérifie. Rejeu **P09** : ancien prédicat accepte le parent, nouveau prédicat le refuse. Les autres copies non effacées sont aussi protégées. |
| **R02 — contenu hors branches** | **PARTIEL** | **P06** : références identiques, mais modification, note non suivie et dossier ignoré visibles ; V2 exige couverture ou abandon. Ces anciens exemples sont fermés. L’inventaire énuméré ne couvre cependant pas le hook unique de **N1**, alors que §5.5 promet tout le contenu. |
| **R03 — preuve ancienne** | **PARTIEL** | **P07** : contenu/références changés malgré la même identité du dossier ; V2 doit refuser. `KEPT` doit aussi refuser. L’ancien cas est fermé. Le nouveau déplacement laisse à préciser le lien entre cible contrôlée et cible effacée : **N2**. |
| **R04 — export historique sans ticket** | **FERMÉ** | **P04** : `copie.json` est dans le contenant ; l’export du tag reste identique, sans Git et sans promesse de `status`. §5.4 l.113–118 abandonne correctement l’hypothèse du ticket présent dans l’ancien tag. |
| **R05 — ordre et réparation** | **PARTIEL** | **P11** : décision symbolique sur branche → fast-forward → retour → vue → tag, sans merge ; le tag contient `RETURNED`. Les décisions ne servent plus de cible de clôture. **P10** refuse bien un FAIL d’une autre nature, mais deux copies ouvertes rendent toute réparation individuelle impossible : **N3**. |
| **R06 — nom de l’annexe** | **FERMÉ** | §5.9 l.164 et annexe l.245 : tickets manuels jamais importés, registre initial vide. Il n’y a plus de conversion prétendument conforme à `copy open`. |
| **R07 — coût** | **FERMÉ** | §5.10 l.168–171 distingue doctrine, lecture automatique, sept arguments d’ouverture, preuves et geste humain. La promesse de coût nul a disparu. La mention de cinq commandes doit simplement intégrer la décision distincte concernant `move` : N4. |

### Vérifications transversales demandées

- **Fiche de sortie.** Le contrôleur 3.20.2 ignore les JSON dans `.git` (`source/scripts/project_control.py:2148–2150`) ; il ne reconnaît pas déjà `copie.json` comme record ou autorisation. La vérification des hooks porte sur le hook `pre-commit` installé, pas sur tout `.git/hooks/` (`3480–3508`). Le pointeur de l’export est dans son contenant, hors de la racine du contrôleur situé dans `source/`. Aucune collision actuelle démontrée. La future bannière doit être ajoutée ; son absence actuelle n’est pas une redline.
- **Empreinte et identité.** Device + inode détectent certains remplacements, pas le retravail dans le même dossier : P07 garde la même identité. La protection vient de l’empreinte **complète des octets et références**, puis de sa liaison à la bonne cible. Hacher seulement les lignes de `git status` ne suffit pas ; P06 montre notamment `! ignored/`, sans liste de ses fichiers. Il faut descendre dans ce dossier pour son empreinte, même si son abandon est nommé en bloc. N1/N2 précisent les défauts de couverture et de liaison.
- **Sous-modules et worktrees.** Leur contenu propre n’est pas inventorié récursivement par la seule commande donnée ; les métadonnées et hooks nécessitent eux aussi un traitement. Aucun sous-module ni worktree supplémentaire n’a été créé pour cette revue courte. N1 est établi par le seul hook, et demande prise en charge explicite ou refus de ces configurations ; il ne prétend pas que leurs variantes ont été rejouées.
- **`KEPT → RETURNED`.** La décision et un retour complet sont exigés (§5.1 l.91), donc nouvelle empreinte/identité et même frontière. Pas de réouverture automatique de R01/R03 constatée dans cette transition. `copy move` reste décidé ; il doit vérifier la portée du ticket pour le nouveau chemin, conserver l’identité de la même copie et invalider les anciens scripts, sans déduire une extension de mandat du seul déplacement.
- **Fenêtre de concurrence.** Elle est honnêtement déclarée en l.160. La condition doit viser **toute écriture**, humaine ou issue d’un processus, et non le seul travail d’un agent. Une sauvegarde humaine après le contrôle a le même effet qu’une écriture d’agent. Ce complément ne remet pas en cause le choix du script humain et ne promet pas de supprimer toute course avec une commande de contrôle séparée.
- **Promotion et vue.** La topologie reste compatible avec un fast-forward. Le journal fourni décrit toutefois un tag puis une vue régénérée après (`source/provenance/CHANGELOG.md:796–798`), alors que V2 place la vue avant le tag. Les tags entrent dans son empreinte (`project_control.py:2530–2546`) : P11 confirme que ces entrées changent après la régénération. La vue sera donc immédiatement périmée ; ce n’est pas un FAIL d’audit. Prévoir une actualisation après le tag, ou annoncer explicitement cette conséquence. La règle « clés rendues au tag » reste satisfaite ; l’histoire d’un tag erroné n’est pas réécrite.

## C — Constats ciblés nouveaux ou résiduels

### N1 — L’inventaire écrit laisse du contenu propre à `.git` hors preuve

**Sévérité : MAJOR. Objet :** §5.5 l.124–132 et §5.8 l.158. **Statut : OUVERT.**

**Scénario et preuve :** après avoir relevé les branches/références, HEAD, stash, statut avec ignorés et empreintes de tous les fichiers de l’arbre de travail, ajouter un hook inédit `.git/hooks/pre-push`. La sonde `N1_git_private` constate `enumerated_categories_unchanged=true`, alors que ce fichier existe seulement dans la copie. Son SHA-256 est `d6860bc827a64a4c1bb0fce44b1e57fa29bddc9313c155b1682e13d0ce15d2e1`. Il n’a pas été exécuté. Le seul fichier `.git` explicitement exclu par la fiche est pourtant `copie.json`.

**Impact :** suivre les catégories énumérées permet de déclarer un inventaire complet sans sauvegarder ni abandonner ce contenu unique. Le nouveau digest ne répare pas une omission de son inventaire.

**Correction minimale :** couvrir ou classer explicitement le contenu propre à `.git` — hooks, configuration utile, travail récupérable par reflogs, données de sous-modules/worktrees — et refuser une configuration non prise en charge. Chaque élément utile doit être rendu ou abandonné par son nom. Ne pas simplement hacher tout `.git` brut : ses fichiers techniques peuvent changer sans nouveau travail. **Fermeture :** le hook de la sonde doit être détecté et empêcher le retour sans couverture ; une catégorie non prise en charge ne doit jamais valoir vide.

### N2 — `copy check ID` ne lie pas explicitement le résultat à la cible du script

**Sévérité : MAJOR. Objet :** §5.8 l.158–159 et `copy move`, l.177/260. **Statut : OUVERT.**

**Scénario et preuve :** un script généré pour A mémorise son chemin. A est déplacé vers B, et le registre est mis à jour par le `move` décidé. A est réoccupé par un autre travail. Le vieux script appelle `copy check ID` : le registre courant désigne B, dont l’identité et le contenu rendus sont conservés ; le contrôle passe. Si l’effacement utilise encore le chemin A capturé lors de la génération, il vise le nouveau travail. La sonde `N2_moved_target` confirme ces trois faits, **sans effacer** quoi que ce soit. Aucun changement concurrent pendant le contrôle n’est nécessaire.

**Impact :** une réalisation plausible du script satisfait les vérifications du dossier courant mais efface un autre dossier. La formulation « efface ce seul dossier » exprime l’intention, sans définir le lien vérifiable entre le contrôle par ID et le chemin embarqué dans un script antérieur au déplacement. Ce n’est pas l’accusation d’un bug déjà codé.

**Correction minimale :** faire valider par `check` le chemin et l’identité attendus par le script, et refuser si l’entrée a été déplacée ; ou produire un résultat contrôlé qui désigne exactement la cible utilisée par l’effacement. Le registre relu doit être celui de la canonique. Exiger l’absence de toute écriture durant la dernière vérification et l’effacement, pas seulement l’absence d’agent. **Fermeture :** un ancien script pour A doit refuser après `move` vers B, même si B est parfaitement rendu et A existe de nouveau.

### N3 — Deux copies ouvertes bloquent la réparation annoncée

**Sévérité : MAJOR. Objet :** §5.7 l.152 et essai multi-copies de §10. **Statut : OUVERT.**

**Scénario et preuve :** A et B sont `OPEN` pour la même version ; un tag est posé trop tôt. L’audit donne deux FAIL `COPIES_RETURNED`. La règle permet `return A` seulement si tous les FAIL portent sur A : celui de B le bloque. Symétriquement, A bloque B. `P10_N3` reproduit exactement ce prédicat : réparation individuelle admise pour une entrée seule, refusée pour A comme pour B quand les deux erreurs existent ; un FAIL `HUMAN_AUTHORIZATION` est également refusé. Aucun retour groupé n’est défini par la fiche.

**Impact :** le cas de réparation promis reste bloqué précisément avec une configuration admise — plusieurs copies pour la même cible. Ce n’est pas un problème de topologie Git ni une demande de lever les autres contrôles.

**Correction minimale :** autoriser une réparation monotone : le retour vérifié de A peut résoudre son erreur tout en laissant celle de B visible ; tout FAIL d’une autre nature reste bloquant, ainsi que toute nouvelle incohérence. Variante : définir un retour groupé atomique pour l’ensemble concerné. **Fermeture :** A puis B (ou le groupe) se réparent sans override global ; entre les deux, B reste explicitement en échec et l’opération ne prétend pas à un audit global PASS.

### N4 — Quelques mentions ne suivent pas encore les décisions prises

**Sévérité : MINOR. Objet :** résumé point 3, §6 l.177, §9 phase 1, §11 et annexe A. **Statut : OUVERT.**

**Scénario et preuve :** un lecteur suivant le résumé solliciterait à nouveau les huit choix et la décision de relecture, déjà actés en §11 et par ce mandat. §6 laisse `move` ouvert alors que l.260 le décide ; phase 1 annonce cinq commandes malgré cette sixième action. Enfin, déplacer un clone emporte son `.git/copie.json` : la condition de bannière de l.118 reste vraie, contrairement à la disparition annoncée en l.177. Les lectures de §11 priment, donc ce ne sont pas des décisions à reprendre.

**Impact :** permissions redemandées inutilement et périmètre d’implémentation ou d’affichage ambigu. La liste de rapatriement de l’annexe reste aussi formulée avec les papiers du tour précédent ; elle doit nommer les nouveaux papiers avant une remise ultérieure.

**Correction minimale :** marquer les choix comme pris, intégrer `move` à la liste, décrire la bannière conservée comme pointeur daté, et actualiser l’inventaire des pièces à rendre. Aucun déplacement ni rapatriement n’est demandé par cette revue.

## D — État du dossier en fin de mandat

Les **378 fichiers préexistants** ont été photographiés par empreinte dans `runs/v2/baseline.json`, puis comparés après les sondes et lors de la remise. Source, anciens rapports, mandats, fiches et anciens sous-dossiers de `runs/` sont inchangés. Le livrable est créé exclusivement ; aucun fichier existant à la racine n’est réécrit.

Seuls `runs/v2/` et `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V2.md` ont été produits. Aucun accès à un autre dossier de travail, aucun réseau, aucune suppression, aucun record ou décision réels. Les renommage/création du scénario A/B restent dans la nouvelle fixture. Les sondes ne sont pas les tests d’acceptation d’une fonctionnalité construite, et la suite entière du contrôleur n’a pas été relancée.

Preuves à conserver avec cette lecture :

| Pièce | Octets | SHA-256 |
|---|---:|---|
| `runs/v2/replay.py` | 8227 | `f08664ce727a76efa4cf8c3c330ec65284a9c305953fe158c66e004a9808e468` |
| `runs/v2/results.json` | 2045 | `68a88afa8ded707fc9fd95a97307e8b454c572b6c289836e994c2cfef97605fa` |
| `runs/v2/commands.json` | 10075 | `309d29262eddaf24651050e49e82d0930d7cf0fd0ce483a5473a411f8cc64862` |
| `runs/v2/baseline.json` | 48637 | `e6d77fdaab409a753941a6fe165a4b976104abc4fe82f08c6b4c8fc21f9a1611` |

La vérification finale et l’empreinte du livrable sont consignées dans `runs/v2/final-verification.json`. Toute correction après remise donnera lieu à une révision liée ou à un erratum.

## E — Verdict terminal

`CADRAGE_TABLEAU_DES_CLES_V2_REQUIRES_MAJOR_REDLINE`
