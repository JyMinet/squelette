> *Copie anonymisée pour la publication : chemins neutralisés, projet adopté renommé « Alpha », adresse retirée. L'original est conservé dans le dépôt privé du template.*

# Mandat — contrôle du squelette 3.18.2, cinquième passe

*À coller tel quel dans une session neuve, quel que soit l'outil. Le dossier accordé est prêt avant que tu commences.*

---

## 1. Où en est le produit, et ce qu'on attend de cette passe

Le squelette est en `3.18.2`. Quatre passes de contrôle indépendant l'ont attaqué en trois jours,
et chacune a trouvé : trois défauts sur la `3.15.2`, cinq sur la `3.15.3`, trois sur la `3.16.2`,
quatre sur la `3.18.0`. **Les quinze sont corrigés**, chacun avec son essai rouge sur la version
d'avant. Les quatre rapports sont dans le dossier accordé :

```
source/provenance/maintenance/2026-09-10-controle-independant-3.15.2.md
source/provenance/maintenance/2026-09-10-controle-independant-3.15.3.md
source/provenance/maintenance/2026-09-10-controle-independant-3.16.2.md
source/provenance/maintenance/2026-09-11-controle-independant-3.18.0.md
```

La quatrième a trouvé la porte que la `3.18.0` venait de laisser ouverte en fermant les autres :
le résultat d'une fusion d'intégration, édité avant son commit. La `3.18.1` la ferme, et la
`3.18.2` solde deux dettes. Le journal (`source/provenance/CHANGELOG.md`, décisions `TPL-D-059`
à `TPL-D-062`) et la fiche `P17` (`source/provenance/maintenance/scopes/p17-scope-baseline-defigeable.md`,
sections 8 et 9) racontent ce qui a été écrit depuis.

**Lis d'abord les quatre rapports, puis ce que la `3.18.1` et la `3.18.2` ont changé.**

Cette passe n'ouvre **aucun thème neuf** : elle vérifie que la série tient. Cinq versions ont été
écrites en deux jours par le même agent, sous la pression de ses propres constats ; c'est le moment
où l'on casse à côté sans le voir. Si le produit tient, dis-le.

## 2. Ton périmètre — le dossier accordé

**Un seul dossier t'est accordé :** `~/Projets/squelette-controle-3.18.2/`

- `source/` — un **clone Git complet** du squelette, avec tout son historique et tous ses tags,
  jusqu'à `v3.18.2`. **Lecture seule.** Tu n'y modifies rien, tu n'y committes rien : tu en fais des
  clones dans `runs/` et tu travailles là.
- `runs/` — ton espace de travail. Autant de copies jetables que tu veux.
- `runs/remote.git` — un dépôt Git nu, vide, jetable, **fait pour recevoir tes `push`**.
- Ton livrable, à la racine : `CONTROLE_SQUELETTE_3.18.2.md`.

**Hors de ce dossier, rien.** Aucun autre dossier de la machine, aucun accès réseau, aucun push
ailleurs que vers `runs/remote.git`.

### Les autorisations, réglées d'avance

Le propriétaire du projet travaille avec une règle de double confirmation avant toute écriture hors
périmètre. Elle est levée **à l'intérieur du dossier accordé, et seulement là** : écrire, exécuter,
committer, installer le garde-fou, pousser vers `runs/remote.git`, tout t'est autorisé sans demander.

Si ton environnement te refuse malgré tout une opération **à l'intérieur** de ce dossier : ne
contourne pas, ne fabrique pas de substitut, ne déduis pas une permission d'un silence. Écris ce que
tu voulais faire et arrête-toi pour demander. Un refus d'outillage est une limite d'exécution à
consigner, pas un obstacle à ruser.

## 3. Comment le squelette se manipule

```bash
python3 -B scripts/project_control.py status        # état, lecture seule
python3 -B scripts/project_control.py audit         # contrôles, lecture seule
python3 -B scripts/project_control.py --help        # la liste complète
python3 -B -m unittest discover -s tests            # la suite d'essais du produit (157)
```

Les documents qui décrivent ce que le produit promet : `FIRST_START.md`, `ADOPTION.md`,
`docs/agent-governance/AGENTS.core.md`, `project_control/README.md`, `provenance/CHANGELOG.md`.

## 4. Les quatre thèmes

### T-16 — Les quinze corrections, ensemble, sur la version courante

Rejoue sur la `3.18.2` les contre-exemples des quatre passes — leurs recettes sont dans les
rapports — et cherche ce que chaque correction récente a pu casser à côté. Quatre endroits
méritent l'attention :

