# Contre-revue — Relecture courte du code P21

Date : 2026-09-28, 22:17–23:10 (Europe/Zurich). Auteur : Claude, auteur du code — conflit d'intérêt déclaré, d'où la vérification par rejeu. Objet : `RELECTURE_COURTE_CODE_P21.md` (Codex, 12 449 octets), verdict `CODE_P21_V2_REQUIRES_MAJOR_REDLINE`, sur le commit `2b4b64606c330b53a3729ee52e5fe11b1cfa33db`.

## Résumé en trois points

1. **Ce qui s'est passé.** Codex a trouvé fermés les six défauts de sa première relecture et le septième ; il a trouvé un défaut nouveau, que ma correction du sixième avait introduit : un tube nommé comme une fiche de sortie (`copie.json`), caché dans le dossier interne de Git d'une copie, faisait attendre le contrôle indéfiniment. Rejoué : confirmé. En le fermant, j'ai fermé aussi ses cousins : le même tube à la place d'un fichier que Git ouvre lui-même, ou au bout d'une inclusion de configuration.
2. **Ce que ça change.** Une fiche n'est plus lue que si c'est un petit fichier ordinaire ; tout le dossier interne de Git d'une copie est vérifié avant que Git n'y soit lancé ; et aucune lecture par Git n'attend plus de cinq minutes. Les 218 essais passent, dans la copie de travail de la session et sur le Mac.
3. **Ce qu'il doit faire.** Faire rejouer par Codex son scénario du tube (mandat très court `MANDAT-CONTROLE-N01-P21.md`) — ou, s'il le juge inutile, passer à la livraison.

Verdict : `CODE_P21_V2_REVIEW_OF_RELECTURE_COURTE_CODE_PASS`

## A — Rejeu

| Constat | Essai | Sur `2b4b646` | Après correction | Verdict |
|---|---|---|---|---|
| `N01` MAJOR — tube `copie.json` dans `.git/hooks/` ou `.git/objects/…` | `test_a_pipe_named_like_an_exit_slip_is_never_opened` | rouge : le contrôle attend jusqu'à l'arrêt forcé (60 s) | vert : refus immédiat, « a special file (pipe, socket or device) » | CONFIRMÉ |

Les contrôles ciblés de Codex sans constat (lignes d'histoire de `R01`, retours d'export de `R02`, original renommé et table de correspondance, clones ordinaires et repli sans `GIT_NO_LAZY_FETCH`, durée du parcours) sont reçus tels quels.

## B — Correction (commit `bf90c40`)

- `read_copy_slip` n'ouvre qu'un fichier ordinaire d'au plus 64 Kio : type vérifié par `lstat` avant l'ouverture et par `fstat` après (ouverture non bloquante, jamais à travers un lien) ; tout autre cas vaut « pas de fiche ». Tout fichier d'une copie que le contrôleur lit passe par la même porte (`open_regular_file`).
- Le parcours de `.git` type chaque entrée d'après la liste du dossier, sans l'ouvrir ; un fichier spécial, à n'importe quel niveau, refuse la copie ; et ce parcours a lieu **avant** toute commande Git dans la copie : un tube à la place de `HEAD`, de `config`, de l'index ou d'une référence n'est jamais tendu à Git, qui l'ouvrirait et attendrait. Essai : même test, cas `.git/HEAD`.
- Pour ce que le contrôleur ne voit pas d'avance — une inclusion de configuration qui pointe hors de la copie vers un tube, un volume qui disparaît — chaque lecture d'une copie par Git est bornée à cinq minutes ; au-delà, la copie est refusée. Essai : même test, cas de l'inclusion, avec une borne abaissée à deux secondes.

## C — Essais et contrôles

| Lieu | Python | Git | Résultat |
|---|---|---|---|
| Mac, espace de travail de Claude, clone du dossier de chantier | 3.10.12 | 2.34.1 | 218 essais OK ; `audit`, `bootstrap-audit`, `core-manifest` PASS ; démo et vue à jour |
| Copie de travail de la session, clone propre de la branche | 3.11.15 | 2.43.0 | 218 essais OK (758 s) ; export public sans erreur et sans registre |

Inventaire réel du dossier de chantier, en lecture seule : parcours de son `.git` sans refus (0,1 s) ; hors de `revue-code/`, seulement la branche, `main` et les papiers de la racine. Les vingt refus de l'inventaire viennent tous des copies d'essai de Codex dans `revue-code/`, qui s'effacera avant le retour du dossier de chantier.

## D — État

Branche `claude/p21-tableau-des-cles` à `a186529` (`bf90c40` la correction, `a186529` la vue) ; transfert `transfert/p21-branche-5.bundle` (8 187 octets, SHA-256 `15132593157f832481bb52a951f7ea56f4f9ae6e2e0398b2bb59f86b6f26429d`), vérifié puis récupéré. `main` à `b9fe0e7`, inchangé. Empreintes au commit `a186529` : `scripts/project_control.py` `8f92767bdafb893387fc08525a425505421180ccef90756e6d9c7ce9748b2da9`, `tests/test_template.py` `5347901af39752c699deddea1af0efedb1aa244042aae5ea415659dde1be74fe`.
