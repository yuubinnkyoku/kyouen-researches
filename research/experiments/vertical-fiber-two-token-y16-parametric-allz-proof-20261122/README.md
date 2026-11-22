# Vertical fiber: two-token y=16 parametric family, all-z universal verifier (part 1 + part 2)

Experiment dir: `vertical-fiber-two-token-y16-parametric-allz-proof-20261122`
Family: `H(R;(x,16);z)`, all `z >= 0`, all `x >= 16`, all `R >= 0`.
Claim under audit: K1237 (`cand16`, published fit, status **observed**
at part-1 time, **promoted proved by part 2**) equals `H` everywhere,
with corollaries

- merge below the diagonal: `x <= z-17  =>  H == single_token(x+16,z,R)` (K0832),
- tail: `R >= x+z+17  =>  H == (x+16) % 2`.

Single-owner declaration note:
[2026-11-22-y16-universal-verifier-single-owner-note.md](../../log/2026-11-22-y16-universal-verifier-single-owner-note.md)
(commit `432664f7`, observed HEAD `76abc080`, counter-declaration grep clean),
published BEFORE the verifier run. Scope: part 1 (12 checks, this
publication) + part 2 (C1d published-slice anchors + census_rows.py third
implementation + C11r), which promotes K1237 observed -> proved on overall
PASS. Part 2 was NOT claimed at part-1 time; the promotion was published
as a separate commit of this dir (same procedure as the y=10/y=12/y=13/
y=14/y=15 part-2 stages).

## Machine composition (verify_y16_universal.py)

Assembled by `scripts/build_verify_y16.py` (SHA-256 `928b8741...`) from the
pinned source bytes shipped in this dir:

- `published_verify_y15_universal.py` (SHA-256 `a39e7ab1...`, the published
  y=15 proof part2 canonical edition, commit `0bf18752`):
  - raw engines `H_ordered` / `H_canonical` + K0832 `single_token` block,
    verbatim (provenance chain K1138/K1141/K1143/K1152/K1231/K1233 unchanged);
  - the `cand15` block (the B-child of every y=16 point and the x=16 merger
    child value), verbatim with a block-local `Y -> Y15` rename (102 block
    lines, byte-compared against the published block modulo the rename);
    its universal proof is K1235; its y=16-scope usage (x >= 16 rows) is
    inside its published universal domain (x >= 15, all z, all R);
  - the check battery, adapted to the y=16 family constants (see below);
- `published_cand16.py` (SHA-256 `1fc9d22b...`, the published K1237 fit
  experiment, commit `33e1c22e`): the `cand16` block verbatim (92 lines,
  byte-compared), fit driver omitted.

Builder regeneration is count-asserted per substitution and byte-identical
across repeated runs (`verify_y16_universal.py` 37,042 bytes, SHA-256
`79e21b2d...`).

**Part 2 extends this part-1 byte in place** (C1d anchor block + the
check_C1d/check_C11r bodies added; the 12 part-1 check bodies
byte-unchanged; the builder script builds the part-1 byte only - no
part-2 assembly script is published, the y=13/y=14/y=15 part-2
procedure). Part-2 edition: 51,691 bytes, SHA-256 `bdf4fe04...`.

Machine swaps relative to the published y=15 machine: merger row x==16 with
A-child `cand15(z,16,R-1)` (multiset (15,16)==(16,15), the y=15 family x=16
row), B-child `cand15(z,x,R-1)`, C-child `1 xor cand16(z-1,x,R-1)`; clip
window `2y+2 = 34` / sentinel 35; census box `z=0..79, x=16..70, R<=x+z+17`
(80*55 = 4,400 rows, 442,200 points per engine); merge `x<=z-17`; tail
`(x+16)%2` at `R >= x+z+17`; C12 deep grid `R<=x+z+18`; C8 keeps the
x=15 rows as closed-form extension-consistency rows only (no raw claim
below x=16), exactly as the x=14 rows did in the y=15 machine; C7 seed
20261162 (the y=14 seed 20261142 / y=15 seed 20261152 series).

## Part 1 results (overall PASS, 3 byte-identical runs)

