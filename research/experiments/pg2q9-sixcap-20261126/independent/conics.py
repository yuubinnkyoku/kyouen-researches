"""Independent conic enumeration in PG(2,9) over GF(9) coordinates.

Builds the standard PG(2,9) from GF(9)=GF(3)[i]/(i^2+1) (no board file is used),
enumerates all non-degenerate conics (zero sets of non-degenerate homogeneous
quadratics, canonicalised up to GF(9)^*), and checks:

  * number of non-degenerate conics = 9^5 - 9^2 = 58,968,
  * every conic is a 10-cap and is maximal (no addable point),
  * all conic point sets are distinct,
  * all 10*58,968 = 589,680 conic 9-subsets are distinct (each is a 9-cap; on a
    sample the addable set is exactly the missing conic point),
  * all 45*58,968 = 2,653,560 conic 8-subsets are distinct (each is an 8-cap;
    on a sample the addable set is exactly the two missing conic points).

These numbers independently pin the 8/9/10-cap layer used in the Grundy chain:
G(10)=0 (all 10-caps maximal), G(9)=1 (no maximal 9-cap, all children are
10-caps), G(8)=0 (all children of a non-maximal 8-cap are 9-caps of G=1).
"""
import itertools
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boardlib

GA = boardlib.GF_ADD
GM = boardlib.GF_MUL
GS = boardlib.GF_SUB
GINV = boardlib.GF_INV

EXPECT_CONICS = 9 ** 5 - 9 ** 2          # 58,968
EXPECT_9SUBSETS = 10 * EXPECT_CONICS      # 589,680
EXPECT_8SUBSETS = 45 * EXPECT_CONICS      # 2,653,560


def det3(m):
    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    ei_fh = GS[GM[e][i]][GM[f][h]]
    di_fg = GS[GM[d][i]][GM[f][g]]
    dh_eg = GS[GM[d][h]][GM[e][g]]
    # det = a*(ei-fh) - b*(di-fg) + c*(dh-eg)
    return GA[GS[GM[a][ei_fh]][GM[b][di_fg]]][GM[c][dh_eg]]


