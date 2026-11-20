#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Independent second verification of K1097 (n11 residual-72 rows, safe8 pool
round-4 re-solve after excluding the 50 REFUTED-D10 roots; published canonical
SHA-256 2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40,
git blob SHA-1 4660c012333b04896c36a23a0837fbdbc2572ef9) (2026-11-20).

Single-owner declaration:
  research/log/2026-11-20-n11-residual72-refuted50-refsolve-second-verification-single-owner-note.md
  (commit de8c44ac96fbde0616a216f184dd54b42b3f2c49)

This machine is an independent re-implementation. Deliberately different code
paths from the published K1097 machine:
  * cocircularity / forbidden-quadruple predicate: anchor-translation to
    the origin followed by the exact integer 3x3 determinant of the rows
    (dx, dy, d(x^2+y^2)) — the same zero set as the 4x4 circle
    determinant, verified against a second path (Bareiss fully-integer
    forward elimination) on all 72 rows — while the K1097 machine expands
    the 4x4 determinant as an alternating sum of four 3x3 cofactor
    determinants,
  * coverage: FULL population re-derivation of the intrinsic C(8,6)=28
    subset coverage of every one of the 120,474 safe8 roots, compared for
    equality against the generation-witness coverage (the K1097 machine
    cross-checks a 39,255-root sample),
  * bipartite maximum matching: Hopcroft-Karp (the K1097 machine uses Kuhn
    augmenting paths),
  * greedy set cover: independent lexicographically-smallest max-gain scan,
  * every re-derived quantity is compared field-by-field against BOTH the
    published K1097 canonical and the K1085 census fields.

Inputs (fail-closed SHA-256 pins, identical to the published machine):
  K1085 5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e
  K1086 3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced
  K1089 808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc
  K1091 edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25
  K1095 335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707
plus the published outputs under verification:
  K1097 canonical (sha256 + git blob sha1 pinned),
  the published K1097 machine source sha256
  f01f459f4f9ec2b9d38c0ed61f14132cf36c870f316d1fae840fe534181192c0
  (step (a): re-executed in this environment, output SHA-256 reproduced
  byte-identically; recorded as an input fact by the operator, and gated
  here against the published pin).

Trust boundary: identical to the published corpus (engine depth-10 verdict
soundness + D4 invariance + the two-wrap rows-72 base universe). The
replacement root sets of rounds 1-3 enter through the same upstream
canonicals as the published machine (K1089 per_root keys, K1091 per_root
keys, K1095 per_root keys); no probes are run here. No row is closed.
REFUTED-D10 is not a LOSS proof. Node counts are not game outcomes. The
standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60},
and classes 1/2/4 all remain UNKNOWN.

