# SIEVE7-U/V: stretch-5/6 watched tracking by composition, spf = 7

Experiment date: 2026-11-18. Item: K0936. Object: the spf = 7 instance of
the SIEVE structure in the K0928 reduced games U(m)/V(m): by iterating the
published composition chain STR2 (K0931) -> S3/S4 (K0933) -> LAD-GEN
(K0934) -> WATCH-MAP (K0935), the watched label is tracked through
stretch-5 and stretch-6 by pure arithmetic on (w, h, n, a); the resulting
32-row class table proves, for every domain m, that the watched survives
stretch 5 and dies at stretch 6 exactly when 7 | 2m+s, hot (V, holding
7) resp. cold (U, holding 6). Via the proved RED (K0928) this resolves
the twin laws LAW1/LAW2 on ALL their residue classes mod 210 (57 + 57,
of which 8 + 8 are new for spf = 7): on those classes the laws are now
theorems, with the prime side collapsed to the three finite pins
C in {3,5,7} resp. {2,4,6}.

All statements below are about the K0859/K0928 reduced games only
(uniform board, REMO continuation, K0928 Lemma P pot dynamics). Nothing
here concerns non-uniform boards or the 11x11 census.

## Setup

U(m): m players, all holding 2, pot 2, pointer 0; watched label m-1;
N = 2m+3. V(m): m players, all holding 2, pot 1, pointer 0; watched
label 0; N = 2m+1. Phase rule (K0928 Lemma P): deal pot stones one each
from the pointer, the loser is the active player at (ptr+pot) mod k
(post-deal), the loser's post-deal holding becomes the new pot, the
pointer moves to the loser's slot after removal. A stretch is a maximal
run of constant pot; the pot during stretch w is w. RED (K0928, proved):
P(2m+1) = 1 + 2V(m) and P(2m+2) = 3 + 2U(m), so P(C) = 1 forces
V(m) = 0 (the watched label 0 is the survivor of V(m)) and P(C) = C-1
forces U(m) = m-1.

Call m DOMAIN (for its side) iff 3 does not divide N and 5 does not
divide N: V: m mod 3 != 1 and m mod 5 != 2; U: m mod 3 != 0 and
m mod 5 != 1. By SIEVE3 (K0931) and SIEVE5 (K0933), in domain the
watched survives stretch 2 and stretch 4; by S3 (K0933) the stretch-4
entry state is exactly F(4, h4; n4) with the watched at distance a4,
with (h4, a4) one of the four published families per side
(V: (1,1) or (3,3); U: (0,1) or (2,3)) and n4 affine in m.

## Statement

**Theorem SIEVE7-U/V (proved).** Let m be domain for its side, s the
side offset (V: s=1, U: s=3), N = 2m+s. Then, for every domain m >= 3:

(i) the watched survives stretch 5;

(ii) the watched dies in stretch 6  <=>  7 | N and N > 7. The death is
    hot-final (V: the watched is the breaking loser, holding 7) resp.
    cold (U: block loser, holding 6), at phase n3 // 7 of stretch 6,
    where n3 is the stretch-6 circle size;

(iii) if 7 does not divide N (including N = 7, where the game ends with
    the watched as survivor), the watched survives stretch 6.

**Corollary SIEVE-COMPOSITE (spf in {3,5,7}, proved).** For every m >= 1
with N = 2m+s composite and spf(N) in {3,5,7}, the watched dies at
stretch spf(N)-1, holding spf(N) (V) resp. spf(N)-1 (U), hot (V) resp.
cold (U). (spf = 3: K0931; spf = 5: K0933; spf = 7: SIEVE7 here. No
composite N with spf <= 7 exists below m = 3.)

**Corollary LAW1/LAW2 mod 210 (proved).** For every odd C >= 3 with
3 | C or 5 | C or 7 | C (57 residue classes mod 210):
P(C) = 1 <=> C prime. For every even C >= 2 with 3 | C+1 or 5 | C+1 or
7 | C+1 (57 residue classes mod 210): P(C) = C-1 <=> C+1 prime.
Proof: RED turns the laws into watched-survival statements about
V((C-1)/2) resp. U((C-2)/2). If C is an odd prime in one of the 57
classes then 3, 5 or 7 divides C, so C in {3,5,7}: pinned
(P(3)=P(5)=P(7)=1). Likewise C+1 in {3,5,7} for LAW2: pinned
(P(2)=1, P(4)=3, P(6)=5). Every other C in the classes is composite
with spf(N) in {3,5,7}, so by SIEVE-COMPOSITE the watched dies, hence
V(m) != 0 and U(m) != m-1, so P(C) != 1 and P(C) != C-1. The new
classes resolved here are the 8 odd residues {7, 49, 77, 91, 119, 133,
161, 203} (mod 210) and, for LAW2, the 8 even residues {6, 48, 76, 90,
118, 132, 160, 202}. The remaining residue classes of C mod 210 depend
on spf >= 11 and stay open; the prime-side survival for general N
remains the SIEVE conjecture.

