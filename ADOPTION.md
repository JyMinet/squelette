# Adoption minimale de V3

> **Portée.** Ce document décrit l'adoption du socle par un projet **déjà gouverné** par une version
> antérieure du squelette. Un dépôt qui n'a jamais été gouverné ne dispose pas encore d'une procédure
> d'import : l'initialisation refuse le code métier déjà présent sous `applications/`, `modules/` ou
> `shared/`, et `legacy_baseline` ne l'exempte pas — il concerne des Work Items historiques, pas du code.
> Limite connue, à cadrer avant d'être ouverte.

> **Vous démarrez un projet neuf ? Ce document n'est pas le vôtre.** Exportez l'arbre suivi du
> squelette **sans** son `.git`, créez une baseline Git autonome, installez le garde-fou
> (`install-gate`), puis donnez `FIRST_START.md` à votre agent : c'est lui qui conduit
> l'initialisation, de l'interview du Project Owner jusqu'au premier Work Item.
>
> Exportez avec `git archive`, pas en copiant les entrées visibles du dossier : le squelette a un
> fichier suivi dont le nom commence par un point, `.gitignore`, qu'un gestionnaire de fichiers ne
> montre pas et n'emporte donc pas.
>
> ```bash
> mkdir mon-projet
> git -C <dossier du squelette> archive HEAD | tar -x -C mon-projet
> cd mon-projet && git init -b main
> ```
>
> Le README détaille la suite sous « Try it ».

Commencer avec le core : instructions, décisions, Work Items et contrôles locaux.
L’agent gère les records et les vues ; le propriétaire donne l’objectif, les
limites et les décisions importantes. Aucune nouvelle validation n’est nécessaire
pour répéter une étape déjà autorisée dans le même périmètre.

Avant d’ajouter une capacité : besoin concret → solution minimale → décision
humaine documentée, comme l’exige [AGENTS.md](AGENTS.md) pour toute activation.
Une capacité n’est jamais adoptée parce qu’elle existe.

Préférer `REUSE > ADAPT > REIMPLEMENT`, mais aussi `OMIT > ACTIVATE WITHOUT NEED`.

## Histoire figée : la baseline d'adoption

Un projet qui a des Work Items antérieurs au contrôleur ne les migre pas : il fige son
histoire à un commit d'adoption, `legacy_baseline` dans `project_control/project-state.v1.json`,
et le contrat courant s'applique à tout ce qui suit. La déclaration est **ancrée à sa décision** :
la décision humaine qu'elle cite nomme le commit exact, dans son propre champ —
`Legacy baseline commit: <commit>` (et `Authorities baseline commit: <commit>` pour la baseline de
la preuve de lecture). Une décision qui a autorisé une ligne ne peut pas en déclarer une autre.
Retirer une baseline ou la déplacer est un geste à part, et ce sont deux gestes. La **retirer**
(`null`) exige une décision du chantier qui le dit (`Legacy baseline removed: <commit>`) ; la
**déplacer** exige une nouvelle décision d'ancrage qui nomme le nouveau commit (`Legacy baseline
commit: <nouveau commit>`), descendant de l'ancien — une baseline ne recule jamais ; le champ de
retrait n'est pas demandé pour un déplacement. Les travaux figés sont relus tels que Git les tient au commit de la baseline.

Un projet dont les baselines ont été déclarées avant cette règle les **confirme** avant de monter :
une décision de confirmation par baseline, qui nomme le commit — c'est lui que le contrôleur
vérifie — et cite la décision d'origine — obligation de rédaction, qu'il ne vérifie pas —, puis
un chantier qui fait citer ces décisions par `human_decision_ref`. `template-upgrade` répète toute
montée avant de l'écrire et refuse tant que le nouveau contrôleur refuserait le projet. Le détail
est dans `project_control/README.md`, « Compatibilité : baseline d'adoption ».

## Runtime : une déclaration unique

Chaque Work Item utilise `runtime_target` :

- `NOT_APPLICABLE` : aucune preuve de déploiement ou runtime exigée ;
- `CONTROLLED_NON_PRODUCTION_RUNTIME` : `RUNTIME_PROVEN`, et déploiement contrôlé
  si le Work Item déploie lui-même ;
- `PRODUCTION` : `PRODUCTION_VERIFIED`, et déploiement si le Work Item déploie
  lui-même.

Cette cible est la déclaration exécutée par Project Control. Elle ne donne pas
à elle seule l’autorisation d’accéder à un service ou de muter un environnement.
Les politiques runtime sont routées avant un travail runtime ; le contrat core
`project_control/schemas/evidence.v1.schema.json` est celui des preuves de clôture.

## Options disponibles

Le dossier `runtime_proof/` fournit des modèles de budget réseau, gestion des
secrets, non-mutation, échantillonnage, replay et panne partielle. Ils sont à
adapter uniquement à un besoin autorisé. Ils ne sont pas des protections réseau
ou des tests exécutables installés automatiquement.

Les schémas et exemples de profil d’adoption du pack restent des modèles
optionnels, sans autorité sur les Work Items. Ne pas créer un deuxième registre
ON/OFF à maintenir en parallèle de leur cible runtime. Les capacités de décision,
journal append-only ou replay restent absentes tant que le projet n’en a pas besoin.

## Exemple et documentation du template

`examples/hello-squelette/` rejoue un changement gouverné complet dans une copie
temporaire (`python3 -B examples/hello-squelette/demo.py`) ; il décrit le template,
pas le projet. Un projet dérivé peut le retirer de sa copie ; ce n'est pas un fichier
core et `template-upgrade` n'y touche jamais.
