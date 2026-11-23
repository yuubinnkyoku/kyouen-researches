"""Enumerate F_p-linear maps as graph arcs:  S = { (a, f(a)) : a in F_q }.

For q = p^e the F_p-linear maps f: F_q -> F_q are exactly the e x e matrices over
F_p, a small algebraically meaningful family (for q=16 there are 65536 of them).
A single hit gives a q-point arc, i.e. K(q) >= q, matching the upper bound of
K1252 and leaving the (q+5)/2 construction far behind.

Run:  python graph_fp_linear.py --q 8 9 25 27
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from inversive_fast import build_circles  # noqa: E402
from arc_lift_verify import Lift  # noqa: E402
from inversive_prime_power import factorize  # noqa: E402


def power(F, a, n):
    r = None
    for _ in range(n):
        r = a if r is None else F.mul(r, a)
    if r is None:
        r = F.sub(a, a)          # a^0 is 1; handled by caller normally
    return r


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    args = ap.parse_args()

    for q in args.q:
        fact = factorize(q)
        if len(fact) != 1:
            print(f"q={q}: not a prime power")
            continue
        p, e = fact[0]
        total = p ** (e * e)
        if total > 300000:
            print(f"q={q}: {total} F_p-linear maps, too many; skipped")
            continue
        lift = Lift(q)
        F, sub = build_field(q)
        points, blocks = build_circles(q, check_orbit_size=True)
        one = F.pow(list(sub)[0], 0)
        zero = F.sub(one, one)
        coord_index = {}
        for i, z in enumerate(points):
            if z is None:
                continue
            v = lift.coords(z)
            coord_index[(v[1], v[2])] = i
        sub_list = list(sub)

        # basis {1, g, ..., g^(e-1)} for a g of degree e over F_p
        def coords_in_basis(a, basis):
            # brute force over F_p^e
            for vec in range(p ** e):
                v = vec
                acc = zero
                for i in range(e):
                    d = v % p
                    v //= p
                    for _ in range(d):
                        acc = F.add(acc, basis[i])
                if acc == a:
                    digits = [(vec // (p ** i)) % p for i in range(e)]
                    return True, digits
            return False, None

        basis = None
        for g in sub_list:
            if g == one or g == zero:
                continue
            cand = []
            cur = one
            for _ in range(e):
                cand.append(cur)
                cur = F.mul(cur, g)
            ok = all(coords_in_basis(a, cand)[0] for a in sub_list)
            if ok:
                basis = cand
                break
        if basis is None:
            print(f"q={q}: no basis found")
            continue
        coords = {a: coords_in_basis(a, basis)[1] for a in sub_list}

        cmasks = []
        for B in blocks:
            mask = 0
            for pt in B:
                mask |= 1 << pt
            cmasks.append(mask)

        hits = 0
        first = None
        for mat in range(total):
            entries = []
            v = mat
            for _ in range(e * e):
                entries.append(v % p)
                v //= p
            images = []
            for j in range(e):
                img = zero
                for i in range(e):
                    for _ in range(entries[i * e + j]):
                        img = F.add(img, basis[i])
                images.append(img)
            S = 0
            ok = True
            for a in sub_list:
                c = coords[a]
                fa = zero
                for j in range(e):
                    for _ in range(c[j]):
                        fa = F.add(fa, images[j])
                key = (a, fa)
                if key not in coord_index:
                    ok = False
                    break
                pt = coord_index[key]
                if (S >> pt) & 1:
                    ok = False
                    break
                S |= 1 << pt
            if not ok:
                continue
            if all(bin(S & m).count("1") < 4 for m in cmasks):
                hits += 1
                if first is None:
                    first = entries
        print(f"q={q}: F_p-linear graph arcs: {hits} of {total} maps"
              + (f"  (first matrix {first})" if first else ""), flush=True)


if __name__ == "__main__":
    main()
