#!/usr/bin/env python3
"""Independent finite audits for the unconditional 4-row 8-point circle gap theorem.

The universal proof is in q48_chord_gap_theorem.md; this program is NOT
substituted for that proof. Only Python's standard library is used.
"""
from math import isqrt


def exclude_even_chords_mod8():
    residues=(0,1,4)
    witnesses=[(a,b,c,d) for a in residues for b in residues
               for c in residues for d in residues
               if (a-2*b+c+2)%8==0 and (b-2*c+d+2)%8==0]
    assert witnesses==[]
    return len(residues)**4


def small_gap_cases():
    # The proof's independent finite endpoint: c<=4 and l=b-c>=1.
    cases = []
    for c in range(1, 5):
        for l in range(1, 2*c*c+3):
            b = c + l
            numer = 2*c*c + 2 - l*l
            if numer <= 0 or numer % l:
                continue
            d1 = numer // l
            if d1 < 2*(b+1)+1:
                continue
            delta = (d1 - 2*b)**2 - 4*(2*b*b+2)
            cases.append((c,l,b,d1,delta))
            assert delta < 0 or isqrt(delta)**2 != delta
    assert cases == [
        (2,1,3,9,-71),
        (3,1,4,19,-15),
        (4,1,5,33,321),
        (4,2,6,15,-287),
    ], cases
    return cases


def first_nonlocal_width_certificate():
    # For an increasing nonlocal profile with largest chord <=73,
    # d3 >= 6*c + 4*l + 3, hence c<=11. Enumerate divisor pairs only.
    cases=[]
    for c in range(1,12):
        for l in range(1,2*c*c+3):
            T=2*c*c+2
            if T%l: continue
            b=c+l
            d1=T//l-l
            d3=d1+4*c+2*l
            if d1%2==0 or d1<2*(b+1)+1 or d3>73: continue
            delta=(d1-2*b)**2-4*(2*b*b+2)
            cases.append((c,l,b,d1,d3,delta))
    assert cases==[
        (2,1,3,9,19,-71),
        (3,1,4,19,33,-15),
        (4,1,5,33,51,321),
        (4,2,6,15,35,-287),
        (5,1,6,51,73,1225),
        (6,2,8,35,63,-159),
    ],cases
    assert isqrt(1225)==35
    # At c=5,l=1 the quadratic roots are k=2 and 37;
    # only k=2 makes d0=d1-2*(b+k)>0.
    b,d1=6,51
    assert d1-2*(b+2)==35 and d1-2*(b+37)<0
    return cases


def enumerate_chords(limit=3000):
    # Independent direct integer-square test, not gap parametrization.
    found = []
    for d0 in range(1, limit+1, 2):
        for d1 in range(1, limit+1, 2):
            sq2 = 2*d1*d1 - d0*d0 - 8
            sq3 = 3*d1*d1 - 2*d0*d0 - 24
            if sq2 <= 0 or sq3 <= 0:
                continue
            d2 = isqrt(sq2)
            d3 = isqrt(sq3)
            if d2*d2 != sq2 or d3*d3 != sq3:
                continue
            found.append((d0,d1,d2,d3))
    expected = [
        (1,3,3,1),
        (35,51,63,73),
        (73,63,51,35),
        (1331,1935,2391,2773),
        (2773,2391,1935,1331),
    ]
    assert found == expected, found
    for d in found:
        if d == (1,3,3,1):
            continue
        assert d == tuple(sorted(d)) or d == tuple(sorted(d, reverse=True))
        assert min(abs(d[i+1]-d[i]) for i in range(3)) >= 10
        s = max(d)
        points = [((s+sign*di)//2, i) for i,di in enumerate(d) for sign in (-1,1)]
        assert len({x for x,y in points}) == 8
        assert all((s+sign*di)%2 == 0 for di in d for sign in (-1,1))
        p = [(s*s-di*di)//4 for di in d]
        C = p[1]-p[0]-1
        assert all(pi == i*i+C*i+p[0] for i,pi in enumerate(p))
        assert all(x*x+y*y-s*x+C*y+p[0] == 0 for x,y in points)
    return found


def pell_sharpness():
    u,v = 19,6
    out=[]
    for n in range(1,9):
        assert u*u-10*v*v==1
        d=(9*v-u,3*u-v,3*u+v,u+9*v)
        assert all(x>0 and x%2 for x in d)
        assert d[0]**2-2*d[1]**2+d[2]**2 == -8
        assert d[1]**2-2*d[2]**2+d[3]**2 == -8
        out.append((n,min(d[i+1]-d[i] for i in range(3))))
        u,v=19*u+60*v,6*u+19*v
    assert out[0] == (1,10)
    return out


if __name__ == '__main__':
    print('even_parity_mod8_cases_excluded=',exclude_even_chords_mod8())
    print('small_gap_cases=',small_gap_cases())
    print('first_nonlocal_width_certificate=',first_nonlocal_width_certificate())
    print('complete_odd_d0_d1_up_to_3000=',enumerate_chords())
    print('pell_gap_checks=',pell_sharpness())
    print('PASS: finite audits; universal proof is separate')
