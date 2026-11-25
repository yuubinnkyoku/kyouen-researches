"""Bounded zero/one/two-deletion exchanges in the fixed-origin/complete-pair family."""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
SEED = HERE.parent/'parabola-warm-improvement-20261109/output/target1299-warm1298-budget500000/candidate.txt'
BASE = HERE.parent/'parabola-cnf-deletion-distance-20261109/output/rc2-p2647-d1323-20261108T184724Z.cnf'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--seed', type=Path, required=True)
    ap.add_argument('--seconds', type=float, default=60)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    raw = args.seed.read_bytes()
    values = list(map(int, raw.split()))
    p, n = values[:2]
    selected = frozenset(values[2:])
    fixed = frozenset((0, 1323, 1324))
    assert p == 2647 and n == len(selected) and n >= 3 and fixed <= selected
    base = BASE.read_bytes()
    assert sha(base) == '0f09fc6efce1ba1b3df795eef24e4bb014fcfad836f31d4e6ba7e99b242ff0b3'
    required_sets = []
    missing_index = defaultdict(list)
    for row in base.decode('ascii').splitlines():
        if not row or row[0] in 'cp':
            continue
        required = frozenset(v if v > 0 else p+v for v in map(int, row.split()[:-1]))
        missing = required-selected
        assert missing
        required_sets.append(required)
        if len(missing) <= 3:
            missing_index[missing].append(required & selected)
    empty_sides = [t for t in range(1, p) if t not in selected and p-t not in selected]
    free = selected-fixed
    removals = set()
    one_deletion_supports = 0
    for t in empty_sides:
        supports = missing_index[frozenset((t,))]
        if not supports:
            removals.add(frozenset())
            continue
        first = min(supports, key=len)
        for a in first & free:
            unhit = next((s for s in supports if a not in s), None)
            if unhit is None:
                one_deletion_supports += 1
                removals.add(frozenset((a,)))
                removals.update(frozenset((a, b)) for b in free if b != a)
            else:
                for b in unhit & free:
                    removed = frozenset((a, b))
                    if all(s & removed for s in supports):
                        removals.add(removed)
    records = dict(p=p, seed_size=n, fixed=sorted(fixed), seed_sha256=sha(raw), seed_path=args.seed.as_posix(), base_sha256=sha(base),
                   max_removed_points=2, target=n+1, proposed_removal_sets=len(removals),
                   empty_sides=len(empty_sides), single_removal_support_options=one_deletion_supports,
                   removal_sets_checked=0, addition_sets_checked=0,
                   source_sha256=sha(Path(__file__).read_bytes()),
                   scope='Projected-CNF neighborhood search only. Positive candidates need independent geometry; no global upper bound is inferred.')
    answer = None
    status = 'NO_PROJECTED_IMPROVEMENT_FOUND'
    for removed in sorted(removals, key=lambda r: (len(r), tuple(sorted(r)))):
        if time.monotonic()-start > args.seconds:
            status = 'UNKNOWN_TIME_LIMIT'
            break
        records['removal_sets_checked'] += 1
        candidates = set(empty_sides) | {p-r for r in removed}
        eligible = [t for t in sorted(candidates)
                    if all(s & removed for s in missing_index[frozenset((t,))])]
        for added_tuple in combinations(eligible, len(removed)+1):
            records['addition_sets_checked'] += 1
            if len({min(t, p-t) for t in added_tuple}) != len(added_tuple):
                continue
            added = frozenset(added_tuple)
            if any(any(not (support & removed) for support in missing_index[frozenset(group)])
                   for k in range(2, len(added)+1) for group in combinations(added_tuple, k)):
                continue
            answer = sorted((selected-removed) | added)
            assert len(answer) == n+1 and fixed <= set(answer)
            assert not any(req <= set(answer) for req in required_sets)
            assert all(not ({i, p-i} <= set(answer)) for i in range(1, (p-1)//2+1) if i != 1323)
            records.update(removed=sorted(removed), added=sorted(added), candidate_size=len(answer),
                           projected_clause_violations=0, geometry='UNCHECKED')
            status = 'PROJECTED_CANDIDATE'
            break
        if answer is not None:
            break
    records.update(status=status, elapsed_seconds=time.monotonic()-start)
    if answer is not None:
        (args.output/'candidate.txt').write_text(f'{p} {len(answer)}\n'+' '.join(map(str, answer))+'\n', encoding='ascii', newline='\n')
    (args.output/'result.json').write_text(json.dumps(records, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(records, indent=2), flush=True)


if __name__ == '__main__':
    main()
