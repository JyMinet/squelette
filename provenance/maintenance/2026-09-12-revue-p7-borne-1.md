> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

P7_BORNE_REVUE_REQUIRES_MAJOR_REDLINE

# Revue P7 — choix de la borne d’éligibilité — contrôleur 1

12 septembre 2026. Revue des intentions, sans prototype ni décision de conception. Un seul rapport ; aucune lecture du livrable du second contrôleur.

## 1. Résumé en trois points

1. Le dossier permet la revue, mais deux assurances du rapport initial sont trop fortes : une fiche peut entrer dans l’empreinte de lecture dans une configuration acceptée ; rendre un champ facultatif dans le schéma ne garantit pas que l’audit acceptera les anciens chantiers.
2. La marque posée à la création est la solution la plus simple pour le parcours ordinaire. Elle reste une recommandation conditionnelle : les fiches importées ou écrites à la main, le premier départ par une reprise et les installations interrompues doivent avoir une règle explicite. La décision humaine offre une autre voie, avec une procédure d’adoption plus lourde. La déduction depuis l’historique reste la moins robuste.
3. Le propriétaire doit faire corriger ces affirmations puis trancher la conception avant construction. La copie source est intacte. Les essais et leurs traces restent dans le dossier jetable prévu.

## 2. Préflight

**Périmètre :** `~/Projets/squelette-revue-p7`, exclusivement. E1 et E2 sont présents dans `entrees/`. `source/` est une copie sans `.git`, conformément au LISEZ-MOI. Les deux noms de livrable étaient absents au contrôle initial ; `REVUE_P7_BORNE-1.md` a aussi été vérifié absent juste avant rédaction.

**Version et commit :** le manifeste annonce `3.19.1`. Le commit de cette archive n’est pas attestable sans ses objets Git. E2 annonce avoir mesuré le HEAD `ebf62f4f46da2a1c5f02f57abd997482033148d2` ; ce SHA n’est pas présenté ici comme un commit vérifié de `source/`. Les empreintes du contrôleur et du schéma correspondent exactement à E2, et les **24 entrées du manifeste** sont conformes selon `core_digest`. Cela confirme les objets techniques mesurés, pas l’identité Git de tout l’arbre. L’absence d’historique, annoncée, ne constitue pas un préflight non conforme.

| Objet | SHA-256 |
|---|---|
| `MANDAT-REVUE-P7-BORNE.md` | `3dc14ae0cef2e95525e3ab9c96903bb7668b914c4f0aa51a4555563fd1a60046` |
| `entrees/mandat-construction-p7-etape-1.md` | `832cba09e5487ff4d24ca874877ead307b71b6c67631f0f7ebd954b369995a2f` |
| `entrees/D1-rapport-mesure-phase-0-P7-etape-1.md` | `ae2ef9efe66b911d5a9905b66c4cf908d43daafd403ec5212936dcc7c0f570fd` |
| `source/scripts/project_control.py`, 6 514 lignes | `3d3e76de08d347467a8843930ac53066f74f37baa783384fbd1c6f10e4d349f0` |
| `source/project_control/schemas/work-item.v1.schema.json` | `52423cacc127ccb60bb8ffd638172033d9b4251b6be08f587f4f0e685f09afd0` |
| Arbre `source/`, avant et après, 125 fichiers | `ddfaf9f9d7b3e37bf8fa7b762f2f419277c0af66b676d620f5ff028b616a5854` |

Empreinte d’arbre : fichiers triés par chemin relatif ; SHA-256 de la concaténation, pour chacun, de son chemin UTF-8, un octet nul, ses octets, un octet nul. Les fichiers cachés sont inclus. `FIRST_START.md` nécessite la normalisation documentée de son marqueur d’initialisation (`source/scripts/project_control.py:141–153`) pour comparer au manifeste ; son SHA brut différent n’est pas une anomalie.

**Méthode et limites.** Lectures des sources, analyse syntaxique Python, appels des fonctions existantes sur copies et données d’essai sous `runs/revue-1/`. Python a été lancé avec `-B`. Aucun code du contrôleur ni schéma sur disque n’a été modifié. Les variantes de schéma sont uniquement des données en mémoire pour reproduire les mesures demandées. Les données fictives sont identifiées par la mention imposée dans le README du répertoire, les journaux et la décision fictive.

Aucun accès au dépôt original, aucune opération réseau, aucun commit, aucune création de branche ou de tag. La découverte Git des essais est bornée au dossier accordé. Les **164 tests déclarés** dans `tests/test_template.py` ont été comptés, mais la suite n’a pas été exécutée : elle fabrique des historiques et des commits, interdits par ce mandat. Le résultat « 164 verts » d’E2 n’est donc pas revalidé ici. Les fonctions appelées et sorties utiles figurent dans `runs/revue-1/mesures.txt` et `scenarios.txt`.

Les restrictions du mandat de construction non renseigné concernent sa future exécution, pas la présente revue, expressément autorisée par le mandat de revue. Aucun droit de construction n’en a été déduit.

Dans la suite, **PC** désigne `source/scripts/project_control.py`. Les plages de lignes se rapportent toujours à cette copie. Les analyses d’options futures sont des observations de conception, sauf lorsqu’un constat précise une expérience effectivement exécutée sur le contrôleur actuel. Aucun échec futur de P7 n’est présenté comme un test exécuté.

## 3. T-01 — Les sept mesures

### B.1 — Empreinte de lecture : partiellement confirmée

Les trois mesures du routage fourni sont reproduites :

