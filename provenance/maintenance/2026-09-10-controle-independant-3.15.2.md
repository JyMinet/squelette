> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

1. Le parcours normal fonctionne sur la copie contrôlée, mais deux protections annoncées présentent des écarts reproductibles : la validation initiale peut accepter des documents encore en brouillon, et une clôture peut consommer un mandat ancien portant un refus. La version ne peut donc pas être déclarée conforme sur la base de ce contrôle.
2. Le filtre des preuves refuse les échecs usuels et les pièces vides. Il refuse aussi un test réellement réussi dans un cas de diagnostic attendu ; une pièce neutre ou certains formats de texte permettent à une déclaration de réussite de passer sans résultat positif supplémentaire. Ces résultats distinguent défauts et limites de garantie.
3. Le contrôle reste partiel : l’historique 3.6.1 annoncé est absent, et les essais indépendants supplémentaires du garde-fou ont été bloqués par l’approbation automatique. Les fichiers source ont été conservés ; les expériences et leurs journaux restent dans `runs/`. Aucun correctif n’est proposé.

# Contrôle de robustesse du squelette 3.15.2

## État exact et périmètre

Racine accordée : `~/Projets/squelette-controle-3.15.2/`. Les chemins préfixés par `source/` ou `runs/` partent de cette racine. Les noms de journaux abrégés dans T-03 partent de `runs/t03/`. Dans la section détaillée T-02, les chemins `logs/`, les numéros de scénarios et les scripts partent de `runs/t02/` ; une notice le rappelle. Date du contrôle : 10 septembre 2026. Le rapport était absent au précontrôle ; sa création finale est exclusive, sans écrasement.

L’entrée est `source/`, un export de **116 fichiers**, sans `.git`, bundle ni archive historique. La version **3.15.2** est celle déclarée dans `provenance/core-manifest.v1.json`. Les **24 fichiers core** correspondent à ce manifeste après la normalisation documentée du premier marqueur d’initialisation dans `FIRST_START.md`. L’empreinte brute de ce dernier diffère normalement de l’empreinte normalisée : ce n’est pas une divergence du core.

Aucun HEAD, tag ou historique de promotion de la source n’est attestable avec cet export. Les SHA courts et les promotions cités dans le CHANGELOG restent des déclarations documentaires, pas des objets Git vérifiés. Les dépôts autonomes des essais ne reconstituent pas cet historique.

| Pièce | SHA-256 |
|---|---|
| `source/provenance/core-manifest.v1.json` | `fdba741d25f58029c201a6266cb3a29564c540c269de8e667e4fb4aa0004f758` |
| `source/scripts/project_control.py` | `8bea8d26d25f61f334f9c584c41ae967475533b80fe5ac013673dee4572937be` |
| `source/scripts/hooks/pre-commit` | `e6e5908ae426ed2857e026736434e34e9e193c32bf7af2495d30f287d32d8516` |
| `source/tests/test_template.py` | `ca75642a37f140bc464830adf21fb3db89fc3ecd3e1e9db62fe8239062401fca` |
| `source/FIRST_START.md`, octets bruts | `fd16f922c0ed1c737f7025ae2443c93c72c233cd4eb0c0853d22e702fcad5eb3` |
| `source/docs/agent-governance/AGENTS.core.md` | `dd2531d349ba7e9a8ebbe2eba4f9fe4163e7e05ccb053d36f79e3c9b5d6c1907` |
| `source/project_control/README.md` | `ec44e4742c6974d4a3f51fec8d0d813a3a7aa92a654021a3c4fb09b07d876a78` |

L’inventaire complet avant essais est `runs/control/meta/source-before.json` ; sa propre empreinte est `f88c74e0d8e66b3f3dec8991a5ef721fc08d73b3c4c9bbeb13f388562c7a8042`. Le contrôle normalisé figure dans `runs/control/meta/preflight.json`. La comparaison finale et l’environnement d’exécution sont consignés plus bas.

## Méthode, privilèges et écarts au protocole

Les trois campagnes indépendantes T-01, T-02 et T-03 utilisent des copies autonomes. T-01 et T-02 emploient des helpers de construction livrés avec les tests, puis les vraies commandes du produit pour les transitions mesurées. T-03 suit les documents, les schémas et deux modèles JSON livrés ; la logique Python du contrôleur et celle de la démo n’ont pas servi à résoudre son parcours. Cela ne constitue pas un essai utilisateur aveugle ni une interview réelle : toutes les autorités de fixture sont fictives. L’accès aux deux modèles JSON de `tests/fixtures/project_control/` dépasse une lecture limitée aux seuls fichiers Markdown ; cette assistance est déclarée, pas assimilée à une autonomie démontrée du seul FIRST_START.

Le terminal est disponible dans toutes les campagnes. Chaque constat précise si des fichiers sont écrits directement, si la gate est installée et si un override sert à construire l’état initial. Un contournement qui exige l’administration de `.git` ou la réécriture d’une baseline ne reçoit pas la même portée qu’un défaut obtenu avec les seules écritures d’un contributeur autorisé.

Aucune commande réseau ni aucun push n’a été exécuté par les campagnes. Un test du produit qui effectue un push vers un dépôt local a été exclu : le mandat interdit aussi ce geste. Les configurations Git de test sont locales, les configurations globales/système sont neutralisées et les temporaires de campagne sont dirigés vers `runs/`.

**Écart initial de périmètre.** Dans le même appel d’outils que la première lecture de la pièce jointe, avant prise en compte de son contenu, un inventaire de noms `AGENTS.md` a été lancé sous l’espace Documents/Codex. Il a retourné un chemin ; aucun contenu trouvé n’a été ouvert. La pièce jointe elle-même a nécessairement été lue à son chemin fourni par l’utilisateur, hors de la racine d’essai. Après connaissance du mandat, aucun projet réel n’a été recherché ou ouvert. L’inventaire initial reste un écart au « hors de ce dossier, rien » ; il n’est pas dissimulé par le confinement ultérieur.

**Conflit de marquage.** Une ligne libre `FIXTURE DE CONTRÔLE — FICTIF, N'AUTORISE RIEN` en tête d’un JSON strict le rend invalide ; une telle ligne dans une pièce vide supprime le cas « vide ». Les textes et scripts nouveaux portent l’avertissement, les preuves JSON le portent dans leur premier champ descriptif, et les fichiers vides/binaires ainsi que les records automatiques sont identifiés par le dossier et la notice de campagne. Les copies inchangées du produit restent inchangées. Le marquage littéral de chaque fichier n’a donc pas été satisfait : c’est une limite du protocole exécuté, pas une nouvelle règle choisie pour le produit. Aucun de ces records n’est présenté comme une autorisation réelle.

## Vérifications, thème par thème

### T-01 — Cohérence des preuves

Dix-neuf scénarios CLI, chacun avec `close`, `audit` et `status --json`, plus deux expériences de diagnostic attendu réellement exécutées avec unittest. La gate est installée, le core reste intact, aucun override ne sert à la campagne mesurée. Les cas détaillés et leurs empreintes figurent dans la section T-01 ci-dessous.

- Standard : pièce positive, clôture DONE ; mélange d’échec historique et de réussite explicite accepté.
- Dégradé correctement refusé : unittest/pytest échoués, toutes pièces négatives, zéro octet, liste vide, échec accompagné d’un binaire, échec après plus de 2 Mio.
- Dégradé accepté : échec accompagné d’une pièce neutre ; sortie négative rendue non UTF-8 ; UTF-16 ; présentation ANSI précise testée ; pièce uniquement binaire.
- Faux positif : véritable test de rejet d’une entrée invalide réussi, code 0 et bilan OK, refusé à cause d’une ligne `ERROR:` attendue.

Un audit PASS sur un chantier encore IN_PROGRESS ne valide pas une preuve que `close` vient de refuser. Il n’a pas été compté comme une réussite de cette preuve.

### T-02 — Exemption des décisions anciennes

Les essais comparent l’état actuel du bloc de décision à l’état au commit de baseline, puis testent des transitions réelles. Ils couvrent décision nouvelle/modifiée, déplacement dans/hors registre, nouvel identifiant, doublons, restauration identique, baseline avancée et décisions de transition. Les privilèges de construction de l’historique figurent dans la section T-02 ci-dessous.

Le comportement standard conserve le vocabulaire ancien inchangé et refuse une décision nouvelle ou modifiée qui n’autorise pas. `create-work-item`, `block` et `resume` refusent les mandats REJECT gelés testés. En revanche, après actualisation de la preuve de lecture, le scénario `close` décrit ci-dessous termine DONE avec ce type de mandat. Les doublons et la redéclaration de baseline ont des résultats distincts ; ils ne sont pas confondus avec cette clôture.

### T-03 — Projet neuf

Le journal `runs/t03/01-initial.log` établit la baseline autonome, l’installation de gate, le status et le bootstrap-audit PASS. L’arbre exporté est ajouté par chemins explicites. Le parcours se poursuit dans `02-initialize.log`, `03-finish.log`, puis `06-cycle.log` : clôture bootstrap PASS, commit sans override refusé, commit avec le mandat fictif prévu par FIRST_START accepté, audit normal PASS, start avec empreinte, écriture autorisée, commit, intégration, close et audit final PASS. Le premier chantier est documentaire et toutes ses gates d’exécution sont explicitement NOT_APPLICABLE ; les preuves de tests sont exercées séparément en T-01.

Cas dégradés exécutés : chemin métier refusé pendant bootstrap ; initialisation incomplète refusée avec les formats attendus ; absence d’empreinte au start refusée ; chemin hors scope refusé ; commande bootstrap après COMPLETE refusée. L’override de la clôture est bien expliqué dans FIRST_START et apparaît dans le journal du commit.

