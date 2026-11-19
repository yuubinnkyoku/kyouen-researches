#!/usr/bin/env python3
# census_z16_y5: third, independent derivation for the z=16, y=5 boundary slice.
# Engine H3 is written from scratch against the game definition (K1050 semantics),
# enumerating moves by DISTINCT TOKEN VALUE on a canonical sorted multiset, with an
# explicit dict memo (no lru_cache, no tuple-index loops): a different code shape
# from both engines of verify_z16_y5.py. It knows nothing about the closed form.
import json, hashlib
from pathlib import Path

def H3(r, tokens, z):
    if r == 0: return 0
    key = (r, tokens, z)
    v = H3.memo.get(key)
    if v is not None: return v
    opts = set()
    prev = None
    for tok in tokens:               # tokens sorted ascending, distinct values
        if tok == prev: continue     # enumerate distinct values once
        prev = tok
        if tok > 1:
            child = list(tokens); child.remove(tok); child.append(tok - 1)
            opts.add(H3(r - 1, tuple(sorted(child)), z))
        else:                        # remove, z grows
            child = list(tokens); child.remove(tok)
            opts.add(H3(r - 1, tuple(sorted(child)), z + 1))
    if z > 0:
        opts.add(1 ^ H3(r - 1, tokens, z - 1))
    res = 0
    while res in opts: res += 1
    H3.memo[key] = res
    return res
H3.memo = {}

def main():
    lines = []
    checks = 0
    for x in range(5, 46):
        tvals, pvals = [], []
        for r in range(0, x + 46):
            v = H3(r, (min(x, 5), max(x, 5)), 16)
            checks += 1
            if v == 2: tvals.append(r)
            elif v == 1: pvals.append(r)
        lines.append("x=%d T=%s" % (x, tvals))
        lines.append("x=%d P=%s" % (x, pvals))
    digest = hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()
    out = "\n".join(lines) + "\n"
    out += "checks=%d\n" % checks
    out += "census_sha256=%s\n" % digest
    (Path(__file__).parent / 'output').mkdir(exist_ok=True)
    (Path(__file__).parent / 'output' / 'census.txt').write_text(out, encoding='utf-8')
    H3.memo.clear()
    print("checks=%d states_written ok" % checks)

main()
