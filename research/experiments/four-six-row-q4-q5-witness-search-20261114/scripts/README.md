# scripts

- `lean4.sh` — one (w,m,q) def-mode instance runner for the
  four-to-six-row q=4/q=5 families (adapted from the
  seven-row-q4-q6-witness-search-20261114 `lean3.sh`):
  sat2.js CNF (kissat verdict, cap from env `KSCAP`, default 100 s;
  rc 10 = SAT, 20 = UNSAT, other = INDET), on SAT decode +
  dual verify (decode_verify.js + verify_witness.py), JSONL record.
  Primary encoding: `--lex=H,V,HV` (the raw def-mode OR encoding is
  dramatically harder — control (3,23,4): INDET 445k conflicts at 100 s
  without lex, SAT in 17.7 s / 66,895 conflicts with lex; verdicts are
  isometry-invariant, so lex changes search only).
- All JS/PY scripts are used **verbatim** from
  `research/experiments/seven-row-inband-families-20261114/scripts/`
  (K0810 census core: sat.js, sat2.js, verify_witness.py) and
  `research/experiments/seven-row-q9-q10-bands-20261114/scripts/`
  (decode_verify.js). Not copied here; see that experiment for sources
  and calibration history.
- genfast.js is deliberately NOT used in this lane: its PAIRTHRESH=12
  pair-witness floor is unsound for (4,5) since the minimum distinct-row
  pair witnesses of a 5-point circle is C(5,2)-(5-4)=9 < 12; the target
  families have q <= w+1 and small n, where the sat2.js all-triples
  census is cheap and byte-stable.
- kissat 4.0.4 official linux-amd64 release binary (GitHub rel-4.0.4), unchanged.
