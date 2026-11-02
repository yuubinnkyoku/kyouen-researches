#!/usr/bin/env python3
"""Independent complete-call proof check for one 11x11 six-stone WIN.

The certificate is zlib-compressed/base64-encoded bytes: one chosen point
per first-encountered first-player turn, in deterministic depth-first order.
At opponent turns ALL legal moves are expanded in ascending point order.
Repeated states are visited once. There is no trusted verdict cache.

Geometry: exact 4x4 integer determinant via fourth-row Laplace expansion,
independent of the generator's 3x3 row-difference determinant.
"""
import base64
import hashlib
import itertools
import json
import sys
import zlib
from functools import lru_cache
from pathlib import Path

N = 121
FULL = (1 << N) - 1
ROOT = int("00000000000200801002000081000000", 16)
EXPECTED_SHA256 = "83bdd3c89555bd80eadae802d47a8dc8289f0aee1a935440fb325f7f9ce25b2b"
EXPECTED = (18649, 12068, 4027, 2554, 27947)
ROWS = tuple((x*x+y*y, x, y, 1)
             for y in range(11) for x in range(11))


def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))


@lru_cache(maxsize=None)
def forbidden(a, b, c):
    first = (ROWS[a], ROWS[b], ROWS[c])
    cofactors = []
    for omit in range(4):
        tri = tuple(tuple(row[j] for j in range(4) if j != omit)
                    for row in first)
        cofactors.append((-1 if omit % 2 == 0 else 1) * det3(*tri))
    bad = 0
    for d, row in enumerate(ROWS):
        if d in (a, b, c):
            continue
        if sum(cofactors[j]*row[j] for j in range(4)) == 0:
            bad |= 1 << d
    return bad


def legal(board):
    ps = tuple(p for p in range(N) if board >> p & 1)
    bad = board
    for triple in itertools.combinations(ps, 3):
        bad |= forbidden(*triple)
    return FULL & ~bad


def safe(board):
    ps = tuple(p for p in range(N) if board >> p & 1)
    return all(not (forbidden(*triple) & board)
               for triple in itertools.combinations(ps, 3))


def verify(data):
    if not isinstance(data, bytes) or not safe(ROOT) or ROOT.bit_count() != 6:
        raise ValueError("invalid certificate or root")
    seen = set()
    index = 0
    strategies = terminals = opponents = edges = 0

    def dfs(board):
        nonlocal index, strategies, terminals, opponents, edges
        if board in seen:
            return
        seen.add(board)
        moves = legal(board)
        if board.bit_count() % 2 == 0:
            if not moves:
                raise ValueError("first player loses at terminal")
            if index >= len(data):
                raise ValueError("missing first-player strategy move")
            p = data[index]
            index += 1
            if p >= N or not (moves >> p & 1):
                raise ValueError("illegal first-player strategy move")
            strategies += 1
            edges += 1
            dfs(board | 1 << p)
        elif not moves:
            terminals += 1
        else:
            opponents += 1
            for p in range(N):
                if moves >> p & 1:
                    edges += 1
                    dfs(board | 1 << p)

    dfs(ROOT)
    if index != len(data):
        raise ValueError("unreachable or extra strategy moves")
    return (len(seen), strategies, opponents, terminals, edges)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: verifier certificate.b64 [--negative]")
    encoded = Path(sys.argv[1]).read_text(encoding="ascii")
    data = zlib.decompress(base64.b64decode(encoded, validate=False))
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise ValueError("certificate bytes differ from independently checked input")
    result = verify(data)
    if result != EXPECTED:
        raise ValueError(f"terminal replay totals changed: {result}")
    negative = 0
    if "--negative" in sys.argv:
        for altered in (data[:-1], data + b"\x00",
                        b"\x00" + data[1:],
                        data[:10] + b"\xff" + data[11:]):
            try:
                verify(altered)
            except ValueError:
                negative += 1
            else:
                raise AssertionError("forged strategy accepted")
        if negative != 4:
            raise AssertionError("negative tests incomplete")
    print(json.dumps({
        "root": f"{ROOT:032x}",
        "original_first_player": "WIN",
        "reached": result[0],
        "strategy_nodes": result[1],
        "opponent_nonterminal": result[2],
        "terminal": result[3],
        "edges": result[4],
        "first_player_losing_terminal": 0,
        "certificate_bytes": len(data),
        "certificate_sha256": EXPECTED_SHA256,
        "independent_geometry": "exact 4x4 Laplace",
        "negative_tests": negative,
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN"
    }, indent=2))


if __name__ == "__main__":
    main()
