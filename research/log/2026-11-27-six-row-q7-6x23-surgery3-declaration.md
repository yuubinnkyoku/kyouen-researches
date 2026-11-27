# Six-row q7 6x23 bounded surgery (3-for-3) around the m22 witness: single-owner declaration

- Date: 2026-11-27
- Lane: fast lane (witness-side bounded surgery), publish-then-execute
- HEAD pinned at declaration: 55b65a7f (main, 2026-11-27T14:27:56Z)
- Scope owner: this declaration claims the witness-side bounded-surgery sweep
  around the six-row q7 6x22 class {2} krow=2:5 deficient maximal witness
  (35 stones, rows [6,6,5,6,6,6], kit 03487c4b, K0815 dai-8) placed on 6x23.
- Complementary to, and disjoint from, the declared SAT-side minpos-rest sweeps
  (6x23 class {2} f43cd66b, 6x26 e61acf82); those lanes are NOT touched.

## Pre-registered search space

- Board 6x23, q=7, safety = no integer line/circle with >= 7 stones,
  maximality = every empty cell on a line/circle with >= 6 stones.
- Bases: the 8 placements of the m22 witness spanning 23 columns:
  shift dx in {0,1} x mirror-x (width 23) x mirror-y (rows 6).
- Surgery: S = base - R + A with |R| <= 3, |A| <= 3, final size <= 35
  (deficient: <= w(q-1)-1 = 35), column span exactly 23 (stones in both
  edge columns), safe and maximal on 6x23.
- Official sweeps: 3-for-3 (rmax=3, amax=3) on all 8 bases; 2-for-2
  (rmax=2, amax=2) on all 8 bases is run first as a quick sub-sweep.

## Pre-registered interpretation

- HIT (any deficient maximal safe 6x23 witness found, size <= 35, span 23):
  M_{6,7} >= 24 (currently [23,402]); the witness is dual-verified
  (independent Fraction verifier + negative controls) and promoted to
  K0815 + results/fixed-width/mwq_stabilization.csv.
- ALL-NEGATIVE: honest bounded local negative around this witness orbit
  (NOT an absence claim for 6x23); recorded as a completion log only,
  bounds unchanged.

## Engine and calibration (fresh implementation, session 2)

- surgery_engine.py / surgery_v3.py: complete enumeration with
  keep_min = q - amax base-curve table (safety exactness), anchored
  curve generation at each uncovered cell (blocking exactness for
  q-1-amax >= 2), and exact-cover branching over coverage + edge-column
  tasks (completeness: every valid A has a minimal representative found).
- Disclosed defect history of the session-1 draft (INVALIDATED, never
  published): (1) circumcircle_key returned -(u,v,w)/2 of the true circle
  parameters (bijective but wrong key circle: counts right, membership
  broken); (2) Anchored generated the degenerate self-line 0=0 for a
  removed-stone cell, fake-blocking it. Session-1 preliminary sweep
  outputs are withdrawn; nothing from session 1 enters the record.
- Session-2 calibration (all re-run from scratch):
  - circumcircle_key unit tests on known circles (incl. the 6-stone
    witness circle x^2+y^2-7x-5y+6=0).
  - Witness reproduction: 6x22 safe+maximal (verify_full, independent
    Fraction); on 6x23 the unique unblocked cell is exactly (22,2) at
    dx0 and (0,2) at dx1 (both verify_full and table agree).
  - Random cross-calibration: 100 random near-base configurations
    (|R|,|A| <= 3), engine verdict vs verify_full: 0/100 mismatches.
  - Positive control: base + (22,2) (36 stones, rows [6,6,6,6,6,6]) is
    safe+maximal on 6x23 but NON-deficient; the sweep redisCOVERS it
    when the size cap is lifted (rmax=0, amax=2) - expected, recorded
    as a non-deficient observation, not a lower bound.
  - Branch completeness: for all 631 removal classes of the 2-for-2
    space, branch solutions equal the brute-force minimal cover
    representatives (17 redundant supersets at rm=() all explained,
    0 unexplained).
- Preliminary (pre-declaration, disclosed): 2-for-2 on dx0 produced zero
  size-feasible candidates (no (R,A) with |A| <= |R| <= 2 covers all
  uncovered cells + edge columns), consistent with the published
  T-cell one-stone-short negatives at 6x22 (252f41db) and 6x26 q6
  (7081aa2b). Official 2-for-2 on all 8 bases will be re-run.

## Execution plan

- Checkpointed driver sweep3.py; state/hits JSONL per basis; each basis
  sweep is deterministic and re-runnable; results byte-compared on rerun.
- On completion: kit under research/experiments/ (engine, driver,
  calibration outputs, results, MANIFEST-sha256.txt) + completion log.

verdict NOT consumed, closure class UNKNOWN at all times, 11x11 UNKNOWN.
