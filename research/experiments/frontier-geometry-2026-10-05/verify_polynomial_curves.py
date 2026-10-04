"""Finite independent checks of the polynomial-curve theorem and Q_p edges.

Every line through two selected points and every circle through three
noncollinear selected points is generated as a primitive integer equation.
Membership is then tested by direct substitution, without modular filtering.
The shared geometry core independently checks Q_p's four-point catalogue.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from math import gcd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/research"))
from kyouen_core import Board  # noqa: E402
sys.path.insert(0, str(ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"))
from parabola_half_bound import clauses_for_pair  # noqa: E402


def prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, int(n**0.5)+1))


def normalize(coefficients: tuple[int, ...]) -> tuple[int, ...]:
    divisor = gcd(*coefficients)
    if divisor == 0:
        return ()
    sign = 1 if next(c for c in coefficients if c) > 0 else -1
    return tuple(c // divisor * sign for c in coefficients)


def circle(a, b, c):
    # Circumcenter equation A(x²+y²)+Bx+Cy+D=0 from three points.
    x0,y0 = a
    u,v = b[0]-x0,b[1]-y0
    s,t = c[0]-x0,c[1]-y0
    denominator = 2*(u*t-v*s)
    if not denominator:
        return ()
    bnorm = b[0]**2+b[1]**2-x0*x0-y0*y0
    cnorm = c[0]**2+c[1]**2-x0*x0-y0*y0
    twice_ux_num = 2*(bnorm*t-v*cnorm)
    twice_uy_num = 2*(u*cnorm-bnorm*s)
    return normalize((denominator, -twice_ux_num, -twice_uy_num,
                      twice_ux_num*x0+twice_uy_num*y0-denominator*(x0*x0+y0*y0)))


def catalogue(points, p, degree):
    lines = set()
    for (x,y),(u,v) in combinations(points,2):
        lines.add(normalize((v-y, x-u, u*y-v*x)))
    circles = {circle(*triple) for triple in combinations(points,3)} - {()}
    line_sizes = [sum(a*x+b*y+c == 0 for x,y in points) for a,b,c in lines]
    circle_sizes = []
    for a,b,c,d in circles:
        size = sum(a*(x*x+y*y)+b*x+c*y+d == 0 for x,y in points)
        if size > degree:
            assert a % p != 0
        circle_sizes.append(size)
    return max(line_sizes, default=1), max(circle_sizes, default=2)


def decomposed_clauses(p, edges, double):
    """Expand signed NAE blocks and origin clauses, independently of old SAT."""
    clauses = set()
    blocks = Counter()
    for edge in edges:
        pairs = [min(t,p-t) for t in edge if t]
        if len(set(pairs)) != len(pairs):
            continue  # Exactly a two-full-pair trapezoid, already excluded.
        if 0 not in edge:
            reflected = tuple(sorted(p-t for t in edge))
            if edge > reflected:
                continue
        literals = tuple(sorted(-min(t,p-t) if t > p//2 else min(t,p-t)
                                for t in edge if t and min(t,p-t) != double))
        clauses.add(literals)
        if 0 in edge:
            assert len(literals) in (2,3)
            blocks[f"origin-{len(literals)}"] += 1
        else:
            assert len(literals) in (3,4)
            clauses.add(tuple(sorted(-literal for literal in literals)))
            blocks[f"nae-{len(literals)}"] += 1
    return clauses, dict(sorted(blocks.items()))


def evaluate(coefficients, t, p):
    return sum(a*pow(t,i,p) for i,a in enumerate(coefficients)) % p


def main():
    if not __debug__:
        raise SystemExit("Assertions must remain enabled.")
    families = [(0,0,1), (1,3,1), (0,0,0,1), (2,1,0,1),
                (0,0,0,0,1), (1,2,3,1,1)]
    checks = []
    edge_checks = []
    for p in range(3,44):
        if not prime(p):
            continue
        for coefficients in families:
            k = len(coefficients)-1
            if p <= 2*k:
                continue
            points = [(t, evaluate(coefficients,t,p)) for t in range(p)]
            line_max,circle_max = catalogue(points, p, k)
            assert line_max <= k and circle_max <= 2*k
            if coefficients == (0,0,1):
                assert line_max == 2 and circle_max == 4
            checks.append(dict(p=p, coefficients=coefficients, degree=k,
                               line_max=line_max, circle_max=circle_max))
        points = [(t,t*t % p) for t in range(p)]
        board = Board(points)
        edges = [tuple(t for t in range(p) if edge >> t & 1) for edge in board.quads]
        trapezoids = 0
        nonsymmetric = 0
        for edge in edges:
            assert sum(edge) % p == 0
            pairs = [min(t,p-t) for t in edge if t]
            repeated = [pair for pair,count in Counter(pairs).items() if count == 2]
            if repeated:
                assert len(repeated) == 2 and 0 not in edge
                trapezoids += 1
            else:
                nonsymmetric += 1
        h = (p-1)//2
        assert trapezoids == h*(h-1)//2
        for double in range(1,h+1):
            expanded, _ = decomposed_clauses(p, edges, double)
            original = {tuple(sorted(c)) for c in clauses_for_pair(p, edges, double)}
            assert expanded == original
        edge_checks.append(dict(p=p, forbidden_edges=len(edges), trapezoids=trapezoids,
                                nonsymmetric_edges=nonsymmetric,
                                exact_nae_decompositions_checked=h,
                                all_quadruples_checked=p*(p-1)*(p-2)*(p-3)//24))
    sharpness = [
        dict(p=3391, degree=3, coefficients=[0,0,0,1],
             equation=[4,-13564,-13564,15658352],
             parameters=[359,827,1682,1709,2564,3032]),
        dict(p=43, degree=4, coefficients=[0,0,0,0,1],
             equation=[1,-43,-37,642],
             parameters=[10,12,13,19,24,30,31,33]),
    ]
    for witness in sharpness:
        p = witness["p"]
        assert prime(p)
        a,b,c,d = witness["equation"]
        points = [(t,evaluate(witness["coefficients"],t,p))
                  for t in witness["parameters"]]
        assert len(points) == 2*witness["degree"]
        assert all(a*(x*x+y*y)+b*x+c*y+d == 0 for x,y in points)
        witness["coordinates"] = points
    result = {"method": "primitive integer line/circle catalogue and shared exact 4x4 core",
              "polynomial_curve_checks": checks, "q4_edge_checks": edge_checks,
              "sharpness_witnesses": sharpness,
              "scope": "finite supporting checks; universal proof is in proof.md"}
    Path(__file__).with_name("polynomial-curve-audit.json").write_text(
        json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(len(checks), "polynomial curves;", len(edge_checks), "Q_p catalogues;",
          sum(r["all_quadruples_checked"] for r in edge_checks), "four-point checks")


if __name__ == "__main__":
    main()
