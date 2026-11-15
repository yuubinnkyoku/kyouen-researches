#!/usr/bin/env python3
"""N x N square board, standard q=4 kyouen game — SAT encoding for K0141.

Forbidden quadruple = 4 distinct cells collinear OR concyclic (standard call
rule) = zero of the 4x4 integer determinant
  | x^2+y^2  x  y  1 |
per K0057's exclusive decomposition. Pure integer arithmetic.

"at least k selected" uses a biconditional (definitional) sequential
counter: s(i,j) <=> (count of x_1..x_i) >= j, for 1<=i<=n, 1<=j<=k:
    s(i,j) <-> s(i-1,j) OR (x_i AND s(i-1,j-1)),  s(i,0)=T, s(0,j)=F (j>=1)
encoded with forward+backward clauses, so prefix-count semantics are an
exact model-theoretic consequence (both directions present).

Controls (all must pass before any solver run):
  (C1) forbidden-quadruple count == K0057's F_10 = 54441 (independent encoder).
  (C2) known 19-stone witness (K0035) contains 0 forbidden quadruples.
  (C3) ge19 CNF: direct evaluation of ALL clauses under the assignment
       (x = witness, s = prefix-count) gives 0 violations.
  (C4) ge20 CNF: same assignment MUST violate the counter (at least one
       clause) — witnesses with <k stones are genuinely excluded.
"""
import json
from itertools import combinations

N = 10
NUM = N * N


def forbidden_quadruples(n):
    pts = [(x, y) for y in range(n) for x in range(n)]
    norms = [x * x + y * y for (x, y) in pts]
    quads = []
    for combo in combinations(range(len(pts)), 4):
        i, j, k, l = combo
        xi, yi = pts[i]
        xj, yj = pts[j]
        xk, yk = pts[k]
        xl, yl = pts[l]
        m = [
            [norms[i] - norms[l], xi - xl, yi - yl],
            [norms[j] - norms[l], xj - xl, yj - yl],
            [norms[k] - norms[l], xk - xl, yk - yl],
        ]
        det = (
            m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        )
        if det == 0:
            quads.append(combo)
    return quads


def build(n, k):
    """Variables: 1..n = x_i (cell i-1). Counter s(i,j) = n + (i-1)*k + j."""

    def s(i, j):
        return n + (i - 1) * k + j

    clauses = []
    for j in range(1, k + 1):
        if j == 1:
            clauses.append([-1, s(1, 1)])          # x_1 -> s(1,1)
            clauses.append([-s(1, 1), 1])           # s(1,1) -> x_1
        else:
            clauses.append([-s(1, j)])             # s(1,j>=2) = false
    for i in range(2, n + 1):
        for j in range(1, k + 1):
            # forward
            clauses.append([-s(i - 1, j), s(i, j)])
            if j == 1:
                clauses.append([-i, s(i, 1)])
            else:
                clauses.append([-i, -s(i - 1, j - 1), s(i, j)])
            # backward
            clauses.append([-s(i, j), s(i - 1, j), i])
            if j >= 2:
                clauses.append([-s(i, j), s(i - 1, j), s(i - 1, j - 1)])
    clauses.append([s(n, k)])
    return n + n * k, clauses, s


def evaluate(clauses, xlit, k_cur):
    """Direct evaluation. xlit: dict cell-index(0-based) -> bool for x vars;
    counter vars take prefix-count semantics: s(i,j) = (#x among first i) >= j.
    Returns violation count."""
    viol = 0
    sl = {}

    def sval(i, j):
        if (i, j) not in sl:
            cnt = sum(1 for t in range(1, i + 1) if xlit.get(t - 1))
            sl[(i, j)] = cnt >= j
        return sl[(i, j)]

    def lit(v):
        neg = v < 0
        a = abs(v)
        if a <= NUM:
            val = xlit.get(a - 1, False)
        else:
            j = (a - NUM - 1) % k_cur + 1
            i = (a - NUM - 1) // k_cur + 1
            val = sval(i, j)
        return (not val) if neg else val

    for cl in clauses:
        if not any(lit(v) for v in cl):
            viol += 1
    return viol


def write_cnf(path, nvars, clauses):
    with open(path, "w") as f:
        f.write("p cnf %d %d\n" % (nvars, len(clauses)))
        for cl in clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")


if __name__ == "__main__":
    quads = forbidden_quadruples(N)
    print("C1: forbidden quadruples on %dx%d: %d (K0057 F_10=54441) %s"
          % (N, N, len(quads), "MATCH" if len(quads) == 54441 else "MISMATCH"))
    wit = [9, 15, 16, 18, 20, 22, 30, 36, 44, 58, 62, 65, 67, 70, 71, 87, 91, 93, 97]
    witset = set(wit)
    bad = sum(1 for q in quads if all(i in witset for i in q))
    print("C2: witness-internal forbidden quads: %d (expect 0) | C(19,4)=%d"
          % (bad, 3876))
    quad_clauses = [[-(q[0] + 1), -(q[1] + 1), -(q[2] + 1), -(q[3] + 1)] for q in quads]
    report = {"n": N, "F10": len(quads), "witness_quads": bad}
    for k, name in [(19, "ge19"), (20, "ge20")]:
        nvars, cnt_clauses, sfn = build(NUM, k)
        clauses = cnt_clauses + quad_clauses
        write_cnf("n10_%s.cnf" % name, nvars, clauses)
        xlit = {w: True for w in wit}
        viol = evaluate(clauses, xlit, k)
        print("%s: vars=%d clauses=%d | direct-eval violations on 19-witness: %s (expect %s)"
              % (name, nvars, len(clauses), viol, 0 if k == 19 else "at least 1"))
        report[name] = {"vars": nvars, "clauses": len(clauses), "witness_violations": viol}
    with open("encode_report.json", "w") as f:
        json.dump(report, f, indent=1)
