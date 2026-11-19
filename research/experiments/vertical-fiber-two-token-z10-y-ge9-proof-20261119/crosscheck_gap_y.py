#!/usr/bin/env python3
"""K1011 independent cross-check: published-verifier rerun + gap-y engine corroboration.

Lane-B (independent lane) verification of K1011 (z=10, y>=9 uniform full Grundy):

(1) Reproduce the published verifier verify_z10_y_ge9_proof.py twice in fresh
    processes, require byte-identical stdout, all_pass, and semantic agreement
    with the published output/audit.json.
(2) Direct two-engine corroboration at y in {13,14,16,17,18} (the sampling gap
    between the published audit's direct_y = {9,10,11,12,15,20}), plus spot
    y in {21,25,30} and deep-d runs, against the published candidate formula
    H(R;(x,y);10) (K1002 uniform restricted to y>=9), R over 0..x+y+13.

Finite corroboration only; the universal claim rests on the two-stage
induction published in report.md.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import verify_z10_y_ge9_proof as pub  # noqa: E402  published K1011 verifier


def odd(r, lo, hi):
    return lo <= r <= hi and r % 2 == 1


def even(r, lo, hi):
    return lo <= r <= hi and r % 2 == 0


# ------------------------------------------------- engines (independent lane)
# order-preserving tupled recursion and descending-canonical recursion over
# position (r, tokens=(x,y), height=10); "10" is fixed here as the initial
# residual height z, matching the published verifier's make_engines contract.
def make_engines():
    @lru_cache(None)
    def ordered(r, tokens, z):
        if r == 0:
            return 0
        opts = set()
        for i, v in enumerate(tokens):
            if v > 1:
                opts.add(ordered(r - 1, tokens[:i] + (v - 1,) + tokens[i + 1:], z))
            else:
                opts.add(ordered(r - 1, tokens[:i] + tokens[i + 1:], z + 1))
        if z:
            opts.add(1 ^ ordered(r - 1, tokens, z - 1))
        return mex(opts)

    @lru_cache(None)
    def canonical(r, tokens, z):
        if r == 0:
            return 0
        opts = set()
        seen = set()
        for i, v in enumerate(tokens):
            if v in seen:
                continue
            seen.add(v)
            if v > 1:
                child = tuple(sorted(tokens[:i] + (v - 1,) + tokens[i + 1:], reverse=True))
                opts.add(canonical(r - 1, child, z))
            else:
                child = tuple(sorted(tokens[:i] + tokens[i + 1:], reverse=True))
                opts.add(canonical(r - 1, child, z + 1))
        if z:
            opts.add(1 ^ canonical(r - 1, tokens, z - 1))
        return mex(opts)

    return ordered, canonical


def mex(values):
    g = 0
    while g in values:
        g += 1
    return g


# ---------------------------------------------- (1) published verifier rerun
def verifier_rerun():
    """Rerun the published verifier twice in an isolated temp tree (its run()
    rewrites output/audit.json, so never execute it inside this experiment dir),
    require byte-identical stdout and a byte-identical regenerated audit.json
    against the published blob."""
    pub_audit_path = HERE / "output" / "audit.json"
    pub_bytes = pub_audit_path.read_bytes()
    tmp = tempfile.mkdtemp(prefix="k1011rerun_")
    try:
        shutil.copy2(HERE / "verify_z10_y_ge9_proof.py", Path(tmp) / "verify_z10_y_ge9_proof.py")
        outs = []
        for _ in range(2):
            p = subprocess.run([sys.executable, str(Path(tmp) / "verify_z10_y_ge9_proof.py")],
                               capture_output=True, text=True, cwd=tmp)
            assert p.returncode == 0, p.stderr[-500:]
            outs.append(p.stdout.strip())
        reproducible = outs[0] == outs[1]
        run_stdout = json.loads(outs[0])
        regen_bytes = (Path(tmp) / "output" / "audit.json").read_bytes()
        regen = json.loads(regen_bytes)
        matches = (run_stdout["all_pass"] is True and regen["all_pass"] is True
                   and run_stdout["counts"] == regen["counts"] == json.loads(pub_bytes)["counts"]
                   and run_stdout["sha256_without_hash_field"] == regen["sha256_without_hash_field"]
                   and run_stdout["total_checks"] == regen["total_checks"]
                   and run_stdout["failures"] in (0, []) and regen["failures"] in (0, []))
        regen_identical_blob = regen_bytes == pub_bytes
        return {
            "rerunable_byte_identical": reproducible,
            "matches_published_audit_semantics": matches,
            "regenerated_audit_blob_identical": regen_identical_blob,
            "run_stdout_sha256": hashlib.sha256(outs[0].encode()).hexdigest(),
            "published_audit_json_sha256": hashlib.sha256(pub_bytes).hexdigest(),
            "total_checks": run_stdout["total_checks"],
        }
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------- (2) gap-y engine corroboration
GAP_Y = [13, 14, 16, 17, 18]      # missing rows in the published direct_y sample
GAP_DMAX = 30
SPOT = [21, 25, 30]
SPOT_DMAX = 12
DEEP = [(13, 60), (16, 60), (13, 200), (18, 100)]


def engine_gap():
    cand = pub.candidate
    rows = []
    failures = []
    total = 0
    planned = [(y, GAP_DMAX) for y in GAP_Y]
    planned += [(y, SPOT_DMAX) for y in SPOT]
    planned += DEEP
    for y, dmax in planned:
        ordered, canonical = make_engines()  # fresh memory per (y, dmax)
        checks = 0
        bad = 0
        for x in range(y, y + dmax + 1):
            S = x + y
            tokens = (x, y)
            for r in range(0, S + 14):
                vo = ordered(r, tokens, 10)
                vc = canonical(r, tokens, 10)
                cf = cand(x, y, r)
                checks += 1
                if not (vo == vc == cf):
                    bad += 1
                    if len(failures) < 50:
                        failures.append({"x": x, "y": y, "r": r,
                                         "ordered": vo, "canonical": vc, "formula": cf})
        rows.append({"y": y, "dmax": dmax, "pairs": dmax + 1,
                     "checks": checks, "failures": bad})
        print("y=%d dmax=%d checks=%d failures=%d" % (y, dmax, checks, bad), flush=True)
        total += checks
    return {"rows": rows, "total_checks": total, "failures": failures}


def main():
    vr = verifier_rerun()
    eg = engine_gap()
    out = {
        "crosscheck": "K1011 independent rerun + gap-y engine corroboration (lane B)",
        "formula": "verify_z10_y_ge9_proof.candidate (K1002 uniform, y>=9 restriction)",
        "engines": "independent in-file order-preserving + descending-canonical mex recursions",
        "range": ("gap y={13,14,16,17,18} d=0..30, spot y={21,25,30} d=0..12, "
                  "deep (y,dmax)={(13,60),(16,60),(13,200),(18,100)}, 0<=R<=x+y+13"),
        "verifier_rerun": vr,
        "engine_gap": eg,
        "all_pass": (vr["rerunable_byte_identical"] and vr["matches_published_audit_semantics"]
                     and eg["failures"] == []),
    }
    print(json.dumps(out))
    (HERE / "output" / "crosscheck_gap_y.json").write_text(
        json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
