> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# RAPPORT DE MESURE — P19 « Deux volumes », phase 0

*15 septembre 2026. Posture : mesure, lecture seule. Aucune écriture hors de ce rapport,
aucune construction, aucun code du contrôleur modifié.*

---

## Résumé en trois points (pour le Project Owner)

1. **Ce que j'ai trouvé.** Dans Alpha, le journal des décisions est de très loin le
   document le plus lourd que l'agent doit relire à chaque démarrage : à lui seul il pèse
   **63 %** de tout ce qui doit être lu. Et **69 % de ce journal** est constitué de décisions
   figées, qui ne bougeront plus jamais.
2. **Ce que ça change.** Couper le journal en deux ferait tomber le poids de chaque démarrage
   d'environ **41 %** — comme si, sur un sac de dix kilos, on en retirait quatre avant chaque
   sortie. J'ai fait l'essai pour de vrai sur une copie jetable : la coupe marche, le texte des
   décisions reste identique au caractère près, et rien d'ancien n'a besoin d'être réécrit.
3. **Ce que tu as à faire.** Lire le § 1 et le § 7, puis dire **« construire »** ou
   **« arrêter »**. Il y a aussi une question de ton ressort au § 8 : ton seuil d'utilité était
   « au moins un tiers » — on est à plus du double, donc c'est largement passé, mais c'est toi
   qui confirmes.

**Verdict : `P19_MEASURE_PASS_BUILD_MAY_START`.**

---

## A. Préflight — l'état exact de ce qui a été mesuré

