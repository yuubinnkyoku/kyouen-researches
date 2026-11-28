# 2026-11-28 n11 thirteenth class-16757 k01+k02 adoption completion

Completion log of the Part declared in
`research/log/2026-11-28-n11-thirteenth-ladder-top-k01k02-adoption-declaration.md`
(declaration commit `5cb113c5`, single owner, publish-then-execute).
Kit: `research/experiments/n11-thirteenth-ladder-top-k01k02-adoption-20261128/`.

## Result: MAKER-PASS x2 byte-identical, head of record advanced

- **New head of record
  `merged-exact-s5-chain-plus-thirteenth-k01k02-20261128.cache`
  sha256 `d772f73c68bf051e7b90e5cd6cfef2a7b1c8e07da888c5f728f7a04b39edd1ec`,
  6,896 rows WIN 214 / LOSS 6,682** - exactly the pre-registered
  shape (BASE `beecb024` 6,894 rows WIN 212 / LOSS 6,682 + the 2
  declared fresh WIN rows k01 1153204147814662144:65536 nodes 2,678,305
  and k02 1152922672837951488:65792 nodes 3,485,963, both class 16757).
- Increment `cebd8dc9...`; manifest `18433ac0...` (schema
  n11-thirteenth-ladder-top-k01k02-win-adoption-manifest-v1); merger
  `90711961...` x3 byte-identical (merge-audits `4f58dd67...` x3).
- Maker gates all PASS: G0 pins + 6-kit MANIFEST self-verification,
  G1 live re-run of BOTH published gate_runner.sh instances (4
  fresh-cold C++ passes, node-exact vs published raws), G2 six-pillar
  re-parse, G3 freshness + conflict audit, G4 quarantine-free +
  canonical-safe, G5 increment, G6 merger x3 + shape check.  Both
  maker runs byte-identical (kitout recursive hash x2).

## Honest disclosures

- First maker invocation died fail-closed on a quarantine-header
  full-sha pin typo (no output written); fixed and disclosed.
- The published k02 cppgate kit's MANIFEST contains a
  self-referential MANIFEST-sha256.txt line whose value cannot match
  (self-reference); the single line is excluded from verification and
  disclosed in the declaration, README and here.  All other 19 lines
  verify.  Owner-lane cosmetic repair is a future item.
- The head cache (288,866 B) was published via chunked reads to avoid
  the 64 KB single-read cap (the known truncation hazard);
  fetch-back byte-verification is recorded in this Part.

## Claim status

Adoption bookkeeping only; NO verdict consumed.  The 2 rows are cache
bookkeeping, NOT a class closure, NOT a root verdict, and transfer
nothing.  Class 16757 completion additionally requires Board-verified
free_now; the WIN-side flip-census review (BASE `beecb024` -> SCEN
`d772f73c`) is the declared follow-up Part (owner-union prediction
pre-registered in `n11-thirteenth-owner-union-precheck-20261128`,
`fdb704d7`).  The standard 11x11 empty board, the 19 central-reply
roots, the two-stone root {60,27} and third moves 100/108 stay
UNKNOWN.  Nodes are bookkeeping, never verdicts.
