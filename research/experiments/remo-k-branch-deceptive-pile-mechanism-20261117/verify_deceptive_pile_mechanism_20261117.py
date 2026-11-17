#!/usr/bin/env python3
"""K0923 audit: pile-game reduction and the spf law for the deceptive
key (1,1,p)|gamma=0 (3-branch REMO determinacy).

Self-contained verifier. Deterministic (no randomness, no wall clock,
no network). Python 3.11+ / stdlib only.

Reduction (proved here, see report.md for the memo proof): the profile
atoms (1,1,0,p,0,0,0) decompose into three star-private atoms
(a in star1, size 1; b in star2, size 1; c in star3, size p). Lemmas
R1-R4 reduce the full region game on this profile to the pile game:

  - occupied atoms are always within a single star (R1);
  - opening a or b completes its star and the elimination cascade
    leaves the opener as the sole survivor (the win-now option, R2);
  - while only c is occupied the play is a forced stretch (R3);
  - the possible-survivor set equals the decision-point movers along
    the unique decision path plus the terminal survivor (R4).

This file implements the pile game exactly and machine-checks, over
p <= 100:

  X1  engine cross-validation: the simulator reproduces the pinned
      K0912 engine (mask_engine_fast2.js, sha256 b904760e...) verdicts
      (determined, survivors) on 88 columns: the (1,1,p) profiles for
      p in {11,13,17} over their full windows r=2..p+1, and composite
      p in {4,6,8,9,15} over 33 sampled columns (engine runs recorded
      in the 2026-11-17 p13/p17 probe logs; the same binary was
      cross-validated against the committed cap<=12 columns and the
      K0920 focus columns in those publications).
  L1  spf law: for 3 <= p <= 100, 2 <= r <= p-1:
      sv == {P_0}  <=>  r < spf(p)   (4,851 columns, 0 violations).
      Hence the deceptive window [2,p-1] is uniformly determined
      exactly for the 24 primes p <= 100, always with survivor P_0.
  L2  single-stretch structure, p <= 40: the decision path always has
      exactly one decision point (the start) and the first forced
      stretch terminates the game; terminal survivor == P_0 <=> r <
      spf(p).
  L3  for every prime p <= 100: sv at r=p and r=p+1 is {P_0,P_1}
      (consistent with theorem J r >= M constancy; M=p).

Universal claims about p > 100 are NOT made; the spf law beyond the
swept range is a conjecture (see report.md).
"""

import json
import os
import sys

# ---------------------------------------------------------------------------
# pile game (exact implementation of the reduction; see report.md)
# ---------------------------------------------------------------------------


def succ(x, A, r):
    for d in range(1, r + 1):
        q = (x + d) % r
        if q in A:
            return q
    raise AssertionError("no active player after %d" % x)


def forced_stretch(p, A, mu, r):
    """Deterministic c-pile stretch from the empty board, mover mu.
    Returns ('end', survivor) or ('decision', A', mu')."""
    A = set(A)
    m = {j: 0 for j in A}
    count = 0
    mover = mu
    while True:
        if count == p:
            mm = m[mover]
            A.discard(mover)
            if len(A) == 1:
                return ('end', next(iter(A)))
            nm = succ(mover, A, r)
            count -= mm
            mover = nm
            if count == 0:
                return ('decision', frozenset(A), nm)
        else:
            m[mover] += 1
            count += 1
            mover = succ(mover, A, r)


def sv_set(p, r):
    """All possible survivors over all plays, (1,1,p)|0, r players."""
    survivors = set()
    A, mu = frozenset(range(r)), 0
    while True:
        survivors.add(mu)          # win-now option at the decision point
        res = forced_stretch(p, A, mu, r)
        if res[0] == 'end':
            survivors.add(res[1])
            return survivors
        A, mu = res[1], res[2]


def path_info(p, r):
    """Decision-point count and terminal survivor of the decision path."""
    A, mu = frozenset(range(r)), 0
    pts = 1
    while True:
        res = forced_stretch(p, A, mu, r)
        if res[0] == 'end':
            return pts, res[1]
        A, mu = res[1], res[2]
        pts += 1


