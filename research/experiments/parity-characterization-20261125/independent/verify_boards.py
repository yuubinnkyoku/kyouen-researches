#!/usr/bin/env python3
"""Independent verifier for the parity characterization K1298 (task 2).

Written from scratch for the audit; no code is shared with the original
experiment under ``parity-characterization-20261125/scripts``.

Model
-----
A board is ``(n, blocks)`` where ``blocks`` is a family of subsets of
``{0,...,n-1}``.  For a fixed integer ``s >= 0`` the positions are the sets
``S`` with ``|S & B| <= s`` for every block ``B``; a move adds one point.
Normal play (no move loses), misere play (no move wins).

For every (board, s) we compute

  * ``G`` : Grundy values of all positions (descending bitmask order),
  * ``Max`` : maximal safe sets (safe sets with no safe one-point extension),
  * (a) all Grundy values in {0,1},
  * (b) all sets in Max have the same size parity,
  * (c) for every position S, all maximal safe supersets of S have the
        same size parity (computed by a superset zeta transform),
  * localized corollary: for every position S,
        (all G(T) for safe T >= S are in {0,1})  <=>  (c) holds at S,
  * if (b) holds with parity p:
        G(S) == (p - |S|) mod 2                        for all positions S,
        misere_win(S) == ((p - |S|) is even)           for all positions S,
        where misere_win is computed by its own recursion
        (terminal position = win for the player to move).

Families
--------
exhaustive_n4 : n=4, all families of 2- and 3-subsets (2^10 boards), s=2,3.
exhaustive_n5 : n=5, all families of 3-subsets      (2^10 boards), s=2,3.
random_n6n7   : 3000 boards (1500 with n=6, 1500 with n=7), block sizes
                2..4, each candidate block kept independently with
                probability 1/2, s=2,3,4.  Seed fixed below.

Python standard library only.
"""

from __future__ import annotations

import itertools
import json
import platform
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "out"
SEED = 20261125


def int_mask(points):
    m = 0
    for p in points:
        m |= 1 << p
    return m


def mex(values):
    g = 0
    while g in values:
        g += 1
    return g


def analyse(n, blocks, s):
    """Analyse one (board, s) instance.  ``blocks`` is a tuple of masks."""
    N = 1 << n
    # Blocks with |B| <= s are satisfied by every set, hence never active.
    active = [b for b in blocks if b.bit_count() > s]
    pc = [m.bit_count() for m in range(N)]

    safe = bytearray(N)
    for m in range(N):
        ok = 1
        for b in active:
            if (m & b).bit_count() > s:
                ok = 0
                break
        safe[m] = ok

    # Children of m are strict supersets (numerically larger), so a descending
    # integer scan computes the Grundy values bottom-up.
    G = [-1] * N
    children = [None] * N
    for m in range(N - 1, -1, -1):
        if not safe[m]:
            continue
        vals = set()
        ch = []
        for x in range(n):
            bit = 1 << x
            if not (m & bit):
                c = m | bit
                if safe[c]:
                    vals.add(G[c])
                    ch.append(c)
        children[m] = ch
        G[m] = mex(vals)

    maximal = [m for m in range(N) if safe[m] and not children[m]]
    max_parities = {pc[m] & 1 for m in maximal}
    max_sizes = {pc[m] for m in maximal}
    uniform_b = len(max_parities) == 1
    only01 = all(G[m] in (0, 1) for m in range(N) if safe[m])
    grundy_dist = {}
    for m in range(N):
        if safe[m]:
            grundy_dist[G[m]] = grundy_dist.get(G[m], 0) + 1

    # Superset zeta transforms.
    def superset_sum(f):
        f = list(f)
        for x in range(n):
            bit = 1 << x
            for m in range(N):
                if not (m & bit):
                    f[m] += f[m | bit]
        return f

    f0 = [0] * N
    f1 = [0] * N
    for m in maximal:
        if pc[m] & 1:
            f1[m] = 1
        else:
            f0[m] = 1
    g0 = superset_sum(f0)  # number of even maximal supersets
    g1 = superset_sum(f1)  # number of odd maximal supersets
    c_ok = all(
        (g0[m] == 0 or g1[m] == 0) for m in range(N) if safe[m]
    )

    bad = [1 if (safe[m] and G[m] not in (0, 1)) else 0 for m in range(N)]
    h = superset_sum(bad)  # number of non-{0,1} positions above m
    local_ok = all(
        ((h[m] == 0) == (g0[m] == 0 or g1[m] == 0))
        for m in range(N)
        if safe[m]
    )

    # Misere outcome: terminal position is a WIN for the player to move.
    win = [False] * N
    for m in range(N - 1, -1, -1):
        if not safe[m]:
            continue
        if not children[m]:
            win[m] = True
        else:
            win[m] = any(not win[c] for c in children[m])

    p = next(iter(max_parities)) if uniform_b else None
    formula_viol = []
    misere_viol = []
    if uniform_b:
        for m in range(N):
            if not safe[m]:
                continue
            want = (p - pc[m]) % 2
            if G[m] != want:
                formula_viol.append({"S": m, "g": G[m], "want": want})
            want_w = (want == 0)
            if win[m] != want_w:
                misere_viol.append({"S": m, "misere": win[m], "want": want_w})

    return {
        "n": n,
        "s": s,
        "num_blocks": len(blocks),
        "num_active_blocks": len(active),
        "num_positions": sum(safe),
        "maximal_sizes": sorted(max_sizes),
        "uniform": uniform_b,
        "uniform_nonconstant": bool(uniform_b and len(max_sizes) > 1),
        "max_parity": p,
        "only01": only01,
        "c_ok": c_ok,
        "local_ok": local_ok,
        "grundy_dist": grundy_dist,
        "formula_viol": len(formula_viol),
        "misere_viol": len(misere_viol),
        "_formula_examples": formula_viol[:5],
        "_misere_examples": misere_viol[:5],
        "_grundy": G,
        "_safe": safe,
        "_maximal": maximal,
        "_pc": pc,
    }


