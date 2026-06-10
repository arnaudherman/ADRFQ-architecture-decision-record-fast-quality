# Génération d'ADR assistée par IA

Ce dépôt permet à une équipe d'architecture d'entreprise de produire des
**Architecture Decision Records (ADR)** de qualité, **en français**, directement
depuis **VS Code avec GitHub Copilot** — à partir d'un procès-verbal de séance
(PV) ou d'un simple sujet. La sortie est **un fichier markdown par décision**,
rangé dans `adr/`.

---

## 1. Objectif

Produire des ADR :

- **rapidement** — à partir d'un PV ou d'un échange de questions, sans repartir
  d'une page blanche ;
- **de qualité** — du vrai contenu (contexte, alternatives écartées, conséquences
  honnêtes), pas un gabarit rempli de placeholders ;
- **lisibles par l'IA** — chaque ADR porte en tête un bloc auto-suffisant (statut,
  périmètre, résumé) pour qu'un assistant connecté (MCP/RAG) puisse en consulter
  des centaines sans halluciner, notamment sans citer une décision périmée comme
  si elle était en vigueur.

---

## 2. Comment ça marche

Trois briques :

- **Un agent « questions d'abord »** (`prompt-agent-adr.md`) : il lit le PV,
  extrait ce qui est dit, repère les trous (surtout les alternatives écartées et
  les conséquences négatives — presque jamais dans un PV), **pose les questions,
  puis s'arrête**. Il ne rédige qu'une fois les trous comblés.
- **Un template canonique** (`template-adr-canonique.md`) : un noyau de sections
  toujours présent, dans le même ordre, plus des modules optionnels à emplacements
  fixes. Toutes les ADR se ressemblent.
- **Un linter** (`scripts/lint-adr.py`) : vérifie qu'une ADR respecte le format
  avant publication.

```
PV de séance ou sujet
        │
        ▼
Agent ADR (Copilot)   ── « questions d'abord » : extrait, demande ce qui manque, s'arrête
        │
        ▼   (réponses de l'architecte)
Rédaction Markdown    ── remplit le template canonique (noyau + modules)
        │
        ▼
adr/ADR-XXXX-titre.md ── en-tête auto-suffisant + corps, sans placeholder
        │
        ▼
Linter                ── garde-fou de conformité
```

Le **markdown est la source de vérité** de bout en bout. La mise sur une plateforme
(Confluence…) est **hors sujet** : la livraison du dépôt est le fichier ADR.

---

## 3. Créer une ADR (VS Code + GitHub Copilot)

### Prérequis

- VS Code avec **GitHub Copilot Chat**, connecté à GitHub.
- Le **mode Agent** de Copilot autorisé (une organisation peut le désactiver ; si
  `/adr-new` n'écrit aucun fichier, voir l'admin GitHub de l'organisation).
- Le dépôt **ouvert comme dossier de travail** (File ▸ Open Folder). À l'ouverture,
  `.github/copilot-instructions.md` est chargé automatiquement : le contexte ADR
  s'applique alors à tout le chat, sans rien faire.

### Étapes

1. Ouvrir **Copilot Chat** (Ctrl/Cmd+Alt+I) et vérifier que le mode est **Agent**
   (menu déroulant en haut de la vue de chat).
2. Lancer la commande : taper **`/adr-new`** dans le chat.
   Variante avec argument : `/adr-new chemin/vers/le-PV.md`.
3. **Fournir l'entrée** quand l'invite apparaît :
   - le chemin d'un **PV** présent dans le dépôt, ou
   - un **sujet** libre (ex. « Choix d'un bus d'événements pour le domaine
     commandes »), ou
   - **rien** → l'agent mène un entretien.
4. **Répondre aux questions.** L'agent résume ce qu'il a compris (3 à 5 puces), pose
   les questions pour combler les trous (en priorité alternatives écartées et
   conséquences négatives), annonce les modules optionnels, **puis s'arrête**.
   Répondre dans le chat, en plusieurs tours si besoin. Un point non tranché sera
   écrit « non tranché en séance », jamais inventé.
5. **Laisser rédiger.** Une fois les réponses obtenues, l'agent calcule le prochain
   ID libre et crée `adr/ADR-XXXX-<titre>.md`.
6. **Accepter le diff** (Keep / Accept) : en mode Agent, l'écriture du fichier passe
   par une validation manuelle.
7. **Vérifier** (recommandé) : lancer le linter (section 4).

### Bon à savoir

- L'agent **ne pose pas toujours les questions de lui-même** : ce comportement est
  imposé par les fichiers `.github`. S'il fonce vers la rédaction malgré tout,
  relancez-le en demandant explicitement de poser les questions d'abord, ou basculez
  le prompt en `agent: plan` pour la phase d'interrogation.
- **Sans Copilot** : `prompt-agent-adr.md` et `template-adr-canonique.md` sont du
  markdown autonome. N'importe quel assistant capable de lire les fichiers du dépôt
  peut reproduire le résultat ; Copilot est simplement la voie outillée.

---

## 4. Vérifier la qualité (linter)

```
python3 scripts/lint-adr.py                       # scanne tout le dossier adr/
python3 scripts/lint-adr.py adr/ADR-0002-xxx.md   # un fichier précis
```

Code de sortie **1** si au moins une ADR est non conforme. Le linter vérifie :

- la **Carte d'identité** et tous ses champs (ID, statut, date ISO, équipe,
  mots-clés, liens) ;