**Trois choix ont dû être déduits ou précisés au-delà de la séquence FIRST_START** : passage de `repository_role` à `PROJECT` en consultant le schéma ; renseignement de `completion_human_decision_ref` avant le premier closeout, révélé par son refus ; choix d’un chemin de conservation du rapport de closeout et de sa référence chaîne dans `closeout_evidence`. Le contrôleur fournit de quoi progresser, mais aucun parcours copié intégralement n’a remplacé ces choix. Les 31 champs du premier Work Item requièrent une construction manuelle à partir du contrat/modèle livré.

**Trois erreurs de saisie du contrôleur de test**, sans attribution de défaut au produit : `depends_on` au lieu de `dependencies`, conditions de clôture non identiques entre record et registre, ligne WI ajoutée hors du tableau de roadmap. Les deux premières sont refusées par l’audit ; la troisième passe l’audit initial puis fait échouer et annuler `start`, jusqu’au déplacement de la ligne dans le tableau. Les refus et la reprise sont conservés, pas supprimés des résultats.

Les modèles de décision interne et de registre, une fois remplis, sont acceptés. Le test livré des modèles et celui des messages sont inclus dans la suite. La campagne T-02 examine le modèle de décision hors dossier. Le contrôle ne prétend pas avoir rempli chaque modèle optionnel runtime du dépôt. La comparaison « documents brouillons avec/sans notices de format » produit le défaut F-T03-01 ci-dessous.

### T-04 — Montée 3.6.1 vers 3.15.2

**Non réalisable avec les entrées fournies.** `runs/t04/input-check.log:4` et les commandes suivantes montrent l’absence de dépôt Git et l’échec de résolution de `v3.6.1`. Aucune archive historique n’est présente. La demande de rendre cet historique disponible dans le dossier accordé n’a reçu aucune réponse au moment de la rédaction.

Un contrôle limité a été exécuté : `template-upgrade --source <source>` depuis le projet T-03 déjà initialisé en 3.15.2. Il compare le même core et passe ; cela n’est pas une montée de version et ne prouve rien sur l’ordre des migrations, les champs introduits après 3.6.1 ou un possible état intermédiaire bloqué.

La procédure documentée a été lue (`ADOPTION.md`, section compatibilité et mise à jour du README Project Control, CHANGELOG), mais aucune ancienne version n’a été reconstruite à partir de souvenirs ou d’un changement artificiel de numéro. Les observations de code sur les mises à jour restent non bloquantes faute de reproduction historique. Aucun accès aux dépôts réels n’a été tenté pour pallier l’entrée manquante.

### T-05 — Garde-fou de commit

Deux niveaux de preuve restent séparés : les vraies opérations T-03 et les tests livrés exécutés sur copie ; les nouvelles expériences adversariales indépendantes, non exécutées après deux rejets de permission automatiques.

| Configuration | Preuve disponible |
|---|---|
| Gate hors arbre, commit normal autorisé | T-03, `06-cycle.log`, vrai commit accepté |
| Canonique protégée, override explicite | T-03, `03-finish.log:163`, refus puis acceptation avec mandat |
| Scope WI et renommage origine/destination | Tests livrés, fonctions commençant aux lignes 3713, 3766 et 3796 de `tests/test_template.py` |
| Référence versionnée retirée, copie standard divergente | Test livré à la ligne 3827 ; contrôle de MISMATCH et de l’audit |
| Ancien mode, retrait du hook versionné | Test livré à la ligne 3943 ; commit accepté et absence ensuite signalée |
| Symlink indexé puis masqué sur disque | Test livré à la ligne 3895 |
| Record falsifié dans l’index mais honnête sur disque | Test livré à la ligne 5045 ; refus de la CLI et du vrai commit, HEAD conservé |
| Fusion normale / passager visible | Test livré à la ligne 4888 |
| Interruption d’une transition start | Test livré à la ligne 4831 ; cela ne couvre pas l’interruption de la gate |
| Copie standard absente, worktree lié, snapshot inaccessible, passager masqué, interruption gate/install | Pas de nouvelle reproduction indépendante ; limites ci-dessous |

Le résultat global de la suite est donné plus bas. Les références ci-dessus identifient les scénarios, pas un verdict indépendant sur toutes les configurations possibles.

**Blocage d’exécution indépendant.** L’approbation automatique a refusé deux fois l’écriture/exécution T-05 dans le dossier accordé, d’abord en invoquant l’absence des deux confirmations de périmètre, puis en précisant que la citation du mandat dans la justification ne suffisait pas à les établir. Le contrôle délégué n’a écrit aucun fichier. La confirmation demandée à l’utilisateur n’était pas reçue au moment de la rédaction. Le refus n’a pas été contourné. La suite déjà autorisée et les essais T-03 constituent des preuves distinctes.

### T-06 — Promesses et contrôles effectifs

| Promesse ou formulation | Ce qui est effectivement établi |
|---|---|
| « la ligne Status doit être exactement… » | Recherche d’une sous-chaîne dans tout le document ; F-T03-01 montre un refus manquant avec les modèles livrés. |
| Aucune transition actuelle ne bénéficie du vocabulaire gelé, y compris `close` | Vrai pour les autres transitions essayées, contredit par la clôture de T-02. |
| Preuve de lecture | L’empreinte porte sur les octets routés, pas sur lecture ou compréhension. Cette limite est explicitement et correctement décrite dans le core. |
| Preuve de réussite avec pièces vérifiables | Références Git, empreintes et reconnaissance textuelle étroite ; pas d’exécution indépendante certifiée. Cette limite est écrite ; les effets d’une pièce neutre et des encodages doivent être conservés dans l’interprétation des résultats. |
| Deux confirmations humaines hors dossier | Des chaînes enregistrées sont vérifiées. Les cas T-02 distinguent confirmations absentes/identiques et simples textes distincts ; ils ne prouvent ni identité humaine ni deux arrêts réellement tenus. |
| Git Safety mécanique, « jamais git add -A », « seul close produit DONE » | Le contrôleur examine les états et records. Il ne dispose pas d’un historique authentifié de toutes les commandes du terminal. Sans scénario supplémentaire, ceci reste une observation de portée, pas un constat bloquant. |
| Gate absente ou ancien mode détectés | Le code affiche ces états mais les classe `PASS: COMMIT_GATE` ; la divergence seule fait FAIL dans ce contrôle. Signalement et refus sont donc deux garanties différentes. |
| Core protégé et version connue | Le manifeste permet la comparaison ; `status` signale la dérive locale. Le README dit explicitement que la dérive locale n’est pas, en elle-même, un échec de l’audit. Aucune attestation externe de la version n’est fournie. |

Les affirmations générales du README (« les règles sont des contrôles », « le contrôleur refuse ») se lisent avec ces limites. Aucune conclusion sur une protection système, des droits réseau, une signature d’auteur ou l’impossibilité pour un administrateur de fabriquer des records n’est justifiée par les contrôles effectués.

## Constats classés

Ordre de gravité : **F-T03-01** (validation initiale), puis anomalie de clôture **T-02** (mandat gelé REJECT, avec privilèges historiques précisés), puis l’anomalie de doublons de registre documentée en T-02, puis **F-T01-01** (faux positif). La redéclaration de baseline T02-F3 est classée comme limite de confiance, pas comme défaut bloquant. Les limites T-01 et les hypothèses statiques T-05 sont séparées des défauts bloquants. Aucune hypothèse sans échec reproduit ne fonde le verdict.

### F-T03-01 — Les notices de format valident des documents encore en brouillon

**Sévérité : majeure ; objet : gate de validation de l’initialisation.** Le défaut peut arriver en suivant les documents : les notices ajoutées aux modèles contiennent déjà les sous-chaînes reconnues comme validation. Il ne nécessite ni modification du contrôleur, ni retrait de gate, ni falsification d’index. Il justifie à lui seul un refus d’homologation de la promesse de validation initiale.

**Reproduction pas à pas.**

1. Créer une copie autonome de l’export et y installer la gate ; exemple conservé : `runs/t03/project`. La construction complète est tracée dans `01-initial.log` et les scripts de fixture `initialize_fixture.py` / `finish_bootstrap.py` ; pour la rejouer, utiliser une nouvelle copie et adapter leurs seules variables de destination, sans réutiliser le projet déjà clos.
2. Renseigner le Charter, la carte et sa revue Anti-Octopus, la branche canonique, une HD de clôture, une conversation, le premier WI AUTHORIZED et sa roadmap/son registre, le style et la langue. Le témoin correctement validé retourne `bootstrap-closeout=0` (`03-finish.log:67`).
3. Remettre uniquement `docs/architecture/INITIAL_ARCHITECTURE.md` et `docs/adr/ADR-0001-initial-architecture-boundaries.md` dans l’état des modèles source, précédés de l’avertissement fictif. Leurs vrais statuts sont DRAFT et PROPOSED ; leurs UNKNOWN subsistent. Les pièces exactes sont conservées sous `runs/t03/evidence/`.
4. Exécuter `python3 -B scripts/project_control.py bootstrap-closeout --path FIRST_START.md --path project_control/project-state.v1.json`. Le résultat est **PASS, code 0**, ligne 103 du journal.
5. Sans changer leurs vrais statuts, supprimer seulement la ligne explicative commençant par `> À la clôture`. Relancer la même commande : **FAIL, code 1**, ligne 139, pour absence de validation d’architecture et d’acceptation d’ADR.
6. Le contrôle remet ensuite ses documents de fixture réellement validés, conserve le vrai rapport positif, termine l’initialisation et le chantier normal. Il n’a pas promu les documents dégradés comme autorités réelles.

**Preuves.** `runs/t03/03-finish.log:70` décrit la variation ; `:103` contient le PASS ; `:106` décrit le retrait des notices ; `:139` contient les deux refus attendus. `source/scripts/project_control.py:2930` et `:2932` testent la présence des mots dans l’ensemble du texte ; les mots attendus sont déjà dans les notices de `source/docs/architecture/INITIAL_ARCHITECTURE.md:5` et `source/docs/adr/ADR-0001-initial-architecture-boundaries.md:5`. Empreinte du contrôleur : table d’état ci-dessus. Les empreintes du journal et des pièces sont dans le registre final des preuves.

