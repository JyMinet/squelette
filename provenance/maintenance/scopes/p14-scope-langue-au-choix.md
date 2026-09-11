# P14 — La langue au choix : français et anglais

*Fiche de cadrage. 9 septembre 2026. Étape 1 : ce que le squelette dit au Project Owner.*

## 1. L'idée, dans ses mots

> « enregistre que l'on veut donner la possibilité que le squelette parle anglais et français ! Faut rajouter l'anglais ! Choix de l'utilisateur ! » (8 sept.)

> « on prévoit les gouvernances en anglais pour plus tard ! » (8 sept.)

Même principe que le style de retour (P11) : la langue est un choix du Project Owner, pas une décision de l'agent.

## 2. Ce que le terrain dit — mesuré avant de cadrer

Le squelette est **déjà bilingue par accident**, et pas là où on le croyait :

| Ce que le contrôleur produit | Langue avant la 3.13.0 | Nombre |
|---|---|---|
| Messages de refus (`ProjectControlError`) | **anglais** | 180 |
| Noms et détails des vérifications (`PASS: CORE_ALIGNED — …`) | **anglais** | ~120 |
| Commande `status` | français | ~30 phrases |
| Vue roadmap (page et Markdown) | français | ~110 phrases |

Autrement dit : ce qui parle à une machine est en anglais, ce qui parle au Project Owner est en français. Le chantier ne consiste donc pas à « ajouter l'anglais » partout, mais à **rendre choisissable la seule partie qui s'adresse à un humain**.

## 3. Décisions du Project Owner (9 sept.)

1. **Périmètre** — le choix couvre la prose qui s'adresse au Project Owner : `status` et la vue roadmap. Les noms de vérifications et les messages de refus restent en anglais. Ce n'est pas un renoncement : ce sont des **identifiants**, un vocabulaire fermé sur lequel s'appuient les essais, le garde-fou de commit et tout outil qui lit la sortie. Les traduire les rendrait instables.
2. **Emplacement** — le choix vit dans Project State (`language`), à côté de `reporting_style`, et la vue le suit, exactement comme `style` suit déjà le style de retour.
3. **Défaut** — aucun. `UNKNOWN` jusqu'à la question de `FIRST_START`, signalé par la vérification `LANGUAGE` tant que ce n'est pas tranché, et exigé pour clore l'initialisation. Le squelette ne suppose pas la langue de son propriétaire.

## 4. Ce que ça donne, concrètement

- Une question de plus dans l'entretien d'initialisation, juste après le style de retour.
- `status` et la vue roadmap dans la langue choisie ; en changer plus tard est une décision humaine, comme pour le style.
- Une vérification d'audit `LANGUAGE`, calquée sur `REPORTING_STYLE`.
- Deux catalogues de messages, un par fichier qui produit de la prose : `SPEECH` dans `project_control.py`, `TEXT` dans `roadmap_view.py`. Bibliothèque standard seulement, comme tout le reste.
- La vue ne traduit jamais les mots du Project Owner : citations, résumés et sources restent tels qu'il les a écrits.

## 5. Ce qui reste hors périmètre

- **Étape 2, plus tard** : les documents de gouvernance en anglais (`AGENTS.md`, `FIRST_START.md`, la Definition of Done, les modèles de décision). C'est un travail de rédaction, pas de mécanique.
- **Toujours en français** : les commits, les tags, le journal du squelette (`provenance/CHANGELOG.md`). Ce sont les archives du Project Owner, pas l'interface.
- **Toujours en anglais** : les identifiants de vérification et les messages de refus.

## 6. Chemin de livraison

Le chemin habituel : version d'essai dans une copie jetable hors du dossier accordé, un essai par comportement nouveau vérifié rouge avant et vert après, double arrêt, branche `claude/v3.13-langue`, promotion sur décision du Project Owner.

Version livrée : **3.13.0**.
