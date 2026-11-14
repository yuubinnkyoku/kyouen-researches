# 7×m q=9 / q=10 row-deficient witness bands — kissat cross-check, band extension, and new (7,9) witnesses (2026-11-14)

## Claim

1. **(7,9)**: On the 7×15..7×23 integer grids (q=9, q点共円/共線禁止), row-deficient
   maximal safe configurations **exist** (55 stones vs. full capacity 56; m=15 witness has
   54). All witnesses are dual-verified (census-free JS verifyConfig + Python Fraction).
   Combined with `seven-row-inband-families-20261114` (witnesses at m=9..14), the witness
   width set of (7,9) includes **{9..23}**.
2. **(7,9)**: On the 7×24..7×60 integer grids, the def-mode instance ("some row has ≤ 7
   stones", no lex) is **UNSAT** for kissat 4.0.4 (exit 20). Widths 24 and 33 are
   re-checked UNSAT with the independent def+lex=H,V,HV encoding (81,997 / 38,424
   conflicts); the extended band endpoints 52 and 60 are likewise re-checked UNSAT with
   def+lex=H,V,HV (25,855 / 19,373 conflicts). Hence the witness-free band of (7,9)
   contains **{24..60}**, and **M_{7,9} = 24 or M_{7,9} ≥ 61** (M ∈ {24} ∪ [61, 613];
   upper bound 613 by K0318 curve-packing substitution, recorded in the source
   experiment's w7_upper_bounds.json).
3. **(7,10)**: The `seven-row-inband-families-20261114` fastsat UNSAT band (m=19..40,
   def+lex=H,V,HV) is **independently confirmed by kissat 4.0.4** on regenerated CNFs —
   the regenerated CNFs are the same instances (fastsat conflicts bit-exact for all 22
   widths: 3,215 / 3,395 / 3,486 / 3,104 / 2,899 / 2,105 / 3,158 / 3,142 / 7,243 / 3,793 /
   4,122 / 4,486 / 11,408 / 4,804 / 2,179 / 11,809 / 3,628 / 41,278 / 3,866 / 4,458 /
   3,195 / 4,702) and kissat returns UNSAT for every width. The band is **extended to
   m=41..51** (both fastsat and kissat UNSAT; worst 15,399 fastsat conflicts at m=46)
   and further to **m=52..60** (kissat 4.0.4 UNSAT per width, lean2.sh; 888–1,634
   conflicts; m=52/60 def+lex=H,V,HV cross-checks UNSAT at 1,033 / 1,020 conflicts).
   With the m=10..18 witnesses of the source experiment, the witness width set of (7,10)
   is {10..18} and the witness-free band is **{19..60}**: **M_{7,10} = 19 or M_{7,10} ≥ 61**
   (M ∈ {19} ∪ [61, 587]; upper bound 587 by K0318 substitution).

## Method

Encoding: `sat2.js` from `seven-row-inband-families-20261114` (verbatim; K0810
`sat.js` census of circleABC integer triples + line pairs, sequential counter, maximality).
The def mode adds the single clause "∨_y ¬rowGe[y]" (some row ≤ q−2 stones), which is
exactly "deficient" because safety caps every row at q−1 (rows are length-m ≥ q lines);
the clause is invariant under H/V/HV, so the lex-leader constraints used on the (7,10)
band are sound (orbit-min satisfies all constraints). For the (7,9) witness search no
lex constraints are used (lex hurts the SAT side; K0815 dai-4 lesson), and the def-no-lex
band instances are the complete encoding of "exists row-deficient maximal safe
configuration". Solvers: kissat 4.0.4 (official linux-amd64 binary) and fastsat.js
(verbatim from the source experiment) for calibration/cross-check.

## Memory-bounded regeneration (genfast.js) — the m ≥ 52 census wall

`sat2.js`'s census (`S.buildCensus`) enumerates ALL point triples to find circles: a
circMap with C(n,3) entries. For 7×m grids this crosses the container memory limit
abruptly: 7×51 (n=357, C=7.55M triples) still fits, 7×52 (n=364, C=7.98M) is OOM-killed
even with `--max-old-space-size=2560` (rc 137), for both q=9 and q=10 — while the CNF
itself is tiny (≈8.2k vars / 29.9k clauses at 7×52 q=9). Only the census blows up.

`scripts/genfast.js` replaces the census (by monkey-patching `S.buildCensus` and reusing
ALL of sat2.js's encoding/dump logic verbatim — zero encoding drift) with a
half-integer-center enumeration: a circle meets any row in ≤ 2 grid points, so a circle
with ≥ w+1 points has a same-row pair, and its center's x-coordinate u = (x_a+x_b)/2 is
a multiple of 1/2 in [0, m−1]. For each of the 2m−1 candidate u, every distinct-row pair
(p,q) solves the center's y exactly (rational), and true q-point circles accumulate
≥ C(q,2)−(q−w) ≥ 13 pair-witnesses (vs threshold 12); candidates get an exact integer
point-set scan. Lines reuse the original pair enumeration. **Curve insertion order
replicates buildCensus exactly** (lines by their two smallest point indices, circles by
their three smallest, lines before circles) so the DIMACS is byte-identical.

**Validation**: genfast CNFs are byte-identical (`cmp`) to sat2.js CNFs on **12 samples**:
(7,34,9), (7,45,9), (7,51,9), (7,51,10), (7,19,10), (7,40,10)+lex=H,V,HV,
(6,21,7), (6,22,8), (5,21,6), (5,22,7), (7,30,9) --cap=40 --counter=tot,
(7,30,9) --rowY=3 — across modes deficient/cap+totalizer/rowfixed, with and without lex.
genfast asserts q ≥ w+1 (below that the half-integer-center guarantee fails; use sat2.js).
Generation cost: 2.7 s at 7×52 (vs OOM); lean2.sh = genfast + kissat + (SAT: dual verify).

## Verification protocol

- Controls: 2×8 q=4 SAT (fastsat 121 conflicts — bit-exact with the source experiment's
  results.jsonl; kissat SAT 37 conflicts) and 2×9 q=4 UNSAT (fastsat 535 — bit-exact;
  kissat 316), consistent with M_{2,4}=9 (K0796).
- Calibration: for every (7,10) width m=19..40 the regenerated CNF reproduces the
  source experiment's fastsat conflict count **bit-exact**, proving the instance
  identity; kissat then gives independent UNSAT verdicts.
- Witness verification: every SAT model is decoded to stones and verified by two
  independent implementations (sat.js verifyConfig census-free JS; verify_witness.py
  Python Fraction — pairs-of-stones lines / triples-of-stones circles) as safe +
  maximal + row-deficient. 9/9 new (7,9) witnesses PASS both.
- Second encoding: (7,9) UNSAT widths 24, 33, 52, 60 re-checked with def+lex=H,V,HV;
  (7,10) widths 52, 60 likewise (all UNSAT).
- Determinism: all recorded numbers survived **two execution-environment resets** and
  were re-run bit-exact (fastsat calibration set and kissat conflicts identical
  across resets).
- Negative observation (honest limitation): fastsat could **not** confirm the (7,9)
  UNSAT band within a 60 s cap at m=24 (210k conflicts, TIMEOUT); the (7,9) band
  evidence is kissat-only (+ lex cross-encoding at 2 widths), unlike the (7,10) band
  where both solvers agree.

## Results

- q9-witness-search/records.jsonl: 50 records — SAT m=15..23 (witnesses in
  s7xMq9_none.witness.json), UNSAT m=24..60 (m=34..45 via lean1.sh/sat2.js,
  m=46..60 via lean2.sh/genfast.js), lex cross-checks at m=24/33/52/60.
- q10-band/records.jsonl: 44 records — m=19..60 all UNSAT (m=19..40 confirmation,
  m=41..51 fastsat+kissat extension, m=52..60 kissat lean2 extension + m=52/60
  lex cross-checks).
- controls/records.jsonl: 2×8/2×9 q=4.

## Scope and limits

Finite machine verification, up to census completeness (all lines/circles with ≥ q grid
points enumerated by the K0810 census or the validated genfast census) and solver
correctness (kissat 4.0.4; fastsat for the calibrated (7,10) band m=19..51). Not a
number-theoretic proof. Determining M_{7,9} = 24 exactly needs persistence at m=61..612
(or a K0342-style tail bound); M_{7,10} = 19 needs persistence at m=61..586. The
witness-search frontiers are 7×61 (q=9) and 7×61 (q=10).

## Reproduction

```sh
node sat2.js 7 24 9 --deficient out.cnf          # (7,9) band instance (no lex)
node sat2.js 7 24 9 --deficient --lex=H,V,HV o2  # lex cross-encoding
node sat2.js 7 40 10 --deficient --lex=H,V,HV o3 # (7,10) band instance
./lean1.sh 7 24 9 <outdir> [LEX]                 # encode + kissat + (SAT: dual verify)
./band1.sh 7 40 10 H,V,HV <outdir>               # encode + fastsat + kissat + record
./lean2.sh 7 52 9 <outdir> [LEX]                 # genfast encode (m>=52) + kissat + record
node genfast.js 7 52 9 --deficient out.cnf       # memory-bounded generator (q >= w+1)
node decode_verify.js 7 23 9 model.txt           # kissat model -> stones -> verifyConfig
python3 verify_witness.py 7 23 9 < stones.json  # Python Fraction independent check
```

sat2.js / sat.js / fastsat.js / verify_witness.py are verbatim from
`research/experiments/seven-row-inband-families-20261114/scripts/` (not duplicated here).
CNFs are deterministically regenerable and not stored (vars/clauses/curves are in the
records); raw kissat logs are stored per instance.
