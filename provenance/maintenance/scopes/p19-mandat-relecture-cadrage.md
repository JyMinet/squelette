> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# MANDAT — relecture de cadrage : « Deux volumes » (chantier P19, version 3.20.0)

*Message autonome : il ne suppose aucun souvenir d'une discussion précédente, et il n'exige
l'accès à aucun fichier. Le texte à examiner est joint en entier en partie B.*

---

# PARTIE A — LE MANDAT

## 1. Le contexte, en quelques lignes

Le Project Owner maintient un squelette de projet gouverné : un modèle réutilisable
(`AGENTS.md` + un contrôleur `project_control.py`) qui impose à un agent une suite de
vérifications avant, pendant et après chaque chantier. Deux projets réels vivent dessus.

Depuis la version 3.6.0, un chantier ne démarre qu'après lecture réelle des documents d'autorité
routés pour son périmètre : le contrôleur liste ces documents avec leur empreinte, l'agent les
lit, puis présente l'empreinte au démarrage. Le registre des décisions humaines
(`docs/governance/HUMAN_DECISIONS.md`) fait partie de ces documents, pour tous les chantiers.

Ce registre grossit sans jamais rétrécir. Le chantier P19 propose de le couper en deux : un
« carnet vivant » qui reste une autorité routée, et un « volume relié » qui contient les
décisions figées par la baseline d'adoption du projet et sort de la liste des documents à lire,
tout en restant vérifié par l'audit.

Une phase de mesure en lecture seule a déjà été exécutée. Ses chiffres sont résumés au § 2 du
texte joint. Tu n'as pas à les recalculer ; tu peux en revanche dire si une conclusion en est
tirée abusivement.

## 2. Ce qui t'est demandé

Une **relecture de conception**, avant écriture du code. Le texte joint est une fiche de cadrage :
il décrit ce qui sera construit et ce qui ne le sera pas. Tu examines si ce qui est décrit tient
debout.

Sept thèmes. Pour chacun, cherche des **configurations dégradées** — des états du dépôt, des
séquences d'opérations ou des cas limites où le dispositif décrit ne produirait pas le résultat
annoncé.

- **T-01 — La ligne de coupe.** Le dispositif coupe à la baseline d'adoption déjà déclarée par le
  projet. Configurations à examiner : un projet sans baseline déclarée ; un projet dont la
  baseline est retirée après la coupe ; une baseline dont la décision qui la déclare serait
  elle-même dans le volume relié ; deux baselines déclarées (adoption et preuve de lecture) dont
  l'une avance.
- **T-02 — L'intégrité du texte déplacé.** La fiche promet un texte identique à l'octet près et
  aucune requalification. Le dispositif décrit garantit-il cela dans tous les cas — notamment aux
  frontières d'un bloc (première décision, dernière décision, lignes vides, fin de fichier) ?
- **T-03 — La résolution des références.** Des enregistrements anciens citent des décisions qui
  partent dans le volume relié. Examine : un enregistrement ancien ; un enregistrement **créé
  après** la coupe qui citerait une décision reliée ; une décision citée à la fois par un
  enregistrement et par une déclaration de baseline ; une décision qui n'existerait dans aucun
  des deux volumes.
- **T-04 — L'empreinte de lecture.** Le volume relié sort de la liste des documents à lire parce
  qu'il n'est pas routé. La preuve de lecture reste-t-elle honnête ? Que promet-elle exactement
  après la coupe, et que ne promet-elle plus ? Le sommaire inséré dans le carnet vivant
  modifie-t-il l'empreinte d'un chantier en cours, et avec quelle conséquence ?
- **T-05 — Les refus.** La commande refuse d'agir dans deux cas : un bloc figé qui diffère de sa
  forme à la baseline, une référence qui cesserait de se résoudre. Ces deux motifs couvrent-ils
  tous les états où la coupe laisserait le dépôt dans une situation moins bonne qu'avant ?
  Manque-t-il un motif de refus ?
- **T-06 — Ce que la fiche promet et ce qu'elle décrit.** Chaque promesse du résumé et des § 1 à 5
  est-elle tenue par le dispositif décrit aux § 5 et 6 ? Signale les écarts dans les deux sens :
  une promesse sans mécanique, une mécanique sans promesse.
- **T-07 — La ligne de sommaire.** L'amendement 1 coupe les champs cités à 120 et 60 caractères et
  marque la coupe. Examine : ce que la ligne perd, et si ce qui reste suffit à reconnaître une
  décision ; le cas d'un champ dont les 120 premiers caractères disent le contraire de la suite ;
  et si « citer en coupant » tient la promesse « jamais reformulée, jamais requalifiée ».
