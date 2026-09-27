> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Diagnostic et proposition — la suite du template échoue dans un projet dérivé qui a relié son volume 1 (core 3.20.0 → correctif 3.20.1)

Discussion Cowork « Squelette », 2026-09-27. Dossier accordé : `~/Projets/Squelette V3 -runtime-proof` (lu seulement à ce stade ; rien n'y a été écrit). Alpha, Redaction_Human et tout autre dépôt réel : ni lus, ni copiés — tout ce qui les concerne vient du brief du Project Owner.

Statut du document : **rapport de diagnostic + proposition**, rendu au `STOP 1` (accepté : « Oui », 2026-09-27 08:45) ; périmètre reformulé et confirmé au `STOP 2` (« Confirmé : branche claude/v3.20.1-fixture-registres-vierges dans ~/Projets/Squelette V3 -runtime-proof, main intouché, pas de push. », 08:48). Il ne décide rien par lui-même : la décision est `TPL-D-076` (`provenance/CHANGELOG.md`), la correction est livrée sur la branche `claude/v3.20.1-fixture-registres-vierges`, la promotion reste une décision séparée.

## Résumé en trois points (pour le Project Owner)

1. **Le mécanisme est confirmé, reproduit sans Alpha, aux mêmes chiffres.** Un projet dérivé jetable, initialisé puis relié (`decision bind`), fait tomber la suite du template lancée depuis chez lui : 181 essais, **144 échecs**, 10 ignorés, 27 réussis — tous les 144 sur la même ligne (« le terme de comparaison manque »). Le même projet, avant la reliure, passe au vert (171 réussis, 10 ignorés). `main` du squelette (3.20.0, commit `0e74009`) n'a rien corrigé de ce point ; aucune version n'existe après la 3.20.0.
2. **La correction est dans la fabrique des copies d'essai, pas dans le contrôle.** La copie repart de registres de décisions vierges : carnet vivant sans décision ni sommaire, aucun volume relié. `DECISION_VOLUMES_CONSISTENT` ne change pas d'une ligne ; le volume 1 des projets réels n'est pas touché. Un essai nouveau (B15) rejoue le cas depuis un projet dérivé au volume relié : rouge sur la 3.20.0, vert après.
3. **Vérifié des deux côtés.** Template : 182 essais verts, audit PASS, démo PASS (VM Linux, Python 3.10.12) ; le prototype tourne aussi sous Python 3.11 (conteneur). Projet dérivé relié, refait sur le prototype 3.20.1 : 182 essais, 172 réussis, 10 ignorés, **0 échec**. Version proposée `3.20.1`, branche `claude/v3.20.1-fixture-registres-vierges`, quatre fichiers touchés dans l'arbre (plus le journal, la feuille de route et la vue à la livraison).

---

## A. Préflight — l'objet tel qu'il est

| Élément | Valeur |
|---|---|
| Dossier accordé | `~/Projets/Squelette V3 -runtime-proof` |
| Branche / HEAD | `main` / `0e74009a251f97f8ab9df8703378d50b7db52de1` |
| Arbre de travail | propre (`git status --porcelain` vide, `GIT_OPTIONAL_LOCKS=0`) |
| Version du core | `3.20.0` (`provenance/core-manifest.v1.json`), 24 fichiers core |
| Dernier tag | `v3.20.0` (35 tags) ; `main` = tag + vue régénérée + `TPL-D-075` (deux mandats rapatriés) |
| `tests/test_template.py` | 6 806 lignes, SHA-256 `65803e29cb735286325cd0dac3a65622dd68b2cb564780b1c87031f9c7cdaa26` — identique au manifeste |
| `scripts/project_control.py` | 7 060 lignes, SHA-256 `21294605fd1e396adeb12077a945ee42c9754f0ee39d45c3d458f280ca30e080` — identique au manifeste |
| Copie fidèle de travail | paquet `git bundle --all` écrit **hors** du dossier accordé (SHA-256 `7b55df63bb3828b7a9d536e5693f41cc8d4d222f9c55e907def672909a97f1a7`), cloné dans l'espace de session ; mêmes HEAD, mêmes 35 tags, mêmes empreintes |
| Miroir public (lecture de confort) | `JyMinet/squelette` à `13db09f` (3.20.0) ; les deux fichiers clés y sont identiques à l'octet (mêmes SHA-256) |

Lecture seule pendant tout le diagnostic : aucune écriture dans le dossier accordé, aucun `fetch`, `pull`, `push`, `checkout`, `commit`, `tag` ni `branch` dans ce dossier.

## B. Le mécanisme, lu dans le code du core

1. `tests/test_template.py`, `make_copy()` (l. 178-200) : `shutil.copytree(ROOT, …)` puis `reset_to_not_started_fixture(root)`, puis `git init -b main` et **un seul commit** « fixture: pristine governed skeleton ». La copie n'a aucune histoire.
2. `reset_to_not_started_fixture()` (l. 217-332) : remet `FIRST_START.md` et `project-state.v1.json` à l'état vierge (baselines `null`, `baseline_head` `UNKNOWN`), élague `applications/modules/shared/contracts/data/reports`, vide la feuille de route, le registre des branches, les classifications, les idées, la vue générée et les records. Pour le carnet de décisions, elle retire tout à partir du premier `## HD-NNN` (l. 272-277) — mais **elle laisse le sommaire du volume** (bloc entre `<!-- decision-volume-1:summary:start -->` et `…:end -->`, qui précède les décisions) et **ne connaît pas `docs/governance/HUMAN_DECISIONS_VOLUME_1.md`**, copié tel quel avec sa ligne `Adoption baseline: <commit>`.
3. `scripts/project_control.py`, `decision_volumes_audit()` (l. 5734-5865), appelé par l'audit dans les deux modes (l. 2202-2204, donc aussi par `bootstrap-audit` et par `bootstrap-closeout`) : si le volume existe, il lit l'origine dans le volume (`DECISIONS_VOLUME_ORIGIN`, l. 89) et exécute `git show <origine>:docs/governance/HUMAN_DECISIONS.md` (l. 5785). Dans une copie sans histoire ce commit n'existe pas → « cannot read … at the binding origin … the comparison term is unavailable » → `DECISION_VOLUMES_CONSISTENT: FAIL` → l'audit de la copie échoue → l'essai échoue avant d'avoir testé ce qu'il voulait tester.
4. Second refus, latent : même si l'histoire existait, la fixture déclare `legacy_baseline: null`, et le contrôle exigerait alors « the volume was bound at … ; the project no longer declares an adoption baseline » (l. 5801-5804). Il n'y a donc **aucune** lecture de la fixture actuelle dans laquelle un volume copié puisse passer : la seule fixture cohérente est celle qui n'en a pas.
5. `make_normal_copy()` → `configure_ready_for_closeout()` réécrit le carnet vivant en entier (l. 401-406) mais ne touche pas au volume : les essais en mode normal tombent pour la même raison que ceux en mode amorçage.

Le contrôle a raison de refuser : le terme de comparaison manque vraiment. La doctrine de la fixture (« A NOT_STARTED fixture is a pristine skeleton … so that a derived project runs this same suite », docstring de `prune_project_content`) n'est pas tenue pour les registres de décisions.

## C. Reproduction sans Alpha

Projet dérivé jetable construit dans l'espace de session avec les aides de la suite elle-même (`make_normal_copy`, `declare_legacy_baseline`, `record_bind_decision`, puis `decision bind --human-decision HD-110`), exactement le chemin des essais `test_binding_*` :

| Projet dérivé | Histoire | Volume 1 | Suite du template lancée depuis ce projet (Python 3.10.12, VM Linux du poste) |
|---|---|---|---|
| `derived-unbound` (contre-épreuve) | 2 commits | absent | **181 essais, OK** — 171 réussis, 10 ignorés (essais propres au template) |
| `derived-bound` (reproduction) | 5 commits, dont `bind 1 frozen Human Decision(s) into volume 1 (HD-110)` | présent, `Adoption baseline: 6d7d589032831e643157ee3708dc8dd085ab0d0e` (commit de **son** histoire) | **181 essais, 144 échecs**, 10 ignorés, 27 réussis |

Les 144 blocs `FAIL` portent tous `the comparison term is unavailable` ; **aucun** échec d'une autre cause (`ERROR` : 0). Ce sont les chiffres du brief (144 / 10 / 27). Le projet dérivé relié passe son propre `audit` (il a son histoire) : `PASS: DECISION_VOLUMES_CONSISTENT — 2 living decision(s); 1 bound in …; bound at 6d7d589`. Premier essai vérifié isolément : `test_a_new_not_started_copy_passes_bootstrap_audit`, même message, en 0,09 s.

## D. `main` du squelette l'a-t-il déjà corrigé ?

Non. `main` = `0e74009` = `v3.20.0` (`e39d4fa`) + vue régénérée + `TPL-D-075` ; aucun tag ni entrée de journal après la 3.20.0 ; `tests/test_template.py` de `main` a l'empreinte du manifeste 3.20.0 et porte la fixture décrite en B. Cohérent avec le brief : la montée d'Alpha vers la 3.20.0 avait fait tourner la suite au vert le 20 septembre **avant** la reliure du même jour.

## E. Inventaire — les autres fichiers copiés tels quels portent-ils une référence à l'histoire du projet dérivé ?

Méthode : lecture de `reset_to_not_started_fixture()` et de tous les appels Git du contrôleur qui prennent un commit lu dans un document ou un record (`show`, `cat-file -e`, `merge-base --is-ancestor`, `rev-list`).

| Fichier (`docs/governance/` sauf mention) | Sort dans la fixture | Cite un commit de l'histoire du projet ? | Résolu par le contrôleur ? | Exposé ? |
|---|---|---|---|---|
| `HUMAN_DECISIONS_VOLUME_1.md` | **copié tel quel** | oui (`Adoption baseline:`) | oui (`decision_volumes_audit`) | **OUI — le défaut** |
| `HUMAN_DECISIONS.md` — blocs `## HD-NNN` (dont `Legacy baseline commit:` / `Authorities baseline commit:`) | retirés | oui | oui (`legacy_baseline`, `frozen_decision_refs`) | non (déjà neutralisé) |
| `HUMAN_DECISIONS.md` — sommaire du volume (`- HD-NNN (…)`) | **laissé** | non (désigne le volume, pas un commit) | seulement si le volume existe | non aujourd'hui ; incohérent avec « fixture vierge » → retiré par la correction |
| `project_control/project-state.v1.json` (`legacy_baseline`, `authorities_baseline`, `baseline_head`) | réécrit | oui | oui | non (déjà neutralisé) |
| `WORKTREE_REGISTRY.md` (entrées `PROJECT_CONTROL:WI-…`) | entrées retirées | oui (heads) | via les records | non |
| `roadmap-state.v1.json`, `ROADMAP.md`, `git-path-classifications.v1.json`, `ideas-state.v1.json`, `IDEAS.md`, `ROADMAP_VIEW.md` (marqueur `head`) | vidés / supprimée | la vue : oui | la vue : `cat-file -e`, sans erreur si absente | non |
| `project_control/{work-items,conversations,agent-runs,deployments}/*.json` (`base_head`, `start_head`, `close_head`, preuves) | supprimés | oui | oui | non |
| `REPOSITORY_STATUS.md` (`CANONICAL HEAD`, `CANONICAL BASELINE`) | copié tel quel (`CANONICAL BRANCH` réécrit par `configure_ready_for_closeout`) | possible | **non** — seul `CANONICAL BRANCH` est lu | non |
| `PROJECT_CHARTER.md`, `DEFINITION_OF_DONE.md`, `MIGRATION_RULES.md`, `RECOVERY.md`, `STORAGE_POLICY.md`, `docs/adr/*`, `docs/architecture/*`, `TEMPLATE_PROVENANCE.md` | copiés tels quels | possible, en prose | non | non |
| `docs/agent-governance/mandatory-documents.v1.json` (routage propre au projet) | copié tel quel | non (chemins) | oui (`DOCUMENT_ROUTING`, existence des fichiers) | non : les fichiers routés sont copiés avec |

Conclusion : le volume 1 est **le seul** document copié tel quel dont le contrôleur compare le contenu à l'histoire Git du projet dérivé. Le sommaire est son satellite : il ne casse rien aujourd'hui (le contrôle rend la main dès qu'il n'y a pas de volume), mais une copie « vierge » qui annonce un volume qu'elle n'a plus est un mensonge de fixture ; la correction le retire avec l'outil du contrôleur (`strip_decisions_summary`, l'inverse exact de ce que `bind` écrit — `REUSE`, pas `REIMPLEMENT`).

