# LAD-GEN: the universal first-stretch-w law of the restricted ladder F(w,h;n)

Experiment date: 2026-11-18. Item: K0934. Object: the first stretch-w of the
family state F(w, h; n) for all w >= 2, 0 <= h <= w, n >= w+1. K0931 proved
the h = 0 case (LAD-h0) and left the class h >= 2, 1 <= r < h open; K0933
proved the w = 4 instance (S4) as part of SIEVE5. This report proves the law
for the full domain: the phase list, the elimination set, the exact end
state, and the watched-position death criterion of the first stretch-w, as
closed forms in (w, h, t, r) where n = (w+1)t + r. The open class of K0931 is
resolved; LAD-h0 and the S4 death table are corollaries.

All statements below are about the K0859 recursion's reduced games only.
Nothing here concerns non-uniform boards.

## Games and vocabulary (reference)

As in K0931/K0933: a state is a cyclic list of holdings, a pointer position
`ptr` (0-based), and a pot p. A phase deals p stones one each to positions
ptr, ptr+1, ... (cyclically); the loser is the position (ptr + p) mod k (k =
active players) read after the deal; the loser's post-deal holding becomes
the new pot; ptr moves to the loser's slot in the shortened list. A
stretch-k is a maximal run of phases whose starting pot is k; a loser
holding exactly the stretch pot dies cold (stretch continues), a loser
holding more dies hot (stretch ends, new pot = holding).

F(w, h; n): n players, the first n-h hold w, the last h hold w+1 ("hot"); pot
w; ptr 0. W_w(n) := F(w, 0; n), H_w(n) := F(w, 1; n), G_w(n) := F(w, 2; n),
T_w(n) := F(w, 3; n). Positions are indices in the ptr-frame circle; the
F(w,h;n) normalization lists the circle from the pointer, cold prefix then
hot suffix. A "uniform" state W_w(n) with all holdings equal is outside the
F-family notation when the pot differs from the holding; we write
W_pot(count) for "count players each holding pot".

Throughout, fix w >= 2, 0 <= h <= w, and write n = (w+1)t + r with t >= 1
and 0 <= r <= w.

## Theorem LAD-GEN (universal, proved)

Let F(w, h; n) be given, n = (w+1)t + r, t >= 1, 0 <= r <= w, and let
J := t if r >= h else t-1 (the number of cold phases). Then the first
stretch-w of F(w,h;n) is exactly as follows.

(a) **Cold blocks.** For each j = 1..J, phase j deals one stone to each of
the original positions (j-1)(w+1), ..., j(w+1)-2 (each of them for the first
time) and eliminates the original position j(w+1)-1, which holds exactly w
(cold death).

(b) **Breaking phase** (phase J+1, the last phase of the stretch; its loser
holds w+1, so the stretch ends and the new pot is w+1), except in the
collapse case:

  - If r < h: ptr is the original position n-r-w-1 = (t-1)(w+1); the deal
    covers the originals (t-1)(w+1), ..., t(w+1)-2 (= n-r-2, no wrap, no
    eliminated position in range); the loser is the original n-r-1, a hot
    player (position n-r-1 >= n-h) never dealt before, holding w+1.
  - If r >= h and r >= 1: ptr is the original position n-r = t(w+1); the
    deal covers the originals t(w+1), ..., n-1 (that is r positions) and
    then wraps to the originals 0, ..., w-r-1 (no eliminated position in
    either range); the loser is the original w-r, a cold player (position
    w-r <= w < n-h) dealt exactly once (block 1), holding w+1.
  - If r = 0 (then h = 0) and t >= 2: ptr is the original 0; the deal covers
    the originals 0, ..., w-1 (all dealt once before, in block 1; none
    eliminated); the loser is the original w+1, a cold player dealt exactly
    once (block 2, if t >= 2; for t = 2 block 2 is the last block and deals
    w+1..2w), holding w+1.
  - **Collapse case** (t, r, h) = (1, 0, 0) (n = w+1, all cold): J = 1 and
    the breaking phase (phase 2) has k = w active players, so q = w//w = 1:
    every survivor (originals 0..w-1, each dealt once in block 1, holding
    w+1) receives one more stone and holds w+2; the loser is the original
    0, holding w+2; the new pot is w+2. The stretch ends in the uniform
    state W_{w+2}(w-1).

