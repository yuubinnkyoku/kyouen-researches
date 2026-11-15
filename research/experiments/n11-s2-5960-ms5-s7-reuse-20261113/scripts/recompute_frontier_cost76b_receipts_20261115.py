#!/usr/bin/env python3
"""Class-2 frontier recomputation folding the class2-lane cost-76b WIN7 receipts
(2 WIN7-D10 bits 72, 96 of the second coverable class-2 target S5
00000000000000801202000000200000's cost-76 child
00000000000000801302000000200000, edge cost 76, demand c1=0,c2=1,c4=0) on top
of the merged cost-65l+74g+69i chain head (solved 1277, 2026-11-15).
"""
import csv
import hashlib
import itertools
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERTS = OUT / "class2-lane-cost76b-certificates"
TMP = OUT / "tmp-cost76b"
CHILD = "00000000000000801302000000200000"
CHILD_V = int(CHILD, 16)
PARENT1 = "00000000000000801202000000200000"
WIN_BITS = [72, 96]
ROOTS = {
    72: "00000000000001801302000000200000",
    96: "00000001000000801302000000200000",
}


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


def git_blob_sha_bytes(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


_orig_write_text = Path.write_text


def _write_text_lf(self, data, encoding=None, errors=None, newline=None):
    with self.open("w", encoding=encoding or "utf-8", errors=errors,
                   newline="\n") as f:
        f.write(data)


Path.write_text = _write_text_lf


# ---------- 1. reproduce the merged cost-65l+74g+69i chain head (1277) ----------
nsM = runpy.run_path(str(HERE / "scripts" / "recompute_frontier_merged_cost65l_74g_69i_20261115.py"))
s_base = nsM["s_cur"]
st_base = nsM["stM"]
covers = nsM["covers"]
manifest = nsM["manifest"]
classes = nsM["classes"]
summary_state = nsM["summary_state"]
remG = nsM["remM"]
demG = nsM["demM"]
prev = set(nsM["prev"]) | {int(r["root_hex"], 16) for r in nsM["merged_addition"]}
assert st_base["solved_s6_in_manifest"] == 1277 and st_base["unique_remaining_s6"] == 6570
assert st_base["sum_remaining_cost"] == 518896
assert st_base["s6_needed_by_open_classes"] == 4840 and st_base["cost_needed_by_open_classes"] == 382619
assert len(prev) == 548, len(prev)  # 532 pre-merge + 16 merged roots (2+10+4)
sha, blen = git_blob_sha(OUT / "class-frontier-merged-cost65l-74g-69i-recompute-20261115.json")
assert sha == "8d96b48273248073958b327ff91f7aecccd09944" and blen == 16208, \
    "regenerated merged head JSON must be byte-identical to main"
sha, blen = git_blob_sha(OUT / "class-frontier-s5-ranking-after-merged-cost65l-74g-69i-20261115.csv")
assert sha == "b149e71379e2e38f277e2ca59b4a27d41f35024e" and blen == 7539
sha, blen = git_blob_sha(OUT / "class-frontier-top-candidates-s6-after-merged-cost65l-74g-69i-20261115.csv")
assert sha == "8f72d7a8faf40d5437b2215cfb94eae719643c25" and blen == 7933
print("CONTROL merged 1277 chain head reproduced byte-identically: "
      "1277/6570/518896/4840/382619 (head JSON + both CSVs blob == main)")

# ---------- 2. claim + child remaining at the 1277 baseline ----------
claim_path = OUT / "class2-lane-cost76b-inflight-20261115.json"
claim = json.loads(claim_path.read_text())
assert claim["s6_child"] == CHILD and claim["s6_s7_edge_cost"] == 76
assert claim["demand"] == {"c1": 0, "c2": 1, "c4": 0}
assert claim["candidate_count"] == 76 and len(claim["legal_candidates"]) == 76
assert CHILD_V in manifest and CHILD_V not in s_base
p1_rows = remG.get(PARENT1, [])
p1_before = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in p1_rows}
assert CHILD in p1_before
assert (len(p1_before), sum(p1_before.values())) == (17, 1325)
d = demG[CHILD]
assert (d["c1"], d["c2"], d["c4"]) == (0, 1, 0), d
canon = nsM["canon"]
del_orbits = {s: canon(CHILD_V & ~(1 << s))
              for s in [i for i in range(121) if (CHILD_V >> i) & 1]}
p1_lift = [s for s, o in del_orbits.items() if f"{o:032x}" == PARENT1]
assert p1_lift, p1_lift
assert len(set(del_orbits.values())) == 6
print(f"CONTROL child genuinely remaining at head 1277: the second target S5 "
      f"holds the child row (17/1325), demand c1=0,c2=1,c4=0, lift stone {p1_lift}")

