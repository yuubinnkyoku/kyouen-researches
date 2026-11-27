# Completion log: n11 ultra-cheap candidates legal/geometry pre-check (2026-11-27, long lane)

Part type: measurement/geometry pre-check (scheduling input only). NO
verdict consumed, NO probe executed, NO branch created. Standard 11x11
empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone
root {60,27} and third moves 100/108: UNKNOWN.

## What was produced

- `research/experiments/n11-ultra-cheap-legal-precheck-20261127/` —
  `scripts/ultra_cheap_legal.py` with TWO independent geometry
  implementations (repo standalone `independent.py` Board vs a fresh
  integer 4x4-determinant concyclicity formulation), calibrated
  against all 4,562 published probe-13 supply `legal` values
  (A exact / B exact / A==B), then applied to the 4 one-unknown
  ultra-cheap candidate S5 keys of the published census:
  - class 1849  / `1153485622925590528:0` — legal 88
  - class 2251  / `1297036830121656320:131074` — legal 80
  - class 16371 / `1153202979851993088:272` — legal 78
  - class 23101 / `1152921505747697664:1032` — legal 85
  All four: stones 5, D4-canonical, quadruple-free safe, and the two
  implementations agree on every legal count.
- 3 cold passes byte-identical (run json sha256 `89fd85ac...`), 25
  gates, 5/5 fail-closed tamper battery (census-run pin, supply legal
  calibration, independent.py pin, stones/safe gates, impl-B
  predicate inversion), clean control re-PASS byte-identical.

## Why this matters

The census left `legal` null for the 4 candidates; this kit closes
that gap with dual-implementation evidence, so the next selection
Part can write its input CSVs / selection json rows for any of these
keys without re-deriving geometry, and the calibration anchors both
implementations to 4,562 published values.

## Concurrency state

Published on top of HEAD `a06352d169` (the ultra-cheap census kit of
the same lane). The twelfth-cost wave-B raws of declaration
`f6d29d16` were STILL absent at publication time (checked via the
GitHub contents API), so the pre-audit kit's Stage B remains
pre-registered and unexecuted. No ownership conflict: this kit
probes nothing and claims no key.

## Access note

This lane runs without access to the user's computer (scheduled task
without the desktop app); publication via GitHub API only, verified
by raw CDN fetch-back.
# Addendum: publication integrity note for the ultra-cheap legal-precheck kit

During fetch-back verification of
`research/experiments/n11-ultra-cheap-legal-precheck-20261127/`, the
kit's `in/shared-s5-tasks.csv` (552,371B) was initially published
TRUNCATED at 63,922B: the publishing path read the file in a single
non-chunked pass and the read boundary cut the file (same failure
class as the 2026-11-27 `sweep-anomalies-raw.txt` 344B-short incident
repaired in commit b874536e8b by a parallel lane). Detected by the
byte-compare fetch-back gate.

Repair: republished the complete file in a second commit with the
read performed in offset-continuation chunks (all 552,371 chars
pushed). Verification of the repaired remote copy, since the raw CDN
edge serving this lane kept returning the stale truncated copy even
after cache-busting attempts: the GitHub contents API reports the
remote git blob sha `98866f47fd9cbd0d243dd88db8e509b1dd9c55b4`, which
is exactly the git blob sha of the local complete file
(sha256 `31f0d29b...`, 4,562 data rows), so the remote copy is
byte-exact and consistent with the kit MANIFEST.

All other 13 kit files and the completion log verified byte-identical
by raw CDN fetch-back on the first pass. No output, script, or gate
content was affected; the census run json and all PASS evidence are
untouched. Verdict NOT consumed, no key probed: standard 11x11 empty
board UNKNOWN, all 19 central-reply roots UNKNOWN, two-stone root
{60,27} and third moves 100/108 UNKNOWN.
