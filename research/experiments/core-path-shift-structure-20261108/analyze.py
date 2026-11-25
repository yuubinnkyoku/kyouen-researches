#!/usr/bin/env python3
"""Structural probe for K0684/K0697: is f_C(L) eventually a shift of the bare path p?

The bare path (Node-Kayles on a path) has Grundy sequence p with eventual period
34. K0684 conjectures every fixed core C attached to a long path is eventually
34-periodic. A strong structural explanation would be f_C(L) = p_{L+s(C)} for all
large L (a core-dependent shift), since then period 34 is inherited from p.

We test this on two certified families:
  - six: all 10688 six-vertex pure-three-edge cores (prefix 0..1343), deep tail
    window L=900..1300, tail block f[1000:1034].
  - le5: all 513 rank<=3 cores on <=5 vertices (K0682, prefix 0..1069), tail
    window L=600..1000, tail block f[700:734].

For each type we scan shifts s and count exact matches f_C[L]==p[L+s] over the
tail window, test the weaker shift-xor form f_C[L]=p[L+s]^c, count distinct
period-34 tail blocks and their minimum periods, and correlate pure shifts with
the core's own Grundy ordinary(C). Exploratory structural analysis, not a proof.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107'))
from engine import ordinary, path_values

HERE = Path(__file__).resolve().parent
SHIFTS = range(-10, 81)
CONFIGS = [
    dict(name='six',
         audit=ROOT / 'research/experiments/rooted-core-six-pure-triple-full-20261108/output/audit.json',
         lo=900, hi=1300, blo=1000, out='shift_probe.json', per='per_type.json'),
    dict(name='le5',
         audit=ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107/output/audit.json',
         lo=600, hi=1000, blo=700, out='shift_probe_le5.json', per='per_type_le5.json'),
]


def has_period(b, q):
    return all(b[i] == b[i + q] for i in range(len(b) - q))


def analyze(cfg):
    data = json.loads(cfg['audit'].read_text(encoding='utf-8'))
    records = data['records']
    lo, hi, blo = cfg['lo'], cfg['hi'], cfg['blo']
    span = hi - lo + 1
    p = path_values(hi + 90)
    perfect_shift = Counter()
    perfect_shiftxor = Counter()
    best_match_hist = Counter()
    tail_blocks = Counter()
    shift_vs_grundy = defaultdict(Counter)
    shift_vs_edges = defaultdict(Counter)
    shift_vs_root = defaultdict(Counter)
    per_type = []
    examples = []
    n_perfect_shift = n_perfect_shiftxor = 0
    for row in records:
        f = row['prefix']
        n = row['n']
        forb = tuple(row['forbidden'])
        best_s, best_m = None, -1
        for s in SHIFTS:
            m = sum(1 for L in range(lo, hi + 1) if f[L] == p[L + s])
            if m > best_m:
                best_m, best_s = m, s
        best_match_hist[best_m] += 1
        block = tuple(f[blo:blo + 34])
        tail_blocks[block] += 1
        is_perfect = best_m == span
        if is_perfect:
            n_perfect_shift += 1
            perfect_shift[best_s] += 1
            g0 = ordinary((n, forb))
            shift_vs_grundy[best_s][g0] += 1
            shift_vs_edges[best_s][len(forb)] += 1
            shift_vs_root[best_s][int(any(e & 1 for e in forb))] += 1
            if len(examples) < 8:
                examples.append((row['forbidden'], best_s))
        c = f[lo] ^ p[lo + best_s]
        if all(f[L] == (p[L + best_s] ^ c) for L in range(lo, hi + 1)):
            n_perfect_shiftxor += 1
            perfect_shiftxor[(best_s, c)] += 1
        per_type.append(dict(n=n, forbidden=forb, best_shift=best_s,
                             best_match=best_m, perfect_shift=is_perfect))
    shift_blocks = {tuple(p[blo + s:blo + 34 + s]) for s in SHIFTS}
    distinct_tail = len(tail_blocks)
    distinct_tail_shift_of_p = sum(1 for b in tail_blocks if b in shift_blocks)
    min_period_types = Counter()
    for b, cnt in tail_blocks.items():
        if has_period(b, 1):
            min_period_types['period1'] += cnt
        elif has_period(b, 2):
            min_period_types['period2'] += cnt
        elif has_period(b, 17):
            min_period_types['period17'] += cnt
        else:
            min_period_types['minperiod34'] += cnt
    out = dict(
        family=cfg['name'], types=len(records), tail_window=[lo, hi], tail_span=span,
        shift_range=[min(SHIFTS), max(SHIFTS)],
        perfect_pure_shift_types=n_perfect_shift,
        perfect_pure_shift_by_offset=dict(sorted(perfect_shift.items())),
        perfect_shiftxor_types=n_perfect_shiftxor,
        perfect_shiftxor_by_offset={f'{s},{c}': v for (s, c), v in sorted(perfect_shiftxor.items())},
        best_match_count_histogram={str(k): v for k, v in sorted(best_match_hist.items())},
        distinct_period34_tail_blocks=distinct_tail,
        distinct_tail_blocks_that_are_path_shifts=distinct_tail_shift_of_p,
        types_by_minimum_tail_period=dict(min_period_types),
        largest_tail_block_class=tail_blocks.most_common(1)[0][1],
        shift_vs_core_grundy={str(s): dict(sorted(c.items())) for s, c in sorted(shift_vs_grundy.items())},
        shift_vs_edge_count={str(s): dict(sorted(c.items())) for s, c in sorted(shift_vs_edges.items())},
        shift_vs_root_membership={str(s): dict(sorted(c.items())) for s, c in sorted(shift_vs_root.items())},
        perfect_shift_examples=examples,
    )
    (HERE / 'output' / cfg['out']).write_text(json.dumps(out, indent=2), encoding='utf-8')
    (HERE / 'output' / cfg['per']).write_text(json.dumps(per_type, separators=(',', ':')), encoding='utf-8')
    return out


def main():
    summary = {}
    for cfg in CONFIGS:
        out = analyze(cfg)
        summary[cfg['name']] = {k: out[k] for k in (
            'types', 'perfect_pure_shift_types', 'perfect_pure_shift_by_offset',
            'distinct_period34_tail_blocks', 'distinct_tail_blocks_that_are_path_shifts',
            'types_by_minimum_tail_period', 'shift_vs_core_grundy')}
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()