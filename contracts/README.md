# Versioned Contracts

Le core ne contient aucun contrat métier actif. Créer uniquement les contrats requis par l’architecture validée.

Principe obligatoire : `PRODUCER → VERSIONED CONTRACT → CONSUMER`.

- annoncer la version produite et les versions acceptées ;
- prouver la compatibilité par contract tests ;
- créer une nouvelle version majeure pour tout changement incompatible de sens, type ou exigence ;
- interdire à un consumer de lire chemins, tables, classes ou stores internes d’un producer ;
- accepter `UNKNOWN` seulement lorsqu’un schéma le prévoit explicitement.

Des exemples spécialisés sont disponibles sous `templates/optional-contracts/`. Ils sont inactifs et sans autorité.
