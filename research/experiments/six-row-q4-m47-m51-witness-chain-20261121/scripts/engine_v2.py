#!/usr/bin/env python3
r"""Clean-room rebuild (engine v2) for the (6,4) m=47/48 witness chain lane.

Single-owner lane declaration:
research/log/2026-11-21-six-row-q4-m47-witness-surgery-single-owner-note.md
(acceptance: positive control = replication of the K1209 (5,4) m=39 ->
m=40 rem2add2 results at the stone-set level; >= 2 independent integer
verification families; deterministic byte-identical reruns; lower-bound
updates only; no global-absence claims).

Provenance: the discovery-time engine ("engine v1") and its raw outputs
were lost to an execution-environment reset BEFORE publication. Engine v2
was rewritten from scratch from the mathematical definitions; every
published claim is re-derived and re-verified under engine v2 with its
own self-tests and positive controls.

Definitions (q-point kyouen; curves = circles and lines; q = 4 here):
- safe      : no curve contains q = 4 stones of the configuration
- blocked c : empty cell c is blocked iff some curve contains c and
              >= q-1 = 3 stones
- maximal   : every board cell is a stone or blocked
- witness   : safe, maximal, row-deficient (some row holds < q-1 stones)
- R(placement), strip version: the first strip cell (column-major order,
  x growing, y = 0..w-1) that is not covered; all columns left of it being
  covered certifies witness-hood for every board width <= R (width-
  monotone coverage for a fixed stone set: the K0853/K1209 criterion).

Surgery edit classes enumerated (removes from the seed frame, adds on the
target board): 1R1A, 2R1A, 2R2A, and (escalation budget, offs by default)
3R1A and 3R2A, each exhaustively searched (class-complete within its
class). |A| >= 1 is forced: the transplant leaves the frontier cell
uncovered and removals never create coverage. Classes with |A| > |R|,
|R|+|A| > 5, and pair coverage relying on a single surviving stone (the
det4 == 0 concyclicity of one survivor with both additions) are NOT
searched; bounded negative records are explicitly scoped to the declared
classes only.

Determinism: iteration over sorted lists everywhere; output JSON with
sort_keys; artifacts rerun 2x and byte-compared before publication.

Exact arithmetic: Python ints and Fractions. Curves through integer
points as integer equations; the 4x4 determinant criterion
det[(x, y, x^2+y^2, 1)] == 0 is used for independent safety checks.
"""
import itertools, json, math, sys
from fractions import Fraction

# ---------------------------------------------------------------- curves

def line_cells(p, q, w, m):
    """All cells (x in [0,m), y in [0,w)) on the line through p != q."""
    (x1, y1), (x2, y2) = p, q
    dx, dy = x2 - x1, y2 - y1
    g = math.gcd(abs(dx), abs(dy)) or 1
    dx //= g; dy //= g
    out = []
    x, y = x1, y1
    while 0 <= x < m and 0 <= y < w:
        out.append((x, y)); x += dx; y += dy
    x, y = x1 - dx, y1 - dy
    while 0 <= x < m and 0 <= y < w:
        out.append((x, y)); x -= dx; y -= dy
    return out

def circle_coeffs(p1, p2, p3):
    """Integer circle equation a*(x^2+y^2)+b*x+c*y+d == 0, a>0, gcd 1.
    Raises ValueError if collinear."""
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    a11, a12 = x2 - x1, y2 - y1
    a21, a22 = x3 - x1, y3 - y1
    det = a11 * a22 - a12 * a21
    if det == 0:
        raise ValueError("collinear")
    b1 = -(x2 * x2 + y2 * y2) + (x1 * x1 + y1 * y1)
    b2 = -(x3 * x3 + y3 * y3) + (x1 * x1 + y1 * y1)
    # Cramer for D,E with exact rationals
    D = Fraction(b1 * a22 - b2 * a12, det)
    E = Fraction(a11 * b2 - a21 * b1, det)
    F = Fraction(-(x1 * x1 + y1 * y1)) - D * x1 - E * y1
    den = 1
    for v in (D, E, F):
        den = den * v.denominator // math.gcd(den, v.denominator)
    A = den; B = int(D * den); C = int(E * den); Dd = int(F * den)
    g = math.gcd(A, math.gcd(abs(B), math.gcd(abs(C), abs(Dd)))) or 1
    A //= g; B //= g; C //= g; Dd //= g
    if A < 0:
        A, B, C, Dd = -A, -B, -C, -Dd
    return (A, B, C, Dd)