def spf(p):
    for q in range(2, int(p ** 0.5) + 1):
        if p % q == 0:
            return q
    return p


# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

# Engine cross-validation table (p, r, determined, survivors) from the
# pinned K0912 engine runs of 2026-11-17 (88 columns; see docstring X1).
ENGINE_CROSS = [[11, 2, True, [0]], [11, 3, True, [0]], [11, 4, True, [0]], [11, 5, True, [0]], [11, 6, True, [0]], [11, 7, True, [0]], [11, 8, True, [0]], [11, 9, True, [0]], [11, 10, True, [0]], [11, 11, False, [0, 1]], [13, 2, True, [0]], [13, 3, True, [0]], [13, 4, True, [0]], [13, 5, True, [0]], [13, 6, True, [0]], [13, 7, True, [0]], [13, 8, True, [0]], [13, 9, True, [0]], [13, 10, True, [0]], [13, 11, True, [0]], [13, 12, True, [0]], [13, 13, False, [0, 1]], [13, 14, False, [0, 1]], [17, 2, True, [0]], [17, 3, True, [0]], [17, 4, True, [0]], [17, 5, True, [0]], [17, 6, True, [0]], [17, 7, True, [0]], [17, 8, True, [0]], [17, 9, True, [0]], [17, 10, True, [0]], [17, 11, True, [0]], [17, 12, True, [0]], [17, 13, True, [0]], [17, 14, True, [0]], [17, 15, True, [0]], [17, 16, True, [0]], [17, 17, False, [0, 1]], [17, 18, False, [0, 1]], [4, 2, False, [0, 1]], [6, 2, False, [0, 1]], [8, 2, False, [0, 1]], [9, 2, True, [0]], [15, 2, True, [0]], [4, 3, False, [0, 2]], [6, 3, False, [0, 2]], [8, 3, False, [0, 1]], [9, 3, False, [0, 1]], [15, 3, False, [0, 1]], [4, 4, False, [0, 3]], [6, 4, False, [0, 3]], [8, 4, False, [0, 2]], [9, 4, False, [0, 2]], [15, 4, False, [0, 1]], [4, 5, False, [0, 3]], [6, 5, False, [0, 4]], [8, 5, False, [0, 2]], [9, 5, False, [0, 2]], [15, 5, False, [0, 2]], [6, 7, False, [0, 5]], [8, 7, False, [0, 4]], [9, 7, False, [0, 3]], [15, 7, False, [0, 3]], [8, 8, False, [0, 5]], [9, 8, False, [0, 4]], [15, 8, False, [0, 3]], [8, 9, False, [0, 5]], [9, 9, False, [0, 5]], [15, 9, False, [0, 3]], [9, 10, False, [0, 5]], [15, 10, False, [0, 3]], [15, 16, False, [0, 7]], [10, 2, False, [0, 1]], [21, 2, True, [0]], [25, 2, True, [0]], [10, 3, False, [0, 2]], [21, 3, False, [0, 1]], [25, 3, True, [0]], [10, 4, False, [0, 3]], [21, 4, False, [0, 2]], [25, 4, True, [0]], [10, 5, False, [0, 4]], [21, 5, False, [0, 3]], [25, 5, False, [0, 1]], [10, 6, False, [0, 5]], [21, 6, False, [0, 4]], [25, 6, False, [0, 2]]]

LAW_PMAX = 100      # spf-law sweep bound
STRETCH_PMAX = 40   # single-stretch structure sweep bound


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def check(name, ok, note):
    return {"name": name, "ok": bool(ok), "note": note}


def law_rows(pmax):
    rows = []
    for p in range(3, pmax + 1):
        s = spf(p)
        window = []
        for r in range(2, p):
            window.append(sorted(sv_set(p, r)) == [0])
        rows.append({
            "p": p,
            "spf": s,
            "prime": s == p,
            "window_all_det": all(window),
            "window_det_count": sum(window),
            "window_len": len(window),
            "sv_r_eq_p": sorted(sv_set(p, p)),
            "sv_r_eq_p_plus_1": sorted(sv_set(p, p + 1)),
        })
    return rows


