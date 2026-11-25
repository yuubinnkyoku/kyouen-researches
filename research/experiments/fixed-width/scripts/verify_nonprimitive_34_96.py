"""Exact independent construction/verification of F(k) upper bounds, 34<=k<=96.
Only six explicit integer-centred circles are considered; no optimality claim.
"""
from math import gcd, isqrt
from pathlib import Path

RADII_SQUARED = (143650, 320450, 1602250, 4165850, 8011250, 11856650)

def circle_rows(n):
    r = isqrt(n)
    return [y for y in range(-r, r+1) if (z := n-y*y) > 0 and isqrt(z)**2 == z]

def compute():
    answers = {}
    for n in RADII_SQUARED:
        rows = circle_rows(n)
        for parity in (0, 1):
            yy = [y for y in rows if y % 2 == parity]
            for k in range(34, min(96, len(yy)) + 1):
                for i in range(len(yy) - k + 1):
                    chosen = yy[i:i+k]
                    width = chosen[-1]-chosen[0]+1
                    if k not in answers or width < answers[k][0]:
                        answers[k] = (width, n, chosen)
    assert set(answers) == set(range(34, 97))
    for k, (width, n, ys) in answers.items():
        assert len(ys) == k and ys == sorted(set(ys))
        assert width == ys[-1]-ys[0]+1
        assert gcd(*(y-ys[0] for y in ys[1:])) == 2
        for y in ys:
            x = isqrt(n-y*y)
            assert x > 0 and x*x+y*y == n
            assert (-x)**2+y*y == n
    return answers

if __name__ == '__main__':
    answers = compute()
    for k, (width, n, ys) in answers.items():
        print(f'{k}\t{width}\t{n}\t{ys[0]}\t{ys[-1]}\t' + ','.join(map(str,ys)))
    print('PASS: 63 constructions, all gcd=2 and two distinct integer points per row', file=__import__('sys').stderr)
