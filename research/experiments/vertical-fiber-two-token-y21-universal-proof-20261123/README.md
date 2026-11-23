# Vertical fiber: two-token y=21 parametric family, all-z universal verifier (single-edition 14-check machine)

Experiment dir: `vertical-fiber-two-token-y21-universal-proof-20261123`
Family: `H(R;(x,21);z)`, all `z >= 0`, all `x >= 21`, all `R >= 0`.
Claim under audit: K1248 (`cand21`, published fit, status **observed** at
machine-build time, **promoted proved by this run**) equals `H` everywhere,
with corollaries

- merge below the diagonal: `x <= z-22  =>  H == single_token(x+21,z,R)` (K0832),
- tail: `R >= x+z+22  =>  H == (x+21) % 2`.

Single-owner declaration note:
[2026-11-23-y21-universal-verifier-single-owner-note.md](../../log/2026-11-23-y21-universal-verifier-single-owner-note.md)
(commit `a0519efe`, observed HEAD-before-push `77d3cadf`, published BEFORE
the machine ran; no competing y=21 universal declaration existed then or at
publication -- the only published y=21 items were fit-form (the K1248 item,
the fit skeleton declaration note and the fit log), each stating that the
universal stage requires a separate declaration). Under the declaration
this machine is registered as the **single-edition 14-check** variant of the
published procedure (the y=13..y=18 part1/part2 editions folded into single
machines from y=19 on): the verifier is built in full form (the part1-style
12 checks plus `C1d` published-slice anchors and the independent
census-ledger consumer `C11r`) from the start, and executed in stages --
transcription check -> C1d preflight gate -> census generation -> 12-check
battery (kept as `output/audit-part1-12checks.json`) -> full 14-check
battery (`output/audit.json`). On overall PASS with byte-identical
determinism runs and the fail-closed battery, the declaration promotes
K1248 observed -> proved (same K item, the
K1141/K1152/K1231/K1233/K1236/K1239/K1241/K1242/K1243/K1245/K1246/K1249
precedent); the machine item is recorded as **K1255**.

## Machine composition (verify_y21_universal.py)

`verify_y21_universal.py` (53,269 bytes, SHA-256
`0ab841d9dd3d445fbde1c8142383d365048d7e3ca79fcd22ec6230c5bcec4c5a`,
single edition, 14 checks: C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/
C12) assembles three transcription blocks, each delimited by explicit
`# @@TRANSCRIPTION-*-START@@/END@@` markers and machine-verified against
the published bytes by `scripts/check_transcriptions_y21.py` (5,556 bytes,
SHA-256 `c4d7cc4e0ab33899bc61e78c768792670bb999ce62efd7d07075d1170b74d06a`,
structural anchors, no line numbers):

- **engine block** (1,957 bytes): `mex` / `H_ordered` / `H_canonical` /
  `q_odd` / `single_token`, verbatim from the published
  `verify_y20_universal.py` (git blob `170f3346`, byte-verified against
  main at the declaration's observed HEAD; provenance chain
  K1138/K1141/K1143/K1152/K1231/K1233/K1235/K1237/K1240/K1242/K1243/K1245/
  K1246/K1249 unchanged);
- **cand20 block** (3,308 bytes): the B-child of every y=21 point and the
  x=21 merger child value, verbatim from the published y=20 machine's
  `cand20` block with the block-local word-boundary rename `Y -> Y20`
  (two-source byte-equality: it equals BOTH the published
  `verify_y20_universal.py` cand20 block modulo the rename AND the
  published `cand20.py` of the K1246 fit experiment (git blob
  `a54cfb40`) modulo the rename, and the two published sources
  byte-agree; its universal proof is K1246, promoted proved by the
  y=20 machine; its y=21-scope usage (B-child x>=21 rows, A-child x=21
  merger) is inside its published universal domain x >= 20);
- **cand21 block** (3,412 bytes): the claim under test, verbatim from the
  published `cand21.py` of the K1248 fit experiment
  (`vertical-fiber-two-token-y21-parametric-fit-20261123`, git blob
  `38613e92`, itself the machine translation of the published cand19
  (K1243 proved) Y=19 -> 21 with a 112,530-point one-shot probe match;
  fit driver omitted).

