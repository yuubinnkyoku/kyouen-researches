#!/usr/bin/env python3
"""Class-2 frontier recomputation folding the class2-lane cost-75d WIN7 receipts
(4 WIN7-D10 bits 12, 40, 92, 111 of the second coverable class-2 target S5
00000000000000801202000000200000's cost-75 child
00000000000040801202000000200000, edge cost 75, demand c1=0,c2=1,c4=0,
single open lift parent) on top of the cost-77c receipts chain head
(solved 1290, 2026-11-15).

This fold was deferred by an execution-environment outage after the sweep and
certificate publication (see research/log/2026-11-15-n11-class2-lane-cost75d-
fold-deferral-note.md); all fold inputs were verified on main at deferral time
and are re-verified here against the current canonical head 1290
(cost-77a/77b/77c and cost-78a folds have landed since, so the rebased
baseline is 1290, not the 1280 named in the deferral note).
"""
import csv
import hashlib
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERTS = OUT / "class2-lane-cost75d-certificates"
TMP = OUT / "tmp-cost75d"
CHILD = "00000000000040801202000000200000"
CHILD_V = int(CHILD, 16)
PARENT1 = "00000000000000801202000000200000"
WIN_BITS = [12, 40, 92, 111]
ROOTS = {
    12: "00000000000040801202000000201000",
    40: "00000000000040801202010000200000",
    92: "00000000100040801202000000200000",
    111: "00008000000040801202000000200000",
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


# ---------- 1. reproduce the cost-77c chain head (1290) ----------
ns77 = runpy.run_path(str(HERE / "scripts" / "recompute_frontier_cost77c_receipts_20261115.py"))
s_base = ns77["s_cur"]
st_base = ns77["stF2"]
covers = ns77["covers"]
manifest = ns77["manifest"]
classes = ns77["classes"]
summary_state = ns77["summary_state"]
remG = ns77["remF2"]
demG = ns77["demF2"]
prev = set(ns77["prev"]) | {int(c["root_hex"], 16) for c in ns77["certs"].values()}
assert st_base["solved_s6_in_manifest"] == 1290 and st_base["unique_remaining_s6"] == 6557
assert st_base["sum_remaining_cost"] == 517923
assert st_base["s6_needed_by_open_classes"] == 4827 and st_base["cost_needed_by_open_classes"] == 381646
assert len(prev) == 565, len(prev)  # 553 + 4 cost-77b roots + 8 cost-77c roots
sha, blen = git_blob_sha(OUT / "class-frontier-cost77c-receipts-recompute-20261115.json")
assert sha == "7f2badce7132aa7fdf76c9ee0283bd14a9ac9e7b" and blen == 10558, \
    "regenerated cost-77c head JSON must be byte-identical to main"
sha, blen = git_blob_sha(OUT / "class-frontier-s5-ranking-after-cost77c-receipts-20261115.csv")
assert sha == "9ada5dfc2057d3a340a3c27a8e984498c17118ad" and blen == 7539
sha, blen = git_blob_sha(OUT / "class-frontier-top-candidates-s6-after-cost77c-receipts-20261115.csv")
assert sha == "8d5583e03e490042898be459d06e03b4aa2b5c13" and blen == 7589
print("CONTROL cost-77c chain head reproduced byte-identically: "
      "1290/6557/517923/4827/381646 (head JSON + both CSVs blob == main)")

# ---------- 2. claim + child remaining at the 1290 baseline ----------
claim_path = OUT / "class2-lane-cost75d-inflight-20261115.json"
claim = json.loads(claim_path.read_text())
assert claim["s6_child"] == CHILD and claim["s6_s7_edge_cost"] == 75
assert claim["demand"] == {"c1": 0, "c2": 1, "c4": 0}
assert claim["candidate_count"] == 75 and len(claim["legal_candidates"]) == 75
assert claim["s5_parent1"] == PARENT1 and claim["s5_parent2"] is None
assert CHILD_V in manifest and CHILD_V not in s_base
rows_p1 = remG.get(PARENT1, [])
parents = {"parent1": {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rows_p1}}
assert CHILD in parents["parent1"], "the child row must still be held by the second target S5"
assert (len(parents["parent1"]), sum(parents["parent1"].values())) == (13, 1018)
d = demG[CHILD]
assert (d["c1"], d["c2"], d["c4"]) == (0, 1, 0), d
canon = ns77["canon"]
stones = [i for i in range(121) if (CHILD_V >> i) & 1]
assert stones == [21, 49, 57, 60, 71, 78], stones
del_orbits = {s: canon(CHILD_V & ~(1 << s)) for s in stones}
assert len(set(del_orbits.values())) == 6
lifts = {s: f"{o:032x}" for s, o in del_orbits.items() if f"{o:032x}" == PARENT1}
assert lifts == {78: PARENT1}, lifts
for s, o in del_orbits.items():
    if s != 78:
        assert f"{o:032x}" not in remG, (s, f"{o:032x}", "claimed closed at head 1277, must stay closed")
print(f"CONTROL child genuinely remaining at head 1290: single open lift parent "
      f"holds the child row (13/1018), demand c1=0,c2=1,c4=0, lift stone 78; "
      f"the other five deletion orbits stay closed")

# ---------- 3. re-derive the sweep from the raw batches ----------
records = []
pilots = []
for i in range(1, 11):
    lines = [json.loads(x) for x in
             (OUT / f"class2-lane-cost75d-raw-batch{i}-20261115.jsonl").read_text().splitlines() if x]
    assert lines[0]["control"] == "pilot_d6" and lines[0]["loss"] is False and lines[0]["nodes"] == 3402
    pilots.append(lines[0]["nodes"])
    records.extend(lines[1:])
assert len(records) == 75
bits = [r["bit"] for r in records]
assert bits == claim["legal_candidates"], "raw candidate bits must equal the claim enumeration"
win = [r for r in records if r["loss"]]
ref = [r for r in records if not r["loss"]]
assert [r["bit"] for r in win] == [12, 40, 92, 111]
assert len(ref) == 71 and not any(r["capped"] for r in records)
assert sum(r["nodes"] for r in records) == 143552593
for r in records:
    assert r["terminalStoneRange"][0] >= 13 and r["terminalStoneRange"][1] <= 17
    assert r["andclose"] is True
    root_v = CHILD_V | (1 << r["bit"])
    assert r["root"] == f"{root_v:032x}" if "root" in r else True
assert all(p == 3402 for p in pilots)
det = [json.loads(x) for x in (OUT / "class2-lane-cost75d-v16-determinism-rerun-20261115.jsonl").read_text().splitlines() if x]
assert det[0]["control"] == "pilot_d6" and det[0]["nodes"] == 3402
det_by_bit = {r["bit"]: r for r in det[1:]}
for b, rec in det_by_bit.items():
    raw = next(r for r in records if r["bit"] == b)
    assert rec["nodes"] == raw["nodes"] and rec["loss"] == raw["loss"]
v15 = json.loads((OUT / "class2-lane-cost75d-v15-crosscheck-pinned-record-20261115.json").read_text())
assert v15["child"] == CHILD and v15["edge_cost"] == 75
assert len(v15["pilots"]) == 3 and all(p["control"] == "pilot_d6" and p["loss"] is False
                                      and p["nodes"] == 5949 for p in v15["pilots"])
v15_bits = {r["bit"]: r for r in v15["win_records"]}
assert set(v15_bits) == set(WIN_BITS)
V15_WIN_NODES = {12: 1406438, 40: 7087163, 92: 16644786, 111: 10234430}
for b in WIN_BITS:
    assert v15_bits[b]["loss"] is True and v15_bits[b]["nodes"] == V15_WIN_NODES[b]
v15_anchor_bits = {r["bit"]: r for r in v15["refuted_anchor_records"]}
assert set(v15_anchor_bits) == {0, 2, 4, 6, 86}
assert all(r["loss"] is False for r in v15["refuted_anchor_records"])
print("CONTROL sweep re-derived from 10 raw batches: 75 candidates exactly "
      "once, 4 WIN7-D10 / 71 REFUTED-D10 / 0 capped, 143,552,593 nodes, "
      "pilots 3402 x10, determinism rerun node-exact, v15 pinned record "
      "4/4 WIN + 5/5 refuted anchors, pilots 5949 x3")

# ---------- 4. certificates ----------
moves_all = json.loads((TMP / "legal-moves.json").read_text())
certs = {}
sums = {"rows": 0, "bytes": 0, "sub_roots_total": 0}
for bit in WIN_BITS:
    root = ROOTS[bit]
    receipt = json.loads((TMP / f"bit{bit}.cert-receipt.json").read_text())
    parts = sorted(CERTS.glob(f"bit{bit}-root-{root}.cert.part*"))
    if parts:
        part_bytes = [p.read_bytes() for p in parts]
        whole = b"".join(pb.replace(b"\r\n", b"\n") for pb in part_bytes)
        sm = json.loads((TMP / f"bit{bit}.cert.split.json").read_text())
        assert sm["whole_bytes"] == receipt["bytes"] and sm["whole_md5"] == receipt["md5"]
        assert sm["whole_git_blob_sha"] == receipt["git_blob_sha"]
        assert len(sm["parts"]) == len(part_bytes)
        for pb, pm in zip(part_bytes, sm["parts"]):
            assert len(pb) == pm["bytes"], (bit, pm)
    else:
        whole = (CERTS / f"bit{bit}-root-{root}.cert").read_bytes()
        sm = None
    assert len(whole) == receipt["bytes"], (bit, len(whole), receipt["bytes"])
    assert hashlib.md5(whole).hexdigest() == receipt["md5"], bit
    assert whole.startswith(b"n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS\n")
    assert whole.splitlines()[1] == b"root " + root.encode()
    rows = whole.splitlines()[2:]
    bj = json.loads((TMP / f"bit{bit}.bigint.json").read_text())
    ts = json.loads((TMP / f"bit{bit}.tsverify.json").read_text().splitlines()[-1])
    cparts = sorted(TMP.glob(f"bit{bit}.consumed.txt.part*"))
    if cparts:
        consumed = [x for x in b"".join(p.read_bytes() for p in cparts).decode().split() if x]
        csm = json.loads((TMP / f"bit{bit}.consumed.split.json").read_text())
        assert csm["whole_bytes"] == len(b"".join(p.read_bytes() for p in cparts))
    else:
        consumed = [x for x in (TMP / f"bit{bit}.consumed.txt").read_text().split() if x]
        csm = None
    moves = moves_all[str(bit)]["moves"]
    assert moves_all[str(bit)]["root"] == root
    assert bj["root_hex"] == root and bj["strategy_rows"] == len(rows)
    assert bj["union_missing"] == 0 and bj["union_extra"] == 0
    assert bj["subroots_passed"] == len(moves)
    assert bj["terminal_range"] == [13, 17]
    assert ts["root_hex"] == root and ts["strategy_rows"] == len(rows)
    assert ts["subroots_passed"] == len(moves) and ts["terminal_stone_range"] == [13, 15, 17]
    assert ts["union_missing"] == 0 and ts["union_extra"] == 0
    assert ts["consumed_rows"] == len(consumed) and len(set(consumed)) == len(rows)
    assert rows == sorted(set(rows)), bit
    certs[str(bit)] = {
        "bit": bit, "root_hex": root,
        "d4_canonical_hex": f"{canon(int(root, 16)):032x}",
        "rows": len(rows), "bytes": len(whole),
        "md5": receipt["md5"], "sha256": receipt["sha256"],
        "whole_git_blob_sha": git_blob_sha_bytes(whole),
        "sub_roots_total": len(moves),
        "loser_first_moves": moves,
        "bigint_verifier": {"union_missing": 0, "union_extra": 0,
                            "subroots_passed": bj["subroots_passed"],
                            "terminal_range": bj["terminal_range"]},
        "ts_verifier": {"union_missing": 0, "union_extra": 0,
                        "subroots_passed": ts["subroots_passed"],
                        "consumed_distinct": len(set(consumed))},
        "v15_anchor_nodes": V15_WIN_NODES[bit],
    }
    sums["rows"] += len(rows)
    sums["bytes"] += len(whole)
    sums["sub_roots_total"] += len(moves)
assert sums["rows"] == 239868
assert sums["bytes"] == 8654219
assert sums["sub_roots_total"] == 242
print("CONTROL 4 published certificates asserted against joined LF bytes: "
      "239,868 rows / 8,654,219 bytes / 242 sub-roots; BigInt + Number "
      "Bareiss 4/4 PASS (union 0/0), split manifests join == whole")

# ---------- 5. root disjointness ----------
new_roots = {int(certs[str(b)]["root_hex"], 16) for b in WIN_BITS}
assert not (new_roots & prev)
prev_d4 = {f"{canon(r):032x}" for r in prev}
assert not ({certs[str(b)]["d4_canonical_hex"] for b in WIN_BITS} & prev_d4)
assert len({certs[str(b)]["d4_canonical_hex"] for b in WIN_BITS}) == 4
print("CONTROL root disjointness: 4 new roots vs 565 folded roots, raw-hex "
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
assert child_closed_by == 12, "the child orbit must be closed by the first receipt"
cov4 = set()
for bit in WIN_BITS:
    cov4 |= covers(int(certs[str(bit)]["root_hex"], 16))
assert s_cur == set(s_base) | cov4, "set-equality: s_after == s_1290 UNION covers(4 roots)"
total_mim = sum(a["marginal_in_manifest"] for a in addition)
total_marg = sum(a["marginal"] for a in addition)
stF2, remF2, uniqF2, demF2 = summary_state(s_cur)
assert stF2["solved_s6_in_manifest"] == 1290 + total_mim
assert s_cur >= s0
assert CHILD_V in s_cur and CHILD_V in manifest
rows_after_p1 = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in remF2.get(PARENT1, [])}
assert CHILD not in rows_after_p1
lost_p1 = set(parents["parent1"]) - set(rows_after_p1)
assert CHILD in lost_p1
assert lost_p1 <= {f"{k:032x}" for k in cov4}, sorted(lost_p1)
print("AFTER cost-75d receipts:", json.dumps(stF2, indent=1))
print(f"total marginal={total_marg} marginal_in_manifest={total_mim}; "
      f"zero-mim receipts: {zero_mim or 'none'}; child orbit closed by bit{child_closed_by}; "
      f"parent1 (second target) {len(rows_after_p1)} rows / {sum(rows_after_p1.values())} "
      f"(was 13/1018, lost {sorted(lost_p1)})")

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
    "schema": "n11-class-frontier-cost75d-receipts-recompute-20261115-v1",
    "date": "2026-11-15",
    "baseline_main": "class-frontier-cost77c-receipts-recompute-20261115.json "
                     "(cost-77c chain head 1290/6557/517923/4827/381646; "
                     "regenerated byte-identical, git blob sha "
                     "7f2badce7132aa7fdf76c9ee0283bd14a9ac9e7b); this fold was "
                     "deferred at head 1280 by the execution-environment outage "
                     "and is executed here rebased to the canonical head 1290 "
                     "per the deferral note's rebase clause",
    "method": "runpy reproduction of the cost-77c chain head (asserting "
              "1290/6557/517923/4827/381646 and the blob-identical 77c head "
              "JSON and both 77c CSVs), the cost-75d child asserted genuinely "
              "remaining at the 1290 baseline (single open lift parent: second "
              "target S5 00000000000000801202000000200000 at 13 rows / 1018; "
              "demand c1=0,c2=1,c4=0 re-derived, lift stone 78; the other five "
              "deletion orbits stay closed), the sweep re-derived from the "
              "ten raw batch JSONLs (75 candidates exactly once, 4 WIN7-D10 / "
              "71 REFUTED-D10 / 0 capped / 143,552,593 nodes, roots == child | "
              "1<<bit, 4 distinct D4 orbits, pilots 3402 x10, determinism rerun "
              "node-exact), the v15 cross-engine pinned record asserted (4 WIN "
              "loss=true nodes 1,406,438/7,087,163/16,644,786/10,234,430, 5 "
              "refuted anchors bits 0/2/4/6/86 loss=false, pilots 5949 x3), all "
              "4 published certificates asserted against the joined LF bytes "
              "(md5/bytes/sha256 from the extraction receipts and split "
              "manifests joining to the whole, rows sorted-unique, sub-roots "
              "== loser mobility, terminal 13..17, BigInt and Number Bareiss "
              "verifier PASS / union 0/0, consumed dumps distinct == rows), "
              "the 4 roots asserted disjoint from the 565 folded receipt roots "
              "both raw-hex and D4-canonically, then the 4 receipts folded in "
              "publication order [12, 40, 92, 111]; the child-orbit closure "
              "(bit12) and a set-equality control hold",
    "controls": {
        "chain_head_1290_reproduced_byte_identical": True,
        "child_genuinely_remaining_at_baseline": True,
        "single_open_lift_parent_held_child_row_at_baseline": True,
        "five_other_deletion_orbits_stay_closed": True,
        "sweep_rederived_from_raw_batches": True,
        "determinism_rerun_node_exact": True,
        "v15_pinned_record_anchors_verified": True,
        "certificates_bytes_md5_verified": True,
        "split_manifests_join_equals_whole": True,
        "root_disjointness_vs_565_roots": True,
        "child_orbit_closure": "closed by the bit-12 receipt (first in publication order), of this fold",
        "set_equality_after_4": "s == s_1290 UNION covers(4 cost-75d roots)",
    },
    "target": {
        "s5_parent_hex": PARENT1, "s6_child_hex": CHILD, "edge_cost": 75,
        "open_parents": [PARENT1],
        "demand_at_baseline_1290": {"c1": 0, "c2": 1, "c4": 0},
        "child_orbit_closure": "closed by the bit-12 receipt of this fold",
        "candidates": 75, "win7_d10": 4, "refuted_d10": 71, "capped": 0,
        "candidate_nodes": 143552593,
        "remaining_rows_after": {
            "parent1_orbits": len(rows_after_p1),
            "parent1_edge_cost": sum(rows_after_p1.values()),
        },
    },
    "cost75d_addition": addition,
    "totals": {
        "receipts": 4, "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "zero_marginal_in_manifest": [f"bit{b}" for b in zero_mim],
        "child_closed_by_bit": child_closed_by,
        "certificate_rows": sums["rows"],
        "certificate_bytes": sums["bytes"],
        "certificate_sub_roots": sums["sub_roots_total"],
        "v15_crosscheck_nodes_sum": sum(V15_WIN_NODES[b] for b in WIN_BITS),
        "v16_sweep_win_nodes_sum": sum(r["nodes"] for r in win),
    },
    "frontier_after_cost75d": {
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
        "cost77d": "second target cost-77 row 00000000100000801202000000200000; "
                   "sweep claimed in-flight on a parallel lane (claim "
                   "class2-lane-cost77d-inflight-20261115.json, claimed at head "
                   "1290); IMPORTANT: the bit-92 receipt of this 75d fold "
                   "cross-covers and already closes that 77d child row at the "
                   "new head 1296, so the parallel 77d fold must follow the "
                   "warm-hygiene pattern (child already closed at its fold "
                   "baseline; per-receipt marginals re-derived from the "
                   "extended union, cost-70g precedent)",
        "next_fold_baseline": "this chain head (see frontier_after_cost75d) is "
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
(OUT / "class-frontier-cost75d-receipts-recompute-20261115.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-cost75d-receipts-recompute-20261115.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in remF2.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / "class-frontier-s5-ranking-after-cost75d-receipts-20261115.csv").open(
        "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits", "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / "class-frontier-top-candidates-s6-after-cost75d-receipts-20261115.csv").open(
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
print("written ranking + top-candidates CSVs (after-cost75d-receipts)")

# ---------- 8. completed-claim control ----------
claim = json.loads(claim_path.read_text())
if claim.get("status", "").startswith("completed") and "fold" in claim:
    f = claim["fold"]
    head_str = (f"{stF2['solved_s6_in_manifest']}/{stF2['unique_remaining_s6']}/"
                f"{stF2['sum_remaining_cost']}/{stF2['s6_needed_by_open_classes']}/"
                f"{stF2['cost_needed_by_open_classes']}")
    assert f["chain_head_before"] == "1290/6557/517923/4827/381646"
    assert f["chain_head_after"] == head_str
    assert f["total_marginal"] == total_marg
    assert f["total_marginal_in_manifest"] == total_mim
    assert f["child_orbit_closed_by_bit"] == child_closed_by
    assert f["parents_after"]["parent1"] == f"{len(rows_after_p1)} rows / {sum(rows_after_p1.values())}"
    assert f["parents_lost_rows"]["parent1"] == sorted(lost_p1)
    obs = f["output_blob_shas"]
    sha_out, blen_out = git_blob_sha(OUT / "class-frontier-cost75d-receipts-recompute-20261115.json")
    assert sha_out == obs["head_json"] and blen_out == f["head_json_bytes"]
    sha_out, blen_out = git_blob_sha(OUT / "class-frontier-s5-ranking-after-cost75d-receipts-20261115.csv")
    assert sha_out == obs["ranking_csv"] and blen_out == f["ranking_csv_bytes"]
    sha_out, blen_out = git_blob_sha(OUT / "class-frontier-top-candidates-s6-after-cost75d-receipts-20261115.csv")
    assert sha_out == obs["top_candidates_csv"] and blen_out == f["top_candidates_csv_bytes"]
    print("CONTROL completed claim fold record matches this recomputation: head "
          + head_str + ", three output blobs re-asserted byte-identical")
