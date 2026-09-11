# Idées du Project Owner

Status: `EMPTY`

Cette vue humaine est synchronisée avec `ideas-state.v1.json`. Une idée est une phrase du Project Owner, citée dans ses mots, datée, avec un état ; elle ne décide rien — l’autorisation reste une Human Decision et un Work Item. Une idée ne quitte jamais la liste par oubli : seulement par `REALIZED` ou `DISCARDED`. Une nouvelle copie ne précharge aucune idée.

## États

`EVOKED` évoquée · `TO_CLARIFY` à clarifier · `TO_SET` à régler · `SCOPED` cadrée · `PLANNED` planifiée · `IN_PROGRESS` en cours · `REALIZED` réalisée · `APPLIED` appliquée (devenue une règle) · `INTEGRATED` intégrée (absorbée par un chantier ou une version) · `LATER` plus tard · `DISCARDED` écartée (la cible nomme la décision qui l’écarte).

La cible (`Cible`) pointe, quand elle existe, vers le Work Item (`WI-NNN`), la version ou la décision (`HD-NNN`) qui porte l’idée.

## Idées

| ID | Date | Idée | État | Cible | Source |
|---|---|---|---|---|---|

Aucune idée n’est préchargée. Enregistrer une idée avec `idea add`, la faire évoluer avec `idea set` ; ne pas synchroniser manuellement les deux représentations.

## Synchronization rule

`project_control.py audit` compare l’identifiant, la date, la citation, l’état, la cible et la source entre Markdown et JSON, vérifie l’unicité des identifiants, les états admis et l’existence des cibles. Toute divergence est fail-closed.
