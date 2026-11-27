#!/usr/bin/env python3
"""Independent second implementation verifier for the 6-vertex graph core family.

Fresh re-derivation: does NOT import the pinned engine, does NOT use the K0682
known table. Recomputes, from scratch with its own state algebra (own canonical
forms, own remap, own play, own mex), the full closure of the family and the
Grundy sequences of every closure state through the certification bound, then
compares record-by-record with the official audit.json. Fail-closed: any
mismatch, missing/phantom record, header inconsistency or window failure exits
rc=1 with verdict FAIL.

Move semantics (mirrors the pinned engine, re-implemented from its documented
behaviour / the K0682 proof text): playing vertex v removes v; every forbidden
edge shrinks by v; any edge shrunk to a single remaining vertex blocks (removes)
that vertex as well; the residual clutter keeps the surviving edges inside the
active vertex set with contained edges dropped; root survival = root in the
active set. Recurrence option assembly per the K0682 proof:
  f_C(L) = mex( {A_C ^ p_{L-1}, B_C ^ p_{L-2}, f_C(L-2)}
                U {f_{C_u}(L) : root survives}
                U {g(D_u) ^ p_L : root dies}
                U {f_C(i) ^ p_{L-3-i} : 0 <= i <= L-3} ).
NOTE (disclosed harness bug, caught fail-closed by this very verifier): the
first version of this verifier seeded the path list with [0] AND appended per
length, shifting all path indices by one; it produced a FAIL verdict and the
bug was fixed before any use of its output. The official audit.json was never
affected (the official solver clones the validated solve_core path
construction, path index == length).
"""
import json
import sys
from functools import lru_cache
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent


# ---- independent state algebra (fresh implementation) ----
def canon(n, edges):
    """Rooted canonical form: minimise sorted edge-bitmask tuple over perms of 1..n-1."""
    edges = tuple(sorted(set(edges)))
    if n <= 1:
        return (n, edges)
    best = None
    for tail in permutations(range(1, n)):
        order = (0,) + tail
        inv = {old: new for new, old in enumerate(order)}
        cand = tuple(sorted(sum(1 << inv[v] for v in range(n) if e >> v & 1) for e in edges))
        if best is None or cand < best:
            best = cand
    return (n, best)


def shrink(n, edges, active_mask):
    """Residual clutter after deleting the vertices outside active_mask."""
    order = [v for v in range(n) if active_mask >> v & 1]
    inv = {old: new for new, old in enumerate(order)}
    alive = []
    for e in edges:
        if e & ~active_mask:
            continue
        alive.append(sum(1 << inv[v] for v in order if e >> v & 1))
    alive = sorted(set(alive))
    keep = [e for e in alive if not any(o != e and o & e == o for o in alive)]
    for e in keep:
        assert e.bit_count() >= 2
    return canon(len(order), keep)


def move(n, edges, v):
    """Play vertex v: returns (residual state, root_alive)."""
    bit = 1 << v
    reduced = [e & ~bit for e in edges]
    blocked = 0
    for e in reduced:
        if e.bit_count() == 1:
            blocked |= e
    active = ((1 << n) - 1) & ~bit & ~blocked
    return shrink(n, edges, active), bool(active & 1)


@lru_cache(maxsize=None)
def g_ordinary(state):
    n, edges = state
    if n == 0:
        return 0
    opts = set()
    seen = set()
    for v in range(n):
        child, _ = move(n, edges, v)
        if child not in seen:
            seen.add(child)
            opts.add(g_ordinary(child))
    g = 0
    while g in opts:
        g += 1
    return g


def root_delete(state):
    n, edges = state
    return shrink(n, edges, ((1 << n) - 1) & ~1)


def family_closure(initial):
    found = set()
    pending = list(initial)
    while pending:
        st = pending.pop()
        if st in found:
            continue
        found.add(st)
        n, edges = st
        for v in range(1, n):
            child, alive = move(n, edges, v)
            if alive:
                pending.append(child)
    return sorted(found, key=lambda s: (s[0], s[1]))


