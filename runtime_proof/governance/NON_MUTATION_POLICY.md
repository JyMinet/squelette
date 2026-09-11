# Non-Mutation Policy

Une preuve `NON_MUTATING` conserve HEAD, index, worktree, configuration gouvernée et autorités inchangés. Artefacts temporaires uniquement sous une racine contrôlée hors repository.

Interdit par défaut : modification produit, commit, push, tag, WI implicite, changement de configuration, enrichissement opportuniste.

Postflight : `HEAD_FINAL == HEAD_INITIAL`, index/worktree clean, fichiers modifiés = 0, commits = 0, push = none.
