"""Record the seven-viewpoint selection of Task B probe targets.

The untouched pool after night batch 2 holds five members
(131631, 162106, 193768, 196002, 211133). This script writes the evidence used
to pick three of them for the batch3 2M probe: ranking.tsv impact columns, the
current plan (n11-night-plan-update3) verdict census, evidence sharing with the
already-certified set, and the free-branch information content. Read-only over
every prior artifact; output goes to this experiment only.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/experiments/n11-s5-s6-quotient-20261013/output/pilots.json'
RANKING = ROOT / 'research/experiments/n11-conflict-ranking-20261013/output/ranking.tsv'
PLAN = ROOT / 'research/experiments/n11-night-plan-update3-20261014/output/effect-measurement3.json'

POOL = [131631, 162106, 193768, 196002, 211133]
SELECTED = [131631, 162106, 211133]
CERTIFIED = [126017, 144095, 209644, 197665,  # WIN
             137694, 143240, 220231, 126899, 121263, 145001, 558600]  # LOSS


def main():
    data = json.loads(SOURCE.read_text())
    rows = {r['s5_index']: r for r in data['rows']}
    ranking = {}
    with RANKING.open() as stream:
        header = stream.readline().rstrip('\n').split('\t')
        for line in stream:
            row = dict(zip(header, line.rstrip('\n').split('\t')))
            ranking[int(row['s5_index'])] = row
    plan = json.loads(PLAN.read_text())

    def children(index):
        return {tuple(c['mask']) for c in rows[index]['children']}

    viewpoints = {}
    for index in POOL:
        row = rows[index]
        own = children(index)
        viewpoints[index] = dict(
            geometry_rank=int(ranking[index]['geometry_rank']),
            impact_per_child_rank=int(ranking[index]['impact_per_child_rank']),
            canonical_s6_children=row['canonical_children'],
            legal_moves=row['legal'],
            stabilizer=row['stabilizer'],
            if_win_loss_choices_invalidated=int(ranking[index]['if_win_loss_choices_invalidated']),
            if_loss_fixed_win_branches_uncovered=int(ranking[index]['if_loss_fixed_win_branches_uncovered']),
            if_win_new_free_win_branches=int(ranking[index]['if_win_new_free_win_branches']),
            if_win_greedy_delta=int(ranking[index]['if_win_greedy_delta']),
            shared_children_with_certified={str(k): len(own & children(k)) for k in CERTIFIED
                                           if own & children(k)},
            selected=index in SELECTED,
        )
    out = dict(
        schema='n11-night-batch3-task-b-selection-v1',
        pool=POOL, selected=SELECTED,
        excluded={i: 'free=3 low information content; at most one free=3 representative allowed'
                  for i in POOL if i not in SELECTED},
        source=str(SOURCE.relative_to(ROOT)),
        ranking=str(RANKING.relative_to(ROOT)),
        plan=str(PLAN.relative_to(ROOT)),
        plan_verdict_census=plan['verdict_census'],
        viewpoints=viewpoints,
    )
    path = EXP / 'output/selection-task-b.json'
    path.parent.mkdir(exist_ok=True)
    assert not path.exists(), 'refusing to overwrite existing selection record'
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps(viewpoints, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
