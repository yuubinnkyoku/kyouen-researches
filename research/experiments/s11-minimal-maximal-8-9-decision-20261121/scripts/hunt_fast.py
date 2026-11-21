# hunt_fast.py — fast local witness hunt for <=9-stone maximal safe configs near the K0320
# 10-stone witness (remove-2 add-1 net, plus remove-1). Uses census_a curves as bitmasks
# (System A, calibrated against published F_n) for bulk coverage checks; only shortlisted
# candidates get the full independent geometry verify (verify_geom, System C).
import sys, json, time
from itertools import combinations
from census_a import census
from verify_geom import verify

def run(n, W, out):
    t0 = time.time()
    info, lines, circles = census(n)
    curves = [frozenset(c) for c in list(lines.values()) + list(circles.values())]
    pts = [(x, y) for x in range(n) for y in range(n)]
    N = n * n
    idx = {p: i for i, p in enumerate(pts)}
    Cmask = [sum(1 << idx[p] for p in C) for C in curves]
    full = (1 << N) - 1
    S = [tuple(p) for p in W]
    smask = sum(1 << idx[p] for p in S)
    # sanity: witness itself must be safe+maximal
    assert verify(n, S, verbose=False), "base witness invalid"
    # precompute per-curve stone counts for S; covered by active curves
    def covered_of(mask):
        cov = mask
        for cm in Cmask:
            if (cm & mask).bit_count() >= 3:
                cov |= cm
        return cov
    results = {"n": n, "base": W, "checked": 0, "shortlists": 0, "walls": {}, "hits": [], "elapsed": 0}
    covS = covered_of(smask)
    assert covS == full
    # active curves involving each stone (for analysis)
    cells = pts
    # rescue map: for each cell u, list of (b) such that b on a curve with >=2 stones of mask8 and u on it
    def rescue(b, mask8, u):
        # is b on a curve with >=2 stones of mask8 that contains u?
        ui = idx[u]
        bi = idx[b]
        for C, cm in zip(curves, Cmask):
            if ui in C and bi in C and (cm & mask8).bit_count() >= 2:
                return True
        return False
    hits = []
    # net 1: remove 1 (9 stones as-is)
    for i in range(len(S)):
        m9 = smask ^ (1 << idx[S[i]])
        if covered_of(m9) == full:
            st = sorted(pts[t] for t in range(N) if (m9 >> t) & 1)
            if verify(n, st, verbose=False):
                results["hits"].append(["rm1", i, st])
    # net 2: remove 2, add 1
    tried = 0
    sl = 0
    for i, j in combinations(range(len(S)), 2):
        removed = [S[i], S[j]]
        m8 = smask ^ (1 << idx[S[i]]) ^ (1 << idx[S[j]])
        st8m = m8
        cov8 = covered_of(m8)
        U = [pts[t] for t in range(N) if not (cov8 >> t) & 1]
        if not U:
            st = sorted(pts[t] for t in range(N) if (m8 >> t) & 1)
            # 8-stone maximal directly!
            if verify(n, st, verbose=False):
                results["hits"].append(["rm2", i, j, st])
        # candidate b must rescue every u in U: quick filter via rescue precomputation
        # build candidate set: cells that lie on a curve with >=2 stones of m8 (potential activators)
        cand = set()
        for C, cm in zip(curves, Cmask):
            k = (cm & m8).bit_count()
            if k >= 2:
                for p in C:
                    if not (m8 >> idx[p]) & 1:
                        cand.add(p)
        for b in cand:
            tried += 1
            ok = True
            for u in U:
                if not rescue(b, m8, u):
                    ok = False
                    break
            if not ok:
                continue
            sl += 1
            st = sorted(pts[t] for t in range(N) if ((m8 | (1 << idx[b])) >> t) & 1)
            if verify(n, st, verbose=False):
                results["hits"].append(["rm2add1", i, j, b, st])
    results["checked"] = tried
    results["shortlists"] = sl
    results["elapsed"] = time.time() - t0
    with open(out, "w") as f:
        json.dump(results, f, indent=1, default=list)
    print(json.dumps({k: v for k, v in results.items() if k != "base"}, default=str))
    return results

if __name__ == "__main__":
    n = int(sys.argv[1])
    W = json.loads(sys.argv[2])
    out = sys.argv[3]
    run(n, W, out)
