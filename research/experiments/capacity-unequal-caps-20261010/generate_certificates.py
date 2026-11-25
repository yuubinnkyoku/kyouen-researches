#!/usr/bin/env python3
"""Construct complete finite Grundy certificates for two unequal-capacity counterexamples."""
import json
from functools import lru_cache
from pathlib import Path

CASES = [
    ("even-slack-grundy2", (1, 2, 2, 3), 2, 4, (1, 0, 0, 1)),
    ("even-slack-grundy3", (1, 1, 2, 2, 3), 2, 4, (0, 1, 0, 0, 1)),
]


def children(x, caps, h, r):
    out = []
    for i in range(len(caps)):
        if x[i] >= caps[i]:
            continue
        y = list(x)
        y[i] += 1
        if sum(sorted(y, reverse=True)[:h]) <= r:
            out.append(tuple(y))
    return sorted(out)


def build(name, caps, h, r, root):
    @lru_cache(None)
    def solve(x):
        s = {solve(y) for y in children(x, caps, h, r)}
        g = 0
        while g in s:
            g += 1
        return g

    solve(root)
    states = sorted(reachable(root, caps, h, r), key=lambda x: (-sum(x), x))
    return dict(name=name, caps=caps, h=h, r=r, root=root,
                slack=r-sum(sorted(root, reverse=True)[:h]),
                root_grundy=solve(root),
                states=[dict(x=x, grundy=solve(x), children=children(x, caps, h, r))
                        for x in states])


def reachable(root, caps, h, r):
    seen = {root}
    todo = [root]
    while todo:
        x = todo.pop()
        for y in children(x, caps, h, r):
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return seen


def main():
    path = Path(__file__).with_name("certificates.json")
    data = [build(*case) for case in CASES]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    for case in data:
        print(case["name"], "states", len(case["states"]), "root", case["root"],
              "slack", case["slack"], "grundy", case["root_grundy"])
    print("WROTE", path)


if __name__ == "__main__":
    main()
