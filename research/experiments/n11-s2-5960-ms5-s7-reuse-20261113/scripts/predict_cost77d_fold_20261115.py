#!/usr/bin/env python3
"""Independent pre-fold prediction brief for the in-flight cost-77d receipts fold.

Reads only published main bytes: the chain of published fold scripts (through the
cost-75d receipts fold, canonical head 1296/6551/517468/4821/381191) is reproduced
by runpy, the in-flight cost-77d claim and the ten published raw batch JSONLs give
the swept candidate list and WIN/REFUTED verdicts. No fold is performed here and
no manifest state is mutated: this file predicts, from the geometry of the 12
published WIN7-D10 candidate roots, exactly which S6 orbits the parallel lane's
forthcoming fold should mark solved, which rows the two open parents should lose,
and which head numbers the fold should print. The parallel lane's fold script and
claim remain the authority; this prediction is a cross-check table for them and for
the fold's second verification.

Interpretation guard: solved counts measure manifest coverage, not game-theoretic
values. The raw batch WIN records are in-flight sweep output, not certificates;
the prediction below assumes the 12 WIN candidates extract into verified WIN7
certificates. REFUTED-D10 proves only absence of a WIN7-D10 certificate. The
11x11 empty board, both two-stone roots, S2 {49,60}, class 1, class 2 and class 4
all remain UNKNOWN.
"""
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"

WIN_BITS_EXPECTED = [7, 12, 39, 58, 62, 64, 66, 78, 94, 96, 108, 111]

# ---------- 1. reproduce the canonical head 1296 via the published chain ----------
ns75 = runpy.run_path(str(HERE / "scripts" / "recompute_frontier_cost75d_receipts_20261115.py"))
s_1296 = ns75["s_cur"]
st_1296 = ns75["stF2"]
manifest = ns75["manifest"]
classes = ns75["classes"]
canon = ns75["canon"]
covers = ns75["covers"]
summary_state = ns75["summary_state"]
prev_roots = ns75["prev"] | {int(c["root_hex"], 16) for c in ns75["certs"].values()}
rem_1296 = ns75["remF2"]
dem_1296 = ns75["demF2"]
assert (st_1296["solved_s6_in_manifest"], st_1296["unique_remaining_s6"],
        st_1296["sum_remaining_cost"], st_1296["s6_needed_by_open_classes"],
        st_1296["cost_needed_by_open_classes"]) == (1296, 6551, 517468, 4821, 381191)
assert len(prev_roots) == 569, len(prev_roots)  # 565 through 77c + 4 cost-75d roots
print("CONTROL canonical head 1296 reproduced: 1296/6551/517468/4821/381191, prev roots", len(prev_roots))

# ---------- 2. the in-flight 77d claim and the published raw batches ----------
claim = json.loads((OUT / "class2-lane-cost77d-inflight-20261115.json").read_text())
assert claim["status"] == "in-flight"
assert claim["candidate_count"] == 77 and len(claim["legal_candidates"]) == 77
CHILD = int(claim["s6_child"], 16)
assert CHILD == int("00000000100000801202000000200000", 16)
PARENT_A = int("00000000000000003800400008000000", 16)  # del-21 open parent at claim time
PARENT_B = int("00000000000000801202000000200000", 16)  # second coverable class-2 target S5
assert claim["s6_s7_edge_cost"] == 77

# child orbit (D4-canonical hex) and its status at the 1296 baseline
child_orbit = canon(CHILD)
child_hex = f"{child_orbit:032x}"
print("CONTROL 77d child orbit", child_hex, "in s_1296 (warm-hygiene precondition):", child_orbit in s_1296)
assert child_orbit in s_1296, "the 77d child row must already be closed at head 1296 (75d bit-92 cross-cover)"

# two open parents of the child: re-derive the deletion structure at head 1296
stones = [i for i in range(121) if (CHILD >> i) & 1]
assert stones == [21, 49, 57, 60, 71, 92], stones
del_orbits = {s: canon(CHILD & ~(1 << s)) for s in stones}
open_dels = {s: f"{o:032x}" for s, o in del_orbits.items() if f"{o:032x}" in rem_1296}
print("CONTROL deletion-orbit parents still open at head 1296:", open_dels)

# ---------- 3. re-derive the sweep verdicts from the ten published raw batches ----------
import glob
recs = {}
pilots = 0
total_nodes = 0
batch_files = sorted(glob.glob(str(OUT / "class2-lane-cost77d-raw-batch*-20261115.jsonl")))
for path in batch_files:
    for line in Path(path).read_text().splitlines():
        r = json.loads(line)
        if "control" in r:
            pilots += 1
            assert r["control"] == "pilot_d6" and r["loss"] is False and r["nodes"] == 3402
            continue
        bit = r["bit"]
        assert bit not in recs, ("duplicate candidate", bit)
        assert bit in claim["legal_candidates"], ("bit not in claim list", bit)
        recs[bit] = r
        total_nodes += r["nodes"]