- le **statut** dans la liste fermée { Proposé, Accepté, Remplacé, Déprécié, Rejeté } ;
- le **résumé** en une phrase et au moins un **mot-clé** ;
- la présence des **sections du noyau** ;
- l'absence de **placeholder** ou de commentaire de gabarit `<!-- -->` ;
- la **réciprocité** des liens « Remplace » / « Remplacé par » entre ADR.

Aucune dépendance (bibliothèque standard Python). Idéal à brancher en pre-commit
ou en CI.

---

## 5. Le format canonique

Référence complète : `template-adr-canonique.md`. En résumé :

**Noyau — toujours présent, dans cet ordre, avec ces titres exacts**
1. Carte d'identité — 2. Résumé de la décision — 3. Contexte et problème —
4. Décision — 5. Conséquences.

**Modules optionnels — emplacements fixes**
- « Critères de décision » et « Options considérées » entre le Contexte (3) et la
  Décision (4) ;
- « Validation et suivi » et « Références » après les Conséquences (5).

On les inclut ou on les retire selon le poids de la décision, mais **on ne les
déplace ni ne les renomme jamais**.

**L'en-tête est le levier « lisible par l'IA »** : la Carte d'identité (statut,
périmètre, remplace / remplacé-par) + le résumé en une phrase forment un bloc
auto-portant qui dit *ce que fait* l'ADR et *si elle est encore valide*, sans tout
lire. Le **statut** est le garde-fou anti-hallucination n°1 (en cas de doute →
Proposé).

Exemple complet et conforme : `adr/ADR-0001-exemple.md`.

---

## 6. Structure du dépôt

```
.
├── README.md                     # ce document
├── template-adr-canonique.md     # template de référence (source de vérité)
├── prompt-agent-adr.md           # comportement de l'agent (source de vérité)
├── adr/                          # les ADR produites
│   └── ADR-0001-exemple.md       # exemple fictif (valide le rendu)
├── .github/                      # intégration GitHub Copilot (cible utilisateur)
│   ├── copilot-instructions.md   # contexte permanent, auto-appliqué
│   └── prompts/
│       └── adr-new.prompt.md     # commande /adr-new dans Copilot Chat
└── scripts/
    └── lint-adr.py               # linter d'ADR
```

---

## 7. Décisions de conception (à ne pas défaire sans raison)

1. **Uniformité par un noyau figé + modules optionnels.** Une personne d'une autre
   équipe doit retrouver Contexte → Décision → Conséquences au même endroit. Les
   modules s'insèrent dans des emplacements fixes ; on ne les déplace ni ne les
   renomme jamais.
2. **L'en-tête est le vrai levier « lisible par l'IA ».** La Carte d'identité + le
   résumé en une phrase forment un bloc auto-portant, analogue à la description d'un
   skill. Le **statut** est le garde-fou anti-hallucination n°1.
3. **Qualité = « questions d'abord ».** L'agent ne rédige pas sur des hypothèses
   inventées : il extrait, repère les trous (alternatives écartées, conséquences
   négatives), puis **demande** avant de rédiger.
4. **Sortie : un seul fichier `.md`, sans placeholder.** Une information manquante et
   non obtenue est écrite explicitement (« non tranché en séance »), jamais inventée.
