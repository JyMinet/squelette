> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Contrôle du squelette 3.18.2 — cinquième passe

1. Deux défauts majeurs sont démontrés : un commit ordinaire peut supprimer un worktree de revue et ses fichiers non committés ; un fichier au nom accentué peut recevoir pendant une fusion du contenu absent de sa branche, avec commit et audit acceptés.
2. Quatre défauts modérés sont également reproduits : fusion renommage/modification refusée, clôture légitime refusée pour un nom accentué, baseline acceptée sous un REJECT répété, et test livré encore dépendant d’un JSON ignoré. Les 157 tests livrés réussissent dans la copie propre. Treize des quinze corrections historiques ont un rejeu indépendant dans cette passe ; deux parcours de montée ne sont pas redémontrés.
3. Aucun correctif produit. La finalisation suit la dernière instruction du propriétaire : uniquement les journaux déjà conservés, leur recroisement et la rédaction, sans nouvelle expérience. Les limites et les deux incidents d’outillage sont consignés en sections 2 et 6.

## 1. État exact et périmètre

Date du contrôle : 11 septembre 2026. Racine exclusivement accordée : `~/Projets/squelette-controle-3.18.2/`. Tous les chemins relatifs ci-dessous partent de cette racine. `source/` est la référence en lecture seule ; les copies, temporaires, scripts de mesure et journaux sont dans `runs/`. Le seul livrable principal est ce fichier.

| Objet | État attesté |
|---|---|
| Source | Branche `main`, propre lors du précontrôle |
| HEAD source | `dba40ea4b4f947f59eea17f1640a0be9a0e91573` |
| Tag `v3.18.2`, commit résolu | `7f8f0b38b9493ad08c0069bdc9aa6ee7505e86fb` |
| Tag `v3.18.1`, commit résolu | `00e02b4bd1db2be760b0a74ba1b40c129866d988` |
| Tag `v3.6.1`, commit résolu | `0d5d86f5960aadbb27b333fced41f6b1b4b0a37d` |
| Différence HEAD / v3.18.2 | `provenance/ROADMAP_VIEW.md` et `provenance/roadmap-template.v1.json`, hors core |
| Produit | Manifeste 3.18.2, 24 fichiers core ; `status`, `audit`, `core-manifest` initiaux PASS |
| Environnement | Python 3.14.0, Git 2.50.1 Apple Git-155, macOS 26.6.2 arm64 |

Preuve d’entrée : `runs/control/preflight.log:1–136`. Les inventaires avant/après comparent **1 354 fichiers, dont 122 hors `.git` et 1 232 dans `.git`** : mêmes chemins, contenus, tailles et permissions, aucun ajout ni retrait. Les deux inventaires ont le SHA-256 `072182ddd43bf00cd44c322b0416c4b39678e3a0650357b3e2abd8329d8565c6` (`runs/control/source-verification.json:1–12`). Les premières lectures précèdent l’inventaire ; les dates d’accès et caches système ne sont pas attestés.

L’assemblage a recalculé les empreintes de **971 pièces** annoncées par les deux sous-rapports achevés : aucune divergence. Il a également comparé les 24 core de la copie de suite et des six scénarios T‑19 avec la source, soit **168 comparaisons**, sans écart après normalisation du premier marqueur FIRST_START. Les volets baselines et régressions conservent séparément leurs 648 et 552 comparaisons. Ces comptes ne constituent pas un inventaire exhaustif de toutes les copies ; les sources fictives de montée et la dérive ADOPTION intentionnelle ne sont pas assimilées à un core intact.

## 2. Méthode, privilèges et écarts au protocole

Les quatre rapports précédents, les changements 3.18.1/3.18.2, les décisions TPL-D-059 à TPL-D-062 et P17 §§ 8–9 ont été lus avant les campagnes. Les autorités FIRST_START, ADOPTION, AGENTS.core et README Project Control ont ensuite été confrontées aux mesures. Les volets sont `runs/merge-baseline/`, `runs/regressions/`, `runs/upgrade-cleanup/`, `runs/t19/` ; les deux premiers ont un `REPORT.md`. Le troisième a des scripts, résultats et journaux, mais son sous-rapport final n’a pas été produit après l’erreur d’outil. Ses preuves retenues ici ont été relues directement, puis recroisées dans `runs/merge-baseline/REVIEW_ASSEMBLY.md`.

Les autorisations du mandat couvrent écritures, exécutions, clones, commits, installation du garde-fou et push local dans la racine. Aucun réseau, aucun push ailleurs que vers `runs/remote.git`. Le seul push est celui de la suite livrée. Aucune écriture ni aucun commit dans `source/` ; aucun correctif ou proposition de code produit.

Les helpers livrés ont servi à préparer l’initialisation et certains records de fixture. Leur **WI-000 DONE est synthétique**. Les créations, démarrages, commits, fusions et clôtures invoqués comme résultats indépendants passent par les vraies commandes du contrôleur intact. Les petits cycles baselines sont documentaires, avec gates explicitement NOT_APPLICABLE. Les programmes de preuve positifs/négatifs sont réellement exécutés ; les formats UTF-16, ANSI et binaires sont des octets synthétiques. Les décisions fictives ne prouvent aucun consentement humain réel.

Les clones sont locaux et sans hardlinks. Certains conservent l’ascendance du squelette ; d’autres sont construits à partir d’une fixture autonome. La simple présence des tags ne transforme pas une fixture actuelle en parcours historique 3.6.1. Les identités Git sont locales et fictives ; les lanceurs neutralisent les configurations système/globale par variables et utilisent des temporaires sous `runs/`, avec Python `-B`. Le code de répétition enlève lui-même les variables `GIT_*` de son sous-processus (`source/scripts/project_control.py:3697`) : l’absence absolue d’influence de configuration globale dans ce sous-processus n’est donc pas attestée.

Les dérogations préparatoires sont déclarées : initialisation fictive, construction du mandat historique REJECT, modification canonique pour les conflits de fusion et HEAD non canonique. **Aucun override ne fonde les six échecs mesurés en section 4.** Le second parent de l’octopus de fixture dépasse le modèle un WI/une branche ; son refus n’est pas classé comme défaut. Un `git merge -m` sans trace du hook n’est pas compté comme preuve du garde-fou : les fusions décisives passent par `--no-ff --no-commit`, puis un vrai `git commit`.

Les interruptions ciblent uniquement les enfants connus des harnais. La trace Python externe suspend le code intact à la fenêtre indiquée, sans remplacer ses fonctions. Le vieillissement des worktrees est obtenu par `os.utime` à moins 1 800 secondes : **aucune attente réelle de trente minutes n’est revendiquée**. Le booléen `a_alive_before_B` est littéral dans le harnais ; la preuve plus étroite repose sur le marqueur de pause, les signaux adressés à l’enfant connu, puis son retour après reprise.

**Incidents et décisions utilisateur.** La lecture initiale de la pièce jointe à son chemin fourni, hors racine, était nécessaire pour connaître le mandat ; aucun autre projet n’a été ouvert. Une tentative `ps -Ao pid,command` a ensuite été refusée (`operation not permitted: ps`). Les campagnes ont été suspendues, sans substitut global. Le propriétaire a expressément autorisé la reprise, précisé que ce geste était extérieur au dossier et demandé de consigner ce qu’il devait attester. Enfin, le sous-agent de montée a terminé en erreur avec le message automatique « This content was flagged for possible cybersecurity risk ». La réponse n’identifie ni commande ni fichier refusé ; elle ne démontre donc pas un refus d’une opération précise du produit. Ce sous-agent n’a pas été relancé après cette erreur. Les mesures non disponibles restent non vérifiées. Les incidents sont transcrits dans `runs/control/EXECUTION_INCIDENTS.md` ; la note `EXECUTION_STOP.md` décrit l’arrêt antérieur, pas l’état final.

