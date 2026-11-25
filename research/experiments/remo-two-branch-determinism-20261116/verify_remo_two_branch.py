#!/usr/bin/env python3
"""K0860 audit: REMO survivor determinism on two-branch synthetic families.

Self-contained. Deterministic (no randomness, no wall clock, no network).
Python 3.11+ / stdlib only.

Checked claims (proof text: report.md in this directory /
research/knowledge/items/K0860-remo-two-branch-determinism.md):

T1 (Theorem E, region-count reduction)  On the two-branch synthetic family
    (maximals A with |A|=C1 < C2=|B|, |A n B| = g < C1; safe sets = subsets of
    A or B), the cell-level REMO game and the region-count game (per-player
    core / exclusive stone counts + branch lock + rotation) have identical
    outcome sets. Machine check: complete enumeration, overlap grid + anchors.
T2 (Theorem F, r=3 closed form)  Explicit path formulas reproduce the region
    game outcome sets exactly on the full r=3 grid.
T3  r | Delta is neither necessary nor sufficient for REMO *survivor*
    determinism. Infinite families (proofs in report.md); instances checked.
T4  Survivor-determined but elimination-order-nondetermined two-branch
    families exist (smallest: (C1,C2,g)=(5,7,*)).
T5  Real-board census: REMO survivor determinism on 2x4 / 2x5 / 2x6 / 3x4
    q=4 integer boards, complete enumeration for the listed r only.

REMO rule (K0859): players 0..r-1 rotate; the first player with no legal move
at a maximal safe position is eliminated; ALL stones owned by the loser are
removed; play continues with the next active player; if the position is still
maximal the next player is eliminated too (chain), until one player survives.

Scope / limits (do not over-read):
- Infinite-family claims are proved in the closed form (report.md); this
  script checks instances only.
- The real-board census covers exactly the listed boards and r.
- 11x11 empty board / two-stone roots / class1/2/4 remain UNKNOWN, unrelated.
- solved 1405 is manifest bookkeeping only.
"""

import hashlib
import json
import os
import sys

sys.setrecursionlimit(100000)


class Budget(Exception):
    """Deterministic node-budget guard (machine-independent)."""


# ---------------------------------------------------------------------------
# generic helpers


def next_active(p, r, active):
    for d in range(1, r + 1):
        q = (p + d) % r
        if q in active:
            return q
    raise AssertionError("no active player after %d" % p)


def outcome_summary(outcomes):
    survivors = sorted({sv for (_, sv) in outcomes})
    orders = sorted(list(o) for o, _ in outcomes)
    first_losers = sorted({o[0] for o, _ in outcomes})
    return {
        "determined": len(survivors) == 1,
        "survivors": survivors,
        "first_losers": first_losers,
        "orders": orders,
        "order_determined": len(orders) == 1,
    }


# ---------------------------------------------------------------------------
# cell-level REMO on the explicit two-branch point family
# cells: core = 0..g-1, A-only = g..C1-1, B-only = C1..C1+C2-g-1


def cell_two_branch(C1, C2, g, r, budget=2_000_000):
    ncells = C1 + C2 - g
    A = frozenset(range(C1))
    B = frozenset(range(g)) | frozenset(range(C1, ncells))
    memo = {}
    nodes = [budget]

    def outcomes(placed, own, mover, active):
        key = (placed, own, mover, active)
        got = memo.get(key)
        if got is not None:
            return got
        nodes[0] -= 1
        if nodes[0] < 0:
            raise Budget("cell budget")
        res = set()
        if placed == A or placed == B:
            loser = mover
            new_placed = frozenset(c for c in placed if own[c] != loser)
            new_own = tuple(-1 if o == loser else o for o in own)
            new_active = frozenset(a for a in active if a != loser)
            if len(new_active) == 1:
                res.add(((loser,), next(iter(new_active))))
            else:
                nm = next_active(loser, r, new_active)
                for od, sv in outcomes(new_placed, new_own, nm, new_active):
                    res.add(((loser,) + od, sv))
        else:
            legal = set()
            if placed <= A:
                legal |= A - placed
            if placed <= B:
                legal |= B - placed
            nm = next_active(mover, r, active)
            for c in sorted(legal):
                res |= outcomes(
                    placed | {c}, own[:c] + (mover,) + own[c + 1:], nm, active
                )
        out = frozenset(res)
        memo[key] = out
        return out

    start = outcomes(frozenset(), (-1,) * ncells, 0, frozenset(range(r)))
    return start, len(memo)


