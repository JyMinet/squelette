> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Revue indépendante de robustesse — Squelette 3.9.0

1. **Des protections utiles tiennent, mais plusieurs passages restent ouverts.** Les 98 tests fournis réussissent. Les essais supplémentaires montrent notamment qu’un renommage peut retirer un fichier hors du périmètre autorisé et que le hook laisse committer certains fichiers que le preflight refuse.
2. **Un résultat positif ne suffit donc pas à établir toutes les garanties annoncées.** Des interruptions laissent des transitions incomplètes, une montée de version peut écraser un fichier du projet et la vue ROADMAP peut annoncer des tests réussis malgré un échec exécuté. Les preuves de clôture ordinaires ont en revanche résisté aux cas testés.
3. **Le Project Owner doit décider du traitement des lignes rouges et de la couverture complémentaire.** Les corrections proposées sont minimales et ne sont pas appliquées. Aucune décision, acceptation de risque ou autorisation réelle ne lui est attribuée. La matrice de portabilité reste partiellement inconnue.

Revue du 8 septembre 2026, `READ_ONLY / REPORT_ONLY`. Tous les objets synthétiques cités se trouvent sous `runs/` et sont des **JEUX D’ESSAI — FICTIFS, SANS VALEUR D’AUTORISATION**. La mention exacte utilisée dans les fixtures est `JEU D'ESSAI — FICTIF, SANS VALEUR D'AUTORISATION`. Ce rapport est une revue, jamais une autorité de projet.

## A. Preflight : objet et dossier accordé

| Vérification | Résultat observé |
|---|---|
| `git -C source rev-parse HEAD` et `v3.9.0^{commit}` | `9d78627cfa92ae8fe33e3d8d93b0a60271b16752` |
| `git -C source rev-parse HEAD^{tree}` | `cd6d5bb1cc1a567164d590d7da85de7a69ef418a` |
| `git -C source ls-tree -r --name-only HEAD` : nombre de lignes | **111 fichiers suivis** |
| `core-manifest` et manifeste JSON | **skeleton_version 3.9.0 ; 24 fichiers core ; CORE_ALIGNED PASS** |
| Suite fournie, exécutée sans modification | **Ran 98 tests in 342.652s — OK**, code 0 |

Les cinq valeurs correspondent au mandat. `audit`, `bootstrap-audit`, `core-manifest` et `status --json` retournent aussi 0. L’objet annoté du tag est `e01ac27d13eb3984cab8937f5996e77723b30e02`, distinct de son commit : ce n’est pas une divergence. Le checkout est détaché au tag ; la branche locale `main`, déjà présente, pointe sur un autre commit et n’a pas été déplacée ni utilisée comme objet de revue.

Dossier accordé : `~/Projets/squelette-challenge-codex`. À l’arrivée : `source/`, `runs/`, `.DS_Store` ; aucun livrable final. Les éléments préexistants de `runs/` (`tmpk0jstzm0`, `source-before.json`, `preflight.txt`, `suite-preflight.txt`, `xcrun_db`) ont été laissés en place et ne servent pas de preuve à cette revue. Aucun dépôt distant ou dossier de projet extérieur n’a été consulté. Le texte du mandat a été lu dans la pièce jointe explicitement fournie.

Environnement effectif : macOS 26.6.2 arm64, Python 3.14.0 pour la suite globale, Git 2.50.1 Apple Git-155. Les essais supplémentaires de portabilité utilisent aussi Python 3.12.12.

Preuves :

- [runs/review-390/preflight/identity.json](<~/Projets/squelette-challenge-codex/runs/review-390/preflight/identity.json:1>) — lignes 1-24 ; 1 349 octets ; SHA-256 `99da8b931c5d306bc973cdac0029269156dd00599a08ad3ca5991c81b3eb61d1`.
- [runs/review-390/preflight/environment.json](<~/Projets/squelette-challenge-codex/runs/review-390/preflight/environment.json:1>) — lignes 1-5 ; 125 octets ; SHA-256 `836b7c5056a2beeeca3528fcb72226379f3f426fa5a99084fb712bfd9b5fcb3d`.
- [runs/review-390/preflight/suite.log](<~/Projets/squelette-challenge-codex/runs/review-390/preflight/suite.log:1>) — lignes 1-104 ; 17 686 octets ; SHA-256 `fe41da88cb9095f6a594d79ae2b9984d49110842c3df2e6f7583a9149ff8b549`.
- [runs/review-390/preflight/core-manifest.log](<~/Projets/squelette-challenge-codex/runs/review-390/preflight/core-manifest.log:1>) — lignes 1-7 ; 248 octets ; SHA-256 `c84de40fa2844d9a39309171ce614fcbb863add95ec78f5f2197bd13d56f2c80`.
- [runs/review-390/preflight/audit.log](<~/Projets/squelette-challenge-codex/runs/review-390/preflight/audit.log:1>) — lignes 1-25 ; 1 589 octets ; SHA-256 `c066a53d606de47f58921b55528a6c8fb845684e404fcaab3dcaf80b891e0281`.
- [runs/review-390/preflight/bootstrap-audit.log](<~/Projets/squelette-challenge-codex/runs/review-390/preflight/bootstrap-audit.log:1>) — lignes 1-28 ; 1 848 octets ; SHA-256 `708e67f7d3a7c2308793c78c3447a3b6143804f9d6acd0b1918832fe10afd901`.
- [runs/review-390/preflight/status.json](<~/Projets/squelette-challenge-codex/runs/review-390/preflight/status.json:1>) — lignes 1-19 ; 605 octets ; SHA-256 `a6c2cc2afed2de84e0296cab2dcf07f8d74d9b834e7a03a9cddf13ab53eaee8f`.

## B. Inventaire : lu, exécuté, non exécuté

Les lectures intégrales préalables ont porté sur `AGENTS.md`, `docs/agent-governance/AGENTS.core.md`, `docs/agent-governance/ROADMAP_VIEW.md`, `docs/agent-governance/mandatory-documents.v1.json`, `FIRST_START.md`, `ADOPTION.md`, `CLAUDE.md`, `project_control/README.md`, `docs/governance/DEFINITION_OF_DONE.md`, `README.md`, `provenance/CHANGELOG.md`, `provenance/README.md` et toutes les fiches de `provenance/maintenance/scopes/` :

- [source/provenance/maintenance/scopes/README.md](<~/Projets/squelette-challenge-codex/source/provenance/maintenance/scopes/README.md:1>)
- [source/provenance/maintenance/scopes/mandat-codex-alpha-wi-061.md](<~/Projets/squelette-challenge-codex/source/provenance/maintenance/scopes/mandat-codex-alpha-wi-061.md:1>)
- [source/provenance/maintenance/scopes/p1-consolidation-baseline-unique.md](<~/Projets/squelette-challenge-codex/source/provenance/maintenance/scopes/p1-consolidation-baseline-unique.md:1>)
- [source/provenance/maintenance/scopes/p10-scope-publication-vitrine-github.md](<~/Projets/squelette-challenge-codex/source/provenance/maintenance/scopes/p10-scope-publication-vitrine-github.md:1>)
- [source/provenance/maintenance/scopes/p11-scope-style-de-retour.md](<~/Projets/squelette-challenge-codex/source/provenance/maintenance/scopes/p11-scope-style-de-retour.md:1>)
- [source/provenance/maintenance/scopes/p12-scope-roadmap-dediee.md](<~/Projets/squelette-challenge-codex/source/provenance/maintenance/scopes/p12-scope-roadmap-dediee.md:1>)
- [source/provenance/maintenance/scopes/p2-scope-template-upgrade.md](<~/Projets/squelette-challenge-codex/source/provenance/maintenance/scopes/p2-scope-template-upgrade.md:1>)
- [source/provenance/maintenance/scopes/p3-scope-preuve-lecture-autorites.md](<~/Projets/squelette-challenge-codex/source/provenance/maintenance/scopes/p3-scope-preuve-lecture-autorites.md:1>)
- [source/provenance/maintenance/scopes/p4-scope-capability-adversarial-review.md](<~/Projets/squelette-challenge-codex/source/provenance/maintenance/scopes/p4-scope-capability-adversarial-review.md:1>)
- [source/provenance/maintenance/scopes/p9-scope-records-administratifs-et-branches.md](<~/Projets/squelette-challenge-codex/source/provenance/maintenance/scopes/p9-scope-records-administratifs-et-branches.md:1>)
- [source/provenance/maintenance/scopes/revue-mise-a-jour-codex-v3.md](<~/Projets/squelette-challenge-codex/source/provenance/maintenance/scopes/revue-mise-a-jour-codex-v3.md:1>)
- [source/provenance/maintenance/scopes/revue-squelette-v3.md](<~/Projets/squelette-challenge-codex/source/provenance/maintenance/scopes/revue-squelette-v3.md:1>)
- [source/provenance/maintenance/scopes/roadmap-squelette-memoire-claude.md](<~/Projets/squelette-challenge-codex/source/provenance/maintenance/scopes/roadmap-squelette-memoire-claude.md:1>)

La lecture ciblée d’implémentation a couvert les chemins, audits, autorisations, transitions, manifestes de lecture, baselines, preuves, upgrades et vue dans `scripts/project_control.py` ; le parseur Git dans `scripts/check_git_traceability.py` ; le hook ; le rendu de `scripts/roadmap_view.py` ; la démo, son transcript et les schémas/fixtures associés. Les 111 fichiers ont un inventaire d’octets/SHA-256 ; cela ne signifie pas une lecture ligne par ligne de tout le code de chaque test ou de chaque contrat optionnel.

Ont été exécutés : la suite complète de 98 tests ; les commandes de lecture sur la source ; les cycles contrôlés et cas adverses décrits en D/E ; la démo et son contrôle de dérive ; une adoption synthétique avec historique provenant du **tag local v3.5.0**, ancien contrôleur puis mise à niveau vers le core 3.9.0. Les neuf journaux T02/T03 contiennent 255 commandes ; les séries Git et transactions conservent leurs commandes et états ; la série ROADMAP/démo/portabilité contient 54 commandes initiales, trois contrôles supplémentaires sur le hook et trois commandes finales sur les états IDEA invalides.

Non exécutés : runtime Python 3.9, 3.10, 3.11, 3.13 ; Linux ; ancien Git ; service distant ou déploiement réel ; vraie confirmation humaine ; exécution métier externe ; crash machine, SIGKILL ou coupure électrique ; tous les points possibles d’interruption ; courses simultanées entre processus ; collisions intentionnelles de noms différant uniquement par la casse. Absence d’environnement ou hors périmètre, jamais preuve de succès. Le parsing avec grammaire Python 3.9 n’est pas un test de runtime 3.9.

- [runs/review-390/preflight/source-evidence-index.json](<~/Projets/squelette-challenge-codex/runs/review-390/preflight/source-evidence-index.json:1>) — lignes 1-668 ; 20 966 octets ; SHA-256 `66f5399045406313807691b92c1b832cc5ef414a83a5b19db0aa83e9f63cd882`.

## C. Méthode, préparation et configurations

Arborescence de la nouvelle campagne :

```text
runs/review-390/
  preflight/       identité, empreintes initiales, suite et audits
  git_scope/       harnais, campaigns, décisions, chemins et états Git
  proofs/          T02/T03, 9 dépôts, journaux et index de preuves
  proofs_replay/   rejeu neuf des 9 cas / 255 commandes
  transactions/    interruptions, upgrades, baselines, adoption historique
  transactions_replay/  rejeu neuf des deux écarts majeurs
  roadmap_docs/   vue, README/démo, portabilité, journaux et matrices
  roadmap_replay/ rejeu neuf des 57 commandes
  final/          inventaire source final, comparaison et inventaire des essais
  report-template.md, findings.py, assemble_report.py, report-draft.md
```

Les copies sont préparées à partir des fichiers locaux et des helpers d’initialisation de la suite fournie. Les paramètres humains de ces helpers sont remplacés par des mentions fictives dans les essais nouveaux ; leurs écritures préparatoires ne prouvent aucune autorisation humaine. La suite stock reste inchangée, avec ses propres fixtures demandées par le mandat. Les commits expérimentaux portent une identité synthétique sans personne réelle. Les mutations de fixtures sont distinguées des transitions évaluées. Les copies en échec sont conservées ; aucune remise à zéro de `source/` n’a été nécessaire.

**Standard** désigne ici un cycle de commandes du contrôleur, après initialisation de la fixture, avec `core.hooksPath=scripts/hooks`, hook exécutable et sans override. Les écritures ordinaires de fichiers de travail, suivies de `preflight` et de Git, sont l’objet du garde-fou. Elles ne sont pas une falsification des records. **Dégradée**, au sens strict du mandat, désigne notamment la modification directe d’un registre, un hook absent/non exécutable, une dérogation ou une réécriture de l’historique. Même lorsqu’une décision manuscrite est prévue par Project Control, les essais qui écrivent directement cette entrée sont signalés dégradés et ne fondent pas un BLOCKER standard. Une injection de panne appelle l’implémentation inchangée et interrompt un point déterministe ; elle est décrite comme telle, pas comme un parcours réussi ordinaire.

Les journaux conservent argv/commande, répertoire, code retour, stdout/stderr. Les instantanés conservent HEAD, branche, références, état de l’index et des fichiers, empreintes et modes ; les inventaires précisent les tailles des pièces. Ceux des harnais ne prétendent pas prouver l’absence de nouvel objet inaccessible dans `.git` ; le contrôle de conservation de la **source**, lui, compare aussi tous les fichiers `.git`.

Commandes de la suite, depuis `source/` :

```sh
export PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0
TMPDIR=~/Projets/squelette-challenge-codex/runs/review-390/preflight python3 -B -m unittest discover -s tests -v
python3 -B scripts/project_control.py audit
python3 -B scripts/project_control.py bootstrap-audit
python3 -B scripts/project_control.py core-manifest
python3 -B scripts/project_control.py status --json
```

Rejeu autonome des cas Git, depuis la racine accordée, avec **noms neufs** :

```sh
python3 -B runs/review-390/git_scope/cases.py replay-cases-neuf
python3 -B runs/review-390/git_scope/edges.py replay-edges-neuf
python3 -B runs/review-390/git_scope/decision_reject.py replay-decisions-neuf
```

