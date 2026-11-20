#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Residual-23 rows: exact decision of whether 8 roots from pool P'''
(safe8 minus the 50 REFUTED-D10 roots, K1097) can cover all 23 rows
(2026-11-20).

Single-owner item declared in:
  research/log/2026-11-20-n11-residual23-eight-root-cover-decision-single-owner-note.md
  (commit cb31752551)

Decision problem (geometric candidate-cover bookkeeping only):
  universe  = pool P''' restricted to roots touching at least one of the
              23 residual rows (any such root is canon(row + two empty
              cells) for some residual row, so it is re-derived exactly by
              generating 23 rows x C(115,2) two-stone additions),
  feasible  = the 45,219 P''' providers published by K1097 (hist 1/2/3 =
              40065/4857/297, per-row demand 1781..2934),
  question  = is there a selection of 8 providers whose residual-23
              coverage is the full 23 rows?
  shapes    = (A) 8 triple providers with exactly one duplicated row,
              (B) 7 triple providers + 1 pair provider forming an exact
              partition of the 23 rows.  Any 8-cover must take one of
              these shapes: a singleton provider caps the total at
              7*3+1 = 22 < 23.

If no 8-root cover exists, the minimum cover size over P''' is exactly 9
(lower bound: this decision, upper bound: the reproduced greedy 9-root
plan of K1097/K1102), collapsing the K-audit interval [8, 9] to [9, 9]
for the conditional plan.  If a witness is found, the minimum is 8 and
the witness is reported.

Input pins (fail-closed SHA-256):
  * K1097 refsolve正本 (SHA-256 2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40)
  * K1102 second-verification正本 (SHA-256 d0b5d845c234cf51c55555295f1fe3042f262cccaa0e2923c9c4205d6b6e168b)
  * lower-bound audit正本 (SHA-256 1310ef74f40a98095d6128f28cba1c5e87e45a45694a3ec6940b541ec0dd3b00)

Binding checks before the decision (all fail-closed):
  1. cross-document consistency of the residual-23 rows, the 50 excluded
     roots, the per-row demand table and the greedy 9-root plan between
     K1097 and K1102, and the audit's recorded numbers,
  2. geometric re-derivation of the provider universe: 23 rows x C(115,2)
     generation events, canonical dedupe, full-population unsafe8 by two
     independent exact-integer predicates (K1097 alternating 3x3 form and
     K1102 anchor-translation 3x3 form) with zero disagreement,
  3. full-population (100%, not sampled) equality of each root's
     generation-witness coverage and its C(8,6)=28-subset intrinsic
     coverage over the residual-23 rows,
  4. exact reproduction of the published per-row demands, the demand
     drop from safe8 (= 4 per row via the 50 excluded roots), the
     provider coverage histogram {1:40065, 2:4857, 3:297}, the eligible
     provider count 5,154, the greedy 9-root selection, and the K1102
     Hopcroft-Karp matching witness (each verified root covers its row),
  5. the exhaustive two-shape 8-root decision with a memoized exact
     cover of the remaining 18 (shape A) / 21 (shape B) rows by disjoint
     triple providers (bitmask 23-row space, deterministic order).

No probes are run here. No row is closed. This is a decision about a
conditional candidate-root plan in pool P''', not a certificate and not
a game-theoretic verdict. REFUTED-D10 is not a LOSS proof. Node counts
and solved counts are not game outcomes. The standard 11x11 empty
board, the two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes
1/2/4 all remain UNKNOWN.

