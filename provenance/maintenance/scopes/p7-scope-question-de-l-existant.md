# P7 — fiche de cadrage : « La question de l'existant » (étape 1)

*Rapatriée dans le dépôt le 12 septembre 2026 (`TPL-D-071`). Ce document réunit, dans l'ordre où
ils ont été écrits et sans retouche de leur texte, le mandat de construction de l'étape 1 puis
son avenant. Append-only : une évolution ajoute une section datée, jamais une réécriture.*

*État du chantier : cadré, non construit. Le rapport de mesure de phase 0 et les deux rapports de
la revue indépendante vivent sous `provenance/maintenance/` à la même date.*

---

## Partie 1 — Mandat de construction (12 septembre 2026)

*12 septembre 2026. Pour la session qui construira le prototype. Entrées : fiche de cadrage V2, contre-vérification, décisions du Project Owner du 12 septembre.*

---

## 0. Avant de lancer — à cocher par Jeoffrey lui-même

- [ ] Une **copie jetable** du squelette existe, hors de l'original, et c'est elle qui est accordée au § 1.
- [ ] Les textes restants sont écrits — ou tu as décidé, en connaissance de cause, de passer devant.
- [ ] Ce qui est ouvert est fermé (commits non poussés, vitrine, montée du projet en attente) — ou tu as décidé de passer devant.

Ce mandat ne se lance pas tant que ces trois lignes ne sont pas cochées par toi. L'ordre est le tien ; il peut changer, mais par une décision, pas par oubli.

## 1. Dossier accordé

`⟨chemin de la copie jetable — à écrire par Jeoffrey, pas par la session⟩`

L'original du squelette n'est jamais le dossier accordé. Toute action qui en sortirait — écrire, brancher, committer, exécuter, pousser ailleurs — exige le double arrêt : d'abord nommer le dossier visé, l'action et l'alternative dans le périmètre ; ensuite reformuler le périmètre exact et obtenir une seconde confirmation explicite qui nomme le dossier. Un « ok » général ne vaut pas.

Aucune suppression de fichier utile, où que ce soit.

## 2. Ce qui est décidé et ne se rediscute pas

| # | Décision |
|---|---|
| 1 | **Deux réponses** à la question de l'existant : « ça existe » ou « rien trouvé ». Pas de « sans objet ». Aucune valeur par défaut. |
| 2 | La question est posée à **tous** les chantiers éligibles, y compris une correction d'une ligne. Le péage est à la taille du trajet : pour une petite correction, un fichier et une section suffisent comme point d'entrée. |
| 3 | Si ça existe et qu'on refait quand même : une **justification écrite**, exigée **au démarrage**, absente = refus. L'outil constate sa présence ; il ne juge pas le motif. |
| 4 | La promesse est **prospective**. Rien n'est promis sur le passé. Aucune enquête rétrospective n'est facilitée par ce chantier. |
| 5 | **Éligibilité** = chantiers ouverts après l'adoption de la version. **Une seule frontière**, partagée par le démarrage, l'audit et toute validation de schéma. Un chantier ancien qui reprend reste ancien. |
| 6 | La déclaration est **figée après le démarrage**. L'existence des chemins se vérifie une fois, au démarrage, jamais après. |
| 7 | Périmètre de l'étape 1, et rien d'autre : le champ, le refus au démarrage, la ligne dans `status`. **Ni** carte assemblée, **ni** recherche menée par le contrôleur, **ni** autre critère d'entrée. |
| 8 | Noms de contrôles et messages de refus en anglais ; textes destinés aux humains selon la convention de langue du projet. |

## 3. Phase 0 — mesurer, en lecture seule, avant toute écriture

Rien de ce qui suit n'est supposé connu. La session mesure et rapporte, sans écrire :

1. **Le record du chantier entre-t-il dans l'empreinte de lecture des autorités** exigée au démarrage ? Si oui, remplir le champ après le calcul de l'empreinte la périme, et le démarrage tourne en rond.
2. Où vit exactement le record d'un Work Item, et quel schéma le décrit.
3. Quel mécanisme de baseline d'adoption existe déjà, et s'il couvre les deux chemins de régression du § 2.5 : le chantier ancien qui reprend, et l'audit qui valide les anciens records contre un schéma commun.
4. Ce que `status` affiche aujourd'hui pour un chantier ouvert, et où la nouvelle ligne s'insère.
5. Si une vérification d'audit doit accompagner le refus au démarrage, ou si le refus suffit.
6. La convention de nommage des contrôles existants, pour y aligner le nouveau.
7. Le nombre de chantiers présents dans la copie, pour mesurer l'effet de la baseline.