Check result: `output/transcriptions-check-y21.json` -- engine equal,
cand20 two-source equal with the two published sources byte-agreeing,
cand21 equal, overall PASS (also re-run on the isolated determinism
tree).

Machine swaps relative to the published y=20 machine: merger row x==21
with A-child `cand20(z,21,R-1)` (multiset (20,21)==(21,20), the y=20
family x=21 row; the canonical-order treatment follows the y=14
confluence incident lesson, applied as in the y=20 machine), B-child
`cand20(z,x,R-1)`, C-child `1 xor cand21(z-1,x,R-1)`; clip window
`2y+2 = 44` / sentinel 45; census box `z=0..79, x=21..70,
R<=x+z+22` (80*50 = 4,000 rows, 432,000 points per engine); merge
`x<=z-22`; tail `(x+21)%2` at `R >= x+z+22`; C12 deep grid
`R<=x+z+23`; C8 keeps the x=20 rows as closed-form
extension-consistency rows only (no raw claim below x=21), exactly as
the x=19 rows did in the y=20 machine, and the deep-tail window check
uses the proved cand20 (K1246) tail claim `R>=x+z+21 => (x+20)%2` at
x>=20; C7 seed 20261212 (the y=16 seed 20261162 / y=17 seed 20261172 /
y=18 seed 20261182 / y=19 seed 20261192 / y=20 seed 20261202 series).

## Staged run results (all stages rc=0, all bad 0)

Executed in the declaration's pre-registered staged order on this host
(Linux x86_64, ~1.0 GiB cgroup class, the same class as the
y=15..y=20 census hosts); the wall times below are per stage.

1. **Transcription check PASS** (`scripts/check_transcriptions_y21.py`):
   engine 1,957 bytes / cand20 3,308 bytes (two-source, renamed) /
   cand21 3,412 bytes all equal, 0.06 s;
   `output/transcriptions-check-y21.json` (SHA-256
   `790071271d91b3cb0c140867b9e07e2b0a6ea8d3b7740b3cb6f44f021547519c`).
2. **C1d preflight gate PASS** (`scripts/preflight_c1d_y21.py`, 13,233
   bytes, SHA-256
   `fee17265f45a3e58d9090a41bb9e1c0ad7ff889e2d3cb8604a9c98d0505e7a6e`):
   published fixed-z slice anchors (z0 in {8,9,10,15,16,17}, x=21..46,
   R=1..x+z0+30) 4-way checked
   (anchor x H_ordered x H_canonical x cand21): **11,856 points bad 0**
   (per z 1,859/1,885/1,911/2,041/2,067/2,093) + published low-R
   single-token reduction R<=z+6 (z0=15/16/17, x=21..159):
   **9,174 points bad 0**; wall 4.5 s;
   `output/preflight-c1d-y21.json` (SHA-256
   `57897cfd4678219ed827546ceb3d9418cb956cf06224b115d57590b1f2c5d94b`).
   The preflight anchor block is byte-verbatim from the published y=20
   preflight (itself the y=10/y=12 chain). The y=10 precedent (this gate
   caught a 170-point evaluation-order bug in the first K1087
   transcription) is why this stage exists; here the 4-way check agreed
   on the first run.
3. **Census ledger generation** (`census_rows.py`, third implementation
   y=21 edition, SHA-256
   `79234646943179248c02ec4b78c23d8303cfc4f371b8f80251d404cc2f561166`,
   XMIN=21 / XMAX=70 / RBUF=23 / ZHI=80, LRU cap 1,600,000):
   `output/census.txt` (800,318 bytes, 4,000 rows + 80 blank separators,
   SHA-256 `d63141b75900a95ed926c9b7574694234c33438760f7038f7c7751104b02e89f`):
   **436,000 points**, zero-value points 217,061, engine states
   (LRU misses) 10,909,227 / hits 21,370,154, ~25.5 s; the tail assert
   `R>=x+z+22 => (x+21)%2` held on every row.
