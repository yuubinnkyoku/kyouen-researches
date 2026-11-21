# Find high-point circles in n x n grid via half-lattice center scan.
# (2x-scaled integer distances: d2 = (2x-i)^2 + (2y-j)^2, center x=i/2, y=j/2)
import sys
from collections import defaultdict
n = int(sys.argv[1])
pts = [(x, y) for x in range(n) for y in range(n)]
best = (0, None, None)
seen = []
for i in range(0, 2*n-1):
    for j in range(0, 2*n-1):
        cnt = defaultdict(int)
        for (x, y) in pts:
            cnt[(2*x-i)**2 + (2*y-j)**2] += 1
        for d2, c in cnt.items():
            if c >= best[0]:
                best = (c, (i/2, j/2), d2/4)
            if c >= 12:
                seen.append((c, (i/2, j/2), d2/4))
seen.sort(key=lambda t: -t[0])
print("n=%d best: count=%d center=%s r^2=%s" % (n, best[0], best[1], best[2]))
print("circles with >=12 lattice points: %d" % len(seen))
for s in seen[:12]:
    print("  count=%d center=(%g,%g) r2=%s" % (s[0], s[1][0], s[1][1], s[2]))
