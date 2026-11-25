# U/V stretch-2 structure theorems, twin-law mod-6 resolution, and the unified weight ladder (K0859 counting recursion)

Experiment date: 2026-11-17. Item: K0931. Object: the reduced games U(m)/V(m)
introduced by K0928 Theorem RED for the K0859 theorem-D counting recursion on
the uniform board with zero reset (P(2m+2) = 3 + 2U(m), P(2m+1) = 1 + 2V(m),
both proved in K0928).

All statements below are about the K0859 recursion's reduced games only.
Nothing in this experiment concerns non-uniform boards.

## Games and vocabulary (reference)

Pot dynamics (K0928 Lemma P): a state is a cyclic list of holdings, a pointer
position `ptr` (0-based into the list), and a pot p. A phase deals p stones,
one each, to positions ptr, ptr+1, ... (cyclically); the loser is the position
(ptr + p) mod k (k = number of active players), read after the deal; the
loser's post-deal holding becomes the new pot; the pointer moves to the
loser's position in the shortened list. Stones are conserved: s + pot = C.

- U(m): m players, each holding 2, pot 2, ptr 0.
- V(m): m players, each holding 2, pot 1, ptr 0.
- F(w, h; n): n players; the first n-h hold w, the LAST h hold w+1 ("hot");
  pot w; ptr 0. W_w(n) := F(w, 0; n), H_w(n) := F(w, 1; n),
  G_w(n) := F(w, 2; n), T_w(n) := F(w, 3; n).

A *stretch-k* of a game is a maximal run of consecutive phases whose starting
pot equals k. A loser who holds exactly the stretch pot dies "cold" (the
stretch continues); a loser who holds more dies "hot" (the stretch ends and
the new pot is their holding). K0928's Lemma E/O are the stretch-1 of G(C);
this report is the stretch-2 level (weight 3) and, for the ladder, the
stretch-w level of F(w, h; n).

The committed tables (K0928/K0929, pins in the audit):
U(m), V(m) for m <= 8000, index 0-based: pin["U"][m-1] = U(m).

## Theorem STR2-V (stretch-2 of V(m); universal, proved)

For m >= 4, write the phase-1 result first: phase 1 of V(m) (pot 1) deals one
stone to label 0 (2 -> 3) and eliminates label 1 at position 1 holding 2
(cold); the pot becomes 2 and ptr = 1 (label 2). The stretch-2 then has length
ceil((m-1)/3) and:

(i) *Block phases.* Block phase j (j = 1..J with J = floor((m-2)/3)) deals to
labels 3j-1 and 3j (each 2 -> 3) and eliminates label 3j+1 holding 2 (cold).
Position arithmetic: before block j the labels removed during the stretch are
{1, 4, 7, ..., 3j-2} (j labels in all), the pointer sits at the position of
label 3j-1, which is position 2j-1 (labels below it: 3j-1 minus j removed),
and the loser position 2j+1 is the label 3j+1 (position (3j+1) - j = 2j+1),
untouched, hence holding 2. No wrap occurs as long as 2j+1 <= k-1 with
k = m-j, i.e. 3j+2 <= m, which is exactly j <= J. After the phase the pointer
is again at the position of label 3(j+1)-1. Induction over j.

(ii) *Breaking phase* (phase J+1 of the stretch), by m mod 3. In each case the
recipients are the two positions from the pointer and the loser is the third;
the loser holds 3 (hot), so the stretch ends with pot 3:

- m = 3q+1 (J = q-1, k = 2q+1, ptr at position 2q-1 = label 3q-1):
  recipients labels 3q-1, 3q (2 -> 3 each); loser position (2q+1) mod (2q+1)
  = 0 = label 0, holding 3 (its phase-1 stone). End state: 2q players, all
  holding 3, pot 3, ptr at label 2, i.e. W3(2q) = F(3,0;2q) with circle
  [2, 3, 5, 6, ..., m-2, m-1].
