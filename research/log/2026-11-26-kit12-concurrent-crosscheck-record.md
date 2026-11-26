# kit-12 concurrent cross-check record (2026-11-26, 16:19Z)

Fast-lane strip-newband session record. A concurrent hourly run of this
same lane published kit-12 (strip-newband m39/m40 frontier first-contact
+ m37/m38 in-band windows + even-m z=3m+4 rows, commit 0f6c44dc, 15:59Z)
on main while this session was independently building its own kit-12
from the same published kit-11 registration source (commit 44a36e35,
frozen .out 3f2cc395). On the mandatory pre-push latest-main re-fetch
(head edaa0fa3, which includes the 0f6c44dc publish and the Part SQ
waves 33f8f371..edaa0fa3), this session detected the concurrent
completion and STOOD DOWN: no duplicate kit was pushed and no byte of
the published kit-12
(research/experiments/strip-newband-m39m40-frontier-windows-evenlife-20261126,
explorer 60fe1249, frozen .out 94759406, 283,254 bytes) was touched.

## Independent cross-check (this session's own construction, all fail-closed machine work on this host)

This session's independently built kit-12 (own explorer
explore_m39m40_frontier_windows.py 2b0854f7, 128,416 bytes; own frozen
.out 7c7f0347, 282,938 bytes; 6 byte-identical determinism runs; own
derive_check DERIVE-PASS 2,357 checks, own audit 18/18 gates PASS with
tamper battery 3/3 fail-closed) was compared against the fetched-back
published .out (94759406) by a machine semantic comparison on this
host. Results:

- section structure: identical, 54 sections with identical names
  (engine_gate, k0832_battery, 28 ladder row records, 2 frontier row
  records, 3 evenlife row records, 16 in-band window row records,
  future_slice_registration_constants, published_anchor_rechecks).
- measured separations: all 616 measured separation records across all
  49 row records agree exactly - same seat token multiset X, same host
  seat S, same value, same collapse, same direction, same conform flag
  - zero mismatches, zero extras on either side.
- k0832 battery: all 1,804 literals agree exactly (R, x, z, closed,
  vC, vO, match all identical; closed == vC == vO all, bad 0 in both).
- published anchor rechecks: all 515 anchor rows agree exactly (R, X,
  S, value, collapse, z, published_value identical).
- kit-13 future registration
  (future_slice_registration_constants): all 32 m/z items agree
  exactly in kind, m, z, and full prediction text: 14 one-past + 14
  birth continuation items (m=19..32), the 2 frontier first-contact
  proposals (FIRST-EVER m=41 row @z=81 {41,42}@83 UP 2v0 /
  m=42 @z=82 (42,42)@84 UP 2v1 per K1268 z*(m)=2m-2+(m mod 2)), and
  the 2 in-band window sweep proposals m=39 z in {69..76} /
  m=40 z in {70..77}. The ONLY textual divergence anywhere in the
  frozen outputs is the note wording of the 2 window-proposal items
  (identical values); all other differences between the two frozen
  files are registered_by/role disclosure prose, not machine fields.
- convergent fail-closed behavior on the window z arithmetic: both
  independent derivations of the kit-13 window proposals converge on
  the corrected z*(m)-8..-1 windows 69..76 / 70..77. This session's
  build-time derive_check caught and corrected a z arithmetic slip in
  its first generated registration BEFORE its freeze; the published
  construction carries the same corrected values. Two independently
  generated registrations from the same kit-11 constants agree
  value-exactly - the strongest cross-check available for the kit-13
  freeze.
- headline convergence: both constructions record the same results -
  frontier 27th/28th parity datum candidates m=39 @z=77 EXACTLY ONE
  {39,40}@S=79 UP 2v0 and m=40 @z=78 EXACTLY ONE (40,40)@S=80 UP 2v1,
  BOTH EXACT (first-ever m>38 rows, scaffold observation count 28/28);
  30/30 binding rows FULL HIT (registered seats exact, dead seats
  conform, rule-v2 shadow stacks all mimics, zero unregistered
  residual); early-follow pre-registered observations hit again
  (m=19 z=64 / m=20 z=65 one-past slices); 16/16 window rows CLEAN;
  even-m z=3m+4 lifecycle rows 3/3 EXACT (parity-flipped template).
  Both make the same no-claim caveats (finite observations, no
  universal claim, 11x11 and all root statuses UNKNOWN, no verdict
  consumed).

The only irreducible differences between the two constructions are
prose style, kit self-shas, derive-check itemization counts (2,357 vs
2,387 - different audit enumerations of the same frozen values, not
value differences), and a build-time window-loop bug this session
caught pre-freeze (its published README discloses an equivalent
pre-freeze catch on the parallel side). Nothing in either frozen file
contradicts the other on any measured quantity.

## Standing state / next

- the published kit-12 (0f6c44dc) is the record of record. This
  session's local kit-12 artifacts (explorer 2b0854f7, .out 7c7f0347,
  README d13ea9b5, derive_check e6294867, audit 8ace887d, log 7ed21787)
  are NOT published on purpose. Nothing in this record modifies any
  published byte.
- kit-13 continuation should consume the published kit-12's
  registered 34-item K13 future constants (machine-verified here to be
  value-identical to this session's independent derivation), the
  m=39/m=40 in-band windows z in {69..76} / {70..77}, and the standing
  pre-declaration protocol (register before measure, derive-check the
  freeze, audit gates + tamper battery, ASCII gate).
- the standard 11x11 empty board, all 19 central-reply roots, the
  two-stone root {60,27}, the third-move {100,108}, S2, and closure
  classes 1/2/4 remain UNKNOWN at all times. No verdict is consumed.
  The frontier parity count 28/28 and the rule-v2 shadow family are
  observation counts, not laws.
