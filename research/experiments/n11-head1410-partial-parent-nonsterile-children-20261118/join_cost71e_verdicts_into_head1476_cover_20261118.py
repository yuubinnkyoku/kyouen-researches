#!/usr/bin/env python3
"""Join the complete cost71e D10 sweep to the head1476 757-root cover universe.

Uses only Python's standard library.  Every input is pinned by Git blob SHA-1.
This is a bookkeeping/geometry audit; it does not run the game solver.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output"
LANE = ROOT / "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output"

INPUTS = {
    "membership": (
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/minimum-cover-root-membership-20261118.json",
        "ab1e655f4a89a677e57515cdbacfe56894323013",
    ),
    "top15_audit": (
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/head1476-class2-top15-verdict-aware-cover-audit-20261118.json",
        "4fd00ae75658021d7a735bf1bd9823ed96cdc9d3",
    ),
    "cost71e_claim": (
        "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71e-inflight-20261117.json",
        "3ca1c69864f5c3d63b48ea6d96bc21f45ba06299",
    ),
    "cost71e_raw_audit": (
        "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71e-raw-sweep-audit-20261117.json",
        "9f56bdb74a71ef5a647432409ffd76928702870a",
    ),
    "cost71e_certificate_manifest": (
        "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71e-certificates/class2-lane-cost71e-win7-certificates-20261117.json",
        "a9ddec439e1931614679c2575e4adeb5fe770d2b",
    ),
}

RAW_BATCH_PINS = {
    1: "d8f279c49c59ae9990590543bfcb92762a15dbff",
    2: "068c78522d763e685e90901f2fa455e8d08af5fe",
    3: "b328ef87c9470bcdcfe752306a54859a8c9d764f",
    4: "1655120dd13423b6a65e951721271a1c32e19f7f",
    5: "7e3afdd181e9a68c235a27100dd8bc1003513f81",
    6: "7f2e1fe078468357112a22bf0a08494b14138d38",
    7: "7c1519eadea48b1a32f4cb8663d4ceaf78d8be3c",
    8: "37d0ed0a1217332a62635af16de808df0571eb14",
    9: "bc384419ba2b8f8b0f55ef2a234f22c68c069bb6",
}
CHILD = "00000000000000c09002000000002000"
EXPECTED_TOP15_UNCLASSIFIED = {
    "00000000200000003801000080000001": 1,
    "00000000000041801202000000080000": 3,
    "00000000000000c09002000000002200": 8,
}
EXPECTED_NODE_TOTAL = 88_919_559


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load_pinned_json(name: str) -> tuple[dict, str]:
    rel, expected = INPUTS[name]
    raw = (ROOT / rel).read_bytes()
    actual = git_blob_sha(raw)
    if actual != expected:
        raise AssertionError(f"{name} blob mismatch: {actual} != {expected}")
    return json.loads(raw), actual


def d4(mask: int, transform: int) -> int:
    out = 0
    for p in range(121):
        if not ((mask >> p) & 1):
            continue
        x, y = p % 11, p // 11
        xy = (
            (x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
            (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x),
        )[transform]
        out |= 1 << (11 * xy[1] + xy[0])
    return out


def canon(mask: int) -> str:
    return f"{min(d4(mask, t) for t in range(8)):032x}"


def count_covers(
    roots: list[str], masks: dict[str, int], full_mask: int,
    allowed_roots: set[str], forced_roots: tuple[str, ...] = (),
) -> int:
    forced = tuple(dict.fromkeys(forced_roots))
    if len(forced) > 6 or any(r not in allowed_roots for r in forced):
        return 0
    initial = 0
    for root in forced:
        initial |= masks[root]
    need = 6 - len(forced)
    dp = [[0] * (full_mask + 1) for _ in range(need + 1)]
    dp[0][initial] = 1
    for root in sorted(allowed_roots - set(forced)):
        rm = masks[root]
        for k in range(need - 1, -1, -1):
            row = dp[k]
            nxt = dp[k + 1]
            for m, value in enumerate(row):
                if value:
                    nxt[m | rm] += value
    return dp[need][full_mask]


def main() -> None:
    loaded = {name: load_pinned_json(name) for name in INPUTS}
    membership = loaded["membership"][0]
    prior = loaded["top15_audit"][0]
    claim = loaded["cost71e_claim"][0]
    raw_audit = loaded["cost71e_raw_audit"][0]
    cert_manifest = loaded["cost71e_certificate_manifest"][0]

    rows_data = membership["derived"]["all_root_memberships"]
    roots = [x["root"] for x in rows_data]
    if len(roots) != 757 or len(set(roots)) != 757:
        raise AssertionError("expected 757 distinct D4 roots")
    target_rows = sorted({r for x in rows_data for r in x["cover_rows"]})
    if len(target_rows) != 11:
        raise AssertionError(f"expected 11 S6 rows, got {len(target_rows)}")
    row_index = {r: i for i, r in enumerate(target_rows)}
    masks = {
        x["root"]: sum(1 << row_index[r] for r in x["cover_rows"])
        for x in rows_data
    }
    if any(mask == 0 or mask.bit_count() > 2 for mask in masks.values()):
        raise AssertionError("candidate root must cover one or two target rows")
    full_mask = (1 << len(target_rows)) - 1

    if claim["schema"] != "n11-class2-lane-cost71e-inflight-20261117-v3":
        raise AssertionError("unexpected cost71e claim schema")
    if claim["s6_child"] != CHILD or claim["candidate_count"] != 71:
        raise AssertionError("cost71e child/candidate count mismatch")
    legal = set(claim["legal_candidates"])
    if len(legal) != 71:
        raise AssertionError("cost71e legal candidate list is not 71 unique bits")
    if raw_audit["verdicts"]["capped_count"] != 0:
        raise AssertionError("cost71e raw audit reports capped candidates")
    if raw_audit["rawPins"] != claim["actual_execution"]["raw_outputs"]["raw_batch_blob_pins"]:
        raise AssertionError("claim/raw-audit raw batch pins differ")
    if raw_audit["verdicts"]["win7_d10_bits"] != claim["actual_execution"]["results"]["win7_d10_bits"]:
        raise AssertionError("claim/raw-audit WIN bit lists differ")

    bit_rows: dict[int, dict] = {}
    pilots = []
    batch_summaries = []
    for batch in range(1, 10):
        rel = (
            "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/"
            f"class2-lane-cost71e-raw-batch{batch}-20261117.jsonl"
        )
        raw = (ROOT / rel).read_bytes()
        actual = git_blob_sha(raw)
        if actual != RAW_BATCH_PINS[batch]:
            raise AssertionError(f"raw batch {batch} blob mismatch: {actual}")
        local_bits = []
        local_nodes = 0
        for line_no, line in enumerate(raw.splitlines(), 1):
            record = json.loads(line)
            if record.get("control") == "pilot_d6":
                if record != {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}:
                    raise AssertionError(f"batch {batch} pilot mismatch")
                pilots.append({"batch": batch, **record})
                continue
            if "bit" not in record:
                raise AssertionError(f"unrecognized raw record in batch {batch}, line {line_no}")
            bit = record["bit"]
            if bit not in legal or bit in bit_rows:
                raise AssertionError(f"unexpected/duplicate candidate bit {bit}")
            if record.get("capped") is not False or record.get("andclose") is not True:
                raise AssertionError(f"candidate bit {bit} is capped or not andclose")
            if record.get("terminalStoneRange") != [13, 17]:
                raise AssertionError(f"candidate bit {bit} terminal range mismatch")
            if not isinstance(record.get("nodes"), int) or record["nodes"] <= 0:
                raise AssertionError(f"candidate bit {bit} has invalid node count")
            raw_root = int(CHILD, 16) | (1 << bit)
            if raw_root.bit_count() != 7:
                raise AssertionError(f"candidate bit {bit} does not make a 7-stone root")
            root = canon(raw_root)
            if root not in masks:
                raise AssertionError(f"cost71e bit {bit} canon is outside the 757-root universe")
            verdict = "WIN7-D10" if record["loss"] is True else "REFUTED-D10"
            bit_rows[bit] = {
                "batch": batch,
                "bit": bit,
                "raw_root": f"{raw_root:032x}",
                "d4_canon_root": root,
                "verdict": verdict,
                "nodes": record["nodes"],
                "capped": record["capped"],
                "andclose": record["andclose"],
                "terminal_stone_range": record["terminalStoneRange"],
            }
            local_bits.append(bit)
            local_nodes += record["nodes"]
        batch_summaries.append({
            "batch": batch,
            "candidate_bits": sorted(local_bits),
            "candidate_count": len(local_bits),
            "candidate_nodes": local_nodes,
            "git_blob_sha1": actual,
        })

    if set(bit_rows) != legal:
        raise AssertionError(f"raw bit coverage mismatch: missing={sorted(legal-set(bit_rows))}")
    if len(pilots) != 9 or any(p["nodes"] != 3402 or p["loss"] for p in pilots):
        raise AssertionError("pilot control coverage mismatch")
    if len({x["d4_canon_root"] for x in bit_rows.values()}) != 71:
        raise AssertionError("cost71e raw candidates collide under D4")
    if len({x["d4_canon_root"] for x in bit_rows.values()} & set(masks)) != 71:
        raise AssertionError("not all 71 raw roots map into the target universe")

    wins = sorted(bit for bit, x in bit_rows.items() if x["verdict"] == "WIN7-D10")
    refuted = sorted(bit for bit, x in bit_rows.items() if x["verdict"] == "REFUTED-D10")
    candidate_nodes = sum(x["nodes"] for x in bit_rows.values())
    if wins != sorted(raw_audit["verdicts"]["win7_d10_bits"]):
        raise AssertionError("raw batch WIN bits differ from raw audit")
    if refuted != sorted(raw_audit["verdicts"]["refuted_d10_bits"]):
        raise AssertionError("raw batch REFUTED bits differ from raw audit")
    if (len(wins), len(refuted), candidate_nodes) != (13, 58, EXPECTED_NODE_TOTAL):
        raise AssertionError("cost71e verdict/node totals mismatch")
    if candidate_nodes + sum(p["nodes"] for p in pilots) != 88_950_177:
        raise AssertionError("cost71e total node count including pilots mismatch")

    certs = cert_manifest["certificates"]
    if len(certs) != 13 or sorted(x["bit"] for x in certs) != wins:
        raise AssertionError("cost71e certificate manifest does not cover exactly 13 WIN bits")
    for cert in certs:
        bit = cert["bit"]
        row = bit_rows[bit]
        if cert["d4_canon_root"] != row["d4_canon_root"]:
            raise AssertionError(f"certificate D4 root mismatch for bit {bit}")
        if cert["subroots"] != cert["subroots_pass"]:
            raise AssertionError(f"certificate subroot verification incomplete for bit {bit}")
        if cert["union_missing"] != 0 or cert["union_extra"] != 0:
            raise AssertionError(f"certificate union mismatch for bit {bit}")
        if cert["terminal_stone_range"] != [13, 17]:
            raise AssertionError(f"certificate terminal range mismatch for bit {bit}")

    top15 = prior["derived"]["top15"]
    if len(top15) != 15:
        raise AssertionError("top15 audit does not contain 15 roots")
    top_by_root = {x["root"]: x for x in top15}
    if len(top_by_root) != 15:
        raise AssertionError("duplicate root in top15")
    initial_counts = {
        "REFUTED-D10": sum(x["status"] == "REFUTED-D10" for x in top15),
        "WIN7-D10": sum(x["status"] == "WIN7-D10" for x in top15),
        "NOT_CLASSIFIED": sum(x["status"] == "NOT_CLASSIFIED_BY_PINNED_STATUS_SOURCES" for x in top15),
    }
    if initial_counts != {"REFUTED-D10": 10, "WIN7-D10": 2, "NOT_CLASSIFIED": 3}:
        raise AssertionError(f"unexpected prior top15 status counts: {initial_counts}")

    joined = []
    for entry in top15:
        raw = next((x for x in bit_rows.values() if x["d4_canon_root"] == entry["root"]), None)
        if raw is None:
            continue
        if entry["status"] not in ("NOT_CLASSIFIED_BY_PINNED_STATUS_SOURCES", raw["verdict"]):
            raise AssertionError(f"top15 status conflict at rank {entry['rank']}")
        joined.append({
            "rank": entry["rank"],
            "root": entry["root"],
            "prior_status": entry["status"],
            "joined_status": raw["verdict"],
            "cost71e_bit": raw["bit"],
            "raw_root": raw["raw_root"],
            "batch": raw["batch"],
            "nodes": raw["nodes"],
            "membership": entry["membership"],
        })

    newly = [x for x in joined if x["prior_status"] == "NOT_CLASSIFIED_BY_PINNED_STATUS_SOURCES"]
    if {x["root"]: x["rank"] for x in newly} != EXPECTED_TOP15_UNCLASSIFIED:
        raise AssertionError("cost71e did not resolve exactly the three previously unclassified top15 roots")
    if any(x["joined_status"] != "REFUTED-D10" for x in newly):
        raise AssertionError("a previously unclassified top15 root did not join as REFUTED-D10")

    final_top15 = []
    for entry in top15:
        raw = next((x for x in bit_rows.values() if x["d4_canon_root"] == entry["root"]), None)
        status = raw["verdict"] if raw else entry["status"]
        if status == "NOT_CLASSIFIED_BY_PINNED_STATUS_SOURCES":
            raise AssertionError("top15 still contains an unclassified root")
        final_top15.append({
            "rank": entry["rank"],
            "root": entry["root"],
            "membership": entry["membership"],
            "legal_replies": entry["legal_replies"],
            "status": status,
            "cost71e_bit": raw["bit"] if raw else None,
            "cost71e_batch": raw["batch"] if raw else None,
            "cost71e_nodes": raw["nodes"] if raw else None,
        })

    ref_roots = {x["root"] for x in final_top15 if x["status"] == "REFUTED-D10"}
    win_roots = {x["root"] for x in final_top15 if x["status"] == "WIN7-D10"}
    if (len(ref_roots), len(win_roots)) != (13, 2):
        raise AssertionError("final top15 must contain 13 REFUTED and 2 WIN roots")

    all_roots = set(roots)
    top_roots = set(top_by_root)
    base_covers = count_covers(roots, masks, full_mask, all_roots)
    covers_avoiding_top15 = count_covers(roots, masks, full_mask, all_roots - top_roots)
    if base_covers != 359_610 or covers_avoiding_top15 != 0:
        raise AssertionError("base minimum-cover count or top15 hitting-set property mismatch")

    old_ref_roots = {x["root"] for x in top15 if x["status"] == "REFUTED-D10"}
    old_win_roots = {x["root"] for x in top15 if x["status"] == "WIN7-D10"}
    old_allowed = all_roots - old_ref_roots
    old_total = count_covers(roots, masks, full_mask, old_allowed)
    old_no_win = count_covers(roots, masks, full_mask, old_allowed - old_win_roots)
    unknown_roots = [x["root"] for x in top15 if x["status"] == "NOT_CLASSIFIED_BY_PINNED_STATUS_SOURCES"]
    old_unknown_forced = {
        root: count_covers(roots, masks, full_mask, old_allowed - old_win_roots, (root,))
        for root in unknown_roots
    }
    old_unknown_pair = count_covers(
        roots, masks, full_mask, old_allowed - old_win_roots, tuple(unknown_roots[:2])
    )
    if (old_total, old_no_win) != (38_265, 13_275):
        raise AssertionError("prior 10-refuted-root cover counts do not reproduce")
    if set(old_unknown_forced.values()) != {4_425} or old_unknown_pair != 0:
        raise AssertionError("prior no-WIN residual partition mismatch")

    rank8_root = next(x["root"] for x in top15 if x["rank"] == 8)
    ref11 = old_ref_roots | {rank8_root}
    allowed11 = all_roots - ref11
    no_win11 = count_covers(roots, masks, full_mask, allowed11 - old_win_roots)
    if no_win11 != 8_850:
        raise AssertionError("one-root intermediate no-WIN residual mismatch")

    allowed_final = all_roots - ref_roots
    final_total = count_covers(roots, masks, full_mask, allowed_final)
    final_no_win = count_covers(roots, masks, full_mask, allowed_final - win_roots)
    win_list = sorted(win_roots)
    if len(win_list) != 2:
        raise AssertionError("expected two known WIN roots")
    both = count_covers(roots, masks, full_mask, allowed_final, tuple(win_list))
    with_each = {
        root: count_covers(roots, masks, full_mask, allowed_final, (root,))
        for root in win_list
    }
    only_each = {root: with_each[root] - both for root in win_list}
    if (
        final_total != 14_496 or final_no_win != 0 or both != 5_196
        or sorted(only_each.values()) != [4_425, 4_875]
    ):
        raise AssertionError("final verdict-aware cover counts mismatch")

    matches = []
    for bit in sorted(bit_rows):
        x = bit_rows[bit]
        universe = next(r for r in rows_data if r["root"] == x["d4_canon_root"])
        matches.append({
            **x,
            "cover_membership": universe["membership"],
            "cover_rows": universe["cover_rows"],
            "top15_rank": top_by_root[x["d4_canon_root"]]["rank"] if x["d4_canon_root"] in top_by_root else None,
        })

    output = {
        "schema": "n11-head1476-cost71e-full-universe-verdict-join-20261118-v1",
        "date": "2026-11-18",
        "source_main_commit": "c56d630bd7e6a7e981de54073a5fd22f79c801cc",
        "target_parent": "00000000000000403800000008000000",
        "target_s6_rows": 11,
        "candidate_root_universe": {
            "distinct_d4_roots": 757,
            "cost71e_sweep_roots_joined": 71,
            "cost71e_joined_fraction": "71/757",
            "cost71e_win7_d10": 13,
            "cost71e_refuted_d10": 58,
            "cost71e_capped": 0,
            "candidate_nodes": candidate_nodes,
            "total_nodes_including_pilots": candidate_nodes + 9 * 3402,
            "certificate_manifest": {
                "path": INPUTS["cost71e_certificate_manifest"][0],
                "blob_sha1": loaded["cost71e_certificate_manifest"][1],
                "certificates": len(certs),
                "all_subroots_pass": all(x["subroots"] == x["subroots_pass"] for x in certs),
                "all_unions_exact": all(x["union_missing"] == 0 and x["union_extra"] == 0 for x in certs),
            },
            "raw_batches": batch_summaries,
            "matched_roots": matches,
        },
        "top15_status": {
            "prior_counts": initial_counts,
            "newly_classified": newly,
            "final_counts": {"REFUTED-D10": len(ref_roots), "WIN7-D10": len(win_roots), "UNKNOWN": 0},
            "final_roots": final_top15,
            "hitting_set": {
                "minimum_cover_count": base_covers,
                "covers_avoiding_all_top15": covers_avoiding_top15,
            },
        },
        "minimum_cover_counts": {
            "base_minimum_covers": base_covers,
            "after_prior_10_refuted_top15": {
                "covers_avoiding_refuted": old_total,
                "covers_with_known_win": old_total - old_no_win,
                "covers_without_known_win": old_no_win,
                "no_win_residual_per_unknown_root": old_unknown_forced,
                "pairwise_intersection_first_two_unknown_roots": old_unknown_pair,
            },
            "after_rank8_refuted": {
                "covers_avoiding_11_refuted": count_covers(roots, masks, full_mask, allowed11),
                "covers_without_known_win": no_win11,
            },
            "after_all_13_refuted_top15": {
                "covers_avoiding_refuted": final_total,
                "covers_without_either_known_win": final_no_win,
                "covers_containing_both_known_wins": both,
                "covers_containing_each_known_win": with_each,
                "covers_containing_only_each_known_win": only_each,
                "interpretation": "All surviving six-root covers contain at least one of the two known WIN7-D10 roots; the other roots in these covers are not thereby proven WIN.",
            },
        },
        "receipt_fold": {
            "cost71e_status": claim["receipt_fold"]["status"],
            "closed_manifest_rows_by_this_join": 0,
            "note": "The 13 certificates are published, but this audit does not fold them into the S6 manifest. The cost71e claim still lists the cost76c, cost66i, cost66j and cost69j fold dependencies.",
        },
        "source_blob_pins": {
            **{name: sha for name, (_, sha) in INPUTS.items()},
            "cost71e_raw_batch_blobs": {str(k): v for k, v in RAW_BATCH_PINS.items()},
        },
        "checks": {
            "membership_757_distinct_roots": len(roots) == 757 and len(set(roots)) == 757,
            "eleven_target_rows": len(target_rows) == 11,
            "all_757_roots_cover_at_most_two_rows": all(m.bit_count() <= 2 for m in masks.values()),
            "cost71e_71_of_71_raw_bits": len(bit_rows) == 71 and set(bit_rows) == legal,
            "cost71e_71_of_71_d4_roots_in_universe": len(matches) == 71,
            "cost71e_13_win_58_refuted_zero_capped": (len(wins), len(refuted)) == (13, 58),
            "cost71e_13_certificates_exact_union": len(certs) == 13 and all(x["union_missing"] == x["union_extra"] == 0 for x in certs),
            "three_prior_unknown_top15_roots_now_refuted": len(newly) == 3 and all(x["joined_status"] == "REFUTED-D10" for x in newly),
            "top15_fully_classified": len(final_top15) == 15 and not any(x["status"].startswith("NOT_CLASSIFIED") for x in final_top15),
            "top15_hitting_set_reproduced": covers_avoiding_top15 == 0,
            "post_filter_all_survivors_include_known_win": final_total == 14_496 and final_no_win == 0,
            "no_verdict_conflict": True,
        },
        "interpretation_guard": (
            "This is a join of already published cost71e raw verdicts/certificates to a separate "
            "757-root minimum-cover universe. It creates no new game-engine verdict and does not "
            "close an S6 manifest row. REFUTED-D10 is not a LOSS proof. The 14,496 covers are only "
            "those avoiding the 13 REFUTED roots among the top15; other roots in them may remain "
            "unclassified or may have statuses outside this audit. The standard 11x11 empty board, "
            "two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
        ),
    }
    if not all(output["checks"].values()):
        raise AssertionError("one or more output checks failed")
    output["check_count"] = len(output["checks"])
    output["all_pass"] = True
    output["script_blob_sha1"] = git_blob_sha(Path(__file__).read_bytes())
    out_path = OUT / "head1476-cost71e-full-universe-verdict-join-20261118.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(out_path.relative_to(ROOT)),
        "all_pass": output["all_pass"],
        "checks": output["check_count"],
        "candidate_roots_joined": len(matches),
        "top15": output["top15_status"]["final_counts"],
        "surviving_minimum_covers": final_total,
        "without_known_win": final_no_win,
        "script_blob_sha1": output["script_blob_sha1"],
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