**Impact réel.** La commande annonce que les livrables d’initialisation sont complets alors que deux documents attestent encore leur non-validation. Les notes introduites pour rendre les refus compréhensibles font elles-mêmes satisfaire le contrôle. La campagne ne démontre pas une autorisation de production, mais bien la perte de ce refus d’initialisation annoncé.

**Privilèges requis.** Terminal et édition normale des documents bootstrap dans une copie ; gate installée et identique. Aucun override pour les deux appels comparés, aucun accès à `.git` pour le défaut. L’override ultérieur de clôture est celui expressément documenté dans FIRST_START et n’intervient pas dans la démonstration A/B.

**Convention de preuves T-02 :** tous les chemins abrégés de cette section sont relatifs à `runs/t02/`, sauf ceux explicitement préfixés par `source/` ou `runs/`. Les empreintes des pièces décisives et leurs lignes sont regroupées dans le registre final.

### T-02 — Exemption des décisions antérieures à la baseline

- L'exemption préserve les décisions héritées inchangées et refuse les textes nouveaux ou altérés ; l'objet, l'auteur et les confirmations obligatoires restent contrôlés.
- Une transition actuelle échappe néanmoins à la promesse : `close` produit effectivement `DONE` avec `Chosen option: REJECT` gelé, après lecture courante des autorités. La gate installée ne l'empêche pas. Résultat reproduit deux fois.
- Les doublons d'identifiant contradictoires ne sont pas détectés ; redéclarer une baseline plus récente avec l'ancienne décision d'adoption rétablit aussi l'exemption. Ces essais exigent une capacité d'écriture des records/Git, précisée ci-dessous. Aucune correction réalisée.

#### Périmètre, méthode et privilèges réellement utilisés

Toutes les lectures de données de projet ont concerné `~/Projets/squelette-controle-3.15.2/` ; toutes les écritures sont sous `runs/t02/`. `source/` est resté en lecture seule. Aucun réseau, remote, autre dépôt réel, publication, installation système ou configuration Git globale. Python/Git et leurs bibliothèques système servent uniquement de runtime. Les commandes ont été exécutées avec l'élévation de filesystem nécessaire pour ce dossier, dans le mandat explicite de contrôle ; cette élévation ne signifie pas un rôle root ni une autorisation fictive du squelette.

Le source exporté ne contenait pas de `.git`. Les helpers de `source/tests/test_template.py` ont copié son arbre, initialisé des dépôts locaux et fabriqué l'état Normal Mode et les records. Les copies et leurs `.git`, commits, baselines et décisions sont entièrement fictifs. `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `TMPDIR=~/Projets/squelette-controle-3.15.2/runs/t02/tmp`, `PYTHONDONTWRITEBYTECODE=1`. L'identité Git est locale (`Fixture Owner`, `fixture@example.invalid`). `PROJECT_CONTROL_HOOK_OVERRIDE` était absent ; aucun override ni `--no-verify` n'a été utilisé.

Les scénarios historiques sont construits par écriture directe de fichiers puis commits de fixture **avant installation de la gate** : cette capacité de préparation permet de créer un passé artificiel qu'une transition moderne stricte refuserait. Pour le défaut `close`, WI-001 est d'abord créé et démarré sous `AUTHORIZE`, puis son HD-102 est réécrit `REJECT`, committé et déclaré historique via `legacy_baseline`. Ce passé n'est pas présenté comme une décision humaine authentique. Après cette préparation, la reproduction installe réellement la gate, lit le manifeste courant, enregistre la relecture et appelle le véritable CLI `close` sans autre modification de code/record ni override. La seconde exécution part du commit précédant ce close dans une autre copie.

Les helpers ont reçu des wrappers de journalisation et de marquage, **pas de substitution de validation**. Chaque appel contrôlé lance le véritable `scripts/project_control.py` de la copie par un sous-processus Python. Empreinte du contrôleur source : `8bea8d26d25f61f334f9c584c41ae967475533b80fe5ac013673dee4572937be`. Les 27 copies conservées ont toutes le même contrôleur ; voir `code-integrity.tsv`. Les logs détaillent CWD, commande, code retour, stdout et stderr ; `results.json` fournit aussi les exemptions et les SHA-256 observés à chaque étape, puis `sha256.tsv` les empreintes des fichiers de preuve conservés.

##### Marquage des fixtures et conflit de format

Les fichiers de test Python ont un commentaire initial portant le marqueur ; les fichiers Markdown/prose et logs créés par le harnais l'ont en tête. Les valeurs descriptives `objective`, `summary`, `Decision` sont marquées lorsque disponibles. Les copies octet-identiques du source sont des objets de test, non de nouveaux mandats. Un préfixe textuel brut en tête d'un JSON imposerait un JSON invalide, et ajouter une clé de commentaire ferait échouer les schémas fermés : les JSON validés restent donc syntaxiquement conformes, sans préfixe brut ; leurs champs descriptifs sont marqués quand le schéma le permet, et leurs chemins sont tous sous les répertoires fictifs. Les métadonnées Git et les fichiers copiés du core gardent également leur format exact. Cette exception de représentation est explicitée ; aucun contenu fictif ne vaut autorisation.

#### Matrice des résultats exécutés

`exit 0` signifie que le CLI accepte ; `exit 1` qu'il refuse. Les contrôles de refus comparent les fichiers de travail, HEAD, branche et statut Git avant/après ; l'intérieur de `.git` n'entre pas dans ce snapshot.

| Scénario | Résultat observé | HD exemptées | État inchangé | Preuve CLI |
|---|---|---|---|---|
| standard AUTHORIZE | exit 0 | HD-101, HD-102 | oui | `logs/025-01-standard-authorize-control.log` |
| legacy unchanged | exit 0 | HD-101, HD-102 | oui | `logs/056-02-legacy-unchanged-control.log` |
| legacy altered | exit 1 | HD-101 | oui | `logs/092-03-legacy-altered-control.log` |
| new after baseline | exit 1 | HD-101 | oui | `logs/124-04-new-after-baseline-control.log` |
| block moved same file | exit 0 | HD-101, HD-102 | oui | `logs/184-05-moved-inside-register-control.log` |
| block moved other file | exit 1 | HD-101 | oui | `logs/220-06-moved-new-file-control.log` |
| same ID duplicate identical | exit 0 | HD-101, HD-102 | oui | `logs/256-07-duplicate-id-identical-control.log` |
| same ID duplicate REJECT last | exit 0 | HD-101, HD-102 | oui | `logs/292-08-duplicate-id-contradictory-control.log` |
| copy text new ID | exit 1 | HD-101, HD-102 | oui | `logs/328-09-new-id-copy-control.log` |
| rewritten then restored identical | exit 0 | HD-101, HD-102 | oui | `logs/369-10-rewritten-identical-control.log` |
| before baseline redeclaration | exit 1 | HD-101 | oui | `logs/405-11-baseline-redeclared-control.log` |
| after baseline redeclaration same authority | exit 0 | HD-101, HD-102, HD-105 | oui | `logs/417-11-baseline-redeclared-control.log` |
| create from frozen REJECT | exit 1 | HD-101, HD-201 | oui | `logs/447-12-create-frozen-reject-control.log` |
| block from frozen REJECT | exit 1 | HD-101, HD-102, HD-201 | oui | `logs/478-13-block-frozen-reject-control.log` |
| resume from frozen REJECT | exit 1 | HD-101, HD-102, HD-201, HD-202 | oui | `logs/515-14-resume-frozen-reject-control.log` |
| close with frozen REJECT mandate | exit 1 | HD-101, HD-102 | oui | `logs/550-15-close-frozen-reject-control.log` |
| acknowledge frozen REJECT after current reading | exit 0 | HD-101, HD-102 | non mesuré | `logs/556-15-close-frozen-reject-control.log` |
| close frozen REJECT after current reading, gate installed | exit 0 | HD-101, HD-102 | non — transition acceptée | `logs/560-15-close-frozen-reject-control.log` |
| audit after close with frozen REJECT | exit 0 | HD-101, HD-102 | oui | `logs/567-15-close-frozen-reject-control.log` |
| 16-confirmation-template current create | exit 0 | aucune | non — transition acceptée | `logs/592-16-confirmation-template-control.log` |
| 16-confirmation-template audit created work item | exit 0 | aucune | oui | `logs/599-16-confirmation-template-control.log` |
| 17-confirmation-ok-go current create | exit 0 | aucune | non — transition acceptée | `logs/624-17-confirmation-ok-go-control.log` |
| 17-confirmation-ok-go audit created work item | exit 0 | aucune | oui | `logs/631-17-confirmation-ok-go-control.log` |
| 18-confirmation-identical current create | exit 1 | aucune | oui | `logs/656-18-confirmation-identical-control.log` |
| 19-confirmation-missing current create | exit 1 | aucune | oui | `logs/681-19-confirmation-missing-control.log` |
| close same REJECT without exemption with current reading | exit 1 | aucune | oui | `logs/724-20-close-modern-reject-control.log` |
| 21-frozen-no-authorizer | exit 1 | HD-101, HD-102 | oui | `logs/755-21-frozen-no-authorizer-control.log` |
| 22-frozen-no-decision | exit 1 | HD-101, HD-102 | oui | `logs/786-22-frozen-no-decision-control.log` |
| 23-frozen-no-confirmations | exit 1 | HD-101, HD-102 | oui | `logs/817-23-frozen-no-confirmations-control.log` |
| preflight same frozen REJECT before close replay | exit 1 | HD-101, HD-102 | non mesuré | `logs/822-24-close-replay-control.log` |
| independent close replay frozen REJECT | exit 0 | HD-101, HD-102 | non — transition acceptée | `logs/827-24-close-replay-control.log` |

