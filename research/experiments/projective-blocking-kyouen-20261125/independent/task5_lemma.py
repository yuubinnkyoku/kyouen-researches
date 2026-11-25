"""Task 5: audit the parity-graded Grundy lemma.

  A. Apply the lemma to every board on which it is claimed to apply:
       * PG(2,2), PG(2,3), PG(2,4)   (all maximal safe sets odd),
       * the seven design boards AG(3,2), AG(4,2), W_11, W_12, W_22, W_23, W_24
         (all maximal safe sets of one common size K).
     For each board we recompute every Grundy value and compare with the
     experiment's own grundy_*.txt / summary.json data, and we check the formula
     Grundy(S) = (p - |S|) mod 2 on every safe set.

  B. Counterexample search on small artificial hypergraphs (4-8 points, blocks
     of size 3-5): exhaustive for n=4,5 (all block sets of sizes 3 and 4) and
     n=6 (all 4-uniform block sets), plus random boards for n=6,7,8.  For every
     board whose maximal safe sets have a uniform size parity we check
     (i) every Grundy value satisfies (p - |S|) mod 2,
     (ii) no Grundy value is >= 2.
     Note: blocks of size 3 can never violate "<= 3 points per block", so only
     blocks of size >= 4 constrain the game; the search therefore focuses on
     4- and 5-blocks (we still include 3-blocks in the n=4,5 exhaustive runs to
     be literal about the requested setup).

Conventions: report convention for misere is 1 = first player wins, 0 = loses
(the same convention as the ROOT lines in the experiment's engine output).
"""

from __future__ import annotations

import itertools
import json
import os
import random
import time

from common import Board, grundy_and_misere, read_board, size_histogram

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
BASE = os.path.dirname(HERE)
DESIGN = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                      "design-kyouen-witt-20261125", "output")

PG_BOARDS = {
    "PG(2,2)": "board_pg2q2.txt",
    "PG(2,3)": "board_pg2q3.txt",
    "PG(2,4)": "board_pg2q4.txt",
}
DESIGN_BOARDS = {
    "AG(3,2)": "board_ag32.txt",
    "AG(4,2)": "board_ag42.txt",
    "W_11": "board_w11.txt",
    "W_12": "board_w12.txt",
    "W_22": "board_w22.txt",
    "W_23": "board_w23.txt",
    "W_24": "board_w24.txt",
}
DESIGN_GRUNDY = {
    "AG(3,2)": "grundy_ag32.txt",
    "AG(4,2)": "grundy_ag42.txt",
    "W_11": "grundy_w11.txt",
    "W_12": "grundy_w12.txt",
    "W_22": "grundy_w22.txt",
    "W_23": "grundy_w23.txt",
    "W_24": "grundy_w24.txt",
}


def parse_grundy_txt(path):
    out = {"size": {}, "grundy": {}}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "SAFE":
                out["safe"] = int(parts[1])
            elif parts[0] == "ROOT":
                out["root"] = (int(parts[1]), int(parts[2]))
            elif parts[0] == "SIZE":
                out["size"][int(parts[1])] = (
                    int(parts[2]), int(parts[3]), int(parts[4]))
            elif parts[0] == "GRUNDY":
                out["grundy"][int(parts[1])] = int(parts[2])
    return out


def audit_board(name, path, cap=3):
    n, blocks = read_board(path)
    board = Board(n, blocks, cap=cap)
    sizes, by_size, maximal = board.enumerate_safe(collect=True)
    grundy, win = grundy_and_misere(board, by_size)

    maximal_hist = size_histogram(maximal)
    parities = {k % 2 for k in maximal_hist}
    uniform = len(parities) == 1
    p = next(iter(parities)) if uniform else None
    dist = {}
    for g in grundy.values():
        dist[g] = dist.get(g, 0) + 1
    dist = dict(sorted(dist.items()))
    formula_mismatches = 0
    if uniform:
        for mask, g in grundy.items():
            if g != (p - mask.bit_count()) % 2:
                formula_mismatches += 1
    return {
        "name": name,
        "n": n,
        "blocks": len(board.block_masks),
        "safe": sum(sizes),
        "safe_by_size": {int(k): int(v) for k, v in enumerate(sizes) if v},
        "maximal_by_size": maximal_hist,
        "uniform_maximal_parity": uniform,
        "p": p,
        "grundy_distribution": {int(k): int(v) for k, v in dist.items()},
        "max_grundy": max(dist),
        "root_grundy": grundy[0],
        "root_misere_first_player_wins": 1 if win[0] else 0,
        "formula_mismatches": formula_mismatches,
        "formula_holds": uniform and formula_mismatches == 0,
        "grundy_in_0_1": set(dist) <= {0, 1},
    }


