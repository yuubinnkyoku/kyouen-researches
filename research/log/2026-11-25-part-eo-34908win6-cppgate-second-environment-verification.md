# Part EO second-environment verification: kit + published outputs fully re-verified, plus an independent 9/9 battery replication on a third host build - all node-exact, zero discrepancies (2026-11-25)

Verification run of Part EO (`research/experiments/n11-centralreply-closure-class34908-cppgate-20261125/`,
declaration `74ec7b17`, outputs `16f578a9`, close-out `50acaf6e`). This lane's
verification is read-only with respect to the Part EO single owner: no
EO-owned file was modified; every executable step below ran in this session's
own detached scratch, from bytes fetched sha-pinned at the fixed commits.
This log is the only file published by this verification.

## 0. Honest scope note: handover after a near-collision

This session began by independently following the Part EN close-out's own
next-step list (option (b): gate class 34908's 6 WIN rows). It had, in scratch:
(a) byte-verified the same pin stack (cpp pin `9193f5b6...` at
`154f3b7a67b97e13acbaee8b04dc74ddca728d19` + both header pins
`5976935d...`/`2e36d694...`), (b) built a binary from that source
(zig 0.13.0, below), (c) fetched and pin-verified all 16 b33/EA provenance
raws plus the EG `rows.json`, and (d) drafted a kit variant (same 9 rows plus
an af029-30m row and a per-key budget-whitelist runner delta). The pre-push
latest-main re-fetch rule then surfaced the competing single-owner
declaration `74ec7b17` (19:26:14Z). ZERO repo writes had been made by this
session at detection time, so the scope was handed cleanly to the declared
owner and this session converted to second-environment verification. The
protocol worked exactly as designed; nothing was re-declared or duplicated.

Two local defective artifacts existed ONLY in this session's scratch and
never reached the repo (recorded for the lesson ledger):

- the drafted runner adaptation contained a transcription defect
  (`f2` replay fields cut `-f4,7,8` instead of `-f4,6,7,8`; same class as
  EN rev1's field-index bug). A typed smoke battery (correct-pass +
  wrong-expected-must-rc43 + whitelist-rejection-must-rc3) caught it before
  any official run. Re-confirms the lesson: exercise the field-reading paths
  with must-fail cases before any official battery.
- the drafted `budget-map.txt` whitelist variant is superseded: the
  published EO runner is byte-EN-rev2 (no whitelist). The af023/af048 15M
  prohibition is procedural in the published kit (the batch table pins 30M
  only). Not a defect; flagged for future kit authors: my local variant
  demonstrates a structural enforcement is possible (rejects af023@15M with
  rc=3 before any execution).

## 1. Pin verification (all byte-exact, independent re-fetch)

- Gate source stack: `kyouen_dfpn_root.cpp`
  `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`,
  `kyouen_residual_micro.hpp`
  `5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5`,
  `n11_s5_quarantine.hpp`
  `2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5`
  (all fetched at `154f3b7a67...`): all three MATCH (same bytes EN/EO
  verified).
- zig 0.13.0 tarball `47,082,308 B`, sha256
  `d45312e61ebcc48032b77bc4cf7fd6915c11fa16e4aad116b66c9468211230ea`
  MATCH (independent download, byte-identical to the EO session's artifact).
- EO kit at `74ec7b17`: 9 input CSVs MATCH the EG-kit pins
  (`bb661fbb`)/EN-kit pins (`949e68a7`) exactly (all nine sha256s equal the
  audit G5 values); runner logic-identical to EN rev2 modulo header comment
  (comment-stripped diff: empty); audit REPLAY regex has exactly 10 capture
  groups WITH a startup `assert REPLAY.groups == 10` (EN rev4 lesson
  structurally enforced). Expected values of all 9 rows cross-checked
  field-wise against the published b33/EA raws fetched independently from
  main (sha re-verified against the EG declaration pins 16/16 + EA anchor
  pair 2/2): no divergence. The EG `rows.json` (fetched, schema check) agrees
  row-wise.

## 2. Independent full-battery replication (third host, third binary)

Battery: the published runner bytes + the published 9 inputs, executed
against this session's own binary built from the same pinned source (`zig
c++ -std=c++20 -O2`, 118s, binary sha256
`b4a5188a9a796ef4d5d740724f437e1a2d3f9801996f43bb2fd0fab93a3832b9` -
third distinct host build after EN `d27acf47...` and EO `330ce012...`; all
three from the same source pins). 9 rows x 2 fresh-cold passes, sequential
single worker, window 19:38:50Z-19:45:22Z (started after the EO owner's
official batch had finished; the two batteries are fully independent).

Result: 9/9 GATE-PASS; p1==p2 per row on all replay fields except wall_s;
all (legal,budget,result,nodes) node-exact against the published pins.
Total nodes: 100,338,525 per pass (200,677,050 both passes) - byte-equal
arithmetic to the EO close-out's own total.

Cross-run vs the EO published raws (`16f578a9`), fields 1-8,10,11
(wall_s excluded): 18/18 identical. Beyond that, 4 raws are byte-identical
INCLUDING wall_s across the two sessions (same second-granularity wall clock):
anchor-at2m p1/p2 `cfa72d66...` (also byte-identical to the EN published
at2m raw per the EO close-out - a three-session byte confluence) and
af029 p1/p2 `7eaa8e6e...`. All other rows differ only in wall_s
(e.g. af023 57/58s here vs 61/62s there), as expected.

## 3. Audit and tamper verification

- Published outputs (`16f578a9` + `50acaf6e`): `audit_gate.json` overall
  PASS, 46 gates, zero FAILs; the four `audit_gate*.json` byte-identical
  (sha256 `b46f2130...`); `gate-status.log` exactly 9 GATE-PASS lines, zero
  MISMATCH/GATE-FAIL/GATE-CRASH; `tamper.log` 3/3 fail-closed with
  sha-change pre-asserts + control byte-identical.
- MANIFEST-sha256.txt: all 37 entries re-fetched at the fixed commits
  (outputs at `16f578a9`, kit/README at `50acaf6e`) and verified on BOTH
  sha256 and size: 37/37 MATCH, 0 mismatches. Close-out completion log
  fetched at `50acaf6e` (9,505 B) and read: claims agree with everything
  this session measured independently.
- This session's own audit replication (published audit bytes run, not
  merely read, against this session's raws): 46 gates ALL PASS x3,
  byte-identical `audit_gate.json` (this session's copy sha256
  `cbaeee5b1fdc1d4f2161b294bdb41d7aaf6fb0ef2f06d941d4ee99b9f3f41022`;
  differs from the EO canonical only in wall-derived detail fields).
- This session's own tamper battery on its scratch copy (complementary to
  the EO battery; every tamper pre-asserted a sha change):
  - T1 raw corruption af047.p1 nodes -1: FAIL `G2:af047` + `G3:af047`, rc=1
  - T2 phantom GATE-FAIL line in gate-status.log: FAIL `G4` (passes=9/9
    bad=1), rc=1
  - T3 one-byte input corruption af050.input.csv: FAIL `G5:af050`, rc=1
    (input-tamper case, not covered by the EO battery - complementary
    detection path)
  - CONTROL pristine copy: rc=0, audit byte-identical to this session's
    canonical.
  3/3 fail-closed + clean control.

## 4. Extra observation (out of the EO batch, consumed nothing)

af029 at the EG-G2c double-reproduction condition, i.e. budget 30M instead
of 15M (published EA anchor row, EG kit sources/ea-raw pins
`1726ecb6...`/`c937f896...` byte-verified by this session's own fetch):
both fresh-cold passes return `replay,0,5,86,0,30000000,1,4862485,...` -
node-exact against the published 30M anchor raw, and identical nodes to the
15M batch row. The budget-independence of af029's WIN-termination node
count, already published for the jsreplay replica via EG G2c, is hereby
reproduced on the C++ second implementation as well, on a third host.
Observation only; nothing consumed.

## 5. Assertions and guards

- This verification consumed NOTHING: no verdict, no adoption, no class
  state change. Class 34908 keeps its 6 unconsumed probe-level WIN rows;
  class 30484 keeps its 4 unconsumed EN-verified WIN rows. Adoption of any
  of them stays a separate Part (pinned merger `90711961...` route, Board
  re-verification, reaudit deltas).
- **The standard 11x11 empty board remains UNKNOWN**; the 19 central-reply
  roots, the two-stone roots {49,60}/{59,60}, S2 {59,60}, and closure
  classes 1/2/4, 30118, 30345, 16371, 20421, 30484, 34908 (every key,
  including adopted rows) remain UNKNOWN. Nodes, expansions and wall clock
  are never verdicts; a GATE-PASS is a second-implementation reproduction of
  a published probe row, not a win/loss claim; probe-level WIN labels under
  a budget ceiling are not class verdicts.
- Single-owner respect: this lane wrote only this log; the Part EO
  experiment dir was never touched. The at2m/af029 byte confluences above
  are observations, not identity claims about host environments.
