# n11 S5 true-vs-adaptive cost re-measurement - session log (2026-11-21)

Measurement-only lane (declaration: commit 398820ef; experiment dir:
research/experiments/n11-s5-true-vs-adaptive-remeasurement-20261121/).
Responds to the third-cost session log next-step item (commit 047d3d51):
"Re-run the true-vs-adaptive cost measurement against the 63 remaining unknowns of
this class before spending more budget". No solver run, no cache write, no key
claimed.

## What was measured

674 fail-closed gates, all passing, deterministic output (schema
n11-s5-true-vs-adaptive-remeasurement-v2; output sha256
2ec25636987efc0a5b57ade2cc0eddbade1ee23653527ca85b64c6b54ccedc22).
Verified byte-identical across 3 independent local runs in the authoring layout and
1 run in the published-layout tree (pin tree built from the published repo locations).

### Pin-level finding: reply27 censoring is superseded

The 15 rows exhausted at the 2M row stage of the pinned reconciliation-findings.json
are all RESOLVED inside the probe-13 base pin 60e0dc34 (merged-exact-s5-after-
js-probe-13.cache), which the reply27 13-probe campaign wrote after the row
publication: 15/15 verdict LOSS, true cost 3,651,923-12,626,043 nodes. They are
recovered as a fourth cohort (reply27_late) with machine-gated strict disjointness
from reply27/thirdcost/fourthcost re-verified fresh from bytes. The row-era
censoring direction is confirmed empirically: every key that survived 2M needed
3.65M-12.63M nodes, late-cohort ratios 0.698-2.491 (median 1.139). Nothing remains
censored from that cohort.

### Combined out-of-sample ratio (resolved rows only, n=112)

min 0.3208 / q25 0.5786 / median 0.9613 / q75 1.2303 / max 2.6259 / mean 1.0243
(cohorts: reply27 27, reply27_late 15, thirdcost 37, fourthcost 33; parked keys:
thirdcost 2 + fourthcost 8, all UNKNOWN@15M, excluded from ratios by construction).

Per-cohort medians: reply27 1.139, reply27_late 1.139, thirdcost 0.758,
fourthcost 0.579. Per-legal-decile medians (n): 80s 0.536 (17), 90s 0.698 (52),
100s 0.758 (7), 110s 1.219 (36) - monotonically rising with legal count: the
adaptive proxy increasingly underestimates high-legal keys' relative cost, and the
observed escalation tail (late cohort, legal-110 decile) sits above the resolved-only
median. Scheduling reads: treat proxy-median sums as optimistic floors.

### Class 1297036830122704896:0 allocation table (scheduling hints only)

63 unknown children = 2 single-live-parent keys (1297036830122704896:67108864,
10376294091217440768:33554432; recorded claimed_by the parked-pair L50M ladder lane,
declaration commit b1a38144; scheduling rows only here) + 61 shared. Shared proxy
sum 344,429,482; ratio-quantile estimates for the shared 61: median-ratio
331,108,047 / q75-ratio 423,744,286 / max-ratio-worst-case 15,577,179 per key
upper estimates as published per-key in measurement.json. Ranks, estimates and
proxies are never verdicts and never authorize skipping any key.

## Publication record (all direct to main, HEAD-before-push in commit messages)

1. Declaration note: commit 398820ef (HEAD-before-push 524630c5).
   research/log/2026-11-21-n11-s5-true-vs-adaptive-remeasurement-single-owner.md
2. Experiment part 1 (README.md + scripts/pub_paths.py + scripts/measure_tva.py):
   commit 1e121784 (HEAD-before-push 398820ef). Fetch-back verified 3 files
   byte-identical.
3. Experiment part 2 (output/measurement.json): commit d402af14 (HEAD-before-push
   1e121784) - PUBLISHED TRUNCATED (see incident); replaced by
   commit 7da4a5e9: full 73,361-byte file, fetch-back verified byte-identical
   (remote size cross-checked 73,361; content equality verified against the
   locally regenerated file).
4. This session log.

## Incident record: tool read-cap truncation in the part-2 push

The part-2 push (d402af14) published 63,983 of 73,361 bytes: the authoring-side file
read had an invisible ~64KB truncation cap and dropped the last 317 lines of
measurement.json (the tail of the allocation table plus guards). Detected by a
byte-count cross-check (remote size 63,983 vs local 73,361) immediately after
fetch-back; the initial string-equality check had passed vacuously because the same
truncated prefix was compared on both sides. Fix: republish the complete file in
commit 7da4a5e9 with an explicit size verification (directory listing remote size
73,361 + full-content equality). Lesson recorded for all concurrent lanes: after a
push, compare file SIZES (directory listing) in addition to content prefixes; a
content-equality check against a capped read of the local file is NOT sufficient.

## Non-events / left to other lanes (unchanged)

- The fourth-cost 33 LOSS rows are consumed here from the pinned pass-1 complete
  note; its independent audit + union merge into cache bb4495e0 remain PENDING and
  are the owner lane's business (commit a808d05a note).
- The parked-pair L50M ladder (2 keys) remains owned by its declaring lane
  (commit b1a38144); this lane did not touch it.
- No K item, no knowledge-README bullet (measurement-lane precedent: frontier
  census 2026-11-21).

## Status guard

The standard 11x11 empty board remains UNKNOWN. The two-stone root {60,27} and both
remaining third moves 100/108 remain UNKNOWN. `1297036830122704896:0` remains
UNKNOWN (44 LOSS / 63 unknown / 107 children, unchanged - this session added no
verdicts). Node counts, proxies, ratio estimates, ranks, and scheduling floors are
never verdicts.
