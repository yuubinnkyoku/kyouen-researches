#!/usr/bin/env python3
"""Three-token residual game, first family X=(x,1,1), kappa=1.

Closed-form candidate cand_x11(z, x, R) == H(R; (x, 1, 1); z) for the
K0832 residual game (abstract, kappa=1; no claim about the 2D board).

Regions (d = x - z, S = x + 2):
  merge    x <= z-3          : single_token(x+2, z, R)   (K0832 published
                              single-token closed form, transcribed verbatim)
  transient d in [-2, +4]    : 14 parametric row types (z parity x d), see
                              cand_x11 docstring in verify file / report.md
  steady   x >= z+5          : V2 = odds<=z-1 u {z+3}   (z even, z=0: {3})
                               V2 = odds<=z+4           (z odd)
                               V1 = {z+1} u parity band [z+5, x+z+3]
                               tail R>=x+z+4: (x+2) mod 2  (sharp)
  exceptions (z,x) in {(2,1),(1,1),(1,2),(0,1),(0,2),(0,3),(0,4)}:
                              explicit rows; the x=1 rows (0,1),(1,1),(2,1)
                              are exactly the published all-ones slice
                              U0(3,.) / U(3,1,.) / U(3,2,.) (universal
                              theorem, vertical-fiber-all-ones-induction-proof).

Status: observed (fitting). No universal claim.
Deterministic, stdlib only.
"""


def q_odd(k):
    return k if k % 2 else k - 1


def single_token(x, z, R):
    """Published single-token closed form (K0832). Transcribed VERBATIM from
    research/experiments/vertical-fiber-two-token-merge-below-diagonal-20261120/
    verify_merge.py (GitHub blob SHA 5c09857abf56258325d8879430eff028b4c4b4fb).
    """
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))


# Exception rows (z, x) -> (V2 tuple, V1F tuple, tail_R, tail_val).
# Verified against the published all-ones slice U/U0 for the x=1 rows.
_EXC = {
    (2, 1): ((1, 5), (3, 4), 6, 1),
    (1, 1): ((1, 3), (2,), 5, 1),
    (1, 2): ((1, 3, 5), (2,), 6, 0),
    (0, 1): ((), (1,), 4, 1),
    (0, 2): ((3,), (1, 4), 5, 0),
    (0, 3): ((3, 5), (1,), 6, 1),
    (0, 4): ((3, 7), (1, 5), 8, 0),
}


def _odds(lo, hi):
    """Odd integers in [lo, hi] (list)."""
    if lo % 2 == 0:
        lo += 1
    return list(range(lo, hi + 1, 2))


def _band(lo, hi, parity):
    """Integers in [lo, hi] congruent to parity (mod 2) (list)."""
    if lo % 2 != parity:
        lo += 1
    return list(range(lo, hi + 1, 2))


def _ev(z, x, R, V2, V1F, t, tv):
    """Evaluate a row (V2 set, V1F set, tail start t, tail value tv)."""
    if R in V2:
        return 2
    if R in V1F:
        return 1
    if R >= t:
        return tv
    return 0


def _row(z, x):
    """Row descriptor (V2 set, V1F set, t, tv) for cand_x11 at (z, x)."""
    if (z, x) in _EXC:
        V2, V1F, t, tv = _EXC[(z, x)]
        return set(V2), set(V1F), t, tv
    d = x - z
    if d <= -3:
        return None  # merge branch: single_token path, no row sets
    par = z & 1
    if d >= 5:
        # steady
        if par == 0:
            V2 = set(_odds(1, max(z - 1, 0))) | {z + 3}
        else:
            V2 = set(_odds(1, z + 4))
        V1F = {z + 1} | set(_band(z + 5, x + z + 3, (z + 1) & 1))
        t = x + z + 4
        tv = (x + 2) & 1
        return V2, V1F, t, tv
    # transient d in [-2, 4]
    if d == -2:
        if par == 0:
            return set(_odds(1, z + 1)), set(), z + 2, 0
        return set(_odds(1, z)), set(), z + 1, 1
    if d == -1:
        if par == 0:
            return set(_odds(1, max(z - 1, 0))), set(), z + 1, 1
        return set(_odds(1, z)), {z + 1}, z + 2, 0
    if d == 0:
        if par == 0:
            return set(_odds(1, max(z - 1, 0))), {z + 1}, z + 2, 0
        return set(_odds(1, z + 2)), {z + 1}, z + 3, 1
    if d == 1:
        if par == 0:
            return set(_odds(1, max(z - 1, 0))) | {z + 3}, {z + 1}, z + 4, 1
        return set(_odds(1, z + 2)), {z + 1}, z + 3, 0
    if d == 2:
        if par == 0:
            V2 = set(_odds(1, max(z - 1, 0))) | {z + 3} | set(_odds(z + 5, 2 * z + 3))
            return V2, {z + 1}, 2 * z + 4, 0
        V2 = set(_odds(1, 2 * z + 3))
        V1F = {z + 1} | set(_band(z + 5, 2 * z + 3, (z + 1) & 1))
        return V2, V1F, 2 * z + 4, 1
    if d == 3:
        if par == 0:
            V2 = set(_odds(1, max(z - 1, 0))) | {z + 3}
            V1F = {z + 1} | set(_band(z + 5, 2 * z + 3, (z + 1) & 1))
            return V2, V1F, 2 * z + 5, 1
        V2 = set(_odds(1, z + 4))
        V1F = {z + 1} | set(_band(z + 5, 2 * z + 4, (z + 1) & 1))
        return V2, V1F, 2 * z + 5, 0
    if d == 4:
        # x = z + 4; diag pin at 2x-1 = 2z+7 collides with the band top on
        # even z (V2 wins) and sits above the band on odd z.
        if par == 0:
            V2 = set(_odds(1, max(z - 1, 0))) | {z + 3} | {2 * x - 1}
            V1F = {z + 1} | set(_band(z + 5, 2 * z + 5, (z + 1) & 1))
            return V2, V1F, x + z + 4, (x + 2) & 1
        V2 = set(_odds(1, z + 4)) | {2 * x - 1}
        V1F = {z + 1} | set(_band(z + 5, 2 * z + 6, (z + 1) & 1))
        return V2, V1F, x + z + 4, (x + 2) & 1
    raise ValueError((z, x, d))


def cand_x11(z, x, R):
    """Closed-form candidate for H(R; (x,1,1); z), kappa=1 residual game.

    Domains: z >= 0, x >= 1, R >= 0. Status: observed (fit).
    """
    if R == 0:
        return 0
    d = x - z
    if d <= -3:
        # merge below the S=x+2 diagonal: x <= z-3 (z >= 4)
        return single_token(x + 2, z, R)
    V2, V1F, t, tv = _row(z, x)
    if not (V2 & V1F):  # T/P disjointness (structural assert)
        pass
    else:
        raise AssertionError(("T/P overlap", z, x, sorted(V2 & V1F)))
    if R in V2:
        return 2
    if R in V1F:
        return 1
    if R >= t:
        return tv
    return 0
