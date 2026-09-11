> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Revue indépendante — Squelette de projet gouverné (V3)

Date : 2026-09-05 · Portée : lecture seule des trois copies présentes sous `~/Projets`
Copies auditées : `Squelette V3 -runtime-proof`, `squelette-projet-gouverne`, `squelette-decision-projet`

---

## A. Constat factuel

| Copie | Git | Contenu | Dernier commit |
|---|---|---|---|
| `squelette-decision-projet` | oui (main + refactor) | socle V1/V2, `project_control.py` 36 Ko | `bede17a refactor(skeleton): generalize project foundation` |
| `squelette-projet-gouverne` | oui (main + fix) | socle consolidé, `project_control.py` 85 Ko, 35 Ko de tests | `becc60f fix(skeleton): simplify project control lifecycle` |
| `Squelette V3 -runtime-proof` | **non versionné** | = `squelette-projet-gouverne` + `ADOPTION.md` + pack `runtime_proof/` | — |

Exécutions de contrôle (read-only) :

- `squelette-projet-gouverne` : `bootstrap-audit` **PASS** (16 contrôles), `audit` **PASS** (13 contrôles).
- `Squelette V3 -runtime-proof` : `bootstrap-audit` **FAIL** — `GIT_REPOSITORY` et `BOOTSTRAP_CHANGE_SCOPE` en échec, faute de dépôt Git.
- Suite de tests V3 : **28 tests, OK en 2,9 s**, bibliothèque standard uniquement.

## B. Niveau de maturité

Estimation : **8,5 / 10 comme moteur de gouvernance**, très au-dessus des frameworks publics de spec-driven development (Spec Kit, BMAD, OpenSpec, Kiro), qui restent au niveau de la convention de prompt. Ici les règles sont **exécutables et fail-closed**.

Ce qui place le squelette à ce niveau :

1. **Double mode avec allowlist** (`BOOTSTRAP_MODE` / `NORMAL_MODE`) : résout le paradoxe d'amorçage (écrire la gouvernance quand la gouvernance exige déjà un Work Item) sans désactiver la sécurité. Le test `test_p_create_work_item_breaks_preflight_creation_circularity` prouve que la circularité a été identifiée et traitée.
2. **Definition of Done à 7 niveaux distincts** (`DEVELOPED` → `PRODUCTION_VERIFIED`) avec tri-état `APPLICABLE` / `NOT_APPLICABLE` / `UNKNOWN`, où `UNKNOWN` **bloque** `DONE`. Aucun framework public ne va aussi loin.
3. **Synchronisation triple fail-closed** roadmap Markdown ↔ `roadmap-state.v1.json` ↔ record Work Item, vérifiée par l'audit.
4. **Mutations transactionnelles** avec rollback (`FileTransaction`), interdiction de `git add .` / `-A` / `reset --hard` / force push, classification obligatoire de tout chemin modifié.
5. **Hiérarchie d'autorité explicite** (Owner > Charter > ADR > contrats > roadmap > implémentation) et règle `STOP` sur ambiguïté.
6. **Politique d'adoption anti-bloat** : `OMIT > ACTIVATE WITHOUT NEED`, toutes les capabilities `OFF` par défaut. Rare et précieux.
7. **Provider-agnostic** : aucune dépendance à un agent particulier ; zéro dépendance externe Python.

## C. Améliorations, par priorité

### P1 — Le squelette ne respecte pas ses propres règles

`ONE_CANONICAL_BASELINE` est imposé aux projets, mais le squelette existe en trois copies dont la plus avancée (V3) n'a pas de dépôt Git et échoue son propre `bootstrap-audit`.

Action : un dépôt unique `squelette`, tags `v1` / `v2` / `v3`, les deux autres copies archivées ; un `REPOSITORY_STATUS.md` renseigné pour le template lui-même.

### P2 — Aucun chemin de mise à jour du template

`TEMPLATE_PROVENANCE.md` dit d'où vient une baseline, mais rien ne dit comment un projet créé en V2 adopte les corrections V3. À 5 projets, chacun forkera silencieusement.

