# six-row q=7 m=21 class-split witness — M_{6,7} >= 22

Date: 2026-11-14. First application of the K0818 class-split machinery (sat3.js on the K0810
census + sat2.js sequential-counter core, decided by the official kissat 4.0.4 linux-amd64
binary) to a q=7 board, attacking the (6,7) unresolved frontier width 6x21.

## Result

**6x21 q=7 class {2} is SAT — a 35-stone deficient maximal safe witness exists on 6x21**
(rows (6,6,5,6,6,6), one deficient row; kissat 1,904,706 conflicts / 98.6 s, no lex).
Therefore **M_{6,7} >= 22** (range 22..402; the K0318/K0024 upper bound 402 is unchanged).
This resolves the K0815 "6x21 unresolved (def+lex 4.55M conflicts single run)" frontier by
class splitting — a further confirmation that splitting the deficiency class collapses the
difficulty of the monolithic instance (cf. the K0815 dai-4 encoding observations).

## Witness

35 stones, rows (6,6,5,6,6,6); coordinates in `output/w67_21.json` (x = column 0..20,
y = row 0..5).

Dual independent verification, both PASS (safe and maximal):
- JS census-free `verifyConfig` (stone-pair lines / stone-triple circles, exact integer
  arithmetic) — ok, size 35, rows [6,6,5,6,6,6].
- Python Fraction verifier (`verify_py.py`, independent implementation, exact rational
  circumcenter via Cramer) — "6x21 q=7 size=35: True ok 35".

## Controls

- **Positive control**: 6x20 q=7 class {2} SAT — 641,859 conflicts / 29.1 s; decoded model
  35 stones rows (6,6,5,6,6,6) passes both verifiers. This is the K0815 dai-2 witness board
  rediscovered through the identical encode→solve→decode→verify path used for 6x21.
- Negative controls (same machinery, earlier session runs): 2x8 q=4 class {0} SAT (K0796
  rediscovered); 2x9 q=4 class {0} UNSAT (M_{2,4}=9 consistent).
- Determinism: identical DIMACS per (w,m,q,class); conflict counts from completed runs.

## Frontier after this run

6x22 q=7 class {2}: single 280 s run INDET at 5,038,264 conflicts (not absence; the other 34
canonical classes are unswept). The (6,7) witness frontier moves to 6x22.

## Scope

Witness existence only (no nonexistence claim at any width). 6x21 q=7 only for this witness;
the 11x11 empty board / two-stone root {49,60} / S2 {59,60} / class 2 / class 4 are unrelated
and remain UNKNOWN.

## Files

- `scripts/sat3.js` (+ `sat2.js`, `sat.js` core, verbatim from the K0818/K0810 lanes)
- `scripts/runall67.sh` — one-instance driver (encode → kissat 280s → decode if SAT)
- `output/records.jsonl` — 6x21 SAT / 6x22 INDET / 6x20 positive control
- `output/w67_21.json` — witness stones + JS verify result
- `output/summary.json` — aggregate
- `output/r6x21q7_c2.txt` — raw kissat SAT log (model included)
- `output/r6x22q7_c2.txt` — raw INDET log (frontier)
- `output/r_ctrl_6x20q7_c2.txt` — raw positive-control log (model included)
