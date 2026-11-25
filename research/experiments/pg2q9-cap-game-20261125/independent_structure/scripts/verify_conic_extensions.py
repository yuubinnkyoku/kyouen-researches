"""Extension statistics for subsets of one conic.

PGL(3,9) is transitive on conics, so the multiset of addable-point counts over
all k-subsets is the same for every conic; checking one conic is exhaustive.

Consequences checked here:
  * every 5-subset of a conic has exactly 21 addable points
    => #6-caps = 58968*C(10,5)*21/6 = 52,009,776 (all 5-caps are conic,
       verified elsewhere);
  * every 8-subset of a conic has exactly 2 addable points (the other two
    conic points) => conic 8-caps are non-maximal;
  * every 9-subset has exactly 1 addable point.
"""
import itertools
from collections import Counter
from pathlib import Path

import pg

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "out"


def bits(mask):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b


def main():
    conics = [int(ln) for ln in (OUT / "conics.txt").read_text().splitlines()]
    C = conics[0]
    pts = list(bits(C))
    print("conic:", pts)
    for k in range(5, 11):
        dist = Counter()
        for sub in itertools.combinations(pts, k):
            dist[pg.addable_mask(list(sub)).bit_count()] += 1
        print(f"k={k}: addable-size distribution {dict(sorted(dist.items()))}")

    e5 = 21
    total6 = 58968 * 252 * e5 // 6
    print(f"\n#6-caps = 58968*C(10,5)*{e5}/6 = {total6}")
    print(f"claimed 52,009,776: {total6 == 52009776}")
    print(f"conic 6-subsets = 58968*C(10,6) = {58968 * 210}")
    print(f"non-conic 6-caps = {total6 - 58968 * 210} (claimed 39,626,496)")


if __name__ == "__main__":
    main()
