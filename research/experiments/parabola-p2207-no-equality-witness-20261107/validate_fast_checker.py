"""Validate drat_check_fast.cpp against the four existing h+2 certificates.

The fast checker differs from drat_check_incremental.cpp in two ways that must
not change the verdict:

  * deletions are found through a Zobrist hash + exact multiset compare instead
    of a backward linear scan (performance only);
  * deleting a clause invalidates the level-0 trail only when that clause is the
    reason of a currently assigned literal (K0707's soundness fix, applied
    locally instead of wholesale).

This script re-checks every committed h+2 certificate with the fast checker,
compares against the recorded receipt, and runs two negative controls (a flipped
literal and a dropped empty clause must both be rejected).

Usage: validate_fast_checker.py [--checker PATH] [--temp DIR]
"""
from __future__ import annotations

import argparse
import gzip
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
CERTS = ["cert-2207-1105", "cert-2531-1267", "cert-2647-1325", "cert-3251-1627"]


def run(checker: Path, cnf: Path, proof: Path):
    t0 = time.time()
    res = subprocess.run([str(checker), str(cnf), str(proof)], capture_output=True, text=True)
    last = res.stdout.strip().splitlines()
    return {"rc": res.returncode, "seconds": round(time.time() - t0, 1),
            "last_line": last[-1] if last else res.stderr.strip()[:200],
            "stats": last[-2] if len(last) > 1 else "",
            "verified": res.returncode == 0 and bool(last) and last[-1].strip() == "VERIFIED"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checker", default=str(Path(tempfile.gettempdir()) / "fastchk" / "drat_fast.exe"))
    args = ap.parse_args()
    checker = Path(args.checker)
    if not checker.exists():
        raise SystemExit(f"missing checker binary: {checker}")
    tmp = Path(tempfile.gettempdir()) / "fastchk"
    tmp.mkdir(parents=True, exist_ok=True)
    records = []
    for name in CERTS:
        dest = OUT / name
        cnf = next(dest.glob("*.cnf"), None)
        drat_gz = next(dest.glob("*.drat.gz"), None)
        receipt = json.loads((dest / "receipt.json").read_text(encoding="utf-8"))
        proof = tmp / f"{name}.drat"
        with gzip.open(drat_gz, "rb") as f, proof.open("wb") as g:
            shutil.copyfileobj(f, g)
        rec = run(checker, cnf, proof)
        rec.update({"cert": name, "p": receipt["p"], "size": receipt["size"],
                    "proof_bytes": proof.stat().st_size,
                    "receipt_verified": receipt.get("verified"),
                    "receipt_check_seconds": receipt.get("check_seconds")})
        print(json.dumps(rec, ensure_ascii=False), flush=True)
        records.append(rec)
        proof.unlink()

    # negative controls on the p=2647 h+2 proof
    dest = OUT / "cert-2647-1325"
    cnf = next(dest.glob("*.cnf"))
    proof = tmp / "neg2647.drat"
    with gzip.open(next(dest.glob("*.drat.gz")), "rb") as f, proof.open("wb") as g:
        shutil.copyfileobj(f, g)
    lines = proof.read_text(encoding="ascii").splitlines()
    i = len(lines) // 3
    while i < len(lines) and (not lines[i].strip() or lines[i][0] == "d"):
        i += 1
    lits = lines[i].split()
    lits[0] = str(-int(lits[0]))
    flipped = tmp / "neg2647_flip.drat"
    flipped.write_text("\n".join(lines[:i] + [" ".join(lits)] + lines[i + 1:]) + "\n", encoding="ascii")
    noempty = tmp / "neg2647_noempty.drat"
    noempty.write_text("\n".join(lines[:-1]) + "\n", encoding="ascii")
    negatives = []
    for path, label in ((flipped, "flipped_literal"), (noempty, "dropped_empty_clause")):
        rec = run(checker, cnf, path)
        rec.update({"control": label, "rejected": not rec["verified"]})
        print(json.dumps(rec, ensure_ascii=False), flush=True)
        negatives.append(rec)

    summary = {
        "checker": str(checker),
        "checker_source": "research/experiments/parabola-p2207-no-equality-witness-20261107/drat_check_fast.cpp",
        "certs": records,
        "all_verified": all(r["verified"] for r in records),
        "matches_receipts": all(r["verified"] == bool(r["receipt_verified"]) for r in records),
        "negative_controls_all_rejected": all(r["rejected"] for r in negatives),
        "negatives": negatives,
        "speedups": {r["cert"]: (round(r["receipt_check_seconds"] / r["seconds"], 2)
                                 if r["seconds"] else None) for r in records},
    }
    (OUT / "fast_checker_validation.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in summary.items() if k not in ("certs", "negatives")},
                     ensure_ascii=False), flush=True)
    return 0 if summary["all_verified"] and summary["negative_controls_all_rejected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
