"""Corrupt real schemas, check actual point definitions, and test the subset lemma."""
import argparse
import gzip
from itertools import product
from pathlib import Path
from schema import audit, prefix
from audit import HERE, PRIOR, CASES, save, sha


def encode(nv, clauses):
    return (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    seed_path = HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt'
    seed = list(map(int, seed_path.read_bytes().split()))[2:]
    rows = []
    for case, folder in CASES.items():
        raw = gzip.decompress((PRIOR/folder/'input.cnf.gz').read_bytes())
        nv, clauses = prefix.parse(raw)
        _, report = audit(raw, seed, case)
        base = report['point_base']
        selected = [1, 2, 3, 4, base+1, base+2538]
        local = [c for c in clauses if all(abs(v) in selected for v in c)]
        assert len(local) == (13 if case == 'changed-pair' else 14)
        for bits in product((False, True), repeat=6):
            values = dict(zip(selected, bits))
            b, n, low, high, a, z = bits
            expected = sum(bits[:4]) == 1 and a == (b or low) and z == (b or high)
            if case == 'no-pair':
                expected = expected and not b
            actual = all(any((v > 0) == values[abs(v)] for v in c) for c in local)
            assert actual == expected
        clone = lambda: [c[:] for c in clauses]
        mutations = {}
        bad = clone(); bad[0][-1] = bad[0][-2]; mutations['broken-onehot'] = bad
        bad = clone(); bad[8883] = bad[8883][:-1] if case == 'changed-pair' else [-bad[8883][0]]
        mutations['wrong-BOTH-cardinality'] = bad
        none_start = 8883+(3804 if case == 'changed-pair' else 1269)
        bad = clone(); bad[none_start][0] = -bad[none_start][0]; mutations['wrong-NONE-complement-polarity'] = bad
        point_start = next(i for i, c in enumerate(clauses) if c == [-base-1, 3, 1])
        bad = clone(); bad[point_start][1] = 7; mutations['wrong-point-definition'] = bad
        bad = clone(); bad[point_start][0] = -3; mutations['point-selector-alias'] = bad
        deletion_start = len(clauses)-report['deletion_clauses']
        bad = clone(); bad[deletion_start][0] = -bad[deletion_start][0]; mutations['wrong-loss-polarity'] = bad
        geometry_start = point_start+report['point_definition_clauses']
        bad = clone(); bad[geometry_start][0] = -bad[geometry_start][0]; mutations['positive-geometric-clause'] = bad
        rejected = []
        for name, altered in mutations.items():
            try:
                audit(encode(nv, altered), seed, case)
            except (AssertionError, KeyError, StopIteration):
                rejected.append(name)
            else:
                raise AssertionError((case, name))
        rows.append(dict(case=case, rejected=rejected, point_truth_assignments=64))
    # A finite analogue of the larger-to-exact-target argument, independent
    # of either CNF builder. The all-size proof is stated in README.
    p, original, target = 11, {0, 1, 2, 10}, 5
    checked = 0
    for mask in range(1 << p):
        chosen = {t for t in range(p) if mask & (1 << t)}
        pairs = [i for i in range(1, 6) if i in chosen and p-i in chosen]
        if 0 not in chosen or len(chosen) < target or len(pairs) > 1 or len(original-chosen) > 2 or pairs == [1]:
            continue
        required = original & chosen
        if pairs:
            d = pairs[0]; required |= {d, p-d}
        assert len(required) <= target
        subset = required | set(sorted(chosen-required)[:target-len(required)])
        assert len(subset) == target and 0 in subset and subset <= chosen
        assert original-subset == original-chosen
        assert [i for i in range(1, 6) if i in subset and p-i in subset] == pairs
        checked += 1
    assert checked > 0
    save(args.output, dict(cases=rows, point_truth_assignments=128, subset_lemma_cases=checked,
         schema_source_sha256=sha((HERE/'schema.py').read_bytes()),
         prefix_source_sha256=sha((HERE.parent/'parabola-p2539-exchange-audit-20261110/schema.py').read_bytes()),
         regression_source_sha256=sha(Path(__file__).read_bytes()),
         scope='Fourteen actual-schema corruptions rejected, exact point-definition truth tables, finite subset-lemma analogue. Not a general checker soundness proof.'))
    print('PASS 14 schema corruptions, 128 point truth assignments,', checked, 'subset cases', flush=True)


if __name__ == '__main__':
    main()
