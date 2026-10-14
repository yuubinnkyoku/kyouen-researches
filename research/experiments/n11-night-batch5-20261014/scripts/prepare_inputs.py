"""Materialize the batch5 input CSVs from the frozen pilots.json source.

Same one-row conflict replay format as night batches 1..4; every file is
asserted byte-equal against the unchanged n11-conflict-closure-20261013 input
of the same index so a drift in the frozen source cannot silently re-root a
probe.

A_INDICES: 162106 budget-extension run (25M; not a same-condition re-run of
           the frozen 10M probe of n11-night-batch4, which ended NODE_LIMIT
           with 58/99 root children WIN).
B_INDICES: 193768 / 196002 first 2M probe (free=3 pool members left untouched
           by night-batch3's selection).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/experiments/n11-s5-s6-quotient-20261013/output/pilots.json'
PRIOR_INPUT = ROOT / 'research/experiments/n11-conflict-closure-20261013/input'

A_INDICES = [162106]
B_INDICES = [193768, 196002]


def main():
    data = json.loads(SOURCE.read_text())
    rows = {r['s5_index']: r for r in data['rows']}
    (EXP / 'input').mkdir(exist_ok=True)
    for index in A_INDICES + B_INDICES:
        row = rows[index]
        assert 'polarity_conflicts' in row['labels'], index
        text = 'conflict,{index},5,{lo},{hi},{legal},5,0,0,0,0\n'.format(
            index=index, lo=row['mask'][0], hi=row['mask'][1], legal=row['legal'])
        path = EXP / f'input/s5-{index}.csv'
        if path.exists():
            assert path.read_text() == text, index
        else:
            path.write_text(text)
        prior = PRIOR_INPUT / f's5-{index}.csv'
        assert prior.read_text() == text, f'{index}: prior input drift'
        print(index, 'ok', row['mask'], row['legal'], row['canonical_children'])


if __name__ == '__main__':
    main()
