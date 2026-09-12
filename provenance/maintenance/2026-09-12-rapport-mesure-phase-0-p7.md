> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# D1 — Rapport de mesure de phase 0

**Chantier** : P7 étape 1 — « La question de l'existant »
**Mandat** : `mandat-construction-p7-etape-1.md` (12 septembre 2026)
**Date** : 2026-09-12
**Posture** : mesure en lecture seule. **Aucune écriture, aucune construction.**

---

## Résumé en trois points

1. **Pas de serpent qui se mord la queue.** Le record du chantier n'entre pas dans l'empreinte de lecture des autorités : écrire la réponse dans le record après le calcul de l'empreinte ne la périme pas. Le premier blocage du § 3 **n'est pas déclenché**.
2. **Il manque une frontière.** Aucune baseline déclarée ne date l'adoption d'une *version* par un projet. Le chemin de régression « le chantier ancien qui reprend » n'est pas couvert. Le second blocage du § 3 **est déclenché**.
3. **Arrêt, décision de conception requise.** Trois options sont soumises au Project Owner au § D. La session ne choisit pas.

---

## A. Préflight — état exact de l'objet mesuré

| | |
|---|---|
| Dossier original (jamais écrit, jamais exécuté) | `~/Projets/Squelette V3 -runtime-proof` |
| Copie jetable mesurée | clone `--no-hardlinks` dans l'espace de session, hors de tout dossier de l'utilisateur |
| Branche | `main` |
| HEAD | `ebf62f4f46da2a1c5f02f57abd997482033148d2` |
| Dernier tag | `v3.19.1` |
| Arbre de travail de l'original | propre (aucune modification en attente) |
| `scripts/project_control.py` | 6 514 lignes — SHA-256 `3d3e76de08d347467a8843930ac53066f74f37baa783384fbd1c6f10e4d349f0` |
| `project_control/schemas/work-item.v1.schema.json` | SHA-256 `52423cacc127ccb60bb8ffd638172033d9b4251b6be08f587f4f0e685f09afd0` |
| Suite d'essais dans la copie | **164 essais, tous verts** (110,8 s) |

Toutes les références de ligne ci-dessous portent sur `scripts/project_control.py` à ce HEAD.

---

## B. Les sept mesures du § 3

### B.1 — Le record du chantier entre-t-il dans l'empreinte de lecture des autorités ? → **NON**

`authority_manifest()` (l. 3435-3458) ne construit l'empreinte qu'à partir des documents **routés** par
`docs/agent-governance/mandatory-documents.v1.json` (clé `base`, plus les `scopes` déduits des
`authorized_paths` par `scopes_for_paths()`, l. 232), moins les 9 chemins de `MANIFEST_EXCLUDED_PATHS`
(l. 93-102). `project_control/work-items/` n'apparaît **nulle part** dans le routage.

Mesure sur trois formes d'autorisation typiques :

| `authorized_paths` | scopes | documents dans l'empreinte | record du chantier dedans ? |
|---|---|---|---|
| `scripts/`, `project_control/` | development, runtime | 22 | **NON** |
| `docs/governance/` | governance | 12 | **NON** |
| `applications/` | development | 12 | **NON** |

**Conséquence** : remplir `prior_art` dans le record après `context-manifest` ne périme pas l'empreinte.
Le démarrage ne tourne pas en rond. **Blocage 1 du § 3 : non déclenché.**

*Effet de bord mesuré, sans conséquence* : `project_control/schemas/work-item.v1.schema.json` **est** routé
(scope `development`). Modifier le schéma change donc l'empreinte des chantiers de ce scope — une fois, au
moment de la montée de version. C'est le comportement normal d'une autorité qui change, pas une circularité.

### B.2 — Où vit le record, quel schéma le décrit

| | |
|---|---|
| Emplacement | `project_control/work-items/<WI-NNN>.json` |
| Schéma | `project_control/schemas/work-item.v1.schema.json` |
| Forme | `additionalProperties: false` ; 30 champs `required` ; 32 propriétés (les deux en trop : `close_head`, `block_records`) |
| Validation de forme | validateur interne `schema_record_errors()` (l. 1236), sous-ensemble de JSON Schema |
| Règles supplémentaires | `validate_work_item()` (l. 1388) |
| Remontée à l'audit | contrôle `SCHEMA_VALIDATION` (l. 2090), alimenté par `project_control_errors()` (l. 2984) |
| Création | `create-work-item` (parseur l. 6189-6226) — tous les champs passent par des options de ligne de commande, plusieurs `required=True` |

