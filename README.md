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
  périmètre, résumé préfixé par sa validité) et le corpus est résumé dans un index
  généré (`adr/INDEX.md`), pour qu'un assistant connecté (MCP/RAG) puisse en
  consulter des centaines sans halluciner, notamment sans citer une décision
  périmée comme si elle était en vigueur.

---

## 2. Comment ça marche

Trois briques :

- **Un agent « questions d'abord »** (`prompt-agent-adr.md`) : il lit le PV,
  extrait ce qui est dit, repère les trous (surtout les alternatives écartées et
  les conséquences négatives — presque jamais dans un PV), **pose les questions,
  puis s'arrête**. Il ne rédige qu'une fois les trous comblés — puis **exécute
  lui-même le linter** sur sa sortie et corrige (deux passes maximum).
- **Un template canonique** (`template-adr-canonique.md`) : un noyau de sections
  toujours présent, dans le même ordre, plus des modules optionnels à emplacements
  fixes. Toutes les ADR se ressemblent.
- **Un linter** (`scripts/lint-adr.py`) : vérifie qu'une ADR respecte le format —
  structure, champs, cohérence des statuts et des liens de remplacement — et
  génère l'index de consultation. Il tourne **trois fois** : lancé par l'agent en
  fin de rédaction, disponible à la main, et **en CI** à chaque push et PR.

```
PV de séance ou sujet
        │
        ▼
Agent ADR (Copilot)     ── « questions d'abord » : extrait, demande ce qui manque, s'arrête
        │
        ▼   (réponses de l'architecte)
Rédaction Markdown      ── remplit le template canonique (noyau + modules)
        │
        ▼
adr/ADR-XXXX-titre.md   ── en-tête auto-suffisant + corps, sans placeholder
        │
        ▼
Linter (par l'agent)    ── corrige jusqu'à zéro erreur, max 2 passes
        │
        ▼
CI (push / PR)          ── linter + tests + fraîcheur de adr/INDEX.md
```

Le **markdown est la source de vérité** de bout en bout. La mise sur une plateforme
(Confluence…) est **hors sujet** : la livraison du dépôt est le fichier ADR.

---

## 3. Créer une ADR (VS Code + GitHub Copilot)

### Prérequis

- VS Code avec **GitHub Copilot Chat**, connecté à GitHub.
- Le **mode Agent** de Copilot autorisé (une organisation peut le désactiver —
  vérifier à l'étape 1 que « Agent » figure bien dans le menu ; sinon, voir
  l'admin GitHub de l'organisation).
- **Python 3** sur le poste (préinstallé sur macOS/Linux ; sur Windows, `py -3`) :
  l'agent s'en sert pour lancer le linter.
- Le dépôt **ouvert comme dossier de travail** (File ▸ Open Folder). À l'ouverture,
  `.github/copilot-instructions.md` est chargé automatiquement : le contexte ADR
  s'applique alors à tout le chat, sans rien faire.

### Étapes

1. Ouvrir **Copilot Chat** (Ctrl/Cmd+Alt+I) et vérifier que le mode est **Agent**
   (menu déroulant en haut de la vue de chat).
2. Lancer la commande : taper **`/adr-new`** dans le chat.
   Variante avec argument : `/adr-new chemin/vers/le-PV.md`.
3. **Fournir l'entrée** si l'agent la demande :
   - le chemin d'un **PV** présent dans le dépôt, ou
   - un **sujet** libre (ex. « Choix d'un bus d'événements pour le domaine
     commandes »), ou
   - **rien** → l'agent mène un entretien.
4. **Répondre aux questions.** L'agent résume ce qu'il a compris (3 à 5 puces) —
   et liste les décisions s'il en repère plusieurs (une ADR chacune) —, pose les
   questions pour combler les trous (en priorité alternatives écartées et
   conséquences négatives), annonce les modules optionnels, **puis s'arrête**.
   Répondre dans le chat, en plusieurs tours si besoin. Un point non tranché sera
   écrit « non tranché en séance », jamais inventé.
