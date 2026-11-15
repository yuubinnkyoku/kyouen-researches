#!/usr/bin/env python3
"""Class-2 frontier recomputation folding the class2-lane cost-69i WIN7 receipts
(4 WIN7-D10 bits 21, 29, 97, 100 of the third coverable class-2 target S5
00000000000000809102000000000000's LAST remaining child
00000000000000809102000000002000, edge cost 69, demand c1=0,c2=2,c4=2) on top
of the merged cost-65l+74g receipts chain head (solved 1270, 2026-11-15).

Closing this child leaves the third target S5 with zero remaining rows, i.e. all
of its six-stone children are first-player WINs, so the S5 itself is a
first-player WIN and the class-2 blocker closes conditionally.
"""
import csv
import hashlib
import itertools
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERTS = OUT / "class2-lane-cost69i-certificates"
TMP = OUT / "tmp-cost69i"
ROOT = HERE.parent.parent.parent
CHILD = "00000000000000809102000000002000"
CHILD_V = int(CHILD, 16)
PARENT1 = "00000000000000809102000000000000"
PARENT2 = "00000000000000801202000000080000"
PARENT3 = "00000000000000003800000000810000"
WIN_BITS = [21, 29, 97, 100]
ROOTS = {
    21: "00000000000000809102000000202000",
    29: "00000000000000809102000020002000",
    97: "00000002000000809102000000002000",
    100: "00000010000000809102000000002000",
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


# ---------- 1. reproduce the merged cost-65l+74g chain head (1270) ----------
nsM = runpy.run_path(str(HERE / "scripts" / "recompute_frontier_merged_cost65l_74g_20261115.py"))
s_base = nsM["s_cur"]
st_base = nsM["stM"]
covers = nsM["covers"]
manifest = nsM["manifest"]
classes = nsM["classes"]
summary_state = nsM["summary_state"]
remG = nsM["remM"]
demG = nsM["demM"]
prev = set(nsM["prev"]) | {int(r["root_hex"], 16) for r in nsM["merged_addition"]}
assert st_base["solved_s6_in_manifest"] == 1270 and st_base["unique_remaining_s6"] == 6577
assert st_base["sum_remaining_cost"] == 519427
assert st_base["s6_needed_by_open_classes"] == 4847 and st_base["cost_needed_by_open_classes"] == 383150
assert len(prev) == 544, len(prev)  # 532 pre-merge + 12 merged roots (2 cost-65l + 10 cost-74g)
sha, blen = git_blob_sha(OUT / "class-frontier-merged-cost65l-74g-recompute-20261115.json")
assert sha == "0210953083309c1dd2d8f1cf036ec1f91e88f267" and blen == 12459, \
    "regenerated merged head JSON must be byte-identical to main"
sha, blen = git_blob_sha(OUT / "class-frontier-s5-ranking-after-merged-cost65l-74g-20261115.csv")
assert sha == "5d88b9c10067679ea37d9c6ee92448518dc81702" and blen == 7579
sha, blen = git_blob_sha(OUT / "class-frontier-top-candidates-s6-after-merged-cost65l-74g-20261115.csv")
assert sha == "7de39cf887e8ea2452304e1b0393fdbcfe81947d" and blen == 4576
print("CONTROL merged cost-65l+74g chain head reproduced byte-identically: "
      "1270/6577/519427/4847/383150 (head JSON + both CSVs blob == main)")

# ---------- 2. claim + child remaining at the 1270 baseline ----------
claim_path = OUT / "class2-lane-cost69i-inflight-20261115.json"
claim = json.loads(claim_path.read_text())
assert claim["s6_child"] == CHILD and claim["s6_s7_edge_cost"] == 69
assert claim["demand"] == {"c1": 0, "c2": 2, "c4": 2}
assert claim["candidate_count"] == 69 and len(claim["legal_candidates"]) == 69
assert CHILD_V in manifest and CHILD_V not in s_base
parents = {}
for name, h in (("parent1", PARENT1), ("parent2", PARENT2), ("parent3", PARENT3)):
    rows = remG.get(h, [])
    d = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rows}
    assert CHILD in d, name
    parents[name] = d