| Objet | État constaté |
|---|---|
| Dossier accordé | `~/Projets/squelette-chantier-p19/` (créé pour ce chantier) |
| Copie de travail | `source/` — clone `--no-hardlinks` de l'atelier, **aucun remote** (`origin` et `nas` retirés) |
| HEAD de la copie | `19b24cfc9ed9c07db37716c28a61fb901a907fbd`, branche `main` |
| Dernier tag | `v3.19.2` — conforme à l'attendu de la fiche |
| Arbre de travail | propre (0 chemin modifié) |
| `status` | `Squelette : 3.19.2 | core aligné` ; mode `BOOTSTRAP_MODE` (le squelette n'est pas un projet initialisé) |
| `core-manifest` | PASS — `skeleton_version 3.19.2`, 24 fichiers de core, arbre conforme au manifeste |
| `audit` | **PASS** — 23 contrôles, aucun échec |
| `bootstrap-audit` | **PASS** — 15 contrôles |
| `check_git_traceability.py` | **PASS** |
| Suite d'essais | **165 essais, tous verts** (121,8 s) — conforme à l'attendu de la fiche |
| `demo.py --check` | PASS |
| Garde-fou | installé par `install-gate` dans `.git/hooks/pre-commit`, référence inchangée |
| Atelier `~/Projets/Squelette V3 -runtime-proof` | **lu seulement** — HEAD `19b24cf`, arbre propre, inchangé en fin de mesure |
| Alpha `~/Projets/alpha` | **lu seulement** — branche `codex/wi-073-challenger-coverage-v2`, HEAD `8ef208e`, inchangé en fin de mesure |
| Clone jetable d'Alpha | `runs/alpha/` — clone `--no-hardlinks --branch main`, sans remote, HEAD `229c9c8`, `audit` PASS avant toute manipulation ; remis à neuf en fin de mesure (0 chemin modifié) |

Aucune divergence de préflight. `P19_PREFLIGHT_STATE_MISMATCH` n'est pas déclenché.

### A.1 Numérotation (§ 9.1 de la fiche)

- Chantiers déclarés dans `provenance/roadmap-template.v1.json` : `P1` → `P18`. **`P19` est
  bien le numéro suivant.** Confirmé.
- Dernière version listée : `3.19.2` (12 sept., `TPL-D-070` / `TPL-D-072`). La clé
  `next_version` vaut `null` : aucune version n'est réservée. **`3.20.0` est disponible.**
  Confirmé.
- Dernier numéro de décision du squelette : `TPL-D-072`.

### A.2 Une observation hors sujet, signalée sans plus

Le bloc `now` de `provenance/roadmap-template.v1.json` est périmé : il annonce « le squelette
est en 3.19.1 », « Alpha en 3.18.1 » et « 164 essais », alors que le dépôt est en
3.19.2, qu'Alpha est monté en 3.19.2 et que la suite compte 165 essais. Ce texte est saisi à la
main, il n'est pas régénéré par `roadmap-view`. Rien n'est décidé ici : c'est noté pour que ça
ne se perde pas.

---

## B. M1 — Le sac du démarrage, avant la coupe

Méthode : reconstitution exacte de `authority_manifest()` — documents `base` du routage plus
les scopes déduits des `authorized_paths` par `scopes_for_paths()`, moins
`MANIFEST_EXCLUDED_PATHS`. Les records de chantier n'entrent pas dans l'empreinte. Estimation
en jetons = octets ÷ 4 (ordre de grandeur assumé).

Trois formes d'autorisation typiques :

| Forme | `authorized_paths` | Scopes déduits |
|---|---|---|
| A — chantier métier | `applications/bitcoin_treasuries/` | `development` |
| B — chantier gouvernance | `docs/governance/` | `governance` |
| C — chantier large | `applications/`, `modules/`, `shared/`, `contracts/`, `data/` | `contracts`, `data`, `development` |

### B.1 Dans le squelette lui-même (copie, HEAD `19b24cf`)

| Forme | Documents | Lignes | Octets | ~jetons | dont `HUMAN_DECISIONS.md` |
|---|---|---|---|---|---|
| A | 12 | 1 616 | 99 194 | 24 798 | 3 365 o = **3,4 %** |
| B | 12 | 1 286 | 97 190 | 24 297 | 3 365 o = **3,5 %** |
| C | 17 | 1 734 | 105 189 | 26 297 | 3 365 o = **3,2 %** |

Les deux documents les plus lourds y sont `project_control/README.md` (40 213 o) et
`docs/agent-governance/AGENTS.core.md` (25 909 o). Le journal des décisions du squelette ne
contient que ses 4 décisions d'exemple : **dans le squelette, la coupe ne se voit pas.** Le
constat de la fiche est confirmé.

### B.2 Dans Alpha (clone jetable de `main`, HEAD `229c9c8`)

| Forme | Documents | Lignes | Octets | ~jetons | dont `HUMAN_DECISIONS.md` |
|---|---|---|---|---|---|
| A | 12 | 3 199 | 294 143 | 73 535 | 185 705 o = **63,1 %** |
| B | 11 | 2 788 | 287 637 | 71 909 | 185 705 o = **64,6 %** |
| C | 17 | 4 975 | 393 325 | 98 331 | 185 705 o = **47,2 %** |

`docs/governance/HUMAN_DECISIONS.md` est le **premier poste dans les trois formes**,
185 705 octets pour 1 409 lignes, soit environ 46 400 jetons relus à chaque `start`, à chaque
`resume` et à chaque `acknowledge-authorities`.

---

## C. M2 — Le journal d'Alpha, et ce que la coupe en ferait

État mesuré : 85 décisions, `HD-001` → `HD-087`, 185 705 octets, 1 409 lignes.

Baselines déclarées dans `project_control/project-state.v1.json` :

| Baseline | Commit | Décision | Décisions présentes | Bloc inchangé depuis | Poids |
|---|---|---|---|---|---|
| `legacy_baseline` | `d4d7b5a` | `HD-074` | 64 (`HD-001` → `HD-064`) | **64 sur 64** | 128 159 o = **69,0 %** du journal |
| `authorities_baseline` | `15ad8f9` | `HD-075` | 66 (`HD-001` → `HD-066`) | 66 sur 66 | 132 318 o = 71,3 % |

Aucune décision modifiée depuis sa baseline, aucune disparue. L'historique d'Alpha est
parfaitement stable — c'est la condition idéale pour une coupe.

### C.1 Projection avec la ligne de coupe retenue (`legacy_baseline`, décision 1 de la fiche)

| | Octets | ~jetons |
|---|---|---|
| Journal aujourd'hui | 185 705 | 46 426 |
| Carnet vivant + sommaire, après la coupe | 64 040 | 16 010 |
| Volume relié (plus lu au démarrage) | 128 159 | 32 039 |
| **Gain à chaque démarrage** | **121 665** | **30 416** |

Le sommaire projeté compte 64 lignes pour 6 494 octets — soit **5 %** du poids qu'il remplace.

### C.2 Effet sur le sac du démarrage complet

Mesuré après application réelle de la coupe dans le clone jetable :

| Forme | Avant | Après | Gain | Part du journal après |
|---|---|---|---|---|
| A — métier | 294 143 o (~73 535 j) | 174 112 o (~43 528 j) | **−120 031 o, −40,8 %** | 37,7 % |
| B — gouvernance | 287 637 o (~71 909 j) | 167 606 o (~41 901 j) | **−120 031 o, −41,7 %** | 39,2 % |
| C — large | 393 325 o (~98 331 j) | 273 294 o (~68 323 j) | **−120 031 o, −30,5 %** | 24,0 % |

Le gain est constant en valeur absolue (~30 000 jetons par démarrage) parce qu'il ne dépend que
du journal ; il pèse plus ou moins selon la taille du reste.

### C.3 Redaction_Human

Non mesuré : le dossier n'a pas été accordé à cette session, et la fiche interdit d'en sortir
pour aller le chercher. La fiche le donnait déjà comme « plus jeune » ; la mesure reste à faire
si tu veux le chiffre, elle prend cinq minutes une fois le dossier ouvert.

---

## D. Le grand essai — la coupe appliquée pour de vrai, puis observée

Fait dans `runs/alpha/` seulement (clone jetable), **sans toucher une ligne du contrôleur**, pour
répondre aux blocages X1 et X2 par un scénario reproductible plutôt que par une opinion. Le
clone a été remis à neuf ensuite ; les scripts sont rangés dans `runs/mesure/`.

### D.1 Ce que la coupe a produit

- 64 décisions déplacées dans `docs/governance/HUMAN_DECISIONS_VOLUME_1.md` ;
- 21 décisions restées dans le carnet vivant (`HD-065` → `HD-087`) ;
- un sommaire de 64 lignes inséré dans le carnet vivant ;
- **empreinte SHA-256 de chaque bloc déplacé : identique avant et après, pour les 64.** Aucune
  décision réécrite, résumée ou requalifiée ;
- aucune décision présente dans les deux volumes ; total conservé : 85.

### D.2 Ce que le contrôleur 3.19.2, inchangé, en dit

`audit` après la coupe naïve : **20 contrôles PASS, 3 FAIL.**

| Contrôle | Résultat | Cause |
|---|---|---|
| `SCHEMA_VALIDATION` | **FAIL** | 62 références `HD-001`…`HD-064` citées par 59 Work Items ne se résolvent plus : `validate_record_links` (ligne 1678) cherche le titre `## HD-NNN` dans le seul carnet vivant |
| `INITIALIZATION_STATE` | **FAIL** | même cause (la clôture d'initialisation relit la décision `HD-001`) |
| `GIT_TRACEABILITY` | **FAIL** | `UNEXPLAINED path: docs/governance/HUMAN_DECISIONS_VOLUME_1.md` — chemin nouveau, non classé |
| `LEGACY_RECORDS_PRESENT` | PASS | 59 Work Items figés à `d4d7b5a` — lit les records, pas les décisions |
| `LEGACY_EVIDENCE_FROZEN` | PASS | idem |
| `AUTHORITIES_BASELINE` | PASS | 60 Agent Runs exemptés à `15ad8f9` |
| `DOCUMENT_ROUTING` | PASS | **le volume 1 sort de l'empreinte de lecture tout seul** : il n'est pas routé, donc il n'entre pas au manifeste ; aucune exemption nouvelle n'est nécessaire |
| `MANDATORY_FILES`, `ROADMAP`, `IDEAS`, `ROADMAP_VIEW`, `WORKTREE_REGISTRY`, `CORE_MANIFEST`, `LANGUAGE`, `REPORTING_STYLE`, `COMMIT_GATE`, `NO_SYMLINKS`, … | PASS | inchangés |

### D.3 Le même essai avec une lecture « union des deux volumes »

Simulé hors du contrôleur, sur le même état :

| Question | Carnet vivant seul | Union des deux volumes |
|---|---|---|
| Références de décisions non résolues (sur 78) | **62** | **0** |
| Décisions figées retrouvées (attendu 64) | 0 | **64** |
| Décisions reliées invalides **sans** l'exemption | — | **5** (`HD-001`, `HD-002`, `HD-003`, `HD-004`, `HD-006`) |
| Décisions reliées invalides **avec** l'exemption | — | **0** |

Lecture : l'exemption des décisions figées survit intégralement à la coupe, à condition que le
contrôleur cherche la décision dans les deux volumes. Les cinq décisions listées sont celles
dont le champ `Chosen option` porte le texte de la décision et non le mot `AUTHORIZE` — ce sont
exactement celles qui avaient fait échouer l'audit d'Alpha le 9 septembre, et que la 3.14.1 avait
réglées par l'exemption. **Sans lecture des deux volumes, ce défaut reviendrait.**

---

## E. M3 — Qui lit le journal, et que deviendrait chacun

Tous les accès au fichier passent par `self.human_decisions` (`scripts/project_control.py`
ligne 1921). **11 points de lecture**, tous de la forme
`self.human_decisions.read_text(encoding="utf-8")` :

| Ligne | Fonction | Ce qu'elle y cherche | Lirait-elle le volume 1 ? |
|---|---|---|---|
| 2217 | `idea_target_errors` | cible d'une idée | oui, par l'union (une idée peut viser une vieille décision) |
| 2525 | `human_decision_entries` | id, date, `Decision:` — pour la vue roadmap | oui, par l'union |
| 3020 | `project_control_errors` | texte passé à `validate_record_links` | **oui — c'est le point décisif** |
| 3240 | `closeout_readiness` | décision de clôture d'initialisation | oui, par l'union |
| 4555 | `require_lifecycle_decision` | mandat d'une transition d'aujourd'hui | oui, par l'union : le texte est identique où qu'il soit ; une décision reliée n'autorise pas davantage pour autant |
| 4772 | `create_work_item` | la décision citée existe-t-elle déjà | oui en **lecture** ; l'**écriture** d'une décision neuve reste dans le carnet vivant, jamais dans le volume |
| 5613 | `legacy_baseline` | la décision qui déclare la baseline | oui, par l'union (cas de garde : une baseline dont la décision serait elle-même reliée) |
| 5653 | `frozen_decision_refs` | texte courant comparé au texte à la baseline | **oui — sans quoi l'exemption disparaît (§ D.3)** |
| 5685 | `authorities_baseline` | idem `legacy_baseline` | oui, par l'union |
| 5947 | `close_work_item` | mandats du chantier clos | oui, par l'union |
| 6092 | `preflight_findings` | mandats du chantier courant | oui, par l'union |

`frozen_decision_refs()` n'a qu'**un seul appelant** (ligne 3024). La surface de changement est
donc minuscule : un accesseur unique qui renvoie le carnet vivant, plus le volume relié quand il
existe, couvre les onze points d'un coup — `REUSE` plutôt que `REIMPLEMENT`. Les écritures, elles,
doivent continuer à viser le seul carnet vivant.

**Sur le coût : la lecture du contrôleur est gratuite en jetons.** Le contrôleur lit des fichiers
sur le disque ; ce que paie l'IA, c'est la liste des autorités du manifeste. Le volume 1 sortant
du manifeste, l'agent ne le lit plus, même si le contrôleur, lui, continue de le lire.

---

## F. M4 — La doctrine à retoucher

Phrases qui nomment le journal des décisions ou un registre unique :

| Fichier | Lignes | Ce qu'il faudrait y ajouter |
|---|---|---|
| `docs/agent-governance/AGENTS.core.md` | 45, 61, 68, **118**, 169, 177, 212 | ligne 118 est la clé : « `HUMAN_DECISIONS.md` en fait partie [des autorités] » — à compléter par les deux volumes, la ligne de coupe, et le fait que le volume relié ne s'ouvre qu'au besoin ; une section neuve décrivant la coupe et étendant « jamais reconstruites ni requalifiées » au déplacement |
| `project_control/README.md` | 33, 81, **101**, 230 | ligne 101 décrit ce que `context-manifest` liste ; ligne 230 décrit la déclaration d'une baseline. À compléter par la nouvelle commande et le contrôle d'audit |
| `FIRST_START.md` | 5, 14, **58**, 75, 95 | ligne 58 énumère les fichiers de gouvernance : y ajouter le volume relié comme fichier facultatif |
| `AGENTS.md`, `ADOPTION.md`, `docs/agent-governance/ROADMAP_VIEW.md` | 0 mention | rien à changer |

---

## G. M5 — Le routage, M6 — le rayon d'impact, M7 — le squelette lui-même

### G.1 M5 — Le routage

`docs/agent-governance/mandatory-documents.v1.json` route `docs/governance/HUMAN_DECISIONS.md`
à **deux endroits** : dans `base` (donc pour tout chantier) et dans le scope `governance`.

`MANIFEST_EXCLUDED_PATHS` (lignes 93-103) contient 9 chemins, tous des records tenus par le
contrôleur lui-même. Le commentaire du code dit expressément : « Human Decisions stay in. »

**Mécanisme le plus simple pour sortir le volume 1 de l'empreinte : ne pas le router du tout.**
Un fichier absent du routage n'entre jamais au manifeste, et le contrôle `DOCUMENT_ROUTING` ne
s'en plaint pas — vérifié en § D.2. Aucune exemption nouvelle, aucune ligne ajoutée à
`MANIFEST_EXCLUDED_PATHS`. C'est le chemin le plus économe.

### G.2 M6 — Le rayon d'impact

- Essais : **1 seul fichier**, `tests/test_template.py`, 25 occurrences de `HUMAN_DECISIONS`
  sur les 165 essais de la suite. Les essais construisent leurs propres dépôts et leurs propres
  décisions — conforme à ce qu'annonce la fiche.
- Dans Alpha : **59 Work Items** citent au moins une décision reliée, **62 références** au total
  sur 78 ; **168 fichiers** mentionnent une décision `HD-001`…`HD-064`.
- Commandes existantes : `status`, `audit`, `pre-commit`, `bootstrap-audit`,
  `bootstrap-preflight`, `bootstrap-closeout`, `preflight`, `create-work-item`, `start`,
  `block`, `resume`, `acknowledge-authorities`, `context-manifest`, `close`, `install-gate`,
  `core-manifest`, `template-upgrade`, `roadmap-view`, `idea`. **Aucune commande n'expose
  aujourd'hui une décision au lecteur** : `bind-decisions` et l'ouverture d'un chapitre
  (`decision show`) sont bien des ajouts, pas des doublons. `idea` fournit le modèle d'une
  commande à sous-verbes (`idea add` / `idea set`) si la coupe et l'ouverture doivent vivre sous
  un même mot (`decision bind` / `decision show`) — à trancher à la construction.
- `docs/governance/git-path-classifications.v1.json` devra connaître le nouveau chemin, sans
  quoi `GIT_TRACEABILITY` échoue (§ D.2).

### G.3 M7 — Le squelette lui-même

`provenance/CHANGELOG.md` pèse **196 249 octets, 2 406 lignes** — plus lourd que le journal de
Alpha. Mais **il n'est routé nulle part** : le mot `provenance/` n'apparaît pas dans le fichier de
routage, et `PATH_SCOPES` ne lui associe aucun scope. Il ne coûte donc **rien** dans l'empreinte
de lecture, aujourd'hui.

Conséquence pour ce lot : **aucune.** Le chantier P19 n'a pas à s'en occuper. Ce qui mérite ta
décision, séparément, c'est de savoir si c'est **normal** : le journal des décisions du squelette
est aussi sa loi, et un agent qui travaille sur le squelette ne le lit pas par obligation. Deux
lectures possibles — c'est voulu (le squelette n'est pas un projet gouverné, il est en
`BOOTSTRAP_MODE`), ou c'est un trou. Rien n'est décidé ici ; le rapport propose, tu tranches.

---

## H. Les trois blocages — aucun n'est déclenché

| | Blocage | Verdict | Preuve |
|---|---|---|---|
| **X1** | l'exemption des décisions figées exigerait de relire le texte intégral à chaque démarrage, et le gain disparaîtrait | **non déclenché** | § D.3 : l'exemption est intégralement retrouvée (64 sur 64) par une lecture des deux volumes côté contrôleur, qui ne coûte aucun jeton ; l'agent, lui, ne lit plus le volume (§ D.2, `DOCUMENT_ROUTING` PASS) |
| **X2** | la coupe casse la résolution des références d'anciens records, et la seule réparation serait de les réécrire | **non déclenché** | § D.2 et § D.3 : les 62 références cassent avec une coupe naïve, et se résolvent toutes (0 échec) dès que le contrôleur lit les deux volumes. **Aucun record n'est touché** — la réparation est dans le contrôleur, jamais dans l'historique |
| **X3** | seuil d'utilité non atteint (décision 7 : moins d'un tiers du journal figé) | **non déclenché** | § C : **69,0 %** du journal est figé, soit plus du double du seuil |

