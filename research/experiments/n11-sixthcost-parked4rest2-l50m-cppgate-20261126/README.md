# Part SN: sixth-cost parked4rest2 L50M WIN rows C++ scrutiny gate (k20/k33) (2026-11-26)

Eighth execution of the C++ second-implementation scrutiny gate (after EN
class-30484, EO class-34908, EQ class-30345 b38-win-18, ET class-30345
ES-re-probe-6, EV closure-batch WIN-4, SK sixth-cost exclusive k01..k08, SM
parked4 k13/k19): the delegated pinned C++ gate of the sixth-cost
parked4rest2 S5 L50M ladder's two WIN rows - the halt-audit's
"win_raws_needing_scrutiny" / "delegated_cpp_gate_targets" that the ladder
lane handed to the scrutiny owner. Both delegated rows plus the 3
calibration anchors GATE-PASSED: two fresh-cold passes per row, node-exact
against the published ladder raws, zero MISMATCH / GATE-FAIL /
GATE-CRASH / TRUNCATED.

Honest coverage disclosure (pre-registered in the declaration): unlike
k13/k19 (SM), NO third-implementation verdict-level corroboration exists
for k20/k33 (the Part SL batch predates their resolution; its claim
string parks them). After this gate the two rows are
second-implementation-verified on top of the ladder's 4-run primary
battery (50M cold pair + 32M margin re-proof + voluntary third cold 50M
verify), but NOT at the k13/k19 coverage level until a separately
declared third-impl part admits them. Any adoption decision must weigh
that asymmetry.

This Part consumes NO verdict. The 2 rows stay gate-verified UNCONSUMED
labels. They only BECOME adoption-eligible for a separately declared
adoption Part (EP/ER/EU/EV/EW/SP pattern); the halt-audit's if-adopted
scenario (recorded NOT-ADOPTED) stays unadopted. The standard 11x11 empty
board, every root, S2, class 1/2/4, and all closure classes stay UNKNOWN.
nodes are bookkeeping, never verdicts.

## Rows (machine-derived by scripts/make_kit_parked4rest2_cppgate_20261126.py, 70 maker gates ALL PASS)

| key | expected legal,budget,result,nodes | published label | status |
|---|---|---|---|
| anchor-at2m | 98,2000000,0,2000000 | anchor (budget-ceiling) | GATE-PASS |
| anchor-aj001 | 84,30000000,2,5156075 | anchor | GATE-PASS |
| anchor-af039 | 89,30000000,2,19234232 | anchor | GATE-PASS |
| k20 10376293541461626880:33619968 | 95,50000000,1,16196331 | WIN (parked4rest2 L50M ladder; resolves at ~1.08x the 15M park budget) | GATE-PASS |
| k33 12682136550675320832:65536 | 91,50000000,1,15842649 | WIN (parked4rest2 L50M ladder) | GATE-PASS |

Single-pass node total 58,429,287 (targets 32,038,980 + anchors
26,390,307; equal per-pass anchor condition as SK/SM) / two-pass bill
116,858,574 (bookkeeping, summed from the per-row raws, the SSOT). Gate
run walls: at2m 3/3 s, aj001 10/10 s, af039 39/38 s, k20 32/32 s, k33
31/32 s (environment bookkeeping, never compared).

## Machine

* Gate source: cpp/solvers/kyouen_dfpn_root.cpp at commit
  154f3b7a67b97e13acbaee8b04dc74ddca728d19, sha256 9193f5b6... (the
  delegated pin, machine-read from the published SK kit gate-rows.json by
  the maker; the solver file has since moved on main - the pin, not the
  current main copy, is the source authority); headers
  kyouen_residual_micro.hpp 5976935d... / n11_s5_quarantine.hpp
  2e36d694... at the same commit, all three fetched from the pinned
  commit and byte-verified this session. Built with zig 0.13.0
  `zig c++ -std=c++20 -O2` (tarball zig-linux-x86_64-0.13.0.tar.xz
  sha256 d45312e6... re-verified this session after the environment
  restart; binary sha256 3f4a426f..., not pinned: source pins are
  authoritative - host codegen differences expected per the SK/SM
  protocol; the declaration's own build hashed 628bced4..., equally
  unpinned).
* Runner: published SM kit runner byte-clone (diff = exactly the 2 comment
  lines naming Part SN; asserted inside the maker) sha256 f2534b76...;
  HARD-STOP on any mismatch; truncated artifacts re-run, never trusted
  (none occurred).
