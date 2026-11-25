# Vertical fiber: two-token y=20 parametric family, all-z universal verifier (single-edition 14-check machine)

Experiment dir: `vertical-fiber-two-token-y20-parametric-allz-proof-20261123`
Family: `H(R;(x,20);z)`, all `z >= 0`, all `x >= 20`, all `R >= 0`.
Claim under audit: K1246 (`cand20`, published fit, status **observed** at
machine-build time, **promoted proved by this run**) equals `H` everywhere,
with corollaries

- merge below the diagonal: `x <= z-21  =>  H == single_token(x+20,z,R)` (K0832),
- tail: `R >= x+z+21  =>  H == (x+20) % 2`.

Single-owner declaration note:
[2026-11-23-y20-universal-verifier-single-owner-note.md](../../log/2026-11-23-y20-universal-verifier-single-owner-note.md)
(commit `c1987caa`, observed HEAD-before-push `69f76309`, published BEFORE
the machine ran; no competing y=20 universal declaration existed then or at
publication). Under the declaration this machine is registered as the
**single-edition 14-check** variant of the published procedure (the y=13..y=18
part1/part2 editions folded into single machines from y=19 on): the verifier
is built in full form (the part1-style 12 checks plus `C1d` published-slice
anchors and the independent census-ledger consumer `C11r`) from the start,
and executed in stages -- transcription check -> C1d preflight gate ->
census generation -> 12-check battery (kept as
`output/audit-part1-12checks.json`) -> full 14-check battery
(`output/audit.json`). On overall PASS with byte-identical determinism runs
and the fail-closed battery, the declaration promotes K1246 observed ->
proved (same K item, the
K1141/K1152/K1231/K1233/K1235/K1237/K1240/K1242/K1243 precedent); the machine
item is recorded as **K1249**.

## Machine composition (verify_y20_universal.py)

`verify_y20_universal.py` (53,146 bytes, SHA-256
`1e2a519f0bf81c401a3d18e0183a24d333ffd5eafabcd4b37032b0ed41a96bc9`,
single edition, 14 checks: C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/
C12) assembles three transcription blocks, each delimited by explicit
`# @@TRANSCRIPTION-*-START@@/END@@` markers and machine-verified against
the published bytes by `scripts/check_transcriptions_y20.py`
(SHA-256 `824209582300d6ae961d14de729361098bc5c9893fa19bb61c8e8e72cda1612b`,
structural anchors, no line numbers):

- **engine block** (1,957 bytes): `mex` / `H_ordered` / `H_canonical` /
  `q_odd` / `single_token`, verbatim from the published
  `verify_y19_universal.py` (commit `99b7e070`, git blob `c0cec1d5`,
  re-checked against main at the declaration's observed HEAD; provenance
  chain K1138/K1141/K1143/K1152/K1231/K1233/K1235/K1237/K1240/K1242/K1243
  unchanged);
- **cand19 block** (3,501 bytes): the B-child of every y=20 point and the
  x=20 merger child value, verbatim from the published y=19 machine's
  `cand19` block with the block-local word-boundary rename `Y -> Y19`
  (two-source byte-equality: it equals BOTH the published
  `verify_y19_universal.py` cand19 block modulo the rename AND the
  published `cand19.py` of the K1243 fit experiment (commit `eaea0f6a`,
  git blob `cb05633f`) modulo the rename; its universal proof is K1243,
  promoted proved by the y=19 machine; its y=20-scope usage (B-child
  x>=20 rows, A-child x=20 merger) is inside its published universal
  domain x >= 19);
- **cand20 block** (3,212 bytes): the claim under test, verbatim from the
  published `cand20.py` of the K1246 fit experiment (commit `7a2d3f9a`,
  git blob `a54cfb40`, re-checked against main at the declaration's
  observed HEAD), fit driver omitted.

Check result: `output/transcriptions-check-y20.json` -- engine equal,
cand19 two-source equal with the two published sources byte-agreeing,
cand20 equal, overall PASS (also re-run on the isolated determinism
tree).

