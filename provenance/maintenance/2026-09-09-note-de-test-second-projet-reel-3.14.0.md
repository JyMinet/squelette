> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Note de test — Squelette 3.14.0 sur un second projet réel

**Projet d'essai** : « Coût moyen crypto » — calculateur de prix de revient moyen pondéré à partir
d'un relevé d'opérations CSV.
**Chemin d'adoption testé** : projet **neuf**, né gouverné, jamais testé jusqu'ici (Alpha couvre
l'autre chemin, l'adoption par un dépôt existant).
**Machine** : conteneur Linux vierge, sans configuration préalable, sans réseau — la situation d'un
inconnu qui découvre le dépôt.
**Date** : 2026-09-09, de 22:28 à 22:48 UTC.

---

## Résumé en trois points

1. **Le cœur tient.** Toutes les promesses centrales du squelette ont été éprouvées et tenues :
   refus d'une écriture hors périmètre, refus de démarrer sans preuve de lecture, refus du commit
   d'initialisation sur la branche canonique, clôture qui exige des preuves. Rien n'est passé en force.
2. **L'accueil ne tient pas.** Un inconnu se heurte à **six formats que le contrôleur exige et
   qu'aucun document n'énonce**, tous pendant l'initialisation, avant son premier commit.
3. **Une preuve peut mentir sans être vue.** Un Work Item a été mené à `DONE` avec une preuve de
   tests qui affirme « tous passent » alors que son propre artefact, dont l'empreinte a été vérifiée,
   affiche `FAILED (failures=1)`.

---

## Chiffres

| | |
|---|---|
| Durée totale (machine) | 19 min 34 s |
| Dont initialisation | 6 min |
| Dont trois Work Items | 13 min |
| Code métier produit | 195 lignes |
| Tests métier produits | 211 lignes, 29 essais, tous verts |
| Commits | 24, dont **11 de gouvernance pure** (46 %) |
| Fichiers de gouvernance touchés | 64 |
| Suite d'essais du squelette | 3 min 30 s, 124 essais, **1 erreur**, 2 ignorés |

**Ratio d'adoption** : sur un projet de 200 lignes, la gouvernance a coûté à peu près autant que le
travail lui-même. C'est tenable, mais c'est la limite basse : sur un projet de 50 lignes, le squelette
coûterait plus cher que ce qu'il protège.

---

## Ce qui a été éprouvé et tenu

| Promesse | Épreuve | Résultat |
|---|---|---|
| Refus d'une écriture hors périmètre | fichier `applications/rapport/note.md` ajouté sous WI-001 | **refusé deux fois** : au preflight (`BUSINESS_CHANGE_AUTHORIZATION`, `AUTHORIZED_PATHS`) et au commit (`WORK_BRANCH_AUTHORIZED_PATHS`, `MODE_AUDIT`), en nommant le fichier |
| Preuve de lecture obligatoire | `start WI-001` sans empreinte | **refusé**, avec la commande à lancer |
| Protection de la branche canonique | commit d'initialisation sur `main` | **refusé** (`CANONICAL_BRANCH_PROTECTED`), franchi par mandat explicite imprimé dans le rapport |
| Preuves figées | seconde écriture sur un chemin de preuve déjà commité | **refusé** — l'immuabilité fonctionne |
| Atomicité des transitions | `create-work-item` | record, décision, conversation, roadmap, registre et classification Git **commités ensemble** |
| Langue et style au choix | `FR` + `PLAIN` | tenus partout dans la prose ; noms de vérifications en anglais, comme annoncé |
| Retrait de l'exemple autorisé | `examples/hello-squelette/` supprimé | audit et `template-upgrade` indifférents, comme promis — **mais voir C-5** |

---

## Constats

### C-1 — MAJEUR — Les modèles écrits dans les documents ne sont pas ce que le contrôleur accepte

Trois occurrences, toutes pendant l'initialisation, toutes bloquantes.

| Document | Ce que le modèle montre | Ce que le contrôleur exige | Message reçu |
|---|---|---|---|
| `docs/governance/HUMAN_DECISIONS.md`, § Modèle | `HD-NNN` en tête de bloc | un titre Markdown `## HD-001` (`scripts/project_control.py:690`) | `missing Human Decision HD-001` |
| `docs/governance/WORKTREE_REGISTRY.md`, § « Modèle **obligatoire** » | un bloc `text` sans balise | des balises HTML `<!-- PROJECT_CONTROL:WI-001 START -->` … `END` (`:2574`) | `missing registry entry: WI-001` |
| Charte, architecture, carte | `Status: DRAFT — PROJECT_OWNER_VALIDATION_REQUIRED` | exactement `` Status: `VALIDATED` `` (`:2832`) | `closeout requires a validated Project Charter` |

