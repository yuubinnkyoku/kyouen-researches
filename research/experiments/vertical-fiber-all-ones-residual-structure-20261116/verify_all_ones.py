#!/usr/bin/env python3
"""Verifier for the all-ones residual family structure (kappa=1, X=(1^k)).

Context (K0832 residual game, kappa=1): H(R;X;z) with moves
  A: token x>=2 -> x-1;  B: token 1 -> z+1;  C (z>=1): z -> z-1 with value flip.
For the all-ones multiset X=(1^k) the state collapses to (k, z, R):
  h(k,z,R) = mex{ h(k-1,z+1,R-1) [k>=1],  1^h(k,z-1,R-1) [z>=1] },  h=0 at R=0.

Machine-checked claims (see report.md):
  W0  reduction engine vs general multiset engine (X=(1^k)), cross-check.
  W1  2-position closed form (CONJECTURE, main claim):
        z=0        : T = empty
        z odd      : T = {1,3,...,q(k)}        (q(n)=largest odd <= n)
        z even >=2 : T = {1,3,...,q(min(k,z))} u ({2k-z+1} if 2k-z+1 >= 1)
      checked on k,z <= 50 over the window R < 2k+z+2; the tail corollary
      (W4: R >= 2k+z-1 => h = k mod 2, from the all-t report's Lemma 4) and the
      window overlap make the 2-position capture self-contained.
  W2  random spot checks of W1 (k,z <= 80, R < 2k+z).
  W3  full-profile closed forms for the z=1 and z=2 slices (CONJECTURE),
      1 <= k <= 60, window R <= 2k+2 (k=0 is trivially all-0).
  W4  tail corollary: h(k,z,R) = k mod 2 for R >= 2k+z-1  (k<=60, z<=50).
  W5  play-length remark: every play has length exactly min(R, 2k+z)
      (random play simulations).
  W6  UNIFIED full-profile closed form for ALL z >= 1 (CONJECTURE, supersedes
      W3 as a strict generalisation), z <= 13, k <= 80, window R <= 2k+z+2.
        z odd (z >= 1):
          R odd : h = 2 if R <= q(k) else (k mod 2)
          R even, k odd :
              h = 0 if R <= min(z-3, k-1)  (pre-wave)
                       or (R ≡ z-1 (mod 4) and z-1 <= R <= 2k-z-1)  (AP4 zero wave)
              else h = 1
          R even, k even :
              h = 1 if R ≡ z+1 (mod 4) and z+1 <= R <= 2k-z-1  (AP4 one wave)
              else h = 0
        z even >= 2:
          h = 2 if R in {1,3,...,q(min(k,z))} or R == 2k-z+1 >= 1
          h = 1 if R ≡ z+1 (mod 4) and z+1 <= R <= 2k-z-1 and R != 2k-z+1
          k odd  : h = 0 if (R even and R <= k-1)
                            or (R ≡ z-1 (mod 4) and z+3 <= R <= 2k-z-3)
                   else h = 1
          k even : h = 0
      k=0 falls out as all-0 under the same formulae (verified in-window).
Writes audit JSON to stdout.
"""
import sys, json, random
from functools import lru_cache
sys.setrecursionlimit(3000000)

def q(n):  # largest odd <= n
    return n if n % 2 == 1 else n - 1

def mex(vals):
    g = 0
    s = set(vals)
    while g in s:
        g += 1
    return g

# ---------- engine 1: (k,z,R) reduction ----------
@lru_cache(maxsize=None)
def h(k, z, R):
    if R == 0:
        return 0
    cands = set()
    if k >= 1:
        cands.add(h(k - 1, z + 1, R - 1))
    if z >= 1:
        cands.add(1 ^ h(k, z - 1, R - 1))
    g = 0
    while g in cands:
        g += 1
    return g