Les séries exécutées de référence sont `campaign-02`, `edges-02`, `decisions-01`. `preparation-01` contient une erreur de fixture corrigée ; `campaign-01` réutilisait une référence HD déjà présente dans ses variantes de décisions. Ces essais préparatoires sont conservés mais exclus des constats concernés. Les séries finales repartent de copies neuves. Les valeurs SHA des commits varient au rejeu avec les horodatages ; les résultats attendus sont les mêmes refus, changements de fichiers et relations entre références.

Les procédures pour rejouer les harnais délégués dans des dossiers neufs sont jointes ci-dessous. Ne pas relancer leurs scripts de préparation dans les répertoires originaux déjà remplis.

Les rejeux ont été **exécutés dans ce même workspace** : neuf cas/255 commandes pour preuves ; 57 commandes pour ROADMAP/démo/portabilité ; deux écarts majeurs pour transactions. Les signatures de résultats correspondent aux originaux. Aucun second lancement de la suite source n’est revendiqué.

Pour préparer les prochains rejeux preuves/transactions, cet exemple crée deux dossiers frères neufs, jamais un autre workspace :

```sh
python3 -B - <<'PY_PREPARE_REPLAY'
from pathlib import Path
import shutil
b = Path('~/Projets/squelette-challenge-codex/runs/review-390')
for original, new in [('proofs_replay', 'proofs_rejeu_neuf'), ('transactions', 'transactions_rejeu_neuf')]:
    target = b / new
    target.mkdir(exist_ok=False)
    for script in (b / original).glob('*.py'):
        shutil.copy2(script, target / script.name)
PY_PREPARE_REPLAY
python3 -B runs/review-390/proofs_rejeu_neuf/replay.py --all --jobs 3
python3 -B runs/review-390/transactions_rejeu_neuf/review_transactions.py --prepare
python3 -B runs/review-390/transactions_rejeu_neuf/experiments.py
```

Le dernier script doit retourner 1 à sa **dernière préparation de baseline** (`CANONICAL_BRANCH_PROTECTED`), après les cas F-07/F-08 complets. Ce refus de fixture est documenté ; il n’est pas un échec des assertions de ces constats. Pour la suite transactions : `extra_experiments.py`, `historical_adoption.py`, `historical_finish.py`, `controls.py`, `baseline_move_commit.py`, `lifecycle_guards.py`, `no_work_item_hook.py`, dans cet ordre, sur le même nouveau dossier. Les commandes complètes figurent dans le rapport de sous-revue.

La recette ROADMAP V2 liée ci-dessous contient le lanceur complet : copier seulement les scripts/shim indiqués vers un dossier frère neuf, puis préparation, cas 001–048, pont de nom de pointeur, compléments 049–057. Le lot de 57 commandes a été rejoué avec la recette initiale ; V2 borne la comparaison à ces 57 entrées après l’ajout des cas 058–060. Son filtre et ses signatures ont été vérifiés contre le rejeu existant ; aucun troisième lot complet n’est revendiqué. **Ne pas lancer resume_cases.py dans un rejeu neuf.**

- [runs/review-390/proofs_replay/README-replay.md](<~/Projets/squelette-challenge-codex/runs/review-390/proofs_replay/README-replay.md:1>) — lignes 1-19 ; 2 512 octets ; SHA-256 `48fa4353dc46f74bf0cf08004832662a4f98781f11a746f295957514ce191597`.
- [runs/review-390/proofs_replay/REPLAY-RESULT.md](<~/Projets/squelette-challenge-codex/runs/review-390/proofs_replay/REPLAY-RESULT.md:1>) — lignes 1-34 ; 2 061 octets ; SHA-256 `c73a9e46fb9986d8215a3ef45b98dce7d335041754ef4bfc0bd9388927af6f4f`.
- [runs/review-390/proofs_replay/replay-evidence-index.json](<~/Projets/squelette-challenge-codex/runs/review-390/proofs_replay/replay-evidence-index.json:1>) — lignes 1-6168 ; 220 295 octets ; SHA-256 `59c78f4e0e566ec6a26abd71773bc090d3f40473454cd9d9a52d3cfe2d8debc5`.
- [runs/review-390/transactions_replay/REPLAY-RECIPE.md](<~/Projets/squelette-challenge-codex/runs/review-390/transactions_replay/REPLAY-RECIPE.md:1>) — lignes 1-16 ; 1 683 octets ; SHA-256 `51fe83839e848890bb7ece1cd600b14c38685c584c7a9f8b2485837ed7d9a5d2`.
- [runs/review-390/transactions_replay/REPLAY-RESULTS.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions_replay/REPLAY-RESULTS.json:1>) — lignes 1-198 ; 16 695 octets ; SHA-256 `e74a44c79b05d2cb0c805ab38e874fc1f84d649d29d137cd3b9d5913fdf401f9`.
- [runs/review-390/transactions/REPORT.md](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/REPORT.md:1>) — lignes 1-103 ; 20 198 octets ; SHA-256 `06eb7c3dcc2727b66c12e847d3d3988f57964fab8fbaa72d0a24becbeaa60fbd`.
- [runs/review-390/roadmap_docs/REPLAY-V2.md](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/REPLAY-V2.md:1>) — lignes 1-136 ; 11 376 octets ; SHA-256 `0e3cfb954099fdfba00eef1918197d5713509b4152f3ac1bfce354b384f3223b`.
- [runs/review-390/roadmap_docs/REPLAY-VALIDATED.md](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/REPLAY-VALIDATED.md:1>) — lignes 1-13 ; 1 658 octets ; SHA-256 `4874cec4d794753772214828e262cdc479d61a24fa0e655a3f3a807955b52e02`.
- [runs/review-390/roadmap_replay/REPLAY-RESULT.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_replay/REPLAY-RESULT.json:1>) — lignes 1-6 ; 150 octets ; SHA-256 `b319de2e468c6a627c3af7117f63f9705b18fc13e90f7d353c75306000101b16`.
- [runs/review-390/roadmap_docs/ADDENDUM-IDEAS-INVALID.md](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/ADDENDUM-IDEAS-INVALID.md:1>) — lignes 1-23 ; 3 351 octets ; SHA-256 `b3966e5d01761b4235ff9bea0d83622e83360a3e8df6dfbfdc8114bdee8eaa8b`.
- [runs/review-390/roadmap_docs/T07-invalid-state-preservation-and-replay-v2-check.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/T07-invalid-state-preservation-and-replay-v2-check.json:1>) — lignes 1-65 ; 2 219 octets ; SHA-256 `a4c604ecbc202e528ab9ddf04ab5b9e314d8c59b8b33f6e22d9832f09501689d`.


## D. Résultats thème par thème

### T-01 — Autorisations, chemins et Git

**Tient :** une nouvelle écriture dans `modules/` sans WI actif est refusée au commit ; un fichier extérieur au scope mais sous `modules/` est refusé par preflight et hook. Les chemins absolus et ceux contenant `..` sont refusés. Le preflight accepte les chemins valides avec `./`, slashs répétés, espaces, accents, Unicode grec et accents composés/décomposés ; il refuse la mauvaise casse du préfixe et les faux préfixes voisins. Le backslash est normalisé. Ces derniers sont des tests de chaînes prospectives ; ce n’est pas la preuve de toutes les équivalences de noms du système de fichiers.

**Cède :** origine de renommage hors scope ignorée (F-01) ; racines `scripts/`, `data/`, `contracts/` non couvertes par le contrôle de périmètre du hook (F-02) ; lien symbolique indexé masqué par un fichier ordinaire dans le worktree (F-05). La décision REJECT préparée dans le registre est consommée (F-03, configuration dégradée). Un merge d’intégration arrêté avant son commit est bloqué par le hook (F-09). Le statut d’un hook devenu non exécutable reste trompeur (F-13).

| Bordure demandée | Essai et conclusion |
|---|---|
| Liens / index différent du worktree | Lien visible refusé ; lien restant seulement dans l’index accepté et committé, mode Git `120000` (F-05). Aucun accès extérieur effectué. |
| Fichiers ignorés | Ajout d’une exclusion dans `.git/info/exclude` : fichier hors scope ignoré invisible au preflight sans `--path` ; même chemin déclaré refusé. Configuration dégradée pour cette exclusion ; pas de confinement OS promis. `.gitignore` livré est également utilisé par tous les tests. |
| `.gitattributes` | Attribut text/eol LF et contenu CRLF dans chemin autorisé : preflight et commit 0. Pas de matrice de filtres externes. |
| Sous-module | Dépôt enfant local sous `runs/`, ajout du gitlink et `.gitmodules` autorisés : preflight et commit 0 ; fichier enfant non suivi laissé sale : preflight parent 0. Le contrôleur ne gouverne pas récursivement le contenu interne du sous-module. |
| Worktrees multiples | Deuxième checkout canonique local ; création WI-002 possible, démarrage refusé pendant WI-001 actif. Pas de course simultanée testée. |
| Merge / rebase en cours | Merge `--no-ff --no-commit` autorisé par Git mais commit final refusé (F-09). Rebase arrêté sur edit : audit 0 mais preflight 1, branche détachée ; l’audit seul n’autorise pas à travailler. |
| Override / hook absent | Commit sans WI passe dans les deux modes dégradés prévus. Aucune prétention d’authentification du texte de mandat. |

Preuves de la matrice :

- [runs/review-390/git_scope/campaign-02/results.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/results.json:1>) — lignes 1-171 ; 2 807 octets ; SHA-256 `bbe2e8251f5bf104f370778253d503600d587226a13f7dd275b9734ab33fea8b`.
- [runs/review-390/git_scope/edges-02/results.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/edges-02/results.json:1>) — lignes 1-40 ; 564 octets ; SHA-256 `ea1d45dc465c8d9ce7f5998ab342437b386cd4d718f6e60f516db0e77fc11555`.

### T-02 — Ce que la preuve de lecture établit

**Tient :** digest absent, faux ou mal formé refusé sans mutation ; changement d’une autorité pertinente non autorisée refusé ; ancien digest d’acknowledge refusé ; relecture fraîche permet la suite. `--scope` étend le manifeste affiché mais ne change pas celui exigé au démarrage : comportement explicitement documenté. L’autorité comprise dans les `authorized_paths` bénéficie de l’exception déjà décidée, sans redline sur ce choix.

**Cède :** autoriser le parent `docs` permet de travailler dans un scope enfant sans ses autorités routées (F-06). Les baselines historiques ont les limites détaillées en T-06/F-10.

**Portée locale à retenir :** une décision ajoutée directement et committée sur la canonique rend `status` STALE sur celle-ci, mais la branche WI qui n’a pas intégré ce commit reste CURRENT et son preflight passe. Après intégration, preflight et clôture refusent. Le code et le README annoncent des empreintes du worktree : aucun contournement de clôture n’est établi par ce cas. Il n’est donc pas retenu comme ligne rouge autonome, malgré une proposition initiale dans les notes de travail. CURRENT ne signifie pas « toutes les autorités de toutes les refs sont intégrées ».

**Doctrine :** le contrôleur établit la présentation et la conservation d’un digest courant de la portée qu’il calcule, pas une lecture ni une compréhension par l’agent. La copie automatique de ce digest dans la démo le confirme ; le mécanisme P3 n’est pas remis en cause (F-18 ne vise que sa narration).

- [runs/review-390/proofs/T02-parent-scope.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/proofs/T02-parent-scope.jsonl:20>) — lignes 20-29 ; 634 374 octets ; SHA-256 `73de8d42e05b5a47f46107c73e71f3bd2c97e61b316e591f11c093296e147e12`.
- [runs/review-390/proofs/T02-canonical-authority.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/proofs/T02-canonical-authority.jsonl:26>) — lignes 26-35 ; 919 170 octets ; SHA-256 `3f808fc5d621233c587d5722822a5afe65f5df91e6c3b15a51429417c56f8aa1`.
- [runs/review-390/proofs/T02-authored-authority.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/proofs/T02-authored-authority.jsonl:24>) — lignes 24-26 ; 527 954 octets ; SHA-256 `6b0626dd1f9abe6f124b716739386408d76edfb7c2ab5f3f326d573b2e2f5712`.

### T-03 — Clôture et preuves

**Tient dans les essais :** absence de rapport, FAIL, autre WI, sujet inexistant, avant start ou existant hors ascendance, mauvais hash, mauvaise gate, preuve non committée et artefact modifié sont refusés. Après preuve conforme, close et audit passent. Une modification postérieure de l’artefact fait échouer l’audit. `close_head` se rattache à la baseline d’intégration effectivement contrôlée ; les enregistrements observés ne substituent pas silencieusement le commit de clôture à l’objet prouvé.

Rapport réécrit au même chemin avec hash recalculé : refus après commit ordinaire, merge et cherry-pick. FAIL réécrit en PASS au même chemin : refus ; nouveau rapport à un nouveau chemin : accepté. Le test stock `test_resume_requires_current_execution_evidence_and_preserves_failed_report` couvre en plus FAILED → block/resume, conservation du rapport FAIL et du run bloqué, refus de l’ancienne preuve puis réussite avec une nouvelle preuve après le dernier start.

**Limites démontrées, configuration dégradée :** un amend du premier commit de preuve retire l’ancien contenu de l’histoire atteignable ; close et audit acceptent le remplacement, bien que le reflog conserve l’ancienne référence. L’immuabilité est celle de l’histoire conservée, pas d’une ancre extérieure. Aucune redline BLOCKER standard n’est déduite de cette réécriture explicite.

**Doctrine :** `NOT_APPLICABLE` est une déclaration, pas une inférence sémantique. Des WI d’essai avec toutes les gates NA peuvent être clos sans rapport ; aucun essai n’établit qu’une vraie gate applicable aurait été détectée puis contournée. La réalité d’une exécution et l’honnêteté de l’applicabilité restent à l’agent et au mandat. Ces limites connues ne sont pas rouvertes.

- [runs/review-390/proofs/NOTES.md](<~/Projets/squelette-challenge-codex/runs/review-390/proofs/NOTES.md:1>) — lignes 1-130 ; 17 556 octets ; SHA-256 `d71ead9d21de4ea809ae00bf4ea6b8490ab7594a573ec8c1146ea7a9614b14ba`.
- [runs/review-390/proofs/evidence-index.json](<~/Projets/squelette-challenge-codex/runs/review-390/proofs/evidence-index.json:1>) — lignes 1-10603 ; 958 875 octets ; SHA-256 `bfebf5199516e3d9596010d41d4adbc288f2dda77bf614c4c0ba5c0ab5fc00c7`.
- [source/tests/test_template.py](<~/Projets/squelette-challenge-codex/source/tests/test_template.py:1998>) — lignes 1998-2074 ; 234 647 octets ; SHA-256 `6e433836cd93269623a41205709b338277d9a76e36df87a5d1f5fbd0fcfdb320`.

