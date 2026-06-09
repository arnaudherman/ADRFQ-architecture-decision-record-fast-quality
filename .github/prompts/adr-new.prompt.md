---
description: Rédige un ADR de qualité (questions d'abord) à partir d'un PV ou en entretien, au format canonique
name: adr-new
argument-hint: [chemin/vers/PV.md] | [sujet de la décision] | (vide → entretien)
agent: agent
---

Tu rédiges un **Architecture Decision Record (ADR)** pour l'équipe d'architecture
d'entreprise. ADR **en français**, de haute qualité, dans la structure canonique.
La sortie attendue est **un seul fichier markdown** dans `adr/`. La publication
(Confluence) est **hors périmètre**.

## Sources de vérité — à lire MAINTENANT et à respecter intégralement

Avant toute chose, lis ces deux fichiers du dépôt. Ils **font foi**. En cas de conflit
avec ce qui suit, **ces fichiers priment**.

- **Comportement** (déroulé en 4 phases, règles de qualité et anti-hallucination) :
  [prompt-agent-adr.md](../../prompt-agent-adr.md)
- **Structure** (noyau figé + modules à emplacements fixes) :
  [template-adr-canonique.md](../../template-adr-canonique.md)

Un exemple de rendu conforme : [adr/ADR-0001-exemple.md](../../adr/ADR-0001-exemple.md).

Tu appliques le comportement du premier en remplissant la structure du second.

## Entrée

Argument reçu : « ${input:entree:Chemin du PV, sujet de la décision, ou laisse vide pour un entretien} »

- **Chemin de fichier existant** → c'est le PV de séance. Lis-le, puis applique les 4 phases.
- **Texte libre (un sujet)** → pas de PV : démarre directement en phase 2, sous forme
  d'entretien (questions par petits groupes) jusqu'à pouvoir rédiger.
- **Vide** → demande à l'architecte de coller le PV ou de nommer le sujet, puis continue.

## Déroulé

### Phases 1 et 2 — Extraction puis analyse des manques

Extrais ce qui est **explicitement présent** dans la source (problème, options débattues,
décision et qui l'a prise, raisonnement, conséquences). Ne déduis rien à ce stade.
Compare au template canonique et identifie les **trous** — surtout : alternatives écartées
et leur « pourquoi pas », conséquences négatives / compromis, statut réel, périmètre,
liens avec une décision remplacée.

### Point de validation — IMPÉRATIF, NE PAS SAUTER

À la fin de la phase 2, présente dans le chat :

1. **ce que tu as compris** (3 à 5 puces) ;
2. les **questions nécessaires** pour combler les trous — en priorité **alternatives
   écartées** et **conséquences négatives / compromis acceptés** ;
3. les **modules optionnels** que tu comptes activer et pourquoi.

**Puis ARRÊTE-TOI et attends les réponses de l'architecte. N'écris AUCUN fichier ADR
tant que les trous bloquants ne sont pas comblés.** Même si tu juges avoir assez de
contexte, tu poses d'abord les questions et tu attends. Si l'architecte laisse un point
ouvert, écris « non tranché en séance » dans l'ADR plutôt que de l'inventer.

### Phases 3 et 4 — Sélection des modules, rédaction et écriture du fichier

Une fois les réponses reçues et les trous comblés :

1. **ID** : scanne le dossier `adr/` et prends le **prochain numéro libre** au format
   `ADR-XXXX` (4 chiffres). L'exemple `ADR-0001` compte ; ne réutilise jamais un ID.
2. **Modules** : noyau toujours présent ; ajoute « Critères de décision » + « Options
   considérées » s'il y a arbitrage ; ajoute « Validation et suivi » si la décision est
   structurante ; ajoute « Références » dès qu'une source existe. Ne déplace jamais une section.
3. **Fichier** : écris **un seul** fichier `adr/ADR-XXXX-<titre-court-en-kebab-case>.md`
   via l'outil d'édition.
4. **Contenu** : template canonique rempli, **sans aucun commentaire `<!-- -->`**,
   **sans aucun placeholder**, en français. Le résumé en une phrase est auto-portant
   (décision + pourquoi). Les conséquences incluent toujours une face négative.
5. **Garde-fous** : statut dans { Proposé, Accepté, Remplacé, Déprécié, Rejeté } ; en cas
   de doute → **Proposé**. N'invente jamais ID, date ou lien d'ADR. Si la décision en
   remplace une autre, renseigne « Remplace » ici et propose la mise à jour de
   « Remplacé par » dans l'ADR visée.
6. Après écriture, n'affiche que le **chemin du fichier créé** et un récapitulatif d'une
   ligne (ID + titre + statut).
