> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

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

---

## Amendement 3 — après la relecture indépendante (15 septembre 2026)

Une relecture indépendante de cette fiche a rendu `P19_CADRAGE_REQUIRES_MAJOR_REDLINE` avec neuf
constats. La contre-vérification (`2026-09-15-contre-revue-cadrage-p19.md`, verdict
`P19_REVIEW_OF_CADRAGE_PASS`) ne rejette aucun constat. Ce que la fiche dit désormais :

**Le contrat d'intégrité part du compte de départ, pas des survivants (R-01, majeur).** Vérifier
que chaque bloc retrouvé est intact laissait une décision que personne ne cite disparaître avec sa
ligne de sommaire, tous contrôles verts — reproduit. Le volume **nomme le commit auquel il a été
relié**, et le contrôle exige que chaque décision enregistrée à cette origine soit encore quelque
part, dans l'un ou l'autre volume. Ce trou existait déjà avant les deux volumes ; la correction
ferme les deux cas.

**Le sommaire doit être fidèle, pas seulement complet (R-02).** Chaque ligne est reconstruite
depuis le bloc relié et comparée littéralement : une ligne peut porter le bon numéro et citer
autre chose.

**L'origine de comparaison est épinglée (R-03).** Jamais la baseline déclarée aujourd'hui : elle
peut légitimement avancer. Un avancement est signalé ; un retrait, une origine non nommée ou
illisible sont des échecs explicites.

**Le sommaire dit ce qu'il est (R-04).** Ses lignes sont des repères, pas des décisions : coupées,
elles ne disent pas ce qui suit — une réserve, une négation, un refus peuvent s'y trouver. Seul le
texte conservé énonce le choix humain.

**Le seuil nomme sa grandeur (R-05, R-06).** Le rappel mesure la part brute occupée par les blocs
figés, pas l'économie nette, et annonce un potentiel sous réserve des contrôles de la commande —
laquelle peut refuser, par exemple si un bloc figé a été réécrit.

**Trois points étaient absents de la fiche, pas du code (R-07, R-08, R-09)** : la reliure est une
transaction ordinaire et un refus ne laisse pas de demi-reliure ; les bornes d'un bloc vont du
titre au titre suivant ou à la fin du fichier ; et vivre dans un volume ne crée aucune exemption —
un chantier créé aujourd'hui qui cite une décision reliée est refusé si elle ne satisfait pas les
règles du jour, ce qui a été vérifié. La preuve de lecture, après la coupe, atteste le carnet
vivant et son sommaire, jamais le texte du volume : c'est le prix assumé du chantier, et il est
écrit.

**Ce qui ne change pas** : la ligne de coupe, les noms des commandes, le seuil d'un tiers, et le
fait que la reliure périodique reste une dette. Quatre essais de plus — 181 au total.
