# Declaration: n11 fifteenth ladder-top k02 WIN-row canonical adoption (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
the adoption maker runs. Any parallel lane must not adopt or audit the
key below until this Part's completion log appears.

## Scope

Canonical adoption (k02-only) of the fifteenth class 5804 k02 WIN row
`6052837899185946628:128` (class 5804, s5_index 212115, legal 87,
WIN(1) nodes 18,247,029 @50M), two-pillar COMPLETE as of completion
log `48ea76d8` (jsreplay replica cold pair node-identical) and the
pillars completion `f2b8f744` (C++ scrutiny gate GATE-PASS
`87,50000000,1,18247029` + third-impl CORROBORATION-PASS result 1
expansions 21,587,934 x2 identical). Base head of record
`3a527d39...` (6,899 rows WIN 217 / LOSS 6,682; k02 verified
fresh/absent from the head by the L50M escalation Part). Declaration
HEAD pin: `d854434fb1b5818b5bc84e38b47c359201383a7f`.

## Method

Fresh maker `make_adoption_fifteenth_k02.py` (machine-adaptation of
the published fifteenth k03 adoption maker
`make_adoption_fifteenth_k03.py` (kit
`n11-fifteenth-ladder-top-k03-adoption-20261128`, commit `bc535153`),
single-row structure identical), fail-closed G0-G6:

- G0 pins: merger `s5_union_merge.py` `90711961...`, policy
  `s5_evidence_policy.py` `78655e94...`, quarantine
  `results/n11-s5-evidence-quarantine.json` `81d23160...`, BASE
  head.cache `3a527d39...` (289,001B), gate source `9193f5b6...` +
  headers `5976933d...`/`2e36d694...` (all byte-fetched and
  sha-verified this session; the three pillar kits re-fetched from
  their published commits `48ea76d8`/`f2b8f744` and verified against
  their published MANIFESTs).
- G1 live re-run of the published C++ gate runner on a scratch kit
  copy at the 50M budget (expected `87,50000000,1,18247029`; wall
  ~40s/pass, single bash invocation).
- G2 re-parse of the three pillars (replica raw pair
  node-identical `08a17318...`/`b6d11625...` - wall_s-only diff, the
  published k02 host-footprint pattern; gate pair; third-impl pair +
  summary cross-check, TI expansions 21,587,934).
- G3 freshness vs BASE (6,899 rows WIN 217 / LOSS 6,682; k02 absent)
  + WIN/LOSS conflict scan.
- G4 quarantine + canonical safety per s5_evidence_policy.
- G5 increment build; G6 merger x3 byte-identical; expected merged
  shape **6,900 rows WIN 218 / LOSS 6,682**, new head of record
  `merged-exact-s5-chain-plus-fifteenth-k02-20261128.cache`.

Pre-registered expected shape: rows 6,899+1, WIN 217+1, LOSS 6,682+0.
Maker run twice; kitout recursive diff must be clean. Tamper battery
fail-closed on distinct maker gates + clean control.

## Non-meaning

Adoption bookkeeping only: NO verdict consumed. The k02 WIN row is
cache bookkeeping, never a root/class verdict. Owner class union
precheck (derived from the frozen graph `54f9c364...` in the L50M
escalation Part): **[5788, 5804, 5815, 7678]**; caveat: shared-owner
pre-exclusion as measured in the fifteenth k01/k03 reaudits - serving
class 5804 is ALREADY excluded_now on BASE (k01/k03 WIN win-hit,
reaudits `3395d0ec`/`e6ceb133`), so the naive flip prediction is the
remaining owner-side statuses to be measured in the WIN-side
flip-census review (declared follow-up Part). If this adoption closes
class 5804's last cost-unknown child, the closure-ladder exit of
class 5804 is measured then (Board-verified free_now at audit time).
The standard 11x11 empty board, all 19 central-reply roots, the
two-stone root {60,27} and its remaining third moves 100/108 stay
UNKNOWN. Nodes/expansions are bookkeeping, never verdicts.

## Disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The gate binary is rebuilt in this execution environment from the
  pinned source `9193f5b6...` with zig 0.13.0 (tarball pin
  `d45312e6...`, sha-verified); it is the same source/build recipe as
  the published k02 cppgate kit GATE-PASS. The G1 live re-run
  re-verifies the target row node-exact against the published raw.
- The k02 replica 50M pair is node-identical but not byte-identical
  (wall_s 98/102), the same host-footprint pattern disclosed in the
  published k02 15M and 50M pairs; the maker's G2 compares the
  (legal,budget,result,nodes)+key fields, never wall_s.
- No cross-host replication kit exists for this row; the
  three-implementation pillar agreement plus this host's live gate
  re-run are the standing evidence.
