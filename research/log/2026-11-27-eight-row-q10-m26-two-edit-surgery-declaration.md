# 2026-11-27 Eight-row q=10, 8x26 complete two-edit surgery — single-owner declaration

## Lane and ownership

Fast lane, single owner. Declaration-time observed HEAD of main:
`a48a7d777ee3b8f1b9729d190ba3fc1d73c75dd8`. I checked for competing
declarations on this topic (8x26 q10 surgery) before publishing; none
observed. Standard 11x11 empty board, two-stone roots, third move, S2, and
all closure classes remain UNKNOWN at every point; no verdicts are consumed.

## Objective

Complete two-edit neighborhood surgery of the published 8x25 m=25 witness
(71 stones, rows [9,9,9,8,9,9,9,9],
`research/experiments/eight-row-bands-20261114/output/w8q10-witness-search/s8x25q10_none.witness.json`,
sha256 `051be05c9c2c41a19a3cfe0fad0ad2fad63c15505df89fbe7b72f7fa54cfd9d`)
on the **8x26 board** (bx=26, by=8, q=10), targeting the unique uncovered
cell **T=(25,3)**. Frontier status for (8,10) is m=26: all four published
encodings INDET (s8x26q10_none 250s-class INDET; rowY3/rowY3lexH/rowY4
probes INDET). M_{8,10} in [26, 940] (upper U_{8,10}=940 curve-packing,
K0318 substitution family).

## Preliminary probe (disclosed, ran before this declaration)

Transplanting the m=25 witness onto 8x26 (unchanged coordinates; the seed
lives in x=0..24) and running the published generalized engine's census
stage gives:

- seed curves on 8x26: c=3: 42,150 / c=4: 2,214 / c=5: 271 / c=6: 68 /
  c=7: 9 / c=8: 3 / c=9: 19; max c = 9 = Q-1, seed safe;
- uncovered-cell census: **exactly one uncovered cell, (25,3)** — the seed
  is one-stone-short on 8x26;
- T-curve census: c7=0, c8=1 — the unique c8 T-curve is the row-3 line
  y=3 carrying the 8 stones of row 3; empty_on=17.

The full surgery enumeration has NOT been run yet; only the census stage
of a probe invocation (dummy target 25,3 chosen to match the census output)
completed. No candidate counts, safe counts, or witness counts exist yet.

## Plan (publish-then-execute)

1. Engine: `scripts/surgery_general.py` sha256
   `8ae82dde4b4959c1e0cfdc388f619d32508623befb29b0c91968bab25d3b6b6a`,
   byte-identical to the engine published in
   `six-row-q6-m26-two-edit-surgery-20261127` and
   `six-row-q7-m22-two-edit-surgery-20261127` (q-parameterized; here
   safety >= 10, blocking >= 9, final size <= 71 = 8x9 - 1, deficiency 1).
2. Calibration: rerun the published 7x32 q=6 m=31 surgery and require exact
   counter reproduction (2,224,675 / 0 / 0; T-curve census c4=1 c3=10).
3. Official runs: full enumeration, chunked (each chunk independently
   re-executes setup; chunk slices partition the sorted candidate list),
   two independent passes (run1/run2) required byte-identical per chunk;
   combine chunk counters.
4. Independent method-disjoint spot-check: integer-only conic re-checker
   (`scripts/spotcheck_int.py` sha256
   `8f57d6b05198451c5f40419cf977a5e94655954ba1c0ee027fb2c4fa887de9ea`)
   on a 300-candidate seeded-random sample of engine-rejected candidates,
   chunked 100/100/100; all must confirm rejection, 0 missed witnesses.
5. Tamper battery: T1 blocked target (fail-closed), T2 unsafe seed
   (complete a 10-stone curve) (fail-closed), T3b weakened blocking gate
   (fail-loud, spurious witnesses expected).
6. Honest scope: a negative result is a LOCAL negative (no 8x26 witness
   within edit distance <= 2 of the m=25 seed), NOT absence of 8x26
   witnesses and NOT a verdict on the INDET SAT encodings. A positive
   witness would be reported immediately and separately.

## Rediscovery control (honest disclosure)

No m=24 witness is published for this family, so no rediscovery positive
control is available; disclosed rather than fabricated.
