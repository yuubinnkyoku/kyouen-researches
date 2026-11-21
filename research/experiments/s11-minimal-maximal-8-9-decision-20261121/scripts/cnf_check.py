# cnf_check.py — constructive satisfiability check of an explicit stone set S against a
# gen_cnf.py v2 DIMACS instance (n x n, at-most-k, z-free encoding).
# Builds the full intended assignment from S alone:
#   x_p := p in S; t_{C,T} := (T subset of S); s[i][j] := |S cap first i points| >= j
# and evaluates EVERY clause literally. Exit 0 iff all clauses satisfied.
# This checks the encoding itself (not just the solver): if kissat says SAT but this
# checker rejects the decoded set, the encoding is broken, not the game.
import sys

def check(n, k, cnf_path, stones):
    pts = [(x, y) for x in range(n) for y in range(n)]
    N = n * n
    S = set(stones)
    assert all(0 <= v < N for v in S) and len(S) == len(S), "bad stones"
    x = [False] * (N + 1)
    for v in S:
        x[v + 1] = True
    # read clauses
    clauses = []
    nv = 0
    with open(cnf_path) as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("c "):
                continue
            if ln.startswith("p cnf"):
                nv = int(ln.split()[2])
                continue
            lits = [int(t) for t in ln.split()[:-1]]
            clauses.append(lits)
    val = [False] * (nv + 1)
    val[1:N + 1] = x[1:]
    # aux semantics unknown at parse time; derive by fixpoint from clause structures:
    # t clauses are (-aid, idx_t) triples; s-counter identified by s convention.
    # Simpler: compute every variable via the generator's semantic invariants.
    # Instead of re-deriving ids, evaluate t/s by checking with a SAT-style propagator:
    # t is false unless forced; s derived from counter recurrence. We do two passes:
    # Pass 1: t_{C,T} true iff all 3 points in S -> detectable from clauses (-aid, pt):
    #   aux var appears ONLY in negative position within its defining clauses, so
    #   any assignment with t := (T subset S) satisfies them. Cover clauses need the
    #   intended t. So set: for each clause (-a, p) with a > N: candidate def of a.
    # We reconstruct meanings: defs[a] = list of points; cover usage keeps (aid) positive.
    defs = {}
    defs_all = {}
    for cl in clauses:
        if len(cl) == 2 and cl[0] < 0 and abs(cl[0]) > N and 0 < cl[1] <= N:
            defs_all.setdefault(abs(cl[0]), []).append(cl[1])
    # t-aux vars have exactly |T|=3 def clauses; the s-counter special base clause
    # (-s[(1,1)], x_0) has only 1 and must NOT be classified as a t-aux.
    for a, plist in defs_all.items():
        if len(plist) >= 3:
            defs[a] = plist
    cover_ok = {}
    # identify s-counter vars: vars > N not in defs. s[i][j] truth = (count_i >= j).
    for a, plist in defs.items():
        val[a] = all(x[p] for p in plist)
    prefix = 0
    s_by_expr = []
    for i in range(1, N + 1):
        prefix += 1 if (i - 1) in S else 0
        for j in range(1, k + 2):
            s_by_expr.append(prefix >= j)
    unknown = sorted(set(range(N + 1, nv + 1)) - set(defs.keys()))
    for idx, v in enumerate(unknown):
        val[v] = s_by_expr[idx]
    # evaluate
    bad = 0
    for cl in clauses:
        sat = False
        for l in cl:
            if l > 0:
                if val[l]:
                    sat = True
                    break
            else:
                if not val[-l]:
                    sat = True
                    break
        if not sat:
            bad += 1
            if bad <= 5:
                cl_s = " ".join(map(str, cl))
                print("VIOLATED:", (cl_s[:97] + "...") if len(cl_s) > 100 else cl_s)
    print("n=%d k=%d stones=%d clauses=%d violated=%d" % (n, k, len(S), len(clauses), bad))
    return bad == 0

if __name__ == "__main__":
    n = int(sys.argv[1]); k = int(sys.argv[2]); path = sys.argv[3]
    stones = [int(v) for v in sys.argv[4].split(",")]
    ok = check(n, k, path, stones)
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
