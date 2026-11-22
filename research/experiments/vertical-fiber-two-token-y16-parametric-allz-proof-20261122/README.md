# Vertical fiber: two-token y=16 parametric family, all-z universal verifier (part 1)

Experiment dir: `vertical-fiber-two-token-y16-parametric-allz-proof-20261122`
Family: `H(R;(x,16);z)`, all `z >= 0`, all `x >= 16`, all `R >= 0`.
Claim under audit: K1237 (`cand16`, published fit, status **observed**)
equals `H` everywhere, with corollaries

- merge below the diagonal: `x <= z-17  =>  H == single_token(x+16,z,R)` (K0832),
- tail: `R >= x+z+17  =>  H == (x+16) % 2`.

Single-owner declaration note:
[2026-11-22-y16-universal-verifier-single-owner-note.md](../../log/2026-11-22-y16-universal-verifier-single-owner-note.md)
(commit `432664f7`, observed HEAD `76abc080`, counter-declaration grep clean),
published BEFORE the verifier run. Scope: part 1 (12 checks, this
publication) + part 2 (C1d published-slice anchors + census_rows.py third
implementation + C11r), which promotes K1237 observed -> proved on overall
PASS. Part 2 is NOT claimed at part-1 time; the promotion, when published,
is a separate commit of this dir.

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
every case; the canonical 12-check audit.json is the last full run.
The audit.json is overwritten by whichever check run wrote it last; the
canonical audit is re-established by the explicit check list (as
`output/published_run.txt` records).

## Reproduction

```sh
python3 scripts/build_verify_y16.py     # regenerates verify_y16_universal.py (byte-identical)
python3 verify_y16_universal.py C11ordered
python3 verify_y16_universal.py C11canonical
python3 verify_y16_universal.py C1 C1b C2 C2b C3 C4 C4t C7 C8 C9 C11 C12
```

## Interpretation

Part 1 is finite machine evidence for the universal claim K1237, of the
same machine class as the y=5..y=15 promotion machines (option
decomposition + closed-form mex identity + finite-type confluence,
anchored to raw engines, to the proved y=15 family B-child and to the
x=16 multiset merger). The status promotion (observed -> proved) is
reserved for part 2 (C1d published-slice anchors at the y=16 rows,
fail-closed pre-flighted, + the census_rows.py third-implementation
ledger consumed by C11r), per the identical two-part procedure used for
y=10/y=12/y=13/y=14/y=15 (K1141/K1152/K1231/K1233/K1235). Comparison
points are comparison counts, never verdicts about the standard 11x11
game; the 11x11 empty board, the two-stone roots {49,60}/{59,60}, S2
{59,60} and classes 1/2/4 remain UNKNOWN and untouched by this experiment.
