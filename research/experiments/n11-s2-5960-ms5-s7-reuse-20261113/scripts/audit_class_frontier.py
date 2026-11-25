#!/usr/bin/env python3
"""Fresh class-2/4 frontier ranking over the latest published receipts.

Recomputes, per unresolved S5 orbit, the remaining S6 orbits after
win7-reuse-hits, the covers() of every verified WIN7 certificate root,
and the three refuted LOSS6 keys, then ranks the blocker candidates of
the open classes (2 = {27,93}, 4 = {23,31,89,97}) and counts how many
remaining S6 orbits each certificate would close (demand).

Snapshot audit: the asserts pin the counts at the baseline main noted in
the roadmap JSON; later certificates invalidate them by design.
"""
import csv
import gzip
import json
from collections import defaultdict
from pathlib import Path

from audit_published_candidates import images

HERE = Path(__file__).resolve().parents[1]
MS5 = HERE.parent / 'n11-s2-5960-milestone5-20261112' / 'output'
WIN7_VERIFIED = (
    'priority-certificates-verified.json',
    'class2-certificates-verified.json',
    'class2-next-certificates-verified.json',
    'class2-next2-certificates-verified.json',
    'class2-next3-certificates-verified.json',
    'class2-next4-certificates-verified.json',
    'class2-batch5-certificates-verified.json',
    'class2-batch3-certificates-verified.json',
    'class2-batch2-certificates-verified.json',
    'class2-batch2b-certificates-verified.json',
    'class2-batch1-certificates-verified.json',
    'class2-batch1b-certificates-verified.json',
)
LOSS6 = (
    '00000000000000809202000400000000',
    '00000000000000003800004008000008',
    '00000000000000805202000000002000',
)


def covers(root):
    return {min(images(root ^ (1 << i))) for i in range(121) if root >> i & 1}


def main():
    winners = set()
    with gzip.open(HERE / 'output/win7-reuse-hits.csv.gz', 'rt', newline='') as f:
        for row in csv.DictReader(f):
            winners.add(int(row['s6_hex'], 16))
    solved = set(winners)
    for name in WIN7_VERIFIED:
        for rec in json.loads((HERE / 'output' / name).read_text())['certificates']:
            if rec['verdict'] == 'WIN7':
                solved |= covers(int(rec['root'], 16))
    manifest = set()
    for path in sorted(MS5.glob('ms5_s6_manifest_part*.csv')):
        with path.open(newline='') as f:
            manifest.update(int(row['hex'], 16) for row in csv.DictReader(f))
    classes = {}
    with gzip.open(HERE / 'output/s5-remaining-after-reuse.csv.gz', 'rt', newline='') as f:
        for row in csv.DictReader(f):
            classes[row['s5_hex']] = int(row['classes'])
    incidences = []
    with gzip.open(HERE / 'output/s5-s6-remaining-incidences.csv.gz', 'rt', newline='') as f:
        incidences = list(csv.DictReader(f))
    assert len(incidences) == 14558 and len(winners) == 498 and len(classes) == 186
    assert len(manifest) == 7867 and len(solved & manifest) == 638

    loss = {int(x, 16) for x in LOSS6}
    rejected = {r['s5_hex'] for r in incidences if int(r['s6_hex'], 16) in loss}
    remaining = defaultdict(list)
    for row in incidences:
        if row['s5_hex'] not in rejected and int(row['s6_hex'], 16) not in solved:
            remaining[row['s5_hex']].append(row)
    unique = {r['s6_hex']: int(r['s6_s7_edge_cost']) for rows in remaining.values() for r in rows}
    assert (len(rejected), len(remaining), len(unique)) == (8, 177, 7208)
    assert sum(unique.values()) == 565500

    demand = defaultdict(lambda: {'c1': 0, 'c2': 0, 'c4': 0})
    for s5, rows in remaining.items():
        bits = classes.get(s5, 0)
        for row in rows:
            d = demand[row['s6_hex']]
            if bits & 1:
                d['c1'] += 1
            if bits & 2:
                d['c2'] += 1
            if bits & 4:
                d['c4'] += 1
    open_only = {k: v for k, v in demand.items() if v['c1'] == 0}
    assert (len(demand) - len(open_only), len(open_only)) == (1783, 5425)
    hist = defaultdict(int)
    for v in open_only.values():
        hist[f"c2={v['c2']},c4={v['c4']}"] += 1
    assert dict(hist) == {
        'c2=0,c4=1': 531, 'c2=0,c4=2': 3078, 'c2=0,c4=3': 35,
        'c2=1,c4=0': 279, 'c2=1,c4=1': 65, 'c2=1,c4=2': 9,
        'c2=2,c4=0': 1356, 'c2=2,c4=1': 6, 'c2=2,c4=2': 66,
    }

    def summary(s5_hex):
        rows = remaining[s5_hex]
        return {
            's5_hex': s5_hex,
            'classes': classes.get(s5_hex, 0),
            'remaining_s6_orbits': len(rows),
            'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows),
        }

    def best(bit):
        ranked = sorted(
            (summary(k) for k in remaining if classes.get(k, 0) & bit),
            key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']),
        )
        return ranked

    class2, class4 = best(2), best(4)
    assert class2[0]['s5_hex'] == '00000000000000003802000008000000'
    assert (class2[0]['remaining_s6_orbits'], class2[0]['remaining_s7_edge_cost']) == (32, 2206)
    assert class4[0]['s5_hex'] == '00000000020000003800000080000000'
    assert (class4[0]['remaining_s6_orbits'], class4[0]['remaining_s7_edge_cost']) == (43, 3391)

    ranking = sorted(
        (summary(k) for k in remaining),
        key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                       r['remaining_s7_edge_cost'], r['s5_hex']),
    )
    with (HERE / 'output/class-frontier-s5-ranking.csv').open('w', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
        for r in ranking:
            w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'], r['remaining_s7_edge_cost']))
    with (HERE / 'output/class-frontier-top-candidates-s6.csv').open('w', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                            ('best class-2 blocker-candidate S5 (current lane target check)', class2[0])):
            w.writerow((f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                        f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"))
            w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
            for row in sorted(remaining[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
                d = demand[row['s6_hex']]
                w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                            f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))

    print(json.dumps({
        'remaining_s5_orbits': len(remaining),
        'unique_remaining_s6': len(unique),
        'sum_remaining_cost': sum(unique.values()),
        'solved_s6_in_manifest': len(solved & manifest),
        'class_composition': {
            'bit1': sum(1 for k in remaining if classes.get(k, 0) & 1),
            'bit2': sum(1 for k in remaining if classes.get(k, 0) & 2),
            'bit4': sum(1 for k in remaining if classes.get(k, 0) & 4),
        },
        'effective_open_worklist': {
            's6_needed_only_by_closed_class1': len(demand) - len(open_only),
            's6_needed_by_open_classes': len(open_only),
            'cost_needed_by_open_classes': sum(int(unique[k]) for k in open_only),
        },
        'demand_histogram_open_only': dict(sorted(hist.items())),
        'best_class2': class2[0],
        'next_class2_candidates': class2[1:4],
        'best_class4': class4[0],
        'scope': 'bookkeeping over published receipts; no new verdict; '
                 '11x11 empty root / {49,60} / S2 {59,60}: UNKNOWN',
    }, indent=2))


if __name__ == '__main__':
    main()