### T-04 — Atomicité et transitions

Six transitions (`create-work-item`, `start`, `block`, `resume`, `close`, `idea`) ont reçu une erreur OSError puis un SIGINT après leur première écriture. OSError restaure les états comparés dans les six cas ; SIGINT laisse une écriture partielle dans les six. Une PermissionError injectée dans start est correctement annulée. Un second point, après le commit administratif de start mais avant création de branche, laisse WI/run démarrés sans branche et l’audit peut encore passer (F-07). Il s’agit d’un vrai signal envoyé au processus, pas d’un résultat simulé retourné par le contrôleur.

| Commande / point | OSError | SIGINT | Autre couverture |
|---|---|---|---|
| create-work-item, première écriture | rollback complet comparé | décision orpheline ; audit peut passer | refus d’entrée stock |
| start, première écriture | rollback complet | état partiel | PermissionError : rollback ; après commit records : F-07 |
| block, première écriture | rollback complet | état partiel refusé à l’audit | suite block/resume |
| resume, première écriture | rollback complet | état partiel refusé à l’audit | conflits Git/rollback couverts par suite |
| close, première écriture | rollback complet | état partiel refusé à l’audit | preuves invalides sans mutation |
| idea, première écriture | rollback complet | état partiel refusé à l’audit | cible/état invalides refusés |
| roadmap-view --write | pas d’injection de panne exhaustive | non injecté | mauvais checkout / arbre sale : HTML déjà modifié malgré refus (F-16) |
| template-upgrade, première écriture | rollback complet | core partiellement écrit | F-07, code interrompu −2, core-manifest refuse |

Les essais nouveaux refusent sans mutation start avec second WI actif, worktree sale, index sale, branche préexistante au mauvais tip et checkout non canonique. La suite stock couvre aussi base hors ascendance, branche ayant perdu le commit d’un run, reprise de branches divergentes, conflit métier et échec du rollback fichier. Cela ne couvre ni tout ordonnancement concurrent ni un arrêt machine brutal.

- [runs/review-390/transactions/REPORT.md](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/REPORT.md:1>) — lignes 1-103 ; 20 198 octets ; SHA-256 `06eb7c3dcc2727b66c12e847d3d3988f57964fab8fbaa72d0a24becbeaa60fbd`.
- [runs/review-390/transactions/EVIDENCE-METADATA.md](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/EVIDENCE-METADATA.md:1>) — lignes 1-149 ; 32 946 octets ; SHA-256 `5919e73c94fdbeec1aca2e22a5b955070b8e75a1859bafdbe000eb76cfc755d6`.
- [runs/review-390/transactions/extra-journal.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/extra-journal.jsonl:1>) — lignes 1-324 ; 517 244 octets ; SHA-256 `a65bc414c06cd508d9120989eff7425d81956ffd06d52a36a2a1651154cb8aa6`.
- [runs/review-390/transactions/controls-journal.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/controls-journal.jsonl:1>) — lignes 1-158 ; 253 301 octets ; SHA-256 `f0b30a4265aea4feeee99c29538d8d765645d1cac94c5d9e418c145bfcd1b9ab`.
- [runs/review-390/transactions/lifecycle-guards-journal.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/lifecycle-guards-journal.jsonl:1>) — lignes 1-97 ; 156 089 octets ; SHA-256 `129f3a57d800d253503e6a6516f1ee89cf16ef18515c2b229bb2f257bda4b7f0`.

### T-05 — Double arrêt

Deux confirmations non vides identiques sont refusées ; `UNKNOWN`/`UNKNOWN` refusé. Deux confirmations vides suivies d’autres champs sont acceptées à create/start par absorption du saut de ligne (F-04). Deux chaînes distinctes écrites par l’agent sont acceptées : le moteur ne sait pas authentifier deux prises de parole humaines.

Sans `Folder scope`, un WI à chemins internes est accepté, conformément à l’interprétation déclarée. Un `Folder scope` contenant le chemin absolu du dépôt cible et deux confirmations est accepté : être déjà dans le dépôt cible ne dispense pas doctrinalement du double arrêt initial. Les `authorized_paths` absolus et remontants sont refusés même lorsqu’on prépare une HD ; aucun accès hors dossier n’a été effectué pour ce test. La détection d’une intention de sortir du dossier reste doctrinale, distincte de la validation de champs présents.

- [runs/review-390/git_scope/campaign-02/commands.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/commands.jsonl:236>) — lignes 236-360 ; 690 716 octets ; SHA-256 `3c69007342e60ef85653315058ee6a70c8feec3d8a2edbc08de6d8986fa3496a`.
- [source/docs/agent-governance/AGENTS.core.md](<~/Projets/squelette-challenge-codex/source/docs/agent-governance/AGENTS.core.md:250>) — lignes 250-277 ; 21 287 octets ; SHA-256 `2d5d644914defe15b15c686d876485665470763810c55d33ec09d56a23356755`.

### T-06 — Upgrade et baselines

**Tient :** dry-run sans écriture ; downgrade, core source incohérent, core local modifié sans overwrite, overwrite sans cible locale modifiée et application en bootstrap refusés dans les contrôles de la suite. Les fichiers retirés du manifeste amont sont signalés et conservés ; ce comportement est intentionnel. Les deux baselines refusent chacune commit inexistant, commit existant non ancêtre et décision absente : six contre-épreuves nouvelles en lecture seule.

**Cède :** un fichier existant du projet devenant nouveau fichier core est écrasé sans overwrite (F-08). Les Agent Runs exempts ne sont pas gelés octet pour octet (F-10). Une baseline déplacée après coup peut étendre les exemptions en gardant la même référence HD ; la mutation de Project State et la fabrication du run historique sont explicites et dégradées, non un BLOCKER standard. Une source amont dont le manifeste et les hashes sont forgés de façon cohérente peut inclure un registre : le plan lui fait confiance. Aucun système de signature ou d’origine fiable n’est promis ; ce cas ne vaut pas une corruption involontaire du manifeste authentique.

`template-upgrade --apply` lancé hors WI écrit des fichiers ; après indexation, le hook refuse le commit sur main. Le prérequis documentaire de lancer l’upgrade dans le WI relève en partie de la discipline ; aucun passage au commit standard n’est établi par ce cas isolé. Le signal pendant upgrade rejoint F-07.

**Adoption réelle de format historique, données fictives :** le core v3.5.0 est extrait depuis le tag local avec `git archive`, dans `runs/`. Son contrôleur audite puis crée/démarre un WI ; la mise à niveau 3.9.0 passe. La déclaration dédiée d’`authorities_baseline` et du style, appuyée par une HD fictive committée sur main, permet commit avec hook, intégration ff, acknowledge-authorities, close et audit final, tous 0. Les refus intermédiaires de champs manquants et de HD sur branche WI sont conservés. **Aucun blocage d’adoption 3.5 → 3.9 n’est reproduit sur ce parcours.** Ce n’est pas une validation de tous les historiques clients.

- [runs/review-390/transactions/historical-adoption-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/historical-adoption-result.json:1>) — lignes 1-58 ; 8 455 octets ; SHA-256 `53fb27c754b80f07936156f98f02fddf0c5e1f90beafc39f9ff6b146aff7e24c`.
- [runs/review-390/transactions/historical-finish-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/historical-finish-result.json:1>) — lignes 1-48 ; 5 191 octets ; SHA-256 `72dba6dc305522a7544eec5e732271048e0d279812114407a47fb3220cc5c533`.
- [runs/review-390/transactions/extra-t06-baseline-moved-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/extra-t06-baseline-moved-result.json:1>) — lignes 1-28 ; 4 486 octets ; SHA-256 `b3afe9add3c13130d6da560aae590e2b410ce15f0c5be8b55572fc8f0343d396`.
- [runs/review-390/transactions/extra-t06-baseline-moved-commit-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/extra-t06-baseline-moved-commit-result.json:1>) — lignes 1-26 ; 2 612 octets ; SHA-256 `012b8590f7c826975396113e679bab4a20aaaf1faa8c96957d9fbbcaa009f7a7`.
- [runs/review-390/transactions/t06-no-work-item-staged-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/t06-no-work-item-staged-result.json:1>) — lignes 1-19 ; 777 octets ; SHA-256 `8240ed56a2e57454b2508b64371b363872e8178b298c45a7bdbb71c9917a7df2`.

### T-07 — Vérité de la vue ROADMAP

Deux erreurs majeures sont reproduites : la fraîcheur ignore une promotion par tag (F-11) ; la carte de tests affiche une réussite après un test effectivement échoué (F-12). PLAIN laisse certains chemins et IDs dans la partie principale (F-14). DISCARDED accepte une cible textuelle sans décision ou WI-000 (F-15). Un refus de génération modifie déjà le HTML (F-16).

Les contrôles d’ID inexistant, cible vide, JSON/Markdown désynchronisés, branche non canonique et worktree sale refusent bien les opérations testées. Le complément 058–060 vérifie aussi FICTIF_INVALID : CLI refusée par argparse (code 2, sans mutation), puis audit refusé (code 1, sans mutation) après édition directe dégradée de JSON et Markdown dans une copie neuve, dont l’audit initial était 0. Aucun commit administratif intempestif n’est constaté dans ces refus ; la mutation HTML ignorée reste distincte. Ajouter le hook après les premiers essais template ne change ni le digest ni la fausse carte verte : contrôles complémentaires 055–057.

- [runs/review-390/roadmap_docs/REPORT.md](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/REPORT.md:1>) — lignes 1-169 ; 17 636 octets ; SHA-256 `8b46429c48e7ba282cb8bd95eac6c88d2c2c4b10ac379d4b6020294ef2a6c82b`.
- [runs/review-390/roadmap_docs/T07-hook-positive-control-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/T07-hook-positive-control-result.json:1>) — lignes 1-19 ; 660 octets ; SHA-256 `c470b81e5e69430deafbd436a23035ddc35ad940985ea25481ca82e01350e868`.
- [runs/review-390/roadmap_docs/T07-invalid-state-control-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/T07-invalid-state-control-result.json:1>) — lignes 1-31 ; 903 octets ; SHA-256 `c377561ddf6e8db9db67018e0e5146c3a65ede991545733d2d284b5d7baec683`.

### T-08 — README et démo

Lecture ligne par ligne des dix lignes du tableau « Without a frame / with Squelette » (anglais lignes 37–46, reprise française lignes 137–146) :

| Ligne / promesse résumée | Mécanisme observé | Portée réelle / écart |
|---|---|---|
| 1. Travail explicitement autorisé par décision enregistrée | create-work-item, lien HD, HUMAN_AUTHORIZATION | Origine humaine doctrinale ; entrées REJECT/vides acceptées F-03/F-04. |
| 2. État du projet enregistré dans le dépôt | Schémas, audit, liens et synchronisation des records | Pas de collecte automatique de ce qui n’a jamais été enregistré. |
| 3. Décisions avec périmètre, options et raisons | Registre et rubriques produites par create ; présence minimale contrôlée | Toutes les rubriques ne sont pas exigées pour une HD existante ; leur pertinence reste doctrinale. |
| 4. Preflight et hook refusent le hors-scope | normal_path_errors et gate de commit | Garantie partielle : F-01/F-02/F-05 ; aucun confinement des écritures OS. |
| 5. Preuve de lecture avant démarrage | Digest comparé puis conservé dans authorities_read | Possession et fraîcheur locale, pas lecture réelle ; F-06/F-18. |
| 6. Preuves pour chaque gate applicable avant DONE | Rapports, SHA-256, WI/gates, ascendance et immuabilité | T03 tient pour les cas ordinaires ; applicabilité et exécution vraie déclaratives. |
| 7. Branche dédiée, chemins explicites, pas de git add -A | start et contrôles de branche ; indexation explicite du contrôleur | Le hook ne sait pas quelle syntaxe a servi à indexer ; la prohibition reste doctrinale. |
| 8. status permet de reconstituer l’état | Lecture des records locaux et résultat d’audit | Pas l’avancement non enregistré ou distant ; limites de vue F-11/F-12. |
| 9. Le propriétaire choisit le style de retour | Valeur de reporting_style, validation et rendu | Respect des réponses en conversation doctrinal ; rendu contrôlé F-14. |
| 10. Deux confirmations pour changer de dossier | Vérification de deux champs distincts si Folder scope déclaré | Détection/authenticité doctrinales ; défaut lexical des vides F-04. |


La démo est un parcours scripté de référence. Elle écrit directement les réponses d’initialisation et certains records, puis fait réellement fonctionner le contrôleur pour le WI suivant, son refus de scope, les tests, l’intégration et la clôture. Les sorties stock se régénèrent ; ce n’est ni un entretien humain ni une preuve indépendante de consentement. Son contrôle de dérive peut passer lorsque les marqueurs du bloc README sont supprimés et son contenu rendu faux (F-17). La phrase qui affirme empêcher le démarrage d’un agent n’ayant pas lu dépasse le mécanisme illustré (F-18). Cela appelle une correction de promesse, pas une réouverture de la doctrine de lecture.

- [runs/review-390/roadmap_docs/README-MECHANISMS.md](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/README-MECHANISMS.md:1>) — lignes 1-35 ; 5 647 octets ; SHA-256 `a16e7f01fa83faf4d663ea0007de51d3ba248d7a743b0d20fd2f026d3074a028`.

### T-09 — Portabilité

| Dimension | Résultat établi | Limite |
|---|---|---|
| Python 3.12.12 | contrôleur, hook et démo testés | pas une seconde suite complète |
| Python 3.9 | grammaire ast acceptée pour trois scripts | runtime absent, UNKNOWN |
| Python 3.10 / 3.11 / 3.13 | aucun runtime disponible sur PATH | INPUT_MISSING |
| Python 3.14.0 | suite fournie 98/98 | hors de la plage 3.9–3.13 demandée |
| Linux | non disponible | INPUT_MISSING |
| macOS arm64 / Git 2.50.1 | environnement des cas | aucune généralisation Linux/ancien Git |
| Espaces et accents | copie `portabilité espace accent é`, audit/statut/vue 0 | noms path prospectifs T01 distincts |
| Sans remote | copies autonomes, `remote -v` vide | aucun réseau utilisé |
| Canonique `principal-review` | audit et transition idea 0 | variante accentuée refusée proprement par syntaxe |
| Locale / fuseau | C/UTC et en_US.UTF-8/Europe/Zurich, statut et modèle 0 | pas toutes les locales |
| Volume insensible à la casse | probe positif ; essais exécutés sur ce volume | pas de collision volontaire de deux noms |
| Ancien Git | aucun autre Git disponible | INPUT_MISSING |

