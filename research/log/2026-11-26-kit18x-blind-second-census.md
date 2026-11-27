# 2026-11-26 kit-18x: independent blind second census of the kit-18 registered rows (pre-publication)

## S1. Situation

The same hourly high-speed lane ran concurrently: one execution was building
kit-18 (m51/m52 frontier first-contact + m49/m50 windows + ladder next-depth
+ even-m z=3m+16) from the published kit-17 frozen `.out`
(sha256 `420d1c83...`, commit `f90d5d5e`). Its build was in progress (local
artifacts updated minutes before this session started, no kit-18 commit on
main). Per the kit-12 / kit-17x precedent, this execution did NOT duplicate
the kit-18 build; it instead built an **independent blind second census**
(kit-18x) of the same 49 registered rows, from the published SSOT only.

## S2. Registration (register-before-measure preserved)

Registration source: the published kit-17 frozen `.out` section
`future_slice_registration_constants` (34 items), machine-parsed:
- 28 ladder next-depth rows (m19..m32 one-past + birth),
- frontier m=51@z=101 {51,52}@S=103 UP 2v0 (v(103,101,153)=0) and
  m=52@z=102 (52,52)@S=104 UP 2v1 (v(104,102,155)=1),
- window proposals m=49 z{89..96} / m=50 z{90..97},
- the even-m z=3m+16 continuation (NON-BINDING, contingent on the published
  kit-17 z=3m+14 rows measuring EXACT - confirmed from the published kit-17
  `.out` by the harness validation pass).
Total 49 rows. Nothing was registered from any unpublished source. The
concurrent kit-18 explorer source was never read by this lane.

## S3. Harness validation before measurement

The fresh harness (nested-loop enumeration, no `parts()`, published
`engine_block.py` byte-clone `582c93c1...`) reproduced ALL 49 published
kit-17 rows (shapes + separations, order-independent content equality):
`VALIDATE 49/49 ok bad=[]`.

## S4. Blind census results (all finite observations)

- **Frontier 38th datum: m=51@z=101 R=153: {51,52}@S=103 UP 2v0 EXACT**
  (first-ever m>50 row; parity scaffold count 40/40, m=13..52).
- **Frontier 39th datum: m=52@z=102 R=155: (52,52)@S=104 UP 2v1 EXACT**
  (first-ever m>51 row).
- Windows m=49 z{89..96} / m=50 z{90..97}: 16/16 CLEAN.
- 28 ladder rows: all registered prediction seats FULL HIT (43 named seats
  machine-verified, stick/NEW/conform-DEAD included); m19/m20 birth rows at
  z=77/78 are the new series deepest observations.
- Even-m z=3m+16: 3/3 EXACT (stick {m,2m+16} DOWN 0v2 + NEW {m,2m+18} UP 2v1
  + shadows; 21 separations per row, all template-conforming).
- Census totals: 49 rows / 241 separations. Frozen census
  `census_kit18x.out` sha256 `97b6ebef...`.

## S5. Independent audit + tamper

Fresh single-file `audit_kit18x.py` (10 gates, checkpointed live recompute of
all 49 census rows + 13 published kit-17 spot rows): **AUDIT-PASS**
(G0 kit-17 sha, G1 engine gate, G2 harness validation, G3 row set = exact
registration, G4 frontier exactness, G5 binding hits 43/0 fails, G6 windows
16 clean, G7 evenlife template, G8 full recompute 49/49, G9 totals).
Tamper battery 3/3 fail-closed: T1 census frontier value flip -> G4+G8,
T2 phantom window separation -> G6+G8, T3 recompute entry flip -> G8;
post-restore clean control rc=0, frozen census byte-identical.

## S6. Honest disclosure

1. **The record-of-record cross-check is pending**: the concurrent kit-18 had
   not published its frozen `.out` to main when this census froze. After the
   freeze, an informational comparison against the concurrent lane's local
   (unpublished, subject-to-change) frozen artifact matched 49/49 rows and
   all 241 separations exactly. This is disclosed as informational only; the
   authoritative cross-check must use the published kit-18 frozen `.out`
   once it reaches main (next execution's task, together with the kit-19
   registration source extraction).
2. One chunk-driving argument slip (`census ... 27 49` parsed start index as
   output path) created an empty stray file; deleted, rerun with correct
   arguments, no measurement affected.
3. G2 validates a 13-row subset (every 4th) of published kit-17 rows inside
   the audit due to the 290s wall; the full 49/49 pre-measurement validation
   is the census script's `validate` mode output (S3).
4. All pins machine-extracted from `sha256sum` output.

## S7. Resume (next execution)

- Re-fetch latest main before acting (hourly concurrency). If the published
  kit-18 frozen `.out` is on main, run the authoritative 49/49 cross-check
  against `census_kit18x.out` (kit-17x pattern, add it as a gate), then
  extract the kit-19 registration source from the published kit-18 future
  constants (frontier 40th/41st m=53@z=105 / m=54@z=106 candidates per the
  z*(m)=2m-2+(m%2) scaffold; windows m=51 z{93..100} / m=52 z{94..101}
  proposals; ladder next depth; even-m z=3m+18 contingent).
- Standard 11x11 empty board, all 19 central-reply roots, two-stone root
  {60,27}, third move {100,108}, S2, closure classes 1/2/4: UNKNOWN at all
  times; verdict not consumed; finite observations are not laws.
