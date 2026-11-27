# n11 Part SY declaration: seventh-cost full-batch third-implementation corroboration (wave A)

Single-owner declaration, publish-then-execute. HEAD at declaration:
08013decb833c14fbf8c7bbc1c97fb32c4682d99 (Part SX wave F completion log;
counter-probe clean at this HEAD: no seventh-cost third-impl kit,
declaration or note of any kind exists on main for these rows - the SW
and SX kit gate-rows.json both pin third_impl as "exists: false ... a
separate future Part", and that Part is declared here).

Scope: the pinned third implementation third_impl.js (sha256
08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998,
byte-equal re-publication provenance of the ea73c3e3 publication,
byte-verified on this host against the pinned sixth-cost third-impl kit
copy) corroborates ALL 42 published seventh-cost rows:

- the 41 LOSS rows k01..k42 minus k05 (published Node replica cold
  pairs, 39 rows resolved at the 15M stage, k16/k17 at the 2M stage;
  Part SW C++ gate 44/44 GATE-PASS), and
- the single WIN row k05 1152921504607932416:536870912 (published
  at50m cold pair WIN(1) ff750cc6 x2, Part SX C++ gate 4/4 GATE-PASS).

Pre-registered protocol:
- C1 calibration on this fresh host first, HARD-STOP on any failure:
  C1a verify_tbl.js gate (sha256 c8c52528..., replica dependency
  jsreplay.js sha256 84585617... at its pinned path, byte-verified),
  C1b two published sixth-cost calibration anchors re-run fresh:
  k06 10376293541462675456:65536 legal 89, expected third_impl
  LOSS(2) expansions 9,474,431 (published k06-cold-a raw), and
  k38 10376293541461626880:66048 legal 100, expected third_impl
  LOSS(2) expansions 25,898,941 (Part SU publication).
- Then 42 targets, two fresh-cold passes each (one node process per
  pass, serial), invocation pinned:
  node third_impl.js --lo=<lo> --hi=<hi> --stones=5 --legal=<legal>
  --row=<kNN>.pN --cap=400000000 --wallcap=260 --memo-power=22
- Expected verdicts machine-derived from the published SW/SX kit
  gate-rows.json expected quadruples (41x result 2, k05 result 1); the
  third-impl expansion counts are compared ONLY across the third
  implementation's own cold pairs (never against replica node counts -
  the implementations count different quantities, sixth-cost precedent).
- HARD-STOP on any result disagreement, cold-pair expansion
  disagreement, GATE_FAIL, crash or truncation; raw partial state
  recorded and disclosed, truncated artifacts re-run never trusted.
- Input pins: the SW/SX kit input CSVs (k05 input sha256 a73a6c70... ==
  the published seventh-cost kit MANIFEST pin; per-row input sha256
  pins carried from the SW/SX gate-rows.json and re-verified in the
  maker).
- Fresh fail-closed audit implementation (not a byte transform of any
  previous audit), maker with 2-run byte-identical output requirement,
  3-mode tamper battery on a scratch copy after the official passes,
  never on the published bytes.

Honest environment disclosure: this executing session is the same
upgraded sandbox session that closed Part SW and Part SX earlier in this
window (native Node.js v22.20.0, Python 3.12); no target pass runs
before this wave A declaration and the wave B kit publication. The
third implementation is the SAME third_impl.js implementation pinned in
the sixth-cost corroboration program (a fresh host, not a fresh
implementation - disclosed; it is the program's standing third
implementation, per the k06/k07/k08 host-honesty precedent).

Meaning and non-meaning: this Part is scheduling and verification only.
NO verdict is consumed, no cache increment, no class-status change. A
verdict-level agreement row is bookkeeping toward adoption eligibility
only (k13/k19/k20/k33/k38 precedent: third-impl corroboration is the
prerequisite the adoption Part checks); adoption itself stays with a
separately declared adoption Part under the parent batch's WIN/LOSS
conflict policy against the canonical head of record 42dbb58f (6,832
rows WIN 201 / LOSS 6,631), which this Part does not touch.

Status guard: the standard 11x11 empty board is UNKNOWN. All 19
central-reply roots are UNKNOWN. The two-stone root {60,27} is UNKNOWN.
Its remaining third moves {100,108} are UNKNOWN. S2 and closure classes
1/2/4 and all closure classes are UNKNOWN. A WIN(1) or LOSS(2) S5 raw is
not a class closure claim, not a root verdict, and transfers nothing.
Nodes and expansions are bookkeeping, never verdicts.
