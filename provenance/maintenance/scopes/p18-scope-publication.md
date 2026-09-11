> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# P18 — Publication : le squelette sait se publier

*Fiche de cadrage. 11 septembre 2026. Ouverte par le Project Owner (« On pourrait ouvrir le git au public ? »), autorisée le jour même.*

## 1. Ce qui est en cause

Le dépôt privé du squelette porte, dans sa couche de provenance, des choses qui n'ont rien à
faire en public : l'adresse e-mail du Project Owner (sur chaque commit, et dans une fiche), les
chemins de sa machine (`~/…`, seize fichiers), le nom de son projet privé adopté avec
son histoire (huit fichiers, quelques centaines de mentions), le chemin de son dépôt de sauvegarde.
Rien de secret — l'historique a été vérifié, les seules occurrences de « secret » ou « password »
sont dans le code du contrôleur qui les refuse — mais du personnel.

Le code et les documents du template sont déjà propres : tout ce qu'il y a à nettoyer est dans
`provenance/` (journal, rapports de contrôle, fiches de cadrage, tableau de bord).

## 2. Le choix : un dépôt public neuf, produit par un script

Ouvrir le dépôt privé tel quel exposerait l'adresse sur cent vingt commits, qu'on ne réécrit pas.
Nettoyer à la main une copie créerait un second squelette qui diverge dès la version suivante.

La publication est donc **une transformation répétable** : `provenance/maintenance/publication/export_public.py`
exporte l'arbre suivi à un tag donné (`git archive`), applique une table de remplacements lisible
en tête du fichier, renomme les fichiers dont le nom porte l'acronyme, ajoute une ligne en tête de
chaque rapport ou fiche modifié pour dire qu'il s'agit d'une copie anonymisée, et **refuse de
finir s'il reste un seul mot interdit** — dans un contenu ou dans un nom de fichier. Le dépôt
privé reste le seul endroit où l'on travaille ; publier une version, c'est relancer le script sur
le tag et pousser le résultat. Le script vit hors du core et ne part pas dans les projets dérivés.

## 3. La règle de nettoyage

| Ce qui sort | Ce qui le remplace |
|---|---|
| l'adresse e-mail | `<adresse retirée>` |
| `~/…` | `~/…` |
| le nom du projet adopté, sous toutes ses formes (nom complet, abréviation, nom de dossier) | **Alpha** — un nom de code, pour que les phrases restent lisibles ; élision française rétablie (« d'Alpha », « qu'Alpha ») |
| le chemin du dépôt de sauvegarde | `SAUVEGARDE` |

**Ce qui reste.** Le prénom du Project Owner : la licence MIT le porte et doit le porter, une
décision a un auteur, et un prénom n'est pas un identifiant. Le journal, les fiches et les quatre
rapports de contrôle indépendant : anonymisés, jamais supprimés — ils sont ce que ce squelette a
de plus rare. Le code, à l'octet : un fichier core que le script devrait modifier fait échouer
l'export ; le core est publié tel quel ou pas du tout.

## 4. Le numéro de la première version publique

Le numéro de version n'est pas une étiquette : `template-upgrade` le compare et refuse de monter
vers un numéro plus petit. Un template public en `1.0.0` serait vu comme plus ancien que la `3.18`
par tout projet dérivé. **La première version publique sera la 4.0.0** — un seul numéro, qui dit
« première version publique » et « quatrième génération », et qui reste montable depuis tout ce
qui existe.

## 5. Ce que ce chantier ne fait pas

- Il ne publie rien : aucun export hors du dossier temporaire de l'essai, aucun dépôt public créé.
  Le premier export réel se fera après la cinquième passe de contrôle et un temps de
  stabilisation, sous son propre double arrêt, vers un dossier local et un dépôt GitHub que le
  Project Owner nommera ; le rendu public est son geste.
- Il ne réécrit pas l'historique du dépôt privé.
- Il ne traduit rien : la langue des documents publics (P14, étape 2) est une décision à part.

## 6. Questions ouvertes

1. Le nom du dépôt public sur GitHub, et le dossier local de l'export.
2. Faut-il que le dépôt public garde l'historique des versions à partir de la 4.0.0 (un commit par
   version publiée) ou reparte à chaque publication ? Proposition : un commit par version
   publiée, taguée, pour que les projets dérivés du dépôt public puissent monter.
3. L'anglais pour le README public (P14, étape 2).

## 7. État

`DONE` pour l'outil, `TO_SCOPE` pour la publication elle-même. Livré en `3.19.0` (`TPL-D-063`) :
le script, son essai (rouge sur la `3.18.2`, où le script n'existe pas ; vert ici : aucun mot
interdit dans l'export de `HEAD`, contenus et noms de fichiers compris, 24 fichiers core
identiques à l'octet à ceux de la révision, ligne d'anonymisation en tête des rapports, licence
intacte, prose relue), et cette fiche.
