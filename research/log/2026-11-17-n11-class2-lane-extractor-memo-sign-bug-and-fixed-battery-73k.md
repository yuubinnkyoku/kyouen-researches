# 2026-11-17 n11 class2 lane: certificate extractor memo-key audit and fixed battery (cost-73k)

Audit base: `main` = `7b9f22899bab8e5d8f9b956a067684d139710c76` (re-fetched immediately before the push; K0906 was taken by the REMO theorem-J lane on the same day, so this item was renumbered K0907 per AGENTS.md).

Checked before editing: `AGENTS.md`, `research/knowledge/README.md`, `research/knowledge/VOCABULARY.yaml`, the v16 repair log `research/log/2026-11-14-n11-class4-lane-v16-memo-key-repair.md`, the milestone-5 experiment README, and the published cost-73k band (manifest `class2-lane-cost73k-win7-certificates-20261117.json`, blob `0892aed0…`).

## Why this audit

The 2026-11-14 v15->v16 runner repair found two memo defects (Uint32Array key sign mismatch, dead 255-sentinel negative bounds) in the runner and explicitly left the other copies — sweep engine, chunk prover, **certificate extractors**, FBT-saturation runners — unaudited, requiring separate versioned audits before reuse. This session audits the WIN7 certificate extractor `class4_child1_cert_extractor_exact.ts` (git blob `52bacf509ea12fad4c936501d30d26b5b66c0085`), the engine behind every published WIN7-D10 certificate extraction including the cost-73k band.

## Findings (both confirmed, both performance-only)

**Bug A (signed memo keys).** `mK0..mK3` are `Uint32Array` while the comparison operands `M0..M3` are int32 JS numbers. Any position occupying cell 31/63/95 has bit 31 set in word 0/1/2, the live word goes negative, and the stored unsigned value never compares equal: `memoFind` never matches such keys and `memoEntry` re-inserts the same key at the next free probe slot on **every visit** — up to 64 copies, which is the key's entire 64-slot probe window (a private window).

**Bug B (dead negative bounds).** `if(h>=0&&d>mNoWin[h]) mNoWin[h]=d;` and the `mNoLose` twin compare against the 255 "unbound" sentinel in the wrong direction; with depths <= 64 they never fire, every entry keeps `nowin=nolose=255`, and both negative-bound shortcuts in `memoFind` are dead.

Soundness is unaffected in both cases: the memo can only miss (never produce a wrong hit or a wrong bound). Every published certificate, node count and verdict remains valid; node counts remain the verbatim-engine values.

## Mechanism quantification (dump analysis)

A dump-only modification (no search-behavior change, no bug fix) exported the whole memo table after a bit-0 first-12-move extraction (verbatim engine, MS=1<<23, 834,262 nodes): 216,719 stored records over 112,731 distinct keys, 16,417 keys with 2..64 copies. **All duplicated keys are high-bit** (bit 31 of k0/k1/k2); no non-high-bit key is stored twice. Max copies = 64; 7 keys own their complete 64-slot window (span exactly 63); every key's copies fit its 64-slot probe window (window fit — the verifier's first draft overclaimed contiguous-run geometry and its own FAIL gate caught it before publication). 125,293 records (57.81%) are high-bit. All 216,719 records have nowin=nolose=255 (bug B). This duplicate-insertion behavior is the concrete mechanism consistent with the published ms18 band bit-0 "clumped-hash insertion failures" stall at 76.6% occupancy.

## Fixed-memo battery (fresh per-bit, byte-identity gated)

Line-level surgery on the verbatim extractor (each bug fix asserted as exactly one line change): fixA replaces `Uint32Array` memo keys with `Int32Array` (exact int32 store/compare); fixB additionally makes the negative-bound updates sentinel-aware. The published cost-73k band (22 bits, S6 child `00000000000000801206000000000400`) was re-extracted per bit in fresh processes at MS=1<<23 with an empty kill table, and every per-root snapshot was byte-compared against the published certificates (split files concatenated):

- fixA: **75,108,849** nodes = 69.23% of the verbatim fresh ms23 battery (108,499,241), −30.8%; 22/22 byte-identical; wall 198.6s.
- fixB: **28,290,025** nodes = 26.07% of verbatim fresh ms23 (−73.9%, 3.83x) and 18.14% of the published ms18 baseline (155,946,109; −81.9%, 5.51x); 22/22 byte-identical; wall 128.5s; bit 0 = 1,277,392 nodes reproduced identically on a second run (determinism gate).
- per-bit memo occupancy is **identical between fixA and fixB on all 22 bits** (removing duplicate insertion fixes the entry set; the negative-bound fix only adds usable bounds to entries, collapsing re-exploration without changing the entry set).
- bit 95: 11,857,737 -> 1,415,400 (0.119).

## Verification and determinism

`verify_extractor_memo_sign_bug_73k_20261117.py`: 24/24 checks pass (pins, source pattern counts, Node.js sign demo, dump regeneration + 20-analysis checks, dump byte-identity across two runs, battery JSON gates). Two full runs produce byte-identical audit JSON. The battery script embeds the measured constants as regression gates; the re-run reproduced all of them exactly.

## Operational incident (recorded as an experiment fact)

An earlier same-day run of this measurement was lost to a sandbox environment reset (the second reset in the session; the first killed an in-flight split/merge worker measurement whose sqlite duplicate analysis exceeded the 300s command limit). All scripts, the verifier, the battery and the publication JSONs were rewritten from scratch and re-run; the fresh battery reproduced the previously recorded totals exactly (fixA 75,108,849 / fixB 28,290,025 / fixB bit0 1,277,392 / bit0 occupied 372,070), which doubles as a determinism anecdote. Lessons applied: push heavy artifacts immediately after generation; never run single commands longer than the 300s environment limit; do duplicate-key analysis with sort-based methods, not one giant sqlite query. The split/merge worker measurement was NOT redone in this session and remains open for a later run.

## Deliberately not done

- The repo-verbatim extractor file is left unchanged: published determinism chains must stay reproducible; adopting the fix for future extractions is a separate lane decision (cf. the v15/v16 split precedent).
- No manifest row opened or closed, no certificate republication (byte-identity is a gate).
- The remaining unaudited copies (sweep engine, chunk prover, FBT-saturation runners) keep their status; each needs its own versioned audit before reuse.

## Published in this commit

- `scripts/verify_extractor_memo_sign_bug_73k_20261117.py`, `scripts/measure_fresh_battery_fixed_memo_73k_20261117.py`
- `output/extractor-memo-sign-bug-verify-73k-20261117.json`, `output/class2-lane-fixed-memo-battery-73k-20261117.json`
- knowledge item `K0907-extractor-memo-sign-bug-and-dead-negative-bounds.md`
- knowledge README bullet and a short experiment-README section pointing at the audit

## Status

No new WIN7/LOSS7 certificate or game verdict was produced. Standard 11x11 empty root, two-stone root `{49,60}`, S2 `{59,60}`, class 2, and class 4 all remain **UNKNOWN**. WIN7-D10 covers individual 7-stone roots within depth 10 only; REFUTED-D10 is not a LOSS proof.
