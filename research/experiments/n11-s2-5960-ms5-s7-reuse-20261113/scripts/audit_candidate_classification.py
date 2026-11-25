#!/usr/bin/env python3
"""Classify oracle-completing candidates against published conditional pools.

WIN7/LOSS7 mean the original first player's outcome, not the S7 mover's.
The sweep pool is only a possible WIN7 witness, not a verdict.
"""
import argparse
from collections import Counter
import csv
import gzip
import json
from pathlib import Path
from audit_published_candidates import images, safe

HERE = Path(__file__).resolve().parents[1]
EXP = HERE.parent
ORACLE = EXP/'n11-central-19-cover-20261031/output/s6sweep/s5_verdicts.json'
FOCUS = EXP/'n11-central-19-cover-20261031/output/focus2154_62certs/verified.json'


def children(mask):
    result = set()
    for move in range(121):
        if not mask >> move & 1:
            child = mask | 1 << move
            if safe(child):
                result.add(min(images(child)))
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--csv',type=Path)
    args = p.parse_args()
    data = json.loads(ORACLE.read_text())
    bases = [int(x,16) for x in data['first_win_s5']+data['second_win_s5']]
    loss6 = [int(x,16) for x in data['loss_s6_covers']]
    assert len(bases) == 94 and len(loss6) == 14
    sweep = set().union(*(children(x) for x in bases))
    loss7_from_loss6 = set().union(*(children(x) for x in loss6))
    assert len(sweep) == 3868 and len(loss7_from_loss6) == 907
    direct = json.loads(FOCUS.read_text())['verified']
    certified_loss7 = {int(k,16) for k,v in direct.items() if v['type'] == 'LOSS7'}
    certified_win7 = {int(k,16) for k,v in direct.items() if v['type'] == 'WIN7'}
    assert (len(certified_loss7),len(certified_win7)) == (35,27)
    assert not loss7_from_loss6 & certified_win7
    rows = []
    for path in sorted((HERE/'output').glob('ms5_s7_reuse_candidates_part*.csv')):
        with path.open(newline='') as f:
            for row in csv.reader(f):
                if row[0] != 's7_hex':
                    rows.append((int(row[0],16),int(row[1],16),'published',row[3]))
    with gzip.open(HERE/'output/additional-candidates.csv.gz','rt',newline='') as f:
        rows.extend((int(r['s7_hex'],16),int(r['s6_hex'],16),'additional',None) for r in csv.DictReader(f))
    assert len(rows) == len({r[0] for r in rows}) == 15072
    classified = []
    counts = Counter()
    parents = {key:set() for key in ('published','additional','all')}
    for child,parent,origin,old_cat in rows:
        direct_win = child in certified_win7
        first_loss = child in certified_loss7 or child in loss7_from_loss6
        assert not (direct_win and first_loss)
        in_sweep = any(min(images(child ^ (1<<i))) in sweep for i in range(121) if child >> i & 1)
        if direct_win:
            cls = 'certified_first_win'
        elif first_loss:
            cls = 'conditional_first_loss'
        elif in_sweep:
            cls = 'possible_first_win'
        else:
            raise AssertionError('candidate is not covered by the published pools')
        if old_cat is not None:
            assert old_cat == ('1' if cls == 'conditional_first_loss' else '2' if cls == 'possible_first_win' else None)
        counts[origin,cls] += 1
        if cls == 'conditional_first_loss':
            parents[origin].add(parent)
            parents['all'].add(parent)
        classified.append((f'{child:032x}',f'{parent:032x}',origin,cls))
    result = {'sweep_s6':len(sweep),'loss_s6':len(loss6),'loss7_children_of_loss6':len(loss7_from_loss6),
              'focus_loss7':len(certified_loss7),'focus_win7':len(certified_win7),
              'counts':{origin:{cls:counts[origin,cls] for cls in ('conditional_first_loss','possible_first_win','certified_first_win')} for origin in ('published','additional')},
              'parents_with_conditional_first_loss':{origin:len(v) for origin,v in parents.items()},
              'scope':'K0675-conditioned LOSS6 results and focus certificate records; possible_first_win is not a verdict'}
    if args.csv:
        with args.csv.open('w',newline='') as f:
            writer = csv.writer(f,lineterminator='\n')
            writer.writerow(('s7_hex','s6_hex','origin','classification'))
            writer.writerows(sorted(classified))
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
