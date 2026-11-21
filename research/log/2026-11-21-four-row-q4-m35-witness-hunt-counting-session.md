# four-row q4 m35 witness-hunt + w-counting lane, session 1 (part 1: counting tables + verifier)

Date: 2026-11-21 (lane session of the declaration
[a423c2f0](2026-11-21-four-row-q4-m35-witness-hunt-counting-single-owner-note.md),
declaration HEAD `0a76535f98f9df883b376b2987fd44780b542fc3`).

## What was done (this run)

Part 1 of the declared lane, complete and published:

1. **w-general (q=4) counting-class tables (w=3..7).** The K1202 w=3
   mechanism was generalized to w >= 4 rows. During the write-up the supply
   bound argument was tightened into a complete first-principles proof of
   the demand/supply inequality (assignment argument + per-row coverage
   bound: circles meet a row in <= 2 points, non-horizontal lines in <= 1,
   3-on-one-row triples are exactly the horizontal lines of saturated rows
   with zero deficient-row coverage; no appeal to K1202/K0318/K0068 proofs),
   satisfying acceptance condition 1 of the declaration. Tables: 34/55/83/119
   classes for w=4/5/6/7, producer `captable_q4.py` (two implementations,
   assert-equal), verifier `verify_counting_wq4_20261121.py`.
2. **Corollaries.** M_{4,4} <= 237, M_{5,4} <= 567, M_{6,4} <= 1113,
   M_{7,4} <= 1929; certified identity B_max(w)+1 = T_w (K0068 thresholds)
   for w = 3..7; class bands (w=4): alive classes = 15/34 at m >= 35
   (m=35 and m=36), single class (2,3,3,3) at m >= 200. These give direct
   pruning (19 skippable classes) for any future m >= 35 class-split sweep.
3. **Fail-closed machine verifier** (stdlib only, deterministic, fail-closed):
   g_pin (7 sha256-pinned inputs), g_census (independent census: reduced
   integer circumcenter circles + primitive-direction lines; reproduces the
   published 8-case cross-check file including (4,35,4): 413 lines +
   41,194 circles = 41,607, plus 91 record-embedded board censuses in full
   mode, 14 deferred boards honestly listed), g_captable (two implementations
   x pinned expected tables x K1202 w=3 calibration (19 classes) x
   permutation invariance x top claims x B_max+1=T_w), g_witness (all 105
   published witnesses of the four banks (4,4)/(5,4)/(6,4)/(4,5) re-verified:
   safety, maximality, row histograms, class inequality m <= B), g_bands
   (exact alive lists), in-run negative control (wrong band rejected) and
   --tamper mode (table value / band list / census anchor / witness stone
   corruptions all detected; no audit written). Battery: two full runs
   (second in isolated cwd) byte-stable digest `cd7631a5...`,
   PYTHONHASHSEED=random fast run stable, full ~136 s / fast ~5 s.
4. **Published**: experiment dir
   `research/experiments/four-row-q4-m35-witness-hunt-counting-20261121/`
   (README + 2 scripts + 7 pinned inputs + audit/reproduction/tables = 13
   files, every push fetch-back byte-verified), K item
   `research/knowledge/items/K1207-fixed-width-q4-counting-class-tables-w3-w7.md`
   (status: proved; relations toward K1202/K0068/K0833/K0318 only), one
   knowledge README bullet appended, this session log. The declaration note's
   lemma sentence and the experiment README's coverage-bound sentence were
   corrected (wording-only faults caught during the write-up; both files
   re-published with explicit wording-fix commits).

## Honest limits

- Part 2 (the (4,4) m=35/36 neighborhood witness engine) was NOT run this
  session; no witness was found and no absence is claimed at m=35/36.
  The published corpus for the engine (records, class table, alive-15 list,
  canonical circle-key geometry) is verified and ready.
- 14 record census boards (w*m > 140) were deferred in full mode (published
  counts cross-checked for self-consistency only); listed in audit.json.
- The class inequality instances were checked on all 105 witnesses; the
  tables' arithmetic is verified, but the inequality itself is the proved
  lemma now in the K1207 text, not re-proved by the verifier.

## Accidents /-concurrency notes

- No push conflicts occurred; all 13 experiment files + 3 wording fixes
  landed on main with fetch-back byte verification. Other lanes (n11 S5,
  s12/s13 corrections, K1204-K1206) were active during the session and are
  untouched.
- K1204-K1206 were taken during this run's battery; the new item is K1207.

## Next (part 2, next runs of this lane)

- Node.js m=35 neighborhood engine: bases from published witnesses (all 31
  of (4,4)), translations x D4 images, essential-reduce layered search using
  the alive-15-class constraint and the verified canonical circle keys.
- Positive results get 3-system verification (Node BigInt + the Python
  verifier geometry + published sat.js verifyConfig) as per acceptance
  condition 2; every negative stays a bounded local statement.
