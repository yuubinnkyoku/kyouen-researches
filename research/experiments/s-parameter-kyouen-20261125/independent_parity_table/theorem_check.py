"""Exhaustive check of the parity theorem underlying K1358 on small boards.

A board is modelled by its family of safe sets, which is an arbitrary finite
downward-closed family (simplicial complex) on n points.  (Every such family is
the safe-set family of a Kyouen board: take the minimal non-faces as blocks and
s large enough.)  For every complex on n=4 and n=5 points we compute the full
Grundy table and check

    (a) all Grundy values are in {0,1}
    (b) all maximal faces have the same size parity

are equivalent, that (b) implies G(S) = (p-|S|) mod 2, and that mixed parity
implies max Grundy >= 2.
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"


def antichains(n):
    """All antichains of the Boolean lattice on n points (as tuples of masks)."""
    subsets = sorted(range(1 << n), key=lambda m: (-m.bit_count(), m))
    res = []

    def rec(i, chosen):
        if i == len(subsets):
            res.append(tuple(chosen))
            return
        S = subsets[i]
        if any(S != T and (S | T) == T for T in chosen):
            rec(i + 1, chosen)
            return
        rec(i + 1, chosen)             # S is not a maximal face
        rec(i + 1, chosen + [S])       # S is a maximal face

    rec(0, [])
    return res


def faces_of(maximal):
    faces = set()
    for M in maximal:
        sub = M
        while True:
            faces.add(sub)
            if sub == 0:
                break
            sub = (sub - 1) & M
    return faces


def grundy_table(n, maximal):
    faces = faces_of(maximal)
    layers = defaultdict(list)
    for f in faces:
        layers[f.bit_count()].append(f)
    g = {}
    for size in range(max((m.bit_count() for m in maximal), default=0), -1, -1):
        for S in layers[size]:
            ch = set()
            for p in range(n):
                if (S >> p) & 1:
                    continue
                T = S | (1 << p)
                if T in faces:
                    ch.add(g[T])
            v = 0
            while v in ch:
                v += 1
            g[S] = v
    return faces, g


def check(n):
    stats = Counter()
    violations = []
    for maximal in antichains(n):
        maximal = list(maximal)
        if not maximal:
            # no faces at all is not a board with the empty position; skip
            continue
        faces, g = grundy_table(n, maximal)
        max_sizes = sorted({M.bit_count() for M in maximal})
        par = {m % 2 for m in max_sizes}
        uniform = len(par) == 1
        gvals = set(g.values())
        binary = gvals <= {0, 1}
        stats["boards"] += 1
        stats["uniform" if uniform else "mixed"] += 1
        if uniform != binary:
            violations.append({"n": n, "maximal": maximal,
                               "uniform": uniform, "gvals": sorted(gvals)})
            continue
        if uniform:
            p = max_sizes[0] % 2
            for S, v in g.items():
                if v != (p - S.bit_count()) % 2:
                    violations.append({"n": n, "maximal": maximal,
                                       "formula_fail": S, "g": v})
                    break
            if max(g.values()) > 1:
                violations.append({"n": n, "maximal": maximal,
                                   "uniform_max_g": max(g.values())})
        else:
            stats["mixed_max_g_ge_2"] += (max(g.values()) >= 2)
            if max(g.values()) < 2:
                violations.append({"n": n, "maximal": maximal,
                                   "mixed_max_g": max(g.values())})
    return stats, violations


def main():
    out = {}
    all_viol = []
    for n in (2, 3, 4, 5):
        stats, viol = check(n)
        print(f"n={n}: {dict(stats)} violations={len(viol)}", flush=True)
        out[str(n)] = {"stats": dict(stats), "violations": viol}
        all_viol.extend(viol)
    out["violations_total"] = len(all_viol)
    OUT.mkdir(exist_ok=True)
    (OUT / "theorem_small_boards.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8")
    print("total violations:", len(all_viol))


if __name__ == "__main__":
    main()
