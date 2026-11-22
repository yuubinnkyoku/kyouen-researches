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

## Session continuation 9 addendum 3 (2026-11-22 ~07:4x-08:0xZ, same lane; repo-wide integrity scan of the kit-pinned experiment mirrors after the cleanup lane, plus batch-7 chain recheck)

Read-only integrity scan of all five kit manifests (678 manifest entries)
against main HEAD, fail-closed (scanner `intscan.py`, kit
`intscan-20261122/`), followed by repo-internal chain rechecks where kit and
repo diverged:

- CLEAN: Part G mirror 96/96, Part O mirror 174/174, Part P mirror 165/165
  manifest entries byte-identical on main. The cleanup lane removed nothing of
  this lane's published evidence.
- Two STALE staging mirrors classified (repo authoritative, no damage):
  `batch5473-thirdimpl-reverify` (outage-era planned 211-gate scope
  superseded by the published 71-gate
  `n11-centralreply-closure-batch6-g018-thirdimpl-20261122` - 43 absent files
  are unpublished planned scope, 17 diffs are wall-time-only with identical
  expansions/ttHits) and `batch10324` (pre-resume staging; repo final raws
  differ only in `wall_s` and, on a few keys, which pass is labeled p1 vs p2).
- Repo-internal chain rechecks (fail-closed, published bytes only):
  (1) batch-7 51 keys: raws 2-pass node-exact LOSS, (result, nodes) ==
  status.log == merged canonical cache consumption, 51/51 (`b7_chain_check`,
  ALL PASS); (2) Part K published audit refetch: 71/71 gates PASS,
  g001/g011/g016 LOSS + g018 WIN third-impl agreement 4/4, anchors node-exact
  9,106,337/4,991,527 and 7,660,602/3,951,175, 0 wall-inconclusive.
- Operating rule recorded in the lane kit: the two stale manifests must not be
  used as repo pins; `doc/integrity-scan-20261122.md` classifies all five
  mirrors. Scanner lesson (own bug, caught by the empty-file sha `e3b0c442`
  appearing as a "mismatch"): parallel file fetches must not share one temp
  output file; fixed in the scanner before any conclusion was drawn.
- Read-only audit; no verdict consumed, no claim change; the standard 11x11
  empty board, the 19 central-reply roots and all closure classes remain
  UNKNOWN; nodes/expansions are not read as outcomes.

## Session continuation 10 (2026-11-22 ~08:4xZ, same lane; Part S retraction record + Part T batch-9 j033 third-impl cross-verification: run, publication, note status update; concurrent Part U batch-8 takeover observed)

- Part S (start of this run): the transport/blob-corruption concern on the
  merged cache raised at the end of continuation 9 was RETRACTED after full
  fetch-back (32/32 manifest entries byte-identical); the damage was a local
  workspace reset artifact, the repo authoritative copy undamaged; published
  as note Part S amendment (`3bc1a7bf`). Operating rule: blob-corruption
  claims stay provisional until kit-mirror and repo copies both disagree.
- Part T: single-owner declaration `4e725538` (note blob `f0ea354d...`), then
  the batch-9 (class 1518) j033 third-implementation cross-verification was run
  and published, exactly as declared (verdict-neutral evidence work):
  - Runs: 16 processes (targets j033/j001/j016/j027 a/b + anchors k02a/l1a
    a/b + negatives ng1/ng2), all clean, a/b identical. j033 WIN agreement
    (third-impl 5,392,392 expansions vs replica df-pn 4,718,280 nodes); LOSS
    spots j001 9,103,477 / j016 10,556,205 / j027 1,401,488 expansions.
    Anchors k02a WIN 9,106,337/4,991,527 and l1a LOSS 7,660,602/3,951,175
    node-exact vs published third-impl values. Rules gate quads 95,670 /
    triples 195,044, mismatch 0; negatives GATE_FAIL on wording, as required.
  - Fail-closed inputs derived by `make_inputs_batch9.py` (batch-2 script
    adapted; batch-9 batch-keys lo/hi are strings, so int-compare was
    required) from the published batch-9 authoritative commit `a321bfb2`
    (raws 8, batch-keys.json `8f2035d1...`, status.log PASS rows), repo
    fetch vs kit mirror 10/10 byte-identical.
  - `audit.py` (batch-9 adaptation, schema/EXP names only): 71/71 gates
    PASS, 2 runs byte-identical, divergence 0, wall-inconclusive 0.
  - Publication: three commits `1ebf75e1` (scaffold 16; pinned scripts 4
    byte-identical to the published Part P experiment) -> `c98ad197`
    (targets 8) -> `eae66b36` (anchors 4 + negatives 2 + rules-gate +
    status.log + audit-summary.json + MANIFEST); experiment dir
    `n11-centralreply-closure-batch9-j033-thirdimpl-20261122` (34 files);
    fetch-back 34/34 byte-identical (commit-pinned raw URLs + sha256sum).
- Note status update `180d85fb` (note blob `4c721238...`, byte-precomputed,
  42,039 chars): the first push attempt failed its note guard and detected a
  concurrent Part U (batch-8 takeover declaration, observed HEAD `9f06b2b2`,
  note blob `a2081397...`); the batch-8 declaring host reportedly vanished
  just before i026 p2, takeover continues h026-h051. Scope disjoint from Part
  T (batch-9-derived keys only; zero contact with batch-8 files); recorded
  in the appendix and re-pushed successfully.
- State: no verdict consumed anywhere. j033 WIN is the sixth unconsumed
  closure WIN (b018/d002/e002/f017/g018/j033), all third-impl corroborated,
  awaiting the scrutiny owner (C++ second-implementation gate pin
  `9193f5b6...`, unchanged). batch-9 remaining keys j034-j051 (18) not
  started; check latest main for Part V-type declarations before touching
  them. 11x11 baseline unchanged (merged cache 5,975 rows `a998f4c0...`,
  excluded 23 / free 34 / unknown 34,502 / remaining 31,836 / greedy 35,857 /
  worklist 65,155). The standard 11x11 empty board, the 19 central-reply
  roots and classes 1518/2634 all remain UNKNOWN; nodes/expansions are not
  read as outcomes.
- Analysis-lane kit mirror: `_19root-refresh-kit/batch9j033-thirdimpl/`
  (47 files incl. repo-unpublished audit-run1/2.txt and sources/;
  MANIFEST 33/33 OK). Observed HEAD-before-push for this log update is
  recorded in the commit message.

## Session continuation 11 (2026-11-22, verifier): batch-8 takeover completion (Part U) + Part V h045 if-adopted decomposition

- Batch-8 takeover (declared note Part U, `37757217`) completed and
  published by the takeover host: chunk 1 `a6fd2c48` (declaring-host rows
  h001-h025 renamed i->h from the kit mirror, rescue-declaring-host/,
  takeover val-gate + cross-check + status.log, 59/59), chunk 2
  `27d3b46f` (h026-h039 fresh cold 2-pass all node-exact LOSS at 15M,
  29/29), WIN-HALT chunk `1f127fb8` (h040-h045 raws: 43 LOSS + h002
  exhaustion UNKNOWN + h045 WIN at s5 103558, `[4035225266258182144,64]`,
  nodes 6,366,900, 2-pass node-exact; total batches: 9 -> 7 WIN-HALT + 2
  clean). h045 is the 7th unconsumed closure WIN; h046-h051 (6 keys)
  untouched; verdicts not consumed anywhere.
- Part V (verifier amendment, note commit `267ead27`): batch-8 h045
  IF-ADOPTED decomposition per Part H-bis/J/R methodology, using a
  published base-control experiment `n11-class2634-base-control-20261122`
  (`242c1de7`: pinned Part M script re-run twice on the takeover host,
  run-to-run byte-identical and byte-equal to the published Part M
  outputs) and `n11-central-reply-class2634-win-h045-ifadopted-20261122`
  (`edd58822`, 32 files): fail-closed increments (44 rows / WIN-only /
  43-LOSS-only, h002 excluded from every increment), conflict-0 merges,
  3-line-diff refresh runs 6/6 byte-identical, and a compare script that
  faithfully re-executes the refresh class-status semantics (with the
  Board fail-closed free verification) and asserts every recomputed
  class_status_count against the published summaries before reporting
  deltas. Fetch-back 39/39 byte-identical (commit-pinned raw URLs).
- Measured deltas vs base: WIN-only excluded_now flips are exactly
  {2634, 5632} (membership 2, 3-route machine cross-check; self-exclusion
  of 2634 as under g018/j033). Unlike j033, the h045 WIN hits the frozen
  update8 plan in exactly 1 group (root 49; remaining 31,836 -> 31,786,
  resolved 23 -> 24). The 43 LOSS rows resolve 43 baseline requirements
  and cut the joint greedy union 35,857 -> 34,906 (-951, largest measured;
  biggest per-root mover root 49, -88) with WIN-only greedy -1 subsumed.
  Worklist deltas exactly additive (-1/-45/-46). free_now 34 and all
  per-root coverage unchanged (machine gate).
- State: no verdict consumed anywhere. The 7 unconsumed WINs remain
  with the scrutiny owner (C++ second-implementation gate pin
  `9193f5b6...`). A Part K/O/P/T-style third-implementation spot
  verification of the batch-8 rows (h045 WIN + stratified LOSS anchors)
  was declared open by Part V and remains unclaimed. The standard
  11x11 empty board, the 19 central-reply roots and classes
  1518/2634 all remain UNKNOWN. Observed HEAD-before-push for this log
  update is recorded in the commit message.

## Session continuation 12 (2026-11-22, verifier): Part W batch-8 h045 third-implementation spot verification - the Part V open declaration fulfilled

- Immediately after the Part V publication (continuation 11), the same
  session executed the third-implementation spot verification of the
  batch-8 rows that Part V had declared open, without a separate prior
  declaration (the open declaration was already on record in
  continuation 11; list_commits confirmed no competing claim on main
  before the push).
- Experiment `research/experiments/n11-centralreply-closure-batch8-h045-thirdimpl-20261122/`,
  published in 3 commits: scaffold `b31abeeb` (README + scripts 6 +
  inputs 9), targets `c5ebc2fc` (8 files), verification tail `a1ba4ccf`
  (anchors 4 + negatives 2 + rules-gate + status.log + audit-summary +
  MANIFEST 33 entries). Fetch-back 34/34 byte-identical
  (commit-pinned raw URLs, curl + cmp).
- Sources pinned to the published batch-8 raws (commit `1f127fb8`,
  batch-keys sha `5c42a950...`); scripts byte-identical to the batch-9
  Part T kit pins except the batch-8-adapted input maker and the audit
  schema name.
- 14 solver runs at max 4 parallel, a/b 2-pass each: h045 WIN 1 at
  7,348,868 expansions / 4,145,900 ttHits (a/b identical, agreeing with
  the replica df-pn WIN 6,366,900 nodes); h018 LOSS 2 (1,756,741 /
  1,066,681); h025 LOSS 2 (13,169,795 / 7,161,043); h026 LOSS 2
  (4,938,236 / 2,884,833); anchors k02a WIN 9,106,337 / 4,991,527 and
  l1a LOSS 7,660,602 / 3,951,175 identical to the published Part T
  measured values; negatives ng1/ng2 GATE_FAIL wording match;
  runlimit/wall-inconclusive 0. Rules gate: quads 95,670 == replicas,
  triples 195,044, mismatches 0. Audit 71/71 gates PASS, two runs
  byte-identical.
- With Part W, all 7 unconsumed closure WINs (b018, d002, e002, f017,
  g018, j033, h045) have third-implementation spot verification on
  record. Verdict consumption remains unchanged: none consumed, the
  scrutiny owner (C++ second-implementation gate pin `9193f5b6...`)
  is still pending. The standard 11x11 empty board, the 19
  central-reply roots and classes 1518/2634 all remain UNKNOWN.
- Note Part W amendment published at note commit `db9805bb`
  (fetch-back byte-identical). Observed HEAD-before-push for this log
  update is recorded in the commit message.

## Session continuation 13 (2026-11-22, verifier): batch-10 (class 8784) parallel declaration observed; own declaration draft withdrawn unpublished; read-only canonical audit of the published Part X scaffold (verdict-neutral)

- While this session was rebuilding its own batch-10 (class 8784, rank 9)
  staging tree after an execution-environment reset (the Part M refresh
  byte-reproduction and the val-gate 4/4 node-exact check were completed
  twice, before and after the reset, with identical results), a parallel
  instance of the hourly lane published the Part X batch-10 declaration
  (commit `ab8641fb`: class 8784 rank 9, 52 keys m001-m052, scaffold 64
  files + note Part X amendment). This session's own batch-10 declaration
  draft (same class, assembled but never pushed) was therefore withdrawn;
  nothing was pushed to the batch-10 scope by this session.
- Read-only audit of the published Part X scaffold (independent
  regeneration on this host): the pinned Part M refresh machinery
  (`0bc10a05...`) was re-run twice from the published pinned inputs (all
  six pins byte-verified: graph `54f9c364...`, merged cache
  `a998f4c0...`, update8 `b658290a...`, board `954d3a10...`, policy
  `78655e94...`, quarantine `81d23160...`); the regenerated worklist
  (sha `ca3ee3bc...`) and the three published refresh outputs are
  byte-identical to the Part M originals. Against that canonical
  material: the 52 published batch-10 input CSVs are byte-identical to
  the canonical serving_class=8784 rows (probe_order 383-434);
  batch-keys.json equals the canonical 52 rows on
  (s5_index, lo, hi, legal, membership_class_count, probe_order) with
  probe_order ascending (lo/hi serialized there as JSON strings; numeric
  values exact, no decimal drift); class_mask `[6052837899186012160, 0]`
  matches the regenerated closure-classes rank-9 row;
  scripts/jsreplay.js sha256 `845856173d...` equals the pinned replica;
  the published val-gate rows are node-exact (at2m result 0/2,000,000
  twice, 15m result 2/3,651,923 and result 2/5,040,200). No defect found.
- Environment note: the execution environment reset once mid-session;
  all published artifacts were unaffected (byte-verified on main and
  mirrored in the kit); the reset destroyed only local scratch trees
  under the work directory, which were fully regenerated with identical
  byte-verified results before the audit above.
- State: batch 10 is in flight by the parallel instance; this session
  does not touch its scope. Verdict consumption unchanged; the 7
  unconsumed closure WINs (b018/d002/e002/f017/g018/j033/h045) stay with
  the scrutiny owner. The standard 11x11 empty board, the 19
  central-reply roots and class 8784 all remain UNKNOWN. Observed
  HEAD-before-push for this log update is recorded in the commit message.

## Session continuation 14 (2026-11-22, prober): batch 11 (class 8785) Part Z - observing the WIN-HALT, declaring-session-loss judgement, takeover with full cross-host reproduction, publication

- Observed on latest main: the Part Z batch-11 (class 8785, renewed rank 8)
  declaration scaffold commit `3cc96099` (2026-11-22T10:28:54Z, 30 files:
  README + batch-keys.json + z001-z028 inputs + val-gate inputs) by a
  parallel instance, then silence after ~10:36Z. The declaring host's kit
  checkpoint mirror (`batch8785-z/`) contained the complete first wave
  evidence: 8 raws (z001-z004 p1/p2, all 2-pass node-exact), its status.log
  (WAVE-START z001-z004 at 10:32:09Z; z002 10:33:54Z, z001 10:34:22Z, z004
  10:35:35Z, z003 PASS 15000000,1,11601265 + WIN-HALT + RUNNER-STOP rc>=42 at
  10:36:40Z) and its four val-gate outputs. **Pre-registered WIN-HALT (rc=45)
  fired at z003** (s5_index 198530, key `[1225542323476103168, 1]`, legal 82,
  probe_order 334: **result 1 WIN, 11,601,265 nodes**, 2-pass node-exact).
  No row was ever published by the declaring session (inconsistent with the
  batch 1-7 push-while-running practice; Part U precedent), so after 20+
  minutes of silence this session judged a declaring-host loss, completed
  the scaffold and published everything under takeover.
- Pre-publication machine audit (fail-closed, all on this host): (1) the 8
  rescued raws carry the quads gate line and 2-pass (budget,result,nodes)
  agreement, consistent with the rescued status.log PASS rows; (2) published
  batch-keys.json (blob `a5d3193a02dd...`, 51 keys) == declaring kit copy
  bytes; the 51 keys == Part Y re-audit worklist rows serving_class=8785
  (probe_order 332-382 of `1807e4d2...`, 51/51, no duplicates, input CSVs
  51/51); (3) 51 keys absent from the canonical merged cache (6,027 rows
  `95e868d6...`) and the quarantine registry (2 active entries), 0 hits; (4)
  no unconsumed WIN key among class 8785's 51 children or class 8106's 52
  (0 hits; b018 re-derived independently); (5) the Part Y rank erratum
  verified against the published renewed closure-classes `61943b85...`
  (rank 8 = 8785, rank 9 = 1518, rank 10 = 8106), matching the Part Z
  declaration's erratum; (6) jsreplay.js == pin `84585617...`.
