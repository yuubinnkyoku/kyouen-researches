#!/usr/bin/env python3
"""Independent verification of three exact K_s(q) values.

Experiment directory: research/experiments/inversive-spectrum-20261124/
Cases: (q=4,s=4), (q=5,s=5), (q=7,s=4).

This script does NOT import or reuse
research/experiments/inversive-spectrum-20261124/scripts/spectrum_sat.py or
research/experiments/inversive-spectrum-20261124/scripts/brute_force.py.
It uses only the Python standard library for the
combinatorial work, plus two small C programs written from scratch
(exhaust.c, q7_bb.c) for the exhaustive / branch-and-bound searches.

Outputs: exact values, witnesses, node counts, wall times, direct witness
verification against the JSON boards, random-set moment checks, and the
symmetry-based upper bound for q=7.
"""
from __future__ import annotations

import json
import random
import re
import shutil
import subprocess
import sys
import time
from itertools import combinations
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output"
PY = sys.executable

CASES = ((4, 4, 9), (5, 5, 16), (7, 4, 13))


# --------------------------------------------------------------------------
# board loading / structural verification
# --------------------------------------------------------------------------
class Board:
    def __init__(self, data: dict):
        self.q = int(data["q"])
        self.v = int(data["v"])
        self.b = int(data["b"])
        self.k = self.q + 1
        self.blocks = [tuple(sorted(int(p) for p in bl)) for bl in data["blocks"]]
        self.block_sets = [frozenset(bl) for bl in self.blocks]
        self.masks = [sum(1 << p for p in bl) for bl in self.blocks]
        self.point_blocks = [[] for _ in range(self.v)]
        for bi, bl in enumerate(self.blocks):
            for p in bl:
                self.point_blocks[p].append(bi)


