"""Task 4: independent Grundy values by full upset DP.

For a sampled cap S the Grundy value is recomputed from scratch:

  1. enumerate *all* caps containing S (the upset of S) with a from-scratch
     safety test and a shuffled point order (enumerate_upset_scratch);
  2. run a fresh descending-size mex DP on that upset (grundy_dp);
  3. read off G(S).

This uses neither the cone enumeration nor the cone Grundy table.

Coverage:
  * every cap of the cone of F with size >= 4 (21,352 caps) is re-verified;
  * F itself plus 10 random AGL(2,9) images of it (10 further triangles);
  * for every claimed (size, Grundy) class, 12 random global samples (random
    affine images of cone caps of that class) -- at least 10 per class as
    required, including the rare (5,3) and (6,2) classes;
  * classes with fewer than 10 cone representatives ((3,1):1, (9,0):7) are
    topped up with images.

Run: python task4_upset.py
"""

import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import (  # noqa: E402
    E, ZERO, enc, dec, parse_board, line_masks, is_cap, fadd, fsub, fmul,
    fiszero,
)
from caplib import (  # noqa: E402
    build_point_lines, is_cap_mask, enumerate_upset_scratch, grundy_dp,
)

OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
N = 81
FULL = (1 << N) - 1

CLAIM_NG = {
    3: {1: 77760},
    4: {0: 1108080},
    5: {1: 7861536, 3: 466560},
    6: {0: 12216096, 1: 77760, 2: 13996800},
    7: {0: 2566080, 1: 21228480},
    8: {0: 3353400, 1: 58320},
    9: {0: 6480, 1: 233280},
    10: {0: 23328},
}


