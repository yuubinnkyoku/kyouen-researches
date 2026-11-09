#!/usr/bin/env python3
"""Compare independent coplanarity/game implementations on every 4-cube state."""
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import runpy

HERE = Path(__file__).resolve().parent
with redirect_stdout(StringIO()):
    original = runpy.run_path(str(HERE / 'verify.py'))
    midpoint = runpy.run_path(str(HERE / 'independent_midpoint_audit.py'))

# product(range(2), repeat=4) orders coordinates opposite to the bit order
# used by the midpoint implementation. Map vertices by their actual tuples.
points_a = original['points']
points_b = midpoint['P']
index_b = {point: i for i, point in enumerate(points_b)}
permutation = [index_b[point] for point in points_a]
assert len(set(permutation)) == 16


def map_mask(mask):
    return sum(1 << permutation[i] for i in range(16) if (mask >> i) & 1)


assert {map_mask(mask) for mask in original['forbidden']} == midpoint['forbidden']
levels = Counter()
for mask in range(1 << 16):
    mapped = map_mask(mask)
    assert original['safe'][mask] == midpoint['safe'][mapped], f'safety mismatch: {mask}'
    if not original['safe'][mask]:
        continue
    a = original['grundy'](mask)
    b = original['misere_win'](mask)
    assert a == midpoint['grundy'][mapped], f'Grundy mismatch: {mask}'
    assert b == midpoint['misere_win'][mapped], f'misère mismatch: {mask}'
    levels[(mask.bit_count(), a, b)] += 1
assert sum(levels.values()) == 8193
print(json.dumps({'states_checked': 65536, 'safe_states_checked': sum(levels.values()),
                  'forbidden_sets_equal': len(original['forbidden']),
                  'vertex_permutation': permutation,
                  'layer_grundy_misere': [
                      {'stones': k, 'grundy': g, 'misere_win': w, 'count': count}
                      for (k, g, w), count in sorted(levels.items())]}, indent=2))
