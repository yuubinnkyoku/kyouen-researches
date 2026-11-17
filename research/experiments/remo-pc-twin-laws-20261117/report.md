# P(C) twin prime laws, parity theorem, and the U/V reduction (K0859 counting recursion)

Experiment date: 2026-11-17. Items: K0928 (proved structure), K0929 (conjectured
twin laws). Object: the K0859 theorem-D counting recursion E(C,r) on the uniform
board with zero reset; P(C) = S(C,C), proved r-independent in K0926 (E6U).

All statements below are about run(C,r) of the K0859 recursion only. Nothing in
this experiment concerns non-uniform boards.

## Recursion (reference)

run(C,r): r players P_0..P_{r-1}, stone counts c_i >= 0, pointer position
`turn` (into the active list). While more than one player is active, a phase
does: ell = C - s where s = total stones held by active players; deal ell
stones one each to positions turn, turn+1, ... (cyclically, active players
only); the loser is the player at position (turn + ell) mod k (k = active
count, i.e. the next position after the last dealt stone); the loser's stones
are removed from their count (count reset to 0) and the loser leaves; the
pointer moves to the loser's position in the shortened list. Survivor = last
remaining player. This is exactly the logic of the K0926 verifier's
`survivor_fast` / `run_trace` (cross-checked by PIN/REF/TWIN below).

## Lemma P (pot reformulation; universal, proved)

Define pot = C - s (the stones to be dealt in the current phase). After a
phase in which the loser holds c-bar stones (post-deal), the new total is
s' = s + ell - c-bar = C - c-bar, hence pot' = c-bar. So the stones dealt in
each phase are exactly the stones held by the previously eliminated player,
and s + pot = C is invariant. In particular, starting from a state where all
active players hold 1 stone, the continuation depends only on the cyclic
sequence of holdings, the pointer, and the pot; the explicit target C never
enters again.

By the K0926 Lemma CAS, run(C,r) for r >= C+1 reaches K_C = (active =
P_0..P_{C-1}, all counts 1, turn 0, pot 0). run(C,C) phase 1 deals C stones
to C players (one each) and eliminates P_0 (position C mod C = 0) holding 1,
leaving C-1 players each holding 1, pot 1, pointer 0. After relabeling, both
continuations are the same game G(C): C players each holding 1 stone, pot 0,
pointer 0. Hence P(C) is the survivor of G(C) for every C >= 1 (and P(1) = 0).

## Lemma E (first stretch, even C; universal, proved)

Let C = 2m+2 >= 4 even. In G(C), the first m+2 phases eliminate exactly
P_0, P_2, P_4, ..., P_{2m}, P_1, in this order, with holdings 1,1,...,1,2
(P_0 holds 1; each even P_{2j} holds 1; P_1 holds 2 when eliminated), and
after phase m+2 the state is: active = [P_3, P_5, ..., P_{2m+1}] (m players),
each holding exactly 2 stones, pot = 2, pointer at P_3.

Proof. Induction on the phase index j = 2..m+2. Invariant before phase j
(2 <= j <= m+1): the eliminated set is {P_0, P_2, ..., P_{2j-4}}; the active
list in cyclic (original) order is [P_1, P_3, ..., P_{2j-3}] followed by
[P_{2j-2}, P_{2j}, ..., P_{2m}] followed by [P_{2m+1}]; holdings: P_1, P_3,
..., P_{2j-5} hold 2 (each received exactly one dealt stone in its own phase),
all other active players hold 1; pot = 1; pointer at position j-2, which is
P_{2j-3} (the odds P_1..P_{2j-3} occupy positions 0..j-2). Base j=2: after
phase 1 (eliminate P_0 holding 1, pot 1, pointer 0 = P_1) the invariant holds.
Step: phase j deals pot=1 stone to position j-2 (P_{2j-3}, which now holds 2)
and eliminates position (j-2)+1 = j-1, which is P_{2j-2} holding 1 (it did not
receive a stone this phase); pot returns to 1; the pointer moves to position
(j-1) in the shortened list, which is again the next odd player P_{2j-1}.
The position arithmetic is within bounds since j-1 < k = 2m+3-j throughout
(j <= m+1). Final phase j = m+2: the active list is the odds
[P_1, P_3, ..., P_{2m-1}, P_{2m+1}] (m+1 players) with P_1..P_{2m-1} holding
2 and P_{2m+1} holding 1, pointer at position m (P_{2m+1}). The phase deals
1 stone to P_{2m+1} (now 2) and eliminates position (m+1) mod (m+1) = 0, i.e.
P_1 holding 2; pot becomes 2; the pointer is at position 0 = P_3. All m
remaining players P_3, ..., P_{2m+1} hold exactly 2. QED.