Le changement ultérieur de répertoire de travail de l’application n’étend pas le périmètre : toutes les lectures et écritures de finalisation ont explicitement ciblé la racine accordée. Après la demande « sans lancer de nouvelle expérience », seuls les fichiers conservés ont été lus, les empreintes vérifiées et les rapports écrits. Aucun contrôleur, Git ou harnais expérimental n’a été relancé.

**Erreurs de préparation conservées.** Le premier scénario `new-rejected-declaration` avait ajouté un deuxième REJECT à deux corps HD identiques par un helper ; les logs 0570/0571 ne sont pas retenus comme témoins REJECT unique. La reprise `new-rejected-declaration-v2` vérifie les cardinalités et fournit le vrai A/B. Les erreurs de chemin lors de lectures et l’omission initiale d’un identifiant de session ne sont pas imputées au produit. Les scripts sont des carnets exploratoires sur destinations conservées, pas des lanceurs idempotents.

## 3. Vérifications thème par thème

### T-16 — Les quinze corrections et leurs interactions

La matrice distingue un rejeu indépendant d’une assertion de la suite. Les preuves détaillées des lignes 1–3, 5–7, 9–10 et 15 figurent aussi dans `runs/regressions/REPORT.md:27–44` ; celles des baselines dans `runs/merge-baseline/REPORT.md:25–47`. Les références ci-dessous visent les fichiers physiques, et leurs empreintes sont indexées en section 7.

| Correction historique | Résultat actuel et preuve indépendante |
|---|---|
| 1 — 3.15.2, brouillons validés par notices | DRAFT/PROPOSED refusés ; documents réellement validés acceptés. `runs/regressions/logs/0009-python3.14.log` et `0011-python3.14.log`. |
| 2 — 3.15.2, close sous mandat REJECT gelé | Audit, actualisation de lecture et close refusent le mandat ; WI demeure IN_PROGRESS. `runs/regressions/logs/0097-python3.14.log`, `0099-python3.14.log`, `0100-python3.14.log`. |
| 3 — 3.15.2, vrai unittest OK avec ERROR attendu refusé | Programme réellement code 0, ERROR/errors=1 attendus ; DONE et audit PASS. `runs/regressions/logs/0044-expected-error.log`, `0048-python3.14.log`, `0049-python3.14.log`. |
| 4 — 3.15.3, adoption ancienne bloquée par nouveaux records | **Pas de nouveau parcours historique complet.** Amorçage couvert par la suite livrée ; cela ne remplace pas 3.6.1 → 3.18.2. |
| 5 — 3.15.3, installation au mauvais emplacement lié | Installation au chemin consulté par Git ; vrai commit interdit refusé, HEAD conservé. `runs/regressions/logs/0109-python3.14.log` à `0114-git.log`. |
| 6 — 3.15.3, index non contrôlable accepté | Index invalide/disque honnête : refus avec snapshot disponible puis indisponible. `runs/regressions/logs/0131-git.log` à `0137-python3.14.log`. |
| 7 — 3.15.3, nouveau passager de fusion masqué | Passager visible ou indexé/absent du disque refusé ; fusion pure acceptée. `runs/regressions/logs/0159-git.log` à `0168-python3.14.log`. La modification d’un chemin accentué déjà présent reste ouverte : F-02. |
| 8 — 3.15.3, ERROR/traceback sans réussite accepté | Programmes réellement code 1 ; leur pièce unique est refusée à close. `runs/regressions/logs/0056-error-only.log`, `0060-python3.14.log`, `0068-real-traceback.log`, `0072-python3.14.log`. |
| 9 — 3.16.2, concurrence perdant des records | Deux créations libres réussissent ; A interrompu/B en attente laisse B réussir et un état cohérent. `runs/regressions/WI-001-free.log`, `WI-002-free.log`, `atomic-concurrent-*`, `0231-python3.14.log`. |
| 10 — 3.16.2, `.gitignore` absent non détecté | Closeout refuse son absence ; allowlist autorise son rétablissement ; vue normale ensuite générée. `runs/regressions/logs/0012-python3.14.log` à `0015-python3.14.log`, `0304-python3.14.log`, `0305-python3.14.log`. |
| 11 — 3.16.2, baseline retirée puis passé réécrit/refixé | Les 14 formes de retrait/malformation sont refusées, deux familles confondues ; retrait sous décision exacte passe. `runs/merge-baseline/results.json`, entrées `shape-*` ; `logs/0513-mandated-removals.log:1–19`. La chaîne d’échec est arrêtée au retrait. |
| 12 — 3.18.0, retrait/recul ajouté pendant fusion | Refus de vrais commits ; même fusion restaurée acceptée et close réussi. `runs/merge-baseline/logs/0062-legacy-merge-remove-refused.log:1–15`, `0067-legacy-merge-remove-control.log:1–16`, `0094-recede-refused.log:1–15` ; authorities : `0493-authorities-merge-refused.log`. |
| 13 — 3.18.0, montée où seul le hook change refusée | Source fictive 3.18.3, simple commentaire de hook et manifeste : répétition, apply, réinstallation, audit réussissent ; FIRST_START reste COMPLETE. `runs/upgrade-cleanup/logs/0061.log:1–17`, `0062.log`, `runs/upgrade-cleanup/results.json:25–33`. |
| 14 — 3.18.0, relance avant commit exécutant ancien HEAD | **Pas de rejeu indépendant de cette recette historique.** Le test livré correspondant passe (`runs/control/suite.log:45–46`). Le HEAD non canonique mesuré ci-dessous est un autre scénario. |
| 15 — 3.18.0, SIGINT laissant le temporaire atomique | Temporaire supprimé, snapshot HEAD/index/fichiers identique ; audit/reprise réussis. `runs/regressions/atomic-single-result.json`, `runs/regressions/atomic-single-child.log`, `0197-python3.14.log`, `0198-python3.14.log`. |

**Interactions de fusion.** Renommage simple, suppression simple, conflit réel sur le même chemin résolu, suppression face à une modification canonique et intégration en deux temps passent. Le renommage combiné à une modification canonique du chemin d’origine échoue : F‑03. L’octopus préparé à deux bras est refusé ; son second bras ne suit pas le modèle un WI/une branche, donc aucun faux refus d’un parcours promis n’est établi. Matrice et preuves : `runs/merge-baseline/REPORT.md:38–47`.

**Commits légitimes de Project State.** Changement FR→EN et TECHNICAL→PLAIN avec les deux baselines, confirmation sans déplacement, déclaration/avance sous champ exact et retrait expressément mandaté réussissent par commit, intégration et close (`runs/merge-baseline/logs/0472-language-style-both-baselines.log:1–19`, `0183-confirm-same-head-commit.log`, `0513-mandated-removals.log`). L’initialisation actuelle réussit dans les fixtures ; le volet baselines a committé COMPLETE avant installation du hook, ce qui ne prouve pas le garde-fou de ce commit. Une adoption ancienne et un commit d’upgrade complet avec baselines ne sont pas redémontrés.

