# WATCH-MAP: where a surviving watched position lands in the next ladder state

Experiment date: 2026-11-18. Item: K0935. Object: the mapping of a watched
position across the first-stretch-w boundary of the restricted ladder
F(w,h;n), i.e. the bookkeeping primitive that K0933 had to do by hand in
S3/S4 and that SIEVE7 (spf = 7, stretch-5/6 tracking) needs in general.
K0934 (LAD-GEN) proved the first-stretch law including the exact end-state
census; this report reads the watched position off that census and proves
a closed form for its position in the NEW circle, then states and
machine-checks the composition: the watched's death in the second stretch
is decided by LAD-GEN applied to the new state at the mapped position.

All statements below are about the K0859 recursion's reduced games only.
Nothing here concerns non-uniform boards.

## Setup and statement

Fix w >= 2, 0 <= h <= w, n = (w+1)t + r with t >= 2 (i.e. n >= 2w+2), and
watch the original position n-a for 1 <= a <= w+1. Assume the watched
SURVIVES the first stretch-w: by LAD-GEN (e) this means a != r+1, and
(h,r,t,a) != (0,0,2,w+1) (the single exception, which dies). Let n2, h2 be
the LAD-GEN end-state parameters:

    r < h :  n2 = n - t,      h2 = h - 1 - r,
    r >= h:  n2 = n - t - 1,  h2 = h + w - r   (and h2 = w when r = h = 0),

so the end state is exactly F(w+1, h2; n2), the circle being listed from
the new pointer (LAD-GEN (c)).

**Lemma WATCH-MAP (universal, proved).** The watched position's index in
the new ptr-frame circle - i.e. its position in the F(w+1,h2;n2)
normalization - is exactly n2 - a2, where:

    r < h,  a <= r    :  a2 = n2 - r + a     (front segment),
    r < h,  a >= r+2  :  a2 = a - r - 1      (long segment),
    r >= h, r >= 1, a <= r    :  a2 = a + w - r     (cold prefix),
    r >= h, r >= 1, a >= r+2  :  a2 = a + w - r - 1,
    r = h = 0, a <= w       :  a2 = w + a - 1
                              (a = w+1 is the dead exception).

(The case a = r+1 is absent because the watched dies there.)

**Corollary WM-COMP (the SIEVE bookkeeping primitive).** The watched dies
in the SECOND stretch (the first stretch-(w+1)) if and only if the position
n2 - a2 belongs to the LAD-GEN elimination set of F(w+1, h2; n2) (its
blocks { j(w+2)-1 } plus its breaking loser), with the phase and holding of
that elimination. In the watched range a2 <= w+2 this reduces to the
LAD-GEN criterion: dies iff a2 = r2 + 1, where r2 = n2 mod (w+2), cold iff
a2 >= h2+1, hot-final iff a2 <= h2. Iterating (WATCH-MAP + LAD-GEN) tracks
the watched through stretches w, w+1, w+2, ... by pure arithmetic on
(w, h, n, a) - no simulation.

## Proof

All three cases read the segment structure of the end circle off the
LAD-GEN end-state proof (K0934 report, section "End state (c)"). We use
twice: the new-frame index of a surviving original x equals its rank among
the survivors, listed from the new pointer.

**Case r < h.** The end circle is [n-r, ..., n-1] (the r undealt hot
survivors, in original order) followed by [0, ..., n-r-2] with the block
losers { i(w+1)-1 : i <= t-1 } removed, then the circle closes.
- If a <= r, the watched original n-a = n-r+(r-a) lies in the front segment
  at index r-a, so a2 = n2 - (r-a) = n2 - r + a.
- If a >= r+2, the watched lies in the long segment. Its index there is
  r + (n-a) - #{ eliminated originals < n-a }. The eliminated originals
  below it are exactly the t-1 block losers: (t-1)(w+1) <= n-a holds
  (equivalent to a <= r+w+1, true since a <= w+1), while the breaking loser
  n-r-1 lies above it (a >= r+2). Hence index = r + n - a - (t-1) and
  a2 = (n-t) - (r+n-a-t+1) = a - r - 1.

**Case r >= h, r >= 1.** The end circle runs from the original w-r+1 up to
n-1 (the block losers { i(w+1)-1 : i <= t } removed; the breaking loser
w-r lies below the start), then the wrap segment 0..w-r-1, then closes.
For a <= w+1 and t >= 2 the watched original n-a >= n-w-1 = t(w+1)+r-w-1
lies above the wrap segment (t >= 2 gives n-a >= (w+1)+r-1 > w-r-1), so it
is in the main segment at index (n-a) - (w-r+1) - E, where E = #{ i <= t :
i(w+1)-1 in [w-r+1, n-a-1] } = #{ i <= t : i(w+1) <= n-a } (every block
loser is >= w >= w-r+1 since r >= 1). For i = t: t(w+1) <= t(w+1)+r-a holds
iff a <= r. So E = t if a <= r, E = t-1 if a >= r+2. Then
a2 = (n-t-1) - (n-a-w+r-1-E) = a+w-r-t+E, i.e. a2 = a+w-r for a <= r and
a2 = a+w-r-1 for a >= r+2.

