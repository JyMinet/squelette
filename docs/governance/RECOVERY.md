# Recovery Runbook

Status: `TEMPLATE — NOT_QUALIFIED`

Objectif : restaurer un état prouvé sans transformer une copie locale inconnue en vérité canonique. Aucune commande destructive n’est fournie par défaut.

## Préconditions

- incident et recovery owner identifiés ;
- baseline, backups, sources éventuelles et autorités accessibles ;
- nouvelle racine de restauration isolée ;
- actions, versions et hashes journalisés lorsque pertinents ;
- aucune écriture en production sans human GO.

## Procédure

1. Identifier la baseline canonique depuis `REPOSITORY_STATUS.md` et vérifier le commit.
2. Identifier les artefacts `IRREPLACEABLE_PROTECTED` et leur backup restaurable.
3. Restaurer Git et artefacts dans une nouvelle racine sans écraser le checkout sinistré.
4. Reconstruire les artefacts `GENERATED_REBUILDABLE` depuis leurs inputs autorisés et processus versionnés.
5. Exécuter tests, contrats, intégration et invariants applicables.
6. Vérifier hashes, versions et écarts attendus.
7. Exécuter `project_control.py audit` et le preflight du Work Item de recovery.
8. Présenter preuves, risques et rollback au Project Owner; obtenir les gates humains requis.
9. Si un runtime existe, remettre en service progressivement et consigner `PRODUCTION_VERIFIED` ou rollback.

`STOP` si baseline, autorité, classification, source applicable, hash, périmètre ou décision humaine est ambigu. Les projets sans runtime documentent recovery de code/documents/artefacts et marquent le déploiement `NOT_APPLICABLE`.