def part_a():
    print("=" * 78)
    print("A. Lemma applications on the claimed boards")
    print("=" * 78)
    with open(os.path.join(DESIGN, "summary.json"), "r", encoding="utf-8") as fh:
        design_summary = {d["name"]: d for d in json.load(fh)["designs"]}

    rows = []
    for name, fname in PG_BOARDS.items():
        res = audit_board(name, os.path.join(BASE, "output", fname))
        res["category"] = "PG"
        q = int(name[-2])
        eng = parse_grundy_txt(os.path.join(BASE, "output", f"grundy_pg2q{q}.txt"))
        res["engine_checks"] = {
            "safe": eng.get("safe") == res["safe"],
            "root": eng.get("root") == (
                res["root_grundy"], res["root_misere_first_player_wins"]),
            "grundy_distribution": eng.get("grundy") == res["grundy_distribution"],
        }
        res["engine_ok"] = all(res["engine_checks"].values())
        rows.append(res)

    for name, fname in DESIGN_BOARDS.items():
        res = audit_board(name, os.path.join(DESIGN, fname))
        res["category"] = "design"
        eng = parse_grundy_txt(os.path.join(DESIGN, DESIGN_GRUNDY[name]))
        ref = design_summary[name]
        eng_checks = {
            "safe": eng.get("safe") == res["safe"],
            "root": eng.get("root") == (
                res["root_grundy"], res["root_misere_first_player_wins"]),
            "grundy_distribution": eng.get("grundy") == res["grundy_distribution"],
            "summary_safe": ref["safe"] == res["safe"],
            "summary_root_grundy": ref["root_grundy"] == res["root_grundy"],
            "summary_root_misere": ref["root_misere"] ==
            res["root_misere_first_player_wins"],
            "summary_grundy_distribution":
            {int(k): int(v) for k, v in ref["grundy_distribution"].items()} ==
            res["grundy_distribution"],
            "summary_maximal_counts":
            {int(k): v["maximal"] for k, v in ref["size_counts"].items()
             if v["maximal"]} == res["maximal_by_size"],
        }
        res["engine_checks"] = eng_checks
        res["engine_ok"] = all(eng_checks.values())
        rows.append(res)

    for res in rows:
        print(f"{res['name']:<9} n={res['n']:>2} safe={res['safe']:>6} "
              f"maximal={res['maximal_by_size']} "
              f"uniform_parity={res['uniform_maximal_parity']} "
              f"p={res['p']} maxG={res['max_grundy']} "
              f"root={res['root_grundy']}/{res['root_misere_first_player_wins']} "
              f"formula={'OK' if res['formula_holds'] else 'FAIL'} "
              f"engine={'OK' if res['engine_ok'] else 'FAIL'}")
        if res["formula_mismatches"]:
            print(f"    formula mismatches: {res['formula_mismatches']}")
        if not res["engine_ok"]:
            print(f"    engine checks: {res['engine_checks']}")

    all_ok = all(
        res["uniform_maximal_parity"] and res["formula_holds"]
        and res["grundy_in_0_1"] and res["engine_ok"]
        for res in rows
    )
    print(f"\nA result: {'PASS' if all_ok else 'FAIL'}")
    return {"rows": rows, "ok": all_ok}


# ---------------------------------------------------------------------------
# B. small artificial hypergraphs
# ---------------------------------------------------------------------------