# ---------- 3. re-derive the sweep from the raw batches ----------
records = []
pilots = []
for i in range(1, 11):
    lines = [json.loads(x) for x in
             (OUT / f"class2-lane-cost76b-raw-batch{i}-20261115.jsonl").read_text().splitlines() if x]
    assert lines[0]["control"] == "pilot_d6" and lines[0]["loss"] is False and lines[0]["nodes"] == 3402
    pilots.append(lines[0]["nodes"])
    records.extend(lines[1:])
assert len(records) == 76
bits = [r["bit"] for r in records]
assert bits == claim["legal_candidates"], "raw candidate bits must equal the claim enumeration"
win = [r for r in records if r["loss"]]
ref = [r for r in records if not r["loss"]]
assert [r["bit"] for r in win] == WIN_BITS
assert len(ref) == 74 and not any(r["capped"] for r in records)
assert sum(r["nodes"] for r in records) == 107961863
for r in records:
    assert r["terminalStoneRange"][0] >= 13 and r["terminalStoneRange"][1] <= 17
    assert r["andclose"] is True
assert all(p == 3402 for p in pilots)
det = [json.loads(x) for x in (OUT / "class2-lane-cost76b-v16-determinism-rerun-20261115.jsonl").read_text().splitlines() if x]
assert det[0]["control"] == "pilot_d6" and det[0]["nodes"] == 3402
det_by_bit = {r["bit"]: r for r in det[1:]}
for b, rec in det_by_bit.items():
    raw = next(r for r in records if r["bit"] == b)
    assert rec["nodes"] == raw["nodes"] and rec["loss"] == raw["loss"]
v15 = [json.loads(x) for x in (OUT / "class2-lane-cost76b-v15-crosscheck-20261115.jsonl").read_text().splitlines() if x]
v15_pilots = [r for r in v15 if r.get("control") == "pilot_d6"]
assert len(v15_pilots) == 1 and v15_pilots[0]["nodes"] == 5949
v15_bits = {r["bit"]: r for r in v15 if "bit" in r}
for b in WIN_BITS:
    assert b in v15_bits and v15_bits[b]["loss"] is True
for b in (0, 1, 2):
    assert b in v15_bits and v15_bits[b]["loss"] is False
assert set(v15_bits) == set(WIN_BITS) | {0, 1, 2}
print("CONTROL sweep re-derived from 10 raw batches: 76 candidates exactly "
      "once, 2 WIN7-D10 / 74 REFUTED-D10 / 0 capped, 107,961,863 nodes, "
      "pilots 3402 x10, determinism rerun node-exact, v15 2/2 WIN + 3/3 "
      "refuted anchors")

# ---------- 4. certificates ----------
moves_all = json.loads((TMP / "legal-moves.json").read_text())
certs = {}
sums = {"rows": 0, "bytes": 0, "sub_roots_total": 0}
for bit in WIN_BITS:
    root = ROOTS[bit]
    receipt = json.loads((TMP / f"bit{bit}.cert-receipt.json").read_text())
    parts = sorted(CERTS.glob(f"bit{bit}-root-{root}.cert.part*of2"))
    if parts:
        whole = b"".join(p.read_bytes().replace(b"\r\n", b"\n") for p in parts)
    else:
        whole = (CERTS / f"bit{bit}-root-{root}.cert").read_bytes()
    assert len(whole) == receipt["bytes"], (bit, len(whole), receipt["bytes"])
    assert hashlib.md5(whole).hexdigest() == receipt["md5"], bit
    assert whole.startswith(b"n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS\n")
    assert whole.splitlines()[1] == b"root " + root.encode()
    rows = whole.splitlines()[2:]
    bj = json.loads((TMP / f"bit{bit}.bigint.json").read_text())
    ts = json.loads((TMP / f"bit{bit}.tsverify.json").read_text().splitlines()[-1])
    consumed = [x for x in (TMP / f"bit{bit}.consumed.txt").read_text().split() if x]
    assert bj["root_hex"] == root and bj["strategy_rows"] == len(rows)
    assert bj["union_missing"] == 0 and bj["union_extra"] == 0
    assert bj["subroots_passed"] == len(moves_all[str(bit)]["moves"])
    assert bj["terminal_range"] == [13, 17]
    assert ts["rows"] == len(rows) and len(set(consumed)) == len(rows)
    assert rows == sorted(set(rows)), bit
    certs[str(bit)] = {
        "bit": bit, "root_hex": root,
        "d4_canonical_hex": f"{canon(int(root, 16)):032x}",
        "rows": len(rows), "bytes": len(whole),
        "md5": receipt["md5"], "sha256": hashlib.sha256(whole).hexdigest(),
        "whole_git_blob_sha": git_blob_sha_bytes(whole),
        "sub_roots_total": len(moves_all[str(bit)]["moves"]),
        "loser_first_moves": moves_all[str(bit)]["moves"],
        "bigint_verifier": {"union_missing": 0, "union_extra": 0,
                            "subroots_passed": bj["subroots_passed"],
                            "terminal_range": bj["terminal_range"]},
        "ts_verifier": {"union_missing": 0, "union_extra": 0,
                        "consumed_distinct": len(set(consumed))},
        "v15_anchor_nodes": v15_bits[bit]["nodes"],
    }
    sums["rows"] += len(rows)
    sums["bytes"] += len(whole)
    sums["sub_roots_total"] += len(moves_all[str(bit)]["moves"])
