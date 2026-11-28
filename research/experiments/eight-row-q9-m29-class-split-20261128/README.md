# Eight-row q=9, 8x29 class-split continuation + transplant surgery (2026-11-28 fast lane)

Single-owner lane declared in
`research/log/2026-11-28-eight-row-q9-m29-class-split-declaration.md`
(declaration commit `c7bac259`, declaration-time HEAD `9def0879`) with
amendment 1 (`research/log/2026-11-28-eight-row-q9-m29-class-split-amendment1.md`,
commit `6e1282c3`, published before the deeper-krow probes). Family
(w,q)=(8,9): witness band 8x9..8x28, M_{8,9} in [29,984], frontier 8x29.
Continues `eight-row-q9-m29-row-split-20261128` (rowY=2 UNSAT, classes
{2}/{5} witness-free; rowY=3/0/1 and class {3} krow=3:7 minpos 0/1 INDET).

## Results

Class-split pieces (sat3.js class/krow/minpos encoding, kissat 4.0.4,
280 s caps), all INDET honest negatives — not absence:

- 8x29 class {3} krow=3:7 minpos=2: INDET 5,255,794 (pre-reset same-instance
  observation 5,791,302)
- 8x29 class {3} krow=3:7 minpos=3: INDET 5,048,319
- 8x29 class {0} krow=0:7 minpos=0: INDET 4,529,434 (first evaluation of
  class {0}; pre-reset 4,951,432)
- 8x29 class {0} krow=0:7 minpos=1: INDET 4,502,209
- 8x29 class {1} krow=1:7 minpos=0: INDET 5,635,529 (first evaluation of
  class {1}; pre-reset 6,175,273)
- amendment-1 deeper-deficiency probes: class {3} krow=3:6 minpos=0 INDET
  4,950,721 (pre-reset 5,639,066); class {3} krow=3:5 minpos=0 INDET
  5,235,559 (pre-reset 5,778,289)

The remaining single-deficiency 8x29 class-split pieces (class {3} p=4..13,
class {0} p=2..13, class {1} p=1..13, krow=c:6/c:5 minpos extensions) stay
unswept (280 s caps show near-uniform 4.5-5.7M conflict resistance across
every decomposition tried so far; heavier caps exceed this container's
piece limit).

## Transplant surgery at 8x29 (new decomposition)

Both published 8x28 63-stone witnesses (the m29-row-split kit's
`s8x28q9_rowY3.witness.json` and the D4-distinct `witness_c3k37p1_28.json`)
were placed on 8x29 at every placement (2 seeds x 4 D4 images x 2 x-shifts
= 16 placements; full-span seeds admit only shifts 0/1) and analyzed with
the census machinery of the pinned sat.js (curves with >= 9 board points;
safety = no curve with 9 stones, maximality = every free cell on a curve
with 8 stones):

- **Every placement is SAFE on 8x29 with EXACTLY ONE unblocked cell** —
  (28,3) at shift 0 / (0,3) at shift 1 for row-preserving images of the
  class-{3} seeds, (28,4)/(0,4) for the V-flipped (class-{4}) images. The
  one-stone-short structure, same type as (7,8) 7x25->7x26 and (5,6)
  m=22->5x23.
- **The unique add-one completion at that cell is a FULL 64-stone maximal
  safe configuration** (rows [8,8,8,8,8,8,8,8]): the first maximal
  configuration ever constructed at 8x29. jsVerify (sat.js verifyConfig)
  PASS on all 16 completions; pyVerify (exact-Fraction verify_witness.py)
  runs through safety and maximality and stops only at its built-in
  deficiency assert — i.e. safety+maximality are independently confirmed
  and the config is full, hence NOT a deficient witness. The short cell is
  in the deficient row, so the completion necessarily destroys deficiency.
