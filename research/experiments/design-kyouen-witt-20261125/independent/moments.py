"""Exact moment (counting) feasibility tests.

For a candidate set S of size s in a design whose blocks are all of size k and
with |S cap B| <= smax for every block B, put

    x_j = #{blocks B : |S cap B| = j},   j = 0..smax.

If the board is a t-design with uniform lambda_r (r = 0..t, lambda_0 = 1,
lambda_1 = replication number r), then for r = 0..min(t, smax)

    sum_j C(j, r) x_j = lambda_r * C(s, r).

(Each r-subset of S lies in exactly lambda_r blocks, and each block containing
j points of S contains C(j, r) of those r-subsets.)  These identities are
necessary; if the linear system has no nonnegative integer solution, no such S
exists.  This is an independent counting argument, not the report's
K_s <= (s-2)lambda_2/lambda_3 + 2 bound.

Additionally, if the board is a 5-design (lambda_5 = 1) then a t=5 row is
included: for smax <= 4 its left side is 0 while the right side is C(s, 5),
so s >= 5 is impossible ("every 5-subset lies in a block").
"""
from fractions import Fraction

from common import binomial


def _solve_square(A, rhs):
    """Solve A x = rhs exactly with Fractions.  Returns list or None."""
    m = len(A)
    n = len(A[0]) if m else 0
    if m != n:
        raise ValueError("not square")
    M = [[Fraction(A[i][j]) for j in range(n)] + [Fraction(rhs[i])]
         for i in range(m)]
    for col in range(n):
        piv = None
        for r in range(col, m):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            return None  # singular
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(m):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    if any(M[i][n] != 0 and all(M[i][j] == 0 for j in range(n)) for i in range(m)):
        return None
    return [M[i][n] for i in range(n)]


def moment_solutions(v, blocks, smax, s, lam, design_t):
    """Return (status, solutions) where status in {'feasible','infeasible'}.

    lam maps r -> uniform lambda_r (r >= 2); r = 0 and r = 1 (b, replication)
    are computed from the boards.
    """
    b = len(blocks)
    per_point = [0] * v
    for B in blocks:
        for p in B:
            per_point[p] += 1
    assert len(set(per_point)) == 1, per_point
    r1 = per_point[0]
    lam_full = {0: b, 1: r1}
    for r in range(2, design_t + 1):
        lam_full[r] = lam[r]

    n = smax + 1
    rows = []
    rhs = []
    for t in range(0, design_t + 1):
        coeff = [binomial(j, t) for j in range(n)]
        val = lam_full[t] * binomial(s, t)
        rows.append(coeff)
        rhs.append(val)
    # drop all-zero rows
    keep_r, keep_b = [], []
    for row, val in zip(rows, rhs):
        if all(c == 0 for c in row):
            if val != 0:
                return "infeasible", []
        else:
            keep_r.append(row)
            keep_b.append(val)
    rows, rhs = keep_r, keep_b
    m = len(rows)

    sols = []
    if m == n:
        sol = _solve_square(rows, rhs)
        if sol is not None and all(x.denominator == 1 and x >= 0 for x in sol):
            sols.append([int(x) for x in sol])
    elif m == n - 1:
        # one free variable: x_{n-1} = t
        cols = n - 1
        A = [[rows[i][j] for j in range(cols)] for i in range(m)]
        for t in range(b + 1):
            rhs_t = [rhs[i] - t * rows[i][n - 1] for i in range(m)]
            sol = _solve_square(A, rhs_t)
            if sol is None:
                continue
            if any(x.denominator != 1 or x < 0 for x in sol):
                continue
            cand = [int(x) for x in sol] + [t]
            if sum(cand) == b and all(c >= 0 for c in cand):
                sols.append(cand)
    else:
        raise ValueError("unexpected system size m=%d n=%d" % (m, n))
    return ("feasible" if sols else "infeasible"), sols


def system_summary(solutions):
    if not solutions:
        return None
    return {("x%d" % j): solutions[0][j] for j in range(len(solutions[0]))}
