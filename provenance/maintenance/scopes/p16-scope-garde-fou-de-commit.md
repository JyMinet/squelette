> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# P16 — Le garde-fou de commit

*Fiche de cadrage. 10 septembre 2026. Ouverte par la seconde passe de contrôle indépendant, pas encore autorisée.*

## 1. D'où vient ce chantier

La seconde passe de contrôle de la `3.15.3` a démontré, contre-exemples exécutés à l'appui, **trois
façons de faire entrer dans l'historique un commit que l'audit aurait refusé**. Aucune n'est née
avec la série 3.14–3.16 : elles sont là depuis que le garde-fou existe sous cette forme, et
personne n'était encore allé les chercher.

Ce n'est pas un détail de confort. Le garde-fou est la seule chose qui empêche un agent — ou une
distraction — d'écrire dans l'historique quelque chose que la gouvernance refuse. Tout le reste du
squelette repose sur lui.

La décision `TPL-D-043` a écarté ces trois constats du lot précédent pour une raison assumée : un
correctif rapide sur la pièce la plus délicate du produit est une mauvaise idée. Cette fiche est ce
qu'on avait promis à la place.

## 2. Les trois constats

### C-1 — Le garde-fou s'annonce installé là où Git ne le cherchera pas

**Ce qui se passe.** Un *worktree lié* est une seconde copie de travail du même dépôt, sur une autre
branche — pratique pour comparer deux versions sans changer de branche. Dans une telle copie,
`install-gate` écrit le garde-fou dans le dossier propre à ce worktree et répond `PASS`. Or Git,
lui, va chercher ses hooks dans le dossier commun du dépôt. Le garde-fou est écrit à un endroit que
Git ne consultera jamais.

Résultat mesuré par le contrôle : la commande de contrôle refuse le commit interdit, mais **le vrai
`git commit` réussit**. Et l'audit suivant annonce toujours « garde-fou installé ».

**Ce que ça coûte.** C'est le pire des trois : une protection qui ment sur sa propre présence est
pire qu'une protection absente, parce qu'on cesse de la surveiller.

**La cause, vérifiée dans le code.** Le contrôleur demande à Git `rev-parse --git-dir`, qui dans un
worktree lié répond le dossier *du worktree*. La bonne question est `rev-parse --git-path
hooks/pre-commit`, qui répond le dossier *commun* — celui que Git utilisera vraiment. Vérifié :

```
git-dir       : …/repo/.git/worktrees/lie
git-path hook : …/repo/.git/hooks/pre-commit     ← celui que Git exécute
```

**Le correctif.** Une ligne : poser la bonne question à Git. Deux fonctions concernées
(`gate_installed_path`, et par ricochet `commit_gate_state` et `install-gate`).

**Ce qu'on risque de casser.** Rien d'évident : dans un dépôt sans worktree lié, les deux questions
donnent la même réponse. Le risque est que des projets aient déjà un garde-fou installé au mauvais
endroit et se voient soudain annoncer `NOT_INSTALLED` — ce qui est la vérité, mais il faut que le
message le dise clairement plutôt que de laisser croire à une régression.

**L'essai.** Créer un worktree lié sans hook commun, installer, tenter un vrai commit interdit :
il doit être refusé. Rouge aujourd'hui, vert après.

---

### C-2 — Un fichier hors périmètre traverse une fusion sans être vu

**Ce qui se passe.** Sur la branche canonique, une fusion d'intégration est préparée sans être
validée. On ajoute à l'index un fichier qui n'appartient ni à la branche fusionnée ni au périmètre
autorisé du chantier. Tant qu'il est visible sur le disque, le garde-fou le refuse. **On l'efface du
disque en laissant son contenu dans l'index** : le garde-fou passe, la fusion est enregistrée, et le
fichier est dans l'historique. L'audit d'après est propre.

**Ce que ça coûte.** Un fichier arbitraire peut entrer par la porte de l'intégration. Le contrôle
précise honnêtement la limite : le chantier reste `IN_PROGRESS`, ça ne produit pas un `DONE`
frauduleux. Mais l'historique, lui, est écrit.

**La cause, vérifiée dans le code — et une erreur d'estimation de ma part.**

Cette fiche annonçait d'abord une refonte de la classification des chemins, « le passage obligé de
chaque commit », avec un risque de régression important. **C'était faux, et il faut le dire avant de
lire la suite.** Cette estimation a été écrite à partir du rapport de contrôle et de l'architecture
générale des deux audits, sans ouvrir la fonction fautive. Le symptôme était bien décrit ; la cause
en a été déduite plus profonde qu'elle ne l'est. Leçon retenue : ne pas chiffrer un risque sans
avoir lu la ligne en cause.

