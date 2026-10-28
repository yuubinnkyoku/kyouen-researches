# N11 fixed round9: 32 terminal S9 certificates

Standard q=4, complete-call, normal play. Original-first-player viewpoint. Empty-board winner **UNKNOWN**.

The 32 canonical S9 keys come **only** from the frozen, independently replayable round8 `next-plan.json` (SHA-256 `b1cce4963565e850598ed0dce4361077ace6933f74855cfd6b187e9cbb1907db`). The full bounded terminal run was completed in [GitHub Actions run 40641534032](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40641534032) using 3×3 integer determinant geometry and independent 4×4 Bareiss geometry. The output `certificate.json` is a frozen copy of that run, not an inferred upper-layer verdict.

Results: **5 WIN9 / 27 LOSS9**, 128 universal WIN10 edges, 417 ordered first-loss obligations (416 distinct terminal S10 leaves, 84495 terminal recursive states per geometry). WIN9 parents add **42** proof-only WIN8 classes (5407 → 5449); the conditional 14-root unproved S8 edge count falls **100 → 93**. 270 canonical LOSS9 parents follow from the fixed LOSS10 witnesses, without asserting global novelty.

`node research/experiments/n11-s9-post-round8-round9-20261028/verify_compact.js --negative` checks the **necessary and sufficient** frozen certificate obligations: all legal WIN10 children for every WIN9, one terminal LOSS10 witness for every LOSS9, both independent geometries, canonical parent incidence, the parent-closure hash, and proof-only WIN8 propagation. It rejects forged verdicts and out-of-range witness indices. It does not need to replay the original first-loss *search order*; `node research/experiments/n11-s9-post-round8-round9-20261028/prove.js --negative` additionally reproduces that full discovery trace and compares all frozen fields byte-for-byte.

The original full run and frozen verification are bounded S9/S10 proofs, **not** S7/S5 or two-stone root closures. No branch/PR; the empty-board result remains UNKNOWN.
