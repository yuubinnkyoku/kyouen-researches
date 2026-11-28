# 2026-11-28 eight-row q9 8x29 class-split continuation + transplant surgery — completion log

Declaration: `research/log/2026-11-28-eight-row-q9-m29-class-split-declaration.md`
(commit `c7bac259`, declaration-time HEAD `9def0879`) + amendment 1
(`research/log/2026-11-28-eight-row-q9-m29-class-split-amendment1.md`,
commit `6e1282c3`, published before the deeper-krow probes). Kit:
`research/experiments/eight-row-q9-m29-class-split-20261128/`. CSV (8,9)
row note updated.

## What was measured (all publish-then-execute, after the declaration)

- Calibration (pre-registered): 8x28 class {3} krow=3:7 minpos=1 cold
  rerun SAT **3,013,059 conflicts, bit-exact with the published value** —
  reproduced twice, once before and once after a full execution-environment
  reset (wall 136 s / 151 s, host-dependent). CNF regeneration x2
  byte-identical.
- Class-split pieces at 8x29, 280 s caps, all INDET honest negatives:
  class {3} krow=3:7 minpos=2 (5,255,794; pre-reset 5,791,302),
  minpos=3 (5,048,319), class {0} krow=0:7 minpos=0 (4,529,434; pre-reset
  4,951,432 — first class-{0} evaluation), minpos=1 (4,502,209),
  class {1} krow=1:7 minpos=0 (5,635,529; pre-reset 6,175,273 — first
  class-{1} evaluation); amendment-1 deeper-deficiency probes class {3}
  krow=3:6 minpos=0 (4,950,721; pre-reset 5,639,066) and krow=3:5
  minpos=0 (5,235,559; pre-reset 5,778,289).
- **Transplant surgery (new decomposition for the uniformly-resistant
  8x29 frontier)**: both published 8x28 witnesses, all 16 placements
  (2 seeds x 4 D4 images x 2 shifts), census screening
  (safe = no >=9-stone curve; maximal = every free cell on an 8-stone
  curve):
  - every placement is **safe with exactly ONE unblocked cell** —
    (28,3)/(0,3) for row-preserving images, (28,4)/(0,4) for V-flipped —
    the one-stone-short structure;
  - the unique add-one completion at that cell is a **full 64-stone
    maximal safe configuration** (rows [8,8,8,8,8,8,8,8]), jsVerify PASS
    on all 16, pyVerify (exact Fraction) passes safety+maximality and
    stops only at its built-in deficiency assert (full, so not a
    deficient witness) — the first maximal configuration ever
    constructed at 8x29;
  - bounded-edit deficient-witness search around all 16 placements,
    complete negative: (1,0)=63, (2,0)=1953, (1,1)=10,647 screened /
    1,314 z-safe, (2,1)=330,456 screened / 75,842 (seed0) / 75,128
    (seed1) safe per placement — 0 maximal, 0 witnesses, fail-closed
    (every screened-maximal candidate must pass verifyConfig or the run
    aborts; 0 false positives). **No 8x29 deficient maximal witness
    within (<=2 removals, <=1 addition) of any placement of either
    published 8x28 witness.** Local negative, not absence; (2,2)
    unswept.
- Controls: census screening reproduces both 8x28 seeds safe+maximal on
  the 8x28 board; 12-sample pyVerify cross-check of screening-rejected
  candidates agrees not-maximal (12/12); probe reruns identical
  (probe2 logs differ only in the wall `ms` field; probe3 stripped-JSON
  reruns byte-identical); every screening count reproduced across the
  environment reset.

## Bottom line

M_{8,9} stays in [29,984]; the frontier stays 8x29. Absence at 8x29 is
decided only for the single-deficiency row classes {2}/{5}; classes
{0}/{1}/{3} stay INDET-undetermined at 280 s caps (near-uniform 4.5-5.7M
conflict resistance across every decomposition tried: direct rowfixed,
lex=H cross-encoding, class/krow/minpos splits, deeper deficiency);
multi-deficiency classes remain unswept — no overall absence claim. The
surgery result is a bounded local negative plus the structural
observation that both frontier witnesses are one-stone-short at 8x29 and
complete to full (non-deficient) there.

## Disclosures

- One mid-lane execution-environment reset (known artifact-save failure
  mode) lost the first-pass working tree including the pre-reset raw
  logs; all published raws are post-reset reruns. Deterministic verdicts
  (calibration SAT) and every screening count reproduced exactly across
  the reset; INDET wall-clock-cut conflict counts are host-dependent and
  both observations are disclosed per piece in the kit records.jsonl.
- CNFs are deterministically regenerable and not published (size policy).
- 11x11 empty board, 19 central-reply roots, two-stone root {60,27},
  third move {100,108}, S2, closure classes: UNKNOWN at all times;
  verdicts not consumed; conflicts are bookkeeping.

## Resume notes (next execution)

- Re-fetch latest main before starting (hourly parallel runs).
- 8x29 remaining: class {3} p=4..13, class {0} p=2..13, class {1}
  p=1..13, krow=c:6/c:5 minpos extensions, multi-deficiency classes —
  all need heavier caps (beyond this container's 280 s piece limit) or a
  smarter decomposition; the transplant surgery (2,2) class (~28M
  configs/placement) is enumerated-able in a longer session.
- The one-stone-short + full-completion structure suggests any 8x29
  deficient witness is >= (2,2)-far from both known 8x28 witnesses,
  consistent with the large consecutive-width witness jumps measured in
  the five-row family (sd=28 at m=21->22).
- Standard 11x11 non-claims unchanged.
