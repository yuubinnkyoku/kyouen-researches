#!/usr/bin/env python3
"""Validate both C engines against a brute-force Python solver on tiny boards.

If the game is small enough (AG(2,2) s=1: 4 points / 6 lines; AG(2,3) s=2:
9 points / 12 lines) we can enumerate *every* subset and compute Grundy values
with a few lines of Python.  Running the published engine and our independent
engine on those boards and comparing all distributions exercises both
implementations on non-trivial cases that are checkable by inspection.

Writes small_ag22.txt / small_ag33.txt and small_*_expected.txt, then runs both
engines and compares.  Exit code 0 iff everything agrees.
"""
import itertools
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def make_ag(q):
    """AG(2,q) with points (x,y) -> y*q+x; lines x=c and y=m*x+c."""
    n = q * q
    lines = []
    for c in range(q):
        lines.append([y * q + c for y in range(q)])            # x = c
    for m in range(q):
        for c in range(q):
            lines.append([(m * x + c) % q * q + x for x in range(q)])  # y=mx+c
    return n, lines


def brute(q):
    n, lines = make_ag(q)
    s = q - 1
    lmask = [sum(1 << p for p in L) for L in lines]

    def safe(mask):
        return all(bin(mask & L).count("1") <= s for L in lmask)

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def g(mask):
        vals = set()
        for p in range(n):
            if mask >> p & 1:
                continue
            nm = mask | (1 << p)
            if safe(nm):
                vals.add(g(nm))
        m = 0
        while m in vals:
            m += 1
        return m

    size = {}
    gr = {}
    maximal = {}
    N = 0
    for mask in range(1 << n):
        if not safe(mask):
            continue
        N += 1
        k = bin(mask).count("1")
        v = g(mask)
        size.setdefault(k, [0, 0, 0])
        size[k][0] += 1
        if k == 0:
            size[k][2] += (v == 0)
        # maximal = no legal moves
        has_move = any(safe(mask | (1 << p)) for p in range(n)
                       if not (mask >> p & 1))
        if not has_move:
            size[k][1] += 1
            maximal[k] = maximal.get(k, 0) + 1
        if v == 0:
            size[k][2] += 1
        gr[v] = gr.get(v, 0) + 1
    # g0 column was counted twice above for k=0; rebuild cleanly
    for k in size:
        size[k][2] = 0
    gsize = {}
    for mask in range(1 << n):
        if not safe(mask):
            continue
        k = bin(mask).count("1")
        v = g(mask)
        gsize[(k, v)] = gsize.get((k, v), 0) + 1
        if v == 0:
            size[k][2] += 1
    maxk = max(size)
    first = {}
    root_children = [g(1 << p) for p in range(n) if safe(1 << p)]
    for v in root_children:
        first[v] = first.get(v, 0) + 1
    return dict(n=n, b=len(lines), s=s, lines=lines, size=size, grundy=gr,
                gsize=gsize, maximal=maximal, first=first, maxk=maxk,
                root=g(0), safe=N)


def write_board(path, spec):
    with open(path, "w", encoding="ascii", newline="\n") as f:
        f.write(f"{spec['n']} {spec['b']}\n")
        for L in spec["lines"]:
            f.write(f"{len(L)} " + " ".join(map(str, L)) + "\n")


def write_expected(path, spec):
    with open(path, "w", encoding="ascii", newline="\n") as f:
        f.write(f"POINTS {spec['n']}\nCIRCLES {spec['b']}\n")
        f.write(f"SAFE {spec['safe']}\nMAXSIZE {spec['maxk']}\n")
        f.write(f"ROOT {spec['root']}\n")
        for k in range(spec["maxk"] + 1):
            N, mx, g0 = spec["size"][k]
            f.write(f"SIZE {k} {N} {mx} {g0}\n")
        for v in sorted(spec["grundy"]):
            f.write(f"GRUNDY {v} {spec['grundy'][v]}\n")
        for (k, v) in sorted(spec["gsize"]):
            f.write(f"GSIZE {k} {v} {spec['gsize'][(k, v)]}\n")
        for k in sorted(spec["maximal"]):
            f.write(f"MAXIMAL {k} {spec['maximal'][k]}\n")
        for v in sorted(spec["first"]):
            f.write(f"FIRSTMOVE {v} {spec['first'][v]}\n")


def parse(path):
    d = {"size": {}, "grundy": {}, "gsize": {}, "maximal": {}, "first": {}}
    with open(path, encoding="utf-8") as f:
        for raw in f:
            t = raw.split()
            if not t:
                continue
            if t[0] == "SAFE":
                d["safe"] = int(t[1])
            elif t[0] == "MAXSIZE":
                d["maxsize"] = int(t[1])
            elif t[0] == "ROOT":
                d["root"] = int(t[1])
            elif t[0] == "SIZE":
                k, N, mx, g0 = map(int, t[1:5])
                d["size"][k] = (N, mx, g0)
            elif t[0] == "GRUNDY":
                d["grundy"][int(t[1])] = int(t[2])
            elif t[0] == "GSIZE":
                d["gsize"][(int(t[1]), int(t[2]))] = int(t[3])
            elif t[0] == "MAXIMAL":
                d["maximal"][int(t[1])] = int(t[2])
            elif t[0] == "FIRSTMOVE":
                d["first"][int(t[1])] = int(t[2])
    return d


failures = []
for q in (2, 3):
    spec = brute(q)
    tag = f"ag2{q}"
    board = os.path.join(HERE, f"small_{tag}.txt")
    expected_path = os.path.join(HERE, f"small_{tag}_expected.txt")
    write_board(board, spec)
    write_expected(expected_path, spec)
    print(f"{tag}: n={spec['n']} b={spec['b']} s={spec['s']} "
          f"safe={spec['safe']} maxk={spec['maxk']} root={spec['root']} "
          f"grundy={spec['grundy']}")

    expected = parse(expected_path)
    for exe in ("ag2q5_s4_independent.exe", "grundy_s_stats_published.exe"):
        out = os.path.join(HERE, f"small_{tag}_{exe.split('.')[0]}.txt")
        before = len(failures)
        with open(out, "wb") as fo, open(out + ".err", "wb") as fe:
            rc = subprocess.call([os.path.join(HERE, exe), board, str(spec["s"])],
                                 stdout=fo, stderr=fe)
        if rc != 0:
            failures.append(f"{tag}/{exe}: exit {rc}")
            continue
        got = parse(out)
        for key in ("safe", "root", "size", "grundy", "gsize", "first"):
            if got.get(key) != expected.get(key):
                failures.append(f"{tag}/{exe}: {key} mismatch "
                                f"(got {got.get(key)}, want {expected.get(key)})")
        # maximal counts: the published engine only prints them in the SIZE
        # column; ours also prints explicit MAXIMAL lines.
        got_max = got.get("maximal") or {}
        if exe.startswith("ag2q5"):
            if got.get("maxsize") != expected.get("maxsize"):
                failures.append(f"{tag}/{exe}: maxsize mismatch")
        else:
            got_max = {k: v[1] for k, v in got["size"].items() if v[1]}
        if got_max != expected.get("maximal"):
            failures.append(f"{tag}/{exe}: maximal mismatch "
                            f"(got {got_max}, want {expected.get('maximal')})")
        if len(failures) == before:
            print(f"  {exe}: agrees with brute force")

print()
if failures:
    print("SMALL-BOARD VALIDATION: FAIL")
    for f_ in failures:
        print("  -", f_)
    sys.exit(1)
print("SMALL-BOARD VALIDATION: PASS "
      "(both engines agree with brute force on AG(2,2) s=1 and AG(2,3) s=2)")
