# n11-seventhcost-selection-independent-crosscheck-20261126

Independent cross-check of the published seventh-cost exclusive S5 selection kit
(`research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/`,
wave A commit 8d8c3c5c, wave B commit 2098c3ea), performed by a separate lane
while the declaring lane runs the k01..k42 ladder. This lane did NOT run any
claimed-key replay: the single-owner ladder is untouched.

## What was verified (all on this execution host)

1. **Pinned artifacts byte-verified** (raw CDN at 2098c3ea):
   `scripts/select_seventh_exclusive.py` sha256 581cb045... and
   `scripts/jsreplay.js` sha256 84585617... match the declaration pins;
   the regenerated selection JSON is byte-identical to the published
   `output/seventh-cost-exclusive-keys.json` (sha256 c395fe03...).
2. **Selector rerun**: the published selector passes all 214 fail-closed
   gates in a reconstructed dependency tree (14 pinned source files fetched
   individually from raw CDN at 2098c3ea; the selector's own pin gates
   re-verified every dependency sha). Two runs identical; all 42 regenerated
   `input/k*.input.csv` byte-identical to the published batch inputs.
   Head-basis measurements reproduce exactly: 108 S5 children / 100 unknown
   under head 42dbb58f / 42 exclusive / 58 shared / proxy_exclusive_sum
   226,065,724 / bands 5,041,585 x4, 5,234,938 x28, 5,932,112 x10.
3. **Validation gate reproduced**: jsreplay reproduces the four published
   two-target-design rows node-exact at 2M x2 (result 0 / nodes 2,000,000)
   and 15M x2 (result 2 / nodes 3,651,923 and 5,040,200), see
   `output/val-gate-repro.json`.
4. **Independent fresh recomputation** (`scripts/xcheck_seventh.py`, selector
   source NOT consulted; own live-class / exclusivity / ordering logic over
   the same published head cache, geometry, supply ledger and priority
   table): the next unclaimed live class is rank index 6 (rank 7)
   `1306043891938492416:0` coverage {100,103,105,108}; 14/14 checks match the
   published selection JSON including the full 42-key exclusive_probe_order
   (key/proxy/legal per key) and bands, see `output/independent-recompute.json`.
   60 live classes under the head (bookkeeping observation).

## Contents

- `scripts/xcheck_seventh.py`: fresh independent recomputation (sha256 in
  MANIFEST-sha256.txt).
- `output/independent-recompute.json`: 14/14 ALL-CHECKS-PASS.
- `output/val-gate-repro.json`: 4/4 node-exact val-gate reproduction.
- `output/selector-rerun-run{1,2}.json`: published-selector rerun summaries
  (214 gates, identical runs).

## Disclosure

- Dependency tree reconstructed file-by-file (no git in this sandbox); every
  dependency sha was re-verified by the selector's own fail-closed pin gates.
- The concurrent-claim disjointness and quarantine-absence gates were verified
  by the selector rerun (its gates read the published claim sources
  machine-side); the fresh recomputation additionally confirmed head-absence
  of all 42 keys.
- Raw CDN was the fetch basis at 2098c3ea; cross-check files were compared
  byte-wise, not via API text extraction.

## Status guard

Selection/scheduling cross-check only. No verdict of this table is claimed or
implied; no ladder row was run or consumed. The standard 11x11 empty board:
UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone root {60,27}: UNKNOWN.
Third-move pair {100,108}: UNKNOWN. Every closure class: UNKNOWN unless a
published Part says otherwise.
