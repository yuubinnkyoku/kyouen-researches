#!/usr/bin/env python3
"""Compare every field of the claimed output file against the independent
computations in this directory, and emit a machine-readable summary.

Claimed file (C engine output):
  research/experiments/s-parameter-kyouen-20261125/output/grundy_pg2q5_s3.txt
Fields: POINTS, CIRCLES, SAFE, ROOT g mv,
        SIZE s safe maximal grundy0, GRUNDY g count,
        FIRSTMOVE g count, PROBE g1 g2 g3, PROBE_CHILDREN g count.
"""
import json
import os
import struct
import sys
from array import array

HERE = os.path.dirname(os.path.abspath(__file__))
CLAIM = os.path.normpath(os.path.join(
    HERE, "..", "output", "grundy_pg2q5_s3.txt"))
BOARD = os.path.normpath(os.path.join(
    HERE, "..", "..", "projective-blocking-kyouen-20261125", "output", "board_pg2q5.txt"))
OUT = os.path.join(HERE, "out_claims_comparison.json")


def parse_claim(path):
    d = {"SIZE": {}, "GRUNDY": {}, "FIRSTMOVE": {}, "PROBE_CHILDREN": {}}
    with open(path) as f:
        for line in f:
            t = line.split()
            if not t:
                continue
            if t[0] in ("POINTS", "CIRCLES", "SAFE"):
                d[t[0]] = int(t[1])
            elif t[0] == "ROOT":
                d["ROOT"] = (int(t[1]), int(t[2]))
            elif t[0] == "SIZE":
                d["SIZE"][int(t[1])] = tuple(int(x) for x in t[2:5])
            elif t[0] == "GRUNDY":
                d["GRUNDY"][int(t[1])] = int(t[2])
            elif t[0] == "FIRSTMOVE":
                d["FIRSTMOVE"][int(t[1])] = int(t[2])
            elif t[0] == "PROBE":
                d["PROBE"] = tuple(int(x) for x in t[1:4])
            elif t[0] == "PROBE_CHILDREN":
                d["PROBE_CHILDREN"][int(t[1])] = int(t[2])
            else:
                d.setdefault("UNKNOWN", []).append(line.rstrip())
    return d


def parse_enum(path):
    d = {"SIZE": {}}
    with open(path) as f:
        for line in f:
            t = line.split()
            if not t:
                continue
            if t[0] == "SAFE":
                d["SAFE"] = int(t[1])
            elif t[0] == "MAXSIZE":
                d["MAXSIZE"] = int(t[1])
            elif t[0] == "SIZE":
                d["SIZE"][int(t[1])] = (int(t[2]), int(t[3]))
    return d


def parse_brute(path):
    d = {"SIZE": {}}
    with open(path) as f:
        for line in f:
            t = line.split()
            if not t:
                continue
            if t[0] == "SIZE":
                d["SIZE"][int(t[1])] = (int(t[2]), int(t[3]))
            elif t[0] == "SAFE":
                d["SAFE"] = int(t[1])
                d["MAXIMAL"] = int(t[3])
    return d


def parse_level(path):
    d = {"SIZE": {}, "GRUNDY": {}, "SIZE_GRUNDY": {}, "SIZE_MISERE": {}}
    with open(path) as f:
        for line in f:
            t = line.split()
            if not t:
                continue
            if t[0] == "SAFE":
                d["SAFE"] = int(t[1])
            elif t[0] == "MAXSIZE":
                d["MAXSIZE"] = int(t[1])
            elif t[0] == "SIZE":
                d["SIZE"][int(t[1])] = (int(t[2]), int(t[3]))
            elif t[0] == "GRUNDY":
                d["GRUNDY"][int(t[1])] = int(t[2])
            elif t[0] == "MISERE":
                d.setdefault("MISERE", {})[int(t[1])] = int(t[2])
            elif t[0] == "ROOT":
                d["ROOT"] = (int(t[1]), int(t[2]))
            elif t[0] == "SIZE_GRUNDY":
                d["SIZE_GRUNDY"][int(t[1])] = [int(x) for x in t[2:]]
            elif t[0] == "SIZE_MISERE":
                d["SIZE_MISERE"][int(t[1])] = (int(t[2]), int(t[3]))
            elif t[0] == "K1298_UNIFORM_CHECKED":
                d["K1298_UNIFORM_VIOL"] = int(t[3])
            elif t[0] == "K1298_DESC_CHECKED":
                d["K1298_DESC_VIOL"] = int(t[3])
            elif t[0] == "K1298_MISERE_CHECKED":
                d["K1298_MISERE_VIOL"] = int(t[3])
    return d