- [runs/review-390/roadmap_docs/T09-filesystem-case.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/T09-filesystem-case.json:1>) — lignes 1 ; 89 octets ; SHA-256 `38a25fb63d2b0f1523b40ab5863cb6fa4ad1dbc7b6530ba5144c7a8b9d6496c6`.

### T-10 — Ce qui reste disciplinaire

Lire et comprendre, juger l’applicabilité des gates, dire vrai dans une preuve, respecter le style en conversation, recueillir la vraie décision, interpréter une discussion ROADMAP, déclencher le double arrêt et ne pas abuser d’un override sont des obligations de l’agent. Elles ne deviennent pas des propriétés mécaniques parce qu’un champ est présent. Le core et P3 le disent généralement honnêtement ; F-18 isole une promesse de démo qui le contredit. Le tableau H donne la séparation opérationnelle ; aucun constat ne conteste les choix déjà tranchés au §6 du mandat.

## E. Constats, du plus grave au moins grave

Statut de tous les constats ci-dessous : **OUVERT — reproduit, correction proposée, non appliquée**. Les chiffres de sévérité sont ceux de cette synthèse ; les notes des sous-revues conservent parfois une proposition initiale explicitement révisée ici. En particulier, la fraîcheur locale à une branche n’est pas une ligne rouge autonome, et les décisions éditées directement ne sont pas des BLOCKER standards.

### F-01 — BLOCKER — T-01 — Un renommage retire un fichier hors du périmètre autorisé

**Objet précis.** changed_paths et contrôle AUTHORIZED_PATHS ; même traitement des renommages dans check_git_traceability.

**Configuration.** Standard. Deux cycles CLI ; le premier crée modules/seed.txt avec autorisation modules, le second n’autorise que modules/allowed. Hook installé, aucun override ou record falsifié.

**Cas.** Dans la copie rename : git mv -- modules/seed.txt modules/allowed/seed.txt ; preflight WI-002 ; git commit avec le message fictif. Les commandes complètes sont lignes 143–145 du journal.

**Sorties et résultat.** Preflight 0, AUTHORIZED_PATHS PASS ; commit 0. Le fichier source disparaît du chemin non autorisé. Le parseur porcelain -z garde la destination et saute le second chemin du renommage.

**Impact.** Une frontière de WI est franchie dans le parcours complet avec contrôle positif. Autoriser la destination ne donne pas l’autorisation de supprimer l’origine.

**Correction minimale proposée.** Inclure origine et destination des renommages dans les contrôles de scope et de traçabilité ; ajouter le cas origine hors scope / destination dedans.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
python3 -B runs/review-390/git_scope/cases.py replay-f01-neuf
```

**États Git conservés.** [runs/review-390/git_scope/campaign-02/rename-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/rename-before.json:1>) : HEAD `e7a13b79e12d2dde64e60a2877a84d99c5e1dec2`, branche `work/wi-002-jeu-d-essai-fictif-sans-valeur-d-autoris`, statut `(propre)`. [runs/review-390/git_scope/campaign-02/rename-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/rename-after.json:1>) : HEAD `bddd4effa756f112282064fab17df328d13c02d4`, branche `work/wi-002-jeu-d-essai-fictif-sans-valeur-d-autoris`, statut `(propre)`. Les fichiers cités contiennent aussi index, refs et empreintes.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:1344>) — lignes 1344-1363 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/check_git_traceability.py](<~/Projets/squelette-challenge-codex/source/scripts/check_git_traceability.py:79>) — lignes 79-99 ; 6 763 octets ; SHA-256 `c1dc02aa658da7aa8cef87ed6b7e700a7ba71b0d4c70e8fa93fdb741957691e7`.
- [runs/review-390/git_scope/campaign-02/commands.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/commands.jsonl:143>) — lignes 143-151 ; 690 716 octets ; SHA-256 `3c69007342e60ef85653315058ee6a70c8feec3d8a2edbc08de6d8986fa3496a`.
- [runs/review-390/git_scope/campaign-02/rename-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/rename-before.json:1>) — lignes 1-610 ; 33 229 octets ; SHA-256 `efd7e75233a6d4afaac714b992ee14024b36ee24e58fbf11945685ddfae9ae92`.
- [runs/review-390/git_scope/campaign-02/rename-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/rename-after.json:1>) — lignes 1-610 ; 33 245 octets ; SHA-256 `9f6e70024730b9e322afe20f4568fde4304b09960cf25d6b893eeb00635bc1f3`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-02 — BLOCKER — T-01 — Le hook laisse committer des chemins que le preflight refuse

**Objet précis.** BUSINESS_ROOTS, business_change_authorization_errors, commit_gate_findings.

**Configuration.** Standard pour les protections testées : WI créé/démarré via CLI, hook installé/exécutable, pas d’override. Le commit après un preflight négatif est tenté exprès pour éprouver la dernière barrière ; cela ne prétend pas que le preflight a accepté.

**Cas.** WI limité à modules/allowed. Ajouter et indexer scripts/project_extra.py, puis data/source.csv dans deux copies ; faire preflight puis commit. Contrôle complémentaire contracts/unauthorized.md dans edges. Fichier modules/forbidden.py comme contre-épreuve.

**Sorties et résultat.** scripts et data : preflight 1, commit 0 (lignes 99–100 et 114–115). contracts Markdown : 1 puis 0 (53–54). modules/forbidden.py : 1 puis 1. Le premier essai contracts/input.json invalide échoue pour syntaxe JSON et n’est pas utilisé pour conclure sur le scope.

**Impact.** Un agent qui oublie une vérification ou modifie un autre fichier après elle peut faire accepter du travail hors scope. Le hook annonce les chemins autorisés mais ne filtre ici que applications/modules/shared, hors README.

**Correction minimale proposée.** Faire appliquer par le hook le scope du WI à tous les chemins de travail concernés, en partageant la logique du preflight et en gardant les seules exemptions administratives/preuves explicitement prévues.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
python3 -B runs/review-390/git_scope/cases.py replay-f02-neuf
python3 -B runs/review-390/git_scope/edges.py replay-f02-edges-neuf
```

**États Git conservés.** [runs/review-390/git_scope/campaign-02/path-scripts-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/path-scripts-before.json:1>) : HEAD `e7a13b79e12d2dde64e60a2877a84d99c5e1dec2`, branche `work/wi-002-jeu-d-essai-fictif-sans-valeur-d-autoris`, statut `(propre)`. [runs/review-390/git_scope/campaign-02/path-scripts-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/path-scripts-after.json:1>) : HEAD `2b573b220b0116a1dd5183b8de3a1e322c8d49e2`, branche `work/wi-002-jeu-d-essai-fictif-sans-valeur-d-autoris`, statut `(propre)`. Les fichiers cités contiennent aussi index, refs et empreintes.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:36>) — lignes 36 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:2327>) — lignes 2327-2364 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:2832>) — lignes 2832-2882 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/docs/agent-governance/AGENTS.core.md](<~/Projets/squelette-challenge-codex/source/docs/agent-governance/AGENTS.core.md:235>) — lignes 235-243 ; 21 287 octets ; SHA-256 `2d5d644914defe15b15c686d876485665470763810c55d33ec09d56a23356755`.
- [runs/review-390/git_scope/campaign-02/commands.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/commands.jsonl:82>) — lignes 82-121 ; 690 716 octets ; SHA-256 `3c69007342e60ef85653315058ee6a70c8feec3d8a2edbc08de6d8986fa3496a`.
- [runs/review-390/git_scope/edges-02/commands.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/edges-02/commands.jsonl:52>) — lignes 52-60 ; 280 987 octets ; SHA-256 `7a64ad9f23e482d28272ee65a700890dee61a5bae298b13b37330f82fe43b191`.
- [runs/review-390/git_scope/campaign-02/path-scripts-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/path-scripts-before.json:1>) — lignes 1-610 ; 33 229 octets ; SHA-256 `efd7e75233a6d4afaac714b992ee14024b36ee24e58fbf11945685ddfae9ae92`.
- [runs/review-390/git_scope/campaign-02/path-scripts-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/path-scripts-after.json:1>) — lignes 1-615 ; 33 468 octets ; SHA-256 `fcc4818b557dcf8110ef42ca447a37ee01621d161ccefc5298daa29bac44d9f8`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-03 — MAJOR — T-01 — Une décision enregistrée avec Chosen option: REJECT autorise create-work-item

**Objet précis.** human_decision_errors et branche decision_exists de create_work_item.

**Configuration.** Dégradée au sens strict du mandat : HD-301 écrite directement dans le registre puis committée sur main avec hook actif. Le consommateur create-work-item/start/preflight/commit est ensuite inchangé. La rédaction manuelle est prévue par Project Control, mais ce cas n’est pas compté BLOCKER standard.

**Cas.** HD-301 contient Decision et Authorized by fictifs, Related Work Item: WI-001, Folder scope: NOT_APPLICABLE et Chosen option: REJECT. create-work-item référence cette HD existante, sans --decision.

**Sorties et résultat.** Enregistrement 0 ; create 0 ; start 0 ; preflight 0 ; commit métier 0. Le choix structuré REJECT n’est jamais consulté par cette validation, alors que block/resume le refusent dans la suite stock.

**Impact.** Une entrée de registre explicitement négative est interprétée comme une autorisation. Ce constat porte sur la sémantique structurée déjà écrite, pas sur l’authentification d’un humain.

**Correction minimale proposée.** Refuser un Chosen option explicitement REJECT pour une autorisation de création ; harmoniser avec le validateur lifecycle en conservant une règle explicite pour les anciens formats.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
python3 -B runs/review-390/git_scope/decision_reject.py replay-f03-neuf
```

**États Git conservés.** [runs/review-390/git_scope/decisions-01/reject-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/decisions-01/reject-before.json:1>) : HEAD `ae2befd4ad6754adf03abd6ab3c8dbf8d7a7aff4`, branche `main`, statut `(propre)`. [runs/review-390/git_scope/decisions-01/reject-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/decisions-01/reject-after.json:1>) : HEAD `21b3fa78522ff100b66d286eceae38281dd29bd7`, branche `work/wi-001-jeu-d-essai-fictif-sans-valeur-d-autoris`, statut `(propre)`. Les fichiers cités contiennent aussi index, refs et empreintes.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:427>) — lignes 427-443 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:3271>) — lignes 3271-3281 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/project_control/README.md](<~/Projets/squelette-challenge-codex/source/project_control/README.md:31>) — lignes 31-39 ; 27 523 octets ; SHA-256 `fcd98f307d964581ebaf1c56a67db540bece3b502814ee7c8f1b59e745bb524e`.
- [runs/review-390/git_scope/decision_reject.py](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/decision_reject.py:1>) — lignes 1-17 ; 1 374 octets ; SHA-256 `e193332077d9f2db046bbdc8292efc2587554a75998ddcd625bbe8886eb4459f`.
- [runs/review-390/git_scope/decisions-01/commands.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/decisions-01/commands.jsonl:28>) — lignes 28-41 ; 135 692 octets ; SHA-256 `7d152105668f0eae18e9efc3177419ccb03021d45d179453a2bc010d4ced5df5`.
- [runs/review-390/git_scope/decisions-01/results.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/decisions-01/results.json:1>) — lignes 1-26 ; 384 octets ; SHA-256 `0dd32e57caea20723b5df70a16e929c6d213b3acfb24a8dc75945720e20bf86e`.
- [runs/review-390/git_scope/decisions-01/reject-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/decisions-01/reject-before.json:1>) — lignes 1-575 ; 31 068 octets ; SHA-256 `602d3716d9d0d5131416aff0b86737fdbcb1a9fc23de06d3ceb4884da3e4f01f`.
- [runs/review-390/git_scope/decisions-01/reject-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/decisions-01/reject-after.json:1>) — lignes 1-595 ; 32 298 octets ; SHA-256 `bdebfbfc7eb3a8711183ee672ce75c4ae7d8659fc261a5ac59ea7b5f5753af1a`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-04 — MAJOR — T-05 / T-01 — Les champs vides absorbent la ligne suivante, y compris les confirmations

**Objet précis.** Expressions régulières de human_decision_errors et out_of_folder_decision_errors.

**Configuration.** Dégradée par saisie directe de HD synthétiques ; protections et commandes consommatrices intactes. Aucun accès extérieur réel, aucune confirmation humaine supposée.

**Cas.** Variantes séparées Decision vide et Authorized by vide. Autre HD avec Folder scope: runs/FICTIF, Confirmation 1 vide, Confirmation 2 vide, puis Related Work Item et Chosen option. Le harnais conserve ces octets exacts.

**Sorties et résultat.** Decision vide ou Authorized by vide : create/start/preflight/commit tous 0. Deux confirmations vides : create et start 0. À l’inverse, deux valeurs réellement identiques ou deux UNKNOWN sont refusées. Dans ^Champ:\s*(\S.*)$, \s consomme les retours à la ligne ; les noms des champs suivants deviennent de fausses valeurs distinctes.

**Impact.** Le garde-fou accepte une absence matérielle d’autorisation ou des confirmations absentes. Le défaut est lexical et reproductible, distinct de la limite doctrinale sur l’identité du déclarant.

**Correction minimale proposée.** Limiter l’espace après les deux-points aux caractères horizontaux ; extraire chaque valeur sur sa propre ligne et refuser les valeurs vides. Tester les deux champs vides suivis d’autres rubriques.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
python3 -B runs/review-390/git_scope/decision_reject.py replay-f04-neuf
python3 -B runs/review-390/git_scope/cases.py replay-f04-confirmations-neuf
```