## F. Correction proposée — dans la fixture seule

`tests/test_template.py`, `reset_to_not_started_fixture()` : le carnet vivant est lu, débarrassé de son sommaire (`self.control_module.strip_decisions_summary`), puis de ses décisions (règle existante inchangée) ; tout `docs/governance/HUMAN_DECISIONS_VOLUME_*.md` de la copie est supprimé. Diff exact (fixture) :

```diff
+        # The decision registers of a pristine skeleton: one living notebook without a recorded
+        # decision, no bound volume and no summary of one. […]
         decisions_path = root / "docs/governance/HUMAN_DECISIONS.md"
-        decisions = decisions_path.read_text(encoding="utf-8")
+        decisions = self.control_module.strip_decisions_summary(
+            decisions_path.read_text(encoding="utf-8")
+        )
         decisions_path.write_text(
             re.sub(r"(?ms)\n## HD-[0-9]{3,}\s*$.*\Z", "\n", decisions),
             encoding="utf-8",
         )
+        for volume in sorted((root / "docs/governance").glob("HUMAN_DECISIONS_VOLUME_*.md")):
+            volume.unlink()
```

Ce qui ne change pas : `scripts/project_control.py` (aucune ligne ; `DECISION_VOLUMES_CONSISTENT` garde ses trois promesses et son refus fail-closed), le volume 1 des projets dérivés (la copie d'essai s'en passe, le projet le garde), la fixture d'un template ou d'un projet qui n'a rien relié (pas de sommaire, pas de volume : les deux lignes ajoutées ne font rien — le template donne 182 essais verts avec des copies identiques à celles d'avant).

