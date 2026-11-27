# Part SM declaration: parked4 L50M WIN rows delegated pinned C++ scrutiny gate (publish-then-execute)

Date: 2026-11-26 (long-term lane session)

## Scope (single-owner claim, publish-then-execute)

Part SM executes the delegated pinned C++ second-implementation scrutiny
gate for the two UNCONSUMED sixth-cost parked-4-keys S5 L50M ladder WIN
rows (the ladder kit resolved both to WIN(1) at budget 50,000,000 and, per
its declared stopping rule 1, never started k20/k33, which stay parked
at 15M, claimable by a later lane, and are untouched by this Part):

- k13 1152921573327376384:536870912 (legal 95), expected
  legal,budget,result,nodes = 95,50000000,1,16402480
- k19 10376293541461626880:65664 (legal 95), expected
  legal,budget,result,nodes = 95,50000000,1,15379062

These are the halt-audit's "win_raws_needing_scrutiny" rows of
research/experiments/n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-20261126/
(commit 4e87e67b); its "determinism" field records verbatim that "a second
implementation (the pinned C++ kyouen_dfpn_root.cpp) re-verification is
REQUIRED before any row may be consumed; this environment has no C++
compiler, so the task is handed to the scrutiny owner". The published
"delegated_cpp_gate_targets" block of the same halt-audit pins both target
lines, budgets 50,000,000, expected results 1 and expected nodes 16,402,480
/ 15,379,062. Part SL (commit f8bf2939 batch audit) already published the
third-implementation verdict-level batch scrutiny (32/32, k13/k19 WIN x3
cold runs each). After a GATE-PASS here both rows carry second + third
implementation coverage and only THEN become adoption-eligible for a
separately declared future adoption Part (EP/ER/EU/EV/EW pattern); the
halt-audit's if-adopted scenario (2 hypothetical UNKNOWN->WIN flips) stays
recorded and NOT adopted. This Part consumes NO verdict, publishes NO
cache row, flips NO class status, and lays NO route to any root
certificate. The standard 11x11 empty board, the two-stone root {60,27},
its remaining third moves {100,108}, S2, class 1/2/4, and every closure
class stay UNKNOWN throughout. Nodes are bookkeeping, never verdicts.

## Pre-registered protocol (fail-closed, no interpretation)

