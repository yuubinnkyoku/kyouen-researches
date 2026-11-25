"""Sampling/structural checks around maximal 8-caps.

* random greedy maximal caps; retain size-8 maximal caps (non-conic);
* verify every 7-subset of such an 8-cap has exactly one addable point
  (the removed one) -- so distinct maximal 8-caps in the sample do not share
  7 points.  Note: addable count 1 already implies the 7-subset is non-conic,
  since any conic 7-subset would have its 3 other conic points addable.
* verify the conic secant/tangent count used in the proof that a maximal
  8-cap cannot contain a conic 7-subset: for an external point of a conic,
  exactly 4 secants and 2 tangents.
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


def load_conics():
    return [int(ln) for ln in (OUT / "conics.txt").read_text().splitlines()]


def greedy_max_cap(rng):
    p = rng.randrange(91)
    cap = [p]
    add = pg.FULL & ~(1 << p)
    while add:
        q = rng.choice(list(bits(add)))
        cap.append(q)
        for a in cap[:-1]:
            add &= ~pg.line_mask(a, q)
        add &= ~(1 << q)
    return sorted(cap)


def main():
    conics = load_conics()
    rng = random.Random(1331)
    n8 = 0
    dist = Counter()
    bad_addable = 0
    bad_point = 0
    trials = 0
    while n8 < 5000 and trials < 200000:
        trials += 1
        cap = greedy_max_cap(rng)
        if len(cap) != 8:
            continue
        n8 += 1
        for a in cap:
            sub = [x for x in cap if x != a]
            e = pg.addable_mask(sub)
            dist[e.bit_count()] += 1
            if e.bit_count() != 1:
                bad_addable += 1
            if e != (1 << a):
                bad_point += 1
    print(f"trials={trials} maximal 8-caps sampled={n8}")
    print(f"7-subset addable-count distribution: {dict(sorted(dist.items()))}")
    print(f"bad addable count (!=1): {bad_addable}")
    print(f"bad addable point (!= removed point): {bad_point}")
    print(f"MAX8_STRUCTURE: {'PASS' if not (bad_addable or bad_point) else 'FAIL'}")

    # external point secant/tangent counts on a conic
    C = conics[0]
    Cpts = set(bits(C))
    ext_counts = Counter()
    for p in range(91):
        if p in Cpts:
            continue
        sec = tan = ext = 0
        for lm in pg.LINES:
            if (lm >> p) & 1:
                n = (lm & C).bit_count()
                if n == 2:
                    sec += 1
                elif n == 1:
                    tan += 1
                else:
                    ext += 1
        ext_counts[(sec, tan, ext)] += 1
    print(f"external-point line-type counts (secants,tangents,external): "
          f"{dict(ext_counts)}")


if __name__ == "__main__":
    main()
