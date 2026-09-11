# Runtime Proof Capability Pack

Capability optionnelle pour prouver de manière bornée et reproductible le comportement réel face à un runtime ou une dépendance externe.

`SUPPORT_IMPLEMENTED != SUPPORT_TESTED != SUPPORT_RUNTIME_OBSERVED != RUNTIME_PROVEN != PRODUCTION_VERIFIED`

`DISCOVER -> QUALIFY -> AUTHORIZE -> ACQUIRE -> INTERPRET -> PUBLISH`

La réussite d’une étape n’autorise jamais implicitement la suivante.

## Utilisation dans le core

Le champ `runtime_target` du Work Item déclare le niveau requis. Les rapports de
clôture utilisent `project_control/schemas/evidence.v1.schema.json` et des fichiers
suivis sous `reports/evidence/WI-NNN/`. `close` vérifie leurs références, leur
cohérence et leur intégrité ; il n’exécute pas lui-même un test live.

Les contrats, patterns et tests attendus de ce pack sont des modèles à adapter,
pas une activation de runtime ou une preuve acquise. Le schéma
`contracts/runtime-proof.v1.schema.json` décrit un compte rendu optionnel ; il ne
remplace pas le contrat core des rapports consommés par `close`.
