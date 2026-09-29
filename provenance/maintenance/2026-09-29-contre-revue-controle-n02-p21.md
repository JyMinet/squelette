# Contre-revue — Contrôle N02 (P21)

Date : 2026-09-29, 08:24–09:00 (Europe/Zurich). Auteur : Claude, auteur du code — conflit d'intérêt déclaré, d'où la vérification par rejeu. Objet : `CONTROLE_N02_P21.md` (Codex, 9 407 octets), verdict `CODE_P21_N02_REQUIRES_MINOR_REDLINE`, sur le commit `8ff30f85427e27a53e42e7688bc061b7305afe93`.

## Résumé en trois points

1. **Ce qui s'est passé.** Codex a trouvé la fiche agrandie bien refusée, et les données ordinaires nommées `copie.json` bien acceptées. Il a trouvé un faux refus mineur, né de ma correction : un original qui s'appelle `source`, dont le dossier voisin contient un `copie.json` qui n'est qu'une simple liste, était pris pour une copie et ne pouvait plus ouvrir de copie. Rejoué : confirmé.
2. **Ce que ça change.** Une seule règle sert désormais partout pour dire si un fichier de ce nom peut être une fiche ; une simple liste ou un JSON étranger à une fiche ne fait plus d'un original une copie ; une vraie fiche, agrandie ou abîmée, si. Les 220 essais passent, dans la copie de travail de la session et sur le Mac.
3. **Ce qu'il doit faire.** Décider : un dernier contrôle court par Codex (mandat `MANDAT-CONTROLE-N03-P21.md`), ou la livraison. Le défaut était mineur — un refus de trop, jamais une autorisation de trop —, et sa correction ne fait que réutiliser la règle déjà contrôlée.

Verdict : `CODE_P21_N02_REVIEW_OF_CONTROLE_N02_PASS`

## A — Rejeu

| Constat | Essai | Sur `8ff30f8` | Après correction | Verdict |
|---|---|---|---|---|
| `N02` — fiche agrandie | `test_a_padded_or_damaged_exit_slip_hides_no_copy` | vert (fermé au tour précédent) | vert | FERMÉ, comme Codex le constate |
| `N03` MINOR — original nommé `source` et liste voisine | `test_an_original_named_source_is_not_taken_for_an_export_by_a_neighbour_file` | rouge : « this repository is a copy » à cause de `[1, 2, 3]` | vert ; une vraie fiche, agrandie ou abîmée, fait toujours refuser | CONFIRMÉ |

Le reste du contrôle est reçu tel quel : copies ordinaires, CLONE et EXPORT, rendues et contrôlées avec des données de projet nommées `copie.json` ; fiche de chaque copie acceptée à sa place jusqu'à 65 536 octets et refusée au-delà ; 219 essais sur 219.

## B — Correction (commit `81f21df`)

La décision « ce fichier peut-il être une fiche ? » est sortie dans une seule fonction, `slip_file_concern`, qui sert l'inventaire (`nested_slip_refusal`) et le garde qui reconnaît le `source/` d'un export (`copy_guard_errors`). Un fichier `copie.json` voisin d'un dépôt nommé `source` n'en fait une copie que s'il peut être une fiche : fiche enregistrée, trop grand pour être lu, illisible, pas du JSON en UTF-8, ou objet qui ressemble à une fiche. Une liste, une chaîne, un objet sans `copy_id` ni `token` : l'original reste un original. La fiche d'une copie dans son `.git`, elle, continue de faire une copie quoi qu'elle contienne.

Ce que la correction ne rouvre pas : un export porte toujours une vraie fiche à la racine de son contenant, qui garde son `source/` ; et une écriture du registre depuis un dépôt qui n'est pas l'original reste refusée par la règle d'origine (`R05`).

## C — Essais et contrôles

| Lieu | Python | Git | Résultat |
|---|---|---|---|
| Mac, espace de travail de Claude, clone du dossier de chantier | 3.10.12 | 2.34.1 | 220 essais OK ; `audit`, `bootstrap-audit`, `core-manifest` PASS ; démo et vue à jour |
| Copie de travail de la session, clone propre de la branche | 3.11.15 | 2.43.0 | 220 essais OK (618 s) |

Export public sans erreur et sans registre.

## D — État

Branche `claude/p21-tableau-des-cles` à `5d60751` (`81f21df` la correction, `5d60751` la vue) ; transfert `transfert/p21-branche-7.bundle` (5 022 octets, SHA-256 `38c98cf1fc794dcc7c69daf37ef88a8ffd873599f84c29332b35ebfe55106589`), vérifié puis récupéré. `main` à `b9fe0e7`, inchangé. Empreintes au commit `5d60751` : `scripts/project_control.py` `9ab8e90fafb336a74499070a766c4b98293feb4be570a1a1808dff1666f9ab9f`, `tests/test_template.py` `0c0410f3c8bc3d83c50982a1c186ade8e61e94ddf3e4a8dd63b8ad813fdfd06e`.
