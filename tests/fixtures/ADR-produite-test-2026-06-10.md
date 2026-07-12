# ADR-0002 — Utiliser PostgreSQL pour le Référentiel Produits

## 1. Carte d'identité

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-0002 |
| Statut             | Proposé |
| Date de décision   | 2026-06-08 |
| Validé par         | — |
| Équipe / périmètre | non documenté en séance (présents : Arnaud, Mehdi, Jonas) |
| Mots-clés          | PostgreSQL, base de données, Référentiel Produits, provisioning |
| Remplace           | — |
| Remplacé par       | — |

## 2. Résumé de la décision

> **[ADR-0002 — Proposé]** Dans le contexte du nouveau service Référentiel Produits, face au besoin de choisir une base de données pour la persistance, nous avons décidé d'utiliser PostgreSQL afin d'obtenir un bénéfice non documenté en séance, en acceptant des compromis non évalués en séance.

## 3. Contexte et problème

Lors de la séance d'architecture du 2026-06-08 (présents : Arnaud, Mehdi, Jonas), le point unique à l'ordre du jour était le choix de la base de données pour le nouveau service Référentiel Produits. Le PV indique que le groupe est parti sur PostgreSQL et que « tout le monde est d'accord ». Jonas s'est vu confier le provisioning. La prochaine séance est à planifier.

Le PV ne documente pas : les alternatives discutées, les critères ayant motivé le choix, ni les conséquences détaillées (coûts, opérationnel, disponibilité, sauvegardes). Ces éléments sont donc non documentés en séance et figurent comme tels dans cette ADR.

## 4. Décision

La décision prise en séance est d'utiliser PostgreSQL pour la persistance du service Référentiel Produits. Le provisioning est attribué à Jonas.

Les détails d'implémentation (versions, configuration haute disponibilité, stratégie de sauvegarde, solution managée vs auto‑hébergée) n'ont pas été tranchés en séance et sont laissés « non tranchés en séance » — ils devront être précisés lors d'une prochaine réunion ou dans un ticket d'implémentation.

## 5. Conséquences

### Positives
- Le provisioning a été attribué (Jonas), ce qui permet d'engager la mise en œuvre opérationnelle une fois les tâches planifiées.
- L'accord de principe sur PostgreSQL évite un blocage immédiat sur le choix de la base.

### Négatives et compromis acceptés
- Les conséquences opérationnelles, coûts d'exploitation, exigences de haute disponibilité et de sauvegarde n'ont pas été évaluées en séance (non évaluées en séance).
- Risques potentiels non documentés en séance : effort d'exploitation, besoin de compétences spécifiques, options de scaling et impacts sur le SLA. Ces points devront faire l'objet d'une analyse avant déploiement en production.

## Références

- PV / source : tests/fixtures/pv-pauvre-postgresql.md (PV séance 2026-06-08)
- Exemple ADR : tests/fixtures/ADR-0001-exemple.md
