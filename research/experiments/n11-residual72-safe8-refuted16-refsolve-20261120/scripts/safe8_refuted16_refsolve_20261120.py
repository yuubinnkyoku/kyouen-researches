#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
safe8 pool re-solve after excluding the 16 REFUTED-D10 roots of the K1086
depth-10 sweep of the 23 greedy add-two candidate roots (2026-11-20).

Single-owner item declared in:
  research/log/2026-11-20-n11-residual72-safe8-refuted16-refsolve-single-owner-note.md

Inputs (fail-closed SHA-256 pins):
  * K1085 census正本: research/experiments/n11-residual72-unsafe-classification-add2stones-20261120/
      output/residual72-unsafe-classification-add2stones-20261120.json
      SHA-256 5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e
  * K1086 sweep正本: research/experiments/n11-residual72-addtwo-greedy23-d10-sweep-20261120/
      output/addtwo-greedy23-d10-sweep-20261120.json
      SHA-256 3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced

The machine re-derives, independently of the K1085 experiment machine:
  Stage B  the add-two universe (72 residual rows x all pairs of empty cells,
           generation witness -> canonical dedup), unsafe8 via exact integer
           4x4 determinants (D-memo triple form), safe8 pool, coverage,
           per-row demand, and the lexicographically-smallest max-gain greedy
           set cover of the 72 rows (must reproduce the published 23 roots),
  Stage C  the K1086 verdict join (7 WIN8-D10 candidates / 16 REFUTED-D10
           facts, both orderings uncapped; claimed-coverage canonization) and
           the residual-49 row extraction,
  Stage D  the post-exclusion re-solve: pool P = safe8 minus the 16 REFUTED
           roots; per-row demand over P; stranded (zero-demand) rows;
           greedy witness; information lower bound; bipartite maximum
           matching; and the intrinsic-coverage footprints of the 7 WIN8
           candidates over the residual-49 rows (geometry facts only).

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

K1085_DEFAULT = os.path.join(
    HERE, "..", "..", "..", "..",
    "home_is_not_used")
