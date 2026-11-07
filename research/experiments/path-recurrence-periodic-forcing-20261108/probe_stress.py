#!/usr/bin/env python3
"""Harder stress test of the K0684 mechanism probe (round 2).

Round 1 (probe.py) found that ALL 50 eventually-34-periodic forcings (arbitrary
random sets and structured constant-xor-path-shift + periodic children) drove the
recurrence

  g(L) = mex( B(L) u {g(L-2)} u {g(i) xor p[L-3-i] : i=0..L-3} )

to eventual minimal period exactly 34. This round attacks that robustness with
much larger forcing values (0..255 and 0..1023), larger option sets, more periodic
children, longer child preperiods, and a longer horizon (M=4000). If period 34
still always emerges, the "absorption" mechanism is very robust and motivates a
general lemma covering the K0684 induction step. Any exception (longer period,
divisor period, non-periodicity, or onset beyond the horizon) bounds the claim.

Observation about an abstract recurrence, NOT a proof of K0684.
"""
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107'))
from engine import mex, path_values

M = 4000
TAIL = 900
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


def periodic_random_sequence(rng, vmax, onset_lo, onset_hi):
    n = rng.randint(onset_lo, onset_hi)
    h = [rng.randint(0, vmax) for _ in range(min(n + 34, M + 1))]
    h += [0] * (M + 1 - len(h))
    for L in range(n + 34, M + 1):
        h[L] = h[L - 34]
    return n, h


def arbitrary_B(rng, vmax, maxset, onset_hi):
    nb = rng.randint(50, onset_hi)
    B = [None] * (M + 1)
    for L in range(min(nb + 34, M + 1)):
        B[L] = frozenset(rng.randint(0, vmax) for _ in range(rng.randint(0, maxset)))
    for L in range(nb + 34, M + 1):
        B[L] = B[L - 34]
    return B, dict(onset=nb, vmax=vmax, maxset=maxset)


def structured_B(rng, vmax, maxset, onset_hi):
    m = rng.randint(1, 6)
    terms = [(rng.randint(0, vmax), rng.choice([-3, -2, -1, 0, 1, 2])) for _ in range(m)]
    r = rng.randint(0, 5)
    children = [periodic_random_sequence(rng, vmax, 50, onset_hi) for _ in range(r)]
    B = []
    for L in range(M + 1):
        s = {a ^ P[max(L + d, 0)] for a, d in terms}
        s.update(h[L] for _, h in children)
        B.append(frozenset(s))
    return B, dict(constant_shift_terms=terms, child_onsets=[n for n, _ in children],
                   vmax=vmax)


def classify(g):
    o = onset34(g)
    q = min_tail_period(g)
    is34 = o <= M - TAIL and q is not None and 34 % q == 0
    return dict(onset34=o, min_tail_period=q, max_grundy=max(g),
                eventually_34_periodic=is34)


def main():
    t0 = time.time()
    rng = random.Random(31415926)
    records = []
    families = [
        ('arbitrary255', lambda r: arbitrary_B(r, 255, 15, 1500), 40),
        ('structured255', lambda r: structured_B(r, 255, 15, 1500), 40),
        ('arbitrary1023', lambda r: arbitrary_B(r, 1023, 25, 2000), 20),
    ]
    for family, gen, count in families:
        for trial in range(count):
            B, params = gen(rng)
            g = solve(B)
            c = classify(g)
            rec = dict(family=family, trial=trial, **params, **c)
            records.append(rec)
            if not c['eventually_34_periodic']:
                rec['tail_sample'] = g[M - 60:]
                print('EXCEPTION', family, trial, c, flush=True)
        done = [r for r in records if r['family'] == family]
        n34 = sum(r['eventually_34_periodic'] for r in done)
        onsets = sorted(r['onset34'] for r in done if r['eventually_34_periodic'])
        print(family, ':', n34, '/', len(done), 'eventually 34-periodic',
              'onset max', (onsets[-1] if onsets else None),
              'elapsed', round(time.time() - t0, 1), flush=True)
    periods = {}
    for r in records:
        key = (r['family'], r['min_tail_period'])
        periods[key] = periods.get(key, 0) + 1
    out = dict(recurrence='g(L)=mex(B(L) u {g(L-2)} u {g(i)^p[L-3-i]:i=0..L-3})',
               bare_path_period=34, horizon=M, tail_window=TAIL, seed=31415926,
               eventually_34_by_family={f: sum(r['eventually_34_periodic'] for r in records
                                               if r['family'] == f) for f, _, _ in families},
               configs_by_family={f: n for f, _, n in families},
               min_tail_period_histogram={f'{f}:{q}': n for (f, q), n in sorted(periods.items(),
                                                                               key=lambda kv: str(kv[0]))},
               onset34_max_by_family={f: max((r['onset34'] for r in records if r['family'] == f
                                              and r['eventually_34_periodic']), default=None)
                                      for f, _, _ in families},
               max_grundy_overall=max(r['max_grundy'] for r in records),
               exceptions=[r for r in records if not r['eventually_34_periodic']],
               records=records)
    target = Path(__file__).with_name('output') / 'stress.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in out.items() if k not in ('records', 'exceptions')},
                     indent=2), flush=True)
    print('TOTAL elapsed', round(time.time() - t0, 1), 's', flush=True)


if __name__ == '__main__':
    main()