# ---------- engine 2: general multiset engine (as in verify_single_token.py) ----------
@lru_cache(maxsize=None)
def H(R, X, z):
    if R == 0:
        return 0
    cands = set()
    for x in set(X):
        nx = list(X)
        if x >= 2:
            nx.remove(x); nx.append(x - 1); nx.sort()
            cands.add(H(R - 1, tuple(nx), z))
        else:
            nx.remove(1); nx.sort()
            cands.add(H(R - 1, tuple(nx), z + 1))
    if z >= 1:
        cands.add(1 ^ H(R - 1, X, z - 1))
    g = 0
    while g in cands:
        g += 1
    return g

# ---------- claimed structures ----------
def predT(k, z):
    """2-position set (conjectured closed form)."""
    if z == 0:
        return set()
    if z % 2 == 1:
        return set(range(1, q(k) + 1, 2))
    s = set(range(1, q(min(k, z)) + 1, 2))
    far = 2 * k - z + 1
    if far >= 1:
        s.add(far)
    return s

def slice_closed_form(k, z, R):
    """Full profile closed form for z in {1,2} (conjectured)."""
    if k == 0:
        return 0  # no tokens: only C moves, h(0,z,R)=0 for all R
    if z == 1:
        if k % 2 == 1:
            if R % 2 == 1 and R <= k:
                return 2
            if R % 4 == 0 and R <= 2 * k - 2:
                return 0
            return 1
        else:
            if R % 2 == 1 and R <= k - 1:
                return 2
            if R % 4 == 2 and 2 <= R <= 2 * k - 2:
                return 1
            return 0
    if z == 2:
        if k % 2 == 1:
            if R == 1 or R == 2 * k - 1:
                return 2
            if R % 2 == 0 and R <= k - 1:
                return 0
            if R % 4 == 1 and 5 <= R <= 2 * k - 5:
                return 0
            if R >= 2 * k:
                return 1
            return 1  # remaining transient: 1s (AP4(3)<=2k-3 and evens in [k+1,2k-2])
        else:
            if R == 1 or R == 2 * k - 1:
                return 2
            if R % 4 == 3 and 3 <= R <= 2 * k - 5:
                return 1
            return 0
    raise ValueError("slice only defined for z in {1,2}")

def unified_slice_closed_form(k, z, R):
    """Unified full-profile closed form for ALL z >= 1 (conjecture, W6).

    Supersedes slice_closed_form (z in {1,2}) as a strict generalisation;
    for k=0 the formulae evaluate to all-0, matching the trivial engine.
    """
    if z < 1:
        raise ValueError("unified slice defined for z >= 1")
    if z % 2 == 1:
        # z odd
        if R % 2 == 1:
            return 2 if R <= q(k) else (1 if k % 2 == 1 else 0)
        if k % 2 == 1:
            if R <= min(z - 3, k - 1):
                return 0
            if R % 4 == (z - 1) % 4 and z - 1 <= R <= 2 * k - z - 1:
                return 0
            return 1
        else:
            if R % 4 == (z + 1) % 4 and z + 1 <= R <= 2 * k - z - 1:
                return 1
            return 0
    else:
        # z even >= 2
        twos = set(range(1, q(min(k, z)) + 1, 2))
        far = 2 * k - z + 1
        if far >= 1:
            twos.add(far)
        if R in twos:
            return 2
        if R % 4 == (z + 1) % 4 and z + 1 <= R <= 2 * k - z - 1 and R != far:
            return 1
        if k % 2 == 1:
            if (R % 2 == 0 and R <= k - 1) or (R % 4 == (z - 1) % 4 and z + 3 <= R <= 2 * k - z - 3):
                return 0
            return 1
        return 0

