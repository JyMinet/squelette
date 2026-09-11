# Secret Handling Policy

Secrets fournis par un canal runtime autorisé, gardés en mémoire, jamais affichés, persistés, commités ou recopiés dans un rapport. Toute sortie est expurgée avant persistance. Secret requis absent/invalide : fail-closed, sans contournement.
