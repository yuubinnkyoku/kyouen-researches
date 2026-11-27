#!/usr/bin/env python3
"""Final gate: assert every result file from stages 1-6 is a PASS and restate
the headline numbers so the report has a single machine-checked summary.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    with open(HERE / name, encoding="utf-8") as f:
        return json.load(f)


def main():
    s1 = load("stage1.json")
    s2 = load("stage2.json")
    s3 = load("stage3.json")
    s4 = load("stage4.json")
    s5 = load("stage5.json")
    s6 = load("stage6.json")

    assert s1["board_checks"]["is_projective_plane_order_4"] is True
    assert s1["matches_claim"] is True
    assert s1["total"] == 180058 and s1["max_size"] == 9

    assert s2["counts_ok"] is True
    assert s2["same_as_dfs"] is True
    assert s2["grundy_ok"] is True
    assert s2["total"] == 180058 and s2["max_size"] == 9
    assert (s2["g0"], s2["g1"], s2["other"]) == (89799, 90259, 0)
    assert s2["uniform"] is True and s2["stuck"] == 360

    assert s3["n_triangles"] == 1120 and s3["n_collinear"] == 210
    assert s3["T_total"] == 5038 and s3["U_total"] == 3809
    assert s3["identity_ok"] is True and s3["total_pairs"] == 6442450

    assert s4["memo_size"] == 180058 and s4["g_empty"] == 1
    assert s4["mismatch_stage2"] == 0 and s4["mismatch_claim"] == 0
    assert s4["all_samples_ok"] is True
    assert s4["chain_ok"] is True and s4["totals_ok"] is True and s4["layer_ok"] is True
    assert (s4["g0"], s4["g1"], s4["other"]) == (89799, 90259, 0)

    assert s5["zero_extension_by_size"] == {"7": 360, "9": 11480}
    assert s5["bad_terminal_grundy"] == 0

    for name, row in s6.items():
        assert row["ok"] is True
        assert row["total"] == (5038 if "triangle" in name else 3809)

    print("FINAL GATE: ALL PASS")
    print("  board: PG(2,4) (2-(21,5,1))")
    print("  safe sets: 180,058  (G0 89,799 / G1 90,259), max size 9")
    print("  layer G: 1,0,1,0,1,0,1,0,1,0")
    print("  maximal: 11,480 size-9 + 360 size-7")
    print("  cones: T=5,038 (1,120 triangles), U=3,809 (210 collinear triples)")
    print("  identity: 1,120*T_m(g)+210*U_m(g)=C(m,3)*N_m(g) for all m,g")
    print("  random caps: 20/size, all match; direct upset DP = array DP")


if __name__ == "__main__":
    main()