4. **Census parts PASS** (`C11ordered` / `C11canonical`,
   bounded-memoization twins of the verbatim raw engines, LRU cap
   1,600,000, separate commands): each engine **432,000 points bad 0**,
   merge corollary per engine 86,469 bad 0, tail per engine 4,000 bad 0;
   walls 24.9 s / 28.6 s;
   `output/census-ordered.json` (SHA-256
   `302794361d7b958bd6be4224eeedaaecd2e7ac981fbc6c2a1c6f2ba9a116175a`) /
   `output/census-canonical.json` (SHA-256
   `b88e3ddcf617dfa23c4f928cc88b6491f8128a2187c82476c6820c7b7e4b165a`).
   The `C11` mode validates both parts fail-closed (engine field, box
   string `z=0..79, x=21..70, R=0..x+z+22`, cache cap, recomputed
   expected counts 432,000 / 86,469 / 4,000) and merges them.
5. **Staged 12-check battery PASS** (the declaration's stage before the
   full battery; kept as `output/audit-part1-12checks.json`, SHA-256
   `dab3dc53eabcceede29087f34240850aa26a21606a4618b97b5b690f959d0abd`):
   C1 25,650 / C1b 45,489 / C1d 135,108 / C2 238,091 / C2b 19,756 /
   C3 1,395 / C4 568,340 / C4t 568,340 (probe, not in bad) /
   C7 200,000 / C8 1,100,592 / C9 892,650 / C12 1,857,350;
   **total_points 5,652,761, total_bad 0**, types 727,229; wall 52.4 s.
   Merge corollary at this stage: 771,114 points bad 0; tail corollary
   184,053 points bad 0.
6. **Full 14-check battery PASS** (C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/
   C9/C11/C11r/C12 in one command, `output/audit.json`, SHA-256
   `c039ca732ed19e30d4ac0eb3941832eefd301cd8872494d0fe0d6f16a255e3ae`):
   **total_points 6,952,761, total_bad 0, types 727,229** (the
   declared arithmetic: 12-check subtotal 6,381,653 + C1d 135,108 +
   C11r 436,000); C11 864,000 (both engines merged), C11r 436,000 over
   4,000 rows; merge corollary **944,052 points bad 0**; tail
   corollary **192,053 points bad 0**; walls 53.8 s (run 1) / 53.3 s
   (run 2) / 53.1 s (run 3).

Type-count series (final 14-check registry, clip 2y+2): y=14: 281,912 ->
y=15: 335,658 -> y=16: 394,686 -> y=17: 457,645 -> y=18: 523,398 ->
y=19: 590,877 -> y=20: 658,978 -> **y=21: 727,229**. The C4 in-box
registered type count at clip 44 / sentinel 45 is 429,397 (succeeding
the y=20 machine's 408,708 at clip 42; the declaration made no advance
numerical prediction here).

### C4t tightness probe: clip 43 has 408 confluence violations, first (60,106,106)

The clip window `2y+2 = 44` is **tight**, the 17th consecutive family
(y=5..21:
12/14/16/18/20/22/24/26/28/30/32/34/36/38/40/42/44), continuing the
pattern that the first violation walks with the band bottom (y=13: clip
27 (60,90,90); y=14: clip 29 (60,92,92); y=15: clip 31 (60,94,94);
y=16: clip 33 (60,96,96); y=17: clip 35 (60,98,98); y=18: clip 37
(60,100,100); y=19: clip 39 (60,102,102); y=20: clip 41 (60,104,104);
**y=21: clip 43 (60,106,106)**), the 9th observation of the walking
first-violation series -- exactly as pre-registered in the declaration
note (violations > 0 -> tight confirmed; the declaration predicted both
the >0 and the (60,106,106) first violation, and the machine matched
both).

## Honest record: declaration predictions vs. machine measurements