assert sums["rows"] == 118437
assert sums["bytes"] == 4272471
assert sums["sub_roots_total"] == 121
print("CONTROL 2 published certificates asserted against joined LF bytes: "
      "118,437 rows / 4,272,471 bytes / 121 sub-roots; BigInt + Number "
      "Bareiss 2/2 PASS (union 0/0)")

# ---------- 5. root disjointness ----------
new_roots = {int(certs[str(b)]["root_hex"], 16) for b in WIN_BITS}
assert not (new_roots & prev)
prev_d4 = {f"{canon(r):032x}" for r in prev}
assert not ({certs[str(b)]["d4_canonical_hex"] for b in WIN_BITS} & prev_d4)
assert len({certs[str(b)]["d4_canonical_hex"] for b in WIN_BITS}) == 2
print("CONTROL root disjointness: 2 new roots vs 548 folded roots, raw-hex "
      "and D4-canonically; 2 distinct D4 orbits")

# ---------- 6. fold the 2 receipts ----------
s0 = set(s_base)
s_cur = set(s_base)
addition = []
zero_mim = []
child_closed_by = None
for bit in WIN_BITS:
    c = certs[str(bit)]
    root = int(c["root_hex"], 16)
    cov = covers(root)
    assert CHILD_V in cov, "every root covers the child via its added stone"
    marg = cov - s_cur
    marg_m = marg & manifest
    if CHILD_V in marg_m:
        assert child_closed_by is None, "the child must be closed exactly once"
        child_closed_by = bit
    rec = {
        "bit": bit, "root_hex": c["root_hex"],
        "d4_canonical_hex": c["d4_canonical_hex"],
        "certified": True, "covers": len(cov), "marginal": len(marg),
        "marginal_in_manifest": len(marg_m),
        "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_m),
        "marginal_non_manifest_hexes": sorted(f"{k:032x}" for k in marg - marg_m),
        "rows": c["rows"], "md5": c["md5"],
        "sub_roots_pass": c["sub_roots_total"],
        "v15_anchor_nodes": c["v15_anchor_nodes"],
    }
    addition.append(rec)
    if not marg_m:
        zero_mim.append(bit)
    s_cur |= marg
assert child_closed_by == 72, "the child orbit must be closed by the first receipt"
cov2 = set()
for bit in WIN_BITS:
    cov2 |= covers(int(certs[str(bit)]["root_hex"], 16))
assert s_cur == set(s_base) | cov2, "set-equality: s_after == s_1277 UNION covers(2 roots)"
total_mim = sum(a["marginal_in_manifest"] for a in addition)
total_marg = sum(a["marginal"] for a in addition)
stF2, remF2, uniqF2, demF2 = summary_state(s_cur)
assert stF2["solved_s6_in_manifest"] == 1277 + total_mim
assert s_cur >= s0
assert CHILD_V in s_cur and CHILD_V in manifest
assert CHILD not in {r["s6_hex"] for r in remF2.get(PARENT1, [])}
rows_after_p1 = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in remF2.get(PARENT1, [])}
p1_lost = set(p1_before) - set(rows_after_p1)
cov2_hexes = {f"{k:032x}" for k in cov2}
assert CHILD in p1_lost
assert p1_lost <= cov2_hexes, sorted(p1_lost - cov2_hexes)
print("AFTER cost-76b receipts:", json.dumps(stF2, indent=1))
print(f"total marginal={total_marg} marginal_in_manifest={total_mim}; "
      f"zero-mim receipts: {zero_mim or 'none'}; child orbit closed by bit{child_closed_by}; "
      f"parent1 (second target) {len(rows_after_p1)} rows / {sum(rows_after_p1.values())} "
      f"(was 17/1325, lost {sorted(p1_lost)})")

