#!/usr/bin/env python3
"""Re-base facts for the in-flight class2-lane claims on the reconciled
canonical head 1405/6443/509457/4713/373180.

The cost-75e claim (class2-lane-cost75e-inflight-20261116.json) references the
superseded merged head 1400 and the cost-76c claim
(class2-lane-cost76c-inflight-20261116.json) references the superseded cost-70g
fork head 1403; both must re-base onto the reconciled canonical head before
folding.  This script reproduces the reconciled head (running the published
reconciliation script, which re-asserts the whole chain, the 70g fold, the
canonical 1400 reconstruction and the reconciliation fold), re-asserts the
three reconciliation output blobs byte-identical to main, then re-derives the
exact status of both claimed children at the reconciled head: genuinely
remaining, in-manifest, open parents with rows/cost/lift stones, edge costs
and demand equal to the claims.  It also emits the full remaining-row
worklist of the second coverable class-2 candidate S5 at 1405 with the prior
lane records (cost-64a STERILE, cost-71d STERILE, cost-75e and cost-76c
claims, and the two unclaimed rows).

Bookkeeping over published receipts; no game-theoretic claim.  11x11 empty
board / two-stone root {49,60} / class 1 / class 2 / class 4 remain UNKNOWN.
"""
import hashlib
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"

CHILD_75E = "00000000040000809002000000000002"
CHILD_76C = "00000000010000809002000001000000"
SECOND_CANDIDATE = "00000000000000801202000040000000"


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


_orig_write_text = Path.write_text


def _write_text_lf(self, data, encoding=None, errors=None, newline=None):
    with self.open("w", encoding=encoding or "utf-8", errors=errors,
                   newline="\n") as f:
        f.write(data)


Path.write_text = _write_text_lf

# ---------- 1. reproduce the reconciled canonical head 1405 ----------
nsR = runpy.run_path(str(HERE / "scripts" /
                         "recompute_frontier_reconcile_canonical1400_"
                         "cost70g_20261116.py"))
s_new = set(nsR["s_new"])
rem_new = nsR["rem_new"]
dem_new = nsR["dem_new"]
manifest = nsR["manifest"]
canon = nsR["canon"]
classes = nsR["classes"]
st_new = nsR["st_new"]
P1 = nsR["PARENT1"]
assert (st_new["solved_s6_in_manifest"], st_new["unique_remaining_s6"],
        st_new["sum_remaining_cost"], st_new["s6_needed_by_open_classes"],
        st_new["cost_needed_by_open_classes"]) == (1405, 6443, 509457, 4713,
                                                   373180)
for name, sha_exp, blen_exp in (
        ("class-frontier-reconciled-canonical1400-cost70g-"
         "recompute-20261116.json",
         "b3ad19d7bfd48c771d5a6827707a9f26940dc1bb", 11352),
        ("class-frontier-s5-ranking-after-reconciled-canonical1400-"
         "cost70g-20261116.csv",
         "26fa720b9935ea3bfa1445409d941a5063c52694", 7535),
        ("class-frontier-top-candidates-s6-after-reconciled-canonical1400-"
         "cost70g-20261116.csv",
         "c3433eeecccf0098a04f227af876b37196c7c0a5", 3801)):
    sha, blen = git_blob_sha(OUT / name)
    assert sha == sha_exp and blen == blen_exp, name
print("CONTROL reconciled canonical head 1405/6443/509457/4713/373180 "
      "reproduced; the three reconciliation output blobs re-asserted "
      "byte-identical to main")


def child_facts(child, lane, claimed_edge_cost, claimed_demand):
    cv = int(child, 16)
    assert cv in manifest, lane
    assert cv not in s_new, f"{lane}: the child must remain open at 1405"
    parents = []
    for s5_hex, rows in rem_new.items():
        d1 = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rows}
        if child in d1:
            lift = [s for s in range(121) if (cv >> s) & 1
                    and f"{canon(cv & ~(1 << s)):032x}" == s5_hex]
            assert lift, (lane, s5_hex, "every open parent of the child must "
                                      "be a one-stone D4 lift of the child")
            parents.append({
                "s5_hex": s5_hex, "classes": classes.get(s5_hex, 0),
                "rows": len(d1), "edge_cost": sum(d1.values()),
                "child_edge_cost": d1[child], "lift_stone": lift,
            })
    assert parents, lane
    assert {p["child_edge_cost"] for p in parents} == {claimed_edge_cost}, lane
    d = dem_new[child]
    assert (d["c1"], d["c2"], d["c4"]) == (claimed_demand["c1"],
                                           claimed_demand["c2"],
                                           claimed_demand["c4"]), lane
    stones = [s for s in range(121) if (cv >> s) & 1]
    print(f"CONTROL {lane} child {child} genuinely remaining at 1405: "
          f"{len(parents)} open parent(s) "
          + ", ".join(f"{p['s5_hex']} {p['rows']} rows / {p['edge_cost']} "
                      f"(lift stone {p['lift_stone'][0]})"
                      for p in sorted(parents, key=lambda p: p["s5_hex"]))
          + f", edge cost {claimed_edge_cost}, demand "
          f"c1={d['c1']},c2={d['c2']},c4={d['c4']}")
    return {
        "child_hex": child, "child_stones_bit_indices": stones,
        "child_edge_cost": claimed_edge_cost,
        "demand_at_canonical1405": {"c1": d["c1"], "c2": d["c2"],
                                    "c4": d["c4"]},
        "in_manifest": True, "genuinely_remaining_at_1405": True,
        "open_parents_at_canonical1405": sorted(
            parents, key=lambda p: (p["rows"], p["s5_hex"])),
    }


