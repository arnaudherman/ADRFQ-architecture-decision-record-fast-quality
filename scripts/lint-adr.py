#!/usr/bin/env python3
"""Linter d'ADR — vérifie le format canonique (structure, Carte d'identité,
résumé préfixé, cohérence statuts ↔ liens de remplacement, unicité des ID)
et génère l'index de consultation.

Usage :
    python3 scripts/lint-adr.py [chemins...]        # défaut : le dossier adr/ du dépôt
    python3 scripts/lint-adr.py --strict [chemins]  # avertissements bloquants
    python3 scripts/lint-adr.py --index adr         # régénère adr/INDEX.md
    python3 scripts/lint-adr.py --check-index adr   # vérifie la fraîcheur de l'index

Codes de sortie : 0 conforme · 1 violation(s) · 2 erreur d'environnement
(chemin introuvable, aucun fichier scanné — jamais de faux vert).
Sous GitHub Actions, chaque violation est aussi émise en annotation ::error/::warning.
Aucune dépendance externe (bibliothèque standard uniquement).
Les règles sont testées par snapshot : python3 tests/lint/run.py.
"""

import argparse
import datetime
import os
import re
import sys
from pathlib import Path

STATUTS = {"Proposé", "Accepté", "Remplacé", "Déprécié", "Rejeté"}
CHAMPS_IDENTITE = [
    "ID",
    "Statut",
    "Date de décision",
    "Équipe / périmètre",
    "Mots-clés",
    "Remplace",
    "Remplacé par",
]
SECTIONS_NOYAU = [
    "Carte d'identité",
    "Résumé de la décision",
    "Contexte et problème",
    "Décision",
    "Conséquences",
]
RE_ID = re.compile(r"^ADR-\d{4}$")
RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Ligne de tableau à EXACTEMENT deux cellules (pipes échappés \| admis dans une cellule).
RE_TABLE_ROW = re.compile(r"^\|\s*((?:\\\||[^|])+?)\s*\|\s*((?:\\\||[^|])+?)\s*\|\s*$")
RE_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
RE_ADR_REF = re.compile(r"ADR-\d{4}")
RE_FENCE = re.compile(r"^\s*(```|~~~)")
# Placeholder = [texte] qui n'est PAS un lien markdown [texte](url).
RE_PLACEHOLDER = re.compile(r"\[[^\]\n]+\](?!\()")
# Préfixe de validité du résumé « [ADR-XXXX — Statut] » : pas un placeholder.
RE_PREFIXE_RESUME = re.compile(r"^\[ADR-\d{4} — (?:%s)\]$" % "|".join(sorted(STATUTS)))
# Crochets éditoriaux légitimes : [sic], références normatives [RFC 7231], [ISO 8601]…
RE_CROCHETS_LEGITIMES = re.compile(r"(?i)^\[(?:sic|rfc\s*\d+|iso[\s/-][\w:.-]+)\]$")
MODULES_OPTIONNELS = [
    "Critères de décision",
    "Options considérées",
    "Validation et suivi",
    "Références",
]
# Marqueur de lacune : « non documenté / évalué / tranché … » suivi de la source —
# « en séance » (la décision vient d'un PV) ou « à ce stade » / « à ce jour »
# (entretien sans séance). Participes de LACUNE uniquement (pas « vote non
# contesté en séance », qui décrit un vote réel).
RE_NON_SEANCE = re.compile(
    r"non\s+(?:documenté|évalué|tranché|discuté|abordé|précisé|exprimé|formulé)(?:e?s?)\s+"
    r"(?:en\s+séance|à\s+ce\s+stade|à\s+ce\s+jour)",
    re.IGNORECASE,
)
# Placeholders textuels (frontières de mots pour éviter les faux positifs).
RE_PLACEHOLDER_TXT = re.compile(r"(?i)\b(?:todo|tbd|xxx|lorem ipsum)\b|à compléter|à définir|ADR-XXXX")
# Gabarit du résumé : marqueurs obligatoires (libellé affiché, motif regex).
MARQUEURS_RESUME = [
    ("dans le contexte", r"dans le contexte"),
    ("face à", r"face\s+(?:à|au|aux)\b"),
    ("nous avons décidé", r"nous avons décidé"),
    ("afin de", r"afin\s+d"),
    ("en acceptant", r"en acceptant"),
]
# Préfixe de validité en tête du blockquote du résumé.
RE_PREFIXE_RESUME_GRAS = re.compile(r"^\*\*\[(ADR-\d{4}) — ([^\]]+)\]\*\*\s*")
# Formules vagues, interdites dans le résumé (bloc lu en priorité par l'IA).
RE_RESUME_CREUX = re.compile(r"\betc\b\.?|d'autres compromis|\bdivers\b", re.IGNORECASE)