(c) **End state** (exact, not just a census). Except in the collapse case,
the survivors, listed from the new pointer, hold exactly

    [w+1]^(n2-h2) followed by [w+2]^h2,   pot w+1,

i.e. the state is exactly F(w+1, h2; n2) in normalization, where

    r < h :  n2 = n - t,      h2 = h - 1 - r,
    r >= h:  n2 = n - t - 1,  h2 = h + w - r   (= (h-1-r) mod (w+1)).

In the collapse case the end state is the uniform state W_{w+2}(w-1)
(w-1 players each holding w+2, pot w+2).

(d) **Elimination set.** The set of positions eliminated during the first
stretch-w is exactly { j(w+1)-1 : 1 <= j <= J } plus the breaking loser of
(b) (the original n-r-1 if r < h; the original w-r if r >= h, r >= 1; the
original w+1 if r = h = 0; the original 0 in the collapse case). The stretch
has J+1 phases (t+1 if r >= h, t if r < h; the collapse case has 2 = t+1).

(e) **Watched criterion.** Assume n >= 2w+2 (i.e. t >= 2) and watch the
original position n-a for a fixed 1 <= a <= w+1. The watched position dies
during the first stretch-w if and only if a = r+1; then it dies in phase t,
cold (holding w) if a >= h+1, hot-final (holding w+1) if a <= h. There is
exactly one exception: (h, r, t, a) = (0, 0, 2, w+1), where the watched
position n-(w+1) = w+1 is the breaking loser of case (b) with r = 0 and dies
hot (holding w+1) in phase t+1 = 3.

## Proof

We use the K0928 Lemma P phase rule throughout. Two frame facts recur: in a
circle where the eliminated originals are exactly {i(w+1)-1 : 1 <= i <= m},
an original x >= m(w+1)-1 that is still active has shortened index x - m;
and after a phase whose loser is at shortened index L, the next pointer is
at shortened index L mod (k-1), i.e. it points at the element that directly
followed the loser.

**Block Lemma (induction on j).** For 1 <= j <= J: before phase j the
eliminated originals are exactly {i(w+1)-1 : 1 <= i <= j-1}, the pot is w,
the circle has k_j = n-(j-1) players, and ptr points at the original
(j-1)(w+1), whose shortened index is (j-1)w. Then phase j runs as claimed
in (a) and restores the four invariants with j+1 in place of j.

*Base.* j = 1: nothing eliminated, k = n, ptr at original 0 = (j-1)(w+1),
shortened index 0 = (j-1)w. 

*Step.* In phase j we have k_j = n-j+1 >= (w+1)t+r-j+1 >= wt+r+1 >= w+1 > w
(using j <= t), so q = pot//k = 0 and rem = w: the deal is the w active
positions starting at ptr. By the induction hypothesis the eliminated
originals i(w+1)-1, i <= j-1, all lie below (j-1)(w+1), and no original in
[(j-1)(w+1), j(w+1)-2] is eliminated (i(w+1)-1 in that interval would force
i >= j and i <= j-1... precisely: i(w+1) >= (j-1)(w+1)+2 forces i >= j, while
i(w+1)-1 <= j(w+1)-2 forces i <= j-1 + (w-1)/(w+1) < j). So the w recipients
are exactly the originals (j-1)(w+1)..j(w+1)-2; each is dealt for the first
time (block i < j dealt only originals <= (j-1)(w+1)-2). The loser is at
shortened index ((j-1)w + w) mod k_j = jw mod k_j; and jw < k_j because
jw <= tw < wt+r+1 <= k_j. By the frame fact its original is jw + (j-1) =
j(w+1)-1 (it lies above all j-1 eliminations). It is active, since the
eliminated originals are <= (j-1)(w+1)-1 < j(w+1)-1. It has never been
dealt (all deals so far ended at (j-1)(w+1)-2), so it holds w if it is a
cold player and w+1 if it is hot. It is cold precisely when
j(w+1)-1 <= n-h-1, i.e. j(w+1) <= n-h = (w+1)t + (r-h): this holds for all
j <= J and fails for j = J+1 (if r >= h, J = t and (t+1)(w+1) > n >= n-h; if
r < h, J = t-1 and t(w+1) > (w+1)t + r - h). So phases 1..J are exactly the
cold block phases, each eliminating j(w+1)-1 with holding w, and phase J+1
would eliminate a hot player or wrap past the end - that phase is the
breaking phase analysed next. The loser's post-pop pointer is jw mod (k_j -
1) = jw (as jw <= tw <= wt+r = k_j - 1 when j <= t... in fact jw <= tw <
n-j+1 - 1 needs j <= t, which holds), which points at the original j(w+1):
the element directly after the loser. In the new frame (j eliminations) its
shortened index is j(w+1) - j = jw. This restores the invariants. ∎ (block
part of (a), and the "J cold phases" count)

