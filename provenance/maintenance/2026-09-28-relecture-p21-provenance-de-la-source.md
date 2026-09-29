> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Provenance de `source/` — relecture « Tableau des clés » V1

Monté le 2026-09-28 à 17:07 (Europe/Zurich) par Claude, sur le double arrêt de Jeoffrey :
« Confirmé : monter le dossier de relecture dans ~/Projets/squelette-revue-tableau-des-cles, atelier lu seulement, rien d'effacé, pas d'envoi. »

## Ce que contient `source/`

- Export de l'atelier privé `~/Projets/squelette-atelier` au tag `v3.20.2`, par `git archive --format=tar v3.20.2` (jamais le checkout vivant), sans `.git`, sans remote, sans historique.
- Tag `v3.20.2` → commit `9b8792e1ef453869105bd0edc2cc085120bbf404` ; arbre `fb1390aa83d1c4472d7e742afc62a79580d4d38e`.
- 138 fichiers exportés, 138 attendus (`git ls-tree -r v3.20.2`). `provenance/core-manifest.v1.json` annonce la version 3.20.2.
- Empreintes SHA-256 de chaque fichier dans `SOURCE-MANIFESTE.sha256` (138 lignes) ; vérification : `cd source && sha256sum -c ../SOURCE-MANIFESTE.sha256`.
- Empreinte du manifeste lui-même : `a0c1ea0d49c0741e23b427d427630569b2478e8a8ed250cc8d971dbd5891f102`.

## Les deux papiers de la relecture (versions corrigées, remplacent les premières)

| Fichier | Octets | SHA-256 |
|---|---:|---|
| `FICHE-CADRAGE-TABLEAU-DES-CLES-V1.md` | 23252 | `d1b3df340e21c0e7dee80ee170f4cbb131e2f4041092717c1db9d6556d111e50` |
| `MANDAT-RELECTURE-TABLEAU-DES-CLES-V1.md` | 5770 | `76c9fa90aafac2d0c87873152aaae66976aa4fbbd9a37a44b6f4e66c0c4e277c` |

Ce sont, à l'octet près, les fichiers que le premier constat de relecture a relevés sous le suffixe `V1_1` dans `Downloads` (section A.3 de ce constat). La paire retenue est celle-ci.

## Ce qui n'a pas été fait

- Atelier lu seulement : aucune écriture, aucune branche, aucun commit, aucun tag (main resté à `b9fe0e7`, arbre propre).
- Rien effacé nulle part ; aucun envoi en ligne.
- Le constat `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V1.md` (12135 octets, `da5c28e91decba6598b13578c92c51bac92c5635748945f14bc3ca29ceccf11f`) est resté tel quel : la reprise s'écrit comme une révision liée (V2), jamais par-dessus.
- `runs/` est vide : clones et copies jetables de la relecture y vivent et partent avec le dossier.
