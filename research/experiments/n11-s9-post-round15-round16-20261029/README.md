# N11 round16: independently verified 28-root S9 terminal proof

The [round15 replan CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40784709162) reduced 269 eligible S9 classes to **215**, with **28 undominated**. The frozen `next-plan.json` selects all 28, covering 28 S8 classes **only prospectively**. The [boundary preflight CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40792078270) verified 728 legal S9→S10 edges, 726 distinct S10 classes, and two shared children, using independent 3×3 and 4×4 exact integer geometry. A separate Python 3×3/D4 enumeration reproduced the same counts.

The [bounded terminal discovery CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40792147135) produced a 28-byte witness vector: **3 WIN9 and 25 LOSS9**. Its 332 distinct terminal leaves required 62,406 recursive states per geometry. The fixed `certificate.json` is linked to the frozen selection and prior certificate by SHA-256. Artifact 12861528445 has ZIP SHA-256 `6fde50266dad5f47d13b08bcc0f084fe2d78bf1e38b7ee6a27d05af4c23a6cb5`.

The [independent compact verification CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40792279382) succeeded, including forged WIN/LOSS and invalid witness rejection. It recomputed **104 terminal leaves and 24,643 states per geometry**, with the same two exact geometries and no WIN/LOSS conflict. Artifact 12862700188 has ZIP SHA-256 `feec8a12d28e8b4b483452e5ef2e4158cc58b4bb7a9ddbe987afd25430b57e8a`.

The [proof-only WIN8 lift CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40792393484) independently replayed the certificate and rebuilt the round7–16 proof frontier. Three WIN9 yielded 27 distinct WIN8 parents, 24 new beyond the previous 5,739. The frozen `lift.json` records **5,763 proof-only WIN8** and **499/548 secured edges**, leaving **49 unproved edges** in the fixed 14-root conditional plan. Artifact 12861579549 has ZIP SHA-256 `560ef4a6cb545a6ef804841ee10a9364b6be17492778ba5958ebe55c4f1869bf`.

From repository root:

```sh
node research/experiments/n11-s9-post-round15-round16-20261029/prove.js
node research/experiments/n11-s9-post-round15-round16-20261029/verify_compact.js --negative
node research/experiments/n11-s9-post-round15-round16-20261029/lift.js
```

No new S7, S5 or two-stone verdict is claimed. The 49 missing conditional edges are not a lower bound for an optimized plan. **Standard 11×11 empty-board winner: UNKNOWN.**