| Chemins autorisés | Scopes | Documents | Fiche incluse |
|---|---|---:|---|
| `scripts/`, `project_control/` | development, runtime | 22 | non |
| `docs/governance/` | governance | 12 | non |
| `applications/` | development | 12 | non |

PC:232–248 calcule les scopes ; PC:3435–3458 construit le manifeste. Les neuf exclusions de PC:93–102 sont des **chemins exacts** : aucun préfixe n’exclut `project_control/work-items/`.

**Contre-exemple exécuté.** Dans une copie, placer la fixture fournie sous `project_control/work-items/WI-001.json`, puis ajouter ce chemin à `base` du routage. `DOCUMENT_ROUTING` reste `PASS` : son contrôle, PC:2055–2072, accepte ce fichier. Calculer l’empreinte, ajouter une propriété `prior_art` à cette fiche fictive, recalculer :

```text
B1.custom.route_present = true
B1.custom.routing_check = [{"detail": "all authorities resolve inside core", "status": "PASS"}]
B1.custom.digest_before = "1daaa5db9f6a614bd0d1edf06862146de41c5e4ecf2746e65957d63e9ea38e47"
B1.custom.digest_after = "bcfb1f94e7da856bbd99e2f3cd715e2068d0d8cf9b36b47f38d8c2058ce2260c"
B1.custom.digest_changed = true
```

Cette expérience prouve l’inclusion et la péremption de l’empreinte. Elle ne prétend pas rendre l’audit complet du projet fictif vert : la fixture n’est pas un projet initialisé, et le schéma actuel refuse encore `prior_art`.

**Correction :** « Le record n’entre pas dans l’empreinte avec le routage fourni. Cette propriété n’est pas garantie par le contrôleur pour tous les projets. » Le premier blocage d’E1 n’est pas déclenché dans la configuration source, mais sa non-occurrence générale n’est pas acquise. Pour un projet ayant ce routage, E1 exige un arbitrage de conception ; la revue ne choisit pas comment modifier l’empreinte. Le changement du schéma routé modifie bien l’empreinte du scope development.

### B.2 — Record et schéma : partiellement confirmée

Emplacement, schéma fermé, validateur interne et remontée à `SCHEMA_VALIDATION` sont confirmés : PC:1236, 1388, 2004–2015, 2089–2090, 2984–3011.

Deux corrections factuelles :

- **31 champs obligatoires, 33 propriétés**, et non 30/32. Comptage direct des tableaux JSON ; `source/project_control/schemas/work-item.v1.schema.json:7–40`. Les deux propriétés facultatives sont bien `close_head` et `block_records`.
- Tous les champs ne viennent pas d’options CLI. La création reçoit les informations de l’appelant et génère notamment le statut `AUTHORIZED`, `start_head: UNKNOWN`, les références et collections initiales (PC:4792–4827 ; parseur à partir de 6189).

### B.3 — Baselines et anciens records : partiellement confirmée

Deux baselines nommées, et aucune borne de version P7, sont présentes dans `BASELINE_DECISION_FIELDS` (PC:37–40). Leur validation exige un commit existant, ancêtre de HEAD, et une décision qui le nomme exactement (PC:5533–5588, 5633–5660). `template-upgrade` écrit cœur et manifeste, sans enregistrer de commit d’adoption (PC:3953–3964).

Les trois expériences de schéma d’E2 sont reproduites exactement :

```text
record avec prior_art, schéma actuel : work-item: unexpected property prior_art
record ancien, propriété ajoutée mais facultative : []
record ancien, propriété globalement required : work-item: missing prior_art
```

Mais **« chemin audit couvert, sans aucune baseline » n’en découle pas**. Deux contre-exemples actuels, sur fixtures et fonctions intactes :

```text
Agent Run sans authorities_read :
  core_schema_errors = []
  validate_agent_run = []
  agent_run_authority_errors = authorities_read is required after the adoption baseline…

Work Item DONE sans close_head :
  core_schema_errors = []
  validate_work_item = []
  done_evidence_errors = WI-001: close_head is missing or not in current history
```

Dans le second cas, l’absence de `close_head` suffit au refus, avant toute recherche d’objet Git. Références : PC:2998–3018, 3572–3593, 5795–5809. De plus, `validate_work_item` possède sa propre liste de champs exigés, PC:1393–1403. Une future obligation inconditionnelle placée à l’un de ces niveaux requalifierait les anciens records malgré un schéma permissif. Aucune obligation `prior_art` n’existe actuellement à ces niveaux : c’est la conclusion de suffisance d’E2 qui est réfutée.

**Correction :** ne pas ajouter `prior_art` aux obligations globales du schéma commun ; cela assure seulement la compatibilité structurelle de l’absence. Appliquer aussi l’éligibilité commune à toutes les règles sémantiques. « Jamais dans required » n’est pas un théorème général sur tous les schémas : il pourrait exister des schémas sélectionnés selon le contexte, mais ce n’est pas l’architecture actuelle et ce serait une règle supplémentaire. Le validateur actuel refuse les mots-clés conditionnels tels que `if` (PC:1238–1243, expérience reproduite).

L’écart entre adoption initiale et montée n’est pas nécessairement peuplé de chantiers, contrairement à la formulation universelle d’E2. Le risque apparaît **lorsqu’un chantier a effectivement été ouvert dans cet intervalle**. Cela suffit à montrer pourquoi les baselines actuelles ne répondent pas à la question P7.

### B.4 — Status : partiellement confirmée

Les lignes affichées et le catalogue FR/EN sont confirmés, PC:307–319 et 6429–6442. L’insertion après les vérifications manquantes est cohérente.

