> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# P9 — Scope Definition : records administratifs et branches

Statut : `SCOPE_DEFINITION_V2 — IMPLEMENTED_ON_BRANCH — NOT_PROMOTED` (V1 ci-dessous conservée telle quelle ; décision et implémentation en fin de document)
Nature : définition de périmètre pour une décision de conception. Aucun code n'est produit, aucun Work Item n'est créé. Toute implémentation exige un mandat explicite sur branche dédiée.
Baseline examinée : `Squelette V3 -runtime-proof`, `main` = `64a3cb1` (`v3.1.0`).

## 1. Problème

Les records administratifs — Work Items, Agent Runs, Conversations, `roadmap-state.v1.json`, `ROADMAP.md`, `WORKTREE_REGISTRY.md`, `HUMAN_DECISIONS.md`, `git-path-classifications.v1.json` — vivent dans l'arbre et sont modifiés par `start`, `block`, `resume` et `close` dans le worktree courant. `start` s'exécute depuis la branche canonique, bascule sur la branche du Work Item, puis écrit ses records : ils sont donc committés **sur la branche du Work Item**, et la canonique ne les voit qu'à l'intégration. L'état administratif est local à chaque branche jusqu'au merge.

C'est la cause racine de la fragilité du blocage/reprise corrigée en R1 par un alignement automatique, qui traite le symptôme (conflits de records au retour) et non la cause.

## 2. Scénarios d'échec démontrés

**S-01 — Unicité du chantier actif aveugle.** WI-001 est `IN_PROGRESS` sur sa branche ; vu depuis la canonique, son record dit encore `AUTHORIZED`. `start WI-002` depuis la canonique passe `SINGLE_ACTIVE_WORK_ITEM`. Deux chantiers actifs coexistent, contrairement à `MAX_ACTIVE_INTEGRATION_CANDIDATES = 1`. Constaté par lecture du code (`preflight_findings`, `SINGLE_ACTIVE_WORK_ITEM` lit les records du checkout courant) ; reproduit dans le bac à sable le 2026-09-06.

**S-02 — Reprise conditionnée à un report manuel.** `resume` lit les records depuis le checkout canonique ; un blocage enregistré sur la branche du Work Item n'y est pas visible. Le report des chemins administratifs vers la canonique est une procédure manuelle, documentée dans `project_control/README.md` (« Blocage et reprise »). Un agent qui l'omet obtient `WI-001 must be BLOCKED, got AUTHORIZED`.

**S-03 — Conflits de records à l'intégration.** WI-001 en cours sur sa branche, WI-002 créé, intégré et clos sur la canonique entre-temps : le merge d'intégration de WI-001 conflicte sur `roadmap-state.v1.json` et le registre, modifiés des deux côtés (reproduit le 2026-09-06, scénario E4). R1 résout ce cas au `resume` seulement ; un Work Item jamais bloqué le rencontre à son merge final.

**S-04 — `status` périmé sur la canonique.** La vue calculée depuis la canonique ignore l'avancement réel des branches ; la « prochaine action » proposée est fausse dès qu'un chantier est en cours ailleurs.

## 3. Objectif

Que l'état administratif du projet ait une seule vérité à tout instant, lisible depuis la branche canonique, sans conflit de records à l'intégration, et sans nouvelle source d'état hors de l'arbre.

## 4. Non-objectifs

- Ne pas sortir les records de Git (pas de base locale, pas de service).
- Ne pas changer le contrat des records (`work-item.v1`, `agent-run.v1`).
- Ne pas modifier les règles de preuve de clôture ni les niveaux de DoD.
- Ne pas traiter la migration des projets antérieurs (P2).

## 5. Options

### Option A — records sur la branche canonique uniquement (recommandée)

Les commandes de cycle de vie ne modifient les records **que sur la branche canonique** ; la branche du Work Item ne porte jamais de changement administratif.

- `start` s'exécute depuis la canonique, écrit ses records, **exige leur commit** avant de créer ou basculer sur la branche (deux temps : `start` écrit et refuse de basculer tant que les records ne sont pas committés ; `checkout WI-NNN` bascule après vérification). Variante : `start --commit` crée lui-même le commit administratif, sur le précédent de R1 (Project Control crée déjà un commit de merge).
- `block`, `resume`, `close` s'exécutent depuis la canonique (`close` l'exige déjà pour l'intégration) ; `block` n'a plus à être exécuté sur la branche, donc plus de report manuel (S-02 disparaît).
- Le preflight sur la branche lit les records **de la canonique** (`git show <canonique>:project_control/...`) et non ceux du checkout, ce qui règle S-01 et rend `SINGLE_ACTIVE_WORK_ITEM` exact.
- Les preuves restent sous `reports/evidence/<WI>/` sur la branche ou la canonique selon le flux actuel.
- Le hook de commit gagne une règle : sur une branche de Work Item, aucun chemin administratif n'est admis.