Machine swaps relative to the published y=19 machine: merger row x==20
with A-child `cand19(z,20,R-1)` (multiset (19,20)==(20,19), the y=19
family x=20 row; the canonical-order treatment follows the y=14
confluence incident lesson, applied as in the y=19 machine), B-child
`cand19(z,x,R-1)`, C-child `1 xor cand20(z-1,x,R-1)`; clip window
`2y+2 = 42` / sentinel 43; census box `z=0..79, x=20..70,
R<=x+z+21` (80*51 = 4,080 rows, 434,520 points per engine); merge
`x<=z-21`; tail `(x+20)%2` at `R >= x+z+21`; C12 deep grid
`R<=x+z+22`; C8 keeps the x=19 rows as closed-form
extension-consistency rows only (no raw claim below x=20), exactly as
the x=18 rows did in the y=19 machine, and the deep-tail window check
uses the proved cand19 (K1243) tail claim `R>=x+z+20 => (x+19)%2` at
x>=19; C7 seed 20261202 (the y=15 seed 20261152 / y=16 seed 20261162 /
y=17 seed 20261172 / y=18 seed 20261182 / y=19 seed 20261192 series).

## Staged run results (all stages rc=0, all bad 0)

Executed in the declaration's pre-registered staged order on this host
(Linux x86_64, ~1.0 GiB cgroup class, the same class as the
y=15..y=19 census hosts); the wall times below are per stage.

1. **Transcription check PASS** (`scripts/check_transcriptions_y20.py`):
   engine 1,957 bytes / cand19 3,501 bytes (two-source, renamed) /
   cand20 3,212 bytes all equal, 0.06 s.
2. **C1d preflight gate PASS** (`scripts/preflight_c1d_y20.py`,
   SHA-256 `3e9932d705c889fa93429a9fe9fa285d24f7289028a0e6a686a1c15e1ba56159`):
   published fixed-z slice anchors (z0 in {8,9,10,15,16,17}, x=20..45,
   R=1..x+z0+30) 4-way checked
   (anchor x H_ordered x H_canonical x cand20): **11,700 points bad 0**
   (per z 1,833/1,859/1,885/2,015/2,041/2,067) + published low-R
   single-token reduction R<=z+6 (z0=15/16/17, x=20..159):
   **9,240 points bad 0**; wall 3.3 s;
   `output/preflight-c1d-y20.json` (SHA-256
   `d2aabc6ee86b3991a1161f4e41540abbe656d7d18efe9e743772d59b00efd09c`).
   The preflight anchor block is byte-verbatim from the published y=19
   preflight (itself the y=10/y=12 chain). The y=10 precedent (this gate
   caught a 170-point evaluation-order bug in the first K1087
   transcription) is why this stage exists; here the 4-way check agreed
   on the first run.
3. **Census ledger generation** (`census_rows.py`, third implementation
   y=20 edition, SHA-256
   `af93fcc725e1a880b6f4aaa95da412b7ae6cb09fb4cd24670ae8b0a4094d87c4`,
   XMIN=20 / XMAX=70 / RBUF=22 / ZHI=80, LRU cap 1,600,000):
   `output/census.txt` (801,508 bytes, 4,080 rows + 80 blank separators,
   SHA-256 `b858c4964eb6f15bf9a2286a947024ed3bf0c0247cd74299d12f7f0ca5c96245`):
   **438,600 points**, zero-value points 219,325, engine states
   (LRU misses) 10,354,827, ~20 s; the tail assert
   `R>=x+z+21 => (x+20)%2` held on every row.
4. **Census parts PASS** (`C11ordered` / `C11canonical`,
   bounded-memoization twins of the verbatim raw engines, LRU cap
   1,600,000, separate commands): each engine **434,520 points bad 0**,
   merge corollary per engine 94,380 bad 0, tail per engine 4,080 bad 0;
   `output/census-ordered.json` (SHA-256
   `ed073fa82bdf585170766a0e31dd2e79f14fc16d38c31b5f983acbc4773a3798`) /
   `output/census-canonical.json` (SHA-256
   `1f420269012fc50eefd71b3b1928058caca11740b0197182da34fdc24c63d276`).
   The `C11` mode validates both parts fail-closed (engine field, box
   string `z=0..79, x=20..70, R=0..x+z+21`, cache cap, recomputed
   expected counts 434,520 / 94,380 / 4,080) and merges them.
5. **Staged 12-check battery PASS** (the declaration's stage before the
   full battery; kept as `output/audit-part1-12checks.json`, SHA-256
   `ff347b9c05f09a823fc751a07165272f528f2713a3d53598f5decb172d7b21bb`):
   C1 25,080 / C1b 44,758 / C1d 135,660 / C2 233,877 / C2b 19,668 /
   C3 1,365 / C4 574,040 / C4t 574,040 (probe, not in bad) /
   C7 200,000 / C8 1,078,938 / C9 895,302 / C12 1,857,592;
   **total_points 5,640,320, total_bad 0**, types 658,978; wall 38.9 s.
   Merge corollary at this stage: 814,607 points bad 0; tail corollary
   184,094 points bad 0.
