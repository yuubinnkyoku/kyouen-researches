# n11 central-reply closure batch-15 (class 5830) WIN r001/r002 third-implementation cross-verification (2026-11-22)

Verifier experiment declared as **Part AL** amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`
(declaration push `ef863117`, observed HEAD-before-push `cf485460`).
It follows the Part G/K/O/P/T/W/AA/AD/AG convention: the two batch-15
unconsumed closure WIN rows (r001/r002, 13th/14th overall) are re-solved
with the pinned third implementation (non-df-pn AND/OR minimax
`third_impl.js`, sha256 `08ea958f...`), and only verdict-level agreement
literature is produced. **Verdicts are NOT consumed**; the adoption decision
stays with the scrutiny owner (C++ second-implementation gate pin
`9193f5b6...`). The standard 11x11 empty board, the 19 central-reply
roots, class 5830 (48 unprobed keys r005-r052) and every other class remain
**UNKNOWN**. Nodes/expansions are not verdicts.

## Declaration summary (full text in the note, Part AL)

- targets = the batch-15 probed rows that carry a verdict = **r001 and r002
  only** (both WIN at 15M budget, 2-pass fresh-cold node-exact, published
  raws commit `d1316b19`). The budget-exhaustion rows r003/r004
  (result 0, 15,000,000 nodes, 2-pass) carry no verdict and were NOT
  re-searched (a third-impl re-search of an exhausted row would be a
  budget escalation requiring a new declaration).
- machine-derived inputs only: `scripts/make_inputs_batch15.py` (adapted
  from the published Part AG batch-13 script) re-derives every input from
  the published batch-15 raws (`sources/raw`, 2-pass node-exact asserted
  per row), the published `batch-keys.json` (sha256
  `af3e4c46af0d84bcb248c350283b07e26b901f6e0d196038e24bd1292b133727`,
  class 5830, 52 keys), the published declaring-host `status.log` (PASS
  lines asserted) and the published per-key input CSVs (scaffold commit
  `b04969bc`; derived-vs-published CSV byte-equality asserted). Zero hand
  transcription.
- anchors (published third-impl values reproduced on this host):
  k02a WIN (legal 87) 9,106,337 expansions / 4,991,527 ttHits and
  l1a LOSS (legal 116) 7,660,602 / 3,951,175.
- negatives (must fail closed): ng1 = k02 legal+1 (88 vs derived 87),
  ng2 = k02 stones 6 (vs actual 5).
- method: 1 row = 1 solver = 1 process, cap 300M expansions, wallcap 240s,
  `--memo-power=22`; every target/anchor run twice (a/b) as a determinism
  gate; audit battery `scripts/audit.py` (schema
  `n11-centralreply-closure-batch15-wins-thirdimpl-audit-v1`) run twice
  with byte-identical output.
- host: same declaring-host sandbox as batch-15 itself (hostname
  `135c7b39-6dfa-4499-9038-092e9efeed37`, 2 cores, at most 2 concurrent
  solver processes).

## Gates (all fail-closed; all PASS)

- rules engine: `verify_tbl.js` replica quads 95,670 == third-impl quads
  95,670; 195,044 randomized triples checked, TBL mismatches 0
  (`output/rules-gate.txt`).
- script pins OK: third_impl `08ea958f...` / verify_tbl `c8c52528...` /
  jsreplay `84585617...` (audited by `scripts/audit.py`).
- negatives: ng1 `GATE_FAIL "legal count mismatch: derived=87 declared=88"`,
  ng2 `GATE_FAIL "stone count mismatch: bits=5 declared=6"` (both in
  `output/status.log`, rc=1 as designed).
- anchors a/b both reproduce the published values exactly, and each a/b
  pair is deterministic (see `output/anchors/`).

## Results (honest, verdicts not consumed)

| row | kind | third-impl verdict | expansions | ttHits | wall a/b (s) | replica (batch-15) | agree |
|-----|------|--------------------|------------|--------|--------------|--------------------|-------|
| r001 `[4035788216211603456, 0]` legal 82 | target | **1 WIN, clean** | 2,856,756 | 1,684,754 | 17.34 / 17.47 | WIN, 2,521,302 nodes @15M | **yes** |
| r002 `[3603442651849818112, 128]` legal 82 | target | **1 WIN, clean** | 6,817,094 | 4,153,893 | 42.37 / 42.85 | WIN, 5,973,924 nodes @15M | **yes** |
| k02a legal 87 | anchor | 1 WIN, clean | 9,106,337 | 4,991,527 | 53.03 / 52.91 | published values | exact |
| l1a legal 116 | anchor | 2 LOSS, clean | 7,660,602 | 3,951,175 | 47.58 / 47.07 | published values | exact |

- Both targets are deterministic within their a/b pairs (result,
  expansion, ttHits, reason identical) and both cleanly agree with the
  published replica verdicts (WIN). WALL-INCONCLUSIVE: none. Divergence:
  none.
- Audit battery: **51/51 gates PASS**, run twice, outputs byte-identical
  (`output/audit-summary.json`, schema
  `n11-centralreply-closure-batch15-wins-thirdimpl-audit-v1`,
  sha256 `c008d74b...`).
- Runner note (recorded honestly): the serial `&&` negative pair in
  `runner-all-thirdimpl.sh` short-circuits after ng1's intentional rc=1,
  so ng2 was launched immediately after the runner with the identical
  pinned `run_thirdimpl.sh` invocation; its GATE_FAIL row is recorded in
  `output/status.log` after PARTAL-RUNNER-EXIT. No other deviation from
  the declaration.

## Non-claims

- r001/r002 remain **unconsumed closure WINs** (13th/14th); this experiment
  does not adopt them, does not update any canonical cache, and does not
  flip any class status. The batch-15 exhaustion rows r003/r004 stay
  honest UNKNOWN (their 15M re-search prohibition is unchanged), and
  r005-r052 remain untouched by the batch-15 WIN-HALT rule.
- Batch-13 (Part AI), batch-14 (Part AF) and Part AJ files were read-only
  throughout. No canonical chain cache was modified anywhere in this
  experiment. **The 11x11 empty board remains UNKNOWN.**

File inventory and sha256 of every published file: `MANIFEST-sha256.txt`.
