# 2026-11-22 n11 S4BD fresh-corpus regeneration resume: pass1 k085-k101 + s6w pair + pass2 completion session log

Lane: the n11 long-term lane (11x11 weak solution). Declaration for this
session: `research/log/2026-11-21-n11-sbd-corpus-regen-resume-pass1-single-owner-note.md`
(`6273b13fe67`, 23:50Z, HEAD-before-push `29e0deca34`). Parent lane
declaration: `research/log/2026-11-21-n11-sbd-fresh-corpus-regen-single-owner-note.md`
(15:39Z). The parent session stalled after its k061-k084 pass-1 checkpoint
(`93ceaab9c3`, 17:22Z); this session resumed it with no new keys claimed.

## What this session executed (all fresh cold, pinned jsreplay sha256
`845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`, fresh
2^22 PnTT per row, deadline 0, exact-order=count, serial single process,
budget 15,000,000)

1. Preflight (before the declaration):
   - jsreplay pin byte-verified; independent.py pin byte-verified
     (`954d3a10...`).
   - All 101 input CSVs regenerated from `input/corpus-def.json` and compared
     byte-for-byte against published (match, as in the k001-k084 audits);
     `input/s6w.input.csv` matches the corpus-def witness entry.
   - Chain base `merged-exact-s5-after-js-probe-13.cache` sha256 `60e0dc34...`
     (5,756 s5verdict rows); all 101 claimed keys absent (exact decimal
     strings); the 7 chain keys disjoint from the corpus selection.
   - Node-exact validation gate 4/4 on this host (at2m x2: 0 / 2,000,000 /
     legal 98,99; 15M rows: 2 / 3,651,923 and 5,040,200).
2. Pass 1 k085-k101 (17 rows): all result 2 exact LOSS within budget,
   78,590,859 nodes total, 0 WIN, 0 unexpected budget exhaustion, every
   verdict equal to the audited union-backlog historical verdict
   (machine-compared). Row walls 13-57s on this host. Pushed `99becad0f9`
   (17 raws; fetch-back 17/17 byte-identical via commit-pinned raw fetch +
   cmp). Pass 1 is thereby complete for the whole declared corpus k001-k101
   (k001-k084 by the parent lane, byte-pinned here at `32d436ae9` for the
   pass-2 comparisons).
3. S6 witness re-execution: `s6w.run1.p1.out` / `s6w.run2.p1.out`, two
   independent cold runs, both result 2, nodes 5,859,060 (wall 29/30s),
   identical to each other in result and nodes and equal to the published
   historical witness row (5,859,060). Pushed `32d436ae9`. This is the route
   material for the TARGET_S5 derived row (acceptance condition 5); no
   derivation, no derived cache row was produced this session.
4. Pass 2 (determinism gate over the whole table): all 100 settled rows
   re-run cold, (result, nodes) identical to pass 1 row-for-row.
   Determinism: 100/100 matches, 0 mismatches; 546,428,673 nodes each pass
   (whole corpus, including the parent-lane rows). k012 (TARGET_S5) was not
   re-run (only result 0, honest UNKNOWN at 15M, not a settled row; its route
   stays the s6w pair). Pushed incrementally `d8575d50a8` (k001-k024),
   `67ae97a243` (k025-k044), `51d4fa7155` (k045-k068), `378a98f592`
   (k069-k101), fetch-back every batch byte-identical (23/23, 20/20, 24/24,
   33/33).
5. Read-only consistency table `output/pass-consistency-table.json`:
   fail-closed aggregate over all 101 rows + s6w (per-row provenance,
   determinism, historical agreement, UNKNOWN guard). All gates pass.

## Session totals

- Fresh exact replay nodes executed this session: pass1 k085-k101
  78,590,859 + s6w pair 11,718,120 + pass2 100 rows 546,428,673 + validation
  gate 12,691,923 = 649,829,575 nodes, serial, single process at a time.
- Zero WIN rows on any corpus key; zero determinism mismatches; zero
  fresh/history disagreements; one honest result-0 row (k012, declared
  TARGET_S5).

## Incidents and honest notes

