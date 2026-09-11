# Definition of Done

`DONE` signifie que le périmètre autorisé et toutes ses gates applicables sont satisfaits. Les niveaux ci-dessous restent distincts : réussir des tests ne prouve ni le déploiement ni le comportement réel en production.

| Niveau | Définition minimale | Preuve attendue |
|---|---|---|
| `DEVELOPED` | Le scope autorisé est implémenté sans changement caché de contrat ou d’autorité. | diff explicite, revue de scope, version |
| `TESTED` | Les tests applicables passent dans un environnement identifié. | rapport de tests et résultats |
| `INTEGRATED` | Le changement est intégré à la baseline candidate et les consumers contractuels restent compatibles. | commit d’intégration, rapport et contract checks |
| `QUALIFIED` | Les exigences fonctionnelles, données, sécurité, performance et recovery applicables sont prouvées. | rapport de qualification et écarts acceptés |
| `CANONICAL` | Un humain autorisé a promu le commit ou artefact comme vérité du projet. | `HD-NNN`, HEAD et hashes |
| `DEPLOYED_IN_CONTROLLED_ENVIRONMENT` | Le commit ou artefact exact est installé dans un environnement contrôlé hors production. | rapport de déploiement et identification de l’environnement |
| `RUNTIME_PROVEN` | Le comportement réel requis a été vérifié dans cet environnement contrôlé. | rapport runtime et résultats observés |
| `DEPLOYED` | Le commit ou artefact exact est installé en production. | rapport de déploiement et autorisation applicable |
| `PRODUCTION_VERIFIED` | Le comportement réel et le rollback ont été vérifiés en production après déploiement. | rapport runtime et human sign-off lorsqu’il est requis |

## Applicabilité et cible

Chaque Work Item déclare séparément `code`, `tests`, `integration`, `deployment` et `runtime_proof`. Un niveau non applicable porte `NOT_APPLICABLE` ; toute applicabilité `UNKNOWN` bloque le preflight et `DONE`.

`runtime_target` fixe les niveaux attendus pour les gates runtime applicables :

| `runtime_target` | Déploiement (si applicable) | Preuve runtime |
|---|---|---|
| `NOT_APPLICABLE` | `NOT_APPLICABLE` | `NOT_APPLICABLE` |
| `CONTROLLED_NON_PRODUCTION_RUNTIME` | `DEPLOYED_IN_CONTROLLED_ENVIRONMENT` | `RUNTIME_PROVEN` |
| `PRODUCTION` | `DEPLOYED` | `PRODUCTION_VERIFIED` |

Le couplage est à sens unique et le contrôleur l’applique : sans cible runtime, `deployment` et `runtime_proof` sont `NOT_APPLICABLE` ; avec une cible runtime, `runtime_proof` est obligatoirement `APPLICABLE`, tandis que `deployment` reste déclaré séparément — `APPLICABLE` si le Work Item installe lui-même le commit ou l’artefact, `NOT_APPLICABLE` pour une preuve runtime sur un déploiement préexistant. Un déploiement sans preuve runtime est refusé.

Un projet sans runtime n’a pas à atteindre les niveaux de déploiement ou de preuve runtime. `RUNTIME_PROVEN` ne vaut jamais `PRODUCTION_VERIFIED`. Les niveaux `QUALIFIED` et `CANONICAL` gardent leurs exigences propres ; `close` ne les attribue pas automatiquement.

## Preuves de clôture

Chaque gate applicable de tests, intégration, déploiement et preuve runtime exige un rapport JSON local et ses artefacts, selon le [contrat Project Control](../../project_control/README.md#format-des-preuves). Un texte libre, un fichier absent, une empreinte différente ou un rapport `FAIL` ne suffit pas.

Le contrôleur vérifie la structure, le Work Item, le niveau, la cible, le commit concerné, les références Git et les empreintes. Ces contrôles rendent les déclarations inspectables ; ils ne certifient pas indépendamment que les essais ou observations rapportés ont réellement eu lieu. L’auteur du rapport doit fournir des résultats honnêtes et reproductibles, et les décisions humaines requises restent obligatoires.

Règle essentielle : `DONE != TESTS_PASS`.

## Clôtures antérieures à la baseline d’adoption

Un projet qui adopte le contrôleur avec un historique déclare une baseline d’adoption (`legacy_baseline` dans Project State, par décision humaine). Les Work Items `DONE` à ce commit restent figés tels qu’enregistrés : leurs preuves ne sont ni reconstruites ni requalifiées, et toute modification de leur record est refusée. Ils ne sont pas `DONE` au sens des règles ci-dessus ; ils sont `DONE` au sens du contrat en vigueur à leur clôture, et `status` les distingue (`LEGACY_PRESERVED`). Tout Work Item clos après la baseline satisfait intégralement les règles ci-dessus.
