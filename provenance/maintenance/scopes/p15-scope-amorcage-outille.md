> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# P15 — L'amorçage outillé

*Fiche de cadrage. 9 septembre 2026. Ouverte par le second projet réel, pas encore autorisée.*

## 1. D'où vient ce chantier

Un second projet réel — « Coût moyen crypto », calculateur de prix de revient moyen pondéré — a été
mené de bout en bout sur le squelette `3.14.0` : projet **neuf**, né gouverné, sur une machine
vierge sans réseau. C'est le premier essai de l'autre chemin d'adoption, celui qu'Alpha
V8 ne couvre pas (V8 est un dépôt existant qui adopte le contrôleur).

Le cœur a tenu sans exception. Ce qui n'a pas tenu, c'est l'accueil, et le rapport le dit d'une
phrase :

> « la douleur n'est pas dans le squelette, elle est exactement là où le squelette n'outille pas —
> l'amorçage. »

## 2. Le constat, mesuré

| | Durée |
|---|---|
| Initialisation, écrite à la main | **6 minutes** |
| WI-002, écrit par `create-work-item` | 4 minutes |
| WI-003, écrit par `create-work-item` | 4 minutes |

Six des sept constats de la note de test tombent dans les six premières minutes. Une fois
`create-work-item` disponible — record, décision, conversation, roadmap humaine, roadmap machine,
registre des branches et classification Git écrits et committés en une transaction — plus un seul
accroc.

La `3.15.0` a balisé ces murs : les modèles sont devenus le texte accepté, les refus disent le
format attendu, le mandat manquant est écrit là où on le cherche. C'est un pansement honnête, pas
le correctif de fond. **Ce que le contrôleur écrit lui-même, personne ne peut le mal écrire.**

## 3. Ce que la commande ferait

Une commande d'amorçage — nom à décider, `bootstrap-work-item` ou `bootstrap-first` — qui, à partir
des réponses de l'interview, écrirait en une transaction :

- la première décision humaine, au format exact, dans `docs/governance/HUMAN_DECISIONS.md` ;
- le premier Work Item et sa référence de conversation ;
- la première entrée du registre des branches, balises comprises ;
- la ligne de roadmap correspondante et la classification Git.

Exactement ce que `create-work-item` fait déjà, mais avant que le Normal Mode existe.

## 4. Ce qu'elle reprendrait aussi

La **route B** du mur de sortie de l'initialisation (`C-2` de la note de test, `TPL-D-035`) : que le
garde-fou reconnaisse de lui-même la transition de clôture — `FIRST_START.md`, Project State et les
records du premier Work Item indexés ensemble, `bootstrap-closeout` PASS — comme administrative, au
lieu d'exiger le mandat d'override. La `3.15.0` a retenu la route A (écrire le mandat dans
`FIRST_START.md`) parce que desserrer une protection mérite son propre chantier et ses propres
essais.

## 5. Ce qu'elle ne ferait pas

- Elle ne conduit pas l'interview : les réponses restent celles du Project Owner.
- Elle ne valide rien à sa place : `Status: VALIDATED` reste un geste humain sur un document lu.
- Elle ne remplace pas `bootstrap-preflight` ni `bootstrap-closeout`.

## 6. Questions ouvertes

1. La commande écrit-elle aussi la charte et l'architecture, ou seulement les records ?
2. Une seule commande, ou une par groupe d'écritures de l'allowlist bootstrap ?
3. La route B change le garde-fou : quels essais démontrent qu'aucune autre écriture ne passe par
   cette porte ?
4. Le ratio d'adoption mesuré — la gouvernance a coûté à peu près autant que les 200 lignes de code
   du projet d'essai — descend-il assez pour qu'un projet de 50 lignes reste défendable ?

## 7. État

`CLOSED` — clos par le Project Owner le 10 septembre 2026, sans être ouvert.

« On a déjà clôturé l'affaire. C'est une mauvaise lecture de ta part. C'est allé très vite en
réalité ! »

La fiche est conservée telle qu'elle a été écrite, parce qu'elle enregistre une mesure réelle. Mais
sa lecture était fausse sur le point qui compte : les six minutes d'initialisation sont du **temps
machine et du travail de l'agent**, pas le temps du Project Owner. Le sien s'est compté en secondes,
et il avait déjà dit de cet essai qu'il était « totalement réussi ». Le mot « douleur », emprunté au
rapport de test, ne décrit pas son expérience et n'aurait pas dû être repris.

Ce qui a effectivement été livré depuis, en `3.15.0` : les modèles réécrits comme texte
directement copiable, les refus qui nomment le format attendu, le mandat écrit au point 4 de
`FIRST_START.md`, la porte d'entrée d'un projet neuf en tête d'`ADOPTION.md`. C'est ce qui manquait ;
la commande d'amorçage n'est pas nécessaire. La « route B » du mur de sortie reste écartée : la
`3.15.0` a retenu la route A, et desserrer une protection reste un chantier qu'on n'ouvre pas sans
raison.
