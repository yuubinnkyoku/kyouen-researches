"""Verifies the SAT witness of the exactly-9 CNF: the 9 chosen vertices of
the binary 6-cube must be in affine general position (all C(9,7)=36
seven-subsets nonsingular), which is exactly what the CNF encodes together
with its exactly-9 counter.  This is the positive control for the UNSAT
side: the same circuit clauses that make 10 points impossible leave a
9-point solution, and the found solution matches the geometric definition.
"""
import sys

# witness vertices extracted from the kissat assignment (x vars 1..64, 1-based)
WITNESS = [11, 22, 28, 37, 42, 49, 57, 58, 63]  # 0-based cube vertices
D = 6


def det_bareiss(a):
    a = [row[:] for row in a]
    n = len(a)
    prev, sign = 1, 1
    for k in range(n - 1):
        piv = next((i for i in range(k, n) if a[i][k]), None)
        if piv is None:
            return 0
        if piv != k:
            a[k], a[piv] = a[piv], a[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[k][k] * a[i][j] - a[i][k] * a[k][j]) // prev
            a[i][k] = 0
        prev = a[k][k]
    return sign * a[-1][-1]


def main():
    pts = WITNESS
    assert len(set(pts)) == 9
    assert all(0 <= p < (1 << D) for p in pts)
    from itertools import combinations
    dets = []
    for sub in combinations(pts, 7):
        m = [[1] + [(p >> i) & 1 for i in range(D)] for p in sub]
        dets.append(det_bareiss(m))
    assert all(v != 0 for v in dets), dets
    print(f"witness {sorted(pts)}: all {len(dets)} seven-subsets nonsingular, "
          f"|det| range [{min(abs(v) for v in dets)}, "
          f"{max(abs(v) for v in dets)}] -- 9-point SAT witness VERIFIED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
