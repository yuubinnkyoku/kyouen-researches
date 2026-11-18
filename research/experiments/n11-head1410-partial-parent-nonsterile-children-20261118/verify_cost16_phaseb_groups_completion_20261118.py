#!/usr/bin/env python3
"""Completion verification for the 31-row cost-16 parent phase-B groups run.

Verifies, from the published/pinned artifacts and the final groups JSONL, that
  (a) all 425 pair-type memberships (a_part/b_part) are present and unique,
  (b) the two global identities hold:
        sum(a_part) == 15 * A16   (A16 from the pinned phase-A output)
        sum(b_part) == 16 * B16   (B16 from the published per-d-slice output,
                                    i.e. the cross-lane aggregate check)
      together with sum(all memberships) == 16 * (A16 + B16),
  (c) the 13 authoritative values in the design log reproduce, with the one
      documented discrepancy ((4,29) b_part, a 2e13 transcription error in the
      design-log table) resolved in favor of the recomputed value (three
      computation epochs agree on it),
  (d) the duplicate (0,8) record removed from the publication JSONL was
      value-identical to the kept copy (deterministic recompute across epochs),
  (e) the direct-mode B_d contributions independently reproduce two published
      per-d slice values (d=18 bottleneck, d=2 hub),
  (f) aggregate output self-consistency: total == A16 + B16, all roots positive,
      witness roots positive with the published A-split, top-50 all pair roots.

The parent structure is read from the cached pickle (regenerable via
cost16_parent_membership_20261118.load_parent from the pinned cover table +
regenerated candidate JSONL; see the cap16m pickled variant header) and checked
against the published cover-table row for the target parent.

Membership counts are combinatorial counts of minimum certificate-cover plans;
they are not search costs or verdicts. REFUTED-D10 and STERILE are not LOSS
proofs. The standard 11x11 empty board, the two-stone roots {49,60}/{59,60},
S2 {59,60}, and classes 1/2/4 remain UNKNOWN.
"""
import hashlib
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")

PHASE_A_PATH = os.path.join(OUT, "cost16-a-phase-20261118.json")
PHASE_A_PIN = "fe4b4b559fd8c3fdc9bc9b9f40a048fc3217c55b"
B16_PATH = os.path.join(OUT, "cost16-b-phase-total-20261118.json")
B16_PIN = "883275fba179c28988b5bfd3aaa3fab79be9be7c"
GROUPS_JSONL = os.path.join(OUT, "cost16-b-groups-20261118.jsonl")
DIRECT_JSONL = os.path.join(OUT, "cost16-b-direct-20261118.jsonl")
AGG_PATH = os.path.join(OUT, "cost16-b-phase-groups-20261118.json")
PICKLE_PATH = os.path.join(OUT, "parent-struct-cost16.pickle")

# Design-log 13-value table (research/log/2026-11-18-n11-cost16-phaseb-groups-design.md).
# (4,29) b_part is the documented transcription error: the table cell reads
# 25,742,803,159,389,724 while every computation epoch produces
# 25,742,823,159,389,724 (difference exactly 2e10).
DESIGN13 = {
    (0, 1): (91761792181385868, 27853976946079866),
    (0, 2): (78727963182297758, 24092183905989464),
    (0, 3): (78573131321269652, 24092183905989464),
    (3, 10): (69881310640344815, 21365825815916217),
    (3, 11): (74830779396074441, 22891368251601111),
    (3, 12): (71826162030315457, 22069237155645012),
    (3, 13): (66996614510092288, 20627613592072713),
    (4, 25): (83946802882578473, 25764337208160624),
    (4, 26): (83291084777602114, 25626317070513069),
    (4, 27): (80957772814234678, 24843883548513390),
    (4, 28): (80495793487071472, 24726663397917852),
    (4, 29): (83754150371345030, 25742803159389724),  # b_part = table's erroneous cell
    (4, 30): (90376219264155870, 27668435192725713),
}
CORRECT_429_B = 25742823159389724

# Pre-cleaning epoch records (removed from the publication JSONL; values from
# the 394-line scratch snapshot, recorded in the completion log).
PRE_CLEAN_DUP_08 = (84443033500707374, 25797556390267152)
PRE_CLEAN_429 = (83754150371345030, 25742823159389724)

A16 = 2305787291293934388
B16 = 660663050386546968
TOTAL = 2966450341680481356

