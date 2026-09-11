# Template Provenance

Ce document établit l'ascendance vérifiée de la baseline courante. Conformément au principe du Charter, une correction crée une révision liée et n'efface pas l'énoncé antérieur.

## Chaîne d'ascendance

```text
bede17a1b3a7d8ecd093d98f4550c34db660b57d
    ↓  export de l'arbre suivi
becc60fc92615f8c9ab2acab185c0c583a5bb584
    ↓  export de l'arbre suivi + ajouts
baseline courante
```

## Maillon 1 — origine de la baseline intermédiaire (énoncé d'origine, conservé)

Cette baseline autonome a été créée à partir de l'arbre suivi du squelette généraliste gouverné au commit source `bede17a1b3a7d8ecd093d98f4550c34db660b57d`.

- méthode : export Git du commit, sans copie brute de `.git/` ;
- fichiers non suivis, caches et artefacts système copiés : `NONE` ;
- historique Git hérité : `NONE` ;
- remote hérité : `NONE`.

Cet énoncé décrit l'origine de la baseline intermédiaire, et non celle de la baseline courante. Voir `ERR-01`.

## Maillon 2 — origine de la baseline courante

- source : arbre suivi au commit `becc60fc92615f8c9ab2acab185c0c583a5bb584`, branche `fix/project-control-simplification-v3` ;
- méthode : export de l'arbre suivi, sans copie brute de `.git/` ;
- historique Git hérité : `NONE` ; remote hérité : `NONE` ;
- écarts assumés par rapport au commit source : `ADOPTION.md` ajouté ; `runtime_proof/` ajouté (21 fichiers) ; `README.md` et `data/README.md` modifiés.

### Vérification

- date : 2026-09-05 ; méthode : comparaison des hashes d'objets Git, fichier par fichier ;
- 74 fichiers dans la baseline courante, dont 52 communs avec le commit source ;
- 50 des 52 fichiers communs sont identiques ; les 2 écarts sont ceux déclarés ci-dessus ;
- comparaison de contrôle contre `bede17a…` : 17 fichiers identiques sur 74, ce qui exclut cette ascendance directe.

## Erratum

`ERR-01` — 2026-09-05. Jusqu'à cette date, ce document ne décrivait que le maillon 1 et attribuait donc à la baseline courante une origine directe au commit `bede17a…`. La vérification par hashes établit que son ascendance directe est `becc60f…`. Le maillon manquant est enregistré ci-dessus. Aucun contenu de la baseline n'est modifié par cet erratum.

Cette trace prouve l'origine de la baseline. Elle n'active aucun template optionnel et n'est ni une autorité runtime ni une dépendance externe.
