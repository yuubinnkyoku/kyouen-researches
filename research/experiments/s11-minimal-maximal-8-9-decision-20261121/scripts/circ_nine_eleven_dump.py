# circ_nine_eleven_dump.py — dump (center, d2, count) of half-lattice circles with 9 or 11 (or 12) points,
# for n in argv, to explain the 4(n-10) counts and the 12-pt family growth.
import sys
from collections import defaultdict

def dump(n):
    pts2 = [(2*x, 2*y) for x in range(n) for y in range(n)]
    out = []
    for i in range(0, 2*n-1):
        for j in range(0, 2*n-1):
            cnt = defaultdict(int)
            for (X, Y) in pts2:
                cnt[(X-i)**2 + (Y-j)**2] += 1
            for d2, c in cnt.items():
                if c in (9, 11, 12, 14, 16):
                    out.append((c, i, j, d2))
    return sorted(out)

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]]:
        res = dump(n)
        for c, i, j, d2 in res:
            print("n=%d pts=%d center=(%d/2,%d/2) d2=%d" % (n, c, i, j, d2))
        print("n=%d total: %d" % (n, len(res)))