class Rapport:
    def __init__(self, fichier):
        self.fichier = fichier
        self.erreurs = []
        self.avertissements = []
        self.refs_corps = set()

    def err(self, champ, msg):
        self.erreurs.append((champ, msg))

    def warn(self, champ, msg):
        self.avertissements.append((champ, msg))


def lignes_hors_code(texte):
    """Itère (index, ligne) en masquant l'intérieur des blocs de code ``` / ~~~."""
    dans_code = False
    fence = None
    for i, ligne in enumerate(texte.splitlines()):
        m = RE_FENCE.match(ligne)
        if m:
            if not dans_code:
                dans_code, fence = True, m.group(1)
            elif m.group(1) == fence:
                dans_code, fence = False, None
            continue
        if not dans_code:
            yield i, ligne


def texte_hors_code(texte):
    """Le texte dont l'intérieur des blocs de code a été retiré."""
    return "\n".join(ligne for _, ligne in lignes_hors_code(texte))


def titres(texte):
    """Liste de (niveau, titre, index_ligne), hors blocs de code."""
    res = []
    for i, ligne in lignes_hors_code(texte):
        m = RE_HEADING.match(ligne)
        if m:
            res.append((len(m.group(1)), m.group(2), i))
    return res


def titre_noyau_attendu(sec):
    """Titre H2 canonique d'une section du noyau : « N. Titre »."""
    return f"{SECTIONS_NOYAU.index(sec) + 1}. {sec}"


def section_contenu(texte, titre_exact, niveau=2):
    """Texte sous le heading de `niveau` dont le titre est EXACTEMENT `titre_exact`,
    jusqu'au heading suivant de même niveau ou supérieur. None si absent."""
    lignes = texte.splitlines()
    debut = None
    for niv, titre, i in titres(texte):
        if niv == niveau and titre == titre_exact:
            debut = i + 1
            break
    if debut is None:
        return None
    corps = []
    dans_code = False
    for ligne in lignes[debut:]:
        if RE_FENCE.match(ligne):
            dans_code = not dans_code
        m = RE_HEADING.match(ligne)
        if m and not dans_code and len(m.group(1)) <= niveau:
            break
        corps.append(ligne)
    return "\n".join(corps)


def parser_identite(texte, rapport=None):
    """Extrait le tableau de la SEULE section « 1. Carte d'identité » -> dict champ: valeur.

    Une ligne de tableau qui n'a pas exactement deux cellules est signalée
    (rapport.warn) : elle masquerait silencieusement un champ.
    """
    champs = {}
    corps = section_contenu(texte, titre_noyau_attendu("Carte d'identité"))
    if corps is None:
        return champs
    for ligne in corps.splitlines():
        s = ligne.strip()
        if not s.startswith("|"):
            continue
        m = RE_TABLE_ROW.match(s)
        if not m:
            if rapport is not None and not re.fullmatch(r"\|[\s:|-]+\|", s):
                rapport.warn("identité", f"ligne de tableau invalide (deux cellules attendues) : « {s[:60]} »")
            continue
        cle = m.group(1).strip()
        val = m.group(2).strip()
        if cle in ("Champ",) or set(cle) <= {"-", ":", " "}:
            continue
        if cle in CHAMPS_IDENTITE and cle not in champs:
            champs[cle] = val
    return champs


def texte_pour_placeholders(texte):
    """Le texte où le markdown légitime à crochets a été retiré :
    blocs et code inline, cases à cocher, liens par référence et leurs définitions."""
    t = texte_hors_code(texte)
    t = re.sub(r"`[^`\n]*`", "", t)                       # code inline
    t = re.sub(r"(?m)^\s*[-*+]\s+\[[ xX]\]\s+", "", t)    # cases à cocher - [ ] / - [x]
    t = re.sub(r"(?m)^\s*\[[^\]\n]+\]:\s+\S+.*$", "", t)  # définitions [ref]: url
    t = re.sub(r"\[[^\]\n]+\]\[[^\]\n]*\]", "", t)        # liens par référence [texte][ref]
    return t


