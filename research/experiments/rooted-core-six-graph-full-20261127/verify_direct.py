#!/usr/bin/env python3
"""Primitive labeled-position verifier (third implementation axis).

For a stratified deterministic sample of family states and small path lengths,
compute the Grundy value of the labeled position (core + two-point path
attached at the root) by direct memoized game recursion on the remaining
vertex set, using ONLY the primitive move semantics of the K0682 proof:

  move at v: remove v from the legal set; every forbidden edge shrinks by v;
  any edge shrunk to a single remaining vertex blocks that vertex (removed from
  the legal set); edges containing a blocked or earlier-removed vertex are
  inert (they can never block again - matching the pinned engine's rule that
  edges outside the active set are discarded).

No canonical forms, no remap, no path value tables, no recurrence assembly.
Compared against the official audit.json record prefixes. Fail-closed.
"""
import json
import random
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent


def grundy_of_position(n, core_edges, L):
    """Labeled game on vertices 0..n-1 (core, root=0) plus path v_i = n+i (i<L),
    edges = core_edges U {(0,n),(n,n+1),...}. Direct recursion on remaining set."""
    total = n + L
    edges = set(core_edges)
    for i in range(L):
        edges.add((1 << (n + i)) | (1 << (0 if i == 0 else n + i - 1)))
    full = (1 << total) - 1

    def moves(R):
        out = []
        for v in range(total):
            bit = 1 << v
            if not R & bit:
                continue
            blocked = 0
            for e in edges:
                e2 = e & ~bit
                # edge shrunk by v; blocks its single vertex if that vertex is
                # still remaining and the rest of the edge is already gone
                if e2 and (e2 & (e2 - 1)) == 0 and (e2 & R) == e2:
                    blocked |= e2
            out.append(R & ~bit & ~blocked)
        return out

    @lru_cache(maxsize=None)
    def g(R):
        opts = set()
        for R2 in moves(R):
            opts.add(g(R2))
        v = 0
        while v in opts:
            v += 1
        return v

    return g(full)


def main():
    audit = json.loads((HERE / 'output' / 'audit.json').read_text())
    records = audit['records']
    rng = random.Random(20261127)  # deterministic stratified sample
    by_stratum = {}
    for r in records:
        by_stratum.setdefault(len(r['forbidden']), []).append(r)
    sample = []
    for k in sorted(by_stratum):
        pool = by_stratum[k]
        for r in rng.sample(pool, min(6, len(pool))):
            sample.append(r)
    errors = []
    checked = 0
    for r in sample:
        n, forbidden = r['n'], list(r['forbidden'])
        for L in range(0, 9):
            gv = grundy_of_position(n, forbidden, L)
            official = r['prefix'][L]
            checked += 1
            if gv != official:
                errors.append('direct mismatch state (n=%d, %s) L=%d: direct=%d official=%d'
                              % (n, forbidden, L, gv, official))
            if len(errors) > 20:
                break
        if len(errors) > 20:
            break
    out = dict(verifier='primitive-direct-labeled',
               sample_states=len(sample), lengths=9, comparisons=checked,
               errors=errors[:20], verdict='PASS' if not errors else 'FAIL')
    (HERE / 'output' / 'verify_direct.json').write_text(json.dumps(out, indent=2))
    print(json.dumps(out))
    return 0 if not errors else 1


if __name__ == '__main__':
    sys.exit(main())
