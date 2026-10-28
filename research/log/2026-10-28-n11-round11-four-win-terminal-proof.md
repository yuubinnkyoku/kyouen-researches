# 2026-10-28: N11 round11, four WIN9 and twenty-eight LOSS9 terminal certificates

Reviewed latest main, AGENTS.md, research/knowledge/README.md, K0105, K0414, and the round10 replan and independent round11 preflight. The frozen 32 S9 candidates had 822 distinct S10 children and no within-batch overlap. No branch or PR was created.

Executed bounded exact minimax of the 32 selected S9 positions to terminal with the existing independent 3×3 difference-determinant and 4×4 Bareiss integer geometry implementations, checking every visited S10 terminal result and complete S9 child boundary in both. Obtained **4 WIN9 / 28 LOSS9**, **320 unique terminal S10 leaves**, **57,384 terminal recursion states per geometry**, **96** universal WIN10 obligations, and **280** distinct canonical LOSS9 parents of the fixed LOSS10 witnesses. WIN9/LOSS9 conflicts **0**.

Frozen witness list, SHA-256 digests, deterministic replay and minimal independent verifier:
`research/experiments/n11-s9-post-round10-round11-20261028/`.
CI workflow: `.github/workflows/n11-s9-post-round10-round11-verify.yml`. Its status is to be checked separately; no CI success is assumed from creating the workflow.

The 280 LOSS9 parents may overlap earlier certificates. The four WIN9 roots potentially imply at most 36 WIN8 parents, but the number **new** relative to the previously proved 5,513 WIN8 classes and the 83 outstanding edges has **not** yet been audited. Do not add them to either count until the proof-only union is recomputed. No S7/S5/two-stone root was closed in this run. Do not interpret potential incidence as proof.

**Standard 11×11 empty-board winner: UNKNOWN.**
