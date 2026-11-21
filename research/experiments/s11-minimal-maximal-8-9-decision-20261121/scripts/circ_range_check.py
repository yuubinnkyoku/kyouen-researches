# circ_range_check.py — do 4+-point half-lattice circles exist OUTSIDE the standard scan range?
# circ_catalog_scan.py scans centers i,j in [0,2n-1). A circle whose hl center lies outside that
# range cannot be partner-closed in the grid (point reflection through center maps every grid
# point's partner outside too). Census (all rational centers) equality for classes >=9 at n=10..12
# already proves no such circle exists with >=9 points there. This script quantifies small classes:
# scan a much wider center range [-2n, 4n) per coordinate and report per-class counts, comparing
# in-range vs wide-range totals.
import sys
from collections import defaultdict

def scan(n, lo, hi):
    hist = defaultdict(int)
    pts2 = [(2*x, 2*y) for x in range(n) for y in range(n)]
    for i in range(lo, hi):
        for j in range(lo, hi):
            cnt = defaultdict(int)
            for (X, Y) in pts2:
                cnt[(X-i)**2 + (Y-j)**2] += 1
            for d2, c in cnt.items():
                if c >= 4:
                    hist[c] += 1
    return dict(sorted(hist.items()))

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]]:
        inner = scan(n, 0, 2*n-1)
        wide = scan(n, -2*n, 4*n)
        print("n=%d  in-range[0,2n):%s" % (n, inner))
        print("n=%d  wide[-2n,4n):%s" % (n, wide))
        extra = {k: wide.get(k,0)-inner.get(k,0) for k in wide if wide[k] != inner.get(k,0)}
        print("n=%d  classes with extra circles outside standard range: %s" % (n, extra if extra else "NONE"))
