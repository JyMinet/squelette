> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# P17 — L'histoire figée qui peut être défigée

*Fiche de cadrage. 10 septembre 2026, ouverte par la troisième passe de contrôle ; tranchée et livrée le 11 septembre 2026.*

## 1. Ce qui est en cause

Un projet qui adopte le contrôleur avec un historique déclare une **baseline d'adoption** dans son
état de projet, par décision humaine. Tout ce qui est avant cette ligne est lu tel qu'il a été
écrit : ses clôtures ne sont **ni reconstruites ni requalifiées**, et toute modification de leurs
records est refusée. C'est la promesse qui rend l'adoption possible — sans elle, aucun projet
existant ne pourrait passer sous gouvernance sans réécrire son passé.

La troisième passe de contrôle a démontré que cette ligne peut être déplacée, et l'histoire derrière
elle réécrite puis refigée. Ce qui rend le constat sérieux, c'est qu'il n'emploie **aucun moyen
détourné** : ni dérogation au garde-fou, ni modification du contrôleur, ni réécriture de l'historique
Git, ni privilège système.

## 2. Le scénario, tel qu'il a été exécuté

1. Un chantier est ouvert avec `project_control/project-state.v1.json` dans ses chemins autorisés —
   ce qui est légitime : c'est le fichier où vivent la langue, le style de retour et les baselines.
2. Ce chantier met la baseline à `null`, committe, intègre et se clôt normalement. À partir de là,
   plus rien ne protège les clôtures anciennes.
3. Sur la branche principale, on modifie l'objectif d'un travail figé depuis des semaines. Le
   commit passe, garde-fou actif, avec l'audit du disque **et** de l'index.
4. Un nouveau chantier redéclare la baseline sur le commit qui contient la modification, **en citant
   la même décision humaine qu'à l'origine** — une décision qui nomme pourtant la baseline
   précédente. L'audit et la clôture passent.
5. Dans une autre copie, le contrôle est allé plus loin : un travail terminé et figé a été remis à
   son état antérieur, redémarré, puis **clos une seconde fois**. Audit final `PASS`.

Ce qui est perdu, ce ne sont pas les anciens commits — ils restent dans Git. C'est leur **statut de
référence intouchable** dans le contrôle courant.

## 3. La cause, en une phrase

Le contrôleur vérifie que la baseline pointe sur un commit qui existe et descend de la branche
courante, et qu'une décision humaine structurée l'accompagne. **Il ne vérifie jamais que cette
décision-là parle de cette baseline-là.** Une décision qui autorisait la ligne A sert à déclarer la
ligne B. Rien n'ancre la déclaration à son mandat.

## 4. Les pistes, et ce qu'elles coûtent

### Piste 1 — Ancrer la déclaration à sa décision *(le fond du problème)*

La décision qui déclare une baseline **nomme le commit**, et le contrôleur refuse une déclaration
dont le commit n'est pas celui que la décision cite. Une nouvelle baseline exige alors une nouvelle
décision, qui dit quel commit et pourquoi.

- **Ce que ça règle :** l'étape 4 du scénario devient impossible. C'est le cœur.
- **Ce que ça coûte :** un champ de plus dans les décisions de ce type, et donc une question de
  compatibilité — **Alpha a deux baselines déclarées** par des décisions qui ne portent
  pas ce champ. Il faut décider ce qu'on fait des déclarations existantes : les accepter telles
  quelles et n'exiger le champ que pour les nouvelles, ou demander une décision de confirmation.
  C'est la vraie question de ce chantier, et elle est pour toi.

### Piste 2 — Retirer une baseline est un geste à part

Aujourd'hui, mettre la baseline à `null` est une écriture ordinaire dans un fichier autorisé.
Ça pourrait exiger sa propre décision, comme un blocage ou une reprise en exigent une.

- **Ce que ça règle :** l'étape 2, la porte d'entrée du scénario.
- **Ce que ça coûte :** peu. C'est la piste la plus simple, et elle est indépendante de la première.

