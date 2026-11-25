"""Probe/artefact case study: decode the parent's stored cap masks and classify them.

Finding (details in REPORT.md, section "Discrepancy"):
  * output/starts6.txt, output/probes6.txt and output/starts.txt store caps as
    "<tag> <high-word> <low-64-bit mask>"; the board points 64..72 live in the
    high word (bit 0 <-> point 64).  Decoding that way reproduces exactly the
    two given start caps, and makes all four 6-cap probes maximal 6-caps.
  * Membership in the three 6-cap orbits computed here:
        cap0 -> orbit C,  cap1 -> orbit B,  cap2 -> orbit C,  cap3 -> orbit B
    whereas output/orbits_maximal.txt records "cap0 in, cap1 out, cap2 in,
    cap3 out" relative to the orbit of {10,47,49,55,61,64} (orbit A).
    The in/out pattern matches orbit C, not orbit A; i.e. the recorded
    reference orbit appears mislabelled.  The claim itself (3 orbits of
    686,784) is unaffected and independently confirmed.

Also re-derives the hyperoval orbit with an independent frozenset BFS and
verifies permute_mask() against set images.
"""
import random

import pg8core as G

BOARD = "../output/board_pg2q8.txt"
HYPEROVAL = [0, 5, 13, 18, 27, 38, 46, 53, 59, 66]
CAP6 = [10, 47, 49, 55, 61, 64]
REPS = {
    "A(start)": CAP6,
    "B": [7, 10, 41, 43, 59, 61],
    "C": [0, 1, 18, 31, 33, 43],
}
PROBES = {
    "cap0": [8, 48, 50, 51, 58, 61],
    "cap1": [17, 27, 30, 44, 52, 70],
    "cap2": [15, 22, 27, 43, 53, 55],
    "cap3": [4, 8, 40, 44, 47, 56],
}


def build_gens():
    gens = []
    for i in range(3):
        for j in range(3):
            if i != j:
                for c in (1, 2):
                    gens.append(G.perm_from_matrix(G.transvection(i, j, c)))
    gens.append(G.perm_from_matrix(G.diagonal(2, 1, 1)))
    gens.append(G.perm_from_matrix(G.coord_swap()))
    return gens


def main():
    n, b, lines = G.read_board(BOARD)
    geo = G.Geometry(n, lines)
    gens = build_gens()
    pbits = [[1 << p[i] for i in range(73)] for p in gens]

    # 1. permute_mask vs set images
    rng = random.Random(7)
    bad = 0
    for _ in range(2000):
        k = rng.choice([3, 6, 10, 20])
        m = G.mask_of(sorted(rng.sample(range(73), k)))
        pi = rng.randrange(len(gens))
        want = G.mask_of(sorted(gens[pi][p] for p in G.set_of(m)))
        if want != G.permute_mask(pbits[pi], m):
            bad += 1
    print("permute_mask vs set-image mismatches: %d / 2000" % bad)

    # 2. frozenset BFS (no bitmasks) reproduces both orbit sizes
    for name, S, expect in (("hyperoval", HYPEROVAL, 32704), ("6-cap start", CAP6, 686784)):
        seen = {frozenset(S)}
        stack = [frozenset(S)]
        while stack:
            cur = stack.pop()
            for g in gens:
                T = frozenset(g[p] for p in cur)
                if T not in seen:
                    seen.add(T)
                    stack.append(T)
        ok = len(seen) == expect
        print("frozenset BFS %-12s size %7d (expect %6d) %s"
              % (name, len(seen), expect, "OK" if ok else "MISMATCH"))
        if name.startswith("6-cap"):
            masks = {G.mask_of(sorted(T)) for T in seen}
            same = masks == G.orbit_of_mask(G.mask_of(CAP6), gens, pbits)
            print("   mask sets equal to bitmask BFS: %s" % same)

    # 3. orbit reps / membership
    orbits = {}
    for k, S in REPS.items():
        orbits[k] = G.orbit_of_mask(G.mask_of(S), gens, pbits)
        print("orbit %-8s rep %-28s size %d" % (k, S, len(orbits[k])))
    print()
    for name, S in PROBES.items():
        m = G.mask_of(S)
        where = [k for k, O in orbits.items() if m in O]
        print("%-5s %-28s cap=%s maximal=%s -> orbit %s"
              % (name, S, geo.is_cap(S), len(geo.addable(S)) == 0, where))
    print()
    print("recorded in output/orbits_maximal.txt: "
              "\"probes vs orbit of {10,47,49,55,61,64}: cap0 in, cap1 out, cap2 in, cap3 out\"")
    print("observed  relative to orbit A: cap0 out, cap1 out, cap2 out, cap3 out")
    print("observed  relative to orbit C: cap0 in,  cap1 out, cap2 in,  cap3 out  <-- same pattern")


if __name__ == "__main__":
    main()
