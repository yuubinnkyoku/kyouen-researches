# 2026-10-28: N11 round11 candidate preflight has zero within-batch overlap

After the [certified round10 proof-only replan](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40670592328)
selected 32 S9 roots against the fixed 83-edge frontier, a separate
[independent preflight CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40671305642)
**passed**. It checked all 32 canonical safe S9 roots, complete S10
legal-child sets under 3×3 difference-determinant and independent 4×4
integer Bareiss geometry, S8 reverse incidence, selection hash, and
negative tests for duplicate/modified keys and forged empty-board verdicts.

- **822** ordered legal S10 children, **822 distinct** canonical S10
  classes. **Zero** within-batch S10 reuse.
- **288** S8 reverse incidences, **288 distinct** canonical S8 parents.
  **Zero** within-batch S8 overlap.
- The 32 candidates still potentially touch **40** of the **83**
  outstanding conditional S8 classes. This is only planning incidence,
  not a new WIN8 certificate.
- New S9/S8 verdicts **0**, two-stone closures **0**.

The exact fixed preflight result is
`research/experiments/n11-s9-post-round10-replan-20261028/preflight.json`,
checked by `audit_next_batch.js` under a bounded CI. For this selected
batch, a cache shared *only across these 32 roots* cannot save any
S10 terminal leaf if every child is visited. Cross-batch reuse and early
LOSS9 witnesses are distinct effects and were not measured.

**Standard 11×11 empty-board winner: UNKNOWN.**
