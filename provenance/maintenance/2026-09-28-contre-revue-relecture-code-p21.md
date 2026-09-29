# Contre-revue — Relecture du code P21 par la seconde IA

Date : 2026-09-28, 21:25–22:30 (Europe/Zurich). Auteur : Claude, auteur du code contre-revu — conflit d'intérêt déclaré : chaque constat vise mon code, d'où la vérification par rejeu (un essai automatique par constat, lancé sur le code relu puis sur le code corrigé) plutôt que par argument. Objet : `RELECTURE_CODE_P21.md` (Codex, 27 679 octets, SHA-256 `9f99f44fc65cbe889501fbbe86dc7eb1c1949ea065f53634b13c7c70bb47e838`), verdict `CODE_P21_REQUIRES_MAJOR_REDLINE`, sur le commit `0ecb5464fdd1e03534dbb32ffc1d487907e4da14`.

## Résumé en trois points

1. **Ce qui s'est passé.** Les six constats de Codex ont été rejoués un par un, chacun sous forme d'essai automatique : sur le code qu'il a relu, les six se reproduisent. Aucun n'est rejeté. En fermant le premier, j'en ai trouvé un septième, de la même famille que le quatrième : lire une copie pouvait faire tourner le programme de vérification de signatures que sa configuration nomme.
2. **Ce que ça change.** Les sept sont corrigés dans le dossier de chantier ; chaque essai échoue sur le code relu et passe sur le code corrigé ; les 217 essais passent, dans la copie de travail de la session et sur le Mac. Le dossier de travail de Codex (`revue-code/`) contient ses copies d'essai, avec leurs propres fiches de sortie : tant qu'il est là, le dossier de chantier refusera d'être rendu. Il est jetable ; il s'effacera avant ce retour.
3. **Ce qu'il doit faire.** Faire rejouer par Codex ses reproductions sur le code corrigé (mandat court `MANDAT-RELECTURE-COURTE-CODE-P21.md`, à côté de ce document), puis décider de la livraison.

Verdict : `CODE_P21_REVIEW_OF_RELECTURE_CODE_PASS`

## A — Preflight

| Objet | Constat |
|---|---|
| `RELECTURE_CODE_P21.md` | 27 679 octets, SHA-256 `9f99f44f…e838`, lu en entier |
| Sondes relues | `revue-code/inventory/probe.py`, `inventory/probe_config.py`, `registry/probe_digest.py`, `registry/probe_nested_registered.py`, `cleanup/probe_stray.py`, avec leurs journaux ; lues sans être exécutées |
| Code relu par Codex | `0ecb546` ; `scripts/project_control.py` `e07444e7…`, `tests/test_template.py` `1500f3c4…` — conformes à son preflight |
| Dossier de chantier | `main` à `b9fe0e7`, inchangé ; rien écrit dans `revue-code/` ni dans le livrable de Codex |

## B — Rejeu des constats

Chaque essai a été lancé d'abord sur le code relu (`0ecb546`, Git 2.43), puis sur le code corrigé.

| Constat | Essai | Sur `0ecb546` | Après correction | Verdict |
|---|---|---|---|---|
| `R01` BLOCKER | `test_a_commit_only_the_old_side_of_a_reflog_entry_reaches_is_still_inventoried` | rouge : l'élément `reflog:<commit>` manque, un retour sans preuve passe | vert | CONFIRMÉ |
| `R02` BLOCKER | `test_an_export_is_kept_only_while_the_original_keeps_the_revision_it_came_from` | rouge : `copy check` passe après la suppression de la dernière branche | vert | CONFIRMÉ |
| `R03` BLOCKER | `test_the_content_digest_tells_every_inventory_apart` | rouge : deux inventaires différents, même empreinte | vert | CONFIRMÉ |
| `R04` MAJOR | `test_reading_a_partial_clone_fetches_nothing_and_runs_nothing` | rouge : le faux transport de la copie a tourné | vert | CONFIRMÉ |
| `R05` MAJOR | `test_copy_commands_run_in_the_original_and_nowhere_else` (étendu aux quatre commandes qui écrivent) | rouge : `copy open` accepté depuis le clone | vert | CONFIRMÉ |
| `R06` MAJOR | `test_a_copy_hidden_inside_git_is_refused_wherever_it_hides` | rouge : aucun refus | vert | CONFIRMÉ |

Gravités acceptées telles quelles. Une nuance sur `R03` : le scénario suppose une cible de lien fabriquée (tabulation et saut de ligne), pas un accident probable ; mais la promesse « l'empreinte voit tout changement » était fausse, et la perte a été exécutée — `BLOCKER` maintenu.

## C — Corrections (commit `e8534bf`)

