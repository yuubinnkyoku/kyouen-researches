#!/usr/bin/env python3
"""Post-recomputation comparison with the experiment's own stored aggregates.

The independent-verifier task forbade reading `output/grundy_general.json`
before recomputing; the independent computation is already complete when this
script runs, so this is the allowed provenance cross-check (claims vs.
independent computation vs. the experiment's stored output).

Output: experiment_output_comparison.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
STORED = EXP / "output" / "grundy_general.json"

NAME_MAP = {
    "AG(2,4)-s2": "AG2(4)_s2",
    "AG(2,5)-s2": "AG2(5)_s2",
    "AG(2,4)-s3": "AG2(4)_s3",
}
FIELD_MAP = {
    "safe_count": "safe",
    "safe_by_size": "size_counts",
    "maximal_by_size": "maximal_by_size",
    "grundy_empty": "root_grundy",
    "misere_empty": "root_misere_win",
    "grundy_distribution": "grundy_dist",
}


def int_keys(value):
    if isinstance(value, dict):
        return {int(k): v for k, v in value.items()}
    return value


def main() -> int:
    with open(HERE / "grundy_results.json", encoding="utf-8") as f:
        independent = json.load(f)["cases"]
    with open(STORED, encoding="utf-8") as f:
        stored = json.load(f)
    stored_by_name = {g["name"]: g for g in stored["games"]}

    out: dict = {
        "generated_by": "independent/compare_experiment_output.py",
        "note": "read output/grundy_general.json only after the independent recomputation completed",
        "stored_file": str(STORED.relative_to(EXP.parent.parent.parent)),
        "cases": {},
        "all_match": True,
    }
    for case_key, stored_name in NAME_MAP.items():
        mine = independent[case_key]
        theirs = stored_by_name[stored_name]
        diffs = {}
        for my_field, their_field in FIELD_MAP.items():
            a = int_keys(mine[my_field])
            b = int_keys(theirs[their_field])
            if a != b:
                diffs[my_field] = {"independent": a, "stored": b}
        case_out = {
            "independent_case": case_key,
            "stored_name": stored_name,
            "fields_compared": list(FIELD_MAP),
            "matches": not diffs,
            "diffs": diffs,
        }
        out["cases"][case_key] = case_out
        if diffs:
            out["all_match"] = False

    with open(HERE / "experiment_output_comparison.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"experiment output match: {out['all_match']}")
    for k, c in out["cases"].items():
        print(f"  {k} vs {c['stored_name']}: {'match' if c['matches'] else 'DIFF'}")
    print("wrote experiment_output_comparison.json")
    return 0 if out["all_match"] else 1


if __name__ == "__main__":
    sys.exit(main())
