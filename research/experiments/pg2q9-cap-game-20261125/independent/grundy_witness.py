"""Task 4 (consequence): direct computational witness of Grundy >= 2.

The census shows that the maximal caps of PG(2,9) have mixed parity (sizes 6, 7,
8, 10).  By K1298 (all Grundy values in {0,1} <=> all maximal safe sets have one
parity) some position must have Grundy value >= 2.

This script does not rely on that theorem.  It takes a small cap S whose maximal
extensions already have mixed parity, enumerates the *whole* residual game under
S (all caps containing S), computes every Grundy value exactly, and reports an
explicit position with Grundy >= 2.  The game tree below a position T only
contains supersets of T, so the residual-game Grundy value of T is its true
Grundy value in the full game.  A uniform-parity residue is used as a control
(the local form of K1298 predicts {0,1} only there).
"""

from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pgcore as pc

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
BOARD = HERE.parent / "output" / "board_pg2q9.txt"


def bits(x):
    while x:
        b = x & -x
        yield b.bit_length() - 1
        x ^= b


def main() -> None:
    n, lines = pc.load_board(BOARD)
    lmask, lid = [], [[-1] * n for _ in range(n)]
    for li, L in enumerate(lines):
        m = 0
        for p in L:
            m |= 1 << p
        lmask.append(m)
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                lid[L[i]][L[j]] = li
                lid[L[j]][L[i]] = li
    allmask = (1 << n) - 1

    def is_cap_mask(mask):
        return all(bin(m & mask).count("1") <= 2 for m in lmask)

    def residue_full(start):
        """{position: addable-point mask} for all caps containing `start`."""
        pos = {}
        b0 = 0
        P = list(bits(start))
        for x, y in combinations(P, 2):
            b0 |= lmask[lid[x][y]]
        stack = [(start, b0)]
        while stack:
            m, b = stack.pop()
            avail = (~b) & allmask
            pos[m] = avail
            for q in bits(avail):
                nb = b
                for x in bits(m):
                    nb |= lmask[lid[q][x]]
                stack.append((m | (1 << q), nb))
        return pos

    def grundy(pos):
        G = {}
        for m in sorted(pos, key=lambda z: bin(z).count("1"), reverse=True):
            ch = set()
            for q in bits(pos[m]):
                ch.add(G[m | (1 << q)])
            g = 0
            while g in ch:
                g += 1
            G[m] = g
        return G

    mixed = None
    control = None
    rejected = 0
    n_caps4 = 0
    for quad in combinations(range(n), 4):
        mask = (1 << quad[0]) | (1 << quad[1]) | (1 << quad[2]) | (1 << quad[3])
        if not is_cap_mask(mask):
            rejected += 1
            continue
        n_caps4 += 1
        pos = residue_full(mask)
        maximal_sizes = sorted({bin(m).count("1") for m, av in pos.items() if av == 0})
        par = {s % 2 for s in maximal_sizes}
        if len(par) > 1 and mixed is None:
            mixed = (mask, pos, maximal_sizes)
        if len(par) == 1 and len(maximal_sizes) > 1 and control is None:
            control = (mask, pos, maximal_sizes)
        if mixed is not None and (control is not None or n_caps4 >= 60):
            break
        if n_caps4 >= 60:
            break

    out = {}
    for name, data in (("mixed", mixed), ("uniform_control", control)):
        if data is None:
            out[name] = None
            continue
        mask, pos, maximal_sizes = data
        G = grundy(pos)
        dist = {}
        for v in G.values():
            dist[v] = dist.get(v, 0) + 1
        best = max(G.values())
        wit = sorted(m for m, v in G.items() if v == best)

        # cross-check the Grundy values against the K1298 formula on every
        # position whose reachable maximal extensions have a single parity:
        #     G(T) = (p - |T|) mod 2.
        maximals = [m for m, av in pos.items() if av == 0]
        uniform_checked = 0
        mixed_pos = 0
        formula_bad = 0
        for T in pos:
            reach = {bin(m).count("1") for m in maximals if (m & T) == T}
            if len({s % 2 for s in reach}) != 1:
                mixed_pos += 1
                continue
            p = next(iter(reach)) % 2
            uniform_checked += 1
            if G[T] != (p - bin(T).count("1")) % 2:
                formula_bad += 1

        out[name] = {
            "start_cap": sorted(bits(mask)),
            "positions_in_residue": len(pos),
            "maximal_extension_sizes": maximal_sizes,
            "parities": sorted({s % 2 for s in maximal_sizes}),
            "grundy_distribution": {str(k): v for k, v in sorted(dist.items())},
            "grundy_max": best,
            "witness_positions": [sorted(bits(m)) for m in wit[:3]],
            "k1298_formula_uniform_positions_checked": uniform_checked,
            "k1298_formula_violations": formula_bad,
            "positions_with_mixed_completion_parity": mixed_pos,
        }
        print(f"[{name}] start {out[name]['start_cap']}: {len(pos)} positions, "
              f"maximal sizes {maximal_sizes}, parities {out[name]['parities']}")
        print(f"    Grundy distribution {out[name]['grundy_distribution']}, max {best}")
        if best >= 2:
            print(f"    witness position {out[name]['witness_positions'][0]} -> Grundy {best}")
        print(f"    K1298 formula G(T)=(p-|T|)%2: checked {uniform_checked} uniform "
              f"positions, violations {formula_bad}; mixed-completion positions {mixed_pos}")

    (OUT / "task4_grundy_witness.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    ok = bool(out["mixed"] and out["mixed"]["parities"] == [0, 1]
              and out["mixed"]["grundy_max"] >= 2)
    if out["uniform_control"] is not None:
        ok = ok and out["uniform_control"]["grundy_max"] <= 1
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
