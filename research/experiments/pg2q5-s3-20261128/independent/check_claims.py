#!/usr/bin/env python3
"""Compare the claimed K1359 table against all reproductions and check the
internal arithmetic and the structural claims.

Inputs (all under this experiment):
  ../output/gsize_pg2q5_s3.txt     claimed table
  published_run.txt                published engine, recompiled here
  indep_run.txt                    independent C implementation
  out/python_full_dp.txt           independent complete Python DP (optional)
  out/board_check.json             board structural check

Writes out/checks.json and prints a PASS/FAIL summary.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLAIMED = os.path.abspath(os.path.join(HERE, "..", "output",
                                       "gsize_pg2q5_s3.txt"))

# The claim as stated in K1359 / the task text, hard-coded independently of
# the claimed output file.
CLAIM_GSIZE = {
    (0, 1): 1,
    (1, 0): 31,
    (2, 1): 465,
    (3, 0): 4495,
    (4, 2): 31000,
    (5, 0): 111600, (5, 1): 46500,
    (6, 0): 15500, (6, 1): 3100, (6, 2): 186000, (6, 3): 387500,
    (7, 0): 480500, (7, 1): 697500, (7, 2): 186000, (7, 4): 186000,
    (8, 0): 465000, (8, 1): 232500, (8, 2): 186000, (8, 3): 1674000,
    (9, 0): 666500, (9, 1): 620000, (9, 2): 930000,
    (10, 0): 248000, (10, 1): 483600,
    (11, 0): 65100,
}
CLAIM_GRUNDY = {0: 2056726, 1: 2083666, 2: 1519000, 3: 2061500,
                4: 186000}
CLAIM_MAXIMAL = {9: 93000, 10: 248000, 11: 65100}
CLAIM_SAFE = 7906892
CLAIM_SIZE_TOTALS = {0: 1, 1: 31, 2: 465, 3: 4495, 4: 31000, 5: 158100,
                     6: 592100, 7: 1550000, 8: 2557500, 9: 2216500,
                     10: 731600, 11: 65100}


def parse_run(path):
    out = {"SIZE": {}, "GRUNDY": {}, "GSIZE": {}, "other": {}}
    with open(path, encoding="utf-8") as f:
        for line in f:
            t = line.split()
            if not t:
                continue
            tag = t[0]
            try:
                if tag == "SIZE":
                    out["SIZE"][int(t[1])] = (int(t[2]), int(t[3]), int(t[4]))
                elif tag == "GRUNDY":
                    out["GRUNDY"][int(t[1])] = int(t[2])
                elif tag == "GSIZE":
                    out["GSIZE"][(int(t[1]), int(t[2]))] = int(t[3])
                elif tag == "ROOT":
                    out["other"]["ROOT"] = (int(t[1]), int(t[2]))
                elif tag in ("POINTS", "CIRCLES", "SAFE"):
                    out["other"][tag] = int(t[1])
                else:
                    out["other"].setdefault(tag, []).append(t[1:])
            except (IndexError, ValueError):
                raise ValueError(f"bad line in {path}: {line!r}")
    return out


def cmp_table(a, b, label, diffs):
    for tag in ("SIZE", "GRUNDY", "GSIZE"):
        keys = sorted(set(a[tag]) | set(b[tag]))
        for k in keys:
            if a[tag].get(k) != b[tag].get(k):
                diffs.append(f"{label}: {tag} {k}: claimed {a[tag].get(k)} "
                             f"vs reproduced {b[tag].get(k)}")
    for tag in ("POINTS", "CIRCLES", "SAFE", "ROOT"):
        if a["other"].get(tag) != b["other"].get(tag):
            diffs.append(f"{label}: {tag}: claimed {a['other'].get(tag)} "
                         f"vs reproduced {b['other'].get(tag)}")


def main():
    checks = []

    def add(cid, desc, ok, detail=""):
        checks.append({"id": cid, "description": desc, "pass": bool(ok),
                       "detail": detail})

    claimed = parse_run(CLAIMED)
    published = parse_run(os.path.join(HERE, "published_run.txt"))
    indep = parse_run(os.path.join(HERE, "indep_run.txt"))

    # ---- task 1: board ----
    with open(os.path.join(HERE, "out", "board_check.json"),
              encoding="utf-8") as f:
        board = json.load(f)
    add("T1-board", "board is 31 points / 31 lines of 6, every pair exactly "
        "once (PG(2,5))", board["is_projective_plane_order_5"],
        f"pairs={board['distinct_pairs_covered']}/"
        f"{board['total_pairs_expected']}, line intersections="
        f"{board['line_intersection_histogram']}")

    # ---- task 2: reproduction ----
    d_pub = []
    cmp_table(claimed, published, "published-vs-claimed", d_pub)
    add("T2-published", "recompiled published engine reproduces every "
        "SIZE/GRUNDY/GSIZE line of the claimed file", not d_pub,
        "; ".join(d_pub[:10]) if d_pub else "all lines identical")

    d_ind = []
    cmp_table(claimed, indep, "independentC-vs-claimed", d_ind)
    add("T2-independentC", "independent C implementation (separate parser, "
        "per-point rule, sorted binary-search DP) reproduces every line",
        not d_ind, "; ".join(d_ind[:10]) if d_ind else "all lines identical")

    pydp_path = os.path.join(HERE, "out", "python_full_dp.txt")
    if os.path.exists(pydp_path):
        pydp = parse_run(pydp_path)
        d_py = []
        cmp_table(claimed, pydp, "pythonFullDP-vs-claimed", d_py)
        add("T2-pythonFullDP", "complete pure-Python DP over all reachable "
            "safe positions reproduces every line", not d_py,
            "; ".join(d_py[:10]) if d_py else "all lines identical")
    else:
        add("T2-pythonFullDP", "complete pure-Python DP output present",
            False, "out/python_full_dp.txt missing")

    # ---- task 5: arithmetic inside the claimed table ----
    bad_sum = []
    for k, (cnt, mx, g0) in sorted(claimed["SIZE"].items()):
        s = sum(v for (kk, gg), v in claimed["GSIZE"].items() if kk == k)
        if s != cnt:
            bad_sum.append(f"size {k}: GSIZE sum {s} != SIZE count {cnt}")
        if g0 != claimed["GSIZE"].get((k, 0), 0):
            bad_sum.append(f"size {k}: SIZE g0 {g0} != GSIZE g0 "
                           f"{claimed['GSIZE'].get((k,0),0)}")
    add("T5-size-sums", "every SIZE count equals the sum of its GSIZE "
        "counts and equals its G0 count", not bad_sum, "; ".join(bad_sum[:10]))

    bad_g = []
    for g, cnt in sorted(claimed["GRUNDY"].items()):
        s = sum(v for (kk, gg), v in claimed["GSIZE"].items() if gg == g)
        if s != cnt:
            bad_g.append(f"G{g}: GSIZE sum {s} != GRUNDY count {cnt}")
    add("T5-grundy-totals", "every GRUNDY total equals the sum over sizes "
        "of the GSIZE cells", not bad_g, "; ".join(bad_g[:10]))

    total_size = sum(v[0] for v in claimed["SIZE"].values())
    total_g = sum(claimed["GRUNDY"].values())
    add("T5-safe-total", "sum of SIZE counts = sum of GRUNDY counts = SAFE "
        "= 7,906,892",
        total_size == total_g == claimed["other"].get("SAFE") == CLAIM_SAFE,
        f"SIZE sum {total_size}, GRUNDY sum {total_g}, "
        f"SAFE {claimed['other'].get('SAFE')}")

    # ---- compare hard-coded claim with the claimed file ----
    add("T5-claim-file-gsize", "claimed file GSIZE table equals the K1359 "
        "table in the task text", claimed["GSIZE"] == CLAIM_GSIZE,
        f"{len(claimed['GSIZE'])} cells vs {len(CLAIM_GSIZE)} claimed")
    add("T5-claim-file-grundy", "claimed file GRUNDY totals equal the task "
        "text", claimed["GRUNDY"] == CLAIM_GRUNDY)
    add("T5-claim-file-sizes", "claimed file SIZE counts equal the task "
        "text", {k: v[0] for k, v in claimed["SIZE"].items()} ==
        CLAIM_SIZE_TOTALS)

    # ---- compare independent results with hard-coded claim ----
    add("T2-indep-eq-claim", "independent C GSIZE table equals the K1359 "
        "table", indep["GSIZE"] == CLAIM_GSIZE)
    add("T2-indep-grundy-eq-claim", "independent C GRUNDY totals equal the "
        "K1359 table", indep["GRUNDY"] == CLAIM_GRUNDY)

    # ---- task 3: maximal positions / maximum size ----
    max_keys = sorted(k for k, v in claimed["SIZE"].items() if v[0] > 0)
    maximal = {k: v[1] for k, v in claimed["SIZE"].items() if v[1]}
    add("T3-max-size", "maximum safe size is 11 (no size-12 positions)",
        max_keys == list(range(12)), f"sizes present: {max_keys}")
    add("T3-maximal-counts", "maximal-position counts are exactly 9:93,000, "
        "10:248,000, 11:65,100", maximal == CLAIM_MAXIMAL,
        f"maximal counts: {maximal}")
    add("T3-maximal-indep", "independent C reproduces the maximal counts",
        {k: v[1] for k, v in indep["SIZE"].items() if v[1]} == CLAIM_MAXIMAL)
    add("T3-g0-vs-maximal", "maximal positions are a subset of G0 and at "
        "sizes 10,11 all G0 positions are maximal",
        all(v[1] <= claimed["GSIZE"].get((k, 0), 0)
            for k, v in claimed["SIZE"].items()) and
        claimed["SIZE"][10][1] == claimed["GSIZE"][(10, 0)] and
        claimed["SIZE"][11][1] == claimed["GSIZE"][(11, 0)])

    # ---- task 4: structural claims ----
    g4_sizes = sorted(k for (k, g) in claimed["GSIZE"] if g == 4)
    add("T4-G4-only-size7", "Grundy 4 occurs only at size 7",
        g4_sizes == [7],
        f"sizes with G4: {g4_sizes}; G4 count "
        f"{claimed['GSIZE'].get((7, 4))}")
    four = {g: v for (k, g), v in claimed["GSIZE"].items() if k == 4}
    add("T4-all-4caps-G2", "all 31,000 safe 4-sets have Grundy 2 "
        "(complete enumeration, not a sample)",
        four == {2: 31000}, f"size-4 distribution: {four}")
    add("T4-G4-is-max", "maximum Grundy value is 4 and no value >4 occurs",
        max(claimed["GRUNDY"]) == 4,
        f"Grundy values: {sorted(claimed['GRUNDY'])}")

    # combinatorial cross-check of the size-4 and size-5 counts
    import math
    k4_formula = math.comb(31, 4) - 31 * math.comb(6, 4)
    k5_formula = (math.comb(31, 5) -
                  31 * (math.comb(6, 4) * (31 - 6) + math.comb(6, 5)))
    add("T5-comb-k4", "size-4 count matches C(31,4) - 31*C(6,4) = 31,000",
        k4_formula == claimed["SIZE"][4][0] == 31000, f"{k4_formula}")
    add("T5-comb-k5", "size-5 count matches C(31,5) - 31*(C(6,4)*25 + "
        "C(6,5)) = 158,100", k5_formula == claimed["SIZE"][5][0] == 158100,
        f"{k5_formula}")

    # ---- claimed JSON companion file ----
    json_path = os.path.abspath(os.path.join(HERE, "..", "output",
                                             "pg2q5_s3_gsize.json"))
    if os.path.exists(json_path):
        with open(json_path, encoding="utf-8") as f:
            jdata = json.load(f)
        jbad = []
        if jdata.get("safe") != CLAIM_SAFE:
            jbad.append(f"safe {jdata.get('safe')}")
        for ks, rec in jdata["sizes"].items():
            k = int(ks)
            if (rec["N"], rec["maximal"]) != claimed["SIZE"][k][:2]:
                jbad.append(f"size {k} N/maximal {rec['N']}/{rec['maximal']} "
                            f"vs {claimed['SIZE'][k][:2]}")
            ng = {int(g): v for g, v in rec["N_g"].items()}
            got = {g: v for (kk, g), v in claimed["GSIZE"].items()
                   if kk == k}
            if ng != got:
                jbad.append(f"size {k} N_g {ng} vs {got}")
        add("T5-claim-json", "claimed JSON companion matches the claimed "
            "text table", not jbad, "; ".join(jbad[:5]))
    else:
        add("T5-claim-json", "claimed JSON companion present", False,
            "pg2q5_s3_gsize.json missing")

    # ---- root ----
    add("T5-root", "root (empty position) has Grundy 1", claimed["other"]
        .get("ROOT") == (1, 1), f"{claimed['other'].get('ROOT')}")

    # ---- board size vs game parameters ----
    add("T5-params", "31 points, 31 lines, line size 6, cap s=3",
        claimed["other"].get("POINTS") == 31 and
        claimed["other"].get("CIRCLES") == 31 and
        board["line_length_histogram"] == {"6": 31},
        f"POINTS {claimed['other'].get('POINTS')}, "
        f"CIRCLES {claimed['other'].get('CIRCLES')}")

    n_pass = sum(c["pass"] for c in checks)
    result = {"checks": checks, "passed": n_pass, "total": len(checks),
              "all_pass": n_pass == len(checks)}
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "checks.json"), "w",
              encoding="utf-8") as f:
        json.dump(result, f, indent=1)

    for c in checks:
        print(f"[{'PASS' if c['pass'] else 'FAIL'}] {c['id']}: "
              f"{c['description']}")
        if not c["pass"]:
            print(f"        {c['detail']}")
    print(f"\n{n_pass}/{len(checks)} checks passed")
    return 0 if result["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
