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

## Session continuation 3 (2026-11-22 ~03:30-03:45Z, same lane)

### Batch 5 (class 12264, Part F) - WIN-HALT at f017

- Closure ranks 1-4 all carried refutation evidence (b018/d002/e002
  unconsumed WINs; 30345 holds b018's cost child), so batch 5 pivoted to
  rank 5: class 12264 (mask `[1152921504606848033, 0]`, 51 unknown, groups
  incl. root 0/third 5). 51 keys f001-f051, all absent from the canonical
  cache (0 hits).
- f001-f016 LOSS (chunk-published: `372b1dd6`, `33b6d26d`), then **f017 WIN
  3,522,635 nodes** (2-pass node-exact, s5 415095, key
  `[1188950301625810945, 70368744177666]`, legal 82) -> WIN-HALT
  (`cfe8605d`); f018 LOSS published as in-flight completion. 18/51 probed,
  f019-f051 unprobed, WIN unconsumed.
- Empirical: 4 of 5 closure batches WIN-halted (16757/20421/16371/12264);
  only 23963 closed. Measure: the cheap (low-unknown) end of the closure
  ranking is WIN-dense; candidate scoring should be revisited (scheduling
  quantity only, never a verdict).

### f017 IF-ADOPTED analysis (verdict NOT consumed)

- `research/experiments/n11-central-reply-12264-win-f017-ifadopted-20261122/`:
  canonical 5,924 + 18 batch-5 rows (17 LOSS + f017 WIN) -> 5,942 rows
  (WIN159/LOSS5783), sha256 `f7c7c960...`; determinism 4/4; baseline
  control holds.
- Deltas (machine-verified): exactly 3 classes flip excluded_now (the
  s5-415095 cost-child holders 12264 / 12327 / 14776); 6 update8 groups
  flip win-hit via frozen-plan-selected class 12264 (roots 0 and 5, thirds
  5/10/55/110/0); resolved among baseline requirement 21 -> 39 (all 18
  batch-5 keys inside the 31,859 baseline requirement - largest single
  adoption delta so far); remaining 31,838 -> 31,787 (root 0 -204, root 5
  -102); free_now 33 unchanged, coverage unchanged; **joint greedy RISES
  35,617 -> 36,989** - first measured adoption that makes the joint plan
  more expensive (roots 0/5 lose their cheap option).
- Commits: `bef0aa4a` (multi-file) + `7f11bf7a` (5,942-row if-adopted cache,
  single file).

### Final state of this session (all three continuations)

- Canonical merged cache UNCHANGED: 5,924 rows (sha `8a721a18...`).
- Unconsumed verdicts awaiting the scrutiny owner: 4 WINs (b018, d002, e002,
  f017) + 22 two-pass LOSS rows (batch3: 3, batch4: 1, batch5: 18 minus...
  precisely: d001/d003/d004, e001, f001-f016+f018 = 21 LOSS rows total).
  All 2-pass node-exact from the pinned jsreplay replica at 15M.
- No closure/coverage/root claim made or consumed this session; free_now 33
  and achieved coverage unchanged; standard 11x11 empty board, the 19
  central-reply roots and all classes remain UNKNOWN.
- Kit mirrors added this continuation: batch12264/, f017ifadopted/.
- Recommended next: scrutiny-owner consumption of the 4 pending WINs (the
  IF-ADOPTED packets are complete for all four), THEN re-run the refresh
  re-audit for a new canonical ranking; further probe batches on blind
  ranking are empirically likely to WIN-HALT early.

## Session continuation 4 (2026-11-22, same lane)

### Part G: third-implementation cross-verification of the closure WINs - ALL AGREE

- Declared as Part G of the single-owner note; experiment
  `research/experiments/n11-centralreply-closure-wins-thirdimpl-reverify-20261122/`
  (scaffold `480238ae`, 27 files; the C++ gate remains impossible in this
  environment - still no compiler, package installation still forbidden).
- The third implementation (pinned `third_impl.js` sha256 `08ea958f...`,
  non-df-pn AND/OR minimax) independently re-derived, verdict-level:
  - **all 4 unconsumed closure WINs agree**: b018 WIN (3,972,982 expansions),
    d002 WIN (6,144,044), e002 WIN (16,384,711), f017 WIN (4,038,798); each
    2-run a/b identical (result, expansion, ttHits), all `clean`.
  - **10/10 stratified LOSS spot rows agree** (d001/d003/d004/e001/f001/
    f005/f009/f013/f016/f018): all result 2, a/b identical.
- This-host anchor reproduction: k02 WIN 9,106,337 expansions / 4,991,527
  ttHits; l1 LOSS 7,660,602 / 3,951,175 - exactly the published third-impl
  values. Rules gate: quads 95,670 == replica, 195,044 triples TBL==wob
  0 mismatches. Negative gates ng1/ng2 GATE_FAIL with published messages.
- `scripts/audit.py` fail-closed: **171/171 gates PASS**, run twice
  byte-identical; MANIFEST.sha256 over 63 published files.
- Operator erratum (disclosed in the experiment README): the first runner
  version looked `--lo/--hi` up from `rows.json` inside Node, and
  JSON.parse -> Number -> String silently rounded k02's 121-bit key
  (`...1424` passed as `...1400`, popcount 5 -> 20). The pinned driver's
  fail-closed stone-count gate caught it before any search ran; no target
  or anchor row was ever produced by the buggy runner. Fixed by passing
  lo/hi/legal/stones from the machine-derived input CSV strings (exact
  integer tokens), and audit gate G0 now asserts every input CSV equals
  its rows.json row in exact Python integers.
- Status: verdicts NOT consumed (adoption stays with the scrutiny owner;
  the C++ second-implementation gate precedent is unchanged and this
  third-impl agreement is additional strengthening evidence only). The
  canonical merged cache is unchanged at 5,924 rows; free_now 33 unchanged;
  11x11 empty board, the 19 central-reply roots and all classes remain
  UNKNOWN; expansions/nodes are not verdicts.
- Recommended next: scrutiny-owner consumption decision for the 4 pending
  WINs (now corroborated by two independent implementations), then the
  refresh re-audit for a new canonical ranking; remaining unprobed keys
  of refuted classes (b021-b048, d005-d049, e003-e050, f019-f051) are
  cache-completion only, never closure evidence.

### Part G addendum: full unconsumed-packet coverage - 25/25 rows agree

- The LOSS spot sample was extended (pre-registered addendum) from 10
  stratified rows to all 21 unconsumed LOSS rows; the remaining 11
  (f002/f003/f004/f006/f007/f008/f010/f011/f012/f014/f015) all agree
  verdict-level (result 2, clean, 2-run deterministic pairs;
  expansions 2,031,528..7,653,660).
- `scripts/audit.py` now **281/281 gates PASS** (run twice byte-identical);
  verdict agreements **4/4 WIN + 21/21 LOSS, 0 divergences,
  0 wall-inconclusive**. The entire unconsumed closure-lane packet is
  corroborated verdict-level by the second (non-df-pn) implementation.
- Verdicts still NOT consumed; scrutiny owner / C++ gate unchanged;
  11x11 empty board, 19 central-reply roots, all classes remain UNKNOWN.

### Continuation 5 (2026-11-22): Part H - joint 4-WIN if-adopted analysis published; additivity machine-gated

- Built and published the joint scenario for the unconsumed 25-row packet
  (4 WIN + 21 LOSS) on top of the canonical 5,924-row cache: 5,949 rows,
  WIN 162 / LOSS 5,787, 0 conflicts, merged sha256 `88ef4388...`
  (pushed as its own single-file commit; analysis-only, NOT canonical).
- Dynamism gates all green: merge selftest PASS, refresh 2-run
  byte-identical, root {60,27} baseline 119/119 free thirds, pinned
  inputs unchanged (Board `954d3a10...`, policy `78655e94...`,
  quarantine `81d23160...`).
- `compare_joint_deltas.py` gates: joint delta == sum of the four single
  deltas on all 11 metrics (0 failures); win-hit class set joint == union
  ({12264, 16757, 20421}); per-root free coverage identical to baseline.
- Joint-scenario numbers (if adopted): excluded_now 23->37, update8
  remaining 31,838->31,709 (additive -29-49-51+0), win-hit 15 groups,
  joint greedy 35,617->36,984 (+1,367; five cheaper than f017-alone
  +1,372), free_now 33 unchanged, probe worklist 65,213->65,183.
- Decision-relevant planning fact: the joint adoption makes the frozen
  19root plan HARDER at the scheduling level (f017's flip of roots 0/5
  dominates); and under joint adoption the closure ranking's cheap end is
  exhausted by the refuted quartet - the first clean candidate is rank 6
  class 5473 (`1158058422931816448:0`, unknown 51).
- Verdicts NOT consumed; canonical cache unchanged at 5,924 rows;
  free_now 33 unchanged; 11x11 empty board, the 19 central-reply roots and
  all classes remain UNKNOWN; expansions/nodes are not verdicts.

- Addendum to Continuation 5 (same session, before any further lane work):
  the P24/decomposition runs RETRACT the mechanism attribution in the
  Part H headline above. Measured decomposition (all read-only, verdicts
  NOT consumed, all runs 2-run byte-identical, root {60,27} 119/119):
  adopting the 4 WINs alone is plan-cost NEUTRAL (greedy -1) and delivers
  the full WIN-side effects (excluded 37, unknown 34,489, update8 remaining
  31,709 = -129, win-hit 15 groups); the 17 batch12264 f-LOSS rows alone
  drive greedy +1,372; the packet-minus-f017 scenario (P24) has the SAME
  greedy 36,984 as the full packet; per-root free coverage never changed
  in any scenario. Additivity P4+P21==P25 holds on 8 of 9 metrics (the
  exception, update8 remaining, has a machine-verified subsumption overlap
  of exactly 20). Consequence: the WIN-adoption decision is separable from
  the +1,367 plan cost, which attaches to the f-LOSS completions. The joint
  experiment README now carries an ERRATUM section; two new experiments are
  published (packet-minus-f017 P24; WIN-vs-LOSS decomposition P4/P17/P21)
  alongside their 4 analysis-only merged caches (own commits).

## Session continuation 5 (2026-11-22 ~04:29-05:10Z, same lane; batch 6 class 5473 + joint 5-WIN if-adopted + REPO OUTAGE)

- **Batch 6 (class 5473, re-audit rank 6**, first clean candidate per Part
  H-bis): scaffold + Part I amendment pushed as `09f24c62` (64 files). A
  g001-g010 raw + status commit was created (`729be22c`, 04:45:56Z), but -
  discovered after the outage ended - **it never reached main** (dangling
  commit; the mid-outage ref update failed silently). All 18 rows were
  re-published post-recovery in a single commit (see continuation 6). Fail-safe before declaring: re-audit
  probe-worklist regenerated on this host from pinned inputs
  (byte-identical incl. closure-classes/per-root-coverage/refresh-summary),
  51/51 keys absent from canonical cache (5,924 rows, sha `8a721a18...`),
  quarantine pair check 0, val-gate 4/4 node-exact (this host 17s/26s at the
  two 15M rows).
- **g001-g018: 17 LOSS then g018 (s5_index 184684, key
  `[1734519175235239936, 0]`, legal 78) result 1 WIN, 5,936,863 nodes,
  2-pass node-exact -> pre-registered WIN-HALT at 18/51 (rc=45). Verdict
  NOT consumed (scrutiny owner pending, as b018/d002/e002/f017). Class
  5473's all-children-LOSS closure route is refuted; the cheap-end
  WIN-density observation now extends to rank 6 (5 of 6 batches halted).**
- **IF-ADOPTED decomposition (Part H-bis methodology applied to batch 6)**:
  `n11-central-reply-class5473-win-g018-ifadopted-20261122/` - increments
  fail-closed from raws (18 rows/1 WIN/17 LOSS), merges conflict-free
  (5,925 `3e77daae...` / 5,941 `d97a307e...` / 5,942 `b839abfc...`),
  per-scenario refresh 2/2 byte-identical, compare script + delta JSON.
  Measured: WIN-only adoption gives excluded 23->27 (classes 4889/4892/5473/
  5501 via s5 184684), update8 remaining 31,838->31,787 (root 26 -102,
  root 49 -102), win-hit 4 groups via class 5473, and **joint greedy
  UNCHANGED at 35,617 in every batch-6 scenario (WIN-only, LOSS-only,
  full)** - unlike the f-batch, batch 6 is planning-cost neutral. LOSS rows
  only add resolved (+17, additive with WIN-side +1 to +18) and worklist
  (-20 additive).
- **Joint 5-WIN IF-ADOPTED**: `n11-central-reply-joint-5win-adoption-ifadopted-20261122/`
  (PJ5WIN = canonical + 4-WIN increment + g018 WIN-only; PJ5FULL = P25
  packet cache + batch-6 18 rows). Merges conflict-free (5,929 `653dfb07...`
  / 5,967 `a31e093b...`), refresh 2/2 byte-identical each. Measured:
  5 WINs alone: excluded 23->41 (+18 = +14 +4 additive), remaining
  31,838->31,658 (-180 = -129 -51 additive), win-hit 19 groups
  (16757:5, 20421:4, 12264:6, 5473:4), greedy 35,616 (-1, neutral).
  43-row full adoption: greedy exactly the Part-H packet value 36,984
  (+1,367) with **zero additional increase from batch-6 rows** - Part H-bis
  attribution (f-batch LOSS completeness drives the increase) holds in the
  joint setting. worklist 65,163 (-50 additive).
- **REPO OUTAGE (publish-pending)**: at ~04:52Z, mid WIN-HALT publish,
  `api.github.com/repos/yuubnnkyoku/kyouen-researches` started returning
  404 for BOTH unauth API and the github_app connector; raw CDN had served
  cached content until ~04:53Z and then 404ed for new fetches too. The
  WIN-HALT commit payload (all 36 raws g001-g018 + status.log + README with
  WIN-HALT section) and both if-adopted experiments (READMEs, scripts,
  increments, audit JSONs, scenario caches, delta JSONs, session log) are
  staged byte-exact in the lane kit (`batch5473/`, `batch5473-ifadopted/`,
  `batch5473-ifadopted-joint5/`, `doc/`) for publish-when-reachable. A
  parallel SAT-stabilization lane's commits (K1220/K1221 errata, last known
  HEAD `d73bb0b8` 04:51:31Z) were the last observed main movements; no path
  conflicts with this lane's pending payloads.
