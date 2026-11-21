# Three-row q=4 stabilization: single-owner declaration note

Date: 2026-11-21T02:14Z
Lane: three-row (w=3) fixed-width q-point lane — sibling of the K0070 (M_{3,6}=9) and
K0071 (M_{3,5}=12) three-row stabilizations, not a continuation of any claimed lane.
Declaration HEAD at write time: 02c4776d34 (full 02c4776d341472bd).

## Declared work (first-published-priority)

This lane claims, to the exclusion of other parallel runs, the true stabilization
length M_{3,4} of the 3xm q=4 fixed-width kyouen board:

(a) **Census cross-validation**: the published four-row lane's sat.js/sat2.js census
    (md5 0cc6021a4e523a0d7f4d5ea0f5f5d40c / 282ae832efa0080127c6c153e65e1c3c) run at
    w=3, compared against the K0318 curve_packing_fixed_width.py curve enumeration
    (pinned at commit 49891aaf2d402436b9581296ec91b52769e687d6) on small boards:
    identical forbidden-curve sets (line + circle, count and point masks).
(b) **Small-board brute-force verification** of the deficient-mode encoding:
    exhaustive enumeration of all maximal safe sets for m <= 6 against kissat
    verdicts on the generated CNFs (both directions).
(c) **Witness band sweep**: def-mode SAT instances for m = 4.. until UNSAT onset;
    each witness configuration independently verified (safety + maximality + deficiency,
    exact integer arithmetic, third system in Python against curve_packing geometry).
(d) **Witness-free sweep**: def-mode UNSAT as far as the run budget allows, honest
    INDET beyond; if a run ever completes the sweep to m = T_{3,4} = 69 (= K0318
    packing_U = old_T min(A,B); for q=4 the packing theorem gives no improvement since
    d1 = C(r-1,3) = 0 and cross_cost = 0, so the closure target is the K0024 bound),
    the closure M_{3,4} = onset follows by the K0077-precedent combination
    (finite exclusion + analytic upper bound) and is published as a new knowledge item.
(e) Publication (experiment dir + K item + log + knowledge README bullet), K number
    triple-checked at push time. Band-only publication if the sweep does not reach 69.

## Acceptance conditions (fail-closed)

1. Pins: sat.js md5 0cc6021a4e523a0d7f4d5ea0f5f5d40c, sat2.js md5
   282ae832efa0080127c6c153e65e1c3c (four-row lane verbatim, unmodified),
   kissat 4.0.4 linux-amd64 md5 3a5eba830aa6008a604fcc9bbe99a325,
   curve_packing_fixed_width.py from commit 49891aaf (K0318 artifacts).
2. Reduction argument stated and audited: for m >= q = 4, def-mode UNSAT iff every
   maximal safe set has all three rows at capacity q-1 = 3, i.e. total capacity 9
   (row lines are forbidden curves with m >= 4 points; row cap 3 per safety clause).
3. Brute-force cross-checks must agree with SAT verdicts on every probed instance
   before any witness or band claim is pushed.
4. Every SAT record publishes a witness verified by two independent systems (JS lane
   verifier + Python curve_packing-geometry verifier).
5. Every push is fetch-back byte-verified against the pinned commit SHA; latest main
   is re-fetched before each part-push; on fetch/push failure the situation is
   recorded and deferred, never forced.
6. K number for the new item is triple-checked at push time (items dir, README
   heading max, latest commit messages).

## Non-goals

- No claim about w=4 q>=6 (closure lane db6660813b owns q7 closure and band
  extension), w=4 q=6 widths >= 30, w=5 (lane 92722ac3), w=6 q=8 (band-closure
  lane), w=7 (K0827), n9-ge19, fold lanes, or the standard 11x11 board and its
  UNKNOWN classes.
- No claim that the packing bound can be improved at q=4; the sweep uses U = 69
  as-is (it equals min(A,B) for this shape, stated as a fact, not as a new result).
