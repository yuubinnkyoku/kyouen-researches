# Part SR declaration: fifth-resumption 30 LOSS rows delegated C++ scrutiny gate (wave A, 2026-11-26)

Long-term lane session (single-owner). This Part closes the coverage
asymmetry the Part SQ completion log records for the THIRTY
fifth-resumption resolved-LOSS rows of the sixth-cost exclusive S5 probe
(k09,k10,k11,k12,k14,k15,k16,k17,k18,k21,k22,k23,k24,k25,k26,k27,k28,
k29,k30,k31,k32,k34,k35,k36,k37,k39,k40,k41,k42,k43; parked k20/k33/k38
excluded, no new verdict for them): they have Part SL third-implementation
verdict-level LOSS(2) corroboration (batch 32/32 all-pass) but NO delegated
pinned C++ second-implementation gate. This Part supplies that gate as a
publish-then-execute kit, Part SM/SN pattern (9th execution of the C++ gate
lineage after EN, EO, EQ, ET, EV, SK, SM, SN).

## Pre-registered scope and protocol (decided before the official run)

- Kit of record:
  research/experiments/n11-sixthcost-fifthres30-cppgate-20261126/
- Gate source: cpp/solvers/kyouen_dfpn_root.cpp at commit
  154f3b7a67b97e13acbaee8b04dc74ddca728d19, sha256 9193f5b6... (the
  delegated pin, machine-read from the published Part SN kit
  gate-rows.json); headers kyouen_residual_micro.hpp 5976935d... /
  n11_s5_quarantine.hpp 2e36d694... at the same commit. Built with zig
  0.13.0 (tarball zig-linux-x86_64-0.13.0.tar.xz sha256 d45312e6...,
  re-verified this session); the binary is NOT pinned (source pins are
  authoritative, host codegen differences expected per SK/SM/SN
  protocol).
- Rows: 3 calibration anchors (byte-clones of the SK kit inputs;
  quadruples == the published SN kit anchors block: anchor-at2m
  98,2000000,0,2000000 / anchor-aj001 84,30000000,2,5156075 /
  anchor-af039 89,30000000,2,19234232) plus the 30 target rows. Expected
  quadruple per target = the published fifth-resumption resolution
  condition (loss15/loss2m15m rows at budget 15000000; loss2m rows
  k28/k32 at budget 2000000), machine-derived by the maker from the
  published probe-lane raws (sha-verified against the published
  audit_k09k43.py ROWS pins) and recorded in input/gate-rows.json.
- Runner: published SN kit runner byte-transform (diff = exactly the 2
  comment lines naming Part SR); TWO fresh-cold passes per row, one
  process per pass; acceptance: p1 == p2 on (legal,budget,result,nodes)
  and both == expected. Any mismatch/crash: HARD-STOP, fail-closed, no
  interpretation (C5). Truncated artifacts re-run, never trusted.
- Official execution order (pre-registered): anchors at2m, aj001, af039
  first, then the 30 targets ascending (k09..k43), serial, after kit
  publication (publish-then-execute).
- Audit: scripts/audit_gate.py (published SN audit transform: docstring +
  machine-generated ROWS/RAW_PROV + part/schema strings only, logic
  byte-identical, asserted by the maker G3); exit 0 only on all-pass;
  4 runs byte-identical required. Tamper battery: SN kit battery
  transform (T1 audit ROWS pin k09 nodes 4018184->4018185; T2 raw
  k09.p1 nodes edit; T3 phantom GATE-PASS line), each must fail closed
  rc=1 with byte-verified restore; clean control rc=0.
- Maker: scripts/make_kit_fifthres30_cppgate_20261126.py, fail-closed
  G0/G1/G2/G3, 231 gates ALL PASS at kit build time (wave B); no
  per-row pin hand-typed (EP pin policy).

## Pre-registered kit byte pins (sha256)

- input/gate-rows.json
  662502671ff478d61505038126f6928bd57126ca767cc18d658139796dfeaad2
  (46,966 bytes; schema n11-sixthcost-fifthres30-cppgate-rows-v1;
  contains the machine-derived per-target budget/expected/input-sha/
  raw-provenance and the maker gate record)
- scripts/make_kit_fifthres30_cppgate_20261126.py
  1aef363333e220734b1bb10a30b4026596ff0ce4c8dea936178459a0449eb301
- scripts/gate_runner.sh
  59cbbefe70d373f6b846898e79083c6b7b18981f7eb3deec65ae81fffd75b00a
- scripts/audit_gate.py
  e8a139a7e4b0c87e1d354b38bcd3f8487dabfc42da3f159f2c01e558f303c625
- tamper_battery.sh
  e4be38228a7ebd35efd81d74b53c106cbe2a7c61079db73d2d1ee79a16f28f87
- input/*.input.csv (33 files): anchors byte-clones of the SK kit
  inputs (sha256 == SK/SN kit pins: at2m ecc0299b..., aj001
  2f6daea5..., af039 e51a3c9d...); the 30 target inputs byte-clones of
  the published third-impl kit inputs (sha256 == audit_k09k43.py INPINS
  pins, machine-verified by the maker G1; full list in
  input/gate-rows.json targets[].input_sha256).

## Freshness and verdict scope (pre-registered)

The maker G2 machine-verifies that the canonical head of record
02db5ab3 (Part SQ, 6,801 s5verdict rows WIN201/LOSS6600,
284,230 bytes, sha-verified) contains NONE of the 30 target [lo,hi]
pairs: all 30 stay fresh (verdict-unconsumed) at declaration and run
time. This Part consumes NO verdict: the 30 rows become
second-implementation gate-verified UNCONSUMED labels on top of their
ladder primary (15M/2M cold pairs) and Part SL third-impl corroboration.
k38 stays parked@15M with NO L50M follow-up claimed by this Part. Any
adoption decision stays with a separately declared adoption Part under
the parent batch's WIN/LOSS conflict policy. The standard 11x11 empty
board, every central-reply root, the two-stone root {60,27}, its
remaining third moves {100,108}, S2, class 1/2/4 and all closure
classes stay UNKNOWN throughout. Nodes are bookkeeping, never
verdicts.

## Concurrency, environment and honesty disclosure

- HEAD re-fetched immediately before this push (277f91b2, the kit-12
  cross-check record; territory disjoint from every path written
  here). Counter-probes at declaration time: code-search "fifthres30"
  0 hits, "part-sr" 0 hits (research/log), no competing fifth-resumption
  C++ gate artifact on main; the probe-lane and third-impl dirs are
  READ-only inputs for this Part.
- Host: upgraded Vibe execution sandbox (native toolchain available
  this session, unlike the third-impl batch hosts which had no C++
  toolchain). zig 0.13.0 tarball downloaded and sha-verified
  (d45312e6...) BEFORE this push; binary built from the pinned source
  with all three sha pins byte-verified.
- Honest pre-declaration disclosure: ONE anchor-at2m calibration run
  (98,2000000,0,2000000, 4 s wall) was executed at binary-build time
  as an environment sanity check BEFORE this declaration push. No
  target row was run before publication; the official
  publish-then-execute run starts after wave B. The calibration raw is
  NOT a target row, consumes nothing, and is re-run officially inside
  the gate execution (anchor rows are part of the pre-registered
  order).

## Wave plan

A: this declaration. B: kit files (gate-rows.json + 33 inputs + 4
scripts). C: results (72 raws + gate-status.log + audit JSONs +
tamper artifacts). D: README + MANIFEST-sha256. F: completion log.
Every wave push re-fetches latest main first (hourly parallel-run
warning) and verifies fetch-back bytes via raw-CDN sha256.
