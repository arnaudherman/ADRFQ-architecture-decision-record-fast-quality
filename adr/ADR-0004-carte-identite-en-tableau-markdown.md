# ADR-0004 — Porter les métadonnées dans un tableau markdown, pas un frontmatter YAML

## 1. Carte d'identité

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-0004 |
| Statut             | Accepté |
| Date de décision   | 2026-06-09 |
| Équipe / périmètre | Ce dépôt — format canonique des ADR |
| Mots-clés          | carte d'identité, tableau markdown, frontmatter, métadonnées, source de vérité |
| Remplace           | — |
| Remplacé par       | — |

## 2. Résumé de la décision

> **[ADR-0004 — Accepté]** Dans le contexte d'un en-tête d'ADR lu à la fois par des humains et par des assistants IA, face au choix entre tableau markdown et frontmatter YAML pour porter les métadonnées, nous avons décidé de tout porter dans le tableau « Carte d'identité » afin d'obtenir une source de vérité unique lisible dans n'importe quel rendu markdown, en acceptant que les outils ADR du marché, qui attendent du frontmatter, ne parsent pas notre en-tête sans une petite spécification dédiée.

## 3. Contexte et problème

Les métadonnées d'une ADR (statut, dates, liens de remplacement) doivent être lisibles par un humain pressé et extractibles par un outil.
Deux conventions existent : le frontmatter YAML (MADR 4.x, la plupart des outils récents) et le tableau dans le corps du document.
Dupliquer les deux garantirait leur divergence ; le frontmatter seul disparaît du rendu de nombreux visualiseurs markdown et impose YAML à des architectes non-développeurs.
Le frontmatter YAML du dépôt d'inspiration me2resh/agent-decision-record avait d'ailleurs été écarté dès le cadrage.

## Critères de décision

- Une seule source de vérité par métadonnée (jamais de duplication).
- Lisibilité humaine dans tout rendu markdown (GitHub, VS Code, visualiseurs internes).
- Extraction machine possible par expressions régulières simples et stables.

## Options considérées

### Option 1 — Tableau markdown « Carte d'identité » _(retenue)_
- Pour : visible dans tout rendu ; éditable sans connaître YAML ; parsable par regex simples que le linter fige et vérifie.
- Contre : convention locale — les outils ADR du marché ne la reconnaissent pas sans adaptation.

### Option 2 — Frontmatter YAML (approche MADR 4.x) _(écartée)_
- Pour : convention dominante de l'outillage récent ; parsable par toute bibliothèque YAML.
- Contre : invisible ou brut dans plusieurs rendus markdown ; impose la syntaxe YAML aux rédacteurs ; MADR note lui-même que le rendu n'est pas standardisé entre parseurs.

### Option 3 — Tableau ET frontmatter dupliqués _(écartée)_
- Pour : lisibilité humaine et compatibilité outillage en même temps.
- Contre : deux sources de vérité pour chaque champ — la divergence n'est qu'une question de temps, et le linter devrait vérifier la cohérence en permanence.

## 4. Décision

Option retenue : « Tableau markdown « Carte d'identité » », parce qu'une source de vérité unique et lisible partout prime sur la compatibilité immédiate avec un outillage que le dépôt n'utilise pas.
Toutes les métadonnées vivent dans le tableau de la section « 1. Carte d'identité », complété par le préfixe de validité du résumé.
Si un consommateur MCP/RAG exige un jour du frontmatter, il sera **dérivé** du tableau par un script (une projection, jamais une seconde source).

## 5. Conséquences

### Positives
- L'en-tête est lisible tel quel par un humain dans tout rendu markdown, sans outillage.
- Le linter parse la carte avec des regex stables, figées comme spécification de parsabilité du format.

### Négatives et compromis acceptés
- Les outils ADR du marché (parsers frontmatter, statuts anglais) ne lisent pas ce format : un consommateur maison doit suivre la spécification de parsabilité du dépôt.
- Le parsing des tableaux markdown (cellules, pipes échappés) doit être maintenu dans le linter.

## Références

- PV / source : cadrage du dépôt (README, « Références — dépôts d'inspiration » : frontmatter YAML de me2resh/agent-decision-record non retenu), commits du 2026-06-09.
- ADR liées : ADR-0002, ADR-0003.