**Ce que répète la montée.** La dérive locale ajoutée dans ADOPTION est refusée sans écrasement ni modification du snapshot, avant répétition (`runs/upgrade-cleanup/logs/0081.log:1–15`). Le contrôleur ne promet donc pas ici de simuler l’application de ce core divergent : il l’arrête. La source où seul le hook change préserve le marqueur COMPLETE. Sur `review-upgrade`, le HEAD `5d80b2…` diffère du canonique `3eb9eb4…` ; la répétition annonce et utilise le HEAD de cette branche (`logs/0104.log:1–16`), sans affirmer répéter le tip canonique. Le message compte zéro fichier core différent pour la source identique. La relance historique après apply non committé reste seulement couverte par la suite.

**Purge et interruptions de répétition.** Le vieux worktree ordinaire et le frais préfixé sont préservés ; l’ancien préfixé est retiré. Mais le worktree humain homonyme et ses voisins disparaissent aussi : F‑01. Une répétition A suspendue avant son audit, vieillie artificiellement, perd son checkout lorsque B fait un dry-run ; B réussit, A repris échoue. Le témoin frais permet aux deux commandes de réussir. SIGINT retire la répétition ; SIGTERM laisse un résidu frais, conservé à la première relance puis retiré après vieillissement (`runs/upgrade-cleanup/results.json:46–97`). Les snapshots correspondants portent sur core/manifeste, HEAD et statut ; ils ne prouvent pas l’absence d’objets Git résiduels.

### T-17 — Observations et anciens « non vérifié »

| Observation de la quatrième passe | Mesure actuelle |
|---|---|
| Choix REJECT, DEFER ou contradictoires | REJECT unique refusé ; DEFER et REJECT puis AUTHORIZE acceptés ; deux REJECT identiques acceptés, y compris pour une nouvelle cible effective : F‑05. |
| Champ d’ancrage dans un bloc de code ; ligne vide supplémentaire | Acceptés. Ancrage absent, mauvaise famille ou doublon non vide refusés. `runs/merge-baseline/REPORT.md:66–82`. |
| Confirmation citant en prose l’ancienne décision/cible mais visant un SHA plus récent | Commit, merge et close acceptés ; le champ exact et l’ascendance sont vérifiés, la concordance sémantique de la prose ne l’est pas. `runs/merge-baseline/logs/0203-confirm-prose-old-field-new-commit.log:1–19`, `0206-python3.14.log:1–14`. |
| Recul accepté par audit d’état, refusé au commit ordinaire | La distinction subsiste dans le contrat ; le recul par fusion est désormais refusé. Pas de nouvelle mesure isolant toutes les variantes d’audit d’état. |
| OK préparatoire puis crash réel | Code 1, pièce unique acceptée DONE et audit PASS. `runs/regressions/logs/0080-prep-ok-crash.log`, `0084-python3.14.log`, `0085-python3.14.log`. Limite textuelle déjà documentée. |
| Encodages et binaires | UTF-16, UTF-8 invalide, ANSI précis et binaire seul acceptés ; vide et erreur après 3 420 030 octets refusés. `runs/regressions/formats-result.json`. Pas de généralisation à tous les formats. |
| Pollution de la suite par un fichier ignoré | La copie est corrigée ; le scan JSON échoue encore : F‑06, A/B/A. |
| Objet Git de répétition restant retrouvable | Pas de nouvelle recherche d’objet résiduel. Le commit jetable est créé par le code ; aucune mesure forensique de sa rétention n’est ajoutée. |
| SIGTERM de répétition laissant un worktree | Reproduit ; reprise possible, résidu frais conservé puis purgé après vieillissement. `runs/upgrade-cleanup/results.json:85–97`. |
| SIGKILL dans gate/application, état partiel après apply | Pas de nouveau rejeu. Les résultats des anciennes passes ne sont pas recomptés. |
| Commit pendant interruption de première installation | Désormais mesuré : mode 0644 après interruption, Git ignore le hook et accepte le commit interdit ; audit MISMATCH, réinstallation, prochain commit refusé. `runs/regressions/logs/0242-git.log`, `0244-python3.14.log`, `0245-python3.14.log`, `0247-git.log`. L’installation interrompue n’avait jamais annoncé PASS. |

La reprise point par point des limites A/B/C reportées par la quatrième passe figure en section 6. Une observation acceptée par le contrat étroit n’est pas automatiquement classée comme défaut.

### T-18 — Doctrine confrontée au code et aux mesures

Le tableau couvre les familles de promesses des deux documents principaux. « Suite seule » et « lecture seule du code » ne signifient pas vérification indépendante. Les écarts documentaires démontrés sont distingués en section 5.

| Promesse et source | Confrontation actuelle |
|---|---|
| README Project Control:5–14, status expose état/audit et n’autorise rien | Statut initial observé, PASS, version et core conformes. Pas de nouvel inventaire transactionnel complet de toutes ses écritures internes. |
| README:30–40, records canoniques et transitions atomiques | Cycles, baselines, concurrence et SIGINT exécutés ; cohérents dans les scénarios retenus. Toute combinaison de transitions n’est pas homologuée. |
| README:32, pre-commit « lecture seule » | Faux sans limitation à certains records : purge effective pendant le vrai commit, F‑01/D‑01. |
| README:32, contenu de branche au merge et exception des conflits | ASCII et conflits de même nom tiennent ; accents/tabulation laissent entrer du contenu ajouté (F‑02), renommage/modification bloque un résultat légitime (F‑03). |
| README:34 et AGENTS.core, start/lecture d’autorités | Démarrages réels avec empreinte ; mandat gelé REJECT refusé à la transition courante. Aucune compréhension humaine attestée, conformément à la limite écrite. |
| README:35 et 115–188, close, commits, preuves | Programmes réellement positifs/négatifs distingués ; limites textuelles reproduites. Commit autorisé au nom accentué refusé à close, F‑04. |
| README:43–90, block/resume, conservation après reprise | Suite livrée verte ; pas de nouvelle campagne complète indépendante de ces transitions. Les anciens résultats ne suffisent pas à affirmer une couverture actuelle totale. |
| README:92–105, preuve de lecture et exemptions | Usage réel lors des cycles et refus du mandat REJECT. Les trois contrôles de manifeste et toutes exemptions ne sont pas remesurés un à un. |
| README:107–113 et ADOPTION:55–70, cible runtime et gates | Code/contrats et suite livrée ; aucun nouveau scénario indépendant runtime/deployment dans cette passe. Aucune production validée. |
| README:115–188, format, immutabilité et bornes Git des preuves | Pièces exactes committées, SHA et refus de sorties négatives mesurés ; immutabilité et toutes bornes temporelles ne sont pas intégralement rejouées. Le texte limite correctement la garantie d’authenticité. |
| README:190–207, vue et idées | Génération après rétablissement du gitignore mesurée ; autres paramètres, langues de vue et transitions d’idées : suite seule. Le rythme affiché n’est pas présenté comme ordonnanceur installé. |
| README:209–218, records et identifiants | Concordance des records dans les cycles ; aucune nouvelle promesse d’authentification fournisseur. |
| README:220–255 et ADOPTION:39–47, ancrage et non-recul | Champs exacts, mauvais ancrages et retraits testés. REJECT répété viole désormais la promesse explicite (F‑05). Distinction retrait/avance mal résumée dans ADOPTION, D‑03. |
| README:238–241, histoire figée | Vrai DONE puis baseline et refus de retrait non mandaté ; pas de nouvelle deuxième clôture du même ancien WI. |
| README:259 et ADOPTION:49–52, confirmation de l’origine | Procédure humaine plus forte que sa vérification : champ exact et ascendance seulement ; observation D‑04. |
| README:263, sous-ensemble de JSON Schema | Lecture de contrat et suite ; aucune nouvelle campagne de mots-clés arbitraires. |
| README:267–269, manifeste et normalisation FIRST_START | Manifeste initial et comparaisons d’octets vérifiés ; marqueur COMPLETE conservé pendant apply. Dérive locale refusée avant écrasement. |
| README:271–289, plan, application et répétition | Hook seul mis à jour avec audit exempté correctement ; HEAD non canonique annoncé ; SIGINT/SIGTERM bornés. F13‑02 historique non rejoué indépendamment. |
| README:277, « Sans --apply, rien n’est écrit » | Dry-run peut supprimer une répétition d’une autre session ; il écrit aussi la répétition explicitement décrite à la ligne 289. D‑02. |
| README:279–300, seed et adoption ancienne | Tests livrés verts, pas de parcours indépendant 3.6.1 → 3.18.2. La consigne de passer par le nouveau contrôleur après l’ancien apply est toujours écrite. |
| README:289, retrait « quoi qu’il arrive », « un autre worktree n’est jamais touché » | SIGTERM laisse un résidu ; autre worktree homonyme détruit. F‑01/D‑01/D‑05. |
| ADOPTION:3–24, portée historique et export neuf avec git archive | Export réel 122 fichiers, octets/modes égaux, gitignore inclus. Ni Finder ni adoption d’un dépôt jamais gouverné ne sont validés. |
| ADOPTION:26–35 et 72–88, adoption minimale/options | Doctrine de décision et modèles optionnels ; aucune activation réseau/runtime exécutée ou revendiquée. |
| ADOPTION:90–96, exemple non core | Classification compatible avec le manifeste ; démo vérifiée par la suite, pas nouvelle expérience indépendante. |
| FIRST_START et AGENTS.core, bootstrap et promesses permanentes | Brouillons, gitignore et transitions réelles couverts ; interview humaine, double consentement réel, authentification et toutes règles doctrinales non observables exclus. |

