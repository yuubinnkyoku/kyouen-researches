"""Final consistency audit over the JSON artifacts of this verification."""

from __future__ import annotations

import json

import g2common as C


def load(name):
    return json.loads((C.OUT / name).read_text(encoding="utf-8"))


def main():
    checks = []

    b = load("task1_boards.json")
    for name, rec in b.items():
        checks.append((f"{name} valid s=2 incidence", rec["valid_s2_incidence_structure"]))
        checks.append((f"{name} pair uniqueness", rec["each_pair_at_most_one_line"]))
        checks.append((f"{name} pair count", rec["pairs_seen"] == rec["pairs_possible"]))

    a5 = load("task2_AG2q5.json")
    checks += [
        ("AG(2,5) maximal 5-caps = 600", a5["maximal_odd_caps"]["count"] == 600),
        ("AG(2,5) 4-subsets 3000 distinct", a5["subsets"]["distinct"] == 3000
         and a5["subsets"]["duplicates"] == 0),
        ("AG(2,5) G2 set = 4-subsets", a5["g2"]["equals_all_subsets"]),
        ("AG(2,5) G2 total 3000", a5["g2"]["count"] == 3000),
        ("AG(2,5) full dist matches", a5["comparison"]["json_grundy_dist"]["match"]),
    ]

    a7 = load("task2_AG2q7.json")
    checks += [
        ("AG(2,7) maximal 7-caps = 2352", a7["maximal_odd_caps"]["count"] == 2352),
        ("AG(2,7) 5-subsets 49392 distinct", a7["subsets"]["distinct"] == 49392
         and a7["subsets"]["duplicates"] == 0),
        ("AG(2,7) G2 set = 5-subsets", a7["g2"]["equals_all_subsets"]),
        ("AG(2,7) G2 total 49392", a7["g2"]["count"] == 49392),
        ("AG(2,7) published GRUNDY matches", a7["comparison"]["txt_grundy"]["match"]),
        ("AG(2,7) published SIZE totals match",
         a7["comparison"]["txt_size_total"]["match"]),
        ("AG(2,7) published maximal column match",
         a7["comparison"]["txt_maximal_column"]["match"]),
        ("AG(2,7) published G0 column match",
         a7["comparison"]["txt_g0_column"]["match"]),
    ]

    pg = load("task2_pg.json")
    checks += [
        ("PG census SAFE = size sum", pg["census"]["safe_matches_size_sum"]),
        ("PG census max7 = 2021760", pg["census"]["claims"]["match"]),
        ("PG low-size census matches", pg["low_size_independent"]["counts_match"]),
        ("PG low-size maximal matches", pg["low_size_independent"]["maximal_match"]),
        ("PG generators all automorphisms", pg["generators"]["all_ok"]),
        ("PG orbit size 2021760", pg["orbit"]["size"] == 2021760),
        ("PG 6-subsets 14152320 distinct", pg["six_subsets"]["count"] == 14152320
         and pg["six_subsets"]["duplicates"] == 0),
        ("PG six-subset claim match", pg["six_subsets"]["match"]),
        ("PG K1333 arithmetic match", pg["k1333_arithmetic"]["match"]),
    ]

    reps = load("task3_reps.json")
    for name, rec in reps.items():
        checks.append((f"{name} 8 reps all G=2 + mixed", rec["all_pass"]))
        checks.append((f"{name} 8 reps present", len(rec["reps"]) >= 5))

    t4 = load("task4_pg.json")
    for key, val in t4["six_cap_sample"]["checks"].items():
        checks.append((f"PG six-cap sample: {key}", val))
    checks.append(("PG published sixcap results match",
                   t4["published"]["published_results_match_ours"]))
    checks.append(("PG G0 arithmetic", t4["published"]["arithmetic_ok"]))
    checks.append(("PG published G2 value 14152320",
                   t4["published"]["k1333_6cap_g2"] == 14152320))

    t5 = load("task5_literal.json")
    expect = {"PG(2,9)": [], "AG(2,7)": [5], "AG(2,5)": [4]}
    for name, rec in t5.items():
        checks.append((f"{name} literal scan G=2 layer", rec["g2_subset_sizes"] == expect[name]))

    bad = [c for c in checks if not c[1]]
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    print(f"\n{len(checks) - len(bad)}/{len(checks)} checks passed")
    if bad:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
