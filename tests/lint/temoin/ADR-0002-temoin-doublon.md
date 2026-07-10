# ADR-0002 — Témoin du doublon d'identifiant

## 1. Carte d'identité

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-0002 |
| Statut             | Remplacé |
| Date de décision   | 2026-07-01 |
| Équipe / périmètre | Équipe témoin — tests du linter |
| Mots-clés          | témoin, doublon, linter |
| Remplace           | — |
| Remplacé par       | — |

## 2. Résumé de la décision

> **[ADR-0002 — Remplacé]** Dans le contexte des tests du linter, face au besoin de vérifier la détection des doublons d'identifiant et l'incohérence « Remplacé sans cible », nous avons décidé de cumuler volontairement ces deux défauts afin d'obtenir des erreurs reproductibles, en acceptant que ce fichier soit éternellement en erreur.

## 3. Contexte et problème

Ce fichier porte le même ID que le témoin cassé, et un statut « Remplacé » sans champ
« Remplacé par » : les deux défauts attendus ici.

## 4. Décision

Conserver ce fichier tel quel : il exerce les règles « ID dupliqué » et « Remplacé sans cible ».

## 5. Conséquences

### Positives
- Les règles d'unicité des ID et de cohérence statut↔liens sont couvertes par le jeu de test.

### Négatives et compromis acceptés
- Ce fichier apparaît en erreur dans toute exécution du linter sur ce dossier.