def idx_to_pt(i):
    return (dec(i // 9), dec(i % 9))


def pt_to_idx(p):
    return 9 * enc(p[0]) + enc(p[1])


def det2(col1, col2):
    return fsub(fmul(col1[0], col2[1]), fmul(col2[0], col1[1]))


def rand_pt(rng):
    return (E[rng.randrange(9)], E[rng.randrange(9)])


def rand_affine(rng):
    while True:
        col1 = rand_pt(rng)
        if col1 == ZERO:
            continue
        col2 = rand_pt(rng)
        if fiszero(det2(col1, col2)):
            continue
        return (col1, col2, rand_pt(rng))


def apply_affine(mp, mask):
    col1, col2, a = mp
    out = 0
    mm = mask
    while mm:
        b = mm & -mm
        i = b.bit_length() - 1
        x, y = idx_to_pt(i)
        q0 = fadd(a[0], fadd(fmul(x, col1[0]), fmul(y, col2[0])))
        q1 = fadd(a[1], fadd(fmul(x, col1[1]), fmul(y, col2[1])))
        out |= 1 << (9 * enc(q0) + enc(q1))
        mm ^= b
    return out


def main():
    rng = random.Random(424242)
    result = {"classes": {}}

    # ------------------------------------------------------------ parent board
    pn, pnb, p_lines = parse_board(HERE.parent / "output" / "board_ag2q9.txt")
    masks = line_masks(N, p_lines)
    pl = build_point_lines(N, masks)

    cone_dump = json.loads((OUT / "cone_by_class.json").read_text(encoding="utf-8"))
    # cone_dump[size][grundy] = list of masks

    # ------------------------------------------------------------ helpers
    order = list(range(N))

    def grundy_by_upset(cap_mask):
        rng.shuffle(order)
        upset = enumerate_upset_scratch(N, masks, pl, cap_mask, order)
        assert cap_mask in upset
        assert all((m & cap_mask) == cap_mask for m in upset)
        assert all(is_cap_mask(m, masks) for m in upset)   # every member is a cap
        g = grundy_dp(upset, N)
        return g[cap_mask], len(upset)

    # ------------------------------------------- every cone cap of size >= 4
    cone_checked = 0
    cone_mismatch = []
    per_class_cone = {}
    for s in range(4, 11):
        for g_str, cap_list in cone_dump.get(str(s), {}).items():
            g_claim = int(g_str)
            for cm in cap_list:
                gv, usize = grundy_by_upset(cm)
                cone_checked += 1
                per_class_cone.setdefault((s, g_claim), [0, 0])
                per_class_cone[(s, g_claim)][0] += 1
                if gv == g_claim:
                    per_class_cone[(s, g_claim)][1] += 1
                else:
                    cone_mismatch.append({"size": s, "claim": g_claim, "got": gv,
                                          "mask": cm, "upset": usize,
                                          "points": sorted(i for i in range(N) if (cm >> i) & 1)})
    result["cone_caps_reverified"] = cone_checked
    result["cone_mismatches"] = cone_mismatch

    # ------------------------------------------------------ F and 10 triangles
    F = (1 << 0) | (1 << 9) | (1 << 1)
    tri_samples = []
    gv, usize = grundy_by_upset(F)
    tri_samples.append({"what": "F", "mask": F, "got": gv, "upset": usize})
    for t in range(10):
        mp = rand_affine(rng)
        img = apply_affine(mp, F)
        gv, usize = grundy_by_upset(img)
        tri_samples.append({"what": "image%d" % t, "mask": img, "got": gv,
                            "upset": usize})
    result["triangle_samples"] = tri_samples
    result["triangle_all_G1"] = all(x["got"] == 1 for x in tri_samples)
    result["triangle_upse_size_uniform"] = len({x["upset"] for x in tri_samples}) == 1

    # ------------------------------- global samples for every claimed class
    # 12 random affine images of cone caps of the class (top-up for rare classes)
    class_rep = {}
    for s in sorted(CLAIM_NG):
        for g in sorted(CLAIM_NG[s]):
            cone_list = cone_dump.get(str(s), {}).get(str(g), [])
            assert cone_list, "class (%d,%d) missing from the cone dump" % (s, g)
            samples = []
            want = 12
            for t in range(want):
                src = cone_list[rng.randrange(len(cone_list))]
                mp = rand_affine(rng)
                img = apply_affine(mp, src)
                samples.append({"src": src, "mask": img, "map": mp})
            ok = 0
            got_list = []
            for smp in samples:
                assert is_cap_mask(smp["mask"], masks)
                gv, usize = grundy_by_upset(smp["mask"])
                smp["got"] = gv
                smp["upset"] = usize
                got_list.append(gv)
                if gv == g:
                    ok += 1
            # class-level totals: cone representatives (already verified above
            # for s >= 4) plus the global images
            cone_verified = per_class_cone.get((s, g), [0, 0])[1]
            class_rep["%d:%d" % (s, g)] = {
                "claim": CLAIM_NG[s][g],
                "cone_representatives_verified": cone_verified,
                "global_images_verified": ok,
                "global_images_total": want,
                "required_10_ok": cone_verified + ok >= 10,
                "global_values": got_list,
            }
    result["classes"] = class_rep
    result["all_global_images_match"] = all(
        v["global_images_verified"] == v["global_images_total"] for v in class_rep.values()
    )
    result["all_classes_have_10_samples"] = all(
        v["required_10_ok"] for v in class_rep.values()
    )

    result["all_task4_checks_ok"] = all(
        [
            not cone_mismatch,
            result["triangle_all_G1"],
            result["triangle_upse_size_uniform"],
            result["all_global_images_match"],
            result["all_classes_have_10_samples"],
        ]
    )

    (OUT / "task4_upset.json").write_text(json.dumps(result, indent=1), encoding="utf-8")

    # ----------------------------------------------------------------- report
    print("=" * 78)
    print("TASK 4  independent Grundy values by full upset DP")
    print("=" * 78)
    print("cone caps of size >= 4 re-verified :", cone_checked)
    print("mismatches                         :", len(cone_mismatch))
    print("triangle samples (F + 10 images)   :", len(tri_samples),
          "all G=1:", result["triangle_all_G1"])
    print("triangle upset sizes               :", sorted({x['upset'] for x in tri_samples}))
    print()
    print("class      claim   cone-reps  images  ok  samples>=10")
    for key in sorted(class_rep, key=lambda k: (int(k.split(':')[0]), int(k.split(':')[1]))):
        v = class_rep[key]
        print("%-8s %10d %9d %7d %5d  %s" % (
            key, v["claim"], v["cone_representatives_verified"],
            v["global_images_verified"], v["global_images_total"],
            v["required_10_ok"]))
    print()
    print("all global images match            :", result["all_global_images_match"])
    print("all classes have >= 10 samples     :", result["all_classes_have_10_samples"])
    print("all task-4 checks                  :", result["all_task4_checks_ok"])
    print("wrote", OUT / "task4_upset.json")
    return result


if __name__ == "__main__":
    r = main()
    raise SystemExit(0 if r["all_task4_checks_ok"] else 1)
