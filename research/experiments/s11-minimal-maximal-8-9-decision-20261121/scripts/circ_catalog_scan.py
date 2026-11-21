# circ_catalog_scan.py — half-lattice center scan: full catalog statistics of lattice circles.
# For every half-lattice center (i/2, j/2) and every scaled distance d2 = (2x-i)^2+(2y-j)^2,
# count lattice points at that distance. Circles with >=4 points are catalogued.
# Validation question: do half-lattice centers capture ALL 4+-point lattice circles
# (i.e., does this count agree with the 3-point-construction catalog census)?
import sys
from collections import defaultdict

def scan(n):
    hist = defaultdict(int)
    total4 = 0
    big = {}
    pts2 = [(2*x, 2*y) for x in range(n) for y in range(n)]
    for i in range(0, 2*n-1):
        for j in range(0, 2*n-1):
            cnt = defaultdict(int)
            for (X, Y) in pts2:
                cnt[(X-i)**2 + (Y-j)**2] += 1
            for d2, c in cnt.items():
                if c >= 4:
                    total4 += 1
                    hist[c] += 1
                    if c >= 12:
                        big[("c%d.%d" % (i, j), d2)] = c
    return total4, dict(sorted(hist.items())), big

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]]:
        t, h, big = scan(n)
        print("n=%d circles(>=4 pts, half-lattice centers)=%d hist=%s" % (n, t, h))
        nbig = len(big)
        print("   circles with >=12 pts: %d; max count: %d" % (nbig, max(big.values()) if big else 0))