- **T-08 — Le rappel.** L'amendement 2 fait dire au contrôleur qu'il y a de quoi relier, à trois
  conditions, et seulement avant la première reliure. Examine : le seuil d'un tiers est-il le bon
  signal ; que voit un projet dont le carnet a regrossi après une reliure, et est-ce acceptable de
  se taire ; le rappel peut-il apparaître là où la commande refuserait d'agir.
- **T-09 — Réversibilité et répétition.** La fiche dit la coupe réversible par Git et ne construit
  pas la reliure périodique. Examine : que signifie « réversible » pour un projet qui a continué à
  travailler depuis la coupe ? Une seconde coupe plus tard rencontrerait-elle un obstacle que la
  première n'a pas rencontré ?

## 3. Posture

**Lecture seule, rapport seul.** Tu n'écris aucun fichier hors de ton rapport, tu ne lances
aucune commande, tu ne proposes pas de code rédigé, tu n'inventes aucune décision. Si une pièce
te manque pour conclure sur un thème, tu le dis nommément et tu passes au suivant.

## 4. La forme d'un constat

**Sans configuration démontrée, pas de ligne rouge.** Une remarque sans situation concrète reste
une observation et ne bloque rien.

Chaque constat porte : un identifiant (`R-01`, `R-02`, …), le thème, la sévérité
(`MAJEUR` / `MINEUR` / `OBSERVATION`), la situation exacte — état de départ, suite d'opérations,
résultat attendu, résultat obtenu —, la phrase précise du texte joint qui est en cause, l'impact,
et une correction proposée en une à trois phrases.

## 5. Hors sujet, à ne pas rediscuter

- Les chiffres de la phase de mesure : ils sont acquis.
- Le choix des noms de commandes (`decision bind`, `decision show`) : tranché par le Project Owner.
- L'ordre des trois lots, et le fait que ce lot ne touche ni à la conversation ni à l'obligation
  de lecture.
- L'application de la coupe dans les projets réels : hors périmètre, avec ses propres conditions.

## 6. Verdict — liste fermée, un seul

- `P19_CADRAGE_PASS` — la conception tient ; aucune correction nécessaire.
- `P19_CADRAGE_REQUIRES_MINOR_REDLINE` — corrections ponctuelles, la conception tient.
- `P19_CADRAGE_REQUIRES_MAJOR_REDLINE` — au moins une configuration démontrée met en défaut une
  promesse centrale.
- `P19_CADRAGE_CANONICAL_CONFLICT` — le texte contredit une règle du squelette citée dans le texte
  lui-même.
- `P19_CADRAGE_INPUT_MISSING` — une pièce indispensable manque ; dis laquelle.

Un verdict hors de cette liste est un défaut de livrable, pas une nuance.

## 7. Forme du rapport

Commence par **trois lignes en langage courant** pour le Project Owner : ce que tu as trouvé, ce
que ça change, ce qu'il doit décider. Le détail technique vient ensuite, thème par thème, puis les
constats, puis le verdict.

Un autre relecteur examine le même texte de son côté. Tu ne lis pas son rapport et il ne lit pas
le tien avant que les deux soient rendus.

---

# PARTIE B — LE TEXTE À EXAMINER, INTÉGRALEMENT

*Copie conforme de la fiche de cadrage V2 du chantier P19, reproduite sans retouche.*

---

# P19 — Deux volumes : le carnet vivant et le volume relié

*Fiche de cadrage **V2** — 15 septembre 2026. Lot 1 du chantier « alléger ce que l'IA doit lire ».
V2 = V1 + les mesures de la phase 0 + les décisions du Project Owner du 15 septembre.
Append-only : une évolution ajoute une section datée, jamais une réécriture silencieuse. La V1
reste lisible dans le projet Claude « Squelette ».*

*Numéro **P19** et version **3.20.0** : confirmés contre le dépôt (rapport de mesure, § A.1).*

---

## Résumé en trois points (pour le Project Owner)

1. **Ce qu'on construit.** Le journal des décisions est coupé en deux : un carnet vivant, relu à
   chaque démarrage, et un volume relié — les décisions figées d'avant l'adoption du squelette —
   qu'on n'ouvre qu'au besoin, avec une ligne de sommaire par décision dans le carnet.
