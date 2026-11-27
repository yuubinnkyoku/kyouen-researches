# Part SW: seventh-cost 41 LOSS rows C++ scrutiny gate (2026-11-27)

Tenth execution of the C++ second-implementation scrutiny gate lineage
(after EN class-30484, EO class-34908, EQ class-30345 b38-win-18, ET
class-30345 ES-re-probe-6, EV closure-batch WIN-4, SK sixth-cost exclusive
k01..k08, SM parked4 k13/k19, SN parked4rest2 k20/k33, SR fifthres30): the
delegated pinned C++ gate of the FORTY-ONE resolved-LOSS rows of the
seventh-cost exclusive S5 probe batch (k01..k42 minus k05). Scope,
protocol, pins and stop rules are pre-registered in the wave A
declaration (research/log/2026-11-27-n11-seventhcost-41loss-cppgate-declaration.md,
commit dfb6b357).

- Targets: 41 rows (39 stage-15m at budget 15000000, k16/k17 stage-2m at
  budget 2000000), expected quadruples machine-derived from the published
  probe raws (SSOT) and cross-checked against the published selection JSON
  (c395fe03) and batch-summary ledger (6881eaaf); per-pass target node bill
  211,789,419 + anchors 26,390,307 (bookkeeping).
- Anchors: anchor-at2m / anchor-aj001 / anchor-af039 (byte-clones of the
  published SR kit inputs; quadruples == the SR kit anchors block).
- Freshness: all 41 target [lo,hi] pairs ABSENT from the canonical head of
  record 42dbb58f (6,832 s5verdict rows WIN 201 / LOSS 6,631,
  sha-verified) - verdict-unconsumed at declaration, run and publication
  time.
- k05 (parked-then-L50M WIN row) is NOT a row of this kit; its C++ gate
  and third-impl corroboration stay separate future Parts.
- Third-implementation corroboration: ABSENT for every target row
  (seventh-cost batch is single-implementation Node replica + this gate;
  SN disclosed-absence pattern; a third-impl Part is required before any
  adoption).

This Part consumes NO verdict. The 41 rows stay gate-verified UNCONSUMED
labels; adoption stays with a separately declared adoption Part under the
parent batch's WIN/LOSS conflict policy. The standard 11x11 empty board,
every central-reply root, the two-stone root {60,27}, its remaining third
moves {100,108}, S2, class 1/2/4 and all closure classes stay UNKNOWN.
Nodes are bookkeeping, never verdicts. S5 LOSS raws are not class closure
claims and not routes to the root certificate.

Kit layout: scripts/ (maker, runner, audit), input/ (44 input.csv +
gate-rows.json), output/ (gate-status.log, raw p1/p2 per row,
audit_gate.json x4). MANIFEST-sha256.txt published with the run record
(wave D).

## Run record (2026-11-27, publish-then-execute per declaration dfb6b357)

Waves A/B published first (declaration dfb6b357; kit 2f7dec1e with maker
all-gates PASS, 2 runs byte-identical; fetch-back 49/49 git-blob-sha
byte-identical). Official execution 02:54:05Z-03:10:46Z sequential
(anchors at2m/aj001/af039 calibrated first, then the 41 targets ascending
k01..k42 minus k05 - pre-registered order), all 44 rows GATE-PASS with
(legal,budget,result,nodes) exactly the published values
(output/gate-status.log, 44 GATE-PASS, zero MISMATCH / GATE-FAIL /
GATE-CRASH / TRUNCATED). Results wave C 45a1bbc6 (93 files, fetch-back
93/93 git-blob-sha byte-identical).

Per-pass node bill: targets 211,789,419 + anchors 26,390,307 per pass;
two-pass bill (211,789,419 + 26,390,307) x 2 = 476,359,452 (bookkeeping,
summed from the per-row raws, the SSOT). Gate run walls: anchors
2/20/79 s; targets 4-42 s per row pass (output/gate-status.log timestamps;
environment bookkeeping, never compared).

Machine:
- Gate source pins: cpp/solvers/kyouen_dfpn_root.cpp sha256 9193f5b6...
  at commit 154f3b7a..., headers 5976935d... / 2e36d694... (byte-verified
  this session). Built with zig 0.13.0 `zig c++ -std=c++20 -O2` (tarball
  sha256 d45312e6... verified this session); binary sha256 a7cb4cc0...,
  NOT pinned: source pins are authoritative (SK/SM/SN/SR protocol).
- Audit: scripts/audit_gate.py (published SR audit transform; logic
  byte-identical, asserted by the maker G3) sha256 36954bc4...; 4 runs
  rc=0 byte-identical sha256 7d60409c... (audit_gate.json == run1 ==
  run2 == run3 published; 221/221 gates).
- Maker: sha256 f7cb080a... - all gates PASS at kit build time (wave B),
  2 runs byte-identical; every per-row pin machine-derived (EP pin
  policy): the 41 target expectations from the published probe-lane raws
  sha-verified against the published MANIFEST-raw-sha256.txt, the
  published selection JSON c395fe03 and the published batch-summary
  ledger 6881eaaf; the anchors from the published SR kit gate-rows.json.
- Tamper battery: tamper_battery.sh (k01 quadruple, scratch copy only):
  T1 audit ROWS pin flip -> G3:k01 FAIL rc=1; T2 raw k01.p1 nodes edit ->
  G2+G3:k01 FAIL rc=1; T3 phantom GATE-PASS line -> G4 FAIL 45/44 rc=1;
  every restore byte-verified; clean control rc=0 (tamper.log). The
  battery ran once inline during the official session and once more via
  this published script (identical outcomes); the scratch copy is deleted,
  never published.
- Freshness (maker G2): all 41 target [lo,hi] pairs ABSENT from the
  canonical head of record 42dbb58f (6,832 s5verdict rows WIN 201 /
  LOSS 6,631, sha-verified) - verdict-unconsumed at declaration, run and
  publication time.

Honest environment disclosure (also in the declaration): this executing
session ran on an upgraded sandbox WITH a native C++ toolchain. One
anchor-at2m calibration run (PASS, 98,2000000,0,2000000) was executed at
binary-build time BEFORE the declaration push as an environment sanity
check (SR precedent); no target row ran before publication. The 124
published probe raws were read from a local cache sha-verified against the
published MANIFEST-raw-sha256.txt fetched from the pinned HEAD
f38d2b43 (fetch-route optimization only; the manifest pins are the raw
SSOT). Counter-probe clean at declaration time (HEAD f38d2b43, no
concurrent lane in this territory).
