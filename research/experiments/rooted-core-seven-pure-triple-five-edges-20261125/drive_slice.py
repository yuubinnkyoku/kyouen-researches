import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from solve_core import build_perm_tables, initial_types, solve, emit_records
import json

n, E, family, budget = 6, 6, 'six-vertex smoke', int(sys.argv[1]) if len(sys.argv) > 1 else 220
mode = sys.argv[2] if len(sys.argv) > 2 else 'smoke6'
if mode == 'smoke6':
    n, E, family = 6, 6, 'six-vertex <=6-edge smoke replay'
else:
    n, E, family = 7, 5, 'seven-vertex <=5-edge (official)'
triples, idx, vmask, tabs = build_perm_tables(n)
t0 = time.time()
initial, raw = initial_types(n, E, triples, vmask, tabs)
from engine import canonical
initial = sorted(set(initial))
for st in initial:
    assert st == canonical(n, tuple(st[1])), st
out = Path(__file__).parent / 'output'
result = solve(initial, 2200, checkpoint=True,
               progress=lambda tag, a, b: print(tag, a, b, flush=True),
               meta=mode, budget_seconds=budget)
assert result['certified'], 'not certified within maxlen'
head = emit_records(result, out / ('%s_records.json' % mode), family, raw, n, E)
print(json.dumps(head, indent=2), flush=True)
print('attempt elapsed', round(time.time()-t0,1), flush=True)