La condition du précédent `authorities` est toutefois plus restrictive que la description : cette valeur n’est construite que pour un chantier `IN_PROGRESS`, et sans échec d’audit (PC:5870–5876). B10 exige au contraire de montrer `UNKNOWN` **avant le premier départ**, quand la réponse manque. Il faut donc compléter aussi le constructeur de vues, PC:5859–5864, et ne pas recopier la condition de la preuve de lecture.

`UNKNOWN` reste une valeur d’affichage ; ce n’est jamais une troisième réponse autorisée de `prior_art.status`.

### B.5 — Audit supplémentaire : partiellement confirmée

Le passage par `project_control_errors` puis `SCHEMA_VALIDATION` existe bien. Un nouveau nom de contrôle n’est pas nécessaire pour intégrer des règles sémantiques.

Cependant, le précédent de lecture ne fournit pas à lui seul le bon contrat : `start` et `resume` réclament une empreinte courante (PC:4928, 5314), et `close` recontrôle les autorités courantes (PC:5931–5935). Le test existant `source/tests/test_template.py:3855–3900` documente même un audit rendu vert par une baseline, suivi d’une clôture refusée pour absence de preuve courante. Ce test a été lu, pas exécuté.

P7 exige un autre partage : complétude applicable au premier départ ; après celui-ci, présence, structure et intégrité de la déclaration, **sans revalider l’existence actuelle des chemins**. Un horodatage ne garantit pas, à lui seul, que le reste de la déclaration n’a pas changé. Le mécanisme de gel doit être spécifié. B9 est donc bien une contrainte, pas une propriété acquise par réemploi du contrôle de lecture.

### B.6 — Nommage : partiellement confirmée

La convention anglaise en majuscules et séparateurs `_` est confirmée. `PRIOR_ART_DECLARED` la respecte ; son ajout n’est pas nécessairement requis.

Le nombre 58 est faux pour l’ensemble des contrôles. L’analyse AST reproduite trouve **65 noms littéraux distincts** passés à `add`. Cinq noms supplémentaires proviennent des appels dynamiques : `WORK_BRANCH_AUTHORIZED_PATHS` (PC:4244), `BASELINE_CHANGE_MANDATED` (PC:4286), et `AUTHORITY_MANIFEST_PRESENT`, `_COMPLETE`, `_CURRENT` (PC:6129–6132), soit **70 noms distincts émis via `add`**. Ce périmètre exclut les codes imprimés autrement, par exemple `INVALID_RECORDS` à la ligne 6509.

Un comptage limité aux appels `add(findings, …)` sur une seule ligne peut expliquer 58 ; l’origine exacte de l’erreur d’E2 n’est pas attestée. Les refus de commande restent des messages anglais.

### B.7 — Nombre de chantiers : confirmée

Zéro JSON dans `source/project_control/work-items/`, seulement son README. L’état est `PROJECT_TEMPLATE`, `NOT_STARTED`, les deux baselines nulles (`source/project_control/project-state.v1.json:4–16`).

On ne peut donc pas observer une population historique de chantiers dans cette copie telle quelle. La suite comporte 164 tests déclarés. Les fixtures et copies sous `runs/` sont aussi des supports de mesure : les tests existants ne constituent pas l’unique possibilité autorisée.

## 4. T-02 — Option A en usage courant

**Lecture retenue :** une marque représente l’origine du chantier dans le projet concerné. Ce sens doit être écrit ; ni `base_head`, fourni à la création, ni `start_head`, posé au départ, ne prouvent cette origine (PC:4720–4722, 4800–4806, 4933–4935).

Les conséquences futures de la table sont des observations : aucune option A n’a été implémentée dans cette revue.

| Situation | Résultat attendu de la marque seule | Réponse fausse possible / précision nécessaire |
|---|---|---|
| Chantier ouvert avant la montée, repris après | Absence de marque conservée : exemption correcte. La montée actuelle ne touche pas les records (PC:3826–3828, 3953–3957). | Un rattrapage de la marque lors de la reprise rendrait un ancien chantier éligible. Il faut interdire toute reclassification à la reprise ou à la clôture. |
| Création, blocage, reprise des semaines après | La marque doit rester celle de l’ouverture ; le temps écoulé ne compte pas. | **Le premier départ peut être `resume`** : `block` accepte `AUTHORIZED` (PC:5040–5064), `resume` peut poser le premier `start_head` et créer le premier run (5257–5260, 5298–5331). Un contrôle limité à la sous-commande `start` épargnerait ce nouveau chantier. |
| Fiche importée ou écrite à la main | Une fiche neuve sans marque ressemble à une fiche ancienne locale. | Faux négatif si un nouvel import est exempté faute de marque ; faux positif si une vieille fiche du même projet récupère une marque étrangère lors d’une restauration. Il faut distinguer import comme **nouveau chantier destinataire** et restauration de la même identité historique. |
| Projet neuf depuis le modèle | Toutes les fiches créées par le nouveau contrôleur peuvent être marquées, y compris en bootstrap. | Le premier WI peut être saisi dans les records de bootstrap ; toute voie de création/admission autorisée doit porter la même règle. La version du créateur ne suffit que si elle correspond à la version réellement adoptée dans le projet. |
| Montée interrompue puis relancée | Le rollback actuel couvre les exceptions attrapées, puis la relance peut reprendre une installation cohérente. | PC:3953–3964 restaure les fichiers sur `BaseException`, mais le journal est en mémoire (PC:705–711) ; cela ne démontre pas la récupération après coupure ou SIGKILL. Un mélange de créateur ancien/nouveau pourrait omettre ou poser prématurément la marque. L’état d’adoption utilisable doit être explicite. |