def section_sans_contenu(corps):
    """Vrai si le corps n'a AUCUNE ligne de contenu (les sous-titres ne comptent pas).
    Contrairement à module_vide, « non … en séance / à ce stade » compte comme du
    contenu : c'est la mention honnête prescrite pour le noyau."""
    if corps is None:
        return False
    return not any(l.strip() and not l.strip().startswith("#") for l in corps.splitlines())


def module_vide(corps):
    """Vrai si le corps d'un module n'a aucun contenu réel, ou seulement des
    mentions « non … en séance / à ce stade » (sous-titres et puces ignorés)."""
    if corps is None:
        return False
    lignes = []
    for ligne in corps.splitlines():
        s = ligne.strip()
        if not s or s.startswith("#"):
            continue
        s = re.sub(r"^[-*+]\s+", "", s)  # retire le marqueur de puce
        lignes.append(s)
    if not lignes:
        return True
    reste = RE_NON_SEANCE.sub("", " ".join(lignes))
    reste = re.sub(r"[\s.;,:–—-]+", "", reste)
    return reste == ""


def lint_fichier(chemin):
    texte = Path(chemin).read_text(encoding="utf-8")
    r = Rapport(chemin)

    # 1. Sections du noyau : titres H2 exacts « N. Titre »
    tt = titres(texte)
    h2 = [titre for niv, titre, _ in tt if niv == 2]
    for sec in SECTIONS_NOYAU:
        attendu = titre_noyau_attendu(sec)
        if attendu in h2:
            continue
        proche = next((t for t in h2 if sec in t), None)
        if proche is not None:
            r.err("noyau", f"titre non canonique : « {proche} » (attendu « {attendu} »)")
        else:
            r.err("noyau", f"section manquante : « {attendu} »")

    # 1b. Titre H1 : unique, au format « ADR-XXXX — Titre »
    h1 = [(titre, i) for niv, titre, i in tt if niv == 1]
    h1_id = None
    if not h1:
        r.err("titre", "titre H1 manquant — aide : ajouter « # ADR-XXXX — Titre de la décision » en tête de fichier")
    else:
        if len(h1) > 1:
            r.err("titre", f"{len(h1)} titres H1 trouvés — un seul attendu")
        m_h1 = re.match(r"^(ADR-\d{4}) — .+$", h1[0][0])
        if m_h1:
            h1_id = m_h1.group(1)
        else:
            r.err("titre", f"format du titre H1 invalide : « {h1[0][0]} » (attendu « ADR-XXXX — Titre »)")

    # 1c. Ordre du noyau (1 → 5) et emplacements fixes des modules
    pos = {}
    for niv, titre, i in tt:
        if niv == 2 and titre not in pos:
            pos[titre] = i
    noyau_pos = [pos.get(titre_noyau_attendu(sec)) for sec in SECTIONS_NOYAU]
    presents = [p for p in noyau_pos if p is not None]
    if presents != sorted(presents):
        r.err("noyau", "sections du noyau dans le désordre — aide : rétablir l'ordre canonique 1 → 5")
    p3 = pos.get(titre_noyau_attendu("Contexte et problème"))
    p4 = pos.get(titre_noyau_attendu("Décision"))
    p5 = pos.get(titre_noyau_attendu("Conséquences"))
    emplacements = {
        "Critères de décision": (p3, p4, "entre « 3. Contexte et problème » et « 4. Décision »"),
        "Options considérées": (p3, p4, "entre « 3. Contexte et problème » et « 4. Décision »"),
        "Validation et suivi": (p5, None, "après « 5. Conséquences »"),
        "Références": (p5, None, "après « 5. Conséquences »"),
    }
    for module, (lo, hi, ou) in emplacements.items():
        pm = pos.get(module)
        if pm is None:
            continue
        if (lo is not None and pm < lo) or (hi is not None and pm > hi):
            r.err("module", f"module « {module} » hors de son emplacement fixe — aide : le placer {ou}")
    for avant, apres in (("Critères de décision", "Options considérées"), ("Validation et suivi", "Références")):
        pa, pb = pos.get(avant), pos.get(apres)
        if pa is not None and pb is not None and pa > pb:
            r.err("module", f"« {avant} » doit précéder « {apres} » (emplacements fixes)")

    # 2. Carte d'identité : présence et validité des champs
    champs = parser_identite(texte, r)
    for c in CHAMPS_IDENTITE:
        if c not in champs:
            r.err("identité", f"champ manquant : « {c} »")

    # valeur vide = erreur (un champ présent mais vide n'est pas un champ rempli)
    for c in ("ID", "Statut", "Date de décision"):
        if c in champs and not champs[c]:
            r.err(c, "valeur vide")

    id_adr = champs.get("ID", "")
    if id_adr and not RE_ID.match(id_adr):
        r.err("ID", f"format invalide : « {id_adr} » (attendu ADR-XXXX)")
    # cohérence ID <-> nom de fichier (erreur : le calcul du prochain ID s'appuie sur les deux)
    m_nom = re.search(r"ADR-(\d{4})", Path(chemin).name)
    if id_adr and RE_ID.match(id_adr) and m_nom and id_adr != f"ADR-{m_nom.group(1)}":
        r.err("ID", f"l'ID « {id_adr} » ne correspond pas au nom de fichier — aide : aligner le nom sur l'ID de la Carte d'identité")
    # convention de nommage du fichier
    if m_nom and not re.fullmatch(r"ADR-\d{4}-[a-z0-9][a-z0-9-]*\.md", Path(chemin).name):
        r.warn("fichier", f"nom hors convention « ADR-XXXX-titre-en-kebab-case.md » : « {Path(chemin).name} »")
    # cohérence ID <-> titre H1
    if id_adr and RE_ID.match(id_adr) and h1_id and h1_id != id_adr:
        r.err("titre", f"l'ID du titre H1 (« {h1_id} ») ne correspond pas à la Carte d'identité (« {id_adr} »)")

    statut = champs.get("Statut", "")
    if statut and statut not in STATUTS:
        r.err("Statut", f"« {statut} » hors liste fermée {sorted(STATUTS)}")

    # cohérence Statut <-> liens de remplacement (le statut est le garde-fou n°1 :
    # une décision remplacée ne doit jamais rester lisible comme « en vigueur »)
    a_remplacant = bool(RE_ADR_REF.search(champs.get("Remplacé par", "—")))
    if a_remplacant and statut in ("Proposé", "Accepté", "Rejeté"):
        r.err("Statut", f"« Remplacé par » est renseigné mais le statut est « {statut} » — aide : une ADR remplacée passe au statut « Remplacé » (ou « Déprécié »)")
    if statut == "Remplacé" and not a_remplacant:
        r.err("Statut", "statut « Remplacé » sans « Remplacé par » renseigné — aide : indiquer l'ADR remplaçante")

    date = champs.get("Date de décision", "")
    if date and date != "—":
        if not RE_DATE.match(date):
            r.err("Date de décision", f"format invalide : « {date} » (attendu AAAA-MM-JJ, ou « — » si la source n'est pas datée)")
        else:
            try:
                datetime.date.fromisoformat(date)
            except ValueError:
                r.err("Date de décision", f"date inexistante : « {date} »")

    equipe = champs.get("Équipe / périmètre", "")
    if "Équipe / périmètre" in champs and (not equipe or equipe == "—"):
        r.err("Équipe / périmètre", "valeur vide")

    motscles = champs.get("Mots-clés", "")
    termes = [t.strip() for t in re.split(r"[,;]", motscles) if t.strip() and t.strip() != "—"]
    if "Mots-clés" in champs and not termes:
        r.err("Mots-clés", "au moins un mot-clé requis")
    elif termes and not (3 <= len(termes) <= 6):
        r.warn("Mots-clés", f"{len(termes)} mot(s)-clé(s) — le template en recommande 3 à 6")

    # 3. Résumé : blockquote présent, préfixe de validité, gabarit, une phrase
    resume = section_contenu(texte, titre_noyau_attendu("Résumé de la décision"))
    if resume is not None:
        quote = [l.strip().lstrip(">").strip() for l in resume.splitlines()
                 if l.strip().startswith(">") and l.strip(" >")]
        if not quote:
            r.err("Résumé", "résumé en une phrase manquant (blockquote « > … »)")
        else:
            texte_resume = " ".join(quote)
            # 3-préfixe : **[ADR-XXXX — Statut]**, cohérent avec la Carte d'identité
            m_pref = RE_PREFIXE_RESUME_GRAS.match(texte_resume)
            if not m_pref:
                r.err("Résumé", "préfixe de validité manquant — aide : commencer le résumé par « **[ADR-XXXX — Statut]** » (mêmes valeurs que la Carte d'identité)")
                sans_prefixe = texte_resume
            else:
                if id_adr and RE_ID.match(id_adr) and m_pref.group(1) != id_adr:
                    r.err("Résumé", f"préfixe : ID « {m_pref.group(1)} » ≠ Carte d'identité « {id_adr} »")
                if statut and m_pref.group(2) != statut:
                    r.err("Résumé", f"préfixe : statut « {m_pref.group(2)} » ≠ Carte d'identité « {statut} »")
                sans_prefixe = texte_resume[m_pref.end():]
            # 3-gabarit : les cinq marqueurs de la phrase type
            bas = sans_prefixe.lower()
            manquants = [lib for lib, motif in MARQUEURS_RESUME if not re.search(motif, bas)]
            if manquants:
                r.err("Résumé", "gabarit incomplet — marqueurs absents : " + ", ".join(f"« {m} »" for m in manquants))
            # 3-une-phrase (heuristique : ponctuation finale suivie d'une majuscule)
            if re.search(r"[.!?]\s+[A-ZÀÂÉÈÊËÎÏÔÙÛÜ«]", sans_prefixe.rstrip(" .!?")):
                r.warn("Résumé", "plusieurs phrases détectées — le résumé doit tenir en UNE phrase auto-portante")

        # 3a. Statut « Accepté » incompatible avec un résumé troué
        if statut == "Accepté" and RE_NON_SEANCE.search(resume):
            r.err("Statut", "statut « Accepté » incompatible avec un résumé incomplet (« non … en séance / à ce stade ») : une décision pas mûre reste « Proposé »")
        # 3b. Formules vagues dans le résumé
        m_creux = RE_RESUME_CREUX.search(resume)
        if m_creux:
            r.err("Résumé", f"formule vague dans le résumé (« {m_creux.group(0)} ») — préciser ou retirer")

    # 3a-bis. Statut « Accepté » avec un corps très troué : signal d'immaturité
    if statut == "Accepté":
        n_lacunes = len(RE_NON_SEANCE.findall(texte_hors_code(texte)))
        if n_lacunes > 4:
            r.warn("Statut", f"{n_lacunes} mentions « non … en séance / à ce stade » pour une ADR « Accepté » — décision mûre ? (seuil indicatif : 4)")

    # 3c. Module optionnel présent mais vide → à retirer (pas inclure vide)
    for module in MODULES_OPTIONNELS:
        if module in h2 and module_vide(section_contenu(texte, module)):
            r.err("module", f"module optionnel vide, à retirer : « {module} »")

    # 3c-bis. Sections du noyau sans aucun contenu (un titre nu n'est pas une section)
    for sec in ("Contexte et problème", "Décision", "Conséquences"):
        corps_sec = section_contenu(texte, titre_noyau_attendu(sec))
        if corps_sec is not None and section_sans_contenu(corps_sec):
            r.err("noyau", f"section du noyau vide : « {titre_noyau_attendu(sec)} »")

    # 3c-ter. « Options considérées » : au moins 2 options, et la Décision commence
    # par la phrase type « Option retenue : « X », parce que … »
    corps_options = section_contenu(texte, "Options considérées")
    if corps_options is not None:
        n_options = len(re.findall(r"(?m)^###\s+Option\b", corps_options))
        if n_options < 2:
            r.err("module", "« Options considérées » avec moins de 2 options — aide : une seule option réellement discutée → retirer le module et le mentionner dans le Contexte")
        corps_dec = section_contenu(texte, titre_noyau_attendu("Décision"))
        if corps_dec is not None:
            premiere = next((l.strip() for l in corps_dec.splitlines() if l.strip()), "")
            if not re.match(r"(?i)^Option retenue\s*:.+parce qu", premiere):
                r.err("Décision", "avec « Options considérées », la Décision commence par « Option retenue : « X », parce que … » (la justification fait partie de la structure)")

    # 3d. Références ADR-XXXX du corps (hors code inline et texte ~~barré~~),
    # mémorisées pour vérification contre l'index en lint de dossier.
    corps_refs = texte_hors_code(texte)
    corps_refs = re.sub(r"`[^`\n]*`", "", corps_refs)
    corps_refs = re.sub(r"~~[^~\n]*~~", "", corps_refs)
    refs_champs = set(RE_ADR_REF.findall(champs.get("Remplace", "") + " " + champs.get("Remplacé par", "")))
    r.refs_corps = set(RE_ADR_REF.findall(corps_refs)) - {id_adr} - refs_champs

    # 4. Aucun placeholder ni commentaire de gabarit résiduel
    if "<!--" in texte_hors_code(texte):
        r.err("placeholder", "commentaire de gabarit résiduel « <!-- … --> »")
    texte_ph = texte_pour_placeholders(texte)
    for ph in sorted(set(RE_PLACEHOLDER.findall(texte_ph))):
        if RE_PREFIXE_RESUME.match(ph) or RE_CROCHETS_LEGITIMES.match(ph):
            continue
        r.err("placeholder", f"placeholder non rempli : « {ph} » — aide : pour un crochet légitime, utiliser un lien « [texte](url) » ou « [texte][ref] »")
    for ph in sorted({m.group(0) for m in RE_PLACEHOLDER_TXT.finditer(texte_ph)}):
        r.err("placeholder", f"marqueur de gabarit résiduel : « {ph} »")

    return r, champs


