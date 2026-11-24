#!/usr/bin/env python3
"""Independent verification of the two game boards.

PG(2,7): 57 points, 57 lines of size 8, every two points on exactly one line
         (projectively: every two lines meet in exactly one point).
AG(2,7): 49 points, 56 lines of size 7, every two points on exactly one line,
         8 parallel classes each consisting of 7 disjoint lines partitioning
         the point set.

Reads only the two board files; writes board_checks.json next to this script.
No third-party imports.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BOARDS = {
    "pg2q7": os.path.join(
        REPO, "research", "experiments", "projective-blocking-kyouen-20261125",
        "output", "board_pg2q7.txt"),
    "ag2q7": os.path.join(
        REPO, "research", "experiments", "s-parameter-kyouen-20261125",
        "output", "board_ag2q7.txt"),
}


def read_board(path):
    with open(path, "r", encoding="utf-8") as f:
        toks = f.read().split()
    it = iter(toks)
    n = int(next(it))
    b = int(next(it))
    lines = []
    for _ in range(b):
        k = int(next(it))
        pts = tuple(int(next(it)) for _ in range(k))
        lines.append(pts)
    try:
        extra = next(it)
        raise AssertionError("trailing token %r" % (extra,))
    except StopIteration:
        pass
    return n, lines


def check_basic(n, lines):
    res = {}
    res["n"] = n
    res["b"] = len(lines)
    res["line_sizes"] = sorted(set(len(L) for L in lines))
    res["line_size_ok"] = all(len(L) == res["line_sizes"][0] for L in lines)
    res["all_points_in_range"] = all(0 <= p < n for L in lines for p in L)
    res["points_distinct_within_line"] = all(len(set(L)) == len(L) for L in lines)
    res["duplicate_lines"] = len(lines) - len(set(frozenset(L) for L in lines))
    covered = set(p for L in lines for p in L)
    res["points_covered"] = len(covered)
    res["all_points_covered"] = (covered == set(range(n)))
    return res


def pair_incidence(n, lines):
    """Return (ok, max_count, pair_count) for point pairs."""
    pair_line = {}
    bad = []
    for li, L in enumerate(lines):
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                key = (L[i], L[j]) if L[i] < L[j] else (L[j], L[i])
                if key in pair_line:
                    bad.append((key, pair_line[key], li))
                else:
                    pair_line[key] = li
    expected = n * (n - 1) // 2
    return (not bad and len(pair_line) == expected,
            len(bad), len(pair_line), expected, bad[:5])


def line_intersections(lines):
    """Return dict of intersection-size distribution and violations for pairs."""
    dist = {}
    viol = []
    b = len(lines)
    sets = [frozenset(L) for L in lines]
    for i in range(b):
        for j in range(i + 1, b):
            c = len(sets[i] & sets[j])
            dist[c] = dist.get(c, 0) + 1
            if c != 1:
                viol.append((i, j, c))
    return dist, viol


def has_quadrangle(n, lines):
    """Four points with no three collinear (PG non-degeneracy)."""
    line_of = {}
    for li, L in enumerate(lines):
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                key = (L[i], L[j]) if L[i] < L[j] else (L[j], L[i])
                line_of[key] = li
    # Fix p0=0, p1 = some point not equal; p2 off line 0-1; p3 off all three lines.
    p0 = 0
    for p1 in range(1, n):
        l01 = line_of[(0, p1)]
        for p2 in range(1, n):
            if p2 == p1:
                continue
            if line_of[(0, p2)] == l01 or line_of[(p1, p2)] == l01:
                continue
            l02 = line_of[(0, p2)]
            l12 = line_of[(p1, p2)]
            for p3 in range(1, n):
                if p3 in (p1, p2):
                    continue
                if (line_of[(0, p3)] in (l01, l02) or
                        line_of[(p1, p3)] in (l01, l12) or
                        line_of[(p2, p3)] in (l02, l12)):
                    continue
                return True, (p0, p1, p2, p3)
    return False, None


def check_pg(n, lines):
    r = check_basic(n, lines)
    r["expected_n"] = 57
    r["expected_b"] = 57
    r["expected_line_size"] = 8
    ok_pair, nbad, npairs, expected, bad = pair_incidence(n, lines)
    r["pair_unique"] = ok_pair
    r["duplicate_pair_count"] = nbad
    r["pairs_seen"] = npairs
    r["pairs_expected"] = expected
    r["duplicate_pair_examples"] = bad
    dist, viol = line_intersections(lines)
    r["line_intersection_distribution"] = {str(k): v for k, v in sorted(dist.items())}
    r["line_pairs_meet_unique_point"] = (viol == [] and set(dist) == {1})
    r["line_pair_violations"] = viol[:5]
    deg = [0] * n
    for L in lines:
        for p in L:
            deg[p] += 1
    r["point_degree_set"] = sorted(set(deg))
    r["point_degrees_all_8"] = (set(deg) == {8})
    quad, witness = has_quadrangle(n, lines)
    r["has_quadrangle"] = quad
    r["quadrangle_witness"] = witness
    r["is_projective_plane_order_7"] = all([
        n == 57, len(lines) == 57, r["line_size_ok"],
        r["line_sizes"] == [8], r["all_points_in_range"],
        r["points_distinct_within_line"], r["duplicate_lines"] == 0,
        r["all_points_covered"], ok_pair, r["line_pairs_meet_unique_point"],
        quad,
    ])
    return r


def check_ag(n, lines):
    r = check_basic(n, lines)
    r["expected_n"] = 49
    r["expected_b"] = 56
    r["expected_line_size"] = 7
    ok_pair, nbad, npairs, expected, bad = pair_incidence(n, lines)
    r["pair_unique"] = ok_pair
    r["duplicate_pair_count"] = nbad
    r["pairs_seen"] = npairs
    r["pairs_expected"] = expected
    r["duplicate_pair_examples"] = bad
    deg = [0] * n
    for L in lines:
        for p in L:
            deg[p] += 1
    r["point_degree_set"] = sorted(set(deg))
    r["point_degrees_all_8"] = (set(deg) == {8})
    # Parallel = disjoint.  Union-find over lines.
    b = len(lines)
    sets = [frozenset(L) for L in lines]
    parent = list(range(b))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    disjoint_partners = [[] for _ in range(b)]
    for i in range(b):
        for j in range(i + 1, b):
            if sets[i].isdisjoint(sets[j]):
                disjoint_partners[i].append(j)
                disjoint_partners[j].append(i)
                union(i, j)
    classes = {}
    for i in range(b):
        classes.setdefault(find(i), []).append(i)
    class_list = sorted(classes.values(), key=lambda L: L[0])
    r["num_classes"] = len(class_list)
    r["class_sizes"] = sorted(len(c) for c in class_list)
    r["each_line_has_6_parallel_partners"] = all(
        len(x) == 6 for x in disjoint_partners)
    class_ok = []
    for c in class_list:
        union_pts = set()
        pairwise_disjoint = True
        for i in range(len(c)):
            union_pts |= sets[c[i]]
            for j in range(i + 1, len(c)):
                if not sets[c[i]].isdisjoint(sets[c[j]]):
                    pairwise_disjoint = False
        class_ok.append({
            "size": len(c),
            "covers_all_points": union_pts == set(range(n)),
            "pairwise_disjoint": pairwise_disjoint,
        })
    r["classes"] = class_ok
    # Lines from different classes must meet in exactly one point.
    cross_dist = {}
    cross_viol = []
    for a in range(len(class_list)):
        for bb in range(a + 1, len(class_list)):
            for i in class_list[a]:
                for j in class_list[bb]:
                    c = len(sets[i] & sets[j])
                    cross_dist[c] = cross_dist.get(c, 0) + 1
                    if c != 1:
                        cross_viol.append((i, j, c))
    r["cross_class_intersection_distribution"] = {
        str(k): v for k, v in sorted(cross_dist.items())}
    r["cross_class_violations"] = cross_viol[:5]
    # Non-degeneracy: three points not all on one line.
    line_of = {}
    for li, L in enumerate(lines):
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                line_of[(L[i], L[j]) if L[i] < L[j] else (L[j], L[i])] = li
    nondeg = False
    witness = None
    for a in range(n):
        for bb in range(a + 1, n):
            for c in range(bb + 1, n):
                if line_of[(a, bb)] != line_of[(a, c)]:
                    nondeg = True
                    witness = (a, bb, c)
                    break
            if nondeg:
                break
        if nondeg:
            break
    r["three_noncollinear_points"] = nondeg
    r["noncollinear_witness"] = witness
    r["is_affine_plane_order_7"] = all([
        n == 49, len(lines) == 56, r["line_size_ok"],
        r["line_sizes"] == [7], r["all_points_in_range"],
        r["points_distinct_within_line"], r["duplicate_lines"] == 0,
        r["all_points_covered"], ok_pair,
        r["point_degrees_all_8"],
        r["num_classes"] == 8, r["class_sizes"] == [7] * 8,
        all(x["covers_all_points"] and x["pairwise_disjoint"] for x in class_ok),
        set(cross_dist) == {1}, nondeg,
    ])
    return r


def main():
    out = {}
    n, lines = read_board(BOARDS["pg2q7"])
    out["pg2q7"] = check_pg(n, lines)
    n, lines = read_board(BOARDS["ag2q7"])
    out["ag2q7"] = check_ag(n, lines)
    path = os.path.join(HERE, "board_checks.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    ok = True
    for name, r in out.items():
        status = "PASS" if r.get("is_projective_plane_order_7",
                                r.get("is_affine_plane_order_7")) else "FAIL"
        ok = ok and status == "PASS"
        print("%s: %s  n=%d b=%d sizes=%s pairs_unique=%s" % (
            name, status, r["n"], r["b"], r["line_sizes"], r["pair_unique"]))
        if name == "pg2q7":
            print("  line intersection dist:", r["line_intersection_distribution"],
                  "point degrees:", r["point_degree_set"],
                  "quadrangle:", r["has_quadrangle"])
        else:
            print("  classes:", r["class_sizes"],
                  "cross dist:", r["cross_class_intersection_distribution"],
                  "point degrees:", r["point_degree_set"])
    print("wrote", path)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