2. **Ce que la mesure a montré.** Dans Alpha, le journal pèse 63 % de tout ce que l'IA
   doit lire avant de démarrer, et 69 % de ce journal est figé. La coupe retire environ
   30 400 jetons à chaque démarrage. L'essai grandeur nature dit que rien ne casse d'irréparable :
   trois contrôles grincent, tous réparables dans l'outil, aucun record à réécrire.
3. **Ce qui est tranché.** Construction autorisée le 15 septembre. Deux commandes :
   `decision bind` et `decision show`. Rien n'est appliqué dans Alpha tant que son
   chantier en cours n'est pas fermé.

---

## 1. Ce que la V1 disait, et qui ne change pas

Les sections 1, 2, 3, 6, 8 et 9 de la V1 restent valables mot pour mot : l'idée dans ses mots,
les deux sacs, l'ordre des trois lots, les neuf comportements B1–B9, le hors-périmètre, le chemin
de livraison. La V2 ne les recopie pas ; elle les confirme.

Rappel du seul point de doctrine qui gouverne tout le reste : **aucune décision n'est réécrite,
résumée ou requalifiée.** Le texte déplacé est identique à l'octet près. Vérifié sur 64 blocs.

---

## 2. Ce que la phase 0 a mesuré (résumé ; détail dans `RAPPORT-MESURE-P19.md`)

| Mesure | Résultat |
|---|---|
| Poids du journal dans le sac du démarrage d'Alpha | **63,1 %** (forme métier), 64,6 % (gouvernance), 47,2 % (large) |
| Journal d'Alpha | 85 décisions, 185 705 octets, ~46 400 jetons |
| Décisions figées par la baseline d'adoption | **64 sur 64 intactes**, 128 159 octets = **69,0 %** du journal |
| Carnet vivant + sommaire après la coupe | 64 040 octets (~16 000 jetons) |
| **Gain à chaque démarrage, reprise, acquittement** | **~30 400 jetons**, soit −41 % du sac total |
| Sommaire projeté | 64 lignes, 6 494 octets — 5 % du poids qu'il remplace |
| Dans le squelette lui-même | 4 décisions d'exemple : la coupe ne s'y voit pas. Confirmé |
| Essai grandeur nature sur copie jetable | 3 contrôles en échec, tous réparables dans l'outil ; **0 record à réécrire** |
| Lecture « deux volumes » | 0 référence cassée sur 78 ; exemption des décisions figées retrouvée à 64 sur 64 |
| Blocages X1, X2, X3 | **aucun déclenché** |
| Verdict | `P19_MEASURE_PASS_BUILD_MAY_START` |

Deux constats de méthode, qui commandent la construction :

- **Tous les accès au journal passent par un seul point** (`self.human_decisions`,
  `scripts/project_control.py` ligne 1921), utilisé à onze endroits. Un accesseur unique qui
  renvoie le carnet vivant plus le volume relié quand il existe couvre les onze d'un coup :
  `REUSE`, pas `REIMPLEMENT`.
- **Le volume relié sort de l'empreinte de lecture tout seul** : un fichier absent du routage
  n'entre jamais au manifeste, et le contrôle de routage ne s'en plaint pas. Aucune exemption
  nouvelle, aucune ligne ajoutée à la liste des chemins exclus.

---

## 3. Les huit décisions de la V1 — état après mesure

| # | Décision | État |
|---|---|---|
| 1 | ligne de coupe = baseline d'adoption déjà déclarée | **tenue.** `authorities_baseline` donnerait 2 décisions de plus pour 4 159 octets : écart négligeable, et la baseline d'adoption est celle dont la doctrine parle déjà |
| 2 | volume relié intact à l'octet près + sommaire dans le carnet | **tenue et démontrée** |
| 3 | seul le carnet vivant reste une autorité routée | **tenue**, et plus simple que prévu (§ 2) |
| 4 | une seule coupe pour l'instant | **tenue**, avec la précision du § 4 ci-dessous |
| 5 | la coupe est un geste du contrôleur, sur décision humaine | **tenue** ; aucune commande existante ne fait déjà cela |
| 6 | sans volume, rien ne change | **tenue** |
| 7 | seuil d'utilité : un tiers | **franchi largement** — 69,0 % |
| 8 | version 3.20.0, chantier P19 | **confirmés** contre le dépôt |

---

## 4. Décisions du Project Owner, 15 septembre 2026

**D-1 — Construction autorisée.** « Je donne mon accord pour construire ! » La construction se
fait dans la copie `~/Projets/squelette-chantier-p19/source`, branche
`claude/v3.20-deux-volumes`, et nulle part ailleurs. La livraison dans l'atelier reste un geste
séparé avec son propre double arrêt.

