# 5x28 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0839 (5x27 witness-free).

## Status

IN FLIGHT — sweep of 5x28 started; results will be pushed batch-by-batch as
raw kissat logs. This file will be updated to COMPLETE when all 58 instances
are decided. Knowledge item (planned): K0840.

## Claim (in progress)

Witness frontier of (5,7): widths 19..27 were verified witness-free
(K0738-K0759, K0816, K0821, K0834, K0835, K0836, K0837, K0838, K0839); this
lane decides 5x28. If all deciding instances are UNSAT, the witness-free width
set of (5,7) becomes {19,...,28}; set form M_{5,7} in {19,...,28} or >= 29;
sharp form (K0821-audit convention) M = 19 or >= 30. Upper 158 (K0332
substitution) unchanged. Frontier would move to 5x29.

## Method (identical to the K0836..K0839 lanes)

- 17 direct row-mirror-canonical deficiency classes by kissat 4.0.4
  class-split SAT; {0},{1} by the complete k x minpos decomposition
  (k=0..4 + k=5 x minpos=0..13 — at m=28 the minpos sound bound stays
  floor((m-1)/2)=13, 14 points per class; columns 0..27:
  min(x_min, 27-x_max) <= 13).
- lex=H cross-encoding re-checks on {0,1},{2}; positive control 5x18 class
  {0} (K0332 witness board; expected SAT 343,134 conflicts bit-exact with the
  seven lane controls).
- sat.js/sat2.js/sat3.js are byte-identical to the K0836..K0839 lane scripts
  (restored from the m=27 lane directory; blob sha verified against main).
- CNF set: 58 (17 direct + 38 k/minpos + 2 lexH + 1 control), built by
  mkcnf.sh.

## Resume procedure (if this session dies mid-sweep)

1. Restore kissat 4.0.4 linux-amd64 and the 5 scripts from this directory
   (byte-compare via git blob sha against main).
2. Regenerate all 58 CNFs with mkcnf.sh.
3. Re-run the 5x18 positive control (expect SAT 343,134 conflicts bit-exact)
   as calibration.
4. Complete the remaining instances with qrun.sh (CAP 280s, 2 workers).
5. Push raw logs batch-by-batch; rebuild records/summary with
   mkrecords5728.js.