class Family:
    def __init__(self, name):
        self.name = name
        self.cases = 0
        self.counts = {
            "uniform": 0,
            "mixed": 0,
            "only01": 0,
            "not_only01": 0,
            "c_ok": 0,
            "c_fail": 0,
            "local_ok": 0,
            "local_fail": 0,
            "uniform_nonconstant": 0,
            "formula_viol": 0,
            "misere_viol": 0,
            "ab_viol": 0,
            "ac_viol": 0,
            "with_active_block": 0,
        }
        self.per_s = {}
        self.violations = []
        self.nonconstant_examples = []

    def add(self, case_id, res):
        self.cases += 1
        c = self.counts
        if res["uniform"]:
            c["uniform"] += 1
        else:
            c["mixed"] += 1
        if res["only01"]:
            c["only01"] += 1
        else:
            c["not_only01"] += 1
        if res["c_ok"]:
            c["c_ok"] += 1
        else:
            c["c_fail"] += 1
        if res["local_ok"]:
            c["local_ok"] += 1
        else:
            c["local_fail"] += 1
        if res["uniform_nonconstant"]:
            c["uniform_nonconstant"] += 1
            if len(self.nonconstant_examples) < 10:
                self.nonconstant_examples.append(
                    {"case": case_id, "maximal_sizes": res["maximal_sizes"]}
                )
        c["formula_viol"] += res["formula_viol"]
        c["misere_viol"] += res["misere_viol"]
        if res["num_active_blocks"] > 0:
            c["with_active_block"] += 1

        bad = []
        if res["only01"] != res["uniform"]:
            c["ab_viol"] += 1
            bad.append("a_vs_b")
        if res["only01"] != res["c_ok"]:
            c["ac_viol"] += 1
            bad.append("a_vs_c")
        if res["formula_viol"]:
            bad.append("grundy_formula")
        if res["misere_viol"]:
            bad.append("misere_formula")
        if not res["local_ok"]:
            bad.append("localized_corollary")
        if bad:
            self.violations.append(
                {
                    "case": case_id,
                    "kinds": bad,
                    "result": {k: v for k, v in res.items() if not k.startswith("_")},
                    "examples": {
                        "formula": res["_formula_examples"],
                        "misere": res["_misere_examples"],
                    },
                }
            )

        ps = self.per_s.setdefault(
            res["s"],
            {"cases": 0, "uniform": 0, "mixed": 0, "only01": 0, "violations": 0},
        )
        ps["cases"] += 1
        ps["uniform"] += int(res["uniform"])
        ps["mixed"] += int(not res["uniform"])
        ps["only01"] += int(res["only01"])
        if bad:
            ps["violations"] += 1


def candidates(n, sizes):
    return [int_mask(c) for k in sizes for c in itertools.combinations(range(n), k)]


