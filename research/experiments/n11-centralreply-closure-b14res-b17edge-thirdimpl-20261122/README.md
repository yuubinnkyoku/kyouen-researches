# n11 central-reply closure batch-14 residual (class 23101) + batch-17 (class 10661) budget-edge rows third-implementation cross-verification (Part AX, 2026-11-22)

Verifier experiment declared as **Part AX** amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`
(declaration push `9771aa5b`, observed HEAD-before-push `29897108`, no
counter-declaration observed). It follows the Part G/K/O/P/T/W/AA/AD/AG/AL/AR
convention: **13 published 2-pass node-exact replica LOSS rows** are
re-solved with the pinned third implementation (non-df-pn AND/OR minimax
`third_impl.js`, sha256 `08ea958f...`), and only verdict-level agreement
literature is produced. **Verdicts are NOT consumed**; the adoption decision
stays with the scrutiny owner (C++ second-implementation gate pin
`9193f5b6...`). The standard 11x11 empty board, the 19 central-reply
roots, class 23101, class 10661 and every other class remain **UNKNOWN**.
Nodes/expansions are not verdicts.

## Declaration summary (full text in the note, Part AX)

- targets = the 10 Part AW batch-14-residual rows **q043..q052** (all LOSS,
  replica raws published at `cb94f808`, experiment
  `research/experiments/n11-centralreply-closure-class23101-batch14-residual-20261122/`)
  plus the 3 batch-17 budget-edge rows **u031 / u033 / u038** (all LOSS,
  replica raws published at `ffc09de1`, experiment
  `research/experiments/n11-centralreply-closure-class10661-batch17-20261122/`;
  u031 is the whole-batch max-nodes row 14,967,263 directly under the 15M
  budget, u031/u033 p2 passes are fresh-cold retries after host resets, all
  disclosed in the published batch-17 status log). The other 39 batch-17
  rows and the remaining Part AQ batch-14 rows (38 LOSS rows; q042 and
  q039-q041 were already covered by Part AR) are NOT re-searched here (a
  future declaration can extend coverage).
- machine-derived inputs only: `scripts/make_inputs_ax.py` (adapted from the
  published Part AR maker) re-derives every input from the published raws
  (`sources/raw`, 26 files, 13 keys x 2 passes, 2-pass node-exact + `# replay_done` +
  in-budget result-2 asserted per key), the published row-audits
  (AW `6b40b131...`, b17 `c19e768f...`), the published runner status logs
  (`sources/status-aw.log`, `sources/status-b17.log`: PASS-line 3-way
  cross-check, AW 10 PASS lines all result 2 + VAL-GATE 4/4 + WAVE-END
  stop=0, b17 EXECUTION-COMPLETE 52/52 LOSS + P2-TRUNCATED-RETRY honesty
  lines + no fired HARD-STOP), the published batch-keys (b14 `dfde0e90...`
  52 keys probe_order 580..589; b17 `db762175...` 52 keys probe_order
  630/632/637) and the published per-key input CSVs (derived-vs-published
  byte-equality asserted for all 10 AW + 3 b17 targets; anchors/negatives
  byte-equality-checked against the published Part AR experiment inputs).
  Zero hand transcription. Maker run 3x, outputs byte-identical.
- anchors (published third-impl values reproduced on this host):
  k02a WIN (legal 87) 9,106,337 expansions / 4,991,527 ttHits and
  l1a LOSS (legal 116) 7,660,602 / 3,951,175.
- negatives (must fail closed): ng1 = k02 legal+1 (88 vs derived 87),
  ng2 = k02 stones 6 (vs actual 5).
- method: 1 row = 1 solver = 1 process, cap 300M expansions, wallcap 240s,
  `--memo-power=22`; every target/anchor run twice (a/b) as a determinism
  gate; audit battery `scripts/audit.py` (schema
  `n11-centralreply-closure-b14res-b17edge-thirdimpl-audit-v1`) run twice
  with byte-identical output and published console captures
  (`output/audit-run1.txt` == `audit-run2.txt`).
- host: Part AW lane sandbox continuation (hostname
  `0d361abd-8326-412f-9807-412e7abb2894`, 2 vCPU, quota halves per-solver
  throughput under 2 concurrent
  solvers); targets therefore executed sequentially (see honesty record 2
  in `output/status.log`). This is a single-host cross-implementation
  corroboration of published raws produced on other hosts (Part AW:
  same-lane earlier session; batch-17: takeover host).

## Gates (all fail-closed; all PASS)

- rules engine: `verify_tbl.js` replica quads 95,670 == third-impl quads
  95,670; 195,044 randomized triples checked, TBL mismatches 0
  (`output/rules-gate.txt`).
- script pins OK: third_impl `08ea958f...` / verify_tbl `c8c52528...` /
  jsreplay `84585617...` / run_thirdimpl `a0b77d83...` (audited by
  `scripts/audit.py`).
- negatives: ng1 `GATE_FAIL "legal count mismatch: derived=87 declared=88"`,
  ng2 `GATE_FAIL "stone count mismatch: bits=5 declared=6"` (both rc=1 as
  designed).
- anchors a/b both reproduce the published values exactly, and each a/b
  pair is deterministic (see `output/anchors/`).
- audit battery: **163/163 gates PASS**, run twice, outputs byte-identical
  (`output/audit-summary.json`, sha256
  `d1fc8999f9cef22f2bf39abffd329225778c6fd2fc55703dc3e6704bfb9586a9`).

