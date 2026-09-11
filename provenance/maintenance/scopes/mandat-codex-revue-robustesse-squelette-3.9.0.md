> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Mandat — Revue de robustesse indépendante du squelette 3.9.0

> À coller dans une session Codex **neuve**, en une seule fois, avant toute autre consigne.

## 0. Ce qui est demandé, en une phrase

Vérifier, preuves à l'appui, que les contrôles du squelette 3.9.0 **refusent bien ce qu'ils annoncent refuser**, que ses garanties correspondent à ce que la documentation promet, et signaler chaque écart avec un cas reproductible. Tu es un relecteur indépendant et exigeant, pas un contributeur.

## 1. Posture — non négociable

`READ_ONLY` / `REPORT_ONLY`.

Interdits : toute écriture hors du livrable unique (§ 9) et du dossier `runs/` (§ 3) ; toute commande Git modifiante dans `source/` (`commit`, `branch`, `tag`, `merge`, `reset`, `clean`, `fetch`, `pull`, `push`, changement de référence) ; produire un correctif, une pull request, un ADR, un objet Project Control ou une décision humaine destinés au projet réel ; **attribuer au Project Owner une décision, une autorisation ou un verdict qu'il n'a pas donnés**, dans un dépôt comme dans le rapport ; écraser un livrable existant.

Consigne ambiguë ou contradictoire : tu l'écris dans le rapport et tu t'arrêtes sur ce point — tu ne tranches pas à la place du Project Owner. `UNKNOWN` reste `UNKNOWN`.

## 2. Objet exact — à vérifier et à rapporter en section A

Le squelette au tag `v3.9.0` :

- commit `9d78627cfa92ae8fe33e3d8d93b0a60271b16752`
- arbre `cd6d5bb1cc1a567164d590d7da85de7a69ef418a`
- 111 fichiers suivis
- `skeleton_version` `3.9.0`, 24 fichiers core (`provenance/core-manifest.v1.json`)
- 98 tests dans `tests/test_template.py`

Vérifie ces cinq valeurs toi-même (`git rev-parse`, `git ls-tree -r --name-only | wc -l`, `core-manifest`, exécution de la suite) et reproduis le résultat. Si l'une ne correspond pas : verdict `..._PREFLIGHT_STATE_MISMATCH` et arrêt — tu ne relis pas un autre objet que celui du mandat.

À lire intégralement avant d'écrire quoi que ce soit : `AGENTS.md`, `docs/agent-governance/AGENTS.core.md`, `docs/agent-governance/ROADMAP_VIEW.md`, `docs/agent-governance/mandatory-documents.v1.json`, `FIRST_START.md`, `ADOPTION.md`, `CLAUDE.md`, `project_control/README.md`, `docs/governance/DEFINITION_OF_DONE.md`, `README.md`, `provenance/CHANGELOG.md`, `provenance/README.md` et les fiches de `provenance/maintenance/scopes/` (elles disent ce qui a déjà été décidé et pourquoi).

## 3. Dossier accordé — et lui seul

`~/Projets/squelette-challenge-codex/`

- `source/` — la copie du squelette au tag. Lecture, commandes en lecture seule (`status`, `audit`, `bootstrap-audit`, `context-manifest`, `core-manifest`, `template-upgrade` sans `--apply`, `roadmap-view --json`) et exécution de la suite de tests, qui travaille en dossier temporaire. **Rien n'y est modifié.**
- `runs/` — tes dépôts d'essai jetables. Tu y crées, exécutes et mets en défaut ce que tu veux : c'est là que se démontrent les cas.
- le livrable unique, à la racine du dossier accordé.

Hors périmètre et interdits d'accès : `~/Projets/Squelette V3 -runtime-proof` (le dépôt d'origine), `alpha` et ses copies, tout autre dossier de la machine, tout dépôt distant — aucun réseau n'est nécessaire.

## 4. Méthode

