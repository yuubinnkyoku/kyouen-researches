#!/usr/bin/env python3
"""K0928/K0929 verifier: P(C) structure of the K0859 counting recursion.

Proved objects (universal proofs written in report.md; machine anchors here):
  STRE     Lemma E: for even C the first C/2+1 eliminations of run(C,C) are
           exactly P_0, P_2, ..., P_{C-2}, P_1 (holdings 1,..,1,2) and the
           reduced state is m=C/2-1 players [P_3,P_5,..,P_{C-1}] all holding 2,
           pot 2, pointer P_3.
  STRO     Lemma O: for odd C the first (C+1)/2 eliminations are exactly
           P_0, P_2, ..., P_{C-1} (all holding 1) and the reduced state is
           m=(C-1)/2 players [P_1,..,P_{C-2}] all holding 2, pot 1, pointer P_1.
  PARITY   Theorem PAR: P(C) is odd for every C >= 2 (proved; anchored on the
           committed table C <= 8000 and the recomputed prefix).
  RED      Theorem RED: P(2m+2) = 3 + 2*U(m), P(2m+1) = 1 + 2*V(m) where
           U/V are the uniform reduced games (each m players hold 2; pot 2
           resp. 1). Checked two ways: pure-python reduced reimplementation
           m <= 150 against the committed tables, and full reconstruction of
           the committed P table from the committed U/V tables (C <= 8000).
Conjectures (machine ranges only, no universal claim):
  LAWS     C <= 8000 committed direct table (two independent JS engines,
           cross-checked against this verifier's python recomputation):
           LAW1 P(C)=1 <=> C prime; LAW2 P(C)=C-1 <=> C+1 prime.
  REDLAWS  m <= 8000 committed reduced tables: V(m)=0 <=> 2m+1 prime;
           U(m)=m-1 <=> 2m+3 prime (via RED this covers C <= 16001).
Anchors:
  PIN      P(1..40) == the K0919 published pin (recomputed here in python).
  REF      python survivor_fast (K0926 published logic) recomputes the
           committed P table prefix C <= 300 exactly.
  TWIN     verbatim per-stone recursion == closed-form twin, C <= 150.

Usage: python3 verify_pc_twin_laws.py [--no-cache]
Audit JSON must be byte-identical across runs (run twice).
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "output")
AUDIT = os.path.join(OUT, "pc_twin_laws_audit.json")

K0919_P40 = [0, 1, 1, 3, 1, 5, 1, 5, 5, 9, 1, 11, 1, 5, 7, 15, 1, 17,
             1, 15, 17, 21, 1, 21, 11, 15, 7, 27, 1, 29, 1, 27, 17, 21,
             11, 35, 1, 5, 7, 39]

# ---------------------------------------------------------------- engines


def survivor_fast(C, r):
    """Closed-form-phase survivor (same dynamics as the K0926 verifier)."""
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


def run_trace(C, r):
    """Full trace with loser holdings and post-state (K0859 recursion)."""
    active = list(range(r))
    counts = [0] * r
    turn = 0
    elim = []  # (loser, holding_at_elimination)
    while len(active) > 1:
        k = len(active)
        s = sum(counts[p] for p in active)
        ell = C - s
        q, t = divmod(ell, k)
        for i in range(k):
            counts[active[(turn + i) % k]] += q + (1 if i < t else 0)
        li = (turn + ell) % k
        loser = active[li]
        elim.append((loser, counts[loser]))
        counts[loser] = 0
        active.pop(li)
        turn = li % len(active) if active else 0
    pot = C - sum(counts[p] for p in active)
    return elim, active, counts, turn, pot


def stretch_state(C, nphases):
    """State of run(C,C) right after `nphases` phases
    (active, counts, pointer position, pot)."""
    r = C
    active = list(range(r))
    counts = [0] * r
    turn = 0
    for _ in range(nphases):
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
        turn = li % len(active) if active else 0
    pot = C - sum(counts[p] for p in active)
    return active, counts, turn, pot


def run_verbatim(C, r):
    """Verbatim per-stone K0859 recursion."""
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


def reduced_survivor(m, pot0):
    """Uniform reduced game: m players each holding 2, given pot, pointer 0.
    Independent reimplementation of pc_reduced.js in python."""
    active = list(range(m))
    counts = [2] * m
    ptr = 0
    pot = pot0
    while len(active) > 1:
        k = len(active)
        pos = ptr
        for _ in range(pot):
            counts[active[pos]] += 1
            pos = (pos + 1) % k
        loser = active[pos]
        pot = counts[loser]
        counts[loser] = 0
        active.pop(pos)
        ptr = pos % len(active)
    return active[0]


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# ---------------------------------------------------------------- checks


def check_pin():
    P = [survivor_fast(C, C) for C in range(1, 41)]
    ok = P == K0919_P40
    return {"name": "PIN: recomputed P(1..40) equals the K0919 published pin",
            "ok": ok, "data": {"P40": P}}


def check_ref(tab):
    N = 300
    rec = [survivor_fast(C, C) for C in range(1, N + 1)]
    ok = rec == tab["P"][:N]
    return {"name": "REF: python survivor_fast recomputes the committed P table prefix C<=300 exactly",
            "ok": ok, "data": {"N": N}}


def check_twin():
    bad = 0
    for C in range(2, 151):
        ev, svv = run_verbatim(C, C)
        tr = run_trace(C, C)
        if ev != tuple(x[0] for x in tr[0]) or svv != tr[1][0]:
            bad += 1
    return {"name": "TWIN: verbatim per-stone recursion == closed-form twin (elim order + survivor), C=2..150",
            "ok": bad == 0, "data": {"pairs": 149, "violations": bad}}


def check_stre():
    """Lemma E machine anchor: even C <= 120."""
    bad = 0
    for C in range(4, 121, 2):
        m = C // 2 - 1
        elim, _active, _c, _t, _p = run_trace(C, C)
        got_elim = [x[0] for x in elim[:m + 2]]
        got_hold = [x[1] for x in elim[:m + 2]]
        expect_elim = list(range(0, C - 1, 2)) + [1]  # P_0,P_2,..,P_{C-2},P_1
        exp_hold = [1] * (m + 1) + [2]
        active, counts, turn, pot = stretch_state(C, m + 2)
        state = (active == list(range(3, C, 2))
                 and all(counts[p] == 2 for p in active)
                 and turn == 0 and pot == 2)
        if got_elim != expect_elim or got_hold != exp_hold or not state:
            bad += 1
    return {"name": "STRE: Lemma E (first stretch, even C): eliminations P_0,P_2,..,P_{C-2},P_1 with holdings (1..1,2), reduced state odds>=3 all 2, pot 2, ptr P_3; C=4..120 even",
            "ok": bad == 0, "data": {"checked": 59, "violations": bad}}


def check_stro():
    """Lemma O machine anchor: odd C <= 121."""
    bad = 0
    for C in range(3, 122, 2):
        m = (C - 1) // 2
        elim, _active, _c, _t, _p = run_trace(C, C)
        got_elim = [x[0] for x in elim[:m + 1]]
        got_hold = [x[1] for x in elim[:m + 1]]
        expect_elim = list(range(0, C, 2))  # P_0,P_2,..,P_{C-1}
        active, counts, turn, pot = stretch_state(C, m + 1)
        state = (active == list(range(1, C, 2))
                 and all(counts[p] == 2 for p in active)
                 and turn == 0 and pot == 1)
        if got_elim != expect_elim or got_hold != [1] * (m + 1) or not state:
            bad += 1
    return {"name": "STRO: Lemma O (first stretch, odd C): eliminations P_0,P_2,..,P_{C-1} all holding 1, reduced state odds all 2, pot 1, ptr P_1; C=3..121 odd",
            "ok": bad == 0, "data": {"checked": 60, "violations": bad}}


def check_red(tab, uv):
    M = 150
    badU = [m for m in range(1, M + 1)
            if reduced_survivor(m, 2) != uv["U"][m - 1]]
    badV = [m for m in range(1, M + 1)
            if reduced_survivor(m, 1) != uv["V"][m - 1]]
    # full reconstruction of the committed P table from committed U/V
    recon_bad = 0
    for m in range(1, min(M, (tab["N"] - 2) // 2) + 1):
        if tab["P"][2 * m + 1] != 3 + 2 * uv["U"][m - 1]:
            recon_bad += 1
        if tab["P"][2 * m] != 1 + 2 * uv["V"][m - 1]:
            recon_bad += 1
    ok = not badU and not badV and recon_bad == 0
    return {"name": "RED: python reduced-game reimplementation matches committed U/V tables m<=150, and P(2m+2)=3+2U, P(2m+1)=1+2V holds on the committed tables m<=150",
            "ok": ok, "data": {"badU": badU[:5], "badV": badV[:5],
                               "recon_violations": recon_bad, "M": M}}


def check_recon(tab, uv):
    """Full-range reconstruction: committed P == 3+2U / 1+2V, all C <= 8000."""
    bad = 0
    N = tab["N"]
    for m in range(1, (N - 2) // 2 + 1):
        if tab["P"][2 * m + 1] != 3 + 2 * uv["U"][m - 1]:
            bad += 1
    for m in range(1, (N - 1) // 2 + 1):
        if tab["P"][2 * m] != 1 + 2 * uv["V"][m - 1]:
            bad += 1
    return {"name": "RECON: committed P table C<=8000 is exactly reconstructed from the committed U/V tables via Theorem RED (both parities, all m)",
            "ok": bad == 0,
            "data": {"violations": bad, "even_pairs": (N - 2) // 2,
                     "odd_pairs": (N - 1) // 2}}


def check_laws(tab):
    N = tab["N"]
    P = tab["P"]
    bad1 = 0
    bad2 = 0
    nprime = 0
    nplus = 0
    bad_parity = 0
    for C in range(2, N + 1):
        v = P[C - 1]
        if (v == 1) != is_prime(C):
            bad1 += 1
        if (v == C - 1) != is_prime(C + 1):
            bad2 += 1
        if v % 2 != 1:
            bad_parity += 1
        if v == 1:
            nprime += 1
        if v == C - 1:
            nplus += 1
    ok = bad1 == 0 and bad2 == 0 and bad_parity == 0
    return {"name": "LAWS: on the committed direct table C<=8000: LAW1 P(C)=1 <=> C prime; LAW2 P(C)=C-1 <=> C+1 prime; PARITY P(C) odd for C>=2 (anchor of the proved Theorem PAR)",
            "ok": ok,
            "data": {"N": N, "law1_violations": bad1, "law2_violations": bad2,
                     "parity_violations": bad_parity,
                     "count_P_is_1": nprime, "count_P_is_C_minus_1": nplus}}


def check_redlaws(uv):
    M = uv["M"]
    U = uv["U"]
    V = uv["V"]
    badV = 0
    badU = 0
    zerosV = 0
    maxU = 0
    for m in range(1, M + 1):
        if (V[m - 1] == 0) != is_prime(2 * m + 1):
            badV += 1
        if (U[m - 1] == m - 1) != is_prime(2 * m + 3):
            badU += 1
        if V[m - 1] == 0:
            zerosV += 1
        if U[m - 1] == m - 1:
            maxU += 1
    ok = badV == 0 and badU == 0
    return {"name": "REDLAWS: on the committed reduced tables m<=8000: V-law V(m)=0 <=> 2m+1 prime; U-law U(m)=m-1 <=> 2m+3 prime (covers C<=16001 via the proved Theorem RED)",
            "ok": ok,
            "data": {"M": M, "vlaw_violations": badV, "ulaw_violations": badU,
                     "count_V_zero": zerosV, "count_U_max": maxU}}


def check_corollary(tab):
    """Proved halves: even C>=4 never P=1; odd C>=3 never P=C-1."""
    bad = 0
    N = tab["N"]
    for C in range(4, N + 1, 2):
        if tab["P"][C - 1] == 1 or tab["P"][C - 1] % 2 == 0 or tab["P"][C - 1] < 3:
            bad += 1
    for C in range(3, N + 1, 2):
        if tab["P"][C - 1] == C - 1:
            bad += 1
    return {"name": "COR: proved corollary anchors on the committed table: P(2m+2)>=3 odd (no even C>=4 has P=1) and no odd C>=3 has P=C-1",
            "ok": bad == 0, "data": {"violations": bad}}


# ---------------------------------------------------------------- assemble


def assemble():
    with open(os.path.join(DATA, "pc_p8000.json")) as f:
        tab = json.load(f)
    with open(os.path.join(DATA, "pc_uv8000.json")) as f:
        uv = json.load(f)
    checks = [check_pin(), check_ref(tab), check_twin(), check_stre(),
              check_stro(), check_red(tab, uv), check_recon(tab, uv),
              check_laws(tab), check_redlaws(uv), check_corollary(tab)]
    audit = {
        "all_ok": all(c["ok"] for c in checks),
        "checks": checks,
        "date": "2026-11-17",
        "follows": "K0859 (theorem D counting recursion, the object), K0919 (P(C) pin C=1..40), K0922 (P(C)=1<=>prime observed C<=300 and the 61-value P(C)=C-1 list which LAW2 identifies as exactly the C with C+1 prime), K0926 (E6U: P(C)=S(C,r) for r>=C, survivor_fast reference logic)",
        "items": ["K0928", "K0929"],
        "pins": {
            "pc_fast.js": sha256_file(os.path.join(HERE, "pc_fast.js")),
            "pc_reduced.js": sha256_file(os.path.join(HERE, "pc_reduced.js")),
            "data/pc_p8000.json": sha256_file(os.path.join(DATA, "pc_p8000.json")),
            "data/pc_uv8000.json": sha256_file(os.path.join(DATA, "pc_uv8000.json")),
        },
        "title": "P(C) twin prime laws and the parity/reduction theorems for the K0859 counting recursion: proved Lemma E/O (first-stretch sieve), Theorem PAR (P(C) odd for C>=2), Theorem RED (P(2m+2)=3+2U(m), P(2m+1)=1+2V(m)); conjectured LAW1/LAW2 (P(C)=1 <=> C prime, P(C)=C-1 <=> C+1 prime) machine-verified C<=8000 direct and C<=16001 via RED",
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
        print("  %-6s %s" % ("OK" if c["ok"] else "FAIL", c["name"][:110]))
    return 0 if audit["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
