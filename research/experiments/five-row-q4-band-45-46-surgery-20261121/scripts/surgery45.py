#!/usr/bin/env python3
r"""Complete bounded-edit surgery for the (5,4) fixed-width lane (m=45 hunt).

Companion to engine_v2.py (pinned sha256 99bd45ae..., byte-identical to the
published five-row-q4-band-41plus / six-row-q4-m47-m51 scripts).  The engine
is NOT modified; this module subclasses its Surgery to close a coverage-mode
gap found while reproducing the published K1209 positive control:

  Engine 2-addition classes (kR2A) propose an addition z for cell u only when
  z lies on a curve through u and a *pair of surviving stones*.  A final-set
  cell u can however also be blocked by the triple {survivor s, y, z}, i.e.
  one survivor plus BOTH additions (mode (d) below).  On the published K1209
  m39->m40 run this is not a corner case: 2 of the 16 witness stone sets per
  D4 base are blocked exclusively in mode (d) (engine finds 14/16; K1213's
  "case-c" diagnosis on the six-row 56/64 control is the same phenomenon).

Complete coverage mode table for a cell u uncovered by the removal-only
config (q = 4, a blocking curve through u needs 3 stones of the FINAL set):
  (a) 3 survivors on one curve through u   -- already in blocked_mask / U
  (b) 2 survivors + y  (per-member Y[u], engine)
  (c) 2 survivors + z  (per-member, engine)
  (d) 1 survivor + y + z (joint, added here)
  (e) occupancy: u == y or u == z          (engine, kept)
  No other mode exists (a blocking triple has at most 2 additions here).
  With one addition (classes kR1A) modes (d)/(e') cannot occur: the engine's
  single-addition classes are therefore already complete.

Extra completeness item handled here: unordered pairs (y, z) are enumerated
once with y = lower bit index; the case remU(y) = [] (y alone covers all U)
is *not* skipped blindly (the engine and K1209 differ here): junk-z pairs
(base = survivors + y, z arbitrary) are enumerated exactly when the kR1A
phase of the SAME removal set verified the 13-stone base as a witness
(row-deficiency is automatic for <= 14 stones on 5 rows); otherwise the base
is unsafe (maximality is implied by remU = [] and deficiency is automatic),
which would make every pair with that base unsafe.  This costs nothing when
the kR1A classes are negative, as in the control.

Joint pool: jpool(u, y) = OR over the rset's SURVIVORS s of the cells of
curve(u, s, y).  This is the EXACT mode-(d) pool, so the pair prefilter
zcand = AND over remU of (Y(u)|bit(u)|jpool(u,y)) is exact: every surviving
z reaches the final verifier as a true candidate.  (An earlier draft used
the all-seed-stone superset pool: equally sound and complete -- every
candidate was re-verified -- but it pushed ~21,500 junk pairs per control
base into verify_config, 160 s/base; the exact pool reproduced the same
16/16 control result.)

Hazard fixed from the first draft: after a removal, the REMOVED stone's own
cell can appear in U, and a removed cell can be picked as y; then curve(u, s,
y) with s equal to u or y degenerates and triple_cells walks a (0,0)-direction
"line" forever (the first draft died in an OOM loop this way).  Such s is
skipped: it is not a survivor, so no valid blocking triple is lost (zjo only
over-counts).

Fast exact arithmetic: integer Cramer circle coefficients (no Fractions) and
per-row quadratic root solving with math.isqrt; masks cached per curve.
Cross-checked against engine_v2.triple_curve / curve_cells on the first
_CURVE_XCHECK distinct curves of every process (assert, fail loudly).

Classes covered for rem_budget = B: kR1A for k = 1..B and kR2A for k = 2..B,
complete as argued.  Provably empty classes are not searched: at w=5, q=4 any
set with > 14 stones saturates all rows to 3 (row capacity q-1) and cannot be
row-deficient, so addition-only edits and 1R2A (15 stones) are impossible;
k-removal 0-addition edits leave uncovered cells (removals only shrink the
blocked set) and cannot be maximal.

Determinism: sorted iteration everywhere, JSON sort_keys; reruns expected
byte-identical.

Usage:
  surgery45.py control <seed.json> <published-main.json> <out.json>
  surgery45.py main <census.json> <out.jsonl> [--minR 41] [--budget 2]
                    [--limit N] [--only "seed/img/shift[,...]"]
"""
import json
import math
import os
import sys
import time
import itertools

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine_v2
from engine_v2 import verify_config