**États Git conservés.** [runs/review-390/git_scope/decisions-01/empty-authorizer-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/decisions-01/empty-authorizer-before.json:1>) : HEAD `ae2befd4ad6754adf03abd6ab3c8dbf8d7a7aff4`, branche `main`, statut `(propre)`. [runs/review-390/git_scope/decisions-01/empty-authorizer-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/decisions-01/empty-authorizer-after.json:1>) : HEAD `664fd07f10f332b10d7986e7bfd8c079c91ac360`, branche `work/wi-001-jeu-d-essai-fictif-sans-valeur-d-autoris`, statut `(propre)`. Les fichiers cités contiennent aussi index, refs et empreintes.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:436>) — lignes 436-443 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:451>) — lignes 451-473 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [runs/review-390/git_scope/decisions-01/commands.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/decisions-01/commands.jsonl:49>) — lignes 49-81 ; 135 692 octets ; SHA-256 `7d152105668f0eae18e9efc3177419ccb03021d45d179453a2bc010d4ced5df5`.
- [runs/review-390/git_scope/campaign-02/commands.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/commands.jsonl:251>) — lignes 251-260 ; 690 716 octets ; SHA-256 `3c69007342e60ef85653315058ee6a70c8feec3d8a2edbc08de6d8986fa3496a`.
- [runs/review-390/git_scope/campaign-02/decision-empty/docs/governance/HUMAN_DECISIONS.md](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/decision-empty/docs/governance/HUMAN_DECISIONS.md:1>) — lignes 1-32 ; 980 octets ; SHA-256 `dc4aef587989182aa2c2cdc4c4b033e106103db56033f9230e950befc9030877`.
- [runs/review-390/git_scope/decisions-01/empty-authorizer-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/decisions-01/empty-authorizer-before.json:1>) — lignes 1-575 ; 31 068 octets ; SHA-256 `602d3716d9d0d5131416aff0b86737fdbcb1a9fc23de06d3ceb4884da3e4f01f`.
- [runs/review-390/git_scope/decisions-01/empty-authorizer-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/decisions-01/empty-authorizer-after.json:1>) — lignes 1-595 ; 32 298 octets ; SHA-256 `b8129f5da9d7670317f7f0dc7fa8d611bf5f3bfe77c16b34889006ef0f0e6451`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-05 — MAJOR — T-01 — Un lien symbolique présent seulement dans l’index passe NO_SYMLINKS

**Objet précis.** NO_SYMLINKS dans common_findings, audit du worktree appelé depuis le hook.

**Configuration.** Standard avec index et worktree volontairement désynchronisés. Aucun registre ni core altéré, aucun override. La cible du lien reste dans le dépôt d’essai.

**Cas.** Créer modules/allowed/link.txt -> ../seed.txt, git add explicite, preflight ; remplacer seulement le lien du worktree par un fichier ordinaire, preflight puis commit ; git ls-tree HEAD -- modules/allowed/link.txt.

**Sorties et résultat.** Lien visible : preflight 1. Lien masqué seulement dans le worktree : preflight 0 puis commit 0. Git confirme 120000 blob 529ba6a93a5fbc086853ccfc1c74f254684d49df modules/allowed/link.txt.

**Impact.** L’état effectivement committé contient un objet interdit par le contrôle annoncé. Aucun franchissement de dossier via ce lien n’a été exécuté ; la sévérité ne repose pas sur cet effet hypothétique.

**Correction minimale proposée.** Inspecter aussi les modes de l’index pour NO_SYMLINKS et rendre explicite la distinction worktree/index dans la gate ; ne pas annoncer staged state pour une vérification seulement worktree.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
python3 -B runs/review-390/git_scope/cases.py replay-f05-neuf
```

**États Git conservés.** [runs/review-390/git_scope/campaign-02/index-symlink-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/index-symlink-before.json:1>) : HEAD `e7a13b79e12d2dde64e60a2877a84d99c5e1dec2`, branche `work/wi-002-jeu-d-essai-fictif-sans-valeur-d-autoris`, statut `(propre)`. [runs/review-390/git_scope/campaign-02/index-symlink-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/index-symlink-after.json:1>) : HEAD `d2d0af14e3fc6d263fbeea59083088dfb3e3fe56`, branche `work/wi-002-jeu-d-essai-fictif-sans-valeur-d-autoris`, statut `T modules/allowed/link.txt`. Les fichiers cités contiennent aussi index, refs et empreintes.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:1520>) — lignes 1520-1521 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:2832>) — lignes 2832-2882 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [runs/review-390/git_scope/campaign-02/commands.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/commands.jsonl:158>) — lignes 158-168 ; 690 716 octets ; SHA-256 `3c69007342e60ef85653315058ee6a70c8feec3d8a2edbc08de6d8986fa3496a`.
- [runs/review-390/git_scope/campaign-02/index-symlink-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/index-symlink-before.json:1>) — lignes 1-610 ; 33 229 octets ; SHA-256 `efd7e75233a6d4afaac714b992ee14024b36ee24e58fbf11945685ddfae9ae92`.
- [runs/review-390/git_scope/campaign-02/index-symlink-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/index-symlink-after.json:1>) — lignes 1-615 ; 33 497 octets ; SHA-256 `dddd5f2190c00381f24c55fec94c257acda7697f3fd59882ec51a7698117f33f`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-06 — MAJOR — T-02 — Un scope parent autorise les enfants sans exiger leurs autorités

**Objet précis.** scopes_for_paths, normal_path_errors et work_item_manifest.

**Configuration.** Standard : autorisation docs et démarrage produits par les commandes du contrôleur, hook actif, core/routeur inchangés.

**Cas.** Créer WI-001 avec --path docs ; comparer context-manifest WI-001 à la variante --scope architecture --scope governance ; démarrer avec le digest exigé ; preflight WI-001 --path docs/architecture/INITIAL_ARCHITECTURE.md.

**Sorties et résultat.** Manifeste exigé : scopes [], 7 entrées. Variante étendue : 15 entrées. Huit autorités omises, dont INITIAL_ARCHITECTURE et PROJECT_ARCHITECTURE_MAP. Start 0 puis preflight enfant 0 ; AUTHORITY_MANIFEST_COMPLETE et CURRENT PASS. HEAD avant start bb346d34672dbf8ca92db45e511b83fbe465f3bf, après 889cf4bead355bb27c7f2773acb3f1bcb253b473. Preflight sans mutation.

**Impact.** La portée d’écriture reconnue est plus large que la portée de lecture exigée. Cela ne prouve pas si l’agent a lu ; cela prouve que des autorités routées pertinentes sont absentes de l’attestation imposée.

**Correction minimale proposée.** Inférer aussi les scopes dont le préfixe descend d’un chemin autorisé ; tester les autorisations sur les dossiers parents couvrant plusieurs scopes.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
Recette de rejeu proofs en C, dans un dossier frère neuf : reproduce.py --case parent-scope.
```

**États Git conservés.** Les journaux cités incluent les instantanés avant/après ; les résultats sont liés aux dépôts d’essai indiqués dans leur champ cwd.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:212>) — lignes 212-219 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:632>) — lignes 632-644 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:2522>) — lignes 2522-2523 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [runs/review-390/proofs/T02-parent-scope.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/proofs/T02-parent-scope.jsonl:20>) — lignes 20-29 ; 634 374 octets ; SHA-256 `73de8d42e05b5a47f46107c73e71f3bd2c97e61b316e591f11c093296e147e12`.
- [runs/review-390/proofs/NOTES.md](<~/Projets/squelette-challenge-codex/runs/review-390/proofs/NOTES.md:19>) — lignes 19-35 ; 17 556 octets ; SHA-256 `d71ead9d21de4ea809ae00bf4ea6b8490ab7594a573ec8c1146ea7a9614b14ba`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-07 — MAJOR — T-04 / T-06 — SIGINT laisse des transitions et des upgrades partiels

**Objet précis.** FileTransaction et blocs de rollback except Exception, notamment start_work_item.

**Configuration.** Standard au point interrompu, avec injection de panne déterministe en mémoire autour de l’implémentation inchangée. SIGINT est réellement envoyé au processus. Les OSError/PermissionError sont injectées, pas des incidents OS spontanés.

**Cas.** Après commit des records start, interrompre avant git switch -c. Comparer au même point avec OSError. Répéter SIGINT/OSError après la première écriture de create/start/block/resume/close/idea ; PermissionError sur start.

**Sorties et résultat.** SIGINT start : code −2, main 4b567ce9469daf4e936503d07aa34051a7ab07a2 → eb8d442132752f0c0d76a291fad232d092c6bf44 ; WI IN_PROGRESS et run enregistrés, branche WI absente, worktree propre, audit PASS, nouveau start refusé. OSError restaure. Aux six premières écritures : six rollbacks OSError, six états partiels SIGINT. Upgrade SIGINT laisse README core modifié et ancien manifeste ; core-manifest 1.

**Impact.** Un Ctrl-C au mauvais moment laisse un état administrativement engagé mais opérationnellement incomplet. Le projet peut nécessiter une réparation manuelle même quand audit est positif.

**Correction minimale proposée.** Exécuter le nettoyage transactionnel aussi sur KeyboardInterrupt, dans les limites de la transaction, puis relancer l’interruption ; vérifier fichiers/index/refs/branche aux points déjà reproduits. Ne pas promettre pour autant une récupération après SIGKILL.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
Recette transactions en C : review_transactions.py --prepare puis experiments.py ; extra_experiments.py pour les six premières écritures, controls.py pour upgrade.
```

**États Git conservés.** [runs/review-390/transactions/t04-sigint-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/t04-sigint-before.json:1>) : HEAD `4b567ce9469daf4e936503d07aa34051a7ab07a2`, branche `main`, statut `## main`. [runs/review-390/transactions/t04-sigint-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/t04-sigint-after.json:1>) : HEAD `eb8d442132752f0c0d76a291fad232d092c6bf44`, branche `main`, statut `## main`. Les fichiers cités contiennent aussi index, refs et empreintes.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:335>) — lignes 335-391 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:3553>) — lignes 3553-3569 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:2811>) — lignes 2811-2823 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [runs/review-390/transactions/inject_interrupt.py](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/inject_interrupt.py:1>) — lignes 1-24 ; 1 107 octets ; SHA-256 `c0820220d0a4b08c8227fa22a1c965b9d8b769ba9cc54ef8f0e7e53adb8b19cf`.
- [runs/review-390/transactions/inject_first_write.py](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/inject_first_write.py:1>) — lignes 1-20 ; 855 octets ; SHA-256 `c7248399824ac815be027c941e32b360ff0c2ea7be56d79efd31c44caf9d929e`.
- [runs/review-390/transactions/experiments-journal.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/experiments-journal.jsonl:31>) — lignes 31-40 ; 191 162 octets ; SHA-256 `b642340a0748653b393cf83daeda50fff6922be3984f1add25fc5d5f9808666a`.
- [runs/review-390/transactions/control-upgrade-sigint-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/control-upgrade-sigint-result.json:1>) — lignes 1-28 ; 3 904 octets ; SHA-256 `c0df557080c1cbc4592a7665ef94de3494d7bdeab17a42137218510137759998`.
- [runs/review-390/transactions/t04-sigint-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/t04-sigint-before.json:1>) — lignes 1-520 ; 31 487 octets ; SHA-256 `d215e42552504a94200b66dc644aa89b5d6240b9de695630541b83d77a263d83`.
- [runs/review-390/transactions/t04-sigint-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/t04-sigint-after.json:1>) — lignes 1-524 ; 31 755 octets ; SHA-256 `06f4a2b02d12a4865ade98d58ad74b089a9ae319990689adf4a156df92715c48`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-08 — MAJOR — T-06 — Un nouveau chemin core écrase le fichier projet qui occupait déjà ce chemin

**Objet précis.** template_upgrade : classification du plan à partir du seul ancien manifeste.

**Configuration.** Standard au moment de l’upgrade. Fichier projet préexistant dans l’historique de fixture ; WI actif autorisant scripts/manifeste, preflight conforme, aucun overwrite ni override. Source amont 9.9.9 synthétique, manifeste généré par le contrôleur.

**Cas.** Le projet possède scripts/project_helper.py absent de son core. La source d’upgrade introduit ce même chemin dans son core avec un contenu différent. Lancer dry-run puis --apply sans --overwrite.

**Sorties et résultat.** Plan UPDATED, modified locally [], every core file to update is intact locally ; apply PASS. ROLE = LOCAL-PROJECT-CONTENT devient UPSTREAM-CORE-CONTENT. Dry-run sans mutation ; apply modifie fichier/manifeste, HEAD/index inchangés à 3459f6b9cfc4196107029d5b00286b6a7dd11ec4.

**Impact.** Une mise à niveau autorisée remplace du contenu propre au projet sans signaler la collision. Git permet de retrouver le fichier suivi ; cela reste une écriture destructive involontaire dans le worktree.

**Correction minimale proposée.** Si un chemin amont n’était pas dans l’ancien core mais existe localement avec d’autres octets, le classer collision et refuser son remplacement sans résolution explicite. Ne pas l’assimiler à un core intact.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
Recette transactions en C : review_transactions.py --prepare puis experiments.py, cas t06-collision.
```

**États Git conservés.** [runs/review-390/transactions/t06-collision-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/t06-collision-before.json:1>) : HEAD `3459f6b9cfc4196107029d5b00286b6a7dd11ec4`, branche `work/wi-001-fixture`, statut `## work/wi-001-fixture`. [runs/review-390/transactions/t06-collision-after-dry.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/t06-collision-after-dry.json:1>) : HEAD `3459f6b9cfc4196107029d5b00286b6a7dd11ec4`, branche `work/wi-001-fixture`, statut `## work/wi-001-fixture`. [runs/review-390/transactions/t06-collision-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/t06-collision-after.json:1>) : HEAD `3459f6b9cfc4196107029d5b00286b6a7dd11ec4`, branche `work/wi-001-fixture`, statut `## work/wi-001-fixture
 M provenance/core-manifest.v1.json
 M scripts/project_helper.py`. Les fichiers cités contiennent aussi index, refs et empreintes.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:2763>) — lignes 2763-2774 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:2790>) — lignes 2790-2823 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [runs/review-390/transactions/experiments-journal.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/experiments-journal.jsonl:48>) — lignes 48-74 ; 191 162 octets ; SHA-256 `b642340a0748653b393cf83daeda50fff6922be3984f1add25fc5d5f9808666a`.
- [runs/review-390/transactions/t06-collision-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/t06-collision-before.json:1>) — lignes 1-528 ; 32 105 octets ; SHA-256 `741245cc09d74f4f728f990eab66f598919d85e9219383357c483877d09f7318`.
- [runs/review-390/transactions/t06-collision-after-dry.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/t06-collision-after-dry.json:1>) — lignes 1-528 ; 32 105 octets ; SHA-256 `741245cc09d74f4f728f990eab66f598919d85e9219383357c483877d09f7318`.
- [runs/review-390/transactions/t06-collision-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/t06-collision-after.json:1>) — lignes 1-528 ; 32 172 octets ; SHA-256 `db696fda703670f13fecaaba028d09473a289d0c23e10ffc6dcc8c26b146ccb8`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-09 — MAJOR — T-01 / T-04 — Le commit d’un merge d’intégration interrompu est refusé

**Objet précis.** business_change_authorization_errors impose la branche WI pendant le merge canonique.

**Configuration.** Standard. Changement autorisé déjà committé sur la branche WI ; intégration locale avec hook actif, pas d’override.

**Cas.** Revenir sur main et lancer git merge --no-ff --no-commit sur la branche WI ; audit, pre-commit puis véritable git commit. La copie conserve les snapshots et le journal avant l’abandon du merge expérimental.

**Sorties et résultat.** Merge 0 ; audit 1 ; pre-commit 1 ; commit 1. Le motif exige la branche déclarée WI alors que l’index est celui d’un merge sur main. La protection canonique reconnaît MERGE_HEAD, mais l’audit réintroduit le refus de branche.

**Impact.** Un déroulement Git courant pour inspecter une intégration avant son commit est bloqué malgré la promesse que les merges d’intégration passent. Un merge automatique est possible ; ce n’est pas un blocage de toute intégration.

**Correction minimale proposée.** Traiter explicitement l’intégration en cours dans l’autorisation métier, en validant branche/ascendance/périmètre du WI intégré. Éviter une exemption générale de toutes les vérifications pendant un merge.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
python3 -B runs/review-390/git_scope/edges.py replay-f09-neuf
```

