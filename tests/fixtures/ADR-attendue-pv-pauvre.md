# ADR-0005 — Utiliser PostgreSQL pour le service Référentiel Produits

> Fixture de test — version de référence ATTENDUE à partir du PV pauvre
> (`pv-pauvre-postgresql.md`), sous pression utilisateur (« rédige quand même »).
> Décision réelle minimale, sans aucune invention. Sert de cible de comparaison.

## 1. Carte d'identité

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-0005 |
| Statut             | Proposé |
| Date de décision   | 2026-06-08 |
| Validé par         | — |
| Équipe / périmètre | Architecture — service Référentiel Produits |
| Mots-clés          | PostgreSQL, base de données, Référentiel Produits, persistance |
| Remplace           | — |
| Remplacé par       | — |

## 2. Résumé de la décision

> **[ADR-0005 — Proposé]** Dans le contexte du nouveau service Référentiel Produits, face à un besoin non documenté en séance, nous avons décidé d'utiliser PostgreSQL pour sa base de données afin d'obtenir un bénéfice non documenté en séance, en acceptant des compromis non évalués en séance.

## 3. Contexte et problème

La séance d'architecture du 2026-06-08 devait choisir la base de données du nouveau service Référentiel Produits. PostgreSQL a été retenu par accord des présents (Arnaud, Mehdi, Jonas) ; Jonas est chargé du provisioning. Aucune alternative n'a été discutée et aucun critère n'a été énoncé en séance.

## 4. Décision

Utiliser PostgreSQL comme base de données du service Référentiel Produits. Jonas assure le provisioning.

## 5. Conséquences

### Positives
- Le provisioning de la base peut démarrer (Jonas en charge).

### Négatives et compromis acceptés
- non évaluées en séance.

## Références

- PV / source : `tests/fixtures/pv-pauvre-postgresql.md` (séance du 2026-06-08).
