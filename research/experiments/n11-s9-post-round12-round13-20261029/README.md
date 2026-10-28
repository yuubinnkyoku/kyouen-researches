# N11 round13: bounded terminal certificates for 32 selected S9 roots

The proof-only round12 replan independently reconstructed **423** eligible S9 classes (from **638**), reduced the incidence-dominance candidate set to **51**, and froze a selection of **32** roots with potential coverage of **34** of the fixed 14-root plan's **64** unproved S8 edges. Potential incidence is not a verdict.

The independent boundary audit of that selection passed [CI 40722986586](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40722986586): **802** legal S10 edges, **801** distinct S10 classes, exactly **1** shared child across the selected roots. The frozen selection and boundary audit are in `../n11-s9-post-round12-replan-20261029/next-plan.json` and `preflight.json`.

`prove.js` processes **only those 32 roots**. It checks the frozen prior terminal certificate, selection hashes and boundary census, then computes each required S10 terminal verdict with the 3×3 difference determinant and independent 4×4 integer determinant. A LOSS9 certificate records a specific LOSS10 child; a WIN9 certificate requires all legal S10 children to be WIN. It also independently checks reverse parent incidence and detects WIN/LOSS contradictions. The bounded workflow writes its result to a downloadable artifact; **an uncompleted or timed-out run is not a proof**.

From the repository root:

```sh
node research/experiments/n11-s9-post-round12-round13-20261029/prove.js > round13-certificate.json
```

After a successful run, independently verify the compact witness and freeze the certificate before lifting WIN9 to WIN8. Neither a successful batch nor its prospective coverage implies a two-stone root or the empty-board verdict.

**Standard 11×11 empty-board winner: UNKNOWN.**
