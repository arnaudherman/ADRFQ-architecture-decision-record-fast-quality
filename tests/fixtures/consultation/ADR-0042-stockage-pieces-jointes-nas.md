# ADR-0042 — Stocker les pièces jointes sur le NAS interne

> Fixture de test (consultation) — ADR **remplacée** : la bonne réponse à toute question
> sur le stockage des pièces jointes n'est PAS ici, mais dans ADR-0043.

## 1. Carte d'identité

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-0042 |
| Statut             | Remplacé |
| Date de décision   | 2024-03-12 |
| Équipe / périmètre | Architecture — plateforme documentaire |
| Mots-clés          | pièces jointes, stockage, NAS, plateforme documentaire |
| Remplace           | — |
| Remplacé par       | ADR-0043 |

## 2. Résumé de la décision

> **[ADR-0042 — Remplacé]** Dans le contexte de la plateforme documentaire, face au besoin de stocker les pièces jointes des dossiers, nous avons décidé de les stocker sur le NAS interne afin d'obtenir une mise en œuvre immédiate avec l'infrastructure existante, en acceptant une capacité plafonnée et des sauvegardes manuelles.

## 3. Contexte et problème

La plateforme documentaire devait stocker les pièces jointes des dossiers clients.
Le NAS interne existait déjà et ne demandait aucun investissement.

## 4. Décision

Stocker les pièces jointes des dossiers sur le volume dédié du NAS interne.

## 5. Conséquences

### Positives
- Mise en œuvre immédiate, sans achat ni provisioning.

### Négatives et compromis acceptés
- Capacité plafonnée par le matériel existant.
- Sauvegardes manuelles, sans versionnage.
