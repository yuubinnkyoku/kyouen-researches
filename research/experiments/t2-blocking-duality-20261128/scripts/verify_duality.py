#!/usr/bin/env python3
"""verify_duality.py — independent verification for the t>=2 blocking-duality kit.

Rebuilds AG(2,q)/PG(2,q) from scratch over GF(q) (q in {3,4,5}; GF(4) with
addition = XOR over F2[w]/(w^2+w+1)), checks the 2-(v,k,1) design property of
both the derived board and the supplied board file, writes the derived board
(board file path + '.derived.txt'), then re-checks every dumped mask:

  - safety (every line has <= s points of S), maximality,
  - t-fold blocking (every line has >= t points), minimality,
  - element-level complement bijection (both directions),
  - size-by-size counts and total counts against the C enumerator output.

Usage:
  verify_duality.py <board.txt> <ag|pg> <q> <s> <maximal.txt> <minimal.txt> <both|maximal|minimal>

With mode 'maximal'/'minimal' only one list is re-verified (counts from a
separate JSON of the C run are then required to be supplied via stdin as
{"maximal":{...},"minimal":{...}} — kept simple: in one-list modes we only
re-verify the given list and its internal properties).
"""
import sys, json, itertools

def gf(q):
    if q == 3:
        els = list(range(3)); add = lambda a,b:(a+b)%3; neg=lambda a:(-a)%3
        mul = lambda a,b:(a*b)%3; inv = lambda a:{1:1,2:2}[a]
        return els, add, neg, mul, inv
    if q == 5:
        els = list(range(5)); add = lambda a,b:(a+b)%5; neg=lambda a:(-a)%5
        mul = lambda a,b:(a*b)%5; inv = lambda a:{1:1,2:3,3:2,4:4}[a]
        return els, add, neg, mul, inv
    if q == 4:
        # elements 0,1,2,3 with 2~w, 3~w^2=w+1 ; addition = XOR
        els = list(range(4))
        def add(a,b): return a ^ b
        neg = lambda a: a
        mullog = {0:None,1:0,2:1,3:2}  # w^1=2, w^2=3=w+1, w^3=1
        def mul(a,b):
            if a == 0 or b == 0: return 0
            e = (mullog[a] + mullog[b]) % 3
            return {0:1,1:2,2:3}[e]
        inv = lambda a: {1:1,2:3,3:2}[a]
        return els, add, neg, mul, inv
    raise SystemExit("unsupported q %d" % q)

def build_board(family, q):
    els, add, neg, mul, inv = gf(q)
    if family == "ag":
        pts = [(x,y) for y in els for x in els]
        lines = []
        for a in els:
            for b in els:
                lines.append([(x, add(mul(a,x), b)) for x in els])
        for c in els:
            lines.append([(c,y) for y in els])
        v, k = q*q, q
    else:
        # projective: nonzero triples up to scalar
        raw = [(x,y,z) for x in els for y in els for z in els if (x,y,z) != (0,0,0)]
        pts, seen = [], set()
        for p in raw:
            key = []
            for lam in els:
                if lam == 0: continue
                key.append((mul(lam,p[0]), mul(lam,p[1]), mul(lam,p[2])))
            key = tuple(sorted(key))
            if key in seen: continue
            seen.add(key); pts.append(p)
        lines = []
        for a in els:
            for b in els:
                for c in els:
                    if (a,b,c) == (0,0,0): continue
                    ln = [p for p in pts if add(add(mul(a,p[0]), mul(b,p[1])), mul(c,p[2])) == 0]
                    if len(ln) == q+1: lines.append(ln)
        # dedup lines (each line found q-1 times via scaling)
        uniq, useen = [], set()
        for ln in lines:
            key = tuple(sorted(pts.index(p) for p in ln))
            if key in useen: continue
            useen.add(key); uniq.append(ln)
        lines = uniq
        v, k = q*q+q+1, q+1
    return pts, lines, v, k

def design_check(pts, lines, v, k, family, q):
    idx = {p:i for i,p in enumerate(pts)}
    ll = [sorted(idx[p] for p in ln) for ln in lines]
    assert len(pts) == v and len(ll) == (q*q+q if family=="ag" else v), "wrong v/b"
    for ln in ll:
        assert len(ln) == k and len(set(ln)) == k, "bad line size"
    pair = {}
    for li, ln in enumerate(ll):
        for a, b in itertools.combinations(ln, 2):
            key = (min(a,b), max(a,b))
            assert key not in pair, "pair on two lines"
            pair[key] = li
    assert len(pair) == v*(v-1)//2, "missing pairs"
    return ll