Les garde-fous actuels interdisent les records sur la branche de chantier, mais autorisent les chemins administratifs sur la canonique, puis auditent l’état indexé (PC:4012–4033). Ils ne prouvent pas que chaque fiche a été produite par une version donnée de `create-work-item`, et ne protègent pas encore un marqueur P7 inexistant. « Protégée par le garde-fou » ne suffit donc pas à garantir l’origine de la marque.

Pour une fiche sans marque et sans preuve d’origine, « ancien » et « neuf admis hors du créateur » restent indiscernables par **la marque seule**. Une procédure d’admission/restauration est indispensable si ces cas font partie de l’usage accepté. Elle ne doit pas ajouter une seconde borne temporelle.

## 5. T-03 — Option B en usage courant

| Situation | Ce que le précédent actuel établit | Ce qui peut être faux avec P7 |
|---|---|---|
| Décision absente | Un objet renseigné exige une décision valide ; `null` signifie simplement aucune baseline. Fonctions appelées : les deux baselines renvoient `None` avec l’état source. | `null = tous éligibles` pénalise les anciens d’un projet qui a oublié sa déclaration ; `null = tous dispensés` épargne les nouveaux. Distinguer projet neuf sans passé et adoption incomplète ; ce n’est pas ajouter un troisième statut de réponse. |
| Décision tardive | Rien n’impose de substituer la date de décision au commit qu’elle nomme. | Une décision tardive qui nomme **le bon commit passé** peut être correcte. Nommer le HEAD du jour dispense les nouveaux ouverts entre adoption et décision. Définir le fonctionnement pendant cet intervalle ; ne pas inventer une borne de secours. |
| Mauvais commit, correctement signé | L’appariement exact décision/état est vérifié. Le contrôleur vérifie existence et ascendance, pas l’installation d’une version à ce commit. | Trop tôt : anciens sollicités ; trop tard : nouveaux exemptés. La décision assume le repère ; sa signature ne prouve pas matériellement l’événement. |
| Aucune baseline préalable | `authorities_baseline` valide son propre objet, sans exiger `legacy_baseline` non nulle (PC:5633–5660). | Aucune raison technique de fabriquer d’abord une adoption ancienne du squelette. La nouvelle borne peut être autonome, sous décision du propriétaire. |
| Projet neuf sans montée | Le modèle existant prévoit des baselines nulles, `FIRST_START.md:56`. | Exiger malgré cela un commit d’adoption dans chaque projet neuf impose un cas bootstrap nouveau. Utiliser le commit de closeout comme borne exonérerait potentiellement le premier WI, qui doit déjà être autorisé avant cette clôture (`FIRST_START.md:78–79, 93–100`). |

**Mesures exécutées :** `require_baseline_named` accepte un SHA identique au champ de la décision fictive et refuse deux SHA différents. Cela teste seulement l’appariement. Une baseline pointant sur le SHA fictif, absent de Git, est refusée par `authorities_baseline` avec `is missing or not in current history`. Aucun « mauvais commit d’adoption accepté de bout en bout » n’a été exécuté : ce risque relève de l’absence de comparaison à un événement de version dans le code actuel.

**« Modèle exact » doit être remplacé par une description précise.** Les deux précédents sont différents :

- `legacy_record` retrouve un WI par son identité dans l’arbre de la borne (PC:5709–5741). Le WI non terminé peut évoluer ; seuls ses préfixes de preuves sont préservés. Les octets entiers sont figés seulement si le record était déjà `DONE` (PC:5779–5786).
- L’exemption des Agent Runs à la borne de lecture dépend d’un **blob inchangé** (PC:3534–3543, 3561–3569). Transposer cette condition au WI ferait perdre l’ancienneté lors d’une reprise légitime.
- Les exemptions de lecture cumulent deux bornes ; P7 ne doit pas reprendre ce cumul. Une baseline existante peut également avancer sur décision (PC:4297–4325) : P7 ne doit pas requalifier les chantiers à chaque déplacement d’une borne d’un autre objet.

**Coût d’adoption, avec unité explicite.**

| Cas | Surcoût minimal identifiable |
|---|---|
| Projet existant avec chantiers antérieurs | **3 opérations de préparation** : identifier le commit exact ; enregistrer la décision qui le nomme ; renseigner `{head, human_decision_ref}` dans Project State. **2 fichiers** concernés. |
| Même projet, décision de montée déjà prévue | Toujours le choix du repère et sa déclaration dans les deux supports, mais **0 ou 1 bloc HD supplémentaire** : le précédent permet plusieurs champs de baseline dans une même décision (`project_control/README.md:249`). « Une décision de plus » n’est pas systématique. |
| Projet neuf selon le précédent `null = aucun historique exempt` | **0 recherche de commit, 0 décision supplémentaire**, champ initial fourni par le modèle. Cette convention doit être écrite pour P7 ; elle n’est pas implicite dans « chaque projet déclare un commit ». |
| Projet neuf si B exige réellement une borne signée partout | De nouveau **3 opérations**, et un protocole de bootstrap à préciser avant le premier WI ; la règle actuelle interdit les baselines non nulles en `NOT_STARTED` (PC:1366–1369). |

Ces nombres ne sont pas des comptes de commandes shell : aucun CLI P7 n’existe et le séquencement de commit/intégration/audit dépend de la procédure retenue. Le contrôleur actuel ne fournit pas une commande générale « déclarer une baseline ». Les contrôles Git et audits peuvent être mutualisés avec la montée, ou ajouter des étapes. Le dire est plus exact que promettre un geste unique.

