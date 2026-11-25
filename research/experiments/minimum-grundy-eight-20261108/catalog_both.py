#!/usr/bin/env python3
"""Complete normal and terminal-one auxiliary Pareto fronts for values 2..9."""
import hashlib
import json
from pathlib import Path
from verify import ROOT, NORMAL, MISERE


def main():
    directory = Path(__file__).resolve().parent
    base = ROOT / 'research/experiments'
    old = json.loads((base / 'pure-triple-few-edge-grundy-20261107/output/audit.json').read_text())['records']
    six = json.loads((base / 'pure-triple-six-edge-complete-20261108/output/audit.json').read_text())['records']
    source7 = base / 'pure-triple-seven-edge-complete-20261108/output/audit.json'
    seven = json.loads(source7.read_text())['records']
    aux6 = json.loads((base / 'pure-triple-six-edge-complete-20261108/output/misere_values.json').read_text())
    aux7 = json.loads((base / 'pure-triple-seven-edge-complete-20261108/output/misere.json').read_text())
    rows6 = [dict(h=r['h'], n=r['n'], edges=r['edges'], grundy=r['grundy']) for r in old]
    rows6 += [dict(h=6, n=r['n'], edges=r['edges'], grundy=r['grundy']) for r in six]
    assert aux6['canonical_rows_sha256'] == hashlib.sha256(json.dumps(rows6, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert aux7['census_sha256'] == hashlib.sha256(source7.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    assert len(rows6) == aux6['kernel_types'] and len(seven) == aux7['kernel_types']
    rows = rows6 + seven
    auxiliary = [aux6['misere_values_free_zero'] + aux7['misere_values_free_zero'],
                 aux6['misere_values_free_one'] + aux7['misere_values_free_one']]
    assert all(len(values) == len(rows) for values in auxiliary)
    minima = {2: 6, 3: 7, 4: 6, 5: 7, 6: 8, 7: 9, 8: 10, 9: 11}
    candidates = {kind: {value: {} for value in minima} for kind in ('normal', 'misere_aux')}

    def insert(kind, value, n, edges, free):
        if value not in candidates[kind]:
            return
        count = len(edges)
        current = candidates[kind][value].get(count)
        if current is None or n < current['n']:
            candidates[kind][value][count] = dict(n=n, edges=edges, value=value, free_parity=free)

    for i, row in enumerate(rows):
        for free in (0, 1):
            insert('normal', row['grundy'] ^ free, row['n'] + free, row['edges'], free)
            insert('misere_aux', auxiliary[free][i], row['n'] + free, row['edges'], free)
    for row in json.loads((directory / 'output/audit_pruned.json').read_text())['records']:
        for kind in candidates:
            insert(kind, row[kind], row['n'], row['edges'], row['n'] - 10)
    fronts = {}
    for kind, values in candidates.items():
        fronts[kind] = {}
        for value, by_edges in values.items():
            points = [(row['n'], count, row) for count, row in by_edges.items()]
            assert min(n for n, _, _ in points) == minima[value]
            front = [dict(legal_points=n, edge_count=count, witness=row) for n, count, row in sorted(points)
                     if not any(p <= n and e <= count and (p, e) != (n, count) for p, e, _ in points)]
            assert any(r['legal_points'] == minima[value] and r['edge_count'] <= 8 for r in front)
            # Re-evaluate every displayed witness from its labeled residual game.
            evaluator = NORMAL.grundy if kind == 'normal' else MISERE.residual_misere
            for item in front:
                witness = item['witness']
                assert evaluator(witness['n'], tuple(witness['edges'])) == value
            fronts[kind][value] = front
    output = dict(audit='PASS', complete_kernel_types_through_seven_edges=len(rows),
                  free_parity_classes=2 * len(rows), fronts=fronts, global_point_lower_bounds=minima,
                  completeness='Every family with at least eight edges is dominated by a point-minimal witness with at most eight edges.',
                  auxiliary_definition='terminal=1; mex of child auxiliaries otherwise; not a disjunctive-sum SG invariant',
                  limitation='Legal points and pure triple edges only; no minimum total geometric board size or anchor count.')
    (directory / 'output/pareto_both.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({kind: {value: [(r['legal_points'], r['edge_count']) for r in front]
                            for value, front in values.items()} for kind, values in fronts.items()}, indent=2))


if __name__ == '__main__':
    main()
