# Part ER second-environment verification (erwin18 second WIN canonical adoption) - 2026-11-25

Independent re-execution of the entire published Part ER chain from the
published bytes only, in a third environment (this run: Python 3.12.14,
Linux x86_64), with no reliance on any local state from either prior
host.  Every stage of Part ER that is re-executed below reproduced
byte-identically, including the extractor's double-run and its own
in-tree re-execution of BOTH refresh forks.  This log asserts NO root
verdict and NO 11x11 outcome: the standard 11x11 empty board and all 19
central-reply roots stay UNKNOWN; verdicts remain unconsumed beyond the
18 adopted WIN rows; nodes are bookkeeping.

## 1. Fetch provenance (publish-then-verify)

All inputs were fetched fresh from raw.githubusercontent at pinned commit
`bc70b536` (ER wave F completion; every dependency and the ER kit itself
landed strictly before it), 280 byte-pinned files in total:

* the Part EQ scrutiny-gate kit MANIFEST-sha256 (sha256 786315f3...) and
  all its 73 referenced members;
* the batch-38 kit MANIFEST-sha256 (4dbf8856...) and all its 180
  referenced members;
* the Part EP kit subset this chain reads: BASE merged cache
  fd29a337... (6,747 rows), EP increment c245bc4c..., the published EP
  refresh fork 99d583c3..., and the EP reaudit outputs 5a1ff0c5... /
  fdd4e4b2... / 487a95c4...;
* the 5 frozen reaudit dependencies of both refresh forks: frozen graph
  54f9c364..., update8 b658290a..., Board source 954d3a10..., policy
  78655e94..., quarantine registry 81d23160...;
* all 14 published Part ER files (scripts 3, refresh fork 6c91e0ce...,
  outputs: increment 4f6b7797..., increments-manifest 48b71d6a...,
  merged cache 9c4dd94e..., merge-audits d55f578f... x3, reaudit
  outputs a6b8d082... / 4c03f965... / 1bf6c25a..., decomp cd11b1a5...).

Every fetched byte was machine-verified before re-execution: 280/280
sha256-exact against the published pins and kit MANIFESTs, and the maker
then re-hashed all 253 kit member files LIVE again inside its own G1
(en 73 + b38 180), so the kit authenticity layer was exercised twice,
independently.  No per-file pin anywhere was hand-typed in this run.

## 2. Re-execution matrix (all from published bytes)

| stage | result vs published pin |
|---|---|
| maker `make_increments_er_win18_adoption.py` (39f6c86a...) | rc=0 PASS in 0.34 s (G0-G6 all-PASS; G1 re-hashed both kits file-by-file); emitted increment `4f6b7797...` and manifest `48b71d6a...` both byte-identical to the published outputs (cmp against the fetched published copies); rows=18 nodes=136,604,338, and the EQ-prose mis-sum record (136,539,338) is carried in the manifest exactly as published |
| merger `s5_union_merge.py` (90711961...) selftest | PASS (positive dedupe+sort; cross-file conflict reject; within-file conflict reject; malformed verdict reject; double-run determinism) |
| merger merge BASE(fd29a337...) + increment, 3 runs from the ER kit root with the published CLI path strings | 3/3 rc=0, merged cache `9c4dd94e...` (6,765 rows WIN 186 / LOSS 6579) and audits `d55f578f...` x3 byte-identical across runs AND to the published pins (the published audits record relative input paths, so the audit bytes reproduce exactly) |
| refresh fork `refresh_adoption_er.py` (6c91e0ce...) | rc=0 PASS in 61.3 s (owner run record: 61 s); `refresh-summary.json` a6b8d082..., `closure-classes.csv` 4c03f965..., `per-root-coverage.csv` 1bf6c25a... all byte-identical to the published reaudit outputs; the size-policy-unpublished `probe-worklist.csv` regenerated at exactly the regen pin `78e499dd...` |
| extractor `compare_deltas_er_adoption.py` (c3e82ea...) - run 1 | rc=0 PASS in 124.1 s (owner: 125 s): re-executed BOTH refresh forks byte-verbatim in isolated scratch trees (published EP 99d583c3... against fd29a337..., ER 6c91e0ce... against 9c4dd94e...), byte-verified all eight outputs against the published/regenerated pins incl. the two worklist regen pins (7cd566bf... / 78e499dd...), and emitted `decomp-deltas-erwin18-adoption.json` byte-identical to the published `cd11b1a5...` |
| extractor - run 2 (clean control after the tamper battery) | rc=0 PASS in 124.8 s, decomp output byte-identical AGAIN (`cd11b1a5...` both times), scratch trees cleaned |

Key extractor stdout, both runs: `ER decomp OK: flips=41
caches=6747->6765 win=168->186 closure_left=[] greedy=36643->36619
decomp_sha=cd11b1a5...`.

## 3. Numeric independence confirms (published-bytes parse + recompute)

* census exactly as published on both sides: before unknown 34,477 /
  excluded_now 43 / free_now 39 / excluded 390; after unknown 34,436 /
  excluded_now 84 / free_now 39 static / excluded 390 static;
* EXACTLY 41 classes flip, all UNKNOWN -> excluded_now, exactly the
  owner classes of the adopted keys that were still unknown; the three
  further owners 29979/30345/30542 do NOT double-flip (owner union 44,
  re-derived from scratch);
* class 30345 cost-unknown 25 -> 7 (stays excluded_now); class 30118
  51 -> 50 (member ai034); class 30354 untouched 96 -> 96; closure CSV
  805 -> 805 rows, no row leaves or enters; the only unknown churn is
  the 2 rows 30118/30345; the only rank churn is the six-row set
  30345 9->8, 34269 8->9, 30118 15->12, 12264 12->13, 5473 13->14,
  16957 14->15;
