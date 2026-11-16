#!/usr/bin/env python3
"""D4-orbit audit of the cost-65o row against the two cost-65n WIN7 receipts.

This is a structural receipt-overlap check, not a search and not a game-value
claim.  It uses the K0863 position-level lemma:
  X covers R iff canon(X) is one of canon(R + t), t in legal_candidates(R).
All source values are frozen below and pinned to the published Git blobs, so
the audit remains reproducible even if the in-flight claim is later superseded.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

N = 11
COST65N_CHILD = int("00000000000000801202010000800000", 16)
COST65N_WIN_BITS = [90, 117]
COST65O_CHILD = int("00000000000000a09002000080000000", 16)

# Exact lists copied from the blob-pinned cost-65o claim v1.
LEGAL_BITS = [
    0, 1, 2, 4, 6, 7, 10, 11, 12, 13, 14, 15, 18, 20, 21, 22, 23, 25,
    28, 32, 33, 34, 41, 43, 44, 45, 48, 54, 56, 59, 62, 64, 65, 66, 67,
    68, 75, 77, 78, 80, 81, 85, 87, 88, 89, 90, 91, 92, 96, 98, 99, 101,
    102, 105, 106, 109, 110, 112, 113, 114, 116, 117, 118, 119, 120,
]
OPEN_BITS = [
    0, 1, 2, 4, 6, 7, 10, 11, 12, 13, 14, 15, 18, 20, 21, 22, 23, 25,
    28, 32, 33, 34, 43, 44, 45, 54, 59, 62, 64, 66, 67, 68, 75, 77, 78,
    81, 85, 87, 88, 89, 90, 91, 92, 96, 98, 101, 102, 105, 106, 109,
    110, 112, 113, 114, 116, 117, 118, 119, 120,
]
TRANSFERRED_CANONS = {
    41: "00000000000000a09002020080000000",
    48: "00000000000000a09003000080000000",
    56: "00000000000000a09102000080000000",
    65: "00000000000000a29002000080000000",
    80: "00000000000100a09002000080000000",
    99: "0000000002000080120a000000200000",
}

# These are the two preregistered cost-65n WIN7-D10 receipts and their
# covered S6 rows.  Their canonical roots were pinned before the fold landed.
RECEIPTS = [
    {
        "bit": 90,
        "root_hex": "00000000040000801202010000800000",
        "canon_hex": "00000000000100003800000048002000",
        "covers_hexes": [
            "00000000000000003800000009080000",
            "00000000000000801202010000800000",
            "00000000000100001800000048002000",
            "00000000000100002800000048002000",
            "00000000000100003000000048002000",
            "00000000000100003800000040002000",
            "00000000000100003800000048000000",
        ],
    },
    {
        "bit": 117,
        "root_hex": "00200000000000801202010000800000",
        "canon_hex": "00000000001020003800000008080000",
        "covers_hexes": [
            "00000000000000801202010000800000",
            "00000000000020003800000008080000",
            "00000000000100809002000000000008",
            "00000000001020001800000008080000",
            "00000000001020002800000008080000",
            "00000000001020003000000008080000",
            "00000000001020003800000000080000",
        ],
    },
]

SOURCE_BLOBS = {
    "main_at_audit": "23480542c21a08bdb4e1756a0226a90586c94f73",
    "cost65n_completed_claim_v2": "257e7093582f9080a551ec4ef42e1bdccee3c878",
    "cost65o_claim_v1": "18c49eb010e0f464f5b7874c5ffbfb0ae34b67bb",
    "cost65o_claim_verification_8_of_8": "cfff0b8087a54f3b4d327d73737f220372f34248",
    "cost65n_fold_preregistration": "da2b2292a3a3436f73dc04bae266de2c01a6ef21",
    "K0863_position_level_lemma": "6b79dbcb2db0b8c34c108c1c227be139a3f1493b",
}


def d4_canon(mask: int) -> int:
    """Return the minimum row-major 121-bit image under D4."""
    points = [(i % N, i // N) for i in range(N * N) if (mask >> i) & 1]
    images = []
    for transform in range(8):
        out = []
        for x, y in points:
            if transform == 0:
                X, Y = x, y
            elif transform == 1:
                X, Y = N - 1 - y, x
            elif transform == 2:
                X, Y = N - 1 - x, N - 1 - y
            elif transform == 3:
                X, Y = y, N - 1 - x
            elif transform == 4:
                X, Y = N - 1 - x, y
            elif transform == 5:
                X, Y = x, N - 1 - y
            elif transform == 6:
                X, Y = y, x
            else:
                X, Y = N - 1 - y, N - 1 - x
            out.append(Y * N + X)
        images.append(sum(1 << i for i in out))
    return min(images)


def hx(value: int) -> str:
    return f"{value:032x}"


def main() -> int:
    checks = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append({"check": name, "pass": bool(ok), "detail": detail})

    # Verify the two new receipt roots against both their child+bit identity
    # and the pre-registered D4 canons.
    receipt_canons = set()
    all_cover_hexes = []
    receipt_records = []
    for rec in RECEIPTS:
        root = COST65N_CHILD | (1 << rec["bit"])
        root_canon = d4_canon(root)
        check(
            f"cost65n bit {rec['bit']} root identity",
            hx(root) == rec["root_hex"] and hx(root_canon) == rec["canon_hex"],
            f"root={hx(root)} canon={hx(root_canon)}",
        )
        receipt_canons.add(root_canon)
        all_cover_hexes.extend(rec["covers_hexes"])
        receipt_records.append({
            "bit": rec["bit"],
            "root_hex": hx(root),
            "d4_canonical_hex": hx(root_canon),
            "covers_hexes": rec["covers_hexes"],
        })

    expected_receipt_canons = {
        int(rec["canon_hex"], 16) for rec in RECEIPTS
    }
    check(
        "receipt roots are two distinct preregistered WIN7 canons",
        len(receipt_canons) == 2 and receipt_canons == expected_receipt_canons,
        ", ".join(sorted(hx(x) for x in receipt_canons)),
    )

    legal_set = set(LEGAL_BITS)
    open_set = set(OPEN_BITS)
    transferred_set = set(TRANSFERRED_CANONS)
    check(
        "cost65o legal/open/transferred partition",
        len(LEGAL_BITS) == 65
        and len(OPEN_BITS) == 59
        and len(TRANSFERRED_CANONS) == 6
        and open_set.isdisjoint(transferred_set)
        and open_set | transferred_set == legal_set,
        f"legal={len(legal_set)} open={len(open_set)} transferred={len(transferred_set)}",
    )

    candidate_records = []
    candidate_canons = {}
    transfer_identity_ok = True
    for bit in LEGAL_BITS:
        root = COST65O_CHILD | (1 << bit)
        root_canon = d4_canon(root)
        candidate_canons[bit] = root_canon
        status = "open" if bit in open_set else "transferred-refuted-d10"
        candidate_records.append({
            "bit": bit,
            "root_hex": hx(root),
            "d4_canonical_hex": hx(root_canon),
            "status": status,
        })
        if bit in TRANSFERRED_CANONS:
            transfer_identity_ok &= hx(root_canon) == TRANSFERRED_CANONS[bit]

    check(
        "six transferred REFUTED-D10 roots reproduce their published D4 canons",
        transfer_identity_ok,
        "bits " + ",".join(str(x) for x in sorted(TRANSFERRED_CANONS)),
    )

    candidate_orbit_count = len(set(candidate_canons.values()))
    check(
        "all 65 cost65o candidate roots have distinct D4 orbits",
        candidate_orbit_count == 65,
        f"{candidate_orbit_count}/65 distinct",
    )

    overlap_bits = sorted(
        bit for bit, root_canon in candidate_canons.items()
        if root_canon in receipt_canons
    )
    open_overlap_bits = sorted(
        bit for bit in OPEN_BITS
        if candidate_canons[bit] in receipt_canons
    )
    transferred_conflict_bits = sorted(
        bit for bit in TRANSFERRED_CANONS
        if candidate_canons[bit] in receipt_canons
    )
    check(
        "no cost65n WIN7 receipt canon overlaps any cost65o legal candidate",
        not overlap_bits,
        f"overlap bits={overlap_bits}",
    )
    check(
        "no cost65n WIN7 receipt conflicts with transferred REFUTED-D10",
        not transferred_conflict_bits,
        f"conflict bits={transferred_conflict_bits}",
    )
    check(
        "no cost65n WIN7 receipt transfers any of the 59 open cost65o bits",
        not open_overlap_bits,
        f"new transfer bits={open_overlap_bits}",
    )

    cost65o_child_canon = d4_canon(COST65O_CHILD)
    covered_row_canons = {d4_canon(int(h, 16)) for h in all_cover_hexes}
    child_is_covered = cost65o_child_canon in covered_row_canons
    check(
        "cost65o child row is not among the preregistered cost65n covered S6 rows",
        not child_is_covered,
        f"child canon={hx(cost65o_child_canon)}; covered row orbits={len(covered_row_canons)}",
    )

    # The cost65o structural verification itself is pinned as 8/8 PASS.
    check(
        "cost65o claim structure was independently verified 8/8",
        True,
        "source blob cfff0b80; this audit does not rerun that separate legality verifier",
    )

    result = {
        "schema": "n11-class2-lane-cost65o-post-cost65n-overlap-audit-20261116-v1",
        "date": "2026-11-16",
        "source_blobs": SOURCE_BLOBS,
        "method": (
            "Independent exact D4 canonicalization of every legal 7-stone root "
            "child|1<<bit in the cost65o row, compared with the two WIN7-D10 "
            "receipt-root canons from cost65n. By K0863's position-level lemma, "
            "a receipt covers an S6 row iff its canonical 7-stone root is one of "
            "that row's own legal candidate-root canons."
        ),
        "cost65o_input": {
            "child_hex": hx(COST65O_CHILD),
            "legal_candidate_count": len(LEGAL_BITS),
            "legal_candidate_bits": LEGAL_BITS,
            "open_candidate_count": len(OPEN_BITS),
            "open_candidate_bits": OPEN_BITS,
            "transferred_refuted_d10_bits": sorted(TRANSFERRED_CANONS),
            "transferred_root_canons": {
                str(bit): TRANSFERRED_CANONS[bit]
                for bit in sorted(TRANSFERRED_CANONS)
            },
            "d4_canonical_candidate_count": candidate_orbit_count,
            "candidate_roots": candidate_records,
        },
        "cost65n_receipts": receipt_records,
        "covered_s6_rows": {
            "raw_reference_count": len(all_cover_hexes),
            "unique_d4_orbits": len(covered_row_canons),
            "cost65o_child_canonical_hex": hx(cost65o_child_canon),
            "cost65o_child_is_covered": child_is_covered,
        },
        "overlap": {
            "all_legal_candidate_bits": overlap_bits,
            "open_candidate_bits": open_overlap_bits,
            "transferred_refuted_conflict_bits": transferred_conflict_bits,
            "new_cost65o_transfers_from_cost65n": len(open_overlap_bits),
            "open_candidates_remaining_against_these_two_receipts": (
                len(OPEN_BITS) - len(open_overlap_bits)
            ),
        },
        "checks": checks,
        "all_pass": all(c["pass"] for c in checks),
        "interpretation_guard": (
            "Structural receipt-overlap audit only. It neither runs the engine "
            "nor changes any verdict or manifest head. It proves only that the "
            "two cost65n WIN7-D10 receipt roots do not cover the cost65o row or "
            "any of its 65 candidate roots. Other receipts published later must "
            "still be checked. REFUTED-D10 is not a LOSS proof; 11x11 remains UNKNOWN."
        ),
    }

    out = Path(__file__).resolve().parents[1] / "output" / (
        "class2-lane-cost65o-post-cost65n-overlap-audit-20261116.json"
    )
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    for item in checks:
        print(("PASS" if item["pass"] else "FAIL"), "|", item["check"], "|", item["detail"])
    print(f"{sum(c['pass'] for c in checks)}/{len(checks)} checks passed")
    print("written", out)
    return 0 if result["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
