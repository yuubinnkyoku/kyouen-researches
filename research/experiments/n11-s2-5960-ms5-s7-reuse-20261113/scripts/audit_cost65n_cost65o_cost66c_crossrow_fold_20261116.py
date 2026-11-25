#!/usr/bin/env python3
"""Independent D4 cross-row and fold-consistency audit for the n11 class-2 lane.

Run from any directory:
  python3 research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost65n_cost65o_cost66c_crossrow_fold_20261116.py

All inputs are blob-pinned. The audit does not run the game engine or verify
certificate bodies; it independently re-derives D4 candidate intersections,
the seven receipt cover sets, and the arithmetic/joins of the published fold.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
SOURCE_MAIN_COMMIT = "fcbd795d9223aff9acb25dd3744450260cc04a98"

INPUTS = {
    "cost65o": ("class2-lane-cost65o-inflight-20261116.json", "18c49eb010e0f464f5b7874c5ffbfb0ae34b67bb"),
    "cost65nFold": ("class-frontier-cost65n-receipts-recompute-20261116.json", "7390c540836d5e8440833aec9b4ac014fd96dd44"),
    "cost66cClaim": ("class2-lane-cost66c-inflight-20261116.json", "5e89637b748cbc70838723edbbfeda907af78da5"),
    "cost66cManifest": ("class2-lane-cost66c-win7-certificates-20261116.json", "463ed0f0aafbf6e21eadc1b7edf1e20051ec7efb"),
    "cost66cFold": ("class-frontier-cost66c-receipts-recompute-20261116.json", "8783993e5c73cc9697c3ca48aef981725f422be8"),
    "cost66cPrereg": ("class2-lane-cost66c-fold-preregistration-20261116.json", "809ad05e1bc560b1086c3d30cc34ad78727e430a"),
    "cost66cProjection": ("class2-lane-fold-projection-basis1444-7roots-20261116.json", "da8cab2f25f0adc4469d09ae1cabf54bf63d9324"),
    "cost66cBatch4": ("class2-lane-cost66c-raw-batch4-20261116.jsonl", "5ff20e15a8d892e930bda28b3198765b9e0d6f57"),
    "cost66cRawAudit": ("class2-lane-cost66c-raw-sweep-audit-20261116.json", "0854b2e2c6a4bde39405ce0954b966a31ce7f3e7"),
}
EXPECTED_V3_BLOB = "6dd3091362dc3d11febd1be020e173fb6df21173"
EXPECTED_CROSS_CANON = "00000000000000a09002080080000000"
EXPECTED_WIN_BITS = [73, 75, 79, 87, 96, 97, 112]


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def read_pinned(key: str) -> bytes:
    filename, expected = INPUTS[key]
    data = (OUT / filename).read_bytes()
    got = git_blob_sha(data)
    assert got == expected, f"{key}: blob mismatch {got} != {expected}"
    return data


def hx(mask: int) -> str:
    return f"{mask:032x}"


def popcount(mask: int) -> int:
    return mask.bit_count()


def d4_canon(mask: int) -> int:
    best = None
    for r in range(8):
        transformed = 0
        for p in range(121):
            if not ((mask >> p) & 1):
                continue
            x, y = p % 11, p // 11
            coords = (
                (x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
                (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x),
            )
            a, b = coords[r]
            transformed |= 1 << (11 * b + a)
        if best is None or transformed < best:
            best = transformed
    assert best is not None
    return best


def covers(root: int) -> list[str]:
    return sorted(
        hx(d4_canon(root ^ (1 << p)))
        for p in range(121)
        if (root >> p) & 1
    )


def candidate_map(claim: dict) -> dict[int, dict]:
    child = int(claim["s6_child"], 16)
    result = {}
    for bit in claim["legal_candidates"]:
        root = child | (1 << bit)
        canonical = d4_canon(root)
        assert canonical not in result, f"duplicate candidate D4 orbit at bit {bit}"
        result[canonical] = {"bit": bit, "root_hex": hx(root)}
    return result


def require(checks: list[dict], name: str, condition: bool, detail: str) -> None:
    checks.append({"name": name, "pass": bool(condition), "detail": detail})
    assert condition, f"{name}: {detail}"


def main() -> None:
    checks: list[dict] = []
    raw = {key: read_pinned(key) for key in INPUTS}
    data = {
        key: json.loads(value)
        for key, value in raw.items()
        if key != "cost66cBatch4"
    }
    batch4 = [json.loads(line) for line in raw["cost66cBatch4"].decode().splitlines() if line.strip()]
    source_blobs = {key: INPUTS[key][1] for key in INPUTS}

    cost65o = data["cost65o"]
    cost65n_fold = data["cost65nFold"]
    cost66c = data["cost66cClaim"]
    manifest = data["cost66cManifest"]
    fold = data["cost66cFold"]
    prereg = data["cost66cPrereg"]
    projection = data["cost66cProjection"]
    raw_audit = data["cost66cRawAudit"]

    require(checks, "cost-65o remains an active reservation",
            cost65o["status"].startswith("IN FLIGHT")
            and cost65o["candidate_count"] == 65
            and cost65o["open_candidate_count"] == 59,
            "status=IN FLIGHT; 65 legal, 59 open, six prior transfers")

    # v4 preserves v3's exact claim fields so the pre-correction state is recoverable.
    require(checks, "cost-66c claim is v4 fold-complete",
            cost66c["schema"] == "n11-class2-lane-cost66c-fold-complete-20261116-v4",
            cost66c["schema"])
    v3_fields = cost66c["fold"]["v3_fields"]
    restored_v3 = copy.deepcopy(cost66c)
    del restored_v3["fold"]["v3_fields"]
    for key in ("schema", "title", "status", "results", "supersedes"):
        restored_v3[key] = v3_fields[key]
    restored_bytes = (json.dumps(restored_v3, indent=1, ensure_ascii=False) + "\n").encode()
    restored_blob = git_blob_sha(restored_bytes)
    require(checks, "v3 claim restoration is byte-exact",
            restored_blob == EXPECTED_V3_BLOB,
            f"restored={restored_blob}; expected={EXPECTED_V3_BLOB}")

    map65o = candidate_map(cost65o)
    map66c = candidate_map(cost66c)
    require(checks, "candidate D4 orbits are unique within both rows",
            len(map65o) == 65 and len(map66c) == 66,
            f"cost65o={len(map65o)}/65; cost66c={len(map66c)}/66")

    intersections = set(map65o) & set(map66c)
    require(checks, "only cross-row candidate orbit is 66c bit83 == 65o bit43",
            len(intersections) == 1
            and hx(next(iter(intersections))) == EXPECTED_CROSS_CANON
            and map66c[next(iter(intersections))]["bit"] == 83
            and map65o[next(iter(intersections))]["bit"] == 43,
            str([(hx(c), map66c[c], map65o[c]) for c in intersections]))

    bit83 = [r for r in batch4 if r.get("bit") == 83]
    require(checks, "cost-66c bit83 is uncapped REFUTED-D10",
            len(bit83) == 1 and bit83[0]["loss"] is False
            and bit83[0]["capped"] is False and bit83[0]["nodes"] == 269856
            and bit83[0]["andclose"] is True,
            str(bit83[0] if bit83 else None))
    require(checks, "cost-65o bit43 is still open and not transferred",
            43 in cost65o["open_candidates_to_sweep"]
            and "43" not in cost65o["transferred_refuted_d10_bits"],
            "bit43 remains open in the active claim")

    revised_open = [b for b in cost65o["open_candidates_to_sweep"] if b != 43]
    revised_batches = {
        str(k): [b for b in cost65o["planned_batch_bit_lists"][str(k)] if b != 43]
        for k in range(1, 9)
    }
    flattened = [b for k in range(1, 9) for b in revised_batches[str(k)]]
    require(checks, "bit43 transfer reduces cost-65o to 58 open candidates",
            len(revised_open) == 58 and flattened == revised_open,
            f"open={len(revised_open)}; batch sizes={[len(revised_batches[str(k)]) for k in range(1, 9)]}")

    cost65n_roots = cost65n_fold["cost65n_additions"]
    canons65n = {d4_canon(int(x["root_hex"], 16)) for x in cost65n_roots}
    require(checks, "cost-65n receipt roots are mutually D4-distinct",
            len(canons65n) == 2, f"distinct={len(canons65n)}")
    require(checks, "cost-65n receipts do not overlap cost-65o candidates",
            all(c not in map65o for c in canons65n), "intersection=0")

    certs = manifest["certificates"]
    require(checks, "cost-66c manifest has the seven expected WIN7 roots",
            len(certs) == 7 and [c["bit"] for c in certs] == EXPECTED_WIN_BITS
            and all(c["verdict"] == "WIN7" for c in certs),
            str([c["bit"] for c in certs]))
    cert_canons = set()
    for cert in certs:
        root = int(cert["root_hex"], 16)
        expected_root = int(cost66c["s6_child"], 16) | (1 << cert["bit"])
        require(checks, f"bit{cert['bit']} root is child|1<<bit and seven stones",
                root == expected_root and popcount(root) == 7, cert["root_hex"])
        canonical = d4_canon(root)
        require(checks, f"bit{cert['bit']} D4 canonical matches manifest",
                hx(canonical) == cert["d4_canonical_hex"], hx(canonical))
        cert_canons.add(canonical)
    require(checks, "seven cost-66c WIN receipts are mutually D4-distinct",
            len(cert_canons) == 7, f"distinct={len(cert_canons)}")
    require(checks, "cost-66c WIN receipts do not overlap cost-65o candidates",
            all(c not in map65o for c in cert_canons), "intersection=0")
    require(checks, "cost-65n and cost-66c WIN receipts are D4-disjoint",
            canons65n.isdisjoint(cert_canons), "intersection=0")
    require(checks, "cost-66c bit83 is in the swept REFUTED-D10 list",
            83 in cost66c["results"]["refuted_d10_swept_bits"],
            "bit83 is REFUTED-D10, not a LOSS proof")

    subroots = sum(c["sub_roots"] for c in certs)
    rows = sum(c["rows"] for c in certs)
    extraction_nodes = sum(c["extraction_nodes"] for c in certs)
    split_count = sum(bool(c["published_cert"].get("parts")) for c in certs)
    require(checks, "all seven certificates have BigInt 0/0 and Bareiss pass",
            all(c["bigint_verify"]["union_missing"] == 0
                and c["bigint_verify"]["union_extra"] == 0
                and c["bareiss_verify"]["all_subroots_pass"] is True
                for c in certs),
            "BigInt union missing/extra 0/0; all Bareiss sub-roots pass")
    require(checks, "certificate totals are 348 sub-roots and five split filesets",
            subroots == 348 and split_count == 5,
            f"subroots={subroots}; split={split_count}")

    shared_fields = ("basis_head", "basis_head_numbers", "basis_roots", "basis_summary",
                     "projected_head", "demand_histogram_deltas", "affected_parents", "receipts")
    require(checks, "pre-registration and projection artifacts agree",
            all(prereg[k] == projection[k] for k in shared_fields),
            "all shared projection fields match")
    require(checks, "post-cost65n basis is head1444 with 764 roots",
            prereg["basis_head"] == 1444 and prereg["basis_roots"] == 764
            and prereg["basis_head_numbers"] == [1444, 174, 6404, 506746, 4677, 370660]
            and cost65n_fold["frontier_after_cost65n"]["solved_s6_in_manifest"] == 1444
            and len(cost65n_roots) == 2,
            "head1441 + two cost65n receipts reproduces the preregistration basis")

    pre_by_root = {r["root_hex"]: r for r in prereg["receipts"]}
    proj_by_root = {r["root_hex"]: r for r in projection["receipts"]}
    fold_by_bit = {r["bit"]: r for r in fold["cost66c_additions"]}
    marginal_union: set[str] = set()
    manifest_union: set[str] = set()
    marginal_total = 0
    manifest_total = 0
    for cert in certs:
        bit, root_hex = cert["bit"], cert["root_hex"]
        a, b, c = pre_by_root[root_hex], proj_by_root[root_hex], fold_by_bit[bit]
        require(checks, f"bit{bit} receipt exists in prereg/projection/fold",
                c["root_hex"] == root_hex, root_hex)
        expected_covers = covers(int(root_hex, 16))
        require(checks, f"bit{bit} seven D4-deletion covers independently reproduce",
                expected_covers == a["covers_hexes"] == b["covers_hexes"] == c["covers_hexes"],
                f"covers={len(expected_covers)}")
        require(checks, f"bit{bit} marginal fields agree across prereg/projection/fold",
                a["marginal_hexes"] == b["marginal_hexes"] == c["marginal_hexes"]
                and a["marginal_manifest_hexes"] == b["marginal_manifest_hexes"]
                == c["marginal_manifest_hexes"],
                f"marginal={c['marginal']}; manifest={c['marginal_in_manifest']}")
        for h in c["marginal_hexes"]:
            require(checks, f"marginal {h} belongs to its cover", h in expected_covers, h)
            require(checks, f"marginal {h} is unique across receipts",
                    h not in marginal_union, h)
            marginal_union.add(h)
        for h in c["marginal_manifest_hexes"]:
            require(checks, f"manifest marginal {h} belongs to marginal",
                    h in c["marginal_hexes"], h)
            manifest_union.add(h)
        marginal_total += c["marginal"]
        manifest_total += c["marginal_in_manifest"]

    require(checks, "seven receipts have 35 disjoint marginals and six manifest rows",
            marginal_total == 35 and len(marginal_union) == 35
            and manifest_total == 6 and len(manifest_union) == 6,
            f"marginal={marginal_total}/{len(marginal_union)}; manifest={manifest_total}/{len(manifest_union)}")
    closed_rows = sorted(fold["totals"]["rows_closed_hexes"])
    require(checks, "six manifest marginal rows equal the fold's six closed rows",
            sorted(manifest_union) == closed_rows
            and cost66c["s6_child"] in closed_rows, ",".join(closed_rows))
    require(checks, "child row is closed exactly once by bit73",
            fold["totals"]["child_closed_by_bit"] == 73
            and cost66c["s6_child"] in fold_by_bit[73]["marginal_manifest_hexes"],
            cost66c["s6_child"])

    lost = fold["lost_rows_per_parent"]
    incidence_count = sum(len(rows_by_hex) for rows_by_hex in lost.values())
    incidence_cost = sum(sum(rows_by_hex.values()) for rows_by_hex in lost.values())
    unique_row_costs: dict[str, int] = {}
    for rows_by_hex in lost.values():
        for row_hex, cost in rows_by_hex.items():
            assert row_hex not in unique_row_costs or unique_row_costs[row_hex] == cost
            unique_row_costs[row_hex] = cost
    duplicate_rows = [
        {"hex": row_hex, "cost": cost}
        for row_hex, cost in sorted(unique_row_costs.items())
        if sum(row_hex in rows_by_hex for rows_by_hex in lost.values()) > 1
    ]
    unique_global_delta = sum(unique_row_costs.values())
    require(checks, "parent deltas are six parents, eight incidences, and 596 incidence-cost",
            len(lost) == 6 and incidence_count == 8 and incidence_cost == 596
            and fold["totals"]["parent_row_incidences"] == 8
            and fold["totals"]["parent_edge_cost_delta"] == 596,
            f"parents={len(lost)}; incidences={incidence_count}; cost={incidence_cost}")
    require(checks, "unique six manifest rows carry 449 edge cost; duplicate incidences explain 147",
            len(unique_row_costs) == 6 and unique_global_delta == 449
            and incidence_cost - unique_global_delta == 147 and len(duplicate_rows) == 2,
            f"unique={unique_global_delta}; incidence={incidence_cost}; duplicates={duplicate_rows}")

    prereg_parents = prereg["affected_parents"]
    parents_after = fold["parents_after"]
    require(checks, "six affected-parent before/after summaries agree with preregistration",
            len(parents_after) == 6 and all(
                p in parents_after
                and parents_after[p]["rows_before"] == v["rows_before"]
                and parents_after[p]["rows"] == v["rows_after"]
                and parents_after[p]["edge_cost_before"] == v["edge_cost_before"]
                and parents_after[p]["edge_cost"] == v["edge_cost_after"]
                and len(lost[p]) == len(v["lost_rows_hexes"])
                and sum(lost[p].values()) == v["lost_edge_cost"]
                for p, v in prereg_parents.items()),
            "all six parent rows/costs match")

    before = prereg["basis_summary"]
    after = fold["frontier_after_cost66c"]
    projected = prereg["projected_head"]
    require(checks, "projected head is 1450/174/6398/506297/4671/370211",
            [after[k] for k in ("solved_s6_in_manifest", "remaining_s5_orbits",
                                "unique_remaining_s6", "sum_remaining_cost",
                                "s6_needed_by_open_classes", "cost_needed_by_open_classes")]
            == [1450, 174, 6398, 506297, 4671, 370211],
            str(after))
    require(checks, "global open-class cost falls by 449 while S5 orbit count stays 174",
            before["cost_needed_by_open_classes"] - after["cost_needed_by_open_classes"] == 449
            and before["remaining_s5_orbits"] == after["remaining_s5_orbits"] == 174
            and before["s6_needed_by_open_classes"] - after["s6_needed_by_open_classes"] == 6
            and before["unique_remaining_s6"] - after["unique_remaining_s6"] == 6,
            "six manifest rows removed; no S5 parent closed")
    require(checks, "fold conflict census is empty against the 764-root head1444 basis",
            fold["totals"]["conflict_census_overlaps"] == []
            and fold["totals"]["folded_roots_at_1444"]["receipt_roots"] == 764
            and fold["totals"]["folded_roots_at_1444"]["distinct_d4_canons"] == 749,
            str(fold["totals"]["folded_roots_at_1444"]))
    require(checks, "v4 claim points to the published manifest and preregistration",
            cost66c["fold"]["certificate_manifest"]["git_blob_sha"] == INPUTS["cost66cManifest"][1]
            and cost66c["fold"]["fold_preregistration"]["git_blob_sha"] == INPUTS["cost66cPrereg"][1],
            "manifest and preregistration blob pins match")
    require(checks, "v4 claim corrects stale certificate/fold result fields",
            cost66c["results"]["certificates_status"].startswith("published and dual-verified")
            and "folded" in cost66c["results"]["row_result"],
            "certificate status and row result are current")

    result = {
        "schema": "n11-class2-lane-cost65n-cost65o-cost66c-crossrow-fold-audit-20261116-v1",
        "date": "2026-11-16",
        "source_main_commit": SOURCE_MAIN_COMMIT,
        "source_blobs": source_blobs,
        "cross_row": {
            "cost65o": {
                "child_hex": cost65o["s6_child"],
                "legal_candidates": 65,
                "prior_transferred_refuted_d10": sorted(int(x) for x in cost65o["transferred_refuted_d10_bits"]),
                "open_before": 59,
                "new_transfer": {
                    "bit": 43,
                    "root_hex": map65o[next(iter(intersections))]["root_hex"],
                    "d4_canonical_hex": EXPECTED_CROSS_CANON,
                    "source": "cost-66c raw batch4 bit83, REFUTED-D10, 269856 nodes",
                },
                "open_after_transfer": 58,
                "open_bits_after_transfer": revised_open,
                "planned_batches_after_transfer": revised_batches,
                "batch_sizes_after_transfer": [len(revised_batches[str(k)]) for k in range(1, 9)],
            },
            "cost66c": {
                "child_hex": cost66c["s6_child"],
                "legal_candidates": 66,
                "win7_bits": EXPECTED_WIN_BITS,
                "win_receipt_canons": sorted(hx(c) for c in cert_canons),
                "cross_row_candidate_overlap_count": 1,
            },
            "only_cross_row_overlap": {
                "d4_canonical_hex": EXPECTED_CROSS_CANON,
                "cost66c_bit": 83,
                "cost66c_verdict": "REFUTED-D10",
                "cost66c_nodes": 269856,
                "cost65o_bit": 43,
                "cost65o_current_status": "OPEN",
            },
            "win_receipt_conflicts": {
                "cost65n_vs_cost65o": 0,
                "cost66c_vs_cost65o": 0,
                "cost65n_vs_cost66c": 0,
            },
            "required_cost65o_update": (
                "When the active cost-65o owner next updates its claim, add bit43 to "
                "transferred_refuted_d10_bits with this D4 canon and remove it from "
                "open_candidates_to_sweep. If an already-run or future 65o raw record "
                "reports WIN7-D10 for bit43, stop and investigate a WIN/REFUTED conflict."
            ),
        },
        "fold": {
            "basis_head": "1444/174/6404/506746/4677/370660",
            "new_head": "1450/174/6398/506297/4671/370211",
            "receipt_count": 7,
            "total_marginal": 35,
            "total_marginal_in_manifest": 6,
            "total_marginal_outside_manifest": 29,
            "manifest_rows_closed": closed_rows,
            "child_closed_by_bit": 73,
            "affected_parents": 6,
            "parent_row_incidences": 8,
            "parent_incidence_edge_cost_delta": 596,
            "unique_manifest_row_edge_cost_delta": 449,
            "duplicate_parent_incidence_cost": 147,
            "duplicate_rows": duplicate_rows,
            "remaining_s5_orbits": 174,
            "unique_remaining_s6": 6398,
            "s6_needed_by_open_classes": 4671,
            "cost_needed_by_open_classes": 370211,
        },
        "checks": checks,
        "all_pass": all(x["pass"] for x in checks),
        "limitations": [
            "This audit independently re-derives D4 candidate intersections and the seven receipt cover sets, and checks the published fold/projection artifacts field-by-field.",
            "It does not rerun the depth-10 engine, reparse the 11.2 MB certificate bodies, or independently reconstruct all 764 basis roots. The fold log records the separate basis reconstruction and seven-certificate re-verification.",
            "The cost-65o claim remains an active reservation; this audit does not modify it.",
        ],
        "interpretation_guard": (
            "REFUTED-D10 is not a LOSS proof. WIN7-D10 certificates apply only to their individual "
            "seven-stone roots. Manifest solved counts are coverage bookkeeping, not game-theoretic "
            "values. Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, "
            "and classes 1/2/4 remain UNKNOWN."
        ),
    }
    output = OUT / "class2-lane-cost65n-cost65o-cost66c-crossrow-fold-audit-20261116.json"
    output.write_text(json.dumps(result, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    print(f"PASS: {len(checks)} checks; only cross-row orbit is cost66c bit83 == cost65o bit43")
    print("cost65o open candidates after transfer:", len(revised_open))
    print("fold head:", result["fold"]["new_head"])
    print("output:", output.name)


if __name__ == "__main__":
    main()