Voies écartées, et pourquoi :
- **Assoupir le contrôle** (accepter une origine introuvable) : interdit par le mandat, et faux — un volume dont l'origine manque ne peut pas être vérifié ; c'est précisément le cas qu'il doit refuser.
- **Reconstruire la fixture depuis les fichiers du template** : un projet dérivé n'a pas les fichiers vierges du template sous la main ; la fixture travaille déjà par soustraction sur les fichiers du projet, la correction suit la même méthode.
- **Donner une histoire à la copie** (rejouer les commits jusqu'à l'origine) : contraire au principe de la copie à un commit, coûteux, et il faudrait aussi rétablir la déclaration de baseline (refus n° 2 en B.4).
- **Un `HUMAN_DECISIONS_VOLUME_*.md` en glob plutôt que la constante du contrôleur** : la doctrine de la fixture est « aucun volume relié », quel qu'en soit le numéro ; le contrôleur 3.20.0 ne connaît que le volume 1 (relier de nouveau est une dette écrite), la fixture n'a pas à dépendre de ce détail.

## G. L'essai qui manquait — B15

`test_the_suite_still_runs_from_a_derived_project_that_bound_its_volume`, placé à la suite des essais « deux volumes ». Il construit un projet dérivé relié avec l'aide existante `bound_project()`, puis, **avec `ROOT` pointé sur ce projet** (`unittest.mock.patch.object`), rejoue trois choses :
1. `make_copy()` → la copie n'a ni volume, ni sommaire, ni décision ; `bootstrap-audit` PASS avec `PASS: DECISION_VOLUMES_CONSISTENT` ;
2. `make_normal_copy()` → `bootstrap-closeout` puis `audit` PASS, même contrôle PASS ;
3. la suite elle-même, en sous-processus depuis le projet dérivé (`python -B -m unittest tests.test_template.GeneralProjectSkeletonTests.test_a_new_not_started_copy_passes_bootstrap_audit`, le premier essai tombé sur le projet réel) → code de retour 0.

