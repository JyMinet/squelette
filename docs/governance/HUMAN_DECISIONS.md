# Human Decisions Register

Ce registre conserve uniquement les décisions humaines structurantes : autorité, périmètre, promotion, activation, canonicalisation, cutover, risque accepté, irréversibilité ou arbitrage de conflit. Il ne copie pas automatiquement les conversations.

Les identifiants `HD-NNN` sont stables, croissants et jamais réutilisés. Une décision superseded reste visible et référence sa remplaçante.

Une nouvelle copie commence sans décision préchargée. Le premier identifiant est attribué pendant l’interview réelle du Project Owner.

## Modèle

Ce bloc est le texte que le contrôleur accepte, à recopier tel quel en remplaçant `NNN` par le
numéro et les `<…>` par leur contenu. Le titre `## HD-NNN` en est la première ligne : c'est lui que
le contrôleur cherche, et sans lui la décision est déclarée manquante alors qu'elle est là.

```text
## HD-NNN

Date: YYYY-MM-DD
Decision: <ce qui est décidé, en une phrase>
Context: <ce qui a conduit à cette décision>
Options considered: AUTHORIZE | REJECT
Chosen option: AUTHORIZE
Reason: <pourquoi cette option et pas une autre>
Scope: <périmètre exact de ce qui est autorisé>
Reversible: YES
Conversation reference: <référence de la conversation | UNKNOWN>
Related ADR: NOT_APPLICABLE
Related Work Item: WI-NNN
Folder scope: NOT_APPLICABLE
Authorized by: <Project Owner>
```

Valeurs admises, quand la ligne en accepte plusieurs : `Reversible` vaut `YES`, `NO` ou `UNKNOWN` ;
`Related ADR` et `Related Work Item` acceptent une référence, `NOT_APPLICABLE` ou `UNKNOWN` ;
`Date` accepte `UNKNOWN`. Écrire **une seule** valeur par ligne : un `<choix>` laissé tel quel est
recopié dans le registre et le contrôleur le lit comme une option qui n'autorise rien.

`Chosen option: AUTHORIZE` est ce qui fait d'une décision un mandat. Une décision qui enregistre un
refus écrit son propre mot — `REJECT`, `DEFER` — et n'autorise alors rien : elle reste au registre
comme trace de ce qui a été refusé.

## Modèle — décision qui sort du dossier accordé

Quand la décision autorise une action hors du dépôt courant (écriture, branche, commit, scripts,
push dans un autre dossier), ou quand elle est enregistrée dans le dépôt cible lui-même après qu'un
agent a franchi un double arrêt pour venir y travailler, elle nomme le dossier et cite les deux
confirmations. Le contrôleur exige `Confirmation 1` et `Confirmation 2`, distinctes et non
`UNKNOWN` ; sans elles la décision n'autorise rien (voir `AGENTS.core.md`).

```text
## HD-NNN

Date: YYYY-MM-DD
Decision: <ce qui est décidé, en une phrase>
Context: <ce qui a conduit à cette décision>
Options considered: AUTHORIZE | REJECT
Chosen option: AUTHORIZE
Reason: <pourquoi cette option et pas une autre>
Scope: <périmètre exact de ce qui est autorisé>
Reversible: YES
Conversation reference: <référence de la conversation | UNKNOWN>
Related ADR: NOT_APPLICABLE
Related Work Item: WI-NNN
Folder scope: <chemin exact du dossier ou du dépôt visé>
Confirmation 1: <première confirmation humaine, citée, nommant le dossier>
Confirmation 2: <seconde confirmation humaine, distincte, nommant le dossier>
Authorized by: <Project Owner>
```

Un travail interne au dépôt, sans sortie de périmètre, porte `Folder scope: NOT_APPLICABLE` et ne
porte pas de ligne de confirmation.
