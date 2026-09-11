# Repository Status

`CANONICAL REPOSITORY: NOT_YET_ESTABLISHED`

`CANONICAL BASELINE: NOT_YET_ESTABLISHED`

`CANONICAL HEAD: UNKNOWN`

`CANONICAL BRANCH: UNKNOWN`

`PRODUCTION REPOSITORY: NOT_DEPLOYED`

`PRODUCTION HEAD: NOT_DEPLOYED`

`BACKUP: TODO(PROJECT_OWNER)`

`LAST FULL QUALIFICATION: NOT_RUN`

`PRODUCTION CUTOVER: NOT_AUTHORIZED`

## Signification des champs

- `CANONICAL REPOSITORY` : dépôt unique autorisé à porter la vérité Git du projet.
- `CANONICAL BASELINE` : commit qualifié servant de point de départ aux Work Items.
- `CANONICAL HEAD` : commit actuellement déclaré canonique, jamais déduit d’un checkout sale.
- `CANONICAL BRANCH` : branche protégée qui porte le HEAD canonique.
- `PRODUCTION REPOSITORY` : dépôt ou artefact réellement déployé.
- `PRODUCTION HEAD` : commit exact en service.
- `BACKUP` : emplacement, type, date et preuve de restauration de la sauvegarde.
- `LAST FULL QUALIFICATION` : dernière preuve couvrant tests, contrats, données et recovery requis.
- `PRODUCTION CUTOVER` : autorisation humaine explicite de mise en production.

Les champs ne sont mis à jour qu’avec preuve Git/documentaire et, pour les promotions/cutover, un `HD-NNN`. `UNKNOWN` ne doit jamais être remplacé par une supposition.