---

## I. Options et points à trancher

### I.1 Les huit décisions de la fiche — ce que la mesure en dit

| # | Décision proposée | Ce que la mesure dit |
|---|---|---|
| 1 | ligne de coupe = `legacy_baseline` | **confirmée.** 64 décisions figées, 0 modifiée, 0 disparue. `authorities_baseline` en donnerait 2 de plus (66) pour 4 159 octets de mieux : écart négligeable, et `legacy_baseline` est la ligne dont la doctrine parle déjà |
| 2 | volume relié intact à l'octet près + sommaire dans le carnet | **confirmée et démontrée** (§ D.1, 64 empreintes identiques). Sommaire : 64 lignes, 6 494 o, 5 % du poids remplacé |
| 3 | seul le carnet vivant reste une autorité routée | **confirmée**, et plus simple que prévu : ne pas router le volume suffit, sans exemption nouvelle (§ G.1) |
| 4 | une seule coupe pour l'instant | rien dans la mesure ne s'y oppose |
| 5 | la coupe est un geste du contrôleur | **confirmée** ; aucune commande existante ne fait déjà cela (§ G.2) |
| 6 | sans volume, rien ne change | **soutenue** : le squelette n'a que 4 décisions d'exemple et aucune baseline ; les 165 essais en place ne voient pas la différence |
| 7 | seuil d'utilité : un tiers | **largement franchi** (69,0 %) |
| 8 | version 3.20.0, chantier P19 | **confirmés** (§ A.1) |

