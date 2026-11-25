# Session log: five-row q=4 witness band m=40+ (fixed-width high-speed lane)

Date: 2026-11-21. Lane instance: the hourly fast-lane run that declared
`research/log/2026-11-21-five-row-q4-witness-band-40plus-single-owner-note.md`
(commit `6604dbe2`, declared 2026-11-21T17:16Z at HEAD `047d3d51`).

## Timeline of this session

1. **Reconnaissance**: fresh main fetched; AGENTS.md conventions, K0725/K0853
   append-criterion lineage and the four-six-row band-extension witnesses
   (m=37/38/39) confirmed; no other lane had claimed the (5,4) m=40 frontier;
   no five-row-40plus experiment directory existed. The single-owner
   declaration was published with acceptance conditions (>= 2 independent
   integer-verification families; lower-bound-update-only publication;
   T_5=567 unchanged).
2. **R(S) census of the published frontier witnesses** (criterion,
   scan limit 200): m=37 -> R=37 stop (37,0); m=38 -> R=39 stop (39,0);
   m=39 -> R=39 stop (39,1). m=40 was a true frontier (none of the
   published witnesses extends to width 40 by free append). The same
   census post-checked the six-row frontiers: (6,5) m=28 rowY0 witness
   (K1201 records) R=28 stop (28,0), witness widths [24,28];
   (6,6) m=24 witness R=24 stop (24,1), widths [24,24]; (6,7) m=21 witness
   (`six-row-q7-m21-class-split-20261114/output/w67_21.json`) R=21 stop
   (21,2), widths [20,21]. All six-row front lines are genuine; the true
   frontiers are (6,5) m=29, (6,6) m=25, (6,7) m=22, (5,4) m=40 (this
   session's target).
3. **Bounded-edit surgery** (independent Node integer implementation,
   safe-integer canonical curve census): 12 bases (the three published
   witnesses x id/H/V/HV), 5x40 board, budgets single-move (2,604 per
   base), rem2add1, rem2add2 (1,565,655 per base). Result: 64 witness
   hits, all from the m=39-family bases, all kind rem2add2, 14 stones,
   rows [3,2,3,3,3]; 0 witnesses from single-move and rem2add1 on every
   base; 0 from m=37/m=38 bases in every budget. Independent D4 recount:
   64 hits = 16 pairwise-distinct sets, every orbit of size exactly 4.
4. **Positive control**: the control run (5x39 board) rediscovered 2
   witnesses per m=38/m=39-family base image (16 hits), 0 from m=37
   bases; the three published bases themselves pass as witnesses of their
   own boards (criterion: old_uncovered=0, safe). Sensitivity of the
   surgery demonstrated before the main claim was trusted.
5. **Independent verification of the 16 sets**:
   - criterion (Fraction circle equations): 16/16 safe
     (maxline=maxcirc=3), old-column coverage complete, R=40, first
     unblocked (40,1), witness widths [maxx+1,40] with maxx staircase
     {31:1, 34:9, 35:1, 36:2, 37:1, 38:1, 39:1};
   - new third verifier (4x4 integer determinant degenerate-concyclicity,
     Leibniz expansion): 16/16 safe+maximal at width 40, 186 empty cells
     each; positive control (published m=38 witness at width 39) PASS;
     tamper negative control rc=1 with witness 4-set printed.
   Cross-implementation disagreement: none.
6. **Band update**: with published widths 5..39, the (5,4) def-mode
   witness band extends to m=40: M_{5,4} in [41, 567] (T_5 unchanged,
   K1207). R(S)=40 for all 16 sets, so the frontier moves to m=41. One
   set (maxx=31) witnesses widths 32..40 alone: nine consecutive widths by
   a single 14-stone set, the widest single-set staircase recorded for
   (5,4).

## Bug history (all caught before any claim was published)

- Local criterion first draft: reach off-by-one convention (fixed against
  the published K0853 outputs' semantics: R = first unblocked column;
  witness widths [maxx+1, R]).
- `surgery.js` circle membership first draft
  `A*x+B*y+C === D*(x^2+y^2)` (algebraically wrong sign); corrected to
  `A*x+B*y+C+D*(x^2+y^2) === 0` after the Python Fraction second
  implementation flagged a blocker disagreement on cell (0,1) of the
  published m=39 witness.
- `det_witness_verify.py` first draft passed index combinations instead
  of point tuples (TypeError, fixed in the same minute; no output was
  produced by the wrong version).

## Incidents

- Two execution-environment resets during the session. The workspace was
  rebuilt each time (witnesses byte-checked against published stone
  coordinates; scripts rebuilt; surgery re-run to completion with
  identical totals). All published artifacts were (re)generated in the
  final environment and are pinned in `output/sha256s.txt`.

## Handoff to the next runs

- The (5,4) frontier is now m=41: a bounded-edit surgery around the 16
  published width-40 sets (edit budget rem2add2 proved the only fertile
  class here: single-move and rem2add1 gave 0 on every base at m=40, so
  m=41 surgery should start from rem2add2 and wider neighborhoods) is
  the natural next step of this lane. Number of bases is now 16x4 images;
  a smarter neighborhood (targeted at the staircase set with maxx=31,
  which has the most free columns to its right) may pay off.
- The six-row frontiers (6,5) m=29, (6,6) m=25, (6,7) m=22 are confirmed
  genuine; surgery lanes analogous to this one can extend them.
- No completeness claim exists for the width-40 witness population; a
  class-split/full census lane remains open.
- mwq_stabilization.csv is intentionally not updated; any band-table
  update should go through the publication conventions with the K1207
  captable as the upper-bound reference.

## Standard disclaimers

Checked counts and candidate counts are not wins or losses. The 11x11
emptied-board question is untouched by this lane and remains UNKNOWN.
No universal statement was promoted from a finite experiment here.
