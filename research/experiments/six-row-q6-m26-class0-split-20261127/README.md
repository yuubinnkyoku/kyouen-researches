# Six-row q=6, 6x26: class {0} krow/minpos decomposition probes — 12 INDET honest negatives (2026-11-27 fast lane)

Single-owner lane declared in
`research/log/2026-11-27-six-row-q6-m26-class0-minpos-declaration.md`
(declaration commit `a9dde1d3`, declaration-time HEAD `fe07ef8d`). Same
machinery as the 6x26 class-split kit `six-row-q6-m26-class-split-20261127`
(scripts byte-clones, sha256 `e04581eb…`/`14ceb854…`/`fcc0cfd8…`;
kissat 4.0.4 official linux-amd64, sha256
`21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`,
unpacked from the official rel-4.0.4 asset zip, zip sha256 `63282e51…`).

## Result

All 12 disjoint minpos sub-instances of **6x26 q=6 class {0} krow=0:4**
(edge-row single-deficiency 29-stone family; V-mirror covers class {5})
were probed at 272s caps — the complete sound H-split of the class
(min(x1, 25-x4) <= 11 for the 4 stones of row 0):

- minpos=0: INDET, 2,402,216 conflicts
- minpos=1: INDET, 2,509,295 conflicts
- minpos=2: INDET, 2,678,856 conflicts
- minpos=3: INDET, 1,355,457 conflicts
- minpos=4: INDET, 1,373,740 conflicts
- minpos=5: INDET, 1,396,332 conflicts
- minpos=6: INDET, 1,588,848 conflicts
- minpos=7: INDET, 1,666,278 conflicts
- minpos=8: INDET, 1,719,671 conflicts
- minpos=9: INDET, 1,822,575 conflicts
- minpos=10: INDET, 1,848,761 conflicts
- minpos=11: INDET, 4,053,417 conflicts

**All honest negatives, not absence.** No witness found; **M_{6,6} stays in
[26, 495], frontier stays 6x26.** The band is lower than the class {2}
krow=2:4 band (1.36M-4.05M vs 3.73M-4.12M conflicts at the same caps):
the edge-row family is *easier* for the solver but still cap-resistant at
272s. With this lane plus the parallel declared lanes (class {2} minpos
REST `e61acf82`, class {1} full split `f9a982d2`), every single-deficiency
canonical row class of 6x26 q=6 is now claimed by exactly one lane;
multi-deficiency classes and krow k<=3 deep-deficiency splits remain
unswept.

Observation probe (bookkeeping, not absence): 6x25 q=6 class {0}
krow=0:4 minpos=11 INDET at 272s, 4,280,184 conflicts — at the width where
class {2} goes SAT (3,574,244 conflicts, 234s), the class {0} analog
resisted the 272s cap.

## Controls

- **Positive control**: 6x25 q=6 class {2} krow=2:4 minpos=11 SAT,
  **3,574,244 conflicts — the published K1217 value reproduced
  bit-exact** (`output/r6x25q6_c2k4p11_mine.txt`, 241.07s; meta
  vars 53,532 / clauses 187,536 == published `meta_c25p11.json`).
- Encoder determinism (pre-declaration, disclosed in the declaration):
  regenerated 6x26 c2k4p11 CNF meta 58,722/205,674 == published.
- Determinism of the encoder: metadata (vars/clauses) in
  `output/meta_*.json`; CNFs regenerable, not published (size policy).
- Disclosure: all target measurements ran after the declaration commit
  `a9dde1d3` (clean publish-then-execute). One probe (P=2) was re-run
  after a background-invocation glitch ("No such file or directory" on
  the second parallel invocation); the re-run is the only measurement
  for P=2 and its raw log is the published one.

## Coordination disclosure

At 15:42:03Z (after this lane's declaration and after all 12 target
probes had completed locally at ~15:00-15:40Z), the commit `79ad283a`
published a four-lane execution scaffolding that lists this lane's
declaration `a9dde1d3` among its targets (82 probes: class0 12,
class1 12, class2rest 19, deepdef 39). This kit is the declaration
owner's completion of `a9dde1d3`; the executor lane's class0 runs, if
published, should be treated as an independent cross-check of this kit
(same-trjectory conflict counts are wall-clock sensitive and are not
expected to be bit-exact at SIGTERM cuts).

## Scope and non-claims

Honest negatives only; no absence claim at any width. Standard 11x11
empty board, two-stone roots, third move, S2, closure classes: UNKNOWN
at all times; verdicts not consumed; conflict counts are bookkeeping.

## Files

- `scripts/`: sat3.js/sat2.js/sat.js byte-clones + the fresh Fraction
  verifier (unused here, included for kit self-containment).
- `output/`: raw kissat logs (12 probes + control + obs), records.jsonl,
  summary.json, meta jsons.
- `MANIFEST-sha256.txt`.