Vérifié dans les deux sens : **rouge** sur la fixture 3.20.0 (copie où seul l'essai est ajouté, manifeste régénéré pour isoler la cause : `AssertionError: True is not false : a pristine skeleton has no bound volume`) ; **vert** avec la correction (2,9 s sous Python 3.11 ; 0,8 s dans la VM sous 3.10).

## H. Vérifications du prototype (hors dossier, clone fidèle en espace de session)

| Vérification | Résultat |
|---|---|
| Suite complète du template, prototype 3.20.1 (VM Linux du poste, Python 3.10.12, 4 lots parallèles) | **182 essais, OK**, 0 ignoré, ~38 s |
| Même suite, conteneur Python 3.11.15 (miroir public, avant régénération de la démo) | 182 essais, 1 échec attendu = dérive du transcript (`demo.py --write` non encore lancé), 1 ignoré (miroir) ; l'essai de la démo repasse après régénération |
| Projet dérivé relié **refait sur le prototype 3.20.1**, suite lancée depuis ce projet | **182 essais, 172 réussis, 10 ignorés, 0 échec** (contre 144 échecs sur la 3.20.0) |
| `project_control.py audit` sur le prototype | `PROJECT_CONTROL: PASS` |
| `project_control.py bootstrap-audit` sur l'arbre **non committé** | `BOOTSTRAP_CHANGE_SCOPE` FAIL — attendu : le squelette est en mode amorçage et son garde-fou refuse les chemins du core tant qu'ils ne sont pas committés sous mandat ; PASS attendu sur l'arbre committé (comme à chaque version) |
| `examples/hello-squelette/demo.py --check` | PASS après `--write` (le transcript et le bloc README portent `3.20.1`) |
| `check_git_traceability.py` | les fichiers modifiés sont tous suivis |
| `core-manifest --write --version 3.20.1` | `PASS: CORE_MANIFEST — skeleton_version 3.20.1, 24 core file(s)` ; `CORE_ALIGNED` |

Empreintes du prototype (branche `claude/v3.20.1-fixture-registres-vierges`, encore non committée, dans le clone de session) : `tests/test_template.py` `4053fe8cbd625f98edf52fa2fbd5a4ba371efb257549fd58e9a761e62e935873` ; `provenance/core-manifest.v1.json` `09d8613ec13c03bbe468851e483da72581e1f397dc40b0c556c7561d4cfb6633` ; `README.md` `aee489cbbe46e24c3ae3cf72f3501a608b90c4755afbe33f8e3180ed91333473` ; `examples/hello-squelette/TRANSCRIPT.md` `55c33c41b27841f579adac1f1ae5da6bb05ffff470a372d49bd0b8286487e9fa`. Patch de la fixture et de l'essai : 74 lignes, SHA-256 `d159dc4172b96843e38167ef998257bbdc0ba99250fc69196ac5140b328c3d75`, appliqué à l'identique dans le clone fidèle.

## I. Ce que la livraison écrirait, si elle est confirmée (STOP 1 → STOP 2)

- **Version** : `3.20.1` (correctif : fixture des essais + un essai ; aucune ligne du contrôleur).
- **Branche** : `claude/v3.20.1-fixture-registres-vierges`, depuis `main` à `0e74009` ; `main` intouché, checkout remis sur `main`, aucun tag, aucun push.
- **Fichiers** — commit « version » (`fix(tests): …`) : `tests/test_template.py` (core), `provenance/core-manifest.v1.json` (version + empreinte), `README.md` et `examples/hello-squelette/TRANSCRIPT.md` (régénérés par `demo.py --write`), `provenance/CHANGELOG.md` (`TPL-D-076` + entrée de maintenance), `provenance/roadmap-template.v1.json` (version 3.20.1, état « maintenant », « promouvoir la 3.20.1 » en attente) ; commit « vue » : `provenance/ROADMAP_VIEW.md` régénérée (`roadmap-view --write`).
- **Décisions** : `TPL-D-076` (cadrage + correctif, avec `Folder scope`, `Confirmation 1`, `Confirmation 2` citées) à la livraison ; `TPL-D-077` (promotion) seulement sur ton mot, plus tard.
- **Mécanique** : commits auteur Jeoffrey + trailers Claude, `PROJECT_CONTROL_HOOK_OVERRIDE="TPL-D-076"` (le squelette est en mode amorçage), livrés par `fetch` local du clone fidèle vers le dossier accordé, sans checkout de la branche dans ton dossier.
- **Restent tes gestes** : promotion (`fast-forward` + tag `v3.20.1` + `TPL-D-077`, sur ton mot), push `origin` / `nas`, release GitHub, miroir public ; **montée d'Alpha vers la 3.20.1 = chantier Alpha à part, sous son propre double arrêt** (hors de ce mandat).

## J. Hors périmètre, non fait, dettes

- Alpha : non lu, non copié, non touché (mandat § 5).
- Aucun assouplissement du contrôleur ; aucun `git add .` / `-A`, `reset --hard`, `clean`, force push.
- Dette héritée, inchangée : la copie d'essai emporte encore les fichiers ignorés du dossier de travail (`make_copy`, notée à la 3.17.1) — sans scénario d'échec démontré ici, pas de redline.
- Observation, sans redline : la doctrine de la fixture vit dans deux docstrings (`prune_project_content`, `running_in_the_template`) et un commentaire ; aucun document routé ne dit « un projet dérivé fait tourner la suite du template chez lui ». Si tu veux que ce soit écrit dans `project_control/README.md`, c'est une ligne de plus dans le même commit — à ta décision.

## K. Verdict de diagnostic

`SQUELETTE_3.20.0_SUITE_FROM_BOUND_PROJECT_REQUIRES_MINOR_REDLINE` — un défaut, une cause, une correction locale à la fixture, un essai qui manquait ; aucun conflit d'autorité, aucune entrée manquante.
