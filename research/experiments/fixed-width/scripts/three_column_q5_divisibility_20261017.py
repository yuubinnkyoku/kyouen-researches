#!/usr/bin/env python3
"""Independent finite checks for the three-column anisotropic q>=5 theorem.

Method A: circles from two vertical chords (uses rational centers).
Method B: all non-collinear triples and normalized integer circle equations.
A game audit independently builds forbidden q-tuples and computes mex.
Only the accompanying paper proves the unbounded statement.
"""
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import gcd


def points(h, d, m):
    return tuple((i * h, j * d) for i in range(3) for j in range(m))


def circle_key(a, b, c):
    x1, y1 = a
    x2, y2 = b
    x3, y3 = c
    dx, dy, ex, ey = x2 - x1, y2 - y1, x3 - x1, y3 - y1
    den = dx * ey - dy * ex
    if den == 0:
        return None
    p = x2*x2 + y2*y2 - x1*x1 - y1*y1
    q = x3*x3 + y3*y3 - x1*x1 - y1*y1
    aa = -p * ey + dy * q
    bb = -dx * q + p * ex
    cc = -den * (x1*x1 + y1*y1) - aa*x1 - bb*y1
    g = gcd(gcd(abs(den), abs(aa)), gcd(abs(bb), abs(cc)))
    den, aa, bb, cc = (z // g for z in (den, aa, bb, cc))
    if den < 0:
        den, aa, bb, cc = -den, -aa, -bb, -cc
    return den, aa, bb, cc


def all_circles_by_triples(P):
    circles = set()
    for a, b, c in combinations(P, 3):
        k = circle_key(a, b, c)
        if k is not None:
            circles.add(k)
    result = {}
    for key in circles:
        den, aa, bb, cc = key
        on = frozenset(p for p in P if den * (p[0]**2 + p[1]**2) + aa*p[0] + bb*p[1] + cc == 0)
        if len(on) >= 5:
            result[key] = on
    return result


def circles_by_two_chords(h, d, m):
    P = points(h, d, m)
    col = [[(i*h, j*d) for j in range(m)] for i in range(3)]
    result = {}
    for i, j in combinations(range(3), 2):
        for a, b in combinations(col[i], 2):
            ya = Fraction(a[1] + b[1], 2)
            r1 = Fraction((a[1] - b[1])**2, 4)
            for c, e in combinations(col[j], 2):
                if c[1] + e[1] != a[1] + b[1]:
                    continue
                r2 = Fraction((c[1] - e[1])**2, 4)
                xi, xj = i*h, j*h
                xc = Fraction(xj*xj - xi*xi, 1) + r2 - r1
                xc /= 2*(xj-xi)
                radius2 = (xi-xc)**2 + r1
                on = frozenset((x, y) for x, y in P if (x-xc)**2 + (Fraction(y)-ya)**2 == radius2)
                if len(on) >= 5:
                    # Convert the independently constructed center into an integer circle key.
                    # Rational coefficients -2xc, -2ya, xc²+ya²-radius²
                    A = -2*xc
                    B = -2*ya
                    C = xc*xc + ya*ya - radius2
                    from math import lcm
                    L = lcm(A.denominator, B.denominator, C.denominator)
                    raw = (L, int(L*A), int(L*B), int(L*C))
                    g = gcd(gcd(abs(raw[0]), abs(raw[1])), gcd(abs(raw[2]), abs(raw[3])))
                    key = tuple(z//g for z in raw)
                    result[key] = on
    return result


def finite_circle_audit():
    cases = 0
    with_5 = 0
    total_5 = 0
    total_6 = 0
    for h in range(1, 6):
        for d in range(1, 6):
            for m in range(3, 9):
                P = points(h, d, m)
                a = circles_by_two_chords(h, d, m)
                b = all_circles_by_triples(P)
                assert a == b, (h, d, m, a.keys() ^ b.keys())
                if h % d:
                    assert not a, (h, d, m, a)
                cases += 1
                with_5 += bool(a)
                total_5 += sum(len(v)==5 for v in a.values())
                total_6 += sum(len(v)==6 for v in a.values())
    return dict(boards=cases, boards_with_five_or_six=with_5,
                circles_exactly_five=total_5, circles_exactly_six=total_6)


def game_audit(h=1, d=2, m=6, q=5):
    P = points(h, d, m)
    n = len(P)
    forbidden = set()
    for indices in combinations(range(n), q):
        Q = [P[i] for i in indices]
        collinear = all((Q[i][0]-Q[0][0])*(Q[1][1]-Q[0][1]) ==
                        (Q[i][1]-Q[0][1])*(Q[1][0]-Q[0][0]) for i in range(2, q))
        k = circle_key(*Q[:3])
        concyclic = (k is not None and all(k[0]*(x*x+y*y)+k[1]*x+k[2]*y+k[3]==0 for x,y in Q))
        if collinear or concyclic:
            forbidden.add(sum(1<<i for i in indices))
    expected = {sum(1<<i for i in indices) for indices in combinations(range(n),q)
                if len({P[i][0] for i in indices}) == 1}
    assert forbidden == expected, (len(forbidden),len(expected), forbidden^expected)
    masks = [sum(1<<i for i in range(col*m, (col+1)*m)) for col in range(3)]
    @lru_cache(None)
    def grundy(state):
        moves = []
        for i in range(n):
            if state & (1<<i):
                continue
            new = state | (1<<i)
            if any((new & fm)==fm for fm in forbidden):
                continue
            moves.append(grundy(new))
        value=0
        while value in moves:
            value+=1
        expected_value = (3*min(m,q-1)-state.bit_count())%2
        assert value == expected_value, (state,value,expected_value)
        return value
    assert grundy(0)==0
    return dict(forbidden_q_tuples=len(forbidden), audited_safe_states=grundy.cache_info().currsize,
                root_grundy=grundy(0))


if __name__ == '__main__':
    print('circle:', finite_circle_audit())
    print('game:', game_audit())
