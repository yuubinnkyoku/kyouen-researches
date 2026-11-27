"""Task 4: independent full census of caps of PG(2,8) up to size 10.

Depth-first extension: a cap is built by adding points in increasing board
index; the set of points forbidden for extension is the union of all lines
meeting the cap in >= 2 points.  Every cap is generated exactly once (by
removing its largest point).  Incidence is taken from the board file only.

Counts are kept for every size; only 9-cap and 10-cap point sets are stored.
Maximal 6-caps are counted (blocked set covers all points outside the cap).
"""
import json
import os
import pickle
import sys
import time

from pg8 import inc

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")


def census(maxsize=10):
    I = inc()
    lof = I.lof
    lmask = I.line_masks
    ALL = I.ALL
    cnt = [0] * (maxsize + 1)
    caps9 = []
    caps10 = []
    n_max6 = 0
    above = [ALL] * 74
    for l in range(73):
        above[l + 1] = ALL & ~((1 << (l + 1)) - 1)

    t0 = time.time()

    def dfs(last, capmask, blocked, caplist):
        nonlocal n_max6
        size = len(caplist)
        cnt[size] += 1
        if size == 9:
            caps9.append(capmask)
        if size == 10:
            caps10.append(capmask)
            return
        if size == 6 and (blocked | capmask) == ALL:
            n_max6 += 1
        avail = above[last + 1] & ~blocked
        while avail:
            b = avail & -avail
            avail ^= b
            q = b.bit_length() - 1
            nb = blocked
            for p in caplist:
                nb |= lmask[lof[p][q]]
            caplist.append(q)
            dfs(q, capmask | b, nb, caplist)
            caplist.pop()

    dfs(-1, 0, 0, [])
    return cnt, caps9, caps10, n_max6, round(time.time() - t0, 2)


def main():
    maxsize = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    os.makedirs(ART, exist_ok=True)
    cnt, caps9, caps10, n_max6, secs = census(maxsize)
    print("counts by size (size: count):")
    for s in range(1, maxsize + 1):
        print(f"  {s}: {cnt[s]}")
    print("maximal 6-caps:", n_max6)
    print("seconds:", secs)
    out = {"counts": {str(s): cnt[s] for s in range(1, maxsize + 1)},
           "n_maximal6": n_max6, "seconds": secs, "maxsize": maxsize}
    tag = "" if maxsize == 10 else f"_upto{maxsize}"
    with open(os.path.join(ART, f"census{tag}.json"), "w") as f:
        json.dump(out, f, indent=1)
    if maxsize == 10:
        with open(os.path.join(ART, "caps.pkl"), "wb") as f:
            pickle.dump({"caps9": caps9, "caps10": caps10}, f)
    return out


if __name__ == "__main__":
    main()