- One execution-environment reset occurred mid-pass-2 (during the k089-k098
  batch call; "Koyeb remote command" infrastructure failure, not a timeout).
  The in-flight batch output files were lost; everything completed up to
  k088 was protected by the knowledge-kit mirror and pushing protocol. The
  workspace was rebuilt (pinned pins re-verified: jsreplay sha256 re-checked)
  and k089-k101 were simply re-run cold; all re-run rows matched pass 1
  exactly (nothing was salvaged silently; every reported p2 number comes
  from a complete post-reset run).
- The first version of this session's consistency-table generator had a
  self-check bug (it compared a full replay row dict against a two-key dict
  for the s6w pair, falsely failing the pair gate). Caught before
  publication, fixed, regenerated; the published table is the fixed
  version with `fail_closed: true` and empty `gates_bad`.
- GitHub unauthenticated API hit its rate limit mid-session; fetch-backs
  switched to commit-pinned raw.githubusercontent fetches plus the
  authenticated GitHub App path. All fetch-backs completed.
- Layout deviation (documented, to be resolved by the merge run): this
  session published pass-2 raws as `output/raw/kNNN.p2.out`
  (execution-time checkpoint naming consistent with the p1 checkpoint
  layout), while the never-yet-executed `scripts/build_merged_cache.py`
  expects `output/raw-pass2/kNNN.p2.out`. The merge run must repoint that
  single path constant (or mirror the raws) and record the one-line diff;
  logic must otherwise stay identical.

## Not done this session (handed to the next run, per the declaration)

- No merge, no cache increment, no derived row for TARGET_S5, no
  `merge-manifest.json`, no audit pipeline (`gen_s6_witness_audit.py`,
  `audit_frontier.py`, `audit_root_loss.py`, reclassify/cardinality/analyze),
  no class-status/coverage/third-move statement, no K item, no knowledge
  README edit. Every verdict of the table remains unconsumed until the
  final-commit gates of the parent declaration are published.
- **The standard 11x11 empty board, the two-stone root {60,27}, and the
  third moves {100,108} remain UNKNOWN. Nodes, pass counts, and solved
  counts are never verdicts.**

## Sources

- Declaration: `research/log/2026-11-21-n11-sbd-corpus-regen-resume-pass1-single-owner-note.md`
- Parent declaration: `research/log/2026-11-21-n11-sbd-fresh-corpus-regen-single-owner-note.md`
- Experiment: `research/experiments/n11-s4bd-fresh-corpus-regen-20261121/`
  (README resume-checkpoint section, `output/raw/*.p1.out`, `output/raw/*.p2.out`,
  `output/raw/s6w.run1/run2.p1.out`, `output/pass-consistency-table.json`)
- Pushes: `6273b13fe67` (declaration), `99becad0f9` (pass1 k085-k101),
  `32d436ae9` (s6w pair), `d8575d50a8`, `67ae97a243`, `51d4fa7155`,
  `378a98f592` (pass2 checkpoints), plus this session's final commit
  (README + consistency table + this log).

## Addendum (post-log pre-verification of the merge pipeline; nothing published from it)

- Motivation: de-risk the next run's merge stage. Nothing below consumed or
  published any verdict.
