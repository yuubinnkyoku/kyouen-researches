#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
safe8 pool round-2 re-solve after excluding the 29 REFUTED-D10 roots
(K1086: 16 greedy roots; K1089: 13 replacement roots) (2026-11-20).

Single-owner item declared in:
  research/log/2026-11-20-n11-residual72-safe8-refuted29-refsolve-single-owner-note.md
  (commit c5dee3deb566a8ee3ad5a61e4a600b6be5e1aaa4)

Inputs (fail-closed SHA-256 pins):
  * K1085 census正本 (SHA-256 5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e)
  * K1086 sweep正本  (SHA-256 3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced)
  * K1089 sweep正本  (SHA-256 808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc)

The machine re-derives, independently of the K1085/K1088 experiment machines:
  Stage A  base state (72 residual rows, canonical, quad-free),
  Stage B  the add-two universe (72 rows x empty-pairs, generation witness ->
           canonical dedup), unsafe8, safe8 pool, coverage, per-row demand,
           and the lexicographically-smallest max-gain greedy set cover of the
           72 rows (must reproduce the published 23 roots),
  Stage C  the K1086 verdict join (7 WIN8 / 16 REFUTED, both orderings
           uncapped) -> residual-49 universe; the K1089 verdict join
           (3 WIN8 / 13 REFUTED over the 16 replacement roots, both orderings
           uncapped) with claim canonicalization and partition checks,
  Stage D  the post-exclusion re-solve: pool P' = safe8 minus the 29 REFUTED
           roots; per-row demand over P'; stranded rows; greedy witness;
           information lower bound; bipartite maximum matching,
  Stage E  intrinsic-coverage footprints of all 10 WIN8-D10 candidates
           (K1086 seven + K1089 three) over the residual-40 rows (geometry
           facts only), and the scope-2 re-solve of the rows that would still
           need new providers even if every WIN8 candidate's future receipt
           folds the rows it intrinsically covers.