assert (len(parents["parent1"]), sum(parents["parent1"].values())) == (1, 69)
assert (len(parents["parent2"]), sum(parents["parent2"].values())) == (72, 5477)
assert (len(parents["parent3"]), sum(parents["parent3"].values())) == (84, 6815)
d = demG[CHILD]
assert (d["c1"], d["c2"], d["c4"]) == (0, 2, 2), d
canon = nsM["canon"]
del_orbits = {s: canon(CHILD_V & ~(1 << s))
              for s in [i for i in range(121) if (CHILD_V >> i) & 1]}
lifts = {name: [s for s, o in del_orbits.items() if f"{o:032x}" == h]
         for name, h in (("parent1", PARENT1), ("parent2", PARENT2), ("parent3", PARENT3))}
assert all(lifts.values()), lifts
assert len(set(del_orbits.values())) == 6
print(f"CONTROL child genuinely remaining at head 1270: three open parents hold "
      f"the child row (1/69, 72/5477, 84/6815), demand c1=0,c2=2,c4=2, lift "
      f"stones {lifts}")

# ---------- 3. re-derive the sweep from the raw batches ----------
records = []
pilots = []
for i in range(1, 10):
    lines = [json.loads(x) for x in
             (OUT / f"class2-lane-cost69i-raw-batch{i}-20261115.jsonl").read_text().splitlines() if x]
    assert lines[0]["control"] == "pilot_d6" and lines[0]["loss"] is False and lines[0]["nodes"] == 3402
    pilots.append(lines[0]["nodes"])
    records.extend(lines[1:])
assert len(records) == 69
bits = [r["bit"] for r in records]
assert bits == claim["legal_candidates"], "raw candidate bits must equal the claim enumeration"
win = [r for r in records if r["loss"]]
ref = [r for r in records if not r["loss"]]
assert [r["bit"] for r in win] == WIN_BITS
assert len(ref) == 65 and not any(r["capped"] for r in records)
assert sum(r["nodes"] for r in records) == 62994015
for r in records:
    assert r["terminalStoneRange"][0] >= 13 and r["terminalStoneRange"][1] <= 17
    assert r["andclose"] is True
assert all(p == 3402 for p in pilots)
det = [json.loads(x) for x in (OUT / "class2-lane-cost69i-v16-determinism-rerun-20261115.jsonl").read_text().splitlines() if x]
assert det[0]["control"] == "pilot_d6" and det[0]["nodes"] == 3402
det_by_bit = {r["bit"]: r for r in det[1:]}
for b, rec in det_by_bit.items():
    raw = next(r for r in records if r["bit"] == b)
    assert rec["nodes"] == raw["nodes"] and rec["loss"] == raw["loss"]
v15 = [json.loads(x) for x in (OUT / "class2-lane-cost69i-v15-crosscheck-20261115.jsonl").read_text().splitlines() if x]
v15_pilots = [r for r in v15 if r.get("control") == "pilot_d6"]
assert len(v15_pilots) == 1 and v15_pilots[0]["nodes"] == 5949
v15_bits = {r["bit"]: r for r in v15 if "bit" in r}
for b in WIN_BITS:
    assert b in v15_bits and v15_bits[b]["loss"] is True
for b in (0, 1, 2):
    assert b in v15_bits and v15_bits[b]["loss"] is False