def build_unsafe(n, blocks, cap=3):
    """Bitmask table: unsafe[mask] = 1 iff some block has > cap points in mask."""
    full = (1 << n) - 1
    unsafe = bytearray(1 << n)
    for blk in blocks:
        if len(blk) <= cap:
            continue
        for sub in itertools.combinations(blk, cap + 1):
            sub_mask = 0
            for p in sub:
                sub_mask |= 1 << p
            rest = full ^ sub_mask
            s = rest
            while True:
                unsafe[sub_mask | s] = 1
                if s == 0:
                    break
                s = (s - 1) & rest
    return unsafe


def analyse_small(n, blocks, masks_by_size, cap=3):
    """Exhaustive game analysis of a hypergraph on <= 8 points."""
    full = (1 << n) - 1
    unsafe = build_unsafe(n, blocks, cap)
    grundy = [0] * (1 << n)
    for k in range(n, -1, -1):
        for mask in masks_by_size[k]:
            if unsafe[mask]:
                continue
            child_values = 0
            rest = full ^ mask
            while rest:
                low = rest & -rest
                rest ^= low
                child = mask | low
                if not unsafe[child]:
                    child_values |= 1 << grundy[child]
            g = 0
            while (child_values >> g) & 1:
                g += 1
            grundy[mask] = g
    maximal_sizes = {}
    max_grundy = 0
    for mask in range(1 << n):
        if unsafe[mask]:
            continue
        g = grundy[mask]
        if g > max_grundy:
            max_grundy = g
        rest = full ^ mask
        extendable = False
        while rest:
            low = rest & -rest
            rest ^= low
            if not unsafe[mask | low]:
                extendable = True
                break
        if not extendable:
            k = mask.bit_count()
            maximal_sizes[k] = maximal_sizes.get(k, 0) + 1
    return unsafe, grundy, maximal_sizes, max_grundy


def check_board_uniform(n, blocks, masks_by_size):
    unsafe, grundy, maximal_sizes, max_grundy = analyse_small(
        n, blocks, masks_by_size)
    parities = {k % 2 for k in maximal_sizes}
    if len(parities) != 1:
        return False, None, 0, max_grundy, maximal_sizes
    p = next(iter(parities))
    mismatches = 0
    for mask in range(1 << n):
        if unsafe[mask]:
            continue
        if grundy[mask] != (p - mask.bit_count()) % 2:
            mismatches += 1
    return True, p, mismatches, max_grundy, maximal_sizes


