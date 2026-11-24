#!/usr/bin/env python3
"""Validate the C census programs against exhaustive brute force on small planes.

Builds PG(2,3) (13 points, 13 lines of 4) and AG(2,3) / AG(2,4), brute-forces
every subset, and compares the size distribution and the maximal-cap counts
with the output of cap_census and cap_census_alt.
"""
import itertools
import json
import os
import subprocess
import sys


def gf_mul_q(q, a, b):
    """multiplication in GF(q) for prime q (elements 0..q-1)."""
    return (a * b) % q


def build_pg(q):
    pts = []
    for v in itertools.product(range(q), repeat=3):
        if v == (0, 0, 0):
            continue
        for c in v:
            if c != 0:
                inv = pow(c, q - 2, q)
                pts.append(tuple((x * inv) % q for x in v))
                break
    pts = sorted(set(pts))
    pindex = {p: i for i, p in enumerate(pts)}
    funcs = set()
    for f in itertools.product(range(q), repeat=3):
        if f == (0, 0, 0):
            continue
        for c in f:
            if c != 0:
                inv = pow(c, q - 2, q)
                funcs.add(tuple((x * inv) % q for x in f))
                break
    lines = []
    for f in sorted(funcs):
        L = [pindex[p] for p in pts
             if sum(gf_mul_q(q, a, b) for a, b in zip(f, p)) % q == 0]
        lines.append(sorted(L))
    return pts, lines


def build_ag(q):
    pts = [(x, y) for x in range(q) for y in range(q)]
    pindex = {p: i for i, p in enumerate(pts)}
    lines = []
    for m in range(q):
        for c in range(q):
            lines.append(sorted(pindex[(x, (m * x + c) % q)] for x in range(q)))
    for c in range(q):
        lines.append(sorted(pindex[(c, y)] for y in range(q)))
    return pts, lines


def write_board(path, n, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{n} {len(lines)}\n")
        for L in lines:
            f.write(f"{len(L)} " + " ".join(str(p) for p in L) + "\n")


def brute_force(n, lines):
    masks = []
    for L in lines:
        m = 0
        for p in L:
            m |= 1 << p
        masks.append(m)
    sizes = [0] * (n + 2)
    maxs = [0] * (n + 2)
    for sub in range(1 << n):
        ok = True
        for m in masks:
            if bin(sub & m).count("1") > 2:
                ok = False
                break
        if not ok:
            continue
        k = bin(sub).count("1")
        sizes[k] += 1
        addable = False
        for q in range(n):
            if (sub >> q) & 1:
                continue
            good = True
            for m in masks:
                if (m >> q) & 1 and bin(sub & m).count("1") >= 2:
                    good = False
                    break
            if good:
                addable = True
                break
        if not addable:
            maxs[k] += 1
    return sizes, maxs


def run_and_parse(exe, board):
    out = board + "." + os.path.basename(exe) + ".out"
    with open(out, "w", encoding="utf-8") as f:
        subprocess.run([exe, board], stdout=f, check=True)
    sizes, maxs = {}, {}
    total = None
    with open(out, encoding="utf-8") as f:
        for ln in f:
            t = ln.split()
            if t and t[0] == "SIZE":
                sizes[int(t[1])] = int(t[2])
                maxs[int(t[1])] = int(t[3])
            elif t and t[0] == "TOTAL":
                total = int(t[1])
    return sizes, maxs, total, out


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs("testdata", exist_ok=True)
    cases = []
    cases.append(("pg23", *build_pg(3)))
    cases.append(("ag23", *build_ag(3)))
    # NB: AG(2,4)/PG(2,4) are not included because build_ag/build_pg use Z/q
    # arithmetic, which is only a field for prime q.
    failures = 0
    for name, pts, lines in cases:
        n = len(pts)
        path = os.path.join("testdata", name + ".txt")
        write_board(path, n, lines)
        esizes, emaxs = brute_force(n, lines)
        print(f"=== {name}: n={n}, lines={len(lines)}, "
              f"line sizes={sorted({len(L) for L in lines})} ===")
        print(f"  brute force total = {sum(esizes)}")
        print(f"  brute force sizes = {[esizes[k] for k in range(n + 1) if esizes[k]]}")
        print(f"  brute force max   = {[ (k, emaxs[k]) for k in range(n + 1) if emaxs[k]]}")
        for exe in ("./cap_census.exe", "./cap_census_alt.exe"):
            sizes, maxs, total, out = run_and_parse(exe, path)
            ok = True
            for k in range(n + 2):
                if sizes.get(k, 0) != esizes[k]:
                    ok = False
                    print(f"  FAIL {exe}: size {k}: {sizes.get(k,0)} != {esizes[k]}")
                if maxs.get(k, 0) != emaxs[k]:
                    ok = False
                    print(f"  FAIL {exe}: maximal {k}: {maxs.get(k,0)} != {emaxs[k]}")
            if total != sum(esizes):
                ok = False
                print(f"  FAIL {exe}: total {total} != {sum(esizes)}")
            print(f"  {'PASS' if ok else 'FAIL'}  {exe}  (log {out})")
            if not ok:
                failures += 1
    print()
    print(f"RESULT: {'PASS' if failures == 0 else 'FAIL'} ({failures} failures)")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
