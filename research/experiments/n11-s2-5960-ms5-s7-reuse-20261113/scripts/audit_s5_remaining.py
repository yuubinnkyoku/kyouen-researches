#!/usr/bin/env python3
"""Recount each unresolved S5's remaining S6 orbits after WIN7 reuse."""
import argparse
import csv
import gzip
import json
from collections import Counter
from pathlib import Path
from audit_published_candidates import images, safe

HERE = Path(__file__).resolve().parents[1]
EXP = HERE.parent
MS5 = EXP/'n11-s2-5960-milestone5-20261112/output'
SWEEP = EXP/'n11-central-19-cover-20261031/output/s6sweep/sweep_results.json'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pairs-csv',type=Path)
    parser.add_argument('--parents-csv',type=Path)
    parser.add_argument('--determinant',action='store_true',help='use the independent determinant geometry predicate')
    args = parser.parse_args()
    if args.determinant:
        from audit_additional_geometry import safe as legal_geometry
    else:
        legal_geometry = safe
    s5s = json.loads((MS5/'ms5_s5_worklist.json').read_text())['entries']
    sweep = json.loads(SWEEP.read_text())
    manifest = {}
    for path in sorted(MS5.glob('ms5_s6_manifest_part*.csv')):
        with path.open(newline='') as f:
            for row in csv.DictReader(f):
                key = int(row['hex'],16)
                assert key not in manifest
                manifest[key] = row
    with gzip.open(HERE/'output/win7-reuse-hits.csv.gz','rt',newline='') as f:
        winners = {int(r['s6_hex'],16) for r in csv.DictReader(f)}
    assert len(s5s) == 196 and len(manifest) == 7867 and len(winners) == 498
    remaining_rows, pairs = [],[]
    known_loss = 0
    for entry in s5s:
        parent = int(entry['hex'],16)
        assert parent.bit_count() == 5 and parent == min(images(parent))
        concrete = [i for i in range(121) if not parent >> i & 1 and legal_geometry(parent | (1<<i))]
        assert len(concrete) == entry['children']
        children = {min(images(parent | (1<<i))) for i in concrete}
        judged_loss = {c for c in children if sweep.get(f'{c:032x}',{}).get('verdict') == 'LOSS_for_mover'}
        assert bool(judged_loss) == entry['hasJudgedLossChild']
        if judged_loss:
            known_loss += 1
            continue
        unjudged = {c for c in children if f'{c:032x}' not in sweep}
        assert unjudged <= manifest.keys()
        missing = sorted(unjudged - winners)
        solved = len(unjudged & winners)
        for child in missing:
            pairs.append((entry['hex'],f'{child:032x}',int(manifest[child]['cost'])))
        remaining_rows.append((entry['hex'],entry['classes'],len(children),len(unjudged),solved,
                               len(missing),sum(int(manifest[c]['cost']) for c in missing)))
    assert known_loss == 10 and len(remaining_rows) == 186
    remaining_rows.sort(key=lambda r:(r[5],r[6],r[0]))
    pairs.sort()
    missing_counts = Counter(row[5] for row in remaining_rows)
    result = {'total_s5_orbits':len(s5s),'already_second_win_s5':known_loss,
              'remaining_s5_orbits':len(remaining_rows),
              'newly_closed_s5':missing_counts[0],
              'minimum_missing_s6_orbits':min(missing_counts),
              's5_s6_remaining_orbit_incidences':len(pairs),
              'sum_of_incidence_costs':sum(r[2] for r in pairs),
              'missing_s6_orbits_histogram':dict(sorted(missing_counts.items())),
              'least_missing':{'s5_hex':remaining_rows[0][0],'classes':remaining_rows[0][1],
                               'missing_s6_orbits':remaining_rows[0][5],
                               'missing_s7_edge_cost':remaining_rows[0][6]},
              'least_missing_by_class':{str(bit):{'s5_hex':best[0], 'classes':best[1],
                                                'missing_s6_orbits':best[5], 'missing_s7_edge_cost':best[6]}
                                        for bit in (1,2,4)
                                        for best in [next(row for row in remaining_rows if row[1] & bit)]},
              'scope':'conditional on sweep verdicts, prior S5 worklist and WIN7 receipt records; costs count S5-S6 incidences'}
    if args.parents_csv:
        with args.parents_csv.open('w',newline='') as f:
            w=csv.writer(f,lineterminator='\n')
            w.writerow(('s5_hex','classes','distinct_s6_orbits','unjudged_s6_orbits','reused_win_s6_orbits','remaining_s6_orbits','remaining_s7_edge_cost'))
            w.writerows(remaining_rows)
    if args.pairs_csv:
        with args.pairs_csv.open('w',newline='') as f:
            w=csv.writer(f,lineterminator='\n')
            w.writerow(('s5_hex','s6_hex','s6_s7_edge_cost'))
            w.writerows(pairs)
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
