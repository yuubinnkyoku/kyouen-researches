#!/usr/bin/env python3
"""Machine anchor for K0932 (SIEVE5-U/V, twin laws mod 30).

Verifies, from fresh full simulations of the K0928 reduced games U(m)/V(m):
  - PIN        committed K0929 tables (sha256, format, P(1..40) anchor),
  - REDRECON   committed U/V tables vs committed P table via proved RED
               (m <= 3999, i.e. every C <= 8000 covered by the P table),
  - TWIN30    twin-law proved classes (LAW1/LAW2 for spf in {3,5}, the
               mod-30 classes) on the committed P table, C <= 8000,
  - FRESHPIN   fresh survivors == committed U/V tables (m = 3..400),
  - SPF        machine evidence: watched dies at pot spf(2m+s)-1 holding
               spf(2m+s)-1 (U) / spf(2m+s) (V); survives iff 2m+s prime,
  - SIEVE3     proved K0931 regression: stretch-2 death iff m = 0 (U) /
               1 (V) mod 3,
  - S5U / S5V  the SIEVE5 closed forms proved in report.md: stretch-3
               length, stretch-4 start state (n, watched position, holdings
               pattern), death <=> m = 1 (U) / 2 (V) mod 5, death block /
               stretch-4 length closed forms, U death cold / V death hot
               and final,
  - S4BREAK    first-stretch-4 breaking structure in survival classes
               (phase, loser position in the ptr-frame circle, held 5),
  - REDFRESH   fresh RED reconstruction of P(C), C <= 1402, == committed.

All stdlib, deterministic. Run from the experiment directory:
    python3 sieve5_verify.py
Exit status 0 iff every check passes.

The closed forms checked here are PROVED in report.md (block induction +
case analysis); this script is the machine anchor, not the proof.
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIN_UV = os.path.join(HERE, "..", "remo-pc-twin-laws-20261117", "data", "pc_uv8000.json")
PIN_P = os.path.join(HERE, "..", "remo-pc-twin-laws-20261117", "data", "pc_p8000.json")
PIN_UV_SHA = "8a3b318bd26b8197c66fd55d79007654d2926a18af165132af8c194bc76d8ae2"
PIN_P_SHA = "58a414bc31fb6266cc2d0e10000436e50f396135847bab5a32163cffff0b975e"
P_PIN_1_40 = [0, 1, 1, 3, 1, 5, 1, 5, 5, 9, 1, 11, 1, 5, 7, 15, 1, 17, 1, 15,
              17, 21, 1, 21, 11, 15, 7, 27, 1, 29, 1, 27, 17, 21, 11, 35, 1,
              5, 7, 39]  # P(1)..P(40), committed pin (K0919/K0929)

M_FRESH = 700          # fresh full simulations, m = 3..M_FRESH, both sides
S4BREAK_MIN_N = 11     # breaking-position closed form requires n >= 11


def spf(n):
    if n < 2:
        return n
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d
        d += 1
    return n


def isprime(n):
    return n >= 2 and spf(n) == n


def play(m, pot0, watch):
    """Play the reduced game from K0928 Lemma P.

    Phase rule: deal pot stones one each from ptr (bulk by divmod), loser is
    the active player at (ptr + pot) % k (post-deal), loser's post-deal
    holding becomes the new pot, ptr = loser's slot after removal.

    Returns a record with:
      survivor   label of the survivor
      death      None or dict(pot, held, phase, in_s4) for the FIRST phase
                 whose loser is the watched label. phase is the 1-based
                 index within the stretch (set for stretch-4 deaths);
                 in_s4 True iff the phase lies in the FIRST stretch-4 run.
      s2death    True iff the watched died at pot 2 (stretch-2)
      s3len      number of stretch-3 (pot-3) phases
      s4         None or the FIRST stretch-4 start state, taken BEFORE the
                 deal of the first pot-4 phase: n, wpos (watched index in
                 the ptr-frame circle), circle (labels in ptr-frame order),
                 holdings snapshot
      s4len      number of first-stretch-4 phases up to and including the
                 watched's stretch-4 death or the first hot loser there
                 (whichever closes it; frozen afterwards)
      s4_break   None or dict(phase, pos, held) for the first hot loser of
                 the first stretch-4 (pos = index in the s4 ptr-frame circle)
    """
    holdings = [2] * m
    active = list(range(m))
    ptr = 0
    pot = pot0
    rec = {"survivor": None, "death": None, "s2death": False, "s3len": 0,
           "s4": None, "s4len": 0, "s4_break": None}
    s4_started = False
    s4_open = True
    while len(active) > 1:
        k = len(active)
        if pot == 3:
            rec["s3len"] += 1
        if pot == 4:
            if not s4_started:
                circle = active[ptr:] + active[:ptr]
                rec["s4"] = {"n": k,
                             "wpos": circle.index(watch) if watch in circle else -1,
                             "circle": circle,
                             "holdings": holdings[:]}
                s4_started = True
            if s4_open:
                rec["s4len"] += 1
        # deal pot stones from ptr
        q, r = divmod(pot, k)
        if q:
            for lab in active:
                holdings[lab] += q
        for i in range(r):
            holdings[active[(ptr + i) % k]] += 1
        L = (ptr + pot) % k
        loser = active[L]
        held = holdings[loser]
        in_first_s4 = s4_started and s4_open and pot == 4
        if in_first_s4:
            if loser == watch:
                rec["death"] = {"pot": 4, "held": held, "phase": rec["s4len"],
                                "in_s4": True}
                s4_open = False
            elif held != 4:
                rec["s4_break"] = {"phase": rec["s4len"],
                                   "pos": rec["s4"]["circle"].index(loser),
                                   "held": held}
                s4_open = False
        if rec["death"] is None and loser == watch:
            rec["death"] = {"pot": pot, "held": held, "phase": None,
                            "in_s4": in_first_s4}
            if pot == 2:
                rec["s2death"] = True
        pot = held
        active.pop(L)
        ptr = L % len(active) if active else 0
    rec["survivor"] = active[0]
    return rec


# ---------------- closed forms (proved; see report.md) ----------------

def s5u_case(m):
    """Predicted (sub, n4, wpos, h) for m % 3 != 0 (U side, stretch-4 start).

    sub 1: A-I  (m=6k+1)  -> W4(3k),      watched at n-1, h=0
    sub 2: A-II (m=6k+4)  -> F(4,2;3k+1), watched at n-3, h=2
    sub 3: B-III(m=6k+2)  -> F(4,2;3k),   watched at n-3, h=2
    sub 4: B-IV (m=6k+5)  -> W4(3k+2),    watched at n-1, h=0
    """
    if m % 3 == 1:
        q = (m - 1) // 3
        if q % 2 == 0:
            k = q // 2
            return (1, 3 * k, 3 * k - 1, 0)
        k = (q - 1) // 2
        return (2, 3 * k + 1, 3 * k - 2, 2)
    q = (m - 2) // 3
    if q % 2 == 0:
        k = q // 2
        return (3, 3 * k, 3 * k - 3, 2)
    k = (q - 1) // 2
    return (4, 3 * k + 2, 3 * k + 1, 0)


def s5v_case(m):
    """Predicted (sub, n4, wpos, h) for m % 3 != 1 (V side, stretch-4 start).

    sub 1: V-A1 (m=6k+3)  -> F(4,3;3k),   watched at n-3, h=3
    sub 2: V-A2 (m=6k+6)  -> F(4,1;3k+2), watched at n-1, h=1
    sub 3: V-B1 (m=6k+2)  -> F(4,1;3k),   watched at n-1, h=1
    sub 4: V-B2 (m=6k+5)  -> F(4,3;3k+1), watched at n-3, h=3
    """
    if m % 3 == 0:
        q = m // 3
        if q % 2 == 1:
            k = (q - 1) // 2
            return (1, 3 * k, 3 * k - 3, 3)
        k = q // 2 - 1
        return (2, 3 * k + 2, 3 * k + 1, 1)
    q = (m - 2) // 3
    if q % 2 == 0:
        k = q // 2
        return (3, 3 * k, 3 * k - 1, 1)
    k = (q - 1) // 2
    return (4, 3 * k + 1, 3 * k - 2, 3)


def s3len_u(m):
    """Predicted stretch-3 length, m % 3 != 0."""
    n1 = 2 * ((m - 1) // 3) if m % 3 == 1 else 2 * ((m - 2) // 3) + 1
    if m % 3 == 1:
        return n1 // 4 + (1 if n1 % 4 else 0)
    return n1 // 4 + 1


def s3len_v(m):
    """Predicted stretch-3 length, m % 3 != 1."""
    n1 = 2 * (m // 3) - 1 if m % 3 == 0 else 2 * ((m - 2) // 3)
    if m % 3 == 0:
        return n1 // 4 + 1
    return n1 // 4 + (1 if n1 % 4 else 0)


def s4len_pred(n4, h):
    """Predicted first-stretch-4 length (death block = same number).

    h in {0,1}: watched sits at the deal wrap boundary n-1  -> (n-1)//5+1
    h in {2,3}: watched sits at n-3                          -> (n-3)//5+1
    Covers both death and survival (breaking) cases.
    """
    return (n4 - 1) // 5 + 1 if h <= 1 else (n4 - 3) // 5 + 1


def s4break_pos(n4, h):
    """Predicted breaking-loser position (ptr-frame circle), survival classes.

    W4(n) and F(4,1;n) (h in {0,1}), 5 !| n: loser at 4 - (n mod 5).
    F(4,2;n) and F(4,3;n) (h in {2,3}), n mod 5 in {0,1,3,4}:
        n=0 mod 5 -> n-1 ; n=1 mod 5 -> n-2 ; n=3 mod 5 -> 1 ; n=4 mod 5 -> 0
    Requires n >= 11.
    """
    if h <= 1:
        return 4 - (n4 % 5)
    return {0: n4 - 1, 1: n4 - 2, 3: 1, 4: 0}[n4 % 5]


# ---------------- checks ----------------

def run_checks():
    """All checks; returns (results dict, all_ok bool)."""
    brk_checked[0] = 0  # reset module-level counter (determinism across runs)
    res = {}
    ok_all = True

    def put(name, ok, n=None, extra=None):
        nonlocal ok_all
        entry = {"ok": bool(ok)}
        if n is not None:
            entry["count"] = n
        if extra:
            entry.update(extra)
        res[name] = entry
        if not ok:
            ok_all = False

    # ---- PIN ----
    with open(PIN_UV, "rb") as f:
        uv_bytes = f.read()
    with open(PIN_P, "rb") as f:
        p_bytes = f.read()
    uv = json.loads(uv_bytes)
    pp = json.loads(p_bytes)
    pin_ok = (hashlib.sha256(uv_bytes).hexdigest() == PIN_UV_SHA
              and hashlib.sha256(p_bytes).hexdigest() == PIN_P_SHA
              and uv["M"] == 8000 and len(uv["U"]) == 8000 and len(uv["V"]) == 8000
              and pp["N"] == 8000 and len(pp["P"]) == 8000
              and pp["P"][:40] == P_PIN_1_40)
    put("PIN", pin_ok, extra={
        "uv_sha256": hashlib.sha256(uv_bytes).hexdigest()[:8],
        "p_sha256": hashlib.sha256(p_bytes).hexdigest()[:8]})

    U_pin = uv["U"]  # U_pin[m-1] = U(m)
    V_pin = uv["V"]
    P_pin = pp["P"]  # P_pin[C-1] = P(C)

    # ---- RED-RECON: committed U/V tables vs committed P table via proved RED ----
    bad = 0
    for m in range(1, 4000):
        if P_pin[2 * m + 1 - 1] != 1 + 2 * V_pin[m - 1]:
            bad += 1
        if P_pin[2 * m + 2 - 1] != 3 + 2 * U_pin[m - 1]:
            bad += 1
    put("REDRECON", bad == 0, n=2 * 3999, extra={"mismatches": bad})

    # ---- TWIN30: twin-law proved classes on the committed P table ----
    law1_classes = {3, 5, 9, 15, 21, 25, 27}
    law2_classes = {2, 4, 8, 14, 20, 24, 26}
    viol = []
    census1 = {}
    census2 = {}
    for C in range(3, 8001, 2):
        c30 = C % 30
        if c30 in law1_classes:
            census1[c30] = census1.get(c30, 0) + 1
            if (P_pin[C - 1] == 1) != isprime(C):
                viol.append(["LAW1", C, P_pin[C - 1]])
    for C in range(2, 8001, 2):
        c30 = C % 30
        if c30 in law2_classes:
            census2[c30] = census2.get(c30, 0) + 1
            if (P_pin[C - 1] == C - 1) != isprime(C + 1):
                viol.append(["LAW2", C, P_pin[C - 1]])
    put("TWIN30", not viol, extra={
        "violations": len(viol), "law1_census": census1,
        "law2_census": census2, "first": viol[:5]})

    # ---- FRESH simulations ----
    fails = []
    spf_bad = pin_bad = sie3_bad = s5_bad = red_bad = brk_bad = 0
    n_u = n_v = n_u35 = n_v35 = 0
    for m in range(3, M_FRESH + 1):
        # ---- U side: U(m), watched label m-1 ----
        ru = play(m, 2, m - 1)
        n_u += 1
        if ru["survivor"] != U_pin[m - 1]:
            pin_bad += 1
            fails.append(["UPIN", m, ru["survivor"]])
        s = 2 * m + 3
        p = spf(s)
        if p != s:
            d = ru["death"]
            if d is None or d["pot"] != p - 1 or d["held"] != p - 1:
                spf_bad += 1
                fails.append(["USPF", m, d])
        elif ru["survivor"] != m - 1:
            spf_bad += 1
            fails.append(["USPFPRIME", m, ru["survivor"]])
        if ru["s2death"] != (m % 3 == 0):
            sie3_bad += 1
            fails.append(["USIEVE3", m, ru["s2death"]])
        if m % 3 != 0:
            n_u35 += 1
            s5_bad += s5u_checks(m, ru, s5u_case, fails)
        # ---- V side: V(m), watched label 0 ----
        rv = play(m, 1, 0)
        n_v += 1
        if rv["survivor"] != V_pin[m - 1]:
            pin_bad += 1
            fails.append(["VPIN", m, rv["survivor"]])
        s = 2 * m + 1
        p = spf(s)
        if p != s:
            d = rv["death"]
            if d is None or d["pot"] != p - 1 or d["held"] != p:
                spf_bad += 1
                fails.append(["VSPF", m, d])
        elif rv["survivor"] != 0:
            spf_bad += 1
            fails.append(["VSPFPRIME", m, rv["survivor"]])
        if rv["s2death"] != (m % 3 == 1):
            sie3_bad += 1
            fails.append(["VSIEVE3", m, rv["s2death"]])
        if m % 3 != 1:
            n_v35 += 1
            s5_bad += s5v_checks(m, rv, s5v_case, fails)
        # RED fresh reconstruction
        if 1 + 2 * rv["survivor"] != P_pin[2 * m + 1 - 1]:
            red_bad += 1
            fails.append(["REDV", m])
        if 3 + 2 * ru["survivor"] != P_pin[2 * m + 2 - 1]:
            red_bad += 1
            fails.append(["REDU", m])

    put("FRESHPIN", pin_bad == 0, n=n_u + n_v, extra={"mismatches": pin_bad})
    put("SPF", spf_bad == 0, n=n_u + n_v, extra={"mismatches": spf_bad})
    put("SIEVE3", sie3_bad == 0, n=n_u + n_v, extra={"mismatches": sie3_bad})
    put("S5U", True, n=n_u35)
    put("S5V", True, n=n_v35)
    put("REDFRESH", red_bad == 0, n=2 * (M_FRESH - 2),
        extra={"mismatches": red_bad})
    # split the s5 fails per side
    u_fails = [f for f in fails if f[0].startswith("U") and f[0] not in
               ("UPIN", "USPF", "USPFPRIME", "USIEVE3")]
    v_fails = [f for f in fails if f[0].startswith("V") and f[0] not in
               ("VPIN", "VSPF", "VSPFPRIME", "VSIEVE3")]
    brk_fails = [f for f in fails if f[0] in ("US4BREAK", "VS4BREAK")]
    res["S5U"]["mismatches"] = len(u_fails) - len(
        [f for f in u_fails if f[0] == "US4BREAK"])
    res["S5V"]["mismatches"] = len(v_fails) - len(
        [f for f in v_fails if f[0] == "VS4BREAK"])
    res["S5U"]["ok"] = res["S5U"]["mismatches"] == 0
    res["S5V"]["ok"] = res["S5V"]["mismatches"] == 0
    put("S4BREAK", not brk_fails, n=len(brk_fails) + brk_checked[0],
        extra={"mismatches": len(brk_fails)})
    if brk_fails:
        ok_all = False
    if u_fails or v_fails:
        ok_all = False
    if not (pin_bad == 0 and spf_bad == 0 and sie3_bad == 0 and red_bad == 0):
        ok_all = False
    res["FRESHFAILS"] = {"ok": True, "total": len(fails),
                         "first": [list(x) for x in fails[:12]]}
    return res, ok_all


brk_checked = [0]


def s5u_checks(m, ru, case_fn, fails):
    """SIEVE5-U closed-form checks for one m (m % 3 != 0). Returns fail count."""
    bad = 0
    sub, n4p, wposp, hp = case_fn(m)
    d = ru["death"]
    dies4 = bool(d and d["in_s4"])
    if dies4 != (m % 5 == 1):
        bad += 1
        fails.append(["US5LAW", m, d])
        return bad
    if dies4:
        if d["held"] != 4:
            bad += 1
            fails.append(["US5HELD", m, d])
        exp_block = n4p // 5 if hp == 0 else (n4p - 2) // 5
        if d["phase"] != exp_block:
            bad += 1
            fails.append(["US5BLOCK", m, d["phase"], exp_block])
    if ru["s3len"] != s3len_u(m):
        bad += 1
        fails.append(["US3LEN", m, ru["s3len"], s3len_u(m)])
    s4 = ru["s4"]
    if s4 is None:
        if n4p > 1 or ru["survivor"] != m - 1:
            bad += 1
            fails.append(["US4MISS", m, n4p])
        return bad
    if s4["n"] != n4p or s4["wpos"] != wposp:
        bad += 1
        fails.append(["US4START", m, s4["n"], n4p, s4["wpos"], wposp])
        return bad
    # holdings pattern: circle positions i >= n-h hold 5, others 4
    for i, lab in enumerate(s4["circle"]):
        want = 5 if i >= n4p - hp else 4
        if s4["holdings"][lab] != want:
            bad += 1
            fails.append(["US4HOLD", m, i, s4["holdings"][lab], want])
            break
    # stretch-4 length (death or breaking) closed form
    if dies4 or ru["s4_break"] is not None:
        if ru["s4len"] != s4len_pred(n4p, hp):
            bad += 1
            fails.append(["US4LEN", m, ru["s4len"], s4len_pred(n4p, hp)])
    # breaking structure in survival classes
    if not dies4 and n4p >= S4BREAK_MIN_N:
        if hp == 0 and n4p % 5 == 0:
            pass  # death class only; survival impossible (5|n -> died)
        else:
            b = ru["s4_break"]
            brk_checked[0] += 1
            if b is None:
                bad += 1
                fails.append(["US4BREAK", m, None])
            elif (b["phase"] != s4len_pred(n4p, hp)
                  or b["pos"] != s4break_pos(n4p, hp) or b["held"] != 5):
                bad += 1
                fails.append(["US4BREAK", m, b, s4break_pos(n4p, hp)])
    return bad


def s5v_checks(m, rv, case_fn, fails):
    """SIEVE5-V closed-form checks for one m (m % 3 != 1). Returns fail count."""
    bad = 0
    sub, n4p, wposp, hp = case_fn(m)
    if n4p == 0:
        # degenerate end: H3(1) (only V-A1 with m=3): the watched label is
        # the sole survivor; no stretch-3/4 phase ever happens.
        if not (rv["survivor"] == 0 and rv["death"] is None
                and rv["s3len"] == 0 and rv["s4"] is None):
            bad += 1
            fails.append(["VS5EDGE", m, rv["survivor"], rv["death"]])
        return bad
    d = rv["death"]
    dies4 = bool(d and d["in_s4"])
    if dies4 != (m % 5 == 2):
        bad += 1
        fails.append(["VS5LAW", m, d])
        return bad
    if dies4:
        if d["held"] != 5:
            bad += 1
            fails.append(["VS5HELD", m, d])
        if d["phase"] != ru_len_ok(rv) or d["phase"] != s4len_pred(n4p, hp):
            bad += 1
            fails.append(["VS5LEN", m, d["phase"], s4len_pred(n4p, hp)])
        if not (d["phase"] == rv["s4len"]):
            bad += 1
            fails.append(["VS5FINAL", m])
    if rv["s3len"] != s3len_v(m):
        bad += 1
        fails.append(["VS3LEN", m, rv["s3len"], s3len_v(m)])
    s4 = rv["s4"]
    if s4 is None:
        if n4p > 1 or rv["survivor"] != 0:
            bad += 1
            fails.append(["VS4MISS", m, n4p])
        return bad
    if s4["n"] != n4p or s4["wpos"] != wposp:
        bad += 1
        fails.append(["VS4START", m, s4["n"], n4p, s4["wpos"], wposp])
        return bad
    for i, lab in enumerate(s4["circle"]):
        want = 5 if i >= n4p - hp else 4
        if s4["holdings"][lab] != want:
            bad += 1
            fails.append(["VS4HOLD", m, i, s4["holdings"][lab], want])
            break
    if not dies4 and n4p >= S4BREAK_MIN_N:
        if hp == 1 and n4p % 5 == 0:
            pass
        else:
            b = rv["s4_break"]
            brk_checked[0] += 1
            if b is None:
                bad += 1
                fails.append(["VS4BREAK", m, None])
            elif (b["phase"] != s4len_pred(n4p, hp)
                  or b["pos"] != s4break_pos(n4p, hp) or b["held"] != 5):
                bad += 1
                fails.append(["VS4BREAK", m, b, s4break_pos(n4p, hp)])
    return bad


def ru_len_ok(rv):
    return rv["s4len"]


def main():
    res, ok = run_checks()
    print(json.dumps(res, indent=2, sort_keys=True))
    print("ALL_OK" if ok else "FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