**Breaking phase.** The frame before phase J+1 has J eliminations, k =
n-J, ptr at original J(w+1), shortened index Jw.

*Case r < h (J = t-1).* k = wt+r+1 > w, so q = 0, rem = w. The deal is the
w active positions from ptr: the originals (t-1)(w+1)..t(w+1)-2; the upper
end is n-r-2 <= n-1 (no wrap), no eliminated original lies in the interval
(block losers are <= (t-2)(w+1)-2... in fact i(w+1)-1 in [(t-1)(w+1),
t(w+1)-2] would force i >= t and i <= t-1, impossible), and none of them
was dealt before (blocks dealt only originals <= (t-1)(w+1)-2). The loser is
at shortened index (tw) mod (wt+r+1) = tw (no mod since tw < wt+r+1),
original t(w+1)-1 = n-r-1; it is active (block losers are <= (t-1)(w+1)-1)
and hot since n-r-1 >= n-h (r <= h-1); it was not dealt (the breaking deal
ends at n-r-2, blocks ended at (t-1)(w+1)-2 = n-r-w-2), so it holds w+1:
a hot death, the stretch ends, the new pot is w+1. This proves (b) case 1.

*Case r >= h, r >= 1 (J = t).* k = wt+r > w, so q = 0, rem = w. The deal
from ptr (original t(w+1), shortened tw) covers the active originals
t(w+1)..n-1 (r positions; the last original is n-1 = t(w+1)+r-1, so this
segment fills exactly r slots, then the circle wraps) and continues at the
originals 0..w-r-1 (w-r positions; none of them is eliminated, since the
smallest eliminated original is w and w >= w-r). None of the first segment
is eliminated (all block losers are <= t(w+1)-1 < t(w+1)) and none was
dealt this stretch... they are dealt here for the first time except that
the hot players among them are exactly the hot tail [n-h, n-1] (n-h =
t(w+1)+r-h >= t(w+1) since r >= h), all inside the first segment. The
originals 0..w-r-1 were each dealt once in block 1 and now receive a second
stone. The loser is at shortened index (tw + w) mod (wt+r) = w-r (since
tw+w = wt+r + (w-r) and 0 <= w-r < wt+r), i.e. the original w-r: no block
loser lies at or below w-r-1... precisely, i(w+1)-1 <= w-r-1 would force
i(w+1) <= w-r <= w < w+1, impossible; so the shortened index w-r is the
original w-r itself. It is cold (w-r <= w-... n-h >= t(w+1) >= w+1 > w-r),
was dealt exactly once (block 1 deals 0..w-1; the breaking deal covers
t(w+1)..n-1 and 0..w-r-1, neither containing w-r), so it holds w+1: a hot
death, new pot w+1. This proves (b) case 2.

*Case r = h = 0, t >= 2 (J = t).* After block t the eliminated originals
are i(w+1)-1, i <= t; the last one, t(w+1)-1 = n-1, is the final original.
The loser of block t was at shortened index tw; the new pointer is
tw mod (n-t) = tw mod (wt) = 0, i.e. the original 0 (the circle wraps to
its front). Phase t+1: k = wt > w (t >= 2), q = 0, rem = w: the deal is the
originals 0..w-1 (none eliminated; each was dealt once in block 1). The
loser is at shortened index w mod wt = w, which is the original w+1
(originals 0..w-1 occupy shortened 0..w-1 and original w is eliminated, so
shortened w is the original w+1). It is cold, was dealt exactly once (block
2 deals w+1..2(w+1)-2, which contains w+1; the breaking deal is 0..w-1), so
it holds w+1: hot death, new pot w+1. This proves (b) case 3.

