"""AG(2,q) for prime powers: circles and lines over F_q, q = p^e.

ff_structure.py only handles prime q (it uses integer coordinates mod q).
For q = 4, 8, 9 we need F_q as F_p[t]/(f).

Blocks:
  * lines: q(q+1) of them, each with q points,
  * circles: the board traces of x^2+y^2+Dx+Ey+F = 0, deduplicated.

A set is safe iff no block carries 4 of its points.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from inversive_prime_power import FiniteField, factorize, find_irreducible


def build_ag(q: int):
    fac = factorize(q)
    if len(fac) != 1:
        raise ValueError(f"q={q} is not a prime power")
    p, e = fac[0]
    F = FiniteField(p, e, find_irreducible(p, e))
    # points of AG(2,q) are pairs (x,y) of field elements
    pts = [(x, y) for x in F.elements() for y in F.elements()]
    idx = {pt: i for i, pt in enumerate(pts)}
    n = len(pts)

    # lines: {a + t*b : t in F} for each direction b up to F^* scaling,
    # where a and b are POINTS of AG(2,q) = F_q^2 (pairs of field elements).
    lines = set()
    seen_dirs = set()
    for b in pts:
        if b == (F.zero, F.zero):
            continue
        # canonical representative: scale so the first non-zero component is 1
        canon = None
        for comp in b:
            if not F.is_zero(comp):
                inv = F.inv(comp)
                canon = tuple(F.mul(c, inv) for c in b)
                break
        if canon in seen_dirs:
            continue
        seen_dirs.add(canon)
        for a in pts:
            line = frozenset(
                idx[(F.add(a[0], F.mul(t, b[0])), F.add(a[1], F.mul(t, b[1])))]
                for t in F.elements()
            )
            lines.add(line)

    # circles: x^2+y^2+Dx+Ey+F0 = 0, where (x,y) ranges over F_q^2
    circles = set()
    for D in F.elements():
        for E in F.elements():
            for F0 in F.elements():
                s = set()
                for x in F.elements():
                    for y in F.elements():
                        val = F.add(
                            F.add(F.add(F.mul(x, x), F.mul(y, y)), F.mul(D, x)),
                            F.add(F.mul(E, y), F0),
                        )
                        if F.is_zero(val):
                            s.add(idx[(x, y)])
                if len(s) >= 3:
                    circles.add(frozenset(s))

    blocks = [sorted(b) for b in circles] + [sorted(b) for b in lines]
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, b in enumerate(blocks):
        for i in b:
            through[i].append(bi)
    return pts, blocks, through, len(circles), len(lines)


def exists_safe_set(q: int, target: int, node_cap: int = 100_000_000):
    pts, blocks, through, nc, nl = build_ag(q)
    n = len(pts)
    n_blocks = len(blocks)
    nodes = 0
    order = sorted(range(n), key=lambda i: len(through[i]))
    rank = {p: r for r, p in enumerate(order)}
    bpts = [tuple(b) for b in blocks]

    def rec(pmask: int, size: int, start_rank: int, cnt: list, chosen: list):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError(f"node cap {node_cap} exceeded")
        if size == target:
            return list(chosen)
        need = (target * (target - 1) * (target - 2) - size * (size - 1) * (size - 2)) // 6
        usable = 0
        for bi in range(n_blocks):
            c = cnt[bi]
            if c >= 3:
                continue
            free = 0
            for j in bpts[bi]:
                if not (pmask >> j & 1):
                    free += 1
            if c + free >= 3:
                usable += 1
        if need > usable:
            return None
        for r in range(start_rank, n):
            i = order[r]
            if pmask >> i & 1:
                continue
            ok = True
            for bi in through[i]:
                if cnt[bi] >= 3:
                    ok = False
                    break
            if not ok:
                continue
            for bi in through[i]:
                cnt[bi] += 1
            chosen.append(i)
            res = rec(pmask | (1 << i), size + 1, r + 1, cnt, chosen)
            chosen.pop()
            for bi in through[i]:
                cnt[bi] -= 1
            if res is not None:
                return res
        return None

    cnt = [0] * n_blocks
    try:
        i0 = order[0]
        for bi in through[i0]:
            cnt[bi] += 1
        witness = rec(1 << i0, 1, rank[i0] + 1, cnt, [i0])
    except TimeoutError as e:
        return None, nodes, str(e), (nc, nl)
    if witness is None:
        return None, nodes, "exhausted (no set of this size)", (nc, nl)
    return [pts[i] for i in witness], nodes, "found", (nc, nl)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[4])
    ap.add_argument("--max-target", type=int, default=8)
    ap.add_argument("--node-cap", type=int, default=100_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        results = []
        K = None
        for t in range(4, args.max_target + 1):
            witness, nodes, status, (nc, nl) = exists_safe_set(q, t, args.node_cap)
            results.append({"target": t, "exists": witness is not None,
                            "nodes": nodes, "status": status})
            print(f"q={q} target={t}: exists={witness is not None} nodes={nodes} "
                  f"status={status} (circles={nc}, lines={nl})", flush=True)
            if witness is None:
                K = t - 1
                break
        rows.append({"q": q, "K": K, "results": results})
        print(f"q={q}: K = {K}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
