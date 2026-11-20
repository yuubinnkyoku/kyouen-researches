#!/usr/bin/env python3
"""Mixed six-vertex rooted cores: bucket machinery for K0684 slice proofs.

35-bit labeled universe on vertices 0..5 (root 0 fixed):
  bits 0..14   = the 15 vertex pairs (edges of size 2)
  bits 15..34  = the 20 vertex triples (edges of size 3)
Labels are minimal clutters by construction: no chosen pair lies inside a
chosen triple. bucket j = exactly j triples; for j>=1 the pair part must be
nonempty ("mixed proper"). Types = orbits under the 120 root-fixing vertex
permutations, represented in engine.canonical form (keys of the published
513-type le5 base table).

solve_state computes the exact recurrences of proof.md for one 6-vertex
state; every retained child has <=5 vertices so its full prefix comes from
the published base table (periodically extended through K0682).

This is a from-scratch rebuild after an execution-environment outage; head
counts must reproduce the previously certified values:
j=0: 32768 labeled / 544 types, j=1: 81900/1018, j=2: 143170/1663,
j=3: 213900/2336, j=4: 286755/3045, j=5: 347904/3536.
"""
import json
import os
from functools import lru_cache
from itertools import combinations, permutations

import numpy as np

import engine

PAIRS = list(combinations(range(6), 2))
TRIPLES = list(combinations(range(6), 3))
PAIR_INDEX = {p: k for k, p in enumerate(PAIRS)}
TRIPLE_INDEX = {t: k for k, t in enumerate(TRIPLES)}
PERMS = [(0,) + p for p in permutations(range(1, 6))]

# pair bits covered by each triple
TRIPLE_COVER = []
for (a, b, c) in TRIPLES:
    m = 0
    for u, v in ((a, b), (a, c), (b, c)):
        m |= 1 << PAIR_INDEX[(min(u, v), max(u, v))]
    TRIPLE_COVER.append(m)


def _perm_bitvecs():
    vecs = []
    for perm in PERMS:
        vec = np.zeros(35, dtype=np.int64)
        for k, (a, b) in enumerate(PAIRS):
            na, nb = perm[a], perm[b]
            vec[k] = PAIR_INDEX[(min(na, nb), max(na, nb))]
        for k, (a, b, c) in enumerate(TRIPLES):
            na, nb, nc = sorted(perm[x] for x in (a, b, c))
            vec[15 + k] = 15 + TRIPLE_INDEX[(na, nb, nc)]
        vecs.append(vec)
    return vecs


_BITVECS = _perm_bitvecs()


def _transform(words, vec):
    """Apply one root-fixing permutation to every 35-bit word."""
    acc = np.zeros(len(words), dtype=np.uint64)
    for k in range(35):
        acc |= (((words >> np.uint64(k)) & np.uint64(1)) << np.uint64(vec[k]))
    return acc


def orbit_min(words):
    words = np.asarray(words, dtype=np.uint64)
    best = words.copy()
    for vec in _BITVECS:
        cand = _transform(words, vec)
        np.minimum(best, cand, out=best)
    return best


def word_tripleset(j_combo):
    """35-bit word with exactly the triples of the combo (no pairs)."""
    w = 0
    for t in j_combo:
        w |= 1 << (15 + t)
    return w


def bucket_labels(j):
    """All labeled minimal clutters with exactly j triples (uint64 array).

    j=0: every pair subset (the empty clutter included; full graph family).
    j>=1: pair part must be nonempty (mixed proper)."""
    out = []
    if j == 0:
        return np.arange(1 << 15, dtype=np.uint64)
    for combo in combinations(range(20), j):
        covered = 0
        for t in combo:
            covered |= TRIPLE_COVER[t]
        free = [k for k in range(15) if not (covered >> k) & 1]
        base = word_tripleset(combo)
        if not free:
            continue  # only the empty pair part; excluded for j>=1
        nfree = len(free)
        bits = [1 << k for k in free]
        rows = np.arange(1, 1 << nfree, dtype=np.uint64)  # skip pair part = 0
        vals = np.zeros(len(rows), dtype=np.uint64)
        for k in range(nfree):
            vals |= ((rows >> np.uint64(k)) & np.uint64(1)) * np.uint64(bits[k])
        vals |= np.uint64(base)
        out.append(vals)
    if not out:
        return np.zeros(0, dtype=np.uint64)
    return np.concatenate(out)