- Honesty record: budget exhaustion never occurred; no verdict consumed; the
  standard 11x11 empty board, all 19 central-reply roots, and every S4
  class remain UNKNOWN. Nodes/budgets/gates are never verdicts.

## Session continuation 6 (2026-11-22 ~05:10-05:5xZ, same lane; repo recovery, full pending-publish clearance, batch-6 third-impl completed)

- **Repo recovery + lost-commit discovery**: the repo became reachable again
  via the github_app connector (unauth API rate-limited 403; connector fine).
  Current main had moved to `c37c8527` (two other-lane commits during/after
  the outage: `4fcee8eb` sweep-resume declaration, `c37c8527` six-row lane
  note; no path conflicts). Path-filtered history for the batch-6 experiment
  dir showed ONLY `09f24c62`: the believed-pushed `729be22c` (raws g001-g010
  + status, created 04:45:56Z) **never reached main** - a dangling commit
  object. Corrected session-log narrative in continuation 5 before
  publishing it (continuation 5 had never been published, so this is not a
  history rewrite).
- **WIN-HALT publication (retry, complete)**: one commit `9fe53799` with all
  38 files (36 raws g001-g018 + status.log + README WIN-HALT section),
  message records observed HEAD-before-push `c37c8527` and supersedes the
  dangling `729be22c`. Fetch-back: 38/38 byte-identical (raw URLs, fresh
  paths; status.log + README verified separately due to subshell accounting).
