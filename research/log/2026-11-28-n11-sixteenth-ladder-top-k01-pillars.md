# Completion log: n11 sixteenth ladder-top k01 WIN pillars (C++ scrutiny gate + third-implementation corroboration)

Declared in `research/log/2026-11-28-n11-sixteenth-ladder-top-k01-pillars-declaration.md`
(commit `60f4bac8`, publish-then-execute, single owner, HEAD pin `07611bec`).
Target: k01 `1155454779397246976:131072` (class 20421, s5_index 528689,
legal 76), the sixteenth ladder-top escalation's WIN(1) row
(nodes 5,273,778 @15M, jsreplay `84585617`, kit `85edd462`).

## Results

1. **C++ scrutiny gate GATE-PASS `76,15000000,1,5273778`**
   (fresh-cold pair post-declaration, two processes, 2-pass
   determinism; node-exact vs the published sixteenth escalation raw
   pair `c246e1da`/`4376868d`). Gate source `9193f5b6` + headers
   `5976935d`/`2e36d694` (standing pins, sha-verified), zig 0.13.0
   tarball pin `d45312e6` re-verified on download, `-std=c++20 -O2`.
2. Anchors 3/3 GATE-PASS, pair node-identical, scratch-run
   pre-declaration on this host (disclosed in the declaration):
   at2m `98,2000000,0,2000000`, aj001 `84,30000000,2,5156075`,
   af039 `89,30000000,2,19234232`, input pins
   `ecc0299b`/`2f6daea5`/`e51a3c9d` byte-verified.
3. Tamper battery 4/4 fail-closed: T1 wrong expected rc=43,
   T2 raw node edit rc=42, T3 missing input rc=2, T4
   gate-rows.json expected flip caught by summary G2 rc=1;
   clean control re-PASS with byte-identical summary; all tampered
   inputs restored byte-identical (sha-verified). Tamper T1/T2 fail
   lines kept in the kit status log as the honest record.
4. **third_impl `08ea958f` CORROBORATION-PASS**: result 1,
   expansions 6,003,522, nodes 3,591,656, ttOverwrites 1,831,190,
   identical on both cold passes (wall_s 18.85 / 19.47), flags
   `--row=k01 --stones=5 --legal=76 --lo=1155454779397246976
   --hi=131072 --cap=400000000 --wallcap=260 --memo-power=22`.
5. **Two-pillar requirement for the k01 WIN row COMPLETE**:
   verdict-level WIN(1) agreement across all three implementations
   (jsreplay replica 5,273,778 nodes; C++ gate 5,273,778 nodes
   node-exact; third_impl result 1 with its own bookkeeping
   expansions/nodes).

## Kits

- `research/experiments/n11-sixteenth-ladder-top-k01-win-cppgate-20261128/`
  (19 files incl. MANIFEST; schema
  `n11-sixteenth-ladder-top-k01-cppgate-summary-v1`; runner
  byte-identical to the standing `f2ebcc3e` runner).
- `research/experiments/n11-sixteenth-ladder-top-k01-thirdimpl-20261128/`
  (5 files incl. MANIFEST; schema
  `n11-sixteenth-ladder-top-k01-thirdimpl-summary-v1`).

## Non-claims / status guard

- NO verdict consumed. The k01 WIN row stays cache bookkeeping;
  adoption is a SEPARATE declared Part (canonical merge into head
  `58110025` (6,900 rows WIN 218) + flip-census/reaudit with the
  disclosed owner-union precheck [15647, 16901, 20421]).
- Class 20421 is NOT complete (k02 `1156299204327378944:131072`,
  k03 `1155173441859489792:131072`, k04 `1153062242096250880:540672`,
  k05 `1152921642046849024:68719477248` remain stage-1 2M UNKNOWN).
- The standard 11x11 empty board, the 19 central-reply roots,
  two-stone root {60,27}, third move {100,108}, and every closure
  class remain UNKNOWN. nodes/expansions/wall_s are bookkeeping.
