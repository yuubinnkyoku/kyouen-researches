# 2026-10-28: N11 next 32 S9 roots, two-geometry S10 boundary preflight

After freezing the round11 proof-only 79-edge replan at 638 eligible S9 classes, independently checked the complete S9→S10 boundary of its **32** selected roots. [Preflight CI run 40694409012](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40694409012) **PASS**, commit `1c14fe2a09d60a88c9356254704a861de3683902`.

The reproducible verifier `research/experiments/n11-s9-post-round11-replan-20261028/preflight.js` reads the frozen `next-plan.json`, checks selection SHA-256 `05f4f971ffeeadb9688a64ab5c67cb6eb193ab891bc3c34c7a0a09515190b53a`, requires exactly 32 distinct nine-stone roots, and compares **every** legal ten-stone child from two independent exact integer geometries (3×3 difference determinant and 4×4 integer determinant). It checks the canonical child multiplicities and fails if any expected count differs.

- **807** legal S9→S10 edges, comprising **805** distinct D4-canonical S10 classes.
- Exactly **2** shared S10 child classes, each with two of the 32 selected S9 parents; all remaining 803 child classes occur once.
- Shared children: `000100c00001008210c0000000000020` and `00042000000000821084800000400020`.
- A full universal S10-boundary pass across all 32 roots can therefore save **at most 2/807 ≈ 0.25%** of distinct S10 evaluations from *within-batch* memoization alone. Reuse of earlier batches, or early LOSS10 witness termination, is not bounded by this observation.
- This is a **boundary and geometry** check only: **0** new terminal verdicts, **0** new two-stone root closures. Potential 37-class S8 coverage is not a proof.

Next: bounded terminal certificates only for these 32 fixed S9 candidates, with independent witness verification and proof-only upward propagation. Avoid an unbounded empty-root search.

**Standard 11×11 empty-board winner: UNKNOWN.**
