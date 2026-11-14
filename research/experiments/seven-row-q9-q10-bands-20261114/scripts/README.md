# scripts

- `lean1.sh` — one def-mode (w,m,q) instance: deterministic CNF, kissat 4.0.4 verdict,
  on SAT decode + dual verify (decode_verify.js + verify_witness.py), JSONL record.
  Optional 5th arg: lex list (e.g. `H,V,HV`) for the second-encoding cross-check.
- `lean2.sh` — same contract as lean1.sh but encodes with genfast.js; required at
  m>=52 (w=7) where sat2.js's all-triples census is OOM-killed in this container.
- `band1.sh` — one def+lex instance: fastsat calibration + kissat independent verdict, JSONL record.
- `genfast.js` — memory-bounded CNF generator: monkey-patches S.buildCensus with a
  half-integer-center circle census (O((2m)n^2) time, O(n^2) memory) and reuses ALL of
  sat2.js's encoding/dump logic verbatim. Byte-identical CNF to sat2.js on 12 validation
  samples (deficient / cap+totalizer / rowfixed, lex on/off, w=5,6,7). Asserts q >= w+1
  (the half-integer-center guarantee needs a same-row pair on every q-point circle);
  below that, use sat2.js. m=52 (7-row) encodes in 2.7 s vs OOM. See report.md
  "Memory-bounded regeneration" for the correctness argument (curve order replicated
  exactly: lines by two smallest point indices, circles by three smallest).
- `decode_verify.js` — kissat v-line model → stones (cell var i+1 = cell[y*m+x]) →
  sat.js verifyConfig (census-free).

sat2.js / sat.js / fastsat.js / verify_witness.py are used **verbatim** from
`research/experiments/seven-row-inband-families-20261114/scripts/` (K0810 census core);
they are not duplicated in this experiment. Paths inside the shell scripts point to
`/home/user/krwork/seven/scripts/` (session workspace); replace with the source
experiment's scripts directory when re-running.

kissat 4.0.4 official linux-amd64 release binary (GitHub rel-4.0.4) is used unchanged.
