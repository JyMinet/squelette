> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# P12 — ROADMAP dédiée : discussion « ROADMAP <PROJET> » et tableau de bord d'avancement

Statut : `SCOPE_DEFINITION_V2 — STEP_1_DONE (page, tâche quotidienne, skills proposées) — STEP_2_PROMOTED (3.8.0, TPL-D-018, § 13.7) — CLAUDE_MIRROR_PENDING`
Révision : V2 (2026-09-08, § 12) cadre l'étape 2 sur la demande du Project Owner (« toutes les infos dans le dossier physique du projet, format JSON ? » → « cadre-le ») ; la V1 (§ 1 à 11) est conservée telle quelle.
Nature : définition de périmètre côté Claude (projet Claude « Squelette »). Aucun code n'est produit dans le squelette, aucun fichier du dépôt n'est touché : P12 n'ajoute rien au core (`OMIT > ACTIVATE WITHOUT NEED`). La première instance a été construite en lecture seule du dépôt, sur le choix du Project Owner « Cadrer P12 + première version depuis le dépôt ».
Baseline examinée : `Squelette V3 -runtime-proof`, `main` = `0d5d86f` (`v3.6.1`) à 23:15, puis `main` = `7964fa4` (`v3.7.0`, TPL-D-016) à 23:35 ; `origin/main` = `nas/main` = `0d5d86f` ; arbre propre ; `bootstrap-audit` PASS (20 contrôles), `audit` PASS, hook actif, core aligné ; 93 puis 94 tests dans la suite (7 sept. 2026).
Origine : « L'utilisateur ouvre un projet. Dans celui-ci il y aura toutes les discussions. L'une d'elles serait le tableau de bord visuel de l'avancement du projet. En l'activant, l'utilisateur n'aurait rien à faire, quel que soit son message il serait ignoré, et l'IA générerait l'avancement, la roadmap du projet. Toutes les anciennes chapitres seraient peu détaillés (avec si c'est possible la possibilité de déployer l'arbre), détails sur l'actuel et le proche à venir, et peu de détails sur la fin. Cette discussion serait systématiquement nommée ROADMAP SQUELETTE. » (Project Owner, 2026-09-07). Précisions du même soir : renvoi des autres demandes vers une autre discussion accepté ; « l'IA choisira sa présentation » ; « régénération automatique toutes les x minutes, l'utilisateur choisira » ; réglages via le squelette « si risque, on le bloque ». Après la première instance : « si je choisis une méthode de conversation simple, je veux un tableau identique. Simple, efficace, lisible par tous, surtout pas pour un ingénieur IT. Et normalement on doit voir apparaître les idées évoquées et donc planifiées. »
Filiation : P6 (guide de continuité, revue du 5 sept. § C) et section D de la même revue (le projet Claude « Squelette » porte l'état du template et des projets qui l'utilisent). Numérotation : P12 est le premier numéro libre après P11.

## 1. Problème

L'état d'un projet gouverné existe, mais nulle part d'un seul tenant. Pour le squelette lui-même : les décisions dans `provenance/CHANGELOG.md`, les chantiers dans les fiches P1 → P11 de ce projet Claude (chacune avec sa propre ligne de statut, parfois en retard), la « prochaine action » dans la mémoire d'un assistant. Personne — Project Owner compris — ne peut lire « où en est-on, qu'est-ce qui vient, qu'est-ce qui m'attend » d'un coup d'œil, et la question « est-ce à jour ? » n'a pas de réponse sans tout relire.

## 2. Scénarios d'échec démontrés

**S-01 — État éparpillé, question sans réponse (réel, 7 sept.).** Le Project Owner demande si le squelette est à jour. La réponse exige de lire le CHANGELOG, les tags, les remotes, cinq fiches et les notes de séance : aucune vue ne l'agrège. Constat de la première lecture : la fiche P11 (V1) est encore `NOT_AUTHORIZED` alors que les décisions ont été prises le soir même ; l'écart n'était visible nulle part.

**S-02 — Une vue tenue de mémoire dérive (réel, 7 sept.).** Les notes de séance disaient « push `origin` + `nas` à faire par lui » ; la lecture du dépôt montre `origin/main` = `nas/main` = `0d5d86f`. Un tableau « généré par l'IA » de mémoire aurait affiché une action en attente qui n'existait plus. Seule une lecture des sources donne l'état vrai — d'où la règle 4.2.

**S-03 — Reprise à l'aveugle (revue du 5 sept., P6).** Une nouvelle session, ou un autre modèle, n'a aucun document qui dise l'état courant, la prochaine gate, ce qui est permis et interdit ; elle repart en relisant tout.

**S-04 — Un tableau qui accepte des décisions (risque de conception, non démontré).** Si la discussion ROADMAP exécutait ce qu'on y tape, une phrase écrite dans une vue d'affichage deviendrait une décision de projet sans le circuit normal (décision humaine enregistrée, double arrêt `TPL-D-011`). Non observé ; nommé ici pour être bloqué par construction (5.6). Décision du Project Owner : « si oui on le bloque ».

**S-05 — Un tableau écrit pour un ingénieur, illisible pour son destinataire (réel, 7 sept.).** La première instance affichait empreintes de commit, noms de commandes et identifiants de décisions dans la lecture principale. Verdict du Project Owner : « très pro », mais pas le tableau qu'il veut en mode simple. Le tableau doit suivre le style de retour du projet (P11) : c'est la même règle que pour les réponses — le détail technique va dans un repli, pas dans la lecture.

