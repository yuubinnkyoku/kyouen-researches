#!/usr/bin/env python3
"""Compare complete, independently generated terminal-four surveys."""
from pathlib import Path
import json

root = Path(__file__).resolve().parent
fast = [json.loads(line) for line in (root/'pair-ranking.jsonl').read_text().splitlines()]
independent = [json.loads(line) for line in (root/'pair-ranking-independent.jsonl').read_text().splitlines()]
assert len(fast) == 1516 and len({tuple(row['pair']) for row in fast}) == 1516
assert fast == independent
for row in fast:
    assert row['uncovered'] == len(row['thirds'])
    assert row['residual_triple_orbits'] == len(row['representatives'])
result = {
    'verified': True,
    'pair_orbits': len(fast),
    'all_records_match_independent_bareiss': True,
    'independent_work': json.loads((root/'pair-ranking-independent-counts.json').read_text()),
    'minimum_residual_triple_orbits': min(row['residual_triple_orbits'] for row in fast),
    'minimizers': [row['pair'] for row in fast if row['residual_triple_orbits'] == 5],
    'minimum_uncovered_thirds': min(row['uncovered'] for row in fast),
    'fully_terminal_four_covered_pairs': sum(row['uncovered'] == 0 for row in fast),
}
(root/'pair-ranking-verified.json').write_text(json.dumps(result, indent=2)+'\n')
