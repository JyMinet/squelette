> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# ROADMAP SQUELETTE — mémoire du tableau

Ce document est la mémoire du tableau de bord « ROADMAP SQUELETTE » (chantier P12, fiche `claude/p12-scope-roadmap-dediee.md`). Il est lu en premier par toute session qui régénère le tableau ; il n'est jamais une preuve : les sources font foi (dépôt en lecture seule, fiches du projet, messages du Project Owner).

## Page

- Adresse : https://claude.ai/code/artifact/6e74eaa9-8e15-492d-b89b-7156bf1588ba — republier **à cette adresse** (paramètre `url`), jamais en créer une autre.
- Fichier source de la dernière version : contenu HTML autonome (CSS et script inclus), forme « stable » décrite ci-dessous.
- Titre de page : `ROADMAP SQUELETTE` (ne pas changer) ; icône 🗺️.

## Réglages de la vue (modifiables seulement par « RÉGLAGE : clé = valeur » dans la discussion ROADMAP)

| Clé | Valeur | Depuis |
|---|---|---|
| `regeneration` | `daily` — tâche planifiée « ROADMAP SQUELETTE — mise à jour quotidienne », chaque jour à 08:00 Europe/Zurich (06:00 UTC), liée au Mac, lecture seule, ne republie que si quelque chose a changé ; créée sur « Tu peux aller au bout ! Je valide la suite » (approbation de la carte par le Project Owner) | 2026-09-07 |
| `style` | `simple` (demande du Project Owner : « lisible par tous, surtout pas pour un ingénieur IT ») | 2026-09-07 |
| `zoom` | `passe=replie`, `loin=titres` | 2026-09-07 |
| `forme` | `stable` | 2026-09-07 |
| `langue` | `fr` | 2026-09-07 |
| `sources` | dépôt `~/Projets/Squelette V3 -runtime-proof` (lecture seule) ; fiches `claude/*.md` de ce projet ; messages du Project Owner | 2026-09-07 |

## Dernière vérification