- **If-adopted decomposition published** `2785f837` (32 files, three
  worklists excluded per policy) + **transport-truncation incident and fix**:
  the file-read transport silently caps at ~64KB, so the first push carried
  truncated (63,961-63,964B) copies of the three ~243KB merged scenario
  caches. Detected by fetch-back diff (same failure mode as the SAT lane's
  b64 errata earlier). Fix commit `e940c118`: chunked reads, full 3 caches
  restored (pwing018 5,925 rows `3e77daae...`, pgloss17 5,941 `d97a307e...`,
  pfull18 5,942 `b839abfc...`); verified byte-identical via the
  commit-pinned API resource (raw CDN still served the stale blob at
  check time - raw caching must be accounted for when verifying modified
  files).
- **Joint 5-WIN if-adopted published** `ffca24d5` (23 files + single-owner
  note Part J amendment). Part J covers both if-adopted scopes (batch-6
  decomposition + joint 5-WIN). Fetch-back: 23/23 + note byte-identical.
- **Batch-6 third-impl cross-verification COMPLETED** (Part G re-application,
  recorded as note amendment **Part K**): targets g018/g001/g011/g016
  a/b pairs all clean (g018 WIN 6,776,591 expansions - verdict agrees with
  the replica WIN 5,936,863 nodes; g001/g011/g016 LOSS
  4,143,095/9,926,469/1,690,556 agree), anchors k02a (WIN 9,106,337/4,991,527,
  27s) and l1a (LOSS 7,660,602/3,951,175, 23s) node-exact vs published
  third-impl values a/b, negatives ng1/ng2 GATE_FAIL with published messages,
  rules-gate quads 95,670 / triples 195,044 mismatch 0 carried. Audit:
  **71/71 gates PASS, run twice byte-identical**, 0 wall-inconclusive.
  Verdict-level corroboration only - NOT adoption; scrutiny owner and the
  C++ gate (`9193f5b6...`) unchanged; verdicts remain unconsumed.
