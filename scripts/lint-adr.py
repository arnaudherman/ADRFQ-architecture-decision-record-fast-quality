#!/usr/bin/env python3
"""Linter d'ADR — vérifie le format canonique (noyau, Carte d'identité, liens).

Usage :
    python3 scripts/lint-adr.py [chemins...]   # défaut : adr/

Sort en code 1 si au moins une erreur est détectée, 0 sinon.
Aucune dépendance externe (bibliothèque standard uniquement).
"""

import argparse
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
RE_TABLE_ROW = re.compile(r"^\|(.+)\|(.+)\|\s*$")
RE_HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$")
RE_ADR_REF = re.compile(r"ADR-\d{4}")
# Placeholder = [texte] qui n'est PAS un lien markdown [texte](url).
RE_PLACEHOLDER = re.compile(r"\[[^\]\n]+\](?!\()")
MODULES_OPTIONNELS = [
    "Critères de décision",
    "Options considérées",
    "Validation et suivi",
    "Références",
]
# « non documenté / évalué(e)(s) / tranché en séance » et variantes.
RE_NON_SEANCE = re.compile(r"non\s+\w+\s+en\s+séance", re.IGNORECASE)
# Formules vagues, interdites dans le résumé (bloc lu en priorité par l'IA).
RE_RESUME_CREUX = re.compile(r"\betc\b\.?|d'autres compromis|\bdivers\b", re.IGNORECASE)


class Rapport:
    def __init__(self, fichier):
        self.fichier = fichier
        self.erreurs = []
        self.avertissements = []

    def err(self, champ, msg):
        self.erreurs.append((champ, msg))

    def warn(self, champ, msg):
        self.avertissements.append((champ, msg))


def parser_identite(texte):
    """Extrait les lignes du tableau Carte d'identité -> dict champ: valeur."""
    champs = {}
    for ligne in texte.splitlines():
        m = RE_TABLE_ROW.match(ligne)
        if not m:
            continue
        cle = m.group(1).strip()
        val = m.group(2).strip()
        if cle in ("Champ", "---", ":---", "---:") or set(cle) <= {"-", ":", " "}:
            continue
        if cle in CHAMPS_IDENTITE and cle not in champs:
            champs[cle] = val
    return champs


def titres(texte):
    return [m.group(1) for ligne in texte.splitlines() if (m := RE_HEADING.match(ligne))]


def section_contenu(texte, fragment_titre):
    """Renvoie le texte sous le 1er heading contenant fragment_titre, jusqu'au heading suivant de même niveau ou supérieur."""
    lignes = texte.splitlines()
    debut = None
    niveau = 0
    for i, ligne in enumerate(lignes):
        m = RE_HEADING.match(ligne)
        if m and fragment_titre in m.group(1):
            debut = i + 1
            niveau = len(ligne) - len(ligne.lstrip("#"))
            break
    if debut is None:
        return None
    corps = []
    for ligne in lignes[debut:]:
        m = RE_HEADING.match(ligne)
        if m:
            n = len(ligne) - len(ligne.lstrip("#"))
            if n <= niveau:
                break
        corps.append(ligne)
    return "\n".join(corps)


