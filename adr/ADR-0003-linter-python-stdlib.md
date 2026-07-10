# ADR-0003 — Écrire le linter en Python, bibliothèque standard uniquement

## 1. Carte d'identité

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-0003 |
| Statut             | Accepté |
| Date de décision   | 2026-06-09 |
| Équipe / périmètre | Ce dépôt — outillage de conformité des ADR |
| Mots-clés          | linter, Python, stdlib, conformité, CI |
| Remplace           | — |
| Remplacé par       | — |

## 2. Résumé de la décision

> **[ADR-0003 — Accepté]** Dans le contexte d'un garde-fou de conformité destiné à tourner sur le poste d'un architecte comme en CI, face au coût d'installation et de maintenance d'une chaîne de dépendances, nous avons décidé d'écrire le linter en Python avec la seule bibliothèque standard afin d'obtenir un outil exécutable partout sans rien installer, en acceptant de parser le markdown avec des expressions régulières maison.

## 3. Contexte et problème

Le linter est le seul maillon déterministe de la chaîne qualité : l'agent LLM peut ignorer une consigne, pas un code de sortie.
Il doit tourner sur le poste d'un architecte non-développeur et dans un job CI minimal, sans étape d'installation.
Les linters ADR existants imposent une chaîne Node/npm (madr-lint) ou un binaire compilé (mdbook-lint, ctxgrd) — un coût d'entrée que ce dépôt ne veut pas payer.

## Critères de décision

- Zéro installation : exécutable là où `python3` existe déjà (macOS, Linux, runners GitHub).
- Déterminisme : mêmes entrées, même verdict, même code de sortie.
- Maintenance par l'équipe d'architecture elle-même, sans écosystème à suivre.

## Options considérées

### Option 1 — Python, bibliothèque standard uniquement _(retenue)_
- Pour : aucune dépendance à installer ni à mettre à jour ; lisible et modifiable par l'équipe ; `python3 scripts/lint-adr.py` suffit, en local comme en CI.
- Contre : parsing markdown par expressions régulières maison, à maintenir quand le template évolue ; certaines règles restent des heuristiques textuelles.

### Option 2 — Réutiliser un linter ADR existant (madr-lint, mdbook-lint) _(écartée)_
- Pour : règles éprouvées, maintenance externalisée.
- Contre : formats MADR/Nygard anglais incompatibles avec le template canonique français ; chaîne Node ou binaire Rust à installer ; configurabilité contraire au canon figé.

### Option 3 — Validation par prompt uniquement (checklist demandée au LLM) _(écartée)_
- Pour : aucun code à écrire ni à maintenir.
- Contre : une checklist que le modèle peut ignorer n'est pas un garde-fou ; non rejouable, non déterministe, invérifiable en CI.

## 4. Décision

Option retenue : « Python, bibliothèque standard uniquement », parce que le garde-fou doit être exécutable partout sans installation et rester déterministe.
Le linter vit dans `scripts/lint-adr.py`, sans aucun import hors bibliothèque standard.
Toute évolution du template canonique se répercute dans le linter et son jeu de test dans la même passe (couplage vérifié en CI).

## 5. Conséquences

### Positives
- Le linter se branche en CI et en pre-commit sans étape d'installation.
- L'agent Copilot peut l'exécuter lui-même en fin de rédaction : la boucle rédige → lint → corrige est fermée.

### Négatives et compromis acceptés
- Le parsing markdown (tableaux, sections, blocs de code) est maison : chaque cas limite doit être couvert par le jeu de test témoin.
- Les règles de contenu (résumé en une phrase, gabarit) restent des heuristiques regex, avec leurs faux positifs potentiels.

## Références

- PV / source : cadrage du dépôt, commit « Phase 2 — linter d'ADR » du 2026-06-09.
- ADR liées : ADR-0002, ADR-0004.
