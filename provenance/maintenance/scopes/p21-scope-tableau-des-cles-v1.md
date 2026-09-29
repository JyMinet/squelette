> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Fiche de cadrage — « Tableau des clés »

Copies de dépôt : ouverture, retour, effacement.

| | |
|---|---|
| Squelette de référence | 3.20.2 (atelier `~/Projets/squelette-atelier`, tag `v3.20.2`) |
| Version de la fiche | V1 — 2026-09-28 |
| État | PROPOSÉE — à relire par une seconde IA avant toute construction |
| Chantier | numéro à attribuer dans `provenance/roadmap-template.v1.json` (prochain numéro libre, P21 si P20 reste le paquet) ; correspond au lot « ménage à la clôture » de l'idée coût du 14 sept. ; indépendant du chantier P20 « paquet de chantier », cadré à part — l'ordre entre les deux est à décider par Jeoffrey |
| Version visée | la suivante après 3.20.2 (3.21.0 si aucune autre ne passe avant) |
| Auteur | Claude, projet Claude « Squelette », sur demande de Jeoffrey (discussion du 28 sept. 2026) |
| Écritures | aucune : rien n'a été écrit ni exécuté dans un dépôt ; cette fiche est un texte |

## Résumé en trois points (pour le Project Owner)

1. **Ce qui s'est passé.** Les copies de dépôt (chantier, revue, répétition) naissent bien — la règle « jamais l'original comme terrain d'essai » marche — mais aucune n'a de fin officielle. Résultat : une douzaine de dossiers en trois semaines, cinq noms différents pour la même idée, deux grands ménages faits à la main, et un jour un mandat qui ne vivait que dans une copie et qu'il a fallu sauver avant d'effacer.
2. **Ce que ça change.** Le dépôt d'origine tient un tableau des clés : chaque copie y a un ticket (la décision qui l'a autorisée), un sort prévu dès le départ et une date de retour. Rendre les clés se prouve (les commits sont revenus, les documents sont rangés) au lieu de se déclarer. Fermer un chantier ou promouvoir une version exige que les clés soient rendues. L'outil n'efface jamais rien : il donne la liste des voitures prêtes à sortir et le script que Jeoffrey lance lui-même.
3. **Ce qu'il doit faire.** Rien tout de suite. Faire relire cette fiche par la seconde IA (mandat joint), puis répondre aux sept questions de la section 8. La construction se fera dans une copie — la première à avoir un ticket, tenu à la main en annexe.

---

## 1. Constat (inventaire de mémoire, à confirmer en phase 0)

Dossiers créés depuis le 5 sept. 2026 pour protéger un original, d'après l'historique du projet Claude « Squelette » :

| Dossier | Usage réel | Sort |
|---|---|---|
| `squelette-challenge-codex` | revue (3.9.0) | effacé le 9 sept. après confirmation |
| `squelette-revue-2` | revue (3.13.0) | sort inconnu |
| `squelette-controle-3.15.2` | revue | sort inconnu |
| `squelette-controle-3.18.2` (859 Mo) | revue | effacé le 15 sept. |
| `squelette-revue-p7` (14 Mo) | revue de cadrage | effacé le 15 sept. |
| `squelette-chantier-p19` | chantier (construction 3.20.0) | effacé le 15 sept. |
| `squelette-chantier-p20` | chantier (P20, le paquet) | effacé le 28 sept. ; ses 12 papiers uniques déplacés dans `~/Projets/_archives/papiers-p20`, hors de tout dépôt |
| `squelette-mutation-20260917` | revue (mandat du 17 sept.) | sort inconnu |
| `alpha-copie-repetition-20260907` | répétition (montée) | effacé le 15 sept. |
| `alpha-copie-repetition-20260909` | répétition (montée) | effacé le 15 sept. |
| `alpha-bootstrap-aborted-20260820` (1,2 Mo) | amorçage abandonné | laissé à la main de Jeoffrey |
| trois dossiers vides | — | effacés le 15 sept. |

Observations :

