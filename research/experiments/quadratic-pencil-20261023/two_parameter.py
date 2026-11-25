#!/usr/bin/env python3
"""Full real (lambda,mu) plane for det[x²+lambda*y²+mu*x*y,x,y,1] on 3x3."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import gcd
from pathlib import Path
import json

from classify import det3, solve
from independent import audit, determinant


def evaluate(line, point):
    a, b, c = line
    x, y = point
    return a*x+b*y+c


def main():
    points = [(x, y) for y in range(3) for x in range(3)]
    common, lines = [], {}
    for ids in combinations(range(9), 4):
        selected = [points[i] for i in ids]
        x, y = selected[-1]
        columns = [lambda u, v: v*v, lambda u, v: u*v, lambda u, v: u*u]
        coefficients = []
        for f in columns:
            fast = det3(*[(f(u,v)-f(x,y), u-x, v-y) for u,v in selected[:-1]])
            slow = determinant([[f(u,v), u, v, 1] for u,v in selected])
            assert fast == slow
            coefficients.append(fast)
        a, b, c = coefficients
        mask = sum(1 << i for i in ids)
        if a == b == c == 0:
            common.append(mask)
        elif a or b:
            divisor = gcd(gcd(a,b),c)
            sign = 1 if next(v for v in coefficients if v) > 0 else -1
            key = tuple(sign*v//divisor for v in coefficients)
            lines.setdefault(key, []).append(mask)
    vertices = set()
    for (a,b,c), (d,e,f) in combinations(lines,2):
        det = a*e-b*d
        if det:
            vertices.add((Fraction(b*f-c*e, det), Fraction(c*d-a*f, det)))

    # A point avoiding all lines exists; find an exact rational representative.
    generic = next((Fraction(x), Fraction(y)) for x in range(30) for y in range(30)
                   if all(evaluate(line,(x,y)) for line in lines))
    strata = [('generic', generic, [])]
    for line in sorted(lines):
        a,b,c = line
        for t in range(len(vertices)+2):
            point = (Fraction(t), Fraction(-c-a*t,b)) if b else (Fraction(-c,a), Fraction(t))
            if point not in vertices:
                break
        else:
            raise AssertionError('no line representative')
        assert [other for other in lines if not evaluate(other,point)] == [line]
        strata.append(('line', point, [line]))
    for point in sorted(vertices):
        strata.append(('intersection', point, sorted(line for line in lines if not evaluate(line,point))))

    cases, comparisons = [], 0
    for kind, point, active in strata:
        edges = common + [edge for line in active for edge in lines[line]]
        # Direct parameter substitution audits the classified family too.
        direct = []
        lam, mu = point
        for ids in combinations(range(9),4):
            matrix = [[x*x+lam*y*y+mu*x*y,x,y,1] for x,y in (points[i] for i in ids)]
            if determinant(matrix) == 0:
                direct.append(sum(1 << i for i in ids))
        assert set(edges) == set(direct)
        profile, safe, values = solve(9, edges)
        comparisons += audit(9, direct, safe, values)
        cases.append({'kind': kind, 'representative': [str(v) for v in point],
                      'active_lines': active, **profile})
    report = {'board': '3x3', 'rule': 'det[x^2+lambda*y^2+mu*x*y,x,y,1]=0',
              'domain': 'all real (lambda,mu)', 'universal_edges': len(common),
              'lines': [{'coefficients': k, 'added_edges': len(v)} for k,v in sorted(lines.items())],
              'strata_by_kind': dict(Counter(c['kind'] for c in cases)),
              'root_grundy_counts': dict(Counter(c['root_grundy'] for c in cases)),
              'all_safe_state_comparisons': comparisons, 'cases': cases}
    Path(__file__).with_name('two-parameter.json').write_text(json.dumps(report,indent=2)+'\n')
    print({k:v for k,v in report.items() if k not in ('lines','cases')})


if __name__ == '__main__':
    main()
