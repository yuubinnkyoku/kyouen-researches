# 2026-11-27 n11 eighth-cost k01 WIN row C++ scrutiny gate: completion log

Part of the eighth-cost lane (class 1297036692750860288:0 exclusive S5
probe, single-owner selection `8e76eaf6` / kit `16bd63ad`, ladder wave C1
`60b76de9` + C2 `0005e5b1` with the k01 WIN(1)@15M resolution and the
WIN stopping rule, third-impl corroboration `8914c50c` / `68869220`).

This Part closes the C++ second-implementation scrutiny gate on the
single eighth-cost WIN row k01 (1297036692750860288:64, legal 84), the
remaining vacant pillar before adoption-eligibility.

## What was done (publish-then-execute)

- Wave A declaration `28b01ced`
  (research/log/2026-11-27-n11-eighthcost-k01-win-cppgate-declaration.md):
  target, expected quadruple (machine-derived from the published at15m
  cold pair, both raws sha256 3be9db9b76f5dbd2756ffe51a2eb4e2c62c09f12d
  6999f7bc9a0376075479062), anchors, pins, stop rules pre-registered.
- Wave B kit `7ed92d18`
  (research/experiments/n11-eighthcost-k01-win-cppgate-20261127/):
  maker gates all PASS (gate source pins 9193f5b6 @154f3b7a + headers,
  k01 input manifest pin a5a18d5e, at15m pair sha 3be9db9b x2 +
  cold-pair identity except wall, expected 84,15000000,1,8514427
  derived from raw run1, at2m UNKNOWN stage raws pinned, canonical head
  5b6e77f7 sha+census 6,874/WIN202/LOSS6672 with the k01 pair ABSENT,
  anchors == SW kit anchors block, anchor inputs SW byte-clones, runner
  = SX runner comment-only transform), 2 maker runs byte-identical.
- Wave C results `86d9659e`: official execution 07:11:06Z-07:13:29Z
  (zig 0.13.0, tarball sha256 d45312e6..., zig c++ -O2, binary not
  pinned; pre-registered order anchor-at2m, anchor-aj001, anchor-af039,
  then the single k01 target; 2 fresh-cold passes per row):

  **k01 GATE-PASS 84,15000000,1,8514427** - the pinned C++ second
  implementation reproduces the published WIN(1) verdict of the at15m
  cold pair node-exactly (2-pass determinism; second WIN-side row of
  the gate lineage after SX). Anchors also GATE-PASS:
  at2m 98,2000000,0,2000000 / aj001 84,30000000,2,5156075 /
  af039 89,30000000,2,19234232.

- Audit: fresh single-row fail-closed audit PASS 31/31 gates, 3 runs
  byte-identical (output/audit_gate.json sha256 4c3a81fc575f7e36aa85f0
  9e3b0befb30d5def5c6c4ea4df8cb7e017eb038b7e), including the G6
  canonical-head freshness re-verification (head sha, census, k01
  absent). Tamper battery 3/3 fail-closed on a scratch copy (T1 audit
  expected pin flip -> G0:target-expected + G3:k01 / T2 raw k01.p1
  nodes edit -> G2:k01 + G3:k01 / T3 phantom GATE-PASS line -> G4)
  + clean control rc=0 (tamper.log).
- Wave D: README run record + refreshed MANIFEST (25 files) + tamper.log.

## Status

k01 (1297036692750860288:64) now has all three implementation pillars:
replica cold pair (3be9db9b x2), C++ second-implementation gate (this
Part), third-implementation CORROBORATION-PASS (third_impl 08ea958f,
WIN(1) expansions 9987963 x2). It is adoption-eligible under the k05
precedent; adoption stays a separately declared Part with a fresh
declaration and the parent batch's WIN/LOSS conflict review.

NO verdict is consumed. The k01 WIN row stays a gate-verified
UNCONSUMED label; the canonical head of record 5b6e77f7 (6,874
s5verdict rows WIN202/LOSS6672) keeps the k01 pair absent. The
standard 11x11 empty board, every central-reply root, the two-stone
root {60,27}, its remaining third moves {100,108}, S2, class 1/2/4 and
all closure classes stay UNKNOWN. WIN(1) raw rows transfer nothing;
nodes are bookkeeping, never verdicts.

## Honest disclosures

- The pre-declaration sanity run of anchor-at2m on this host (probe
  copy, before the wave A push) already reproduced 98,2000000,0,2000000
  (environment calibration; disclosed in the README run record).
- The audit is a fresh single-row implementation written with the
  published SX audit as the structural precedent (SS/SX precedent,
  disclosed); it adds a G6 canonical-head freshness gate (SX has no
  head re-verification at audit time).
- The maker is a structural clone of the published SX maker with the
  eighth-cost pin set; the tamper battery is the SX battery adapted to
  the k01 quadruple and the K01_HEAD env; both disclosed in-source.
- Environment: this session could not reach the user's computer
  (scheduled-task run); all publication went through the GitHub API,
  all SSOT inputs were re-fetched from main and sha-verified before the
  maker gates ran.

## Addendum (wave D correction)

The first wave D MANIFEST (commit c7d5a7db) listed a stray non-source
entry scripts/__pycache__/audit_gate.cpython-312.pyc (a local
py_compile artifact, never pushed to main). The kit bytes themselves
were unaffected (24/25 fetch-back matches; the single mismatch was the
never-published .pyc). The .pyc was removed and the MANIFEST
regenerated (24 entries, all published files) in the follow-up commit;
fetch-back of the corrected MANIFEST is 24/24.
