#!/usr/bin/env python3
"""n11 class2-lane pre-sweep census v20 (head 1589, 2026-11-18).

First worklist-wide post-fold census. What changed since census v19
(presweep-1473, 22 verdict maps, 82d/82e revalidation, exhausted
three-family pool):

  * the receipt-harvest global fold
    (class-frontier-receipt-harvest-global-fold-20261118.json) closed 113
    open S6 manifest rows by orbit-level transfer of published WIN7-D10
    receipts, moving the head from 1476 to
    1589/174/6259/495507/4543/360227;
  * per the coordinator correction after the v19 pool exhaustion, this
    census rebuilds the candidate pool from the FULL worklist (all unswept
    rows at head 1589), applying the STERILE-parent exclusion, instead of
    the exhausted three-family pool.

Method: import the global-fold audit module (rebuilds the 79-source harvest
and re-derives the fold with all assertions), then at head 1589:

  1. classify every open S5 parent whose remaining rows are all category
     'sterile' as fully-STERILE and exclude those rows from the pool;
  2. rank the remaining unswept rows by (cost, open bits after harvest
     overlay, hex); note: the overlay counts pre-64h harvest verdicts only;
     post-64h map bits are re-run fresh under the sweep protocol, so the
     open-bit figure is an upper bound for confirmation-bit accounting;
  3. select the next sweep target.

Selection policy refinement (recorded here): the base policy stays
'cheapest cost, then fewest open bits, then hex'. The coordinator's
certificate-candidate concentration rule (lane priority 2) adds a
parent-closure-first override: a sweep that can complete the row set of an
S5 parent takes precedence when it is within reach, because a fully closed
parent is the only mechanism that reduces remaining_s5_orbits (174), and it
extends manifest secured coverage. The global fold left exactly one such
step available: class-2 parent 00000000000000403800000008000000 has one
open row left (00000000000000403800000008000008, cost 78, one open parent,
no engine verdicts, 2 harvest-confirmation bits), so census v20 selects it
despite the cheaper global rows (cheapest eligible is cost 50). If the
sweep finds a WIN bit, the parent becomes the first fully receipt-closed
S5 parent; if all bits are REFUTED, the row is STERILE and the parent is
D10-unclosable - both are definitive structural outcomes.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]          # lane dir
OUT = HERE / "output"
EX = HERE.parent
sys.path.insert(0, str(HERE / "scripts"))
sys.path.insert(0, str(HERE / "scripts"))

import audit_receipt_harvest_global_fold_20261118 as gfold  # noqa: E402
from legal_candidates import legal_candidates  # noqa: E402

canon, stones = gfold.canon, gfold.stones

TARGET = "00000000000000403800000008000008"
TARGET_PARENT = "00000000000000403800000008000000"


def main():
    # 0. re-derive the fold state (all assertions inside)
    harvest, _ns, _w, ref_canons = gfold.rebuild_harvest()
    fold = json.loads((OUT / "class-frontier-receipt-harvest-global-fold-20261118.json").read_bytes())
    assert fold["frontier_after_receipt_harvest_global_fold"] == {
        "solved_s6_in_manifest": 1589, "remaining_s5_orbits": 174,
        "unique_remaining_s6": 6259, "sum_remaining_cost": 495507,
        "s6_needed_by_open_classes": 4543, "cost_needed_by_open_classes": 360227,
    }
    closed = {r["row_hex"] for r in fold["receipts_by_row"]}
    assert len(closed) == 113

    rows1410 = {}
    import csv
    with open(gfold.SRC_WORKLIST) as f:
        for r in csv.DictReader(f):
            rows1410[r["s6_canonical_hex"]] = r
    led = json.loads(gfold.SRC_LEDGER.read_bytes())
    open1476 = {h: v for h, v in rows1410.items() if h not in set(led["derived"]["closed_rows_66"])}
    open1589 = {h: v for h, v in open1476.items() if h not in closed}
    assert len(open1589) == 6259

    k = json.loads(gfold.SRC_CENSUS.read_bytes())
    parents = {p["hex"]: p for p in k["open_s5_census"]}
    parent_set = set(parents)

    # 1. fully-STERILE parents at 1589
    p_rows = defaultdict(list)
    for h, v in open1589.items():
        m = int(h, 16)
        for p in {canon(m ^ (1 << q)) for q in stones(m)} & parent_set:
            p_rows[p].append(h)
    fully_sterile = sorted(p for p, hs in p_rows.items()
                           if all(open1589[h]["category"] == "sterile" for h in hs))
    sterile_row_count = sum(len(p_rows[p]) for p in fully_sterile)
    sterile_cost = sum(int(open1589[h]["own_candidates_s6_s7_edge_cost"]) for p in fully_sterile for h in p_rows[p])
    print(f"[1] fully-STERILE parents at 1589: {len(fully_sterile)} ({sterile_row_count} rows, cost {sterile_cost})")

    # 2. eligible pool
    harvest_win = set(c for c, v in harvest.items() if v["verdict"] == "WIN7-D10")
    harvest_ref = set(ref_canons)
    eligible = []
    for h, v in open1589.items():
        if v["category"] != "unswept":
            continue
        m = int(h, 16)
        ps = sorted({canon(m ^ (1 << q)) for q in stones(m)} & parent_set)
        if ps and set(ps) <= set(fully_sterile):
            continue
        _, bits = legal_candidates(h)
        known_ref = sum(1 for b in bits if canon(m | (1 << b)) in harvest_ref)
        known_win = sum(1 for b in bits if canon(m | (1 << b)) in harvest_win)
        eligible.append({
            "row": h, "cost": int(v["own_candidates_s6_s7_edge_cost"]),
            "legal_bits": len(bits), "harvest_known_refuted": known_ref,
            "harvest_known_win": known_win,
            "open_bits_upper_bound": len(bits) - known_ref - known_win,
            "parents": ps,
        })
    eligible.sort(key=lambda r: (r["cost"], r["open_bits_upper_bound"], r["row"]))
    assert len(eligible) == 6223, len(eligible)
    print(f"[2] eligible unswept rows: {len(eligible)}")

    # 3. target detail
    trow = [r for r in eligible if r["row"] == TARGET]
    assert len(trow) == 1
    trow = trow[0]
    assert trow["parents"] == [TARGET_PARENT], trow["parents"]
    assert trow["harvest_known_win"] == 0
    assert trow["harvest_known_refuted"] == 2
    assert trow["cost"] == 78 and trow["legal_bits"] == 78
    m = int(TARGET, 16)
    _, bits = legal_candidates(TARGET)
    conf_bits = sorted(b for b in bits if canon(m | (1 << b)) in harvest_ref)
    assert conf_bits == [13, 115], conf_bits
    print(f"[3] target {TARGET}: cost {trow['cost']}, {trow['legal_bits']} legal bits, "
          f"{len(conf_bits)} harvest-confirmation bits {conf_bits}, parent {TARGET_PARENT} classes {parents[TARGET_PARENT]['classes']}")

    record = {
        "schema": "n11-class2-lane-next-target-presweep-1589-v20-20261118-v1",
        "date": "2026-11-18",
        "status": "target-selected",
        "basis_head": fold["frontier_after_receipt_harvest_global_fold"],
        "basis_record": "class-frontier-receipt-harvest-global-fold-20261118.json (this script re-derives it via the audit module before ranking)",
        "pool_definition": {
            "base": "all worklist-1410 rows minus fold-chain-ledger closed rows minus the 113 receipt-harvest global-fold rows (head 1589)",
            "excluded": "35 STERILE rows (category=sterile), 1 transfer_partial row (00000000000000801222000000800000, parents both partial_sterile, 3 transferred refuted bits awaiting engine confirmation - watch item, not a sweep target)",
            "sterile_parent_exclusion": {
                "fully_sterile_parents_at_1589": [
                    {"s5_hex": p, "classes": parents[p]["classes"],
                     "rows": len(p_rows[p]),
                     "cost": sum(int(open1589[h]["own_candidates_s6_s7_edge_cost"]) for h in p_rows[p]),
                     "head1410_classification": parents[p]["classification"]}
                    for p in fully_sterile
                ],
                "rows_excluded": sterile_row_count,
                "cost_excluded": sterile_cost,
            },
        },
        "overlay_note": "open_bits_upper_bound uses the pre-64h harvest overlay only (78 sources + 76d/77e); the 22 post-64h verdict maps are not bit-folded here; sweep protocol re-runs confirmation bits fresh, so post-64h overlap does not affect target cost accounting",
        "ranking_policy": {
            "base": "cheapest cost, then fewest open bits, then hex",
            "override": "parent-closure-first (coordinator certificate-candidate concentration): a sweep that can complete an S5 parent's row set takes precedence; rationale: only a fully closed parent reduces remaining_s5_orbits (174) and extends manifest secured coverage",
            "eligible_rows": len(eligible),
            "cheapest_20": [{k: r[k] for k in ("row", "cost", "legal_bits", "harvest_known_refuted", "open_bits_upper_bound")} for r in eligible[:20]],
        },
        "selected_target": {
            "row_hex": TARGET,
            "band_cost": 78,
            "legal_bits": 78,
            "category": "unswept",
            "open_parents": [TARGET_PARENT],
            "parent_classes": parents[TARGET_PARENT]["classes"],
            "parent_rows_before_fold": 12,
            "parent_rows_after_fold": 1,
            "parent_edge_cost_after_fold": 78,
            "harvest_known_win_bits": 0,
            "harvest_confirmation_bits": conf_bits,
            "fresh_bits": 78 - len(conf_bits),
            "expected_nodes_upper_bound": "78 bits x cap 1e9; the 82d/82e rows of similar cost completed at ~1.2e8 candidate nodes total",
            "outcome_if_win": "first fully receipt-closed S5 parent; remaining_s5_orbits 174 -> 173; certificate extraction per cert_driver protocol, then receipt fold of the new root",
            "outcome_if_all_refuted": "row STERILE; parent 00000000000000403800000008000000 D10-unclosable (definitive negative structural fact); revalidation band like 82d/82e",
        },
        "controls": {
            "fold_rederivation": "PASS (audit module assertions all green)",
            "eligible_pool_size": 6223,
            "target_consistency": "PASS (no known WIN bit, 2 confirmation bits, single open parent, cost 78)",
        },
        "interpretation_guard": "Census and target selection only; no new engine verdict; the 11x11 empty board remains UNKNOWN.",
        "next_action": "Sweep 00000000000000403800000008000008 (cost 78) in 9-bit batches per the ev82e protocol: v17 runner, v15 crosscheck, deterministic re-run of disagreements, cap 1e9 per bit, andclose 1, terminal range [13,17], raw JSONL published; band name to be assigned from the next free cost-78 slot (78a/78c used).",
    }
    outp = OUT / "class2-lane-next-target-presweep-1589-v20-20261118.json"
    outp.write_text(json.dumps(record, indent=1) + "\n")
    print(f"[4] wrote {outp.name}: {outp.stat().st_size} bytes")


if __name__ == "__main__":
    main()
