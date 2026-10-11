#!/usr/bin/env python3
"""Independent local check: the two surviving 33-row masks at w=330 fail mod 59.
The two masks are outputs of the main modular intersection verifier, not
independently reconstructed here. This is only an auxiliary audit.
"""
rows = [0, 76, 77, 81, 84, 86, 93, 104, 112, 114, 123, 139,
        153, 158, 167, 186, 198, 207, 219, 238, 247, 252, 266,
        282, 291, 293, 301, 312, 319, 321, 324, 328, 329]
p = 59
qr = {x*x % p for x in range(p)}
for name, candidate in [('A', rows), ('reflected', [329-y for y in rows])]:
    possible = []
    for c in range(p):
        n_candidates = set(range(p))
        for y in candidate:
            a = (2*y+c)**2 % p
            n_candidates.intersection_update((a+z) % p for z in qr)
            if not n_candidates:
                break
        possible.extend((c,n) for n in n_candidates)
    assert not possible, (name, possible)
    print(f"MOD59_EXCLUDED {name} {len(candidate)} rows")
