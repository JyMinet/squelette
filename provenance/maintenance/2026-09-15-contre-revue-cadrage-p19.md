> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Contre-revue de la relecture de cadrage — P19 « Deux volumes »

*15 septembre 2026. Contre-vérification, par Claude, de la relecture indépendante rendue sur la
fiche de cadrage V2 (verdict `P19_CADRAGE_REQUIRES_MAJOR_REDLINE`, neuf constats R-01 à R-09).*

*Objet contre-vérifié : le rapport de relecture. Objet de référence : le code réellement construit
sur `claude/v3.20-deux-volumes`, que le relecteur n'avait pas — il le dit lui-même et s'interdit
d'en tirer des conclusions. Chaque constat a été rejoué contre ce code, dans des dépôts jetables
montés par la suite d'essais.*

---

## Résumé en trois points (pour le Project Owner)

1. **La relecture est juste, et son constat principal est un vrai trou.** Le contrôle vérifiait
   que tout ce qu'il retrouvait était en ordre, sans jamais compter ce qui devait être là. J'ai
   reproduit la disparition : une décision reliée que personne ne cite s'efface avec sa ligne de
   sommaire, et tous les contrôles restent verts. C'est corrigé, avec son essai.
2. **Sept constats sur neuf sont retenus et traités**, dont cinq corrigés dans le code. Deux ne
   sont pas des défauts : la protection contre une reliure à moitié écrite existait déjà, et une
   décision reliée n'autorise rien de neuf — je l'ai vérifié en essayant de créer un chantier qui
   la cite, et l'outil refuse.
3. **Rien à décider de ta part.** Aucune correction ne change la ligne de coupe, les commandes, ni
   ce que tu as tranché. Le nombre d'essais passe de 177 à 181.

**Verdict : `P19_REVIEW_OF_CADRAGE_PASS`** — la relecture tient ; aucun de ses constats n'est
rejeté, et sa ligne rouge majeure est fondée.

---

## A. Préflight

| Objet | État |
|---|---|
| Rapport contre-vérifié | relecture de cadrage P19, neuf constats, verdict `P19_CADRAGE_REQUIRES_MAJOR_REDLINE` |
| Code de référence | `squelette-chantier-p19/source`, branche `claude/v3.20-deux-volumes`, état à `e369e65` au début de la contre-vérification |
| Méthode | chaque scénario rejoué dans un dépôt jetable monté par la suite d'essais ; aucune écriture hors de la copie |
| Atelier, Alpha | non touchés |

**Une remarque de méthode, à porter au crédit du relecteur.** Il distingue partout ce qu'il
démontre de ce qu'il ne peut pas vérifier faute de code, et refuse d'appeler défaut ce qui n'est
qu'une absence dans la pièce qu'on lui a donnée. Deux de ses observations tombent d'ailleurs
précisément parce que le code fait ce que la fiche ne disait pas.

---

## B. Les neuf constats, un par un

### R-01 — La conservation exhaustive n'est pas exprimée — **MAJEUR — CONFIRMÉ, corrigé**

**Rejoué.** Un projet relié dont cinq décisions (`HD-120` à `HD-124`) ne sont citées par aucun
enregistrement. Audit vert. On retire `HD-122` du volume et sa ligne du sommaire. Résultat :
**audit vert**. Une décision a disparu et rien ne le voit.

C'est exactement le scénario décrit. La cause est celle qu'il nomme : les invariants partaient du
volume présent, jamais de l'ensemble attendu. Le contrôle des références ne rattrapait rien,
puisque personne ne citait cette décision.

**Corrigé.** Le volume nomme désormais, sur sa propre ligne, le commit auquel il a été relié. Le
contrôle part de l'ensemble des décisions enregistrées à **cette** origine et exige que chacune
soit encore quelque part — dans le volume, ou revenue dans le carnet vivant. Rejoué après
correction : `FAIL — recorded at the binding origin and no longer in either volume: HD-122`.