Machine anchor: STRE, even C = 4..120, exact elimination order, holdings,
reduced state (violations 0).

## Lemma O (first stretch, odd C; universal, proved)

Let C = 2m+1 >= 3 odd. In G(C), the first m+1 phases eliminate exactly
P_0, P_2, ..., P_{2m} in this order, each holding 1, and after phase m+1 the
state is: active = [P_1, P_3, ..., P_{2m-1}] (m players), each holding exactly
2 stones, pot = 1, pointer at P_1.

Proof. Same induction; before phase j (2 <= j <= m+1) the active list is
[P_1, P_3, ..., P_{2j-3}] followed by [P_{2j-2}, P_{2j}, ..., P_{2m}] (no
trailing odd player, since C-1 = 2m is even); phase j deals 1 to P_{2j-3}
and eliminates P_{2j-2} at position j-1. At j = m+1 the active list is the
odds P_1..P_{2m-1} (holding 2, ..., 2, 1 for P_{2m-1}) followed by P_{2m};
the phase deals 1 to P_{2m-1} (now 2) and eliminates position m, which is
P_{2m} holding 1; pot = 1; pointer at position 0 = P_1. All m remaining
players hold exactly 2. QED.

Machine anchor: STRO, odd C = 3..121, violations 0.

## Theorem PAR (parity; universal, proved)

For every C >= 2, P(C) is odd.

Proof. C = 2: direct computation (P(2) = 1). C >= 4 even: by Lemma E, after
the first m+2 phases every remaining player has odd index (P_3, ..., P_{C-1});
eliminations afterwards can only remove remaining players, so the survivor is
odd. C >= 3 odd: by Lemma O the remaining players are P_1, ..., P_{C-2}, all
odd. QED.

Machine anchors: STRE/STRO (stretch structure), LAWS parity field on the
committed table C <= 8000 (violations 0), COR.

## Theorem RED (reduction to uniform games; universal, proved)

Define two families of reduced games, depending only on m:
- U(m): m players, each holding 2 stones, pot 2, pointer at position 0;
- V(m): m players, each holding 2 stones, pot 1, pointer at position 0.
(In both, the pot rule of Lemma P applies: deal the pot starting at the
pointer, eliminate the next player, the pot becomes their holding, the
pointer moves past them; total stones are conserved: 2m+2 resp. 2m+1.)

Then for all m >= 1:
  P(2m+2) = 3 + 2*U(m)   and   P(2m+1) = 1 + 2*V(m),
where U(m), V(m) denote the survivor's 0-based position in the reduced
circle.

Proof. By Lemma E the continuation of G(2m+2) after the first stretch is
exactly U(m) with the identification P_{3+2i} <-> i (uniform holdings 2, pot
2, pointer at i=0), so the survivor is P_{3+2*U(m)}. By Lemma O the
continuation of G(2m+1) is V(m) with P_{1+2i} <-> i (uniform 2, pot 1,
pointer at 0), so the survivor is P_{1+2*V(m)}. By Lemma P the continuation
dynamics only depend on the cyclic holding sequence, pointer and pot. QED.

Machine anchors: RED (python reduced reimplementation vs committed tables,
m <= 150), RECON (the committed P table C <= 8000 is reconstructed exactly
from the committed U/V tables, both parities, all m), plus 10 direct spot
checks in 8000 < C <= 16001 (see below).

## Corollary (proved halves of the twin laws)

(i) P(C) >= 3 for all even C >= 4; in particular P(C) = 1 never holds for
even C >= 4 (as 3 + 2*U(m) >= 3).
(ii) P(C) <= C-2 for all odd C >= 3; in particular P(C) = C-1 never holds for
odd C >= 3 (as 1 + 2*V(m) <= 1 + 2(m-1) = C-2).
Together with P(1) = 0 = C-1 and P(2) = 1, this shows:
LAW1 (P(C) = 1 <=> C prime) is equivalent to the V-conjecture below, and
LAW2 (P(C) = C-1 <=> C+1 prime) is equivalent to the U-conjecture below.

## Conjectures (machine ranges only; no universal claim)

LAW1: P(C) = 1  <=>  C is prime.
  Machine: committed direct table C <= 8000 (1007 primes, all with P = 1;
  0 violations), consistent via RED up to C <= 16001.
  Extends the K0922 observation (C <= 300) by more than an order of magnitude.

