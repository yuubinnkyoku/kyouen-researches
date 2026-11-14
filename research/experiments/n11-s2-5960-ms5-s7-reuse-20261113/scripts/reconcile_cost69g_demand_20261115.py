#!/usr/bin/env python3
"""Independent reconciliation of the demand-classes discrepancy flagged by
class2-lane-next-fold-prediction-independent-audit-20261115.json for the
cost-69g child 00000000000000809102000000002000 (chain demand c1=0,c2=2,c4=2
whose sum 4 was read as "4 servers" vs 3 distinct open S5 parents measured
by the third-method audit).

Method (independent of the chain scripts):
- load the complete 7,867-row ms5_s6 manifest (part1..6);
- load the 175-row open-S5 ranking at the canonical chain head
  (after-cost70c-warm3 = the 1,163 head, gain-0 extension);
- re-derive the parent-orbit serving relation geometrically: parent S5 of an
  S6 hex h is canon(h ^ 1<<s) over the 6 stones of h (D4 canonicalization,
  8 transforms, bit index 11*y + x, exact integers only);
- re-derive the chain demand semantics from the published chain source
  (recompute_frontier_full.py): the S5 'classes' field is a bitmask
  (bit 0 = class 1, bit 1 = class 2, bit 2 = class 4) and the per-child
  demand c1/c2/c4 counts each serving open S5 once per class bit set, so a
  dual-class S5 (classes=6) contributes +1 to c2 AND +1 to c4;
- count, per child, both the distinct open parent orbits and the per-class
  demand, and compare with the chain-published demand (top-candidates CSV).

No chain execution, no repo verifier import, no floating point.
"""
import csv, json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'


def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    raise FileNotFoundError([str(p) for p in paths])


# Repo layout (research/experiments/...): the manifest parts live in the
# milestone5 experiment dir; a local run keeps them under manifest/.
MANIFEST_DIR = first_existing([
    HERE / 'manifest',
    HERE.parent / 'n11-s2-5960-milestone5-20261112' / 'output',
])
# Ranking CSV: local scratch name vs the published frontier file name.
RANKING_CSV = first_existing([
    OUT / 'ranking_warm3.csv',
    OUT / 'class-frontier-s5-ranking-after-cost70c-warm3-20261115.csv',
])


def canon(v):
    pts = []
    w = v
    while w:
        b = w & -w
        pts.append(b.bit_length() - 1)
        w ^= b
    best = None
    for t in range(8):
        m = 0
        for p in pts:
            x, y = p % 11, p // 11
            if t == 0:
                xx, yy = x, y
            elif t == 1:
                xx, yy = y, 10 - x
            elif t == 2:
                xx, yy = 10 - x, 10 - y
            elif t == 3:
                xx, yy = 10 - y, x
            elif t == 4:
                xx, yy = 10 - x, y
            elif t == 5:
                xx, yy = x, 10 - y
            elif t == 6:
                xx, yy = y, x
            else:
                xx, yy = 10 - y, 10 - x
            m |= 1 << (11 * yy + xx)
        if best is None or m < best:
            best = m
    return best


def stones(v):
    pts = []
    w = v
    while w:
        b = w & -w
        pts.append(b.bit_length() - 1)
        w ^= b
    return pts


def demand_of(open_parents):
    """Chain semantics (recompute_frontier_full.py lines 114-121): per class bit."""
    d = {'c1': 0, 'c2': 0, 'c4': 0}
    for cls in open_parents:
        if cls & 1:
            d['c1'] += 1
        if cls & 2:
            d['c2'] += 1
        if cls & 4:
            d['c4'] += 1
    return d


