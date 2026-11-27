# 2026-11-26 — frontier rows z=27..z=34 + one-past/two-past decay micro-kit: PARITY-SPLIT FRONTIER LAW CANDIDATE 6/6 (m=15@z=29, m=16@z=30, m=17@z=33, m=18@z=34 all exactly-one separations at the predicted shapes), one-past decay is itself PARITY-SPLIT (odd 2->1 UP 1v0 / even 2->0 DOWN 0v1; naive uniform drop-2-to-1 REFUTED), secondary separations BORN at two-past, m=13 original shape DIES at three-past, four first-ever z=28 touches all conform, k=35/k=36 tail supply pre-computations confirmed

Kit: `research/experiments/strip-frontier-z27-z34-20261126/`
(explore_z27z34_frontier.py `0475c5d9` / engine_block.py `582c93c1`
pin `bd5f22e4` / frozen .out `fa55ae7b` 17,897 B / README).

Slot check (pre-claim, at kit-build time): latest main head `f5124331`
(2026-11-26T04:48:55Z). Counter-probes clean: NO z=27-slice census kit
(`filename:explore_z27` 0 hits), NO z=28..34 engine values of any kind
(`explore_z28`/`explore_z29`/`explore_frontier` 0 relevant hits), NO
frontier row record at z >= 27, "k=35" hits only the unrelated
n11-cost16 closure lane. The only published z=27 engine values are the
four z26f20 handoff spots. Every z in {27..34} position measured here
was touched by the engine for the FIRST time at the frozen first run,
except the 7 listed recheck anchors.

## §1 Role

Executes the z26f20 kit log S5 handoff items #1 (frontier test data),
#2 (one-past datum candidates), #3 (k=35 pre-computation), #4 (the
z=28 base-spot touch with blind option tables). All candidates were
frozen into the explore script docstring BEFORE the first run;
drafting used the published K0832 closed form and pure combinatorial
shape counting only — no engine recursion, no observational drafting
(nothing existed to observe).

## §2 Registered predictions vs measured (frozen docstring, run 1; 6/6 runs byte-identical)

FRONTIER ROW RECORDS (x0 style, R=m+z+1, parts >= m, co-token allowed,
arity <= 3, S in {m..m+38}):

1. m=15 @ z=29 (z*(15)=29, ODD): PREDICTED exactly one separation
   {15,16}@S=31 UP 2v0. MEASURED: 50 shapes, EXACTLY ONE separation
   {15,16}@S=31 UP 2v0. HIT. Parity-split datum 3.
2. m=16 @ z=30 (z*(16)=30, EVEN): PREDICTED (16,16)@S=32 UP 2v1.
   MEASURED: 40 shapes, exactly one separation (16,16)@S=32 UP 2v1.
   HIT. Datum 4.
3. m=17 @ z=33 (z*(17)=33, ODD): PREDICTED {17,18}@S=35 UP 2v0.
   MEASURED: 32 shapes, exactly one separation {17,18}@S=35 UP 2v0.
   HIT. Datum 5.
4. m=18 @ z=34 (z*(18)=34, EVEN): PREDICTED (18,18)@S=36 UP 2v1.
   MEASURED: 26 shapes, exactly one separation (18,18)@S=36 UP 2v1.
   HIT. Datum 6.

The z26f20 S5#1 parity-split frontier-record law candidate is now
6/6 (odd m=13/15/17 -> {m,m+1}@S=2m+1 UP 2v0; even m=14/16/18 ->
(m,m)@S=2m UP 2v1). STILL A CANDIDATE: six finite observations, m in
{13..18} only; no universal claim.

PAST-FRONTIER ROW RECORDS (NO CANDIDATE sections, recorded verbatim):