- Takeover cross-host reproduction (this host `d3578b9e...`, pinned replica,
  fresh cold, all node-exact vs the declaring host): val-gate 4/4
  (15m 2/3,651,923 and 2/5,040,200; at2m 0/2,000,000 x2); **z003 WIN
  1/11,601,265 both passes**; z001 LOSS 3,146,511 both; z002 LOSS 2,256,914
  both; z004 LOSS 2/6,424,054 both (runner wall 10:55:50-11:01:28Z).
  Published as output/raw/z00X.pN.takeover.out + output/val-gate/
  *.takeover.out + output/status.takeover.log alongside the declaring
  host's rescued rows (batch-8 `.takeover.out` naming convention).
- Publication: scaffold completion (43 files: z029-z051 inputs, rescued
  raws + status.log, declaring-host val-gate outputs, val-gate input CSVs,
  scripts) then takeover outputs + README amendment (takeover provenance +
  cross-host reproduction + Result) + single-owner note Part Z status
  update + this log continuation.
- Honesty record: 4/51 probed, z005-z051 untouched (WIN-HALT respected; no
  new keys started). z003 is the 8th unconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003), verdict NOT consumed,
  scrutiny owner (C++ second-implementation gate pin `9193f5b6...`)
  unchanged. Third-implementation spot verification of z003 (Part
  K/O/P/T/W lineage) NOT done. If-adopted decomposition (Part V/R lineage)
  NOT done. Next clean candidate: renewed rank 10 class 8106 (1518 carries
  j033, 8785 carries z003). The standard 11x11 empty board, the 19
  central-reply roots and class 8785 all remain UNKNOWN throughout;
  nodes/passes are not verdicts. Observed HEAD-before-push for this log
  update is recorded in the commit message.


## Session continuation 15 (2026-11-22, verifier): Part AA batch-11 z003 third-implementation cross-verification executed and published; note status update; all 8 unconsumed WINs now third-implementation verified

- Scope: Part AA, declared in the single-owner note before execution
  (commit `1d750f19`, observed HEAD `2da303db...`): verdict-level
  cross-verification of the batch-11 WIN row z003 and the full first-wave
  probed LOSS rows (z001/z002/z004; batch 11 probed 4/51, z005-z051
  untouched) with the pinned third implementation (`third_impl.js` pin
  `08ea958f...`), anchors k02a/l1a and negatives ng1/ng2. Verdict NOT
  consumed in any way; the adoption decision remains with the scrutiny
  owner (C++ second-implementation gate pin `9193f5b6...` precedent,
  unchanged; not executable in this compiler-less lane).
- Machine results (all gates fail-closed, run on this host, max 4
  parallel, 1 row = 1 process, cap 300M expansions, wallcap 240s,
  a/b two-run determinism): z003 third-impl WIN 1 / 13,781,596 expansions /
  7,500,476 ttHits (a/b identical; agrees with the pinned-replica df-pn
  WIN 11,601,265 nodes, cross-host node-exact published by the
  Part Z takeover); z001 LOSS 3,594,991 / z002 LOSS 2,547,371 /
  z004 LOSS 7,426,794 expansions (all agree with replica verdicts
  3,146,511 / 2,256,914 / 6,424,054 nodes). Anchors reproduced the
  published third-implementation values exactly (k02a WIN 9,106,337 /
  4,991,527; l1a LOSS 7,660,602 / 3,951,175). Negatives ng1/ng2 matched
  the GATE_FAIL wording. Rules gate: quads 95,670 == replica, triples
  195,044, mismatches 0. audit.py (schema `batch11-z003-thirdimpl-audit-v1`)
  71/71 gates PASS, executed twice byte-identical; divergence 0;
  wall-inconclusive 0.
- Inputs machine-derived by `make_inputs_batch11.py` (fail-closed,
  zero hand transcription) from the published batch-11 raws of BOTH hosts
  (declaring-host p1/p2 8 files + takeover-host `.takeover.out` 8 files,
  commit-pinned raw CDN from `12be47c7`/`40e02623`, sha256 all verified),
  cross-checked against status.log, status.takeover.log, and the
  published batch-keys.json (sha256 `8ef22069...`, commit `3cc96099`).
- Publication: experiment directory
  `research/experiments/n11-centralreply-closure-batch11-z003-thirdimpl-20261122/`
  (34 files) in 3 commits: `28b23f14` (scaffold) -> `fea875eb` (targets)
  -> `f2a8fa48` (anchors + negatives + rules-gate + status.log +
  audit-summary.json + MANIFEST), after the declaration commit
  `1d750f19`. Fetch-back: commit-pinned raw URL + sha256sum, 34/34 files
  byte-identical.
- Meaning: all 8 unconsumed closure WINs (b018/d002/e002/f017/g018/
  j033/h045/z003) are now third-implementation cross-verified
  (Part G / Part P / Part T (j033) / Part W (h045) / this Part AA
  (z003)). Verdicts remain unconsumed; scrutiny owner unchanged.
  Batch record stands at 11 batches: 8 WIN-HALT + 3 clean
  (23963/10324/8784, the 33rd/34th/35th Board-verified free classes).
  Open items for future declarations: z003 if-adopted decomposition
  (Part V/R lineage, refresh kit scenario pin `88671526...`, base
  cache `95e868d6...` series) and next batch candidate renewed rank 10
  class 8106 `[1152926194711134208, 0]` (unknown 52).
- Honesty record: 11x11 empty board, the 19 central-reply roots and
  class 8785 remain UNKNOWN throughout; nodes/expansions are not
  verdicts. Observed HEAD-before-push for this update is recorded in
  the commit message.


## Session continuation 16 (2026-11-22, verifier): Part AB batch-11 z003 if-adopted decomposition executed and published; base control cross-host reproduction; greedy non-additivity measured (verdict unchanged)

- Scope: Part AB, declared in the single-owner note before execution
  (commit `a081823a`, observed HEAD `3de95445...` after the concurrent
  eight-row-lane commits were checked for scope non-interference): the
  Part H-bis / J / R / V lineage what-if decomposition for the batch-11
  WIN row z003 (s5 198530, WIN 1, 11,601,265 nodes, 4-way cross-host
  node-exact, third-implementation verified by Part AA). Verdict NOT
  consumed anywhere; verdicts of all 8 unconsumed closure WINs stay with
  the scrutiny owner (C++ second-implementation gate pin `9193f5b6...`
  precedent, unchanged).
- Base control (published first):
  `research/experiments/n11-class8785-z003-base-control-20261122/`
  (commit `36ac2359`, 7 files, fetch-back 7/7 byte-identical, observed
  HEAD-before-push `33f4d041...`). Pinned inputs fetched from the repo
  canonical copies and sha256-verified (dependency-graph `54f9c364...`,
  merged cache 6,027 rows `95e868d6...`, update8 `b658290a...`, board
  `954d3a10...`, policy `78655e94...`, quarantine `81d23160...`); the
  published Part Y scenario script (`88671526...`) ran twice on this host:
  all four outputs byte-identical between runs, and the three summary
  outputs byte-equal to the published Part Y re-audit; probe-worklist
  65,154 rows sha `1807e4d2...` matches the Part Y/Z record.
- Decomposition experiment (published):
  `research/experiments/n11-centralreply-class8785-win-z003-ifadopted-20261122/`
  (commit `7f698e9a`, 32 files, fetch-back 32/32 byte-identical). Three
  increments machine-derived fail-closed from the published batch-11 raws
  of both hosts (4-way pass agreement + declaring status.log agreement +
  batch-keys cross-check; shas `2778d392...` / `32c582c1...` /
  `939f8deb...`); three scenario merges onto the canonical 6,027-row
  cache (published merger, selftest PASS, conflicts 0, duplicates 0;
  6,028/6,030/6,031 rows); per-scenario refresh byte-copies (docstring +
  ROOT + CACHE + sha-pin lines only) run twice each, 6/6 byte-identical;
  root {X,60,27} baseline 119/119 everywhere; per-root free coverage
  identical to base everywhere.
- Machine-verified results (`compare_deltas_batch11.py`, all gates PASS;
  class_status_counts recomputed from graph+update8+cache and asserted
  equal to the published summaries for BASE and all three scenarios before
  any delta; `output/decomp-deltas-batch11.json` sha `99c744b9...`):
  excluded_now flips = exactly {5307, 5748, 8785} in PWINZ003 and PFULL4
  (graph holders of s5 198530, membership_class_count 3; class 8785
  self-exclusion like 5473/1518/2634), PLOSS3 empty; class 8785 unknown
  51 -> 50/48/47 (additive); update8 win-hit = exactly 5 groups all
  served by class 5748; newly resolved baseline requirements
  {198530} / {211089} / {198530,211089}; remaining delta -58/-1/-58
  (sub-additive by exactly 1: s5 211089 (z004) is also a cost child of
  class 5748, machine-verified from the frozen graph, so its separate
  LOSS resolution is subsumed by the win-hit unknown-set drops);
  worklist -2/-4/-6 (fully additive); **joint greedy 35,242 -> 35,241 /
  35,241 / 36,039: WIN-only -1, LOSS-only -1, full +797 - the first
  measured packet whose full greedy exceeds both single-row scenarios**
  (per-root greedy_union_size changed only at root 49: 2,890 -> 2,899 /
  2,899 / 2,946; the union growth beyond that is greedy option
  re-selection cascades; group_best_options_nonfree 2,127 invariant).
  All scheduling quantities; no coverage or verdict content.
- Honesty record: verdicts not consumed; z005-z051 untouched; scenario
  caches are analysis-only; the standard 11x11 empty board, the 19
  central-reply roots, class 8785 (canonical cache still has all 51
  children unknown) and class 8106 remain UNKNOWN throughout;
  nodes/passes/expansions are not verdicts. Open item for a future
  declaration: next batch candidate renewed rank 10 class 8106
  `[1152926194711134208, 0]` (unknown 52). Kit mirrors saved under
  `batch8785-z-ifadopted/` (33-entry manifest) and
  `reaudit8785-z-base-control/` (8-entry manifest). Observed
  HEAD-before-push for this update is recorded in the commit message.

## Continuation 17 (2026-11-22): batch 12 (class 8106, Part AC) declared, run, and published - WIN-HALT x2 (n005/n006), two WIN rows in one wave, verdicts not consumed

- Session opened after an execution-environment reset had wiped the local
  workspace mid-preparation (recorded honestly below). Latest main was
  re-fetched first; HEAD was `a134d8fd` (eight-row lane), the closure-lane
  note and session log untouched by parallel lanes.
- Fail-safe block re-done from scratch after the reset: the six Part Y
  pinned inputs were re-fetched from the repo canonical copies
  (commit `0a369d6c` pinned raw) with all sha256 matching
  (dependency-graph `54f9c364...`, merged cache 6,027 rows `95e868d6...`,
  update8 `b658290a...`, board `954d3a10...`, policy `78655e94...`,
  quarantine `81d23160...`), and the published Part Y scenario script
  (`88671526...`) was re-run twice on this host: all four outputs
  byte-identical between the runs; closure-classes /
  per-root-coverage / refresh-summary byte-equal to the published Part Y
  canonical outputs; probe-worklist 65,154 rows sha `1807e4d2...` matching
  the published record (cross-host byte-exact reproduction).
- Batch-12 (class 8106, renewed rank 10) keys machine-extracted from the
  regenerated worklist: 52 rows, probe_order 434-485, all absent from the
  canonical cache (52/52 misses), quarantine cross-check 0 hits,
  duplicate free, closure-classes rank-10 row byte-verified, 8-WIN-key
  cross-check 0 hits. Part AC declaration pushed as note amendment
  (commit `609e9137`, fetch-back byte-exact), then the scaffold
  (README + batch-keys.json 52 keys + 52 input CSVs + pinned jsreplay.js +
  runbatch.sh + runner-all.sh + val-gate 4 inputs and 4 this-host outputs,
  65 files) published as commit `d333bb2c` with 65/65 fetch-back
  byte-exact. Val-gate 4/4 node-exact on this host (at2m result
  0/2,000,000 twice; 15m result 2/3,651,923 and result 2/5,040,200).
- Runner (2 cores, up to 4 workers, probe-order waves, resume-safe):
  wave 1 n001-n004 all LOSS; wave 2 surfaced **two** 2-pass node-exact
  WIN rows - n006 (s5 219608, `[1152926194711134208, 128]`, legal 78,
  3,695,373 nodes) and n005 (s5 188395, `[1153489144664555520, 0]`,
  legal 82, 12,863,268 nodes) - with in-flight n007/n008 completing LOSS
  (2,905,330 / 3,442,689). Batch stopped at 8/52 probed under the
  pre-registered WIN-HALT rule. First closure batch with two WINs, and
  the first WIN (n006) is a canonical child sharing the class mask lo.
- Raw chunks published: `eca35f3c` (n001-n004, 8/8 fetch-back) and
  `ace92d84` (n005-n008 + status.log, 9/9 fetch-back); README Result
  section published as `68f2c699` (fetch-back byte-exact).
- n005/n006 are the 9th and 10th unconsumed closure WINs
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006), all pending the
  scrutiny owner. Third-implementation cross-verification and the
  8-row if-adopted decomposition remain open (future declarations).
  Next first-clean candidate: renewed rank 11 class 16930
  (`[1152921504875282432, 272]`, unknown 52; 10-WIN cross-check 0 hits).
- Nothing consumed anywhere. The standard 11x11 empty board, the 19
  central-reply roots, class 8785/8106 and every other class remain
  UNKNOWN; node counts are not verdicts. Kit mirror saved under
  `batch8106-n/` (82 files + manifest). Observed HEAD-before-push
  for this update is recorded in the commit message.

## Continuation 18 (2026-11-22): Part AD batch-12 third-implementation cross-verification completed and published - all 10 unconsumed closure WINs now third-impl corroborated (verdicts not consumed)

- Part AD (single-owner note amendment, declared before execution, note
  commit `33657c94`, observed HEAD-before-push `9759774b`) executed and
  published the third-implementation verdict-level cross-verification of
  the complete batch-12 probed set: 2 WIN rows (n005/n006) + 6 LOSS rows
  (n001-n004/n007/n008), Part G/K/O/P/T/W/AA protocol unchanged.
- Inputs machine-derived by `make_inputs_batch12.py` fail-closed from the
  published batch-12 sources (raws chunk commits `eca35f3c`/`ace92d84`,
  commit-pinned raw CDN): 2-pass (budget,result,nodes) equality asserts,
  status.log PASS rows + `n005 WIN-HALT`/`n006 WIN-HALT` +
  RUNNER-STOP/RUNNER-EXIT presence asserts, batch-keys.json (sha256
  `de55df83...`, scaffold `d333bb2c`) key/legal cross-checks in exact
  Python ints, derived CSVs byte-equal to the published batch-12 input
  CSVs (8/8). Sources not republished.
- 22 solver rows on this 2-core host (pairs, at-most-4 convention), all
  clean, every a/b pair identical on (result, expansion, ttHits, reason):
  - **n005 WIN agree** (third-impl 15,280,890 expansions / 8,220,782
    ttHits vs replica WIN 12,863,268 nodes); **n006 WIN agree**
    (4,233,764 / 2,394,370 vs 3,695,373);
  - 6/6 LOSS agree (n001 7,693,366 / n002 3,554,378 / n003 5,243,307 /
    n004 4,271,858 / n007 3,359,814 / n008 3,976,246 expansions);
  - anchors k02a WIN 9,106,337/4,991,527 and l1a LOSS 7,660,602/3,951,175
    node-exact the published third-impl values; ng1/ng2 GATE_FAIL with the
    published messages; rules gate quads 95,670 == replica, 195,044
    triples, 0 mismatches;
  - audit.py (schema `batch12-wins-thirdimpl-audit-v1`, run twice
    byte-identical): **111/111 gates PASS, 0 divergences, 0
    wall-inconclusive**.
- Publication: `research/experiments/n11-centralreply-closure-batch12-wins-thirdimpl-20261122/`
  commits `4e9c525f` (scaffold 20) → `d44fcfb4` (targets 16) → `d25a0db9`
  (anchors 4 + negative 2 + rules-gate + status.log + audit-summary +
  MANIFEST, 10). Fetch-back commit-pinned raw + cmp: **46/46 byte-exact,
  MANIFEST 45/45 sha256 exact**; the 4 pinned scripts byte-identical to
  the published Part AA copies (blob-sha match).
- Note Part AD publication status update pushed as `6d14c38b`: the
  parallel Part AE (batch 13, class 16930) declaration had landed on the
  note in between; the create_or_update sha gate caught the stale note
  copy, the note was re-fetched and the appendix re-appended on top of the
  latest bytes (declared interleave recorded, no clobbering).
- Milestone: **all ten unconsumed closure WINs**
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006) are now
  third-implementation corroborated at the verdict level (Part G/P/T/W/
  AA/AD). Verdicts still not consumed; adoption remains with the scrutiny
  owner (C++ second-implementation gate precedent, pin `9193f5b6...`).
- Honesty record: nothing consumed anywhere; n009-n052 (44 batch-12 keys)
  untouched; the standard 11x11 empty board, the 19 central-reply roots,
  class 8106 and every other class remain UNKNOWN throughout;
  nodes/expansions are not verdicts. Open items for future declarations:
  n005/n006 if-adopted decomposition (Part V/R/AB style over the 8 probed
  rows). Kit mirror refreshed under `batch8106-n-thirdimpl/` (46-entry
  manifest, byte-identical to the published files). Observed
  HEAD-before-push for this update is recorded in the commit message.

