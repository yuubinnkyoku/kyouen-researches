#!/usr/bin/env python3
"""Class-2 frontier recomputation folding the class2-lane cost-77a WIN7 receipts
(3 WIN7-D10 bits 40, 64, 111 of the second coverable class-2 target S5
00000000000000801202000000200000's cost-77 child
00000000000000801202000000204000, edge cost 77, demand c1=0,c2=2,c4=0) on top
of the cost-76b receipts chain head (solved 1280, 2026-11-15).
"""
import csv
import hashlib
import itertools
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERTS = OUT / "class2-lane-cost77a-certificates"
TMP = OUT / "tmp-cost77a"
CHILD = "00000000000000801202000000204000"
CHILD_V = int(CHILD, 16)
PARENT1 = "00000000000000801202000000200000"
PARENT2 = "00000000000000003800000408000000"
WIN_BITS = [40, 64, 111]
ROOTS = {
    40: "00000000000000801202010000204000",
    64: "00000000000000811202000000204000",
    111: "00008000000000801202000000204000",
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


# ---------- 1. reproduce the cost-76b chain head (1280) ----------
ns76 = runpy.run_path(str(HERE / "scripts" / "recompute_frontier_cost76b_receipts_20261115.py"))
s_base = ns76["s_cur"]
st_base = ns76["stF2"]
covers = ns76["covers"]
manifest = ns76["manifest"]
classes = ns76["classes"]
summary_state = ns76["summary_state"]
remG = ns76["remF2"]
demG = ns76["demF2"]
prev = set(ns76["prev"]) | {int(c["root_hex"], 16) for c in ns76["certs"].values()}
assert st_base["solved_s6_in_manifest"] == 1280 and st_base["unique_remaining_s6"] == 6567
assert st_base["sum_remaining_cost"] == 518678
assert st_base["s6_needed_by_open_classes"] == 4837 and st_base["cost_needed_by_open_classes"] == 382401
assert len(prev) == 550, len(prev)  # 548 + 2 cost-76b roots
sha, blen = git_blob_sha(OUT / "class-frontier-cost76b-receipts-recompute-20261115.json")
assert sha == "0c35759729663fd561574fd4c5c8ccf2e46550a5" and blen == 6899, \
    "regenerated cost-76b head JSON must be byte-identical to main"
sha, blen = git_blob_sha(OUT / "class-frontier-s5-ranking-after-cost76b-receipts-20261115.csv")
assert sha == "25e4cd0385532c8100b8b4937226294a1e805486" and blen == 7539
sha, blen = git_blob_sha(OUT / "class-frontier-top-candidates-s6-after-cost76b-receipts-20261115.csv")
assert sha == "5f16284cbabf1f68f1119dd4555b0ecc2ab244c7" and blen == 7847
print("CONTROL cost-76b chain head reproduced byte-identically: "
      "1280/6567/518678/4837/382401 (head JSON + both CSVs blob == main)")

# ---------- 2. claim + child remaining at the 1280 baseline ----------
claim_path = OUT / "class2-lane-cost77a-inflight-20261115.json"
claim = json.loads(claim_path.read_text())
assert claim["s6_child"] == CHILD and claim["s6_s7_edge_cost"] == 77
assert claim["demand"] == {"c1": 0, "c2": 2, "c4": 0}
assert claim["candidate_count"] == 77 and len(claim["legal_candidates"]) == 77
assert CHILD_V in manifest and CHILD_V not in s_base
parents = {}
for name, h in (("parent1", PARENT1), ("parent2", PARENT2)):
    rows = remG.get(h, [])
    d = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rows}
    assert CHILD in d, name
    parents[name] = d
assert (len(parents["parent1"]), sum(parents["parent1"].values())) == (16, 1249)
assert (len(parents["parent2"]), sum(parents["parent2"].values())) == (62, 5092)
d = demG[CHILD]
assert (d["c1"], d["c2"], d["c4"]) == (0, 2, 0), d
canon = ns76["canon"]
del_orbits = {s: canon(CHILD_V & ~(1 << s))
              for s in [i for i in range(121) if (CHILD_V >> i) & 1]}
