> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Mandat de relecture courte — Fiche de cadrage « Tableau des clés » V2

Contrôle de fermeture des corrections, avant construction. Mandat donné par Jeoffrey (Project Owner) le 2026-09-28 ; rédigé par Claude. Style de retour du Project Owner : PLAIN (résumé en trois points en tête ; corps technique).

Relecture **courte et ciblée** : on vérifie que les sept corrections ferment les scénarios démontrés au tour précédent et n'en ouvrent pas de nouveaux. Pas de relecture complète du contrôleur ni de la suite d'essais ; lire seulement ce qu'il faut pour trancher.

## 1. Objet

- `FICHE-CADRAGE-TABLEAU-DES-CLES-V2.md` (avec sa section 11 : décisions du Project Owner, prises).
- Pièces de référence, lecture seule : ta relecture `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V1_V2.md` et ses fixtures sous `runs/` ; la contre-revue `CONTRE-REVUE-RELECTURE-TABLEAU-DES-CLES-V2.md` ; `source/` (squelette 3.20.2, inchangé, vérifiable par `SOURCE-MANIFESTE.sha256`).

## 2. Dossier accordé

`~/Projets/squelette-revue-tableau-des-cles/` et lui seul. Tout ce qui y existe est en lecture seule, sauf :

- `runs/v2/` — nouveau sous-dossier pour les sondes de ce tour (les dossiers existants de `runs/` ne sont ni modifiés ni recréés) ; fixtures marquées « FIXTURE DE RELECTURE — FICTIF, N'AUTORISE RIEN » ;
- livrable unique à la racine : `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V2.md`, création exclusive, append-only.

Aucun accès à l'atelier, à `alpha`, à `Redaction_Human`, à `~/Projets/_archives/` ni à tout autre dossier. Aucun envoi en ligne. Aucune suppression.

## 3. Posture

`READ_ONLY` / `REPORT_ONLY`, mêmes interdits qu'au tour précédent. Les décisions de la section 11 de la fiche sont des décisions humaines prises : on peut en signaler une conséquence dangereuse, on ne les rediscute pas.

## 4. Ce qu'il faut vérifier

**V-01 à V-07 — fermeture.** Pour chacun de R01 à R07 : la correction de la V2 (table de la section 0) ferme-t-elle le scénario démontré ? Rejouer contre les règles écrites de la V2 les sondes pertinentes du tour précédent (au minimum P06, P07, P09, P04, P10/P11) dans `runs/v2/`. Verdict par constat : `FERMÉ` | `PARTIEL` (avec le chemin qui reste ouvert) | `OUVERT`.

**V-08 — nouveaux trous.** Les corrections ont-elles ouvert un scénario d'échec ? Points à regarder en priorité :

- la fiche de sortie dans `.git/copie.json` (clone) et à la racine du contenant (export) : un outil existant du contrôleur la lit-il, l'ignore-t-il, peut-elle être prise pour autre chose ?
- l'inventaire du retour (`git status --porcelain=v2 --ignored`, stash, références) : un cas manque-t-il (sous-modules, worktrees de la copie, fichiers dans `.git/` hors `copie.json`, hooks) ?
- `copy check` : la comparaison d'empreinte et d'identité (device + inode) suffit-elle ; la fenêtre déclarée entre contrôle et effacement est-elle correctement bornée ;
- l'ordre de clôture de 5.7 : est-il compatible avec la promotion telle que la décrit le CHANGELOG de `source/` (décision enregistrée sur la branche, fast-forward, vue régénérée, tag) ; la réparation limitée de `COPIES_RETURNED` peut-elle servir à masquer un autre échec ;
- la transition `KEPT → RETURNED` et `copy move` : réintroduisent-elles R01 ou R03 ?

**V-09 — cohérence interne.** Contradictions restantes entre sections (comme celle de la V1 entre 4.4 et 5.7), et entre la section 11 et le reste de la fiche.

## 5. Standard et verdict

Même standard que le tour précédent : sans scénario démontré, pas de redline. Verdict terminal, liste fermée :

`CADRAGE_TABLEAU_DES_CLES_V2_PASS` · `…_REQUIRES_MINOR_REDLINE` · `…_REQUIRES_MAJOR_REDLINE` · `…_CANONICAL_CONFLICT` · `…_INPUT_MISSING` · `…_OUTPUT_ALREADY_EXISTS`.

## 6. Structure du livrable (court)

Résumé en trois points ; A preflight (empreintes des pièces lues, `source/` revérifié) ; B table R01–R07 → FERMÉ / PARTIEL / OUVERT avec preuve ; C nouveaux constats (V-08, V-09) au format habituel ; D état du dossier en fin de mandat ; E verdict terminal.

## 7. Après la relecture

Les papiers de ce dossier (deux relectures, deux mandats, deux fiches, la contre-revue) sont rapatriés dans l'atelier par un geste séparé sous double arrêt ; `runs/` est abandonné comme jetable ; le dossier est ensuite effacé par Jeoffrey.
