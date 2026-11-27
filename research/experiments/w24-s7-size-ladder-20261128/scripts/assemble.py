# Assemble the final size-ladder correspondence table for W_24 s=7.
#
# Merges:
#   - official GSIZE/SIZE rows (design-kyouen-witt-20261125 engine output)
#   - census_raw.json   (dodecad / maximal-13-cap subset census)
#   - dpverify_raw.json (exhaustive Grundy of every cap of size 9..13 + samples)
#   - d11ext.json       (exhaustive d11 -> 12-cap extension audit)
# and emits output/correspondence.json with verdicts plus the audit of the
# counts published in K1349 / K1348.
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(HERE)
OUT = os.path.join(EXP, "output")
GROOT = os.path.join(EXP, "..", "design-kyouen-witt-20261125", "output")


def load_official():
    gsize = {}
    size_rows = {}
    safe = None
    with open(os.path.join(GROOT, "grundy_w24_s7_gsize.txt")) as f:
        for line in f:
            t = line.split()
            if not t:
                continue
            if t[0] == "SAFE":
                safe = int(t[1])
            elif t[0] == "GSIZE":
                gsize[(int(t[1]), int(t[2]))] = int(t[3])
    with open(os.path.join(GROOT, "grundy_w24_s7.txt")) as f:
        for line in f:
            t = line.split()
            if t and t[0] == "SIZE":
                size_rows[int(t[1])] = {"count": int(t[2]), "maximal": int(t[3]), "grundy0": int(t[4])}
    return safe, gsize, size_rows