- m = 3q (J = q-1, k = 2q, ptr at position 2q-1 = label 3q-1 = m-1):
  recipients labels m-1 (2 -> 3) and, wrapping, label 0 (3 -> 4, hot);
  loser position (2q+1) mod 2q = 1 = label 2, holding 3. End state: 2q-1
  players, label 0 hot with 4, all others 3, pot 3, ptr at label 3, i.e.
  H3(2q-1) = F(3,1;2q-1) with circle [3, 5, 6, 8, ..., m-1, 0].
- m = 3q+2 (J = q, all labels 0..m-1 except 0 are touched by the blocks,
  ptr wraps to position 0 = label 0 holding 3): recipients labels 0 and 2
  (3 -> 4 each, both hot); loser position 2 = label 3, holding 3. End state:
  2q players, labels 0 and 2 hot with 4, others 3, pot 3, ptr at label 5,
  i.e. G3(2q) = F(3,2;2q) with circle [5, 6, 8, 9, ..., m-3, m-2, 0, 2].

Note that in the last case label m-1 = 3q+1 is the block-q loser (3j+1 with
j = q), removed cold with 2.

Machine anchor: theorem_verify.py, m = 4..1000, exact loser sequence
(labels 4, 7, 10, ... then the breaking loser), exact holdings (block losers
hold 2, breaking loser holds 3), exact end circle and pot, 3,988 checks,
0 failures (SIEVE check below).

## Theorem STR2-U (stretch-2 of U(m); universal, proved)

For m >= 4, the stretch-2 of U(m) has length ceil((m+1)/3):

(i) *Block phases.* Block phase j (j = 1..J with J = floor(m/3)) deals to
labels 3j-3 and 3j-2 (each 2 -> 3) and eliminates label 3j-1 holding 2
(cold). Position arithmetic mirrors STR2-V: before block j the removed labels
are {2, 5, ..., 3j-4} (j-1 labels), the pointer is at the position of label
3j-3, which is 2j-2, the recipients sit at positions 2j-2, 2j-1, and the
loser position 2j is label 3j-1 (position (3j-1)-(j-1) = 2j), untouched.
No wrap as long as 2j <= k-1 with k = m-j+1, i.e. 3j <= m, which is j <= J.

(ii) *Breaking phase*, by m mod 3 (loser holds 3, hot, stretch ends, pot 3):

- m = 3q+2 (J = q, k = 2q+2, ptr at position 2q = label 3q = m-2):
  recipients labels m-2, m-1 (2 -> 3 each); loser position (2q+2) mod (2q+2)
  = 0 = label 0, holding 3. Label m-1 is ALIVE holding 3. End state:
  W3(2q+1), circle [1, 3, 4, 6, 7, ..., m-2, m-1].
- m = 3q+1 (J = q, k = 2q+1, ptr at position 2q = label 3q = m-1):
  recipients labels m-1 (2 -> 3) and, wrapping, label 0 (3 -> 4, hot);
  loser position (2q+2) mod (2q+1) = 1 = label 1, holding 3. Label m-1 is
  ALIVE holding 3. End state: H3(2q), circle [3, 4, 6, 7, ..., m-1, 0].
- m = 3q, q >= 2 (J = q, all labels are consumed by the blocks, the block-q
  loser being label 3q-1 = m-1, so the pointer wraps to position 0 = label 0):
  recipients labels 0 and 1 (3 -> 4 each, both hot); loser position 2 =
  label 3, holding 3. Label m-1 is DEAD (block-q loser, cold, held 2).
  End state: G3(2q-1), circle [4, 6, 7, 9, 10, ..., 0, 1].

Machine anchor: theorem_verify.py, m = 4..1000, 0 failures.

## Corollary SIEVE3-U (proved; the p = 3 instance of the SIEVE conjecture)

In U(m), label m-1 is eliminated during stretch-2 if and only if m = 0
(mod 3). (For m = 3 mod 3 with q = 1, i.e. m = 3, direct play: phase 1
eliminates label 2 = m-1 cold; U(3) = 1 != 2, consistent with the committed
pin P(8) = 5 != 7.) For m = 1, 2 mod 3 label m-1 is a breaking recipient and
survives stretch-2 holding 3.

