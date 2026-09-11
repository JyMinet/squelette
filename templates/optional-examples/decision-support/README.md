# Optional Decision-Support Example

Status: `OPTIONAL / NOT_ACTIVE / NOT_AUTHORITY / NOT_PART_OF_CORE`

Cette note consolide les anciens dossiers spécialisés retirés du core : acquisition, observations, signals, decision engine, append-only history, publication et decision portal.

L’exemple illustre seulement une séparation possible : une source est acquise et prouvée, des observations peuvent être normalisées, des signals peuvent être calculés, un moteur peut produire un record, puis une couche de publication et une interface peuvent le présenter. Chaque étape possède ses internes et publie un contrat versionné.

Ce pipeline n’est ni universel ni recommandé par défaut. Ne créer ces composants que si le Charter, l’architecture et l’Anti-Octopus Review prouvent leur nécessité. Les contrats illustratifs correspondants vivent sous `templates/optional-contracts/`.