**D-2 — Le nom des commandes : deux mots.** « je suis ton conseil, deux mots :
`decision bind` / `decision show` ». Un seul mot entre au vocabulaire — `decision` — avec deux
sous-verbes, sur le modèle d'`idea add` / `idea set`. `decision bind` relie ; `decision show`
ouvre un chapitre, dans l'un ou l'autre volume.

**D-3 — Alpha attend la fin de son chantier.** « Alpha est en pause sur un chantier en
cours ! Il serait judicieux d'attendre la fin du chantier avant de faire des modifications
dedans. » Rien n'est appliqué dans Alpha dans ce chantier — c'était déjà le
hors-périmètre de la V1 — et l'application future attendra **trois** conditions au lieu de deux :
la promotion de la 3.20.0, **la clôture du chantier en cours d'Alpha**, et un double
arrêt propre. Écrit ici pour que ça ne se perde pas.

**D-4 — Le tableau de bord corrigé.** « Corriger A.2 » : le bloc saisi à la main de la feuille de
route annonçait la 3.19.1, Alpha en 3.18.1 et 164 essais. Corrigé dans la copie,
commit `5b1204c`, vue régénérée. Ce bloc n'est pas régénéré automatiquement — c'est une limite
connue, pas un défaut de ce chantier.

**D-5 — Redaction Human : écarté.** « Si tu me proposes l'accès en lecture à mes décisions, cela
ne m'intéresse pas plus que cela. » Aucune mesure sur ce projet, aucun accès demandé.

**D-6 — Le journal du squelette lui-même : dette écrite, rien de plus.** Le journal des décisions
du squelette (196 249 octets) n'est obligatoire pour personne : il n'est pas routé. Deux lectures
possibles — c'est normal (le squelette est un moule, pas un projet gouverné), ou c'est un trou.
Rien n'est décidé ; la question est inscrite comme dette connue et revient après le lot 2, quand
le paquet rendra cette lecture bon marché.

**D-7 — La périodicité.** *En attente de sa réponse.* La coupe est un geste unique par projet ;
le carnet vivant se remplit à nouveau. Trois voies ont été posées : manuel (on oublie),
automatique (refusé par Claude : déplacer du texte de gouvernance sans décision humaine
contredit tout le reste du squelette), ou **l'outil rappelle et l'humain décide**. Recommandation
de Claude : le rappel. Sans réponse, la version est livrée sans rappel, et l'ajout reste possible
plus tard sans rien défaire.

---

## 5. Ce que la construction fait, dans l'ordre

1. **Un accesseur unique** pour le texte des décisions : carnet vivant seul quand il n'y a pas de
   volume, carnet vivant + volume relié sinon. Les onze points de lecture passent par lui. Les
   **écritures** continuent de viser le seul carnet vivant.
2. **`decision bind`** — la coupe, sous décision humaine : déplace les blocs figés, écrit le
   sommaire, classe le nouveau chemin, committe elle-même sur la branche canonique comme les
   autres records administratifs. Refuse si un seul bloc diffère de sa forme à la baseline, si une
   seule référence cesserait de se résoudre, ou s'il n'y a pas de baseline.
3. **`decision show`** — ouvre un chapitre, dans l'un ou l'autre volume, sans rien écrire.
4. **`DECISION_VOLUMES_CONSISTENT`** — le contrôle d'audit : blocs reliés identiques à leur forme
   à la baseline, sommaire complet, aucune décision en double, aucun bloc relié postérieur à la
   ligne de coupe.
5. **L'empreinte de lecture** : le volume n'est pas routé, donc il n'entre pas au manifeste ; le
   carnet vivant, sommaire compris, y reste.
6. **`status`** dit combien de décisions sont vivantes et combien sont reliées, en français et en
   anglais, par le catalogue de phrases. Les refus restent en anglais, comme tous les autres.
7. **La doctrine** : `AGENTS.core.md`, `project_control/README.md`, `FIRST_START.md`.
8. **Neuf essais**, un par comportement, chacun vérifié rouge avant et vert après.

---

## 6. Ce qui reste interdit, sans changement

Écrire dans l'atelier, dans Alpha ou dans Redaction Human ; pousser ; taguer ;
supprimer un dossier ou un fichier utile ; inventer une décision humaine ou un numéro de journal ;
requalifier une décision ; modifier les attentes d'un essai existant pour le faire passer.

---

## 7. Journal de la fiche

