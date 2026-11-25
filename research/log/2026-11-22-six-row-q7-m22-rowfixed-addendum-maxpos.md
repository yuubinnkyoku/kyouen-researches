# Addendum to the single-owner declaration: maxpos refinement for cap-resistant minpos leaves

Date: 2026-11-22 (UTC). Lane: fast lane, six-row (6,7) 6x22 rowfixed y-split decision sweep.
Parent declaration: `2026-11-22-six-row-q7-m22-rowfixed-single-owner-note.md` (commit 24a98f89).
Addendum-time HEAD: 0e858300e747eee5d0fc3adad0a22f9d6ec0c463 (latest main re-fetched immediately before this push).

## Registered refinement (extends the declared refinement ladder)

`--maxpos=V`: pin the RIGHTMOST stone of the pinned row Y at column V, adding unit clauses
-cell[Y][x] for x > V and +cell[Y][V].

Applicability: only for leaves whose parent instance (rowfixed k-exact + minpos leaf)
already hit the time cap as INDET. First known such leaf: rf(6,22,7) y2k3 minpos=0
(INDET 4,136,258 conflicts at the 255 s cap).

## Soundness argument (complete refinement, no symmetry invoked)

Within a minpos leaf (row Y exact count k >= 1, leftmost stone x_l = P), every configuration
has a well-defined rightmost stone x_r with x_r in [P, m-1]. The V-leaves for V = P..m-1
(requires V >= P) are pairwise disjoint and their union is the whole parent leaf: a disjoint
exhaustive partition by equality of x_r. All-leaves-UNSAT implies parent-leaf UNSAT.

DONE (refinement closure rule): a minpos leaf counts as decided UNSAT only when (a) the plain
leaf terminates UNSAT, or (b) all its V-leaves terminate UNSAT. INDET of some V-leaf keeps the
parent leaf open (no absence claim).

## Explicit non-combination

`--maxpos` (and `--minpos`) must NOT be combined with `--lex=H`: H maps x_l -> m-1-x_r,
so minpos/maxpos leaf solution sets are not H-invariant, and H-orbit lex-leader constraints
can drop in-leaf solutions. lex=H remains sound for rowfixed k-exact instances without
minpos/maxpos (H preserves rows and row stone counts), as used for the y2k2_lexH cross-check.

## Controls required before any maxpos leaf counts toward the decision

1. Encoder regression: modified sat_rf.js must regenerate the published CNFs bit-exactly
   (3 representative pins: y2k0 plain, y2k2p5 minpos, y2k2_lexH; md5 match vs records).
2. Negative control: rf(6,22,8) rowY=0 k=1 minpos=0 maxpos=21 MUST be UNSAT (it is a subset of
   the calibration instance cal2 rowY=0, published value UNSAT 337,741 conflicts, reproduced
   bit-exact earlier this session). Any SAT here invalidates the mechanism.
3. Positive control: rf(6,21,7) rowY=2 k=5 minpos=1 maxpos=20 MUST be SAT (it contains the
   cal4 witness whose row 2 stones are [1,16,17,19,20], triple-verified this session), and the
   decoded witness must pass both verification systems with row-2 leftmost=1, rightmost=20,
   exactly 5 stones in row 2.

All other terms of the parent declaration (verdict semantics, non-goals, calibration set,
K-item-only-on-completion, parallel-run policy) remain unchanged.
