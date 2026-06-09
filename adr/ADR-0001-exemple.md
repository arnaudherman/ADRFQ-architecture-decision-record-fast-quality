# ADR-0001 — Exposer les services aux partenaires derrière une passerelle d'API unique

> Exemple fictif servant à valider le rendu du template canonique. Aucune décision réelle.

## 1. Carte d'identité

| Champ              | Valeur |
|--------------------|--------|
| ID                 | ADR-0001 |
| Statut             | Accepté |
| Date de décision   | 2026-05-14 |
| Équipe / périmètre | Architecture d'entreprise — exposition des services aux partenaires externes (intégration B2B) |
| Mots-clés          | API Gateway, Kong, sécurité, intégration partenaires, OAuth2, observabilité |
| Remplace           | — |
| Remplacé par       | — |

## 2. Résumé de la décision

> Dans le contexte de l'ouverture progressive de nos services à des partenaires externes, face à la multiplication de points d'entrée hétérogènes et mal sécurisés, nous avons décidé de centraliser toute exposition externe derrière une passerelle d'API unique (Kong auto-hébergée) afin d'uniformiser l'authentification, la limitation de débit et l'observabilité, en acceptant un point de passage supplémentaire à exploiter et à rendre hautement disponible.

## 3. Contexte et problème

Plusieurs services internes sont aujourd'hui exposés directement à des partenaires, chacun avec sa propre mécanique : certaines API valident une clé passée dans l'URL, d'autres reposent sur de l'authentification basique, aucune n'applique de limitation de débit (*rate limiting* : plafonnement du nombre d'appels par client et par période). Il n'existe pas de journal centralisé du trafic externe.

Un audit de sécurité a relevé ces écarts comme un risque majeur (fuite de clés, absence de traçabilité). En parallèle, la feuille de route métier prévoit l'intégration de trois nouveaux partenaires au second semestre 2026, ce qui aggraverait l'hétérogénéité si rien ne change.

Le problème : comment ouvrir le système d'information à des tiers de façon **sûre, traçable et reproductible**, sans réécrire chaque service ni retarder l'arrivée des partenaires ?

## Critères de décision

- Sécurité : authentification et autorisation uniformes et auditables sur tout le trafic externe.
- Délai de mise en œuvre compatible avec l'onboarding partenaires prévu au S2 2026.
- Compétences déjà présentes dans l'équipe (maîtrise de Nginx/Lua).
- Coût d'exploitation et niveau de dépendance à un fournisseur (éviter un verrouillage cloud).
- Observabilité centralisée (journaux et métriques d'appels en un seul endroit).

## Options considérées

### Option 1 — Passerelle d'API auto-hébergée (Kong) _(retenue)_
- Pour : s'appuie sur Nginx/Lua déjà connus de l'équipe ; portable d'un environnement à l'autre ; configuration déclarative (onboarding partenaire sans développement) ; pas de verrouillage cloud.
- Contre : composant supplémentaire à exploiter, patcher et rendre hautement disponible ; la haute disponibilité a un coût d'infrastructure.

### Option 2 — Passerelle managée du fournisseur cloud _(écartée)_
- Pour : pas d'infrastructure à exploiter, haute disponibilité incluse, mise en route rapide.
- Contre : verrouillage fort sur le fournisseur ; modèle de coût à l'appel difficile à prévoir au volume cible ; portabilité quasi nulle si une partie du SI reste sur site.

### Option 3 — Statu quo : chaque service gère sa propre exposition _(écartée)_
- Pour : aucun nouveau composant, aucun coût immédiat.
- Contre : ne corrige aucun des écarts de l'audit ; le coût de sécurisation est payé autant de fois qu'il y a de services ; l'hétérogénéité empire à chaque nouveau partenaire.

## 4. Décision

Toute exposition de service vers un partenaire externe passe désormais par une **passerelle d'API Kong auto-hébergée**, déployée en DMZ. L'authentification se fait par OAuth2 *client credentials* (un jeu d'identifiants par partenaire), avec une limitation de débit définie par partenaire. Les services internes ne sont plus joignables directement depuis l'extérieur. L'option Kong est retenue parce qu'elle satisfait le critère de sécurité tout en réutilisant les compétences existantes et en évitant un verrouillage cloud.

## 5. Conséquences

### Positives
- Authentification, autorisation et limitation de débit uniformes sur tout le trafic externe.
- Journaux et métriques d'appels centralisés : la traçabilité demandée par l'audit est obtenue.
- Onboarding d'un nouveau partenaire par configuration, sans modifier le code des services.

### Négatives et compromis acceptés
- Nouveau composant critique : il doit être rendu hautement disponible, ce qui a un coût d'infrastructure et d'exploitation.
- L'équipe doit monter et maintenir des compétences sur les *plugins* Lua de Kong.
- Un saut réseau supplémentaire ajoute quelques millisecondes de latence.
- Effort de migration : les partenaires existants doivent basculer vers le nouveau point d'entrée.

## Validation et suivi

- Indicateur de réussite : 100 % du trafic partenaire transite par la passerelle d'ici fin Q3 2026 ; zéro incident d'authentification lié à une exposition directe.
- Revue prévue le : 2027-01-15
- À rouvrir si : le nombre de partenaires reste inférieur ou égal à deux et que le coût de la haute disponibilité dépasse le bénéfice, ou si une contrainte réglementaire impose une solution managée certifiée.

## Références

- PV / source : PV de la séance d'architecture du 2026-05-14 (comité d'exposition du SI).
- ADR liées : —
- Autres : schéma d'exposition DMZ (IcePanel).
