# Part EQ: closure class 30345 b38-win-18 C++ scrutiny gate (2026-11-25)

Third execution of the C++ second-implementation scrutiny gate in the
central-reply chain (after EN class-30484, after EO class-34908).  All 18
unconsumed batch-38 WIN rows of closure class 30345 plus the 3 calibration
anchors GATE-PASSED: two fresh-cold passes per row, node-exact against the
published batch-38 drive raws, zero MISMATCH / GATE-FAIL / GATE-CRASH.

This Part consumes NO verdict.  The 18 rows remain unconsumed probe-level
WIN labels until a separately declared adoption Part follows (Part EP
pattern).  The standard 11x11 empty board, every root, and closure class
30345 all stay UNKNOWN.  nodes are bookkeeping, never verdicts.

## Target pool (machine-derived by scripts/make_kit_eq_win18_cppgate.py)

Part EF batch-38 probed 49 fresh keys of class 30345: 24 LOSS (consumed by
Part EM), 6 EXHAUSTED (honest UNKNOWN), 19 WIN (unconsumed).  Part EP
adopted ai048 (the dual-class 30484/30345 key, WIN 2,232,854) into the
canonical head fd29a337...; the elementary-geometry maker verifies this via
the EP increment c245bc4c... and confirms all other 18 WIN (lo,hi) pairs
fresh (absent from the 6,747-row head).  Targets, all @15,000,000:

| key | expected legal,budget,result,nodes |
|---|---|
| ai002 | 74,15000000,1,3552766 |
| ai003 | 79,15000000,1,5682652 |
| ai005 | 87,15000000,1,11770537 |
| ai006 | 88,15000000,1,8819998 |
| ai010 | 78,15000000,1,13066796 |
| ai013 | 78,15000000,1,10255279 |
| ai014 | 79,15000000,1,14969659 |
| ai017 | 81,15000000,1,8468415 |
| ai023 | 85,15000000,1,13676098 |
| ai028 | 76,15000000,1,4892185 |
| ai034 | 74,15000000,1,3087464 |
| ai035 | 84,15000000,1,4227036 |
| ai036 | 82,15000000,1,8137160 |
| ai039 | 87,15000000,1,13065437 |
| ai043 | 74,15000000,1,3897909 |
| ai046 | 80,15000000,1,5256793 |
| ai047 | 82,15000000,1,2946085 |
| ai049 | 72,15000000,1,832069 |

Single-pass target node total 136,539,338 (bookkeeping).  Anchors:
anchor-at2m @2M (0, 2,000,000), anchor-af039 @30M (2, 19,234,232),
anchor-aj001 @30M (2, 5,156,075) - inputs byte-cloned from the EO kit,
expected quadruples machine-extracted from the published EO raws.

## Machine

* Gate source: cpp/solvers/kyouen_dfpn_root.cpp at commit
  154f3b7a67b97e13acbaee8b04dc74ddca728d19, sha256 9193f5b6...; headers
  kyouen_residual_micro.hpp 5976935d... / n11_s5_quarantine.hpp
  2e36d694... at the same commit.  Built with zig 0.13.0 `zig c++
  -std=c++20 -O2 -I sources` (binary 1d6ca50d..., not pinned: the source
  pins are authoritative - EN/EO disclosure kept; each official pass is a
  fresh process on the published inputs).
* Runner: EN/EO runner rev2 byte-clone (3a8ee4fd source, disclosed diff =
  the 3 comment lines naming Part EQ).  HARD-STOP on any mismatch; the
  truncated-artifact replay_done guard is never trusted (no truncated
  artifacts occurred in this run).
* Audit: EO rev4 structure (10-capture-group REPLAY regex asserted at
  import).  ROWS/RAW_PROV machine-generated from the published source
  kits; no per-row pin hand-typed (EP pin policy).

## Run record (2026-11-25, publish-then-execute)

Waves A..C published first (declaration 233ebe38, kit 9e8db4b5), then the
official execution 20:38:17Z-20:49:47Z at 2 workers (targets in
PASS-order: anchors-at2m/aj001/af039 calibrated first), all 21 rows
GATE-PASS with (legal,budget,result,nodes) exactly the published values.
Audit: 4 runs byte-identical sha256 c2ff2232271d87459fd6954b5076e3a6462c84
9a15cd891fe51f343c931f0174.  Tamper battery 3/3 fail-closed (T1 audit-pin
break -> G3:ai002 rc1; T2 raw nodes byte-alter -> G2+G3:ai005 rc1; T3
phantom GATE-PASS -> G4 passes=22/21 rc1; every tamper byte-change
asserted before the audit run) + clean control byte-identical
(output/tamper.log).  No MISMATCH / GATE-FAIL / GATE-CRASH / TRUNCATED
event occurred at any point of the official record.

Honest note: one pre-declaration anchor-at2m smoke pass ran in a scratch
/tmp directory for build sanity and was discarded; every published raw is
a fresh official pass.

## Out of scope

The 6 EXHAUSTED keys, the loss-adoptable ai044, the dual-class batch-1 key
b018 (same-condition re-probe prohibited), the k04 sixth-cost WIN, all
other probe-level WINs: nothing here is consumed.  No adoption, no
coverage claim, no root verdict - the 18 rows become gate-verified
UNCONSUMED labels only.
