#!/usr/bin/env python3
"""Cross-check of the K1023 all-z Theorem P1 verifier against the
independently authored K1022 (z >= 6) verifier.

Motivation.  The sibling experiment
`vertical-fiber-two-token-y1-parametric-proof-20261119` (K1022) proves the
two-token 1-parametric vertical-fiber candidate for z >= 6 only, from a
verbatim census of published z-slice verifiers.  The K1023 result in this
directory extends the universal theorem to ALL z >= 1 plus the z = 0 base
case cand0, via a type-machine construction.  The two artifacts were built
by different derivations, so agreement between their closed forms and raw
game engines is a genuinely independent double anchor.

Checks (checking their verifier is fetched from the sibling directory):

  (a) census-formula agreement on their theorem's domain:
      z = 6..80, x = 1..60, R = 0 .. x+z+100  (both closed forms),
  (b) far-z probes: z in {97, 98, 997, 998, 2999, 3000}, x <= 30,
      R = 0 .. x+z+29 (both closed forms; both are census-derived formulas,
      so agreement here is transcription/extension agreement, not a raw
      check),
  (c1) K1023 extension domain z = 1..5, x = 1..25, R = 0 .. x+z+30:
      K1023 cand == their H_canonical == their H_ordered raw recursions,
  (c2) z = 0 base case, x = 1..25, R = 0 .. 2x+30:
      K1023 cand0 == their H_canonical == their H_ordered raw recursions
      (their published theorem excludes z = 0; their raw engines still
      define ground truth, so this directly double-anchors cand0),
  (c3) z = 0 wide grid, x = 26..40, R = 0 .. 2x+10:
      K1023 cand0 == their H_canonical.

Output: output/cross_check_k1022.json (byte-stable; no provenance fields
coupled to the sibling's file bytes).  Exit status 1 on any mismatch or if
the sibling verifier cannot be located; 0 with all checks PASS otherwise.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIBLING = HERE.parent / "vertical-fiber-two-token-y1-parametric-proof-20261119" / "verify_y1_parametric_proof.py"
SELF = HERE / "verify_p1_universal.py"
OUT = HERE / "output"


def _load(name, path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    result = {"checks": []}

    def record(name, grid, points, mismatches):
        result["checks"].append(
            dict(name=name, grid=grid, points=points, status="PASS" if mismatches == 0 else "FAIL")
        )

    if not SIBLING.is_file() or not SELF.is_file():
        result["sibling_present"] = bool(SIBLING.is_file())
        result["self_present"] = bool(SELF.is_file())
        OUT.mkdir(exist_ok=True)
        (OUT / "cross_check_k1022.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print("CROSS-CHECK INCOMPLETE: missing verifier file(s)", file=sys.stderr)
        return 1

    theirs = _load("k1022_verifier", SIBLING)
    mine = _load("k1023_verifier", SELF)

    # (a) closed-form agreement, z = 6..80 (their theorem's domain)
    n = mism = 0
    for z in range(6, 81):
        rmax = z + 100
        for x in range(1, 61):
            for r in range(0, x + rmax):
                n += 1
                if theirs.cand(z, x, r) != mine.cand(z, x, r):
                    mism += 1
    record(
        "(a) closed forms agree, z=6..80 x<=60 R<x+z+100",
        "z=6..80, x=1..60, R=0..x+z+99, K1022 cand == K1023 cand", n, mism)

    # (b) far probes
    n = mism = 0
    for z in (97, 98, 997, 998, 2999, 3000):
        for x in range(1, 31):
            for r in range(0, x + z + 30):
                n += 1
                if theirs.cand(z, x, r) != mine.cand(z, x, r):
                    mism += 1
    record(
        "(b) closed forms agree, far z",
        "z in {97,98,997,998,2999,3000}, x<=30, R<x+z+30, both census-derived formulas",
        n, mism)

    # (c1) extension domain z = 1..5 vs their raw engines
    n = mism = 0
    for z in range(1, 6):
        for x in range(1, 26):
            X = (x, 1)
            for r in range(0, x + z + 31):
                n += 1
                c = mine.cand(z, x, r)
                ho = theirs.H_ordered(r, X, z)
                hc = theirs.H_canonical(r, X, z)
                if not (c == ho == hc):
                    mism += 1
        theirs.H_ordered.cache_clear()
        theirs.H_canonical.cache_clear()
    record(
        "(c1) z=1..5 vs raw engines",
        "z=1..5, x<=25, R<=x+z+30, K1023 cand == K1022 H_canonical == K1022 H_ordered",
        n, mism)

    # (c2) z = 0 base case vs their raw engines
    n = mism = 0
    for x in range(1, 26):
        X = (x, 1)
        for r in range(0, 2 * x + 31):
            n += 1
            c = mine.cand0(x, r)
            ho = theirs.H_ordered(r, X, 0)
            hc = theirs.H_canonical(r, X, 0)
            if not (c == ho == hc):
                mism += 1
        theirs.H_ordered.cache_clear()
        theirs.H_canonical.cache_clear()
    record(
        "(c2) z=0 base vs raw engines",
        "z=0, x<=25, R<=2x+30, K1023 cand0 == K1022 H_canonical == K1022 H_ordered",
        n, mism)

    # (c3) z = 0 wide grid, canonical engine
    n = mism = 0
    for x in range(26, 41):
        X = (x, 1)
        for r in range(0, 2 * x + 11):
            n += 1
            if mine.cand0(x, r) != theirs.H_canonical(r, X, 0):
                mism += 1
        theirs.H_canonical.cache_clear()
        theirs.H_ordered.cache_clear()
    record(
        "(c3) z=0 wide grid",
        "z=0, x=26..40, R<=2x+10, K1023 cand0 == K1022 H_canonical", n, mism)

    result["overall"] = "PASS" if all(c["status"] == "PASS" for c in result["checks"]) else "FAIL"

    OUT.mkdir(exist_ok=True)
    (OUT / "cross_check_k1022.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")

    for c in result["checks"]:
        print(f'{c["status"]}  {c["name"]}: {c["points"]} points')
    print("OVERALL:", result["overall"])
    return 0 if result["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