LAW2: P(C) = C-1  <=>  C+1 is prime.
  Machine: committed direct table C <= 8000 (1006 values, all with P = C-1;
  0 violations), consistent via RED up to C <= 16001.
  This identifies the K0922 "61 values with P(C) = C-1 for C <= 300" list
  exactly: they are the C <= 300 with C+1 prime (61 = pi(301) - 1).

V-conjecture: V(m) = 0  <=>  2m+1 is prime.
  Machine: committed reduced table m <= 8000 (1862 zeros, all at primes of
  the form 2m+1; 0 violations).

U-conjecture: U(m) = m-1  <=>  2m+3 is prime.
  Machine: committed reduced table m <= 8000 (1861 values; 0 violations).

By the Corollary, V-conjecture <=> LAW1 and U-conjecture <=> LAW2 as
universal statements; all four remain conjectures.

## Data and cross-verification

Engines (pinned by sha256 in the audit):
- pc_fast.js (sha256 563d9601d782ab0ebda7b44741260ef12dd8d0273f6fab088c7c5f20d3bba8b8):
  direct closed-form-phase engine, two implementations (closed-form and
  verbatim per-stone), C <= 8000 in 121.5 s (Node 22, TypedArrays).
- pc_reduced.js (sha256 3e9730eeca273a6634ae5b432ed3c1d2df4ed58942b83bf83ae1cb513dcd7e41):
  reduced-game engine on a different state space (no C, no ell recomputation),
  m <= 8000 in 66.1 s.
- data/pc_p8000.json (sha256 58a414bc31fb6266cc2d0e10000436e50f396135847bab5a32163cffff0b975e):
  {"N": 8000, "P": [P(1), ..., P(8000)]}.
- data/pc_uv8000.json (sha256 8a3b318bd26b8197c66fd55d79007654d2926a18af165132af8c194bc76d8ae2):
  {"M": 8000, "U": [...], "V": [...]}.

Independence: (a) pc_fast.js vs the K0926 published python `survivor_fast`
logic: identical on C <= 400; verbatim per-stone twin identical on C <= 200
(and the verifier recomputes C <= 300 in python, REF); (b) pc_reduced.js
reconstructs the full committed P table via RED with 0 violations (RECON,
7999 checks covering both parities); (c) the verifier's own python
reduced-game reimplementation matches the committed U/V tables m <= 150
(RED); (d) direct spot re-checks of P(C) against the RED reconstruction at
C in {8011, 9338, 10001, 11315, 12007, 13333, 14127, 15002, 15555, 16001}:
10/10 OK (pc_fast.js vs pc_reduced.js, outside the committed direct range).

Verifier: verify_pc_twin_laws.py (stdlib only, deterministic, ~0.5 s).
10 checks PIN / REF / TWIN / STRE / STRO / RED / RECON / LAWS / REDLAWS / COR,
all OK. Audit output/pc_twin_laws_audit.json byte-identical across cold runs
(sha256 6bc2ee08b51d465f74797cba1a3b3ecb9d48601394b0b9821842d992495a53b2).

## Further finite observations (not promoted to conjectures)

- P(C) is always the index of an odd player (Theorem PAR); the first stretch
  is a clean "sieve pass" eliminating every second player, suggesting a
  stretch-hierarchy (the U/V games are the weight-2 level; their own first
  stretches would be weight-3 games). The stretch-hierarchy beyond level 2 is
  not worked out here.
- Small-value structure (finite, from the committed tables, m <= 8000):
  P(C) = 7 occurs only at C = 3*m' with m' in {5, 9, 13, 29, 41, 53, 73,
  101, ...} (all m' = 1 mod 4, but not all 1 mod 4 occur); P(C) = 5 occurs at
  C in {6, 8, 9, 14, 38, 62, 74, 158, ...}. No closed form is claimed.
- P(2^k) for k = 1..12: 1, 3, 5, 15, 27, 47, 71, 255, 455, 719, 807, 4079;
  equals 2^k - 1 exactly at k in {1, 2, 4, 8} (consistent with LAW2: the
  Fermat primes 3, 5, 17, 257; k = 12 gives 2^12+1 = 4097 = 17*241
  composite and indeed P(4096) = 4079 != 4095).

## Limitations

Uniform board, zero reset, K0859 recursion only; no statement about
non-uniform boards. LAW1/LAW2/U-conjecture/V-conjecture are conjectures with
finite machine evidence, not theorems; the machine evidence beyond C > 8000
rests on Theorem RED (proved) plus the committed reduced tables. P(C) has no
closed form claimed for general C. The 11x11 open-board status is unchanged
(empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 all
UNKNOWN).