def read_dumps():
    with open(os.path.join(HERE, "safesets.bin"), "rb") as f:
        assert f.read(8)[:7] == b"PG2Q5S3"
        n, nb, maxsize = struct.unpack("<III", f.read(12))
        cnt = struct.unpack("<%dQ" % (maxsize + 1), f.read(8 * (maxsize + 1)))
        mx = struct.unpack("<%dQ" % (maxsize + 1), f.read(8 * (maxsize + 1)))
        masks, adds = [], []
        for s in range(maxsize + 1):
            a = array("I"); a.fromfile(f, cnt[s]); masks.append(a)
            a = array("I"); a.fromfile(f, cnt[s]); adds.append(a)
        assert f.read() == b""
    with open(os.path.join(HERE, "grundy_values.bin"), "rb") as f:
        assert f.read(8)[:7] == b"PG2G5V1"
        vn, vnb, vmax = struct.unpack("<III", f.read(12))
        vcnt = struct.unpack("<%dQ" % (vmax + 1), f.read(8 * (vmax + 1)))
        vals = []
        for s in range(vmax + 1):
            a = array("B"); a.fromfile(f, vcnt[s]); vals.append(a)
        assert f.read() == b""
    assert (n, nb, maxsize) == (vn, vnb, vmax) and cnt == vcnt
    return n, nb, maxsize, cnt, mx, masks, adds, vals


