# 2026-11-26 — registered-handoff execution: TWENTY-SECOND-tail candidate HOLD (odd supply form 7/7 candidate), m=18 base-spot z=25 resolved at both readings, first z=25 boundary survey all-conform, K1335 m=16 band clean at z=25

Slot check (pre-claim, per registered handoffs): at kit-build time the
latest main (head `d3d7405b`, 2026-11-26T02:25:13Z) contained the
published z=24 floor-18 census kit (commit `35f7fe59`) and its §5
handoffs, NO T-Z24 declaration, no z24-min19 critical census beyond it,
and no z=25 work of any kind (`"floor-19" OR f19` → 0 hits; the only
"TWENTY-SECOND-tail" hit was the z24f18 §5 handoff text itself). The
z24f18 §5 item #1 (T-Z24 / z24-min19 declaration lane) was deliberately
left untouched: its strips m ∈ {19..23} are already measured clean by
the published kit and the rest is a proof task. This kit takes exactly
the §5 items #2 and #3 — both finished completely here.

## §1 Context and kit role

The z24f18 kit's §5 ranked the fast-lane-constrained leftovers: item #2
(the TWENTY-SECOND-tail, k=31 odd-form supply identity: the natural
next of the even/odd supply-identity chain) and item #3 (the m=18
base-spot z-sequence anomaly: register a blind z=25 pick BEFORE
measuring, after the alternation broke at z=24 with nine points on
record). This kit executes both, adds the consolidated supply table
(k ∈ {23..31}, domain extended by one point to {0}∪{12..65}), and uses
the opportunity to take the first machine data at the completely
un-opened z=25 frontier: eleven blind boundary spots covering the
on-line m=18 pair, the one-above pair named literally by the §5 text,
their complete direct-input neighborhood, the m=17 on-line 4th member,
and the first two members of the K1335 m=16 residual band's z=25 entry.
Everything is a frozen pre-declaration: option-set resolution tables
were written into the docstring BEFORE the first run.

## §2 Kit construction and discipline (executed before the first run)

