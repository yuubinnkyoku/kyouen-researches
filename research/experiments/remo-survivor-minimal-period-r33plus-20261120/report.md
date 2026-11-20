# REMO survivor-column minimal period, r = 33..48 (K0925 S32 -> S48, K1145)

Declared fast-lane follow-up of [K0925](../../knowledge/items/K0925-remo-survivor-minimal-period-r32.md)
(single-owner note: `research/log/2026-11-20-remo-survivor-witness-r33plus-single-owner-note.md`).
Method is verbatim K0925 W5: for the uniform-board counting recursion
E(C,r) (K0859 Theorem D) with Q(r) = lcm(1..r),

* positive direction (K0919 THEOREM PER / K0925 THEOREM W+, universal,
  every C >= 1): Q(r) is a period of the survivor column,
* LEMMA DIV (K0922): the survivor column's minimal period divides
  Q(r),
* so it is exactly Q(r) iff every PROPER divisor d of Q(r) is
  rejected by one witness C with S(C+d,r) != S(C,r),
  witness minimal ascending in [1,150], fallback [151,1500].

## Theorem S48 (machine, r = 33..48)

Every proper divisor of Q(r), r = 33..48, is rejected by a witness
C <= 150; the fallback window was never needed and no divisor
remained unwitnessed.  With LEMMA DIV the survivor column's minimal
period is exactly Q(r) for every r = 33..48 (combined with K0925
THEOREM S32: swept range r = 2..48).  Trust boundary identical to
K0925 S32: the survivor dynamics are the published survivor_fast
(closed-form share-count rewrite, pinned to the verbatim per-stone
K0859 recursion), and the minimality statement is per-r column
eventual periodicity claims that LEMMA DIV reduces to the (proper
divisor rejection + positive period) finite facts above.

## The sweep

1,548,272 proper divisors total (Q(48) = 4.43e20 has 294,911 proper
divisors, enumerated from the factorization e_p = max{a : p^a <= r};
trial division to sqrt(Q(48)) ~ 2.1e10 is infeasible, so S0 pins the
factorization-based enumeration against trial division for r = 2..20
and the analytic exponent pattern for r = 33..48).

| r | proper | unwit | wit_max | Q//argmax | C=1 not wit | fallback |
|---|---|---|---|---|---|---|
| 33-36 | 18431 | 0 | 25 | 29 | 9146 | 0 |
| 37-40 | 36863 | 0 | 35 | 37 | 18024 | 0 |
| 41-42 | 73727 | 0 | 29 | 37 | 35584 | 0 |
| 43-46 | 147455 | 0 | 30 | 31 | 70365 | 0 |
| 47-48 | 294911 | 0 | 39 | 47 | 139189 | 0 |

Simulation count 2,959,796 (~1.9 per divisor); witness C=1 succeeds
for 808,586 divisors (52.2%); the witness histogram at r = 48 is
C=1: 155,722, C=2: 78,994, C=3: 29,495, C=4: 17,029, C=5: 5,848,
C=6: 3,888 (full histogram in the audit).

## Observations (finite, r = 33..48 unless noted)

1. **Bounded witness extended**: wit_max_sv <= r-1 holds for every
   r = 33..48 (max 39 at r = 47,48).  Combined with K0925 the
   observation now covers r = 2..48 (global max 39).  The witness
   -maximal divisor is again of the form Q/p with h* = 1 (M_1
   failure; here p = 47, v_47(r) = v_47(Q(r)) = 1).
2. **Equal-Q witness-stream identity (new, sha-pinned)**: within each
   equal-Q block {r : lcm(1..r) = Q} the ENTIRE per-divisor witness
   stream d -> w is identical across the block (the audit pins each
   r's stream by a chained sha256; blocks {17,18}, {19..22},
   {23,24}, {25,26}, {27,28}, {29,30}, {32..36}, {37..40}, {41,42},
   {43..46}, {47,48} all have one shared stream sha; r = 31 is a
   singleton Q(31) = Q(32)/2 block).  K0925's published aggregates
   already coincided within blocks; the stream sha sharpens this to
   "every single witness decision is r-invariant inside the block".
   The witness map is a function of (Q, d) there, not of r.  No
   proof is attempted here; K0926's plateau theory (S(C,r) = P(C)
   for C <= r-1) explains the small-C side but not the r-invariance
   of the S(C+d,r) side. Observation only, recorded as a question:
   does the block-identity follow from the K0926/K0928 reduction
   structure?

## Machine checks (audit.json, 5/5 ok, sha256 0b5ae7eb5f840c038e66d3712f599a21741ccafc1665ba545a38cb7fbebfb0b8)

* S0 divisor enumeration pin (factorization == trial division
  r = 2..20; analytic pattern r = 33..48).
* S1 K0925 reproduction: r = 17..32 recomputed
  (proper/unwitnessed/wit_max_sv/wit_argmax_over_Q/sv_C1_same) equal
  the published K0925 audit values verbatim (audit sha b3733ed5...),
  so this implementation's W5 semantics are exactly K0925's.
* S2 the main sweep r = 33..48 (aggregates + chained stream sha
  above).
* S3 positive period anchors: S(C+Q(r),r) == S(C,r) for C in
  [1,1500] plus anchors {Q-1, Q+1, Q+5, 2Q-1}, 24,064 comparisons,
  0 mismatches (machine anchor; universal proof is K0925 W+).
* S4 twin anchor at the new range: verbatim per-stone K0859
  recursion == closed-form twin == survivor_fast on the full
  (elim, survivor) pair for r = 33..48, C = [1,150] (2,400 pairs,
  0 mismatches; K0925 TWIN already covered r = 2..24).

Determinism: assemble runs twice per invocation and must be
byte-identical; two independent processes (separate cwd full
recomputation, one of them budget-resumed at shard boundaries) wrote
byte-identical `output/audit.json` (sha256 above; 32,790 bytes).
Per-(check,r) checkpoints live in `output/` and `--no-cache`
recomputes everything; CI runs the script fresh and `git diff`-pins
the audit.

## Out of scope

Universal survivor minimality (bounded-witness conjecture) stays
OPEN; nothing here concerns non-uniform boards or the 11x11 empty
board; no claim about r >= 49.

## Reproduce

```sh
python3 survivor_witness_r33plus.py            # full compute (~6 min fresh)
python3 survivor_witness_r33plus.py --no-cache # recompute ignoring checkpoints
```
