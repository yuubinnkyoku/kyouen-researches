# n11 Part SY kit: seventh-cost full-batch third-implementation corroboration (wave B)

Kit of the wave A declaration (research/log/2026-11-27-n11-seventhcost-
thirdimpl-corroboration-declaration.md, HEAD 47ae14ea). Publish-then-
execute: no target pass runs before this publication.

## Files

- input/gate-rows.json - schema n11-seventhcost-thirdimpl-corroboration-
  rows-v1, 42 targets (k01..k42: 41 expected LOSS(2), k05 expected
  WIN(1)), every expected result machine-derived from the published Part
  SW / Part SX kit gate-rows expected quadruples and replica_verdict
  fields (maker G5), per-row input sha256 pins re-verified (maker G3).
  Input CSVs are byte-clones of the published SW/SX kit inputs
  (k05 input sha256 a73a6c70... == published seventh-cost kit MANIFEST
  pin).
- scripts/third_impl.js - sha256 08ea958f... (the program's standing
  third implementation, byte-equal re-publication provenance of the
  ea73c3e3 publication; byte-verified against the pinned sixth-cost
  third-impl kit copy on this host).
- scripts/verify_tbl.js - sha256 c8c52528... pristine byte-clone. NOTE:
  its replica dependency path is the pinned knowledge-mount
  jsreplay.js (sha256 84585617...); a byte-equal copy is carried at
  scripts/jsreplay_lane.js for self-containedness (the published
  verify_tbl.js bytes are unmodified).
- scripts/run_target.sh - pinned invocation per pass:
  node third_impl.js --lo=<lo> --hi=<hi> --stones=5 --legal=<legal>
  --row=<kNN>.pN --cap=400000000 --wallcap=260 --memo-power=22
- scripts/make_kit_sy_20261127.py - fresh maker (8 fail-closed gates,
  2 runs byte-identical, disclosed in docstring), run record below.
- scripts/audit_sy.py - fresh fail-closed audit (G0-G6), runs in wave C
  on the official outputs.

## Calibration (already executed post-declaration, this host, Node v22.20.0)

- C1a verify_tbl: rc=0, replica quads 95,670 / mine 95,670, triples
  checked 195,044 mismatches 0 (output/c1a-verify-tbl.txt, pristine
  byte-clone run).
- C1b calib-k06 10376293541462675456:65536 legal 89: LOSS(2) expansions
  9,474,431 - EXACT match to the published sixth-cost k06-cold-a raw.
- C1b calib-k38 10376293541461626880:66048 legal 100: LOSS(2)
  expansions 25,898,941 - EXACT match to the Part SU publication.

## Meaning and non-meaning

Verdict-level corroboration bookkeeping only. NO verdict is consumed,
no cache increment, no class-status change. Third-impl expansions are
compared ONLY across the third implementation's own cold pairs, never
against replica node counts. The standard 11x11 empty board, all 19
central-reply roots, the two-stone root {60,27}, its remaining third
moves {100,108}, S2 and all closure classes are UNKNOWN. Expansions and
nodes are bookkeeping, never verdicts.
