#!/usr/bin/env python3
"""Independent integer-circle equation audit of scan.cpp witnesses and W=6 exhaustive maxima."""
from __future__ import annotations
import itertools
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ROW_RE = re.compile(r"a=(\d+) b=(\d+) max=(\d+).*?y0=(\[[^]]*\]) y\d+=(\[[^]]*\]) y\d+=(\[[^]]*\])")


def count_circles(rows: tuple[tuple[int, ...], ...], a: int, b: int) -> int:
    """Generate every three-horizontal-chord candidate and test a circle equation.

    A circle through (x,z) at y=0 has equation x^2+y^2-s*x+e*y+p=0,
    with s=x+z, p=x*z. Use one point on y=a to determine a*e
    and then test the remaining three points with integer arithmetic.
    No use of the weighted-product identity or middle-edge lookup.
    """
    result = 0
    for u, v in itertools.combinations(rows[0], 2):
        s, p = u + v, u * v
        for m, n in itertools.combinations(rows[1], 2):
            ae = -(m*m + a*a - s*m + p)
            if a*(n*n + a*a - s*n + p) + ae*a != 0:
                continue
            for t, w in itertools.combinations(rows[2], 2):
                y = a + b
                if a*(t*t + y*y - s*t + p) + ae*y != 0:
                    continue
                if a*(w*w + y*y - s*w + p) + ae*y != 0:
                    continue
                result += 1
    return result


def parse(text: str):
    for line in text.splitlines():
        match = ROW_RE.search(line)
        if match:
            a,b,expected = map(int,match.group(1,2,3))
            rows = tuple(tuple(int(x) for x in s.strip('[]').split(',') if x) for s in match.group(4,5,6))
            yield a,b,expected,rows


def audit_witnesses(path: Path):
    rows = list(parse(path.read_text()))
    assert len(rows) == 21, len(rows)
    for a,b,expected,witness in rows:
        if expected == 0:
            assert witness == ((),(),())
            continue
        assert all(len(row)==5 for row in witness)
        observed = count_circles(witness,a,b)
        assert observed == expected, (a,b,expected,observed,witness)
    print('W=16 witness audit: 21/21 cases match independent exact circle equations')


def audit_small(scan_executable: Path):
    process = subprocess.run([str(scan_executable),'6','6'],capture_output=True,text=True,check=True)
    reported = {(a,b):expected for a,b,expected,_ in parse(process.stdout)}
    subsets = list(itertools.combinations(range(6),5))
    assert len(reported)==21
    for a in range(1,7):
        for b in range(a,7):
            best=0
            for r0 in subsets:
                for r1 in subsets:
                    for r2 in subsets:
                        best=max(best,count_circles((r0,r1,r2),a,b))
            assert best == reported[a,b], (a,b,best,reported[a,b])
    print('W=6 exhaustive independent audit: 21/21 gap pairs, 216 configurations each')

if __name__=='__main__':
    audit_witnesses(ROOT.parent/'output'/'results-w16.txt')
    audit_small(Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'scan')