checks = []


def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok),
                   "detail": detail if isinstance(detail, str)
                   else json.dumps(detail)})
    return bool(ok)


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def main():
    pa_bytes = open(PHASE_A_PATH, "rb").read()
    check("pin.phase_a_output", git_blob_sha(pa_bytes) == PHASE_A_PIN,
          git_blob_sha(pa_bytes))
    b16_bytes = open(B16_PATH, "rb").read()
    check("pin.b16_output", git_blob_sha(b16_bytes) == B16_PIN,
          git_blob_sha(b16_bytes))
    pa = json.loads(pa_bytes)
    b16out = json.loads(b16_bytes)
    check("pins.A16_B16_match_published",
          pa["derived"]["type_A_total"] == A16
          and b16out["derived"]["type_B_total"] == B16
          and b16out["derived"]["total_minimum_covers"] == TOTAL,
          {"A16": pa["derived"]["type_A_total"],
           "B16": b16out["derived"]["type_B_total"]})

    import pickle
    P, tbl = pickle.load(open(PICKLE_PATH, "rb"))
    r = len(P["target"])
    k = tbl["witness_size"]
    check("struct.parent_shape",
          r == 31 and k == 16 and tbl["exact"]
          and tbl["hex"] == "00000000000000003800000008001000",
          {"r": r, "k": k})
    hist = defaultdict(int)
    for root, cov in P["proot_rows"].items():
        hist[len(cov)] += 1
    check("struct.roots_histogram",
          dict(hist) == {1: 1483, 2: 425}
          and len(P["pair_roots"]) == 425
          and {len(rl) for rl in P["pair_roots"].values()} == {1},
          dict(hist))

    recs = {}
    summaries = 0
    dup = 0
    with open(GROUPS_JSONL) as f:
        for line in f:
            e = json.loads(line)
            if e.get("summary"):
                summaries += 1
                continue
            if e["root"] in recs:
                dup += 1
            recs[e["root"]] = e
    check("jsonl.no_duplicates", dup == 0, dup)
    check("jsonl.records_425", len(recs) == 425, len(recs))
    types = sorted(P["pair_roots"].keys())
    expected = {P["pair_roots"][t][0]: t for t in types}
    check("jsonl.root_set_matches_structure", set(recs) == set(expected),
          len(set(recs) ^ set(expected)))
    check("jsonl.pair_consistent",
          all(tuple(recs[root]["pair"]) == expected[root] for root in recs))

    sum_a = sum(e["a_part"] for e in recs.values())
    sum_b = sum(e["b_part"] for e in recs.values())
    check("identity.sum_a_eq_15A16", sum_a == 15 * A16,
          {"sum_a": str(sum_a), "15*A16": str(15 * A16)})
    check("identity.sum_b_eq_16B16_cross_lane", sum_b == 16 * B16,
          {"sum_b": str(sum_b), "16*B16": str(16 * B16)})

    bypair = {tuple(e["pair"]): e for e in recs.values()}
    exact12 = all(bypair[p]["a_part"] == a and bypair[p]["b_part"] == b
                  for p, (a, b) in DESIGN13.items() if p != (4, 29))
    check("design13.twelve_exact", exact12)
    e429 = bypair[(4, 29)]
    check("design13.a_part_429_matches", e429["a_part"] == DESIGN13[(4, 29)][0],
          e429["a_part"])
    check("design13.b_part_429_transcription_error",
          e429["b_part"] == CORRECT_429_B
          and DESIGN13[(4, 29)][1] == CORRECT_429_B - 20_000_000_000
          and PRE_CLEAN_429 == (e429["a_part"], CORRECT_429_B),
          {"jsonl_b": str(e429["b_part"]),
           "table_b": str(DESIGN13[(4, 29)][1]),
           "delta": 20000000000})
    e08 = bypair[(0, 8)]
    check("dup.removed_08_copy_identical",
          (e08["a_part"], e08["b_part"]) == PRE_CLEAN_DUP_08,
          {"kept": [e08["a_part"], e08["b_part"]], "pre": list(PRE_CLEAN_DUP_08)})

    bd = {e["d"]: e["b_d"] for e in b16out["derived"]["b_slices"]}
    direct = {}
    with open(DIRECT_JSONL) as f:
        for line in f:
            e = json.loads(line)
            direct[e["d"]] = e["contrib"]
    check("direct.b_d_rows_present", sorted(direct) == [2, 18], sorted(direct))
    check("direct.b_d_18_matches_slice", direct.get(18) == bd[18],
          {"direct": str(direct.get(18)), "slice": str(bd[18])})
    check("direct.b_d_2_matches_slice", direct.get(2) == bd[2],
          {"direct": str(direct.get(2)), "slice": str(bd[2])})

    agg = json.load(open(AGG_PATH))
    check("aggregate.all_pass", agg["all_pass"] and agg["check_count"] == 9)
    check("aggregate.total", agg["derived"]["total_minimum_covers"] == TOTAL
          and agg["derived"]["type_A_disjoint"] == A16
          and agg["derived"]["type_B_one_duplicate_row"] == B16)
    per_row = pa["derived"]["singleton_membership_stats"]["per_row"]
    mem = {}
    for root, e in recs.items():
        mem[root] = e["a_part"] + e["b_part"]
    root_row = {root: s for s, rl in P["singleton_roots"].items() for root in rl}
    for root, s in root_row.items():
        mem[root] = int(per_row[str(s)])
    check("aggregate.membership_map_consistent",
          agg["derived"]["membership"] == {x: mem[x] for x in sorted(mem)}
          and len(mem) == 1908
          and sum(mem.values()) == 16 * TOTAL,
          {"n": len(mem), "sum": str(sum(mem.values()))})
    wit = tbl["witness_roots"]
    check("aggregate.witness_positive",
          all(mem[x] > 0 for x in wit)
          and sorted(len(P["proot_rows"][x]) for x in wit) == [1] + [2] * 15)
    check("aggregate.all_roots_positive",
          all(v > 0 for v in mem.values()), min(mem.values()))
    top = agg["derived"]["top50_by_membership"]
    check("aggregate.top50_sorted_all_pair",
          len(top) == 50
          and all(top[i]["membership"] >= top[i + 1]["membership"]
                  for i in range(49))
          and all(e["kind"] == "pair" for e in top))
    pair_min = min(v for x, v in mem.items() if x not in root_row)
    sing_max = max(v for x, v in mem.items() if x in root_row)
    check("membership.pair_dominance",
          pair_min > sing_max,
          {"pair_min": str(pair_min), "singleton_max": str(sing_max),
           "ratio": pair_min / sing_max})

    out = {
        "schema": "n11-cost16-phaseb-groups-completion-verification-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Completion verification of the 425 pair-root memberships "
                  "(A/B split) for the 31-row cost-16 parent "
                  "00000000000000003800000008001000: cross-lane identity "
                  "sum(b_part)==16*B16, design-13 reconciliation with the "
                  "resolved (4,29) transcription error, direct-mode B_d spot "
                  "checks, aggregate self-consistency"),
        "inputs": {
            "phase_a_output": {"git_blob_sha1": PHASE_A_PIN},
            "b16_slice_output": {"git_blob_sha1": B16_PIN},
            "groups_jsonl": {"records": len(recs), "summaries": summaries},
            "direct_jsonl": {"rows": sorted(direct)},
            "aggregate_output": "cost16-b-phase-groups-20261118.json",
            "parent_pickle": ("(regenerable via cost16_parent_membership_"
                              "20261118.load_parent from the pinned cover "
                              "table and the regenerated candidate JSONL)"),
        },
        "headline": {
            "A16": A16, "B16": B16, "total": TOTAL,
            "sum_a_part": str(sum_a), "sum_b_part": str(sum_b),
            "cross_lane_check": "sum(b_part)/16 == published B16 (exact)",
            "membership_max": max(mem.values()),
            "membership_min": min(mem.values()),
            "pair_min": str(pair_min), "singleton_max": str(sing_max),
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(c["pass"] for c in checks),
        "interpretation_guard": (
            "Membership counts are counts of alternative minimum "
            "certificate-cover plans, not search costs or verdicts. "
            "REFUTED-D10 and STERILE are not LOSS proofs."),
        "unknown_status": (
            "Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    out_path = os.path.join(OUT, "cost16-phaseb-groups-completion-verification-20261118.json")
    with open(out_path, "w") as f:
        f.write(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"checks": len(checks), "all_pass": out["all_pass"],
                      "failed": [c["name"] for c in checks if not c["pass"]]},
                     indent=1))
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
