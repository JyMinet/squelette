> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Mandat de contrôle — constat N03 (P21, 3.21.0)

Contrôle de fermeture d'un seul constat mineur, avant livraison. Suite de ton contrôle `CONTROLE_N02_P21.md` (verdict `CODE_P21_N02_REQUIRES_MINOR_REDLINE`). Mandat donné par Jeoffrey (Project Owner) ; rédigé par Claude, auteur de la correction — conflit d'intérêt déclaré. Style de retour : PLAIN (résumé en trois points en tête).

## 1. Objet

- Branche `claude/p21-tableau-des-cles` au commit `5d607510a3257e1159ee7ce50cdc682954e52ec6` ; la correction est dans `git diff 8ff30f85427e27a53e42e7688bc061b7305afe93..5d607510a3257e1159ee7ce50cdc682954e52ec6` (commit `81f21df`, puis la vue). Empreintes attendues : `scripts/project_control.py` `9ab8e90fafb336a74499070a766c4b98293feb4be570a1a1808dff1666f9ab9f` ; `tests/test_template.py` `0c0410f3c8bc3d83c50982a1c186ade8e61e94ddf3e4a8dd63b8ad813fdfd06e`.
- Pièce de référence : `CONTRE-REVUE-CONTROLE-N02-P21.md`.

## 2. Dossier accordé

`~/Projets/squelette-chantier-p21/`, mêmes règles qu'aux tours précédents. Écritures permises : `revue-code/v5/` (clone `git clone --no-local --branch claude/p21-tableau-des-cles ~/Projets/squelette-chantier-p21 revue-code/v5/clone`, temporaires `TMPDIR=…/revue-code/v5/tmp`, sondes) et le livrable unique `CONTROLE_N03_P21.md` à la racine, en création exclusive. Rien d'autre ; tes dossiers `revue-code/` existants sont lus, jamais modifiés. Toute lecture Git du dossier de chantier se fait avec `GIT_OPTIONAL_LOCKS=0`, dès la première.

## 3. Ce qu'il faut vérifier

- **K-01** — ton scénario `probe_source_guard.py` rejoué contre le code corrigé : l'original nommé `source` ouvre-t-il sa deuxième copie malgré la liste voisine ? `FERMÉ` | `PARTIEL` | `OUVERT`.
- **K-02** — une vraie fiche d'export à cet endroit, normale, agrandie ou abîmée, fait-elle toujours refuser ? La correction ouvre-t-elle un trou démontré ?
- **K-03** — suite complète dans `revue-code/v5/clone`.

Standard habituel : sans scénario démontré, pas de redline.

## 4. Verdict

Liste fermée : `CODE_P21_N03_PASS` · `CODE_P21_N03_REQUIRES_MINOR_REDLINE` · `CODE_P21_N03_REQUIRES_MAJOR_REDLINE` · `CODE_P21_N03_INPUT_MISSING` · `CODE_P21_N03_OUTPUT_ALREADY_EXISTS`.

Livrable court : résumé en trois points ; preflight ; K-01 à K-03 ; état du dossier ; verdict.

---

**Texte à coller dans la demande à Codex** (dossier de travail : `~/Projets/squelette-chantier-p21`, avec droit d'écriture) :

> Réalise le contrôle décrit dans ~/Projets/squelette-chantier-p21/MANDAT-CONTROLE-N03-P21.md, en respectant exactement le dossier accordé, les interdits et la structure du livrable. Livrable unique : CONTROLE_N03_P21.md à la racine de ce dossier.