assert len(recs) == 77 and len(set(claim["legal_candidates"])) == 77
assert set(recs) == set(claim["legal_candidates"])
assert pilots == 10
win_bits = sorted(b for b, r in recs.items() if r["loss"])
refuted = sorted(b for b, r in recs.items() if not r["loss"] and not r["capped"])
capped = sorted(b for b, r in recs.items() if r["capped"])
assert win_bits == WIN_BITS_EXPECTED, win_bits
assert capped == []
print(f"CONTROL sweep re-derived from 10 raw batches: 77 candidates, 12 WIN {win_bits}, "
      f"{len(refuted)} REFUTED, 0 capped, nodes {total_nodes:,}, pilots 3402 x10")

# ---------- 4. predicted receipts: the 12 WIN roots and their coverage geometry ----------
pred_roots = []
seen_orbits = set()
duplicate_prev_bits = []
for bit in win_bits:
    root = CHILD | (1 << bit)
    if root in prev_roots:
        duplicate_prev_bits.append(bit)
        continue
    if root in seen_orbits:
        raise AssertionError("duplicate raw root")
    seen_orbits.add(root)
    d4 = canon(root)
    pred_roots.append({"bit": bit, "root_hex": f"{root:032x}",
                       "d4_canonical_hex": f"{d4:032x}",
                       "raw_disjoint_from_prev_569": True})
assert len({r["d4_canonical_hex"] for r in pred_roots}) == len(pred_roots), "distinct D4 orbits among the new roots"
d4_prev = {canon(p) for p in prev_roots}
assert not ({canon(int(r["root_hex"], 16)) for r in pred_roots} & d4_prev), "D4 disjointness vs prev"
print(f"CONTROL predicted roots: {len(pred_roots)} mutually distinct raw and D4, disjoint from the 569 folded roots")
if duplicate_prev_bits:
    for bit in duplicate_prev_bits:
        root = CHILD | (1 << bit)
        d4_hit = canon(root) in d4_prev
        print(f"NOTE bit {bit} root {root:032x} is a RAW and D4 duplicate of an already-folded root "
              f"(d4_hit={d4_hit}); predicted marginal must be 0")
    print(f"PREDICT {len(duplicate_prev_bits)} WIN candidate root(s) {duplicate_prev_bits} duplicate "
          f"already-folded roots: their receipts add zero marginal and must not be counted as new roots")

per_bit = []
union_covers = set()
for bit in win_bits:
    root = CHILD | (1 << bit)
    cov = covers(root)
    assert len(cov) == 7, (bit, len(cov))  # 7-stone root, 7 deletion orbits
    marg = cov - s_1296
    union_covers |= cov
    per_bit.append({
        "bit": bit,
        "root_hex": f"{root:032x}",
        "already_folded_root_duplicate": bit in duplicate_prev_bits,
        "covers_7": True,
        "covered_already_solved_1296": len(cov) - len(marg),
        "predicted_marginal": len(marg),
        "predicted_marginal_in_manifest": len(marg & manifest),
        "predicted_marginal_hexes": sorted(f"{m:032x}" for m in marg),
    })
    if bit in duplicate_prev_bits:
        assert not marg, (bit, "an already-folded root's covers must be fully solved at head 1296")
total_marg = sum(p["predicted_marginal"] for p in per_bit)
union_marg = union_covers - s_1296
assert {f"{m:032x}" for m in union_marg} == set().union(*[set(p["predicted_marginal_hexes"]) for p in per_bit], set())
assert len(union_marg) <= total_marg
mim = len(union_marg & manifest)
print(f"PREDICT total per-receipt marginal {total_marg}, union marginal {len(union_marg)}, "
      f"union in-manifest {mim}")

# ---------- 5. predicted post-fold head and parent row effects ----------
s_pred = s_1296 | union_covers
st_pred, rem_pred, uniq_pred, dem_pred = summary_state(s_pred)
print("PREDICT post-77d head:",
      f"{st_pred['solved_s6_in_manifest']}/{st_pred['unique_remaining_s6']}/"
      f"{st_pred['sum_remaining_cost']}/{st_pred['s6_needed_by_open_classes']}/"
      f"{st_pred['cost_needed_by_open_classes']}")
assert st_pred["solved_s6_in_manifest"] == 1296 + mim

rows_pa = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1296.get(f"{PARENT_A:032x}", [])}
rows_pb = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1296.get(f"{PARENT_B:032x}", [])}
pa_hex, pb_hex = f"{PARENT_A:032x}", f"{PARENT_B:032x}"
print(f"CONTROL at head 1296: parent-A {pa_hex} {len(rows_pa)} rows / {sum(rows_pa.values())}; "
      f"parent-B (second target) {pb_hex} {len(rows_pb)} rows / {sum(rows_pb.values())}")
lost_pa = sorted(set(rows_pa) & {f"{m:032x}" for m in union_marg})
lost_pb = sorted(set(rows_pb) & {f"{m:032x}" for m in union_marg})
print(f"PREDICT parent-A loses {len(lost_pa)} of {len(rows_pa)} rows: {lost_pa}")
print(f"PREDICT parent-B (second target S5) loses {len(lost_pb)} of {len(rows_pb)} rows: {lost_pb}")