*Collapse case (t, r, h) = (1, 0, 0).* n = w+1, all holdings w. Block 1
(J = 1): k = w+1 > w, q = 0, rem = w: deal 0..w-1, loser at (0+w) mod (w+1)
= w, the original w, holding w (cold). Phase 2: k = w, pot w, so q = 1,
rem = 0: every survivor (originals 0..w-1, each holding w+1 after block 1)
receives one more stone and holds w+2; the loser is at (0 + w) mod w = 0,
the original 0, holding w+2. The new pot w+2 differs from w, so the stretch
ends after 2 = t+1 phases in the uniform state W_{w+2}(w-1). This proves
(b) case 4 and (c) collapse.

**End state (c).** We track who holds what at the end and in which order the
survivors are listed from the new pointer.

*Case r < h.* Eliminated: the block losers i(w+1)-1 (i <= t-1) and the
breaking loser n-r-1; n2 = n-t survivors, pot w+1. The stretch's deals are
the originals 0..n-r-2 minus the block losers (blocks cover 0..(t-1)(w+1)-2
minus earlier block losers; the breaking phase covers (t-1)(w+1)..t(w+1)-2 =
n-r-2... jointly: every original in [0, n-r-2] except a block loser is
dealt exactly once, and no original is dealt twice). The survivors in
[n-r, n-1] are undealt. Holdings: cold survivors (originals < n-h, minus
block losers) hold w+1; hot survivors split: those in [n-h, n-r-2] are dealt
once and hold w+2 (h-r-1 of them), those in [n-r, n-1] are undealt and hold
w+1 (r of them). So exactly h2 = h-1-r survivors hold w+2. The new pointer:
the breaking loser was at shortened index tw; the new pointer is tw mod
(n-t) = tw (tw < wt+r+1 = n-t+1, and tw <= wt < wt+r+1... tw mod (n-t):
n-t = wt+r+1 > tw, so the pointer is tw), pointing at the original
t(w+1) = n-r. So the survivor circle, from the pointer, is
[n-r, n-1] (r players, w+1), then [0, ..., n-r-2] skipping block losers
(cold survivors hold w+1, in original order), and the dealt hot survivors
[n-h, n-r-2] come last in this second segment and hold w+2. Since all w+2
holders are the largest originals of the second segment, the circle reads
[w+1]^(n2-h2) followed by [w+2]^h2: exactly F(w+1, h-1-r; n-t). ∎

*Case r >= h, r >= 1.* Eliminated: block losers i(w+1)-1 (i <= t) and the
original w-r; n2 = n-t-1 survivors, pot w+1. Deals: blocks cover 0..
t(w+1)-2 minus block losers i <= t-1; the breaking phase covers
t(w+1)..n-1 (which contains the whole hot tail [n-h, n-1], since n-h =
t(w+1)+r-h >= t(w+1)) and the wrap 0..w-r-1. So: the originals 0..w-r-1 are
dealt twice (block 1 + breaking wrap), the originals w-r+1..n-1 minus block
losers are dealt exactly once, the original w-r is eliminated. No hot player
is eliminated (the breaking loser w-r and all block losers are cold), and
every hot player is dealt exactly once (breaking first segment): all h hot
survivors hold w+2, and the w-r double-dealt colds hold w+2. So h2 =
h + (w-r) = h+w-r survivors hold w+2. The new pointer: the breaking loser
was at shortened index w-r; the new pointer is (w-r) mod (wt+r-1) = w-r
(since w-r <= w-1 < wt+r-1... w-1 < wt+r-1 holds as 1 < w(t-1)+r+... for
t >= 2 clear; for t = 1, wt+r-1 = w+r-1 >= w > w-r as r >= 1), pointing at
the original w-r+1 (the element after the eliminated w-r; note the original
w further along is eliminated). The circle from there: colds w-r+1..n-h-1
(plus the colds after eliminated block losers) hold w+1, then the hot tail
[n-h, n-1] holds w+2 (h players, consecutive), then the wrap segment
0..w-r-1 holds w+2 (w-r players, consecutive), and the circle closes. The
two w+2 segments are adjacent across the wrap-end of the circle, so the
circle from the pointer reads [w+1]^(n2-h2) followed by [w+2]^(h+w-r):
exactly F(w+1, h+w-r; n-t-1). ∎

