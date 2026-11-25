#!/usr/bin/env python3
"""Independent structural audit of the cost73l claim and census-v8 partition.

This does NOT run the depth-10 game engine and does NOT validate its verdicts.
It independently re-derives K0868 survival candidates with integer det4,
checks the 66+7 partition, verifies the S5 parent orbit, and reconstructs
all seven transferred roots under D4.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CLAIM_NAME = "class2-lane-cost73l-inflight-20261117.json"
CENSUS_NAME = "class2-lane-next-target-presweep-1473-v8-20261117.json"
CLAIM_BLOB = "fa13a0ada22e3de95c06e9a3101ce6d2a738f5b1"
CENSUS_BLOB = "2542914e02db14a8426a1a16ef1c2cfcd9817375"
OUTPUT_NAME = "class2-lane-cost73l-claim-structural-audit-20261117.json"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load_pinned(name: str, expected_blob: str) -> dict:
    raw = (OUT / name).read_bytes()
    actual = git_blob_sha(raw)
    if actual != expected_blob:
        raise ValueError(f"{name}: Git blob SHA {actual} != {expected_blob}")
    return json.loads(raw)


def occupied_bits(mask: int) -> list[int]:
    return [p for p in range(121) if (mask >> p) & 1]


def det3(a: int, b: int, c: int) -> int:
    def row(p: int) -> tuple[int, int, int]:
        x, y = p % 11, p // 11
        return x * x + y * y, x, y

    qa, xa, ya = row(a)
    qb, xb, yb = row(b)
    qc, xc, yc = row(c)
    return (
        qa * (xb * yc - yb * xc)
        - xa * (qb * yc - yb * qc)
        + ya * (qb * xc - xb * qc)
    )


def det4(a: int, b: int, c: int, d: int) -> int:
    # K0868: expansion of the [x^2+y^2, x, y, 1] determinant.
    return det3(a, b, c) - det3(a, b, d) + det3(a, c, d) - det3(b, c, d)


def derive_survival_candidates(stones: list[int]) -> tuple[list[int], dict[int, list[int]]]:
    legal: list[int] = []
    excluded_witnesses: dict[int, list[int]] = {}
    occupied = set(stones)
    triples = [
        (stones[i], stones[j], stones[k])
        for i in range(len(stones))
        for j in range(i + 1, len(stones))
        for k in range(j + 1, len(stones))
    ]
    for p in range(121):
        if p in occupied:
            continue
        witness = next((triple for triple in triples if det4(*triple, p) == 0), None)
        if witness is None:
            legal.append(p)
        else:
            excluded_witnesses[p] = list(witness)
    return legal, excluded_witnesses


def transform_position(p: int, transform: int) -> int:
    x, y = p % 11, p // 11
    images = (
        (x, y),
        (y, 10 - x),
        (10 - x, 10 - y),
        (10 - y, x),
        (10 - x, y),
        (x, 10 - y),
        (y, x),
        (10 - y, 10 - x),
    )
    a, b = images[transform]
    return 11 * b + a


def d4_canon(mask: int) -> str:
    images: list[int] = []
    for transform in range(8):
        image = 0
        for p in occupied_bits(mask):
            image |= 1 << transform_position(p, transform)
        images.append(image)
    return f"{min(images):032x}"


def audit_objects(claim: dict, census: dict) -> dict:
    child_hex = claim["s6_child"]
    child = int(child_hex, 16)
    stones = occupied_bits(child)
    legal, excluded = derive_survival_candidates(stones)
    listed = claim["legal_candidates"]
    engine = claim["engine_candidate_bits"]
    opened = engine["open_bits"]
    confirmation = engine["confirmation_bits"]
    selected = census["selected_target"]
    transfers = claim["transfers"]

    checks = {
        "child_has_six_stones": len(stones) == 6,
        "det4_rederives_73_survival_moves": (
            len(legal) == 73
            and claim["candidate_count"] == 73
            and claim["s6_s7_edge_cost"] == 73
            and selected["legal_candidates"] == 73
        ),
        "claim_legal_list_is_exact": listed == legal,
        "all_115_empty_cells_are_partitioned": (
            len(legal) + len(excluded) == 121 - len(stones)
            and len(legal) == 73
            and len(excluded) == 42
        ),
        "every_excluded_cell_has_det4_zero_witness": (
            len(excluded) == 42
            and all(len(witness) == 3 for witness in excluded.values())
            and all(det4(*witness, p) == 0 for p, witness in excluded.items())
        ),
        "engine_partition_is_66_plus_7": (
            len(opened) == 66
            and len(confirmation) == 7
            and engine["open_bit_count"] == 66
            and engine["confirmation_bit_count"] == 7
        ),
        "open_and_confirmation_partition_exactly_legal": (
            len(set(opened)) == len(opened)
            and len(set(confirmation)) == len(confirmation)
            and not (set(opened) & set(confirmation))
            and sorted(opened + confirmation) == legal
        ),
        "s5_parent_is_a_d4_one_stone_deletion": any(
            d4_canon(child ^ (1 << p)) == claim["s5"] for p in stones
        ),
        "claim_and_census_use_same_head": (
            census["chain_head"] == claim["basis_head"].split(" ")[0]
        ),
        "selected_child_parent_and_cost_match": (
            selected["s6_hex"] == child_hex
            and selected["parent"] == claim["s5"]
            and selected["cost"] == claim["s6_s7_edge_cost"]
            and selected["demand"] == claim["demand"]
        ),
        "census_sweep_bits_match_claim": selected["sweep_bits"] == opened,
        "census_confirmation_bits_match_claim": (
            [item["bit"] for item in selected["confirmation_bits"]] == confirmation
        ),
        "rank_one_is_selected_target": (
            census["ranking_top10"][0]["s6_hex"] == child_hex
            and census["ranking_top10"][0]["cost"] == 73
            and census["ranking_top10"][0]["open_after_census_v8"] == 66
        ),
        "rank_two_matches_recorded_runner_up": (
            census["ranking_top10"][1]["s6_hex"] == selected["runner_up"]["s6_hex"]
            and census["ranking_top10"][1]["cost"] == selected["runner_up"]["cost"] == 74
            and census["ranking_top10"][1]["open_after_census_v8"]
            == selected["runner_up"]["open_after_census_v8"] == 69
        ),
        "transfer_bits_equal_confirmation_bits": (
            sorted(int(bit) for bit in transfers) == confirmation
        ),
    }

    transfer_rows = []
    for bit in confirmation:
        transfer = transfers[str(bit)]
        actual_canon = d4_canon(child | (1 << bit))
        transfer_rows.append({
            "bit": bit,
            "verdict": transfer["verdict"],
            "published_root_canon": transfer["root_canon"],
            "recomputed_root_canon": actual_canon,
            "root_canon_matches": actual_canon == transfer["root_canon"],
        })
    checks["all_seven_transfer_roots_match_d4"] = all(
        row["root_canon_matches"] for row in transfer_rows
    )

    confirmation_by_bit = {item["bit"]: item["verdict"] for item in selected["confirmation_bits"]}
    checks["transfer_verdicts_match_census"] = all(
        transfers[str(bit)]["verdict"] == confirmation_by_bit[bit]
        for bit in confirmation
    )
    verdicts = [transfers[str(bit)]["verdict"] for bit in confirmation]
    checks["confirmation_split_is_two_win_five_refuted"] = (
        verdicts.count("WIN7-D10") == 2
        and verdicts.count("REFUTED-D10") == 5
    )

    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError("audit failed: " + ", ".join(failed))

    return {
        "checks": checks,
        "all_checks_pass": True,
        "child": child_hex,
        "s5_parent_canon": claim["s5"],
        "stone_bits": stones,
        "legal_candidate_count": len(legal),
        "legal_candidates": legal,
        "excluded_empty_cell_count": len(excluded),
        "excluded_cell_zero_determinant_witnesses": [
            {"cell": p, "triple": witness}
            for p, witness in sorted(excluded.items())
        ],
        "open_bit_count": len(opened),
        "confirmation_bit_count": len(confirmation),
        "confirmation_bits": confirmation,
        "transfer_rows": transfer_rows,
        "verdict_semantics": {
            "WIN7-D10": "individual seven-stone root has a first-player win within depth 10",
            "REFUTED-D10": "no such depth-10 win was found; this is not a LOSS proof",
        },
        "engine_sweep_performed_by_this_audit": False,
        "receipt_fold_performed_by_this_audit": False,
        "empty_board_outcome": "UNKNOWN",
    }


def expect_rejection(name: str, claim: dict, census: dict, mutate) -> dict:
    changed_claim = copy.deepcopy(claim)
    changed_census = copy.deepcopy(census)
    mutate(changed_claim, changed_census)
    try:
        audit_objects(changed_claim, changed_census)
    except (AssertionError, KeyError, ValueError):
        return {"test": name, "rejected": True}
    return {"test": name, "rejected": False}


def main() -> None:
    claim = load_pinned(CLAIM_NAME, CLAIM_BLOB)
    census = load_pinned(CENSUS_NAME, CENSUS_BLOB)
    result = audit_objects(claim, census)
    negative_tests = [
        expect_rejection(
            "missing_legal_candidate",
            claim, census,
            lambda c, s: c["legal_candidates"].pop(),
        ),
        expect_rejection(
            "duplicate_legal_candidate",
            claim, census,
            lambda c, s: c["legal_candidates"].append(c["legal_candidates"][0]),
        ),
        expect_rejection(
            "missing_open_bit",
            claim, census,
            lambda c, s: c["engine_candidate_bits"]["open_bits"].pop(),
        ),
        expect_rejection(
            "wrong_transfer_root",
            claim, census,
            lambda c, s: c["transfers"]["106"].update(root_canon="0" * 32),
        ),
        expect_rejection(
            "wrong_selected_child",
            claim, census,
            lambda c, s: s["selected_target"].update(s6_hex="0" * 32),
        ),
    ]
    result["negative_tests"] = negative_tests
    result["negative_tests_pass"] = all(item["rejected"] for item in negative_tests)
    result["source_pins"] = {
        CLAIM_NAME: CLAIM_BLOB,
        CENSUS_NAME: CENSUS_BLOB,
    }
    result["basis_commit"] = "43838dec48c863589d897a32497c59524b6be071"
    result["schema"] = "n11-class2-lane-cost73l-claim-structural-audit-20261117-v1"
    result["date"] = "2026-11-17"
    result["all_checks_pass"] = (
        result["all_checks_pass"] and result["negative_tests_pass"]
    )
    payload = json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    output = OUT / OUTPUT_NAME
    output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