- Gate source: the delegated pin cpp/solvers/kyouen_dfpn_root.cpp at
  commit 154f3b7a67b97e13acbaee8b04dc74ddca728d19 sha256
  9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e with
  headers kyouen_residual_micro.hpp 5976935d... and n11_s5_quarantine.hpp
  2e36d694... at the same commit (pins machine-read from the published
  Part SK kit gate-rows.json by the kit maker; the source bytes fetched
  from the pinned commit verify all three pins - maker G0). Disclosure
  kept from SK: the solver file has since moved on main (at HEAD eb87a405
  it hashes a0786acb...; the pin, not the current main copy, is the source
  authority). Build: zig 0.13.0 official tarball
  zig-linux-x86_64-0.13.0.tar.xz sha256
  d45312e61ebcc48032b77bc4cf7fd6915c11fa16e4aad116b66c9468211230ea,
  `zig c++ -std=c++20 -O2` binary sha256
  d376b9e7831471ddd7a2ce7c59515a38edc309b9b8bfc9c5b49bcc7c029c41fb
  (recorded, not pinned: source pins are authoritative - SK disclosure
  pattern; zig emits its usual "cannot build new glibc 2.41.0; providing
  instead 2.39.0" toolchain note, recorded here).
- Runner: the published Part SK kit runner rev2 byte-clone (diff = exactly
  the 2 comment lines naming Part SM; assert inside the maker). Row order:
  3 calibration anchors first (SK kit byte-cloned inputs, SK kit
  MANIFEST-sha256.txt pins, equal expected quadruples), then k13, k19.
  Two fresh-cold passes per row, one process per pass. Acceptance per row:
  p1 == p2 on (legal,budget,result,nodes) AND both == the pre-registered
  expected quadruple above. Any MISMATCH / GATE-FAIL / GATE-CRASH /
  truncated output: HARD-STOP, no interpretation, no re-run-and-trust,
  honest disclosure in the completion log. wall_s is never compared.
- Anchors (calibration, expectations machine-read from the SK kit
  gate-rows.json anchors block):
  - anchor-at2m 1152921504606851072:536870946 budget 2,000,000 expected
    98,2000000,0,2000000
  - anchor-aj001 1152922604269469696:65536 budget 30,000,000 expected
    84,30000000,2,5156075
  - anchor-af039 1152921504607895681:68719476736 budget 30,000,000
    expected 89,30000000,2,19234232
- Audit: kit scripts/audit_gate.py (machine transform of the published SK
  kit audit script; diff = module docstring + machine-generated
  ROWS/RAW_PROV + part/schema strings, asserted inside the maker) over the
  kit outputs (raw shape, per-row p1/p2 determinism except wall_s,
  published-raw pins, gate-status accounting, input byte-clones). Tamper
  battery: kit tamper_battery.sh (machine transform of the SK battery:
  k13 quadruple flip on the audit pin / on a raw / a phantom third
  GATE-PASS line; restore + byte-verified; clean control rc=0).
- Freshness (maker G4): both target (lo,hi) pairs are absent from the
  canonical merged head of record 16a12390... (Part EW close-out, 6,797
  s5verdict rows WIN 197 / LOSS 6,600, published file
  research/experiments/n11-centralreply-sixthwin5-adoption-predecl-20261126/
  output/merged-exact-s5-chain-plus-sixthwin5-20261126.cache), so both rows
  are verdict-unconsumed labels at declaration time.
- Kit maker: scripts/make_kit_parked4_cppgate_20261126.py, 69 fail-closed
  gates ALL PASS at build time (G0 gate-source pins; G1 parked4-kit SSOT
  discipline incl. base15m park baselines, the l50m-run1/run2 pairs, the
  32M margin re-proof raws, the voluntary run3-verify raws, the published
  two-target validation rows, the status.log accounting; G2 cross-SSOT vs
  the halt-audit per_key/delegated blocks + the ladder kit README lines +
  the pinned solver/jsreplay pins + the published third-impl batch
  summary; G3 anchor byte-pins vs the SK kit MANIFEST; G4 canonical-head
  freshness; G8 emit + ASCII-only assertion + clone byte-verification).
  Maker stdout byte-identical across two runs; emitted kit bytes
  byte-identical across those runs (determinism pre-checked).

## Pre-registered kit byte pins (published in wave B right after this log)

Kit root: research/experiments/n11-sixthcost-parked4-l50m-cppgate-20261126/

- input/k13.input.csv =
  298dd6e6b6655d12aefaae138a2e1d85388220546ff68e4d6b7081c6097b0526
  (byte-clone of the ladder kit input/batch-k13.input.csv)
- input/k19.input.csv =
  88c107d7d060ef756a394d722de3a80b4ee60bad5647785cbbb65eb088da6190
  (byte-clone of the ladder kit input/batch-k19.input.csv)
- input/anchor-at2m.input.csv =
  ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348
  (byte-clone of the SK kit input; == EQ/EN/EO/EV kit input)
- input/anchor-aj001.input.csv =
  2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c
- input/anchor-af039.input.csv =
  e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691
- input/gate-rows.json =
  9818accccba39af567c6a5b9f5e32a5267838a4a0299c691cf4a2ede7f60581a
  (schema n11-sixthcost-parked4-cppgate-rows-v1)
- scripts/make_kit_parked4_cppgate_20261126.py =
  c01856edbfcca15d0f8cdac0c902b353281d10d29c7082911151cb6f8440f32a
- scripts/audit_gate.py =
  6dbcb5df6fe9dcf46e6c48eb2a656f1669444b58854bc311fa7f5dd97e9332c0
- scripts/gate_runner.sh =
  bf7167c1b7d793e2dcbe80817d63de4013179639f3ecd54141f18e0c25346446
- tamper_battery.sh =
  b5b6e81a9c1a17cdc3faf8e8d6b47598f74aea840d4925503f471d71be89038a

## Counter-probe record (claim-clean)

Content probes run at build time AND at push time (HEAD eb87a405,
2026-11-26T11:4xZ): search_code queries "parked4" + "cppgate",
"15379062" under research/experiments, "16402480" (earlier build probe),
"Part SM", "delegated_cpp_gate_targets". Zero competing k13/k19 C++ gate
artifacts exist on main: "Part SM" returns nothing; the expectation values
appear only in the ladder kit itself, the Part SL third-impl replica raws
and the third-impl batch summary; "delegated_cpp_gate_targets" appears
only inside the ladder kit. The sixthwin5 dossier kit mentions the
parked4 rows only as NOT adopted records. ("Part SN" also returns nothing;
SM is the next free slot after SK/SL.)

## Environment disclosure

This session is a long-term lane run without access to the user's machine
(the Vibe desktop app is not attached); every repo interaction happens
through the GitHub API, and the pinned C++ build happens in this sandbox
with zig 0.13.0 as in Part SK. All published waves get curl + cmp/sha256
fetch-back byte verification. If any push fetch-back fails, or a
concurrent lane pushes into the same territory first, this lane re-reads
the latest main, does not force its way, and records the situation
honestly for the next session instead.

## Status guard

Scheduling and verification only. No verdict is consumed. Unknown stays
unknown. The parked keys k20/k33 remain parked@15M (claimable by a later
lane) and are not touched by this Part. If any row GATE-FAILs, both rows
stay exactly as the canonical chain has them and the failure is recorded
as an experimental fact with full raws.
