#!/usr/bin/env python3
"""List unresolved S7 orbits for the smallest remaining class-1 S5 obligation."""
import argparse
import csv
import gzip
import json
from collections import defaultdict
from pathlib import Path
from audit_published_candidates import images, safe
from audit_candidate_classification import children

HERE = Path(__file__).resolve().parents[1]
SOURCE = HERE.parent/'n11-central-19-cover-20261031/output'
S5 = '00000000000000803082000000000000'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--csv',type=Path)
    p.add_argument('--determinant',action='store_true')
    args = p.parse_args()
    if args.determinant:
        from audit_additional_geometry import safe as legal_geometry
    else:
        legal_geometry = safe
    with gzip.open(HERE/'output/s5-s6-remaining-incidences.csv.gz','rt',newline='') as f:
        rows = [r for r in csv.DictReader(f) if r['s5_hex'] == S5]
    assert len(rows) == 13
    loss6 = json.loads((SOURCE/'s6sweep/s5_verdicts.json').read_text())['loss_s6_covers']
    first_loss = set().union(*(children(int(key,16)) for key in loss6))
    first_win = set()
    for name in ('s6sweep/verified.json','focus2154_62certs/verified.json','frontier2140/verified.json'):
        data = json.loads((SOURCE/name).read_text())
        assert not data['fails']
        for key,entry in data['verified'].items():
            if entry['type'] == 'WIN7':
                first_win.add(int(key,16))
            elif entry['type'] == 'LOSS7':
                first_loss.add(int(key,16))
            else:
                raise ValueError('unexpected certificate type')
    assert not first_win & first_loss
    parent_data, unknown_incidence = [],[]
    all_children, all_unknown = set(),set()
    for row in rows:
        parent = int(row['s6_hex'],16)
        raw = [i for i in range(121) if not parent >> i & 1 and legal_geometry(parent | (1<<i))]
        assert len(raw) == int(row['s6_s7_edge_cost'])
        child_moves = defaultdict(list)
        for move in raw:
            child = min(images(parent | (1<<move)))
            child_moves[child].append(move)
        cs = set(child_moves)
        assert not cs & first_win
        unknown = cs - first_loss - first_win
        all_children |= cs
        all_unknown |= unknown
        parent_data.append({'s6_hex':row['s6_hex'],'legal_moves':len(raw), 'distinct_s7_orbits':len(cs),
                            'known_first_loss_orbits':len(cs & first_loss),'unknown_s7_orbits':len(unknown)})
        for child in unknown:
            unknown_incidence.append((f'{child:032x}',row['s6_hex'],min(child_moves[child])))
    assert len(all_children) == 727 and len(all_children & first_loss) == 31 and len(all_unknown) == 696
    result = {'s5_hex':S5,'s6_orbits':len(rows),'legal_move_incidences':sum(r['legal_moves'] for r in parent_data),
              'distinct_s7_orbits':len(all_children),'known_first_loss_s7_orbits':len(all_children & first_loss),
              'known_first_win_s7_orbits':len(all_children & first_win),'unknown_s7_orbits':len(all_unknown),
              'unknown_s6_s7_incidences':len(unknown_incidence),'per_s6':parent_data,
              'scope':'known first-loss includes K0675-conditioned LOSS6 children; unknown means no matching published receipt, not a verdict'}
    if args.csv:
        with args.csv.open('w',newline='') as f:
            w=csv.writer(f,lineterminator='\n')
            w.writerow(('s7_hex','s6_hex','move_in_s6_coordinates'))
            w.writerows(sorted(unknown_incidence))
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