## Proof of SIEVE7-U/V

**Composition region (m >= 60).** Write the domain class c = m mod 30
and m = 30j + c; m >= 60 forces j >= 2, and every j >= 2 gives a domain
m in the same class. The proof is the iteration

    (w, h, n, a) = stretch-4 start (S3, published)
    -> LAD-GEN (K0934): death criterion + end-state census
    -> WATCH-MAP (K0935): surviving watched position in the next state

applied twice. The point is that every branch parameter the two
theorems consult is a CLASS CONSTANT except the last one:

1. STR2+S3 (published) give the stretch-4 entry as F(4, h4; n4), watched
   a4, with n4 = 15j + c4 (S3's closed forms are affine in m with
   slope 1/2; e.g. V-A1: n4 = 3k with m = 6k+3 = 30j+3 -> n4 = 15j).
   h4, a4 and r4 = n4 mod 5 = c4 mod 5 are class constants. The domain
   condition excludes exactly the S4 death residue r4 (U: n4 = 0 mod 5
   for the a4=1 families, n4 = 2 mod 5 for a4=3; V: mirrored), so the
   watched survives stretch 4.

2. WATCH-MAP at (4, h4, n4, a4) (published w=4 tables) sends the
   watched to a2 (class constant, one of {1,2,3,4}), h2 (class
   constant) and n2 = n4 - t4 - [r4 >= h4] with t4 = n4 // 5 = 3j +
   c4 // 5. So n2 = 12j + c2: the slope 12 is FORCED by the
   composition; only c2 is a class constant. r5 = n2 mod 6 = c2 mod 6
   and t5 = n2 // 6 = 2j + e5 are then class-affine.

3. Stretch-5 criterion (LAD-GEN (e) via WM-COMP): the watched dies
   iff a2 = r5 + 1, i.e. a2 = c2 mod 6 + 1 - both sides class
   constants. The 32-row table below verifies a2 != r5+1 in every
   class: NO stretch-5 death ever occurs in domain. This is (i).

4. WATCH-MAP at (5, h2, n2, a2) sends the watched to a3 and h3 (class
   constants) and n3 = n2 - t5 - [r5 >= h2] = 10j + c3 (slope 10
   forced again).

5. Stretch-6 criterion: the watched dies iff a3 = r6 + 1 with
   r6 = n3 mod 7 = (3j + c3) mod 7 - the ONLY j-dependent branch
   parameter in the whole iteration. Since gcd(3, 7) = 1, the
   solutions form exactly one residue class j = rho (mod 7). The death
   type is also class-constant: V has a3 <= h3 in every class (hot
   breaking loser, holding w+1 = 7, phase t6), U has a3 = h3 + 1 in
   every class (cold block-t6 loser, holding w = 6, phase t6); in both
   cases LAD-GEN (d) gives the death phase as t6 = n3 // 7. This is
   the per-class content of (ii).

6. Congruence identity: 7 | N = 2(30j+c)+s is 4j + 2c + s = 0
   (mod 7), again a single residue class of j (mod 7). For each row
   the two residues coincide: rho is recorded in the table and the
   identity is the one-line substitution 3rho + c3 = a3 - 1 (mod 7)
   and 4rho + 2c + s = 0 (mod 7) (machine-verified per row, CLASS
   check rho == exp_rho). Hence death at stretch 6 <=> 7 | N; and for
   m >= 60, N >= 2*60+1 = 121 > 7, so 7 | N automatically means the
   composite case of (ii), and 7 not dividing N gives (iii).