#### Constat T02-F1 — `close` bénéficie de l'exemption historique (sévérité élevée, P1)

**Promesse contredite.** `source/docs/agent-governance/AGENTS.core.md:391-398`, `source/project_control/README.md:224` et le commentaire `source/scripts/project_control.py:4850-4852` indiquent que les transitions actuelles, explicitement `close`, lisent leur mandat en entier et ne bénéficient pas de l'exemption. Pourtant, le corps de `close_work_item` (`source/scripts/project_control.py:5149-5278`) ne réexamine pas les HD avec le mode strict : ses audits passent par `validate_record_links` (`:1426-1452`) qui désactive le contrôle du choix pour `frozen_decisions`.

**Séquence vérifiée.** Dans `15-close-frozen-reject/`, WI-001 est IN_PROGRESS, HD-102 porte REJECT et fait partie de la baseline `468d8854476f2d1f6d052571eff56f347aaed809`. Le premier `close` refuse uniquement la preuve de lecture périmée (`logs/550-15-close-frozen-reject-control.log:12`). Après `install-gate`, `context-manifest --json` et `acknowledge-authorities` avec le digest courant, le `close` passe (`logs/560-15-close-frozen-reject-control.log:12`) et committe DONE au HEAD `8f0bf0c52fd489a492865bea42c0acb5fa6a53f5`. L'audit final passe (`logs/567-15-close-frozen-reject-control.log`). Le record conservé porte `status: DONE` à `15-close-frozen-reject/project_control/work-items/WI-001.json:9` et HD-102 garde `Chosen option: REJECT` dans le registre.

**Contre-vérifications.** Sur le même mandat sans l'exemption et avec la lecture déjà fraîche, `close` refuse explicitement `Chosen option is not AUTHORIZE: REJECT`, sans modifier l'état (`logs/724-20-close-modern-reject-control.log:12`). La copie `24-close-replay/` montre aussi un `preflight` refusant `HUMAN_AUTHORIZATION` (`logs/822-24-close-replay-control.log`) puis un `close` accepté (`logs/827-24-close-replay-control.log:12`), sans changement de la décision entre les deux.

**Impact et limite.** Une clôture actuelle d'un chantier en cours peut ainsi être validée/committée contre un refus historique que le preflight refuse. La démonstration utilise une applicabilité explicite NOT_APPLICABLE pour code/tests/intégration/runtime afin d'isoler le mandat ; elle ne montre pas de falsification de preuves ni d'autorisation de démarrer un nouveau chantier via `start`. `create-work-item`, `block` et `resume` avec un REJECT gelé ont tous refusé. L'état historique artificiel demande un auteur capable de modifier les records et de préparer la baseline ; ce n'est pas une escalade de privilèges système. Aucun contournement du code ou de la gate n'est nécessaire **au moment du close**.

**Reproduction autonome depuis le commit de preuve.** Les commandes suivantes créent uniquement une nouvelle copie T-02 ; le répertoire d'arrivée doit être neuf. Le retour attendu du dernier `close` est 0 et DONE. Aucun réseau n'est utilisé.

```sh
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_CONFIG_NOSYSTEM=1
export TMPDIR=~/Projets/squelette-controle-3.15.2/runs/t02/tmp
unset PROJECT_CONTROL_HOOK_OVERRIDE
python3 -B - <<'PY_REPLAY'
from pathlib import Path
import shutil
r = Path('~/Projets/squelette-controle-3.15.2/runs/t02')
shutil.copytree(r/'15-close-frozen-reject', r/'relecture-close-neuve')
PY_REPLAY
cd ~/Projets/squelette-controle-3.15.2/runs/t02/relecture-close-neuve
git switch -C main 3786aead616f16e24c1b22b34d33f4cab6fec754
python3 -B scripts/project_control.py install-gate
python3 -B scripts/project_control.py preflight WI-001
python3 -B scripts/project_control.py close WI-001
python3 -B scripts/project_control.py audit
```

Le preflight est attendu en échec : son journal comporte le refus HUMAN_AUTHORIZATION à la ligne 38 et aussi un refus de branche à la ligne 44. Son code retour ne suffit donc pas à isoler l’autorisation ; c’est la contre-épreuve `close` sans exemption, log 724, qui l’isole. Poursuivre vers `close` fait précisément partie de ce test adversarial autorisé. Le reset de branche `switch -C` ne concerne que la copie créée pour ce test ; aucun dépôt de travail réel n'est ciblé.

#### Constat T02-F2 — doublons contradictoires ignorés (sévérité moyenne, P2)

Le registre promet des identifiants stables, jamais réutilisés (`source/docs/governance/HUMAN_DECISIONS.md:5`). `decision_block` (`source/scripts/project_control.py:733-740`) prend la première occurrence. `frozen_decision_refs` (`:4871-4875`) compare uniquement ce premier bloc ; le jeu d'identifiants de `validate_record_links` (`:1437`) efface les doublons.

Dans `08-duplicate-id-contradictory/`, une première HD-102 historique inchangée porte LEGACY_APPROVED ; un second bloc `## HD-102` ajouté après la baseline porte REJECT. L'audit accepte, HD-102 est encore exemptée (`logs/292-08-duplicate-id-contradictory-control.log`). La copie 07 accepte aussi le doublon identique. Copier le texte sous un **nouvel** identifiant HD-109, référencé par le WI, est en revanche refusé : il n'existe pas dans la baseline (`logs/328-09-new-id-copy-control.log`).

Privilège : édition directe et commit du registre sur la copie, préparation sans gate installée. L'essai montre une incohérence historique non détectée par audit ; il ne démontre pas à lui seul qu'une nouvelle transition est autorisée par le second bloc. L'ordre des doublons devient sémantiquement déterminant. Les fichiers conservés et leur audit se rejouent en lecture seule :

```sh
cd ~/Projets/squelette-controle-3.15.2/runs/t02/08-duplicate-id-contradictory
GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 python3 -B scripts/project_control.py audit
```

#### Constat T02-F3 — baseline réassignable avec l'ancienne HD (sévérité moyenne / limite de confiance, P2)

`legacy_baseline` (`source/scripts/project_control.py:4811-4833`) vérifie un commit existant/ancêtre et une décision enregistrée utilisable hors vocabulaire AUTHORIZE. Il ne lie pas le SHA déclaré au texte de cette décision et ne vérifie pas l'immutabilité de la déclaration.

Dans `11-baseline-redeclared/`, HD-102 historique est modifiée en REJECT et committée ; l'audit refuse, l'exemption est perdue (`logs/405-11-baseline-redeclared-control.log`). Seul `project-state.v1.json.legacy_baseline.head` est ensuite avancé vers le commit de la modification ; `human_decision_ref` reste HD-105, dont le texte continue de nommer **l'ancien** SHA. L'audit repasse (`logs/417-11-baseline-redeclared-control.log`) et considère HD-102 et HD-105 gelées. Il n'a pas substitué HEAD implicitement : il a accepté la redéclaration explicite sans nouvelle correspondance d'autorité.

Privilège : pouvoir écrire Project State et committer une histoire préparée. Les commits de corruption ont été fabriqués sans gate installée ; ce scénario ne prouve pas qu'une mutation refusée franchirait une gate déjà active. Il prouve qu'une déclaration contrôlée par le même auteur que les records ne constitue pas un ancrage historique immuable. L'adoption peut légitimement être déclarative ; la limite doit être distinguée du défaut de close, qui viole une promesse explicite de transition actuelle.

#### Résultats attendus et limites de représentation

- Un bloc legacy inchangé est accepté ; un bloc modifié, un nouveau bloc post-baseline référencé, un nouvel identifiant copié et le déplacement dans un autre fichier sont refusés.
- Déplacer le bloc dans le même registre conserve son exemption. Le contrôleur compare son contenu avec `.strip()`, pas sa position. Il ne promet pas d'identité de position.
- Modifier puis restaurer les octets d'origine dans deux commits rend l'exemption. C'est une comparaison d'état courant, sans analyse des modifications intermédiaires. La formule « inchangée depuis » est plus large que ce contrôle ; ce résultat n'autorise pas à conclure à une identité continue dans l'histoire Git.
- Même présentes telles quelles dans la baseline, les décisions avec auteur UNKNOWN, objet UNKNOWN, ou Folder scope sans confirmations restent refusées (`logs/755`, `786`, `817`). L'exemption ne supprime donc pas ces trois contrôles.
- Tous les audits de la matrice sont restés en lecture seule selon le snapshot ; les refus de transition contrôlés n'ont modifié ni records, ni HEAD, ni branche, ni état Git visible. Ce n'est pas une preuve d'absence de toute écriture interne à `.git`.

#### T02-F4 — Portée mécanique des confirmations (T-06 ; limite de forme, sévérité modérée)

Aucune opération n'a été effectuée dans un dossier cible : les chemins et confirmations sont uniquement des chaînes dans des HD fictives.

Le modèle « décision qui sort du dossier accordé » de `source/docs/governance/HUMAN_DECISIONS.md:44-75` a été recopié, en remplaçant les identifiants NNN par HD-201/WI-001 pour relier le chantier ; les autres placeholders sont restés littéraux, avec le marqueur dans Decision. `create-work-item` puis `audit` passent (`logs/592`, `599`). Le `Folder scope` reste alors littéralement `<chemin exact du dossier ou du dépôt visé>` ; les deux confirmations sont les placeholders distincts du modèle et `Authorized by` reste `<Project Owner>`.

Avec un Folder scope nommant le chemin fictif sous `runs/t02/` et `Confirmation 1: ok`, `Confirmation 2: go`, le même create et l'audit passent (`logs/624`, `631`). Avec deux fois `ok`, le create refuse (`logs/656`) ; avec la seconde confirmation absente, il refuse (`logs/681`).