Symmetrically SIEVE3-V (proved): in V(m), label 0 is eliminated during
stretch-2 if and only if m = 1 (mod 3) (breaking loser of the m = 3q+1 case);
otherwise it is hot (4) in the H3/G3 end state.

Note 2m+1 = 0 (mod 3) iff m = 1 (mod 3), and 2m+3 = 0 (mod 3) iff m = 0
(mod 3): SIEVE3 is exactly the statement that the p = 3 prime factor kills
the watched label at the pot-(p-1) = pot-2 stretch.

## Theorem LAW1-mod6 (universal, proved)

For every C = 3 (mod 6): P(C) = 1 if and only if C is prime.

Proof. C = 3: prime, and P(3) = 1 (committed pin, K0919/K0929). C >= 9 with
C = 3 (mod 6): C is composite (divisible by 3, greater than 3). Write
C = 2m+1, so m = (C-1)/2 = 3t+1 = 1 (mod 3) and m >= 4. By Theorem RED
(K0928), P(C) = 1 + 2V(m), so P(C) = 1 iff V(m) = 0 iff label 0 survives
V(m). By STR2-V (ii), m = 1 (mod 3) makes label 0 the breaking loser of
stretch-2: label 0 is eliminated, so V(m) != 0 and P(C) != 1. Both sides of
the equivalence are false for every such C. QED.

## Theorem LAW2-mod6 (universal, proved)

For every C = 2 (mod 6): P(C) = C-1 if and only if C+1 is prime.

Proof. C = 2: C+1 = 3 prime and P(2) = 1 = C-1 (committed pin). C >= 8 with
C = 2 (mod 6): C is composite and C+1 = 3 (mod 6), C+1 >= 9, so C+1 is
composite. Write C = 2m+2, so m = (C-2)/2 = 3t = 0 (mod 3) and m >= 3. By
Theorem RED, P(C) = 3 + 2U(m), so P(C) = C-1 = 2m+1 iff U(m) = m-1 iff label
m-1 survives U(m). By SIEVE3-U, m = 0 (mod 3) eliminates label m-1 in
stretch-2 (for m = 3 directly, see above; for m >= 4 by STR2-U). Hence
U(m) != m-1 and P(C) != C-1. Both sides are false for every such C. QED.

The remaining classes of LAW1/LAW2 (C = 1, 5 mod 6 for LAW1; C = 0, 4 mod 6
for LAW2) are, by Theorem RED, exactly equivalent to the SIEVE conjectures
below and remain open.

## The 6-reduction (proved, machine-anchored)

STR2-V/U exhibit the stretch-2 end states as weight-3 ladder instances:
V(3q+1) -> W3(2q), V(3q) -> H3(2q-1), V(3q+2) -> G3(2q),
U(3q+2) -> W3(2q+1), U(3q+1) -> H3(2q), U(3q) -> G3(2q-1).
Conversely the phase-1 of V(m) is the w = 2 ladder instance F(2, 1; m-1)
(m-1 players all 2 except the last hot 3, pot 2), which is why the ladder
below with w = 2 reproduces the U/V level and with w = 3 the weight-3 level.
Machine anchor: for every m in [4,1000], playing the reduced game
(survivor_of on the expected end circle, pot 3) and mapping the survivor
position back through the position->label map reproduces the committed
V(m)/U(m) pins exactly (theorem_verify.py, 0 mismatches). This is a
machine check of the proved theorems (the reduction itself is a direct
consequence of the pot dynamics, K0928 Lemma P).

## Theorem LAD-h0 (stretch-w ladder, h = 0; universal, proved)

For w >= 2, let n = (w+1)k + r with k >= 1 and 0 <= r <= w. The stretch-w of
W_w(n) = F(w, 0; n) has exactly k+1 phases and ends as follows:

