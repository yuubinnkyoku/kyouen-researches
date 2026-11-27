# Part SS declaration: k38 L50M follow-up LOSS row C++ scrutiny gate (2026-11-26)

Single-owner publish-then-execute declaration (10th execution of the C++
second-implementation scrutiny gate lineage: EN, EO, EQ, ET, EV, SK, SM, SN,
SR). This Part delegates the pinned C++ second-implementation gate to the
single row k38 `10376293541461626880:66048` of the sixth-cost exclusive S5
batch (fifth resumption, machine order position 38), which the L50M
follow-up completion (commit `2bc21cf3`, first implementation jsreplay cold
pair, 21,839,049 nodes) just turned into a loss-resolved row.

## Claimed territory

Exactly one target row: k38, expected quadruple
`100,50000000,2,21839049` (legal 100, budget 50,000,000, result 2, nodes
21,839,049), the SSOT being the published raws
`at50m-run1-k38.out.csv` (sha256 f7e51958...) and
`at50m-run2-k38.out.csv` (sha256 53d0f69d...) at commit `2bc21cf3`.
No other key, row, class or cache is claimed; no adoption is performed.

## Why this Part

The Part SR gate covered the 30 fifth-resumption LOSS rows but explicitly
excluded k38 ("parked k20/k33/k38 excluded"). The L50M follow-up has now
resolved k38 as LOSS(2) with a first-implementation cold pair only. This
gate adds the pinned C++ second-implementation scrutiny (2 fresh-cold
passes, node-exact) so k38 reaches the same second-implementation coverage
level as the 30 SR rows. Third-implementation corroboration for k38 remains
an open vacancy (honest disclosure, not claimed here).

## Pre-registered execution

- Gate source pins (byte-verified this session against commit
  `154f3b7a67b97e13acbaee8b04dc74ddca728d19`): `cpp/solvers/kyouen_dfpn_root.cpp`
  sha256 9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e,
  headers `kyouen_residual_micro.hpp` 5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5
  and `n11_s5_quarantine.hpp` 2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5.
  Built with zig 0.13.0 `zig c++ -std=c++20 -O2` (tarball
  zig-linux-x86_64-0.13.0.tar.xz sha256
  d45312e61ebcc48032b77bc4cf7fd6915c11fa16e4aad116b66c9468211230ea,
  byte-verified this session). Binary not pinned: source pins are
  authoritative (SK/SM/SN/SR protocol).
- Rows and pre-registered run order: anchors first
  `anchor-at2m` (98,2000000,0,2000000), `anchor-aj001`
  (84,30000000,2,5156075), `anchor-af039` (89,30000000,2,19234232), then the
  single target `k38` (100,50000000,2,21839049). Anchor inputs are
  byte-clones of the published SR kit anchor inputs (pins in
  input/gate-rows.json); the k38 input is the byte-clone of the published
  sixth-cost probe kit input (sha256 b6ef9f43...).
- Acceptance per row: two fresh-cold passes, p1 == p2 on
  (legal,budget,result,nodes) and both == the pinned expected quadruple
  (runner `scripts/gate_runner.sh`, machine-identical logic to the
  EN/EO/EQ/ET/SK/SM/SN/SR runner rev2, comment block only names Part SS).
  Any mismatch/crash/truncation: HARD-STOP, recorded, re-run fresh; a
  truncated artifact is never published.
- Audit: `scripts/audit_gate.py` - a FRESH single-row implementation of the
  gate checks, not a byte-transform of the SR audit script (disclosed): G0
  schema pins, G1 input byte pins, G2 raw completeness, G3 per-row
  p1==p2==expected, G4 phantom-raw and status-log consistency, G5 target
  freshness (the k38 [lo,hi] pair absent from the canonical head of record
  02db5ab3, sha-verified). Fail-closed rc=1. The audit runs 4 times; all
  four outputs byte-identical. A 3-mode tamper battery (expectation flip ->
  G3, raw edit -> G2/G3, phantom raw -> G4) must fail-closed, with byte
  restore verification and a clean control pass.
- Environment sanity disclosure: one anchor-at2m calibration run (PASS,
  98,2000000,0,2000000, wall 3 s) was executed at binary-build time BEFORE
  this declaration push (SR precedent); NO target row ran before
  publication.
- Publication paths (pre-registered):
  `research/experiments/n11-sixthcost-k38-l50m-cppgate-20261126/` with
  input/ (4 input csv + gate-rows.json + canonical-head.cache byte-clone),
  scripts/ (runner + audit), output/raw/<key>.p1.out/.p2.out x8,
  output/gate-status.log, output/audit_gate.json (+3 audit rerun copies),
  tamper.log, README.md, MANIFEST-sha256.txt, and the completion log
  `research/log/2026-11-26-part-ss-k38-l50m-cppgate-completion.md`.

## Verdict scope

NO verdict is consumed. k38 stays a gate-verified UNCONSUMED batch row.
Adoption of the k38 LOSS row (and of the 30 SR LOSS rows) remains a
separately declared future Part under the parent batch's WIN/LOSS conflict
policy. The standard 11x11 empty board, the 19 central-reply roots, the
two-stone root {60,27}, its remaining third moves {100,108}, S2, class
1/2/4 and all closure classes stay UNKNOWN throughout. Nodes are
bookkeeping, never verdicts.

## Counter-probe

At declaration push time the latest main HEAD is `2bc21cf3` (the k38 L50M
completion, this session). No commit touching k38 C++ gate / "cppgate"
territory for k38 exists (the SR/SM/SN gate kits cover other rows and
explicitly exclude k38); no concurrent lane has claimed this Part.
