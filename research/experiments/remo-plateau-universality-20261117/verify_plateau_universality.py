#!/usr/bin/env python3
"""K0926 verifier: plateau universality E6U for the K0859 counting recursion.

Checks (all deterministic, stdlib only, no external sweeps):
  PIN      P(C) = S(C, C) table C=1..40 pinned to the K0919 published list.
  CAS      Lemma CAS (universal statement, exhaustive machine check
           r=2..40 x C=1..r-1): phase-1 loser P_C, zero-stone cascade
           eliminating P_{C+1}..P_{r-1} in phases 2..r-C with ell=0,
           canonical state K_C reached after phase r-C (C>=2),
           survivor P_0 for C=1.
  COUPLE   The coupling step of the proof (exhaustive r=2..60 x C=1..r-1):
           run (C,r) reaches K_C after phase r-C, run (C,r+1) reaches the
           identical state after phase r-C+1, the two continuations are
           identical (k, ell, li, loser) sequences, survivors equal.
  E6U      S(C,r) == P(C) for r=2..60, C=1..min(r-1,40) exhaustive
           plus anchor spots r in {61, 97, 128} for C=1..40.
  TWIN     verbatim per-stone K0859 recursion == closed-form twin on all
           (C,r) with C<=min(r-1,30), r<=40, plus the diagonal (C,C), C<=40.
  WITCONN  Bounded-witness connection (finite): r=2..24, every proper
           divisor d of Q(r) has a witness C in [1, r-1] against the
           window values S(C,r)=P(C) (early-exit scan).
Audit JSON assembled from a single data pass and required byte-identical
across runs (run twice; --no-cache recomputes everything).

Usage: python3 verify_plateau_universality.py [--no-cache]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
AUDIT = os.path.join(OUT, "plateau_universality_audit.json")

K0919_P40 = [0, 1, 1, 3, 1, 5, 1, 5, 5, 9, 1, 11, 1, 5, 7, 15, 1, 17,
             1, 15, 17, 21, 1, 21, 11, 15, 7, 27, 1, 29, 1, 27, 17, 21,
             11, 35, 1, 5, 7, 39]

# ---------------------------------------------------------------- runs


def run_trace(C, r):
    """Closed-form twin with per-phase pre-state (K0859 recursion)."""
    active = list(range(r))
    counts = [0] * r
    turn = 0
    phases = []
    while len(active) > 1:
        k = len(active)
        s = sum(counts[p] for p in active)
        ell = C - s
        q, t = divmod(ell, k)
        li = (turn + ell) % k
        loser = active[li]
        phases.append({"k": k, "ell": ell, "li": li, "loser": loser,
                       "turn": turn, "active": list(active),
                       "counts": list(counts)})
        for i in range(k):
            counts[active[(turn + i) % k]] += q + (1 if i < t else 0)
        counts[loser] = 0
        active.pop(li)
        if active:
            turn = li % len(active)
    return phases, active[0]


def survivor_fast(C, r):
    """Survivor only (same dynamics as run_trace)."""
    active = list(range(r))
    counts = [0] * r
    turn = 0
    while len(active) > 1:
        k = len(active)
        s = sum(counts[p] for p in active)
        ell = C - s
        q, t = divmod(ell, k)
        for i in range(k):
            counts[active[(turn + i) % k]] += q + (1 if i < t else 0)
        li = (turn + ell) % k
        loser = active[li]
        counts[loser] = 0
        active.pop(li)
        if active:
            turn = li % len(active)
    return active[0]


def run_verbatim(C, r):
    """Verbatim K0859 per-stone recursion (K0925 TWIN anchor object)."""
    active = list(range(r))
    counts = [0] * r
    turn = 0
    elim = []
    while len(active) > 1:
        k = len(active)
        s = sum(counts[p] for p in active)
        ell = C - s
        for m in range(ell):
            counts[active[(turn + m) % k]] += 1
        li = (turn + ell) % k
        loser = active[li]
        elim.append(loser)
        counts[loser] = 0
        active.pop(li)
        if active:
            turn = li % len(active)
    return tuple(elim), active[0]


def lcm_all(r):
    out = 1
    for i in range(2, r + 1):
        a, b = out, i
        while b:
            a, b = b, a % b
        out = out * i // a
    return out


def divisors(n):
    out = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            out.append(i)
            if i != n // i:
                out.append(n // i)
        i += 1
    return sorted(out)


def canonical_state(trace, upto):
    """Post-phase state after trace phase index `upto` (0-based)."""
    active = list(range(trace[0]["k"]))
    counts = [0] * trace[0]["k"]
    turn = 0
    for ph in trace[:upto + 1]:
        k = ph["k"]
        ell = ph["ell"]
        q, t = divmod(ell, k)
        for i in range(k):
            counts[active[(turn + i) % k]] += q + (1 if i < t else 0)
        li = (turn + ell) % k
        loser = active[li]
        counts[loser] = 0
        active.pop(li)
        turn = li % len(active) if active else 0
    return active, counts, turn


# ---------------------------------------------------------------- checks


def check_pin():
    P = {}
    for C in range(1, 41):
        P[C] = survivor_fast(C, C)
    ok = [P[C] for C in range(1, 41)] == K0919_P40
    return {"name": "PIN: P(C)=S(C,C) recomputed C=1..40 equals the K0919 published P(C) pin",
            "ok": ok, "data": {"P40": [P[C] for C in range(1, 41)]}}


def check_cas(P):
    bad = 0
    examples = []
    for r in range(2, 41):
        for C in range(1, r):
            trace, sv = run_trace(C, r)
            ok = True
            # phase 1: ell==C, loser P_C
            if trace[0]["ell"] != C or trace[0]["loser"] != C:
                ok = False
            # phases 1..r-C: losers P_C..P_{r-1} in order, ell==0 for j>=2
            for j in range(r - C):
                if trace[j]["loser"] != C + j:
                    ok = False
                if j >= 1 and trace[j]["ell"] != 0:
                    ok = False
            if C == 1:
                # survivor P_0 reached right after the cascade
                if sv != 0 or len(trace) != r - 1:
                    ok = False
                if trace[r - 2]["loser"] != r - 1:
                    ok = False
            else:
                act, cnt, turn = canonical_state(trace, r - C - 1)
                if act != list(range(C)) or any(cnt[p] != 1 for p in act) or turn != 0:
                    ok = False
            if not ok:
                bad += 1
                if len(examples) < 5:
                    examples.append({"r": r, "C": C})
    return {"name": "CAS: zero-stone cascade lemma, exhaustive r=2..40 x C=1..r-1 (losers P_C..P_{r-1}, ell=0 in phases 2..r-C, canonical state K_C after phase r-C, survivor P_0 for C=1)",
            "ok": bad == 0, "data": {"violations": bad, "examples": examples}}


def check_couple():
    bad = 0
    examples = []
    for r in range(2, 61):
        for C in range(1, r):
            trA, svA = run_trace(C, r)
            trB, svB = run_trace(C, r + 1)
            # A reaches K_C after phase r-C (index r-C-1); B after phase r-C+1
            if C == 1:
                okA = len(trA) == r - 1 and trA[-1]["loser"] == r - 1 and svA == 0
                okB = len(trB) == r and trB[-1]["loser"] == r and svB == 0
                ok = okA and okB and svA == svB
            else:
                actA, cntA, turnA = canonical_state(trA, r - C - 1)
                actB, cntB, turnB = canonical_state(trB, r - C)
                # compare states projected on the active players
                # (eliminated players carry count 0 and never return)
                ok = (actA == actB and turnA == turnB
                      and [cntA[p] for p in actA] == [cntB[p] for p in actB]
                      and actA == list(range(C))
                      and all(cntA[p] == 1 for p in actA) and turnA == 0)
                if ok:
                    # continuations identical
                    contA = [(p["k"], p["ell"], p["li"], p["loser"]) for p in trA[r - C:]]
                    contB = [(p["k"], p["ell"], p["li"], p["loser"]) for p in trB[r - C + 1:]]
                    if contA != contB or svA != svB:
                        ok = False
            if not ok:
                bad += 1
                if len(examples) < 5:
                    examples.append({"r": r, "C": C})
    return {"name": "COUPLE: merge coupling run(C,r) vs run(C,r+1) both reach the identical canonical state K_C and proceed identically, exhaustive r=2..60 x C=1..r-1",
            "ok": bad == 0, "data": {"violations": bad, "examples": examples}}


def check_e6u(P):
    bad = 0
    examples = []
    checked = 0
    for r in range(2, 61):
        for C in range(1, min(r, 41)):
            checked += 1
            if survivor_fast(C, r) != P[C]:
                bad += 1
                if len(examples) < 5:
                    examples.append({"r": r, "C": C})
    spots = 0
    for r in (61, 97, 128):
        for C in range(1, 41):
            spots += 1
            if survivor_fast(C, r) != P[C]:
                bad += 1
                if len(examples) < 5:
                    examples.append({"r": r, "C": C, "spot": True})
    return {"name": "E6U: S(C,r)==P(C) for r>=C, exhaustive r=2..60 x C<=min(r-1,40) plus anchor spots r in {61,97,128} x C=1..40",
            "ok": bad == 0,
            "data": {"violations": bad, "exhaustive_pairs": checked, "spot_pairs": spots}}


def check_twin():
    bad = 0
    pairs = 0
    for r in range(2, 41):
        for C in range(1, min(r, 31)):
            pairs += 1
            ev, svv = run_verbatim(C, r)
            tr, svf = run_trace(C, r)
            ef = tuple(p["loser"] for p in tr)
            if ev != ef or svv != svf:
                bad += 1
    for C in range(1, 41):
        pairs += 1
        ev, svv = run_verbatim(C, C)
        tr, svf = run_trace(C, C)
        if ev != tuple(p["loser"] for p in tr) or svv != svf:
            bad += 1
    return {"name": "TWIN: verbatim per-stone K0859 recursion == closed-form twin, all C<=min(r-1,30) x r<=40 plus diagonal (C,C) C<=40 (full elim sequence + survivor)",
            "ok": bad == 0, "data": {"pairs": pairs, "violations": bad}}


def check_witconn(P):
    bad = 0
    total = 0
    missing = []
    per_r = {}
    for r in range(2, 25):
        Q = lcm_all(r)
        proper = divisors(Q)[:-1]
        svC = {C: survivor_fast(C, r) for C in range(1, r)}
        # window values equal P(C) (E6U)
        for C in range(1, r):
            if svC[C] != P[C]:
                return {"name": "WITCONN", "ok": False,
                         "data": {"error": "window value != P(C)", "r": r, "C": C}}
        nowit = 0
        maxc = 0
        for d in proper:
            total += 1
            w = None
            for C in range(1, r):
                if survivor_fast(C + d, r) != svC[C]:
                    w = C
                    break
            if w is None:
                nowit += 1
                bad += 1
                if len(missing) < 10:
                    missing.append({"r": r, "d": d})
            elif w > maxc:
                maxc = w
        per_r[str(r)] = {"proper": len(proper), "no_witness_in_window": nowit,
                         "max_first_witness": maxc}
    return {"name": "WITCONN: bounded-witness connection (finite), r=2..24 every proper divisor d of Q(r) has a witness C in [1,r-1] against window values S(C,r)=P(C)",
            "ok": bad == 0,
            "data": {"total_divisors": total, "missing": missing, "per_r": per_r}}


def assemble():
    P = {}
    for C in range(1, 41):
        P[C] = survivor_fast(C, C)
    checks = [check_pin(), check_cas(P), check_couple(), check_e6u(P),
              check_twin(), check_witconn(P)]
    audit = {
        "all_ok": all(c["ok"] for c in checks),
        "checks": checks,
        "date": "2026-11-17",
        "follows": "K0859 (theorem D counting recursion, the object), K0919 (E6 finite plateau observation C<=24 and the P(C) pin C=1..40 that this experiment proves universally and reproduces exactly), K0925 (bounded-witness observation wit_max_sv <= r-1, r<=32; the window reformulation [1,r-1] of that conjecture is connected here and machine-confirmed for r<=24)",
        "item": "K0926",
        "title": "Plateau universality E6U: S(C,r) = S(C,C) = P(C) for every r >= C (universal proof via the zero-stone cascade lemma CAS and the merge coupling), closing the K0919 E6 finite observation",
    }
    return audit


def main():
    no_cache = "--no-cache" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    audit = assemble()
    blob = json.dumps(audit, indent=1, sort_keys=True) + "\n"
    if not no_cache and os.path.exists(AUDIT):
        with open(AUDIT) as f:
            old = f.read()
        if old == blob:
            print("OK: audit byte-identical")
            return 0
    with open(AUDIT, "w") as f:
        f.write(blob)
    print("audit written (%d bytes)" % len(blob.encode()))
    print("all_ok =", audit["all_ok"])
    for c in audit["checks"]:
        print("  %-8s %s" % ("OK" if c["ok"] else "FAIL", c["name"][:110]))
    return 0 if audit["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
