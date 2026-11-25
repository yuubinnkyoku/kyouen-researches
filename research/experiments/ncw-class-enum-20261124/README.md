# ncw-class-enum-20261124: symbolic class-enumeration closure certificate (K1310 evidence addition)

Purpose: machine certificate for the **mex-closure algebra layer** of the
published K1310 hand proof (declaration note `research/log/
2026-11-24-ncw-window-single-owner-note.md` SS2.4/SS2.5 region tables), by
exhaustive **symbolic class enumeration**: the closure
`claim == mex(typed children)` is reduced to a finite case analysis over
label classes and every case is machine-checked.

This kit is an **evidence addition to K1310** (AGENTS.md: the same
proposition's evidence updates go into the same K item). It contains **no
new theorem and no new universal claim**: the universal laws T-NCW-P /
T-NCW-B, the typed-child identities, and their engine grounding stay in
the published K1310 package and its 51,439-point official audit.

## What the certificate adds

The published audit (verify_k1310.py D5) checks the typed-children closure
on **finite cells** (9,016 pts, vs the engine). This kit closes the gap
between "checked on finite cells" and "holds for all cells" *for the
closure arithmetic*, by:

1. **Partition**: domain cells are classified by comparison labels only
   (pair: pz/pg/gs(3)/ggs(5)/gzs(6)/tau(7)/m1/g1/k1; bed: pz/gs(5)/tb(5)/
   a1/k1; see the script docstring). Every realizable label combination
   has a concrete witness: **280 pair classes + 39 bed classes**.
2. **Determination + closure**: for each class, the claim and ALL typed
   child values are computed **symbolically from the label bits alone**
   (children: A-fall / A-compress, g=1 corner bed, m=1 B-exit single
   token, C-child pair/bed on (k-1, z-1) with the concession flip `1 ^`,
   k=1 C-child on the K1303 band row). `mex(children) == claim` is
   verified **per class**. Labels are functions of the cell; children are
   functions of the labels; per-class closure + partition proves the
   closure for **all** cells by finite case analysis (280 + 39 cases).
3. **Grounding (finite)**: a coverage census re-derives every cell's
   labels and requires agreement with the transcribed laws, the class
   tables, and mex closure; and requires the cell's label combination to
   hit an enumerated class (partition completeness). Default census
   z<=30, m<=12, g<=40, a<=14: **108,000 pair + 3,150 bed cells, bad 0**;
   deep census `34 16 44 20`: **203,456 + 5,780, bad 0**.
4. **Transcription gate** (`eqcheck.py`): imports the shipped
   `enum_classes.py` and compares its law implementations against
   verbatim transcriptions of the published K1310 kit's P / Bm /
   single_token / cpsfG over 1,031,085 points, bad 0.

## Files

- `enum_classes.py` self-contained (stdlib only), deterministic; argv
  `ZM MM GM AM` override the census box (default `30 12 40 14`). Prints a
  `RESULT:` line; exit code 0 iff every bad count and the missing-class
  count are 0 (fail-closed).
- `eqcheck.py` the transcription-equivalence gate above (also rc-gated).
- `output/` frozen outputs: `frozen_default.out`, `frozen_deep.out`
  (deep census), `predry1-4.out` (determinism runs), `eqcheck.out`, and
  the official audit runs + `detcheck.json` (published after fetch-back).
- `tamper/` the three pre-declared tamper variants `t1.py` (claim parity
  flip in `sym_claim_pair`), `t2.py` (concession flip `1 ^` removed from
  the pair C-child evaluator: the historical draft bug), `t3.py`
  (witness off-by-one hiding three classes), with their outputs: all
  rc=1 with the pre-declared FAIL counts.

## Chain

Single-owner declaration note published FIRST
(`research/log/2026-11-24-ncw-class-enum-note.md`), then this kit, then
fetch-back sha verification, then the official runs from the fetched-back
bytes, then the audit outputs + report log + the K1310 artifact entry.