## Continuation 19 (2026-11-22): batch 13 (class 16930, Part AE) declared, run, and published - WIN-HALT x2 (p002/p003), verdicts not consumed; same-scope Part AD duplicate stood down, full cross-host audit-summary agreement verified

- Session opened after a context compaction. Latest main re-fetch found the
  Part AD declaration (`33657c94`, batch12-wins third-impl, another owner,
  "declared before execution") already on the note, while the local
  workspace had meanwhile executed the SAME scope (batch-12 n005/n006
  third-impl battery over the 8 probed rows, 111/111 gates PASS,
  byte-identical audit twice). Per the pre-registered rule (do not proceed
  when a same-scope declaration exists on main), the duplicate execution
  was NOT published and stood down. The Part AD owner has since executed
  and published the full battery (`4e9c525f` scaffold / `d44fcfb4`
  targets / `d25a0db9` tail, 46 files, 111/111 gates PASS). Machine
  cross-check after that publication: the stood-down duplicate's
  audit-summary agrees with the published Part AD audit-summary on ALL
  8 target rows (replica_result, third_result, third_expansion,
  third_ttHits) - full cross-host agreement - recorded as an extra
  reproducibility corroboration of the third implementation only; it
  changes no verdict and nothing is consumed. Kit mirror
  `batch8106-n-thirdimpl` preserves the duplicate's bytes; the
  published Part AD audit-summary correctly renamed the schema
  (`batch12-wins-thirdimpl-audit-v1`), while the local copy of the
  template had kept the batch11-z003 EXP/schema strings (caught and
  fixed before anything was published here).
- Technical warning recorded for the Part AD owner (and any future
  third-impl session): `audit.py` cloned from the Part AA template keeps
  the batch11-z003 EXP/schema strings and the generated
  `audit-summary.json` mislabels the experiment. Caught and fixed locally
  before any publication (re-run 111/111 PASS, twice byte-identical).
- Batch 13 declared as Part AE (`72608b64`, observed HEAD `7eb9ab70`):
  first clean candidate under the pre-registered rule = renewed rank 11
  class 16930 (mask `[1152921504875282432, 272]`, unknown 52; ranks 1-9
  carry refutation evidence, rank 10 (8106) WIN-HALTed in Part AC).
  Fail-safes machine-run and PASS before declaring: 52 keys
  (probe_order 486-537) extracted from the regenerated Part Y worklist
  (run1 == run2, sha `1807e4d2...`; closure-classes.csv /
  per-root-coverage.csv / refresh-summary.json byte-equal to the published
  canonical copies at `7eb9ab70`); 52/52 absent from the canonical merged
  cache (6,027 rows, sha `95e868d6...`); quarantine 0 hits both
  directions; duplicate free; rank-row byte check; 10-WIN-key cross-check
  0 hits (now including n005/n006).
- Scaffold published `90ee1c87` (65 files, 65/65 fetch-back byte-exact;
  batch-keys.json sha `c6c56a1a...`; pinned replica jsreplay.js
  `84585617...`; val-gate 4/4 node-exact on this host: at2m 0/2,000,000
  twice, 15m 2/3,651,923 and 2/5,040,200). Kit mirror saved under
  `batch16930/`.
- Runner (2 cores, up to 4 workers, one 4-key wave, resume-safe) started
  2026-11-22T12:16:52Z, stopped 12:21:20Z under the pre-registered
  WIN-HALT rule at 4/52 probed: **p003 WIN 1 / 7,489,274 nodes** (key
  `[3458764514088976384, 272]`, legal 81, s5 203419) and **p002 WIN 1 /
  10,770,254 nodes** (key `[1153484454828703744, 272]`, legal 85, s5
  185003), both 2-pass fresh cold node-exact; in-flight wave members
  disclosed honestly (p001 LOSS 4,631,275, p004 LOSS 2,291,059); no
  determinism mismatch, no budget exhaustion. p005-p052 (48 keys) unprobed.
- p002 and p003 are the 11th and 12th unconsumed closure WINs; nothing
  consumed anywhere; the standard 11x11 empty board, the 19 central-reply
  roots and class 16930 remain UNKNOWN; node counts are not verdicts.
  Publications: raw chunk + status `b4b55ec8` (9/9 fetch-back
  byte-exact), README Result `f5df3cbf` (byte-exact).
- Open items for future declarations: third-implementation
  cross-verification of the two WIN rows (plus the 2 LOSS rows), if-adopted
  decomposition of the 4 probed rows, batch 14 = rank 12 class 23101
  (`[1152921504892059648, 16]`, unknown 52) as the next first-clean
  candidate (fail-safes re-run at declaration time). Observed
  HEAD-before-push for this update is recorded in the commit message.

## Continuation 20 (2026-11-22): Part AG batch-13 third-implementation cross-verification completed and published - all 12 unconsumed closure WINs now third-impl corroborated (verdicts not consumed)

- Fresh main pull before any execution: HEAD `54b7453d` (batch-14 Part AF
  scaffold published; Part AE batch-13 WIN-HALT x2 status published; the
  open items were the batch-13 third-impl cross-verification and the
  batch-12/13 if-adopted decompositions). No same-scope declaration for a
  batch-13 third-impl experiment; Part AG sequence number free; declared
  Part AG in the single-owner note as commit `e84242c8` (138,848 bytes,
  fetch-back byte-exact) BEFORE the first solver run, observed
  HEAD-before-push `54b7453d`.
- Experiment `research/experiments/n11-centralreply-closure-batch13-wins-thirdimpl-20261122/`:
  inputs machine-derived from the published batch-13 sources (raws 8 +
  status.log, chunk commit `b4b55ec8`, commit-pinned raw CDN; batch-keys.json
  sha `c6c56a1a...` pinned against scaffold `90ee1c87`) by the Part AD
  script adapted with all EXP/schema strings renamed to
  `batch13-wins-thirdimpl-*` (the Part AE stale-template warning heeded);
  every derived target CSV byte-identical to the published batch-13 input
  CSVs; kit mirror cross-check 10/10 byte-identical before execution.
- Execution (2-core host): rules gate first (quads 95,670 == replica;
  195,044 triples, TBL==wob, 0 mismatches), negatives ng1/ng2 both GATE_FAIL
  with the published messages (ng1 inside the runner, ng2 executed
  immediately after the runner's exit because the runner chained the two
  negative gates with `&&` after ng1 which exits rc=1 by design; disclosed
  in the README honesty record), anchors k02a/l1a reproduced EXACTLY at
  9,106,337/4,991,527 and 7,660,602/3,951,175 (a/b pairs), then the
  complete probed row set: **p002 WIN 1 third-impl 12,593,747 expansions /
  7,021,485 ttHits (replica WIN 10,770,254 nodes) and p003 WIN 1
  8,626,319/4,959,871 (replica 7,489,274) agree; p001 LOSS 2
  5,334,954/3,020,029 and p004 LOSS 2 2,593,393/1,571,815 agree (replica
  4,631,275 / 2,291,059); 0 divergences, 0 wall-inconclusive**, all a/b
  pairs identical on (result, expansion, ttHits, reason); every wall time
  far below the 240 s wallcap (max 76.75 s).
- audit.py (schema `batch13-wins-thirdimpl-audit-v1`, run twice
  byte-identical): **71/71 gates PASS**. Nothing was consumed into any
  canonical cache; the p002/p003 WINs (11th/12th unconsumed closure WINs)
  stay scrutiny-owner-blocked. With this, the twelve unconsumed closure
  WINs (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003) are
  all third-implementation corroborated at the verdict level.
- Publication: scaffold `71f4803d` (17 files: README + pinned scripts 7 +
  inputs 9; the 4 pinned script bytes blob-identical to the published Part
  AD / Part AA copies) -> targets `62f29489` (8 rows) -> completion
  `ba5d0309` (10 files incl. audit-summary.json and MANIFEST). Fetch-back:
  **35/35 files byte-exact, MANIFEST 34/34 sha256 exact**. Note Part AG
  publication status update `611e7ab2`. Kit mirror saved under
  `batch16930-thirdimpl/`.
- Open items for future declarations: if-adopted decomposition of the
  batch-13 4 probed rows and of the batch-12 8 probed rows (both the
  WIN-only / LOSS-only / full splits, Part V/R/AB methodology); batch 14
  (Part AF) continues under its own owner. Verdicts unchanged everywhere:
  the standard 11x11 empty board, the 19 central-reply roots and class
  16930 remain UNKNOWN; nodes/expansions are not verdicts. Observed
  HEAD-before-push for this update is recorded in the commit message.

## Continuation 21 (2026-11-22, this host): Part AH batch-12 if-adopted decomposition completed and published

- Resumed from continuation 20. Part AG closure (batch-13 third-impl)
  had already been published by this host earlier in the session; the
  remaining explicit open item from Part AD was the batch-12 (class 8106)
  n005/n006 if-adopted decomposition, declared as **Part AH** in the
  single-owner note (commit `41e1ff52`, blob sha1-locked update on top of
  the Part AG status note `611e7ab2`) BEFORE any execution. Raw-CDN main
  caching served a stale note copy during the pre-check; detected via the
  local blob-sha1 recomputation rule (commit-pinned fetch is the fresh-main
  check, `main` raw URLs are not trustworthy during parallel pushes).
- Base control
  `research/experiments/n11-class8106-n005n006-base-control-20261122/`:
  pinned Part Y refresh script (`88671526...`), pinned inputs
  machine-sha-verified after commit-pinned fetch (dependency graph
  `54f9c364...` etc), executed twice: 2/2 byte-identical runs AND the three
  outputs byte-equal to the published Part Y canonical re-audit
  (`61943b85...`/`33f01a0c...`/`25987add...`), i.e. the third host
  environment reproduces Part Y and the batch-11 base control
  byte-exactly. Publishing + fetch-back: commit `9fd7dee5`.
