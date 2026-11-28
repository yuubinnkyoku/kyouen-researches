# 2026-11-28 Six-row q=6, 6x26 multi-deficiency two-deficient-row classes k=4:4 — wave A takeover declaration

## Status

Takeover single-owner declaration (publish-then-execute). The original
single-owner wave A declaration is `211ae16c`
(`research/log/2026-11-27-six-row-q6-m26-multidef-twodrow-declaration.md`,
2026-11-27T17:56:56Z, declaration-time HEAD `07937d74`). Takeover basis:

- No completion, kit, or measurement for the wave A targets has been
  published since the declaration (verified by a commit scan of main up
  to 2026-11-28T01:27Z; the only multidef-related commit after the
  declaration is `2b188b6d`, an unrelated class0-kit raw-log restore).
- The declaring session's persisted work tree (knowledge `_work-m26-multidef`)
  contains only machinery: probe.sh, the calibration CNF
  `cal_c2k4p11.cnf`, and a partial positive-control log
  `r_calib_6x25_c2k4p11.txt` whose last progress line is at ~102.8s
  process time (killed mid-run; no target probe was measured, no
  records.jsonl target rows exist). The lane is stalled >7h with its
  owner session gone.

This takeover re-declares the same target set under this session's
ownership. No target measurement (any of the 108 sub-instances) has been
run by this session before this declaration; only machinery verification
(disclosed below) has been done.

Declaration-time HEAD: `7d49c0e6` (main, 2026-11-28T01:27:26Z),
re-fetched immediately before this push.

## Non-interference

Targets are exactly the wave A set of the original declaration: 6x26
q=6 two-deficient-row classes D={a,b}, both rows pinned at exactly 4
stones (krow a:4,b:4; all other rows FULL at 5), 28 stones, minpos
H-split P=0..11 on row a=D[0], 9 canonical classes under V in the
priority order {0,5}, {0,1}, {1,4}, {0,4}, {1,3}, {2,3}, {0,3}, {1,2},
{0,2} (covers all 15 pairs). Disjoint from every parallel declared lane
(seven-row q6 7x32 `7d49c0e6`, seven-row q7 7x27 `40a05ee3`, seven-row
q8 7x26 `93c10bc7`, three-row q4 m30 `4505b70a`, four-row q6 m35
`e529754e`, eight-row q10 `3994ce9d`, n11 thirteenth lanes, n10
lanes, PG/AG finite-ring lanes). The other stalled six-row q6 6x26
single-deficiency lanes (class {1} `f9a982d2`, class {2} REST
`e61acf82`, deepdef `9e703319`) are NOT taken over by this
declaration and remain with their owners.

## Decoding convention (unchanged from the original declaration)

SAT in any deciding sub-instance => 6x26 two-deficient-row k=4:4
28-stone deficient-maximal witness exists => M_{6,6} >= 27 (range update
[26,495] -> [27,495]); witness decoded and dual-verified (sat3.js decode
+ verifyConfig, verify_frac.py independent Fraction verifier), negative
controls (remove one stone -> non-maximal, add one stone -> rejected),
and a cold-pair rerun before any claim. All swept sub-instances UNSAT =>
the k=4:4 layer is witness-free in the swept classes at 6x26 (partial
absence). INDET at cap => honest negative, not absence.

## Engine and calibration (pre-declaration, disclosed)

- Scripts sat3.js/sat2.js/sat.js/verify_frac.py: byte-clones verified
  sha256 `e04581eb`/`14ceb854`/`fcc0cfd8`/`837fe24b` == published
  class0-split kit MANIFEST.
- kissat 4.0.4 official linux-amd64, binary sha256
  `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`
  (verified before this declaration; --version 4.0.4).
- Encoder calibration: regenerated 6x26 class {0} krow=0:4 minpos=0 CNF
  meta vars 58,722 / clauses 205,663 == published
  `meta_6x26q6_c0k4p0.json` bit-exact. First-generation multidef meta
  6x26 class {0,5} krow=0:4,5:4 minpos=0: vars 58,722 / clauses 205,665
  (exactly +2 clauses over class {0} p0 = the second krow pin pair, as
  expected from the encoder).
- Positive control (acceptance, run AFTER this declaration): 6x25 q=6
  class {2} krow=2:4 minpos=11 must reproduce the published K1217 value
  SAT 3,574,244 conflicts bit-exact.

## Execution plan

Per-probe cap 272s (SIGTERM), one kissat invocation per probe. Probes
run in small parallel batches (<=4 concurrent kissat processes) within
single shell calls; each probe keeps its own raw kissat log and encoder
meta json. CNFs regenerable, not published (size policy). Every swept
sub-instance is published with its raw log; unswept sub-instances
remain bookkeeping-open and are NOT absence claims.

## Bookkeeping

11x11 empty board, all 19 central-reply roots, two-stone root {60,27},
third move {100,108}, S2, all closure classes: UNKNOWN at all times; no
verdict consumed by this lane; conflicts are bookkeeping.
