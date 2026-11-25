# scripts

- `lean3.sh` — one (w,m,q) def-mode instance: genfast.js CNF when q >= w+1
  (else sat2.js), kissat 4.0.4 verdict (240s cap), on SAT decode + dual verify
  (decode_verify.js + verify_witness.py), JSONL record. Optional 5th arg: lex list.
  Row-split runs (m=24/25 rowY=3) used sat2.js's `--rowY` mode directly
  (see report.md and ../output/row-split/records.jsonl).
- `sat2.js`, `sat.js`, `fastsat.js`, `verify_witness.py` are used **verbatim** from
  `research/experiments/seven-row-inband-families-20261114/scripts/` (K0810 census core).
- `genfast.js`, `decode_verify.js` are used **verbatim** from
  `research/experiments/seven-row-q9-q10-bands-20261114/scripts/` (K0820;
  genfast byte-identity to sat2.js re-validated for q=8 on 4 samples:
  ../output/controls/genfast_q8_byteidentity.json).
- kissat 4.0.4 official linux-amd64 release binary (GitHub rel-4.0.4), unchanged.