- Decomposition
  `research/experiments/n11-centralreply-class8106-win-n005n006-ifadopted-20261122/`:
  batch-12 published raws were re-fetched from the published chunks
  (`eca35f3c` wave-1, `ace92d84` wave-2) and verified 17/17 byte-identical
  to the kit mirror BEFORE use. Increments built 3-way fail-closed
  (p1/p2/status; batch-12 has no takeover passes by construction, unlike
  batch-11's 4-way): full 8 rows `d1954280...`, win-only 2 rows
  `dd5fc998...` (first multi-WIN increment of the closure grind), loss-only
  6 rows `d18ddaf8...`. Scenario caches via the published fail-closed union
  merger (selftest PASS, conflicts 0, dup 0): PWIN2 6,029 rows WIN 160 /
  LOSS 5,869 `c13f81d7...`; PLOSS6 6,033 `898ca5f4...`; PFULL8 6,035
  `21bbef33...`. Scenario refresh scripts are diff-verified 4-hunk
  adaptations of the Part Y script (docstring/ROOT/CACHE/sha-pin only);
  2 runs per scenario, 6/6 deterministic.
- Deltas (`compare_deltas_batch12.py` -> `decomp-deltas-batch12.json`
  `a4152995...`; all recomputed class_status_counts asserted equal to all
  four published summaries before reporting; Board fail-closed free
  verification re-executed for every scenario):
  - excluded_now flips: PWIN2 = PFULL8 = {5007, 5011, 6147, 6166, 8106}
    (23 -> 28), PLOSS6 empty; the flip set is the UNION of the two WIN
    holder triples (3+3, overlap = class 8106 itself = union 5),
    machine-identified three ways (graph cost-child holders,
    batch-keys membership_class_count, recompute flip sets).
  - class 8106 unknown 52 -> 50/46/44, additivity gated.
  - update8: all 8 probed rows are baseline requirements (batch-11
    contrast: only z003/z004); newly-resolved 2/6/8 exact; remaining
    sub-additive by exactly 6 (-52/-6/-52) because the class-8106 flip
    drops its whole 52-member remaining set.
  - win-hit groups 4 (PWIN2 = PFULL8), all served by class 8106 itself
    (reply 60; roots first=14 and first=38), doubling as an excluded_now
    flip (batch-11's z003 pattern hit via peer 5748 which did not
    self-exclude).
  - joint greedy +52/0/+52 additive (contrast Part AB +797 cascade);
    per-root individual_greedy_union NON-additive at root 14
    (+1/+7/+5); roots 38 and 49 additive; per-root free coverage
    (free_now/uncovered) identical to base in every scenario; root
    first=27 119/119 free thirds everywhere.
  - worklist additive -4/-7/-11; group_best_options_nonfree 2,127 in all
    four runs.
- Published commits `9fd7dee5` (scaffold + base control), `7ca0c3af`
  (increments + merges + scenario scripts), `bc97ef35` (pwin2),
  `c2fe5514` (ploss6), `3e6c0f89` (pfull8 + deltas); note Part AH status
  update `b0255e04` (blob `fb5225a4`, byte-exact, sha1-locked). Fetch-back
  verification: 38/38 published files byte-identical to this host
  (commit-pinned raw). Kit mirrors saved under
  `batch8106-n005n006-ifadopted/` and `class8106-n005n006-base-control/`
  with MANIFEST-sha256.
- Verdicts NOT consumed: n005/n006 remain unconsumed closure WINs (the
  batch-12 item of the Part AD open list is CLOSED; the batch-13 4-row
  decomposition remains open for a future declaration). The standard
  11x11 empty board, the 19 central-reply roots, class 8106 (canonical
  universe untouched; 52 -> 44 unknown only under the full what-if) and
  every other class remain UNKNOWN. Nodes are not verdicts. Observed
  HEAD-before-push for this update is recorded in the commit message.

## Continuation 22 (2026-11-22, this host): batch 15 (class 5830, Part AK) declared, run, and published - WIN-HALT x2 (r001/r002), verdicts not consumed

Batch 15 target = renewed rank 13 class 5830 (mask `[4035788216077385728, 0]`,
unknown 52, groups root-49/third-59 + root-49/third-61; batch 14 = class 23101
in flight by another operator, ranks 1-12 evidence-carrying/WIN-halted/in
flight). Full protocol as AF/AC/AE: Part Y workspace regenerated from the six
pinned inputs on this host (3 runs byte-identical; closure-classes
`61943b85...` / per-root-coverage `33f01a0c...` / refresh-summary
`25987add...` / probe-worklist `1807e4d2...` all equal the published
canonical bytes, published closure-classes.csv cmp-verified), 52 keys
machine-extracted (probe_order 590-641, batch-keys.json sha256
`af3e4c46af0d84bcb248c350283b07e26b901f6e0d196038e24bd1292b133727`),
fail-safe 6/6 PASS (canonical cache 6,027 rows 0 hits, quarantine 0 both
directions, duplicate-free, rank-13 row byte-check, 12-WIN-key cross-check
0 hits from the ten published batch-keys.json files, contiguity +
class_unknown_now=52 every row), val-gate fresh 4/4 node-exact (at2m
0/2,000,000 x2; 15m 2/3,651,923 and 2/5,040,200; quads 95,670). Declaration
`0f57eef7` (note Part AK, note blob `deea536f...` after push) then scaffold
`b04969bc` (66 files fetch-back byte-identical).

Wave 1 (4 workers, 2-core host): **r001 WIN** (probe_order 590, s5_index
103560, key `[4035788216211603456, 0]`, legal 82, result 1, **2,521,302
nodes**, 2-pass fresh cold node-exact) - first key of the batch, the **13th
unconsumed closure WIN**; **r002 WIN** (probe_order 591, s5_index 103561,
key `[3603442651849818112, 128]`, legal 82, result 1, **5,973,924 nodes**,
2-pass) - the **14th unconsumed closure WIN** (third multi-WIN wave after
batch-12 n005/n006 and batch-13 p002/p003); r003 (key
`[4035788216077385729, 0]`, legal 97) and r004 (key
`[1729945206863692800, 128]`, legal 100) budget exhaustion at 15,000,000
nodes, result 0, 2-pass, honest UNKNOWN (no 15M same-condition re-search
under the stop rule). All 4 rows machine cross-checked against batch-keys
and worklist (legal, lo, hi); p1/p2 (result, nodes, budget) identical,
rc=42 never fired; RUNNER-STOP rc>=42 protocol followed; r005-r052 (48
keys) not attempted. Publications: raws+status `d1316b19`, README Result
`a35fb210`, note Part AK status update `24d4bd08`, all fetch-back
byte-identical. Batch record: 15 batches -> 12 WIN-HALT + 3 clean.

Third-implementation cross-verification of r001/r002 and the class-5830
if-adopted decomposition have NOT been declared at publication time -
check latest main for competing declarations before starting either.
Adoption of both WINs remains with the scrutiny owner (C++ second
implementation gate pin `9193f5b6...`; this host still has no compiler and
package installation is forbidden). The standard 11x11 empty board, the 19
central-reply roots, class 5830 (48 unprobed children) and every other
class remain UNKNOWN. Nodes are not verdicts.

## Continuation 23 (2026-11-22, this host): Part AJ joint unconsumed if-adopted decomposition completed and published

- Resumed from continuation 22 (batch 15 Part AK was run and published by
  the parallel operator; this host stayed read-only on it). The declared
  and scaffolded Part AJ joint decomposition (note commit `8d5cb672`,
  scaffold `978634cf`) was executed and published as
  `research/experiments/n11-centralreply-joint-unconsumed-ifadopted-20261122/`
  (commit `7704f5c3`, 26 files, fetch-back sha256 26/26 byte-identical;
  the three 3.7MB scenario probe-worklists are regenerable from the
  published scripts and were not republished, Part AH precedent).
- Host environment resets destroyed /home/user/work twice mid-run; the
  whole working set was rebuilt from commit-pinned fetches under the
  permanent kit mirror `joint10-unconsumed-ifadopted/` BEFORE publication,
  with all fail-closed gates re-run PASS and every byte-sha matching the
  pre-reset run (lesson recorded: work lives under knowledge/, commands
  stay <= 240s).
- Honest correction published by the maker's own fail-closed gate: the
  first increment run ABORTed (b001 already inside the canonical BASE
  6,027-row cache). Precise re-measurement found exactly 19 batch-1 LOSS
  rows (b001..b017, b019, b020) already in BASE with identical verdicts
  AND node counts; batch-1's WIN b018 is NOT in BASE; the other eight
  batches have zero BASE overlap; no verdict conflicts anywhere. Those
  19 rows are excluded as pre-consumed duplicates (verdict+node identity
  gate, stricter than the declared 0-hit expectation; the declaration
  numbers JLOSS141/JALL151 were planning quantities). Packet: 151 probed
  rows -> **132 unique-new = 10 WIN + 122 LOSS** (JWIN10 `fe2c6f68...` /
  JLOSS122 `e5fe80af...` / JALL132 `cc841d6e...`); h002 (batch-8, 15M
  exhaustion result 0) stays excluded with its exhaustion shape
  gate-checked and its re-search still forbidden.
- Scenario caches (published union merger pin `90711961...`, selftest
  PASS, WIN/LOSS conflicts 0, duplicates 0): JWIN10 6,037 rows
  `7881724a...`, JLOSS122 6,149 `d80ee94b...`, JALL132 6,159
  `13bfec6e...`, each with a merge audit. Refresh scripts are
  diff-verified 4-hunk adaptations of the pinned Part Y script
  (`88671526...`), 2 runs per scenario, 6/6 byte-identical; per-root
  free coverage identical to BASE on every root; root first=27 keeps
  119/119 free thirds in all four runs.
- Deltas (`compare_deltas_joint10.py` -> `decomp-deltas-joint10.json`
  `24b5aa11...`; all recomputed class_status_counts asserted equal to the
  published BASE+scenario summaries before reporting; Board fail-closed
  free verification re-executed per scenario):
  - JWIN10: excluded_now 23 -> **53** (+30), unknown 34,501 -> 34,471;
    the flip set is machine-identical to the frozen-graph valid holder
    union of the ten WIN S5 children; only class 8106 is a multi-WIN
    holder (n005+n006); update8 win_hit_groups 0 -> 29; free_now stays
    35; root27 stays 119/119.
  - JLOSS122: ZERO flips (excluded_now 23, free_now 35, unknown 34,501);
    update8 resolved 75 -> 163 (+88 of the 122 rows are frozen-baseline
    requirements), remaining 31,784 -> 31,696; joint greedy 35,242 ->
    36,201; probe worklist 65,154 -> 65,011.
  - JALL132: excluded_now 53 / unknown 34,471 (identical to JWIN10);
    update8 resolved 75 -> 171 (+96), remaining -> 31,442, joint greedy
    -> 36,193, worklist -> 64,996; the nine batch-class unknown deltas
    are additive (full == WIN + LOSS for every class); update8 remaining
    and joint greedy deltas are honestly NONadditive (WIN hits drop
    whole planned groups while LOSS rows resolve single requirements);
    greedy nonadditive roots (0, 14, 49) recorded, not gated away.
- Verdicts NOT consumed: the ten WINs remain hypothetical adoptions
  pending the scrutiny owner (C++ second-implementation gate pin
  `9193f5b6...`; third-implementation verdict-level cross-verification
  already published for all ten, Parts G/H/K/O/P/T/W/AA/AD/AG). The 122
  LOSS rows remain unconsumed published evidence outside the canonical
  cache. Batch-13 (Part AI) and batch-14 (Part AF) scopes untouched
  (read-only). The standard 11x11 empty board, the 19 central-reply
  roots, the unprobed children of the nine batch classes and every
  other class remain UNKNOWN. Nodes are not verdicts. Observed
  HEAD-before-push for the experiment push: `5d745781`; note Part AJ
  publication status update pushed as `17e3619f` (blob sha1-locked
  `65e74c00`, fetch-back byte-identical).

## Continuation 24 (2026-11-22, this host): Part AL batch-15 r001/r002 third-implementation cross-verification completed and published - verdict-level agreement on both WINs, 51/51 gates, verdicts NOT consumed

Following the Part G/K/O/P/T/W/AA/AD/AG convention, the 13th/14th unconsumed
closure WINs from batch 15 (class 5830, r001 `[4035788216211603456, 0]` /
r002 `[3603442651849818112, 128]`, both legal 82, published raws `d1316b19`)
were re-solved with the pinned third implementation (non-df-pn AND/OR
minimax `third_impl.js` `08ea958f...`). Declaration pushed first (Part AL,
note commit `ef863117`, observed HEAD-before-push `cf485460`, conflicting
declaration check clean), then executed on this host
(`135c7b39-6dfa-4499-9038-092e9efeed37`, 2 cores, at most 2 concurrent
solver processes).

- Machine-derived inputs only: `make_inputs_batch15.py` (adapted from the
  published Part AG batch-13 script) re-derives every input from the
  published batch-15 raws (per-row 2-pass node-exact asserted), the
  published `batch-keys.json` (sha256 `af3e4c46...`, class 5830, 52 keys),
  the published declaring-host status.log (PASS lines asserted,
  r003/r004 exhaustion rows asserted result 0, WIN-HALT stop lines
  asserted) and the published per-key input CSVs (scaffold `b04969bc`,
  derived-vs-published byte-identical). Zero hand transcription.
- Gates: verify_tbl quads 95,670 == replica, 195,044 randomized triples
  mismatches 0; anchors k02a (WIN, legal 87, 9,106,337/4,991,527) and l1a
  (LOSS, legal 116, 7,660,602/3,951,175) reproduced the published
  third-impl values exactly, a/b deterministic; negatives ng1 (legal+1)
  and ng2 (stones 6) both GATE_FAIL as designed; honest runner note: the
  serial `&&` negative pair short-circuits after ng1's intentional rc=1,
  so ng2 was launched immediately after the runner with the identical
  pinned script and its row recorded in status.log (README documents it).
- **Results (cap 300M, wallcap 240s, memo-power 22, 1 row x 2 runs):**
  r001 third-impl result 1 WIN, 2,856,756 expansions / 1,684,754 ttHits,
  clean, a/b identical (walls 17.34/17.47s); r002 result 1 WIN,
  6,817,094 / 4,153,893, clean, a/b identical (walls 42.37/42.85s). Both
  agree with the published replica verdicts (WIN at 15M). Wall-inconclusive
  0, divergence 0. Audit battery 51/51 gates PASS, run twice with
  byte-identical output (audit-summary.json sha256 `c008d74b...`,
  schema `batch15-wins-thirdimpl-audit-v1`).
- r003/r004 (15M exhaustion, honest UNKNOWN) were NOT re-searched (a
  third-impl re-search would be a budget escalation requiring a new
  declaration); r005-r052 (48 keys) remain untouched. Batch-13 (Part AI),
  batch-14 (Part AF) and Part AJ files stayed read-only throughout. No
  canonical cache was modified.
- Publications: experiment dir
  `n11-centralreply-closure-batch15-wins-thirdimpl-20261122/` 29 files
  (with MANIFEST-sha256.txt) commit `ca7ad4fc`, fetch-back 29/29
  byte-identical; note Part AL status update commit `dbd57fb2` (blob
  sha1 `b86f2373`, fetch-back byte-identical).
- Adoption of both WINs remains with the scrutiny owner (C++ second
  implementation gate pin `9193f5b6...`; this host still has no compiler
  and package installation is forbidden). The standard 11x11 empty
  board, the 19 central-reply roots, class 5830 (48 unprobed children)
  and every other class remain UNKNOWN. Nodes are not verdicts.


## Continuation 25 (2026-11-22, this host): Part AI batch-13 (class 16930) if-adopted decomposition PUBLISHED under takeover - 28/28 fetch-back byte-identical, verdicts NOT consumed

The batch-13 declaring host (Part AI, note amendment `a0cdb0da` at
2026-11-22T13:08Z) stayed silent for 2h+ with no status update, no
experiment directory and no kit evidence on main (absent at observed HEADs
`858a4158` 15:18Z and `ada9bc95` 15:25Z), so this session executed the
published declaration under the same Part U / Part Z takeover convention.
No conflicting declaration existed; nothing in the declaration was changed.

- All computation gates PASS on this host: published batch-13 sources
  re-verified 10/10 byte-identical (8 raws + status.log + batch-keys
  `c6c56a1a...` at `858a4158`); BASE control refresh re-executed twice,
  byte-identical to the published Part Y canonical on all four outputs
  (fifth independent cross-host reproduction); increments maker twice
  byte-identical (`bb238f67...` / `50c09a06...` / `3a8bcb11...`;
  3-way p1/p2/status node-exact, BASE overlap 0, quarantine 0, WIN set
  exactly {p002,p003}); sha-pinned union merges 6,029/6,029/6,031 rows,
  conflicts 0 (`c180e6d6...` / `ac7b6cdd...` / `faacb374...`);
  three scenario refreshes twice each, 6/6 byte-identical (honest note: the
  first concurrent launch was OOM-killed, all final runs serial); delta
  extractor twice byte-identical (`c62cabb4...`) with fail-closed
  recompute gates against BASE and all published scenario summaries.
- Machine-measured decomposition: PWIN2 excluded_now 23->28, flips
  {4903, 5471, 5513, 5626, 16930} (= the frozen-graph eligible holder
  union of the two WIN S5 children; only multi-WIN holder = 16930),
  unknown 34,501->34,496, class 16930 closure rank 11->5 (unknown 52->50);
  PLOSS2 zero flips, probe worklist 65,154->65,152; PFULL4 worklist
  65,150 (additive) and update8 unchanged in every scenario (resolved 75,
  remaining 31,784, win_hit_groups 0 - batch-13 is update8-neutral);
  free_now 35 and per-root free coverage unchanged everywhere, root 27
  stays 119/119; joint greedy 35,242 unchanged, per-root greedy roots
  26/48 move -2/-2/-4 additively.
- Publications: experiment dir
  `n11-centralreply-class16930-win-p002p003-ifadopted-20261122/` 28 files
  (with MANIFEST-sha256.txt) pushed as commit `79a7f72d` (15:34:45Z),
  fetch-back 28/28 byte-identical including the three ~247KB scenario
  caches; scenario probe-worklists not published per Part AH precedent
  (sha256s recorded in the experiment README); note Part AI status update
  appended to the single-owner note in the same session.
- Verdicts NOT consumed: p002/p003 remain hypothetical adoptions pending
  the scrutiny owner (C++ second-implementation gate pin
  `9193f5b6...`), p001/p004 LOSS rows remain unconsumed published
  evidence outside the canonical cache. p005-p052 (48 keys) unprobed.
  The standard 11x11 empty board, the 19 central-reply roots, class
  16930 and every other class remain UNKNOWN. Nodes are not verdicts.

## Continuation 26: Part AN batch-15 (class 5830) r001/r002 if-adopted decomposition published under its own declaration

Executed the Part AN declaration (commit `d94b4ff0` 15:41:57Z, observed
HEAD-before-push `953ae601`) on this host; no counter-declaration existed
and no takeover was needed (declaring host = this session).

- Single-scenario structure: batch-15 has zero resolved LOSS rows
  (r003/r004 are 15M budget-exhaustion rows, result 0, nodes==budget,
  honest UNKNOWN, type-gated out of every increment), so PWIN2 is also
  the full-packet scenario - machine-asserted in the increments manifest
  (row_counts losses 0, full_packet_eq_win_only true).
- All gates PASS: increments maker 2x byte-identical (2 WIN rows,
  `05c10e1f...`); sha-pinned s5_union_merge (`90711961...`, selftest
  PASS) 2x byte-identical (6,029 rows, WIN160/LOSS5,869,
  `51693301...`); scenario refresh 2x serial (66s/61s; single-process
  after the batch-13 concurrent OOM lesson), 3 outputs byte-identical
  (`496f3761...`/`37223c04...`/`f4256c28...`); delta extractor 3x
  byte-identical (`e67df758...`) with fail-closed recompute gates
  (class_status_counts re-executed from graph+update8+cache and asserted
  equal to the published summaries for BASE and PWIN2).
- Machine-measured decomposition: the flip is NOT the batch's own class -
  class 5830 was ALREADY excluded_now at BASE (5 pre-existing WIN cost
  children among 57); adopting r001/r002 newly excludes exactly side
  class 2634 ({2634} == eligible holder union). excluded_now 23->24,
  unknown 34,501->34,500, free_now 35 unchanged; class 5830 unknown_now
  52->50 and class 2634 51->49 (own membership delta 2 each).
  batch-keys membership_class_count (1) is closure-scoped vs the
  frozen-graph holder sets {2634, 5830} which drive the flips - both
  recorded per key in the delta output (scope distinction first made
  explicit here; batch-13 holders happened to match membership counts).
- update8 moves forward (unlike update8-neutral batch-13): r001/r002
  (s5 103560/103561) are frozen baseline requirements - resolved 75->77,
  remaining 31,784->31,734, win_hit_groups 0->1 (first win-hit group is
  s4 class 2634 on the root-first-49/third-71 group).
- Scheduling: joint greedy 35,242->35,240, probe worklist 65,154->65,150,
  root 27 stays 119/119, per-root free coverage columns unchanged on
  every root, the only individual_greedy_union mover is root first 49
  (2,890->2,888).
- Publications: experiment dir
  `n11-centralreply-class5830-win-r001r002-ifadopted-20261122/` 14 files
  (README + MANIFEST-sha256.txt) pushed as commit `c37b2790`
  (15:49:30Z), fetch-back 14/14 byte-identical including the ~247KB
  scenario cache; probe-worklist not published per Part AH precedent
  (sha256 in the experiment README); note Part AN status update
  appended as commit `138795ce`.
- Verdicts NOT consumed: r001/r002 remain hypothetical adoptions pending
  the scrutiny owner (C++ second-implementation gate pin
  `9193f5b6...`); r003/r004 are honest UNKNOWN and must not be read as
  verdicts; r005-r052 (48 keys) unprobed. The standard 11x11 empty
  board, the 19 central-reply roots, class 5830 and every other class
  remain UNKNOWN. Nodes are not verdicts.


## Continuation 27 (2026-11-22, this host): batch 16 (class 10687, Part AM) declared, executed, and published - 52/52 all LOSS, the fourth clean all-LOSS batch

Executed the Part AM declaration (commit `4386ace3`, observed
HEAD-before-push `1976f566`) on this host. Renewed closure ranks 1-13 were
all evidence-carrying, WIN-halted or in flight (5830 = batch-15 r001/r002,
23101 = batch-14 in flight by the Part AF owner), so the first clean
candidate was renewed rank 14, class 10687 (mask `[1224979098661617664, 0]`,
unknown 52, groups (16,56)+(16,64)), 52 keys, probe_order 642-693.

- Pre-declaration failsafes 6/6 PASS: 0 hits in the 6,027-row canonical
  merged cache (`95e868d6...`), 0 quarantine hits (`81d23160...`), no
  in-batch duplicates, closure-classes rank-14 row byte-checked (`61943b85...`),
  zero overlap with the 608 published batch 1-15 keys, contiguous
  probe_order. The Part Y refresh was re-executed on this host from the
  pinned 6 inputs before extraction and reproduced the published canonical
  outputs byte-identically (4th recorded reproduction); val-gate fresh
  4/4 node-exact immediately before the run.
- Result: **52/52 keys all LOSS (result 2)**, 2-pass fresh-cold node-exact
  on every key, WIN 0, exhaustion 0, determinism mismatch 0; total
  168,262,885 nodes per pass; per-row machine cross-check vs batch-keys in
  row-audit.json (schema `n11-centralreply-closure-class10687-batch16-rowaudit-v1`,
  `589c1141...`), batch-keys sha256 `465cf44721a661ce94babeb12...` (full value
  in the experiment README and MANIFEST).
- Host events, honestly recorded: repeated environment resets killed the
  background runner mid-batch (15:15Z truncated t002.p2/t003.p2; 15:27Z
  truncated t020.p2/t022.p1; 15:32Z truncated t020.p2/t022.p1/t023.p1/t024.p1;
  plus the ~15:31Z `/home/user/work` wipe - the knowledge kit checkpoint held
  the authoritative state). A `# replay_done` completeness guard was
  installed in `runbatch.sh` BEFORE any re-run, and the final 7 waves were
  executed as foreground single-wave invocations (`scripts/runwave.sh`).
  No stop rule ever fired; all 8 truncated fragments (no verdict lines) are
  published under `output/raw-truncated-hostevent/` for transparency. The
  batch has zero exhaustion rows and no complete row was ever re-run, so
  the truncated passes' fresh-cold re-runs are not same-condition
  re-searches of any resolved row (stated in the README).
- Publications: experiment dir
  `n11-centralreply-closure-class10687-batch16-20261122/` - 180 files in
  3 commits (scaffold `14092b5e`, results `0aac7e0c`,
  README+row-audit+MANIFEST `d349e8f8`), fetch-back 180/180 byte-identical
  against MANIFEST-sha256.txt at the publication commit. runner.log kept
  internal (kit-mirrored). Note Part AM status update appended as commit
  `7711aab9` (blob sha1 lock `f36db386...` -> `fefd11c8...`, byte-count
  gate 142,517 chars passed before push).
- Closure candidate, verdicts NOT consumed: the fourth clean all-LOSS
  batch overall (after 23963, 8784, 10324). The 52 LOSS rows only become
  consumable through the sha-pinned fail-closed union merger (`90711961...`)
  as a published increment plus an independent refresh re-audit - a
  separate declaration (Part AP-equivalent) that must first re-check
  ranks 1-13 (batch-15 if-adopted is now published as Part AN `c37b2790`;
  batch-14 23101 still in flight). No root coverage, no class closure, no
  third-move secured is claimed by this batch. The 14 unconsumed closure
  WINs (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/
  r001/r002) remain third-implementation cross-verified and await the
  scrutiny owner (C++ second-implementation gate pin `9193f5b6...`). The
  standard 11x11 empty board, the 19 central-reply roots, class 10687 and
  every other class remain UNKNOWN. Nodes are not verdicts.


Addendum to Continuation 27: publication erratum. The experiment README's
precedent tally sentence originally read "(the 16th batch overall: 13
WIN-HALT + 3 clean all-LOSS precede it)"; machine re-check of the published
batch records showed batch-14 (class 23101) is declared but
result-unpublished (its output/ directory carries no results), so the
completed precedent record is 11 WIN-HALT + 3 clean in 14 batches. Corrected
in place by erratum commit `572dcbc3` (README + updated MANIFEST-sha256.txt,
fetch-back 180/180 byte-identical at that commit). Batch-16 remains the
fourth clean all-LOSS batch; no verdict, count or claim of the batch itself
is affected. The note Part AM status update carries no tally sentence and
needed no correction.


