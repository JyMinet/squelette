> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Fiche de cadrage — « Tableau des clés » — V3

Copies de dépôt : ouverture, retour, déplacement, effacement.

| | |
|---|---|
| Squelette de référence | 3.20.2 (atelier `~/Projets/squelette-atelier`, tag `v3.20.2`) |
| Version de la fiche | V3 — 2026-09-28 ; remplace la V2 (conservée) après la relecture courte `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V2.md` (verdict `CADRAGE_TABLEAU_DES_CLES_V2_REQUIRES_MAJOR_REDLINE` : R01, R04, R06, R07 fermés ; R02, R03, R05 partiels ; N1–N3 MAJOR, N4 MINOR) et sa contre-revue (`CADRAGE_TABLEAU_DES_CLES_V2_REVIEW_OF_RELECTURE_COURTE_PASS`) |
| État | DÉCISIONS PRISES (section 11, 2026-09-28 18:05) — construction possible sur le mot de Jeoffrey et sous son propre double arrêt ; N1–N3 deviennent des essais obligatoires |
| Chantier | P21 si P20 reste le paquet ; ordre entre les deux à décider par Jeoffrey |
| Version visée | la suivante après 3.20.2 |
| Écritures | aucune : cette fiche est un texte |

## Résumé en trois points (pour le Project Owner)