def module_vide(corps):
    """Vrai si le corps d'un module n'a aucun contenu réel, ou seulement des
    mentions « non … en séance » (sous-titres et puces ignorés)."""
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

    # 1. Sections du noyau présentes
    tt = titres(texte)
    for sec in SECTIONS_NOYAU:
        if not any(sec in t for t in tt):
            r.err("noyau", f"section manquante : « {sec} »")

    # 2. Carte d'identité : présence et validité des champs
    champs = parser_identite(texte)
    for c in CHAMPS_IDENTITE:
        if c not in champs:
            r.err("identité", f"champ manquant : « {c} »")

    id_adr = champs.get("ID", "")
    if id_adr and not RE_ID.match(id_adr):
        r.err("ID", f"format invalide : « {id_adr} » (attendu ADR-XXXX)")
    # cohérence ID <-> nom de fichier
    m_nom = re.search(r"ADR-(\d{4})", Path(chemin).name)
    if id_adr and RE_ID.match(id_adr) and m_nom and id_adr != f"ADR-{m_nom.group(1)}":
        r.warn("ID", f"l'ID « {id_adr} » ne correspond pas au nom de fichier")

    statut = champs.get("Statut", "")
    if statut and statut not in STATUTS:
        r.err("Statut", f"« {statut} » hors liste fermée {sorted(STATUTS)}")

    date = champs.get("Date de décision", "")
    if date and not RE_DATE.match(date):
        r.err("Date de décision", f"format invalide : « {date} » (attendu AAAA-MM-JJ)")

    equipe = champs.get("Équipe / périmètre", "")
    if "Équipe / périmètre" in champs and (not equipe or equipe == "—"):
        r.err("Équipe / périmètre", "valeur vide")

    motscles = champs.get("Mots-clés", "")
    termes = [t.strip() for t in re.split(r"[,;]", motscles) if t.strip() and t.strip() != "—"]
    if "Mots-clés" in champs and not termes:
        r.err("Mots-clés", "au moins un mot-clé requis")

    # 3. Résumé en une phrase présent (blockquote non vide sous la section)
    resume = section_contenu(texte, "Résumé de la décision")
    if resume is not None:
        quote = [l for l in resume.splitlines() if l.strip().startswith(">") and l.strip(" >")]
        if not quote:
            r.err("Résumé", "résumé en une phrase manquant (blockquote « > … »)")

        # 3a. Statut « Accepté » incompatible avec un résumé troué
        if statut == "Accepté" and RE_NON_SEANCE.search(resume):
            r.err("Statut", "statut « Accepté » incompatible avec un résumé incomplet (« non … en séance ») : une décision pas mûre reste « Proposé »")
        # 3b. Formules vagues dans le résumé
        m_creux = RE_RESUME_CREUX.search(resume)
        if m_creux:
            r.err("Résumé", f"formule vague dans le résumé (« {m_creux.group(0)} ») — préciser ou retirer")

    # 3c. Module optionnel présent mais vide → à retirer (pas inclure vide)
    for module in MODULES_OPTIONNELS:
        if any(module in t for t in tt) and module_vide(section_contenu(texte, module)):
            r.err("module", f"module optionnel vide, à retirer : « {module} »")

    # 4. Aucun placeholder ni commentaire de gabarit résiduel
    if "<!--" in texte:
        r.err("placeholder", "commentaire de gabarit résiduel « <!-- … --> »")
    for ph in sorted(set(RE_PLACEHOLDER.findall(texte))):
        r.err("placeholder", f"placeholder non rempli : « {ph} »")

    return r, champs


def verifier_liens(index):
    """Cohérence Remplace / Remplacé par entre les ADR scannées.

    index : { id_adr: (rapport, champs) }
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
                    r.warn(champ, f"« {ref} » introuvable dans le périmètre scanné (cohérence non vérifiable)")
                    continue
                cible_champs = index[ref][1]
                retour = cible_champs.get(inverse, "—")
                if id_a not in RE_ADR_REF.findall(retour):
                    r.err(champ, f"lien non réciproque : {id_a} dit « {champ} {ref} » mais {ref} n'a pas « {inverse} {id_a} »")


def collecter(chemins):
    fichiers = []
    for c in chemins:
        p = Path(c)
        if p.is_dir():
            fichiers.extend(sorted(p.glob("*.md")))
        elif p.is_file():
            fichiers.append(p)
        else:
            print(f"chemin introuvable : {c}", file=sys.stderr)
    return fichiers


def main():
    ap = argparse.ArgumentParser(description="Linter d'ADR (format canonique).")
    ap.add_argument("chemins", nargs="*", default=["adr"], help="fichiers ou dossiers (défaut : adr/)")
    args = ap.parse_args()

    fichiers = collecter(args.chemins)
    if not fichiers:
        print("Aucun fichier .md à analyser.")
        return 0

    index = {}
    rapports = []
    for f in fichiers:
        r, champs = lint_fichier(f)
        rapports.append(r)
        id_adr = champs.get("ID", "")
        if RE_ID.match(id_adr or ""):
            index[id_adr] = (r, champs)

    verifier_liens(index)

    n_ok = 0
    for r in rapports:
        if not r.erreurs and not r.avertissements:
            print(f"  OK    {r.fichier}")
            n_ok += 1
        else:
            etat = "ERREUR" if r.erreurs else "AVERT "
            print(f"  {etat} {r.fichier}")
            for champ, msg in r.erreurs:
                print(f"          ✗ [{champ}] {msg}")
            for champ, msg in r.avertissements:
                print(f"          ⚠ [{champ}] {msg}")
            if not r.erreurs:
                n_ok += 1

    n_err = sum(1 for r in rapports if r.erreurs)
    print(
        f"\nRésumé : {n_ok}/{len(rapports)} conforme(s), {n_err} en erreur "
        f"({len(rapports)} fichier(s) scanné(s))."
    )
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
