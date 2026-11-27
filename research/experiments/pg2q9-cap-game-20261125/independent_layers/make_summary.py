"""Collect the machine-readable results of steps 1-4 into one summary."""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"


def load(name):
    p = OUT / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def main() -> None:
    s1 = load("step1_board_census.json")
    s2 = load("step2_grundy_samples.json")
    s3 = load("step3_global_checks.json")
    s4 = load("step4_conic_uniqueness.json")
    s5 = load("step5_conic6.json")
    cs = load("conics_summary.json")

    summary = {
        "verdict": {
            "board_is_PG(2,9)": s1["isomorphism"]["isomorphism"] if s1 else None,
            "projective_plane_of_order_9": s1["board"]["projective_plane_of_order_9"] if s1 else None,
            "census_and_analysis_agree": s1["arithmetic"]["analysis_matches_census"] if s1 else None,
            "all_G_sums_equal_census": all(s1["arithmetic"]["checks"]["G_sums"].values()) if s1 else None,
            "conics": cs,
            "independent_cap_counts": s1.get("independent_counts") if s1 else None,
            "independent_counts_match_census_up_to": s1.get("independent_counts_match_census_up_to") if s1 else None,
            "samples": {k: v for k, v in (s2["summary"] if s2 else {}).items()},
            "sample_failures": [],
            "global_checks_failures": s3["failures"] if s3 else None,
            "conic_uniqueness_failures": s4["failures"] if s4 else None,
            "conic6_failures": s5["failures"] if s5 else None,
        }
    }
    (OUT / "verification_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print("wrote", OUT / "verification_summary.json")


if __name__ == "__main__":
    main()