def main():
    claim = parse_claim(CLAIM)
    enum = parse_enum(os.path.join(HERE, "enum_out.txt"))
    brute = parse_brute(os.path.join(HERE, "brute_out.txt"))
    level = parse_level(os.path.join(HERE, "grundy_level_out.txt"))
    n, nb, maxsize, cnt, mx, masks, adds, vals = read_dumps()

    checks = []

    def chk(name, claim_v, computed_v, note=""):
        ok = claim_v == computed_v
        checks.append({"check": name, "claim": claim_v,
                       "computed": computed_v, "pass": ok, "note": note})
        return ok

    chk("POINTS", claim["POINTS"], n, "board file header")
    chk("CIRCLES", claim["CIRCLES"], nb, "board file header")
    chk("SAFE", claim["SAFE"], enum["SAFE"], "DFS enumeration")
    chk("SAFE_brute", claim["SAFE"], brute["SAFE"], "exhaustive subsets up to size 12")
    chk("SAFE_level", claim["SAFE"], level["SAFE"], "level DP")

    max_sizes = sorted(s for s, (c, m) in enum["SIZE"].items() if m > 0)
    claim_max_sizes = sorted(s for s, (c, m, g0) in claim["SIZE"].items() if m > 0)
    chk("maximal_sizes", claim_max_sizes, max_sizes,
        "sizes with any maximal set")
    for s in sorted(claim["SIZE"]):
        c, m, g0 = claim["SIZE"][s]
        ec, em = enum["SIZE"].get(s, (0, 0))
        chk("SIZE_%d_count" % s, c, ec)
        chk("SIZE_%d_maximal" % s, m, em)
        chk("SIZE_%d_grundy0" % s, g0, level["SIZE_GRUNDY"].get(s, [0])[0])
        chk("SIZE_%d_count_brute" % s, c, brute["SIZE"].get(s, (0, 0))[0])
        chk("SIZE_%d_maximal_brute" % s, m, brute["SIZE"].get(s, (0, 0))[1])

    for g in sorted(claim["GRUNDY"]):
        chk("GRUNDY_%d" % g, claim["GRUNDY"][g], level["GRUNDY"].get(g, 0))

    chk("ROOT_grundy", claim["ROOT"][0], level["ROOT"][0], "G(empty)")
    chk("ROOT_misere", claim["ROOT"][1], level["ROOT"][1], "misere(empty)")

    # FIRSTMOVE g -> number of moves from empty whose child has Grundy g
    first = {}
    av = adds[0][0]
    while av:
        p = (av & -av).bit_length() - 1
        av &= av - 1
        g = vals[1][list(masks[1]).index(masks[0][0] | (1 << p))] & 15
        first[g] = first.get(g, 0) + 1
    chk("FIRSTMOVE", claim["FIRSTMOVE"], first,
        "histogram of child Grundy over the 31 first moves")

    # PROBE: Grundy of masks 1, 3, 7
    probe = []
    for s, want in ((1, 1), (2, 3), (3, 7)):
        idx = list(masks[s]).index(want)
        probe.append(vals[s][idx] & 15)
    chk("PROBE", claim["PROBE"], tuple(probe), "G({0}), G({0,1}), G({0,1,2})")

    # PROBE_CHILDREN: children of mask 7 by Grundy
    s = 3
    idx = list(masks[s]).index(7)
    kids = {}
    av = adds[s][idx]
    while av:
        p = (av & -av).bit_length() - 1
        av &= av - 1
        child = 7 | (1 << p)
        ci = list(masks[s + 1]).index(child)
        g = vals[s + 1][ci] & 15
        kids[g] = kids.get(g, 0) + 1
    chk("PROBE_CHILDREN", claim["PROBE_CHILDREN"], kids,
        "children of {0,1,2} grouped by Grundy")

    # K1298 structural checks (from the exhaustive level DP)
    k_viol = level.get("K1298_UNIFORM_VIOL", None)
    d_viol = level.get("K1298_DESC_VIOL", None)
    m_viol = level.get("K1298_MISERE_VIOL", None)
    checks.append({"check": "K1298_formula_violations", "claim": 0,
                   "computed": k_viol, "pass": k_viol == 0})
    checks.append({"check": "K1298_desc2_equiv_violations", "claim": 0,
                   "computed": d_viol, "pass": d_viol == 0})
    checks.append({"check": "K1298_misere_formula_violations", "claim": 0,
                   "computed": m_viol, "pass": m_viol == 0})

    # extra: claimed size distribution sums to SAFE
    checks.append({
        "check": "size_distribution_sums_to_SAFE",
        "claim": claim["SAFE"],
        "computed": sum(c for c, m, g0 in claim["SIZE"].values()),
        "pass": sum(c for c, m, g0 in claim["SIZE"].values()) == claim["SAFE"]})
    checks.append({
        "check": "grundy_distribution_sums_to_SAFE",
        "claim": claim["SAFE"],
        "computed": sum(claim["GRUNDY"].values()),
        "pass": sum(claim["GRUNDY"].values()) == claim["SAFE"]})

    failed = [c for c in checks if not c["pass"]]
    res = {
        "claim_file": CLAIM,
        "n_checks": len(checks),
        "failed": len(failed),
        "ok": not failed,
        "unknown_claim_lines": claim.get("UNKNOWN", []),
        "checks": checks,
    }
    with open(OUT, "w") as f:
        json.dump(res, f, indent=2)
    print("checks: %d, failed: %d" % (len(checks), len(failed)))
    for c in failed:
        print("FAIL", c["check"], "claim=", c["claim"], "computed=", c["computed"])
    if claim.get("UNKNOWN"):
        print("unknown claim lines:", claim["UNKNOWN"])
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["ok"] else 1)


if __name__ == "__main__":
    main()
