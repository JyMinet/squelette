# Contre-revue de la seconde revue indépendante — squelette 3.13.0

*9 septembre 2026. Objet : les sept constats du rapport `REVUE_SQUELETTE_3.13.0.md`. Lecture seule sur le dépôt ; essais dans une copie jetable hors du dossier accordé.*

## Résumé en trois points

1. **Les sept constats se confirment**, et j'en ai trouvé un huitième en vérifiant le premier — plus grave que tout ce que la revue signale. Le garde-fou de commit annonce « audit PASS on the staged state » alors qu'il **contrôle l'arbre de travail, pas ce qui va être enregistré**. On peut donc indexer un record de gouvernance falsifié, remettre le fichier sain dans le dossier, et le garde-fou laisse passer.
2. **Quatre des sept constats sont de moi, et datent d'aujourd'hui.** Trois viennent de la livraison de la langue faite il y a quelques heures, un du lot B. Aucun n'est grave, mais ils disent quelque chose : une livraison rapide, même vérifiée par 119 essais, laisse passer ce qu'aucun essai ne regarde.
3. **Deux constats graves confirmés**, plus le nouveau. Ils touchent tous les deux la thèse centrale du projet : ce que le squelette accepte d'enregistrer comme preuve.

## 1. Verdicts, un par constat

| Constat | Objet, en clair | Vérification | Verdict | Sévérité retenue |
|---|---|---|---|---|
| **NOUVEAU** | Le garde-fou dit contrôler ce qui va être enregistré ; il contrôle le dossier. Un record falsifié indexé puis masqué entre dans l'historique | Rejoué : `WI-999` fantôme, marqué terminé, committé avec l'accord du garde-fou | **Confirmé** | **BLOCKER, configuration standard** |
| `F-01` | Un `.gitignore` large fait échouer la création d'un chantier et laisse l'index à moitié modifié, que le garde-fou accepte ensuite | Rejoué : cinq fichiers en `MM`, garde-fou PASS, commit accepté, roadmap citant un chantier dont la fiche est absente | **Confirmé** | **Majeur, standard** |
| `F-02` | Un commit antérieur à l'autorisation du chantier vaut preuve de développement | Rejoué : le commit **initial du dépôt** accepté, `DEVELOPED`, `DONE`, audit PASS ; le vrai commit du travail nulle part | **Confirmé** | **Majeur, standard** |
| `F-03` | Un dépôt non gouverné ne peut pas adopter le squelette si son code vit sous `modules/` | Établi par lecture : `NO_ACTIVE_BUSINESS_CAPABILITY` refuse tout code métier en mode bootstrap | **Confirmé** | Mineur — limite de couverture assumée, à dire dans la doc |
| `F-04` | En anglais, une sauvegarde à jour est marquée en alerte | Établi par lecture : le test porte sur le préfixe `identiques`/`The remote`, or le libellé anglais commence par `identical` | **Confirmé** | Mineur — **régression de ce jour (P14)** |
| `F-05` | La doctrine propose encore un réglage de langue devenu sans effet | Établi par lecture : `ROADMAP_VIEW.md` le liste, la vue suit Project State | **Confirmé** | Mineur — **omission de ce jour (P14)** |
| `F-06` | Une source ajoutée par le contrôleur reste en français dans la vue anglaise | Établi par lecture : `VERSION_TAGS_SOURCE` est une chaîne française codée en dur | **Confirmé** | Mineur — **omission du lot B** |
| `F-07` | Le README annonce un contrôleur uniquement francophone | Établi par lecture : la phrase est toujours là, et la démo la contredit | **Confirmé** | Mineur — **omission de ce jour (P14)** |

Aucune fausse alerte. Aucun constat de goût présenté comme un défaut.

## 2. Le constat nouveau, et pourquoi il est le plus grave

En vérifiant `F-01`, une phrase m'a arrêté dans la sortie du garde-fou :

```
PASS: MODE_AUDIT — audit PASS on the staged state
```

« on the staged state » — sur l'état indexé. Or `commit_gate_findings` appelle `audit_findings()`, qui lit les fichiers **sur le disque**. Seules trois vérifications consultent réellement l'index : la liste des chemins indexés, les liens symboliques (corrigé au lot A) et le périmètre du chantier (corrigé en 3.9.1). Tout le reste — la validité des records, la cohérence roadmap/fiches, les preuves — juge l'arbre de travail.

**Le cas, rejoué dans une copie neuve, garde-fou installé, sans override :**

1. On modifie `roadmap-state.v1.json` pour y ajouter un chantier `WI-999` marqué terminé, qui n'existe pas.
2. On l'indexe (`git add`).
3. On remet le fichier sain dans le dossier de travail.

```
index  : contient WI-999 ? oui
arbre  : contient WI-999 ? non
garde-fou               : PASS
    PASS: MODE_AUDIT — audit PASS on the staged state
commit                  : ACCEPTÉ
dans l'historique       : WI-999 présent
```

