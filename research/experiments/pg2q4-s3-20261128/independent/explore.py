"""Exploratory independent enumeration of the PG(2,4) s=3 safe-set lattice.

Writes nothing outside this directory. Python standard library only.
"""
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOARD = HERE.parent.parent / "projective-blocking-kyouen-20261125" / "output" / "board_pg2q4.txt"


def read_board(path):
    rows = path.read_text().splitlines()
    n, nb = map(int, rows[0].split())
    blocks = []
    for row in rows[1:]:
        vals = list(map(int, row.split()))
        assert vals[0] == 5
        blocks.append(sum(1 << p for p in vals[1:]))
    assert len(blocks) == nb
    return n, blocks


def check_pg(n, blocks):
    """Verify the point/line axioms of a projective plane of order 4."""
    problems = []
    if n != 21:
        problems.append(f"n={n}")
    if len(blocks) != 21:
        problems.append(f"#lines={len(blocks)}")
    for i, m in enumerate(blocks):
        if m.bit_count() != 5:
            problems.append(f"line {i} size {m.bit_count()}")
    if len(set(blocks)) != len(blocks):
        problems.append("duplicate lines")
    pair_line = {}
    for i, m in enumerate(blocks):
        pts = [p for p in range(n) if (m >> p) & 1]
        for a in range(5):
            for b in range(a + 1, 5):
                pair_line[(pts[a], pts[b])] = pair_line.get((pts[a], pts[b]), 0) + 1
    bad = [k for k, v in pair_line.items() if v != 1]
    if bad:
        problems.append(f"{len(bad)} pairs not on exactly one line, e.g. {bad[:5]}")
    if len(pair_line) != n * (n - 1) // 2:
        problems.append("pair coverage incomplete")
    per_point = [sum(1 for m in blocks if (m >> p) & 1) for p in range(n)]
    if any(c != 5 for c in per_point):
        problems.append(f"points on not 5 lines: {per_point}")
    return problems


def enumerate_safe(n, blocks):
    """Enumerate every safe set exactly once by DFS in increasing point order."""
    pc = [[] for _ in range(n)]
    for c, m in enumerate(blocks):
        for p in range(n):
            if (m >> p) & 1:
                pc[p].append(c)
    counts = [0] * len(blocks)
    order = []
    sys_stack = [(0, 0)]  # (mask, next point index)
    # iterative DFS keeping the counts array consistent is awkward; use recursion
    import sys
    sys.setrecursionlimit(10000)

    def dfs(mask, start):
        order.append(mask)
        for p in range(start, n):
            ok = True
            for c in pc[p]:
                if counts[c] >= 3:
                    ok = False
                    break
            if not ok:
                continue
            for c in pc[p]:
                counts[c] += 1
            dfs(mask | (1 << p), p + 1)
            for c in pc[p]:
                counts[c] -= 1

    dfs(0, 0)
    return order, pc


def grundy_all(order):
    by_size = defaultdict(list)
    for m in order:
        by_size[m.bit_count()].append(m)
    g = {}
    for k in range(max(by_size), -1, -1):
        for m in by_size[k]:
            opts = set()
            for p in range(21):
                if (m >> p) & 1:
                    continue
                nm = m | (1 << p)
                if nm in g:
                    opts.add(g[nm])
            v = 0
            while v in opts:
                v += 1
            g[m] = v
    return by_size, g


def cone(n, blocks, base):
    """All safe supersets of base, with their full (upset-local) Grundy values."""
    pc = [[] for _ in range(n)]
    for c, m in enumerate(blocks):
        for p in range(n):
            if (m >> p) & 1:
                pc[p].append(c)
    counts = [0] * len(blocks)
    for p in range(n):
        if (base >> p) & 1:
            for c in pc[p]:
                counts[c] += 1
    order = []

    def dfs(mask, start):
        order.append(mask)
        for p in range(start, n):
            if (base >> p) & 1:
                continue
            if any(counts[c] >= 3 for c in pc[p]):
                continue
            for c in pc[p]:
                counts[c] += 1
            dfs(mask | (1 << p), p + 1)
            for c in pc[p]:
                counts[c] -= 1

    dfs(base, 0)
    g = {}
    for m in sorted(order, key=lambda x: -x.bit_count()):
        opts = set()
        for p in range(n):
            if (m >> p) & 1:
                continue
            nm = m | (1 << p)
            if nm in g:
                opts.add(g[nm])
        v = 0
        while v in opts:
            v += 1
        g[m] = v
    return order, g


def main():
    n, blocks = read_board(BOARD)
    problems = check_pg(n, blocks)
    print("PG(2,4) axiom problems:", problems if problems else "NONE")

    triples = list(__import__("itertools").combinations(range(n), 3))
    line_of = {}
    for i, m in enumerate(blocks):
        pts = [p for p in range(n) if (m >> p) & 1]
        for a in range(5):
            for b in range(a + 1, 5):
                line_of[(pts[a], pts[b])] = i

    def collinear(t):
        a, b, c = t
        return (blocks[line_of[(a, b)]] >> c) & 1

    cols = [t for t in triples if collinear(t)]
    noncols = [t for t in triples if not collinear(t)]
    print(f"C(21,3)={len(triples)} collinear={len(cols)} noncollinear={len(noncols)}")
    print("collinear triples == 21*C(5,3):", len(cols) == 21 * math.comb(5, 3))

    order, pc = enumerate_safe(n, blocks)
    by_size, g = grundy_all(order)
    print("total safe sets:", len(order))
    print("size distribution:", {k: len(v) for k, v in sorted(by_size.items())})
    dist = {k: dict(Counter(g[m] for m in v)) for k, v in sorted(by_size.items())}
    print("size/G distribution:", dist)
    term = {k: sum(1 for m in v if not any(
        ((m | (1 << p)) in g) for p in range(n) if not ((m >> p) & 1))) for k, v in sorted(by_size.items())}
    print("maximal (terminal) counts by size:", term)

    for name, base in [("triangle {0,1,5}", (1 << 0) | (1 << 1) | (1 << 5)),
                       ("collinear {0,1,2}", (1 << 0) | (1 << 1) | (1 << 2))]:
        ordc, gc = cone(n, blocks, base)
        Tc = Counter(m.bit_count() for m in ordc)
        Gc = defaultdict(Counter)
        for m in ordc:
            Gc[m.bit_count()][gc[m]] += 1
        print(f"cone {name}: size={len(ordc)}")
        for k in sorted(Tc):
            print(f"   k={k}: T={Tc[k]} G={dict(Gc[k])}")

    # write a machine-readable dump for later steps
    out = {
        "problems": problems,
        "counts": {str(k): len(v) for k, v in sorted(by_size.items())},
        "grundy": {str(k): {str(x): c for x, c in sorted(dist[k].items())} for k in sorted(dist)},
        "terminal": {str(k): v for k, v in sorted(term.items())},
    }
    (HERE / "explore_out.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
