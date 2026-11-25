#!/usr/bin/env python3
"""Independent (selected-class count, outside subset) mex formulation."""
from functools import lru_cache
import json
from pathlib import Path
from random import Random

from verify_modules import invariant_orbit_clutters

if not __debug__:
    raise SystemExit('Assertions must remain enabled.')


def count_game(k, outside, orbits, misere=False):
    def safe(s, mask):
        return not any(s >= t and mask & b == b for t, b in orbits)

    @lru_cache(None)
    def grundy(s, mask):
        values = set()
        if s < k and safe(s+1, mask):
            values.add(grundy(s+1, mask))
        for v in range(outside):
            bit = 1 << v
            if not mask & bit and safe(s, mask | bit):
                values.add(grundy(s, mask | bit))
        if misere and not values:
            return 1
        value = 0
        while value in values:
            value += 1
        return value

    assert safe(0, 0)
    value = grundy(0, 0)
    return value, grundy.cache_info().currsize


def check(k, outside, orbits):
    orbits = tuple(sorted(set((t, b) for t, b in orbits if t <= k)))
    pure = [t for t, b in orbits if b == 0]
    if pure:
        keep = min(k, min(pure)-1)
    else:
        depth = max((t for t, b in orbits), default=0)
        keep = k % 2 if depth == 0 else depth+(k-depth) % 2
    trimmed = tuple((t, b) for t, b in orbits if t <= keep)
    original, states = count_game(k, outside, orbits)
    reduced, reduced_states = count_game(keep, outside, trimmed)
    assert original == reduced, (k, outside, orbits, keep, original, reduced)
    original_misere, _ = count_game(k, outside, orbits, misere=True)
    reduced_misere, _ = count_game(keep, outside, trimmed, misere=True)
    assert original_misere == reduced_misere, (
        'misere', k, outside, orbits, keep, original_misere, reduced_misere)
    return dict(k=k, outside=outside, orbit_count=len(orbits), kept=keep,
                grundy=original, misere_auxiliary_mex=original_misere,
                original_count_states=states,
                reduced_count_states=reduced_states)


def main():
    exhaustive = []
    for outside in (2, 3):
        count = 0
        states = 0
        for edges in invariant_orbit_clutters(6, outside, 4):
            orbits = tuple({((edge & 63).bit_count(), edge >> 6) for edge in edges})
            row = check(6, outside, orbits)
            count += 1
            states += row['original_count_states']
        exhaustive.append(dict(k=6, outside=outside, rank=4,
                               all_invariant_clutters=count, count_states=states))
    rng = Random(20261005)
    random_rows = []
    for i in range(720):
        outside = rng.randrange(0, 7)
        k = rng.randrange(1, 49)
        max_depth = min(k, rng.randrange(0, 9))
        candidates = [(t, b) for t in range(max_depth+1)
                      for b in range(1 << outside) if t+b.bit_count() >= 2]
        if i % 2:
            candidates = [(t, b) for t, b in candidates if b]
        selected = rng.sample(candidates, min(len(candidates), rng.randrange(0, 26)))
        random_rows.append(check(k, outside, selected))
    sharpness = [dict(k=k, grundy=count_game(k, 3, ((3, 2), (2, 5), (0, 6)))[0])
                 for k in range(9)]
    assert [row['grundy'] for row in sharpness] == [0, 1, 2, 2, 3, 2, 3, 2, 3]
    result = dict(
        scope='Exchangeable-class normal/misere kernel; 11x11 outcome remains UNKNOWN.',
        independent_formulation='Count selected X points and explicit outside subset.',
        misere_scope='Auxiliary mex has terminal value one; its zero means P. No xor additivity claimed.',
        exhaustive_orbit_families=exhaustive,
        deterministic_random_orbit_cases=random_rows,
        rank_four_sharpness=sharpness,
        status='VERIFIED',
    )
    output = Path(__file__).resolve().parents[1] / 'output/independent-count-audit.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print('Independent count mex:', sum(row['all_invariant_clutters'] for row in exhaustive),
          'complete orbit clutters;', len(random_rows),
          'additional orbit families; normal and misere auxiliary mex; sharpness checked.')


if __name__ == '__main__':
    main()
