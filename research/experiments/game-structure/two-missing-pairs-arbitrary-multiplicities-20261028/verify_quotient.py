"""Independent clique-subset recurrence for the two-missing-pair theorem.

All base cases for k=4,5 with one or two missing pairs are exhausted,
after the proven parity/positivity reduction. No named-vertex deletion.
"""
from itertools import combinations, product


def grundy(k, counts):
    """Clique-mask recurrence, with isolated independent-point parity stripped.

    A[M] is the parity of independent points adjacent to at least one
    surviving clique vertex. Selecting an independent point of type S
    changes the mask to M minus S and creates A[M] xor A[M minus S] xor 1
    isolated points.
    """
    limit = 1 << k
    full = limit - 1
    types = [sig for sig, mult in counts.items() if mult]
    odd_types = [sig for sig, mult in counts.items() if mult & 1]
    active_parity = [0] * limit
    for sig in odd_types:
        for mask in range(1, limit):
            if sig & mask:
                active_parity[mask] ^= 1
    z = [sum(1 for sig in odd_types if sig & (1 << i)) & 1
         for i in range(k)]
    f = [0] * limit
    for mask in range(1, limit):
        a = active_parity[mask]
        seen = 0
        for i in range(k):
            if mask & (1 << i):
                seen |= 1 << (a ^ z[i])
        for sig in types:
            if mask & sig:
                smaller = mask & ~sig
                child = f[smaller] ^ a ^ active_parity[smaller] ^ 1
                seen |= 1 << child
        mex = 0
        while seen & (1 << mex):
            mex += 1
        f[mask] = mex
    return f[full]


def parity_data(k, counts):
    u = 0
    z = [0] * k
    for sig, mult in counts.items():
        if mult % 2:
            u ^= 1
            for i in range(k):
                if sig & (1 << i):
                    z[i] ^= 1
    return u, z


def verify():
    grand = [0] * 4
    total = 0
    for k in (4, 5):
        for label, missing in (
            ("one", {(0, 1)}),
            ("adjacent", {(0, 1), (0, 2)}),
            ("disjoint", {(0, 1), (2, 3)}),
        ):
            pairs = [p for p in combinations(range(k), 2) if p not in missing]
            dist = [0] * 4
            for multiplicities in product((1, 2), repeat=len(pairs)):
                base = {(1 << a) | (1 << b): m for (a, b), m in zip(pairs, multiplicities)}
                for leaves in product((0, 1, 2), repeat=k):
                    counts = dict(base)
                    counts.update({1 << i: leaves[i] for i in range(k)})
                    u, z = parity_data(k, counts)
                    expected = (1 ^ u ^ z[0]) if len(set(z)) == 1 else 2 + u
                    observed = grundy(k, counts)
                    if observed != expected:
                        raise AssertionError((k, label, multiplicities, leaves, observed, expected))
                    dist[observed] += 1
                    grand[observed] += 1
                    total += 1
            print(f"k={k} missing={label} cases={sum(dist)} distribution={dist}")
    assert total == 254016
    assert grand == [8104, 8104, 118886, 118922]
    print(f"ALL_OK cases={total} distribution={grand}")


if __name__ == "__main__":
    verify()
