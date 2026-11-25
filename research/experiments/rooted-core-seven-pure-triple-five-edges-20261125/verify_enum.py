#!/usr/bin/env python3
"""Independent enumeration/closure verification for the seven-vertex
pure-three-edge <=5-edge family (K0684 evidence update).

  (E1) labeled family count: sum_{k=0..5} C(35,k) = 384,168 (binomial identity),
  (E2) rooted-type enumeration reproduced from scratch (canonical min over the
       720 root-fixing vertex permutations, precomputed permutation tables),
  (E3) Burnside independent orbit count over the 720 vertex permutations acting
       on the 35 triples: (1/|G|) * sum_g Fix(g) == 924 (no canonical forms used),
  (E4) orbit-stabilizer cross-check: sum over types of 720/|Aut(type)| == 384,168
       (independently recomputed stabilizer sizes via permutation images),
  (E5) every enumerated type is a fixed point of engine.canonical (published
       code path), and the type set is disjoint from the K0682 base table,
  (E6) closure of the type set reproduces 2,948 states = 2,604 new + 344 base
       states with the {7: 924, 6: 1680} vertex split,
  (E7) the 7-vertex new states of the published shard records equal the
       enumerated type set exactly.

Standard library only. Deterministic. Ends with VERIFY-ENUM: PASS.
"""
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107'))
from engine import canonical, closure

N = 7
E = 5
TRIPLES = list(combinations(range(N), 3))
IDX = {t: i for i, t in enumerate(TRIPLES)}
VMASK = [sum(1 << v for v in t) for t in TRIPLES]
MASK_IDX = {VMASK[i]: i for i in range(len(TRIPLES))}
BASE = ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107/output/audit.json'


def build_tables():
    tabs = []
    for p in permutations(range(1, N)):
        vmap = (0,) + p
        tabs.append(tuple(IDX[tuple(sorted(vmap[v] for v in t))] for t in TRIPLES))
    return tabs


def enumerate_types(tabs):
    raw = 0
    types = set()
    for k in range(E + 1):
        for fam in combinations(range(len(TRIPLES)), k):
            mask = 0
            for i in fam:
                mask |= 1 << i
            bits = []
            m = mask
            while m:
                b = m & -m
                bits.append(b.bit_length() - 1)
                m ^= b
            best = None
            for tab in tabs:
                key = tuple(sorted(VMASK[tab[i]] for i in bits))
                if best is None or key < best:
                    best = key
            types.add((N, best))
            raw += 1
    return sorted(types), raw


def burnside_orbit_count(tabs):
    """Number of <orbit>s of <=5-edge families under the vertex-permutation group.

    A family (edge set of <=5 triples) is fixed setwise by permutation g iff it
    is a union of whole cycles of g's induced action on the 35 triples.
    """
    total = 0
    for tab in tabs:
        seen = [False] * len(TRIPLES)
        cycles = []
        for i in range(len(TRIPLES)):
            if seen[i]:
                continue
            j = i
            count = 0
            while not seen[j]:
                seen[j] = True
                j = tab[j]
                count += 1
            cycles.append(count)
        # count unions of cycles of total size <= E (empty union included)
        ways = {0: 1}
        for size in cycles:
            if size > E:
                continue
            nxt = dict(ways)
            for tot, cnt in ways.items():
                nxt[tot + size] = nxt.get(tot + size, 0) + cnt
            ways = nxt
        total += sum(cnt for tot, cnt in ways.items() if tot <= E)
    assert total % len(tabs) == 0, total
    return total // len(tabs)


def stabilizer_sum(types, tabs):
    """Sum over types of orbit size 720/|Aut(type)| must equal the raw count."""
    total = 0
    for state in types:
        _, edges = state
        indices = [MASK_IDX[e] for e in edges]
        aut = 0
        for tab in tabs:
            image = tuple(sorted(VMASK[tab[i]] for i in indices))
            if image == edges:
                aut += 1
        assert aut > 0, state
        assert len(tabs) % aut == 0, (state, aut)
        total += len(tabs) // aut
    return total


def main():
    tabs = build_tables()
    raw_expected = sum(1 for k in range(E + 1) for _ in combinations(range(len(TRIPLES)), k))
    assert raw_expected == 384168, raw_expected
    print('E1 labeled families by binomial identity: %d' % raw_expected, flush=True)

    types, raw = enumerate_types(tabs)
    assert raw == 384168, raw
    assert len(types) == 924, len(types)
    print('E2 enumeration reproduced: raw %d, rooted types %d' % (raw, len(types)), flush=True)

    orbits = burnside_orbit_count(tabs)
    assert orbits == 924, orbits
    print('E3 Burnside independent orbit count: %d' % orbits, flush=True)

    orbit_total = stabilizer_sum(types, tabs)
    assert orbit_total == raw, (orbit_total, raw)
    print('E4 orbit-stabilizer sum 720/|Aut| over types: %d == raw count' % orbit_total, flush=True)

    base = json.loads(BASE.read_text(encoding='utf-8'))
    base_keys = {(row['n'], tuple(row['forbidden'])) for row in base['records']}
    nonfixed = [t for t in types if canonical(N, tuple(t[1])) != t]
    assert not nonfixed, nonfixed[:3]
    assert not (set(types) & base_keys), 'type set intersects base table'
    print('E5 all 924 types are engine.canonical fixed points; disjoint from base table', flush=True)

    states = closure(types)
    new = [s for s in states if s not in base_keys]
    known = [s for s in states if s in base_keys]
    assert len(states) == 2948 and len(new) == 2604 and len(known) == 344, \
        (len(states), len(new), len(known))
    split = {6: 0, 7: 0}
    for s in new:
        split[s[0]] += 1
    assert split == {6: 1680, 7: 924}, split
    print('E6 closure: 2948 states = 2604 new {%d six-vertex, %d seven-vertex} + 344 base'
          % (split[6], split[7]), flush=True)

    parts = sorted((HERE / 'output/shards').glob('part*.json'))
    seven = set()
    for part in parts:
        data = json.loads(part.read_text(encoding='utf-8'))
        for row in data['records']:
            if row['n'] == N:
                seven.add((row['n'], tuple(row['forbidden'])))
    assert seven == set(types), (len(seven ^ set(types)))
    assert len(seven) == 924
    print('E7 7-vertex records of the published shards equal the enumerated type set', flush=True)
    print('VERIFY-ENUM: PASS', flush=True)


if __name__ == '__main__':
    main()