12 checks (C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12):
total comparison points **6,331,848**, total bad **0**, types **394,686**
(C4-time 309,141). Per-check: C1 22,800 / C1b 41,834 / C2 217,021 /
C2b 19,316 / C3 1,245 / C4 595,990 / C4t 595,990 (probe, not in bad) /
C7 200,000 / C8 992,652 / C9 905,670 / C11 884,400 / C12 1,854,930.

Corollaries: merge `x<=z-17 => H == single_token(x+16,z,R)` at 1,243,466
points bad 0 (first full raw-engine anchoring of the y=16 merge region,
which the fit probe box could not contain - the y=16 box is the first with
zero in-box merge rows, per the fit declaration); tail
`R>=x+z+17 => H == (x+16)%2` at 193,300 points bad 0.

C4t tightness probe: clip 33 (2y+1) has **1,638 confluence violations,
first (60,96,96)** - so the clip window `2y+2 = 34` is **tight**, the 12th
consecutive family (y=5..16: 12/14/16/18/20/22/24/26/28/30/32/34),
continuing the pattern that the first violation walks with the band bottom
(y=13: clip 27 (60,90,90); y=14: clip 29 (60,92,92); y=15: clip 31
(60,94,94); y=16: clip 33 (60,96,96)).

Type count: 394,686 types (y=13 clip 28: 234,180 -> y=14 clip 30: 281,912
-> y=15 clip 32: 335,658 -> y=16 clip 34: 394,686).

## C11 census: bounded-memoization twins

Box `z=0..79, x=16..70, R<=x+z+17`: 442,200 points per engine (55 x-rows
per z; the y=15 box had 56). Design is the published y=12/y=13/y=14/y=15
part1 design: the published engine's code object re-bound into a shallow
copy of the module globals with the recursive name resolving to an
LRU-capped cache (cap 1,600,000); engine-per-command (C11ordered 18.1 s /
C11canonical 19.5 s, run 1); the C11 mode validates both parts fail-closed
against recomputed expected counts (442,200 / merge 127,464 / tail 4,400
per engine) and merges them.

Host note: this execution host is more memory-capped than the y=15 host
(an unbounded raw-engine scan over z=40..79, R<=x+z+17 was OOM-killed;
the y=15 host completed the same shape of scan unbounded). All published
raw-engine anchors on this host therefore use the bounded twins; the
unbounded verbatim engines anchor C1/C1b/C3 on their small boxes.

## Honest incident record (fail-closed worked as designed)

The first C11ordered execution before any publication compared the census
against the family-15 tuple `(x, 15)` (a run_census tail literal missed
by the builder renames): 442,200 pts, bad 147,972, and the census self-
reported FAIL (rc=1). Diagnosed (the bad set matched the y=15 family bias),
fixed with a count-asserted substitution in the builder, machine
regenerated byte-deterministically, census re-run clean (bad 0 both
engines). No bad-census byte was published; the incident is recorded in
`output/published_run.txt` and here. Compare: the y=10 pre-flight of the
same transcription chain caught a K1087 first-draft evaluation-order bug
(170 mismatches) - raw anchoring catches exactly this class of slip.

## Determinism and fail-closed

`output/audit.json` (SHA-256 `7b5acc8c...`), `output/census-ordered.json`
(`fd94dda3...`), `output/census-canonical.json` (`3934307f...`): 3
executions byte-identical - two same-cwd runs plus one isolated
tree/cwd/HOME run with `PYTHONHASHSEED=random` (census parts regenerated
on the isolated side, byte-identical). Fail-closed exercised and caught
before publication: (1) census part points tamper 442,200 -> 442,201
(FAIL-CLOSED), (2) census part missing (FAIL-CLOSED), (3) census
merge-corollary bad tamper (FAIL-CLOSED), (4) census part box field
tamper (FAIL-CLOSED), (5a) `Y` constant tamper 16 -> 17 in the cand16
block (C1: 903 bad, FAIL), (5b) block-local `Y15` tamper 15 -> 16 in the
B-child (C1b: 777 bad, FAIL). Baseline restored and byte-confirmed after
every case; at part-1 publication time the canonical 12-check audit.json
was the last full run (superseded by the part-2 14-check audit of
record).
The audit.json is overwritten by whichever check run wrote it last; the
canonical audit is re-established by the explicit check list (as
`output/published_run.txt` records).

