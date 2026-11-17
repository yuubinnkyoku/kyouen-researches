#!/usr/bin/env python3
"""Independent structural audit of the cost78c claim; no game search is run.

Uses only the Python standard library. Recomputes K0868 det4 legality,
the 66+12 partition, D4 canonical roots, and all twelve transfer sources.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

SCRIPT = Path(__file__).resolve()
EXPERIMENT = SCRIPT.parents[1]
ROOT = SCRIPT.parents[4]
OUT = EXPERIMENT / "output"
BASE_MAIN = "9bf3866cd4a2b71cdf5d11cb313ffc7173abf1b2"
PINS = {
    "claim": ("class2-lane-cost78c-inflight-20261117.json", "7c38b88e33d1c176bdedf582bea7138cfa6a067a"),
    "census": ("class2-lane-next-target-presweep-1473-v11-20261117.json", "1e2b6a2b688db1a93098edea62b5793b54efaaba"),
    "cost64d": ("class2-lane-cost64d-inflight-20261116.json", "e3cf7378a08b156c5c0299c52e4ccbcd59de9236"),
    "cost70b": ("class2-lane-cost70b-sweep-20261114.json", "d0eb4d23f674d218b23065ca72d4b63b58a9eeea"),
    "cost70b_batch5": ("class2-lane-cost70b-raw-batch5-20261114.jsonl", "67ded8a966b1880604985fd817fbe4195f29f47d"),
}
K0868 = ("research/knowledge/items/K0868-n11-s6-s7-sweep-candidate-convention.md",
         "b097210d0b49d7cf014cc6a554298b1e49e83384")


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def read_pinned(path: Path, expected: str) -> bytes:
    data = path.read_bytes()
    actual = git_blob_sha(data)
    assert actual == expected, (str(path), actual, expected)
    return data


def read_json(name: str) -> dict:
    filename, pin = PINS[name]
    return json.loads(read_pinned(OUT / filename, pin))


def det3(p: int, q: int, r: int) -> int:
    def row(bit: int) -> tuple[int, int, int]:
        x, y = bit % 11, bit // 11
        return x * x + y * y, x, y

    a, b, c = row(p), row(q), row(r)
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def det4(a: int, b: int, c: int, d: int) -> int:
    return det3(a, b, c) - det3(a, b, d) + det3(a, c, d) - det3(b, c, d)


def d4_images(mask: int) -> list[int]:
    images = [0] * 8
    for p in range(121):
        if not (mask >> p) & 1:
            continue
        x, y = p % 11, p // 11
        coords = (
            (x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
            (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x),
        )
        for i, (a, b) in enumerate(coords):
            images[i] |= 1 << (11 * b + a)
    return images


def canon(mask: int) -> int:
    return min(d4_images(mask))


def hex128(mask: int) -> str:
    return f"{mask:032x}"


def main() -> None:
    claim = read_json("claim")
    census = read_json("census")
    cost64d = read_json("cost64d")
    cost70b = read_json("cost70b")
    batch5 = [
        json.loads(line)
        for line in read_pinned(OUT / PINS["cost70b_batch5"][0], PINS["cost70b_batch5"][1]).decode().splitlines()
        if line.strip()
    ]
    k0868_bytes = read_pinned(ROOT / K0868[0], K0868[1])
    k0868_text = k0868_bytes.decode()

    checks: dict[str, dict] = {}

    def check(name: str, ok: bool, **detail) -> None:
        checks[name] = {"ok": bool(ok), **detail}
        assert ok, (name, detail)

    child = int(claim["s6_child"], 16)
    stones = claim["child_stones_bit_indices"]
    stone_mask = sum(1 << b for b in stones)
    check("child_hex_matches_stones", child == stone_mask, hex=claim["s6_child"], stones=stones)
    triples = [
        (stones[i], stones[j], stones[k])
        for i in range(len(stones))
        for j in range(i + 1, len(stones))
        for k in range(j + 1, len(stones))
    ]
    legal, forbidden = [], []
    for p in range(121):
        if (child >> p) & 1:
            continue
        witness = next((t for t in triples if det4(*t, p) == 0), None)
        if witness is None:
            legal.append(p)
        else:
            forbidden.append({"bit": p, "witness": list(witness)})

    listed = sorted(claim["legal_candidates"])
    check("det4_legal_set_matches_claim", legal == listed,
          derived_count=len(legal), claim_count=len(listed))
    check("all_empty_cells_partitioned", len(legal) + len(forbidden) == 115,
          empty=115, legal=len(legal), forbidden=len(forbidden))

    open_bits = sorted(claim["engine_candidate_bits"]["open_bits"])
    confirmation_bits = sorted(claim["engine_candidate_bits"]["confirmation_bits"])
    union = sorted(open_bits + confirmation_bits)
    check("open_confirmation_disjoint", len(union) == len(set(union)),
          open=len(open_bits), confirmation=len(confirmation_bits))
    check("open_plus_confirmation_equals_legal", union == legal,
          union_count=len(union), legal_count=len(legal))
    check("candidate_counts",
          claim["candidate_count"] == claim["s6_s7_edge_cost"] == len(legal) == 78
          and len(open_bits) == 66 and len(confirmation_bits) == 12,
          candidate_count=claim["candidate_count"], edge_cost=claim["s6_s7_edge_cost"])

    transfers = claim["transfers"]
    transfer_bits = sorted(map(int, transfers))
    check("transfer_bits_match_confirmation", transfer_bits == confirmation_bits,
          transfer_bits=transfer_bits)
    target_transfer_checks = []
    for bit in confirmation_bits:
        item = transfers[str(bit)]
        root = hex128(canon(child | (1 << bit)))
        target_transfer_checks.append({
            "bit": bit, "root_canon": root, "claim_root_canon": item["root_canon"],
            "canon_match": root == item["root_canon"], "verdict": item["verdict"],
        })
    check("all_target_transfer_canons_and_verdict_labels",
          all(x["canon_match"] and x["verdict"] == "REFUTED-D10" for x in target_transfer_checks),
          count=len(target_transfer_checks))

    source_specs = {
        5: ("cost69j", 3), 13: ("cost64d", 3), 14: ("cost72d", 3),
        20: ("cost64h", 3), 34: ("cost73j", 3), 46: ("cost73i", 3),
        97: ("cost71e", 87), 103: ("cost66i", 33), 108: ("cost66j", 87),
        110: ("cost73k", 33), 115: ("cost70b", 48), 118: ("cost73l", 87),
    }
    source_checks = []
    maps = census["new_verdict_maps"]
    for target_bit, (name, source_bit) in source_specs.items():
        transfer = transfers[str(target_bit)]
        if name == "cost64d":
            source_mask = int(cost64d["s6_child"], 16) | (1 << source_bit)
            target_mask = child | (1 << target_bit)
            verdict_ok = source_bit in cost64d["results"]["refuted_d10_bits"]
            root_relation_ok = source_mask == target_mask and hex128(source_mask) == transfer["root_canon"]
            relation = "raw-identical"
        elif name == "cost70b":
            source_mask = int(cost70b["s6_child_hex"], 16) | (1 << source_bit)
            records = [r for r in batch5 if r.get("bit") == source_bit]
            verdict_ok = (len(records) == 1 and records[0].get("loss") is False
                          and records[0].get("capped") is False)
            root_relation_ok = hex128(canon(source_mask)) == transfer["root_canon"]
            relation = "D4-canon-equal"
        else:
            source = maps[name]
            source_mask = int(source["child"], 16) | (1 << source_bit)
            verdict_ok = source_bit in source["refuted_d10_bits"]
            root_relation_ok = hex128(canon(source_mask)) == transfer["root_canon"]
            relation = "D4-canon-equal"
        source_checks.append({
            "target_bit": target_bit, "source": name, "source_bit": source_bit,
            "verdict_ok": verdict_ok, "canon_or_identity_ok": root_relation_ok,
            "identity": relation,
        })
    check("all_12_transfer_sources_verified",
          len(source_checks) == 12 and all(x["verdict_ok"] and x["canon_or_identity_ok"] for x in source_checks),
          count=len(source_checks), checks=source_checks)

    selected = census["selected_target"]
    census_ok = (
        selected["s6_hex"] == claim["s6_child"]
        and selected["cost"] == 78
        and selected["legal_candidates"] == 78
        and selected["demand"] == claim["demand"]
        and sorted(selected["sweep_bits"]) == open_bits
        and sorted(x["bit"] for x in selected["confirmation_bits"]) == confirmation_bits
    )
    check("census_selection_matches_claim", census_ok, chain_head=census["chain_head"],
          selected=selected["s6_hex"])
    check("confirmation_prediction_all_refuted",
          all(v == "REFUTED-D10" for v in claim["engine_candidate_bits"]["confirmation_verdicts_predicted"].values()))
    check("k0868_definition_pin_and_terms",
          all(term in k0868_text for term in ("det4", "own_candidates", "共線")))

    input_pins = {
        "claim": {"path": f"{EXPERIMENT.relative_to(ROOT)}/output/{PINS['claim'][0]}", "git_blob_sha": PINS["claim"][1]},
        "census": {"path": f"{EXPERIMENT.relative_to(ROOT)}/output/{PINS['census'][0]}", "git_blob_sha": PINS["census"][1]},
        "cost64d": {"path": f"{EXPERIMENT.relative_to(ROOT)}/output/{PINS['cost64d'][0]}", "git_blob_sha": PINS["cost64d"][1]},
        "cost70b": {"path": f"{EXPERIMENT.relative_to(ROOT)}/output/{PINS['cost70b'][0]}", "git_blob_sha": PINS["cost70b"][1]},
        "batch5": {"path": f"{EXPERIMENT.relative_to(ROOT)}/output/{PINS['cost70b_batch5'][0]}", "git_blob_sha": PINS["cost70b_batch5"][1]},
        "k0868": {"path": K0868[0], "git_blob_sha": K0868[1]},
    }
    result = {
        "schema": "n11-cost78c-claim-structure-audit-20261118-v1",
        "date": "2026-11-18",
        "base_main_before_publication": BASE_MAIN,
        "input_pins": input_pins,
        "method": {
            "geometry": "K0868: exact det4 != 0 for every triple of the six stones; det4=0 excludes a cell",
            "symmetry": "D4 minimum over all eight square transforms",
            "scope": "claim structure and transfer provenance only; no depth-10 search and no new verdict",
        },
        "child": {"hex": claim["s6_child"], "stone_bits": stones},
        "geometry": {
            "triple_count": len(triples), "empty_cells": 115,
            "legal_candidates": len(legal), "forbidden_cells": len(forbidden),
            "legal_candidate_bits": legal, "forbidden_witnesses": forbidden,
        },
        "partition": {
            "open_bits": open_bits, "confirmation_bits": confirmation_bits,
            "disjoint": True, "union_count": len(union),
        },
        "target_transfers": target_transfer_checks,
        "source_provenance": source_checks,
        "census_selection": {
            "chain_head": census["chain_head"], "selected_target": selected["s6_hex"],
            "edge_cost": selected["cost"], "demand": selected["demand"],
        },
        "checks": checks,
        "all_pass": True,
        "failures": [],
        "interpretation_guard": (
            "Structural audit only. No depth-10 search was run, no WIN/LOSS verdict was created, "
            "no certificate or receipt was changed. REFUTED-D10 is not a LOSS proof; standard 11x11 remains UNKNOWN."
        ),
    }
    target = OUT / "class2-lane-cost78c-claim-structure-audit-20261118.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "all_pass": True, "legal": len(legal), "forbidden": len(forbidden),
        "open": len(open_bits), "confirmation": len(confirmation_bits),
        "target_canons": len(target_transfer_checks), "source_provenance": len(source_checks),
        "output": str(target),
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
