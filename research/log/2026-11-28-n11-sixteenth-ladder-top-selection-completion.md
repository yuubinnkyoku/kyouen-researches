# 2026-11-28 n11 sixteenth ladder-top selection completion

Completion log for the sixteenth closure-ladder top-candidate
selection, declared single-owner publish-then-execute at
`a178dd64` (declaration log
`research/log/2026-11-28-n11-sixteenth-ladder-top-selection-declaration.md`),
kit published at `b4e338aa`
(`research/experiments/n11-sixteenth-ladder-top-selection-20261128/`,
14 files, fetch-back 14/14 byte-identical at commit pin
`b4e338aa`).

## Executed and measured

- Head basis: `58110025...` (fifteenth k02 adoption, 6,900 rows WIN 218
  / LOSS 6,682); ladder basis: the published fifteenth k02 adoption
  reaudit closure ladder `e10b5765...` (798 rows).
- 798/798 ladder rows' unknown_now recomputed from graph `54f9c364`
  + head + update8 receipts `b658290a`: exact match, zero deviation.
- Top-5 gated exactly as pre-registered: 20421 (5) / 34269 (11) /
  12264 (33) / 5343 (46) / 13342 (50); scanned ranks 1-12.
- Selection: class 20421 `1155173304420536320:131072`, 5 remaining
  unknown S5 keys, all UNCLAIMED, fresh, quarantine-free, 5-stone,
  D4-canonical, canonical-safe, none in probe-13 supply:
  k01 `1155454779397246976:131072` (s5 528689, legal 76),
  k02 `1156299204327378944:131072` (s5 543795, legal 73),
  k03 `1155173441859489792:131072` (s5 605961, legal 73),
  k04 `1153062242096250880:540672` (s5 620742, legal 83),
  k05 `1152921642046849024:68719477248` (s5 625899, legal 78);
  dual legal derivation Board vs fresh 4x4-determinant: 76/76, 73/73,
  73/73, 83/83, 78/78.
- Selector `select_sixteenth_ladder_top.py` sha256 `040a7440...`
  (structural adaptation of the fifteenth instrument `2ebdf573...`,
  claim machinery extended with the adopted fifteenth k01/k02/k03
  as `fifteenth_3`): 45 fail-closed gates PASS; 3 cold runs
  byte-identical (run json sha256 `17c8765d...`).
- Tamper battery 5/5 fail-closed at the intended computational gates
  (T1 closure rank-1 unknown_now flip 5->4 -> P2 recomputation +
  top-5; T2 head row deletion -> P1 head-shape + P3 fifteenth-adopted;
  T3 claim duplicate -> P3 fourteenth-adopted + P4 selection displaced
  to 34269; T4 graph s4_cost child removal -> P2 + P4; T5 update8
  receipt deletion -> P1 update8-receipts + P2); clean control re-PASS
  byte-identical; all tampered pinned inputs restored byte-identical.
- Pre-pass disclosure honored: one full-battery pre-pass run before
  the declaration pre-registered the expectations; the declared
  3-run execution agrees byte-for-byte; zero deviation.

## Disclosure (bookkeeping)

The declaration's HEAD pin cites `03f52eba` (the fifteenth k02
reaudit completion).  Two fast-lane n6q8 commits (`00a9e6f5`,
`8f5b7dcb`, `0da7990b`) landed on main between that pin and the
declaration push, so the declaration commit `a178dd64`'s actual
parent is `0da7990b`.  No sixteenth-selection content was affected:
the cache head-of-record pin `58110025`, the ladder pin
`e10b5765` and all dependency pins are independent of those
commits and verified byte-identical on this host.

## Claim status

Selection and scheduling bookkeeping only: NO verdict is claimed or
implied.  The standard 11x11 empty board: UNKNOWN.  All 19
central-reply roots: UNKNOWN.  Two-stone root {60,27}: UNKNOWN.
Third-move pair {100,108}: UNKNOWN.  Every closure class stays
UNKNOWN.  Legal counts, proxy and nodes are bookkeeping, never
verdicts.