- m=13 @ z=27 (TWO-past; registered under S5#2, honestly relabelled):
  76 shapes, TWO separations: {13,14}@S=27 value 1 vs collapse 2
  (DOWN 1v2 — the old frontier shape now sits BELOW its collapse) and
  a NEW secondary {13,16}@S=29 UP 2v0.
- m=14 @ z=27 (ONE-past): 62 shapes, ONE separation: (14,14)@S=28
  value 0 vs collapse 1 (DOWN 0v1).
- m=15 @ z=30 (ONE-past, kit-added): 50 shapes, ONE separation:
  {15,16}@S=31 value 1 vs collapse 0 (UP 1v0).
- m=16 @ z=31 (ONE-past, kit-added): 40 shapes, ONE separation:
  (16,16)@S=32 value 0 vs collapse 1 (DOWN 0v1).
- m=13 @ z=28 (THREE-past, kit-added): 76 shapes, ONE separation:
  {13,16}@S=29 UP 1v0 — the original frontier shape {13,14}@S=27 is
  GONE (conform at z=28: engine value 1 = collapse 1). The original
  DIES at three-past for m=13.
- m=14 @ z=28 (TWO-past, kit-added): 62 shapes, TWO separations:
  (14,14)@S=28 DOWN 0v2 (original persists, still value 0, collapse
  rose to 2) and NEW secondary (14,16)@S=30 UP 2v1.

## §3 The new structural picture (all finite observations, z<=34, m<=18)

ONE-PAST PARITY DECAY candidate (2 data per parity): one slice past
its own frontier, the unique frontier separation PERSISTS at the same
shape, but the value drops PARITY-DEPENDENTLY: ODD m: 2 -> 1 (UP 1v0,
odd m=13@z=26 published, m=15@z=30 new); EVEN m: 2 -> 0 (DOWN 0v1,
m=14@z=27, m=16@z=31 new). This refutes the naive z26f20 S5#2
formulation (uniform drop 2->1) as stated; its m=13 datum was the odd
case.

SECONDARY-BIRTH candidate: at two-past the row gains a SECOND
separation (m, m+delta) with delta = 3 for the single odd datum
(m=13: {13,16}@S=29) and delta = 2 for the single even datum
(m=14: (14,16)@S=30), born at value 2. The secondary then decays
(m=13 secondary: 2 at z=27 -> 1 at z=28; candidate: 0/conform at
z=29). The original parity-decays and eventually DIES by crossing
into the collapse region (m=13 original: UP 2v0 -> UP 1v0 -> DOWN
1v2 -> conform at three-past).

Pending discriminators: m=15/m=16 two-past (secondary shape: gap 3
vs gap 2?), m=14 three-past z=29 (original death: m=13 precedent
says conform), m=17/m=18 one-past (parity decay candidates), see §5.

## §4 z=28 base-spot touch + rechecks + supply

- Four FIRST-EVER z=28 engine touches t1..t4 = 0,1,1,0 ALL CONFORM
  via the frozen option tables (t1/t2 blind collapse-conform picks;
  t3 mex{t1,0}=1 iff t1=0; t4 mex{t2,1}=0 iff t2=1 — both option
  tables held). m=18 base-spot on-line z-sequence now
  z in {16..28} = 0,1,0,1,0,1,0,1,1,1,1,1,1 (13 members; the
  post-z=23 run of ones reaches six consecutive slices);
  m=17 z-sequence z in {16..28} = all zero (7 members).
- Recheck anchors: 4/4 published z=27 handoff values reproduced;
  3/3 published frontier separation engine values reproduced
  ({13,14}@z=25 = 2, {13,14}@z=26 = 1, (14,14)@z=26 = 2). Semantic
  note: in the frozen JSON the separation-anchor rows carry
  `match: false` because that field is the collapse-CONFORM criterion
  `value == collapse == published_value`; for separation anchors the
  operative recheck criterion is `value == published_value` (3/3 PASS)
  — disclosed here and in the kit README.
- k=35 (twenty-sixth tail, ODD): registered S5#3 candidate CONFIRMED
  by closed-form scan over {0} U {12..69}: hold {0} U {12..35}, then
  UNIFORM 0v1 for all s in {36..69} (odd-z supply chain candidate
  9/9). k=36 (twenty-seventh tail, EVEN, kit-added): break 0v2 at
  s=36, then UNIFORM 2v1 for s in {37..70} (even chain candidate
  9/9). z=35/z=36-slice supply data precomputed for the future
  declaration lanes.
- K0832 battery 44/44 (closed form vs canonical engine vs ordered
  engine). Determinism 6/6 byte-identical (~11 s per run). Post-freeze
  ordered-engine audit of all 12 separations + 4 touches: 16/16
  identical.

## §5 Handoff (new registrations, all BEFORE any measurement, for future executions)

1. ONE-PAST PARITY-DECAY candidates (test the §3 rule at the values
   m=17/m=18): m=17@z=34 row — predicted unique separation
   {17,18}@S=35 UP 1v0 (odd decay; collapse v(35,34,52)=0);
   m=18@z=35 row — predicted unique separation (18,18)@S=36 DOWN
   0v1 (even decay; collapse v(36,35,54)=1). Register-then-measure.
2. SECONDARY-BIRTH+z28 NEXT SLICES (decay/death curve): m=15@z=31
   two-past (predicted: original {15,16}@31 DOWN 1v2 per the
   collapse jump v(31,31,47)=2 with odd value staying 1; secondary
   shape candidate {15,18}@S=33 UP 2v0 by the gap-3 rule); m=16@z=32
   two-past (original (16,16)@32 prediction: even value stays 0,
   collapse v(32,32,49)=2 -> DOWN 0v2; secondary candidate
   (16,18)@S=34 UP 2v1 by the gap-2 rule); m=14@z=29 three-past
   (candidate: original (14,14) DIES conform at z=29 per the m=13
   precedent; secondary (14,16) decays 2->1); m=13@z=29 four-past
   (candidate: secondary {13,16} decays 1->0-or-conform; NO
   hard value pick).
3. BASE-SPOT z=29 touch: blind option tables with the now-PUBLISHED
   t3/t4 as C-child inputs: u3 = H(48;(18,18);29) with frozen table
   {B-child = u1 = H(47;{17,18};29) blind, C-child 1^t3 = 1^1 = 0
   PUBLISHED by this kit} -> candidate mex{u1,0} = 1 iff u1=0;
   u4 = H(47;(17,17);29) with table {B-child = u2 = H(46;{16,17};29)
   blind, C-child 1^t4 = 1^0 = 1 PUBLISHED} -> candidate mex{u2,1}
   = 0 iff u2=1. u1/u2 are blind collapse-conform picks
   (v(35,29,47), v(33,29,46)).
4. TAIL SUPPLY next pre-computations: k=37 (twenty-eighth, ODD:
   hold {0} U {12..37}, uniform 0v1 s in {38..71}); k=38
   (twenty-ninth, EVEN: hold {0} U {12..37}, 0v2 at s=38, uniform
   2v1 s in {39..72}). K0832 closed-form, engine-free.
5. z=26 floor-21 (z-5 CRITICAL) census kit remains the registered
   heavy lane (its head row is NOT derivable from published data —
   needs the even-critical same-floor profile rederivation first;
   unchanged from z26f20 S5#3).
6. 11x11 UNKNOWN: unchanged. No action.

## §6 Caveats

Finite machine observations only, plus disclosed hand derivations
whose candidate status is stated per section; no universal claim; no
K slot claimed (1 experiment != 1 K). Raw engine pinned at
`bd5f22e4…`. Every measured z in {27..34} value was first touched at
the frozen run; drafting used closed form + combinatorics only.
11x11 empty board, two-stone roots, S2, class 1/2/4, 19
central-reply roots and all closure classes: UNKNOWN unchanged; no
verdict consumed.
