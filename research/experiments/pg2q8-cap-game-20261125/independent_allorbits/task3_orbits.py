"""TASK 3 -- PGL(3,8) orbit sizes of the four K1327 start caps.

Each orbit is computed twice: once by the C engine (pg8.exe, hash-set BFS over
73-bit masks) and once here in pure Python (byte-chunk table BFS).  Both are
compared with the K1327 values.
"""

import sys
import time

import pg2q8 as P
import pgl_act as A

STARTS = [
    ("cap7", [12, 16, 18, 22, 54, 66, 69], 2747136),
    ("cap8", [12, 16, 18, 22, 40, 54, 66, 69], 1177344),
    ("cap6_nm", [1, 10, 12, 59, 62, 65], 4120704),
    ("cap6_max", [10, 47, 49, 55, 61, 64], 686784),
]


def parse_kv(lines):
    """parse 'tag [name] key=value ...' C output lines"""
    out = []
    for ln in lines:
        toks = ln.split()
        if not toks:
            continue
        d = {"tag": toks[0], "arg": toks[1] if len(toks) > 1 and "=" not in toks[1] else ""}
        for t in toks:
            if "=" in t:
                k, v = t.split("=", 1)
                d[k] = v
        out.append(d)
    return out


def read_c_results(path="results_c.txt"):
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    return parse_kv(lines)


def main():
    out = []

    def say(s=""):
        out.append(str(s))
        print(s)

    canon = P.canonical_lines()

    # ---------------------------------------------------------------- start caps
    say("== start caps ==")
    caps = {}
    for name, pts, expect in STARTS:
        m = A.mask_of(pts)
        cap = P.is_cap(pts)
        # collinearity via the board lines: any board line containing 3 points?
        coll = False
        for L in canon:
            if sum(1 for p in pts if p in L) >= 3:
                coll = True
                break
        # extendable?
        ext = []
        for q in range(73):
            if q in pts:
                continue
            if P.is_cap(pts + [q]):
                ext.append(q)
        caps[name] = (m, pts, expect)
        say(f"{name}: {sorted(pts)}")
        say(f"  is_cap(3-collinear-free)={cap} no_line_has_3={not coll} "
            f"extendable={bool(ext)} (#extensions={len(ext)})")

    # ---------------------------------------------------------------- C results
    say()
    say("== C engine orbit sizes ==")
    cvals = {}
    try:
        for d in read_c_results():
            if d["tag"] == "start":
                cvals[d["arg"]] = int(d["size"])
                say(f"  C: {d['arg']:9s} size={d['size']:>10s} "
                    f"is_cap={d.get('is_cap')} is_max={d.get('is_max')} "
                    f"in_conic={d.get('in_conic')}")
    except FileNotFoundError:
        say("  (results_c.txt not found; run pg8.exe all first)")

    # ---------------------------------------------------------------- Python BFS
    say()
    say("== pure-Python orbit BFS (independent implementation) ==")
    tables = A.generator_tables()
    ok = True
    results = []
    for name, pts, expect in STARTS:
        m = A.mask_of(pts)
        t0 = time.time()
        n = A.orbit_size(tables, m)
        dt = time.time() - t0
        cval = cvals.get(name)
        good = (n == expect) and (cval in (None, expect))
        ok = ok and good
        results.append((name, n, expect, cval))
        say(f"  {name:9s} python={n:>9d} C={str(cval):>9s} K1327={expect:>9d} "
            f"{'OK' if good else 'MISMATCH'}  ({dt:.1f}s)")

    # classification of the start caps (conic layer membership)
    say()
    say("== classification ==")
    conic = None
    for pts, expect in [((12, 16, 18, 22, 54, 66, 69), None)]:
        pass
    # conic via the quadratic form x0^2 + x1*x2
    conic_pts = []
    for i, v in enumerate(P.POINTS):
        if (P.gf_mul(v[0], v[0]) ^ P.gf_mul(v[1], v[2])) == 0:
            conic_pts.append(i)
    conic = A.mask_of(conic_pts)
    say(f"standard conic (x0^2+x1*x2=0): {sorted(conic_pts)} "
        f"size={len(conic_pts)} is_cap={P.is_cap(conic_pts)}")
    for name, pts, expect in STARTS:
        m = A.mask_of(pts)
        sub = (m & conic) == m
        say(f"  {name:9s} contained_in_standard_conic={sub}")

    good = ok
    say()
    say(f"TASK 3: {'PASS' if good else 'FAIL'}")
    with open("results_task3.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