lifts = {name: [s for s, o in del_orbits.items() if f"{o:032x}" == h]
         for name, h in (("parent1", PARENT1), ("parent2", PARENT2))}
assert all(lifts.values()), lifts
assert len(set(del_orbits.values())) == 6
print(f"CONTROL child genuinely remaining at head 1280: two open parents hold "
      f"the child row (16/1249 and 62/5092), demand c1=0,c2=2,c4=0, lift "
      f"stones {lifts}")

# ---------- 3. re-derive the sweep from the raw batches ----------
records = []
pilots = []
for i in range(1, 11):
    lines = [json.loads(x) for x in
             (OUT / f"class2-lane-cost77a-raw-batch{i}-20261115.jsonl").read_text().splitlines() if x]
    assert lines[0]["control"] == "pilot_d6" and lines[0]["loss"] is False and lines[0]["nodes"] == 3402
    pilots.append(lines[0]["nodes"])
    records.extend(lines[1:])
assert len(records) == 77
bits = [r["bit"] for r in records]
assert bits == claim["legal_candidates"], "raw candidate bits must equal the claim enumeration"
win = [r for r in records if r["loss"]]
ref = [r for r in records if not r["loss"]]
assert [r["bit"] for r in win] == WIN_BITS
assert len(ref) == 74 and not any(r["capped"] for r in records)
assert sum(r["nodes"] for r in records) == 103356793
for r in records:
    assert r["terminalStoneRange"][0] >= 13 and r["terminalStoneRange"][1] <= 17
    assert r["andclose"] is True
assert all(p == 3402 for p in pilots)
det = [json.loads(x) for x in (OUT / "class2-lane-cost77a-v16-determinism-rerun-20261115.jsonl").read_text().splitlines() if x]
assert det[0]["control"] == "pilot_d6" and det[0]["nodes"] == 3402
det_by_bit = {r["bit"]: r for r in det[1:]}
for b, rec in det_by_bit.items():
    raw = next(r for r in records if r["bit"] == b)
    assert rec["nodes"] == raw["nodes"] and rec["loss"] == raw["loss"]
v15 = [json.loads(x) for x in (OUT / "class2-lane-cost77a-v15-crosscheck-20261115.jsonl").read_text().splitlines() if x]
v15_pilots = [r for r in v15 if r.get("control") == "pilot_d6"]
assert len(v15_pilots) == 1 and v15_pilots[0]["nodes"] == 5949
v15_bits = {r["bit"]: r for r in v15 if "bit" in r}
for b in WIN_BITS:
    assert b in v15_bits and v15_bits[b]["loss"] is True
for b in (0, 1, 2):
    assert b in v15_bits and v15_bits[b]["loss"] is False
assert set(v15_bits) == set(WIN_BITS) | {0, 1, 2}
print("CONTROL sweep re-derived from 10 raw batches: 77 candidates exactly "
      "once, 3 WIN7-D10 / 74 REFUTED-D10 / 0 capped, 103,356,793 nodes, "
      "pilots 3402 x10, determinism rerun node-exact, v15 3/3 WIN + 3/3 "
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
assert sums["rows"] == 157475
assert sums["bytes"] == 5671984
assert sums["sub_roots_total"] == 182
print("CONTROL 3 published certificates asserted against joined LF bytes: "
      "157,475 rows / 5,671,984 bytes / 182 sub-roots; BigInt + Number "
      "Bareiss 3/3 PASS (union 0/0)")

# ---------- 5. root disjointness ----------
new_roots = {int(certs[str(b)]["root_hex"], 16) for b in WIN_BITS}
assert not (new_roots & prev)
prev_d4 = {f"{canon(r):032x}" for r in prev}
assert not ({certs[str(b)]["d4_canonical_hex"] for b in WIN_BITS} & prev_d4)
assert len({certs[str(b)]["d4_canonical_hex"] for b in WIN_BITS}) == 3
print("CONTROL root disjointness: 3 new roots vs 550 folded roots, raw-hex "
      "and D4-canonically; 3 distinct D4 orbits")

# ---------- 6. fold the 3 receipts ----------
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
assert child_closed_by == 40, "the child orbit must be closed by the first receipt"
cov3 = set()
for bit in WIN_BITS:
    cov3 |= covers(int(certs[str(bit)]["root_hex"], 16))
assert s_cur == set(s_base) | cov3, "set-equality: s_after == s_1280 UNION covers(3 roots)"
total_mim = sum(a["marginal_in_manifest"] for a in addition)
total_marg = sum(a["marginal"] for a in addition)
stF2, remF2, uniqF2, demF2 = summary_state(s_cur)
assert stF2["solved_s6_in_manifest"] == 1280 + total_mim
assert s_cur >= s0
assert CHILD_V in s_cur and CHILD_V in manifest
for name, h in (("parent1", PARENT1), ("parent2", PARENT2)):
    assert CHILD not in {r["s6_hex"] for r in remF2.get(h, [])}, name
rows_after = {}
lost = {}
for name, h in (("parent1", PARENT1), ("parent2", PARENT2)):
    rows_after[name] = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in remF2.get(h, [])}
    lost[name] = set(parents[name]) - set(rows_after[name])
    assert CHILD in lost[name]
    assert lost[name] <= {f"{k:032x}" for k in cov3}, (name, sorted(lost[name]))
