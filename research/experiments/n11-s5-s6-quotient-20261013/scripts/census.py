"""Exact legal-child quotient census, no verdict inference or solver search."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'research/experiments/n11-independent-exact-audit-20261010/scripts'))
from independent import Board


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', choices=['pilots', 'joint'], default='pilots')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    source = ROOT / 'research/experiments/n11-proof-cost-comparison-20261012/output/pilot-candidates.json'
    pilots = json.loads(source.read_text())
    assert 'polarity_conflicts' in pilots and 'dual_use' not in pilots
    labels = {}
    for label in ('cheapest10', 'polarity_conflicts'):
        for r in pilots[label]:
            labels.setdefault(r['s5_index'], []).append(label)
    sources = {str(source.relative_to(ROOT)): sha(source)}
    if args.scope == 'pilots':
        records = {r['s5_index']: r for label in ('cheapest10', 'polarity_conflicts') for r in pilots[label]}
    else:
        gp = ROOT / 'research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz'
        pp = gp.parent / 'chosen-plans.json'
        with gzip.open(gp, 'rt') as stream:
            graph = json.load(stream)
        indices = json.loads(pp.read_text())['plans']['_joint_19_roots']['required_new_s5']
        records = {e: {'s5_index': e, 'mask': graph['s5_masks'][e]} for e in indices}
        sources.update({str(p.relative_to(ROOT)): sha(p) for p in (gp, pp)})
    board = Board(11)
    union = Counter()
    rows = []
    for count, (index, rec) in enumerate(sorted(records.items()), 1):
        mask = rec['mask'][0] | rec['mask'][1] << 64
        pts = board.points(mask)
        assert len(pts) == 5 and board.canonical(mask) == mask
        moves = board.points(board.legal(mask))
        stabilizer = [t for t, mapping in enumerate(board.maps) if sum(mapping[p] for p in pts) == mask]
        fixed = [sum(board.maps[t][p] == 1 << p for p in moves) for t in stabilizer]
        orbit_count, remainder = divmod(sum(fixed), len(stabilizer))
        assert remainder == 0
        orbit_reps = {min(board.maps[t][p].bit_length()-1 for t in stabilizer) for p in moves}
        assert len(orbit_reps) == orbit_count
        child_to_moves = {}
        for p in moves:
            child = board.canonical(mask | 1 << p)
            child_to_moves.setdefault(child, []).append(p)
        children = set(child_to_moves)
        assert len(children) <= orbit_count
        union.update(children)
        row = dict(s5_index=index, mask=rec['mask'], points=list(pts), labels=labels.get(index, []),
                   legal=len(moves), stabilizer=stabilizer, fixed_moves=fixed,
                   stabilizer_orbits=orbit_count, canonical_children=len(children),
                   extra_merges=orbit_count-len(children))
        if args.scope == 'pilots' or row['extra_merges']:
            row['children'] = [{'mask': [c & ((1<<64)-1), c>>64], 'moves': ps}
                               for c, ps in sorted(child_to_moves.items())]
        rows.append(row)
        if count % 1000 == 0:
            print(f'{count}/{len(records)} parents; {len(union)} distinct children', file=sys.stderr, flush=True)
        # Keep canonical/geometry caches bounded across the million-child census.
        if count % 250 == 0:
            board.canonical.cache_clear()
            board.legal.cache_clear()
    result = dict(schema='n11-s5-s6-quotient-v1', scope=args.scope, source_sha256=sources,
                  parents=len(rows), legal_edges=sum(r['legal'] for r in rows),
                  stabilizer_orbits=sum(r['stabilizer_orbits'] for r in rows),
                  canonical_child_incidence=sum(r['canonical_children'] for r in rows),
                  distinct_children=len(union), shared_children=sum(n>1 for n in union.values()),
                  cross_parent_duplicate_incidence=sum(n-1 for n in union.values()),
                  parent_extra_merge_count=sum(r['extra_merges']>0 for r in rows),
                  extra_merges=sum(r['extra_merges'] for r in rows),
                  stabilizer_histogram=dict(sorted(Counter(len(r['stabilizer']) for r in rows).items())),
                  child_parent_multiplicity=dict(sorted(Counter(union.values()).items())),
                  ranking=[r['s5_index'] for r in sorted(rows,key=lambda r:(r['canonical_children'],r['legal'],r['s5_index']))],
                  rows=rows,
                  verdicts='UNKNOWN: geometric obligations only; no WIN/LOSS conclusions')
    output = args.output or EXP / 'output' / f'{args.scope}.json'
    if output.suffix == '.gz':
        with output.open('wb') as raw:
            with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as stream:
                stream.write((json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)+'\n').encode())
    else:
        output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','ranking')}, indent=2))

if __name__ == '__main__':
    main()
