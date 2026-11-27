#!/usr/bin/env python3
"""Compare the independent layer map against claim K1349 and against the raw
engine outputs of design-kyouen-witt-20261125.

Reads : out/task1_board.json, out/layer_map.txt,
        ../../design-kyouen-witt-20261125/output/grundy_w24_s7.txt,
        ../../design-kyouen-witt-20261125/output/grundy_w24_s7_gsize.txt
Writes: out/claim_check.json, out/claim_check.txt
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
EXP = os.path.abspath(os.path.join(HERE, "..", "..", "design-kyouen-witt-20261125", "output"))

# ------------------------------------------------------------------ claim K1349
CLAIM = {
    "layers": {
        (9, "dodecad"):    {"count": 566720,  "G": 2},
        (9, "nondodecad"): {"count": 728640,  "G": 1},
        (10, "dodecad"):   {"count": 170016,  "G": 1},
        (10, "nondodecad"): {"count": 1700160, "G": 0},
        (11, "dodecad"):   {"count": 30912,   "G": 0},
        (11, "nondodecad"): {"count": 2040192, "G": 2},
    },
    "size12": {"maximal": {"count": 1020096, "G": 0},
               "nonmaximal": {"count": 373520, "G": 1}},
    "size13": {"maximal": {"count": 30912, "G": 0}},
    "profiles": {
        (9, "dodecad"):    (180, 21),
        (9, "nondodecad"): (168, 14),
        (10, "dodecad"):   (36, 12),
        (10, "nondodecad"): (36, 4),
        (11, "dodecad"):   (0, 12),
        (11, "nondodecad"): (6, 1),
    },
    "dodecad_subsets": {9: 566720, 10: 170016, 11: 30912, 12: 2576},
    "weight_enumerator": {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1},
}

checks = []          # (name, ok, detail)


def chk(name, ok, detail=""):
    checks.append({"name": name, "ok": bool(ok), "detail": str(detail)})


def parse_c(path):
    d = {"safe": {}, "gsize": {}, "maximal": {}, "cross": {}, "profile": {},
         "prof_types": {}, "samples": []}
    for line in open(path):
        p = line.split()
        if not p:
            continue
        if p[0] == "SAFE_TOTAL":
            d["total"] = int(p[1])
        elif p[0] == "SAFE":
            d["safe"][int(p[1])] = int(p[2])
        elif p[0] == "SIZE":
            k = int(p[1])
            d["safe"][k] = int(p[2].split("=")[1])
            d["maximal"][k] = int(p[3].split("=")[1])
        elif p[0] == "GSIZE":
            d["gsize"][(int(p[1]), int(p[2]))] = int(p[3])
        elif p[0] == "CROSS":
            k = int(p[1].split("=")[1])
            typ = p[2].split("=")[1]
            g = int(p[3].split("=")[1])
            d["cross"][(k, typ, g)] = int(p[4].split("=")[1])
        elif p[0] == "PROFILE":
            k = int(p[1].split("=")[1])
            typ = p[2].split("=")[1]
            a = int(p[3].split(":")[1])
            b = int(p[4].split(":")[1])
            d["profile"][(k, typ, a, b)] = int(p[5].split("=")[1])
        elif p[0] == "PROFILE_TYPES":
            k = int(p[1].split("=")[1])
            typ = p[2].split("=")[1]
            d["prof_types"][(k, typ)] = int(p[3].split("=")[1])
        elif p[0] == "DODECADSUBSETS":
            d.setdefault("ddsub", {})[int(p[1])] = int(p[2])
        elif p[0] == "SAMPLE":
            d["samples"].append((int(p[1].split("=")[1]), p[2].split("=")[1],
                                 int(p[3].split("=")[1])))
        elif p[0] == "GOLAY":
            d.setdefault("golay", []).append(line.strip())
        elif p[0] == "ROOT":
            d["root"] = int(p[1])
        elif p[0] == "TOTAL_G":
            d["total_g"] = {int(x.split(":")[0]): int(x.split(":")[1]) for x in p[1:]}
        elif p[0] == "DODECAD_CHECK":
            d["dodecad_check"] = line.strip()
        elif p[0] == "SIZE12":
            d["size12"] = {x.split("=")[0]: int(x.split("=")[1]) for x in p[1:]}
        elif p[0] == "MAXLIST":
            d["maxlist"] = (int(p[2]), int(p[4]))
        elif p[0] == "FIVES":
            d["fives"] = line.strip()
        elif p[0] == "UNSAFE_MARKS":
            d["unsafe_marks"] = int(p[1])
    return d


def parse_engine(path):
    d = {"size": {}, "grundy": {}, "gsize": {}}
    for line in open(path):
        p = line.split()
        if not p:
            continue
        if p[0] == "SAFE":
            d["safe"] = int(p[1])
        elif p[0] == "ROOT":
            d["root"] = int(p[1])
        elif p[0] == "SIZE":
            d["size"][int(p[1])] = (int(p[2]), int(p[3]), int(p[4]))
        elif p[0] == "GRUNDY":
            d["grundy"][int(p[1])] = int(p[2])
        elif p[0] == "GSIZE":
            d["gsize"][(int(p[1]), int(p[2]))] = int(p[3])
    return d


def main():
    t1 = json.load(open(os.path.join(OUT, "task1_board.json")))
    c = parse_c(os.path.join(OUT, "layer_map.txt"))

    # ---------------- task 1: board and Golay ----------------
    chk("board is 24 points / 759 blocks of size 8",
        t1["n"] == 24 and t1["blocks"] == 759 and t1["block_size"] == [8],
        f'{t1["n"]} {t1["blocks"]} {t1["block_size"]}')
    chk("S(5,8,24): lambda_0..5 = 759,253,77,21,5,1",
        [t1["lambda"][str(t)][0] for t in range(6)] == [759, 253, 77, 21, 5, 1],
        [t1["lambda"][str(t)][0] for t in range(6)])
    chk("block intersections only 0/2/4",
        sorted(t1["pair_intersections"]) == ["0", "2", "4"],
        t1["pair_intersections"])
    chk("Golay span rank 12, 4096 words", t1["golay_rank"] == 12 and t1["golay_span"] == 4096,
        f'{t1["golay_rank"]}/{t1["golay_span"]}')
    chk("weight enumerator {0:1,8:759,12:2576,16:759,24:1}",
        {int(k): v for k, v in t1["weight_enumerator"].items()}
        == CLAIM["weight_enumerator"], t1["weight_enumerator"])
    chk("weight-8 words are exactly the 759 blocks", t1["weight8_equals_blocks"])
    chk("dodecads = 2576 weight-12 words", t1["dodecads"] == 2576, t1["dodecads"])
    chk("dodecad/octad intersections = {2,4,6}, constant profile 132/495/132",
        t1["dodecad_octad_profiles"]["ok_even_2_4_6"]
        and t1["dodecad_octad_profiles"]["constant"],
        t1["dodecad_octad_profiles"]["profile"])
    for k in (9, 10, 11, 12):
        chk(f"dodecad {k}-subsets distinct = {CLAIM['dodecad_subsets'][k]} "
            f"(injective, no block inside)",
            t1["dodecad_subsets"][str(k)]["distinct"] == CLAIM["dodecad_subsets"][k]
            and t1["dodecad_subsets"][str(k)]["containing_a_block"] == 0,
            t1["dodecad_subsets"][str(k)])

    # ---------------- C total / per-size ----------------
    chk("independent SAFE total = 7,932,035", c.get("total") == 7932035, c.get("total"))
    for k in range(14):
        s = c["safe"].get(k, 0)
        gsum = sum(v for (kk, g), v in c["gsize"].items() if kk == k)
        chk(f"size {k}: Grundy distribution sums to safe count", s == gsum, f"{s} vs {gsum}")

    # ---------------- claim: layer structure ----------------
    for (k, typ), cl in CLAIM["layers"].items():
        cnt = c["cross"].get((k, typ, cl["G"]), 0)
        chk(f"size {k} {typ}: count {cl['count']} at G={cl['G']}", cnt == cl["count"],
            f"got {cnt}")
        # set equality: no other Grundy value occurs in this type
        others = {g: v for (kk, t, g), v in c["cross"].items()
                  if kk == k and t == typ and g != cl["G"] and v}
        chk(f"size {k} {typ}: ALL such caps have G={cl['G']} (no other value)",
            not others, others)
        tot = sum(v for (kk, t, g), v in c["cross"].items() if kk == k and t == typ)
        chk(f"size {k} {typ}: total = claimed count", tot == cl["count"], tot)
        # the two types must partition the safe k-sets
    for k in (9, 10, 11):
        tot = sum(v for (kk, t, g), v in c["cross"].items() if kk == k for _ in [0])
        chk(f"size {k}: dodecad + nondodecad = safe count {c['safe'].get(k)}",
            tot == c["safe"].get(k), tot)
    chk("every dodecad-subset position is safe (flags count 566720+170016+30912+2576)",
        c.get("ddsub", {}).get(9) == 566720 and c.get("ddsub", {}).get(10) == 170016
        and c.get("ddsub", {}).get(11) == 30912 and c.get("ddsub", {}).get(12) == 2576,
        c.get("ddsub"))

    # ---------------- claim: size 12 / 13 ----------------
    chk("size 12 maximal count = 1,020,096",
        c["maximal"].get(12) == CLAIM["size12"]["maximal"]["count"], c["maximal"].get(12))
    chk("size 12: maxima have G=0 and non-maxima G=1",
        c["gsize"].get((12, 0)) == 1020096 and c["gsize"].get((12, 1)) == 373520
        and sum(v for (k, g), v in c["gsize"].items() if k == 12) == 1393616,
        {g: v for (k, g), v in c["gsize"].items() if k == 12})
    chk("size 13 count 30,912, all maximal, all G=0",
        c["safe"].get(13) == 30912 and c["maximal"].get(13) == 30912
        and c["gsize"].get((13, 0)) == 30912,
        (c["safe"].get(13), c["maximal"].get(13)))
    chk("no safe position of size 14", c["safe"].get(14, 0) == 0, c["safe"].get(14))
    chk("maximal positions only at sizes 12 and 13",
        all(c["maximal"].get(k, 0) == 0 for k in range(12))
        and c["maximal"].get(12) == 1020096 and c["maximal"].get(13) == 30912,
        {k: v for k, v in c["maximal"].items() if v})

    # ---------------- claim: profiles, constant per type ----------------
    for (k, typ), (a, b) in CLAIM["profiles"].items():
        pr = {key: v for key, v in c["profile"].items() if key[0] == k and key[1] == typ}
        chk(f"size {k} {typ}: profile (12:{a}, 13:{b}) and constant over all caps",
            pr == {(k, typ, a, b): CLAIM["layers"][(k, typ)]["count"]}
            and c["prof_types"].get((k, typ)) == 1,
            {"distinct": c["prof_types"].get((k, typ)), "profiles": pr})

    # ---------------- totals / cross-check with G=2 claim ----------------
    chk("total Grundy 0/1/2 = 3662291/1662832/2606912",
        c.get("total_g") == {0: 3662291, 1: 1662832, 2: 2606912}, c.get("total_g"))
    chk("G=2 total = dodecad9 + nondodecad11 = 566720+2040192",
        2606912 == 566720 + 2040192, 566720 + 2040192)
    chk("no Grundy value > 2 anywhere",
        all(g <= 2 for (k, g) in c["gsize"]), sorted(set(g for (k, g) in c["gsize"])))
    chk("G(empty) = 0", c.get("root") == 0, c.get("root"))

    # ---------------- structural 12-cap classification ----------------
    s12 = c.get("size12", {})
    chk("non-maximal 12-caps = 2576 dodecads + 370944 non-dodecad; the non-dodecad "
        "non-maxima are exactly the 11-subset-of-dodecad + outside-point family",
        s12.get("nonmax") == 373520 and s12.get("nonmax_dodecad") == 2576
        and s12.get("nonmax_nondodecad") == 370944
        and s12.get("nonmax_nondodecad_with_dodecad11") == 370944
        and s12.get("maximal_with_dodecad11") == 0, s12)
    chk("dodecad check: every dodecad is a non-maximal 12-cap with G=1 and 12 moves; "
        "the 370944 extensions are distinct non-maximal non-dodecad 12-caps",
        "wrong_g=0" in c["dodecad_check"] and "moves_ok=1" in c["dodecad_check"]
        and "pair_bad=0" in c["dodecad_check"]
        and "distinct_extensions=370944" in c["dodecad_check"],
        c["dodecad_check"])

    # ---------------- compare with raw engine output files ----------------
    eng = parse_engine(os.path.join(EXP, "grundy_w24_s7.txt"))
    chk("engine file: SAFE total agrees", eng["safe"] == c["total"], (eng["safe"], c["total"]))
    chk("engine file: ROOT agrees", eng["root"] == c["root"], (eng["root"], c["root"]))
    for k, (cnt, mx, g0) in eng["size"].items():
        ours_cnt = c["safe"].get(k, 0)
        ours_mx = c["maximal"].get(k, 0)
        ours_g0 = c["gsize"].get((k, 0), 0)
        chk(f"engine file SIZE {k} (count,maximal,G0) agrees",
            (cnt, mx, g0) == (ours_cnt, ours_mx, ours_g0),
            f"engine {(cnt, mx, g0)} vs ours {(ours_cnt, ours_mx, ours_g0)}")
    chk("engine file: GRUNDY totals agree",
        eng["grundy"] == {g: c["total_g"][g] for g in sorted(c["total_g"])},
        (eng["grundy"], c["total_g"]))

    gsz_path = os.path.join(EXP, "grundy_w24_s7_gsize.txt")
    if os.path.exists(gsz_path):
        g = {"gsize": {}, "safe": None}
        for line in open(gsz_path):
            p = line.split()
            if not p:
                continue
            if p[0] == "SAFE":
                g["safe"] = int(p[1])
            elif p[0] == "GSIZE":
                g["gsize"][(int(p[1]), int(p[2]))] = int(p[3])
        chk("engine GSIZE file agrees with independent GSIZE",
            g["gsize"] == c["gsize"] and g["safe"] == c["total"],
            {"n_engine": len(g["gsize"]), "n_ours": len(c["gsize"]),
             "diff": {k: (g["gsize"].get(k), c["gsize"].get(k))
                      for k in set(g["gsize"]) | set(c["gsize"])
                      if g["gsize"].get(k) != c["gsize"].get(k)}})

    # ---------------- report ----------------
    npass = sum(1 for x in checks if x["ok"])
    nfail = len(checks) - npass
    lines = []
    for x in checks:
        lines.append(("PASS " if x["ok"] else "FAIL ") + x["name"]
                     + ("" if x["ok"] else f"  [{x['detail']}]"))
    lines.append(f"SUMMARY {npass}/{len(checks)} passed, {nfail} failed")
    txt = "\n".join(lines) + "\n"
    open(os.path.join(OUT, "claim_check.txt"), "w").write(txt)
    json.dump({"checks": checks, "npass": npass, "nfail": nfail},
              open(os.path.join(OUT, "claim_check.json"), "w"), indent=2)
    print(txt)
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