- **Un cas reproductible** = les commandes exactes, leurs sorties, l'état Git avant et après, rejouable depuis zéro dans un dépôt d'essai neuf. Un cas qui ne se rejoue pas n'est pas un cas.
- Les preuves se donnent par chemin, numéro de ligne, octets, SHA-256 — jamais de mémoire.
- **Sans cas reproductible, pas de ligne rouge.** Un doute ou une inélégance sont des observations : elles ne bloquent rien.
- Pour chaque point examiné, dis dans quelle catégorie il tombe : **garanti par le contrôleur** (un contrôle refuse), **tenu par la doctrine** (rien ne l'empêche mécaniquement, c'est la discipline de l'agent), ou **non couvert**. Confondre les deux premières est en soi un constat à signaler.
- **Jeux d'essai.** Dans `runs/` uniquement, tu crées tout ce qu'un cas demande : décisions, Work Items, Agent Runs, conversations, rapports de preuve, artefacts, branches, commits, dépôts entiers. Chacun porte la mention `JEU D'ESSAI — FICTIF, SANS VALEUR D'AUTORISATION` dans son texte et n'est attribué à personne. La suite de tests du squelette procède déjà ainsi (`HD-101`, `HD-102`, preuves synthétiques). Cité dans le rapport, un jeu d'essai donne toujours son chemin sous `runs/`.
- **Deux configurations, à distinguer systématiquement.** *Standard* : le dépôt tel qu'un projet l'utilise — garde-fou de commit installé (`git config core.hooksPath scripts/hooks`), tout passe par les commandes du contrôleur. *Dégradée* : garde-fou absent, fichiers écrits directement, variable d'environnement de dérogation utilisée. Un écart constaté en configuration standard et un écart qui n'apparaît qu'en configuration dégradée n'ont pas la même portée ; la sévérité s'en déduit.
- Mets le contrôleur à l'épreuve comme le ferait un utilisateur pressé, distrait ou trop confiant : c'est le profil réel d'un agent au travail.

## 5. Thèmes

**T-01 — Les refus tiennent-ils ?** Une écriture métier sans Work Item autorisé, ou hors des `authorized_paths`, est-elle toujours refusée ? Cas limites à couvrir : chemins inhabituels (segments relatifs, casse, accents, espaces, Unicode), liens symboliques, index et copie de travail désynchronisés, `.gitignore` et `.gitattributes`, sous-modules, worktrees multiples, merge ou rebase en cours, dérogation `PROJECT_CONTROL_HOOK_OVERRIDE`, garde-fou non installé.

**T-02 — Que prouve exactement la preuve de lecture ?** `context-manifest` fournit l'empreinte : un agent peut la relayer sans avoir lu les documents. Qu'est-ce qui est réellement établi, et qu'est-ce qui ne l'est pas ? La péremption fonctionne-t-elle dans tous les cas (autorité modifiée, décision ajoutée, autorité comprise dans les `authorized_paths`, `--scope`, baselines d'adoption) ? Une empreinte périmée ou mal formée est-elle toujours refusée ?

**T-03 — La clôture peut-elle aboutir sans preuve valable ?** Rapport pointant un artefact modifié après coup ; preuve empruntée à un autre Work Item ; `subject_commit` hors de l'ascendance attendue ; gates déclarées `NOT_APPLICABLE` pour éviter le travail ; `close_head` ; immuabilité d'un rapport mise en défaut par un merge, un amend ou un cherry-pick ; un statut `FAILED` qui redeviendrait une réussite.

**T-04 — Les transitions sont-elles atomiques ?** Interruption au milieu de `create-work-item`, `start`, `block`, `resume`, `close`, `idea`, `roadmap-view --write` (erreur d'écriture, permission refusée, signal) : l'état revient-il intégralement en arrière ? Deux chantiers actifs, branche préexistante à un autre tip, copie de travail sale, branche canonique divergente, commit historique perdu.

**T-05 — Le double arrêt tient-il ?** Décision hors dossier avec deux confirmations identiques, vides, `UNKNOWN`, ou rédigées par l'agent lui-même ; `Folder scope` absent alors que des `authorized_paths` sortent du dépôt ; chemins absolus ou remontants dans un Work Item ; sémantique de `Folder scope` quand la décision vit dans le dépôt cible.

**T-06 — La montée de version d'un projet existant.** `template-upgrade` : retour à une version antérieure, manifeste incohérent ou modifié, fichier core modifié localement, `--overwrite` mal employé, fichier core disparu en amont. Baselines d'adoption (`legacy_baseline`, `authorities_baseline`) : commit inexistant, non ancêtre, décision absente, baseline déplacée après coup. Un projet réel avec historique peut-il adopter la 3.9.0 sans se retrouver bloqué ? (Un blocage de ce type a déjà été trouvé en 3.6.0 : voir la fiche P3.)

**T-07 — La vue roadmap dit-elle vrai ?** Vue périmée présentée comme à jour ; `sources_digest` insensible à un changement de source ; identifiants techniques présents en style `PLAIN` ; commit automatique du contrôleur au mauvais moment (branche de travail, copie sale) ; contrôle `IDEAS` mis en défaut (désynchronisation JSON / Markdown, cible inexistante, état hors liste).

**T-08 — Le README promet-il plus que le squelette ne tient ?** Reprends ligne par ligne le tableau « Without a frame / with Squelette » et dis, pour chacune, quel mécanisme la tient — ou qu'aucun ne la tient. Puis la démo `examples/hello-squelette/` : l'entretien d'initialisation y est scripté et écrit certains records directement, comme les fixtures de tests — est-ce représentatif de ce qu'un vrai agent doit faire, ou est-ce arrangé pour bien paraître ? Le test de non-dérive peut-il passer alors que le README ne dit plus la vérité ?

**T-09 — Est-ce que ça fonctionne ailleurs ?** Versions de Python (3.9 à 3.13), Linux, dossiers avec espaces et accents, dépôt sans dépôt distant, branche canonique nommée autrement, Git ancien, locale et fuseau horaire différents, système de fichiers insensible à la casse.

**T-10 — Ce qui n'est pas mécanique.** Liste franchement ce qui ne repose que sur la discipline de l'agent (lire réellement les autorités, respecter le style de retour, tenir la convention de la discussion ROADMAP, ne pas abuser de la dérogation). Dis si la documentation le présente honnêtement comme tel, ou le laisse passer pour une garantie.

Si le temps ou le budget manquent : T-01 à T-06 d'abord, et déclare les thèmes non traités plutôt que de les survoler.

## 6. Déjà tranché — ne pas rouvrir

Le contrôleur s'exprime en français (une version anglaise est un chantier à part) ; le style de retour, la convention de la discussion ROADMAP et la lecture effective des autorités sont assumés comme relevant de la doctrine ; la stratégie de publication, la licence, les Topics et la release appartiennent au Project Owner ; les commits et les tags sont en français ; le README a un premier écran en anglais puis en français. Pas de constat sur ces choix — sauf si tu démontres un cas concret qu'ils provoquent.

## 7. Standard des constats

Chaque constat porte : identifiant (`F-01`, `F-02`, …) · sévérité · thème (`T-0N`) · objet précis (fichier, fonction, contrôle) · cas reproductible (commandes et sorties) · preuve (chemin, lignes, SHA-256) · configuration (standard ou dégradée) · impact réel pour un projet gouverné · correction proposée, la plus petite possible · statut.

Sévérités : `BLOCKER` — en configuration standard, un projet gouverné peut aujourd'hui faire passer du travail non autorisé, non lu ou non prouvé. `MAJOR` — écart réel sous condition réaliste, ou blocage d'adoption. `MINOR` — défaut réel, conséquences limitées. `OBSERVATION` — pas de cas reproductible.

## 8. Verdicts — vocabulaire fermé

Un verdict par thème, puis un verdict terminal, préfixés `SQUELETTE_3.9.0_REVUE_T0N_` et `SQUELETTE_3.9.0_REVUE_` :

`…_PASS` · `…_REQUIRES_MINOR_REDLINE` · `…_REQUIRES_MAJOR_REDLINE` · `…_CANONICAL_CONFLICT` · `…_INPUT_MISSING` · `…_PREFLIGHT_STATE_MISMATCH` · `…_OUTPUT_ALREADY_EXISTS`

Un verdict hors de cette liste est un défaut de livrable, pas une nuance.

## 9. Livrable

Un seul fichier : `~/Projets/squelette-challenge-codex/REVUE_ROBUSTESSE_SQUELETTE_3.9.0.md`. S'il existe déjà : verdict `…_OUTPUT_ALREADY_EXISTS`, et tu n'écris rien. Append-only : une correction crée une révision liée (`V2`, erratum), jamais une réécriture silencieuse.

Sections, dans cet ordre :

**A.** Preflight : état exact de l'objet (les cinq valeurs du § 2, vérifiées par toi) et du dossier accordé.
**B.** Inventaire : ce qui a été lu, ce qui a été exécuté, ce qui ne l'a pas été et pourquoi.
**C.** Méthode : arborescence de `runs/`, commandes de préparation, configurations employées.
**D.** Thème par thème (T-01 → T-10) : ce qui a été vérifié, ce qui a tenu, ce qui a cédé, avec les cas.
**E.** Constats, du plus grave au moins grave.
**F.** Lignes rouges (`BLOCKER` et `MAJOR`), chacune avec la correction minimale proposée.
**G.** Observations sans cas reproductible.
**H.** Tableau à trois colonnes : garanti par le contrôleur / tenu par la doctrine / non couvert (T-10).
**I.** Conflits d'autorité rencontrés, s'il y en a.
**J.** Décisions attendues du Project Owner.
**K.** État final du dossier accordé (`source/` inchangé, contenu de `runs/`).
**L.** Verdicts : un par thème, puis le verdict terminal.

Le rapport est technique ; commence-le par un résumé de trois points en langage courant pour le Project Owner : ce qui a été trouvé, ce que ça change, ce qu'il doit décider.

## 10. Ce qui n'est pas demandé

Une refonte, des fonctionnalités nouvelles, des remarques de style ou de formulation, une traduction, une optimisation de performance, l'ajout d'une dépendance, un avis sur la stratégie de publication. Le squelette est délibérément minimal : `OMIT > ACTIVATE WITHOUT NEED`. Toute proposition qui ajoute un mécanisme doit démontrer le cas concret qu'elle évite.