Ce qui est tenu mais insuffisamment expliqué : le refus d’un REJECT unique laisse encore passer DEFER et les choix ambigus ; la reconnaissance des jetables est fondée sur le nom du parent et son âge, pas sur un propriétaire enregistré ou un processus terminé. Ces deux portées ressortent du code et des expériences, alors que les formulations courtes invitent à une garantie plus large.

### T-19 — Un seul angle nouveau : noms de fichiers rendus par Git

Angle choisi après lecture des quatre rapports : le passage des chemins réels aux chemins cités par Git. Il n’était pas ouvert par ces rapports et concerne des noms usuels dans un projet francophone. La règle de contenu introduite en 3.18.1 lit `git diff --name-only`, puis réutilise ces chaînes comme noms de blobs ; c’était un risque concret, pas un thème arbitraire.

Six scénarios ont été **effectivement terminés avant la consigne de finaliser sans nouveaux essais**. Les commandes et retours sont dans `runs/t19/commands.json`, les résultats dans `runs/t19/results.json:1–96`. Le core et le hook sont inchangés. Aucun autre nom ou réglage n’est ajouté à cette couverture.

| Scénario | pre-commit / vrai commit | Suite mesurée |
|---|---|---|
| `resume.py`, contenu ajouté pendant fusion | Refus / refus | HEAD conservé |
| `résumé.py`, même ajout | PASS / accepté | Contenu ajouté dans HEAD, absent de branche ; audit PASS |
| `my file.py`, même ajout | Refus / refus | HEAD conservé |
| `a\tb.py`, tabulation réelle, même ajout | PASS / accepté | Contenu ajouté dans HEAD ; audit PASS |
| `resume.py`, fusion intacte | PASS / accepté | close du commit légitime : DONE |
| `résumé.py`, fusion intacte | PASS / accepté | close refusé ; même commit clos après seul réglage local `core.quotePath=false` |

Deux conséquences sont donc séparées : perte du contrôle du contenu au commit (F‑02), refus d’une clôture honnête (F‑04). Le DONE du dernier scénario ne concerne **pas** le scénario au contenu ajouté.

## 4. Constats classés par gravité

### F-01 — Majeur, P1 : la purge supprime un worktree qui n’appartient pas au contrôleur

**Promesse :** `source/project_control/README.md:289` et `source/provenance/CHANGELOG.md:603–608`, seuls les propres jetables périmés sont retirés, jamais un autre worktree.

**Scénario exécuté.** Dans `runs/upgrade-cleanup/cleanup-legitimate/`, gate installée, créer un worktree lié sur la branche nommée `human-review`, sous `runs/upgrade-cleanup/project-control-upgrade-review/human-review`. Ajouter `uncommitted-review.txt` dans le worktree et `meeting-notes.txt` à côté de lui, dans son dossier parent. Vieillir uniquement le mtime du checkout de 1 800 secondes. Committer ensuite un rapport ordinaire `reports/check.txt` sur main.

Le vrai commit réussit (`runs/upgrade-cleanup/logs/0020.log:1–16`). Le worktree et **tout son parent** ont disparu après ce commit, y compris les deux notes non committées ; la branche Git survit. Préparation, empreintes avant suppression et mesures de présence : `runs/upgrade-cleanup/campaign.py:36–49`, `runs/upgrade-cleanup/results.json:2–15`, liste avant/après `logs/0018.log` et `0021.log`, branche conservée `0022.log`. Les notes étaient des fixtures, pas les documents d’un humain réel. Aucune destruction de commits Git n’est alléguée.

**Témoins.** Le worktree ancien dont le parent ne porte pas ce préfixe et le worktree frais préfixé restent présents ; l’ancien préfixé est retiré (`runs/upgrade-cleanup/results.json:16–24`, `logs/0042.log:1–17`). L’âge est simulé, non attendu en temps réel. Aucun privilège de suppression ou modification de hook ne sert à la mesure : le commit ordinaire déclenche le code produit.

**Extension déjà exécutée.** Deux commandes de répétition : A est suspendue avant l’audit, son checkout vieilli ; le dry-run B le retire, puis A repris échoue `No such file or directory`. Sans vieillissement, les deux réussissent (`concurrency.py:13–22`, `runs/upgrade-cleanup/results.json:46–72`, `logs/0121.log:1–16`, `live-aged-A.stdout:1–13`). Ce test démontre aussi que l’âge seul ne prouve pas la fin de la commande. Ce n’est pas une mesure statistique ni une attente réelle supérieure à quinze minutes.

**Cause bornée :** `source/scripts/project_control.py:3984–4015` retient le préfixe du parent et le mtime du checkout, effectue `worktree remove --force`, puis retire récursivement le parent. Aucun enregistrement de propriété, contenu voisin ou commande vivante n’est vérifié. Impact majeur : perte de fichiers locaux non committés par une opération ordinaire sans demande de suppression.

### F-02 — Majeur, P1 : un nom accentué rend inopérant le contrôle du contenu ajouté pendant une fusion

**Promesse :** `source/project_control/README.md:32`, la fusion emporte le contenu de sa branche, sauf résolution d’un chemin changé des deux côtés.

