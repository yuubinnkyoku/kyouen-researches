# Vertical fiber: two-token y=15 parametric family, all-z universal verifier (part 1 + part 2)

Experiment dir: `vertical-fiber-two-token-y15-parametric-allz-proof-20261122`
Family: `H(R;(x,15);z)`, all `z >= 0`, all `x >= 15`, all `R >= 0`.
Claim under audit: K1235 (`cand15`, published fit, status **observed** at
part 1 time, **promoted proved by part 2**) equals `H` everywhere, with
corollaries

- merge below the diagonal: `x <= z-16  =>  H == single_token(x+15,z,R)` (K0832),
- tail: `R >= x+z+16  =>  H == (x+15) % 2`.

Single-owner declaration note:
[2026-11-22-y15-universal-verifier-single-owner-note.md](../../log/2026-11-22-y15-universal-verifier-single-owner-note.md)
(commit `c34a19ff`, observed HEAD `bcc761b8`, counter-declaration grep clean),
published BEFORE the verifier run. Scope: part 1 (12 checks) + part 2
(C1d published-slice anchors + census_rows.py third implementation + C11r)
which promotes K1235 observed -> proved on overall PASS. Part 2 was NOT in
the part-1 publication; at part-2 publication (below) the promotion IS
claimed, under the same declared scope.

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

Part 2 extends this part-1 byte **in place** (C1d + C11r bodies added; the
12 part-1 check bodies byte-unchanged; no part-2 assembly script is
published, the y=13/y=14 part-2 procedure), producing the part-2 edition
`verify_y15_universal.py` (1,313 lines, SHA-256 `a39e7ab1...`) audited
below.

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

## Part 2: C1d published-slice anchors + census_rows.py consumer (2026-11-22 added; promotes K1235 observed -> proved)

The promotion stage left open by part 1, executed with the same procedure
that promoted the y=10/y=12/y=13/y=14 machines (K1141/K1152/K1231/K1233).
The C1d anchor block (anchor functions A8u..A17u) is the published y=14
part-2 canonical verifier's anchor block **verbatim** (its universal proof
domain covers the y=15 rows reached here), with only the provenance header
rewritten from the y=15 preflight measurements (count-asserted
substitutions: cand15, 13,485/9,570). The single textual "y=14" remnant
outside provenance naming is deliberate: the comment citing the
y=10/y=12/y=13/y=14 part-2 C1d precedent.

### C1d (published fixed-z slice anchors at the y=15 rows: 138,330 points, bad 0)

`scripts/preflight_c1d_y15.py` (SHA-256 `fdc4ca86...`, generated from the
published y=14 preflight with count-asserted y=15 scan constants)
fail-closed pre-verification BEFORE the machine body ran: the published
uniform closed forms (z=8: K0999/K1000, z=9: K1001, z=10: K1011,
z=15/16/17: K1065/K1077/K1087) 4-way checked
(anchor x H_ordered x H_canonical x cand15) on z0 in {8,9,10,15,16,17},
x=15..45, R=1..x+z0+30: **13,485 points bad 0** (per z: 2,108 / 2,139 /
2,170 / 2,325 / 2,356 / 2,387), plus the published low-R single-token
reduction R<=z+6 on the z0=15/16/17 y=15 rows
(cand15 vs single_token(x+15,z0,R)): **9,570 points bad 0**; wall ~3 s;
2 runs byte-identical (one on the isolated side);
`output/preflight-c1d-y15.json` (SHA-256 `cd67d3fe...`; the file is the
pretty-printed canonical byte, stdout is the same JSON compacted).
The y=10 precedent (this stage caught a 170-point evaluation-order bug in
the first K1087 transcription) is why this stage exists; here the anchors
are a verbatim re-transcription, and the 4-way check agreed on the first
run. Machine C1d then sweeps 6 z0 x x=15..159 x R=1..x+61 (**128,760
points**) plus the lowR rows (9,570): total **138,330, bad 0**.

### C11r (independent census ledger consumer: 448,000 points, bad 0, fail-closed)

`census_rows.py` (the third implementation; y=15 edition, SHA-256
`28e84955...`) writes `output/census.txt` (824,466 bytes, 4,480 rows + 80
blank separators, SHA-256 `1465a011...`): z=0..79, x=15..70, per-row
Thue-Morse index, value-2 support T, value-1 support P (explicit R lists)
and tail flag: **448,000 points**, zero-value points 223,127, engine states
(LRU misses) 7,666,827, LRU cap 1,600,000 explicit; the tail assert
`R>=x+z+16 => (x+15)%2` held on every row. Wall 15.7-16.3 s, maxrss
639,524 KB. C11r re-derives every row from cand15 and compares idx/T/P/
tail (duplicate or missing rows, rows != 80*56, missing trailing newline
are FAIL-CLOSED): 448,000 points **bad 0**.

### Part-2 full audit (14 checks, overall PASS, total_points 6,935,639, bad 0)

