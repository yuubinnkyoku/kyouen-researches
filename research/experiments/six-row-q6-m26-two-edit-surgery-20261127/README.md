# Six-row q=6, 6x26: complete two-edit surgery, negative (2026-11-27 fast lane)

Single-owner lane declared in
`research/log/2026-11-27-six-row-q6-m26-two-edit-surgery-declaration.md`
(declaration-time HEAD `76181b40d85c1bb3e72e14292d75203f6d31b71e`; declaration
commit `26c25331`).

## Headline result

- The complete two-edit neighborhood (S' = seed - R + A, |R| <= 2, |A| <= 2,
  final size <= 29, A on empty cells, target cell T occupied or blocked) of the
  published 6x25 K1217 witness (29 stones, rows [5,5,4,5,5,5],
  `six-row-q6-m25-frontier-crunch-20261122/witness/w6x25_class2.json`,
  sha256 `4ec0887057b0d60397401f99a15ec43c3c61076eddd0b4e6c1fdd88fb4b4f309`)
  on the **6x26 board** targeting the unique uncovered cell **T=(25,2)**
  contains **no safe row-deficient maximal configuration**:
  - 836,890 unique candidates, 0 safe, 0 safe-maximal witnesses.
- The seed is one-stone-short on 6x26: machine census says the ONLY uncovered
  cell of the transplanted witness is (25,2) (the crunch-kit crosscheck note
  "not maximal (23,2)" refers to the bbox-normalized coordinate system; in the
  raw placement the uncovered cell is (25,2), reproduced here).
- This is a **local negative only**: no 6x26 witness within edit distance
  <= 2 (<= 2 removals, <= 2 additions) of the m=25 seed. NOT an absence claim
  for 6x26 overall. **M_{6,6} stays in [26, 495]** (K1217 lower bound,
  K0806/K0318 upper bound unchanged). Frontier stays 6x26.
- Measured observation: the m=25 witness is at symmetric difference >= 34
  (>= 17 stone moves) from both K1215 6x24 witnesses over all 4 flip images
  x all translations dx in [-26,26] - consecutive-width witness jumps are
  large in this family too (same phenomenon as the five-row m=26/m=24
  observation and the seven-row m=32 lane).

## Completeness argument (why the enumeration covers all maximal states)

- Any witness S' with |R|,|A| <= 2 must be maximal, so every cell is occupied
  or blocked; in particular T=(25,2) (uncovered in the seed) must be
  occupied or blocked in S'.
- Blocking a cell needs a curve through it with >= q-1 = 5 stones of S'.
  With <= 2 additions, such a curve carries >= 3 seed stones even after
  up to 2 removals, i.e. it is one of the seed's curves through T with
  c - t >= 3, c in {3,4} (c = 5 through T would mean T is blocked in the
  seed). The T-curve census is {c3: 3, c4: 3}; the need = 5 - (c - t)
  case split (need in {1,2}) is enumerated completely.
- Final size <= 29 keeps the config row-deficient (30 = all six rows at
  capacity 5 is non-deficient; 31+ needs a 6-stone row = unsafe). Hence
  a <= r in the enumeration.
- q=6 generalization of the published 7x32 q=6 engine
  (`seven-row-q6-m32-two-edit-surgery-20261127/scripts/surgery_m32.py`,
  sha256 `fe277e8a0360f25be3a7dff1f7c949248833fa9f547d9dc30db183a1c33fe3f0`);
  at q=6 the thresholds coincide, so the calibration below is exact.

## Engine, calibration, controls

- `scripts/surgery_general.py`: fresh q/board-parameterized implementation
  (Exact Fraction arithmetic, self-tests, seed-safety and target-unblocked
  fail-closed asserts, chunkable, optional seeded sample dump).
- **Calibration (exact)**: with the published 7x32 q=6 configuration
  (m=31 witness seed sha256 `8e46b0c82732bf1b3a0d95dbbf05a6ed08c4dacbc680fc3433657dfef6880b36`,
  T=(31,3)) the engine reproduces the published
  `surgery-m32.json` (sha256 `5867e7deae16b251f7ffcb418c4df34c2862781444776f024b1bcc35766801a6`)
  exactly: candidates 2,224,675 / safe 0 / witnesses 0 / T-curve c4=1 c3=10
  (`output/calib-m32.json`).