*Case r = h = 0, t >= 2.* Eliminated: block losers i(w+1)-1 (i <= t) and the
original w+1; n2 = wt-1 survivors, pot w+1. Deals: blocks cover
0..n-2 = t(w+1)-2 minus block losers i <= t-1; the breaking phase covers
0..w-1 a second time. The original n-1 = t(w+1)-1 is block t's loser.
Survivors: 0..w-1 hold w+2 (double-dealt), the originals w+2..n-2 minus
block losers i = 2..t-1 hold w+1. So h2 = w survivors hold w+2. The new
pointer: the breaking loser was at shortened index w; the new pointer is
w mod (n-t-1) = w (as w < wt-1 for t >= 2), pointing at the original w+2
(originals 0..w-1 then the eliminated w, w+1 behind it). The circle from
there: [w+2..n-2 minus block losers] hold w+1, then the wrap 0..w-1 hold
w+2: exactly F(w+1, w; wt-1). ∎ (This is the r = 0 line of LAD-h0.)

**Elimination set (d).** Immediate from the block lemma and the breaking
case analysis: the phases of the stretch are exactly the J blocks and the
breaking phase; the phase count is J+1. ∎

**Watched criterion (e).** Assume t >= 2, 1 <= a <= w+1. The watched
original n-a dies in the first stretch-w iff n-a is in the elimination set
(d). n-a = i(w+1)-1 for some i <= J iff (w+1)t + r - a = i(w+1) - 1, which
forces a = r+1 and i = t; that i is allowed (t <= J) iff r >= h, and then
the death is phase t, cold, holding w (block lemma). If r < h, the breaking
loser n-r-1 is the watched position iff a = r+1: death in phase t = J+1,
hot, holding w+1. So for a = r+1 the watched always dies, in phase t, cold
iff a >= h+1, hot-final iff a <= h. Conversely, for a ≠ r+1 the watched
position is no block loser; it remains to check the r >= h breaking
losers, which live at the far end of the circle: the original w-r (r >= 1)
is the watched n-a iff a = (w+1)t + 2r - w, which for t >= 2 exceeds w+1
(a >= 2(w+1) - w = w+2), outside the watched range; the original w+1
(r = 0, h = 0) is the watched n-a iff a = (w+1)(t-1), which is <= w+1 iff
t = 2. That single surviving coincidence, (h, r, t, a) = (0, 0, 2, w+1),
is the exception: the watched n-(w+1) = w+1 is the breaking loser of case
(b), dies hot (holding w+1) in phase t+1 = 3. (For t >= 3 the breaking
losers are again outside the watched range.) The hypothesis n >= 2w+2 is
exactly what excludes the t = 1 wrap collisions. ∎

## Corollaries

**LAD-h0 (K0931, regression).** For h = 0: r = 0 (t >= 2) gives the end
state F(w+1, w; wt-1); r >= 1 gives F(w+1, w-r; wt+r-1); (t, r) = (1, 0)
collapses to W_{w+2}(w-1). These are exactly the LAD-h0 lines of K0931,
now re-derived inside LAD-GEN. (Machine-checked: LG6, 903 cases.)

**Open class of K0931 resolved.** The class h >= 2, 1 <= r < h - the last
open residue class of the restricted ladder - is case 1 of the breaking
phase and case 1 of the end state: breaking loser n-r-1 (hot), end state
F(w+1, h-1-r; n-t). No class of the first stretch-w law remains open.

