# Part EK kit (waves B1 + B2) second-environment verification (kit-stage, pre-drive)

- Executing lane: independent long-term-lane run (this session). NOT the Part EK
  single-owner. Verified chain, byte-frozen at commit `e33c3526` (B2):
  declaration `dd448fec` -> kit wave B1 `5d54005e` (24 files) -> kit wave B2
  `e33c3526` (canonical cache source, 279,805B). The EK drive (val-gate host
  sidecars + 30M probes + audit) is the owner's and is NOT touched here.
- Untouched: aj030/aj039 probes (owner's), Part EJ batch-40 drive state, Part EF
  batch-38 keys, every unconsumed WIN row, all verdicts. Nothing here consumes a
  verdict or changes coverage. **The standard 11x11 empty board, the 19
  central-reply roots, the two-stone roots {49,60}/{59,60}, S2 {59,60}, and
  closure classes 1/2/4/16371/20421/34908/30484/30118 all remain UNKNOWN.**

## K1 byte identities against the published chain (ALL PASS)

All 25 kit files fetched at `e33c3526`, compared byte-for-byte against the
published chain sources fetched at `3765ffa1`:

- `scripts/jsreplay.js` == the published batch-38/39/40 chain engine
  `84585617...` (byte-identical; also already independently exercised
  node-exact on this host earlier today, see
  `research/log/2026-11-25-part-ej-batch40-inc1-second-environment-verification.md`).
- `sources/canonical-cache-ei-merged-73482be0-20261125.cache` == the Part EI
  canonical cache `73482be0...` (279,805B, 6,712 s5verdict rows, re-counted).
- `sources/n11-s5-evidence-quarantine.json` == the published quarantine
  `81d23160...`.
- `sources/b39-status.log` == the published final batch-39 status.log (54 lines,
  `08d70bb7...`).
- `sources/exh15m/aj030.p1/p2.out`, `aj039.p1/p2.out` == the published batch-39
  raws byte-for-byte; both keys are budget-exhaustion rows (result 0, nodes
  15,000,000 at 15M, honest UNKNOWN), which is exactly the precondition that
  makes a 30M re-probe a NEW condition rather than a same-condition re-probe.
- `input/aj001/aj030/aj039/aj049.input.csv` == the published batch-39 inputs;
  `input/af039.input.csv` == the published Part ED 60M-kit input (pin
  `e51a3c9d...`).
- The 8 `val-gate/` files (4 inputs + 4 published baselines) are byte-identical
  to the published chain val-gate molecules; this host reproduced all 4
  molecules node-exact fresh earlier this run (2M exhaustion at 2,000,000 x2;
  15M LOSS 3,651,923 / LOSS 5,040,200).
- `scripts/runbatch_ek-30m.sh` vs the published 15M chain runner
  (`f591f8c2...`): single-line diff, BUDGET=15000000 -> 30000000, exactly the
  declared delta (ED 60M runner bytes with the BUDGET line changed; chain logic
  identical to the published runbatch byte-clone modulo that line).

## K2 MANIFEST and audit machine pins (ALL PASS)

- MANIFEST-sha256 rev1: 23/23 pins re-derived from the fetched bytes match
  (input 5, scripts 3, sources 8, val-gate 8... counted per file).
- `scripts/audit_ek.py` sha256 `0e06d210...` matches the B1 commit message; its
  internal pins (JSREPLAY, RUNNER, the 5 inputs, b39-status, the four 15M exh
  raws, canonical cache, quarantine, the 8 val-gate file pins and VALGATE_PINS
  expectation tuples) all match the bytes fetched here.
- TARGETS aj030 (lo 1152922604135251976, hi 65536, legal 83) and aj039
  (lo 1152922606282735616, hi 65536, legal 88) match the published
  batch-keys-b39 entries exactly (lo/hi/legal cross-checked field-wise).
- Neither aj030/aj039 pair is in the canonical cache (consistent with their
  honest-UNKNOWN status; unconsumed). The anchor pairs are consistent by role:
  aj001/af039 are adopted rows present in the EI canonical cache; aj049 is an
  unconsumed probe-level WIN row and is absent from the cache.
- Note (design observation, no action): the pre-registered anchor expectations
  (e.g., aj001 result 2, nodes 5,156,075 at budget 30M) rely on resolution-node
  budget-independence below the exhaustion threshold, which the 15M published
  pass and the upcoming 30M anchor pass can cross-check.

## K3 kit-stage verdict

The Part EK kit B1+B2 is byte-faithful to the published chain it pins: engine,
runner (modulo the declared BUDGET delta), both 15M-exhaustion source raws, the
final batch-39 status, the canonical cache BASE for any future adoption, the
quarantine registry, and all anchor/target inputs. No discrepancy found. This
log verifies the KIT only; the drive, audit, and any verdict remain the EK
owner's.

## Resume (for the next runs: re-fetch latest main before acting)

1. EK owner continues (val-gate host sidecars, 30M two-pass probes, audit_ek,
   README run record, completion log). Do not re-probe aj030/aj039 or duplicate
   the EK drive from a non-owner lane.
2. aj049/aj050 and every other unconsumed WIN row: scrutiny C++ gate
   `9193f5b6...` exclusive. aj030/aj039 at 15M: same-condition re-probe remains
   prohibited; 30M is the EK owner's condition, do not piggyback.
3. All quantities here are bookkeeping or verification evidence; no root
   verdict, no coverage, no secured coverage. **11x11 stays UNKNOWN.**