### Piste 3 — Une baseline ne recule jamais

Une nouvelle baseline doit être un descendant de l'ancienne. On peut avancer la ligne du passé, on
ne peut pas la reculer ni la déplacer latéralement.

- **Ce que ça règle :** une partie des variantes, pas le scénario principal — dans le scénario, la
  nouvelle baseline **est** un descendant.
- **Ce que ça coûte :** peu, mais l'effet est partiel. À prendre en complément, pas seule.

### Piste 4 — Un travail figé ne se rouvre pas

Un Work Item `DONE` avant la baseline ne peut pas revenir à un état antérieur, quelle que soit la
baseline courante — son identité et son empreinte sont retenues ailleurs que dans l'état de projet.

- **Ce que ça règle :** l'étape 5, la double clôture.
- **Ce que ça coûte :** il faut décider **où** cette mémoire vit, pour qu'elle ne soit pas elle-même
  effaçable par un chantier autorisé. C'est la question difficile de cette piste, et elle mérite
  d'être posée avant d'écrire quoi que ce soit.

## 5. Ce que je recommanderais

Les pistes 2 et 3 sont courtes, sûres et indépendantes : elles ferment la porte d'entrée sans rien
changer au format des décisions. La piste 1 est le fond, et elle demande **ta** décision sur les
déclarations existantes d'Alpha. La piste 4 demande une réflexion sur l'endroit où
loger une mémoire qu'un chantier ne peut pas effacer.

Je ne recommande pas de tout faire d'un coup. Mais je ne recommande pas non plus de s'arrêter aux
pistes 2 et 3 : elles rendent le scénario plus difficile, pas impossible.

## 6. Questions ouvertes

1. **Les baselines déjà déclarées** (Alpha en a deux) : acceptées telles quelles, ou
   confirmées par une nouvelle décision qui nomme leur commit ?
2. **Où loger la mémoire d'un travail figé**, pour qu'un chantier autorisé ne puisse pas l'effacer ?
   Dans le journal du projet, dans un fichier propre au contrôleur, ailleurs ?
3. **Le fichier d'état du projet devrait-il rester ouvert aux chantiers ordinaires ?** C'est par là
   que tout passe. Le fermer aurait d'autres conséquences — la langue et le style y vivent aussi.
4. **Une quatrième passe de contrôle** après ce chantier, ou attend-on d'avoir plus de kilomètres
   sur les projets réels ?

## 7. Réponses du Project Owner (11 septembre 2026)

1. **Les baselines déjà déclarées** — « On confirme ! » (`TPL-D-053`) : chacune reçoit une décision
   de confirmation qui nomme son commit exact et cite la décision d'origine, laquelle n'est pas
   réécrite ; puis un chantier fait citer ces décisions par l'état du projet. Pour
   Alpha : deux décisions, un petit chantier, **avant** la montée vers la 3.18.0.
2. **Où loger la mémoire d'un travail figé** — nulle part de neuf : **dans Git, au commit de la
   baseline**. Le contrôleur relisait déjà les records figés tels que Git les tient à ce commit
   (`legacy_records`). L'historique n'est pas ce qu'un chantier peut effacer ; ce qui manquait,
   c'était que la ligne ne bouge pas en silence.
3. **Le fichier d'état reste ouvert aux chantiers** — oui, mais ses deux lignes de baseline changent
   de régime : elles ne se retirent, ne se déplacent et ne se redéclarent que sur une décision qui
   nomme le commit visé, ou qui dit qu'on retire la ligne. Pistes 1 et 2 de cette fiche en une seule
   règle, plus la piste 3 ; la piste 4 en découle — une double clôture exige désormais deux
   décisions humaines qui disent chacune ce qu'elles font.
4. **Une quatrième passe de contrôle** — oui, juste après ce chantier, sur une version taguée,
   avec le mandat habituel : ce chantier touche le format des décisions et la protection du passé.

