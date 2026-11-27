"""Compare the independent recomputation with the K1358 claim and its sources.

For cone computations the positions of size < t are not in any cone.  They are
recovered from the mex chain: for m = t-1 the children are the t-sets, whose
Grundy values are the (uniform) values of the t-subset orbits; for m < t-1 the
children all have one value.  Counts are C(n,m) for these sizes.
"""
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kyouen_lib as K
import sources as S

ROOT = HERE.parent.parent  # research/experiments
OUT = HERE / "out"


def load_result(name):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def intkeys(d):
    return {int(k): int(v) for k, v in d.items()}


def nonzero(d):
    return {int(k): int(v) for k, v in d.items() if int(v) > 0}


def parity_name(sizes):
    ps = {m % 2 for m in sizes}
    if ps == {0}:
        return "even-uniform"
    if ps == {1}:
        return "odd-uniform"
    return "mixed"


def mex(vals):
    v = 0
    while v in vals:
        v += 1
    return v


def per_size_from_cones(res):
    cones = res["cones"]
    t = res["t"]
    Nts = res["orbit_Nt"]
    if len(cones) == 1:
        inf, issues = K.inflate(cones[0]["T_g"], Nts[0], t)
    else:
        inf, issues = K.inflate_multi([c["T_g"] for c in cones], Nts, t)
    return {int(m): {int(g): int(v) for g, v in ctr.items()}
            for m, ctr in inf.items()}, issues


def completed_from_cone(res):
    """Full size/grundy/per-size tables for a cone computation."""
    n = res["n"]
    t = res["t"]
    per_large, issues = per_size_from_cones(res)
    orbit_g = sorted({c["root_grundy"] for c in res["cones"]})
    per = {m: dict(ctr) for m, ctr in per_large.items()}
    # mex chain for sizes 0..t-1
    g_at = {}
    for m in range(t - 1, -1, -1):
        if m == t - 1:
            g_at[m] = mex(orbit_g)
        else:
            g_at[m] = 0 if g_at[m + 1] != 0 else 1
        per[m] = {g_at[m]: math.comb(n, m)}
    sizes = {m: sum(ctr.values()) for m, ctr in per.items()}
    gd = Counter()
    for ctr in per.values():
        for g, v in ctr.items():
            gd[g] += v
    maximal = nonzero(res["inflated_maximal_by_size"])
    return {m: per[m] for m in sorted(per)}, {m: sizes[m] for m in sorted(sizes)}, \
        dict(sorted(gd.items())), maximal, issues, g_at


def txt_per_size(txt):
    per = defaultdict(dict)
    for (m, g), v in txt["GSIZE"].items():
        per[int(m)][int(g)] = int(v)
    return dict(per)


def sum_dicts(dicts):
    out = Counter()
    for d in dicts:
        for g, c in d.items():
            out[int(g)] += int(c)
    return dict(out)


