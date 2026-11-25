# 2026-10-28: N11 round9 5 terminal WIN9 and 93 remaining conditional edges

Reviewed latest main, AGENTS.md, research/knowledge/README.md, K0023/K0105/K0329, round8 fixed plan, and current N11 experiment/log state. Selected only the 32 classes frozen by the independently checked round8 replan; did not run the enormous empty root.

The [completed bounded run](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40641534032) returned **5 WIN9 / 27 LOSS9** under independently checked 3×3 and 4×4 integer geometry. 417 ordered terminal obligations, 416 distinct S10 leaves, 84495 terminal states per geometry. 128 WIN10 edges establish all universal children for five WIN9. Twenty-seven LOSS9 have explicit LOSS10 witnesses. The full result and witness hashes are frozen in `research/experiments/n11-s9-post-round8-round9-20261028/certificate.json`, and `verify_compact.js` independently rechecks all proof obligations and negative controls.

Proof-only WIN8 **5407 → 5449 (+42)**. The conditional 14-root frontier improves from **100 to 93 unproved S8 edges (−7)**; no WIN/LOSS conflict. The LOSS10 witnesses induce 270 canonical LOSS9 parents, not all claimed globally new. Two-stone roots closed: 0. The 14-root conditional plan is not an empty-root certificate. **N11 empty-board winner UNKNOWN.**

The frozen compact verifier avoids repeating the first-loss scan: it needs at most 128+27=155 terminal child obligations instead of 417; it still recomputes both geometries and every necessary WIN/LOSS witness. This is a verifier work bound, not a measured runtime claim.

Frozen independent verifier [CI run 40642259972](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40642259972) **PASS**, including forged-WIN/LOSS and out-of-range witness rejection. It recomputed 155 distinct S10 terminal leaves (155 obligations) and 27,384 terminal recursion states per geometry, compared with 416 leaves and 84,495 states in the full first-loss discovery trace: **62.7% fewer distinct leaves and 67.6% fewer terminal states**. These are replay-work reductions, not an end-to-end wall-clock speedup claim. No extra upper-layer verdicts were inferred from verifier counts.