The declaration note pre-computed every check point count, the
preflight boxes, the census geometry, the C11r row/point counts, the
12-check subtotal, the 14-check total, the merge/tail corollary point
counts, the C4t first violation and the C11r tail-flip probe count with
`predict_y21_counts.py` (loop geometry only, no game evaluation), and
cross-validated that function against BOTH the published y=19 and y=20
audits (all 14 check counts of each machine audit reproduced exactly,
totals 6,941,913 / 6,947,960) BEFORE this machine ran. Every declared
machine-computed prediction matched the measurement exactly (preflight
11,856 + 9,174; C1d 135,108 = 125,934 + 9,174; census 4,000 rows /
432,000 per engine / 4,000 tail per engine; C11r 436,000; 12-check
subtotal 6,381,653; staged battery 5,652,761; total 6,952,761; merge
corollary 944,052; tail corollary 192,053; C4t violations > 0 with
first (60,106,106); C11r tail-flip probe exactly 4,000). One
declaration-prose discrepancy is recorded honestly: the declaration
note's census-geometry prose line wrote the per-engine merge-region
count as **86,436** -- a digit transposition of the machine-computed
**86,469** (the same note's declared merge corollary total 944,052
requires 86,469 per engine (944,052 = 771,114 + 2 x 86,469) and matched
the machine exactly; the machine's own recomputed expected counts,
which the C11 mode enforces fail-closed, are 86,469). The declaration
note is a dated primary source and is not amended; the correct figure
is 86,469. No other amendment was needed at any stage of this run. The
build of the machine itself went through count-asserted builder
corrections before any battery ran (local build only, never published);
all published bytes are the final builds.

## Determinism (4 byte-identical full audits)

run1 (canonical cwd) -> run2 (same-cwd rerun, fresh process) -> run3
(same-cwd second rerun; stdout byte-identical and audit.json rewritten
identically) -> run4 (isolated tree/cwd/HOME under `env -i`, PATH
pinned, `PYTHONHASHSEED=random`, with the FULL pipeline regenerated on
the isolated side: transcription check, preflight, census_rows.py, both
census parts, the staged 12-check battery, and the full 14-check
command; census_rows engine states reproduced exactly: misses
10,909,227 / hits 21,370,154).
`output/audit.json`, `census.txt`, `census-ordered.json`,
`census-canonical.json`, `preflight-c1d-y21.json`,
`transcriptions-check-y21.json`, `audit-part1-12checks.json` all
byte-identical across the runs (the isolated regeneration reproduces
every published byte from scratch).

## Fail-closed battery (12 probes, all caught; scratch tree only)

Exercised on a scratch copy of the canonical tree; the canonical tree's
11 published files were hash-verified after the whole battery and no
tampered byte was published:

1. census.txt missing: FAIL-CLOSED "census.txt is missing; run
   census_rows.py first", rc=1;
2. census.txt data-row deleted: FAIL-CLOSED "census rows 3999 != 4000",
   rc=1;
3. duplicate census-row injection: FAIL-CLOSED "duplicate census row
   (0,21)", rc=1;
4. census.txt P-set member tamper (first row, `P={1,3,...} ->
   P={4,3,...}`): C11r bad 1, overall FAIL, rc=1;
5. census.txt T-set bogus-member injection (first row, `T={} ->
   T={5}`): C11r bad 1, overall FAIL, rc=1;
6. C11r tail flip `(x+21)` -> `(x+22)` on a tampered verifier copy:
   C11r bad 4,000 (every row; the declaration predicted exactly the
   row count), overall FAIL, rc=1;
7. anchor mis-binding `(17, A17u) -> (17, A10u)` on a tampered verifier
   copy: C1d bad 14,769, overall FAIL, rc=1;
8. low-R reference shift `R -> R+1` on a tampered verifier copy: C1d
   bad 9,174 (every low-R point independently mismatches, the exact
   low-R box size), overall FAIL, rc=1;
9. corollary merge boundary tamper `x<=z-22 -> x<=z-21` on a tampered
   verifier copy: merge corollary pts 806,178 bad 7,435 (tail bad 0),
   overall FAIL, rc=1;
10. type-machine clip window tamper `CLIP, SENT = 44, 45 -> 42, 43`:
    C4 confluence violations, bad 1,360, overall FAIL, rc=1;
