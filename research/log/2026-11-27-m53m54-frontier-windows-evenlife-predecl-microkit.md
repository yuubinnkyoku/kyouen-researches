# 2026-11-27 kit-19: strip-newband m53/m54 frontier first-contact + m51/m52 in-band windows + even-m z=3m+18 + ladder next depths (pre-declared microkit, TAKEOVER PUBLICATION)

## S1 Summary

kit-19 continues the strip-newband pre-declaration microkit series. The
registration source was the published kit-18 frozen .out (commit 9ac8e079,
sha256 c3087285..., 34 future constants). 49 rows were registered and
measured: 28 ladder m=19..32 next-depth one-past/birth rows, 2 frontier
first-contact rows, 16 in-band window rows, 3 even-m z=3m+18 lifecycle rows.
Total separations 273 = the data-driven registered count (audit G8).
The 30 binding rows are ALL FULL HIT with zero unregistered separations.

Highlights (all finite observations, no claim):
- Frontier 40th/41st parity datums, FIRST-EVER m>52 rows, both EXACT:
  m=53 @ z=105 {53,54}@S=107 UP 2v0 (collapse v(107,105,159)=0),
  m=54 @ z=106 (54,54)@S=108 UP 2v1 (collapse v(108,106,161)=1).
  Frontier parity scaffold now 42/42 (m=13..54). NOT a law.
- Windows m=51 z{93..100} / m=52 z{94..101}: 16/16 CLEAN (zero separations).
  First below-frontier m=51/m=52 rows.
- Ladder next depths; m19/m20 birth z=79/80 new series-deepest. Early-follow
  confirmed a 9th consecutive time (m=19 z=78: 12-split shadow set of co=60,
  host {19,60} UP 1v0; m=20 z=79: 11-split, host {20,60} DOWN 0v1).
- Boundary equistack 5th observation: birth NEW seat {27,54} @S=81 (co=54=2m
  exactly), equistack {27,27,27} an exact mimic (audit G13).
- Even-m z=3m+18 lifecycle 3/3 EXACT (stick {m,2m+18} DOWN 0v2 + NEW
  {m,2m+20} UP 2v1 + 23 seps/row, trio conform absent; chain observed
  z=3m-1..3m+18).
- Battery 2,290/2,290 (64 new). Anchors 1,662/1,662 (kit-18 census 241 spots
  first-anchored here).

## S2 Artifacts (kit dir research/experiments/strip-newband-m53m54-frontier-windows-evenlife-20261127/)

- README.md
- engine_block.py sha256 582c93c1... (byte-clone series engine)
- explore_m53m54_frontier_windows_evenlife.py sha256 9a010e43... (342,886 B)
- explore_m53m54_frontier_windows_evenlife.out sha256 12277fd4... (626,727 B)
- audit_kit19.py sha256 8fb44100... (20 gates)
- derive_check_kit19.py sha256 63ef1c73... (3,533 checks DERIVE-PASS)

## S3 Verification

- Determinism: 4 byte-identical runs (owner lane; run1..run4 CHUNK-DONE rc=0,
  all sha256 12277fd4...; takeover lane re-verified md5 equality of the four
  run files and the frozen .out before publishing).
- derive_check: 3,533 DERIVE-PASS, 0 fails; 3 takeover-lane invocations,
  byte-identical output.
- audit: 20/20 gates PASS; owner lane runs 1 and 2 byte-identical
  (cmp-verified); takeover-lane clean control via the checkpointed audit
  runner: AUDIT-PASS, byte-identical to both owner payloads.
- Tamper battery 3/3 fail-closed: T1 battery closed flip -> G3 (owner lane);
  T2 frontier m53 datum value flip -> G7+G9+G14 (takeover; single-field diff
  of the tampered file verified before audit; audit resumed from the owner
  lane's checkpoint pkl, deterministic); T3 anchor published_value flip ->
  G4 only (takeover; fresh tamper file, single-field diff verified). Frozen
  .out sha re-verified unchanged after the battery.
- kit-19x independent blind second census (commit f38d2b43, census sha256
  275faedc..., frozen before this kit's output was read by that lane): its
  pre-publication informational comparison against this kit's local frozen
  runs matched 49/49 rows and 273/273 separations exactly. The authoritative
  published-vs-published cross-check follows this publication.

## S4 Registration for kit-20 (engine-free, NOT measured here)

34 future constants (see frozen .out section future_slice_registration_constants):
- 28 ladder next-depth one-past/birth pairs m=19..m=32, rule-v2 stack lists
  composed FRESH for the kit-20 seats.
- Frontier 42nd/43rd: m=55 @ z=109 {55,56}@S=111 UP 2v0 (collapse
  v(111,109,165)=0) / m=56 @ z=110 (56,56)@S=112 UP 2v1 (collapse
  v(112,110,167)=1).
- Windows: m=53 z{97..104}, m=54 z{98..105}.
- Even-m z=3m+20 continuation proposal (contingent, NON-BINDING).

## S5 No-claim caveats

Finite observations only. Frontier parity 42/42, rule-v2 shadow observations
(early-follow 9/9, boundary equistack 5-observation series), and the even-m
lifecycle template are observation counts, not laws. The standard 11x11
empty board, all 19 central-reply roots, the two-stone root {60,27}, the
third-move {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all
times. No verdict is consumed. Nodes and shape counts are bookkeeping. No
K-slot claim is made.

## S6 Honest disclosure

1. TAKEOVER PUBLICATION: the kit-19 owner lane fell silent at ~03:37Z after
   completing generation, the 4-run determinism battery, both audit runs and
   tamper T1. Per the kit-16 takeover precedent the concurrent kit-19x census
   lane completed tamper T2/T3, the clean control, derive_check re-runs,
   README/log and the push waves. NO measurement, generation or freeze step
   was redone; the frozen bytes are the owner lane's 4-run battery.
2. One environment reset occurred during the takeover T3 audit's first
   invocation; the checkpoint pkl survived on the persistent mount and the
   audit resumed from it. The clean control (a full independent third audit)
   and audit1/2 byte-identity bracket the resumed runs.
3. T2's audit resumed from the owner lane's own checkpoint state (its last
   action before silence was starting the T2 audit); the state machine is
   deterministic and the tampered T2 file was byte-verified (single-field
   value flip) before auditing. The result equals a fresh T2 audit by
   determinism; the disclosed resume is provenance, not a shortcut.
4. The frozen kit-18 one-past prediction texts omit the one-past stack
   lists (birth texts carry them); the measured one-past shadow sets exactly
   match standing rule-v2 admissible co-splits (m19:12, m20:11, m21:7,
   m22:6, m23:5, m24:4, m25:3, m26:2, m27..32:0) with no other unregistered
   separation. Text-completeness property, disclosed as such; kit-19x
   reported the same measurement-side facts from the same texts.
5. Hand-typed pins forbidden: every pin in this log was machine-extracted
   from the frozen files.
6. All published files are pure ASCII (byte scan before push).