**S-06 — Une idée évoquée qui disparaît (réel, 7 sept.).** La première instance ne montrait que les chantiers numérotés ; les idées exprimées en conversation (plugin, sauvegarde, README bilingue, « jamais l'original »…) n'y figuraient qu'implicitement, ou pas du tout. « On doit voir apparaître les idées évoquées et donc planifiées » : une idée exprimée par le Project Owner est une ligne de roadmap avec un état, jamais un oubli.

## 3. Objectif

Un endroit unique, visuel, toujours à la même adresse, qui montre où en est le projet, ce qui vient ensuite et ce qui attend le Project Owner — construit uniquement à partir des sources, sans rien décider, avec le zoom demandé (passé replié, présent et proche avenir détaillés, fin en titres), régénéré à la demande ou automatiquement au rythme choisi.

## 4. Non-objectifs

- Pas de nouvelle source de vérité : le tableau est une vue calculée. Il ne remplace ni `ROADMAP.md` / `roadmap-state.v1.json` / `status` d'un projet dérivé, ni le CHANGELOG du template.
- Pas un canal de décision : rien de ce qui est tapé dans la discussion ROADMAP ne devient une décision, un Work Item, une écriture dans un dépôt.
- Pas de modification du core du squelette pour P12. P6 (guide de continuité généré par le contrôleur, dans le dépôt) reste un chantier distinct et complémentaire.
- Pas de vérification de la lecture effective par l'utilisateur.

## 5. Contrat proposé

### 5.1 La discussion

- Nom : `ROADMAP <NOM DU PROJET>` — ici « ROADMAP SQUELETTE ». Une discussion par projet Claude.
- Activation : le premier message de la discussion (« ROADMAP SQUELETTE — activer », ou l'appel de la skill 5.9).
- Comportement : tout message → régénération du tableau, quel que soit son contenu. Deux exceptions : une phrase qui commence par `RÉGLAGE :` (5.5) ; une phrase qui commence par `STOP ROADMAP` (désactive la convention pour la suite de la discussion). Toute autre demande — question, tâche, décision — reçoit une phrase de renvoi vers une autre discussion, sans exécution. Décision du Project Owner : « Je suis ok avec le renvoi vers une autre discussion ! »
- Limite assumée : Claude ne voit pas le nom d'une discussion ; la convention est tenue par la consigne (skill et document du projet), pas par une serrure.

### 5.2 Sources, par ordre d'autorité

1. **Le dépôt, s'il existe** (lecture seule stricte). Projet dérivé : `status --json`, `ROADMAP.md`, `roadmap-state.v1.json`, `HUMAN_DECISIONS.md`, records Work Item / Agent Run, tags, branches, remotes. Template : `provenance/CHANGELOG.md` (décisions `TPL-D-NNN` et entrées de maintenance), tags, branches, remotes, contrôles read-only (`bootstrap-audit`, `audit`, `status`).
2. **Les fiches du projet Claude** : scope definitions, revues, mandats, comptes rendus.
3. **La mémoire du tableau** (5.8) : dernier état connu, jamais une preuve.

Règles : chaque ligne du tableau cite sa source ; ce qui n'a pas de source est marqué « inconnu » ; une source inaccessible donne « non vérifié depuis <date> » sur les lignes concernées ; le tableau n'invente rien et ne complète rien. Un projet sans dépôt (projet documentaire, ou dossier non accordé à la session) se construit sur 2 et 3 seulement — choix de conception de Claude ; la phrase « on n'est pas obligé d'avoir un dépôt » du Project Owner n'était pas une demande mais une question sur une formulation, retirée par lui (« n'en tiens pas compte », 7 sept.). Lecture seule : `GIT_OPTIONAL_LOCKS=0`, aucune commande Git modifiante, aucun script qui écrit (`python3 -B`, commandes read-only seulement), `git status` vierge avant et après.

### 5.3 Zoom

- **Passé** : arbre replié — une entrée par version ou événement, déployable ; sous-entrées pour les épisodes (répétitions, dérives, correctifs).
- **Maintenant** : détail complet — version, sauvegardes, chantiers ouverts, contrôles, projets dérivés.
- **Ce qui t'attend** : actions et décisions du Project Owner uniquement, dans l'ordre.
- **Prochaines étapes** : détail des deux à quatre étapes suivantes, avec leur chemin (prototype → double arrêt → branche → tests → promotion → push).
- **Plus loin** : titres seulement.
- **Tes idées, et ce qu'elles sont devenues** (bloc obligatoire) : chaque idée exprimée par le Project Owner en conversation — citée dans ses mots, datée — avec son état dans une liste close : `évoquée` (pas encore traitée), `à clarifier`, `à régler`, `cadrée` (fiche), `planifiée` (version cible), `en cours`, `réalisée`, `appliquée` (règle), `intégrée` (absorbée par un chantier), `plus tard`, `écartée` (avec la décision qui l'écarte). Source de chaque ligne : le message d'origine (date), la fiche ou le compte rendu qui le cite. Une idée ne sort de la liste que par `réalisée` ou `écartée`, jamais par oubli.

### 5.4 Forme

Page HTML publiée comme artefact Claude, republiée à la même adresse à chaque régénération (l'historique des versions est conservé par la page). L'IA choisit la forme à la première instance ; elle la garde ensuite stable d'une régénération à l'autre pour que le lecteur retrouve ses repères ; un changement de forme est un réglage (5.5). Bandeau de vérification obligatoire en tête : date et heure, mode de lecture, version, sauvegardes, contrôles, mode de régénération. « L'IA choisira sa présentation » — proposition : libre la première fois, stable ensuite (§ 8, point 1).

**Le tableau suit le style de retour du projet (P11).** `PLAIN` : langage courant, lisible par quelqu'un qui n'est pas informaticien ; aucun identifiant technique (empreinte de commit, nom de commande, code de décision, nom de fichier) dans la lecture principale ; les sources sont nommées simplement (« le dossier du squelette, lu ce soir », « fiche P2 », « ton message du 7 sept. ») ; le détail technique de la vérification vit dans un repli en pied de page (« Pour les techniciens ») et dans la mémoire du tableau. `TECHNICAL` : identifiants, empreintes, verdicts et chemins dans la lecture. Tant que le projet ne porte pas encore `reporting_style` (avant 3.7.0), le style est celui demandé par le Project Owner ; pour Squelette : simple. Décision du Project Owner : « si je choisis une méthode de conversation simple, je veux un tableau identique ».

### 5.5 Réglages de la vue

Enregistrés dans la mémoire du tableau (5.8), modifiés uniquement par une phrase explicite dans la discussion ROADMAP — `RÉGLAGE : <clé> = <valeur>` — et datés :

| Clé | Valeurs | Défaut |
|---|---|---|
| `regeneration` | `off` (manuelle) · `1h` · `4h` · `daily` | `off` |
| `style` | `simple` · `technique` (suit `reporting_style` du projet dès 3.7.0) | celui du projet ; Squelette : `simple` |
| `zoom` | niveaux de 5.3 ; `passe=replie|deploye`, `loin=titres|detail` | `passe=replie`, `loin=titres` |
| `forme` | `stable` · `libre` (nouvelle forme à la prochaine régénération) | `stable` |
| `langue` | `fr` · `en` | `fr` |
| `sources` | liste des dossiers (lecture seule) et fiches | dépôt du projet + `claude/*.md` |

Décision du Project Owner : « L'utilisateur choisira ! ». L'intervalle minimal d'une tâche planifiée est en général d'une heure : `x minutes` se lit `x heures`.

### 5.6 Ce qui est bloqué depuis la discussion ROADMAP

Toute écriture dans un dépôt (fichier, branche, commit, tag, push), toute commande Git modifiante, tout script qui écrit, toute décision de projet (`HD-NNN`, `TPL-D-NNN`), toute création ou modification de Work Item, tout changement d'autorité, de version ou de gouvernance, toute rédaction de mandat. Une demande de ce type reçoit un refus en une phrase et un renvoi vers une autre discussion. La règle `TPL-D-011` (double arrêt) reste entière et n'est jamais déclenchée depuis cette discussion : le tableau affiche, il ne pilote pas. Décision du Project Owner : « si oui on le bloque ».

### 5.7 Régénération automatique

Une tâche planifiée au rythme réglé (≥ 1 h). Pour un projet dont le dépôt vit sur le Mac, la tâche a besoin du Mac allumé et du dossier accordé ; sinon elle régénère quand même le tableau, avec « non vérifié depuis <date> » sur les lignes issues du dépôt. Idempotence : si aucune source n'a changé (HEAD identique, fiches identiques), rien n'est réécrit et la tâche le dit en une ligne. Chaque régénération effective crée une nouvelle version de la même page.

### 5.8 Mémoire du tableau

`claude/roadmap-<projet>.md` dans le projet Claude (ici `claude/roadmap-squelette.md`) : adresse de la page, réglages, dernière vérification (date, HEAD, remotes, contrôles), procédure de régénération, contenu textuel du tableau, journal des régénérations. Une session sans accès au dépôt peut ainsi relire le dernier état connu — marqué comme tel.

### 5.9 Consigne : skill `roadmap-squelette`

La seule action possible : régénérer. Procédure : lire la mémoire du tableau → lire les sources dans l'ordre 5.2 (dépôt en lecture seule si accordé, sinon le noter) → comparer avec le dernier état → reconstruire la page dans la même forme → republier à la même adresse → mettre à jour la mémoire du tableau → répondre en une ligne (« régénéré le … sur … ; N changements » ou « rien n'a changé »). Refus et renvoi pour tout le reste (5.6). Pour un autre agent (Codex), le même texte vaut comme document du projet. La skill `squelette-projet` gagne une phrase de renvoi : « la ROADMAP affiche, elle ne décide rien ».