**Scénario exécuté.** Dans `runs/t19/accent-edited/`, créer/démarrer WI‑001 autorisé pour `modules/noms/résumé.py`, puis y committer `VALUE = "FROM_AUTHORIZED_BRANCH"`. Sur main inchangée depuis le démarrage, ouvrir la fusion sans commit. Remplacer seulement dans le résultat la valeur par `ADDED_DURING_MERGE`, indexer explicitement ce chemin, appeler pre-commit puis le vrai commit. Il n’existe aucun conflit ni modification canonique justifiant une résolution.

Les deux contrôles acceptent. Le merge commit `fccc7311631d1546b5ae37b37695ff265b72b853` contient `ADDED_DURING_MERGE`, tandis que la branche conserve `FROM_AUTHORIZED_BRANCH` ; l’audit suivant passe avec hook installé identique (`runs/t19/logs/0053.log`, `0055.log:1–17`, `0057.log:1–9`, `0058.log:1–9`, `0059.log:1–35`). Aucun override, retrait du hook, panne ou modification du produit.

**Témoins.** Même scénario pour `resume.py` et `my file.py` : refus et HEAD conservé (`0035.log`, `0078.log`). Tabulation réelle dans le nom : acceptation également (`0098.log:1–17`, `0102.log`). Fusion intacte ASCII : commit et close passent (`0120.log`, `0125.log`).

**Explication au code :** les noms échappés/cités de `git diff --name-only` sont conservés tels quels par `git_lines`; `integration_merge_errors` les réutilise pour résoudre les blobs (`source/scripts/project_control.py:2466–2468`, `3059–3085`). Les échecs de résolution ne sont pas refusés ; leurs sorties vides se comparent égales. Le mécanisme explique la différence mesurée, sans généralisation à tous les noms.

**Portée :** entrée dans l’historique d’un contenu métier absent de la branche, puis audit PASS. Le chemin lui-même était autorisé ; la garantie mise en défaut est le contrôle de son contenu supplémentaire pendant l’intégration. Aucun DONE, exécution runtime ni retrait de baseline n’est démontré pour cette variante. Les baselines disposent d’une barrière séparée, qui tient dans leurs replays.

### F-03 — Modéré, P2 : renommage et modification légitimes empêchent l’intégration

Dans `runs/merge-baseline/clones/rename-canonical-modify/`, la branche WI autorisée renomme `docs/merge-fixture/file.txt` en `renamed.txt` sans changer ses trois lignes. Une modification canonique préparatoire, expressément mandatée, change la première ligne du fichier d’origine. Git fusionne automatiquement correctement (`logs/0291-git.log:1–8`). Sans éditer le résultat, le vrai commit refuse le blob de `renamed.txt` comme différent de la branche (`0295-rename-canonical-modify-merge.log:1–15`) ; HEAD est conservé.

Le résultat indexé est un renommage à 100 % des octets canoniques ; `HEAD:file.txt` et `:renamed.txt` ont le même blob `b14a33a72ac9d2bb2af4fe7ed91dea7d0802dcf8` (`0613-rename-auto-result.log:6–9`, `0617-rename-identical-blobs.log:6–7`). Renommage seul et conflit au même nom passent (`0224-rename-merge.log`, `0270-two-sided-conflict-merge.log`).

Le filtre de `source/scripts/project_control.py:3077–3092` ne relie pas le nom d’origine au nom d’arrivée pour reconnaître les changements des deux côtés. La promesse de résolution légitime du README:32 est donc trop étroite dans son exécution. Impact : intégration bloquée, sans perte de données. L’override sert seulement à préparer le parent canonique ; aucun override du commit refusé.

### F-04 — Modéré, P2 : close refuse le commit réellement autorisé d’un fichier accentué

Dans `runs/t19/accent-clean/`, WI‑001 autorise exactement `modules/noms/résumé.py`. Le commit `57834337b6359fc2abe0f7a471feaf9aeb7f72a5` écrit ce fichier ; sa fusion intacte et l’audit réussissent. `close WI-001 --commit <ce SHA>` refuse pourtant : « commit touches nothing this Work Item was authorized to change » (`runs/t19/logs/0148.log:1–15`).

Le seul réglage local `git config core.quotePath false` est changé ; la même commande close, sur le même commit, produit DONE (`0149.log:1–8`, `0150.log:1–15`). Le témoin ASCII passe sans réglage (`0125.log`). Ce réglage est un témoin causal déjà exécuté, pas une recommandation de contournement. Les gates tests/runtime/intégration de ce petit scénario sont explicitement NOT_APPLICABLE ; le code exige le commit intégré.

Le parcours des commits réutilise lui aussi des noms rendus par Git sans les décoder (`source/scripts/project_control.py:5805–5809`). Impact : clôture honnête bloquée selon le nom et la configuration locale. Ce DONE reste distinct du scénario F‑02 au contenu ajouté.

### F-05 — Modéré, P2 : répéter REJECT suffit à faire accepter une nouvelle cible de baseline

**Promesse explicite depuis 3.18.1 :** « Une décision dont l’option choisie est REJECT ne déclare rien » (`source/project_control/README.md:236`).

Dans `runs/merge-baseline/clones/new-rejected-declaration-v2/`, enregistrer sur main deux décisions nommant le même nouveau SHA `2859600fd0efe32c9b4830f7b03c7d4dcd0e662e`. HD‑206 porte un seul `Chosen option: REJECT` ; HD‑207 porte deux occurrences identiques et aucun AUTHORIZE (`logs/0620-rejected-decisions.log:59–90`). Le WI courant possède sa propre autorisation AUTHORIZE pour modifier Project State.

Avancer la baseline en citant HD‑206 : audit et vrai commit refusés, HEAD conservé (`0598-new-single-reject-audit.log:1–34`, `0599-new-single-reject-commit.log:1–17`). Même SHA en citant HD‑207 : audit, commit, fusion et audit final acceptés (`0604-new-double-reject-audit.log`, `0605-new-double-reject-commit.log:1–19`, `0607-new-double-reject-merge.log`, `0608-new-double-reject-post-audit.log:1–34`). Aucun override ne fonde le A/B.

Le lecteur de champ n’obtient pas une valeur unique en présence du doublon ; le refus spécialisé teste REJECT exact, laissant passer l’ambiguïté. Impact : un refus explicitement répété peut enregistrer le déplacement de la référence. Le scénario ne démontre pas qu’un mandat REJECT autorise create/start/close, ni qu’une clôture historique a ensuite été réécrite. L’observation générale des choix contradictoires devient ici une violation de la correction REJECT expressément promise.

### F-06 — Modéré, P2 : le scan JSON livré dépend encore d’un fichier ignoré

Dans `runs/regressions/ignored-pollution/`, exécuter les deux tests inchangés `test_a_new_not_started_copy_passes_bootstrap_audit` et `test_all_json_and_schema_documents_parse` : deux succès (`runs/regressions/logs/0173-ignored-A.log:1–10`). Ajouter seulement `Claude outputs/incomplete-download.json`, octets `{"download":`. `check-ignore` confirme l’exclusion, le statut Git reste vide (`0174-git.log`, `0175-git.log`).

La même commande donne `.E` : la copie bootstrap passe, le scan JSON échoue avec `JSONDecodeError` (`0176-ignored-B.log:1–29`). Retirer ce seul fichier de fixture fait repasser les deux tests (`0177-ignored-A2.log:1–10`). Le produit et les assertions n’ont pas été modifiés.

