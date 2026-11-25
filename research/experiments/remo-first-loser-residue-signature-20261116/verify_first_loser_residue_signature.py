#!/usr/bin/env python3
"""Finite arithmetic audit of the published 3-branch REMO non-collapse keys.

Game outcomes are not recomputed here. The finite failure lists are imported
from the complete cap<=10 sweeps K0862/K0864/K0866/K0869; Lemma FL (K0864)
then identifies their possible first losers as the branch-size residues.
"""
from __future__ import annotations
import itertools, json
from collections import Counter
from pathlib import Path

CAP = 10
# Each entry is (sorted branch-size triple, admissible gamma values).
FAILURES = {
    3: [((2,3,8), range(2)), ((2,8,9), range(2)),
        ((3,3,8), range(2)), ((3,8,8), range(2)),
        ((3,8,9), range(2)), ((8,8,9), range(6)),
        ((8,9,9), range(6))],
    4: [((8,8,9), range(6)), ((8,9,9), range(6))],
    5: [((8,8,9), range(6)), ((8,9,9), range(6))],
    6: [((4,4,8), range(3)), ((4,8,8), range(3))],
    7: [((4,4,9), range(3)), ((4,9,9), range(3))],
    8: [((6,6,8), range(5)), ((6,8,8), range(5))],
}
PAIRS = {3:(0,2), 4:(0,1), 5:(3,4), 6:(2,4), 7:(2,4), 8:(0,6)}
COUNTS = {3:22, 4:12, 5:12, 6:6, 7:6, 8:10}
SOURCES = {3:"K0862 (re-derived in K0864)", 4:"K0864", 5:"K0864",
           6:"K0864", 7:"K0866", 8:"K0869"}

def keys():
    return [(s,g) for s in itertools.combinations_with_replacement(range(1,CAP+1),3)
            for g in range(min(s))]

def signature(sizes, r):
    return tuple(sorted({c % r for c in sizes}))

def build_audit():
    all_keys = keys()
    key_set = set(all_keys)
    assert len(all_keys) == 715
    formula = sum(a * ((CAP-a+2)*(CAP-a+1)//2) for a in range(1,CAP+1))
    assert formula == len(all_keys)

    classes = {}
    for r in range(3,10):
        c = Counter(len(signature(s,r)) for s,g in all_keys)
        classes[str(r)] = {"keys_by_distinct_first_loser_count":
                           {str(k):c[k] for k in (1,2,3)}}
    noncollapse = {}
    for r, families in FAILURES.items():
        rows = [(s,g) for s,gs in families for g in gs]
        assert len(rows) == COUNTS[r] and len(set(rows)) == len(rows)
        assert all(row in key_set for row in rows)
        sigs = {signature(s,r) for s,g in rows}
        assert sigs == {PAIRS[r]}
        noncollapse[str(r)] = {
            "source": SOURCES[r],
            "noncollapse_key_count": len(rows),
            "size_families": [list(s) for s,gs in families],
            "gamma_values_by_size_family": {
                ",".join(map(str,s)): list(gs) for s,gs in families},
            "distinct_first_loser_residue_pair": list(PAIRS[r]),
            "all_noncollapse_keys_have_exactly_two_first_loser_residues": True,
            "all_noncollapse_keys_share_same_residue_pair": True,
        }

    single9 = [(s,g) for s,g in all_keys if len(signature(s,9)) == 1]
    expected = {((a,a,a),g) for a in range(1,11) for g in range(a)}
    expected |= {((1,1,10),0), ((1,10,10),0)}
    assert set(single9) == expected and len(single9) == 57
    assert classes["9"]["keys_by_distinct_first_loser_count"] == {
        "1":57, "2":336, "3":322}

    return {
        "title":"Three-branch REMO first-loser residue signature census",
        "status":"finite-complete-census-derived-from-published-boundaries",
        "domain":{"branch_count":3,"max_branch_size":CAP,"keys":715,
                  "gamma_range":"0 <= gamma < min(C_1,C_2,C_3)"},
        "key_count_crosscheck":{"direct_enumeration":715,
                                "minimum_size_sum":formula,"match":True},
        "noncollapse_signature_r3_to_r8":noncollapse,
        "residue_class_census_r3_to_r9":classes,
        "r9_prefilter":{
            "single_residue_keys":57,"two_residue_keys":336,
            "three_residue_keys":322,"total_keys":715,
            "singleton_residue_characterization":
                "all equal triples (a,a,a), 1<=a<=10, 0<=gamma<a; "
                "plus (1,1,10)|gamma=0 and (1,10,10)|gamma=0",
            "singleton_residue_key_count_by_pattern":
                {"equal_triples":55,"mixed_1_10_triples":2},
            "two_residue_keys_are_ordering_hint_only":True,
            "complete_r9_sweep_must_not_skip_other_classes":True},
        "interpretation":{
            "proved_input":"For every k-branch profile and r, possible first losers "
                "are exactly {C_i mod r} (Lemma FL, K0864).",
            "finite_observation":"For cap<=10 and r=3..8, every published "
                "non-collapse key has exactly two distinct first-loser residues; "
                "for each r all such keys share one residue pair.",
            "not_proved":"This does not prove that one or three distinct first-loser "
                "residues force survivor determinacy for arbitrary profiles or r. "
                "The r=9 data is only an arithmetic prefilter census, not an outcome sweep."},
        "all_checks_pass":True}

def main():
    result = build_audit()
    out = Path(__file__).resolve().parent / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+"\n",
                   encoding="utf-8")
    print(out.read_text(encoding="utf-8"), end="")

if __name__ == "__main__":
    main()