- Honesty record: no verdict consumed anywhere; the standard 11x11 empty
  board, all 19 central-reply roots, and every S4 class remain UNKNOWN.
  Nodes/expansions/budgets/gates are never verdicts. Part K is appended
  post-completion for scope recording (disclosed in the amendment itself).

## Session continuation 7 (2026-11-22 ~05:35-06:1xZ, same lane; execution-environment reset mid-batch, parallel-run collision handled, batch 7 COMPLETE 51/51 all-LOSS, class 10324 CLOSED free via re-audit)

- **Environment reset mid-batch**: at ~05:35Z the remote execution environment
  reset (work dir wiped, no solver state lost besides staging), right after a
  concurrent instance of this same hourly lane had stashed h001-h019 raws to
  the kit (`batch10324/`) with status rows timestamped 05:23:12-05:35:18Z.
  Duplicate executions of h001-h010 by both instances produced identical
  (result, nodes, legal) rows - an unplanned 2-host determinism cross-check.
- **Batch 7 resumed and COMPLETED**: after rebuilding from the kit stash and
  re-fetching the pinned inputs (shas verified), h020-h051 ran to completion:
  **51/51 keys 2-pass node-exact LOSS at 15M, NO WIN-HALT, no mismatch, no
  exhaustion** - the first batch since batch 2 (class 23963) without a WIN
  stop. Cumulative 203,517,761 nodes. Checkpoint pushes: h011-h019
  (`209a0479`, with a batch-keys metadata erratum: per-row
  membership_class_count from the worklist rows), h020-h030 (`72fe8613`),
  h031-h042 (`fdff5c4e`), final h043-h051 + README (`ac2ff9ae`).