assert set(v15_bits) == set(WIN_BITS) | {0, 1, 2}
print("CONTROL sweep re-derived from 9 raw batches: 69 candidates exactly "
      "once, 4 WIN7-D10 / 65 REFUTED-D10 / 0 capped, 62,994,015 nodes, "
      "pilots 3402 x9, determinism rerun node-exact, v15 4/4 WIN + 3/3 "
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
assert sums["rows"] == 204339
assert sums["bytes"] == 7379919
assert sums["sub_roots_total"] == 216
print("CONTROL 4 published certificates asserted against joined LF bytes: "
      "204,339 rows / 7,374,919 bytes / 216 sub-roots; BigInt + Number "
      "Bareiss 4/4 PASS (union 0/0)")

# ---------- 5. root disjointness ----------
new_roots = {int(certs[str(b)]["root_hex"], 16) for b in WIN_BITS}
assert not (new_roots & prev)
prev_d4 = {f"{canon(r):032x}" for r in prev}
assert not ({certs[str(b)]["d4_canonical_hex"] for b in WIN_BITS} & prev_d4)
assert len({certs[str(b)]["d4_canonical_hex"] for b in WIN_BITS}) == 4
print("CONTROL root disjointness: 4 new roots vs 542 folded roots, raw-hex "
      "and D4-canonically; 4 distinct D4 orbits")

# ---------- 6. fold the 4 receipts ----------
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
assert child_closed_by == 21, "the child orbit must be closed by the first receipt"
cov4 = set()
for bit in WIN_BITS:
    cov4 |= covers(int(certs[str(bit)]["root_hex"], 16))
assert s_cur == set(s_base) | cov4, "set-equality: s_after == s_1270 UNION covers(4 roots)"
total_mim = sum(a["marginal_in_manifest"] for a in addition)
total_marg = sum(a["marginal"] for a in addition)
stF2, remF2, uniqF2, demF2 = summary_state(s_cur)
assert stF2["solved_s6_in_manifest"] == 1270 + total_mim
assert s_cur >= s0
assert CHILD_V in s_cur and CHILD_V in manifest
for name, h in (("parent1", PARENT1), ("parent2", PARENT2), ("parent3", PARENT3)):
    assert CHILD not in {r["s6_hex"] for r in remF2.get(h, [])}, name
rows_after = {}
lost = {}
for name, h in (("parent1", PARENT1), ("parent2", PARENT2), ("parent3", PARENT3)):
    rows_after[name] = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in remF2.get(h, [])}
    lost[name] = set(parents[name]) - set(rows_after[name])
    assert CHILD in lost[name]
    assert lost[name] <= {f"{k:032x}" for k in cov4}, (name, sorted(lost[name]))