**Sortie de phase 0 : un rapport de mesure court, puis un arrêt.** La construction ne commence pas avant que ce rapport soit remis.

Deux résultats de mesure **bloquent** la construction — et ne se contournent pas par une astuce :

- **Le record entre dans l'empreinte.** Arrêt, décision de conception requise du Project Owner. La session propose les options (par exemple : exclure le record de l'empreinte ; ou exiger la réponse avant le calcul de l'empreinte), elle ne choisit pas.
- **La baseline existante ne couvre pas les deux chemins de régression.** Arrêt. On n'invente pas une seconde baseline à côté de la première ; on revient avec le constat.

## 4. Forme attendue du champ

À adapter à la convention constatée en phase 0. Ce qui suit fixe le sens, pas la syntaxe :

```
prior_art:
  capability:      texte — ce que le chantier doit savoir faire       (exigé)
  status:          FOUND | NONE_FOUND                                  (exigé, deux valeurs)

  # si FOUND :
  candidates:      liste, au moins un — { path, entry_point, note }    (chaque path doit exister au démarrage)
  reuse_decision:  REUSE | ADAPT | REIMPLEMENT                         (exigé si FOUND)
  justification:   texte                                               (exigé si REIMPLEMENT)
  external:        texte libre — capacité connue dans un autre dépôt   (optionnel, aucun contrôle de chemin)

  # si NONE_FOUND :
  searched:        { paths: [...], terms: [...] }                      (les deux non vides ; chaque path doit exister)

  declared_at:     horodatage posé par le contrôleur au démarrage, figé ensuite
```

Une chaîne non vide ne vaut pas réponse : le refus porte sur une réponse **incomplète**, pas seulement sur un champ vide.

## 5. Comportements à construire — un essai chacun, rouge avant, vert après

| # | Comportement | Attendu |
|---|---|---|
| B1 | chantier éligible, champ absent | `start` refusé |
| B2 | `FOUND` sans candidat, ou candidat sans chemin ou sans point d'entrée | `start` refusé |
| B3 | `FOUND` avec un chemin qui n'existe pas | `start` refusé |
| B4 | `NONE_FOUND` sans `paths` ou sans `terms`, ou avec un `path` inexistant | `start` refusé |
| B5 | `FOUND` + `REIMPLEMENT` sans justification | `start` refusé |
| B6 | `FOUND` complet, puis `NONE_FOUND` complet | `start` accepté, `declared_at` posé |
| B7 | chantier ouvert **avant** adoption, repris après | `start` et `close` sans réclamer le champ |
| B8 | audit complet sur un dépôt ne contenant que des records anciens | vert |
| B9 | déclaration figée : chemin cité au démarrage, puis déplacé pendant le chantier | `close` et audit ne bloquent pas |
| B10 | `status` sur un chantier éligible sans réponse | la ligne apparaît, valeur `UNKNOWN` |

Et : la suite d'essais existante reste verte ; aucun essai existant n'est modifié pour passer.

## 6. Livrables

| | Livrable | Forme |
|---|---|---|
| D1 | Rapport de mesure de phase 0 | court, factuel, avant toute écriture |
| D2 | Transcription des essais | chaque essai montré rouge avant, vert après, dans la copie |
| D3 | **Un seul script bash** à lancer par Jeoffrey dans l'original | `set -euo pipefail` ; textes écrits en entier ; **liste exacte des fichiers touchés en tête** ; aucun push, aucun tag, aucune suppression. Le script ne touche pas aux records administratifs de l'original : l'ouverture du chantier et la décision de promotion s'y font par les commandes du contrôleur, lancées par Jeoffrey, comme d'habitude. |
| D4 | Textes prêts à coller | entrée CHANGELOG ; ligne de roadmap (P7 étape 1 livrée, étapes 2 et 3 ouvertes) ; paragraphe pour le template AGENTS.md expliquant le champ en une phrase |
| D5 | Retour en langage courant | ce qui a été fait, ce que ça change, ce que Jeoffrey doit faire — sans identifiants ni codes |

## 7. Verdict de fin de construction

Un seul, dans cette liste :

