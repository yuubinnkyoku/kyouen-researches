# N11 round12: certificate-only replan against 64 conditional S8 edges

The independently verified round12 terminal certificate proves **12 WIN9 / 20 LOSS9** among 32 selected roots. Its proof-only lift increases certified WIN8 from **5,545 to 5,643** and reduces the *fixed* conditional 14-root S7 plan from **79 to 64** unproved S8 edges. Neither figure proves an S7 root, a two-stone root, or the empty board.

`replan.js` replays the round12 compact terminal certificate with independent 3×3 and 4×4 integer geometry, including forged-witness rejection. It checks the round9–12 witness chain, WIN8 lift and all LOSS10-to-LOSS9 parent closures. It reconstructs the frozen **638** eligible S9 classes, removes the 32 selected round12 roots and all newly certified LOSS9 parents, then discards candidates no longer incident to the 64 unproved S8 edges. A deterministic dominance filter and bounded greedy/exchange planner choose at most 32 new S9 candidates.

From the repository root:

```sh
node research/experiments/n11-s9-post-round12-replan-20261029/replan.js
```

The bounded CI workflow checks this reconstruction and uploads exact JSON. After independent verification, freeze that output in `next-plan.json`; when present, the script checks exact equality and fails closed on a mismatch. Potential incidence is not a WIN proof. Do not infer success from a launched CI run.

**Standard 11×11 empty-board winner: UNKNOWN.**
