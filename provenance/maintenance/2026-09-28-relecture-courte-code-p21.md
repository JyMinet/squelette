> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Relecture courte du code P21 — corrections de la 3.21.0

1. **Ce qui s’est passé.** Les six reproductions de la première relecture et le scénario supplémentaire de signature sont désormais fermés. La vérification ciblée a trouvé une régression : un type particulier de fichier nommé `copie.json` bloque le contrôle au lieu d’être refusé.
2. **Ce que ça change.** Les pertes précédemment démontrées ne se reproduisent plus avec leurs scénarios. La correction du parcours de `.git` demande encore une retouche avant livraison ; aucun nouvel effacement indu n’a été démontré.
3. **Ce que Jeoffrey doit faire.** Faire corriger le blocage décrit en C, puis faire rejouer son scénario et les tests avant livraison. Aucun correctif ni aucune livraison n’a été effectué pendant cette relecture.

## A — Preflight

Date : 2026-09-28. Mandat : `MANDAT-RELECTURE-COURTE-CODE-P21.md`. Références lues : gouvernance applicable, `RELECTURE_CODE_P21.md`, sondes précédentes, `CONTRE-REVUE-RELECTURE-CODE-P21.md`, différences du contrôleur, des essais ciblés et de la doctrine. Relecture limitée aux corrections et à leurs conséquences ; aucune reprise de l’audit général du contrôleur.

| Vérification | Résultat |
|---|---|
| Branche / commit relus | `claude/p21-tableau-des-cles` / `2b4b64606c330b53a3729ee52e5fe11b1cfa33db` |
| Comparaison | `0ecb5464fdd1e03534dbb32ffc1d487907e4da14..2b4b64606c330b53a3729ee52e5fe11b1cfa33db` |
| SHA-256 du contrôleur | `86307fac9589c7b80e4f3f3e3403998477c54e9539d47befcb073aa38e69fd6f` — conforme |
| SHA-256 des tests | `e27fb846c1a59595ac324d72a7b70282dd8983cedec4c59d1521fe742bf2a5d0` — conforme |
| Python / Git | `3.14.7` / `2.50.1 (Apple Git-155)` |
| Livrable / dossier V2 à l’arrivée | Tous deux absents |

Clone créé par la commande prescrite dans `revue-code/v2/clone`. Tout essai utilise `TMPDIR=~/Projets/squelette-chantier-p21/revue-code/v2/tmp`, `PYTHONDONTWRITEBYTECODE=1` et `GIT_OPTIONAL_LOCKS=0`. Fixtures, décisions et commits d’essai portent le marquage « FIXTURE DE RELECTURE — FICTIF, N'AUTORISE RIEN » ; ils n’engagent aucun projet réel. Les anciennes sondes ont été adaptées dans V2, sans modifier leurs originaux ni le code relu.

## B — Fermeture de R01–R06 et C-01

Les chemins des scripts et journaux ci-dessous sont relatifs à `revue-code/v2/` ; les localisations du code renvoient au commit relu dans son clone. Les sondes se rejouent avec `python3 -B <script> [argument]`, depuis la racine accordée, avec l’environnement de A. `FERMÉ` porte sur le scénario du constat initial ; les régressions sont distinguées en C.

