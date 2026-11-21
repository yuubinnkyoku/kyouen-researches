# circ_big_scan.py — big-class-only circle scan for larger n (memory-light).
# For centers i,j in [0,2n-1): count points per (center,d2); record classes >=12 with (c,i,j,d2),
# and aggregate counts for classes 9,10,11. Classes <9 are skipped entirely.
import sys
from collections import defaultdict

def scan_big(n):
    pts2 = [(2*x, 2*y) for x in range(n) for y in range(n)]
    hist911 = defaultdict(int)
    bigs = []
    for i in range(0, 2*n-1):
        for j in range(0, 2*n-1):
            cnt = defaultdict(int)
            for (X, Y) in pts2:
                cnt[(X-i)**2 + (Y-j)**2] += 1
            for d2, c in cnt.items():
                if c >= 12:
                    bigs.append((c, i, j, d2))
                elif c >= 9:
                    hist911[c] += 1
    return dict(sorted(hist911.items())), sorted(bigs)

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]]:
        h911, bigs = scan_big(n)
        byC = defaultdict(list)
        for c, i, j, d2 in bigs:
            byC[c].append(d2)
        print("n=%d hist(9..11)=%s" % (n, h911))
        for c in sorted(byC):
            fam = defaultdict(int)
            for d2 in byC[c]:
                fam[d2] += 1
            print("n=%d pts=%d families=%s total=%d" % (n, c, dict(sorted(fam.items())), sum(fam.values())))
