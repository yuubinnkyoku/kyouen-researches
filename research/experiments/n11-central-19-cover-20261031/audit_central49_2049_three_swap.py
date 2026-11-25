#!/usr/bin/env python3
"""Exact three-for-three neighborhood of the independently 4x4-audited 2049 cover."""
import json

import audit_central49_2092_three_swap as search
import verify_central49_2092_two_swap_local_optimum as baseline
from verify_central49_2049_three_swap import REMOVED, ADDED


def main():
    selected = set(baseline.reconstruct())
    rm = {int(k, 16) for k in REMOVED}
    ad = {int(k, 16) for k in ADDED}
    search.need(len(rm) == len(ad) == 3 and rm <= selected
                and not (ad & selected), "invalid 2049 replacement")
    selected = (selected - rm) | ad
    result = search.audit(selected, expected_baseline=2049)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
