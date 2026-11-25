"""Task 3: concrete cap checks.

(a) find a non-conic 8-cap and verify it is maximal (0 addable points);
(b) the specified 7-cap {11,22,29,32,44,61,89}: cap? conic? maximal?
(c) a conic 9-cap is non-maximal and contained in a conic 10-cap;
(d) a conic 10-cap is maximal.
Also samples conic 8-caps: non-maximal, extensions are exactly the other conic points.
"""
import itertools
import random
import time
from pathlib import Path

import pg

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "out"


def load_conics():
    return [int(ln) for ln in (OUT / "conics.txt").read_text().splitlines()]


def mask_of(points):
    m = 0
    for p in points:
        m |= 1 << p
    return m


def bits(mask):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b


def addable_mask(points):
    return pg.addable_mask(points)


def conics_containing(points, conics):
    cm = mask_of(points)
    return [c for c in conics if c & cm == cm]


def describe_cap(points, conics):
    pts = sorted(points)
    cap = pg.is_cap(pts)
    ext = addable_mask(pts)
    cont = conics_containing(pts, conics) if cap else []
    print(f"  points={pts}")
    print(f"  size={len(pts)} cap={cap} conic={bool(cont)} "
          f"#containing_conics={len(cont)}")
    print(f"  addable={list(bits(ext))} (#{ext.bit_count()}) maximal={ext == 0}")
    return cap, cont, ext


def greedy_cap2(rng):
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
    t0 = time.time()
    conics = load_conics()
    print(f"loaded {len(conics)} conics")
    # data-file conic representative
    rep = [0, 1, 10, 20, 31, 45, 51, 62, 75, 88]
    repm = mask_of(rep)
    print(f"conic_layer.json representative {rep}: in conic list = {repm in conics}")
    print(f"  is cap = {pg.is_cap(rep)}")

    # ---------- (b) specified 7-cap ----------
    print("\n(b) specified 7-cap {11,22,29,32,44,61,89}")
    cap7 = [11, 22, 29, 32, 44, 61, 89]
    okb = describe_cap(cap7, conics)
    ext = addable_mask(cap7)

    # extend the 7-cap by addable points; look for a maximal non-conic 8-cap
    found8 = None
    for q in bits(ext):
        pts = sorted(cap7 + [q])
        if len(pts) != 8 or not pg.is_cap(pts):
            continue
        e = addable_mask(pts)
        cont = conics_containing(pts, conics)
        print(f"  extension by {q}: 8-cap, conic={bool(cont)}, "
              f"addable={list(bits(e))} (#{e.bit_count()}), maximal={e == 0}")
        if e == 0 and not cont and found8 is None:
            found8 = pts
    if found8 is None:
        # random greedy search
        rng = random.Random(20261125)
        for trial in range(20000):
            pts = greedy_cap2(rng)
            if len(pts) == 8 and not conics_containing(pts, conics):
                e = addable_mask(pts)
                if e == 0:
                    found8 = pts
                    print(f"  random greedy trial {trial}: maximal non-conic 8-cap {pts}")
                    break
        else:
            print("  random greedy failed to find a maximal non-conic 8-cap")
    if found8:
        print(f"  using non-conic maximal 8-cap: {found8}")
        # verify directly: all 7-subsets are caps; none conic; each has exactly
        # the removed point addable?  (structural aside)
        for removed in found8:
            sub = [x for x in found8 if x != removed]
            cont = conics_containing(sub, conics)
            e = addable_mask(sub)
            print(f"    subset minus {removed}: conic={bool(cont)} "
                  f"addable={list(bits(e))} (#{e.bit_count()})")

    # ---------- (c),(d) conic 10-cap and its 9-subsets ----------
    print("\n(c),(d) conic 10-cap and 9-subset")
    C = conics_containing(rep, conics)
    cmask = C[0]
    Cpts = list(bits(cmask))
    print(f"  conic {Cpts}")
    print(f"  conic is cap={pg.is_cap(Cpts)} addable={addable_mask(Cpts)} "
          f"maximal={addable_mask(Cpts) == 0}")
    nine = Cpts[:-1]
    rem = Cpts[-1]
    e9 = addable_mask(nine)
    print(f"  9-subset {nine} (removed {rem}): cap={pg.is_cap(nine)} "
          f"conic={bool(conics_containing(nine, conics))} "
          f"addable={list(bits(e9))} (#{e9.bit_count()}) maximal={e9 == 0} "
          f"removed_addable={(e9 >> rem) & 1}")

    # conic 8-subsets
    cont_nonmax = 0
    for k in range(3):
        pass
    print("\n  sample conic 8-subsets:")
    for drop in itertools.combinations(range(10), 2):
        eight = [Cpts[i] for i in range(10) if i not in drop]
        e = addable_mask(eight)
        cont = conics_containing(eight, conics)
        assert pg.is_cap(eight)
        assert cont
        print(f"    drop {drop}: addable={list(bits(e))} (#{e.bit_count()}) maximal={e == 0}")
        if e != 0:
            cont_nonmax += 1
    print(f"  non-maximal conic 8-subsets: {cont_nonmax}/45")

    print(f"\ntotal time {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