def triple_curve(p1, p2, p3):
    """(kind, desc) for the unique curve through 3 pairwise-distinct
    integer points: ('line', (dx, dy, x1, y1)) or ('circle', (a,b,c,d))."""
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    if (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1) == 0:
        dx, dy = x2 - x1, y2 - y1
        g = math.gcd(abs(dx), abs(dy)) or 1
        return ("line", (dx // g, dy // g, x1, y1))
    return ("circle", circle_coeffs(p1, p2, p3))

def curve_has(kind, desc, cell):
    (x, y) = cell
    if kind == "line":
        dx, dy, x1, y1 = desc
        return dx * (y - y1) == dy * (x - x1)
    a, b, c, d = desc
    return a * (x * x + y * y) + b * x + c * y + d == 0

def curve_cells(kind, desc, w, m):
    """Cells on the curve within x in [0,m), y in [0,w)."""
    if kind == "line":
        return line_cells((desc[2], desc[3]),
                          (desc[2] + desc[0], desc[3] + desc[1]), w, m)
    a, b, c, d = desc
    out = []
    for x in range(m):
        xx = x * x
        for y in range(w):
            if a * (xx + y * y) + b * x + c * y + d == 0:
                out.append((x, y))
    return out

def triple_cells(p1, p2, p3, w, m):
    kind, desc = triple_curve(p1, p2, p3)
    return kind, desc, curve_cells(kind, desc, w, m)

# ---------------------------------------------------------------- verifier

def det4(rows):
    """Exact integer determinant of a 4x4 matrix (Bareiss, pivoting)."""
    a = [list(r) for r in rows]
    n = 4
    sign = 1
    prev = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            swap = None
            for i in range(k + 1, n):
                if a[i][k] != 0:
                    swap = i; break
            if swap is None:
                return 0
            a[k], a[swap] = a[swap], a[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // prev
        prev = a[k][k]
    return sign * a[n - 1][n - 1]

def verify_config(stones, w, m, q):
    """Full from-scratch verification (independent codepath: det4 safety
    + per-cell triple-descriptor blocking). stones: iterable of [x, y]."""
    st = sorted((int(x), int(y)) for (x, y) in stones)
    n = len(st)
    assert len(set(st)) == n
    for (x, y) in st:
        assert 0 <= x < m and 0 <= y < w, (x, y)
    res = dict(w=w, m=m, q=q, n=n, safe=True, maximal=True, rows=None,
               rowDeficient=None, ok=None, uncovered=[])
    for quad in itertools.combinations(st, q):
        xs = [p[0] for p in quad]; ys = [p[1] for p in quad]
        ss = [x * x + y * y for (x, y) in quad]
        if det4([[xs[i], ys[i], ss[i], 1] for i in range(q)]) == 0:
            res["safe"] = False
            break
    rowcount = [0] * w
    for (_, y) in st:
        rowcount[y] += 1
    res["rows"] = rowcount
    res["rowDeficient"] = min(rowcount) < q - 1
    descriptors = [triple_curve(*tri) for tri in itertools.combinations(st, q - 1)]
    stset = set(st)
    unc = []
    for x in range(m):
        for y in range(w):
            c = (x, y)
            if c in stset:
                continue
            blocked = False
            for (kind, desc) in descriptors:
                if curve_has(kind, desc, c):
                    blocked = True
                    break
            if not blocked:
                unc.append([x, y])
    res["uncovered"] = unc
    res["maximal"] = len(unc) == 0
    res["ok"] = bool(res["safe"] and res["maximal"] and res["rowDeficient"])
    return res

# ---------------------------------------------------------------- surgery

class Surgery:
    """Bounded-edit surgery, seed frame w x m_seed -> target w x m_target.

    Internals: triple-curve registry as integer bitmasks over the target
    board (bit x*w + y); coverage of the uncovered set U by candidate
    additions via pair-coverage masks cached per (ordered pair, cell).
    Final check of every prefilter survivor is a from-scratch
    verify_config (independent codepath).
    """

    def __init__(self, w, m_seed, q, seed_stones, m_target):
        assert q == 4
        self.w, self.q = w, q
        self.m_seed, self.m_target = m_seed, m_target
        self.seed = sorted((int(x), int(y)) for (x, y) in seed_stones)
        for (x, y) in self.seed:
            assert 0 <= x < m_seed and 0 <= y < w
        self.n = len(self.seed)
        self.seed_index = {s: i for i, s in enumerate(self.seed)}
        self.wb, self.mb = w, m_target
        self.full_mask = (1 << (m_target * w)) - 1
        # triple registry: (triple, mask) on the target board
        self.triples = []
        for tri in itertools.combinations(self.seed, 3):
            kind, desc, cells = triple_cells(*tri, w, m_target)
            mask = 0
            for (x, y) in cells:
                mask |= 1 << (x * w + y)
            self.triples.append((tri, mask))
        # pair coverage cache: (p1, p2, u) -> mask of cells y on a curve
        # with p1, p2, u (y != u)
        self.paircache = {}

    def bit(self, c):
        return 1 << (c[0] * self.w + c[1])

    def blocked_mask(self, removed_idx):
        rem = set(removed_idx)
        out = 0
        for (tri, mask) in self.triples:
            if not mask:
                continue
            if any(self.seed_index[s] in rem for s in tri):
                continue
            out |= mask
        return out

    def cover_mask(self, p1, p2, u):
        key = (p1, p2, u)
        got = self.paircache.get(key)
        if got is None:
            kind, desc, cells = triple_cells(p1, p2, u, self.wb, self.mb)
            got = 0
            for (x, y) in cells:
                got |= 1 << (x * self.wb + y)
            got &= ~self.bit(u)
            self.paircache[key] = got
        return got

    def run(self, rem_budget=2):
        board_w, board_m = self.wb, self.mb
        out = dict(w=self.w, m_seed=self.m_seed, q=self.q,
                   m_target=self.m_target,
                   seedStones=[[s[0], s[1]] for s in self.seed],
                   remBudget=rem_budget, witnesses=[], counts={},
                   finalChecks=0, maxUncovered=0)
        witnesses, seen = out["witnesses"], set()
        seed = self.seed

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
                    U.append((idx // board_w, idx % board_w))
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
                # ---- class (k,1): single addition y covering all U
                cands = (Y[u0] | self.bit(u0)) & empty
                order = []
                mm = cands
                while mm:
                    b = mm & (-mm)
                    idx = b.bit_length() - 1
                    order.append((idx // board_w, idx % board_w))
                    mm ^= b
                d1["singleCandidates"] += len(order)
                for y in order:
                    by = self.bit(y)
                    covered = all((u == y) or (Y[u] & by) for u in U)
                    if not covered:
                        continue
                    d1["passingPrefilter"] += 1
                    out["finalChecks"] += 1
                    S2 = sorted(surv + [y])
                    res = verify_config(S2, self.w, board_m, self.q)
                    if res["ok"] and tuple(S2) not in seen:
                        seen.add(tuple(S2))
                        witnesses.append(dict(
                            stones=[[s[0], s[1]] for s in S2],
                            rows=res["rows"], n=res["n"], cls=labels1))
                        d1["witnesses"] += 1
                # ---- class (k,2): pair additions (the k=2 case is the
                # K1209 class; k=3 is the declared escalation)
                if k < 2:
                    continue
                label2 = "%dR2A" % k
                d2 = cd(label2, "pairCandidates")
                d2["rsets"] += 1
                d2["uncoveredCells"] += len(U)
                ylist = [(u0[0], u0[1])]
                mm = Y[u0] & empty
                while mm:
                    b = mm & (-mm)
                    idx = b.bit_length() - 1
                    ylist.append((idx // board_w, idx % board_w))
                    mm ^= b
                for y in ylist:
                    by = self.bit(y)
                    remU = [u for u in U if u != y and not (Y[u] & by)]
                    if not remU:
                        continue
                    z0 = remU[0]
                    zlist = [(z0[0], z0[1])]
                    mm = Y[z0] & empty & ~by
                    while mm:
                        b = mm & (-mm)
                        idx = b.bit_length() - 1
                        zlist.append((idx // board_w, idx % board_w))
                        mm ^= b
                    for z in zlist:
                        if z == y:
                            continue
                        d2["pairCandidates"] += 1
                        bz = self.bit(z)
                        if not all((u == z) or (Y[u] & bz) for u in remU):
                            continue
                        d2["passingPrefilter"] += 1
                        out["finalChecks"] += 1
                        S2 = sorted(surv + [y, z])
                        res = verify_config(S2, self.w, board_m, self.q)
                        if res["ok"] and tuple(S2) not in seen:
                            seen.add(tuple(S2))
                            witnesses.append(dict(
                                stones=[[s[0], s[1]] for s in S2],
                                rows=res["rows"], n=res["n"], cls=label2))
                            d2["witnesses"] += 1
        return out

def run_surgery(w, m_seed, q, seed_stones, m_target, rem_budget=2):
    return Surgery(w, m_seed, q, seed_stones, m_target).run(rem_budget)

# ---------------------------------------------------------------- census

def fold_images(stones, w):
    xs = [x for (x, _) in stones]
    lo, hi = min(xs), max(xs)
    span = hi - lo
    return span, {
        "id": sorted((x - lo, y) for (x, y) in stones),
        "H":  sorted((span - (x - lo), y) for (x, y) in stones),
        "V":  sorted((x - lo, w - 1 - y) for (x, y) in stones),
        "HV": sorted((span - (x - lo), w - 1 - y) for (x, y) in stones),
    }

def census_placements(seeds, w, q, scan):
    """Exact R(placement) for the 4-image x 0..(scan-1-span) family of
    each seed pattern. Bit layout: column x (>= -LIM) at bit position
    (x + LIM)*w + y with LIM = scan; translations shift by s*w."""
    assert q == 4
    LIM = scan
    full = ((1 << (scan * w)) - 1) << (LIM * w)
    placements = []
    for name in sorted(seeds):
        stones = sorted(map(tuple, seeds[name]))
        span, imgs = fold_images(stones, w)
        for img in ("id", "H", "V", "HV"):
            pat = imgs[img]
            reg = []
            for tri in itertools.combinations(pat, 3):
                kind, desc = triple_curve(*tri)
                mk = 0
                if kind == "line":
                    dx, dy, x1, y1 = desc
                    x, y = x1, y1
                    while -LIM <= x < scan and 0 <= y < w:
                        mk |= 1 << ((x + LIM) * w + y)
                        x += dx; y += dy
                    x, y = x1 - dx, y1 - dy
                    while -LIM <= x < scan and 0 <= y < w:
                        mk |= 1 << ((x + LIM) * w + y)
                        x -= dx; y -= dy
                else:
                    a, b, c, d = desc
                    for x in range(-LIM, scan):
                        xx = x * x
                        for y in range(w):
                            if a * (xx + y * y) + b * x + c * y + d == 0:
                                mk |= 1 << ((x + LIM) * w + y)
                reg.append(mk)
            smask = 0
            for (sx, sy) in pat:
                smask |= 1 << ((sx + LIM) * w + sy)
            for s in range(0, scan - span):
                blk = 0
                for mk in reg:
                    blk |= mk << (s * w)
                st = smask << (s * w)
                unc = full & ~blk & ~st
                pl = dict(seed=name, image=img, shift=s,
                          stones=[[x + s, y] for (x, y) in pat],
                          reached=[]
                          )
                if unc == 0:
                    pl.update(R=scan, firstUncovered=None, scanBound=True)
                else:
                    idx = (unc & (-unc)).bit_length() - 1
                    fx = idx // w - LIM
                    fy = idx % w
                    assert 0 <= fy < w and fx >= 0
                    pl.update(R=fx, firstUncovered=[fx, fy],
                              scanBound=(fx >= scan - 1))
                pl.pop("reached")
                placements.append(pl)
    return placements

# ---------------------------------------------------------------- selftest

SEED_M46 = [[21, 0], [39, 0], [12, 1], [30, 1], [33, 1], [12, 2], [35, 2],
            [38, 2], [8, 3], [31, 3], [33, 3], [7, 4], [15, 4], [33, 4],
            [4, 5], [5, 5], [30, 5]]

def do_selftest():
    """Battery: (a) all 16 published K1209 m40 witnesses verify ok;
    (b) tamper fails; (c) unsafe flagged; (d) m46 seed witness ok;
    (e) calibration R for the published m46 placement."""
    out = {}
    W40 = json.load(open("kit/distinct-m40-witnesses.json"))
    oks = [verify_config([tuple(s) for s in ws], 5, 40, 4)["ok"]
           for ws in W40]
    out["control_m40_all_ok"] = all(oks)
    out["control_m40_count"] = len(oks)
    ws = sorted(map(tuple, W40[0]))
    bad = [(s[0] + 1, s[1]) if s == ws[3] else s for s in ws]
    out["tamper_m40_fails"] = not verify_config(bad, 5, 40, 4)["ok"]
    bad2 = [ws[0], ws[1], ws[2],
            (ws[3][0], ws[3][1] + 1 if ws[3][1] + 1 < 5 else 0)]
    bad2 = sorted(set(bad2))
    out["unsafe_flagged"] = not verify_config(
        [[0, 0], [1, 0], [2, 0], [3, 0]], 5, 40, 4)["safe"]
    r = verify_config([tuple(s) for s in SEED_M46], 6, 46, 4)
    out["m46_seed_witness_ok"] = r["ok"]
    out["m46_seed_rows"] = r["rows"]
    # calibration via census of a single seed family at scan=48
    pls = census_placements({"m46": SEED_M46}, 6, 4, 48)
    cal = [p for p in pls if p["seed"] == "m46" and p["image"] == "id"
           and p["shift"] == 4]
    out["calibration_m46_R46"] = bool(
        cal and cal[0]["R"] == 46 and cal[0]["firstUncovered"] == [46, 0])
    return out

# ---------------------------------------------------------------- CLI

def _cli():
    mode = sys.argv[1]
    if mode == "selftest":
        print(json.dumps(do_selftest(), sort_keys=True, indent=1))
    elif mode == "verify":
        cfg = json.load(open(sys.argv[2]))
        r = verify_config(cfg["stones"], cfg["w"], cfg["m"], cfg.get("q", 4))
        r["tag"] = cfg.get("tag")
        print(json.dumps(r, sort_keys=True, indent=1))
    elif mode == "verifymany":
        cfg = json.load(open(sys.argv[2]))
        results = []
        for it in cfg["items"]:
            m = it["m"] if "m" in it else cfg.get("m")
            r = verify_config(it["stones"], cfg["w"], m,
                              cfg.get("q", 4))
            results.append(dict(tag=it["tag"], m=m, ok=r["ok"], safe=r["safe"],
                                maximal=r["maximal"], rows=r["rows"],
                                rowDeficient=r["rowDeficient"], n=r["n"],
                                uncoveredCount=len(r["uncovered"])))
        print(json.dumps(dict(w=cfg["w"], q=cfg.get("q", 4),
                              results=results), sort_keys=True, indent=1))
    elif mode == "run":
        cfg = json.load(open(sys.argv[2]))
        r = run_surgery(cfg["w"], cfg["m_seed"], cfg["q"], cfg["seed"],
                        cfg["m_target"], cfg.get("remBudget", 2))
        # uncoveredBase: uncovered cells of the seed on the target board
        print(json.dumps(r, sort_keys=True, indent=1))
    elif mode == "census":
        cfg = json.load(open(sys.argv[2]))
        # cfg: {w, q, scan, seeds: {name: stones}, calib: [...] }
        pls = census_placements(cfg["seeds"], cfg["w"], cfg["q"], cfg["scan"])
        for c in cfg.get("calib", []):
            fam = [p for p in pls if p["seed"] == c["seed"]
                   and p["image"] == c["image"] and p["shift"] == c["shift"]]
            assert fam and fam[0]["R"] == c["R"] and \
                fam[0]["firstUncovered"] == c["firstUncovered"], c
        pls.sort(key=lambda p: (-p["R"], p["seed"], p["image"], p["shift"]))
        top = len(cfg.get("topList", [])) or None
        print(json.dumps(dict(
            w=cfg["w"], q=cfg["q"], scan=cfg["scan"],
            calibration=cfg.get("calib", []), placements=pls),
            sort_keys=True, indent=1))
    else:
        raise SystemExit("unknown mode")

if __name__ == "__main__":
    _cli()