Conséquences : plus aucun conflit de records à l'intégration (S-03), `status` exact (S-04), alignement de R1 réduit au cas métier. Coût : refonte de `start`/`block`/`resume`/`close` et de la moitié des tests ; changement de procédure dans `AGENTS.md` (autorité).

### Option B — statu quo + visibilité inter-branches

Conserver le flux actuel et corriger S-01 et S-04 par une lecture croisée : quand le record canonique d'un Work Item dit `AUTHORIZED` et que sa branche déclarée existe, `preflight` et `status` lisent aussi `git show <branche>:project_control/work-items/<WI>.json` et considèrent le statut le plus avancé. S-02 et S-03 restent traités par procédure et par l'alignement de R1.

Coût faible (lecture seule, quelques dizaines de lignes, deux tests). Ne supprime pas la cause.

### Option C — records hors branche (worktree ou branche `project-control` dédiée)

Une branche administrative unique, toujours checkout dans un worktree séparé. Une seule vérité, mais une seconde arborescence à maintenir, une nouvelle classe d'opérations Git et une rupture avec « les records vivent dans le projet ». Non recommandée : contraire à `OMIT > ACTIVATE WITHOUT NEED`.

## 6. Impacts

- `DIRECT` : `scripts/project_control.py` (`start`, `block`, `resume`, `close`, `preflight_findings`, `status_payload`), `AGENTS.md` (procédure Normal Mode), `project_control/README.md`, `tests/test_template.py`, hook de commit.
- `INDIRECT` : projets dérivés — Alpha en premier — dont le flux quotidien change (commit administratif avant bascule) ; P2 doit livrer ce changement avec une migration nulle (les records ne changent pas de forme).
- `AUTHORITY` : la procédure de preflight Normal Mode change de séquence — décision humaine requise.
- `CONCURRENT` : P3 (preuve de lecture) touche `preflight` et les Agent Runs ; à ordonner après P9. P2 touche le core : indépendant mais à livrer après.

## 7. Points non tranchés

- Project Control peut-il créer des commits administratifs (`start --commit`) ou l'agent reste-t-il seul auteur des commits : `UNKNOWN` (précédent : le commit de merge de R1).
- Le preflight sur la branche doit-il refuser tout chemin administratif indexé, ou seulement avertir : `UNKNOWN`.
- Faut-il conserver l'alignement automatique de R1 une fois l'option A en place (il ne resterait utile qu'aux conflits métier, qu'il refuse) : `UNKNOWN`.

## 8. Critères de fermeture proposés

1. S-01 à S-04 sont chacun refusés ou résolus par le contrôleur, avec un test dédié.
2. Un merge d'intégration après deux Work Items entrelacés ne produit aucun conflit sur un chemin administratif (test).
3. `status` depuis la canonique reflète l'état réel de tous les Work Items (test).
4. Suite complète verte ; `audit` et `bootstrap-audit` PASS sur copie neuve.
5. Aucune dépendance hors bibliothèque standard ; aucune nouvelle source d'état.


## V2 — décision et implémentation (2026-09-07)

Statut : `SCOPE_DEFINITION_V2 — IMPLEMENTED_ON_BRANCH — NOT_PROMOTED`

### Décisions du Project Owner

- « P9- A » : option A retenue (records administratifs sur la branche canonique uniquement).
- « Project Control commite lui-même » : le point non tranché n° 1 est tranché — les transitions créent leur commit administratif, l'agent ne l'écrit pas à la main.
- Contrainte de sécurité rappelée par le Project Owner et respectée : `alpha` est accessible **en lecture seule** (aucune écriture, aucune commande Git modifiante, aucun script de ce dépôt exécuté). Il n'a servi qu'à l'inspection de P2.

### Points non tranchés — résolution

