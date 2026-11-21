# d_count.py — independent collinear-quartet counter D_n (v2).
# Primitive directions (a,b), gcd(|a|,|b|)=1, (a,b) != (0,0), normalized to the upper half:
#   a >= 1, b in {-(n-1)..n-1}, plus (0,1). Each maximal grid line in such a direction is a ray
# starting where the predecessor (x-a, y-b) is off the board. Integer points on a line with
# primitive direction form one contiguous run in k, so each quartet is counted exactly once.
# No circle machinery is used anywhere (fully independent of census_a). fix v2: v1 forgot
# negative slopes (a,-b), e.g. n=7 missed 660-575=85 = dir (1,-1)+(1,-2)+(2,-1) shares.
import sys
from math import gcd

def D_n(n):
    total = 0
    per_dir = {}
    dirs = [(0, 1), (1, 0)]
    for a in range(1, n):
        for b in range(-(n - 1), n):
            if b == 0 or gcd(a, abs(b)) != 1:
                continue
            dirs.append((a, b))
    for (a, b) in dirs:
        s = 0
        for x in range(n):
            for y in range(n):
                px, py = x - a, y - b
                if 0 <= px < n and 0 <= py < n:
                    continue
                kx = (n - 1 - x) // a if a > 0 else 10**9
                if b > 0:
                    ky = (n - 1 - y) // b
                elif b < 0:
                    ky = y // (-b)
                else:
                    ky = 10**9
                l = 1 + min(kx, ky)
                if l >= 4:
                    s += l * (l - 1) * (l - 2) * (l - 3) // 24
        if s:
            per_dir[(a, b)] = s
        total += s
    return total, per_dir

if __name__ == "__main__":
    pub = {7: 660, 8: 1524, 9: 3156}  # published anchors (census D columns n=7..9)
    for n in [int(a) for a in sys.argv[1:]]:
        d, pd = D_n(n)
        top = sorted(pd.items(), key=lambda kv: -kv[1])[:10]
        tag = ""
        if n in pub:
            tag = "  PUBLISHED=%d  %s" % (pub[n], "MATCH" if d == pub[n] else "MISMATCH")
        print("n=%d D_n=%d%s  top dirs: %s" % (n, d, tag, top))
