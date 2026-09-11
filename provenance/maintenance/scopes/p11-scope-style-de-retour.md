> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# P11 — Style de retour au Project Owner : technique ou simple, au choix de l'utilisateur

Statut : `SCOPE_DEFINITION_V2 — DELIVERED_AND_PROMOTED (v3.7.0, TPL-D-016) — PUSHED — DERIVED_PROJECT_UPGRADE_PENDING`
Révision : V2 (2026-09-07, § 10) enregistre les décisions du Project Owner, la livraison et la promotion ; la V1 du même jour est conservée telle quelle ci-dessous (§ 1 à 9) et n'est pas modifiée rétroactivement.
Nature : définition de périmètre. Aucun code n'est produit, aucun Work Item n'est créé, aucun dossier n'est touché. Toute implémentation exige une décision du Project Owner puis, pour écrire dans le squelette, le double arrêt.
Baseline examinée : `Squelette V3 -runtime-proof`, `main` = `0d5d86f` (`v3.6.1`).
Origine : « je pensais au moment de la configuration du projet proposer d'imposer à l'IA de faire soit un retour technique comme tu le faisais avant, soit tel que tu me réponds maintenant ! Ce doit être le choix de l'utilisateur. » (Project Owner, 2026-09-07). Numérotation : P10 = publication ; P11 est le premier numéro libre.

## 1. Problème

Le squelette impose aux agents des règles de fond (autorités, preuves, double arrêt) mais rien sur la **forme des retours** faits à la personne qui pilote le projet. Aujourd'hui cette forme dépend de l'agent, de la session et de la conversation : un agent rend compte en jargon (chemins, empreintes, verdicts), un autre en langage courant ; la préférence exprimée par le Project Owner vit dans la mémoire d'un outil (celle de Claude, par exemple) et n'est connue ni des autres agents (Codex) ni des sessions suivantes. Le projet — seule chose que tous les agents lisent — ne porte pas cette information.

## 2. Scénarios d'échec démontrés

**S-01 — Une demande mal comprise, une action utile refusée (réel, 2026-09-07).** Une demande de permission, formulée techniquement (« droit de suppression sur le dossier », en réalité les verrous temporaires de Git), a été lue comme « supprimer le dossier source ». Refus, inquiétude, deux échanges pour rétablir, et une opération nécessaire retardée. Une phrase en langage courant sur ce qui allait être effacé exactement aurait suffi ; rien dans le projet n'obligeait l'agent à la produire.

**S-02 — Le style se perd à chaque nouvelle session ou nouvel agent.** Le Project Owner a demandé des retours simples (« je veux des retours explications de ce type désormais ! »). Cette consigne n'existe que dans une mémoire d'assistant : une session Codex, ou une session Claude sans cette mémoire, repart en mode technique par défaut. La préférence n'est pas une autorité du projet, elle n'est donc pas lue au démarrage ni prouvée lue.

**S-03 — Un agent change de registre de lui-même.** Sans règle, un agent alterne selon la complexité du sujet : simple quand tout va bien, technique dès qu'un incident survient — précisément le moment où le Project Owner a le plus besoin de comprendre. Le choix de style doit être une décision de l'humain, stable, pas une appréciation de l'agent au fil de l'eau.

## 3. Objectif

Que le projet porte lui-même, comme donnée de gouvernance, le style de retour choisi par le Project Owner ; que ce choix soit demandé au démarrage du projet, visible dans `status`, obligatoire pour tout agent, et modifiable seulement par décision humaine.

## 4. Non-objectifs

- Ne pas définir une personnalité ni un ton d'agent : c'est une règle de **forme des retours**, pas une persona.
- Ne pas alléger le fond : en mode simple, le contenu technique n'est pas supprimé, il est déplacé dans les rapports et fichiers ; les records, preuves, messages de commit et rapports gardent leur structure.
- Ne pas vérifier mécaniquement le style d'une réponse : le contrôleur ne lit pas la conversation. Il garantit que le choix existe, qu'il est déclaré, affiché et lu (autorité) ; le respect du style relève de la doctrine, comme la lecture effective des autorités.
- Ne pas gérer plusieurs interlocuteurs : le style est celui du Project Owner du projet.

## 5. Contrat proposé

### 5.1 Où le choix vit

`project_control/project-state.v1.json` gagne un champ obligatoire `reporting_style` :

```json
"reporting_style": "PLAIN"
```