### B.3 — Baseline d'adoption existante, et couverture des deux chemins de régression

**Ce qui existe.** Deux baselines déclarées, et deux seulement (`BASELINE_DECISION_FIELDS`, l. 37-40) :

| Baseline | Ce qu'elle date | Déclaration |
|---|---|---|
| `legacy_baseline` (l. 5565) | le commit où **le projet a adopté le squelette** | `{head, human_decision_ref}` dans `project_control/project-state.v1.json`, la décision devant porter `Legacy baseline commit: <sha>` exactement une fois |
| `authorities_baseline` (l. 5633) | le commit où **le projet a adopté la preuve de lecture** (squelette 3.6+) | idem, champ `Authorities baseline commit:` |

Mécaniques attachées : `legacy_records()` (l. 5709) lit les records exactement tels qu'ils étaient commis
à la baseline ; `frozen_decision_refs()` (l. 5590) n'exempte que les décisions dont le bloc n'a pas changé
depuis. Depuis la 3.18.0, une baseline ne recule jamais et ne se retire que sur décision.

**Chemin 2 — l'audit qui valide les anciens records contre un schéma commun → couvert, sans aucune baseline.**
Mesuré en rejouant le validateur sur un record ancien :

| Situation | Résultat mesuré |
|---|---|
| record portant `prior_art`, schéma **actuel** | `work-item: unexpected property prior_art` → le schéma **doit** être étendu |
| record ancien (sans `prior_art`), `prior_art` **optionnel** dans le schéma | aucune erreur |
| record ancien, `prior_art` **ajouté aux `required`** | `work-item: missing prior_art` → **tous** les anciens records tombent |

Donc : le champ entre dans `properties` et **jamais** dans `required`. La frontière ne vit pas dans le schéma.

**Chemin 1 — le chantier ancien qui reprend → NON couvert.**
Le § 2.5 fixe l'éligibilité aux « chantiers ouverts **après l'adoption de la version** ». Or aucune des deux
baselines ne date l'adoption d'une version : l'une date l'adoption du squelette, l'autre celle de la preuve
de lecture. Il n'existe aucun troisième objet déclaré, et aucun enregistrement du commit de montée
(`template-upgrade` remplace le cœur et le manifeste, il ne pose aucun repère daté).

Conséquence mécanique : pour tout projet déjà en route, l'écart entre sa baseline d'adoption du squelette et
sa montée vers la version qui porte la règle n'est pas vide. Les chantiers ouverts dans cet intervalle
seraient traités comme neufs et se verraient réclamer la réponse à leur reprise ou à leur clôture —
exactement ce que le § 2.4 (promesse prospective) et le comportement **B7** interdisent.

Le mandat interdit d'inventer une seconde baseline à côté de la première. **Blocage 2 du § 3 : déclenché.**

### B.4 — Ce que `status` affiche pour un chantier ouvert, et où la nouvelle ligne s'insère

Pour chaque chantier dont le statut n'est pas `DONE`, `REJECTED` ou `SUPERSEDED` (l. 6429-6442) :

```
status.item          {id} — {title} : {status}
status.objective       Objectif : …
status.item_branch     Branche : … | Cible : …
status.missing         Vérifications manquantes : …
status.authorities     Autorités lues : …        (affichée seulement si le chantier en a)
status.block / resume  …                          (affichées seulement si bloqué)
```

La nouvelle ligne s'insère **après `status.missing`**, au même rang que `status.authorities` : même nature
(l'état d'une exigence portée par le chantier), même affichage conditionnel. Elle passe par le catalogue
`SPEECH` (l. 307-312), avec ses deux formulations `FR` et `EN`, conformément à la règle de langue de la 3.13.0.

### B.5 — Faut-il une vérification d'audit en plus du refus au démarrage ? → **Non, pas de contrôle nommé nouveau**

Précédent mesuré : la preuve de lecture refuse au démarrage (`require_authorities_digest`, l. 3498) **et** se
revérifie à l'audit — non par un contrôle dédié, mais par `project_control_errors()` qui alimente
`SCHEMA_VALIDATION`. La forme de `prior_art` (deux valeurs, candidats portant `path` et `entry_point`,
justification si `REIMPLEMENT`) peut emprunter la même voie.