- **Determinism**: run1 vs run2 byte-identical (`output/surgery-m26.run1.json`
  sha256 `7cfe56c7243591552c0f911ac2b46bd31e23c935c23cd505cf931c87b3e3a070`,
  = run2). Bonus cross-reset reproduction: the pre-reset working-tree run
  produced the same sha before an environment reset destroyed it, and the
  rebuilt run reproduced it byte-exactly.
- **Independent spot-check**: `scripts/spotcheck_int.py` is a method-disjoint
  re-checker (integer conic coefficients x^2+y^2 scaled by an integer
  determinant; no Fraction, no seed tables, no case split; rebuilds all
  curves from S' itself). Unit tests: the circle through (0,0),(2,0),(0,2)
  yields exactly {(0,0),(2,0),(0,2),(2,2)}; a 6-collinear config is
  correctly unsafe. On a seeded-random sample of 300 engine-rejected
  candidates (of 836,890; sample file published), all 300 rejections are
  confirmed and no missed witness (`output/spotcheck-summary.json`).
- **Tamper battery** (`output/tamper/tamper-summary.json`):
  - T1 target changed to a seed-blocked cell -> fail-closed
    ("target must be unblocked in the seed", rc=1);
  - T2 seed tampered (stone added completing a 6-stone curve) -> fail-closed
    ("seed unsafe", rc=1);
  - T3 safety gate weakened (>= Q -> >= Q+1) on an engine copy -> counters
    identical (every candidate is maximality-rejected anyway); detection is
    by the engine sha256 pin in MANIFEST, disclosed, output not published;
  - T3b blocking gate weakened (>= Q-1 -> >= Q-2) -> fail-loud: counters
    diverge (safe 64,262 / spurious witnesses 64,262), byte-differs from the
    official run; full spurious log elided, excerpt published.

## Honest disclosures

- Preliminary local runs (engine build, calibration, a preliminary 6x26
  enumeration with identical counts) happened BEFORE the declaration was
  pushed; the declaration discloses this and all recorded/official runs
  (calibration, determinism pair, sample dump, spot-check, tamper battery)
  were executed AFTER the declaration commit `26c25331`.
- One environment reset destroyed the first working tree mid-session
  (nothing was published from it); all artifacts were rebuilt from main
  (published inputs re-fetched and sha-verified) and the rebuilt official
  runs are the ones recorded here. The pre-reset main-run sha equals the
  post-reset sha (disclosed above as cross-reset determinism).
- No rediscovery positive control exists in this lane: the m=25 witness is
  at sd >= 34 from both m=24 witnesses, so no 6x25-from-6x24 control is
  possible within two edits; the published-m32 exact calibration is the
  positive control instead.
- Standard 11x11 empty board, two-stone roots, third move, S2, closure
  classes are untouched and remain UNKNOWN at all times; verdicts are not
  consumed; candidates/safe/conflicts counts are bookkeeping.

## Outputs

- `output/m25.witness.stones.json`: seed stones (extracted from the
  published witness, pins in MANIFEST).
- `output/calib-m32.json` + stdout: published-7x32 calibration record.
- `output/surgery-m26.run1.json` (+ stdout, + 300-line seeded sample) and
  `output/surgery-m26.run2.json` (+ stdout): official main runs.
- `output/spotcheck-summary.json`, `output/tamper/*`: control records.

## Reproduction

```sh
python3 scripts/surgery_general.py --bx 32 --by 7 --q 6 --target 31,3 \
  --seed <published m31.witness.stones.json> --out calib.json
# calib.json == published surgery-m32.json counters
python3 scripts/surgery_general.py --bx 26 --by 6 --q 6 --target 25,2 \
  --seed output/m25.witness.stones.json --out run.json --sample 300
python3 scripts/spotcheck_int.py run.json run.json.sample.jsonl 300 0 100
# (chunks 100/100/100)
```
