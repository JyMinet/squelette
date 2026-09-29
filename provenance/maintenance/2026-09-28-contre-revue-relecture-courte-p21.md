> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Contre-revue — Relecture courte de la fiche « Tableau des clés » V2

Date : 2026-09-28. Auteur : Claude (auteur de la fiche ; conflit d'intérêt déclaré, d'où la vérification par le code et par les sondes plutôt que par argument). Lecture seule du dossier `~/Projets/squelette-revue-tableau-des-cles/` ; la fiche V3 et cette contre-revue y sont ajoutées sans rien modifier d'existant.

## Résumé en trois points

1. **Ce qui s'est passé.** Les quatre constats nouveaux de Codex (N1 à N4) et ses remarques transversales sont confirmés, aucun n'est rejeté. En corrigeant, un point de plus est apparu : la réparation « copie par copie » qu'il proposait serait elle-même refusée par le garde-fou de commit.
2. **Ce que ça change.** La fiche V3 retient la variante que Codex donnait en second : la réparation groupée, en une transaction. Le reste suit ses corrections, avec deux précisions sur le compartiment caché de Git.
3. **Ce que Jeoffrey doit faire.** Dire si l'on construit maintenant (les trois cas devenant des essais obligatoires, la seconde IA relisant le code) ou si la V3 repasse d'abord en relecture.

## A — Preflight

| Objet | Constat |
|---|---|
| `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V2.md` | 118 lignes, lu en entier ; `c71e93d4…0e93` |
| Pièces antérieures | fiche V2, contre-revue V2, mandat V2 : empreintes identiques à leur dépôt |
| `source/` | 138 fichiers, `sha256sum -c` OK |
| `runs/v2/results.json` | lu : sondes P04, P06, P07, P09, N1, N2, P10_N3, P11 |

## B — Vérifications

| Constat | Vérification | Résultat |
|---|---|---|
| N1 MAJOR — `.git` hors inventaire | `N1_git_private` : hook `pre-push` unique, catégories énumérées inchangées. Relu : la V2 n'excluait que `copie.json` de `.git`. | CONFIRMÉ. Instance plus grave ajoutée : un commit joignable seulement par le reflog (branche supprimée) est du travail récupérable que ni les références ni `git status` ne montrent. |
| N2 MAJOR — script après déplacement | `N2_moved_target` : contrôle par identifiant sur B passe, le vieux script vise A réoccupé, rien effacé. Relu : la V2 ne liait pas le chemin contrôlé au chemin effacé. | CONFIRMÉ. |
| N3 MAJOR — réparation à deux copies | `P10_N3` : réparation individuelle refusée pour A comme pour B. | CONFIRMÉ. |
| N4 MINOR — mentions périmées | Relu : résumé point 3, §6, §9 phase 1, bannière d'un clone déplacé, annexe A. | CONFIRMÉ. |
| Vue et tag | `source/scripts/project_control.py` l. 2530–2546 : les tags entrent dans l'empreinte de fraîcheur de la vue ; `source/provenance/CHANGELOG.md` l. 796–798 : tag sur la décision, vue régénérée ensuite. | CONFIRMÉ : l'ordre de la V2 (vue avant tag) rendait la vue aussitôt périmée. |
| Fiche de sortie | l. 2148–2150 : l'audit saute les JSON sous `.git`. | CONFIRMÉ : aucune collision. |
| Fenêtre d'écriture | La V2 ne visait que « un agent ». | CONFIRMÉ : toute écriture compte. |

## C — Ajouts de la contre-revue

**C-01 — La réparation monotone copie par copie est refusée par le garde-fou.** Les transitions du contrôleur committent à travers le garde-fou « like any other » (`commit_records`, l. 4589–4593) ; le garde-fou lance l'audit du mode sur l'état indexé et refuse un état en échec (`scripts/hooks/pre-commit`). Après le retour de A seul, le FAIL de B demeure : le commit du retour de A serait refusé. La correction principale de N3 (« A puis B ») exigerait d'assouplir le garde-fou pour accepter un état partiellement rouge — brèche générale, écartée. La fiche V3 retient la variante groupée de Codex : une transaction couvrant toutes les copies en faute (rendues, ou `KEPT` sous décision), audit PASS à la sortie. Critère de fermeture de Codex respecté (« A puis B, ou le groupe, sans override global »).

**C-02 — Le garde-fou installé vit dans `.git/hooks`.** Depuis 3.10.0, `install-gate` place la copie exécutable du garde-fou dans `.git/hooks/pre-commit` (vérification l. 3494). Une correction de N1 qui compterait tous les hooks ferait échouer chaque retour. La V3 classe comme technique le garde-fou installé **identique** au fichier `scripts/hooks/pre-commit` de la copie ; un garde-fou différent devient un élément à rendre.

**C-03 — Nouveau retour.** La V2 ne disait pas quoi faire d'une copie `RETURNED` retravaillée (Codex le demandait déjà au tour précédent). La V3 admet un nouveau retour complet qui remplace l'empreinte.

## D — Désaccords

Aucun sur le fond. La réparation groupée n'est pas un désaccord : c'est la variante que Codex proposait, choisie parce que l'autre heurte le garde-fou.

## Verdict

`CADRAGE_TABLEAU_DES_CLES_V2_REVIEW_OF_RELECTURE_COURTE_PASS`
