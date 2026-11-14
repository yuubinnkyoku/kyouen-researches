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

- `genff.js` — fastest census CNF generator: same-row-pair-pair enumeration
  (a q>=w+2-point circle has >=2 same-row pairs; two pairs (y1,e1),(y2,e2) determine
  it exactly; pure-integer pre-filter with >= min(3,w-2,ceil((q-4)/2)) further rows
  carrying an in-grid point — provably no false negatives — then the genfast-identical
  exact scan; ORDERED offset pairs required, equal offsets included: an unordered loop
  silently misses circles, pinned by the (6,20,8) control). Lines for q>w are the w
  horizontal rows. Byte-identical CNF to sat2.js (8 samples incl. --cap=+tot/rowY/lex
  and w=6) and genfast.js (4 samples incl. m=100) — `scripts/genff-verification.md`.
  ~0.74s at (7,150,10) vs genfast 69s; asserts q>=w+2, w<=7.
- `leanff.sh` — lean2.sh contract with genff.js + gen_sec field; CNFs deleted after the
  kissat run (deterministically regenerable).
- `batchff.sh` — wall-budget batch driver over m (resumable per-instance).

sat2.js / sat.js / fastsat.js / verify_witness.py are used **verbatim** from
`research/experiments/seven-row-inband-families-20261114/scripts/` (K0810 census core);
they are not duplicated in this experiment. Paths inside the shell scripts point to
`/home/user/krwork/seven/scripts/` (session workspace); replace with the source
experiment's scripts directory when re-running.

kissat 4.0.4 official linux-amd64 release binary (GitHub rel-4.0.4) is used unchanged.