**Interprétation (P2 pour la promesse de format humain).** `out_of_folder_decision_errors` (`source/scripts/project_control.py:774-801`) contrôle la présence, UNKNOWN et l'inégalité des chaînes ; il ne vérifie pas qu'elles nomment le dossier, qu'elles sont réellement humaines, qu'elles proviennent de deux échanges, ni que les placeholders ont été remplacés. `AGENTS.core.md:300-305` demande davantage au niveau doctrinal. La non-authentification humaine est une limite de la donnée déclarative ; l'acceptation de placeholders/« ok » est une insuffisance de validation de la forme promise. Aucun droit filesystem n'est acquis par ce mécanisme.

#### Artefacts et reproductibilité

`run_t02.py`, `continue_t02.py`, `supplement_t02.py`, `controls_t02.py`, `replay_t02.py` contiennent les constructions et appels CLI. Les scripts ont été lancés successivement une fois ; ils préservent des répertoires nommés et refusent donc une relance sur les mêmes destinations déjà présentes. Les CWD et commandes complets sont dans chacun des 800+ petits logs ; les recettes ci-dessus permettent les vérifications décisives sur les copies conservées. Les traces des trois interruptions du **harnais** (commit sans changement, mauvaise référence de helper, découpage de bloc) sont conservées sous `aborted*`; elles n'ont pas été classées comme défaut du produit. Elles ont été corrigées seulement dans les outils de test avant reprise.

Aucune suite complète n'a été relancée par ce sous-contrôle ; le parent exécute la campagne globale. La matrice couvre 31 observations CLI sur 24 scénarios, avec deux reproductions positives du défaut close et un contrôle négatif. Ce rapport ne généralise pas au-delà des formats et privilèges explicitement exercés.
### T-01 — Preuves de réussite contredites : observations et limites

1. Les refus annoncés fonctionnent sur les sorties usuelles : unittest/pytest échoués, toutes les pièces échouées, pièce vide et absence de pièce. Une erreur placée après 2 Mio reste détectée.
2. Le contrôle reste une heuristique fragile : un texte neutre ou un encodage non UTF-8 peut laisser passer une déclaration PASS sans aucune sortie positive. À l'inverse, un vrai test de fixture réussi, qui imprime un diagnostic d'erreur attendu, est refusé.
3. Aucun produit réel, runtime, réseau ou autorité réelle n'a été activé. Ce dossier apporte les fixtures, commandes et sorties pour qualifier les limites ; aucune correction du squelette n'a été faite.

#### Périmètre et méthode

Toutes les actions de contrôle sont restées sous `~/Projets/squelette-controle-3.15.2/`; `source/` n'a été que lu. Les écritures ont été limitées à `runs/t01/`. L'export de 116 fichiers n'avait pas de `.git` : la fixture `runs/t01/base/` possède donc un Git autonome, sans remote. L'initialisation fictive reprend les helpers fournis par `source/tests/test_template.py` (construction manuelle de la fixture de bootstrap) puis vérifie `bootstrap-closeout` et `audit`. Ce n'est pas une interview humaine réelle ni une homologation de son contenu.

Le cycle mesuré est ensuite exécuté par les vraies commandes CLI du produit : `install-gate`, `create-work-item`, `context-manifest`, `start`, commit du changement fictif, merge sur `main`, commit de preuves et `close`. Le chantier `WI-001` ne rend applicable que la gate `tests`, avec `runtime_target=NOT_APPLICABLE`. Chaque scénario repart d'une copie indépendante de la même baseline intégrée `449a55f9c4bae5bec39e75507d899a6dd96ba079`. La gate est installée, identique à sa référence, active lors du commit de preuve. Aucun `PROJECT_CONTROL_HOOK_OVERRIDE` n'a servi. Les scénarios n'éditent que les preuves autorisées ; ils ne changent pas le contrôleur, le schéma ni le hook.

Les 19 scénarios de la matrice possèdent chacun un `close`, un `audit` et un `status --json` réellement exécutés. Deux expériences supplémentaires exécutent aussi un sous-processus unittest de fixture. Le premier essai a laissé `ERROR:` après le nom du test, sur la même ligne : accepté ; l'essai v2 place ce diagnostic au début de la ligne et reproduit le faux positif. Le premier essai et son assertion de harness échouée sont conservés dans `actual-pass-commands.txt` et `cases/actual_pass_expected_error/` ; ils ne sont pas présentés comme un refus.

##### Marquage des fixtures et conflit de format explicite

Les fichiers texte fictifs créés par le contrôle portent l'avertissement en tête (un commentaire pour les fichiers Python). Les rapports de preuve JSON doivent rester du JSON valide et leur schéma interdit les propriétés supplémentaires : une ligne libre en tête les ferait échouer avant le comportement testé. Leur premier champ est donc `summary`, dont la valeur commence par l'avertissement. Les records JSON produits par les helpers et la CLI, et les métadonnées Git générées, ne peuvent pas tous recevoir un préfixe sans altérer le test : leur caractère fictif est documenté ici et par leur confinement à `runs/t01/`. Les documents du produit sont des copies exactes, pas de nouvelles autorités. Le scénario `empty` garde intentionnellement zéro octet ; l'ajout d'un avertissement supprimerait précisément le cas testé. Le scénario UTF-16 contient l'avertissement dans ce même encodage. Aucun de ces fichiers n'autorise quoi que ce soit hors de la fixture.

#### Promesse testée et portée à conserver

`source/project_control/README.md:152` à `162` précise le quantificateur **toutes** les pièces texte, énumère les marqueurs et exclut les pièces binaires. `source/docs/agent-governance/AGENTS.core.md` reprend la même promesse. La vérité indépendante d'une exécution est expressément exclue (`source/project_control/README.md:177`, `source/docs/governance/DEFINITION_OF_DONE.md:37`). Les résultats ci-dessous ne doivent donc pas être présentés comme la rupture d'une attestation cryptographique ou d'une barrière contre un auteur malveillant qui peut fournir les rapports.

Implémentation déterminante : `source/scripts/project_control.py:690` (regex), `:700` (UTF-8 strict), `:709` (premier marqueur trouvé sans interpréter le résultat final), `:4723` (lecture complète), `:4727` (refus du vide), `:4772` à `:4784` (condition `read and all(...)`). SHA-256 du contrôleur source et de toutes ses copies : `8bea8d26d25f61f334f9c584c41ae967475533b80fe5ac013673dee4572937be`.

#### F-T01-01 — Faux positif sur un test réussi imprimant une erreur attendue

**Nature / gravité : anomalie de robustesse, modérée pour l'usage.** Elle bloque la clôture honnête d'un test de rejet d'entrée invalide. Elle ne donne aucun accès supplémentaire et ne détruit aucune preuve. Le privilège nécessaire est seulement celui du contributeur autorisé à committer son rapport de test ; aucune modification de la gate ou d'un record administratif n'est requise.

La fixture `runs/t01/cases/actual_pass_expected_error_v2/reports/evidence/WI-001/actual_test.py` vérifie qu'une conversion invalide lève bien `ValueError`. Le sous-processus unittest réussit avec le code 0. Sa sortie contient à la ligne 3 `ERROR: invalid input (expected diagnostic)`, puis `Ran 1 test` et `OK` aux lignes 7 et 9. Le rapport déclare honnêtement PASS et cite les bons octets. Pourtant `close` sort avec le code 1 et conserve `WI-001` en `IN_PROGRESS`.

Preuve d'exécution : `runs/t01/actual-pass-v2-commands.txt:7` (commande du test), `:8` (code 0), `:17` (OK), `:38` (commande de clôture), `:39` (code 1), `:46` (refus qui cite le diagnostic attendu). Le commit des trois fichiers a été accepté par la gate, lignes 22 à 36. Message exact :

```text
result is PASS but every text artifact it cites reports a failure: reports/evidence/WI-001/actual-output.txt ('ERROR: invalid input (expected diagnostic)')
```

SHA-256 de `actual-output.txt` : `2272dbeef5dd16f1b8229e1bd3789e0c5d8aa7a63a82fd7ed8b64421ddc168bb`.
SHA-256 de `tests.json` : `166342e9ac3701330d326bfc654ab652676c7a337937534914de671e4a0b7467`.

Cause : la présence d'une seule ligne correspondante suffit à qualifier toute la pièce d'échec, même si cette ligne est une observation attendue et que le bilan final est positif. Le scénario synthétique `falsepositive_quoted_failed` démontre aussi le refus d'un historique négatif cité dans la même pièce que le résultat final OK. Ce n'est pas le cas multi-pièces honnête, qui passe.

#### L-T01-02 — Une pièce neutre suffit à supprimer le refus

**Nature / gravité : limite de garantie documentée par le quantificateur, modérée si présentée comme une validation du résultat.** Ce n'est pas une escalade de privilèges. Un auteur de preuve autorisé n'a besoin que d'ajouter une pièce texte à son rapport.

Témoin : `unittest_failed` cite seulement un journal de 81 octets qui termine sur `FAILED (failures=2)` ; refus `close=1`. Le scénario `failed_plus_marker_only` cite exactement ces mêmes 81 octets (SHA identique), plus une pièce de 49 octets qui ne contient que l'avertissement de fixture, sans résultat de test. Le rapport obtient `close=0`, `DONE`, puis `audit=0` et `status=0`. Aucun résultat positif n'a été ajouté.

Le journal du refus est `runs/t01/logs/0046-unittest_failed-python3.14.txt:12`. Les journaux d'acceptation sont `runs/t01/logs/0156-failed_plus_marker_only-python3.14.txt:12`, puis `0157-...` et `0158-...`. Le second fichier est lisible en entier à `runs/t01/cases/failed_plus_marker_only/reports/evidence/WI-001/failed_plus_marker_only-2.txt:1`. Les SHA-256 des deux pièces sont respectivement `2aeabc3699cbed0f0165e67651ffa33053064096045cdd95aa39137ace845549` et `a512557ef20a75e81ffa02e7a42a553a13f7f3ad4a88486260bd349ad1261f6d`.

