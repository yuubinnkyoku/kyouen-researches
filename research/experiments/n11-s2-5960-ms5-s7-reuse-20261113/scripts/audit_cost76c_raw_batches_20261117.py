#!/usr/bin/env python3
"""Audit the published cost76c raw batches without rerunning the search engine.

Run from any directory:
    python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost76c_raw_batches_20261117.py
Only Python's standard library is used.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CLAIM_NAME = "class2-lane-cost76c-claim-input-20261117.json"
PRESWEEP_NAME = "class2-lane-next-target-presweep-1452-20261116.json"
CLAIM_BLOB = "8932f2d5e100325549a5f251a1d883558cae0708"
PRESWEEP_BLOB = "0d9a94a272de9fe45708757f17bfea60239a3c9b"
RAW_BLOBS = {
    1: "1aebb80f0b4f4384a7207afff4c706433d0fcaff",
    2: "7b0b471d81ad1815f529bfc98a63acdff73ccc7a",
    3: "9f5c63cd2c93a276ebcfc6874f2f0aa870921c0c",
    4: "a7c5ee5167529ff44351f5b438cf1636352bffca",
    5: "a07e06607aeb6b9a06f629e9210bc6774b43e964",
    6: "beb9283161491d17c435890f563b8c7f283b48a3",
    7: "a511e748ba227b2d20627f653acde89fca0e19e6",
    8: "a2aa8bb60fd7f5c875a234ead60f4826335d32a6",
    9: "0f41ee0c7f685f8a41a5574a399dde3c6eea7eee",
    10: "273f6e710d791b20e5ec2ab57ae53b7127f18122",
}
WIN_CANONS = {
    61: "0000000001000080b002000001000000",
    99: "00000000040000809002000000400800",
    113: "00000000040000809002000000400008",
}


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def read_pinned(path: Path, expected: str) -> bytes:
    data = path.read_bytes()
    actual = git_blob_sha(data)
    if actual != expected:
        raise AssertionError(f"blob SHA mismatch: {path.name}: {actual} != {expected}")
    return data


def parse_jsonl(data: bytes, path: Path):
    rows = []
    for line_no, raw in enumerate(data.decode("utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            rows.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{path.name}:{line_no}: {exc}") from exc
    return rows


def main() -> None:
    checks = {}

    def check(name: str, condition: bool) -> None:
        checks[name] = bool(condition)
        if not condition:
            raise AssertionError(name)

    claim_bytes = read_pinned(OUT / CLAIM_NAME, CLAIM_BLOB)
    claim = json.loads(claim_bytes)
    presweep_bytes = read_pinned(OUT / PRESWEEP_NAME, PRESWEEP_BLOB)
    presweep = json.loads(presweep_bytes)

    batches = []
    records = []
    for batch_no in range(1, 11):
        name = f"class2-lane-cost76c-raw-batch{batch_no}-20261116.jsonl"
        path = OUT / name
        data = read_pinned(path, RAW_BLOBS[batch_no])
        rows = parse_jsonl(data, path)
        bit_rows = [row for row in rows if isinstance(row.get("bit"), int)]
        pilots = [row for row in rows if row.get("control") == "pilot_d6"]
        if len(pilots) != 1:
            raise AssertionError(f"{name}: expected exactly one pilot")
        pilot = pilots[0]
        if not (pilot.get("loss") is False and pilot.get("nodes") == 3402
                and pilot.get("capped") is False):
            raise AssertionError(f"{name}: pilot mismatch")
        planned = claim["engine"]["batches"][batch_no - 1]["bits"]
        actual = [row["bit"] for row in bit_rows]
        if actual != planned:
            raise AssertionError(f"{name}: bit list differs from claim batch plan")
        batches.append({
            "batch": batch_no,
            "bits": actual,
            "win_bits": [row["bit"] for row in bit_rows if row.get("loss") is True],
            "node_sum": sum(row["nodes"] for row in bit_rows),
            "pilot_nodes": pilot["nodes"],
            "blob_sha1": RAW_BLOBS[batch_no],
        })
        records.extend(bit_rows)

    by_bit = {row["bit"]: row for row in records}
    if len(by_bit) != len(records):
        raise AssertionError("duplicate bit records")
    legal = sorted(claim["legal_candidates"])
    transfers = sorted(int(bit) for bit in claim["transfers"])
    open_bits = claim["engine_candidate_bits"]["open_bits"]
    cross_bits = claim["engine_candidate_bits"]["crosscheck_bits"]
    reused_bits = claim["engine_candidate_bits"]["reused_transferred_bits"]
    wins = sorted(row["bit"] for row in records if row.get("loss") is True)
    refuted = [row for row in records
               if row.get("loss") is False and row.get("capped") is False]
    capped = [row for row in records if row.get("capped") is True]

    check("ten_raw_batches", len(batches) == 10)
    check("all_76_legal_bits_once", sorted(by_bit) == legal and len(records) == 76)
    check("batch_plan_matches_raw", True)  # each batch was checked before aggregation
    check("one_exact_pilot_per_batch", len(batches) == 10
          and all(batch["pilot_nodes"] == 3402 for batch in batches))
    check("all_uncapped_and_andclose", len(records) == 76
          and all(row.get("capped") is False and row.get("andclose") is True
                  for row in records))
    check("terminal_range_13_17", all(row.get("terminalStoneRange") == [13, 17]
                                      for row in records))
    check("all_15_transfers_rerun_refuted", len(transfers) == 15
          and all(bit in by_bit and by_bit[bit].get("loss") is False
                  and by_bit[bit].get("capped") is False for bit in transfers))
    check("crosscheck_and_reuse_partition_transfers",
          len(cross_bits) == 5 and len(reused_bits) == 10
          and set(cross_bits).isdisjoint(reused_bits)
          and set(cross_bits) | set(reused_bits) == set(transfers))
    check("61_open_bits_present", len(open_bits) == 61
          and set(open_bits).isdisjoint(transfers)
          and set(open_bits) | set(transfers) == set(legal))
    check("three_wins_exactly", wins == [61, 99, 113])
    check("73_refuted_zero_capped", len(refuted) == 73 and len(capped) == 0)
    check("planned_66_actual_76_recorded", len(open_bits) + len(cross_bits) == 66
          and len(records) == 76)

    child = claim["s6_child"]
    presweep_rows = {
        row["bit"]: row for row in presweep["bit_tables"][child]["bits"]
    }
    winner_roots = []
    for bit in wins:
        row = presweep_rows[bit]
        if row.get("status") != "open" or row.get("root_canon") != WIN_CANONS[bit]:
            raise AssertionError(f"winner bit {bit}: presweep root mismatch")
        winner_roots.append({
            "bit": bit,
            "root_canon": row["root_canon"],
            "nodes": by_bit[bit]["nodes"],
        })
    check("winner_root_canons_match_presweep", len(winner_roots) == 3)

    node_sum = sum(row["nodes"] for row in records)
    pilot_sum = sum(batch["pilot_nodes"] for batch in batches)
    output = {
        "schema": "n11-class2-lane-cost76c-raw-sweep-audit-20261117-v1",
        "date": "2026-11-17",
        "status": "raw-sweep-audited; certificate-extraction-pending; receipt-fold-pending",
        "source_blob_pins": {
            CLAIM_NAME: CLAIM_BLOB,
            PRESWEEP_NAME: PRESWEEP_BLOB,
            **{f"class2-lane-cost76c-raw-batch{n}-20261116.jsonl": sha
               for n, sha in RAW_BLOBS.items()},
        },
        "target": {
            "s5": claim["s5"],
            "s6_child": child,
            "legal_candidate_count": len(legal),
            "canonical_head_at_sweep": "1452/174/6396/506144/4669/370058",
        },
        "plan_vs_execution": {
            "planned_engine_bits": len(open_bits) + len(cross_bits),
            "planned_reused_transferred_bits": len(reused_bits),
            "actual_raw_engine_bits": len(records),
            "note": ("The claim partitions 61 open + 5 crosscheck bits = 66 planned "
                     "engine bits and marks 10 transferred bits for reuse. The "
                     "published batch arrays and raw outputs nevertheless cover "
                     "all 76 legal bits, so those 10 reuse-marked bits were also "
                     "rerun and must not be counted as saved work."),
        },
        "result": {
            "win7_d10_bits": wins,
            "winner_roots": winner_roots,
            "refuted_d10_count": len(refuted),
            "capped_count": len(capped),
            "candidate_node_sum": node_sum,
            "pilot_count": len(batches),
            "pilot_nodes_each": 3402,
            "pilot_node_sum": pilot_sum,
            "total_nodes_including_pilots": node_sum + pilot_sum,
            "terminal_stone_range": [13, 17],
            "transferred_refuted_bits_rerun": transfers,
        },
        "batch_summaries": batches,
        "checks": checks,
        "interpretation_guard": {
            "loss_true": "WIN7-D10 for that individual seven-stone root.",
            "loss_false_uncapped": "REFUTED-D10, not a LOSS proof.",
            "capped": "No conclusion from that candidate.",
            "scope": ("This audit does not extract or independently verify the "
                      "three WIN7 certificate trees and does not fold receipts."),
        },
    }
    destination = OUT / "class2-lane-cost76c-raw-audit-20261117.json"
    destination.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    print(json.dumps({
        "status": output["status"],
        "wins": wins,
        "refuted": len(refuted),
        "capped": len(capped),
        "nodes": node_sum,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "output": str(destination),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