(i) *Block phases.* Block j = 1..k deals w stones to positions
(j-1)(w+1), ..., j(w+1)-1 of the ORIGINAL circle (each holding w -> w+1) and
eliminates position j(w+1)-1 (holding w, cold). Positions are consumed in
order and no wrap occurs because (w+1)k <= n. After block k, positions
k(w+1)..n-1 (r of them, the "unprocessed") still hold w and positions
0..k(w+1)-1 except the k losers (kw of them, the "kept") hold w+1.

(ii) *Breaking phase* (phase k+1), by r:

- r >= 1: the pointer is at the first unprocessed position (original index
  k(w+1)). The w recipients are the r unprocessed (w -> w+1) followed by the
  first w-r kept positions (w+1 -> w+2); the loser is the next position,
  kept index w-r, holding w+1 (hot). The stretch ends with pot w+1. The
  remaining n' = wk + r - 1 players, read from the new pointer (the position
  after the loser), are [w+1]^(n'-h") followed by [w+2]^h" with
  h" = h' = w-r: i.e. the end state is F(w+1, w-r; n') up to rotation,
  n' >= h" always (n' - h" = w(k-1) + 2r - 1 >= 0).
- r = 0, k >= 2: the pointer wraps to kept index 0. The w recipients are
  kept indices 0..w-1 (w+1 -> w+2); the loser is kept index w, holding w+1
  (hot). End state F(w+1, w; n') with n' = wk - 1, pot w+1.
- r = 0, k = 1 (collapse): n = w+1; after block 1 the w kept hold w+1 and
  the pointer wraps to kept 0. The breaking phase deals w stones to ALL w
  remaining players (w+1 -> w+2) and eliminates position (0+w) mod w = 0,
  holding w+2. The end state is w-1 players all holding w+2, pot w+2, i.e.
  W_{w+2}(w-1): the base weight JUMPS to w+2.

Machine anchor: ladder_verify.py grid w=2, h=0, n <= 1000 (and the w=3,4,5
columns), exact end circle, pot, and survivor-consistency (the reduced game's
survivor maps to the full game's survivor), 0 failures.

## The restricted ladder F(w, h; n) for h >= 1 (machine-verified, unproved)

Machine-verified rule (ladder_verify.py, 8,282 checks, 0 failures; grids
w=2 n<=1000, w=3 n<=800, w=4 n<=250, w=5 n<=150, all h = 0..w): with
n = (w+1)k + r, k >= 1, the stretch-w of F(w, h; n) ends in the state of a
reduced game with base B = w+1 (usual) or B = w+2 (collapse n' < h'), where

  h' = (h-1-r) mod (w+1),   n' = w*k + e,   e = (r-1) if h = 0 else max(r-1, 0),

the end circle from the new pointer is [B]^(n'-h") + [B+1]^h" (hot at the
end) with h" = min(h', n') (h" = 0 in the collapsed case, which occurs only
for h = 0, k = 1, r = 0), the end pot is B, and the reduced game's survivor
maps back to the full game's survivor.

Applicability (as verified): h = 0 with any r (this is Theorem LAD-h0), or
h >= 1 with r = 0 or r >= h. The class h >= 2 with 1 <= r < h is OPEN: its
end states have a different structure (not covered by the rule; skipped by
the verifier, not refuted). No proof is claimed for the h >= 1 instances;
only the h = 0 case is proved (above).

## Conjecture SIEVE (machine range m <= 8000; universal proof OPEN)

Watching the two labels that Theorem RED makes responsible for the twin laws:

- SIEVE-V: in V(m), label 0 is eliminated in the pot-(p-1) stretch, where
  p = spf(2m+1) (smallest prime factor), dying with exactly p stones
  (held = pot + 1, a hot death), if 2m+1 is composite; label 0 survives the
  whole game iff 2m+1 is prime (then V(m) = 0).
- SIEVE-U: in U(m), label m-1 is eliminated in the pot-(p-1) stretch,
  p = spf(2m+3), dying with exactly p-1 stones (held = pot, a cold death),
  if 2m+3 is composite; label m-1 survives iff 2m+3 is prime
  (then U(m) = m-1).

SIEVE3-V/SIEVE3-U above are the proved p = 3 instances. The p >= 5 instances
are open; the next case SIEVE5-U (pot-4 stretch: label m-1 dies iff
5 | 2m+3) is the first open one.

Machine evidence (sieve_test.py, pins mode): for every m <= 8000 the watched
label's death (when it dies) is exactly at the pot-(spf-1) stretch with the
claimed holding: V violations 0, U violations 0, and the surviving cases
match the committed U/V tables with 0 pin mismatches (2,666 V deaths at
pot 2, 1,066 at pot 4, 608 at pot 6, 332 at pot 10, 254 at pot 12, 178 at
pot 16, 150 at pot 18, 119 at pot 22, ...; the U side mirrors this with cold
deaths: 2,666 / 1,066 / 608 / 332 / 255 / 178 / 150 / 119 at the same
pots). Via Theorem RED this is exactly LAW1/LAW2 evidence up to C <= 16001,
consistent with the K0929 direct evidence.

The SIEVE conjecture is NOT proved: the universal statement would need the
death-level mechanism (why the watched label always dies exactly at the
spf-1 stretch, for every prime factor) for all p. The mod-6 theorems above
are unconditional; the remaining composite classes of LAW1 (C = 1, 5 mod 6)
and LAW2 (C = 0, 4 mod 6) are equivalent to SIEVE-V resp. SIEVE-U.

## Data and cross-verification

Scripts (pinned by sha256 in the audit; all stdlib python, deterministic):
- sieve_test.py: SIEVE sweep m <= 8000 with death-record extraction,
  pins mode compares survivors with the committed U/V tables (~70 s).
- theorem_verify.py: STR2-V/U + SIEVE3-U + 6-reduction, m in [4,1000],
  3,988 checks, 0 failures (~40 s). End-state expectations are generated
  from the theorems' closed forms and compared against fresh simulations;
  the survivor reduction plays the reduced game and maps positions back to
  labels, checked against the committed pins.
- ladder_verify.py: restricted ladder rule on the four grids,
  8,282 checks, 0 failures (~3 s).
- w3_explore.py + data/w3_explore.json: deterministic exploration data for
  the W3/H3/G3 stretch-3 end-state shapes (n mod 4 classes) and position-0
  death levels, n <= 300 (input for the weight-4 level; no claim here).

Audit: audit_build.py re-runs the three verifiers fresh and assembles
output/uv_stretch_ladder_audit.json (4 checks: SIEVE / STR2 / LADDER /
W3EXPLORE, all_ok true). Two cold runs produce byte-identical output
(sha256 5ab2907d1800f60c6ad4d7149608e1b3be6c1ec19e19e066423ab3208cea328c).
Input pins: the K0928/K0929 committed tables
(../remo-pc-twin-laws-20261117/data/pc_uv8000.json,
sha256 8a3b318bd26b8197c66fd55d79007654d2926a18af165132af8c194bc76d8ae2;
pc_p8000.json,
sha256 58a414bc31fb6266cc2d0e10000436e50f396135847bab5a32163cffff0b975e).

## Limitations

Uniform board, zero reset, K0859 recursion (via K0928 Theorem RED) only; no
statement about non-uniform boards. Proved here: STR2-V/U, SIEVE3-V/U,
LAW1-mod6, LAW2-mod6, LAD-h0. Machine-verified only (no proof): the
restricted ladder for h >= 1 and the SIEVE conjecture m <= 8000. Open: the
ladder class h >= 2 with 1 <= r < h, SIEVE for p >= 5, the weight-4
(W4/H4/G4/T4) internal structure, and LAW1/LAW2 on the classes
C = 1, 5 resp. 0, 4 (mod 6). No closed form for P(C) is claimed. The 11x11
open-board status is unchanged (empty board, two-stone roots {49,60}/{59,60},
S2 {59,60}, classes 1/2/4 all UNKNOWN).