1. **Ce qui s'est passé.** La relecture courte confirme que quatre trous sur sept sont bouchés. Trois rustines étaient incomplètes : le compartiment caché de la voiture (le dossier interne de Git) n'était pas inventorié ; un vieux script de ménage pouvait viser l'ancienne place d'une voiture déplacée, où une autre voiture s'était garée entre-temps ; et avec deux voitures en retard, la réparation se bloquait.
2. **Ce que ça change.** La V3 inventorie le compartiment caché par une liste fermée (ce qu'on ne connaît pas bloque, au lieu de passer) ; le script de ménage dit exactement quelle voiture, à quelle place, dans quel état il va effacer, et refuse si quoi que ce soit a bougé ; les voitures en retard se rendent ensemble, d'un seul coup. La vue se régénère après la pose de l'étiquette de version, comme aujourd'hui.
3. **Ce qu'il doit faire.** Rien à trancher sur le fond : les huit décisions sont prises. Seulement dire si on construit maintenant (les trois cas deviennent des essais obligatoires et la seconde IA relit le code à la fin), ou si la V3 repasse d'abord en relecture.

## 0. Ce qui change

### Depuis la V1

| Constat | Correction | Où |
|---|---|---|
| R01 — cible parente de l'original | Disjonction dans les deux sens, sur chemins résolus, avec l'original et toute copie non effacée ; revérifiée au moment d'effacer | 5.3, 5.8 |
| R02 — contenu hors branches | Le retour porte sur **tout** le contenu de la copie, pour tous les usages | 5.5 |
| R03 — preuve ancienne | Empreinte du contenu enregistrée au retour, recalculée juste avant l'effacement | 5.5, 5.8 |
| R04 — export d'un tag | Fiche de sortie dans la copie (`.git/` pour un clone, contenant pour un export) ; registre de l'original seule autorité | 4.5, 5.4 |
| R05 — ordre de clôture | Un seul ordre : rapatrier, intégrer, rendre, poser le tag | 5.7 |
| R06 — nom de l'annexe | Tickets de l'annexe manuels, jamais importés ; registre initial vide | 5.9, annexe A |
| R07 — coût | Coût décrit par acteur | 5.10 |

### Depuis la V2

| Constat | Correction | Où |
|---|---|---|
| N1 — contenu propre à `.git` hors inventaire | Inventaire de `.git` par liste fermée : références, commits seulement joignables par le reflog, stash, hooks, config, `info/` ; le garde-fou installé identique à sa référence est technique ; sous-modules, worktrees liés, opération Git en cours et tout élément inconnu → refus « non pris en charge », jamais compté comme vide | 5.5 |
| N2 — script après déplacement | Le script transmet à `copy check` le chemin, l'identité et l'empreinte de ce qu'il va effacer ; refus si le registre de la canonique désigne autre chose ; `copy move` invalide donc tout script antérieur | 5.6 bis, 5.8 |
| N3 — réparation bloquée à deux copies | Réparation groupée : une seule transaction rend (ou passe `KEPT` sous décision) toutes les copies en faute, l'audit résultant doit être PASS — seule forme qui passe aussi le garde-fou de commit | 5.7 |
| N4 — mentions périmées | Section 8 marquée décidée ; six commandes ; bannière d'un clone déplacé ; liste des papiers à rendre à jour | 5.4, 6, 8, 9, annexe A |
| Vue et tag | Vue régénérée **après** le tag, comme aujourd'hui : le tag entre dans l'empreinte de fraîcheur de la vue | 5.7 |
| Fenêtre d'effacement | Condition : aucune écriture dans la copie, par personne ni par aucun programme | 5.8 |
| Empreinte | Octets et références, en descendant dans les dossiers ignorés ; device + inode ne sert qu'à détecter un remplacement | 5.5 |
| Retravail après retour | Un retour peut être refait sur une copie `RETURNED` dont le contenu a changé : même règle complète, nouvelle empreinte | 5.5 |

## 1. Constat

Inchangé depuis la V1 (inventaire de mémoire à confirmer en phase 0). Une douzaine de dossiers en trois semaines, six mots pour trois usages, deux ménages à la main, un mandat sauvé de justesse le 15 sept., l'établi du chantier P20 effacé le 28 sept. après sauvegarde de ses papiers hors de tout dépôt, sans trace vérifiable. Aucun endroit du dépôt ne dit quelles copies existent, pourquoi, ni ce qu'on en fera.

## 2. Les façons dont ça casse

- **S1 — Le parking.** Travail rapatrié, dossier resté.
- **S2 — Le second original.** Le travail continue dans la copie, ou n'en revient jamais.
- **S3 — La perte à l'effacement.** Un document né dans la copie part avec elle.
- **S4 — L'effacement de trop.** L'effacement d'une « copie » emporte l'original, une autre copie, un travail repris depuis, ou un autre dossier venu occuper la place. La mécanique existe pour éviter S1–S3 ; elle ne doit jamais créer S4.

Hors périmètre : S0, la dérive inverse (écrire dans l'original), couverte par le double arrêt.

## 3. But et non-buts

**But.** Toute copie **déclarée** d'un dépôt gouverné a un ticket, un sort prévu, une date de retour, une preuve de retour vérifiée, et une fin enregistrée ; aucun effacement proposé par l'outil ne peut toucher l'original, une autre copie, un autre dossier, ni du travail non rendu.

**Non-buts.** L'outil ne crée, ne déplace ni n'efface jamais un dossier (le contrôleur continue de retirer ses propres worktrees jetables, régime séparé, inchangé). Pas de surveillance du disque. Les clones de la VM de session ne sont pas suivis. Le double arrêt et la politique des branches ne changent pas. Aucun nouveau document d'autorité routé.

## 4. Principes

1. **Une copie = un ticket.** Pas de copie sans décision humaine qui la nomme. Un ticket peut couvrir plusieurs copies ; chacune a son entrée.
2. **Le tableau des clés vit dans l'original.** Le registre de l'original, lu sur la branche canonique, est la seule autorité sur l'état d'une copie.
3. **Une copie n'est jamais un second original.** Pas de version, pas de tag, pas de lien GitHub ni NAS. Une copie protège par séparation, pas par interdiction : les droits d'accès restent ceux du mandat.
4. **Rendre les clés avant de fermer.** Aucun Work Item clos, aucun tag de version posé tant qu'une copie rattachée est `OPEN`. Rendre se prouve, pour tout le contenu de la copie.
5. **Le ticket avant la voiture, la fiche de sortie avec la voiture.** L'ouverture s'enregistre dans l'original avant la copie ; le geste de copie, déjà autorisé par le double arrêt, dépose dans la copie une fiche de sortie qui la désigne.
6. **Jamais d'effacement sur une preuve ancienne.** Juste avant d'effacer, on relit le registre courant et la copie telle qu'elle est, à la place exacte qu'on va effacer.
7. **Ce qu'on ne connaît pas bloque.** Un élément que l'inventaire ne sait pas classer n'est jamais compté comme vide.

## 5. Mécanique proposée

### 5.1 Le registre

- Projet dérivé : `project_control/copies-state.v1.json`, record administratif canonique, committé par le contrôleur (règle 3.2.0). Template : `provenance/copies-state.v1.json`, avec le traitement propre au rôle template (branche de référence `main`, comme la vue roadmap du template aujourd'hui) — à écrire explicitement, sans initialiser le template comme un projet.
- Les deux chemins entrent dans la classification des chemins administratifs (ils n'y sont pas en 3.20.2) ; le garde-fou refuse une branche de travail qui **modifie** le registre (la présence héritée de la canonique reste admise).
- Registre absent = registre vide. Il n'entre pas dans les fichiers obligatoires, n'est pas routé, n'entre pas dans la preuve de lecture. Il entre dans les sources qui rendent la vue roadmap périmée.

Une entrée :

```
id             COPY-NNN
name           nom du dossier (5.2)
path           chemin absolu résolu actuel
kind           CLONE (dépôt Git copié de l'original) | EXPORT (contenant de revue avec source/ exporté d'un tag)
usage          chantier | revue | repetition
ticket         HD-NNN (projet) ou TPL-D-NNN (template)
closes_with    WI-NNN | version X.Y.Z  (typé ; jamais une décision)
origin         original_path (résolu), commit ou tag copié, root_commit
fate           RETURN_THEN_ERASE | ERASE | KEEP
due            date de retour prévue
opened_at      date
state          OPEN | RETURNED | ERASED | KEPT
returns        preuves : {kind: commit|file|abandon|keep, ref, sha256, role?, reason?, verified_at}
content_digest empreinte de l'inventaire complet au dernier retour (5.5)
identity       device + inode du dossier au dernier retour ou déplacement
moves          historique : {from, to, at, identity}
closed_at      date ; closing_decision pour KEPT
```

États : `OPEN → RETURNED → ERASED | KEPT` ; `RETURNED → RETURNED` par un nouveau retour complet si la copie a changé ; `KEPT → RETURNED` sous décision (une copie gardée qu'on veut finalement effacer repasse par un retour complet). Terminal : `ERASED`. `copy move` est admis dans tout état sauf `ERASED`.

### 5.2 Le nom

`<dépôt>-<usage>-<référence>`, usage ∈ `chantier | revue | repetition`, référence = numéro de chantier, version ou identifiant de ticket, suffixe `-2`, `-3` pour plusieurs copies d'un même ticket. La date n'entre pas dans le nom.

### 5.3 L'ouverture — `copy open`

Lancée dans l'original, depuis la canonique. Arguments : `--path`, `--kind`, `--usage`, `--ticket`, `--closes-with`, `--fate`, `--due`.

Refus mécaniques :

- **frontière** : sur chemins résolus (liens suivis), refus si la cible est égale à l'original, contenue dans l'original, **contient l'original**, ou chevauche dans un sens ou dans l'autre une copie non `ERASED` ; refus si un composant du chemin est un lien symbolique ; refus si le volume n'est pas monté ou lisible ;
- ticket inconnu, ou HD dont `Folder scope:` ne couvre pas le chemin (chemins résolus : égal ou contenu dans le dossier accordé, jamais une sous-chaîne) ; HD refusée ou sans les deux confirmations (réutilisation de la validation du double arrêt existante) ;
- TPL-D sans lignes structurées `Folder scope:`, `Confirmation 1:`, `Confirmation 2:` (décision 2) ;
- `closes_with` déjà clos (Work Item `DONE`, version déjà taguée) ou inconnu ;
- sort, usage ou kind hors liste, date absente, nom hors règle.

Le chemin peut ne pas encore exister.

### 5.4 La fiche de sortie

Le geste de copie, autorisé par le double arrêt, dépose une fiche de sortie `copie.json` (id, original, chemin prévu, ticket, sort, date de retour, date d'émission) :

- `CLONE` : dans `.git/copie.json` — hors de l'arbre suivi, ne salit rien, ne part pas dans un commit ; le contrôleur 3.20.2 ignore déjà les JSON sous `.git` ;
- `EXPORT` : à la racine du contenant de revue, à côté de `source/` (l'export reste intact ; aucun tag n'est touché).

`status` dans un clone qui porte `.git/copie.json` :

- chemin actuel = chemin de la fiche : « COPIE de <original> — ticket … — retour attendu le … (d'après la fiche de sortie du <date>) » ;
- chemin différent : « COPIE DÉPLACÉE de <original> — la fiche de sortie indique <ancien chemin> ; le déplacement se déclare depuis l'original (`copy move`) ».

L'outil n'écrit jamais dans la copie : la fiche garde son chemin d'origine, la bannière le signale. Un export n'a pas de `status` : la fiche s'y lit comme un document, et le mandat de revue la cite. La fiche est un pointeur daté, pas une autorité.

### 5.5 Le retour — `copy return`

Lancée dans l'original, lecture seule sur la copie. Le retour porte sur **tout le contenu** de la copie, quel que soit l'usage.

**1. L'inventaire** — tout ce que la copie a de différent de son origine.

`CLONE` :

- **arbre de travail** : fichiers modifiés (indexés ou non), non suivis, ignorés (`git status --porcelain=v2 --ignored`), en **descendant dans chaque dossier ignoré** : chaque fichier compte, avec son empreinte ;
- **références** : toutes (branches, tags, notes, HEAD détachée), chaque entrée du stash, et les **commits joignables seulement par le reflog** (travail perdu de vue mais récupérable, par exemple après une branche supprimée) ;
- **contenu propre de `.git`, par liste fermée** :
  - *à rendre ou abandonner* : fichiers de `hooks/` (hors exemples `*.sample` livrés par Git et hors garde-fou installé **identique** au fichier `scripts/hooks/pre-commit` de la copie), `config`, fichiers de `info/` ;
  - *lus comme références* : `refs/`, `packed-refs`, `HEAD`, `logs/` ;
  - *techniques, ignorés par leur nom* : `objects/`, `index`, `ORIG_HEAD`, `FETCH_HEAD`, `COMMIT_EDITMSG`, `description` par défaut, verrous `*.lock`, `copie.json` — la liste exacte s'écrit dans la doctrine après la mesure de la phase 0 ;
  - *refusés, « non pris en charge »* : sous-modules (`modules/`, `.gitmodules`), worktrees liés (`worktrees/` non vide), opération Git en cours (fusion, rebase, cherry-pick, bisect), et **tout élément de `.git` qu'aucune catégorie ne nomme**.

`EXPORT` : tous les fichiers du contenant hors `source/` (descente complète), plus tout écart de `source/` à son manifeste d'export.

**2. Le rendu.** Chaque élément de l'inventaire est couvert par une preuve :

- commit ou référence : atteignable depuis une référence de l'original (`merge-base --is-ancestor`) ;
- fichier : `--file <chemin dans l'original> --sha256 <…> [--role mandat|livrable|rapport|note]` ; committé dans l'original avec ces octets à HEAD (pas seulement suivi) ;
- abandon : `--abandon <élément> --reason "<…>"` ; un dossier jetable (le `runs/` d'une revue, un dossier ignoré de construction) s'abandonne en bloc avec sa raison — son contenu entre quand même dans l'empreinte.

**3. Les refus.** Élément non couvert ; revue sans pièce de rôle `mandat` ; configuration non prise en charge ; dépôt, objet ou fichier illisible. Jamais « rendu par omission ». Une copie refusée reste `OPEN` : Jeoffrey décide (la ranger à la main, puis refaire le retour ; ou `KEPT` sous décision).

**4. L'empreinte.** L'outil enregistre l'empreinte de l'inventaire complet — octets de chaque fichier compté, cibles de chaque référence, contenu des éléments de `.git` à rendre — et l'identité du dossier. Hacher les seules lignes de `git status` ne suffit pas.

**5. Nouveau retour.** Sur une copie `RETURNED` dont le contenu a changé, `copy return` se refait entièrement et remplace l'empreinte.

Un chantier arrêté avant livraison suit la même règle : ses branches sont abandonnées par leur nom, ses papiers uniques rendus comme fichiers.

### 5.6 La fin — `copy close`

`--state ERASED` : refusé si le chemin existe encore. Un chemin absent ne suffit pas si l'identité ne peut être tranchée (volume démonté) : refus « indisponible, pas effacé ». `--state KEPT` : exige `--decision` ; la copie reste visible, exclue de tout nettoyage ; la garder n'autorise pas à y reprendre le travail.

### 5.6 bis Le déplacement — `copy move` (décision 8)

Lancée dans l'original, après que le dossier a été déplacé : `copy move COPY-NNN --path <nouveau>`.

- Frontière de 5.3 refaite pour le nouveau chemin.
- Le ticket doit couvrir le nouveau chemin ; sinon refus — un déplacement hors du dossier accordé demande un nouveau ticket, il ne s'en déduit jamais.
- À l'ancien chemin, plus rien ou un dossier d'une autre identité ; au nouveau chemin, un dossier lisible.
- Copie `RETURNED` : l'inventaire recalculé au nouveau chemin doit avoir l'empreinte enregistrée ; sinon refus et nouveau retour exigé (5.5).
- Le registre prend le nouveau chemin et la nouvelle identité et garde l'historique (`moves`). Tout script de ménage généré avant ne peut plus passer `copy check` (5.8).

### 5.7 L'ordre de clôture

**Un seul ordre, pour toute copie rattachée à une version du template :**

1. rapatrier la branche de la copie dans l'original (fetch) et vérifier ;
2. enregistrer la décision de promotion sur la branche (comme aujourd'hui) puis fast-forward de `main` (intégration, sous le mandat de promotion) ;
3. `copy return` sur `main` (commit administratif, qui passe le garde-fou) ;
4. vérifier dans `status` qu'aucune copie rattachée à la version n'est `OPEN`, puis **poser le tag** sur ce commit : la version figée contient des clés rendues ;
5. régénérer la vue et la committer **après** le tag, comme aujourd'hui (`main` un commit devant le tag) — le tag entre dans l'empreinte de fraîcheur de la vue (`displayed_version_tags`) : une vue régénérée avant le tag serait aussitôt périmée.

Pour un Work Item d'un projet dérivé : rapatrier, intégrer, `copy return` sur la canonique, puis `close`. `close WI-NNN` refuse tant qu'une copie `closes_with = WI-NNN` est `OPEN` ; `copy open` refuse une cible déjà close. Dans un projet dérivé, l'outil ne laisse donc aucun chemin vers une incohérence de clés : elle ne peut naître que d'un tag de version posé trop tôt, dans le template.

`COPIES_RETURNED` (audit) : FAIL si une copie `OPEN` a sa cible close.

**Réparation groupée.** Toute transition administrative passe par le garde-fou de commit, qui refuse un état dont l'audit échoue (contrôleur : `commit_records`, « the commit goes through the commit hook like any other »). Une réparation copie par copie laisserait l'audit rouge tant qu'une autre copie est en faute, donc serait refusée. D'où : quand l'audit n'a que des FAIL `COPIES_RETURNED`, `copy return` accepte plusieurs copies dans **une seule transaction**, qui doit couvrir **toutes** les copies en faute — chacune rendue, ou passée `KEPT` sous décision — et laisser un audit PASS. Tout FAIL d'une autre nature refuse. Pas d'override du garde-fou. Le commit tagué trop tôt garde son registre `OPEN` : incohérence historique connue, signalée, jamais réécrite.

`status` : « Copies : n ouvertes (dont k en retard) · m à effacer · p conservées ». Le retard est un avertissement, jamais un FAIL (décision 1).

### 5.8 L'effacement — `copy check` et `copy cleanup`

- `copy check COPY-NNN --path <P> --identity <I> --digest <D>` (lecture seule, lancée dans l'original) :
  - lit le registre **sur la pointe de la branche canonique** : l'entrée doit être `RETURNED`, avec un sort d'effacement, et porter exactement `path = P`, `identity = I`, `content_digest = D` ;
  - refait la frontière de 5.3 sur `P` résolu ;
  - vérifie qu'à `P` se trouve un dossier d'identité `I` et que son inventaire recalculé a l'empreinte `D`.
  Tout écart refuse : déplacement déclaré, nouveau retour, passage à `KEPT`, contenu nouveau, dossier remplacé ou réoccupé, source illisible.
- `copy cleanup` écrit un script bash (`set -euo pipefail`, textes complets). Pour chaque copie, le script porte en clair `P`, `I` et `D` relevés à sa génération, appelle `copy check` avec eux, s'arrête au premier refus, efface **ce même `P`** (la même variable), puis affiche la commande `copy close --state ERASED`. Une copie à la fois, l'effacement immédiatement après son contrôle. Jeoffrey lance le script.
- Condition écrite en tête du script : aucune écriture dans les copies concernées pendant qu'il tourne — ni par un agent, ni par une personne, ni par un programme (éditeur, synchronisation, sauvegarde). Limite déclarée : quelques instants restent entre le contrôle et l'effacement.

### 5.9 Adoption, et copies d'avant la règle

Registre absent = vide ; audit PASS par construction ; aucune copie antérieure reconstruite. Une copie existante que Jeoffrey veut garder s'enregistre `KEPT` sous décision, comme constat présent, sans retour historique inventé. Les copies de l'annexe A ne sont pas importées.

### 5.10 Coût

- **Pour l'agent au démarrage** : aucun nouveau document d'autorité routé ; la doctrine ajoutée au core (une section « Copies ») allonge le texte déjà lu ; chaque ticket est une décision humaine de plus dans le carnet (comme aujourd'hui avec le double arrêt).
- **Automatique** : `status` et l'audit lisent le registre (pas la copie).
- **Par copie** : `copy open` (sept arguments) ; `copy return` (une preuve par élément de l'inventaire — souvent quelques-unes, un abandon en bloc pour un dossier jetable ; le calcul de l'empreinte lit tous les octets de la copie, coût mesuré en phase 0) ; `copy close` ; `copy move` si la copie bouge.
- **Pour Jeoffrey** : lancer le script de ménage (groupable) — chaque effacement recalcule l'empreinte de la copie —, puis `copy close`.

## 6. Limites assumées

- Une copie jamais déclarée est invisible.
- L'outil ne peut pas empêcher un envoi depuis une copie qui aurait gardé ses liens ; le retour révèle ce qui n'est pas revenu, pas ce qui est parti.
- Une copie déplacée garde sa fiche de sortie d'origine ; sa bannière dit « déplacée » ; le registre ne suit que par `copy move`. Elle n'est jamais déclarée `ERASED` pour autant (identité, 5.6).
- Un volume démonté rend la copie « indisponible », pas « effacée ».
- Quelques instants entre `copy check` et l'effacement (5.8).
- Une copie contenant un sous-module, un worktree lié, une opération Git en cours ou un élément de `.git` inconnu ne peut pas être rendue par l'outil : elle reste `OPEN` jusqu'au rangement humain ou à une décision `KEPT`.
- Un tag posé avant le retour, par erreur, reste incohérent à jamais dans l'histoire (5.7).

## 7. Options écartées

- **Branches seules** : elles ne séparent pas les dossiers (S0). Une copie sépare, elle n'interdit pas : la sécurité vient du mandat et du double arrêt.
- **Worktrees Git** : partagent objets, configuration et remotes ; incompatibles avec « sans liens ». Les worktrees jetables internes du contrôleur restent inchangés.
- **Fichier marqueur dans l'arbre suivi** : écarté ; la fiche de sortie vit dans `.git/` (clone) ou dans le contenant (export).
- **Jumeau Markdown** du registre : pas maintenant.
- **Effacement ou déplacement par l'outil** : non ; le script, lancé par Jeoffrey, fait lui-même le dernier contrôle ; le déplacement est un geste, `copy move` le constate.
- **Réparation copie par copie** : refusée par le garde-fou tant qu'une autre copie est en faute ; remplacée par la réparation groupée (5.7). Assouplir le garde-fou pour accepter un état « partiellement rouge » ouvrirait une brèche générale : écarté.
- **Hacher tout `.git` brut** : ses fichiers techniques changent sans nouveau travail (index, objets repackés) ; remplacé par la liste fermée.
- **Retard en échec d'audit** : non (décision 1).
- **Inventaire automatique du disque** : plus tard (décision 4).

## 8. Décisions (prises le 2026-09-28 — voir section 11)

| # | Sujet | Retenu | Avis de Codex |
|---|---|---|---|
| 1 | Retard | avertissement dans `status` | avertissement |
| 2 | Ticket d'une copie du template | futures entrées TPL-D avec lignes `Folder scope:`, `Confirmation 1:`, `Confirmation 2:` ; anciennes intouchées | corriger le format |
| 3 | Copies conservées | `KEPT` sous décision, exclues du ménage | oui |
| 4 | Inventaire du disque | plus tard | plus tard |
| 5 | Copies présentes à l'adoption | au cas par cas : effacement par Jeoffrey ou `KEPT` sous décision | idem |
| 6 | Noms | `copy open / return / check / close / cleanup` ; `cleanup` prépare un script | garder |
| 7 | Papiers | rendus dans le dépôt ; tiroir d'archives hors dépôt ≠ preuve | dépôt par défaut |
| 8 | Copie déplacée | `copy move` sous le même ticket (5.6 bis) | — |

Commandes au total : six (décisions 6 et 8).

## 9. Plan

**Phase 0 — mesure, lecture seule, droit d'arrêter.** Déjà faite en partie par les deux relectures (lecteur HD réutilisable ; zéro `Folder scope` structuré dans les TPL-D ; fast-forward suivi d'un commit de retour démontré ; JSON sous `.git` ignorés par l'audit ; commits administratifs soumis au garde-fou). Reste :

- relever le contenu réel de `.git` dans un clone de l'atelier et dans une copie d'Alpha (lecture seule, sur accord), pour écrire la liste fermée complète de 5.5 ;
- mesurer le temps de l'inventaire complet (descente dans les ignorés comprise) sur une copie de la taille d'Alpha ;
- inventorier les dossiers présents sous `~/Projets` (lecture seule, sur accord).

Arrêt si : la liste fermée de `.git` ne peut pas être établie sans laisser de catégorie inconnue sur un clone ordinaire ; ou l'inventaire d'une copie ordinaire ne tient pas dans la limite d'un appel (3 minutes) de la VM du poste.

**Phase 1 — construction dans une copie**, sous double arrêt : les deux rôles (template et projet), registre, fiche de sortie, six commandes, `COPIES_RETURNED` avec la réparation groupée, bannière, doctrine (section « Copies » d'`AGENTS.core.md`, `project_control/README.md`, format structuré des TPL-D), manifeste, démo, CHANGELOG, roadmap. Essais de la section 10. Relecture du code par la seconde IA à la fin.

**Phase 2 — livraison** dans l'atelier (double arrêt séparé), promotion selon l'ordre de 5.7 — la première à l'appliquer.

**Phase 3 — plus tard**, chacun sous son double arrêt : montée d'Alpha, miroir public.

## 10. Essais

**Nouveaux (absents avant, verts après) :**

1. Frontière : cible égale, enfant, **parent**, chevauchement avec une autre copie, lien symbolique, volume absent → refus.
2. `copy open` : nom, usage, kind, sort hors liste ; date absente ; ticket inconnu, refusé, sans confirmations, `Folder scope` ne couvrant pas le chemin ; TPL-D sans lignes structurées ; `closes_with` déjà clos.
3. Retour d'un clone : refus avec un fichier non suivi, modifié non committé, ignoré (y compris un fichier au fond d'un dossier ignoré), un stash, une HEAD détachée non rendus ; accepté après rendu ou abandon nommé.
4. **`.git` (N1)** : hook inédit (`pre-push`) → refus tant que non rendu ou abandonné ; garde-fou installé identique à sa référence → aucun élément ; garde-fou installé **différent** → élément à rendre ; commit joignable seulement par le reflog (branche supprimée) → refus ; sous-module, worktree lié, rebase en cours, fichier inconnu dans `.git` → refus « non pris en charge ».
5. Retour d'un export : refus avec un fichier nouveau hors `source/` ou un écart de `source/` ; refus d'une revue sans mandat.
6. Fichier rendu : refus s'il est seulement suivi sans ces octets à HEAD.
7. `copy check` : refus après retravail dans la copie, après passage à `KEPT`, après remplacement du dossier, source illisible, fichier modifié au fond d'un dossier abandonné en bloc.
8. **Déplacement (N2)** : script généré pour A ; déplacement vers B et `copy move` ; A réoccupé par un autre dossier → le vieux script refuse, rien n'est effacé ; `copy move` refusé si le ticket ne couvre pas B, ou si une copie `RETURNED` a changé.
9. Nouveau retour : copie `RETURNED` retravaillée → `copy check` refuse ; nouveau `copy return` → nouvelle empreinte → `copy check` passe.
10. Ordre 5.7 : tag posé après le retour → audit PASS au tag ; vue régénérée après le tag → à jour.
11. **Réparation groupée (N3)** : deux copies `OPEN`, tag posé trop tôt → retour d'une seule refusé avec un message nommant l'autre ; retour groupé des deux (ou une rendue + une `KEPT` sous décision) en une transaction → audit PASS, garde-fou accepte ; FAIL d'une autre nature → refus.
12. `close WI-NNN` refusé avec une copie `OPEN`, accepté avec `RETURNED`.
13. `copy close ERASED` refusé si le dossier existe ou si l'identité est indisponible ; `KEPT` refusé sans décision ; `KEPT → RETURNED` sous décision.
14. Bannière d'un clone avec `.git/copie.json` au bon chemin ; bannière « déplacée » à un autre chemin ; aucune fiche → « ce dossier n'a pas de ticket ».
15. Garde-fou : branche de travail qui modifie le registre → refus ; en rôle template et en rôle projet.
16. Deux copies d'un même ticket : deux entrées, deux retours, clôture examinant les deux.

**Non-régression (verts avant et après) :**

17. Projet sans registre : audit PASS.
18. Projet dérivé qui monte vers cette version : audit PASS sans registre.
19. Worktrees jetables du contrôleur : inchangés.

## Annexe A — tickets manuels de ce chantier (jamais importés)

| Nom | Kind | Usage | Ticket | Sort | Retour |
|---|---|---|---|---|---|
| `squelette-revue-tableau-des-cles` | EXPORT | revue | double arrêt du 28 sept. 17:06 | rendre dans `provenance/maintenance/` de l'atelier, sous double arrêt séparé : fiches V1, V2, V3 ; mandats V1 et V2 ; relectures `…_V1`, `…_V1_V2`, `…_V2` ; les deux contre-revues ; `SOURCE-PROVENANCE.md` et `SOURCE-MANIFESTE.sha256`. Abandonner : `source/` (reconstructible à l'octet depuis le tag `v3.20.2`) et `runs/` avec `runs/v2/` (fixtures jetables). Puis effacer | avant la construction, ou à sa fin (décision de Jeoffrey) |
| `squelette-chantier-p21` | CLONE | chantier | double arrêt de la phase 1 | rendre (branche fetchée), puis effacer | à la promotion |

Le registre réel part vide : la première entrée sera la première copie ouverte après la promotion de cette version.

## 11. Décisions de Jeoffrey (2026-09-28, 18:05)

Réponse donnée dans la discussion du projet Claude « Squelette » : « d'accord avec les propositions ». Les huit propositions de la section 8 de la V2 sont retenues telles quelles :

| # | Décision |
|---|---|
| 1 | Le retard est un avertissement dans `status`, jamais un échec d'audit. |
| 2 | Les **futures** entrées TPL-D portent des lignes structurées `Folder scope:`, `Confirmation 1:`, `Confirmation 2:` ; les entrées existantes ne sont pas touchées. Tant qu'une TPL-D n'a pas ces lignes, `copy open` la refuse comme ticket. |
| 3 | Les copies conservées (`KEPT`) sont admises sous décision, visibles, exclues du ménage. |
| 4 | L'inventaire du disque (`copy scan`) vient plus tard, hors de ce chantier. |
| 5 | Les copies déjà présentes à l'adoption se traitent au cas par cas : effacement par Jeoffrey ou `KEPT` sous décision ; rien n'est reconstruit. |
| 6 | Commandes : `copy open`, `copy return`, `copy check`, `copy close`, `copy cleanup` ; `cleanup` prépare un script, il n'efface rien. |
| 7 | Les papiers d'une revue ou d'un chantier arrêté se rendent dans le dépôt (committés, vérifiés). Un tiroir d'archives hors dépôt n'est pas une preuve de retour. Conséquence : les papiers du chantier P20 rangés le 28 sept. dans `~/Projets/_archives/papiers-p20` ne comptent pas comme rendus ; les rapatrier dans l'atelier est une décision séparée, non prise. |
| 8 | Une copie déplacée se corrige par `copy move` sous le même ticket, avec la même frontière qu'à l'ouverture. |

Ces décisions n'autorisent aucune construction ni aucune écriture dans un dépôt : la construction attend le mot de Jeoffrey, puis son propre double arrêt.