def part_b():
    print()
    print("=" * 78)
    print("B. Counterexample search on small artificial hypergraphs")
    print("=" * 78)
    results = {}

    def summarise(label, stats):
        print(f"  {label}:")
        print(f"    boards={stats['boards']} uniform-parity={stats['uniform']} "
              f"uniform_with_G>=2={stats['uniform_ge2']} "
              f"formula_mismatches={stats['formula_mismatches']} "
              f"mixed_with_G>=2={stats['mixed_ge2']} "
              f"[{stats['seconds']:.1f} s]")
        results[label] = stats

    def new_stats():
        return {"boards": 0, "uniform": 0, "uniform_ge2": 0,
                "formula_mismatches": 0, "mixed_ge2": 0, "examples": []}

    # -- exhaustive n = 4 and n = 5, all block sets with blocks of size 3 and 4
    for n in (4, 5):
        masks_by_size = [[m for m in range(1 << n) if m.bit_count() == k]
                         for k in range(n + 1)]
        block_pool = [frozenset(c) for size in (3, 4)
                      for c in itertools.combinations(range(n), size)]
        stats = new_stats()
        t0 = time.time()
        for r in range(len(block_pool) + 1):
            for chosen in itertools.combinations(range(len(block_pool)), r):
                blocks = [tuple(block_pool[i]) for i in chosen]
                stats["boards"] += 1
                uniform, p, mism, maxg, maxsizes = check_board_uniform(
                    n, blocks, masks_by_size)
                if uniform:
                    stats["uniform"] += 1
                    if mism:
                        stats["formula_mismatches"] += 1
                    if maxg >= 2:
                        stats["uniform_ge2"] += 1
                        if len(stats["examples"]) < 3:
                            stats["examples"].append(
                                {"blocks": [sorted(b) for b in blocks],
                                 "maximal_sizes": maxsizes,
                                 "max_grundy": maxg})
                elif maxg >= 2:
                    stats["mixed_ge2"] += 1
        stats["seconds"] = time.time() - t0
        summarise(f"exhaustive n={n}, blocks of size 3-4", stats)

    # -- exhaustive n = 6 over all sets of 4-blocks
    n = 6
    masks_by_size = [[m for m in range(1 << n) if m.bit_count() == k]
                     for k in range(n + 1)]
    four_blocks = [frozenset(c) for c in itertools.combinations(range(n), 4)]
    stats = new_stats()
    t0 = time.time()
    for r in range(len(four_blocks) + 1):
        for chosen in itertools.combinations(range(len(four_blocks)), r):
            blocks = [tuple(four_blocks[i]) for i in chosen]
            stats["boards"] += 1
            uniform, p, mism, maxg, maxsizes = check_board_uniform(
                n, blocks, masks_by_size)
            if uniform:
                stats["uniform"] += 1
                if mism:
                    stats["formula_mismatches"] += 1
                if maxg >= 2:
                    stats["uniform_ge2"] += 1
                    if len(stats["examples"]) < 3:
                        stats["examples"].append(
                            {"blocks": [sorted(b) for b in blocks],
                             "maximal_sizes": maxsizes,
                             "max_grundy": maxg})
            elif maxg >= 2:
                stats["mixed_ge2"] += 1
    stats["seconds"] = time.time() - t0
    summarise("exhaustive n=6, all 4-uniform block sets", stats)

    # -- random boards n = 6, 7, 8 with blocks of size 3-5
    rng = random.Random(20261125)
    for n in (6, 7, 8):
        masks_by_size = [[m for m in range(1 << n) if m.bit_count() == k]
                         for k in range(n + 1)]
        stats = new_stats()
        t0 = time.time()
        for _trial in range(400):
            nblocks = rng.randint(1, 8)
            blocks = [tuple(sorted(rng.sample(range(n), rng.choice((3, 4, 5)))))
                      for _ in range(nblocks)]
            stats["boards"] += 1
            uniform, p, mism, maxg, maxsizes = check_board_uniform(
                n, blocks, masks_by_size)
            if uniform:
                stats["uniform"] += 1
                if mism:
                    stats["formula_mismatches"] += 1
                if maxg >= 2:
                    stats["uniform_ge2"] += 1
                    if len(stats["examples"]) < 3:
                        stats["examples"].append(
                            {"blocks": [list(b) for b in blocks],
                             "maximal_sizes": maxsizes,
                             "max_grundy": maxg})
            elif maxg >= 2:
                stats["mixed_ge2"] += 1
        stats["seconds"] = time.time() - t0
        summarise(f"random n={n}, 400 boards, blocks of size 3-5", stats)

    total_boards = sum(s["boards"] for s in results.values())
    total_uniform = sum(s["uniform"] for s in results.values())
    counterexamples = sum(s["uniform_ge2"] for s in results.values())
    mismatches = sum(s["formula_mismatches"] for s in results.values())
    print(f"\n  total boards tested: {total_boards}")
    print(f"  boards with uniform maximal-size parity: {total_uniform}")
    print(f"  uniform-parity boards with a Grundy value >= 2: {counterexamples}")
    print(f"  uniform-parity boards violating the formula: {mismatches}")
    verdict = counterexamples == 0 and mismatches == 0
    print(f"  B result: {'PASS (no counterexample)' if verdict else 'FAIL'}")
    return {"stats": results, "total_boards": total_boards,
            "total_uniform": total_uniform,
            "counterexamples": counterexamples,
            "formula_mismatches": mismatches,
            "ok": verdict}


def main():
    os.makedirs(OUT, exist_ok=True)
    a = part_a()
    b = part_b()
    out = {"part_a": a, "part_b": b, "ok": a["ok"] and b["ok"]}
    with open(os.path.join(OUT, "task5_lemma.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print("\nTASK 5:", "PASS" if out["ok"] else "FAIL")


if __name__ == "__main__":
    main()
