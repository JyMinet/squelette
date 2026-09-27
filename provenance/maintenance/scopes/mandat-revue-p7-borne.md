> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Mandat de revue — P7 étape 1 : le choix de la borne d'éligibilité

*Squelette de projet gouverné, version 3.19.1. Mandat rédigé le 12 septembre 2026. À coller dans une session neuve et indépendante. Deux contrôleurs différents mènent cette revue séparément.*

---

## 0. Ce qu'on te demande, en trois lignes

1. Vérifier sept mesures déjà prises sur le code, et dire pour chacune si elle tient.
2. Examiner trois options de conception en situation d'usage courant, et dire ce que chacune donne de faux, et quand.
3. Rendre un seul document, avec un verdict pris dans une liste fermée, et un classement motivé des trois options.

Tu ne modifies rien. Tu ne proposes pas de code. Tu rapportes.

---

## 1. Le contexte, en peu de mots

Ce dépôt est un modèle de projet réutilisable. Il fournit un contrôleur en ligne de commande (`scripts/project_control.py`) qui encadre le travail d'un agent : un chantier (« Work Item ») ne démarre pas sans autorisation, l'agent doit prouver qu'il a lu les documents qui font autorité, et un audit vérifie l'ensemble à tout moment.

On veut ajouter **une ligne de plus à la fiche d'un chantier** : « qu'est-ce qui existe déjà sur ce sujet, et où ? ». Deux réponses possibles, pas de troisième. Le contrôleur refuse de démarrer le chantier tant que la réponse n'est pas là et complète.

La règle ne doit valoir que pour les chantiers **ouverts après son arrivée**. Jamais pour les anciens. C'est là que le travail s'est arrêté : le contrôleur ne sait pas dater l'arrivée d'une version dans un projet. Il faut choisir **comment il le saura**. Trois options sont sur la table. C'est l'objet de cette revue.

---

## 2. Dossier accordé et posture

| | |
|---|---|
| Dossier accordé | `~/Projets/squelette-revue-p7` |
| Contenu attendu | `source/` — copie du dépôt au tag `v3.19.1`, **lecture seule** ; `entrees/` — les pièces du § 3 ; `runs/` — copies jetables si tu veux rejouer quelque chose |
| Livrable unique | `REVUE_P7_BORNE-1.md` (premier contrôleur) ou `REVUE_P7_BORNE-2.md` (second), à la racine du dossier accordé |

Posture : **lecture seule, rapport seul.**

- Rien n'est écrit hors du livrable unique, et rien hors du dossier accordé.
- Pas de `fetch`, `pull`, `push`, `tag`, `commit`, ni de branche.
- `source/` reste intact d'un bout à l'autre ; toute manipulation se fait dans une copie sous `runs/`.
- Aucun autre dossier de la machine n'est ouvert.
- Si un doute d'autorité apparaît, tu t'arrêtes et tu l'écris ; tu ne tranches jamais à la place du Project Owner.
- Les deux contrôleurs travaillent séparément : tu ne lis pas le livrable de l'autre avant d'avoir rendu le tien.

---

## 3. Pièces fournies

| | Pièce | Rôle |
|---|---|---|
| E1 | `mandat-construction-p7-etape-1.md` | ce qui est décidé et ne se rediscute pas (§ 2), la forme attendue du champ (§ 4), les dix comportements attendus (§ 5) |
| E2 | `D1-rapport-mesure-phase-0-P7-etape-1.md` | les sept mesures prises sur le code, avec leurs références de ligne, et les trois options (§ D) |
| E3 | `source/` | le dépôt au tag `v3.19.1` |

Le contrôleur (`scripts/project_control.py`, ses schémas, ses documents de gouvernance) est **identique** entre le tag `v3.19.1` et l'état courant du dépôt : les commits postérieurs ne touchent que des documents rapatriés. Travailler au tag est donc suffisant et préférable.

Si une pièce manque ou ne correspond pas à ce qui est annoncé, tu rends `P7_BORNE_REVUE_INPUT_MISSING` ou `P7_BORNE_REVUE_PREFLIGHT_STATE_MISMATCH` et tu t'arrêtes là.

---

## 4. Ce qui est fixé et ne se rediscute pas