7. Validity for ALL j >= 2, not just the machine range: the
   composition theorems need n >= 2w+2 at each stretch and 1 <= a <=
   w+1 for the criterion. From the affine forms, over all 32 classes:
   n4 = 15j + c4 >= 29, n2 = 12j + c2 >= 19, n3 = 10j + c3 >= 16 at
   j = 2, growing with j; and a2 in {1,2,3,4} <= 6, a3 in {1,4,5} <= 7.
   So every j >= 2 lies in the composition domain, and steps 1-6 hold
   for the whole unbounded region m >= 60. The table itself is a
   finite object (32 rows of class constants) obtained by applying the
   published closed forms; every row is machine-verified against the
   tracker and against fresh full simulations (below), but the
   unboundedness is the content of steps 1-6, not of the machine run.

**Finite region (3 <= m < 60).** The full statement (i)+(ii)+(iii) is
checked exhaustively by fresh simulation for every domain m in
[3, 59] on both sides (62 domain pairs; 8 stretch-6 deaths: V m =
24, 38, 45, 59 and U m = 23, 37, 44, 58, with N = 49, 77, 91, 119);
non-domain m die at stretch 2 or 4 (SIEVE3/SIEVE5 regression). The
degenerate prime N = 7 (V m = 3; U m = 2 is outside the range) ends
the game with the watched as survivor, consistent with (iii).

## The 32-row class table (m = 30j + c, j >= 2)

Columns: the class (side, c, S3 case, c mod 5), the stretch-4 entry
n4, h4, r4 = n4 mod 5; the stretch-5 entry n2, h2, watched a2,
r5 = n2 mod 6, t5 = n2//6; the stretch-6 entry n3, h3, watched a3;
the death residue rho (death <=> j = rho mod 7 <=> 7 | 2m+s) and the
death type with holding.

