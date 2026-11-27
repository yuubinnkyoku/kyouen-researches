# 2026-11-27 Part SY wave-B kit: independent cross-check (second host)

Lane: long-running 11x11 lane. Session could not reach the user's PC
(scheduled task without the desktop app); publication via GitHub API only,
sandbox upgraded (Node v22.20.0).

## Situation on resume

Latest main re-fetched first. A same-hourly parallel execution had already
published Part SY wave A (declaration 47ae14ea, 03:29:24Z) and wave B (kit
ef598429, 03:32:03Z) for the seventh-cost full-batch (41 LOSS rows + k05
WIN row) third-implementation corroboration, and is executing the 42 target
passes (kit output dir still partial). Duplicating the batch execution was
avoided; this lane instead performed the independent cross-check of the
published wave-B kit, per the selection-cross-check precedent (8bad4b41).

## Result: CROSSCHECK-PASS (all fail-closed gates, rc=0)

Kit: research/experiments/n11-seventhcost-sy-waveb-independent-crosscheck-20261127/
(fully self-contained byte-clones; 230 files pinned in MANIFEST-sha256.txt).

1. Expectations re-derived from published artifacts with a fresh parser
   (no SY maker/audit code read): 42/42 targets' expected_result /
   stage_budget / replica_expected_quad re-derived from the 126 published
   probe raws (2M sweep, 15M pairs, k05 50M pair ff750cc6 x2) equal the SY
   gate-rows values: 41 exact LOSS(2) + k05 exact WIN(1). Stage policy and
   pair determinism machine-checked.
2. Selection provenance: lo/hi/legal of all 42 targets equal the published
   seventh-cost-exclusive-keys.json (sha256 c395fe03... re-verified); input
   CSVs of the SY kit are byte-identical to the probe kit inputs (42/42),
   input_sha256 pins re-verified.
3. SW kit 41 expected quads and SX kit k05 expected quad
   (90,50000000,1,15763505) + ff750cc6 raw-pair pin all equal the SY
   replica_expected_quad values.
4. Pins: third_impl.js 08ea958f..., jsreplay_lane.js == jsreplay pin
   84585617... (== knowledge-mount copy), verify_tbl.js c8c52528...;
   batch-summary.json 6881eaaf... == published ledger pin; canonical head
   42dbb58f (6832 rows WIN201 LOSS6631).
5. Second-host calibration, this host, Node v22.20.0: C1a verify_tbl rc=0
   (quads 95670/95670, triples 195044, mismatches 0, values byte-equal to
   the owner's run record); C1b calib-k06 LOSS(2) expansions 9,474,431 two
   cold passes identical; C1b calib-k38 LOSS(2) expansions 25,898,941 -
   both EXACT matches to the published provenances.
6. This cross-check's own verification: determinism 3 runs byte-identical
   (crosscheck.json c998d3a5...); tamper battery 3/3 fail-closed + clean
   control rc=0; an ad-hoc fourth tamper (SX k05 quad flip) also
   fail-closed.

## Honest disclosures

- (a) First-draft crosscheck had a fixed BASE path, so the tamper battery
  detected 0/3; fixed to CC_BASE-relative and re-run 3/3 fail-closed before
  freezing. The battery earned its keep.
- (b) First raw parser had a column-offset bug (leading "replay" token;
  legal=c[3], budget=c[5], result=c[6], nodes=c[7] - the same lesson as the
  pre-audit instrument's first draft); caught by the fail-closed gates.
- (c) The SX kit stores its target under a singular "target" key; the
  generic quad pass would have silently skipped it - an explicit
  comparison was added and tamper-verified (T4).
- (d) kit-19 record of record is still unpublished on main; the kit-19x
  authoritative cross-check remains pending for a future run.
- (e) Verdicts NOT consumed; no cache increment; expansions/nodes are
  bookkeeping. The standard 11x11 empty board, all 19 central-reply roots,
  the two-stone root {60,27}, its remaining third moves {100,108}, S2 and
  all closure classes are UNKNOWN.

## Resume (re-fetch latest main before starting; hourly parallel runs)

- If Part SY wave C (42 third-impl results) has landed: run the published
  audit_sy.py plus this lane's crosscheck on the official outputs, then the
  adoption Part (BASE 42dbb58f, fresh declaration, WIN/LOSS conflict
  review) becomes eligible.
- kit-19 authoritative cross-check once kit-19 is published.
- This kit is standalone-reproducible: python3 scripts/crosscheck_sy.py
  (CC_BASE defaults to the kit root).
