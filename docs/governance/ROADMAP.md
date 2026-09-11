# Roadmap

Status: `INITIALIZATION — EMPTY`

Cette vue humaine est synchronisée avec `roadmap-state.v1.json`. Une nouvelle copie ne précharge aucun chantier. Le premier Work Item est créé et autorisé par le Project Owner pendant FIRST_START.

## Lifecycle

`PROPOSED → AUTHORIZED → IN_PROGRESS → IMPLEMENTED → INTEGRATED → DEPLOYED → RUNTIME_PROVEN → DONE`

États latéraux : `BLOCKED`, `REJECTED`, `SUPERSEDED`.

- `AUTHORIZED` exige une Human Decision enregistrée ;
- `IN_PROGRESS` exige le preflight normal, après clôture de FIRST_START ;
- `DEPLOYED` et `RUNTIME_PROVEN` ne sont utilisés que lorsqu’ils sont applicables ;
- `DONE` exige toutes les preuves applicables et refuse toute applicabilité `UNKNOWN`.

Integration state : `UNMERGED`, `ACTIVE_WORK`, `INTEGRATED`, `HISTORICAL`.

En `NORMAL_MODE`, la roadmap est valide au repos avec tous les Work Items `DONE`
et aucun Work Item `AUTHORIZED` ou `IN_PROGRESS`. Un chantier permanent ou un
Work Item suivant ne sont jamais requis par l’audit.

## Work Items

| Internal ID | Display reference | Work Item | Status | Integration | Human gate | Depends on |
|---|---|---|---|---|---|---|

Aucun Work Item n’est préchargé. Lors de l’initialisation, ajouter chaque résumé
ici et son état équivalent dans `roadmap-state.v1.json`, avec un record complet
sous `project_control/work-items/`. Après initialisation, utiliser
`create-work-item`; ne pas synchroniser manuellement les trois représentations.

## Synchronization rule

`project_control.py audit` compare l’identifiant, la référence d’affichage, le titre, le statut et l’état d’intégration entre Markdown, JSON et le record Work Item. Toute divergence est fail-closed.