Gravité : le message de refus **affirme l'absence de ce qui est présent**. Un utilisateur qui vient
d'écrire sa décision et s'entend dire qu'elle n'existe pas conclut que l'outil est cassé, pas que son
format l'est. Aucun des trois messages ne dit quoi écrire.

Correctif proposé : que chaque modèle documenté soit exactement le texte accepté, et que le refus
cite le format attendu (« expected heading `## HD-001` »). Un essai qui vérifie que le bloc « Modèle »
de chaque document passe le parseur correspondant fermerait la famille entière.

### C-2 — MAJEUR — Le commit d'initialisation est refusé par le garde-fou que FIRST_START fait installer

`FIRST_START.md` § « Closeout explicite », point 4 : « committer cette transition explicitement ».
`FIRST_START.md` § « Utilisation quotidienne » : « installer la gate de commit ».
Les deux consignes se contredisent : la gate refuse (`CANONICAL_BRANCH_PROTECTED`, 7 chemins listés).

`PROJECT_CONTROL_HOOK_OVERRIDE` est la voie prévue, documentée dans `project_control/README.md` et
`AGENTS.core.md` — mais **`FIRST_START.md` ne la mentionne pas une seule fois** (0 occurrence), et
c'est le seul document qu'un projet neuf est invité à suivre.

C'est l'observation O-13 déjà connue, mais mesurée ici sur son vrai coût : c'est le **mur de sortie**
de l'initialisation. Un inconnu s'arrête là.

Correctif proposé : soit ajouter le mandat au point 4 de FIRST_START, soit — l'option déjà envisagée
dans la fiche P10 — que la gate reconnaisse la transition de clôture (`FIRST_START.md` +
`project-state.v1.json` + records du premier Work Item indexés ensemble, `bootstrap-closeout` PASS)
comme administrative.

### C-3 — MAJEUR — Une preuve peut affirmer le contraire de son artefact

**Scénario démontré.** Sous WI-003 :

1. un test est cassé volontairement, la suite est lancée, sa sortie rouge est capturée dans
   `reports/evidence/WI-003/sortie-tests.txt` (`FAILED (failures=1)`) ;
2. le code est restauré — le livrable n'a jamais été cassé, seul l'artefact l'est ;
3. `tests.json` déclare `"result": "PASS"`, `"level": "TESTED"`, résumé « 29 tests unittest […]
   Tous passent », artefact = la sortie rouge, empreinte SHA-256 exacte ;
4. `close WI-003 --test-evidence …` → **`PASS: TRANSACTION — Work Item DONE`**.

Le contrôleur a vérifié la structure de la preuve, l'existence de l'artefact, son empreinte, le
commit métier, l'intégration de la branche et la fraîcheur de la lecture des autorités. Il n'a jamais
regardé **ce que l'artefact dit**.

Nuance de justice : le squelette ne peut pas lancer les tests d'un projet dont il ignore la commande.
Mais il peut détecter la contradiction **interne** à sa propre preuve. C'est la même famille que F-12
(« toutes réussies » sans avoir lancé les tests), traitée en 3.11.0 pour la vue roadmap et laissée
ouverte pour les preuves de clôture.

Correctif proposé, bon marché : quand `result` vaut `PASS`, refuser si un artefact texte contient un
marqueur d'échec (`FAILED`, `failures=`, `ERROR:`, `Traceback`, `exit 1`). Ça n'attrape pas un menteur
déterminé, mais ça attrape l'agent qui copie une sortie sans la lire — le cas réel.
Complément possible : un champ `command` dans la preuve, et l'exigence que l'artefact soit la sortie
de cette commande.

La trace de l'épreuve est conservée dans le dépôt : `reports/evidence/WI-003/LISEZ-MOI.md`.

### C-4 — MINEUR — Le format des preuves s'apprend en brûlant des chemins

Trois tentatives ont été nécessaires pour clore WI-001 :

| Tentative | Refus | Documenté ? |
|---|---|---|
| 1 | `recorded_at must be a past timestamp with timezone` | non — le schéma dit `{"type": "string"}` |
| 2 | `evidence path must be inside reports/evidence/WI-001/` | non |
| 3 | acceptée | |

Et comme une preuve est immuable dès son premier commit (C-1 des bonnes surprises), chaque échec
condamne le nom du fichier : la clôture s'est faite sur `tests-3.json` et `integration-3.json`.
C'est exactement l'`integration-2.json` d'Alpha — ce n'était pas un accident d'Alpha, c'est le
comportement normal.

Correctif proposé : que le schéma porte `"format": "date-time"` et un exemple complet, et que le
message de refus donne la forme attendue. Éventuellement, laisser réécrire une preuve tant qu'elle
n'a jamais été acceptée par un `close`.

