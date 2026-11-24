"""Bonus / reference cross-checks (beyond tasks 1-5).

* one more census layer: the number of 5-caps via  sum over 4-caps of the
  number of extensions, divided by 5  (no full 5-cap enumeration needed)
* the same identity for 4-caps from the 3-cap layer
* internal consistency of output/census_pg2q9.txt and output/orbits.txt
  (distribution sum, q^5-q^2 conics, orbit x stabilizer = |PGL|)
"""
import json

import core
import task2_counts as T2

ALL = core.ALL_POINTS
FB = T2.FB


def main():
    caps3 = T2.enumerate_caps3()
    caps4 = T2.enumerate_caps4(caps3)

    s3 = 0
    for (a, b, c) in caps3:
        forb = FB[a][b] | FB[a][c] | FB[b][c]
        own = (1 << a) | (1 << b) | (1 << c)
        s3 += bin(ALL & ~forb & ~own).count("1")
    s4 = 0
    for (a, b, c, d) in caps4:
        forb = FB[a][b] | FB[a][c] | FB[a][d] | FB[b][c] | FB[b][d] | FB[c][d]
        own = (1 << a) | (1 << b) | (1 << c) | (1 << d)
        s4 += bin(ALL & ~forb & ~own).count("1")

    out = {
        "sum_ext_over_3caps": s3,
        "sum_ext_over_3caps_div4": s3 // 4,
        "equals_n_caps4": s3 // 4 == len(caps4) and s3 % 4 == 0,
        "n_caps4": len(caps4),
        "sum_ext_over_4caps": s4,
        "n_caps5_derived": s4 // 5,
        "equals_n_caps5_exact_div": s4 % 5 == 0,
        "claim_n_caps5_14859936": s4 // 5 == 14859936,
    }

    # ---- reference distribution ----
    census = {0: 1, 1: 91, 2: 4095, 3: 110565, 4: 1769040, 5: 14859936,
              6: 52009776, 7: 51554880, 8: 7960680, 9: 589680, 10: 58968}
    out["census_sum"] = sum(census.values())
    out["census_sum_ok"] = sum(census.values()) == 128917712
    out["census_k3_matches_mine"] = census[3] == len(caps3)
    out["census_k4_matches_mine"] = census[4] == len(caps4)
    out["census_k5_matches_mine"] = census[5] == s4 // 5
    out["conics_formula_q5_minus_q2"] = 9 ** 5 - 9 ** 2
    out["conics_eq_census_k10"] = 9 ** 5 - 9 ** 2 == census[10]
    out["caps9_eq_10_times_conics"] = census[9] == 10 * census[10]

    # ---- reference orbit table: orbit x stabiliser = |PGL| ----
    pgl = 42456960
    orbits = {3: (110565, 384), 4: (1769040, 24), 6: (707616, 60),
              7: (2021760, 21), 8: (5307120, 8), 10: (58968, 720)}
    out["orbit_x_stab"] = {str(k): v[0] * v[1] for k, v in orbits.items()}
    out["orbit_x_stab_all_pgl"] = all(v[0] * v[1] == pgl for v in orbits.values())

    print(json.dumps(out, indent=1))
    with open("out_bonus.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