- **Class 10324 closure re-audit PASSED**: fail-closed increment (51 rows
  `39b975e8...`) + published `s5_union_merge.py` (selftest PASS) merge into
  canonical 5,924 (`8a721a18...`) -> **5,975 rows `a998f4c0...`** (WIN 158 /
  LOSS 5,817, 0 conflicts) + published `refresh_19root_frontier.py`
  (byte-copy, only the 2 cache-pin lines changed, all 6 pinned inputs
  sha-verified, 2-run byte-identical). **Class 10324 is certified as the
  34th Board-verified free class** (`free_now` 33->34, board verification
  34/34 with 0 rejected, `unknown` 34,503->34,502). Root third coverage
  244->248 (root 14: 6->8, root 16: 10->12). update8 `remaining_now`
  31,838->31,836 with 2 newly-resolved baseline requirements (batch-7 h043
  s5 362082, h051 s5 362090). Joint greedy 35,617->35,857 (+240, LOSS-side
  option-pool effect, f-batch direction). Worklist 65,213->65,155. Closure
  ranking: 10324 gone entirely; next clean candidate rank 7 class 2634
  (`[4035225266258182144, 0]`, 51 unknown).
- Honesty record: only the 51 batch-7 LOSS rows were consumed; the six
  unconsumed WINs (b018/d002/e002/f017/g018) stay scrutiny-owner-pending;
  no verdict was created or asserted; **the standard 11x11 empty board and
  the 19 central-reply roots remain UNKNOWN.** Nodes/expansions are never
  verdicts.

