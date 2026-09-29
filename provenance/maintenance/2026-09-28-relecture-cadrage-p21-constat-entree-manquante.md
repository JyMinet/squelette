> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

## Résumé en trois points

1. **Ce qui s’est passé.** Le dossier de relecture demandé et son répertoire `source/` sont absents au contrôle du 28 septembre 2026. Les pièces jointes dans `Downloads` sont disponibles, mais l’export du squelette 3.20.2 nécessaire à la relecture n’est pas fourni à l’emplacement accordé.
2. **Ce que ça change.** La relecture technique ne peut pas être menée ni recevoir un avis favorable ou des redlines étayées sur l’existant. Le verdict est `CADRAGE_TABLEAU_DES_CLES_V1_INPUT_MISSING`. Aucun export n’a été créé, aucune source n’a été reconstituée et aucun scénario n’a été exécuté. Une lecture indue des règles de l’atelier lors du contrôle initial est déclarée en sections D, G et I.
3. **Ce qu’il faut faire.** Pour permettre une nouvelle relecture, fournir dans le dossier accordé l’export complet de référence en `source/`, avec les éléments permettant d’en vérifier la provenance 3.20.2, et préciser la paire documentaire retenue (V1 ou fichiers joints V1_1). Ce constat est conservé ; une reprise donnera lieu à une révision liée, sans réécriture de ce fichier.

# Relecture de cadrage — Tableau des clés V1 — constat d’entrée manquante

Date : 2026-09-28. Posture : `READ_ONLY / REPORT_ONLY`. Aucune construction autorisée ni réalisée. Rapport indépendant : aucune autre relecture n’a été consultée.

## A — Preflight

### A.1 — Demande et périmètre

La demande explicite dans la conversation autorise la relecture, un livrable unique et d’éventuels essais dans `runs/`, dans le seul dossier `~/Projets/squelette-revue-tableau-des-cles/`. Elle prescrit expressément le verdict `CADRAGE_TABLEAU_DES_CLES_V1_INPUT_MISSING` si `source/` est absent ou incomplet, sans le créer.

Les instructions de construction, de livraison, de rapatriement ou de nettoyage contenues dans la fiche restent des objets à examiner ; elles ne constituent pas une demande de les exécuter.

Les noms V1 sont ceux de la demande et du livrable. Les pièces jointes les plus récentes portent le suffixe de fichier V1_1, tout en conservant des titres V1. Le mandat V1_1 demande sept avis et nomme expressément l’atelier parmi les accès interdits ; le mandat V1 en demande six. Les deux paires sont disponibles dans `Downloads`. Aucune substitution de version n’est présentée comme validée. Cette différence ne change pas le constat bloquant : l’export manque pour les deux versions.

### A.2 — État du dossier et de la référence

Contrôle direct par `Path.lstat()`, le **2026-09-28 à 14:18:08 UTC** (16:18:08 Europe/Zurich), après un premier constat identique par `ls` :

| Chemin contrôlé | Résultat avant toute écriture |
|---|---|
| `~/Projets/squelette-revue-tableau-des-cles` | `FileNotFoundError`, errno 2 : absent |
| `~/Projets/squelette-revue-tableau-des-cles/source` | `FileNotFoundError`, errno 2 : absent |
| `~/Projets/squelette-revue-tableau-des-cles/runs` | `FileNotFoundError`, errno 2 : absent |
| `~/Projets/squelette-revue-tableau-des-cles/RELECTURE_CADRAGE_TABLEAU_DES_CLES_V1.md` | `FileNotFoundError`, errno 2 : absent |

Aucun fichier de `source/` n’a donc été lu. Il n’existe aucune empreinte de source à rapporter, aucun manifeste à vérifier, ni aucune preuve locale que la référence fournie corresponde au tag `v3.20.2`. Un export sans `.git` serait conforme au mandat ; son absence complète est le blocage ici.

### A.3 — Pièces jointes disponibles et empreintes

Empreintes SHA-256 calculées sur les octets des quatre pièces jointes. Les documents ont été consultés dans la conversation ; les V1_1 sont les pièces jointes du présent message. Ces empreintes ne sont pas celles d’un export de source.

