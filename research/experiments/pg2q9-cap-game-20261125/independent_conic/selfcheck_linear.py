"""Self-check of the linear-algebra / projectivity machinery used everywhere.

200 random determinants against a permutation expansion, 200 random inverses,
300 random projectivity round-trips through the four-point frame
reconstruction, and the field axioms."""
import itertools
import json
import random

import gf9 as F
import pg9 as P

OUT = "results_selfcheck.json"


def det_brute(M):
    total = 0
    for perm in itertools.permutations(range(3)):
        inv = sum(1 for i in range(3) for j in range(i + 1, 3)
                  if perm[i] > perm[j])
        term = 1
        for i in range(3):
            term = F.MUL[term][M[i][perm[i]]]
        total = F.ADD[total][term] if inv % 2 == 0 else F.sub(total, term)
    return total


def main():
    rnd = random.Random(11)
    res = {}
    ok_field, notes = F.field_checks()
    res["field_axioms"] = {"ok": ok_field, "notes": notes}

    bad_det = 0
    for _ in range(200):
        A = tuple(tuple(rnd.randrange(9) for _ in range(3)) for _ in range(3))
        if P.mat_det(A) != det_brute(A):
            bad_det += 1
    res["determinants"] = {"checked": 200, "mismatches": bad_det}

    bad_inv = 0
    n_inv = 0
    I = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    while n_inv < 200:
        A = tuple(tuple(rnd.randrange(9) for _ in range(3)) for _ in range(3))
        if P.mat_det(A) == 0:
            continue
        n_inv += 1
        Ai = P.mat_inv(A)
        if P.mat_mul(Ai, A) != I or P.mat_mul(A, Ai) != I:
            bad_inv += 1
    res["inverses"] = {"checked": n_inv, "mismatches": bad_inv}

    # projectivity round trip: random V, random frame, images, reconstruction
    bad_rt = 0
    n_rt = 0
    while n_rt < 300:
        while True:
            V = tuple(tuple(rnd.randrange(9) for _ in range(3)) for _ in range(3))
            if P.mat_det(V) != 0:
                break
        src = rnd.sample(range(91), 4)
        frame = True
        for a in range(4):
            for b in range(a + 1, 4):
                for c in range(b + 1, 4):
                    if (P.PAIR_LINE[src[a]][src[b]] >> src[c]) & 1:
                        frame = False
        if not frame:
            continue
        n_rt += 1
        pts = [P.POINTS[i] for i in src]
        dst = [F.normalise(P.mat_vec(V, p)) for p in pts]
        M = P.projectivity_from_frame(pts, dst)
        if M is None:
            bad_rt += 1
            continue
        for i in range(91):
            a = F.normalise(P.mat_vec(M, P.POINTS[i]))
            b = F.normalise(P.mat_vec(V, P.POINTS[i]))
            if a != b:
                bad_rt += 1
                break
    res["projectivity_round_trip"] = {"checked": n_rt, "mismatches": bad_rt}

    res["pass"] = (ok_field and bad_det == 0 and bad_inv == 0 and bad_rt == 0)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))
    print("\nSELF-CHECK:", "PASS" if res["pass"] else "FAIL")


main()