def word_state(w):
    """35-bit word -> engine clutter state (before canonicalization)."""
    edges = []
    for k in range(15):
        if (w >> k) & 1:
            a, b = PAIRS[k]
            edges.append((1 << a) | (1 << b))
    for k in range(20):
        if (w >> (15 + k)) & 1:
            a, b, c = TRIPLES[k]
            edges.append((1 << a) | (1 << b) | (1 << c))
    return (6, tuple(sorted(edges)))


def bucket_types(j, cache_dir='.'):
    """(types, labeled, reps): engine-canonical orbit representatives."""
    cache = os.path.join(cache_dir, f'types_j{j}.json')
    if os.path.exists(cache):
        d = json.load(open(cache))
        if d.get('v') == 2:
            return ([(t[0], tuple(t[1])) for t in d['types']],
                    d['labeled'], d['reps'])
    words = bucket_labels(j)
    labeled = int(len(words))
    mins = orbit_min(words)
    uniq = np.unique(mins)
    reps = int(len(uniq))
    states = sorted({engine.canonical(6, word_state(int(w))[1]) for w in uniq})
    json.dump({'v': 2, 'labeled': labeled, 'reps': reps,
               'types': [[s[0], list(s[1])] for s in states]},
              open(cache, 'w'))
    return states, labeled, reps


@lru_cache(None)
def load_base():
    """Published 513-type le5 table: state -> 1070-prefix (values 0..1069)."""
    here = os.path.dirname(os.path.abspath(__file__))
    d = json.load(open(os.path.join(here, 'audit_base.json')))
    return {(r['n'], tuple(r['forbidden'])): r['prefix'] for r in d['records']}


def base_value(known, child, length):
    """f_child(length) for a <=5-vertex retained child (periodic tail)."""
    p = known[child]
    if length < len(p):
        return p[length]
    return p[500 + (length - 500) % 34]


def path_table(limit):
    return engine.path_values(limit)


@lru_cache(None)
def _prep(state):
    """(after_root, without_root, retained_children, detached_ordinaries)."""
    n = state[0]
    after_root = engine.ordinary(engine.play(state, 0)[0])
    without_root = engine.ordinary(engine.delete_root(state))
    retained, detached = [], []
    for v in range(1, n):
        child, alive = engine.play(state, v)
        if alive:
            retained.append(child)
        else:
            detached.append(engine.ordinary(child))
    return after_root, without_root, tuple(retained), tuple(detached)


def solve_state(state, limit, known, path):
    """Exact f_state(L) for L=0..limit (single 6-vertex state, per proof.md).

    Every retained child has <=5 vertices, so its values come from the
    published base table with the certified periodic tail (K0682)."""
    after_root, without_root, retained, detached = _prep(state)
    for child in retained:
        if child not in known:
            raise KeyError((state, child))
    seq = []
    for length in range(limit + 1):
        options = {after_root ^ path[max(length - 1, 0)]}
        for child in retained:
            options.add(base_value(known, child, length))
        for g in detached:
            options.add(g ^ path[length])
        if length >= 1:
            options.add(without_root ^ path[max(length - 2, 0)])
        if length >= 2:
            options.add(seq[length - 2])
            options.update(seq[i] ^ path[length - 3 - i]
                           for i in range(length - 2))
        seq.append(engine.mex(options))
    lf = max((i for i in range(len(seq) - 34) if seq[i] != seq[i + 34]),
             default=-1)
    return seq, lf


def direct(state, length):
    """Raw subset-game Grundy check independent of the engine machinery.

    Core points 0..n-1, path points n..n+length-1 hanging off the root 0.
    A move occupies a point; the occupied set must never fully contain a
    forbidden edge. Normal play on the safe subsets, memoized by mask."""
    n, forbidden = state
    pts = n + length
    emask = [sum(1 << v for v in range(n) if e >> v & 1) for e in forbidden]
    if length >= 1:
        emask.append((1 << 0) | (1 << n))
        for i in range(length - 1):
            emask.append((1 << (n + i)) | (1 << (n + i + 1)))
    memo = {}

    def g(occ):
        r = memo.get(occ)
        if r is not None:
            return r
        opts = set()
        for v in range(pts):
            bit = 1 << v
            if occ & bit:
                continue
            occ2 = occ | bit
            if any(e == (e & occ2) for e in emask if e & bit):
                continue
            opts.add(g(occ2))
        r = engine.mex(opts)
        memo[occ] = r
        return r

    return g(0), len(memo)