Action : champ `skeleton_version` dans `project-state.v1.json`, `CHANGELOG.md` du template, et commande `template-upgrade` (diff du core, allowlist de mise à jour du core, refus si le projet a modifié le core).

### P3 — La lecture des autorités est déclarative, pas prouvée

`mandatory-documents.v1.json` route dix documents de base à lire avant toute écriture. Rien ne vérifie qu'ils ont été lus, ni dans quel état.

Action : commande `context-manifest` produisant les autorités applicables **avec leur SHA-256**, champ `authorities_read: [{path, sha256}]` dans l'Agent Run, et refus au preflight si un hash ne correspond plus à l'état courant. Transforme une obligation morale en gate machine — et détecte au passage un agent qui travaille sur une autorité périmée.

### P4 — La pratique de revue adversariale n'est pas dans le squelette

Le dispositif le plus différenciant (mandats de reviewer indépendant, verdicts à vocabulaire fermé `…_PASS` / `…_REQUIRES_MINOR_REDLINE` / `…_CANONICAL_CONFLICT` / `…_INPUT_MISSING`, challenges adversariaux, contre-revues croisées sans lecture mutuelle, réconciliation dual-review, règle « pas de redline sans scénario d'échec démontré ») vit uniquement dans la pratique Alpha, réinventé à chaque fois.

Action : capability optionnelle `ADVERSARIAL_REVIEW` (`OFF` par défaut) : gabarit de mandat reviewer, liste fermée des verdicts, arborescence `reports/<phase>/{scope-reconstructions,challenges,cross-reviews,reconciliations}`, schéma de findings/redlines à champs obligatoires.

### P5 — Pas de granularité au-dessus du Work Item

Alpha fonctionne par **passes** A–I avec gate de fermeture et freeze global ; le squelette s'arrête au Work Item. La phase est donc gérée à la main, hors contrôle machine.

Action : objet `PHASE` (ou `PASS`) avec ouverture, Work Items rattachés, challenge de fermeture, gate humaine, scellement et état `FROZEN`.

### P6 — Pas de guide de continuité

`conversations/` référence les échanges mais aucun document ne permet à une nouvelle session — ou à un autre modèle — de reprendre sans tout relire.

Action : `docs/governance/CONTINUITY_GUIDE.md` régénéré par le contrôleur : état courant, prochaine gate, ce qui est autorisé, ce qui est interdit, HEAD de référence.

### P7 — Definition of Ready absente

Sept niveaux de sortie, aucun critère d'entrée. L'interview couvre l'initialisation du projet, pas l'admission d'un Work Item.

### P8 — Points mineurs

- Le profil d'adoption (`ADOPTION.md`) est en prose : `adoption-profile.v1.schema.json` existe dans `runtime_proof/contracts/` mais aucun record actif n'est produit ni audité. Capability déclarée, non contrôlée.
- `RECOVERY.md` porte `TEMPLATE — NOT_QUALIFIED` : un exercice de restauration réel, une fois, changerait son statut.
- Les interdits Git (`git add -A`, etc.) sont de la prose ; un hook `pre-commit` local les rendrait mécaniques.
- `ADOPTION.md` n'existe qu'en V3 — à consolider dans la baseline unique (P1).

## D. Intégration côté Claude

| Emplacement | Rôle | État |
|---|---|---|
| `AGENTS.md` à la racine du dépôt projet | autorité opérationnelle, lue à chaque session | déjà en place |
| `CLAUDE.md` racine (3 lignes → `AGENTS.md`) | point d'entrée attendu par Claude Code / Cowork | **manquant** |
| Skill `squelette-projet` | doctrine + procédures invocables dans n'importe quelle session, sans dossier connecté | à créer |
| Project « Squelette » (celui-ci) | doctrine, CHANGELOG du template, état des projets qui l'utilisent | à alimenter |
| Tâche planifiée | `audit` périodique des dépôts gouvernés | optionnel |