## Continuation 28 (2026-11-22, this host): Part AO batch-16 (class 10687) 52-row all-LOSS if-adopted decomposition published - PLOSS52 single scenario, fetch-back 16/16, verdicts NOT consumed

Part AO (declared as note amendment `ede3eb42`, observed HEAD-before-push
`6af95d9c`, no counter-declaration) is complete. The single scenario
PLOSS52 = BASE (canonical 6,027-row cache `95e868d6...`) + all 52 LOSS
rows of batch-16 was computed with the doubled-run discipline: increments
maker twice byte-identical (52 rows, `95345a5b...`), sha-pinned union
merger (`90711961...`, selftest PASS) twice byte-identical (6,079 rows,
WIN 158 / LOSS 5,921, conflicts 0, `342e8683...`), scenario refresh twice
serial (~60 s each; all 4 outputs byte-identical:
`7fd15927...` / `7405699e...` / `ec52a56d...` / worklist `3b28ba59...`,
the worklist itself unpublished per Part AH precedent), delta extractor
three times byte-identical (`dd6a01ef...`). The extractor re-executes the
published refresh class pass (including Board fail-closed child
verification of every free candidate) and asserts class_status_counts,
known-universe and per-root free-coverage equality against the published
BASE and PLOSS52 summaries before emitting any delta.

Published as one commit `5a5e56d8`: 16 files under
`research/experiments/n11-centralreply-class10687-loss52-ifadopted-20261122/`
(scripts 4, output 6 incl. the scenario cache and delta JSON, loss52
refresh outputs 3, README, status.log, MANIFEST-sha256.txt), fetch-back
16/16 byte-identical. Note Part AO status update appended as `e762457e`
(blob sha1 lock `059ba5aa...` -> `7b14c2ac...`, fetch-back
byte-identical, Part AQ declaration section untouched).

Machine-measured deltas (scheduling only, no verdict consumed):
- Zero flips: a zero-WIN increment can only free. Transition ledger:
  excluded 390 / excluded_now 23 / free_now 35 all unchanged,
  unknown->free_now exactly 1 (class 10687), unknown->unknown 34,500.
- Class 10687 becomes a Board-verified what-if free candidate
  (free_now 35->36 projection; NOT a closure claim). Its 52 BASE-unknown
  cost children are machine-checked to be exactly the 52 increment keys;
  every one of the 143 graph holder classes satisfies
  scenario_unknown_now == BASE unknown_now - own increment membership
  (class 10661 53->52, class 10695 own 2).
- Newly free thirds {(root 16, third 56), (root 16, third 64)} are
  machine-identical to the batch's groups_served_full; the (central,16)
  row is the only changed per-root coverage row (free 14->16, uncovered
  105->103, free+uncovered==119 held); root 27 baseline stays 119/119.
- update8 advances by exactly one requirement (s5 376421): resolved
  75->76, remaining 31,784->31,783, win_hit_groups 0 unchanged.
- Scheduling quantities: joint greedy 35,242->38,522 (heuristic
  re-selection after two groups left the non-free set; NOT a coverage
  regression), probe worklist 65,154->65,097 (-57), closure candidate
  table 811->810 rows (class 10687 machine-checked absent); the rank-14
  row passes to class 10661 (mask `[1152921505697431552, 0]`, unknown
  52, (24,30)-range groups) - the machine-identified next all-LOSS
  batch candidate.

Erratum recorded: Continuation 27's batch-keys sha abbreviation
`465cf44721a661ce94babeb12...` is a transcription slip; the correct full
value is
`465cf44721a661ce94babe12212c26c697ebb346392548fcdafaa9d3e8c3dd4e`.
The full value was already correctly published in the batch-16
README/MANIFEST and the Part AM note status; no claim or cross-check was
affected. (Found by machine grep while preparing this continuation; the
Part AO note status update carries the same record.)

Operational standard confirmed this round: publication fetch-back over
the public repo is fastest and most reliable via bash curl to
commit-pinned raw.githubusercontent.com URLs (<commit-sha>/<path>) with
sha256sum comparison against the pushed MANIFEST/local files; the
sandbox connector path still rate-limits under parallel loads, and
main-ref raw URLs can serve CDN-stale bytes - always pin the publication
commit sha.

Not touched: batch-14 (Part AQ takeover session, in flight), batch-15
(Part AN), all published raws. The 14 unconsumed closure WINs still
await the scrutiny owner (C++ gate pin `9193f5b6...`). Class 10687 is
NOT closed: consumption of the 52 LOSS rows still requires a fresh
declaration (Part AP-equivalent: canonical increment + refresh re-run +
independent audit), and the closure candidate table must be re-read
from the latest main before selecting any next batch (batch-14 and
batch-17 candidates compete). The standard 11x11 empty board, the 19
central-reply roots, class 10687 and every other class remain UNKNOWN;
nodes are bookkeeping, never verdicts.

## Continuation 29 (2026-11-22, this host): Part AP concluded and recorded - batch-16 52 LOSS rows canonically adopted, reaudit published, class 10687 closure-qualified under the canonical classification; verdicts unchanged

This continuation closed the record-keeping remainder of Part AP (declared
`815391db`, observed HEAD-before-push `a71bef64`). The canonical adoption
and reaudit products themselves were published in the previous leg
(commit `cd00857d` single-file canonical reaudit cache + commit
`20deb45d` reaudit experiment 13 files, both fetch-back
byte-identical at that commit); no computation was re-run here.

- Note Part AP status update published: note blob sha1 `34d4c759...` ->
  `7bb7a66d8f6d2a7bc9a1a88f6c57e845f7fe66a0`, insert-only (inserted
  between the Part AP declaration section end and the Part AQ section
  start, needle count machine-verified == 1), note 153,203 -> 157,722
  chars, fetch-back byte-identical against the pushed content
  (commit `be6f50df`). Observed HEAD-before-push `9e4ffca9`: main had
  moved past `20deb45d` via other-lane commits during the record-keeping
  gap, but the note itself was untouched; the note blob sha1 lock
  reconfirmed `34d4c759...` and the insertion applied cleanly under the
  create_or_update sha guard. Execution-environment instability
  (temporary unavailability of the local bash/file tools) forced the
  whole fetch -> needle-check -> push -> fetch-back chain to run in the
  connector sandbox instead of the local workspace; verification used
  in-memory string equality against the freshly fetched resource text
  (byte-equivalent for this ASCII+JA payload, length 157,722 == pushed
  length).
- Recorded Part AP machine results (from the execution leg, all
  fetch-back byte-verified there): canonical reaudit cache 6,079 rows
  (WIN 158 / LOSS 5,921, 249,622 bytes), sha256
  `342e86838e0c2bef915798059cb397f7c91e59c65426bf74db19530ecdd7979e`,
  byte-identical to the Part AO scenario cache (cmp); increments maker
  re-derivation byte-equal to the published increment `95345a5b...` /
  manifest `28c90ba7...`; merger 2x byte-identical, conflicts 0,
  duplicates 0, merge-audit run1 == run2; adoption refresh 2x serial
  byte-identical with the 3 CSV outputs byte-equal to the Part AO
  outputs and refresh-summary `b278f822...` differing from the Part AO
  summary `7fd15927...` ONLY in `pins.merged_cache.path`; adoption delta
  extractor 3x byte-identical, all gates PASS, output `70c1b31e...`
  differing from the Part AO delta JSON `dd6a01ef...` only in the three
  caption columns + pins.scenario_summary_sha256 (delta values
  byte-identical).
- Canonical consequences recorded: **class 10687 closure-qualified under
  the canonical classification** (Board fail-closed free verification
  free_candidates 36 / board_verified_free 36 / rejected {}; free_now
  35 -> 36; unknown 34,500; closure-classes table 811 -> 810 rows with
  class 10687 absent; per-root change only (central, first=16): free
  14 -> 16, uncovered 105 -> 103, free+uncovered==119 held; root 16
  secures the 2 groups {(16,56),(16,64)}; root 27 baseline 119/119;
  update8 resolved 75 -> 76 (s5 376421), remaining 31,783, win-hit
  groups 0; joint greedy re-selection 38,522, scheduling only). Rank 14
  passes to class 10661 (`[1152921505697431552, 0]`, unknown 52) = the
  machine-identified batch-17 candidate.
- Consumed: exactly the 52 batch-16 LOSS rows (canonical classification).
  No WIN row was adopted: the 14 unconsumed closure WINs
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002)
  remain scrutiny-owner-blocked (C++ second-implementation gate pin
  `9193f5b6...`).
- Honesty record: the standard 11x11 empty board, the 19 central-reply
  roots and every class verdict remain UNKNOWN throughout; free_now /
  closure qualification is canonical classification status, never a
  win/loss claim; nodes/budgets/gates are never verdicts. Open items:
  batch-17 declaration (class 10661) after a fresh main re-read,
  Part AQ (batch-14 takeover, in flight by its owner) untouched,
  knowledge-base entry update for Part AP completion (local).


## Continuation 30 (2026-11-22, this host): Part AQ batch-14 (class 23101) completed under takeover - WIN-HALT at q042, the 15th unconsumed closure WIN, verdicts NOT consumed

Takeover provenance and publication (all byte-verified):

- takeover basis: Part AF declared 2026-11-22T12:26:47Z (scaffold `54b7453d`)
  and never published a row or status line; 3h40m silence far exceeds the
  20-minute batch 8/11 criterion; no declaring-host rows existed in any
  mirror (nothing to rescue). Declared in the note as Part AQ (commit
  `398a96ae`, observed HEAD-before-push `ede3eb42`), with the Part AF
  pre-registered protocol taken over unchanged (2-pass fresh cold, budget
  15M, mismatch HARD-STOP rc=42, WIN-HALT rc=45, in-flight wave members
  disclosed complete, 4-key waves).
- pre-execution verification on this host (all PASS): published scaffold
  65/65 byte-identical to the kit mirror; jsreplay pin
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`;
  fail-safes (1)-(6): 52/52 keys absent from the then-canonical 6,027-row
  cache `95e868d6...`, quarantine (active 2) 0 hits both directions,
  duplicate-free, closure-classes rank-12 row byte-agreement, 12
  unconsumed WIN keys 0 hits (lo/hi re-extracted from published batch
  raws), probe_order 538-589 == worklist 65,154 rows `1807e4d2...` with
  lo/hi/legal/s5_index agreement vs batch-keys `dfde0e90...`; val-gate
  4/4 node-exact fresh (at2m 0/2,000,000 twice; 15m 2/3,651,923 and
  2/5,040,200), takeover outputs saved as `*.takeover-aq.out`.
- execution result: **WIN-HALT at q042 (probe_order 579, s5_index 745184,
  key `[1152921505747697664, 1032]`, legal 85): result 1 WIN, 9,149,084
  nodes, 2-pass fresh-cold node-exact.** Same-wave q039/q040/q041 disclosed
  complete LOSS (2,502,014 / 2,175,857 / 2,514,109 nodes). 42 probed =
  41 LOSS + 1 WIN, exhaustion 0, mismatch 0, 88,338,850 nodes/pass.
  q043-q052 (10 keys) not started per the halt rule. No truncation on this
  host (all 84 raws carry the `# replay_done` trailer; the takeover wave
  wrapper `scripts/runwave-aq.sh` was introduced with that completeness
  guard and WAVE-START/WAVE-END logging).
- machine row audit `output/row-audit.json` (schema
  `n11-centralreply-closure-class23101-batch14-rowaudit-takeover-v1`,
  sha256 `cc22a1c8...`): all 42 rows two-pass node-exact, key/legal/
  probe_order agreement, 95,670 quadruple gate both passes, status.log
  cross-check, problems empty.
- publication: 156 files in 4 commits (raws q001-q021 `21affe23`, raws
  q022-q042 `d064e3aa`, status+audit+val-gate+runner `4cf1d248`, README
  Takeover/Result + MANIFEST `7b211d38`), fetch-back 156/156 byte-exact
  against the MANIFEST at the publication commit; kit mirror byte-equal.
  Note Part AQ status update `eaccb0b4` (note blob
  `a4cd1465...`, fetch-back byte-identical).
- honesty record: the parallel lane completed Part AO (`5a5e56d8`) and
  Part AP (canonical 6,027 -> 6,079 rows `342e8683...`, class 10687
  closure-qualified) during this takeover; zero writes to their scope.
  All 52 batch-14 keys re-checked absent from the new 6,079-row canonical
  cache (0 hits, including q042).
- verdict guards (unchanged): q042 is the 15th unconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002
  /q042), scrutiny-owner-blocked (C++ second-implementation gate pin
  `9193f5b6...`). The all-52-children-LOSS closure route for class 23101
  is refuted by a verified WIN child (verdict-level route statement
  only). Batch tally: 15 batches -> 12 WIN-HALT + 3 clean. The standard
  11x11 empty board, the 19 central-reply roots, class 23101 and its S5
  children remain UNKNOWN throughout; nodes are not verdicts.
- open items (re-read latest main before starting): (a) q042
  third-implementation cross-verification (Part G/K/O/P/T/W/AA/AD
  protocol, anchors 2 + negatives 2, rules gate), (b) q042 single-WIN
  if-adopted decomposition (Part V/R/AB/AH/AI/AN flow), (c) 41 LOSS rows
  canonical adoption + reaudit (Part AP flow, increments built against
  the new 6,079-row canonical), (d) batch-17 declaration (class 10661
  per the Part AP reaudit, machine-identified next clean candidate).

## Continuation 31 (2026-11-22, this host): Part AR batch-14 q042 third-implementation cross-verification completed and published - 4/4 verdict agreement WIN=1 LOSS=3 cross-host; verdicts NOT consumed

Declared in the note as Part AR (commit `e640f5b6`, observed
HEAD-before-push `a54a9402`, note blob lock `a4cd1465...`; no
counter-declaration observed). Scope: the batch-14 WIN-HALT row q042 plus
its same-wave disclosed LOSS rows q039/q040/q041, re-solved with the pinned
third implementation (non-df-pn AND/OR minimax `third_impl.js`, sha256
`08ea958f...`, same Part G/K/O/P/T/W/AA/AD/AG/AL protocol).

Execution (all gates fail-closed, all PASS):

- Input derivation: `make_inputs_batch14.py` (adapted from the published
  batch-15 Part AL script, sha256 `19c442d1...`) re-derives everything
  from the published batch-14 takeovers (publication commit `7b211d38`:
  q039-q042 p1/p2 raws 8, status.log, batch-keys `dfde0e90...`, per-key
  input CSVs), asserting 2-pass node-exactness, the `q042 WIN-HALT` and
  WAVE-END stop=1 lines, RUNNER-START presence, derived-vs-published CSV
  byte equality and class_index 23101. First invocation ABORTed on a
  q042 PASS-row parse bug (`toks[3]` index), fixed and re-run clean.
- Prerequisite gates: rules gate (replica quads 95,670 == third-impl
  quads 95,670; 195,044 randomized triples, TBL mismatches 0); script
  pins 3/3; anchors node-exact on this host (k02a WIN 9,106,337
  expansions / 4,991,527 ttHits; l1a LOSS 7,660,602 / 3,951,175 - both
  exactly the published values); negatives ng1 (legal+1: 88 vs derived
  87) and ng2 (stones 6 vs 5) both GATE_FAIL with the exact expected
  wording, rc=1.
