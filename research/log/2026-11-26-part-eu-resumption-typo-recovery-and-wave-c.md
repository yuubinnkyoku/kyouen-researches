# Part EU resumption: owner-typo outage recovery + wave C outputs (2026-11-26)

Session record of the long-term lane that resumed the interrupted Part EU
(euwin2 third WIN canonical adoption, closure class 30345).  Everything in
this log was computed from published bytes only, at a third environment,
fail-closed.

## 0) The 2026-11-26 "repo hidden / all-404" outage is RETRACTED - it was an owner-name typo

The 2026-11-26 00:38Z+ diagnostics recorded in the lane notes concluded the
account/repo had been hidden (all REST endpoints 404).  That conclusion is
wrong: the owner `yuubnnkyoku` used in those probes and in the
github_app calls is an i-less typo.  The correct owner is
`yuubinnkyoku` (12 chars, 'i' after 'b'; the repo path quoted in every
lane charter).  Machine evidence, re-run this session:

* `GET /users/octocat` -> 200 while `GET /users/yuubnnkyoku` -> 404
  explained by the typo alone; under the correct owner the repo resolves:
  `list_commits` at `yuubinnkyoku/kyouen-researches` -> 200.
* `github_app.get_me` returns login `yuubinnkyoku` (correct) while its
  `profile_url` field carries the typo'd `yuubnnkyoku` - a connector
  response quirk; the login field is the authority.
* main HEAD was `ee7a951b` (2026-11-26T00:04:28Z, Part EV close-out)
  before AND after the whole "outage" window: no commit landed between
  00:04Z and this session because each hourly lane aborted on the
  mis-diagnosis.  Nothing was ever hidden; read/write access worked all
  along.

Operational lesson (now recorded in the lane knowledge): before concluding
"account hidden", a 404 storm must be probed with the `get_me` login field
verbatim AND both spellings side by side; the sandbox curl channel reaches
api.github.com / raw.githubusercontent directly and is the right
differential tool.

## 1) Part EU state at resumption (pre-registered chain)

The Part EU declaration (7136d22c,
`research/log/2026-11-25-part-eu-win2-adoption-declaration.md`) pre-registered
the full deterministic chain: maker -> merger -> refresh fork -> extractor,
with pins increment `d9365d80`, merged `3ba48608`, merge-audits `9f807c95` x3,
refresh outputs `2b70bb55` / `59a4c85f` / `cfc2bfe1` and worklist regen pin
`397a4379` (unpublished per size policy).  Wave B (kit scripts: merger
90711961, maker f2ae97a1, extractor aaf13bdc) landed 3/3; waves C..F never
landed due to the typo outage.  The canonical BASE meanwhile remains the
Part ER head `9c4dd94e` (6,765 rows WIN 186 / LOSS 6,579).

## 2) Wave C regeneration executed this session (published bytes only)

Dependency fetch, all sha256 verified byte-for-byte:

* 271/271 kit files (Part ER kit 14, Part ES kit 38, Part ET kit 38, b38 kit
  181) against the four published MANIFESTs (`cc987739`/`f0c1c27a`/`4dbf8856`/
  ER `46eef302`), plus frozen deps dependency-graph `54f9c364`, update8
  `b658290a`, Board source `954d3a10`, evidence policy `78655e94`, quarantine
  `81d23160`, and the three EU kit scripts (pins above).

Execution (all fail-closed, all rc=0):

* **maker** G0-G5 all PASS: BASE cache accounting 6,765 rows WIN 186 /
  LOSS 6,579; the 18 Part-ER adopted rows re-verified WIN in BASE
  (regression tie, not re-adopted); b38 SSOT 49 keys, pool re-derived from
  the published b38 raws = exactly {ai007,ai024,ai030,ai038,ai040,ai041}
  = the ET registry targets; ES/ET gate raws node-exact vs ES source raws
  at the 30M condition; ES-30M WIN disposition of the pool = exactly
  {ai007,ai040}; freshness (both adopted keys absent from BASE) and
  quarantine 0 hits.
* increment-euwin2-20261125.cache = `d9365d80...` (declared pin,
  byte-identical); increments-manifest.json = `793f68c5...` (extractor
  pre-pin, byte-identical).
