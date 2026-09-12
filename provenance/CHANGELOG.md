# Changelog du template

Journal des versions du squelette lui-même. Il complète `TEMPLATE_PROVENANCE.md`
(origine de la baseline) et ne concerne aucun projet dérivé : un projet créé à
partir de l'arbre suivi hérite de ce journal comme trace de l'ascendance de son
template, sans en faire un record de projet.

Règles : une entrée par maintenance du core ; mandat humain, branche dédiée,
baseline, contrôles exécutés et rapport détaillé sous `provenance/maintenance/`.
Depuis la 3.9.0, une maintenance qui change ce que le contrôleur affiche, le nombre
de fichiers suivis ou la version régénère aussi la démo (`python3 -B
examples/hello-squelette/demo.py --write`) avant de committer : le test de la suite
la rejoue et refuse tout écart entre le README et la sortie réelle.
Aucune entrée n'implique une promotion de la branche canonique : la promotion est
une décision humaine enregistrée séparément. Append-only.

## Décisions du Project Owner — 2026-09-06

Décisions prises et enregistrées ici parce que `docs/governance/HUMAN_DECISIONS.md`
reste vierge dans le template : il appartient aux projets dérivés, pas au template.

- `TPL-D-001` — **Doctrine ratifiée.** La règle introduite par la maintenance
  `codex/v3-fiabilite-simplicite` dans `AGENTS.md` (« Reprise et charge
  administrative » : une autorisation humaine déjà donnée couvre les étapes
  ordinaires dans son périmètre ; une nouvelle décision n'est demandée que pour
  un nouveau périmètre, un risque ou un enjeu d'autorité) est ratifiée telle
  quelle. Elle s'applique à tout projet dérivé de cette baseline.
- `TPL-D-002` — **Promotion.** `claude/v3-redlines` est promue branche canonique
  par fast-forward de `main` ; la baseline antérieure `35da2a2` reçoit le tag
  `v3.0.0`, la baseline promue le tag `v3.1.0`. Les branches `codex/*` et
  `claude/v3-redlines` sont entièrement contenues dans `main`.
- `TPL-D-003` — **Baseline unique.** Ce dépôt est la seule baseline du squelette
  (`ONE_CANONICAL_BASELINE` appliqué au template lui-même). Les copies
  `squelette-projet-gouverne` et `squelette-decision-projet` sont archivées :
  marqueur `ARCHIVED.md` et tag `archived-2026-09-06` dans chacune, aucune
  évolution ne leur est plus apportée. Toute nouvelle copie part de `main` de ce
  dépôt.
- `TPL-D-004` — **Remote canonique.** Le dépôt est sauvegardé sur GitHub, dépôt
  privé `JyMinet/squelette` (`origin` = `https://github.com/JyMinet/squelette.git`).
  `main` et les tags y sont poussés depuis le poste du Project Owner ; aucun agent
  ne pousse. Le NAS reste disponible comme second remote, sans rôle canonique.

## Décisions du Project Owner — 2026-09-07

- `TPL-D-005` — **Records sur la branche canonique.** Option A de la scope definition
  P9 retenue (« P9- A ») avec le modèle « Project Control commite lui-même » : les
  records administratifs ne vivent que sur la branche canonique ; `create-work-item`,
  `start`, `block`, `resume` et `close` s'exécutent depuis son checkout et committent
  eux-mêmes leurs records ; la branche d'un Work Item ne porte jamais de changement
  administratif. La procédure de preflight Normal Mode d'`AGENTS.md` change en
  conséquence. S'applique à tout projet dérivé de cette baseline.
- `TPL-D-006` — **Promotion.** `claude/v3.2-git-safety` puis
  `claude/v3.2-records-canonical` sont promues branche canonique par fast-forward de
  `main` ; la baseline promue reçoit le tag `v3.2.0`. Mandat « ok je te suis ! »
  (2026-09-07), sur la proposition de promouvoir avant d'ouvrir P2. Le push vers
  `origin` reste le geste du Project Owner (`TPL-D-004`).

## Décisions du Project Owner — 2026-09-07 (suite)

- `TPL-D-007` — **Ensemble core du template.** Pour le manifeste du core et
  `template-upgrade` (P2, étape 1b), le core versionné est : `CLAUDE.md`,
  `FIRST_START.md`, `ADOPTION.md`, `scripts/` (contrôleur, traçabilité Git, hook),
  `tests/test_template.py` et `tests/fixtures/project_control/`,
  `project_control/schemas/` et `project_control/README.md`,
  `docs/governance/DEFINITION_OF_DONE.md`, et `docs/agent-governance/AGENTS.core.md`
  (nouveau, extrait d'`AGENTS.md`). Hors core : `AGENTS.md` (au projet, inclut le
  core et ne peut que le renforcer), `README.md`, les documents de gouvernance
  remplis par le projet, les records, le métier, `runtime_proof/`, `provenance/`.
  Décision « Liste proposée » (2026-09-07).
- `TPL-D-008` — **Promotion.** `claude/v3.3-legacy-baseline` est promue branche
  canonique par fast-forward de `main` ; la baseline promue reçoit le tag `v3.3.0`.
  Décision « Oui, v3.3.0 maintenant » (2026-09-07). Push `origin` et `nas` par le
  Project Owner.

## Décisions du Project Owner — 2026-09-07 (suite 4)

- `TPL-D-011` — **Dossier accordé, double arrêt.** « Si la consigne donnée fait sortir
  du dossier accordé, il doit y avoir deux stop pour confirmation minimum. » Toute
  consigne, plan ou mandat dont l'exécution sortirait du dépôt courant (écriture,
  branche, commit, scripts, push dans un autre dossier) exige `STOP 1` (nommer le
  dossier cible, l'action, l'alternative dans le périmètre) puis `STOP 2` (reformuler le
  périmètre exact et obtenir une seconde confirmation explicite qui nomme le dossier) ;
  un accord général ne vaut pas. Par défaut, l'original d'un projet réel ne sert jamais
  de terrain d'essai : une copie dont l'original n'est pas impacté est la voie normale.
  Décision prise après la dérive du 2026-09-07 (l'étape 2 de P2 conduite dans l'original
  de `alpha` au lieu d'une copie, sur un choix jamais posé au Project
  Owner ; annulée, original restauré). S'applique à tout projet dérivé.

## Décisions du Project Owner — 2026-09-07 (suite 6)

- `TPL-D-013` — **Preuve de lecture des autorités (P3).** Mandat « alors p3 ? »
  (2026-09-07), P3 conduite dans le template lui-même, sans second projet. Deux
  options tranchées par le Project Owner : mécanisme « empreinte présentée par
  l'agent » — `start` et `resume` exigent `--authorities-digest`, égal à l'empreinte
  courante des autorités du Work Item, que le contrôleur n'affiche jamais ; périmètre
  « autorités routées seulement » — documents de base de
  `mandatory-documents.v1.json` plus les scopes déduits des `authorized_paths`, les
  records tenus par Project Control exclus, `HUMAN_DECISIONS.md` inclus. Un Agent Run
  antérieur à la baseline d'adoption est exempt. S'applique à tout projet dérivé.

## Décisions du Project Owner — 2026-09-07 (suite 5)

- `TPL-D-012` — **Promotion.** `claude/v3.5-double-stop` est promue branche canonique
  par fast-forward de `main` ; la baseline promue reçoit le tag `v3.5.0`
  (`skeleton_version` `3.5.0`, première version portant `TPL-D-011`). Décision
  « promouvoir » (2026-09-07). Push `origin` et `nas` par le Project Owner.

## Décisions du Project Owner — 2026-09-07 (suite 7)

- `TPL-D-014` — **Promotion.** `claude/v3.6-proof-of-reading` est promue branche
  canonique par fast-forward de `main` ; la baseline promue reçoit le tag `v3.6.0`
  (`skeleton_version` `3.6.0`, première version portant la preuve de lecture des
  autorités, `TPL-D-013`). Décision « promouvoir » (2026-09-07). La règle apparue
  pendant l'implémentation — une autorité comprise dans les `authorized_paths` du
  Work Item ne périme pas sa propre preuve — est promue avec elle. Push `origin` et
  `nas` par le Project Owner.

## Décisions du Project Owner — 2026-09-07 (suite 8)

- `TPL-D-015` — **Promotion.** `claude/v3.6.1-authorities-baseline` est promue branche
  canonique par fast-forward de `main` ; la baseline promue reçoit le tag `v3.6.1`
  (`skeleton_version` `3.6.1`, première version adoptable par un projet dérivé ayant des
  Agent Runs entre sa baseline d'adoption et la preuve de lecture : `authorities_baseline`,
  correctif de `RL-T-01`). Décision « promouvoir » (2026-09-07), après le double arrêt du
  portage (« Confirmé : branche claude/v3.6.1-authorities-baseline dans
  ~/Projets/Squelette V3 -runtime-proof, main intouché, pas de push. ») et le
  feu vert sur le droit de suppression limité aux verrous Git. La 3.6.0 reste taguée comme
  sauvegarde ; aucun projet avec historique ne doit l'adopter. Push `origin` et `nas` par
  le Project Owner.

## Décisions du Project Owner — 2026-09-07 (suite 9)

- `TPL-D-016` — **Promotion.** `claude/v3.7-reporting-style` est promue branche
  canonique par fast-forward de `main` ; la baseline promue reçoit le tag `v3.7.0`
  (`skeleton_version` `3.7.0`, première version où le Project Owner choisit à
  l'initialisation la forme des retours qui lui sont faits — `reporting_style`
  `TECHNICAL` ou `PLAIN`, P11 — et où `Folder scope` se renseigne aussi dans le dépôt
  cible après un double arrêt, O-10). Décision « simple etpromouvoir » (2026-09-07),
  après le double arrêt du portage (« Confirmé : branche claude/v3.7-reporting-style
  dans ~/Projets/Squelette V3 -runtime-proof, main intouché, pas de
  push. »). Le mot « simple » de la même décision est le choix du Project Owner pour
  son projet dérivé (`reporting_style` `PLAIN`), à enregistrer dans ce projet-là sous
  sa propre décision humaine lors de sa mise à niveau ; il ne change rien au template,
  dont l'état livré reste `UNKNOWN` jusqu'à l'interview de chaque nouveau projet.
  Push `origin` et `nas` par le Project Owner.

## Décisions du Project Owner — 2026-09-08

- `TPL-D-017` — **La ROADMAP dans le dossier (P12, étape 2 ; P6).** Sur la proposition
  « toutes les infos dans le dossier physique du projet, format JSON ? » (Project Owner,
  2026-09-08), cadrée dans `provenance/maintenance/scopes/p12-scope-roadmap-dediee.md`
  § 12, les sept recommandations sont retenues telles quelles (« je suis ok avec la
  suite. On va de l'avant », 2026-09-08) : (1) les idées du Project Owner vivent dans un
  fichier léger en deux formes synchronisées (`docs/governance/ideas-state.v1.json` +
  `IDEAS.md`), pas en Work Items `PROPOSED` ; (2) la page HTML générée est ignorée par
  Git, les données et la vue Markdown sont committées ; (3) la roadmap du squelette
  lui-même vit sous `provenance/` ; (4) les fiches de cadrage et de revue sont
  rapatriées dans `provenance/maintenance/scopes/` dans la même version ; (5) nouvelle
  commande `roadmap-view`, distincte de `status` ; (6) la page Claude et la tâche
  quotidienne restent un miroir de la vue générée ; (7) version `3.8.0`. La ligne
  « pas obligé d'avoir un dépôt » de l'étape 1 est retirée à sa demande (« cette info
  est has been »). Le core s'étend à `docs/agent-governance/ROADMAP_VIEW.md`
  (complément à `TPL-D-007`). Ordre décidé le même jour : 3.8.0, puis challenge du
  squelette par Codex (« quand squelette est terminé, on va faire un challenge à
  Codex »), puis la mise à niveau d'Alpha en dernier (« on terminera par la
  mise à jour Alpha »). La promotion de la 3.8.0 reste une décision séparée.

## Décisions du Project Owner — 2026-09-08 (suite)

- `TPL-D-018` — **Promotion.** `claude/v3.8-roadmap-in-repo` est promue branche
  canonique par fast-forward de `main` ; la baseline promue reçoit le tag `v3.8.0`
  (`skeleton_version` `3.8.0`, première version où la ROADMAP vit dans le dossier :
  idées du Project Owner en deux formes synchronisées, vue générée par `roadmap-view`,
  roadmap du squelette sous `provenance/`, fiches de cadrage rapatriées —
  `TPL-D-017`, P12 étape 2 et P6). Décision « promouvoir » (2026-09-08), après le
  double arrêt du portage (« je suis d'accord pour que tu écrives dans ce dossier »
  puis « Confirmé : branche claude/v3.8-roadmap-in-repo dans
  ~/Projets/Squelette V3 -runtime-proof, main intouché, pas de push. »)
  et le droit de suppression limité aux fichiers temporaires de Git. Livraison en
  trois commits (`b97703a` version, `d5c3e5b` correctif de la vue constaté dans le
  dépôt réel, `2487619` vue générée), 97 tests OK sur le poste du Project Owner.
  Le tag est posé sur le commit qui enregistre cette décision ; la vue
  `provenance/ROADMAP_VIEW.md` est régénérée ensuite et committée à part, sans
  changement du core : `main` est un commit devant `v3.8.0`. Push `origin` et
  `nas` par le Project Owner.

## Décisions du Project Owner — 2026-09-08 (suite 2)

- `TPL-D-019` — **La vitrine GitHub (P10, étape 1).** Sur les remarques de GPT transmises
  par le Project Owner (« Améliore le github avec ces remarques de gpt […] Qu'en penses
  tu ? », 2026-09-08), cadrées dans
  `provenance/maintenance/scopes/p10-scope-publication-vitrine-github.md`, quatre
  décisions le même jour (01:25) : (1) la vitrine passe **après la 3.8.0 et avant le
  challenge du squelette par Codex** ; (2) le premier écran du README est **en anglais,
  puis le même en français, dans le même fichier**, la documentation existante inchangée
  ensuite ; (3) l'exemple est une **démo rejouable qui produit la vraie sortie du
  contrôleur, vérifiée par un test** — jamais un extrait inventé ni un dossier figé ;
  (4) **licence MIT** (aucune licence n'existait), titulaire « MINET Jeoffrey ». Le
  nouveau README est validé tel quel (« Réadme ok »). Réserves retenues face aux
  remarques de GPT : la sortie de `status` montrée est produite par la démo et non
  rédigée ; la release GitHub portera la version qui contient la vitrine, non
  `v3.0.0` ; l'annonce publique reste, comme décidé le 7 sept., pour après un second
  vrai projet (étape 2 de P10). Version `3.9.0`. La promotion reste une décision
  séparée.

## Décisions du Project Owner — 2026-09-08 (suite 3)

- `TPL-D-020` — **Promotion.** `claude/v3.9-vitrine-github` est promue branche
  canonique par fast-forward de `main` ; la baseline promue reçoit le tag `v3.9.0`
  (`skeleton_version` `3.9.0`, première version portant la vitrine GitHub : README
  problème → solution → démo → fonctionnement, en anglais puis en français ; exemple
  `hello-squelette` rejouable dont la sortie réelle alimente le README et est vérifiée
  par un test ; `CONTRIBUTING.md` ; licence MIT — `TPL-D-019`, P10 étape 1). Décision
  « promouvoir » (2026-09-08), après le double arrêt du portage (« Je suis ok » puis
  « Confirmé : branche claude/v3.9-vitrine-github dans
  ~/Projets/Squelette V3 -runtime-proof, main intouché, pas de push. »)
  et le droit de suppression limité aux fichiers temporaires de Git. Livraison en deux
  commits (`3850313` version, `23b056b` vue générée), 98 tests OK dans le dépôt ; `main`
  ayant avancé entre-temps d'un commit de provenance (`fe26c06`, sauvegardes 3.8.0
  envoyées), la branche l'a intégré par un commit de merge (`33c5169`) avant la
  promotion — aucune réécriture d'histoire. Le tag est posé sur le commit qui
  enregistre cette décision ; la vue `provenance/ROADMAP_VIEW.md` est régénérée ensuite
  et committée à part : `main` est un commit devant `v3.9.0`. Push `origin` et `nas`,
  release GitHub, About et Topics : gestes du Project Owner.

## Décisions du Project Owner — 2026-09-08 (suite 4)

- `TPL-D-021` — **Correctif de portée après la revue de robustesse (P13).** La revue
  indépendante demandée au fournisseur Codex sur le tag `v3.9.0`
  (`provenance/maintenance/2026-09-08-revue-robustesse-codex-3.9.0.md`, mandat dans
  `provenance/maintenance/scopes/`, 18 constats, verdict
  `SQUELETTE_3.9.0_REVUE_REQUIRES_MAJOR_REDLINE`) a produit deux constats `BLOCKER`
  reproduits indépendamment avant toute correction. Sur mandat « prépare la 3.9.1 »
  (2026-09-08), la version `3.9.1` corrige exactement ces deux points et la variante
  trouvée pendant la contre-vérification, sans rien traiter d'autre : (1) un renommage
  compte des deux côtés — sortir un fichier d'un emplacement exige que cet emplacement
  soit autorisé ; (2) la gate de commit applique les `authorized_paths` du Work Item
  actif à tout chemin indexé, et non aux seules racines métier ; (3) `status` n'annonce
  la gate comme active que si Git l'exécute réellement (fichier présent et exécutable),
  et `AGENTS.core.md` énonce la limite assumée : la gate ne peut pas contrôler le commit
  qui la supprime elle-même, mais sa disparition fait échouer tout contrôle suivant. Les
  dix constats `MAJOR` et les cinq `MINOR` restants sont contre-vérifiés séparément et
  feront l'objet d'une décision distincte. La promotion reste une décision séparée.

## Décisions du Project Owner — 2026-09-08 (suite 5)

- `TPL-D-022` — **Promotion.** `claude/v3.9.1-scope-renames-and-gate` est promue branche
  canonique par fast-forward de `main` ; la baseline promue reçoit le tag `v3.9.1`
  (`skeleton_version` `3.9.1`, première version où l'origine d'un renommage est classée
  comme sa destination et où la gate de commit applique les `authorized_paths` du Work
  Item actif à tout chemin indexé — `TPL-D-021`, constats `F-01`, `F-02` et `F-13` de la
  revue de robustesse, plus la limite assumée de la gate face à sa propre suppression).
  Décision « promouvoir » (2026-09-08), après le double arrêt du portage (« ok go ! »
  puis « Confirmé : branche claude/v3.9.1-scope-renames-and-gate dans
  ~/Projets/Squelette V3 -runtime-proof, main intouché, pas de push. ») et
  le droit de suppression limité aux fichiers temporaires de Git. Livraison en trois
  commits (`cf50e70` correctif, `3a50773` vue, `52dfaff` `.gitignore`), 101 tests OK sur
  le poste du Project Owner. Le même jour, sur sa demande (« on en finisse avec ce
  dossier parasite ! »), le dossier « Claude outputs » — où l'application dépose les
  fichiers téléchargés depuis une conversation — est ignoré par Git : rien n'est
  supprimé, la traçabilité cesse d'échouer sur des fichiers étrangers au projet. Le tag
  est posé sur le commit qui enregistre cette décision ; la vue est régénérée ensuite et
  committée à part : `main` est un commit devant `v3.9.1`. Push `origin` et `nas`,
  release GitHub, About et Topics : gestes du Project Owner.

## Décisions du Project Owner — 2026-09-09

