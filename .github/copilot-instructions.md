# Instructions de dépôt — Rédaction d'ADR (équipe d'architecture d'entreprise)

Ce dépôt sert à produire des **Architecture Decision Records (ADR)** de haute qualité,
**en français**, dans une **structure canonique figée**. La sortie attendue est **un seul
fichier markdown** dans le dossier `adr/`. La publication (Confluence) est **hors périmètre**.

## Sources de vérité — à lire et respecter intégralement

Avant toute rédaction d'ADR, lis et applique ces deux fichiers du dépôt. Ils **font foi**.
En cas de conflit avec les présentes instructions, **ces fichiers priment**.

- **Comportement** (déroulé en 4 phases, « questions d'abord », règles de qualité,
  règles anti-hallucination) : [prompt-agent-adr.md](../prompt-agent-adr.md)
- **Structure** (noyau figé dans un ordre fixe + modules optionnels à emplacements fixes) :
  [template-adr-canonique.md](../template-adr-canonique.md)

Tu appliques le comportement du premier en remplissant la structure du second.
Un exemple de rendu conforme est disponible : [adr/ADR-0001-exemple.md](../adr/ADR-0001-exemple.md).

## Comportement attendu (rappel — la source détaillée reste prompt-agent-adr.md)

- **Langue : français.** Tout l'ADR, sans exception.
- **Les questions d'abord.** Tu ne rédiges **jamais** une ADR à partir d'hypothèses inventées.
  Quand une information manque, tu la **demandes**. Tu ne combles un trou par déduction
  que si elle est évidente, et tu la signales (« je suppose X, corrige si besoin »).
- **Point de validation impératif.** Après la phase d'analyse (extraction + identification
  des trous), tu présentes : (1) un résumé de ce que tu as compris (3 à 5 puces) ;
  (2) la liste des questions, en priorité **alternatives écartées** et **conséquences
  négatives / compromis acceptés** ; (3) les modules optionnels que tu comptes activer
  et pourquoi. **Puis tu t'ARRÊTES et tu attends les réponses. Tu ne rédiges pas l'ADR avant.**
- **Point laissé ouvert.** Si l'architecte choisit de ne pas trancher un point, tu l'écris
  explicitement « non tranché en séance » dans l'ADR, plutôt que de l'inventer.

## Structure et sélection des modules (rappel — détail dans template-adr-canonique.md)

- Le **noyau est toujours présent**, dans cet ordre, avec ces titres exacts :
  1. Carte d'identité — 2. Résumé de la décision — 3. Contexte et problème —
  4. Décision — 5. Conséquences. **On ne renomme ni ne réordonne jamais le noyau.**
- Les **modules optionnels** occupent des emplacements fixes : « Critères de décision »
  et « Options considérées » entre le Contexte (3) et la Décision (4) ; « Validation et suivi »
  et « Références » après les Conséquences (5). On les inclut ou on les retire, jamais on ne les déplace.
- Sélection selon le poids de la décision : décision légère / réversible → noyau seul ;
  arbitrage entre options → ajoute « Critères de décision » + « Options considérées » ;
  décision structurante / coûteuse à défaire → ajoute en plus « Validation et suivi » ;
  toujours, si une source existe → ajoute « Références ».

## Règles de qualité (ce qui fait une bonne ADR)

- Le **résumé en une phrase est auto-portant** : il contient la décision *et* le pourquoi.
  Gabarit : « Dans le contexte de X, face à Y, nous avons décidé Z afin d'obtenir W, en acceptant V. »
- Le **contexte explique le POURQUOI**, lisible par quelqu'un d'extérieur à l'équipe.
  Tout sigle ou terme interne est explicité une fois.
- Les **options écartées valent autant que l'option retenue** : un vrai « contre », pas un repoussoir.
- Les **conséquences sont honnêtes** : toujours une face négative ou un compromis assumé.
- **Aucun placeholder dans la sortie finale.** Section non remplissable → tu poses la question,
  ou tu écris explicitement « non documenté en séance ».

## Règles anti-hallucination (ces ADR seront consultées en masse par un MCP/RAG)

- Le **statut** appartient à la liste fermée { Proposé, Accepté, Remplacé, Déprécié, Rejeté }
  et est rempli sans ambiguïté. **En cas de doute, statut = Proposé** (jamais « Accepté » par défaut).
- Si la décision en **remplace** une autre, renseigne « Remplace » dans le nouvel ADR et
  propose la mise à jour de « Remplacé par » dans l'ADR visée (les deux côtés, quand l'info existe).
- Les **mots-clés** sont concrets (techno, composant, domaine métier) pour la recherche sémantique.
- **Tu n'inventes jamais un ID, une date ou un lien d'ADR.** Champ inconnu → tu demandes
  ou tu laisses un marqueur explicite à compléter par l'architecte.

## Format et nommage du fichier de sortie

- **Un seul fichier** : `adr/ADR-XXXX-<titre-court-en-kebab-case>.md`.
- **ID** : prochain numéro libre au format `ADR-XXXX` (4 chiffres) en scannant le dossier `adr/`.
  L'exemple `ADR-0001` compte ; ne réutilise jamais un ID existant.
- **Contenu** : template canonique rempli, **sans aucun commentaire `<!-- -->`**,
  **sans aucun placeholder de gabarit**, en français.
