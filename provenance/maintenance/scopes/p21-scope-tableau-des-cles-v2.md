> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Fiche de cadrage — « Tableau des clés » — V2

Copies de dépôt : ouverture, retour, effacement.

| | |
|---|---|
| Squelette de référence | 3.20.2 (atelier `~/Projets/squelette-atelier`, tag `v3.20.2`) |
| Version de la fiche | V2 — 2026-09-28 ; remplace la V1 (conservée) après la relecture `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V1_V2.md` (verdict `…_REQUIRES_MAJOR_REDLINE`) et sa contre-revue (`…_REVIEW_OF_RELECTURE_V2_PASS`) |
| État | DÉCISIONS PRISES (section 11, 2026-09-28 18:05) — relecture courte des corrections par Codex avant construction |
| Chantier | P21 si P20 reste le paquet ; ordre entre les deux à décider par Jeoffrey |
| Version visée | la suivante après 3.20.2 |
| Écritures | aucune : cette fiche est un texte |

## Résumé en trois points (pour le Project Owner)

1. **Ce qui s'est passé.** La relecture a trouvé sept trous dans la V1. Le plus grave : un dossier qui contient l'original pouvait être déclaré comme « copie » et partir à l'effacement avec lui. Les autres : le travail non enregistré dans la copie échappait au contrôle, une vieille preuve pouvait autoriser un effacement même si on avait retravaillé dedans entre-temps, et l'ordre « rendre les clés / promouvoir » se contredisait.
2. **Ce que ça change.** La V2 bouche les sept trous. La copie et l'original ne peuvent plus se chevaucher ; rendre les clés veut dire « tout ce qui est dans la copie est soit revenu, soit abandonné par son nom » ; au moment d'effacer, on relit la copie telle qu'elle est ce jour-là ; le tag de version se pose en dernier, une fois les clés rendues.
3. **Ce qu'il doit faire.** Répondre aux huit questions de la section 8 (les avis de Codex sont notés à côté), puis dire si la V2 repasse chez Codex pour une relecture courte.

## 0. Ce qui change depuis la V1

| Constat | Correction dans la V2 | Où |
|---|---|---|
| R01 — cible parente de l'original | Disjonction dans les deux sens, sur chemins résolus, avec l'original et avec toute copie non effacée ; revérifiée au moment d'effacer | 5.3, 5.8 |
| R02 — contenu hors branches | Le retour porte sur **tout** le contenu de la copie, pour tous les usages : chaque différence est rendue ou abandonnée par son nom | 5.5 |
| R03 — preuve ancienne | Empreinte du contenu enregistrée au retour ; `copy check` relit l'état courant du registre et la copie courante juste avant l'effacement | 5.5, 5.8 |
| R04 — export d'un tag | Une « fiche de sortie » posée dans la copie au moment de la copie (dans `.git/` pour un clone, à la racine du contenant pour une revue) ; le registre de l'original reste la seule autorité | 4.5, 5.4 |
| R05 — ordre de clôture | Un seul ordre : rapatrier, intégrer, rendre, **puis** poser le tag ; `copy return` peut réparer une incohérence de clés sans lever les autres refus | 5.7 |
| R06 — nom de l'annexe | Les deux copies de l'annexe restent des tickets manuels, jamais importés ; le registre part vide | 5.9, annexe A |
| R07 — coût | Coût décrit par acteur | 5.10 |
| D-O1 | Deux rôles, template et projet dérivé, traités séparément | 5.1, 9 |
| D-O5 | « Physiquement » retiré : une copie ne retire aucun accès à l'original | 7 |

## 1. Constat

Inchangé depuis la V1 (inventaire de mémoire à confirmer en phase 0). Une douzaine de dossiers en trois semaines, six mots pour trois usages, deux ménages à la main, un mandat sauvé de justesse le 15 sept., l'établi du chantier P20 effacé le 28 sept. après sauvegarde de ses papiers hors de tout dépôt, sans trace vérifiable. Aucun endroit du dépôt ne dit quelles copies existent, pourquoi, ni ce qu'on en fera.

## 2. Les trois façons dont ça casse

- **S1 — Le parking.** Travail rapatrié, dossier resté.
- **S2 — Le second original.** Le travail continue dans la copie, ou n'en revient jamais.
- **S3 — La perte à l'effacement.** Un document né dans la copie part avec elle.
- **S4 — L'effacement de trop** (ajouté par la relecture). L'effacement d'une « copie » emporte l'original, une autre copie ou un travail repris depuis. C'est la faute la plus grave possible : la mécanique existe pour éviter S1–S3, elle ne doit jamais créer S4.