Un chantier fantôme, déclaré terminé, entre dans l'historique **avec l'accord du garde-fou**, dont le message affirme avoir contrôlé exactement ce qui vient d'être enregistré.

`F-01` en est un cas particulier accidentel : le contrôleur lui-même fabrique l'écart entre index et arbre, puis son propre garde-fou le bénit.

**Correction proposée** : le garde-fou doit auditer l'arbre que le commit va créer. La façon propre est de matérialiser l'index dans un répertoire temporaire (`git checkout-index` ou `git stash create` sur l'index) et d'auditer là ; à défaut, comparer index et arbre de travail sur les chemins administratifs et refuser toute divergence. Et, dans tous les cas, **cesser d'écrire « on the staged state »** tant que ce n'est pas vrai — c'est exactement la faute que le lot B a corrigée ailleurs.

## 3. Les deux constats graves de la revue

### `F-02` — n'importe quel vieux commit vaut preuve de développement

Rejoué : un chantier autorisé, démarré, dont le vrai travail est committé sur sa branche puis intégré. À la clôture, on donne le **commit initial du dépôt** — antérieur de tout l'historique à l'autorisation :

```
close --commit <commit initial>  : ACCEPTÉ
statut                    : DONE
development_status        : DEVELOPED
commits enregistrés       : ["c225841523df…"]   ← le commit initial
audit                     : PASS
```

Le commit qui contient réellement le travail n'apparaît nulle part. Le contrôleur vérifie deux choses — le commit existe, et il est ancêtre de HEAD — et rien d'autre. Il refuse bien un commit **non intégré** ; il ne vérifie pas que le commit accepté a quoi que ce soit à voir avec le chantier.

**Correction proposée** : exiger que le commit cité soit postérieur au `start_head` du chantier et touche au moins un chemin de ses `authorized_paths`. Ce n'est pas juger le code, c'est vérifier le lien.

### `F-01` — la transaction de création laisse l'index à moitié fait

Rejoué : avec `*.json` dans le `.gitignore` — cas banal —, `create-work-item` échoue à indexer ses nouveaux records, restaure les fichiers, mais **pas l'index**. Cinq fichiers restent indexés avec leur nouveau contenu. Le commit qui suit enregistre une roadmap citant `WI-001` dont la fiche n'existe pas.

**Correction proposée** : restaurer l'index comme les fichiers en cas d'échec d'indexation, et anticiper les chemins administratifs ignorés (les indexer avec `-f`, ou refuser d'emblée en nommant le motif d'ignore).

## 4. Les quatre mineurs, et ce qu'ils disent de moi

`F-04`, `F-05`, `F-07` viennent de la livraison de la langue de cet après-midi. `F-06` vient du lot B de ce matin. Tous sont vrais, aucun n'est grave, tous auraient été évités par une relecture que je n'ai pas faite.

`F-04` mérite un mot : j'avais déjà calculé le bon booléen (`self._backups_ok`) deux lignes plus haut, et j'ai quand même écrit un test sur le préfixe du texte. C'est précisément le genre de raccourci que le lot B condamnait.

**Corrections** : utiliser le booléen existant ; retirer `language` de la liste des réglages de la vue dans la doctrine ; traduire le libellé de la source virtuelle en gardant sa clé d'empreinte ; réécrire la phrase du README sur la langue.

## 5. Ce que la revue a bien fait, et ses limites

Elle est honnête sur ce qu'elle n'a pas prouvé : le chiffre de « 15 commandes en 3,2 secondes » est explicitement présenté comme non représentatif d'une adoption humaine ; la matrice des 70 promesses distingue « tenue (essai) », « tenue (lecture) » et « non vérifiée — doctrine » au lieu de tout compter comme vérifié ; et elle dit ce qui tient, ce que j'avais demandé et que la première revue n'avait pas fait.

Sa limite : elle n'a pas cherché l'écart index/arbre, alors que sa propre reproduction de `F-01` le montrait. Elle a vu le symptôme sans remonter à la cause.

## 6. Ce que je propose

Un seul lot, **3.14.0**, parce que les trois défauts sérieux touchent la même chose — ce que le squelette accepte comme preuve — et qu'il serait malsain d'en laisser un ouvert :

1. Le garde-fou audite l'arbre que le commit va créer, ou dit la vérité sur ce qu'il contrôle.
2. La création restaure l'index comme les fichiers, et gère les chemins ignorés.
3. La clôture exige un commit relié au chantier : postérieur à son démarrage, touchant son périmètre.
4. Les quatre mineurs, dans la foulée.
5. `F-03` : dire dans `ADOPTION.md` et le README ce que le squelette couvre — un projet déjà gouverné par une V3 antérieure — et ce qu'il ne couvre pas encore.

Chaque point suit le chemin habituel : cas reproductible avant correction, essai rouge avant / vert après, double arrêt, branche, promotion sur ta décision.
