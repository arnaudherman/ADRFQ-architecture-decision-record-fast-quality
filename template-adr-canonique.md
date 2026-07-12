<!-- ============================================================= -->
<!-- TEMPLATE ADR CANONIQUE — v2                                    -->
<!--                                                               -->
<!-- RÈGLE D'UNIFORMITÉ (ne jamais enfreindre) :                   -->
<!--   - Le NOYAU est toujours présent, dans CET ordre, avec ces   -->
<!--     titres exacts. On ne renomme pas, on ne réordonne pas.    -->
<!--   - Les MODULES optionnels occupent des EMPLACEMENTS FIXES    -->
<!--     (repérés ci-dessous). On les inclut ou on les retire,     -->
<!--     mais on ne les déplace jamais. Un module que la source ne -->
<!--     nourrit pas est OMIS, jamais rempli de vide.              -->
<!--   - Une décision légère = noyau seul.                         -->
<!--     Une décision lourde = noyau + modules pertinents.         -->
<!--                                                               -->
<!-- Ordre canonique des sections :                                -->
<!--   1. Carte d'identité ........... NOYAU                       -->
<!--   2. Résumé de la décision ...... NOYAU                       -->
<!--   3. Contexte et problème ....... NOYAU                       -->
<!--   [emplacement A] Critères de décision ..... optionnel        -->
<!--   [emplacement B] Options considérées ...... optionnel        -->
<!--   4. Décision .................... NOYAU                      -->
<!--   5. Conséquences ............... NOYAU                       -->
<!--   [emplacement C] Validation et suivi ....... optionnel       -->
<!--   [emplacement D] Références ................ optionnel       -->
<!--                                                               -->
<!-- Nom de fichier : adr/ADR-XXXX-titre-court-en-kebab-case.md ;  -->
<!-- le numéro est identique à l'ID de la Carte d'identité (le     -->
<!-- linter compare).                                              -->
<!--                                                               -->
<!-- RÈGLES D'ÉCRITURE GLOBALES (tout le document) :               -->
<!--   - LACUNES : une information absente de la source s'écrit    -->
<!--     « non documenté en séance » (décision issue d'un PV) ou   -->
<!--     « non documenté à ce stade » (entretien) — jamais une     -->
<!--     invention. Pour une date : « — ».                         -->
<!--   - AUTO-SUFFISANCE : chaque section nomme explicitement la   -->
<!--     techno, l'option ou le composant dont elle parle — jamais -->
<!--     « cette solution ». Renvois internes interdits et rejetés -->
<!--     par le linter : « ci-dessus », « ci-dessous », « voir     -->
<!--     plus haut », « comme mentionné plus haut ». Une section   -->
<!--     doit rester compréhensible isolée (lecture par extraits   -->
<!--     RAG).                                                     -->
<!--   - SOBRIÉTÉ : pas de diagramme ni de bloc de code dans       -->
<!--     l'ADR (le linter avertit) ; un lien dans « Références »   -->
<!--     vers la doc séparée.                                      -->
<!--                                                               -->
<!-- Avant publication : retirer tous les commentaires <!-- --> .  -->
<!-- Le linter rejette toute trace de gabarit : commentaire        -->
<!-- résiduel, crochets « [À remplir] », « ADR-XXXX » hors ID      -->
<!-- réel, « AAAA-MM-JJ » littéral, liste de statuts non résolue   -->
<!-- en une seule valeur.                                          -->
<!-- ============================================================= -->

# ADR-XXXX — [Titre court et factuel de la décision]

<!-- Le titre nomme la décision, pas le problème.                  -->
<!-- Bon : « Utiliser PostgreSQL pour la persistance du catalogue »-->
<!-- Mauvais : « Choix de base de données »                        -->

## 1. Carte d'identité

<!-- Bloc auto-suffisant, lu en premier par un humain ET par un    -->
<!-- retriever (MCP/RAG). Doit suffire à savoir QUOI, par QUI,     -->
<!-- SUR QUELLE PREUVE, et surtout SI LA DÉCISION EST ENCORE EN    -->
<!-- VIGUEUR, sans lire la suite. Le statut est le champ           -->
<!-- anti-hallucination n°1 : UNE seule valeur de la liste fermée. -->
<!-- Le tableau est d'UN SEUL TENANT : ne rien insérer entre ses   -->
<!-- lignes (il doit se rendre et se parser comme un seul bloc     -->
<!-- dans tout environnement).                                     -->

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-XXXX |
| Statut             | Proposé \| Accepté \| Remplacé \| Déprécié \| Rejeté |
| Date de décision   | AAAA-MM-JJ \| — |
| Validé par         | [personne (rôle) ou instance] \| — |
| Équipe / périmètre | [équipe propriétaire + domaine concerné] |
| Mots-clés          | [3 à 6 termes pour la recherche : techno, domaine métier, composant] |
| Remplace           | — \| ADR-XXXX |
| Remplacé par       | — \| ADR-XXXX |

<!-- Date de décision : la date de la séance (AAAA-MM-JJ). Si la   -->
<!-- source n'est pas datée, écrire « — » — ne JAMAIS inventer une -->
<!-- date. Une ADR « Accepté » peut avoir une date « — » (backfill -->
<!-- d'une décision en vigueur depuis un PV non daté).             -->
<!--                                                               -->
<!-- Validé par : la PREUVE que le statut a été tranché — qui a    -->
<!-- approuvé (Accepté) ou prononcé le rejet (Rejeté). Jamais la   -->
<!-- liste des présents ni des personnes consultées (pas de RACI). -->
<!-- Formats : « Prénom Nom (rôle) » ou « comité d'architecture,   -->
<!-- vote du AAAA-MM-JJ ». La date y est FACULTATIVE : ne l'écrire -->
<!-- que si la source la rattache à la validation elle-même — ne   -->
<!-- pas la déduire de la date de séance. Si la source ne rattache -->
<!-- aucune validation nominative à LA décision : « — », et le     -->
<!-- statut reste « Proposé » (le linter vérifie ce couplage).     -->
<!-- Pour une « Remplacé » ou « Déprécié » : conserver la valeur   -->
<!-- qu'avait le champ avant le changement de statut.              -->
<!--                                                               -->
<!-- Mots-clés : en minuscules et en français, sauf les noms       -->
<!-- propres de produits (PostgreSQL, Kong…) ; au singulier.       -->
<!--                                                               -->
<!-- Cohérences vérifiées par le linter :                          -->
<!--   Statut = Accepté ou Rejeté  =>  Validé par ≠ « — »          -->
<!--   Statut = Proposé            =>  Validé par = « — »          -->
<!--   Statut = Remplacé           =>  Remplacé par ≠ « — »        -->
<!--   Remplacé par ≠ « — »   =>  Statut ∈ { Remplacé, Déprécié }  -->
<!--   Au niveau du corpus : toute ADR citée dans Remplace /       -->
<!--   Remplacé par existe, les liens sont réciproques, et le      -->
<!--   graphe de remplacement ne contient aucun cycle.             -->

## 2. Résumé de la décision

<!-- UNE phrase, auto-portante. C'est ce qu'un RAG remonte et ce   -->
<!-- qu'un lecteur pressé lit. Doit contenir la décision ET le     -->
<!-- pourquoi, pas seulement le quoi. Suivre le gabarit :          -->
<!--                                                               -->
<!-- Le préfixe **[ADR-XXXX — Statut]** est OBLIGATOIRE : il porte -->
<!-- l'identité et la validité de la décision dans le bloc même    -->
<!-- qu'un retriever remonte. Il reprend exactement l'ID et le     -->
<!-- Statut de la Carte d'identité (le linter vérifie).            -->
<!--                                                               -->
<!-- Les cinq segments en gras sont TOUS présents, TOUJOURS dans   -->
<!-- cet ordre (le linter vérifie l'ordre : c'est lui qui permet   -->
<!-- à un parseur de découper le résumé en segments fiables) :     -->
<!--   Dans le contexte de → face à → nous avons décidé →          -->
<!--   afin d'obtenir → en acceptant.                              -->
<!-- Au-delà d'environ 90 mots, le linter avertit (dérive vers le  -->
<!-- paragraphe : la longueur ~60 mots est un optimum assumé).     -->
<!--                                                               -->
<!-- Ne JAMAIS compléter un segment par inférence. Si la source ne -->
<!-- le dit pas, écrire le marqueur de lacune (« face à un besoin  -->
<!-- non documenté en séance », « en acceptant des compromis non   -->
<!-- évalués en séance »…).                                        -->
<!--                                                               -->
<!-- Cas d'une ADR Rejetée : le gabarit reste le même, la décision -->
<!-- est négative et porte la raison du rejet — « nous avons       -->
<!-- décidé de NE PAS [proposition], afin d'éviter [risque         -->
<!-- identifié], en acceptant [ce à quoi on renonce] » (le linter  -->
<!-- avertit si le segment décision d'une Rejetée ne contient pas  -->
<!-- « ne pas »).                                                  -->