Enfin, le rehearsal de montée juge le nouveau contrôleur sur une copie de l’état commis (PC:3740–3800, 3925–3945). Une nouvelle déclaration rendue obligatoire avant même de pouvoir installer le nouveau schéma peut provoquer une dépendance circulaire d’adoption. Non reproduit ici ; procédure de migration à expliciter.

## 6. T-04 — Option C en usage courant

| Situation | Analyse | Niveau de preuve |
|---|---|---|
| Historique réécrit | Une réécriture qui conserve l’information pertinente n’entraîne pas nécessairement une erreur. Il faut définir quelle ascendance et quelle branche sont examinées. | Observation ; aucune réécriture exécutée. |
| Commits regroupés | Une version et des créations de WI peuvent se retrouver dans un même commit. L’ordre interne disparaît ; un choix avant/après peut exonérer un neuf ou solliciter un ancien. | Observation ; aucun squash exécuté. |
| Dépôt recréé sans historique | Un premier arbre peut contenir version récente et anciens records. Il ne contient pas leurs événements d’ouverture d’origine. Prendre ce premier commit ou HEAD n’apporte pas l’information manquante. | Limite de la donnée d’entrée ; pas de projet Git recréé dans cette revue. |
| Cœur sans manifeste | La version et son chemin historique sont indisponibles. Le contrôleur actuel rapporte déjà le manifeste absent (PC:3650–3663) et la montée exige les manifestes local/source (3839–3854). | Lecture directe ; **pas** un cas forcément accepté en silence. |
| Montée puis retour à une version antérieure | Le chemin ordinaire `template-upgrade` refuse les downgrades. Après un recovery autorisé, « première adoption » et « dernière réadoption » auraient des effets différents sur les WI intermédiaires. | Refus de downgrade exécuté en dry-run ; recovery non exécuté. |
| Copie de travail sans objets Git | Le manifeste donne la version, mais aucune commande ne peut y retrouver le commit d’introduction. La fonction de classification doit signaler l’indisponibilité au lieu d’exempter ou d’exiger par défaut. | `git log --format=%H -- provenance/core-manifest.v1.json` exécuté dans la copie : code 128, `fatal: not a git repository…`. |

Le dry-run a utilisé deux copies autorisées ; seule la valeur de version du manifeste local était fictivement passée à `3.20.0`. La source de montée restait conforme à `3.19.1`. Résultat : `SOURCE_MANIFEST PASS`, `LOCAL_MANIFEST PASS`, `UPGRADE_DIRECTION FAIL`, avec `a downgrade is not an upgrade`. Aucun retour arrière n’a été appliqué.

Autre ambiguïté intrinsèque au scénario d’usage : le premier commit portant la version peut être celui de la **branche de montée**, antérieur à son adoption sur la canonique. Des WI peuvent être ouverts entre ces événements. C doit nommer l’événement visé et traiter l’ordre partiel Git ; « le premier commit » seul ne suffit pas.

E2 a donc raison de signaler la dépendance à l’histoire, mais tort de généraliser « faussent en silence ». Selon le cas, une erreur est déjà détectée, l’information peut être préservée, ou elle devient indéterminable. B dépend également des objets Git de sa borne ; sa déclaration explicite ne le rend pas indépendant de l’historique.

## 7. T-05 — Une seule frontière et les dix comportements

### Frontière d’origine, phase de contrôle et preuve disponible

Une seule frontière signifie un même classement ancien/éligible pour **tous** les points d’entrée. Cela ne signifie pas que l’audit doive interdire un chantier autorisé sans réponse avant son premier départ : B10 impose que cet état soit représentable.

La création valide puis audite ses records (PC:4828, 4865, 4498–4505). `start`, `resume`, `close` commencent aussi par un audit (PC:4891, 5166, 5908 ; 4426–4430). Exiger inconditionnellement `prior_art` ou un `declared_at` déjà posé dans cet audit empêcherait d’atteindre la transition censée les enregistrer.

Règle commune à écrire : **éligibilité attachée à l’ouverture ; complétude exigée au premier départ réussi, y compris par `resume` ; déclaration ensuite conservée ; existence des chemins contrôlée seulement à ce premier départ.** Le schéma structurel doit rester compatible avec les états légitimes des deux populations et des différentes phases. Sa validation contextualisée doit employer la même éligibilité ; un validateur JSON isolé qui ignore le contexte ne peut pas dater une adoption Git.

| Option | Une seule frontière possible | Où une divergence apparaîtrait |
|---|---|---|
| A | Lire partout la même marque d’origine, conservée par toutes les transitions. | `start` lit la marque, mais audit ajoute une obligation globale ; ou admission manuelle sans marque ; ou contrôle ajouté uniquement à `start` tandis que `resume` effectue le premier départ. La marque facilite le partage, sans le réaliser dans le validateur actuel. |
| B | Une borne P7 et l’ensemble durable des identités de WI déjà ouvertes à cette borne, indépendamment des changements légitimes de leurs fiches. | Démarrage par présence à la borne, audit par blob inchangé ; ou comparaison au `start_head` du dernier run ; ou cumul avec les deux autres baselines. Un déplacement ultérieur de la borne peut aussi changer le classement. |
| C | Même événement Git et même ensemble historique résolus pour tous les contrôles. | Une commande choisit la première occurrence sur une branche, une autre l’intégration canonique ; ou l’une utilise l’historique tandis qu’une autre se rabat sur HEAD/version courante lors d’un manque d’objets. Sans information, le résultat doit rester indisponible. |