- `TPL-D-023` — **Lot A des correctifs de robustesse : les autorisations (P13).** Les
  quinze constats restants de la revue de robustesse ont été contre-vérifiés un par un,
  indépendamment du rapport (`claude/contre-revue-des-15-constats.md`, huit rejoués sur
  une copie neuve, sept établis par lecture du code) : tous confirmés, aucun rejeté.
  Sur mandat « Je valide tout » (2026-09-09), les correctifs sont livrés en trois lots
  successifs, du plus proche de l'autorisation au plus lointain. Le lot A, version
  `3.10.0`, traite ce qui décide **qui a le droit d'écrire quoi** : `F-03` (une décision
  qui enregistre un refus n'autorise plus rien), `F-04` (un champ vide est une valeur
  absente, jamais la ligne suivante), `F-05` (un lien symbolique indexé puis caché dans
  l'arbre de travail reste refusé), `F-06` (autoriser un dossier parent oblige à lire les
  autorités de ses enfants), et la fermeture de la brèche de la gate assumée en `3.9.1` :
  la gate exécutable est installée **hors de l'arbre de travail** (`install-gate`), le
  fichier versionné n'en est plus que la référence, et le contrôleur vérifie leur
  identité (`COMMIT_GATE`). Les lots B (`3.11.0`, ce que le squelette affirme) et C
  (`3.12.0`, robustesse d'exécution) suivront séparément. La promotion reste une décision
  séparée.

## Décisions du Project Owner — 2026-09-09 (suite 2)

- `TPL-D-025` — **Lot B des correctifs de robustesse : ce que le squelette affirme (P13).**
  Deuxième des trois lots validés par « Je valide tout » (`TPL-D-023`), sur mandat « le lot B
  (3.11.0) ! » (2026-09-09). Les cinq constats traités ont tous la même forme : le squelette
  énonce quelque chose que personne n'a vérifié. `F-12` — la vue annonçait « toutes réussies »
  à partir du seul résultat de l'audit, sans avoir exécuté un test ; elle rapporte désormais ce
  que le contrôleur a réellement contrôlé et compte les essais sans en déclarer l'issue.
  `F-11` — la vue nomme la version promue d'après les tags du dépôt ; ces tags entrent donc dans
  son empreinte de fraîcheur, un tag posé la rend périmée. `F-17` — retirer les deux marqueurs du
  README neutralisait silencieusement le contrôle qui garantit que le README ne ment pas ; leur
  absence est maintenant une dérive. `F-18` — la vitrine promettait « un agent qui n'a pas lu ne
  peut pas démarrer » ; la portée exacte de la preuve de lecture est écrite dans la doctrine et
  dans la démo. `F-14` — en style simple, la vue n'ajoute plus d'identifiant technique de son
  cru hors du repli, et la doctrine dit ce que ce style couvre : les cellules que la vue compose,
  jamais les mots du Project Owner, qui sont montrés tels quels. Le lot C (`3.12.0`, robustesse
  d'exécution) suit séparément. La promotion reste une décision séparée.

## Décisions du Project Owner — 2026-09-09 (suite 4)

- `TPL-D-027` — **Lot C des correctifs de robustesse : la robustesse d'exécution (P13).**
  Dernier des trois lots validés par « Je valide tout » (`TPL-D-023`), sur mandat « Ensuite lot C »
  (2026-09-09). Cinq constats, tous vérifiés par un cas reproductible avant correction : `F-07`
  une interruption clavier échappait au filet des transitions, qui ne rattrapait que les erreurs
  ordinaires ; `F-08` une montée de version écrasait sans un mot un fichier du projet situé sur un
  chemin que le nouveau core revendique ; `F-09` un merge d'intégration inspecté avant commit était
  refusé alors que la doctrine promet qu'il passe ; `F-10` le gel d'un historique adopté exemptait
  par le nom, si bien qu'un enregistrement réécrit emportait son exemption ; `F-16`
  `roadmap-view --write` réécrivait la page avant de refuser en annonçant « lecture seule ».
  S'y ajoute, hors revue, la réinstallation automatique du garde-fou après `template-upgrade` :
  la copie exécutable vit hors de l'arbre, la mise à niveau ne peut donc pas l'atteindre, et un
  projet restait à une commande oubliée d'un commit non gardé. Ce lot clôt le traitement des
  dix-huit constats de la revue de robustesse. La promotion reste une décision séparée.

## Décisions du Project Owner — 2026-09-09 (suite 6)

- `TPL-D-029` — **La langue au choix (P14, étape 1).** Sur mandat « On attaque p14 » (2026-09-09) et
  après trois décisions prises le même jour : (1) **périmètre** — le choix couvre la prose adressée
  au Project Owner, `status` et la vue roadmap ; les noms de vérifications et les messages de refus
  restent en anglais, ce sont des identifiants d'un vocabulaire fermé sur lesquels s'appuient les
  essais, la gate de commit et tout outil qui lit la sortie ; (2) **emplacement** — le choix vit dans
  Project State (`language`), à côté de `reporting_style`, et la vue le suit, comme `style` suit déjà
  le style de retour ; (3) **défaut** — aucun : `UNKNOWN` tant que l'interview `FIRST_START` n'a pas
  posé la question, signalé par la vérification `LANGUAGE`, et exigé pour clore l'initialisation.
  Le squelette ne suppose pas la langue de son propriétaire. L'étape 2 — les documents de gouvernance
  en anglais — reste prévue pour plus tard ; les commits, les tags et ce journal restent en français.
  La promotion reste une décision séparée.

## Décisions du Project Owner — 2026-09-09 (suite 8)

- `TPL-D-031` — **Correctifs de la seconde revue indépendante (3.14.0).** Une seconde revue,
  confiée au fournisseur Codex sur le tag `v3.13.0` avec des angles neufs — adoption d'un dépôt non
  gouverné, première lecture, cohérence doctrine ↔ mécanique, la langue —, a rendu sept constats,
  dont deux `MAJOR`, et le verdict `SQUELETTE_3.13.0_REVUE_REQUIRES_MAJOR_REDLINE`. La contre-revue
  (`claude/contre-revue-3.13.0.md`) les confirme tous les sept, n'en rejette aucun, et en établit un
  **huitième, plus grave**, trouvé en vérifiant le premier : le garde-fou de commit annonçait
  « audit PASS on the staged state » alors qu'il lisait les fichiers du dossier de travail. Sur
  mandat « go 3.14.0 » (2026-09-09), un lot unique corrige les trois défauts sérieux — ils touchent
  la même chose, ce que le squelette accepte comme preuve — et les cinq mineurs. Quatre de ces
  mineurs étaient des régressions ou omissions introduites le jour même par les versions `3.11.0`
  et `3.13.0` : elles sont corrigées avec le reste et consignées comme telles. La promotion reste
  une décision séparée.

## Décisions du Project Owner — 2026-09-09 (suite 9)

- `TPL-D-032` — **Promotion.** `claude/v3.14-preuves` est promue branche canonique par fast-forward
  de `main` ; la baseline promue reçoit le tag `v3.14.0` (`skeleton_version` `3.14.0`, première
  version où la gate de commit juge **l'arbre que le commit va créer** et non seulement l'arbre de
  travail, où un commit cité en preuve doit appartenir au chantier qui le cite, et où la création
  des records restaure son index — `TPL-D-031`, les sept constats de la seconde revue indépendante
  et le huitième trouvé en les contre-vérifiant). Décision « Promouvoir » (2026-09-09), après le
  double arrêt du portage (« Portes ! », refusé comme trop général, puis « Confirmé : branche
  claude/v3.14-preuves dans ~/Projets/Squelette V3 -runtime-proof, main intouché, pas
  de push. »). Livraison en deux commits (`684fd3b` correctifs, `57f78b4` vue), 124 tests OK sur le
  poste du Project Owner, `audit`, `bootstrap-audit` et traçabilité PASS. Le tag est posé sur le
  commit qui enregistre cette décision ; la vue est régénérée ensuite et committée à part : `main`
  est un commit devant `v3.14.0`. Push `origin` et `nas`, releases GitHub : gestes du Project Owner.

## Décisions du Project Owner — 2026-09-09 (suite 10)

- `TPL-D-033` — **Les décisions figées gardent leur vocabulaire (3.14.1).** La répétition de la
  mise à niveau d'Alpha (`3.6.1` → `3.14.0`), jouée sur une copie jetable du projet,
  s'arrête sur un refus du contrôleur : trois décisions humaines de ce projet, enregistrées en août
  2026 et clôturées bien avant sa baseline d'adoption, portent dans `Chosen option:` le contenu de
  la décision et non le mot `AUTHORIZE`. La règle introduite par la `3.10.0` (`TPL-D-023`, constat
  `F-03`) les requalifie, l'audit échoue et plus aucun commit n'est possible. Or la doctrine promet,
  dans `AGENTS.core.md` comme dans `project_control/README.md`, que les clôtures figées à la
  baseline d'adoption ne sont « jamais reconstruites ni requalifiées » : le contrôleur contredit ici
  sa propre promesse, et le défaut est du squelette, pas du projet. Trois routes ont été présentées
  au Project Owner — corriger le squelette, amender les trois décisions du projet, ou rester en
  `3.6.1`. Décision : « A » (2026-09-09), corriger le squelette ; « Dans le meme mouvement ! » pour
  les quatre essais de la suite qui ne peuvent pas tourner dans un projet dérivé ; numéro retenu
  « 3.14.1 », une correction. La promotion reste une décision séparée.

## Décisions du Project Owner — 2026-09-10 (suite)

- `TPL-D-040` — **Promotion.** `claude/v3.15.2-essai-garde` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.15.2` (`skeleton_version` `3.15.2`,
  première version où la suite du template est verte à la fois dans le template et dans un projet
  dérivé réel — `TPL-D-039`). Décision « Promeus » (2026-09-10). Livraison en deux commits
  (`6307fe7` correctif, `f0a137e` vue), 133 tests OK dans le template et 133 OK (9 ignorés) sur la
  copie d'Alpha montée en `3.15.2`, `audit`, `bootstrap-audit`, traçabilité et
  `demo.py --check` PASS. Le tag est posé sur le commit qui enregistre cette décision ; la vue est
  régénérée ensuite et committée à part : `main` est un commit devant `v3.15.2`. Push `origin` et
  `nas`, release GitHub : gestes du Project Owner.

## Décisions du Project Owner — 2026-09-10

- `TPL-D-039` — **Un essai du template qui échouait dans un projet dérivé (3.15.2).** La répétition
  de la montée d'Alpha, rejouée dans le bon ordre, passe de bout en bout : registres
  déposés d'abord sur la canonique, core appliqué sur la branche de chantier, intégration en
  fast-forward, `audit` `PASS`, `status` complet. La suite du template tourne sur ce projet en
  114 secondes — 133 essais, 8 ignorés — et il en reste **un** rouge :
  `test_an_idea_is_not_a_work_item_and_an_inherited_view_is_not_stale`, ajouté par la `3.15.0`.
  Il attend qu'une copie annonce une vue « périmée » ; un projet dérivé n'a pas encore de vue du
  tout, et l'essai déclare un échec là où il n'y a rien à vérifier. C'est la famille de constats
  que la `3.14.1` avait fermée pour quatre essais, rouverte par inadvertance le soir même. Options
  présentées au Project Owner : corriger, ou écrire dans la condition de clôture d'Alpha « 132
  verts, 1 rouge qui ne nous concerne pas ». Décision : « ok A pour le squelette » (2026-09-10) —
  corriger, parce qu'un contrôle rouge qu'on explique dans un coin est exactement la porte que le
  squelette passe son temps à fermer. Le projet dérivé n'a rien à corriger de son côté : il reçoit
  l'essai réparé avec le core. La promotion reste une décision séparée.

## Décisions du Project Owner — 2026-09-10 (suite 2)

- `TPL-D-041` — **Les trois lignes rouges du contrôle indépendant de la 3.15.2.** Un contrôle
  indépendant (Codex, dossier isolé `squelette-controle-3.15.2`, copie de la `3.15.2` sans
  historique) rend le verdict `SQUELETTE_3.15.2_REQUIRES_MAJOR_REDLINE` et démontre trois défauts,
  contre-exemples exécutés à l'appui. Deux sont majeurs et viennent tous les deux du squelette,
  pas d'un projet : (1) `F-T03-01` — les notices de format ajoutées sous les lignes `Status:` par
  la `3.15.0` étaient elles-mêmes lues comme la valeur du statut, si bien qu'un document resté
  brouillon passait la validation initiale ; (2) `T-02` — la clôture ne relisait jamais son propre
  mandat, de sorte qu'un Work Item ouvert à la baseline d'adoption pouvait se clore sur une
  décision devenue un refus, parce que l'exemption des décisions figées le couvrait encore. Le
  troisième est mineur : (3) `F-T01-01` — un essai qui réussit en imprimant une erreur attendue
  (`ERROR: …` dans une ligne de journal) était compté comme une pièce en échec et sa preuve
  refusée. Décision : « je veux la 3.15.3 » (2026-09-10) — corriger les trois dans le squelette,
  un essai par correction, rouge sur la `3.15.2` et vert sur la `3.15.3`. La promotion reste une
  décision séparée. `T-04` (montée `3.6.1` → `3.15.2`) n'a pas pu être vérifié par ce contrôle :
  le mandat fournissait une archive de tag, donc sans historique — le défaut est du mandat, à
  reprendre dans un second passage.

## Décisions du Project Owner — 2026-09-10 (suite 4)

- `TPL-D-043` — **Deux des cinq constats de la seconde passe de contrôle (3.16.0).** La seconde passe
  du contrôle indépendant a fait ce que la première n'avait pas pu faire : un vrai projet construit
  sur la `3.6.1`, quatre chantiers menés jusqu'à `DONE`, puis monté vers la `3.15.3`. Verdict
  `SQUELETTE_3.15.3_REQUIRES_MAJOR_REDLINE`, cinq constats. Ce que le contrôle valide au passage :
  les trois corrections de la `3.15.3` tiennent, les 136 essais passent, et les 19 fichiers des
  clôtures figées traversent la montée à l'octet près — ajouter un seul saut de ligne à l'un d'eux
  fait refuser l'audit. Trois constats visent le garde-fou de commit (`F-T05-01` installation
  annoncée au mauvais endroit dans un worktree lié, `F-T05-03` passager de fusion masqué,
  `F-T05-02` instantané indisponible qui autorise au lieu de refuser) ; ils préexistent à la
  `3.15.3` et demandent leur propre cadrage. Les deux autres touchent ce qui sert tous les jours,
  et ce sont eux que cette version corrige. Options présentées au Project Owner : tout traiter
  d'un coup, traiter d'abord ces deux-là, ou ne traiter que la régression. Décision : « Allons sur
  B » (2026-09-10) — les deux, le garde-fou dans une version suivante avec son propre cadrage,
  parce qu'un correctif rapide sur la pièce la plus délicate du produit est une mauvaise idée.
  La promotion reste une décision séparée.

## Décisions du Project Owner — 2026-09-11

- `TPL-D-052` — **Promotion.** `claude/v3.17-histoire-et-concurrence` est promue branche canonique
  par fast-forward de `main` ; la baseline promue reçoit le tag `v3.17.0` (`skeleton_version`
  `3.17.0`, première version où deux sessions ne peuvent plus se perdre l'une l'autre et où un
  projet ne peut plus naître amputé de son `.gitignore` — `TPL-D-051`). Décision « Promeus ! »
  (2026-09-11). Livraison en deux commits (`381ce7b` correctif, `af304af` vue), 144 essais OK dans
  le template et 144 OK (9 ignorés) sur une copie d'Alpha montée en `3.17.0`, `audit`,
  `bootstrap-audit`, traçabilité et `demo.py --check` PASS. Trois essais neufs, tous rouges sur la
  `3.16.2`, dont un qui lance réellement deux processus en parallèle. Le tag est posé sur le commit
  qui enregistre cette décision ; la vue est régénérée ensuite et committée à part : `main` est un
  commit devant `v3.17.0`. Envoi vers `origin` et `nas` et release GitHub : gestes du Project Owner
  (`TPL-D-004`).
- `TPL-D-053` — **Les baselines déjà déclarées seront confirmées, pas acceptées telles quelles.**
  Première des quatre questions de la fiche de cadrage `P17` : le jour où une déclaration de baseline
  devra nommer le commit qu'elle fige, que fait-on des déclarations existantes, qui ne le nomment
  pas ? Deux routes — les accepter et n'exiger le champ que des futures, ou demander une décision de
  confirmation. Décision : « On confirme ! » (2026-09-11). Alpha est le seul projet à
  avoir une vraie histoire figée à protéger, et c'est pour lui que la promesse existe : ses deux
  baselines (`legacy_baseline`, autorité `HD-065` ; `authorities_baseline`, autorité `HD-066`)
  recevront chacune une décision qui nomme leur commit exact, dans le même mouvement que le
  chantier. Les trois autres questions de la fiche restent ouvertes.
- `TPL-D-054` — **Un essai livré par la 3.17.0 ne mesure pas ce qu'il annonce ; il est corrigé en
  3.17.1.** La montée d'Alpha vers la `3.17.0` (`WI-064`) a trouvé
  `test_a_project_without_its_gitignore_is_refused_before_it_breaks` rouge, dans ce dépôt comme dans
  le squelette : l'essai retire `.gitignore` d'une copie du projet, mais la copie emporte aussi ce que
  ce fichier masquait — le dossier où l'application dépose ses fichiers, la vue générée — et le
  contrôleur refuse ces fichiers-là pour une raison étrangère à ce que l'essai mesure. Il passait
  quand ce dossier était presque vide ; son résultat dépendait de ce qui traînait à côté. Écrit et
  promu par l'agent exécutant. Une preuve de tests `PASS` aurait été fausse, une exception écrite dans
  la condition de clôture aurait été un contrôle rouge expliqué dans un coin : `WI-064` a été
  **bloqué** (`HD-072`, `TEMPLATE_TEST_DEFECT_UPSTREAM`) avec pour condition de reprise une version
  du squelette où cet essai vérifie ce qu'il annonce sans dépendre des fichiers ignorés présents dans
  la copie. Double arrêt : `STOP 1` (dossier, action, alternative : ne rien corriger, `WI-064` bloqué
  indéfiniment, chaque projet adoptant la `3.17.0` héritant d'un essai capricieux) → « Confirmé :
  correction de l'essai et 3.17.1 dans ~/Projets/Squelette V3 -runtime-proof, pas de
  push. » ; `STOP 2` (périmètre exact : branche, sept fichiers, déroulé) → « Confirmé : branche
  claude/v3.17.1-essai-gitignore-deterministe dans ~/Projets/Squelette V3
  -runtime-proof, pas de push. » (2026-09-11). Dette notée, non traitée : **toutes** les copies
  d'essai emportent les fichiers ignorés du dossier de travail, et `stage_explicit_files` le
  contourne déjà à demi-mot ; aucun autre essai n'a démontré d'échec à cause de cela — sans scénario
  d'échec démontré, pas de redline. La promotion reste une décision séparée.
- `TPL-D-055` — **Promotion.** `claude/v3.17.1-essai-gitignore-deterministe` est promue branche
  canonique par fast-forward de `main` ; la baseline promue reçoit le tag `v3.17.1`
  (`skeleton_version` `3.17.1`, version où l'essai du `.gitignore` manquant ne dépend plus de ce qui
  traîne à côté du squelette — `TPL-D-054`). Mandat de promotion : la double confirmation du
  2026-09-11 (« correction de l'essai et 3.17.1 … pas de push »), qui couvrait promotion et tag.
  Livraison en deux commits (`a9e91ae` correctif, `a7463aa` vue), 144 essais OK dans le template,
  `audit`, `bootstrap-audit` et `demo.py --check` PASS. Le tag est posé sur le commit qui enregistre
  cette décision ; la vue est régénérée ensuite et committée à part : `main` est un commit devant
  `v3.17.1`. Envoi vers `origin` et `nas` et release GitHub : gestes du Project Owner
  (`TPL-D-004`). Alpha reprend `WI-064` sur cette version, par la voie normale.
- `TPL-D-056` — **P17 cadré : la ligne du passé ne bouge que sur décision.** Les trois questions
  restantes de la fiche, proposées ensemble et acceptées d'un mot — « je suis d'accord »
  (2026-09-11). (2) La mémoire d'un travail figé ne vit nulle part de neuf : **dans Git, au commit
  de la baseline**, où le contrôleur relisait déjà les records figés ; l'historique n'est pas ce
  qu'un chantier peut effacer, ce qui manquait c'est que la ligne ne bouge pas en silence. (3) Le
  fichier d'état **reste ouvert** aux chantiers ordinaires, mais ses deux lignes de baseline ne se
  retirent, ne se déplacent et ne se redéclarent que sur une décision qui nomme le commit visé ou
  qui dit qu'on retire la ligne — pistes 1 et 2 de la fiche en une règle, plus la piste 3 ; la
  piste 4 en découle. (4) **Une quatrième passe de contrôle** juste après ce chantier, sur une
  version taguée. Mandat de livraison : double arrêt — `STOP 1` (dossier, action, les quatre
  règles, alternative : livrer seulement les pistes 2 et 3, qui rendent le scénario plus difficile
  sans le rendre impossible) → « ok » ; `STOP 2` (branche, fichiers, déroulé) → « Confirmé : branche
  claude/v3.18-baseline-ancree dans ~/Projets/Squelette V3 -runtime-proof, pas de
  push. » La fiche entre dans le dépôt avec les quatre réponses
  (`provenance/maintenance/scopes/p17-scope-baseline-defigeable.md`). La promotion reste une
  décision séparée.
- `TPL-D-057` — **Livraison de la 3.18.0.** Quatre règles, six essais rouges sur la `3.17.1` :
  la décision d'une baseline nomme son commit (`Legacy baseline commit:` /
  `Authorities baseline commit:`, refus de l'audit sinon) ; retirer une baseline exige une
  décision du chantier en cours qui la nomme (`… baseline removed:`, garde-fou
  `BASELINE_CHANGE_MANDATED`) ; une baseline ne recule jamais ; et toute montée est **répétée
  avant d'être écrite** — `HEAD` extrait dans un worktree jetable, le core prévu écrit et committé,
  l'audit du nouveau contrôleur lancé dessus (`UPGRADE_REHEARSAL`), `--apply` refusé tant qu'il
  refuse. Cette dernière règle est générique : elle aurait arrêté la montée à l'aveugle vers la
  `3.8.0` comme elle arrêtera une montée vers la `3.18.0` d'un projet dont les baselines ne sont pas
  confirmées, alors que le contrôleur qui monte le projet ignore la règle nouvelle. Pour
  Alpha, l'ordre est écrit : deux décisions de confirmation, un chantier qui les fait
  citer, puis la montée. Commits passés sous le mandat `TPL-D-056`. La promotion reste une décision
  séparée.
- `TPL-D-058` — **Promotion.** `claude/v3.18-baseline-ancree` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.18.0` (`skeleton_version`
  `3.18.0`, première version où la ligne du passé ne bouge que sur décision et où une montée se
  répète avant de s'écrire — `TPL-D-056`, `TPL-D-057`). Mandat de promotion : la double
  confirmation du 2026-09-11 (« Confirmé : branche claude/v3.18-baseline-ancree … pas de
  push. »), qui couvrait promotion et tag. Livraison en deux commits (`10c9e30` chantier,
  `a38631a` vue), 149 essais OK dans le template, `audit`, `bootstrap-audit` et `demo.py --check`
  PASS. Le tag est posé sur le commit qui enregistre cette décision ; la vue est régénérée ensuite
  et committée à part : `main` est un commit devant `v3.18.0`. Envoi vers `origin` et `nas` et
  release GitHub : gestes du Project Owner (`TPL-D-004`). Alpha : confirmer ses deux
  baselines, puis monter — sous double arrêt.
- `TPL-D-059` — **Quatre anomalies de la quatrième passe de contrôle, et la dette démontrée
  (3.18.1).** La quatrième passe, sur la `3.18.0`, a rendu `SQUELETTE_3.18.0_REQUIRES_MAJOR_REDLINE` :
  quatre anomalies reproduites avec de vrais commits, aucun faux positif — et les onze corrections
  précédentes qui tiennent toutes. La majeure est de l'agent exécutant : la règle du retrait de
  baseline ne courait que sur la branche de chantier, « hors fusion », et la vérification des
  fusions d'intégration ne regardait que les noms des fichiers apportés ; le résultat d'une fusion
  édité avant son commit pouvait retirer la baseline sur le chemin, et une clôture figée être
  réécrite ensuite, audit au vert. Trois modérées : une montée où seul le garde-fou change refusée
  à tort par la répétition ; une répétition relancée après une montée écrite mais non committée qui
  répétait avec l'ancien contrôleur ; un Ctrl-C laissant un fichier temporaire qui bloquait la
  suite. Plus la dette notée en `3.17.1` et démontrée par la passe : un fichier ignoré à côté du
  squelette faisait échouer deux essais. Décision : « ok » sur le `STOP 1` (tout corriger d'un
  coup, y compris l'observation non bloquante — une décision `REJECT` déclarait une baseline —
  plutôt que la majeure seule), puis « Confirmé : branche claude/v3.18.1-fusion-et-repetition
  dans ~/Projets/Squelette V3 -runtime-proof, pas de push. » (2026-09-11). Le rapport
  est rapatrié. La promotion reste une décision séparée.
- `TPL-D-060` — **Promotion.** `claude/v3.18.1-fusion-et-repetition` est promue branche canonique
  par fast-forward de `main` ; la baseline promue reçoit le tag `v3.18.1` (`skeleton_version`
  `3.18.1`, version où une fusion d'intégration n'emporte que ce que sa branche a produit et où la
  répétition de montée est mesurée contre `HEAD` — `TPL-D-059`). Mandat de promotion : la double
  confirmation du 2026-09-11, qui couvrait promotion et tag. Livraison en deux commits (`2fa1917`
  correctifs, `467d2ac` vue), 156 essais OK dans le template, `audit`, `bootstrap-audit` et
  `demo.py --check` PASS. Le tag est posé sur le commit qui enregistre cette décision ; la vue est
  régénérée ensuite et committée à part : `main` est un commit devant `v3.18.1`. Envoi vers
  `origin` et `nas` et release GitHub : gestes du Project Owner (`TPL-D-004`). Alpha :
  montée de routine vers la 3.18.1, sous double arrêt.
- `TPL-D-061` — **Les deux dettes sont soldées (3.18.2).** « ok » sur le `STOP 1` (les deux dettes
  d'un coup plutôt que rien), puis « Confirmé : branche claude/v3.18.2-copies-perimees dans
  ~/Projets/Squelette V3 -runtime-proof, pas de push. » (2026-09-11). Le garde-fou
  et la répétition de montée retirent au démarrage les checkouts jetables que le contrôleur a
  lui-même créés et qu'une commande tuée a laissés derrière elle — deux d'entre eux ont été trouvés
  dans Alpha, laissés par une clôture coupée par la limite de temps de l'outil, et
  retirés à la main sur « ok, nettoie » ; jamais un autre worktree. Le tableau de bord du squelette
  dit la vérité du jour au lieu de raconter Alpha en 3.6.1. Une retouche de message en passant. La
  promotion reste une décision séparée.
- `TPL-D-062` — **Promotion.** `claude/v3.18.2-copies-perimees` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.18.2` (`skeleton_version`
  `3.18.2`, version où le contrôleur range ses propres copies jetables — `TPL-D-061`). Mandat de
  promotion : la double confirmation du 2026-09-11, qui couvrait promotion et tag. Livraison en
  deux commits (`99ca249` dettes, `22c7016` vue), 157 essais OK dans le template, `audit`,
  `bootstrap-audit` et `demo.py --check` PASS. Le tag est posé sur le commit qui enregistre cette
  décision ; la vue est régénérée ensuite et committée à part : `main` est un commit devant
  `v3.18.2`. Envoi vers `origin` et `nas` et release GitHub : gestes du Project Owner
  (`TPL-D-004`). Ensuite : la cinquième passe de contrôle, sur cette version.
- `TPL-D-063` — **P18 : le squelette sait se publier (3.19.0).** « On pourrait ouvrir le git au
  public ? » puis, sur la proposition d'un dépôt public neuf nettoyé de tout ce qui touche au projet
  adopté et aux chemins portant son identifiant : « ok go » (2026-09-11). Choix arrêtés dans la
  discussion : le dépôt public est un **miroir produit par un script** depuis le dépôt privé, jamais
  édité à la main (un nettoyage manuel créerait un second squelette qui diverge) ; l'adresse
  e-mail sort, les chemins de la machine deviennent `~/…`, le projet adopté devient « Alpha », le
  dépôt de sauvegarde `SAUVEGARDE` ; **le prénom reste** (« toi tu conseils quoi ? jeoffrey? » —
  conseil : le garder, la licence MIT le porte déjà, une décision a un auteur, un prénom n'est pas
  un identifiant) ; les rapports de contrôle et le journal restent, anonymisés et marqués comme
  copies ; la première version publique sera la **4.0.0**, parce que `template-upgrade` refuse de
  monter vers un numéro plus petit. Double arrêt : `STOP 1` (construire l'outil, pas publier ;
  alternative : attendre la cinquième passe) → « ok » ; `STOP 2` → « Confirmé : branche
  claude/v3.19-publication dans ~/Projets/Squelette V3 -runtime-proof, pas de push. »
  La publication elle-même sera un double arrêt à part, après la cinquième passe. La promotion
  reste une décision séparée.
- `TPL-D-064` — **Promotion.** `claude/v3.19-publication` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.19.0` (`skeleton_version`
  `3.19.0`, version où le squelette sait produire sa copie publique — `TPL-D-063`). Mandat de
  promotion : la double confirmation du 2026-09-11, qui couvrait promotion et tag. Livraison en
  deux commits (`ce659a9` outil, `6392766` vue), 158 essais OK dans le template, `audit`,
  `bootstrap-audit` et `demo.py --check` PASS. Le tag est posé sur le commit qui enregistre cette
  décision ; la vue est régénérée ensuite et committée à part : `main` est un commit devant
  `v3.19.0`. Envoi vers `origin` et `nas` et release GitHub : gestes du Project Owner
  (`TPL-D-004`). La publication réelle attend la cinquième passe.
- `TPL-D-065` — **Les six constats de la cinquième passe de contrôle (3.19.1).** La cinquième
  passe, sur la `3.18.2`, verdict `SQUELETTE_3.18.2_REQUIRES_MAJOR_REDLINE` : deux défauts majeurs
  — le rangement des copies jetables de la `3.18.2` retirait un worktree qui n'était pas au
  contrôleur, avec la note posée dedans et celle posée à côté, parce qu'il reconnaissait les
  siennes à un nom de dossier et à un âge (`F-01`) ; un nom que Git cite (accent, tabulation)
  rendait inopérante la règle de contenu des fusions, deux lectures vides se comparant égales
  (`F-02`) — et quatre modérés : un renommage légitime bloquait l'intégration (`F-03`), `close`
  refusait le commit autorisé d'un fichier accentué (`F-04`), deux lignes `Chosen option: REJECT`
  faisaient accepter une nouvelle cible de baseline (`F-05`), le scan JSON livré dépendait encore
  d'un fichier ignoré (`F-06`) ; plus six écarts documentaires (`D-01` à `D-06`). Ce qu'elle
  valide : les quinze corrections antérieures tiennent toutes, 157 essais passent. Question du
  Project Owner : « on est plus dans la cyber sécurité que dans un bug réel ? Une autre passe
  générale à effectuer après ? » — réponse : quatre bugs d'usage courant (perte de fichiers par
  une commande ordinaire, noms accentués du quotidien, renommage, essai), deux qui tiennent la
  promesse centrale du squelette (rien ne se glisse en silence dans une fusion ni dans une
  décision) ; ensuite une contre-vérification ciblée des six corrections par le même contrôleur,
  une pause sans nouvelle règle, et la prochaine passe générale juste avant la `4.0.0` publique.
  Double arrêt : `STOP 1` (corriger les six, chacune avec son essai rouge sur la `3.19.0`, et
  réécrire les six phrases de doctrine ; alternative : ne corriger que les deux majeures, non
  recommandée) → « ok » ; `STOP 2` (périmètre exact) → « Confirmé : branche
  claude/v3.19.1-noms-et-copies dans ~/Projets/Squelette V3 -runtime-proof, pas de
  push. » La promotion reste une décision séparée.
- `TPL-D-066` — **Promotion.** `claude/v3.19.1-noms-et-copies` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.19.1` (`skeleton_version`
  `3.19.1`, version où les chemins sont lus tels que les fichiers sont nommés et où le contrôleur
  ne retire que les copies jetables qu'il prouve siennes — `TPL-D-065`). Mandat de promotion : la
  double confirmation du 2026-09-11, qui couvrait promotion et tag. Livraison en trois commits
  (`5e5a305` les six corrections, `647cf34` le script d'export gardé privé, `f0d914c` le droit
  d'exécution de deux scripts, perdu par une retouche sur le dossier monté), 164 essais OK dans le
  template sur l'état committé, `audit`, `bootstrap-audit` et `demo.py --check` PASS, export de
  `HEAD` mesuré `EXPORTED`. Le tag est posé sur le commit qui enregistre cette décision ; la vue
  est régénérée ensuite et committée à part : `main` est un commit devant `v3.19.1`. Envoi vers
  `origin` et `nas` et release GitHub : gestes du Project Owner (`TPL-D-004`). Ensuite : la
  contre-vérification ciblée des six corrections, puis Alpha en 3.19.1.
- `TPL-D-067` — **Première publication : la 3.19.1, sous le nom `squelette`.** « Avant cela tu me
  confirmes que la version en ligne de squelette est anonymisée ? Si non faut publier la version
  anonyme ! » (2026-09-11) — la version en ligne est le dépôt privé, non anonymisé ; la copie
  publique n'existait qu'à l'essai. Choix arrêtés : la **première version publique est la 3.19.1
  telle quelle**, même numéro que le privé et que le projet adopté — la `4.0.0` annoncée par
  `TPL-D-063` est gardée pour la vraie nouvelle génération, après la passe générale ; le dépôt
  public s'appelle **`squelette`** (« squelette », réponse à « quel nom lui donnerais-tu ? »), le
  dépôt privé sera renommé `squelette-atelier` par le Project Owner, le dossier local de l'export
  est `~/Projets/squelette`, créé par lui ; les commits publics sont signés « Jeoffrey » avec une
  adresse d'alias qu'il a donnée, jamais l'adresse du dépôt privé ; **« efface le nas »** : la
  marque de la machine de sauvegarde devient « NAS » dans la copie. Double arrêt : `STOP 1`
  (deux dossiers cibles, l'action, l'alternative : attendre la contre-vérification, plus
  recommandée) → « ok, efface le nas » ; `STOP 2` (périmètre exact, cinq étapes) → « Confirmé :
  publication de la 3.19.1 dans ~/Projets/squelette et décision dans
  ~/Projets/Squelette V3 -runtime-proof, pas de push. » Côté privé, hors core et
  sans version nouvelle : l'outil d'export remplace `NAS`/`nas` et les refuse s'ils survivent ;
  et un mot n'est plus borné par `\b` mais par tout ce qui n'est pas une lettre ou un chiffre —
  `STEP_2_DONE_ON_REAL_Alpha` gardait son acronyme à travers deux exports, `\b` tenant le
  souligné pour l'intérieur d'un mot (`word_pattern`). Mesuré sur `v3.19.1` : 168 + 5
  occurrences de l'acronyme, 18 + 76 de la marque, 27 fichiers modifiés, 1 renommé, l'outil
  retiré, 0 fichier core, 0 mot interdit. Dette notée, hors périmètre : la vérification de
  l'essai `test_the_published_copy_carries_nothing_private_and_leaves_the_core_untouched` borne
  encore l'acronyme par `\b` (fichier core, à aligner à la prochaine version). Premier export réel
  refusé par l'outil lui-même : son dossier, retiré *après* extraction, n'a pas pu l'être sur un
  dossier où la suppression n'est pas permise, et il s'est refusé sur ses propres tables (bon
  refus) ; le dossier n'est plus extrait du tout (`tar --exclude`), et un refus explicite reste
  s'il survivait. Second constat dans la copie : `demo.py --check` y dérivait d'un chiffre — le
  transcript comptait les fichiers suivis (123), et le miroir en a un de moins (l'outil) ; la
  phrase ne compte plus (`examples/hello-squelette/demo.py`, hors core), transcript régénéré. La
  copie publique est donc produite depuis `main` à cette date — core identique à `v3.19.1` à
  l'octet, manifeste `3.19.1`, plus la maintenance de publication du jour — et porte le tag
  `v3.19.1` de son côté. Rien n'est envoyé :
  renommer le privé, créer le dépôt public et pousser sont les gestes du Project Owner
  (`TPL-D-004`). **Faits le jour même** : le privé renommé `JyMinet/squelette-atelier` et poussé
  (`origin` et NAS à `b256b08`), le dépôt public `JyMinet/squelette` créé, `main` et le tag
  `v3.19.1` poussés, release publiée — https://github.com/JyMinet/squelette/releases/tag/v3.19.1.

## Décisions du Project Owner — 2026-09-12

- `TPL-D-068` — **Le rapport de la seconde revue indépendante rejoint la collection.** La série
  des rapports de contrôle sous `provenance/maintenance/` allait de la `3.9.0` à la `3.18.2` sans
  trou, sauf un : la seconde revue indépendante, confiée au fournisseur Codex sur le tag `v3.13.0`
  (`ad95129`), sept constats dont deux `MAJOR` et le verdict
  `SQUELETTE_3.13.0_REVUE_REQUIRES_MAJOR_REDLINE`, était restée dans son atelier
  (`~/Projets/squelette-revue-2`) au lieu de suivre ses correctifs dans le dépôt.
  Ses constats, eux, ont bien été traités le 2026-09-09 par la `3.14.0` (`TPL-D-031`), avec le
  huitième que leur contre-vérification a fait apparaître. Mandat : « Rapatrier ce rapport dans
  provenance/maintenance/, nommé comme les autres de la série » (2026-09-12). Le rapport est copié
  tel quel, octet pour octet, sous le nom de la série et daté du jour de la revue :
  `provenance/maintenance/2026-09-09-controle-independant-3.13.0.md`, SHA-256
  `7e6049017a14d2265e48d2d22892078f47ba7b5064b4aeb035ede2f5948f2ab4`. Rien d'autre ne change :
  aucun fichier core, aucune version nouvelle, aucune promotion, la vue n'est pas régénérée. Les
  liens de preuve que le rapport porte désignent les `runs/` de son atelier, qui ne le suit pas
  dans le dépôt — comme les rapports voisins, qui nomment leurs `runs/` sans les emporter. Dette
  notée, hors périmètre : la contre-revue (`contre-revue-3.13.0.md`), qui a confirmé les sept
  constats et en a établi un huitième, reste elle aussi hors du dépôt.
- `TPL-D-069` — **La contre-revue rejoint le rapport qu'elle contre-vérifie ; la dette de
  `TPL-D-068` est soldée le jour même.** Le jour de la seconde revue indépendante, sa
  contre-vérification confirmait ses sept constats, n'en rejetait aucun, et en établissait un
  huitième plus grave, trouvé en vérifiant le premier : le garde-fou de commit annonçait « audit
  PASS on the staged state » alors qu'il lisait l'arbre de travail, si bien qu'un record de
  gouvernance falsifié, indexé puis masqué, entrait dans l'historique avec son accord. C'est elle
  qui a cadré le lot unique de la `3.14.0` (`TPL-D-031`). Elle n'avait jamais quitté l'espace de
  travail de l'agent : ni dans le dépôt, ni sur le poste du Project Owner. Mandat : « go »
  (2026-09-12), sur la proposition de la faire rentrer par le même chemin que le rapport. Elle est
  écrite telle quelle sous `provenance/maintenance/2026-09-09-contre-revue-3.13.0.md`, à la date de
  sa rédaction, SHA-256
  `6ca656f9cd518d9d22e74845610f816a53175a2188371dbb8b1b713e7fbefe2a`. Son texte n'est pas retouché :
  elle désigne le rapport par le nom qu'il portait dans l'atelier (`REVUE_SQUELETTE_3.13.0.md`),
  devenu `2026-09-09-controle-independant-3.13.0.md` dans le dépôt — un rapport rapatrié se
  copie, il ne se réécrit pas. Rien d'autre ne change : aucun fichier core, aucune version
  nouvelle, aucune promotion, la vue n'est pas régénérée. Avec `TPL-D-068`, le dossier de la
  seconde revue est désormais complet dans le dépôt : le rapport, et ce qui l'a contre-vérifié.

- `TPL-D-070` — **La reprise d'un chantier bloqué passe le garde-fou.** La revue indépendante de
  « P7 étape 1 » (deux contrôleurs séparés, dossier `squelette-revue-p7`) a trouvé, en cherchant
  autre chose, un défaut du contrôleur `3.19.1` : **avec le garde-fou installé, un chantier bloqué
  qui porte ses propres commits ne peut plus reprendre dès qu'un autre chantier a été clos entre
  temps sur la canonique.** La fusion d'alignement est refusée parce que le commit de clôture du
  chantier voisin est jugé contre la seule branche courante, qui ne le contient pas encore.
  Reproduit, puis expliqué : la suite d'essais ne le voyait pas parce qu'elle monte ses dépôts
  **sans installer le garde-fou** — le même parcours passe sans lui et échoue avec. Décision :
  « Option A, et le grain de sable d'abord » (2026-09-12), sur la proposition de corriger ce
  défaut avant de construire P7, un prototype bâti sur un contrôleur qui refuse une reprise
  légitime ne se vérifiant pas proprement. Correctif sur `claude/v3.19.2-reprise-sous-garde-fou`,
  version `3.19.2` ; la promotion reste une décision séparée.

- `TPL-D-071` — **La borne d'éligibilité de « la question de l'existant » : l'option A, et le
  dossier du chantier rejoint le dépôt.** L'étape 1 de P7 ajoute à la fiche d'un chantier une ligne
  « qu'est-ce qui existe déjà là-dessus, et où ? », avec deux réponses possibles et un refus au
  démarrage tant qu'elle manque. La phase de mesure, en lecture seule, a levé un arrêt : la règle ne
  doit valoir que pour les chantiers ouverts après son arrivée, or aucune des deux baselines
  déclarées (`legacy_baseline`, `authorities_baseline`) ne date l'adoption d'une **version** par un
  projet. Revue par deux contrôleurs indépendants (dossier `squelette-revue-p7`, rapports rapatriés
  ci-dessous), puis réconciliation. Décision : « Option A » (2026-09-12) — **la marque voyage dans la
  fiche** : la voie d'admission marque la fiche, le contrôleur ne réclame la déclaration qu'aux
  fiches marquées, les fiches déjà présentes n'en portent pas et ne sont jamais interrogées. L'option
  C (borne déduite de l'historique Git) est **écartée** : elle se fausse en silence sur un historique
  regroupé, exporté, cloné superficiellement ou ramené en arrière. Les options B (borne signée par
  décision, forme de `authorities_baseline`) et D (inventaire figé à la montée) restent des replis
  documentés. L'avenant 1 ajoute quatre définitions sans lesquelles la règle se contredit en usage
  réel — « ouvert » veut dire admis et non démarré ; toutes les voies d'admission posent la marque, et
  une fiche arrivée autrement est **ancienne** mais signalée ; la déclaration est exigée au premier
  départ effectif, `resume` compris ; une fiche administrative ne périme jamais sa propre empreinte de
  lecture — plus trois comportements à démontrer (B11 à B13) et un **erratum** au rapport de mesure :
  sa conclusion « le record n'entre pas dans l'empreinte » vaut pour le routage livré, pas pour un
  projet libre de sa liste. Le chantier passe à `SCOPED` ; la construction n'est pas commencée et
  reste prévue pour la `3.20.0`, après le correctif `3.19.2`.

- `TPL-D-072` — **Promotion de la `3.19.2`.** « Promeus, puis enchaîne » (2026-09-12), sur la
  proposition de promouvoir avant d'entreprendre quoi que ce soit d'autre : un projet ne monte que
  depuis une version promue et étiquetée, jamais depuis une branche de travail.
  `claude/v3.19.2-reprise-sous-garde-fou` est promue branche canonique par fast-forward de `main` ;
  la baseline promue reçoit le tag `v3.19.2`, posé sur le commit qui enregistre cette décision ; la
  vue est régénérée ensuite et committée à part, si bien que `main` est un commit devant le tag.
  L'envoi vers `origin` et vers le NAS, ainsi que la release GitHub, restent les gestes du Project
  Owner (`TPL-D-004`). Suite annoncée le même jour : la montée d'Alpha — en `3.18.1`,
  elle passera donc directement en `3.19.2` — puis le rafraîchissement du miroir public anonymisé,
  chacun sous son propre double arrêt.

## Décisions du Project Owner — 2026-09-10 (suite 10)

- `TPL-D-051` — **Deux des trois constats de la troisième passe de contrôle (3.17.0).** La troisième
  passe a ouvert trois thèmes que personne n'avait attaqués — les baselines déclarées, deux sessions
  simultanées, la naissance d'un projet par le geste réel — et les trois ont cédé. Verdict
  `SQUELETTE_3.16.2_REQUIRES_MAJOR_REDLINE`. Ce qu'elle valide au passage : les huit corrections
  précédentes tiennent toutes, la montée de version n'a plus son impasse, et les 141 essais passent.
  Décision : « on avance ! » (2026-09-10), sur la proposition de corriger tout de suite les deux
  constats corrigeables — `F-10` le `.gitignore`, `F-09` les écritures simultanées — et de **cadrer
  d'abord** `F-08`, la baseline défigeable, qui demande d'ancrer une déclaration à la décision qui
  la nomme, donc de toucher au format des décisions, alors qu'Alpha en a deux
  déclarées. La promotion reste une décision séparée.

## 2026-09-12 — `claude/v3.19.2-reprise-sous-garde-fou` — ce que le prochain commit portera vraiment

- Mandat : `TPL-D-070`. Double arrêt : `STOP 1` (dossier cible, action, alternative : garder le
  correctif dans la copie de session et remettre un patch) → « Le correctif et le rangement » ;
  `STOP 2` (périmètre exact reformulé) → « Confirmé : branche
  claude/v3.19.2-reprise-sous-garde-fou dans ~/Projets/Squelette V3 -runtime-proof,
  main intouché, pas de tag, pas de push. »
- Baseline : `main` à `ebf62f4` (`v3.19.1` = `ae8bace`, plus trois commits de provenance).
- Origine : la revue indépendante de « P7 étape 1 — le choix de la borne d'éligibilité »
  (`squelette-revue-p7`, deux contrôleurs, verdict `REQUIRES_MAJOR_REDLINE`). Le défaut n'a rien
  à voir avec la question de l'existant ; il a été rencontré en la mesurant.
- **Le défaut.** `done_evidence_errors` juge le `close_head` d'un chantier `DONE` par
  `merge-base --is-ancestor <close_head> HEAD`. Pendant la fusion d'alignement d'une reprise, la
  branche courante ne contient pas encore la canonique : le commit de clôture du chantier voisin
  n'y est pas, le contrôle échoue, et le garde-fou refuse le commit de fusion
  (`MODE_AUDIT — SCHEMA_VALIDATION: WI-002: close_head is missing or not in current history`).
  Le même refus tombe sur la photo de l'index, construite par `staged_worktree` avec `HEAD` pour
  seul parent alors que le commit réel en aura deux.
- **Pourquoi la suite ne le voyait pas.** `make_normal_copy` ne pose pas le garde-fou, et deux
  essais seulement l'installent. `test_resume_aligns_diverged_branch_by_merge_and_closes`
  mesurait donc un parcours qui n'existe pas chez un utilisateur. Règle à retenir : un essai qui
  porte sur ce que le garde-fou voit doit installer le garde-fou.
- **Le correctif, deux touches de la même idée.** `history_heads()` nomme ce dont le prochain
  commit descendra — `HEAD`, plus chaque parent inscrit dans `MERGE_HEAD`, lu ligne par ligne pour
  ne pas perdre une fusion à plus de deux parents ; `in_current_history()` juge une ascendance
  contre cet ensemble et non contre `HEAD` seul. `done_evidence_errors` l'emploie ; `staged_worktree`
  fabrique désormais sa photo avec les mêmes parents que le commit réel, ce que sa propre docstring
  promettait déjà (« exactly what the commit would create »).
- **Essai ajouté**, rouge avant, vert après :
  `test_resume_merges_under_the_installed_commit_gate` — le même parcours de reprise, avec
  `install-gate` posé avant la fusion.
- 165 essais verts (164 + 1) ; démo régénérée (`demo.py --write`, la seule différence est la ligne
  de version) ; manifeste du core à `3.19.2`, 24 fichiers.
- **Rien à réinstaller.** `scripts/hooks/pre-commit` n'a pas changé : il appelle le contrôleur, et
  c'est le contrôleur qui est corrigé. Un projet déjà monté reçoit le correctif par
  `template-upgrade` sans rejouer `install-gate` pour ce motif.
- Portée volontairement étroite : les autres tests d'ascendance contre `HEAD` (baselines déclarées,
  contrôles de clôture, `status`) ne sont pas touchés, faute de scénario d'échec démontré. Observation
  laissée ouverte : ils jugeraient de la même façon un commit arrivant par une fusion en cours.

## 2026-09-11 — `claude/v3.19.1-noms-et-copies` — les noms lus tels quels, les copies prouvées siennes

- Mandat : `TPL-D-065`. Double arrêt : `STOP 1` posé (dossier, action, alternative) → « ok » ;
  `STOP 2` (périmètre exact reformulé) → « Confirmé : branche claude/v3.19.1-noms-et-copies dans
  ~/Projets/Squelette V3 -runtime-proof, pas de push. »
- Baseline : `main` à `29343f7` (`v3.19.0` = `6fb869a`, plus la vue régénérée).
- Rapport de la cinquième passe rapatrié :
  `provenance/maintenance/2026-09-11-controle-independant-3.18.2.md`.
- **F-01 — le contrôleur ne retire que ce qu'il prouve sien.** La purge de la `3.18.2`
  reconnaissait ses copies jetables au préfixe du dossier porteur et à l'âge du checkout, puis
  effaçait le dossier porteur en entier : un worktree de relecture sous un dossier au nom
  ressemblant, sa note non committée et la note posée à côté ont disparu sur un commit ordinaire ;
  et une répétition suspendue, vieillie, a perdu son checkout sous les pieds d'une seconde
  commande. Désormais chaque copie jetable naît dans un dossier porteur qui contient une marque
  (`PROJECT_CONTROL_THROWAWAY` : dépôt, nom du checkout, pid, date), tenue verrouillée (`flock`)
  tant que la commande vit (`open_throwaway` / `close_throwaway`). Le rangement
  (`purge_stale_throwaway_checkouts`) ne retire qu'un worktree dont le porteur a la marque, qui
  nomme ce dépôt et ce checkout, et dont le verrou est libre — ce que le système ne rend qu'à la
  mort de la commande ; il retire ce checkout, la marque, et le porteur s'il est vide, jamais
  récursivement. Un dossier hors de la liste des worktrees n'est effacé que s'il est un checkout
  lié de ce dépôt (`is_own_linked_checkout`). Ni nom, ni âge, ni voisin : plus aucun critère de
  ce genre.
- **F-02 / F-04 — les chemins sont lus tels que les fichiers sont nommés.** `git diff
  --name-only`, `show --name-only` et `ls-tree --name-only` citent et échappent un nom qu'ils
  jugent inhabituel (`"r\303\251sum\303\251.py"`) ; la règle de contenu des fusions les
  réutilisait comme noms de blobs, chaque lecture échouait, et deux échecs se comparaient égaux :
  une valeur ajoutée pendant la fusion sous un nom accentué (ou avec une tabulation) était
  committée comme intégration, audit vert. `close --commit` faisait de même et refusait le commit
  réellement autorisé d'un fichier accentué, sauf réglage local `core.quotePath=false`. Nouveau
  lecteur `git_paths` (`-z`, décodage `surrogateescape`) pour la fusion, la clôture et les records
  figés ; et une lecture qui échoue **refuse** (« what it writes for these paths could not be
  read ») au lieu de comparer.
- **F-03 — un renommage compte pour ses deux noms.** La branche renomme un fichier sans en
  changer une ligne, la canonique modifie l'ancien nom : Git fusionne juste, dans le nouveau nom,
  et la règle de contenu refusait ce résultat comme différent de la branche. Le diff de la branche
  est lu avec `-M` ; l'ancien et le nouveau nom sont à elle, et un changement canonique de l'un
  fait de l'autre une résolution.
- **F-05 — une décision choisit une fois.** `Chosen option: REJECT` écrit deux fois : le champ
  lu comme valeur unique répondait `None`, qui n'est pas `REJECT`, et la baseline avançait vers
  le commit qu'une décision deux fois refusée nommait. `human_decision_field_values` lit toutes
  les lignes ; `require_baseline_named` refuse plus d'une ligne `Chosen option`, quelle qu'elle
  soit, et toujours `REJECT`.
- **F-06 — le scan JSON lit ce que Git voit.** `test_all_json_and_schema_documents_parse`
  parcourait encore le dossier (`rglob`), `.git` excepté : un téléchargement à moitié écrit dans
  un dossier ignoré le faisait échouer. Il lit `git ls-files --cached --others
  --exclude-standard -- '*.json'` : suivis ou présents et non ignorés, jamais ignorés. Erratum
  posé sur la mention « dette close » de la `3.18.1` (`D-06`).
- **Un défaut trouvé en chemin : l'export de la `3.19.0` refusait sa propre publication.** Son
  essai nommait en clair les chaînes interdites ; `tests/test_template.py` étant core, l'export
  de tout `HEAD` portant ce fichier refusait (« a core file would change »). La suite de la
  `3.19.0` ne l'a pas vu : l'export lit une révision committée, et le fichier a été committé
  après la suite. L'essai lit désormais les chaînes dans le script, et vérifie d'abord que
  **l'arbre de travail** ne porte dans aucun fichier core ce que l'export réécrirait. Derrière
  ce premier refus, un second : le script d'export lui-même, une fois committé, restait dans la
  copie avec ses tables — précisément les chaînes que la copie ne doit pas porter — et l'export
  se refusait sur lui. **Le script reste privé** : son dossier
  `provenance/maintenance/publication/` est retiré de la copie (`REMOVED`), refus si un fichier
  core y vivait, et l'essai de la copie s'ignore là où le script est absent — dans le miroir
  public, qui est un template lui aussi. Mesuré sur `HEAD` de cette branche : 26 fichiers
  modifiés, 1 renommé, 1 dossier retiré, tous sous `provenance/`, 0 fichier core.
- **Doctrine (`D-01` à `D-06`)** : `pre-commit` « en lecture seule » dit ce qu'il extrait et
  retire ; « sans `--apply`, rien n'est écrit » dit « dans le projet » ; retrait et déplacement
  d'une baseline sont deux gestes, chacun avec sa décision (`ADOPTION.md`) ; la citation de la
  décision d'origine est une obligation de rédaction, le commit nommé est ce qui est vérifié ;
  le paragraphe des copies jetables dit la marque, le verrou, et ce qui n'est jamais touché ;
  la règle de contenu des fusions nomme le renommage et la lecture des chemins tels quels ;
  `REJECT` et le doublon de `Chosen option` ne déclarent rien.
- Sept essais nouveaux, un réécrit — `test_an_integration_merge_edited_under_a_name_git_quotes_is_refused`,
  `test_a_closure_accepts_the_authorized_commit_of_a_file_git_quotes`,
  `test_a_rename_on_the_branch_merges_with_a_canonical_change_to_the_old_name`,
  `test_a_decision_that_chooses_twice_declares_no_baseline`,
  `test_the_gate_never_touches_a_worktree_that_is_not_its_own`,
  `test_the_gate_removes_its_own_dead_throwaway_checkouts_and_leaves_a_running_one` (remplace
  l'essai de la `3.18.2`), `test_a_json_file_the_project_ignores_does_not_fail_its_json_check` —
  tous rouges sur la `3.19.0` (copie jetable portant le contrôleur `3.19.0` et ces essais ; celui
  des JSON, sur le fichier d'essais de la `3.19.0` augmenté de lui seul), verts ici. 164 essais.
- Manifeste régénéré (`skeleton_version` `3.19.1`), démo et transcript régénérés.
- Non fait : pas de push ; Alpha reste en `3.18.1` ; la contre-vérification ciblée
  et la publication attendent.

## 2026-09-11 — `claude/v3.19-publication` — le squelette sait se publier

- Mandat : `TPL-D-063`. Double arrêt : `STOP 1` posé (dossier, action, alternative) → « ok » ;
  `STOP 2` (périmètre exact reformulé) → « Confirmé : branche claude/v3.19-publication dans
  ~/Projets/Squelette V3 -runtime-proof, pas de push. »
- Baseline : `main` à `dba40ea` (`v3.18.2` = `7f8f0b3`, plus la vue régénérée).
- Chantier : `P18`, fiche `provenance/maintenance/scopes/p18-scope-publication.md`.
- **Le script d'export**, `provenance/maintenance/publication/export_public.py` — hors du core, il
  ne part pas dans les projets dérivés. `git archive <révision>` vers un dossier cible vide, table
  de remplacements en tête du fichier (adresse, chemins, nom du projet adopté sous toutes ses
  formes, dépôt de sauvegarde, élision française rétablie après le nom de code), renommage des
  fichiers dont le nom porte l'acronyme, ligne « copie anonymisée » en tête de chaque Markdown
  modifié sous `provenance/maintenance/`, JSON revalidé après remplacement, et **refus** s'il reste
  un mot interdit dans un contenu ou un nom de fichier, ou si un fichier core devait changer.
  Mesuré sur `HEAD` : 23 fichiers modifiés, 1 renommé, tous sous `provenance/`, 0 fichier core.
- **Un essai propre au template**, ignoré dans un projet dérivé :
  `test_the_published_copy_carries_nothing_private_and_leaves_the_core_untouched` — rouge sur
  la `3.18.2` (le script n'existe pas), vert ici : aucun mot interdit dans l'export de `HEAD`,
  contenus et noms compris ; les 24 fichiers core et le manifeste identiques à l'octet à ce que
  `HEAD` tient ; ligne d'anonymisation en tête du rapport de la quatrième passe ; licence intacte ;
  prose relue (« d'Alpha »). 158 essais.
- Manifeste régénéré (`skeleton_version` `3.19.0`), démo et transcript régénérés.
- Non fait : aucun export réel, aucun dépôt public, pas de push ; Alpha reste en
  3.18.1.

## 2026-09-11 — `claude/v3.18.2-copies-perimees` — le garde-fou range ses copies jetables

- Mandat : `TPL-D-061`. Double arrêt : `STOP 1` posé (dossier, action, alternative : ne rien faire)
  → « ok » ; `STOP 2` (périmètre exact reformulé) → « Confirmé : branche
  claude/v3.18.2-copies-perimees dans ~/Projets/Squelette V3 -runtime-proof, pas de
  push. »
- Baseline : `main` à `5a01892` (`v3.18.1` = `00e02b4`, plus la vue régénérée).
- **Le contrôleur retire ses checkouts jetables périmés** (`purge_stale_throwaway_checkouts`), au
  démarrage du garde-fou et de la répétition de montée : un worktree lié dont le dossier porteur
  commence par `project-control-staged-` ou `project-control-upgrade-` et dont le checkout a plus
  de quinze minutes (`THROWAWAY_CHECKOUT_MAX_AGE_SECONDS`) est retiré et son dossier effacé ; un
  checkout plus récent, ou un worktree qui n'est pas le sien, n'est jamais touché. Un essai, rouge
  sur la `3.18.1` : un périmé retiré au commit suivant, un frais et un worktree ordinaire (vieux
  lui aussi) laissés.
- Le message de la répétition ne compte plus le manifeste parmi les fichiers core qui diffèrent
  de `HEAD` (il affichait « 1 » quand rien ne changeait).
- Tableau de bord du template : la section « maintenant » réécrite (3.18.1 des deux côtés,
  baselines d'Alpha confirmées, quatre passes et quinze défauts corrigés, 156 essais, deux projets
  réels), `current_version` remis à jour ; ce qui attend le Project Owner : la promotion, puis la
  cinquième passe.
- Documentation : `project_control/README.md`, une phrase sur la purge.
- 157 essais. Manifeste régénéré (`skeleton_version` `3.18.2`), démo et transcript régénérés.
- Non fait : push, release ; Alpha reste en 3.18.1 — la 3.18.2 ne lui apporte que la
  purge, il montera avec la version suivante ou sur décision.

## 2026-09-11 — `claude/v3.18.1-fusion-et-repetition` — une fusion n'emporte que ce que sa branche a produit

- Mandat : `TPL-D-059`. Double arrêt : `STOP 1` posé (dossier, action, alternative : la majeure
  seule) → « ok » ; `STOP 2` (périmètre exact reformulé) → « Confirmé : branche
  claude/v3.18.1-fusion-et-repetition dans ~/Projets/Squelette V3 -runtime-proof,
  pas de push. »
- Baseline : `main` à `4b44cc8` (`v3.18.0` = `df551cc`, plus la vue régénérée).
- Rapport de contrôle rapatrié : `provenance/maintenance/2026-09-11-controle-independant-3.18.0.md`.
- **F12-01 — une fusion d'intégration emporte le contenu de sa branche, pas seulement ses chemins.**
  `integration_merge_errors` compare désormais, pour chaque chemin apporté que seule la branche a
  changé depuis la base, le blob indexé au blob de la branche (`MERGE_HEAD`) ; un chemin changé des
  deux côtés est une résolution, jugée par l'audit. Et `BASELINE_CHANGE_MANDATED` court partout où
  l'état du projet est indexé — branche de chantier, canonique, fusion — au lieu de la seule branche
  de chantier hors fusion. Deux essais avec une vraie fusion `--no-ff --no-commit` éditée avant son
  commit : retrait refusé, recul refusé, la même fusion non éditée acceptée.
- **F13-01 — un audit qui n'échoue que sur le garde-fou est une réussite.** La répétition lisait le
  code de sortie non nul comme un second échec générique et refusait une montée légitime dont seul
  le hook changeait. Elle distingue maintenant les échecs rapportés des échecs exemptés, et ne lit
  le code de sortie que quand aucun échec n'est rapporté.
- **F13-02 — la répétition est mesurée contre `HEAD`.** Elle écrivait dans la copie jetable ce que
  l'application allait écrire sur le disque ; un core déjà sur le disque sans être committé lui
  laissait tout « identique », et l'audit tournait sur l'ancien contrôleur tenu par `HEAD`. Elle
  écrit désormais chaque fichier core dont le blob à `HEAD` diffère de la source (`blob_digest`),
  quel que soit le disque.
- **F14-01 — l'interruption n'est pas une exception.** `FileTransaction.write_bytes` attrapait
  `Exception` pour effacer son temporaire ; un `KeyboardInterrupt` passait au travers et laissait
  `.HUMAN_DECISIONS.md.<aléa>` inexpliqué. `BaseException`, puis relance.
- **Les copies d'essai n'emportent plus ce que le squelette ignore** (`fixture_copy_ignore`, à
  partir de `git ls-files --others --ignored --exclude-standard --directory` sur le squelette), pour
  `make_copy` comme pour les sources de montée fabriquées. La dette de la `3.17.1` est close.
  *(Erratum 3.19.1 : close pour les copies d'essai seulement ; le scan JSON du template lisait
  encore le dossier — F-06 de la cinquième passe, corrigé en 3.19.1.)*
- **Une décision `REJECT` ne déclare pas de baseline** (observation de la passe, retenue).
- Sept essais, tous rouges sur la `3.18.0` — vérifié sur une copie jetable portant le contrôleur
  3.18.0 et ces essais, avec un JSON à moitié écrit dans un dossier ignoré pour l'essai des
  copies — et verts ici : `test_a_baseline_cannot_be_removed_by_editing_an_integration_merge`,
  `test_a_baseline_cannot_recede_through_an_integration_merge`,
  `test_an_upgrade_that_only_changes_the_gate_is_rehearsed_and_accepted`,
  `test_a_rehearsal_rerun_after_an_uncommitted_apply_still_audits_with_the_new_controller`,
  `test_an_interruption_leaves_no_temporary_file_behind`,
  `test_a_fixture_copy_carries_nothing_the_template_ignores`,
  `test_a_rejected_decision_declares_no_baseline`. 156 essais.
- Documentation : `project_control/README.md` (ce qu'une fusion d'intégration peut emporter, la
  répétition mesurée contre `HEAD`, l'exemption du garde-fou lue comme telle, `REJECT`) ; fiche
  `P17` : section 9, la quatrième passe.
- Manifeste régénéré (`skeleton_version` `3.18.1`), démo et transcript régénérés.
- Non fait : push, release, montée d'Alpha vers la 3.18.1 (sous son propre double
  arrêt).

## 2026-09-11 — `claude/v3.18-baseline-ancree` — la ligne du passé ne bouge que sur décision

- Mandat : `TPL-D-056`. Double arrêt : `STOP 1` posé (dossier, action, alternative) → « ok » ;
  `STOP 2` (périmètre exact reformulé) → « Confirmé : branche claude/v3.18-baseline-ancree dans
  ~/Projets/Squelette V3 -runtime-proof, pas de push. »
- Baseline : `main` à `fae1f4c` (`v3.17.1` = `d437c16`, plus la vue régénérée).
- Chantier : `P17`, fiche déposée dans `provenance/maintenance/scopes/p17-scope-baseline-defigeable.md`
  avec les quatre réponses du Project Owner.
- **Règle 1 — la décision d'une baseline nomme son commit.** `legacy_baseline()` et
  `authorities_baseline()` exigent que la décision citée porte `Legacy baseline commit: <commit>`
  (resp. `Authorities baseline commit:`) exactement une fois, égal au commit déclaré. Une décision
  qui a autorisé la ligne A ne peut plus déclarer la ligne B ; le refus nomme le commit que la
  décision cite réellement. Aucune décision figée n'est réécrite : un projet antérieur à la règle
  **confirme** ses baselines par de nouvelles décisions que l'état du projet cite ensuite.
- **Règle 2 — retirer une baseline est un geste à part.** Sur une branche de chantier, le garde-fou
  compare l'état du projet indexé à celui de `HEAD` (`BASELINE_CHANGE_MANDATED`) : une baseline
  passée à `null` exige qu'une décision du chantier en cours, **lue dans `HEAD`** et non sur le
  disque, porte `Legacy baseline removed: <commit>`. Les fichiers sont lus par `git show`, jamais
  dans l'arbre de travail.
- **Règle 3 — une baseline ne recule jamais.** Le même garde-fou refuse un déplacement vers un
  commit qui ne descend pas de l'ancien ; vers l'avant, la décision qui nomme le nouveau commit est
  vérifiée par l'audit de l'état indexé, qui suit.
- **Règle 4 — une montée se répète avant de s'écrire.** `template-upgrade` extrait `HEAD` dans un
  worktree lié jetable, y écrit le core prévu, le committe (`--no-verify`, hooks neutralisés,
  identité propre) et lance `audit` **du nouveau contrôleur** dessus ; les `FAIL` sont rapportés
  dans `UPGRADE_REHEARSAL`, `COMMIT_GATE` excepté puisque l'application réinstalle le garde-fou ;
  `--apply` refuse tant que la répétition refuse. Le worktree est retiré dans tous les cas. La
  répétition porte sur ce que Git tient : un fichier amorcé mais non committé n'y est pas, et
  l'essai de la 3.16.0 committe désormais ses amorces avant d'appliquer, comme la doc le disait.
- Six essais, tous rouges sur la `3.17.1` (vérifié sur une copie jetable portant le contrôleur de
  la 3.17.1 et ces essais) et verts ici :
  `test_a_decision_that_declared_one_baseline_cannot_declare_another`,
  `test_a_baseline_leaves_only_on_a_decision_that_names_the_removal` (vrai `git commit` refusé,
  puis accepté avec la décision),
  `test_a_baseline_never_recedes` (vrai `git commit`),
  `test_an_upgrade_is_rehearsed_before_it_is_written` (une source dont le contrôleur apporte une
  règle que le projet ne satisfait pas ; aucun worktree laissé derrière),
  `test_the_frozen_history_can_no_longer_be_defrozen_through_the_governed_path` (le scénario
  complet, arrêté à l'étape 2), et un cas ajouté à
  `test_legacy_baseline_must_be_declared_by_a_recorded_decision_in_current_history`. 149 essais.
- Documentation : `project_control/README.md` (ancrage, retrait et déplacement, projet antérieur à
  la règle, répétition de la montée), `ADOPTION.md` (section « Histoire figée »).
- Manifeste régénéré (`skeleton_version` `3.18.0`), démo et transcript régénérés.
- Non fait : push, release, Alpha (deux décisions de confirmation, un chantier de
  citation, puis la montée — sous leur propre double arrêt), quatrième passe de contrôle.

## 2026-09-11 — `claude/v3.17.1-essai-gitignore-deterministe` — l'essai ne mesure que ce qu'il annonce

- Mandat : `TPL-D-054`. Double arrêt : `STOP 1` posé (dossier, action, alternative) → « Confirmé :
  correction de l'essai et 3.17.1 dans ~/Projets/Squelette V3 -runtime-proof, pas de
  push. » ; `STOP 2` (périmètre exact reformulé) → « Confirmé : branche
  claude/v3.17.1-essai-gitignore-deterministe dans ~/Projets/Squelette V3
  -runtime-proof, pas de push. »
- Baseline : `main` à `8083f31` (`v3.17.0` = `2c58aac`, plus la vue régénérée).
- Trouvé par : la montée d'Alpha vers la `3.17.0` (`WI-064`, bloqué par `HD-072`).
- **L'essai du `.gitignore` manquant dépendait de ce qui traînait à côté.** La copie d'essai est
  faite du dossier de travail tel qu'il est, fichiers ignorés compris — les 27 fichiers du dossier
  `Claude outputs/`, la vue HTML générée. En retirant `.gitignore`, l'essai les rendait tous visibles
  et le contrôleur les refusait (`BOOTSTRAP_CHANGE_SCOPE`) ; puis le `.gitignore` minimal que l'essai
  réécrit ne les masquait pas davantage, et l'audit final échouait. Rien de tout cela n'est ce que
  l'essai mesure. Correction dans l'essai seul : avant de retirer `.gitignore`, il **efface de sa
  propre copie temporaire** les fichiers que le projet ignore (`git ls-files --others --ignored`),
  puis vérifie en plus que le refus ne cite **que** le fichier manquant (`MANDATORY_FILES` présent,
  `BOOTSTRAP_CHANGE_SCOPE` absent). Aucune ligne du contrôleur ne change.
- Vérifié dans les deux sens : rouge avant la correction (reproduit, 27 chemins refusés hors
  périmètre) ; vert après ; et **rouge à nouveau** si l'on retire `.gitignore` de `REQUIRED_FILES`
  dans une copie jetable du produit — l'essai garde bien ce qu'il annonce garder.
- 144 essais OK, en deux lots de 72 (limite de durée de l'outil, pas du produit).
- Manifeste régénéré (`skeleton_version` `3.17.1`), démo et transcript régénérés.
- Commit passé sous `PROJECT_CONTROL_HOOK_OVERRIDE="TPL-D-054"` : le squelette est lui-même en mode
  amorçage, et son garde-fou refuse tout commit qui touche aux essais ou au core hors des chemins
  d'amorçage — c'est sa règle, pas un défaut. Le mandat est celui de la double confirmation ; il est
  imprimé dans le rapport du commit.
- **Dette notée, non traitée** : la cause profonde est dans la fabrique des copies d'essai
  (`make_copy`), qui emporte les fichiers ignorés du dossier de travail ; `stage_explicit_files` la
  contourne déjà en les écartant du `git add`. Nettoyer à la racine toucherait les 121 copies
  d'essai. Aucun autre essai n'a démontré d'échec à cause de cela : pas de redline sans scénario
  d'échec démontré. Candidat pour un chantier, pas pour un correctif.
- Non fait : push, release, montée d'Alpha (reprise de `WI-064` à faire par la voie
  normale, avec une nouvelle décision qui constate la condition de reprise).

## 2026-09-10 — `claude/v3.17-histoire-et-concurrence` — les records s'écrivent un à la fois, et un projet ne naît pas amputé

- Mandat : `TPL-D-051`. Double arrêt : `STOP 1` posé (dossier, action, alternative : deux fiches de
  cadrage et rien d'écrit) → « ok » ; `STOP 2` (périmètre exact reformulé) → « Confirmé : branche
  claude/v3.17-histoire-et-concurrence dans ~/Projets/Squelette V3 -runtime-proof,
  main intouché, pas de push. »
- Baseline : `main` à `98c186b` (`v3.16.2` = `f3c1f57`, plus la vue régénérée).
- Rapport de contrôle rapatrié : `provenance/maintenance/2026-09-10-controle-independant-3.16.2.md`.
- **`F-09` — deux sessions qui écrivent en même temps.** Sans aucun trucage, deux `create-work-item`
  lancés ensemble échouaient tous les deux en laissant la roadmap et le registre citer un Work Item
  dont le record n'existait plus ; et avec un peu de timing, l'annulation de l'une restaurait des
  fichiers dans l'état d'avant le travail que l'autre venait de committer. Deux causes, deux
  corrections. **Le verrou** : ces commandes lisent les registres, calculent l'état suivant et le
  réécrivent ; un verrou pris au moment d'écrire laisse la lecture dehors, là où les deux sessions
  se perdaient. Il est donc pris **avant la première lecture**, tenu pour toute la commande, et
  déposé dans le dossier Git commun — partagé par tous les checkouts du dépôt, hors de l'arbre de
  travail, donc invisible d'un commit et de la traçabilité. Réentrant dans un même processus, il ne
  se bloque pas sur lui-même ; une commande en lecture seule ne le prend jamais et n'attend donc
  jamais derrière un écrivain. **L'annulation** : elle ne remet plus aveuglément les octets pris au
  départ. Un fichier qui ne porte plus ce que cette transaction y a écrit n'est pas à elle : elle le
  laisse et le nomme, plutôt que d'effacer le travail enregistré par quelqu'un d'autre.
- **`F-10` — un projet peut naître amputé.** Le squelette a **un** fichier suivi dont le nom commence
  par un point, `.gitignore`, qu'un gestionnaire de fichiers ne montre pas et n'emporte donc pas.
  Sans lui, l'initialisation ne se contentait pas de passer : elle **se terminait avec succès**, et
  le projet cassait ensuite — la première vue générée écrivait une page HTML que rien n'ignorait, et
  l'audit suivant devenait négatif. Il devient un fichier obligatoire, refusé par l'audit là où un
  nouveau venu lit encore les instructions, autorisé pendant l'initialisation au lieu d'y être
  interdit, et amorcé par `--seed-required` à la montée de version. La documentation donne la
  commande d'export (`git archive`) au lieu de décrire l'intention : c'est elle qui emporte les
  fichiers cachés.
- Trois essais, tous rouges sur la `3.16.2` et verts ici, dont un qui **lance vraiment deux processus
  en parallèle** : `test_two_transactions_at_once_are_serialised_and_leave_a_coherent_state`,
  `test_a_rollback_never_undoes_what_another_session_committed`,
  `test_a_project_without_its_gitignore_is_refused_before_it_breaks`. 144 essais au total.
- Manifeste régénéré (`skeleton_version` `3.17.0`), démo et transcript régénérés.
- **Reste ouvert : `F-08`**, l'histoire figée qui peut être défigée. Un chantier légitimement
  autorisé à écrire l'état du projet retire la baseline, on modifie une clôture ancienne, puis on
  redéclare la baseline sur le commit réécrit **avec la même vieille décision** — le tout par la voie
  normale, sans dérogation ni réécriture de l'historique Git. Le contrôleur vérifie que la baseline
  pointe sur un commit existant et qu'une décision structurée l'accompagne ; il ne vérifie jamais que
  cette décision-là parle de cette baseline-là. Fiche de cadrage livrée séparément.

## Décisions du Project Owner — 2026-09-10 (suite 9)

- `TPL-D-049` — **Promotion.** `claude/v3.16.2-passager-de-fusion` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.16.2` (`skeleton_version` `3.16.2`,
  première version où **les cinq constats de la seconde passe de contrôle indépendant sont tous
  traités** et où le chantier `P16` est clos — `TPL-D-047`). Décision « Je promeus » (2026-09-10).
  Livraison en deux commits (`8674676` correctif, `504bd92` vue), 141 essais OK dans le template et
  141 OK (9 ignorés) sur une copie d'Alpha montée en `3.16.2`, `audit`,
  `bootstrap-audit`, traçabilité et `demo.py --check` PASS. Le tag est posé sur le commit qui
  enregistre cette décision ; la vue est régénérée ensuite et committée à part : `main` est un commit
  devant `v3.16.2`. Envoi vers `origin` et `nas` et release GitHub : gestes du Project Owner
  (`TPL-D-004`).
- `TPL-D-050` — **Un état manquant au tableau des chantiers, à ajouter proprement.** La clôture de
  `P15` a révélé que le schéma de la roadmap du template n'a pas d'état pour un chantier **clos sans
  avoir été ouvert** : `DONE`, `PARTIAL`, `IN_PROGRESS`, `SCOPED`, `TO_SCOPE`, `LATER`. `P15` a donc
  été inscrit `DONE` avec un résumé qui dit ce qui s'est réellement passé, plutôt que d'élargir le
  schéma du core hors du périmètre confirmé. Décision : « On ajoutera l'état proprement » —
  l'ajouter dans une version suivante, avec sa migration et son essai, et remettre `P15` dans le bon
  état à ce moment-là. Jusque-là, le résumé porte la vérité que l'étiquette ne dit pas.

## Décisions du Project Owner — 2026-09-10 (suite 8)

- `TPL-D-047` — **Le passager de fusion, et une estimation fausse corrigée (3.16.2).** La fiche `P16`
  annonçait pour le lot C une refonte de la classification des chemins, « le passage obligé de chaque
  commit », avec un risque de régression important — d'où la décision de le garder pour sa propre
  version. La mesure faite ensuite dans l'atelier a montré que c'était faux : la cause tient en une
  ligne, le correctif en un mot, et rien d'autre n'est touché. L'estimation avait été écrite depuis
  le rapport de contrôle et l'architecture générale, sans ouvrir la fonction fautive. Décision : « Ok
  on s'occupe de la C ! » (2026-09-10), livrer maintenant plutôt que de laisser un trou connu ouvert
  le temps d'un chantier qui n'a plus lieu d'être, et corriger la fiche dans le même mouvement pour
  qu'elle ne conserve pas une estimation démentie. La promotion reste une décision séparée.
- `TPL-D-048` — **Chantier `P15` « Amorçage outillé » clos sans être ouvert.** « on a déjà clôturé
  l'affaire. C est une mauvaise lecture de ta part. C est aller très vite en réalité ! »
  (2026-09-10). La fiche lisait les six minutes d'initialisation du second projet réel comme une
  douleur d'adoption ; ce sont du temps machine et du travail de l'agent, pas le temps du Project
  Owner, qui avait déjà qualifié cet essai de « totalement réussi ». Ce qui manquait vraiment a été
  livré en `3.15.0` — modèles copiables, refus qui nomment le format, mandat écrit dans
  `FIRST_START.md`, porte d'entrée d'un projet neuf dans `ADOPTION.md`. La commande d'amorçage n'est
  pas nécessaire ; la route B du mur de sortie reste écartée. La fiche est conservée avec sa mesure
  et sa lecture corrigée.

## 2026-09-10 — `claude/v3.16.2-passager-de-fusion` — ce que le commit emporte, c'est l'index

- Mandat : `TPL-D-047`. Double arrêt : `STOP 1` posé (dossier, action, alternative : laisser le trou
  ouvert jusqu'à un chantier plus large) → « Ok on s'occupe de la C ! » ; `STOP 2` (périmètre exact
  reformulé) → « Confirmé : branche claude/v3.16.2-passager-de-fusion dans ~/Projets/
  Squelette V3 -runtime-proof, main intouché, pas de push. »
- Baseline : `main` à `6880fa0` (`v3.16.1` = `d3d5c89`, plus la vue régénérée).
- **`F-T05-03` — le passager de fusion.** Pendant une fusion, les deux règles de branche sont
  volontairement mises de côté — une intégration n'est pas du développement — et tout le poids
  repose sur une seule vérification : *cette fusion n'apporte-t-elle que ce que sa branche a
  changé ?* Pour y répondre, elle comparait `HEAD` **au dossier de travail**. Or le commit emporte
  **l'index**. Un fichier hors périmètre mis à l'index puis effacé du disque disparaissait de la
  comparaison — absent de `HEAD`, absent du disque — tout en restant dans ce que le commit allait
  écrire ; la fusion était enregistrée et l'audit d'après était propre. La vérification lit
  désormais l'index (`diff --cached`). Effet de bord voulu : un fichier modifié sur le disque mais
  non indexé n'est plus signalé par cette vérification pendant une fusion — le commit ne l'emporte
  pas, et l'audit du dossier de travail continue de le voir de son côté.
- Un essai, rouge sur la `3.16.1` et vert ici, avec un vrai `git commit` de fusion :
  `test_a_merge_passenger_hidden_from_the_disk_is_still_refused`. L'essai voisin, qui refuse le même
  passager tant qu'il est visible sur le disque, reste vert : les deux cas sont couverts.
- **Les cinq constats de la seconde passe de contrôle sont désormais traités**, et le chantier `P16`
  est clos. Reste, comme prévu, une troisième passe de contrôle.
- Fiche `P16` corrigée : elle portait pour le lot C une estimation démentie par la mesure, et la
  raison de l'erreur y est écrite. Fiche `P15` close sans avoir été ouverte (`TPL-D-048`).
- Manifeste régénéré (`skeleton_version` `3.16.2`), démo et transcript régénérés. Vérifié sur une
  copie d'Alpha montée avec ce correctif.

## Décisions du Project Owner — 2026-09-10 (suite 7)

- `TPL-D-046` — **Promotion.** `claude/v3.16.1-garde-fou-lots-a-b` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.16.1` (`skeleton_version` `3.16.1`,
  première version où le garde-fou de commit est installé là où Git le cherche vraiment, et où un
  état indexé illisible est refusé au lieu d'être accepté sur le seul audit du disque —
  `TPL-D-045`). Décision « promouvoir » (2026-09-10). Livraison en deux commits (`04d3d6b`
  correctif, `2d94e0f` vue), 140 essais OK dans le template et 140 OK (9 ignorés) sur une copie de
  Alpha montée en `3.16.1`, `audit`, `bootstrap-audit`, traçabilité et
  `demo.py --check` PASS. Les deux essais des lots A et B tournent avec de vrais `git commit` dans
  de vrais worktrees liés. Le tag est posé sur le commit qui enregistre cette décision ; la vue est
  régénérée ensuite et committée à part : `main` est un commit devant `v3.16.1`. Envoi vers `origin`
  et `nas` et release GitHub : gestes du Project Owner (`TPL-D-004`). Reste ouvert : le lot C.

## Décisions du Project Owner — 2026-09-10 (suite 6)

- `TPL-D-045` — **Le garde-fou de commit, lots A et B (3.16.1).** La seconde passe de contrôle avait
  démontré trois façons de faire entrer dans l'historique un commit que l'audit aurait refusé. Aucune
  n'est née de la série 3.14–3.16 : elles sont là depuis que le garde-fou existe sous cette forme.
  La fiche de cadrage `P16` a présenté les trois, chacun avec ce qu'il casse, ce que coûterait sa
  correction et ce que la correction risque de casser, plus quatre questions. Décision : « on fait
  dans un ordre professionnel et logique » puis « je suis d'accord » (2026-09-10), sur la proposition
  de livrer **A et B maintenant** — sûrs, courts, sans nouveau comportement — et de garder **C**, le
  passager de fusion, pour sa propre version : le corriger veut dire changer la classification des
  chemins, c'est-à-dire le passage obligé de chaque commit du squelette et de tous ses projets.
  Les trois autres questions tranchées avec : un projet au garde-fou mal installé le découvre par
  l'audit qui le nomme pour ce qu'il est, C-3 garde sa porte mandatée, et la troisième passe de
  contrôle attendra que C soit livré. La promotion reste une décision séparée.

## 2026-09-10 — `claude/v3.16.1-garde-fou-lots-a-b` — le garde-fou est là où Git le cherche, et ce qu'il ne peut pas lire, il le refuse

- Mandat : `TPL-D-045`. Double arrêt : `STOP 1` posé (dossier, action, alternative : attendre que le
  lot C soit tranché d'abord) → « je suis d'accord » ; `STOP 2` (périmètre exact reformulé) →
  « Confirmé : branche claude/v3.16.1-garde-fou-lots-a-b dans ~/Projets/Squelette V3
  -runtime-proof, main intouché, pas de push. »
- Baseline : `main` à `4a3e93b` (`v3.16.0` = `139b813`, plus la vue régénérée).
- Fiche de cadrage déposée : `provenance/maintenance/scopes/p16-scope-garde-fou-de-commit.md`.
- **Lot A (`C-1`) — le garde-fou s'annonçait installé là où Git ne le cherche pas.** Un *worktree
  lié* est une seconde copie de travail du même dépôt ; il a son propre dossier Git, mais Git lit ses
  hooks dans le dossier **commun**. Le contrôleur demandait `rev-parse --git-dir`, qui dans un
  worktree lié répond le dossier du worktree : `install-gate` y écrivait le garde-fou et répondait
  `PASS`, l'audit annonçait « installé », et le vrai `git commit` interdit passait. Deux questions
  posées à Git remplacent la mauvaise : `--git-common-dir` dit **où installer**, `--git-path
  hooks/pre-commit` dit **ce que Git exécutera vraiment** — et cette seconde honore aussi
  `core.hooksPath`, donc elle est vraie dans tous les cas. Si la copie installée n'est pas le fichier
  que Git exécutera, l'état est `NOT_INSTALLED` : c'est la vérité, et une protection qui ment sur sa
  propre présence est pire qu'une protection absente.
- **Lot B (`C-3`) — ce que le garde-fou ne pouvait pas lire, il l'acceptait.** Pour juger ce que le
  commit va vraiment écrire, le garde-fou matérialise l'index en arbre réel. Quand cette création
  était rendue impossible, il retombait sur le seul audit du dossier de travail et l'annonçait dans
  une ligne `PASS` — une garantie qui s'annule au moment où on la gêne, et précisément sur l'état
  qu'elle ne pouvait plus lire. Elle refuse désormais (`STAGED_STATE_AUDITED`), en disant pourquoi et
  en nommant la sortie : `PROJECT_CONTROL_HOOK_OVERRIDE`, pour un environnement qui ne peut
  réellement pas faire de checkout temporaire. C'est ce que `FAIL_CLOSED` veut dire.
- Un essai par lot, rouge sur la `3.16.0` et vert ici, tous deux avec de **vrais** `git commit` :
  `test_the_gate_is_installed_where_git_will_look_even_in_a_linked_worktree` (worktree lié réel,
  commit interdit refusé, `HEAD` inchangé) et `test_a_commit_is_refused_when_the_staged_state_cannot_be_read`
  (instantané rendu impossible sans toucher au garde-fou ni au contrôleur, refus puis passage sous
  mandat).
- Manifeste régénéré (`skeleton_version` `3.16.1`), démo et transcript régénérés. Ligne périmée du
  tableau de bord corrigée : `main` et les tags sont partis sur `origin` et `nas`, seules les
  releases restent.
- **Reste ouvert : le lot C**, le passager de fusion. Un fichier hors périmètre mis à l'index puis
  effacé du disque traverse une fusion sans être vu : le dossier de travail ne l'a plus, et dans
  l'instantané il n'est plus un *changement* mais une part de l'arbre, alors que la vérification de
  traçabilité classe des changements. Le corriger touche le passage obligé de chaque commit ; c'est
  sa propre version, avec sa campagne de non-régression sur des projets réels.

## Décisions du Project Owner — 2026-09-10 (suite 5)

- `TPL-D-044` — **Promotion.** `claude/v3.16-montee-et-preuves` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.16.0` (`skeleton_version` `3.16.0`,
  première version où un projet monte depuis la `3.6.1` par les seules commandes documentées, et où
  un diagnostic d'erreur n'est plus lu comme le verdict d'une campagne — `TPL-D-043`). Décision
  « je prommeux » (2026-09-10). Livraison en deux commits (`f263989` correctif, `fda4620` vue),
  138 essais OK dans le template et 138 OK (9 ignorés) sur une copie d'Alpha montée en
  `3.16.0`, `audit`, `bootstrap-audit`, traçabilité et `demo.py --check` PASS. La preuve décisive
  est ailleurs que dans la suite : la copie d'Alpha remise à son état d'avant la
  montée — vraie `3.6.1`, sans les trois fichiers obligatoires — s'arrête sur `MANDATORY_FILES` en
  visant la `3.15.3` et va jusqu'au bout en visant la `3.16.0`. Le tag est posé sur le commit qui
  enregistre cette décision ; la vue est régénérée ensuite et committée à part : `main` est un
  commit devant `v3.16.0`. Envoi vers `origin` et `nas` et release GitHub : gestes du Project
  Owner (`TPL-D-004`). Restent ouverts, pour un chantier à part : les trois constats du garde-fou
  de commit.

## 2026-09-10 — `claude/v3.16-montee-et-preuves` — un diagnostic n'est pas un verdict, et une montée ne laisse pas le projet sans issue

- Mandat : `TPL-D-043` (« Allons sur B », 2026-09-10). Double arrêt : `STOP 1` posé (dossier,
  action, alternative : une note de cadrage sans écriture) → « go » ; `STOP 2` (périmètre exact
  reformulé) → « Confirmé : branche claude/v3.16-montee-et-preuves dans ~/Projets/
  Squelette V3 -runtime-proof, main intouché, pas de push. »
- Baseline : `main` à `777ef0f` (`v3.15.3` = `ed7494b`, plus la vue régénérée).
- Rapport de contrôle rapatrié : `provenance/maintenance/2026-09-10-controle-independant-3.15.3.md`.
- **`F-07-01` — ma régression de la veille.** La `3.15.3` avait restreint les marqueurs d'échec aux
  seules lignes de verdict, sur une affirmation écrite dans le code : « un programme qui a vraiment
  échoué finit toujours sur une de ces lignes ». C'est faux, et le contrôle l'a démontré : un script
  qui imprime `ERROR: …` puis sort en erreur n'en imprime aucune, et une preuve `PASS` pouvait citer
  cette sortie comme unique pièce. La `3.15.2` refusait exactement ces octets. La règle se lit
  maintenant sur deux niveaux, et c'est le bon découpage depuis le début : un **verdict d'échec**
  (`FAILED`, un résumé pytest qui compte des échecs) tranche quoi que la pièce contienne ; un
  **diagnostic** (`FAIL:`, `ERROR:`, un traceback, un décompte non nul) ne vaut échec que si rien
  dans la pièce n'annonce une réussite. Le diagnostic seul, c'est tout ce qu'un programme mort a eu
  le temps de dire ; le même à côté d'un `OK`, c'est ce qu'imprime un essai qui vérifie qu'une
  entrée invalide est refusée. Corrige au passage le faux positif que le contrôle avait relevé comme
  limite : un `errors=1` dans une ligne de diagnostic, à côté d'un `OK`, ne refuse plus rien. Le
  contrat de `project_control/README.md`, qui décrivait encore la règle d'avant, dit maintenant ce
  que le code fait.
- **`F-T04-01` — la montée documentée ne suffisait pas.** Une version plus récente peut rendre
  obligatoires des fichiers qui appartiennent au projet et que le core ne porte pas — sa liste
  d'idées, ses réglages de vue. Trois règles justes séparément ferment ensemble la porte :
  `template-upgrade` ne touche pas aux records, l'audit exige ces fichiers, et les copier sur la
  branche du chantier est refusé parce que ce sont des records administratifs. Le projet ne peut
  alors ni auditer ni committer. `template-upgrade` les nomme désormais dans son rapport
  (`REQUIRED_FILES`), `--apply` refuse tant qu'ils manquent au lieu de laisser le projet dans cet
  état, et `--seed-required` les écrit — sur la branche canonique et nulle part ailleurs, vierges
  comme le template les tient, jamais par-dessus un fichier existant. La procédure écrite donne
  l'ordre, y compris depuis une version trop ancienne pour connaître la commande : appliquer le
  core d'abord, puis amorcer avec le nouveau contrôleur.
  **C'est le mur rencontré en montant Alpha le 10 septembre, contourné à la main sur
  le moment et jamais corrigé dans le squelette.** Le contrôle l'a retrouvé seul.
- Un essai par correction, rouge sur la `3.15.3` et vert ici :
  `test_the_only_output_of_a_program_that_died_is_not_a_proof_of_success`,
  `test_an_upgrade_names_and_seeds_the_files_the_new_version_requires`. L'essai honnête de la
  `3.15.3` couvre en plus le décompte `errors=` à côté d'un `OK`.
- Manifeste régénéré (`skeleton_version` `3.16.0`), démo et transcript régénérés.
- Vérifié sur un vrai projet : la copie d'Alpha remise à l'état où elle était **avant**
  sa montée — `3.6.1`, sans les trois fichiers — monte jusqu'à la `3.16.0` par les seules commandes
  documentées, audit `PASS` à l'arrivée, sans copie manuelle ni impasse. Le même parcours vers la
  `3.15.3` s'arrête sur `MANDATORY_FILES`.
- Reste ouvert, pour une version suivante : les trois constats du garde-fou de commit.

## Décisions du Project Owner — 2026-09-10 (suite 3)

- `TPL-D-042` — **Promotion.** `claude/v3.15.3-redlines-controle` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.15.3` (`skeleton_version` `3.15.3`,
  première version corrigée des trois lignes rouges du contrôle indépendant de la `3.15.2` —
  `TPL-D-041`). Décision « promeus » (2026-09-10). Livraison en trois commits (`8448747` correctif,
  `e3e3f16` vue, `1d290da` correction d'une ligne inexacte du tableau de bord), 136 essais OK dans
  le template et 136 OK (9 ignorés) sur une copie d'Alpha montée en `3.15.3`, `audit`,
  `bootstrap-audit`, traçabilité et `demo.py --check` PASS. Chaque correction a son essai, rouge sur
  la `3.15.2` et vert ici. Le tag est posé sur le commit qui enregistre cette décision ; la vue est
  régénérée ensuite et committée à part : `main` est un commit devant `v3.15.3`. Envoi vers `origin`
  et `nas` et release GitHub : gestes du Project Owner (`TPL-D-004`). État des envois à cette date :
  `main` et les tags jusqu'à `v3.15.2` sont sur les deux remotes.

## 2026-09-10 — `claude/v3.15.3-redlines-controle` — un statut est ce que le document déclare, une clôture relit son mandat

- Mandat : `TPL-D-041` (« je veux la 3.15.3 », 2026-09-10). Double arrêt : `STOP 1` posé (dossier,
  action, alternative) → « je veux la 3.15.3 » ; `STOP 2` (périmètre exact reformulé) → « Confirmé :
  branche claude/v3.15.3-redlines-controle dans ~/Projets/Squelette V3 -runtime-proof,
  main intouché, pas de push. »
- Baseline : `main` à `3fc2845` (`v3.15.2` = `f0a137e`, plus la vue régénérée).
- Rapport de contrôle rapatrié : `provenance/maintenance/2026-09-10-controle-independant-3.15.2.md`.
- R1 (`F-T03-01`, majeur) — `declared_status()` lit la valeur de la ligne `Status:` du document
  lui-même, et les quatre contrôles de clôture initiale comparent cette valeur au statut attendu au
  lieu de chercher le mot quelque part dans le texte. Une notice qui explique ce que le contrôleur
  attend reste une notice ; un brouillon reste un brouillon. La notice de la charte est reformulée
  pour ne plus porter le jeton `TODO(PROJECT_OWNER)` littéral.
- R2 (`T-02`, majeur) — `close` relit son mandat avant de clore : une clôture faite aujourd'hui
  exige une décision humaine qui autorise aujourd'hui, quoi qu'ait figé la baseline. Et l'exemption
  des décisions figées ne couvre plus que les Work Items **déjà DONE** à cette baseline : la
  baseline fige des clôtures, pas le droit de clore. Un Work Item resté ouvert à l'adoption suit le
  contrat courant à sa prochaine clôture.
- R3 (`F-T01-01`, mineur) — les marqueurs d'échec d'une pièce de preuve se limitent aux lignes de
  verdict (`FAIL` en tête de ligne, `failures=`/`errors=` non nuls, `N failed` d'une ligne de
  résumé). Un `ERROR:` attendu, imprimé par un essai qui vérifie qu'une entrée invalide est
  refusée, ne fait plus d'une preuve `PASS` une preuve refusée.
- Un essai par correction, rouge sur la `3.15.2` et vert sur la `3.15.3` :
  `test_a_note_about_the_expected_status_does_not_validate_a_draft`,
  `test_close_reads_its_mandate_in_full_whatever_the_baseline_froze`,
  `test_a_run_that_passes_while_printing_an_expected_error_is_not_refused`.
- Deux essais de la `3.14.1` sont réécrits sans changer ce qu'ils protègent : leur montage figeait
  une décision au vocabulaire d'époque derrière un Work Item **ouvert**. Sous la règle de R2, c'est
  une clôture d'aujourd'hui : le montage passe donc le Work Item par sa clôture avant la baseline,
  ce que fait un projet réel qui adopte le contrôleur (helper
  `create_start_and_close_lifecycle_work_item`).
- Manifeste régénéré (`skeleton_version` `3.15.3`), démo et transcript régénérés.
- Vérifié des deux côtés : suite verte dans le template, et suite verte sur une copie de
  Alpha montée en `3.15.3`.

## 2026-09-10 — `claude/v3.15.2-essai-garde` — l'essai de la vue héritée passe son tour

- Mandat : `TPL-D-039` (« ok A pour le squelette et Alpha ! », 2026-09-10).
  Double arrêt : `STOP 1` posé (dossier, action, alternative : écrire l'exception dans la condition
  de clôture d'Alpha) → « ok A pour le squelette et Alpha ! » ; `STOP 2` (périmètre exact reformulé) →
  « Confirmé : branche claude/v3.15.2-essai-garde dans ~/Projets/Squelette V3
  -runtime-proof, main intouché, pas de push. »
- Baseline : `main` à `c4e1127` (`v3.15.1` = `49bdb1d`, plus la vue régénérée).
- `test_an_idea_is_not_a_work_item_and_an_inherited_view_is_not_stale` porte désormais
  `skip_unless_template()`, comme les quatre essais que la `3.14.1` avait gardés. Il lit une copie
  de l'arbre courant et la vue que cette copie hérite : dans un projet dérivé, cette vue n'existe
  pas encore, et la question n'a pas d'objet. Manifeste régénéré (`skeleton_version` `3.15.2`),
  démo et transcript régénérés.
- Vérifié des deux côtés : suite verte dans le template, et suite verte dans la copie de
  Alpha montée en 3.15.2.
- Rappel de méthode, valable au-delà de cet essai : un essai qui lit un fichier propre au template
  — sa roadmap, sa vue générée, son exemple — se garde. Les quatre premiers l'ont appris à la
  `3.14.1`, celui-ci à la `3.15.2` ; la règle est écrite dans la docstring de
  `running_in_the_template()`.

## Décisions du Project Owner — 2026-09-09 (suite 15)

- `TPL-D-038` — **Promotion.** `claude/v3.15.1-preuve-honnete` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.15.1` (`skeleton_version` `3.15.1`,
  première version où une preuve `PASS` peut porter le journal d'une campagne ratée à côté de ce qui
  a réussi, et n'est refusée que si toutes ses pièces lisibles rapportent un échec — `TPL-D-037`,
  faux positif révélé par la répétition de la montée d'Alpha sur la preuve de
  `WI-060`). Décision « je promeus » (2026-09-09), après le double arrêt du portage (« on suis ton
  idée ! », puis « Si c'est une approche pro et methodique qui ne génere pas de contre coup :
  Confirmé : branche claude/v3.15.1-preuve-honnete dans ~/Projets/Squelette V3
  -runtime-proof, main intouché, pas de push. »). Livraison en deux commits (`adea60e` correctif,
  `1ad3ea6` vue), 133 tests OK sur le poste du Project Owner, `audit`, `bootstrap-audit`,
  traçabilité et `demo.py --check` PASS, et l'audit de la copie d'Alpha rendu `PASS`
  par le seul remplacement du core. Le tag est posé sur le commit qui enregistre cette décision ;
  la vue est régénérée ensuite et committée à part : `main` est un commit devant `v3.15.1`.
  Push `origin` et `nas`, release GitHub : gestes du Project Owner.

## Décisions du Project Owner — 2026-09-09 (suite 14)

- `TPL-D-037` — **Une preuve peut garder la campagne ratée à côté de celle qui a réussi (3.15.1).**
  La répétition de la montée d'Alpha vers la `3.15.0`, jouée sur une copie jetable
  vingt minutes après la promotion, s'arrête sur le contrôle introduit la veille au soir. Le
  coupable est un chantier réel de ce projet, `WI-060`, clos le 5 septembre : sa preuve de tests
  groupe dix pièces, dont le journal d'une première campagne qui avait échoué sur des verrous de
  fichiers (`FAILED (errors=4)`) et le journal de la reprise isolée où les trente-trois cas
  passent (`OK`). Le résumé de la preuve le dit explicitement. Autrement dit, le contrôle refusait
  exactement la conduite que la doctrine demande : garder la campagne ratée visible plutôt que la
  cacher. Le Project Owner a demandé si l'on ne pouvait pas suspendre le contrôle et le remettre
  ensuite ; la réponse retenue est non — une règle fausse remise plus tard reste fausse, et Alpha
  aurait dû monter deux fois. Décision : corriger tout de suite, en gardant la modification
  minuscule et en la vérifiant sur les données réelles du projet, « Si c'est une approche pro et
  methodique qui ne génere pas de contre coup » (2026-09-09). La promotion reste une décision
  séparée.

## 2026-09-09 — `claude/v3.15.1-preuve-honnete` — la campagne ratée garde sa place

- Mandat : `TPL-D-037` (« on suis ton idée ! », 2026-09-09), sur le blocage rencontré par la
  répétition de la montée d'Alpha.
  Double arrêt : `STOP 1` posé (dossier cible, actions, alternative) → « on suis ton idée ! » ;
  `STOP 2` (périmètre exact reformulé) → « Confirmé : branche claude/v3.15.1-preuve-honnete dans
  ~/Projets/Squelette V3 -runtime-proof, main intouché, pas de push. »
- Baseline : `main` à `cd80ce5` (`v3.15.0` = `711c981`, plus la vue régénérée).
- **Le contrôle punissait l'honnêteté.** Il refusait une preuve `PASS` dès qu'**une** de ses pièces
  rapportait un échec. Il ne refuse plus que la preuve dont **toutes** les pièces lisibles en
  rapportent un — le cas de l'auteur qui recopie une sortie sans la lire, seul cas où une preuve se
  contredit vraiment. Une preuve peut donc porter le journal d'une campagne ratée à côté de ce qui a
  réussi, ce que la doctrine demandait déjà par ailleurs. Les pièces binaires ne sont pas lues et ne
  témoignent de rien, ni dans un sens ni dans l'autre. Le refus nomme désormais toutes les pièces
  qu'il a lues, avec la ligne retenue pour chacune.
- Vérification sur le cas réel qui a servi de révélateur : sur la copie d'Alpha
  arrêtée au blocage, le seul remplacement du core par celui de la `3.15.1` rend `audit` `PASS`, le
  lot de dix pièces de `WI-060` étant accepté avec sa campagne ratée intacte.
- Tests : un nouveau (133 au total), rouge sur la `3.15.0` et vert sur la `3.15.1` — un lot de deux
  pièces, l'une rouge et l'autre verte, clôture acceptée, et le journal rouge vérifié inchangé après
  la clôture. L'essai de la `3.15.0` — une preuve dont l'unique pièce est rouge reste refusée — est
  conservé tel quel ; seule la phrase du refus qu'il vérifie a changé. Manifeste régénéré
  (`skeleton_version` `3.15.1`), démo et transcript régénérés.
- Ce que cette version ne prétend pas : elle n'attrape pas un auteur décidé, qui joindra la pièce
  qu'il veut. La limite est écrite dans la doctrine depuis la `3.15.0` et le reste.

## Décisions du Project Owner — 2026-09-09 (suite 13)

- `TPL-D-036` — **Promotion.** `claude/v3.15-preuves-et-accueil` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.15.0` (`skeleton_version` `3.15.0`,
  première version où une preuve qui annonce `PASS` est refusée quand un artefact qu'elle cite
  rapporte un échec, où les modèles écrits dans les documents sont le texte que le contrôleur
  accepte, où les refus nomment le format qu'ils attendent, où `FIRST_START` porte le mandat qui
  autorise le commit qu'il réclame, et où une vue générée dans un autre arbre n'est plus dite
  périmée — `TPL-D-035`, constats `C-1` à `C-7` de la note de test du second projet réel).
  Décision « promouvoir » (2026-09-09), après le double arrêt du portage (« Je penche pour A
  maintenant, B dans le chantier d'amorçage », puis « Confirmé : branche
  claude/v3.15-preuves-et-accueil dans ~/Projets/Squelette V3 -runtime-proof, main
  intouché, pas de push. »). Livraison en trois commits (`b8fb4d2` correctifs, `d65ffc8` vue,
  `75b9e20` transcript régénéré sur le dépôt), 132 tests OK sur le poste du Project Owner, `audit`,
  `bootstrap-audit`, traçabilité et `demo.py --check` PASS. Le tag est posé sur le commit qui
  enregistre cette décision ; la vue est régénérée ensuite et committée à part : `main` est un
  commit devant `v3.15.0`. Le chantier `P15` — l'amorçage outillé — est ouvert et fiché, non cadré.
  Push `origin` et `nas`, release GitHub : gestes du Project Owner.

## Décisions du Project Owner — 2026-09-09 (suite 12)

- `TPL-D-035` — **Ce que le squelette prouve et ce qu'il dit en accueillant (3.15.0).** Un second
  projet réel — « Coût moyen crypto », calculateur de prix de revient moyen — a été mené de bout en
  bout sur le squelette `3.14.0` : projet **neuf**, né gouverné, sur une machine vierge, ce qui
  éprouve pour la première fois l'autre chemin d'adoption qu'Alpha. Vingt minutes,
  trois Work Items clos et prouvés, audit `PASS`. Le cœur a tenu sans exception : écriture hors
  périmètre refusée deux fois, démarrage sans preuve de lecture refusé, commit sur la canonique
  refusé, réécriture d'une preuve refusée. Sept constats, dont un que ni la revue de robustesse ni
  la seconde revue n'avaient trouvé : **une preuve peut affirmer le contraire de son artefact**, et
  le contrôleur rend `DONE`. Décision du Project Owner (2026-09-09) : corriger, « vas y ! », en un
  seul chantier `3.15.0` couvrant les six constats restants ; pour le mur de sortie de
  l'initialisation, « je penche pour A maintenant, B dans le chantier d'amorçage » — écrire le
  mandat manquant dans `FIRST_START.md` plutôt que desserrer le garde-fou, ce qui sera repris quand
  l'amorçage sera outillé. La commande d'amorçage elle-même reste hors de cette version : c'est un
  chantier, pas un correctif. La promotion reste une décision séparée.

## 2026-09-09 — `claude/v3.15-preuves-et-accueil` — une preuve ne contredit pas sa pièce, et l'accueil dit ce qu'il attend

- Mandat : `TPL-D-035` (« vas y ! », 2026-09-09), sur la note de test du second projet réel,
  rapatriée sous `provenance/maintenance/2026-09-09-note-de-test-second-projet-reel-3.14.0.md`.
  Fiche du chantier ouvert par elle : `provenance/maintenance/scopes/p15-scope-amorcage-outille.md`.
  Double arrêt : `STOP 1` posé (dossier cible, actions, ce qu'elles modifieraient, alternative) →
  « Je penche pour A maintenant, B dans le chantier d'amorçage » ; `STOP 2` (périmètre exact
  reformulé) → « Confirmé : branche claude/v3.15-preuves-et-accueil dans
  ~/Projets/Squelette V3 -runtime-proof, main intouché, pas de push. »
- Baseline : `main` à `9fa6a1f` (`v3.14.1` = `a39c14c`, plus la vue régénérée).
- **`C-3` — une preuve ne peut plus contredire ce qu'elle montre.** Reproduction, refaite ici sur une
  copie neuve : un chantier intégré, une preuve `result: PASS` dont l'artefact se termine par
  `FAILED (failures=1)`, empreinte exacte — la `3.14.1` rendait `DONE`. Le contrôleur lit désormais
  les artefacts texte d'une preuve qui annonce `PASS` et la refuse quand l'un d'eux rapporte un
  échec : ligne commençant par `FAILED`, `FAIL:`, `ERROR:` ou `Traceback (most recent call last):`,
  décompte `failures=` ou `errors=` non nul, résumé pytest annonçant des échecs. Le refus cite la
  ligne entière qu'il a lue. Ce contrôle n'exécute rien et ne juge pas la campagne — le contrôleur
  ne connaît pas la commande de test d'un projet et ne la connaîtra pas : il ferme l'écart entre ce
  qu'une preuve affirme et ce qu'elle donne à lire, c'est-à-dire le cas de l'auteur qui recopie une
  sortie sans la lire. Une campagne échouée s'enregistre comme sa propre preuve avec `result: FAIL`,
  que l'historique conserve. Doctrine dans `AGENTS.core.md` et `project_control/README.md`.
- **`C-1` — les modèles écrits dans les documents sont désormais le texte accepté.** Trois murs,
  tous pendant l'initialisation, tous rencontrés d'affilée. Le modèle de décision humaine montrait
  `HD-NNN` quand le contrôleur cherche le titre `## HD-001` ; celui du registre montrait un bloc de
  texte quand le contrôleur cherche ses deux balises ; les documents disaient « à valider » sans
  jamais donner le mot, `VALIDATED`, qui ne s'apprenait qu'en lisant le code. Les deux modèles sont
  réécrits pour être recopiables tels quels — un second modèle couvre la décision qui sort du
  dossier accordé — et chaque document porte, sous sa ligne `Status`, le mot exact que la clôture
  exige. Les menus (`<choix>`, `A | B | C`) sont retirés des lignes que le contrôleur lit : un
  `<choice>` laissé tel quel s'était retrouvé recopié dans le registre d'un vrai projet. Un essai
  vérifie désormais que chaque bloc « Modèle » passe le parseur du contrôleur.
- **Les refus disent ce qu'ils attendent.** « décision manquante » devient « décision manquante :
  titre `## HD-001` attendu dans `docs/governance/HUMAN_DECISIONS.md` » ; « entrée de registre
  manquante » nomme les deux balises ; les quatre refus de clôture citent la ligne `Status` exacte ;
  l'horodatage d'une preuve donne un exemple complet.
- **`C-2` — le mandat manquant est écrit là où on le cherche.** `FIRST_START.md` demandait de
  committer la transition de clôture et le garde-fou la refusait, la porte de sortie étant
  documentée dans deux autres fichiers. Le point 4 porte désormais le mandat
  (`PROJECT_CONTROL_HOOK_OVERRIDE`) et dit qu'il reste visible dans le rapport du commit. Route A de
  `TPL-D-035` ; la route B — que la gate reconnaisse d'elle-même la transition de clôture — est
  renvoyée au chantier d'amorçage.
- **`C-4` — le format des preuves s'écrit au lieu de s'apprendre en brûlant des chemins.** Le schéma
  porte `format: date-time` sur `recorded_at`, `project_control/README.md` donne un exemple complet
  et directement recopiable, et les deux pièges — le fuseau horaire, l'emplacement des artefacts —
  sont nommés. L'immuabilité d'une preuve reste entière : c'est elle qui condamnait un nom de
  fichier à chaque essai raté.
- **`C-6` — `ADOPTION.md` dit enfin au projet neuf où aller** : exporter l'arbre suivi sans `.git`,
  créer une baseline, installer le garde-fou, confier `FIRST_START.md` à l'agent. Le document
  s'ouvrait sur « ce n'est pas votre cas » sans indiquer de porte.
- **`C-7` — deux petites malhonnêtetés de langage.** Une idée n'est plus annoncée comme un Work Item
  (`IDEA_ID:` au lieu de `WORK_ITEM_ID:`). Une vue générée dans un autre arbre — le cas d'une copie
  qui vient de naître — n'est plus dite « périmée » mais « pas encore la tienne » : le contrôleur
  reconnaît qu'elle a été produite à un commit que ce dépôt n'a pas. Le signal reste exact pour le
  template, dont la vue est bien la sienne.
- `C-5`, le septième constat, était déjà clos par la `3.14.1` : vérifié sur un projet dérivé simulé
  sans le dossier d'exemple, les six essais concernés s'ignorent au lieu de casser.
- Tests : quatre nouveaux (132 au total), chacun vérifié rouge sur la `3.14.1` et vert sur la
  `3.15.0` — la preuve qui contredit sa pièce, les modèles passés au parseur du contrôleur, les
  refus qui nomment leur format, l'idée qui n'est pas un chantier et la vue héritée. Deux essais
  existants ont été ajustés à la nouvelle formulation de la vue. Manifeste régénéré
  (`skeleton_version` `3.15.0`), démo et transcript régénérés.
- Non traité par cette version, volontairement : la commande d'amorçage qui écrirait la première
  décision, le premier record et la première entrée de registre comme `create-work-item` le fait
  ensuite — le vrai correctif de fond, mesuré par le second projet réel : six minutes pour
  l'initialisation écrite à la main, quatre minutes par chantier ensuite.

## Décisions du Project Owner — 2026-09-09 (suite 11)

- `TPL-D-034` — **Promotion.** `claude/v3.14.1-decisions-figees` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.14.1` (`skeleton_version` `3.14.1`,
  première version où une décision humaine enregistrée avant la baseline d'adoption d'un projet, et
  inchangée depuis, est lue dans son propre vocabulaire au lieu d'être requalifiée par une règle
  postérieure, et où les quatre essais qui rejouent le template sur lui-même s'ignorent dans un
  projet dérivé — `TPL-D-033`, défaut découvert en répétant la mise à niveau d'Alpha).
  Décision « promotion » (2026-09-09), après le double arrêt du portage (« 3.14.1 » et « Dans le
  meme mouvement ! », puis « Confirmé : branche claude/v3.14.1-decisions-figees dans
  ~/Projets/Squelette V3 -runtime-proof, main intouché, pas de push. »). Livraison en
  deux commits (`f7dc1e1` correctif, `ad7b49e` vue), 128 tests OK sur le poste du Project Owner,
  `audit`, `bootstrap-audit`, traçabilité et `demo.py --check` PASS. Le tag est posé sur le commit
  qui enregistre cette décision ; la vue est régénérée ensuite et committée à part : `main` est un
  commit devant `v3.14.1`. Push `origin` et `nas`, release GitHub : gestes du Project Owner.

## 2026-09-09 — `claude/v3.14.1-decisions-figees` — les décisions figées gardent leur vocabulaire

- Mandat : `TPL-D-033` (« A », puis « 3.14.1 » et « Dans le meme mouvement ! », 2026-09-09).
  Objet : le refus rencontré par la répétition de la montée d'Alpha, et les quatre
  essais du template qui échouent dans un projet dérivé.
  Double arrêt : `STOP 1` posé (dossier cible, actions, ce qu'elles modifieraient, alternative dans
  le périmètre) → réponse « 3.14.1 » et « Dans le meme mouvement ! » ; `STOP 2` (périmètre exact
  reformulé) → « Confirmé : branche claude/v3.14.1-decisions-figees dans ~/Projets/Squelette V3 -runtime-proof,
  main intouché, pas de push. »
- Baseline : `main` à `b31b4d5` (`v3.14.0` = `7c3226f`, plus la vue régénérée, deux idées et
  l'observation `O-15`).
- **Une règle de forme requalifiait des décisions figées.** Reproduction, sur une copie neuve d'un
  projet gouverné : un Work Item clos, sa décision réécrite dans le vocabulaire d'un autre temps
  (`Chosen option: PILOT_SELECTION = APPROVED for the three listed companies`), le tout figé par une
  baseline d'adoption déclarée — la `3.14.0` refuse l'audit, `SCHEMA_VALIDATION` et
  `INITIALIZATION_STATE` en tête, et le dépôt entier devient immobile. Correctif :
  `frozen_decision_refs()` relit `HUMAN_DECISIONS.md` **au commit de la baseline** et retient les
  décisions dont le bloc n'a pas changé depuis ; pour celles-là seulement, le contrôle
  `Chosen option: AUTHORIZE` n'est pas exigé. Tout le reste leur est demandé comme à n'importe
  quelle décision : `Decision`, `Authorized by`, et les deux confirmations d'un `Folder scope`.
  L'exemption suit l'état et non le nom — une décision réécrite depuis la baseline repasse sous la
  règle courante —, exactement comme la `3.12.0` (`F-10`) l'a fait pour la preuve de lecture des
  Agent Runs. Les blancs autour d'un bloc n'en font pas partie : la dernière décision d'un fichier
  court jusqu'à sa fin, et enregistrer une décision plus tardive ne doit pas révoquer à soi seul
  l'exemption d'une décision antérieure. Aucune transition du jour n'est touchée :
  `create-work-item`, `block`, `resume` et `close` lisent leur mandat en entier, si bien que la
  protection de la `3.10.0` — un refus enregistré ne devient jamais une autorisation — reste
  entière.
- **Quatre essais du template échouaient dans un projet dérivé.** `test_the_view_never_claims_that_tests_passed`,
  `test_plain_style_adds_no_path_of_its_own_outside_the_technical_block`,
  `test_roadmap_view_is_generated_from_the_files_in_a_stable_sourced_form` et
  `test_the_demo_states_the_exact_reach_of_the_proof_of_reading` rejouent le template sur lui-même :
  ils lisent `provenance/ROADMAP_VIEW.md`, `provenance/roadmap-template.v1.json` ou
  `examples/hello-squelette/demo.py`, absents par construction d'un projet dérivé. Mesuré sur
  Alpha monté en `3.14.0` : 118 réussis, 2 ignorés, 4 en échec. Ils s'ignorent
  désormais hors du template (`skip_unless_template`, sur le modèle de l'essai de la démo), et la
  condition de clôture d'un projet peut de nouveau s'écrire « suite verte ».
- Tests : quatre nouveaux (128 au total). Deux vérifiés rouges sur la `3.14.0` et verts sur la
  `3.14.1` — la décision figée gardée dans son vocabulaire, la décision réécrite qui perd son
  exemption. Un troisième est vert sur les deux versions : c'est un garde-fou, il vérifie qu'une
  décision enregistrée **après** la baseline exige toujours `AUTHORIZE`, donc que l'exemption ne
  fuit pas. Le quatrième est rouge sur la `3.14.0` : il rejoue les quatre essais ci-dessus dans une
  copie déclarée `PROJECT` et exige qu'ils s'ignorent. Manifeste régénéré (`skeleton_version`
  `3.14.1`), démo et transcript régénérés.
- Vérification sur le cas réel : sur une copie d'Alpha arrêtée au blocage, le seul
  remplacement du core par celui de la `3.14.1` rend `audit` `PASS` et `status` complet
  (`Squelette : 3.14.1 | core aligné`, `Retour au Project Owner : simple (PLAIN)`,
  `Langue : français (FR)`, garde-fou hors de l'arbre) — sans qu'aucune décision du projet ait été
  modifiée.

## 2026-09-09 — `claude/v3.14-preuves` — ce que le squelette accepte comme preuve (P13, seconde revue)

- Mandat : `TPL-D-031` (« go 3.14.0 », 2026-09-09). Objet : les sept constats de
  `REVUE_SQUELETTE_3.13.0.md`, contre-vérifiés dans `claude/contre-revue-3.13.0.md`, plus le
  constat que cette contre-vérification a fait apparaître.
  Double arrêt : <<CONFIRMATIONS>>
- Baseline : `main` à `2a39786` (`v3.13.0` = `ad95129`, plus la vue régénérée).
- **Le garde-fou jugeait le dossier de travail, pas ce qui allait être enregistré.** Reproduction :
  un record de gouvernance falsifié (`WI-999`, chantier fantôme marqué `DONE`) indexé, puis le
  fichier sain remis dans le dossier — le garde-fou répondait `PASS: MODE_AUDIT — audit PASS on the
  staged state` et le commit entrait dans l'historique. Correctif : `staged_worktree` matérialise
  l'index en arbre réel (`write-tree`, `commit-tree`, `worktree add` détaché) et l'audite là ; le
  résultat s'ajoute à l'audit du dossier de travail, sans le remplacer. Les deux sont nécessaires et
  aucun ne remplace l'autre : les vérifications qui portent sur les **changements en attente**
  (autorisation métier, traçabilité Git, merge en cours) n'ont de sens que dans le dépôt vivant, où
  ces changements existent ; celles qui portent sur le **contenu** (records, schémas, cohérence
  roadmap/fiches, manifeste) doivent juger ce que le commit emporte. Un échec de l'un ou de l'autre
  refuse le commit, et le message dit désormais lequel des deux a été audité. Détail d'exécution qui
  a coûté une itération : dans un hook de commit, Git exporte `GIT_INDEX_FILE` et en tient le
  verrou ; `worktree add` doit être lancé sans lui, faute de quoi il échoue et l'on retombe
  silencieusement sur l'ancien comportement.
- **La création laissait l'index à moitié fait** (`F-01`). Avec un `.gitignore` large — `*.json`,
  cas banal —, `git add` échouait après avoir indexé les fichiers suivis, la restauration ne
  couvrait que les fichiers, et le garde-fou acceptait ensuite de committer une roadmap citant un
  chantier dont la fiche était absente. Correctif : les records administratifs sont indexés avec
  `-f` — ce sont ceux du contrôleur, le `.gitignore` d'un projet ne les cache pas — et l'index est
  restauré comme les fichiers en cas d'échec.
- **N'importe quel vieux commit valait preuve de développement** (`F-02`). Le contrôleur vérifiait
  l'existence du commit et son ascendance de `HEAD`, et rien d'autre : le **commit initial du
  dépôt** clôturait un chantier en `DEVELOPED`, `DONE`, audit `PASS`. Correctif : un commit cité
  doit être un descendant du `start_head` du chantier et toucher au moins un de ses
  `authorized_paths`. Ce n'est pas juger le code, c'est vérifier le lien.
- Cinq mineurs, tous confirmés : `F-04` la ligne des sauvegardes testait le préfixe d'un libellé
  traduit, si bien qu'une sauvegarde à jour s'affichait en alerte en anglais — le booléen exact
  existait déjà deux lignes plus haut ; `F-05` la doctrine proposait encore un réglage de langue
  devenu sans effet — retiré de la liste, gardé au schéma sans être requis pour ne pas invalider un
  projet déjà monté ; `F-06` la source virtuelle des versions taguées était une chaîne française
  codée en dur — traduite, sa clé d'empreinte inchangée ; `F-07` le README annonçait un contrôleur
  uniquement francophone, ce que sa propre démo contredisait ; `F-03` l'adoption d'un dépôt jamais
  gouverné n'a pas de procédure — la limite est désormais écrite dans `README.md` et en tête
  d'`ADOPTION.md` au lieu d'être découverte à l'usage.
- Tests : cinq nouveaux (124 au total), chacun vérifié rouge sur la `3.13.0` et vert sur la
  `3.14.0`. Un essai existant a été corrigé : il périmait la vue par une différence accidentelle de
  formatage du fichier de réglages, il la périme maintenant par un vrai changement de source.
  Manifeste régénéré (`skeleton_version` `3.14.0`), transcript de la démo régénéré.
- Observation ouverte, laissée à la décision du Project Owner : `O-15` — **dans le squelette
  lui-même, `idea add` écrit au mauvais endroit.** La commande enregistre dans
  `docs/governance/ideas-state.v1.json` et `docs/governance/IDEAS.md`, les idées d'un *projet* ;
  or la vue du template lit `provenance/roadmap-template.v1.json`, les idées du *template*. Une
  idée enregistrée par la voie documentée n'apparaît donc pas dans le tableau de bord du squelette,
  et sa numérotation repart à `ID-001` alors que la roadmap du template va déjà jusqu'à `ID-022` :
  deux listes, deux numérotations, aucune ne voit l'autre. Constaté le 9 sept. en enregistrant les
  idées `ID-021` et `ID-022` du Project Owner, qui ont dû être écrites à la main. Aucun cas de perte
  de donnée : les deux fichiers restent cohérents entre eux, ce sont les *bons* fichiers qui ne sont
  pas les mêmes selon le rôle du dépôt. Correction attendue : quand le rôle est `PROJECT_TEMPLATE`,
  `idea add` et `idea set` doivent écrire dans la roadmap du template, là où la vue lit.

## Décisions du Project Owner — 2026-09-09 (suite 7)

- `TPL-D-030` — **Promotion.** `claude/v3.13-langue` est promue branche canonique par fast-forward
  de `main` ; la baseline promue reçoit le tag `v3.13.0` (`skeleton_version` `3.13.0`, première
  version où la langue du contrôleur est un choix du Project Owner enregistré dans Project State,
  posé par l'interview `FIRST_START`, exigé pour clore l'initialisation, et respecté par `status`
  et la vue roadmap — `TPL-D-029`, chantier P14 étape 1). Décision « Promouvoir » (2026-09-09),
  après le double arrêt du portage (« tu peux porter ! », refusé comme trop général, puis
  « Confirmé : branche claude/v3.13-langue dans ~/Projets/Squelette V3 -runtime-proof,
  main intouché, pas de push. »). Livraison en deux commits (`fac9c53` version, `0dbd53b` vue),
  119 tests OK sur le poste du Project Owner, `audit`, `bootstrap-audit` et traçabilité PASS. Le tag
  est posé sur le commit qui enregistre cette décision ; la vue est régénérée ensuite et committée à
  part : `main` est un commit devant `v3.13.0`. Push `origin` et `nas`, release GitHub : gestes du
  Project Owner.

## 2026-09-09 — `claude/v3.13-langue` — la langue au choix (P14, étape 1)

- Mandat : `TPL-D-029` (« On attaque p14 », 2026-09-09). Fiche de cadrage :
  `claude/p14-scope-langue-au-choix.md`.
  Double arrêt : <<CONFIRMATIONS>>
- Baseline : `main` à `e5ce40e` (`v3.12.0` = `3e4918e`, plus la vue régénérée).
- Constat de départ, mesuré avant de cadrer : le squelette était déjà bilingue par accident, et pas
  là où on le croyait. Les 180 messages de refus et les ~120 noms et détails de vérifications sont
  **déjà en anglais** ; le français ne vivait que dans `status` (une trentaine de phrases) et la vue
  roadmap (une centaine). Le chantier ne consistait donc pas à « ajouter l'anglais » partout, mais à
  rendre choisissable la seule partie qui s'adresse à un humain.
- Project State porte `language` (`FR` | `EN` | `UNKNOWN`), requis par le schéma, validé comme
  `reporting_style`, exigé `FR` ou `EN` pour `COMPLETE` et pour `bootstrap-closeout`. Nouvelle
  vérification d'audit `LANGUAGE`, calquée sur `REPORTING_STYLE`. Question ajoutée à l'interview
  `FIRST_START`.
- Deux catalogues de messages, un par fichier qui produit de la prose : `SPEECH` dans
  `project_control.py` (`status`, la prochaine action, le modèle de la vue) et `TEXT` dans
  `roadmap_view.py` (titres, colonnes, libellés d'état, pieds de page). Bibliothèque standard
  seulement, comme tout le reste. Les dates, les libellés d'état et l'espace avant le deux-points
  suivent la langue.
- La vue ne traduit jamais les mots du Project Owner : ses citations, résumés et sources sont montrés
  tels qu'il les a écrits. La doctrine (`AGENTS.core.md`, section « Langue ») dit où passe la
  frontière.
- La démo `hello-squelette` choisit désormais l'anglais : le bloc de sortie du README, dernier
  français de la vitrine, est entièrement en anglais.
- Tests : trois nouveaux (119 au total), chacun vérifié rouge sur la `3.12.0` et vert sur la
  `3.13.0` — la langue est choisie par le Project Owner et bloque la clôture tant qu'elle ne l'est
  pas, `status` change de langue quand les noms de vérifications et les refus n'en changent pas, la
  vue suit la langue sans traduire son propriétaire. Manifeste régénéré (`skeleton_version`
  `3.13.0`), transcript de la démo régénéré.
- Non traité par cette version, volontairement : les documents de gouvernance en anglais (étape 2).

## Décisions du Project Owner — 2026-09-09 (suite 5)

- `TPL-D-028` — **Promotion.** `claude/v3.12-robustesse` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.12.0` (`skeleton_version`
  `3.12.0`, première version où une interruption clavier annule une transition comme n'importe
  quelle panne, où une montée de version refuse d'écraser un fichier du projet, où un merge
  d'intégration passe sans pouvoir porter autre chose que ce que sa branche a changé, où
  l'exemption de preuve de lecture suit l'état gelé et non le nom, et où rien n'est écrit avant
  qu'un refus soit écarté — `TPL-D-027`, constats `F-07`, `F-08`, `F-09`, `F-10` et `F-16` de la
  revue de robustesse). Décision « Promouvoir » (2026-09-09), après le double arrêt du portage
  (« Oui je le veut », refusé comme trop général, puis « Confirmé : branche
  claude/v3.12-robustesse dans ~/Projets/Squelette V3 -runtime-proof, main intouché,
  pas de push. »). Livraison en deux commits (`01b847f` correctif, `d235c75` vue), 116 tests OK sur
  le poste du Project Owner, `audit`, `bootstrap-audit` et traçabilité PASS. Le tag est posé sur le
  commit qui enregistre cette décision ; la vue est régénérée ensuite et committée à part : `main`
  est un commit devant `v3.12.0`. **Cette promotion clôt le chantier P13** : les dix-huit constats
  de la revue de robustesse du tag `3.9.0` sont traités, en quatre versions (`3.9.1`, `3.10.0`,
  `3.11.0`, `3.12.0`) et sept décisions (`TPL-D-021` à `TPL-D-028`). Push `origin` et `nas`,
  release GitHub : gestes du Project Owner.

## 2026-09-09 — `claude/v3.12-robustesse` — la robustesse d'exécution (P13, lot C)

- Mandat : `TPL-D-027` (« Ensuite lot C », 2026-09-09). Objet : les constats `F-07`, `F-08`,
  `F-09`, `F-10`, `F-16` de
  `provenance/maintenance/2026-09-08-revue-robustesse-codex-3.9.0.md`, contre-vérifiés dans
  `claude/contre-revue-des-15-constats.md`.
  Double arrêt : <<CONFIRMATIONS>>
- Baseline : `main` à `5fe9680` (`v3.11.0` = `b43acdc`, plus la vue régénérée).
- `F-07` — les douze gestionnaires qui annulent une transition attrapent désormais
  `BaseException` et non `Exception` : `KeyboardInterrupt` n'en dérive pas, si bien qu'un Ctrl-C
  passait au travers sans rien annuler. Reproduction : un `start` interrompu juste après le commit
  des records et la création de la branche laissait, sur la `3.11.0`, `HEAD` avancé, le Work Item
  `IN_PROGRESS` et une branche de travail ; en `3.12.0` tout est rendu à son état d'avant.
- `F-08` — `template-upgrade` classait `UPDATED`, donc à écraser, un fichier du projet situé sur un
  chemin absent de l'ancien manifeste : aucun écart n'était signalé pour lui puisque l'ancien
  manifeste l'ignorait. Reproduction sur une `3.11.0` intacte : `APPLY` réussi, fichier du projet
  remplacé, pas un mot. Nouvel état `PROJECT_FILE`, refusé sans `--overwrite` comme un fichier du
  core modifié localement, avec son propre message. Le message de `--overwrite` inutile devient
  « names no protected file », les deux familles étant désormais protégées.
- `F-09` — un merge en cours n'est plus jugé comme du développement. `BUSINESS_CHANGE_AUTHORIZATION`
  passe la main à `integration_merge_errors`, qui vérifie ce que le merge **intègre** : tout chemin
  que le merge apporte dans l'arbre canonique doit être un chemin que la branche fusionnée a
  elle-même changé depuis la base de fusion. Le merge légitime passe ; un fichier glissé dans le
  commit de merge, que la branche n'a jamais touché, est refusé en étant nommé. La doctrine
  promettait le premier ; elle ne disait rien du second, désormais fermé.
- `F-10` — l'exemption de preuve de lecture suivait le **nom** de l'Agent Run gelé : réécrire le
  contenu d'un enregistrement exempt lui faisait emporter son exemption vers du travail fait
  aujourd'hui. Elle suit maintenant l'**état** : `agent_run_blobs_at` retient l'empreinte du blob à
  la baseline, et seul un fichier resté identique octet pour octet reste exempt. L'audit signale
  ceux qui ont changé et n'ont toujours pas de preuve ; un enregistrement qui a depuis acquis sa
  preuve n'est pas signalé, il n'a simplement plus besoin de l'exemption.
- `F-16` — `write_roadmap_view` décide de tout ce qui peut refuser **avant** d'écrire le premier
  octet. La page n'est plus réécrite par une commande qui finit sur un refus.
- Hors revue — après un `template-upgrade --apply` réussi, le garde-fou installé hors de l'arbre est
  réinstallé depuis la référence mise à jour (`COMMIT_GATE_REINSTALLED`) ; s'il n'était pas installé,
  la commande le dit au lieu de laisser croire que tout est en ordre.
- Tests : cinq nouveaux (116 au total), chacun vérifié rouge sur la `3.11.0` et vert sur la
  `3.12.0`. Manifeste régénéré (`skeleton_version` `3.12.0`), transcript de la démo régénéré.
- Les dix-huit constats de la revue de robustesse sont désormais tous traités ou explicitement
  écartés.

## Décisions du Project Owner — 2026-09-09 (suite 3)

- `TPL-D-026` — **Promotion.** `claude/v3.11-affirmations` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.11.0` (`skeleton_version`
  `3.11.0`, première version où la vue ne déclare plus le résultat d'essais qu'elle n'a pas
  exécutés, où les versions taguées entrent dans son empreinte de fraîcheur, où l'absence des
  marqueurs du README est une dérive, et où la portée de la preuve de lecture est énoncée sans
  la dépasser — `TPL-D-025`, constats `F-11`, `F-12`, `F-14`, `F-17` et `F-18` de la revue de
  robustesse). Décision « promouvoir » (2026-09-09), après le double arrêt du portage
  (« tu peux continuer ! », refusé comme trop général, puis « Confirmé : branche
  claude/v3.11-affirmations dans ~/Projets/Squelette V3 -runtime-proof, main
  intouché, pas de push. »). Livraison en deux commits (`733e5df` correctif, `5840958` vue),
  111 tests OK sur le poste du Project Owner, `audit`, `bootstrap-audit` et traçabilité PASS.
  Le tag est posé sur le commit qui enregistre cette décision ; la vue est régénérée ensuite et
  committée à part : `main` est un commit devant `v3.11.0`. Push `origin` et `nas`, release
  GitHub : gestes du Project Owner.

## 2026-09-09 — `claude/v3.11-affirmations` — ce que le squelette affirme (P13, lot B)

- Mandat : `TPL-D-025` (« le lot B (3.11.0) ! », 2026-09-09). Objet : les constats `F-11`, `F-12`,
  `F-14`, `F-17`, `F-18` de
  `provenance/maintenance/2026-09-08-revue-robustesse-codex-3.9.0.md`, contre-vérifiés dans
  `claude/contre-revue-des-15-constats.md`.
  Double arrêt : <<CONFIRMATIONS>>
- Baseline : `main` à `55357e7` (`v3.10.0` = `a0c9776`, plus la vue régénérée).
- Reproductions préalables, sur une copie neuve de la `3.10.0` : un essai volontairement rouge
  committé, manifeste réaligné, arbre propre — `audit` PASS et la vue annonçant
  « Vérifications : toutes réussies · 107 tests déclarés » alors qu'un essai sur 107 échouait ;
  un tag posé sans que `status` cesse d'annoncer « Vue roadmap : à jour » ; les deux marqueurs du
  README retirés et une ligne du bloc falsifiée, `demo.py --check` répondant « match the
  controller's output » et sortant avec le code 0.
- `F-12` — le contrôleur ne prétend plus rien sur les essais. Le bandeau et la tuile disent
  « les contrôles du dossier passent » (ou échouent) et, séparément, « N essais automatiques
  présents, non exécutés par cette vue » ; la ligne de « Maintenant » suit la même règle.
  `docs/agent-governance/ROADMAP_VIEW.md` (core) gagne une section « Ce que la vue n'affirme pas ».
- `F-11` — `roadmap_view_sources_digest` ajoute une entrée `(versions taguées du dépôt)` :
  l'empreinte des tags que la vue affiche. Poser, déplacer ou supprimer un tag rend la vue
  périmée. Le commit courant et les têtes distantes en restent volontairement exclus, sinon
  committer la vue la périmerait aussitôt, et la repousser après chaque régénération, sans fin ;
  la doctrine le dit.
- `F-17` — `demo.py` : l'absence du bloc `hello-squelette` est une dérive (`--check` échoue en
  la nommant) et `--write` refuse plutôt que d'écrire à moitié. Le contrôle qui garantit la
  première page du README ne peut plus être désactivé en retirant deux commentaires.
- `F-18` — la démo dit ce que la preuve de lecture établit — le travail a démarré depuis le texte
  courant de chaque autorité, et toute modification l'invalide — et ce qu'aucune mécanique ne peut
  établir : qu'un esprit a lu. `AGENTS.core.md` (core) porte le même paragraphe, avec la consigne
  de ne pas promettre davantage.
- `F-14` — la cellule « Fiche » de la table des chantiers est composée par la vue : en style simple
  elle dit « fiche de cadrage dans le dossier » et les chemins passent au repli technique, où ils
  restent tous. La doctrine précise le partage : la vue n'ajoute pas d'identifiant de son cru,
  et ne réécrit pas les mots du Project Owner.
- Tests : cinq nouveaux (111 au total), chacun vérifié rouge sur la `3.10.0` et vert sur la
  `3.11.0` — un tag périme la vue et un commit ordinaire ne la périme pas, aucune sortie n'annonce
  un résultat d'essais, le style simple n'ajoute aucun chemin hors du repli, les marqueurs retirés
  font échouer le contrôle, la démo énonce la portée exacte de la preuve de lecture.
  Manifeste régénéré (`skeleton_version` `3.11.0`), transcript de la démo régénéré.
- Non traités par cette version, volontairement : les constats du lot C (`F-07`, `F-08`, `F-09`,
  `F-10`, `F-16`) et la relance automatique d'`install-gate` après une montée de version.

## Décisions du Project Owner — 2026-09-09 (suite)

- `TPL-D-024` — **Promotion.** `claude/v3.10-autorisations` est promue branche canonique par
  fast-forward de `main` ; la baseline promue reçoit le tag `v3.10.0` (`skeleton_version`
  `3.10.0`, première version où le garde-fou de commit s'exécute depuis une copie installée
  **hors de l'arbre de travail**, où une décision qui enregistre un refus n'autorise rien,
  où un champ vide est une valeur absente et où l'index est lu pour les liens symboliques —
  `TPL-D-023`, constats `F-03` à `F-06` de la revue de robustesse). Décision « promouvoir »
  (2026-09-09), après le double arrêt du portage (« Ok » puis « Confirmé : branche
  claude/v3.10-autorisations dans ~/Projets/Squelette V3 -runtime-proof, main
  intouché, pas de push. »). Livraison en deux commits (`5f83a90` correctif, `2d244b0` vue),
  106 tests OK sur le poste du Project Owner, `audit`, `bootstrap-audit` et traçabilité PASS.
  Le tag est posé sur le commit qui enregistre cette décision ; la vue est régénérée ensuite
  et committée à part : `main` est un commit devant `v3.10.0`. **Après une montée de version,
  chaque dépôt qui utilise le squelette doit rejouer `install-gate`** : la copie installée du
  garde-fou n'est pas mise à jour par `template-upgrade`, et le contrôle `COMMIT_GATE` signale
  l'écart. Push `origin` et `nas`, releases GitHub (3.9.1 puis 3.10.0), About et Topics :
  gestes du Project Owner.

## 2026-09-09 — `claude/v3.10-autorisations` — les autorisations (P13, lot A)

- Mandat : `TPL-D-023` (« Je valide tout », 2026-09-09). Objet : les constats `F-03`,
  `F-04`, `F-05`, `F-06` de
  `provenance/maintenance/2026-09-08-revue-robustesse-codex-3.9.0.md`, contre-vérifiés
  dans `claude/contre-revue-des-15-constats.md`, plus la fermeture de la brèche de la
  gate laissée assumée par la `3.9.1`.
  Double arrêt : <<CONFIRMATIONS>>
- Baseline : `main` à `eb15ef2` (`v3.9.1` = `deb95d7`, plus la vue régénérée).
- `F-03` — `human_decision_errors` lit **toutes** les lignes `Chosen option:` d'une
  décision : dès qu'une seule ne vaut pas `AUTHORIZE`, la décision est refusée comme
  autorisation. Une décision qui enregistre un refus (`REJECT`, `DEFER`) ne peut plus
  servir de mandat à un Work Item.
- `F-04` — les sept expressions qui lisent un champ d'une décision (`Chosen option`,
  `Folder scope`, `Confirmation 1`, `Confirmation 2`, et les champs de portée) exigent
  la valeur **sur la ligne du champ** : `:[ \t]*(\S.*)$` au lieu de `:\s*(\S.*)$`. Un
  champ laissé vide ne capture plus la ligne suivante ; un `Folder scope:` vide suivi
  d'un chemin n'autorise plus ce chemin, et deux confirmations vides ne valent plus
  double arrêt.
- `F-05` — nouvelle lecture de l'index (`git ls-files -s -z`, mode `120000`) : la
  vérification `NO_SYMLINKS` voit les liens **indexés**, y compris ceux effacés de
  l'arbre de travail après avoir été indexés. Ce que le commit emporte est ce qui est
  contrôlé.
- `F-06` — `scopes_for_paths` route aussi les autorités des **enfants** d'un chemin
  autorisé : autoriser `docs/` oblige désormais à lire les autorités de
  `docs/architecture/` et `docs/governance/`. Le devoir de lecture couvre tout ce que
  l'autorisation permet d'écrire.
- Gate de commit hors de l'arbre de travail : nouvelle commande `install-gate` qui copie
  `scripts/hooks/pre-commit` dans `<git-dir>/hooks/pre-commit`, la rend exécutable et
  neutralise un `core.hooksPath` pointant vers l'arbre suivi. Le fichier versionné
  devient la **référence** ; `commit_gate_state()` compare l'installé à la référence et
  rend `INSTALLED`, `IN_TREE`, `MISMATCH` ou `NOT_INSTALLED` ; la vérification d'audit
  `COMMIT_GATE` échoue sur `MISMATCH`. Déplacer ou supprimer le fichier versionné ne
  désarme plus la gate : la copie installée continue de refuser le commit. Limite
  résiduelle, écrite dans la doctrine : une suppression explicite de la copie installée,
  faite au terminal hors du cadre, reste possible — elle est constatée par le contrôle
  suivant (`status`, `audit`) et ne peut pas passer pour un état normal.
- Doctrine et documents alignés : `AGENTS.core.md` (core), `FIRST_START.md`,
  `project_control/README.md`, `README.md`, `CONTRIBUTING.md`, et la démo, qui installe
  la gate par `install-gate`.
- Suite de tests : le montage d'une copie d'essai ne tente plus d'indexer un fichier que le
  projet ignore. Depuis la `3.9.1`, le dossier où l'application dépose les téléchargements
  d'une conversation est ignoré par Git ; dès qu'il contenait un fichier, `git add` le
  refusait et 91 tests échouaient pour une raison étrangère à ce qu'ils vérifient.
- Démo rendue indépendante de l'état du dépôt d'où on la rejoue : la vue roadmap générée
  (`provenance/ROADMAP_VIEW.md`, `provenance/roadmap/`) n'est plus exportée dans la copie,
  puisqu'un projet neuf ne l'hérite pas. La ligne « Vue roadmap » du transcript cessait
  d'être reproductible dès que la vue du dépôt source était périmée, et `--check` signalait
  alors une dérive qui n'en était pas une.
- Tests : cinq nouveaux (106 au total), chacun vérifié rouge sur la `3.9.1` et vert sur la
  `3.10.0` — décision qui enregistre un refus, champ vide, lien symbolique indexé puis
  caché, dossier parent et autorités des enfants, gate qui survit à la suppression de sa
  référence (avec `MISMATCH` et retour au mode `IN_TREE`). Le test existant sur la
  disparition de la gate est réécrit : il documente désormais ce que le mode historique
  `IN_TREE` ne peut pas faire, et renvoie au nouveau. Manifeste régénéré
  (`skeleton_version` `3.10.0`), transcript de la démo régénéré.
- Non traités par cette version, volontairement : les constats des lots B (`F-11`, `F-12`,
  `F-14`, `F-17`, `F-18`) et C (`F-07`, `F-08`, `F-09`, `F-10`, `F-16`).

## 2026-09-08 — `claude/v3.9.1-scope-renames-and-gate` — portée des renommages et gate de commit (P13)

- Mandat : `TPL-D-021` (« prépare la 3.9.1 », 2026-09-08). Objet des correctifs : les
  constats `F-01` et `F-02` de `provenance/maintenance/2026-09-08-revue-robustesse-codex-3.9.0.md`.
  Double arrêt : <<CONFIRMATIONS>>
- Baseline : `main` à `0a90dfc` (`v3.9.0` = `9d78627`, plus la vue régénérée).
- Contre-vérification préalable, indépendante du rapport, sur une copie neuve du tag et
  sur un autre environnement (Linux, Python 3.10, Git 2.34) : les deux `BLOCKER` se
  reproduisent ; une variante non signalée par la revue a été trouvée — déplacer
  `scripts/hooks/pre-commit` retire la gate, et ce commit-là n'est contrôlé par personne.
- `changed_paths` (`scripts/project_control.py`) et `parse_porcelain_z`
  (`scripts/check_git_traceability.py`) classent désormais **l'origine d'un renommage**
  comme sa destination ; une copie, qui laisse son origine intacte, ne compte que par sa
  destination. Le preflight, l'audit et la traçabilité voient donc les deux côtés.
- Nouvelle vérification `WORK_BRANCH_AUTHORIZED_PATHS` dans `commit_gate_findings` :
  sur la branche d'un Work Item, tout chemin indexé non administratif est mesuré contre
  les `authorized_paths` du Work Item `IN_PROGRESS` unique, par la même fonction que le
  preflight (`normal_path_errors`) ; un commit sans Work Item actif unique est refusé.
  Les merges d'intégration et l'override humain explicite restent inchangés ; la branche
  canonique garde `CANONICAL_BRANCH_PROTECTED`.
- `hooks_installed` exige le fichier présent et exécutable, pas seulement la
  configuration : `status` cessait d'être exact dès que Git n'exécutait plus la gate
  (constat `F-13` de la revue).
- `AGENTS.core.md` (core) : trois paragraphes ajoutés dans « Git Safety et traçabilité »
  — le renommage compte des deux côtés, la gate applique la portée du Work Item à tout
  chemin, et la limite assumée de la gate face à sa propre suppression, avec la conduite
  attendue de l'agent (rétablir avant toute écriture, signaler).
- Tests : trois nouveaux (101 au total), chacun vérifié rouge sur la 3.9.0 et vert sur la
  3.9.1 — renommage hors périmètre refusé par le preflight, la gate et la traçabilité ;
  gate qui refuse un chemin hors périmètre hors racines métier, et laisse passer un
  chemin autorisé ; suppression de la gate constatée immédiatement par l'audit et par
  `status`. Manifeste régénéré (`skeleton_version` `3.9.1`), transcript de la démo
  régénéré (la gate affiche une vérification de plus).
- Rapport de la revue et son mandat rapatriés sous `provenance/maintenance/`.
- Non traités par cette version, volontairement : les dix constats `MAJOR` et les cinq
  `MINOR` restants de la revue.

## 2026-09-08 — `claude/v3.9-vitrine-github` — la vitrine GitHub (P10 étape 1)

- Mandat : `TPL-D-019` (2026-09-08) ; scope
  `provenance/maintenance/scopes/p10-scope-publication-vitrine-github.md` (V2 : constat
  sur pièces, version d'essai, observations, plan de livraison ; V3 § 14 : livraison).
  Double arrêt (`TPL-D-011`) : STOP 1 posé le 2026-09-08 (dossier, action, alternative)
  → « Je suis ok » ; STOP 2 (périmètre exact reformulé) → « Confirmé : branche
  claude/v3.9-vitrine-github dans ~/Projets/Squelette V3 -runtime-proof,
  main intouché, pas de push. » Droit de suppression limité aux fichiers temporaires
  de Git.
- Baseline : `main` à `4c93ddf` (`v3.8.0` = `e6f53b0`, plus la vue régénérée).
- README — premier écran en anglais : titre « Squelette », sous-titre « Governance and
  control for AI-assisted projects », signature « Who decides. Who does. What proves
  it's done. », schéma texte, « Why Squelette? » (le contrôleur refuse, il ne conseille
  pas), tableau « Without a frame / with Squelette » (dix lignes, chacune adossée à un
  mécanisme : décision humaine exigée par `create-work-item`, records audités,
  `authorized_paths` + preflight + hook, preuve de lecture, preuves par gate, une branche
  par Work Item, `status`, `reporting_style`, `Folder scope` + deux confirmations), démo
  (bloc généré entre `<!-- hello-squelette:begin -->` / `<!-- hello-squelette:end -->` :
  `status` pendant le chantier, `preflight` refusé hors périmètre, `status` final),
  « Try it », « What it is — and what it is not » ; puis le même premier écran en
  français ; puis la documentation existante inchangée depuis « Commencer ou
  reprendre ». Le README dit que le contrôleur parle français (O-11).
- Exemple — `examples/hello-squelette/demo.py` (bibliothèque standard) rejoue dans un
  dossier temporaire : export de l'arbre suivi sans `.git`, baseline Git, hook ;
  Bootstrap Mode (refus d'un chemin métier, acceptation des chemins d'interview) ;
  Project Owner scripté (Charter, architecture, ADR-0001, HD-001, WI-000, CONV-000,
  roadmap, registre ; style `PLAIN`) ; `bootstrap-closeout` ; transition `COMPLETE`
  committée sous `PROJECT_CONTROL_HOOK_OVERRIDE="HD-001: FIRST_START closeout"` (O-12) ;
  `create-work-item WI-001` (HD-002) ; `context-manifest` ; `start` refusé sans
  empreinte puis accepté ; dérive `modules/billing/invoice.py` refusée par le
  preflight ; `modules/hello/` accepté ; tests ; commit sur la branche ; merge ;
  preuves ; `close --commit` ; `roadmap-view --write` ; `status` ; `audit` ;
  `git log --graph`. `--write` régénère `TRANSCRIPT.md` et le bloc du README ;
  `--check` compare ; `--verbose` garde les lignes `PASS:` ; valeurs volatiles
  normalisées (`<commit>`, `<sha256>`, `<sha>`, `<date>`, `<timestamp>`, `<demo>`,
  `<duration>`) ; suites de `PASS:` repliées en « … N controls PASS … ». La démo refuse
  de tourner hors du template. `examples/hello-squelette/README.md` et `TRANSCRIPT.md`
  (généré).
- Test — `test_hello_squelette_transcript_and_readme_block_match_the_controller`
  (`demo.py --check` ; ignoré hors du template ou sans `python3` sur le PATH). Suite :
  98 tests (97 + 1).
- `CONTRIBUTING.md` (court, bilingue) ; `LICENSE` (MIT, MINET Jeoffrey) — hors core :
  la licence voyage avec toute nouvelle copie, un projet dérivé garde la sienne ;
  `ADOPTION.md` : section « Exemple et documentation du template ».
- Squelette — `provenance/roadmap-template.v1.json` : version 3.9.0, chantier P10
  (`IN_PROGRESS`, fiche), idée ID-019, attente « promouvoir la vitrine », étape « après
  la promotion », entrée du passé ; règle de maintenance ajoutée en tête de ce journal
  (démo régénérée à chaque maintenance, O-14). Manifeste régénéré (`skeleton_version`
  `3.9.0`, 24 fichiers core : `ADOPTION.md` et le fichier de tests changent).
- Observations sans scénario d'échec, laissées à la décision du Project Owner : O-11
  (messages du contrôleur en français), O-12 (la clôture de l'initialisation exige le
  mandat d'override sur la canonique), O-13 (« Vue roadmap : périmée » sur une copie
  neuve avant initialisation, 3.8.0), O-14 (règle de maintenance, appliquée).
- Vérifications : `demo.py --check` vert ; 98 tests OK sur la version d'essai (VM de
  session, Python 3.10) et sur le poste du Project Owner ; `bootstrap-audit` et `audit`
  PASS sur la branche après commit.

## 2026-09-08 — `claude/v3.8-roadmap-in-repo` — la ROADMAP dans le dossier (P12 étape 2, P6)

- Mandat : « je suis ok. avec la suite. On va de l'avant […] Va de l'avant ! »
  (2026-09-08), sur la fiche P12 § 12 ; scope
  `provenance/maintenance/scopes/p12-scope-roadmap-dediee.md`.
- Baseline : `main` à `7964fa4` (`v3.7.0`).
- Idées — `idea add --quote --source [--state] [--stated-at] [--target] [--note]` et
  `idea set ID-NNN [--state] [--target] [--note]` écrivent les deux formes (schéma
  `ideas-state.v1.schema.json`, états fermés `EVOKED` … `DISCARDED`) et, en
  `NORMAL_MODE`, les committent eux-mêmes depuis la branche canonique sur un worktree
  propre (`chore(project-control): idea ID-NNN <état>`, P9-A) ; en `BOOTSTRAP_MODE`
  ils écrivent seulement. Contrôle d'audit `IDEAS` : synchronisation Markdown / JSON,
  identifiants uniques, états admis, cibles existantes (`WI-NNN` dans la roadmap,
  `HD-NNN` enregistrée), `DISCARDED` avec sa cible. Une idée n'autorise rien.
- Vue — `roadmap-view [--json] [--write] [--html P] [--markdown P] [--style]` calcule
  la vue depuis les fichiers du dépôt (roadmap et records, décisions, idées, Project
  State, manifeste, remotes, tags ; dans le squelette : `provenance/roadmap-template.v1.json`)
  et la rend par `scripts/roadmap_view.py` (core) en page HTML autonome
  (`reports/roadmap/ROADMAP.html`, ignorée) et en Markdown (`docs/governance/ROADMAP_VIEW.md`,
  committé ; première ligne `sources_digest`, `generated_at`, `head`). Forme stable :
  bandeau de vérification, chiffres clés, versions, « Maintenant », « Ce qui t'attend »,
  « Prochaines étapes », « Plus loin », les idées et ce qu'elles sont devenues, le passé
  replié, un repli technique ; chaque ligne cite sa source ; le style suit
  `reporting_style` (`PLAIN` : aucun identifiant technique hors du repli). Réglages
  `project_control/roadmap-view.v1.json` (`style`, `zoom`, `language`, `regeneration`
  `OFF | HOURLY | EVERY_4_HOURS | DAILY`, `mirrors`). `status` affiche « Vue roadmap : à
  jour | périmée | absente » ; contrôle `ROADMAP_VIEW` (réglages valides ; une vue
  périmée n'est jamais une erreur). En `NORMAL_MODE`, la vue Markdown est réécrite et
  committée par le contrôleur lui-même, seulement quand ses sources ont changé, depuis
  la canonique sur un worktree propre (`chore(project-control): roadmap view`) ;
  `--style` ne touche que la page ; un chemin explicite est une simple écriture.
- Squelette — `provenance/roadmap-template.v1.json` (schéma `template-roadmap.v1.schema.json` :
  versions, chantiers P1 → P12 avec leur fiche, décisions, situation, attentes, étapes,
  idées ID-001 → ID-018, passé) et `provenance/roadmap-view.v1.json` ; sorties
  `provenance/roadmap/ROADMAP.html` (ignorée) et `provenance/ROADMAP_VIEW.md`. La
  version courante affichée est la plus haute taguée ; une version listée sans tag est
  « la suivante ». Fiches rapatriées dans `provenance/maintenance/scopes/` (README,
  revue du 5 sept., contre-revue Codex, P1, P2, P3, P4, P9, P11, P12, mandat WI-061,
  mémoire de la discussion ROADMAP).
- Doctrine — `docs/agent-governance/ROADMAP_VIEW.md` (core, routé pour le scope
  `governance`) : la vue montre et ne décide rien ; l'idée s'enregistre dans la session
  où elle est dite ; dans la discussion « ROADMAP <PROJET> », tout message est une
  régénération, `RÉGLAGE :` et `STOP ROADMAP` sont les seules exceptions, tout le reste
  est renvoyé, rien n'y est écrit ni décidé. Section « Vue ROADMAP et idées du Project
  Owner » dans `AGENTS.core.md` ; rappels dans `CLAUDE.md`, `FIRST_START.md`,
  `project_control/README.md`, `README.md`.
- Écarts assumés par rapport à la fiche : pas de `ROADMAP_TEMPLATE.md` rédigé à la main
  (la vue Markdown générée est la forme humaine, `OMIT`) ; pas de `last_generated` dans
  les réglages (le marqueur de la vue le porte) ; `IDEAS.md` n'est pas routé comme
  autorité (une idée ne décide rien, et chaque `idea add` périmerait la preuve de
  lecture) ; le rythme s'écrit `DAILY` plutôt que `daily`.
- Tests : trois nouveaux — vue d'une copie neuve (rien d'écrit sans `--write`, sources
  citées, `PLAIN` sans commit hors repli, réglage invalide refusé, vue périmée jamais une
  erreur) ; idées (deux formes committées, cible inexistante et `DISCARDED` sans cible
  refusés sans écriture, branche de travail et worktree sale refusés, désynchronisation
  refusée par l'audit, Bootstrap Mode sans commit) ; vue d'un projet initialisé (commit
  par le contrôleur seulement au changement des sources, `--style` sans commit, branche
  de travail refusée, chemin explicite non committé, aucun chantier du template dans la
  vue du projet). Fixture `NOT_STARTED` étendue (idées, réglages, vues générées).
  Manifeste régénéré (`skeleton_version` `3.8.0`).
- Limite assumée : le contrôleur garantit la forme, les sources et la cohérence de la
  vue ; il ne peut ni entendre une idée à la place de l'agent ni tenir la convention de
  la discussion ROADMAP à sa place — c'est de la doctrine, comme le style de retour.

## 2026-09-07 — `claude/v3.7-reporting-style` — style de retour au Project Owner (P11) et `Folder scope` dans le dépôt cible (O-10)

- Mandat : « je pensais au moment de la configuration du projet proposer d'imposer à l'ia
  de faire soit un retour technique […] soit tel que tu me réponds maintenant ! Ce doit être
  le choix de l'utilisateur. » puis décisions 1-2-3 et « ok » (2026-09-07) ; scope
  `claude/p11-scope-style-de-retour.md`.
- Baseline : `main` à `0d5d86f` (`v3.6.1`).
- P11 — Le Project Owner choisit à l'initialisation la forme des retours qui lui sont
  faits : `reporting_style` dans `project-state.v1.json`, obligatoire, `TECHNICAL` ou
  `PLAIN`, `UNKNOWN` seulement tant que la question n'a pas été posée (`NOT_STARTED`).
  Question ajoutée à l'interview de `FIRST_START.md` ; `bootstrap-closeout` et tout état
  `COMPLETE` refusent `UNKNOWN` nominativement ; contrôle d'audit `REPORTING_STYLE` ;
  `status` l'affiche en première ligne après le projet (« Retour au Project Owner : … »)
  et dans `status --json`. Doctrine : section « Retours au Project Owner » d'`AGENTS.core.md`
  — `TECHNICAL` : détail complet dans la conversation ; `PLAIN` : langage courant en trois
  points (ce qui s'est passé, ce que ça change, ce qu'il doit faire), détail dans les
  fichiers, une phrase sur ce qui sera touché avant toute demande de permission ; records,
  preuves, rapports et commits gardent leur forme dans les deux cas, un rapport `PLAIN`
  commence par un résumé en trois points ; changer le style = décision humaine enregistrée.
  Rappel dans `CLAUDE.md`, `project_control/README.md`. Un projet 3.6.x ajoute la ligne à
  la mise à niveau, sous décision humaine (`missing reporting_style` jusque-là).
- O-10 — `Folder scope` se renseigne aussi lorsque la décision est enregistrée dans le
  dépôt cible lui-même, après qu'un agent a franchi un double arrêt pour y venir : la
  décision nomme le dossier et cite les deux confirmations, vérifiées par le contrôleur de
  ce dépôt ; un travail interne sans sortie de périmètre porte `NOT_APPLICABLE`
  (`AGENTS.core.md`, modèle de `HUMAN_DECISIONS.md`).
- Tests : un nouveau — copie neuve `UNKNOWN` (bootstrap-audit PASS, `status` « non
  choisi ») ; `bootstrap-closeout` refusé sans choix, accepté avec ; projet initialisé :
  première ligne de `status` et `status --json` ; `UNKNOWN`, libellé inconnu ou champ absent
  refusés nominativement après `COMPLETE`, sans traceback ni écriture. Fixture `NOT_STARTED`
  et helper de clôture des tests étendus. Manifeste régénéré (`skeleton_version` `3.7.0`).
- Limite assumée : le contrôleur garantit que le choix existe, est affiché et lu ; il ne
  vérifie pas la forme d'une réponse. Le respect du style relève de la doctrine, comme la
  lecture effective des autorités.

## 2026-09-07 — `claude/v3.6.1-authorities-baseline` — baseline de preuve de lecture (correctif P3)

- Mandat : « fais ce qui est pro ! » (2026-09-07), après la démonstration de la mise à
  niveau de routine `3.5.0 → 3.6.0` sur un clone jetable d'un projet dérivé réel
  (redline `RL-T-01`, MAJOR) ; périmètre confirmé par double arrêt sur ce dépôt.
- Baseline : `main` à `8ea4aec` (`v3.6.0`).
- Défaut corrigé : l'audit 3.6.0 exigeait `authorities_read` sur tout Agent Run absent de
  la baseline d'adoption. Un projet ayant vécu entre sa `legacy_baseline` et l'arrivée de
  la preuve de lecture porte des Agent Runs clos sans preuve, que `acknowledge-authorities`
  ne peut pas réparer (Agent Run en cours seulement) : après `template-upgrade --apply`,
  `audit` échouait, le hook refusait tout commit et toute transition était verrouillée —
  la 3.6.0 était inadoptable par un projet avec historique.
- Contenu : `authorities_baseline` dans `project-state.v1.json`, obligatoire, `null` sans
  Agent Run antérieur à la preuve de lecture, sinon `{"head", "human_decision_ref"}` sur le
  modèle exact de `legacy_baseline` (commit existant et ancêtre de `HEAD`, décision humaine
  enregistrée, `HEAD` jamais substitué, refusée en `NOT_STARTED`). Les Agent Runs présents
  dans l'arbre à ce commit sont exempts de `authorities_read`
  (`authorities_exempt_agent_run_refs` = union des deux baselines) ; tout Agent Run
  postérieur porte la preuve. Nouveau contrôle d'audit `AUTHORITIES_BASELINE`
  (déclaration valide, nombre d'Agent Runs exempts) ; message d'erreur complété
  (« exempt only through authorities_baseline ») ; `status --json` expose
  `authorities_baseline`. Le Work Item de mise à niveau déclare la baseline par sa
  décision humaine puis enregistre sa propre lecture par `acknowledge-authorities`
  depuis la canonique avant `close` (`AUTHORITY_MANIFEST_AT_CLOSE` l'exige).
- Doctrine : phrase d'exemption étendue dans `AGENTS.core.md` ; `project_control/README.md`
  (preuve de lecture, records, compatibilité) ; `FIRST_START.md` (`null` pour un projet neuf).
- Tests : un nouveau — Agent Run enregistré après la baseline d'adoption sans preuve →
  audit refusé et `acknowledge-authorities` impuissant ; baseline déclarée → audit `PASS`
  nominatif et `status --json` ; le Work Item en cours ferme après `acknowledge-authorities`
  et pas avant ; un Agent Run postérieur à la baseline reste soumis à la preuve ;
  déclarations invalides (commit hors historique, décision non enregistrée, tête mal
  formée, absence) refusées sans traceback ni écriture ; `NOT_STARTED` refusé. Fixture
  `NOT_STARTED` des tests étendue. 93 tests. Manifeste régénéré (`skeleton_version` `3.6.1`).
- Correction connexe : `test_context_manifest_is_deterministic_and_follows_the_work_item_scopes`
  attendait `runtime_proof/README.md` (routage du template) et échouait dans un projet dérivé
  (Alpha ne route pas `runtime_proof/`) ; il suit désormais le routage de la copie testée
  (règle v3.4.1 : aucun test core ne dépend du contenu du projet).
- Note de transition : un projet déjà en 3.6.0 (copie neuve) ajoute
  `"authorities_baseline": null` à son `project-state` lors de la mise à niveau — la seule
  casse, signalée nominativement (`missing authorities_baseline`).

## 2026-09-07 — `claude/v3.6-proof-of-reading` — preuve de lecture des autorités (P3)

- Mandat : « alors p3 ? ou il faut un second projet ? » puis les deux options retenues
  (`TPL-D-013`, 2026-09-07).
- Baseline : `main` à `855558d` (`v3.5.0`).
- Contenu : `context-manifest [WI-NNN] [--scope S] [--json]` (lecture seule) liste les
  autorités du Work Item — base routée plus scopes déduits des `authorized_paths` par
  préfixe de chemin (`PATH_SCOPES`), records tenus par Project Control exclus
  (`MANIFEST_EXCLUDED_PATHS`) — avec le SHA-256 de chaque fichier et `MANIFEST_DIGEST`
  (SHA-256 des lignes `chemin sha256` triées). `start` et `resume` exigent
  `--authorities-digest` égal à l'empreinte courante, sans jamais l'afficher, et
  enregistrent `authorities_read` (empreinte, horodatage, HEAD, scopes, entrées) sur
  l'Agent Run créé ; le schéma `agent-run.v1` gagne ce champ optionnel. Le preflight
  d'un Work Item démarré vérifie `AUTHORITY_MANIFEST_PRESENT`, `_COMPLETE` et
  `_CURRENT` ; `status` expose `authorities` (`CURRENT` / `STALE` / `MISSING`) ; `close`
  refuse une lecture périmée (`AUTHORITY_MANIFEST_AT_CLOSE`) ; une autorité comprise
  dans les `authorized_paths` du Work Item ne périme pas sa propre preuve (l'agent en
  est l'auteur sous autorisation : mise à jour du core, amendement du Charter) ;
  `acknowledge-authorities WI-NNN --authorities-digest` enregistre une nouvelle lecture
  sur le dernier Agent Run, depuis la canonique, et committe
  (`chore(project-control): acknowledge authorities WI-NNN`). L'audit exige
  `authorities_read` sur tout Agent Run absent de la baseline d'adoption
  (`legacy_agent_run_refs`).
- Doctrine : « Preuve de lecture des autorités » dans `AGENTS.core.md` (procédure
  Normal Mode : `context-manifest` → lecture → `start --authorities-digest`) ; section
  et commandes dans `project_control/README.md`.
- Tests : cinq nouveaux — manifeste déterministe et routé par scope, exclusions ;
  `start`/`resume` refusés sans empreinte ou avec une empreinte périmée, sans fuite de
  l'empreinte attendue, records intacts ; Charter amendé pendant la session → preflight
  `FAIL`, `status` `STALE`, `close` refusé jusqu'à `acknowledge-authorities` ; autorité
  autorisée en écriture modifiée par le Work Item lui-même → preflight `PASS`, autre
  autorité modifiée → `FAIL` ; Agent Run antérieur à la baseline d'adoption exempt. Les tests existants présentent l'empreinte
  au démarrage. Fixture `agent-run.valid.json` étendue. Manifeste régénéré
  (`skeleton_version` `3.6.0`).
- Limite assumée : l'empreinte prouve que l'agent a obtenu la version exacte des
  autorités au moment du démarrage, pas qu'il les a comprises ; une autorité modifiée
  hors du dépôt (consigne orale) reste hors de portée du contrôleur.

## 2026-09-07 — `claude/v3.5-double-stop` — dossier accordé et double arrêt

- Mandat : « Dans notre squelette on va rajouter une sécurité ! … Peux-tu faire les
  modifications ? » (`TPL-D-011`, 2026-09-07).
- Baseline : `main` à `44905d1` (`v3.4.1`).
- Contenu : nouvelle section « Dossier accordé — double arrêt » dans `AGENTS.core.md`
  (déclencheur précis : écrire, brancher, committer, exécuter, pousser hors du dépôt ;
  lire n'est pas sortir ; contenu exigé de chaque arrêt ; défaut « copie, jamais
  l'original ») ; rappel dans `CLAUDE.md`. Forme mécanique : le modèle de décision
  humaine gagne `Folder scope:` et `Confirmation 1:` / `Confirmation 2:` ; le
  contrôleur (`human_decision_errors`) refuse toute décision hors dossier sans deux
  confirmations distinctes non `UNKNOWN`, avec motif nominatif dans `preflight`
  (`HUMAN_AUTHORIZATION`), `create-work-item`, `block`, `resume`, `audit` (liens des
  records) et la baseline d'adoption. Une décision sans `Folder scope` ou
  `NOT_APPLICABLE` reste inchangée.
- Aussi : formulation du hook corrigée (`O-08`) — l'audit du mode porte sur le
  worktree, la protection de la canonique sur l'état indexé (`AGENTS.core.md`,
  `project_control/README.md`).
- Tests : deux nouveaux — validateur (huit cas, dont confirmations identiques et
  `UNKNOWN`) ; Work Item adossé à une décision hors dossier refusé au preflight et au
  `start` jusqu'aux deux confirmations. Manifeste régénéré (`skeleton_version`
  `3.5.0`).
- Limite assumée : le contrôleur ne voit que les décisions enregistrées dans le
  dépôt ; la conduite de l'agent face à une consigne orale relève de la doctrine et de
  la skill de l'agent, mises à jour en même temps.

## Décisions du Project Owner — 2026-09-07 (suite 3)

- `TPL-D-010` — **Promotion.** `claude/v3.4.1-project-agnostic-suite` est promue
  branche canonique par fast-forward de `main` ; la baseline promue reçoit le tag
  `v3.4.1` (`skeleton_version` `3.4.1`). Décision « promouvoir » (2026-09-07), après
  la répétition générale de l'étape 2 de P2 sur un clone jetable de
  `alpha` (85/85). `v3.4.1` est la source du mandat d'adoption du core
  par `alpha` (WI-061). Push `origin` et `nas` par le Project Owner.

## 2026-09-07 — `claude/v3.4.1-project-agnostic-suite` — suite de tests indépendante du projet (P2, étape 1b, correctif)

- Mandat : « promouvoir » (2026-09-07) et répétition générale de l'étape 2 sur un
  clone jetable de `alpha` (lecture seule sur le dépôt, clone local dans
  l'espace de session, supprimé après) : avec le core `v3.4.0`, `audit`, `status`,
  `core-manifest` et `template-upgrade` passent sur Alpha, mais la suite du template
  échoue 65 fois — les fixtures `NOT_STARTED` copiaient tout l'arbre du projet, dont
  ses 242 fichiers métier sous `modules/`, et `NO_ACTIVE_BUSINESS_CAPABILITY` refusait
  chaque copie. Un test core ne doit dépendre d'aucun contenu du projet.
- Baseline : `main` à `b50228a` (`v3.4.0`).
- Contenu : la fixture `NOT_STARTED` est un squelette vierge — `applications/`,
  `modules/`, `shared/`, `contracts/`, `data/` et `reports/` sont ramenés à leur
  `README.md` avant `git init` ; `.DS_Store` ignoré à la copie. Test dédié
  (`test_not_started_fixture_prunes_project_capability_data_and_reports`). Manifeste
  régénéré (`skeleton_version` `3.4.1`, seul `tests/test_template.py` change).
- Ce que cela règle : la suite du template est exécutable telle quelle dans un projet
  dérivé — condition de l'étape 2 (« suite du template verte sur Alpha »).

## Décisions du Project Owner — 2026-09-07 (suite 2)

- `TPL-D-009` — **Promotion.** `claude/v3.4-template-upgrade` est promue branche
  canonique par fast-forward de `main` ; la baseline promue reçoit le tag `v3.4.0`,
  première version décrite par `provenance/core-manifest.v1.json`
  (`skeleton_version` `3.4.0`). Décision « promouvoir » (2026-09-07), après la
  question « dans l'ordre je dois soumettre à Codex en premier ? » : la mise à niveau
  d'un projet dérivé (étape 2 de P2, `alpha` en premier) part d'une
  version promue et taguée, jamais d'une branche. Push `origin` et `nas` par le
  Project Owner.

## 2026-09-07 — `claude/v3.4-template-upgrade` — manifeste du core et `template-upgrade` (P2, étape 1b)

- Mandat : « Étape 1 et après on passe à la deux ? » puis décisions « Oui, v3.3.0
  maintenant » et « Liste proposée » (`TPL-D-007`, 2026-09-07).
- Baseline : `main` à `285b56c` (`v3.3.0`).
- Contenu : `provenance/core-manifest.v1.json` — `skeleton_version` et empreinte
  SHA-256 des fichiers core retenus par `TPL-D-007` (19 fichiers), régénéré par
  `core-manifest --write --version` (réservé au template) ; `FIRST_START.md` hashé
  avec son marqueur d'initialisation normalisé. `AGENTS.md` scindé : le core vit dans
  `docs/agent-governance/AGENTS.core.md` (fichier core, routé en base), la racine
  appartient au projet et le déclare (`AGENTS_CORE:`) ; `audit` gagne
  `CORE_MANIFEST` (manifeste présent et bien formé, fichiers core présents, core
  déclaré) ; `status` affiche la version et l'écart local (`core_drift`), qui n'est
  pas une erreur d'audit. Nouvelle commande `template-upgrade --source <arbre>` :
  rapport par défaut (`IDENTICAL`, `UPDATED`, `ADDED`, `REMOVED_UPSTREAM`,
  `MODIFIED_LOCALLY`), `--apply` en `NORMAL_MODE` seulement, refus des fichiers
  modifiés localement sans `--overwrite` nominatif, fichiers retirés en amont jamais
  supprimés, marqueur de `FIRST_START.md` conservé, droits d'exécution copiés,
  manifeste de la source adopté, vérification avant validation, rollback complet ;
  retour de version refusé ; aucun record touché.
- Ce que cela règle : S-02 et S-03 de P2 (core modifié écrasé ; version inconnue) ;
  l'étape 2 (le projet dérivé remplace son core par celui du template) devient
  vérifiable et reproductible.
- Tests : cinq nouveaux — manifeste conforme à l'arbre et à l'ensemble décidé ;
  audit exigeant manifeste et déclaration du core ; dry-run sans écart sur copie
  neuve et refus d'`--apply` en Bootstrap Mode ; mise à jour des fichiers intacts,
  refus des fichiers modifiés, records intouchés, refus du retour de version et d'une
  source non intacte ; `core-manifest --write` réservé au template.

## 2026-09-07 — `claude/v3.3-legacy-baseline` — baseline d'adoption (P2, étape 1)

- Mandat : « ok je te suis ! » (2026-09-07), sur la proposition « promouvoir `v3.2.0`
  puis ouvrir P2 étape 1 », après la scope definition P2 (V2 : constats de
  l'inspection en lecture seule de `alpha`).
- Baseline : `main` à `713e472` (`v3.2.0`).
- Contenu : `project-state.v1.json` gagne `legacy_baseline`, obligatoire — `null`
  sans histoire antérieure, sinon commit d'adoption et décision humaine. `audit`
  gagne `LEGACY_RECORDS_PRESENT` et `LEGACY_EVIDENCE_FROZEN` : les Work Items `DONE`
  à la baseline conservent exactement leurs octets, les autres gardent leurs
  références de preuve comme préfixe inchangé ; `close_head` et les preuves
  structurées ne sont exigés que pour une clôture postérieure à la baseline ;
  `status` distingue `LEGACY_PRESERVED`, `STRUCTURED_VERIFIED`, `PENDING` et
  `INVALID` (`evidence_validation`). Une baseline absente, divergente ou sans
  décision bloque ; le contrôleur ne lui substitue jamais `HEAD`.
- Origine : modèle `LEGACY_EVIDENCE_BASELINE` du contrôleur de `alpha`
  (WI-060), repris comme record de projet plutôt que comme constante du contrôleur
  (`REUSE > ADAPT`) ; aucun concept métier importé.
- Ce que cela règle : S-01 de P2 — un contrôleur neuf sur des records anciens — sans
  migration de records ; l'étape 2 (le projet dérivé remplace son core par celui du
  template) devient possible.
- Aussi, en commit séparé sur la même branche : paragraphe d'introduction du README
  en anglais (mandat « L'anglais devra être saisi ! » ; commits et tags restent en
  français).
- Tests : deux nouveaux — histoire figée et preuve neuve vers l'avant ; baseline
  déclarée par une décision enregistrée, dans l'historique courant, jamais inférée.

## 2026-09-07 — `claude/v3.2-records-canonical` — records sur la branche canonique (P9, option A)

- Mandat : « P9-A » puis « Project Control commite lui-même » (décisions du Project
  Owner, 2026-09-07), après la scope definition P9.
- Baseline : `claude/v3.2-git-safety` (`55c5a35`), elle-même sur `v3.1.0`.
- Contenu : les records administratifs ne vivent que sur la branche canonique.
  `create-work-item`, `start`, `block`, `resume` et `close` s'exécutent depuis son
  checkout, à son tip, sur un worktree propre, et committent eux-mêmes leurs records
  (`chore(project-control): <transition> WI-NNN`) ; `start` crée la branche du Work
  Item depuis le commit de records ; `resume` committe avant d'aligner la branche.
  La branche d'un Work Item ne porte jamais de changement administratif :
  `preflight` et le hook le refusent (`WORK_BRANCH_RECORDS_READ_ONLY`). Tout échec
  annule le commit de records (`update-ref`) et restaure branche et fichiers.
- Ce que cela règle : unicité du chantier actif exacte depuis la canonique (S-01),
  fin du report manuel des records de blocage (S-02), plus aucun conflit de records
  aux merges d'intégration (S-03), `status` exact depuis la canonique (S-04). Les
  scénarios sont couverts par des tests, dont la reprise après entrelacement jusqu'à
  la clôture et le rollback d'un `start` échouant après son commit.
- Compatibilité : en Bootstrap Mode, les records de l'initialisation restent
  committés par l'agent avec elle ; les projets antérieurs adoptent le nouveau flux
  sans migration de records (aucun champ ne change), mais leurs branches en cours
  qui portent des records doivent être intégrées avant.

## 2026-09-06 — `claude/v3.2-git-safety` — hook de commit

- Mandat : « Ok je suis tous les points ! On attaque ! », après la proposition
  d'évolutions utiles sans complexification (hook Git, `template-upgrade`, preuve
  de lecture des autorités).
- Baseline : `main` à `64a3cb1d9281ee9e8d11277d84cd66a60d1f9aa2` (`v3.1.0`).
- Contenu : commande read-only `pre-commit` et hook `scripts/hooks/pre-commit`
  (installation `git config core.hooksPath scripts/hooks`) — audit du mode courant
  sur l'état indexé avant chaque commit, protection de la branche canonique
  (records administratifs, `reports/` et `provenance/` seuls admis, merges
  d'intégration admis), contournement explicite `PROJECT_CONTROL_HOOK_OVERRIDE`
  imprimé dans le rapport ; `status` indique si le hook est actif ; le hook est un
  fichier obligatoire du core. Deux tests exercent le hook par de vrais `git commit`.
- Ce que le hook rend mécanique : « un `bootstrap-audit` en échec interdit le
  commit », « ne pas développer directement sur la branche canonique sauf
  autorisation humaine explicite », « une écriture métier exige la branche, le
  statut et un chemin autorisé du Work Item » — jusqu'ici de la prose.

## 2026-09-06 — `claude/v3-redlines` — corrections après contre-revue

- Mandat : « ok corrigeons les lignes rouges ! », après la contre-revue indépendante
  des deux maintenances Codex (verdicts `…_REQUIRES_MINOR_REDLINE` pour
  `c98a94a`, `…_REQUIRES_MAJOR_REDLINE` pour `811b63b`).
- Baseline : `811b63bbf72f52329848fdcfec8e1ea73855afd8`.
- R1 — `resume` aligne une branche divergée par un commit de merge de la canonique
  dans la branche du Work Item, records administratifs pris de la canonique, refus
  et annulation sur conflit métier, rollback du tip en cas d'échec ; le scénario
  « chantier bloqué avec commit propre, autre chantier intégré, reprise, clôture »
  est couvert par un test.
- R2 — couplage à sens unique entre `runtime_target` et les gates runtime :
  `runtime_proof` obligatoire avec une cible runtime, `deployment` déclaré
  séparément ; Definition of Done et Project Control alignés sur le contrôleur.
- R3 — ADOPTION.md rétablit `OMIT > ACTIVATE WITHOUT NEED` et la décision humaine
  documentée pour toute activation, conformément à AGENTS.md.
- R4 — l'historique de maintenance du template quitte `WORKTREE_REGISTRY.md` et
  `reports/` pour `provenance/` (ce journal et `provenance/maintenance/`).
- R5 — `create-work-item` ajoute `reports/evidence/<WI-NNN>` aux chemins autorisés.
- Nettoyage : clé dupliquée dans la table des états du registre ; le test de la
  Definition of Done couvre les neuf niveaux.
- Contrôles : `audit`, `bootstrap-audit`, `check_git_traceability`, suite de tests
  complète ; résultats dans le message de commit.

## 2026-09-06 — `codex/v3-retour-v8` (`811b63b`) — blocage et reprise

- Mandat utilisateur : « ok go ! Et mettre a jour V3 en fonctions des connaissance
  ce V8 !? Si j ai bien compris on les appliques mais tu n'as pas proposé! ».
- Baseline : `c98a94a5009b9ffe2591fcaf89288998f96a982b` ; source du retour
  d'expérience générique : contrôleur du projet consommateur à `d4d7b5ad…`,
  adapté sans règle de domaine.
- Contenu : audit des changements métier selon le mode
  (`BUSINESS_CHANGE_AUTHORIZATION`), transitions `block` / `resume` avec
  `block_records` et décisions humaines structurées, provenance des Agent Runs,
  immutabilité des preuves après premier commit, branche canonique déclarée
  respectée. 69 tests.
- Rapport détaillé : `provenance/maintenance/2026-09-06-v3-retour-v8.md`.
- Contre-revue indépendante du 2026-09-06 : `…_REQUIRES_MAJOR_REDLINE` (reprise
  refusée dès que la branche bloquée portait un commit non intégré) — corrigé par
  l'entrée `claude/v3-redlines`.

## 2026-09-06 — `codex/v3-fiabilite-simplicite` (`c98a94a`) — fiabilité et simplicité

- Mandat utilisateur : « donc regarde pour ameliorer notre version V3 ! », avec la
  demande de conserver un cadre simple.
- Baseline : `35da2a2d82520cd735f5c1884fdc5f185254e8f6`.
- Contenu : commande `status`, `start_head` et ascendance vérifiée au démarrage,
  preuves de clôture en rapports JSON vérifiés (schéma `evidence.v1`, SHA-256,
  `close_head`), niveaux `DEPLOYED_IN_CONTROLLED_ENVIRONMENT` et `RUNTIME_PROVEN`,
  `runtime_target`, validation stricte des records, README raccourci. 45 tests.
- Rapport détaillé : `provenance/maintenance/2026-09-06-v3-fiabilite-simplicite.md`.
- Contre-revue indépendante du 2026-09-06 : `…_REQUIRES_MINOR_REDLINE` — corrigé
  par l'entrée `claude/v3-redlines`.

## 2026-09-05 — `main` (`35da2a2`) — baseline Git autonome

- Mandat : rendre la copie V3 conforme à ses propres règles et versionnée.
- Contenu : baseline Git autonome de la copie V3 (socle gouverné + `ADOPTION.md`
  + pack `runtime_proof/`), provenance complétée (`becc60f` → baseline courante,
  erratum `ERR-01`), `CLAUDE.md` comme point d'entrée agent. 28 tests.
- Détail : `TEMPLATE_PROVENANCE.md`.
