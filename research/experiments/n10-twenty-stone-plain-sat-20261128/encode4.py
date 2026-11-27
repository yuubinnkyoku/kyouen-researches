#!/usr/bin/env python3
"""Encode the n x n q=4 maximum-safe-set decision as CNF (rev4b).

Cell vars 1..n^2 (cell (x,y) -> 1 + x + n*y). Forbidden quadruple: (-a -b -c -d).

modes (both sound AND complete for '>= k stones selected'):
  seqleast : sequential at-least-k counter, assert s_{k,N}
  selmax   : selector vars u (exactly-one(x,u), u <-> not x) + Sinz
             at-most-(N-k) sequential counter on u
Both were brute-force calibrated on n=4 (max 7) and n=5 (max 9) boards.
"""
import json, sys

class Enc:
    def __init__(self, base):
        self.next = base + 1
        self.clauses = []
    def new(self):
        v = self.next; self.next += 1; return v

def seq_atleast(lits, k, enc):
    n = len(lits)
    s = [[None] * (n + 1) for _ in range(k + 1)]
    for i in range(1, k + 1):
        for j in range(1, n + 1):
            s[i][j] = enc.new()
    enc.clauses.append((-lits[0], s[1][1]))
    for i in range(2, k + 1):
        enc.clauses.append((-s[i][1],))
    for j in range(2, n + 1):
        enc.clauses.append((-lits[j - 1], s[1][j]))
        enc.clauses.append((-s[1][j - 1], s[1][j]))
        for i in range(2, k + 1):
            enc.clauses.append((-s[i - 1][j - 1], -lits[j - 1], s[i][j]))
            enc.clauses.append((-s[i][j - 1], s[i][j]))
    for i in range(1, k + 1):
        for j in range(1, n + 1):
            if j == 1:
                enc.clauses.append((-s[i][1], lits[0]))
            else:
                enc.clauses.append((-s[i][j], lits[j - 1], s[i][j - 1]))
            if i >= 2:
                enc.clauses.append((-s[i][j], s[i - 1][j]))
                if j >= 2:
                    enc.clauses.append((-lits[j - 1], -s[i][j], s[i - 1][j - 1]))
    enc.clauses.append((s[k][n],))

def sinz_atmost(lits, r, enc):
    n = len(lits)
    s = [[None] * (n + 1) for _ in range(r + 1)]
    for i in range(1, r + 1):
        for j in range(1, n + 1):
            s[i][j] = enc.new()
    enc.clauses.append((-lits[0], s[1][1]))
    for i in range(2, r + 1):
        enc.clauses.append((-s[i][1],))
    for j in range(2, n + 1):
        enc.clauses.append((-lits[j - 1], s[1][j]))
        enc.clauses.append((-s[1][j - 1], s[1][j]))
        for i in range(2, r + 1):
            enc.clauses.append((-s[i - 1][j - 1], -lits[j - 1], s[i][j]))
            enc.clauses.append((-s[i][j - 1], s[i][j]))
        enc.clauses.append((-s[r][j - 1], -lits[j - 1]))

def build(n, k, mode, forb):
    N = n * n
    enc = Enc(N)
    for quad in forb:
        a, b, c, d = [x + 1 for x in quad]
        enc.clauses.append((-a, -b, -c, -d))
    if mode == "seqleast":
        seq_atleast(list(range(1, N + 1)), k, enc)
    elif mode == "selmax":
        r = N - k
        u = [enc.new() for _ in range(N)]
        for i in range(N):
            enc.clauses.append((-u[i], -(i + 1)))  # not both
            enc.clauses.append((i + 1, u[i]))      # at least one
        sinz_atmost(u, r, enc)
    else:
        raise SystemExit("unknown mode")
    return enc

def main():
    n = int(sys.argv[1]); k = int(sys.argv[2])
    mode = sys.argv[3] if len(sys.argv) > 3 else "seqleast"
    forbfile = sys.argv[4] if len(sys.argv) > 4 else f"forb_n{n}.json"
    cnffile = sys.argv[5] if len(sys.argv) > 5 else f"n{n}_k{k}_{mode}.cnf"
    forb = json.load(open(forbfile))["forbidden"]
    enc = build(n, k, mode, forb)
    nv = enc.next - 1
    with open(cnffile, "w") as f:
        f.write(f"p cnf {nv} {len(enc.clauses)}\n")
        for c in enc.clauses:
            f.write(" ".join(str(x) for x in c) + " 0\n")
    print(json.dumps({"n": n, "k": k, "mode": mode, "vars": nv,
                      "clauses": len(enc.clauses), "forbidden": len(forb),
                      "cnf": cnffile}))

if __name__ == "__main__":
    main()