La condition `if` d’un schéma a été rejetée expérimentalement : `work-item: unsupported schema keywords ['if']`. L’assertion E2 « marque lue à l’identique par le schéma » exige donc une précision d’architecture ; elle n’est pas fournie par le validateur présent.

### Passage de B1 à B10

**T** = tenu tel quel par l’intention, après réalisation du contrôle commun décrit dans E1 ; **R** = tenu au prix d’une règle supplémentaire à écrire ; **I** = impossible à établir avec les seules données de l’option dans le cas indiqué. Ces mentions sont des évaluations de conception, **pas des tests P7 passés**. T ne signifie pas que le contrôleur 3.19.1 contient déjà P7. Pour C, les T supposent l’événement historique disponible et déterminé ; à défaut, aucune classification correcte n’est certifiable.

| Comportement | A | B | C | Motif |
|---|---|---|---|---|
| B1 — éligible sans champ : refus au départ | R | R | R | Viser le premier départ par `start` **ou** `resume`, sans rendre impossible l’état préalable sans réponse. |
| B2 — FOUND sans candidat/chemin/entrée : refus | T | T | T | Le contrat commun l’énonce ; le choix de borne n’ajoute pas de difficulté propre. |
| B3 — FOUND, chemin inexistant : refus | T | T | T | Vérification unique au premier départ, déjà demandée. |
| B4 — NONE_FOUND incomplet/chemin inexistant : refus | T | T | T | Même contrôle commun ; préciser les éléments blancs en T-06. |
| B5 — REIMPLEMENT sans justification : refus | T | T | T | Présence écrite requise ; pas de jugement du motif. |
| B6 — réponses complètes acceptées, horodatées | R | R | R | Définir saisie et transaction : poser le gel seulement au départ réussi ; rien de figé après échec. Les autres gates continuent de s’appliquer. |
| B7 — ancien ouvert avant adoption, repris après | R | R | R / I | A : absence de marque conservée et identité historique restaurée correctement. B : appartenance historique, jamais blob courant. C : R si histoire exploitable ; I pour reconstituer la vraie frontière après perte de l’information nécessaire. |
| B8 — audit d’anciens records | R | R | R / I | Schéma facultatif **et** exemptions sémantiques cohérentes. C : I si l’ancienneté ne peut plus être établie par sa seule source de données. Le dépôt doit être valide par ailleurs ; ce dossier sans Git n’est pas un test d’audit vert. |
| B9 — chemin déplacé après départ, close/audit admis | R | R | R | Définir le gel de toute la déclaration et l’absence de nouvelle vérification de chemin, y compris à la reprise. Ne pas réutiliser le contrôle de fraîcheur des autorités. |
| B10 — status éligible sans réponse : UNKNOWN | R | R | R | Alimenter le constructeur de vue avant IN_PROGRESS ; classifier par la même borne ; UNKNOWN seulement à l’affichage. |

Aucune option de borne ne garantit à elle seule B9. Si un chemin disparu est aussi une **autorité obligatoire** toujours routée, d’autres contrôles existants peuvent légitimement échouer. L’essai B9 doit déplacer un candidat sans casser une autre obligation indépendante ; il prouve que **P7 n’ajoute pas** de refus tardif fondé sur ce chemin, pas que toute suppression de fichier doit rendre l’audit vert.

La frontière exacte doit aussi définir « ouverture » : la création/autorisation de la fiche et le démarrage ne sont pas le même événement (PC:4800–4806 contre 4933–4935). L’option A suppose le premier ; B et C doivent viser le même événement, y compris pour le premier WI de bootstrap et les imports.

## 8. T-06 — Forme du champ

La forme donne une structure utile, mais « une chaîne non vide ne vaut pas réponse » ne définit pas ce que le contrôleur peut vérifier. Il faut distinguer **complétude mécanique** et **contenu déclaratif utile**, sans promettre une appréciation automatique du motif.

Expériences avec `schema_record_errors`, PC:1261–1277 :

| Valeur et contrainte d’essai | Résultat | Conclusion |
|---|---|---|
| Trois espaces, texte `minLength: 1` | accepté | Une longueur minimale n’élimine pas les blancs. |
| Liste contenant une chaîne vide, seulement `minItems: 1` | accepté | La cardinalité ne contrôle pas chaque élément. |
| Liste contenant un espace, éléments `minLength: 1` | accepté | Les blancs doivent aussi être traités dans les listes. |
| Terme `x`, `minLength: 1` | accepté | Un caractère peut être un identifiant légitime ; sa longueur ne prouve pas sa pertinence. |
| Justification `Oui`, `minLength: 1` | accepté | Présence formelle ; aucun motif réellement explicité. |
| Chemin `data/README.md` de la copie | existe | L’existence ne démontre aucun rapport avec la capacité du chantier. |

Ce sont des démonstrations des primitives actuelles, **pas des contournements d’un contrôle P7 qui n’existe pas**. Le nettoyage CLI actuel retire déjà les blancs de bord (PC:860–864), contrairement au simple `minLength`.

**Formulation proposée, sans code :**

> Une réponse complète contient tous les éléments exigés pour son statut. Chaque texte exigé, y compris chaque élément d’une liste, doit rester non vide après retrait des blancs de bord. Pour FOUND, chaque candidat indique un chemin local et un point d’entrée permettant de retrouver un fichier, une section, un symbole ou une commande ; sa note explique le rapport avec la capacité recherchée. Pour NONE_FOUND, les chemins et termes décrivent la recherche effectivement menée. Pour REIMPLEMENT, la justification écrite indique pourquoi le candidat n’est pas repris ou adapté. Le contrôleur vérifie la présence, la structure, les valeurs admises et, au premier départ seulement, l’existence des chemins locaux. Il ne certifie ni la pertinence ou l’exhaustivité de la recherche, ni la qualité du motif de réimplémentation.