Ces huit points ont été tranchés par le Project Owner. Les examiner est hors sujet ; les prendre pour contrainte est le travail.

1. **Deux réponses** seulement : « ça existe » ou « rien trouvé ». Pas de troisième valeur, aucune valeur par défaut.
2. La question est posée à **tous** les chantiers éligibles, y compris une correction d'une ligne.
3. Si ça existe et qu'on refait quand même : une **justification écrite**, exigée au démarrage. L'outil constate sa présence, il ne juge pas le motif.
4. La promesse est **prospective**. Rien n'est promis ni demandé sur le passé.
5. **Éligibilité = chantiers ouverts après l'adoption de la version.** Une seule frontière, partagée par le démarrage, l'audit et toute validation de schéma. Un chantier ancien qui reprend reste ancien.
6. La déclaration est **figée après le démarrage**. L'existence des chemins cités se vérifie une fois, au démarrage, jamais après.
7. Périmètre : le champ, le refus au démarrage, la ligne dans `status`. **Ni** carte assemblée, **ni** recherche menée par le contrôleur, **ni** autre critère d'entrée.
8. Noms de contrôles et messages de refus en anglais ; textes destinés aux humains selon la convention de langue du projet.

---

## 5. Les trois options, énoncées neutrement

**Option A — la borne voyage dans la fiche.**
La commande de création de la nouvelle version marque chaque fiche qu'elle crée. Le démarrage ne réclame la déclaration qu'aux fiches portant cette marque. Les fiches déjà présentes n'en portent pas et n'en porteront jamais.

**Option B — la borne est signée par une décision humaine.**
Chaque projet déclare, par une décision enregistrée, le commit à partir duquel la règle s'applique chez lui — sur le modèle exact des deux bornes qui existent déjà dans le contrôleur (`legacy_baseline`, `authorities_baseline`).

**Option C — la borne est déduite de l'historique.**
Le contrôleur cherche dans l'historique Git le commit qui enregistre pour la première fois la nouvelle version dans le manifeste du cœur, et s'en sert comme repère.

---

## 6. Les questions posées

### T-01 — Les sept mesures tiennent-elles ?

Rejoue chacune des sept mesures de E2 § B sur `source/`. Pour chacune : confirmée, partiellement confirmée, ou fausse — avec la preuve (chemin, lignes, sortie de commande). Signale toute mesure incomplète ou toute conséquence qui n'en découle pas.

Deux points méritent une attention particulière :

