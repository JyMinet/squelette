> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Mandat de relecture du code — chantier P21 « Tableau des clés » (3.21.0)

Relecture indépendante du code, avant sa livraison dans l'atelier. Mandat donné par Jeoffrey (Project Owner) le 2026-09-28 : « Construire » (18:27), la seconde IA relisant le code à la fin de la construction. Rédigé par Claude, auteur du code — conflit d'intérêt déclaré : on attend des scénarios rejoués, pas des arguments. Style de retour du Project Owner : PLAIN (résumé en trois points en tête ; le corps peut être technique).

## 1. Objet

- Dépôt : `~/Projets/squelette-chantier-p21`, clone débranché de l'atelier du squelette (aucun remote).
- Code relu : la branche `claude/p21-tableau-des-cles` au commit `0ecb5464fdd1e03534dbb32ffc1d487907e4da14`, contre sa base `main` = `b9fe0e7bd91ab02a9cda967fdddd6c51b56d13c8` (3.20.2 et sa vue). Empreintes attendues au commit relu : `scripts/project_control.py` SHA-256 `e07444e75e36174511e0e6f888e18f6b0e9d7c5ea756399f1881b950f7eef141` ; `tests/test_template.py` SHA-256 `1500f3c4cb1f3dd819eb440fbc88e2f9f68dc89f3550230385b43ec338173f06`.
- Le cœur : dans `scripts/project_control.py`, tout ce qui touche aux copies — les fonctions `copy_*`, `clone_inventory`, `export_inventory`, `inventory_digest`, `abandoned_items`, `copy_path_errors` ; les méthodes `copies_*`, `copy_*`, `open_copy`, `return_copies`, `check_copy`, `move_copy`, `close_copy`, `copies_cleanup_script`, `copy_slip_banner` ; les ajouts à l'audit (`COPIES_REGISTER`, `COPIES_RETURNED`), à `close`, au garde-fou de commit (`TEMPLATE_COPIES_ON_MAIN`), à `status` et à la vue. Puis : `project_control/schemas/copies-state.v1.schema.json`, `provenance/maintenance/publication/export_public.py`, les essais P21 de `tests/test_template.py` (à partir de « Copies of the repository (P21) »), la doctrine (`docs/agent-governance/AGENTS.core.md`, section « Copies du dépôt ») et le guide des commandes (`project_control/README.md`, section « Copies du dépôt »).
- Pièces de référence, en lecture seule : `RAPPORT-CONSTRUCTION-P21.md` (ce qui est construit, les écarts assumés à la fiche, les dix trous d'une première revue indépendante et leurs fermetures) ; `RAPPORT-MESURE-P21.md` ; dans la branche, la fiche de cadrage V3 (`provenance/maintenance/scopes/p21-scope-tableau-des-cles.md`) et le CHANGELOG (décision `TPL-D-080` ; entrée de maintenance du 2026-09-28).

## 2. Dossier accordé

`~/Projets/squelette-chantier-p21/` et lui seul.

**En lecture seule** : tout ce qui y existe, `.git` compris. Aucune commande Git qui écrive dans ce dépôt — ni `checkout`, `switch`, `commit`, `fetch`, `worktree`, `stash`, `gc`, ni même `git status` sans `GIT_OPTIONAL_LOCKS=0`. Pour lire la branche, la cloner dans le sous-dossier de travail.

**Écritures permises**, et seulement celles-ci :

- `revue-code/` — nouveau sous-dossier, pour tout le travail : le clone de relecture (`git clone --no-local --branch claude/p21-tableau-des-cles ~/Projets/squelette-chantier-p21 revue-code/clone`), les dossiers temporaires (`TMPDIR=~/Projets/squelette-chantier-p21/revue-code/tmp` pour toute exécution d'essais ou de sondes), les sondes et leurs copies d'essai ; toute fixture porte la mention « FIXTURE DE RELECTURE — FICTIF, N'AUTORISE RIEN » ;
- le livrable unique, à la racine : `RELECTURE_CODE_P21.md`, en création exclusive. S'il existe déjà : verdict `CODE_P21_OUTPUT_ALREADY_EXISTS`, rien d'écrit.

Aucun accès à l'atelier (`squelette-atelier`), à `alpha`, à `squelette-revue-tableau-des-cles`, à `_archives/` ni à tout autre dossier. Aucun envoi en ligne. Aucune suppression hors de `revue-code/`. Un script d'effacement produit par le contrôleur (`copy cleanup`) ne se lance que sur des copies d'essai situées dans `revue-code/`, après en avoir lu le contenu.

## 3. Posture

`READ_ONLY` sur le dépôt, `REPORT_ONLY` : aucun correctif appliqué, aucun commit ; une correction se propose dans le livrable (description ou diff). Les décisions enregistrées du Project Owner (`TPL-D-080` ; décisions 1 à 8 de la fiche) et les écarts assumés listés dans `RAPPORT-CONSTRUCTION-P21.md` (section A) sont des données : on peut en signaler une conséquence dangereuse démontrée, on ne les rediscute pas.

## 4. Ce qu'il faut chercher

Deux questions d'abord : **le script d'effacement peut-il faire perdre du travail, ou effacer autre chose que la copie qu'il vient de contrôler ?** et **une commande `copy` peut-elle écrire ailleurs que dans le registre, ou laisser le dépôt dans un état que le garde-fou refuse ?**

- **C-01 — Inventaire** (`copy return`, `copy check`) : un contenu présent seulement dans la copie peut-il échapper à l'inventaire, ou y être compté comme déjà rendu ? Clone et export ; arbre de travail, index, références, reflog, stash, `.git` par liste fermée ; liens symboliques ; noms non ASCII ; fichiers ignorés ; ce que la configuration d'une copie peut faire exécuter au contrôleur.
- **C-02 — Couverture** : un élément couvert par l'original peut-il en disparaître entre le retour et l'effacement sans que `copy check` refuse ? Preuves de fichiers, abandons par préfixe, tags annotés, commits de reflog.
- **C-03 — Effacement** : le script peut-il effacer un autre dossier que celui contrôlé — chemins, liens, montages, table de correspondance (`PROJECT_CONTROL_PATH_MAP`), guillemets, caractères de contrôle, ordre des contrôles, dossier parent épinglé ? La fenêtre entre contrôle et effacement est-elle bien celle que la doctrine déclare ?
- **C-04 — Lieu d'exécution** : une commande `copy` lancée depuis une copie, un autre clone, un contenant d'export ou une branche de travail peut-elle agir ?
- **C-05 — Registre et garde-fou** : `copy open`, `return`, `move` et `close` n'écrivent-ils que le registre, sur la branche de référence, dans un état que l'audit accepte ? La réparation groupée peut-elle masquer un autre échec ? Le registre peut-il devenir invalide par une voie normale ?
- **C-06 — Non-régression** : projet sans registre ; projet dérivé qui monte en 3.21.0 (`template-upgrade`) ; export public ; vue ; `status` ; worktrees jetables du contrôleur.
- **C-07 — Les dix trous de la première revue** (tableau B du rapport de construction, plus les deux ajouts) : chacun est-il fermé dans le code, pas seulement dans son essai ? Verdict par trou : `FERMÉ` | `PARTIEL` (avec le chemin qui reste ouvert) | `OUVERT`.
- **C-08 — Cohérence** : la doctrine et le guide promettent-ils ce que le code ne fait pas, ou l'inverse ?

## 5. Standard et verdict

Sans scénario démontré, pas de redline : chaque constat porte sa reproduction (commandes, fixtures dans `revue-code/`, sortie observée). Gravités : `BLOCKER` (perte de travail, ou effacement hors de la copie, démontrés), `MAJOR` (garantie écrite non tenue), `MINOR`, `NOTE`.

Verdict terminal, liste fermée : `CODE_P21_PASS` · `CODE_P21_REQUIRES_MINOR_REDLINE` · `CODE_P21_REQUIRES_MAJOR_REDLINE` · `CODE_P21_CANONICAL_CONFLICT` · `CODE_P21_INPUT_MISSING` · `CODE_P21_OUTPUT_ALREADY_EXISTS`.

## 6. Structure du livrable

Résumé en trois points (ce qui s'est passé, ce que ça change, ce que Jeoffrey doit faire) ; **A** preflight — commit relu, empreintes vérifiées, versions de Python et de Git, résultat de la suite complète dans `revue-code/clone` ; **B** constats au format habituel (identifiant, gravité, scénario, preuve, correction proposée) ; **C** table des dix trous et des deux ajouts → `FERMÉ` / `PARTIEL` / `OUVERT` ; **D** état du dossier en fin de mandat (rien d'écrit hors de `revue-code/` et du livrable ; `git -C … rev-parse main claude/p21-tableau-des-cles` inchangés) ; **E** verdict terminal.

## 7. Après la relecture

Le livrable est rangé tel quel dans l'atelier à la livraison, sous double arrêt séparé. `revue-code/` est abandonné comme jetable au retour du dossier de chantier, que Jeoffrey efface ensuite.

---

**Texte à coller dans la demande à Codex** (dossier de travail de Codex : `~/Projets/squelette-chantier-p21`, avec droit d'écriture) :

> Réalise la relecture de code décrite dans ~/Projets/squelette-chantier-p21/MANDAT-RELECTURE-CODE-P21.md, en respectant exactement le dossier accordé, les interdits et la structure du livrable. Livrable unique : RELECTURE_CODE_P21.md à la racine de ce dossier.