def exhaustive_family(name, n, sizes, s_values):
    cand = candidates(n, sizes)
    assert len(cand) == 10, (name, len(cand))
    fam = Family(name)
    fam.n = n
    fam.s_values = s_values
    fam.num_boards = 1 << len(cand)
    for sel in range(1 << len(cand)):
        blocks = tuple(cand[i] for i in range(len(cand)) if (sel >> i) & 1)
        for s in s_values:
            case_id = f"{name}:sel={sel:04d}({sel:010b}):s={s}"
            fam.add(case_id, analyse(n, blocks, s))
    return fam


def random_family(name, sizes, n_values, boards_per_n, s_values, rng):
    fam = Family(name)
    fam.n = list(n_values)
    fam.s_values = s_values
    fam.num_boards = boards_per_n * len(n_values)
    for n in n_values:
        cand = candidates(n, sizes)
        for i in range(boards_per_n):
            blocks = tuple(b for b in cand if rng.random() < 0.5)
            for s in s_values:
                case_id = f"{name}:n={n}:board={i:04d}:s={s}"
                fam.add(case_id, analyse(n, blocks, s))
    return fam


def summary(fam):
    return {
        "name": fam.name,
        "n": fam.n,
        "s_values": fam.s_values,
        "num_boards": fam.num_boards,
        "cases": fam.cases,
        "counts": fam.counts,
        "per_s": {str(k): v for k, v in sorted(fam.per_s.items())},
        "nonconstant_examples": fam.nonconstant_examples,
        "violations": fam.violations[:50],
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("python:", sys.version.replace("\n", " "))
    print("seed:", SEED)

    fam4 = exhaustive_family(
        "exhaustive_n4", 4, (2, 3), (2, 3)
    )
    print(f"{fam4.name}: boards={fam4.num_boards} cases={fam4.cases}")
    fam5 = exhaustive_family(
        "exhaustive_n5", 5, (3,), (2, 3)
    )
    print(f"{fam5.name}: boards={fam5.num_boards} cases={fam5.cases}")
    rng = random.Random(SEED)
    famr = random_family(
        "random_n6n7", (2, 3, 4), (6, 7), 1500, (2, 3, 4), rng
    )
    print(f"{famr.name}: boards={famr.num_boards} cases={famr.cases}")

    families = [fam4, fam5, famr]
    totals = {
        "cases": sum(f.cases for f in families),
        "uniform": sum(f.counts["uniform"] for f in families),
        "mixed": sum(f.counts["mixed"] for f in families),
        "only01": sum(f.counts["only01"] for f in families),
        "not_only01": sum(f.counts["not_only01"] for f in families),
        "c_ok": sum(f.counts["c_ok"] for f in families),
        "c_fail": sum(f.counts["c_fail"] for f in families),
        "local_ok": sum(f.counts["local_ok"] for f in families),
        "local_fail": sum(f.counts["local_fail"] for f in families),
        "uniform_nonconstant": sum(
            f.counts["uniform_nonconstant"] for f in families
        ),
        "formula_viol": sum(f.counts["formula_viol"] for f in families),
        "misere_viol": sum(f.counts["misere_viol"] for f in families),
        "ab_viol": sum(f.counts["ab_viol"] for f in families),
        "ac_viol": sum(f.counts["ac_viol"] for f in families),
        "with_active_block": sum(
            f.counts["with_active_block"] for f in families
        ),
        "violating_cases": sum(len(f.violations) for f in families),
    }

    result = {
        "tool": "independent verifier for K1298 (task 2)",
        "python": sys.version,
        "platform": platform.platform(),
        "seed": SEED,
        "model": "positions = safe sets; moves add one point; normal/misere as documented",
        "families": [summary(f) for f in families],
        "totals": totals,
        "verdict": {
            "a_iff_b": totals["ab_viol"] == 0,
            "a_iff_c": totals["ac_viol"] == 0,
            "grundy_formula_when_uniform": totals["formula_viol"] == 0,
            "misere_formula_when_uniform": totals["misere_viol"] == 0,
            "localized_corollary": totals["local_fail"] == 0,
        },
    }

    out = OUT_DIR / "verification_boards.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print("wrote", out)
    print("totals:", json.dumps(totals, sort_keys=True))

    bad = totals["violating_cases"]
    if bad:
        print(f"FAIL: {bad} violating cases")
        for f in families:
            for v in f.violations[:10]:
                print(" ", v["case"], v["kinds"])
        return 1
    print("PASS: no violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
