> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Mandat de contrôle — constat N01 (P21, 3.21.0)

Contrôle de fermeture d'un seul constat, avant livraison. Suite de ta relecture courte `RELECTURE_COURTE_CODE_P21.md` (verdict `CODE_P21_V2_REQUIRES_MAJOR_REDLINE`), qui demandait de « faire rejouer son scénario et les tests avant livraison ». Mandat donné par Jeoffrey (Project Owner) ; rédigé par Claude, auteur de la correction — conflit d'intérêt déclaré. Style de retour : PLAIN (résumé en trois points en tête).

## 1. Objet

- Branche `claude/p21-tableau-des-cles` au commit `a186529a39ae4f6c6fdb60460915908b67afe82c` ; la correction est dans `git diff 2b4b64606c330b53a3729ee52e5fe11b1cfa33db..a186529a39ae4f6c6fdb60460915908b67afe82c` (commit `bf90c40`, puis la vue). Empreintes attendues : `scripts/project_control.py` `8f92767bdafb893387fc08525a425505421180ccef90756e6d9c7ce9748b2da9` ; `tests/test_template.py` `5347901af39752c699deddea1af0efedb1aa244042aae5ea415659dde1be74fe`.
- Pièce de référence : `CONTRE-REVUE-RELECTURE-COURTE-CODE-P21.md`.

## 2. Dossier accordé

`~/Projets/squelette-chantier-p21/`, mêmes règles qu'aux deux tours précédents. Écritures permises : `revue-code/v3/` (clone `git clone --no-local --branch claude/p21-tableau-des-cles ~/Projets/squelette-chantier-p21 revue-code/v3/clone`, temporaires `TMPDIR=…/revue-code/v3/tmp`, sondes) et le livrable unique `CONTROLE_N01_P21.md` à la racine, en création exclusive. Rien d'autre ; tes dossiers `revue-code/` existants sont lus, jamais modifiés.

## 3. Ce qu'il faut vérifier

- **K-01** — ton scénario `probe_fifo.py` (tube `copie.json` sous `.git/hooks/` et sous `.git/objects/…`), rejoué contre le code corrigé : refus rapide, processus terminé ? `FERMÉ` | `PARTIEL` | `OUVERT`.
- **K-02** — la correction ouvre-t-elle un trou ou un faux refus démontré (un tube à la place d'un fichier que Git ouvre ; une inclusion de configuration vers un tube ; la borne de cinq minutes) ?
- **K-03** — suite complète dans `revue-code/v3/clone`.

Standard habituel : sans scénario démontré, pas de redline.

## 4. Verdict

Liste fermée : `CODE_P21_N01_PASS` · `CODE_P21_N01_REQUIRES_MINOR_REDLINE` · `CODE_P21_N01_REQUIRES_MAJOR_REDLINE` · `CODE_P21_N01_INPUT_MISSING` · `CODE_P21_N01_OUTPUT_ALREADY_EXISTS`.

Livrable court : résumé en trois points ; preflight ; K-01 à K-03 ; état du dossier ; verdict.

---

**Texte à coller dans la demande à Codex** (dossier de travail : `~/Projets/squelette-chantier-p21`, avec droit d'écriture) :

> Réalise le contrôle décrit dans ~/Projets/squelette-chantier-p21/MANDAT-CONTROLE-N01-P21.md, en respectant exactement le dossier accordé, les interdits et la structure du livrable. Livrable unique : CONTROLE_N01_P21.md à la racine de ce dossier.