## Session continuation 8 (2026-11-22 ~06:1xZ onward, same lane; d315e38c fetch-back verified, batch 8 declared for class 2634)

- First action of this continuation was the unfinished verification from the
  previous run: fetch-back of commit `d315e38c` (9 experiment files + note +
  session log, plus the canonical merged cache) — **11/11 byte-identical**
  (canonical cache 5,975 rows / 244,860 bytes / sha256 `a998f4c0...`
  confirmed on the remote). The Part M re-audit kit stash `reaudit10324/` was
  added to the lane kit. Main HEAD at start: `d315e38c` (no new lane-external
  commits; an m35 SAT-lane instance had committed `db663914`/`85386533`/
  `986ab607` before `6577a3f3`, all observed and non-colliding).
- **Batch 8 declared for class 2634** (Part N amendment of the single-owner
  note; experiment `n11-centralreply-closure-class2634-batch8-20261122/`):
  the Part M rank-7 next clean candidate, 51 keys h001-h051 (probe_order
  281-331 of the 65,155-row regenerated worklist, sha256 `ca3ee3bc...`;
  all 51 rows published via batch-keys.json). Fail-safes before declaring:
  51/51 keys absent from the canonical 5,975-row cache (`a998f4c0...`);
  quarantine (`81d23160...`) key cross-check 0 hits both directions
  (including distinct hi=128 member 10448914085452972032:128 vs quarantined
  10448351135499552764:128); no same-scope declaration on main (checked
  content listing + HEAD). Pinned solver `jsreplay.js` `845856173d...`
  byte-identical to batches 1-7; val-gate 4/4 node-exact on this host before
  the first row (at2m 0/2,000,000 twice; 15m 2/3,651,923 and 2/5,040,200).
- **Erratum published**: the batch-7 README fail-safe line claimed the
  quarantine registry had "4 active entries"; the pinned registry
  (`81d23160...`) contains exactly 2 active entries. Corrected in-repo in the
  batch-7 README with an erratum marker; conclusion (0 hits) unaffected.
- Honesty record: nothing consumed by the declaration; **the standard 11x11
  empty board, the 19 central-reply roots and class 2634 remain UNKNOWN.**

## Session continuation 9 (2026-11-22 ~06:58-07:10Z, same lane; parallel batch-8 instance left untouched, outstanding Part-O third-impl verified and published)

- Context: this session started with the shared lane kit showing an active
  parallel instance of this hourly lane mid-batch-8 (class 2634, Part N
  declared at `fdc46d98`, i001-i025 probed by 06:54Z per the kit status
  mirror, incl. one 15M-budget exhaustion row). Nothing in the batch-8
  scope was touched - the Part N single-owner declaration covers it.
- The one remaining unpublished product from the repo-404 outage window was
  identified and closed: the batch-7 third-implementation
  cross-verification (outage-session kit lettering "Part M", declared with
  timestamp 2026-11-22T05:58Z, staged in the lane kit). Repo lettering
  check: the recovery session had already issued Part M for the class-10324
  closure merge + re-audit and Part N for batch 8, so the experiment ships
  as **Part O** with the mapping disclosed in the experiment README and
  the note amendment.