ROWS = [
    dict(i=1, board="PG(2,9)", s=2, claim_sizes=[6, 7, 8, 10],
         claim_parity="mixed", claim_max_g=2, result="cone_PG2q9_s2.json"),
    dict(i=2, board="AG(2,5)", s=2, claim_sizes=[5, 6],
         claim_parity="mixed", claim_max_g=2, result="full_AG2q5_s2.json"),
    dict(i=3, board="AG(2,7)", s=2, claim_sizes=[6, 7, 8],
         claim_parity="mixed", claim_max_g=2, result="cone_AG2q7_s2.json"),
    dict(i=4, board="AG(2,9)", s=2, claim_sizes=[6, 7, 8, 9, 10],
         claim_parity="mixed", claim_max_g=3, result="cone_AG2q9_s2.json"),
    dict(i=5, board="PG(2,3)", s=3, claim_sizes=[7, 9],
         claim_parity="odd-uniform", claim_max_g=1,
         result="full_PG2q3_s3.json", cone_result="cone_PG2q3_s3.json"),
    dict(i=6, board="PG(2,4)", s=3, claim_sizes=[7, 9],
         claim_parity="odd-uniform", claim_max_g=1,
         result="full_PG2q4_s3.json", cone_result="cone_PG2q4_s3.json"),
    dict(i=7, board="AG(2,4)", s=3, claim_sizes=[8, 9],
         claim_parity="mixed", claim_max_g=2, result="full_AG2q4_s3.json"),
    dict(i=8, board="AG(2,5)", s=3, claim_sizes=[9, 10, 11],
         claim_parity="mixed", claim_max_g=4, result="full_AG2q5_s3.json"),
    dict(i=9, board="PG(2,5)", s=3, claim_sizes=[9, 10, 11],
         claim_parity="mixed", claim_max_g=4, result="cone_PG2q5_s3.json"),
    dict(i=10, board="PG(2,4)", s=4, claim_sizes=[12, 13, 14, 16],
         claim_parity="mixed", claim_max_g=3, result="full_PG2q4_s4.json"),
    dict(i=11, board="W_22", s=5, claim_sizes=[11, 12, 15],
         claim_parity="mixed", claim_max_g=3,
         result="full_W22_s5.json", cone_result="cone_W22_s5.json"),
    dict(i=12, board="W_24", s=5, claim_sizes=[6],
         claim_parity="even-uniform", claim_max_g=1,
         result="full_W24_s5.json", cone_result="cone_W24_s5.json"),
    dict(i=13, board="W_24", s=6, claim_sizes=[12],
         claim_parity="even-uniform", claim_max_g=1,
         result="full_W24_s6.json", cone_result="cone_W24_s6.json"),
    dict(i=14, board="W_24", s=7, claim_sizes=[12, 13],
         claim_parity="mixed", claim_max_g=2,
         result="cone_W24_s7.json"),
]


