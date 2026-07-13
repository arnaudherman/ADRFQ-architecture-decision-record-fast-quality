---
applyTo: "adr/**/*.md"
description: Invariants du format canonique — s'appliquent à TOUTE édition d'une ADR, même hors /adr-new
---

Tu édites une **ADR au format canonique** de ce dépôt. Ces invariants s'appliquent quelle
que soit la demande (retouche, changement de statut, correction) :

- **Structure figée.** Noyau dans cet ordre avec ces titres exacts : `1. Carte d'identité`,
  `2. Résumé de la décision`, `3. Contexte et problème`, `4. Décision`, `5. Conséquences`.
  Modules optionnels à emplacements fixes (« Critères de décision », « Options considérées »
  entre 3 et 4 ; « Validation et suivi », « Références » après 5). On ne renomme, ne
  réordonne, ne déplace jamais.
- **Statut** dans la liste fermée { Proposé, Accepté, Remplacé, Déprécié, Rejeté }.
  Passage à « Accepté » **uniquement** sur preuve donnée par l'architecte (vote, validation
  nominative) ; en cas de doute → « Proposé ». **La preuve vit dans « Validé par »** :
  Accepté/Rejeté ⇒ renseigné, Proposé ⇒ « — » ; une « Remplacé » conserve sa valeur d'origine.
- **Le préfixe du résumé suit le statut.** Tout changement d'ID ou de statut dans la Carte
  d'identité se répercute sur le préfixe `**[ADR-XXXX — Statut]**` du bloc résumé, et
  réciproquement.
- **Une ADR « Accepté » ne se modifie pas sur le fond, elle se remplace** (`/adr-remplace`).
  Corrections de forme (typo, lien cassé) : oui. Changer la décision, les options ou les
  conséquences : non — propose un remplacement.
- **Remplacement réciproque.** « Remplace » et « Remplacé par » vont toujours par paire
  entre les deux ADR, et une ADR avec « Remplacé par » renseigné porte le statut « Remplacé »
  (ou « Déprécié »).
- **Rien d'inventé.** Information absente → « non documenté en séance » (ou « à ce stade »
  en entretien sans séance) dans le corps, « — » dans les champs de la Carte d'identité qui
  l'admettent (Date de décision, Validé par, Remplace, Remplacé par — Équipe/périmètre et
  Mots-clés exigent un contenu réel). Jamais de
  placeholder `[à compléter]`, jamais de commentaire `<!-- -->`.
- **Après toute édition**, exécute `python3 scripts/lint-adr.py adr/` et corrige les
  erreurs signalées (au maximum deux passes, sinon montre-les).
