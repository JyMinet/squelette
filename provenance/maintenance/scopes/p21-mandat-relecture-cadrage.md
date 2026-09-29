> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Mandat de relecture — Fiche de cadrage « Tableau des clés » V1

Relecture indépendante d'une fiche de cadrage avant construction. Mandat donné par Jeoffrey (Project Owner) le 2026-09-28 ; rédigé par Claude. Style de retour du Project Owner : PLAIN (le rapport commence par un résumé en trois points ; le corps reste technique).

## 1. Objet

- La fiche `FICHE-CADRAGE-TABLEAU-DES-CLES-V1.md` (texte, aucune mécanique construite).
- Le squelette de projet gouverné en version 3.20.2, fourni en lecture seule dans `source/` (export du tag `v3.20.2`, sans `.git` ni remote), pour juger de la faisabilité et de la cohérence avec l'existant : `AGENTS.core.md`, `scripts/project_control.py`, `project_control/README.md`, `provenance/core-manifest.v1.json`, `provenance/CHANGELOG.md`, `tests/`.

## 2. Dossier accordé

`~/Projets/squelette-revue-tableau-des-cles/` et lui seul :

- `source/` — lecture seule, jamais modifié ;
- `FICHE-CADRAGE-TABLEAU-DES-CLES-V1.md` et ce mandat — lecture seule ;
- `runs/` — clones et copies jetables pour rejouer des scénarios ; tout record, décision ou Work Item fictif créé là est marqué « FIXTURE DE RELECTURE — FICTIF, N'AUTORISE RIEN » ;
- livrable unique à la racine : `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V1.md`, append-only (une correction crée une révision liée, V2 ou erratum, jamais une réécriture).

Aucun accès à l'atelier original (`~/Projets/squelette-atelier`), à `alpha`, à `Redaction_Human`, à `~/Projets/_archives/` ni à tout autre dépôt ou dossier. Aucun envoi en ligne. Aucune suppression hors `runs/`.

## 3. Posture

`READ_ONLY` / `REPORT_ONLY`. Interdits : toute écriture hors du livrable et de `runs/` ; `fetch`, `pull`, `push`, `checkout`, `commit`, `tag`, `branch` dans `source/` ; produire un candidat de code, un ADR, un objet Project Control ou une décision humaine ; recommander une action dans un autre dossier autrement que comme décision à prendre par l'humain. Session indépendante : ne pas lire d'autre relecture avant d'avoir rendu la sienne.

## 4. Thèmes

- **T-01 — Chaque règle ferme-t-elle un scénario réel ?** Pour chacune des sections 5.1 à 5.9 : quel scénario d'échec (S1 parking, S2 second original, S3 perte à l'effacement) la règle ferme-t-elle, et par quel chemin resterait-il ouvert ? Une règle qui ne ferme rien est un constat.
- **T-02 — Cohérence avec la doctrine existante.** Records canoniques committés par le contrôleur (3.2.0), double arrêt et champ `Folder scope` (3.5.0, O-10), « jamais de suppression », baselines d'adoption jamais reconstruites, garde-fou dans `.git/hooks` (3.10.0), preuve de lecture non alourdie. Signaler toute contradiction, et toute règle de la fiche qui existe déjà sous une autre forme (`REUSE > ADAPT > REIMPLEMENT`).
- **T-03 — Faisabilité mécanique.** Le contrôleur peut-il, tel qu'il est en 3.20.2 : lire la ligne `Folder scope:` d'une décision (HD dans `HUMAN_DECISIONS.md`, TPL-D dans `provenance/CHANGELOG.md`) ; vérifier `merge-base --is-ancestor` et les branches d'un autre dépôt en lecture ; poser un record après un tag en gardant la promotion en fast-forward ; afficher une bannière dans `status` à partir du chemin réel du dossier ? Répondre par preuve (chemin, lignes) ou par un essai dans `runs/`.
- **T-04 — Configurations dégradées.** Copie faite par export sans `.git` ; copie déplacée ou renommée ; deux copies pour un même ticket ; copie contenant ses propres clones jetables ; chemin sur un autre volume ; dossier accordé plus large que la copie (limite assumée, section 6) ; projet dérivé qui adopte la règle avec des dossiers déjà présents. Pour chaque cas : la fiche dit-elle ce qui se passe, et ce qui se passe est-il acceptable ?
- **T-05 — Coût.** Ce que la règle ajoute à un chantier ordinaire (arguments, commandes, lectures) et à un démarrage de session ; la fiche prétend « zéro lecture supplémentaire au démarrage » — vrai ou faux, avec preuve.
- **T-06 — Les options écartées.** Branches seules, worktrees, fichier marqueur, jumeau Markdown, retard comme échec d'audit, inventaire du disque : l'écart est-il justifié par un scénario, ou par une préférence ?

Avis non liant demandé, en fin de rapport, sur les sept questions de la section 8 de la fiche.

## 5. Standard

Sans scénario d'échec démontré, pas de redline : une observation reste une observation. Un constat porte : identifiant, sévérité (BLOCKER / MAJOR / MINOR), objet (section de la fiche ou fichier de `source/`), scénario reproductible, preuve (chemin, lignes, octets, SHA-256 ; ou rejeu dans `runs/`), impact, correction proposée, statut.

## 6. Verdict terminal (liste fermée)

`CADRAGE_TABLEAU_DES_CLES_V1_PASS` · `…_REQUIRES_MINOR_REDLINE` · `…_REQUIRES_MAJOR_REDLINE` · `…_CANONICAL_CONFLICT` · `…_INPUT_MISSING` · `…_OUTPUT_ALREADY_EXISTS`. Un verdict hors liste est un défaut de livrable.

## 7. Structure du livrable

Résumé en trois points pour le Project Owner, puis sections lettrées dans cet ordre : A preflight (état exact de `source/` : chemin, empreintes des fichiers lus) ; B inventaire ; C rejeu des scénarios (T-01, T-04) ; D constats ; E redlines ; F blockers ; G conflits d'autorité ; H avis sur les sept questions ; I état du dossier en fin de mandat (rien d'écrit hors livrable et `runs/`) ; J verdict terminal.

## 8. Après la relecture

Le livrable et ce mandat sont copiés dans l'atelier (`provenance/maintenance/`) par un geste séparé sous double arrêt ; le dossier de relecture est ensuite effacé par Jeoffrey. C'est la première copie à suivre la règle que la fiche propose (annexe A de la fiche).
