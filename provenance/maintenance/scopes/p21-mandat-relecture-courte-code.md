> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Mandat de relecture courte du code — chantier P21 « Tableau des clés » (3.21.0)

Contrôle de fermeture des corrections, avant livraison. Suite de ta relecture `RELECTURE_CODE_P21.md` (verdict `CODE_P21_REQUIRES_MAJOR_REDLINE`), qui demandait de « faire rejouer ces reproductions et la suite complète avant livraison ». Mandat donné par Jeoffrey (Project Owner) ; rédigé par Claude, auteur du code et des corrections — conflit d'intérêt déclaré. Style de retour du Project Owner : PLAIN (résumé en trois points en tête ; le corps peut être technique).

Relecture **courte et ciblée** : on vérifie que les corrections ferment tes six constats et le constat supplémentaire trouvé en les fermant, et qu'elles n'ouvrent pas de nouveau trou. Pas de relecture complète du contrôleur ni de la suite d'essais ; lire seulement ce qu'il faut pour trancher.

## 1. Objet

- Dépôt : `~/Projets/squelette-chantier-p21`.
- Code relu : la branche `claude/p21-tableau-des-cles` au commit `2b4b64606c330b53a3729ee52e5fe11b1cfa33db`. Les corrections sont dans `git diff 0ecb5464fdd1e03534dbb32ffc1d487907e4da14..2b4b64606c330b53a3729ee52e5fe11b1cfa33db` (commit `e8534bf`, puis la vue régénérée). Empreintes attendues au commit relu : `scripts/project_control.py` SHA-256 `86307fac9589c7b80e4f3f3e3403998477c54e9539d47befcb073aa38e69fd6f` ; `tests/test_template.py` SHA-256 `e27fb846c1a59595ac324d72a7b70282dd8983cedec4c59d1521fe742bf2a5d0`.
- Pièces de référence, en lecture seule : ta relecture `RELECTURE_CODE_P21.md` et tes sondes sous `revue-code/` ; la contre-revue `CONTRE-REVUE-RELECTURE-CODE-P21.md` (rejeu, corrections, constat supplémentaire `C-01`).

## 2. Dossier accordé

`~/Projets/squelette-chantier-p21/` et lui seul, mêmes règles qu'au tour précédent : tout ce qui existe est en lecture seule, `.git` compris (aucune commande Git qui y écrive ; `GIT_OPTIONAL_LOCKS=0` pour toute lecture) ; tes sous-dossiers existants de `revue-code/` sont lus, ni modifiés ni recréés.

Écritures permises, et seulement celles-ci :

- `revue-code/v2/` — nouveau sous-dossier pour ce tour : le clone (`git clone --no-local --branch claude/p21-tableau-des-cles ~/Projets/squelette-chantier-p21 revue-code/v2/clone`), les temporaires (`TMPDIR=~/Projets/squelette-chantier-p21/revue-code/v2/tmp`), les sondes rejouées et leurs fixtures, marquées « FIXTURE DE RELECTURE — FICTIF, N'AUTORISE RIEN » ;
- le livrable unique, à la racine : `RELECTURE_COURTE_CODE_P21.md`, en création exclusive. S'il existe déjà : verdict `CODE_P21_V2_OUTPUT_ALREADY_EXISTS`, rien d'écrit.

Aucun accès à un autre dossier, aucun envoi en ligne, aucune suppression hors de `revue-code/v2/`. Un script d'effacement produit par le contrôleur ne se lance que sur des copies d'essai de `revue-code/v2/`, après lecture.

## 3. Posture

`READ_ONLY` / `REPORT_ONLY`, comme au tour précédent. Les décisions du Project Owner et les écarts assumés restent des données.

## 4. Ce qu'il faut vérifier

- **V-01 à V-06 — fermeture.** Pour chacun de `R01` à `R06` : rejouer ta sonde, adaptée au clone `revue-code/v2/clone`, contre le code corrigé. Verdict par constat : `FERMÉ` | `PARTIEL` (avec le chemin qui reste ouvert) | `OUVERT`.
- **V-07 — le constat supplémentaire `C-01`** (programme de signature lancé par `git reflog show`) : fermé ?
- **V-08 — nouveaux trous.** Les corrections en ouvrent-elles ? À regarder en priorité : la règle d'origine de `R05` (original renommé, table de correspondance `PROJECT_CONTROL_PATH_MAP`) ; la détection des clones partiels de `R04` (faux refus sur un clone ordinaire ; versions de Git qui ignorent `GIT_NO_LAZY_FETCH`) ; le parcours de tout `.git` de `R06` (faux refus, durée) ; les lignes d'histoire de `R01` (un commit orphelin peut-il encore échapper ?) ; l'élément d'origine d'un export de `R02` (abandon, nouveau retour) ; l'empreinte de `R03`.
- **V-09 — suite complète** dans `revue-code/v2/clone`.

## 5. Standard et verdict

Même standard : sans scénario démontré, pas de redline. Verdict terminal, liste fermée : `CODE_P21_V2_PASS` · `CODE_P21_V2_REQUIRES_MINOR_REDLINE` · `CODE_P21_V2_REQUIRES_MAJOR_REDLINE` · `CODE_P21_V2_CANONICAL_CONFLICT` · `CODE_P21_V2_INPUT_MISSING` · `CODE_P21_V2_OUTPUT_ALREADY_EXISTS`.

## 6. Structure du livrable (court)

Résumé en trois points ; **A** preflight (commit relu, empreintes, versions de Python et de Git) ; **B** table `R01`–`R06` et `C-01` → `FERMÉ` / `PARTIEL` / `OUVERT`, avec la preuve ; **C** nouveaux constats (V-08) au format habituel ; **D** résultat de la suite complète ; **E** état du dossier en fin de mandat ; **F** verdict terminal.

## 7. Après la relecture

Tes livrables sont rangés tels quels dans l'atelier à la livraison, sous double arrêt séparé. `revue-code/` contient des copies d'essai munies de leurs fiches de sortie : le dossier de chantier refusera d'être rendu tant qu'elles sont là ; Jeoffrey efface `revue-code/` avant ce retour.

---

**Texte à coller dans la demande à Codex** (dossier de travail de Codex : `~/Projets/squelette-chantier-p21`, avec droit d'écriture) :

> Réalise la relecture courte décrite dans ~/Projets/squelette-chantier-p21/MANDAT-RELECTURE-COURTE-CODE-P21.md, en respectant exactement le dossier accordé, les interdits et la structure du livrable. Livrable unique : RELECTURE_COURTE_CODE_P21.md à la racine de ce dossier.
