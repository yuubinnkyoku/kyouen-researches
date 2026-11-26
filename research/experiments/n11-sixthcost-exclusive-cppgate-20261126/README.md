# Part SK: sixth-cost exclusive-probe C++ scrutiny gate (k01..k08) (2026-11-26)

Sixth execution of the C++ second-implementation scrutiny gate (after EN
class-30484, EO class-34908, EQ class-30345 b38-win-18, ET class-30345
ES-re-probe-6, EV closure-batch WIN-4) - the FIRST outside the
central-reply closure-batch chain: the delegated pinned C++ gate of the
sixth-cost exclusive-probe batch (declared since 2026-11-21, recorded
unexecuted in every sixth-cost lane session's "no C++ toolchain in this
sandbox" delegation note). The eight delegated rows plus the 3 calibration
anchors GATE-PASSED: two fresh-cold passes per row, node-exact against the
published probe-kit replica raws, zero MISMATCH / GATE-FAIL /
GATE-CRASH / TRUNCATED.

This Part consumes NO verdict. The 8 rows stay gate-verified UNCONSUMED
labels. The 5 WIN rows (k02/k03/k04/k05/k08) BECOME adoptable by a
separately declared adoption Part (EP/ER/EU/EV pattern), against the
already-published 5-WIN if-adopted scenario in the probe kit's
`output/win-finding-ifadopted-k08.json` (five UNKNOWN->WIN class flips;
sixth-cost class children 101->93; remaining third moves {100,108}
unchanged - scheduling facts, not outcome claims). The standard 11x11
empty board, every root, S2, class 1/2/4, and all closure classes stay
UNKNOWN. nodes are bookkeeping, never verdicts.

## Rows (machine-derived by scripts/make_kit_sixthcost_cppgate_20261126.py, 178 maker gates ALL PASS)

| key | expected legal,budget,result,nodes | published label | status |
|---|---|---|---|
| anchor-at2m | 98,2000000,0,2000000 | anchor | GATE-PASS |
| anchor-aj001 | 84,30000000,2,5156075 | anchor | GATE-PASS |
| anchor-af039 | 89,30000000,2,19234232 | anchor | GATE-PASS |
| k01 | 87,15000000,2,10369650 | LOSS | GATE-PASS |
| k02 | 87,15000000,1,7717432 | WIN (no published third-impl yet; this gate IS the second implementation for k02) | GATE-PASS |
| k03 | 81,15000000,1,9255414 | WIN | GATE-PASS |
| k04 | 83,15000000,1,9433024 | WIN | GATE-PASS |
| k05 | 88,15000000,1,13397611 | WIN | GATE-PASS |
| k06 | 89,15000000,2,8182231 | LOSS | GATE-PASS |
| k07 | 87,2000000,2,1419823 | LOSS (2M resolution condition; published 15M pair agrees 2/1,419,823) | GATE-PASS |
| k08 | 89,15000000,1,6195897 | WIN | GATE-PASS |

Single-pass node total 92,361,389 (targets 65,971,082 + anchors 26,390,307;
the anchor condition is the EV-anchor condition, equal per-pass totals) /
two-pass bill 184,722,778 (bookkeeping, summed from the per-row raws, the
SSOT).

## Machine

* Gate source: cpp/solvers/kyouen_dfpn_root.cpp at commit
  154f3b7a67b97e13acbaee8b04dc74ddca728d19, sha256 9193f5b6... (the
  delegated pin; the file has since moved on main - at HEAD 4d1b7db7 it
  hashes a0786acb...; the pin, not the current main copy, is the source
  authority); headers kyouen_residual_micro.hpp 5976935d... /
  n11_s5_quarantine.hpp 2e36d694... at the same commit. Built with zig
  0.13.0 `zig c++ -std=c++20 -O2` (binary sha256 efb30000..., not
  pinned: source pins are authoritative - EN/EO/EQ/ET/EV disclosure
  kept; each official pass is a fresh process on the byte-cloned kit
  inputs).
* Runner: EV runner rev2 byte-clone (EV bytes 31dc23c3; diff = exactly the
  2 comment lines naming Part SK) sha256 36392268...; HARD-STOP on any
  mismatch; truncated artifacts re-run, never trusted (none occurred).
* Audit: EQ rev4 structure emitted by the maker from the EV audit template
  (diff: module docstring + machine-generated ROWS/RAW_PROV) sha256
  14f56c1d...; 4 runs byte-identical sha256 ad139ece...
  (audit_gate.json == run1 == run2 == run3).
* Maker: scripts/make_kit_sixthcost_cppgate_20261126.py sha256 72bbfbcabb5
  ... - fail-closed G0..G8, ALL 178 gates PASS; stdout byte-identical
  across two runs. Honest note in G3: a first draft hand-typed the aj001
  anchor pin with one wrong hex pair; the fail-closed byte-pin gate caught
  it before any emit and pin loading became machine-extracted from the
  published EV kit MANIFEST (EP pin policy, structurally enforced).
* Freshness: all 8 target [lo,hi] pairs absent from the canonical head
  6e49dd84... (Part EM head of record, 6,792 s5verdict rows
  WIN192/LOSS6600) - maker G4, machine-verified.

## Run record (2026-11-26, publish-then-execute per declaration e42e44a4)

Waves A/B published first (declaration e42e44a4, kit 2112241a with
fetch-back 16/16 byte-identical), THEN the official execution
08:22:15Z-08:28:25Z sequential (anchors at2m/aj001/af039 calibrated
first, then k01..k08 in key order), all 11 rows GATE-PASS with
(legal,budget,result,nodes) exactly the published values. Audit 3 runs
byte-identical + the pre-battery clean baseline (overall PASS).
Tamper battery 3/3 fail-closed (T1 audit ROWS pin break ->
G3:k01 rc1; T2 raw k01.p1 nodes byte-alter -> G2:k01 + G3:k01 rc1;
T3 phantom GATE-PASS -> G4 passes=12/11 rc1; every tamper byte-change
asserted before the audit run, every restore byte-verified, final clean
control rc0) - tamper.log. Host: Vibe upgraded sandbox (Debian 13, 2
cores), zig 0.13.0 provisioned from the official upstream tarball
(apt package installation is forbidden in this sandbox; no preinstalled
C++ toolchain); zig's glibc 2.41->2.39 substitution warning disclosed.

## Out of scope

The k13/k19 L50M WINs and the 30 fifth-resumption LOSS rows (no pinned
C++ expectations yet; a future cppgate Part can take them with fresh
pinned targets), every consumed row, the probe dir itself (no raw/output
path of the probe kit written by this Part), the third-implementation
program (parallel lane territory), the parked-4 L50M ladder territory,
and the canonical adoption machinery (no cache file touched): nothing
here is consumed. No adoption, no coverage, no secured-coverage, no root
verdict - the 8 rows become gate-verified UNCONSUMED labels only. The
standard 11x11 empty board, all 19 central-reply roots, S2, class 1/2/4,
the two-stone root {60,27}, and its remaining third moves {100,108} stay
UNKNOWN.