- Six mots pour trois usages : `challenge`, `revue`, `controle`, `mutation` (tous des revues), `chantier`, `copie-repetition`. La référence est tantôt une version, tantôt un numéro de chantier, tantôt une date, tantôt rien.
- Deux ménages à la main (script du 12 sept. ; 893 Mo le 15 sept.), chacun précédé d'une vérification d'empreintes faite exprès.
- Le 15 sept., deux mandats ne vivaient que dans les dossiers à effacer ; ils ont été copiés dans `provenance/maintenance/scopes/` sous TPL-D-075 avant l'effacement. Leçon notée ce jour-là : « vérifier les mandats avant d'effacer un dossier de chantier ».
- Le 28 sept., l'établi du chantier P20 a été effacé après sauvegarde de ses papiers uniques dans un dossier d'archives hors de tout dépôt : le réflexe existe, mais rien n'en garde la trace ni ne pourrait la vérifier (question 7).
- Aucun endroit du dépôt ne dit quelles copies existent, pourquoi, ni ce qu'on en fera.

Critère d'arrêt (quand un défaut mérite une règle) : le défaut s'est produit plus d'une fois, a coûté deux ménages et a failli faire perdre un document. Il mérite une règle.

## 2. Les trois façons dont ça casse

- **S1 — Le parking.** Le travail est rapatrié, le dossier reste. Personne ne sait plus s'il peut partir ; il faut recalculer des empreintes pour le savoir. Cas réel : `squelette-controle-3.18.2`, 859 Mo, effacé trois jours après la fin de son usage.
- **S2 — Le second original.** Le travail continue dans la copie après sa livraison, ou la copie garde des commits qui ne reviennent jamais, ou une copie faite avec ses liens GitHub/NAS envoie quelque chose. Rien aujourd'hui ne distingue, dans la copie, une copie d'un original.
- **S3 — La perte à l'effacement.** Un document né dans la copie (mandat, rapport, note) part avec elle ; le rapport rangé dans le dépôt perd la trace de ce au nom de quoi il a été écrit. Cas réel : 15 sept., évité de justesse.

Hors périmètre, mais nommé pour ne pas le confondre : **S0 — la dérive inverse** (un agent écrit dans l'original au lieu de la copie, WI-061 du 7 sept.). Le double arrêt la couvre ; cette fiche n'y touche pas.

## 3. But et non-buts

**But.** Toute copie d'un dépôt gouverné présente sur le disque de Jeoffrey a : un ticket (la décision humaine qui l'a autorisée), un sort prévu à l'ouverture, une date de retour, une preuve de retour vérifiée par l'outil, et une fin enregistrée. L'outil de l'original refuse de déclarer fini ce qui détient encore des clés.

**Non-buts.**

- L'outil ne crée ni n'efface jamais un dossier. L'effacement reste le geste de Jeoffrey (règle « on ne supprime pas », inchangée).
- Pas de surveillance du disque : l'outil ne connaît que les chemins qu'on lui déclare (un inventaire à la demande, en lecture seule, est proposé en option — section 7).
- Les clones de session dans la VM de Claude ne sont pas suivis : ils meurent avec la session.
- Rien ne change à la politique des branches ni au double arrêt.
- Aucun nouveau document Markdown à lire au démarrage.

## 4. Principes

1. **Une copie = un chantier = un ticket.** Pas de copie sans décision humaine qui la nomme ; le nom de la copie se déduit de son usage et de sa référence.
2. **Le tableau des clés vit dans l'original.** C'est l'original qui sait où sont ses copies, pourquoi, depuis quand, et ce qu'on en fera. Une copie sans sort prévu est une anomalie dès l'ouverture.
3. **Une copie n'est jamais un second original.** Pas de version, pas de tag, pas de lien GitHub ni NAS ; `status` dans la copie dit « je suis une copie de … ».
4. **Fermer le chantier, c'est rendre les clés.** Aucune clôture de Work Item ni promotion de version tant qu'une copie du ticket n'est pas au moins « rendue » (preuve vérifiée ou rien à rendre). Rendre se prouve, ne se déclare pas.
5. **Le ticket avant la voiture.** On enregistre l'ouverture dans l'original **avant** de faire la copie, pour que la copie emporte son propre ticket et que sa branche ne diverge pas de la canonique à cause de lui.

