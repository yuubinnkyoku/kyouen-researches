# 2026-10-29: N11 round12 proof-only replan, 638 → 423 eligible S9 classes

Reviewed latest main (including unrelated coplanar results), AGENTS.md, research/knowledge/README.md, K0023, the round12 terminal certificate and lift, and the new round12 replan implementation. Recovered the completed [round12 replan CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40713128765), **PASS** at commit `ad08d97d73fd36dd646a3d5a4440f17196fbbd93`. The exact JSON appeared in the successful job log and was uploaded as artifact `n11-round12-proof-only-64-edge-replan` (ID `12826943358`, ZIP SHA-256 `43580d92ed394eb4ca09a7a104565cd5fdfa64bb74723753f7a695cecf21c6da`). No branch or PR was created.

The bounded script independently replayed the round12 compact terminal certificate with two exact integer geometries and forged-witness rejection, verified prior witness hashes and LOSS10-to-LOSS9 parent closures, and reconstructed the 638 eligible candidates. It then applied only certified exclusions and incidence pruning:

- Before round12: **638** eligible S9 classes.
- Proof exclusions: **36** (32 selected round12 roots and 4 additional certified LOSS9 parents).
- Remaining after proof exclusions: **602**.
- No longer incident to the fixed plan's 64 unproved S8 edges: **179**.
- Still eligible: **423** (215 fewer, **33.7%** reduction from 638).
- Deterministic incidence-dominance reduction: **51** candidate classes.
- Next 32 selected S9 roots potentially cover **34** of 64 unproved S8 classes; **802** legal S10 child edges. The exchange stage made **0** swaps. These are prospective coverage and legal edges, not a winner proof.
- Proof-only WIN8 remains **5,643**; fixed conditional 14-root S7 plan remains **548** edges, **484** secured and **64** unproved. No WIN/LOSS conflicts, no new S7/S5 verdicts, no new two-stone closures.

The complete ordered selection and SHA-256 `41c3f7d019848012f37bb27e1aaf60773a577fe21b9aac2f025f0093cc3c1d64` were frozen in `research/experiments/n11-s9-post-round12-replan-20261029/next-plan.json`. The replan script now checks exact equality with a fresh reconstruction; the path-triggered post-freeze CI is [run 40722919387](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40722919387). Its result must be checked, not presumed.

An independent two-geometry S9→S10 boundary preflight was added as `preflight.js` with a bounded [workflow](https://github.com/yuubinnkyoku/kyouen-researches/actions/workflows/n11-s9-post-round12-preflight.yml). It checks all 32 roots, their exact legal children, the selected-key hash, and the total 802 edges, and reports cross-root sharing. Its [first run 40722986586](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40722986586) **PASS**: **802** legal S10 edges, **801** distinct S10 classes, **1** cross-root duplicate (child `0000a000000000821080000400000038`, shared by the roots ending in `...028` and `...030`). Both exact integer geometries agree on every selected root. The output is frozen in `research/experiments/n11-s9-post-round12-replan-20261029/preflight.json`; the subsequent path-triggered CI must separately confirm the frozen equality. The one duplicated child saves at most 1/802 ≈ 0.125% of terminal work if all children are evaluated, excluding reuse against earlier batches.

Next: recover both CI outcomes, freeze independently verified preflight output, then run bounded terminal certificates for precisely the 32 selected roots. Avoid unbounded root runs and treating potential incidence, pn/dn or partial searches as outcomes.

**Standard 11×11 empty-board winner: UNKNOWN.**