def assemble_audit():
    checks = []

    # X1: engine cross-validation
    bad = 0
    for p, r, det, sv in ENGINE_CROSS:
        sim = sorted(sv_set(p, r))
        if sim != sorted(sv) or (sim == [0]) != det:
            bad += 1
    checks.append(check("engine_cross_88", bad == 0 and len(ENGINE_CROSS) == 88,
                        "columns=%d mismatches=%d" % (len(ENGINE_CROSS), bad)))

    # L1: spf law, p <= 100, r <= p-1
    cols = 0
    viol = 0
    for p in range(3, LAW_PMAX + 1):
        s = spf(p)
        for r in range(2, p):
            det = sorted(sv_set(p, r)) == [0]
            cols += 1
            if det != (r < s):
                viol += 1
    checks.append(check("spf_law_p100", viol == 0,
                        "columns=%d violations=%d" % (cols, viol)))

    # window = primes exactly (p <= 100)
    rows = law_rows(LAW_PMAX)
    primes = [x["p"] for x in rows if x["prime"]]
    det_windows = [x["p"] for x in rows if x["window_all_det"]
                   and x["window_len"] > 0]
    checks.append(check("deceptive_window_is_primes", det_windows == primes,
                        "window-det p=%s" % str(det_windows)))

    # L2: single-stretch structure, p <= 40
    cols = 0
    bad = 0
    for p in range(3, STRETCH_PMAX + 1):
        s = spf(p)
        for r in range(2, p):
            pts, term = path_info(p, r)
            cols += 1
            if pts != 1 or (term == 0) != (r < s):
                bad += 1
    checks.append(check("single_stretch_p40", bad == 0,
                        "columns=%d violations=%d" % (cols, bad)))

    # L3: primes: sv at r=p and r=p+1 == [0,1]
    bad = 0
    for p in primes:
        if sorted(sv_set(p, p)) != [0, 1]:
            bad += 1
        if sorted(sv_set(p, p + 1)) != [0, 1]:
            bad += 1
    checks.append(check("prime_r_ge_p_sv01", bad == 0,
                        "primes=%d bad=%d" % (len(primes), bad)))

    all_ok = all(c["ok"] for c in checks)
    audit = {
        "meta": {
            "date": "2026-11-17",
            "item": "K0923",
            "claim": ("(1,1,p)|0 reduces to the pile game (lemmas R1-R4, "
                      "proved); spf law det <=> r < spf(p) machine-verified "
                      "for p <= 100; deceptive window = primes exactly "
                      "(machine, p <= 100); beyond p=100 conjecture"),
            "engine_provenance": ("K0912 pin mask_engine_fast2.js sha256 "
                                  "b904760e...; 88-column cross table from "
                                  "the 2026-11-17 p13/p17 probe sessions"),
            "scope": ("finite machine law p <= 100; universal spf claim is "
                      "a conjecture; (1,p,p) subfamily not covered"),
        },
        "law_rows": rows,
        "machine_checks": checks,
        "summary": {"all_ok": all_ok, "checks_total": len(checks)},
    }
    return audit


def serialize(audit):
    return json.dumps(audit, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def run():
    a1 = assemble_audit()
    b1 = serialize(a1)
    a2 = assemble_audit()
    b2 = serialize(a2)
    if b1 != b2:
        sys.stderr.write("FATAL: two runs differ (nondeterminism)\n")
        sys.exit(1)
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "output", "deceptive_pile_mechanism_law.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if os.path.exists(out_path):
        with open(out_path, "rb") as f:
            committed = f.read().decode()
        if committed != b1:
            sys.stderr.write("FATAL: regenerated audit differs from "
                             "committed file\n")
            sys.exit(1)
        print("OK: audit byte-identical to committed output")
    else:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(b1)
        print("wrote %s" % out_path)
    import hashlib
    print("audit sha256 %s" % hashlib.sha256(b1.encode()).hexdigest())
    print("AUDIT PASSED" if a1["summary"]["all_ok"] else "AUDIT FAILED")
    for c in a1["machine_checks"]:
        print("  [%s] %s" % ("ok" if c["ok"] else "NG", c["name"]))
        print("        %s" % c["note"])
    if not a1["summary"]["all_ok"]:
        sys.exit(1)


if __name__ == "__main__":
    run()