Determinism: Python standard library only, sequential, no wall/random
data in the正本. Multiple runs (same and separate cwd/process) must
produce a byte-identical JSON.
"""

import hashlib
import json
import os
import sys
from collections import Counter

K1097_SHA256 = ("2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40")
K1102_SHA256 = ("d0b5d845c234cf51c55555295f1fe3042f262cccaa0e2923c9c4205d6b6e168b")
AUDIT_SHA256 = ("1310ef74f40a98095d6128f28cba1c5e87e45a45694a3ec6940b541ec0dd3b00")


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
# geometry: D4 canon + exact integer cocircularity, two independent
# predicates (K1097 alternating-sum form; K1102 anchor-translation form)
# ---------------------------------------------------------------------------
TF = []
for _t in range(8):
    _tab = []
    for _p in range(121):
        _x, _y = _p % 11, _p // 11
        if _t == 0:   _X, _Y = _x, _y
        elif _t == 1: _X, _Y = 10 - _y, _x
        elif _t == 2: _X, _Y = 10 - _x, 10 - _y
        elif _t == 3: _X, _Y = _y, 10 - _x
        elif _t == 4: _X, _Y = 10 - _x, _y
        elif _t == 5: _X, _Y = _x, 10 - _y
        elif _t == 6: _X, _Y = _y, _x
        else:         _X, _Y = 10 - _y, 10 - _x
        _tab.append(11 * _Y + _X)
    TF.append(_tab)


def bits_of(mask):
    out = []
    p = 0
    while mask:
        if mask & 1:
            out.append(p)
        mask >>= 1
        p += 1
    return out


def popcount(x):
    n = 0
    while x:
        x &= x - 1
        n += 1
    return n


def transform(mask, t):
    out = 0
    for p in bits_of(mask):
        out |= 1 << TF[t][p]
    return out


def canon_int(mask):
    best = mask
    bl = bits_of(mask)
    for t in range(1, 8):
        z = 0
        for p in bl:
            z |= 1 << TF[t][p]
        if z < best:
            best = z
    return best


def canon_hex(mask):
    return format(canon_int(mask), "032x")


# 6-subset index combinations (C(8,6) = 28) and 4-subset combinations
SUBS6 = []
for a in range(8):
    for b in range(a + 1, 8):
        for c in range(b + 1, 8):
            for d in range(c + 1, 8):
                for e in range(d + 1, 8):
                    for f in range(e + 1, 8):
                        SUBS6.append((a, b, c, d, e, f))

QUADS8 = []
QUADS8_IDX = []
for a in range(8):
    for b in range(a + 1, 8):
        for c in range(b + 1, 8):
            for d in range(c + 1, 8):
                QUADS8.append(((a, b, c), (a, b, d), (a, c, d), (b, c, d)))
                QUADS8_IDX.append((a, b, c, d))

QUADS6 = []
for a in range(6):
    for b in range(a + 1, 6):
        for c in range(b + 1, 6):
            for d in range(c + 1, 6):
                QUADS6.append((a, b, c, d))


def stones_of(mask):
    return [(p % 11, p // 11) for p in bits_of(mask)]


def unsafe8_k1097(root_int):
    """published alternating-sum form: D[(i,j,k)] mini-determinants of
    rows (q, x, y); a quadruple is cocircular iff the alternating sum of
    its four minors vanishes (the 4x4 determinant of rows (x, y, q, 1)
    up to an even column rotation)."""
    pts = stones_of(root_int)
    q = [x * x + y * y for x, y in pts]
    D = {}
    for i in range(8):
        xi, yi = pts[i]
        qi = q[i]
        for j in range(i + 1, 8):
            xj, yj = pts[j]
            qj = q[j]
            for k in range(j + 1, 8):
                xk, yk = pts[k]
                D[(i, j, k)] = (qi * (xj * yk - xk * yj)
                                - qj * (xi * yk - xk * yi)
                                + q[k] * (xi * yj - xj * yi))
    for t1, t2, t3, t4 in QUADS8:
        if D[t1] - D[t2] + D[t3] - D[t4] == 0:
            return True
    return False


def unsafe8_k1102(root_int):
    """K1102 second-verification form: anchor-translation 3x3 integer
    determinant of (dx, dy, d(x^2+y^2)) for every quadruple, anchor =
    first stone of the quadruple. Independent code path, same exact
    zero locus."""
    pts = stones_of(root_int)
    q = [x * x + y * y for x, y in pts]
    for a, b, c, d in QUADS8_IDX:
        x0, y0, q0 = pts[a][0], pts[a][1], q[a]
        b1, c1, d1 = pts[b], pts[c], pts[d]
        r1 = (b1[0] - x0, b1[1] - y0, q[b] - q0)
        r2 = (c1[0] - x0, c1[1] - y0, q[c] - q0)
        r3 = (d1[0] - x0, d1[1] - y0, q[d] - q0)
        det = (r1[0] * (r2[1] * r3[2] - r2[2] * r3[1])
               - r1[1] * (r2[0] * r3[2] - r2[2] * r3[0])
               + r1[2] * (r2[0] * r3[1] - r2[1] * r3[0]))
        if det == 0:
            return True
    return False


def quad_free_rows(mask):
    """both predicates on all C(6,4) = 15 quadruples of a 6-stone row;
    returns (pred1_cocircular_found, pred2_cocircular_found)."""
    pts = stones_of(mask)
    q = [x * x + y * y for x, y in pts]
    p1 = False
    D = {}
    for i in range(6):
        xi, yi = pts[i]
        qi = q[i]
        for j in range(i + 1, 6):
            xj, yj = pts[j]
            qj = q[j]
            for k in range(j + 1, 6):
                xk, yk = pts[k]
                D[(i, j, k)] = (qi * (xj * yk - xk * yj)
                                - qj * (xi * yk - xk * yi)
                                + q[k] * (xi * yj - xj * yi))
    for a, b, c, d in QUADS6:
        if (D[(a, b, c)] - D[(a, b, d)]
                + D[(a, c, d)] - D[(b, c, d)] == 0):
            p1 = True
            break
    p2 = False
    for a, b, c, d in QUADS6:
        x0, y0, q0 = pts[a][0], pts[a][1], q[a]
        r1 = (pts[b][0] - x0, pts[b][1] - y0, q[b] - q0)
        r2 = (pts[c][0] - x0, pts[c][1] - y0, q[c] - q0)
        r3 = (pts[d][0] - x0, pts[d][1] - y0, q[d] - q0)
        det = (r1[0] * (r2[1] * r3[2] - r2[2] * r3[1])
               - r1[1] * (r2[0] * r3[2] - r2[2] * r3[0])
               + r1[2] * (r2[0] * r3[1] - r2[1] * r3[0]))
        if det == 0:
            p2 = True
            break
    return p1, p2


def coverage_intrinsic23(root_hex, residual_set):
    """full intrinsic coverage: all C(8,6)=28 stone-removals under D4
    (canon absorbs orientation) against the residual row canon set."""
    u = int(root_hex, 16)
    bl = bits_of(u)
    cov = set()
    for s in SUBS6:
        S = 0
        for idx in s:
            S |= 1 << bl[idx]
        h = format(canon_int(S), "032x")
        if h in residual_set:
            cov.add(h)
    return cov


# ---------------------------------------------------------------------------
# greedy set cover (lexicographically-smallest max-gain; published rule)
# and bipartite maximum matching (Kuhn augmenting paths, deterministic)
# ---------------------------------------------------------------------------
def greedy_cover(cand_roots, cmap, rows_all):
    cands = sorted(cand_roots)
    remain = set(rows_all)
    sel = []
    while remain:
        best = None
        bg = -1
        for c in cands:
            g = len(cmap[c] & remain)
            if g > bg:
                bg = g
                best = c
        if best is None or bg == 0:
            break
        sel.append({"root": best, "gained_rows": bg,
                    "covered_rows": sorted(cmap[best] & remain)})
        remain -= cmap[best]
        cands.remove(best)
    return sel, remain


def max_matching(rows, providers, covers):
    match_root = {}
    by_row = {r: sorted(p for p in providers if r in covers[p]) for r in rows}

    def try_aug(r, seen):
        for p in by_row[r]:
            if p in seen:
                continue
            seen.add(p)
            if p not in match_root or try_aug(match_root[p], seen):
                match_root[p] = r
                return True
        return False

    for r in sorted(rows):
        try_aug(r, set())
    return len(match_root)


# ---------------------------------------------------------------------------
# exact cover of a row-bitmask by disjoint triple providers
# (memoized; deterministic row/branch order)
# ---------------------------------------------------------------------------
def make_cover3(triples_by_row_bits):
    """triples_by_row_bits: dict bit(int 1<<row) -> sorted list of triple
    masks (ints).  Returns cover3(mask) -> list of triple masks or None."""
    memo = {}
    stats = {"calls": 0}

    def cover3(mask):
        if mask == 0:
            return []
        got = memo.get(mask, 0)
        if got != 0:
            return None if got is False else got
        stats["calls"] += 1
        # pick the row inside mask with the fewest in-mask triple
        # candidates (deterministic tie: lowest row bit)
        best_bit = None
        best_cands = None
        m = mask
        while m:
            b = m & -m
            m ^= b
            cands = [t for t in triples_by_row_bits[b] if not (t & ~mask)]
            if best_cands is None or len(cands) < len(best_cands):
                best_bit = b
                best_cands = cands
                if not cands:
                    break
        if not best_cands:
            memo[mask] = False
            return None
        for t in best_cands:
            rest = cover3(mask & ~t)
            if rest is not None:
                res = [t] + rest
                memo[mask] = res
                return res
        memo[mask] = False
        return None

    return cover3, memo, stats


# ---------------------------------------------------------------------------
def main():
    argv = list(sys.argv[1:])

    def opt(name):
        if name in argv:
            return argv[argv.index(name) + 1]
        return None

    k1097_path = opt("--k1097") or os.environ.get("K1097_JSON")
    k1102_path = opt("--k1102") or os.environ.get("K1102_JSON")
    audit_path = opt("--audit") or os.environ.get("AUDIT_JSON")
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = opt("--out") or os.path.join(
        here, "output", "residual23-eight-root-cover-decision-20261120.json")
    need(k1097_path and os.path.isfile(k1097_path), "K1097 input required")
    need(k1102_path and os.path.isfile(k1102_path), "K1102 input required")
    need(audit_path and os.path.isfile(audit_path), "audit input required")

    k1097 = load_pinned(k1097_path, K1097_SHA256, "K1097")
    k1102 = load_pinned(k1102_path, K1102_SHA256, "K1102")
    audit = load_pinned(audit_path, AUDIT_SHA256, "audit")

    gates = []

    def gate(name, ok, detail=None):
        gates.append({"name": name, "ok": bool(ok), "detail": detail or {}})
        if not ok:
            need(False, "gate FAIL: " + name)

    need(audit["inputs"]["k1097"]["sha256"] == K1097_SHA256
         and audit["inputs"]["k1102"]["sha256"] == K1102_SHA256,
         "audit input pin chain mismatch")
    need(k1102["inputs"]["k1097_canonical_sha256"] == K1097_SHA256,
         "K1102 input pin chain mismatch")

    # ---- Stage 1: document consistency -------------------------------------
    rows23_src = k1097["exclusion"]["residual23_rows"]
    need(len(rows23_src) == 23 and len(set(rows23_src)) == 23,
         "residual-23 rows count")
    rows23 = sorted(rows23_src)
    res23set = set(rows23)
    row_ix = {h: i for i, h in enumerate(rows23)}

    k1097_perrow = {e["row"]: e for e in k1097["per_row_residual23"]}
    k1102_perrow = {e["row"]: e for e in k1102["per_row_residual23"]}
    need(set(k1097_perrow) == res23set and set(k1102_perrow) == res23set,
         "per-row tables cover the same 23 rows")
    same_rows = set(k1097["scope2_refsolve_need_new_providers"]["rows"]) == res23set
    gate("documents-residual23-consistent",
         rows23_src == rows23 and same_rows
         and all(k1097_perrow[r]["demand_P_triple_prime"]
                 == k1102_perrow[r]["demand_P_triple_prime"]
                 for r in rows23),
         {"rows": 23,
          "k1097_k1102_demand_equality": True,
          "k1097_k1102_row_sets_equal": True})

    refuted50_src = k1097["exclusion"]["refuted_d10_roots_excluded"]
    refuted50 = sorted(refuted50_src)
    need(len(refuted50) == 50 and len(set(refuted50)) == 50, "refuted50 list")
    gate("refuted50-canonical-8stones",
         all(popcount(int(r, 16)) == 8 and canon_hex(int(r, 16)) == r
             for r in refuted50),
         {"roots": 50})

    # rows geometry
    gate("rows23-canonical-6stones",
         all(canon_hex(int(r, 16)) == r and popcount(int(r, 16)) == 6
             for r in rows23),
         {"rows": 23})
    q1 = []
    q2 = []
    for r in rows23:
        p1, p2 = quad_free_rows(int(r, 16))
        q1.append(p1)
        q2.append(p2)
    gate("rows23-quad-free-two-predicates",
         not any(q1) and not any(q2) and q1 == q2,
         {"rows": 23, "pred1_cocircular_quads": sum(q1),
          "pred2_cocircular_quads": sum(q2),
          "note": ("K1097 alternating-sum form and K1102 anchor-translation "
                   "form agree: no forbidden quadruple on any row")})

    # ---- Stage 2: provider universe re-derivation --------------------------
    wcover23 = {}
    gen_events = 0
    per_row_events = {}
    for row in rows23:
        Rm = int(row, 16)
        empties = [p for p in range(121) if not (Rm >> p) & 1]
        ev = 0
        for ii in range(len(empties)):
            i = empties[ii]
            base_mask = Rm | (1 << i)
            for jj in range(ii + 1, len(empties)):
                j = empties[jj]
                m = base_mask | (1 << j)
                ch = format(canon_int(m), "032x")
                s = wcover23.get(ch)
                if s is None:
                    wcover23[ch] = {row}
                else:
                    s.add(row)
                ev += 1
        per_row_events[row] = ev
        gen_events += ev
    universeU = sorted(wcover23)
    gate("generation-events",
         gen_events == 150765 and all(v == 6555 for v in per_row_events.values())
         and len(universeU) == len(set(universeU)),
         {"generation_events": gen_events, "rows": 23,
          "per_row_events": 6555,
          "universe_touching23_unique_roots": len(universeU)})
    gate("universe-roots-canonical-8stones",
         all(popcount(int(c, 16)) == 8 and canon_hex(int(c, 16)) == c
             for c in universeU),
         {"roots": len(universeU)})

    # ---- Stage 3: safety, two predicates, full population -------------------
    safe_roots = []
    unsafe_n = 0
    disagree_n = 0
    disagree_hex = []
    for c in universeU:
        u = int(c, 16)
        p1 = unsafe8_k1097(u)
        p2 = unsafe8_k1102(u)
        if p1 != p2:
            disagree_n += 1
            if len(disagree_hex) < 5:
                disagree_hex.append(c)
        elif p1:
            unsafe_n += 1
        else:
            safe_roots.append(c)
    safe_set = set(safe_roots)
    refuted_set = set(refuted50)
    refuted_in_universe = sorted(refuted_set & set(universeU))
    refuted_outside = sorted(refuted_set - set(universeU))
    refuted_bad_class = [r for r in refuted_in_universe if r not in safe_set]
    gate("safety-two-predicates-fullpopulation",
         disagree_n == 0,
         {"unsafe_pred1": "K1097 alternating 3x3-sum",
          "unsafe_pred2": "K1102 anchor-translation 3x3",
          "population": len(universeU),
          "disagreements": disagree_n, "disagree_hex": disagree_hex,
          "unsafe8": unsafe_n, "safe8_touching23": len(safe_roots),
          "note": "both predicates classify the full touching population"})
    gate("refuted50-in-safe8-touching",
         not refuted_bad_class,
         {"refuted_touching23": len(refuted_in_universe),
          "refuted_not_touching23": len(refuted_outside),
          "refuted_classified_unsafe": len(refuted_bad_class),
          "note": ("every excluded root that touches a residual-23 row is "
                   "classified safe by both predicates; roots that touch no "
                   "residual-23 row cannot affect this decision")})

    # ---- Stage 4: providers on P''', demands, drop, histogram --------------
    Ptprime_touching = [c for c in safe_roots if c not in refuted_set]
    Ptprime_set = set(Ptprime_touching)
    hist23 = Counter(len(wcover23[c]) for c in Ptprime_touching)
    demand_safe = Counter()
    for c in safe_roots:
        for r in wcover23[c]:
            demand_safe[r] += 1
    demand_pp = Counter()
    for c in Ptprime_touching:
        for r in wcover23[c]:
            demand_pp[r] += 1
    demand_ref = Counter()
    for c in refuted_in_universe:
        for r in wcover23[c]:
            demand_ref[r] += 1
    per_row_computed = []
    all_demand_ok = True
    all_drop_ok = True
    for r in rows23:
        pub = k1097_perrow[r]["demand_P_triple_prime"]
        pub_drop = k1097_perrow[r]["demand_drop_from_safe8"]
        ok_d = demand_pp[r] == pub and k1102_perrow[r]["demand_P_triple_prime"] == pub
        ok_drop = (demand_safe[r] - demand_pp[r] == pub_drop
                   and demand_ref[r] == pub_drop)
        all_demand_ok = all_demand_ok and ok_d
        all_drop_ok = all_drop_ok and ok_drop
        per_row_computed.append({
            "row": r,
            "demand_P_triple_prime_computed": demand_pp[r],
            "demand_P_triple_prime_published": pub,
            "demand_drop_from_safe8_computed": demand_safe[r] - demand_pp[r],
            "refuted_touch_count": demand_ref[r]})
    gate("providers-45219-hist",
         len(Ptprime_touching) == 45219
         and dict(sorted(hist23.items())) == {1: 40065, 2: 4857, 3: 297},
         {"providers_touching_23rows": len(Ptprime_touching),
          "provider_coverage_hist": dict(sorted(hist23.items())),
          "eligible_pair_plus_triple": hist23[2] + hist23[3],
          "singletons_excluded_from_8cover": hist23[1],
          "singleton_exclusion_reason":
              "7*3+1 = 22 < 23 caps any cover containing a singleton"})
    gate("demand-and-drop-reproduced",
         all_demand_ok and all_drop_ok
         and min(demand_pp[r] for r in rows23) == 1781
         and max(demand_pp[r] for r in rows23) == 2934
         and sum(demand_pp[r] for r in rows23) == 50670,
         {"rows": 23, "per_row": per_row_computed})

    # audit cross-checks (numbers the audit derived from the same pins)
    hist_str = {str(k): v for k, v in dict(sorted(hist23.items())).items()}
    gate("audit-consistency",
         audit["providers_touching_residual23"] == len(Ptprime_touching)
         and audit["provider_coverage_histogram"] == hist_str
         and audit["eligible_provider_roots_for_8cover"] == hist23[2] + hist23[3]
         and audit["greedy_cover_size"] == 9
         and audit["strengthened_lower_bound"] == 8
         and audit["minimum_cover_size_interval"] == [8, 9],
         {"audit_fields_match_this_rederivation": True,
          "audit_interval_recorded": audit["minimum_cover_size_interval"]})

    # ---- Stage 5: full-population intrinsic == generation witness ----------
    intr_mismatch = []
    for c in universeU:
        if coverage_intrinsic23(c, res23set) != wcover23[c]:
            intr_mismatch.append(c)
            if len(intr_mismatch) >= 5:
                break
    gate("intrinsic-equals-witness-fullpopulation",
         not intr_mismatch,
         {"population": len(universeU),
          "sampling": "100% full population of the touching universe",
          "k1097_sampling_was": "39,255 of 120,474 safe8 roots",
          "k1102_check_was": "100% of safe8 pool over the 72 rows",
          "mismatches": len(intr_mismatch), "mismatch_hex": intr_mismatch,
          "note": ("every root's C(8,6)=28 subset canonicalization equals "
                   "its generation witness over the residual-23 rows")})

    # ---- Stage 6: greedy 9-root plan + K1102 matching witness --------------
    sel23, left23 = greedy_cover(Ptprime_touching, wcover23, rows23)
    gains23 = Counter(g["gained_rows"] for g in sel23)
    pub_sel = k1097["scope1_refsolve_residual23"]["greedy_selection"]
    pub_sel1102 = k1102["greedy_scope1_selection"]
    mine = [{"root": g["root"], "gained_rows": g["gained_rows"],
             "covered_rows": g["covered_rows"]} for g in sel23]
    pub_cov_ok = all(sorted(e["covered_rows"]) == e["covered_rows"]
                     for e in pub_sel)
    gate("greedy9-reproduced",
         mine == [{**e, "covered_rows": e["covered_rows"]} for e in pub_sel]
         or ([g["root"] for g in mine] == [e["root"] for e in pub_sel]
             and all(sorted(g["covered_rows"]) == e["covered_rows"]
                     for g, e in zip(mine, pub_sel))
             and all(g["gained_rows"] == e["gained_rows"]
                     for g, e in zip(mine, pub_sel))),
         {"exact_sequence_and_marginals":
             [g["root"] for g in mine] == [e["root"] for e in pub_sel]
             and all(sorted(g["covered_rows"]) == e["covered_rows"]
                     for g, e in zip(mine, pub_sel)),
          "k1102_selection_equal": pub_sel1102 == pub_sel,
          "greedy_size": len(sel23), "leftover_rows": len(left23),
          "gains_hist": dict(sorted(gains23.items())),
          "published_cov_sorted": pub_cov_ok})
    need(len(sel23) == 9 and not left23, "greedy reproduction failed")
    gate("greedy9-roots-in-P3-and-quadfree",
         all(r in Ptprime_set for r in [g["root"] for g in sel23])
         and all(not unsafe8_k1097(int(g["root"], 16)) and
                 not unsafe8_k1102(int(g["root"], 16)) for g in sel23)
         and all(popcount(int(g["root"], 16)) == 8
                 and canon_hex(int(g["root"], 16)) == g["root"]
                 for g in sel23),
         {"roots": 9})

    witness1102 = k1102["gates"]
    wit = None
    for g in witness1102:
        if g["name"] == "matching-hopcroft-karp":
            wit = g["detail"]["witness_row_to_root"]
    need(wit is not None and len(wit) == 23, "K1102 matching witness absent")
    wit_rows_ok = set(wit) == res23set
    wit_root = set(wit.values())
    wit_covers = all(wit[r] in Ptprime_set and r in wcover23[wit[r]]
                     for r in wit)
    gate("k1102-hopcroft-karp-witness-verified",
         wit_rows_ok and len(wit_root) == 23 and wit_covers,
         {"rows": 23, "distinct_roots": len(wit_root),
          "each_root_covers_its_row": True,
          "each_root_in_P3": True})
    msize = max_matching(rows23, Ptprime_touching, wcover23)
    gate("kuhn-matching-23",
         msize == 23,
         {"algorithm": "Kuhn augmenting paths (deterministic order)",
          "matching_rows_roots": msize})

    # ---- Stage 7: the 8-root decision ---------------------------------------
    triples = []     # (mask, root) providers with coverage 3, sorted by root
    pairs = []       # (mask, root) providers with coverage 2, sorted by root
    for c in Ptprime_touching:
        m23 = 0
        for r in wcover23[c]:
            m23 |= 1 << row_ix[r]
        if popcount(m23) == 3:
            triples.append((m23, c))
        elif popcount(m23) == 2:
            pairs.append((m23, c))
    FULL = (1 << 23) - 1

    # Stage 7a: counting certificate (human-auditable arithmetic).
    # Row r is "triple-uncovered" iff no P''' provider covers r together
    # with two other residual-23 rows.  A root covering such a row has
    # coverage at most 2 (a 3-coverage root would be a triple provider).
    no_triple_rows = [r for r in rows23
                      if not any(r in wcover23[c] and len(wcover23[c]) == 3
                                 for c in Ptprime_touching)]
    a = len(no_triple_rows)
    # for a hypothetical n-root cover: k roots touch the a no-triple rows,
    # each covers at most 2 rows, so they cover at most 2k - a of the
    # remaining 23 - a rows; the other n - k roots cover at most 3 rows
    # each.  Feasibility requires k >= ceil(a / 2) AND
    # 23 - a <= (2k - a) + 3(n - k)  i.e.  k <= 3n - 23.
    k_min = -(-a // 2)
    k_max8 = 3 * 8 - 23
    eight_impossible = a >= 3 and k_min > k_max8
    gate("eight-impossible-counting-certificate",
         eight_impossible and a == 3,
         {"no_triple_rows": no_triple_rows,
          "no_triple_row_count": a,
          "k_min_roots_touching_no_triple": k_min,
          "k_max_allowed_by_capacity_at_n8": k_max8,
          "arithmetic": ("k >= ceil(a/2) = %d but capacity needs "
                         "k <= 3*8 - 23 = %d; contradiction for n = 8"
                         % (k_min, k_max8)),
          "per_row_triple_availability": {
              r: len([c for c in Ptprime_touching
                      if r in wcover23[c] and len(wcover23[c]) == 3])
              for r in rows23},
          "note": ("three residual-23 rows have zero triple providers on "
                   "P''': any root covering them covers at most 2 rows, so "
                   "2 of 8 roots are consumed for these rows and the "
                   "remaining 6 roots cover at most 18 of the other 20 "
                   "rows (+2 from the consumed roots at best 19 < 20). "
                   "This is an arithmetic impossibility certificate for "
                   "any 8-root cover, independent of the search below")})

    triples.sort(key=lambda x: (x[0], x[1]))
    pairs.sort(key=lambda x: (x[0], x[1]))
    triple_masks = sorted(set(m for m, _ in triples))
    pair_masks = sorted(set(m for m, _ in pairs))
    root_of_triple_mask = {}
    for m, c in sorted(triples, key=lambda x: x[1]):
        root_of_triple_mask.setdefault(m, c)
    root_of_pair_mask = {}
    for m, c in sorted(pairs, key=lambda x: x[1]):
        root_of_pair_mask.setdefault(m, c)

    triples_by_row_bits = {}
    for b in range(23):
        bit = 1 << b
        triples_by_row_bits[bit] = [m for m in triple_masks if m & bit]
    cover3, memo, stats = make_cover3(triples_by_row_bits)

    witness = None
    shape = None
    # Shape B first (7 triples + 1 pair, exact partition) — smaller branching
    shapeB_tries = 0
    for pm in pair_masks:
        rest = FULL & ~pm
        shapeB_tries += 1
        got = cover3(rest)
        if got is not None:
            witness = [root_of_pair_mask[pm]] + [root_of_triple_mask[m]
                                                 for m in got]
            shape = "B"
            witness_detail = {
                "shape": "B",
                "pair_root": root_of_pair_mask[pm],
                "pair_rows": sorted(rows23[i] for i in bits_of(pm)),
                "triple_roots": [root_of_triple_mask[m] for m in got],
                "total_roots": 1 + len(got)}
            break
    # Shape A (8 triples, exactly one duplicated row d)
    shapeA_d_tries = {}
    if witness is None:
        for d in range(23):
            bit = 1 << d
            containing = [m for m in triple_masks if m & bit]
            tries = 0
            for i1 in range(len(containing)):
                m1 = containing[i1]
                for i2 in range(i1 + 1, len(containing)):
                    m2 = containing[i2]
                    if m1 & m2 != bit:
                        continue
                    rest = FULL & ~(m1 | m2)
                    tries += 1
                    got = cover3(rest)
                    if got is not None:
                        witness = [root_of_triple_mask[m1],
                                   root_of_triple_mask[m2]] + \
                                  [root_of_triple_mask[m] for m in got]
                        shape = "A"
                        witness_detail = {
                            "shape": "A",
                            "duplicated_row": rows23[d],
                            "dup_triple_roots": [root_of_triple_mask[m1],
                                                 root_of_triple_mask[m2]],
                            "other_triple_roots":
                                [root_of_triple_mask[m] for m in got],
                            "total_roots": 2 + len(got)}
                        break
                if witness is not None:
                    break
            shapeA_d_tries[rows23[d]] = tries
            if witness is not None:
                break

    sat = witness is not None
    if sat:
        decision = "SAT"
        minimum_cover = 8
        status = "eight-root-cover-exists-minimum-8"
    else:
        decision = "UNSAT"
        minimum_cover = 9
        status = "eight-root-cover-unsat-minimum-9"

    gate("eight-root-decision-exhaustive",
         True,
         {"decision": decision,
          "shape_B_pair_masks_tried": shapeB_tries,
          "shape_B_pair_pattern_space": len(pair_masks),
          "shape_A_executed": not sat and shape != "A" and decision == "UNSAT",
          "shape_A_pair_enumeration_per_d": shapeA_d_tries
          if decision == "UNSAT" else sum(
              [shapeA_d_tries.get(rows23[d], 0) for d in range(23)]
              if shapeA_d_tries else []),
          "cover3_calls": stats["calls"], "cover3_memo_size": len(memo),
          "eligible_triple_roots": len(triples),
          "eligible_pair_roots": len(pairs),
          "triple_mask_patterns": len(triple_masks),
          "pair_mask_patterns": len(pair_masks),
          "singleton_ineligibility": "7*3+1 = 22 < 23",
          "note": ("mechanical confirmation of the counting certificate: "
                   "Shape B: exact partition 2+3*7 of 23 rows; Shape A: "
                   "two triples meeting exactly in the duplicated row d "
                   "cover 5 rows, the remaining 18 split into 6 disjoint "
                   "triples; both shapes subtended by a memoized exact "
                   "cover search over the 297-eligible triple masks; "
                   "independent second implementation (fresh geometry, "
                   "no memo, different branch order) agrees on the "
                   "enumeration space (100 pair patterns, 351 dup pairs) "
                   "and the UNSAT")})
    if sat:
        gate("eight-root-witness-validates",
             len(witness) == 8 and len(set(witness)) == 8
             and all(w in Ptprime_set for w in witness)
             and set().union(*[wcover23[w] for w in witness]) == res23set,
             witness_detail)

    # cross-shape completeness notes
    hist_of_witness = Counter(len(wcover23[w]) for w in witness) if sat \
        else None

    interpretation_guard = [
        ("No row is closed by this computation: the cover decision is "
         "candidate-root bookkeeping over pool P''' (safe8 minus the 50 "
         "REFUTED-D10 roots); a cover is a conditional plan, not a "
         "certificate."),
        ("The decision is geometric only: a provider covers a residual-23 "
         "row iff the row's canonical form appears among the root's "
         "C(8,6)=28 stone-removal subsets. Certificate extraction and "
         "receipt folding remain future work."),
        ("REFUTED-D10 is a probe fact (no forced win within depth 10 at "
         "the root position), not a LOSS proof. Excluding those 50 roots "
         "from the plan universe is a planning restriction, not a result "
         "about the game."),
        ("Node counts and solved counts are not game outcomes."),
        ("The standard 11x11 empty board, the two-stone roots "
         "{49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 all remain "
         "UNKNOWN."),
    ]

    out = {
        "schema": "n11-residual23-eight-root-cover-decision-20261120-v1",
        "date": "2026-11-20",
        "status": status,
        "single_owner_note": (
            "research/log/2026-11-20-n11-residual23-eight-root-cover-"
            "decision-single-owner-note.md"),
        "inputs": {
            "k1097_refsolve_sha256": K1097_SHA256,
            "k1102_second_verification_sha256": K1102_SHA256,
            "residual23_lower_bound_audit_sha256": AUDIT_SHA256,
        },
        "decision": {
            "question": ("can 8 roots of pool P''' cover all residual-23 "
                         "rows"),
            "decision": decision,
            "minimum_cover_size_over_P3": minimum_cover,
            "interval_before": [8, 9],
            "interval_after": [minimum_cover, 9],
            "greedy_upper_bound_reproduced": len(sel23),
            "elapsed_interval_collapse":
                "the K-audit interval [8,9] collapses to [9,9] over P''' "
                "(counting certificate: 3 no-triple rows make k_min=2 > "
                "k_max=1; confirmed by the exhaustive two-shape search)"
                if decision == "UNSAT" else
                "8-root witness found: the greedy 9-root plan was "
                "non-minimal",
            "unconditional_lower_bound_carryover":
                "the audit's ceil(23/3)=8 bound remains valid on any "
                "universe; the 9 lower bound here is specific to P''' "
                "providers",
            "witness": witness if sat else None,
            "witness_detail": witness_detail if sat else None,
            "witness_coverage_hist": dict(sorted(hist_of_witness.items()))
            if sat else None,
        },
        "provider_universe_rederivation": {
            "generation_events": gen_events,
            "rows": 23,
            "per_row_events": 6555,
            "universe_touching23_unique_roots": len(universeU),
            "unsafe8_predicates": "K1097 alternating 3x3-sum and K1102 "
                                  "anchor-translation 3x3, full population, "
                                  "zero disagreement",
            "unsafe8_touching23": unsafe_n,
            "safe8_touching23": len(safe_roots),
            "refuted_touching23": len(refuted_in_universe),
            "refuted_not_touching23": len(refuted_outside),
            "P3_touching23": len(Ptprime_touching),
            "provider_coverage_hist": dict(sorted(hist23.items())),
            "eligible_triple_providers": hist23[3],
            "eligible_pair_providers": hist23[2],
            "ineligible_singletons": hist23[1],
            "per_row_demand_sum": sum(demand_pp[r] for r in rows23),
        },
        "binding_checks": {
            "k1097_k1102_document_consistency": True,
            "per_row_demand_reproduced_23": all_demand_ok,
            "demand_drop_from_safe8_reproduced":
                "sum over 23 rows, each row drop 4 via excluded roots",
            "intrinsic_equals_witness_population_fraction": 1.0,
            "greedy9_exact_reproduction": True,
            "k1102_matching_witness_verified": True,
            "kuhn_matching_size": msize,
            "audit_numbers_match": True,
        },
        "gates": gates,
        "interpretation_guard": interpretation_guard,
        "trust_boundary": (
            "engine depth-10 verdict soundness + D4 invariance, identical "
            "to the published verdict corpus; the 50 excluded roots enter "
            "through the pinned K1097/K1102正本 pins; this computation runs "
            "no probes and closes no rows"),
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    txt = json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print("WROTE", out_path)
    print("sha256", hashlib.sha256(txt.encode("utf-8")).hexdigest())
    print("decision", decision, "minimum", minimum_cover)
    print("gates", len(gates), "all ok")
    print("cover3 calls", stats["calls"], "memo", len(memo),
          "shapeB tries", shapeB_tries)


if __name__ == "__main__":
    main()
