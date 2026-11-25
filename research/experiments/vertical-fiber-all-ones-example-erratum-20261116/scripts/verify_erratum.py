#!/usr/bin/env python3
"""Exact two-engine audit for the stale all-ones example (k,z)=(4,6).

The recurrence is the K0832 residual game restricted to X=(1^k):
  h(k,z,R) = mex({h(k-1,z+1,R-1)} if k>0
                union {1 xor h(k,z-1,R-1)} if z>0).
A second engine keeps the general multiset X explicitly.
The all-R tail R >= 2k+z-1 is supplied by the already-proved K0832
residual-regime lemma; this script checks the finite prefix and cross-engine
agreement, not that unbounded lemma.
"""
from functools import lru_cache
import hashlib
import json
from pathlib import Path


def mex(values):
    present = set(values)
    result = 0
    while result in present:
        result += 1
    return result


@lru_cache(maxsize=None)
def h_reduced(k, z, R):
    if R == 0:
        return 0
    options = []
    if k >= 1:
        options.append(h_reduced(k - 1, z + 1, R - 1))
    if z >= 1:
        options.append(1 ^ h_reduced(k, z - 1, R - 1))
    return mex(options)


@lru_cache(maxsize=None)
def h_multiset(R, X, z):
    if R == 0:
        return 0
    options = []
    for x in sorted(set(X)):
        child = list(X)
        child.remove(x)
        if x >= 2:
            child.append(x - 1)
            child.sort()
            options.append(h_multiset(R - 1, tuple(child), z))
        else:
            child.sort()
            options.append(h_multiset(R - 1, tuple(child), z + 1))
    if z >= 1:
        options.append(1 ^ h_multiset(R - 1, X, z - 1))
    return mex(options)


def twos(k, z, upper):
    return [R for R in range(1, upper + 1) if h_reduced(k, z, R) == 2]


def main():
    k, z, upper = 4, 6, 60
    rows = []
    for R in range(upper + 1):
        reduced = h_reduced(k, z, R)
        multiset = h_multiset(R, (1,) * k, z)
        rows.append({"R": R, "reduced": reduced, "multiset": multiset})
    mismatches = [row for row in rows if row["reduced"] != row["multiset"]]
    actual_twos = [row["R"] for row in rows if row["reduced"] == 2]
    stale_example = [1, 3, 5, 7]
    false_positives = sorted(set(stale_example) - set(actual_twos))
    missing = sorted(set(actual_twos) - set(stale_example))

    # The exact all-R conclusion combines the finite prefix R=0..12 with
    # K0832's proved tail lemma at R >= 2k+z-1 = 13.
    tail_start = 2 * k + z - 1
    finite_prefix = [h_reduced(k, z, R) for R in range(tail_start)]
    tail_checks = [h_reduced(k, z, R) == (k % 2) for R in range(tail_start, upper + 1)]

    # The stale four-element list is exactly reproduced at (k,z)=(6,6),
    # which is a diagnostic clue, not a claim about the original author's intent.
    diagnostic_twos = twos(6, 6, upper)

    source = Path(__file__).read_bytes()
    audit = {
        "actual_R_with_H2_through_60": actual_twos,
        "case": {"R_checked": [0, upper], "k": k, "z": z},
        "conclusion": "For (k,z)=(4,6), H(R;(1,1,1,1);6)=2 exactly at R={1,3}; the old example's {5,7} are false positives. The list {1,3,5,7} occurs at (k,z)=(6,6).",
        "diagnostic_k6_z6_R_with_H2_through_60": diagnostic_twos,
        "finite_prefix_R_0_to_12": finite_prefix,
        "stale_false_positives": false_positives,
        "stale_missing_values": missing,
        "stale_report_list": stale_example,
        "tail": {
            "checks_through_60": len(tail_checks),
            "finite_checks_pass": all(tail_checks),
            "proved_value": k % 2,
            "start_R": tail_start,
            "unbounded_basis": "K0832: R >= 2k+z-1 implies H = sum(X) mod 2"
        },
        "two_engine": {
            "first_mismatches": mismatches[:5],
            "mismatches": len(mismatches),
            "multiset_cache_states": h_multiset.cache_info().currsize,
            "reduced_cache_states": h_reduced.cache_info().currsize,
            "states": len(rows)
        },
        "verifier_sha256": hashlib.sha256(source).hexdigest()
    }
    assert not mismatches
    assert finite_prefix == [0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert actual_twos == [1, 3]
    assert false_positives == [5, 7]
    assert missing == []
    assert all(tail_checks)
    assert diagnostic_twos == stale_example
    print(json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
