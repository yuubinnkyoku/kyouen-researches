"""Search for maximal 6-, 7-, 8-caps and verify their defining properties.

Random greedy caps stopped at the target size; a maximal target cap is one
with no addable points.  Maximal 6/7/8 caps must be non-conic (a conic
6/7/8-cap has 4/3/2 addable conic points).
"""
import random
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


def random_cap_of_size(rng, size):
    p = rng.randrange(91)
    cap = [p]
    add = pg.FULL & ~(1 << p)
    while len(cap) < size and add:
        q = rng.choice(list(bits(add)))
        cap.append(q)
        for a in cap[:-1]:
            add &= ~pg.line_mask(a, q)
        add &= ~(1 << q)
    return sorted(cap)


def main():
    conics = set(int(ln) for ln in (OUT / "conics.txt").read_text().splitlines())
    rng = random.Random(42456960)
    for size in (6, 7, 8):
        found = None
        counts = Counter()
        trials = 0
        while found is None and trials < 300000:
            trials += 1
            cap = random_cap_of_size(rng, size)
            if len(cap) != size:
                continue
            e = pg.addable_mask(cap)
            counts[e.bit_count()] += 1
            if e == 0:
                found = cap
                break
        print(f"size {size}: trials={trials}, addable-count distribution of "
              f"sampled {size}-caps: {dict(sorted(counts.items()))}")
        if found:
            m = 0
            for p in found:
                m |= 1 << p
            print(f"  found maximal {size}-cap: {found}")
            print(f"  is_cap={pg.is_cap(found)} addable={pg.addable_mask(found)} "
                  f"conic={m in conics}")
        else:
            print(f"  no maximal {size}-cap found")


if __name__ == "__main__":
    main()
