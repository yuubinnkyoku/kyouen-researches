# n11 S5 true-vs-adaptive cost re-measurement (2026-11-21)

Measurement-only session. Re-derives, from published pinned bytes only, the current
out-of-sample relationship between observed exact-replay resolution node counts
("true cost") and the adaptive truncated-cost proxy (legal-decile historical mean of
the frozen historical-cost-profile corpus, censored at 15M in its source corpus), and
publishes the allocation table for the 63 unknown children of the third-cost class
`1297036830122704896:0`, as requested by the third-cost session log (commit 047d3d51).

No solver was run, no cache was written, no key was claimed. Scheduling hints only.

## Method

- Cohorts, all re-derived fresh from the pinned bytes (never from prose):
  - `reply27`: 42 rows of the pinned reconciliation-findings.json; 27 resolved LOSS
    at 15M participate in the ratio sample.
  - `reply27_late`: the 15 rows exhausted at the 2M row stage, all later resolved
    LOSS inside the probe-13 base pin 60e0dc34; true cost re-read from the base pin
    (3,651,923-12,626,043 nodes). Strict disjointness from every other cohort is
    machine-gated.
  - `thirdcost`: 37 resolved LOSS rows (chain cache bb4495e0 minus probe-13 base) + 2
    parked UNKNOWN@15M.
  - `fourthcost`: 33 resolved LOSS + 8 parked UNKNOWN@15M of the pinned fourth-cost
    pass-1 complete note (41 keys; authoritative order pinned in
    fourth-cost-exclusive-keys.json).
- Ratio = true resolution nodes / adaptive proxy, per key, out-of-sample.
- 674 fail-closed machine gates (pin sha256, cache row counts and sort order, byte
  preservation, verdict re-computation, cohort disjointness, cohort coverage of the
  pinned selections, legal counts, proxy bin agreement). Any gate failure exits
  non-zero and writes no output.
- Deterministic: byte-identical output across independent runs (verified 3x in the
  authoring layout and 1x in the published-layout tree).

## Headline results

- Combined out-of-sample ratio, resolved rows only, n=112:
  min 0.3208, q25 0.5786, median 0.9613, q75 1.2303, max 2.6259, mean 1.0243.
- Per-cohort medians: reply27 1.139, reply27_late 1.139, thirdcost 0.758,
  fourthcost 0.579.
- Per-legal-decile medians (n): 80s 0.536 (17), 90s 0.698 (52), 100s 0.758 (7),
  110s 1.219 (36). The median ratio rises monotonically with legal count: the proxy
  increasingly underestimates high-legal keys' relative cost.
- reply27 censoring recovery: every row censored at the 2M row stage was later
  resolved LOSS inside the probe-13 base pin (late-cohort ratios 0.698-2.491,
  median 1.139). The row-era censoring direction is confirmed and nothing remains
  censored from that cohort. Parked keys remain only in thirdcost (2) and fourthcost
  (8), both UNKNOWN@15M, untouched here.
- Class `1297036830122704896:0` allocation (scheduling hints only): 63 unknown
  children = 2 single-live-parent (claimed by the parked-pair L50M ladder lane,
  declaration commit b1a38144) + 61 shared; shared proxy sum 344,429,482;
  shared-sum ratio-quantile estimates: median-ratio 331,108,047 and q75-ratio
  423,744,286 nodes.

## Interpretation guards

- The ratio sample is resolved-only and therefore selected toward keys the chain
  could close; keys parked at 15M are excluded from ratios by construction. Both
  observed tails (legal 110 median 1.22, late-cohort max 2.49) say escalations cost
  more than the proxy suggests; treat proxy-median estimates as optimistic floors
  for scheduling, never as expected costs.
- The proxy corpus is censored at 15M (2,629 unique S5 keys, selection bias
  documented upstream in the profile caveat).
- No resolution probability is calibrated or claimed anywhere in this experiment.

## Reproducibility

From a repo checkout:

```sh
python3 research/experiments/n11-s5-true-vs-adaptive-remeasurement-20261121/scripts/measure_tva.py
```

Output is `output/measurement.json`, deterministic byte-for-byte.
sha256 2ec25636987efc0a5b57ade2cc0eddbade1ee23653527ca85b64c6b54ccedc22.

Dual layout: `scripts/pub_paths.py` resolves the pinned inputs either from their
published repo locations (above) or from the authoring-kit layout; every input is
sha256-gated in both layouts.

## Status guard

The standard 11x11 empty board remains UNKNOWN. The two-stone root {60,27} and both
remaining third moves 100/108 remain UNKNOWN. `1297036830122704896:0` remains UNKNOWN
(44 LOSS / 63 unknown / 107 children). Node counts, proxies, ratio estimates and
allocation ranks are never verdicts and never authorize skipping any key.