`fixture_copy_ignore` corrige donc bien la copie ; `source/tests/test_template.py:5466–5467` scanne encore directement les JSON du dossier, hors `.git` seulement. La dette démontrée par deux tests à la quatrième passe n’est soldée que pour l’un d’eux, malgré `source/provenance/CHANGELOG.md:649`. Impact : vérification livrée faussement négative selon un téléchargement ignoré, pas corruption d’un record de projet. Aucune généralisation à tous les contenus ignorés.

## 5. Écarts documentaires, observations non bloquantes et hypothèses

### Écarts documentaires mesurés

| ID | Formulation et ligne | Comportement mesuré / qualification |
|---|---|---|
| D‑01 | README Project Control:32, pre-commit « en lecture seule » ; :289, jamais un autre worktree | F‑01 supprime worktree et parent pendant un vrai commit, dont le rapport affiche `READ_ONLY: true`. Le préfixe et le mtime ne prouvent pas la propriété. Écart documentaire associé au P1, pas second défaut compté. |
| D‑02 | README:277, « Sans --apply, rien n’est écrit » | Dry-run B annonce `DRY_RUN — nothing written` tout en supprimant le checkout A (`runs/upgrade-cleanup/logs/0121.log:4–15`, `runs/upgrade-cleanup/results.json:46–64`). La ligne 289 décrit pourtant une écriture/commit jetable. Il faut distinguer absence d’application du core et absence de mutation ; le texte actuel ne le fait pas partout. |
| D‑03 | ADOPTION:45–46 rapproche retrait **ou déplacement** du champ `Legacy baseline removed` | README:253–255 distingue retrait mandaté et avance sous nouvelle décision d’ancrage. Une avance effective est acceptée sans champ de retrait (`runs/merge-baseline/logs/0203-confirm-prose-old-field-new-commit.log:1–19`, scénario `confirm-prose-old-field-new`). Ambiguïté de procédure démontrée, non défaut de l’acceptation légitime. |
| D‑04 | ADOPTION:49–52 et README:259, confirmer en citant l’origine | La citation de l’ancienne HD/cible en prose ne garantit pas la même cible : parcours divergent accepté. C’est une obligation doctrinale non vérifiée sémantiquement, à distinguer de l’ancrage exact réellement contrôlé. |
| D‑05 | README:289, worktree retiré « quoi qu’il arrive » | SIGTERM laisse un résidu frais ; la relance le conserve, puis le retire après vieillissement (`runs/upgrade-cleanup/results.json:85–97`). Nettoyage différé partiel, pas garantie absolue à l’arrêt. |
| D‑06 | CHANGELOG:649, dette des copies/tests « close » | F‑06 prouve une correction partielle de l’ancien A/B/A : le scan JSON reste dépendant du fichier ignoré. |

Les formulations « contenu de branche », « REJECT ne déclare rien » et l’exception des conflits sont également mises en défaut par F‑02/F‑03/F‑05 ; elles ne sont pas recomptées en défauts documentaires autonomes.

### Observations non bloquantes

Les choix DEFER/contradictoires, le champ dans un bloc de code et le champ vide supplémentaire restent des tolérances de lecture. Les refus des mandats courants restent distincts. Le OK préparatoire suivi d’un crash et les encodages non reconnus restent des limites de l’heuristique textuelle publiée, sans promesse d’authentification des exécutions. Un audit PASS après close refusé laisse le chantier IN_PROGRESS : il ne valide pas la preuve rejetée.

L’installation interrompue avant chmod laisse une fenêtre où Git ignore le hook. Cette fenêtre est désormais mesurée, mais elle était déjà décrite en 3.15.3 ; l’installation n’avait pas annoncé une réussite, et la réinstallation rétablit le refus. Elle n’est donc pas ajoutée comme nouveau défaut de la version.

### Hypothèses restantes

D’autres noms nécessitant une citation Git, d’autres directions de renommage, d’autres topologies de fusion ou d’autres erreurs de résolution pourraient produire des effets voisins. Les mesures présentes ne suffisent pas à les affirmer. La simulation d’âge ne donne pas la fréquence d’une purge de session réellement longue. Aucune de ces hypothèses, ni l’absence d’un essai, ne fonde la redline.

## 6. Ce qui n’a pas été vérifié, et pourquoi

### Limites d’exécution et demandes refusées

- **Inspection globale des processus : refusée, puis exclue explicitement.** `ps -Ao pid,command` devait retrouver une exécution dont l’identifiant de session n’avait pas été transmis, puis permettre de vérifier s’il restait des processus de campagne. Aucune liste n’a été obtenue ; aucun substitut hors périmètre n’a été cherché. La fin des commandes connues peut être établie par leurs retours ou journaux terminés ; **l’absence globale de processus résiduels n’est pas attestée**.
- **Sous-agent de montée : erreur de filtre automatique.** La demande portait sur les replays de montée/purge dans les copies autorisées ; l’outil a terminé son tour avec « This content was flagged for possible cybersecurity risk », sans désigner l’opération arrêtée. Aucun succès n’est déduit de ce silence. Les journaux existants suffisent aux mesures retenues, mais pas au parcours historique 3.6.1 → 3.18.2 ni au rejeu indépendant exact de F13‑02. Aucun sous-rapport final de ce volet n’est inventé. Le message ne permet pas d’attribuer ce refus à une commande Git, un accès de fichier ou une politique de permissions précise.
- **Arrêt des nouvelles expériences demandé par le propriétaire.** La finalisation n’a comblé aucune lacune par un nouveau test. T‑19 reste limité à six scénarios terminés. Les propositions de compléments des agents n’ont pas été exécutées après cette consigne.

### Registre des anciennes limites, point par point

Les identifiants A, B et C sont ceux que le rapport 3.18.0 reprend des trois premières passes. « Mesuré » ci-dessous concerne uniquement cette cinquième passe.