> **[ADR-XXXX — Statut]** Dans le contexte de **[situation]**, face à **[problème / contrainte]**, nous avons décidé **[la décision]** afin d'obtenir **[bénéfice visé]**, en acceptant **[le principal compromis]**.

## 3. Contexte et problème

<!-- Le POURQUOI, en langage NEUTRE : décrire des FAITS, sans      -->
<!-- plaider pour la solution retenue (un contexte-plaidoyer       -->
<!-- masque les alternatives). Nommer l'ÉLÉMENT DÉCLENCHEUR quand  -->
<!-- la source le donne : quel incident, quelle contrainte, quelle -->
<!-- échéance force la décision MAINTENANT ? — et ne pas en        -->
<!-- inventer un si elle est muette. Quelles contraintes           -->
<!-- (techniques, métier, délais, existant) ? Une personne d'une   -->
<!-- autre équipe doit comprendre l'enjeu sans contexte préalable. -->
<!-- Pas de jargon non explicité.                                  -->
<!--                                                               -->
<!-- Si la séance n'a discuté aucune alternative, l'écrire ICI     -->
<!-- (« aucune alternative n'a été discutée en séance ») et        -->
<!-- OMETTRE le module « Options considérées » — ne jamais         -->
<!-- fabriquer un comparatif.                                      -->

[À remplir]

<!-- ===== EMPLACEMENT A — module optionnel ===== -->
## Critères de décision

<!-- OPTIONNEL. À inclure dès qu'un arbitrage non trivial est      -->
<!-- documenté dans la source. Ce sur quoi on a jugé les options ; -->
<!-- rend la décision auditable. Ne lister que des critères        -->
<!-- réellement évoqués. Quand ce module est présent, la raison    -->
<!-- donnée en section 4 après « parce que » devrait reprendre au  -->
<!-- moins un critère listé ici (consigne de rédaction, vérifiée   -->
<!-- par le relecteur, pas par le linter).                         -->

- [Critère 1 — ex. coût d'exploitation]
- [Critère 2 — ex. compétences déjà présentes dans l'équipe]
- [Critère 3 — ex. compatibilité avec l'existant]

<!-- ===== EMPLACEMENT B — module optionnel ===== -->
## Options considérées

<!-- OPTIONNEL — recommandé quand la source documente PLUSIEURS    -->
<!-- options réellement discutées. Lister UNIQUEMENT les           -->
<!-- alternatives explicitement évoquées dans la source : une      -->
<!-- option que la séance n'a pas évoquée est une invention, pas   -->
<!-- une analyse. Une seule option discutée → OMETTRE ce module et -->
<!-- le dire dans « 3. Contexte et problème ». Inclure l'option    -->
<!-- retenue ET les options écartées : le « pourquoi pas » a       -->
<!-- autant de valeur que le « pourquoi ».                         -->
<!--                                                               -->
<!-- Contrat vérifié par le linter quand le module est présent :   -->
<!--   - au moins 2 options ;                                      -->
<!--   - exactement UNE option porte _(retenue)_, les autres       -->
<!--     _(écartée)_ — sauf ADR « Rejeté », où aucune option n'est -->
<!--     retenue (toutes _(écartée)_) ;                            -->
<!--   - le nom de l'option _(retenue)_ est identique au « X » de  -->
<!--     « Option retenue : « X » » en section 4 ;                 -->
<!--   - chaque option a « Pour : » ET « Contre : » non vides — un -->
<!--     vrai contre, pas un repoussoir ; si la source n'en donne  -->
<!--     aucun, écrire « non documenté en séance », ne pas en      -->
<!--     fabriquer.                                                -->

### Option 1 — [nom] _(retenue / écartée)_
- Pour : [...]
- Contre : [...]

### Option 2 — [nom] _(retenue / écartée)_
- Pour : [...]
- Contre : [...]

## 4. Décision

<!-- Le QUOI, sans ambiguïté. Ce qu'on fait concrètement, à        -->
<!-- l'impératif ou au présent. Nommer explicitement la techno ou  -->
<!-- le composant retenu — jamais « cette option ».                -->
<!--                                                               -->
<!-- Si le module « Options considérées » est présent, la section  -->
<!-- COMMENCE par la phrase type (vérifiée par le linter) :        -->
<!--   Option retenue : « [nom] », parce que [raison déterminante].-->
<!-- La raison déterminante est un FAIT tiré de la source, pas un  -->
<!-- jugement de valeur. Canevas utiles : « seule option           -->
<!-- satisfaisant le critère éliminatoire [K] », « ressort         -->
<!-- meilleure sur les critères [C1] et [C2] ». Justifications     -->
<!-- creuses interdites si non sourcées dans le PV — « standard    -->
<!-- du marché », « tout le monde l'utilise », « c'est la          -->
<!-- meilleure solution », « on a toujours fait comme ça » : le    -->
<!-- linter les signale en avertissement.                          -->

[À remplir]

## 5. Conséquences

<!-- HONNÊTE. Inclure les deux faces. Une ADR sans conséquences    -->
<!-- négatives est suspecte : toute décision a un coût.            -->
<!--                                                               -->
<!-- Chaque conséquence découle de la décision DANS CE CONTEXTE :  -->
<!-- une négative qui serait vraie pour n'importe quelle techno    -->
<!-- est un cliché — la remplacer, ou écrire « non évaluées en     -->
<!-- séance ». Le compromis « en acceptant … » du résumé désigne   -->
<!-- le MÊME compromis qu'une puce des « Négatives et compromis    -->
<!-- acceptés » (le linter vérifie le recoupement des termes, en   -->
<!-- avertissement).                                               -->

### Positives
- [Ce qui devient plus simple / possible]

### Négatives et compromis acceptés
- [Ce qu'on perd, ce qui devient plus difficile, la dette assumée]

<!-- ===== EMPLACEMENT C — module optionnel ===== -->
## Validation et suivi

<!-- OPTIONNEL. Comment saura-t-on que la décision était bonne, et -->
<!-- qu'est-ce qui la remettrait en cause ? Le déclencheur nommé   -->
<!-- (« À rouvrir si ») vaut mieux qu'une date d'expiration.       -->
<!-- Ne remplir que ce que la séance a réellement fixé — ne JAMAIS -->
<!-- inventer un indicateur ni une condition de réouverture : en   -->
<!-- proposer un à l'architecte pour confirmation explicite, ou    -->
<!-- omettre la puce (voire le module entier). « Revue prévue le » -->
<!-- porte une vraie date AAAA-MM-JJ (le linter vérifie).          -->

- Indicateur de réussite : [...]
- Revue prévue le : [AAAA-MM-JJ]
- À rouvrir si : [condition qui invaliderait la décision]

<!-- ===== EMPLACEMENT D — module optionnel ===== -->
## Références

<!-- OPTIONNEL. Traçabilité longue : la source de la décision (PV  -->
<!-- de séance, ticket) et les ADR liées. Le PV reste la preuve    -->
<!-- d'audit COMPLÈTE (débats, participants, votes) : la ligne     -->
<!-- « Validé par » de la Carte d'identité n'en est que le résumé  -->
<!-- minimal lisible par le RAG, qui ne suit pas les liens.        -->
<!-- Toujours lier le PV ici quand il existe. Une ADR amendée sans -->
<!-- être remplacée se cite ici, dans « ADR liées ».               -->

- PV / source : [référence ou lien de la séance d'origine]
- ADR liées : [ADR-XXXX, ADR-XXXX]
- Autres : [docs, diagrammes IcePanel, etc.]