# Six-row q=5, 6x32: SAT-side class-split direct evaluation (2026-11-28 fast lane)

Single-owner lane declared in
`research/log/2026-11-28-six-row-q5-m32-class-split-declaration.md`
(declaration commit `ed37b8ab`, declaration-time HEAD `5cc8e1fb`).

## Status: IN PROGRESS (batch 1 published)

Batch 1 covers class {0} (deficient row 0, V-canonical class {0,5}), single
deficiency krow=0:3 (exactly q-2 = 3 stones in the deficient row), minpos
p = 0..15 (the m=32 sound H-split, floor((m-1)/2) = 15). Every piece is
INDET at the 275s cap — near-uniform frontier resistance
(1,290,389 .. 1,594,220 conflicts), the same wall shape as the 6x23 q7 /
6x26 q6 / 7x28 q7 frontiers. Honest negatives, NOT absence.

Classes {1} and {2} and deeper deficiency (k <= 2) are unswept so far.

## Controls

- **6x28 class {0} krow=0:3 positive control: SAT** (1,215,854 conflicts /
  219.88s, pre-reset first observation; dual-verified: sat.js `verifyConfig`
  ok, 23 stones rows [3,4,4,4,4,4]; fresh `scripts/verify_frac.py` safe
  (max curve 4 = q-1) + maximal (0 unblocked)). The control raw log was lost
  to the execution-environment reset disclosed below and is regenerated in a
  later batch.
- **6x31 class {0} krow=0:3 declared control resisted the 275s cap**
  (INDET 1,317,564 conflicts, pre-reset observation, raw lost) — disclosed as
  an honest negative; the 6x28 SAT control is the validated positive control.
- kissat 4.0.4 official linux-amd64 binary, sha256
  `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`.
- Scripts are byte-clones of the published
  `six-row-q7-m22-class-split-20261127` kit (sha256 pins in its MANIFEST;
  re-verified after the reset: fcc0cfd8… sat.js / 14ceb854… sat2.js /
  e04581eb… sat3.js / 837fe24b… verify_frac.py).

## Honest disclosures

- One execution-environment reset (Koyeb artifact-save failure) destroyed the
  working tree after class {0} minpos=9 had run; pieces p0..p9 raw logs and
  both control raws are pre-reset observations recorded in this README and in
  `output/records.jsonl` (`reset: pre` marker); p10..p15 raws were generated
  post-reset from re-fetched byte-identical scripts and the re-downloaded
  pinned kissat binary. Raw logs for p0..p9 and the controls are queued for
  regeneration in a later batch (kissat determinism on this host makes the
  conflicts counts expected to reproduce bit-exactly).
- No piece has been found SAT so far; no witness claim; M_{6,5} ∈ [32, 658]
  unchanged (K1216); no absence claim at 6x32 (INDET is not absence).
- conflicts are bookkeeping. Standard 11x11 empty board, two-stone root
  {60,27}, third move {100,108}, S2, all closure classes: UNKNOWN at all
  times; verdicts not consumed.

## Reproduce

```sh
node scripts/sat3.js 6 32 5 --class=0 --krow=0:3 --minpos=P cnf/x.cnf
timeout 275 ./kissat-4.0.4-linux-amd64 cnf/x.cnf
```
