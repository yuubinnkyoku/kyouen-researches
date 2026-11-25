#!/usr/bin/env python3
"""Generate complete reachable-position mex certificates; exact integer arithmetic."""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
WITNESSES = [
    {"name": "four", "capacities": [4, 4, 5, 5], "h": 3, "r": 12, "root": [2, 1, 1, 0]},
    {"name": "five", "capacities": [1, 4, 4, 5, 5], "h": 3, "r": 12, "root": [0, 2, 1, 1, 0]},
]


def build(witness):
    c = tuple(witness["capacities"])
    h, r = witness["h"], witness["r"]
    root = tuple(witness["root"])
    rows = {}

    @lru_cache(None)
    def solve(x):
        child_values = []
        for i in range(len(c)):
            if x[i] >= c[i]:
                continue
            y = x[:i] + (x[i] + 1,) + x[i + 1:]
            if sum(sorted(y, reverse=True)[:h]) <= r:
                child_values.append(solve(y))
        value = 0
        while value in child_values:
            value += 1
        rows[','.join(map(str, x))] = value
        return value

    value = solve(root)
    return {**witness, "grundy": value, "states": dict(sorted(rows.items()))}


def main():
    output = {"rule": "increase one labeled column by one if within c and top-h sum <= r", "witnesses": [build(x) for x in WITNESSES]}
    p = HERE / "certificates.json"
    p.write_text(json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n', encoding='utf-8')
    print('generated', [(x['name'], x['grundy'], len(x['states'])) for x in output['witnesses']])


if __name__ == '__main__':
    main()
