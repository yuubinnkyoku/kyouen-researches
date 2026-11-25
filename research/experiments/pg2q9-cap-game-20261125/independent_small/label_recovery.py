"""How the board's point labelling was recovered (and then verified).

The board file only gives lines as sets of point indices; it does not say which
vector of GF(9)^3 each index is.  We recovered the correspondence from the data:

1. the first 10 lines (indices 0..9) all contain point 0 and each is
   {0} + a block of 9 consecutive indices:
        L0 = {0} u {1..9},  L1 = {0} u {10..18}, ... , L9 = {0} u {82..90}
   so index 0 is the base of a pencil and the other 90 points are grouped
   block-by-block by the pencil line they lie on.
2. that is exactly what you get from the map

        index 0             -> (0:0:1)
        index 1+j  (0<=j<9) -> (0:1:E[j])
        index 10+9p+j       -> (1:E[p]:E[j])          E[k] = 3*(k//3)+(k%3)

   (i.e. "all points of the line x=0 first, then the points with x=1 ordered
   lexicographically by (y,z)"), because the lines through (0:0:1) are
   x = 0 and y = lam*x, and y = lam*x carries exactly the 9 points
   (1:lam:z), z in GF(9).

This script re-derives the pencil structure from the file and then verifies
that the map reproduces all 91 lines *in the file's own order*.
"""
import json
from pathlib import Path

BOARD = Path(__file__).resolve().parent.parent / "output" / "board_pg2q9.txt"


def read_board(path):
    with open(path, "r", encoding="utf-8") as fh:
        head = fh.readline().split()
        n, nl = int(head[0]), int(head[1])
        lines = []
        for _ in range(nl):
            parts = fh.readline().split()
            assert int(parts[0]) == len(parts) - 1
            lines.append(tuple(int(x) for x in parts[1:]))
        rest = fh.read().strip()
    return n, nl, lines, rest


# ---- GF(9) ----
ADD = [[0] * 9 for _ in range(9)]
MUL = [[0] * 9 for _ in range(9)]
NEG = [0] * 9
INV = [0] * 9


def enc(a, b):
    return 3 * a + b


for _x in range(9):
    _a, _b = _x // 3, _x % 3
    NEG[_x] = enc((-_a) % 3, (-_b) % 3)
    for _y in range(9):
        _c, _d = _y // 3, _y % 3
        ADD[_x][_y] = enc((_a + _c) % 3, (_b + _d) % 3)
        MUL[_x][_y] = enc((_a * _c - _b * _d) % 3, (_a * _d + _b * _c) % 3)
for _x in range(1, 9):
    for _y in range(1, 9):
        if MUL[_x][_y] == 3:
            INV[_x] = _y
ZERO, ONE = 0, 3


def vadd(u, v):
    return (ADD[u[0]][v[0]], ADD[u[1]][v[1]], ADD[u[2]][v[2]])


def vsmul(c, v):
    return (MUL[c][v[0]], MUL[c][v[1]], MUL[c][v[2]])


def canon(v):
    for x in v:
        if x != ZERO:
            ix = INV[x]
            return (MUL[ix][v[0]], MUL[ix][v[1]], MUL[ix][v[2]])
    raise ValueError


def main():
    n, nl, board, rest = read_board(BOARD)
    # ---- step 1: pencil structure at point 0 ----
    thr = [i for i, L in enumerate(board) if 0 in L]
    blocks = []
    for i in thr:
        other = sorted(set(board[i]) - {0})
        blocks.append(other)
    structure = {
        "lines_through_0": thr,
        "each_is_0_plus_9_consecutive": all(
            b == list(range(b[0], b[0] + 9)) for b in blocks),
        "blocks": [[b[0], b[-1]] for b in blocks],
    }

    # ---- step 2: the candidate index -> vector map ----
    PTS = [None] * 91
    PTS[0] = (ZERO, ZERO, ONE)
    for j in range(9):
        PTS[1 + j] = (ZERO, ONE, j)
    for p in range(9):
        for j in range(9):
            PTS[10 + 9 * p + j] = (ONE, p, j)
    assert all(v is not None for v in PTS)
    idx = {v: i for i, v in enumerate(PTS)}
    assert len(idx) == 91

    lines = set()
    for i in range(91):
        for j in range(i + 1, 91):
            s = frozenset(idx[canon(vadd(vsmul(a, PTS[i]), vsmul(b, PTS[j])))]
                          for a in range(9) for b in range(9)
                          if not (a == ZERO and b == ZERO))
            lines.add(tuple(sorted(s)))
    mine = sorted(lines)
    same_set = mine == sorted(tuple(sorted(L)) for L in board)
    same_order = mine == [tuple(sorted(L)) for L in board]
    print(json.dumps({**structure,
                      "n_computed_lines": len(mine),
                      "reproduces_board_as_set": same_set,
                      "reproduces_board_in_file_order": same_order,
                      "trailing_content": rest}, indent=1))


if __name__ == "__main__":
    main()