La cause réelle tient en une ligne. Pendant une fusion, les deux règles de branche sont
volontairement mises de côté (« une intégration n'est pas du développement ») et tout le poids
repose sur une seule vérification : *cette fusion n'apporte-t-elle que ce que sa branche a
changé ?* Pour répondre, elle comparait `HEAD` **au dossier de travail** (`git diff HEAD`). Or le
commit, lui, emporte **l'index**. Un fichier mis à l'index puis effacé du disque n'apparaît plus
dans cette comparaison — il n'est ni dans `HEAD` ni sur le disque — alors qu'il est bel et bien
dans ce que le commit va écrire.

**Le correctif.** Lire l'index : `git diff --cached HEAD`. Un mot.

**Ce qu'on risque de casser — mesuré, pas estimé.** La vérification ne tourne que pendant une
fusion, et le correctif ne change que la source de sa comparaison. Mesure faite sur la `3.16.1` :
141 essais verts dans le template, 141 verts (9 ignorés) sur une copie d'un projet réel monté avec
le correctif, audit `PASS`. Rien d'autre n'est touché.

Un effet de bord, voulu : un fichier modifié sur le disque mais **non indexé** n'est plus signalé
par cette vérification pendant une fusion. C'est correct — le commit ne l'emporte pas — et l'audit
du dossier de travail continue de le voir de son côté.

**Les essais.** Le contre-exemple du contrôle, plus un témoin par usage légitime qui doit rester
vert : une fusion d'intégration normale, un renommage, une reprise après blocage.

---

### C-3 — Quand le garde-fou ne peut pas prendre son instantané, il laisse passer

**Ce qui se passe.** Pour auditer ce que le commit va vraiment écrire, le garde-fou matérialise
l'index en arbre réel, dans un worktree temporaire. Si cette création est rendue impossible, il
**retombe silencieusement sur le seul audit du dossier de travail** — et l'annonce dans une ligne
`PASS`. Le commit passe. Le contrôle l'a démontré en rendant le dossier de métadonnées de Git
inutilisable ; c'est le plus difficile à atteindre des trois, il demande un accès administratif aux
entrailles de Git.

**Ce que ça coûte.** Une garantie annoncée qui s'annule d'elle-même quand elle est gênée. La
doctrine du squelette dit `FAIL_CLOSED` : ce qu'on ne peut pas vérifier, on le refuse.

**La cause, vérifiée dans le code.** Trois lignes explicites : quand l'instantané ne peut pas être
créé, la fonction rend les résultats du dossier de travail et un libellé disant que l'état indexé
n'a pas pu être matérialisé. Aucun échec n'est levé.

**Le correctif.** Court : refuser au lieu de rendre. Une ligne de refus, un message qui dit
pourquoi, et un `PROJECT_CONTROL_HOOK_OVERRIDE` reste la porte de secours mandatée pour un
environnement où la création d'un worktree temporaire est réellement impossible.

**Ce qu'on risque de casser.** Le vrai risque : un environnement légitime où la création échoue —
disque plein, système de fichiers exotique, permissions restreintes en intégration continue. Un
projet se retrouverait incapable de committer sans override. Il faut décider si c'est acceptable
(je pense que oui, c'est exactement ce que « fail-closed » veut dire) et surtout écrire le message
de refus pour qu'il soit compréhensible et donne la sortie.

**L'essai.** Rendre l'instantané impossible, tenter un vrai commit : refusé. Puis le même avec
l'override : accepté et tracé.

## 3. Ce que je propose

Trois lots, dans cet ordre, parce qu'ils vont du sûr au risqué :

| Lot | Contenu | Ampleur | Risque de régression |
|---|---|---|---|
| **A** | C-1, le garde-fou au bon endroit | une ligne + un essai | quasi nul |
| **B** | C-3, l'instantané impossible refuse | quelques lignes + deux essais | faible, mais change un comportement |
| **C** | C-2, le passager de fusion | un mot (mesuré après coup) | nul, mesuré |

A et B ont tenu dans une même version, la `3.16.1`. C devait avoir la sienne avec une campagne de
non-régression ; la mesure faite après coup a montré que c'était un correctif de la même famille que
les deux autres, et il est livré en `3.16.2` (`TPL-D-047`). Le découpage en trois lots reste bon ;
seule l'estimation du lot C était mauvaise.

## 4. Ce que ce chantier ne ferait pas

- Il ne transforme pas le garde-fou en protection contre un adversaire déterminé qui a les droits
  d'administration sur le dépôt. Le garde-fou est local : le contrôle l'a rappelé, un dépôt nu
  accepte ce qu'on lui pousse, et aucune protection serveur n'a jamais été promise.
- Il ne touche pas à la question de la protection côté remote (GitHub, NAS), qui est un autre
  sujet et une autre décision.

## 5. Questions ouvertes

1. **Les trois lots, ou seulement A et B ?** C est le plus utile et le plus risqué. Il est
   défendable de le remettre à après un usage plus large du squelette.
2. **Un projet qui découvre son garde-fou mal installé** (conséquence de C-1) : on le laisse
   découvrir par l'audit, ou la montée de version le réinstalle d'office ?
3. **C-3 et l'override** : refuser sec, ou refuser avec une porte mandatée ? Je penche pour la
   porte mandatée, cohérente avec le reste du produit.
4. **Faut-il une troisième passe de contrôle** après ce chantier, et sur quels thèmes ?

## 6. État

`DONE`. Les quatre questions ont été tranchées par le Project Owner le 10 septembre 2026
(« on fait dans un ordre professionnel et logique », puis « je suis d'accord ») :

1. les trois lots, mais en deux versions — **A et B en `3.16.1`**, C dans la sienne, avec sa propre
   campagne de non-régression ;
2. un projet au garde-fou mal installé le découvre par l'audit, qui le nomme `NOT_INSTALLED`
   puisque c'est la vérité, et `install-gate` le remet au bon endroit ; la montée de version le
   réinstalle déjà d'office ;
3. C-3 refuse, mais garde sa porte mandatée (`PROJECT_CONTROL_HOOK_OVERRIDE`) ;
4. une troisième passe de contrôle **après** C, pas avant.

**Livré en `3.16.1` :** C-1 et C-3 (`TPL-D-045`). **Livré en `3.16.2` :** C-2 (`TPL-D-047`).
Le chantier est clos ; il reste une troisième passe de contrôle, prévue après ce lot.
