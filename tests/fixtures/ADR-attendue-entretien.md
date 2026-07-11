# ADR-0006 — Introduire un bus d'événements Kafka pour le domaine commandes

> Fixture de test — sortie de référence ATTENDUE en **mode entretien** (aucun PV) :
> l'AS documente sa décision en dialoguant avec l'agent. Les parts non tranchées sont
> marquées « à ce stade » (et non « en séance » : il n'y a pas eu de séance).

## 1. Carte d'identité

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-0006 |
| Statut             | Proposé |
| Date de décision   | 2026-07-11 |
| Équipe / périmètre | Architecture solution — domaine commandes |
| Mots-clés          | Kafka, bus d'événements, découplage, domaine commandes |
| Remplace           | — |
| Remplacé par       | — |

## 2. Résumé de la décision

> **[ADR-0006 — Proposé]** Dans le contexte du domaine commandes, face au besoin de découpler le service Commandes de ses consommateurs, nous avons décidé d'introduire un bus d'événements Kafka afin d'obtenir un découplage des traitements aval, en acceptant des compromis non évalués à ce stade.

## 3. Contexte et problème

Cette décision est documentée en entretien, sans procès-verbal : l'architecte solution la capture en dialoguant avec l'assistant.

Le service Commandes appelle aujourd'hui directement les services Facturation et Logistique, ce qui le couple à leur disponibilité.

Kafka est déjà exploité en interne pour un autre domaine, ce qui en fait le candidat naturel. Une file managée cloud a été évoquée mais non évaluée à ce stade.

## 4. Décision

Le service Commandes publie ses événements métier sur un bus Kafka ; les services Facturation et Logistique s'y abonnent.

Les appels directs entre Commandes et ses consommateurs sont supprimés au profit de cette publication.

## 5. Conséquences

### Positives
- Le service Commandes n'est plus bloqué si Facturation ou Logistique est indisponible : sa publication est découplée de leur traitement.

### Négatives et compromis acceptés
- non évaluées à ce stade.