def main():
    rng = random.Random(20261116)
    out = {"W0": {"checks": 0, "mismatches": 0, "first": []},
           "W1": {"checks": 0, "mismatches": 0, "first": []},
           "W2": {"checks": 0, "mismatches": 0, "first": []},
           "W3": {"checks": 0, "mismatches": 0, "first": []},
           "W4": {"checks": 0, "mismatches": 0, "first": []},
           "W5": {"checks": 0, "violations": 0},
           "W6": {"checks": 0, "mismatches": 0, "first": []}}

    # ---- W0: reduction vs multiset engine ----
    for k in range(0, 21):
        for z in range(0, 13):
            for R in range(0, 31):
                out["W0"]["checks"] += 1
                a = h(k, z, R)
                b = H(R, (1,) * k, z)
                if a != b:
                    out["W0"]["mismatches"] += 1
                    if len(out["W0"]["first"]) < 5:
                        out["W0"]["first"].append([k, z, R, a, b])

    # ---- W1: 2-position closed form, full grid, window R < 2k+z ----
    for k in range(0, 51):
        for z in range(0, 51):
            n = 2 * k + z
            act = set(R for R in range(1, n + 2) if h(k, z, R) == 2)
            pred = set(p for p in predT(k, z) if p < n + 2)
            out["W1"]["checks"] += 1
            if act != pred:
                out["W1"]["mismatches"] += 1
                if len(out["W1"]["first"]) < 5:
                    out["W1"]["first"].append([k, z, sorted(pred), sorted(act)])

    # ---- W2: random spot checks ----
    for _ in range(300):
        k = rng.randint(0, 80)
        z = rng.randint(0, 80)
        n = 2 * k + z
        act = set(R for R in range(1, n + 2) if h(k, z, R) == 2)
        pred = set(p for p in predT(k, z) if p < n + 2)
        out["W2"]["checks"] += 1
        if act != pred:
            out["W2"]["mismatches"] += 1
            if len(out["W2"]["first"]) < 5:
                out["W2"]["first"].append([k, z, sorted(pred), sorted(act)])

    # ---- W3: slice closed forms z in {1,2}, full profile ----
    for z in (1, 2):
        for k in range(0, 61):
            for R in range(0, 2 * k + 3):
                out["W3"]["checks"] += 1
                a = slice_closed_form(k, z, R)
                b = h(k, z, R)
                if a != b:
                    out["W3"]["mismatches"] += 1
                    if len(out["W3"]["first"]) < 5:
                        out["W3"]["first"].append([k, z, R, a, b])

    # ---- W4: tail corollary R >= 2k+z-1 => h = k mod 2 ----
    for k in range(0, 61):
        for z in range(0, 51):
            for R in range(2 * k + z - 1, 2 * k + z + 4):
                if R < 0:
                    continue
                out["W4"]["checks"] += 1
                a = h(k, z, R)
                b = k % 2
                if a != b:
                    out["W4"]["mismatches"] += 1
                    if len(out["W4"]["first"]) < 5:
                        out["W4"]["first"].append([k, z, R, a, b])

    # ---- W5: play length = min(R, 2k+z), random play simulation ----
    for _ in range(400):
        k = rng.randint(0, 30)
        z = rng.randint(0, 30)
        R = rng.randint(0, 60)
        kk, zz, rr = k, z, R
        length = 0
        while rr > 0 and (kk > 0 or zz > 0):
            moves = []
            if kk >= 1:
                moves.append("B")
            if zz >= 1:
                moves.append("C")
            mv = moves[rng.randrange(len(moves))]
            if mv == "B":
                kk -= 1; zz += 1
            else:
                zz -= 1
            rr -= 1
            length += 1
        expect = min(R, 2 * k + z)
        out["W5"]["checks"] += 1
        if length != expect:
            out["W5"]["violations"] += 1

    # ---- W6: unified slice closed form for ALL z >= 1, full profile ----
    for z in range(1, 14):
        for k in range(0, 81):
            for R in range(0, 2 * k + z + 3):
                out["W6"]["checks"] += 1
                a = unified_slice_closed_form(k, z, R)
                b = h(k, z, R)
                if a != b:
                    out["W6"]["mismatches"] += 1
                    if len(out["W6"]["first"]) < 5:
                        out["W6"]["first"].append([k, z, R, a, b])

    print(json.dumps(out, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__":
    main()
