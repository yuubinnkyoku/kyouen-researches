# N11 round16: bounded 28-root S9 terminal discovery

The successful round15 replan (workflow 40784709162; artifact 12859615577, ZIP SHA-256 `32914e69634cab8b0c01c7314349d6a7998e05f089f4e3461c46742daf5cff3b`) reduced 269 eligible S9 classes to **215**, of which **28** remain undominated. The frozen next plan selects those 28 classes to potentially cover 28 S8 classes in the fixed 14-root plan; the 52 unproved S7-plan edges remain unproved.

A separately implemented Python 3×3 exact determinant + D4 orbit enumeration confirms **728 legal S9→S10 edges, 726 distinct S10 classes and two duplicated children**. The repository `preflight.js` independently replays the same boundary with 3×3 and 4×4 integer determinants, comparing its result to the frozen `preflight.json`. The separate CI must succeed before treating this as repository-verified.

`prove.js` is restricted to these 28 roots. For a WIN9 claim it checks every legal S10 child to terminal with two exact geometries. For a LOSS9 claim it stores a specific independently verified LOSS10 child. It also checks reverse parent incidence and WIN/LOSS conflicts. This is a discovery calculation: any output is **not** an accepted certificate until a separate verifier independently replays the frozen witness bytes.

Run from the repository root:

```sh
node research/experiments/n11-s9-post-round15-replan-20261029/preflight.js
node research/experiments/n11-s9-post-round15-round16-20261029/prove.js
```

No new S7, S5 or two-stone verdict is claimed. **Standard 11×11 empty-board winner: UNKNOWN.**
