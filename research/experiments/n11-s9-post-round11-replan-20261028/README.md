# N11 round11: certificate-only replan against 79 conditional S8 edges

The independently verified round11 terminal certificate proves 4 WIN9 and 28 LOSS9; its proof-only lift raises WIN8 from **5,513 to 5,545** and reduces the *fixed* conditional 14-root S7 plan from **83 to 79** unproved S8 edges. These are not two-stone or empty-board verdicts.

`replan.js` independently replays the minimal round11 terminal obligations with 3×3 and 4×4 exact integer geometry and forged-witness negative controls. It checks all three successive terminal certificate identities and loss-witness parent closures, reconstructs the previously frozen 709 eligible S9 candidates, excludes the 32 selected round11 roots and all newly derived certified LOSS9 parents, then removes candidates that no longer touch the 79 unproved S8 edges. A deterministic incidence-dominance filter and bounded greedy/exchange optimization choose at most 32 further S9 candidates.

Run from the repository root:

```sh
node research/experiments/n11-s9-post-round11-replan-20261028/replan.js
```

The [bounded workflow](https://github.com/yuubinnkyoku/kyouen-researches/actions/workflows/n11-s9-post-round11-replan.yml) checks the result in CI (15-minute limit) and uploads the exact JSON. After independent verification, freeze that output in `next-plan.json` so future runs reject mismatches. A launched job is not a completed proof or a measured improvement. Potential incidence is not a WIN verdict.

**Standard 11×11 empty-board winner: UNKNOWN.**
