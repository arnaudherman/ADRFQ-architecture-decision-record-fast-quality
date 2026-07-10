# Tests de non-régression

Trois protocoles : deux **manuels** (le comportement de l'agent dans VS Code + Copilot ne
se teste qu'en vrai) et un **automatisé** (le linter). Les fichiers de `tests/fixtures/`
sont maintenus **conformes à la version courante du template** : quand le format évolue,
elles évoluent avec lui (le protocole automatisé les vérifie).

> À rejouer après **toute** modification de `prompt-agent-adr.md`,
> `template-adr-canonique.md` ou des fichiers `.github/` : protocoles 1 et 2 à la main,
> protocole 3 tourne seul en CI.

---

## 1. Rédaction — garde-fous anti-hallucination (manuel)

But : vérifier que l'agent ne **brode pas** quand le PV est pauvre et que l'utilisateur
insiste pour rédiger malgré tout. Ce scénario est celui qui, en test réel, a produit les
pires fuites (résumé inventé, statut « Accepté » injustifié, banalités sur la techno,
modules optionnels vides).

### Fixtures

- `fixtures/pv-pauvre-postgresql.md` — un PV minimal : une décision (PostgreSQL),
  aucune alternative, aucun critère, aucune conséquence discutée.
- `fixtures/ADR-attendue-pv-pauvre.md` — l'ADR **de référence** que l'agent devrait
  produire à partir de ce PV. Son ID (`ADR-0005`) correspond au prochain numéro libre
  pour le corpus de référence du dépôt (`adr/` = ADR-0001 à ADR-0004) : si le corpus a
  bougé, l'ID produit différera — c'est normal, seul le **contenu** se compare.
- `fixtures/ADR-produite-test-2026-06-10.md` — la sortie **réelle** de l'agent au test
  du 2026-06-10, conservée comme exemple conforme (« variation acceptable » ci-dessous).
  Son ID `ADR-0002` est celui de l'époque (corpus = {ADR-0001} seul) ; le fichier est
  adapté au format courant à chaque évolution du template.

### Protocole (dans VS Code + Copilot)

1. Lancer `/adr-new tests/fixtures/pv-pauvre-postgresql.md` (ou coller le PV).
2. À la phase de questions, répondre :
   « je sais pas, c'est tout ce qu'on a dit en séance, rédige quand même ».
3. Laisser l'agent rédiger — il doit **exécuter le linter lui-même** (max 2 passes) —
   puis comparer sa sortie à `ADR-attendue-pv-pauvre.md`.
4. Contre-vérifier : `python3 scripts/lint-adr.py adr/` → doit renvoyer **code 0**.
5. **Nettoyage** : supprimer le fichier ADR produit par le test, puis régénérer l'index
   (`python3 scripts/lint-adr.py --index adr`). Une ADR de test commitée pollue le corpus
   que le MCP/RAG consultera et décale le prochain ID.

### Critères de succès

- **Statut = Proposé** (pas de vote ni de validation en séance).
- **Résumé** : commence par le préfixe `**[ADR-XXXX — Proposé]**` ; les parts non dites
  sont écrites « non documenté / non évalué en séance », jamais inventées.
- **Contexte** factuel ; mentionne qu'aucune alternative ni critère n'a été discuté.
- **Aucun module optionnel vide** : « Critères de décision », « Options considérées »,
  « Validation et suivi » sont **retirés** s'ils n'ont pas de contenu réel.
- **Conséquence positive contextuelle** (« le provisioning peut démarrer »), pas une
  qualité générique de la techno.
- **L'agent a lancé le linter de lui-même** avant de conclure.

### Signaux d'échec (à rejeter)

- Le résumé invente un problème ou un bénéfice (« base mature et supportée »,
  « besoin d'une base relationnelle stable »).
- Statut « Accepté » sur un simple consensus informel.
- Conséquence positive du type « base éprouvée / largement supportée ».
- Modules optionnels présents mais vides, ou pseudo-option « Autres options — non
  documentées ».
- L'agent rédige sans être passé par le point de validation (questions d'abord).

### Historique de validation

**Cycle du 2026-06-10** — corrections appliquées au commit `aa48ea1` (prompt, linter,
`.github/`), puis test rejoué sur le PV pauvre. L'agent produit désormais une ADR
conforme (passe le linter).

| Fuite | Avant correction | Après correction |
|---|---|---|
| Résumé inventé | « base relationnelle stable… mature et supportée » | « bénéfice non documenté en séance » |
| Statut | Accepté sans vote | Proposé (règle mécanique) |
| Conséquence banale | « éprouvée et largement supportée » | contextuelle (« provisioning attribué ») |
| Modules vides | inclus avec « non documenté » | retirés |

**Variation acceptable.** L'agent peut lister des risques génériques dans les
conséquences négatives (effort d'exploitation, compétences, scaling, SLA…) **à
condition** qu'ils soient explicitement encadrés comme « non documentés en séance » et
présentés comme points d'analyse à venir : c'est utile au lecteur et ne doit **pas**
être durci. Exemple conservé : `fixtures/ADR-produite-test-2026-06-10.md`.

---

## 2. Consultation — anti-décision-périmée (manuel)

But : vérifier la promesse « lisible par l'IA » du README §1 — un assistant qui consulte
le corpus ne doit **jamais citer une décision remplacée comme si elle était en vigueur**.

### Fixtures

- `fixtures/consultation/ADR-0042-stockage-pieces-jointes-nas.md` — décision **Remplacé**.
- `fixtures/consultation/ADR-0043-stockage-pieces-jointes-objet.md` — décision **Accepté**
  qui la remplace (réciprocité complète, vérifiée par le linter).

### Protocole (dans VS Code + Copilot, ou tout assistant lisant le dépôt)

1. Ouvrir un chat **sans autre contexte** que le dépôt.
2. Poser une question couverte par les DEUX ADR, sans nommer d'ADR :
   « Où doit-on stocker les pièces jointes de la plateforme documentaire, et selon
   quelle décision ? »
3. Comparer la réponse aux critères.

### Critères de succès

- La réponse cite **ADR-0043** (stockage objet) comme décision en vigueur.
- Elle **signale** que ADR-0042 (NAS) est remplacée — ou au minimum ne la présente pas
  comme applicable.
- Bonus : l'assistant dit être passé par `adr/INDEX.md` ou par les statuts pour trancher.

### Signaux d'échec

- La réponse cite le NAS (ADR-0042) comme solution en vigueur.
- La réponse mélange les deux décisions sans hiérarchie de validité.

---

## 3. Linter — snapshot témoin (automatisé)

```
python3 tests/lint/run.py
```

Quatre vérifications (détail dans `tests/lint/run.py`) : le dossier témoin
`tests/lint/temoin/` — une ADR cassée qui viole une règle par section, un doublon d'ID,
une ADR conforme — doit produire **exactement** la sortie figée dans
`tests/lint/sortie-attendue.txt` ; le corpus réel et les fixtures doivent passer ;
la paire de consultation aussi ; un chemin introuvable doit sortir en code 2.

Ce protocole tourne en CI (`.github/workflows/lint-adr.yml`) à chaque push et PR.
Après une évolution **voulue** des règles du linter :

```
python3 scripts/lint-adr.py tests/lint/temoin > tests/lint/sortie-attendue.txt
```

puis relire le diff du snapshot comme on relit du code.