# ---------- 7. outputs ----------
def best(rem, bit):
    return sorted(
        ({"s5_hex": k, "classes": classes.get(k, 0),
          "remaining_s6_orbits": len(rows),
          "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r["remaining_s6_orbits"], r["remaining_s7_edge_cost"], r["s5_hex"]))

class2 = best(remF2, 2)
class4 = best(remF2, 4)
AUDIT_BLOCKED = "00000000000000809082000000000000"
result = {
    "schema": "n11-class-frontier-cost76b-receipts-recompute-20261115-v1",
    "date": "2026-11-15",
    "baseline_main": "class-frontier-merged-cost65l-74g-69i-recompute-20261115.json "
                     "(merged chain head 1277/6570/518896/4840/382619; "
                     "regenerated byte-identical, git blob sha "
                     "8d96b48273248073958b327ff91f7aecccd09944)",
    "method": "runpy reproduction of the merged 1277 chain head (asserting "
              "1277/6570/518896/4840/382619 and the blob-identical merged head "
              "JSON and both merged CSVs), the cost-76b child asserted genuinely "
              "remaining at the 1277 baseline (the second target S5 "
              "00000000000000801202000000200000 holds the child row at 17 rows / "
              "1325, demand c1=0,c2=1,c4=0 re-derived, one-stone deletion "
              "re-derived), the sweep re-derived from the ten raw batch JSONLs "
              "(76 candidates exactly once, 2 WIN7-D10 / 74 REFUTED-D10 / 0 "
              "capped / 107,961,863 nodes, roots == child | 1<<bit, 2 distinct "
              "D4 orbits, pilots 3402 x10, determinism rerun node-exact), the "
              "v15 cross-engine anchors asserted (2 WIN loss=true, refuted "
              "anchors bits 0/1/2 loss=false, pilot 5949), both published "
              "certificates asserted against the joined LF bytes (md5/bytes "
              "from the extraction receipts, rows sorted-unique, sub-roots == "
              "loser mobility, terminal 13..17, BigInt and Number Bareiss "
              "verifier PASS / union 0/0), the 2 roots asserted disjoint from "
              "the 548 folded receipt roots both raw-hex and D4-canonically, "
              "then the 2 receipts folded in publication order [72, 96]; the "
              "child-orbit closure (bit72) and a set-equality control hold",
    "controls": {
        "chain_head_1277_reproduced_byte_identical": True,
        "child_genuinely_remaining_at_baseline": True,
        "open_parent_held_child_row_at_baseline": True,
        "sweep_rederived_from_raw_batches": True,
        "determinism_rerun_node_exact": True,
        "v15_cross_engine_anchors_verified": True,
        "certificates_bytes_md5_verified": True,
        "root_disjointness_vs_548_roots": True,
        "child_orbit_closure": "closed by the bit-72 receipt (first in publication order), of this fold",
        "set_equality_after_2": "s == s_1277 UNION covers(2 cost-76b roots)",
    },
    "target": {
        "s5_parent_hex": PARENT1, "s6_child_hex": CHILD, "edge_cost": 76,
        "open_parents": [PARENT1],
        "demand_at_baseline_1277": {"c1": 0, "c2": 1, "c4": 0},
        "child_orbit_closure": "closed by the bit-72 receipt of this fold",
        "candidates": 76, "win7_d10": 2, "refuted_d10": 74, "capped": 0,
        "candidate_nodes": 107961863,
        "remaining_rows_after": {
            "parent1_orbits": len(rows_after_p1),
            "parent1_edge_cost": sum(rows_after_p1.values()),
        },
    },
    "cost76b_addition": addition,
    "totals": {
        "receipts": 2, "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "zero_marginal_in_manifest": [f"bit{b}" for b in zero_mim],
        "child_closed_by_bit": child_closed_by,
        "certificate_rows": sums["rows"],
        "certificate_bytes": sums["bytes"],
        "certificate_sub_roots": sums["sub_roots_total"],
        "v15_crosscheck_nodes_sum": sum(v15_bits[b]["nodes"] for b in WIN_BITS),
        "v16_sweep_win_nodes_sum": sum(r["nodes"] for r in win),
    },
    "frontier_after_cost76b": {
        "solved_s6_in_manifest": stF2["solved_s6_in_manifest"],
        "remaining_s5_orbits": stF2["remaining_s5_orbits"],
        "unique_remaining_s6": stF2["unique_remaining_s6"],
        "sum_remaining_cost": stF2["sum_remaining_cost"],
        "s6_needed_by_open_classes": stF2["s6_needed_by_open_classes"],
        "cost_needed_by_open_classes": stF2["cost_needed_by_open_classes"],
        "demand_histogram_open_only": stF2["hist"],
        "best_class2": class2[0] if class2 else None,
        "audit_blocked_class2": next((c for c in class2 if c["s5_hex"] == AUDIT_BLOCKED), None),
        "best_coverable_class2": next((c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED), None),
        "next_class2": class2[1:4],
        "best_class4": class4[0] if class4 else None,
        "next_class4": class4[1:4],
    },
    "outstanding_not_folded": {
        "cost75d": "second target cost-75 row; sweep in flight on a parallel lane",
        "cost74h": "sterile sweep, no fold material",
        "next_fold_baseline": "this chain head (see frontier_after_cost76b) is "
                              "the new canonical baseline for all subsequent "
                              "folds; assert it before extending",
    },
    "interpretation_guard": "bookkeeping over published receipts; solved counts "
                            "measure manifest coverage, not the game-theoretic "
                            "value of any position; REFUTED-D10 sweeps prove "
                            "only absence of WIN7-D10; WIN7 certificates prove "
                            "a win within depth 10 from the individual "
                            "7-stone roots only; 11x11 empty board / two-stone "
                            "root {49,60} / S2 {59,60} remain UNKNOWN",
}
(OUT / "class-frontier-cost76b-receipts-recompute-20261115.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-cost76b-receipts-recompute-20261115.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in remF2.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / "class-frontier-s5-ranking-after-cost76b-receipts-20261115.csv").open(
        "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits", "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / "class-frontier-top-candidates-s6-after-cost76b-receipts-20261115.csv").open(
        "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    coverable = [c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED]
    for label, cand in (("best class-4 blocker-candidate S5", class4[0] if class4 else None),
                        ("best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)",
                         next((c for c in class2 if c["s5_hex"] == AUDIT_BLOCKED), None)),
                        ("best coverable class-2 blocker-candidate S5",
                         coverable[0] if coverable else None),
                        ("second coverable class-2 candidate S5",
                         coverable[1] if len(coverable) > 1 else None)):
        if cand is None:
            continue
        rows = remF2.get(cand["s5_hex"], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(("s5_hex", "s6_hex", "s6_s7_edge_cost", "demand"))
        for row in sorted(rows, key=lambda r: int(r["s6_s7_edge_cost"])):
            d = demF2[row["s6_hex"]]
            w.writerow((cand["s5_hex"], row["s6_hex"], row["s6_s7_edge_cost"],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print("written ranking + top-candidates CSVs (after-cost76b-receipts)")

# ---------- 8. completed-claim control ----------
claim = json.loads(claim_path.read_text())
if claim.get("status", "").startswith("completed") and "fold" in claim:
    f = claim["fold"]
    head_str = (f"{stF2['solved_s6_in_manifest']}/{stF2['unique_remaining_s6']}/"
                f"{stF2['sum_remaining_cost']}/{stF2['s6_needed_by_open_classes']}/"
                f"{stF2['cost_needed_by_open_classes']}")
    assert f["chain_head_before"] == "1277/6570/518896/4840/382619"
    assert f["chain_head_after"] == head_str
    assert f["total_marginal"] == total_marg
    assert f["total_marginal_in_manifest"] == total_mim
    assert f["child_orbit_closed_by_bit"] == child_closed_by
    assert f["parents_after"]["parent1"] == f"{len(rows_after_p1)} rows / {sum(rows_after_p1.values())}"
    obs = f["output_blob_shas"]
    sha_out, blen_out = git_blob_sha(OUT / "class-frontier-cost76b-receipts-recompute-20261115.json")
    assert sha_out == obs["head_json"] and blen_out == f["head_json_bytes"]
    sha_out, blen_out = git_blob_sha(OUT / "class-frontier-s5-ranking-after-cost76b-receipts-20261115.csv")
    assert sha_out == obs["ranking_csv"] and blen_out == f["ranking_csv_bytes"]
    sha_out, blen_out = git_blob_sha(OUT / "class-frontier-top-candidates-s6-after-cost76b-receipts-20261115.csv")
    assert sha_out == obs["top_candidates_csv"] and blen_out == f["top_candidates_csv_bytes"]
    print("CONTROL completed claim fold record matches this recomputation: head "
          + head_str + ", three output blobs re-asserted byte-identical")
