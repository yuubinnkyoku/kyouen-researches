# 5x27 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0838 (5x26 witness-free).

## Status

IN FLIGHT — this lane decides 5x27 q=7 (witness frontier of (5,7)). CNF set
is 58 (17 direct classes + {0},{1} krow k=0..4 + k=5 x minpos=0..13 + 2 lex=H
cross-checks + 5x18 positive control). Scripts are byte-identical to the
K0821..K0838 lanes (sat.js/sat2.js/sat3.js restored from the m=26 lane, git
blob sha verified); mkcnf.sh/qrun.sh ported for m=27 (minpos sound bound grows
to floor((m-1)/2)=13: for columns 0..26, min(x_min, 26-x_max) <= 13 since
x_min <= x_max). Positive control must reproduce 5x18 class {0} SAT 343,134
conflicts bit-exactly (sixth cross-lane reproduction). Raw logs are pushed
batch-by-batch.

## Claim under test

No row-deficient maximal safe configuration exists on 5x27 q=7 (i.e. 5x27 is
witness-free; every maximal safe configuration has 30 stones). If UNSAT
holds for all 53 deciding instances, the witness-free width set of (5,7)
extends to {19,...,27} and the sharp form becomes M_{5,7} = 19 or >= 29;
the frontier then moves to 5x28. A SAT would give M_{5,7} = 28 exactly
(witness at 27 forces M >= 28; widths 20..26 are verified witness-free).

## Protocol (K0816/K0821/K0834..K0838)

- 19 row-mirror-canonical deficiency classes; 17 direct + {0},{1} by the
  complete k x minpos decomposition (k = 0..4 exact deficient-row count;
  k = 5 x minpos = 0..13, 14 points per class at m=27, 28 sub-instances).
- kissat 4.0.4 (official linux-amd64 release binary), 2-worker qrun.sh with
  per-instance caps; raw logs pushed per batch.

## Resume protocol (proven across resets in K0835/K0837/K0838)

1. Regenerate CNFs with the byte-identical encoders (mkcnf.sh).
2. Calibrate: re-run 1-2 already-decided instances and compare conflicts with
   the main logs bit-exactly.
3. Run the remaining instances via qrun.sh; push raw logs batch-by-batch.
4. Build records/summary (mkrecords port), report.md, K item, research log,
   results CSV/README rows.
