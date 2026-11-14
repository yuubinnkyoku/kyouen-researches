# 2026-11-14 n11 cost-68 frontier: open-demand histogram mismatch

Source: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost68-frontier-recompute-20261114.json` on main (read 2026-11-14).

The published `frontier_after_cost68.s6_needed_by_open_classes` is **5259**, but summing the nine buckets of `demand_histogram_open_only` yields:

```text
528 + 3043 + 18 + 278 + 65 + 9 + 1306 + 6 + 61 = 5314
```

The histogram total **5314** is exactly the *after-cost61b* `open_s6` count, whereas after-cost64, after-cost65, and after-cost68 report 5284, 5277, and 5259. This strongly suggests that the histogram is stale, but the underlying S5/S6 incidence data and full recompute script must be rerun before deciding which field is correct. Do **not** treat the nine bucket counts as the current after-cost68 class demand or use them for coordinator prioritization without regeneration.

Independent consistency checks on the ten published stages: `solved_in_manifest + unique_remaining == 7846` at every stage; solved count increases monotonically, remaining cost decreases monotonically. These checks do not independently validate certificate semantics or the claimed class-2 blocker closure.

Reproduce: run `python -c 'import json; p="research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost68-frontier-recompute-20261114.json"; d=json.load(open(p)); f=d["frontier_after_cost68"]; print(sum(f["demand_histogram_open_only"].values()), f["s6_needed_by_open_classes"])'` (expected `5314 5259`).

No change to the mathematical verdict: standard 11×11 empty board and S2 roots remain **UNKNOWN**.
