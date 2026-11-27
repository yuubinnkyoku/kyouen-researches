# merge_results.py — combine stage1/stage2/crosscheck outputs into the
# final structure_summary.json.  Standard library only.
# Usage: python -I merge_results.py OUTDIR
import sys, json, os

def main():
    outdir = sys.argv[1]
    s1 = json.load(open(os.path.join(outdir, "stage1_summary.json")))
    parts = [json.load(open(os.path.join(outdir, "grundy_part%d.json" % i))) for i in range(4)]
    xc = json.load(open(os.path.join(outdir, "crosscheck.json")))

    g = {"0": 0, "1": 0, "2": 0}
    for p in parts:
        for k in g:
            g[k] += p["grundy_hist"][k]
    processed = sum(p["processed"] for p in parts)
    fails = {k: sum(p["fails"][k] for p in parts) for k in parts[0]["fails"]}

    # the four contiguous parts partition the nond11 file; part0 extras cover d11+dodecads
    p0 = parts[0]
    summary = {
        "board": "research/experiments/design-kyouen-witt-20261125/output/board_w24.txt",
        "s_param": 7,
        "golay": {
            "span_size": s1["span_size"],
            "weight_hist": {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1},
            "dodecads": s1["dodecads"],
            "verified": s1["pass"]["weights"] and s1["pass"]["dodecads"] and xc["weights_ok"],
        },
        "caps13": {
            "count": s1["caps13_count"],
            "all_terminal": s1["caps13_nonmaximal"] == 0,
            "dodecads_per_cap": {"1": s1["per_cap_dodecad_hist"]["1"]},
            "caps_per_dodecad": {"min": s1["per_dodecad_caps_min"], "max": s1["per_dodecad_caps_max"]},
            "total_incidences": s1["total_incidences"],
            "verified_each_cap_exactly_one_dodecad": s1["pass"]["incidence"],
        },
        "eleven_subsets": {
            "d11_count": s1["d11_count"], "d11_distinct": s1["d11_duplicates"] == 0,
            "d11_per_cap": {"12": s1["d11_per_cap_hist"]["12"]},
            "d11_grundy": p0["d11_grundy_hist"],
            "d11_profile": p0["d11_profile_hist"],
            "d11_all_verified": p0["d11_bad"] == 0,
            "nond11_count": s1["nond11_count"], "nond11_distinct": s1["nond11_duplicates"] == 0,
            "nond11_processed_full": processed == 2040192,
            "nond11_grundy": g,
            "nond11_profile": p0["profile_hist"],
            "nond11_fails": fails,
            "count_identity": {
                "caps_times_66": 30912 * 66,
                "grundy2_size11_total_K1342": 2040192,
                "match": g["2"] == 2040192 and s1["nond11_count"] == 2040192,
            },
            "incidence_identity_dodecad_cap": {
                "sum_caps_per_dodecad": s1["per_dodecad_caps_max"] * s1["dodecads"],
                "caps13_count": s1["caps13_count"],
                "match": s1["per_dodecad_caps_min"] == s1["per_dodecad_caps_max"] == 12
                         and s1["per_dodecad_caps_max"] * s1["dodecads"] == s1["caps13_count"],
            },
            "incidence_identity_d11_cap": {
                "sum_d11_per_cap": 30912 * 12,
                "sum_sup13_per_d11": p0["d11_profile_hist"].get("0,12", 0) * 12,
                "expected_total": 370944,
                "match": s1["d11_per_cap_hist"].get("12", 0) == 30912
                         and p0["d11_profile_hist"].get("0,12", 0) == 30912,
            },
        },
        "dodecads_grundy_s7": {
            "hist": p0["dodecads_grundy_hist"],
            "addable_points_per_dodecad": p0["dodecad_addable_hist"],
            "sup13_per_dodecad": p0["dodecad_sup13_hist"],
            "note": "at s=7 a dodecad has 12 safe children (all terminal 13-caps), so G=mex{0}=1; non-terminal, non-maximal",
        },
        "python_crosscheck": xc,
        "all_pass": bool(s1["pass"]["all"] and xc["all_ok"] and p0["d11_bad"] == 0
                         and p0["dodecads_bad"] == 0 and processed == 2040192
                         and fails["grundy_ne_2"] == 0 and fails["sup13_ne_1"] == 0
                         and fails["sanity"] == 0 and fails["order"] == 0),
    }
    with open(os.path.join(outdir, "structure_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print("all_pass:", summary["all_pass"])

main()