def main():
    gg = S.parse_grundy_general(
        ROOT / "s-parameter-kyouen-20261125/output/grundy_general.json")
    census = S.parse_census_pg2q9(
        ROOT / "pg2q9-cap-game-20261125/output/census_pg2q9.txt")
    sp_ag29 = S.parse_spectrum(
        ROOT / "ag2q9-cap-game-20261128/output/ag2q9_spectrum.json")
    sp_pg23 = S.parse_spectrum(
        ROOT / "pg2q3-s3-20261128/output/pg2q3_s3_spectrum.json")
    sp_pg24 = S.parse_spectrum(
        ROOT / "pg2q4-s3-20261128/output/pg2q4_s3_spectrum.json")
    txt_ag27 = S.parse_grundy_txt(
        ROOT / "s-parameter-kyouen-20261125/output/stats_ag2q7_s2.txt")
    txt_pg25 = S.parse_grundy_txt(
        ROOT / "s-parameter-kyouen-20261125/output/grundy_pg2q5_s3.txt")
    txt_w22 = S.parse_grundy_txt(
        ROOT / "design-kyouen-witt-20261125/output/grundy_w22_s5.txt")
    txt_w24_5 = S.parse_grundy_txt(
        ROOT / "design-kyouen-witt-20261125/output/grundy_w24_s5.txt")
    txt_w24_6 = S.parse_grundy_txt(
        ROOT / "design-kyouen-witt-20261125/output/grundy_w24_s6.txt")
    txt_w24_7 = S.parse_grundy_txt(
        ROOT / "design-kyouen-witt-20261125/output/grundy_w24_s7.txt")

    def from_txt(txt, with_per_size=True):
        maximal = {m: d["maximal"] for m, d in txt["SIZE"].items()
                   if d["maximal"] > 0}
        sizes = {m: d["total"] for m, d in txt["SIZE"].items()}
        gd = dict(txt["GRUNDY"])
        per = txt_per_size(txt) if (with_per_size and txt["GSIZE"]) else None
        return maximal, sizes, gd, per

    def from_gg(name):
        g = gg[name]
        return intkeys(g["maximal_by_size"]), intkeys(g["size_counts"]), \
            intkeys(g["grundy_dist"]), None

    # ---- published side
    pub = {}
    pub[1] = {
        "maximal": {m: d["maximal"] for m, d in census["SIZE"].items()
                    if d["maximal"] > 0},
        "sizes": {m: d["total"] for m, d in census["SIZE"].items()},
        "grundy": sum_dicts(S.K1352_PG2Q9.values()),
        "per_size": S.K1352_PG2Q9,
        "source": "census_pg2q9.txt (sizes/maximal); K1352 (Grundy; not a "
                  "K1358 artifact)",
    }
    pub[2] = dict(zip(("maximal", "sizes", "grundy", "per_size"),
                      from_gg("AG2(5)_s2")))
    pub[2]["source"] = "grundy_general.json AG2(5)_s2"
    pub[3] = dict(zip(("maximal", "sizes", "grundy", "per_size"),
                      from_txt(txt_ag27)))
    pub[3]["source"] = "stats_ag2q7_s2.txt"
    pub[4] = {
        "maximal": None,
        "sizes": {int(m): v["N"] for m, v in sp_ag29["sizes"].items()},
        "grundy": sum_dicts(v["N_g"] for v in sp_ag29["sizes"].values()),
        "per_size": {int(m): {int(g): int(c) for g, c in v["N_g"].items()}
                     for m, v in sp_ag29["sizes"].items()},
        "source": "ag2q9_spectrum.json (N/N_g; no maximal column)",
    }
    for pid, sp, name, kmax in (
            (5, sp_pg23, "pg2q3_s3_spectrum.json", "PG2q3_s3"),
            (6, sp_pg24, "pg2q4_s3_spectrum.json", "PG2q4_s3")):
        pub[pid] = {
            "maximal": dict(S.K1357_MAXIMAL[kmax]),
            "sizes": {int(m): v["N"] for m, v in sp["sizes"].items()},
            "grundy": sum_dicts(v["N_g"] for v in sp["sizes"].values()),
            "per_size": {int(m): {int(g): int(c)
                                  for g, c in v["N_g"].items()}
                         for m, v in sp["sizes"].items()},
            "source": name + " (N/N_g; maximal from K1357)",
        }
    pub[7] = dict(zip(("maximal", "sizes", "grundy", "per_size"),
                      from_gg("AG2(4)_s3")))
    pub[7]["source"] = "grundy_general.json AG2(4)_s3"
    pub[8] = dict(zip(("maximal", "sizes", "grundy", "per_size"),
                      from_gg("AG2(5)_s3")))
    pub[8]["source"] = "grundy_general.json AG2(5)_s3"
    pub[9] = dict(zip(("maximal", "sizes", "grundy", "per_size"),
                      from_txt(txt_pg25, with_per_size=False)))
    pub[9]["source"] = "grundy_pg2q5_s3.txt"
    pub[10] = dict(zip(("maximal", "sizes", "grundy", "per_size"),
                       from_gg("PG2(4)_s4")))
    pub[10]["source"] = "grundy_general.json PG2(4)_s4"
    pub[11] = dict(zip(("maximal", "sizes", "grundy", "per_size"),
                       from_txt(txt_w22)))
    pub[11]["source"] = "grundy_w22_s5.txt"
    pub[12] = dict(zip(("maximal", "sizes", "grundy", "per_size"),
                       from_txt(txt_w24_5, with_per_size=False)))
    pub[12]["source"] = "grundy_w24_s5.txt"
    pub[13] = dict(zip(("maximal", "sizes", "grundy", "per_size"),
                       from_txt(txt_w24_6, with_per_size=False)))
    pub[13]["source"] = "grundy_w24_s6.txt"
    pub[14] = dict(zip(("maximal", "sizes", "grundy", "per_size"),
                       from_txt(txt_w24_7, with_per_size=False)))
    pub[14]["source"] = "grundy_w24_s7.txt"
    # root Grundy values (empty position)
    pub[1]["root"] = 0  # K1352 k=0 G0
    pub[2]["root"] = gg["AG2(5)_s2"]["root_grundy"]
    pub[3]["root"] = txt_ag27["root_grundy"]
    pub[4]["root"] = int(next(iter(sp_ag29["sizes"]["0"]["N_g"])))
    pub[5]["root"] = int(next(iter(sp_pg23["sizes"]["0"]["N_g"])))
    pub[6]["root"] = int(next(iter(sp_pg24["sizes"]["0"]["N_g"])))
    pub[7]["root"] = gg["AG2(4)_s3"]["root_grundy"]
    pub[8]["root"] = gg["AG2(5)_s3"]["root_grundy"]
    pub[9]["root"] = txt_pg25["root_grundy"]
    pub[10]["root"] = gg["PG2(4)_s4"]["root_grundy"]
    pub[11]["root"] = txt_w22["root_grundy"]
    pub[12]["root"] = txt_w24_5["root_grundy"]
    pub[13]["root"] = txt_w24_6["root_grundy"]
    pub[14]["root"] = txt_w24_7["root_grundy"]

    results = []
    for row in ROWS:
        res = load_result(row["result"])
        cres = (load_result(row["cone_result"])
                if row.get("cone_result") else None)
        if "maximal_by_size" in res:  # full DP
            maximal = nonzero(res["maximal_by_size"])
            sizes = nonzero(res["size_counts"])
            gd = nonzero(res["grundy_dist"])
            total = res["positions"]
            g_at = None
            if cres is not None:
                per_size, _, _, _, _, g_at = completed_from_cone(cres)
            else:
                per_size = None
        else:  # cone
            per_size, sizes, gd, maximal, issues, g_at = completed_from_cone(res)
            total = sum(sizes.values())
        rec_sizes = sorted(maximal)
        rec_parity = parity_name(rec_sizes)
        rec_max_g = max(gd)
        p = pub[row["i"]]
        max_source_sizes = None
        if row["i"] == 4:
            # the spectrum JSON's T column is the cone count, not maximality
            max_source_sizes = None

        rep = {
            "row": row["i"],
            "board": row["board"],
            "s": row["s"],
            "claim": {"maximal_sizes": row["claim_sizes"],
                      "parity": row["claim_parity"],
                      "max_grundy": row["claim_max_g"]},
            "recomputed": {
                "maximal_sizes": rec_sizes,
                "maximal_counts": {str(m): maximal[m] for m in rec_sizes},
                "parity": rec_parity,
                "grundy_values": sorted(gd),
                "max_grundy": rec_max_g,
                "root_grundy": (res["root_grundy"] if "maximal_by_size" in res
                                else g_at[0]),
                "positions": total,
                "size_totals": {str(m): sizes[m] for m in sorted(sizes)},
                "grundy_dist": {str(g): gd[g] for g in sorted(gd)},
                "size_grundy": ({str(m): {str(g): v for g, v in ctr.items()}
                                 for m, ctr in per_size.items()}
                                if per_size else None),
            },
            "published": {
                "source": p["source"],
                "maximal_sizes": (sorted(p["maximal"])
                                  if p["maximal"] is not None else None),
                "maximal_counts": ({str(m): p["maximal"][m]
                                    for m in sorted(p["maximal"])}
                                   if p["maximal"] is not None else None),
                "max_grundy": (max(p["grundy"]) if p["grundy"] else None),
                "positions": (sum(p["sizes"].values())
                              if p["sizes"] else None),
            },
            "checks": {},
        }
        c = rep["checks"]
        c["claim_maximal_sizes"] = rec_sizes == row["claim_sizes"]
        c["claim_parity"] = rec_parity == row["claim_parity"]
        c["claim_max_grundy"] = rec_max_g == row["claim_max_g"]
        c["published_maximal_sizes"] = (
            None if p["maximal"] is None else sorted(p["maximal"]) == rec_sizes)
        c["published_maximal_counts"] = (
            None if p["maximal"] is None else p["maximal"] == maximal)
        c["published_size_totals"] = (
            None if not p["sizes"] else p["sizes"] == sizes)
        c["published_grundy_dist"] = (
            None if not p["grundy"] else p["grundy"] == gd)
        c["published_positions"] = (
            None if not p["sizes"] else sum(p["sizes"].values()) == total)
        c["published_root_grundy"] = (
            p["root"] == rep["recomputed"]["root_grundy"])
        if p.get("per_size") is not None and per_size is not None:
            exp = {int(m): {int(g): int(v) for g, v in ctr.items() if int(v)}
                   for m, ctr in p["per_size"].items()}
            got = {m: {g: v for g, v in ctr.items() if v > 0}
                   for m, ctr in per_size.items()}
            c["published_per_size_grundy"] = exp == got
            if exp != got:
                diff = {}
                for m in sorted(set(exp) | set(got)):
                    if exp.get(m, {}) != got.get(m, {}):
                        diff[str(m)] = [exp.get(m), got.get(m)]
                c["per_size_diff"] = diff
        else:
            c["published_per_size_grundy"] = None
        c["maximal_counts_le_size_totals"] = all(
            maximal[m] <= sizes.get(m, 0) for m in maximal)
        c["maximal_counts_le_g0"] = gd.get(0, 0) >= sum(maximal.values())
        if "cones" in res:
            c["cone_divisibility_ok"] = (not res["inflate_issues"]
                                         and not res["max_inflate_issues"])
            c["orbit_counts"] = res["orbit_Nt"]
            c["small_size_grundy"] = ({str(m): g for m, g in g_at.items()}
                                      if g_at else None)
        # ---- structure checks against the published cone data
        if row["i"] == 1:
            sc = S.parse_spectrum(
                ROOT / "pg2q9-cap-game-20261125/output/small_cap_grundy.json")["3"]
            c0 = res["cones"][0]
            c["cone_F_matches_published"] = c0["F"] == sc["cap"]
            c["cone_size_matches_published"] = (c0["cone_size"]
                                                == sc["upset_positions"])
            c["cone_size_layer_matches_published"] = (
                {int(m): v for m, v in c0["size_counts"].items()}
                == {int(m): v for m, v in sc["upset_sizes"].items()})
            c["cone_root_grundy_matches_published"] = (
                c0["root_grundy"] == sc["grundy"])
        if row["i"] == 4:
            pub_t = {int(m): int(v["T"]) for m, v in sp_ag29["sizes"].items()
                     if "T" in v}
            pub_tg = {int(m): {int(g): int(x) for g, x in v["T_g"].items()}
                      for m, v in sp_ag29["sizes"].items() if "T_g" in v}
            mine_t = {int(m): int(v) for m, v in res["cones"][0]["T"].items()}
            mine_tg = {int(m): {int(g): int(x) for g, x in ctr.items()}
                       for m, ctr in res["cones"][0]["T_g"].items()}
            c["published_cone_T"] = mine_t == pub_t
            c["published_cone_T_g"] = mine_tg == pub_tg
            c["cone_size_matches_published"] = (
                res["cones"][0]["cone_size"] == 21353)
        if row["i"] in (5, 6):
            sp = sp_pg23 if row["i"] == 5 else sp_pg24
            pub_t = {int(m): {int(g): int(x) for g, x in v["T_g"].items()}
                     for m, v in sp["sizes"].items() if "T_g" in v}
            pub_u = {int(m): {int(g): int(x) for g, x in v["U_g"].items()}
                     for m, v in sp["sizes"].items() if "U_g" in v}
            mine_t = {int(m): {int(g): int(x) for g, x in ctr.items()}
                      for m, ctr in cres["cones"][0]["T_g"].items()}
            mine_u = {int(m): {int(g): int(x) for g, x in ctr.items()}
                      for m, ctr in cres["cones"][1]["T_g"].items()}
            c["published_triangle_cone_T_g"] = mine_t == pub_t
            c["published_collinear_cone_T_g"] = mine_u == pub_u
            c["cone_sizes"] = [cres["cones"][0]["cone_size"],
                               cres["cones"][1]["cone_size"]]
            c["cone_divisibility_ok"] = (not cres["inflate_issues"]
                                         and not cres["max_inflate_issues"])
        results.append(rep)
        flags = [c["claim_maximal_sizes"], c["claim_parity"],
                 c["claim_max_grundy"]]
        print(f"row {row['i']:2d} {row['board']:7s} s={row['s']}: "
              f"sizes={rec_sizes} parity={rec_parity} G={sorted(gd)} "
              f"maxG={rec_max_g} claim={flags} "
              f"pub_sizes={c['published_maximal_sizes']} "
              f"pub_max={c['published_maximal_counts']} "
              f"pub_tot={c['published_size_totals']} "
              f"pub_G={c['published_grundy_dist']} "
              f"pub_persize={c['published_per_size_grundy']}", flush=True)

    uniform = [r for r in results if r["recomputed"]["parity"] != "mixed"]
    mixed = [r for r in results if r["recomputed"]["parity"] == "mixed"]

    def all_checks(key):
        return all(r["checks"][key] is not False for r in results)

    summary = {
        "rows": len(results),
        "uniform_rows": [[r["row"], r["board"], r["s"]] for r in uniform],
        "mixed_rows": [[r["row"], r["board"], r["s"]] for r in mixed],
        "uniform_all_max_g_1": all(r["recomputed"]["max_grundy"] == 1
                                   for r in uniform),
        "uniform_all_grundy_0_1": all(
            set(r["recomputed"]["grundy_values"]) <= {0, 1} for r in uniform),
        "uniform_distribution_is_parity_law": all(
            (lambda p: (
                r["recomputed"]["grundy_dist"].get("0", 0) ==
                sum(v for m, v in r["recomputed"]["size_totals"].items()
                    if int(m) % 2 == p)
                and r["recomputed"]["grundy_dist"].get("1", 0) ==
                sum(v for m, v in r["recomputed"]["size_totals"].items()
                    if int(m) % 2 != p)
            ))(1 if r["recomputed"]["parity"] == "odd-uniform" else 0)
            for r in uniform),
        "mixed_all_max_g_ge_2": all(r["recomputed"]["max_grundy"] >= 2
                                    for r in mixed),
        "all_claim_sizes": all(r["checks"]["claim_maximal_sizes"]
                               for r in results),
        "all_claim_parity": all(r["checks"]["claim_parity"]
                                for r in results),
        "all_claim_max_g": all(r["checks"]["claim_max_grundy"]
                               for r in results),
        "all_published_max_sizes": all_checks("published_maximal_sizes"),
        "all_published_max_counts": all_checks("published_maximal_counts"),
        "all_published_size_totals": all_checks("published_size_totals"),
        "all_published_grundy": all_checks("published_grundy_dist"),
        "all_published_positions": all_checks("published_positions"),
        "all_published_root": all_checks("published_root_grundy"),
        "all_published_per_size_grundy": all_checks(
            "published_per_size_grundy"),
        "all_divisibility_ok": all(r["checks"].get(
            "cone_divisibility_ok", True) for r in results),
        "all_structure_checks": all(
            v for r in results for k, v in r["checks"].items()
            if isinstance(v, bool) and (
                k.startswith("cone_") or k.startswith("published_cone")
                or k.startswith("published_triangle_cone")
                or k.startswith("published_collinear_cone"))),
    }
    (OUT / "comparison.json").write_text(
        json.dumps({"summary": summary, "rows": results}, indent=1),
        encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