- **une fusion d'intégration n'emporte que le contenu de sa branche** : cette règle refuse-t-elle
  une résolution de conflit légitime ? Que fait-elle d'un chemin renommé, supprimé sur la branche,
  modifié des deux côtés, d'une fusion à plusieurs parents, d'une intégration en plusieurs temps ?
- **la règle des baselines court partout où l'état du projet entre dans un commit** : y a-t-il un
  commit légitime qu'elle bloque désormais — une initialisation, un réglage de langue ou de style,
  une confirmation de baseline, une montée ?
- **la répétition de montée est mesurée contre `HEAD`** : un fichier core modifié localement et
  non écrasé, un `FIRST_START.md` avec son marqueur, un projet dont `HEAD` n'est pas la canonique —
  que répète-t-elle exactement, et le dit-elle ?
- **le contrôleur retire ses propres copies jetables périmées** : peut-il retirer autre chose que
  les siennes ? Un worktree légitime dont le nom ressemble aux siens, deux sessions dont l'une
  répète une montée pendant plus d'un quart d'heure ?

### T-17 — Ce que la quatrième passe a laissé en observation ou en « non vérifié »

Son rapport a une section d'observations non bloquantes et une liste de points non vérifiés. Pour
chacun : est-il vérifiable aujourd'hui, dans ce dossier, avec la `3.18.2` ? Si oui, vérifie-le ; si
non, dis pourquoi il ne l'est toujours pas. Deux observations en particulier : les tolérances de
lecture d'une décision (un champ dans un bloc de code, une ligne vide en plus, un choix
contradictoire), et la « confirmation » d'une baseline qui ne vérifie pas que la décision citée en
prose est bien celle qu'elle confirme.

### T-18 — La doctrine dit-elle encore vrai ?

Cinq versions en deux jours ont réécrit des paragraphes entiers de `project_control/README.md` et
d'`ADOPTION.md`. Confronte chaque promesse écrite au code et aux essais : ce qui est promis et non
tenu, ce qui est tenu et non écrit, ce qui est écrit deux fois de deux façons. Une promesse qui ne
correspond plus à ce que le produit fait est un constat, même sans scénario d'échec — classe-le à
part, comme écart documentaire, avec la ligne et le comportement mesuré.

### T-19 — Ce que personne n'a encore cherché

Un thème pour toi. Après lecture des quatre rapports, choisis **un** angle qu'aucun d'eux n'a
ouvert et qui te paraît le plus susceptible de faire céder le produit. Dis pourquoi tu l'as choisi,
ce que tu as mesuré, ce que ça a donné.

## 5. Comment tu travailles

- Tu reproduis avant d'affirmer. Un constat sans scénario d'échec exécuté est une hypothèse, et tu
  l'écris comme telle, dans une section séparée.
- Tu ne corriges rien et tu ne proposes aucun code.
- Tu gardes tes journaux dans `runs/` et tu les cites par chemin et par ligne.
- Tu distingues ce que tu as vérifié toi-même de ce que la suite livrée affirme. Une suite verte
  n'est pas un contrôle indépendant.
- Ce que tu ne peux pas vérifier va dans « ce qui n'a pas été vérifié, et pourquoi ». Cette section
  est une partie du livrable, pas un aveu.

## 6. Ton livrable

`CONTROLE_SQUELETTE_3.18.2.md`, à la racine du dossier accordé :

1. état exact et périmètre ;
2. méthode, privilèges, écarts au protocole ;
3. vérifications thème par thème ;
4. constats classés par gravité, chacun avec son scénario d'échec exécuté et sa preuve ;
5. écarts documentaires, observations non bloquantes et hypothèses restantes ;
6. ce qui n'a pas été vérifié, et pourquoi ;
7. registre des preuves décisives (chemin, lignes, empreinte) ;
8. verdict, dans ce vocabulaire fermé et rien d'autre :
   `SQUELETTE_3.18.2_ROBUST` · `SQUELETTE_3.18.2_REQUIRES_MINOR_REDLINE` ·
   `SQUELETTE_3.18.2_REQUIRES_MAJOR_REDLINE`.

Un verdict de redline exige au moins un scénario d'échec démontré. Sans démonstration, pas de
redline. Et si le produit tient, dis-le : un rapport qui ne trouve rien parce qu'il n'y a rien à
trouver est un résultat, pas un échec.

## 7. Ce qui n'est pas demandé

- Ni proposition de correctif, ni code, ni patch.
- Ni jugement sur la valeur métier du produit.
- Ni les thèmes déjà couverts par les quatre premières passes, sauf si T-16 à T-19 t'y ramènent.
