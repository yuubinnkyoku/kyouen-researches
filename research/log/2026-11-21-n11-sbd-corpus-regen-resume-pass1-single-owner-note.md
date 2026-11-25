# n11 S4BD fresh-corpus regeneration resume (pass 1 k085-k101, s6w, pass 2 as budget permits): single-owner declaration

- Declaration time: 2026-11-21T23:50Z. Lane identity: the n11 long-term lane
  (11x11 weak-solution critical path: re-establish the decided-class corpus on
  the chain-native lineage that closes the S4 boundary, third-move coverage
  119/119 and the root {60,27} certificate).
- Resumed work: the S4 fresh-corpus regeneration lane
  (`research/experiments/n11-s4bd-fresh-corpus-regen-20261121/`, single-owner
  declaration `2026-11-21T15:39Z`, HEAD at declaration `904e7b40b2f8`), whose
  owning session stalled after the k061-k084 pass-1 checkpoint
  (`93ceaab9c3`, 2026-11-21T17:22Z). No raw has been pushed by that lane since
  (verified on latest main before this note). This session declares the resume
  of that exact experiment under its original 101-key claim set: **no new key
  is claimed anywhere**, and every acceptance condition of the original
  declaration remains in force unchanged. HEAD at the moment of this note's
  final pre-push re-fetch: recorded in the push commit message.
- Scope of this session, in order:
  1. Pass 1 (fresh cold 15M replay, `scripts/jsreplay.js`, pinned sha256
     `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`,
     verified byte-equal on this host) for the remaining corpus keys
     `k085..k101` (17 keys), machine order k085..k101, one solver process per
     row, fresh 2^22 PnTT per row, deadline 0, exact-order=count, <=15,000,000
     nodes, cold runs only.
  2. If wall-clock permits: the S6 witness re-execution `input/s6w.input.csv`
     (LOSS witness `(1152921504675009536,536870912)`, legal 87) twice as an
     independent cold determinism pair (fresh TT per run, 15M budget), as
     material for the TARGET_S5 derived-row route of acceptance condition 5.
     The derived cache row itself, the membership/parity machine check
     (`scripts/gen_s6_witness_audit.py`) and the corpus merge are NOT executed
     this session unless every upstream gate is already in hand.
  3. If wall-clock still permits: pass 2 (determinism re-run of settled rows,
     same recipe, one additional cold run per settled key, machine order from
     k001), pushed as incremental `output/raw/kNNN.p2.out` checkpoints.
- Re-verified on this host before declaration (raw evidence kept in the kit):
  - jsreplay pin byte-equal (sha256 `8458...`).
  - All 101 input CSVs regenerated from `input/corpus-def.json`
    (`schema n11-s4bd-fresh-corpus-regen-def-v1`) byte-identical to published,
    exactly as in the k001-k084 audits; `input/s6w.input.csv` matches the
    corpus-def witness entry (stones 6, legal 87).
  - Chain base `merged-exact-s5-after-js-probe-13.cache` sha256
    `60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6`
    (5,756 s5verdict rows); all 101 claimed keys absent from it
    (machine-checked as exact decimal strings); `chain7` keys disjoint from
    the corpus selection (machine-checked).
  - Node-exact validation gate 4/4 reproduced on this host this session
    (at2m x2: result 0 / nodes 2,000,000 / legal 98,99; 15M rows: result 2 /
    nodes 3,651,923 and 5,040,200), byte-stable against the published val
    outputs except wall_s where applicable.
- Stopping rules (fail-closed, unchanged from the parent declaration):
  - Any fresh WIN (result 1) on a corpus key halts further claimed-key starts
    THIS session: the raw is published with an honest label, the class closure
    claim is blocked, no interpretation in-session, hand to the next run / the
    scrutiny owner.
  - A determinism mismatch (pass1 vs pass2) is a hard stop of the batch:
    publish raws plainly, record, defer.
  - Budget-exhausted rows (result 0) stay honest UNKNOWN raws; no forcing, no
    derived cache row this session.
  - k012 (`TARGET_S5`) pass-1 raw (result 0 at 15M, published by the parent
    lane) is accepted as-is and not re-run by this session except through the
    documented s6w witness route.
- No consumption: no cache increment, no merge, no class-status change, no
  coverage or third-move statement, no K item, no knowledge README edit this
  session. Verdicts of the whole table remain unconsumed until the full
  two-pass merge manifest + frontier audit + root-loss audit are published by
  a later run of this lane. Nodes/solved counts are never verdicts. **The
  standard 11x11 empty board, the two-stone root {60,27} and the third moves
  {100,108} remain UNKNOWN throughout.**
- Disjointness (machine-verified on latest main at declaration):
  - Bank full-band recalibration lane (declared `451e0fe8e4`, 22:33Z): not
    touched (its paths: third-implementation experiment dir, own session log).
  - Sixth-cost k03..k43 batch: stays halted under its own stop rule; its keys
    never enter this corpus (the corpus keys are disjoint S4 canonical
    children/unclaimed rows; machine-checked).
  - Pass-1 audit lanes (k001-k084): read-only consumers; this session pushes
    only new raw files (`output/raw/kNNN.p1.out`, `kNNN.p2.out`, s6w raws
    under this experiment dir), a README checkpoint update of this experiment
    only, and its own session log under `research/log/`.
  - All other lanes active since 17:22Z (five-row band, six-row, seven-row,
    s12/s13, three-row, K1058) are non-n11-S4 topics and path-disjoint.
- Environment facts: 2 cores; Node.js v22.20.0; Python 3.12.14; serial
  single-process foreground runs; no C++ toolchain (delegated C++ gate for WIN
  rows remains with the scrutiny owner); this host's raw fetches (raw/ and
  api.github.com) worked with commit-fixed pins; fetch-back byte verification
  on every push; latest `main` re-fetched immediately before every push.