- Results (1 row = 1 solver = 1 process, cap 300M, wallcap 240s,
  --memo-power=22, every row run twice a/b, all a/b deterministic clean):
  q042 **WIN** 10,728,035 expansions / 5,758,042 ttHits (a 65.14s /
  b 64.78s); q039 / q040 / q041 **LOSS** 2,828,518 / 2,425,671 /
  2,843,397 expansions (ttHits 1,663,204 / 1,519,018 / 1,693,916).
  **4/4 verdict agreement with the takeover replica (jsreplay df-pn
  family), executed on a different sandbox host: cross-host
  cross-implementation corroboration. Wall-inconclusive 0, divergence
  0.** Node counts differ across implementations as expected; only
  verdicts are cross-checked.
- Verdict-level route statement: the class 23101 all-52-children-LOSS
  closure route is refuted by a two-implementation-agreed WIN child
  (q042). Verdicts NOT consumed: q042 stays the 15th unconsumed closure
  WIN (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/
  r001/r002/q042), scrutiny owner (C++ second-implementation gate pin
  `9193f5b6...`) unchanged.
- Audit battery: batch-14-adapted `audit.py` (schema
  `n11-centralreply-closure-batch14-q042-thirdimpl-audit-v1`, sha256
  `4bb6266b...`): **71/71 gates PASS, two runs byte-identical**
  (output/audit-summary.json sha256 `18125d63...`).
- Publication (49 files, 5 commits, no branch/PR): sources+input
  `5ad33735` (23) -> transcription-slip fix `335fc0a1` (2 slips caught
  by commit-pinned fetch-back BEFORE push: status.log q025 timestamp
  prefix, ng2 stone count) -> scripts `703840f9` (6, sha-verified copies
  of published bytes + audit.py schema transform) -> outputs
  `af79f4a1` (18; the audit-run1 trailing-quote slip was caught by the
  pre-push SHA checklist) -> README + audit-summary.json +
  MANIFEST-sha256.txt `0f69d03` (publication complete). **Fetch-back
  49/49 byte-identical at `0f69d03`** (full MANIFEST sha256 sweep via
  the public-repo commit-pinned raw curl route). Note Part AR status
  update `5993e38` (note blob `8edd32f7...` -> `1ca1bc2b...`,
  prefix byte-identical, appendix fetch-back sha256-verified).
- Runner honesty note: the first negatives invocation hit a shell cwd
  grouping bug (ng2 solver never started, "No such file or directory");
  re-invoked with absolute paths, ng1 re-ran producing a byte-identical
  GATE_FAIL row, so status.log carries a duplicated identical ng1 RUN
  line. Disclosed in the experiment README; no other deviation.
- Operational (verification workflow hardened this session):
  `github_app.get_file_contents` resource text is byte-faithful
  (verified against git blob sha1 via raw curl); pre-push pure-JS
  SHA-256 comparison of every pasted payload catches transcription
  slips before they reach main (2 caught here);
  `web_search.open_url` is byte-destructive and must never be used for
  verification; note/sessionlog appends happen in-connector as
  fetched-text + appendix + create_or_update_file sha lock.
- Honesty record: the standard 11x11 empty board, the 19 central-reply
  roots, class 23101 and all 52 batch-14 keys remain UNKNOWN throughout;
  nodes/expansions are not verdicts. Open items (re-read latest main
  first): (a) q042 single-WIN if-adopted decomposition (Part
  V/R/AB/AH/AI/AN flow), (b) 41 LOSS rows canonical adoption + reaudit
  (Part AP flow, increments against the 6,079-row canonical), (c)
  batch-17 declaration (class 10661 per the Part AP reaudit).
## Continuation 32 (2026-11-22, this host): Part AS batch-14 (class 23101) 41-LOSS canonical adoption reaudit completed and published - canonical 6,079 -> 6,120 rows; class 23101 unknown 52 -> 11, closure rank 12 -> 1 (stays UNKNOWN-status); q042 WIN NOT consumed

Declared in the note as Part AS (commit `5b6af2ed`, observed
HEAD-before-push `b394c3ca`, note blob lock `7a534356...`; no
counter-declaration observed - the only interleaved commit was the
disjoint y=13 verifier lane `7196cbd5`). Scope: adopt exactly the 41
LOSS rows (q001..q041) of batch-14 into the canonical exact-S5 verdict
cache in the Part AP form; the single WIN row q042 is NOT adopted
(full != loss, machine-asserted in the manifest).

Execution (all gates fail-closed, all PASS):

- Increment derivation: `make_increments_batch14.py` (adapt of the
  published Part AP maker `e35b545d...`) from the published batch-14
  raws (publication commit `7b211d38`, MANIFEST 144/144 byte-match):
  41-row increment sha256 `5194af93...`, manifest sha256 `8b5540f9...`
  (schema `batch14-loss41-increments-manifest-v1`, row counts
  41/0/41/0 of 42 resolved 52 probed, unadopted_win_ids == ["q042"],
  unadopted_win_s5_index 745184, full_packet_eq_loss_only false,
  win_scenario_exists true). q042's 2-pass node-exact WIN raw
  (result 1, 9,149,084 nodes) re-parsed and machine-excluded.
- Union merge: sha-pinned fail-closed merger `90711961...`
  (byte-copy pin, selftest PASS) merged the 41 rows into the Part AP
  canonical 6,079-row cache `342e8683...`: **canonical 6,120 rows
  (WIN 158 / LOSS 5,962, conflicts 0, duplicates 0), 251,466 bytes,
  sha256 `be9cb24e...`**, two runs byte-identical, merge audits
  byte-identical (`54c581ee...`). This is the repo's next canonical
  exact-S5 verdict cache.
- Adoption refresh: adapted `refresh_adoption_23101.py` (Part AP
  `ad3dc0e6...` + 3 hunks: docstring, cache path, cache-sha expectation
  machine-extracted from the cache file itself), 2 serial runs,
  4 outputs byte-identical between runs (refresh-summary `f2008e70...`,
  closure-classes `3ee1dbb6...`, per-root-coverage `527c7e9a...`,
  probe-worklist `1c96df05...`, 3.7MB unpublished, sha recorded).
- Delta extractor: `compare_deltas_batch14_adoption.py` (Part AP
  `f78f7e60...` adapted: batch-14 batch-keys schema, six-faced q042
  non-consumption gate set (increment, BASE cache, scenario cache,
  quarantine registry, BASE/scenario index_verdict, class-23101
  scenario-unknown child set), zero-WIN new-free-empty gate,
  closure-table churn observation, raw 2-pass WIN re-verification;
  all recompute gates unchanged), 3 runs byte-identical
  (`7155fdaa...`), all gates PASS, with BASE = the published Part AP
  reaudit outputs fetched at pin commit `20deb45d` and sha-verified
  (`b278f822...` / `7405699e...` / `ec52a56d...`).
- Machine-measured adoption deltas (canonical classification only):
  class 23101 unknown cost children **52 -> 11** (remaining 11 =
  unconsumed q042 s5 745184 + 10 unprobed keys 745455..745465,
  machine-matched); closure-candidate rank **12 -> 1** (unknown_now
  11); class 23101 neither frees nor excludes. free_now 36 /
  excluded_now 23 / unknown 34,500 all unchanged (transitions ledger
  all-identity, flips 0, newly free 0 - gated); per-root free coverage
  unchanged for all 19 roots (root 27 baseline 119/119); update8
  resolved 76 -> 79 (s5 707915 / 713201 / 740437, all increment-LOSS
  gated), remaining 31,783 -> 31,780, groups_free 127; closure table
  810 -> 809 rows (7 left / 6 entered, ledger churn); class 10661
  stays rank 14 (batch-17 candidate); joint greedy 38,522 -> 36,726
  (-1,796) and probe worklist 65,097 -> 64,941 (-156), both
  bookkeeping, zero coverage change.
- Publication (16 files, 3 commits, no branch/PR): canonical cache
  alone `f03809fa` (observed HEAD `7196cbd5`; 251,466-byte payload
  fully re-assembled via line-chunked reads with exact length check -
  the r9 64KB-truncation lesson holds) -> scripts + increment +
  manifest `5e579b03` -> outputs + README + status.log + MANIFEST
  `8c42e44c` (publication complete). **Fetch-back 15/15 byte-identical
  at `8c42e44c`** (commit-pinned raw curl + sha256 against every
  MANIFEST line). Note Part AS status update `6c74cefb` (note blob
  `7a534356...` -> `3c9f42f4...`, fetched-text + appendix +
  sha-locked create_or_update_file, GitHub-reported blob sha equals
  the locally computed one).
- Runner honesty note: two first-draft extractor slips (batch-keys
  groups_served_full vs groups_served_first_seen schema naming; replay
  CSV column-offset misalignment) were caught immediately by
  fail-closed gates and fixed before any output was accepted; the
  extraction then passed 3x byte-identical. No transcription sha
  incidents in this continuation.
- Verdict guards (unchanged): q042 stays the 15th unconsumed closure
  WIN (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/
  r001/r002/q042), scrutiny-owner-blocked (C++ second-implementation
  gate pin `9193f5b6...`). The 41 LOSS rows are the only verdicts
  consumed here (via the fail-closed merger).
- Honesty record: the standard 11x11 empty board, the 19 central-reply
  roots, class 23101 (now an 11-unknown-child unknown class), the 10
  unprobed keys q043-q052 and every other class remain UNKNOWN
  throughout; nodes/worklist/greedy numbers are not verdicts. Open
  items (re-read latest main first): (a) q042 single-WIN if-adopted
  decomposition (Part V/R/AB/AH/AI/AN flow, increments against the new
  6,120-row canonical `be9cb24e...`), (b) batch-17 declaration
  (class 10661, rank 14), (c) closing class 23101 via its remaining
  10 unprobed keys + the q042 adoption decision (scrutiny owner).

## Continuation 33 (2026-11-22, this host): Part AT q042 single-WIN if-adopted decomposition completed and published - flips 4 classes [23092, 23101, 23115, 23938] unknown->excluded_now on the projection, coverage provably unchanged, update8 provably unchanged; verdict NOT consumed

Declared in the note as Part AT (commit `58938933`, observed
HEAD-before-push `2f88a495`, note blob lock `9a5dfdb7...`). Part AS's
unconsumed 15th closure WIN (q042, s5_index 745184, key
`[1152921505747697664, 1032]`, 2-pass node-exact result 1, 9,149,084
nodes) decomposed as a single-row IF-ADOPTED projection against the
published canonical 6,120 rows (`be9cb24e...`): a scrutiny-owner
adoption precomputation only, adopting neither recommendation nor
rejection, consuming zero verdicts.

- Maker: `scripts/make_increment_q042_win.py` (Part AS/AP maker line
  single-WIN adapt; fixed the WAVE-END regex that could not match
  multi-key publish lines) machine-reverified the 2-pass WIN from the
  published batch-14 raws (publication commit `7b211d38`), gated
  BASE-absence (6,120 rows) and quarantine-absence, and emitted the
  single-row increment sha256 `b4958328...` + manifest sha256
  `894e9420...` (schema `batch14-q042-win-ifadopted-increment-manifest-v1`,
  ifadopted_only, canonical_cache_untouched pin `be9cb24e...`).
- Merge: sha-pinned byte-copy merger `90711961...` (selftest PASS) run
  3x byte-identical; if-adopted cache 6,121 rows (WIN 159 / LOSS 5,962),
  251,513 bytes, sha256 `1434c68b...`; merge-audit 3x byte-identical
  (`e1d11a66...`); BASE canonical reverified byte-identical after every
  merge (the projection is not the repo canonical chain).
- Refresh: adapted `reaudit/scripts/refresh_q042_ifadopted.py` (3-hunk
  adapt of the Part AS refresh `5992738d...`; sha expectation extracted
  from the cache file itself) run 2x serial, all four outputs
  byte-identical: refresh-summary `029cc3b6...`, closure-classes
  `987c4ecb...`, per-root-coverage `ec71c81b...`, probe-worklist
  `af0c28c5...` (not published, sha recorded only).
- Extractor: `scripts/compare_deltas_q042_ifadopted.py` (WIN if-adopted
  adapt of the Part AS extractor `9e885ae0...`; new gates: flips must
  equal the machine-computed BASE-unknown graph holder set of s5 745184
  (computed from the pinned graph, not hardcoded), a pure WIN adoption
  can free no class (newly-free-classes empty), can move no per-root
  free/uncovered count (0 changed rows) and create no newly free third,
  class 23101 must be among the flips with scenario-unknown exactly 10,
  canonical BASE sha pin, BASE index_verdict absence (verdict not
  consumed on main), raw 2-pass re-verification; all Part AS recompute
  gates kept) run 3x byte-identical (sha256 `8e6ce1c6...`), all gates
  PASS.
- Result (projection classification-ledger delta only): flips =
  [23092, 23101, 23115, 23938], all four unknown -> excluded_now
  (one-way: their all-LOSS closure routes are permanently refuted by the
  verified WIN child; route statement, not a closure claim);
  excluded_now 23 -> 27, unknown 34,500 -> 34,496, free_now 36
  unchanged; transitions ledger exactly those 4 + identities. Class
  23101: scenario-unknown children exactly the 10 unprobed keys
  (745455..745465); closure-candidate table 809 rows unchanged, zero
  churn, stays rank 1 unknown_now 10 (the table is a probing-worklist
  view; the flip lives in class_status_counts + the ledger).
  Coverage: per-root free/uncovered unchanged for all 19 roots (root
  27 baseline 119/119), newly free thirds [] (all gated); sole
  per-root-greedy mover root 24 (2,785 -> 2,784, bookkeeping). update8:
  resolved 79 unchanged, remaining 31,780 unchanged, groups_free 127,
  win_hit_groups [] -> []; machine-established that s5 745184 sits
  OUTSIDE the update8 baseline requirement. joint greedy 36,726 ->
  36,725, probe worklist 64,941 -> 64,940 (both bookkeeping).
- Publication (16 files, 3 commits, no branch/PR): if-adopted cache
  alone `59fe5654` (observed HEAD `58938933`; 251,513-byte payload
  fully re-assembled via line-chunked reads with exact length/eol/tail
  checks) -> scripts + increment + manifest `f0a45654` (observed HEAD
  `59fe5654`) -> outputs + README + status.log + MANIFEST `175864a5`
  (publication complete; observed HEAD `f0a45654`). **Fetch-back 15/15
  byte-identical at `175864a5`** (commit-pinned raw curl + sha256
  against every MANIFEST line). Kit mirror
  `_19root-refresh-kit/batch23101-q042-ifadopted/` (16 files, all sha
  verified, 3.6MB probe-worklist not mirrored per precedent). Note Part
  AT status update `ee3b6f73`-observed (note blob `9a5dfdb7...` ->
  `f34401cd...`, sha-locked create_or_update_file, GitHub-reported blob
  sha equals the locally computed one; fetch-back byte-identical,
  `ee3b6f73` was another lane's y13 commit recorded as the observed
  HEAD-before-push of the note update).
- Runner honesty note: one false "blob moved" gate abort (the blob-sha
  field was read from the wrong response slot; the GitHub API contents
  call confirmed the lock blob `9a5dfdb7...` was still current and the
  note untouched, after which the push proceeded with the recorded
  observed HEAD). No other incidents in this continuation.
- Verdict guards (unchanged): q042 stays the 15th unconsumed closure
  WIN (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/
  r001/r002/q042), scrutiny-owner-blocked (C++ second-implementation
  gate pin `9193f5b6...`). Zero verdicts consumed by this Part; the
  canonical cache stays 6,120 rows `be9cb24e...`.
- Honesty record: the standard 11x11 empty board, the 19 central-reply
  roots, class 23101 (projection excluded_now, on the canonical chain
  an 11-unknown-child unknown class), the 10 unprobed keys q043-q052
  and every other class remain UNKNOWN throughout; nodes/worklist/
  greedy numbers are not verdicts. Open items (re-read latest main
  first): (a) batch-17 declaration (class 10661, rank 14, unknown 52),
  (b) closing class 23101 via its remaining 10 unprobed keys + the
  q042 adoption decision (scrutiny owner), (c) any new unconsumed
  closure WIN lanes' if-adopted precomputations as they appear.

## Continuation 34 (2026-11-22, this host): Part AU batch-17 (class 10661) declared and scaffold published - the first candidate without refutation evidence, machine-verified 52-key packet u001..u052; no probe run, verdicts NOT consumed

Declared in the note as Part AU (note blob `f34401cd...` -> `14794159...`,
sha-locked create_or_update_file, observed HEAD-before-push recorded in the
commit message). Selection rationale (machine-gated): Part AS reaudit
closure-candidate rank 1 (class 23101) is in-flight (10 unprobed keys +
unconsumed q042); ranks 2-13 (16757, 20421, 16371, 30345, 12264, 5473,
2634, 8785, 1518, 8106, 16930, 5830) all hold unconsumed closure WIN cost
children (routes permanently refuted); rank 14 class 10661 (mask
`[1152921505697431552, 0]`, unknown 52 of 53 cost children, closure groups
(24,30)+(24,90), first-seen (24,30)) is the first candidate without
refutation evidence.

- Maker: `scripts/make_batch17_keys.py` (fail-closed scaffold maker, all
  gates inlined) run 3x byte-identical. Keys from the published Part AS
  reaudit probe-worklist (sha-pinned `1c96df05...`), serving_class ==
  10661, exactly 52 rows, probe_order 600..651 contiguous; key ids
  u001..u052 (batch 1-16 letters b/c/d/e/f/g/h/j/m/z/n/p/q/r/t all
  distinct); batch-keys.json sha256 `db762175...` (schema
  n11-centralreply-closure-class10661-batch17-input-v1); 52 one-line
  input CSVs byte-identical across runs.
