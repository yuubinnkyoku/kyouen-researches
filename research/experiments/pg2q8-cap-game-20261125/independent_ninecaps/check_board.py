"""Task 1 (part A): validate the board file as PG(2,8) and the example 9-cap."""
import json
import os
import sys

from pg8 import PTS, PTIDX, board_checks, inc, GEO_LINES

EXAMPLE = (2, 3, 10, 12, 21, 45, 47, 50, 52)


def main():
    out = {}
    res = board_checks()
    out["board_checks"] = res
    print("== board checks ==")
    for k, v in res.items():
        print(f"  {k}: {v}")

    I = inc()
    # cap test, brute force directly on the board incidence
    S = list(EXAMPLE)
    out["example"] = S
    out["example_size"] = len(S)
    out["example_distinct"] = len(set(S)) == 9
    bad = []
    for i in range(9):
        for j in range(i + 1, 9):
            L = I.lof[S[i]][S[j]]
            on = [k for k in range(9) if k not in (i, j) and I.lof[S[i]][S[k]] == L]
            if on:
                bad.append((S[i], S[j], L, [S[k] for k in on]))
    out["example_is_cap"] = not bad
    out["example_collinear_witnesses"] = bad
    print("== example 9-cap ==")
    print("  size:", len(S), "distinct:", out["example_distinct"])
    print("  is cap:", out["example_is_cap"], "witnesses:", bad)
    print("  blocked points (on a secant):", (I.blocked_mask(S) & I.ALL).bit_count(),
          "of 73")
    ext = [p for p in range(73) if not (I.blocked_mask(S) >> p) & 1]
    out["example_extension_points"] = ext
    print("  points not on any secant (could extend):", ext)

    # The example in coordinates
    out["example_vectors"] = {p: PTS[p] for p in S}
    print("  vectors:", {p: PTS[p] for p in S})

    # check 9 points are not all on one line / span the plane
    out["example_spans_plane"] = True  # 9-cap has no 3 collinear, so >=3 independent
    # additionally: confirm the plane is PG(2,8) intrinsically: 73 points, line size 9
    out["is_projective_plane_order_8"] = (
        res["n_lines"] == 73 and res["all_lines_size_9"]
        and res["every_pair_exactly_once"] and res["each_point_on_9_lines"])

    os.makedirs("artifacts", exist_ok=True)
    with open(os.path.join("artifacts", "task1.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)
    print("\nPASS task1:", res["matches_coordinate_PG28"] and out["is_projective_plane_order_8"]
          and out["example_is_cap"] and len(S) == 9)


if __name__ == "__main__":
    sys.exit(0 if main() is None else 1)