### I.2 Ce qui reste à trancher par le Project Owner

1. **Construire ou arrêter.** C'est la question du § 9.2 de la fiche. Un « ok » général
   n'ouvre pas la construction.
2. **Le nom des commandes.** `bind-decisions` + `decision show`, ou un seul mot à sous-verbes
   `decision bind` / `decision show` sur le modèle d'`idea`. Proposition de Claude : le second,
   parce qu'il n'ajoute qu'un mot au vocabulaire au lieu de deux.
3. **Le journal du squelette lui-même** (§ G.3) : normal ou trou ? Aucune urgence, aucun effet
   sur ce lot.
4. **Redaction_Human** (§ C.3) : veux-tu la mesure, et donc l'ouverture de son dossier en
   lecture ?

---

## J. État Git final

| Dépôt | État |
|---|---|
| Atelier `Squelette V3 -runtime-proof` | HEAD `19b24cf`, arbre propre — **inchangé**, jamais écrit |
| Alpha `alpha` | branche `codex/wi-073-challenger-coverage-v2`, HEAD `8ef208e` — **inchangé**, jamais écrit, son travail en cours intact |
| `squelette-chantier-p19/source` | HEAD `19b24cf`, arbre propre, aucun remote, garde-fou installé — aucun commit, aucune branche créée |
| `squelette-chantier-p19/runs/alpha` | HEAD `229c9c8`, arbre propre (simulation annulée) |
| Poussé, tagué | **rien** |

