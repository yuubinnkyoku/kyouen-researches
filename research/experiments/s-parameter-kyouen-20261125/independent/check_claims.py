#!/usr/bin/env python3
"""Compare the independently computed values against the claimed values.

Reads the machine-readable results produced by independent/verify.py and
independent/parity_lemma_ag24_s2.json, and emits claims_check.json with a
field-by-field PASS/FAIL table.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

CLAIMS = {
    "AG(2,4)-s2": {
        "safe_count": 1793,
        "safe_by_size": {0: 1, 1: 16, 2: 120, 3: 480, 4: 840, 5: 288, 6: 48},
        "maximal_by_size": {4: 120, 6: 48},
        "grundy_empty": 0,
        "misere_empty": 1,
        "grundy_distribution": {0: 1009, 1: 784},
    },
    "AG(2,5)-s2": {
        "safe_count": 16426,
        "maximal_by_size": {5: 600, 6: 1000},
        "grundy_empty": 0,
        "misere_empty": 1,
        "grundy_distribution": {0: 5401, 1: 8025, 2: 3000},
    },
    "AG(2,4)-s3": {
        "safe_count": 26073,
        "maximal_by_size": {8: 120, 9: 1120},
        "grundy_empty": 1,
        "misere_empty": 0,
        "grundy_distribution": {0: 12184, 1: 12929, 2: 960},
    },
}


def normalise(value):
    if isinstance(value, dict):
        return {int(k): v for k, v in value.items()}
    return value


def main() -> int:
    with open(HERE / "grundy_results.json", encoding="utf-8") as f:
        results = json.load(f)
    with open(HERE / "parity_lemma_ag24_s2.json", encoding="utf-8") as f:
        lemma = json.load(f)

    out: dict = {
        "generated_by": "independent/check_claims.py",
        "claims_source": "task statement (independent-verifier prompt)",
        "cases": {},
        "all_pass": True,
    }

    for key, claim in CLAIMS.items():
        computed = results["cases"][key]
        case_out = {"field_pass": {}, "field_values": {}, "pass": True}
        for field, expected in claim.items():
            actual = normalise(computed.get(field))
            ok = actual == expected
            case_out["field_pass"][field] = ok
            case_out["field_values"][field] = {"claimed": expected, "computed": actual}
            if not ok:
                case_out["pass"] = False
                out["all_pass"] = False
        out["cases"][key] = case_out

    # Statement-level checks required by the task.
    ag24 = results["cases"]["AG(2,4)-s2"]
    ag25 = results["cases"]["AG(2,5)-s2"]
    statement = {
        "ag24_s2_maximal_sizes_even": sorted(lemma["maximal_sizes"]) == [4, 6]
        and lemma["parity_uniform"]
        and lemma["p"] == 0,
        "ag24_s2_grundy_only_0_1": set(map(int, ag24["grundy_distribution"])) == {0, 1},
        "ag24_s2_parity_formula_every_safe_set": lemma["violations"] == 0
        and lemma["num_safe_sets_checked"] == 1793,
        "ag24_s2_p_is_0": lemma["p"] == 0,
        "ag25_s2_mixed_parity": len(ag25["maximal_parities"]) == 2,
        "ag25_s2_grundy_2_present": ag25["grundy_distribution"].get("2", 0) > 0,
    }
    out["statements"] = statement
    if not all(statement.values()):
        out["all_pass"] = False

    with open(HERE / "board_validation.json", encoding="utf-8") as f:
        out["board_validation_passed"] = json.load(f)["all_passed"]
    if not out["board_validation_passed"]:
        out["all_pass"] = False

    with open(HERE / "claims_check.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)
        f.write("\n")

    print(f"overall PASS: {out['all_pass']}")
    for key, c in out["cases"].items():
        print(f"  {key}: {'PASS' if c['pass'] else 'FAIL'}")
        for field, ok in c["field_pass"].items():
            print(f"    {field}: {'ok' if ok else 'MISMATCH'}")
    print("  statements:")
    for name, ok in statement.items():
        print(f"    {name}: {'ok' if ok else 'MISMATCH'}")
    print("wrote claims_check.json")
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
