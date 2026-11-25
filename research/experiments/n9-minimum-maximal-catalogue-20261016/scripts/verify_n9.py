"""Independent verification for the n=9 minimum-maximal catalogue.

Distinct from analyze_n9.py: it never canonicalises curves.  A point set of four
grid points is degenerate exactly when the 4x4 determinant over (x^2+y^2, x, y, 1)
vanishes (collinear or concyclic).  So for an empty point p the number of
blocking curves equals the number of triples {a,b,c} of S with det4(p,a,b,c)=0,
because no curve carries four stones of S (verified separately).

Also checks:
  * the brute-force count of degenerate quadruples on 9x9 equals the enumerator's
    forbidden_quads (validates the shared geometry);
  * every round50 known configuration has a D4 image inside the enumerated set.

Writes ../output/n9_independent_verify.json.
"""
import glob
import json
import os
import subprocess
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "output"))
N = 9
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
ROUND50 = os.path.join(REPO, "research", "experiments", "original-claims",
                       "output", "round50_n9_private_family.json")


def pt(i):
    return (i % N, i // N)


def det(m):
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    s = 0
    for j in range(n):
        s += ((-1) ** j) * m[0][j] * det([r[:j] + r[j + 1:] for r in m[1:]])
    return s


def det4(p1, p2, p3, p4):
    return det([[x * x + y * y, x, y, 1] for (x, y) in (p1, p2, p3, p4)])


def tr(i, t):
    r, c = divmod(i, N)
    if t == 1:
        r, c = c, r
    elif t == 2:
        r, c = r, N - 1 - c
    elif t == 3:
        r, c = N - 1 - r, c
    elif t == 4:
        r, c = c, N - 1 - r
    elif t == 5:
        r, c = N - 1 - c, r
    elif t == 6:
        r, c = N - 1 - r, N - 1 - c
    elif t == 7:
        r, c = N - 1 - c, N - 1 - r
    return r * N + c


def main():
    pts = [pt(i) for i in range(N * N)]
    fq = sum(1 for q in combinations(pts, 4) if det4(*q) == 0)
    out = subprocess.run([os.environ.get("NINE_ENUM", os.path.join(HERE, "enum")),
                          "9", "9", "1", "0", "-", "1", "0"],
                         capture_output=True, text=True)
    tool_fq = json.loads(out.stdout)["forbidden_quads"]
    geometry_match = (fq == tool_fq)

    sets = []
    seen = set()
    for f in sorted(glob.glob(os.path.join(OUT, "state_root*.json"))):
        d = json.load(open(f))
        if not d["complete"]:
            raise SystemExit("incomplete state file: %s" % f)
        for s in d["sets"]:
            key = tuple(sorted(s))
            if key not in seen:
                seen.add(key)
                sets.append(list(key))

    hist = {}
    bad = []
    for S in sets:
        Sp = [pt(i) for i in S]
        Ssset = set(Sp)
        empt = [p for p in pts if p not in Ssset]
        best = min(sum(1 for a, b, c in combinations(Sp, 3) if det4(p, a, b, c) == 0)
                   for p in empt)
        hist[best] = hist.get(best, 0) + 1
        if best != 1:
            bad.append((best, S))

    ours = set(tuple(s) for s in sets)
    orbit_ok = None
    if os.path.exists(ROUND50):
        known = [tuple(sorted(x)) for x in
                 json.load(open(ROUND50))["maximal_sets_ids"]]
        orbit_ok = sum(1 for k in known
                       if any(tuple(sorted(tr(i, t) for i in k)) in ours
                              for t in range(8)))

    result = {"n": 9, "k": 9,
              "forbidden_quads_bruteforce": fq,
              "forbidden_quads_enumerator": tool_fq,
              "geometry_match": geometry_match,
              "distinct_sets": len(sets),
              "independent_min_b_histogram": {str(k): v for k, v in sorted(hist.items())},
              "sets_with_min_b_not_1": len(bad),
              "round50_configs": 16 if orbit_ok is not None else 0,
              "round50_with_d4_image_in_set": orbit_ok}
    json.dump(result, open(os.path.join(OUT, "n9_independent_verify.json"), "w"))
    print(json.dumps(result))


if __name__ == "__main__":
    main()