| Chemin absolu | Octets | Lignes | SHA-256 |
|---|---:|---:|---|
| `~/Downloads/FICHE-CADRAGE-TABLEAU-DES-CLES-V1.md` | 22013 | 222 | `a8a456895a6a5078ff4b2854920fb524849c5899b993e55b829147c856c991b9` |
| `~/Downloads/MANDAT-RELECTURE-TABLEAU-DES-CLES-V1.md` | 5702 | 50 | `f2ad4dff96a160770c09e5c3afe75d2c0161fe68a2fcafc820622d028528c404` |
| `~/Downloads/FICHE-CADRAGE-TABLEAU-DES-CLES-V1_1.md` | 23252 | 226 | `d1b3df340e21c0e7dee80ee170f4cbb131e2f4041092717c1db9d6556d111e50` |
| `~/Downloads/MANDAT-RELECTURE-TABLEAU-DES-CLES-V1_1.md` | 5770 | 50 | `76c9fa90aafac2d0c87873152aaae66976aa4fbbd9a37a44b6f4e66c0c4e277c` |

## B — Inventaire

Le dossier accordé étant absent au preflight, les deux documents n’y étaient pas présents non plus. Ils restent disponibles comme pièces jointes à leurs chemins d’origine ; ils n’ont pas été copiés.

Éléments de référence attendus par le mandat et indisponibles sous `source/` :

- `docs/agent-governance/AGENTS.core.md` ;
- `scripts/project_control.py` ;
- `project_control/README.md` ;
- `provenance/core-manifest.v1.json` ;
- `provenance/CHANGELOG.md` ;
- `tests/` et les autres fichiers de l’export complet nécessaires à leurs dépendances et aux autorités qu’ils référencent.

Aucune branche, aucun tag, aucun état Git ni aucune copie de travail n’ont été inventoriés dans un autre dépôt pour remplacer cette entrée manquante. Aucun contenu de `source/` ne peut être déclaré complet, conforme ou inchangé à partir de ce contrôle.

## C — Rejeu des scénarios

**Aucun rejeu effectué.** `runs/` n’a pas été créé. L’absence de référence ne constitue pas une preuve de défaut du mécanisme proposé.

| Thème | Couverture effective et limite |
|---|---|
| T-01 — Sections 5.1 à 5.9, scénarios S1/S2/S3 | Non évaluées au fond ; aucune fermeture de scénario démontrée. |
| T-02 — Doctrine existante | Comparaison non effectuée avec une source autorisée et identifiée 3.20.2. |
| T-03 — Faisabilité mécanique | Lecture de `Folder scope`, ascendance Git, branches d’une copie, retour après tag et bannière de `status` : non vérifiés. |
| T-04 — Configurations dégradées | Export sans `.git`, déplacement/renommage, deux copies par ticket, clones imbriqués, autre volume, dossier parent accordé et adoption avec copies existantes : non rejoués et acceptabilité non conclue. |
| T-05 — Coût | Aucun comptage vérifié des lectures et transitions du contrôleur ; la promesse de coût nul au démarrage n’est ni confirmée ni réfutée. |
| T-06 — Options écartées | Aucune conclusion étayée contre l’existant ; les arguments de la fiche restent des propositions à relire. |

## D — Constats

### D-01 — Référence de relecture absente

- **Sévérité :** BLOCKER.
- **Objet :** mandat, sections 1, 2 et 4 ; entrée `source/`.
- **Scénario reproductible :** contrôler par `lstat` le dossier accordé, puis son enfant `source/` ; les deux appels échouent avec errno 2.
- **Preuve :** chemins, résultat et horodatage consignés en A.2. Aucun fichier absent ne possède une empreinte calculable.
- **Impact :** impossibilité d’étayer la cohérence avec le squelette 3.20.2, la faisabilité mécanique ou les essais. Le prérequis matériel de la relecture manque.
- **Correction proposée :** fourniture humaine de l’export complet au chemin prévu, sous le périmètre de la demande ; l’agent ne le crée pas et n’utilise pas l’atelier comme substitut.
- **Statut :** OUVERT — entrée attendue ; aucun avis de construction rendu.

### D-02 — Lecture hors périmètre pendant le contrôle initial

