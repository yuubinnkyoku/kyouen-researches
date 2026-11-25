# gen_cnf.py v2 — CNF for: "exists a maximal safe S-subset with |S| <= k" (decision version, at-most-k)
# on the standard n x n grid (coords 0..n-1), q = 4 (2 lines, 2 circles).
# Encoding (z-free):
#   var x_p for each grid point p (1..n*n).
#   aux t_{C,T} for each curve C (>=4 pts) and each 3-subset T of C: "all 3 points of T are stones",
#     encoded as implications t -> x_t. Auxes are shared across cells. Triples T containing the covered
#     cell c are harmless in cover clauses (they imply x_c, which is false when the clause is decisive).
#   safety: for each curve C and each 4-subset Q of C: clause [-x_q, q in Q].  (quartet-free)
#   cover/maximality: for each cell c: clause [x_c, (t_{C,T}: C through c, T 3-subset of C)].
#   at-most-k: sequential counter with s[i][j] = "first i points contain >= j stones", unit -s[N][k+1].
# Deterministic output. Prints stats + md5.
import sys, hashlib
from census_a import census
from itertools import combinations

def gen(n, k, out_path):
    info, lines, circles = census(n)
    curves = [frozenset(c) for c in list(lines.values()) + list(circles.values())]
    pts = [(x, y) for x in range(n) for y in range(n)]
    idx = {p: i + 1 for i, p in enumerate(pts)}
    nv = n * n
    aux_id = {}
    clauses = []
    for C in curves:
        Cs = sorted(C)
        for T in combinations(Cs, 3):
            aid = nv + 1 + len(aux_id)
            aux_id[(C, T)] = aid
            for t in T:
                clauses.append((-aid, idx[t]))
    nv2 = nv + len(aux_id)
    # safety: quartet-free
    for C in curves:
        for Q in combinations(sorted(C), 4):
            clauses.append(tuple(-idx[q] for q in Q))
    # cover
    through = {p: [] for p in pts}
    for C in curves:
        for p in C:
            through[p].append(C)
    for p in pts:
        lits = [idx[p]]
        for C in through[p]:
            Cs = sorted(C)
            for T in combinations(Cs, 3):
                lits.append(aux_id[(C, T)])
        clauses.append(tuple(lits))
    # at-most-k sequential counter: s[i][j] = ">= j stones among first i pts"
    s = {}
    for i in range(1, len(pts) + 1):
        for j in range(1, k + 2):
            s[(i, j)] = nv2 + 1 + len(s)
    clauses.append((-s[(1,1)], idx[pts[0]]))
    clauses.append((-idx[pts[0]], s[(1,1)]))
    for j in range(2, k + 2):
        clauses.append((-s[(1,j)],))
    for i in range(2, len(pts) + 1):
        x = idx[pts[i-1]]
        for j in range(1, k + 2):
            b = s[(i,j)]
            if j == 1:
                a = s[(i-1,1)]
                clauses.append((-b, a, x))
                clauses.append((-a, b))
                clauses.append((-x, b))
            else:
                a = s[(i-1,j)]
                a2 = s[(i-1,j-1)]
                clauses.append((-b, a, a2))
                clauses.append((-b, a, x))
                clauses.append((-a, b))
                clauses.append((-a2, -x, b))
    clauses.append((-s[(len(pts), k + 1)],))
    nv_total = nv2 + len(s)
    with open(out_path, "w") as f:
        f.write("c kyouen s_n decision n=%d k=%d q=4 gen_cnf.py v2\n" % (n, k))
        f.write("p cnf %d %d\n" % (nv_total, len(clauses)))
        for cl in clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")
    h = hashlib.md5(open(out_path, "rb").read()).hexdigest()
    return h

def gen_fund(n, k, in_path, out_path):
    # adds one clause: some stone lies in the D4 orbit-representative set F.
    # Equisatisfiable with the plain instance: (<=) clause-subset trivially; (=>) any solution S has
    # some stone c, some g in D4 maps c into F, and g(S) satisfies all clauses since safety, cover,
    # and the counter are D4-invariant (rotations/reflections preserve lines, circles, incidences).
    import hashlib as _h
    pts = [(x, y) for x in range(n) for y in range(n)]
    N = n * n
    def orbit(i):
        x, y = pts[i]
        cand = set()
        for (xx, yy) in [(x, y), (y, x), (n - 1 - x, y), (x, n - 1 - y),
                         (n - 1 - x, n - 1 - y), (n - 1 - y, x), (y, n - 1 - x), (n - 1 - y, n - 1 - x)]:
            cand.add((xx, yy))
        return cand
    seen = set()
    F = []
    for i in range(N):
        if i in seen:
            continue
        F.append(i)
        for (xx, yy) in orbit(i):
            seen.add(pts.index((xx, yy)))
    with open(in_path) as f:
        lines = f.read().split("\n")
    for ln_i, ln in enumerate(lines):
        if ln.startswith("p cnf "):
            v, c = map(int, ln.split()[2:4])
            lines[ln_i] = "p cnf %d %d" % (v, c + 1)
            break
    cl = " ".join(str(i + 1) for i in F) + " 0"
    lines.insert(-1, cl)
    txt = "\n".join(lines)
    with open(out_path, "w") as f:
        f.write(txt)
    h = _h.md5(txt.encode()).hexdigest()
    print("n=%d k=%d [+fund |F|=%d]: md5=%s" % (n, k, len(F), h))
    return h

if __name__ == "__main__":
    n, k, path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    gen(n, k, path)
    if len(sys.argv) > 4 and sys.argv[4] == "--fund":
        gen_fund(n, k, path, path + ".fund.cnf")
