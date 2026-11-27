"""Independent verification: board is PG(2,9), determine coordinate convention.

Board file: output/board_pg2q9.txt
First line "91 91"; then 91 lines "10 p1 ... p10" (0-based point ids).

Model: GF(9) = GF(3)[i]/(i^2+1), i^2 = -1 = 2.
Elements are pairs (a,b) meaning a + b*i, a,b in GF(3).
Canonical nonzero vector: first nonzero coordinate is the field element 1.
Board index = rank among sorted canonical vectors (lexicographic in encoded coords).

This script:
  * parses the board and checks the projective-plane axioms,
  * tests candidate field-element integer encodings and sorted-canonical-vector
    index orders against the board's line sets,
  * reports the matching convention.
"""
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BOARD = ROOT.parent / "output" / "board_pg2q9.txt"

Q = 3
# field elements as (a,b), a+b*i, i^2=2
P = 3
ELEMS = [(a, b) for a in range(3) for b in range(3)]
ZERO = (0, 0)
ONE = (1, 0)
I = (0, 1)


def fadd(x, y):
    return ((x[0] + y[0]) % 3, (x[1] + y[1]) % 3)


def fneg(x):
    return ((-x[0]) % 3, (-x[1]) % 3)


def fsub(x, y):
    return fadd(x, fneg(y))


def fmul(x, y):
    # (a+bi)(c+di) = ac + bd*i^2 + (ad+bc)i = ac + 2bd + (ad+bc)i
    a, b = x
    c, d = y
    return ((a * c + 2 * b * d) % 3, (a * d + b * c) % 3)


def feq(x, y):
    return x == y


def parse_board():
    lines = BOARD.read_text().splitlines()
    n, m = map(int, lines[0].split())
    board = []
    for ln in lines[1:]:
        vals = list(map(int, ln.split()))
        assert vals[0] == len(vals) - 1
        board.append(tuple(vals[1:]))
    return n, m, board


def check_plane(n, m, rows):
    """Check the projective plane axioms on the raw board."""
    ok = True
    msgs = []
    pts = set(range(n))
    if len(rows) != m:
        ok = False
        msgs.append(f"line count {len(rows)} != {m}")
    for i, r in enumerate(rows):
        if len(r) != 10:
            ok = False
            msgs.append(f"line {i} length {len(r)}")
        if len(set(r)) != len(r):
            ok = False
            msgs.append(f"line {i} repeated point")
        if not set(r) <= pts:
            ok = False
            msgs.append(f"line {i} out-of-range point")
    # every pair of points on exactly one line
    pair_line = {}
    bad_pairs = []
    for li, r in enumerate(rows):
        for a, b in itertools.combinations(sorted(r), 2):
            key = (a, b)
            if key in pair_line:
                bad_pairs.append((key, pair_line[key], li))
            pair_line[key] = li
    total_pairs = n * (n - 1) // 2
    if len(pair_line) != total_pairs:
        ok = False
        msgs.append(f"pair coverage {len(pair_line)} != {total_pairs}")
    if bad_pairs:
        ok = False
        msgs.append(f"{len(bad_pairs)} pairs on >1 line")
    # each point on 10 lines
    deg = [0] * n
    for r in rows:
        for p in r:
            deg[p] += 1
    if any(d != 10 for d in deg):
        ok = False
        msgs.append(f"point degrees not all 10: {sorted(set(deg))}")
    # any two lines meet in exactly one point
    line_sets = [frozenset(r) for r in rows]
    bad_meet = []
    for i in range(m):
        for j in range(i + 1, m):
            inter = line_sets[i] & line_sets[j]
            if len(inter) != 1:
                bad_meet.append((i, j, len(inter)))
    if bad_meet:
        ok = False
        msgs.append(f"{len(bad_meet)} line pairs meet != 1 point; e.g. {bad_meet[:5]}")
    return ok, msgs, pair_line, deg


