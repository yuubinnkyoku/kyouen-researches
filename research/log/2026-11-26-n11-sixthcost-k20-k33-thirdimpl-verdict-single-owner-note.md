# n11 sixth-cost k20/k33 third-implementation verdict re-verification: single-owner fresh declaration (2026-11-26)

Declared: 2026-11-26T14:30Z (lane: the n11 long-term lane; single-owner,
publish-then-execute). This is the separately declared third-impl Part that
research/log/2026-11-26-part-sn-parked4rest2-k20k33-cppgate-completion.md
pre-registered as the natural next step before any adoption Part weighs the
two unconsumed parked4rest2 L50M WIN rows: k20/k33 carry the ladder 4-run
primary battery plus the Part SN delegated pinned C++ second-implementation
gate (GATE-PASS, node-exact), but NO third-implementation verdict-level
corroboration, because
research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/
(k09..k43 resolved batch, 32/32) parks them explicitly. This Part extends the
third-implementation program to exactly those two rows, per the
fresh-declaration program rule (WIN-row precedent).

HEAD re-fetched immediately before this push: `a0166a12` (2026-11-26T14:15:50Z,
the kit-10 newband publish; paths disjoint from everything written here).
Counter-probe at declaration time: code-search and commit-search probes
("part-so", "k20 k33 thirdimpl", "k20k33 third") all return zero competing
artifacts for a k20/k33 third-impl extension.

Host honesty: this runs on a NEW host (Vibe upgraded sandbox with Node.js
v22.20.0 and Python3, no C++ toolchain). Per the k05 fresh-host precedent the
C1 calibration is re-executed fresh on this host this session and no
published calibration raw is reused.

## Scope (exactly two rows; nothing else is measured or claimed)

- k20 `10376293541461626880:33619968` (stones 5, legal 95), row spec
  `target,0,5,10376293541461626880,33619968,95,0,0,0,0,0` (exact published
  ladder input bytes, `input/batch-k20.input.csv` sha256
  `0984400f8aa99735e11e2638f5bc9a9273ddd296e845f7b7118f3ada81adddad`).
- k33 `12682136550675320832:65536` (stones 5, legal 91), row spec
  `target,0,5,12682136550675320832,65536,91,0,0,0,0,0` (exact published
  ladder input bytes, `input/batch-k33.input.csv` sha256
  `ca081b0f2f85e62b39cbbd1178a7be839c87e3446b2357657bbfe8681f82e2f4`).

Replica raws (the SSOT comparisons, consumed at HEAD `a0166a12` from the
parked4rest2 ladder kit
`research/experiments/n11-sixthcost-class10376293541461626880-parked4rest2-s5-l50m-ladder-20261126/output/raw/`,
all TEN fetched and sha256-verified against the kit MANIFEST before this
declaration):

k20 (result 1 WIN, nodes 16,196,331 on all four resolution stages; base15m
parked baseline result 0, nodes 15,000,000):
`base15m-10376293541461626880-33619968.out.csv` 64a069a2a66f677ffd01c4eb03eb6b43aa07ac041319c3fb5ecce5b853c21774`,
`l50m-run1-` f852cd55f7f80bdf57ccbe753e78a0b09deb5f7c552af51caed5f4d583aa2c73,
`l50m-run2-` 86db668a0288aeb3695f0fb0c3285f128d906ca8dbbf240d6d17b566303601e3,
`l50m-margin-` e5525aab03eb0e272dd44dbe04a0c0c98bddcd2afc3c14c0e474e7055fbafa55,
`l50m-run3-verify-` bf2b12fffb194540205b4eb2c80e98b907059701a36969035824f3b0a339efff.

k33 (result 1 WIN, nodes 15,842,649 on all four resolution stages; base15m
parked baseline result 0, nodes 15,000,000):
`base15m-12682136550675320832-65536.out.csv` 4fb1067184f15036cea90c496c6ebb160ffacd18395adff327c104da71356af8,
`l50m-run1-` 664ebc3a88ed14cb5a8f418df213368ab8501533c13a60f50261d93d841fc54f,
`l50m-run2-` c08cdd7854c9a1c177428e86d08039edfeafe79e340001dc7f386ca0c706a3d2,
`l50m-margin-` 39154465a07ee7c97bebab517b284c77866d42374ba6ca5a446a5b502676526e,
`l50m-run3-verify-` 598538dce0cadc2be4752a6276fe3a8de0f5d3d873d4e7d214063924ebd7b530.

## Implementation and pins (unchanged from the parent program)

third_impl.js sha256
`08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998`,
verify_tbl.js sha256
`c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251`,
replica jsreplay.js sha256
`845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
(byte-clone of the ladder kit publication, consumed by verify_tbl.js only).
All three re-fetched from HEAD `a0166a12` and sha-verified before this push.

## Pre-registered protocol

- C1 fresh calibration on this host, before any k20/k33 row runs:
  (i) verify_tbl.js replica-vs-mine completion-table equality battery
  (identical quads count required, zero mismatches tolerated, rc=0);
  (ii) anchor w2 `10376293541461626880:131328` full third_impl run must
  reproduce the published witness WIN(1) at expansions 7,583,990
  (two executions, identical quadruple).
- C2 per-row verdict-level expectations: k20 WIN(1), k33 WIN(1). Three full
  cold runs per row (a, b, and v = --verify-legal=1) with identical
  (result, expansions, ttHits, ttOverwrites) required; the verify-legal run
  additionally requires identical (result, expansions). Invocation as the
  batch precedent: --cap=400000000 --wallcap=270 --memo-power=22.
  Expansion counts are compared only across this implementation's own cold
  runs and are never compared to replica node counts (anti-copy gate:
  expansions != 16,196,331 for k20, != 15,842,649 for k33).
- C4 fail-closed input gates per row (declared legal+1 and declared
  stones=6, --cap=4000000 --wallcap=60): each must GATE_FAIL with
  process exit status 1.
- C5 any disagreement is a hard stop: publish raws, no interpretation,
  hand to the scrutiny owner.
- Auditor: a separate data-driven audit script (audit_k20k33.py), fail-closed
  (rc=0 only on all gates PASS), deterministic byte-identical across runs,
  with negative tamper controls on full kit copies (a verdict flip on each
  row failing determinism + verdict-level gates, a replica-raw edit failing
  the sha + batch-count gates), byte-verified restores and a final clean
  control. Existing auditors (audit.py, audit_k04.py, audit_k05.py,
  audit_k06k07k08.py, audit_k09k43.py) stay byte-frozen.
- publication: this declaration log first (wave A); then the run raws, the
  calibration raws, the negative-gate raws, the tamper log, the new auditor,
  per-row replica-raw copies (so the auditor is self-contained), a README
  addendum and a MANIFEST append inside the parent experiment dir
  `research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/`;
  no K item, no knowledge README edit, no probe-dir write, no cache file,
  no class/root/board claim.
- C6 no verdict consumed; the two rows remain unconsumed solver-trusted
  evidence; adoption stays with the scrutiny owner. The standard 11x11 empty
  board, the two-stone root {60,27}, and its remaining third moves
  {100,108} remain UNKNOWN. Node/expansion counts are never verdicts.

## Claim hygiene

This Part makes NO verdict, class, coverage, secured-coverage or root claim.
It is scheduling and verification only. Verdict-level agreement assertions,
if any, will only be made by the post-run addendum against the published
replica raws listed above, and any disagreement triggers the C5 hard stop.
Parallel lanes: before each push, latest main is re-fetched; a competing
k20/k33 third-impl publication detected at any stage causes a stand-down
(the Part SP cross-check precedent).
