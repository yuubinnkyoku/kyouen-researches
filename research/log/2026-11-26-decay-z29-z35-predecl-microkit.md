# 2026-11-26 — decay-curve micro-kit z=29..z=35: one-past parity-decay 3/3 per parity (m=17 UP 1v0 / m=18 DOWN 0v1 both exactly-one HITS), two-past secondary-birth FULL HIT both parities (gap-3 {15,18} / gap-2 (16,18)), m=14 three-past zero-separation prediction HALF-REFUTED (original died but the secondary follows the ROW-parity decay 2->0), TERTIARY separations discovered born at 4-past (m=13 {13,18}, m=14 (14,18)) and 6-past slot next, the {13,16} secondary DIED at 3 slices after birth, four first-ever z=29 touches all conform, k=37/k=38 supply candidates confirmed (10/10)

Kit: `research/experiments/strip-decay-z29-z35-20261126/`
(explore_decay_z29_z35.py `608eeec8` / engine_block.py `582c93c1`
pin `bd5f22e4` / frozen .out `9c4f18e7` 17,695 B / README).

Slot check (pre-claim, at kit-build time): latest main head `d49b480a`
(the frontier micro-kit itself). No published engine value exists for
any position measured here (the m=17 row at z=34, m=18 row at z=35,
m=15 row at z=31, m=16 row at z=32, m=14 rows at z=29/30, m=13 rows
at z=29/30, the four z=29 touch spots); every value was first touched
at the frozen first run, except the 12 listed recheck anchors. All
candidates were frozen in the docstring BEFORE the first run, drafted
from PUBLISHED frontier-kit observations + the K0832 closed form
only; 6/6 runs byte-identical (~9 s per run); post-freeze ordered
engine audit 16/16 identical; K0832 battery 38/38.

## §2 Registered predictions vs measured

1. m=17 @ z=34 (ONE past, ODD): predicted exactly one separation
   {17,18}@S=35 UP 1v0. MEASURED: 32 shapes, exactly one — HIT.
   Odd decay now 3/3 (m=13@z=26, m=15@z=30, m=17@z=34).
2. m=18 @ z=35 (ONE past, EVEN): predicted exactly one (18,18)@S=36
   DOWN 0v1. MEASURED: 26 shapes, exactly one — HIT. Even decay 3/3
   (m=14@z=27, m=16@z=31, m=18@z=35).
3. m=15 @ z=31 (TWO past, ODD): predicted exactly two: original
   {15,16}@S=31 DOWN 1v2 (stuck value 1) + secondary {15,18}@S=33 UP
   2v0. MEASURED: 50 shapes, exactly those two — FULL HIT (the
   original-stuck and gap-3 secondary predictions both hold).
4. m=16 @ z=32 (TWO past, EVEN): predicted (16,16)@S=32 DOWN 0v2 +
   secondary (16,18)@S=34 UP 2v1. MEASURED: 40 shapes, exactly those
   two — FULL HIT (gap-2 rule holds).
5. m=14 @ z=29 (THREE past, EVEN): predicted ZERO separations (both
   shapes conform). MEASURED: 62 shapes, ONE separation —
   HALF-REFUTED in the most informative way: the original (14,14)
   DID die conform (its death completed the 3-slice lifetime),
   but the secondary (14,16)@S=30 did NOT decay 2->1; it decayed
   2->0 — the ROW-parity decay, secondary included — and persists
   DOWN 0v1. The "secondary decays like the odd m=13 case" analogy
   is dead: the decay is a property of the ROW, not of the
   separation.
6. m=13 @ z=29 (FOUR past, ODD): non-binding stuck-value expectation
   held ({13,16}@S=29 DOWN 1v2, value still 1) but the "ONLY
   separation" wording is FALSIFIED: a NEW TERTIARY {13,18}@S=31 UP
   2v0 was BORN at four-past (76 shapes, exactly two separations).
7. m=13 @ z=30 (FIVE past, kit-added NO CANDIDATE): 76 shapes, ONE
   separation {13,18}@S=31 UP 1v0 — the secondary {13,16} DIED
   conform exactly 3 slices after its birth ({13,16}: born 2v0 at
   z=27, 1v0 at z=28, 1v2 at z=29, conform at z=30). 3-slice
   lifetime datum 2.
8. m=14 @ z=30 (FOUR past, kit-added NO CANDIDATE): 62 shapes, TWO
   separations: (14,16)@S=30 DOWN 0v2 (still stuck at 0, collapse
   rose to 2) and the NEW TERTIARY (14,18)@S=32 UP 2v1 born at
   four-past — the EVEN 4-past birth slot, datum 2 (with m=13).
9. z=29 touch u1..u4 = 0,1,1,0 ALL CONFORM via the frozen option
   tables. m=18 base-spot on-line z-sequence now z in {16..29} =
   0,1,0,1,0,1,0,1,1,1,1,1,1,1 (14 members); m=17 z-sequence
   z in {16..29} = all zero (8 members).