def load_board(q: int) -> Board:
    with open(OUT / f"board_q{q}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return Board(data)


def verify_design(board: Board) -> dict:
    """Verify all design identities used by the upper-bound arguments."""
    q, v, b, k = board.q, board.v, board.b, board.k
    assert v == q * q + 1, (v, q * q + 1)
    assert b == q * (q * q + 1), (b, q * (q * q + 1))
    assert len(board.blocks) == b
    assert len(set(board.blocks)) == b, "duplicate circles"
    assert all(len(bl) == k for bl in board.blocks), "circle size"
    assert all(len(set(bl)) == k for bl in board.blocks), "repeated point in circle"
    assert all(0 <= p < v for bl in board.blocks for p in bl), "point index"
    # point degrees
    degree = [len(pb) for pb in board.point_blocks]
    assert all(d == q * (q + 1) for d in degree), ("degree", set(degree))
    # pair multiplicities: every pair on exactly q+1 circles
    pbs = [set(pb) for pb in board.point_blocks]
    pair_lambda = None
    for i, j in combinations(range(v), 2):
        m = len(pbs[i] & pbs[j])
        assert m == q + 1, ("pair lambda", i, j, m)
        pair_lambda = m
    # triple multiplicities: every triple on exactly one circle
    tri_count: dict[tuple[int, int, int], int] = {}
    for bl in board.blocks:
        for tri in combinations(bl, 3):
            tri_count[tri] = tri_count.get(tri, 0) + 1
    assert len(tri_count) == comb(v, 3), (len(tri_count), comb(v, 3))
    assert all(c == 1 for c in tri_count.values()), "triple lambda"
    return {
        "v": v,
        "b": b,
        "block_size": k,
        "degree": q * (q + 1),
        "pair_lambda": pair_lambda,
        "triples": len(tri_count),
        "triple_lambda": 1,
    }


def moment_identities(board: Board, trials: int, seed: int) -> dict:
    """Random-set check of sum C(|S cap C|,2)=C(|S|,2)(q+1) and
    sum C(|S cap C|,3)=C(|S|,3)."""
    q, v = board.q, board.v
    rng = random.Random(seed)
    max2 = max3 = 0
    bad = 0
    for _ in range(trials):
        n = rng.randrange(0, v + 1)
        S = set(rng.sample(range(v), n))
        s2 = s3 = 0
        for bl in board.blocks:
            c = len(S.intersection(bl))
            s2 += c * (c - 1) // 2
            s3 += c * (c - 1) * (c - 2) // 6
        d2 = abs(s2 - comb(n, 2) * (q + 1))
        d3 = abs(s3 - comb(n, 3))
        if d2:
            bad += 1
        if d3:
            bad += 1
        max2 = max(max2, d2)
        max3 = max(max3, d3)
    return {"trials": trials, "max_abs_diff_2": max2, "max_abs_diff_3": max3,
            "failures": bad}


# --------------------------------------------------------------------------
# witnesses / direct verification
# --------------------------------------------------------------------------
def verify_witness(board: Board, S, s: int) -> dict:
    S = list(S)
    assert len(S) == len(set(S)), "witness has repeated points"
    assert all(0 <= p < board.v for p in S), "witness point out of range"
    Sset = set(S)
    worst = 0
    bad = []
    for bi, bl in enumerate(board.blocks):
        c = len(Sset.intersection(bl))
        if c > worst:
            worst = c
        if c > s:
            bad.append((bi, c))
    return {"size": len(Sset), "worst_circle_intersection": worst,
            "ok": not bad, "bad_circles": bad[:10], "num_bad_circles": len(bad),
            "circles_checked": board.b}


def witness_string(S) -> str:
    return "[" + ", ".join(str(p) for p in S) + "]"


# --------------------------------------------------------------------------
# C helpers (from-scratch solvers)
# --------------------------------------------------------------------------
def compile_c(src: Path, exe: Path) -> None:
    gcc = shutil.which("gcc")
    if gcc is None:
        raise SystemExit("gcc not found; C solvers are required")
    r = subprocess.run([gcc, "-O2", "-o", str(exe), str(src)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gcc failed for {src}:\n{r.stderr}")


def write_board_data(board: Board, path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{board.v} {board.b} {board.k}\n")
        for bl in board.blocks:
            f.write(" ".join(str(p) for p in bl) + "\n")


def parse_kv(text: str) -> dict[str, str]:
    return dict(re.findall(r"(\w+)=([^\s]+)", text))


def run_exhaust(exe: Path, data: Path, s: int, n: int) -> dict:
    t0 = time.perf_counter()
    r = subprocess.run([str(exe), str(data), str(s), str(n)],
                       capture_output=True, text=True)
    wall = time.perf_counter() - t0
    if r.returncode != 0:
        raise RuntimeError(f"exhaust failed: {r.stderr}")
    kv = parse_kv(r.stdout)
    wit = [int(x) for x in kv.get("witness", "").split(",") if x]
    return {"count": int(kv["count"]), "nodes": int(kv["nodes"]),
            "c_seconds": float(kv["seconds"]), "wall_seconds": wall,
            "witness": wit, "raw": r.stdout.strip()}


def run_bb(exe: Path, data: Path, s: int, n: int, fixed) -> dict:
    t0 = time.perf_counter()
    r = subprocess.run([str(exe), str(data), str(s), str(n)]
                       + [str(p) for p in fixed], capture_output=True, text=True)
    wall = time.perf_counter() - t0
    kv = parse_kv(r.stdout)
    sat = kv.get("result") == "SAT"
    wit = [int(x) for x in kv.get("witness", "").split(",") if x]
    return {"sat": sat, "nodes": int(kv["nodes"]),
            "c_seconds": float(kv["seconds"]), "wall_seconds": wall,
            "witness": wit, "raw": r.stdout.strip(), "returncode": r.returncode}


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main() -> None:
    t_start = time.perf_counter()
    print("=" * 78)
    print("INDEPENDENT EXACT VERIFICATION  K_s(q)")
    print("experiment: research/experiments/inversive-spectrum-20261124")
    print("cases: (q=4,s=4), (q=5,s=5), (q=7,s=4)")
    print("=" * 78)

    exe_exhaust = HERE / "exhaust.exe"
    exe_bb = HERE / "q7_bb.exe"
    compile_c(HERE / "exhaust.c", exe_exhaust)
    compile_c(HERE / "q7_bb.c", exe_bb)
    print("compiled from scratch: exhaust.exe, q7_bb.exe (gcc -O2)")

    # symmetry / model verification needed for the q=7 upper bound
    print("\n--- q=7 board model and Mobius symmetry (supporting scripts) ---")
    for script in ("field_model.py", "verify_symmetry.py"):
        t0 = time.perf_counter()
        r = subprocess.run([PY, str(HERE / script)], capture_output=True, text=True)
        sec = time.perf_counter() - t0
        print(f"[{script}, {sec:.3f}s]")
        print(r.stdout.strip())
        if r.returncode != 0:
            raise RuntimeError(f"{script} failed:\n{r.stderr}")

    results = {"experiment": "inversive-spectrum-20261124/independent",
               "cases": [], "moments": {}, "symmetry_q7": {
                   "field_model": "alpha^2=6, label=b+7a for a+b*alpha, inf=49; "
                                  "350/350 Baer sublines equal board blocks",
                   "generators": "x->x+1, x->lambda*x, x->1/x with lambda=(1,2)",
                   "ordered_triples_reached": 117600,
                   "ordered_triples_total": 50 * 49 * 48,
                   "conclusion": "generated group is 3-transitive on the 50 points",
               }}
    total_wall = 0.0

    for q, s, published in CASES:
        board = load_board(q)
        t_case = time.perf_counter()
        print("\n" + "=" * 78)
        print(f"=== q={q}, s={s}  (published claim: {published}) ===")
        print("=" * 78)

        t0 = time.perf_counter()
        info = verify_design(board)
        t_design = time.perf_counter() - t0
        print(f"board: v={info['v']} b={info['b']} k={info['block_size']}; "
              f"degree={info['degree']}; pair_lambda={info['pair_lambda']}; "
              f"triples={info['triples']} each on {info['triple_lambda']} circle "
              f"({t_design:.3f}s)")
        assert info["v"] == q * q + 1 and info["b"] == q * (q * q + 1)

        t0 = time.perf_counter()
        mres = moment_identities(board, trials=200, seed=20261124 + q)
        t_mom = time.perf_counter() - t0
        print(f"moment identities on 200 random S: max|diff2|={mres['max_abs_diff_2']}, "
              f"max|diff3|={mres['max_abs_diff_3']}, failures={mres['failures']} "
              f"({t_mom:.3f}s)")
        assert mres["failures"] == 0
        results["moments"][f"q{q}"] = mres

        data_path = HERE / f"board_q{q}.dat"
        write_board_data(board, data_path)

        if q in (4, 5):
            # exhaustive enumeration: witness of size s-claimed value, and
            # complete count of all (published+1)-subsets.
            t0 = time.perf_counter()
            wres = run_exhaust(exe_exhaust, data_path, s, published)
            ures = run_exhaust(exe_exhaust, data_path, s, published + 1)
            phase_wall = time.perf_counter() - t0
            assert wres["count"] > 0, "no witness found"
            assert ures["count"] == 0, "counterexample of larger size found"
            witness = sorted(wres["witness"])
            vres = verify_witness(board, witness, s)
            assert vres["ok"], vres
            method = ("complete enumeration of every subset of the relevant size "
                      "(exhaust.c)")
            node_w, node_u = wres["nodes"], ures["nodes"]
            time_w, time_u = wres["c_seconds"], ures["c_seconds"]
            extra = (f"count of valid {published}-sets = {wres['count']}; "
                     f"count of valid {published+1}-sets = {ures['count']}")
            upper_detail = {"method": method,
                            "target_size": published + 1,
                            "num_valid": ures["count"],
                            "nodes": ures["nodes"],
                            "c_seconds": ures["c_seconds"],
                            "wall_seconds": ures["wall_seconds"]}
        else:
            # q=7: WLOG fixed triple by verified 3-transitive Mobius symmetry.
            fixed = (0, 7, 49)
            t0 = time.perf_counter()
            wres = run_bb(exe_bb, data_path, s, published, fixed)
            ures = run_bb(exe_bb, data_path, s, published + 1, fixed)
            ures2 = run_bb(exe_bb, data_path, s, published + 1, (0, 8, 49))
            phase_wall = time.perf_counter() - t0
            assert wres["sat"], "no witness found containing fixed triple"
            assert not ures["sat"], "14-set containing fixed triple exists!"
            assert not ures2["sat"], "second fixed triple counterexample!"
            witness = sorted(wres["witness"])
            vres = verify_witness(board, witness, s)
            assert vres["ok"], vres
            method = ("branch-and-bound over all sets containing the fixed triple "
                      "(0,7,49), which is WLOG by the verified 3-transitive Mobius "
                      "symmetry (q7_bb.c); moment-identity upper bound at every node")
            node_w, node_u = wres["nodes"], ures["nodes"]
            time_w, time_u = wres["c_seconds"], ures["c_seconds"]
            extra = (f"fixed-triple search: 13-set nodes={wres['nodes']}; "
                     f"14-set nodes={ures['nodes']}; "
                     f"second fixed triple (0,8,49): 14-set nodes={ures2['nodes']}")
            upper_detail = {"method": method,
                            "fixed_triple": list(fixed),
                            "second_fixed_triple": [0, 8, 49],
                            "target_size": published + 1,
                            "num_valid": 0,
                            "nodes": ures["nodes"],
                            "second_nodes": ures2["nodes"],
                            "c_seconds": ures["c_seconds"],
                            "second_c_seconds": ures2["c_seconds"],
                            "wall_seconds": ures["wall_seconds"] +
                                            ures2["wall_seconds"]}

        print(f"witness search: nodes={node_w} c_time={time_w:.4f}s")
        print(f"witness (size {len(witness)}): {witness_string(witness)}")
        print(f"direct verification against board JSON: every one of the "
              f"{vres['circles_checked']} circles meets it in at most {s}; "
              f"worst intersection={vres['worst_circle_intersection']} -> "
              f"{'PASS' if vres['ok'] else 'FAIL'}")
        print(f"upper bound: {method}")
        print(f"  target size {published+1}: num_valid={upper_detail['num_valid']}, "
              f"nodes={node_u}, c_time={time_u:.4f}s -> "
              f"{'UNSAT (no such set)' if upper_detail['num_valid']==0 else 'SAT'}")
        print(f"  {extra}")
        print(f"EXACT VALUE: K_{s}({q}) = {published}  "
              f"[{('CONFIRMED' if len(witness)==published else 'DISCREPANCY')}]")

        computed = len(witness)
        results["cases"].append({
            "q": q, "s": s, "published": published, "computed": computed,
            "witness": witness, "witness_size": computed,
            "witness_search": {"nodes": node_w, "c_seconds": time_w},
            "witness_direct_verification": vres,
            "upper_bound": upper_detail,
            "design": info,
            "status": "confirmed" if computed == published else "discrepancy",
        })
        total_wall += time.perf_counter() - t_case

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    diffs = []
    for row in results["cases"]:
        ok = row["computed"] == row["published"]
        if not ok:
            diffs.append(row)
        print(f"  q={row['q']:>2}  s={row['s']:>2}  published={row['published']:>2}  "
              f"independent={row['computed']:>2}  "
              f"witness_size={row['witness_size']:>2}  "
              f"{'CONFIRMED' if ok else 'DISCREPANCY'}")
    print(f"discrepancies: {len(diffs)}")
    print(f"total case wall time: {total_wall:.3f}s; "
          f"process wall time: {time.perf_counter()-t_start:.3f}s")
    if diffs:
        print("DISCREPANT CASES:", diffs)

    results["summary"] = {
        "all_confirmed": not diffs,
        "num_discrepancies": len(diffs),
        "total_case_seconds": total_wall,
        "process_seconds": time.perf_counter() - t_start,
    }
    with open(HERE / "results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
    print(f"results written to {HERE / 'results.json'}")


if __name__ == "__main__":
    main()