def main():
    # ---- manifest ----
    man = {}
    for i in range(1, 7):
        with (MANIFEST_DIR / f'ms5_s6_manifest_part{i}.csv').open() as f:
            for row in csv.DictReader(f):
                h = row['hex']
                assert h not in man, 'duplicate manifest row'
                man[h] = (int(row['cost']), int(row['classes']))
    assert len(man) == 7867, len(man)

    # ---- open S5 ranking at the 1,163 head ----
    open_s5 = {}
    with RANKING_CSV.open() as f:
        for row in csv.DictReader(l for l in f if not l.startswith('#')):
            open_s5[row['s5_hex']] = (int(row['classes']), int(row['remaining_s6_orbits']),
                                      int(row['remaining_s7_edge_cost']))
    assert len(open_s5) == 175, len(open_s5)

    # ---- chain-published demand per child (top-candidates CSV) ----
    chain_demand = {}
    with (OUT / 'class-frontier-top-candidates-s6-after-cost70c-warm3-20261115.csv').open() as f:
        cur_s5 = None
        for line in f:
            line = line.rstrip('\n')
            if not line.strip() or line.startswith('#'):
                continue
            parts = next(csv.reader([line]))
            if not parts or parts[0].startswith('#') or parts[0] == 's5_hex':
                continue
            if len(parts) < 4:
                continue
            if parts[0] in open_s5:
                cur_s5 = parts[0]
            chain_demand.setdefault(parts[1], (cur_s5, parts[2], parts[3]))

    controls = [
        ('cost-69g child (claimed in flight by the parallel lane)',
         '00000000000000809102000000002000'),
        ('cost-72 child of the third target (next unswept after 69g)',
         '00000000000000809102000002000000'),
        ('cost-69f child (solved at head 1163, control)',
         '00000000000000809102000000000008'),
        ('cost-65j child (claimed in flight, pre-covered at head, control)',
         '00000000000000809102000080000000'),
    ]
    per = []
    for label, h in controls:
        v = int(h, 16)
        assert h in man, f'{h} not in manifest'
        cost, mclass = man[h]
        assert len(stones(v)) == 6, 'child must have 6 stones'
        lifts = {}
        for s in stones(v):
            p = canon(v ^ (1 << s))
            lifts.setdefault(f'{p:032x}', []).append(s)
        parents = []
        for p, srcs in sorted(lifts.items()):
            in_open = p in open_s5
            cls = open_s5[p][0] if in_open else None
            parents.append({'s5_hex': p, 'lift_stones': srcs, 'open_at_head': in_open,
                            'classes_bitmask': cls,
                            'classes_served': sorted(c for c in (1, 2, 4) if cls is not None and cls & c),
                            'remaining_s6_orbits': open_s5[p][1] if in_open else None,
                            'remaining_s7_edge_cost': open_s5[p][2] if in_open else None})
        open_cls = [p['classes_bitmask'] for p in parents if p['open_at_head']]
        dem = demand_of(open_cls)
        distinct_open = len(open_cls)
        entry = {
            'label': label, 's6_hex': h, 'manifest_cost': cost,
            'manifest_classes_bitmask': mclass,
            'distinct_parent_s5_orbits': len(parents),
            'distinct_open_parent_s5_orbits': distinct_open,
            'parents': parents,
            'per_class_demand': dem,
            'demand_sum_c1c2c4': dem['c1'] + dem['c2'] + dem['c4'],
            'chain_published_demand': chain_demand.get(h),
        }
        per.append(entry)
        pub = chain_demand.get(h)
        pub_str = pub[2] if pub else None
        mine = f"c1={dem['c1']},c2={dem['c2']},c4={dem['c4']}"
        print(f"== {label}\n   hex={h} cost={cost} parents={len(parents)} "
              f"distinct_open={distinct_open} demand={mine} chain={pub_str} "
              f"match={pub_str == mine}")
        for p in parents:
            print(f"   parent {p['s5_hex']} classes={p['classes_bitmask']} "
                  f"serves={p['classes_served']} open={p['open_at_head']} "
                  f"rem={p['remaining_s6_orbits']} lift_stones={p['lift_stones']}")

    g = per[0]
    assert g['per_class_demand'] == {'c1': 0, 'c2': 2, 'c4': 2}
    assert g['distinct_open_parent_s5_orbits'] == 3
    dual = [p for p in g['parents'] if p['open_at_head'] and p['classes_bitmask'] == 6]
    assert len(dual) == 1

    out = {
        'schema': 'n11-class2-lane-cost69g-demand-reconciliation-20261115-v1',
        'date': '2026-11-15',
        'trigger': 'class2-lane-next-fold-prediction-independent-audit-20261115.json '
                   'flagged for the cost-69g child 00000000000000809102000000002000: '
                   '"measured 3 distinct open S5 parents among the 175-row ranking" vs '
                   'the claim/chain demand c1=0,c2=2,c4=2 (read as 4 servers)',
        'state': 'canonical chain head 1163/6684/527280/4954/391003 '
                 '(class-frontier-after-cost70c-warm3-recompute-20261115.json, gain-0 '
                 'extension of the cost-69f receipts head; open-S5 set unchanged since '
                 'the 1148 state, both 175 rows)',
        'method': 'independent of the chain execution: complete 7,867-row manifest '
                  '(ms5_s6_manifest_part1..6.csv) + 175-row open-S5 ranking at the head '
                  '(class-frontier-s5-ranking-after-cost70c-warm3-20261115.csv); parent '
                  'orbits re-derived geometrically as canon(h ^ 1<<s) over the 6 stones '
                  'of h with an exact D4 canonicalization (8 transforms, bit index '
                  '11*y+x, validated against published canonical hexes and the 69f '
                  'child->parent pair); demand semantics re-derived from the published '
                  'chain source recompute_frontier_full.py: the S5 classes field is a '
                  'bitmask (bit 0 = class 1, bit 1 = class 2, bit 2 = class 4) and '
                  'per-child demand counts each serving open S5 once per set class bit',
        'finding': {
            'resolution': 'NO bookkeeping error on either side. The cost-69g child has '
                          'exactly 3 distinct open parent S5 orbits at the 1,163 head; '
                          'one of them (00000000000000801202000000080000) is a '
                          'dual-class S5 with classes bitmask 6 (serves BOTH the class-2 '
                          'and the class-4 demand), so the per-class demand is '
                          'c1=0, c2=2, c4=2 whose SUM is 4. The third-method audit '
                          'counted distinct open parents (3, correct); the claim '
                          'records the per-class demand (c1=0,c2=2,c4=2, correct); '
                          'reading c1+c2+c4 as a distinct-server count created the '
                          'apparent discrepancy',
            'open_parents_of_the_69g_child': [
                {'s5_hex': p['s5_hex'], 'classes_bitmask': p['classes_bitmask'],
                 'classes_served': p['classes_served'],
                 'remaining_s6_orbits': p['remaining_s6_orbits'],
                 'remaining_s7_edge_cost': p['remaining_s7_edge_cost'],
                 'lift_stone': p['lift_stones'][0]}
                for p in g['parents'] if p['open_at_head']],
            'demand_semantics_confirmed': 'per-class counts, not distinct-server '
                                          'counts; a classes=6 S5 contributes to both '
                                          'c2 and c4 (chain source '
                                          'recompute_frontier_full.py: if bits&2: '
                                          'c2+=1; if bits&4: c4+=1)',
            'recommendation': 'claims and audits should state BOTH numbers '
                              '(distinct open parents = 3, per-class demand '
                              'c1=0,c2=2,c4=2) to prevent the same misreading; the '
                              'audit-blocked S5 00000000000000809082000000000000 has '
                              'classes bitmask 3 (class-1 AND class-2 demand) - its '
                              'children all carry c1>=1 and are therefore excluded '
                              'from the open_classes (c1==0) frontier accounting, '
                              'which is the structural reason it is '
                              'receipt-unclosable within this ledger',
        },
        'controls': [
            {'label': e['label'], 's6_hex': e['s6_hex'], 'manifest_cost': e['manifest_cost'],
             'manifest_classes_bitmask': e['manifest_classes_bitmask'],
             'distinct_parent_s5_orbits': e['distinct_parent_s5_orbits'],
             'distinct_open_parent_s5_orbits': e['distinct_open_parent_s5_orbits'],
             'per_class_demand': e['per_class_demand'],
             'demand_sum_c1c2c4': e['demand_sum_c1c2c4'],
             'matches_chain_published_demand': (
                 e['chain_published_demand'][2] ==
                 f"c1={e['per_class_demand']['c1']},c2={e['per_class_demand']['c2']},"
                 f"c4={e['per_class_demand']['c4']}") if e['chain_published_demand'] else None,
             'parents': e['parents']}
            for e in per
        ],
        'interpretation_guard': 'bookkeeping over published receipts and the static '
                                'manifest; demand counts measure how many open S5 '
                                'orbits per class a remaining S6 orbit serves, not the '
                                'game-theoretic value of any position; REFUTED-D10 '
                                'sweeps prove only absence of WIN7-D10; 11x11 empty '
                                'board / two-stone root {49,60} / S2 {59,60} / class 2 '
                                '/ class 4 remain UNKNOWN',
    }
    (OUT / 'class2-lane-cost69g-demand-reconciliation-20261115.json').write_text(
        json.dumps(out, indent=1) + '\n')
    print('written class2-lane-cost69g-demand-reconciliation-20261115.json')


if __name__ == '__main__':
    main()
