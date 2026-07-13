# ADR-0003 — Témoin conforme au format canonique

## 1. Carte d'identité

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-0003 |
| Statut             | Proposé |
| Date de décision   | — |
| Validé par         | — |
| Équipe / périmètre | Équipe témoin — tests du linter |
| Mots-clés          | témoin, conformité, linter |
| Remplace           | — |
| Remplacé par       | — |

## 2. Résumé de la décision

> **[ADR-0003 — Proposé]** Dans le contexte des tests du linter, face au besoin d'un contrôle positif, nous avons décidé de maintenir ce fichier parfaitement conforme afin d'obtenir la preuve que le linter ne produit pas de faux positifs, en acceptant de le mettre à jour à chaque évolution du template.

## 3. Contexte et problème

Le jeu de test a besoin d'un fichier que le linter doit déclarer conforme : si ce fichier
passe en erreur, c'est le linter qui a régressé, pas le fichier. Sa date « — » exerce au
passage la sentinelle « source non datée ».

## 4. Décision

Maintenir ce fichier conforme au template canonique, en le mettant à jour à chaque
évolution du format.

## 5. Conséquences

### Positives
- Tout faux positif introduit dans le linter est détecté immédiatement.

### Négatives et compromis acceptés
- Une évolution du template impose de mettre à jour ce fichier et le snapshot.