def verifier_liens(index, dossier_complet):
    """Cohérence Remplace / Remplacé par entre les ADR scannées.

    index : { id_adr: (rapport, champs) }
    dossier_complet : True si un dossier entier a été scanné — une référence
    pendante y est une ERREUR (l'ADR visée n'existe pas) ; en lint de
    fichier(s) isolé(s), simple avertissement (cohérence non vérifiable).
    """
    ids = set(index.keys())
    for id_a, (r, champs) in index.items():
        for champ, inverse in (("Remplace", "Remplacé par"), ("Remplacé par", "Remplace")):
            val = champs.get(champ, "—")
            for ref in RE_ADR_REF.findall(val):
                if ref == id_a:
                    r.err(champ, f"référence circulaire vers soi-même ({ref})")
                    continue
                if ref not in ids:
                    if dossier_complet:
                        r.err(champ, f"« {ref} » introuvable dans le dossier scanné — aide : référence pendante (ADR inexistante ou ID erroné)")
                    else:
                        r.warn(champ, f"« {ref} » introuvable dans le périmètre scanné (cohérence non vérifiable en lint mono-fichier)")
                    continue
                cible_champs = index[ref][1]
                retour = cible_champs.get(inverse, "—")
                if id_a not in RE_ADR_REF.findall(retour):
                    r.err(champ, f"lien non réciproque : {id_a} dit « {champ} {ref} » mais {ref} n'a pas « {inverse} {id_a} »")