# frontier-wide: all S5 parents that lose rows under the predicted fold
all_lost_by_parent = {}
for s5_hex, rows in rem_1296.items():
    lost = sorted(set(r["s6_hex"] for r in rows) & {f"{m:032x}" for m in union_marg})
    if lost:
        all_lost_by_parent[s5_hex] = lost
print("PREDICT parents losing rows:", {k: len(v) for k, v in sorted(all_lost_by_parent.items())})

# ---------- 6. the second target S5's remaining rows after the predicted fold ----------
st_pred2 = st_pred  # same call, same state
rows_pb_after = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_pred.get(pb_hex, [])}
print(f"PREDICT second target S5 after 77d: {len(rows_pb_after)} rows / {sum(rows_pb_after.values())}")
next_rows = sorted(rows_pb_after.items(), key=lambda kv: kv[1])
print("PREDICT remaining rows by cost:", next_rows)

# ---------- 7. write the machine-readable prediction brief ----------
brief = {
    "schema": "n11-class2-lane-cost77d-fold-prediction-20261115-v1",
    "date": "2026-11-15",
    "session": "long-lane session after the cost-75d fold second verification; planning brief only",
    "status": "prediction for the in-flight parallel cost-77d receipts fold; NOT a fold, NOT a claim, NOT a certificate",
    "baseline": "canonical head 1296/6551/517468/4821/381191 (cost-75d receipts fold; reproduced via the published runpy chain)",
    "sweep_inputs": "published in-flight claim class2-lane-cost77d-inflight-20261115.json (77 candidates) and the ten published raw batch JSONLs (77 records + 10 pilot controls, 152,577,045 nodes, 0 capped)",
    "predicted_win_bits": win_bits,
    "predicted_refuted_bits": refuted,
    "child": {
        "s6_hex": f"{CHILD:032x}",
        "d4_orbit_hex": child_hex,
        "edge_cost": 77,
        "status_at_baseline_1296": "already closed in s_1296 by the cost-75d bit-92 cross-cover (warm-hygiene precondition); in manifest",
        "open_deletion_parents_at_1296": open_dels,
    },
    "predicted_receipts": per_bit,
    "predicted_totals": {
        "sum_per_receipt_marginal": total_marg,
        "union_marginal": len(union_marg),
        "union_marginal_in_manifest": mim,
        "zero_mim_receipts": [p["bit"] for p in per_bit if p["predicted_marginal_in_manifest"] == 0],
    },
    "predicted_head_after_fold": {
        "solved_s6_in_manifest": st_pred["solved_s6_in_manifest"],
        "unique_remaining_s6": st_pred["unique_remaining_s6"],
        "sum_remaining_cost": st_pred["sum_remaining_cost"],
        "s6_needed_by_open_classes": st_pred["s6_needed_by_open_classes"],
        "cost_needed_by_open_classes": st_pred["cost_needed_by_open_classes"],
    },
    "predicted_parent_effects": {
        pa_hex: {"rows_before": len(rows_pa), "cost_before": sum(rows_pa.values()),
                 "lost_rows": lost_pa,
                 "rows_after": len(rows_pa) - len(lost_pa)},
        pb_hex: {"rows_before": len(rows_pb), "cost_before": sum(rows_pb.values()),
                 "lost_rows": lost_pb,
                 "rows_after": len(rows_pb) - len(lost_pb)},
    },
    "predicted_all_parents_losing_rows": {k: len(v) for k, v in sorted(all_lost_by_parent.items())},
    "second_target_after_predicted_fold": {
        "rows": len(rows_pb_after),
        "cost": sum(rows_pb_after.values()),
        "rows_by_cost": next_rows,
    },
    "caveats": [
        "the 12 WIN records are raw in-flight sweep output, not certificates; the fold's receipts exist only after the parallel lane extracts and publishes verifiable WIN7 certificates, and any determinism rerun or cross-engine discrepancy could revise the WIN list",
        "this prediction is geometry-only: covers(root) = the D4-canonical S6 deletion orbits of each 7-stone root; it assumes every WIN candidate extracts into a verified certificate",
        "the parallel lane's fold script and completed claim remain the authority; a mismatch between the fold and this table is an experiment fact to record, not a reason to force either",
    ],
    "interpretation_guard": "solved counts measure manifest coverage, not game-theoretic values; REFUTED-D10 is not a LOSS proof; WIN7 certificates prove a first-player win within depth 10 from the individual 7-stone roots only; 11x11 empty board / two-stone root {49,60} / S2 {59,60} / class 1 / class 2 / class 4 all remain UNKNOWN",
}
out_path = OUT / "class2-lane-cost77d-fold-prediction-20261115.json"
out_path.write_text(json.dumps(brief, indent=1, sort_keys=True) + "\n")
import hashlib
data = out_path.read_bytes()
print("WROTE", out_path.name, len(data), "bytes, md5", hashlib.md5(data).hexdigest())
