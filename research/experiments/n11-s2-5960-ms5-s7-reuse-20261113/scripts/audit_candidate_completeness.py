#!/usr/bin/env python3
"""Enumerate legal oracle-completing children of the published S6 worklist.

The oracle's D4 images are all considered. This checks candidate coverage,
not the game verdicts or the completeness of the S6 worklist itself.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

from audit_published_candidates import images, safe

HERE = Path(__file__).resolve().parents[1]
EXPERIMENTS = HERE.parent
ORACLE = EXPERIMENTS/'n11-central-19-cover-20261031/output/s6sweep/s5_verdicts.json'
MANIFEST = EXPERIMENTS/'n11-s2-5960-milestone5-20261112/output'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--missing-csv',type=Path)
    args = parser.parse_args()
    oracle = json.loads(ORACLE.read_text())
    base = [int(x,16) for x in oracle['first_win_s5']+oracle['second_win_s5']]
    assert len(base) == len(set(base)) == 94
    assert all(x.bit_count() == 5 and x == min(images(x)) for x in base)
    orbit = {y for x in base for y in images(x)}
    assert len(orbit) == 744
    parents = []
    for path in sorted(MANIFEST.glob('ms5_s6_manifest_part*.csv')):
        with path.open(newline='') as source:
            parents.extend(int(row['hex'],16) for row in csv.DictReader(source))
    assert len(parents) == len(set(parents)) == 7867
    published = set()
    for path in sorted((HERE/'output').glob('ms5_s7_reuse_candidates_part*.csv')):
        with path.open(newline='') as source:
            published.update(int(row[0],16) for row in csv.reader(source) if row[0] != 's7_hex')
    assert len(published) == 8763
    candidate_pairs = set()
    subset_count = 0
    for parent in parents:
        missing_bits = set()
        for position in orbit:
            diff = position & ~parent
            if diff == 0:
                subset_count += 1
            elif diff.bit_count() == 1:
                missing_bits.add(diff)
        for move_bit in missing_bits:
            expanded = parent | move_bit
            if safe(expanded):
                child = min(images(expanded))
                candidate_pairs.add((child,parent,move_bit.bit_length()-1))
    assert subset_count == 0
    by_child = {child for child,_,_ in candidate_pairs}
    assert len(candidate_pairs) == len(by_child)
    missing = sorted(candidate_pairs, key=lambda x:x[0])
    missing = [row for row in missing if row[0] not in published]
    assert published <= by_child
    has_candidate = {parent for _,parent,_ in candidate_pairs}
    added_parent = {parent for _,parent,_ in missing}
    result = {'input_sha256':hashlib.sha256(ORACLE.read_bytes()).hexdigest(),
              'oracle_bases':len(base),'oracle_images':len(orbit),
              's6_worklist_parents':len(parents),'parents_already_containing_oracle':subset_count,
              'published_children':len(published),'all_children':len(by_child),
              'missing_children':len(missing),'parents_with_candidate':len(has_candidate),
              'parents_without_candidate':len(parents)-len(has_candidate),
              'parents_with_missing_candidate':len(added_parent),
              'sample_missing':{'s7_hex':f'{missing[0][0]:032x}',
                                's6_hex':f'{missing[0][1]:032x}','move_in_s6_coordinates':missing[0][2]},
              'scope':'given 94 oracle bases and published S6 worklist; no game verdicts or class labels'}
    if args.missing_csv:
        with args.missing_csv.open('w',newline='') as out:
            writer=csv.writer(out,lineterminator='\n')
            writer.writerow(('s7_hex','s6_hex','move_in_s6_coordinates'))
            writer.writerows((f'{child:032x}',f'{parent:032x}',move) for child,parent,move in missing)
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