- Gates: canonical BASE `be9cb24e...` (6,120 rows) 0/52 hits; quarantine
  0/52; canonical-safe 52/52; mask_to_index == s5_index 52/52; every
  s5_index a graph cost child of 10661; the unconsumed WIN child s5
  745184 NOT a key; overlap with batch 1..16 (813 keys, 16 sha-pinned
  batch-keys files fetched from repo raw) == 0; Board(11) legal recount
  == worklist legal 52/52 (range 72..97); published closure rank-14 row
  content match + re-derived group-best view (809 candidate rows) with
  class 10661 at rank 14 and groups {(24,30),(24,90)}.
- Honesty note: one sha transcription slip in the first maker draft
  (worklist pin 0a8329 vs 0e8329) was caught immediately by the
  fail-closed pin gate and fixed; the published Part AS status.log
  was verified to carry the correct full sha (460e8329). No other
  incidents.
- Publication: note Part AU declaration first (blob `14794159...`),
  then the scaffold as a single commit `62b60a07` (observed HEAD
  `adc4358a`; 57 files: README + status.log + MANIFEST + maker +
  batch-keys + 52 input CSVs). **Fetch-back 56/56 byte-identical at
  `62b60a07`** (commit-pinned raw curl + sha256 against every MANIFEST
  line); the note fetch-back is byte-identical too. Kit mirror
  `_19root-refresh-kit/batch10661/` (57 files, sha-verified).
- Execution protocol (pre-registered, for a later session): pinned
  replica jsreplay.js `84585617...` byte-copy, 2-pass fresh cold,
  budget 15M, 1 solver/1 row/1 process, publish=ALL, workers max 2,
  val-gate 4 anchors reproduced first; stop rules mismatch ->
  HARD-STOP rc=42, WIN -> HALT rc=45 (honest label, NOT adopted,
  verdict NOT consumed), exhaustion -> honest UNKNOWN; consumption only
  of 2-pass LOSS rows via the fail-closed merger in a separately
  declared adoption Part.
- Verdict guards (unchanged): zero verdicts consumed by this Part; the
  canonical cache stays 6,120 rows `be9cb24e...`; the 15 unconsumed
  closure WIN rows stay scrutiny-owner-blocked (C++ second-implementation
  gate pin `9193f5b6...`).
- Honesty record: the standard 11x11 empty board, the 19 central-reply
  roots, class 10661 (unknown 52 cost children) and all 52 keys remain
  UNKNOWN throughout; probe orders, legal counts and node numbers are
  not verdicts. Open items (re-read latest main first): (a) execute
  batch-17 under the declared protocol, (b) the scrutiny owner's q042
  adoption decision, (c) class 23101's remaining 10 unprobed keys.

## Continuation 35 (2026-11-22, this host): Part AU batch-17 (class 10661) executed and published under takeover - 52/52 all LOSS, the fifth clean all-LOSS batch, 17th completed batch; verdicts NOT consumed

- Re-read latest main first: the competing lane (y14) had advanced past
  `24e418a9` (observed HEAD for commit A: `c15d4813`), the batch-17
  experiment `output/` did not exist on main yet, no counter-declaration
  for the batch-17 execution scope existed (the Part AU declaration
  `adc4358a` and scaffold `62b60a07` from the parallel session were the
  only 10661 items), so this host executed under the declared protocol.
- Execution: pinned replica `jsreplay.js` (`84585617...` byte-copy)
  2-pass fresh-cold node-exact, budget 15M, max 2 workers (2-key wave).
  **52/52 keys LOSS (result 2)**, WIN 0, budget exhaustion 0, mismatch 0.
  Total nodes 196,536,452 per pass (range 1,651,860 .. 14,967,263; u031
  settled LOSS at 14,967,263 nodes, just under budget). Fifth clean
  all-LOSS batch (after 23963/10324/8784/10687); 17th completed batch.
- Pre-execution val-gate on this host: 4/4 node-exact (at2m 0/2,000,000
  twice; 15m `(2, 3651923)` / `(2, 5040200)`; forbidden-four check
  95,670).
- Host event (honesty record): 4 sandbox environment resets occurred
  mid-write; 5 pass files (u017.p2, u018.p2, u027.p2, u031.p2, u033.p2)
  were left truncated. The completeness guard detected the missing
  `# replay_done`, quarantined the fragments under
  `output/raw-truncated-hostevent/`, and re-ran exactly those passes
  fresh-cold. No fragment ever contained a verdict line; no completed row
  was ever re-searched (same failure mode as batch-16).
- row-audit.json (schema
  `n11-centralreply-closure-class10661-batch17-rowaudit-v1`, sha256
  `c19e768f...`): all 52 rows machine-re-verified from the raws
  (p1==p2 node-exact, within budget, result 2, input row match,
  status.log match). PASS.
- Runner delta disclosed: `scripts/runbatch.sh` (`f591f8c2...`) is a
  byte-copy of the published batch-16 runner plus one honest-exhaustion
  label (jsreplay exits 0 on exhaustion; the 15M exhaustion row must not
  be recorded as PASS; never fired in this batch since exhaustion was 0).
  `scripts/runwave.sh` (`8efd78c2...`) is the 2-key wave. Both pinned in
  the MANIFEST.
- Publication (4 commits, each message records observed HEAD-before-push):
  A `2e035ed7` (runner scripts + this-host val-gate outputs + merged
  execution status.log), B `2266f8c7` (raw u001..u052, 104 files),
  C `54d2b0ee` (5 host-event fragments), D `ffc09de1` (row-audit.json +
  README execution-result section + MANIFEST-sha256, 177 entries) =
  publication complete. **Fetch-back 177/177 byte-identical** against the
  publication-commit-pinned raw URLs.
- Note amendment published: Part AU status update appended to the
  single-owner note (blob sha1 lock `14794159...` -> server blob
  `e0a4f154...`, server size 249,483 bytes exactly matching the local
  composition; paged 5-read full-content transfer verified by server-side
  blob identity).
- Verdict guards (unchanged): zero verdicts consumed by this Part; the
  52 LOSS rows may only later enter an increment via the sha-pinned
  fail-closed merger (`90711961...`) in a separately declared adoption
  Part; the canonical cache stays 6,120 rows `be9cb24e...`; the 15
  unconsumed closure WIN rows stay scrutiny-owner-blocked. The standard
  11x11 empty board, the 19 central-reply roots, class 10661 and all 52
  keys remain UNKNOWN throughout; nodes, legal counts and probe orders
  are bookkeeping, never verdicts. Open items (re-read latest main first):
  (a) the batch-17 52-LOSS canonical adoption Part (if-adopted
  decomposition optional), (b) the scrutiny owner's q042 adoption
  decision, (c) class 23101's remaining 10 unprobed keys, (d) next
  batch-18 candidate selection from the latest closure-classes rank.

## Continuation 36 (2026-11-22, this host): Part AW batch-14 residual (class 23101) q043..q052 executed and published - 10/10 all LOSS, batch-14 key set fully enumerated on this lane (42 rows Part AQ + 10 rows here); verdicts NOT consumed

- Selection and declaration: latest main re-fetched first; Part AV
  (batch-17 class 10661 adoption + reaudit, declaration `340abef3`) was
  declared-before-execution and still in flight, so the non-contact open
  item (c) from Continuation 35 was taken: the 10 unprobed residual keys
  q043..q052 of batch-14 (class 23101). Part AW declared BEFORE execution
  (note amendment `da131f10`, observed HEAD `3542315d`, note blob lock
  `141a8647...`), with a pre-registered deviation from the batch-14/16/17
  protocol: WIN rows get an honest WIN-CONTINUE label and the batch
  CONTINUES (rationale declared: the class 23101 all-LOSS closure route is
  already refuted by the published q042 WIN, so halting buys no route
  information; full enumeration minimizes the class unknown count on every
  branch).
- Scaffold maker `make_residual_keys.py` (published in commit A, 3 runs
  byte-identical): fail-closed gates G1-G7 all PASS - published batch-14
  batch-keys sha `dfde0e90...` (52 keys of class 23101), residual
  {q043..q052} with probe_order 580..589 and s5_index
  {745455..745457, 745459..745465}, the unadopted q042 WIN s5 745184
  verified absent, input CSVs byte-equal to the published batch-14 files
  (per-file MANIFEST sha pins), canonical 6,120 rows `be9cb24e...` 0/10
  hits, quarantine `81d23160...` 0/10, batch-17 batch-keys `db762175...`
  s5-disjoint, published batch-14 row-audit `cc22a1c8...` probed set
  {q001..q042} + its machine-recorded unprobed_keys == the residual set.
- Execution: pinned replica `jsreplay.js` (`84585617...` byte-copy)
  2-pass fresh cold, budget 15M, worker max 2 (runbatch.sh operated in
  2-key parallel foreground pairs; disclosed in status.log and README).
  val-gate 4/4 node-exact on this host BEFORE the first probe (at2m
  0/2,000,000 x2, 15m `(2, 3651923)`/`(2, 5040200)`, forbidden quads
  95,670). **10/10 keys LOSS (result 2)**, WIN 0 (the WIN-CONTINUE rule
  never fired), exhaustion 0, mismatch 0, total nodes 23,252,550/pass
  (range 557,594..8,353,244, largest q049). No host interruption, zero
  truncated passes.
- Runner deltas disclosed: `runbatch.sh` (`989e359c...`) = published
  batch-17 `f591f8c2...` with the WIN block replaced by the declared
  honest WIN-CONTINUE label (continue, verdict NOT consumed);
  `runwave.sh` (`885830d0...`) = done-set adds WIN-CONTINUE. Both pinned
  in the MANIFEST.
- row-audit.json (schema
  `n11-centralreply-closure-class23101-batch14residual-rowaudit-v1`,
  sha256 `6b40b131...`): all 10 rows machine-re-verified from raws (both
  passes carry `# replay_done`, p1==p2 node-exact on all fields, within
  budget, result 2, input/batch-keys/status agreement); 3 runs
  byte-identical.
- Publication (3 commits, each message records observed HEAD-before-push):
  A `a5b514d7` (scaffold: runner scripts + maker + inputs + this-host
  val-gate + merged status.log, 26 files), B `ecfe258d` (raw q043..q052,
  20 files), C `cb94f808` (row-audit.json + README + MANIFEST-sha256,
  48 entries) = publication complete. **Fetch-back 48/48 byte-identical**
  (publication-commit-pinned raw URLs, MANIFEST per-file sha256 all rows).
- Note amendment published: Part AW status update appended to the
  single-owner note (blob sha1 lock `a60f8a95...` -> server blob
  `ba30165e...`, server size 260,851 bytes exactly matching the local
  composition; chunk-assembled full-content transfer verified by
  server-side blob identity).
- Verdict guards (unchanged): zero verdicts consumed by this Part; the 10
  LOSS rows may only later enter an increment via the sha-pinned
  fail-closed merger (`90711961...`) in a separately declared adoption
  Part whose BASE is the post-AV canonical 6,172-row cache (this Part
  touched no batch-17 artifact and no canonical cache); after that
  adoption, class 23101's canonical unknown cost-children shrink to the
  single unconsumed q042 WIN (route statement, no closure claim). The
  q042 adoption decision stays with the scrutiny owner (C++ second
  implementation gate pin `9193f5b6...`). The standard 11x11 empty board,
  the 19 central-reply roots, class 23101 (unknown 11 children on the
  current 6,120 canonical) and all 10 keys remain UNKNOWN throughout;
  nodes are bookkeeping, never verdicts. Open items (re-read latest main
  first): (a) the batch-17 52-LOSS canonical adoption Part (Part AV, in
  flight), (b) the scrutiny owner's q042 adoption decision, (c) the
  batch-14 residual 10-LOSS adoption Part after Part AV lands (BASE =
  canonical 6,172), (d) next batch-18 candidate selection from the
  post-adoption closure-classes rank.

## Continuation 37 (2026-11-22, this host): Part AY batch-18 (class 16131) declared, scaffold published, executed to WIN-HALT at the first wave (v001+v002 both WIN), published; verdicts NOT consumed

- Re-read latest main first: the competing lane had published Part AX
  (third-implementation cross-verification of batch-14 residual + batch-17
  edge rows, commits `dbab0b9b`..`115c7ad3`) and declared it before this
  lane's batch-18; no counter-declaration for the batch-18/class-16131
  scope existed, so this lane renamed its batch-18 to **Part AY**
  (previous kit name Part AX) and declared BEFORE execution: note amendment
  commit `6cde1b0b` (observed HEAD `0c9707ad`, note blob sha1 lock
  `2c53c205...`), base-independence pinned to the published canonical
  6,120-row cache `be9cb24e...` (Part AV output neither read nor needed:
  batch-17 keys are class-10661 cost children, disjoint from class 16131).
- Key derivation (published, no worklist transcription): make_batch18_keys
  v2 (published-base edition) derives the 53 class-16131 unknown graph-cost
  children directly from the pinned graph + canonical base, s5_index
  ascending key ids v001..v053, 3 runs byte-identical, all gates PASS
  (canonical 0/53 hits, quarantine 0/53, 15 unconsumed closure WIN children
  absent, duplicates 0 vs all 18 published packets / 875 rows, Board(11)
  legal 74..97 re-derived 53/53, rank table: ranks 1-13 win-refuted, rank
  14 class 10661 fully probed by batch-17, rank 15 = 16131 first clean).
  batch-keys.json sha256 `1bb3ed41...`. Scaffold publication: 70 files,
  commit `c36825c7`.
- Execution (after declaring, verifying no counter-declaration, val-gate
  first): val-gate 4/4 node-exact on this host (at2m 0/2,000,000 x2, 15m
  `(2,3651923)`/`(2,5040200)`, forbidden quads 95,670). Pinned replica
  `jsreplay.js` (`84585617...`) 2-pass fresh cold, budget 15M, max 2
  workers (two parallel published `runbatch.sh` (`f591f8c2...`)
  instances, odd/even split; disclosed in status.log RUNNER-NOTE and
  README). **First wave: both workers' first keys are WIN (result 1)**:
  **v001 WIN 5,656,151 nodes** (legal 83, key [1154610354467115008, 64])
  and **v002 WIN 7,898,204 nodes** (legal 84, key
  [3459890413727387648, 64]), both 2-pass node-exact, both within budget.
  Pre-registered WIN-HALT fired on both workers (rc=45); batch stopped.
  2/53 keys probed, 51 keys never run (fresh, re-probe rule not
  triggered).
- Publication: B `3c07f51a` (raws v001/v002 p1/p2 + status.log) + C
  `938e34f2` (README results section + MANIFEST-sha256 73 entries) =
  publication complete. **Fetch-back 9/9 byte-identical** (local kit vs
  commit-pinned repo read: 4 raws + status.log + README + MANIFEST +
  batch-keys + jsreplay + one CSV-equivalents set).
- Note amendment published: Part AY status update appended (blob lock
  `68a2e075...` -> commit `30d04759`, server blob `29c7b878...`).
- Consequences (route statements only, NOT verdicts): unconsumed closure WIN
  candidates now **17** (15 prior + v001 + v002), all scrutiny-owner
  blocked (C++ second-implementation gate pin `9193f5b6...`); if either
  v001/v002 WIN is adopted, the class 16131 all-LOSS closure route is
  refuted and the next clean candidate is rank 16 class 16513. Zero
  verdicts consumed; canonical cache stays 6,120 rows `be9cb24e...`.
- Honesty record: the standard 11x11 empty board, the 19 central-reply
  roots, class 16131 (51 children unprobed) and all 53 keys remain UNKNOWN
  throughout; node counts are bookkeeping, never verdicts. Part AV
  (batch-17 class 10661 adoption + reaudit, declaration `340abef3`
  19:20:42Z) remains unpublished on main at this session's end; takeover
  criteria unchanged (~23:00Z). Open items (re-read latest main first):
  (a) Part AV publication / takeover decision, (b) the scrutiny owner's
  WIN adoption decisions (now 17 candidates), (c) batch-18 continuation
  (51 fresh keys v003..v053) or pivot to batch-19 class 16513 (rank 16)
  under a new declaration, (d) the batch-17 52-LOSS adoption Part whose
  BASE follows Part AV.

## Continuation 38 (2026-11-22, this host): Part AX third-implementation cross-verification executed and published - 13/13 targets clean LOSS (Part AW q043..q052 + batch-17 budget-edge u031/u033/u038), 13/13 replica verdict agreements, 163/163 audit gates; verdicts NOT consumed

- Resumed from continuation 36 (Part AW publication complete at `cb94f808`).
  Part AV (batch-17 class 10661 adoption, declared `340abef3`) was still
  unpublished at resume. This continuation carved out Part AX, a
  non-intersecting verifier scope in the Part AR third-impl convention,
  declared BEFORE execution (note amendment commit `9771aa5b`, observed
  HEAD-before-push `29897108`, no counter-declaration; Part AY batch-18
  class 16131 was declared later at `6cde1b0` with declared non-contact -
  target row sets are disjoint; the Part AY declaration explicitly cites
  Part AX as non-contacting).
