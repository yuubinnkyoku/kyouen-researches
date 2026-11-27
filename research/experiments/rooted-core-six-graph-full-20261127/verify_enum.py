#!/usr/bin/env python3
"""Enumeration verifier for the 6-vertex graph core family (group-theoretic).

E1: independent canonical enumeration of all 2^15 = 32768 raw two-edge clutters
    on vertices {0..5} (root 0 fixed) -> rooted types, using a fresh
    lexicographic-minimisation canonical form (no engine import).
E2: Burnside orbit count over S_5 acting on the 15 pair slots must equal the
    E1 type count (two independent derivations of the same number).
E3: orbit-stabilizer coverage: for each type, 120/|Aut(type)| summed over
    types must equal 32768 (each raw input is covered by its orbit with
    multiplicity |Aut|), and every raw input maps to exactly one type.
Fail-closed.
"""
import json
import sys
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 6


def fresh_canonical(edges):
    best = None
    for tail in permutations(range(1, N)):
        order = (0,) + tail
        inv = {old: new for new, old in enumerate(order)}
        cand = tuple(sorted(sum(1 << inv[v] for v in range(N) if e >> v & 1)
                            for e in edges))
        if best is None or cand < best:
            best = cand
    return best


def main():
    audit = json.loads((HERE / 'output' / 'audit.json').read_text())
    pairs = [(a, b) for a in range(N) for b in range(a + 1, N)]
    idx = {p: i for i, p in enumerate(pairs)}
    perms = list(permutations(range(1, N)))
    actions = []
    for p in perms:
        vmap = (0,) + p
        actions.append([idx[tuple(sorted((vmap[a], vmap[b])))] for a, b in pairs])

    errors = []
    reps = {}
    for mask in range(1 << len(pairs)):
        edges = tuple(sorted(1 << a | 1 << b
                             for i, (a, b) in enumerate(pairs) if mask >> i & 1))
        reps.setdefault(fresh_canonical(edges), []).append(mask)
    types_e1 = len(reps)
    if types_e1 != audit['distinct_initial_types']:
        errors.append('E1 type count %d != audit %d' % (types_e1, audit['distinct_initial_types']))
    if audit['raw_inputs'] != 32768:
        errors.append('raw_inputs != 32768')

    total = 0
    for act in actions:
        seen = [False] * len(pairs)
        c = 0
        for s in range(len(pairs)):
            if not seen[s]:
                c += 1
                j = s
                while not seen[j]:
                    seen[j] = True
                    j = act[j]
        total += 1 << c
    if total % 120:
        errors.append('Burnside sum not divisible by 120')
    types_e2 = total // 120
    if types_e2 != types_e1:
        errors.append('E2 Burnside %d != E1 %d' % (types_e2, types_e1))

    orbit_sum = 0
    for key in reps:
        aut = 0
        for p in perms:
            vmap = (0,) + p
            img = tuple(sorted(sum(1 << vmap[v] for v in range(N) if e >> v & 1)
                               for e in key))
            if img == key:
                aut += 1
        orbit_sum += 120 // aut if aut else 0
        if not aut:
            errors.append('no automorphism for type %r (impossible)' % (key,))
    if orbit_sum != 32768:
        errors.append('E3 orbit-stabilizer sum %d != 32768' % orbit_sum)
    if sum(len(m) for m in reps.values()) != 32768:
        errors.append('E3 raw membership sum != 32768')

    out = dict(verifier='enumeration-burnside', types_e1=types_e1,
               types_burnside=types_e2, orbit_stabilizer_sum=orbit_sum,
               errors=errors, verdict='PASS' if not errors else 'FAIL')
    (HERE / 'output' / 'verify_enum.json').write_text(json.dumps(out, indent=2))
    print(json.dumps(out))
    return 0 if not errors else 1


if __name__ == '__main__':
    sys.exit(main())