## 5. Mécanique proposée

### 5.1 Le registre

- Un fichier par dépôt, record administratif comme `ideas-state` : `project_control/copies-state.v1.json` dans un projet dérivé ; `provenance/copies-state.v1.json` dans le squelette lui-même (même précédent que les idées).
- Record canonique : il ne vit que sur la branche canonique et le contrôleur le committe lui-même (`chore(project-control): …`), règle 3.2.0 inchangée. Une branche de travail qui le porte est refusée par le garde-fou (règle existante, à couvrir par un essai).
- Ce n'est pas une autorité : il n'est pas routé par `mandatory-documents`, il n'entre pas dans la preuve de lecture, il ne coûte rien au démarrage. Il se lit par `status` et par la vue roadmap.

Une entrée :

```
id            COPY-NNN
name          nom du dossier (règle de nommage, 5.2)
path          chemin absolu déclaré
usage         chantier | revue | repetition
ticket        HD-NNN (projet dérivé) ou TPL-D-NNN (squelette) — la décision qui nomme le dossier
closes_with   WI-NNN, ou une version X.Y.Z, ou HD-NNN / TPL-D-NNN
origin        commit copié, tag s'il y en a un, root_commit (identité du dépôt)
fate          RETURN_THEN_ERASE | ERASE | KEEP
due           date de retour prévue
opened_at     date
state         OPEN | RETURNED | ERASED | KEPT
returns       liste de preuves : {kind: commit|file, ref, sha256, verified_at}
closed_at     date ; closing_decision pour KEPT
```

États : `OPEN → RETURNED → ERASED | KEPT`. Terminaux : `ERASED`, `KEPT`. « À effacer » n'est pas un état : c'est `RETURNED` avec un sort autre que `KEEP`.

### 5.2 Le nom

`<dépôt>-<usage>-<référence>`, usage pris dans la liste fermée `chantier | revue | repetition`, référence = numéro de chantier, version ou identifiant du ticket ; suffixe `-2`, `-3` si un même ticket a besoin de plusieurs copies. Exemples : `squelette-chantier-p20`, `squelette-revue-3.20.2`, `alpha-repetition-wi-083`. La date n'entre pas dans le nom : le registre la porte. `copy open` refuse un nom hors règle.

### 5.3 L'ouverture — `copy open`

Lancée dans l'original, depuis la canonique. Arguments : `--path`, `--usage`, `--ticket`, `--closes-with`, `--fate`, `--due`.

Refus mécaniques :