## Part 2: C1d published-slice anchors + census_rows.py consumer (2026-11-22 added; promotes K1237 observed -> proved)

The promotion stage left open by part 1, executed with the same procedure
that promoted the y=10/y=12/y=13/y=14/y=15 machines
(K1141/K1152/K1231/K1233/K1235). The C1d anchor block (anchor functions
A8u..A17u) is the published y=15 part-2 canonical verifier's anchor block
**verbatim** (its universal proof domain covers the y=16 rows reached
here), with only the provenance header rewritten from the y=16 preflight
measurements (13,140/9,504, cand16). The single textual "y=14/y=15"
remnants outside provenance naming are deliberate: the comment citing the
y=10/y=12/y=13/y=14/y=15 part-2 C1d precedent.

### C1d (published fixed-z slice anchors at the y=16 rows: 137,808 points, bad 0)

`scripts/preflight_c1d_y16.py` (SHA-256 `6a3094c1...`, generated from the
published y=15 preflight with count-asserted y=16 scan constants)
fail-closed pre-verification BEFORE the machine body ran: the published
uniform closed forms (z=8: K0999/K1000, z=9: K1001, z=10: K1011,
z=15/16/17: K1065/K1077/K1087) 4-way checked
(anchor x H_ordered x H_canonical x cand16) on z0 in {8,9,10,15,16,17},
x=16..45, R=1..x+z0+30: **13,140 points bad 0** (per z: 2,055 / 2,085 /
2,115 / 2,265 / 2,295 / 2,325), plus the published low-R single-token
reduction R<=z+6 on the z0=15/16/17 y=16 rows
(cand16 vs single_token(x+16,z0,R)): **9,504 points bad 0**; wall ~3 s;
2 runs byte-identical (one on the isolated side);
`output/preflight-c1d-y16.json` (SHA-256 `efb24340...`; the file is the
pretty-printed canonical byte, stdout is the same JSON compacted).
The y=10 precedent (this stage caught a 170-point evaluation-order bug in
the first K1087 transcription) is why this stage exists; here the anchors
are a verbatim re-transcription, and the 4-way check agreed on the first
run. Machine C1d then sweeps 6 z0 x x=16..159 x R=1..x+61 (**128,304
points**) plus the lowR rows (9,504): total **137,808, bad 0**.

### C11r (independent census ledger consumer: 446,600 points, bad 0, fail-closed)

`census_rows.py` (the third implementation; y=16 edition, SHA-256
`76e89fe9...`) writes `output/census.txt` (817,944 bytes, 4,400 rows + 80
blank separators, SHA-256 `f0b1a960...`): z=0..79, x=16..70, per-row
Thue-Morse index, value-2 support T, value-1 support P (explicit R lists)
and tail flag: **446,600 points**, zero-value points 223,295, engine states
(LRU misses) 8,193,227, LRU cap 1,600,000 explicit (the memory-capped-host
adaptation, mirroring the published y=12..y=15 editions on the same
class of host); the tail assert `R>=x+z+17 => (x+16)%2` held on every
row. Wall ~20 s. C11r re-derives every row from cand16 and compares idx/
T/P/tail (duplicate or missing rows, rows != 80*55 = 4,400, missing
trailing newline are FAIL-CLOSED): 446,600 points **bad 0**.

### Part-2 full audit (14 checks, overall PASS, total_points 6,916,256, bad 0)

C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12 in one command: C1d
137,808 and C11r 446,600 added to part 1's 6,331,848:
total_points **6,916,256**, total_bad **0**, types **394,686**. Merge
corollary 1,243,466 and tail 193,300 unchanged, bad 0. C4t consistent
with part 1 (1,638 violations at clip 33, first (60,96,96)). Wall 35.5 s
(run 1) / 36.0 s (run 2) / 36.0 s (isolated run 3); the C11ordered/
C11canonical parts rerun in the part-2 session reproduce the part-1
published bytes. `output/audit.json` (part-2 stage wording, SHA-256
`9748ff5c...`) is the canonical audit of record.