def canonical_vectors():
    """All canonical nonzero vectors under first-nonzero=1, over GF(9)."""
    out = []
    # x=0 -> y must be 1 if y nonzero; z free
    out.append((ZERO, ZERO, ONE))
    for z in ELEMS:
        out.append((ZERO, ONE, z))
    for y in ELEMS:
        for z in ELEMS:
            out.append((ONE, y, z))
    return out


def candidate_encodings():
    """Linear isomorphisms GF(3)^2 -> labels 0..8 with label(0)=0.

    An additive isomorphism is determined by images of 1=(1,0) and i=(0,1):
    label(a,b) = a*L1 + b*Li mod 3, interpreted in base 3 as L1*a + Li*b?
    We enumerate affine (Z/3)^2 structures: label(a,b) = (u*a+v*b mod 3) + 3*(w*a+x*b mod 3)
    over invertible 2x2 matrices.  This includes a+3b, b+3a, 3a+b, 3b+a, and
    the nontrivial GL(2,3) twists.  We also allow the coordinate label map to be
    applied to (a,b) before the base-3 packing.
    """
    encs = []
    gl2 = []
    for a, b, c, d in itertools.product(range(3), repeat=4):
        det = (a * d - b * c) % 3
        if det != 0:
            gl2.append((a, b, c, d))
    for M in gl2:
        a, b, c, d = M

        def enc(e, a=a, b=b, c=c, d=d):
            x, y = e
            return ((a * x + b * y) % 3) + 3 * ((c * x + d * y) % 3)

        encs.append((f"M={M}", enc))
    return encs


def main():
    n, m, rows = parse_board()
    print(f"board: {n} points, {m} lines")
    ok, msgs, pair_line, deg = check_plane(n, m, rows)
    print(f"PLANE_AXIOMS: {'PASS' if ok else 'FAIL'}")
    for s in msgs:
        print("  ", s)

    cv = canonical_vectors()
    assert len(cv) == 91, len(cv)

    # generate line sets as canonical-vector indices for each encoding, then
    # map to board ids by rank; compare to board line sets.
    results = []
    for name, enc in candidate_encodings():
        # ranks of canonical vectors
        keyed = sorted((enc(v[0]), enc(v[1]), enc(v[2]), k) for k, v in enumerate(cv))
        rank = {}
        for r, (_a, _b, _c, k) in enumerate(keyed):
            rank[k] = r
        # line sets in canonical-vector index space: normals canonical
        line_sets = set()
        for nv in cv:
            members = []
            for k, v in enumerate(cv):
                # nv . v = 0
                s = ZERO
                for x, y in zip(nv, v):
                    s = fadd(s, fmul(x, y))
                if s == ZERO:
                    members.append(rank[k])
            line_sets.add(frozenset(members))
        board_sets = set(frozenset(r) for r in rows)
        if line_sets == board_sets:
            results.append((name, rank, enc, True, 0))
        else:
            results.append((name, rank, enc, False, len(line_sets ^ board_sets)))

    matches = [r for r in results if r[3]]
    print(f"candidate encodings tested: {len(results)}; exact line-set matches: {len(matches)}")
    for name, rank, enc, good, diff in matches[:10]:
        print("  MATCH", name, "diff", diff)

    if matches:
        name, rank, enc, _, _ = matches[0]
        # dump mapping: board id -> canonical vector (a,b per coord)
        mapping = [None] * 91
        for k, v in enumerate(cv):
            mapping[rank[k]] = v
        out = {
            "board_points": n,
            "board_lines": m,
            "encoding": name,
            "rank_to_vector": [[[a, b] for (a, b) in v] for v in mapping],
        }
        (ROOT / "out" / "board_coordinates.json").write_text(json.dumps(out))
        print("wrote out/board_coordinates.json")
        # verify lines directly from mapping: each board line must be a line
        # (i.e. there is a nonzero normal orthogonal to all members)
        print("sample mapping: board id -> (x,y,z) in (a,b) pairs")
        for i in range(0, 91, 15):
            print(" ", i, mapping[i])
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
