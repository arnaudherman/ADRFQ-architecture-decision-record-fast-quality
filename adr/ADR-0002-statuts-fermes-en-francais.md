# ADR-0002 — Utiliser une liste fermée de cinq statuts en français

## 1. Carte d'identité

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-0002 |
| Statut             | Accepté |
| Date de décision   | 2026-06-09 |
| Équipe / périmètre | Ce dépôt — format canonique des ADR |
| Mots-clés          | statut, vocabulaire fermé, anti-hallucination, cycle de vie |
| Remplace           | — |
| Remplacé par       | — |

## 2. Résumé de la décision

> **[ADR-0002 — Accepté]** Dans le contexte d'ADR destinées à être consultées en masse par des assistants IA, face au risque qu'une décision périmée soit citée comme en vigueur, nous avons décidé de fermer le champ Statut sur cinq valeurs françaises { Proposé, Accepté, Remplacé, Déprécié, Rejeté } afin d'obtenir un garde-fou vérifiable mécaniquement par le linter, en acceptant la rigidité d'un vocabulaire non extensible.

## 3. Contexte et problème

Le statut est le premier champ qu'un assistant IA doit lire : il dit si la décision est encore valide.
Le standard dominant MADR laisse ce champ en texte libre (`proposed | rejected | … | superseded by ADR-0123`), ce qui invite à inventer des statuts et rend toute vérification mécanique impossible.
Un corpus dont le statut n'est pas fiable produit exactement l'hallucination que ce dépôt combat : une décision morte citée comme vivante.

## Critères de décision

- Vérifiabilité mécanique par le linter (liste fermée = comparaison exacte).
- Lisibilité immédiate pour une équipe francophone.
- Couverture du cycle de vie réel d'une décision (proposition, adoption, remplacement, abandon, rejet).

## Options considérées

### Option 1 — Liste fermée de cinq statuts en français _(retenue)_
- Pour : vérifiable mécaniquement ; cohérente avec un corpus rédigé en français ; couvre le cycle de vie complet.
- Contre : vocabulaire non extensible sans modifier template et linter ; nécessite une table de correspondance vers l'anglais pour les outils du marché.

### Option 2 — Statut en texte libre (approche MADR) _(écartée)_
- Pour : souplesse totale ; compatibilité de fait avec l'écosystème MADR.
- Contre : invérifiable mécaniquement ; la relation de remplacement encodée dans une chaîne libre n'est ni structurée ni réciproque ; dérive garantie sur des centaines d'ADR.

### Option 3 — Statuts anglais standard (proposed, accepted…) _(écartée)_
- Pour : compréhension directe par les outils ADR anglo-saxons.
- Contre : rupture de langue au milieu d'ADR entièrement françaises ; le gain outillage est obtenu à moindre coût par une simple table de correspondance FR → EN.

## 4. Décision

Option retenue : « Liste fermée de cinq statuts en français », parce que c'est la seule qui rend le garde-fou n°1 vérifiable mécaniquement tout en restant cohérente avec un corpus francophone.
Le champ Statut de la Carte d'identité accepte exactement { Proposé, Accepté, Remplacé, Déprécié, Rejeté }.
Le linter rejette toute autre valeur.
« Accepté » n'est posé que sur preuve (vote ou validation nominative) ; en cas de doute, « Proposé ».

## 5. Conséquences

### Positives
- Le linter vérifie le statut par comparaison exacte : aucun état exotique ne peut entrer dans le corpus.
- La cohérence statut ↔ liens de remplacement devient elle aussi vérifiable (une ADR « Remplacé par » ne peut pas rester « Accepté »).

### Négatives et compromis acceptés
- Tout besoin d'état nouveau (ex. « En cours de revue ») impose de faire évoluer template, linter et jeu de test ensemble.
- Les outils ADR du marché attendent des statuts anglais : la table de correspondance FR → EN doit être documentée.

## Validation et suivi

- Indicateur de réussite : zéro statut hors liste dans le corpus (vérifié en continu par le linter en CI).
- Revue prévue le : —
- À rouvrir si : le besoin d'un statut « En cours de revue », distinct de « Proposé », se confirme à l'usage (question ouverte du README).

## Références

- PV / source : cadrage du dépôt, commits « Phase 0 » à « Phase 2 » du 2026-06-09.
- ADR liées : ADR-0004.
