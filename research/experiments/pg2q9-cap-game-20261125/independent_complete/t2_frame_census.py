"""Task 1/2: census via a fixed frame, and full Grundy distribution on the cone."""

from __future__ import annotations

import json
import math
import time

import game
import pg


def main():
    t0 = time.time()
    n, b, blocks = pg.load_board()
    g = game.CapGame(n, blocks)
    frame = (0, 1, 10, 20)
    fc = game.frame_census(g, frame)
    T = fc["T"]
    maximal = fc["maximal"]
    gd = fc["grundy_dist"]
    print("T:", T)
    print("maximal through frame:", maximal)
    print("grundy dist through frame:", {k: dict(v) for k, v in gd.items()})

    # N4 = number of 4-caps: brute force over all 4-subsets.
    t1 = time.time()
    n4 = 0
    for S in __import__("itertools").combinations(range(n), 4):
        m = (1 << S[0]) | (1 << S[1]) | (1 << S[2]) | (1 << S[3])
        if g.is_cap(m):
            n4 += 1
    print("N4 brute force:", n4, "seconds:", round(time.time() - t1, 2))
    assert n4 == 1769040, n4

    # closed forms for low sizes
    n0, n1, n2 = 1, n, n * (n - 1) // 2
    n3 = math.comb(n, 3) - b * math.comb(10, 3)
    print("n0..n3:", n0, n1, n2, n3)
    assert (n0, n1, n2, n3) == (1, 91, 4095, 110565)

    # derive all N_k and maximal counts
    derived_N = {0: n0, 1: n1, 2: n2, 3: n3, 4: n4}
    derived_max = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for k in range(5, 11):
        derived_N[k] = game.double_count(T[k], n4, k)
        derived_max[k] = game.double_count(maximal[k], n4, k)
    print("derived N:", derived_N)
    print("derived maximal:", derived_max)

    # global Grundy distribution for k >= 4 by double counting
    global_g = {}
    for k in range(4, 11):
        global_g[k] = {}
        for val, cnt in gd[k].items():
            global_g[k][val] = game.double_count(cnt, n4, k)
    print("global G distribution:", global_g)
    assert sum(global_g[6].values()) == derived_N[6]
    assert sum(global_g[7].values()) == derived_N[7]

    out = {
        "frame": list(frame),
        "T": {str(k): v for k, v in sorted(T.items())},
        "maximal_through_frame": {str(k): v for k, v in sorted(maximal.items())},
        "grundy_through_frame": {
            str(k): {str(gv): c for gv, c in sorted(gd[k].items())}
            for k in sorted(gd)
        },
        "N4_bruteforce": n4,
        "derived_N": {str(k): v for k, v in sorted(derived_N.items())},
        "derived_maximal": {str(k): v for k, v in sorted(derived_max.items())},
        "global_grundy": {
            str(k): {str(gv): c for gv, c in sorted(global_g[k].items())}
            for k in sorted(global_g)
        },
        "seconds": round(time.time() - t0, 3),
    }
    (pg.HERE / "out").mkdir(exist_ok=True)
    (pg.HERE / "out" / "t2_frame_census.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )
    print("seconds:", out["seconds"])


if __name__ == "__main__":
    main()
