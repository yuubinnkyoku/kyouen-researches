"""Materialize the batch3 input CSVs from the frozen pilots.json source.

Same one-row conflict replay format as night batches 1/2; every file is
asserted byte-equal against the unchanged n11-conflict-closure-20261013 input
of the same index so a drift in the frozen source cannot silently re-root a
probe.

A_INDICES: 206386 budget-extension run (25M, not a same-condition re-run of
           the frozen 10M probe of n11-night-batch2).
B_INDICES: first capture-enabled probe of three members of the untouched pool.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/experiments/n11-s5-s6-quotient-20261013/output/pilots.json'
PRIOR_INPUT = ROOT / 'research/experiments/n11-conflict-closure-20261013/input'

A_INDICES = [206386]
B_INDICES = [131631, 162106, 211133]


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