def graph_types(n=6):
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
    reps = set()
    for mask in range(1 << len(pairs)):
        edges = tuple(sorted(1 << a | 1 << b
                             for i, (a, b) in enumerate(pairs) if mask >> i & 1))
        reps.add(canon(n, edges))
    return sorted(reps)


def mex(opts):
    g = 0
    while g in opts:
        g += 1
    return g


def solve_all(states, limit):
    """Compute f_state(L) for L=0..limit for every closure state, no known table."""
    path = []
    values = {st: [] for st in states}
    for L in range(0, limit + 1):
        # path[L]: bare two-point path value, engine convention (index == length).
        path.append(mex({path[max(j - 1, 0)] ^ path[max(L - j - 2, 0)]
                         for j in range(L)}))
        for st in states:
            n, edges = st
            after = g_ordinary(move(n, edges, 0)[0])
            deleted = g_ordinary(root_delete(st))
            options = {after ^ path[max(L - 1, 0)]}
            for v in range(1, n):
                child, alive = move(n, edges, v)
                if alive:
                    options.add(values[child][L])
                else:
                    options.add(g_ordinary(child) ^ path[L])
            if L >= 1:
                options.add(deleted ^ path[max(L - 2, 0)])
            if L >= 2:
                options.add(values[st][L - 2])
                for i in range(L - 2):
                    options.add(values[st][i] ^ path[L - 3 - i])
            values[st].append(mex(options))
    return path, values


def main(argv):
    audit_path = Path(argv[1]) if len(argv) > 1 else (HERE / 'output' / 'audit.json')
    audit = json.loads(audit_path.read_text())
    errors = []
    if audit.get('jointly_certified') is not True:
        errors.append('audit claims jointly_certified is not true')
        out = dict(verifier='independent-second-implementation', errors=errors, verdict='FAIL')
        print(json.dumps(out))
        return 1
    if audit.get('values_needed_through') != 2 * audit['joint_start_candidate'] + 69:
        errors.append('needed != 2*start+69')
    if audit.get('new_closure_states') != audit.get('closure_states', 0) - audit.get('known_closure_states', 0):
        errors.append('closure accounting mismatch in audit header')
    needed = audit['values_needed_through']
    initial = graph_types(6)
    states = family_closure(initial)
    if len(initial) != audit['distinct_initial_types']:
        errors.append('initial type count %d != %d' % (len(initial), audit['distinct_initial_types']))
    if len(states) != audit['closure_states']:
        errors.append('closure count %d != %d' % (len(states), audit['closure_states']))
    path, values = solve_all(states, needed)
    recs = {(r['n'], tuple(r['forbidden'])): r for r in audit['records']}
    if len(recs) != audit['new_closure_states']:
        errors.append('record count mismatch')
    checked = 0
    for st, rec in recs.items():
        if st not in values:
            errors.append('record state %r not in independent closure' % (st,))
            continue
        mine = values[st][:needed + 1]
        if mine != rec['prefix']:
            bad = [i for i in range(min(len(mine), len(rec['prefix'])))
                   if mine[i] != rec['prefix'][i]]
            errors.append('value mismatch %r first at %d' % (st, bad[0] if bad else -1))
            if len(errors) > 50:
                break
        checked += 1
    # window check on ALL closure states (independent certification window)
    start = audit['joint_start_candidate']
    winfail = 0
    for st in states:
        seq = values[st]
        for i in range(start, min(2 * start + 36, len(seq) - 34)):
            if seq[i] != seq[i + 34]:
                errors.append('independent window failure %r at %d' % (st, i))
                winfail += 1
                break
        if winfail > 20:
            break
    out = dict(verifier='independent-second-implementation',
               initial_types=len(initial), closure_states=len(states),
               records_checked=checked, values_through=needed,
               window_start=start, errors=errors[:50],
               verdict='PASS' if not errors else 'FAIL')
    out_path = HERE / 'output' / 'verify_independent.json'
    if audit_path == (HERE / 'output' / 'audit.json'):
        out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out))
    return 0 if not errors else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