# resolved at runtime via env or --k1085 / --k1086 (both mandatory below)


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
            e_ij = xi * yj - xj * yi
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
    out_path = opt("--out") or os.path.join(HERE, "output",
                                            "safe8-refuted16-refsolve-20261120.json")
    need(k1085_path and os.path.isfile(k1085_path), "K1085 input required")
    need(k1086_path and os.path.isfile(k1086_path), "K1086 input required")

    k1085 = load_pinned(k1085_path, K1085_SHA256, "K1085")
    k1086 = load_pinned(k1086_path, K1086_SHA256, "K1086")

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
    # quad-free rows via the 4x4 determinant (6 stones -> C(6,4)=15 quads)
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

    # coverage crosscheck: all multi-coverage safe8 roots + every 60th root
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

    # greedy reproduction (full safe8 pool; published rule)
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

    # ---- Stage C: K1086 verdict join ----------------------------------------
    cl = k1086["classification"]
    win7 = sorted(e["root"] for e in cl["win8_d10_candidates"])
    ref16 = sorted(e["root"] for e in cl["refuted_d10_facts"])
    need(len(win7) == 7 and len(ref16) == 16 and not (set(win7) & set(ref16)),
         "K1086 classification sizes")
    per_root = k1086["per_root"]
    def probe(root, ordering):
        return per_root[root]["probes"].get(ordering)
    ok_verdicts = True
    for r in win7:
        for o in ("andclose1", "andclose0"):
            pr = probe(r, o)
            ok_verdicts = ok_verdicts and pr is not None and pr["loss"] is True \
                and pr["capped"] is False
    for r in ref16:
        for o in ("andclose1", "andclose0"):
            pr = probe(r, o)
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
          "sum_claims_partition_72rows": True,
          "note": ("the greedy plan partitions the 72 rows exactly: the 7 "
                   "WIN candidates claim 23 rows, the 16 REFUTED roots claim "
                   "the complementary 49 rows")})

    # ---- Stage D: post-exclusion re-solve -----------------------------------
    P = [c for c in safe8 if c not in set(ref16)]
    need(len(P) == 120458, "pool size after exclusion")
    gate("pool-P-size", len(P) == 120458, {"safe8": 120474,
                                           "excluded_refuted": 16,
                                           "P": len(P)})

    demandP = Counter()
    for c in P:
        for r in wcover82[c]:
            demandP[r] += 1
    d49 = [demandP[r] for r in residual49]
    stranded49 = [r for r in residual49 if demandP[r] == 0]
    hist49 = Counter(d49)
    hist_rows = Counter(len(wcover82[c] & set(residual49)) for c in P
                        if wcover82[c] & set(residual49))
    gate("residual49-demand-on-P", True,
         {"min": min(d49), "max": max(d49), "sum": sum(d49),
          "stranded_rows": len(stranded49), "stranded_hex": stranded49,
          "demand_hist_over_49_rows": dict(sorted(hist49.items())),
          "provider_coverage_hist_over_49rows":
              dict(sorted(hist_rows.items())),
          "providers_touching_49rows": sum(hist_rows.values())})

    # intrinsic coverage footprints of the WIN8 candidates
    win_foot = {}
    for r in win7:
        full = coverage_of82(r, residualSet72)
        win_foot[r] = {"claimed": sorted(pubc[r]),
                       "intrinsic": sorted(full)}
    extra = {}
    for r in win7:
        ex = [row for row in win_foot[r]["intrinsic"] if row not in pubc[r]]
        if ex:
            extra[r] = ex
    # rows of the residual 49 covered intrinsically by some WIN candidate
    win_cover49 = {}
    for row in residual49:
        covs = [r for r in win7 if row in win_foot[r]["intrinsic"]]
        if covs:
            win_cover49[row] = sorted(covs)
    need_new = [r for r in residual49 if r not in win_cover49]
    gate("win8-intrinsic-footprints", True,
         {"win_roots_with_extra_intrinsic_rows": len(extra),
          "win8_intrinsic_extra_rows": {k: sorted(v) for k, v in sorted(extra.items())},
          "residual49_covered_by_win8_intrinsic": len(win_cover49),
          "residual49_remaining_after_win8_intrinsic": len(need_new),
          "note": ("intrinsic coverage = full C(8,6) subset re-derivation; "
                   "a residual-49 row inside a WIN candidate's intrinsic "
                   "coverage is a geometry fact only: it would need that "
                   "root's certificate extraction AND receipt fold to close; "
                   "nothing is closed here")})

    # scope 1 re-solve: all 49 residual rows, pool P
    sel49, left49 = greedy_cover(P, wcover82, residual49)
    gains49 = Counter(g["gained_rows"] for g in sel49)
    lb49 = -(-49 // 4)
    msize49, _ = max_matching(residual49, P, wcover82)
    gate("scope1-greedy-re-solve-49rows", True,
         {"greedy_size": len(sel49), "leftover_rows": len(left49),
          "leftover_hex": sorted(left49),
          "gains_hist": dict(sorted(gains49.items())),
          "lower_bound_rows": lb49,
          "max_matching_rows_roots": msize49,
          "plan_probes_two_orderings": 2 * len(sel49),
          "stranded_rows_under_P": len(stranded49),
          "selection": [{"root": g["root"], "gained_rows": g["gained_rows"],
                         "covered_rows": g["covered_rows"]} for g in sel49]})

    # scope 2 re-solve: rows that need a NEW provider even if every WIN8
    # candidate's future receipt folds the rows it intrinsically covers
    selN, leftN = greedy_cover([c for c in P if c not in set(win7)],
                                wcover82, need_new)
    gainsN = Counter(g["gained_rows"] for g in selN)
    msizeN, _ = max_matching(need_new, [c for c in P if c not in set(win7)],
                             wcover82)
    lbN = -(-len(need_new) // 4)
    gate("scope2-re-solve-post-win8-intrinsic", True,
         {"rows": len(need_new),
          "row_hex": need_new,
          "greedy_size": len(selN), "leftover_rows": len(leftN),
          "leftover_hex": sorted(leftN),
          "gains_hist": dict(sorted(gainsN.items())),
          "lower_bound_rows": lbN,
          "max_matching_rows_roots": msizeN,
          "plan_probes_two_orderings": 2 * len(selN),
          "selection": [{"root": g["root"], "gained_rows": g["gained_rows"],
                         "covered_rows": g["covered_rows"]} for g in selN]})

    # per-row table for the residual 49
    provider_rows = {}
    per_row49 = []
    for row in residual49:
        ent = {
            "row": row,
            "demand_P": demandP[row],
            "demand_drop_from_safe8": demand8[row] - demandP[row],
            "stranded_under_P": row in stranded49,
            "win8_intrinsic_cover": win_cover49.get(row, []),
            "greedy_provider": next((g["root"] for g in sel49
                                     if row in wcover82[g["root"]]), None),
            "refuted_plan_provider": next((r for r in ref16
                                            if row in pubc[r]), None),
        }
        per_row49.append(ent)
    gate("per-row-table-complete",
         len(per_row49) == 49
         and sum(1 for e in per_row49 if e["greedy_provider"]) ==
             49 - len(left49),
         {"rows": len(per_row49),
          "with_greedy_provider": sum(1 for e in per_row49
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
        "schema": "n11-residual72-safe8-refuted16-refsolve-20261120-v1",
        "date": "2026-11-20",
        "status": "refsolve-computed",
        "single_owner_note": ("research/log/2026-11-20-n11-residual72-"
                              "safe8-refuted16-refsolve-single-owner-note.md"),
        "inputs": {
            "k1085_census_sha256": K1085_SHA256,
            "k1086_sweep_sha256": K1086_SHA256,
            "k1069_depth10_protocol_reference": "runner v17, cap 30M",
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
        "exclusion": {
            "refuted_d10_roots_excluded": ref16,
            "win8_d10_candidates": win7,
            "pool_P_size": len(P),
            "residual49_rows": residual49,
        },
        "win8_intrinsic_footprints": win_foot,
        "scope1_refsolve_residual49": {
            "greedy_selection": [{"root": g["root"],
                                  "gained_rows": g["gained_rows"],
                                  "covered_rows": g["covered_rows"]}
                                 for g in sel49],
            "greedy_size": len(sel49),
            "gains_hist": dict(sorted(gains49.items())),
            "leftover_rows": sorted(left49),
            "lower_bound_rows": lb49,
            "max_matching": msize49,
            "probes_two_orderings": 2 * len(sel49),
            "stranded_rows": stranded49,
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
        "per_row_residual49": per_row49,
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