def verifier_cycles(index):
    """Détecte les cycles du graphe « Remplacé par » (A → B → … → A)."""
    grafo = {id_a: [ref for ref in RE_ADR_REF.findall(champs.get("Remplacé par", "—")) if ref in index]
             for id_a, (_, champs) in index.items()}
    couleur = dict.fromkeys(grafo, 0)  # 0 blanc, 1 en cours, 2 fini
    signales = set()

    def visite(n, chemin):
        couleur[n] = 1
        for v in grafo[n]:
            if couleur[v] == 1:
                cycle = chemin[chemin.index(v):] + [v] if v in chemin else [n, v]
                cle = frozenset(cycle)
                if cle not in signales:
                    signales.add(cle)
                    index[v][0].err("Remplacé par", f"cycle de remplacement : {' → '.join(cycle)}")
            elif couleur[v] == 0:
                visite(v, chemin + [v])
        couleur[n] = 2

    for n in grafo:
        if couleur[n] == 0:
            visite(n, [n])


def collecter(chemins):
    """Retourne (fichiers, dossier_complet, introuvables). INDEX.md (généré) est exclu."""
    fichiers = []
    dossier_complet = False
    introuvables = []
    for c in chemins:
        p = Path(c)
        if p.is_dir():
            dossier_complet = True
            fichiers.extend(f for f in sorted(p.glob("*.md")) if f.name != "INDEX.md")
        elif p.is_file():
            fichiers.append(p)
        else:
            print(f"chemin introuvable : {c}", file=sys.stderr)
            introuvables.append(c)
    return fichiers, dossier_complet, introuvables


