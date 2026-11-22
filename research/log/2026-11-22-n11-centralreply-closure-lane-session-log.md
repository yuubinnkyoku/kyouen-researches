# n11 central-reply closure lane session log (2026-11-22, ~02:29-03:12Z)

Compaction-continuation of the long-term lane (empty-board 11x11 weak solve,
K0415/K0417 line). All pushes byte-verified via commit-pinned raw URLs
(curl + md5/sha256). No branch/PR. Single-owner declaration:
`2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`
(completed Parts A+B; Part C amendment added this session).

## Session commits (this lane)

| commit | content |
|---|---|
| `61e3ae3e` | batch 1 (class 16757) raws b001-b016 (16 keys, all 2-pass node-exact LOSS 15M) |
| `33a4d703` | batch 1 **WIN-HALT at b018**: 2-pass node-exact result 1, nodes 3,549,602 both passes; README status; b021-b048 unprobed |
| `24261fff` | batch 2 (class 23963) scaffold + declaration amendment Part C (48 keys from probe-worklist, cache-absent verified 48/48, val-gate 4/4 on host) |
| `77aef9f0`, `c0f574a3`, `a4a0c696` | batch 2 raws c001-c016 / c017-c032 / c033-c048 + status + batch audits |
| `6dc6e1b0` | closure increment merge + class 23963 free re-audit (experiment dir: increment 67 rows, merge audit, refresh re-audit script + outputs) |
| `6657fa74` | merged canonical chain cache (5,924 rows, sha256 `8a721a18...`), single-file commit |
| `610c2997` | re-audit addendum: LF-canonical CSVs + script lineterminator note |
| `aea7abcb` | b018 WIN **IF-ADOPTED analysis** (experiment dir, build + refresh vs if-adopted cache) |
| `ecb5f1be` | if-adopted merged cache (5,925 rows, sha256 `062ff64d...`), single-file commit |

## Findings

1. **b018 WIN (batch 1 halt, pre-registered rule fired)**: S5 528497, key
   `[1153204079095189504, 65536]`, legal 60, result 1, 3,549,602 nodes,
   2-pass node-exact. Consequence: the all-48-LOSS closure route for S4 class
   16757 is refuted by a verified WIN child. Verdict NOT consumed (scrutiny
   owner pending; lane rule).
2. **Class 23963 all-48-LOSS closure route survives batch 2**: 48/48 keys
   2-pass node-exact result 2 at budget 15M, zero WIN/mismatch/exhaustion;
   independent row audit JSON published; total 76,504,609 nodes per pass.
3. **Fail-closed increment**: 67 rows (19 from batch 1 + 48 from batch 2, LOSS
   only) merged into the 5,857-row base cache by the published sha-gated union
   merger (selftest PASS, conflicts 0, duplicates 0) -> canonical 5,924-row
   chain cache (`8a721a18...`).
4. **Class 23963 certified free (closable certificate material) by the
   independent re-verification audit**: refresh re-run vs the merged cache
   (determinism 2/2 byte-identical, all other input pins unchanged, baseline
   control root {27,60}: 119/119 holds): class free_now 32 -> 33,
   board-verified 33/33 rejected 0; class 23963 disappears from
   closure-classes.csv and its worklist slots drop to 0. Machine consequences:
   frozen update8 remaining S5 31,859 -> 31,838 (resolved_count 21), probe
   worklist 65,290 -> 65,213 slots (591 removed), root first=24 free-thirds
   8 -> 10 and root first=26 7 -> 8 (of 119 each; the class's 3 groups are
   2 on root 24 + 1 on root 26).
5. **If-adopted analysis for b018** (analysis only, nothing consumed):
   adopting would flip exactly 3 classes to excluded_now (16757, 30345, 15640 -
   the three cost-child holder classes of s5 528497), win-hit-block 5 update8
   group records (all via class 16757: roots 36 x3, 48 x2), resolved
   requirement 21 -> 22, remaining 31,838 -> 31,809, free_now *unchanged* 33
   (23963 closure unaffected), coverage counts unchanged everywhere.

## Status

