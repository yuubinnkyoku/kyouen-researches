# 2026-11-28 eight-row q9 8x29 row-split direct evaluation — single-owner declaration (publish-then-execute)

## Scope (single-owner)

- Board family (w,q)=(8,9), deficient-maximal band. Current published state (results/fixed-width/mwq_stabilization.csv (8,9) row, source K0318;eight-row-bands-20261114): witness band 8x9..8x28 (m=27 and m=28 resolved by rowY=3 fixed-row split, 154,022 / 3,049,989 conflicts), M_{8,9} in [29,984], frontier 8x29. No width >= 29 has ever been evaluated.
- Target: **8x29 rowfixed evaluation**, deficiency-row conditioning over the 4 vertical-mirror row classes {0,1,2,3} (V: y <-> 7-y), in the order rowY=3 first (continuation of the m=27/28 conditioning), then 0, 1, 2 as needed.
- WIN-stop rule: first SAT piece stops the sweep (a single witness resolves the band extension); remaining pieces stay unswept and are disclosed as such.
- Honest INDET policy: any piece hitting its time cap is recorded INDET with conflicts as an honest negative; no absence claim from INDET. UNSAT of a rowfixed piece is a per-piece absence claim only (deficiency must be in that row class); absence at 8x29 requires all 4 row classes UNSAT plus multi-deficiency classes, which this Part does not claim unless measured.

## Pre-registered calibration (executed after this declaration is published)

- Cold rerun of the published m=28 rowY=3 instance through the identical pipeline: expected **SAT, conflicts 3,049,989** (records.jsonl eight-row-bands-20261114/output/w8q9-witness-search). Bit-exact conflicts expected; wall time is host-dependent and disclosed, not gated.
- CNF determinism: regeneration of the (8,28,9) rowY=3 CNF twice, byte-identical.

## Toolchain pins (all fetched from main before this declaration)

- genfast.js sha256 409b52164962298dbbd6e4138098696e0147f07ec935479a2b8b645f2594aa53 (eight-row-bands-20261114/scripts, VERBATIM from seven-row-q9-q10-bands-20261114)
- decode_verify.js sha256 bf64e42810e62861570b13cab55381ccb9f85a795eebe902f43be5edc898f5bf
- sat.js fcc0cfd8bfc7497390369111a5523547c3873435336fdf21d60b39d66cf5dac1, sat2.js 14ceb85414b56b1dd89a74c9a00fe29169ff19095da1df2a57b7f6606317da9e, verify_witness.py 298ff590c376f3075a0e3b6813dcf16a754564fbbe600c4e1b5d6316db6ce243 (seven-row-inband-families-20261114/scripts)
- kissat 4.0.4 official linux-amd64, md5 3a5eba830aa6008a604fcc9bbe99a325, sha256 21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1 (pinned binary reused; md5 matches the K1134 band-lane pin)
- Time cap per instance: 280 s (container piece cap); escalation beyond the cap is a fresh decision, not part of this Part.

## Verification protocol on SAT

- Model decode via decode_verify.js (jsVerify) + independent exact-Fraction verify_witness.py (pyVerify); both must PASS (safe + maximal + deficient). Cold pair: the deciding piece is rerun cold; conflicts must be identical (wall time may differ).
- New K item on a SAT verdict updates the (8,9) csv row (witness band, M_{8,9} lower bound); an all-INDET/UNSAT-with-gaps outcome is published as honest negatives only.

## Non-goals / disclaimers

- No 11x11 claim: the standard 11x11 empty board and all closure classes remain UNKNOWN; verdicts here are not consumed by any 11x11 bookkeeping.
- No multi-deficiency (2-deficient-row) coverage at 8x29 is claimed by this Part unless explicitly run and disclosed.
- Parallel-lane hygiene: latest main was re-fetched immediately before this declaration; no eight-row q9 8x29 lane was declared or in flight (active single-owner lanes today: 5x28, 6x23, 6x26 multi-def, 6x31, 6x32, 7x28, 7x32, 7x38, six-row q8 band m=109..370, n11 escalation/adoption lanes).
- HEAD at declaration time: ed37b8ab (re-checked; this declaration is the only eight-row q9 claim).
