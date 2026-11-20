# REMO survivor-column minimal period: maximal-proper-divisor reduction (LEMMA RED) and the r = 49..150 maxdiv sweep

Knowledge item: K1163 (renumbered from a drafted K1162; see the
renumbering note under "Determinism and trust").

Declared fast-lane follow-up to K0925 (THEOREM S32) and K1145
(THEOREM S48) for the uniform-board counting recursion E(C,r) of
K0859 Theorem D: the survivor column C -> S(C,r).
Single-owner note:
`research/log/2026-11-20-remo-survivor-maxdiv-r49plus-single-owner-note.md`
(declaration commit `97b741b8`, typo-fix commit `f4af3e1b`, scope
unchanged).  This lane is independent of the `r33plus` lane's
declared sweep scope; the universal survivor-minimality proof
attempt invited by
[the r33plus note](../../log/2026-11-20-remo-survivor-witness-r33plus-single-owner-note.md)
remains OPEN -- this experiment is the machine fragment the
invitation calls for (reduction lemma + extension sweep + structure
observations), not the universal proof.

## LEMMA RED (universal, proved)

Let r >= 2, Q(r) = lcm(1..r), and let f be the survivor column
(f(C) = S(C,r)).  By K0925 THEOREM W+ (universal, all C >= 1) Q(r) is
a period of f, and by K0922 LEMMA DIV the set of periods of f is
exactly the set of positive multiples of its minimal period m, with
m | Q(r).  Then:

**m = Q(r)  iff  for every prime p <= r the maximal proper divisor
Q(r)/p is not a period of f** (equivalently: rejected by one witness
C with S(C+Q/p,r) != S(C,r)).

Proof.  If m < Q(r), pick any prime p dividing Q(r)/m.  Every prime
factor of Q(r) is <= r, so p <= r.  Then Q(r)/p = m * (Q(r)/(m p)) is
an integer multiple of m, hence a period; it is a proper divisor of
Q(r).  Conversely, if Q(r)/p is a period for some prime p <= r, then
m | Q(r)/p | Q(r) and m <= Q(r)/p < Q(r), so m < Q(r).  QED.

So the full proper-divisor sweep of K0925/K1145 collapses from
d(Q(r)) - 1 divisors to pi(r) maximal-proper-divisor checks:

| r | proper divisors of Q(r) | maximal proper divisors |
|---|---|---|
| 48 | 294,911 | 15 |
| 100 | 660,602,879 | 25 |
| 128 | 96,636,764,159 | 31 |
| 150 | 1,546,188,226,559 | 35 |

(The one-line covering fact behind this collapse -- every proper
divisor d of Q(r) divides at least one Q(r)/p: pick any prime q
dividing Q(r)/d -- is machine-anchored by C0 for r = 2..36,
146,121 proper divisors.)

With the K0926 E6U plateau (S(C,r) = P(C) for C <= r), the
bounded-witness window form of K0925 specializes at maxdiv level to:
the conjecture requires, for every prime p <= r, some C in [1,r-1]
with S(C+Q/p,r) != P(C).  LEMMA RED gives no window bound by itself;
the window bound below is observation.

## THEOREM S150 (machine, r = 2..150)

The survivor column's minimal period is exactly Q(r) for every
r = 2..150.  For r = 2..48 this is the published K0925/K1145
full-divisor machine determination (THEOREM S32 + THEOREM S48).  For
r = 49..150 the C4 sweep rejects every maximal proper divisor
Q(r)/p (p prime, 2,602 pairs) by a witness C <= 150 (fallback
[151,1500] never needed, fail-closed), which by THEOREM W+ (positive
direction) and LEMMA DIV + LEMMA RED (necessity direction)
determines the minimal period.  Trust boundary identical to K1145:
the swept dynamics are the published closed-form `survivor_fast`
(anchored to the verbatim per-stone K0859 recursion by C2 at the new
range and by the K0925/K1145 TWIN checks), and the necessity
reduction is the proved lemma above rather than any per-divisor
exhaustive search at r >= 49.

## The sweep (r = 49..150)

Witness per (r,p): minimal C, ascending, window [1,150] (+ fallback
[151,1500], unused).  All 2,602 pairs witnessed; **2,602/2,602
witnesses are <= r-1** (global max 124, at the block {131..136}).
The witness histogram over the 2,602 pairs is spread between values
2 and 102+ (top: C=32 x93, C=10 x89, C=27 x86, C=4 x78, C=14 x77;
full histogram in the audit).  The full per-(r,p) witness table is
published as `output/maxdiv_witness_table.txt` (r = 2..150, one line
per r, witnesses in ascending-prime order; SHA-256
`cdf890c1d4ad559bae337dd0f029384236494c99f5a5135674e585dde23f1990`,
also pinned inside the audit).

