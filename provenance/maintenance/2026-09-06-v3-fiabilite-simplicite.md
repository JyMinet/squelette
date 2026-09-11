# V3 améliorée — 6 septembre 2026

Mandat : « donc regarde pour ameliorer notre version V3 ! », après revue de la
V3 et demande de conserver un cadre simple. Conversation Codex :
`01a07390-a662-7013-8526-26d7a87df4c1`.

Baseline examinée : `35da2a2d82520cd735f5c1884fdc5f185254e8f6`.
Branche de maintenance : `codex/v3-fiabilite-simplicite`.
La maintenance est terminée ; cette branche n’est pas une promotion de main.
FIRST_START reste `NOT_STARTED`, identité `UNKNOWN`, roadmap et records projet
vierges. Aucun runtime, service externe ou projet consommateur n’a été modifié.

## Résultat pour l’utilisateur

- Une seule commande `status` pour retrouver la situation et la prochaine action.
  L’affichage courant résume les travaux terminés et détaille ceux qui restent ;
  `--json` expose l’ensemble aux outils. Aucune nouvelle source d’état à maintenir.
- README raccourci de 99 à 57 lignes, détails regroupés dans Project Control.
  L’agent entretient les records ; une autorisation existante couvre les étapes
  ordinaires de son périmètre.
- Les options runtime restent des modèles à adopter selon le besoin. La cible
  du Work Item gouverne les contrôles, sans registre ON/OFF supplémentaire.

## Corrections

1. `start` conserve `base_head`, capture `start_head` sur la branche canonique
   courante, vérifie l’ascendance, refuse les divergences et restaure l’état
   administratif ainsi que la branche si le démarrage échoue.
2. `close` exige des rapports JSON locaux suivis dans Git, reliés au Work Item,
   à la gate, à la cible et au commit concerné. Les artefacts sont vérifiés par
   SHA-256 ; les rapports absents, FAIL, mal formés ou périmés sont refusés.
3. Les preuves historiques sont conservées ; une correction après un échec peut
   fournir une nouvelle preuve PASS. `close_head` fige la baseline de clôture,
   pour que les travaux suivants n’invalident pas les anciennes preuves.
4. Un runtime contrôlé exige `DEPLOYED_IN_CONTROLLED_ENVIRONMENT` et
   `RUNTIME_PROVEN` ; la production exige `DEPLOYED` et `PRODUCTION_VERIFIED`.
   Une clôture avec intégration exige la branche canonique déclarée.
5. Les contraintes du sous-ensemble de schémas utilisé par le core sont exécutées.
   Les records mal formés échouent proprement ; la provenance Run/Work Item doit
   correspondre. Aucune dépendance Python externe ajoutée.
6. Le routage des autorités inclut la procédure d’adoption et les politiques
   runtime pour les travaux concernés. Les modèles du pack ne sont pas présentés
   comme des protections ou tests déjà exécutables.

## Réutilisation et périmètre

Les mécanismes de baseline et de cible runtime ont été adaptés depuis le
contrôleur générique présent dans le projet consommateur, après revue. Son
acceptation de preuves en texte libre n’a pas été reprise. Aucune logique de
domaine ni aucun record de ce projet n’a été importé.

L’Impact Map, le Conflict Gate et le registre de cette maintenance figurent dans
`docs/governance/WORKTREE_REGISTRY.md`. Code, tests et documentation ont été
travaillés sur des périmètres distincts ; une revue indépendante a vérifié les
cas de provenance, de fraîcheur des preuves et de données mal formées.

## Vérification

- Dépôt source de référence avant modification : audit PASS ; 28 tests PASS.
- Version améliorée : **45 tests PASS**, suite complète exécutée en 60,332 s.
- Scénarios couverts : copie vierge, premier démarrage après commit, autorisation
  commitée, branche incorrecte/divergente et rollback, deux Work Items successifs,
  preuves absentes/non commitées/FAIL/fausse empreinte/mauvaise cible/périmées,
  historique FAIL → correction → PASS, contrôlé/production, schémas invalides,
  état en lecture seule et erreur JSON sans traceback.
- Audit du template, traçabilité Git, affichage `status` et `status --json` : PASS.
- `git diff --check` : PASS.

Les fixtures sont synthétiques. Ces résultats prouvent les contrôles locaux,
pas l’exécution d’un système réel ni une validation de production.

## Limites et suite

Les rapports restent des déclarations dont le contrôleur vérifie la cohérence,
les références et l’intégrité. Il ne certifie pas indépendamment la vérité d’une
observation. Les autorisations humaines de production restent obligatoires.

Cette révision ne crée pas un moteur complet de blocage/reprise, un tableau de
bord web ou un système de plugins. Ces ajouts n’ont pas été nécessaires aux
corrections vérifiées ; `status` indique les blocages sans les résoudre.

Une ancienne copie déjà initialisée nécessite une migration explicite des
records et preuves. Ne pas remplacer son contrôleur en place : conserver sa
version jusqu’à conversion et vérification. Le dépôt source historique distinct
n’a pas été mis à jour automatiquement. Pour de nouvelles copies, utiliser
l’arbre suivi de cette branche après revue de son contenu.