## Results (honest, verdicts not consumed)

| row | kind | third-impl verdict | expansions | ttHits | wall a/b (s) | replica nodes (source) | agree |
|-----|------|--------------------|------------|--------|--------------|-----------------------|-------|
| q043 `[1152921505747697664, 66560]` legal 84 | target | **2 LOSS, clean** | 2,897,806 | 1,750,477 | 8.61 / 8.68 | 2,573,254 (Part AW) | **yes** |
| q044 `[1152921505747697664, 33792]` legal 97 | target | **2 LOSS, clean** | 2,063,808 | 1,324,547 | 6.68 / 6.87 | 1,855,550 (Part AW) | **yes** |
| q045 `[1152921505747697664, 17408]` legal 94 | target | **2 LOSS, clean** | 1,147,664 | 721,096 | 3.73 / 3.68 | 1,028,674 (Part AW) | **yes** |
| q046 `[1152991873351025152, 1140850688]` legal 99 | target | **2 LOSS, clean** | 1,234,919 | 752,013 | 3.96 / 3.89 | 1,101,099 (Part AW) | **yes** |
| q047 `[1152921504892059648, 1040]` legal 82 | target | **2 LOSS, clean** | 611,783 | 409,734 | 2.12 / 2.16 | 557,594 (Part AW) | **yes** |
| q048 `[1152991873351025664, 1140850688]` legal 84 | target | **2 LOSS, clean** | 3,220,649 | 1,946,653 | 10.03 / 9.98 | 2,860,377 (Part AW) | **yes** |
| q049 `[1152991873352073216, 1140850688]` legal 92 | target | **2 LOSS, clean** | 9,553,013 | 5,249,231 | 28.65 / 28.51 | 8,353,244 (Part AW) | **yes** |
| q050 `[1152921505747697664, 33555456]` legal 91 | target | **2 LOSS, clean** | 2,455,153 | 1,454,282 | 7.49 / 7.30 | 2,178,945 (Part AW) | **yes** |
| q051 `[1152921505747697664, 16778240]` legal 97 | target | **2 LOSS, clean** | 1,630,007 | 987,498 | 5.12 / 5.13 | 1,451,266 (Part AW) | **yes** |
| q052 `[1152921505747697664, 9216]` legal 98 | target | **2 LOSS, clean** | 1,441,842 | 900,441 | 4.66 / 4.60 | 1,292,547 (Part AW) | **yes** |
| u031 `[1233986297916293120, 67108864]` legal 97 | target | **2 LOSS, clean** | 17,661,456 | 9,400,266 | 51.99 / 50.65 | 14,967,263 (b17, budget edge) | **yes** |
| u033 `[1224987894754574336, 67108864]` legal 96 | target | **2 LOSS, clean** | 9,004,340 | 4,971,048 | 27.50 / 27.90 | 7,806,486 (b17) | **yes** |
| u038 `[1152921514287366144, 0]` legal 96 | target | **2 LOSS, clean** | 7,705,757 | 4,296,325 | 23.09 / 22.54 | 6,589,964 (b17) | **yes** |
| k02a legal 87 | anchor | 1 WIN, clean | 9,106,337 | 4,991,527 | 53.03 / 53.40 | published values | exact |
| l1a legal 116 | anchor | 2 LOSS, clean | 7,660,602 | 3,951,175 | 22.57 / 22.25 | published values | exact |

- All 13 targets are deterministic within their a/b pairs (result,
  expansion, ttHits, reason identical) and all 13 cleanly agree with the
  published replica verdicts (13/13 LOSS, incl. the budget-edge u031).
  Node counts differ between implementations as expected (ratio ~1.13-1.18);
  only verdicts are cross-checked. Total third-impl expansions 60,628,197
  per pass. WALL-INCONCLUSIVE: none. Divergence: none. WIN: none.
- The Part AW residual enumeration (class 23101 batch-14 key set, 10 rows)
  and the budget-edge trio of the Part AV adoption-declaration's source
  batch (batch-17 class 10661) are therefore corroborated at verdict level
  by an independent implementation (13/13 agreement); adoption decisions
  remain scrutiny-owner blocked and unchanged.
- Runner honesty records (full text in `output/status.log`): (1) a shell
  cwd grouping bug during the first anchor invocation started k02a tag=a
  once before the intended clean invocation (duplicated identical RUN
  line; deterministic fields unchanged; k02a.b never started in that
  shell; Part AR ng1 precedent); (2) targets executed sequentially after
  observing the host CPU quota halving under concurrent pairs (walls stay
  short of the 240s wallcap; deterministic fields wall-independent).

## Non-claims

- This experiment consumes **zero verdicts**: no canonical cache write, no
  class status flip, no root-coverage/ secured claim. The 15 unconsumed
  closure WINs (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/
  p003/r001/r002/q042) wait on the scrutiny owner, and so do the batch-14
  residual 10 LOSS rows and the batch-17 52 LOSS rows (Part AV adoption)
  and their future adoption Parts (`consumed_into_canonical_cache: false`
  in `input/rows.json`).
- Batch-18 and all other lanes were read-only throughout. No canonical
  chain cache was modified anywhere in this experiment. **The 11x11 empty
  board remains UNKNOWN.**

File inventory and sha256 of every published file: `MANIFEST-sha256.txt`
(self excluded).
