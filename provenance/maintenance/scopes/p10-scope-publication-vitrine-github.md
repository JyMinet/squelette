> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# P10 — Publication, étape 1 : la vitrine GitHub (README, exemple, licence, contribution, release)

Statut : `SCOPE_DEFINITION_V3 — STEP_1_PROMOTED (v3.9.0, TPL-D-020) — PUSH_RELEASE_ABOUT_PENDING (gestes du Project Owner)`
Révision : V3 (2026-09-08, matin, Europe/Zurich) — § 14 : livraison dans le dépôt après double arrêt. V2 (§ 13) : constat sur pièces, décisions prises, version d'essai, plan, observations. La V1 (§ 1 à 12) est conservée telle quelle, sauf le statut des décisions en § 8.
Nature : définition de périmètre côté Claude (projet Claude « Squelette »). Aucun fichier du dépôt n'est touché. L'implémentation exige un mandat explicite, puis le double arrêt (`TPL-D-011`) avant toute écriture dans `Squelette V3 -runtime-proof`, sur branche dédiée, sans promotion.
Dépôt non relu pour la V1 (demande d'accès restée sans réponse à 01:19) ; **relu en lecture seule pour la V2** (accès accordé à 01:27) : constat en § 13.1. Les mentions « à vérifier » de la V1 sont tranchées en § 13.1.
Baseline examinée en V2 : `main` = `7964fa4` (`v3.7.0`) = `origin/main` = `nas/main` ; checkout sur la branche `claude/v3.8-roadmap-in-repo` (3 commits au-dessus de `main` : `b97703a`, `d5c3e5b`, `2487619` — la 3.8.0 livrée par l'autre discussion, non promue, aucun tag `v3.8.0`) ; arbre propre (`git status --porcelain` vide ; `provenance/roadmap/` présent et ignoré, attendu depuis la 3.8.0).
Origine : « Améliore le github avec ces remarques de gpt : […] Qu'en penses tu ? » (Project Owner, 2026-09-08, 01:18). Remarques reproduites intégralement en § 11.
Filiation : revue du 5 sept. (§ D : le projet Claude porte l'état du template ; P8 : points mineurs) ; décision du 7 sept. « publication publique seulement après un second projet réel » ; idée « README en anglais » (7 sept., réalisée : README bilingue en 3.3.0) ; idée « challenge Codex quand le squelette est terminé » (8 sept., ID-017, planifiée) ; ordre « on terminera par la mise à jour Alpha » (8 sept., ID-018).
Numérotation : P10 = publication (note du 7 sept.). Étape 1 = présentation (cette fiche : la vitrine, dépôt encore privé). Étape 2 = publication proprement dite (dépôt public, release, annonce) — plus tard, sur décision séparée.

## 1. Problème

Le README parle à qui connaît déjà le projet. D'après GPT, son titre actuel est « Squelette V3 — garder le cap du projet » (à vérifier) et il commence par le mécanisme, pas par le problème. Un visiteur qui arrive de l'extérieur range le dépôt dans la case « encore un template `AGENTS.md` / prompt framework », alors que ce qui le distingue — règles exécutables et fail-closed (le contrôleur refuse, il ne conseille pas), Work Items autorisés, décisions humaines enregistrées, preflight, provenance Git, Definition of Done à sept niveaux, et depuis l'été : preuve de lecture des autorités (3.6), double arrêt (3.5), style de retour choisi par l'utilisateur (3.7), mise à niveau du core (3.4), hook Git (3.2), vue roadmap (3.8) — n'apparaît pas au premier écran. La revue du 5 sept. faisait déjà ce constat de fond : « très au-dessus des frameworks publics de spec-driven development […] qui restent au niveau de la convention de prompt » ; la présentation ne le montre pas.

## 2. Scénarios d'échec

**S-01 — Le visiteur classe le projet dans « un fichier d'instructions de plus » (risque, décrit par GPT ; plausible au vu du titre cité).** Conséquence : pas d'essai, pas de retour, pas de second projet réel venu d'ailleurs.

**S-02 — Un extrait de sortie inventé dans le README (risque de conception, contenu dans la proposition de GPT elle-même : « même si cet exemple doit être adapté à la sortie réelle de ton outil »).** Dans un projet dont la thèse est « une preuve, pas une déclaration », un extrait inventé contredit la thèse dès le premier écran ; et un extrait réel copié à la main périme à chaque version (la ligne « Retour au Project Owner » n'existe que depuis 3.7.0, la ligne « Vue roadmap » que depuis 3.8.0). Le README doit montrer une sortie produite par une exécution réelle et vérifiée mécaniquement.

**S-03 — Un projet exemple figé dans le dépôt (risque de conception, issu de la proposition `examples/hello-squelette/` telle que formulée).** Un projet gouverné vit avec ses records committés par le contrôleur sur sa branche canonique (P9-A) : un dépôt Git imbriqué ne se committe pas dans le dépôt parent ; une copie du core dans l'arbre du template crée un second exemplaire de `project_control.py` à côté du vrai (effet sur `core-manifest` / `template-upgrade` à vérifier) ; et l'exemple vieillit à chaque version. Il faut un exemple qui se régénère.

**S-04 — Annonce avant maturité (risque, écarté par décision).** Le Project Owner a décidé le 7 sept. que la publication publique attend un second projet réel ; GPT lui-même recommande de ne pas lancer de communication avant cinq prérequis. La vitrine se prépare dépôt privé ; l'ouverture est une décision séparée (étape 2).

**S-05 — Deux README qui divergent (risque, si l'on choisit deux fichiers EN/FR).** Le squelette interdit à ses projets les documents parallèles ; deux README complets sont deux sources pour le même premier écran. Si deux langues, un seul fichier, et la partie traduite limitée au premier écran.

**S-06 — Le README contredit la doctrine (risque, O-09).** Le README n'est pas une autorité mais il porte de la doctrine ; une phrase de vitrine (« l'agent ne peut pas… ») qui promet plus que `AGENTS.core.md` et le contrôleur ne garantissent devient une fausse affirmation publique. Chaque affirmation du premier écran doit pointer vers le mécanisme qui la tient (contrôle d'audit, commande, test).

## 3. Objectif

Qu'un visiteur comprenne en dix secondes le problème et la différence, en deux minutes le cycle complet sur un exemple réel qu'il peut rejouer, et qu'il sache comment essayer avec son propre agent — sans une seule affirmation non tenue par un mécanisme, sans une seule sortie de commande qui ne soit produite et vérifiée.

## 4. Non-objectifs

- Pas de publication (dépôt public, release visible du public, annonce Hacker News / Reddit / LinkedIn) : étape 2, décision séparée du Project Owner.
- Pas de changement de doctrine ni de core « pour faire joli » (GPT : « il ne faut pas chercher à faire plus joli : il faut faire comprendre plus vite »).
- Pas de traduction complète de la documentation technique en anglais : seul le premier écran est bilingue à l'étape 1.
- Aucun geste GitHub par un agent : push, release, About, Topics restent les gestes du Project Owner (`TPL-D-004`).

## 5. Contrat proposé

### 5.1 README — premier écran, dans cet ordre

1. **Titre et sous-titre (anglais)** : « Squelette » ; « Governance and control for AI-assisted projects » ; une phrase : garder explicites le but, le périmètre, l'autorité humaine et la preuve d'achèvement, même quand plusieurs agents se relaient pendant des mois. Signature : « Who decides. Who does. What proves it's done. » (reprise de la formule actuelle du README, que GPT propose de conserver).
2. **Schéma** (texte, tel que proposé par GPT, complété) : Humain → Squelette (Charter, Work Items autorisés, décisions humaines, preflight, preuve de lecture, provenance Git, Definition of Done, vue roadmap) → agents (ChatGPT · Claude · Codex · Gemini · autres) → travail + preuves.
3. **Why Squelette?** — trois phrases : les projets longs pilotés par des IA dérivent ; un agent oublie une contrainte, réinterprète une décision, écrit hors périmètre ou déclare fini sans preuve ; Squelette ajoute une couche de contrôle de projet entre l'humain et les agents, et **le contrôleur refuse** (fail-closed) au lieu de recommander.
4. **Tableau « Without / With Squelette »** (GPT), avec trois lignes ajoutées : « l'agent dit avoir lu les règles » → « preuve de lecture exigée (empreinte) » ; « l'agent choisit comment il te parle » → « style de retour choisi par l'utilisateur » ; « un agent touche un autre dossier » → « double arrêt, refus mécanique ».
5. **Démo** : la sortie **réelle** de `status` (et d'un refus de preflight, si la place le permet) produite par l'exemple 5.2, entre marqueurs `<!-- hello-squelette:begin -->` / `<!-- hello-squelette:end -->`, régénérée par la démo et vérifiée par un test.
6. **Try it** : trois commandes (cloner, rejouer la démo, créer son projet selon `ADOPTION.md` / `FIRST_START.md` — à aligner sur la procédure réelle, à vérifier) et la phrase de GPT : « Clone it. Give FIRST_START.md to Claude / Codex / ChatGPT. See how the agent behaves. »
7. **What it is / what it is not** : pas un prompt framework ; un contrôleur en Python standard, sans dépendance, agnostique du fournisseur ; les règles sont des contrôles, pas des recommandations.
8. **En français** : le même premier écran, condensé (titre, pourquoi, tableau, démo, essai), pour tenir la décision « README bilingue ».
9. **Ensuite** : la documentation existante, inchangée sauf relecture de cohérence (numéros de version, commandes).

Vocabulaire : « Squelette » reste le nom ; le descriptif devient « a lightweight governance framework for projects built with AI agents » (GPT), jamais « skeleton » comme catégorie.

### 5.2 Exemple `examples/hello-squelette/` — une démo rejouable, pas un dossier figé

Un script (`python3 -B examples/hello-squelette/demo.py`, bibliothèque standard seule) qui, dans un dossier temporaire : exporte l'arbre suivi du squelette courant (sans `.git`), initialise une baseline Git autonome, joue un Project Owner scripté (réponses fixes à l'interview de `FIRST_START.md`, dont le style de retour), enregistre **une** décision humaine, crée et autorise **un** Work Item avec ses `authorized_paths`, fait **une** petite modification dans le périmètre, montre **un** refus (écriture hors périmètre, refusée par le preflight), passe les tests, clôt le Work Item avec ses preuves, affiche `status` — puis écrit `examples/hello-squelette/TRANSCRIPT.md` (sortie réelle, champs volatils normalisés : dates, empreintes, chemins) et met à jour le bloc du README entre marqueurs (`--update-readme`). Le dépôt du squelette reste intact (`git status` vierge après la démo).

Un test de la suite du template rejoue la démo et compare : `TRANSCRIPT.md` et le bloc du README doivent être identiques à la sortie régénérée, sinon le test est rouge. **Le README ne peut plus mentir.** `REUSE` : les fixtures de tests construisent déjà des projets initialisés en dossier temporaire (P12 § 12.8, points 1 à 5) ; la démo s'appuie dessus au lieu de réinventer.

Emplacement : `examples/` (attendu par un visiteur GitHub). Conséquence à régler : un projet dérivé exporte l'arbre suivi et emporterait `examples/` ; soit `ADOPTION.md` dit qu'un projet dérivé peut retirer `examples/`, soit l'export l'exclut — à vérifier sur la procédure réelle d'export (§ 8, décision 3).

### 5.3 `CONTRIBUTING.md` — très court

Comment proposer (issue ou discussion, en anglais ou en français) ; le core est gouverné : une amélioration passe par le template, jamais par un projet dérivé, et respecte `OMIT > ACTIVATE WITHOUT NEED` ; tests obligatoires (`python3 -B -m unittest discover -s tests`), bibliothèque standard seule ; commits et tags en français (règle du Project Owner), README bilingue ; interdits Git repris d'`AGENTS.core.md` ; le Project Owner tranche. Une ligne pour les agents : « If you are an AI agent, read `AGENTS.md` first. »

### 5.4 `LICENSE`

À vérifier dans le dépôt. Si absente : le choix de la licence est une décision du Project Owner (Claude n'est pas juriste). Éléments factuels : MIT — courte, très permissive, exige seulement de conserver la notice ; Apache-2.0 — permissive, avec clause sur les brevets et fichier `NOTICE` ; licences copyleft (GPL, AGPL) — obligent les dérivés à rester sous la même licence. Point propre au squelette : un projet dérivé emporte le core (`scripts/project_control.py`, schémas, tests) — la notice de licence du template doit donc voyager avec le core (dans `provenance/` ou en tête des fichiers), sinon les dérivés perdent la notice. À trancher en V2 après lecture du dépôt.

### 5.5 Release GitHub

Les tags existent (`v3.0.0` → `v3.7.0`, à vérifier) ; une « release » GitHub est une page attachée à un tag, avec des notes. Proposition : première release sur la version qui porte la vitrine (la page de release montre alors le README refait), notes préparées par Claude à partir de `provenance/CHANGELOG.md` (décisions `TPL-D-NNN` et entrées de maintenance), création par le Project Owner sur GitHub. GPT propose « probablement v3.0.0 » : non — v3.0.0 est une version passée ; la release porte la version courante, les tags antérieurs restent l'historique.

### 5.6 About et Topics (gestes du Project Owner sur GitHub)

About — deux candidats, au choix : « Governance framework for AI-assisted projects: human authority, controlled scope, persistent decisions and verifiable completion. » (GPT, précis) ; « Keep AI-assisted projects on course: human decisions, controlled scope, and proof of what was actually done. » (plus simple, dans l'esprit « phrase simple, accrocheuse, réaliste » demandé le 7 sept.). Topics : garder `ai`, `ai-agents`, `ai-coding`, `ai-governance`, `ai-safety`, `ai-tools` ; ajouter `agentic-ai`, `human-in-the-loop`, `llm`, `codex`, `claude-code`, `software-governance` ; retirer `ai-model` (GPT ; d'accord : le projet ne traite pas de modèles). `ai-security` : à garder seulement si le hook et les interdits Git sont présentés comme sécurité, sinon retirer.

### 5.7 Version et manifeste

README, `CONTRIBUTING.md`, `LICENSE`, `examples/` sont hors core. Le test de la démo vit dans `tests/test_template.py` (core) → manifeste régénéré → version `3.9.0` (après 3.8.0), décision `TPL-D-0NN`. Si le test est placé hors core, la version reste mineure de toute façon (nouveau contenu visible).

## 6. Impacts

- `DIRECT` : `README.md` (hors core, premier écran refait, reste relu) ; `CONTRIBUTING.md`, `LICENSE`, `examples/hello-squelette/` (nouveaux, hors core) ; `tests/test_template.py` (+ fixtures) (core) ; `provenance/CHANGELOG.md` (décision, entrée de maintenance) ; si 3.8.0 est promue : `provenance/roadmap-template.v1.json` (chantier P10 état, idée ID-019) et vue régénérée ; `ADOPTION.md` (une phrase sur `examples/`, à vérifier).
- `INDIRECT` : un projet dérivé reçoit le nouveau test par `template-upgrade` (il doit passer hors du template : la démo exporte l'arbre du dépôt où elle tourne — dans un projet dérivé, le test doit se déclarer `NOT_APPLICABLE` ou être conçu indépendant du contenu, comme en 3.4.1) ; `examples/` dans l'export (§ 5.2).
- `AUTHORITY` : le README n'est pas une autorité ; chaque affirmation du premier écran est adossée à un mécanisme nommé (O-09 appliqué au README). `CONTRIBUTING.md` rappelle l'autorité du Project Owner. Décision humaine du template requise pour la version.
- `CONCURRENT` : 3.8.0 en attente de STOP 2 (autre discussion) ; challenge Codex planifié (ID-017) ; Alpha en dernier (ID-018). Cette fiche P10 est postérieure à la liste de migration de P12 § 12.5.7 : à rapatrier dans `provenance/maintenance/scopes/` avec la livraison 3.9.0 si 3.8.0 est promue avant.

## 7. Décisions du Project Owner déjà prises (rappel)

1. README bilingue, paragraphe d'introduction en anglais (7 sept.) ; commits et tags uniquement en français.
2. Push, release, About, Topics : ses gestes, jamais ceux d'un agent (`TPL-D-004`).
3. Publication publique seulement après un second projet réel (7 sept.).
4. Ordre : 3.8.0 → challenge Codex → correctifs éventuels → mise à niveau d'Alpha en dernier (8 sept.).
5. About GitHub : « phrase simple, accrocheuse, réaliste, pas trop technique » (7 sept.).
6. Jamais l'original comme terrain d'essai ; double arrêt avant toute écriture dans un dossier accordé (`TPL-D-011`).

## 8. Décisions attendues du Project Owner

1. ~~**Ordre**~~ — tranché le 8 sept. (01:25) : **après la 3.8.0, avant le challenge Codex**.
2. ~~**Langue**~~ — tranché : **premier écran en anglais puis le même en français, dans le même fichier** ; le reste inchangé.
3. ~~**Exemple**~~ — tranché : **démo rejouable, vraie sortie, vérifiée par un test** ; emplacement `examples/` (réalisé en version d'essai, § 13.3).
4. ~~**Licence**~~ — tranché : **MIT** ; il n'y avait aucune licence dans le dépôt (§ 13.1). Reste à préciser par lui : le nom du titulaire du copyright (ligne `Copyright (c) 2026 …`).
5. **About / Topics** : phrase retenue (§ 5.6) ; retraits et ajouts de Topics.
6. **Release** : première release sur la version vitrine (recommandé) ; notes préparées par Claude, création par lui.
7. **Version** : `3.9.0` (proposé).
8. **Qui rédige** : Claude rédige et le Project Owner relit (proposé) ; ou GPT rédige la « V4 du README » qu'il propose et Claude contre-revoit (schéma déjà pratiqué le 6 sept. pour la mise à jour Codex de V3).
9. **Annonce** : inchangée (après un second projet réel) — confirmer ou modifier.

## 9. Critères de fermeture proposés

1. Aucune sortie de commande dans le README qui ne soit produite par la démo et vérifiée par un test (test rouge si le README diverge — essai : modifier une ligne du bloc, le test échoue).
2. La démo se rejoue en une commande, Python 3 standard, sans dépendance, sur Mac et Linux ; le dépôt reste intact (`git status --porcelain --ignored` vierge après).
3. Le premier écran (avant le premier titre technique) contient : problème, différence, schéma, tableau, démo, essai ; il tient en une hauteur d'écran raisonnable (GPT : « les 25 premières lignes »).
4. `CONTRIBUTING.md` et `LICENSE` présents et cohérents ; la notice de licence est présente dans une copie neuve exportée (essai).
5. Relecture croisée README ↔ `AGENTS.core.md` : aucune promesse du README qui ne soit tenue par un contrôle, une commande ou un test (liste des correspondances dans le rapport de maintenance ; candidat naturel pour le challenge Codex).
6. Tests verts (97 + nouveaux), manifeste régénéré, `audit` et `bootstrap-audit` PASS sur `main` après promotion.
7. Notes de release prêtes ; About et Topics mis à jour par le Project Owner ; le Project Owner confirme que le premier écran lui est lisible en mode simple.

## 10. Limites assumées

- Stars, forks et essais ne se commandent pas : la vitrine améliore la compréhension, pas la garantie d'adoption.
- Le README reste sans autorité : une phrase de README ne l'emporte jamais sur `AGENTS.core.md` ni sur le contrôleur.
- Deux langues = double entretien du premier écran, volontairement limité à quelques dizaines de lignes.
- Release, dépôt public, About, Topics dépendent des gestes du Project Owner.
- Cette V1 est écrite sans lecture du dépôt ; la V2 la corrigera sur pièces.

## 11. Annexe — remarques de GPT, telles que transmises par le Project Owner (2026-09-08)

> **Rôle** — Transformer Squelette V3 d'un dépôt techniquement sérieux en un projet GitHub compréhensible, testable et partageable.
>
> **Contexte** — À partir de ta capture et du README fourni, le projet a déjà une identité assez nette. Le point fort n'est pas « aider une IA à coder ». Le point fort est plutôt : empêcher un projet piloté avec des IA de dériver silencieusement. Tu apportes trois choses qui sont rarement réunies : autorité humaine explicite, périmètre de travail contrôlé et preuve vérifiable de ce qui a réellement été fait. Ton texte actuel est bon pour quelqu'un qui a déjà compris le projet. En revanche, pour un visiteur qui arrive depuis Reddit, Hacker News ou LinkedIn, il commence encore trop « documentation interne ». Le premier écran doit vendre le problème avant d'expliquer le mécanisme.
>
> **Contrainte** — Le principal risque de promotion aujourd'hui est que le visiteur pense : « Encore un template AGENTS.md / prompt framework. » Alors que ton projet va nettement plus loin avec les Work Items, le preflight, les décisions humaines, la provenance du core, les contrôles Git et la Definition of Done. Il faut donc immédiatement montrer cette différence.
>
> **Action** — Je modifierais en priorité les 25 premières lignes du README. Ton titre actuel : « Squelette V3 — garder le cap du projet » est parlant en français, mais insuffisant pour GitHub international. Je passerais à quelque chose comme :
>
> Squelette
> Governance and control for AI-assisted projects.
> Keep the goal, scope, human authority and evidence of completion explicit — even when several AI agents work on the project over time.
>
> Puis immédiatement :
>
> ```
> Human
>   │
>   │ defines goal / scope / decisions
>   ▼
> SQUELETTE
>   │
>   ├── Project Charter
>   ├── Authorized Work Items
>   ├── Human Decisions
>   ├── Preflight controls
>   ├── Git provenance
>   └── Definition of Done
>   │
>   ▼
> AI agents
> ChatGPT · Claude · Codex · Gemini · others
>   │
>   ▼
> Work + evidence
> ```
>
> Puis une section **Why Squelette?** Je la ferais très courte : « Long-running AI projects tend to drift. An agent may forget previous constraints, reinterpret decisions, modify files outside the intended scope or declare work complete without sufficient evidence. Squelette adds a project-control layer between the human and the agents. » Et là, seulement ensuite, tu expliques ton fonctionnement.
>
> Je mettrais également un tableau très visible :
>
> | Sans cadre | Avec Squelette |
> |---|---|
> | « Fais la suite du projet » | Work Item explicitement autorisé |
> | Contexte dépendant du chat | État conservé dans le dépôt |
> | Décisions mélangées aux conversations | Décisions humaines enregistrées |
> | Agent libre d'élargir le périmètre | Scope contrôlé |
> | « Ça devrait fonctionner » | Preuves requises |
> | Changements difficiles à expliquer | Provenance Git |
> | Nouvelle IA = reprise difficile | `status` pour reconstruire l'état |
>
> C'est probablement le meilleur argument commercial du projet.
>
> Il manque aussi à mon avis une démonstration extrêmement simple. Actuellement tu dis : `python3 -B scripts/project_control.py status`. Très bien. Mais le visiteur devrait immédiatement voir ce que cela donne :
>
> ```
> PROJECT
> Goal: Build a local document analysis service
> STATE
> Branch: wi/004-document-import
> Work Item: WI-004
> Authorization: VALID
> Preflight: PASS
> SCOPE
> Allowed:
>   src/import/
>   tests/import/
> Forbidden:
>   authentication/
>   deployment/
> EVIDENCE
> Tests: PASS
> Audit: PASS
> NEXT ACTION
> Project Owner validation required
> ```
>
> Même si cet exemple doit être adapté à la sortie réelle de ton outil, l'effet est très important : en dix secondes, je comprends ce que Squelette apporte.
>
> **Un autre changement important : le vocabulaire.** Je ne présenterais pas principalement Squelette comme un « skeleton ». En anglais, framework, control layer ou governance framework décrivent mieux son ambition. Par exemple : « Squelette is a lightweight governance framework for projects built with AI agents. » Et ta formule actuelle : « who decides, who does, and the proof it's done » est excellente. Je la conserverais presque comme signature : « Who decides. Who does. What proves it's done. » C'est court, mémorisable et directement lié à ton architecture.
>
> **Positionnement GitHub** — Tes Topics sont déjà plutôt bons : ai, ai-agents, ai-coding, ai-governance, ai-safety, ai-security, ai-tools. J'ajouterais probablement, selon la limite GitHub : agentic-ai, human-in-the-loop, project-management, software-governance, llm, codex, claude-code. Je retirerais éventuellement ai-model, car ton projet ne traite pas vraiment de modèles. La description About pourrait devenir : « Governance framework for AI-assisted projects: human authority, controlled scope, persistent decisions and verifiable completion. » C'est plus précis que la version actuelle.
>
> **Avant de promouvoir : 5 éléments** — Je ne lancerais pas encore une grosse communication. Je ferais d'abord ces cinq choses : 1. README orienté problème → solution → démo → fonctionnement. 2. Un vrai release GitHub, probablement v3.0.0 ou une version clairement définie, plutôt que seulement des tags. 3. LICENSE clairement visible. 4. CONTRIBUTING.md très simple. 5. Un projet exemple de quelques minutes permettant de comprendre le cycle complet. Le projet exemple pourrait devenir ton arme principale. Par exemple :
>
> ```
> examples/
> └── hello-squelette/
>     ├── project initialized
>     ├── one human decision
>     ├── one authorized Work Item
>     ├── one completed task
>     └── evidence
> ```
>
> Cela permettrait ensuite de dire : « Clone it. Give FIRST_START.md to Claude/Codex/ChatGPT. See how the agent behaves. » Là, tu n'es plus seulement en train de documenter une méthode : tu la démontres.
>
> **Promotion** — Une fois ces modifications faites, je lancerais d'abord Squelette dans des communautés techniques avec un positionnement de recherche/expérimentation plutôt que marketing. Le titre Hacker News/Reddit que je testerais serait : « I built a governance layer to stop AI agents from silently drifting on long-running projects » et non : « I created Squelette V3 ». Le premier parle du problème du lecteur. Le second parle de ton produit. Pour GitHub même, ton accroche pourrait devenir : « AI agents are good at executing tasks. Keeping a project coherent for weeks or months is a different problem. Squelette is an attempt to solve that. »
>
> **Format de réponse** — À ce stade, je considère que le fond de Squelette est nettement plus intéressant que sa présentation actuelle ne le laisse percevoir. Il ne faut pas chercher à faire plus « joli » : il faut faire comprendre plus vite que ce n'est pas un énième fichier d'instructions pour agent. La priorité serait donc : README → exemple concret → Release → lancement. Je peux maintenant te faire directement une V4 du README d'accueil, en conservant toute ta documentation technique mais en réécrivant seulement la partie visible au premier écran pour maximiser les chances de stars, forks et essais.

### Lecture de Claude, point par point

| Remarque de GPT | Avis | Pourquoi |
|---|---|---|
| Problème → solution → démo → fonctionnement | D'accord | Le constat de la revue du 5 sept. (« très au-dessus des frameworks publics ») n'est pas visible au premier écran. |
| Titre et sous-titre en anglais | D'accord, avec la version française à la suite | Décision « README bilingue » (7 sept.) ; un seul fichier (S-05). |
| Schéma texte | D'accord, à compléter | Ajouter la preuve de lecture et la vue roadmap ; tout ce qui y figure doit exister dans le dépôt. |
| Tableau sans / avec | D'accord, trois lignes de plus | Preuve de lecture, style de retour, double arrêt : ce sont les différences les plus récentes et les plus rares. |
| Sortie de `status` dans le README | D'accord sur l'intention, **pas sur la méthode** | L'extrait proposé est inventé (S-02) ; il sera produit par la démo et vérifié par un test. |
| Vocabulaire « governance framework », signature | D'accord | « Squelette » reste le nom. |
| Topics / About | D'accord dans l'ensemble | Gestes du Project Owner ; phrase About à choisir (§ 5.6). |
| Release « probablement v3.0.0 » | Pas d'accord sur la version | Les tags existent ; la release porte la version courante qui contient la vitrine (§ 5.5). |
| LICENSE, CONTRIBUTING | D'accord | À vérifier ce qui existe ; licence = décision du Project Owner (§ 5.4). |
| `examples/hello-squelette/` figé | D'accord sur l'idée, **pas sur la forme** | Dossier figé impossible à tenir (S-03) ; démo rejouable + transcript testé (§ 5.2). |
| « Clone it. Give FIRST_START.md to … » | D'accord | C'est exactement le parcours réel d'adoption ; à aligner sur `ADOPTION.md`. |
| Promotion HN / Reddit ensuite | D'accord sur « pas maintenant » ; le « quand » est déjà décidé | Après un second projet réel (décision du 7 sept.) ; le challenge Codex passe avant (ID-017). |
| GPT rédige la « V4 du README » | Possible | Décision 8 de § 8 : Claude rédige et le Project Owner relit, ou GPT rédige et Claude contre-revoit. |

## 12. Suite

Réponses du Project Owner aux décisions § 8 → accès en lecture au dossier `Squelette V3 -runtime-proof` (à redemander ; ou bouton « Ajouter un dossier ») → V2 de cette fiche sur pièces (README actuel, `LICENSE`, `CONTRIBUTING`, `examples/`, procédure d'export, fixtures de tests, tags) → prototype hors dossier (copie de travail en espace de session, comme 3.6.1, 3.7.0, 3.8.0) : README premier écran EN/FR, `CONTRIBUTING.md`, `LICENSE` si décidée, démo + transcript + test, notes de release → relecture des textes par le Project Owner (fichiers livrés dans la conversation) → STOP 1 / STOP 2 → livraison sur branche `claude/v3.9-vitrine-github` (nom proposé), aucun tag, aucun push → « promouvoir » sur décision → push, release, About, Topics par lui.

---

## 13. V2 — constat sur pièces, version d'essai, plan de livraison (2026-09-08)

Statut : `PROTOTYPE_READY_OUT_OF_FOLDER — NOT_AUTHORIZED`. Rien n'a été écrit dans `Squelette V3 -runtime-proof` : lecture seule (`GIT_OPTIONAL_LOCKS=0`, `git status --porcelain` vide avant et après chaque lecture, `python3 -B`). La version d'essai vit sur un clone de travail en espace de session (`$HOME/work/sq-vitrine-git`, branche `claude/v3.9-vitrine-github`, commit `5755535` au-dessus de `2487619`) et dans la conversation (fichiers livrés).

### 13.1 Constat sur pièces (lecture seule, 01:27 → 04:50)

- **README.md** (`main` 7964fa4, 55 lignes, 5 073 octets) : titre « Squelette V3 — garder le cap du projet », premier paragraphe en français, second paragraphe en anglais en italique (« A simple frame to run a project with AI agents: who decides, who does, and the proof it's done… »), puis « Commencer ou reprendre », « Utiliser le minimum nécessaire », « Ce que les contrôles garantissent », « Références utiles ». Diagnostic de GPT confirmé : le mécanisme vient avant le problème ; aucune sortie de commande n'est montrée. La 3.8.0 (branche `claude/v3.8-roadmap-in-repo`) ajoute une seule ligne au README (« Vue ROADMAP » dans les références).
- **LICENSE, CONTRIBUTING.md, NOTICE, examples/** : absents (`ls` sur la racine ; 82 fichiers suivis en 3.7.0, 105 en 3.8.0).
- **Tags** : `v3.0.0` → `v3.7.0` ; branches `claude/*` ×10 et `codex/*` ×2 contenues dans `main`, plus `claude/v3.8-roadmap-in-repo` (3 commits, non promue). `origin/main` = `nas/main` = `7964fa4`.
- **`status` réel sur le template** (3.7.0, `main`) : « Projet : UNKNOWN | BOOTSTRAP_MODE / Retour au Project Owner : non choisi (UNKNOWN) … / Branche : main | HEAD : 7964fa4… / Contrôles : PASS / Hook de commit : actif / Squelette : 3.7.0 | core aligné / Travaux terminés : 0 | Bloqués : 0 / Prochaine action : Initialiser le projet avec FIRST_START.md … ». Le contrôleur parle français (O-11).
- **Suite de tests** : 94 tests en 3.7.0, 97 en 3.8.0 ; les fixtures (`make_copy`, `configure_ready_for_closeout`, `make_normal_copy`, `create_lifecycle_work_item`, `write_committed_evidence`, `close_with_evidence`, `test_t_end_to_end_two_work_items_and_two_idle_audits`) construisent déjà des projets initialisés en dossier temporaire : la démo en reprend la méthode (`REUSE`).
- **Procédure d'adoption** (README « Références utiles », `FIRST_START.md` « Utilisation quotidienne », skill) : exporter l'arbre suivi sans `.git`, créer une baseline Git autonome, installer le hook (`git config core.hooksPath scripts/hooks`), lire `FIRST_START.md` et `AGENTS.md`, `bootstrap-audit`, interview, `bootstrap-closeout`, `COMPLETE` conjoint, commit explicite. La démo suit exactement cette procédure.
- **Hook et clôture de l'initialisation** : la transition `NOT_STARTED → COMPLETE` committée sur la canonique est refusée par le hook (`CANONICAL_BRANCH_PROTECTED`) sans `PROJECT_CONTROL_HOOK_OVERRIDE` — c'est la voie documentée (« une écriture directement autorisée sur la canonique s'exécute avec `PROJECT_CONTROL_HOOK_OVERRIDE="<mandat humain>"` », `AGENTS.core.md` Git Safety) ; la démo la montre telle quelle, mandat `HD-001: FIRST_START closeout` (O-12).

### 13.2 Décisions prises (01:25)

Ordre après la 3.8.0 et avant le challenge Codex ; premier écran anglais puis français dans le même fichier ; démo rejouable vérifiée par un test ; licence MIT. Restent ouvertes : titulaire du copyright, About / Topics, release, version (3.9.0 proposé), qui rédige (la version d'essai est rédigée par Claude ; GPT peut la contre-revoir si le Project Owner le souhaite), annonce (inchangée).

### 13.3 La version d'essai (hors du dossier)

Préparée d'abord sur l'arbre 3.7.0, puis **rebasée sur la 3.8.0** (`2487619`) une fois constatée sa livraison sur branche, puisque la vitrine passe après elle. Contenu (9 fichiers, +1 265 / −6) :

1. **`README.md`** — premier écran en anglais : titre « Squelette », sous-titre « Governance and control for AI-assisted projects », signature « Who decides. Who does. What proves it's done. », lien vers la version française, schéma texte (Charter et décisions, Work Items autorisés à chemins explicites, preflight fail-closed, preuve de lecture, provenance Git et hook, Definition of Done), « Why Squelette? » (trois phrases ; « the controller refuses — it does not advise »), tableau « Without a frame / with Squelette » (dix lignes, dont preuve de lecture, style de retour, double arrêt), « Two minutes: one governed change, for real » avec le bloc généré entre `<!-- hello-squelette:begin -->` / `<!-- hello-squelette:end -->` (trois sorties réelles : `status` pendant le chantier, `preflight` refusé hors périmètre, `status` final), « Try it » (clone, démo, tests, puis `FIRST_START.md` à son agent), « What it is — and what it is not » ; puis **le même premier écran en français** (« Squelette — en français ») ; puis la documentation existante de la 3.8.0, inchangée à partir de « Commencer ou reprendre ». Chaque affirmation du tableau est adossée à un mécanisme du dépôt (S-06) : décision humaine exigée par `create-work-item`, records audités, `authorized_paths` + preflight + hook, `context-manifest` / `start --authorities-digest`, preuves par gate, une branche par Work Item et chemins explicites, `status`, `reporting_style`, `Folder scope` + deux confirmations.
2. **`examples/hello-squelette/demo.py`** (663 lignes, bibliothèque standard) — rejoue dans un dossier temporaire : export de l'arbre suivi sans `.git` (`git ls-files`, ou parcours si pas de dépôt), `git init -b main`, commit de la copie vierge, installation du hook ; `status` ; `bootstrap-audit` ; `bootstrap-preflight` refusé sur `modules/hello/greeting.py` et accepté sur les chemins d'interview ; Project Owner scripté (Charter, carte d'architecture et Anti-Octopus, architecture initiale, ADR-0001, HD-001, `REPOSITORY_STATUS`, WI-000, CONV-000, roadmap JSON + Markdown, registre — projet « Hello Squelette », clé `HELLO`, style `PLAIN`) ; `bootstrap-audit`, commit des records (hook : bootstrap-audit) ; `bootstrap-closeout` PASS ; transition `COMPLETE` + WI-000 `DONE`, commit sous `PROJECT_CONTROL_HOOK_OVERRIDE="HD-001: FIRST_START closeout"` ; `audit` ; `status` (au repos) ; `create-work-item WI-001` (HD-002, chemin `modules/hello`, code/tests/integration applicables) ; `context-manifest WI-001` ; `start` refusé sans empreinte, puis accepté avec ; `status` (IN_PROGRESS, autorités lues à jour) ; dérive `modules/billing/invoice.py` indexée → `preflight` refusé (`BUSINESS_CHANGE_AUTHORIZATION`, `AUTHORIZED_PATHS`) ; dérive retirée ; `modules/hello/greeting.py` + `test_greeting.py` indexés → `preflight` PASS ; tests (2 OK) ; commit sur la branche (hook : `WORK_BRANCH_RECORDS_READ_ONLY`) ; merge `--no-ff` dans `main` ; preuves `tests.json` / `integration.json` + artefacts SHA-256, commit (hook : `CANONICAL_BRANCH_PROTECTED` PASS) ; `close WI-001 --commit <feat> …` → `DONE` ; `roadmap-view --write` (3.8.0 : vue Markdown committée par le contrôleur) ; `status` (au repos, vue à jour, 2 travaux terminés) ; `audit` ; `git log --oneline --graph`. Durée : ≈ 2 s. Le dépôt d'origine n'est jamais modifié ; `--write` réécrit `TRANSCRIPT.md` et le bloc du README ; `--check` compare et échoue en cas d'écart (message : la commande pour régénérer) ; `--verbose` garde toutes les lignes `PASS:` ; la démo refuse de tourner hors du template (`repository_role` ≠ `PROJECT_TEMPLATE` ou `NOT_STARTED` absent).
   Normalisation des valeurs volatiles : SHA-256 → `<sha256>`, commits 40 hex → `<commit>`, SHA courts en tête de ligne de `git log --graph` et entre parenthèses → `<sha>`, horodatages → `<timestamp>`, dates → `<date>`, dossier temporaire → `<demo>`, durée des tests → `<duration>` ; les suites de lignes `PASS:` (deux ou plus) sont repliées en « … N controls PASS … » pour que les refus restent lisibles. Déterminisme vérifié : trois `--check` consécutifs verts après un `--write` ; `git log --graph` (ordre topologique) remplace `git log` dont l'ordre variait à la seconde près.
3. **`examples/hello-squelette/TRANSCRIPT.md`** (343 lignes, généré) et **`examples/hello-squelette/README.md`** (mode d'emploi, huit étapes, note en français).
4. **`tests/test_template.py`** — `test_hello_squelette_transcript_and_readme_block_match_the_controller` : lance `demo.py --check` depuis la racine ; ignoré (`skipTest`) hors du template (projet dérivé) ou sans `python3` sur le PATH. Suite : **98 tests OK** sur la 3.8.0 + vitrine (97 + 1), ≈ 55 s dans la VM de session (Python 3.10, git 2.34).
5. **`CONTRIBUTING.md`** (bilingue, court : issue d'abord avec scénario d'échec ; core modifié seulement ici ; bibliothèque standard ; tests, `demo.py --write`, manifeste ; chemins Git explicites, hook et mandat ; commits et tags en français ; « no demonstrated scenario, no change » ; le Project Owner tranche ; ligne pour les agents : « If you are an AI agent: read `AGENTS.md` first »).
6. **`LICENSE`** — texte MIT, ligne de copyright `Copyright (c) 2026 [NOM DU TITULAIRE — à confirmer par le Project Owner]`. La licence voyage avec toute nouvelle copie (arbre suivi exporté) ; elle reste hors core (un projet dérivé garde sa propre licence pour son propre code ; `template-upgrade` n'y touche pas).
7. **`ADOPTION.md`** (core) — section « Exemple et documentation du template » : `examples/` décrit le template, un projet dérivé peut le retirer, `template-upgrade` n'y touche jamais.
8. **`provenance/core-manifest.v1.json`** régénéré (`3.9.0`, 24 fichiers core — le fichier de tests et `ADOPTION.md` changent).

Vérifications : `demo.py --check` vert ×3 ; 98 tests OK ; `bootstrap-audit` sur le clone : refus attendu `BOOTSTRAP_CHANGE_SCOPE` sur les chemins core / hors allowlist tant que la maintenance n'est pas committée (comme toutes les maintenances précédentes) — sur la copie de démo, `bootstrap-audit` PASS (23 contrôles) et `audit` PASS (20 contrôles) après initialisation.

### 13.4 Observations (sans scénario d'échec : rien ne bloque)

- **O-11 — Le contrôleur parle français.** `status`, les libellés de `reporting_style`, la « Prochaine action » sont en français dans un README dont le premier écran est en anglais ; le README le dit (« The controller speaks French for now »). Une sortie anglaise (`--lang en`, ou locale) serait un chantier de P10 étape 2 (publication), à décider ; les commandes, records, schémas et rapports sont neutres.
- **O-12 — Clôture de l'initialisation et hook.** Le commit de la transition `NOT_STARTED → COMPLETE` sur la canonique exige `PROJECT_CONTROL_HOOK_OVERRIDE` (voie documentée, mandat = la décision humaine, visible dans la commande). Option pour une version suivante : que la gate `pre-commit` reconnaisse la transition de clôture (`FIRST_START.md` + `project-state.v1.json` + records du premier Work Item, indexés ensemble, `bootstrap-closeout` PASS) comme administrative, sans mandat d'override. Décision du Project Owner ; la démo montre la voie actuelle telle quelle.
- **O-13 — « Vue roadmap : périmée » sur une copie neuve.** Avant l'initialisation, `status` d'une copie neuve du template (3.8.0) affiche « Vue roadmap : périmée — roadmap-view --write » : la vue du template embarquée sous `provenance/` est jugée contre le HEAD de la copie. Après l'interview : « absente », puis « à jour » après `roadmap-view --write`. Cosmétique ; à signaler à la discussion 3.8.0.
- **O-14 — Règle de maintenance.** Chaque maintenance qui change ce que le contrôleur affiche (ou le nombre de fichiers suivis, ou la version) doit relancer `demo.py --write` avant de committer, sinon le test est rouge ; à ajouter aux règles de `provenance/CHANGELOG.md` à la livraison (c'est déjà dans `CONTRIBUTING.md`).

### 13.5 Plan de livraison (après la promotion de la 3.8.0, après double arrêt)

Dossier cible : `~/Projets/Squelette V3 -runtime-proof`. Préalable : `main` promue en 3.8.0 (`TPL-D-018` à venir, autre discussion), checkout revenu sur `main`. Actions, toutes réversibles tant que rien n'est promu : branche `claude/v3.9-vitrine-github` depuis `main` ; application de la version d'essai (les neuf fichiers ; si `main` a bougé depuis `2487619`, README = nouveau premier écran + documentation courante, puis `core-manifest --write --version 3.9.0` et `demo.py --write` rejoués) ; nom du titulaire dans `LICENSE` ; cette fiche copiée dans `provenance/maintenance/scopes/p10-scope-publication-vitrine-github.md` ; `provenance/CHANGELOG.md` (entrée de maintenance + décision `TPL-D-0NN` : vitrine, MIT, exemple, version 3.9.0) ; `provenance/roadmap-template.v1.json` (chantier P10 état `IN_PROGRESS` / `DELIVERED`, idée ID-019 « Améliore le github avec ces remarques de gpt » du 8 sept., version 3.9.0) ; tests 98 OK, `audit` / `bootstrap-audit` ; premier commit avec `PROJECT_CONTROL_HOOK_OVERRIDE` (mandat), auteur Jeoffrey + trailers Claude, message en français ; puis `roadmap-view --write` dans le dépôt et second commit `chore(provenance): roadmap view` (comme en 3.8.0). Interdits : écriture sur `main`, tag, push, suppression hors verrous Git temporaires. Promotion (« promouvoir » → fast-forward, tag `v3.9.0`), push `origin` + `nas`, release GitHub (notes préparées par Claude depuis le journal), About et Topics : gestes du Project Owner.

### 13.6 Ce qui attend le Project Owner

1. Relire les textes livrés dans la conversation (README, CONTRIBUTING, LICENSE, transcript) et dire ce qui doit changer.
2. Donner le nom à mettre sur la ligne de copyright de `LICENSE`.
3. Promouvoir la 3.8.0 (autre discussion) ; puis, ici, STOP 1 / STOP 2 pour la livraison de la vitrine sur branche.
4. Plus tard, sur décision : release GitHub, About / Topics, O-11 (contrôleur en anglais), O-12, annonce (après un second projet réel).

---

## 14. V3 — livraison dans le dépôt (2026-09-08)

### 14.1 Décisions et confirmations

- Textes relus par le Project Owner : « Réadme ok », puis « 1-Parfait! » (2026-09-08).
- Titulaire du copyright de `LICENSE` (MIT) : « MINET Jeoffrey » (d'abord donné « Jeoffrey MINET », puis corrigé « 2- MINET Jeoffrey »).
- Préalable constaté sur pièces : la 3.8.0 est promue (« C EST PROMU mais pas encore sur git ni sur le nas ») — `main` = `4c93ddf`, tag `v3.8.0` = `e6f53b0` (`TPL-D-018`), checkout sur `main`, arbre propre ; `origin/main` = `nas/main` = `7964fa4` au moment du STOP 1, puis `4c93ddf` constaté au moment de la livraison (« 3-c est fait ! » : la 3.8.0 est envoyée sur GitHub et le NAS).
- Décision du template : `TPL-D-019` (journal `provenance/CHANGELOG.md`) — les quatre décisions du 8 sept. 01:25, la licence MIT et son titulaire, le README validé, les réserves retenues face aux remarques de GPT, la version 3.9.0.
- Double arrêt (`TPL-D-011`) — Folder scope : `~/Projets/Squelette V3 -runtime-proof` (dépôt cible lui-même, O-10 variante B). Confirmation 1 (réponse au STOP 1 : dossier cible, action, ce qu'elle modifie, alternative dans le périmètre) : « Je suis ok ». Confirmation 2 (réponse au STOP 2 : périmètre exact reformulé — branche, actions autorisées et interdites, réversibilité) : « Confirmé : branche claude/v3.9-vitrine-github dans ~/Projets/Squelette V3 -runtime-proof, main intouché, pas de push. » Droit de suppression demandé et limité aux fichiers temporaires de Git (verrous), rien d'autre.

### 14.2 Ce qui est livré, comment

Branche `claude/v3.9-vitrine-github` créée depuis `main` (`4c93ddf`) ; la version d'essai (§ 13.3), rebasée sur la 3.8.0 et complétée, y est appliquée telle quelle : `README.md`, `CONTRIBUTING.md`, `LICENSE` (MINET Jeoffrey), `ADOPTION.md`, `examples/hello-squelette/{demo.py, README.md, TRANSCRIPT.md}`, `tests/test_template.py`, `provenance/core-manifest.v1.json` (3.9.0, 24 fichiers core), `provenance/CHANGELOG.md` (règle de maintenance O-14 en tête, `TPL-D-019`, entrée `claude/v3.9-vitrine-github`), `provenance/roadmap-template.v1.json` (version 3.9.0, chantier P10 `IN_PROGRESS`, idée ID-019, attente « promouvoir la vitrine », étape « après la promotion », entrée du passé ; « Publication, étape 2 … » dans « Plus loin »), cette fiche (`provenance/maintenance/scopes/p10-scope-publication-vitrine-github.md`). Dans le dépôt lui-même, avant le commit : `core-manifest` (aligné), `python3 -B examples/hello-squelette/demo.py --write` (transcript et bloc du README régénérés depuis le vrai dépôt — 110 fichiers suivis), `demo.py --check`, suite de tests complète, `bootstrap-audit` après commit. Deux commits, auteur Jeoffrey, trailers Claude, mandat dans `PROJECT_CONTROL_HOOK_OVERRIDE` : la version, puis `roadmap-view --write` et `chore(provenance): roadmap view (3.9.0, avant promotion)`. Checkout remis sur `main` ; aucun tag, aucun push, `main` inchangé.

### 14.3 Ce qui attend le Project Owner

1. « promouvoir » → fast-forward de `main`, tag `v3.9.0`, décision `TPL-D-020` au journal, vue régénérée ; puis push `origin` + `nas` par lui.
2. Release GitHub sur `v3.9.0` (notes préparées par Claude depuis le journal, création par lui) ; About et Topics (§ 5.6).
3. Plus tard, sur décision : O-11 (messages du contrôleur en anglais), O-12 (clôture de l'initialisation sans mandat d'override), challenge du squelette par Codex (ID-017, après cette version), Alpha en dernier (ID-018), publication étape 2 après un second vrai projet.

### 14.4 Promotion (2026-09-08, soir)

« promouvoir » (Project Owner) → `TPL-D-020`. Entre la livraison et la promotion, `main` avait avancé d'un commit de provenance venu d'une autre discussion (`fe26c06`, sauvegardes 3.8.0 envoyées) : la branche l'a intégré par un commit de merge (`33c5169`, vue régénérée, aucune réécriture d'histoire), puis la décision est enregistrée, le tag `v3.9.0` posé sur ce commit, `main` avancé par fast-forward, la vue régénérée et committée à part sur `main`. Incident sans conséquence : un verrou Git périmé (`.git/HEAD.lock`, laissé par une opération de l'autre discussion) a fait échouer un changement de branche ; il a été retiré au titre du droit de suppression accordé (fichiers temporaires de Git uniquement) et l'état a été vérifié avant de continuer. Restent ses gestes : push `origin` + `nas` de `main` et du tag, release GitHub sur `v3.9.0`, About et Topics ; puis, dans l'ordre décidé : challenge Codex, Alpha en dernier.