def main():
    t0 = time.time()
    std = boardlib.build_std_pg29()
    lines = [sorted(ln) for ln in std.lines]
    plane = boardlib.Plane(91, lines)
    ax = plane.validate_plane()
    print("standard-model board axioms:", ax)
    assert ax["n_points"] == 91 and ax["n_lines"] == 91 and ax["line_sizes"] == [10]
    lm = plane.lmask
    ld = plane.lid
    full = plane.full

    pts = std.points
    mono = []
    for (x, y, z) in pts:
        mono.append((GM[x][x], GM[y][y], GM[z][z], GM[x][y], GM[x][z], GM[y][z]))

    # canonical nonzero symmetric coefficient 6-tuples up to GF(9)^*
    canon = set()
    for coeff in itertools.product(range(9), repeat=6):
        if not any(coeff):
            continue
        first = next(c for c in coeff if c)
        inv = GINV[first]
        canon.add(tuple(GM[inv][c] for c in coeff))
    print("canonical nonzero symmetric 6-tuples:", len(canon))

    conics = []
    degenerate = 0
    bad_size = bad_cap = bad_max = 0
    for coeff in canon:
        a, b, c, d, e, f = coeff
        half = 2  # inverse of 2 in GF(9)
        m = [[a, GM[d][half], GM[e][half]],
             [GM[d][half], b, GM[f][half]],
             [GM[e][half], GM[f][half], c]]
        if det3(m) == 0:
            degenerate += 1
            continue
        mask = 0
        for i, (x2, y2, z2, xy, xz, yz) in enumerate(mono):
            q = 0
            q = GA[q][GM[a][x2]]
            q = GA[q][GM[b][y2]]
            q = GA[q][GM[c][z2]]
            q = GA[q][GM[d][xy]]
            q = GA[q][GM[e][xz]]
            q = GA[q][GM[f][yz]]
            if q == 0:
                mask |= 1 << i
        if mask.bit_count() != 10:
            bad_size += 1
            continue
        if not plane.is_cap(mask):
            bad_cap += 1
            continue
        if plane.addable(mask) != 0:
            bad_max += 1
            continue
        conics.append(mask)
    print("non-degenerate conics: %d (expected %d)" % (len(conics), EXPECT_CONICS))
    print("degenerate forms: %d; bad size/cap/maximal: %d/%d/%d"
          % (degenerate, bad_size, bad_cap, bad_max))
    print("distinct conic point sets: %d" % len(set(conics)))
    print("time (conics) %.1fs" % (time.time() - t0))

    def addable_from_idx(idx):
        blocked = 0
        for ii in range(len(idx)):
            a = idx[ii]
            la = ld[a]
            for jj in range(ii + 1, len(idx)):
                blocked |= lm[la[idx[jj]]]
        return full & ~blocked

    # ---- 9-subsets: distinctness (all) + addable sample -----------------
    nine = set()
    for C in conics:
        idx = [i for i in range(91) if (C >> i) & 1]
        for k in range(10):
            nine.add(C & ~(1 << idx[k]))
    print("\nconic 9-subsets: %d (expected %d) %s"
          % (len(nine), EXPECT_9SUBSETS,
             "PASS" if len(nine) == EXPECT_9SUBSETS else "FAIL"))

    sample = conics[:: max(1, len(conics) // 300)][:300]
    nine_bad = 0
    n9 = 0
    for C in sample:
        idx = [i for i in range(91) if (C >> i) & 1]
        for k in range(10):
            S = [idx[t] for t in range(10) if t != k]
            add = addable_from_idx(S)
            n9 += 1
            if add != (1 << idx[k]):
                nine_bad += 1
    print("  9-subset addable-set==missing sample: %d checked, bad %d" % (n9, nine_bad))

    # ---- 8-subsets: distinctness (all) + addable sample -----------------
    eight = set()
    for C in conics:
        idx = [i for i in range(91) if (C >> i) & 1]
        for k1, k2 in itertools.combinations(range(10), 2):
            eight.add(C & ~(1 << idx[k1]) & ~(1 << idx[k2]))
    print("conic 8-subsets: %d (expected %d) %s"
          % (len(eight), EXPECT_8SUBSETS,
             "PASS" if len(eight) == EXPECT_8SUBSETS else "FAIL"))

    eight_bad = 0
    n8 = 0
    for C in sample:
        idx = [i for i in range(91) if (C >> i) & 1]
        for k1, k2 in itertools.combinations(range(10), 2):
            S = [idx[t] for t in range(10) if t != k1 and t != k2]
            add = addable_from_idx(S)
            n8 += 1
            if add != ((1 << idx[k1]) | (1 << idx[k2])):
                eight_bad += 1
    print("  8-subset addable-set==missing-pair sample: %d checked, bad %d" % (n8, eight_bad))

    print("\nSummary:")
    ok1 = len(conics) == EXPECT_CONICS and bad_max == 0 and len(set(conics)) == EXPECT_CONICS
    ok2 = len(nine) == EXPECT_9SUBSETS and nine_bad == 0
    ok3 = len(eight) == EXPECT_8SUBSETS and eight_bad == 0
    print("  nondegenerate conics are 10-caps and maximal, all distinct: %s"
          % ("PASS" if ok1 else "FAIL"))
    print("  conic 9-subsets distinct (%d) and each has 1 addable point: %s"
          % (len(nine), "PASS" if ok2 else "FAIL"))
    print("  conic 8-subsets distinct (%d) and each has 2 addable points: %s"
          % (len(eight), "PASS" if ok3 else "FAIL"))
    print("  cross-check with census: 10-caps %d, 9-caps %d, non-max 8-caps %d"
          % (len(conics), len(nine), len(eight)))
    print("  total time %.1fs" % (time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
