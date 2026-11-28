# Completion log: n11 fifteenth ladder-top k02 WIN-row canonical adoption

Completion of the Part declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-k02-adoption-declaration.md`
(commit `12d43eb9`, single owner, publish-then-execute). Kit:
`research/experiments/n11-fifteenth-ladder-top-k02-adoption-20261128/`
(commit `26ff68dc`, 9 files; fetch-back 9/9 byte-identical against
the kit MANIFEST via commit-pinned raw CDN + sha256).

## Result

- **New head of record `merged-exact-s5-chain-plus-fifteenth-k02-20261128.cache`
  sha256 `58110025dd5cca7f1e824d8871b50462dc9fcbeac8b9aa69c5f4d33299c894ae`,
  6,900 rows WIN 218 / LOSS 6,682** - exactly the pre-registered shape
  (BASE `3a527d39...` 6,899 rows WIN 217 / LOSS 6,682 + the 1 declared
  fresh WIN row k02 `6052837899185946628:128` WIN(1) nodes 18,247,029).
- Increment sha256 `2b96a3a9...` (1 WIN row); merger `90711961...` x3
  byte-identical; MAKER-PASS x2 with kitout recursive-diff clean.
- G0 pins all sha-verified before use (merger/policy/quarantine/BASE
  head/gate source+headers; 3 source kits re-fetched from published
  commits `48ea76d8`/`f2b8f744` and verified against their published
  MANIFESTs).
- G1 live re-run of the published gate_runner.sh on a scratch kit copy:
  fresh-cold C++ pair at the 50M budget, node-exact vs the published
  raw, `87,50000000,1,18247029` (gate binary rebuilt this session from
  the pinned source `9193f5b6...` with zig 0.13.0, tarball pin
  `d45312e6...`; wall ~78s per maker run).
- Tamper battery 5/5 fail-closed (T1 replica result flip -> G2 replica
  pair mismatch; T2 TI expansions drift -> G2 TI pair mismatch; T3
  gate quad flip -> G1 live re-run; T4 quarantine-key injection with
  re-pinned registry and a fully valid entry -> G4 "quarantined key
  k02"; T5 coherent freshness world with re-pinned BASE -> G3
  freshness) + clean control re-PASS byte-identical; registry and BASE
  restored byte-identical after T4/T5. No output was produced by any
  tamper run (all aborted before G5).

## Disclosures

- Maker is a machine-adaptation of the published fifteenth k03 adoption
  maker (commit `bc535153`), every replacement count-asserted and the
  adapted script re-parsed; two adaptation slips (REPL/GATEKIT/TIKIT
  dict keys and the G2 gate-quad budget literal initially kept
  k03/15M values) were caught by residue grep before any maker run.
- The k02 replica 50M pair is node-identical but not byte-identical
  (wall_s 98/102), the published host-footprint pattern; G2 compares
  (legal,budget,result,nodes)+key fields, never wall_s.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only; fetch-back via
  commit-pinned raw CDN.

## Status guard / next

Adoption bookkeeping only: NO verdict consumed. The k02 WIN row is
cache bookkeeping, never a root/class verdict. Owner class union
precheck [5788, 5804, 5815, 7678] (frozen graph `54f9c364...`);
caveat: shared-owner pre-exclusion - serving class 5804 is already
excluded_now on BASE (k01/k03 WIN win-hit, reaudits `3395d0ec`/
`e6ceb133`). If this adoption closed class 5804's last cost-unknown
child, the closure-ladder exit of class 5804 is measured in the
declared WIN-side flip-census follow-up Part (BASE `3a527d39` ->
SCEN `58110025`; single-owner declaration required). The standard
11x11 empty board, all 19 central-reply roots, the two-stone root
{60,27} and its remaining third moves 100/108 stay UNKNOWN.
Nodes/expansions are bookkeeping, never verdicts.