- **V1** — 15 septembre 2026, écrite depuis le projet Claude « Squelette ».
- **V2** — 15 septembre 2026, après la phase 0 : mesures intégrées (§ 2), les huit décisions de
  la V1 confirmées (§ 3), sept décisions du Project Owner ajoutées (§ 4), plan de construction
  arrêté (§ 5). Aucune décision de la V1 n'est barrée.

---

## Amendement 1 — la ligne de sommaire cite et marque sa coupe (15 septembre 2026, après construction)

**Ce que la construction a trouvé.** La décision 2 disait : une ligne de sommaire portant « la
première ligne du champ `Chosen option` recopiée telle quelle ». Appliquée au vrai journal de
Alpha, dans un clone jetable, cette règle produit un sommaire de **97 438 octets — 63 %
du carnet vivant qu'il est censé alléger**, une ligne atteignant 12 212 octets. Le gain tombe de
65 % à 17 % du journal : le chantier ne tient plus sa promesse, et passe sous le seuil d'utilité de
la décision 7.

La cause n'est pas le champ `Chosen option` (19 673 octets au total) mais le champ `Decision`
(75 479 octets) : dans un projet réel, ces champs sont des paragraphes écrits sur une seule ligne,
pas des titres. Un sommaire qui les recopie entiers n'est plus un sommaire.

**Ce qui est décidé, sous la responsabilité de Claude.** La ligne de sommaire **cite** le début de
chaque champ, mot pour mot, et **marque sa coupe** : `Decision` à 120 caractères, `Chosen option` à
60, suivis de `[…]` lorsque le texte continue. Aucun mot n'est changé, rien n'est reformulé, rien
n'est réordonné, rien n'est requalifié — la coupe est mécanique, visible, et le texte enregistré
reste à une commande de distance (`decision show HD-NNN`). Un essai le vérifie : une décision
écrite sur une très longue ligne produit une ligne de sommaire courte et marquée, le volume garde
son texte entier, et la commande d'ouverture le rend intégralement.

**Ce que ça donne sur le vrai journal**, mesuré après la coupe réelle dans le clone jetable :
sommaire de 11 430 octets pour 64 décisions (17 % du carnet vivant, ligne la plus longue :
230 octets), carnet vivant ramené de 186 333 à **68 958 octets**, audit `23 PASS / 0 FAIL`.

**Ce que le Project Owner peut renverser d'un mot** : les deux longueurs (120 et 60), ou le
principe même de la coupe s'il préfère un sommaire qui ne porte que le numéro et la date.

---

## Amendement 2 — le rappel, et les deux dettes écrites (15 septembre 2026)

**Décision du Project Owner : « Je valide le rappel ! » et « Question 3 : on écrit comme dette ! »**

**Le rappel.** Le contrôleur signale qu'il y a de quoi relier ; il ne relie jamais de lui-même.
Trois conditions réunies, et pas une de moins : aucun volume n'existe encore, une baseline
d'adoption est déclarée, et les décisions figées pèsent **au moins un tiers** du registre — le
seuil d'utilité du Project Owner lui-même (décision 7). `status` ajoute alors une ligne, en
français et en anglais, qui nomme la commande. Une fois la reliure faite, cette ligne cède la place
au décompte des deux volumes.

Le rappel n'apparaît **que là où la commande existe**. C'est délibéré : après une première reliure,
`decision bind` refuse d'agir, parce que relier une seconde fois demanderait de déplacer la ligne
de coupe. Signaler « il serait temps de relier à nouveau » désignerait une porte qui ne s'ouvre
pas. La voie automatique reste écartée — déplacer du texte de gouvernance sans décision humaine
contredit tout le reste du squelette.

**Les deux dettes**, écrites dans `provenance/roadmap-template.v1.json`, section « plus tard » :

1. **Le journal du squelette lui-même n'est obligatoire pour personne.** `provenance/CHANGELOG.md`
   (196 249 octets, plus gros que celui d'Alpha) n'est routé nulle part : un agent qui
   travaille sur le squelette peut commencer sans l'avoir ouvert. Normal pour un moule, ou trou —
   rien n'est tranché. Le rendre obligatoire coûterait environ 49 000 jetons par chantier. À
   reprendre après le lot 2, qui rendra cette lecture bon marché.
2. **Relier une seconde fois.** Le carnet vivant se remplit à nouveau ; déplacer la ligne de coupe
   est une décision humaine et une mécanique que cette version ne construit pas.

**Ce que ça change à la décision 6** (« sans volume, rien ne change ») : un projet sans volume
**et sans rien à relier** ne voit aucune différence. Un projet qui a de quoi relier voit une ligne
de plus dans son état — c'est le rappel, et c'est voulu.
