# 2026-11-27 n11 tenth-cost k01/k02 C++ scrutiny gate: wave A declaration

Single-owner declaration of the C++ second-implementation scrutiny
gate Part for the two resolved tenth-cost batch rows (replica stage-2
15M cold pairs published in kit
n11-tenthcost-batch-stage1-2m-20261127, commits b8049d8b / 3485348c;
third-impl corroboration CORROBORATION-PASS published in
n11-tenthcost-k01k02-thirdimpl-corroboration-20261127, commit
232a4a52). Publish-then-execute: the official run happens after this
push, in the pre-registered order below.

## Targets (expected quadruples machine-derived from the published 15M replica raws)

- k01 `1297036692683751424:131074`: expected
  `86,15000000,2,6783438` (exact-LOSS(2) row).
- k02 `1297036692683751424:131136`: expected
  `84,15000000,1,8799140` (WIN(1) row, 6th WIN-side gate row of the
  lineage if it passes).

Input pins: byte-clones of the published tenth-cost selection kit
input CSVs (k01/k04... k01 sha256 = input_pin recorded in
input/gate-rows.json, machine sha256-verified against the selection
kit MANIFEST at kit assembly).

## Anchors (byte-clones of the published SW kit anchor inputs; quadruples == the SW kit anchors block)

- anchor-at2m: budget 2000000, expected `98,2000000,0,2000000`
- anchor-aj001: budget 30000000, expected `84,30000000,2,5156075`
- anchor-af039: budget 30000000, expected `89,30000000,2,19234232`

## Pins

- Gate source: kyouen_dfpn_root.cpp @154f3b7a, sha256 9193f5b6...,
  with headers kyouen_residual_micro.hpp (5976935d...) and
  n11_s5_quarantine.hpp (2e36d694...), all fetched from main history
  and sha256-verified on this host before the build.
- Toolchain: zig 0.13.0 (tarball sha256 d45312e6...), built with
  `zig c++ -O2 -std=c++20`; binary not pinned (lineage precedent).
- Runner: byte-clone of the published n11-ninthcost-parked3-l50m
  runner with a comment-block-only transform (code lines
  machine-identical, asserted at kit assembly).
- Freshness: both target [lo,hi] pairs are ABSENT from the canonical
  head of record 47280073... (6,887 s5verdict rows WIN 206 / LOSS
  6,681, sha-verified, absence machine-checked at kit assembly).
- Acceptance: two fresh-cold passes per row; p1 == p2 on
  (legal,budget,result,nodes); both == expected; any mismatch or
  crash is a HARD-STOP, fail-closed. Nodes are bookkeeping.
- Execution order (pre-registered): anchor-at2m, anchor-aj001,
  anchor-af039, k01, k02, sequential.

## Honest disclosures

- Pre-declaration host sanity: the gate binary was built from the
  pinned source before this declaration, but no anchor or target row
  was executed before this push (the zig build itself is disclosed as
  environment preparation).
- The replica and third-impl results this gate corroborates were
  produced and published earlier this session by this same lane.
- A GATE-PASS here brings k01/k02 to implementation pillar parity
  (replica cold pair + C++ gate + third impl); adoption is a separate
  future Part (fresh single-owner declaration, WIN/LOSS conflict
  review, merger 90711961, flip-census review for the k02 WIN row per
  the SZ/EM precedent, BASE 47280073).
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only. Before each push the
  latest main is re-fetched; concurrent-lane conflicts are recorded,
  not forced.

## Guards

Gate bookkeeping only; no verdict is claimed or implied. A WIN(1)/
LOSS(2) gate result is only a verdict-level agreement of the second
implementation with the published first-implementation raws. The
standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Every closure class: UNKNOWN unless a published Part says
otherwise. Nodes are never evidence.