- Publishing-session pre-verification (machine checks, all PASS): MANIFEST
  174/174 OK; pinned script bytes (`third_impl.js` `08ea958f...`,
  `verify_tbl.js` `c8c52528...`, `jsreplay.js` `84585617...`) match the
  published experiments; input rows.json replica (result, nodes) match the
  published batch-7 status.log 51/51, keys (lo:hi) match batch-keys.json
  51/51; audit-summary all_pass=true (541 gates, 51/51 LOSS verdict
  agreements vs published replica verdicts, 0 divergences, 0
  wall-inconclusive), anchors k02/l1 exactly reproduced (9,106,337 /
  4,991,527 and 7,660,602 / 3,951,175), negative gates GATE_FAIL with the
  published messages.
- Publishes: `eb061b60` (scaffold 66 files), `0dfdc4df` (102 target a/b
  raws), `0fddb890` (anchors + negative + audit-summary),
  `d548489f` (note Part O amendment). Fetch-back: 175 experiment files +
  the note compared against commit-pinned raw URLs byte-for-byte
  (`cmp`), 0 mismatches.
- Net effect: the published class-10324 (34th Board-verified free class)
  evidence bundle is now cross-implementation verified end-to-end - 51
  replica 2-pass LOSS rows + 51 third-implementation verdict agreements,
  fail-closed audited. Batch-7's sibling batches 2/6 third-impl coverage
  (23963: Part C-era; batch-6: Part K) is unchanged.
- Operational notes: the lightweight pre-upgrade sandbox `sha256sum` shim
  is broken (returns digest errors) - manifest rechecks were redone in the
  upgraded environment and the earlier "174 OK" provisional result was
  confirmed. `file_system.read_file` chunked transport caps near 24K
  chars per call and reports chars, not bytes (use `wc -m` for UTF-8
  payload size assertion; byte counts only for pure-ASCII payloads).
- Honesty record: verdicts not consumed anywhere; the standard 11x11 empty
  board, the 19 central-reply roots, class 2634 and every closure class
  remain UNKNOWN. Nodes/expansions are never verdicts.
- Addendum (post-continuation-9 check, same session, ~07:1xZ): an
  independent post-publication audit of the class-10324 consumption chain
  was run from the published bytes only: (1) the published merged cache
  (5,975 rows) refetches with sha256 exactly `a998f4c0...` (the note Part M
  pin) and is byte-identical to the lane kit mirror; (2) sorted row sets
  show merged == canonical 5,924 (sha256 `8a721a18...`, refetched from
  main, pin-verified) UNION batch-7 increment 51, zero duplicate rows,
  zero key collisions (the WIN/LOSS conflict gate is structurally
  confirmed: increment and canonical are disjoint); (3) verdict counts
  WIN 158 / LOSS 5,817, exactly as Part M published; (4) all 51 increment
  rows match the published batch-7 status.log on (nodes, verdict) through
  the published batch-keys.json lo:hi mapping, 51/51, 0 mismatches.
  Read-only audit, no new claim, no verdict consumed; the standard 11x11
  empty board, the 19 central-reply roots and all closure classes remain
  UNKNOWN.

## Session continuation 9 addendum (2026-11-22 ~07:10-07:3xZ, same lane; Part P executed and published, class-23963 consumed evidence bundle cross-verified by the third implementation)

Part P, pre-registered at `03c8e0fa`: third-implementation reverify of the 48
consumed rows (c001-c048, all LOSS, 2-pass node-exact) of batch 2 /
class 23963, the first free class closed by Board verification. Same protocol
and gates as Parts G/K/O; verdict not consumed; post-hoc corroboration
literature only.

