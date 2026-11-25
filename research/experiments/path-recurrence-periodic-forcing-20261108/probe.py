#!/usr/bin/env python3
"""Mechanism probe for K0684: does periodic forcing of the rooted-path
self-convolution recurrence preserve eventual period 34?

The exact recurrence (validated in the rooted-core experiments) is

  g(L) = mex( B(L) u {g(L-2)} u {g(i) xor p[L-3-i] : i=0..L-3} )

where p is the bare Node-Kayles path Grundy (eventual period 34) and B(L) is the
non-self "forcing" contributed by the fixed core: a finite set of constant-xor-
path-shift terms plus the values f_child(L) of strictly smaller cores, which the
K0684 induction hypothesis assumes are eventually 34-periodic.

This isolates the induction STEP from any geometry. We prescribe B(L) directly
and ask whether the solution g is forced to be eventually 34-periodic. Two
families:

  arbitrary  : B(L) is a random set, made 34-periodic from a random onset.
  structured : B(L) = {a_k xor p[L+s_k]} u {h_j[L]}, a_k small constants, s_k
               small shifts, h_j random 34-periodic sequences (modeling children).

If structured forcing always yields period 34 while arbitrary sometimes does not,
K0684's periodicity is a property of the core's specific forcing structure, not of
periodicity alone. If both always yield 34, that supports a general lemma covering
the induction step. This is an observation about an abstract recurrence, NOT a
proof of K0684 and NOT a statement about actual cores.
"""
from itertools import combinations
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107'))
from engine import mex, path_values

M = 2000
TAIL = 600
P = path_values(M + 2)


def solve(Bset):
    g = []
    for L in range(M + 1):
        opts = set(Bset[L])
        if L >= 2:
            opts.add(g[L - 2])
            opts.update(g[i] ^ P[L - 3 - i] for i in range(L - 2))
        g.append(mex(opts))
    return g


def onset34(g):
    last = -1
    for L in range(M - 34 + 1):
        if g[L] != g[L + 34]:
            last = L
    return last + 1


def min_tail_period(g):
    tail = g[M - TAIL + 1:]
    n = len(tail)
    for q in range(1, n // 2 + 1):
        if all(tail[i] == tail[i + q] for i in range(n - q)):
            return q
    return None


def arbitrary_B(rng):
    nb = rng.randint(50, 800)
    B = [None] * (M + 1)
    for L in range(min(nb + 34, M + 1)):
        B[L] = frozenset(rng.randint(0, 31) for _ in range(rng.randint(0, 5)))
    for L in range(nb + 34, M + 1):
        B[L] = B[L - 34]
    return B, dict(onset=nb)


def structured_B(rng):
    m = rng.randint(1, 4)
    terms = [(rng.randint(0, 15), rng.choice([-2, -1, 0, 1])) for _ in range(m)]
    r = rng.randint(0, 3)
    children = []
    for _ in range(r):
        nj = rng.randint(50, 700)
        h = [rng.randint(0, 31) for _ in range(min(nj + 34, M + 1))]
        h += [0] * (M + 1 - len(h))
        for L in range(nj + 34, M + 1):
            h[L] = h[L - 34]
        children.append((nj, h))
    B = []
    for L in range(M + 1):
        s = {a ^ P[max(L + d, 0)] for a, d in terms}
        s.update(h[L] for _, h in children)
        B.append(frozenset(s))
    return B, dict(constant_shift_terms=terms,
                   child_onsets=[nj for nj, _ in children])


def classify(g):
    o = onset34(g)
    q = min_tail_period(g)
    is34 = o <= M - TAIL and q is not None and 34 % q == 0
    return dict(onset34=o, min_tail_period=q, max_grundy=max(g),
                eventually_34_periodic=is34)


def main():
    t0 = time.time()
    rng = random.Random(20261108)
    records = []
    # Baseline: empty forcing (trivial core) must reproduce a 34-periodic path.
    g0 = solve([frozenset()] * (M + 1))
    base = classify(g0)
    base_matches_path = all(g0[L] == P[L + 1] for L in range(M + 1))
    print('BASELINE empty forcing:', base, 'equals p[L+1]:', base_matches_path, flush=True)
    for family, gen in [('arbitrary', arbitrary_B), ('structured', structured_B)]:
        for trial in range(25):
            B, params = gen(rng)
            g = solve(B)
            c = classify(g)
            rec = dict(family=family, trial=trial, **params, **c)
            records.append(rec)
            if not c['eventually_34_periodic']:
                print('EXCEPTION', family, trial, c, flush=True)
        done = [r for r in records if r['family'] == family]
        n34 = sum(r['eventually_34_periodic'] for r in done)
        print(family, ':', n34, '/', len(done), 'eventually 34-periodic',
              'elapsed', round(time.time() - t0, 1), flush=True)
    periods = {}
    for r in records:
        key = (r['family'], r['min_tail_period'])
        periods[key] = periods.get(key, 0) + 1
    out = dict(recurrence='g(L)=mex(B(L) u {g(L-2)} u {g(i)^p[L-3-i]:i=0..L-3})',
               bare_path_period=34, horizon=M, tail_window=TAIL,
               baseline_empty_forcing=base, baseline_equals_shifted_path=base_matches_path,
               configs_per_family=25,
               eventually_34_by_family={f: sum(r['eventually_34_periodic'] for r in records
                                               if r['family'] == f) for f in ('arbitrary', 'structured')},
               min_tail_period_histogram={f'{f}:{q}': n for (f, q), n in sorted(periods.items(),
                                                                               key=lambda kv: str(kv[0]))},
               exceptions=[r for r in records if not r['eventually_34_periodic']],
               records=records)
    target = Path(__file__).with_name('output') / 'probe.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in out.items() if k not in ('records', 'exceptions')},
                     indent=2), flush=True)
    print('TOTAL elapsed', round(time.time() - t0, 1), 's', flush=True)


if __name__ == '__main__':
    main()