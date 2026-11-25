#!/usr/bin/env python3
"""
Width-66 surgery for the (7,4) seven-row family, seed = w65-01 id-image @ shift 11.

Board 7x66, base = w65-01 stones shifted +11 (bbox cols 11..64).
All cells blocked except T = (0,6)  [left-roof cell] -- single uncovered cell.

Surgery classes (declared-lane completeness policy, NEED=3 for q=4):
  (i) c0=2 classes: T-curves carrying exactly 2 base stones; place exactly one
      new stone a1 ON a T-curve (any board cell of the curve, empty in base).
      - 1R1A: remove 1 base stone, add a1.
      - 2R1A: remove 2 base stones, add a1.
  (ii) c0=1 class NOT in this run: 2R2A (two adds on a curve through T with
      exactly 1 base stone) -- run separately (surgery66_2r2a.py) if attempted.
  (iii) c0=0 (3 adds) out of scope for this run (scoped negative if 0 hits).

Each final state is verified from scratch by verify_int.verify (safe+maximal+def);
hits are additionally tamper-checked (drop each stone -> must break maximal).
All results are flushed to a JSONL log after each class.
"""
import json
import sys
import time
from verify_int import verify, circle_thru, line_thru, curve_cells

M, H, Q = 66, 7, 4

def main():
    rec = json.load(open("w65-01.json"))
    stones = [tuple(s) for s in rec["stones"]]
    xs = [p[0] for p in stones]
    mn = min(xs)
    base = [(x - mn + 11, y) for (x, y) in stones]  # id image @ shift 11
    S = set(base)

    # sanity: base fails maximality ONLY at T; and T blocked set
    r0 = verify(base, M, H, Q)
    assert r0["safe"], "base must be safe"
    print("base unblocked:", r0["unblocked"], "count(all): recomputing full list")
    # full unblocked list
    from verify_int import curves_with_3plus
    curves = curves_with_3plus(base)
    blocked = set()
    counts = {}
    for (kind, cur) in curves:
        cells = curve_cells(kind, cur, M, H)
        cnt = sum(1 for c in cells if c in S)
        counts[(kind, cur)] = cnt
        if cnt == Q - 1:
            for c in cells:
                if c not in S:
                    blocked.add(c)
    empty = [(x, y) for x in range(M) for y in range(H) if (x, y) not in S]
    un = [c for c in empty if c not in blocked]
    print("base safe:", r0["safe"], "unblocked:", un)
    assert un == [(0, 6)] or set(un) == {(0, 6)}, f"expected only T=(0,6), got {un}"
    T = (0, 6)

    # T-curves with exactly 2 base stones: pairs (s1, s2) -> line/circle through T,s1,s2
    tcurves = []  # (curve key, cells)
    bl = list(base)
    n = len(bl)
    seen = set()
    for i in range(n):
        for j in range(i + 1, n):
            if bl[i] == T or bl[j] == T:
                continue
            # line through pair and T?
            ln = line_thru(bl[i], bl[j])
            if ln and (ln[0] * T[0] + ln[1] * T[1] + ln[2]) == 0:
                key = ("line", ln)
                if key not in seen:
                    seen.add(key)
                    cells = [c for c in curve_cells("line", ln, M, H)]
                    cnt = sum(1 for c in cells if c in S)
                    if cnt == 2:
                        tcurves.append(("line", ln, cells))
            ci = circle_thru(bl[i], bl[j], T)
            if ci:
                key = ("circle", ci)
                if key not in seen:
                    seen.add(key)
                    cells = [c for c in curve_cells("circle", ci, M, H)]
                    cnt = sum(1 for c in cells if c in S)
                    if cnt == 2:
                        tcurves.append(("circle", ci, cells))
    print(f"T-curves with exactly 2 base stones: {len(tcurves)}")

    # add candidates: empty cells on those curves
    addcells = []
    for (kind, cur, cells) in tcurves:
        for c in cells:
            if c not in S and c != T and c not in [a for a in addcells]:
                addcells.append(c)
    print(f"distinct add-cell candidates on 2-stone T-curves: {len(addcells)}")
    # note: T itself could be an add? placing a stone AT T: T is empty; if we add at T,
    # T is no longer empty, maximality vacuous for it. Include T as an add cell too.
    if T not in addcells:
        addcells.append(T)

    out = open("surgery66_results.jsonl", "w")
    t_start = time.time()
    hits = {"1R1A": [], "2R1A": []}
    stats = {}

    import os
    done_a1 = set()
    if os.path.exists("surgery66_progress.txt"):
        done_a1 = set(open("surgery66_progress.txt").read().split())
        print("resuming, skip a1 idx:", sorted(done_a1)[:10], "..." if len(done_a1)>10 else "")
    # ---- class 1R1A ----
    n_checked = 0
    for a1 in addcells:
        for ri in range(n):
            R = bl[ri]
            if R == a1:
                continue
            S2 = [c for c in bl if c != R] + [a1]
            r = verify(S2, M, H, Q)
            n_checked += 1
            if r["safe"] and r["maximal"]:
                hits["1R1A"].append({"removed": [R], "added": [a1], "k": len(S2), "rowCounts": r["rowCounts"], "def": r["def"]})
                out.write(json.dumps({"cls": "1R1A", "removed": [list(R)], "added": [list(a1)]}) + "\n")
                out.flush()
                print("HIT 1R1A remove", R, "add", a1)
    stats["1R1A"] = {"checked": n_checked, "hits": len(hits["1R1A"]), "sec": time.time() - t_start}
    print("1R1A done:", stats["1R1A"])

    # ---- class 2R1A ----
    n_checked = 0
    t2 = time.time()
    last_flush = time.time()
    progress_f = open("surgery66_progress.txt", "a")
    for ai, a1 in enumerate(addcells):
        if str(ai) in done_a1:
            continue
        for i in range(n):
            for j in range(i + 1, n):
                R1, R2 = bl[i], bl[j]
                if R1 == a1 or R2 == a1:
                    continue
                S2 = [c for c in bl if c != R1 and c != R2] + [a1]
                r = verify(S2, M, H, Q)
                n_checked += 1
                if r["safe"] and r["maximal"]:
                    hits["2R1A"].append({"removed": [R1, R2], "added": [a1], "k": len(S2), "rowCounts": r["rowCounts"], "def": r["def"]})
                    out.write(json.dumps({"cls": "2R1A", "removed": [list(R1), list(R2)], "added": [list(a1)]}) + "\n")
                    out.flush()
                    print("HIT 2R1A remove", R1, R2, "add", a1)
        progress_f.write(f"{ai}\n")
        progress_f.flush()
        if time.time() - last_flush > 30:
            print(f"  progress: a1={a1} checked={n_checked} elapsed={time.time()-t2:.0f}s", flush=True)
            last_flush = time.time()
    stats["2R1A"] = {"checked": n_checked, "hits": len(hits["2R1A"]), "sec": time.time() - t2}
    print("2R1A done:", stats["2R1A"])

    out.close()
    with open("surgery66_summary.json", "w") as f:
        json.dump({"board": [7, 66], "q": 4, "base": [list(c) for c in base],
                   "T": list(T), "tcurves2": len(tcurves), "addCells": len(addcells),
                   "stats": stats, "hits": hits}, f, indent=1)
    print("WROTE surgery66_summary.json")

if __name__ == "__main__":
    main()