11. in_P21 tail parity flip (x even -> x odd) on a tampered verifier
    copy: C1 bad 2,449 / C2 bad 23,478, overall FAIL, rc=1;
12. in_P21 band parity tamper (off%2==0 -> off%2==1, both band lines)
    on a tampered verifier copy: C1 bad 1,692 / C2 bad 24,431, overall
    FAIL, rc=1.

Probe-design honest record: the first issues of probes (4) and (5)
were no-ops of the probe harness itself, not missed detections -- the
tamper regexes matched ASCII bracket set syntax `[...]` while the
ledger rows carry brace sets `T={} / P={...}`, so the edit aborted
before any byte was tampered and the untouched copies ran PASS. Both
were re-issued with effective tampering (first-row P-member change
`P={1,...} -> P={4,...}`; `T={} -> T={5}`) and both were caught
immediately (C11r bad 1 twice). The canonical tree was cmp'd clean
against the isolated regeneration after the whole battery.

## Promotion decision

With the full 14-check audit PASS (6,952,761 comparison points, bad 0),
the fail-closed pre-verified C1d anchors, the independent
third-implementation census ledger consumed by C11r, 4 byte-identical
audit runs (3 same-cwd + 1 isolated, the isolated one a full pipeline
regeneration), and the fail-closed battery all caught (with the two
probe-design no-ops recorded honestly), **K1248 is promoted observed ->
proved** (same K item, no new numbering, the
K1141/K1152/K1231/K1233/K1236/K1239/K1241/K1242/K1243/K1245/K1246/K1249
precedent; the machine item is K1255). The corollaries are fixed as
universal claims in the same scope: the merge proposition's y=21
edition `x<=z-22 => H == single_token(x+21,z,R)` and the tail value
`R>=x+z+22 => H == (x+21)%2`, so **the merge proposition now holds
universally through y=1..21**. The B-child of the y=21 family is the
verbatim cand20 (K1246, proved), extending the B-child verbatim chain
to cand9..cand20 and the proved-B-child usage to cand10/cand12..cand20.
The two-token universal series is complete through y=21 (K1246 existed
as the y=20 endpoint; K1248 extends it by one family).

## Reproduction

```sh
cd research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123
python3 scripts/check_transcriptions_y21.py        # transcription byte-equality (repo-root discovery via AGENTS.md)
python3 scripts/preflight_c1d_y21.py               # C1d preflight gate (~5 s)
python3 census_rows.py                             # regenerate output/census.txt (~26 s)
python3 verify_y21_universal.py C11ordered         # census part 1 (~25 s)
python3 verify_y21_universal.py C11canonical      # census part 2 (~29 s)
python3 verify_y21_universal.py                    # staged 12-check battery (~52 s, keep audit.json as audit-part1-12checks.json)
python3 verify_y21_universal.py C1 C1b C1d C2 C2b C3 C4 C4t C7 C8 C9 C11 C11r C12   # full 14-check battery (~54 s)
```

Note: the bare `verify_y21_universal.py` invocation (no arguments) runs
the STAGED 12-check battery only (C11/C11r excluded) in this edition;
the full 14-check battery always requires the explicit 14-check
argument list above (running `C11` alone only validates and merges the
census parts).

## Interpretation

Same trust boundary as the y=5..y=20 machines: option decomposition +
closed-form mex identity + finite-type confluence over the
free-coordinate box, anchored to raw engines, to the proved y=20
family (K1246, the B-child), and to the x=21 multiset merger
(20,21)==(21,20). Finite comparison is finite observation; the
machine's PASS is mechanical evidence for the universal claim, and the
14-check audit (C1d published slice anchors at the y=21 rows +
census_rows.py third-implementation ledger + C11r, plus byte-identical
determinism runs) is the basis on which K1248 has been promoted
observed -> proved in this dir. The standard 11x11 empty board, the
two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain
UNKNOWN and are unrelated to this family. Three or more tokens,
y>=22 families, fixed-width and q-point stabilization length are out
of scope.