Cause : `all(marker for _, marker in read)` est faux dès qu'une pièce lisible n'a aucun marqueur. Aucune preuve de succès positive n'est exigée de cette pièce. Cela respecte littéralement la règle « toutes les pièces », mais ne permet pas d'affirmer qu'une campagne ratée ne pourrait passer qu'accompagnée de la campagne qui a réussi. Le scénario `failed_plus_neutral` reproduit le même effet avec un inventaire neutre ordinaire.

#### L-T01-03 — Encodage et présentation du texte changent le verdict

**Nature / gravité : limites de reconnaissance, faible à modérée selon les formats réellement produits.** Le cas binaire est explicitement exclu par la documentation ; il ne constitue donc pas une rupture de cette exclusion. L'effet d'un seul octet non UTF-8 sur un journal par ailleurs lisible et l'absence de traitement ANSI rendent néanmoins la protection facile à perdre, même accidentellement.

`failure_invalid_utf8` reprend les 81 octets du témoin négatif et ajoute seulement `0xff`. Tout le fichier est alors classé non texte, la liste `read` devient vide et `close` produit DONE, suivi d'un audit PASS. Le marqueur FAILED reste présent dans les octets. SHA-256 de la pièce de 82 octets : `5a0467d518ea83bb51e9f8b79fb1c0ee38ac41becd31da1fdebe920aff2f3fe0`. Sortie : `runs/t01/logs/0096-failure_invalid_utf8-python3.14.txt:12`; audit : `0097-...`; état : `0098-...`.

`failure_utf16` montre le même effet pour un journal UTF-16 avec BOM, qui est du texte pour un lecteur mais exclu par le décodage UTF-8 strict du produit. `binary_only` passe également sans pièce textuelle : comportement conforme à cette frontière, mais aucune pièce n'y témoigne d'un succès. À l'inverse, `failed_plus_binary` est bien refusé : une pièce binaire supplémentaire ne dilue pas un échec UTF-8 reconnu.

`failure_ansi` contient les octets `\x1b[31mFAILED\x1b[0m (2 cases unsuccessful)` : un terminal affiche FAILED, mais les regex ancrées ne reconnaissent pas cette ligne et le rapport passe. Cette fixture ne comporte pas de décompte `failures=2`, qui aurait offert un second marqueur reconnu ; aucune conclusion n'est tirée pour tous les formats colorés. `lowercase_failed` est aussi accepté, conformément au vocabulaire sensible à la casse. Sources : `source/scripts/project_control.py:690` et `:700`.

#### Contrôles positifs et négatifs réussis

Le témoin `standard_pass` clôture DONE. `unittest_failed`, `all_failed` et `pytest_failed` sont refusés et citent les lignes négatives ; les HEAD de preuve et de fin restent identiques. La pièce de zéro octet est refusée par `empty evidence file`, et une liste d'artefacts vide par `evidence.artifacts: too few items`. L'échec UTF-8 accompagné d'un binaire reste refusé. Le mélange d'une pièce négative et d'une pièce terminant sur OK est accepté, sans disparition de l'échec. `FAILED_CASES=0` ne déclenche pas de faux positif.

Le fichier `failure_large` mesure exactement 2 097 222 octets : le FAILED se trouve après les 2 097 152 octets de remplissage. La clôture est refusée. Il n'existe pas de taille maximale de lecture dans la fonction inspectée (`read_bytes()` sans borne) : « au-delà de la taille lue » n'est donc pas un seuil caché atteint par ce test. Le test confirme une lecture au-delà de 2 Mio et ne constitue pas une mesure de résistance à l'épuisement mémoire.

L'audit reste PASS dans les scénarios refusés parce que le chantier est encore `IN_PROGRESS` et que les rapports rejetés ne sont pas devenus les références d'une clôture. Ce PASS ne valide pas la campagne refusée et ne doit pas être compté comme un contournement supplémentaire.

#### Matrice exécutée

| Scénario | Pièces / comportement | close | État final | audit | status |
|---|---|---:|---|---:|---:|
| standard_pass | Témoin positif : OK | 0 | DONE | 0 | 0 |
| unittest_failed | Témoin négatif : FAILED (failures=2) | 1 | IN_PROGRESS | 0 | 0 |
| all_failed | Deux pièces négatives reconnues | 1 | IN_PROGRESS | 0 | 0 |
| empty | 0 octet : refus structurel | 1 | IN_PROGRESS | 0 | 0 |
| binary_only | Aucun texte lisible : accepté | 0 | DONE | 0 | 0 |
| failed_plus_binary | Binaire ne dilue pas le texte échoué | 1 | IN_PROGRESS | 0 | 0 |
| failure_invalid_utf8 | Même FAILED, suivi de 0xff | 0 | DONE | 0 | 0 |
| failure_utf16 | FAILED en UTF-16 avec BOM | 0 | DONE | 0 | 0 |
| failure_ansi | FAILED entouré de couleur ANSI | 0 | DONE | 0 | 0 |
| failure_large | FAILED après 2 Mio : détecté | 1 | IN_PROGRESS | 0 | 0 |
| mixed_red_green | Échec conservé avec un succès explicite | 0 | DONE | 0 | 0 |
| failed_plus_neutral | Échec + inventaire neutre : accepté | 0 | DONE | 0 | 0 |
| failed_plus_marker_only | Échec + simple étiquette de fixture : accepté | 0 | DONE | 0 | 0 |
| falsepositive_expected_error | Diagnostic attendu + OK : refus | 1 | IN_PROGRESS | 0 | 0 |
| falsepositive_word_boundary | FAILED_CASES=0 : accepté, pas de faux positif | 0 | DONE | 0 | 0 |
| falsepositive_quoted_failed | Ancien échec cité + OK final : refus | 1 | IN_PROGRESS | 0 | 0 |
| empty_artifact_list | Liste vide : refus schéma | 1 | IN_PROGRESS | 0 | 0 |
| lowercase_failed | Variante minuscule non reconnue | 0 | DONE | 0 | 0 |
| pytest_failed | Résumé pytest négatif reconnu | 1 | IN_PROGRESS | 0 | 0 |
| actual_pass_expected_error | Vrai unittest, diagnostic au milieu de ligne | 0 | DONE | non exécuté | non exécuté |
| actual_pass_expected_error_v2 | Vrai unittest code 0, diagnostic en début de ligne | 1 | IN_PROGRESS | non exécuté | non exécuté |

#### Reproduction et traçabilité

Depuis la racine accordée, une nouvelle campagne complète, sans écraser les copies conservées :

```sh
python3 -B runs/t01/run_matrix.py replay-001
```

`replay-001` doit désigner un nouveau sous-dossier de `runs/t01/`. Le script refuse de réutiliser une baseline existante. Il importe les helpers de test source avec génération de bytecode désactivée ; aucun dossier temporaire extérieur n'est utilisé. Les configurations Git globales et système sont neutralisées par une configuration locale à la campagne et un dossier de templates vide. Aucun remote ni appel réseau n'est nécessaire. Les chemins de fichiers Git ajoutés sont explicites.

Pour le faux positif réellement exécuté, le test et la preuve sont conservés dans `cases/actual_pass_expected_error_v2/`. Dans cette copie, rejouer `python3 -B reports/evidence/WI-001/actual_test.py` démontre le code 0 et le bilan OK ; rejouer `python3 -B scripts/project_control.py close WI-001 --test-evidence reports/evidence/WI-001/tests.json` reproduit le refus. Ces commandes sont déjà consignées, avec leurs codes retour, dans `actual-pass-v2-commands.txt`. Le fichier d'artefact contient la sortie de l'exécution enregistrée ; sa durée précise n'est pas supposée identique à chaque nouvelle exécution.

`results.json` contient pour chaque scénario les SHA-256 du rapport et du Work Item, les SHA-256 et tailles des pièces, les HEAD avant/après et les chemins de trois journaux. Il contient aussi la liste chronologique des 219 commandes de la matrice avec leur cwd, arguments et code retour. Les journaux portent les commandes exactes et leurs sorties. Les horodatages de rapport et les commits varient lors d'une reproduction ; les verdicts et le contenu des pièces synthétiques doivent rester identiques.

`core-integrity.tsv` vérifie 528 comparaisons (24 fichiers core dans 22 copies), toutes identiques à `source/`, avec la seule normalisation du marqueur FIRST_START prévue par le produit. `source-sha256.tsv` inventorie les 116 fichiers source à la fin du contrôle. Le parent possède le contrôle d’intégrité global avant/après ; cette sous-campagne ne prétend pas avoir créé un instantané antérieur de tout le dossier source.

#### Index des preuves par scénario

