<!-- ============================================================= -->
<!-- TEMPLATE ADR CANONIQUE — v1                                    -->
<!--                                                               -->
<!-- RÈGLE D'UNIFORMITÉ (ne jamais enfreindre) :                   -->
<!--   - Le NOYAU est toujours présent, dans CET ordre, avec ces   -->
<!--     titres exacts. On ne renomme pas, on ne réordonne pas.    -->
<!--   - Les MODULES optionnels occupent des EMPLACEMENTS FIXES    -->
<!--     (numérotés ci-dessous). On les inclut ou on les retire,   -->
<!--     mais on ne les déplace jamais.                            -->
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
<!-- Avant publication : retirer tous les commentaires <!-- --> .  -->
<!-- ============================================================= -->

# ADR-XXXX — [Titre court et factuel de la décision]

<!-- Le titre nomme la décision, pas le problème.                  -->
<!-- Bon : « Utiliser PostgreSQL pour la persistance du catalogue »-->
<!-- Mauvais : « Choix de base de données »                        -->

## 1. Carte d'identité

<!-- Bloc auto-suffisant, lu en premier par un humain ET par un    -->
<!-- retriever (MCP/RAG). Doit suffire à savoir QUOI, par QUI, et  -->
<!-- surtout SI LA DÉCISION EST ENCORE EN VIGUEUR, sans lire la    -->
<!-- suite. Le statut est le champ anti-hallucination n°1.         -->

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-XXXX |
| Statut             | Proposé \| Accepté \| Remplacé \| Déprécié \| Rejeté |
| Date de décision   | AAAA-MM-JJ |
| Équipe / périmètre | [équipe propriétaire + domaine concerné] |
| Mots-clés          | [3 à 6 termes pour la recherche : techno, domaine métier, composant] |
| Remplace           | — \| ADR-XXXX |
| Remplacé par       | — \| ADR-XXXX |

## 2. Résumé de la décision

<!-- UNE phrase, auto-portante. C'est ce qu'un RAG remonte et ce   -->
<!-- qu'un lecteur pressé lit. Doit contenir la décision ET le     -->
<!-- pourquoi, pas seulement le quoi. Suivre le gabarit :          -->

> Dans le contexte de **[situation]**, face à **[problème / contrainte]**, nous avons décidé **[la décision]** afin d'obtenir **[bénéfice visé]**, en acceptant **[le principal compromis]**.

## 3. Contexte et problème

<!-- Le POURQUOI. Quelle situation force une décision ? Quelles    -->
<!-- contraintes (techniques, métier, délais, existant) ? Une      -->
<!-- personne d'une autre équipe doit comprendre l'enjeu sans      -->
<!-- contexte préalable. Pas de jargon non explicité.              -->

[À remplir]

<!-- ===== EMPLACEMENT A — module optionnel ===== -->
## Critères de décision

<!-- OPTIONNEL. À inclure dès qu'il y a un arbitrage non trivial.  -->
<!-- Ce sur quoi on a jugé les options. Rend la décision auditable.-->

- [Critère 1 — ex. coût d'exploitation]
- [Critère 2 — ex. compétences déjà présentes dans l'équipe]
- [Critère 3 — ex. compatibilité avec l'existant]

<!-- ===== EMPLACEMENT B — module optionnel ===== -->
## Options considérées

<!-- OPTIONNEL mais FORTEMENT recommandé pour toute décision        -->
<!-- importante : c'est ce qui distingue une ADR correcte d'une    -->
<!-- bonne ADR. Lister les alternatives RÉELLEMENT envisagées,     -->
<!-- avec leurs pour/contre. Inclure l'option retenue ET les       -->
<!-- options écartées (le « pourquoi pas » a autant de valeur).    -->

### Option 1 — [nom] _(retenue / écartée)_
- Pour : [...]
- Contre : [...]

### Option 2 — [nom] _(retenue / écartée)_
- Pour : [...]
- Contre : [...]

## 4. Décision

<!-- Le QUOI, sans ambiguïté. Ce qu'on fait concrètement, à        -->
<!-- l'impératif ou au présent. Si une option a été retenue        -->
<!-- ci-dessus, dire laquelle et la raison déterminante.           -->

[À remplir]

## 5. Conséquences

<!-- HONNÊTE. Inclure les deux faces. Une ADR sans conséquences    -->
<!-- négatives est suspecte : toute décision a un coût.            -->

### Positives
- [Ce qui devient plus simple / possible]

### Négatives et compromis acceptés
- [Ce qu'on perd, ce qui devient plus difficile, la dette assumée]

<!-- ===== EMPLACEMENT C — module optionnel ===== -->
## Validation et suivi

<!-- OPTIONNEL. Comment saura-t-on que la décision était bonne ?   -->
<!-- Indicateurs, date de revue, conditions de remise en cause.    -->

- Indicateur de réussite : [...]
- Revue prévue le : [AAAA-MM-JJ]
- À rouvrir si : [condition qui invaliderait la décision]

<!-- ===== EMPLACEMENT D — module optionnel ===== -->
## Références

<!-- OPTIONNEL. Traçabilité. La source de la décision (PV de       -->
<!-- séance, ticket) et les ADR liées.                             -->

- PV / source : [référence ou lien de la séance d'origine]
- ADR liées : [ADR-XXXX, ADR-XXXX]
- Autres : [docs, diagrammes IcePanel, etc.]