- Execution (paired a/b runs, one row per process, cap 300M expansions,
  wallcap 240s): all 48 rows byte-identical across the two runs; third-impl
  expansions 636,315-4,341,425 (replica df-pn nodes 579,880-3,815,424);
  anchors k02a (WIN 9,106,337 / 4,991,527 ttHits) and l1a (LOSS 7,660,602 /
  3,951,175 ttHits) node-exact vs the published third-impl values; negative
  gates ng1/ng2 GATE_FAIL with matching wording; `audit.py` (fail-closed, run
  twice byte-identical): **511/511 gates PASS, 48/48 LOSS verdict agreement,
  0 divergence, 0 wall-inconclusive**.
- Publication commits: `a84f8254` (scaffold 63 files) -> `cb739fcd` (targets
  96 files) -> `dbd7c5c2` (anchors 4 + negative 2 + audit-summary.json) ->
  note publication amendment `c89bce19`. Fetch-back: all 166 experiment files
  byte-identical against their pinned commits (raw URL + cmp), note amendment
  byte-identical as well.
- Sources: the 96 published batch-2 raws were re-fetched from main and
  machine-verified byte-identical (96/96) before use; batch-keys.json
  (sha256 `3b37c923...`) deliberately not re-published, documented in the
  experiment README.
- Parallel lanes: the finite-field cleanup lane landed
  e86a4373/f996c16b/2aeb33d0 during execution. Post-hoc recheck confirms all
  Part O experiment files (README, audit-summary, rows.json) remain
  byte-identical on main against the kit mirror; no path collision with this
  lane. The parallel batch-8 instance (class 2634, Part N scope) was not
  touched; its i002 15M-budget depletion row belongs to that lane's scope.
- No verdict consumed, no claim changes: the standard 11x11 empty board, the
  19 central-reply roots and all closure classes remain UNKNOWN;
  nodes/expansions are not read as outcomes.

## Session continuation 9 addendum 2 (2026-11-22 ~07:4xZ, same lane; read-only post-publication independent chain audit of the class-23963 consumption evidence)

Independently audited the full published evidence chain for class 23963
(batch 2, the first free class closed by Board verification), from freshly
fetched published bytes only (no lane-staged file trusted):

- Method: `chain_audit_23963.py` (sha256 `fef60288...`, fail-closed, stdlib
  only; run twice, byte-identical output) over: the published batch-2 raws
  (96 files re-fetched from main), the published batch-2 status.log (48
  rows), the kit batch-keys.json (sha256 `3b37c923...` re-checked), the
  published Part P `input/rows.json` and `output/audit-summary.json`, and the
  published canonical merged cache (5,975 rows, sha256
  `a998f4c0b13383cb50bbbdb60761182722ba45280fd585739ad5d08bc182ed1b` -
  the full pin from the note Part M record).
- Result: **ALL PASS - 13,521 independent machine gates.** Specifically:
  (1) raws: 48/48 keys 2-pass node-exact LOSS at the 15M budget
  (replica df-pn nodes 579,880-3,815,424), keys unique; (2) published
  status.log: 48/48 (result, nodes) identical to the raws; (3) batch-keys
  identity: 48/48 key (lo, hi) and legal match the raws; (4) Part P input
  rows.json: 48/48 replica (result, nodes) equal the published batch-2
  values, all expect_third LOSS; anchors k02a/l1a and negatives ng1/ng2 rows
  present with the pinned geometry; (5) Part P audit-summary (published): 511
  published gates all PASS on refetch, verdict agreements 48/48
  third-impl LOSS == replica LOSS, anchor node-exact details 9,106,337/4,991,527
  and 7,660,602/3,951,175, negatives GATE_FAIL, 0 wall-inconclusive; (6)
  canonical cache consumption intact: all 48 batch-2 keys present **exactly
  once**, each verdict LOSS with nodes byte-consistent with the raws, cache
  totals WIN 158 / LOSS 5,817.
- Read-only audit; no verdict consumed, no claim change; the script and both
  run logs are staged in the lane kit (`batch23963-thirdimpl-reverify/chainaudit/`)
  for reproducibility. The standard 11x11 empty board, the 19 central-reply
  roots and all closure classes remain UNKNOWN; nodes/expansions are not read
  as outcomes.