- **`R01`.** Les reflogs se lisent par `git rev-list --parents --reflog --not --all` : tout commit qu'un reflog atteint — du côté ancien comme du côté nouveau de ses entrées — et qu'aucune référence n'atteint entre dans l'inventaire, une ligne d'histoire par élément (son commit le plus récent : l'original qui le garde garde ses ancêtres ; un abandon l'abandonne avec eux). Une erreur de lecture de `HEAD` ou des reflogs refuse la copie au lieu de compter pour vide.
- **`R02`.** L'inventaire d'un export porte l'élément `origin:<commit>` : couvert tant qu'une branche ou un tag de l'original garde la révision exportée, sinon abandonné par son nom. `COPY_COVERAGE` le refait avant tout effacement.
- **`R03`.** `inventory_digest` hache la liste triée des paires en JSON canonique, tout caractère hors ASCII échappé. Pas de transition à prévoir : la 3.21.0 n'est pas livrée, aucun registre ne porte d'empreinte ancienne.
- **`R04`.** Un clone partiel — `extensions.partialClone`, `remote.*.promisor`, `*.partialclonefilter` dans la configuration lue avec ses inclusions, ou un paquet `.promisor` — est refusé avant toute lecture d'objet. En plus : `GIT_NO_LAZY_FETCH=1` (reconnu par Git 2.45 et suivants) et tout transport interdit sur la ligne de commande (`protocol.*.allow=never`), qui prime sur tout fichier de configuration.
- **`R05`.** Les commandes qui écrivent le registre refusent un registre dont une entrée a été écrite par un autre original (« inherited from the original at … »). Conséquence assumée et écrite : un original déplacé ne lance plus de commande `copy` tant qu'il n'est pas revenu à sa place — c'était déjà vrai de ses effacements.
- **`R06`.** Tout `.git` est parcouru : un dépôt, ou une copie enregistrée, qui s'y trouve — parmi les hooks comme dans les dossiers que Git tient pour lui — est refusé, quel que soit l'abandon qui couvre son dossier. Reste une limite écrite : un simple fichier glissé dans `objects/`, `refs/` ou `logs/` n'est pas inventorié.

## D — Constat supplémentaire, trouvé en fermant `R01`

`C-01` — MAJOR, même famille que `R04`. L'ancienne lecture des reflogs passait par `git reflog show`, une commande de journal. Avec `log.showSignature=true` dans la configuration de la copie, elle vérifie chaque commit signé avec le programme que nomme `gpg.program`. Démontré : une copie portant un commit à signature factice a fait tourner un faux programme pendant l'inventaire. Fermé par le même changement que `R01` (lecture par `rev-list`, commande de bas niveau qui ne vérifie rien). Essai : `test_reading_a_copy_verifies_no_signature_with_a_program_it_names`, rouge sur `0ecb546`, vert après. Au passage : `core.alternateRefsCommand` compte parmi les réglages qui ont un sens, et un `.DS_Store` dans `.git` n'est plus une entrée inconnue.

## E — Essais et contrôles

| Lieu | Python | Git | Résultat |
|---|---|---|---|
| Copie de travail de la session, clone propre de la branche | 3.11.15 | 2.43.0 | 217 essais OK (790 s) ; `audit`, `bootstrap-audit` PASS ; export public sans erreur et sans registre |
| Mac, espace de travail de Claude, clone du dossier de chantier hors du dossier monté | 3.10.12 | 2.34.1 | 217 essais OK (155 s) ; `audit`, `bootstrap-audit`, `core-manifest` PASS ; démo et vue à jour |

Les sept essais nouveaux ou étendus ont été relancés contre le code relu : tous rouges.

## F — État du dossier de chantier

- `main` à `b9fe0e7` (extrait, inchangé) ; branche `claude/p21-tableau-des-cles` à `2b4b646` : `e8534bf` (les corrections), `2b4b646` (vue régénérée). Transfert : `transfert/p21-branche-4.bundle` (13 122 octets, SHA-256 `05372575299738b5f547492f8f2b60301cfeaf5956eb8072d12c0d1423e3c204`), vérifié puis récupéré dans la branche.
- Papiers à la racine, hors suivi : le rapport de mesure, le rapport de construction, le mandat de relecture du code, la relecture de Codex, cette contre-revue et le mandat court.
- **Inventaire réel du dossier de chantier, en lecture seule, avec le code corrigé** : 9 081 éléments, dont presque tous viennent de `revue-code/`, et dix refus — tous des copies d'essai de Codex, enregistrées par des originaux fictifs posés à côté d'elles dans `revue-code/`. Hors de ce dossier : la branche et `main` (couverts dès que l'atelier a la branche) et les papiers de la racine, rien d'autre. `revue-code/` étant jetable, il s'effacera avant le retour du dossier de chantier.
- Le fichier verrou vide `.git/index.lock` laissé au tour précédent est toujours là ; il ne gêne rien.

## G — Suite

1. **Relecture courte par Codex** : rejouer ses sondes `R01` à `R06` et le constat `C-01` contre `2b4b646` ; suite complète.
2. Livraison dans l'atelier — double arrêt séparé ; les papiers rangés tels quels sous `provenance/maintenance/`.
3. Promotion — décision séparée.
4. Retour du dossier de relecture et du dossier de chantier ; pour ce dernier, `revue-code/` effacé d'abord.