### Part-2 determinism (3 runs byte-identical) and fail-closed (6 probes)

run1 (same cwd) -> run2 (same-cwd rerun) -> run3 (isolated tree/cwd/HOME +
`env -i` with pinned PATH + `PYTHONHASHSEED=random`, preflight,
census_rows.py and BOTH census parts regenerated on the isolated side):
audit.json, census.txt, census-ordered.json, census-canonical.json,
preflight-c1d-y16.json all byte-identical; census.txt byte-identical
across 3 census_rows.py runs (2 main-tree + 1 isolated).

Fail-closed exercised on a scratch tree, all caught before publication:
(1) census part points tamper 442,200 -> 442,201 (FAIL-CLOSED), (2) census
canonical part missing (FAIL-CLOSED), (3) corollary merge bound tamper
x<=z-17 -> x<=z-16 (fake C2 on a tampered verifier copy: merge bad 200,
overall FAIL, rc=1), (4) census.txt P-set one-digit tamper (C11r bad 1,
FAIL, no PASS output), (5) census.txt missing (FAIL-CLOSED), (6)
census.txt duplicate-row injection (FAIL-CLOSED "duplicate census row").
Baseline bytes restored and cmp'd clean after every probe; the main-tree
audit.json was never touched by the probes.

### Promotion decision

With the full 14-check audit PASS, the fail-closed pre-verified C1d
anchors, the independent third-implementation census (C11r), and three
byte-identical audit runs, **K1237 is promoted observed -> proved**
(same K item, no new numbering, the K1023/K1233/K1235 part1/part2
precedent). The corollaries are fixed as universal claims in the same
scope: the merge proposition's y=16 edition `x<=z-17 => H ==
single_token(x+16,z,R)` and the tail value `R>=x+z+17 => H == (x+16)%2`,
so the merge proposition now holds universally through y=1..16. The
B-child of the y=16 family is the verbatim cand15 (K1235, proved),
extending the B-child verbatim chain to cand9..cand15 (seven links) and
the proved-B-child usage to cand10/cand12..cand15 (five links).

## Reproduction

```sh
python3 scripts/build_verify_y16.py     # regenerates the part-1 machine byte
                                        # (the part-2 edition is the part-1 byte
                                        #  extended in place; no part-2 assembly
                                        #  script is published - the y=13/y=14/
                                        #  y=15 part-2 procedure)
python3 scripts/preflight_c1d_y16.py    # fail-closed pre-flight of the anchors
python3 census_rows.py                  # third-implementation census ledger
python3 verify_y16_universal.py C11ordered
python3 verify_y16_universal.py C11canonical
python3 verify_y16_universal.py C1 C1b C1d C2 C2b C3 C4 C4t C7 C8 C9 C11 C11r C12
```

Note: `output/audit.json` is overwritten by whichever check run wrote it
last; the canonical audit is re-established by the explicit full check
list (as `output/published_run.txt` records).

## Interpretation

Parts 1 + 2 are finite machine evidence for the universal claim K1237,
of the same machine class as the y=5..y=15 promotion machines (option
decomposition + closed-form mex identity + finite-type confluence,
anchored to raw engines, to the proved y=15 family B-child, to the
x=16 multiset merger, and (C1d) to the published z=8/9/10/15/16/17
slice closed forms). Part 2 (fail-closed pre-flighted C1d anchors +
census_rows.py third-implementation ledger consumed by C11r) completed
the two-part procedure, and **K1237 is promoted observed -> proved**
under the single-owner declaration's scope (same procedure as
K1141/K1152/K1231/K1233/K1235). Finite checks remain finite evidence
under this machine class: the trust boundary is the finite-type
confluence box, not an abstract proof; comparison points are comparison
counts, never verdicts about the standard 11x11 game; the 11x11 empty
board, the two-stone roots {49,60}/{59,60}, S2 {59,60} and classes
1/2/4 remain UNKNOWN and untouched by this experiment.