6. **Full 14-check battery PASS** (C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/
   C9/C11/C11r/C12 in one command, `output/audit.json`, SHA-256
   `a09cad0e4b5d3a9eaf16511faf58428cec1b8d4401b15012964165d0bc8814ee`):
   **total_points 6,947,960, total_bad 0, types 658,978** (the
   declared arithmetic: 12-check subtotal 6,373,700 + C1d 135,660 +
   C11r 438,600); C11 869,040 (both engines merged), C11r 438,600 over
   4,080 rows; merge corollary **1,003,367 points bad 0**; tail
   corollary **192,254 points bad 0**; wall 39.5 s.

Type-count series (final 14-check registry, clip 2y+2): y=14: 281,912 ->
y=15: 335,658 -> y=16: 394,686 -> y=17: 457,645 -> y=18: 523,398 ->
y=19: 590,877 -> **y=20: 658,978**.

### C4t tightness probe: clip 41 has 570 confluence violations, first (60,104,104)

The clip window `2y+2 = 42` is **tight**, the 16th consecutive family
(y=5..20:
12/14/16/18/20/22/24/26/28/30/32/34/36/38/40/42), continuing the pattern
that the first violation walks with the band bottom (y=13: clip 27
(60,90,90); y=14: clip 29 (60,92,92); y=15: clip 31 (60,94,94);
y=16: clip 33 (60,96,96); y=17: clip 35 (60,98,98); y=18: clip 37
(60,100,100); y=19: clip 39 (60,102,102); **y=20: clip 41
(60,104,104)**), the 8th observation of the walking first-violation
series -- exactly as pre-registered in the declaration note (violations
> 0 -> tight confirmed; the declaration predicted both the >0 and the
(60,104,104) first violation, and the machine matched both).

## Honest record: declaration predictions vs. machine measurements

The declaration note pre-computed every check point count, the
preflight boxes, the census geometry, the C11r row/point counts, the
12-check subtotal, the 14-check total, the merge/tail corollary point
counts, the C4t first violation and the C11r tail-flip probe count with
`predict_y20_counts.py` (loop geometry only, no game evaluation), and
cross-validated that function against the published y=19 audit (all 14
check counts of the y=19 machine audit reproduced exactly, total
6,941,913) BEFORE this machine ran. Every single declared prediction
matched the machine measurement exactly (preflight 11,700 + 9,240;
C1d 135,660 = 126,420 + 9,240; census 4,080 rows / 434,520 per engine /
94,380 merge per engine / 4,080 tail per engine; C11r 438,600;
12-check subtotal 6,373,700; total 6,947,960; merge corollary
1,003,367; tail corollary 192,254; C4t violations > 0 with first
(60,104,104)). No amendment was needed at any stage of this run. The
build of the machine itself went through count-asserted builder
corrections before any battery ran (local build only, never published);
all published bytes are the final builds.

## Determinism (4 byte-identical full audits)

run1 (canonical cwd) -> run2 (same-cwd rerun, fresh process) -> run3
(same-cwd second rerun; stdout byte-identical and audit.json rewritten
identically) -> run4 (isolated tree/cwd/HOME under `env -i`, PATH
pinned, `PYTHONHASHSEED=random`, with the FULL pipeline regenerated on
the isolated side: transcription check, preflight, census_rows.py, both
census parts, and the full 14-check command; census_rows engine states
reproduced exactly: misses 10,354,827 / hits 20,284,849).
`output/audit.json`, `census.txt`, `census-ordered.json`,
`census-canonical.json`, `preflight-c1d-y20.json`,
`transcriptions-check-y20.json` all byte-identical across the runs (the
isolated regeneration reproduces every published byte from scratch).

## Fail-closed battery (12 probes, all caught; scratch tree only)

Exercised on a scratch copy of the canonical tree; the canonical tree's
outputs were byte-verified after every probe and no tampered byte was
published:

1. census.txt missing: FAIL-CLOSED "census.txt is missing; run
   census_rows.py first", rc=1;
2. census.txt data-row deleted: FAIL-CLOSED "census rows 4079 != 4080",
   rc=1;
3. duplicate census-row injection: FAIL-CLOSED "duplicate census row
   (0,20)", rc=1;
4. census.txt P-set member tamper (first row): C11r bad 1, overall
   FAIL, rc=1;
5. census.txt T-set bogus-member injection: C11r bad 1, overall FAIL,
   rc=1;