- Rebase note: while this Part AX record was being composed and
  pushed, the parallel AY lane published its own Continuation 37
  (batch-18 Part AY) to this session log; this Part AX record was
  renumbered 37 -> 38 and rebased onto the new head (session-log blob
  sha1 `84e6d514` -> `576d5616`, 154,249 bytes, verified byte-identical
  before push). The two continuations are disjoint Parts with no
  content conflict; the push was re-attempted with the new blob lock and
  records the observed HEAD-before-push in its commit message.
- Scope: 13 published 2-pass fresh-cold node-exact replica LOSS rows:
  the Part AW batch-14 residual q043..q052 (publication `cb94f808`) plus
  the batch-17 (class 10661, publication `ffc09de1`) budget-edge trio
  u031 (14,967,263 nodes - the whole-batch max-nodes row directly under
  the 15M budget; its published p2 is a fresh-cold retry after a host
  reset) / u033 (7,806,486, p2 retry) / u038 (6,589,964). The experiment
  is verdict-level corroboration literature for the Part AV
  adoption-declaration edge rows and the future class 23101 residual
  LOSS adoption Part; the other 39 batch-17 rows and the remaining Part
  AQ batch-14 rows (38; q042/q039-q041 were Part AR's) were not
  re-searched here.
- Execution: pinned third implementation `third_impl.js` (sha256
  `08ea958f...`, non-df-pn AND/OR minimax), 1 row = 1 solver = 1
  process, cap 300,000,000 expansions, wallcap 240s, `--memo-power=22`,
  every target/anchor run twice (a/b). **13/13 targets clean LOSS
  (result 2), 13/13 verdict agreements with the published replica
  rows**; every a/b pair identical in result/expansion/ttHits/reason
  (determinism PASS); total third-impl expansions 60,628,197/pass
  (range 611,783 q047 .. 17,661,456 u031 = 1.18x the budget-edge
  replica nodes; whole-table third/replica node ratios 1.11-1.18, the
  same band as Part AR). WIN 0, WALL-INCONCLUSIVE 0, DIVERGENCE 0.
- Gates: rules engine replica quads 95,670 == third-impl quads 95,670,
  195,044 randomized triples 0 mismatch; anchors k02a WIN (legal 87)
  9,106,337 expansions / 4,991,527 ttHits and l1a LOSS (legal 116)
  7,660,602 / 3,951,175 reproduced node-exact vs the published
  third-impl values on this host (a/b pairs); negatives ng1 (legal+1)
  and ng2 (stones 6) fail-closed with the exact designed wording; maker
  `make_inputs_ax.py` fail-closed on all sources (26 raw files 2-pass
  node-exact + `# replay_done` + in-budget result-2; published
  row-audits `6b40b131`/`c19e768f` cross-checks; runner status PASS
  3-way incl. the AW VAL-GATE 4/4 + WAVE-END stop=0 lines and the b17
  EXECUTION-COMPLETE 52/52 LOSS + P2-TRUNCATED-RETRY honesty lines, no
  fired HARD-STOP; batch-keys `dfde0e90`/`db762175` probe_order
  580..589 / 630/632/637; derived-vs-published input CSV byte-equality
  10+3 targets + 4 anchor/negatives against the published Part AR
  inputs), 3 runs byte-identical; audit battery `audit.py` **163/163
  gates PASS**, run twice byte-identical with published console
  captures (schema `n11-centralreply-closure-b14res-b17edge-thirdimpl-audit-v1`,
  sha256 `d1fc8999...`).
- Honesty records (full text in the experiment status.log and README):
  (1) a shell cwd grouping bug at the first anchor invocation started
  k02a tag=a once ahead of the intended clean pair (duplicated identical
  RUN line, deterministic fields unchanged, k02a.b never started in that
  shell; the absolute-path re-run overwrote the output - Part AR's ng1
  precedent). (2) The host CPU quota halves per-solver throughput when 2
  solvers run concurrently (k02a solo wall 25.63s vs 53.03s in the
  pair), so the 13 targets were executed sequentially, within the
  declared cap of max 2; deterministic fields are wall-independent.
- Publication: experiment dir
  `research/experiments/n11-centralreply-closure-b14res-b17edge-thirdimpl-20261122/`
  (113 files + MANIFEST) in 5 commits: A `dbab0b9b` (scaffold:
  pinned scripts + maker + audit.py + inputs, 24 files), A2 `b2867591`
  (published source raws archive, 26 files), A3 `b826eebc` (sources
  rest: batch-keys, row-audits, runner logs, published input CSVs,
  source MANIFESTs - 25 files), B `db036985` (solver outputs: targets
  a/b 26, anchors 4, negatives 2, rules-gate, status.log - 34 files),
  C `115c7ad3` (audit-summary + audit-run captures + README +
  MANIFEST-sha256 113 entries) = publication complete. **Fetch-back
  113/113** MANIFEST sha256 match at the publication commit. The note
  status update was appended and fetched back byte-identical (blob sha1
  lock `fc0910a5...` -> push `a0bd6061`, 275,176 bytes).
- Verdict guards (unchanged): zero verdicts consumed; this is
  verdict-level corroboration literature only. The Part AV batch-17
  52-LOSS adoption, the future class 23101 residual 10-LOSS adoption
  Part (BASE = post-AV canonical 6,172), and the scrutiny owner's 15
  unconsumed closure WIN / q042 adoption decisions (C++ second
  implementation gate pin `9193f5b6...`) are untouched and unabridged;
  no canonical cache write happened anywhere in this Part. The standard
  11x11 empty board, the 19 central-reply roots, class 23101, class
  10661 and all 13 keys remain UNKNOWN throughout; nodes and expansions
  are bookkeeping, never verdicts.
- Open items (re-read latest main first): (a) the Part AV batch-17
  52-LOSS canonical adoption publication (in flight), (b) the batch-18
  Part AY probes by a later session (v001..v053; declared `6cde1b0`,
  scaffold `c36825c7`; this lane did not contact them), (c) the class
  23101 residual 10-LOSS adoption Part after Part AV lands (BASE =
  canonical 6,172), (d) the scrutiny owner's 15-WIN/q042 adoption gate,
  (e) optional extension of third-impl spot coverage to further batch
  rows under a new declaration.

## Continuation 39 (2026-11-22, this host): Part AZ batch-18 WIN-row third-implementation cross-verification executed and published - 2/2 targets clean WIN with 2/2 replica verdict agreement, anchors node-exact, negatives fail-closed, 53/53 audit gates; verdicts NOT consumed

- Scope and declaration: Part AZ cross-verified the two WIN rows
  v001/v002 published in batch-18 (Part AY, class 16131) under the third
  implementation (verdict-free corroboration, Part G / AR / AX line).
  Declared by single-owner-note amendment at commit `a5ea2aa08...`
  (note lock blob `1c4917ac`, 281,536 bytes); batch-18 sources were not
  touched, the 51 unconsumed batch-18 keys and Part AV remained
  uncontacted by this Part.
- Experiment published at
  `research/experiments/n11-centralreply-closure-b18win-thirdimpl-20261122/`
  (43 files + MANIFEST, 43 manifest rows) in 3 commits: A `2e6d14ee`
  (scaffold: pinned third-impl harness, maker, audit inputs, 27 files),
  B `9a997c21` (solver outputs: target a/b pairs, anchors, negatives,
  rules-gate, status.log - 15 files), C `2f944d5d` (README + MANIFEST) =
  publication complete. **Fetch-back 43/43** manifest sha256 match at
  the publication commit.
- Determinism and gates: maker `make_inputs_az.py` run 3x byte-identical,
  all gates PASS. Source pins: batch-18 batch-keys `1bb3ed41` (53 keys,
  class 16131; v001 s5 `153671` / membership 2; v002 s5 `207534` /
  membership 3), 4 published raws (`24b45c8a`, `1fc367bd`, `41c10ec2`,
  `e9f578fc`), status-b18 `4b785add`, README `8b6a85b3`, published input
  CSVs `edee9be8` / `e8bbbaed`.
- Execution (sequential battery order negatives -> anchors -> targets):
  v001 third-impl WIN 6,558,484 expansions / 3,610,051 ttHits (replica
  5,656,151 nodes, ratio 1.16); v002 WIN 9,204,329 / 5,027,672 (replica
  7,898,204, ratio 1.17); a/b all identical; 15,762,813 expansions per
  full pass. Anchors k02a WIN 9,106,337 / 4,991,527 and l1a LOSS
  7,660,602 / 3,951,175 reproduce the published anchor values
  node-exact. ng1/ng2 fail-closed lines exact. Rules gate: quads
  95,670 == 95,670, triples 195,044 with mismatch 0.
- Audit: `audit.py` schema
  `n11-centralreply-closure-b18win-thirdimpl-audit-v1`, 53/53 gates
  PASS, run 2x byte-identical.
- Note status update appended: commit `792ee250` (blob `02080cd1`,
  285,045 bytes; note lock `1c4917ac` guard, observed HEAD `2f944d5d`),
  fetch-back byte-identical against the commit-pinned raw URL.
- Verdict guards (unchanged): zero verdicts consumed; this is
  verdict-level corroboration literature only. The 17 unconsumed closure
  WIN candidates (15 prior + batch-18 v001 + v002), the Part AV batch-17
  52-LOSS adoption, the future class 23101 residual 10-LOSS adoption
  Part (BASE = post-AV canonical 6,172) and the scrutiny owner's
  adoption gates are untouched and unabridged; no canonical cache write
  happened anywhere in this Part. The standard 11x11 empty board, the 19
  central-reply roots, class 23101, class 10661, class 16131 and all 53
  batch-18 keys remain UNKNOWN throughout; expansions, nodes and ttHits
  are bookkeeping, never verdicts.
- Open items (re-read latest main first): (a) the Part AV batch-17
  52-LOSS adoption publication (in flight), (b) batch-18 Part AY
  continuation / batch-19 (class 16513) selection by a later session
  (declared `6cde1b0`, scaffold `c36825c7`; this lane did not contact
  them), (c) the class 23101 residual 10-LOSS adoption Part after Part
  AV lands (BASE = canonical 6,172), (d) the scrutiny owner's 17-WIN
  adoption gate, (e) optional extension of third-impl spot coverage to
  further batch rows under a new declaration.

## Continuation 40 (2026-11-22, this host): Part BA batch-18 WIN-row v001+v002 two-WIN if-adopted decomposition executed and published - flips [4139, 5611, 6073, 16131] machine-computed holder union (double holder 16131), class 16131 BASE-unknown == the 53 batch-18 key s5 indices (new strong gate), excluded_now 23->27 projection; verdicts NOT consumed

- Scope and declaration: Part BA projects the classification-ledger
  consequence of adopting the two batch-18 WIN rows (v001 s5 153671 /
  v002 s5 207534) TOGETHER, as the scrutiny owner's adoption-decision
  precomputation (verdict-free, Part V/R/AB/AH/AI/AN/AO/AT precedent).
  Declared by single-owner-note amendment at commit `607c876af...`
  (note lock blob `01e980d9`, 290,488 bytes; observed HEAD-before-push
  `f8cc6c9d`). Same-scope counter-declaration grep over the note and
  the experiment directory listing: none. This closes the if-adopted
  gap: all 17 unconsumed closure WINs now have if-adopted
  decompositions. Batch-18 sources, the 51 unconsumed batch-18 keys
  and Part AV remained uncontacted.
- Environment note: one environment reset mid-run; all pinned inputs
  (graph `54f9c364`, update8 `b658290a`, Board `954d3a10`, policy
  `78655e94`, quarantine `81d23160`, BASE cache `be9cb24e` + 3 Part AS
  reaudit outputs, batch-18 batch-keys `1bb3ed41` + raws
  `24b45c8a`/`1fc367bd`/`41c10ec2`/`e9f578fc` + status-b18
  `4b785add`) were re-fetched from main and re-verified by sha; every
  stage was re-run after the rebuild and the primary and rebuilt
  outputs were byte-identical end to end (an extra determinism check).
- Execution: maker `make_increment_v001v002_win.py` run 3x
  byte-identical (increment `4f8fc29b`, 2 rows / 2 WINs; manifest
  `13736030`, schema `batch18-win-v001v002-ifadopted-increment-manifest-v1`,
  ifadopted_only, canonical untouched pin, base_cache_absent_hits 0,
  quarantine_hits 0); sha-pinned merger (byte-copy pin `90711961`,
  selftest PASS) run 2x byte-identical -> if-adopted cache 6,122 rows
  (WIN 160 / LOSS 5,962, conflicts 0) `6bfa9faa` (251,556 bytes),
  merge-audit run1/run2 byte-identical `4cdad34b`; BASE canonical
  6,120 rows `be9cb24e` byte-verified unchanged after all merges.
  Refresh adapt (from the published Part AT refresh `5f9810e6`,
  2-hunk adapt; cache sha expectation extracted from the cache file
  itself) run 2x serial, all four outputs byte-identical:
  refresh-summary `af95270b`, closure-classes `e5a91e15`,
  per-root-coverage `9f59ebf8`, probe-worklist `18429b91` (NOT
  published, sha recorded). Delta extractor
  `compare_deltas_v001v002_ifadopted.py` (`c1c39b50`, two-WIN adapt
  of the published Part AT extractor `207cfbcc`) run 3x
  byte-identical, all gates PASS (delta json `e3679aae`, schema
  `n11-b18win-v001v002-ifadopted-decomp-deltas-v1`); five fail-closed
  tamper tests (increment nodes, scenario summary, batch-keys s5,
  extractor WIN-constant, extractor BATCH_CLASS constant) were each
  caught by the intended pin/gate, immediately restored and
  re-verified byte-identical.
- Measured projection (bookkeeping, never verdicts): flips
  [4139, 5611, 6073, 16131] == the machine-computed BASE-unknown
  members of the graph holder union of s5 153671/207534 (v001 holders
  [4139, 16131]; v002 holders [5611, 6073,
  16131]; double holders [16131] only), all four unknown ->
  excluded_now; transitions ledger unknown->unknown 34,496 /
  excluded->excluded 390 / excluded_now->excluded_now 23 /
  free_now->free_now 36, no other transition, no regression;
  excluded_now 23 -> 27, unknown 34,500 -> 34,496, free_now 36
  unchanged; newly free classes/thirds empty (gated); per-root
  free/uncovered changed rows 0 (gated), root 27 baseline 119/119;
  class 16131 BASE-unknown children == the 53 batch-18 key s5 indices
  (new strong agreement gate), scenario-unknown 53 -> 51;
  closure-candidate table 809 rows unchanged with churn none, class
  16131 rank 15 -> 7 (unknown_now 51, groups_served 5, the table is a
  probing-worklist view); update8 resolved 79 -> 81 (newly [153671,
  207534], both inside the baseline requirement), win_hit_groups
  [] -> 5 (all five are class 16131 closure groups), groups_free_now
  127 unchanged, remaining_now 31,780 -> 31,729 (-51, the five
  win-hit groups drop out of the frozen per-group unknown union);
  joint greedy 36,726 -> 36,724 and probe worklist 64,941 -> 64,939
  (movers root 12 and root 48, -2 each).
- Publication: the experiment dir
  `research/experiments/n11-centralreply-class16131-win-v001v002-ifadopted-20261122/`
  (15 files + 1 unpublished worklist, 15 manifest rows) in 3 commits:
  A `603b4f4f` (if-adopted cache 6,122 rows), B (maker `1e7865cb`,
  merger `00c3cdc6`, extractor `ce134e05`, refresh `94b00500`,
  increment `8e8c51d5`, manifest `1b8bc3c8`, merge-audits `19366a1e`
  / `b4e8e534`), C (refresh-summary `2df84b96`, closure-classes
  `26ef7844`, per-root-coverage `e3abf46c`, delta json `f11677f3`,
  README `00c735de`, status.log `2cabe757`, MANIFEST-sha256
  `333ef6d1`) = publication complete. **Fetch-back 15/15** manifest
  sha256 match at each publication commit.
- Note status update appended: commit `592516d2` (blob `762fc545`,
  296,440 bytes; note lock `01e980d9` guard, observed HEAD `333ef6d1`),
  fetch-back byte-identical against the commit-pinned raw URL.
- Verdict guards (unchanged): zero verdicts consumed; the if-adopted
  cache 6,122 rows is a non-canonical projection, not the canonical
  chain; all 17 unconsumed closure WINs remain unconsumed on the
  canonical chain; the scrutiny owner's adoption gate (C++ second
  implementation, pin `9193f5b6`) is untouched and unabridged; this
  Part neither recommends nor rejects adoption; no canonical cache
  write happened anywhere. The standard 11x11 empty board, the 19
  central-reply roots, class 16131 (51 remaining unknown children)
  and all 53 batch-18 keys remain UNKNOWN throughout; nodes, worklist
  and greedy sizes are bookkeeping, never verdicts.
- Open items (re-read latest main first): (a) the Part AV batch-17
  52-LOSS adoption publication (still in flight at this Continuation),
  (b) batch-18 Part AY continuation / batch-19 (class 16513)
  selection by a later session, (c) the class 23101 residual 10-LOSS
  adoption Part after Part AV lands (BASE = canonical 6,172), (d) the
  scrutiny owner's 17-WIN adoption gate, (e) optional joint
  if-adopted extensions (e.g. the 17-WIN joint projection) under a
  new declaration.