**À noter, et ce n'est pas à sa décharge :** ce trou existait déjà avant les deux volumes. Sur la
`3.19.2`, supprimer du registre une décision que personne ne cite passait aussi l'audit. La coupe
ne crée pas le défaut ; elle le rend plus grave, parce qu'un volume que personne ne lit au
démarrage ne sera pas non plus remarqué à l'œil. La correction ferme les deux cas.

### R-02 — Un sommaire complet n'est pas nécessairement fidèle — **MINEUR — CONFIRMÉ, corrigé**

**Rejoué.** Ligne de `HD-101` remplacée par `- HD-101 (1999-01-01) — CECI N'EST PAS LA DÉCISION
ENREGISTRÉE — REJET`. Blocs reliés intacts, chaque identifiant a sa ligne. Résultat : **audit
vert**.

**Corrigé.** Le contrôle reconstruit chaque ligne à partir du bloc relié et la compare
littéralement. Rejoué : `FAIL — summary lines do not quote the decision they name: HD-101`.

Il a raison de souligner la conséquence : une empreinte correcte du carnet aurait prouvé la
lecture d'une attribution fausse.

### R-03 — Origine de comparaison après retrait ou avancement — **MINEUR — partiellement confirmé, corrigé**

**Retrait de la déclaration** : déjà traité avant sa relecture — l'audit échouait avec un message
explicite. Non reproduit comme défaut.

**Avancement de la baseline** : confirmé. Le contrôle comparait à la déclaration du jour. Après un
avancement légitime, il accusait les six décisions reliées d'être « bound but not recorded at the
adoption baseline » — un échec trompeur, qui désigne le volume alors que c'est la ligne de
référence qui a bougé.

**Corrigé.** L'origine est épinglée dans le volume et c'est elle qui sert de comparaison. Un
avancement est désormais **signalé, pas sanctionné** : `bound at dd44bba; adoption baseline now
declared at fd587e6`. Un retrait reste un échec explicite qui nomme l'origine réelle. Origine non
nommée ou illisible : échec explicite également.

### R-04 — L'extrait peut porter un sens opposé — **MINEUR — retenu, corrigé dans le texte**

Il ne conclut pas à une requalification, et il a raison : le texte canonique reste entier. Le
risque qu'il décrit est réel : un préfixe littéralement exact peut donner l'impression inverse de
la décision, et le marqueur annonce une omission sans en dire la portée.

**Corrigé.** Le sommaire porte désormais, en tête, une phrase qui dit ce qu'il est : *« Ces lignes
sont des repères, pas des décisions. Une ligne coupée ne dit pas ce qui vient après : une réserve,
une négation ou un refus peuvent s'y trouver. Seul le texte conservé énonce le choix humain. »* La
doctrine le redit. L'identifiant reste ce qui distingue deux décisions au début identique.

L'option « numéro et date seulement » qu'il rappelle reste ouverte ; elle coûte la lisibilité du
sommaire, et c'est au Project Owner de trancher s'il la préfère.

### R-05 — Le seuil change de grandeur — **MINEUR — CONFIRMÉ, corrigé dans le texte**

Exact. La part du registre occupée par les blocs figés et l'économie nette après remplacement par
le sommaire ne sont pas la même chose, et les deux étaient présentées comme « le seuil d'un
tiers ».

**Corrigé.** La grandeur est nommée : le rappel mesure la **part brute occupée par les blocs
figés**, et l'annonce comme un potentiel, jamais comme une économie garantie d'un tiers.

### R-06 — Le rappel peut précéder un refus normal — **OBSERVATION — CONFIRMÉ, corrigé dans le texte**

**Rejoué.** Un bloc figé réécrit après la baseline : le rappel s'affiche, et la commande refuse.
Les deux à la fois, comme il l'annonce.

**Corrigé.** Le rappel dit maintenant : *« reliure possible, sous réserve de ses contrôles :
decision bind »*. Je n'ai pas ajouté la vérification d'intégrité complète au rappel : il tourne à
chaque `status`, et lui faire relire l'intégralité des blocs à chaque affichage ferait payer à tout
le monde le coût qu'on essaie précisément de retirer.

### R-07 — Protection contre une reliure à moitié écrite — **OBSERVATION — ce n'est pas un défaut**

