# SIEVE5-U/V: the stretch-3/stretch-4 structure of the U/V reduced games, the p = 5 instance of SIEVE, and the twin laws' spf-in-{3,5} (mod 30) resolution

Experiment date: 2026-11-18. Item: K0933. Object: the reduced games U(m)/V(m)
of K0928 Theorem RED (P(2m+2) = 3 + 2U(m), P(2m+1) = 1 + 2V(m)), continuing
K0931. K0931 proved the stretch-2 structure (STR2-V/U), the p = 3 instance of
the SIEVE conjecture (SIEVE3-V/U), the twin laws on the mod-6 classes
(LAW1-mod6/LAW2-mod6), and the h = 0 stretch ladder (LAD-h0). This report
proves the next level: the stretch-3 of every STR2 end state (with watched
tracking), the stretch-4 structure of the four weight-4 families that appear
(W4, F(4,1; .), F(4,2; .), F(4,3; .)), the p = 5 instances SIEVE5-U and
SIEVE5-V, and, as corollaries, the twin laws on all classes whose smallest
prime factor is 3 or 5, i.e. the mod-30 resolution.

All statements below are about the K0859 recursion's reduced games only.
Nothing here concerns non-uniform boards.

## Games and vocabulary (reference)

As in K0931: a state is a cyclic list of holdings, a pointer position `ptr`
(0-based), and a pot p. A phase deals p stones one each to positions ptr,
ptr+1, ... (cyclically); the loser is the position (ptr + p) mod k (k =
active players) read after the deal; the loser's post-deal holding becomes
the new pot; ptr moves to the loser's position in the shortened list.
U(m): m players, each 2, pot 2, ptr 0, watched label m-1. V(m): m players,
each 2, pot 1, ptr 0, watched label 0. F(w, h; n): n players, the first n-h
hold w, the LAST h hold w+1 ("hot"); pot w; ptr 0; W_w(n) := F(w, 0; n),
H_w(n) := F(w, 1; n), G_w(n) := F(w, 2; n), T_w(n) := F(w, 3; n). A
stretch-k is a maximal run of phases whose starting pot is k; a loser
holding exactly the stretch pot dies cold (stretch continues), a loser
holding more dies hot (stretch ends, new pot = holding). Positions are
always indices in the ptr-frame circle (position 0 = pointer), and the
F(w,h;n) normalization lists the circle from the pointer.

K0931's STR2 end states (proved there) are the inputs here:

- U, m = 3q+1: H3(2q), watched label m-1 at position 2q-2 holding 3, hot
  (label 0) at position 2q-1 holding 4.
- U, m = 3q+2: W3(2q+1), watched at position 2q = n'-1 holding 3.
- V, m = 3q:   H3(2q-1), watched (label 0) at position 2q-2 = n'-1 holding
  4 (hot, last).
- V, m = 3q+2: G3(2q), watched at position 2q-2 = n'-2 holding 4 (hot),
  label 2 at n'-1 holding 4.
- V, m = 3q+1: label 0 is the stretch-2 breaking loser (SIEVE3-V), excluded
  below. U, m = 3q: label m-1 is dead (SIEVE3-U), excluded below.

Committed tables (pins in the audit): U(m), V(m) for m <= 8000, P(C) for
C <= 8000, 0-based pin["U"][m-1] = U(m), pin["P"][C-1] = P(C).

## Common block lemma for stretch-3 (L3)