6. C11r tail flip `(x+20)` -> `(x+21)` on a tampered verifier copy:
   C11r bad 4,080 (every row; the declaration predicted exactly the
   row count), overall FAIL, rc=1;
7. anchor mis-binding `(17, A17u) -> (17, A10u)` on a tampered verifier
   copy: C1d bad 14,666, overall FAIL, rc=1;
8. low-R reference shift `R -> R+1` on a tampered verifier copy: C1d
   bad 9,240 (every low-R point independently mismatches, the exact
   low-R box size), overall FAIL, rc=1;
9. corollary merge boundary tamper `x<=z-21 -> x<=z-20` on a tampered
   verifier copy: merge corollary bad 7,528, overall FAIL, rc=1;
10. type-machine clip window tamper `CLIP, SENT = 42, 43 -> 40, 41`:
    C4 confluence violations, bad 1,881, overall FAIL, rc=1;
11. in_P20 tail parity flip (x odd -> x even) on a tampered verifier
    copy: C1 bad 4,898 / C2 bad 24,024, overall FAIL, rc=1;
12. in_P20 band parity tamper on a tampered verifier copy: C1 bad
    1,763 / C2 bad 24,451, overall FAIL, rc=1.

Probe-design honest record: the first issue of probes (4) and (8) were
no-ops of the probe harness itself, not missed detections -- (4)'s sed
pattern `P={21,23}` does not occur in the ledger (rows carry full P
sets), and (8)'s end-of-line anchor missed the trailing `:` of the
tampered line. Both were re-issued with effective tampering (first-row
P-member change; in-line R -> R+1) and both were caught immediately
(C11r bad 1; C1d bad 9,240). The canonical tree was cmp'd clean against
the isolated regeneration after the whole battery.

## Promotion decision

With the full 14-check audit PASS (6,947,960 comparison points, bad 0),
the fail-closed pre-verified C1d anchors, the independent
third-implementation census ledger consumed by C11r, 4 byte-identical
audit runs (3 same-cwd + 1 isolated, the isolated one a full pipeline
regeneration), and the fail-closed battery all caught (with the two
probe-design no-ops recorded honestly), **K1246 is promoted observed ->
proved** (same K item, no new numbering, the
K1141/K1152/K1231/K1233/K1235/K1237/K1240/K1242/K1243 precedent; the
machine item is K1249). The corollaries are fixed as universal claims in
the same scope: the merge proposition's y=20 edition
`x<=z-21 => H == single_token(x+20,z,R)` and the tail value
`R>=x+z+21 => H == (x+20)%2`, so **the merge proposition now holds
universally through y=1..20**. The B-child of the y=20 family is the
verbatim cand19 (K1243, proved), extending the B-child verbatim chain
to cand9..cand19 and the proved-B-child usage to cand10/cand12..cand19.
The two-token universal series is complete through y=20 (K1243 existed
as the y=19 endpoint; K1246 extends it by one family).

## Reproduction

```sh
cd research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123
python3 scripts/check_transcriptions_y20.py        # transcription byte-equality (repo-root discovery via AGENTS.md)
python3 scripts/preflight_c1d_y20.py               # C1d preflight gate (~3 s)
python3 census_rows.py                             # regenerate output/census.txt (~20 s)
python3 verify_y20_universal.py C11ordered         # census part 1 (~19 s)
python3 verify_y20_universal.py C11canonical       # census part 2 (~22 s)
python3 verify_y20_universal.py                    # staged 12-check battery (~39 s, keep audit.json as audit-part1-12checks.json)
python3 verify_y20_universal.py C1 C1b C1d C2 C2b C3 C4 C4t C7 C8 C9 C11 C11r C12   # full 14-check battery (~40 s)
```

## Interpretation

Same trust boundary as the y=5..y=19 machines: option decomposition +
closed-form mex identity + finite-type confluence over the
free-coordinate box, anchored to raw engines, to the proved y=19
family (K1243, the B-child), and to the x=20 multiset merger
(19,20)==(20,19). Finite comparison is finite observation; the
machine's PASS is mechanical evidence for the universal claim, and the
14-check audit (C1d published slice anchors at the y=20 rows +
census_rows.py third-implementation ledger + C11r, plus byte-identical
determinism runs) is the basis on which K1246 has been promoted
observed -> proved in this dir. The standard 11x11 empty board, the
two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain
UNKNOWN and are unrelated to this family. Three or more tokens,
y>=21 families, fixed-width and q-point stabilization length are out
of scope.
