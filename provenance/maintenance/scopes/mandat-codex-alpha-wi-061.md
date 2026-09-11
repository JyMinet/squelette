> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Mandat — Alpha WI-061 : adoption du core du squelette (P2, étape 2)

Statut : `MANDATE_WITHDRAWN — WRONG_TARGET` (2026-09-07)

**Retrait.** Ce mandat visait le dépôt original `alpha`. Le Project Owner a tranché le 2026-09-07 : le vrai Alpha ne sert jamais directement de terrain d'essai au squelette ; seule une copie (clone) dont l'original n'est pas impacté est acceptable. Le mandat est retiré ; la branche `codex/wi-061-adoption-core-v3-4-1` produite dans l'original (trois commits, non fusionnés, non poussés) est à supprimer par le Project Owner selon le topo de retour arrière (`p2-scope-template-upgrade.md`, § 13). Une réédition éventuelle de ce mandat ne pourra viser qu'un clone d'Alpha, sur décision explicite. Le texte ci-dessous est conservé comme trace, il n'est plus à exécuter.

Rédigé le 2026-09-07 pour le Project Owner, à coller tel quel dans une nouvelle discussion Codex (ou à confier à Claude sous mandat d'écriture). Les blocs entre `« »` sont les décisions humaines déjà prises ; rien d'autre n'est à inférer.

---

## Texte du mandat (à coller)

Tu interviens dans le dépôt `~/Projets/alpha` (branche canonique `main`, HEAD attendu `8038b78`, worktree propre, aucun Work Item `IN_PROGRESS`, dernier Work Item `WI-060`, dernière décision `HD-065`). Si l'un de ces préalables n'est pas vérifié, `STOP` et rapport.

**Objectif.** Remplacer le core de Project Control d'Alpha par celui du squelette `v3.4.1` (dépôt `~/Projets/Squelette V3 -runtime-proof`, `main`, tag `v3.4.1`) sans migrer aucun record, en figeant l'historique à la baseline d'adoption déjà en vigueur, puis prouver l'alignement par `template-upgrade`.

**Règles.** Gouvernance d'Alpha : Human Decision, Work Item, branche dédiée, preflight, preuves structurées, comme pour `WI-060`. `GIT_OPTIONAL_LOCKS=0`. Chemins explicites, jamais `git add -A`, `git add .`, `reset --hard`, `clean`, force push. Aucun push : la promotion de `main` et les push NAS restent le geste du Project Owner. Aucune modification des records historiques, des rapports de fermeture globale (`reports/a-i-global-closure/`) ni du modèle métier. Un fichier core ne se modifie pas à la main : il est copié depuis le squelette ou laissé tel quel. Toute question d'autorité, tout conflit entre une règle projet et le core : `STOP` et décision humaine.

**Séquence.**

1. Décision humaine `HD-066` dans `docs/governance/HUMAN_DECISIONS.md` : « Adopter le core du squelette v3.4.1 dans Alpha sans migration de records ; baseline d'adoption `d4d7b5ad8108646139c155a8ca198e699eda7645` (autorité `HD-065`) ; exécutant : Codex ; aucune promotion ni push par l'agent. » Autorisé par : Jeoffrey.
2. `create-work-item WI-061` avec le contrôleur actuel d'Alpha : titre « Adoption du core du squelette v3.4.1 », `--human-decision HD-066`, `authorized_paths` : `CLAUDE.md`, `FIRST_START.md`, `ADOPTION.md`, `AGENTS.md`, `scripts`, `tests`, `project_control/schemas`, `project_control/README.md`, `project_control/project-state.v1.json`, `docs/governance/DEFINITION_OF_DONE.md`, `docs/agent-governance`, `provenance/core-manifest.v1.json`, `reports/evidence/WI-061` ; `--code NOT_APPLICABLE --tests APPLICABLE --integration APPLICABLE --deployment NOT_APPLICABLE --runtime-proof NOT_APPLICABLE --runtime-target NOT_APPLICABLE` ; impacts : direct = fichiers core, indirect = toute session d'agent sur Alpha, autorité = `AGENTS.md` (le core devient `AGENTS.core.md`), concurrent = `NONE` (aucun chantier actif). Puis `start WI-061` : la branche déclarée est créée et le preflight passe. Committer les records selon le flux Alpha en vigueur.
3. Sur la branche, copier depuis le squelette **à `v3.4.1`** (`git -C <squelette> archive v3.4.1 | tar -x -C <dossier temporaire>`) les 19 fichiers listés par son `provenance/core-manifest.v1.json`, chemin par chemin, droits d'exécution conservés (`scripts/project_control.py`, `scripts/hooks/pre-commit`), en **conservant** dans `FIRST_START.md` la ligne `INITIALIZATION_STATUS: COMPLETE` d'Alpha. Copier `provenance/core-manifest.v1.json` tel quel. Ne pas exécuter `core-manifest --write` : il est réservé au squelette.
4. `project_control/project-state.v1.json` : ajouter `"legacy_baseline": {"head": "d4d7b5ad8108646139c155a8ca198e699eda7645", "human_decision_ref": "HD-065"}` (avant `initialization`), rien d'autre ne change.
5. `AGENTS.md` d'Alpha : insérer en tête, sous le titre, la ligne `` `AGENTS_CORE: docs/agent-governance/AGENTS.core.md` `` ; supprimer les sections qui ne sont que la copie de l'ancien core (elles vivent maintenant dans `AGENTS.core.md`) ; conserver sous « Règles propres au projet » chaque règle spécifique à Alpha, avec l'autorité qui la fonde. Une règle Alpha qui affaiblirait le core est un conflit : `STOP`.
6. `docs/agent-governance/mandatory-documents.v1.json` : ajouter `docs/agent-governance/AGENTS.core.md` dans `base`, juste après `AGENTS.md`.
7. `tests/test_evidence_migration.py` : supprimer (`git rm`), sa constante `LEGACY_EVIDENCE_BASELINE` disparaît avec l'ancien contrôleur ; la politique est couverte par `test_legacy_baseline_*` de la suite du squelette.
8. `git config core.hooksPath scripts/hooks` dans le checkout.
9. Vérification, sur la branche, tout doit être vrai :
   - `python3 -B scripts/project_control.py audit` → `PROJECT_CONTROL: PASS`, avec `LEGACY_RECORDS_PRESENT — 59 legacy Work Item(s) frozen at d4d7b5ad…`, `LEGACY_EVIDENCE_FROZEN` PASS, `CORE_MANIFEST — skeleton_version 3.4.1` ;
   - `python3 -B scripts/project_control.py status` → `Squelette : 3.4.1 | core aligné`, `Travaux terminés : 59 (dont 58 figés avant la baseline d'adoption) | Bloqués : 1` ;
   - `python3 -B scripts/project_control.py core-manifest` → `CORE_ALIGNED` ;
   - `python3 -B scripts/project_control.py template-upgrade --source "~/Projets/Squelette V3 -runtime-proof"` → `identical 19, updated [], added [], removed upstream [], modified locally []` ;
   - `python3 -B -m unittest discover -s tests` → 85 tests OK.
   Ces cinq résultats ont été obtenus le 2026-09-07 sur un clone jetable d'Alpha (répétition générale) ; un écart est un fait nouveau à rapporter, pas à contourner.
10. Commits sur la branche par chemins explicites (le hook est actif : un commit refusé se corrige, il ne se force pas). Preuves sous `reports/evidence/WI-061/` (rapports JSON `tests` et `integration` selon `project_control/README.md`), intégration de la branche dans `main` par le Project Owner ou sur son instruction, puis `close WI-061` depuis `main` avec le nouveau contrôleur (il committe lui-même la clôture).
11. Rapport final : chemins modifiés, SHA-256 des 19 fichiers core, sorties intégrales des cinq vérifications, état Git (branche, HEAD, `main`), et la liste des règles Alpha conservées dans `AGENTS.md`.

**Critère de fin.** `template-upgrade --dry-run` = zéro écart et suite verte sur `main` après intégration ; à partir de là, les versions suivantes du squelette s'appliquent à Alpha par `template-upgrade` sous Work Item.

---

## Notes pour le Project Owner (hors mandat)

- Préalable rempli le 2026-09-07 : `v3.4.1` promue (`44905d1`, TPL-D-010) ; vérifier que `origin` et `nas` sont poussés avant de soumettre. (`v3.4.0` ne convenait pas : sa suite de tests échouait dans un projet dérivé — 65 échecs constatés en répétition.)
- Le flux quotidien d'Alpha change avec ce core : `create-work-item`, `start`, `block`, `resume`, `close` s'exécutent depuis `main` et committent eux-mêmes leurs records (P9-A) ; le hook refuse un record sur une branche de Work Item. À annoncer dans `HD-066` si tu veux que ce soit tracé.
- `WI-061` est le dernier Work Item créé par l'ancien contrôleur et le premier clos par le nouveau : c'est prévu, la répétition l'a couvert côté validation (60/60 records valides, WI-060 vérifié en structuré).
- Le dossier pré-freeze (fermeture globale A–I) n'est pas touché ; il peut reprendre après `WI-061` sans dépendance.

---

## Amendement 1 (2026-09-07) — réponse au STOP de Codex

**Constat de Codex (exact).** Préalables conformes (Alpha `main` = `8038b78`, propre, 0 `IN_PROGRESS`, `HD-065` ; source `v3.4.1` = `44905d1`). Conflit d'autorité : l'introduction de `docs/governance/WORKTREE_REGISTRY.md` d'Alpha (document routé en base) dit « fast-forward strict, toute divergence est refusée » à la reprise, alors que le core `v3.4.1` aligne la branche par fast-forward ou commit de merge et refuse seulement le conflit métier (`AGENTS.core.md`, lignes 121–131). Le mandat prescrit `STOP` ; l'arrêt est correct.

**Origine du conflit.** La phrase d'Alpha est l'ancienne doctrine du squelette (reprise refusée dès que la branche a divergé), jugée impasse par la contre-revue du 2026-09-06 (F-01) et remplacée, sur décision du Project Owner, par l'alignement automatique (`claude/v3-redlines`, `v3.1.0`). Le registre du squelette a été mis à jour à ce moment-là (« fast-forward ou commit de merge, jamais de réécriture ») ; la copie d'Alpha, antérieure, ne l'a pas été — et `WORKTREE_REGISTRY.md` est hors core (TPL-D-007), donc hors de portée de `template-upgrade`. Le mandat aurait dû prévoir cette réconciliation ; c'est une omission du mandat, pas une dérive d'Alpha.

**Vérification complémentaire (lecture seule, 2026-09-07).** Aucune autre règle générale en conflit dans `REPOSITORY_STATUS.md`, `RECOVERY.md`, `STORAGE_POLICY.md`, `ROADMAP.md`, `README.md` d'Alpha. `HUMAN_DECISIONS.md` mentionne « fast-forward strict » dans des décisions historiques propres à des Work Items (WI-013, WI-022) : ce sont des décisions datées, pas des règles générales ; elles restent intactes.

**Décision proposée au Project Owner (à confirmer).** Oui : ajouter `docs/governance/WORKTREE_REGISTRY.md` aux `authorized_paths` de `WI-061` et l'inscrire dans `HD-066`, avec ce périmètre exact :

- seule l'introduction du registre (tout ce qui précède le premier bloc `<!-- PROJECT_CONTROL:WI-… START -->`) est réconciliée ; les blocs gérés historiques restent inchangés octet pour octet, et seul le contrôleur crée puis fait évoluer le bloc `WI-061` ;
- la réconciliation reprend **telle quelle** l'introduction de `docs/governance/WORKTREE_REGISTRY.md` du squelette à `v3.4.1` (`REUSE > ADAPT` : `start` committe les records sur la canonique avant la création de la branche ; `resume` aligne par fast-forward si la branche est en retard, sinon par commit de merge de la canonique, refuse le conflit métier, n'autorise ni rebase, ni cherry-pick, ni perte d'un commit), en conservant `MAX_ACTIVE_INTEGRATION_CANDIDATES = 1` ; une phrase propre à Alpha n'est conservée que si elle renforce, et elle est listée dans le rapport final ;
- aucune reprise de `WI-013`, aucune intégration de `WI-061` dans `main` par l'agent, aucun push : inchangé.

**Texte à coller pour Codex, une fois la décision prise :**

> Décision du Project Owner : autorisation accordée. Ajoute `docs/governance/WORKTREE_REGISTRY.md` aux `authorized_paths` de `WI-061` et mentionne-le dans `HD-066`. Réconcilie uniquement l'introduction du registre (avant le premier bloc géré) en reprenant telle quelle l'introduction du registre du squelette à `v3.4.1`, `MAX_ACTIVE_INTEGRATION_CANDIDATES = 1` conservé ; blocs historiques intacts ; toute phrase propre à Alpha conservée seulement si elle renforce, et listée dans le rapport. Le reste du mandat est inchangé : aucune reprise de WI-013, aucune intégration ni push par l'agent. Revérifie les préalables, puis reprends à l'étape 1.

**Leçon pour le squelette (à traiter dans une maintenance ultérieure, pas dans WI-061).** Des documents hors core portent de la doctrine du template (introduction du registre, définitions de `REPOSITORY_STATUS.md`, paragraphe « Normal Mode exige… » du README) : un projet dérivé peut donc garder une doctrine périmée que `template-upgrade` ne voit pas. Piste : ramener l'introduction du registre au modèle et à un renvoi vers Project Control (fichier core), et faire signaler par `template-upgrade` les documents hors core dont l'en-tête doctrinal diffère de celui du squelette. Observation `O-09`.