* **merger** selftest PASS; merge 3 runs -> merged-exact-s5-chain-plus-
  euwin2-20261125.cache = `3ba48608...`, 6,767 rows WIN 188 / LOSS 6,579
  (declared pin, byte-identical); merge-audit-run1/2/3.json
  byte-identical = `9f807c95...` x3 (declared pin).
* **scenario refresh fork** (disclosed diff vs the published Part ER
  refresh `6c91e0ce`: ONLY the CACHE path, the expected cache sha, and the
  docstring; all computation bytes identical): executed rc=0 ->
  refresh-summary `2b70bb55`, closure-classes `59a4c85f`,
  per-root-coverage `cfc2bfe1`, probe-worklist regen `397a4379`
  (3,717,712 B, unpublished per size policy) - ALL FOUR declared
  post-condition pins byte-identical.
* Independent census cross-check (this session, vs the published Part ER
  reaudit outputs): closure-classes.csv 805 -> 805 rows, ZERO rows
  leave/enter, the only unknown_now churn is class 30345: 7 -> 5, the only
  class_rank churn is the exact two-row swap {30345: 8->7, 20421: 7->8};
  class_status_counts 34,436/84/39/390 -> 34,430/90/39/390 (exactly the 6
  declared UNKNOWN->excluded_now flips, net); win_hit groups unchanged
  (10 groups, class 30354) on both sides; frozen update8 static
  (31,859 / 260 / 131 / remaining 31,505); joint greedy 36,619 static;
  group_best_options_nonfree 2,105 static; worklist 64,309 -> 64,307;
  per-root free_now/uncovered thirds identical at every root; the
  individual greedy union changes only at the 2 declared roots
  (12: 2850 -> 2848, 36: 3007 -> 3005).  Pure re-selection bookkeeping;
  no coverage claim.

**Wave C published** (commit f7e607b1): the six output files above;
fetch-back at the commit is 6/6 byte-identical to the regenerated
artifacts = to the declared pins.

## 3) Wave D blocker (honest disclosure - the ONLY unsatisfied pin)

The published extractor `compare_deltas_eu_adoption.py` (aaf13bdc) also pins
the scenario refresh script itself: SCEN_REFRESH_SHA = `a377eea0...`.  Those
exact fork bytes were produced by the pre-declaration exploration of the
declaring session, were never published (wave B pushed only the 3 kit
scripts), and the declaring session's environment is gone; repo-wide code
search for `a377eea0` / `refresh_adoption_eu` finds only the extractor pin.

A regenerated fork that satisfies the declared diff policy (only the CACHE
path, the expected sha and the docstring differ from the ER refresh
`6c91e0ce`; verified: exactly 3 diff regions, all computation bytes
identical; fork sha `353f15d3...`) reproduces all four refresh outputs
byte-identically (the outputs are docstring-insensitive - executed here),
but does NOT satisfy `a377eea0`.  The extractor therefore fails closed at
exactly that pin (rc=1, observed; all other pin-list objects verified
byte-identical this session - 24/25).

Decision deferred (NOT taken this session): waves D (refresh fork +
decomp-deltas-euwin2-adoption.json), E (close-out README + MANIFEST-sha256),
F (completion log) remain open.  Options for the next owner session:

1. recover the exact `a377eea0` fork bytes (not found in any published
   artifact so far), or
2. issue a disclosed repair of the extractor's SCEN_REFRESH_SHA pin to a
   disclosed-diff fork (byte-verifiable against `6c91e0ce` in exactly the
   3 declared regions), re-run the extractor to full PASS, then land
   waves D-F.  This changes published kit bytes and must be its own
   declared repair decision.

Until the Part closes, the operating canonical BASE remains the Part ER
head `9c4dd94e`: the EU merged cache `3ba48608` is published and byte-pinned
but not yet adoption-complete; no census effect is consumed anywhere.

## 4) Guarantees

The standard 11x11 empty board stays UNKNOWN.  Every central-reply root
stays UNKNOWN.  Consuming the 2 WIN labels asserts NO root verdict; nodes
are bookkeeping.  Unconsumed and untouched: the 4 ES-30M-resolved LOSS rows
(ai024/ai030/ai038/ai041, EM-pattern territory), the b38 15M
honest-EXHAUSTED labels (honest UNKNOWN at 15M, same-condition re-probe
ban untouched), b018 (dual-class, scrutiny-owner pending), the k04
sixth-cost WIN, and every other unconsumed probe-level WIN.  No free
coverage, secured coverage, or root-resolution claim is made anywhere.
