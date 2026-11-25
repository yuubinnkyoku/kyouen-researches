# N11 proof-only replan after round14

The deterministic coordinator independently verifies the frozen round14 terminal certificate and round9–14 proof chain. It does **not** use unfinished df-pn counts as verdicts, and does not search a giant root.

The successful [round14 replan workflow](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40761294714) produced artifact 12849336028 (ZIP SHA-256 `d22e4fb67432f3b5bb7d409352c43750612591067597a6f614e6fb2c28851413`). Its exact structured output is frozen as `next-plan.json`.

Of 338 previously eligible S9 classes, 32 selected roots and 4 additional proven LOSS9 parents are excluded, then 33 no-longer-relevant candidates are dropped. This leaves **269 eligible classes**, **34 undominated options**, and the next **32 selected S9 classes** (SHA-256 `8ecdb3519e14352d03a8103f40ed81950030ca72461d53603e372a2ae469f0f6`). Their potential S8 coverage is 32 classes; this is **not a proof**. The fixed conditional 14-root plan still has **55 unproved edges**. Certified WIN8 remains **5,715 classes**.

The separate `preflight.js` checks every legal S9→S10 move using both the 3×3 difference determinant and independent 4×4 integer Bareiss determinant. Its `preflight.json` records **814 legal S10 edges, 812 distinct S10 classes, and two shared child classes**. The frozen values are checked against an independently implemented Python 3×3 geometry enumeration and are subject to repository CI replay.

From repository root:

```sh
node research/experiments/n11-s9-post-round14-replan-20261029/replan.js
node research/experiments/n11-s9-post-round14-replan-20261029/preflight.js
```

No S7/S5/two-stone root was closed. **Standard 11×11 empty-board winner: UNKNOWN.**
