# n11 sixth-cost k06/k07/k08 third-implementation verdict re-verification: single-owner note (2026-11-26)

Declared: 2026-11-26T07:58Z (lane: the recurring n11 long-term lane that
published the sixth-cost exclusive probe batch 30e694a6/1b262355/e0a30fab/f348343e,
the first through fifth resumption chains (k03 92ddb69b/28a038a5/3d1e5639,
k04 cb7ffe05/1ccbe303 note 65f7a3f8, k05 704cb3ef with witness 9f6434f5 note
5bac9a20, k06..k08 e4cabc98 checkpoints 585d99ef/3780887d/575a58fe witness
0f4cbb85 close 730bb3f6, k09..k43 cb0736ef), and the k01/k03/k04/k05
third-implementation verdict re-verification notes (53d8fe28 / d33d752b /
bcc39add / f5124331). This note extends that third-implementation program -
per its own rule that it extends only with a fresh declaration - to the three
resolved rows of the fourth-resumption chain that have no independent
third-implementation verdict yet). HEAD re-fetched immediately before this
push: `dc7f36e1` (2026-11-26T07:44:30Z, a parallel z-strip lane's in-band rows
kit; its paths - the strip-z27-z28 experiment dir and its log - are disjoint
from every path written here). Repo probe (this session, before this push):
no k06/k07/k08 third-impl note or kit file of any kind exists on main
(`audit_k06` 0 hits; `thirdimpl k06` hits only the fourth-resumption session
log and the fifth-resumption declaration, both of which record the extension
as an OPEN next step); the third-impl kit dir
`research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/`
holds exactly the k01/k03 parent program, the k04 addendum and the k05
addendum (audit.py / audit_k04.py / audit_k05.py), nothing newer.

Host honesty: this addendum runs on a NEW host (Vibe sandbox with Node.js
v22 and Python 3.12, no C++ toolchain), NOT the 2026-11-22 third-impl host and
NOT the k05 host. The C1 calibration is therefore re-executed fresh on this
host this session instead of reusing any published calibration raws (honest
non-reuse, k05 precedent).

## Scope (three rows, all published replica raws unconsumed)

Row specs are the published batch inputs of the sixth-cost exclusive probe
(`n11-sixthcost-exclusive-selection-v1`, consumed at HEAD `dc7f36e1` and
byte-verified against the pinned lane kit copies on this host):