- Files: `explore_m18spot25_tail22.py` (frozen, sha256
  `28fa10099c5201b6a3b030982278ebbc2386ed1da3d5c9be1445bf43912282bb`),
  `engine_block.py` (byte-clone sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`,
  pin `bd5f22e4…` asserted at startup), frozen stdout
  `explore_m18spot25_tail22.out` (sha256
  `33fa0b657c89249a2d58e1c443ac255ee3343c99c129410648501cd335e63d01`,
  31,813 bytes). Six runs all byte-identical (frozen + default ×2 +
  PYTHONHASHSEED=random + env -i isolated dirs ×2), rc 0, ~0.2 s each.
- Section structure: (a) engine-free supply-identity table k ∈ {23..31}
  over s ∈ {0}∪{12..65}; (b) K0832 closed-form-vs-engine battery (18
  single-token literals); (c) blind spot census (11 first-ever + 6
  published rechecks); (d) deterministic resolution through the frozen
  tables.
- Hand derivations (frozen BEFORE the first run): the 22nd-tail
  candidate re-derived independently from the K0832 branch analysis (for
  s ∈ {12..31} both components equal s%2 — the z=32≥x+1 and z=31≥x+1
  branches with m<32, with the s=31 x=z boundary returning x%2=1; breaks
  at s=32: x%2=0 vs (R+z)%2=1; s ∈ {33..65}: (R+32)%2=0 vs (R+31)%2=1
  uniformly); the option-set decomposition of every measured pair written
  from the canonical-engine move rule; the collapse v(Σ,z,R) of every
  position via the PROVED K0832 closed form.
- Position-arithmetic disclosure: the m=18 base-spot z-sequence members
  are the ON-LINE pairs H(18+z+1;(18,18);z) (z=23: (42;·)=1 PROVED
  K1344 anchor, z=24: (43;·)=1 published), so the z=25 on-line member is
  (44;·;25); the z24f18 §5 text names (45;·;25) — one above. Both were
  measured, resolving the handoff under either reading. The blind pick
  registered BEFORE the run was the full frozen option-set table
  (mex{c25, 1^b24} with c25=(44;{17,18};25) and b24=(44;{18,18};24)
  both themselves blind) plus the two conditional candidates (m=16
  band continuation B=1; m=18 on-line "2 iff g=1").
- Drafting scratch (K1344-D6, strict form): engine cross-checks limited
  to already-published input literals ONLY — the six recheck anchors,
  the collapse literal closed forms, the supply-identity sample points.
  No drafting engine evaluation at ANY position measured by this kit:
  the eleven blind spots were first touched by the engine at the frozen
  first run.
- No file edited after any run.

## §3 Results (finite observations)

1. **TWENTY-SECOND-tail (k=31) NEW: candidate HOLD, both predeclared
   components** — v(s,32,32)=v(s,31,32) holds exactly on {0}∪{12..31}
   (21 points), breaks **0v1 at s=32**, **UNIFORM 0v1 for ALL s ∈
   {33..65}**. Odd-z supply form measured chain k=19/21/23/25/27/29
   (6/6 published) + k=31 here → candidate **7/7**. z=31 slice supply
   datum precomputed for the future z=31 declaration lane.
2. **14th..21st tail identities (k ∈ {23..30}) rechecked over the
   extended domain {0}∪{12..65}: every published constant reproduced**
   (odd-k first breaks at s=k+1 with uniform 0v1; even-k first breaks
   0v2 at s=k+1 then 2v1 tails — exactly as published by the series
   kits). The consolidated table is the kit's machine-recorded artifact.
3. **Item #3 resolved, first blind pick FIRED**: H(45;(18,18);25) = **0**
   = v(36,25,45) conforming; fired cell (c25=1, b24=0) → options
   {1, 1^0=1} → mex 0, exactly the §5 text's first guess.
4. **m=18 on-line z-sequence 11th member: H(44;(18,18);25) = 1 =
   v(36,25,44) CONFORMING** (fired cell g=0 → {0,0} → mex 1; the
   conditional value-2 branch did not fire). The on-line sequence
   z=16..25 now reads **0,1,0,1,0,1,0,1,1,1** — after breaking
   alternation at z=24, z=25 repeats 1 (second consecutive break
   instance; 10 finite points).
5. **First-ever z=25 boundary survey: 8/8 spots CONFORM** (zero
   deviations in the whole kit): on-line and one-above m=18 pairs,
   cross pairs (44;{17,18};25)=1 and (43;{17,18};25)=0, m=17 on-line
   4th member (43;(17,17);25)=0, one-below pair (42;(17,17);25)=1,
   m=16-line members (42;{16,17};25)=1 and (42;{16,18};25)=1 — all
   equal to their K0832 staircase collapses.
6. **K1335 m=16 residual band (z ∈ {22..29}) z=25 entry: first two
   members CLEAN — both registered band-continuation candidates HOLD**
   (B and the (16,18) member = their collapses = 1): fourth consecutive
   clean z (22/23/24/25 datapoints on record for the band).
7. **m=17 base-spot z-sequence: FOURTH consecutive zero** —
   H(43;(17,17);25)=0 conforming via B=1; z=22..25: 0,0,0,0 (the frozen
   surprise branch "2 iff B=0" did not fire).
8. **Six published rechecks reproduce the published values exactly**
   (determinism identity with the z24f18/K1344 frozen data):
   (42;(18,18);23)=1, (43;(18,18);24)=1, (42;{17,18};24)=0,
   (42;(17,17);24)=0, (41;(16,18);24)=1, (41;(16,17);24)=1.
9. **K0832 battery 18/18 PASS** (closed form vs raw engine at every
   single-token literal used by the kit).

## §4 Honest record

- The blind pre-registration took the honest structural form (frozen
  option-set tables, not naked value picks, because the direct inputs
  were themselves unmeasured); two conditional candidates were
  registered and one fired (band continuation) while the other did not
  (the m=18 on-line value-2 branch) — both outcomes are recorded as
  run data, not retro-fitted.
- All eleven blind spots first touched by the engine at the frozen
  first run; drafting engine work covered published literals only.
- Finite machine observations + PROVED closed-form evaluations +
  disclosed hand derivations with candidate status stated per section.
  No universal statement; no theorem claimed.
- No K slot claimed; no T-Z consumed (T-Z24 does not exist); the
  z24f18 §5 item #1 (declaration lane) untouched.
- 11×11 UNKNOWN unchanged (explicit).

## §5 Handoff (new registrations, all BEFORE any measurement)

Ranked next targets for the fast lane:

1. **TWENTY-THIRD-tail (k=32, EVEN form): registered candidate** —
   v(s,33,33) vs v(s,32,33) over the next extended domain {0}∪{12..66}:
   hold {0}∪{12..31}, break **0v2 at s=32**, then **UNIFORM 2v1 for ALL
   s ∈ {33..66}** (even-z supply form now measured 6/6 at
   k=20/22/24/26/28/30; k=32 would extend it to the 7/7 candidate;
   derivable from K0832 exactly as the 22nd was).
2. **z=26 floor-20 (EVEN) structural +2-shift registration**: by the
   machine-checked consecutive-even structural identity (z=18→20→22→24
   value-exact 15/15 shared cells per kit, four consecutive gaps), the
   registered candidate for the z=26 sub-critical edition is the
   11-entry deviant lattice at positions **{20,22,24,26}**: head trio
   @s=20 {B(j=6) DOWN 0v2, A(j=7) UP 1v0, A2(j=8) UP 2v1}; @s=22 {C UP
   1v0, B UP 2v1, D DOWN 0v2}; @s=24 {E UP 1v0, D UP 2v1, G DOWN 0v2};
   @s=26 {F UP 1v0, G UP 2v1}; all other rungs conform; 0 multivalue.
   Dependency-discipline note (answering the z24f18 §5 item #5): the
   z=26 head-trio DERIVATION with zero observational dependencies needs
   the z=25 lattice PROVED first (T-Z25 after T-Z24 — the same
   one-behind structure as every edition); this registration is a
   structural PREDICTION, not a derivation; the measuring kit must
   disclose which it relies on.
3. **Base-spot z-sequence z=26 blind picks (register BEFORE measuring)**:
   m=18 on-line 12th member H(45;(18,18);26) (chain z=16..25:
   0,1,0,1,0,1,0,1,1,1 — the candidate is a structural mex table over
   its blind inputs, as done here) and m=17 5th member H(44;(17,17);26)
   (chain 0,0,0,0).
4. **z=25 residual-band record entries (for whichever lane opens z=25
   first)**: the m=15 band (K1335, z ∈ {21..28}) z=25 entry and the
   **m=14 band (K1330, z ∈ {20..25}) z=25 entry = band COMPLETION** are
   unmeasured; a small record sweep mirroring this kit's m=16-first-
   members format would close the m=14 band. The m=13 band (K1328) is
   already complete at z=24 (z ∈ {19..24}).
5. **11×11 UNKNOWN: unchanged. No action.**

## §6 Caveats

Finite machine observations only, plus pure closed-form precomputations,
plus disclosed hand derivations whose candidate status is stated per
section; no universal claim; raw engine pinned at `bd5f22e4…` (embedded,
engine_gate PASS in the frozen output). 11×11 empty board, two-stone
roots, S2, class 1/2/4 and all central-reply roots: all UNKNOWN,
unchanged.