10. Rechecks 12/12 value==published (four z=28 touches + eight
    frontier-kit separation values; the `match` field is the conform
    criterion — False BY DESIGN for separation anchors, disclosed
    in the frozen output's match_field_note).
11. k=37 (twenty-eighth tail, ODD): hold {0} U {12..37}, then UNIFORM
    0v1 for s in {38..71} — CONFIRMED by closed-form scan; odd-z
    supply chain candidate 10/10. k=38 (twenty-ninth, EVEN): break
    0v2 at s=38, then UNIFORM 2v1 for s in {39..72} — CONFIRMED;
    even chain candidate 10/10. z=37/z=38-slice supply data
    precomputed.

## §3 The SEPARATION LIFE-CYCLE structure candidate (multi-datum now; m in {13..18}, z <= 35)

Across the published curves (m=13: z=25..30 the deepest; m=14:
z=26..30; m=15: z=29..31; m=16: z=30..32; m=17: z=33..34; m=18:
z=34..35) the finite observations now line up as: in the m-row at
slice z*(m)+2d (d = 0,1,2,...) a separation is BORN at shape
(m, m+2d+1) for ODD m / (m, m+2d) for EVEN m (gaps 1,3,5 resp.
0,2,4 — data: m=13 {13,14}/{13,16}/{13,18}; m=14 (14,14)/(14,16)/
(14,18); m=15 {15,16}/{15,18}; m=16 (16,16)/(16,18); m=17 {17,18};
m=18 (18,18)) with value 2; after birth the value is STUCK at
1 (odd row) resp. 0 (even row) — never 2 again; death (conform) hits
at birth+3 in all four observed deaths ({13,14} died at 3-past,
{13,16} died at 5-past, (14,14) died at 3-past, and by prediction
(14,16) dies at 5-past z=31). Visibility (UP/DOWN/conform-invisible)
is value-vs-collapse and closed-form-computable per slice. This
remains a CANDIDATE scaffold from finite observations; no universal
claim.

## §5 Handoff (new registrations, all BEFORE any measurement)

1. DEATH-VALLEY predictions (the boldest falsifiable next points,
   both parities, THREE past): m=15 @ z=32 — predicted ZERO
   separations ({15,16} dead at 3-past; {15,18} stuck at 1 =
   collapse v(33,32,49)=1 conform-invisible); m=16 @ z=33 —
   predicted ZERO separations ((16,16) dead; (16,18) stuck 0 =
   collapse v(34,33,51)=0). Two consecutive empty rows would be the
   first "clean valley" between birth waves.
2. TERTIARY-BIRTH next points (FOUR past): m=15 @ z=33 — predicted
   ONE separation {15,20}@S=35 born UP 2v0 (only separation;
   collapse v(35,33,49)=0); m=16 @ z=34 — predicted ONE separation
   (16,20)@S=36 born UP 2v1 (only; collapse v(36,34,51)=1); m=13 @
   z=31 (SIX past) — predicted TWO: {13,18} DOWN 1v2 (stuck 1 vs
   collapse v(31,31,45)=2) + {13,20}@S=33 born UP 2v0 (collapse
   v(33,31,45)=0); m=14 @ z=31 (FIVE past) — predicted ZERO
   ((14,16) dead at birth+3; (14,18) stuck 0 = collapse
   v(32,31,47)=0 conform-invisible).
3. m=13 @ z=32 (SEVEN past, kit-added next) — predicted ONE:
   {13,20} UP 1v0 ({13,18} dead at birth+3; collapse v(33,32,46)=0).
4. BASE-SPOT z=30 touch: blind option tables with the now-PUBLISHED
   u3/u4 as C-child inputs (w3 = H(49;(18,18);30) table {B-child =
   w1 = H(48;{17,18};30) blind, C-child 1^u3 = 1^1 = 0 PUBLISHED} ->
   candidate mex{w1,0}=1 iff w1=0; w4 = H(48;(17,17);30) table
   {B-child = w2 = H(47;{16,17};30) blind, C-child 1^u4 = 1^0 = 1
   PUBLISHED} -> candidate mex{w2,1}=0 iff w2=1; w1/w2 blind
   collapse-conform picks (v(35,30,48), v(33,30,47)).
5. TAIL SUPPLY next: k=39 (thirtieth, ODD: hold {0} U {12..39},
   uniform 0v1 s in {40..73}); k=40 (thirty-first, EVEN: hold
   {0} U {12..39}, 0v2 at s=40, uniform 2v1 s in {41..74}).
6. z=26 floor-21 (z-5 CRITICAL) census kit remains the registered
   heavy lane (head row not derivable from published data; needs the
   even-critical same-floor profile rederivation first).
7. 11x11 UNKNOWN: unchanged. No action.

## §6 Caveats

Finite machine observations only; candidate scaffolds stated per
section; no universal claim; no K slot claimed (1 experiment != 1
K). Raw engine pinned at `bd5f22e4…`. All collapse constants quoted
in the registrations are K0832 closed-form values re-derivable from
the published form. 11x11 empty board, two-stone roots, S2, class
1/2/4, 19 central-reply roots and all closure classes: UNKNOWN
unchanged; no verdict consumed.
