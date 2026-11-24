"""Task 1 -- verify the four start sets are caps and maximal (board incidences only).

Board: output/board_pg2q9.txt (PG(2,9), 91 points, 91 lines of 10).
No coordinates are used here: everything is pure incidence checking, so this
task is independent of the GF(9) model and of the isomorphism.

Run:  python task1_caps.py
"""

from __future__ import annotations

import itertools
import json

import pgcore as pc

STARTS = {
    6: [4, 9, 20, 32, 69, 84],
    7: [16, 47, 51, 56, 60, 80, 82],
    8: [32, 39, 42, 47, 56, 59, 84, 87],
    10: [6, 9, 27, 32, 34, 37, 45, 75, 77, 82],
}


def audit_cap(P, cap):
    cap = sorted(cap)
    cs = set(cap)
    res = {"cap": cap, "size": len(cap), "distinct": len(cs) == len(cap)}
    res["in_range"] = all(0 <= p < P.n for p in cap)
    # (a) cap: at most 2 points on every line
    worst = 0
    bad_lines = []
    for lid, L in enumerate(P.lines):
        c = len(cs & set(L))
        worst = max(worst, c)
        if c > 2:
            bad_lines.append(lid)
    res["max_points_on_a_line"] = worst
    res["is_cap"] = worst <= 2 and res["distinct"] and res["in_range"]
    res["lines_with_3plus"] = bad_lines
    # lines meeting the cap in exactly 2 points (secants) / 1 (tangents) / 0
    sec = [lid for lid, L in enumerate(P.lines) if len(cs & set(L)) == 2]
    tan = [lid for lid, L in enumerate(P.lines) if len(cs & set(L)) == 1]
    res["n_secants"] = len(sec)
    res["n_tangents"] = len(tan)
    res["n_external"] = P.nlines - len(sec) - len(tan)
    res["secant_count_expected"] = len(cap) * (len(cap) - 1) // 2
    res["secant_count_ok"] = len(sec) == res["secant_count_expected"]
    # (b) maximal: no outside point can be added.  A point q outside the cap is
    # addable iff it lies on no secant line (i.e. every line through q meets the
    # cap in <= 1 point).
    on_secant = set()
    for lid in sec:
        on_secant |= P.line_sets[lid]
    addable = [q for q in range(P.n) if q not in cs and q not in on_secant]
    res["addable_points"] = addable
    res["is_maximal"] = len(addable) == 0
    # independent re-check of maximality, point by point (add and test)
    recheck = []
    for q in range(P.n):
        if q in cs:
            continue
        if all(len((cs | {q}) & set(L)) <= 2 for L in P.lines):
            recheck.append(q)
    res["addable_points_recheck"] = recheck
    res["maximal_recheck_agrees"] = addable == recheck
    res["PASS"] = bool(res["is_cap"] and res["is_maximal"] and res["secant_count_ok"]
                       and res["maximal_recheck_agrees"])
    return res


def main():
    P = pc.read_board()
    plane_checks = pc.check_plane(P, "board_pg2q9.txt")
    out = {"board": plane_checks, "caps": {}}
    print(f"board: {P.n} points, {P.nlines} lines; axioms ok = {plane_checks['all_ok']}")
    for k, cap in STARTS.items():
        r = audit_cap(P, cap)
        out["caps"][k] = r
        print(f"\nsize {k}: cap={cap}")
        print(f"  is_cap={r['is_cap']} (max points on a line = {r['max_points_on_a_line']}), "
              f"secants={r['n_secants']} (expect {r['secant_count_expected']}), "
              f"tangents={r['n_tangents']}, external={r['n_external']}")
        print(f"  is_maximal={r['is_maximal']} (addable points = {r['addable_points']})")
        print(f"  PASS={r['PASS']}")
    out["all_PASS"] = all(r["PASS"] for r in out["caps"].values())
    pc.RESULTS.mkdir(parents=True, exist_ok=True)
    (pc.RESULTS / "task1_caps.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nTASK 1: {'PASS' if out['all_PASS'] else 'FAIL'}")
    return out


if __name__ == "__main__":
    main()
