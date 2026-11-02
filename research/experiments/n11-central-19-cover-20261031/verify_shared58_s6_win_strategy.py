#!/usr/bin/env python3
"""Independent terminal replay of a certified original-first WIN6.

This verifier does not use the searcher's 3x3 geometry, cached verdicts,
proof numbers, or a claimed WIN/LOSS label. Every opponent response is
recomputed with a 4x4 integer Bareiss determinant. A separate check proves
the WIN6 is one of the 46 witnesses in the repaired 1,980-S7 plan.
"""
import argparse
import hashlib
import json
from functools import lru_cache
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_KEY = "00000000000000203808200000000000"
ROOT = int(ROOT_KEY, 16)
DERIVED_ROOT_KEY = "0000000000000020380c000000000000"
DERIVED_ROOT = int(DERIVED_ROOT_KEY, 16)
BOARD = (1 << 121) - 1
CERT = HERE / "shared58_s6_win_strategy.cert"
EXPECTED_SHA256 = "10e816538fbe6cc0062e2d0dd0fe96930ef294101812701305e1595b531b21da"


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def points(mask):
    out = []
    while mask:
        bit = mask & -mask
        out.append(bit.bit_length() - 1)
        mask ^= bit
    return out


def det4(a, b, c, d):
    rows = []
    for p in (a, b, c, d):
        x, y = p % 11, p // 11
        rows.append([x*x + y*y, x, y, 1])
    sign, previous = 1, 1
    for k in range(3):
        if rows[k][k] == 0:
            pivot_row = next((i for i in range(k+1, 4) if rows[i][k]), None)
            if pivot_row is None:
                return 0
            rows[k], rows[pivot_row] = rows[pivot_row], rows[k]
            sign = -sign
        pivot = rows[k][k]
        for i in range(k+1, 4):
            for j in range(k+1, 4):
                numerator = rows[i][j]*pivot - rows[i][k]*rows[k][j]
                need(numerator % previous == 0, "nonintegral Bareiss step")
                rows[i][j] = numerator // previous
            rows[i][k] = 0
        previous = pivot
    return sign * rows[3][3]


@lru_cache(maxsize=None)
def blocked_by_triple(a, b, c):
    return sum(1 << p for p in range(121) if det4(a, b, c, p) == 0)


def legal(mask):
    blocked = mask
    for triple in combinations(points(mask), 3):
        blocked |= blocked_by_triple(*triple)
    return BOARD & ~blocked


def parse_certificate(text):
    lines = text.splitlines()
    need(lines[:3] == [
        "# n11-original-first-WIN-strategy-v1",
        "BOARD 11", "ROOT " + ROOT_KEY], "certificate header changed")
    strategy = {}
    previous = -1
    for row in lines[3:]:
        parts = row.split(" ")
        need(len(parts) == 2, "malformed strategy row")
        key, move = parts
        need(len(key) == 32 and all(c in "0123456789abcdef" for c in key)
             and move.isascii() and move.isdecimal(), "bad key/move")
        mask, p = int(key, 16), int(move)
        need(previous < mask <= BOARD and mask.bit_count() % 2 == 0
             and 0 <= p < 121, "unsorted, duplicate, or off-turn strategy")
        previous = mask
        strategy[mask] = p
    return strategy


def replay(strategy, root=ROOT, first_move=70):
    need(root.bit_count() == 6 and all(det4(*quad) != 0
         for quad in combinations(points(root), 4)), "unsafe six-stone root")
    need(strategy.get(root) == first_move, "root strategy move changed")
    need(len(strategy) == 10881, "unexpected strategy row count")
    need(legal(root) & (1 << first_move), "root move illegal")
    visited, terminals, layers = set(), [], {}

    def visit(mask):
        if mask in visited:
            return
        visited.add(mask)
        n = mask.bit_count()
        layers[n] = layers.get(n, 0) + 1
        moves = legal(mask)
        if moves == 0:
            need(n % 2 == 1, "losing even-stone terminal")
            terminals.append(n)
        elif n % 2 == 0:
            need(mask in strategy, "missing first-player strategy")
            p = strategy[mask]
            need(moves & (1 << p), "illegal first-player strategy move")
            visit(mask | (1 << p))
        else:
            while moves:
                bit = moves & -moves
                visit(mask | bit)
                moves ^= bit

    visit(root)
    need(set(strategy) <= visited, "unreachable/unused strategy rows")
    need((len(visited), len(terminals), min(terminals), max(terminals))
         == (16980, 2237, 13, 17), "terminal DAG counts changed")
    return {"strategy_nodes": len(strategy), "visited_states": len(visited),
            "terminal_leaves": len(terminals), "terminal_min": min(terminals),
            "terminal_max": max(terminals), "layers": layers}


