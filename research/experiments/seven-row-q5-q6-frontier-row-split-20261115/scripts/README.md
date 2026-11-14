# scripts

- `rowsplit.sh` — one (w,m,q,rowY) rowfixed instance runner (NEW in this
  experiment): sat2.js `--rowY=Y` CNF, kissat 4.0.4 verdict (CAP arg,
  default 200s), on SAT decode + dual verify (decode_verify.js +
  verify_witness.py), JSONL record. Record schema identical to
  seven-row-q7-witness-search-20261114/output/row-split/records.jsonl.
- `sat2.js`, `sat.js`, `verify_witness.py` are used **verbatim** from
  `research/experiments/seven-row-q7-witness-search-20261114/scripts/`
  (K0810 census core; `--rowY=Y` rowfixed mode is a sat2.js built-in,
  previously used by the (7,7) m=25/26 and (7,8) m=24 row-splits), and
  `decode_verify.js` from
  `research/experiments/seven-row-q9-q10-bands-20261114/scripts/`.
  Not copied here; see those experiments for sources and calibration
  history.
- kissat 4.0.4 official linux-amd64 release binary (GitHub rel-4.0.4),
  unchanged. sha256
  21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1
  (re-fetched after an environment reset; identical hash).
- Post-reset calibration recorded in ../report.md: (7,5) m=31 def-mode
  SAT 31,000 conflicts bit-exact with the published frontier-extension
  record.