* update8 frozen baseline static (union 31,859; resolved 260;
  remaining_now 31,505; groups_free_now 131); exactly 10 win_hit groups,
  all of s4 class 30354, 97 unknown children each;
* Board-verified free 39/39 both sides, zero rejections; greedy deltas
  only at roots 0 (2981->2980), 12 (2868->2850), 36 (3025->3007);
  joint greedy union 36,643 -> 36,619 (-24); probe worklist 64,309 -
  the honest shrinking tradeoff of consuming 18 previously-unknown WIN
  verdicts (EP grew it by +183; ER shrinks it by -24).

No re-executed number diverged from any published value anywhere.

## 4. Tamper battery (fail-closed, sha-change proven BEFORE each gate)

Every scenario asserts the tampered file's sha256 actually changed
against the pin BEFORE the gate run, then restores byte-exactly and
re-verifies (post-battery full 280-file integrity: 0 drift):

* T-ER1 manifest tamper: one trailing byte on
  `output/increments-manifest.json` -> sha change asserted
  (48b71d6a -> 7369a394...), extractor rc=1 ABORT `manifest sha
  drift: 7369a394... != 48b71d6a...` at the pin table, before any
  refresh re-execution; restored byte-exact.
* T-ER2 scenario-cache tamper: +1 on the nodes field of a LOSS row of
  the merged cache `9c4dd94e...` -> tamper proven via a full-list
  re-check (exactly ONE of 280 pinned files drifted, the merged cache,
  sha 17d5bfd0...), refresh fork rc=1 fail `merged cache sha256
  drift`; restored to `9c4dd94e...` byte-exact.
* T-ER3 quarantine tamper: one trailing NUL byte on the quarantine
  registry -> sha change asserted (81d23160 -> c4da2ebc...), refresh
  fork rc=1 fail `quarantine registry sha256 drift`; restored
  byte-exact by refetch at the pinned commit.
* T-ER4 source-raw tamper: nodes 3552766 -> 3552767 on the b38 kit
  `output/raw/ai002.p1.out` -> sha change asserted (a3aa00f6 ->
  2f568c41...), maker rc=1 ABORT `kit sha drift (b38):
  output/raw/ai002.p1.out` (the MANIFEST pin layer catches a live
  nodes falsification before any eligibility logic); restored
  byte-exact to the b38 MANIFEST pin; clean control maker re-run rc=0
  with byte-identical emission.
* T-ER5 merger WIN/LOSS conflict: a synthetic increment re-emitting an
  existing BASE LOSS key (135268368:536870912) as WIN -> merger rc=1
  `GATE FAILED: WIN/LOSS conflict at 135268368:536870912: verdict 2
  (input #1 line 2) vs verdict 1 (input #2 line 2)` with NO output
  file and NO audit file written (a falsified WIN can never cross the
  union merger silently).

## 5. Honest notes

(a) One transient execution-environment hiccup occurred mid-battery
(the first T-ER1/T-ER2 command was served by an instance with a stale
view of the workspace: several files read as absent, one python
invocation returned rc=2 'can't open file', and the T-ER1 append never
landed; only the T-ER2 cache mutation had landed).  Recovery was
fail-closed throughout: a full 280-file pinned integrity re-check ran
BEFORE the T-ER2 gate (proving exactly the intended file and only that
file had drifted), the gate then failed as designed, both files were
restored byte-exactly, and the battery was re-run cleanly scenario by
scenario (T-ER1 re-issued above).  No conclusion in this log depends
on the affected command.

(b) This environment's raw CDN again returned 404 for full 40-hex
commit-sha URLs while serving the same paths at the short sha
(`bc70b536`, the identical commit); the same quirk was recorded by the
Part EP second-environment verification.  All pins were verified after
fetch regardless.

(c) One file (the ER reaudit per-root-coverage.csv) needed a single
retry on its first fetch (transient CDN failure); the retry verified
byte-exact against the published pin 1bf6c25a...

(d) Part ER outputs remain single-published: no byte of the ER kit was
altered on main by this verification; re-execution wrote only to local
scratch and /tmp, and this log is the only artifact pushed.

## 6. Guarantees

Part ER is now verified in a second, independent environment from
published bytes alone, all stages included: the adopted 18 WIN rows'
full eligibility chain (two-pass fresh-cold node-exact b38 source raws,
the EQ C++ second-implementation scrutiny-gate kit re-hashed
file-by-file with SSOT-extracted pins, batch-keys SSOT quadruples,
freshness to BASE fd29a337..., quarantine absence, the ai048 EP
regression tie), the deterministic union merge with byte-identical
audits, the Board-driven reaudit, and the extractor's independent
41-flip census with both refresh forks re-executed twice (once in each
of two full extractor runs, each byte-identical).  The standard 11x11
empty board stays UNKNOWN; all 19 central-reply roots stay UNKNOWN;
class 30345/30118/30354 status changes are derived scheduling
bookkeeping from the WIN consumptions; nodes are bookkeeping; no
verdict beyond the 18 adopted WIN rows is consumed anywhere by this
log.

## 7. Resume

* The canonical head remains `9c4dd94e...` (6,765 rows WIN 186 / LOSS
  6,579); every future adoption / refresh / extractor must re-baseline
  here, now proven reproducible on a third host from published bytes.
* No unconsumed gate-verified WIN row remains from batch-38: class
  30345 now holds 7 unknown members (the 6 honest-EXHAUSTED keys at
  the 15M condition plus b018-pending territory), which are NOT
  adoptable without a different-condition probe (the same-condition
  re-probe ban stands) or a third-implementation route.
* The K1337/K1338 conic-lane publications concurrent with this run were
  orthogonal (no Part ER path touched); conflicts were checked before
  push and none existed.
