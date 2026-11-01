#!/usr/bin/env python3
"""Independently replay a complete original-first WIN strategy from a fixed S6.

The certificate supplies first-player moves only. Every second-player move is
recomputed by independent 4x4 Bareiss integer geometry, and every reached
terminal must be an odd-stone (original-first WIN) position. No solver verdicts
or historical caches are read.
"""
import argparse
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json

N = 11
V = 121
BOARD = (1 << V) - 1
ROOT = int("00000000000000603800000000008000", 16)
HERE = Path(__file__).resolve().parent
CERT = HERE / "focus_s6_win_strategy_1984.cert"


def need(ok, why):
    if not ok:
        raise ValueError(why)


def points(mask):
    result = []
    while mask:
        bit = mask & -mask
        result.append(bit.bit_length() - 1)
        mask ^= bit
    return result


def determinant4(a, b, c, d):
    matrix = []
    for p in (a, b, c, d):
        x, y = p % N, p // N
        matrix.append([x*x+y*y, x, y, 1])
    sign, prev = 1, 1
    for k in range(3):
        if matrix[k][k] == 0:
            pivot_row = next((i for i in range(k+1, 4) if matrix[i][k]), None)
            if pivot_row is None:
                return 0
            matrix[k], matrix[pivot_row] = matrix[pivot_row], matrix[k]
            sign = -sign
        pivot = matrix[k][k]
        for i in range(k+1, 4):
            for j in range(k+1, 4):
                numerator = matrix[i][j]*pivot - matrix[i][k]*matrix[k][j]
                need(numerator % prev == 0, "non-integral Bareiss step")
                matrix[i][j] = numerator // prev
            matrix[i][k] = 0
        prev = pivot
    return sign * matrix[3][3]


@lru_cache(maxsize=None)
def blocked_by_triple(a, b, c):
    return sum(1 << p for p in range(V) if determinant4(a, b, c, p) == 0)


def legal_moves(mask):
    ps = points(mask)
    blocked = mask
    for triple in combinations(ps, 3):
        blocked |= blocked_by_triple(*triple)
    return points(BOARD & ~blocked)


def read_certificate(text):
    lines = text.splitlines()
    need(len(lines) >= 4 and lines[:3] == [
        "# n11-original-first-WIN-strategy-v1", "BOARD 11",
        "ROOT 00000000000000603800000000008000"], "wrong certificate header")
    strategy = {}
    previous = -1
    for line in lines[3:]:
        row = line.split(" ")
        need(len(row) == 2, "malformed strategy row")
        key, move = row
        need(len(key) == 32 and all(c in "0123456789abcdef" for c in key)
             and move.isascii() and move.isdecimal(), "invalid key or move")
        mask = int(key, 16)
        p = int(move)
        need(previous < mask <= BOARD and 0 <= p < V,
             "duplicate/unsorted/off-board strategy row")
        need(mask.bit_count() % 2 == 0, "strategy at wrong player turn")
        previous = mask
        strategy[mask] = p
    need(len(strategy) == 5923, "wrong strategy entry count")
    return strategy


def replay(strategy):
    need(ROOT in strategy and strategy[ROOT] == 20,
         "missing or changed root winning move")
    visited = set()
    terminal = []

    def visit(mask):
        if mask in visited:
            return
        visited.add(mask)
        moves = legal_moves(mask)
        n = mask.bit_count()
        if not moves:
            need(n % 2 == 1, "reached losing even-stone terminal")
            terminal.append(n)
        elif n % 2 == 0:
            need(mask in strategy, "first-player strategy move missing")
            p = strategy[mask]
            need(p in moves, "first-player move is illegal")
            visit(mask | (1 << p))
        else:
            for p in moves:
                visit(mask | (1 << p))

    visit(ROOT)
    need(set(strategy) <= visited, "unreachable/unused strategy entries")
    need((len(visited), len(terminal), min(terminal), max(terminal))
         == (8949, 951, 13, 17), "proof DAG counts changed")
    return {
        "schema": "n11-central49-focused-s6-terminal-win-strategy-v1",
        "root": f"{ROOT:032x}",
        "first_player_winning_move": 20,
        "even_strategy_nodes": len(strategy),
        "visited_states": len(visited),
        "odd_terminal_win_leaves": len(terminal),
        "minimum_terminal_stones": min(terminal),
        "maximum_terminal_stones": max(terminal),
        "s6_original_first_outcome": "WIN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
        "evidence_level": "INDEPENDENT_FULL_TERMINAL_STRATEGY_REPLAY"
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=CERT)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    raw = args.certificate.read_text(encoding="utf-8")
    result = replay(read_certificate(raw))
    if args.negative:
        for mutation in (
            raw.replace("00000000000000603800000000008000 20",
                        "00000000000000603800000000008000 15", 1),
            raw.replace("BOARD 11", "BOARD 10", 1),
            "\n".join(raw.splitlines()[:-1]) + "\n",
        ):
            try:
                replay(read_certificate(mutation))
            except ValueError:
                continue
            raise AssertionError("tampered certificate accepted")
        result["negative_tests"] = 3
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