**Case r = h = 0 (t >= 2).** The end circle runs from the original w+2 to
n-2 (the block losers { i(w+1)-1 : 2 <= i <= t-1 } removed; the eliminated
w, w+1 lie below the start, the block t loser n-1 above the end), then the
wrap 0..w-1. The watched (a <= w; a = w+1 is the dead exception) lies in
the main segment at index (n-a) - (w+2) - E with E = #{ i in [2, t-1] :
i(w+1) <= n-a } = t-2 (for i in [2, t-1]: (t-1)(w+1) <= t(w+1)-a holds
iff a <= w+1). So index = n-a-w-t and, with n = t(w+1) and n2 = wt-1:
a2 = (wt-1) - (t(w+1)-a-w-t) = w+a-1. ∎

**WM-COMP.** The end state is exactly F(w+1,h2;n2) in the new frame
(LAD-GEN (c)); the watched's index there is n2-a2 (WATCH-MAP); the second
stretch's elimination set, in that frame, is the LAD-GEN set of
F(w+1,h2;n2) (LAD-GEN (d)). ∎

## The w = 4 tables (SIEVE7 input)

For the four weight-4 families of K0933's S4 (watched position n-a,
surviving residues r = n mod 5 only), WATCH-MAP gives the a2 table of the
stretch-5 state F(5, h2; n2):

- W4(n) = F(4,0;n), a = 1: r >= 1 survives with a2 = 5-r (h2 = 4-r,
  n2 = 4t+r-1); r = 0 is the dying residue (S4), not mapped.
- F(4,1;n), a = 1: r >= 1 survives with a2 = 5-r (h2 = 5-r, n2 = 4t+r-1);
  r = 0 dies (S4).
- F(4,2;n), a = 3: survives r in {0,1,3,4} with a2 = 2, 1, 4, 3
  respectively (r < h for r in {0,1}: h2 = 1-r, n2 = 5t+r-t; r >= h for
  r in {3,4}: h2 = 6-r, n2 = 4t+r-1); r = 2 dies (S4).
- F(4,3;n), a = 3: same a2 table {r=0: 2, r=1: 1, r=3: 4, r=4: 3}
  (h2 = 2-r for r in {0,1}, h2 = 7-r for r in {3,4}, n2 as above);
  r = 2 dies (S4).

Applying the stretch-5 criterion (dies iff a2 = r2+1, r2 = n2 mod 6) to
these tables and iterating once more is exactly the SIEVE7 computation
(m mod 42 classes); it is left to the next report.

## Machine verification (watchmap_verify.py, audit_build.py)

The LAD-GEN core (simulator + first-stretch closed forms) is copied
verbatim from the published K0934 verifier; the new content is
watchmap() (the closed form above) and two checks over the full grid
w in 2..7, h in 0..w, n in w+1..155:

  - WM1: for every n >= 2w+2 and 1 <= a <= w+1 whose watched survives (per
    the proved criterion (e), exception included): the watched's index in
    the simulated end circle equals n2 - a2 (23,714 checks, 0 failures).
  - WM2: composition: the watched dies in the simulated second stretch
    iff n2 - a2 is in the LAD-GEN elimination set of F(w+1,h2;n2), with
    matching phase and holding (23,713 checks, 0 failures; skipped where
    stretch 2 leaves the LAD-GEN domain).

audit_build.py runs the suite twice in-process, asserts agreement, and
writes the deterministic audit output/watchmap_audit.json (no timestamps,
sorted keys): all_ok = true, fail_count = 0, runs_identical = true; file
sha256 024d86211a1a72f5c26f395b78d4e10d727594bb006190c357c10d9b1a27c36b
(2026-11-18); two cold invocations produce byte-identical audits.

The proofs above are paper proofs; the script is the machine anchor, not
the proof.

## Limitations

- Domain: as LAD-GEN plus t >= 2 (n >= 2w+2) and 1 <= a <= w+1; the
  watched must survive the first stretch (a = r+1 and the exception
  (0,0,2,w+1) are deaths, not mapped).
- The map is into the F-family end state; the collapse case (t,r,h) =
  (1,0,0) never occurs here (t >= 2), and h2 > w+1 end states are mapped
  fine by WATCH-MAP itself but leave the LAD-GEN domain for the NEXT
  stretch's death criterion (WM2 skips exactly those points).
- The a2 <= w+2 reduction of WM-COMP is the watched-range criterion; for
  larger a2 (possible when a + w - r - 1 > w+2) the full elimination-set
  membership must be used (WM2 does exactly that).
- Not run: `uv run check/build`, unittests (no clone/uv in this
  environment). generated/ and the root README untouched.