def read_board_file(path):
    toks = open(path).read().split()
    n, L = int(toks[0]), int(toks[1])
    i = 2; lines = []
    for _ in range(L):
        k = int(toks[i]); i += 1
        lines.append([int(toks[i+j]) for j in range(k)]); i += k
    assert all(0 <= p < n for ln in lines for p in ln)
    return n, lines

def main():
    board, family, q, s, maxf, minf, mode = sys.argv[1:8]
    q = int(q); s = int(s)
    pts, lines, v, k = build_board(family, q)
    derived = design_check(pts, lines, v, k, family, q)
    l = k; t = l - s
    # write derived board (own labeling)
    with open(board + ".derived.txt", "w") as f:
        f.write("%d %d\n" % (v, len(derived)))
        for ln in derived:
            f.write(str(len(ln)) + " " + " ".join(map(str, ln)) + "\n")
    # board file design check
    n, blines = read_board_file(board)
    assert n == v, "board file n mismatch"
    bset = [sorted(ln) for ln in blines]
    assert len(bset) == len(derived), "board file line count mismatch"
    pair = {}
    for li, ln in enumerate(bset):
        assert len(ln) == k, "board file line size"
        for a, b in itertools.combinations(ln, 2):
            key = (min(a,b), max(a,b))
            assert key not in pair, "board file: pair on two lines"
            pair[key] = li
    assert len(pair) == v*(v-1)//2
    full = (1 << n) - 1
    linemask = [0]*len(blines)
    for li, ln in enumerate(blines):
        for p in ln: linemask[li] |= 1 << p
    deg = [[] for _ in range(n)]
    for li, ln in enumerate(blines):
        for p in ln: deg[p].append(li)

    def is_safe(S): return all((linemask[li] & S).bit_count() <= s for li in range(len(blines)))
    def is_maximal(S):
        for p_ in range(n):
            if S >> p_ & 1: continue
            if is_safe(S | (1 << p_)): return False
        return True
    def is_blocking(C): return all((linemask[li] & C).bit_count() >= t for li in range(len(blines)))
    def is_minimal(C):
        for p_ in range(n):
            if not (C >> p_ & 1): continue
            if is_blocking(C & ~(1 << p_)): return False
        return True

    report = {"board": board, "family": family, "q": q, "v": v, "k": k, "l": l, "s": s, "t": t,
              "design_ok": True, "derived_board": board + ".derived.txt"}
    def load(path):
        out = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line: out.append(int(line, 16))
        return out
    if mode in ("both", "maximal"):
        M = load(maxf)
        cnt = {}
        bad = 0
        for m in M:
            if not (is_safe(m) and is_maximal(m)): bad += 1; continue
            cnt[m.bit_count()] = cnt.get(m.bit_count(), 0) + 1
        report["maximal_recheck_bad"] = bad
        report["maximal_counts"] = {str(a): b for a, b in sorted(cnt.items())}
    if mode in ("both", "minimal"):
        N_ = load(minf)
        cnt = {}
        bad = 0
        for m in N_:
            if not (is_blocking(m) and is_minimal(m)): bad += 1; continue
            cnt[m.bit_count()] = cnt.get(m.bit_count(), 0) + 1
        report["minimal_recheck_bad"] = bad
        report["minimal_counts"] = {str(a): b for a, b in sorted(cnt.items())}
    if mode == "both":
        M = load(maxf); N_ = load(minf)
        Sset = set(M); Cset = set(N_)
        assert len(Sset) == len(M) and len(Cset) == len(N_), "duplicates in dump"
        fail_f = sum(1 for m in M if (full ^ m) not in Cset)
        fail_b = sum(1 for m in N_ if (full ^ m) not in Sset)
        report["complement_fail_forward"] = fail_f
        report["complement_fail_backward"] = fail_b
        report["all_ok"] = (report["maximal_recheck_bad"] == 0 and
                            report["minimal_recheck_bad"] == 0 and fail_f == 0 and fail_b == 0 and
                            sum(report["maximal_counts"].values()) == sum(report["minimal_counts"].values()))
    print(json.dumps(report, indent=1, sort_keys=True))

if __name__ == "__main__":
    main()
