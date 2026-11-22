# n11 central-reply closure class 10687 exact-S5 probe batch 16 (2026-11-22)

Batch 16 of the central-reply 19-root closure grind (K0415/K0417 line). Declared
as **Part AM** amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`
(declaration commit `4386ace3`, observed HEAD-before-push `1976f566`,
note blob sha1 `b86f2373`).

## Selection (pre-registered rule: first clean candidate)

Renewed closure ranks 1-13 are all evidence-carrying, WIN-halted or in flight
(16757: b018; 20421: d002; 30345: 30345 cost child of b018's s5 528497;
16371: e002; 12264: f017; 5473: g018; 2634: h045; 8785: z003; 1518: j033;
8106: n005/n006; 16930: p002/p003; 23101: batch-14 in flight by the Part AF
owner; 5830: r001/r002 WIN-HALT batch 15), so the first clean candidate is
**renewed rank 14 class 10687** (mask `[1224979098661617664, 0]`, unknown 52,
groups served 2: (root first=16, third=56) and (first=16, third=64); the 52
still-unknown canonical S5 children all sit in the (16,56) group). The batch
keys are scheduling quantities, never verdicts.

## Declaration summary (full text in the note, Part AM)

- keys: `input/batch-keys.json` (52 keys t001-t052, probe_order 642-693
  contiguous, sha256
  `465cf44721a661ce94babe12212c26c697ebb346392548fcdafaa9d3e8c3dd4e`),
  machine-extracted from the published re-audit probe-worklist (sha256
  `1807e4d2...`) with Board-recomputed legal counts (76-95); per-key input
  CSVs `input/t001..t052.input.csv`.
- pre-declaration failsafes (all fail-closed, all PASS): (1) all 52
  (lo,hi) pairs absent from the canonical merged chain cache (6,027 rows,
  sha256 `95e868d6...`) - 0 hits; (2) quarantine registry (sha256
  `81d23160...`) - 0 hits; (3) no in-batch duplicates (52 key ids, 52
  distinct (lo,hi) pairs); (4) closure-classes.csv rank-14 row
  `14,10687,1224979098661617664,0,52,16,56,2` byte-checked; (5) zero overlap
  with the 608 published batch 1-15 keys; (6) probe_order 642-693 contiguous.
- Part Y refresh reproduction on the declaring host before extraction: the
  pinned 6-input refresh (script + sha-gated graph/cache/update8/Board/policy/
  quarantine) reproduced the published canonical bytes (closure-classes
  `61943b85...`, per-root-coverage `33f01a0c...`, probe-worklist `1807e4d2...`,
  refresh-summary `25987add...`, all cmp byte-identical; the 4th independent
  reproduction on record).
- val-gate: fresh 4/4 node-exact on the declaring host immediately before the
  run (at2m-1/at2m-2 = 0/2,000,000 x2; 15m-1 = 2 at 3,651,923; 15m-2 = 2 at
  5,040,200; forbidden quadruples 95,670) - `output/val-gate/`.
- method: pinned replica `jsreplay.js` (sha256 `84585617...`), 2-pass fresh
  cold replay, budget 15,000,000, 1 solver / 1 row / 1 process, workers <= 2
  (2-core host), 4-key waves, resume-safe, publish=ALL; stop rules as
  pre-registered (mismatch HARD-STOP rc=42, WIN HALT rc=45, exhaustion = honest
  UNKNOWN with same-condition 15M re-search forbidden).

## Result (honest; verdicts NOT consumed; closure NOT claimed)

**52/52 keys all LOSS, 2-pass fresh cold node-exact, zero WIN, zero budget
exhaustion, zero determinism mismatch. Total 168,262,885 nodes per pass** over
the 52 keys (row-by-row machine cross-check vs batch-keys:
`output/row-audit.json`, schema
`n11-centralreply-closure-class10687-batch16-rowaudit-v1`, sha256
`589c1141...`; per-key nodes recorded there; status.log has all 52
`PASS 15000000,2,<nodes>` lines).

Consequence: under the pre-registered batch rule, the all-LOSS closure route
for S4 class 10687 survives its first full probe (the 16th batch overall:
13 WIN-HALT + 3 clean all-LOSS precede it). The 52 LOSS rows are NOT consumed
here: consumption happens only through the fail-closed union merger as a
published increment plus an independent refresh re-audit; this batch alone
asserts no root coverage, no class closure, and no third-move secured claim.
Adoption of the unconsumed closure WINs (now 14: b018/d002/e002/f017/g018/
j033/h045/z003/n005/n006/p002/p003/r001/r002, all third-implementation
cross-verified, Parts G..AL) remains with the scrutiny owner (C++ second
implementation gate pin `9193f5b6...`). The standard 11x11 empty board, the 19
central-reply roots and every class remain **UNKNOWN**. Nodes are not verdicts.

## Host events, honestly recorded (full detail in `output/status.log`)

Two environment resets killed background runner processes mid-batch (15:15Z
witness pass truncations t002.p2/t003.p2; 15:27Z host recycle during wave
t020/t022-t024; plus a /home/user/work scratch wipe at ~15:31Z that destroyed
the declaring host's working copy - the kit checkpoint under
`_19root-refresh-kit/batch10687/` held and became the authoritative state).
Recovery: a `# replay_done` completeness guard was added to `runbatch.sh`
BEFORE any re-run (a pass file counts as complete only with its terminal
line; truncated files carry no verdict line, so their fresh-cold re-run is not
a same-condition re-search of any completed exhaustion row - no exhaustion
row existed in this batch anyway) and the final 7 waves were executed as
foreground one-wave invocations (`scripts/runwave.sh`). All 8 truncated
fragments are preserved under `output/raw-truncated-hostevent/` for
transparency (211 header bytes each, no verdict lines). No stop rule ever
fired; every published raw is a complete 2-pass node-exact pair.

File inventory and sha256 of every published file: `MANIFEST-sha256.txt`.