def selected_in_repaired_plan():
    source = json.loads((HERE / "conditional_s6_cover_46_exclude_certified_win6.json").read_text())
    need(source["schema"] == "n11-central49-conditional46-repaired-exclude-certified-win6-v1",
         "unexpected repaired plan source")
    selected = set(source["selected_s6_classes"])
    need(len(selected) == 46, "bad initial cover")
    swaps = (HERE / "conditional_s6_cover_46_repaired_1980_swaps.txt").read_text().splitlines()
    need(len(swaps) == 23 and len(swaps[5:]) == 18, "bad repaired swap count")
    for line in swaps[5:]:
        remove1, remove2, add1, add2, _, _ = line.split()
        need(remove1 != remove2 and remove1 in selected and remove2 in selected
             and add1 != add2 and add1 not in selected and add2 not in selected,
             "invalid repaired witness swap")
        selected.remove(remove1)
        selected.remove(remove2)
        selected.update([add1, add2])
    need(len(selected) == 46 and ROOT_KEY in selected
         and DERIVED_ROOT_KEY in selected,
         "certified WIN6 roots not both present in repaired 46-witness plan")
    return True


def rotate180(mask):
    return sum(1 << (120-p) for p in points(mask))


def lifted_strategy(base):
    # The first S7 after base move 70 rotates to the S7 after move 75
    # from a different repaired-cover S6. All subsequent replies rotate too.
    need(rotate180(ROOT | (1 << 70)) == DERIVED_ROOT | (1 << 75),
         "claimed shared seven-stone child is not a 180-degree image")
    result = {DERIVED_ROOT: 75}
    for mask, move in base.items():
        if mask == ROOT:
            continue
        rotated = rotate180(mask)
        need(rotated not in result, "colliding rotated strategy states")
        result[rotated] = 120-move
    need(len(result) == 10881, "lifted strategy size mismatch")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=CERT)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256,
         "certificate SHA256 differs from the independently checked witness")
    text = raw.decode("utf-8")
    base = parse_certificate(text)
    result = replay(base)
    derived = lifted_strategy(base)
    result["derived_s6"] = DERIVED_ROOT_KEY
    result["derived_root_move"] = 75
    result["derived_proof"] = replay(derived, DERIVED_ROOT, 75)
    result["in_repaired_46_s6"] = selected_in_repaired_plan()
    result["certified_repaired_s6_win_count"] = 2
    result["s6_original_first_outcome"] = "WIN"
    result["repaired_1980_s7_loss_cover_status"] = "REFUTED"
    result["two_stone_root_outcome"] = "UNKNOWN"
    result["empty_board_outcome"] = "UNKNOWN"
    if args.negative:
        for changed in (
            text.replace(ROOT_KEY + " 70", ROOT_KEY + " 69", 1),
            text.replace("BOARD 11", "BOARD 10", 1),
            "\n".join(text.splitlines()[:-1]) + "\n",
        ):
            try:
                replay(parse_certificate(changed))
            except ValueError:
                continue
            raise AssertionError("tampered strategy accepted")
        forged = dict(derived)
        forged[DERIVED_ROOT] = 74
        try:
            replay(forged, DERIVED_ROOT, 75)
        except ValueError:
            pass
        else:
            raise AssertionError("tampered lifted strategy accepted")
        result["negative_tests"] = 4
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
