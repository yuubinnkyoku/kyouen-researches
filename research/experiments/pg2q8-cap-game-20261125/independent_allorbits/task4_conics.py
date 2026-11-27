"""TASK 4 -- conic orbits.

Two independent computations:
  (a) the number of conics: 32,704 = |PGL(3,8)|/|PGL(2,8)| = 16,482,816/504,
      computed as the PGL orbit of one conic;
  (b) for k = 5..9, the PGL orbit of a k-subset of one conic.  If its size is
      32,704*C(9,k) then the conic k-subsets form a single orbit.
(b) is done by the C engine for every k and re-done here in pure Python for
k = 8, 9 (the smaller ones) as a cross-check.
"""

import math
import sys
import time

import pg2q8 as P
import pgl_act as A
import parse_out

CLAIM = {6: 2747136, 7: 1177344, 8: 294336, 9: 32704}


def main():
    out = []

    def say(s=""):
        out.append(str(s))
        print(s)

    nconics = 32704
    tables = A.generator_tables()

    # ------------------------------------------------------------- the conic
    say("== the standard conic Q = x0^2 + x1*x2 ==")
    conic_pts = [i for i, v in enumerate(P.POINTS)
                 if (P.gf_mul(v[0], v[0]) ^ P.gf_mul(v[1], v[2])) == 0]
    conic = A.mask_of(conic_pts)
    say(f"points: {sorted(conic_pts)}")
    say(f"size={len(conic_pts)} is_cap={P.is_cap(conic_pts)}")
    # every pair on a distinct secant, no three collinear (already is_cap)
    say("zero set size = q+1 = 9 and no three collinear -> non-degenerate conic")

    say()
    say("== number of conics ==")
    t0 = time.time()
    n = A.orbit_size(tables, conic)
    say(f"Python orbit of the 9-point conic: {n}  ({time.time()-t0:.1f}s)")
    say(f"|PGL(3,8)|/|PGL(2,8)| = 16482816/504 = {16482816//504}")
    say(f"quadratic-form census (C engine) should give 32704 distinct conics")

    say()
    say("== conic k-subsets: C engine ==")
    cvals = {}
    quads = {}
    for d in parse_out.read("results_c.txt"):
        for k in range(5, 10):
            key = f"conic_orbit_k{k}"
            if key in d:
                cvals[k] = int(d[key])
        for key in ("quads_forms_up_to_scalar", "quads_with_9point_arc_zeros",
                    "quads_distinct_conics"):
            if key in d:
                quads[key] = int(d[key])
    ok = True
    for k in range(5, 10):
        want = nconics * math.comb(9, k)
        got = cvals.get(k)
        good = got == want
        ok = ok and good
        say(f"  k={k}: C orbit={str(got):>9s}  32704*C(9,{k})={want:>9d}  "
            f"{'OK' if good else 'MISMATCH'}")
    if quads:
        say(f"  quadratic forms up to scalar: {quads.get('quads_forms_up_to_scalar')}")
        say(f"  forms whose zero set is a 9-arc: {quads.get('quads_with_9point_arc_zeros')}")
        say(f"  distinct conics: {quads.get('quads_distinct_conics')} "
            f"(= forms / 7: {'OK' if quads.get('quads_distinct_conics') == quads.get('quads_with_9point_arc_zeros') else 'MISMATCH'})")
        ok = ok and quads.get("quads_distinct_conics") == nconics

    say()
    say("== conic k-subsets: pure-Python cross-check (k=8,9) ==")
    pvals = {}
    for k in (8, 9):
        start = A.mask_of(sorted(conic_pts)[:k])
        t0 = time.time()
        sz = A.orbit_size(tables, start)
        dt = time.time() - t0
        pvals[k] = sz
        want = nconics * math.comb(9, k)
        say(f"  k={k}: python orbit={sz:>9d}  expected={want:>9d}  "
            f"{'OK' if sz == want else 'MISMATCH'}  ({dt:.1f}s)")

    say()
    say("== K1327 claims for the conic layer ==")
    for k in (6, 7, 8, 9):
        want = nconics * math.comb(9, k)
        good = (cvals.get(k) == CLAIM[k] == want)
        ok = ok and good
        say(f"  k={k}: claim={CLAIM[k]:>9d} computed={str(cvals.get(k)):>9s} "
            f"32,704*C(9,{k})={want:>9d}  {'OK' if good else 'MISMATCH'}")
    say(f"  number of conics claim: 32,704 = computed {n}  "
        f"{'OK' if n == nconics else 'MISMATCH'}")
    ok = ok and (n == nconics)

    say()
    say(f"TASK 4: {'PASS' if ok else 'FAIL'}")
    with open("results_task4.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
