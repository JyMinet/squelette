# Artifact Migration Rules

Status: `OPTIONAL — APPLY_WHEN_ARTIFACT_MIGRATION_EXISTS`

Une migration ne doit jamais transformer un ancien cache, export, rendu ou checkout en autorité implicite.

## Gates génériques

1. identifier owner, source, destination et autorité ;
2. classifier l’artefact selon `STORAGE_POLICY.md` ;
3. enregistrer version et intégrité avant/après lorsque pertinent ;
4. travailler dans une destination isolée et réversible ;
5. valider contrats et invariants applicables ;
6. obtenir l’autorisation humaine requise avant promotion, cutover ou suppression ;
7. conserver la provenance et la preuve.

Pour un artefact reconstruisible : `AUTHORIZED INPUTS → VERSIONED PROCESS → VALIDATED OUTPUT`. Les orchestrateurs restent techniques et les règles appartiennent à leur owner.

L’adoption d’une nouvelle version du contrôleur sur un historique de Work Items existant n’est pas une migration : elle fige l’histoire à une baseline d’adoption déclarée (`legacy_baseline`, voir [Project Control](../../project_control/README.md#compatibilité--baseline-dadoption)) et n’en transforme aucun record.

Si le projet ne migre aucun artefact, ce document est `NOT_APPLICABLE`.
