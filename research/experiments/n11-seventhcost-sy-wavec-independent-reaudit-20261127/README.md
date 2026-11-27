# n11 Part SY wave-C independent re-audit (third host)

Independent verification of the published Part SY wave C official outputs
(research/experiments/n11-seventhcost-thirdimpl-corroboration-20261127,
wave C commit 6148e568, results 42/42 third-impl verdict-level agreements,
HEAD at execution 088f6878). This lane did NOT execute any target pass; it
re-audits the published official outputs with a fresh verifier.

## What was verified (all machine-checked, fail-closed, rc=0)

- Wave-B cross-check kit byte-clone integrity: all 229 MANIFEST files
  re-fetched from published main and sha256-verified 229/229; the published
  crosscheck_sy.py re-run on this third host: CROSSCHECK-PASS rc=0
  (all 42 target expectations re-derived from the 126 published probe raws,
  41 exact LOSS + k05 exact WIN).
- The published audit_sy.py (rev2, sha256 722175e7...) re-run twice on the
  official wave-C outputs: rc=0, rc=0, output sha256 5ce0151f... byte-equal
  to the owner's published audit_sy.run1..run4 (output/published-audit-
  reproduction.txt).
- Fresh independent re-audit (scripts/fresh_reaudit_sy_wavec.py, written
  without reading the owner's audit implementation; disclosure below):
  - 84 target raws parsed with a fresh parser: schema, rc=0 trailers, clean
    reason, row labels, stones=5, lo/hi/legal vs gate-rows, per-pass
    result == expected_result, 41 LOSS + k05 WIN, exactly 84 files no
    extras (H7).
  - Per-target cold pairs: result / expansions / ttHits identical across
    p1/p2; two-pass expansion bill 529,416,996 (bookkeeping).
  - Kit pins: SY kit third_impl.js / verify_tbl.js / jsreplay_lane.js /
    gate-rows.json and all 42 input CSVs byte-equal to the wave-B
    cross-check kit clones.
  - Calibration: c1a rc=0 quads 95,670 triples 195,044 mismatches 0;
    calib-k06 LOSS(2) 9,474,431; calib-k38 LOSS(2) 25,898,941.
  - Three-pillar verdict consistency (H5/H6): every third-impl verdict
    re-checked against (a) the replica verdict re-derived from the 126
    probe raws and (b) the C++ gate expected quadruples (SW 41 LOSS rows,
    SX k05 WIN 90,50000000,1,15763505): 42/42 agreement.
  - Determinism: 2 runs byte-identical (output sha256 11e93d9b...).
- Tamper battery (scratch copies only, deleted after): 5/5 fail-closed
  (T1 k05 expected_result flip -> H1/H3/H5 + per-pass gates; T2 k10.p2
  expansion edit -> pair + bill gates; T3 phantom k99 raw -> H7; T4
  k01.p1 result flip -> expected/quad/pair/H3/H5 gates; T5 k07.p2 rc
  trailer removal -> trailer gate) + clean control rc=0.

## Disclosures

- The author had read the first 40 lines (docstring) of the published
  audit_sy.py before writing the fresh verifier; the parser, gate set and
  expectation derivation here are fresh. Both implementations agree.
- Verdict-level bookkeeping only. NO verdict is consumed, no cache
  increment, no class-status change. The standard 11x11 empty board, all
  19 central-reply roots, the two-stone root {60,27}, its remaining third
  moves {100,108}, S2 and all closure classes are UNKNOWN. Expansions and
  nodes are bookkeeping, never verdicts.
- The 7th-cost batch (41 LOSS + k05 WIN) is adoption-eligible with all
  three pillars verified on three hosts; adoption stays with a separately
  declared adoption Part against the canonical head of record 42dbb58f
  (6,832 rows WIN 201 / LOSS 6,631) under the parent batch's WIN/LOSS
  conflict policy.