# ---------------------------------------------------------------------------
# region-count game (Theorem E)
# state: core counts per player, exclusive counts per player, branch lock.


def region_two_branch(C1, C2, g, r, budget=500_000):
    memo = {}
    nodes = [budget]

    def bump(t, i):
        return t[:i] + (t[i] + 1,) + t[i + 1:]

    def outcomes(core, excl, branch, mover, active):
        key = (core, excl, branch, mover, active)
        got = memo.get(key)
        if got is not None:
            return got
        nodes[0] -= 1
        if nodes[0] < 0:
            raise Budget("region budget")
        t = sum(core) + sum(excl)
        res = set()
        if (branch == "A" and t == C1) or (branch == "B" and t == C2):
            loser = mover
            ncore = tuple(0 if i == loser else core[i] for i in range(r))
            nexcl = tuple(0 if i == loser else excl[i] for i in range(r))
            nbranch = branch if sum(nexcl) > 0 else "F"
            new_active = frozenset(a for a in active if a != loser)
            if len(new_active) == 1:
                res.add(((loser,), next(iter(new_active))))
            else:
                nm = next_active(loser, r, new_active)
                for od, sv in outcomes(ncore, nexcl, nbranch, nm, new_active):
                    res.add(((loser,) + od, sv))
        else:
            nm = next_active(mover, r, active)
            if branch == "F":
                if sum(core) < g:
                    res |= outcomes(bump(core, mover), excl, "F", nm, active)
                # A-only cells exist because g < C1; B-only cells because C2 > C1 > g
                res |= outcomes(core, bump(excl, mover), "A", nm, active)
                res |= outcomes(core, bump(excl, mover), "B", nm, active)
            elif branch == "A":
                if sum(core) < g:
                    res |= outcomes(bump(core, mover), excl, "A", nm, active)
                if sum(excl) < C1 - g:
                    res |= outcomes(core, bump(excl, mover), "A", nm, active)
            else:  # "B"
                if sum(core) < g:
                    res |= outcomes(bump(core, mover), excl, "B", nm, active)
                if sum(excl) < C2 - g:
                    res |= outcomes(core, bump(excl, mover), "B", nm, active)
        out = frozenset(res)
        memo[key] = out
        return out

    start = outcomes((0,) * r, (0,) * r, "F", 0, frozenset(range(r)))
    return start, len(memo)


# ---------------------------------------------------------------------------
# closed form for r=3 (Theorem F)
#
# Phase 1 ends at terminal X in {A,B} (both reachable from the root).
# L1 = C_X; first loser lam = L1 mod 3 (first mover is P_0 WLOG); the loser
# owns o = (L1 - lam)/3 stones of the terminal; dip position size s' = L1 - o.
# Dip type (region profile of the surviving position S' = X minus the loser's
# stones): free (S' inside the core) is feasible iff o >= C_X - g; locked X is
# always feasible (o <= C_X - 1). Phase 2 from locked X has forced length
# l2 = C_X - s'; from a free dip both terminals are reachable, l2 = C_Y - s'.
# Phase 2 rotates over the two survivors starting at lam+1, so
# loser2 = (lam + 1 + (l2 mod 2)) mod 3 and survivor = (-lam - loser2) mod 3.