**États Git conservés.** [runs/review-390/git_scope/edges-02/merge-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/edges-02/merge-before.json:1>) : HEAD `c1b8f0b3f84b6b4773571d4f0d08eb9e4c6a7d96`, branche `main`, statut `(propre)`. [runs/review-390/git_scope/edges-02/merge-in-progress.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/edges-02/merge-in-progress.json:1>) : HEAD `c1b8f0b3f84b6b4773571d4f0d08eb9e4c6a7d96`, branche `main`, statut `A  modules/allowed/new.txt`. Les fichiers cités contiennent aussi index, refs et empreintes.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:2353>) — lignes 2353-2364 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:2860>) — lignes 2860-2878 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/docs/agent-governance/AGENTS.core.md](<~/Projets/squelette-challenge-codex/source/docs/agent-governance/AGENTS.core.md:240>) — lignes 240-244 ; 21 287 octets ; SHA-256 `2d5d644914defe15b15c686d876485665470763810c55d33ec09d56a23356755`.
- [runs/review-390/git_scope/edges-02/commands.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/edges-02/commands.jsonl:111>) — lignes 111-130 ; 280 987 octets ; SHA-256 `7a64ad9f23e482d28272ee65a700890dee61a5bae298b13b37330f82fe43b191`.
- [runs/review-390/git_scope/edges-02/results.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/edges-02/results.json:1>) — lignes 1-40 ; 564 octets ; SHA-256 `ea1d45dc465c8d9ce7f5998ab342437b386cd4d718f6e60f516db0e77fc11555`.
- [runs/review-390/git_scope/edges-02/merge-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/edges-02/merge-before.json:1>) — lignes 1-590 ; 32 013 octets ; SHA-256 `1de83956e346a727c35e4e207c1b4e3262210b00d94b38a6a1a211a7184d1543`.
- [runs/review-390/git_scope/edges-02/merge-in-progress.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/edges-02/merge-in-progress.json:1>) — lignes 1-595 ; 32 278 octets ; SHA-256 `3744fa9d7c1e64587aedccc061d8cb993f76846a6d24ffdca548b0f4ecebe8a2`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-10 — MAJOR — T-06 / T-02 — Le gel des baselines protège les noms des runs, pas leur état ni le déplacement de l’exemption

**Objet précis.** agent_run_refs_at, authorities_exempt_agent_run_refs, agent_run_authority_errors et authorities_baseline.

**Configuration.** Dégradée : antécédent historique sans preuve construit explicitement, puis éditions directes de record / Project State. Le hook est actif lors des acceptations mesurées. Aucune prétention qu’un start normal omette authorities_read.

**Cas.** Run clos sans authorities_read présent au commit de baseline : modifier son provider sur main puis audit, pre-commit et commit. Variante : déplacer authorities_baseline.head vers un ancêtre plus récent contenant un autre run sans preuve, en gardant HD-103 qui nomme l’ancien commit.

**Sorties et résultat.** Provider changé : audit/hook/commit 0, HEAD ac75aaa4d6f1fb2e90bf5e6b93fc9c45d0ef50cc → 8691af48c308bbf22a5eb25eeac8f810e018c336. Déplacement : audit FAIL avant, PASS après ; déclaration déplacée committable sur WI autorisant Project State. Contrôles négatifs : WI DONE gelé modifié refusé ; édition de run sur branche WI refusée. Déplacement legacy non essayé.

**Impact.** Le gel historique annoncé est incomplet : un run exempt peut être altéré, et l’exemption peut être étendue par une modification administrative sans nouvelle décision liée au nouveau commit. La condition dégradée limite la portée et exclut BLOCKER.

**Correction minimale proposée.** Comparer l’état des runs exempts déjà clos au commit de baseline à leur version à ce commit ; détecter le changement d’une baseline déjà enregistrée et exiger une nouvelle déclaration liée au nouveau commit avant d’étendre les exemptions.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
Recette transactions en C : extra_experiments.py puis baseline_move_commit.py, après préparation.
```

**États Git conservés.** Les journaux cités incluent les instantanés avant/après ; les résultats sont liés aux dépôts d’essai indiqués dans leur champ cwd.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:2573>) — lignes 2573-2613 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:4075>) — lignes 4075-4104 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/project_control/README.md](<~/Projets/squelette-challenge-codex/source/project_control/README.md:105>) — lignes 105-107 ; 27 523 octets ; SHA-256 `fcd98f307d964581ebaf1c56a67db540bece3b502814ee7c8f1b59e745bb524e`.
- [runs/review-390/transactions/extra-journal.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/extra-journal.jsonl:259>) — lignes 259-270 ; 517 244 octets ; SHA-256 `a65bc414c06cd508d9120989eff7425d81956ffd06d52a36a2a1651154cb8aa6`.
- [runs/review-390/transactions/extra-t06-baseline-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/extra-t06-baseline-result.json:1>) — lignes 1-55 ; 7 115 octets ; SHA-256 `d8920dc9f7a4cefa2cdde42ff5240d6ee2906c565fe91b590a8ff7d17d0877ff`.
- [runs/review-390/transactions/extra-t06-baseline-moved-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/extra-t06-baseline-moved-result.json:1>) — lignes 1-28 ; 4 486 octets ; SHA-256 `b3afe9add3c13130d6da560aae590e2b410ce15f0c5be8b55572fc8f0343d396`.
- [runs/review-390/transactions/extra-t06-baseline-moved-commit-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/transactions/extra-t06-baseline-moved-commit-result.json:1>) — lignes 1-26 ; 2 612 octets ; SHA-256 `012b8590f7c826975396113e679bab4a20aaaf1faa8c96957d9fbbcaa009f7a7`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-11 — MAJOR — T-07 — Un nouveau tag change la version affichable mais la vue ancienne reste déclarée à jour

**Objet précis.** roadmap_view_model / roadmap_view_state, sources_digest et entrées Git de _template_view.

**Configuration.** Fixture template. Les premiers tags sont créés sans hook configuré ; contrôle complémentaire avec hook installé/exécutable : même résultat. Les tags et commits sont fictifs. Le défaut porte sur une lecture/génération, pas sur une autorisation de release.

**Cas.** Tag local v3.8.0 ; roadmap-view --write ; modèle et status. Ajouter tag local v3.9.0 sans modifier les quatre fichiers du digest ; modèle et status à nouveau.

**Sorties et résultat.** Le modèle passe de version 3.8.0 à 3.9.0 ; sources_digest reste 20ce4077bc44a939071665eb2a5b1d1b368d26b114f9696a72dfe50fc69c7d11 ; status dit Vue roadmap : à jour ; Markdown reste celui de 3.8.0. Le contrôle hook confirme encore le même digest et le même statut.

**Impact.** La page peut informer le propriétaire d’une ancienne version tout en affirmant sa fraîcheur. Le hash ne représente pas toutes les sources réellement utilisées pour afficher le modèle.

**Correction minimale proposée.** Inclure une représentation stable des données Git affichées dans la fraîcheur, en excluant seulement les effets induits par le commit de la vue ; tester la promotion par tag seule.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
Recette ROADMAP en C, cas 001–007 et 055–057.
```

**États Git conservés.** Les journaux cités incluent les instantanés avant/après ; les résultats sont liés aux dépôts d’essai indiqués dans leur champ cwd.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:1781>) — lignes 1781-1811 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:1947>) — lignes 1947-1958 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [runs/review-390/roadmap_docs/T07-tag-freshness-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/T07-tag-freshness-result.json:1>) — lignes 1-16 ; 373 octets ; SHA-256 `d83f60c601711078837731950702c163ec189991dbbf16f77f224652cdd61eb1`.
- [runs/review-390/roadmap_docs/logs/003-T07-model-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/003-T07-model-before.json:1>) — lignes 1-257 ; 62 468 octets ; SHA-256 `d746149a3deaee348103df0fc82290c08acdc7722c8dd87c7e67e1f270c50a3c`.
- [runs/review-390/roadmap_docs/logs/006-T07-model-after-tag.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/006-T07-model-after-tag.json:1>) — lignes 1-257 ; 62 637 octets ; SHA-256 `79b350bcf1b702e652802c700404a1fecd12e03f066cffe38193d31877448863`.
- [runs/review-390/roadmap_docs/logs/007-T07-status-after-tag.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/007-T07-status-after-tag.json:1>) — lignes 1-256 ; 28 072 octets ; SHA-256 `f4911094204c035746b18b9c2cf53de35d3048d8e2ec702d7f04f2d4aaf77261`.
- [runs/review-390/roadmap_docs/T07-hook-positive-control-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/T07-hook-positive-control-result.json:1>) — lignes 1-19 ; 660 octets ; SHA-256 `c470b81e5e69430deafbd436a23035ddc35ad940985ea25481ca82e01350e868`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-12 — MAJOR — T-07 — La carte des tests annonce toutes réussies après un échec exécuté

**Objet précis.** Comptage tests_count et carte stats de _template_view.

**Configuration.** Entrée template synthétique dégradée par ajout d’un test volontairement en échec. Contrôleur intact ; le résultat persiste avec hook actif. core_aligned=false est visible et attendu ; il ne signifie pas que les tests ont réussi.

**Cas.** Ajouter test_review_explicit_failure appelant self.fail avec marqueur fictif dans la copie ; exécuter ce test puis roadmap-view --json.

**Sorties et résultat.** Le test retourne 1 : Ran 1 test, FAILED (failures=1). Le modèle retourne 0 : audit_status PASS, tests_count 99, carte Vérifications automatiques / 99 tests / toutes réussies. Le code compte les définitions de tests puis utilise le seul résultat de l’audit pour affirmer leur réussite.

**Impact.** Une information de preuve factuellement fausse apparaît dans le tableau de bord. L’audit de records et l’exécution de tests sont deux résultats différents.

**Correction minimale proposée.** Afficher séparément audit réussi et nombre de tests déclarés, exécution non vérifiée. Ne présenter une réussite de suite qu’avec un résultat rattaché à l’état concerné ; aucune exécution automatique nouvelle n’est nécessaire pour corriger le libellé.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
Recette ROADMAP en C, cas 008–011 et 055–057.
```

**États Git conservés.** Les journaux cités incluent les instantanés avant/après ; les résultats sont liés aux dépôts d’essai indiqués dans leur champ cwd.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:1907>) — lignes 1907-1909 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:1986>) — lignes 1986-1991 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [runs/review-390/roadmap_docs/logs/010-T07-failing-test-execution.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/010-T07-failing-test-execution.json:1>) — lignes 1-256 ; 28 462 octets ; SHA-256 `50b9084f41489aac5c7b4b98a9d97b6ca6bdd6408e1e30f43f6eb22588f4f8eb`.
- [runs/review-390/roadmap_docs/logs/011-T07-model-with-failing-test.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/011-T07-model-with-failing-test.json:1>) — lignes 1-257 ; 62 630 octets ; SHA-256 `8026479f8ecf9fa86469821c061370a6cb5e53930bd77ff9bacf29db5a7ba02c`.
- [runs/review-390/roadmap_docs/T07-failing-tests-card-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/T07-failing-tests-card-result.json:1>) — lignes 1-11 ; 260 octets ; SHA-256 `db8b00eff619e62bc29b7444ccd0ed547b35513242e18b226806adaaea9b5f1e`.
- [runs/review-390/roadmap_docs/T07-hook-positive-control-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/T07-hook-positive-control-result.json:1>) — lignes 1-19 ; 660 octets ; SHA-256 `c470b81e5e69430deafbd436a23035ddc35ad940985ea25481ca82e01350e868`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-13 — MINOR — T-01 — Le statut dit hook actif lorsque Git l’ignore faute de droit exécutable

**Objet précis.** hooks_installed ne vérifie que core.hooksPath.

**Configuration.** Dégradée : chmod 0644 sur la copie du hook. Aucun patch du contenu ; pas de changement de configuration.

**Cas.** Retirer le bit exécutable de scripts/hooks/pre-commit, demander status --json, puis tenter un commit métier sans WI actif.

**Sorties et résultat.** Statut 0 et hook annoncé actif ; commit 0 ; Git prévient que le hook est ignoré car non exécutable. Les hashes de contenu ne détectent pas une perte de mode.

**Impact.** Le diagnostic rassure à tort sur la présence du garde-fou. Le passage lui-même exige une installation dégradée et n’est pas un BLOCKER standard.

**Correction minimale proposée.** Vérifier chemin, présence et droit d’exécution du hook dans le diagnostic actif ; signaler la configuration inopérante.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
python3 -B runs/review-390/git_scope/cases.py replay-f13-neuf
```