5. **Un template unique** pour l'instant (pas de multi-template par équipe — voir
   questions ouvertes).

---

## 8. Périmètre

**Dans le périmètre**
- L'agent qui produit une ADR de qualité au format canonique.
- Les garde-fous de qualité et anti-hallucination (linter, validation des champs).

**Hors périmètre** (à ne pas implémenter sans demande)
- L'export / le formatage vers une plateforme (Confluence, etc.) : **hors sujet**.
  La livraison du dépôt est le fichier ADR markdown ; sa mise en plateforme ne nous
  concerne pas.
- Le support de plusieurs templates d'équipe. Envisagé, mais reporté : on
  standardise d'abord, on harmonisera l'existant ensuite si la gouvernance suit.
- La numérotation automatique inter-équipes et la gestion centralisée du statut
  « superseded ».

---

## 9. État et suite

**Construit** — exemple + format de référence ; agent rédacteur exposé dans Copilot
(`/adr-new`) ; linter de conformité.

**Différé / hors sujet** — multi-template par équipe (différé) ; export Confluence
(hors sujet).

**Pistes possibles** — brancher le linter en pre-commit / CI ; trancher les
questions ouvertes ci-dessous.

---

## 10. Questions ouvertes

- **Format de l'en-tête** : petit tableau (actuel) ou lignes étiquetées simples ?
  Facile à basculer ; le contenu des champs ne change pas.
- **Liste des statuts** : la liste fermée actuelle convient-elle, ou faut-il un état
  « En cours de revue » distinct de « Proposé » ?
- **Une ou plusieurs équipes** : reste-t-on sur un template unique (hypothèse
  actuelle) ou le multi-template deviendra-t-il nécessaire ?

---

## 11. Faire évoluer le format

Le **comportement** de l'agent et la **structure** des ADR sont du markdown, dans
deux fichiers qui font foi :

- `template-adr-canonique.md` — la structure (noyau + modules) ;
- `prompt-agent-adr.md` — le comportement (4 phases, qualité, anti-hallucination).

Toute évolution du format se fait dans ces deux fichiers. Pensez à répercuter le
changement dans `scripts/lint-adr.py` (les vérifications) et, si besoin, dans les
fichiers `.github/`. Lancez le linter après modification.

**Non-régression.** Le dossier `tests/fixtures/` contient un PV volontairement pauvre
et l'ADR de référence attendue (cas qui, en test réel, faisait halluciner l'agent :
résumé inventé, statut « Accepté » injustifié, banalités sur la techno, modules vides).
Après toute modification de `prompt-agent-adr.md`, `template-adr-canonique.md` ou des
fichiers `.github/`, rejouez le protocole décrit dans `tests/README.md`.

---

## 12. Références — dépôts d'inspiration

Repos évalués pendant le cadrage. Le template et le prompt s'en inspirent mais ne
les copient pas ; ils restent utiles comme référence d'implémentation.

**Retenus comme inspiration**

- `tomerariel/ai-adr` — https://github.com/tomerariel/ai-adr
  Agent « questions d'abord » (contexte, alternatives, compromis) avant rédaction,
  sortie au format MADR, templates default / lightweight. **Meilleure référence**
  pour l'agent rédacteur (questions d'abord, puis génération).

- `macromania/adr-agent` — https://github.com/macromania/adr-agent
  Même logique de questions de clarification, plus un pattern d'ancrage RAG (vector
  store) sur un référentiel. Utile si on veut, plus tard, ancrer le contenu sur un
  cadre interne.

- `me2resh/agent-decision-record` — https://github.com/me2resh/agent-decision-record
  On en a repris **une seule idée** : le résumé de décision en une phrase (« dans le
  contexte de X… nous avons décidé Z… en acceptant V »), réutilisé dans l'en-tête.
  Son frontmatter YAML n'a pas été retenu.

**Écartés (mentionnés pour mémoire)**

- `joshrotenberg/adrs` — https://github.com/joshrotenberg/adrs
  CLI Rust avec serveur MCP intégré et export JSON. Écarté : la consultation par
  l'IA passe déjà par le MCP Confluence existant, pas besoin d'un MCP dédié.

- `zircote/git-adr` — https://github.com/zircote/git-adr
  ADR stockées dans les git notes, rédaction assistée par IA annoncée mais non
  implémentée dans la réécriture Rust. Écarté pour cette raison.
