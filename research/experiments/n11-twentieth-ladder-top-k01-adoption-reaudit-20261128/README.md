# n11 twentieth ladder-top k01 adoption reaudit (flip-census/refresh)

Execution kit of the Part declared in
`research/log/2026-11-28-n11-twentieth-ladder-top-k01-adoption-reaudit-declaration.md`
(commit `2b96c5d9`, single owner, publish-then-execute): the WIN-side
flip-census review of the twentieth ladder-top k01 canonical adoption
(declaration `35f902c6`, completion `6292a823`; BASE = class-20421 k05
head of record `e1a9cacc...` 6,905 rows WIN 223 / LOSS 6,682,
SCEN = twentieth k01 head of record `1f1430f3...` 6,906 rows
WIN 224 / LOSS 6,682).

## Measured (3 refresh runs + 3 measurer runs byte-identical)

- **Status flips: exactly the 2 owner-union classes [769, 34269]
  flip unknown -> excluded_now** (the declaration's naive TWO-flip
  prediction holds with zero deviation). Census: unknown 34,352 ->
  34,350 / excluded_now 168 -> 170 / free_now 39 (Board-verified both
  sides) / excluded 390. UNLIKE the k05 adoption, the serving class
  34269 is NOT pre-excluded at BASE: it becomes win-hit by its OWN
  adopted child (the measured flip list EQUALS the owner union).
- **Serving class 34269 (1152921504624672768:68719476736) STAYS in
  the closure ladder: 797 -> 797 rows, entered [], left [], ZERO
  rank-churn cells** (unknown_now 11 -> 10, rank 1 -> 1). The other
  flipping owner class 769 sits OUTSIDE the ladder on both sides.
  The ladder STAY is a scheduling/census statement, NOT a class
  closure claim and NOT a root verdict.
- Per-root coverage: free_now/uncovered identical on all 20 roots;
  two individual greedy re-routes measured (root 12 drops
  2,931 -> 2,930 and root 24 drops 2,775 -> 2,774, scheduling
  re-route churns of those roots' greedy orderings, NOT coverage
  claims); joint greedy MEASURES 43,184 -> 43,183; probing worklist
  64,251 -> 64,250 (SCEN regen pin `55778a3f...` / 3,713,956 B,
  unpublished per size policy; BASE pin `09865553...` / 3,714,021 B
  reproduced).
- update8: the adopted s5 index 38891 sits INSIDE the frozen baseline
  requirement (resolved 291 -> 292, groups_free_now 131 unchanged).
  **ONE DISCLOSED DEVIATION from the declaration's naive prediction
  (35 -> 35): the win-hit group set MEASURES 35 -> 40** - the
  serving class 34269 IS an update8 plan group class, so its own
  adoption win-hits its 5 plan groups (all 5 added groups have
  s4_class_index 34269; no group removed) and removes their 10
  further unknown children from remaining_now (31,332 -> 31,321).
  The other owner class 769 is NOT a plan group class. The
  declaration's standing caveat (the measured census replaces the
  prediction) covers exactly this case.

## Gates (fail-closed)

Refresh: 3-region byte-clone of the published class20421 k05 reaudit
refresh (docstring, CACHE path to the twentieth k01 adoption kit head
cache, expected cache sha `1f1430f3...`); 3 sequential runs
byte-identical (~70s/run): summary `7e69da46`, closure `1a96311e`,
per-root `f83a73c5`. BASE-side pin reproduction: 1 run of the
published class20421 k05 refresh (unchanged bytes, CACHE
`e1a9cacc...`) reproduces the published class20421 k05 reaudit
outputs (summary `dae1f1b3`, closure `a33f0cb9`, per-root
`ecfe4a0c`) byte-for-byte plus the BASE worklist regen pin
`09865553` / 3,714,021 B (executed BEFORE the declaration as the
standing disclosed anchor; reads BASE bytes only). Measurer:
structural adaptation of the class20421 k05 measurer with expected
values pinned from the first measured run; 3 runs byte-identical
(census json `b7a70814...`); external tamper battery 4/4
fail-closed (MT1 SCEN-cache verdict flip caught by the SCEN cache
sha pin, MT2 BASE closure csv byte-tamper caught by the BASE
closure pin, MT3 adoption-manifest byte-tamper caught by the
manifest pin, MT4 SCEN worklist row deletion caught by the SCEN
worklist pin - each aborted at its own pin BEFORE the census json
was written; census json sha snapshot `b7a70814...` unchanged
throughout) + clean control re-PASS byte-identical.

## Honest disclosures

- The measurer is a structural adaptation of the published
  class20421 k05 measurer (`868d8b39` kit, byte-verified raw fetch
  this session): kit paths, pins, adopted-row constants, expected
  flip/ladder/greedy/update8 values, the flip-block semantics
  (owner-union EQUALS flip list here vs strict subset at k05),
  the win-hit-group block (grows 35 -> 40 here) and the verdict
  block were rewritten; the census recount logic, tamper battery
  and assertion chain are otherwise byte-identical computation.
- The declaration's update8 win-hit-group prediction (unchanged
  35 -> 35) did NOT hold; the measured 35 -> 40 growth is disclosed
  above and in the census json verdict block. Everything else in
  the pre-registered prediction (2 flips, census counts, ladder
  stay 797 with no exit, worklist -1, resolved +1) holds exactly.
- The standard 11x11 empty board, the 19 central-reply roots, the
  two-stone root {60,27} and third moves 100/108 stay UNKNOWN.
  This lane runs without access to the user's computer
  (scheduled task); publication is via the GitHub API only.

## Files

- `DECLARATION.md` - the published declaration (copy).
- `README.md` - this file.
- `MANIFEST.txt` - sha256 of every published kit file.
- `output/census-deltas-twentieth-k01-adoption.json` - the census
  deltas (3 byte-identical measurer runs).
- `output/tamper-battery-stdout.log` - the external tamper battery
  outcome log (4/4 fail-closed + clean control).
- `reaudit/output/refresh-summary.json` - the SCEN refresh summary.
- `reaudit/output/closure-classes.csv` - the SCEN closure ladder
  (797 rows).
- `reaudit/output/per-root-coverage.csv` - the SCEN per-root
  coverage.
- `reaudit/scripts/refresh-adoption-twentieth-k01.py` - the
  3-region byte-clone refresh.
- `scripts/measurer-adoption-twentieth-k01.py` - the fail-closed
  measurer.
- `reaudit/output/probe-worklist.csv` - UNPUBLISHED per size
  policy, pinned by sha256 only in MANIFEST.txt.

## Status guard

Adoption reaudit bookkeeping only: NO verdict consumed. Even with
the flips and the ladder stay measured, class-status flips are
census bookkeeping, NOT class closures and NOT root verdicts. The
standard 11x11 empty board, the 19 central-reply roots, the
two-stone root {60,27} and third moves 100/108 stay UNKNOWN.
Nodes/expansions are bookkeeping, never verdicts.
