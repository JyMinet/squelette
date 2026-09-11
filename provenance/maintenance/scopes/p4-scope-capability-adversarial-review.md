# P4 — Scope Definition V1 : capability `ADVERSARIAL_REVIEW`

Statut : `SCOPE_DEFINITION_V1 — NOT_AUTHORIZED`
Nature : définition de périmètre. Extraction d'une pratique existante en capability optionnelle du squelette. Aucune écriture exécutée.

## 1. Problème

Le dispositif de revue indépendante — mandats de reviewer, verdicts à vocabulaire fermé, challenges adversariaux, contre-revues croisées, réconciliation multi-reviewers — existe et fonctionne, mais uniquement comme pratique reconstruite à chaque phase. Il n'a ni gabarit, ni schéma, ni contrôle. Conséquences observables : le vocabulaire de verdicts est réénoncé dans chaque mandat, l'indépendance des reviewers repose sur la discipline de l'opérateur, et rien n'empêche un livrable d'écraser un précédent.

## 2. Positionnement

Capability **optionnelle**, `OFF` par défaut, conforme à `OMIT > ACTIVATE WITHOUT NEED`. Elle ne s'active que si le projet déclare un besoin de revue indépendante. Elle n'introduit aucun runtime, aucune dépendance externe, aucun provider imposé.

## 3. Non-objectifs

- Ne pas imposer de modèle ni de fournisseur d'IA comme reviewer.
- Ne pas automatiser le jugement : la capability structure la revue, elle ne la rend pas.
- Ne pas remplacer les gates humaines existantes.
- Ne pas rendre la revue obligatoire pour un Work Item ordinaire.

## 4. Contenu proposé

### 4.1 Arborescence normalisée

```text
reports/<phase>/
  scope-reconstructions/
  scope-definitions/
  challenges/
  cross-reviews/
  reconciliations/
  closure-challenges/
```

Règle append-only : un livrable n'est jamais écrasé. Une correction crée une révision liée (`V2`, erratum), jamais une réécriture silencieuse — reprise du principe déjà présent dans le Charter.

### 4.2 Vocabulaire de verdicts fermé

Un verdict terminal appartient à une liste close, préfixée par l'objet revu :

- `…_PASS`
- `…_REQUIRES_MINOR_REDLINE`
- `…_REQUIRES_MAJOR_REDLINE`
- `…_CANONICAL_CONFLICT`
- `…_INPUT_MISSING`
- `…_PREFLIGHT_STATE_MISMATCH`
- `…_OUTPUT_ALREADY_EXISTS`

Pour une contre-revue : `…_REVIEW_OF_<X>_PASS`, `…_REQUIRES_MINOR_RECONCILIATION`, `…_REQUIRES_MAJOR_RECONCILIATION`, plus les trois derniers ci-dessus.

Un verdict hors liste est un défaut de livrable, pas une nuance.

### 4.3 Gabarit de mandat reviewer

Champs obligatoires : objet revu et son état exact (chemin, HEAD, SHA-256) ; posture (`READ_ONLY` / `REPORT_ONLY`) ; interdits explicites — aucune écriture hors du livrable, aucun `fetch`/`pull`/`push`/`checkout`/`commit`/`tag`/`branch`, aucun ADR, aucun objet Project Control, aucune décision humaine simulée ; chemin unique du livrable, jamais d'écrasement ; liste close des verdicts ; standard de redline ; structure de rapport imposée.

### 4.4 Standard de redline

**Sans scénario d'échec démontré, pas de redline.** Une observation sans scénario reste une observation, pas un blocage. Un finding porte : identifiant, sévérité, objet, scénario d'échec reproductible, preuve (chemin, lignes, octets, SHA-256), impact, correction proposée, statut.

### 4.5 Règles d'indépendance

- Un reviewer ne lit pas le livrable d'un autre reviewer avant d'avoir rendu le sien.
- Une contre-revue lit l'objet **et** le livrable qu'elle contre-revoit, jamais la contre-revue parallèle.
- La réconciliation lit tout, et n'est pas rendue par un reviewer de premier tour.
- Chaque mandat s'exécute dans une session indépendante.

### 4.6 Schéma machine

`review-artifact.v1.schema.json` : type (`scope_reconstruction` | `challenge` | `cross_review` | `reconciliation` | `closure_challenge`), phase, objet revu avec son hash, reviewer (identité libre, provider-agnostic), verdict issu de la liste close, compteurs de findings par sévérité, chemin du livrable, dépendances de lecture déclarées.

Contrôle d'audit associé : verdict dans la liste close, livrable existant et non écrasé, dépendances de lecture cohérentes avec les règles d'indépendance.

## 5. Impacts

- `DIRECT` : nouveau répertoire `adversarial_review/` (gouvernance, gabarits, schéma), `ADOPTION.md`, éventuellement un contrôle d'audit conditionné à l'activation.
- `INDIRECT` : aucun projet existant n'est affecté tant que la capability est `OFF`.
- `AUTHORITY` : introduit une notion de phase implicite dans l'arborescence `reports/<phase>/`, qui recoupe P5 (objet `PHASE`). Dépendance à arbitrer.
- `CONCURRENT` : P1 doit être clos avant, sous peine d'ajouter la capability à une copie non canonique.

## 6. Points non tranchés

- La capability suppose-t-elle P5 (objet `PHASE`) ou reste-t-elle documentaire : `UNKNOWN`.
- Le contrôle d'indépendance est-il vérifiable par machine, ou seulement déclaratif : `UNKNOWN`.
- Nombre minimal de reviewers pour déclencher une réconciliation : `UNKNOWN`.

## 7. Critères de fermeture proposés

1. Un projet avec la capability `OFF` est strictement inchangé — audit et tests identiques.
2. Un projet avec la capability `ON` refuse un verdict hors liste close et un livrable qui écraserait un existant.
3. Les gabarits permettent de conduire une phase de revue sans réénoncer les conventions dans le mandat.
4. Aucune dépendance hors bibliothèque standard.
