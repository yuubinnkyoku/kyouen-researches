# n11 ultra-cheap one-unknown candidates: legal/geometry pre-check (2026-11-27)

Companion instrument to the published ultra-cheap class-completion
census (`n11-ultra-cheap-class-census-20261127`, run json sha256
`a60716ac...`): that census left `legal` null for the four
one-unknown S5 keys (none of them is in the probe-13 supply). This
kit derives, by TWO independent implementations, the per-key geometry
facts a future selection Part needs, so the next selection does not
have to re-derive them:

- stones == 5
- D4-canonical (canonical(mask) == mask)
- quadruple-free / safe (is_canonical_safe_s5_key)
- the legal-move count of the position (the `legal` field of a
  selection json / input CSV row)

## Implementations

- **A**: the repo's published standalone geometry
  `research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py`
  (sha256 `954d3a10...`, copied byte-exact into `in/`), Board(11)
  integer two-perpendicular-bisector completion, blocked-set legal.
- **B**: written fresh for this kit (`scripts/ultra_cheap_legal.py`):
  a square q is illegal iff some occupied triple is collinear-with-q
  or concyclic-with-q, tested by the exact integer 4x4 determinant
  criterion; D4 canonicalization by explicit point remapping. A
  genuinely different formulation from A.

## Calibration (the trust anchor)

BOTH implementations first reproduce the published probe-13 supply
(`in/shared-s5-tasks.csv`, sha256 `31f0d29b...`, 4,562 rows) exactly:
impl A matches all 4,562 published `legal` values, impl B matches all
4,562, and A == B on all 4,562, before any candidate key is derived.

## Result (PASS, rc=0, 3 runs byte-identical, 25 gates, 5/5 fail-closed tampers)

| class_index | unknown S5 key | legal | stones | D4 | safe |
|---|---|---|---|---|---|
| 1849 | 1153485622925590528:0 | 88 | 5 | yes | yes |
| 2251 | 1297036830121656320:131074 | 80 | 5 | yes | yes |
| 16371 | 1153202979851993088:272 | 78 | 5 | yes | yes |
| 23101 | 1152921505747697664:1032 | 85 | 5 | yes | yes |

Run json sha256 (3 runs byte-identical):
`89fd85ac8255a235b8557a35d7cfb229f8173ea940a6174c1e405d2f245afd73`.

## Tamper battery (5/5 fail-closed; clean control re-PASS byte-identical)

- T1 census run json candidate key flip -> P0c census-run-sha pin
  (plus the fresh-key gates), rc=1
- T2 supply `legal` value edit -> P1b/P1c supply-calibration gates, rc=1
- T3 appended byte to `in/independent.py` -> P0a independent-sha pin, rc=1
- T4 candidate replaced by a 2-stone key -> P0c pin AND P3a stones /
  P3c safe / P3d agreement gates, rc=1
- T5 impl-B concyclic predicate inverted -> caught by the P1c supply
  calibration gate (4,562-row semantic detector), rc=1

## Honest disclosures

- The first clean attempt failed its own P1a gate: the EXPECTED row
  count constant was initially set to 4,556 from a misread of the CSV
  line count; the machine-observed count is 4,562 rows (the CSV has
  4,563 lines including header) and the constant was corrected before
  any PASS was recorded.
- The supply sha pin (`31f0d29b...`) was added together with that
  fix, so the row-count gate failure also demonstrated the kit does
  not trust the local copy blindly.
- The first tamper-battery attempt ran in `/tmp` and failed for an
  environmental reason (`s5_evidence_policy.py` resolves
  `parents[4]` at import time, which does not exist at shallow
  paths); the battery was re-run at a sufficient directory depth and
  that constraint is a property of the repo script, not a kit defect.
- `s5_evidence_policy.ROOT` is unused here (only
  `is_canonical_safe_s5_key`, a pure function, is imported); the
  quarantine registry itself was already checked by the census kit.

## Meaning and non-meaning

Geometry/legality bookkeeping for scheduling only. NO verdict is
claimed or consumed, no key is probed, and resolving any of these
keys still requires the standing cold-pair + C++ second-implementation
+ third-implementation corroboration pillars under a single-owner
selection declaration. Nodes and proxy values are never evidence of
WIN or LOSS. The standard 11x11 empty board: UNKNOWN. All 19
central-reply roots: UNKNOWN. The two-stone root {60,27} and its
remaining third moves 100/108: UNKNOWN.

This lane runs without access to the user's computer (scheduled
task); publication via GitHub API only, verified by raw CDN
fetch-back.
