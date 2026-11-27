# kit-19x: independent blind second census of the kit-19 registered rows

Kit dir: `research/experiments/strip-newband-m53m54-blind-second-census-20261127/`

## What this is

The same hourly lane's parallel execution was detected building kit-19
(knowledge mount `_kit19-build/`, determinism runs in progress; kit-19 not
on main at this census's freeze). Following the kit-17x / kit-18x
precedent, this run avoided duplicating the kit-19 build and instead
constructed an INDEPENDENT BLIND SECOND CENSUS of the same registered rows.
The parallel lane's kit-19 explorer source and any kit-19 run outputs were
NOT read before this census was frozen. The record of record for the
kit-19 rows is the parallel lane's kit-19 (published separately); this kit
is the independent second sensor. The authoritative published-vs-published
cross-check follows the kit-18x precedent once kit-19 is on main.

## Registration source (public SSOT only)

The 34-item kit-19 registration machine-parsed from the published kit-18
frozen output section `future_slice_registration_constants`
(main HEAD 9ac8e079, `.out` sha256 `c3087285fbdbd44d0588132f9c1d4c75fce2913b816ce383a5f0b377154364ba`,
engine pin `bd5f22e4...`). 49 measured rows:

- 28 ladder rows: one-past (m,z) and birth (m,z), m=19..32, next depth
- 2 frontier rows: m=53 @ z=105, m=54 @ z=106 (FIRST-EVER m>52 rows)
- 16 window rows: m=51 z in {93..100}, m=52 z in {94..101} (= z*(m)-8..-1)
- 3 evenlife rows: m=14/16/18 @ z=3m+18 (NON-BINDING, contingent on the
  published kit-18 z=3m+16 3/3 EXACT outcomes)

## Semantics and independence

Measurement semantics reconstructed from the published kit-18 explorer
(SSOT): per row (m,z), R=m+z+1, S in [m, max(m+38,z+2)], X = all
nondecreasing token multisets with min(X)=m and arity<=3, hv=H_canonical(R,X,z),
ev=single_token(S,z,R), separation iff hv != ev. The enumeration is a
FRESH nested-loop implementation (`parts` in census_kit19x.py); the engine
is the published `engine_block.py` byte-clone (sha256 `582c93c1...`, pin
`bd5f22e4...` on the embedded block). Before any kit-19x row was measured,
the harness reproduced all 49 published kit-18 row records exactly
(VALIDATE-PASS 49/49: separation lists and shape counts byte-equal).

## Results (all finite observations; NO universal claim)

- **Frontier 40th/41st datum, both EXACT**: m=53 @ z=105, R=159,
  {53,54}@S=107 UP 2v0 (collapse v(107,105,159)=0); m=54 @ z=106, R=161,
  (54,54)@S=108 UP 2v1 (collapse v(108,106,161)=1). First-ever m>52 rows;
  frontier parity scaffold now 42/42 for m=13..54.
- **Windows 16/16 CLEAN**: m=51 z{93..100} and m=52 z{94..101}, zero
  separations each, as registered (candidates; no strip-derivation claim).
- **Ladder 28/28 FULL HIT**: every registered seat separation present with
  exact (X, S, direction, value, collapse); every registered dead seat
  conforms; every registered stack candidate is an exact mimic; zero
  separations outside seats + rule-v2 shadows. Boundary equistack observed
  again: m=27 birth, co=54=2m at the NEW seat, {27,27,27}@S=81 UP 2v0 is an
  exact mimic of {27,54}@S=81.
- **Evenlife z=3m+18 3/3 template EXACT** (NON-BINDING): stick {m,2m+18}
  DOWN 0v2 + NEW {m,2m+20} UP 2v1 for m=14/16/18; 4th consecutive even-m
  lifecycle depth (z=3m+12, +14, +16, +18 all template-EXACT).
- Totals: 49 rows, 273 separations (kit-18: 241), 46 binding rows FULL HIT.

## Verification

- Validation: 49/49 published kit-18 rows reproduced exactly before
  measurement (VALIDATE-PASS, kit18.out sha pin c3087285...).
- Determinism: 2 full passes over all 49 rows (4 chunked runs each)
  byte-identical; PYTHONHASHSEED=random spot chunk byte-identical.
- Audit: `audit_kit19x.py` 10/10 gates PASS, 2 runs byte-identical
  (engine pin, kit-18 source pin, census pin, 30/30 registration texts
  byte-verbatim vs the public .out, 6 spot rows live-recomputed,
  structure 49=28+2+16+3, windows 16/16 clean, frontier exact values,
  totals, VERIFY-PASS, VALIDATE-PASS).
- Tamper: 3/3 fail-closed on scratch copies (T1 frontier value flip ->
  G2+G4+G5b; T2 phantom window separation -> G2+G5a+G5c; T3 prediction
  text flip -> G2+G3), clean control rc=0.
- All published files ASCII.

## Honest disclosure

1. The parallel kit-19 build was detected via the shared knowledge mount
   (file listing + chunk-progress status lines only). The kit-18 frozen
   `.out` and `engine_block.py` used as registration source / engine pin
   are byte-identical to main HEAD (sha256 machine-verified against the
   published pins); no kit-19 measured content was read before freeze.
2. The frozen kit-19 one-past prediction texts omit the rule-v2 stack
   lists (the birth texts carry them). The measured one-past shadows are
   exactly the standing rule-v2 admissible co-splits (co>=2m, both split
   tokens >= m), per-row counts m19:12, m20:11, m21:7, m22:6, m23:5,
   m24:4, m25:3, m26:2, m27..m32:0 (co<2m non-admissible), each an exact
   seat mimic; zero other separations. This is disclosed, not a kit-19
   registration defect claim.
3. The first harness build without the per-S H cache clear was OOM-killed
   (rc 137) in the 1GB cgroup; fixed with the published kit-18 per-S
   clear practice (values identical; re-validated 49/49).
4. Chunked execution (4 chunks per pass) is a wall-time measure only; each
   chunk re-derives its rows from scratch (no cross-chunk state).
5. The kit-19 authoritative cross-check (published kit-19 .out vs this
   frozen census, kit-18x pattern) is PENDING until the parallel lane
   publishes kit-19.

## Standing caveats

The 11x11 empty board, all 19 central-reply roots, the two-stone root
{60,27}, the third move {100,108}, S2 and closure classes 1/2/4 remain
UNKNOWN at all times; no verdict is consumed. The frontier parity scaffold
42/42, the rule-v2 shadow enumeration, the boundary equistack and the
even-m lifecycle templates are finite observations, not laws.

## Files

- `census_kit19x.py` - fresh harness (validate + measure modes)
- `census_kit19x.out` - frozen census (sha256
  `275faedc80d04e2899c081eb7c56a0bcb80f7cf01b644793c6b846eb3d10a2f4`, 97,357 bytes)
- `verify_kit19x.py` / `verify.json` - FULL-HIT verification vs registration
- `assemble_kit19x.py` - frozen-output assembler
- `audit_kit19x.py` - 10 fail-closed gates
- `tamper_kit19x.py` - 3-test tamper battery
- `engine_block.py` - published engine byte-clone (sha256 `582c93c1...`)
- `kit19_registration_extracted.json` - machine-parsed 34-item registration
