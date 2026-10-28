# N11 round13: bounded terminal certificates for 32 selected S9 roots

The proof-only round12 replan independently reconstructed **423** eligible S9 classes (from **638**), reduced the incidence-dominance candidate set to **51**, and froze a selection of **32** roots with potential coverage of **34** of the fixed 14-root plan's **64** unproved S8 edges. Potential incidence is not a verdict.

The independent boundary audit of that selection passed [CI 40722986586](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40722986586): **802** legal S10 edges, **801** distinct S10 classes, exactly **1** shared child across the selected roots. The frozen selection and boundary audit are in `../n11-s9-post-round12-replan-20261029/next-plan.json` and `preflight.json`.

`prove.js` processes **only those 32 roots**. It checks the frozen prior terminal certificate, selection hashes and boundary census, then computes each required S10 terminal verdict with the 3×3 difference determinant and independent 4×4 integer determinant. A LOSS9 certificate records a specific LOSS10 child; a WIN9 certificate requires all legal S10 children to be WIN. It also independently checks reverse parent incidence and detects WIN/LOSS contradictions. The bounded workflow writes its result to a downloadable artifact; **an uncompleted or timed-out run is not a proof**.

From the repository root:

```sh
node research/experiments/n11-s9-post-round12-round13-20261029/prove.js > round13-certificate.json
```

## Verified result (2026-10-29)

[Discovery run 40723296898](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40723296898) succeeded. The artifact's JSON is frozen as `certificate.json`, with the original 32-root selection and witness SHA-256. Exactly **4 WIN9** and **28 LOSS9** were proved, with **100** WIN10 child obligations for the four WIN9 roots. Discovery evaluated **307** distinct S10 leaves and **49,755** terminal recursive states per exact geometry; the 28 LOSS10 witnesses yield **280** canonical LOSS9 parents.

[Independent verification run 40733280615](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40733280615) **PASS**, including forged-witness rejection and full replay equality. The compact verifier needs **128** distinct S10 terminal leaves and **22,180** recursive states per geometry, **58.3%** and **55.4%** fewer respectively than discovery. These are terminal-recomputation counts, not elapsed-time speedups.

The upward proof-only lift is implemented in `lift.js`; any WIN8 and conditional-plan coverage changes must be independently checked before being counted. No two-stone root was closed by this terminal batch.

**Standard 11×11 empty-board winner: UNKNOWN.**
