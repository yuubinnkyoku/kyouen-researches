# 2026-10-28: N11 round9 proof-only replan, eligible S9 1011 to 890

Reviewed current main, AGENTS.md, knowledge README, K0023/K0414, round8 fixed plan, round9 frozen terminal certificate, and earlier cross-batch LOSS9 closures. The bounded [CI run 40648005327](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40648005327) **PASS** independently checked all 32 S9 claims using 3x3 and 4x4 integer geometries: five WIN9 with all S10 children, 27 LOSS9 with a terminal LOSS10 witness each. Recomputed 155 distinct S10 leaves and 27,384 terminal recursion states per geometry. The 270 derived LOSS9 parents were checked for legal incidence and SHA-256 equality with the fixed round9 certificate. WIN/LOSS conflicts: zero.

Proof-only WIN8 remains **5449** (round9's already certified +42), and the conditional 14-root S8 frontier remains **93 unproved edges**. No new S7/S5 or two-stone verdicts.

The old eligible S9 census was **1011**. Round9 proof excludes **50**: the 32 selected classes and **18 additional** LOSS9 parents. Of the 961 remaining, **71** no longer touch any of the 93 unproved S8 classes after round9's WIN8 propagation. Thus eligible S9 classes are **890** (1011 - 50 - 71). Dominance pruning leaves **125**, versus 156 in the previous 100-edge plan.

The next 32-class proposal has **43 potential** distinct S8 hits and **830** legal S10 children. The previous proposal's 47 hits and 842 children targeted a different frontier and are not proof gains or measured speedups. Selection SHA-256: `42702f97100ee62a07d6c0603409ac17a19f8db47c8bf3039083c8e8fced3299`. The exact machine-readable output is frozen in `research/experiments/n11-s9-post-round9-replan-20261028/next-plan.json` and compared byte-for-byte against re-computation in CI.

This is a verified candidate reduction and proof reuse, not a new upper-layer terminal verdict. Standard 11x11 empty-board winner **UNKNOWN**.
