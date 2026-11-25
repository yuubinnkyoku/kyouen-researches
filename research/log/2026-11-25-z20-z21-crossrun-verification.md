# 2026-11-25 z=20/z=21 cross-run verification + base-spot lattice parity lemma — verification log

Lane: high-speed lane (a different hourly execution of the recurring
task than the one that published the z20/z21 censuses). Status of this
document: verification record + one new engine-free closed-form lemma
(provisional knowledge item K1332). No census slot is claimed; no
universal statement is made beyond the K0832-derived lemma; no verdict
of any game position is consumed.

## 1. Context: collision avoidance record

This lane's earlier same-day session had independently built and
executed a z=20 min>=15 (floor-15) pre-declaration census kit (script
explore_z20f15.py adapted from the published z19 kit script, five
byte-identical runs plus an ordered-engine cross-check). Immediately
before pushing, the mandatory latest-main refetch found the SAME census
already published by the parallel hourly execution: commit `2cc16d34`
(19:08:02Z, z20-min15 kit + predecl log) and, minutes later, `8a106233`
(19:17:52Z, z21-min16 kit + predecl log). Per the collision protocol the
duplicate push was CANCELLED (this lane pushed no z=20 kit file), and
this run pivoted to post-publication verification, which is what this
log records. The retained local z=20 measurements (this kit's
`z20_crossrun/` files) and a FRESH z=21 re-derivation
(`verify_z21_indep.py`, built new in this session from this lane's own
z20 explorer, NOT from the published z21 script) are published here as
the cross-run side of the verification.

## 2. Kit construction (post-publication, fresh derivation)

- `verify_z21_indep.py` (sha256 `43aa03b2...`), adapted from this lane's
  own z20 explorer (sha256 `d4df9769...`, itself descended from the
  published z19 kit script `e41138e2...` at commit `6a6832ce`): all z21
  parameter sets re-derived in this session from the lattice law
  R=m+z+1 (floor 16, cells j=1..15 with R=j+22, s-domain {0} u {16..46},
  tail spots {47..54}, strip m in {16..20}, spots m in {21..24}, base
  spot (38;(16,16);21), below-band (22;Y;22), record rows m in
  {15,14,13,12}, identity domains {0} u {12..58}), plus a NEW
  engine-free section (h) base_spot_lattice_parity_closed_form.
- Engine block embedded byte-identical to the published chain engine
  (startup pin `bd5f22e4...` asserted at runtime, gate PASS; standalone
  file sha256 `582c93c1...` included in the kit).
- Determinism: FOUR runs byte-identical (default x2, PYTHONHASHSEED=1,
  env -i isolated directory), rc 0 each; frozen `verify_z21_indep.out`
  (sha256 `07ef7cd4...`) IS that stdout.
- Both published frozen outputs were fetched after publication and
  saved locally with sha verification: the local copies are
  byte-identical to the published pins (z20 `09e9026a...`, z21
  `10f94100...`). Comparisons ran against those byte-verified copies.

## 3. Results (all judgment-free)

### 3.1 z=21 independent verification: FULL AGREEMENT

`compare_z21.py` against the published frozen z21 output: **330 rows /
436 field checks / 0 mismatches** (rc 0). Full-value row equality on:
the engine pin; 15 cells x 96 shapes (every deviant dict identical:
F {20 DOWN 1v2 + hole@21 + tail 22..46 UP 2v0 with shape counts
1..9}, G {20 DOWN 0v1}, E {18 DOWN 1v2, 20 UP 2v0}, D {18 DOWN 0v1},
C {16 DOWN 1v2, 18 UP 2v0}, B {16 DOWN 0v1}, A {16 UP 2v0},
A2..A9 collapsed; multivalue 0); 120 tail spots (F 8/8 mismatch,
others 112/112); strip cumulative 44/79/107/130/150 with 0 violations;
records m15 50/0 + ext 49/0, m14 62/0, m13 76/0, m12 92/0; 12 strip
spots all match; base spot H(38;(16,16);21)=1=v(32,21,38); below-band
96 shapes 0 deviants 0 multivalue; all three identity sections as full
value rows (twelfth hold {0} u {12..21} + uniform 0v1 s>=22;
thirteenth hold {0} u {12..21} + 0v2@22 + uniform 2v1 s>=23;
fourteenth hold {0} u {12..23} + uniform 0v1 s>=24).

### 3.2 z=20 cross-run verification: FULL AGREEMENT

`compare_z20.py` against the published frozen z20 output: **242 rows /
335 field checks / 0 mismatches** (rc 0), over the shared sections: 14
cells x 105 shapes, 112 tail spots, strip 185 shapes 0 violations
(cumulative 55/99/134/162/185), records m14 62/0 + ext 61/0, m13 76/0,
m12 92/0, 12 strip spots, base spot H(36;(15,15);20)=0, below-band
105/0/0, eleventh + twelfth identities over the shared s-domain
{0} u {12..56} (the published kit's identity domains extend one step
further; those extra rows are outside this lane's z20 script and are
excluded from the count).

