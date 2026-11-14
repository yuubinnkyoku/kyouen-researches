# scripts

- `lean1.sh` — one def-mode (w,m,q) instance: deterministic CNF, kissat 4.0.4 verdict,
  on SAT decode + dual verify (decode_verify.js + verify_witness.py), JSONL record.
  Optional 5th arg: lex list (e.g. `H,V,HV`) for the second-encoding cross-check.
- `band1.sh` — one def+lex instance: fastsat calibration + kissat independent verdict, JSONL record.
- `decode_verify.js` — kissat v-line model → stones (cell var i+1 = cell[y*m+x]) →
  sat.js verifyConfig (census-free).

sat2.js / sat.js / fastsat.js / verify_witness.py are used **verbatim** from
`research/experiments/seven-row-inband-families-20261114/scripts/` (K0810 census core);
they are not duplicated in this experiment. Paths inside the shell scripts point to
`/home/user/krwork/seven/scripts/` (session workspace); replace with the source
experiment's scripts directory when re-running.

kissat 4.0.4 official linux-amd64 release binary (GitHub rel-4.0.4) is used unchanged.
