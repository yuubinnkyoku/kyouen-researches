"""Cone + frame double-counting recomputation for the large boards.

The cone of a safe t-set F is the set of all safe sets containing F.  If the
automorphism group of the board acts transitively on t-subsets, then

    N_m(g) = N_t * T_m(g) / C(m,t)

where T_m(g) counts cone positions of size m and Grundy g and N_m(g) is the
global count.  For s=3 projective boards the safe 3-subsets split into two
orbits (non-collinear triples and collinear triples), and the two cones are
combined.  Maximal positions (terminal, G=0) are double counted identically.

Results are written to out/cone_<key>.json.
"""
import json
import math
import sys
import time
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kyouen_lib as K

ROOT = HERE.parent.parent  # research/experiments
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


def line_through_map(n, blocks):
    owner = {}
    for B in blocks:
        for a, b in combinations(B, 2):
            owner[(a, b) if a < b else (b, a)] = B
    return owner


def find_triangle(n, blocks, owner):
    for a, b, c in combinations(range(n), 3):
        B = owner[(a, b)]
        if c not in B:
            return (a, b, c)
    raise RuntimeError("no triangle")


def count_collinear_triples(blocks):
    return sum(math.comb(len(B), 3) for B in blocks)


def orbit_structures(n, blocks, t):
    """Count t-subset orbits relevant for the s=3 PG boards (t=3) or the
    full t-subset orbit (design boards, t = 3 or 5 with lambda_t = 1)."""
    total = math.comb(n, t)
    if t == 3:
        col = count_collinear_triples(blocks)
        # all collinear triples are distinct?  pairs determine a line, so a
        # 3-subset cannot be in two blocks unless the blocks agree on the pair.
        return {"triangles": total - col, "collinear": col}
    return {"all": total}


def design_lambda_check(n, blocks, t):
    """Verify that every t-subset is in exactly one block (lambda_t = 1)."""
    seen = set()
    dup = 0
    for B in blocks:
        for T in combinations(B, t):
            if T in seen:
                dup += 1
            else:
                seen.add(T)
    return {"covered": len(seen), "expected": math.comb(n, t),
            "duplicates": dup, "lambda_t_1": len(seen) == math.comb(n, t)
            and dup == 0}


def do_cone(key, board_path, s, F, t, Nt, note="", second=None,
            second_Nt=None):
    n, blocks = K.load_board(board_path)
    val = K.validate_board(n, blocks)
    t0 = time.time()
    cone = K.cone_distribution(n, blocks, s, F)
    print(f"  cone F={F} size={cone['cone_size']} "
          f"maximal={cone['maximal_by_size']} {time.time()-t0:.1f}s", flush=True)
    cones = [cone]
    Nts = [Nt]
    if second is not None:
        t0 = time.time()
        cone2 = K.cone_distribution(n, blocks, s, second)
        print(f"  cone F={second} size={cone2['cone_size']} "
              f"maximal={cone2['maximal_by_size']} {time.time()-t0:.1f}s",
              flush=True)
        cones.append(cone2)
        Nts.append(second_Nt)

    # distinguish single-orbit vs two-orbit calls
    if len(cones) == 1:
        inflated, issues = K.inflate(cones[0]["T_g"], Nt, t)
        max_inflated, max_issues = K.inflate_counts(cones[0]["T_max"], Nt, t)
    else:
        inflated, issues = K.inflate_multi(
            [c["T_g"] for c in cones], Nts, t)
        max_inflated, max_issues = K.inflate_counts_multi(
            [c["T_max"] for c in cones], Nts, t)
    by_size, by_g = K.collapse(inflated)
    max_by_size = {int(m): int(v) for m, v in max_inflated.items() if v}
    res = {
        "key": key,
        "board_file": str(board_path).replace("\\", "/"),
        "n": n,
        "b": len(blocks),
        "s": s,
        "t": t,
        "note": note,
        "validation": val,
        "cones": cones,
        "orbit_Nt": Nts,
        "inflated_N_by_size": by_size,
        "inflated_N_by_grundy": by_g,
        "inflated_maximal_by_size": dict(sorted(max_by_size.items())),
        "inflate_issues": issues,
        "max_inflate_issues": max_issues,
        "max_grundy": K.max_grundy(inflated),
        "seconds": round(time.time() - t0, 2),
    }
    (OUT / f"cone_{key}.json").write_text(json.dumps(res, indent=1),
                                          encoding="utf-8")
    print(f"  inflated sizes={list(by_size)} maximal={max_by_size} "
          f"maxG={res['max_grundy']}", flush=True)
    return res


# --------------------------------------------------------------------- tasks

