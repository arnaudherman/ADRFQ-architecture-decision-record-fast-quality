# ADR-0004 — Témoin du contrat du template

## 1. Carte d'identité

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-0004 |
| Statut             | Proposé |
| Date de décision   | 2026-07-01 |
| Validé par         | Mme Test (architecte d'entreprise) |
Note égarée au milieu du tableau : elle le coupe en deux.
| Équipe / périmètre | Équipe témoin — tests du linter |
| Mots-clés          | témoin, contrat, linter |
| Remplace           | — |
| Remplacé par       | — |

## 2. Résumé de la décision

> **[ADR-0004 — Proposé]** Face à un besoin d'erreurs reproductibles, dans le contexte des tests du linter, nous avons décidé de violer le contrat du template afin d'obtenir un témoin stable, en acceptant un compromis fantôme.

## 3. Contexte et problème

Ce fichier viole volontairement les règles du contrat du template : couplage
statut↔validation, tableau d'un seul tenant, ordre des segments du résumé, contrat du
module « Options considérées », justification creuse, date de revue.

## Options considérées

### Option 1 — Alpha _(retenue)_
- Pour : exerce la règle du nom d'option.
- Contre : ne correspond pas au « X » de la section 4.

### Option 2 — Beta _(écartée)_
- Pour : présente pour atteindre les deux options.
- Contre :

## 4. Décision

Option retenue : « Beta », parce que c'est la meilleure solution.

Conserver ce fichier tel quel : il exerce les règles du contrat du template.

## 5. Conséquences

### Positives
- Les règles du contrat sont couvertes par le snapshot.

### Négatives et compromis acceptés
- La maintenance devient coûteuse.

## Validation et suivi

- Indicateur de réussite : chaque règle du contrat apparaît dans la sortie attendue.
- Revue prévue le : bientôt
