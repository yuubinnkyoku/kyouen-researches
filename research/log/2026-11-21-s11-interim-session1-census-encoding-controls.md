# s_11 decision lane session 1: census n=10..12 into K0057, fixed encoding, control ladder (interim; s_11 remains 8..10)

Date: 2026-11-21 (sessions 07:20Z..~09:00Z). Lane: standard-board minimal-maximal s_n
(K0026/K0312/K0147/K0148/K0149 family); single-owner declaration
[a45a626d](../experiments/s11-minimal-maximal-8-9-decision-20261121/README.md) (07:22Z).
Experiment dir: [s11-minimal-maximal-8-9-decision-20261121](../experiments/s11-minimal-maximal-8-9-decision-20261121/README.md).

## Outcome of this session

No s_11 verdict yet: all (11, k) decision runs are INDET at freeze
([s11-minimal-maximal-8-9-decision-20261121 snapshot](../experiments/s11-minimal-maximal-8-9-decision-20261121/records/kissat_inprogress_snapshot.txt); n11_k10 --sat at 491s / 893k conflicts still running under
the background driver). The published bound 8 <= s_11 <= 10 (K0312 + K0320) is unchanged. What this
session did produce, and pushed to main:

1. **K0057 filled in** with the previously missing n=10/11/12 collinear/cocircular quartet splits
   (D_10 = 5,928 / C_10 = 48,513, D_11 = 10,428 / C_11 = 85,242, C_12 = 141,272 from published
   F_12 = 158,426 and D_12 = 17,154), the 4+-point curve catalog stats for n=10..12 (lines
   154/232/326, circles 12,170/20,847/34,031 with full size histograms), and the 16-point lattice
   circle of the n=12 grid (center (5.5,5.5), r^2 = 65/2). Validation stack: the System A catalog
   census reproduced every published anchor (F_5..F_12, D_7/8/9, D_12, n=12 line sensor 326,
   C_12/n^5 = 0.568 ratio, n=9 12-point circle count 4); D_n was double-implemented by a
   circle-free primitive-direction enumeration (d_count.py) agreeing on all n=5..12; the
   >=12-point circle counts were triple-implemented by a half-lattice center scan (big_circle.py):
   n=9: 4, n=10: 9, n=11: 21, n=12: 42 = {12:37, 14:4, 16:1}.
2. **Control ladder for the decision encoding, all PASS** (pinned kissat 4.0.4
   md5 3a5eba830aa6008a604fcc9bbe99a325): n=5 k=4 UNSAT / k=5 SAT (s_5 = 5), n=7 k=6 UNSAT
   (71s, 798,605 conflicts) / k=7 SAT (14s, model = the published K0031 witness stone set,
   geometr. verified), plus clause-level solver-independent positive/negative checks
   (cnf_check.py): K0320 witness satisfies all 523,640 clauses of n11 k=10; its 9-stone subset
   violates exactly 17 cover clauses; the K0031 witness satisfies all 40,311 clauses of n7 k=7
   and violates exactly the one cardinality unit clause of n7 k=6.
3. **Encoding bug found and fixed** (this is why controls matter): the v1 sequential counter read
   s[(i,j)] where s[(i-1,j)] was intended (self-reference), making cardinality clauses vacuous.
   v2 is deterministic; all nine CNF instance md5s are pinned in [cnf_md5_pins.txt](../experiments/s11-minimal-maximal-8-9-decision-20261121/records/cnf_md5_pins.txt) and were
   reproduced byte-identically across three environment resets (each reset = rebuild + md5 match).
4. **Negative neighborhood hunt recorded**: around the K0320 10-stone witness, all remove-1 nets
   non-maximal; remove-2/add-1 net (45 pairs x ~113 candidates = 5,085) contains no 9-stone
   maximal safe configuration (8.1s). Labeled as a failed local search, NOT a nonexistence result;
   neighborhood distance >= 3 unexplored.
5. **Fundament (fund) encoding lemma documented**: adding one clause "some stone lies in the D4
   cell-orbit transversal" (|F| = 21 on 11x11) is equisatisfiable with the plain instance
   (D4-invariance of safety/cover/cardinality + orbit transversality); used to accelerate SAT-side
   hunting. Any fund-SAT witness will still be decoded and geometry-verified before any claim.

## Failures / lessons (as-is, for the record)

- Three foreground 115s timeouts reset the execution environment mid-session (lesson already
  operationally applied: no compute+sleep combos in one call; background driver via nohup only;
  pure-Python Fraction scans at n=11 scale restricted to stone-triple transports).
- The /proc-scan kill-loop pitfall (self-match on own command strings) nearly killed the driver;
  avoid process management by string matching entirely.
- cnf_check.py v1 misclassified the s-counter base clause (-s[(1,1)], x_0) as a t-aux definition
  (shifting all counter assignments by one); caught immediately by the negative control refusing
  to fail in the predicted pattern. v2 classifies t-auxa by ">= 3 definition clauses".

## Next (same lane, not redeclared — covered by a45a626d)

- Observe the driver to verdict: n11_k10 --sat (positive control), n11_k9fund --sat (if SAT:
  s_11 <= 9 with witness decoding + verification, then n11_k8fund decides 8 vs 9; if UNSAT:
  s_11 = 10 given K0320's 10-stone maximality), then the n9 control pair.
- Only after verdicts: K0312 status update, K0149/K0147/K0148 impact notes, result log.

Not claimed here: any s_11 value, any s_n for n >= 12, any monotonicity statement, any reading of
conflicts counts as win/loss. Nodes/conflicts are not verdicts; a cut run is INDET.
