> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Mandat de contrôle — constat N02 (P21, 3.21.0)

Contrôle de fermeture d'un seul constat, avant livraison. Suite de ton contrôle `CONTROLE_N01_P21.md` (verdict `CODE_P21_N01_REQUIRES_MAJOR_REDLINE`), qui demandait de « corriger N02 et rejouer les contrôles avant livraison ». Mandat donné par Jeoffrey (Project Owner) ; rédigé par Claude, auteur de la correction — conflit d'intérêt déclaré. Style de retour : PLAIN (résumé en trois points en tête).

## 1. Objet

- Branche `claude/p21-tableau-des-cles` au commit `8ff30f85427e27a53e42e7688bc061b7305afe93` ; la correction est dans `git diff a186529a39ae4f6c6fdb60460915908b67afe82c..8ff30f85427e27a53e42e7688bc061b7305afe93` (commit `735882e`, puis la vue). Empreintes attendues : `scripts/project_control.py` `18d81d57abd1f65f6204bcefdc0cc702b351bf0df64364a373e2821bd5c85744` ; `tests/test_template.py` `f599236fde1353ca574ef5b6546a542d2c861c78c2e838019c872ad4f6c53def`.
- Pièce de référence : `CONTRE-REVUE-CONTROLE-N01-P21.md` (la règle retournée : tout fichier nommé `copie.json` est refusé, sauf s'il est clairement autre chose).

## 2. Dossier accordé

`~/Projets/squelette-chantier-p21/`, mêmes règles qu'aux tours précédents. Écritures permises : `revue-code/v4/` (clone `git clone --no-local --branch claude/p21-tableau-des-cles ~/Projets/squelette-chantier-p21 revue-code/v4/clone`, temporaires `TMPDIR=…/revue-code/v4/tmp`, sondes) et le livrable unique `CONTROLE_N02_P21.md` à la racine, en création exclusive. Rien d'autre ; tes dossiers `revue-code/` existants sont lus, jamais modifiés. Toute lecture Git du dossier de chantier se fait avec `GIT_OPTIONAL_LOCKS=0`, dès la première.

## 3. Ce qu'il faut vérifier

- **K-01** — ton scénario `probe_large_slip.py` (copie EXPORT réellement enregistrée par un second original, fiche agrandie à 65 537 octets, travail unique), rejoué contre le code corrigé : le contrôle d'avant l'effacement refuse-t-il ? `FERMÉ` | `PARTIEL` | `OUVERT`.
- **K-02** — la règle retournée ouvre-t-elle un trou, ou un faux refus démontré sur une copie ordinaire (un `copie.json` du projet ; la fiche de la copie elle-même) ?
- **K-03** — suite complète dans `revue-code/v4/clone`.

Standard habituel : sans scénario démontré, pas de redline.

## 4. Verdict

Liste fermée : `CODE_P21_N02_PASS` · `CODE_P21_N02_REQUIRES_MINOR_REDLINE` · `CODE_P21_N02_REQUIRES_MAJOR_REDLINE` · `CODE_P21_N02_INPUT_MISSING` · `CODE_P21_N02_OUTPUT_ALREADY_EXISTS`.

Livrable court : résumé en trois points ; preflight ; K-01 à K-03 ; état du dossier ; verdict.

---

**Texte à coller dans la demande à Codex** (dossier de travail : `~/Projets/squelette-chantier-p21`, avec droit d'écriture) :

> Réalise le contrôle décrit dans ~/Projets/squelette-chantier-p21/MANDAT-CONTROLE-N02-P21.md, en respectant exactement le dossier accordé, les interdits et la structure du livrable. Livrable unique : CONTROLE_N02_P21.md à la racine de ce dossier.
