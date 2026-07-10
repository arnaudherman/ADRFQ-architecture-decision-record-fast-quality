# ADR-0043 — Stocker les pièces jointes dans le stockage objet interne

> Fixture de test (consultation) — ADR **en vigueur** : c'est elle qu'un assistant doit
> citer pour toute question sur le stockage des pièces jointes, en signalant que
> ADR-0042 est remplacée.

## 1. Carte d'identité

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-0043 |
| Statut             | Accepté |
| Date de décision   | 2026-01-20 |
| Équipe / périmètre | Architecture — plateforme documentaire |
| Mots-clés          | pièces jointes, stockage objet, S3, plateforme documentaire |
| Remplace           | ADR-0042 |
| Remplacé par       | — |

## 2. Résumé de la décision

> **[ADR-0043 — Accepté]** Dans le contexte de la croissance de la plateforme documentaire, face à la saturation du NAS interne et à l'absence de versionnage, nous avons décidé de stocker les pièces jointes dans le stockage objet interne compatible S3 afin d'obtenir une capacité extensible et des sauvegardes versionnées, en acceptant la migration des volumes existants et une dépendance au service de stockage objet.

## 3. Contexte et problème

Le NAS interne retenu par la décision précédente (ADR-0042) arrive à saturation et ses sauvegardes manuelles ont causé deux pertes de versions.
La croissance de la plateforme documentaire impose une capacité extensible.
La décision a été validée en comité d'architecture du 2026-01-20 (validation nominative au PV).

## 4. Décision

Stocker toutes les pièces jointes dans le stockage objet interne compatible S3, avec versionnage activé.
Migrer les volumes existants du NAS par lots, puis décommissionner le volume dédié.

## 5. Conséquences

### Positives
- Capacité extensible sans palier matériel.
- Versionnage et sauvegardes automatiques.

### Négatives et compromis acceptés
- Migration des volumes existants à planifier et à suivre.
- Dépendance au service de stockage objet interne (SLA à surveiller).

## Références

- PV / source : comité d'architecture du 2026-01-20 (fixture fictive).
- ADR liées : ADR-0042 (remplacée).