### 5.10 Lien avec le squelette

P12 est le versant Claude ; P6 est le versant dépôt (`CONTINUITY_GUIDE.md` régénéré par le contrôleur). Ils sont complémentaires : pour un projet dérivé, la source première du tableau est `status --json`, déjà calculée depuis les records, et P6 en serait la forme lisible dans l'arbre. Aucune modification du core n'est requise pour P12.

## 6. Impacts

- `DIRECT` : projet Claude « Squelette » (cette fiche, `claude/roadmap-squelette.md`), une page publiée, une skill à enregistrer par le Project Owner.
- `INDIRECT` : aucun fichier du dépôt ; la skill `squelette-projet` gagne une phrase (5.9).
- `AUTHORITY` : aucune — le tableau cite les autorités, il n'en est pas une.
- `CONCURRENT` : P11 / 3.7.0 en cours ; P12 n'y touche pas et le montre.

## 7. Décisions du Project Owner déjà prises (2026-09-07)

1. Une discussion dédiée par projet, nommée systématiquement (« ROADMAP SQUELETTE »).
2. Toute autre demande est renvoyée vers une autre discussion.
3. La présentation est choisie par l'IA.
4. Régénération automatique au rythme choisi par l'utilisateur.
5. Réglages de la vue permis ; réglages du projet bloqués.
6. Première instance sur le projet Squelette lui-même, depuis le dépôt en lecture seule.
7. Le tableau suit le style de retour : en mode simple, même tableau, lisible par tous, sans jargon (5.4).
8. Les idées évoquées apparaissent dans le tableau, avec leur état (5.3).

## 8. Décisions attendues

1. ~~Sens exact de « on n'est pas obligé d'avoir un dépôt »~~ — clos le 7 sept. : ce n'était pas une idée mais une question sur une phrase de Claude ; retirée par le Project Owner (« n'en tiens pas compte »). La forme reste : libre la première fois, stable ensuite (5.4).
2. ~~Réglage initial de `regeneration` pour Squelette~~ — clos le 7 sept. : « Tu peux aller au bout ! Je valide la suite » → `daily` (tâche planifiée « ROADMAP SQUELETTE — mise à jour quotidienne », 08:00 Europe/Zurich, liée au Mac, lecture seule, republie seulement si changement ; approbation de la carte par le Project Owner ; modifiable par `RÉGLAGE : regeneration = …`).
3. Nom générique pour les autres projets : « ROADMAP <NOM DU PROJET> » ?
4. La phrase de réglage `RÉGLAGE : …` convient-elle ?
5. Enregistrer la skill `roadmap-squelette` (carte proposée le 7 sept.) et la mise à jour de `squelette-projet` (carte proposée le 7 sept. : `reporting_style`, séquence `context-manifest` → lecture → `start --authorities-digest`, `acknowledge-authorities`, renvoi de la ROADMAP) ; généraliser `roadmap-squelette` à tout projet (`roadmap-projet`) ?
6. Cadrer P6 (guide de continuité dans le dépôt) maintenant, ou après 3.7.0 ?

## 9. Critères de fermeture proposés

1. Une page à adresse stable pour Squelette, régénérée au moins une fois depuis une autre discussion sans changement de forme.
2. Chaque ligne porte une source ; une source inaccessible produit « non vérifié depuis … » (essai : dossier non accordé).
3. Une demande hors régénération dans la discussion ROADMAP est refusée et renvoyée (essai).
4. Un réglage changé par `RÉGLAGE : …` est appliqué et enregistré dans la mémoire du tableau.
5. Régénération automatique : une tâche planifiée au rythme choisi, idempotente (rien réécrit sans changement).
6. Aucun fichier du dépôt modifié par P12 : `git status` vierge avant et après chaque régénération.
7. En style simple, la lecture principale ne contient aucun identifiant technique ; le Project Owner le confirme à la relecture.
8. Toute idée exprimée par le Project Owner dans une discussion du projet figure dans le bloc des idées avec un état de la liste close (essai : une idée lancée dans une autre discussion apparaît à la régénération suivante).

## 10. Limites assumées

« Tout message ignoré » n'est pas verrouillable ; la stabilité de la forme dépend de la consigne ; le tableau vaut ce que valent ses sources — une fiche en retard s'y voit comme un écart signalé, pas corrigé ; l'intervalle minimal d'une tâche planifiée ; pour un dépôt local, la régénération automatique dépend du Mac.

## 11. Première instance — ROADMAP SQUELETTE (2026-09-07, 23:15)