print("AFTER cost-77a receipts:", json.dumps(stF2, indent=1))
print(f"total marginal={total_marg} marginal_in_manifest={total_mim}; "
      f"zero-mim receipts: {zero_mim or 'none'}; child orbit closed by bit{child_closed_by}; "
      f"parent1 (second target) {len(rows_after['parent1'])} rows / {sum(rows_after['parent1'].values())} "
      f"(was 16/1249, lost {sorted(lost['parent1'])}); "
      f"parent2 {len(rows_after['parent2'])} rows / {sum(rows_after['parent2'].values())} "
      f"(was 62/5092, lost {sorted(lost['parent2'])})")

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
    "schema": "n11-class-frontier-cost77a-receipts-recompute-20261115-v1",
    "date": "2026-11-15",
    "baseline_main": "class-frontier-cost76b-receipts-recompute-20261115.json "
                     "(cost-76b chain head 1280/6567/518678/4837/382401; "
                     "regenerated byte-identical, git blob sha "
                     "0c35759729663fd561574fd4c5c8ccf2e46550a5)",
    "method": "runpy reproduction of the cost-76b chain head (asserting "
              "1280/6567/518678/4837/382401 and the blob-identical 76b head "
              "JSON and both 76b CSVs), the cost-77a child asserted genuinely "
              "remaining at the 1280 baseline (two open parents: second target "
              "S5 00000000000000801202000000200000 at 16 rows / 1249 and "
              "class-2 S5 00000000000000003800000408000000 at 62 rows / 5092; "
              "demand c1=0,c2=2,c4=0 re-derived), the sweep re-derived from the "
              "ten raw batch JSONLs (77 candidates exactly once, 3 WIN7-D10 / "
              "74 REFUTED-D10 / 0 capped / 103,356,793 nodes, roots == child | "
              "1<<bit, 3 distinct D4 orbits, pilots 3402 x10, determinism rerun "
              "node-exact), the v15 cross-engine anchors asserted (3 WIN "
              "loss=true, refuted anchors bits 0/1/2 loss=false, pilot 5949), "
              "all 3 published certificates asserted against the joined LF "
              "bytes (md5/bytes from the extraction receipts, rows "
              "sorted-unique, sub-roots == loser mobility, terminal 13..17, "
              "BigInt and Number Bareiss verifier PASS / union 0/0), the 3 "
              "roots asserted disjoint from the 550 folded receipt roots both "
              "raw-hex and D4-canonically, then the 3 receipts folded in "
              "publication order [40, 64, 111]; the child-orbit closure "
              "(bit40) and a set-equality control hold",
    "controls": {
        "chain_head_1280_reproduced_byte_identical": True,
        "child_genuinely_remaining_at_baseline": True,
        "two_open_parents_held_child_row_at_baseline": True,
        "sweep_rederived_from_raw_batches": True,
        "determinism_rerun_node_exact": True,
        "v15_cross_engine_anchors_verified": True,
        "certificates_bytes_md5_verified": True,
        "root_disjointness_vs_550_roots": True,
        "child_orbit_closure": "closed by the bit-40 receipt (first in publication order), of this fold",
        "set_equality_after_3": "s == s_1280 UNION covers(3 cost-77a roots)",
    },
    "target": {
        "s5_parent_hex": PARENT1, "s6_child_hex": CHILD, "edge_cost": 77,
        "open_parents": [PARENT1, PARENT2],
        "demand_at_baseline_1280": {"c1": 0, "c2": 2, "c4": 0},
        "child_orbit_closure": "closed by the bit-40 receipt of this fold",
        "candidates": 77, "win7_d10": 3, "refuted_d10": 74, "capped": 0,
        "candidate_nodes": 103356793,
        "remaining_rows_after": {
            "parent1_orbits": len(rows_after["parent1"]),
            "parent1_edge_cost": sum(rows_after["parent1"].values()),
            "parent2_orbits": len(rows_after["parent2"]),
            "parent2_edge_cost": sum(rows_after["parent2"].values()),
        },
    },
    "cost77a_addition": addition,
    "totals": {
        "receipts": 3, "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "zero_marginal_in_manifest": [f"bit{b}" for b in zero_mim],
        "child_closed_by_bit": child_closed_by,
        "certificate_rows": sums["rows"],
        "certificate_bytes": sums["bytes"],
        "certificate_sub_roots": sums["sub_roots_total"],
        "v15_crosscheck_nodes_sum": sum(v15_bits[b]["nodes"] for b in WIN_BITS),
        "v16_sweep_win_nodes_sum": sum(r["nodes"] for r in win),
    },
    "frontier_after_cost77a": {
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
        "cost75d": "second target cost-75 row; 4 certificates published, fold pending on a parallel lane",
        "next_fold_baseline": "this chain head (see frontier_after_cost77a) is "
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
(OUT / "class-frontier-cost77a-receipts-recompute-20261115.json").write_text(
    json.dumps(result, indent=1) + "\n")
print("written class-frontier-cost77a-receipts-recompute-20261115.json")

ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in remF2.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))
with (OUT / "class-frontier-s5-ranking-after-cost77a-receipts-20261115.csv").open(
        "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits", "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))

with (OUT / "class-frontier-top-candidates-s6-after-cost77a-receipts-20261115.csv").open(
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
print("written ranking + top-candidates CSVs (after-cost77a-receipts)")

# ---------- 8. completed-claim control ----------
claim = json.loads(claim_path.read_text())
if claim.get("status", "").startswith("completed") and "fold" in claim:
    f = claim["fold"]
    head_str = (f"{stF2['solved_s6_in_manifest']}/{stF2['unique_remaining_s6']}/"
                f"{stF2['sum_remaining_cost']}/{stF2['s6_needed_by_open_classes']}/"
                f"{stF2['cost_needed_by_open_classes']}")
    assert f["chain_head_before"] == "1280/6567/518678/4837/382401"
    assert f["chain_head_after"] == head_str
    assert f["total_marginal"] == total_marg
    assert f["total_marginal_in_manifest"] == total_mim
    assert f["child_orbit_closed_by_bit"] == child_closed_by
    assert f["parents_after"]["parent1"] == f"{len(rows_after['parent1'])} rows / {sum(rows_after['parent1'].values())}"
    assert f["parents_after"]["parent2"] == f"{len(rows_after['parent2'])} rows / {sum(rows_after['parent2'].values())}"
    obs = f["output_blob_shas"]
    sha_out, blen_out = git_blob_sha(OUT / "class-frontier-cost77a-receipts-recompute-20261115.json")
    assert sha_out == obs["head_json"] and blen_out == f["head_json_bytes"]
    sha_out, blen_out = git_blob_sha(OUT / "class-frontier-s5-ranking-after-cost77a-receipts-20261115.csv")
    assert sha_out == obs["ranking_csv"] and blen_out == f["ranking_csv_bytes"]
    sha_out, blen_out = git_blob_sha(OUT / "class-frontier-top-candidates-s6-after-cost77a-receipts-20261115.csv")
    assert sha_out == obs["top_candidates_csv"] and blen_out == f["top_candidates_csv_bytes"]
    print("CONTROL completed claim fold record matches this recomputation: head "
          + head_str + ", three output blobs re-asserted byte-identical")