Compléments nécessaires :

- Nommer explicitement les sous-champs exigés du candidat, dont le statut de `note`, et les règles applicables aux champs de la branche non choisie. Une liste non vide doit contenir des éléments complets, pas des objets vides.
- Définir des chemins relatifs au projet, sans évasion par chemin absolu, parent ou lien symbolique ; vérifier la résolution seulement au départ, sans lire un autre dépôt. Préciser si les répertoires sont acceptés, avec un point d’entrée assez précis pour retrouver le candidat.
- Ne pas imposer un seuil de caractères censé juger la valeur d’un terme ou d’un motif. Une justification d’un mot peut rester mécaniquement présente ; prétendre garantir son utilité violerait la limite « l’outil ne juge pas le motif ».
- `external` reste informatif et ne remplace pas un candidat local obligatoire. Le cas « connu uniquement ailleurs » doit recevoir une interprétation claire du périmètre de recherche, en conservant les **deux seules réponses** décidées.
- Réserver `declared_at` au contrôleur et figer l’ensemble de la déclaration, pas seulement cette date. Un contenu et une date valides ne prouvent pas leur absence de modification.

L’incomplétude de ces formulations constitue une observation de conception commune aux options. Les essais de primitives ne justifient pas de qualifier le prototype futur de contournable.

## 9. T-07 — Un angle supplémentaire : comment la réponse entre dans le parcours

**Angle retenu : le trajet de saisie et sa transaction.** Les questions précédentes déterminent qui répond, quand et avec quoi ; elles ne disent pas par quelle opération la réponse entre dans la fiche. Même avec une bonne borne, ce trajet conditionne la possibilité d’utiliser le contrôle.

Le contrôleur actuel crée et committe les records en mode normal (PC:4857–4871), exige un audit administratif puis un arbre propre avant `start` (PC:4891–4898, 4426–4435) et interdit les records sur la branche de chantier (PC:4019–4024, 6104–6110). Le parseur actuel ne reçoit aucun `prior_art`. Ajouter seulement un champ et un refus laisse donc le geste de saisie non défini.

Cela **ne démontre pas une impasse** : un commit administratif sur la canonique est possible selon PC:4012–4018. Il faut décrire le parcours autorisé, sans inventer une dérogation ni solliciter une autorisation humaine à chaque réponse.

Formulation proposée :

> Le contrat de commande précise comment transmettre et corriger la déclaration avant le premier départ. Cette saisie suit les transitions administratives du contrôleur. Au premier départ réussi, la validation de la réponse, la vérification des chemins, la pose de declared_at et le passage en cours appartiennent à la même transaction. Un échec ne laisse pas une déclaration figée. Toute reprise ultérieure conserve la déclaration et son horodatage.

La saisie à la création, une transition de déclaration, ou un paramètre du premier départ sont des modalités à examiner ; aucune n’est sélectionnée ici. Elles restent dans le périmètre « champ, refus, status ». Le cas d’une fiche elle-même routée doit auparavant recevoir l’arbitrage signalé en T-01, conformément à E1.

## 10. Constats, du plus grave au moins grave

Seuls les constats ci-dessous participent au verdict. Les scénarios futurs non exécutés restent les observations explicitement signalées en T-02 à T-07.

### R1 — Majeur — E2 généralise à tort l’exclusion de la fiche de l’empreinte

**Objet :** E2 résumé 1, B.1 et état du premier blocage.

**Situation reproductible :** 1. Copier `source/` dans un répertoire d’essai. 2. Copier la fixture Work Item sous le chemin `project_control/work-items/WI-001.json`. 3. Ajouter ce chemin à `base` du routage. 4. Appeler `common_findings(False)` et relever uniquement `DOCUMENT_ROUTING`, puis `work_item_manifest`. 5. Ajouter la propriété fictive `prior_art` à la fiche, puis rappeler `work_item_manifest`.

**Preuve :** routage `PASS`, record présent dans les entrées, empreintes différentes données en T-01 et dans `runs/revue-1/mesures.txt`. PC:93–102, 2055–2072, 3435–3458. L’audit complet de la fixture n’est pas déclaré vert.

**Conséquence :** l’assurance « remplir après context-manifest ne périme pas l’empreinte » est fausse dans une configuration de routage acceptée. Le mandat de construction réserve précisément ce cas à une décision de conception. Une assurance générale de non-blocage ne peut pas être conservée.

**Correction suggérée :** borner la mesure au routage fourni, documenter le contre-exemple et faire arbitrer le traitement du record routé avant de promettre une garantie générale. Aucune modification de routage n’est appliquée au produit.

### R2 — Modéré — E2 confond compatibilité du schéma et compatibilité de l’audit

**Objet :** E2 B.3 « chemin audit couvert, sans aucune baseline ».

**Situation reproductible :** 1. Charger la fixture Agent Run en mémoire. 2. Retirer `authorities_read`. 3. Appeler `core_schema_errors`, `validate_agent_run`, puis `agent_run_authority_errors` avec les baselines nulles du modèle. 4. Sur la fixture Work Item DONE, retirer `close_head`, puis appeler la validation de schéma, `validate_work_item` avec la clé ALPHA, et `done_evidence_errors`.

**Preuve :** les validations structurelles passent et les contrôles sémantiques refusent, sorties intégrales dans les deux journaux. PC:2998–3018, 3572–3593, 5795–5809. Aucune fonction n’a été remplacée ou simulée.