- The unpublished `scripts/build_merged_cache.py` was executed on a local
  scratch tree (repo-path-pinned; base cache, geometry.json.gz,
  s5_evidence_policy.py, quarantine registry all sha-verified against the
  published pins) with exactly two deviations, both documented here and NOT
  published: (1) `RAWS2` repointed from `output/raw-pass2/` to `output/raw/`
  (the actual pass-2 checkpoint location; one-line path diff, logic
  identical); (2) a scratch-only placeholder for `k012`'s pass-2 raw
  (declared out of this session's scope), which lets the loop run but means
  the k012 determinism pair was NOT actually exercised. The scratch pass
  also used byte-copies `s6w.p1.out`/`s6w.p2.out` of the run1/run2 raws to
  satisfy the script's expected filenames.
- Result: every fail-closed gate that does not depend on k012's pass-2 raw
  PASSED (canonical/safe/quarantine-free 101-key geometry checks with
  Board-derived legal counts; input/raw structural checks; 100-row
  determinism; s6w pair; fresh/history agreement; base cache integrity;
  derived k012 row shape; merged-cache construction: 5,756 + 101 = 5,857
  rows, strictly sorted, no duplicates, no quarantined keys, no base
  conflict).
- Scratch merged-cache sha256 was `4fee9d5e...` and the scratch manifest
  records 100 direct-settled rows + the 1 derived TARGET_S5 row
  (verdict 2, nodes 0). The scratch outputs and scratch manifest were
  deleted (they contain the k012 placeholder), so this sha is only an
  expected-byte-target candidate for the merge run: the canonical merged
  cache is expected to be byte-identical IF the merge run re-executes the
  unpatched script with a true `k012.p2.out` whose row is the same honest
  result 0 / nodes 15,000,000 exhaustion (the k012 cache row is derived and
  does not depend on its pass-2 raw, but the determinism gate must truly
  run).
- Merge-run checklist (next session, with its own declaration):
  1. Run `k012` pass-2 fresh cold (budget 15M; expected result 0,
     nodes 15,000,000; ~2-3 min), publish `output/raw/k012.p2.out`.
  2. Repoint `RAWS2` in `scripts/build_merged_cache.py` to `output/raw/`
     (one-line path diff, logic identical, record both shas), or mirror
     the raws into `output/raw-pass2/`.
  3. Execute `gen_s6_witness_audit.py` (witness membership / odd-stone
     AND polarity machine check for the derived row).
  4. Execute the unpatched merge; publish merged cache + merge-manifest;
     compare the merged-cache sha256 against the scratch pre-verification
     candidate above (identical bytes expected; any divergence is a
     publication blocker to investigate first).
  5. Only then the Oct 12 audit pipeline (audit_frontier, audit_root_loss,
     reclassify, cardinality, analyze) and the class-closure /
     119/119-coverage / root-{60,27} statements under their own gates.
- No verdict was consumed by this addendum. The standard 11x11 empty board,
  the two-stone root {60,27}, and the third moves {100,108} remain UNKNOWN.

## Addendum 2 (further scratch pre-verification of the audit pipeline; still nothing published)

- The two audit stages were also exercised on the same local scratch tree
  (same two path repoints and the k012 pass-2 placeholder caveats as
  addendum 1; scratch outputs deleted after the checks, values recorded here
  as expected-value anchors for the merge run only):
  - `scripts/gen_s6_witness_audit.py` PASS: single LOSS witness
    `(1152921504675009536,536870912)`, pass determinism true, derived
    parent S5 outcome LOSS; the Oct 12 published raw `s6-211.csv` (fetched,
    unchanged) carries the identical replay row result 2 / nodes 5,859,060.
  - `scripts/audit_frontier.py` (whose internal gates machine-regenerate
    every one of the 3,384 frozen S4 child boundaries against the
    independent Board and hard-require the residual set to be {100,108} or
    empty) ran clean on the scratch merged cache in ~4s. Expected values if
    the canonical merge is published (NOT asserted by this session):
    cache rows 5,857 (LOSS 5,699 / WIN 158), all-S4 class counts
    {LOSS 32, WIN 272, UNKNOWN 3080}, third-move coverage 119/119 secured,
    remaining third moves [], target S4 `(1297036692683752448,0)` all-106
    children LOSS, status LOSS.
  - `scripts/audit_root_loss.py` ran clean in ~4s on the scratch cache and
    produced the move-by-move root `{60,27}` certificate structure with
    `root_outcome: LOSS` (solver-trusted AND/OR propagation over
    independently regenerated root moves x S4 responses x S5 children; not
    a terminal-only proof). Also NOT asserted by this session: it must be
    re-executed by the merge run on the published canonical cache.
- Combined with addendum 1, the entire remaining pipeline of the parent
  declaration is now exercised end-to-end in scratch with every
  non-k012-pass-2 gate passing and expected values recorded (kit:
  `preverification-expected-values.json` in the lane kit mirror). The merge
  run's checklist is unchanged: k012 pass-2 fresh cold; the RAWS2/WITNESS2
  path repoints (or raw mirroring); then the unpatched pipeline.
- Again: no verdict consumed, no class-status or coverage claim published.
  The standard 11x11 empty board remains UNKNOWN; the two-stone root {60,27}
  keeps its guarded treatment until the canonical publication passes all
  gates; nodes and pass counts are never verdicts.
