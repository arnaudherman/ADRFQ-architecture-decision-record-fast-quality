# Projet — Génération d'ADR assistée par IA

Document de passation. Lisible seul : il rappelle l'objectif, ce qui est
déjà fait, les décisions à respecter et la suite à construire. Destiné à
être repris par Claude Code.

---

## 1. Objectif

Permettre à une équipe d'architecture d'entreprise de produire des
**Architecture Decision Records (ADR)** :

- **rapidement** — à partir d'un procès-verbal de séance (PV) ou d'un
  échange de questions, sans repartir d'une page blanche ;
- **de qualité** — du vrai contenu (contexte, alternatives écartées,
  conséquences honnêtes), pas un gabarit rempli de placeholders ;
- **lisibles par l'IA** — chaque ADR porte en tête un bloc auto-suffisant
  pour qu'un assistant connecté (MCP/RAG) puisse en consulter des centaines
  sans halluciner, notamment sans citer une décision périmée comme si elle
  était en vigueur.

Les ADR sont rédigées **en français**.

---

## 2. État actuel

Deux artefacts de référence font foi :

- `template-adr-canonique.md` — la structure de référence d'une ADR.
- `prompt-agent-adr.md` — le comportement de l'agent qui rédige une ADR.

Outillage construit à ce jour :

- **Phase 0** — dépôt initialisé ; dossier `adr/` créé avec `ADR-0001` (exemple
  fictif exerçant noyau + modules pour valider le rendu du template).
- **Phase 1** — commande Claude Code `/adr-new`
  (`.claude/commands/adr-new.md`) : applique « questions d'abord », s'arrête au
  point de validation, puis génère un seul `.md` canonique dans `adr/`.
- **Phase 2** — linter `scripts/lint-adr.py` (Python, sans dépendance) :
  vérifie la Carte d'identité et ses champs, le statut (liste fermée), le
  résumé, les mots-clés, les sections du noyau, l'absence de placeholder et la
  cohérence des liens « Remplace » / « Remplacé par ». Lancer :
  `python3 scripts/lint-adr.py` (code de sortie 1 si une ADR est non conforme).

Reste à construire : les phases différées — export Confluence et multi-template
par équipe (voir section 7).

---

## 3. Le pipeline cible

```
PV de séance ou questions
        │
        ▼
Agent ADR  ── « questions d'abord » : extrait du PV, demande ce qui manque
        │
        ▼
Rédaction en Markdown ── remplit le template canonique (noyau + modules)
        │
        ▼
Fichier .md unique ── en-tête auto-suffisant + corps
        │
        ▼
(différé) Confluence ── collage manuel, consultation via MCP existant
```

Le **markdown est la source de vérité** de bout en bout. On ne cible
Confluence qu'à la toute fin, et cette partie est **hors périmètre pour
l'instant** (voir section 5).

---

## 4. Décisions prises (à ne pas défaire sans raison)

Ces choix sont le fruit de la phase de cadrage. Les conserver sauf décision
explicite.

1. **Uniformité par un noyau figé + modules optionnels.** Le noyau d'une ADR
   est toujours présent, dans le même ordre, avec les mêmes titres : une
   personne d'une autre équipe doit retrouver Contexte → Décision →
   Conséquences au même endroit. Les modules optionnels (Critères, Options,
   Validation, Références) s'insèrent dans des **emplacements fixes** ; on les
   inclut ou on les retire, jamais on ne les déplace ni ne les renomme.

2. **L'en-tête est le vrai levier « lisible par l'IA ».** La « Carte
   d'identité » (statut, périmètre, remplace/remplacé-par) + le résumé en une
   phrase forment un bloc auto-portant, analogue à la description d'un skill :
   il dit *ce que fait* l'ADR et *si elle est encore valide* sans tout lire.
   Le **statut** est le garde-fou anti-hallucination n°1.

3. **Qualité = « questions d'abord ».** L'agent ne rédige pas sur des
   hypothèses inventées. Il extrait ce que dit la source, repère les trous
   (surtout : alternatives écartées et conséquences négatives, presque jamais
   dans un PV), puis **demande** avant de rédiger.

4. **Sortie : un seul fichier `.md`, sans placeholder.** Si une information
   manque et n'est pas obtenue, l'agent l'écrit explicitement
   (« non tranché en séance ») au lieu de l'inventer.

5. **On part du template fourni.** Pas de support multi-template par équipe
   pour l'instant (voir questions ouvertes).

---

## 5. Périmètre

**Dans le périmètre maintenant**
- L'agent qui produit une ADR de qualité au format canonique.
- Les garde-fous de qualité et anti-hallucination (validation des champs).

**Hors périmètre pour l'instant** (à ne pas implémenter sans demande)
- L'export / le formatage vers Confluence (Cloud vs Data Center non tranché).
- Le support de plusieurs templates d'équipe (mapping de champs canoniques
  vers des templates existants). Envisagé, mais reporté : on standardise
  d'abord, on harmonisera l'existant ensuite si la gouvernance suit.
- La numérotation automatique inter-équipes et la gestion centralisée du
  statut « superseded ».

---

## 6. Fichiers du projet

| Fichier | Rôle | Stabilité |
|---|---|---|
| `template-adr-canonique.md` | Structure de référence d'une ADR (noyau + modules) | Source de vérité |
| `prompt-agent-adr.md` | Comportement de l'agent rédacteur | Source de vérité |
| `README.md` | Ce document de passation et de plan | Vivant |

---

