# n11 central-reply closure batch-14 (class 23101) q042 WIN + in-wave LOSS trio third-implementation cross-verification (2026-11-22)

Verifier experiment declared as **Part AR** amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`
(declaration push `e640f5b6`, observed HEAD-before-push `a54a9402`, no
counter-declaration observed). It follows the Part G/K/O/P/T/W/AA/AD/AG/AL
convention: the batch-14 WIN-HALT row **q042** (15th unconsumed closure WIN,
takeover batch completed under Part AQ) plus its same-wave in-flight LOSS
rows **q039/q040/q041** (disclosed complete at the halt) are re-solved with
the pinned third implementation (non-df-pn AND/OR minimax `third_impl.js`,
sha256 `08ea958f...`), and only verdict-level agreement literature is
produced. **Verdicts are NOT consumed**; the adoption decision stays with
the scrutiny owner (C++ second-implementation gate pin `9193f5b6...`). The
standard 11x11 empty board, the 19 central-reply roots, class 23101 (its
S5 children and all 52 batch-14 keys) and every other class remain
**UNKNOWN**. Nodes/expansions are not verdicts.

## Declaration summary (full text in the note, Part AR)

- targets = **q042 (WIN, result 1, 9,149,084 nodes @15M budget, 2-pass
  fresh-cold node-exact, published under the Part AQ takeover)** and the
  same-wave LOSS trio **q039 (2,502,014) / q040 (2,175,857) / q041
  (2,514,109)**, all published at publication commit `7b211d38`
  (experiment `research/experiments/n11-centralreply-closure-class23101-batch14-20261122/`).
  The other 38 LOSS rows of the 42 probed are NOT re-searched here (a
  future declaration can extend spot coverage); q043-q052 remain untouched
  by the batch-14 WIN-HALT rule.
- machine-derived inputs only: `scripts/make_inputs_batch14.py` (adapted
  from the published Part AL batch-15 script) re-derives every input from
  the published batch-14 raws (`sources/raw`, 8 files, 4 keys x 2 passes,
  2-pass node-exact asserted per key), the published `batch-keys.json`
  (sha256 `dfde0e90b75fd261b51ef746fe69a16eb182a99f5d2f8e1ff8bfa6efe936d71f`,
  class 23101, 52 keys, scaffold commit `54b7453d`), the published
  takeover-host `status.log` (PASS lines asserted against the raws; the
  `q042 WIN-HALT` stop line asserted present exactly once, the halting
  `WAVE-END q039 q040 q041 q042 stop=1` asserted present, `RUNNER-START`
  asserted present) and the published per-key input CSVs (derived-vs-
  published CSV byte-equality asserted for all four targets). Zero hand
  transcription.
- anchors (published third-impl values reproduced on this host):
  k02a WIN (legal 87) 9,106,337 expansions / 4,991,527 ttHits and
  l1a LOSS (legal 116) 7,660,602 / 3,951,175.
- negatives (must fail closed): ng1 = k02 legal+1 (88 vs derived 87),
  ng2 = k02 stones 6 (vs actual 5).
- method: 1 row = 1 solver = 1 process, cap 300M expansions, wallcap 240s,
  `--memo-power=22`; every target/anchor run twice (a/b) as a determinism
  gate; audit battery `scripts/audit.py` (schema
  `n11-centralreply-closure-batch14-q042-thirdimpl-audit-v1`) run twice
  with byte-identical output.
- host: takeover-lane sandbox (hostname
  `b2377489-0c17-4cee-a000-31ace123892c`, 2 cores, at most 2 concurrent
  solver processes); the batch-14 declaring sessions ran on a different
  sandbox host (takeover host), so this is a cross-host cross-implementation
  corroboration.

## Gates (all fail-closed; all PASS)

- rules engine: `verify_tbl.js` replica quads 95,670 == third-impl quads
  95,670; 195,044 randomized triples checked, TBL mismatches 0
  (`output/rules-gate.txt`).
- script pins OK: third_impl `08ea958f...` / verify_tbl `c8c52528...` /
  jsreplay `84585617...` (audited by `scripts/audit.py`).
- negatives: ng1 `GATE_FAIL "legal count mismatch: derived=87 declared=88"`,
  ng2 `GATE_FAIL "stone count mismatch: bits=5 declared=6"` (both rc=1 as
  designed).
- anchors a/b both reproduce the published values exactly, and each a/b
  pair is deterministic (see `output/anchors/`).

## Results (honest, verdicts not consumed)

| row | kind | third-impl verdict | expansions | ttHits | wall a/b (s) | replica (batch-14) | agree |
|-----|------|--------------------|------------|--------|--------------|--------------------|-------|
| q042 `[1152921505747697664, 1032]` legal 85 | target | **1 WIN, clean** | 10,728,035 | 5,758,042 | 65.14 / 64.78 | WIN, 9,149,084 nodes @15M | **yes** |
| q039 `[1161928704146800640, 16]` legal 99 | target | **2 LOSS, clean** | 2,828,518 | 1,663,204 | 18.12 / 18.09 | LOSS, 2,502,014 nodes | **yes** |
| q040 `[1157425104519430144, 16]` legal 87 | target | **2 LOSS, clean** | 2,425,671 | 1,519,018 | 16.07 / 16.38 | LOSS, 2,175,857 nodes | **yes** |
| q041 `[1152921505747697664, 1028]` legal 90 | target | **2 LOSS, clean** | 2,843,397 | 1,693,916 | 18.10 / 18.19 | LOSS, 2,514,109 nodes | **yes** |
| k02a legal 87 | anchor | 1 WIN, clean | 9,106,337 | 4,991,527 | 56.40 / 57.46 | published values | exact |
| l1a legal 116 | anchor | 2 LOSS, clean | 7,660,602 | 3,951,175 | 47.51 / 47.82 | published values | exact |

- All four targets are deterministic within their a/b pairs (result,
  expansion, ttHits, reason identical) and all four cleanly agree with the
  published takeover-replica verdicts (q042 WIN, the trio LOSS). Node counts
  differ between implementations as expected (e.g. q042 10,728,035
  third-impl expansions vs 9,149,084 replica nodes); only verdicts are
  cross-checked. WALL-INCONCLUSIVE: none. Divergence: none.
- The winning row q042 verdict is therefore corroborated by an independent
  implementation on an independent host: the class 23101 all-52-children-
  LOSS closure route is refuted at verdict level by a two-implementation-
  agreed WIN child (route statement only; adoption remains scrutiny-owner
  blocked).
- Audit battery: **71/71 gates PASS**, run twice, outputs byte-identical
  (`output/audit-summary.json`, sha256
  `18125d63a0b6ae0ad22ec58b10c947c945b775d625b8c6889d1c07b0c06a292b`).
- Runner note (recorded honestly): the first negatives invocation was
  launched with a shell cwd grouping bug; ng1 ran (fail-closed GATE_FAIL)
  while ng2's process never started (`No such file or directory` before any
  solver spawn). The pair was re-invoked with absolute paths; ng1 re-ran
  producing the byte-identical GATE_FAIL row, so `output/status.log`
  carries a duplicated identical ng1 RUN line and one ng2 line. No other
  deviation from the declaration.

## Non-claims

- q042 remains an **unconsumed closure WIN** (15th: b018/d002/e002/f017/
  g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042); this experiment
  does not adopt it, does not update any canonical cache, and does not
  flip any class status. The batch-14 rows (41 LOSS + q042 WIN) stay out
  of the canonical chain cache (`consumed_into_canonical_cache: false` in
  `input/rows.json`); re-audit against the current 6,079-row canonical
  (sha256 `342e8683...`) remains the adopting session's duty.
- Batch-16 (Parts AO/AP), Part AQ files, the finite-field lane and all
  other experiments were read-only throughout. No canonical chain cache
  was modified anywhere in this experiment. **The 11x11 empty board
  remains UNKNOWN.**

File inventory and sha256 of every published file: `MANIFEST-sha256.txt`.