def closed_form_r3(C1, C2, g):
    outcomes = set()
    for (L1, CX) in ((C1, "A"), (C2, "B")):
        lam = L1 % 3
        o = (L1 - lam) // 3
        sp = L1 - o
        dips = ["locked"]
        if o >= (C1 if CX == "A" else C2) - g:
            dips.append("free")
        for dip in dips:
            L2s = [C1 if CX == "A" else C2] if dip == "locked" else [C1, C2]
            for L2 in L2s:
                l2 = L2 - sp
                assert l2 >= 1
                loser2 = (lam + 1 + (l2 % 2)) % 3
                outcomes.add(((lam, loser2), (-lam - loser2) % 3))
    return frozenset(outcomes)


# ---------------------------------------------------------------------------
# real boards, q=4 complete kyouen (co-circular or collinear 4-sets forbidden)


def det3(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def det4(m):
    # integer 4x4 determinant: Laplace expansion along the first row
    total = 0
    for j in range(4):
        minor = [
            [m[i][k] for k in range(4) if k != j] for i in range(1, 4)
        ]
        total += (-1) ** j * m[0][j] * det3(minor)
    return total


def board_tables(W, H):
    pts = [(x, y) for y in range(H) for x in range(W)]
    n = len(pts)
    quads_by_high = [[] for _ in range(n)]
    import itertools

    for q in itertools.combinations(range(n), 4):
        rows = []
        for i in q:
            x, y = pts[i]
            rows.append([x * x + y * y, x, y, 1])
        if det4(rows) == 0:
            mask = sum(1 << i for i in q)
            quads_by_high[max(q)].append(mask)
    size = 1 << n
    safe = [False] * size
    maximal = [False] * size
    for m in range(size):
        if m == 0:
            safe[m] = True
            continue
        h = m.bit_length() - 1
        base = m ^ (1 << h)
        ok = safe[base]
        if ok:
            for q in quads_by_high[h]:
                if q & m == q:
                    ok = False
                    break
        safe[m] = ok
    for m in range(size):
        if not safe[m]:
            continue
        mx = True
        # maximal iff every empty cell admits a safe addition
        for c in range(n):
            if not (m >> c) & 1:
                if safe[m | (1 << c)]:
                    mx = False
                    break
        maximal[m] = mx
    census = {}
    for m in range(size):
        if maximal[m]:
            census[bin(m).count("1")] = census.get(bin(m).count("1"), 0) + 1
    return pts, n, safe, maximal, census


def real_board_remo(W, H, r, budget=2_500_000):
    pts, n, safe, maximal, census = board_tables(W, H)
    memo = {}
    nodes = [budget]

    def outcomes(mask, own, mover, active):
        key = (mask, own, mover, active)
        got = memo.get(key)
        if got is not None:
            return got
        nodes[0] -= 1
        if nodes[0] < 0:
            raise Budget("real board budget")
        res = set()
        if maximal[mask]:
            loser = mover
            nmask = mask
            nown = list(own)
            for c in range(n):
                if own[c] == loser:
                    nown[c] = -1
                    nmask &= ~(1 << c)
            nown = tuple(nown)
            new_active = frozenset(a for a in active if a != loser)
            if len(new_active) == 1:
                res.add(((loser,), next(iter(new_active))))
            else:
                nm = next_active(loser, r, new_active)
                for od, sv in outcomes(nmask, nown, nm, new_active):
                    res.add(((loser,) + od, sv))
        else:
            nm = next_active(mover, r, active)
            for c in range(n):
                if not (mask >> c) & 1 and safe[mask | (1 << c)]:
                    res |= outcomes(
                        mask | (1 << c), own[:c] + (mover,) + own[c + 1:], nm, active
                    )
        out = frozenset(res)
        memo[key] = out
        return out

    start = outcomes(0, (-1,) * n, 0, frozenset(range(r)))
    return start, len(memo), census


# ---------------------------------------------------------------------------
# audit construction


def build_audit():
    checks = []

    def check(name, ok):
        checks.append({"name": name, "ok": bool(ok)})
        return bool(ok)

    audit = {
        "schema": "remo-two-branch-determinism-audit/1",
        "generated_by": "verify_remo_two_branch.py",
    }

    # ---- r=3 grid: region game vs closed form -----------------------------
    grid = {}
    grid_mismatch = 0
    fl_wrong = 0
    det_cnt = 0
    surv_det_order_nondet = []
    rdiv_det = [0, 0]  # (r|Delta families: determined, nondetermined)
    rndiv_det = [0, 0]
    for C1 in range(3, 9):
        for C2 in range(C1 + 1, 13):
            for g in range(0, C1):
                try:
                    reg, _ = region_two_branch(C1, C2, g, 3)
                except Budget:
                    continue
                cf = closed_form_r3(C1, C2, g)
                if reg != cf:
                    grid_mismatch += 1
                k = "%d,%d,%d" % (C1, C2, g)
                s = outcome_summary(reg)
                grid[k] = {
                    "det": s["determined"],
                    "surv": s["survivors"],
                    "orders": s["orders"],
                }
                if s["determined"]:
                    det_cnt += 1
                if s["determined"] and not s["order_determined"]:
                    surv_det_order_nondet.append(k)
                exp_fl = sorted({C1 % 3, C2 % 3})
                if s["first_losers"] != exp_fl:
                    fl_wrong += 1
                if (C2 - C1) % 3 == 0:
                    rdiv_det[1 if s["determined"] else 0] += 1
                else:
                    rndiv_det[1 if s["determined"] else 0] += 1
    check(
        "r3 grid: region game == closed form (197 families)",
        grid_mismatch == 0,
    )
    check(
        "r3 grid: first loser set == {C1 mod 3, C2 mod 3} (K0339)",
        fl_wrong == 0,
    )

    # ---- locked-regime criterion (derived in report.md Theorem F) ----------
    # both dips locked iff g < C1 - o1 and g < C2 - o2; then determined iff
    # f(lam1,o1) == f(lam2,o2) with f(lam,o) = (-lam - (lam+1+(o%2))%3) % 3,
    # and for Delta = 0 mod 3 this is iff Delta/3 is even.
    def f_surv(lam, o):
        return (-lam - (lam + 1 + (o % 2)) % 3) % 3

    crit_wrong = 0
    crit_cnt = 0
    rdiv_wrong = 0
    for C1 in range(3, 9):
        for C2 in range(C1 + 1, 13):
            lam1, o1 = C1 % 3, (C1 - C1 % 3) // 3
            lam2, o2 = C2 % 3, (C2 - C2 % 3) // 3
            for g in range(0, C1):
                if g >= C1 - o1 or g >= C2 - o2:
                    continue
                k = "%d,%d,%d" % (C1, C2, g)
                if k not in grid:
                    continue
                crit_cnt += 1
                pred = f_surv(lam1, o1) == f_surv(lam2, o2)
                if grid[k]["det"] != pred:
                    crit_wrong += 1
                if (C2 - C1) % 3 == 0:
                    if pred != ((C2 - C1) // 3 % 2 == 0):
                        rdiv_wrong += 1
    check(
        "r3 locked regime: determined iff f(lam1,o1)==f(lam2,o2) (%d families)"
        % crit_cnt,
        crit_wrong == 0,
    )
    check(
        "r3 locked regime with 3|Delta: determined iff Delta/3 even",
        rdiv_wrong == 0,
    )
    audit["r3_grid"] = {
        "families": len(grid),
        "determined": det_cnt,
        "survivor_determined_order_nondetermined": surv_det_order_nondet,
        "determinism_vs_rd": {
            "r_divides_delta": {"determined": rdiv_det[1], "nondetermined": rdiv_det[0]},
            "r_not_divides_delta": {"determined": rndiv_det[1], "nondetermined": rndiv_det[0]},
        },
        "families": grid,
    }

    # ---- cell-level vs region game ----------------------------------------
    cell_checked = 0
    cell_mismatch = 0
    cell_skipped = []
    for r in (3, 4):
        for C1 in range(3 if r == 3 else 4, 7):
            for C2 in range(C1 + 1, 8):
                for g in range(0, C1):
                    try:
                        cell, _ = cell_two_branch(C1, C2, g, r)
                    except Budget:
                        cell_skipped.append("%d,%d,%d,r%d" % (C1, C2, g, r))
                        continue
                    reg, _ = region_two_branch(C1, C2, g, r)
                    cell_checked += 1
                    if cell != reg:
                        cell_mismatch += 1
    check(
        "cell-level == region game on overlap grid (Theorem E)",
        cell_mismatch == 0 and cell_checked >= 40,
    )
    audit["cell_vs_region"] = {
        "families_checked": cell_checked,
        "mismatches": cell_mismatch,
        "skipped_budget": cell_skipped,
    }

    # ---- K0859 anchor family (6,9,g=3) ------------------------------------
    anchor = {}
    a_cell, _ = cell_two_branch(6, 9, 3, 3)
    a_reg, _ = region_two_branch(6, 9, 3, 3)
    a_cf = closed_form_r3(6, 9, 3)
    s = outcome_summary(a_cell)
    check("K0859 anchor: cell == region == closed form", a_cell == a_reg == a_cf)
    check(
        "K0859 anchor r=3: first loser always P_0, survivors {1,2}",
        s["first_losers"] == [0] and s["survivors"] == [1, 2],
    )
    anchor["r3"] = {"determined": False, "survivors": [1, 2], "first_losers": [0]}
    a2, _ = cell_two_branch(6, 9, 3, 2)
    # r=2: REMO==CASC (single elimination); loser = L mod 2 at terminal size
    # L in {6,9}; survivor = last placer = (L-1) mod 2; determined iff 2 | Delta.
    exp2 = frozenset([((6 % 2,), (6 - 1) % 2), ((9 % 2,), (9 - 1) % 2)])
    check("K0859 anchor r=2: REMO==CASC, loser=(L mod 2), survivor=(L-1) mod 2",
          a2 == exp2)
    anchor["r2"] = {
        "determined": outcome_summary(a2)["determined"],
        "survivors": outcome_summary(a2)["survivors"],
        "first_losers": outcome_summary(a2)["first_losers"],
    }
    for r in (4, 5, 6):
        reg, _ = region_two_branch(6, 9, 3, r)
        sr = outcome_summary(reg)
        anchor["r%d" % r] = {
            "determined": sr["determined"],
            "survivors": sr["survivors"],
            "first_losers": sr["first_losers"],
        }
        check(
            "K0859 anchor r=%d: first losers == {6,9} mod r" % r,
            sr["first_losers"] == sorted({6 % r, 9 % r}),
        )
    audit["anchor_6_9_3"] = anchor

    # ---- infinite-family instance checks (Theorem F dichotomies) ----------
    fam = {}

    def fam_check(name, C1, C2, gamma_list, r, predict):
        # predict(g) -> None (no claim) or (determined, survivors)
        entries = {}
        ok = True
        mismatch_cf = 0
        for g in gamma_list:
            try:
                reg, _ = region_two_branch(C1, C2, g, r, budget=2_000_000)
            except Budget:
                entries[str(g)] = {"skipped": "budget"}
                ok = False
                continue
            if r == 3:
                cf = closed_form_r3(C1, C2, g)
                if cf != reg:
                    mismatch_cf += 1
            s = outcome_summary(reg)
            entries[str(g)] = {
                "det": s["determined"],
                "surv": s["survivors"],
            }
            if predict is not None:
                det, surv = predict(g)
                if s["determined"] != det or s["survivors"] != surv:
                    ok = False
        fam[name] = entries
        return ok, mismatch_cf

    # (6u,9u): determined for all g iff u even; survivor P_2 (u even),
    # survivors {1,2} (u odd). r|Delta (= 3u).
    ok_all = True
    cf_mm = 0
    for u in (1, 2, 3):
        C1, C2 = 6 * u, 9 * u
        pred = (
            (lambda g: (True, [2])) if u % 2 == 0 else (lambda g: (False, [1, 2]))
        )
        ok, mm = fam_check(
            "6u-9u u=%d" % u, C1, C2, range(0, C1), 3, pred
        )
        ok_all = ok_all and ok
        cf_mm += mm
    check("(6u,9u) r=3: determined for ALL g iff u even (r|Delta, both ways)", ok_all)
    check("(6u,9u) r=3: closed form == region game on all instances", cf_mm == 0)

    # (6u,12u): determined for all g, survivor P_2 (r|Delta).
    ok_all = True
    for u in (1, 2):
        C1, C2 = 6 * u, 12 * u
        ok, mm = fam_check(
            "6u-12u u=%d" % u, C1, C2, range(0, C1), 3, lambda g: (True, [2])
        )
        ok_all = ok_all and ok
    check("(6u,12u) r=3: determined for ALL g, survivor P_2 (r|Delta sufficient side)", ok_all)

    # (3t+2,3t+4): determined for all g iff t odd; survivor P_0 (t odd),
    # survivors {1,2} (t even). Delta = 2, never divisible by 3.
    ok_all = True
    for t in (1, 2, 3, 4):
        C1, C2 = 3 * t + 2, 3 * t + 4
        pred = (
            (lambda g: (True, [0])) if t % 2 == 1 else (lambda g: (False, [1, 2]))
        )
        ok, mm = fam_check("3t2-3t4 t=%d" % t, C1, C2, range(0, C1), 3, pred)
        ok_all = ok_all and ok
    check(
        "(3t+2,3t+4) r=3: determined for ALL g iff t odd (r does not divide Delta)",
        ok_all,
    )

    # (3,6): non-determined for all g (small trap case).
    ok, mm = fam_check("3-6", 3, 6, range(0, 3), 3, lambda g: (False, [1, 2]))
    check("(3,6) r=3: non-determined for ALL g (r|Delta, region subtlety)", ok)
    audit["families"] = fam

    # ---- r=2: REMO == CASC, determinism iff 2 | Delta ---------------------
    ok_all = True
    for (C1, C2, g) in ((6, 9, 3), (5, 7, 3), (4, 6, 2), (8, 10, 5)):
        reg, _ = region_two_branch(C1, C2, g, 2)
        exp = frozenset(
            (((L % 2),), (L - 1) % 2) for L in (C1, C2)
        )
        det_expected = (C2 - C1) % 2 == 0
        if reg != exp or outcome_summary(reg)["determined"] != det_expected:
            ok_all = False
    check(
        "r=2: REMO==CASC on two-branch families; determined iff 2|Delta",
        ok_all,
    )

    # ---- r=4,5,6 region grids ----------------------------------------------
    r_tables = {}
    for r, (c1_lo, c2_hi) in ((4, (4, 12)), (5, (5, 10)), (6, (6, 10))):
        det = 0
        ndet = 0
        fl_wrong = 0
        checked = 0
        skipped = 0
        sdo = 0
        det_examples = []
        for C1 in range(c1_lo, 9):
            for C2 in range(C1 + 1, c2_hi + 1):
                for g in range(0, C1):
                    try:
                        reg, _ = region_two_branch(C1, C2, g, r, budget=300_000)
                    except Budget:
                        skipped += 1
                        continue
                    checked += 1
                    s = outcome_summary(reg)
                    if s["determined"]:
                        det += 1
                        if len(det_examples) < 8:
                            det_examples.append(
                                {"c1": C1, "c2": C2, "g": g, "survivors": s["survivors"]}
                            )
                        if not s["order_determined"]:
                            sdo += 1
                    else:
                        ndet += 1
                    if s["first_losers"] != sorted({C1 % r, C2 % r}):
                        fl_wrong += 1
        r_tables[str(r)] = {
            "families_checked": checked,
            "skipped_budget": skipped,
            "determined": det,
            "nondetermined": ndet,
            "determined_but_order_nondetermined": sdo,
            "determined_examples": det_examples,
        }
        check(
            "r=%d grid: first loser set == {C1,C2} mod r (K0339)" % r,
            fl_wrong == 0,
        )
    audit["r456_tables"] = r_tables

    # ---- real-board census -------------------------------------------------
    expected_census = {
        (2, 4): {"4": 8, "5": 16},
        (2, 5): {"5": 72, "6": 6},
        (2, 6): {"5": 108, "6": 64},
        (3, 4): {"5": 104, "6": 78},
    }
    real = {}
    census_ok = True
    for (W, H) in ((2, 4), (2, 5), (2, 6), (3, 4)):
        _, _, _, _, census = board_tables(W, H)
        got = {str(k): v for k, v in sorted(census.items())}
        if got != expected_census[(W, H)]:
            census_ok = False
        entry = {"maximal_census": got}
        rlist = (3, 4, 5, 6)
        sizes = sorted(census.keys())
        for r in rlist:
            try:
                oc, states, _ = real_board_remo(W, H, r)
            except Budget:
                entry["r%d" % r] = {"skipped": "state budget"}
                continue
            s = outcome_summary(oc)
            fl_ok = s["first_losers"] == sorted({sz % r for sz in sizes})
            entry["r%d" % r] = {
                "determined": s["determined"],
                "survivors": s["survivors"],
                "first_losers": s["first_losers"],
                "orders_count": len(s["orders"]),
                "order_determined": s["order_determined"],
                "states": states,
                "first_loser_k0339_ok": fl_ok,
            }
            if not fl_ok:
                census_ok = False
        real["%dx%d" % (W, H)] = entry
    check("real boards: maximal-size censuses match published values", census_ok)
    audit["real_boards"] = real

    # ---- summary ------------------------------------------------------------
    audit["machine_checks"] = [
        {"count": len(checks), "all_ok": all(c["ok"] for c in checks), "items": checks}
    ]
    audit["notes"] = [
        "two-branch synthetic family: maximals A (|A|=C1), B (|B|=C2), "
        "|A n B|=g<C1; safe = subsets of A or B; REMO rule as in K0859",
        "grids are finite; infinite-family claims proved in report.md/K0860 text",
        "region/cell/real enumerations are complete game-tree enumerations "
        "with ownership (memoized DFS), not samples",
        "real-board census covers only the listed boards and r",
        "11x11 empty board / two-stone roots / class1/2/4: UNKNOWN, unrelated",
        "solved 1405 is manifest bookkeeping only",
    ]
    return audit


def serialize(audit):
    return json.dumps(audit, sort_keys=True, ensure_ascii=False, indent=1) + "\n"


def main():
    audit1 = build_audit()
    blob1 = serialize(audit1)
    audit2 = build_audit()
    blob2 = serialize(audit2)
    d1 = hashlib.sha256(blob1.encode()).hexdigest()
    d2 = hashlib.sha256(blob2.encode()).hexdigest()
    if d1 != d2:
        sys.stderr.write("FATAL: two runs differ (nondeterminism)\n")
        sys.exit(1)
    all_ok = all(c["ok"] for c in audit1["machine_checks"][0]["items"])
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "output",
        "remo_two_branch_audit.json",
    )
    if os.path.exists(out_path):
        with open(out_path, "rb") as f:
            committed = f.read().decode()
        if committed != blob1:
            sys.stderr.write(
                "FATAL: regenerated audit differs from committed file "
                "(sha256 %s)\n" % d1
            )
            sys.exit(1)
        print("OK: audit byte-identical (sha256 %s), %d machine checks all_ok=%s"
              % (d1, audit1["machine_checks"][0]["count"], all_ok))
    else:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(blob1)
        print("wrote %s (sha256 %s), %d machine checks all_ok=%s"
              % (out_path, d1, audit1["machine_checks"][0]["count"], all_ok))
    if not all_ok:
        sys.stderr.write("FATAL: failed machine checks present\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
