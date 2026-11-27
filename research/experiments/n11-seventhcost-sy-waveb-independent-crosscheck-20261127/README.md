# n11 Part SY wave-B kit: independent cross-check (second host)

Independent verification of the published Part SY wave-B kit
(research/experiments/n11-seventhcost-thirdimpl-corroboration-20261127,
wave B commit ef598429, declaration 47ae14ea). This lane did NOT execute any
of the 42 SY target passes (owner lane is executing them); it verifies the
kit's expectations, pins, provenance and calibration on an independent host.

## What was verified (all machine-checked, fail-closed, rc=0)

- gate-rows.json schema/heads: declaration head 47ae14ea, canonical head
  42dbb58f (rows 6832 WIN201 LOSS6631) == batch-summary head_basis.
- 42 targets: lo/hi/legal vs the published selection
  seventh-cost-exclusive-keys.json (sha256 c395fe03..., pin match);
  expected_result / stage_budget / replica_expected_quad re-derived from
  the 126 published probe raws (2M sweep 42, 15M pairs, k05 50M pair
  ff750cc6 x2) with a fresh parser; 41 exact LOSS(2) + k05 exact WIN(1);
  stage policy (2M/15M/50M, UNKNOWN nodes==budget, pair determinism).
- input_sha256: SY kit input CSVs == probe kit input CSVs byte-identical
  (42/42), pins in gate-rows re-verified.
- SW kit expected quads 41/41 and SX kit k05 expected quad
  90,50000000,1,15763505 + raw_pair_sha256 ff750cc6 pin: all equal to the
  SY replica_expected_quad values.
- Pins: third_impl.js 08ea958f..., jsreplay_lane.js == pinned jsreplay
  84585617... (also == knowledge-mount copy), verify_tbl.js c8c52528...
- batch-summary.json sha256 6881eaaf... == the published ledger pin.

## Independent second-host calibration (this host, Node v22.20.0)

- C1a verify_tbl: rc=0, replica quads 95670 / mine 95670, triples checked
  195044, mismatches 0 (output/c1a-verify-tbl.txt) - byte-equal to the
  owner's wave-B run record.
- C1b calib-k06 (10376293541462675456:65536 legal 89): LOSS(2) expansions
  9,474,431, two cold passes identical (27.5-28.1s each) - EXACT match to
  the owner's calibration and the published sixth-cost k06-cold-a raw
  (output/calib-k06-pass1.txt, calib-k06-pass2.txt).
- C1b calib-k38 (10376293541461626880:66048 legal 100): LOSS(2) expansions
  25,898,941 (73.8s) - EXACT match to the Part SU publication
  (output/calib-k38-pass1.txt).

## Verification of this cross-check

- Determinism: 3 runs byte-identical (output/crosscheck.json sha256
  c998d3a5fc549b22aecb22059e5510e3a2b363a2c7e41e343246390cbe8b1584).
- Tamper battery (scratch copies only): 3/3 fail-closed (T1 k07
  expected_result flip / T2 k20 stage_budget flip / T3 k15 15m raw nodes
  edit) + clean control rc=0 (output/tamper-battery.txt). A fourth ad-hoc
  tamper (SX k05 expected quad flip) was also confirmed fail-closed.

## Disclosures

- This kit carries byte-clones of the SY wave-B kit files (gate-rows.json,
  third_impl.js, jsreplay_lane.js, verify_tbl.js), the SW/SX kit
  gate-rows, the selection keys/batch-summary and all 126 raws so the
  cross-check is reproducible standalone (CC_BASE defaults to the kit
  root; scripts/crosscheck_sy.py).
- First-draft crosscheck had a fixed BASE path that ignored tampered
  scratch copies; the tamper battery caught it (0/3 detected) and it was
  fixed to CC_BASE-relative before freezing. Also the first raw parser had
  a column-offset bug (leading "replay" token; legal=c[3], budget=c[5],
  result=c[6], nodes=c[7]) - caught by the fail-closed gates themselves.
- The SX kit uses a singular "target" key; an explicit comparison was
  added after noticing the generic pass would have skipped it.

## Meaning and non-meaning

This is integrity/corroboration bookkeeping for the SY kit BEFORE its
target passes land. NO verdict is consumed, no cache increment, no
class-status change. The standard 11x11 empty board, all 19 central-reply
roots, the two-stone root {60,27}, its remaining third moves {100,108},
S2 and all closure classes are UNKNOWN. Expansions and nodes are
bookkeeping, never verdicts.