**Conséquence :** rendre `prior_art` facultatif ne suffit pas à établir B8. Le futur branchement sémantique pourrait réintroduire une exigence pour les anciens records. Ce n’est pas un défaut P7 actuel ; c’est une déduction invalide dans le rapport mesuré.

**Correction suggérée :** limiter la conclusion à la structure ; exiger le prédicat commun d’éligibilité dans toutes les validations sémantiques et les audits avant/après transitions, avec une phase préalable permettant B10.

### R3 — Mineur — Deux comptages et la description de la création sont inexacts

**Objet :** E2 B.2 et B.6.

**Situation reproductible :** 1. Charger le schéma JSON et compter `required` et `properties`. 2. Analyser l’AST du contrôleur et réunir les deuxièmes arguments littéraux des appels `add`. 3. Résoudre les trois sites d’appels dynamiques cités en T-01. 4. Lire la construction du dictionnaire de création.

**Preuve :** **31/33**, **65 noms littéraux**, **70 via add après résolution dynamique**, contre 30/32 et 58. Les 65 noms sont conservés dans `mesures.txt`. PC:4244, 4286, 4792–4827, 6129–6132 ; schéma:7–40.

**Conséquence :** la précision factuelle d’E2 est à corriger. Ces erreurs seules ne bloquent pas le choix d’une borne.

**Correction suggérée :** remplacer les nombres, nommer le périmètre du comptage et distinguer les paramètres reçus des propriétés générées.

## 11. Classement motivé soumis au Project Owner

**1. Option A, recommandation conditionnelle.** Elle transporte le classement avec la fiche et convient naturellement aux reprises et aux projets neufs ; elle demande le moins d’administration par projet. La condition décisive est de définir toutes les voies d’admission, import/restauration compris, et de protéger la marque pendant les transitions. Il faut également préciser l’adoption effective lors d’une installation interrompue. Sans ces règles, l’absence de marque ne prouve pas l’ancienneté. A n’est donc pas prête « telle quelle ».

**2. Option B.** Elle rend le repère explicite et imputable à une décision du projet. Elle peut passer devant A si le propriétaire privilégie cette déclaration et accepte le coût réel décrit en T-03. Le précédent fournit des validations utiles, mais pas une solution à recopier intégralement : null, premier WI, appartenance historique, moment d’installation et stabilité de la borne exigent une rédaction propre à P7. Son choix relève du propriétaire, notamment parce qu’E1 interdit au constructeur d’inventer cette baseline sans arbitrage.

**3. Option C.** Elle évite une déclaration supplémentaire mais reporte la difficulté sur une donnée parfois absente ou ambiguë. La version inscrite dans l’arbre ne suffit pas à dater son adoption dans le projet. Les erreurs ne sont pas toutes silencieuses, et tout historique réécrit n’est pas automatiquement invalide ; ces nuances ne résolvent pas la perte d’information ni le choix de l’événement canonique.

Ce classement porte sur le parcours d’usage et les contraintes fixées, pas sur des performances mesurées d’implémentations inexistantes. **Aucune option n’est adoptée par cette revue.** Aucune quatrième voie n’est ajoutée : les précisions demandées sont des conditions de cohérence des trois options, pas une nouvelle borne inventée.

## 12. État final

`source/` intact : **125 fichiers avant et après**, même empreinte d’arbre `ddfaf9f9d7b3e37bf8fa7b762f2f419277c0af66b676d620f5ff028b616a5854`.

Créations sous `runs/` : un seul espace `runs/revue-1/`, **255 fichiers** au total :

- `README.md`, mention de fiction et périmètre des essais ;
- `copie/`, copie initiale des 125 fichiers, plus une fiche fictive `WI-001.json` ; seul le routage, cette fiche, Project State et la valeur de version du manifeste y ont servi de données expérimentales ;
- `reference/`, seconde copie intacte des 125 fichiers, utilisée comme source du dry-run ;
- `mesures.txt`, sorties des mesures d’empreinte, schéma, contrôles et contenu ;
- `scenarios.txt`, sorties des tests d’exigence sémantique, d’appariement de décision, d’absence d’historique et de refus de downgrade ;
- `decision-fictive.md`, décision identifiée comme fictive, sans autorité et sans commit.

Empreintes des traces :

| Fichier | SHA-256 |
|---|---|
| `runs/revue-1/mesures.txt` | `6083380b5236b2482b122ca36f4bb45c1cade7b3cd7ae6f63d2caa2db778d9ee` |
| `runs/revue-1/scenarios.txt` | `7ca2edb3be785af6c6e7c4489313f23c5e286cf9b852bad83a188a524187696b` |
| `runs/revue-1/decision-fictive.md` | `d77b3481155ad9df326c66e338edf23e6c1d0414594a5180576726ae3c287148` |

Les essais sont laissés en place, comme traces jetables, sans nettoyage. Aucun historique Git n’a été créé. Aucun patch, prototype ou fiche de chantier réelle n’a été produit. Le seul livrable de revue est le présent fichier, écrit une fois.

## 13. Verdict

**P7_BORNE_REVUE_REQUIRES_MAJOR_REDLINE**

Justification : le contre-exemple exécuté R1 contredit une assurance portant directement sur un blocage de conception prévu par E1 ; R2 invalide la suffisance annoncée pour l’audit des anciens records. R3 appelle des corrections factuelles mineures. Les autres limites et règles supplémentaires sont exposées pour l’arbitrage du propriétaire ; elles ne sont pas transformées en constats bloquants sans expérimentation du comportement futur.
