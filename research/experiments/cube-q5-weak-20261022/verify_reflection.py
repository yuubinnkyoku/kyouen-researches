#!/usr/bin/env python3
"""Independent determinant/permutation audit; no cofactor completion table."""
from itertools import combinations, permutations, product
from pathlib import Path
import json
import sys

from reflection import reply


def main():
    source = Path(sys.argv[1])
    recorded = json.loads(source.read_text())
    shape = tuple(recorded["shape"])
    points = list(product(*(range(n) for n in shape)))
    lookup = {p: i for i, p in enumerate(points)}
    mirror = [lookup[reply(shape, p)] for p in points]
    reps = [i for i, j in enumerate(mirror) if i < j]
    lifts = [(sum(t*t for t in p), *p) for p in points]
    terms = [(p, (-1)**sum(p[i] > p[j] for i in range(4) for j in range(i+1, 4)))
             for p in permutations(range(4))]

    def forbidden(ids):
        base = lifts[ids[0]]
        rows = [tuple(a-b for a, b in zip(lifts[i], base)) for i in ids[1:]]
        return sum(sign*rows[0][p[0]]*rows[1][p[1]]*rows[2][p[2]]*rows[3][p[3]]
                   for p, sign in terms) == 0

    def legal(state):
        return [p for p in range(len(points)) if p not in state and
                not any(forbidden((*four, p)) for four in combinations(state, 4))]

    counts = {"symmetric_safe_states": 0, "legal_reply_checks": 0,
              "symmetric_terminal_states": 0, "states_by_stones": {},
              "terminal_by_stones": {}, "all_replies_legal": True}

    def visit(state, start):
        assert all(not forbidden(five) for five in combinations(state, 5))
        assert {mirror[i] for i in state} == set(state)
        moves = legal(state)
        counts["symmetric_safe_states"] += 1
        k = str(len(state))
        counts["states_by_stones"][k] = counts["states_by_stones"].get(k, 0)+1
        if not moves:
            counts["symmetric_terminal_states"] += 1
            counts["terminal_by_stones"][k] = counts["terminal_by_stones"].get(k, 0)+1
        for p in moves:
            assert mirror[p] not in state and mirror[p] != p
            assert mirror[p] in legal((*state, p)), (state, p)
            counts["legal_reply_checks"] += 1
        for j in range(start, len(reps)):
            p = reps[j]
            if p in moves:
                visit(tuple(sorted((*state, p, mirror[p]))), j+1)

    visit((), 0)
    for key, value in counts.items():
        assert recorded[key] == value, (key, recorded[key], value)
    print(json.dumps({"shape": shape, "independent_determinant_check": True,
                      "compared_fields": counts}, indent=2))


if __name__ == "__main__":
    main()
