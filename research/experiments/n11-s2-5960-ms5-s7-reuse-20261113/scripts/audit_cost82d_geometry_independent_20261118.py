#!/usr/bin/env python3
"""Independent geometry audit for the cost82d six-stone S6 child.

Uses a 24-term Leibniz determinant, independent of the repository's Bareiss
legal-candidate enumerator. Checks the complete survival-move set and D4
canonical forms of the 17 confirmation roots.
"""
from itertools import combinations, permutations
import json
from pathlib import Path

CLAIM_BLOB = "cffeda699c1ed0c0c9333c1b12124776f7297324"
K0868_BLOB = "b097210d0b49d7cf014cc6a554298b1e49e83384"
K0863_BLOB = "c2ae353cab4a7dbcd28ec53b0f57d35ab4f26a5d"
K0865_BLOB = "6b79dbcb2db0b8c34c108c1c227be139a3f1493b"
COST81_LOG_BLOB = "a5d25f595deba5dd59dce531ea2c2619f0272c3c"
RAW_AUDIT_SCRIPT_BLOB = "5d612a36530a1cf083345423f2ce2a5ba0cb615a"
CHILD_HEX = "00000000020000003800000080000800"
STONES = [11, 31, 59, 60, 61, 89]
EXPECTED_LEGAL = [
    2,3,4,5,6,7,8,10,14,15,16,17,18,19,26,27,28,29,30,32,33,34,35,36,
    37,38,39,40,41,42,43,44,45,46,49,50,51,53,54,66,67,69,70,71,72,
    74,75,76,77,78,79,81,82,83,84,85,86,87,90,91,92,93,94,95,99,101,
    102,103,104,105,106,108,109,110,112,113,114,115,116,117,118,120
]
CONFIRMATION = [5,15,27,30,32,35,41,45,46,74,75,79,85,90,93,105,115]
EXPECTED_CANONS = {
    5:"00000000020000003800000080000820",
    15:"00000000020000003800000080008800",
    27:"00000000020000003800000088000800",
    30:"000000000200000038000000c0000800",
    32:"00000000020000003800000180000800",
    35:"00000000020000003800000880000800",
    41:"00000000020000003800020080000800",
    45:"00000000020000003800200080000800",
    46:"00000000020000003800400080000800",
    74:"00000000020004003800000080000800",
    75:"00000000020008003800000080000800",
    79:"00000000020080003800000080000800",
    85:"00000000022000003800000080000800",
    90:"00000000060000003800000080000800",
    93:"00000000220000003800000080000800",
    105:"0000000a000000003800000000820000",
    115:"0000000a000000003800000000800020",
}

def row(p):
    x, y = p % 11, p // 11
    return (x*x + y*y, x, y, 1)

def det4(points):
    rows = [row(p) for p in points]
    total = 0
    for perm in permutations(range(4)):
        inversions = sum(perm[i] > perm[j]
                         for i in range(4) for j in range(i+1,4))
        product = 1
        for i in range(4):
            product *= rows[i][perm[i]]
        total += (-1 if inversions % 2 else 1) * product
    return total

def transform_point(p, t):
    x, y = p % 11, p // 11
    images = (
        (x,y), (10-y,x), (10-x,10-y), (y,10-x),
        (10-x,y), (x,10-y), (y,x), (10-y,10-x)
    )
    a, b = images[t]
    return 11*b+a

def transform_mask(mask, t):
    out = 0
    for p in range(121):
        if (mask >> p) & 1:
            out |= 1 << transform_point(p,t)
    return out

def canon(mask):
    return min(transform_mask(mask,t) for t in range(8))