Consequence: every measured cell/tail/strip/record/spot/base/below-band
value of BOTH published censuses is cross-run reproduced. The A21f16
A-rank break rebirth (s=16=z-5, UP 2v0), the F21f16 twelfth hole+tail
form, the K1325 m=12 residual band closure (92/0 at its frontier
z*(12)=22), and the fourteenth-tail supply datum all agree
value-for-value with the published frozen rows.

### 3.3 Base-spot lattice parity lemma (NEW, engine-free, proved)

**Lemma (K1332, provisional number): for every z >= 11,
v(2z-10; z; 2z-4) = z (mod 2)**, where (R;X;z) = (2z-4; (z-5,z-5); z) is
the slice-z base-spot lattice position (T-Zz numbering R=m+z+1 at
m=z-5).

Proof (pure K0832 single-token closed form): with x=2z-10,
(i) 1 <= z <= x-1 = 2z-11 (iff z>=11), so the middle regime applies;
(ii) q_odd(z) <= z < R = 2z-4 (z>4), so R is past the q_odd threshold;
(iii) R < x+z = 3z-10 (iff z>6), so the (R+z)%2 branch is selected.
Hence v = (R+z)%2 = (3z-4)%2 = z (mod 2).

Machine cross-check (kit `verify_z21_indep.py` section (h), engine-free):
z in {11..200}, 190/190 rows consistent with all four branch invariants
recorded per row, 0 mismatches.

**Corollary (proved slices):** for each z in {15,16,17,18,19}, the
published strip theorem T-Zz (K1320 min>=10, K1322 min>=11, K1325
min>=12, K1328 min>=13, K1330 min>=14; claim position R=m+z+1,
min(X)=m>=z-5, universal) covers the base-spot position
X=(z-5,z-5), so H(2z-4;(z-5,z-5);z) = z (mod 2) is a THEOREM COROLLARY
(value row z=15..19: 1,0,1,0,1). This promotes four points (z=16..19) of
the published base-spot z-parity sequence (recorded in the published z20
and z21 kit logs as "SIX data points 0/1/0/1/0/1, z=22 candidate: 0",
i.e. as observations) to corollaries, and adds the z=15 point (=1) which
was not in the published observation list.

**Remaining observations:** the z=20 and z=21 points (0 and 1) sit on
the same closed-form parity on the collapse side, but the absorption
identity (base-spot H value = collapse value) at z=20/21 is so far a
pair of census observations; both were cross-run re-verified in this
session (sections 3.1, 3.2). They become corollaries once T-Z20 and
T-Z21 are declared.

**Same-day confirmation:** while this run was being prepared, the
parallel lane published the z=22-min17 census kit (commit `115c0bb9`),
which measured the z=22 base spot H(40;(17,17);22) = 0 = v(34,22,40)
(the kit's "seventh parity point") — exactly this lemma's closed-form
prediction for z=22. It remains an observation until T-Z22 is declared.

**Predictions:** z=23 base spot 1, z=24 base spot 0, and so on, for as
long as absorption persists — the collapse-side parity is closed-form
for ALL z >= 11; only the absorption side needs the slice proofs.

## 4. Honest record (this run)

- **Prior-work check:** repo-wide code search found no existing
  base-spot parity item ("base-spot parity" in research/knowledge/: zero
  hits); the published z20/z21 census logs record
  the base-spot sequence as data points with the z=22 candidate, with
  NO closed-form proof — the lemma and its corollary are new here.
- **K number:** provisional. The repo currently carries TWO distinct
  items numbered K1330 (items/K1330-strip-z19-min14.md and
  items/K1330-pg2q8-pgammal-cap-orbits.md, concurrent lanes), so
  K1332 is claimed provisionally and integration-time renumbering is
  expected per the repo convention.
- **Independence limits:** the verified census values come from the
  same pinned engine bytes as the publishing run's; the environment is
  the same remote sandbox class (fresh session; the z21 derivation was
  rebuilt in this session from this lane's own lineage and its output
  compared as parsed values, not as a byte clone of the published
  script's stdout). This is a cross-run re-measurement, not a
  third-party hardware verification.
- No wall-clock, no randomness, no hash-seed dependence in any frozen
  output; the comparison counts are field-level, disclosed above.
- The z=22 census predeclaration (position-set {18,20,22} with the
  definition-domain exclusion, even-z station identity, F single-point
  at s=22, base-spot candidate 0, fifteenth-tail pre-computation)
  remains the publishing lane's handoff item and was NOT touched here.

## 5. Handoff

- T-Z20 / T-Z21 declaration lanes: both census inputs now carry an
  independent cross-run verification (this kit); the base-spot collapse
  parity is closed-form for all z>=11, so their proofs only need the
  absorption side.
- The next census lane (z=22) should re-fetch main before pushing as
  usual; this kit does not touch the z=22 slice.
- K1332 numbering reconciliation belongs to the integration pass.

## 6. Standard caveats

Everything in this kit and log is FINITE machine observation against
the pinned raw engine, plus pure closed-form checks; the only proved
statement added is the K0832-derived parity lemma (and its corollaries
on proved slices). No verdict of any game position is consumed.
Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2
{59,60}, classes 1/2/4, and all central-reply roots: all UNKNOWN,
unchanged. The battery/spot counts are engine cross-checks, not proof
substitutes.
