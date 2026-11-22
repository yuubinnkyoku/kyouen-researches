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