In a state F(3, h; n') (pot 3, ptr 0), as long as the block conditions below
hold, phase j (the j-th phase of the stretch) deals 3 stones to the circle
positions 4j-4, 4j-3, 4j-2 (original frame; each +1) and eliminates position
4j-1 (holding 3, cold). Induction: before phase j the positions removed
during the stretch are {4i-1 : 1 <= i <= j-1}; the pointer is at original
position 4(j-1), whose shortened position is 4(j-1) - (j-1) = 3(j-1); the
three recipients are the next three shortened positions (originals 4j-4,
4j-3, 4j-2, untouched by earlier blocks since block i dealt to originals
<= 4i-2 <= 4j-6); the loser is shortened position 3(j-1)+3 = 3j, the
original 4j-1 (position 4j-1 minus j-1 removals), which is untouched and
holds 3 unless it lies in the hot tail. No wrap occurs iff 3j <= k-1 with
k = n'-(j-1), i.e. 4j <= n'. After the phase the pointer is again at
original position 4j. A block is cold-valid iff additionally the deal
positions and the loser are not in the hot tail and not the watched
(dealt-to positions must hold 3, i.e. 4j-2 <= n'-1-h, and the loser must
hold 3: 4j-1 <= n'-1-h). When a loser holds 4 (hot), the stretch ends
(breaking) and the pot becomes 4.

## Theorem S3-U (stretch-3 of the U-side STR2 end states; universal, proved)

Case A, m = 3q+1 (m >= 4, q >= 1), start H3(2q), watched at n'-2 (holds 3),
hot at n'-1 (holds 4), n' = 2q:

- A-I, q = 2k even (k >= 1): n' = 4k. By L3, blocks j = 1..k-1 are
  cold-valid (4j-1 <= 4k-5 < watched 4k-2; deals <= 4k-6). Phase k (the
  breaking phase): pointer at original 4k-4 (shortened 3k-3, k_active =
  3k+1), deal to originals 4k-4, 4k-3, and the watched 4k-2 (3 -> 4 each);
  loser shortened 3k = original 4k-1, the hot position, holding 4 -> hot
  death, pot 4. Stretch-3 length: k = n'/4. End state: 3k players, all
  holding 4 (block recipients 4, breaking recipients 4, hot removed), pot 4,
  ptr = 0 (the loser was last), circle [0, 1, 2, 4, 5, ..., 4k-3, watched],
  i.e. W4(3k) with the watched at position n''-1 = 3k-1.
- A-II, q = 2k+1 odd (k >= 0): n' = 4k+2. Blocks j = 1..k cold (losers
  4j-1 <= 4k-1 < watched 4k). Breaking phase k+1: pointer at original 4k
  (shortened 3k, active 3k+2), deal to the watched (3 -> 4), the hot 4k+1
  (4 -> 5), and wrapping, original 0 (block-1 recipient, 4 -> 5); loser =
  shortened (3k+3) mod (3k+2) = 1 = original 1 (block-1 recipient, holding
  4) -> hot, pot 4. Stretch-3 length: k+1 = floor(n'/4)+1. End state: 3k+1
  players, circle from ptr (original 2): [2, 4, 5, ..., 4k-2, watched(4),
  hot(5), 0(5)], holdings [4]^(n''-2) + [5, 5], pot 4, i.e. F(4, 2; 3k+1)
  with the watched at n''-3 = 3k-2. Edge k = 0 (m = 4): the breaking deal
  is watched (3->4), hot (4->5), watched again (4->5); loser = the hot,
  holding 5; the watched is the sole survivor (no stretch-4 at all).

Case B, m = 3q+2 (m >= 5, q >= 1), start W3(2q+1), watched at n'-1
(holds 3, last), n' = 2q+1:

- B-III, q = 2k even (k >= 1): n' = 4k+1. Blocks j = 1..k cold (losers
  4j-1 <= 4k-1 = n'-2). Breaking phase k+1: pointer at original 4k = the
  watched (shortened 3k, active 3k+1), deal to the watched (3 -> 4),
  original 0 (block-1 recipient, 3 -> 4), original 1 (block-1 recipient,
  3 -> 4); loser = shortened (3k+3) mod (3k+1) = 2 = original 2 (block-1
  recipient, holding 4) -> hot, pot 4. Stretch-3 length: k+1. End state:
  3k players, circle from ptr (original 3): [3, 4, 5, ..., 4k-2, watched(4),
  0(5), 1(5)], holdings [4]^(n''-2) + [5, 5], i.e. F(4, 2; 3k) with the
  watched at n''-3 = 3k-3.
- B-IV, q = 2k+1 odd (k >= 0): n' = 4k+3. Blocks j = 1..k cold (losers
  4j-1 <= 4k-1 < watched 4k+2). Breaking phase k+1: pointer at original 4k
  (shortened 3k, active 3k+3), deal to 4k, 4k+1, watched 4k+2 (3 -> 4
  each); loser = shortened (3k+3) mod (3k+3) = 0 = original 0 (block-1
  recipient, holding 4) -> hot, pot 4. Stretch-3 length: k+1 = floor(n'/4)+1.
  End state: 3k+2 players, circle from ptr (original 1): [1, 2, 4, 5, ...,
  4k+1, watched], ALL holding 4, pot 4, i.e. W4(3k+2) with the watched at
  n''-1 = 3k+1. Edge k = 0 (m = 5): n' = 3, no blocks; the breaking phase
  deals to all three (3 -> 4), loser original 0 (hot), end W4(2) with the
  watched last.

In all four cases the watched is a breaking-phase recipient and never a
loser, and every earlier loser holds 3 (cold). Machine anchor: S5U checks
below (stretch-3 length, end n'', watched position, holdings pattern,
survival), m = 3..700, 0 mismatches.

## Theorem S3-V (stretch-3 of the V-side STR2 end states; universal, proved)

Case A, m = 3q (q >= 1), start H3(2q-1), watched = label 0 at n'-1
(hot, 4), n' = 2q-1:

- V-A1, q = 2k+1 odd (k >= 0): n' = 4k+1. Blocks j = 1..k cold (losers
  4j-1 <= 4k-1 = n'-2, untouched hold 3, deals <= 4k-2 = n'-2). Breaking
  phase k+1: pointer at original 4k = the watched (shortened 3k, active
  3k+1), deal to the watched (4 -> 5), original 0 (block-1 recipient,
  3 -> 4), original 1 (block-1 recipient, 3 -> 4); loser = original 2
  (block-1 recipient, holding 4) -> hot, pot 4. Stretch-3 length: k+1 =
  floor(n'/4)+1. End state: 3k players, circle from ptr (original 3):
  [3, 4, 5, ..., 4k-2, watched(5), 0(5), 1(5)], holdings [4]^(n''-3) +
  [5, 5, 5], i.e. F(4, 3; 3k) with the watched at n''-3 = 3k-3. Edge k = 0
  (m = 3): n' = 1, the watched is the sole survivor (no stretch-3).
- V-A2, q = 2k+2 even (k >= 0): n' = 4k+3. Blocks j = 1..k cold. Breaking
  phase k+1: pointer at original 4k (shortened 3k, active 3k+3), deal to
  4k, 4k+1 (3 -> 4 each), the watched 4k+2 (4 -> 5); loser = original 0
  (block-1 recipient, holding 4) -> hot, pot 4. Stretch-3 length: k+1.
  End state: 3k+2 players, circle from ptr (original 1): [1, 2, 4, ..., 4k+1,
  watched(5)], holdings [4]^(n''-1) + [5], i.e. F(4, 1; 3k+2) with the
  watched at n''-1 = 3k+1. Edge k = 0 (m = 6): end F(4, 1; 2).

Case B, m = 3q+2 (q >= 0), start G3(2q), watched at n'-2 (hot, 4), the
other hot (label 2) at n'-1, n' = 2q:

- V-B1, q = 2k even (k >= 1): n' = 4k. Blocks j = 1..k-1 cold (losers
  4j-1 <= 4k-5 = n'-3). Breaking phase k: pointer at original 4k-4
  (shortened 3k-3, active 3k+1), deal to 4k-4, 4k-3 (3 -> 4 each), the
  watched 4k-2 (4 -> 5); loser = shortened 3k = original 4k-1, the other
  hot, holding 4 (not dealt) -> hot, pot 4. Stretch-3 length: k. End
  state: 3k players, all holding 4 except the watched (5), pot 4, ptr = 0
  (loser last), circle [0, 1, 2, 4, ..., 4k-3, watched(5)], i.e. F(4, 1; 3k)
  with the watched at n''-1 = 3k-1.
- V-B2, q = 2k+1 odd (k >= 0): n' = 4k+2. Blocks j = 1..k cold (losers
  4j-1 <= 4k-1 = n'-3, deals <= 4k-2 < watched 4k). Breaking phase k+1:
  pointer at original 4k = the watched (shortened 3k, active 3k+2), deal
  to the watched (4 -> 5), the other hot 4k+1 (4 -> 5), wrapping original 0
  (block-1 recipient, 3 -> 4); loser = original 1 (block-1 recipient,
  holding 4) -> hot, pot 4. Stretch-3 length: k+1. End state: 3k+1 players,
  circle from ptr (original 2): [2, 4, 5, ..., 4k-2, watched(5), hot(5),
  0(5)], holdings [4]^(n''-3) + [5, 5, 5], i.e. F(4, 3; 3k+1) with the
  watched at n''-3 = 3k-2. Edge k = 0 (m = 5): the breaking leaves the
  watched as sole survivor (no stretch-4).

In all cases the watched is a breaking-phase recipient and never a loser.
Machine anchor: S5V checks, m = 3..700, 0 mismatches.

## Theorem S4 (stretch-4 of the four weight-4 families; universal, proved)

Write n = 5t + r. Positions are ptr-frame. The four families and their
watched positions:

(1) W4(n), watched at n-1 holding 4 (this is LAD-h0 with w = 4, restated
with the watched). Blocks j = 1..t (r = 0) resp. j = 1..t (r >= 1; the
block losers 5j-1 <= 5t-1 <= n-2 avoid the watched) deal to 5j-5..5j-2
(4 -> 5) and eliminate 5j-1 (cold, 4).

- r = 0: block t eliminates position 5t-1 = n-1, the WATCHED, holding 4
  (its deal covered n-5..n-2, not n-1) -> COLD death at block t = n/5.
  The stretch continues (cold death).
- r >= 1: breaking phase t+1 (K0931 LAD-h0): the watched is among the r
  unprocessed recipients (4 -> 5, alive); the loser is kept index 4-r,
  a block-1 recipient holding 5 -> hot, the stretch ends with pot 5. In
  ptr-frame positions the loser sits at position 4-r (kept indices 0..3
  coincide with circle positions 0..3). The watched never dies.

(2) F(4, 1; n), watched at n-1 holding 5 (hot). Cold blocks j = 1..J,
J = (n-1)/5 floor: losers 5j-1 <= n-2 hold 4 (cold), deals 5j-5..5j-2
hold 4 (5j-2 <= n-2), untouched hot tail.

- r = 0 (5 | n): after J = t-1 cold blocks, block t deals n-5..n-2
  (4 -> 5) and eliminates 5t-1 = n-1, the WATCHED, holding 5 -> HOT
  death at block t = n/5; the pot becomes 5, so this is the FINAL phase
  of the first stretch-4.
- r in {1,2,3,4}: breaking phase J+1, pointer at original 5J = n-r; the
  deal covers the last r positions (the watched included: 5 -> 6, alive)
  and wraps into kept positions; the loser is the circle position 4-r
  (block-1 recipient holding 5, hot); the stretch ends with pot 5.
  (Tiny n = 2, 3, 4: the same loser formula holds by direct play, the
  loser holding 6 or 5.)

(3) F(4, 2; n), watched at n-3 holding 4, hot 5s at n-2, n-1. Cold blocks
j = 1..J, J = (n-3)/5 floor: losers 5j-1 <= n-4 hold 4 (cold), deals
5j-5..5j-2 <= n-5 hold 4.

- r = 2 (n = 5t+2): after J = t-1 cold blocks, block t deals n-7..n-4
  (4 -> 5) and eliminates 5t-1 = n-3, the WATCHED, holding 4 (untouched)
  -> COLD death at block t = (n-2)/5. The stretch continues (cold death).
- r = 0: J = t-1; breaking phase t, pointer at n-5, deal n-5, n-4 (4->5),
  watched n-3 (4->5), n-2 (5->6); loser n-1 (hot 5), stretch ends pot 5;
  watched alive (5).
- r = 1: J = t-1; breaking phase t, pointer at n-6 (n >= 11; n = 6
  directly), deal n-6, n-5, n-4 (4->5), watched (4->5); loser n-2 (hot 5),
  stretch ends pot 5; watched alive (5). [This is the first instance of
  the ladder's open class h >= 2, 1 <= r < h.]
- r = 3: J = t (block t eliminates 5t-1 = n-4, cold); breaking phase t+1,
  pointer at n-3 = the watched, deal watched (4->5), n-2 (5->6), n-1
  (5->6), wrap 0 (block-1 recipient 4->5); loser position 1 (block-1
  recipient, 5, hot), stretch ends pot 5; watched alive (5).
- r = 4: J = t; breaking phase t+1, pointer at n-4, deal n-4 (4->5),
  watched (4->5), n-2 (5->6), n-1 (5->6); loser wrap position 0 (block-1
  recipient, 5, hot), stretch ends pot 5; watched alive (5).

(4) F(4, 3; n), watched at n-3 holding 5 (hot), hot tail n-3, n-2, n-1.
Cold blocks j = 1..J, J = (n-3)/5 floor, as in (3).

- r = 2 (n = 5t+2): after J = t-1 cold blocks, block t deals n-7..n-4
  (4 -> 5) and eliminates 5t-1 = n-3, the WATCHED, holding 5 -> HOT
  death at block t = (n-2)/5; the pot becomes 5: the FINAL phase of the
  first stretch-4. [Also an open-class instance: h = 3, r = 2 < h.]
- r = 0: breaking phase t, pointer at n-5, deal n-5, n-4 (4->5), watched
  (5->6), n-2 (5->6); loser n-1 (hot 5), ends pot 5; watched alive (6).
- r = 1: breaking phase t, pointer at n-6, deal n-6, n-5, n-4 (4->5),
  watched (5->6); loser n-2 (hot 5), ends pot 5; watched alive (6).
  [Open class: h = 3, r = 1.]
- r = 3: breaking phase t+1, pointer at the watched, deal watched (5->6),
  n-2 (5->6), n-1 (5->6), wrap 0 (block-1 recipient 4->5); loser position
  1 (block-1 recipient, 5, hot), ends pot 5; watched alive (6).
- r = 4: breaking phase t+1, pointer at n-4, deal n-4 (4->5), watched
  (5->6), n-2 (5->6), n-1 (5->6); loser wrap position 0 (5, hot), ends
  pot 5; watched alive (6).

Summary (the four families share one skeleton; the death block j* is the
unique j with 5j-1 = watched position, and the first stretch-4 length is
(n-1)//5 + 1 for watched-at-(n-1) families, (n-3)//5 + 1 for
watched-at-(n-3) families, covering both death and breaking):

  family        death iff        death block   death type
  W4(n)         5 | n            n/5           cold (stretch continues)
  F(4,1;n)      5 | n            n/5           hot, FINAL phase
  F(4,2;n)      n = 2 (mod 5)    (n-2)/5       cold (stretch continues)
  F(4,3;n)      n = 2 (mod 5)    (n-2)/5       hot, FINAL phase

Machine anchor: S4BREAK + S5U/S5V death checks below (death block/length,
holding, finality, and the survival breaking: phase, loser position, held
5), 0 mismatches.

## Theorem SIEVE5-U (universal, proved)

For m >= 4 with m =/= 0 (mod 3): in U(m), the watched label m-1 is
eliminated during the FIRST stretch-4 if and only if m = 1 (mod 5), i.e.
m mod 30 in {1, 11, 16, 26}; the death is cold (holding 4) at block
n''/5 (sub-cases A-I, B-IV) resp. (n''-2)/5 (sub-cases A-II, B-III), and
no earlier stretch kills it. If m =/= 1 (mod 5), the watched survives the
first stretch-4 (as a breaking recipient or untouched).

Proof. By SIEVE3-U (K0931), the premise m =/= 0 (mod 3) means the watched
survives stretch-2 (as a breaking recipient). The STR2-U end state is
H3(2q) (m = 3q+1) resp. W3(2q+1) (m = 3q+2), with the watched at the
position stated above. S3-U converts these into the stretch-4 start states:

  sub-case  m          n''    family         watched at   death iff
  A-I       6k+1       3k     W4(3k)         n''-1        5 | 3k  <=> 5 | k
  A-II      6k+4       3k+1   F(4,2;3k+1)    n''-3        3k+1 = 2 (mod 5)
  B-III     6k+2       3k     F(4,2;3k)      n''-3        3k = 2 (mod 5)
  B-IV      6k+5       3k+2   W4(3k+2)       n''-1        5 | 3k+2 <=> 3k+2 = 0 (mod 5)

and S4 decides the death. The congruences map to mod 30: A-I 5|k ⟺
m = 6k+1 ≡ 1 (30); A-II k ≡ 2 (5) ⟺ m ≡ 16 (30); B-III k ≡ 4 (5) ⟺
m ≡ 26 (30); B-IV k ≡ 1 (5) ⟺ m ≡ 11 (30). The union is exactly
m ≡ 1 (mod 5) ∧ m ≢ 0 (mod 3). The stretch-3 never kills the watched
(S3-U: it is a breaking recipient), so the first possible death after
stretch-2 is the stretch-4 one claimed. Edges: m = 4 (A-II, k = 0) and
m = 5 (B-IV, k = 0, n'' = 2: one breaking phase, watched alive) are in
the survival classes; direct play confirms U(4) = 3 = m-1, U(5) = 4 =
m-1 (2m+3 = 11, 13 prime). QED.

## Theorem SIEVE5-V (universal, proved)

For m >= 3 with m =/= 1 (mod 3): in V(m), the watched label 0 is
eliminated during the FIRST stretch-4 if and only if m = 2 (mod 5), i.e.
m mod 30 in {2, 12, 17, 27}; the death is hot (holding 5) and is the
FINAL phase of the first stretch-4 (block n''/5 resp. (n''-2)/5), and no
earlier stretch kills it. If m =/= 2 (mod 5), the watched survives the
first stretch-4.

Proof. SIEVE3-V: the premise keeps the watched alive through stretch-2
(hot in the H3/G3 end state). S3-V converts into stretch-4 start states:

  sub-case  m          n''    family         watched at   death iff
  V-A1      6k+3       3k     F(4,3;3k)      n''-3        3k = 2 (mod 5)
  V-A2      6k+6       3k+2   F(4,1;3k+2)    n''-1        5 | 3k+2
  V-B1      6k+2       3k     F(4,1;3k)      n''-1        5 | 3k <=> 5 | k
  V-B2      6k+5       3k+1   F(4,3;3k+1)    n''-3        3k+1 = 2 (mod 5)

S4 decides: V-A1 k ≡ 4 (5) ⟺ m ≡ 27 (30); V-A2 k ≡ 1 (5) ⟺ m ≡ 12 (30);
V-B1 k ≡ 0 (5) ⟺ m ≡ 2 (30); V-B2 k ≡ 2 (5) ⟺ m ≡ 17 (30); union
m ≡ 2 (mod 5) ∧ m ≢ 1 (mod 3). The stretch-3 never kills the watched
(S3-V). Edges: m = 3 (V-A1, k = 0): the watched is the sole survivor;
m = 5 (V-B2, k = 0): sole survivor; m = 6 (V-A2, k = 0, n'' = 2): the
stretch-4 breaking phase kills the other player, the watched survives.
All are in survival classes (2m+1 = 7, 11, 13 prime; pins V = 0).
m = 2 lies below the premise (2m+1 = 5): direct play V(2) = 0. QED.

Together with SIEVE3-U/V (K0931) this proves the SIEVE conjecture's
composite side for spf in {3, 5}: if 2m+3 (resp. 2m+1) is composite with
smallest prime factor p in {3, 5}, the watched label dies exactly at the
pot-(p-1) stretch, holding p-1 (U, cold, delta 0) resp. p (V, hot,
delta 1). The prime side (survival when 2m+s is a prime >= 7) remains
conjectural (machine range m <= 8000, K0931).

## Corollary LAW1-{3,5} (twin law 1 on all spf in {3,5} classes; universal)

For every odd C >= 3 with 3 | C or 5 | C (equivalently C mod 30 in
{3, 5, 9, 15, 21, 25, 27}): P(C) = 1 if and only if C is prime.

Proof. (<=) A prime divisible by 3 or 5 is 3 or 5; pins P(3) = P(5) = 1
(K0919/K0929 committed tables). (=>) Contrapositive. Let C be odd
composite with 3 | C or 5 | C. If 3 | C then C ≡ 3 (mod 6) and LAW1-mod6
(K0931) applies. Otherwise 5 | C, 3 ∤ C, so C >= 25 and C ≡ 5 or 25
(mod 30); write C = 2m+1: then m = (C-1)/2 ≡ 2 (mod 5), m ≢ 1 (mod 3),
m >= 12. By SIEVE5-V the watched label 0 is eliminated in stretch-4, so
V(m) ≠ 0, and by Theorem RED (K0928), P(C) = 1 + 2V(m) ≠ 1. QED.

## Corollary LAW2-{3,5} (twin law 2 on all spf in {3,5} classes; universal)

For every even C >= 2 with 3 | (C+1) or 5 | (C+1) (equivalently
C mod 30 in {2, 4, 8, 14, 20, 24, 26}): P(C) = C-1 if and only if C+1
is prime.

Proof. (<=) C+1 ∈ {3, 5} means C ∈ {2, 4}; pins P(2) = 1, P(4) = 3.
(=>) Let C+1 be composite. If 3 | (C+1), then C ≡ 2 (mod 6), C+1 ≡ 3
(mod 6) composite >= 9, and LAW2-mod6 (K0931) applies. Otherwise
5 | (C+1), 3 ∤ (C+1), so C+1 >= 25; write C = 2m+2: then
m = (C-2)/2 ≡ 1 (mod 5), m ≢ 0 (mod 3), m >= 11. By SIEVE5-U the watched
label m-1 is eliminated in stretch-4, so U(m) ≠ m-1, and
P(C) = 3 + 2U(m) ≠ 2m+1 = C-1. QED.

The remaining LAW1/LAW2 classes are those with spf >= 7 (C ≡ 1, 7, 11,
13, 17, 19, 23, 29 resp. 0, 6, 10, 12, 16, 18, 22, 28 mod 30), which
require SIEVE for p >= 7 and stay OPEN (both the composite side and the
prime-survival side).

## Ladder upgrades (from machine-verified to proved)

K0931 verified the restricted ladder rule for F(w,h;n) on four grids
(8,282 checks) but proved only h = 0 (LAD-h0). This report proves:

- The stretch-3 of F(3,1;n) at n ≡ 0, 2 (mod 4) with the watched at n-2
  (A-I, A-II), F(3,1;n) at n ≡ 1, 3 (V-A1, V-A2) with the watched at
  n-1, F(3,0;n) at n ≡ 1, 3 (B-III, B-IV) with the watched at n-1, and
  F(3,2;n) at n ≡ 0, 2 (V-B1, V-B2) with the watched at n-2: eight
  instances, all with watched tracking (previously machine-verified only,
  except the h = 0 ones which LAD-h0 covers without the watched).
- The stretch-4 of F(4,0;n) (LAD-h0 + watched statement), F(4,1;n) for
  all r, F(4,2;n) for all r, F(4,3;n) for all r, each with watched
  tracking, death/breaking structure and holdings.
- The FIRST PROVED INSTANCES of the ladder's open class
  h >= 2, 1 <= r < h: F(4,2; 5t+1) (breaking loser at position n-2,
  hot 5, phase (n-3)//5+1 = t, end pot 5, watched survives at 5),
  F(4,3; 5t+2) (the hot FINAL death at block (n-2)/5 = t: the very
  mechanism of SIEVE5-V), and F(4,3; 5t+1) (breaking loser n-2). The
  general open-class structure for arbitrary w remains open.

## Machine verification (sieve5_verify.py, audit_build.py)

All stdlib Python, deterministic, no timestamps. From the experiment
directory: python3 sieve5_verify.py (exit 0 iff all checks pass),
python3 audit_build.py (runs the whole suite twice in-process, requires
identical results, writes output/sieve5_uv_audit.json; two cold runs are
byte-identical, sha256 2c1917e07254c44f69482f830b626bdc93b305d4e3d6ead733cfce7cc3fe9cf7).

Checks (all pass, 0 mismatches; counts from the committed audit JSON):

- PIN: the K0928/K0929 committed tables
  (pc_uv8000.json sha256 8a3b318bd26b8197c66fd55d79007654d2926a18af165132af8c194bc76d8ae2,
  pc_p8000.json sha256 58a414bc31fb6266cc2d0e10000436e50f396135847bab5a32163cffff0b975e)
  plus the P(1..40) anchor [0, 1, 1, 3, 1, 5, 1, 5, 5, 9, 1, 11, 1, 5,
  7, 15, 1, 17, 1, 15, 17, 21, 1, 21, 11, 15, 7, 27, 1, 29, 1, 27, 17,
  21, 11, 35, 1, 5, 7, 39].
- REDRECON: the committed U/V tables reproduce the committed P table via
  the PROVED Theorem RED, every m <= 3999 (7,998 comparisons), 0
  mismatches (pure pin-vs-pin consistency).
- TWIN30: the proved twin-law classes on the committed P table, every
  C <= 8000: LAW1 classes {3,5,9,15,21,25,27} mod 30 (census 267, 267,
  267, 267, 266, 266, 266), LAW2 classes {2,4,8,14,20,24,26} mod 30
  (census 267, 267, 267, 267, 267, 266, 266), zero violations of
  "P(C)=1 ⟺ prime" resp. "P(C)=C-1 ⟺ C+1 prime".
- FRESHPIN: fresh full simulations of U(m) and V(m), m = 3..700 (1,396
  games), survivors equal the committed pins, 0 mismatches.
- SPF: machine evidence for the SIEVE conjecture at the fresh range:
  for composite 2m+s, the watched's first death is at pot spf-1 with
  holding spf-1 (U) resp. spf (V); for prime 2m+s the watched survives;
  0 violations at m <= 700 (spf <= 803).
- SIEVE3: the proved K0931 regression, stretch-2 death iff m ≡ 0 (U)
  resp. 1 (V) (mod 3), 0 mismatches.
- S5U / S5V: the closed forms of this report, for every m = 3..700 in
  the premise classes (465 m each side): death ⟺ m ≡ 1 resp. 2 (mod 5),
  death block closed forms (n''/5, (n''-2)/5), U death cold / V death
  hot and FINAL (phase == first-stretch-4 length), stretch-3 length
  closed forms, stretch-4 start state (n'', watched position, holdings
  pattern [4]^(n''-h) + [5]^h), 0 mismatches.
- S4BREAK: the survival-class breaking structure (phase
  (n-1)//5+1 resp. (n-3)//5+1, loser circle position 4-r resp.
  {0: n-1, 1: n-2, 3: 1, 4: 0}, held 5), 723 checks at n'' >= 11,
  0 mismatches.
- REDFRESH: fresh RED reconstruction P(C) = 1+2V(m) resp. 3+2U(m) from
  the fresh survivors equals the committed P table for all C <= 1402
  (1,396 comparisons), 0 mismatches.

The verifier's game engine implements K0928 Lemma P directly (deal,
loser, pot, pointer) and was checked against the committed pins before
use (fresh survivors match the K0929 tables exactly). The closed-form
expectations are generated from the theorems above, independently of the
engine's stretch bookkeeping.

## Limitations

Uniform board, zero reset, K0859 recursion (via K0928 Theorem RED) only;
no statement about non-uniform boards. Proved here: S3-U/V (eight cases),
S4 (four families, all r), SIEVE5-U/V, LAW1-{3,5}, LAW2-{3,5}, and the
listed ladder upgrades (including three open-class instances). Machine
evidence only (no universal proof): SIEVE for spf >= 7 (m <= 8000,
K0931; fresh re-verification m <= 700 here) and the prime-side survival
for primes >= 7. OPEN: SIEVE p >= 7 (the next target is the stretch-6 /
spf = 7 mechanism, i.e. the W5/F(5,h; .) families), the general
open-class ladder structure for arbitrary w, the W4/H4/G4/T4 families'
deep structure beyond the first stretch-4, and LAW1/LAW2 on the
spf >= 7 classes. No closed form for P(C) is claimed beyond the proved
classes. The 11x11 open-board status is unchanged (empty board,
two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 all UNKNOWN);
the pruning lemmas here concern the reduced games only.