| Constat | Verdict | Rejeu et preuve observée |
|---|---|---|
| **R01 — ancien OID de reflog omis** | **FERMÉ** | `inventory/probe.py reflog` → `inventory/reflog.log`. Le commit conservé seulement par l’ancien OID apparaît comme `reflog:<sha>` ; retour sans preuve refusé, code 1. La lecture `rev-list --parents --reflog --not --all` remplace l’intersection fautive, avec contrôle des erreurs (`scripts/project_control.py:1683–1694`). |
| **R02 — origine d’export non protégée** | **FERMÉ** | `inventory/probe.py export` → `inventory/export.log`. Après retrait de la dernière branche conservant l’origine, `copy check` refuse `COPY_COVERAGE` et nomme `origin:<sha>`, code 1. L’origine est désormais un élément inventorié et couvert (`:3416–3421`, `:3444–3446`). |
| **R03 — sérialisation ambiguë** | **FERMÉ** | `root/probe_digest.py` → `root/digest.log`. Même lien contenant tabulation/LF, puis ajout du fichier après abandon préfixé : deux empreintes différentes, `COPY_CONTENT FAIL`, fichier conservé. Les paires triées sont sérialisées en JSON avec échappement ASCII (`:1777–1784`). |
| **R04 — programme lancé par clone partiel** | **FERMÉ** | `root/probe_config.py` → `root/config.log`. Même objet arbre manquant et faux transport local : retour refusé pour `partial clone`, code 1 ; `CONFIG_EXECUTED False`. La détection intervient avant la lecture d’objet (`:1531–1554`, `:1657–1659`). |
| **R05 — écriture depuis registre hérité** | **FERMÉ** | `cleanup/probe_stray.py` → `cleanup/probe_stray.log`. Le même `copy close` depuis un clone sans fiche est refusé : `inherited from the original at …`, code 1. Aucun commit créé, deux registres restés `OPEN`. Vérification d’origine ajoutée aux mutations (`:3489–3497`). |
| **R06 — copie imbriquée dans les hooks** | **FERMÉ** | `cleanup/probe_nested_registered.py` → journal homonyme `.log`. Deux originaux et deux ouvertures réelles de fixture : refus de dépôt imbriqué et de sa fiche ; retour refusé malgré l’abandon préfixé. Seconde copie toujours `OPEN`, travail conservé. Parcours ajouté de tout `.git` (`:1511–1529`). |
| **C-01 — programme de signature via reflog** | **FERMÉ** | `root/probe_signature.py` → `root/signature.log`. Commit à signature fictive et `log.showSignature=true` : inventaire corrigé sans exécution, puis retour sans exécution. Témoin sur la même fixture : l’ancienne commande `reflog show` lance bien le faux programme. Le remplacement par `rev-list` ferme donc le scénario, sans simplement rendre la fixture inopérante. |

## C — Nouveaux constats et vérifications ciblées V-08

### P21-V2-N01 — MAJOR — Le nouveau parcours bloque sur un tube nommé `copie.json`

**Scénario.** Dans un clone de fixture déjà rendu et dont `copy check` passe, créer un FIFO — un tube nommé, sans programme écrivain — à `.git/hooks/copie.json`. Lancer le véritable `copy check`. L’ancien code refuse rapidement ce fichier spécial ; le code corrigé reste bloqué en essayant de lire sa prétendue fiche.

**Localisation.** `scripts/project_control.py:1526–1527`, dans `nested_copies_in_git_dir`, appelle `nested_slip_refusal` pour toute entrée portant ce nom. À `:1505`, celui-ci passe à `read_copy_slip` sans exiger un fichier régulier. Pour les hooks, le premier parcours avait déjà constaté le fichier spécial ; le second attend néanmoins l’ouverture du tube par un écrivain et empêche de restituer le refus.

**Reproduction :**

```sh
export TMPDIR=~/Projets/squelette-chantier-p21/revue-code/v2/tmp
export PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0
python3 -B revue-code/v2/cleanup/probe_fifo.py \
  revue-code/v2/cleanup/stray-3yqbynxu
```

Cette fixture provient de `probe_stray.py`, puis de `probe_v08.py <fixture>` qui effectue son retour. Les scripts conservent les commandes, bornent les sous-processus et retirent le tube dans leur nettoyage. Preuve : `revue-code/v2/cleanup/probe_fifo.log`.

```text
V2_CLI_BEFORE_FIFO_RC 0
OLD_CODE_INVENTORY_RC 0
refusals: [".git/hooks/copie.json: a special file (...) — not supported"]
seconds: 0.12424033274874091
V2_CLI_TIMEOUT 3.004 seconds; child killed and waited
PARTIAL_STDOUT None PARTIAL_STDERR None
V2_CLI_AFTER_FIFO_RC 0
FIFO_REMOVED True
```

Le code de sortie 0 du témoin ancien est celui de la sonde : son résultat contient bien le refus d’inventaire. Le dépassement de trois secondes du code corrigé a nécessité l’arrêt du sous-processus. Même blocage reproduit sous `.git/objects/review-fixture/copie.json` (`probe_v08.log`). Aucun effacement ni perte de travail n’est revendiqué ; la garantie écrite de refus des fichiers spéciaux n’est plus tenue (`docs/agent-governance/AGENTS.core.md:353–355` et contrat de `copy_walk`, `scripts/project_control.py:1436–1438`, qui prévoit précisément le risque d’attente sur un tube). Ce problème est introduit par la correction de R06.

**Correction proposée.** Vérifier le type par `lstat` avant de lire une fiche détectée ; refuser explicitement les entrées non régulières et conserver l’exclusion des liens. Ne jamais ouvrir un tube, socket ou périphérique pour déterminer s’il contient du JSON. Ajouter les deux cas, hooks et dossier technique, avec refus rapide et processus terminé. Aucun correctif appliqué dans cette relecture.

**Autres vérifications ciblées :**

