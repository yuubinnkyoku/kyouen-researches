# Part SM: sixth-cost parked4 L50M WIN rows C++ scrutiny gate (k13/k19) (2026-11-26)

Seventh execution of the C++ second-implementation scrutiny gate (after EN
class-30484, EO class-34908, EQ class-30345 b38-win-18, ET class-30345
ES-re-probe-6, EV closure-batch WIN-4, SK sixth-cost exclusive k01..k08):
the delegated pinned C++ gate of the sixth-cost parked-4-keys S5 L50M
ladder's two WIN rows - the halt-audit's "win_raws_needing_scrutiny" /
"delegated_cpp_gate_targets" that the ladder lane (no C++ toolchain in its
sandbox) handed to the scrutiny owner. Both delegated rows plus the 3
calibration anchors GATE-PASSED: two fresh-cold passes per row, node-exact
against the published ladder raws, zero MISMATCH / GATE-FAIL /
GATE-CRASH / TRUNCATED.

Part SL already published the third-implementation verdict-level batch
scrutiny (32/32; k13/k19 WIN with x3 cold runs each). With this gate both
WIN rows now carry second + third implementation coverage on top of the
ladder's own 4-run primary evidence (50M determinism pair + 32M margin
re-proof + voluntary third cold 50M verify).

This Part consumes NO verdict. The 2 rows stay gate-verified UNCONSUMED
labels. They only BECOME adoption-eligible for a separately declared
adoption Part (EP/ER/EU/EV/EW pattern); the halt-audit's if-adopted
scenario (2 hypothetical UNKNOWN->WIN flips, recorded NOT-ADOPTED) stays
unadopted. The standard 11x11 empty board, every root, S2, class 1/2/4,
and all closure classes stay UNKNOWN. nodes are bookkeeping, never
verdicts. The parked keys k20/k33 remain parked@15M (claimable by a later
lane) and are untouched.

## Rows (machine-derived by scripts/make_kit_parked4_cppgate_20261126.py, 69 maker gates ALL PASS)

| key | expected legal,budget,result,nodes | published label | status |
|---|---|---|---|
| anchor-at2m | 98,2000000,0,2000000 | anchor (budget-ceiling) | GATE-PASS |
| anchor-aj001 | 84,30000000,2,5156075 | anchor | GATE-PASS |
| anchor-af039 | 89,30000000,2,19234232 | anchor | GATE-PASS |
| k13 1152921573327376384:536870912 | 95,50000000,1,16402480 | WIN (L50M ladder; the proof needs ~1.09x the 15M park) | GATE-PASS |
| k19 10376293541461626880:65664 | 95,50000000,1,15379062 | WIN (L50M ladder; the proof completes at ~1.025x the 15M park) | GATE-PASS |

Single-pass node total 58,171,849 (targets 31,781,542 + anchors
26,390,307; equal per-pass anchor condition as SK) / two-pass bill
116,343,698 (bookkeeping, summed from the per-row raws, the SSOT). Gate
run walls: at2m 4/4 s, aj001 12/12 s, af039 44/45 s, k13 37/37 s, k19
35/35 s (environment bookkeeping, never compared).

## Machine

* Gate source: cpp/solvers/kyouen_dfpn_root.cpp at commit
  154f3b7a67b97e13acbaee8b04dc74ddca728d19, sha256 9193f5b6... (the
  delegated pin, machine-read from the published SK kit gate-rows.json by
  the maker; at HEAD eb87a405 the file on main hashes a0786acb... - the
  pin, not the current main copy, is the source authority); headers
  kyouen_residual_micro.hpp 5976935d... / n11_s5_quarantine.hpp
  2e36d694... at the same commit. Built with zig 0.13.0
  `zig c++ -std=c++20 -O2` (tarball zig-linux-x86_64-0.13.0.tar.xz
  sha256 d45312e6...; binary sha256 d376b9e7..., not pinned: source pins
  are authoritative - SK disclosure kept; zig emits its usual glibc
  downgrade toolchain note).
* Runner: SK kit runner rev2 byte-clone (diff = exactly the 2 comment
  lines naming Part SM; asserted inside the maker) sha256 bf7167c1...;
  HARD-STOP on any mismatch; truncated artifacts re-run, never trusted
  (none occurred).
* Audit: EQ rev4 structure via machine transform of the published SK kit
  audit script (diff: module docstring + machine-generated ROWS/RAW_PROV
  + part/schema strings only) sha256 6dbcb5df...; 5 runs rc=0
  byte-identical sha256 a11983dd... (audit_gate.json == run1 == run2 ==
  run3 published; run4 = the post-battery clean-control regeneration,
  also byte-identical, recorded in tamper.log).
* Maker: scripts/make_kit_parked4_cppgate_20261126.py sha256 c01856ed...
  - fail-closed G0..G8, ALL 69 gates PASS; stdout byte-identical across
  two runs; emitted kit bytes byte-identical across those runs.
* Tamper battery: SK kit battery transform (k13 quadruple): T1 audit ROWS
  pin flip -> G3:k13 FAIL rc=1; T2 raw k13.p1 flip -> G2+G3:k13 FAIL
  rc=1; T3 phantom GATE-PASS line -> G4 FAIL 6/5 rc=1; every restore
  byte-verified; clean control rc=0 (tamper.log, t1_result.json).
* Freshness: both target [lo,hi] pairs absent from the canonical head
  16a12390... (Part EW head of record, 6,797 s5verdict rows WIN197 /
  LOSS6600, maker G4) - verdict-unconsumed at declaration and run time.
* Cross-SSOT pinned by the maker (G2): halt-audit.json per_key stages
  incl. base15m park baselines (result 0 / nodes 15,000,000), the
  delegated_cpp_gate_targets block (budget/result/nodes/target line),
  the ladder kit README result lines (k13/k19 "WIN(1) in nodes" with
  legal 95 and the 9193f5b6 delegated-solver pin and the jsreplay
  8458561... pin), the published status.log accounting lines, and the
  Part SL third-impl batch summary (all_pass, 32 rows, k13/k19
  verdict_level_agreement with replica_resolution_nodes 16,402,480 /
  15,379,062, x3 cold runs).

## Run record (2026-11-26, publish-then-execute per declaration, wave A commit d21e506d)

Waves A/B published first (declaration d21e506d; kit wave B 332ce273 with
fetch-back 10/10 byte-identical), THEN the official execution
11:45:34Z-11:50:30Z sequential (anchors at2m/aj001/af039 calibrated
first, then k13, k19 - pre-registered order), all 5 rows GATE-PASS with
(legal,budget,result,nodes) exactly the published ladder values
(output/gate-status.log). Results wave C 17 files (e9be85ff, fetch-back
17/17 byte-identical), audit 26/26 gates and the 3-mode tamper battery
completed after the official passes. Counter-probe re-checked at push
time: no competing k13/k19 gate artifacts on main.

## Status guard

Scheduling and verification only. No verdict is consumed. The canonical
chain head of record 16a12390 (6,797 rows WIN197/LOSS6600) is untouched
by this Part. If a future adoption Part adopts these rows, the
halt-audit's hypothetical class movement for 10376293541461626880:65536
(0 WIN / 8 LOSS / 100 UNKNOWN on the lane-time head 6e49dd84) and the 2
recorded global UNKNOWN->WIN keys are decided by the canonical chain
merge under the parent batch's WIN/LOSS conflict policy, not by this
kit. The two-stone root {60,27}, its remaining third moves {100,108},
and the 11x11 empty board remain UNKNOWN throughout. S5 WIN raws are
not class closure claims and not routes to the root certificate.