assert len(rows_after["parent1"]) == 0, "the third target S5 must have zero remaining rows"
print("AFTER cost-69i receipts:", json.dumps(stF2, indent=1))
print(f"total marginal={total_marg} marginal_in_manifest={total_mim}; "
      f"zero-mim receipts: {zero_mim or 'none'}; child orbit closed by bit{child_closed_by}; "
      f"parent1 (third target) {len(rows_after['parent1'])} rows / {sum(rows_after['parent1'].values())} (was 1/69); "
      f"parent2 {len(rows_after['parent2'])} rows / {sum(rows_after['parent2'].values())} (was 72/5477); "
      f"parent3 {len(rows_after['parent3'])} rows / {sum(rows_after['parent3'].values())} (was 84/6815)")

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
third_target_closed = PARENT1 not in remF2
result = {
    "schema": "n11-class-frontier-merged-cost65l-74g-69i-recompute-20261115-v1",
    "date": "2026-11-15",
    "baseline_main": "class-frontier-merged-cost65l-74g-recompute-20261115.json "
                     "(merged cost-65l+74g chain head 1270/6577/519427/4847/383150; "
                     "regenerated byte-identical, git blob sha "
                     "0210953083309c1dd2d8f1cf036ec1f91e88f267)",
    "method": "runpy reproduction of the merged cost-65l+74g chain head (asserting "
              "1270/6577/519427/4847/383150 and the blob-identical merged head "
              "JSON and both merged CSVs), the cost-69i child asserted genuinely "
              "remaining at the 1270 baseline (three open parents: third target "
              "S5 00000000000000809102000000000000 at 1 row / 69, class-2 S5 "
              "00000000000000801202000000080000 at 72 rows / 5477, class-4 S5 "
              "00000000000000003800000000810000 at 84 rows / 6815; demand "
              "c1=0,c2=2,c4=2 re-derived), the sweep re-derived from the nine "
              "raw batch JSONLs (69 candidates exactly once, 4 WIN7-D10 / 65 "
              "REFUTED-D10 / 0 capped / 62,994,015 nodes, roots == child | "
              "1<<bit, 4 distinct D4 orbits, pilots 3402 x9, determinism rerun "
              "node-exact), the v15 cross-engine anchors asserted (4 WIN "
              "loss=true, refuted anchors bits 0/1/2 loss=false, pilot 5949), "
              "all 4 published certificates asserted against the joined LF "
              "bytes (md5/bytes from the extraction receipts, rows "
              "sorted-unique, sub-roots == loser mobility, terminal 13..17, "
              "BigInt and Number Bareiss verifier PASS / union 0/0), the 4 "
              "roots asserted disjoint from the 542 folded receipt roots both "
              "raw-hex and D4-canonically, then the 4 receipts folded in "
              "publication order [21, 29, 97, 100]; the child-orbit closure "
              "(bit21), the zero-remaining-rows control for the third target "
              "S5 and a set-equality control all hold. Receipts only",
    "controls": {
        "chain_head_1270_reproduced_byte_identical": True,
        "child_genuinely_remaining_at_baseline": True,
        "three_open_parents_held_child_row_at_baseline": True,
        "sweep_rederived_from_raw_batches": True,
        "determinism_rerun_node_exact": True,
        "v15_cross_engine_anchors_verified": True,
        "certificates_bytes_md5_verified": True,
        "root_disjointness_vs_542_roots": True,
        "child_orbit_closure": "closed by the bit-21 receipt (first in publication order), of this fold",
        "third_target_s5_zero_remaining_rows": True,
        "class2_blocker_conditionally_closed": True,
        "set_equality_after_4": "s == s_1270 UNION covers(4 cost-69i roots)",
    },
    "target": {
        "s5_parent_hex": PARENT1, "s6_child_hex": CHILD, "edge_cost": 69,
        "open_parents": [PARENT1, PARENT2, PARENT3],
        "demand_at_baseline_1270": {"c1": 0, "c2": 2, "c4": 2},
        "child_orbit_closure": "closed by the bit-21 receipt of this fold",
        "candidates": 69, "win7_d10": 4, "refuted_d10": 65, "capped": 0,
        "candidate_nodes": 62994015,
        "remaining_rows_after": {
            "parent1_orbits": len(rows_after["parent1"]),
            "parent1_edge_cost": sum(rows_after["parent1"].values()),
            "parent2_orbits": len(rows_after["parent2"]),
            "parent2_edge_cost": sum(rows_after["parent2"].values()),
            "parent3_orbits": len(rows_after["parent3"]),
            "parent3_edge_cost": sum(rows_after["parent3"].values()),
        },
    },
    "cost69i_addition": addition,
    "totals": {
        "receipts": 4, "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "zero_marginal_in_manifest": [f"bit{b}" for b in zero_mim],
        "child_closed_by_bit": child_closed_by,
        "certificate_rows": sums["rows"],
        "certificate_bytes": sums["bytes"],
        "certificate_sub_roots": sums["sub_roots_total"],
        "v15_crosscheck_nodes_sum": sum(v15_bits[b]["nodes"] for b in WIN_BITS),
        "v16_sweep_win_nodes_sum": sum(r["nodes"] for r in win),
    },
    "frontier_after_cost69i": {
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
        "third_target_s5_closed": third_target_closed,
        "third_target_s5": PARENT1,
        "third_target_s5_status": ("first-player WIN: all six-stone children are "
                                   "WIN (the last row closed by this fold), so the "
                                   "class-2 blocker closes conditionally"),
    },
    "outstanding_not_folded": {
        "cost65l": "folded at the forked head 1261 on a parallel lane; must be "
                   "merged with the 69i chain by this unified fold",
        "cost70g_cost73g_cost73h": "already folded on the 1244-1257 chain",
        "cost69g": "stale claim (head 1163) for this same child; no artifacts",
        "next_fold_baseline": "this chain head (see frontier_after_cost69i) is "
                              "the new canonical baseline for all subsequent "
                              "folds; assert it before extending",
    },
    "interpretation_guard": "bookkeeping over published receipts; solved counts "
                            "measure manifest coverage, not the game-theoretic "
                            "value of any position; REFUTED-D10 sweeps prove "
                            "only absence of WIN7-D10; WIN7 certificates prove "
                            "a win within depth 10 from the individual "
                            "7-stone roots only; the third target S5 has zero "
                            "remaining six-stone children after this fold, which "
                            "makes it a first-player WIN under the standard "
                            "even-OR/odd-AND convention and conditionally closes "
                            "the class-2 blocker; 11x11 empty board / two-stone "
                            "root {49,60} / S2 {59,60} remain UNKNOWN",
}
(OUT / "class-frontier-merged-cost65l-74g-69i-recompute-20261115.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-merged-cost65l-74g-69i-recompute-20261115.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in remF2.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / "class-frontier-s5-ranking-after-merged-cost65l-74g-69i-20261115.csv").open(
        "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits", "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / "class-frontier-top-candidates-s6-after-merged-cost65l-74g-69i-20261115.csv").open(
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
print("written ranking + top-candidates CSVs (after-merged-cost65l-74g-69i)")

# The 69i lane's own claim records the 1266 -> 1273 fold; this unified
# merge is a separate recomputation on the merged 1270 head and does
# not re-assert that claim.
