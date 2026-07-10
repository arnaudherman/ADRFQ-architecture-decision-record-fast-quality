---
description: Remplace une ADR existante par une nouvelle décision (les deux fichiers mis à jour dans la même passe, réciprocité garantie)
name: adr-remplace
argument-hint: [ADR-XXXX à remplacer] [sujet de la nouvelle décision]
agent: agent
---

Tu remplaces une **ADR existante** par une **nouvelle décision**, pour l'équipe
d'architecture d'entreprise. Le remplacement est une **transaction** : la nouvelle ADR
et l'ancienne sont mises à jour **dans la même passe**, jamais l'une sans l'autre.

## Sources de vérité — à lire MAINTENANT et à respecter intégralement

- **Comportement** : [prompt-agent-adr.md](../../prompt-agent-adr.md)
- **Structure** : [template-adr-canonique.md](../../template-adr-canonique.md)

En cas de conflit avec ce qui suit, **ces fichiers priment**.

## Entrée

L'entrée est le **texte qui suit `/adr-remplace`** : l'ID de l'ADR à remplacer
(`ADR-XXXX`), éventuellement suivi du sujet de la nouvelle décision. S'il manque l'ID,
demande-le avant toute chose.

## Préconditions — à vérifier AVANT d'agir

Lis l'ADR visée dans `adr/` et vérifie :

1. **Elle existe.** Sinon : signale-le et arrête-toi.
2. **Son statut est « Accepté » ou « Déprécié ».** Une ADR « Proposé » ne se remplace pas,
   elle s'amende dans la discussion ; une « Rejeté » n'est pas en vigueur ; signale et
   arrête-toi.
3. **Elle n'est pas déjà remplacée.** Si « Remplacé par » est déjà renseigné vers une autre
   ADR, **n'écrase jamais ce lien** : signale-le et arrête-toi.

## Questions ciblées (puis ARRÊT)

Avant de rédiger, pose ces questions — et **attends les réponses** :

1. **Pourquoi** la décision existante ne tient plus (fait déclencheur, contrainte nouvelle) ?
2. **Ce qui change** concrètement par rapport à l'ancienne décision ?
3. **Chemin de migration** : que devient l'existant construit sur l'ancienne décision
   (reprise, coexistence, date butoir) ?

Les règles de `/adr-new` s'appliquent (max 7 questions, alternatives écartées et
conséquences négatives en priorité, rien d'inventé).

## Transaction de remplacement

Une fois les réponses reçues :

1. **Nouvelle ADR** : prochain ID libre, template canonique rempli, **statut « Proposé »**
   — un remplacement ne s'auto-accepte **jamais** ; il sera accepté selon la même règle
   mécanique que toute ADR (vote ou validation nominative). Champ « Remplace : ADR-XXXX »
   renseigné. Le contexte explique pourquoi l'ancienne décision est remplacée.
2. **Ancienne ADR — trois retouches, rien d'autre** :
   - champ « Remplacé par » → l'ID de la nouvelle ;
   - champ « Statut » → « Remplacé » ;
   - préfixe de son résumé → `**[ADR-XXXX — Remplacé]**`.
   Tu ne touches ni au Contexte, ni à la Décision, ni aux Conséquences de l'ancienne :
   c'est un document d'archive, pas un brouillon.
3. **Vérification finale (obligatoire)** : `python3 scripts/lint-adr.py adr/` — la
   réciprocité Remplace/Remplacé-par et la cohérence des statuts y sont vérifiées.
   Corrige et relance, **au maximum deux passes** ; s'il reste des erreurs, montre-les.
4. Affiche un récapitulatif de deux lignes (ancienne : ID + « Remplacé » ; nouvelle :
   ID + titre + « Proposé »). **Puis arrête-toi.**

## Note sur le statut de l'ancienne

Le statut de la nouvelle ADR est « Proposé » tant qu'elle n'est pas validée — mais
l'ancienne passe à « Remplacé » **dès maintenant** : c'est la volonté exprimée par
l'architecte en lançant cette commande. S'il préfère attendre la validation de la
nouvelle avant de basculer l'ancienne, il le dira ; dans ce cas arrête-toi après la
nouvelle ADR et dis explicitement que l'ancienne reste inchangée (le linter refusera
le champ « Remplace » orphelin : retire-le alors de la nouvelle et note le lien dans
« Références / ADR liées » en attendant la validation).