def main():
    which = sys.argv[1:] or ["all"]

    def run(name):
        return "all" in which or name in which

    if run("PG2q9_s2"):
        print("=== PG(2,9) s=2", flush=True)
        bp = ROOT / "pg2q9-cap-game-20261125/output/board_pg2q9.txt"
        n, blocks = K.load_board(bp)
        val = K.validate_board(n, blocks)
        print("  board", K.validate_board(n, blocks), flush=True)
        owner = line_through_map(n, blocks)
        F = find_triangle(n, blocks, owner)
        col = count_collinear_triples(blocks)
        Nt = math.comb(n, 3) - col
        print("  triangle", F, "N3 =", Nt, flush=True)
        do_cone("PG2q9_s2", bp, 2, F, 3, Nt,
                note="triangle orbit; PGL(3,9) transitive on triangles")

    if run("AG2q9_s2"):
        print("=== AG(2,9) s=2", flush=True)
        bp = ROOT / "ag2q9-cap-game-20261128/output/board_ag2q9.txt"
        n, blocks = K.load_board(bp)
        print("  board", K.validate_board(n, blocks), flush=True)
        F = (0, 9, 1)  # matches cone_ag2q9.py
        col = count_collinear_triples(blocks)
        Nt = math.comb(n, 3) - col
        print("  F", F, "N3 =", Nt, flush=True)
        do_cone("AG2q9_s2", bp, 2, F, 3, Nt,
                note="triangle orbit; AGL(2,9) transitive on triangles")

    if run("AG2q7_s2"):
        print("=== AG(2,7) s=2", flush=True)
        bp = ROOT / "s-parameter-kyouen-20261125/output/board_ag2q7.txt"
        n, blocks = K.load_board(bp)
        print("  board", K.validate_board(n, blocks), flush=True)
        owner = line_through_map(n, blocks)
        F = find_triangle(n, blocks, owner)
        col = count_collinear_triples(blocks)
        Nt = math.comb(n, 3) - col
        print("  triangle", F, "N3 =", Nt, flush=True)
        do_cone("AG2q7_s2", bp, 2, F, 3, Nt,
                note="triangle orbit; AGL(2,7) transitive on triangles")

    if run("PG2q5_s3"):
        print("=== PG(2,5) s=3", flush=True)
        bp = ROOT / "projective-blocking-kyouen-20261125/output/board_pg2q5.txt"
        n, blocks = K.load_board(bp)
        print("  board", K.validate_board(n, blocks), flush=True)
        owner = line_through_map(n, blocks)
        Ft = find_triangle(n, blocks, owner)
        Fc = blocks[0][:3]
        col = count_collinear_triples(blocks)
        Ntri = math.comb(n, 3) - col
        do_cone("PG2q5_s3", bp, 3, Ft, 3, Ntri,
                note="two 3-subset orbits: triangle and collinear",
                second=Fc, second_Nt=col)
        # second orbit count: collinear triples = sum C(|B|,3) = 620
        res = json.loads((OUT / "cone_PG2q5_s3.json").read_text())
        res["orbit_Nt"] = [Ntri, col]
        (OUT / "cone_PG2q5_s3.json").write_text(json.dumps(res, indent=1))

    if run("PG2q3_s3"):
        print("=== PG(2,3) s=3 (cross-check)", flush=True)
        bp = ROOT / "projective-blocking-kyouen-20261125/output/board_pg2q3.txt"
        n, blocks = K.load_board(bp)
        owner = line_through_map(n, blocks)
        Ft = find_triangle(n, blocks, owner)
        Fc = blocks[0][:3]
        col = count_collinear_triples(blocks)
        Ntri = math.comb(n, 3) - col
        do_cone("PG2q3_s3", bp, 3, Ft, 3, Ntri,
                note="two 3-subset orbits: triangle and collinear",
                second=Fc, second_Nt=col)
        res = json.loads((OUT / "cone_PG2q3_s3.json").read_text())
        res["orbit_Nt"] = [Ntri, col]
        (OUT / "cone_PG2q3_s3.json").write_text(json.dumps(res, indent=1))

    if run("PG2q4_s3"):
        print("=== PG(2,4) s=3 (cross-check)", flush=True)
        bp = ROOT / "projective-blocking-kyouen-20261125/output/board_pg2q4.txt"
        n, blocks = K.load_board(bp)
        owner = line_through_map(n, blocks)
        Ft = find_triangle(n, blocks, owner)
        Fc = blocks[0][:3]
        col = count_collinear_triples(blocks)
        Ntri = math.comb(n, 3) - col
        do_cone("PG2q4_s3", bp, 3, Ft, 3, Ntri,
                note="two 3-subset orbits: triangle and collinear",
                second=Fc, second_Nt=col)
        res = json.loads((OUT / "cone_PG2q4_s3.json").read_text())
        res["orbit_Nt"] = [Ntri, col]
        (OUT / "cone_PG2q4_s3.json").write_text(json.dumps(res, indent=1))

    if run("W22_s5"):
        print("=== W_22 s=5", flush=True)
        bp = ROOT / "design-kyouen-witt-20261125/output/board_w22.txt"
        n, blocks = K.load_board(bp)
        print("  board", K.validate_board(n, blocks), flush=True)
        print("  3-(22,6,1) check", design_lambda_check(n, blocks, 3),
              flush=True)
        F = (0, 1, 2)
        Nt = math.comb(n, 3)
        do_cone("W22_s5", bp, 5, F, 3, Nt,
                note="all triples one orbit (M_22 3-transitive); lambda_3=1")

    for s in (5, 6, 7):
        key = f"W24_s{s}"
        if run(key):
            print(f"=== W_24 s={s}", flush=True)
            bp = ROOT / "design-kyouen-witt-20261125/output/board_w24.txt"
            n, blocks = K.load_board(bp)
            if s == 5:
                print("  board", K.validate_board(n, blocks), flush=True)
                print("  5-(24,8,1) check",
                      design_lambda_check(n, blocks, 5), flush=True)
            F = (0, 1, 2, 3, 4)
            Nt = math.comb(n, 5)
            do_cone(key, bp, s, F, 5, Nt,
                    note="all 5-subsets one orbit (M_24 5-transitive); lambda_5=1")


if __name__ == "__main__":
    main()
