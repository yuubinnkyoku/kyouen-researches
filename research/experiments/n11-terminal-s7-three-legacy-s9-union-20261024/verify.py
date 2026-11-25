#!/usr/bin/env python3
"""Two integer-geometry methods independently recheck S9 AND certificates."""
import argparse
import json
from itertools import combinations
from pathlib import Path

ROOTS = ("00000100910000001042100000000040",
         "00000000000830841040000004010000",
         "00000100100000001042100000004018")
STATES = (941, 2877, 190)
XY = [(i % 11, i // 11) for i in range(121)]


def det3(a, b, c, d):
    x, y = XY[d]
    u, v, w = [(XY[p][0]-x, XY[p][1]-y,
                XY[p][0]**2+XY[p][1]**2-x*x-y*y)
               for p in (a, b, c)]
    return (u[0]*(v[1]*w[2]-v[2]*w[1])
            - u[1]*(v[0]*w[2]-v[2]*w[0])
            + u[2]*(v[0]*w[1]-v[1]*w[0]))


def det4(a, b, c, d):
    rows = [[XY[p][0]**2+XY[p][1]**2, XY[p][0], XY[p][1], 1]
            for p in (a, b, c, d)]
    sign = 1
    for k in range(3):
        if rows[k][k] == 0:
            j = next((j for j in range(k+1, 4) if rows[j][k]), None)
            if j is None:
                return 0
            rows[k], rows[j] = rows[j], rows[k]
            sign = -sign
        pivot = rows[k][k]
        for i in range(k+1, 4):
            for j in range(k+1, 4):
                numerator = rows[i][j]*pivot-rows[i][k]*rows[k][j]
                rows[i][j] = numerator//(1 if k == 0 else rows[k-1][k-1])
            rows[i][k] = 0
    return sign*rows[3][3]


def points(board):
    return [i for i in range(121) if board >> i & 1]


def canonical(board):
    result = None
    for t in range(8):
        out = 0
        for i in points(board):
            x, y = XY[i]
            q = ((x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
                 (10-x, y), (10-y, 10-x), (x, 10-y), (y, x))[t]
            out |= 1 << (q[1]*11+q[0])
        result = out if result is None else min(result, out)
    return result


def legal(board, determinant):
    triples = list(combinations(points(board), 3))
    return [i for i in range(121) if not (board >> i & 1)
            and not any(determinant(*q, i) == 0 for q in triples)]


def solve10(key, determinant):
    board = int(key, 16)
    base = points(board)
    moves = legal(board, determinant)
    n = len(moves)
    assert n <= 63, (key, n)
    bad = []
    for i, j in combinations(range(n), 2):
        if any(determinant(a, c, moves[i], moves[j]) == 0
               for a, c in combinations(base, 2)):
            bad.append((1 << i) | (1 << j))

    def forbidden(mask):
        return any(mask & z == z for z in bad)

    for i, j, k in combinations(range(n), 3):
        mask = (1 << i) | (1 << j) | (1 << k)
        if not forbidden(mask) and any(
                determinant(p, moves[i], moves[j], moves[k]) == 0
                for p in base):
            bad.append(mask)
    for i, j, k, l in combinations(range(n), 4):
        mask = (1 << i) | (1 << j) | (1 << k) | (1 << l)
        if not forbidden(mask) and determinant(
                moves[i], moves[j], moves[k], moves[l]) == 0:
            bad.append(mask)

    bans = [[] for _ in range(n)]
    for mask in bad:
        for i in range(n):
            if mask >> i & 1:
                bans[i].append(mask ^ (1 << i))
    memo = {}

    def win(state):
        if state in memo:
            return memo[state]
        for i in range(n):
            bit = 1 << i
            if state & bit or any(state & x == x for x in bans[i]):
                continue
            if not win(state | bit):
                memo[state] = True
                return True
        memo[state] = False
        return False

    return win(0), len(memo), n


def verify(cert, terminal=True):
    assert cert["format"] == "n11-s9-three-legacy-terminal-v1"
    assert cert["board"] == 11 and cert["perspective"] == "fixed-original-first"
    assert cert["empty_winner"] == "UNKNOWN"
    assert len(cert["roots"]) == 3
    total_leaves = total_states = 0
    for row, root, expected in zip(cert["roots"], ROOTS, STATES):
        assert row["s9_win"] == root and row["states"] == expected
        board = int(root, 16)
        assert len(points(board)) == 9 and canonical(board) == board
        assert all(det3(*q) != 0 and det4(*q) != 0
                   for q in combinations(points(board), 4))
        children3 = sorted({f"{canonical(board | (1 << i)):032x}"
                            for i in legal(board, det3)})
        children4 = sorted({f"{canonical(board | (1 << i)):032x}"
                            for i in legal(board, det4)})
        assert children3 == children4 == row["s10_win_children"]
        subtotal = 0
        if terminal:
            for key in children3:
                a, b = solve10(key, det3), solve10(key, det4)
                assert a == b and a[0], (root, key, a, b)
                subtotal += a[1]
            assert subtotal == expected
        total_leaves += len(children3)
        total_states += subtotal
    assert total_leaves == 50
    assert not terminal or total_states == 4008
    return {"s9_win_roots": 3, "s10_win_leaves": total_leaves,
            "states": total_states if terminal else None,
            "empty_board": "UNKNOWN"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    cert = json.loads(Path(__file__).with_name("certificate.json").read_text())
    print(json.dumps(verify(cert), indent=2))
    if args.negative:
        from copy import deepcopy
        for mutation in range(4):
            c = deepcopy(cert)
            if mutation == 0:
                c["roots"][0]["s10_win_children"].pop()
            elif mutation == 1:
                c["roots"][1]["s10_win_children"][0] = c["roots"][1]["s10_win_children"][1]
            elif mutation == 2:
                c["roots"][2]["s9_win"] = c["roots"][0]["s9_win"]
            else:
                c["board"] = 10
            try:
                verify(c, terminal=False)
            except AssertionError:
                continue
            raise RuntimeError("mutation accepted")
        print("PASS four malformed certificates rejected")
