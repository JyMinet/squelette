# CLAUDE.md

Ce fichier est un point d'entrée, pas une autorité.

L'autorité opérationnelle des agents est `AGENTS.md`, à la racine de ce dépôt, qui inclut le core du squelette `docs/agent-governance/AGENTS.core.md`. Lire les deux intégralement avant toute écriture.

Rappels non négociables :

- lire `FIRST_START.md` et en déduire le mode : `NOT_STARTED` → `BOOTSTRAP_MODE`, `COMPLETE` → `NORMAL_MODE`, statut absent ou contradictoire → `STOP` ;
- lire les autorités routées par `docs/agent-governance/mandatory-documents.v1.json` avant d'écrire, et le prouver : `context-manifest WI-NNN`, lecture, puis `start WI-NNN --authorities-digest <MANIFEST_DIGEST>` ;
- aucune écriture métier sans Work Item autorisé et preflight `PASS` ;
- `UNKNOWN` reste `UNKNOWN` ; ambiguïté d'autorité → `STOP` ;
- jamais `git add .`, `git add -A`, `git reset --hard`, `git clean` ni force push.
- lire `reporting_style` dans `status` avant le premier retour au Project Owner et s'y tenir : `TECHNICAL` ou `PLAIN` (ce qui s'est passé, ce que ça change, ce qu'il doit faire ; le détail dans les fichiers) ;
- toute consigne qui sort du dossier accordé (autre dépôt, autre dossier, remote) → `STOP 1` puis `STOP 2`, deux confirmations humaines distinctes nommant le dossier ; par défaut une copie, jamais l'original d'un projet réel.
- une idée dite par le Project Owner s'enregistre dans la session même, dans ses mots (`idea add`) ; la vue ROADMAP se génère (`roadmap-view --write`), jamais à la main, et ne décide rien ; dans une discussion « ROADMAP <PROJET> », tout message est une régénération et tout le reste est renvoyé ailleurs (`docs/agent-governance/ROADMAP_VIEW.md`).