- `P7_BUILD_READY_FOR_PROMOTION` — tout est vert, D1 à D5 remis.
- `P7_BUILD_BLOCKED_DESIGN_DECISION_NEEDED` — la phase 0 a levé l'un des deux blocages du § 3 ; le rapport dit lequel et propose les options.
- `P7_BUILD_INPUT_MISSING` — une entrée manque ; le rapport dit laquelle.
- `P7_BUILD_PREFLIGHT_STATE_MISMATCH` — la copie ne correspond pas à l'état attendu ; le rapport dit en quoi.

## 8. Après la construction

- Version proposée : **3.20.0**, sauf si une version intermédiaire est sortie entre-temps.
- Revue indépendante du prototype avant promotion, par un mandat séparé. Le rapport de construction est écrit pour qu'un relecteur sans contexte puisse le vérifier.
- Promotion sur décision du Project Owner, jamais autrement.
- Non compris dans ce mandat : le critère d'utilité à vingt chantiers (§ 10 de la fiche) se relève à la main, plus tard ; il n'a pas besoin de code.

---

*Mandat sans autorité propre. Il n'ouvre aucun droit d'écriture hors du dossier accordé au § 1.*

---

## Partie 2 — Avenant 1 : le choix de la borne d'éligibilité (12 septembre 2026)

*12 septembre 2026. Entrées : le mandat de construction du 12 septembre, le rapport de mesure de phase 0, les deux rapports de revue indépendante et la réconciliation qui les recoupe. Cet avenant complète le mandat ; il ne le remplace pas.*

---

## 0. Ce que cet avenant change

1. Il nomme l'option retenue et ferme la question restée ouverte à la fin de la phase 0.
2. Il ajoute quatre définitions qui manquaient et sans lesquelles la règle se contredit en usage réel.
3. Il corrige une conclusion du rapport de mesure, ajoute trois comportements à démontrer, et sort du périmètre un défaut indépendant à corriger avant la construction.

Tout ce que le mandat d'origine fixe et qui n'est pas nommé ici reste en vigueur, à l'identique.

---

## 1. Option retenue

**Option A — la borne voyage dans la fiche.** La fiche d'un chantier porte une marque posée au moment où elle entre dans le projet ; le contrôleur ne réclame la déclaration qu'aux fiches marquées. Les fiches déjà présentes n'en portent pas, n'en porteront jamais, et ne sont jamais interrogées.

Les options B (borne signée par décision humaine) et D (inventaire figé à la montée) restent des voies de repli documentées, à rouvrir seulement si le § 2.2 ci-dessous se révèle intenable. L'option C (borne déduite de l'historique Git) est écartée : la déduction se fausse en silence dès qu'un historique est regroupé, exporté, cloné superficiellement ou ramené en arrière.

---

## 2. Les quatre définitions qui manquaient

### 2.1 — « Ouvert » veut dire *admis dans le projet*, pas *démarré*

Un chantier est ouvert au moment où sa fiche entre dans le projet, quelle que soit la voie. C'est là, et seulement là, que la marque se pose. Le démarrage vient plus tard et ne décide rien de l'éligibilité.

Conséquence directe : une fiche créée avant l'arrivée de la règle reste ancienne pour toujours, même si elle démarre, se bloque, reprend ou se clôt des mois après.

### 2.2 — Toutes les voies d'admission posent la marque

La commande de création n'est pas la seule porte d'entrée. Une fiche peut aussi arriver par copie depuis un autre projet, par écriture à la main, ou par une montée de version. La règle doit valoir pour toutes :

- toute voie d'admission prévue par le contrôleur pose la marque ;
- une fiche qui apparaît sans marque est traitée comme **ancienne** — donc jamais interrogée — mais son arrivée hors des voies prévues est **signalée** par l'audit, et non passée sous silence.

C'est la condition à laquelle tient l'option A : elle est sûre tant qu'aucune fiche n'entre sans qu'on le sache. Ce point est à démontrer, pas à supposer (voir B11).

### 2.3 — La réponse est exigée au premier départ effectif, quelle que soit la commande qui le provoque

Le mandat d'origine dit « au démarrage ». Cela reste vrai, mais il faut le préciser : un chantier peut être admis, puis bloqué, puis reprendre sans avoir jamais démarré. Dans ce cas c'est la reprise qui constitue le premier départ, et c'est elle qui réclame la réponse.

