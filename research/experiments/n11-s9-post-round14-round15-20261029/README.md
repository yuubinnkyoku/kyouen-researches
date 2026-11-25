# N11 round15 bounded terminal discovery

Consumes the **frozen and independently verified** post-round14 32-root plan, whose legal S10 boundary consists of 814 edges / 812 distinct S10 classes. This is a targeted terminal experiment, not an unbounded root search.

`prove.js` checks the round14 certificate linkage, frozen preflight, every selected S9→S10 boundary in two integer geometries, and every S10 terminal leaf used for a WIN9 universal proof or LOSS9 witness. It caches duplicate S10 terminal leaves within this run and derives reverse LOSS9 parents only from independently checked LOSS10 witnesses. A WIN/LOSS conflict aborts the run.

The output is an **unfrozen discovery candidate** until independently replayed by a separate verifier and fixed as `certificate.json`. The discovery run by itself is not an accepted new verdict. No S7, S5, two-stone, or empty-board verdict is implied.

Run from the repository root:

```sh
node research/experiments/n11-s9-post-round14-round15-20261029/prove.js
```

**Standard 11×11 empty-board winner: UNKNOWN.**
