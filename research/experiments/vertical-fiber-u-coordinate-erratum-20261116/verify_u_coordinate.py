#!/usr/bin/env python3
"""Audit the false XOR/mex re-coordinate in the residual-game note."""
from functools import lru_cache
from itertools import combinations_with_replacement
import json


def mex(values):
    values = set(values)
    g = 0
    while g in values:
        g += 1
    return g


@lru_cache(maxsize=None)
def H(R, X, z):
    if R == 0:
        return 0
    options = set()
    for x in set(X):
        rest = list(X)
        rest.remove(x)
        if x >= 2:
            rest.append(x - 1)
            rest.sort()
            options.add(H(R - 1, tuple(rest), z))
        else:
            rest.sort()
            options.add(H(R - 1, tuple(rest), z + 1))
    if z >= 1:
        options.add(1 ^ H(R - 1, X, z - 1))
    return mex(options)


@lru_cache(maxsize=None)
def U_claimed(R, X, z):
    """The incorrect 'C unflipped, B flipped' recurrence from the note."""
    if R == 0:
        return z & 1
    options = set()
    for x in set(X):
        rest = list(X)
        rest.remove(x)
        if x >= 2:
            rest.append(x - 1)
            rest.sort()
            options.add(U_claimed(R - 1, tuple(rest), z))
        else:
            rest.sort()
            options.add(1 ^ U_claimed(R - 1, tuple(rest), z + 1))
    if z >= 1:
        options.add(U_claimed(R - 1, X, z - 1))
    return mex(options)


@lru_cache(maxsize=None)
def U_exact(R, X, z):
    """Exact recurrence obtained by substituting H=U xor (z mod 2)."""
    if R == 0:
        return z & 1
    eps = z & 1
    options = set()
    for x in set(X):
        rest = list(X)
        rest.remove(x)
        if x >= 2:
            rest.append(x - 1)
            rest.sort()
            options.add(U_exact(R - 1, tuple(rest), z) ^ eps)
        else:
            rest.sort()
            options.add(U_exact(R - 1, tuple(rest), z + 1) ^ eps ^ 1)
    if z >= 1:
        options.add(U_exact(R - 1, X, z - 1) ^ eps)
    return mex(options) ^ eps


def main():
    multisets = [()]
    for size in range(1, 4):
        multisets.extend(combinations_with_replacement(range(1, 5), size))

    states = 0
    claimed_count = 0
    exact_count = 0
    first_claimed = []
    first_exact = []
    for R in range(0, 9):
        for X in multisets:
            for z in range(0, 7):
                states += 1
                actual = H(R, X, z) ^ (z & 1)
                claimed = U_claimed(R, X, z)
                exact = U_exact(R, X, z)
                if actual != claimed:
                    claimed_count += 1
                    if len(first_claimed) < 10:
                        first_claimed.append([R, list(X), z, H(R, X, z), actual, claimed])
                if actual != exact:
                    exact_count += 1
                    if len(first_exact) < 10:
                        first_exact.append([R, list(X), z, H(R, X, z), actual, exact])

    R, X, z = 1, (1,), 1
    original_options = {H(0, (), 2), 1 ^ H(0, (1,), 0)}
    claimed_options = {1 ^ U_claimed(0, (), 2), U_claimed(0, (1,), 0)}
    witness = {
        "state": {"R": R, "X": list(X), "z": z},
        "original_H_options": sorted(original_options),
        "H": H(R, X, z),
        "actual_U": H(R, X, z) ^ (z & 1),
        "claimed_U_options": sorted(claimed_options),
        "claimed_U": U_claimed(R, X, z),
        "exact_U": U_exact(R, X, z),
    }

    assert states == 2205
    assert claimed_count == 620
    assert exact_count == 0
    assert witness == {
        "state": {"R": 1, "X": [1], "z": 1},
        "original_H_options": [0, 1],
        "H": 2,
        "actual_U": 3,
        "claimed_U_options": [0, 1],
        "claimed_U": 2,
        "exact_U": 3,
    }

    out = {
        "grid": {
            "R": [0, 8],
            "multiset_size": [0, 3],
            "token_values": [1, 4],
            "z": [0, 6],
            "multisets": len(multisets),
            "states": states,
            "claimed_recurrence_mismatches": claimed_count,
            "exact_recurrence_mismatches": exact_count,
            "first_claimed_mismatches": first_claimed,
            "first_exact_mismatches": first_exact,
        },
        "minimal_counterexample": witness,
        "mex_xor": {
            "set": [0, 1],
            "xor": 1,
            "mex_then_xor": mex([0, 1]) ^ 1,
            "xor_then_mex": mex([0 ^ 1, 1 ^ 1]),
        },
        "result": "PASS",
    }
    print(json.dumps(out, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
