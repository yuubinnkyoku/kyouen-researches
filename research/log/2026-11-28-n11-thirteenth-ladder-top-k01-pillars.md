# 2026-11-28 n11 thirteenth ladder-top k01 WIN-row pillars complete

Completion log of the Part declared in
`2026-11-28-n11-thirteenth-ladder-top-k01-pillars-declaration.md`
(declaration commit `c3cb9f7e`, single owner, publish-then-execute;
the k01 target runs happened only after the declaration was on main).
Target: the thirteenth ladder-top escalation k01 WIN row
`1153204147814662144:65536` (class 16757, legal 72, s5_index 556117,
WIN(1) nodes 2,678,305 @15M, escalation kit `12d8359c`, log
`1fe6498e`), head of record `beecb024...`.

## Results (both pillars PASS; two-pillar requirement COMPLETE)

- **C++ scrutiny gate GATE-PASS `72,15000000,1,2678305`**
  (`n11-thirteenth-ladder-top-k01-win-cppgate-20261128`, commit
  `f1f5c49d`): fresh-cold pair node-identical, node-exact vs the
  published escalation raw (wall_s 5 each).  Gate source
  `9193f5b6...` + headers `5976935d...`/`2e36d694...` byte-fetched
  and sha-verified; zig 0.13.0 (tarball pin `d45312e6...`,
  sha256-verified download), `-std=c++20 -O2`.
- Anchors 3/3 GATE-PASS node-exact: anchor-at2m `98,2000000,0,2000000`,
  anchor-aj001 `84,30000000,2,5156075`, anchor-af039
  `89,30000000,2,19234232`; all six anchor raws byte-identical
  (sha256) to the published u03/u04 pillars kit raws (cross-host
  determinism byte-exact).
- Tamper battery 4/4 fail-closed (T1 expected flip rc=43, T2 raw
  nodes edit rc=42, T3 missing input rc=2, T4 gate-rows.json pin
  flip caught by summary gate G2 rc=1) + clean control re-PASS.
- **Third-impl corroboration CORROBORATION-PASS**
  (`n11-thirteenth-ladder-top-k01-thirdimpl-20261128`, same commit
  `f1f5c49d`): third_impl.js `08ea958f...`,
  `--row=k01 --stones=5 --legal=72 --lo=1153204147814662144
  --hi=65536 --cap=400000000 --wallcap=260 --memo-power=22`, returns
  result 1 (A wins), expansions 3,024,529, nodes 1,801,458, quads
  95,670, ttOverwrites 44,704, both cold passes identical except
  wall (8.94 / 8.90 s).  Expansions measured, not pre-registered.
- **Verdict-level WIN(1) agreement across all three implementations**
  (jsreplay replica + C++ gate + third_impl).  The k01 WIN row is now
  pillar-complete.

## Claim status

NO verdict consumed.  No k01 adoption is performed: an adoption Part
additionally requires the standing WIN-side flip-census review, and
class 16757 completion requires k02 (still stage-1 2M UNKNOWN,
parking/L50M only under a future declaration) and Board-verified
free_now at adoption time.  Fetch-back: all 25 published kit files
byte-identical at commit `f1f5c49d`.

## Next work

- k02 resolution under a separate declaration (parked or L50M);
  then the class 16757 adoption review (flip census + Board-verified
  free_now).

## Guards

The standard 11x11 empty board: UNKNOWN.  All 19 central-reply
roots: UNKNOWN.  Two-stone root {60,27}: UNKNOWN.  Third-move pair
{100,108}: UNKNOWN.  Nodes and expansions are bookkeeping, never
verdicts.  (declaration `c3cb9f7e`, kits commit `f1f5c49d`)