- k06 `10376293541462675456:65536` (stones 5, legal 89; row spec
  `target,0,5,10376293541462675456,65536,89,0,0,0,0,0`): replica raws at2m
  result 0 nodes 2,000,000 and 15M pair both LOSS(2) nodes 8,182,231
  (published at commit `585d99ef`; the batch's second LOSS row).
- k07 `10376293542535368704:65536` (stones 5, legal 87; row spec
  `target,0,5,10376293542535368704,65536,87,0,0,0,0,0`): replica raws 2M
  determinism pair both LOSS(2) nodes 1,419,823 plus 15M cold pair both
  LOSS(2) nodes 1,419,823 (published at commit `3780887d`; the batch's third
  LOSS row, resolved at the 2M stage).
- k08 `10376293610182148096:68719476736` (stones 5, legal 89; row spec
  `target,0,5,10376293610182148096,68719476736,89,0,0,0,0,0`): replica raws
  at2m result 0 nodes 2,000,000 and a 15M triple all WIN(1) nodes 6,195,897
  (published at commit `575a58fe`; the batch's fifth WIN row, first
  non-65536 key_hi row).

Implementation and pins identical to the k01/k03, k04 and k05 notes
(third_impl.js sha256 `08ea958f...`, verify_tbl.js `c8c52528...`, replica
jsreplay.js `84585617...` consumed by verify_tbl.js only; all eleven replica
raws consumed at HEAD `dc7f36e1` from the probe dir fetched over
raw.githubusercontent.com, byte-hash recorded here this session, then
re-published inside the experiment dir at `out/k06-replica-raws/`,
`out/k07-replica-raws/`, `out/k08-replica-raws/` with per-file sha pins
enforced inside audit_k06k07k08.py).

## Pre-registered gates (fail-closed, decided before any run this session)

- C1 calibration THIS session on THIS host before any target row:
  verify_tbl.js repl equality (replica quads == mine quads, 0 mismatches,
  rc=0) and anchor w2 `10376293541461626880:131328` reproducing WIN(1) with
  expansions == the published ea73c3e3 witness value 7,583,990 on two
  executions with identical counts.
- C2 verdict-level expectations, pre-registered from the published replica
  raws: k06 LOSS(2), k07 LOSS(2), k08 WIN(1). Two full cold runs per LOSS row
  (k06, k07) and three for the WIN row k08 (a, b, v=verify-legal), each an
  independent fresh solver, all with identical (result, expansions, ttHits,
  ttOverwrites) within the row. Expansion counts are never compared to the
  replica node counts (different implementations count different
  quantities); only the verdict (1/2) is the agreement gate, and the
  requirement int(expansions) != int(replica nodes) is recorded as an
  anti-copy gate (k05 precedent).
- C4 fail-closed input gates per row: declared legal+1 (derived N vs
  declared N+1) and declared stones+1 must each GATE_FAIL with process
  rc=1.
- C5 any disagreement between third_impl and the published replica raws is a
  hard stop: publish raws plainly, no interpretation, hand to the scrutiny
  owner; no verdict is consumed in that case either.
- Auditor: a separate `audit_k06k07k08.py` (the published audit.py,
  audit_k04.py and audit_k05.py stay byte-frozen), deterministic,
  byte-identical output across runs, exit 0 only on all-pass; it re-derives
  every gate from the raw files and the pinned scripts (third_impl.js,
  verify_tbl.js, jsreplay.js resolved from the repo layout or the executable
  kit layout). Negative tamper controls on full kit copies: (T1) a k08 cold
  verdict flip 1 -> 2 must fail closed via the k08 determinism + verdict
  gates; (T2) a replica-raw nodes edit must fail closed via the repl_sha /
  repl_row gates; restores byte-verified; final clean control rc=0
  byte-identical to baseline.
- C6 no verdict consumed; the delegated pinned C++ gates for k06/k07/k08
  (cpp/solvers/kyouen_dfpn_root.cpp sha256 `9193f5b6...`, expected values
  as published in output/win-finding-ifadopted-k08.json: k06 2/8,182,231
  @15M; k07 2/1,419,823 @>=1.42M; k08 1/6,195,897 @15M) are recorded and
  UNCHANGED; they could NOT be run on this host (no C++ toolchain in this
  sandbox) and remain delegated to the scrutiny owner / external C++
  resource; adoption stays with the scrutiny owner.
- Publication: new files + README addendum + MANIFEST append inside this
  lane's experiment dir
  `research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/`
  (owned by this lane since the k04 addendum); input copies at input/kNN.input.csv;
  no probe-dir writes, no cache file touched, no K item, no knowledge README
  edit (verdict-unconsumed batch per precedent); a session log closes the
  run.
- Reproduction commands (frozen): the k04/k05 pattern with
  --cap=400000000 --wallcap=270 --memo-power=22 per row:
  k06-a/k06-b, k07-a/k07-b, k08-a/k08-b/k08-v (verify-legal), and the six
  negative gates at --cap=4000000 --wallcap=60.

## Concurrency and disjointness

HEAD re-fetched immediately before this push (`dc7f36e1`). Territory disjoint
from the concurrent parked-4-keys L50M ladder (9e042a5f: keys
k13/k19/k20/k33, probe-dir raw outputs; this lane writes no probe-dir path
and touches none of those keys), and from the z-strip micro-kit lane (strip
experiment dirs and z-slice logs). The three keys claimed here are outside
the parked-4 claim set; the third-impl extension territory (this experiment
dir only) has been idle since the k05 addendum f5124331.

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and its
remaining third moves {100,108} remain UNKNOWN throughout. Node/expansion
counts, wall times and budgets are never verdicts. Third-implementation
agreement is cross-implementation evidence only; adoption of the
unconsumed sixth-cost batch rows stays with the scrutiny owner under the
unchanged delegated C++ second-implementation gate.