- Page : https://claude.ai/code/artifact/6e74eaa9-8e15-492d-b89b-7156bf1588ba (privée tant que non partagée). Trois versions le 7 sept., même adresse : « Première instance » (technique ; S-05 / S-06 constatés par le Project Owner), « Version simple + tes idées » (langage courant, bloc des idées, détails techniques repliés), puis « 3.7.0 promue — 23:35 ».
- S-02 vécu en direct : pendant la construction du tableau, une autre discussion a livré (18bff7b) puis promu (`TPL-D-016`, `main` = `7964fa4` = `v3.7.0` à 23:34) la version 3.7.0. Le tableau construit à 23:15 était déjà périmé à 23:33 ; la relecture du dépôt l'a détecté et corrigé. Conséquence pour la skill : relire les sources à chaque régénération, sans exception, même quelques minutes après la précédente ; ne jamais republier depuis la mémoire du tableau seule.
- Lecture du dépôt (lecture seule, `GIT_OPTIONAL_LOCKS=0`) : `rev-parse`, `for-each-ref`, `tag`, `branch --merged`, `log`, `status --porcelain --ignored` ; `python3 -B scripts/project_control.py bootstrap-audit | audit | status`. `git status --ignored` vierge après. Fiches lues : revue du 5 sept., P1, P2 (V11), P3 (V3), P4, P9, P11.
- Constats utiles à la lecture : `origin` et `nas` alignés sur `0d5d86f` (S-02) ; fiche P11 en retard sur les décisions du soir (S-01) ; 11 branches toutes contenues dans `main`, aucun chantier ouvert dans le dépôt.
- Forme retenue (à garder stable) : bandeau de vérification en langage courant ; quatre chiffres (version, décisions, tests, chantiers ouverts) ; séquence des versions 3.0.0 → 3.6.1 → 3.7.0 ; colonnes « Maintenant » / « Ce qui t'attend » et « Prochaines étapes » / « Plus loin » ; table « Tes idées, et ce qu'elles sont devenues » (quinze idées, du 5 au 7 sept.) ; table des chantiers P1 → P12 avec état et fiche ; arbre du passé replié, avec un repli « Pour les techniciens » en dernier ; règles et réglages en pied.
- Mémoire du tableau : `claude/roadmap-squelette.md`.
- Quatrième version (23:55) : sauvegardes 3.7.0 constatées faites par le Project Owner (`origin/main` = `nas/main` = `7964fa4`) ; mise à jour quotidienne réglée ; fiche P11 passée en V2 (décisions, livraison, promotion) par cette discussion.

---

## 12. V2 — étape 2 : la ROADMAP dans le dossier du projet (fusion avec P6)

Statut : `SCOPE_DEFINITION_V2 — STEP_2_SCOPED — NOT_AUTHORIZED`
Nature : définition de périmètre d'une maintenance du squelette. Aucun code n'est produit, aucun fichier du dépôt n'est touché. L'implémentation exige un mandat explicite, puis le double arrêt (`TPL-D-011`) avant toute écriture dans `Squelette V3 -runtime-proof`, sur branche dédiée, sans promotion.
Baseline examinée : `main` = `7964fa4` (`v3.7.0`), lecture seule le 2026-09-08 vers 00:20 : `roadmap-state.v1.schema.json`, `work-item.v1.schema.json`, `roadmap_errors()` du contrôleur, `status --json`, `provenance/README.md`, `.gitignore`, `mandatory-documents.v1.json`, `AGENTS.core.md`. `git status` vierge avant et après.
Origine : « Je me demande si ce n'est pas préférable que toutes les infos soient dans le dossier physique du projet. Format JSON ? » puis « cadre-le » (Project Owner, 2026-09-08).

### 12.1 Problème

L'étape 1 a mis la ROADMAP au bon endroit pour le lecteur (une page, une adresse) mais au mauvais endroit pour les données : la mémoire du tableau, les fiches P1 → P12 et la liste des idées vivent dans le projet Claude, hors du dossier — non versionnées, non sauvegardées sur GitHub et le NAS, illisibles pour Codex, hors de la preuve de lecture. C'est une source d'état hors de l'arbre, ce que le squelette interdit à ses projets (« pas de document parallèle, pas de nouvelle couche de suivi » — README ; « aucune nouvelle source d'état hors de l'arbre » — P9).

### 12.2 Scénarios d'échec démontrés

**S-07 — Un document hors du dépôt écrasé sans trace (réel, 7 sept.).** La fiche P11 a été modifiée le même soir par deux discussions ; la seconde écriture a recouvert la première sans conflit ni historique — le projet Claude n'a ni versions ni verrou. Dans le dépôt, la même situation produit un conflit Git visible, ou deux commits.