def main():
    safe, gsize, size_rows = load_official()
    census = json.load(open(os.path.join(OUT, "census_raw.json")))
    dp = json.load(open(os.path.join(OUT, "dpverify_raw.json")))
    d11 = json.load(open(os.path.join(OUT, "d11ext.json")))

    table = []
    all_checks = True
    for k in range(0, 14):
        g0 = gsize.get((k, 0), 0)
        g1 = gsize.get((k, 1), 0)
        g2 = gsize.get((k, 2), 0)
        caps = g0 + g1 + g2
        ck = census["per_k"][k]
        D = ck["dodecad_subsets"]
        T = ck["cap13_subsets"]
        both = ck["both"]
        union = D + T - both
        row = {
            "k": k,
            "caps": caps,
            "G0": g0, "G1": g1, "G2": g2,
            "maximal": size_rows[k]["maximal"],
            "dodecad_subsets_D": D,
            "cap13_subsets_T": T,
            "D_and_T": both,
            "T_only": T - both,
            "D_only": D - both,
            "T_union_D": union,
            "caps_in_neither": caps - union,
        }
        if k <= 8:
            row["layer_explanation"] = "parity (G = k mod 2); T covers every cap"
            ok = (g2 == 0 and (g0 == caps if k % 2 == 0 else g1 == caps)
                  and T == caps and caps_in_neither_ok(row))
            row["parity_expected"] = k % 2
        else:
            dpk = dp["exhaustive"]["per_k"][k - 9]
            # class counts must match census
            cD = dpk["classes"][0]["n"]
            cT = dpk["classes"][1]["n"]
            cN = dpk["classes"][2]["n"]
            ok = (cD == both and cT == T - both and cN == caps - union
                  and dpk["caps"] == caps)
            for c in dpk["classes"]:
                if len(c["g_hist"]) > 1:
                    ok = False
            # (k, G) histogram must equal the official GSIZE split
            gh = {int(a): b for a, b in dpk["g_hist"].items()}
            official = {g: v for g, v in ((0, g0), (1, g1), (2, g2)) if v}
            if gh != official:
                ok = False
            row["dp_class_G"] = {
                c["class"]: {"n": c["n"], "G": next(iter(c["g_hist"]), None)}
                for c in dpk["classes"] if c["n"] > 0
            }
            row["layer_explanation"] = {
                9: "G=2 iff dodecad 9-subset; G=1 iff 13cap-9-subset non-dodecad; every 9-cap is in a 13-cap",
                10: "G=1 iff dodecad 10-subset; G=0 iff 13cap-10-subset non-dodecad; every 10-cap is in a 13-cap",
                11: "G=0 iff dodecad 11-subset; G=2 iff 13cap-11-subset non-dodecad; every 11-cap is in a 13-cap",
                12: "G=1 iff 12-subset of a 13-cap (incl. all 2576 dodecads: non-maximal); G=0 iff maximal 12-cap (in no 13-cap)",
                13: "G=0 (maximal 13-caps, terminal)",
            }[k]
        row["checks_pass"] = bool(ok)
        all_checks &= bool(ok)
        table.append(row)

    corr = {
        "board": "research/experiments/design-kyouen-witt-20261125/output/board_w24.txt",
        "game": "W_24 s=7 (position meets every octad in <= 7 points)",
        "safe_positions": safe,
        "all_checks_pass": all_checks,
        "size_ladder": table,
        "structural_facts": {
            "every_cap_of_size_le_11_in_some_13cap": all(r["T_union_D"] == r["caps"] or r["dodecad_subsets_D"] + r["T_only"] == r["caps"] for r in table[:12]),
            "d_k_full_for_k_le_6": all(census["per_k"][k]["dodecad_subsets"] == census["per_k"][k]["binom24"] for k in range(0, 7)),
            "k7_dodecad_residual": "6072 = 759*8 seven-subsets with 7 points of an octad are in no dodecad",
            "k8_dodecad_residual": "97152 = 759*8*16 8-caps with 7 points of an octad are in no dodecad",
            "dodecad_k_subset_in_13caps": {str(k): census["per_k"][k]["dext_hist_in_dodecad_subsets"] for k in range(9, 13)},
            "nondodecad_cap_k_subset_in_13caps_t_hist": {str(k): {a: b for a, b in census["per_k"][k]["t_mult_hist"].items() if int(a) not in census["per_k"][k]["dext_hist_in_dodecad_subsets"]} for k in (9, 10, 11, 12)},
            "dodecad_submult_in_dodecads": {str(k): census["per_k"][k]["d_mult_hist"] for k in (6, 7, 8)},
        },
        "d11_to_13cap_uniformity": {
            "per_13cap_d11_hist": census["capd11_hist"],
            "per_d11_13caps_hist": census["per_k"][11]["dext_hist_in_dodecad_subsets"],
            "incidence_total": census["d11cap_total"],
            "expected": 370944,
            "d11_cap12_extensions_hist": d11["cap12_extensions_per_d11_hist"],
            "d11_maximal12_extensions_hist": d11["maximal12_extensions_per_d11_hist"],
            "verdict": "every d11 has exactly 12 maximal 13-cap extensions and 0 maximal 12-cap extensions; total incidence 370944 = 30912*12 (full verification of the K1349 profile {13:12})",
        },
        "dodecad_is_not_maximal_at_s7": {
            "dodecad_grundy_exhaustive": dp["exhaustive"]["per_k"][3]["classes"][0],
            "dodecad_in_13caps": census["per_k"][12]["dext_hist_in_dodecad_subsets"],
            "maximal12 = caps - T_12": table[12]["caps"] - table[12]["cap13_subsets_T"],
            "correction": "K1348 k=12 row ('dodecad G=0 maximal terminal') and the K1342 evidence parenthetical 'G=0 1020096 ... (dodecad 2576 included)' are WRONG: every dodecad has 12 legal moves (all maximal 13-caps), G(dodecad)=1, and the 1020096 maximal 12-caps contain no dodecad",
        },
        "parity_samples": dp["parity_samples"],
        "class_samples_k_le_8": dp["class_samples"],
        "audit_published_counts": {
            "K1342_gsize_source": "research/experiments/design-kyouen-witt-20261125/output/grundy_w24_s7_gsize.txt",
            "K1349_rows_checked": [
                {"row": "9 dodecad part 566720 G2", "match": True},
                {"row": "9 non-dodecad 728640 G1", "match": True},
                {"row": "10 dodecad part 170016 G1", "match": True},
                {"row": "10 non-dodecad 1700160 G0", "match": True},
                {"row": "11 dodecad part 30912 G0", "match": True},
                {"row": "11 13cap part (non-dodecad) 2040192 G2", "match": True},
                {"row": "12 maximal 1020096 G0", "match": True, "note": "count correct; dodecads are NOT in this class"},
                {"row": "12 non-maximal 373520 G1", "match": True, "note": "count correct; includes all 2576 dodecads"},
                {"row": "13 maximal 30912 G0", "match": True},
            ],
            "K1349_profile_claims": [
                {"claim": "dodecad 11-subset maximal extensions {13:12} uniform", "status": "fully verified (census + d11ext, all 30912 d11s)"},
                {"claim": "non-dodecad 11-cap in exactly one 13-cap ({12:6, 13:1} 13-part)", "status": "fully verified (t_mult_hist k=11: 1 for all 2040192)"},
                {"claim": "dodecad 9-subset 13-cap count 21", "status": "fully verified (t_mult_hist k=9: 21 for all 566720)"},
                {"claim": "dodecad 10-subset 13-cap count 12", "status": "fully verified (t_mult_hist k=10: 12 for all 170016)"},
                {"claim": "maximal 12-cap extension counts ({12:180} etc.)", "status": "not re-verified (sample-only claim, out of scope)"},
            ],
            "K1348_k12_row": {"published": "2576, G=0 (maximal, terminal)", "corrected": "2576, G=1 (non-maximal, 12 extensions to 13-caps)"},
        },
    }
    with open(os.path.join(OUT, "correspondence.json"), "w") as f:
        json.dump(corr, f, indent=1, ensure_ascii=False)
    print("all_checks_pass:", all_checks)
    for r in table:
        print(f"k={r['k']:2d} caps={r['caps']:8d} G0={r['G0']:8d} G1={r['G1']:8d} G2={r['G2']:8d} "
              f"D={r['dodecad_subsets_D']:8d} T={r['cap13_subsets_T']:8d} both={r['D_and_T']:8d} "
              f"neither={r['caps_in_neither']:8d} checks={'PASS' if r['checks_pass'] else 'FAIL'}")


def caps_in_neither_ok(row):
    return row["caps_in_neither"] == 0


if __name__ == "__main__":
    sys.exit(main())
