# Eight-row q=9, 8x29 row-split direct evaluation — first 8x29 evaluation (2026-11-28 fast lane)

Single-owner lane declared in
`research/log/2026-11-28-eight-row-q9-m29-row-split-declaration.md`
(declaration commit `ec68f8f4`, declaration-time HEAD `ed37b8ab`, clean
publish-then-execute). Family (w,q)=(8,9): published witness band 8x9..8x28,
M_{8,9} in [29,984] (upper U=984, K0318 substitution), frontier 8x29. This is
the first evaluation of any width >= 29 in this family.

## Results

Rowfixed sweep (deficiency-row conditioning over the 4 vertical-mirror row
classes; V: y <-> 7-y), genfast.js CNF + kissat 4.0.4, 280 s caps:

- **rowY=2: UNSAT, 5,079,168 conflicts, decided in 205.0 s** — the single-
  deficiency row classes {2}/{5} are **witness-free at 8x29** (per-class
  absence, kissat UNSAT certificate). Cold pair bit-exact across a full
  execution-environment reset (pre-reset run: identical 5,079,168 conflicts).
- rowY=3: INDET 5,177,768 conflicts @ 280 s (pre-reset same-trajectory cut at
  5,338,027; wall-clock cuts are same-trajectory, not bit-exact)
- rowY=0: INDET 4,732,792 @ 280 s (pre-reset 4,853,093)
- rowY=1: INDET 5,602,963 @ 280 s (pre-reset 5,746,874)
- rowY=3 + lex=H cross-encoding (sound with rowY since H preserves rows):
  INDET 4,972,540 @ 280 s

Class-split probes (sat3.js class/krow/minpos decomposition, positive pieces
of the rowY=3 class):

- 8x29 class {3} krow=3:7 minpos=0: INDET 5,424,393 @ 280 s
- 8x29 class {3} krow=3:7 minpos=1: INDET 5,228,774 @ 280 s

All INDET pieces are honest negatives, not absence. Near-uniform 4.7-5.6M
conflict resistance across all pieces at these caps.

## Controls

- **Calibration (pre-registered)**: cold rerun of the published 8x28 rowY=3
  instance through the identical pipeline: **SAT, 3,049,989 conflicts —
  bit-exact with the published records.jsonl**
  (eight-row-bands-20261114/output/w8q9-witness-search), and the decoded
  witness stones are **bit-identical to the published m=28 witness**
  (`s8x28q9_rowY3.witness.json`). Dual verification (decode_verify.js
  verifyConfig + exact-Fraction verify_witness.py) both PASS.
- **Positive control for the class-split pipeline**: 8x28 class {3}
  krow=3:7 minpos=1 SAT, 3,013,059 conflicts; decoded 63-stone witness rows
  [8,8,8,7,8,8,8,8], dual-verified (jsVerify + pyVerify PASS), and
  **D4-non-congruent to the published 8x28 witness** — a second, essentially
  distinct 63-stone deficient maximal witness at 8x28 (bonus observation).
- CNF determinism: the (8,28,9) rowY=3 CNF was regenerated twice,
  byte-identical; the lex=H CNF regeneration byte-identical.

## Toolchain (pins in the declaration)

- genfast.js sha256 409b5216... (eight-row-bands-20261114, verbatim)
- sat3.js sha256 e04581eb... (six-row-q6-m26-class-split-20261127, verbatim)
- sat.js fcc0cfd8..., sat2.js 14ceb854..., verify_witness.py 298ff590...
  (seven-row-inband-families-20261114, verbatim), decode_verify.js bf64e428...
- kissat 4.0.4 official linux-amd64, md5 3a5eba830aa6008a604fcc9bbe99a325,
  sha256 21da5d98... (pinned binary; not redistributed here)

## Disclosure

- A mid-lane Koyeb artifact-save failure reset the execution environment once
  (known file-loss failure mode). All raw logs published here are post-reset
  reruns; the pre-reset same-instance observations (SAT calibration conflicts
  identical; UNSAT rowY=2 conflicts identical; INDET time-cut conflict counts
  listed above) are disclosed per piece in `output/records.jsonl`. The UNSAT
  and SAT verdicts are deterministic and reproduced bit-exactly; INDET
  conflict counts at wall-clock cuts are host-dependent by nature.
- CNFs and model files are deterministically regenerable and not published
  (size policy of the source lanes; meta jsons are published).

## Scope and non-claims

- No absence claim at 8x29 overall: only the single-deficiency classes
  {2}/{5} are decided witness-free; classes {0}/{1}/{3} (and V-mirrors
  {7}/{6}/{4}) are INDET-undetermined, and **multi-deficiency classes (2+
  deficient rows) are unswept**.
- M_{8,9} stays in [29,984]; the frontier stays 8x29.
- Standard 11x11 empty board, two-stone roots, third move, S2, closure
  classes: UNKNOWN at all times; verdicts not consumed; conflicts are
  bookkeeping.

## Files

- `scripts/`: pinned byte-clones + the fresh `rowrun.sh` / `clsrun.sh` runners.
- `output/`: raw kissat logs, meta jsons, witness jsons, `records.jsonl`,
  `summary.json`.
- `MANIFEST-sha256.txt`.
