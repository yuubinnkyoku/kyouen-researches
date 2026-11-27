# Six-row q=6, 6x26: class {2} krow/minpos decomposition probes — 4 INDET honest negatives (2026-11-27 fast lane)

Single-owner lane declared in
`research/log/2026-11-27-six-row-q6-m26-class-split-declaration.md`
(declaration commit `02e40e9e`, declaration-time HEAD `f45869dd`). Same
machinery as the 6x22 q=7 kit `six-row-q7-m22-class-split-20261127`
(scripts byte-clones; kissat 4.0.4 official linux-amd64, sha256
`21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`).

## Result

4 of the 23 disjoint minpos sub-instances of **6x26 q=6 class {2}
krow=2:4** (the single-deficiency 29-stone family of the m=24/m=25
witnesses) were probed at 272s caps, prioritized around the m=25 witness
geometry (row-2 leftmost stone x=11):

- minpos=10: INDET, 3,729,885 conflicts
- minpos=11: INDET, 3,969,268 conflicts (family analog position)
- minpos=12: INDET, 3,862,795 conflicts
- minpos=13: INDET, 4,123,449 conflicts

**All honest negatives, not absence.** No witness found; **M_{6,6} stays in
[26, 495], frontier stays 6x26.** The near-uniform ~3.7-4.1M-conflict
resistance band resembles the 6x23 q=7 probes (`records.jsonl`), i.e. the
krow/minpos split that collapsed the (6,7) 6x22 frontier does not
immediately crack (6,6) 6x26 at these caps. Remaining minpos values
(P = 0..9, 14..22), class {1} krow splits, and the other canonical classes
remain unswept.

## Controls

- **Positive control**: 6x25 q=6 class {2} krow=2:4 minpos=11 SAT,
  **3,574,244 conflicts — the published K1217 value reproduced
  bit-exactly** (`output/r6x25q6_c2k4p11.txt`).
- Determinism of the encoder: metadata (vars/clauses) in
  `output/meta_*.json`; CNFs regenerable, not published (size policy).
- Disclosure: all runs happened after the declaration commit `02e40e9e`
  (clean publish-then-execute, no preliminary probes this time).

## Scope and non-claims

Honest negatives only; no absence claim at any width. Standard 11x11 empty
board, two-stone roots, third move, S2, closure classes: UNKNOWN at all
times; verdicts not consumed; conflict counts are bookkeeping.

## Files

- `scripts/`: sat3.js/sat2.js/sat.js byte-clones + the fresh Fraction
  verifier (unused here, included for kit self-containment).
- `output/`: raw kissat logs, records.jsonl, summary.json, meta jsons.
- `MANIFEST-sha256.txt`.
