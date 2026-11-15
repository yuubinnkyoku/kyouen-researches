# 5x26 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0837 (5x25 witness-free).

## Status

IN FLIGHT — sweep started. Scripts and the 56 CNFs (17 direct classes +
{0},{1} k=0..4 + k=5 x minpos=0..12 + 2 lex=H + 5x18 positive control) are
generated; raw logs will be pushed batch-by-batch as instances decide.

## Claim

Witness frontier of (5,7): widths 19..25 are verified witness-free
(K0738-K0759, K0816, K0821, K0834, K0835, K0836, K0837); this lane decides
5x26. Witness-free would extend the set to {19,...,26} (M = 19 or >= 28 in
the K0821-audit sharp form); a witness would give M >= 27. Upper 158
(K0332 substitution) unchanged.

## Setup

- mkcnf.sh: 56 CNFs. The m=26 minpos sound bound is floor((m-1)/2) = 12
  (13 points per class, same as m=25: for columns 0..25, min(x_min,
  25-x_max) <= 12 since x_min <= x_max).
- qrun.sh: 2-worker claim-directory queue runner (timeout caps per batch).
- sat.js/sat2.js/sat3.js: byte-identical to the K0836/K0837 lane scripts.
- Positive control 5x18 class {0} must reproduce SAT 343,134 conflicts
  bit-exactly (fifth cross-lane reproduction, K0821/K0834/K0835/K0836/K0837).