### C-5 — MINEUR — Faire ce que le document autorise casse la suite d'essais

`ADOPTION.md` : « Un projet dérivé peut le retirer de sa copie ; ce n'est pas un fichier core ».
Le dossier `examples/hello-squelette/` a donc été retiré, comme permis.

`tests/test_template.py::test_the_demo_states_the_exact_reach_of_the_proof_of_reading` lit
`examples/hello-squelette/demo.py` sans condition → `FileNotFoundError`. 124 essais, 1 erreur.

C'est un essai ajouté en 3.11.0 pour fermer F-18. **Ce constat est probablement déjà clos par la
3.14.1** (`skip_unless_template()`), à confirmer sur le tag promu — je testais la 3.14.0.

### C-6 — MINEUR — `ADOPTION.md` ne sert pas au cas qu'il devrait servir

Première phrase du document : il ne couvre que l'adoption par un projet **déjà gouverné**, et un
dépôt jamais gouverné « ne dispose pas encore d'une procédure d'import ». La vraie procédure pour un
projet neuf est dans le README, dans une phrase noyée au milieu de la section « Try it » :
exporter l'arbre suivi sans `.git`, créer une baseline, donner `FIRST_START.md` à l'agent.

Un inconnu ouvre le fichier qui s'appelle « ADOPTION ». Il y lit que ça ne le concerne pas, et rien
ne lui dit où aller.

### C-7 — COSMÉTIQUE — Deux petites choses vues au passage

- **Vue roadmap « périmée » sur un dépôt qui vient de naître** (avant toute initialisation).
  C'est l'observation O-13, toujours présente en 3.14.0. Le mot juste serait « absente ».
- **`idea add` affiche `WORK_ITEM_ID: ID-001`** pour une idée. Une idée n'est pas un Work Item ;
  l'étiquette du champ est empruntée.

---

## Ce qui a très bien marché

- **`create-work-item` est excellent.** Une commande, et le record, la décision humaine, la
  conversation, la roadmap humaine, la roadmap machine, le registre des branches et la classification
  Git sont écrits et commités ensemble. WI-002 et WI-003 ont pris **4 minutes chacun**, contre
  6 minutes pour la seule initialisation de WI-001 écrite à la main.

  **C'est le vrai enseignement du test** : la douleur n'est pas dans le squelette, elle est
  exactement là où le squelette n'outille pas — l'amorçage. Tout ce que C-1, C-2 et C-4 décrivent
  disparaîtrait avec une commande `bootstrap-*` qui écrirait la première décision, le premier record
  et la première entrée de registre comme `create-work-item` le fait ensuite.

- **Les refus sont précis.** Ils nomment le fichier fautif, la vérification, la ligne. Quand le
  format est connu, le squelette est un plaisir à utiliser.

- **Le français et le style simple sont tenus** de bout en bout, sans une phrase anglaise dans la
  prose adressée au propriétaire.

---

## Réponse à la question posée

**Le squelette est-il fiable ?** Sur ce qu'il contrôle, oui : il n'a rien laissé passer de ce qu'il
sait détecter. La seule brèche démontrée est C-3, et elle est structurelle — il vérifie la forme des
preuves, jamais leur véracité.

**Un projet neuf peut-il l'adopter ?** Aujourd'hui, seulement avec quelqu'un qui connaît déjà le
squelette. Six formats non écrits et un mur documenté ailleurs séparent un inconnu de son premier
commit. Aucun n'est grave. Ensemble, ils sont le motif d'abandon.

**Est-il prêt pour la publication publique ?** La mécanique, oui. L'accueil, pas encore : C-1 et C-2
sont ce que rencontrera le premier visiteur du dépôt, dans les vingt premières minutes, et il n'aura
personne à qui demander.

---

## Ce qui existe maintenant

Un projet réel, complet, gouverné de bout en bout, qui calcule ce qu'il annonce :

```
$ python3 -B -m modules.portefeuille.rapport releve.csv
Prix de revient moyen par actif

BTC
  quantité restante   : 0.45
  prix de revient     : 42666.67 €
  coût total engagé   : 19200.00 €
  quantité vendue     : 0.3
  frais cumulés       : 37.30 €

ETH
  quantité restante   : 6
  prix de revient     : 2666.67 €
  coût total engagé   : 16000.00 €
  frais cumulés       : 13.60 €

Ce rapport est un calcul de prix de revient moyen pondéré, en euros, frais comptés à part.
Ce n'est pas un calcul fiscal et il ne vaut pas déclaration.
```

3 Work Items `DONE`, 4 décisions humaines, 29 essais verts, audit `PASS`, projet au repos.
