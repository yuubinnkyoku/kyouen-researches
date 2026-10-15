#!/usr/bin/env python3
"""Independent integer audit for the unbounded four-row q=8 Pell completion.

The mathematical proof is in ../reports/q48-all-nonlocal-pell-20261015.md.
This script is only a finite audit; it does not prove an infinite assertion.
"""
from math import gcd, isqrt

# These initial chord quadruples were independently enumerated by the q48 census.
CHORDS = [
    (35, 51, 63, 73),
    (1331, 1935, 2391, 2773),
    (50543, 73479, 90795, 105301),
    (445465, 715719, 908883, 1067653),
    (98119, 1096275, 1547259, 1893727),
]


def normalize(chords):
    a, b, c, d = chords
    assert 0 < a < b < c < d and all(z % 2 for z in chords)
    s, t, u, v = (d + a) // 2, (d - a) // 2, (c + b) // 2, (c - b) // 2
    assert s * t == 3 * u * v
    h = gcd(s, v)
    A, B, L = s // h, v // h, h
    g = gcd(A, 3)
    assert (u * g) % A == 0
    M = (u * g) // A
    P, Q = A*A - B*B, (A*A - 9*B*B)//(g*g)
    assert A > 3*B and Q > 0 and P >= 15
    assert Q*M*M - P*L*L == 8
    assert isqrt(P*Q)**2 != P*Q
    return A, B, g, L, M, P, Q


def pell_fundamental(D):
    """Continued fractions: minimal positive solution U²-D V²=1."""
    a0 = isqrt(D)
    assert a0*a0 != D
    m, den, a = 0, 1, a0
    p0, p1, q0, q1 = 1, a, 0, 1
    while p1*p1 - D*q1*q1 != 1:
        m = den*a - m
        den = (D-m*m)//den
        a = (a0+m)//den
        p0, p1 = p1, a*p1+p0
        q0, q1 = q1, a*q1+q0
    return p1, q1


def chord_from_params(A, B, g, L, M):
    return (A*L - (3*B//g)*M, (A//g)*M - B*L,
            (A//g)*M + B*L, A*L + (3*B//g)*M)


def direct_circle_audit(chords):
    """Check 8 distinct lattice points on one circle, by direct circle equation."""
    D = max(chords)
    pts = []
    for y, d in enumerate(chords):
        assert d > 0 and d % 2 and d <= D
        pts.extend([((D-d)//2, y), ((D+d)//2, y)])
    assert len(set(pts)) == 8
    # x²+y²+Bx+Cy+E=0, first and last row determine B,C,E.
    # The horizontal center is D/2, so B=-D.
    E4 = D*D - chords[0]*chords[0]
    C4 = chords[0]*chords[0] - chords[1]*chords[1] - 4
    assert E4 % 4 == 0 and C4 % 4 == 0
    E, C = E4//4, C4//4
    for x,y in pts:
        assert x*x+y*y-D*x+C*y+E == 0
    # Independent four-point concyclicity via determinant of lifted points.
    # Fix the first three non-collinear points and check remaining five.
    p0,p1,p2 = pts[:3]
    def det3(r1,r2,r3):
        return (r1[0]*(r2[1]*r3[2]-r2[2]*r3[1])
               -r1[1]*(r2[0]*r3[2]-r2[2]*r3[0])
               +r1[2]*(r2[0]*r3[1]-r2[1]*r3[0]))
    def row(p,base):
        x,y=p; a,b=base
        return (x-a,y-b,x*x+y*y-a*a-b*b)
    for p in pts[3:]:
        assert det3(row(p1,p0),row(p2,p0),row(p,p0)) == 0
    return D+1


def audit_square_discriminant_exception():
    """All same-parity factor pairs of 8/p, p squarefree dividing 8."""
    possible = []
    for p in (1,2):
        n=8//p
        for u in range(1,isqrt(n)+1):
            if n%u:continue
            v=n//u
            if (u+v)%2 or (v-u)%2:continue
            SM,RL=(u+v)//2,(v-u)//2
            if RL>0:
                possible.append((p,RL,SM))
    assert possible == [(1,1,3)]
    return possible


def finite_square_discriminant_scan():
    """Independent finite exhaustive check, not the proof of the lemma."""
    found=[]
    for P in range(1,201):
        for Q in range(1,201):
            if isqrt(P*Q)**2 != P*Q:
                continue
            for L in range(1,101):
                num=P*L*L+8
                if num%Q:continue
                M=isqrt(num//Q)
                if M*M*Q == num:
                    found.append((P,Q,L,M))
    assert sorted(found)==[(1,1,1,3),(1,9,1,1)]
    return found


def main():
    print('Square discriminant factorization exceptions (p, rL, sM):',
          audit_square_discriminant_exception())
    print('Independent P,Q<=200, L<=100 scan:',finite_square_discriminant_scan())
    for initial in CHORDS:
        A,B,g,L,M,P,Q = normalize(initial)
        D=P*Q
        U,V=pell_fundamental(D)
        # Squaring ensures U odd, V even; thus chord parity is preserved.
        U,V=U*U+D*V*V, 2*U*V
        assert U%2==1 and V%2==0 and U*U-D*V*V==1
        widths=[]
        for _ in range(3):
            chords=chord_from_params(A,B,g,L,M)
            assert chords[0]>0 and all(chords[i]<chords[i+1] for i in range(3))
            assert all(d%2 for d in chords)
            assert chords[0]*chords[0]-2*chords[1]*chords[1]+chords[2]*chords[2]==-8
            assert chords[1]*chords[1]-2*chords[2]*chords[2]+chords[3]*chords[3]==-8
            widths.append(direct_circle_audit(chords))
            L,M=U*L+Q*V*M,U*M+P*V*L
            assert Q*M*M-P*L*L==8
        assert widths[0]<widths[1]<widths[2]
        print('initial=',initial,'slope=',(A,B),'P,Q=',(P,Q),
              'Pell_D_digits=',len(str(D)),'width_digits=',tuple(len(str(w)) for w in widths))
    print('PASS: five independent initial shapes; 15 generated circles; 75 lifted determinant checks')

if __name__=='__main__':
    main()
