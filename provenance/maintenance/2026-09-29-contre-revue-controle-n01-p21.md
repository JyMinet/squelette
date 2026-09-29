# Contre-revue — Contrôle N01 (P21)

Date : 2026-09-29, 06:57–08:10 (Europe/Zurich). Auteur : Claude, auteur du code — conflit d'intérêt déclaré, d'où la vérification par rejeu. Objet : `CONTROLE_N01_P21.md` (Codex, 11 157 octets, rendu le 29 septembre à 06:33), verdict `CODE_P21_N01_REQUIRES_MAJOR_REDLINE`, sur le commit `a186529a39ae4f6c6fdb60460915908b67afe82c`.

## Résumé en trois points

1. **Ce qui s'est passé.** Codex a trouvé le tube fermé, partout où il l'a posé. Il a trouvé un défaut nouveau, né de ma correction : une fiche de sortie authentique, simplement agrandie d'espaces au-delà de 64 Kio, n'était plus lue — et la copie qu'elle désigne, cachée dans le dossier interne de Git, passait le contrôle d'avant l'effacement. Rejoué : confirmé.
2. **Ce que ça change.** La règle est retournée : tout fichier qui porte le nom d'une fiche est refusé, sauf s'il est clairement autre chose. Trop grand, illisible, écrit dans un autre encodage, abîmé, ou ressemblant à une fiche : refusé. Aucun fichier de ce nom n'a sa place dans le dossier interne de Git. Les 219 essais passent, dans la copie de travail de la session et sur le Mac.
3. **Ce qu'il doit faire.** Faire rejouer par Codex ce dernier scénario (mandat très court `MANDAT-CONTROLE-N02-P21.md`) — ou passer à la livraison.

Verdict : `CODE_P21_N01_REVIEW_OF_CONTROLE_N01_PASS`

## A — Rejeu

| Constat | Essai | Sur `a186529` | Après correction | Verdict |
|---|---|---|---|---|
| `N01` — tube `copie.json` | `test_a_pipe_named_like_an_exit_slip_is_never_opened` | vert (fermé au tour précédent) | vert | FERMÉ, comme Codex le constate |
| `N02` MAJOR — fiche agrandie au-delà de 64 Kio | `test_a_padded_or_damaged_exit_slip_hides_no_copy` | rouge : la fiche de 65 537 octets n'est pas vue | vert : refus, dans l'arbre de travail comme dans `.git/objects/` | CONFIRMÉ |

Le reste du contrôle de Codex est reçu tel quel : les tubes à la place de `HEAD`, de `config`, de l'index, d'une référence ou de la fiche sont refusés en moins d'une seconde ; l'inclusion vers un tube est refusée au bout de la borne de cinq minutes, par appel à Git ; aucun faux refus sur les copies ordinaires essayées ; 218 essais sur 218.

Sur son écart de procédure déclaré (un premier `git status` sans `GIT_OPTIONAL_LOCKS=0` dans le dossier de chantier) : sans conséquence. Le verrou vide `.git/index.lock`, laissé là depuis le 28 septembre, empêchait justement toute réécriture de l'index ; et l'index ne porte rien qui ne soit ailleurs.

## B — Correction (commit `735882e`)

`nested_slip_refusal` ne cherche plus à reconnaître une fiche valide pour refuser : elle refuse tout fichier nommé `copie.json` qui n'est pas clairement autre chose. Un tel fichier est lu seulement s'il est ordinaire et d'au plus 64 Kio ; alors :

- du JSON en UTF-8 (marque d'octets admise) dont l'objet ne porte ni `copy_id` ni `token` — une donnée du projet — ou qui n'est pas un objet : pas une fiche ;
- un objet qui porte `copy_id`, `token` et `original` : une autre copie enregistrée, refusée comme avant ;
- tout le reste — trop grand pour être lu, illisible, pas du JSON en UTF-8 (un autre encodage, une fiche abîmée), ou un objet qui ressemble à une fiche sans se lire comme une fiche enregistrée : refusé.

Dans `.git`, aucun fichier de ce nom n'a sa place, sous la fiche de la copie elle-même : il est refusé quoi qu'il contienne. `read_copy_slip`, qui sert à l'identité et à la bannière, garde sa réponse « pas de fiche » : elle y est sûre, puisqu'une identité illisible est refusée. Écrit comme limite : une fiche se reconnaît à son nom et à sa place ; renommée ou déplacée, elle n'est plus une fiche, et la copie qu'elle désignait ne peut plus être ni rendue ni effacée par son propre original.

L'essai couvre 65 536 et 65 537 octets, une fiche abîmée, précédée d'une marque d'octets, écrite en UTF-16, privée de son original ; un objet du projet et une liste ne sont pas des fiches ; une copie imbriquée dans l'arbre de travail à fiche agrandie fait refuser le retour, même abandonnée en bloc ; dans `.git/objects/`, elle fait refuser le contrôle d'avant l'effacement, et un `copie.json` vide aussi.

## C — Essais et contrôles

| Lieu | Python | Git | Résultat |
|---|---|---|---|
| Mac, espace de travail de Claude, clone du dossier de chantier | 3.10.12 | 2.34.1 | 219 essais OK ; `audit`, `bootstrap-audit`, `core-manifest` PASS ; démo et vue à jour |
| Copie de travail de la session, clone propre de la branche | 3.11.15 | 2.43.0 | 219 essais OK (609 s) |

Export public sans erreur et sans registre. Inventaire réel du dossier de chantier, en lecture seule : aucun refus hors de `revue-code/` ; 56 éléments hors de ce dossier (la branche, `main`, les 37 tags, les papiers de la racine et les fichiers de transfert).

## D — État

Branche `claude/p21-tableau-des-cles` à `8ff30f8` (`735882e` la correction, `8ff30f8` la vue) ; transfert `transfert/p21-branche-6.bundle` (6 936 octets, SHA-256 `7251e10c94984227cb9d1ed4caa259fca18da71ce9230fac12d54ad9fec7070e`), vérifié puis récupéré. `main` à `b9fe0e7`, inchangé. Empreintes au commit `8ff30f8` : `scripts/project_control.py` `18d81d57abd1f65f6204bcefdc0cc702b351bf0df64364a373e2821bd5c85744`, `tests/test_template.py` `f599236fde1353ca574ef5b6546a542d2c861c78c2e838019c872ad4f6c53def`.