En revanche, **revérifier l'existence des chemins à l'audit est exclu** : le § 2.6 fige la déclaration après le
démarrage et le comportement **B9** exige qu'un chemin déplacé pendant le chantier ne bloque ni la clôture ni
l'audit. L'existence se vérifie une fois, au démarrage, jamais après.

### B.6 — Convention de nommage des contrôles

58 contrôles distincts. Forme constante : majuscules, mots séparés par `_`, en anglais, groupe nominal, souvent
`<OBJET>_<ÉTAT>` — `LEGACY_RECORDS_PRESENT`, `WORK_ITEM_AUTHORIZED`, `AUTHORITIES_BASELINE`, `IMPACT_MAP`,
`CONFLICT_GATE`, `COMMIT_GATE`, `REPORTING_STYLE`, `LANGUAGE`. Un contrôle nouveau s'écrirait donc
`PRIOR_ART_DECLARED`. Les refus de commande sont des phrases anglaises levées en `ProjectControlError`.

### B.7 — Nombre de chantiers présents dans la copie → **0**

`project_control/work-items/` ne contient que son `README.md`. `project_control/project-state.v1.json` porte
`repository_role: PROJECT_TEMPLATE`, `initialization.status: NOT_STARTED`, `legacy_baseline: null`,
`authorities_baseline: null`.

**Conséquence** : l'effet d'une baseline ne peut pas être observé dans le squelette lui-même. Les 164 essais
construisent leurs propres dépôts et leurs propres records ; c'est là, et là seulement, que les comportements
B7, B8 et B9 se démontreront.

---

## C. Les deux blocages du § 3

| Blocage | État | Fondement |
|---|---|---|
| Le record entre dans l'empreinte | **non déclenché** | § B.1 |
| La baseline existante ne couvre pas les deux chemins de régression | **déclenché** | § B.3 |

---

## D. Options soumises au Project Owner (la session ne choisit pas)

Toutes trois supposent acquis ce qui est déjà mesuré : `prior_art` entre dans `properties` du schéma et jamais
dans `required` ; l'existence des chemins se vérifie une seule fois, au démarrage.

**Option A — la frontière voyage dans le record.**
La commande de création de la nouvelle version marque chaque record qu'elle crée ; le démarrage ne réclame la
déclaration qu'aux records portant cette marque. Les records déjà présents n'en portent pas et n'en porteront
jamais : on ne leur demande rien, ni à la reprise, ni à la clôture.
*Pour* : une seule frontière, lue à l'identique par le démarrage, l'audit et le schéma ; aucun objet déclaré
nouveau ; aucune lecture de l'historique ; comportement identique dans un projet neuf et dans un projet monté.
*Contre* : la frontière vit dans un record administratif — protégée par le garde-fou de commit et par la règle
qui interdit d'écrire les records depuis une branche de chantier, mais elle y vit.

**Option B — une troisième baseline déclarée, sur le modèle de `authorities_baseline`.**
Chaque projet déclare, par décision humaine, le commit à partir duquel la règle s'applique chez lui. C'est
exactement ce qui a été fait quand la preuve de lecture est arrivée en 3.6.1.
*Pour* : conforme à la doctrine existante, forme éprouvée, frontière explicite et signée.
*Contre* : le § 3 du mandat interdit à la session de la prendre. Seul le Project Owner peut lever cette
interdiction. Coût d'adoption : une décision de plus à écrire dans chaque projet qui monte.

**Option C — la frontière déduite de l'historique Git.**
Le commit qui enregistre pour la première fois la nouvelle version dans le manifeste du cœur sert de repère.
*Pour* : aucun objet nouveau, aucune décision supplémentaire.
*Contre* : c'est une déduction, pas une déclaration. Elle dépend d'un historique intact : une réécriture, un
écrasement de commits, un projet qui reçoit le cœur sans son manifeste la faussent en silence. Signalée pour
être complet ; c'est la plus fragile des trois.

---

## E. Verdict

```
P7_BUILD_BLOCKED_DESIGN_DECISION_NEEDED
```

Le blocage est celui du second tiret du § 3 : la baseline existante ne couvre pas les deux chemins de
régression. Les options sont au § D. Aucune écriture n'a eu lieu ; le dossier original n'a été ni écrit, ni
branché, ni exécuté.