C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12 in one command: C1d
138,330 and C11r 448,000 added to part 1's 6,349,309:
total_points **6,935,639**, total_bad **0**, types **335,658**. Merge
corollary 1,304,870 and tail 195,917 unchanged, bad 0. Wall 34.8 s (run 1) /
34.3 s (run 2) / 34 s (isolated run 3), maxrss 473,520 KB; the C11ordered/
C11canonical parts rerun in the part-2 session reproduce the part-1
published bytes. `output/audit.json` (part-2 stage wording, SHA-256
`401be383...`).

### Part-2 determinism (3 runs byte-identical) and fail-closed (5 probes)

run1 (same cwd) -> run2 (same-cwd rerun) -> run3 (isolated tree/cwd/HOME +
`env -i` with pinned PATH + `PYTHONHASHSEED=random`, preflight,
census_rows.py and BOTH census parts regenerated on the isolated side):
audit.json, census.txt, census-ordered.json, census-canonical.json,
preflight-c1d-y15.json all byte-identical; census.txt byte-identical
across 3 census_rows.py runs.

Fail-closed exercised on a scratch tree, all caught before publication:
(1) census part points tamper 443,520 -> 443,521 (FAIL-CLOSED),
(2) census canonical part missing (FAIL-CLOSED), (3) corollary merge bound
tamper x<=z-16 -> x<=z-15 (overall FAIL, merge bad 223), (4) census.txt
P-set one-digit tamper (C11r bad 1, FAIL, no PASS output), (5) census.txt
missing (FAIL-CLOSED). Baseline bytes restored and cmp'd clean after
(1)(2)(4)(5); the main-tree audit.json was never touched by the probes.

### Promotion decision

With the full 14-check audit PASS, the fail-closed pre-verified C1d
anchors, the independent third-implementation census (C11r), and three
byte-identical audit runs, **K1235 is promoted observed -> proved**
(same K item, no new numbering, the K1023/K1233 part1/part2 precedent).
The corollaries are fixed as universal claims in the same scope: the merge
proposition's y=15 edition `x<=z-16 => H == single_token(x+15,z,R)` and the
tail value `R>=x+z+16 => H == (x+15) mod 2`, so the merge proposition now
holds universally through y=1..15. The B-child of the y=15 family is the
verbatim cand14 (K1233, proved), extending the B-child verbatim chain to
cand9..cand14 (six links) and the proved-B-child usage to
cand10/cand12/cand13/cand14 (four links).

## Interpretation conventions

- K1235's status at part-1 publication time stayed **observed**; part 2
  (C1d published fixed-z slice anchors z=8/9/10/15/16/17 at the y=15 rows,
  preflighted fail-closed, + census_rows.py third implementation + C11r;
  same procedure that promoted K1023.../K1233 through their part1/part2
  machines) executed that promotion: **K1235 is proved as of the part-2
  publication**, in the same K item.
- x=14 rows inside the C8 identity sweep are closed-form
  extension-consistency rows (no raw claim below x=15), exactly as the
  x=13 rows in the published y=14 machine and the x=12 rows in the
  published y=13 machine; they contributed 0 bad.
- Finite sweeps are finite machine evidence; the trust boundary (option
  decomposition soundness, mex identity, finite type-space completeness) is
  the same machine classification as the y=5..y=15 series.
- The standard 11x11 empty board / two-stone roots {49,60}/{59,60} / S2
  {59,60} / classes 1/2/4 are all UNKNOWN and untouched. Three or more
  tokens, y>=16 families, fixed-width, q-point stabilization lengths are
  out of scope.
- knowledge.yml CI registration is not added for this experiment (the
  current main has no CI step for the y=11/y=12/y=13/y=14 machines either;
  CI registration stopped at y=10/K1141): the published bytes are the audit
  canonical.

## Files

- `verify_y15_universal.py` - the part-2 canonical verifier (1,313 lines,
  SHA-256 `a39e7ab1...`; the byte published at part 1, 942 lines SHA-256
  `583252cc...`, is extended in place by part 2 with the 12 part-1 check
  bodies byte-unchanged)
- `scripts/build_verify_y15.py` - the part-1 assembler (marker-bounded
  extraction, rename count-asserts, forbidden/required token gates); not
  re-run in part 2 (in-place extension, the y=13/y=14 procedure)
- `scripts/preflight_c1d_y15.py` - the part-2 pre-verification
  (SHA-256 `fdc4ca86...`)
- `census_rows.py` - the third implementation, y=15 edition
  (SHA-256 `28e84955...`)
- `published_verify_y14_universal.py`, `published_cand15.py` - the pinned
  source bytes the builder consumes
- `output/audit.json` - the 14-check canonical part-2 audit
  (SHA-256 `401be383...`)
- `output/census-ordered.json`, `output/census-canonical.json` - C11 parts
  (unchanged from part 1)
- `output/census.txt` - the census ledger (SHA-256 `1465a011...`)
- `output/preflight-c1d-y15.json` (SHA-256 `cd67d3fe...`)
- `output/published_run.txt` - full run record (part 1: smoke spots, 3
  runs, fail-closed, timings, environment; part 2: preflight, census,
  14-check runs 1-3, fail-closed 5 probes, timings, file SHAs)