Hors périmètre : S0, la dérive inverse (écrire dans l'original), couverte par le double arrêt.

## 3. But et non-buts

**But.** Toute copie **déclarée** d'un dépôt gouverné a un ticket, un sort prévu, une date de retour, une preuve de retour vérifiée, et une fin enregistrée ; aucun effacement proposé par l'outil ne peut toucher l'original, une autre copie, ni du travail non rendu.

**Non-buts.** L'outil ne crée ni n'efface jamais un dossier (le contrôleur continue de retirer ses propres worktrees jetables, régime séparé, inchangé). Pas de surveillance du disque. Les clones de la VM de session ne sont pas suivis. Le double arrêt et la politique des branches ne changent pas. Aucun nouveau document d'autorité routé.

## 4. Principes

1. **Une copie = un ticket.** Pas de copie sans décision humaine qui la nomme. Un ticket peut couvrir plusieurs copies ; chacune a son entrée.
2. **Le tableau des clés vit dans l'original.** Le registre de l'original est la seule autorité sur l'état d'une copie.
3. **Une copie n'est jamais un second original.** Pas de version, pas de tag, pas de lien GitHub ni NAS. Une copie n'empêche pas d'écrire dans l'original : elle protège par séparation, pas par interdiction ; les droits d'accès restent ceux du mandat.
4. **Rendre les clés avant de fermer.** Aucun Work Item clos, aucun tag de version posé tant qu'une copie rattachée est `OPEN`. Rendre se prouve, pour tout le contenu de la copie.
5. **Le ticket avant la voiture, la fiche de sortie avec la voiture.** L'ouverture s'enregistre dans l'original avant la copie ; le geste de copie, déjà autorisé par le double arrêt, dépose dans la copie une fiche de sortie qui la désigne.
6. **Jamais d'effacement sur une preuve ancienne.** Juste avant d'effacer, on relit le registre courant et la copie telle qu'elle est.

## 5. Mécanique proposée

### 5.1 Le registre

- Projet dérivé : `project_control/copies-state.v1.json`, record administratif canonique, committé par le contrôleur (règle 3.2.0). Template : `provenance/copies-state.v1.json`, avec le traitement propre au rôle template (branche de référence `main`, comme la vue roadmap du template aujourd'hui) — à écrire explicitement, sans initialiser le template comme un projet.
- Les deux chemins entrent dans la classification des chemins administratifs (ils n'y sont pas en 3.20.2) ; le garde-fou refuse une branche de travail qui **modifie** le registre (la simple présence héritée de la canonique reste admise, comme aujourd'hui).
- Registre absent = registre vide. Il n'entre pas dans les fichiers obligatoires, n'est pas routé, n'entre pas dans la preuve de lecture. Il entre dans les sources qui rendent la vue roadmap périmée.

Une entrée :

```
id             COPY-NNN
name           nom du dossier (5.2)
path           chemin absolu résolu déclaré
kind           CLONE (dépôt Git copié de l'original) | EXPORT (contenant de revue avec source/ exporté d'un tag)
usage          chantier | revue | repetition
ticket         HD-NNN (projet) ou TPL-D-NNN (template)
closes_with    WI-NNN | version X.Y.Z  (typé ; jamais une décision)
origin         original_path (résolu), commit ou tag copié, root_commit
fate           RETURN_THEN_ERASE | ERASE | KEEP
due            date de retour prévue
opened_at      date
state          OPEN | RETURNED | ERASED | KEPT
returns        preuves : {kind: commit|file|abandon, ref, sha256, role?, reason?, verified_at}
content_digest empreinte du contenu de la copie au moment du retour (5.5)
identity       device + inode du dossier au moment du retour
closed_at      date ; closing_decision pour KEPT
```

États : `OPEN → RETURNED → ERASED | KEPT` ; `KEPT → RETURNED` possible sous décision (une copie gardée qu'on veut finalement effacer repasse par un retour complet). Terminal : `ERASED`.

### 5.2 Le nom

`<dépôt>-<usage>-<référence>`, usage ∈ `chantier | revue | repetition`, référence = numéro de chantier, version ou identifiant de ticket, suffixe `-2`, `-3` pour plusieurs copies d'un même ticket. La date n'entre pas dans le nom.

### 5.3 L'ouverture — `copy open`

Lancée dans l'original, depuis la canonique. Arguments : `--path`, `--kind`, `--usage`, `--ticket`, `--closes-with`, `--fate`, `--due`.

Refus mécaniques :

- **frontière (R01)** : sur chemins résolus (`realpath`, liens suivis), refus si la cible est égale à l'original, contenue dans l'original, **contient l'original**, ou chevauche dans un sens ou dans l'autre une copie non `ERASED` ; refus si un composant du chemin est un lien symbolique ; refus si le chemin est sur un volume non monté ou illisible ;
- ticket inconnu, ou HD dont `Folder scope:` ne couvre pas le chemin (comparaison de chemins résolus : égal ou contenu dans le dossier accordé, jamais une sous-chaîne) ; HD refusée ou sans les deux confirmations → refus (réutilisation de la validation du double arrêt existante) ;
- pour un TPL-D : voir question 2 ;
- `closes_with` déjà clos (Work Item `DONE`, version déjà taguée) ou inconnu ;
- sort, usage ou kind hors liste, date absente, nom hors règle.

Le chemin peut ne pas encore exister.

### 5.4 La fiche de sortie

Le geste de copie, autorisé par le double arrêt, dépose une fiche de sortie `copie.json` (id, original, ticket, sort, date de retour, date d'émission) :

- `CLONE` : dans `.git/copie.json` — hors de l'arbre suivi, ne salit rien, ne part pas dans un commit ;
- `EXPORT` : à la racine du contenant de revue, à côté de `source/` (l'export reste intact ; aucun tag n'est touché).

`status` lancé dans un clone qui porte `.git/copie.json` commence par « COPIE de <original> — ticket … — retour attendu le … (d'après la fiche de sortie du <date>) ». Un export n'a pas de `status` (pas de Git) : la fiche de sortie s'y lit comme un document, et le mandat de revue la cite. La fiche de sortie est un pointeur, pas une autorité : l'état réel est dans le registre de l'original.

### 5.5 Le retour — `copy return`

Lancée dans l'original, lecture seule sur la copie. Le retour porte sur **tout le contenu** de la copie, quel que soit l'usage :

1. **L'inventaire.** L'outil dresse la liste de tout ce que la copie a de différent de son origine :
   - `CLONE` : références (branches, tags, HEAD détachée), stash, fichiers modifiés indexés ou non, fichiers non suivis **et ignorés** (`git status --porcelain=v2 --ignored`), hors `.git/copie.json` ;
   - `EXPORT` : fichiers du contenant hors `source/`, plus tout écart de `source/` à son manifeste d'export.
2. **Le rendu.** Chaque élément de l'inventaire doit être couvert par une preuve :
   - commit ou référence : atteignable depuis une référence de l'original (`merge-base --is-ancestor`) ;
   - fichier : `--file <chemin dans l'original> --sha256 <…> [--role mandat|livrable|rapport|note]` ; le fichier doit être committé dans l'original avec ces octets à HEAD (pas seulement suivi) ;
   - abandon : `--abandon <élément> --reason "<…>"` ; un dossier jetable déclaré (le `runs/` d'une revue) s'abandonne en bloc avec sa raison.
3. **Les refus.** Élément non couvert ; revue sans pièce de rôle `mandat` ; dépôt ou objet illisible (jamais « rendu par omission »).
4. **L'empreinte.** L'outil enregistre l'empreinte de l'inventaire complet (`content_digest`) et l'identité du dossier (`identity`). C'est ce que `copy check` comparera avant l'effacement.

Un chantier arrêté avant livraison suit la même règle : ses branches sont abandonnées par leur nom, ses papiers uniques rendus comme fichiers.

### 5.6 La fin — `copy close`

`--state ERASED` : refusé si le chemin existe encore. Un chemin absent ne suffit pas si l'identité ne peut être tranchée (volume démonté) : refus « indisponible, pas effacé ». `--state KEPT` : exige `--decision` ; la copie reste visible, exclue de tout nettoyage ; la garder n'autorise pas à y reprendre le travail.

### 5.7 L'ordre de clôture (R05)

**Un seul ordre, pour toute copie rattachée à une version du template :**

1. rapatrier la branche de la copie dans l'original (fetch) et vérifier ;
2. enregistrer la décision de promotion sur la branche (comme aujourd'hui) puis fast-forward de `main` (intégration, sous le mandat de promotion) ;
3. `copy return` sur `main` (commit administratif) ;
4. régénérer la vue ;
5. **poser le tag** sur cet état : la version figée contient des clés rendues.

Pour un Work Item d'un projet dérivé : rapatrier, intégrer, `copy return` sur la canonique, puis `close`. `close WI-NNN` refuse tant qu'une copie `closes_with = WI-NNN` est `OPEN`.

`COPIES_RETURNED` (audit) : FAIL si une copie `OPEN` a sa cible close. Réparation : `copy return` est admis quand les seuls FAIL d'audit sont des `COPIES_RETURNED` portant sur l'entrée rendue ; tout autre FAIL continue de refuser. Si un tag a été posé par erreur avant le retour, le commit tagué garde son registre `OPEN` : il est signalé par `status` comme incohérence historique connue, jamais réécrit, et l'audit courant redevient PASS après le retour.

`status` : « Copies : n ouvertes (dont k en retard) · m à effacer · p conservées ». Le retard est un avertissement, jamais un FAIL (question 1).

### 5.8 L'effacement — `copy check` et `copy cleanup`

- `copy check COPY-NNN` (lecture seule, lancée dans l'original) : relit le registre **courant** (l'entrée doit être `RETURNED` avec sort d'effacement), refait la frontière de 5.3 sur le chemin résolu, compare l'identité du dossier et recalcule l'inventaire de la copie : son empreinte doit être celle du retour. Tout écart — contenu nouveau, sort changé en `KEPT`, dossier remplacé, source illisible — refuse.
- `copy cleanup` écrit un script bash (`set -euo pipefail`, textes complets) qui, pour chaque copie, lance `copy check` **juste avant** l'effacement, s'arrête au premier refus, efface ce seul dossier, puis affiche la commande `copy close --state ERASED`. Jeoffrey lance le script.
- Limite déclarée : entre le contrôle et l'effacement, il reste une fenêtre de quelques instants ; le script ne tourne pas pendant qu'un agent travaille dans la copie (condition écrite en tête du script).

### 5.9 Adoption, et copies d'avant la règle

Registre absent = vide ; audit PASS par construction ; aucune copie antérieure reconstruite. Une copie existante que Jeoffrey veut garder s'enregistre `KEPT` sous décision, comme constat présent, sans retour historique inventé. Les copies de l'annexe A ne sont pas importées.

### 5.10 Coût (R07)

- **Pour l'agent au démarrage** : aucun nouveau document d'autorité routé ; la doctrine ajoutée au core (une section « Copies ») allonge le texte déjà lu ; chaque ticket est une décision humaine de plus dans le carnet (comme aujourd'hui avec le double arrêt).
- **Automatique** : `status` et l'audit lisent le registre.
- **Par copie** : `copy open` (sept arguments), `copy return` (une preuve par élément de l'inventaire — souvent quelques-unes, un abandon en bloc pour un dossier jetable), `copy close`.
- **Pour Jeoffrey** : lancer le script de ménage (groupable), puis `copy close`.

## 6. Limites assumées

- Une copie jamais déclarée est invisible.
- L'outil ne peut pas empêcher un envoi depuis une copie qui aurait gardé ses liens ; le retour révèle ce qui n'est pas revenu, pas ce qui est parti.
- Une copie déplacée perd sa bannière ; elle n'est jamais déclarée `ERASED` pour autant (identité, 5.6). Correction : `copy move COPY-NNN --path <nouveau>` sous le même ticket (même frontière) — ou question laissée ouverte, voir question 8.
- Un volume démonté rend la copie « indisponible », pas « effacée ».
- La fenêtre entre `copy check` et l'effacement (5.8).
- Un tag posé avant le retour, par erreur, reste incohérent à jamais dans l'histoire (5.7).

## 7. Options écartées

- **Branches seules** : elles ne séparent pas les dossiers (S0). Une copie sépare, elle n'interdit pas : la sécurité vient du mandat et du double arrêt.
- **Worktrees Git** : partagent objets, configuration et remotes ; incompatibles avec « sans liens ». Les worktrees jetables internes du contrôleur restent inchangés.
- **Fichier marqueur dans l'arbre suivi** : écarté ; la fiche de sortie vit dans `.git/` (clone) ou dans le contenant (export) — c'est le correctif de R04.
- **Jumeau Markdown** du registre : pas maintenant.
- **Effacement par l'outil** : non ; le script, lancé par Jeoffrey, fait lui-même le dernier contrôle.
- **Retard en échec d'audit** : non.
- **Inventaire automatique du disque** : plus tard (question 4).

## 8. Décisions à prendre par Jeoffrey

| # | Question | Proposé | Avis de Codex |
|---|---|---|---|
| 1 | Retard : avertissement ou échec d'audit ? | avertissement | avertissement |
| 2 | Ticket d'une copie du template (TPL-D, écrit en prose, aucun champ `Folder scope` lisible) | structurer les **futures** entrées TPL-D (lignes `Folder scope:`, `Confirmation 1:`, `Confirmation 2:`), sans toucher aux anciennes | corriger le format |
| 3 | Copies conservées (`KEPT`) | oui, sous décision, exclues du ménage | oui |
| 4 | Inventaire du disque (`copy scan`) | plus tard | plus tard |
| 5 | Copies déjà présentes au moment de l'adoption | au cas par cas : effacer (ton geste) ou `KEPT` sous décision | idem |
| 6 | Noms des commandes | `copy open / return / check / close / cleanup` | garder, préciser que `cleanup` prépare un script |
| 7 | Papiers d'une revue ou d'un chantier arrêté | dans le dépôt (committés, vérifiés) ; le tiroir d'archives hors dépôt n'est pas une preuve de retour | dépôt par défaut |
| 8 | Copie déplacée | `copy move` sous le même ticket | (non posée à Codex) |

## 9. Plan

**Phase 0 — mesure, lecture seule.** Déjà largement faite par la relecture (lecteur HD réutilisable ; zéro `Folder scope` structuré dans les TPL-D ; fast-forward suivi d'un commit de retour démontré). Reste : l'inventaire réel des dossiers sous `~/Projets` (lecture seule, sur accord) et la mesure du coût de l'inventaire `git status --ignored` sur un clone de la taille d'Alpha.

**Phase 1 — construction dans une copie**, sous double arrêt : les deux rôles (template et projet), registre, fiche de sortie, cinq commandes, `COPIES_RETURNED` avec sa réparation limitée, bannière, doctrine, manifeste, démo, CHANGELOG, roadmap.

**Phase 2 — livraison** dans l'atelier (double arrêt séparé), promotion selon l'ordre de 5.7 — la première à l'appliquer.

**Phase 3 — plus tard**, chacun sous son double arrêt : montée d'Alpha, miroir public.

## 10. Essais

**Nouveaux (absents avant, verts après) :**

1. Frontière : cible égale, enfant, **parent**, chevauchement avec une autre copie, lien symbolique, volume absent → refus.
2. `copy open` : nom, usage, kind, sort hors liste ; date absente ; ticket inconnu, refusé, sans confirmations, `Folder scope` ne couvrant pas le chemin ; `closes_with` déjà clos.
3. Retour d'un clone : refus avec un fichier non suivi, un fichier modifié non committé, un fichier ignoré, un stash, une HEAD détachée non rendus ; accepté après rendu ou abandon nommé.
4. Retour d'un export : refus avec un fichier nouveau hors `source/` ou un écart de `source/` ; refus d'une revue sans mandat.
5. Fichier rendu : refus s'il est seulement suivi sans ces octets à HEAD.
6. `copy check` : refus après retravail dans la copie, après passage à `KEPT`, après remplacement du dossier, source illisible.
7. Ordre 5.7 : tag posé après le retour → audit PASS au tag ; tag posé avant → `COPIES_RETURNED` FAIL, `copy return` réparateur admis, autre FAIL toujours refusé.
8. `close WI-NNN` refusé avec une copie `OPEN`, accepté avec `RETURNED`.
9. `copy close ERASED` refusé si le dossier existe ou si l'identité est indisponible ; `KEPT` refusé sans décision ; `KEPT → RETURNED` sous décision.
10. Bannière d'un clone avec `.git/copie.json` ; aucune fiche → « ce dossier n'a pas de ticket ».
11. Garde-fou : branche de travail qui modifie le registre → refus ; en rôle template et en rôle projet.
12. Deux copies d'un même ticket : deux entrées, deux retours, clôture examinant les deux.

**Non-régression (verts avant et après) :**

13. Projet sans registre : audit PASS.
14. Projet dérivé qui monte vers cette version : audit PASS sans registre.
15. Worktrees jetables du contrôleur : inchangés.

## Annexe A — tickets manuels de ce chantier (jamais importés)

| Nom | Kind | Usage | Ticket | Sort | Retour |
|---|---|---|---|---|---|
| `squelette-revue-tableau-des-cles` | EXPORT | revue | double arrêt du 28 sept. 17:06 | rendre (V1, V2 de la relecture, mandat, fiche V1, contre-revue, rapportés dans `provenance/maintenance/` de l'atelier sous double arrêt séparé ; `runs/` abandonné comme jetable), puis effacer | à la décision de construire |
| `squelette-chantier-p21` | CLONE | chantier | double arrêt de la phase 1 | rendre (branche fetchée), puis effacer | à la promotion |

Le registre réel part vide : la première entrée sera la première copie ouverte après la promotion de cette version.

## 11. Décisions de Jeoffrey (2026-09-28, 18:05)

Réponse donnée dans la discussion du projet Claude « Squelette » : « d'accord avec les propositions ». Les huit propositions de la section 8 sont retenues telles quelles :

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

Ces décisions n'autorisent aucune construction ni aucune écriture dans un dépôt : la construction attend la relecture courte, puis son propre double arrêt.
