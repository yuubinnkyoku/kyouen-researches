"""Task 2 (Python side): complete solve of the s-game for s = 1..5.

For each s this enumerates *every* safe set exactly once (increasing-order DFS,
independent of the original engine), then runs a bottom-up mex DP over the
enumerated positions to obtain the full Grundy and misere distributions.

Structural claims checked here:
  s=1: safe = empty + 24 singletons; maximal = the 24 singletons
  s=2,3,4: no safe set of size s+1 (every (s+1)-set lies in an octad), and the
           maximal safe sets are exactly all s-sets (C(24,s) of them)
  s=5: maximal safe sets are exactly the 6-sets not contained in any octad
       (113344), and every such 6-set is maximal (checked directly)
"""

from __future__ import annotations

import itertools
import json
import math
import sys

from common import (
    B,
    N,
    OUT_DIR,
    enumerate_safe,
    grundy_misere,
    load_board,
    octad_masks,
    thru_lists,
)


def six_sets_not_in_octad(octads):
    """All 6-subsets that lie in no octad, plus a direct maximality check."""
    in_octad = set()
    for o in octads:
        for T in itertools.combinations(o, 6):
            in_octad.add(T)
    out = []
    for T in itertools.combinations(range(N), 6):
        if T in in_octad:
            continue
        out.append(T)
    # maximality of a 6-set S for s=5: for every p outside S there must be an
    # octad B with p in B and |S cap B| = 5 (then adding p gives 6 > 5).
    oct_sets = [frozenset(o) for o in octads]
    maximal = 0
    failures = []
    for T in out:
        Ts = set(T)
        cover = set()
        for o in oct_sets:
            if len(Ts & o) == 5:
                cover |= o
        if set(range(N)) - Ts <= cover:
            maximal += 1
        else:
            failures.append(T)
    return len(in_octad), out, maximal, failures


def solve(s: int, octads, thru, pts, oct_masks, do_dp=True):
    res = enumerate_safe(s, octads, thru, pts)
    by_size = res["by_size"]
    counts = [len(x) for x in by_size]
    maximal = res["maximal"]
    out = {
        "s": s,
        "safe_by_size": {k: v for k, v in enumerate(counts) if v},
        "safe_total": sum(counts),
        "maximal_by_size": {k: v for k, v in enumerate(maximal) if v},
    }
    if do_dp:
        gdist, mdist, root_g, root_m, gtab, mtab = grundy_misere(
            by_size, s, oct_masks)
        out["grundy_by_size"] = {k: dict(v) for k, v in enumerate(gdist) if v}
        out["misere_by_size"] = {k: dict(v) for k, v in enumerate(mdist) if v}
        gtot: dict[int, int] = {}
        for d in gdist:
            for g, c in d.items():
                gtot[g] = gtot.get(g, 0) + c
        mtot: dict[int, int] = {}
        for d in mdist:
            for m, c in d.items():
                mtot[m] = mtot.get(m, 0) + c
        out["grundy_total"] = dict(sorted(gtot.items()))
        out["misere_total"] = dict(sorted(mtot.items()))
        out["root_grundy"] = root_g
        out["root_misere"] = root_m
    return out


def main(argv):
    ss = [int(x) for x in argv[1:]] or [1, 2, 3, 4, 5]
    header, octads = load_board()
    thru, pts = thru_lists(octads)
    oct_masks = octad_masks(octads)
    results = {}
    failures = []

    if 5 in ss:
        n_in, six_out, six_max, six_fail = six_sets_not_in_octad(octads)
        results["s5_structure"] = {
            "six_subsets_in_octad": n_in,
            "six_subsets_not_in_octad": len(six_out),
            "not_in_octad_but_not_maximal": len(six_fail),
            "maximal_direct_check": six_max,
            "expected": math.comb(N, 6) - B * math.comb(8, 6),
        }
        if len(six_out) != math.comb(N, 6) - B * math.comb(8, 6):
            failures.append("s5: 6-set count mismatch")
        if six_fail:
            failures.append("s5: some octad-free 6-set is not maximal")

    for s in ss:
        r = solve(s, octads, thru, pts, oct_masks, do_dp=True)
        results[f"s{s}"] = r
        # structural checks
        if s == 1:
            if r["safe_total"] != 25 or r["maximal_by_size"] != {1: 24}:
                failures.append("s1: counts mismatch")
            if r["root_grundy"] != 1 or r["root_misere"] != 0:
                failures.append("s1: root value mismatch")
        if s in (2, 3, 4):
            if r["safe_by_size"].get(s + 1, 0) != 0:
                failures.append(f"s{s}: unexpected safe sets of size {s+1}")
            exp = math.comb(N, s)
            if r["maximal_by_size"] != {s: exp}:
                failures.append(f"s{s}: maximal counts {r['maximal_by_size']} != {{{s}: {exp}}}")
            if sum(1 for k in r["safe_by_size"] if k > s):
                failures.append(f"s{s}: safe sets above size {s}")
        if s == 5:
            exp = math.comb(N, 6) - B * math.comb(8, 6)
            if r["safe_by_size"].get(6) != exp:
                failures.append(f"s5: safe 6-sets {r['safe_by_size'].get(6)} != {exp}")
            if r["maximal_by_size"] != {6: exp}:
                failures.append(f"s5: maximal counts {r['maximal_by_size']} != {{6: {exp}}}")
            if sum(1 for k in r["safe_by_size"] if k > 6):
                failures.append("s5: safe sets above size 6")
        print(f"s={s}: safe={r['safe_total']} maximal={r['maximal_by_size']} "
              f"G(root)={r.get('root_grundy')} misere(root)={r.get('root_misere')}",
              flush=True)

    results["checks_failed"] = failures
    results["PASS"] = not failures
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    name = "task2_python_" + "_".join(str(s) for s in ss) + ".json"
    (OUT_DIR / name).write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(json.dumps(results, indent=1))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
