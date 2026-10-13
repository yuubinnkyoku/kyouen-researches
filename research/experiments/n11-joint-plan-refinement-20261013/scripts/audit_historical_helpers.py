#!/usr/bin/env python3
"""Small counterexamples for two historical optimizer helper contracts.

This does not edit historical code or invalidate the independently certified
element-only bound.  It documents a dormant shrinking control-flow bug and
an auxiliary relaxation that is not valid for minimum-union selection.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / 'research/experiments/n11-joint-s5-proof-planning-20261012/scripts/optimize_s5_selection.py'
OLD = EXP / 'input/historical-optimizer-before-lp-audit.py'
sys.path.insert(0, str(Path(__file__).resolve().parent))
spec = importlib.util.spec_from_file_location('historical_snapshot', OLD)
historical = importlib.util.module_from_spec(spec)
spec.loader.exec_module(historical)
from refine_plan import forced_shrink


def main():
    inst = historical.Instance([[0, 1], [1, 2], [2, 0]],
                               [(0, 0, 0), (0, 0, 1), (0, 0, 2)],
                               [{0}, {1}, {2}])
    initial_assign, initial_union = [0, 1, 2], {0, 1, 2}
    inst.union = lambda assign: set().union(*(inst.cost[assign[i]] for i in inst.paid))
    old_assign, old_union = historical.shrink(inst, list(initial_assign), set(initial_union))
    history = []
    new_assign, new_union = forced_shrink(inst, list(initial_assign), set(initial_union), history)
    assert len(old_union) == 3 and len(new_union) == 2
    assert all(inst.cost[new_assign[i]] <= new_union for i in inst.paid)

    lp_inst = historical.Instance([[0, 1]], [(0, 0, 0)], [{0}, {1}])
    auxiliary = historical._lp_relaxation_dual(lp_inst)
    feasible = set(lp_inst.cost[0])
    assert auxiliary == 2 and len(feasible) == 1
    out = {
        'schema': 'historical-minimum-union-helper-counterexamples-v1',
        'source_path': str(OLD.relative_to(ROOT)),
        'historical_source_path': str(ORIGINAL.relative_to(ROOT)),
        'source_sha256': hashlib.sha256(OLD.read_bytes()).hexdigest(),
        'shrink': {'groups': [[0, 1], [1, 2], [2, 0]], 'cost': [[0], [1], [2]],
                   'initial_assign': initial_assign, 'initial_union': sorted(initial_union),
                   'historical_output_union': sorted(old_union),
                   'corrected_output_union': sorted(new_union),
                   'corrected_assign': new_assign, 'corrected_history': history,
                   'diagnosis': 'feasible remains false after successful repair, so repaired candidates are discarded'},
        'auxiliary_lp': {'groups': [[0, 1]], 'cost': [[0], [1]],
                         'feasible_assign': [0], 'feasible_union': sorted(feasible),
                         'historical_auxiliary_bound': auxiliary, 'exact_optimum': 1,
                         'diagnosis': 'an integral union must contain one chosen option per group; it need not intersect every unchosen option'},
        'scope': 'The existing 6577 element-only dual certificate and all feasible-plan upper bounds are unaffected. The auxiliary 728 value should not be presented as a generic valid minimum-union lower bound.'}
    path = EXP / 'output/historical-helper-audit.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'shrink_before': len(old_union), 'shrink_after': len(new_union),
                      'auxiliary_lp_counterexample': auxiliary, 'true_optimum': 1}))


if __name__ == '__main__':
    main()
