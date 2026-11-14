# scripts

- `lean3.sh` — one (w,m,q) def-mode instance runner (identical to the
  seven-row-q8-witness-search-20261114 copy): sat2.js CNF when q < w+1
  (genfast.js inapplicable at q = w), kissat 4.0.4 verdict (240s cap),
  on SAT decode + dual verify (decode_verify.js + verify_witness.py),
  JSONL record.
- All JS/PY scripts are used **verbatim** from
  `research/experiments/seven-row-inband-families-20261114/scripts/`
  (K0810 census core: sat2.js, sat.js, fastsat.js, verify_witness.py)
  and `research/experiments/seven-row-q9-q10-bands-20261114/scripts/`
  (decode_verify.js). Not copied here; see that experiment for sources
  and calibration history (fastsat/kissat bit-exact controls,
  cross-reset determinism, genfast byte-identity).
- Row-split runs (m=25 rowY=0..3) used sat2.js `--rowY=Y` directly;
  see ../output/row-split/records.jsonl (200s caps).
- kissat 4.0.4 official linux-amd64 release binary (GitHub rel-4.0.4), unchanged.