| side | m mod 30 | case | n4 | h4 | r4 | n2 | h2 | a2 | r5 | t5 | n3 | h3 | a3 | rho | death |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| U | 2 | B-III | 15j+0 | 2 | 0 | 12j+0 | 1 | 2 | 0 | 2j+0 | 10j+0 | 0 | 1 | 0 | cold 6 |
| U | 4 | A-II | 15j+1 | 2 | 1 | 12j+1 | 0 | 1 | 1 | 2j+0 | 10j+0 | 4 | 5 | 6 | cold 6 |
| U | 5 | B-IV | 15j+2 | 0 | 2 | 12j+1 | 2 | 3 | 1 | 2j+0 | 10j+1 | 0 | 1 | 2 | cold 6 |
| U | 7 | A-I | 15j+3 | 0 | 3 | 12j+2 | 1 | 2 | 2 | 2j+0 | 10j+1 | 4 | 5 | 1 | cold 6 |
| U | 8 | B-III | 15j+3 | 2 | 3 | 12j+2 | 3 | 4 | 2 | 2j+0 | 10j+2 | 0 | 1 | 4 | cold 6 |
| U | 10 | A-II | 15j+4 | 2 | 4 | 12j+3 | 2 | 3 | 3 | 2j+0 | 10j+2 | 4 | 5 | 3 | cold 6 |
| U | 13 | A-I | 15j+6 | 0 | 1 | 12j+4 | 3 | 4 | 4 | 2j+0 | 10j+3 | 4 | 5 | 5 | cold 6 |
| U | 14 | B-III | 15j+6 | 2 | 1 | 12j+5 | 0 | 1 | 5 | 2j+0 | 10j+4 | 0 | 1 | 1 | cold 6 |
| U | 17 | B-IV | 15j+8 | 0 | 3 | 12j+6 | 1 | 2 | 0 | 2j+1 | 10j+5 | 0 | 1 | 3 | cold 6 |
| U | 19 | A-I | 15j+9 | 0 | 4 | 12j+7 | 0 | 1 | 1 | 2j+1 | 10j+5 | 4 | 5 | 2 | cold 6 |
| U | 20 | B-III | 15j+9 | 2 | 4 | 12j+7 | 2 | 3 | 1 | 2j+1 | 10j+6 | 0 | 1 | 5 | cold 6 |
| U | 22 | A-II | 15j+10 | 2 | 0 | 12j+8 | 1 | 2 | 2 | 2j+1 | 10j+6 | 4 | 5 | 4 | cold 6 |
| U | 23 | B-IV | 15j+11 | 0 | 1 | 12j+8 | 3 | 4 | 2 | 2j+1 | 10j+7 | 0 | 1 | 0 | cold 6 |
| U | 25 | A-I | 15j+12 | 0 | 2 | 12j+9 | 2 | 3 | 3 | 2j+1 | 10j+7 | 4 | 5 | 6 | cold 6 |
| U | 28 | A-II | 15j+13 | 2 | 3 | 12j+10 | 3 | 4 | 4 | 2j+1 | 10j+8 | 4 | 5 | 1 | cold 6 |
| U | 29 | B-IV | 15j+14 | 0 | 4 | 12j+11 | 0 | 1 | 5 | 2j+1 | 10j+9 | 0 | 1 | 4 | cold 6 |
| V | 0 | V-A2 | 15j-1 | 1 | 4 | 12j-1 | 1 | 1 | 5 | 2j-1 | 10j-1 | 1 | 1 | 5 | hot 7 |
| V | 3 | V-A1 | 15j+0 | 3 | 0 | 12j+0 | 2 | 2 | 0 | 2j+0 | 10j+0 | 1 | 1 | 0 | hot 7 |
| V | 5 | V-B2 | 15j+1 | 3 | 1 | 12j+1 | 1 | 1 | 1 | 2j+0 | 10j+0 | 5 | 5 | 6 | hot 7 |
| V | 6 | V-A2 | 15j+2 | 1 | 2 | 12j+1 | 3 | 3 | 1 | 2j+0 | 10j+1 | 1 | 1 | 2 | hot 7 |
| V | 8 | V-B1 | 15j+3 | 1 | 3 | 12j+2 | 2 | 2 | 2 | 2j+0 | 10j+1 | 5 | 5 | 1 | hot 7 |
| V | 9 | V-A1 | 15j+3 | 3 | 3 | 12j+2 | 4 | 4 | 2 | 2j+0 | 10j+2 | 1 | 1 | 4 | hot 7 |
| V | 11 | V-B2 | 15j+4 | 3 | 4 | 12j+3 | 3 | 3 | 3 | 2j+0 | 10j+2 | 5 | 5 | 3 | hot 7 |
| V | 14 | V-B1 | 15j+6 | 1 | 1 | 12j+4 | 4 | 4 | 4 | 2j+0 | 10j+3 | 5 | 5 | 5 | hot 7 |
| V | 15 | V-A1 | 15j+6 | 3 | 1 | 12j+5 | 1 | 1 | 5 | 2j+0 | 10j+4 | 1 | 1 | 1 | hot 7 |
| V | 18 | V-A2 | 15j+8 | 1 | 3 | 12j+6 | 2 | 2 | 0 | 2j+1 | 10j+5 | 1 | 1 | 3 | hot 7 |
| V | 20 | V-B1 | 15j+9 | 1 | 4 | 12j+7 | 1 | 1 | 1 | 2j+1 | 10j+5 | 5 | 5 | 2 | hot 7 |
| V | 21 | V-A1 | 15j+9 | 3 | 4 | 12j+7 | 3 | 3 | 1 | 2j+1 | 10j+6 | 1 | 1 | 5 | hot 7 |
| V | 23 | V-B2 | 15j+10 | 3 | 0 | 12j+8 | 2 | 2 | 2 | 2j+1 | 10j+6 | 5 | 5 | 4 | hot 7 |
| V | 24 | V-A2 | 15j+11 | 1 | 1 | 12j+8 | 4 | 4 | 2 | 2j+1 | 10j+7 | 1 | 1 | 0 | hot 7 |
| V | 26 | V-B1 | 15j+12 | 1 | 2 | 12j+9 | 3 | 3 | 3 | 2j+1 | 10j+7 | 5 | 5 | 6 | hot 7 |
| V | 29 | V-B2 | 15j+13 | 3 | 3 | 12j+10 | 4 | 4 | 4 | 2j+1 | 10j+8 | 5 | 5 | 1 | hot 7 |

Reading examples: V c=24 (V-A2, m = 5 mod 6, m = 4 mod 5): m = 24
gives N = 49 = 7^2; the row says n3 = 10j-3 (j=0: 7), a3 = h3 = 1,
rho = 0, hot 7 - and indeed V(24) dies at stretch 6, phase 7//7 = 1,
holding 7. U c=23 (B-IV, m = 3 mod 5): U(23) with N = 49 dies cold
holding 6 at phase n3//7 = 7//7 = 1 (the stretch-6 state is the
collapse configuration F(6,0;7), the watched being its block-1
loser). In every U row a3 = h3+1 (first cold position), in every V
row a3 = h3 (the hot breaking position).