| Scénario | Journal close | SHA-256 rapport |
|---|---|---|
| standard_pass | `runs/t01/logs/0036-standard_pass-python3.14.txt` | `84d1c4172cb9cce238e1740825b750a3ed1124179967a806bd117454567f6eb6` |
| unittest_failed | `runs/t01/logs/0046-unittest_failed-python3.14.txt` | `e49dadc26fabd21d1ac710c262ab8942c75e6b236a79100fc35541442eba71ff` |
| all_failed | `runs/t01/logs/0056-all_failed-python3.14.txt` | `0a10e030cf34d632d78d29fafb80e6efe07d0916f0f6fa1b62b865351da1e530` |
| empty | `runs/t01/logs/0066-empty-python3.14.txt` | `f3c3886043c74fd4df8700bdce28e41aedff459fa4e9e99e7acd540544a69968` |
| binary_only | `runs/t01/logs/0076-binary_only-python3.14.txt` | `fd1caa1a519e19e508d78a91be09f98d8df8b8066c5852e9008d456871fd4efb` |
| failed_plus_binary | `runs/t01/logs/0086-failed_plus_binary-python3.14.txt` | `5e2717722c940a413d6e6973a59e380bb2d2aac704a31b05181431ad7422ff78` |
| failure_invalid_utf8 | `runs/t01/logs/0096-failure_invalid_utf8-python3.14.txt` | `ad14d762eb98a33b2795437ddc168321cd0100396131e3318cb5e453d969c351` |
| failure_utf16 | `runs/t01/logs/0106-failure_utf16-python3.14.txt` | `2422ad6c9226dc961583eb7394ba5ac31acb52d6b87bcdaf458f347e873e21cf` |
| failure_ansi | `runs/t01/logs/0116-failure_ansi-python3.14.txt` | `5f2ff66f70fcc70964fd4246c237d46db94e92ce064f94f2623871cf049eaf31` |
| failure_large | `runs/t01/logs/0126-failure_large-python3.14.txt` | `ae8ddb6ad8d816f913d63e3dd36a5ae9c73cfdde9cf3be04ae5dd1adc781fbc5` |
| mixed_red_green | `runs/t01/logs/0136-mixed_red_green-python3.14.txt` | `023661e4a414303a87ebd1044b952c61a9159d6450e20ee1de8b2bec7e6b4cf0` |
| failed_plus_neutral | `runs/t01/logs/0146-failed_plus_neutral-python3.14.txt` | `57d7113b918de2abd1e870036daff724a713801a75d26c7203b957e6ffc70ff6` |
| failed_plus_marker_only | `runs/t01/logs/0156-failed_plus_marker_only-python3.14.txt` | `61659ba9dc7770913715900b6eb1014b2addd3911c1e7363626b85f10707b830` |
| falsepositive_expected_error | `runs/t01/logs/0166-falsepositive_expected_error-python3.14.txt` | `ce432e65e85f38265431eb5522f544f0de13868f4670a9c4e3132fb82d1d74ed` |
| falsepositive_word_boundary | `runs/t01/logs/0176-falsepositive_word_boundary-python3.14.txt` | `14a748a38f0e3cd9ba739e968c1ccc009ab8fe857527c11e0445f10a1aeb5060` |
| falsepositive_quoted_failed | `runs/t01/logs/0186-falsepositive_quoted_failed-python3.14.txt` | `aba912c0bdcb5b6293b666f5a4cd65b89bf0c604f5e6a81b09f41d38be00c5e1` |
| empty_artifact_list | `runs/t01/logs/0196-empty_artifact_list-python3.14.txt` | `976a648ce2376b8ba4b5cf866fa510dc1567341e6c2a30cee9eddffe840402a0` |
| lowercase_failed | `runs/t01/logs/0206-lowercase_failed-python3.14.txt` | `c800fb748609e4e76afd9c6eabfab0caad0a814d2e9ba965d76c9a6052fc5dbe` |
| pytest_failed | `runs/t01/logs/0216-pytest_failed-python3.14.txt` | `084129c48b6f965a356eee21cb7cab5b4fa7af750549e78cdb3b9b18a1ea69b9` |

#### Limites restantes

La campagne mesure le contrôle de cohérence de la gate tests ; elle ne relance pas les  tests fonctionnels complets du squelette, ne vérifie aucun runtime de production et ne prouve pas que les rapports inventés correspondent à un travail métier. Elle ne démontre aucun franchissement de permission système, aucune modification de la gate ni aucune falsification d'autorité réelle. La création d'un projet initialisé a volontairement employé les fixtures du produit et des décisions marquées fictives ; l'efficacité du parcours d'onboarding humain appartient à T-03. Les autres modes de preuve partagent la fonction inspectée, mais aucune clôture runtime/déploiement n'a été exécutée ici : toute extrapolation à ces gates doit rester explicitement une inférence de code.

## Observations non bloquantes et hypothèses restantes

Les observations O-T05 ci-dessous sont issues de la lecture du contrôleur, **sans échec reproductible exécuté dans cette campagne indépendante**. Leur sévérité reste non qualifiée ; aucune ne fonde le verdict. Elles ne sont pas des correctifs proposés. Le SHA-256 du fichier cité est celui donné dans l’état exact.

| ID | Objet, référence et protocole restant | Privilège nécessaire / limite |
|---|---|---|
| O-T05-01 | `scripts/project_control.py:3016` et `:3056` : comparer, dans un worktree lié jetable, le chemin installé et le chemin de hook effectivement consulté par Git ; comparer CLI pre-commit et vrai commit interdit en bootstrap. | Créer un worktree local et y installer la gate. Hypothèse de faux INSTALLED, non démontrée. |
| O-T05-02 | `:3559`, `:3588` : l’impossibilité de matérialiser l’index renvoie les seuls constats du disque, sans ajouter de FAIL. Comparer un index invalide masqué par un disque honnête, d’abord snapshot disponible puis indisponible. | Simulation d’une panne de `.git/worktrees`, privilège d’administration Git explicite. Aucun commit de ce scénario n’a été effectué. |
| O-T05-03 | `:2815` : tester un passager indexé pendant une fusion puis absent du disque, au-delà du passager visible couvert par la suite. | Écriture de l’index et du worktree de fixture ; aucun résultat expérimental indépendant. |
| O-T05-04 | Interrompre installation ou matérialisation au moment précis de la mutation et examiner le contrôle suivant. | Injection d’interruption à définir dans une copie ; le test d’interruption de `start` ne répond pas à ce point. |

O-T06-01 — La phrase « inchangée depuis » ne prouve pas une continuité historique : T-02 montre qu’une décision modifiée puis restaurée octet pour octet retrouve l’exemption. Cela correspond à une comparaison d’état, que le mandat demandait précisément d’examiner, sans contrôle des états intermédiaires. Privilège : écrire et committer le registre ; preuve `runs/t02/logs/369-10-rewritten-identical-control.log:6`, empreinte dans le registre des preuves. Aucune nouvelle transition stricte n’est réputée autorisée par cette seule observation.

O-T06-02 — Une gate absente est affichée comme telle tout en laissant `PASS: COMMIT_GATE` (`runs/t02/logs/417-11-baseline-redeclared-control.log:29`). C’est un signalement textuel exact, mais un code de succès ne garantit pas qu’un hook est installé. Ce comportement de configuration est distinct d’un défaut de l’installation, qui n’a pas été reproduit indépendamment ici.

## Suite livrée et portée de son résultat

La découverte trouve **133 tests** ; **132 sont exécutés, tous réussis**. Résultat exact : `Ran 132 tests in 486.552s`, puis `OK`. Le test `test_an_up_to_date_backup_reads_as_good_in_both_languages` est exclu avant exécution parce qu’il effectue un push local (`source/tests/test_template.py:5136`). Il ne faut donc pas annoncer « 133/133 » ni une suite intégrale sans réserve.

La suite provient d’une copie autonome intacte `runs/control/suite-project/`, sous Python 3.14.0 et Git 2.50.1 (Apple Git-155). Les temporaires ont été confinés à `runs/control/tmp/`. Le journal nominatif est `runs/control/suite.log` ; le lanceur est `runs/control/run_suite.py`. Les tests des modèles et de messages passent, mais n’exercent pas la comparaison de notices qui a révélé F-T03-01. Une suite verte n’annule donc pas les contre-exemples indépendants.

## Ce qui n’a pas été vérifié, et pourquoi

- Historique réel, tag et HEAD source ; évolution exécutée 3.6.1 → 3.15.2, décisions/preuves réellement anciennes : entrée historique absente. Aucun substitut fabriqué ne vaut cette vérification.
- Essais indépendants T-05 listés ci-dessus, après deux rejets de l’approbation automatique et en l’absence de réponse à la confirmation demandée. Ni permission déduite du silence, ni opération refusée reprise indirectement.
- La suite complète au sens strict : un push, même vers un dépôt local jetable, est interdit par le mandat ; son test a été exclu.
- Exhaustivité des formats de logs et épuisement mémoire : le grand fichier testé dépasse 2 Mio ; ce n’est pas un test de saturation. Pas de généralisation à toutes les sorties ANSI ou à tous les encodages.
- Clôtures runtime/déploiement, production, réseaux, authenticité d’une décision humaine, valeur métier des preuves, signatures d’auteurs : hors des campagnes réalisées et, pour plusieurs éléments, explicitement hors garantie du produit.
- Expérience d’initialisation limitée aux documents Markdown, sans aucun modèle annexe : T-03 a également consulté les schémas et deux fixtures JSON. Aucun code Python de logique n’a servi à résoudre le parcours, mais la stricte indépendance de cette aide documentaire n’est pas démontrée.
- Absence absolue d’écritures internes Git lors d’une commande dite lecture seule : les comparaisons de refus portent sur HEAD, branche, index/statut et fichiers de travail, pas sur tous les objets internes. Aucun résultat n’est présenté comme une expertise forensique exhaustive du disque.
- Conformité littérale du préfixe d’avertissement pour JSON, binaires, fichiers vides et métadonnées Git : impossibilité de représentation décrite dans la méthode. L’écart initial d’inventaire hors dossier est également conservé comme limite d’exécution du mandat.

## Registre des preuves décisives

Les numéros ci-dessous sont des lignes de fichier, comptées depuis 1. Les empreintes portent sur les fichiers complets, pas sur les seules lignes citées. Les matrices T-01 et T-02 donnent les cas complémentaires ; leurs inventaires propres permettent de retrouver toutes les pièces de ces campagnes.

