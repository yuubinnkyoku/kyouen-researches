# Seven-row q=7, 7x28: classes {0}/{1}/{2} first coverage + class {3} minpos 5/6 + complete two-edit surgery, all negative (2026-11-28 fast lane)

Single-owner lane declared in
`research/log/2026-11-28-seven-row-q7-m28-classes012-declaration.md`
(declaration-time HEAD `3686a5c0`, declaration commit `bdb7513a`).

## Result 1: sweep pieces all INDET (honest negatives, not absence)

kissat 4.0.4 (official linux-amd64 binary, sha256
`21da5d98...ac93a1`), SIGTERM time-cuts at 275/272s caps:

- class {3} krow=3:5 minpos=5: INDET, 2,914,708 conflicts (275s)
- class {3} krow=3:5 minpos=6: INDET, 2,927,565 conflicts (272s)
- class {0} krow=0:5 minpos=0: INDET, 2,710,560 conflicts (272s; H-mirror covers class {6})
- class {1} krow=1:5 minpos=0: INDET, 2,724,218 conflicts (272s; H-mirror covers class {5})
- class {2} krow=2:5 minpos=0: INDET, 2,570,306 conflicts (272s; H-mirror covers class {4})

All mirror classes now have first coverage at 7x28 krow=:5. The conflict
band (2.57M..2.93M) sits inside the class {3} band published by
seven-row-q7-m28-class-split-20261128 (2.73M..3.45M) — the near-uniform
resistance extends across all row positions of the single deficiency.
**Honest negatives per piece only, no absence claim at any width.**
Not swept here: minpos >= 1 for classes {0}/{1}/{2}, minpos 8..13 for
class {3}, krow=3:4 deep-deficiency, multi-deficiency classes.

**M_{7,7} stays in [28,708]; the frontier stays 7x28.**

## Result 2: complete two-edit surgery of the 7x27 witness on 7x28, negative (both placements)

Engine: `surgery_general.py` (sha256 `8ae82dde...b6b6b6a`), byte-clone of
the six-row-q6-m26-two-edit-surgery-20261127 kit script (q/board
parameterized, exact Fraction arithmetic, seed-safety and
target-unblocked fail-closed asserts). Seed: the published 7x27 witness
(`seven-row-q7-m27-class-split-20261128/output/w77_27.json`, 41 stones),
placed on 7x28 both ways (shift-0 and +1 right-shift; each leaves exactly
one uncovered cell):

- shift+1, T=(0,3): **2,158,423 unique candidates, 0 safe, 0 safe-maximal
  witnesses**;
- shift-0, T=(27,3): **2,158,423 unique candidates, 0 safe, 0 witnesses**.

Local negative only: no 7x28 witness within edit distance <= 2
(<= 2 removals, <= 2 additions, final size <= 41) of either placement of
the m=27 seed. NOT an absence claim for 7x28 overall.

### Structural observation (one-curve frontier)

For both placements the T-curve census is exactly `{c4: 0, c5: 1}`:
the only curve through the uncovered frontier cell carrying >= 4 seed
stones is the deficient row-3 horizontal line itself (5 stones). All
blocking routes within 2 edits must complete that single line, and every
such completion fails safety. The frontier cell of a
single-deficiency witness is generically "one-curve" — this matches the
m=26 (6,6) surgery census {c3: 3, c4: 3} being richer only because q=6
blocking needs 5 stones; and it is consistent with the large
consecutive-width witness jumps (sd 28..34) measured across the family.

### Controls

- **Calibration (byte-exact)**: 6x26 published surgery case reproduced
  byte-for-byte — `output/calib-m26.json` sha256
  `7cfe56c7243591552c0f911ac2b46bd31e23c935c23cd505cf931c87b3e3a070`
  is identical to the published `surgery-m26.run1.json` of the six-row
  kit (candidates 836,890 / safe 0 / witnesses 0, T-curve census
  {c3: 3, c4: 3}), with the published m25 seed
  (`m25.witness.stones.json`, sha256 `9f910a8c...38751`).
- **Toolchain calibration**: 7x24 q7 class {3} krow=3:5 minpos=1 SAT,
  64,031 conflicts — bit-exact with the published family control.
- **Determinism**: surgery run1/run2 sha256-identical at both placements
  (`4f80801b...de844` shift+1, `b37f4a78...575d` shift-0).
- **Independent spot-check**: `spotcheck_int.py` (method-disjoint
  integer-conic re-checker, sha256 `8f57d6b0...49ea`) on a seeded-random
  sample of 300 engine-rejected candidates: 300/300 rejections confirmed,
  0 missed witnesses.

## Files

- `output/r7x28q7_c{3k5p5,3k5p6,0k5p0,1k5p0,2k5p0}.txt`: raw time-cut logs.
- `output/cal7x24.txt`: calibration raw log (SAT, 64,031 conflicts).
- `output/calib-m26.json`: engine calibration output (6x26 exact match).
- `output/seed7x28_shift{0,1}.json`: surgery seeds.
- `output/surgery-m28.run{1,2}.json`, `output/surgery-m28-s0.run{1,2}.json`:
  surgery outputs (deterministic pairs).
- `output/surgery-m28.run2.json.sample.jsonl`, `output/spotcheck-summary.txt`:
  spot-check sample and result.
- `output/records.jsonl`, `output/summary.json`: machine-readable records.
- CNFs not published (size policy). Sweep scripts: byte-clones of the
  seven-row-q7-m27-class-split-20261128 kit (sat.js fcc0cfd8 / sat2.js
  14ceb854 / sat3.js e04581eb / verify_frac.py 837fe24b), pinned by that
  kit's MANIFEST; surgery scripts pinned by the six-row
  m26 kit's MANIFEST (not re-published).

## Non-claims

No 11x11 root / two-stone root {60,27} / third move {100,108} / S2 /
closure-class verdict is created, consumed, or transferred; all remain
UNKNOWN. Conflict counts are bookkeeping. The unswept pieces and classes
carry no absence claim; M_{7,7} <= 708 stands and exact M needs
persistence at m=28..707 or a tail bound.