**S-08 — Un état reconstitué, jamais calculé (réel, 7 sept.).** Le tableau a dû être rebâti à partir du journal, des tags, des remotes, de cinq fiches et des notes de séance ; quatre lectures dans la soirée ont donné quatre états, et la livraison de la 3.7.0 par une autre discussion n'a été vue qu'en relisant tout. Un export calculé par le contrôleur (`status --json` existe déjà pour l'état courant) est déterministe ; une reconstitution par un agent ne l'est pas.

**S-09 — Des idées sans domicile (réel).** Les seize idées du Project Owner listées dans la page n'existent nulle part dans le dossier : aucun agent autre que celui qui a produit la page ne peut les lire, les reprendre ni les clore.

**S-10 — Le squelette sans roadmap dans son propre dossier (revue du 5 sept., P1 et P6).** La revue demandait un « REPOSITORY_STATUS renseigné pour le template lui-même » et un guide de reprise généré par le contrôleur. Le suivi du template vit dans le journal (décisions) et dans le projet Claude (chantiers) : pas de vue « où en est-on » dans le dossier, et les fiches de cadrage — qui sont des rapports de maintenance — ne sont pas sous `provenance/maintenance/` comme les rapports de Codex.

### 12.3 Objectif

Tout ce que la ROADMAP montre vient de fichiers du dossier du projet, versionnés et vérifiés par l'audit ; la page est **générée** par le contrôleur à partir de ces fichiers ; la discussion ROADMAP et la page Claude ne sont plus qu'un miroir et un relais. P6 (guide de continuité régénéré par le contrôleur) est réalisé par la même livraison.

### 12.4 Non-objectifs

- Pas de nouvelle couche de suivi pour ce que la roadmap couvre déjà : les chantiers restent des Work Items, avec leur cycle de vie et leurs records.
- Pas d'écriture depuis la discussion ROADMAP : elle reste en lecture seule (5.6 inchangé). Les idées sont enregistrées par la discussion de travail, sous les règles ordinaires.
- Pas de service, pas de dépendance hors bibliothèque standard, pas de page « vivante » : un fichier généré, ouvrable sur le Mac.
- Pas de changement de sémantique des statuts de Work Item ni des niveaux de DONE.

### 12.5 Contrat proposé

#### 12.5.1 Les données, deux formes toujours (JSON pour la machine, Markdown pour l'humain), synchronisées et auditées

Le squelette procède déjà ainsi pour la roadmap (`roadmap-state.v1.json` ↔ `ROADMAP.md`, contrôle `ROADMAP` de l'audit). La même règle s'applique à ce qui manque.

**Projet dérivé (Alpha et suivants).** Sources existantes, réutilisées telles quelles : `docs/governance/roadmap-state.v1.json` + `ROADMAP.md` (chantiers, statuts, gates), records `project_control/work-items/`, `docs/governance/HUMAN_DECISIONS.md` (décisions), `status --json` (état courant : mode, branche, contrôles, version du squelette, style de retour, chantier actif, prochaine action). Ajouts :

- **Idées** : `docs/governance/ideas-state.v1.json` + `docs/governance/IDEAS.md`, schéma `project_control/schemas/ideas-state.v1.schema.json`. Une idée = `{idea_id: "ID-NNN", stated_at, quote (mots du Project Owner), source (discussion, date), state, target (WI-NNN | version | HD-NNN | null), note}`. États (liste close, en anglais dans le record, en français dans la vue) : `EVOKED`, `TO_CLARIFY`, `TO_SET`, `SCOPED`, `PLANNED`, `IN_PROGRESS`, `REALIZED`, `APPLIED`, `INTEGRATED`, `LATER`, `DISCARDED` (avec la décision qui l'écarte). Une idée ne quitte la liste que par `REALIZED` ou `DISCARDED`. Nouveau contrôle d'audit `IDEAS` : Markdown et JSON synchronisés, identifiants uniques, états admis, cible existante (`WI-NNN` présent dans la roadmap, `HD-NNN` présent dans les décisions). Pourquoi pas un Work Item `PROPOSED` : le statut existe, mais chaque entrée de la roadmap exige un record complet (31 champs obligatoires : `authorized_paths`, impacts, gates…) — trop lourd pour une phrase dite en conversation, et cela mélangerait l'idée avec le chantier autorisé. Une idée `PLANNED` ou `IN_PROGRESS` pointe vers son Work Item ; c'est là que la jonction se fait.
- **Réglages et pointeurs de la vue** : `project_control/roadmap-view.v1.json` (schéma `roadmap-view.v1.schema.json`) — `style` (`FOLLOW_REPORTING_STYLE` par défaut), `zoom` (`past`, `far`), `language`, `regeneration` (`off` | `1h` | `4h` | `daily`, intention déclarée ; l'automatisation reste côté Claude), `mirrors` (`[{provider: "claude", url}]`), `last_generated` (`{at, head, sources_digest}`). Aucune donnée de projet n'y vit : seulement la vue.

**Le squelette lui-même.** Son dossier ne doit pas porter une roadmap de projet (`docs/governance/ROADMAP.md` reste vide dans le template : une copie neuve ne précharge aucun chantier). Sa propre roadmap va là où vit déjà son histoire, `provenance/`, qui « décrit le template, jamais le projet dérivé » : `provenance/roadmap-template.v1.json` + `provenance/ROADMAP_TEMPLATE.md` — chantiers P1 → P12 `{id, title, state, versions: [], decisions: [TPL-D-NNN], scope: chemin de la fiche}`, décisions attendues, prochaines étapes, idées du Project Owner sur le template (même modèle que `ideas-state`) — et `provenance/roadmap-view.v1.json`. Les fiches de cadrage et de revue rejoignent `provenance/maintenance/scopes/` (P1 → P12, revue du 5 sept., contre-revue, mandat WI-061), comme les rapports de Codex l'ont fait en `v3.1.0` (R4). Un projet dérivé emporte ces fichiers comme trace de l'ascendance de son template, sans en faire un record de projet (règle déjà écrite dans `provenance/README.md`).

#### 12.5.2 La vue, générée par le contrôleur

Nouvelle commande, lecture seule : `roadmap-view [--json] [--html <chemin>] [--markdown <chemin>]`. Elle lit les sources ci-dessus (ou, dans le template, `provenance/roadmap-template.v1.json`), applique le style (`reporting_style` du projet ; `PLAIN` = langage courant, aucun identifiant technique hors du repli « Pour les techniciens » ; `TECHNICAL` = identifiants, empreintes, verdicts), le zoom (passé replié, présent et prochaines étapes détaillés, plus loin en titres, « Ce qui t'attend » = décisions humaines en attente), et produit : la charge `--json` (ce que le miroir Claude consomme), la page HTML autonome (`reports/roadmap/ROADMAP.html` par défaut dans un projet ; `provenance/roadmap/ROADMAP.html` dans le template) et la vue Markdown (`docs/governance/ROADMAP_VIEW.md` ; `provenance/ROADMAP_VIEW.md`). Chaque ligne cite sa source (fichier). Bandeau de vérification : date, HEAD, résultat de l'audit, version du squelette, état des remotes s'ils sont lisibles, `sources_digest` (SHA-256 des fichiers sources triés) — si le digest n'a pas changé, rien n'est réécrit (idempotence). `status` gagne une ligne « Vue roadmap : à jour | périmée | absente » par comparaison du digest.

C'est P6 tel que la revue le décrivait (« état courant, prochaine gate, ce qui est autorisé, ce qui est interdit, HEAD de référence »), sous une forme lisible par tous.

#### 12.5.3 Enregistrer une idée

Commande `idea add --quote "<mots du Project Owner>" --source "<discussion, date>" [--state EVOKED]` et `idea set ID-NNN --state <état> [--target <WI|version|HD>] [--note …]` : écrivent les deux formes (JSON, Markdown) et committent sur la branche canonique comme les autres transitions (`chore(project-control): idea ID-NNN`, P9-A). Enregistrer une idée n'est pas une décision : cela n'autorise rien ; l'autorisation reste un `HD-NNN` et un Work Item. Depuis la discussion ROADMAP : jamais (5.6) ; depuis une discussion de travail : couvert par l'autorisation ordinaire (`TPL-D-001`). Un agent qui entend une idée du Project Owner l'enregistre dans la session même, sans attendre.

#### 12.5.4 La consigne, dans le dossier

`docs/agent-governance/ROADMAP_VIEW.md` (fichier core, routé pour le scope `governance`) : la doctrine de la discussion ROADMAP — affiche, ne décide rien ; tout message = régénération ; `RÉGLAGE :` ; renvoi de tout le reste ; lecture par `roadmap-view --json`, jamais reconstitution. Une section courte dans `AGENTS.core.md` (« Vue ROADMAP ») la résume. La skill Claude `roadmap-squelette` devient un relais de ce document et lit `roadmap-view --json` au lieu du journal et des fiches ; Codex lit le document.

#### 12.5.5 Fichiers générés et Git

Les fichiers de données (JSON, Markdown) sont committés — ce sont les informations. Le HTML est régénérable en une commande : proposition, l'ignorer (`reports/roadmap/*.html`, sur le modèle de `reports/*.json` déjà ignoré) ; alternative, le committer à chaque changement de digest. Décision attendue.

#### 12.5.6 Ce qui reste côté Claude

Le miroir (page publiée) et la tâche quotidienne : elle exécute `roadmap-view --json` en lecture seule sur le Mac et republie la page si le digest a changé ; sans accès au Mac, « non vérifié depuis <date> ». Le projet Claude ne garde que des pointeurs (`claude/README.md` : où vivent les fichiers, adresse de la page) et la skill. Les fiches P1 → P12 y sont retirées une fois copiées dans le dépôt et vérifiées (SHA-256), pour qu'il n'y ait plus qu'une source.

#### 12.5.7 Migration (même livraison)

1. Copier les fiches (P1, P2, P3, P4, P9, P11, P12, revue du 5 sept., contre-revue Codex, mandat WI-061) dans `provenance/maintenance/scopes/`, telles quelles, avec leurs révisions.
2. Créer `provenance/roadmap-template.v1.json` et `ROADMAP_TEMPLATE.md` à partir de l'état textuel de `claude/roadmap-squelette.md` (chantiers P1 → P12, décisions TPL-D-001 → 016, idées 1 → 17), vérifiés contre le journal et les tags.
3. Générer la première `provenance/roadmap/ROADMAP.html` et la comparer à la page publiée (même contenu, même forme).
4. Réduire le projet Claude aux pointeurs ; republier la page depuis `roadmap-view --json`.

### 12.6 Impacts

- `DIRECT` (core, manifeste à régénérer) : `scripts/project_control.py` (`roadmap-view`, `idea`, contrôle `IDEAS`, ligne de `status`), `project_control/schemas/ideas-state.v1.schema.json`, `project_control/schemas/roadmap-view.v1.schema.json`, `docs/agent-governance/ROADMAP_VIEW.md`, `docs/agent-governance/AGENTS.core.md` (section), `FIRST_START.md` (une phrase : la vue se génère), `project_control/README.md`, `CLAUDE.md`, `tests/test_template.py` (+ fixtures), `.gitignore`. Hors core : `docs/governance/IDEAS.md` + `ideas-state.v1.json` vierges, `project_control/roadmap-view.v1.json` (défauts), `provenance/` (roadmap du template, vue, `maintenance/scopes/`), `provenance/CHANGELOG.md`.
- `INDIRECT` : un projet dérivé reçoit le core par `template-upgrade` ; les fichiers hors core (`IDEAS.md`, `ideas-state`, `roadmap-view`) sont ajoutés par le Work Item de mise à niveau, sous décision humaine — comme `legacy_baseline` et `reporting_style`. `mandatory-documents.v1.json` est un fichier projet : le routage de `ROADMAP_VIEW.md` et `IDEAS.md` s'y ajoute dans le même Work Item (c'est le cas O-09 : documents hors core porteurs de doctrine — à traiter ensemble).
- `AUTHORITY` : `IDEAS.md` n'est pas une autorité (une idée ne décide rien) ; routé en lecture pour le scope `governance`, pas en base. `ROADMAP_VIEW.md` est une doctrine d'agent (comme `AGENTS.core.md`). Décision humaine du template requise (`TPL-D-0NN`).
- `CONCURRENT` : Alpha reporté par le Project Owner (montée en une fois vers la version stabilisée : cette version en fera partie) ; O-09 lié ; P4 / P5 inchangés.

### 12.7 Décisions attendues du Project Owner

1. **Idées** : fichier d'idées léger (`ideas-state` + `IDEAS.md`, recommandé) ou Work Items `PROPOSED` (record complet obligatoire, lourd) ?
2. **HTML généré** : ignoré par Git (recommandé, régénérable en une commande) ou committé à chaque changement ?
3. **Roadmap du squelette lui-même** dans `provenance/` (recommandé), ou ailleurs ?
4. **Migration des fiches** P1 → P12 dans `provenance/maintenance/scopes/` : dans la même version (recommandé) ou plus tard ?
5. **Commande** : `roadmap-view` nouvelle (recommandé) ou extension de `status` ?
6. **Miroir Claude** : garder la page publiée et la tâche quotidienne comme miroir (recommandé) ou page locale seulement ?
7. **Version** : livrer comme `3.8.0` (nouvelle commande, nouveaux schémas, nouveau document core) — proposé.

### 12.8 Critères de fermeture proposés

1. Copie neuve : `roadmap-view --html` produit une page valide sans chantier ni idée ; `bootstrap-audit` PASS ; aucun chantier du template n'apparaît dans la vue d'un projet dérivé (test).
2. Projet avec chantiers, décisions et idées : la page et la vue Markdown reflètent `roadmap-state`, `HUMAN_DECISIONS`, `ideas-state`, `status` ; une désynchronisation `IDEAS.md` / JSON est refusée nominativement par l'audit (test).
3. `PLAIN` : aucun identifiant technique hors du repli « Pour les techniciens » (test sur le HTML généré) ; `TECHNICAL` : identifiants présents (test).
4. Idempotence : deux appels sans changement de sources ne réécrivent rien ; `status` dit « à jour » ; après un `close`, « périmée » jusqu'à régénération (test).
5. `idea add` / `idea set` : deux formes écrites et committées, états hors liste refusés, cible inexistante refusée (test).
6. Squelette : `provenance/roadmap-template.v1.json` + `ROADMAP_TEMPLATE.md` + page générée présents ; fiches dans `provenance/maintenance/scopes/` avec leurs SHA-256 dans le rapport de maintenance ; projet Claude réduit aux pointeurs ; page miroir republiée depuis `roadmap-view --json` (vérification manuelle du Project Owner : même contenu que la page du 8 sept.).
7. 94 + nouveaux tests verts ; bibliothèque standard seule ; manifeste régénéré ; `audit` et `bootstrap-audit` PASS sur `main`.

### 12.9 Limites assumées

- La page Claude reste un miroir hébergé hors du dossier ; l'original est le fichier généré dans le dossier.
- Une idée dite dans une conversation n'entre dans le dossier que si un agent l'enregistre : la règle 12.5.3 le lui impose, le contrôleur ne peut pas l'entendre à sa place.
- La tâche quotidienne dépend du Mac allumé et du dossier accordé ; sinon elle marque « non vérifié ».
- Cette maintenance touche le core : elle attend son tour derrière la stabilisation décidée par le Project Owner (« on va attendre car le squelette se développe ») et se livre après double arrêt, sur branche dédiée, sans promotion.

### 12.10 Suite

Sur mandat du Project Owner : réponses aux sept décisions → prototype hors dossier (clone de travail en espace de session, comme pour 3.6.1 et 3.7.0), vérifié sur une copie neuve et sur un clone jetable de la copie d'Alpha → STOP 1 / STOP 2 → livraison sur branche `claude/v3.8-roadmap-in-repo` (nom proposé) → promotion sur décision → push par lui → migration du projet Claude (12.5.7) → mise à jour des skills `roadmap-squelette` et `squelette-projet`.

## 13. Étape 2 — livraison 3.8.0 (2026-09-08)

Mandat : « je suis ok. avec la suite. On va de l'avant […] Va de l'avant ! » (2026-09-08), les sept décisions de § 12.7 retenues telles que recommandées (`TPL-D-017`, `provenance/CHANGELOG.md`). Idée notée le même jour : « Tu peux noter que quand squelette est terminé, on va faire un challenge à Codex ! » (ID-017, planifiée) ; ordre décidé : 3.8.0 → challenge Codex → correctifs éventuels → mise à niveau d'Alpha en dernier (« On terminera par la mise à jour Alpha ! », ID-018).

### 13.1 Comment la version d'essai a été préparée

Hors du dossier, comme pour 3.6.1 et 3.7.0 : copie de travail en espace de session (`sq-proto8`), initialisée depuis les 82 fichiers suivis de `main` = `7964fa4` (`v3.7.0`) — arbre vérifié identique octet pour octet (même empreinte de `git ls-tree -r`, 82 entrées) —, taguée `v3.7.0`. Le dépôt `Squelette V3 -runtime-proof` n'a été lu qu'en lecture seule (`GIT_OPTIONAL_LOCKS=0`, `git status` vierge avant et après chaque lecture ; le 8 sept. à la fin de la préparation : `main` = `7964fa4`, `origin/main` = `nas/main` = `7964fa4`, tag `v3.7.0` sur HEAD, arbre propre).

### 13.2 Ce qui est livré

Le détail est dans l'entrée `claude/v3.8-roadmap-in-repo` de `provenance/CHANGELOG.md`. En résumé : commandes `idea add` / `idea set` et contrôle `IDEAS` (12.5.1, 12.5.3) ; commande `roadmap-view` et rendu `scripts/roadmap_view.py`, page HTML ignorée par Git et vue Markdown committée, ligne « Vue roadmap » de `status`, contrôle `ROADMAP_VIEW` (12.5.2, 12.5.5) ; réglages `roadmap-view.v1.json` ; doctrine `docs/agent-governance/ROADMAP_VIEW.md` (core, routée pour `governance`) et section d'`AGENTS.core.md` (12.5.4) ; roadmap du squelette `provenance/roadmap-template.v1.json` + `provenance/roadmap-view.v1.json`, vue `provenance/ROADMAP_VIEW.md` + `provenance/roadmap/ROADMAP.html`, fiches rapatriées dans `provenance/maintenance/scopes/` (12.5.1, 12.5.7 étapes 1 à 3) ; manifeste `3.8.0` (24 fichiers core).

### 13.3 Écarts par rapport à § 12, assumés

1. Pas de `provenance/ROADMAP_TEMPLATE.md` rédigé à la main : la vue Markdown générée (`provenance/ROADMAP_VIEW.md`) est la forme humaine — un document de plus à tenir aurait contredit `OMIT > ACTIVATE WITHOUT NEED`.
2. Pas de champ `last_generated` dans `roadmap-view.v1.json` : la première ligne de la vue Markdown porte `sources_digest`, `generated_at` et `head` ; le fichier de réglages ne change qu'à un réglage.
3. `IDEAS.md` n'est pas routé comme autorité (§ 12.6 le prévoyait pour `governance`) : une idée ne décide rien, et chaque `idea add` aurait périmé la preuve de lecture des chantiers en cours. `ROADMAP_VIEW.md` (doctrine) est routé, lui.
4. Rythme écrit `OFF | HOURLY | EVERY_4_HOURS | DAILY` plutôt que `off | 1h | 4h | daily` ; libellés en français dans la vue.
5. La vue Markdown d'un projet initialisé est committée par le contrôleur lui-même (`chore(project-control): roadmap view`), seulement quand ses sources ont changé, depuis la canonique sur un worktree propre — la règle P9-A appliquée à la vue ; sans cela, chaque régénération aurait laissé un fichier modifié qui bloque `start`, `close` et `idea`. `--style` ne touche que la page ; un chemin explicite (`--markdown`) est une simple écriture non committée.
6. La version « actuelle » du squelette est la plus haute taguée dans le dépôt, jamais la valeur du fichier ; une version listée dans le fichier sans tag est affichée comme « la suivante » — ainsi la promotion (tag) suffit, sans réécrire le fichier.
7. `roadmap-view --write` (raccourci vers les chemins par défaut) s'ajoute à `--html` / `--markdown`.

### 13.4 Vérifications sur la version d'essai

- Suite complète : 97 tests (94 + 3 nouveaux), OK ; les trois nouveaux couvrent § 12.8 points 1 à 5 (copie neuve, idées, projet initialisé, `PLAIN` / `TECHNICAL`, idempotence, désynchronisation refusée, aucun chantier du template dans la vue d'un projet).
- `core-manifest` : `CORE_ALIGNED`, `3.8.0`, 24 fichiers core ; `template-upgrade --source <squelette>` depuis un projet initialisé de test : `identical 24`, rien à écrire.
- `bootstrap-audit` sur la copie de travail, avant commit : refus attendu `BOOTSTRAP_CHANGE_SCOPE` (chemins core), identique à toutes les maintenances précédentes ; `audit` PASS avec les contrôles `IDEAS` et `ROADMAP_VIEW` une fois les fichiers committés.
- Page générée regardée une fois (capture) : forme stable, sections dans l'ordre, étiquettes de la frise sans collision ; la vue Markdown lue en entier.
- Non fait ici : la répétition sur un clone jetable d'Alpha (§ 12.10) — Alpha n'est pas accessible à cette session ; elle aura lieu lors de sa mise à niveau, en dernier, après le double arrêt. Non fait non plus, et pour après la promotion : la migration côté Claude (§ 12.5.7 étape 4) et la mise à jour des deux consignes.

### 13.5 Livraison dans le dépôt (après double arrêt)

Dossier cible : `~/Projets/Squelette V3 -runtime-proof`. Actions prévues, toutes réversibles tant que rien n'est promu : branche `claude/v3.8-roadmap-in-repo` depuis `main` (`7964fa4`) ; application du patch de la version d'essai ; commit des chemins explicites avec `PROJECT_CONTROL_HOOK_OVERRIDE` (hook actif, chemins core), auteur Jeoffrey, trailers Claude ; puis `roadmap-view --write` exécuté dans le dépôt et second commit `chore(provenance): roadmap view` pour que la vue committée décrive le dépôt réel (tags, remotes, audit PASS) et non la copie de travail. Interdits : toute écriture sur `main`, tout tag, tout push, toute suppression hors verrous Git temporaires. Promotion (« promouvoir » → fast-forward de `main`, tag `v3.8.0`) et push : gestes du Project Owner, décision séparée (`TPL-D-018` à venir).

### 13.6 Livraison effectuée dans le dépôt (2026-09-08, 06:36 → 07:10 Europe/Zurich)

Double arrêt : « je suis d'accord pour que tu écrives dans ce dossier » (confirmation 1) puis « Confirmé : branche claude/v3.8-roadmap-in-repo dans ~/Projets/Squelette V3 -runtime-proof, main intouché, pas de push. » (confirmation 2). Droit de suppression accordé pour les seuls fichiers temporaires de Git.

Déroulé, dans `~/Projets/Squelette V3 -runtime-proof` : état vérifié avant (main = `7964fa4` = `v3.7.0`, propre, `origin/main` = `nas/main` = `7964fa4`) ; branche `claude/v3.8-roadmap-in-repo` créée depuis `main` ; 34 fichiers déposés et vérifiés octet pour octet (SHA-256 identiques à la version d'essai) ; bit d'exécution de `scripts/project_control.py` rétabli (perdu à la copie) ; `core-manifest` `CORE_ALIGNED` ; `bootstrap-audit` refusant `BOOTSTRAP_CHANGE_SCOPE` avant commit, comme attendu.

Trois commits (auteur Jeoffrey, mention de Claude et référence de session), le garde-fou de commit passé avec un mandat explicite imprimé dans son rapport pour les deux premiers :

1. `b97703a` — `feat(3.8.0): la ROADMAP dans le dossier — idées, réglages, vue générée, fiches (P12 étape 2, P6)` — les 34 fichiers.
2. `d5c3e5b` — `fix(3.8.0): la vue juge les sauvegardes sur la branche principale et date en UTC` — constaté en générant la vue dans le vrai dépôt : la comparaison aux remotes se faisait sur la branche courante (jamais poussée avant promotion) et l'heure de vérification se lisait comme une heure locale ; `scripts/project_control.py`, `scripts/roadmap_view.py`, manifeste régénéré (3.8.0, 24 fichiers core).
3. `2487619` — `chore(provenance): roadmap view (3.8.0, avant promotion)` — `provenance/ROADMAP_VIEW.md` généré par `roadmap-view --write` dans le dépôt (sources_digest `2856aca9…`, audit PASS, « Sauvegardes : identiques (v3.7.0) », « Branches de travail non intégrées : claude/v3.8-roadmap-in-repo »).

Fichiers temporaires de Git effacés : 34 `tmp_obj_*` sous `.git/objects/` (laissés par `git add` faute de droit de suppression au moment de l'indexation) ; aucun verrou ; `git fsck` propre.

Vérifications après livraison, sur la branche : `bootstrap-audit` PASS (23 contrôles), `audit` PASS, `status` : « Squelette : 3.8.0 | core aligné », « Vue roadmap : à jour », hook actif ; `check_git_traceability` PASS ; `git diff --check` propre ; suite complète **97 tests OK** (Python 3.10 du poste, en quatre lots : 23 + 25 + 27 + 22) ; arbre propre (seule la page HTML générée, ignorée par Git, est présente). `main` inchangé à `7964fa4`, tags et remotes inchangés, aucun push.

Reste : la promotion (« promouvoir » → fast-forward de `main`, entrée `TPL-D-018` dans le journal, tag `v3.8.0`) et le push par le Project Owner ; puis la migration côté Claude (§ 12.5.7 étape 4) et la mise à jour des deux consignes.

### 13.7 Promotion (2026-09-08, 07:30 Europe/Zurich)

Décision « promouvoir » du Project Owner. Dans le même dossier, sans envoi : `main` avancée par fast-forward sur `claude/v3.8-roadmap-in-repo` (`2487619`) ; décision `TPL-D-018` enregistrée dans `provenance/CHANGELOG.md` ; `provenance/roadmap-template.v1.json` mis à jour (3.8.0 promue, P6 fait, idée ID-016 réalisée, attente : envoi sur GitHub et le NAS) ; cette fiche complétée (§ 13.6 et § 13.7) ; commit `docs(provenance): enregistrer la décision du Project Owner TPL-D-018` ; tag annoté `v3.8.0` sur ce commit ; puis vue régénérée (`roadmap-view --write`) et committée à part — `main` est donc un commit devant `v3.8.0`, sans changement du core (le manifeste `3.8.0` reste identique au tag). Les SHA exacts sont dans le journal Git et dans la vue.

À peaufiner plus tard (pas dans cette version, pour ne pas toucher le core après le tag) : quand `main` n'est devant le tag que par la vue régénérée, la vue dit « le commit courant n'est pas tagué » — exact, mais une formulation plus douce (« sur la 3.8.0, plus la vue régénérée ») serait plus juste pour un lecteur non technicien. Bon candidat pour le challenge Codex ou une 3.8.x.

Reste, côté Claude (§ 12.5.7 étape 4) : page publiée republiée depuis `roadmap-view --json`, fiches du projet Claude réduites à des pointeurs, consignes `roadmap-squelette` et `squelette-projet` mises à jour. Puis, dans l'ordre décidé : challenge Codex, correctifs éventuels, mise à niveau d'Alpha en dernier.

Envoi fait par le Project Owner le 8 sept. au soir (`git push origin main v3.8.0 && git push nas main v3.8.0`) : `origin/main` = `nas/main` = `main` = `4c93ddf`, tag `v3.8.0` sur les deux ; vérifié en lecture seule. La ligne « Envoyer la 3.8.0 sur GitHub et le NAS » est retirée du fichier de roadmap. À peaufiner aussi (même lot que ci-dessus) : cette attente devrait être produite par le contrôleur lui-même quand les sauvegardes sont en retard, plutôt qu'écrite à la main dans le fichier de roadmap — il sait déjà le constater.