**S4 of K0933 (regression).** w = 4. The four families and their watched
positions: W4(n) = F(4,0;n) watched a=1; F(4,1;n) watched a=1;
F(4,2;n) watched a=3; F(4,3;n) watched a=3. By (e): W4's watched dies iff
r = 0 (a = r+1 = 1), cold, phase t; F(4,1)'s watched dies iff r = 0,
hot-final (r < h), phase t; F(4,2)'s watched dies iff r = 2, cold
(r >= h), phase t; F(4,3)'s watched dies iff r = 2, hot-final (r < h),
phase t. These are exactly the S4 death table rows of K0933, including the
cold/hot-final and death-block-t columns. (Machine-checked: LG7, 580
cases.) The S4 length formula (n-a)//5 + 1 also follows: if the watched
dies, its death phase is t = n//5 and (n-a)//5+1 = t because
0 < a <= 5 (a = r+1 <= 5 forces (r-a)//5 = -1); if it survives, the family
constraint links the two sides: for a = h+1 the surviving residues satisfy
r ≠ h, so r >= h iff r >= h+1 = a iff a <= r, and (n-a)//5+1 = t+1 iff
a <= r iff r >= h iff the stretch length is t+1; the same equivalence
(r >= h iff a <= r) holds for a = h on the surviving residues r ≠ h-1.

**Ladder recursion.** Outside the collapse, the first stretch maps
F(w,h;n) to F(w+1, (h-1-r) mod (w+1); n-t-[r >= h]) - one closed step of
the ladder w -> w+1 -> w+2 -> ... The two-stretch composition is
machine-checked directly (LG8): the stretch-2 closed forms (w' = w+1,
applied to the claimed end state) match the continued simulation of the
same game, for every w <= 5, h <= w, n <= 90 with h2 <= w+1 (the LAD-GEN
domain of the second stretch).

## Machine verification (ladder_gen_verify.py, audit_build.py)

`ladder_gen_verify.py` implements the K0928 phase-rule simulator and the
closed forms above, and checks LG1-LG8 over the full grid
w in 2..7, h in 0..w, n in w+1..155 (every residue r, every family, 4,949
games):

  - LG1 first-stretch length (J+1 phases; collapse 2);
  - LG2 every cold block: exact deal set, loser, holding (68,411 blocks);
  - LG3 the breaking phase: ptr, exact deal set, loser, holding (4,949);
  - LG4 the exact end-state circle (holdings list equality, not just
    multiset) and end pot (4,949);
  - LG5 the elimination set (4,949) and the watched criterion (e) with its
    exception, for every n >= 2w+2 and 1 <= a <= w+1 (28,470 checks);
  - LG6 LAD-h0 regression, h = 0 (903 cases);
  - LG7 S4 regression: death tables, cold/hot-final, death phase, length
    formula, for n = 11..155 (580 cases);
  - LG8 two-stretch handoff: stretch 2 predicted from the claimed end
    state via LAD-GEN (w' = w+1) against the direct simulation, w <= 5,
    n <= 90 (1,503 games, 8,924 stretch-2 block checks).

`audit_build.py` runs the full check suite twice in-process, asserts both
runs agree, and writes the deterministic audit `output/ladder_gen_audit.json`
(no timestamps, sorted keys). Result: all_ok = true, fail_count = 0,
runs_identical = true; audit sha256
52cbab9aa98095044e254b6d9355d340e68840e6fc51a809a6e4c9e95fa01d36
(2026-11-18); two cold invocations produce byte-identical audits.

The proofs above are paper proofs; the script is the machine anchor, not the
proof. The paper proof covers all w >= 2, 0 <= h <= w, t >= 1; the grid is a
finite witness, not the argument.

## Limitations

- Domain: w >= 2, 0 <= h <= w, n >= w+1. The watched criterion (e) needs
  n >= 2w+2 (t >= 2); for t = 1 the breaking loser can collide with watched
  positions (excluded by hypothesis, not analysed).
- The end state (c) is exact, but the ladder RECURSION (applying LAD-GEN to
  the next stretch) needs the next state in-domain: h2 <= w+1 (i.e. h <= r+1
  on the r >= h side) and n2 >= w+2. LG8 covers exactly that subgrid; the
  h2 > w+1 exits (e.g. w large, h = w, r small) leave the F-family notation
  (more w+2-holders than the denomination gap) and are not iterated here.
- The collapse case (t, r, h) = (1, 0, 0) exits the ladder into the uniform
  state W_{w+2}(w-1), a jump w -> w+2 with a different structure (uniform
  states are their own lane); it is covered as a closed form but not
  iterated.
- Watched tracking ACROSS stretches (the SIEVE machinery: where the watched
  position lands in the new circle, and its new a) is not part of LAD-GEN;
  K0933's S3/S4 did this by hand for w = 3, 4. Applying LAD-GEN to SIEVE7
  (spf = 7, stretch-6 tracking from the S3 end states) is the natural next
  step: the per-stretch law is now universal, so only the watched-position
  bookkeeping across the finitely many (n mod 42) residue classes remains.
- Not run: `uv run check/build`, unittests (no clone/uv in this
  environment). generated/ and the root README untouched.