- **Bounded-edit deficient-witness search: complete negative.** Around
  every placement the edit classes (1,0) [63], (2,0) [1953], (1,1)
  [10,647 screened / 1,314 z-safe], (2,1) [330,456 screened / 75,842
  (seed0) or 75,128 (seed1) safe] were fully enumerated per placement
  (fail-closed: every screened-maximal candidate must pass verifyConfig or
  the run aborts; 0 maximal, 0 witnesses, 0 false positives). So **no 8x29
  deficient maximal witness exists within (<=2 removals, <=1 addition) of
  any placement of either published 8x28 witness** — a local negative, not
  absence. The (2,2) class (28M configs/placement) is unswept.

## Controls

- Calibration (pre-registered): 8x28 class {3} krow=3:7 minpos=1 SAT
  **3,013,059 conflicts bit-exact** with the published value — reproduced
  twice in this lane, once before and once after a full execution-
  environment reset (136 s / 151 s wall). CNF regeneration x2
  byte-identical.
- Census-screening control: the identical screening path reproduces both
  8x28 seeds as safe+maximal on the 8x28 board (unsafe=0, unblocked=0,
  verifyConfig ok, size 63, rows [8,8,8,7,8,8,8,8]).
- 12-sample pyVerify cross-check: deterministic samples of swap(1,1) and
  (2,1) candidates that the screening rejects as not-maximal are
  independently confirmed not-maximal by the exact-Fraction verifier
  (12/12 agree, 0 false negatives in the sample).
- Determinism: probe2/probe3 reruns identical (probe2 logs differ only in
  the wall-time `ms` field; probe3 stripped-JSON reruns byte-identical);
  cross-reset reproduction of every screening count (1314 z-safe, 75,842 /
  75,128 (2,1)-safe, add-one 1/16 placements, 0 hits).

## Toolchain

- Scripts VERBATIM from
  `research/experiments/eight-row-q9-m29-row-split-20261128/scripts`
  (sat.js fcc0cfd8..., sat2.js 14ceb854..., sat3.js e04581eb...,
  genfast.js 409b5216..., decode_verify.js bf64e428...,
  verify_witness.py 298ff590..., sha-verified at commit 1e813043).
- Fresh scripts: probe2.js / probe3.js / probe_ctrl.js (census screening +
  bounded-edit surgery), run1.sh (piece runner). Witness seed jsons are
  byte-clones of the published m29-row-split kit outputs
  (s8x28q9_rowY3.witness.json, witness_c3k37p1_28.json) — not republished
  here; fetch from that kit.
- kissat 4.0.4 official linux-amd64, sha256 21da5d984e38b74f620f14c62442f
  834f27b9158decdb722540d97f98aac93a1 (pinned binary, not redistributed).

## Disclosure

- One mid-lane execution-environment reset (the known artifact-save
  failure mode) lost the first-pass working tree, including the raw logs
  of the pre-reset piece runs. All raw logs published here are post-reset
  reruns. Deterministic verdicts reproduced exactly (calibration SAT
  3,013,059 bit-exact across the reset; every probe screening count
  identical); INDET wall-clock-cut conflict counts are host-dependent and
  both observations are disclosed per piece in `output/records.jsonl`.
- CNFs are deterministically regenerable and not published (size policy).

## Scope and non-claims

- No absence claim at 8x29 overall: classes {2}/{5} remain the only decided
  witness-free classes; classes {0}/{1}/{3} stay INDET-undetermined at
  these caps; multi-deficiency classes remain unswept; the surgery
  negative is local (bounded edit distance from two known witnesses).
- M_{8,9} stays in [29,984]; the frontier stays 8x29.
- Standard 11x11 empty board, 19 central-reply roots, two-stone root
  {60,27}, third move {100,108}, S2, closure classes: UNKNOWN at all
  times; verdicts not consumed; conflicts are bookkeeping.

## Files

- `scripts/`: fresh probe/runner scripts.
- `output/`: raw kissat logs + meta jsons + calibration log, records.jsonl,
  probe result jsons, control sample candidates, the completion config.
- `MANIFEST-sha256.txt`.