- **Histoires de R01 :** six commits orphelins, deux chaînes réunies par un merge et une histoire indépendante donnent deux obligations distinctes. Importer le merge ne couvre pas l’autre histoire, qui reste refusée jusqu’à son abandon exact (`inventory/histories.log`).
- **Origine d’export R02 :** un nouveau retour vide ne répare pas la couverture perdue ; l’abandon exact de l’origine passe. Une modification ultérieure de `source/README.md` reste refusée jusqu’à un nouveau retour explicite ; l’ancienne empreinte cesse alors de passer (`inventory/export-returns.log`).
- **Origine renommée / table :** refus sans correspondance ; `PROJECT_CONTROL_PATH_MAP` reliant l’ancien chemin déclaré au nouveau chemin local permet retour et contrôle sans réécrire la provenance. Retour à la place initiale : succès sans table. Cela conserve la sémantique déclarative de la table et la conséquence assumée du renommage (`cleanup/probe_v08.log`).
- **Clones ordinaires / repli transport :** clone ordinaire accepté, `promisor=false` sans faux refus, configuration incluse avec `promisor=true` détectée. Variable `GIT_NO_LAZY_FETCH` retirée dans la sonde : refus anticipé maintenu et transport SSH refusé sans lancer le faux programme (`root/partial-v08.log`). C’est une simulation limitée du flag ignoré sur Git 2.50.1, pas une exécution sur une ancienne version de Git.
- **Durée du parcours :** environ 0,11–0,13 s pour la fixture ordinaire ; 0,16 s après ajout de 5 000 fichiers ordinaires dans `objects/`, sans faux refus. Mesure locale, pas une borne générale. Ces simples fichiers restent hors inventaire selon la limite écrite (`cleanup/probe_v08.log`).

## D — Suite complète

**217/217 tests distincts PASS** : aucun échec, erreur, test ignoré, manque ou doublon. Suite inchangée de `tests.test_template`, importée normalement depuis `revue-code/v2/clone`, répartie en trois tranches disjointes de 73, 72 et 72 tests. Les trois processus se sont terminés avec le code 0, en 410,559 s, 330,199 s et 406,670 s respectivement, pauses de lecture des scripts comprises.

Exécution : `python3 -B revue-code/v2/regression/run_shard.py <1|2|3>`, avec l’environnement de A ; le lanceur se place dans le clone. Les quatre scripts d’effacement générés ont été archivés et lus intégralement avant autorisation locale de reprise, avec leurs cibles vérifiées dans `revue-code/v2/tmp/`.

Preuve nominative exhaustive : `revue-code/v2/regression/suite-217-results.json` ; synthèse : `suite-summary.log` ; sorties : `shard-1.log`, `shard-2.log`, `shard-3.log` dans le même dossier. Les deux empreintes de A restent conformes après les tests et le clone relu reste propre. La réussite de la suite ne couvre pas le scénario FIFO ajouté par cette relecture.

## E — État du dossier en fin de mandat

Le contrôle des SHA-256, cibles des liens et modes des **10 881 fichiers et liens préexistants** ne relève aucun changement, retrait ni ajout hors des sorties autorisées. Cela inclut `.git`, l’ancien rapport et tous les anciens sous-dossiers de `revue-code/`. Preuves : `revue-code/v2/original-before.json`, `verify_preexisting.py` et `original-verification.json`.

Le dépôt original reste sur `main`. `git rev-parse main claude/p21-tableau-des-cles`, avec `GIT_OPTIONAL_LOCKS=0`, conserve respectivement :

```text
b9fe0e7bd91ab02a9cda967fdddd6c51b56d13c8
2b4b64606c330b53a3729ee52e5fe11b1cfa33db
```

Écritures limitées à `revue-code/v2/` et au présent livrable, créé exclusivement. Aucun changement du produit, aucun envoi en ligne. Les scripts d’effacement exécutés par les tests ont été lus avant exécution et ne ciblaient que des fixtures de V2. Les tubes de la reproduction ont été retirés et les sous-processus arrêtés puis attendus. Les preuves et les autres copies d’essai sont conservées ; conformément au mandat, Jeoffrey effacera `revue-code/` avant le retour du dossier de chantier.

## F — Verdict terminal

**CODE_P21_V2_REQUIRES_MAJOR_REDLINE**

R01–R06 et C-01 sont fermés sur leurs reproductions. Le nouveau constat `P21-V2-N01`, de gravité `MAJOR`, reste à corriger. La relecture n’autorise ni livraison, ni promotion, ni intervention hors du dossier accordé.