Valeurs : `TECHNICAL` | `PLAIN` | `UNKNOWN`. `UNKNOWN` n'est admis qu'en `NOT_STARTED` (la question n'a pas encore été posée) ; `bootstrap-closeout` et tout état `COMPLETE` le refusent nominativement (`project-state: reporting_style must be TECHNICAL or PLAIN`), sur le modèle de `project_owner`. Le schéma `project-state.v1.schema.json` est étendu ; la copie neuve du template porte `UNKNOWN`.

Pourquoi `project-state` et pas le Charter : c'est le seul document lu par le contrôleur, affiché par `status` et présent dans tout projet ; le Charter peut le reprendre en prose, ce n'est pas lui qui fait foi.

### 5.2 Comment le choix est demandé

`FIRST_START.md`, interview obligatoire, une question de plus, posée dans les mots du Project Owner :

> Comment voulez-vous que l'IA vous rende compte ? **Technique** : rapports détaillés dans la conversation même (chemins, empreintes, verdicts, sections). **Simple** : langage courant, en trois points — ce qui s'est passé, ce que ça change, ce que vous devez faire — le détail technique restant dans les fichiers et rapports.

La réponse est enregistrée dans `project-state` et citée dans la Human Decision d'initialisation. Le squelette ne propose pas de défaut : sans réponse, `UNKNOWN`, et la clôture de l'initialisation est refusée.

### 5.3 Ce que l'agent doit faire (doctrine, `AGENTS.core.md`, nouvelle section « Retours au Project Owner »)

- Lire `reporting_style` (il figure dans `status`, première ligne après le projet) avant le premier retour de la session, et s'y tenir toute la session.
- `TECHNICAL` : les retours dans la conversation peuvent porter le détail complet — chemins, lignes, octets, SHA-256, verdicts à vocabulaire fermé, sections lettrées.
- `PLAIN` : chaque retour au Project Owner est en langage courant et répond, dans l'ordre, à trois questions — **ce qui s'est passé**, **ce que ça change**, **ce qu'il doit faire** (rien, ou une action nommée) ; pas de terme technique sans une explication d'une ligne ; le détail (chemins, empreintes, sorties de commandes) va dans un rapport ou un fichier, pas dans la réponse ; un STOP, un refus, un incident se disent aussi simplement, sans les minimiser ; toute demande de permission dit en une phrase ce qui sera exactement touché ou effacé, et ce qui ne le sera pas.
- Dans les deux styles : les records, preuves, rapports, messages de commit et décisions humaines gardent leur forme normative — le style ne s'applique qu'à ce qui est dit au Project Owner.
- Le Project Owner peut demander ponctuellement l'autre forme (« donne-moi la version technique ») sans que le record change ; changer le style du projet est une **décision humaine enregistrée** (`HD-NNN`, `Related Work Item: NOT_APPLICABLE`) qui met à jour `project-state` — jamais une initiative de l'agent.

`CLAUDE.md` : un rappel d'une ligne (« lire `reporting_style` dans `status` et s'y tenir »).

### 5.4 Ce que le contrôleur fait

- `audit` : contrôle `REPORTING_STYLE_DECLARED` — champ présent, valeur admise, `UNKNOWN` refusé après `COMPLETE`.
- `bootstrap-closeout` : refuse `UNKNOWN`.
- `status` : ligne `Retour au Project Owner : simple (PLAIN)` / `technique (TECHNICAL)` juste après la ligne « Projet », et `reporting_style` dans `status --json` — la première chose qu'une nouvelle session lit.
- `project-state` est déjà exclu de l'empreinte de lecture des autorités (`MANIFEST_EXCLUDED_PATHS`) ; le champ est donc porté par `status`, pas par la preuve de lecture. Si le Project Owner veut que la preuve de lecture couvre le style, une phrase dans le Charter (autorité routée) suffit — option, non requise.

### 5.5 Projets existants

Un projet déjà en 3.6.x reçoit le schéma par `template-upgrade` ; l'audit réclame alors la ligne par son nom (`missing reporting_style`) et le Work Item de mise à niveau l'ajoute sous une décision humaine qui cite le choix — exactement le chemin suivi pour `legacy_baseline` et `authorities_baseline`. Pour Alpha : une décision `HD-067`, `"reporting_style": "PLAIN"` si tel est le choix du Project Owner, dans le même Work Item que la mise à niveau vers la version qui l'introduit.

### 5.6 Skill `squelette-projet`