## 7. Feuille de route (par phases, avec points de validation)

Approche incrémentale : chaque phase se termine par un point de validation
avant de passer à la suivante.

### Phase 0 — Mise en place
- Initialiser la structure du dépôt (proposition ci-dessous).
- Intégrer les deux fichiers existants tels quels.
- Créer un dossier `adr/` qui accueillera les ADR produites, avec un exemple
  `ADR-0001` fictif pour valider le rendu du template.
- **Validation :** le template se lit bien, l'exemple respecte le noyau.

### Phase 1 — Agent utilisable
- Transformer `prompt-agent-adr.md` en commande Claude Code (slash command
  ou skill) qui : prend un PV en entrée, applique « questions d'abord »,
  s'arrête au point de validation, puis génère un seul `.md` au format
  canonique dans `adr/`.
- **Validation :** sur un PV réel, l'agent pose les bonnes questions avant de
  rédiger, et la sortie ne contient aucun placeholder.

### Phase 2 — Garde-fous de qualité (linter d'ADR)
- Écrire un script de validation léger qui, pour chaque ADR de `adr/`,
  vérifie :
  - présence de la Carte d'identité et de tous ses champs ;
  - statut ∈ liste fermée { Proposé, Accepté, Remplacé, Déprécié, Rejeté } ;
  - présence du résumé en une phrase et d'au moins un mot-clé ;
  - présence des sections du noyau ;
  - cohérence des liens « Remplace » / « Remplacé par » entre ADR.
- **Validation :** le linter détecte une ADR volontairement incomplète.

### Phase 3 — différé : export Confluence
- Décliner le `.md` en format collable sur Confluence. Dépend du choix
  Cloud vs Data Center (non tranché).

### Phase 4 — différé : multi-template par équipe
- Définir un dictionnaire de champs canoniques et un mécanisme de mapping
  pour que l'agent produise dans le template d'une équipe tout en garantissant
  la présence des champs de l'en-tête.

---

## 8. Structure de dépôt proposée

À adapter aux conventions du dépôt cible.

```
.
├── README.md                     # ce document
├── template-adr-canonique.md     # template de référence
├── prompt-agent-adr.md           # comportement de l'agent
├── adr/                          # les ADR produites
│   └── ADR-0001-exemple.md
├── .claude/
│   └── commands/
│       └── adr-new.md            # commande agent (phase 1)
└── scripts/
    └── lint-adr.*                # linter d'ADR (phase 2)
```

Choix du langage du linter (Python ou Node) : à aligner sur les conventions
du dépôt d'accueil. Aucune dépendance lourde requise — c'est de la lecture de
markdown.

---

## 9. Questions ouvertes

- **Format de l'en-tête** : petit tableau (actuel) ou lignes étiquetées
  simples ? Facile à basculer ; le contenu des champs ne change pas.
- **Liste des statuts** : la liste fermée actuelle convient-elle, ou faut-il
  un état « En cours de revue » distinct de « Proposé » ?
- **Une ou plusieurs équipes** : confirme si l'on reste sur un template unique
  (hypothèse actuelle) ou si la phase 4 deviendra nécessaire.

---

## 10. Pour démarrer (Claude Code)

1. Lire `template-adr-canonique.md` et `prompt-agent-adr.md` : ce sont les
   spécifications de comportement, pas seulement des exemples.
2. Exécuter la **phase 0**, puis s'arrêter pour validation avant la phase 1.
3. Ne rien implémenter de la section « hors périmètre » sans demande explicite.
4. Respecter les décisions de la section 4 ; toute remise en cause doit être
   signalée plutôt que faite silencieusement.

---

## 11. Références — dépôts d'inspiration

Repos évalués pendant le cadrage. Le template et le prompt s'en inspirent
mais ne les copient pas ; ils restent utiles comme référence d'implémentation.

**Retenus comme inspiration**

- `tomerariel/ai-adr` — https://github.com/tomerariel/ai-adr
  Plugin Claude Code : agent « questions d'abord » (contexte, alternatives,
  compromis) avant rédaction, sortie au format MADR, templates default /
  lightweight. **Meilleure référence pour la phase 1** (l'agent comme commande
  Claude Code). NB : le README du repo affiche `owner/ai-adr` dans l'install,
  c'est un placeholder — utiliser `tomerariel/ai-adr`.

- `macromania/adr-agent` — https://github.com/macromania/adr-agent
  Même logique de questions de clarification, plus un pattern d'ancrage RAG
  (vector store) sur un référentiel. Utile si on veut, plus tard, ancrer le
  contenu sur un cadre interne.

- `me2resh/agent-decision-record` — https://github.com/me2resh/agent-decision-record
  On en a repris **une seule idée** : le résumé de décision en une phrase
  (« dans le contexte de X… nous avons décidé Z… en acceptant V »), réutilisé
  dans l'en-tête. Son frontmatter YAML n'a pas été retenu (inutile hors d'un
  dépôt de fichiers).

**Écartés (mentionnés pour mémoire)**

- `joshrotenberg/adrs` — https://github.com/joshrotenberg/adrs
  CLI Rust avec serveur MCP intégré et export JSON. Écarté : la consultation
  par l'IA passe déjà par le MCP Confluence existant, pas besoin d'un MCP dédié.

- `zircote/git-adr` — https://github.com/zircote/git-adr
  ADR stockées dans les git notes, rédaction assistée par IA annoncée mais non
  implémentée dans la réécriture Rust. Écarté pour cette raison.