_CURVE_XCHECK = 5000
_xchecks = [0]          # completed engine-equality checks
_xcheck_bad = [0]


# ------------------------------------------------- fast exact curve machinery

def triple_curve_fast(p1, p2, p3):
    """Canonical (kind, desc) for the curve through 3 distinct integer
    points.  Circle desc (a,b,c,d) with a > 0 and gcd(a,|b|,|c|,|d|) = 1;
    line desc (dx, dy, x1, y1) primitive, base point canonical (smallest
    of the three points).  Matches engine_v2 curve identity exactly on
    circles; line descs may differ in the base point, which is irrelevant:
    lines are compared only through their full cell masks (cache key below
    uses the curated desc plus both the fast and engine desc sets are
    xchecked)."""
    pts = sorted((p1, p2, p3))
    (x1, y1), (x2, y2), (x3, y3) = pts
    det = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    if det == 0:
        dx, dy = x2 - x1, y2 - y1
        g = math.gcd(abs(dx), abs(dy)) or 1
        return ("line", (dx // g, dy // g, x1, y1))
    f1 = x1 * x1 + y1 * y1
    f2 = x2 * x2 + y2 * y2
    f3 = x3 * x3 + y3 * y3
    a11, a12 = x2 - x1, y2 - y1
    a21, a22 = x3 - x1, y3 - y1
    b1 = -(f2 - f1)
    b2 = -(f3 - f1)
    # Cramer numerators over det (integer)
    bn = b1 * a22 - b2 * a12
    cn = a11 * b2 - a21 * b1
    dn = -(f1 * det) - bn * x1 - cn * y1
    g = math.gcd(math.gcd(abs(det), abs(bn)), math.gcd(abs(cn), abs(dn))) or 1
    a, b, c, d = det // g, bn // g, cn // g, dn // g
    if a < 0:
        a, b, c, d = -a, -b, -c, -d
    assert a > 0
    return ("circle", (a, b, c, d))


def _circle_cells(a, b, c, d, w, m):
    """Exact cells on a*(x^2+y^2)+b*x+c*y+d == 0 within the board."""
    out = []
    if a == 0:                      # cannot happen for real circles
        raise AssertionError("degenerate circle desc")
    for y in range(w):
        k = a * y * y + c * y + d
        disc = b * b - 4 * a * k
        if disc < 0:
            continue
        r = math.isqrt(disc)
        if r * r != disc:
            continue
        nums = (-b - r, -b + r) if r else (-b,)
        for num in nums:
            if num % (2 * a) == 0:
                x = num // (2 * a)
                if 0 <= x < m:
                    out.append((x, y))
    out.sort()
    return out


_curve_mask_cache = {}


def curve_mask(kind, desc, w, m):
    key = (kind, desc, w, m)
    got = _curve_mask_cache.get(key)
    if got is not None:
        return got
    if kind == "line":
        dx, dy, x1, y1 = desc
        cells = engine_v2.line_cells((x1, y1), (x1 + dx, y1 + dy), w, m)
    else:
        cells = _circle_cells(*desc, w, m)
    mask = 0
    if _xchecks[0] < _CURVE_XCHECK:
        if kind == "circle":
            ref = engine_v2.curve_cells(kind, desc, w, m)
        else:
            dx, dy, x1, y1 = desc
            ref = engine_v2.line_cells((x1, y1), (x1 + dx, y1 + dy), w, m)
        if sorted(ref) != sorted(cells):
            _xcheck_bad[0] += 1
            raise AssertionError(
                "curve cells mismatch for %s %s" % (kind, desc))
        _xchecks[0] += 1
    for (x, y) in cells:
        mask |= 1 << (x * w + y)
    _curve_mask_cache[key] = mask
    return mask


class SurgeryJoint(engine_v2.Surgery):

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.jmask_cache = {}

    def jmask(self, u, s, y):
        """Bitmask of the board cells on the curve through the three
        distinct points (u, s, y).  Symmetric cache (the curve does not
        depend on the argument order)."""
        key = tuple(sorted((u, s, y)))
        got = self.jmask_cache.get(key)
        if got is None:
            kind, desc = triple_curve_fast(u, s, y)
            got = curve_mask(kind, desc, self.wb, self.mb)
            self.jmask_cache[key] = got
        return got

    def jpool(self, u, y, surv):
        """EXACT joint-coverage pool for z given the rset's survivors:
        cells z such that some survivor s lies on a common curve through
        u, y, z (blocking mode (d): {s, y, z} on one curve through u).
        Exact means prefilter survivors are true candidates, so the final
        verifier is called only on genuine ones."""
        j = 0
        for s in surv:
            j |= self.jmask(u, s, y)
        return j

    def run(self, rem_budget=2):
        board_w, board_m = self.wb, self.mb
        out = dict(w=self.w, m_seed=self.m_seed, q=self.q,
                   m_target=self.m_target,
                   seedStones=[[s[0], s[1]] for s in self.seed],
                   remBudget=rem_budget, witnesses=[], counts={},
                   finalChecks=0, maxUncovered=0,
                   engine="SurgeryJoint-3",
                   curveChecks=_xchecks[0], curveCheckBad=_xcheck_bad[0])
        witnesses, seen = out["witnesses"], set()
        seed = self.seed
        bw = board_w

        def cd(label, key):
            d = out["counts"].setdefault(
                label, dict(rsets=0, uncoveredCells=0, **{key: 0},
                            passingPrefilter=0, witnesses=0))
            return d

        for k in range(1, rem_budget + 1):
            labels1 = "%dR1A" % k
            for rem in itertools.combinations(range(self.n), k):
                surv = [seed[i] for i in range(self.n) if i not in rem]
                surv_mask = 0
                for s in surv:
                    surv_mask |= self.bit(s)
                blocked = self.blocked_mask(rem)
                unc_mask = self.full_mask & ~blocked & ~surv_mask
                U = []
                mm = unc_mask
                while mm:
                    b = mm & (-mm)
                    idx = b.bit_length() - 1
                    U.append((idx // bw, idx % bw))
                    mm ^= b
                d1 = cd(labels1, "singleCandidates")
                d1["rsets"] += 1
                d1["uncoveredCells"] += len(U)
                out["maxUncovered"] = max(out["maxUncovered"], len(U))
                if not U:
                    continue
                pairs = list(itertools.combinations(surv, 2))
                Y = {}
                for u in U:
                    mk = 0
                    for (p1, p2) in pairs:
                        mk |= self.cover_mask(p1, p2, u)
                    Y[u] = mk
                empty = self.full_mask & ~surv_mask
                u0 = U[0]
                # ---- class (k,1): single addition (engine-complete)
                cands = (Y[u0] | self.bit(u0)) & empty
                order = []
                mm = cands
                while mm:
                    b = mm & (-mm)
                    idx = b.bit_length() - 1
                    order.append((idx // bw, idx % bw))
                    mm ^= b
                d1["singleCandidates"] += len(order)
                vok = {}
                for y in order:
                    by = self.bit(y)
                    if not all((u == y) or (Y[u] & by) for u in U):
                        continue
                    d1["passingPrefilter"] += 1
                    S2 = sorted(surv + [y])
                    key = tuple(S2)
                    if key in seen:
                        continue
                    out["finalChecks"] += 1
                    res = verify_config(S2, self.w, board_m, self.q)
                    vok[y] = bool(res["ok"])
                    if res["ok"]:
                        seen.add(key)
                        witnesses.append(dict(
                            stones=[[s[0], s[1]] for s in S2],
                            rows=res["rows"], n=res["n"], cls=labels1))
                        d1["witnesses"] += 1
                # ---- class (k,2): pair additions, complete modes (a)-(e)
                if k < 2:
                    continue
                label2 = "%dR2A" % k
                d2 = cd(label2, "pairCandidates")
                d2["rsets"] += 1
                d2["uncoveredCells"] += len(U)
                ymask = {u: (Y[u] | self.bit(u)) for u in U}
                mm = empty
                while mm:
                    b = mm & (-mm)
                    mm ^= b
                    yidx = b.bit_length() - 1
                    y = (yidx // bw, yidx % bw)
                    remU = [u for u in U if u != y and not (Y[u] & b)]
                    if not remU:
                        if vok.get(y):
                            # base = survivors + y is a 13-stone witness:
                            # maximality and deficiency are then automatic
                            # and only safety of S2 must be checked.
                            zpool = empty & ~b & ~((1 << (yidx + 1)) - 1)
                            mmz = zpool
                            while mmz:
                                bz = mmz & (-mmz)
                                mmz ^= bz
                                zidx = bz.bit_length() - 1
                                z = (zidx // bw, zidx % bw)
                                d2["pairCandidates"] += 1
                                S2 = sorted(surv + [y, z])
                                key = tuple(S2)
                                if key in seen:
                                    continue
                                out["finalChecks"] += 1
                                res = verify_config(S2, self.w, board_m,
                                                    self.q)
                                if res["ok"]:
                                    seen.add(key)
                                    witnesses.append(dict(
                                        stones=[[s[0], s[1]] for s in S2],
                                        rows=res["rows"], n=res["n"],
                                        cls=label2 + "-junkz"))
                                    d2["witnesses"] += 1
                        continue
                    zcand = empty & ~b & ~((1 << (yidx + 1)) - 1)
                    for u in remU:
                        zcand &= (ymask[u] | self.jpool(u, y, surv))
                    mmz = zcand
                    while mmz:
                        bz = mmz & (-mmz)
                        mmz ^= bz
                        zidx = bz.bit_length() - 1
                        z = (zidx // bw, zidx % bw)
                        d2["pairCandidates"] += 1
                        S2 = sorted(surv + [y, z])
                        key = tuple(S2)
                        if key in seen:
                            continue
                        out["finalChecks"] += 1
                        res = verify_config(S2, self.w, board_m, self.q)
                        if res["ok"]:
                            seen.add(key)
                            witnesses.append(dict(
                                stones=[[s[0], s[1]] for s in S2],
                                rows=res["rows"], n=res["n"], cls=label2))
                            d2["witnesses"] += 1
        return out


# ------------------------------------------------------------------ control

def do_control(seed_path, pub_path, out_path):
    seed = json.load(open(seed_path))
    pub = json.load(open(pub_path))
    W, Q, M_T, M_S = 5, 4, 40, 38

    def d4(stones, img):
        out = []
        for (x, y) in stones:
            nx = (M_T - 1 - x) if img in ("H", "HV") else x
            ny = (W - 1 - y) if img in ("V", "HV") else y
            out.append([nx, ny])
        return sorted(out)

    def fs(stones):
        return frozenset(map(tuple, stones))

    pub_by_base = {}
    for r in pub["results"]:
        pub_by_base.setdefault(r["base"], set()).add(fs(r["stones"]))

    out = {"mode": "control", "w": W, "q": Q, "m_seed": M_S,
           "m_target": M_T, "engine": "SurgeryJoint-3", "remBudget": 2,
           "curveChecks": _xchecks[0], "curveCheckBad": _xcheck_bad[0],
           "bases": {}, "setEquality": {}, "summary": {}}
    t0 = time.time()
    for img in ("id", "H", "V", "HV"):
        base = d4(seed, img)
        r = SurgeryJoint(W, M_S, Q, base, M_T).run(rem_budget=2)
        wit2 = [fs(w["stones"]) for w in r["witnesses"]
                if w["cls"] == "2R2A"]
        witall = [fs(w["stones"]) for w in r["witnesses"]]
        eq = set(wit2) == pub_by_base.get("m39/" + img, set())
        out["bases"]["m39/" + img] = {
            "counts": r["counts"], "finalChecks": r["finalChecks"],
            "maxUncovered": r["maxUncovered"],
            "witnessesByClass": {
                c: sum(1 for w in r["witnesses"] if w["cls"] == c)
                for c in sorted({w["cls"] for w in r["witnesses"]})},
            "witnessStones": sorted(sorted(w["stones"])
                                    for w in r["witnesses"]),
        }
        out["setEquality"]["m39/" + img] = bool(eq)
        out["summary"]["m39/" + img] = {
            "engine2R2A": len(wit2), "engineAll": len(witall),
            "published": len(pub_by_base.get("m39/" + img, set())),
            "equal": bool(eq)}
        out["allPartial"] = all(out["setEquality"].values())
        json.dump(out, open(out_path, "w"), sort_keys=True, indent=1)
        print(img, out["summary"]["m39/" + img],
              "compat", round(time.time() - t0, 1), "s", flush=True)
    out["allEqual"] = all(out["setEquality"].values())
    out["curveChecks"] = _xchecks[0]
    out["curveCheckBad"] = _xcheck_bad[0]
    json.dump(out, open(out_path, "w"), sort_keys=True, indent=1)
    print("ALL_EQUAL", out["allEqual"], "compat", round(time.time() - t0, 1),
          "s curveChecks", _xchecks[0], "bad", _xcheck_bad[0], flush=True)


# --------------------------------------------------------------------- main

def do_main(census_path, out_path, min_r, budget, limit, only, m_target):
    c = json.load(open(census_path))
    assert (c["w"], c["q"]) == (5, 4)
    done = set()
    if os.path.exists(out_path):
        for line in open(out_path):
            line = line.strip()
            if line:
                done.add(json.loads(line)["key"])
    sel = [p for p in c["placements"] if p["R"] >= min_r and
           all(0 <= x[0] < m_target for x in p["stones"])]
    sel.sort(key=lambda p: (-p["R"], p["seed"], p["image"], p["shift"]))
    if only:
        want = set(tuple(s.split("/")) for s in only.split(","))
        sel = [p for p in sel if (p["seed"], p["image"], str(p["shift"]))
               in want]
    if limit:
        sel = sel[:limit]
    print("selected", len(sel), "placements; done", len(done), flush=True)
    f = open(out_path, "a")
    for p in sel:
        key = "%s/%s/%d" % (p["seed"], p["image"], p["shift"])
        if key in done:
            print("skip", key, flush=True)
            continue
        t0 = time.time()
        r = SurgeryJoint(5, m_target, 4, [tuple(s) for s in p["stones"]],
                         m_target).run(rem_budget=budget)
        rec = dict(key=key, R=p["R"], firstUncovered=p["firstUncovered"],
                   counts=r["counts"], finalChecks=r["finalChecks"],
                   maxUncovered=r["maxUncovered"],
                   curveChecks=_xchecks[0], curveCheckBad=_xcheck_bad[0],
                   witnessesByClass={
                       cl: sum(1 for w in r["witnesses"] if w["cls"] == cl)
                       for cl in sorted({w["cls"]
                                         for w in r["witnesses"]})},
                   witnesses=r["witnesses"])
        f.write(json.dumps(rec, sort_keys=True) + "\n")
        f.flush()
        print(key, "R=", p["R"], "wits=", rec["witnessesByClass"],
              "checks=", r["finalChecks"],
              "secs=", round(time.time() - t0, 1), flush=True)
    f.close()


def _main():
    mode = sys.argv[1]
    if mode == "control":
        do_control(sys.argv[2], sys.argv[3], sys.argv[4])
    elif mode == "main":
        args = sys.argv[2:]
        census_path, out_path = args[0], args[1]
        kw = {}
        i = 2
        while i < len(args):
            if args[i] == "--minR":
                kw["min_r"] = int(args[i + 1]); i += 2
            elif args[i] == "--budget":
                kw["budget"] = int(args[i + 1]); i += 2
            elif args[i] == "--limit":
                kw["limit"] = int(args[i + 1]); i += 2
            elif args[i] == "--only":
                kw["only"] = args[i + 1]; i += 2
            elif args[i] == "--mtarget":
                kw["m_target"] = int(args[i + 1]); i += 2
            else:
                raise SystemExit("bad arg " + args[i])
        do_main(census_path, out_path, kw.get("min_r", 41),
                kw.get("budget", 2), kw.get("limit"), kw.get("only"),
                kw.get("m_target", 45))
    else:
        raise SystemExit("unknown mode")


if __name__ == "__main__":
    _main()
