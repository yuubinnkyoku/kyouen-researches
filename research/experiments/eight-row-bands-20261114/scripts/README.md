# scripts — eight-row-bands-20261114

Runners for w=8 (and w=7 q=8) row-deficient band instances. All encoding logic is
reused verbatim from `seven-row-q9-q10-bands-20261114` / `seven-row-inband-families-20261114`:

- `genfast.js` — memory-bounded CNF generator (half-integer-center census for q >= w+1),
  VERBATIM from `seven-row-q9-q10-bands-20261114/scripts/genfast.js`. Byte-identity against
  `sat2.js` re-validated for the new coverage of this experiment: (7,25,8) def,
  (7,40,8) def+lex=H,V,HV, (8,30,9) def, (8,35,10) def+lex=H,V,HV (4/4 `cmp` MATCH;
  the source experiment's 12 samples covered only w<=7 with q in {6,7,8,9,10} at w<=6).
- `decode_verify.js`, `lean2.sh` — VERBATIM from the source experiment except the inner
  kissat `timeout 275` -> `timeout 230` (this session's container hard-stops at ~290 s per
  command; the CNF and the recorded verdicts/conflicts are unaffected for any width that
  resolves within 230 s; widths hitting the cap are recorded INDET honestly).
- `sat.js` / `sat2.js` / `fastsat.js` / `verify_witness.py` are NOT duplicated here —
  they are used verbatim from `seven-row-inband-families-20261114/scripts/`
  (`lean2.sh` resolves them via SEVEN_SCRIPTS, default `/home/user/krwork/seven/scripts`).

Usage (same CLI as the source experiment):

```sh
./lean2.sh 8 23 9 <outdir> [LEX]   # genfast CNF (q>=w+1) + kissat + (SAT: dual verify)
./lean2.sh 8 30 10 <outdir> [LEX]
./lean2.sh 7 30 8 <outdir> [LEX]
```

CNFs are deterministically regenerable and not stored; per-instance kissat logs
(`*.kissat.txt`), SAT witnesses (`*.witness.json`, dual-verified), and the aggregated
`records.jsonl` are stored per family directory.