# ---------------------------------------------------------------------------
# Index généré (adr/INDEX.md) — point d'entrée de consultation pour un MCP/RAG :
# la validité de chaque décision (statut) est lisible sans ouvrir les fichiers.
# ---------------------------------------------------------------------------

MARQUEUR_INDEX_DEBUT = ("<!-- adr-index : tableau régénéré par « python3 scripts/lint-adr.py --index » "
                        "— ne rien éditer entre ces marqueurs -->")
MARQUEUR_INDEX_FIN = "<!-- adr-index:fin -->"
RE_MARQUEUR_INDEX = re.compile(r"<!-- adr-index[^>]*-->")


def generer_table_index(dossier):
    """Le tableau markdown | ID | Titre | Statut | Remplacé par | trié par ID."""
    entrees = []
    for f in sorted(Path(dossier).glob("*.md")):
        if f.name == "INDEX.md":
            continue
        texte = f.read_text(encoding="utf-8")
        champs = parser_identite(texte)
        h1 = next((t for n, t, _ in titres(texte) if n == 1), f.stem)
        titre = re.sub(r"^ADR-\d{4}\s+—\s+", "", h1)
        entrees.append((
            champs.get("ID", "?"),
            titre,
            champs.get("Statut", "?"),
            champs.get("Remplacé par", "—") or "—",
            f.name,
        ))
    entrees.sort(key=lambda e: (e[0], e[4]))
    lignes = ["| ID | Titre | Statut | Remplacé par |", "|----|-------|--------|--------------|"]
    for id_adr, titre, statut, remplace_par, nom in entrees:
        lignes.append(f"| {id_adr} | [{titre}]({nom}) | {statut} | {remplace_par} |")
    return "\n".join(lignes)