La skill Claude ajoute au préambule : lire `reporting_style` dans `status` et appliquer le style pour tout retour au Project Owner ; en `PLAIN`, la structure « ce qui s'est passé / ce que ça change / ce qu'il doit faire » et la règle « une phrase sur ce qui sera touché » pour toute demande de permission. La skill relaie la doctrine du projet ; elle ne la remplace pas (un agent sans skill la lit dans `AGENTS.core.md`).

## 6. Impacts

- `DIRECT` : `project_control/schemas/project-state.v1.schema.json`, `scripts/project_control.py` (validation, audit, `status`, closeout), `FIRST_START.md` (question), `docs/agent-governance/AGENTS.core.md` (section), `CLAUDE.md` (rappel), `project_control/README.md`, `project_control/project-state.v1.json` du template (`UNKNOWN`), fixture `NOT_STARTED` des tests, `tests/test_template.py`, manifeste (`3.7.0`), `provenance/CHANGELOG.md`.
- `INDIRECT` : tous les projets dérivés ajoutent une ligne à la mise à niveau (nominative) ; les agents doivent lire `status` avant leur premier retour — déjà la première commande prescrite.
- `AUTHORITY` : `AGENTS.core.md` gagne une obligation de forme ; décision humaine du template requise (`TPL-D-0NN`).
- `CONCURRENT` : O-10 (`Folder scope` dans le dépôt cible) et O-09 (documents hors core porteurs de doctrine) sont des maintenances de doctrine du même ordre — à livrer dans la même version `3.7.0` si le Project Owner le souhaite, sinon séparément. La mise à jour de la skill (séquence `context-manifest` → lecture → `start --authorities-digest`, déjà prévue) et celle-ci se font ensemble.

## 7. Décisions du Project Owner

1. **Deux styles ou trois ?** Proposé : deux, `TECHNICAL` et `PLAIN`, tels qu'énoncés (« soit… soit »). Variante possible : un troisième, `PLAIN_WITH_TECHNICAL_APPENDIX` (réponse simple suivie d'un bloc technique) — non recommandé : c'est le rapport qui joue ce rôle.
2. **Portée du style** : la conversation seulement (proposé), ou aussi les rapports ? Proposé : les rapports restent techniques dans les deux cas ; en `PLAIN`, chaque rapport commence par un résumé en trois points pour le Project Owner.
3. **Nom et valeurs** : `reporting_style` / `TECHNICAL` / `PLAIN` — ou des libellés en français dans le record ? Proposé : anglais dans le record (comme tous les champs existants), français dans `status` et la question.
4. **Où pour Alpha** : `PLAIN` dès la mise à niveau vers 3.7.0, sous `HD-067` ? À confirmer.
5. **Livraison** : `3.7.0` seule, ou avec O-10 et O-09 ?

## 8. Critères de fermeture proposés

1. Une copie neuve ne peut pas clore son initialisation sans choisir (`bootstrap-closeout` refuse `UNKNOWN`, test).
2. Un projet `COMPLETE` sans le champ ou avec `UNKNOWN` est refusé nominativement par l'audit ; avec `TECHNICAL` ou `PLAIN`, PASS ; `status` affiche la ligne (test).
3. Un projet 3.6.1 mis à niveau vers 3.7.0 par `template-upgrade` voit l'audit réclamer la ligne, puis PASS une fois déclarée sous décision humaine (test, clone historique).
4. `AGENTS.core.md`, `CLAUDE.md`, `FIRST_START.md`, README à jour ; manifeste `3.7.0` aligné ; suite verte (93 + nouveaux).
5. Skill `squelette-projet` mise à jour et validée par le Project Owner.
6. Aucune dépendance hors bibliothèque standard.

## 9. Limites assumées

Le contrôleur ne peut pas vérifier qu'une réponse est « simple » : il garantit que le choix existe, est visible et lu. Le respect du style est une obligation de doctrine, au même titre que la lecture effective des autorités — détectable par le Project Owner, pas par la machine. La règle des trois questions est un cadre, pas un gabarit rigide : une réponse d'une ligne à une question d'une ligne reste possible.

---

## 10. V2 — décisions, livraison, promotion (2026-09-07, soir)

Statut : `SCOPE_DEFINITION_V2 — DELIVERED_AND_PROMOTED (v3.7.0, TPL-D-016) — PUSHED — DERIVED_PROJECT_UPGRADE_PENDING`
Rédigée par la discussion ROADMAP (P12) à partir du dépôt lu en lecture seule (23:35 puis 23:55) et des décisions enregistrées ; elle ne modifie pas la V1.