Witness maxima are CONSTANT inside every equal-Q block (the argmax
prime is that of the shared block map):

| r range (block) | wit_max | argmax prime(s) |
|---|---|---|
| 49-52 | 38 | 47 |
| 53-58 | 40 | 47 |
| 59-60 | 42 | 7 |
| 61-63 | 46 | 47 |
| 64-66 | 45 | 47 |
| 67-70 | 52 | 61 |
| 71-72 | 48 | 71 |
| 73-78 | 51 | 73 |
| 79-80 | 58 | 71 |
| 81-82 | 68 | 79 |
| 83-88 | 55 | 73 |
| 89-96 | 72 | 83 |
| 97-100 | 90 | 97 |
| 101-102 | 69 | 97 |
| 103-106 | 60 | 103 |
| 107-108 | 66 | 97 |
| 109-112 | 101 | 103 |
| 113-120 | 102 | 107 |
| 121-124 | 97 | 109 |
| 125-126 | 99 | 11 |
| 127 (singleton) | 110 | 127 |
| 128-130 | 110 | 127 |
| 131-136 | 124 | 131 |
| 137-138 | 110 | 11 |
| 139-148 | 106 | 139 |
| 149-150 | 109 | 131 |

## Observations (finite, r <= 150 unless noted)

1. **Bounded witness, maxdiv fragment**: every maximal proper
   divisor of Q(r) is rejected by a witness C <= r-1 for all
   r = 2..150 (the full-divisor window form is the K0926
   restatement of the bounded-witness conjecture; the maxdiv
   fragment is observed to hold through r = 150, the full-divisor
   form only through r = 48 via K0925/K1145).  Universal survivor
   minimality stays OPEN.
2. **Equal-Q block identity extended** (K1145 obs. 2, sharpened to
   maxdiv granularity and r <= 150): inside each of the 40
   multi-member equal-Q blocks in 2..150 the ENTIRE (p -> minimal
   witness) map is identical across the block; large blocks include
   {89..96} (24 shared primes), {113..120} (30), {131..136} (32),
   {139..148} (34).  All adjacent-block control pairs have differing
   maps.  Not explained by the E-side phase structure (K1154 V6:
   the E-side h* map is block-non-invariant).
3. **The h*=1 "argmax" pattern of r <= 48 does not extend**: in
   r = 49..150 the wit_max-argmax divisor Q/argmax_p has h* = 1
   (M_1 failure, v_p(r) = v_p(Q(r))) for only 6 of 102 values of r,
   namely r in {71, 73, 97, 103, 131, 139} -- exactly the prime
   block leaders whose own divisor Q/p takes the shared block
   maximum (blocks {71,72} p = 71, {73..78} p = 73, {97..100} p = 97,
   {103..106} p = 103, {131..136} p = 131, {139..148} p = 139);
   for all other blocks the argmax maxdiv has h* >= 2 (e.g.,
   r = 109..112 p = 103 h* = 7, r = 113..120 p = 107 h* = 7..14,
   r = 149..150 p = 131 h* = 19).  K1145's smaller-range pattern
   ("the witness-maximal divisor is a Q/p with h* = 1") is
   therefore an artifact of the r <= 48 range.  Additionally, at
   r in {19,20,21,22,27,28} the published full-divisor witness
   maximum strictly EXCEEDS the maxdiv maximum (the witness-maximal
   divisor is not even maximal); C3 records the machine exception
   list against the published K0925 maxima.
4. **Reject-vector non-identity (negative refinement of obs. 2)**:
   the K1145 identity is exactly at the minimal-witness level.  The
   full reject vectors (C in [1,60]) of same-block r pairs DIFFER
   for some primes: block {17,18} at p = 3 (first vector difference
   C = 12), block {37,38,39,40} at p = 13 (C = 27) and p = 19
   (C = 20), block {113,120} at p = 13 (C = 27) and p = 19 (C = 44);
   while their minimal witnesses agree.  For the block {89,90} NO
   vector difference was found in the window (24 shared primes,
   C <= 60): reject-vector identity is block- and p-dependent, so
   the minimal-witness-level statement is the correct invariant.
   No value-level identity holds (same-block survivor columns differ
   from each other starting just beyond the K0926 plateau; checked in
   the lane log, not part of the audit).

