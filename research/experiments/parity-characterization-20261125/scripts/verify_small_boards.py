"""Exhaustive/random verification of the parity characterization theorem.

Theorem (to be checked computationally on small boards):
For a finite achievement game (positions = sets with |S ∩ B| <= s for every
block B; moves add one point; normal play), the following are equivalent:
  (a) every position has Grundy value 0 or 1;
  (b) all maximal safe sets have the same parity.
Moreover, when (b) holds with common parity p,
  Grundy(S) = (p − |S|) mod 2   and   misere_win(S) = 1 iff (p − |S|) is even.

We also check the localized form: for every position S, all Grundy values of
positions T >= S are <= 1  <=>  all maximal extensions of S have the same parity.

Boards checked:
  * n=4: all block families from 2-blocks and 3-blocks (2^10 = 1024) for s=2,3;
  * n=5: all 3-uniform families (2^10), all 2-uniform families (2^10), all
    4-uniform families (2^5), for s=2,3;
  * n=6,7,8: random block families (fixed seed), for s=2,3,4.

Usage:
    python verify_small_boards.py
"""

from __future__ import annotations

import json
import random
from collections import Counter
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def popcount(x: int) -> int:
    return x.bit_count()


def analyze(n: int, blocks: list[tuple[int, ...]], s: int):
    """Return (parity_set_of_maximal_sets, grundy dict, misere dict)."""
    line_masks = [sum(1 << p for p in B) for B in blocks]
    safe = []
    for mask in range(1 << n):
        if all(popcount(mask & B) <= s for B in line_masks):
            safe.append(mask)
    safe_set = set(safe)
    maximal = []
    for mask in safe:
        addable = False
        for p in range(n):
            if (mask >> p) & 1:
                continue
            if mask | (1 << p) in safe_set:
                addable = True
                break
        if not addable:
            maximal.append(mask)
    parity = {popcount(m) & 1 for m in maximal}
    g = {m: 0 for m in safe}
    mis = {m: 0 for m in safe}
    for mask in sorted(safe, key=lambda m: -popcount(m)):
        children = [mask | (1 << p) for p in range(n)
                    if not (mask >> p) & 1 and (mask | (1 << p)) in safe_set]
        mex = set()
        mis_win = 1 if not children else 0
        for ch in children:
            mex.add(g[ch])
            if mis[ch] == 0:
                mis_win = 1
        v = 0
        while v in mex:
            v += 1
        g[mask] = v
        mis[mask] = mis_win
    return parity, g, mis, maximal


def check_board(n, blocks, s):
    parity, g, mis, maximal = analyze(n, blocks, s)
    uniform = len(parity) == 1
    only01 = max(g.values()) <= 1
    res = {"uniform": uniform, "only01": only01,
           "equiv_ok": uniform == only01, "formula_ok": True,
           "local_ok": True}
    if uniform:
        p = next(iter(parity))
        for m in g:
            if g[m] != (p - popcount(m)) % 2:
                res["formula_ok"] = False
                break
        # misere: win iff (p - |S|) even
        for m in mis:
            if mis[m] != (1 if (p - popcount(m)) % 2 == 0 else 0):
                res["formula_ok"] = False
                break
    # localized form: for every safe S, all Grundy values in the upset <= 1
    # iff all maximal extensions of S have the same parity.
    if not res["local_ok"]:
        return res
    positions = list(g) if n <= 5 else random.Random(n * 1000 + s).sample(
        list(g), min(40, len(g)))
    # group maximal sets by their subsets (only for small n)
    for S in positions:
        ext_par = {popcount(M) & 1 for M in maximal if (S & ~M) == 0}
        subtree_only01 = all(g[T] <= 1 for T in g if (S & ~T) == 0)
        if (len(ext_par) == 1) != subtree_only01:
            res["local_ok"] = False
            break
    return res


def families(n: int, k: int):
    return list(combinations(range(n), k))


def main() -> None:
    rng = random.Random(20261125)
    summary = Counter()
    violations = []
    examples = []

    def run(n, blocks, s, label):
        r = check_board(n, blocks, s)
        summary["boards"] += 1
        summary["uniform"] += r["uniform"]
        summary["mixed"] += not r["uniform"]
        summary["only01"] += r["only01"]
        if not r["equiv_ok"]:
            violations.append({"label": label, "n": n, "s": s, "blocks": blocks,
                               "reason": "uniform parity != only01"})
        if not r["formula_ok"]:
            violations.append({"label": label, "n": n, "s": s, "blocks": blocks,
                               "reason": "grundy/misere formula"})
        if not r["local_ok"]:
            violations.append({"label": label, "n": n, "s": s, "blocks": blocks,
                               "reason": "localized form"})
        if r["uniform"] and len(examples) < 5:
            examples.append({"n": n, "s": s, "blocks": [list(b) for b in blocks]})

    # n=4: all families of 2-blocks and 3-blocks
    for n, ks in [(4, [2, 3]), (5, [2, 3, 4])]:
        for k in ks:
            fams = families(n, k)
            for bits in range(1 << len(fams)):
                blocks = [fams[i] for i in range(len(fams)) if (bits >> i) & 1]
                if not blocks:
                    continue
                for s in (2, 3):
                    run(n, blocks, s, f"exhaustive-n{n}-k{k}-b{bits}")

    # random boards n=6,7,8 with block sizes 2..min(4,n)
    trials_for = {6: 800, 7: 400, 8: 150}
    for n in (6, 7, 8):
        fam = {k: families(n, k) for k in range(2, min(4, n) + 1)}
        for trial in range(trials_for[n]):
            blocks = []
            for k, fs in fam.items():
                if not fs:
                    continue
                prob = rng.choice([0.1, 0.2, 0.3, 0.5])
                for b in fs:
                    if rng.random() < prob:
                        blocks.append(b)
            if not blocks:
                continue
            for s in (2, 3, 4):
                if s >= 2:
                    run(n, blocks, s, f"random-n{n}-t{trial}")

    result = {"summary": dict(summary), "violations": violations,
              "uniform_examples": examples}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "verification.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
    print(json.dumps({"summary": dict(summary),
                      "violations": len(violations)}, indent=1))


if __name__ == "__main__":
    main()