No probes are run here. No row is closed. Greedy/witness outputs are a
conditional plan (candidate bookkeeping), not certificates. REFUTED-D10 is
not a LOSS proof. The standard 11x11 empty board, the two-stone roots
{49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 all remain UNKNOWN.

Determinism: Python standard library only, sequential, no wall/random data
in the正本. Multiple runs (same and separate cwd/process) must produce a
byte-identical JSON.
"""

import hashlib
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))

K1085_SHA256 = ("5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e")
K1086_SHA256 = ("3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced")
K1089_SHA256 = ("808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc")


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
# geometry: D4 canon + exact integer cocircularity/collinearity (resolve5
# conventions, re-implemented; no floats)
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
    best = None
    for t in range(8):
        z = transform(mask, t)
        if best is None or z < best:
            best = z
    return best


def canon_hex(mask):
    return format(canon_int(mask), "032x")


QUADS8 = []
for a in range(8):
    for b in range(a + 1, 8):
        for c in range(b + 1, 8):
            for d in range(c + 1, 8):
                QUADS8.append(((a, b, c), (a, b, d), (a, c, d), (b, c, d)))


def unsafe8(root_int):
    bl = bits_of(root_int)
    pts = [(p % 11, p // 11) for p in bl]
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


def coverage_of82(root_hex, residual_set):
    """full intrinsic coverage: all C(8,6)=28 stone-removals under D4
    (canon absorbs orientation) against the residual row canon set."""
    u = int(root_hex, 16)
    bl = bits_of(u)
    cov = set()
    for i in range(8):
        for j in range(i + 1, 8):
            for k in range(j + 1, 8):
                for l in range(k + 1, 8):
                    for m in range(l + 1, 8):
                        for n in range(m + 1, 8):
                            S = ((1 << bl[i]) | (1 << bl[j]) | (1 << bl[k])
                                 | (1 << bl[l]) | (1 << bl[m]) | (1 << bl[n]))
                            h = canon_hex(S)
                            if h in residual_set:
                                cov.add(h)
    return cov


# ---------------------------------------------------------------------------
# greedy set cover (lexicographically-smallest max-gain; published rule) and
# bipartite maximum matching (Kuhn augmenting paths, deterministic order)
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
    """bipartite maximum matching rows x roots; returns (size, row->root)."""
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
    row_of = {r: p for p, r in match_root.items()}
    return len(match_root), row_of


# ---------------------------------------------------------------------------
def main():
    argv = list(sys.argv[1:])
    def opt(name):
        if name in argv:
            return argv[argv.index(name) + 1]
        return None
    k1085_path = opt("--k1085") or os.environ.get("K1085_JSON")
    k1086_path = opt("--k1086") or os.environ.get("K1086_JSON")
    k1089_path = opt("--k1089") or os.environ.get("K1089_JSON")
    out_path = opt("--out") or os.path.join(HERE, "output",
                                            "safe8-refuted29-refsolve-20261120.json")
    need(k1085_path and os.path.isfile(k1085_path), "K1085 input required")
    need(k1086_path and os.path.isfile(k1086_path), "K1086 input required")
    need(k1089_path and os.path.isfile(k1089_path), "K1089 input required")

    k1085 = load_pinned(k1085_path, K1085_SHA256, "K1085")
    k1086 = load_pinned(k1086_path, K1086_SHA256, "K1086")
    k1089 = load_pinned(k1089_path, K1089_SHA256, "K1089")

    gates = []

    def gate(name, ok, detail=None):
        gates.append({"name": name, "ok": bool(ok), "detail": detail or {}})
        if not ok:
            need(False, "gate FAIL: " + name)

    # ---- Stage A: base state ------------------------------------------------
    base = k1085["base_state"]
    rows72 = base["residual_row_hex"]
    need(len(rows72) == base["residual_rows"] == 72, "residual rows count")
    need(len(set(rows72)) == 72, "residual rows distinct")
    gate("rows72-canonical-6stones",
         all(canon_hex(int(r, 16)) == r and popcount(int(r, 16)) == 6
             for r in rows72),
         {"rows": len(rows72)})

    def _det3(a, b, c):
        (x1, y1), (x2, y2), (x3, y3) = a, b, c
        q1 = x1 * x1 + y1 * y1
        q2 = x2 * x2 + y2 * y2
        q3 = x3 * x3 + y3 * y3
        return (q1 * (x2 * y3 - x3 * y2) - q2 * (x1 * y3 - x3 * y1)
                + q3 * (x1 * y2 - x2 * y1))

    def quad_free6(mask):
        pts = [(p % 11, p // 11) for p in bits_of(mask)]
        for a in range(6):
            for b in range(a + 1, 6):
                for c in range(b + 1, 6):
                    for d in range(c + 1, 6):
                        det = (_det3(pts[a], pts[b], pts[c])
                               - _det3(pts[a], pts[b], pts[d])
                               + _det3(pts[a], pts[c], pts[d])
                               - _det3(pts[b], pts[c], pts[d]))
                        if det == 0:
                            return False
        return True
    gate("rows72-quad-free", all(quad_free6(int(r, 16)) for r in rows72),
         {"rows": len(rows72), "note": "forbidden quadruples absent on all 72 rows"})

    census = k1085["add_two_stones_census"]
    greedy_pub = census["greedy_roots"]
    need(len(greedy_pub) == 23, "greedy roots count 23")
    gate("greedy23-8stones-canonical",
         all(popcount(int(e["root"], 16)) == 8
             and canon_hex(int(e["root"], 16)) == e["root"] for e in greedy_pub),
         {"roots": 23})
    need(census["greedy_set_cover_size"] == 23 and
         census["greedy_leftover_rows"] == 0, "published greedy arithmetic")

    # ---- Stage B: universe82 rebuild (independent re-derivation) -----------
    residualSet72 = set(rows72)
    wcover82 = {}
    gen_events = 0
    canon_cache = {}
    for row in rows72:
        Rm = int(row, 16)
        empties = [p for p in range(121) if not (Rm >> p) & 1]
        for ii in range(len(empties)):
            i = empties[ii]
            base_mask = Rm | (1 << i)
            for jj in range(ii + 1, len(empties)):
                j = empties[jj]
                m = base_mask | (1 << j)
                c = canon_cache.get(m)
                if c is None:
                    c = canon_int(m)
                    canon_cache[m] = c
                ch = format(c, "032x")
                s = wcover82.get(ch)
                if s is None:
                    wcover82[ch] = {row}
                else:
                    s.add(row)
                gen_events += 1
    universe82 = sorted(wcover82)
    need(all(popcount(int(c, 16)) == 8 for c in universe82),
         "universe82 roots are eight stones")
    safe8 = []
    unsafe8_n = 0
    for c in universe82:
        if unsafe8(int(c, 16)):
            unsafe8_n += 1
        else:
            safe8.append(c)
    safe8set = set(safe8)
    gate("stageB-universe82-balance",
         gen_events == 471960 and len(universe82) == 380098
         and len(safe8) == 120474 and unsafe8_n == 259624,
         {"generation_events": gen_events, "universe82_roots": len(universe82),
          "safe8": len(safe8), "unsafe8": unsafe8_n,
          "published_pins": {"generation_events": 471960,
                             "universe82_roots": 380098,
                             "safe8": 120474, "unsafe8": 259624}})

    cmap_pub_hist = Counter(len(wcover82[c]) for c in safe8)
    demand8 = Counter()
    for c in safe8:
        for r in wcover82[c]:
            demand8[r] += 1
    dvals = [demand8[r] for r in rows72]
    gate("stageB-coverage-and-demand",
         dict(sorted(cmap_pub_hist.items())) == {1: 82602, 2: 33104, 3: 4718, 4: 50}
         and min(dvals) == 1714 and max(dvals) == 2944
         and sum(dvals) == 163164 and min(dvals) > 0,
         {"safe8_coverage_hist": dict(sorted(cmap_pub_hist.items())),
          "per_row_safe8_demand_min": min(dvals),
          "per_row_safe8_demand_max": max(dvals),
          "demand_sum": sum(dvals)})

    xcheck = set(c for c in safe8 if len(wcover82[c]) >= 2)
    for idx, c in enumerate(safe8):
        if idx % 60 == 0:
            xcheck.add(c)
    xbad = []
    for c in sorted(xcheck):
        if coverage_of82(c, residualSet72) != wcover82[c]:
            xbad.append(c)
    gate("stageB-coverage-crosscheck", not xbad,
         {"checked_roots": len(xcheck), "mismatches": len(xbad),
          "sampling": ("all multi-coverage (>=2) safe8 roots and every "
                       "60th sorted safe8 root; full C(8,6)=28 subset "
                       "re-derivation vs generation witness")})

    sel72, left72 = greedy_cover(safe8, wcover82, rows72)
    gains_hist = Counter(g["gained_rows"] for g in sel72)
    pub_roots = [e["root"] for e in greedy_pub]
    pub_cov = {e["root"]: sorted(e["covered_rows"]) for e in greedy_pub}
    mine_roots = [g["root"] for g in sel72]
    mine_cov = {g["root"]: g["covered_rows"] for g in sel72}
    gate("stageB-greedy-23-reproduced",
         mine_roots == pub_roots and not left72
         and dict(sorted(gains_hist.items())) == {4: 7, 3: 13, 2: 2, 1: 1}
         and all(pub_cov[r] == mine_cov[r] for r in pub_roots),
         {"reproduced_size": len(sel72), "leftover": len(left72),
          "gains_hist": dict(sorted(gains_hist.items())),
          "exact_root_sequence_match": mine_roots == pub_roots,
          "exact_marginal_coverage_match":
              all(pub_cov[r] == mine_cov[r] for r in pub_roots)})
    gate("greedy23-all-in-safe8",
         all(e["root"] in safe8set for e in greedy_pub), {"roots": 23})

    # ---- Stage C1: K1086 verdict join ----------------------------------------
    cl = k1086["classification"]
    win7 = sorted(e["root"] for e in cl["win8_d10_candidates"])
    ref16 = sorted(e["root"] for e in cl["refuted_d10_facts"])
    need(len(win7) == 7 and len(ref16) == 16 and not (set(win7) & set(ref16)),
         "K1086 classification sizes")
    per_root6 = k1086["per_root"]
    ok_verdicts = True
    for r in win7:
        for o in ("andclose1", "andclose0"):
            pr = per_root6[r]["probes"].get(o)
            ok_verdicts = ok_verdicts and pr is not None and pr["loss"] is True \
                and pr["capped"] is False
    for r in ref16:
        for o in ("andclose1", "andclose0"):
            pr = per_root6[r]["probes"].get(o)
            ok_verdicts = ok_verdicts and pr is not None and pr["loss"] is False \
                and pr["capped"] is False
    gate("k1086-verdict-pins",
         ok_verdicts and cl["capped_probes"] == 0 and cl["error_probes"] == 0
         and cl["nodes_total"] == 18032471
         and sorted(win7 + ref16) == sorted(pub_roots),
         {"win8_d10_candidates": len(win7), "refuted_d10_facts": len(ref16),
          "capped": cl["capped_probes"], "error": cl["error_probes"],
          "nodes_total": cl["nodes_total"],
          "exactly_the_greedy_plan_roots":
              sorted(win7 + ref16) == sorted(pub_roots)})

    pubc = {e["root"]: set(e["covered_rows"]) for e in greedy_pub}
    win_rows = set()
    for r in win7:
        win_rows |= pubc[r]
    ref_rows = set()
    for r in ref16:
        ref_rows |= pubc[r]
    need(len(win_rows) == 23, "win claimed rows 23")
    residual49 = [r for r in rows72 if r not in win_rows]
    need(len(residual49) == 49, "residual49 count")
    gate("residual49-partition",
         win_rows <= residualSet72 and ref_rows == set(residual49)
         and len(ref_rows) == 49
         and sum(len(pubc[r]) for r in ref16) == 49
         and sum(len(pubc[r]) for r in win7) == 23,
         {"win_rows": 23, "refuted_claim_rows": 49,
          "sum_claims_partition_72rows": True})

    # ---- Stage C2: K1089 verdict join (16 replacement roots) ----------------
    k1089_doc = k1089
    ncl = k1089_doc["classification"]
    win3 = sorted(e["root"] for e in ncl["win8_d10_candidates"])
    ref13 = sorted(e["root"] for e in ncl["refuted_d10_facts"])
    unresolved9 = ncl["unresolved"]
    sed16 = sorted(k1089_doc["per_root"].keys())
    need(len(win3) == 3 and len(ref13) == 13 and not unresolved9
         and not (set(win3) & set(ref13))
         and sorted(win3 + ref13) == sed16,
         "K1089 classification sizes")
    per_root9 = k1089_doc["per_root"]
    ok_verdicts9 = True
    for r in win3:
        for o in ("andclose1", "andclose0"):
            pr = per_root9[r]["probes"].get(o)
            ok_verdicts9 = ok_verdicts9 and pr is not None and pr["loss"] is True \
                and pr["capped"] is False
    for r in ref13:
        for o in ("andclose1", "andclose0"):
            pr = per_root9[r]["probes"].get(o)
            ok_verdicts9 = ok_verdicts9 and pr is not None and pr["loss"] is False \
                and pr["capped"] is False
    gate("k1089-verdict-pins",
         ok_verdicts9 and ncl["capped_probes"] == 0 and ncl["error_probes"] == 0
         and ncl["nodes_total"] == 6339079,
         {"win8_d10_candidates": len(win3), "refuted_d10_facts": len(ref13),
          "capped": ncl["capped_probes"], "error": ncl["error_probes"],
          "nodes_total": ncl["nodes_total"]})
    gate("replace16-in-safe8",
         len(sed16) == 16
         and all(r in safe8set and popcount(int(r, 16)) == 8
                 and canon_hex(int(r, 16)) == r for r in sed16),
         {"roots": 16,
          "note": "all 16 replacement roots are canonical quadruple-free "
                  "safe8 pool members (K1089 geometry gate re-checked against "
                  "the re-built pool)"})
    need(not (set(sed16) & set(ref16)), "replacement roots exclude ref16")

    # canonicalized claims of the 16 replacement roots (K1089 principal claims
    # are D4-orientation hexes; canonicalize into residual row hexes)
    resid49set = set(residual49)
    claims9 = {}
    ok_canon = True
    bad_canon = []
    for r in sed16:
        cs = per_root9[r]["covered_rows"]
        cans = set()
        for h in cs:
            can = canon_hex(int(h, 16))
            cans.add(can)
            if can not in resid49set:
                ok_canon = False
                bad_canon.append({"root": r, "claim": h, "canon": can})
        ok_canon = ok_canon and cans <= wcover82[r]
        claims9[r] = cans
    n_claims = sum(len(claims9[r]) for r in sed16)
    distinct_claims = set()
    for r in sed16:
        distinct_claims |= claims9[r]
    # exactly-once partition across the 16 replacement roots
    counts = Counter()
    for r in sed16:
        for h in claims9[r]:
            counts[h] += 1
    dup_rows = [h for h, n in counts.items() if n > 1]
    win3_claims = set()
    for r in win3:
        win3_claims |= claims9[r]
    ref13_claims = set()
    for r in ref13:
        ref13_claims |= claims9[r]
    gate("replace16-claims-canonicalized",
         ok_canon and n_claims == 49 and len(distinct_claims) == 49
         and not dup_rows
         and len(win3_claims) == 9 and len(ref13_claims) == 40
         and not (win3_claims & ref13_claims)
         and ref13_claims | win3_claims == resid49set
         and all(claims9[r] <= wcover82[r] for r in sed16),
         {"claims_total": n_claims, "claims_distinct": len(distinct_claims),
          "dup_rows": sorted(dup_rows),
          "win3_claim_rows": len(win3_claims),
          "ref13_claim_rows": len(ref13_claims),
          "partition_of_residual49": True,
          "bad_canon": bad_canon[:5],
          "note": ("claims canonicalize into residual-49 rows, each exactly "
                   "once, and every claim is inside the root's generation-"
                   "witness coverage (intrinsic)")})

    # ---- Stage D: post-exclusion re-solve over pool P' -----------------------
    ref29 = set(ref16) | set(ref13)
    need(len(ref29) == 29, "29 excluded roots")
    Pprime = [c for c in safe8 if c not in ref29]
    need(len(Pprime) == 120445, "pool P' size after exclusion")
    gate("pool-P-prime-size", len(Pprime) == 120445,
         {"safe8": 120474, "excluded_refuted": 29, "P_prime": len(Pprime)})

    residual40 = sorted(ref13_claims)
    need(len(residual40) == 40, "residual40 count")
    gate("residual40-definition",
         set(residual40) == ref13_claims and not (set(residual40) & win3_claims)
         and set(residual40) <= resid49set,
         {"rows": 40, "source": "canonicalized claims of the 13 REFUTED-D10 "
                                "replacement roots"})

    demandP = Counter()
    for c in Pprime:
        for r in wcover82[c]:
            demandP[r] += 1
    d40 = [demandP[r] for r in residual40]
    stranded40 = [r for r in residual40 if demandP[r] == 0]
    hist40 = Counter(d40)
    hist_rows = Counter(len(wcover82[c] & set(residual40)) for c in Pprime
                        if wcover82[c] & set(residual40))
    gate("residual40-demand-on-P-prime", True,
         {"min": min(d40), "max": max(d40), "sum": sum(d40),
          "stranded_rows": len(stranded40), "stranded_hex": stranded40,
          "demand_hist_over_40_rows": dict(sorted(hist40.items())),
          "provider_coverage_hist_over_40rows":
              dict(sorted(hist_rows.items())),
          "providers_touching_40rows": sum(hist_rows.values())})

    # ---- Stage E: intrinsic footprints of all 10 WIN8 candidates -------------
    win10 = win7 + win3
    win_claims_canon = {}
    for r in win7:
        win_claims_canon[r] = set(canon_hex(int(h, 16)) for h in pubc[r])
    for r in win3:
        win_claims_canon[r] = set(claims9[r])
    win_foot = {}
    for r in win10:
        full = coverage_of82(r, residualSet72)
        win_foot[r] = {"claimed": sorted(win_claims_canon[r]),
                       "intrinsic": sorted(full),
                       "intrinsic_equals_claimed":
                           full == win_claims_canon[r]}
    intrinsic40 = {}
    for row in residual40:
        covs = [r for r in win10 if row in win_foot[r]["intrinsic"]]
        if covs:
            intrinsic40[row] = sorted(covs)
    win_extra = {}
    for r in win10:
        ex = [row for row in win_foot[r]["intrinsic"]
              if row not in win_claims_canon[r]]
        if ex:
            win_extra[r] = ex
    need_new = [r for r in residual40 if r not in intrinsic40]
    gate("win10-intrinsic-footprints", True,
         {"win_roots": len(win10),
          "win_per_root_intrinsic_equals_claimed":
              all(win_foot[r]["intrinsic_equals_claimed"] for r in win10),
          "win_extra_intrinsic_rows_over_claims":
              {k: sorted(v) for k, v in sorted(win_extra.items())},
          "residual40_covered_by_win_intrinsic": len(intrinsic40),
          "residual40_remaining_after_win_intrinsic": len(need_new),
          "note": ("intrinsic coverage = full C(8,6) subset re-derivation "
                   "against the re-derived residual-72 canon set; per-root "
                   "claims are the canonicalized published claims of K1086 "
                   "(7 roots) / K1089 (3 roots); a residual-40 row inside a "
                   "WIN candidate's intrinsic coverage is a geometry fact "
                   "only: it would need that root's certificate extraction "
                   "AND receipt fold to close; nothing is closed here")})

    # scope 1 re-solve: all 40 residual rows, pool P'
    sel40, left40 = greedy_cover(Pprime, wcover82, residual40)
    gains40 = Counter(g["gained_rows"] for g in sel40)
    lb40 = -(-40 // 4)
    msize40, _ = max_matching(residual40, Pprime, wcover82)
    gate("scope1-greedy-re-solve-40rows", True,
         {"greedy_size": len(sel40), "leftover_rows": len(left40),
          "leftover_hex": sorted(left40),
          "gains_hist": dict(sorted(gains40.items())),
          "lower_bound_rows": lb40,
          "max_matching_rows_roots": msize40,
          "plan_probes_two_orderings": 2 * len(sel40),
          "stranded_rows_under_P_prime": len(stranded40),
          "selection": [{"root": g["root"], "gained_rows": g["gained_rows"],
                         "covered_rows": g["covered_rows"]} for g in sel40]})

    # scope 2 re-solve: rows that still need a NEW provider even if all 10
    # WIN candidates' future receipt folds cover their intrinsic rows
    pool_new = [c for c in Pprime if c not in set(win10)]
    selN, leftN = greedy_cover(pool_new, wcover82, need_new)
    gainsN = Counter(g["gained_rows"] for g in selN)
    msizeN, _ = max_matching(need_new, pool_new, wcover82)
    lbN = -(-len(need_new) // 4)
    gate("scope2-re-solve-post-win-intrinsic", True,
         {"rows": len(need_new), "row_hex": need_new,
          "greedy_size": len(selN), "leftover_rows": len(leftN),
          "leftover_hex": sorted(leftN),
          "gains_hist": dict(sorted(gainsN.items())),
          "lower_bound_rows": lbN,
          "max_matching_rows_roots": msizeN,
          "plan_probes_two_orderings": 2 * len(selN),
          "selection": [{"root": g["root"], "gained_rows": g["gained_rows"],
                         "covered_rows": g["covered_rows"]} for g in selN]})

    # per-row table for the residual 40
    per_row40 = []
    for row in residual40:
        ent = {
            "row": row,
            "demand_P_prime": demandP[row],
            "demand_drop_from_safe8": demand8[row] - demandP[row],
            "stranded_under_P_prime": row in stranded40,
            "win_intrinsic_cover": intrinsic40.get(row, []),
            "win3_claimed": row in win3_claims,
            "greedy_provider": next((g["root"] for g in sel40
                                     if row in wcover82[g["root"]]), None),
            "refuted_plan_provider": next((r for r in ref13
                                           if row in claims9[r]), None),
        }
        per_row40.append(ent)
    gate("per-row-table-complete",
         len(per_row40) == 40
         and sum(1 for e in per_row40 if e["greedy_provider"]) ==
             40 - len(left40),
         {"rows": len(per_row40),
          "with_greedy_provider": sum(1 for e in per_row40
                                      if e["greedy_provider"])})

    interpretation_guard = [
        ("No row is closed by this computation: greedy/witness selections "
         "are a conditional plan and a candidate-root bookkeeping, not "
         "certificates."),
        ("REFUTED-D10 is a probe fact (no forced win within depth 10 for the "
         "tested side at the root position), not a LOSS proof."),
        ("Node counts and solved counts are not game outcomes."),
        ("The standard 11x11 empty board, the two-stone roots {49,60}/{59,60}, "
         "S2 {59,60}, and classes 1/2/4 all remain UNKNOWN."),
    ]

    out = {
        "schema": "n11-residual72-safe8-refuted29-refsolve-20261120-v1",
        "date": "2026-11-20",
        "status": "refsolve-computed",
        "single_owner_note": ("research/log/2026-11-20-n11-residual72-"
                              "safe8-refuted29-refsolve-single-owner-note.md "
                              "(commit c5dee3deb566a8ee3ad5a61e4a600b6be5e1aaa4)"),
        "inputs": {
            "k1085_census_sha256": K1085_SHA256,
            "k1086_sweep_sha256": K1086_SHA256,
            "k1089_sweep_sha256": K1089_SHA256,
            "depth10_protocol_reference": "runner v17, cap 30M",
        },
        "stageB_universe_independent_rederivation": {
            "generation_events": gen_events,
            "universe82_roots": len(universe82),
            "safe8": len(safe8),
            "unsafe8": unsafe8_n,
            "safe8_coverage_hist": dict(sorted(cmap_pub_hist.items())),
            "per_row_safe8_demand_min": min(dvals),
            "per_row_safe8_demand_max": max(dvals),
            "demand_sum": sum(dvals),
            "coverage_crosscheck_roots": len(xcheck),
            "greedy_reproduction_exact": True,
        },
        "verdicts": {
            "k1086": {"win8_d10_candidates": win7,
                      "refuted_d10_facts": ref16,
                      "win7_claimed_rows_canon": 23},
            "k1089": {"win8_d10_candidates": win3,
                      "refuted_d10_facts": ref13,
                      "replacement16_roots": sed16,
                      "win3_claimed_rows_canon": len(win3_claims),
                      "ref13_claimed_rows_canon": len(ref13_claims)},
        },
        "exclusion": {
            "refuted_d10_roots_excluded": sorted(ref29),
            "win8_d10_candidates": win10,
            "pool_P_prime_size": len(Pprime),
            "residual40_rows": residual40,
        },
        "win10_intrinsic_footprints": win_foot,
        "scope1_refsolve_residual40": {
            "greedy_selection": [{"root": g["root"],
                                  "gained_rows": g["gained_rows"],
                                  "covered_rows": g["covered_rows"]}
                                 for g in sel40],
            "greedy_size": len(sel40),
            "gains_hist": dict(sorted(gains40.items())),
            "leftover_rows": sorted(left40),
            "lower_bound_rows": lb40,
            "max_matching": msize40,
            "probes_two_orderings": 2 * len(sel40),
            "stranded_rows": stranded40,
        },
        "scope2_refsolve_need_new_providers": {
            "rows": need_new,
            "greedy_selection": [{"root": g["root"],
                                  "gained_rows": g["gained_rows"],
                                  "covered_rows": g["covered_rows"]}
                                 for g in selN],
            "greedy_size": len(selN),
            "gains_hist": dict(sorted(gainsN.items())),
            "leftover_rows": sorted(leftN),
            "lower_bound_rows": lbN,
            "max_matching": msizeN,
            "probes_two_orderings": 2 * len(selN),
        },
        "per_row_residual40": per_row40,
        "gates": gates,
        "interpretation_guard": interpretation_guard,
        "trust_boundary": ("engine depth-10 verdict soundness + D4 invariance, "
                           "identical to the published verdict corpus; this "
                           "computation runs no probes and closes no rows"),
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    txt = json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print("WROTE", out_path)
    print("sha256", hashlib.sha256(txt.encode("utf-8")).hexdigest())
    print("gates", len(gates), "all ok")


if __name__ == "__main__":
    main()