- standard 11x11 empty board **UNKNOWN**; all 19 central-reply roots UNKNOWN
  (none resolved by this session); class 16757 UNKNOWN with 29 unknown
  children under the canonical cache (b018 + b021-b048), permanently
  non-closable via all-LOSS once its WIN child is consumed; class 23963 = the
  33rd free/closable class; genuine next all-LOSS candidate = class 20421
  (49 unknown, first=12/third=51, 4 groups, rank 2 in the re-audit
  closure-classes.csv).
- b018 verdict: unconsumed on main, if-adopted analysis published for the
  scrutiny owner (k04 precedent style).

## Operational notes (session-specific)

- The upgraded environment lost the `git` binary (package install forbidden);
  publication went through `github_app.push_files` with commit-pinned raw
  fetch-back verification (curl+md5). HEAD moved 5x mid-session (seven-row /
  six-row lanes, disjoint paths); re-fetch before each push and record the
  observed HEAD-before-push in the message.
- `push_files` **normalizes CRLF to LF in transport**: csv.writer(default)
  CSVs cannot round-trip byte-exactly; the re-audit refresh script now writes
  LF-canonical CSVs (`lineterminator="\\n"`), documented in its header and
  README.
- `tools.file_system.read_file` appears to cap around ~60KB per call for
  single-line payloads (and per-chunk); large files (242KB caches) read fine
  via line-chunked reads (limit 1500 lines); payloads >~60KB must be split.
- knowledge README (repo, 776KB) was NOT appended this session (payload size
  risk via the API route); a git-capable session should append the standard
  bullet for this session per lane convention.

## Resume (next runs)

1. Fetch latest main first (hourly parallel runs; other lanes push actively).
2. Next closure batch candidate: **class 20421** (rank 2 re-audit
   closure-classes.csv, 49 unknown children, first=12/third=51, 4 groups):
   new declaration (Part D) + scaffold + val-gate + 2-pass probes; same
   protocol as batches 1/2 (keys extractable from the re-audit
   `probe-worklist.csv` rows `serving_class=20421`).
3. Class 16757 batch 1 leftovers b021-b048 (28 keys, informational for cache
   completeness; cannot close the class): separate declaration if pursued.
4. b018 adoption decision: scrutiny owner (C++ second-implementation gate
   `cpp/solvers/kyouen_dfpn_root.cpp` pin `9193f5b6...` precedent); adoption
   consequences are pre-computed in the if-adopted analysis.
5. Kit mirrors (reset-proof): `/home/user/knowledge/kyouen-research/_19root-refresh-kit/`
   (batch16757/, batch23963/, batch23963-reaudit/, b018ifadopted/).

## Session continuation 2 (2026-11-22 ~03:13-03:30Z, same lane)

Environment was reset mid-session (work dir lost; kit mirrors survived and
were used to rebuild; node/curl/python3 present, git absent as before).
Re-fetched latest main at each step; all pushes went through
github_app.push_files with commit-pinned raw fetch-back byte verification.

### Batch 3 (class 20421, Part D) - WIN-HALT at d002

- val-gate 4/4 node-exact reproduced on the RESET host (at2m result 0 /
  2,000,000 x2; 15m result 2 / 3,651,923; result 2 / 5,040,200).
- d001 LOSS 879,510 nodes; d002 **WIN 5,359,994 nodes** (2-pass node-exact,
  s5 197253, key `[3461016313634230272, 131072]`, legal 73) -> pre-registered
  WIN-HALT; d003 LOSS 2,113,678; d004 LOSS 11,969,338. All 2-pass
  node-exact. Class 20421's all-LOSS closure route refuted; d005-d049
  unprobed; WIN unconsumed (scrutiny owner pending).
- Operator note: one stray runner invocation with a `--check` argument
  (treated as key id, exit 43, no solver run); spurious artifacts removed
  and disclosed in the batch README before publishing.
- Commits: `5bafed82` (scaffold + Part D, 62 files) -> `6e2a789f`
  (WIN-HALT raws d001-d004 + status + README).

### d002 IF-ADOPTED analysis (verdict NOT consumed)

