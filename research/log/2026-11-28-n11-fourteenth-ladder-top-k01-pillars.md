# 2026-11-28 n11 fourteenth ladder-top k01 WIN-row pillars complete

Completion log of the Part declared in
`2026-11-28-n11-fourteenth-ladder-top-k01-pillars-declaration.md`
(declaration commit `2215d322`, single owner, publish-then-execute;
the k01 target runs happened only after the declaration was on main).
Target: the fourteenth ladder-top escalation k01 WIN row
`6053401124017274880:0` (class 5804, legal 86, s5_index 198576,
WIN(1) nodes 4,360,661 @15M, escalation kit `5c670bc6`, log
`4b2aceb6`), head of record `d772f73c...` (6,896 rows WIN 214 /
LOSS 6,682).

## Results (both pillars PASS; two-pillar requirement COMPLETE)

- **C++ scrutiny gate GATE-PASS `86,15000000,1,4360661`**
  (`n11-fourteenth-ladder-top-k01-win-cppgate-20261128`, commit
  `35b5fef1`): fresh-cold pair node-identical, node-exact vs the
  published escalation raw (wall_s 8 each, host wall-clock only).
  Gate source `9193f5b6...` + headers `5976935d...`/`2e36d694...`
  byte-fetched and sha-verified; zig 0.13.0 (tarball pin
  `d45312e6...`, sha256-verified download), `-std=c++20 -O2`.
- Anchors 3/3 GATE-PASS node-exact: anchor-at2m `98,2000000,0,2000000`,
  anchor-aj001 `84,30000000,2,5156075`, anchor-af039
  `89,30000000,2,19234232`.  Anchor raws byte-identical (sha256) to
  the published thirteenth kit raws except anchor-af039.p1, which
  differs only in wall_s (published 38 vs this host 39; host
  wall-clock only, node-exact) - cross-host determinism node-exact
  throughout.
- Tamper battery 4/4 fail-closed (T1 expected flip rc=43, T2 raw
  nodes edit rc=42, T3 missing input rc=2, T4 gate-rows.json pin
  flip caught by summary gate G2 rc=1) + clean control re-PASS.
- **Third-impl corroboration CORROBORATION-PASS**
  (`n11-fourteenth-ladder-top-k01-thirdimpl-20261128`, same commit
  `35b5fef1`): third_impl.js `08ea958f...`,
  `--row=k01 --stones=5 --legal=86 --lo=6053401124017274880
  --hi=0 --cap=400000000 --wallcap=260 --memo-power=22`, returns
  result 1 (A wins), expansions 5,009,747, nodes 2,862,666, quads
  95,670, ttOverwrites 937,736, both cold passes identical except
  wall (14.14 / 14.35 s).  Expansions measured, not pre-registered.
- **Verdict-level WIN(1) agreement across all three implementations**
  (jsreplay replica + C++ gate + third_impl).  The k01 WIN row is now
  pillar-complete.

## Claim status

NO verdict consumed.  No k01 adoption is performed: an adoption Part
additionally requires the standing WIN-side flip-census review
(merger pin `90711961...`, expected head row count 6,897 with
WIN 215), and class 5804 completion requires k02/k03/k04 (still
stage-1 2M UNKNOWN, re-escalation only under a future declaration)
and Board-verified free_now at adoption time.  Fetch-back: all 25
published kit files byte-identical at commit `35b5fef1`.

## Next work

- k01 adoption Part under a separate declaration (flip census +
  merger pin `90711961...` + serving class 5804 BASE-side census
  status measurement); k02-k04 re-escalation under separate
  declarations.

## Guards

The standard 11x11 empty board: UNKNOWN.  All 19 central-reply
roots: UNKNOWN.  Two-stone root {60,27}: UNKNOWN.  Third-move pair
{100,108}: UNKNOWN.  Nodes and expansions are bookkeeping, never
verdicts.  (declaration `2215d322`, kits commit `35b5fef1`)