| Constat / contrôle | Fichier et lignes utiles | SHA-256 du fichier |
|---|---|---|
| Intégrité avant | `runs/control/meta/source-before.json` — 1 | `f88c74e0d8e66b3f3dec8991a5ef721fc08d73b3c4c9bbeb13f388562c7a8042` |
| Intégrité après | `runs/control/meta/source-after.json` — 1 | `f88c74e0d8e66b3f3dec8991a5ef721fc08d73b3c4c9bbeb13f388562c7a8042` |
| Comparaison normalisée | `runs/control/meta/preflight.json` — 1 | `7b02eb0a0780af586d152fb8967b12069943e308035f0c935c8751a203b5c488` |
| Bilan intégrité/runtime | `runs/control/meta/verification.json` — 1 | `df4301a972c02b9e06faf9eb57c8530398d7c6f537d55fc1116c03dddbbc4e1a` |
| Suite 132 tests | `runs/control/suite.log` — 3 et fin | `b43f0a0e20ece530a60fe07fe80c31322ebe71b07477e82d4ef113bdd1a462ec` |
| T04 entrée manquante | `runs/t04/input-check.log` — 4–18 | `e7a48c30d8cd87732f2948f48f28fb36196266d5e5ba6c70cf89354d6636c9d4` |
| F-T03-01 témoin/A-B | `runs/t03/03-finish.log` — 67, 103, 139 | `2d4aa28776c72ae7b724271431692299f2d12ab43cece8e0188a8c9d71f0b732` |
| F-T03-01 architecture | `runs/t03/evidence/draft-architecture.md` — 5, 7 | `20fdbe0b8e62737f805a4a78ead6edd1ae81086593c09868b66298450a9d570e` |
| F-T03-01 ADR | `runs/t03/evidence/proposed-adr.md` — 5, 7 | `e91fdd7aca0ca339ea6f431141bef550a58142551097390eec264efac0fd2d5e` |
| T03 cycle complet | `runs/t03/06-cycle.log` — 34, 128, 171, 201 | `bc286ce16a09d674a31bc777a238701f1f4b6d27d81abf26ed98ba8e4db5fd87` |
| T02-F1 close accepté | `runs/t02/logs/560-15-close-frozen-reject-control.log` — 6, 12 | `36d826100a4b75936fa888fc4aeb6a2d59f9e159e01b50a627d07b5fba44f54b` |
| T02-F1 contre-épreuve | `runs/t02/logs/724-20-close-modern-reject-control.log` — 6, 12 | `ce177982c7365412a67655f5b19f678859df4a4ee32c5f7cd63c874e35dc3430` |
| T02-F1 réplication | `runs/t02/logs/827-24-close-replay-control.log` — 6, 12 | `e1c7d22a6c6fe274b788ecceff296e8a3c4d90fd8bfc028ff836fd90bfa5d9e1` |
| T02-F1 mandat REJECT | `runs/t02/15-close-frozen-reject/docs/governance/HUMAN_DECISIONS.md` — 10, 16 | `fccf47260b15abe24da677b2ecaafb8a3980a5a1e36f7a55dadcc38463190327` |
| T02-F1 état DONE | `runs/t02/15-close-frozen-reject/project_control/work-items/WI-001.json` — 9 | `1e939389898a27e6a340c0f384b09ce643873161abc1d06b21b9434febb86ed7` |
| T02-F1 preflight non isolé | `runs/t02/logs/822-24-close-replay-control.log` — 30, 38, 44 | `0fd32b8930fe09576b79f930e93903029af0bdc84b05da0f3ee9b27e8c539ecf` |
| T02-F2 doublon | `runs/t02/logs/292-08-duplicate-id-contradictory-control.log` — 6, 20, 29 | `bccdbacb4ca520137d11bd501445d8ee00fd5a0378a29e186f008a1710ed9064` |
| T02-F2 registre | `runs/t02/08-duplicate-id-contradictory/docs/governance/HUMAN_DECISIONS.md` — 10, 16, 40, 45 | `5656bc818a4ac26de280a1729d29f74bf4c4834bac08da38f258f157501a81ef` |
| T02-F3 avant redéclaration | `runs/t02/logs/405-11-baseline-redeclared-control.log` — 20 | `3a3528cf518455718209cf7c82e82d83c2bd38c4bc2c73e3a8828809b4aa9fee` |
| T02-F3 après redéclaration | `runs/t02/logs/417-11-baseline-redeclared-control.log` — 6, 29 | `ca8feb6236f89e08f9d2dea4e4904005f920a5ad0675505aa4ac964c03bb6e79` |
| T02-F3 état | `runs/t02/11-baseline-redeclared/project_control/project-state.v1.json` — 8–10 | `a8a790ba5a933f50f797d90202255e3b42dd14dfd76bd9e2bedc3dd8970097a8` |
| T02-F3 ancienne décision | `runs/t02/11-baseline-redeclared/docs/governance/HUMAN_DECISIONS.md` — 25, 28, 31 | `38581c198175c8b9e8f074856ab7ae55de4a68fb1ed7cd637c21f3bda8382c1a` |
| O-T06-01 restauration | `runs/t02/logs/369-10-rewritten-identical-control.log` — 6 | `64fcf0bfbeaee9637f00ff4c5853608eafc4552682cb5977980c7ae2afba41e9` |
| T02-F4 placeholders | `runs/t02/logs/592-16-confirmation-template-control.log` — 6, 12 | `b729af40bda656c09c33a2bbbd149a6b54c2687305eb7ed4dd6aa3e7c873f391` |
| T02-F4 ok/go | `runs/t02/logs/624-17-confirmation-ok-go-control.log` — 6, 12 | `19dec0b139c86316b050337b7a8618477d805fb4dca0aafe0a98eb13f49d01d0` |
| T02-F4 texte des confirmations | `runs/t02/17-confirmation-ok-go/docs/governance/HUMAN_DECISIONS.md` — 24–26 | `63f0f7e233a26784e9fa33e2b9c54d1a9dc74cce8fc157b66297481c81e09765` |
| T02-F4 identiques refusées | `runs/t02/logs/656-18-confirmation-identical-control.log` — 6, 12 | `dda79f7a5c012cee397ea3e5ae407ce57911e712c29021c982047d68db82921e` |
| T02-F4 absente refusée | `runs/t02/logs/681-19-confirmation-missing-control.log` — 6, 12 | `5121f25a7d5a1d12d10e06137d86402c5a4a732b111cc6f6988c6ddc2357ccd1` |
| F-T01-01 test réussi/refus | `runs/t01/actual-pass-v2-commands.txt` — 7–17, 38–46 | `5daa6ddac084361d2169ef01978135f5d552015606d5643617d134b970b45046` |
| F-T01-01 sortie réelle | `runs/t01/cases/actual_pass_expected_error_v2/reports/evidence/WI-001/actual-output.txt` — 3, 7, 9 | `2272dbeef5dd16f1b8229e1bd3789e0c5d8aa7a63a82fd7ed8b64421ddc168bb` |
| L-T01-02 pièce neutre | `runs/t01/logs/0156-failed_plus_marker_only-python3.14.txt` — 12 | `a3ecd17c2b2a587690ef8f07dcae453c6e49a712fc9b7f168b526609beed3ffd` |
| L-T01-03 UTF-8 invalide | `runs/t01/logs/0096-failure_invalid_utf8-python3.14.txt` — 12 | `a28293211b6503afb20393d14773480a2ce5eb42a4632ecc80ce56715714e355` |
| Matrice T01 | `runs/t01/results.json` — 1 et scénarios | `b1fd840dab816f4bcaf50c7cbe53a5108f50f22e4e65cd44a3ed1baf09acd851` |
| Matrice T02 | `runs/t02/results.json` — 1 et scénarios | `864b362f663d94b42fc7793ac08fb589291ca2bc792b4bae7f50aab02c392725` |
| Empreintes T02 | `runs/t02/sha256.tsv` — 1 et fichiers | `1b8b762fbcb143d1697e871bc969c46f30a10e2dddab9c0ec79658e6e4efb626` |
| Core copies T01 | `runs/t01/core-integrity.tsv` — 1 et fichiers | `6dd45d426703b96d1848d8144e79303251459b21466132c89474460b7ad45c66` |
| Contrôleur copies T02 | `runs/t02/code-integrity.tsv` — 1 et fichiers | `37141d7a8fb97021068868f96c5b719ebfe63aacfefd2e150937b4ca8ac1ea29` |

## État final du dossier

`source/` conserve exactement les **116 chemins, tailles et empreintes de contenu** de l’inventaire initial ; la comparaison est refaite après fin de suite, avant écriture du livrable. Aucun correctif, ajout ou retrait de fichier source. Empreinte d’arbre (lignes triées `chemin<TAB>taille<TAB>SHA-256<LF>`) : `6a3045d6d2d793e3ab7648506f05fa14f0fa034147e02d81409b795fe5a103b1`.

Les campagnes restent inspectables dans `runs/` :

- `control/` : inventaires avant/après, lanceur, journal de suite, copie de suite, brouillon d’assemblage et vérification finale ;
- `t01/` : baseline, 21 cas de preuves, journaux, matrices et inventaires ; certains chantiers sont volontairement restés IN_PROGRESS après refus ;
- `t02/` : 27 copies de contrôleur, dont les états historiques incohérents ou refusés volontairement conservés, recettes et journaux ;
- `t03/` : parcours et contre-épreuves ; le projet final est propre sur `main`, premier chantier DONE ;
- `t04/` : preuve d’entrée historique absente et comparaison limitée de même version ;
- aucun dossier d’essai T-05 indépendant n’a été créé par l’agent bloqué.

Volume des fichiers de `runs/` au relevé avant création du rapport : 115 583 236 octets, y compris les objets Git des copies. Répartition : `control/` 306 fichiers, `t01/` 8253 fichiers, `t02/` 10384 fichiers, `t03/` 383 fichiers, `t04/` 1 fichiers. Les temporaires de la suite sont nettoyés par la suite elle-même ; les preuves et copies nommées n’ont pas été nettoyées. Aucun processus de test lancé par ce contrôle ne reste en cours.

Le seul livrable final créé à la racine est `CONTROLE_SQUELETTE_3.15.2.md`. Les fichiers de `runs/` sont les matériaux reproductibles du contrôle. Ce verdict est fondé sur les refus manquants reproduits, avec les limites de couverture ci-dessus ; il ne prétend pas qualifier une montée 3.6.1 ni les hypothèses T-05 non exécutées.

## Verdict

SQUELETTE_3.15.2_REQUIRES_MAJOR_REDLINE