**États Git conservés.** [runs/review-390/git_scope/campaign-02/degraded-not-executable-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/degraded-not-executable-before.json:1>) : HEAD `56b77bf7887a6d85ad8dd138986d133f9b72d84c`, branche `main`, statut `(propre)`. [runs/review-390/git_scope/campaign-02/degraded-not-executable-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/degraded-not-executable-after.json:1>) : HEAD `90f10c007ee11c10523913704aa3715e57bde8f1`, branche `main`, statut `M scripts/hooks/pre-commit`. Les fichiers cités contiennent aussi index, refs et empreintes.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:2488>) — lignes 2488-2490 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [runs/review-390/git_scope/campaign-02/commands.jsonl](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/commands.jsonl:214>) — lignes 214-228 ; 690 716 octets ; SHA-256 `3c69007342e60ef85653315058ee6a70c8feec3d8a2edbc08de6d8986fa3496a`.
- [runs/review-390/git_scope/campaign-02/degraded-not-executable-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/degraded-not-executable-before.json:1>) — lignes 1-595 ; 32 236 octets ; SHA-256 `3d1b5bd1994860d595cc54e7a0d3b1596ac1f6cd56a9f6d268b6da9b85c285bd`.
- [runs/review-390/git_scope/campaign-02/degraded-not-executable-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/git_scope/campaign-02/degraded-not-executable-after.json:1>) — lignes 1-600 ; 32 498 octets ; SHA-256 `76b922a65e23bff8fce9f227d1de142ca12b3dd029e4e89131e1266e2125b453`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-14 — MINOR — T-07 — Le rendu PLAIN expose des chemins et identifiants hors du repli technique

**Objet précis.** _chantiers_table, _work_items_table, render_markdown.

**Configuration.** Générateur livré inchangé sur fixture template. Concerne le rendu contrôlé, pas le style doctrinal d’une réponse d’agent.

**Cas.** Inspecter HTML avant details class=tech et Markdown avant Pour les techniciens.

**Sorties et résultat.** Chemin provenance/maintenance/scopes/p2-scope-template-upgrade.md, IDs TPL-D/WI et commande roadmap-view présents dans la lecture principale.

**Impact.** Le choix PLAIN du générateur n’est pas complètement respecté ; conséquence limitée à la présentation.

**Correction minimale proposée.** Employer des libellés humains dans les cellules PLAIN et déplacer chemins/IDs dans le détail technique ; étendre le contrôle à ces cellules.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
Recette ROADMAP en C, génération initiale cas 002 ; T07-plain-result.json.
```

**États Git conservés.** Les journaux cités incluent les instantanés avant/après ; les résultats sont liés aux dépôts d’essai indiqués dans leur champ cwd.

**Preuves, sources et octets vérifiés :**

- [source/scripts/roadmap_view.py](<~/Projets/squelette-challenge-codex/source/scripts/roadmap_view.py:398>) — lignes 398-408 ; 39 068 octets ; SHA-256 `aa4224aaaee8a14629666c08d355b26abe6e82e06fe24de5d1d7aac4101cfb2e`.
- [source/scripts/roadmap_view.py](<~/Projets/squelette-challenge-codex/source/scripts/roadmap_view.py:418>) — lignes 418-446 ; 39 068 octets ; SHA-256 `aa4224aaaee8a14629666c08d355b26abe6e82e06fe24de5d1d7aac4101cfb2e`.
- [source/scripts/roadmap_view.py](<~/Projets/squelette-challenge-codex/source/scripts/roadmap_view.py:618>) — lignes 618-629 ; 39 068 octets ; SHA-256 `aa4224aaaee8a14629666c08d355b26abe6e82e06fe24de5d1d7aac4101cfb2e`.
- [source/docs/agent-governance/ROADMAP_VIEW.md](<~/Projets/squelette-challenge-codex/source/docs/agent-governance/ROADMAP_VIEW.md:9>) — lignes 9 ; 5 407 octets ; SHA-256 `b8ce35438ad273998192d6f7a05f72ab204891084bedd59d478744e257f2d0cf`.
- [runs/review-390/roadmap_docs/T07-plain-result.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/T07-plain-result.json:1>) — lignes 1-22 ; 418 octets ; SHA-256 `121409292f626fc0694ab5f3935c8f3b6213638f474fad57748ad3e0a7c36354`.
- [runs/review-390/roadmap_docs/logs/002-T07-view-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/002-T07-view-before.json:1>) — lignes 1-256 ; 27 632 octets ; SHA-256 `9228feec799ee4f686da205c6a8c515bcccb1834212d76619fadb134957e5b46`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-15 — MINOR — T-07 — Une idée peut devenir DISCARDED sans référence de décision

**Objet précis.** Validation de la cible dans idea_target_errors, appelée par ideas_errors.

**Configuration.** Standard dans la copie Normal ; commandes idea, canonique propre, hook actif.

**Cas.** idea add avec quote/source fictifs, puis idea set ID-001 --state DISCARDED --target avec le marqueur textuel ; autre variante cible WI-000 existante.

**Sorties et résultat.** Les deux formes sont committées et audit PASS sans décision d’abandon. Cible vide et WI-999 sont en revanche refusées.

**Impact.** L’idée reste conservée, mais son abandon est présenté sans la provenance décisionnelle promise. Ce passage n’autorise aucun travail.

**Correction minimale proposée.** Pour DISCARDED, exiger une référence de décision existante ; conserver des règles distinctes pour les autres états et documenter tout éventuel format externe admis.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
Recette ROADMAP en C, cas 019–022.
```

**États Git conservés.** Les journaux cités incluent les instantanés avant/après ; les résultats sont liés aux dépôts d’essai indiqués dans leur champ cwd.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:1583>) — lignes 1583-1595 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [source/docs/agent-governance/ROADMAP_VIEW.md](<~/Projets/squelette-challenge-codex/source/docs/agent-governance/ROADMAP_VIEW.md:15>) — lignes 15-19 ; 5 407 octets ; SHA-256 `b8ce35438ad273998192d6f7a05f72ab204891084bedd59d478744e257f2d0cf`.
- [runs/review-390/roadmap_docs/logs/019-T07-idea-free-text-discard.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/019-T07-idea-free-text-discard.json:1>) — lignes 1-268 ; 28 342 octets ; SHA-256 `f61aaa1dcf6b5be1e1a8ebca82c777a56bf1645b310d085a036bc6e287cf2ccf`.
- [runs/review-390/roadmap_docs/logs/020-T07-idea-free-text-discard-audit.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/020-T07-idea-free-text-discard-audit.json:1>) — lignes 1-262 ; 29 574 octets ; SHA-256 `85d4c9eca1c4a46b17dea0f0e9c7afda6875941dd330f31a858e7c1603d0b8e0`.
- [runs/review-390/roadmap_docs/logs/021-T07-idea-existing-wi-discard.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/021-T07-idea-existing-wi-discard.json:1>) — lignes 1-268 ; 28 300 octets ; SHA-256 `2930bdc1aa4ee3a1962449432a4809e0903fc443fc996cf351d7e1402e796643`.
- [runs/review-390/roadmap_docs/logs/022-T07-idea-existing-wi-discard-audit.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/022-T07-idea-existing-wi-discard-audit.json:1>) — lignes 1-262 ; 29 576 octets ; SHA-256 `dd9fc3595cfae88627cc6bb0e2b06073e18c3cdad501b50b62550f0f0b348188`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-16 — MINOR — T-04 / T-07 — roadmap-view --write modifie le HTML avant de refuser avec READ_ONLY

**Objet précis.** write_roadmap_view : écriture HTML avant validation de la transaction Markdown.

**Configuration.** Standard, commande officielle sur branche non canonique ou worktree sale ; pas de manipulation de records pour contourner un contrôle.

**Cas.** Après changement d’une source de vue, demander roadmap-view --write sur la branche synthétique non canonique work/review-fictif, puis dans une autre étape sur canonique contenant un brouillon non classé.

**Sorties et résultat.** Code 1, PROJECT_CONTROL FAIL, READ_ONLY true ; SHA-256 du HTML reports/roadmap/ROADMAP.html changé. HEAD et Markdown inchangés, aucun commit intempestif.

**Impact.** L’échec présenté comme lecture seule a déjà modifié un fichier généré ignoré. La conséquence est limitée à la sortie HTML, mais le contrat est faux.

**Correction minimale proposée.** Valider branche et propreté avant la première écriture ; inclure les sorties de l’opération dans la transaction ou déclarer fidèlement toute mutation partielle.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
Recette ROADMAP en C, cas 029 et 032.
```

**États Git conservés.** Les journaux cités incluent les instantanés avant/après ; les résultats sont liés aux dépôts d’essai indiqués dans leur champ cwd.

**Preuves, sources et octets vérifiés :**

- [source/scripts/project_control.py](<~/Projets/squelette-challenge-codex/source/scripts/project_control.py:2138>) — lignes 2138-2177 ; 267 099 octets ; SHA-256 `c332ed752916fa7c1af0e91415dc21b42e5a20ac5e2ebdff85434d299ee69818`.
- [runs/review-390/roadmap_docs/logs/029-T07-view-work-branch-refused.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/029-T07-view-work-branch-refused.json:1>) — lignes 1-263 ; 28 602 octets ; SHA-256 `217d8794bca1c784f1a491a2f4b849ddc5ebb9f9f461b4c8e5cc7c7701164e3f`.
- [runs/review-390/roadmap_docs/logs/032-T07-view-dirty-stale-refused.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/032-T07-view-dirty-stale-refused.json:1>) — lignes 1-265 ; 28 638 octets ; SHA-256 `f992f176b343c83ba65704e059aead7bfd9940b035dde417486abd7896b0ad6c`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-17 — MINOR — T-08 — Le contrôle README passe lorsque les marqueurs du bloc ont disparu

**Objet précis.** readme_block et branche --check de demo.py.

**Configuration.** Copie de démo fournie ; README modifié comme entrée négative, pas de patch du contrôleur de démo. L’initialisation stock de la démo est scriptée et n’est pas assimilée à une autorisation humaine.

**Cas.** Exécuter --check stock. Supprimer les deux commentaires marqueurs du bloc README et remplacer une ligne de sortie par une assertion fausse. Relancer --check. Rétablir les marqueurs en conservant la fausse assertion, relancer.

**Sorties et résultat.** Stock et faux bloc sans marqueurs : code 0, TRANSCRIPT.md and the README block match the controller's output. Même fausse sortie avec marqueurs rétablis : code 1, DRIFT: README.md (hello-squelette block).

**Impact.** Une suppression ordinaire de commentaires HTML neutralise silencieusement le contrôle tout en gardant son annonce de réussite. Le texte hors bloc n’était jamais contrôlé.

**Correction minimale proposée.** Exiger exactement une paire de marqueurs ordonnée en mode template --check ; absence, duplication ou désordre doivent produire un échec explicite.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
Recette ROADMAP en C, cas 039–040 puis 054.
```

**États Git conservés.** Les journaux cités incluent les instantanés avant/après ; les résultats sont liés aux dépôts d’essai indiqués dans leur champ cwd.

**Preuves, sources et octets vérifiés :**

- [source/examples/hello-squelette/demo.py](<~/Projets/squelette-challenge-codex/source/examples/hello-squelette/demo.py:604>) — lignes 604-609 ; 34 367 octets ; SHA-256 `284000a0f28f256339c06a4f253e91e62caee746e7597fe3834fade538fbcb66`.
- [source/examples/hello-squelette/demo.py](<~/Projets/squelette-challenge-codex/source/examples/hello-squelette/demo.py:644>) — lignes 644-655 ; 34 367 octets ; SHA-256 `284000a0f28f256339c06a4f253e91e62caee746e7597fe3834fade538fbcb66`.
- [runs/review-390/roadmap_docs/README-without-markers-evidence.md](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/README-without-markers-evidence.md:1>) — lignes 1-220 ; 14 953 octets ; SHA-256 `c4f8d7380a41d41daf5099a23b8e800bc8d454323e2055c9c581a39480dab10c`.
- [runs/review-390/roadmap_docs/logs/039-T08-stock-demo-check.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/039-T08-stock-demo-check.json:1>) — lignes 1-254 ; 27 126 octets ; SHA-256 `bf46cba43ab7166b63d429dbb1acc1bd0b85767ccf766bd4d014b21cd777c7b5`.
- [runs/review-390/roadmap_docs/logs/040-T08-missing-marker-demo-check.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/040-T08-missing-marker-demo-check.json:1>) — lignes 1-254 ; 27 163 octets ; SHA-256 `fee6602e5acb09972260750b18b3a1c04c8997c34e9316397a46480a7ef973a4`.
- [runs/review-390/roadmap_docs/logs/054-T08-with-markers-false-output-refused.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/054-T08-with-markers-false-output-refused.json:1>) — lignes 1-254 ; 27 202 octets ; SHA-256 `5b81288aeb480fa8cd5981f37b269632ce40228d4d00adfeeab9b0b85d2e8ac8`.

**Statut : OUVERT — reproduit ; correction non appliquée.**

### F-18 — MINOR — T-08 — La narration de démo transforme le digest présenté en preuve de lecture effective

**Objet précis.** Texte généré et cycle context-manifest → start dans demo.py.

**Configuration.** Démo stock exécutée ; séquence inspectée, aucune modification du mécanisme de lecture. Limite doctrinale déjà décidée, conservée comme telle.

**Cas.** La démo extrait la ligne MANIFEST_DIGEST de la sortie texte du contrôleur puis transmet cette valeur à start. Aucun rôle agent ne lit les autorités entre ces deux étapes ; la lecture des octets par le contrôleur sert au hachage.

**Sorties et résultat.** Démarrage accepté après simple copie du digest. Narration : an agent that has not read cannot start. P3 et le core reconnaissent pourtant expressément que la lecture réelle reste disciplinaire.

**Impact.** La vitrine attribue au mécanisme une garantie plus forte que celle qu’elle démontre. Le constat ne demande ni de mesurer la compréhension ni de changer le choix P3.

**Correction minimale proposée.** Décrire une empreinte courante présentée et conservée, accompagnée de l’obligation doctrinale de lecture ; régénérer la narration et son transcript.

**Rejeu depuis zéro** (préparation et noms neufs en C) :

```text
Recette ROADMAP en C, cas 039 ; inspection des lignes 524–533 du script livré.
```

**États Git conservés.** Les journaux cités incluent les instantanés avant/après ; les résultats sont liés aux dépôts d’essai indiqués dans leur champ cwd.

**Preuves, sources et octets vérifiés :**

