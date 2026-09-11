# First Start — Governed Initialization Procedure

`INITIALIZATION_STATUS: NOT_STARTED`

FIRST_START est une procédure d’initialisation. Après sa clôture, les autorités permanentes sont le Charter, l’architecture, les ADR, les Human Decisions, la roadmap et Project Control.

## Lifecycle des contrôles

```text
NOT_STARTED
    ↓
BOOTSTRAP_MODE (allowlist fail-closed)
    ↓
bootstrap-closeout PASS + Human Decision
    ↓
FIRST_START et Project State → COMPLETE
    ↓
NORMAL_MODE (preflight Work Item obligatoire)
```

Bootstrap Mode autorise seulement les écritures de gouvernance nécessaires à l’interview, à la validation et à la création du premier Work Item. Il n’autorise aucune fonctionnalité, donnée de domaine, activation, intégration externe, runtime ou déploiement.

## Avant toute écriture d’initialisation

1. lire intégralement FIRST_START, AGENTS et les autorités routées ;
2. exécuter `python3 -B scripts/project_control.py bootstrap-audit` ;
3. produire l’Impact Map et le Conflict Gate ;
4. déclarer les chemins prévus avec `bootstrap-preflight --path <path>` ;
5. conserver `UNKNOWN` pour toute information non établie ;
6. ne jamais écrire hors allowlist.

## Interview obligatoire du Project Owner

Établir et faire confirmer :

- nom du projet et `project_key` éventuel ;
- problème, résultat attendu et critères de réussite ;
- utilisateurs, opérateurs, consommateurs et rôles ;
- périmètre et non-objectifs ;
- inputs, outputs, sources et données éventuels ;
- classification des données, y compris irremplaçables et reconstruisibles ;
- systèmes externes et dépendances ;
- sécurité, confidentialité et accès ;
- architecture, frontières, owners et contrats ;
- runtime cible ou `NOT_APPLICABLE` ;
- niveau d’automatisation et validations humaines ;
- risques et tolérance au risque ;
- applicabilité des tests, intégration, déploiement et preuve runtime ;
- **style de retour** : comment le Project Owner veut que l’IA lui rende compte — `TECHNICAL` (rapports détaillés dans la conversation même : chemins, empreintes, verdicts, sections) ou `PLAIN` (langage courant, en trois points : ce qui s’est passé, ce que ça change, ce qu’il doit faire ; le détail technique reste dans les fichiers et rapports). Le choix est enregistré dans Project State (`reporting_style`) ; sans réponse il reste `UNKNOWN` et la clôture de l’initialisation est refusée.
- **langue** : dans quelle langue l’IA s’adresse au Project Owner — `FR` ou `EN`. Elle gouverne la prose qui lui est destinée (`status`, vue roadmap). Les noms de vérifications et les messages de refus restent en anglais : ce sont des identifiants, pas du texte. Le choix est enregistré dans Project State (`language`) ; sans réponse il reste `UNKNOWN` et la clôture de l’initialisation est refusée.

L’assistant distingue faits, hypothèses et inconnues, reformule, puis demande validation. Il ne déduit jamais une décision absente.

## Records autorisés pendant Bootstrap Mode

- `project_control/project-state.v1.json` : identité, clé facultative, owner, `reporting_style` et `language` choisis par le Project Owner, et transition ; `legacy_baseline` et `authorities_baseline` restent `null` pour un projet neuf (ils ne se renseignent que par une décision humaine d’adoption d’un historique existant, respectivement pour les preuves de clôture et pour la preuve de lecture des autorités) ;
- `project_control/conversations/*.json` : référence provider-agnostic, sans copie intégrale ni secret ;
- `docs/governance/HUMAN_DECISIONS.md` : décisions humaines réelles ;
- `project_control/work-items/*.json` : premier Work Item interne `WI-NNN` ;
- `docs/governance/ROADMAP.md` et `roadmap-state.v1.json` : résumés synchronisés ;
- `docs/governance/IDEAS.md` et `ideas-state.v1.json` : les idées dites par le Project Owner pendant l’interview, dans ses mots (`idea add`, sans commit en Bootstrap Mode) ; `project_control/roadmap-view.v1.json` et `docs/governance/ROADMAP_VIEW.md` : réglages et vue générée de la ROADMAP (`roadmap-view --write`) ;
- `project_control/agent-runs/*.json` : seulement si une exécution d’initialisation doit être tracée.

Un `project_key` est facultatif. Avec `project_key = ALPHA` et `WI-001`, la référence d’affichage est `ALPHA-001`. Sans clé, elle reste `WI-001`. La clé ne change jamais l’identifiant interne ni les règles du contrôleur.

## Livrables avant clôture

Le Project Owner valide explicitement :

1. Project Charter et non-objectifs ;
2. sources/données ou leur non-applicabilité ;
3. architecture initiale et ownership ;
4. Anti-Octopus Review sans inconnue bloquante ;
5. ADR initiaux acceptés ou explicitement non applicables ;
6. Human Decision structurante ;
7. Conversation de référence ;
8. roadmap humaine/machine synchronisée ;
9. premier Work Item `AUTHORIZED` ;
10. `bootstrap-closeout` sans erreur.

## Closeout explicite

Exécuter :

```bash
python3 -B scripts/project_control.py bootstrap-closeout \
  --path FIRST_START.md \
  --path project_control/project-state.v1.json
```

Après PASS seulement :

1. enregistrer la preuve de closeout dans Project State ;
2. mettre `INITIALIZATION_STATUS: COMPLETE` ici ;
3. mettre `initialization.status: COMPLETE` dans Project State avec Human Decision, date et baseline HEAD ;
4. committer cette transition explicitement. Le garde-fou de commit protège la branche
   canonique et refusera ce commit-là : il se fait avec le mandat humain explicite prévu pour cela,
   `PROJECT_CONTROL_HOOK_OVERRIDE="HD-NNN: clôture de FIRST_START"`, qui est imprimé dans le rapport
   du commit et reste donc visible ;
5. exécuter `project_control.py audit`.

Dès `COMPLETE`, Bootstrap Mode est refusé. Tout travail ultérieur utilise `project_control.py preflight WI-NNN` sur une branche dédiée. Un retour vers `NOT_STARTED` exige une décision humaine de recovery ; il n’est jamais implicite.

## Utilisation quotidienne

Dès la baseline Git autonome créée, installer la gate de commit dans le checkout :
`python3 -B scripts/project_control.py install-gate`. Elle est copiée hors de l’arbre de
travail, là où aucun commit ne peut l’emporter, refuse tout commit dont l’audit du mode
courant échoue et protège la branche canonique ; `status` dit d’où elle s’exécute. La
relancer après chaque montée de version du squelette.

Après initialisation, commencer par `python3 -B scripts/project_control.py status`.
Il indique aussi si la vue ROADMAP est à jour ; `roadmap-view --write` la régénère
depuis les fichiers du dépôt, et une idée du Project Owner s’enregistre par `idea add`
dans la session où elle est dite (voir `docs/agent-governance/ROADMAP_VIEW.md`).
L’agent lit ensuite les seules autorités applicables au travail prévu. Il produit
les records et preuves pendant le travail ; le propriétaire n’a pas à les remplir
manuellement. La branche canonique doit être déclarée dans REPOSITORY_STATUS
avant le closeout. L’autorisation du premier Work Item doit être commitée avec
l’initialisation avant son démarrage. Après `COMPLETE`, les transitions de Project
Control (`create-work-item`, `start`, `block`, `resume`, `close`) s’exécutent depuis la
branche canonique et committent elles-mêmes leurs records.