| Point | Traitement actuel et limite restante |
|---|---|
| A1 — historique, tags/HEAD, montée ancienne | Références et historique fournis contrôlés ; **aucun nouveau parcours complet 3.6.1 → 3.18.2**, ni saut exact vers 3.15.2. Les anciens programmes/runs ne sont pas fournis. |
| A2 — essais de garde-fou bloqués | Worktree lié, snapshot indisponible, passager masqué et fenêtre d’installation mesurés. SIGKILL dans le hook et toute interruption d’installation ne sont pas remesurés. |
| A3 — push exclu de la suite ancienne | Tous les 157 tests exécutés, destination du seul push adaptée au bare autorisé. Aucune protection serveur ou destination réseau testée. |
| A4 — formats/exhaustivité/mémoire | UTF-16, UTF-8 invalide, ANSI précis, binaire, vide et 3,42 Mo mesurés. Saturation mémoire et tous formats non testés. |
| A5 — runtime/déploiement/production/réseau/authenticité | Aucun nouveau scénario indépendant des gates runtime/deployment ; suite seule. Production, réseau, signatures, identité et vérité métier non attestés, faute de cible autorisée et de preuve externe. |
| A6 — initialisation sans annexes | Helpers et routage utilisés ; pas de parcours Markdown seul ni onboarding humain aveugle. |
| A7 — toute écriture interne des commandes lecture seule | Intégrité source avant/après mesurée. Aucun nouvel inventaire complet `.git` avant/après de chaque status/audit/core-manifest. Purge et répétition ont des mutations démontrées ; dates d’accès, caches et écritures transitoires non mesurés. |
| A8 — anciens préfixes et écarts de périmètre | Ancienne obligation de préfixe non reprise. Fixtures identifiées sans invalider JSON/binaires. Incidents actuels explicités ; les anciens ne sont pas réexécutés ni effacés. |
| B1 — usage réel plusieurs jours/personnes | Fixtures courtes, aucune exploitation humaine durable. |
| B2 — onboarding/consentement réels | Aucun ; décisions fictives et préparation assistée. |
| B3 — toutes interruptions/pannes OS | SIGINT atomique, attente concurrente, SIGINT/SIGTERM répétition et interruption d’installation mesurés. Coupure électrique, saturation disque, SIGKILL apply et autres fenêtres non mesurés. |
| B4 — tous hooksPath/worktrees/snapshots | Topologies ciblées seulement. Pas de tous hooks tiers, signatures, ACL ou configurations de plateforme. |
| B5 — runtime et authenticité métier | Même borne qu’A5. |
| B6 — formats et anciennes corrections | Matrice bornée A4 ; treize contre-exemples historiques rejoués, deux recettes de montée non redémontrées. Aucun ancien thème supplémentaire ouvert. |
| B7 — effets des runtimes/caches | Même borne qu’A7. |
| B8 — versions intermédiaires/quatre chantiers métier/scripts anciens | Aucun rejeu intégral : scripts/runs historiques absents et arrêt des nouvelles expériences. Des tags présents ne valent pas exécution. |
| C1 — Finder/ACL/quarantaine/xattrs | Export Git réel, 122 fichiers et modes/octets comparés. Pas de pilotage Finder, attributs étendus ou ACL. |
| C2 — deux humains/LLM durablement, probabilités | Deux processus et ordonnancements ciblés, sans statistique ni durée réelle prolongée. |
| C3 — toutes courses block/resume/close | Créations libres et A interrompu/B en attente mesurées ; matrice complète des transitions entre worktrees non mesurée. |
| C4 — authenticité/horodatages des témoignages | Aucune authenticité externe ; les fixtures ne l’attestent pas. |
| C5 — quatre anciens cycles métier | Non répétés ; petits cycles documentaires courants seulement. |
| C6 — runtime/encodages/épuisement/réseau | A4/A5 : formats bornés, pas d’épuisement ni production. |
| C7 — effets système internes | Même borne qu’A7. |

Autres limites propres à la quatrième passe : aucune seconde clôture d’un ancien WI après retrait par fusion, désormais arrêté au retrait ; aucun auto-référencement d’un commit contenant son propre SHA ; aucune confirmation réelle d'Alpha lue hors périmètre ; aucune source hostile, panne matérielle, attente réelle de 600 secondes ou épuisement par accumulation d’orphelins rejoué. La rétention d’objets Git de répétition n’est pas remesurée. Le renommage inverse de F‑03 et toute variante non listée de T‑19 restent hors couverture. Ces limites ne retirent rien aux scénarios effectivement échoués et conservés.

## 7. Registre des preuves décisives

Les lignes sont physiques, comptées depuis 1 ; les empreintes SHA-256 portent sur le fichier entier. `runs/control/evidence-index.tsv` donne le registre général des journaux et pièces d’assemblage ; les deux `EVIDENCE.tsv` des sous-rapports en conservent la sélection initiale, vérifiée sans divergence. Le tableau ci-dessous permet de retrouver directement les pièces décisives. Les scripts sont les recettes, les logs sont les exécutions, les JSON de résultats sont les mesures regroupées : aucun résumé n’est présenté comme un substitut de commande.