Il ne peut pas se prononcer faute de contrat reproduit, et il le dit. Vérification : la commande
réutilise la mécanique transactionnelle existante, celle de toutes les écritures administratives —
écriture sous transaction, vérification, commit, et retour complet à l'état antérieur si l'une des
trois échoue, y compris l'annulation du commit déjà fait. Un refus ne laisse pas une demi-reliure.

**Traité** : c'est désormais écrit dans la doctrine, puisque son absence de la fiche était le
problème.

### R-08 — Frontières d'un bloc — **OBSERVATION — retenu, écrit**

Exact : la fiche ne définissait pas les bornes d'un bloc. Le code réutilise la fonction de découpe
existante du contrôleur, inchangée, celle-là même qui sert à toutes les lectures de décisions
depuis l'origine — la reliure n'invente pas son propre découpage.

**Traité** : les bornes sont écrites dans la doctrine — un bloc va de son titre au titre suivant ou
à la fin du fichier, lignes vides comprises, et c'est ce texte qui est comparé.

### R-09 — Retrouvée, admissible, lue — **OBSERVATION — ce n'est pas un défaut, et c'est désormais prouvé**

**Rejoué**, dans les deux sens :

- un enregistrement figé à la baseline qui cite une décision reliée écrite dans le vocabulaire de
  son temps : audit vert, l'exemption suit la décision dans son volume ;
- un chantier **créé aujourd'hui** qui cite la même décision : **refusé** — *« Chosen option is not
  AUTHORIZE »* — et aucun enregistrement n'est écrit.

Vivre dans un volume ne crée donc aucune exemption. Sa distinction entre retrouvée, admissible et
lue est juste, et un essai apparié la garde désormais.

Sur la preuve de lecture, il a également raison, et c'est le prix assumé de ce chantier : après la
coupe, la preuve atteste la lecture du carnet vivant et de son sommaire, jamais celle du texte
conservé dans le volume. C'est écrit dans la doctrine, sans lui prêter une portée plus large.

---

## C. Ce qui a changé dans le code

| Correction | Constat |
|---|---|
| Le volume nomme le commit auquel il a été relié ; c'est lui, et non la déclaration du jour, qui sert de comparaison | R-01, R-03 |
| Le contrôle part de l'ensemble des décisions enregistrées à cette origine et exige que chacune soit encore présente | R-01 |
| Chaque ligne de sommaire est reconstruite depuis le bloc relié et comparée littéralement | R-02 |
| Avancement de la baseline signalé, retrait et origine illisible : échecs explicites | R-03 |
| Le sommaire dit qu'il est un repère, pas une décision | R-04 |
| Le rappel nomme la grandeur qu'il mesure et annonce un potentiel sous réserve des contrôles | R-05, R-06 |
| Doctrine : transaction, bornes d'un bloc, absence d'exemption, portée de la preuve de lecture | R-07, R-08, R-09 |

**Quatre essais nouveaux**, chacun vérifié rouge sur la `3.19.2` **et** sur la `3.20.0` d'avant
correction, vert après : la disparition d'une décision que personne ne cite, la ligne de sommaire
mal attribuée, l'origine épinglée (avancement puis retrait), et le couple ancien/nouvel
enregistrement. **181 essais au total, tous verts.**

## D. Ce qui n'a pas changé, et pourquoi

- La ligne de coupe reste la baseline d'adoption déjà déclarée.
- Les deux commandes gardent leurs noms.
- La reliure périodique n'est pas construite : elle reste une dette écrite, comme il le relève
  lui-même sans en faire une exigence.
- Le seuil d'un tiers n'est pas renégocié : c'est une décision du Project Owner.

## E. Verdict

```
P19_REVIEW_OF_CADRAGE_PASS
```

La relecture tient. Aucun de ses neuf constats n'est rejeté ; sept sont retenus et traités, deux
sont établis comme n'étant pas des défauts du code — ce que le relecteur avait explicitement laissé
ouvert faute de pièce. Sa ligne rouge majeure était fondée et est fermée.

---

## F. Journal

- V1 — 15 septembre 2026. Append-only : une correction crée une révision liée, jamais une
  réécriture silencieuse.