- ticket absent ou inconnu du journal des décisions ;
- ticket dont la ligne `Folder scope:` ne contient pas le chemin déclaré (la copie doit être exactement le dossier que le double arrêt a nommé) — à confirmer en phase 0 : la ligne est-elle lisible par la machine dans les deux journaux (HUMAN_DECISIONS.md et provenance/CHANGELOG.md) ?
- sort hors liste, date de retour absente, `closes_with` absent ;
- chemin égal à l'original, ou contenu dans l'original, ou contenu dans une autre copie ouverte (pas de copie de copie : les clones jetables d'une revue vivent dans son `runs/` et partent avec elle) ;
- nom hors règle (5.2).

Le chemin peut ne pas encore exister : le ticket précède la voiture (principe 5). La copie se fait ensuite, par le geste déjà autorisé par le double arrêt.

### 5.4 La copie sait qu'elle est une copie

Aucun fichier marqueur. Dans un dossier dont le chemin réel correspond à une entrée `OPEN` de son propre registre (emporté à la copie), `status` commence par : « COPIE de <original> — ticket <…> — sort prévu <…> — retour attendu le <…> ». Un dossier copié sans ticket, ou déplacé après coup, n'affiche rien : `status` dit « ce dossier n'a pas de ticket ». L'audit dans la copie ne change pas : une copie doit pouvoir tout exécuter.

### 5.5 Le retour — `copy return`

Lancée dans l'original. La preuve dépend de l'usage :

- **chantier** : `--commit <sha>` (un ou plusieurs) ; l'outil vérifie que chaque commit est atteignable depuis une référence de l'original (`merge-base --is-ancestor`), enregistre la branche qui le porte, **et** lit les branches de la copie : toute branche de la copie qui n'est pas contenue dans l'original doit être soit déclarée dans les preuves, soit explicitement abandonnée (`--abandon <branche>`). Rien ne reste dans la copie sans qu'on l'ait dit.
- **revue** : `--file <chemin dans l'original> --sha256 <…>` pour chaque livrable **et** pour le mandat qui l'a commandé ; l'outil vérifie que chaque fichier existe, est suivi par Git, et porte l'empreinte déclarée. Refus si le mandat manque (leçon du 15 sept.). Si la question 7 le décide, un chemin d'archive hors dépôt (`--archive <chemin absolu> --sha256 <…>`) est accepté aussi, vérifié par existence et empreinte seulement.
- **chantier arrêté avant livraison** (cas du 28 sept.) : ses branches sont déclarées abandonnées et ses papiers uniques sont rendus comme ceux d'une revue (fichiers déclarés, vérifiés) ; rien ne part sans avoir été nommé.
- **repetition** : rien à rendre ; `copy return` passe la copie en `RETURNED` avec un rapport facultatif (`--file`), vérifié de la même manière s'il est déclaré.

Lire la copie n'est pas en sortir : la commande ne modifie jamais la copie.

### 5.6 La fin — `copy close`

`--state ERASED` : refusé si le chemin existe encore (« la voiture est encore là »). `--state KEPT` : exige `--decision <HD/TPL-D>` (garder une copie comme constat daté est une décision) et un chemin existant. Une copie `KEPT` reste visible dans `status` (« conservées : n ») : elle ne disparaît pas de la vue.

### 5.7 Fermer le chantier, c'est rendre les clés

- `close WI-NNN` refuse si une copie dont `closes_with = WI-NNN` est encore `OPEN`. `RETURNED` suffit : l'effacement, geste humain, peut venir après.
- Vérification d'audit `COPIES_RETURNED` : FAIL si une copie est `OPEN` alors que son `closes_with` est clos (Work Item `DONE`, version taguée, décision enregistrée). Pour le squelette, la procédure de promotion (fast-forward + tag + TPL-D) intègre `copy return` juste après le tag : la fenêtre entre les deux est fermée par la même main.
- `status`, une ligne : « Copies : n ouvertes (dont k en retard) · m à effacer · p conservées ». La vue roadmap gagne une section du même contenu, générée, jamais rédigée.

### 5.8 L'effacement

L'outil n'efface rien. `copy cleanup` écrit un script bash (`set -euo pipefail`, textes complets) qui, pour chaque copie `RETURNED` à effacer : re-vérifie les preuves du registre (commits présents, empreintes des fichiers), s'arrête au premier écart, efface le dossier, et affiche la commande `copy close --state ERASED` à lancer ensuite. Jeoffrey lance le script dans son Terminal ; c'est la forme qu'il a demandée le 12 sept.

### 5.9 Adoption par un projet existant

Comme pour les baselines : les copies antérieures à l'adoption ne sont jamais reconstruites. Un projet qui monte vers cette version part d'un registre vide ; les dossiers déjà présents sur le disque relèvent d'un choix de Jeoffrey (les effacer, ou en enregistrer certains `KEPT` sous décision). L'audit d'un projet qui vient d'adopter la règle est PASS par construction.

### 5.10 Coût

Registre non routé, non lu par la preuve de lecture ; une ligne de plus dans `status` ; une commande à quatre verbes. Le double arrêt ne change pas : le ticket **est** la décision qu'il produit déjà. Ce que l'outil demande en plus tient dans les arguments de `copy open`.

## 6. Limites assumées

- Une copie jamais déclarée est invisible : le registre ne connaît que ce qu'on lui dit. (Inventaire à la demande en option, section 7.)
- L'outil ne peut pas empêcher un `git push` depuis une copie qui aurait gardé ses liens : la règle « sans liens » reste doctrine et geste de copie ; le retour (5.5) révèle après coup les commits qui ne sont pas revenus, pas les envois.
- Une copie déplacée ou renommée perd sa bannière `status` ; le registre garde l'ancien chemin jusqu'à correction (`copy open` d'une entrée corrigée sous le même ticket, l'ancienne fermée).
- L'outil ne voit pas d'autre disque, d'autre machine, ni la VM de session.
- Un ticket peut nommer un dossier plus large que la copie (un dossier parent accordé) : la vérification `Folder scope` accepte alors tout chemin contenu dedans, ce qui est moins strict que « exactement le dossier ».

## 7. Options écartées, et pourquoi

- **Les branches seules.** Une branche protège le contenu, pas le dossier ; le danger réel est l'agent qui écrit au mauvais endroit. La copie l'en empêche physiquement, la branche non. Les branches restent la manière de travailler **dans** la copie (`claude/vX.Y-…`) et de rapatrier.
- **Les worktrees Git** (`git worktree add ../squelette-chantier-p20`). Inventaire gratuit (`git worktree list`), pas de duplication des objets. Écartés parce qu'un worktree partage `.git` et les remotes : impossible d'y donner un dossier « sans liens GitHub ni NAS », et une commande dans le worktree touche le dépôt de l'original. Contraire au principe 3.
- **Un fichier marqueur écrit dans la copie.** Écrit par une commande de l'original dans un autre dossier : sortie de périmètre à chaque ouverture. Remplacé par le registre emporté (5.4) — réutilisation plutôt qu'objet neuf.
- **Un jumeau Markdown du registre** (comme `IDEAS.md`). Un document de plus à tenir et à lire ; `status` et la vue roadmap suffisent. Pourra venir si l'usage le réclame.
- **L'effacement par l'outil.** Contraire à la règle « on ne supprime pas » ; le script lancé par Jeoffrey garde la main humaine et la vérification.
- **Le retard comme échec d'audit.** Une copie en retard bloquerait les commits de l'original, alors que le retard est un signal, pas une incohérence. Proposé en avertissement `status` ; l'échec d'audit est réservé à l'incohérence (ticket clos, clés non rendues). Question 1.
- **L'inventaire automatique du disque.** Une lecture d'un dossier parent (`copy scan --root …`, lecture seule, sur demande) qui listerait les dossiers portant `AGENTS.md` + `scripts/project_control.py` et le même `root_commit` sans entrée au registre — « voitures sans ticket ». Utile pour la phase 0 et les ménages ; pas dans la mécanique de base. Question 4.

## 8. Décisions à prendre par Jeoffrey (après la relecture)

1. **Le retard** : simple avertissement dans `status` (proposé), ou échec d'audit qui bloque les commits de l'original ?
2. **La vérification du ticket** : si la phase 0 montre que `Folder scope` n'est pas lisible par la machine dans `provenance/CHANGELOG.md`, accepte-t-on, pour le squelette seul, un ticket cité sans vérification du chemin (déclaration), ou corrige-t-on d'abord le format des entrées TPL-D ?
3. **Les copies conservées** (`KEPT`) : les autoriser, sous décision, comme constats datés (proposé) — ou n'admettre que le retour puis l'effacement ?
4. **L'inventaire à la demande** (`copy scan`) : le construire dans cette version, plus tard, ou jamais ?
5. **Les copies existantes** au moment de l'adoption : effacement (ton geste, script fourni) ou enregistrement `KEPT` de certaines ?
6. **Les noms** : `copy open / return / close / cleanup` (proposés, deux mots comme `decision bind`) — tes mots.
7. **Les papiers d'une revue ou d'un chantier arrêté** : rangés dans le dépôt (`provenance/maintenance/`, vérifiés par Git et par empreinte — proposé), ou dans `~/Projets/_archives/` hors dépôt comme le 28 sept. (vérifiés par empreinte seulement), ou les deux admis ?

## 9. Plan

**Phase 0 — mesure, lecture seule, droit d'arrêter.** Dans une copie de lecture du squelette et, si accordé en lecture, d'Alpha : (a) vérifier la forme des lignes `Folder scope:` dans les deux journaux ; (b) vérifier que la promotion peut rester un fast-forward avec un record `copy return` posé après le tag ; (c) inventorier les dossiers présents sous `~/Projets` (lecture seule, sur accord) et classer chacun selon la section 1. Rapport `RAPPORT-MESURE-<chantier>.md` à la racine de la copie, verdict fermé `<CHANTIER>_MEASURE_PASS_BUILD_MAY_START | _STOP_<raison>`.

Trois conditions d'arrêt : la ligne `Folder scope` n'est lisible dans aucun des deux journaux ; le record de retour rend la promotion impossible sans fusion ; un projet dérivé qui adopte la règle passerait en audit FAIL sans geste humain (contraire à 5.9).

**Phase 1 — construction dans une copie.** Sous double arrêt distinct, dans `squelette-chantier-<numéro>` (première copie à ticket, annexe A) : registre et schéma, les quatre commandes, `COPIES_RETURNED`, la ligne `status`, la section de vue, le script de ménage, doctrine dans `AGENTS.core.md` (une section « Copies ») et `project_control/README.md`, manifeste du core, `demo.py --write`, CHANGELOG (TPL-D), roadmap. Essais rouges avant / verts après (section 10). Relecture du code par la seconde IA si Jeoffrey le demande.

**Phase 2 — livraison dans l'atelier.** Double arrêt séparé, fetch de la branche, main intouché, aucun tag, aucun push ; promotion sur son mot. Puis `copy return` de la copie de chantier et son effacement par lui : le chantier se ferme en appliquant sa propre règle.

**Phase 3 — plus tard, chacun sous son double arrêt** : montée d'Alpha (jamais pendant un de ses chantiers), rafraîchissement du miroir public.

## 10. Essais attendus (rouges sur 3.20.2, verts après)

1. Un projet sans registre : audit PASS ; `copy open` crée le registre au premier usage, depuis la canonique.
2. `copy open` refuse un nom hors règle, un usage hors liste, un sort hors liste, une date de retour absente.
3. `copy open` refuse un ticket inconnu, et un ticket dont `Folder scope` ne contient pas le chemin.
4. `copy open` refuse un chemin dans l'original ou dans une copie ouverte.
5. `status` dans la copie affiche la bannière quand son chemin correspond à une entrée `OPEN` ; rien quand elle a été déplacée.
6. `copy return` (chantier) refuse un commit absent de l'original ; refuse tant qu'une branche de la copie non contenue dans l'original n'est ni déclarée ni abandonnée.
7. `copy return` (revue) refuse un fichier absent, non suivi, ou d'empreinte différente ; refuse sans mandat déclaré.
8. `close WI-NNN` refuse avec une copie `OPEN` ; accepte avec `RETURNED`.
9. `COPIES_RETURNED` : FAIL quand la version de `closes_with` est taguée et la copie `OPEN` ; PASS après `copy return`.
10. `copy close --state ERASED` refuse si le dossier existe ; `--state KEPT` refuse sans décision.
11. Le garde-fou refuse une branche de travail qui porte le registre.
12. `copy cleanup` ne liste que les copies `RETURNED` à effacer, et son script s'arrête sur une empreinte qui ne correspond plus.
13. Un projet dérivé qui monte vers cette version reste en audit PASS sans registre.

## Annexe A — tickets tenus à la main pour ce chantier (en l'absence du registre)

| Nom | Usage | Origine | Ticket | Sort | Retour attendu |
|---|---|---|---|---|---|
| `squelette-revue-tableau-des-cles` | revue | export du tag `v3.20.2`, sans `.git` ni liens | décision de Jeoffrey ouvrant la relecture (mandat joint) | rendre (livrable + mandat copiés dans `provenance/maintenance/`), puis effacer | à la remise de la relecture |
| `squelette-chantier-<numéro>` | chantier | copie de l'atelier au commit de départ, sans liens | double arrêt de la phase 1 (TPL-D à venir) | rendre (branche `claude/v3.21-…` fetchée dans l'atelier), puis effacer | à la promotion |

Ces deux lignes deviennent les deux premières entrées du registre si la construction aboutit ; sinon elles restent ici, datées.
