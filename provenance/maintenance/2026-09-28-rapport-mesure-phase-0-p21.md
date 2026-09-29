> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Rapport de mesure — chantier P21 « Tableau des clés » — phase 0

Date : 2026-09-28, 18:40–18:55 (Europe/Zurich). Auteur : Claude. Mandat : double arrêt du 2026-09-28 (STOP 1 « Je suis ok », 18:32 ; STOP 2, 18:33 : « Confirmé : dossier de chantier ~/Projets/squelette-chantier-p21, copie de l'atelier sans liens GitHub ni NAS, atelier et Alpha lus seulement, aucun envoi, aucun effacement. »). Référence : `FICHE-CADRAGE-TABLEAU-DES-CLES-V3.md`, section 9.

## Résumé en trois points

1. **Ce qui s'est passé.** Le dossier de chantier est monté : une copie de l'atelier débranchée, avec son garde-fou et sa fiche de sortie. Les trois mesures prévues sont faites, en lecture seule. L'atelier et Alpha n'ont pas bougé.
2. **Ce que ça change.** Aucun des deux arrêts prévus ne se déclenche : le tiroir caché de Git se classe entièrement, et l'inventaire complet d'Alpha prend moins de dix secondes. Une pièce de la fiche ne tient pas : l'« identité » d'un dossier par ses numéros système n'est pas fiable à travers le montage du poste. Elle est remplacée par un jeton porté par la fiche de sortie, toujours contrôlé avec l'empreinte du contenu.
3. **Ce qu'il doit faire.** Rien. La construction commence.

Verdict : `P21_MEASURE_PASS_BUILD_MAY_START` (avec l'ajustement A-01).

## A — Montage du dossier de chantier

| Élément | État |
|---|---|
| Dossier | `~/Projets/squelette-chantier-p21` — c'est la copie elle-même (clone à la racine, conforme au modèle `CLONE` de la fiche) |
| Origine | clone de `~/Projets/squelette-atelier` à `main` = `b9fe0e7bd91ab02a9cda967fdddd6c51b56d13c8` (tag `v3.20.2` sur `9b8792e`) ; 37 tags |
| Liens | aucun remote (`git remote` vide) : ni GitHub, ni NAS, ni l'atelier |
| Garde-fou | `install-gate` : PASS ; `.git/hooks/pre-commit` identique à `scripts/hooks/pre-commit` |
| Branche de travail | `claude/p21-tableau-des-cles` créée sur `main` ; la copie reste sur `main` (aucun remplacement de fichier suivi à faire dans le dossier monté) |
| Réglages Git | `core.createObject=rename`, `gc.auto=0`, `maintenance.auto=false` — pour que Git n'ait pas à effacer de fichiers temporaires dans le dossier monté |
| Fiche de sortie | `.git/copie.json`, posée à la main (antérieure à l'outil, jamais importée) |
| Vérification | `git fsck` sans erreur ; `git status` propre |
| Transfert | `transfert/p21-depart.bundle` (1 095 672 octets, historique complet) : sert à travailler dans une copie de session ; abandonné en bloc au retour |
| Atelier | `main` toujours à `b9fe0e7`, arbre propre, aucun verrou créé |

## B — Mesure 1 : le tiroir `.git` réel

**Copie du chantier (clone récent, Git 2.34 dans la VM) :** `HEAD`, `branches/` (vide), `config`, `copie.json`, `description` (texte par défaut), `hooks/` (exemples `*.sample` + `pre-commit` installé), `index`, `info/exclude` (commentaires seulement), `logs/`, `objects/`, `packed-refs`, `project-control.lock` (verrou administratif du contrôleur, vide), `refs/`.

**Alpha (lecture seule) :** en plus des mêmes éléments : `COMMIT_EDITMSG`, `FETCH_HEAD`, `ORIG_HEAD`, `info/refs` (produit par `update-server-info`), `index.lock.perime-20260912` (verrou périmé renommé à la main), `verrous-perimes-20260912/` (dossier), 4 entrées de stash, des références hors `heads/`/`tags/` (`refs/codex/turn-diffs/checkpoints/…`, écrites par Codex), 69 branches `work/…`, un remote `nas`, `user.*` dans la config.

**Liste fermée qui en découle (à écrire dans la doctrine) :**

| Catégorie | Éléments | Traitement |
|---|---|---|
| Lus comme références | `HEAD`, `refs/**` (tous espaces, y compris `refs/codex/…` et `refs/stash`), `packed-refs`, `logs/**` | chaque référence et chaque commit seulement joignable par le reflog devient un élément ; couvert si l'original le contient (par ses références ou ses reflogs) |
| Techniques, ignorés par leur nom | `objects/**`, `index`, `COMMIT_EDITMSG`, `FETCH_HEAD`, `ORIG_HEAD`, `shallow`, `info/refs`, `copie.json`, tout `*.lock`, `hooks/*.sample`, `branches/` vide, `worktrees/` vide, `description` au texte par défaut, `info/exclude` sans règle active | aucun élément |
| À rendre ou abandonner | autres fichiers de `hooks/` (sauf `pre-commit` identique à `scripts/hooks/pre-commit`), autres fichiers de `info/`, `description` modifiée, clés de `config` hors préfixes techniques (`core.`, `user.`, `branch.`, `gc.`, `maintenance.`, `init.`, `extensions.`, `pack.`, `fetch.`, `pull.`) — en particulier tout `remote.*`, qui est un lien | un élément par fichier ou par clé |
| Refusés, opération en cours | `MERGE_HEAD`, `MERGE_MSG`, `MERGE_MODE`, `AUTO_MERGE`, `SQUASH_MSG`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `REBASE_HEAD`, `rebase-merge/`, `rebase-apply/`, `sequencer/`, `BISECT_*` | « non pris en charge » |
| Refusés, configuration | `modules/`, `worktrees/` non vide, `.gitmodules` dans l'arbre | « non pris en charge » |
| Tout le reste | par exemple `index.lock.perime-20260912`, `verrous-perimes-20260912/` d'Alpha | « non pris en charge », jamais compté comme vide |

Deux choix de la fiche sont précisés par la mesure :

- `info/exclude` et `description` : le texte par défaut varie selon la version de Git ; la règle retenue ne compare pas à un modèle mais regarde le contenu (aucune règle active ; texte par défaut connu).
- `config` : la classer entière comme élément obligerait à l'abandonner à chaque retour ; la règle retenue inventorie les clés qui portent du sens (liens, alias, inclusions, hooks, filtres) et laisse les réglages techniques.

Arrêt n° 1 (« la liste fermée ne peut pas être établie sans catégorie inconnue sur un clone ordinaire ») : **non déclenché** — sur le clone du chantier, tout se classe ; les deux éléments inconnus d'Alpha sont des résidus d'un incident passé, et leur refus est voulu.

## C — Mesure 2 : le temps de l'inventaire complet

Sur Alpha, à travers le montage, en lecture seule (`GIT_OPTIONAL_LOCKS=0`) :

| Étape | Résultat |
|---|---|
| Listes (`ls-files --others`, `ls-files --others --ignored`, `diff HEAD --name-only`) | 6,1 s — 0 non suivi, 5 696 ignorés, 0 modifié |
| Empreintes de tous ces fichiers | 5 696 fichiers, 769,8 Mo, 2,7 s |
| Répartition des ignorés | `data/` 5 453, `modules/` 229, `Claude outputs/` 5, `scripts/` 4, `reports/` 2, `tests/` 2, `.DS_Store` 1 |

Arrêt n° 2 (« l'inventaire d'une copie ordinaire ne tient pas dans un appel de 3 minutes ») : **non déclenché** — moins de 10 s pour le plus gros dépôt gouverné présent.

## D — Mesure 3 : les dossiers de `~/Projets`

Lecture seule (noms, tailles, gouvernance, identité Git).

| Dossier | Taille | Nature | Rapport au constat |
|---|---:|---|---|
| `squelette-atelier` | 20,8 Mo | original du squelette (racine `35da2a2d`, `origin` + `nas`) | — |
| `squelette-chantier-p21` | 20,7 Mo | copie `CLONE` de l'atelier, sans remote | ticket manuel (annexe A) |
| `squelette-revue-tableau-des-cles` | 6,7 Mo | copie `EXPORT` (contenant + `source/`) | ticket manuel (annexe A) |
| `squelette` | 5,8 Mo | miroir public (racine différente `ba4340c1`) | pas une copie : un produit de l'export |
| `alpha` | 1,38 Go | original Alpha (`nas`) | — |
| `alpha-reports` | 11 Mo | rapports hors dépôt | papiers hors dépôt |
| `Dossier jetable Alpha Essai Claude` | 531 Mo | dossier d'essai (scripts, campagne, documents), pas un dépôt | hors périmètre : pas une copie de dépôt, mais un « établi » sans ticket |
| `_archives/squelette-revue-2` | 126,6 Mo | ancienne revue 3.13.0 | constat « sort inconnu » → rangée aux archives |
| `_archives/squelette-decision-projet`, `_archives/squelette-projet-gouverne` | 301,6 Mo + 1,4 Mo | baselines archivées le 6 sept. | archives voulues |
| `_archives/papiers-p20`, `_archives/papiers-claude-atelier` | 200 Ko + 380 Ko | papiers hors dépôt | décision 7 : pas une preuve de retour |
| `Claude outputs` | 60 Ko | scripts et `DETTES_CONNUES.md` | papiers hors dépôt |
| `controle-redaction-human` | vide | — | dossier vide |
| `Redaction_Human`, `boite-a-chaussures`, `BTC holding` et une plateforme d'un ancien projet | — | autres projets gouvernés | pas des copies |

Absents : `squelette-controle-3.15.2`, `squelette-mutation-20260917` (sort « inconnu » dans le constat : ils n'existent plus au premier niveau). Aucun autre dossier au premier niveau ne partage la racine `35da2a2d` de l'atelier : il n'y a aujourd'hui aucune « voiture sans ticket » du squelette hors des archives.

## E — Ajustement A-01 : l'identité d'un dossier

**Constat.** Le dossier Projets est vu par la VM à travers un montage FUSE : `st_dev` = 41 pour tout le montage et des numéros d'inode courts attribués par la couche de montage (208567 pour le chantier). Ces numéros sont stables d'un appel à l'autre dans une même session, mais rien ne garantit qu'ils soient les mêmes dans une autre session, ni dans le Terminal du Mac, où Jeoffrey lance le script de ménage. Une identité device + inode enregistrée dans la VM ferait refuser à tort `copy check` lancé depuis le Mac, ou l'inverse.

**Ajustement.** `copy open` produit un jeton aléatoire, écrit dans la fiche de sortie par le geste de copie (`.git/copie.json` pour un clone, `copie.json` à la racine du contenant pour un export). L'identité d'une copie est alors : sa fiche de sortie, avec le bon identifiant et le bon jeton, au chemin enregistré. `copy return`, `copy move` et `copy check` la contrôlent. La sécurité de l'effacement repose, comme dans la V3, sur l'empreinte complète du contenu. Un double du dossier (même jeton, même contenu) ne contient rien qui n'ait été rendu ; un autre dossier venu occuper la place n'a pas le jeton et est refusé.

**Portée.** Le reste de la V3 est inchangé. La fiche de sortie du chantier P21, posée à la main avant l'outil, n'a pas de jeton : elle n'est pas importée (annexe A).

## F — État en fin de phase 0

- Atelier : `main` à `b9fe0e7`, 0 modification, aucun verrou créé.
- Alpha : lu seulement (listes et empreintes avec `GIT_OPTIONAL_LOCKS=0`), rien écrit.
- Écritures : seulement `~/Projets/squelette-chantier-p21` (copie, fiche de sortie, `transfert/`, ce rapport).
- Aucun envoi, aucun effacement.

## G — Verdict

`P21_MEASURE_PASS_BUILD_MAY_START`
