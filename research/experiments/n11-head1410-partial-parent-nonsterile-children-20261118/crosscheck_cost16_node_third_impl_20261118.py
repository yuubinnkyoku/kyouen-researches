#!/usr/bin/env python3
"""Driver and verifier for the Node.js third-implementation cross-check of
the cost-16 parent A16/B16 minimum-cover totals.

The companion module node_crosscheck_cost16_ab_20261118.mjs re-implements the
whole computation (row derivation from pinned inputs, det4 candidate
enumeration, D4 canonicalization, weighted perfect-matching memo DP with
Number storage asserted < 2^53, BigInt outer sums) independently of the two
published Python implementations (checkpoint fresh-slice and shared-memo).

This driver
  1. re-runs the fast modes (--anchor11, --graph31) every time,
  2. runs the 31 fresh-memo B slices and 31 fresh-memo A slices as separate
     node processes (one fresh memo per slice), resumably, under a per-run
     time budget,
  3. assembles the final verification JSON once every slice is present,
     comparing every value against the pinned published outputs.

No game-tree search, no verdict.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "output", "cost16-node-third-impl-crosscheck-20261118.json")
SLICES_DIR = os.path.join(HERE, "output", "node-third-impl-slices")

MJS = os.path.join(HERE, "node_crosscheck_cost16_ab_20261118.mjs")
PM_LIMIT = 2 ** 53

PINS = {
    "shared_memo_crosscheck": (
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost16-shared-memo-crosscheck-20261118.json",
        "41d37ed863a85c8a9bdadaf0f39bb6d1a452c60d",
    ),
    "phase_a": (
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost16-a-phase-20261118.json",
        "fe4b4b559fd8c3fdc9bc9b9f40a048fc3217c55b",
    ),
    "membership11": (
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/minimum-cover-root-membership-20261118.json",
        "ab1e655f4a89a677e57515cdbacfe56894323013",
    ),
    "worklist": (
        "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
        "2fee1d0718547a62e346d35f5858d7913e37c097",
    ),
    "census": (
        "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
        "9c251da3138c5cb0516e097be5e5d0427dfaf5f0",
    ),
    "ledger": (
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
        "e8785d509e8a11a37c0d03cc450455a14708c34d",
    ),
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def read_pinned(name: str) -> bytes:
    rel, pin = PINS[name]
    with open(os.path.join(ROOT, rel), "rb") as f:
        data = f.read()
    if git_blob_sha(data) != pin:
        raise SystemExit("pin mismatch for %s: expected %s" % (name, pin))
    return data


def run_node(args, timeout=280):
    t0 = time.time()
    proc = subprocess.run(["node", MJS] + args, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise SystemExit("node %s failed rc=%d: %s" % (args, proc.returncode, proc.stderr[:500]))
    lines = [l for l in proc.stdout.splitlines() if l.strip()]
    if len(lines) != 1:
        raise SystemExit("node %s produced %d lines" % (args, len(lines)))
    doc = json.loads(lines[0])
    doc["_wall_seconds"] = round(time.time() - t0, 3)
    return doc


def run_slices(budget_seconds: float) -> bool:
    """Runs pending slices; returns True when all 62 are present."""
    os.makedirs(SLICES_DIR, exist_ok=True)
    t0 = time.time()
    todo = [("b", d) for d in range(31)] + [("a", s) for s in range(31)]
    for kind, idx in todo:
        path = os.path.join(SLICES_DIR, "%s%d.json" % (kind, idx))
        if os.path.exists(path):
            continue
        if time.time() - t0 > budget_seconds:
            print("time budget reached; slices pending:", flush=True)
            return False
        doc = run_node(["--%sslice" % kind, str(idx)])
        with open(path, "w") as f:
            json.dump(doc, f, separators=(",", ":"))
        print("slice %s%d done in %.1fs" % (kind, idx, doc["_wall_seconds"]), flush=True)
    return True


def assemble() -> int:
    checks = []

    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str) else json.dumps(detail)})

    node_version = subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip()
    check("node.version", bool(node_version), node_version)

    pub = json.loads(read_pinned("shared_memo_crosscheck"))
    pub_d = pub["derived"]
    phase_a = json.loads(read_pinned("phase_a"))["derived"]
    mem11 = json.loads(read_pinned("membership11"))["derived"]

    anchor = run_node(["--anchor11"])
    graph31 = run_node(["--graph31"])

    # ---- anchor11 ----
    cs = anchor["cover_space"]
    check("anchor11.A", cs["singleton_type_covers"] == str(mem11["cover_space"]["singleton_type_covers"]),
          {"mine": cs["singleton_type_covers"], "pub": mem11["cover_space"]["singleton_type_covers"]})
    check("anchor11.B", cs["six_pair_covers"] == str(mem11["cover_space"]["six_pair_covers"]),
          {"mine": cs["six_pair_covers"], "pub": mem11["cover_space"]["six_pair_covers"]})
    check("anchor11.total", cs["total_minimum_covers"] == str(mem11["cover_space"]["total_minimum_covers"]),
          {"mine": cs["total_minimum_covers"], "pub": mem11["cover_space"]["total_minimum_covers"]})
    pub_rows = {x["row"]: x for x in mem11["per_row"]}
    row_mism = [x["row"] for x in anchor["per_row"]
                if pub_rows[x["row"]]["singleton_roots"] != x["singleton_roots"]
                or pub_rows[x["row"]]["ways10"] != x["ways10"]]
    check("anchor11.per_row", len(row_mism) == 0 and len(anchor["per_row"]) == 11, row_mism)
    pub_mem = {x["root"]: x for x in mem11["all_root_memberships"]}
    mem_mism = []
    for x in anchor["all_root_memberships"]:
        p = pub_mem.get(x["root"])
        if p is None or str(p["membership"]) != x["membership"] \
                or str(p["singleton_type_covers"]) != x["singleton_type_covers"] \
                or str(p["six_pair_type_covers"]) != x["six_pair_type_covers"] \
                or sorted(p["cover_rows"]) != x["cover_rows"]:
            mem_mism.append(x["root"])
    check("anchor11.root_memberships",
          len(mem_mism) == 0 and len(anchor["all_root_memberships"]) == len(pub_mem) == 757,
          {"mismatches": mem_mism[:10], "mine": len(anchor["all_root_memberships"]), "pub": len(pub_mem)})
    total_membership = sum(int(x["membership"]) for x in anchor["all_root_memberships"])
    check("anchor11.identity_6x", total_membership == int(cs["total_minimum_covers"]) * 6, total_membership)

    # ---- graph31 structure ----
    g = graph31["graph"]
    pub_rows31 = {x["row"]: x["edge_cost"] for x in pub_d["target_rows"]}
    check("graph31.rows", {x["hex"]: x["cost"] for x in g["rows"]} == pub_rows31 and len(g["rows"]) == 31)
    check("graph31.candidate_occurrences", g["candidate_occurrences"] == pub_d["candidate_occurrences"],
          g["candidate_occurrences"])
    check("graph31.distinct_roots", g["distinct_D4_roots"] == pub_d["distinct_D4_roots"], g["distinct_D4_roots"])
    check("graph31.span_histogram", g["root_coverage_histogram"] == pub_d["root_coverage_histogram"],
          g["root_coverage_histogram"])
    check("graph31.pair_types", g["pair_types"] == pub_d["pair_types"], g["pair_types"])
    check("graph31.pair_multiplicity", g["pair_type_multiplicity_histogram"] == pub_d["pair_type_multiplicity_histogram"],
          g["pair_type_multiplicity_histogram"])
    check("graph31.singleton_roots", g["singleton_root_count"] == pub_d["singleton_root_count"], g["singleton_root_count"])
    check("graph31.per_row_singleton",
          g["per_row_singleton_root_count"] == [phase_a["per_row_singleton_root_count"][str(i)] for i in range(31)])
    check("graph31.per_row_degree",
          g["per_row_pair_root_degree"] == [phase_a["per_row_pair_root_degree"][str(i)] for i in range(31)])

    # ---- slices ----
    missing = [k + str(i) for k, rng in (("b", range(31)), ("a", range(31))) for i in rng
               if not os.path.exists(os.path.join(SLICES_DIR, "%s%d.json" % (k, i)))]
    check("slices.complete", len(missing) == 0, missing)
    if missing:
        print(json.dumps({"all_pass": False, "missing_slices": missing}, indent=1))
        return 1

    b_rows = []
    a_rows = []
    B16 = 0
    for d in range(31):
        doc = json.load(open(os.path.join(SLICES_DIR, "b%d.json" % d)))
        pb = pub_d["B_by_doubled_row"][d]
        ok = doc["mode"] == "bslice" and doc["double_row_index"] == d \
            and doc["B_d"] == str(pb["B_d"]) \
            and doc["degree"] == int(pb["degree"]) and doc["anchors"] == int(pb["anchors"])
        check("bslice.%d" % d, ok,
              {"mine": doc["B_d"], "pub": str(pb["B_d"]), "degree": doc["degree"], "anchors": doc["anchors"]})
        B16 += int(doc["B_d"])
        b_rows.append({k: doc[k] for k in ("double_row_index", "row_hex", "degree", "anchors", "B_d",
                                            "fresh_memo_states")})
    A16 = 0
    for s in range(31):
        doc = json.load(open(os.path.join(SLICES_DIR, "a%d.json" % s)))
        pa = pub_d["A16_per_row_pm"][str(s)]
        ok = doc["mode"] == "aslice" and doc["row_index"] == s \
            and doc["pm_value"] == pa and doc["pm_value"] < PM_LIMIT \
            and doc["singleton_root_count"] == phase_a["per_row_singleton_root_count"][str(s)]
        check("aslice.%d" % s, ok, {"mine": doc["pm_value"], "pub": pa})
        A16 += doc["singleton_root_count"] * doc["pm_value"]
        a_rows.append({k: doc[k] for k in ("row_index", "row_hex", "singleton_root_count",
                                            "pm_value", "fresh_memo_states")})

    check("A16", A16 == pub_d["A16"], {"mine": A16, "pub": pub_d["A16"]})
    check("B16", B16 == pub_d["B16"], {"mine": B16, "pub": pub_d["B16"]})
    check("total", A16 + B16 == pub_d["total_minimum_covers"],
          {"mine": A16 + B16, "pub": pub_d["total_minimum_covers"]})

    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-cost16-node-third-impl-crosscheck-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Third-implementation (Node.js) cross-check of the cost-16 parent "
                  "A16/B16 minimum-cover totals: 31 fresh-memo B slices, 31 fresh-memo "
                  "A slices, full 11-row anchor with all 757 root memberships"),
        "inputs": {name: {"path": rel, "git_blob_sha1": pin} for name, (rel, pin) in PINS.items()},
        "method": ("node_crosscheck_cost16_ab_20261118.mjs re-derives the 31 target rows "
                   "from the pinned worklist/census/ledger, regenerates candidate roots "
                   "with integer det4 + D4 BigInt canonicalization, and computes weighted "
                   "perfect-matching counts with a lazily evaluated memo DP stored as JS "
                   "Numbers (every stored pm value is asserted < 2^53 so all Number "
                   "arithmetic in the DP is exact); outer products and sums (B_d, A16, "
                   "B16) accumulate in BigInt. Each B slice and each A slice runs in its "
                   "own node process with a fresh memo (independent of both the published "
                   "checkpoint fresh-slice design and the shared-memo design). The 11-row "
                   "anchor recomputes A/B/total, per-row singleton counts and ways10, and "
                   "per-root membership for every root, matching the published membership "
                   "output field by field."),
        "derived": {
            "node_version": node_version,
            "anchor11": {
                "cover_space": anchor["cover_space"],
                "per_row": anchor["per_row"],
                "root_membership_count": len(anchor["all_root_memberships"]),
                "root_membership_mismatches": len(mem_mism),
                "identity_sum_equals_6x_total": total_membership == int(cs["total_minimum_covers"]) * 6,
                "memo_states": anchor["memo_states"],
            },
            "graph31": {k: g[k] for k in ("row_count", "candidate_occurrences", "distinct_D4_roots",
                                          "root_coverage_histogram", "pair_types",
                                          "pair_type_multiplicity_histogram", "singleton_root_count",
                                          "per_row_singleton_root_count", "per_row_pair_root_degree")},
            "B_by_doubled_row_fresh_memo": b_rows,
            "A_per_row_pm_fresh_memo": a_rows,
            "A16": A16,
            "B16": B16,
            "total_minimum_covers": A16 + B16,
            "max_pm_value": max(r["pm_value"] for r in a_rows),
            "pm_limit": PM_LIMIT,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Finite combinatorial verification only. A16/B16 count "
                                 "minimum certificate-covers of the 31 target rows under the "
                                 "planning cover semantics (a root covers a row iff the row "
                                 "generates the root as a 1-stone D4-canonical extension); "
                                 "they are bookkeeping counts, not WIN/REFUTED claims, and "
                                 "no root has been validated as a certificate. REFUTED-D10 "
                                 "and STERILE are not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(OUT, "w") as f:
        f.write(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"all_pass": all_pass, "checks": len(checks),
                      "failed": [c["name"] for c in checks if not c["pass"]][:10],
                      "A16": A16, "B16": B16, "total": A16 + B16}, indent=1))
    return 0 if all_pass else 1


def main():
    budget = 240.0
    args = sys.argv[1:]
    if "--budget" in args:
        budget = float(args[args.index("--budget") + 1])
    mode = args[0] if args and not args[0].startswith("--") else "run"
    if mode == "assemble":
        sys.exit(assemble())
    complete = run_slices(budget)
    if not complete:
        sys.exit(3)
    sys.exit(assemble())


if __name__ == "__main__":
    main()
