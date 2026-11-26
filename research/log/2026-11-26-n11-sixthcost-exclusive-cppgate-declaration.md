# Part SK declaration: sixth-cost exclusive-probe k01..k08 C++ scrutiny gate (2026-11-26)

Publish-then-execute declaration for the SIXTH execution of the C++
second-implementation scrutiny gate (after Part EN class-30484, EO
class-34908, EQ class-30345 b38-win-18, ET class-30345 ES-re-probe-6, EV
closure-batch WIN-4) - the FIRST execution outside the central-reply
closure-batch chain. This Part executes the long-waiting delegated C++ gate
of the sixth-cost exclusive-probe batch (`n11-sixthcost-class-s5-exclusive-
probe-10376293541461626880-20261121`): every sixth-cost lane session since
2026-11-21 has recorded the same delegation ("no C++ toolchain in this
sandbox (re-verified); delegated to the scrutiny owner / external C++
resource; any later C++ disagreement fails closed in favor of discarding
the row") for these 8 pinned rows. This session runs on a host with a C++
toolchain and takes the delegation.

The gate re-verifies, two-pass fresh-cold and node-exact against the
published replica raws, the EIGHT delegated rows (the batch's k01..k08
selection:

| key | key [lo,hi] | expected legal,budget,result,nodes | published label |
|---|---|---|---|
| k01 | [1297036692683751424, 1114112] | 87,15000000,2,10369650 | LOSS (parent batch) |
| k02 | [1297036692683751424, 68157440] | 87,15000000,1,7717432 | WIN (parent batch) |
| k03 | [10376293541461626880, 65792] | 81,15000000,1,9255414 | WIN (first resumption) |
| k04 | [10376293541461626888, 65536] | 83,15000000,1,9433024 | WIN (second resumption) |
| k05 | [10376293541461757952, 65536] | 88,15000000,1,13397611 | WIN (third resumption) |
| k06 | [10376293541462675456, 65536] | 89,15000000,2,8182231 | LOSS (fourth resumption) |
| k07 | [10376293542535368704, 65536] | 87,2000000,2,1419823 | LOSS (fourth resumption, resolved at the 2M stage) |
| k08 | [10376293610182148096, 68719476736] | 89,15000000,1,6195897 | WIN (fourth resumption, first non-65536 key_hi row) |

k07 runs at its published 2M resolution condition (its published 15M cold
pair agrees: result 2, nodes 1,419,823); every other row runs at the
published 15M probe condition. All eight quadruples were machine-extracted
by the kit maker from the published probe-kit raws and cross-verified
against `output/win-finding-ifadopted-k08.json` (adoption_requirement text
+ unconsumed_batch_rows), the probe-kit README delegated-target lines, and
the published third-implementation audit summaries (k01/k03/k04/k05/k06/
k07/k08 verdict-level agreement; k02 has NO published third-impl
reproduction - recorded honestly, the C++ gate IS the second implementation
for k02, and the third-impl batch declared by the concurrent lane earlier
today does not cover it either).

This Part consumes NO verdict. The 8 rows stay UNCONSUMED labels; the
gate only makes the 5 WIN rows (k02/k03/k04/k05/k08) adoptable by a
separately declared adoption Part (EP/ER/EU/EV-pattern), with the 5-WIN
if-adopted scenario already published in
`output/win-finding-ifadopted-k08.json` (five UNKNOWN->WIN class flips,
sixth-cost class children 101->93, remaining third moves {100,108}
unchanged - a scheduling fact, not an outcome claim).

## The gate machine (byte-pinned, fail-closed - EN/EO/EQ/ET/EV lineage)

1. Source authority (EV-declared pin): `cpp/solvers/kyouen_dfpn_root.cpp`
   at commit 154f3b7a67b97e13acbaee8b04dc74ddca728d19, sha256
   9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e;
   headers kyouen_residual_micro.hpp 5976935d... / n11_s5_quarantine.hpp
   2e36d694... at the same commit. All three fetched at that commit and
   sha-verified byte-exact this session (the file has since moved on main:
   at HEAD 4d1b7db7 the solver file hashes a0786acb... - the delegated pin,
   not the current main copy, is the source authority; disclosed).
2. Runner: `scripts/gate_runner.sh` sha256 36392268... - a byte-clone of
   the EV runner rev2 (31dc23c3..., itself the EN/EO/EQ/ET runner rev2
   3a8ee4fd bytes; the diff vs the EV bytes is EXACTLY the 2 comment
   lines naming Part SK - disclosed, machine-verified). Two fresh-cold
   passes, one process per pass; acceptance p1 == p2 on
   (legal,budget,result,nodes) and both == the published raw; HARD-STOP on
   any mismatch; truncated artifacts re-run, never trusted.
3. Kit maker: `scripts/make_kit_sixthcost_cppgate_20261126.py` sha256
   72bbfbcabb5c092f75c15ff605c5e2e21a15f2bcf9f2edfa021292084dc8303c -
   fail-closed G0..G8 (178 gates, ALL PASS this session; stdout
   byte-identical across two runs). G0 gate-source pins / G1 probe-kit SSOT
   discipline (input row-spec shape; 2-pass raws identity except wall_s;
   k07 2M-stage resolution pair; voluntary run3-verify identity for
   k02/k03/k04/k05/k08; status.log accounting) / G2 cross-SSOT (witness
   k08 JSON + probe README + third-impl summaries; honest k02 absence) /
   G3 anchors byte pins machine-extracted from the published EV kit
   MANIFEST (a first draft of this maker hand-typed the aj001 anchor pin
   with one wrong hex pair; the fail-closed byte-pin gate caught it and the
   pin loading was re-implemented machine-extracted - EP pin policy,
   structurally enforced) / G4 freshness vs the canonical head
   6e49dd84... (6,792 s5verdict rows WIN192/LOSS6600, Part EM close-out
   head of record; all 8 target [lo,hi] pairs absent) / G8 emit.
4. Audit: `scripts/audit_gate.py` sha256 14f56c1d... - emitted by the maker
   from the EV audit template (EQ rev4 structure; 10-capture-group REPLAY
   regex asserted at import; diff vs the EV template: module docstring +
   ROWS/RAW_PROV only - disclosed). ROWS/RAW_PROV machine-generated from
   the published probe-kit raws; no per-row pin hand-typed.
5. Anchors (calibration, 3, EN/EO/EQ/ET/EV lineage, byte-clone of the EV
   kit input == EQ kit input, MANIFEST-pinned): anchor-at2m @2M
   (98,2000000,0,2000000), anchor-aj001 @30M (84,30000000,2,5156075),
   anchor-af039 @30M (89,30000000,2,19234232).
6. Inputs: `input/k01..k08.input.csv` byte-clones from the probe kit
   (pins in input/gate-rows.json, maker-verified); anchor CSVs
   MANIFEST-pinned.
7. Tamper battery (post-run): `tamper_battery.sh` sha256 2b1c60c9... -
   EV battery structure with k01 rows (T1 break audit ROWS expected pin
   -> G3:k01 fail-closed; T2 raw k01.p1 nodes byte-alter -> G2:k01+G3:k01
   fail-closed; T3 phantom GATE-PASS -> G4 fail-closed). Order per
   protocol: pin-assert -> backup -> tamper -> pre-assert -> audit(expect
   rc1 + named gate) -> restore -> restore-assert -> clean control rc0.

## Host honesty

NEW host (a Vibe upgraded sandbox: Debian 13 trixie, 2 cores, Python 3.12,
Node 22; NO preinstalled C++ toolchain - apt package installation is
forbidden in this sandbox). Zig 0.13.0 was provisioned as the official
upstream tarball (ziglang.org zig-linux-x86_64-0.13.0.tar.xz, `zig
version` -> 0.13.0); the binary is built with exactly the EN/EO/EQ/ET/EV
lineage command `zig c++ -std=c++20 -O2` from the pin-verified sources.
The binary is NOT pinned (EN/EO/EQ/ET/EV disclosure kept: source pins are
the authority; each official pass is a fresh process). Zig's glibc
substitution warning (2.41 requested, 2.39 provided) is disclosed.

Pre-declaration disclosure: the kit maker was run locally to assemble and
validate the kit BEFORE this declaration (ALL 178 gates PASS; the emitted
kit bytes are what wave B publishes). NO solver pass of the C++ machine
has run on ANY of the eight target rows NOR on any anchor before this
publication (stricter than the EV precedent's own disclosure: not even a
calibration anchor has run yet; anchors run first in the official
execution, then k01..k08).

Any disagreement between the C++ gate and the published replica raws is a
hard stop: publish raws plainly, no interpretation, fail closed in favor
of discarding the scrutinized row (probe-kit precedent).

## Execution plan (declared before any run)

Anchors first (at2m@2M, aj001@30M, af039@30M; 2 passes each), then
k01..k08 in key order (k07 at its 2M resolution condition) - 22 fresh-cold
solver passes total, one run at a time on this 2-core host (modest CPU
footprint; no shared-server load concern beyond this). Then the audit
(>= 2 runs byte-identical), the tamper battery, and the close-out
(README + MANIFEST + completion log).

## Concurrency and disjointness

HEAD re-fetched immediately before this push: 4d1b7db7 (2026-11-26T08:10Z,
the concurrent sixth-cost lane's third-impl batch declaration). Repo
probes this session: no sixthcost cppgate kit/log/commit exists on main
(`sixthcost-exclusive-cppgate` 0 hits; maker filename 0 hits). Territory
disjoint from: the third-implementation lane (the k01-k03 experiment dir
and every *thirdimpl* note - this Part writes no third-impl path and runs
no JS), the parked-4 L50M ladder lane (their probe-dir raw outputs; this
Part writes no probe-dir path), the z-strip lane (strip experiment dirs
and z-slice logs), and the canonical adoption machinery (no cache file is
touched). The parked-4 WIN rows k13/k19 and the 30 fifth-resumption LOSS
rows have NO pinned C++ expectations yet and stay OUT of this Part's
scope (a future cppgate Part can take them with fresh pinned targets).

## Out of scope (consumed NOWHERE by this Part)

Every adopted canonical row, the k13/k19 L50M WINs, the 30 fifth-
resumption LOSS rows, and all remaining probe-level unconsumed labels:
nothing here is consumed. Adoption of the 5 gate-passing WIN rows (if the
gate passes) stays with a separately declared adoption Part. No coverage,
no secured-coverage and no root-verdict claim is made anywhere.

## Guarantees

The standard 11x11 empty board stays UNKNOWN. All 19 central-reply roots,
S2, class 1/2/4, the two-stone root {60,27}, and its remaining third
moves {100,108} stay UNKNOWN. nodes are bookkeeping, never verdicts. The
8 rows are gate-verified UNCONSUMED labels on pass - and nothing else.
