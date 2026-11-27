"""Shared helpers for the independent verification of the AG(2,9) cap-game claim.

Standard library only.

Independent conventions used here (written from scratch, not copied from the
parent scripts):

  field element   : pair (a, b) meaning a + b*i with i^2 = -1 = 2 (mod 3)
  field order E   : enc(a,b) = 3*a + b, i.e. E = [0, 1, 2, i, 1+i, 1+2i, 2, 2+i, 2+2i]
  own point index : 9*enc(y) + enc(x)   (``y-major``); the parent uses 9*enc(x)+enc(y)
  own line order  : 9 vertical lines x = c (c in E order), then 81 lines y = m*x + b
                    (m in E order, b in E order)

The parent board is read from ../output/board_ag2q9.txt and is analysed, never
written.
"""

from pathlib import Path

MOD = 3

E = [(a, b) for a in range(3) for b in range(3)]
ZERO = (0, 0)
ONE = (1, 0)


# ---------------------------------------------------------------- GF(9)
def fadd(u, v):
    return ((u[0] + v[0]) % MOD, (u[1] + v[1]) % MOD)


def fsub(u, v):
    return ((u[0] - v[0]) % MOD, (u[1] - v[1]) % MOD)


def fneg(u):
    return ((-u[0]) % MOD, (-u[1]) % MOD)


def fmul(u, v):
    a, b = u
    c, d = v
    return ((a * c - b * d) % MOD, (a * d + b * c) % MOD)


def fiszero(u):
    return u[0] == 0 and u[1] == 0


def finv(u):
    if fiszero(u):
        raise ZeroDivisionError
    for v in E:
        if fmul(u, v) == ONE:
            return v
    raise AssertionError("no inverse")


def enc(u):
    return 3 * u[0] + u[1]


def dec(k):
    return (k // 3, k % 3)


# ---------------------------------------------------------------- boards
def build_board(major="y"):
    """Build AG(2,9) from the field.

    Returns (points, lines) where ``points[i]`` is the field-coordinate pair and
    ``lines`` is the ordered list of 90 index lists.

    major="y": index = 9*enc(y) + enc(x)
    major="x": index = 9*enc(x) + enc(y)   (the parent's convention)
    """
    if major == "x":
        pts = [(x, y) for x in E for y in E]
    else:
        pts = [(x, y) for y in E for x in E]
    idx = {p: i for i, p in enumerate(pts)}
    lines = []
    for c in E:                                # vertical lines x = c
        lines.append([idx[(c, y)] for y in E])
    for m in E:                                # y = m*x + b
        for b in E:
            lines.append([idx[(x, fadd(fmul(m, x), b))] for x in E])
    return pts, lines


def parse_board(path):
    """Read a board file: first line 'n num_lines', then '9 p1 ... p9' rows."""
    rows = Path(path).read_text(encoding="utf-8").splitlines()
    n, nb = map(int, rows[0].split())
    lines = []
    for row in rows[1:]:
        if not row.strip():
            continue
        vals = list(map(int, row.split()))
        if vals[0] != len(vals) - 1:
            raise ValueError("bad row: %r" % row)
        lines.append(vals[1:])
    if len(lines) != nb:
        raise ValueError("expected %d lines, got %d" % (nb, len(lines)))
    return n, nb, lines


def line_masks(n, lines):
    out = []
    for L in lines:
        m = 0
        for p in L:
            m |= 1 << p
        out.append(m)
    return out


def point_lines(n, masks):
    """For every point, the list of indices of lines through it."""
    pl = [[] for _ in range(n)]
    for ci, m in enumerate(masks):
        mm = m
        while mm:
            b = mm & -mm
            pl[b.bit_length() - 1].append(ci)
            mm ^= b
    return pl


def verify_linear_space(n, lines):
    """Check the AG(2,9) axiom package; returns a dict of checks and a list of errors."""
    errors = []
    info = {}
    info["n_points"] = n
    info["n_lines"] = len(lines)
    if n != 81:
        errors.append("n != 81")
    if len(lines) != 90:
        errors.append("line count != 90")

    seen = set()
    for L in lines:
        if len(L) != 9:
            errors.append("line of length %d" % len(L))
        if len(set(L)) != 9:
            errors.append("repeated point inside a line")
        for p in L:
            if not (0 <= p < n):
                errors.append("point out of range")
        key = tuple(sorted(L))
        if key in seen:
            errors.append("duplicate line")
        seen.add(key)
    if errors:
        return {"ok": False, "errors": errors[:10], **info}

    masks = line_masks(n, lines)

    # every pair of points on exactly one line
    paircount = {}
    for L in lines:
        s = sorted(L)
        for i in range(9):
            for j in range(i + 1, 9):
                paircount[(s[i], s[j])] = paircount.get((s[i], s[j]), 0) + 1
    bad_pairs = [k for k, v in paircount.items() if v != 1]
    if len(paircount) != n * (n - 1) // 2:
        errors.append("not all pairs covered")
    if bad_pairs:
        errors.append("%d pairs not on exactly one line" % len(bad_pairs))

    # two distinct lines meet in at most one point; the disjoint pairs are the
    # 10 parallel classes (each line has exactly 8 parallel partners)
    bad_intersections = 0
    disjoint_pairs = 0
    for i in range(len(masks)):
        for j in range(i + 1, len(masks)):
            inter = (masks[i] & masks[j]).bit_count()
            if inter > 1:
                bad_intersections += 1
            elif inter == 0:
                disjoint_pairs += 1
    if bad_intersections:
        errors.append("%d line pairs meet in more than one point" % bad_intersections)
    info["disjoint_line_pairs"] = disjoint_pairs
    if disjoint_pairs != 360:
        errors.append("disjoint line pairs != 360 (90*8/2)")

    # every point on exactly 10 lines
    deg = [0] * n
    for L in lines:
        for p in L:
            deg[p] += 1
    if any(d != 10 for d in deg):
        errors.append("point degree != 10")

    # parallelism: the 10 parallel classes each have 9 disjoint lines covering all points
    full = (1 << n) - 1
    used = [False] * len(masks)
    nclasses = 0
    for i in range(len(masks)):
        if used[i]:
            continue
        cls = [i] + [j for j in range(len(masks)) if not used[j] and j != i and (masks[j] & masks[i]) == 0]
        u = 0
        for j in cls:
            u |= masks[j]
            used[j] = True
        if len(cls) != 9 or u != full:
            errors.append("bad parallel class at line %d" % i)
        nclasses += 1
    info["parallel_classes"] = nclasses
    if nclasses != 10:
        errors.append("parallel class count != 10")

    info["ok"] = not errors
    info["errors"] = errors
    return info


def cap_violations(mask, masks):
    """Return the number of lines containing >= 3 points of ``mask``."""
    return sum(1 for m in masks if (mask & m).bit_count() >= 3)


def is_cap(mask, masks):
    return all((mask & m).bit_count() <= 2 for m in masks)


def mex(values):
    v = 0
    while v in values:
        v += 1
    return v
