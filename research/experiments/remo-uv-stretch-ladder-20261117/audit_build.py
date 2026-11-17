#!/usr/bin/env python3
"""Deterministic audit builder for the U/V stretch-sieve + unified weight ladder run.

Runs the three verifiers fresh (they are deterministic), parses their printed
summaries, pins every input/output file by sha256, and writes
output/uv_stretch_ladder_audit.json. Running this script twice must produce
byte-identical output.
"""
import ast
import hashlib
import json
import re
import subprocess
import sys


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def run(args):
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stdout + p.stderr)
        raise SystemExit(f"verifier failed: {args}")
    return p.stdout


def main():
    # --- SIEVE (stretch-sieve conjecture, pins mode) ---
    out = run([sys.executable, "sieve_test.py", "8000", "pins"])
    m = re.search(r"N=(\d+): V violations=(\d+)  U violations=(\d+)  "
                  r"pin mismatches=(\d+)", out)
    if not m:
        raise SystemExit("cannot parse sieve_test output")
    n, bv, bu, bp = (int(x) for x in m.groups())
    mv = re.search(r"V \(pot_at, held-pot\) counts: (\[.*\])", out)
    mu = re.search(r"U \(pot_at, held-pot\) counts: (\[.*\])", out)
    top_v = [[list(k), c] for k, c in ast.literal_eval(mv.group(1))]
    top_u = [[list(k), c] for k, c in ast.literal_eval(mu.group(1))]
    sieve = {
        "N": n,
        "v_violations": bv,
        "u_violations": bu,
        "pin_mismatches": bp,
        "top_v_deaths": top_v,
        "top_u_deaths": top_u,
    }
    # --- STR2 (stretch-2 end-state theorems + 6-reduction + SIEVE3-U) ---
    out = run([sys.executable, "theorem_verify.py"])
    m = re.search(r"m in \[(\d+),(\d+)\]: checks=(\d+) failures=(\d+)", out)
    if not m:
        raise SystemExit("cannot parse theorem_verify output")
    mlo, mhi, nch, nfail = (int(x) for x in m.groups())
    str2 = {"m_lo": mlo, "m_hi": mhi, "checks": nch, "failures": nfail}
    # --- LADDER (restricted unified weight ladder) ---
    out = run([sys.executable, "ladder_verify.py"])
    lines = [l for l in out.splitlines() if l.strip()]
    ok_lines = [l for l in lines if l.endswith(": OK")]
    m = re.search(r"total checks: (\d+)", out)
    if not m or len(ok_lines) != 18:
        raise SystemExit("cannot parse ladder_verify output")
    ladder = {"grid_lines": len(ok_lines), "checks": int(m.group(1)),
              "failures": 0}
    # --- pins ---
    pins = {
        "sieve_test.py": sha256("sieve_test.py"),
        "theorem_verify.py": sha256("theorem_verify.py"),
        "ladder_verify.py": sha256("ladder_verify.py"),
        "w3_explore.py": sha256("w3_explore.py"),
        "data/w3_explore.json": sha256("data/w3_explore.json"),
        "../remo-pc-twin-laws-20261117/data/pc_uv8000.json":
            sha256("../remo-pc-twin-laws-20261117/data/pc_uv8000.json"),
        "../remo-pc-twin-laws-20261117/data/pc_p8000.json":
            sha256("../remo-pc-twin-laws-20261117/data/pc_p8000.json"),
    }
    checks = [
        {
            "name": ("SIEVE: on the U/V reduced games (K0928), for all m<=8000 "
                     "the watched label dies exactly at the pot-(spf-1) "
                     "stretch: V label 0 dies holding spf(2m+1) (hot, delta 1) "
                     "when 2m+1 is composite and survives iff prime; U label "
                     "m-1 dies holding spf(2m+3)-1 (cold, delta 0) when 2m+3 "
                     "is composite and survives iff prime; survivors match "
                     "the committed U/V tables (K0929)"),
            "ok": (bv == 0 and bu == 0 and bp == 0),
            "data": sieve,
        },
        {
            "name": ("STR2: stretch-2 end-state theorems on the U/V reduced "
                     "games, V(m) length ceil((m-1)/3) with block losers at "
                     "labels 1 mod 3 and breaking losers 0/2/3 by m mod 3, "
                     "U(m) length ceil((m+1)/3) with block losers 2 mod 3 and "
                     "breaking losers 3/1/0 by m mod 3, the 6-reduction to "
                     "W3/H3/G3 shapes, and SIEVE3-U (U label m-1 dies in "
                     "stretch 2 iff m = 0 mod 3); all survivors pinned "
                     "against the committed tables"),
            "ok": nfail == 0,
            "data": str2,
        },
        {
            "name": ("LADDER: restricted unified weight ladder F(w,h;n) "
                     "(first n-h players hold w, last h hold w+1 hot, pot w, "
                     "ptr 0; rule applies for h=0 all r, or h>=1 with r=0 or "
                     "r>=h; the open class h>=2 with 1<=r<h is skipped): "
                     "grids w=2 n<=1000, w=3 n<=800, w=4 n<=250, w=5 n<=150, "
                     "all h=0..w"),
            "ok": ladder["failures"] == 0,
            "data": ladder,
        },
        {
            "name": ("W3EXPLORE: deterministic W3/H3/G3 stretch-3 exploration "
                     "data (end-state shapes by n mod 4, position-0 death "
                     "levels) pinned by sha256"),
            "ok": True,
            "data": {"sha256": pins["data/w3_explore.json"]},
        },
    ]
    audit = {
        "all_ok": all(c["ok"] for c in checks),
        "checks": checks,
        "date": "2026-11-17",
        "follows": (
            "K0859 (REMO counting recursion, the uniform-board survivor P(C) "
            "via theorem D), K0928 (pot formulation, Lemma E/O, Theorem RED "
            "reducing P(C) to the U/V reduced games and pinning their tables "
            "m<=8000), K0929 (twin prime laws LAW1/LAW2 as conjectures whose "
            "mod-6 composite classes this run resolves universally via "
            "STR2/SIEVE3-U), K0919/K0926 (P(C) pins C=1..40 and plateau "
            "universality anchoring the committed tables)"),
        "items": ["K0931"],
        "pins": pins,
        "title": (
            "U/V stretch structure for the reduced REMO games and a unified "
            "weight ladder: proved STR2-V/U (stretch-2 end states with "
            "lengths and loser classes), SIEVE3-U (U label m-1 dies in "
            "stretch-2 iff 3|m), the twin-law mod-6 resolution (LAW1 "
            "universal on composites C=3 mod 6, C>=9; LAW2 universal on "
            "composites C=2 mod 6, C>=8), the 6-reduction V/U -> W3/H3/G3, "
            "and LAD h=0 (stretch-w ladder end state for every w, frame "
            "induction proof); the restricted ladder F(w,h;n) is "
            "machine-verified on four grids (8,282 checks) with the open "
            "class h>=2, 1<=r<h excluded; the SIEVE conjecture (death level "
            "= spf-1 mechanism) is machine-verified m<=8000 with 0 "
            "violations and remains unproven in general"),
    }
    with open("output/uv_stretch_ladder_audit.json", "w") as f:
        json.dump(audit, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print("all_ok =", audit["all_ok"])


if __name__ == "__main__":
    main()
