# Completion log: n11 ultra-cheap class-completion candidate census (2026-11-27, long lane)

Part type: measurement/census (scheduling input only). NO verdict consumed,
NO probe executed, NO branch created. Standard 11x11 empty board: UNKNOWN.
All 19 central-reply roots: UNKNOWN. Two-stone root {60,27} and third moves
100/108: UNKNOWN.

## What was produced

- `research/experiments/n11-ultra-cheap-class-census-20261127/` — fresh
  census instrument `scripts/ultra_cheap_census.py`
  (sha256 `c5e7b88e76d1a4652c67bfdd05b870b0c1076681a55c64691eaa87e6f9af634d`),
  three cold passes byte-identical (run json sha256
  `a60716ac84e22833eaf570819d8744a2c66b2ad1d563b3791ade829eaed87906`),
  18 gates, 5/5 fail-closed tamper battery with clean control re-PASS.
- Result: all 804 closure-ladder rows' `unknown_now` independently
  recomputed from frozen dependency graph `54f9c364...` + head `1e2eeda2...`
  + update8 receipts `b658290a...` — 804/804 exact match. Exactly 4 classes
  sit at one remaining unknown S5 child, all 4 keys unclaimed across all
  15 claim sets (focus_35, cert_38, third_39, fourth_41, fifth..eleventh,
  twelfth_51, sbd_101, parked_6, quarantine_2), fresh vs head, not in
  probe-13 supply:
  - class 16371 / unknown S5 `1153202979851993088:272`
  - class 23101 / unknown S5 `1152921505747697664:1032`
  - class 1849  / unknown S5 `1153485622925590528:0`
  - class 2251  / unknown S5 `1297036830121656320:131074`

## Why this matters (cost argument)

Each of these 4 keys is a single-verdict class completion: strictly
cheaper than any multi-key serving-class batch the coordinator can
schedule next. This is scheduling bookkeeping only; selecting and
probing any of them belongs to a future selection Part with its own
single-owner declaration.

## Verification and disclosures

- Trust boundary re-implemented fresh (the published refresh machinery
  was not read or executed); SZ-wave-E note's 4-class prediction
  reproduced independently, and the class-16371 unknown key matches
  the SZ-wave-E published measurement verbatim.
- 3 runs byte-identical; tamper battery T1..T5 all fail-closed (P2
  recomputation gate, P0 head/graph sha pins, P3 claim-size gate; T5
  receipt-deletion caught by both pin and semantic gate). Clean control
  re-PASS byte-identical.
- Disclosures: first draft keyed classes by geometry.json.gz and failed
  its own gate (rewritten against the dependency graph before any
  recorded result); CAND_SHA pin typo (62/64 chars) caught by the pin
  gate; update8 `resolved_s5_verdicts` holds 23 keys (282 is a different
  counter); first T5 attempt was a structural no-op (no receipt key is
  in the head cache) and was replaced with receipt deletion.
- 23 receipt keys cross-checked against head: 0 receipt/cache conflicts.

## Concurrency state at publication time

- twelfth-cost batch stage-1 sweep declaration `f6d29d16` (16:41Z)
  still without published wave-B raws at last poll (HEAD `3e92e42a6`).
  This census does not touch the twelfth batch or its selection kit;
  no ownership conflict.

## Access note

This lane runs without access to the user's computer (scheduled task
without the desktop app); publication via GitHub API only, verified by
raw CDN fetch-back.
