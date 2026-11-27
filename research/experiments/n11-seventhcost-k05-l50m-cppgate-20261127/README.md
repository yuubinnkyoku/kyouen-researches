# Part SX: seventh-cost k05 L50M WIN row C++ scrutiny gate (2026-11-27)

Eleventh execution of the C++ second-implementation scrutiny gate lineage
(after EN, EO, EQ, ET, EV, SK, SM, SN, SR, SW): the delegated pinned C++
gate on the SINGLE seventh-cost parked-then-L50M WIN row k05
(1152921504607932416:536870912). Scope, protocol, pins and stop rules
are pre-registered in the wave A declaration
(research/log/2026-11-27-n11-seventhcost-k05-l50m-cppgate-declaration.md).

- Target: k05 at budget 50000000, expected quadruple
  90,50000000,1,15763505 (machine-derived from the published at50m cold
  pair, both raws sha256 ff750cc6...); stage policy pinned (published 2M
  and 15M UNKNOWN stage raws precede the escalation).
- Anchors: anchor-at2m / anchor-aj001 / anchor-af039 (byte-clones of the
  published SW kit inputs; quadruples == the SW kit anchors block).
- Freshness: the k05 [lo,hi] pair ABSENT from the canonical head of
  record 42dbb58f (6,832 s5verdict rows WIN 201 / LOSS 6,631,
  sha-verified) - verdict-unconsumed at declaration, run and publication
  time.
- Audit: FRESH single-row fail-closed implementation (Part SS precedent,
  disclosed) - not a byte transform of the batch audit.
- Third-implementation corroboration: VACANT (k20/k33 WIN precedent
  requires it before any adoption; a separate future Part).

This Part consumes NO verdict. The k05 WIN row stays a gate-verified
UNCONSUMED label; a WIN(1) gate result is only a verdict-level agreement
of the second implementation with the published first-implementation cold
pair. Adoption stays with a separately declared adoption Part under the
parent batch's WIN/LOSS conflict policy. The standard 11x11 empty board,
every central-reply root, the two-stone root {60,27}, its remaining third
moves {100,108}, S2, class 1/2/4 and all closure classes stay UNKNOWN.
Nodes are bookkeeping, never verdicts. S5 raws are not class closure
claims and not routes to the root certificate.

Kit layout: scripts/ (maker, runner, audit), input/ (k05 + 3 anchors +
gate-rows.json), output/ (gate-status.log, raw p1/p2 per row,
audit_gate.json x4). MANIFEST-sha256.txt published with the run record.

## Run record (2026-11-27, publish-then-execute per declaration, wave A)

Waves A/B published first (declaration commit = parent of kit commit
2accd8a5; kit 2accd8a5 with maker 25/25 gates PASS, 2 runs
byte-identical). Official execution 03:19:13Z-03:22:10Z sequential
(anchors at2m/aj001/af039 calibrated first, then the single k05 target at
budget 50000000 - pre-registered order), all 4 rows GATE-PASS with
(legal,budget,result,nodes) exactly the published values
(output/gate-status.log): **k05 GATE-PASS 90,50000000,1,15763505 - the
pinned C++ second implementation reproduces the published WIN(1) verdict
of the at50m cold pair (ff750cc6 x2) node-exactly** (first WIN-side row
of the gate lineage since EV/SN). Results wave C 670cb4d7.

Two-pass node bill: k05 15,763,505 x 2 + anchors 26,390,307 x 2 =
85,307,624 (bookkeeping). Gate run walls: anchors 2/21/75 s; k05
31/31 s per pass (output/gate-status.log timestamps; environment
bookkeeping, never compared).

Machine:
- Gate source pins: cpp/solvers/kyouen_dfpn_root.cpp sha256 9193f5b6...
  at commit 154f3b7a..., headers 5976935d... / 2e36d694... (byte-verified
  in the Part SW session of the same host session). Built with zig 0.13.0
  `zig c++ -std=c++20 -O2` (tarball sha256 d45312e6... verified); binary
  sha256 a7cb4cc0..., NOT pinned: source pins are authoritative
  (SK/SM/SN/SR/SW protocol).
- Audit: scripts/audit_gate.py FRESH single-row implementation (Part SS
  precedent, disclosed in the declaration and maker docstring; not a byte
  transform of the batch audit) sha256 829811ed...; 4 runs rc=0
  byte-identical sha256 31c84d20... (audit_gate.json == run1 == run2 ==
  run3 published; 26/26 gates).
- Maker: sha256 2d4742bc... - 25/25 gates PASS at kit build time, 2 runs
  byte-identical; every pin machine-derived (EP pin policy): the k05
  expected quadruple and raw-pair sha from the published at50m raws
  (ff750cc6 x2, sha-verified), the input pin from the published
  seventh-cost kit MANIFEST, the stage-policy raws (published 2M UNKNOWN)
  pinned, the anchors from the published SW kit gate-rows.json.
- Tamper battery: tamper_battery.sh (k05 quadruple, scratch copy only):
  T1 audit expected pin flip -> G0:target-expected + G3:k05 FAIL rc=1;
  T2 raw k05.p1 nodes edit -> G2+G3:k05 FAIL rc=1; T3 phantom GATE-PASS
  line -> G4 FAIL 5/4 rc=1; every restore byte-verified; clean control
  rc=0 (tamper.log). The scratch copy is deleted, never published.
- Freshness (maker G2): the k05 [lo,hi] pair ABSENT from the canonical
  head of record 42dbb58f (6,832 s5verdict rows WIN 201 / LOSS 6,631,
  sha-verified) - verdict-unconsumed at declaration, run and publication
  time.

Honest environment disclosure (also in the declaration): this executing
session ran on an upgraded sandbox WITH a native C++ toolchain; the
anchor-at2m calibration PASS of Part SW (same host session, same binary)
is the environment sanity check; no k05 pass ran before publication.