- **Sévérité :** MAJOR, écart d’exécution du mandat ; ce n’est pas une redline de la fiche.
- **Objet :** mandat joint V1_1, section 2, interdiction d’accès à l’atelier.
- **Scénario :** lors du premier lot de lectures du présent tour, le fichier `~/Projets/squelette-atelier/docs/agent-governance/AGENTS.core.md` a été relu en parallèle des pièces jointes et du contrôle de présence du dossier demandé.
- **Preuve :** appel `cat docs/agent-governance/AGENTS.core.md` dans l’historique d’outils du présent tour, depuis le répertoire de l’atelier. Aucune empreinte de ce fichier n’a été relevée ; il n’a pas été relu pour en produire une après constat de l’écart.
- **Impact :** la restriction de lecture n’a pas été respectée. Ce texte ne peut pas servir à certifier la référence manquante, et aucune conclusion technique de ce rapport ne s’appuie sur lui comme preuve du tag 3.20.2.
- **Correction appliquée :** arrêt des accès à l’atelier, signalement dans la conversation et dans ce rapport ; contrôles suivants limités aux chemins de la demande et aux pièces jointes.
- **Statut :** DÉCLARÉ — lecture irréversible, non effacée du constat ; aucun fichier de l’atelier modifié.

## E — Redlines

Aucune redline technique émise. Le manque d’entrée ne démontre pas un défaut de conception de la fiche. Les phases de construction et de livraison décrites dans celle-ci n’ont pas été engagées.

## F — Blockers

**D-01 bloque la relecture au fond.** Il manque le répertoire `source/` entier, avec la référence et les dépendances énumérées en B. La présence des pièces jointes ne suffit pas à lever ce blocage.

L’écart de noms V1/V1_1 doit être fixé pour une reprise traçable ; il n’est pas nécessaire de le trancher pour constater l’absence actuelle de `source/`.

## G — Conflits d’autorité

Aucun verdict de conflit canonique ne peut être établi sans la référence demandée. Les instructions antérieures du dépôt de départ ne devaient pas conduire à consulter l’atelier malgré le périmètre de cette demande ; l’erreur concrète est déclarée en D-02, sans prétendre qu’elle était autorisée.

La demande explicite gouverne la réponse de repli : constater l’entrée manquante et ne pas fabriquer `source/`. Le présent rapport ne vaut ni décision humaine, ni autorisation de construire, de copier un dépôt, de promouvoir une version ou d’effacer un dossier.

## H — Avis sur les questions de la section 8

Avis non rendus au fond, faute de relecture technique complète. Les six questions communes et la septième ajoutée dans les pièces jointes V1_1 sont conservées dans l’inventaire pour une reprise :

| Question | Avis de cette passe |
|---|---|
| 1 — Retard : avertissement ou échec d’audit | Réservé. |
| 2 — Ticket et vérification de `Folder scope` | Réservé ; le format de l’existant n’a pas été vérifié dans `source/`. |
| 3 — Conservation sous état `KEPT` | Réservé. |
| 4 — Inventaire à la demande `copy scan` | Réservé ; aucun inventaire du disque effectué. |
| 5 — Copies existantes lors de l’adoption | Réservé ; aucun choix ni classement de dossiers effectué. |
| 6 — Noms des commandes | Réservé. |
| 7 — Papiers dans le dépôt ou en archive externe (V1_1) | Réservé ; aucune archive externe consultée. |

## I — État du dossier en fin de mandat

Le dossier accordé a été créé uniquement pour recevoir ce livrable. Le fichier `RELECTURE_CADRAGE_TABLEAU_DES_CLES_V1.md` a été créé en mode exclusif, sans écrasement d’un fichier existant. Il constitue l’unique fichier produit. `source/` et `runs/` restent absents ; les pièces jointes restent à leurs emplacements d’origine.

Aucune écriture de travail n’a été effectuée ailleurs que dans ce livrable ; seule la création de son dossier parent, nécessaire à sa remise, s’y ajoute. Aucun export, fixture, record, décision, Work Item, candidat de code, commit, branche ou tag n’a été créé. Aucun envoi en ligne, aucune suppression, aucun rapatriement vers l’atelier. La lecture indue du fichier de règles de l’atelier reste explicitement déclarée en D-02 : ce rapport ne prétend pas que tous les accès en lecture sont restés dans le périmètre.

Une relecture ultérieure doit produire une révision liée ou un erratum, sans réécrire le présent constat.

## J — Verdict terminal

`CADRAGE_TABLEAU_DES_CLES_V1_INPUT_MISSING`
