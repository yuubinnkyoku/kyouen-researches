#!/usr/bin/env python3
"""Record-level consistency audit for the unpublished-raw cost73k sweep.

This does NOT independently rerun the df-pn engine. It checks the published
per-bit summary against the pinned census-v7 claim, independently derives
all 73 S6->S7 survival moves using K0868's exact det4 expansion, and verifies
the node totals, batch partition, and v6/v7 confirmation bookkeeping.

For historical replay after the in-flight claim is updated, recover its v1
bytes with: git show a0987c37:<claim path> > /tmp/cost73k-claim-v1.json
then pass --claim /tmp/cost73k-claim-v1.json.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
ROOT = HERE.parents[2]
RECORD_DEFAULT = OUT / "class2-lane-cost73k-concurrent-session-sweep-record-20261117.json"
CLAIM_DEFAULT = OUT / "class2-lane-cost73k-inflight-20261117.json"
CENSUS_DEFAULT = OUT / "class2-lane-next-target-presweep-1472-v7-20261117.json"
K0868_DEFAULT = ROOT / "research/knowledge/items/K0868-n11-s6-s7-sweep-candidate-convention.md"

PINS = {
    "record": "0cba988e2a65e9195b0a0e6a3168a518e27079fb",
    "claim": "a24d3557ef23a279cc08c2d578e420f676f28f05",
    "census": "68246f3263fe6cbb49ffafa866f73b49cf3c2ebb",
    "K0868": "b097210d0b49d7cf014cc6a554298b1e49e83384",
}
EXPECTED_V6_CONFIRM = [23, 26, 34, 53, 55, 107]
EXPECTED_V7_CONFIRM = [14, 23, 26, 34, 53, 55, 107]


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def det3(a, b, c):
    def row(p):
        x, y = p
        return x*x + y*y, x, y
    a0,a1,a2 = row(a)
    b0,b1,b2 = row(b)
    c0,c1,c2 = row(c)
    return (a0*(b1*c2-b2*c1) - a1*(b0*c2-b2*c0)
            + a2*(b0*c1-b1*c0))


def det4(a, b, c, d):
    return det3(a,b,c)-det3(a,b,d)+det3(a,c,d)-det3(b,c,d)


def derive_survival_moves(stone_bits):
    stones = [(i % 11, i // 11) for i in stone_bits]
    occupied = set(stone_bits)
    triples = list(itertools.combinations(stones, 3))
    legal, blocked = [], []
    for bit in range(121):
        if bit in occupied:
            continue
        d = (bit % 11, bit // 11)
        (blocked if any(det4(a,b,c,d) == 0 for a,b,c in triples)
         else legal).append(bit)
    return legal, blocked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", type=Path, default=RECORD_DEFAULT)
    ap.add_argument("--claim", type=Path, default=CLAIM_DEFAULT)
    ap.add_argument("--census", type=Path, default=CENSUS_DEFAULT)
    ap.add_argument("--k0868", type=Path, default=K0868_DEFAULT)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--skip-pins", action="store_true",
                    help="fixture tests only; never use for publication")
    args = ap.parse_args()

    raw = {
        "record": args.record.read_bytes(),
        "claim": args.claim.read_bytes(),
        "census": args.census.read_bytes(),
        "K0868": args.k0868.read_bytes(),
    }
    docs = {k: json.loads(raw[k]) for k in ("record", "claim", "census")}
    hashes = {k: git_blob_sha(v) for k, v in raw.items()}
    if not args.skip_pins:
        for key, expected in PINS.items():
            assert hashes[key] == expected, (key, hashes[key], expected)

    record, claim, census = docs["record"], docs["claim"], docs["census"]
    child_hex = claim["s6_child"]
    child = int(child_hex, 16)
    stones = [i for i in range(128) if (child >> i) & 1]
    assert stones == claim["child_stones_bit_indices"]
    assert stones == record["sweep_execution"]["child_stones_bit_indices"]
    assert len(stones) == 6
    assert record["sweep_execution"]["child"] == child_hex

    legal, blocked = derive_survival_moves(stones)
    assert legal == claim["legal_candidates"]
    assert len(legal) == claim["candidate_count"] == claim["s6_s7_edge_cost"] == 73

    bits_meta = claim["engine_candidate_bits"]
    open_bits = bits_meta["open_bits"]
    v7_confirm = bits_meta["confirmation_bits"]
    assert sorted(v7_confirm) == EXPECTED_V7_CONFIRM
    assert len(open_bits) == bits_meta["open_bit_count"] == 66
    assert len(v7_confirm) == bits_meta["confirmation_bit_count"] == 7
    assert not (set(open_bits) & set(v7_confirm))
    assert sorted(open_bits + v7_confirm) == legal

    per = record["verdicts"]["per_bit"]
    per_bits = sorted(map(int, per))
    assert per_bits == legal
    wins = sorted(int(b) for b, r in per.items() if r["loss"] is True)
    refuted = sorted(int(b) for b, r in per.items() if r["loss"] is False)
    capped = sorted(int(b) for b, r in per.items() if r["capped"] is True)
    assert wins == sorted(record["verdicts"]["win7_d10_bits"])
    assert refuted == sorted(record["verdicts"]["refuted_d10_bits"])
    assert len(wins) == 25 and len(refuted) == 48 and not capped
    assert set(wins).isdisjoint(refuted)
    assert sorted(wins + refuted) == legal

    node_sum = sum(r["nodes"] for r in per.values())
    sweep = record["sweep_execution"]
    assert node_sum == sweep["candidate_nodes_total"] == 128861941
    pilot_delta = sweep["total_nodes_including_pilots"] - node_sum
    assert pilot_delta == 9 * 3402
    assert sweep["capped_count"] == 0
    assert sweep["terminal_stone_range_all_bits"] == [13, 17]
    assert "9/9 batches" in sweep["pilot_controls"] and "nodes=3402" in sweep["pilot_controls"]
    assert "25/25 loss=true" in sweep["v15_cross_engine_check"]

    batch = {}
    for bit, result in per.items():
        b = result["batch"]
        batch.setdefault(b, {"count": 0, "nodes": 0, "bits": []})
        batch[b]["count"] += 1
        batch[b]["nodes"] += result["nodes"]
        batch[b]["bits"].append(int(bit))
    assert sorted(batch) == list(range(1, 10))
    assert {b: x["count"] for b, x in batch.items()} == {
        1:9, 2:9, 3:9, 4:9, 5:9, 6:9, 7:9, 8:4, 9:6
    }
    assert batch[7]["nodes"] == 24968847

    # The concurrent session used its earlier v6 claim: six confirmations,
    # with bit 14 still in the 67-bit open sweep. The canonical v7 claim adds
    # bit 14 as a seventh confirmation after the cost73j map landed.
    v6_confirm = record["situation"]["this_session_claim_v1"]["confirmation_bits"]
    assert sorted(v6_confirm) == EXPECTED_V6_CONFIRM
    assert record["situation"]["this_session_claim_v1"]["open_bit_count"] == 67
    v6_open = sorted(set(legal) - set(v6_confirm))
    batch1_to8 = sorted(bit for b in range(1, 9) for bit in batch[b]["bits"])
    assert v6_open == batch1_to8 and len(v6_open) == 67
    assert batch[9]["bits"] == sorted(v6_confirm)
    assert 14 in v6_open and per["14"]["batch"] == 1

    claim_transfers = {int(b): v["verdict"] for b, v in claim["transfers"].items()}
    v7_pred = record["confirmation_agreement"]["census_v7_claim_predictions"]
    v7_fresh = record["confirmation_agreement"]["fresh_outcomes"]
    v6_pred = record["confirmation_agreement"]["census_v6_claim_predictions"]
    actual = {
        b: ("WIN7-D10" if per[str(b)]["loss"] else "REFUTED-D10")
        for b in EXPECTED_V7_CONFIRM
    }
    assert claim_transfers == actual
    assert {int(k): v for k, v in v7_pred.items()} == actual
    assert {int(k): v for k, v in v7_fresh.items()} == actual
    assert {int(k): v for k, v in v6_pred.items()} == {
        b: actual[b] for b in EXPECTED_V6_CONFIRM
    }

    v7_target = census["selected_target"]
    assert v7_target["s6_hex"] == child_hex
    assert v7_target["cost"] == len(legal) == 73
    assert v7_target["legal_candidates"] == 73
    assert sorted(v7_target["sweep_bits"]) == open_bits
    assert census["ranking_top10"][0]["s6_hex"] == child_hex
    assert sorted(v7_target["confirmation_bits"], key=lambda x: x["bit"]) == sorted(
        v7_target["confirmation_bits"], key=lambda x: x["bit"])

    canonical_claim = record["situation"]["parallel_session_claim_v1"]
    assert PINS["claim"][:8] in canonical_claim["file"]
    assert sorted(canonical_claim["confirmation_bits"]) == EXPECTED_V7_CONFIRM
    assert canonical_claim["open_bit_count"] == 66
    assert "yes" in canonical_claim["canonical"]
    assert claim["actual_execution"]["batches_run"] == 0
    assert claim["actual_execution"]["results"] is None

    result = {
        "schema": "n11-class2-lane-cost73k-concurrent-record-consistency-audit-20261117-v1",
        "status": "PASS: published summary is internally consistent with the pinned v7 claim and exact geometry",
        "source_pins": hashes,
        "target": {
            "s6_child": child_hex,
            "stone_bits": stones,
            "stone_coordinates": [[i, i % 11, i // 11] for i in stones],
            "survival_moves": legal,
            "survival_count": len(legal),
            "completing_or_blocked_moves": blocked,
            "completing_count": len(blocked),
            "all_empty_cells_partitioned": len(legal) + len(blocked) == 115,
        },
        "sweep_record_checks": {
            "per_bit_count": len(per_bits),
            "win7_d10_count": len(wins),
            "refuted_d10_count": len(refuted),
            "capped_count": len(capped),
            "win_and_refuted_partition_all_legal_moves": True,
            "per_bit_node_sum": node_sum,
            "recorded_candidate_nodes": sweep["candidate_nodes_total"],
            "total_nodes_including_pilots": sweep["total_nodes_including_pilots"],
            "pilot_delta": pilot_delta,
            "nine_pilot_controls_exact_3402": True,
            "batch_distribution": batch,
            "batch7_nodes_match_recorded_24968847": True,
            "terminal_stone_range_recorded": sweep["terminal_stone_range_all_bits"],
            "v15_cross_engine_summary": sweep["v15_cross_engine_check"],
        },
        "cross_session_confirmation": {
            "v6_confirmation_bits": EXPECTED_V6_CONFIRM,
            "v6_confirmation_count": len(v6_confirm),
            "v6_open_count": len(v6_open),
            "v6_batch9_matches_six_confirmations": True,
            "bit14_was_v6_open_and_was_run_in_batch1": True,
            "v7_confirmation_bits": EXPECTED_V7_CONFIRM,
            "v7_confirmation_outcomes": {str(k): actual[k] for k in EXPECTED_V7_CONFIRM},
            "v7_confirmation_agreement": "7/7",
            "v6_confirmation_agreement": "6/6",
            "canonical_v7_claim_remains_inflight": True,
            "canonical_claim_batches_run": claim["actual_execution"]["batches_run"],
        },
        "evidence_boundary": {
            "raw_batch_bytes_published": False,
            "raw_batch_audit_published": False,
            "certificate_manifest_published": False,
            "determinism_claim_independently_rechecked": False,
            "v15_per_bit_records_available": False,
            "node_sum_and_partition_recomputed_from_published_per_bit_table": True,
            "this_audit_does_not_rerun_or_independently_verify_the_search_engine": True,
        },
        "interpretation_guard": "WIN7-D10 applies only to each individual 7-stone root within depth 10; REFUTED-D10 is not a LOSS proof; no receipt row is closed by this audit; standard 11x11 remains UNKNOWN.",
    }
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