## Machine verification (sieve7_verify.py, audit_build.py)

The LAD-GEN core (ladder_gen, watch_dies, watchmap) is copied verbatim
from the published K0934/K0935 verifiers; the play() engine follows
the K0928 Lemma P phase rule exactly as in the published K0932/K0933
verifiers; the tracker (track) is the composition of the two. Checks
(m = 1..700 fresh simulations of both sides unless noted):

  - PIN        committed K0929 tables (sha256, format, P(1..40)).
  - REDRECON   committed U/V tables vs committed P table via proved
               RED, m <= 3999 (7,998 comparisons, 0 mismatches).
  - FRESHPIN   fresh survivors == committed U/V tables (1,400 games).
  - CANON      every tracker stretch entry (pots 2..6) equals the
               engine entry: n, holdings [w]^(n-h)+[w+1]^h, watched
               at n-a (4,358 entries, 0 fails).
  - TRK        tracker death/survival == engine for every m in
               [60,700] both sides: death pot, holding, phase within
               the stretch, run lengths (1,282 games, 0 fails).
  - S3REG      tracker stretch-4 entry == published K0933 S3 closed
               forms (854 checks).
  - K935TBL    tracker stretch-5 entry == published K0935 w=4 tables
               (684 domain checks).
  - SV7EDGE    finite region 3 <= m < 60: (i)/(ii)/(iii) exhaustive,
               plus the non-domain stretch-2/4 regression (62 domain
               pairs, 8 stretch-6 deaths, 0 fails).
  - SV7        composition region 60 <= m <= 700, domain classes:
               no stretch-5 death, stretch-6 death <=> 7 | 2m+s,
               hot/cold semantics, holding 7/6, phase = n3//7
               (684 domain pairs; 98 deaths, 586 survivals, 0 fails).
  - CLASS      the 32-row table: affine fits exact for j = 2..16,
               constants uniform per class, exactly one death residue
               equal to the residue of 7 | 2(30j+c)+s, holding and
               death type uniform, engine agreement for every j
               (32/32 rows, 0 fails).
  - TWIN210    twin laws on the committed P table, C <= 8000:
               LAW1 over all 57 odd classes and LAW2 over all 57 even
               classes (4,343 numbers, 0 violations; the 8+8 new
               classes are exactly the spf = 7 residues listed in the
               corollary).
  - SIEVEOBS   observation only (NOT part of the theorem): for every
               m <= 700, the watched dies at pot spf(N)-1 holding
               spf(N) (V) / spf(N)-1 (U) iff N composite, is the
               survivor iff N prime, and every watched death pot is
               even (1,400 games, 0 exceptions).

audit_build.py runs the suite twice in-process, asserts agreement and
writes the deterministic output/sieve7_uv_audit.json (no timestamps,
sorted keys; the 32-row table is embedded in full). File sha256
5a0fa03a4a36faf1277bc026a3e4652b2541bbef85c0f3769639e9e3aa3c8ac2;
two cold invocations produce byte-identical audits (payload sha256
25a15e07c69c5cd9cccaa9dad7e4fb6692f5896f794771e0d628ea1e905c6315).

The proofs above are paper proofs composed of published universal
theorems; the script is the machine anchor, not the proof.

## Limitations

- Domain: the SIEVE statement quantifies over the K0928 reduced games
  only; non-domain m (3 | N or 5 | N) are covered by K0931/K0933.
- The spf >= 11 part of the SIEVE conjecture (composite side) and the
  prime-side survival for general N remain OPEN; SIEVEOBS is machine
  observation (m <= 700), not a theorem.
- The class-table machine verification covers j = 2..16 per class and
  m <= 700 overall; the unbounded claim rests on the paper argument
  (branch parameters class-constant, slopes forced, single j-residue
  mod 7, affine lower bounds keeping every j >= 2 in domain).
- The twin laws are now theorems on the 57+57 classes with 3, 5 or 7
  dividing C resp. C+1; they say nothing about C in the remaining
  residue classes, and no closed form for P(C) is claimed.
- Not run: `uv run check/build`, unittests (no clone/uv in this
  environment). generated/ and the root README untouched. The 11x11
  census and all board-game statements are untouched (UNKNOWN).