« je suis d'accord » — Project Owner, 11 septembre 2026, sur ces trois réponses proposées ensemble.

## 8. État

`DONE`. Livré en `3.18.0` (`TPL-D-056` cadrage et mandat, `TPL-D-057` livraison) :

- **Règle 1 — la décision d'une baseline nomme son commit.** `Legacy baseline commit:` /
  `Authorities baseline commit:` ; l'audit refuse une déclaration dont le commit n'est pas celui que
  sa décision cite. L'étape 4 du scénario est fermée.
- **Règle 2 — retirer une baseline est un geste à part.** Le garde-fou (`BASELINE_CHANGE_MANDATED`)
  refuse un commit qui efface une baseline sans une décision du chantier en cours, enregistrée sur
  la canonique, qui porte `Legacy baseline removed: <commit>`. L'étape 2 est fermée.
- **Règle 3 — une baseline ne recule jamais.** Un déplacement vers un commit qui ne descend pas de
  l'ancien est refusé par le même garde-fou.
- **Règle 4 — une montée se répète avant de s'écrire.** `template-upgrade` extrait `HEAD` dans un
  worktree jetable, y écrit le core prévu, y lance l'audit **du nouveau contrôleur** et refuse
  `--apply` tant que cet audit refuse (`UPGRADE_REHEARSAL`). Générique : c'est le mur de la 3.8.0
  (trois registres) comme celui des baselines à confirmer.

Six essais, chacun rouge sur la `3.17.1` et vert en `3.18.0`, dont le scénario complet de la
troisième passe rejoué et arrêté à l'étape 2, et deux qui passent par de vrais `git commit`.

Reste : les deux décisions de confirmation d'Alpha et son chantier de citation, puis sa
montée ; la quatrième passe de contrôle.

## 9. Quatrième passe de contrôle (11 septembre 2026, soir)

Rapport : `provenance/maintenance/2026-09-11-controle-independant-3.18.0.md`. Verdict
`SQUELETTE_3.18.0_REQUIRES_MAJOR_REDLINE`, quatre anomalies reproduites avec de vrais commits ; les
onze corrections précédentes tiennent toutes.

- **F12-01, majeur.** La règle 2 ne s'appliquait que sur la branche de chantier, « hors fusion » ; et
  la vérification des fusions d'intégration ne regardait que les *noms* des fichiers apportés, pas
  leur contenu. Un chantier qui avait légitimement touché l'état du projet pouvait donc voir sa
  fusion dans `main` éditée avant son commit — la baseline retirée sur le chemin — puis une clôture
  figée réécrite, audit au vert. Corrigé en `3.18.1` : une fusion d'intégration n'emporte que le
  contenu de sa branche, fichier par fichier, et la règle des baselines s'applique partout où l'état
  du projet entre dans un commit.
- **F13-01 et F13-02, modérés.** La répétition de montée refusait à tort une montée où seul le
  garde-fou change (code de sortie lu comme un second échec), et pouvait répéter avec l'ancien
  contrôleur si le nouveau core était déjà sur le disque sans être committé. Corrigés : la répétition
  est mesurée contre `HEAD`, et un audit qui n'échoue que sur le garde-fou est une réussite.
- **F14-01, modéré.** Une interruption clavier entre l'écriture d'un temporaire et son renommage le
  laissait derrière elle. Corrigé : l'interruption n'est pas une exception ordinaire, le temporaire
  est effacé quand même.
- **La dette de la section 8 est démontrée** (un JSON à moitié écrit dans un dossier ignoré fait
  échouer deux essais) et traitée : les copies d'essai n'emportent plus ce que le squelette ignore.
- Observation retenue : une décision `REJECT` portant le champ d'ancrage déclarait une baseline. Un
  refus ne déclare rien, désormais.

Sept essais, chacun rouge sur la `3.18.0` et vert en `3.18.1`.

