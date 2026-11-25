# N11 proof-only replan after round13

This directory contains a bounded deterministic coordinator for the fixed conditional 14-root S7 plan. It **does not** perform unbounded root search and does not infer a winner from incidence, incomplete df-pn counts, or potential coverage.

`replan.js` independently replays the frozen round13 32-root terminal certificate (including forged-witness rejection and two integer geometries), verifies the full round9–round13 proof chain, reconstructs the certified WIN8 frontier and LOSS9 witness-parent closures, and then filters only S9 candidates incident to the *remaining* unproved S8 edges. It removes the 32 selected round13 roots, every additional certified LOSS9 parent, and candidates no longer touching an unproved edge. The remaining options are dominance-pruned and the deterministic 32-root coordinator selects the next bounded batch.

It requires a **verified and frozen** `../n11-s9-post-round12-round13-20261029/lift.json` before running. Once that prerequisite is available, run from the repository root:

```sh
node research/experiments/n11-s9-post-round13-replan-20261029/replan.js
```

Freeze the exact result as `next-plan.json` only after a successful independent run. Subsequent runs reject any mismatch. Selection and potential S8 coverage are *not* terminal proofs, and no two-stone root is closed by this coordinator alone.

**Standard 11×11 empty-board winner: UNKNOWN.**