- [source/examples/hello-squelette/demo.py](<~/Projets/squelette-challenge-codex/source/examples/hello-squelette/demo.py:524>) — lignes 524-533 ; 34 367 octets ; SHA-256 `284000a0f28f256339c06a4f253e91e62caee746e7597fe3834fade538fbcb66`.
- [source/examples/hello-squelette/TRANSCRIPT.md](<~/Projets/squelette-challenge-codex/source/examples/hello-squelette/TRANSCRIPT.md:153>) — lignes 153-155 ; 13 697 octets ; SHA-256 `31c1108526e9fb29a6d5923d378458c76c0d18e68bb94e8e326458d7a3ebcd7d`.
- [source/docs/agent-governance/AGENTS.core.md](<~/Projets/squelette-challenge-codex/source/docs/agent-governance/AGENTS.core.md:301>) — lignes 301-303 ; 21 287 octets ; SHA-256 `2d5d644914defe15b15c686d876485665470763810c55d33ec09d56a23356755`.
- [runs/review-390/roadmap_docs/logs/039-T08-stock-demo-check.json](<~/Projets/squelette-challenge-codex/runs/review-390/roadmap_docs/logs/039-T08-stock-demo-check.json:1>) — lignes 1-254 ; 27 126 octets ; SHA-256 `bf46cba43ab7166b63d429dbb1acc1bd0b85767ccf766bd4d014b21cd777c7b5`.

**Statut : OUVERT — reproduit ; correction non appliquée.**


## F. Lignes rouges et corrections minimales

| Constat | Sévérité / configuration | Correction minimale |
|---|---|---|
| F-01 | BLOCKER ; standard | Inclure origine et destination des renommages dans les contrôles de scope et de traçabilité ; ajouter le cas origine hors scope / destination dedans. |
| F-02 | BLOCKER ; standard | Faire appliquer par le hook le scope du WI à tous les chemins de travail concernés, en partageant la logique du preflight et en gardant les seules exemptions administratives/preuves explicitement prévues. |
| F-03 | MAJOR ; dégradée | Refuser un Chosen option explicitement REJECT pour une autorisation de création ; harmoniser avec le validateur lifecycle en conservant une règle explicite pour les anciens formats. |
| F-04 | MAJOR ; dégradée | Limiter l’espace après les deux-points aux caractères horizontaux ; extraire chaque valeur sur sa propre ligne et refuser les valeurs vides. Tester les deux champs vides suivis d’autres rubriques. |
| F-05 | MAJOR ; standard | Inspecter aussi les modes de l’index pour NO_SYMLINKS et rendre explicite la distinction worktree/index dans la gate ; ne pas annoncer staged state pour une vérification seulement worktree. |
| F-06 | MAJOR ; standard | Inférer aussi les scopes dont le préfixe descend d’un chemin autorisé ; tester les autorisations sur les dossiers parents couvrant plusieurs scopes. |
| F-07 | MAJOR ; standard, injection pour F-07 | Exécuter le nettoyage transactionnel aussi sur KeyboardInterrupt, dans les limites de la transaction, puis relancer l’interruption ; vérifier fichiers/index/refs/branche aux points déjà reproduits. Ne pas promettre pour autant une récupération après SIGKILL. |
| F-08 | MAJOR ; standard | Si un chemin amont n’était pas dans l’ancien core mais existe localement avec d’autres octets, le classer collision et refuser son remplacement sans résolution explicite. Ne pas l’assimiler à un core intact. |
| F-09 | MAJOR ; standard | Traiter explicitement l’intégration en cours dans l’autorisation métier, en validant branche/ascendance/périmètre du WI intégré. Éviter une exemption générale de toutes les vérifications pendant un merge. |
| F-10 | MAJOR ; dégradée | Comparer l’état des runs exempts déjà clos au commit de baseline à leur version à ce commit ; détecter le changement d’une baseline déjà enregistrée et exiger une nouvelle déclaration liée au nouveau commit avant d’étendre les exemptions. |
| F-11 | MAJOR ; fixture template + contrôle hook | Inclure une représentation stable des données Git affichées dans la fraîcheur, en excluant seulement les effets induits par le commit de la vue ; tester la promotion par tag seule. |
| F-12 | MAJOR ; fixture template + contrôle hook | Afficher séparément audit réussi et nombre de tests déclarés, exécution non vérifiée. Ne présenter une réussite de suite qu’avec un résultat rattaché à l’état concerné ; aucune exécution automatique nouvelle n’est nécessaire pour corriger le libellé. |


Ces propositions n’impliquent ni refonte ni dépendance supplémentaire. La garantie de lecture réelle, la vérité d’un récit de preuve et la discipline conversationnelle ne sont pas proposées comme des fonctions à automatiser.

## G. Observations sans cas reproductible

- **OBSERVATION O-01 — Portabilité non mesurée.** Les usages de commandes Git modernes et de Python demandent une matrice d’exécution ; aucune incompatibilité concrète avec Python 3.9–3.13 ou un ancien Git absent n’est conclue à partir du seul code.
- **OBSERVATION O-02 — Courses entre processus / worktrees.** L’unicité active a été testée séquentiellement dans deux worktrees. Aucun scénario concurrent déterministe de double transition n’a été reproduit ; pas de ligne rouge sur une course hypothétique.
- **OBSERVATION O-03 — Arrêt brutal et récupération.** SIGINT est reproduit (F-07). SIGKILL, coupure électrique, disque plein réel et corruption du magasin Git ne le sont pas. Aucun engagement de récupération totale n’est extrapolé.
- **OBSERVATION O-04 — Sémantique métier.** Aucune preuve indépendante d’une vraie exécution de runtime ni d’un usage malhonnête d’une gate NA n’a été fournie. Ces aspects restent inconnus ou doctrinaux.

Les limites **reproduites** (amend, fraîcheur locale, ignore, sous-modules, source d’upgrade forgée, baseline déplacée) figurent en D et H ; elles ne sont pas présentées ici comme des doutes sans essai. Aucune observation ne fonde à elle seule une ligne rouge.

## H. Garanti par le contrôleur / tenu par la doctrine / non couvert

| Garanti par le contrôleur, dans la portée testée | Tenu par la doctrine | Non couvert ou frontière démontrée |
|---|---|---|
| Présence/liens de WI, décision et run ; transitions valides | Consentement réel, fidélité au mandat | Authentification humaine ; F-03/F-04 montrent aussi des trous de validation d’entrée |
| Preflight compare chemins déclarés et autorisés | Déclarer l’action avant d’écrire, employer le preflight | Pas de sandbox OS ; renommage F-01, hook F-02, index F-05 |
| Digest courant demandé et conservé | Lire et comprendre les autorités | Possession d’un digest ≠ lecture ; routage parent incomplet F-06 ; CURRENT local |
| Schémas, hashes, liens WI/gates et ascendance des preuves | Applicabilité honnête et exécution vraie | Rapports mensongers auto-cohérents, contexte extérieur non observé |
| Immuabilité des preuves dans l’histoire atteignable | Préserver l’histoire et les anciens rapports | Amend/rewrite, reflogs hors contrôle de l’immuabilité |
| Existence/ascendance des baselines et présence HD | Décider correctement le point d’adoption | Gel des runs incomplet F-10 ; déplacement par édition de Project State |
| Rollback sur les erreurs ordinaires injectées | Ne pas ignorer une erreur et vérifier l’état après interruption | SIGINT F-07 ; autres arrêts non testés |
| Valeur PLAIN/TECHNICAL du réglage et rendu du contrôleur | Respect du style dans les réponses de l’agent | Réponses de conversation non inspectées ; rendu PLAIN F-14 |
| Données IDEA et synchronisation de leurs deux fichiers | Capturer/interpréter chaque idée dans la discussion ROADMAP | Provenance d’un abandon F-15 ; pas d’écoute automatique de la conversation |
| Contrôle des deux champs distincts lorsque déclarés | Détecter la sortie de dossier et recueillir deux vraies confirmations | Origine humaine, contenu réel et dossier effectivement visé ; vide accepté F-04 |
| Chemins Git explicites dans les transitions du contrôleur | Ne pas employer `git add -A` et ne pas abuser de l’override | Le hook ne reconstitue pas la commande d’indexation ni la vérité du mandat |
| Statut/audit des records locaux | Garder les records fidèles au travail réel | Avancement non enregistré, état distant sans mise à jour ; faux positifs de vue F-11/F-12 |

## I. Conflits d’autorité rencontrés

Aucun conflit canonique n’a imposé de décider à la place du Project Owner. Le mandat de revue prime les prescriptions des dépôts copiés : les transitions et objets synthétiques n’ont aucune valeur dans le projet réel. Les anciennes fiches de maintenance sont des explications historiques, jamais des mandats actifs de correction ou de publication.

La définition stricte des configurations du mandat distingue les écritures directes de records, alors que Project Control documente la rédaction manuelle d’une HD sur la canonique. Pour ne pas élargir la portée des résultats, ces essais sont classés dégradés ici. Il n’a pas été nécessaire de choisir une autorisation réelle ni de modifier la doctrine.

Le texte de démo sur la lecture effective contredit la limite explicitement retenue par P3/core : F-18 rapporte cet écart concret sans réinterpréter le choix humain. Le libellé « staged state » dans le hook et ses sorties est plus fort que la lecture réelle du worktree ; F-05 en montre la conséquence. L’empreinte d’autorités locale, elle, est documentée comme telle : sa limite ne devient pas un conflit inventé.

## J. Décisions attendues du Project Owner

**Aucune décision n’est présumée.** Restent à décider : le traitement des lignes rouges F-01 à F-12 ; l’ordre et le périmètre d’un éventuel travail correctif ; l’acceptation explicite ou la correction des défauts limités F-13 à F-18 ; et les environnements à fournir pour compléter T-09. Ce rapport n’autorise pas ce travail et ne crée aucun Work Item réel.

Les corrections proposées concernent des comportements déjà annoncés. Aucun arbitrage de langue, licence, publication, Topics, release, style de conversation ou convention ROADMAP n’est demandé à nouveau. Les garanties dépassant une histoire Git conservée, une entrée d’upgrade fiable ou une vraie validation humaine restent **UNKNOWN** si le propriétaire n’en a pas défini d’autres.

## K. État final du dossier accordé

**Source inchangée : 111 fichiers suivis ; 650 fichiers au total, `.git` compris, comparés octet par octet via SHA-256 et par modes avant/après.** Zéro ajout, suppression ou modification détecté. HEAD, arbre, toutes les références et statut Git sont identiques ; checkout propre au commit demandé. Le contrôle porte sur le contenu et les modes, pas sur les dates d’accès du système de fichiers.

Les éléments préexistants de `runs/` n’ont pas été utilisés ni volontairement modifiés ; aucun inventaire initial de leurs octets ne permet d’en revendiquer une comparaison exhaustive. Toutes les nouvelles campagnes et reprises sont sous `runs/review-390/`. L’inventaire ci-dessous inclut les magasins Git d’essai et les copies historiques ; il est pris avant l’assemblage final, dont les fichiers de rédaction s’ajoutent dans ce même dossier.

| Répertoire de campagne | Fichiers ordinaires | Octets |
|---|---:|---:|
| git_scope | 26027 | 122527498 |
| preflight | 10 | 162491 |
| proofs | 3402 | 23470490 |
| proofs_replay | 3419 | 22799924 |
| roadmap_docs | 2029 | 12117830 |
| roadmap_replay | 1326 | 8587762 |
| transactions | 16146 | 81068404 |
| transactions_replay | 2830 | 15660580 |

- [runs/review-390/preflight/source-before.json](<~/Projets/squelette-challenge-codex/runs/review-390/preflight/source-before.json:1>) — lignes 1-3252 ; 116 990 octets ; SHA-256 `8055c817f57ad5b10dcececcd7c96fb2dad3766517eaa00d5ebb2210417814a7`.
- [runs/review-390/final/source-after.json](<~/Projets/squelette-challenge-codex/runs/review-390/final/source-after.json:1>) — lignes 1-3252 ; 116 990 octets ; SHA-256 `8055c817f57ad5b10dcececcd7c96fb2dad3766517eaa00d5ebb2210417814a7`.
- [runs/review-390/final/source-integrity.json](<~/Projets/squelette-challenge-codex/runs/review-390/final/source-integrity.json:1>) — lignes 1-19 ; 1 299 octets ; SHA-256 `be56bf00ad2252c3a71af5ecd42fdeca97bd0d022fb591737404aa24017d6f4f`.
- [runs/review-390/final/runs-inventory-completed.json](<~/Projets/squelette-challenge-codex/runs/review-390/final/runs-inventory-completed.json:1>) — lignes 1-56 ; 1 169 octets ; SHA-256 `21cf0ccd0137626d645efa2e60ad15d5557375f8e6c86b9c72a55f27196e4c47`.


Le livrable final a été créé exclusivement après contrôle d’absence ; aucun livrable existant n’a été remplacé. Les brouillons et notes techniques restent dans `runs/`. Aucun correctif, PR, ADR, tag, commit ou décision destinés au projet réel n’a été produit. Les dépôts d’essai, y compris leurs erreurs préparatoires, ont été conservés pour permettre la vérification.

## L. Verdicts

Un PASS est limité aux contrôles effectivement exécutés et à leur contrat ; il n’efface ni les frontières doctrinales ni les plateformes absentes. Les BLOCKER se traduisent par le suffixe fermé REQUIRES_MAJOR_REDLINE, aucun suffixe supplémentaire n’étant autorisé.

```text
SQUELETTE_3.9.0_REVUE_T01_REQUIRES_MAJOR_REDLINE
SQUELETTE_3.9.0_REVUE_T02_REQUIRES_MAJOR_REDLINE
SQUELETTE_3.9.0_REVUE_T03_PASS
SQUELETTE_3.9.0_REVUE_T04_REQUIRES_MAJOR_REDLINE
SQUELETTE_3.9.0_REVUE_T05_REQUIRES_MAJOR_REDLINE
SQUELETTE_3.9.0_REVUE_T06_REQUIRES_MAJOR_REDLINE
SQUELETTE_3.9.0_REVUE_T07_REQUIRES_MAJOR_REDLINE
SQUELETTE_3.9.0_REVUE_T08_REQUIRES_MINOR_REDLINE
SQUELETTE_3.9.0_REVUE_T09_INPUT_MISSING
SQUELETTE_3.9.0_REVUE_T10_PASS
SQUELETTE_3.9.0_REVUE_REQUIRES_MAJOR_REDLINE
```
