# N11 round14 bounded terminal certificate

The frozen [round13 proof-only replan](../n11-s9-post-round13-replan-20261029/next-plan.json) selects exactly 32 canonical nine-stone roots from 338 eligible classes incident to the 60 still-unproved conditional S7-plan edges. Independent [preflight](../n11-s9-post-round13-replan-20261029/preflight.json) confirms 798 legal S10 edges and 797 distinct S10 classes with two integer geometries.

`prove.js` searches **only** those 32 S9 roots. Every evaluated S10 child is terminal-solved with independent 3×3 difference-determinant and 4×4 integer-determinant geometry; an S9 LOSS uses one exact S10 LOSS witness, while S9 WIN requires all its S10 children WIN. No inference is made from unfinished df-pn counts.

Run from the repository root:

```sh
node research/experiments/n11-s9-post-round13-round14-20261029/prove.js > round14-certificate.json
```

Freeze `certificate.json` only after successful discovery and independently replay with `verify_compact.js --negative`. The latter rejects forged witness polarity and invalid indices. Do not record a new WIN9/LOSS9, WIN8, S7, S5, or two-stone verdict until the relevant independent certificate has passed. An upward WIN8 lift must separately check prior evidence, conflicts, and conditional edge coverage.

**Standard 11×11 empty-board winner: UNKNOWN.**