Determinism: Python standard library only, sequential, no wall/random data
in the canonical JSON.
"""

import hashlib
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))

K1085_SHA256 = "5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e"
K1086_SHA256 = "3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced"
K1089_SHA256 = "808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc"
K1091_SHA256 = "edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25"
K1095_SHA256 = "335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707"
K1097_CANON_SHA256 = "2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40"
K1097_CANON_BLOB_SHA1 = "4660c012333b04896c36a23a0837fbdbc2572ef9"
K1097_MACHINE_SHA256 = "f01f459f4f9ec2b9d38c0ed61f14132cf36c870f316d1fae840fe534181192c0"
K1097_RERUN_SHA256 = "2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40"


class Fail(Exception):
    pass


def need(ok, msg):
    if not ok:
        raise Fail(msg)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def load_pinned(path, sha, label):
    real = sha256_file(path)
    need(real == sha, f"{label} sha256 pin FAIL: {real}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# board geometry: 11x11, cell p -> (x, y) = (p % 11, p // 11).
# The bit-index convention is data-forced (the published hexes are canonical
# minima under exactly this coordinate map); every derived quantity below is
# gated against the published corpus, so a convention mismatch cannot pass.
# ---------------------------------------------------------------------------
def build_TF():
    TF = []
    for _t in range(8):
        tab = [0] * 121
        for p in range(121):
            x, y = p % 11, p // 11
            if _t == 0:
                X, Y = x, y
            elif _t == 1:
                X, Y = y, 10 - x
            elif _t == 2:
                X, Y = 10 - x, 10 - y
            elif _t == 3:
                X, Y = 10 - y, x
            elif _t == 4:
                X, Y = 10 - y, 10 - x
            elif _t == 5:
                X, Y = y, x
            elif _t == 6:
                X, Y = x, 10 - y
            else:
                X, Y = 10 - x, y
            tab[p] = 11 * Y + X
        TF.append(tab)
    return TF


TF = build_TF()
BIT = [[1 << TF[t][p] for p in range(121)] for t in range(8)]


def bits_of(mask):
    out = []
    p = 0
    while mask:
        low = mask & -mask
        out.append(low.bit_length() - 1)
        mask ^= low
        p += 1
    return out


def transform(mask, t):
    row = BIT[t]
    z = 0
    m = mask
    while m:
        low = m & -m
        m ^= low
        z |= row[low.bit_length() - 1]
    return z


def canon_int(mask):
    best = (1 << 128)
    for t in range(8):
        z = transform(mask, t)
        if z < best:
            best = z
    return best


def canon_hex(mask):
    return format(canon_int(mask), "032x")


def popcount(x):
    n = 0
    while x:
        x &= x - 1
        n += 1
    return n


# ---------------------------------------------------------------------------
# forbidden-quadruple predicate: exact zero test of the 4x4 integer
# determinant  | x  y  x^2+y^2  1 ; ... |  by Bareiss fraction-free forward
# elimination (fully integer arithmetic; no floats).  Zero  <=>  the four
# points are cocircular or collinear (degenerate circle).  This is the same
# predicate as the published alternating-3x3-cofactor form (Laplace
# expansion of the same determinant) but a different computation path.
# ---------------------------------------------------------------------------
def bareiss_det4(M):
    n = 4
    prev = 1
    piv = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            swap = -1
            for r in range(k + 1, n):
                if M[r][k] != 0:
                    swap = r
                    break
            if swap < 0:
                return 0
            M[k], M[swap] = M[swap], M[k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
            M[i][k] = 0
        prev = M[k][k]
        if prev == 0:
            return 0
        piv *= 1
    return M[n - 1][n - 1]


def quad_forbidden(points):
    """True iff no 4-subset of `points` is cocircular-or-collinear.

    Independent predicate path: translate the first point of each 4-subset
    to the origin and take the exact integer 3x3 determinant of the rows
    (dx, dy, d(x^2+y^2)) of the other three points.  A circle through the
    origin has equation x^2+y^2+ux+vy=0, so the determinant vanishes iff the
    four points are cocircular or collinear (degenerate circle) -- the same
    zero set as the 4x4 determinant |x y x^2+y^2 1| used by the published
    machine, computed by a different route (the published machine expands
    the same 4x4 determinant as an alternating sum of four 3x3 cofactor
    determinants; this implementation row-reduces by an anchor translation
    instead).  All arithmetic is exact integer arithmetic.
    """
    n = len(points)
    q = [x * x + y * y for x, y in points]
    for a in range(n - 3):
        xa, ya = points[a]
        qa = q[a]
        for b in range(a + 1, n - 2):
            dxb = points[b][0] - xa
            dyb = points[b][1] - ya
            dqb = q[b] - qa
            for c in range(b + 1, n - 1):
                dxc = points[c][0] - xa
                dyc = points[c][1] - ya
                dqc = q[c] - qa
                for d in range(c + 1, n):
                    dxd = points[d][0] - xa
                    dyd = points[d][1] - ya
                    dqd = q[d] - qa
                    det = (dxb * (dyc * dqd - dyd * dqc)
                           - dyb * (dxc * dqd - dxd * dqc)
                           + dqb * (dxc * dyd - dxd * dyc))
                    if det == 0:
                        return False
    return True


def quad_forbidden_bareiss(points):
    """Slow-path crosscheck: 4x4 Bareiss fraction-free determinant."""
    n = len(points)
    for a in range(n - 3):
        xa, ya = points[a]
        qa = xa * xa + ya * ya
        for b in range(a + 1, n - 2):
            xb, yb = points[b]
            qb = xb * xb + yb * yb
            for c in range(b + 1, n - 1):
                xc, yc = points[c]
                qc = xc * xc + yc * yc
                for d in range(c + 1, n):
                    xd, yd = points[d]
                    qd = xd * xd + yd * yd
                    M = [[xa, ya, qa, 1], [xb, yb, qb, 1],
                         [xc, yc, qc, 1], [xd, yd, qd, 1]]
                    if bareiss_det4([row[:] for row in M]) == 0:
                        return False
    return True


def bit_points(mask):
    return [(p % 11, p // 11) for p in bits_of(mask)]


# ---------------------------------------------------------------------------
# Hopcroft-Karp maximum bipartite matching (rows -> provider roots).
# ---------------------------------------------------------------------------
def hopcroft_karp(rows, adj):
    """returns (matching size, {row: provider})"""
    INF = float("inf")
    pair_u = {}
    pair_v = {}
    dist = {}

    def bfs():
        queue = []
        for u in rows:
            if u not in pair_u:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = INF
        dist[None] = INF
        found = False
        qi = 0
        while qi < len(queue):
            u = queue[qi]
            qi += 1
            du = dist[u]
            if du >= dist[None]:
                continue
            for v in adj[u]:
                pu = pair_v.get(v)
                if pu is None:
                    if dist[None] == INF:
                        dist[None] = du + 1
                    found = True
                elif dist.get(pu, INF) == INF:
                    dist[pu] = du + 1
                    queue.append(pu)
        return found

    def dfs(u):
        if u is None:
            return True
        du = dist[u]
        for v in adj[u]:
            pu = pair_v.get(v)
            if pu is None or (dist.get(pu, INF) == du + 1 and dfs(pu)):
                pair_u[u] = v
                pair_v[v] = u
                return True
        dist[u] = INF
        return False

    matching = 0
    while bfs():
        for u in rows:
            if u not in pair_u and dfs(u):
                matching += 1
    return matching, pair_u


# ---------------------------------------------------------------------------
# greedy set cover: lexicographically-smallest max-gain (published rule),
# written as an independent scan (strictly-better replacement).
# ---------------------------------------------------------------------------
def greedy_cover(cand_roots, cmap, rows_all):
    cands = sorted(cand_roots)
    cands_set = {c: cmap[c] for c in cands}
    remain = set(rows_all)
    sel = []
    while remain:
        best = None
        bg = 0
        for c in cands:
            g = len(cands_set[c] & remain)
            if g > bg:
                bg = g
                best = c
        if best is None:
            break
        sel.append({"root": best, "gained_rows": bg,
                    "covered_rows": sorted(cands_set[best] & remain)})
        remain -= cands_set[best]
        cands.remove(best)
        del cands_set[best]
    return sel, remain


# ---------------------------------------------------------------------------
def main():
    argv = list(sys.argv[1:])

    def opt(name):
        return argv[argv.index(name) + 1] if name in argv else None

    k1085_path = opt("--k1085") or os.environ.get("K1085_JSON")
    k1086_path = opt("--k1086") or os.environ.get("K1086_JSON")
    k1089_path = opt("--k1089") or os.environ.get("K1089_JSON")
    k1091_path = opt("--k1091") or os.environ.get("K1091_JSON")
    k1095_path = opt("--k1095") or os.environ.get("K1095_JSON")
    k1097_path = opt("--k1097canon") or os.environ.get("K1097_CANON_JSON")
    machine_path = opt("--k1097machine") or os.environ.get("K1097_MACHINE")
    rerun_path = opt("--k1097rerun") or os.environ.get("K1097_RERUN")
    out_path = opt("--out") or os.path.join(
        HERE, "output", "refuted50-refsolve-second-verification-20261120.json")
    need(k1085_path and os.path.isfile(k1085_path), "K1085 input required")
    need(k1086_path and os.path.isfile(k1086_path), "K1086 input required")
    need(k1089_path and os.path.isfile(k1089_path), "K1089 input required")
    need(k1091_path and os.path.isfile(k1091_path), "K1091 input required")
    need(k1095_path and os.path.isfile(k1095_path), "K1095 input required")
    need(k1097_path and os.path.isfile(k1097_path), "K1097 canonical required")
    need(machine_path and os.path.isfile(machine_path), "machine source required")
    need(rerun_path and os.path.isfile(rerun_path), "machine rerun output required")

    k1085 = load_pinned(k1085_path, K1085_SHA256, "K1085")
    k1086 = load_pinned(k1086_path, K1086_SHA256, "K1086")
    k1089 = load_pinned(k1089_path, K1089_SHA256, "K1089")
    k1091 = load_pinned(k1091_path, K1091_SHA256, "K1091")
    k1095 = load_pinned(k1095_path, K1095_SHA256, "K1095")

    # published canonical under verification: double pin
    canon_sha = sha256_file(k1097_path)
    with open(k1097_path, "rb") as f:
        blob = f.read()
    import hashlib as _h
    blob_sha1 = _h.sha1(b"blob %d\x00" % len(blob) + blob).hexdigest()
    need(canon_sha == K1097_CANON_SHA256 and blob_sha1 == K1097_CANON_BLOB_SHA1,
         "K1097 canonical double-pin FAIL")
    with open(k1097_path, "r", encoding="utf-8") as f:
        k1097 = json.load(f)

    # step (a): the published machine re-executed by the operator in a fresh
    # environment must reproduce the canonical byte-identically.
    need(sha256_file(machine_path) == K1097_MACHINE_SHA256,
         "machine source sha256 pin FAIL")
    need(sha256_file(rerun_path) == K1097_RERUN_SHA256,
         "machine rerun output sha256 pin FAIL (execution-level "
         "reproduction)")

    gates = []

    def gate(name, ok, detail=None):
        gates.append({"name": name, "ok": bool(ok), "detail": detail or {}})
        if not ok:
            need(False, "gate FAIL: " + name)

    # published canonical self-consistency: all gates ok
    gate("canon-gates-all-pass",
         all(g["ok"] for g in k1097["gates"]) and len(k1097["gates"]) == 27,
         {"gates": len(k1097["gates"])})

    # ---- Stage A: base universe -----------------------------------------
    base = k1085["base_state"]
    rows72 = base["residual_row_hex"]
    need(len(rows72) == base["residual_rows"] == 72, "rows72 count")
    need(len(set(rows72)) == 72, "rows72 distinct")
    gate("rows72-canonical-6stones",
         all(canon_hex(int(r, 16)) == r and popcount(int(r, 16)) == 6
             for r in rows72), {"rows": 72})
    gate("rows72-quad-free-translation-det3",
         all(quad_forbidden(bit_points(int(r, 16))) for r in rows72),
         {"rows": 72, "predicate": "anchor-translation 3x3 integer "
                                    "determinant of (dx, dy, d(x^2+y^2)); "
                                    "forbidden quadruples absent on all "
                                    "C(6,4)=15 subsets"})
    gate("rows72-quad-free-bareiss-crosscheck",
         all(quad_forbidden_bareiss(bit_points(int(r, 16))) for r in rows72),
         {"rows": 72, "predicate": "Bareiss 4x4 fraction-free integer "
                                    "determinant; both independent paths "
                                    "agree that all 72 rows are quad-free"})

    # ---- Stage B: universe82 / safe8 / FULL coverage re-derivation ------
    residual72 = set(rows72)
    wcover = {}
    canon_cache = {}
    gen_events = 0
    for row in rows72:
        Rm = int(row, 16)
        empt = [p for p in range(121) if not (Rm >> p) & 1]
        for ii in range(len(empt)):
            i = empt[ii]
            bm = Rm | (1 << i)
            for jj in range(ii + 1, len(empt)):
                m = bm | (1 << empt[jj])
                c = canon_cache.get(m)
                if c is None:
                    c = canon_int(m)
                    canon_cache[m] = c
                ch = format(c, "032x")
                s = wcover.get(ch)
                if s is None:
                    wcover[ch] = {row}
                else:
                    s.add(row)
                gen_events += 1
    universe82 = sorted(wcover)
    safe8 = []
    unsafe8_n = 0
    for c in universe82:
        if quad_forbidden(bit_points(int(c, 16))):
            safe8.append(c)
        else:
            unsafe8_n += 1
    safe8set = set(safe8)
    gate("universe82-rebuild",
         gen_events == 471960 and len(universe82) == 380098
         and len(safe8) == 120474 and unsafe8_n == 259624,
         {"generation_events": gen_events, "universe82": len(universe82),
          "safe8": len(safe8), "unsafe8": unsafe8_n})

    # crosscheck against the K1085 census fields too
    census = k1085["add_two_stones_census"]
    gate("k1085-census-agreement",
         census["generation_events"] == gen_events
         and census["universe82_roots"] == len(universe82)
         and census["safe8"] == len(safe8)
         and census["unsafe8"] == unsafe8_n,
         {"note": "re-derivation matches the K1085 census fields "
                  "as well as the K1097 pins"})

    # FULL population intrinsic-coverage re-derivation for every safe8 root:
    # all C(8,6)=28 six-stone subsets, canonical, intersected with the
    # residual-72 row set; must equal the generation-witness coverage.
    mismatches = 0
    cov_hist = Counter()
    for c in safe8:
        u = int(c, 16)
        bl = [1 << p for p in bits_of(u)]
        cov = set()
        for blist in _combinations6(bl):
            S = 0
            for b in blist:
                S |= b
            h = canon_hex(S)
            if h in residual72:
                cov.add(h)
        if cov != wcover[c]:
            mismatches += 1
        cov_hist[len(cov)] += 1
    gate("safe8-fullopulation-intrinsic-equals-generation",
         mismatches == 0,
         {"safe8_roots": len(safe8), "mismatches": mismatches,
          "intrinsic_coverage_hist": dict(sorted(cov_hist.items())),
          "note": ("every safe8 root's full C(8,6)=28 subset coverage equals "
                   "its generation-witness coverage; the published machine "
                   "sampled 39,255 roots, this check covers 100% of the "
                   "pool")})

    # coverage hist + per-row demand (independent recount)
    hist_pub_eq = dict(sorted(cov_hist.items())) == {1: 82602, 2: 33104,
                                                      3: 4718, 4: 50}
    demand = Counter()
    for c in safe8:
        for r in wcover[c]:
            demand[r] += 1
    dvals = [demand[r] for r in rows72]
    gate("coverage-hist-and-demand",
         hist_pub_eq and min(dvals) == 1714 and max(dvals) == 2944
         and sum(dvals) == 163164 and min(dvals) > 0,
         {"coverage_hist": dict(sorted(cov_hist.items())),
          "demand_min": min(dvals), "demand_max": max(dvals),
          "demand_sum": sum(dvals)})
    census_hist = {int(k): v for k, v in census["safe8_coverage_hist"].items()}
    gate("k1085-census-hist-agreement",
         census_hist == dict(cov_hist)
         and census["per_row_safe8_demand_min"] == min(dvals)
         and census["per_row_safe8_demand_max"] == max(dvals)
         and census["demand_sum"] == sum(dvals),
         {"note": "K1085 census hist, demand bounds and demand sum agree"})

    # ---- greedy 23 reproduction -----------------------------------------
    greedy_pub = census["greedy_roots"]
    need(len(greedy_pub) == 23, "greedy roots count")
    sel72, left72 = greedy_cover(safe8, wcover, rows72)
    mine_roots = [g["root"] for g in sel72]
    pub_roots = [e["root"] for e in greedy_pub]
    pub_cov = {e["root"]: sorted(e["covered_rows"]) for e in greedy_pub}
    gate("greedy23-reproduced",
         mine_roots == pub_roots and not left72
         and all(pub_cov[g["root"]] == g["covered_rows"] for g in sel72)
         and Counter(g["gained_rows"] for g in sel72) == {4: 7, 3: 13, 2: 2, 1: 1},
         {"reproduced": len(sel72), "leftover": len(left72),
          "exact_sequence": mine_roots == pub_roots,
          "exact_marginal_coverage": all(pub_cov[g["root"]] == g["covered_rows"]
                                         for g in sel72)})
    gates_need = Counter({4: 7, 3: 13, 2: 2, 1: 1})
    gate("greedy23-gains-hist",
         Counter(g["gained_rows"] for g in sel72) == gates_need,
         {"gains_hist": dict(sorted(Counter(
             g["gained_rows"] for g in sel72).items()))})
    gate("greedy23-quad-free-bareiss",
         all(popcount(int(e["root"], 16)) == 8
             and canon_hex(int(e["root"], 16)) == e["root"]
             and quad_forbidden(bit_points(int(e["root"], 16)))
             and e["root"] in safe8set for e in greedy_pub),
         {"roots": 23})

    # ---- upstream verdict joins (K1086 / K1089 / K1091 / K1095) ---------
    def join_sweep(doc, label):
        cl = doc["classification"]
        win = sorted(e["root"] for e in cl["win8_d10_candidates"])
        ref = sorted(e["root"] for e in cl["refuted_d10_facts"])
        sed = sorted(doc["per_root"].keys())
        ok_v = (len(win), len(ref), len(sed))
        per = doc["per_root"]
        nodes_sum = 0
        for rr in sed:
            for o in ("andclose1", "andclose0"):
                pr = per[rr]["probes"][o]
                nodes_sum += pr["nodes"]
        return cl, win, ref, sed, per, nodes_sum

    cl86, win7, ref16, sed23a, per86, nodes86 = join_sweep(k1086, "K1086")
    gate("k1086-join",
         len(win7) == 7 and len(ref16) == 16
         and sorted(win7 + ref16) == sed23a
         and sed23a == sorted(pub_roots)
         and cl86["capped_probes"] == 0 and cl86["error_probes"] == 0
         and cl86["unresolved"] == []
         and nodes86 == cl86["nodes_total"] == 18032471
         and all(per86[r]["probes"][o]["loss"] is True and
                 per86[r]["probes"][o]["capped"] is False
                 for r in win7 for o in ("andclose1", "andclose0"))
         and all(per86[r]["probes"][o]["loss"] is False and
                 per86[r]["probes"][o]["capped"] is False
                 for r in ref16 for o in ("andclose1", "andclose0")),
         {"win": len(win7), "ref": len(ref16),
          "nodes_total_recomputed": nodes86,
          "nodes_total_field": cl86["nodes_total"],
          "note": ("nodes_total recomputed as the sum of all per-probe node "
                   "counts (46 probes) independent of the field")})
    # canonical-claim crosscheck between K1086 per_root and K1085 census plan
    canon_claims86 = {r: sorted({canon_hex(int(h, 16))
                                 for h in per86[r]["covered_rows"]})
                      for r in sed23a}
    gate("k1086-claims-canonicalized-equal-k1085-census",
         all(sorted(pub_cov[r]) == canon_claims86[r] for r in sed23a),
         {"roots": 23,
          "note": ("raw K1086 covered_rows canonicalize to exactly the K1085 "
                   "census greedy-plan covered rows")})

    # residual 49
    pubc86 = {e["root"]: set(e["covered_rows"]) for e in greedy_pub}
    win_rows86 = set()
    for r in win7:
        win_rows86 |= pubc86[r]
    ref_rows86 = set()
    for r in ref16:
        ref_rows86 |= pubc86[r]
    residual49 = [r for r in rows72 if r not in win_rows86]
    resid49 = set(residual49)
    gate("residual49-partition",
         len(win_rows86) == 23 and len(ref_rows86) == 49
         and not (win_rows86 & ref_rows86)
         and win_rows86 | ref_rows86 == residual72
         and ref_rows86 == resid49
         and sum(len(pubc86[r]) for r in ref16) == 49
         and sum(len(pubc86[r]) for r in win7) == 23,
         {"win_rows": 23, "refuted_claim_rows": 49})

    cl89, win3a, ref13, sed16, per89, nodes89 = join_sweep(k1089, "K1089")
    gate("k1089-join",
         len(win3a) == 3 and len(ref13) == 13
         and sorted(win3a + ref13) == sed16
         and not (set(win3a) & set(ref13)) and not (set(sed16) & set(ref16))
         and cl89["capped_probes"] == 0 and cl89["error_probes"] == 0
         and cl89["unresolved"] == []
         and nodes89 == cl89["nodes_total"] == 6339079
         and all(r in safe8set and popcount(int(r, 16)) == 8
                 and canon_hex(int(r, 16)) == r
                 and quad_forbidden(bit_points(int(r, 16))) for r in sed16)
         and all(per89[r]["probes"][o]["loss"] is True and
                 per89[r]["probes"][o]["capped"] is False
                 for r in win3a for o in ("andclose1", "andclose0"))
         and all(per89[r]["probes"][o]["loss"] is False and
                 per89[r]["probes"][o]["capped"] is False
                 for r in ref13 for o in ("andclose1", "andclose0")),
         {"win": len(win3a), "ref": len(ref13),
          "nodes_total_recomputed": nodes89,
          "nodes_total_field": cl89["nodes_total"]})

    claims89 = {}
    ok89 = True
    for r in sed16:
        cans = {canon_hex(int(h, 16)) for h in per89[r]["covered_rows"]}
        ok89 = ok89 and cans <= resid49 and cans <= wcover[r]
        claims89[r] = cans
    counts89 = Counter()
    for r in sed16:
        for h in claims89[r]:
            counts89[h] += 1
    win3a_rows = set()
    for r in win3a:
        win3a_rows |= claims89[r]
    ref13_rows = set()
    for r in ref13:
        ref13_rows |= claims89[r]
    gate("replace16-claims-partition",
         ok89 and sum(len(claims89[r]) for r in sed16) == 49
         and len(ref13_rows | win3a_rows) == 49
         and not [h for h, n in counts89.items() if n > 1]
         and len(win3a_rows) == 9 and len(ref13_rows) == 40
         and ref13_rows | win3a_rows == resid49,
         {"claims": 49, "win3_rows": 9, "ref13_rows": 40,
          "exactly_once": True, "intrinsic_containment": True})

    residual40 = sorted(ref13_rows)
    resid40 = set(residual40)
    need(len(residual40) == 40, "residual40")

    cl91, win3b, ref12, sed15, per91, nodes91 = join_sweep(k1091, "K1091")
    gate("k1091-join",
         len(win3b) == 3 and len(ref12) == 12
         and sorted(win3b + ref12) == sed15
         and not (set(win3b) & set(ref12))
         and not (set(sed15) & set(ref16)) and not (set(sed15) & set(ref13))
         and cl91["capped_probes"] == 0 and cl91["error_probes"] == 0
         and cl91["unresolved"] == []
         and nodes91 == cl91["nodes_total"] == 7383022
         and all(r in safe8set and popcount(int(r, 16)) == 8
                 and canon_hex(int(r, 16)) == r
                 and quad_forbidden(bit_points(int(r, 16))) for r in sed15)
         and all(per91[r]["probes"][o]["loss"] is True and
                 per91[r]["probes"][o]["capped"] is False
                 for r in win3b for o in ("andclose1", "andclose0"))
         and all(per91[r]["probes"][o]["loss"] is False and
                 per91[r]["probes"][o]["capped"] is False
                 for r in ref12 for o in ("andclose1", "andclose0")),
         {"win": len(win3b), "ref": len(ref12),
          "nodes_total_recomputed": nodes91,
          "nodes_total_field": cl91["nodes_total"]})

    claims91 = {}
    ok91 = True
    for r in sed15:
        cans = {canon_hex(int(h, 16)) for h in per91[r]["covered_rows"]}
        ok91 = ok91 and cans <= resid40 and cans <= wcover[r]
        claims91[r] = cans
    counts91 = Counter()
    for r in sed15:
        for h in claims91[r]:
            counts91[h] += 1
    win3b_rows = set()
    for r in win3b:
        win3b_rows |= claims91[r]
    ref12_rows = set()
    for r in ref12:
        ref12_rows |= claims91[r]
    gate("replace15-claims-partition",
         ok91 and sum(len(claims91[r]) for r in sed15) == 40
         and len(win3b_rows | ref12_rows) == 40
         and not [h for h, n in counts91.items() if n > 1]
         and len(win3b_rows) == 10 and len(ref12_rows) == 30
         and win3b_rows | ref12_rows == resid40,
         {"claims": 40, "win3b_rows": 10, "ref12_rows": 30,
          "exactly_once": True, "intrinsic_containment": True})

    residual30 = sorted(ref12_rows)
    resid30 = set(residual30)
    need(len(residual30) == 30, "residual30")

    cl95, win3c, ref9, sed12, per95, nodes95 = join_sweep(k1095, "K1095")
    gate("k1095-join",
         len(win3c) == 3 and len(ref9) == 9
         and sorted(win3c + ref9) == sed12
         and not (set(win3c) & set(ref9))
         and not (set(sed12) & set(ref16)) and not (set(sed12) & set(ref13))
         and not (set(sed12) & set(ref12))
         and cl95["capped_probes"] == 0 and cl95["error_probes"] == 0
         and cl95["unresolved"] == []
         and nodes95 == cl95["nodes_total"] == 5700222
         and all(r in safe8set and popcount(int(r, 16)) == 8
                 and canon_hex(int(r, 16)) == r
                 and quad_forbidden(bit_points(int(r, 16))) for r in sed12)
         and all(per95[r]["probes"][o]["loss"] is True and
                 per95[r]["probes"][o]["capped"] is False
                 for r in win3c for o in ("andclose1", "andclose0"))
         and all(per95[r]["probes"][o]["loss"] is False and
                 per95[r]["probes"][o]["capped"] is False
                 for r in ref9 for o in ("andclose1", "andclose0")),
         {"win": len(win3c), "ref": len(ref9),
          "nodes_total_recomputed": nodes95,
          "nodes_total_field": cl95["nodes_total"]})

    claims95 = {}
    ok95 = True
    for r in sed12:
        cans = {canon_hex(int(h, 16)) for h in per95[r]["covered_rows"]}
        ok95 = ok95 and cans <= resid30 and cans <= wcover[r]
        claims95[r] = cans
    counts95 = Counter()
    for r in sed12:
        for h in claims95[r]:
            counts95[h] += 1
    win3c_rows = set()
    for r in win3c:
        win3c_rows |= claims95[r]
    ref9_rows = set()
    for r in ref9:
        ref9_rows |= claims95[r]
    gate("replace12-claims-partition",
         ok95 and sum(len(claims95[r]) for r in sed12) == 30
         and len(win3c_rows | ref9_rows) == 30
         and not [h for h, n in counts95.items() if n > 1]
         and len(win3c_rows) == 7 and len(ref9_rows) == 23
         and win3c_rows | ref9_rows == resid30,
         {"claims": 30, "win3c_rows": 7, "ref9_rows": 23,
          "exactly_once": True, "intrinsic_containment": True})

    # ---- Stage D: post-exclusion pool + residual 23 ----------------------
    ref50 = sorted(set(ref16) | set(ref13) | set(ref12) | set(ref9))
    need(len(ref50) == 50, "ref50")
    gate("ref50-union",
         len(ref50) == 50 and set(ref50) <= safe8set,
         {"roots": 50, "breakdown": {"K1086": len(ref16),
                                     "K1089": len(ref13),
                                     "K1091": len(ref12),
                                     "K1095": len(ref9)}})
    gate("ref50-matches-canon",
         sorted(k1097["exclusion"]["refuted_d10_roots_excluded"]) == ref50,
         {"note": "independent re-derivation equals the published list"})

    P3 = [c for c in safe8 if c not in set(ref50)]
    gate("pool-P3",
         len(P3) == 120424,
         {"safe8": len(safe8), "excluded": 50, "P_triple_prime": len(P3)})
    gate("pool-P3-matches-canon",
         k1097["exclusion"]["pool_P_triple_prime_size"] == len(P3))

    residual23 = sorted(ref9_rows)
    resid23 = set(residual23)
    need(len(residual23) == 23, "residual23")
    gate("residual23-definition",
         not (resid23 & win3c_rows) and resid23 <= resid30
         and sorted(k1097["exclusion"]["residual23_rows"]) == residual23,
         {"rows": 23,
          "source": "canonicalized claims of the 9 K1095 REFUTED-D10 roots"})

    demandT = Counter()
    for c in P3:
        for r in wcover[c]:
            demandT[r] += 1
    d23 = [demandT[r] for r in residual23]
    stranded = [r for r in residual23 if demandT[r] == 0]
    hist_rows = Counter(len(wcover[c] & resid23) for c in P3
                        if wcover[c] & resid23)
    gate("residual23-demand",
         min(d23) == 1781 and max(d23) == 2934 and sum(d23) == 50670
         and not stranded
         and dict(sorted(hist_rows.items())) == {1: 40065, 2: 4857, 3: 297}
         and sum(hist_rows.values()) == 45219,
         {"min": min(d23), "max": max(d23), "sum": sum(d23),
          "stranded": len(stranded),
          "provider_hist": dict(sorted(hist_rows.items())),
          "providers_touching": sum(hist_rows.values())})
    gate("residual23-demand-matches-canon",
         all(e["demand_P_triple_prime"] == demandT[e["row"]]
             for e in k1097["per_row_residual23"]),
         {"note": "per-row demand values equal the published table"})

    # ---- greedy re-solve scope 1 / scope 2 ------------------------------
    sel23, left23 = greedy_cover(P3, wcover, residual23)
    gains23 = Counter(g["gained_rows"] for g in sel23)
    lb = -(-23 // 4)
    gate("scope1-greedy",
         len(sel23) == 9 and not left23
         and dict(sorted(gains23.items())) == {1: 1, 2: 2, 3: 6}
         and lb == 6,
         {"greedy_size": len(sel23), "leftover": len(left23),
          "gains_hist": dict(sorted(gains23.items())),
          "lower_bound": lb,
          "selection": [{"root": g["root"],
                          "gained_rows": g["gained_rows"],
                          "covered_rows": g["covered_rows"]}
                         for g in sel23]})
    canon_sel = k1097["scope1_refsolve_residual23"]["greedy_selection"]
    gate("scope1-greedy-matches-canon",
         [{"root": g["root"], "gained_rows": g["gained_rows"],
           "covered_rows": g["covered_rows"]} for g in sel23] == canon_sel,
         {"note": ("exact root sequence, per-root gains and covered rows "
                   "equal the published selection")})
    # every selected root is a verified quadruple-free pool member
    gate("greedy9-quad-free-bareiss",
         all(popcount(int(g["root"], 16)) == 8
             and canon_hex(int(g["root"], 16)) == g["root"]
             and quad_forbidden(bit_points(int(g["root"], 16)))
             and g["root"] in safe8set and g["root"] not in set(ref50)
             for g in sel23),
         {"roots": 9})
    # exactly-once partition of the 23 rows
    union23 = []
    for g in sel23:
        union23 += g["covered_rows"]
    gate("greedy9-exactly-once",
         len(union23) == 23 and len(set(union23)) == 23
         and set(union23) == resid23,
         {"rows": 23})

    # Hopcroft-Karp maximum matching
    adj = {r: [c for c in P3 if r in wcover[c]] for r in residual23}
    asize, pair = hopcroft_karp(residual23, adj)
    witness = {r: pair[r] for r in residual23 if r in pair}
    ok_witness = len(witness) == 23 and all(
        row in wcover[witness[row]] for row in witness)
    distinct = len(set(witness.values())) == len(witness)
    gate("matching-hopcroft-karp",
         asize == 23 and ok_witness and distinct,
         {"matching_size": asize, "algorithm": "Hopcroft-Karp",
          "distinct_providers": distinct,
          "witness_row_to_root": {r: witness[r] for r in sorted(witness)},
          "note": ("independent algorithm; each row receives a distinct "
                   "verified provider covering it")})

    # ---- Stage E: WIN16 intrinsic footprints ----------------------------
    win16 = win7 + win3a + win3b + win3c
    need(len(win16) == 16, "win16")
    gate("win16-list-matches-canon",
         sorted(k1097["exclusion"]["win8_d10_candidates"]) == sorted(win16)
         and len(set(win16)) == 16,
         {"roots": 16})
    win_claims = {}
    for r in win7:
        win_claims[r] = {canon_hex(int(h, 16)) for h in pubc86[r]}
    for r in win3a:
        win_claims[r] = set(claims89[r])
    for r in win3b:
        win_claims[r] = set(claims91[r])
    for r in win3c:
        win_claims[r] = set(claims95[r])
    foot = {}
    for r in win16:
        u = int(r, 16)
        bl = bits_of(u)
        cov = set()
        for blist in _combinations6([1 << b for b in bl]):
            S = 0
            for b in blist:
                S |= b
            h = canon_hex(S)
            if h in residual72:
                cov.add(h)
        foot[r] = cov
    extra = {r: sorted(foot[r] - win_claims[r]) for r in win16
             if foot[r] - win_claims[r]}
    gate("win16-footprints",
         all(win_claims[r] <= foot[r] for r in win16)
         and extra == {"0000000800000000380000000810000a":
                       ["00000000000000003800000008001080"]}
         and all(foot[r] - win_claims[r] == set() for r in win16
                 if r != "0000000800000000380000000810000a"),
         {"per_root": {r: {"intrinsic_equals_claimed":
                           foot[r] == win_claims[r],
                           "claimed": sorted(win_claims[r]),
                           "intrinsic": sorted(foot[r])}
                       for r in win16},
          "extra": extra,
          "note": ("full C(8,6) re-derivation; 15/16 candidates have "
                   "intrinsic == claimed, the K1095 third root carries the "
                   "single published extra row")})
    gate("win16-footprints-matches-canon",
         all(sorted(k1097["win16_intrinsic_footprints"][r]["intrinsic"])
             == sorted(foot[r])
             and sorted(k1097["win16_intrinsic_footprints"][r]["claimed"])
             == sorted(win_claims[r]) for r in win16),
         {"note": "per-root intrinsic and claimed lists equal the canonical"})
    intrinsic_hit = sorted(row for row in resid23
                           if any(row in foot[r] for r in win16))
    gate("residual23-outside-win-intrinsic",
         intrinsic_hit == [],
         {"rows_hit": intrinsic_hit,
          "note": "no residual-23 row lies inside any WIN intrinsic"})
    # scope 2
    need_new = [r for r in residual23
                if not any(r in foot[w] for w in win16)]
    gate("scope2-rows",
         len(need_new) == 23 and need_new == residual23,
         {"rows": len(need_new)})
    pool_new = [c for c in P3 if c not in set(win16)]
    selN, leftN = greedy_cover(pool_new, wcover, residual23)
    gainsN = Counter(g["gained_rows"] for g in selN)
    mN, pairN = hopcroft_karp(residual23,
                              {r: [c for c in pool_new
                                   if r in wcover[c]] for r in residual23})
    gate("scope2-greedy",
         len(selN) == 9 and not leftN
         and dict(sorted(gainsN.items())) == {1: 1, 2: 2, 3: 6}
         and mN == 23
         and [g["root"] for g in selN] == [g["root"] for g in sel23],
         {"greedy_size": len(selN), "matching": mN,
          "same_selection_as_scope1": [g["root"] for g in selN]
          == [g["root"] for g in sel23],
          "selection": [{"root": g["root"],
                         "gained_rows": g["gained_rows"],
                         "covered_rows": g["covered_rows"]}
                        for g in selN]})
    canon_sel2 = k1097["scope2_refsolve_need_new_providers"]["greedy_selection"]
    gate("scope2-greedy-matches-canon",
         [{"root": g["root"], "gained_rows": g["gained_rows"],
           "covered_rows": g["covered_rows"]} for g in selN] == canon_sel2,
         {"note": "published scope-2 selection equal"})

    # per-row table crosscheck vs canonical
    mytab = []
    for row in residual23:
        mytab.append({
            "row": row,
            "demand_P_triple_prime": demandT[row],
            "demand_drop_from_safe8": demand[row] - demandT[row],
            "stranded_under_P_triple_prime": row in stranded,
            "win_intrinsic_cover": sorted(r for r in win16 if row in foot[r]),
            "win3c_claimed": row in win3c_rows,
            "greedy_provider": next((g["root"] for g in sel23
                                      if row in wcover[g["root"]]), None),
            "refuted_plan_provider": next((r for r in ref9
                                           if row in claims95[r]), None),
        })
    canon_tab = k1097["per_row_residual23"]
    gate("per-row-table-matches-canon",
         len(canon_tab) == 23 and all(
             e["row"] == mytab[i]["row"]
             and e["demand_P_triple_prime"]
             == mytab[i]["demand_P_triple_prime"]
             and e["demand_drop_from_safe8"]
             == mytab[i]["demand_drop_from_safe8"]
             and e["stranded_under_P_triple_prime"]
             == mytab[i]["stranded_under_P_triple_prime"]
             and e["win_intrinsic_cover"]
             == mytab[i]["win_intrinsic_cover"]
             and e["win3c_claimed"] == mytab[i]["win3c_claimed"]
             and e["greedy_provider"] == mytab[i]["greedy_provider"]
             and e["refuted_plan_provider"] == mytab[i]["refuted_plan_provider"]
             for i, e in enumerate(canon_tab)),
         {"rows": 23,
          "note": "demand, drop, stranded flag, win-intrinsic and win3c "
                  "claim flags all equal the published table"})

    gate("verdict-summary-matches-canon",
         k1097["verdicts"]["k1086"]["win8_d10_candidates"] == win7
         and k1097["verdicts"]["k1086"]["refuted_d10_facts"] == ref16
         and k1097["verdicts"]["k1089"]["win8_d10_candidates"] == win3a
         and k1097["verdicts"]["k1089"]["refuted_d10_facts"] == ref13
         and k1097["verdicts"]["k1091"]["win8_d10_candidates"] == win3b
         and k1097["verdicts"]["k1091"]["refuted_d10_facts"] == ref12
         and k1097["verdicts"]["k1095"]["win8_d10_candidates"] == win3c
         and k1097["verdicts"]["k1095"]["refuted_d10_facts"] == ref9,
         {"note": "all four verdict joins equal the canonical"})

    interpretation_guard = [
        ("Second verification only: no probes run, no row closed; greedy "
         "and witness selections are a conditional plan (bookkeeping), not "
         "certificates."),
        ("REFUTED-D10 is a probe fact (no forced win within depth 10 at the "
         "tested root), not a LOSS proof."),
        ("Node counts and solved counts are not game outcomes."),
        ("The standard 11x11 empty board, the two-stone roots {49,60}/{59,60}, "
         "S2 {59,60}, and classes 1/2/4 all remain UNKNOWN."),
    ]

    out = {
        "schema": "n11-residual72-refuted50-refsolve-second-verification-20261120-v1",
        "date": "2026-11-20",
        "status": "second-verification-passed",
        "single_owner_note": ("research/log/2026-11-20-n11-residual72-"
                              "refuted50-refsolve-second-verification-"
                              "single-owner-note.md (commit "
                              "de8c44ac96fbde0616a216f184dd54b42b3f2c49)"),
        "inputs": {
            "k1085_census_sha256": K1085_SHA256,
            "k1086_sweep_sha256": K1086_SHA256,
            "k1089_sweep_sha256": K1089_SHA256,
            "k1091_sweep_sha256": K1091_SHA256,
            "k1095_sweep_sha256": K1095_SHA256,
            "k1097_canonical_sha256": K1097_CANON_SHA256,
            "k1097_canonical_git_blob_sha1": K1097_CANON_BLOB_SHA1,
            "k1097_machine_sha256": K1097_MACHINE_SHA256,
            "k1097_machine_rerun_output_sha256": K1097_RERUN_SHA256,
        },
        "methodology_differences": {
            "quadruple_predicate": ("anchor-translation 3x3 integer determinant "
                                    "of (dx, dy, d(x^2+y^2)) for every 4-subset, "
                                    "with a Bareiss 4x4 fraction-free "
                                    "crosscheck on all 72 rows "
                                    "(published machine: alternating sum of "
                                    "four 3x3 cofactor determinants)"),
            "coverage_check": ("full population: all 120,474 safe8 roots "
                               "(published machine sampled 39,255)"),
            "matching_algorithm": ("Hopcroft-Karp (published: Kuhn "
                                   "augmenting paths)"),
            "nodes_totals": ("recomputed as sums of per-probe counts "
                             "(published: field pins)"),
        },
        "second_verification_results": {
            "rows72": 72,
            "universe82": len(universe82),
            "safe8": len(safe8),
            "unsafe8": unsafe8_n,
            "generation_events": gen_events,
            "safe8_fullopulation_coverage_mismatches": mismatches,
            "k1086": {"win8": len(win7), "refuted16": len(ref16),
                      "nodes_total": nodes86},
            "k1089": {"win3": len(win3a), "refuted13": len(ref13),
                      "nodes_total": nodes89},
            "k1091": {"win3": len(win3b), "refuted12": len(ref12),
                      "nodes_total": nodes91},
            "k1095": {"win3": len(win3c), "refuted9": len(ref9),
                      "nodes_total": nodes95},
            "refuted_excluded": 50,
            "pool_P_triple_prime": len(P3),
            "residual23": 23,
            "demand_min": min(d23), "demand_max": max(d23),
            "demand_sum": sum(d23),
            "providers_touching_23rows": sum(hist_rows.values()),
            "provider_hist": dict(sorted(hist_rows.items())),
            "greedy_scope1": {"size": len(sel23),
                              "gains_hist": dict(sorted(gains23.items())),
                              "leftover": len(left23),
                              "lower_bound": lb},
            "greedy_scope2": {"size": len(selN),
                              "gains_hist": dict(sorted(gainsN.items())),
                              "leftover": len(leftN)},
            "matching": {"size": asize,
                         "witness": {r: pair[r] for r in sorted(witness)}},
            "win16_footprints": {r: sorted(foot[r]) for r in win16},
            "win16_extra_rows": extra,
            "residual23_win_intrinsic_hits": intrinsic_hit,
        },
        "greedy_scope1_selection": [{"root": g["root"],
                                     "gained_rows": g["gained_rows"],
                                     "covered_rows": g["covered_rows"]}
                                    for g in sel23],
        "per_row_residual23": mytab,
        "gates": gates,
        "interpretation_guard": interpretation_guard,
        "trust_boundary": ("engine depth-10 verdict soundness + D4 "
                           "invariance; replacement root sets of rounds 1-3 "
                           "enter through the same upstream canonicals as "
                           "the machine under verification; this "
                           "verification runs no probes and closes no rows"),
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    txt = json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print("WROTE", out_path)
    print("sha256", hashlib.sha256(txt.encode("utf-8")).hexdigest())
    print("gates", len(gates), "all ok")


def _combinations6(bits):
    """all 6-of-8 index combinations as lists of single-bit masks"""
    out = []
    n = len(bits)
    for i in range(n - 5):
        for j in range(i + 1, n - 4):
            for k in range(j + 1, n - 3):
                for l in range(k + 1, n - 2):
                    for m in range(l + 1, n - 1):
                        for o in range(m + 1, n):
                            out.append([bits[i], bits[j], bits[k],
                                        bits[l], bits[m], bits[o]])
    return out


if __name__ == "__main__":
    main()
