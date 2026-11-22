# Vertical fiber: two-token y=15 parametric family, all-z universal verifier (part 1)

Experiment dir: `vertical-fiber-two-token-y15-parametric-allz-proof-20261122`
Family: `H(R;(x,15);z)`, all `z >= 0`, all `x >= 15`, all `R >= 0`.
Claim under audit: K1235 (`cand15`, published fit, status **observed** at part 1
time) equals `H` everywhere, with corollaries

- merge below the diagonal: `x <= z-16  =>  H == single_token(x+15,z,R)` (K0832),
- tail: `R >= x+z+16  =>  H == (x+15) % 2`.

Single-owner declaration note:
[2026-11-22-y15-universal-verifier-single-owner-note.md](../../log/2026-11-22-y15-universal-verifier-single-owner-note.md)
(commit `c34a19ff`, observed HEAD `bcc761b8`, counter-declaration grep clean),
published BEFORE the verifier run. Scope: part 1 (12 checks) + part 2
(C1d published-slice anchors + census_rows.py third implementation + C11r)
which promotes K1235 observed -> proved on overall PASS. Part 2 is NOT in
this part-1 publication; the promotion is NOT claimed here.

## Machine composition (verify_y15_universal.py)

Assembled by `scripts/build_verify_y15.py` (SHA-256 `034683a4...`) from the
pinned source bytes shipped in this dir:

- `published_verify_y14_universal.py` (SHA-256 `6ac219cf...`, the published
  y=14 proof part2 canonical edition, commit `7026c860`):
  - raw engines `H_ordered` / `H_canonical` + K0832 `single_token` block,
    verbatim (provenance chain K1138/K1141/K1143/K1152/K1231 unchanged);
  - the `cand14` block (the B-child of every y=15 point and the x=15 merger
    child value), verbatim with a block-local `Y -> Y14` rename
    (24 rename sites, count-asserted in the builder); its universal proof is
    K1233; its y=15-scope usage (x >= 15 rows) is inside its published
    universal domain (x >= 14, all z, all R);
- `published_cand15.py` (SHA-256 `f61997dd...`, the published K1235 fit
  experiment, commit `8222f6f6`): the `cand15` block verbatim, fit driver
  omitted.

Machine swaps relative to the published y=14 machine: merger row x==15 with
A-child `cand14(z,15,R-1)` (multiset (14,15)==(15,14), the y=14 family x=15
row), B-child `cand14(z,x,R-1)`, C-child `1 xor cand15(z-1,x,R-1)`; clip
window `2y+2 = 32` / sentinel 33; census box `z=0..79, x=15..70, R<=x+z+16`
(80*56 = 4,480 rows, 443,520 points per engine); merge `x<=z-16`; tail
`(x+15)%2` at `R >= x+z+16`; C12 deep grid `R<=x+z+17`. Pre-run smoke
anchors (published_run.txt): raw-engines-vs-cand15 small box (2,016 pts),
merger child raw (808 pts), y=14 B-child raw (8,580 pts), raw options vs
closed options (3,060 pts), merge rows raw (3,960 pts, z=31..40), tail rows
raw (4,030 pts) - all 0 mismatches, before the full machine ran.

## Part 1 results (overall PASS, 3 byte-identical runs)

12 checks (C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12):
total comparison points **6,349,309**, total bad **0**, types **335,658**
(C4-time 279,619). Per-check: C1 22,515 / C1b 43,228 / C2 218,834 /
C2b 19,228 / C3 1,215 / C4 601,255 / C4t 601,255 (probe, not in bad) /
C7 200,000 / C8 993,180 / C9 908,202 / C11 887,040 / C12 1,853,357.

Corollaries: merge `x<=z-16 => H == single_token(x+15,z,R)` at 1,304,870
points bad 0 (first full raw-engine anchoring of the y=15 merge region, which
the fit probe box could not contain); tail `R>=x+z+16 => H == (x+15)%2` at
195,917 points bad 0.

C4t tightness probe: clip 31 (2y+1) has **2,030 confluence violations,
first (60,94,94)** - so the clip window `2y+2 = 32` is **tight**, the 11th
consecutive family (y=5..15: 12/14/16/18/20/22/24/26/28/30/32), continuing
the pattern that the first violation walks with the band bottom
(y=13: clip 27 ' (60,90,90); y=14: clip 29 ' (60,92,92); y=15: clip 31 '
(60,94,94)).

## C11 census: bounded-memoization twins

Box `z=0..79, x=15..70, R<=x+z+16`: 443,520 points per engine. Design is the
published y=12/y=13/y=14 part1 design: the published engine's code object
re-bound into a shallow copy of the module globals with the recursive name
resolving to an LRU-capped cache (cap 1,600,000); engine-per-command
(C11ordered 15 s / C11canonical 19 s, run 1); the C11 mode validates both
parts fail-closed against recomputed expected counts
(443,520 / merge 135,975 / tail 4,480 per engine) and merges them.

## Determinism and fail-closed

`audit.json` (SHA-256 `9f12d6e7...`), `census-ordered.json`
(`50819ab3...`), `census-canonical.json` (`64b006a3...`): 3 executions
byte-identical - two same-cwd runs plus one isolated tree/cwd/HOME run with
`PYTHONHASHSEED=random` (census parts regenerated on the isolated side,
byte-identical). Fail-closed exercised and caught before publication:
(1) census part points tamper 443,520 -> 443,521 (FAIL-CLOSED),
(2) census part missing (FAIL-CLOSED), (3) corollary merge bound tamper
x<=z-16 -> x<=z-15 (overall FAIL, total_bad 223), baseline restored and
byte-confirmed. The audit.json is overwritten by whichever check run wrote
it last: the canonical 12-check audit is re-established by running the
explicit check list (as published_run.txt records).

## Interpretation conventions

- K1235's status at part-1 publication time stays **observed**. The
  observed -> proved promotion decision is part 2's (C1d published
  fixed-z slice anchors z=8/9/10/15/16/17 at the y=15 rows, preflighted
  fail-closed, + census_rows.py third implementation + C11r; same procedure
  that promoted K1023.../K1233 through their part1/part2 machines).
- x=14 rows inside the C8 identity sweep are closed-form
  extension-consistency rows (no raw claim below x=15), exactly as the
  x=13 rows in the published y=14 machine and the x=12 rows in the
  published y=13 machine; they contributed 0 bad.
- Finite sweeps are finite machine evidence; the trust boundary (option
  decomposition soundness, mex identity, finite type-space completeness) is
  the same machine classification as the y=5..y=14 series.
- The standard 11x11 empty board / two-stone roots {49,60}/{59,60} / S2
  {59,60} / classes 1/2/4 are all UNKNOWN and untouched. Three or more
  tokens, y>=16 families, fixed-width, q-point stabilization lengths are
  out of scope.
- knowledge.yml CI registration is not added for this experiment (the
  current main has no CI step for the y=11/y=12/y=13/y=14 machines either;
  CI registration stopped at y=10/K1141): the published bytes are the audit
  canonical.

## Files

- `verify_y15_universal.py` - the part-1 canonical verifier (942 lines,
  SHA-256 `583252cc...`)
- `scripts/build_verify_y15.py` - the assembler (marker-bounded extraction,
  rename count-asserts, forbidden/required token gates)
- `published_verify_y14_universal.py`, `published_cand15.py` - the pinned
  source bytes the builder consumes
- `output/audit.json` - the 12-check canonical audit
- `output/census-ordered.json`, `output/census-canonical.json` - C11 parts
- `output/published_run.txt` - full run record (smoke spots, 3 runs,
  fail-closed, timings, environment)