La règle exacte : **pour une fiche marquée, la première commande qui met le chantier en travail exige la déclaration complète**, qu'il s'agisse du démarrage ou d'une reprise. Pour une fiche non marquée, aucune commande ne la réclame jamais.

L'horodatage est posé par le contrôleur à ce premier départ, et la déclaration est figée ensuite — ce qui ne change rien au § 2.6 du mandat d'origine, seulement le moment exact où le verrou se ferme.

### 2.4 — Une fiche administrative ne périme jamais sa propre empreinte de lecture

Le contrôleur écarte déjà de l'empreinte de lecture les documents qu'il tient lui-même, parce qu'autrement chaque transition invaliderait la preuve du chantier en cours. Cet écart doit couvrir aussi les fiches de chantier : **si un projet déclare une fiche parmi ses documents à lire, ce chemin est écarté de l'empreinte**, comme le sont déjà la feuille de route, l'état du projet et la liste des idées.

Sans cette règle, un projet qui route ses propres fiches se retrouve dans une impasse : écrire la réponse dans la fiche périme la preuve de lecture, et le démarrage tourne en rond.

---

## 3. Erratum au rapport de mesure de phase 0

Le § B.1 du rapport conclut que la fiche d'un chantier n'entre pas dans l'empreinte de lecture. **Cette conclusion vaut pour le routage livré avec le modèle, et pour lui seul.** L'empreinte se calcule à partir des documents que le projet déclare : un projet libre de sa liste peut y mettre une fiche, et créer ainsi la circularité que la mesure écartait.

La mesure n'était donc pas fausse, mais incomplète — elle décrivait une configuration, pas une garantie. Le § 2.4 ci-dessus transforme le constat en règle. Le premier blocage du § 3 du mandat d'origine reste levé, désormais pour une bonne raison.

---

## 4. Comportements ajoutés à démontrer (suite du § 5 du mandat)

| # | Comportement | Attendu |
|---|---|---|
| B11 | une fiche déposée dans le projet sans passer par une voie d'admission prévue | elle n'est **pas** éligible, et l'audit signale son arrivée |
| B12 | un projet qui déclare une fiche de chantier parmi ses documents à lire | le démarrage reste possible : écrire la réponse ne périme pas la preuve de lecture |
| B13 | un chantier marqué, admis puis bloqué **avant** tout démarrage, qui reprend | la reprise exige la déclaration complète |

Les dix comportements B1 à B10 du mandat d'origine sont inchangés. La formulation du champ au § 4 reste valable ; le rappel « une chaîne non vide ne vaut pas réponse » doit être appliqué à chaque partie de la réponse, et pas seulement au champ pris dans son ensemble.

---

## 5. Un défaut indépendant, à corriger avant la construction

La revue a mis au jour un défaut du contrôleur actuel qui n'a rien à voir avec la question de l'existant, mais qui bloque un usage courant :

> Quand le garde-fou de commit est en place, un chantier bloqué qui porte ses propres commits ne peut plus reprendre dès lors qu'un autre chantier a été clos entre-temps. La vérification du commit de clôture du chantier voisin est faite contre la seule branche courante, qui ne contient pas encore ce commit au moment de la fusion ; le contrôle échoue et le garde-fou refuse.

Reproduit et vérifié. La raison pour laquelle la suite d'essais ne le voyait pas est identifiée : les essais montent leurs dépôts **sans installer le garde-fou**, et le scénario passe donc sans lui alors qu'il échoue avec.

Ce défaut sort du périmètre de P7. Il appelle son propre correctif, accompagné d'un essai qui installe le garde-fou — c'est-à-dire un essai qui mesure ce qui se passe réellement chez l'utilisateur, et non une version allégée du même parcours.

**Ordre recommandé** : ce correctif d'abord, la construction de P7 ensuite. Un prototype bâti sur un contrôleur qui refuse une reprise légitime ne se vérifie pas proprement.

---

## 6. Ce qui ne change pas

Les huit décisions du § 2 du mandat d'origine, la forme du champ au § 4, les dix comportements B1 à B10, le périmètre du § 2.7 (le champ, le refus au départ, la ligne d'état — ni carte assemblée, ni recherche menée par le contrôleur, ni autre critère d'entrée), les livrables D1 à D5, et la liste fermée des verdicts.

La promotion reste la décision du Project Owner, jamais autrement.

---

*Avenant sans autorité propre. Il n'ouvre aucun droit d'écriture hors du dossier accordé au § 1 du mandat d'origine.*