- `research/experiments/n11-central-reply-20421-win-d002-ifadopted-20261122/`:
  canonical 5,924-row cache + 4-row batch-3 increment (3 LOSS + d002 WIN),
  published merger selftest PASS, conflicts 0 -> 5,928 rows
  (WIN159/LOSS5769), sha256 `f0bcbbc8...`; refresh script byte-copy with only
  the 2 cache pins changed; determinism 4/4; baseline control 119/119 holds.
- Deltas (machine-verified): exactly 4 classes flip excluded_now
  (23 -> 27): the s5-197253 cost-child holders 5255 / 5282 / 6030 / 20421;
  4 update8 groups flip win-hit (roots 12 and 37, all via 20421);
  remaining 31,838 -> 31,789 (root 12: -98, root 37: -98); resolved among
  baseline requirement 21 -> 25; groups_free_now 122 unchanged; free_now 33
  unchanged; per-root free-third coverage unchanged everywhere; worklist
  65,213 -> 65,209; joint greedy 35,617 -> 35,613.
- Commits: `596f3ae5` (multi-file) + `0ecdb829` (5,928-row if-adopted cache,
  single file).

### Batch 4 (class 16371, Part E) - WIN-HALT at e002

- First ranked closure class with no refutation evidence (16757: b018;
  20421: d002; 30345: holds b018's s5 528497). 50 keys e001-e050
  (root first=26/third=50 group), all absent from the canonical cache
  (0 hits), worklist-sourced, Board legal counts fixed 74..94.
- e001 LOSS 882,800 nodes; e002 **WIN 14,112,632 nodes** (2-pass node-exact,
  s5 183566, key `[1153765929805414400, 16]`, legal 79) -> WIN-HALT;
  e003-e050 unprobed; WIN unconsumed.
- Empirical note: 3 of 4 closure batches have now WIN-halted (16757: b018;
  20421: d002; 16371: e002); only 23963 closed 48/48 LOSS. The cheap end of
  the closure-classes ranking appears WIN-dense.
- Commits: `537e92de` (scaffold + Part E, 64 files) -> `8910e2c3`
  (WIN-HALT raws e001/e002 + status + README).

### e002 IF-ADOPTED analysis (verdict NOT consumed)

- `research/experiments/n11-central-reply-16371-win-e002-ifadopted-20261122/`:
  canonical 5,924 + 2-row batch-4 increment (e001 LOSS + e002 WIN) -> 5,926
  rows (WIN159/LOSS5767), sha256 `cd3ad8d7...`; determinism 4/4; baseline
  control holds.
- Deltas (machine-verified): exactly 4 classes flip excluded_now: the
  s5-183566 cost-child holders 4864 / 4903 / 5613 / 16371; **NO update8
  consequence** (16371 is not a frozen-plan selected class; neither e001
  nor e002 is in the 31,859 baseline requirement; remaining stays 31,838);
  free_now 33 unchanged, coverage unchanged, worklist 65,213 -> 65,211;
  joint greedy 35,617 -> 35,616; per-root greedy root 26 5,203 -> 5,202,
  root 48 2,822 -> 2,820.
- Commits: `ca175508` (multi-file) + `72c2fe96` (5,926-row if-adopted cache,
  single file).

### State on main after this continuation

- Canonical merged cache is UNCHANGED at 5,924 rows (sha `8a721a18...`);
  all six batch-3/4 verdicts (4 LOSS + 2 WIN) remain UNCONSUMED pending the
  scrutiny owner (3 WINs now: b018, d002, e002, all 2-pass node-exact from
  the pinned replica; C++ second-implementation gate precedent).
- free_now 33 / achieved coverage unchanged; no closure, coverage or root
  claim was made or consumed; standard 11x11 empty board, the 19
  central-reply roots and all classes remain UNKNOWN.
- Kit mirrors added: batch20421/ (complete incl. raws), d002ifadopted/,
  batch16371/, e002ifadopted/ (each with increment, merge-audit,
  refresh-summary, closure-classes, per-root-coverage, probe-worklist,
  scripts).
- Next runs: clean closure candidate = class 12264 (rank 5 re-audit
  closure-classes.csv, 51 unknown) via a new declaration (Part F); or
  scrutiny-owner consumption of the 3 pending WINs, which would formally
  exclude 16757/20421 (and 30345/15640/5255/5282/6030/4864/4903/5613/16371)
  and reshape the ranking.
