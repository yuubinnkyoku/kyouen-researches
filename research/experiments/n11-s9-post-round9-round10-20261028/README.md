# N11 post-round9 round10: 32 frozen S9 terminal claims and WIN8 lift

The 32 canonical nine-stone positions are the exact keys in
`../n11-s9-post-round9-replan-20261028/next-plan.json` (selection SHA-256
`42702f97100ee62a07d6c0603409ac17a19f8db47c8bf3039083c8e8fced3299`).

`prove.js` discovers terminal WIN/LOSS with both the 3×3 difference determinant
and independent 4×4 integer Bareiss geometry, caching terminal S10 results
within the batch. The fixed `certificate.json` contains 8 WIN9 (all 207 S10
children checked) and 24 LOSS9 (one explicit LOSS10 witness each), plus 240
canonical LOSS9 parents of the certified LOSS10 witnesses.

The bounded [terminal discovery CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40654746616)
passed: 393 distinct S10 terminal leaves, 68,906 recursive states per geometry.
The [independent fixed-certificate CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40654867335)
also passed, including forged WIN9/LOSS9 and out-of-range witness rejection.
`verify_compact.js --negative` checks only 231 required terminal leaves and
42,709 recursive states per geometry (a replay-work reduction, not an
end-to-end speedup claim). `prove.js` replays the complete discovery and
requires exact equality with the frozen certificate.

The [bounded proof-only WIN8 lift CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40654919639)
**passed**. `lift.js` independently rebuilds the earlier proof-only WIN8
frontier and propagates only the eight terminal-certified WIN9 roots, checking
the source hash chain, legal parent-child incidence, and known LOSS8 conflicts.
Its output is frozen in `lift.json`; future `lift.js` executions fail on a
mismatch.

The eight WIN9 yield **72** distinct WIN8 parent classes, **64** new relative
to the previous proof-only set: **5,449 → 5,513**. The fixed conditional
14-root S8 frontier has **548** edges, with secured **455 → 465** and unproved
**93 → 83**. No WIN/LOSS conflicts or new S7/S5/two-stone verdicts.

Next: replan the bounded S9 terminal candidate batch against the **83**
remaining edges. This fixed conditional 14-root coverage is **not** a
re-optimized minimum, a two-stone root closure, or an empty-board proof.

**Standard 11×11 empty-board winner: UNKNOWN.**