def contenu_index(dossier):
    """Le contenu complet attendu de INDEX.md (préserve tout hors marqueurs)."""
    chemin = Path(dossier) / "INDEX.md"
    bloc = f"{MARQUEUR_INDEX_DEBUT}\n{generer_table_index(dossier)}\n{MARQUEUR_INDEX_FIN}"
    if chemin.is_file():
        existant = chemin.read_text(encoding="utf-8")
        sections = RE_MARQUEUR_INDEX.split(existant)
        if len(sections) == 3:  # avant / (table) / après
            return sections[0] + bloc + sections[2]
        if len(sections) > 3:
            raise ValueError("INDEX.md contient plus d'une paire de marqueurs adr-index")
    # bootstrap : fichier absent ou sans marqueurs
    return (
        "# Index des ADR\n\n"
        "Point d'entrée de consultation : lire ce tableau (ID, statut) **avant** d'ouvrir\n"
        "une ADR, et ne jamais citer comme en vigueur une décision non « Accepté ».\n\n"
        f"{bloc}\n"
    )


def commande_index(dossier, verifier_seulement):
    p = Path(dossier)
    if not p.is_dir():
        print(f"Erreur d'environnement : dossier introuvable : {dossier}", file=sys.stderr)
        return 2
    chemin = p / "INDEX.md"
    attendu = contenu_index(p)
    if verifier_seulement:
        actuel = chemin.read_text(encoding="utf-8") if chemin.is_file() else None
        if actuel != attendu:
            print(f"INDEX désynchronisé : régénérer avec « python3 scripts/lint-adr.py --index {dossier} »")
            return 1
        print(f"INDEX à jour : {chemin}")
        return 0
    chemin.write_text(attendu, encoding="utf-8")
    print(f"INDEX régénéré : {chemin}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Linter d'ADR (format canonique).")
    ap.add_argument("chemins", nargs="*", default=None, help="fichiers ou dossiers (défaut : le dossier adr/ à côté du script)")
    ap.add_argument("--strict", action="store_true", help="les avertissements comptent comme des erreurs")
    ap.add_argument("--index", action="store_true", help="régénère INDEX.md dans le dossier d'ADR puis s'arrête")
    ap.add_argument("--check-index", action="store_true", help="vérifie qu'INDEX.md est à jour (exit 1 sinon)")
    args = ap.parse_args()

    # Défaut robuste : le dossier adr/ du dépôt, résolu depuis le script (pas le cwd).
    chemins = args.chemins or [str(Path(__file__).resolve().parent.parent / "adr")]

    if args.index or args.check_index:
        if len(chemins) != 1:
            print("Erreur : --index / --check-index attendent un seul dossier.", file=sys.stderr)
            return 2
        return commande_index(chemins[0], verifier_seulement=args.check_index)

    fichiers, dossier_complet, introuvables = collecter(chemins)
    if introuvables:
        print(f"Erreur d'environnement : {len(introuvables)} chemin(s) introuvable(s).", file=sys.stderr)
        return 2
    if not fichiers:
        # Dossier existant mais sans ADR = état initial légitime (le corpus démarre vide),
        # pas une erreur. Un chemin introuvable ou un cwd erroné est déjà traité ci-dessus → 2 :
        # on ne réintroduit pas le « faux vert », on reconnaît juste un corpus encore vide.
        print("0 ADR à analyser (dossier vide) — rien à vérifier.")
        return 0

    index = {}
    rapports = []
    statuts_corpus = {}
    for f in fichiers:
        try:
            r, champs = lint_fichier(f)
        except OSError as e:
            print(f"Erreur d'environnement : lecture impossible de {f} ({e})", file=sys.stderr)
            return 2
        rapports.append(r)
        statut_f = champs.get("Statut", "")
        if statut_f in STATUTS:
            statuts_corpus[statut_f] = statuts_corpus.get(statut_f, 0) + 1
        id_adr = champs.get("ID", "")
        if RE_ID.match(id_adr or ""):
            if id_adr in index:
                autre_r, _ = index[id_adr]
                r.err("ID", f"ID dupliqué : « {id_adr} » déjà utilisé par {autre_r.fichier}")
                autre_r.err("ID", f"ID dupliqué : « {id_adr} » aussi utilisé par {f}")
            else:
                index[id_adr] = (r, champs)

    verifier_liens(index, dossier_complet)
    verifier_cycles(index)

    # Références ADR-XXXX du corps : vérifiables seulement en lint de dossier.
    if dossier_complet:
        ids_connus = set(index.keys())
        for r in rapports:
            for ref in sorted(r.refs_corps - ids_connus):
                r.warn("référence", f"« {ref} » cité dans le corps mais introuvable dans le dossier scanné")

    en_ci = bool(os.environ.get("GITHUB_ACTIONS"))
    n_ok = 0
    for r in rapports:
        erreurs = list(r.erreurs)
        avertissements = list(r.avertissements)
        if args.strict:
            erreurs += avertissements
            avertissements = []
        if not erreurs and not avertissements:
            print(f"  OK    {r.fichier}")
            n_ok += 1
        else:
            etat = "ERREUR" if erreurs else "AVERT "
            print(f"  {etat} {r.fichier}")
            for champ, msg in erreurs:
                print(f"          ✗ [{champ}] {msg}")
                if en_ci:
                    print(f"::error file={r.fichier}::[{champ}] {msg}")
            for champ, msg in avertissements:
                print(f"          ⚠ [{champ}] {msg}")
                if en_ci:
                    print(f"::warning file={r.fichier}::[{champ}] {msg}")
            if not erreurs:
                n_ok += 1
        r.erreurs_effectives = erreurs

    n_err = sum(1 for r in rapports if r.erreurs_effectives)
    inventaire = ", ".join(f"{n} {s}" for s, n in sorted(statuts_corpus.items(), key=lambda x: -x[1])) or "aucun statut lisible"
    print(
        f"\nRésumé : {n_ok}/{len(rapports)} conforme(s), {n_err} en erreur "
        f"({len(rapports)} fichier(s) scanné(s))."
        f"\nCorpus par statut : {inventaire}."
    )
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