### Décisions du Project Owner (§ 7, tranchées le 2026-09-07)

1. Deux styles seulement : `TECHNICAL` / `PLAIN`.
2. Les rapports restent techniques dans les deux cas ; en `PLAIN`, chaque rapport commence par un résumé en trois points.
3. Nom et valeurs : `reporting_style` / `TECHNICAL` / `PLAIN` (anglais dans le record, français dans `status` et la question).
4. Alpha passe en `PLAIN` à sa prochaine mise à niveau, sous sa propre décision humaine (le mot « simple » de la décision de promotion vaut pour le projet dérivé, pas pour le template, dont l'état livré reste `UNKNOWN`).
5. Livraison : `3.7.0` = P11 + O-10 (variante B : `Folder scope` renseigné aussi dans le dépôt cible, avec les deux confirmations) ; O-09 reporté à une version suivante. Décision « ok », puis « simple et promouvoir ».

### Livraison

- Prototype préparé hors dossier (clone de travail en espace de session, `e07ba54` sur `v3.6.1`, 94 tests OK, audits PASS) et transition vérifiée sur un clone jetable de la copie d'Alpha (3.6.1 → 3.7.0 : `missing reporting_style` puis PASS avec `PLAIN`, 94/94).
- Double arrêt : STOP 1 puis STOP 2 « Confirmé : branche claude/v3.7-reporting-style dans ~/Projets/Squelette V3 -runtime-proof, main intouché, pas de push. »
- Branche `claude/v3.7-reporting-style` : `18bff7b` — `feat(v3): style de retour au Project Owner (P11) et Folder scope dans le dépôt cible (O-10)` ; `7964fa4` — `docs(provenance): enregistrer la décision du Project Owner TPL-D-016`. Entrée détaillée dans `provenance/CHANGELOG.md` (contenu, tests, limite assumée).
- Ce qui est implémenté correspond au contrat § 5 : `reporting_style` obligatoire dans `project-state` (`UNKNOWN` seulement en `NOT_STARTED`), question dans l'interview de `FIRST_START.md`, refus nominatif à `bootstrap-closeout` et après `COMPLETE`, contrôle d'audit `REPORTING_STYLE`, première ligne de `status` (« Retour au Project Owner : … ») et `status --json`, section « Retours au Project Owner » dans `AGENTS.core.md`, rappels dans `CLAUDE.md` et `project_control/README.md`, O-10 dans `AGENTS.core.md` et le modèle de `HUMAN_DECISIONS.md` ; un test nouveau ; manifeste `3.7.0` ; 94 tests.

### Promotion et sauvegardes

- `TPL-D-016` — promotion par fast-forward de `main` : `main` = `7964fa4` = tag `v3.7.0` (constaté à 23:34). Contrôles sur `main` : `bootstrap-audit` PASS (20 contrôles, dont `REPORTING_STYLE`), `audit` PASS, `status` : « Retour au Project Owner : non choisi (UNKNOWN) », « Squelette : 3.7.0 | core aligné », hook actif.
- Push `origin` et `nas` faits par le Project Owner : `origin/main` = `nas/main` = `7964fa4` (constaté à 23:55).

### Critères de fermeture (§ 8) — état

1. Copie neuve, clôture refusée sans choix : **rempli** (test, entrée CHANGELOG).
2. `COMPLETE` sans champ ou `UNKNOWN` refusé, `status` affiche la ligne : **rempli** (test).
3. Projet 3.6.1 → 3.7.0 : audit réclame la ligne puis PASS sous décision : **rempli** (vérification sur clone de la copie d'Alpha).
4. Documents et manifeste à jour, suite verte : **rempli** (94/94).
5. Skill `squelette-projet` mise à jour et validée : **en attente** — proposition faite au Project Owner le 7 sept. (carte à enregistrer).
6. Bibliothèque standard seule : **rempli**.

### Suite

- Alpha : mise à niveau de routine `3.6.1 → 3.7.0` par `template-upgrade` sous Work Item, `HD-067` avec `"reporting_style": "PLAIN"` ; cible = l'original → double arrêt avant toute rédaction de mandat ; puis push NAS par le Project Owner.
- Skill `squelette-projet` : enregistrer la mise à jour proposée (lecture de `reporting_style`, séquence `context-manifest` → lecture → `start --authorities-digest`, `acknowledge-authorities`, renvoi de la ROADMAP).
- O-09 (documents hors core porteurs de doctrine) : version suivante, à cadrer.
