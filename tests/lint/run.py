#!/usr/bin/env python3
"""Tests de non-régression du linter d'ADR (stdlib uniquement).

Usage : python3 tests/lint/run.py

Quatre vérifications :
  1. le dossier témoin (tests/lint/temoin/) produit EXACTEMENT la sortie
     figée dans sortie-attendue.txt, avec le code de sortie 1 ;
  2. le corpus réel (adr/, puis chaque fixture séparément) est conforme (code 0) ;
  3. la paire de consultation (tests/fixtures/consultation/) est conforme —
     réciprocité Remplace/Remplacé-par et cohérence des statuts comprises ;
  4. un chemin inexistant est une erreur d'ENVIRONNEMENT (code 2, jamais
     un faux vert).

Sort en code 1 si au moins une vérification échoue.
Après une évolution VOULUE des règles : régénérer le snapshot avec
  python3 scripts/lint-adr.py tests/lint/temoin > tests/lint/sortie-attendue.txt
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LINTER = REPO / "scripts" / "lint-adr.py"
SNAPSHOT = REPO / "tests" / "lint" / "sortie-attendue.txt"


def lancer(*args):
    return subprocess.run(
        [sys.executable, str(LINTER), *args],
        capture_output=True, text=True, cwd=REPO,
    )


def main():
    echecs = []

    # 1. Témoin cassé : sortie identique au snapshot, code 1
    res = lancer("tests/lint/temoin")
    attendu = SNAPSHOT.read_text(encoding="utf-8")
    if res.returncode != 1:
        echecs.append(f"témoin : code de sortie {res.returncode} (attendu 1)")
    if res.stdout != attendu:
        echecs.append("témoin : la sortie du linter diverge du snapshot sortie-attendue.txt")
        for ligne in _diff(attendu, res.stdout):
            print(f"    {ligne}")

    # 2. Corpus réel conforme (adr/ d'un côté ; chaque fixture séparément —
    # les fixtures ne font pas partie du corpus, leurs ID ne s'y confrontent pas)
    res = lancer("adr")
    if res.returncode != 0:
        echecs.append(f"corpus adr/ : code de sortie {res.returncode} (attendu 0)\n{res.stdout}")
    for fixture in ("tests/fixtures/ADR-attendue-pv-pauvre.md",
                    "tests/fixtures/ADR-produite-test-2026-06-10.md",
                    "tests/fixtures/ADR-attendue-entretien.md"):
        res = lancer(fixture)
        if res.returncode != 0:
            echecs.append(f"fixture {fixture} : code de sortie {res.returncode} (attendu 0)\n{res.stdout}")

    # 3. Paire de consultation (Remplacé ↔ Remplaçant) conforme
    res = lancer("tests/fixtures/consultation")
    if res.returncode != 0:
        echecs.append(f"paire de consultation : code de sortie {res.returncode} (attendu 0)\n{res.stdout}")

    # 4. Échec fermé sur chemin introuvable
    res = lancer("tests/lint/dossier-inexistant")
    if res.returncode != 2:
        echecs.append(f"chemin introuvable : code de sortie {res.returncode} (attendu 2)")

    if echecs:
        print("ÉCHEC des tests du linter :")
        for e in echecs:
            print(f"  ✗ {e}")
        return 1
    print("OK — 4/4 vérifications du linter passées (snapshot, corpus, consultation, échec fermé).")
    return 0


def _diff(attendu, obtenu):
    """Diff unifié tronqué, pour localiser la divergence de snapshot."""
    import difflib
    return list(difflib.unified_diff(
        attendu.splitlines(), obtenu.splitlines(),
        fromfile="sortie-attendue.txt", tofile="sortie-obtenue", lineterm="",
    ))[:40]


if __name__ == "__main__":
    sys.exit(main())