# ---------- 2. the two in-flight claims ----------
facts_75e = child_facts(
    CHILD_75E, "cost75e", 75, {"c1": 0, "c2": 2, "c4": 0})
facts_75e["claim_baseline_superseded"] = \
    "1400/6448/509842/4718/373565 (merged head, commit 2fbb5aa2)"
facts_75e["claim_record"] = \
    "class2-lane-cost75e-inflight-20261116.json: sweep completed locally " \
    "(75 candidates, 4 claimed WIN7-D10 bits 6/10/11/37, 0 capped, " \
    "108,292,517 nodes, determinism rerun node-exact); raw batches, " \
    "certificates and fold NOT yet published (environment went unavailable " \
    "mid-certification) - the local numbers are a coordination memo, not " \
    "published evidence"
facts_76c = child_facts(
    CHILD_76C, "cost76c", 76, {"c1": 0, "c2": 2, "c4": 0})
facts_76c["claim_baseline_superseded"] = \
    "1403/6445/509589/4715/373312 (cost-70g fork head, commit dee808f0)"
facts_76c["claim_record"] = \
    "class2-lane-cost76c-inflight-20261116.json: in-flight, 76 legal " \
    "candidates"

# ---------- 3. second candidate S5 remaining-row worklist at 1405 ----------
rows_p1 = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_new.get(P1, [])}
assert (len(rows_p1), sum(rows_p1.values())) == (6, 439)
prior = {
    "00000000000000801282000040000000":
        "STERILE: cost-64a claim (class2-lane-cost64a-inflight-20261116.json) "
        "completed, 64 candidates, 0 WIN7-D10",
    "00000000000000801202000040000400":
        "STERILE: cost-71d claim (class2-lane-cost71d-inflight-20261116.json) "
        "completed, 71/71 REFUTED-D10, 97,476,178 nodes, no fold",
    "00000000040000809002000000000002":
        "cost-75e claim, sweep completed locally, artifacts unpublished",
    "00000000010000809002000001000000":
        "cost-76c claim, in-flight",
}
worklist = []
for h, c in sorted(rows_p1.items(), key=lambda kv: (kv[1], kv[0])):
    d = dem_new[h]
    worklist.append({
        "s6_hex": h, "s6_s7_edge_cost": c,
        "demand": {"c1": d["c1"], "c2": d["c2"], "c4": d["c4"]},
        "prior_record": prior.get(h, "no prior claim on file"),
    })
print("second candidate S5 worklist at 1405: "
      + "; ".join(f"{w['s6_hex']} edge {w['s6_s7_edge_cost']} "
                  f"({w['prior_record'].split(':')[0]})"
                  for w in worklist))

result = {
    "schema": "n11-class2-lane-rebase-facts-canonical1405-20261116-v1",
    "date": "2026-11-16",
    "canonical_head": {
        "head": "1405/6443/509457/4713/373180",
        "source": "class-frontier-reconciled-canonical1400-cost70g-"
                  "recompute-20261116.json (git blob sha "
                  "b3ad19d7bfd48c771d5a6827707a9f26940dc1bb, commit ca0e8c42)",
        "reproduced": "the reconciliation script re-run end-to-end; the "
                      "three reconciliation output blobs re-asserted "
                      "byte-identical",
    },
    "cost75e_rebase_facts": facts_75e,
    "cost76c_rebase_facts": facts_76c,
    "second_candidate_worklist_at_1405": {
        "s5_hex": SECOND_CANDIDATE, "rows": 6, "edge_cost": 439,
        "rows_detail": worklist,
        "note": "rows at edge 64 and 71 are STERILE for WIN7-D10 at depth 10 "
                "(cost-64a / cost-71d sweeps), so the second candidate S5 can "
                "only be closed through the remaining four rows (75/76/76/77)",
    },
    "rebase_rule": "any fold or claim landing after commit ca0e8c42 must use "
                   "the reconciled canonical head 1405/6443/509457/4713/373180 "
                   "as its baseline; the 75e and 76c claim files must record "
                   "the re-based baseline when they retire",
    "interpretation_guard": "bookkeeping over published receipts; solved "
                            "counts measure manifest coverage, not the "
                            "game-theoretic value of any position; REFUTED-D10 "
                            "sweeps prove only absence of WIN7-D10; STERILE "
                            "rows are unclosable by depth-10 WIN7 receipts, "
                            "which is NOT a LOSS proof; 11x11 empty board / "
                            "two-stone root {49,60} / S2 {59,60} / class 1 / "
                            "class 2 / class 4 remain UNKNOWN",
}
(OUT / "class2-lane-rebase-facts-75e-76c-on-canonical1405-20261116.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class2-lane-rebase-facts-75e-76c-on-canonical1405-20261116.json")
sha, blen = git_blob_sha(OUT / "class2-lane-rebase-facts-75e-76c-on-"
                               "canonical1405-20261116.json")
print(f"blob class2-lane-rebase-facts-75e-76c-on-canonical1405-20261116.json: "
      f"{sha} ({blen} bytes)")