5. **Laisser rédiger et vérifier.** L'agent calcule le prochain ID libre, crée
   `adr/ADR-XXXX-<titre>.md`, puis **lance le linter et corrige** ce qu'il signale
   (deux passes maximum — au-delà, il montre les erreurs restantes).
6. **Accepter le diff** (Keep / Accept) : en mode Agent, l'écriture du fichier passe
   par une validation manuelle.
7. **Régénérer l'index** si l'agent ne l'a pas fait :
   `python3 scripts/lint-adr.py --index adr` (la CI échoue si l'index est périmé).

### En cas d'ADR non conforme

Si le linter signale des erreurs après coup : **demander à l'agent, dans le même
chat, de corriger le fichier existant**. Ne pas relancer `/adr-new` — la commande
est conçue pour créer, elle produirait une **deuxième ADR** avec un nouvel ID à
côté de la défectueuse.

### Remplacer une décision existante

Une ADR « Accepté » ne se modifie pas : elle se **remplace**. Taper
**`/adr-remplace ADR-XXXX <sujet>`** : l'agent vérifie les préconditions, pose ses
questions, écrit la nouvelle ADR (« Remplace ») **et** met à jour l'ancienne
(« Remplacé par », statut → « Remplacé ») dans la même passe, puis re-vérifie la
réciprocité au linter.

### Quand ne PAS créer une ADR

Le corpus est consulté en masse par l'IA : le polluer de pseudo-décisions dégrade
toutes les réponses. Pas d'ADR pour : un détail d'implémentation local, un
contournement temporaire, une convention de style, une décision sans impact au-delà
de l'équipe qui la prend. En cas de doute : est-ce qu'une autre équipe (ou un
assistant IA) aura besoin de savoir *pourquoi* dans un an ? Non → pas d'ADR.

### Bon à savoir

- L'agent **ne pose pas toujours les questions de lui-même** : ce comportement est
  imposé par les fichiers `.github`, mais reste une instruction que le modèle peut
  rater. S'il fonce vers la rédaction, relancez-le en demandant explicitement de
  poser les questions d'abord — c'est le remède sans risque.
- **Édition manuelle d'une ADR** : les invariants du format s'appliquent aussi hors
  `/adr-new` — `.github/instructions/adr.instructions.md` (portée `adr/**`) les
  rappelle à Copilot à chaque édition.
- **Sans Copilot** : `prompt-agent-adr.md` et `template-adr-canonique.md` sont du
  markdown autonome. N'importe quel assistant capable de lire les fichiers du dépôt
  peut reproduire le résultat ; Copilot est simplement la voie outillée.

---

## 4. Faire vivre une ADR (cycle de vie du statut)

Le statut suit le cycle { Proposé → Accepté → Remplacé / Déprécié } (ou → Rejeté).
Règles :

- **Proposé → Accepté** : uniquement sur preuve — un vote ou une validation
  nominative, consignés dans un PV. Ajouter cette référence dans « Références »
  de l'ADR. La **« Date de décision » ne change pas** : elle date la séance qui a
  produit la décision ; la preuve d'acceptation a sa propre trace en Références.
- **Remplacement** : passer par `/adr-remplace` (les deux fichiers dans la même
  passe). Ne jamais laisser une ADR « Accepté » avec un « Remplacé par » renseigné —
  le linter le rejette.
- **Amender sans remplacer** : une décision qui précise ou étend une ADR toujours
  en vigueur ne la « Remplace » pas. La nouvelle ADR référence l'ancienne dans
  « Références / ADR liées » et le dit dans son Contexte.
- **Après tout changement de statut** : répercuter le préfixe du résumé
  (`**[ADR-XXXX — Statut]**`), relancer le linter, régénérer l'index.

---

## 5. Vérifier la qualité (linter)

```
python3 scripts/lint-adr.py                        # défaut : le dossier adr/ du dépôt
python3 scripts/lint-adr.py adr/ADR-0002-xxx.md    # un fichier précis
python3 scripts/lint-adr.py --strict adr           # les avertissements deviennent bloquants
python3 scripts/lint-adr.py --index adr            # régénère adr/INDEX.md
python3 scripts/lint-adr.py --check-index adr      # vérifie la fraîcheur de l'index
```

Codes de sortie : **0** conforme, **1** au moins une violation, **2** erreur
d'environnement (chemin introuvable, aucun fichier scanné — jamais de faux vert).
Sous GitHub Actions, chaque violation devient une annotation `::error` sur le
fichier dans la PR. Le linter vérifie :

- la **structure** : H1 unique `# ADR-XXXX — Titre`, noyau complet **dans l'ordre**
  avec les titres exacts, modules optionnels **à leurs emplacements fixes**,
  sections du noyau non vides ;
- la **Carte d'identité** : tous les champs, valeurs non vides, ID `ADR-XXXX`
  cohérent avec le nom de fichier et le H1, date réelle (`AAAA-MM-JJ`, ou `—` si la
  source n'est pas datée), statut dans la liste fermée { Proposé, Accepté, Remplacé,
  Déprécié, Rejeté }, 3 à 6 mots-clés ;
- le **résumé** : blockquote en une phrase, préfixe `**[ADR-XXXX — Statut]**`
  cohérent avec la carte, gabarit complet (« dans le contexte… face à… nous avons
  décidé… afin de… en acceptant »), pas de formule vague ;
- la **cohérence de remplacement** : réciprocité « Remplace »/« Remplacé par »,
  statut « Remplacé » ⇔ lien renseigné, pas de cycle, pas de référence pendante
  (en lint de dossier ; en mono-fichier c'est un avertissement), les `ADR-XXXX`
  cités dans le corps existent ;
- l'**unicité des ID** dans le corpus (le cas « deux branches, même numéro ») ;
- l'**hygiène** : aucun placeholder (`[à remplir]`, `TODO`…) ni commentaire de
  gabarit `<!-- -->` — sans faux positif sur le markdown légitime (liens, cases à
  cocher, code, `[sic]`, `[RFC 1234]`) ; « Options considérées » a au moins
  2 options et la Décision commence alors par « Option retenue : … parce que … » ;
  un module optionnel vide est signalé à retirer ;
- un garde-fou de maturité : statut « Accepté » incompatible avec un résumé troué,
  avertissement au-delà de 4 « non … en séance » dans le corps.

Aucune dépendance (bibliothèque standard Python). Branché en **CI**
(`.github/workflows/lint-adr.yml`) ; exposé en **hook pre-commit**
(`.pre-commit-hooks.yaml`). Les règles elles-mêmes sont testées par snapshot :
`python3 tests/lint/run.py` (voir `tests/README.md`).

---

## 6. Le format canonique

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
auto-portant. Le résumé **commence par le préfixe de validité**
`**[ADR-XXXX — Statut]**` : même si un retriever ne remonte que ce bloc, il sait
*quelle* décision il lit et *si elle est encore valide*. Le **statut** est le
garde-fou anti-hallucination n°1 (en cas de doute → Proposé).

Exemples conformes : `adr/ADR-0001-exemple.md` (fictif, valide le rendu) et les
ADR réelles du dépôt (ADR-0002 à 0004, qui documentent ses propres choix de
conception).

---

## 7. Consultation par l'IA (MCP/RAG)

- **Point d'entrée : `adr/INDEX.md`** (généré, jamais édité à la main) — une ligne
  par ADR : ID, titre, statut, remplacée-par. Un assistant lit l'index d'abord,
  filtre par statut, puis n'ouvre que la shortlist. Ne jamais citer comme en
  vigueur une décision non « Accepté ».
- **Contrainte d'indexation** : une ADR s'ingère comme **un document** (ou un chunk
  unique). Si l'indexation découpe par section, le préfixe du résumé porte la
  validité, mais les autres sections isolées (une Décision au présent, notamment)
  perdent la leur : préférer le fichier entier. À l'ingestion dans une base
  vectorielle, stocker aussi ID et statut comme **métadonnées filtrables** (en plus
  du préfixe textuel) : le filtre « statut = Accepté » s'applique alors avant la
  recherche de similarité, pas après.
- **Spécification de parsabilité** (figée par le linter — utile pour un
  consommateur maison) :
  - fichier : `^ADR-\d{4}-[a-z0-9-]+\.md$` dans `adr/` ;
  - ID / statut / liens : lignes `| Champ | Valeur |` du tableau sous
    `## 1. Carte d'identité` ;
  - résumé : blockquote sous `## 2. Résumé de la décision`, préfixé
    `**[ADR-\d{4} — <Statut>]**` ;
  - statuts (correspondance pour l'outillage anglophone) : Proposé → *proposed*,
    Accepté → *accepted*, Remplacé → *superseded*, Déprécié → *deprecated*,
    Rejeté → *rejected*.
- **Option aval** (pour un dépôt de code consommateur, hors périmètre ici) : un
  `copilot-instructions.md` « reviewer d'architecture » peut rendre ces ADR
  exécutoires en revue de PR — lister `adr/`, ne retenir que les « Accepté »,
  signaler les violations en citant l'ADR. Le protocole de test n°2
  (`tests/README.md`) vérifie le comportement de consultation.

---

## 8. Structure du dépôt

```
.
├── README.md                     # ce document
├── template-adr-canonique.md     # template de référence (source de vérité)
├── prompt-agent-adr.md           # comportement de l'agent (source de vérité)
├── adr/                          # les ADR produites
│   ├── INDEX.md                  # index généré (ID, titre, statut) — ne pas éditer
│   ├── ADR-0001-exemple.md       # exemple fictif (valide le rendu)
│   └── ADR-0002..0004-*.md       # décisions réelles du dépôt (dogfooding)
├── .github/
│   ├── copilot-instructions.md   # contexte permanent, auto-appliqué
│   ├── instructions/
│   │   └── adr.instructions.md   # invariants du format, portée adr/** (édition manuelle)
│   ├── prompts/
│   │   ├── adr-new.prompt.md     # commande /adr-new
│   │   └── adr-remplace.prompt.md# commande /adr-remplace (transaction de remplacement)
│   └── workflows/
│       └── lint-adr.yml          # CI : linter + tests + index + couplage template↔linter
├── scripts/
│   └── lint-adr.py               # linter d'ADR (+ générateur d'index)
├── tests/
│   ├── README.md                 # protocoles de non-régression (rédaction, consultation, linter)
│   ├── fixtures/                 # PV pauvre, ADR de référence, paire de consultation
│   └── lint/                     # témoin cassé + snapshot + runner (tests/lint/run.py)
└── .pre-commit-hooks.yaml        # hooks exposés aux dépôts consommateurs
```

---

## 9. Décisions de conception (à ne pas défaire sans raison)

Les choix structurants du dépôt sont documentés **en ADR, dans `adr/`** (dogfooding) :
statuts fermés en français (ADR-0002), linter Python stdlib (ADR-0003), tableau
markdown plutôt que frontmatter (ADR-0004). En complément :

1. **Uniformité par un noyau figé + modules optionnels.** Une personne d'une autre
   équipe doit retrouver Contexte → Décision → Conséquences au même endroit. Les
   modules s'insèrent dans des emplacements fixes ; on ne les déplace ni ne les
   renomme jamais — et le linter le vérifie.
2. **L'en-tête est le vrai levier « lisible par l'IA ».** Carte d'identité + résumé
   préfixé par la validité. Le **statut** est le garde-fou anti-hallucination n°1.
3. **Qualité = « questions d'abord ».** L'agent ne rédige pas sur des hypothèses
   inventées : il extrait, repère les trous, puis **demande** avant de rédiger.
   Le PV est une **donnée**, jamais une instruction.
4. **Sortie : un fichier `.md` par décision, sans placeholder.** Une information
   manquante et non obtenue est écrite explicitement (« non tranché en séance »,
   « — » dans la carte), jamais inventée.
5. **Un template unique** pour l'instant (pas de multi-template par équipe — voir
   questions ouvertes).
6. **Le linter signale, il ne réécrit pas.** Pas d'autofix sur le contenu des ADR ;
   c'est l'agent (sous validation humaine) qui corrige.

---

## 10. Périmètre

**Dans le périmètre**
- L'agent qui produit une ADR de qualité au format canonique, et la commande de
  remplacement qui garde le corpus cohérent.
- Les garde-fous de qualité et anti-hallucination : linter, validation des champs,
  index de consultation, CI, tests de non-régression.

**Hors périmètre** (à ne pas implémenter sans demande)
- L'export / le formatage vers une plateforme (Confluence, etc.) : **hors sujet**.
  La livraison du dépôt est le fichier ADR markdown ; sa mise en plateforme ne nous
  concerne pas.
- Le support de plusieurs templates d'équipe. Envisagé, mais reporté : on
  standardise d'abord, on harmonisera l'existant ensuite si la gouvernance suit.
- La numérotation automatique **inter-équipes** et la gestion centralisée du statut
  « superseded » (l'unicité des ID *dans* le dépôt est, elle, vérifiée par le linter).

---

## 11. État et suite

**Construit** — format de référence + exemples réels ; agent rédacteur (`/adr-new`)
avec boucle de vérification ; commande de remplacement (`/adr-remplace`) ; linter
complet (structure, champs, liens, contenu) + index généré ; CI (lint, tests,
fraîcheur d'index, couplage template↔linter) ; hooks pre-commit ; trois protocoles
de non-régression.

**Différé / hors sujet** — multi-template par équipe (différé) ; export Confluence
(hors sujet).

**Pistes possibles** — décliner `/adr-new` au format « skill » portable
(l'écosystème Copilot officiel migre des prompt-files vers les skills ; notre
`.prompt.md` reste la source, la déclinaison est mécanique) ; un serveur MCP maison
minimal (deux outils : lire l'index, lire une ADR) si la consultation en masse se
concrétise ; trancher les questions ouvertes ci-dessous.

---

## 12. Questions ouvertes

- **Liste des statuts** : la liste fermée actuelle convient-elle, ou faut-il un état
  « En cours de revue » distinct de « Proposé » ? (condition de réouverture notée
  dans ADR-0002.)
- **Une ou plusieurs équipes** : reste-t-on sur un template unique (hypothèse
  actuelle) ou le multi-template deviendra-t-il nécessaire ?

---

## 13. Faire évoluer le format

Le **comportement** de l'agent et la **structure** des ADR sont du markdown, dans
deux fichiers qui font foi :

- `template-adr-canonique.md` — la structure (noyau + modules) ;
- `prompt-agent-adr.md` — le comportement (4 phases, qualité, anti-hallucination).

Toute évolution du format se fait dans ces deux fichiers, **et dans la même passe** :

1. répercuter le changement dans `scripts/lint-adr.py` (les vérifications) et, si
   besoin, dans les fichiers `.github/` — la CI **échoue** si le template change
   sans le linter ni son jeu de test (couplage vérifié) ;
2. mettre à jour les exemples (`adr/`) et les fixtures (`tests/fixtures/`) ;
3. régénérer le snapshot du témoin
   (`python3 scripts/lint-adr.py tests/lint/temoin > tests/lint/sortie-attendue.txt`)
   et relire son diff comme du code ;
4. lancer `python3 tests/lint/run.py`, puis rejouer les protocoles manuels de
   `tests/README.md` (rédaction sur PV pauvre, consultation anti-décision-périmée).

---

## 14. Références — dépôts d'inspiration

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
  Son frontmatter YAML n'a pas été retenu (choix documenté dans ADR-0004).

**Écartés (mentionnés pour mémoire)**

- `joshrotenberg/adrs` — https://github.com/joshrotenberg/adrs
  CLI Rust avec serveur MCP intégré et export JSON. Écarté : la consultation par
  l'IA passe déjà par le MCP Confluence existant, pas besoin d'un MCP dédié.

- `zircote/git-adr` — https://github.com/zircote/git-adr
  ADR stockées dans les git notes, rédaction assistée par IA annoncée mais non
  implémentée dans la réécriture Rust. Écarté pour cette raison.