* Audit: kit scripts/audit_gate.py (machine transform of the published SM
  kit audit script; diff: module docstring + machine-generated
  ROWS/RAW_PROV + part/schema strings only) sha256 23aa7d52...; 4 runs
  rc=0 byte-identical sha256 3fbb449d... (audit_gate.json == run1 == run2
  == run3 published; the post-battery clean-control regeneration inside
  tamper.log is also byte-identical).
* Maker: scripts/make_kit_parked4rest2_cppgate_20261126.py sha256
  a5b91526... - fail-closed G0..G8, ALL 70 gates PASS at kit build time
  (wave B, maker-run by the declaring lane; this executing session
  re-verified every kit byte pin against the published declaration).
* Tamper battery: SM kit battery transform (k20 quadruple): T1 audit
  ROWS pin flip -> G3:k20 FAIL rc=1; T2 raw k20.p1 flip -> G2+G3:k20
  FAIL rc=1; T3 phantom GATE-PASS line -> G4 FAIL 6/5 rc=1; every restore
  byte-verified; clean control rc=0 (tamper.log, t1_result.json).
* Freshness (maker G4): both target [lo,hi] pairs absent from the
  canonical head of record 16a12390... (Part EW head of record, 6,797
  s5verdict rows WIN197 / LOSS6600) - verdict-unconsumed at declaration
  and run time. Note: the canonical head has since advanced at Part SP to
  cc3694bb (6,799 rows WIN199/LOSS6600); the gate re-probe of cc3694bb
  confirms both pairs still absent (k20/k33 remains fresh; the Part SP
  adoption consumed k13/k19 only).
* Cross-SSOT pinned by the maker (G2): halt-audit per_key stages incl.
  base15m park baselines, the delegated_cpp_gate_targets block
  (budget/result/nodes/target line), the ladder kit README result lines
  with the 9193f5b6 delegated-solver pin and the jsreplay 8458561... pin,
  the published status.log accounting lines, and the disclosed Part SL
  third-impl ABSENCE (summary claim string parks k20/k33; 32 rows, no
  k20/k33 entry).

## Run record (2026-11-26, publish-then-execute per declaration, wave A commit 41a4d5d3)

Waves A/B were published first by the declaring lane (declaration
41a4d5d3; kit wave B 08f9fd14 with maker 70/70). THIS execution session
re-verified all 10 published kit byte pins, fetched the pinned gate
source from commit 154f3b7a with all three sha256 pins matching, rebuilt
zig 0.13.0 (tarball sha d45312e6... re-verified), then ran the official
execution 14:00:08Z-14:04:07Z sequential (anchors at2m/aj001/af039
calibrated first, then k20, k33 - pre-registered order), all 5 rows
GATE-PASS with (legal,budget,result,nodes) exactly the published ladder
values (output/gate-status.log). Results wave C 17 files (26a583d0,
fetch-back 17/17 sha256 byte-identical via raw-CDN pin comparison), audit
26/26 gates and the 3-mode tamper battery completed after the official
passes. Counter-probe re-checked at wave-C push time: main head still
8d21dbe8 (no concurrent lane in this territory), no competing k20/k33
gate artifacts on main (code-search "Part SN" / "parked4rest2 cppgate" /
"16196331" probes clean).

Honest environment disclosure: this executing session began AFTER its
sandbox host was replaced mid-download (the zig tarball fetch timed out
and reset the environment; nothing of record value was lost - every kit
byte was re-fetched from main and re-verified against the published
declaration pins before use, and the pinned gate source was fetched fresh
from commit 154f3b7a). The fetch-back text-path probe via the contents
API initially reported false mismatches (a connector text-extraction
artifact); the authoritative fetch-back is the raw-CDN sha256 comparison
above, which was 17/17 byte-identical.

## Status guard

Scheduling and verification only. No verdict is consumed. The canonical
chain head of record (cc3694bb after Part SP; 16a12390 at declaration
time) is untouched by this Part. If a future adoption Part adopts these
rows, the halt-audit's hypothetical class movement and the recorded
flip set are decided by the canonical chain merge under the parent
batch's WIN/LOSS conflict policy, not by this kit; the third-impl
asymmetry above must be weighed first. The two-stone root {60,27}, its
remaining third moves {100,108}, and the 11x11 empty board remain
UNKNOWN throughout. S5 WIN raws are not class closure claims and not
routes to the root certificate.
