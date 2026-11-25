# K1209: the (5,4) witness band extends to m=40 — sixteen three-family-verified width-40 witnesses by bounded-edit surgery, R(S) census of the published five/six-row frontier witnesses, and M_{5,4} in [41, 567]

Date: 2026-11-21
Lane: standard-rule fixed-width q=4, five-row band ("witness band m=40+"
fast lane). Single-owner declaration:
`research/log/2026-11-21-five-row-q4-witness-band-40plus-single-owner-note.md`
(commit `6604dbe2`, 2026-11-21T17:16Z, HEAD-at-declaration `047d3d51`),
with acceptance conditions: >= 2 independent integer-verification
families, lower-bound-update-only publication, T_5 = 567 unchanged.
All conditions were met (three families were used).

## Claims (each machine-verified and exactly scoped)

1. **R(S) census (free-append criterion, exact integer arithmetic).** The
   published (5,4) band-top witnesses m=37/38/39
   (`four-six-row-q4-q5-band-extension-20261115`) have R = 37, 39, 39
   (first unblocked cells (37,0), (39,0), (39,1)): none covers width 40,
   so m=40 was a true frontier of the (5,4) band. The same census on the
   published six-row frontier witnesses: (6,5) m=28 (`s6x28q5_rowY0`)
   R=28, (6,6) m=24 (`s6x24q6_def`) R=24, (6,7) m=21 (`w67_21.json`)
   R=21: all three six-row front lines are genuine (true frontiers
   m=29 / m=25 / m=22). R(S)=m0 means this set stops at m0; nothing is
   claimed about other sets.
2. **Sixteen width-40 (5,4) def-mode witnesses.** Bounded-edit surgery
   (deterministic, seedless; budgets single-move / remove-2+add-1 /
   remove-2+add-2; the last is the only fertile class) on the 5x40 board
   from the 12 D4 images of the three published witnesses produced
   64 hits = **16 pairwise-distinct (mod D4) stone sets** (every orbit of
   size 4), each 14 stones, rows [3,2,3,3,3], safe (maxline=maxcirc=3)
   and maximal on the full 5x40 board (186 empty cells all blocked).
   Verified independently by three integer-implementation families with
   zero disagreement: safe-integer canonical curve census (discovery
   time), Fraction circle-equation criterion (old-column coverage
   complete, R=40, first unblocked (40,1) for all 16), and a new 4x4
   integer-determinant degenerate-concyclicity verifier (16/16 PASS,
   positive control PASS, tamper control fails loudly).
3. **Band update (the only value change).** With widths 5..39 already
   witnessed (K1207 re-verified bank and band-extension witnesses), the
   band now includes m=40:
   **M_{5,4} in [41, 567]** (lower bound: width 40 witnessed; upper
   bound T_5 = 567 from the K1207 demand-supply inequality, unchanged).
   R(S)=40 for all 16 sets (each stops leaving (40,1) free), so the
   frontier moves to m=41. One set (maxx=31) witnesses nine consecutive
   widths 32..40 alone — the widest single-set staircase recorded for
   (5,4); the other 15 cover [35,40], [36,40], [37,40] (x2), [38,40],
   [39,40], [40,40].

## What this is not

- No completeness claim for the width-40 witness population: only the
  declared bounded-edit neighborhoods of the published witnesses were
  searched; witnesses outside them may exist.
- No existence or absence claim at m=41 or beyond: UNDETERMINED. The
  distance from 41 to 567 is open.
- mwq_stabilization.csv is unchanged (K1201 precedent).
- Checked/candidate counts are not wins or losses; the standard 11x11
  empty board is unrelated to this lane and remains UNKNOWN.
- The K1207 inequality and the published witness banks are used as
  verified inputs; not re-derived here.

## Evidence

- Experiment: `research/experiments/five-row-q4-witness-band-40plus-20261121/`
  (README, 3 scripts, 6 input witnesses, 8 raw outputs + sha256 pins;
  fetch-back byte-verified).
- Session log: `research/log/2026-11-21-five-row-q4-witness-band-40plus-session.md`.

## Relations

- Uses K0853 (append criterion lemma and script lineage).
- Uses K1207 (T_5 = 567 upper bound; re-verified witness bank m=5..36).
- Uses the `four-six-row-q4-q5-band-extension-20261115` witnesses
  (m=37/38/39) and K1201 records + `six-row-q7-m21-class-split-20261114`
  (six-row frontier witnesses).
- Negative-space counterpart of the K1208 (4,4) m=35/36 frontier record:
  this lane extends the (5,4) band; both keep the same honesty rules.