def main():
    child = int(CHILD_HEX,16)
    reconstructed = [p for p in range(121) if (child >> p) & 1]
    assert reconstructed == STONES
    parent_bad_quads = [q for q in combinations(STONES,4) if det4(q) == 0]
    triples = list(combinations(STONES,3))
    legal = []
    for p in range(121):
        if p in STONES:
            continue
        if all(det4((*triple,p)) != 0 for triple in triples):
            legal.append(p)
    assert not parent_bad_quads
    assert legal == EXPECTED_LEGAL and len(legal) == 82

    stabilizer = [t for t in range(8) if transform_mask(child,t) == child]
    root_canons = {p:f"{canon(child | (1<<p)):032x}" for p in legal}
    assert len(stabilizer) == 1 and len(set(root_canons.values())) == 82

    confirmation = {
        str(bit): {
            "computed_canon":root_canons[bit],
            "expected_canon":EXPECTED_CANONS[bit],
            "match":root_canons[bit] == EXPECTED_CANONS[bit],
        } for bit in CONFIRMATION
    }
    assert all(x["match"] for x in confirmation.values())
    controls = {
        "four_cocircular_square":det4((0,1,11,12)) == 0,
        "four_collinear_diagonal":det4((0,12,24,36)) == 0,
        "generic_nonzero_determinant":det4((11,31,59,0)) == 8,
    }
    assert all(controls.values())

    result = {
        "schema":"n11-cost82d-independent-geometry-audit-20261118-v1",
        "date":"2026-11-18",
        "source_pins":{
            "cost82d_claim_blob":CLAIM_BLOB,
            "candidate_convention_K0868_blob":K0868_BLOB,
            "sterile_theorem_K0863_blob":K0863_BLOB,
            "historical_census_K0865_blob":K0865_BLOB,
            "cost81_cross_version_log_blob":COST81_LOG_BLOB,
            "cost82d_raw_audit_script_blob":RAW_AUDIT_SCRIPT_BLOB,
        },
        "target":{
            "s5":"00000000020000003800000080000000",
            "s6_child":CHILD_HEX,"stones":STONES,"edge_cost":82,
        },
        "method":"24-term Leibniz expansion of the exact integer determinant of rows [x^2+y^2,x,y,1]; enumerate all 20 triples of the six stones against all 115 empty cells; D4 canonicalization independently recomputed on 11x11 coordinates.",
        "determinant_controls":controls,
        "parent_safe":True,"unsafe_parent_four_subsets":[],
        "triples_per_candidate":len(triples),
        "derived_legal_candidates":legal,"expected_legal_candidates":EXPECTED_LEGAL,
        "candidate_count":len(legal),"candidate_set_exact":True,"missing":[],"extra":[],
        "parent_D4_stabilizer":stabilizer,
        "distinct_D4_child_root_canons":len(set(root_canons.values())),
        "root_canons":{str(k):v for k,v in root_canons.items()},
        "confirmation_bits":CONFIRMATION,
        "confirmation_canons":confirmation,
        "confirmation_canons_all_match":True,
        "all_82_child_roots_D4_distinct":True,
        "historical_sterile_context":{
            "k0865_blob":K0865_BLOB,"k0863_blob":K0863_BLOB,
            "cost81_cross_version_log_blob":COST81_LOG_BLOB,
            "statement":"K0865 head-1410 census records the S5 parent as all_remaining_sterile with 18 S6 rows; the cost81 cross-version log identifies this cost82d child among those historical references. The v17 82/82 REFUTED-D10 sweep is a revalidation, not a newly discovered row or frontier reduction."
        },
        "interpretation_guard":"Geometry only. This independently validates the 82 survival candidates and the 17 confirmation-root D4 canons; it does not prove any game verdict. The separate v17 raw sweep is 0 WIN7-D10 / 82 REFUTED-D10 / 0 capped. REFUTED-D10 is not a LOSS proof. No receipt fold or S6/S5 closure follows.",
        "all_pass":True,
    }
    out = Path(__file__).resolve().parents[1] / "output" / "class2-lane-cost82d-independent-geometry-audit-20261118.json"
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__ == "__main__":
    main()