1. Commits administratifs par Project Control : **oui** (décision ci-dessus). Message `chore(project-control): <transition> WI-NNN`, identité Git du checkout.
2. Chemin administratif indexé sur une branche de Work Item : **refus**, pas avertissement. `preflight` et le hook renvoient `WORK_BRANCH_RECORDS_READ_ONLY` ; le commit est bloqué.
3. Alignement automatique de R1 : **conservé** dans `resume`, réduit à son rôle métier — fast-forward quand la branche est simplement en retard, merge de la canonique sinon, refus et annulation sur conflit métier. Les records n'y participent plus (ils ne vivent que sur la canonique).

### Ce qui a été implémenté

Branche `claude/v3.2-records-canonical`, commit `433cda0`, depuis `claude/v3.2-git-safety` (`55c5a35`), elle-même sur `v3.1.0`. `main` reste à `64a3cb1`.

- `create-work-item`, `start`, `block`, `resume`, `close` : exigent le checkout de la branche canonique, à son tip, sur un worktree propre (`require_canonical_checkout`, `require_clean_worktree`) ; écrivent leurs records puis les committent (`commit_records`).
- `start` : records committés sur la canonique (`start_head` = ce commit), puis création de la branche du Work Item depuis ce commit ; une branche préexistante au `start_head` est avancée par `update-ref`. Preflight de la branche après bascule ; tout échec annule le commit de records (`update-ref` avec ancienne valeur attendue, `restore --staged`, rollback des fichiers) et supprime ou restaure la branche.
- `block` : depuis la canonique, plus de report manuel des records de blocage.
- `resume` : records committés sur la canonique avant la bascule ; alignement de la branche ensuite (ff-only, sinon merge) ; rollback complet sur échec, y compris abandon du merge.
- `close` : depuis la canonique, records committés par la commande.
- `preflight` : nouvelle constatation `WORK_BRANCH_RECORDS_READ_ONLY` (chemin administratif modifié hors canonique) ; `commit_gate_findings` la porte aussi, donc le hook refuse le commit.
- Bootstrap Mode inchangé : les records de l'initialisation restent committés par l'agent avec elle.
- Documents alignés : `AGENTS.md` (preflight Normal Mode), `project_control/README.md` (cycle, blocage/reprise), `FIRST_START.md` (utilisation quotidienne), `provenance/CHANGELOG.md` (entrée `claude/v3.2-records-canonical`).

### Critères de fermeture — état

1. S-01 à S-04 : `test_records_live_on_canonical_branch_only` couvre S-01 (second `start` refusé par `SINGLE_ACTIVE_WORK_ITEM` depuis la canonique), S-04 (`status --json` exact depuis la canonique) et le refus des records sur branche (preflight et hook) ; S-02 disparaît par construction (`block` s'exécute depuis la canonique — tests `block_resume_*` adaptés) ; S-03 est couvert par `test_resume_aligns_diverged_branch_by_merge_and_closes` (chantier bloqué, autre chantier créé, intégré et clos entre-temps, reprise puis clôture sans conflit administratif). **Rempli.**
2. Merge d'intégration après entrelacement sans conflit administratif : même test ; l'entrelacement sans blocage est désormais impossible (un seul chantier actif, vu depuis la canonique). **Rempli.**
3. `status` exact depuis la canonique : assertion S-04 ci-dessus. **Rempli.**
4. Suite complète verte : 77 tests OK (bac à sable 119 s, poste du Project Owner 31 s) ; `audit`, `bootstrap-audit`, `status` PASS sur la branche ; `test_a_new_not_started_copy_passes_bootstrap_audit` couvre la copie neuve. **Rempli.**
5. Bibliothèque standard seule ; aucune nouvelle source d'état hors de l'arbre. **Rempli.**

Rollback couvert en plus par `test_start_rolls_back_its_records_commit_when_the_branch_preflight_fails` (échec injecté après le commit de records : tip canonique, branche, worktree et records restaurés, `audit` PASS).

### Compatibilité et suite

- Projets antérieurs (Alpha en premier) : aucun champ de record ne change, donc aucune migration de données ; mais toute branche en cours qui porte des records doit être intégrée avant l'adoption du nouveau flux. À prendre en compte dans P2.
- Décisions attendues du Project Owner : promotion de `claude/v3.2-git-safety` puis `claude/v3.2-records-canonical` sur `main` (fast-forward, tag proposé `v3.2.0`), puis P2 étape 1 (`legacy_baseline` dans le template), puis P3.