---

## K. Verdict

```
P19_MEASURE_PASS_BUILD_MAY_START
```

La construction peut commencer, après la fiche V2 et la relecture par la seconde IA, dans la
copie et nulle part ailleurs.

---

## L. Journal du rapport

- V1 — 15 septembre 2026. Append-only : une correction crée une révision liée, jamais une
  réécriture silencieuse.

---

## M. Erratum 1 — la projection du sommaire (15 septembre 2026, après construction)

Le § C.1 projetait un sommaire de 6 494 octets, calculé en coupant les champs recopiés à 90 et 60
caractères. La fiche V2, elle, demandait de recopier la première ligne du champ **telle quelle**,
sans coupe. Les deux ne disent pas la même chose, et c'est la fiche qui commandait la construction.

Appliquée au vrai journal, la règle « telle quelle » produit un sommaire de **97 438 octets**,
63 % du carnet vivant, une ligne atteignant 12 212 octets — le gain tombe à 17 % du journal. La
cause : dans un projet réel, `Decision` et `Chosen option` sont des paragraphes écrits sur une
seule ligne.

Corrigé par l'amendement 1 de la fiche : la ligne de sommaire **cite** le début de chaque champ et
**marque sa coupe** (`[…]`). Mesure réelle après la coupe, dans le clone jetable, avec le
contrôleur 3.20.0 : sommaire 11 430 octets, carnet vivant 186 333 → **68 958 octets**, empreinte de
lecture de la forme métier 294 143 → **182 863 octets** (−37,8 %), audit **23 PASS / 0 FAIL**.

Les chiffres des § B, C et D ne changent pas : ils portent sur l'état d'avant et sur la coupe
elle-même, non sur la forme du sommaire.
