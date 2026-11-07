#!/usr/bin/env python3
"""Structural probe for K0684: is f_C(L) eventually a shift of the bare path p?

The bare path (Node-Kayles on a path) has Grundy sequence p with eventual period
34. K0684 conjectures every fixed core C attached to a long path is eventually
34-periodic. A strong structural explanation would be f_C(L) = p_{L+s(C)} for all
large L (a core-dependent shift), since then period 34 is inherited from p.

We test this on the certified pure-triple six-vertex audit (10688 types, prefixes
0..1343). For each type we scan shifts s and count exact matches f_C[L]==p[L+s]
over a deep tail window, and also test the weaker shift-xor form f_C[L]=p[L+s]^c.
This is an exploratory structural analysis, not a proof.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107'))
from engine import ordinary, path_values

AUDIT = ROOT / 'research/experiments/rooted-core-six-pure-triple-full-20261108/output/audit.json'
LO, HI = 900, 1300          # deep tail window (inclusive)
SHIFTS = range(-10, 81)


def main():
    data = json.loads(AUDIT.read_text(encoding='utf-8'))
    records = data['records']
    p = path_values(HI + 90)
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
        forb = tuple(row['forbidden'])
        best_s, best_m = None, -1
        for s in SHIFTS:
            m = sum(1 for L in range(LO, HI + 1) if f[L] == p[L + s])
            if m > best_m:
                best_m, best_s = m, s
        span = HI - LO + 1
        best_match_hist[best_m] += 1
        block = tuple(f[1000:1034])
        tail_blocks[block] += 1
        is_perfect = best_m == span
        if is_perfect:
            n_perfect_shift += 1
            perfect_shift[best_s] += 1
            g0 = ordinary((6, forb))
            ne = len(forb)
            root_in = any(e & 1 for e in forb)
            shift_vs_grundy[best_s][g0] += 1
            shift_vs_edges[best_s][ne] += 1
            shift_vs_root[best_s][int(root_in)] += 1
            if len(examples) < 8:
                examples.append((row['forbidden'], best_s))
        c = f[LO] ^ p[LO + best_s]
        if all(f[L] == (p[L + best_s] ^ c) for L in range(LO, HI + 1)):
            n_perfect_shiftxor += 1
            perfect_shiftxor[(best_s, c)] += 1
        per_type.append(dict(forbidden=forb, best_shift=best_s, best_match=best_m,
                             perfect_shift=is_perfect))
    # how many distinct tail blocks are pure shifts of the path block?
    pblock = tuple(p[1000:1034])
    shift_blocks = {tuple(p[1000 + s:1034 + s]) for s in SHIFTS}
    distinct_tail = len(tail_blocks)
    distinct_tail_shift_of_p = sum(1 for b in tail_blocks if b in shift_blocks)

    def has_period(b, q):
        return all(b[i] == b[i + q] for i in range(34 - q))
    min_period_types = Counter()
    for b, n in tail_blocks.items():
        if has_period(b, 1):
            min_period_types['period1'] += n
        elif has_period(b, 2):
            min_period_types['period2'] += n
        elif has_period(b, 17):
            min_period_types['period17'] += n
        else:
            min_period_types['minperiod34'] += n
    out = dict(
        types=len(records), tail_window=[LO, HI], tail_span=HI - LO + 1,
        shift_range=[min(SHIFTS), max(SHIFTS)],
        perfect_pure_shift_types=n_perfect_shift,
        perfect_pure_shift_by_offset=dict(sorted(perfect_shift.items())),
        perfect_shiftxor_types=n_perfect_shiftxor,
        perfect_shiftxor_by_offset={f'{s},{c}': n for (s, c), n in sorted(perfect_shiftxor.items())},
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
    target = Path(__file__).with_name('output') / 'shift_probe.json'
    target.write_text(json.dumps(out, indent=2), encoding='utf-8')
    (Path(__file__).with_name('output') / 'per_type.json').write_text(
        json.dumps(per_type, separators=(',', ':')), encoding='utf-8')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()