## Machine checks (audit.json, 8/8 ok)

* C0 covering anchor (r = 2..36): every proper divisor of Q(r)
  divides at least one maximal proper divisor Q(r)/p (146,121
  proper divisors; the algebraic one-liner is in LEMMA RED).
* C1 brute-force equivalence (r = 2..24): an independent
  reimplementation of the K0925 W5 full-divisor minimal-witness
  sweep (window [1,150], fallback [151,1500]) and the maxdiv-only
  sweep agree on the per-r verdict "every proper divisor rejected"
  (e.g., r = 24: 1,919 proper divisors, 0 unwitnessed both ways),
  and the maxdiv subset witnesses match the full sweep exactly
  (the maxdiv sweep here is a second, independent code path).
* C2 TWIN anchor at the new range: verbatim per-stone K0859
  recursion == closed-form twin on the full (elim, survivor) pair
  and survivor_fast == the survivor component, r grid
  {49,...,150} (15 values), C in [1,60], 900 pairs, 0 mismatches.
* C3 published-value pins (r = 2..48): (a) the maxdiv table
  reproduces the K0922 audit M5 w_sv values for d = Q/p,
  r = 10..16, verbatim (K0925-verifier transcription; w_elim = 1
  universal by K0925 W+); (b) the per-r maxdiv witness maximum is
  <= the published full-divisor maximum for every r = 2..48, with
  equality everywhere except r in {19,20,21,22,27,28} (strict,
  machine-recorded exception list).
* C4 the main sweep (r = 49..150, 2,602 (r,p) pairs): every
  maximal proper divisor rejected, witness <= r-1 on every pair,
  per-r aggregates (Q, wit_max, argmax prime, argmax h* and its
  class, histogram) in the audit; with W+ and DIV+RED this gives
  THEOREM S150.
* C5 positive period anchors at the new range: S(C+Q(r),r) ==
  S(C,r) for ten r in [49,150], C in [1,50] plus anchors
  {Q-1,Q+1,Q+5,2Q-1}, 540 comparisons, 0 bad (machine anchor; the
  universal proof is K0925 W+ / K1154).
* C6 equal-Q block minimal-witness-map identity (r = 2..150):
  40/40 multi-blocks identical, controls all differ (48 blocks
  total in 2..150).
* C7 reject-vector non-identity observations (blocks {17,18},
  {37,38,39,40}, {89,90}, {113,120}; vector window [1,60]).

## Determinism and trust

Deterministic, stdlib only, no network, no clock in the audit.
`assemble` runs twice per invocation and must be byte-identical.
Two independent full recomputes (`--no-cache`), both in an isolated
cwd + isolated HOME and one with `PYTHONHASHSEED=random`, wrote
byte-identical `output/audit.json`
(SHA-256 d916f0a2fd8455d02de86e25b34e51a921a03dacc2db159207c00fc161c1110d,
51,077 bytes) and byte-identical
`output/maxdiv_witness_table.txt` (SHA-256
`cdf890c1d4ad559bae337dd0f029384236494c99f5a5135674e585dde23f1990`,
9,148 bytes; pinned inside the audit); one fresh full run takes
~110 s.  `output/published_run.txt` is the stdout record of the
published fresh run (its elapsed line is not part of the pinned
bytes).  Per-r checkpoints live in `output/ck/` (not published) and
`--no-cache` recomputes everything.

Renumbering note (publication time): the item id was initially
drafted as K1162, which another lane published first (17:31Z); the
AGENTS.md renumbering rule moves this item to **K1163**.  The
verifier's embedded `item` field was changed accordingly and a fresh
`--no-cache` full recompute printed `checks:8 ok:8 all_ok:True` in
112.2 s; its audit is byte-identical to the previously double-verified
bytes except the one-line item field (machine-checked by diff), and
the witness table is unchanged.

## Out of scope

No claim about r >= 151; no claim about non-maximal divisors at
r >= 49 (their witnesses are finite-swept only through r = 24 by C1
and through r = 48 by the published K0925/K1145 sweeps); nothing
about the universal bounded-witness conjecture beyond the observed
maxdiv fragment; Δ != 0 non-uniform boards and the 11x11 empty
board are untouched; no meaning is claimed for h* on the survivor
side beyond the K1154 E-side analysis.

## Reproduce

```sh
python3 verify_survivor_maxdiv_r49plus.py             # cached checkpoints
python3 verify_survivor_maxdiv_r49plus.py --no-cache # full recompute (~110 s)
```