| Objet | Chemin | Lignes | SHA-256 |
|---|---|---|---|
| Entrée/version | `runs/control/preflight.log` | 1–136 | `c9dfc1c4533ca683801f27727c90735b663db6009ee2541f216647761ccff66f` |
| Source conservée | `runs/control/source-verification.json` | 1–12 | `e0d036abfd91e05fc54c7daa708d3379a8edc85639e64b61b5eee8804fcdbb0e` |
| 971 pièces recroisées | `runs/control/subreport-evidence-verification.json` | 1–15 | `af66da366dfc3057e6ef51b8c70fa79b8e2574cb3921b0d35b6fb5897d9c3ef9` |
| Core suite/T19 | `runs/control/assembly-core-verification.json` | 1–40 | `e73a66e6c761fa5af9561a50f4573dd989d4b47c474feccd75e35c29ab5e1272` |
| Suite entière | `runs/control/suite.log` | 1, 45–46, 71–73, 224–226 | `d35fa51a6464aface205336ece3e8e1a468d5b072cd327d5c2def694c5d2fbb4` |
| Réception bare | `runs/control/remote-files.json` | 1–7 | `2dc1fdae93496f5e9de02d4b7bfcfc25453ae08f2794941cc55b98b2088dfeac` |
| Incidents outil | `runs/control/EXECUTION_INCIDENTS.md` | 1–25 | `e62de101a1d4261327f220e28b7d75a0977b105a50db283b06b3d0ecfb0b8242` |
| Recroisement P1 | `runs/merge-baseline/REVIEW_ASSEMBLY.md` | 1–35 | `64412c3af2c553ab6930c037b4708b93a07bac100db03039c2aaf83a822b75dd` |
| Purge recette | `runs/upgrade-cleanup/campaign.py` | 35–61 | `8a6cdcf1f23d6e94a1ee8710bdd8986ab8b4c901d9bcabc0604c424a1fcad063` |
| Purge états/témoins | `runs/upgrade-cleanup/results.json` | 2–33, 46–97 | `775d382c560f592429d2902b401957e89569fc396d8981fe73d80babf0307288` |
| Purge vrai commit | `runs/upgrade-cleanup/logs/0020.log` | 1–16 | `b3e1811b64d17008811ec6dd6789f173ed886f8ebb8bb26f44d95297e56df7ca` |
| Worktree avant | `runs/upgrade-cleanup/logs/0018.log` | 1–12 | `c0f2cd938013d4a58ef3411f961fb6b6c0d589d0761c82740872bf798871e1ef` |
| Worktree après | `runs/upgrade-cleanup/logs/0021.log` | 1–8 | `d07ab19caff33bb800f0be3eb52c34179cdde9076afd80630da7088094f01efa` |
| Branche conservée | `runs/upgrade-cleanup/logs/0022.log` | 1–5 | `0ac9720f6f942bae7619bf4f162dcaf992795d044f28e4217116c5d95480bbe5` |
| Témoins purge | `runs/upgrade-cleanup/logs/0042.log` | 1–16 | `acd7251f8b9b71f60fe8ae6b36ba2c3e5e5cbdafba5e781c8130931f0cbace77` |
| Répétition concurrente | `runs/upgrade-cleanup/concurrency.py` | 1–26 | `0ce0db5ff972d2e0424abd39ef9c2899be01496cd16cedaeda5baee62547bf1b` |
| Dry-run B | `runs/upgrade-cleanup/logs/0121.log` | 1–16 | `8f73b33cdb356fbb848092fd1c9277c31c2c32801a06bc669173d5fab9064063` |
| A repris échoue | `runs/upgrade-cleanup/live-aged-A.stdout` | 1–12 | `7e1ecb7196c1cf79034e4aeb3fe26edcd167a22aa87f9acedd6950d507c1b279` |
| Hook seul accepté | `runs/upgrade-cleanup/logs/0061.log` | 1–17 | `80743580aaa82c4b8cd8a9fb593362b9aa994df14c26bf18785f6b5db84aaa8e` |
| Dérive refusée | `runs/upgrade-cleanup/logs/0081.log` | 1–15 | `51497d54dd9745a1b48af4ffcf208a23d7144efd3ed28affd27d60f88826ad95` |
| HEAD non canonique | `runs/upgrade-cleanup/logs/0104.log` | 1–16 | `a0ca362b990378d4fc77a0514793f1e8137f5a36134f1ef776f4df09781b8930` |
| T19 recette | `runs/t19/campaign.py` | 1–91 | `ac4a1a1377edfb550a93c87e714a030887a5b692d34861f24c537d393e963214` |
| T19 six résultats | `runs/t19/results.json` | 1–96 | `8a821e5742354a08d19e4722b67e42275a0948652d249ac56b4f7875c80f88e6` |
| ASCII refusé | `runs/t19/logs/0035.log` | 1–16 | `4590db5c3f66177471f7352f5ba0f875e4308f31fe21b0c39b2b1248867edf45` |
| Accent accepté | `runs/t19/logs/0055.log` | 1–17 | `3370528497b1166c75102d5f1a0ef1b7ce70411b891b7eb68a464046c33acae7` |
| Contenu HEAD | `runs/t19/logs/0057.log` | 1–9 | `4d89a5ad032811883d8fa21e8f1a4cba43c08d3136de57713655a619f9f53e94` |
| Contenu branche | `runs/t19/logs/0058.log` | 1–9 | `6fbb4a6697f88dfb841767b2018fec28bd6e7a616e9df3f496f6b12e3f18a1b7` |
| Audit après ajout | `runs/t19/logs/0059.log` | 1–35 | `90be6dd0eb70d4de10aab6415051fcd54ebd390fc3563a0f3ac51158aaa63a0a` |
| Tabulation acceptée | `runs/t19/logs/0098.log` | 1–17 | `ffc2b91993dbcf2c47aad2be9112d983cafec4b17df8683259994e0679b98afb` |
| Close accent refusé | `runs/t19/logs/0148.log` | 1–15 | `4ee4847ca1bfc1d69dc9742e6f78910c22b5f6da02b2b4894c06a077260a4b1a` |
| Seul réglage local | `runs/t19/logs/0149.log` | 1–8 | `fc3c13ab61f8691c4f55be752f970e76e321735524a93000e3795a3baf5ad238` |
| Close accent accepté | `runs/t19/logs/0150.log` | 1–15 | `639e3a4db27dce53493f77b45f7bfd04aa74c17c2ee7bdfa544d4621ed9bff1d` |
| Fusion renommage Git | `runs/merge-baseline/logs/0291-git.log` | 1–8 | `75b11b2d5cdc06c0c695fa29d14e039ad8b7bc4d293258245247d3c73abe5d4c` |
| Fusion renommage refusée | `runs/merge-baseline/logs/0295-rename-canonical-modify-merge.log` | 1–15 | `800ee582922da500fa9f568381e81d69dcab9b06c4d55a04e9ed40403698a7f4` |
| Blobs renommage égaux | `runs/merge-baseline/logs/0617-rename-identical-blobs.log` | 1–9 | `0ae0912bf2a1e2289f3b980081fc0694c5779f7e99a3b6787e5f76382f0820c7` |
| REJECT inputs | `runs/merge-baseline/logs/0620-rejected-decisions.log` | 59–90 | `990f3d9fe3439c9ceb7f8f7cc75a9c873bec2f7d62be39cca210141e492e6ff4` |
| REJECT simple refusé | `runs/merge-baseline/logs/0599-new-single-reject-commit.log` | 1–17 | `ae1236cfb533c62d817c1c78c19c85aa3f37b7509d0ac7e7e9d4bbead91f98fe` |
| REJECT double accepté | `runs/merge-baseline/logs/0605-new-double-reject-commit.log` | 1–19 | `7ac55556a24c8894beda188aa27c7f44a0d5fc4697280498ef556db544c1abcf` |
| REJECT audit final | `runs/merge-baseline/logs/0608-new-double-reject-post-audit.log` | 1–34 | `7f2cc2ea679e2accf0629e17bb204b6ddf31ad24f4c3d8d55b3a99296bf568e6` |
| Ancienne fusion retirée refusée | `runs/merge-baseline/logs/0062-legacy-merge-remove-refused.log` | 1–15 | `706a507fea14ffe6a59d0547ff5eeb5b33360d75413617f71a3c567f2b2334d6` |
| Fusion restaurée acceptée | `runs/merge-baseline/logs/0067-legacy-merge-remove-control.log` | 1–16 | `99770284c81a0b889207e7b487afe2138c77a20e25b8c4135004a11d2f92b7f7` |
| Confirmation prose divergente | `runs/merge-baseline/logs/0203-confirm-prose-old-field-new-commit.log` | 1–19 | `52d400e0d1939f05eb7142df4486abb3074336d5ef605c853b321f98e910868d` |
| Ignored témoin A | `runs/regressions/logs/0173-ignored-A.log` | 1–10 | `f2fb9344927f0e7eff4de95201ec1a6d4c692c527c7ae4f7624403fe0c7e7bf0` |
| Ignored échec B | `runs/regressions/logs/0176-ignored-B.log` | 1–29 | `e7fc6ab70b85c72ee1282900b8f523cd77855950afa2370bfcbbf808e5a30612` |
| Ignored reprise A | `runs/regressions/logs/0177-ignored-A2.log` | 1–10 | `72747ca2eda44bb7f8b73c3d0985cc429c9c17ca786b63970036359239b8f306` |
| SIGINT snapshot | `runs/regressions/atomic-single-result.json` | 1–265 | `3e2dcb69b60acb49cb852c17b0c64cb331436f6327d06832d6b29d6e71d6bcd2` |
| Installation fenêtre | `runs/regressions/logs/0242-git.log` | 1–10 | `5d095bdd7ef528fa06fa958dd37def9b28723d1d005c774732dc2d4f9dde5e50` |
| Formats | `runs/regressions/formats-result.json` | 1–50 | `2220ba94a1024099bf1d25077162cb074ade807aca358228eba833ea316e8e03` |
| Export | `runs/regressions/export-result.json` | 1–5 | `6daaf96245c30090bbe6688a8cc14b2885cbae7dea5edd43f465b18b188ebab8` |

**Suite livrée, résultat séparé.** `Ran 157 tests in 680.273s`, puis `OK` (`runs/control/suite.log:224–226`), aucun test ignoré. Le lanceur conserve les assertions et fichiers livrés ; il adapte seulement les destinations de `git init --bare` et `remote add backup` vers `runs/remote.git`, et vérifie celle du push (`suite.log:71–73`, `run_suite.py`). Ce n’est pas la commande de découverte strictement inchangée. Le bare contient le commit `3c975d10018916a88b4ff04c92075b3734be3f06` sur main (`runs/control/remote-files.json`), relevé par lecture de ses fichiers de refs pendant la finalisation. La suite verte et l’échec A/B/A avec fichier ignoré concernent deux contextes distincts, explicitement conservés.

La redline repose sur les deux P1 reproduits, et non sur les lacunes de couverture, une hypothèse de code ou une promesse simplement supposée. Le dossier source est identique à l’inventaire initial. Les copies refusées, conflits non committés, notes d’incident et témoins restent des preuves ; aucun nettoyage final n’a été fait pour améliorer artificiellement leurs états.

## 8. Verdict

SQUELETTE_3.18.2_REQUIRES_MAJOR_REDLINE