- Date : 2026-09-08, 00:20 (Europe/Zurich) — cinquième lecture (23:15, 23:33, 23:35, 23:55, 00:20) : `main` = `7964fa4`, checkout `main`, arbre propre ; remotes lus à 23:55 ; contrôles à 23:35.
- Dépôt lu en lecture seule (`GIT_OPTIONAL_LOCKS=0`, `python3 -B`) : `main` = `7964fa45239a233fee9d7198996b3c36f48181d4` = tag `v3.7.0` (promue à 23:34 par l'autre discussion ; à 23:15 `main` = `0d5d86f` = `v3.6.1`) ; `origin/main` = `nas/main` = `7964fa4` (v3.7.0, poussés par le Project Owner vers 23:50) ; arbre propre (`git status --porcelain --ignored` vide) ; 12 branches (`claude/*` ×10, `codex/*` ×2) toutes contenues dans `main` ; tags `v3.0.0` (35da2a2) → `v3.7.0` (7964fa4).
- Contrôles sur `main` 3.7.0 : `bootstrap-audit` PASS (20 contrôles) ; `audit` PASS ; `status` : `BOOTSTRAP_MODE`, nouvelle ligne « Retour au Project Owner : non choisi (UNKNOWN) », hook actif, « Squelette : 3.7.0 | core aligné » ; manifeste core 3.7.0 ; 94 tests dans `tests/test_template.py` (94/94 OK à la livraison, journal).
- Décisions du template : `TPL-D-001` → `TPL-D-016` (`provenance/CHANGELOG.md` ; TPL-D-016 = promotion 3.7.0, « simple et promouvoir »).
- Non vérifié ce soir : `alpha` (fiche P2 § 18 : `main` = `a31faa9`, core 3.6.1, push NAS à faire par le Project Owner).

## Forme stable de la page (à reproduire à l'identique, contenu mis à jour)

1. En-tête : eyebrow « Squelette de projet · tableau de bord », titre, chapeau ; bandeau de vérification en langage courant (Vérifié le / Comment / Version / Sauvegardes / Vérifications / Mise à jour).
2. Quatre chiffres : version actuelle, décisions prises, vérifications automatiques (tests), chantiers ouverts dans le dossier.
3. « Les versions, dans l'ordre » : stepper ordinal 3.0.0 → version actuelle (anneau « ACTUELLE ») → prochaine version en pointillé, avec date et deux mots.
4. Deux colonnes : gauche « Maintenant » (détail) puis « Ce qui t'attend » (actions du Project Owner, liseré ambre) ; droite « Prochaines étapes » (détail) puis « Plus loin » (titres).
5. « Tes idées, et ce qu'elles sont devenues » : table Quand / Ton idée (citée) / Ce qu'elle est devenue / État (liste close de la fiche P12 § 5.3).
6. « Les chantiers, du premier au douzième » : table N° / Chantier (nom en langage courant) / État / Où en est-on / Fiche.
7. « Ce qui est derrière nous » : arbre replié (`details`), une entrée par version ou événement, sous-entrées pour les épisodes, boutons « Tout déployer / Tout replier » ; dernier repli « Pour les techniciens » avec les identifiants (HEAD, tags, contrôles, commandes).
8. Pied : « Règles de ce tableau », « Réglages de la vue », « Comment s'en servir ».
Style simple : aucun identifiant technique hors du repli « Pour les techniciens » ; sources nommées simplement (« dossier du squelette, lu ce soir », « fiche P2 », « ton message du 7 sept. »).

## Procédure de régénération (skill `roadmap-squelette`)

1. Lire ce document. 2. Lire les sources : demander l'accès en lecture au dossier du squelette si la session ne l'a pas (sinon marquer « non vérifié depuis <date> » sur les lignes issues du dépôt) ; commandes read-only seulement ; lire les fiches `claude/*.md` (lignes de statut) ; relever les idées nouvelles du Project Owner dans les discussions connues. 3. Comparer avec « Dernière vérification » et « État du tableau » ci-dessous ; si rien n'a changé, ne rien republier et le dire en une ligne. 4. Sinon reconstruire la page dans la forme stable, republier à l'adresse ci-dessus, mettre à jour ce document (vérification, état, journal). 5. Répondre en une ligne. Tout le reste est refusé et renvoyé vers une autre discussion (fiche P12 § 5.6).

## État du tableau (contenu textuel, 2026-09-07 23:35)

**Maintenant.** Version 3.7.0 promue ce soir (style de retour au choix + O-10), 94 tests, 20 contrôles PASS ; sauvegardes GitHub et NAS en 3.7.0 (faites par le Project Owner) ; aucun chantier ouvert (12 branches intégrées) ; le squelette est un modèle sans roadmap propre (journal 16 décisions + fiches) ; Alpha en 3.6.1 (non vérifié ce soir), sauvegarde NAS à envoyer.

**Ce qui attend le Project Owner.** (1) Approuver la tâche planifiée quotidienne (carte) ; rythme modifiable par « RÉGLAGE : regeneration = … ». (2) Enregistrer les deux cartes de skill : `roadmap-squelette` et la mise à jour de `squelette-projet` (3.7.0). (3) P12 étape 2 : recommandations validées (« je suis ok avec la suite, on va de l'avant ») → prototype 3.8.0 hors dossier, puis STOP 1 / STOP 2. (4) Alpha : en dernier (« on terminera par la mise à jour Alpha ») — après 3.8.0, montée en une fois avec PLAIN (double arrêt car original) ; sauvegarde NAS d'Alpha à envoyer.

**Prochaines étapes.** Alpha vers la version stabilisée du squelette (reporté, sa décision) ; skills enregistrées puis première régénération depuis une autre discussion (vérifier la forme stable) ; O-09 (documents annexes) dans une version suivante, à cadrer ; plus tard sur décision : P4, P5, P6 après un second vrai projet. Fiche P11 mise à jour (V2) le 7 sept.

**Plus loin.** P4 revue contradictoire (cadrée, non autorisée) ; P5 phases ; P6 guide de reprise dans le dossier ; P7 critères d'entrée ; P8 restes (profil d'adoption audité, exercice de restauration) ; P10 publication / plugin après un second vrai projet.

**Idées du Project Owner (17).** Revue indépendante + intégration Claude (5 sept., réalisée) ; trame / suivi / roadmap (5 sept., en cours) ; Codex sur V3 + vérification (6 sept., réalisée) ; sauvegarde GitHub puis NAS (7 sept., réalisée) ; README en anglais (7 sept., réalisée) ; mettre à niveau Alpha (7 sept., réalisée) ; jamais l'original + deux stop (7 sept., réalisée : 3.5.0) ; « on ne supprime pas V3 » (7 sept., appliquée) ; plugin Claude (7 sept., plus tard) ; style de retour au choix (7 sept., réalisée : 3.7.0 promue) ; discussion ROADMAP dédiée (7 sept., en cours) ; régénération automatique au choix (7 sept., intégrée : chaque jour à 8 h, modifiable) ; réglages via le squelette, bloqués pour le projet (7 sept., intégrée) ; tableau simple + idées visibles (7 sept., intégrée) ; « on va attendre car le squelette se développe » → mise à niveau d'Alpha reportée (7 sept., appliquée). « toutes les infos dans le dossier physique, format JSON ? » → P12 étape 2 cadrée, fusion P6, recommandations validées (8 sept., en cours) ; « on terminera par la mise à jour Alpha » (8 sept., appliquée : Alpha en dernier). Total : 17 idées (une ligne retirée à la demande du Project Owner le 8 sept.).

**Chantiers.** P1 fait ; P2 fait ; P3 fait ; P4 cadré ; P5 à cadrer ; P6 à cadrer ; P7 à cadrer ; P8 partiel ; P9 fait ; P10 plus tard ; P11 fait (3.7.0 promue et sauvegardée ; fiche V2) ; P12 étape 1 faite, étape 2 cadrée (fiche § 12, sept décisions attendues) ; P6 cadré avec elle.

**Passé (entrées de l'arbre).** 5 sept. revue + 3.0.0 ; 6 sept. 3.1.0 (Codex, contre-revue, redlines, TPL-D-001..003) ; 6 sept. 3.2.0 (hook, P9-A, GitHub) ; 6 sept. 3.3.0 (legacy_baseline, README) ; 6 sept. 3.4.0 (manifeste, template-upgrade) ; 7 sept. 3.4.1 (tests autonomes, répétition) ; 7 sept. 3.5.0 (dérive WI-061, retour arrière, double arrêt ; sous-entrée : répétition sur copie PASS) ; 7 sept. 3.6.0 (P3) ; 7 sept. 3.6.1 (RL-T-01, authorities_baseline ; sous-entrée : Alpha → 3.6.1 dans l'original) ; 7 sept. 3.7.0 (P11 + O-10, TPL-D-016) ; 7 sept. fiches P11 et P12 ; repli « Pour les techniciens ».

## Journal des régénérations

- 2026-09-07 23:20 — première instance (technique), dépôt lu à 23:15 (main 0d5d86f = v3.6.1).
- 2026-09-07 23:30 — version simple + bloc « Tes idées », même adresse (retour du Project Owner : « lisible par tous », « les idées évoquées doivent apparaître »).
- 2026-09-07 23:47 — premier passage de la tâche planifiée (session automatique) : aucun dossier attaché (carte non encore approuvée), fiches relues, page republiée avec « non vérifié » ; skills non encore enregistrées à cette heure.
- 2026-09-08 00:45 — ligne « pas obligé d'avoir un dépôt » retirée du tableau et de ce document à la demande du Project Owner (« cette info est has been ») ; P12 étape 2 passée « en cours » (recommandations validées) ; Alpha noté « en dernier ».
- 2026-09-08 00:35 — la discussion ROADMAP a fusionné ce passage avec sa lecture du dossier de 00:20 (chips « non vérifié » levés), ajouté l'idée « JSON dans le dossier » (cadrée) et P12 étape 2 / P6 ; conflit de version géré par relecture complète de la version publiée avant republication.
- 2026-09-08 00:30 — cinquième version (non publiée telle quelle : fusionnée à 00:35) : idée « JSON dans le dossier » ajoutée (cadrée), P12 étape 2 et P6 dans « Ce qui t'attend » et « Prochaines étapes ».
- 2026-09-07 23:58 — quatrième version : sauvegardes 3.7.0 constatées faites (origin = nas = 7964fa4) ; réglage `regeneration = daily` (tâche planifiée créée) ; « Ce qui t'attend » et « Prochaines étapes » refaits ; fiche P11 V2 déposée.
- 2026-09-07 23:50 — ligne « pas obligé d'avoir un dépôt » passée à « écartée » (retirée par le Project Owner) ; question ouverte supprimée de « Ce qui t'attend ».
- 2026-09-07 23:38 — troisième version : relecture du dépôt à 23:33 puis 23:35 → 3.7.0 livrée puis promue par l'autre discussion (TPL-D-016) ; tableau mis à jour (version, sauvegardes en retard, chantiers, idée P11 réalisée, entrée du passé, repli technique). Séance « ROADMAP » du projet Squelette (Claude, Cowork) ; lecture seule, `git status` vierge après chaque lecture.