- la conclusion B.1 (le record d'un chantier n'entre pas dans l'empreinte de lecture) : existe-t-il une configuration de projet, même inhabituelle, où il y entrerait ?
- la conclusion B.3 (le champ doit rester facultatif dans le schéma) : existe-t-il un autre endroit du contrôleur qui, indépendamment du schéma, refuserait un record ancien une fois le champ introduit ?

### T-02 — Option A en usage courant

Dans quelles situations la marque posée à la création donne-t-elle une réponse fausse — c'est-à-dire réclame la question à un chantier ancien, ou l'épargne à un chantier neuf ? À examiner au minimum :

- un dépôt qui monte de version alors qu'un chantier est déjà ouvert, puis le reprend ;
- un chantier créé, bloqué, puis repris des semaines plus tard ;
- une fiche recopiée depuis un autre projet, ou écrite à la main ;
- un projet neuf créé à partir du modèle ;
- une montée de version interrompue puis relancée.

### T-03 — Option B en usage courant

Même exercice. À examiner au minimum : la décision absente ; écrite après coup ; nommant un commit qui n'est pas celui de la montée ; un projet sans borne d'adoption préalable ; un projet neuf, qui n'a aucune montée à dater. Chiffre aussi le coût réel d'adoption : combien de gestes en plus, pour un projet existant et pour un projet neuf.

### T-04 — Option C en usage courant

Même exercice. À examiner au minimum : historique réécrit ou commits regroupés ; dépôt recréé sans son historique ; cœur installé sans son manifeste ; version montée puis ramenée en arrière ; copie de travail prise sans les objets Git.

### T-05 — Une seule frontière, et les dix comportements

Le point 5 du § 4 exige **une seule** frontière, partagée par le démarrage, l'audit et la validation de schéma. Pour chaque option : montre qu'elle est unique, ou exhibe le cas où deux frontières apparaissent et divergent.

Puis, pour chaque option, passe les dix comportements attendus de E1 § 5 (B1 à B10) : tenu tel quel / tenu au prix d'une règle supplémentaire à écrire / impossible. Les cas B7, B8 et B9 sont les plus discriminants.

### T-06 — La forme du champ

La forme proposée en E1 § 4 est-elle complète ? Cherche les manières d'écrire une réponse qui franchirait le contrôle sans rien dire d'utile : chaîne vide ou blanche, liste à un élément vide, chemin qui existe mais ne veut rien dire, terme de recherche d'un caractère, justification réduite à un mot. Le mandat dit qu'« une chaîne non vide ne vaut pas réponse » : le dis-tu suffisamment ? Propose la formulation qui manque, sans écrire de code.

### T-07 — Un angle de ton choix

Un seul, celui qui te paraît le plus utile et qui n'est couvert par aucune question ci-dessus. Dis pourquoi tu l'as retenu.

---

## 7. Standard de constat

**Sans situation démontrée, pas de constat bloquant.** Une remarque sans situation reste une observation et ne bloque rien.

Un constat porte : un identifiant, une sévérité (mineur / modéré / majeur), l'objet, la situation reproductible pas à pas, la preuve (chemin, lignes, octets, empreinte, sortie de commande), la conséquence, et la correction suggérée.

Les trois options sont des intentions, pas du code : une situation se démontre donc sur le contrôleur existant (ce qu'il fait aujourd'hui) ou par un enchaînement de commandes rejoué dans une copie sous `runs/`, jamais par un raisonnement seul. Quand une démonstration n'est pas possible, dis-le et classe le point en observation.

Les données et décisions inventées pour les besoins de la revue sont permises **dans `runs/` uniquement**, marquées en tête « EXEMPLE DE REVUE — FICTIF, N'AUTORISE RIEN ».

---

## 8. Verdict

Un seul, pris dans cette liste, en tête du livrable :

- `P7_BORNE_REVUE_PASS`
- `P7_BORNE_REVUE_REQUIRES_MINOR_REDLINE`
- `P7_BORNE_REVUE_REQUIRES_MAJOR_REDLINE`
- `P7_BORNE_REVUE_INPUT_MISSING`
- `P7_BORNE_REVUE_PREFLIGHT_STATE_MISMATCH`
- `P7_BORNE_REVUE_OUTPUT_ALREADY_EXISTS`

Un verdict hors liste est un défaut de livrable, pas une nuance.

---

## 9. Forme du livrable

Un seul fichier, `REVUE_P7_BORNE-1.md` ou `REVUE_P7_BORNE-2.md` selon que tu es le premier ou le second contrôleur, écrit une fois. Une correction crée une révision liée (V2, erratum), jamais une réécriture silencieuse.

Sections, dans cet ordre :

1. **Résumé en trois points** pour le Project Owner, en langage courant, sans identifiants ni codes.
2. **Préflight** : chemin du dossier accordé, commit de `source/`, empreintes des pièces fournies, état de `source/` avant et après.
3. **T-01 à T-07**, une section par question.
4. **Constats**, du plus grave au moins grave.
5. **Classement motivé des trois options**, présenté comme une recommandation à trancher par le Project Owner — jamais comme une étape acquise. Si une quatrième voie apparaît en cours de revue, elle s'ajoute au classement, avec sa démonstration.
6. **État final** : `source/` intact (compte de fichiers et empreinte avant/après), ce qui a été créé sous `runs/`.
7. **Verdict**.

---

## 10. Ce qui n'est pas demandé

- Écrire du code, un correctif, un patch ou une fiche de chantier.
- Ouvrir, lire ou citer un autre dépôt de la machine.
- Rediscuter les huit points du § 4.
- Élargir le périmètre du § 4 point 7 (carte assemblée, recherche menée par le contrôleur, autre critère d'entrée).
- Décider. La décision appartient au Project Owner.

---

*Mandat sans autorité propre. Il n'ouvre aucun droit d'écriture hors du dossier accordé au § 2.*
