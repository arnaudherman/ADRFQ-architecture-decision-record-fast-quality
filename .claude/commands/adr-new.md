---
description: Rédige un ADR de qualité (questions d'abord) à partir d'un PV ou en entretien, au format canonique
argument-hint: [chemin/vers/PV.md] | [sujet de la décision] | (vide → entretien)
---

Tu rédiges un **Architecture Decision Record (ADR)** pour l'équipe d'architecture
d'entreprise. ADR **en français**, de haute qualité, dans la structure canonique.

## Sources de vérité — à respecter intégralement

- **Comportement** (déroulé en 4 phases, règles de qualité et anti-hallucination) :
  @prompt-agent-adr.md
- **Structure** (noyau figé + modules à emplacements fixes) :
  @template-adr-canonique.md

Ces deux fichiers font foi. Tu appliques le comportement du premier en remplissant
la structure du second. En cas de conflit avec ce qui suit, ces fichiers priment.

## Entrée

Argument reçu : « $ARGUMENTS »

- **Chemin de fichier existant** → c'est le PV de séance. Lis-le, puis applique les 4 phases.
- **Texte libre (un sujet)** → pas de PV : démarre directement en phase 2, sous forme
  d'entretien (questions par petits groupes) jusqu'à pouvoir rédiger.
- **Vide** → demande à l'architecte de coller le PV ou de nommer le sujet, puis continue.

## Point de validation — impératif

À la fin de la **phase 2**, tu présentes :
1. ce que tu as compris (3 à 5 puces) ;
2. les questions nécessaires pour combler les trous — en priorité **alternatives
   écartées** et **conséquences négatives / compromis** ;
3. les modules optionnels que tu comptes activer et pourquoi.

**Puis tu t'ARRÊTES et tu attends les réponses. Tu ne rédiges pas l'ADR avant.**
Si l'architecte laisse un point ouvert, tu l'écris « non tranché en séance »
dans l'ADR plutôt que de l'inventer.

## Rédaction et sortie

Une fois les trous comblés (phases 3 et 4) :

1. **ID** : scanne le dossier `adr/` et prends le prochain numéro libre au format
   `ADR-XXXX` (4 chiffres). L'exemple `ADR-0001` compte ; ne réutilise jamais un ID.
2. **Fichier** : écris **un seul** `adr/ADR-XXXX-<titre-court-en-kebab-case>.md`.
3. **Contenu** : template canonique rempli, **sans aucun commentaire `<!-- -->`**,
   **sans placeholder**, en français.
4. **Garde-fous** : statut dans { Proposé, Accepté, Remplacé, Déprécié, Rejeté } ;
   en cas de doute → **Proposé**. N'invente jamais ID, date ou lien d'ADR.
   Si la décision en remplace une autre, renseigne « Remplace » ici et propose la
   mise à jour de « Remplacé par » dans l'ADR visée.
5. Après écriture, n'affiche que le **chemin du fichier créé** et un récapitulatif
   d'une ligne (ID + titre + statut).
