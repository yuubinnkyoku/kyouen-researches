# Vertical fiber: two-token y=22 parametric family, all-z universal verifier (single-edition 14-check machine)

Experiment dir: `vertical-fiber-two-token-y22-universal-proof-20261123`
Family: `H(R;(x,22);z)`, all `z >= 0`, all `x >= 22`, all `R >= 0`.
Claim under audit: K1256 (`cand22`, published fit, status **observed** at
machine-build time, **promoted proved by this run**) equals `H` everywhere,
with corollaries

- merge below the diagonal: `x <= z-23  =>  H == single_token(x+22,z,R)` (K0832),
- tail: `R >= x+z+23  =>  H == (x+22) % 2`.

Single-owner declaration note:
[2026-11-23-y22-universal-verifier-single-owner-note.md](../../log/2026-11-23-y22-universal-verifier-single-owner-note.md)
(commit `e1e60cd4`, observed HEAD-before-push `db195667`, published BEFORE
the machine ran; no competing y=22 universal declaration existed then or at
publication -- the only published y=22 items were fit-form (the K1256 item,
the fit skeleton declaration note commit `c0baada6` and the fit log), each
stating that the universal stage requires a separate declaration). Under the
declaration this machine is registered as the **single-edition 14-check**
variant of the published procedure (per the y=13..y=18 part1/part2 editions
folded into single machines from y=19 on): the verifier is built in full form
(the part1-style 12 checks plus `C1d` published-slice anchors and the
independent census-ledger consumer `C11r`) from the start, and executed in
stages -- transcription check -> C1d preflight gate -> census generation ->
12-check battery (kept as `output/audit-part1-12checks.json`) -> full
14-check battery (`output/audit.json`). On overall PASS with byte-identical
determinism runs and the fail-closed battery, the declaration promotes
K1256 observed -> proved (same K item, the
K1141/K1152/K1231/K1233/K1236/K1239/K1241/K1242/K1243/K1245/K1246/K1249/K1255
precedent); the machine item is recorded as **K1257**.

**y=22 is the first family outside the previously proved universal range
(y=1..21, K1248 proved), and this machine is the first whose B-child is
itself a proved universal closed form** (the published cand21, K1248
promoted proved by the y=21 machine K1255): the B-child verbatim chain
extends to cand9..cand21, with proved B-child usage cand10/cand12..cand21.

## Machine composition (verify_y22_universal.py)

`verify_y22_universal.py` (53,422 bytes, SHA-256
`96d9787fae441a39c1cf0475e446b9dfef9bcc8297818afc1bd82a9f3c19ec6b`,
single edition, 14 checks: C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/
C12) assembles three transcription blocks, each delimited by explicit
`# @@TRANSCRIPTION-*-START@@/END@@` markers and machine-verified against
the published bytes by `scripts/check_transcriptions_y22.py` (5,580 bytes,
SHA-256 `08b02ddce2a3013778f1a9ee2afb706915febed992695934ca69272b14556668`,
structural anchors, no line numbers):

- **engine block** (1,957 bytes): `mex` / `H_ordered` / `H_canonical` /
  `q_odd` / `single_token`, verbatim from the published
  `verify_y21_universal.py` (git blob `ca5e8284`, byte-verified against
  main; provenance chain K1138/K1141/K1143/K1152/K1231/K1233/K1235/K1237/
  K1240/K1242/K1243/K1245/K1246/K1249/K1255 unchanged);
- **cand21 block** (3,502 bytes): the B-child of every y=22 point and the
  x=22 merger child value, verbatim from the published y=21 machine's
  `cand21` block with the block-local word-boundary rename `Y -> Y21`
  (two-source byte-equality: it equals BOTH the published
  `verify_y21_universal.py` cand21 block modulo the rename AND the
  published `cand21.py` of the K1248 fit experiment (git blob
  `38613e92`) modulo the rename, and the two published sources
  byte-agree; its universal proof is K1248, promoted proved by the y=21
  machine; **series-first proved-universal B-child**; its y=22-scope
  usage (B-child x>=22 rows, A-child x=22 merger) is inside its proved
  universal domain x >= 21);
- **cand22 block** (3,212 bytes): the claim under test, verbatim from the
  published `cand22.py` of the K1256 fit experiment
  (`vertical-fiber-two-token-y22-parametric-fit-20261123`, git blob
  `fd50358e`, itself the machine translation of the published cand20
  (K1246 proved) Y=20 -> 22 with a 119,567-point one-shot probe match;
  fit driver omitted).

Check result: `output/transcriptions-check-y22.json` -- engine equal,
cand21 two-source equal with the two published sources byte-agreeing,
cand22 equal, overall PASS (also re-run on the isolated determinism
tree).

Machine swaps relative to the published y=21 machine: merger row x==22
with A-child `cand21(z,22,R-1)` (multiset (21,22)==(22,21), the y=21
family x=22 row; the canonical-order treatment follows the y=14
confluence incident lesson, applied as in the y=21 machine), B-child
`cand21(z,x,R-1)`, C-child `1 xor cand22(z-1,x,R-1)`; clip window
`2y+2 = 46` / sentinel 47; census box `z=0..79, x=22..70,
R<=x+z+23` (80 x 49 = 3,920 rows, 429,240 points per engine); merge
`x<=z-23` (first non-empty at z=45 in the census box); tail `(x+22)%2`
at `R >= x+z+23`; C12 deep grid `R<=x+z+24`; C8 keeps the x=21 rows as
closed-form extension-consistency rows only (no raw claim below x=22),
exactly as the x=20 rows did in the y=21 machine, and the deep-tail
window check uses the proved cand21 (K1248) tail claim
`R>=x+z+22 => (x+21)%2` at x>=21 with window (x+z+23, x+z+24, x+z+25);
C7 seed 20261222 (the y=19 seed 20261192 / y=20 seed 20261202 /
y=21 seed 20261212 series).

## Staged run results (all stages rc=0, all bad 0)

Executed in the declaration's pre-registered staged order on this host
(Linux x86_64, memory-capped sandbox, ~1.0 GiB cgroup class); the wall
times below are per stage.

1. **Transcription check PASS** (`scripts/check_transcriptions_y22.py`):
   engine 1,957 bytes / cand21 3,502 bytes (two-source, renamed) /
   cand22 3,212 bytes all equal, 0.06 s;
   `output/transcriptions-check-y22.json` (SHA-256
   `7767d14cdded3bc7bc34e2ebe701b18a40408c999778844d2a199719e9b2a470`).
2. **C1d preflight gate PASS** (`scripts/preflight_c1d_y22.py`, 13,335
   bytes, SHA-256
   `765cd4caed813e5619ab13d8419fa26d7110304958411966153fe2481b74cabd`):
   published fixed-z slice anchors (z0 in {8,9,10,15,16,17}, x=22..47,
   R=1..x+z0+30) 4-way checked
   (anchor x H_ordered x H_canonical x cand22): **12,012 points bad 0**
   (per z 1,885/1,911/1,937/2,067/2,093/2,119) + published low-R
   single-token reduction R<=z+6 (z0=15/16/17, x=22..159):
   **9,108 points bad 0**; wall ~5 s;
   `output/preflight-c1d-y22.json` (SHA-256
   `a65b967d13bbaa62f623a9a789285a76a2ed4f15939552740052f0ea5973dcea`).
   The preflight anchor block is byte-verbatim from the published y=21
   preflight (itself the y=10/y=12 chain). The y=10 precedent (this gate
   caught a 170-point evaluation-order bug in the first K1087
   transcription) is why this stage exists; here the 4-way check agreed
   on the first run.
3. **Census ledger generation** (`census_rows.py`, third implementation
   y=22 edition, SHA-256
   `36ff30566025713e509a42a46f715cad1280ee4e2dac7319a61b216430347a24`,
   XMIN=22 / XMAX=70 / ZHI=80 / RBUF=24, LRU cap 1,600,000):
   census.txt (791,080 bytes, 3,920 rows + 80 blank separators,
   SHA-256
   `3275cc742e23f41a19a376a3057cfebf5073d9d84f8ef72ac029c05eaa541c53`,
   **not published in this edition**: reproduced via the generator +
   SHA pin, per the y=21 edition convention):
   **433,160 points**, zero-value points 216,626, engine states
   (LRU misses) 11,469,227 / hits 22,466,349, ~65 s; the tail assert
   `R>=x+z+23 => (x+22)%2` held on every row.
4. **Census parts PASS** (`C11ordered` / `C11canonical`,
   bounded-memoization twins of the verbatim raw engines, LRU cap
   1,600,000, separate commands): each engine **429,240 points bad 0**,
   merge corollary per engine 78,750 bad 0, tail per engine 3,920 bad 0;
   walls 22.6 s / 24.9 s;
   `output/census-ordered.json` (SHA-256
   `246506b2e4d11478376e9f0cb80a4fd8a59286ef9395c1a931f5c231c68da9dc`) /
   `output/census-canonical.json` (SHA-256
   `da0c20fcc8e3e791d219cb86cf4671a4565b45f1bd89a66110753c45ba068434`).
   The `C11` mode validates both parts fail-closed (engine field, box
   string `z=0..79, x=22..70, R=0..x+z+23`, cache cap, recomputed
   expected counts 429,240 / 78,750 / 3,920) and merges them.
5. **Staged 12-check battery PASS** (the declaration's stage before the
   full battery; kept as `output/audit-part1-12checks.json`, SHA-256
   `1d434dbd21e1c9b9ce5e00f3b4913c8240b1d9ef6d9df94cdc81932970999bab`):
   C1 26,220 / C1b 46,220 / C1d 134,550 / C2 242,305 / C2b 19,844 /
   C3 1,425 / C4 562,559 / C4t 562,559 (probe, not in bad) /
   C7 200,000 / C8 1,122,279 / C9 889,974 / C12 1,856,745;
   **total_points 5,664,680, total_bad 0**, types 797,559; wall 42.0 s.
   Merge corollary at this stage: 729,700 points bad 0; tail corollary
   183,318 points bad 0.
6. **Full 14-check battery PASS** (C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/
   C9/C11/C11r/C12 in one command, `output/audit.json`, SHA-256
   `41813df3ebfb80d812bb0cd61d3a74c86a3d2868d35c890240c7f0abacb9ac7a`):
   **total_points 6,956,320, total_bad 0, types 797,559** (the
   declared arithmetic: staged battery 5,664,680 + C11 858,480 + C11r
   433,160); C11 858,480 (both engines merged), C11r 433,160 over
   3,920 rows; C1d in-battery sweep 134,550 = anchors 125,442 +
   lowR 9,108; merge corollary **887,200 points bad 0**; tail
   corollary **191,158 points bad 0**; wall ~41.5 s per run.

Type-count series (final 14-check registry, clip 2y+2): y=14: 281,912 ->
y=15: 335,658 -> y=16: 394,686 -> y=17: 457,645 -> y=18: 523,398 ->
y=19: 590,877 -> y=20: 658,978 -> y=21: 727,229 -> **y=22: 797,559**.
The C4 in-box registered type count at clip 46 / sentinel 47 is 448,494
(succeeding the y=21 machine's 429,397 at clip 44; the declaration made
no advance numerical prediction here).

### C4t tightness probe: clip 45 has 280 confluence violations, first (60,108,108)

The clip window `2y+2 = 46` is **tight**, the 18th consecutive family
(y=5..22:
12/14/16/18/20/22/24/26/28/30/32/34/36/38/40/42/44/46), continuing the
pattern that the first violation walks with the band bottom (y=13: clip
27 (60,90,90); y=14: clip 29 (60,92,92); y=15: clip 31 (60,94,94);
y=16: clip 33 (60,96,96); y=17: clip 35 (60,98,98); y=18: clip 37
(60,100,100); y=19: clip 39 (60,102,102); y=20: clip 41 (60,104,104);
y=21: clip 43 (60,106,106); **y=22: clip 45 (60,108,108)**), the 10th
observation of the walking first-violation series -- exactly as
pre-registered in the declaration note (violations > 0 -> tight
confirmed; the declaration predicted both the >0 and the (60,108,108)
first violation, and the machine matched both).

## Honest record: declaration predictions vs. machine measurements

The declaration note pre-computed every check point count (C1 26,220 /
C1b 46,220 / C1d 134,550 / C2 242,305 / C2b 19,844 / C3 1,425 /
C4=C4t 562,559 / C7 200,000 / C8 1,122,279 / C9 889,974 / C11 858,480 /
C12 1,856,745), the C1d decomposition (anchors 125,442 + lowR 9,108),
the preflight boxes (12,012 + 9,108 = 21,120, per-z 1,885/1,911/1,937/
2,067/2,093/2,119), the census geometry (3,920 rows = 80*49, 429,240
points/engine, merge region 78,750/engine first non-empty at z=45, tail
3,920/engine), the C11r row/point counts (3,920 rows, 433,160 points),
the staged battery subtotal (5,664,680), the 14-check total (6,956,320),
the merge/tail corollary point counts (887,200 / 191,158), the C4t
first violation (280 > 0 violations at clip 45, first (60,108,108)) and
the C11r tail-flip probe count (3,920) with `predict_y22_counts.py`
(loop geometry only, no game evaluation), and cross-validated that
function against the published y=19, y=20 AND y=21 audits (all 14 check
counts and corollary counts of each machine audit reproduced exactly,
totals 6,941,913 / 6,947,960 / 6,952,761) BEFORE this machine ran.
**Every declared machine-computed prediction matched the measurement
exactly; no amendment was needed at any stage of this run** (in
particular no digit transposition recurred -- the declaration note was
written by machine-transcribing the predictor's stdout, per its own
honest-record section). The build of the machine itself went through
count-asserted builder corrections before any battery ran (local build
only, never published); all published bytes are the final builds.

## Determinism (4 byte-identical full audits)

run1 (canonical cwd) -> run2 (same-cwd rerun, fresh process) -> run3
(same-cwd second rerun; stdout byte-identical and audit.json rewritten
identically) -> run4 (isolated tree/cwd/HOME under `env -i`, PATH
pinned, `PYTHONHASHSEED=random`, with the FULL pipeline regenerated on
the isolated side: transcription check, preflight, census_rows.py, both
census parts, the staged 12-check battery, and the full 14-check
command; census_rows engine states reproduced exactly: misses
11,469,227 / hits 22,466,349).
`output/audit.json`, `census.txt`, `census-ordered.json`,
`census-canonical.json`, `preflight-c1d-y22.json`,
`transcriptions-check-y22.json`, `audit-part1-12checks.json` all
byte-identical across the runs (the isolated regeneration reproduces
every published byte from scratch; bytecode-cache hygiene applied:
`__pycache__` purged, PYTHONDONTWRITEBYTECODE=1).

## Fail-closed battery (12 probes, all caught; scratch tree only)

Exercised on a scratch copy of the canonical tree; the canonical tree's
published files were hash-verified after the whole battery and no
tampered byte was published:

1. census.txt missing: FAIL-CLOSED "census.txt is missing; run
   census_rows.py first", rc=1;
2. census.txt data-row deleted: FAIL-CLOSED "census rows 3919 != 3920",
   rc=1;
3. duplicate census-row injection: FAIL-CLOSED "duplicate census row
   (0,22)", rc=1;
4. census.txt P-set member tamper (first row): C11r bad 1, overall FAIL,
   rc=1;
5. census.txt T-set bogus-member injection (first row, `T={} ->
   T={5}`): C11r bad 1, overall FAIL, rc=1;
6. C11r tail flip `(x+22)` -> `(x+23)` on a tampered verifier copy:
   C11r bad 3,920 (every row; the declaration predicted exactly the
   row count), overall FAIL, rc=1;
7. anchor mis-binding `(17, A17u) -> (17, A10u)` on a tampered verifier
   copy: C1d bad 14,869, overall FAIL, rc=1;
8. low-R reference shift `R -> R+1` on a tampered verifier copy: C1d
   bad 9,108 (every low-R point independently mismatches, the exact
   low-R box size), overall FAIL, rc=1;
9. corollary merge boundary tamper `x<=z-23 -> x<=z-22` on a tampered
   verifier copy: merge corollary bad 59, overall FAIL, rc=1;
   honest record: the first probe issue was a no-op of the probe
   harness itself (the boundary edit did not take effect and the
   untouched copy ran PASS), re-issued with an effective tamper and
   caught immediately;
10. type-machine clip window tamper `CLIP, SENT = 46, 47 -> 44, 45`:
    C4 confluence violations, bad 945, overall FAIL, rc=1;
11. in_P22 tail parity flip (x%2==1 -> x%2==0; even-y type, x-odd tail)
    on a tampered verifier copy: C1 bad 4,898 / C2 bad 24,024, overall
    FAIL, rc=1;
12. in_P22 band parity tamper (off%2==0 -> off%2==1) on a tampered
    verifier copy: C1 bad 1,763 / C2 bad 24,451, overall FAIL, rc=1.

## Promotion decision

With the full 14-check audit PASS (6,956,320 comparison points, bad 0),
the fail-closed pre-verified C1d anchors, the independent
third-implementation census ledger consumed by C11r, 4 byte-identical
audit runs (3 same-cwd + 1 isolated, the isolated one a full pipeline
regeneration), and the fail-closed battery all caught (with the probe
(9) harness no-op recorded honestly), **K1256 is promoted observed ->
proved** (same K item, no new numbering, the
K1141/K1152/K1231/K1233/K1236/K1239/K1241/K1242/K1243/K1245/K1246/K1249/
K1255 precedent; the machine item is K1257). The corollaries are fixed
as universal claims in the same scope: the merge proposition's y=22
edition `x<=z-23 => H == single_token(x+22,z,R)` and the tail value
`R>=x+z+23 => H == (x+22)%2`, so **the merge proposition now holds
universally through y=1..22**. The B-child of the y=22 family is the
verbatim cand21 (K1248, proved), extending the B-child verbatim chain
to cand9..cand21 and the proved-B-child usage to cand10/cand12..cand21.
The two-token universal series is complete through y=22 (K1248 was the
y=21 endpoint; K1256 extends it by one family, the first beyond the
previously proved range).

Honest limitation record: unlike the y=21 edition, where a sibling
hourly execution independently rebuilt the machine and reproduced every
published byte on a second host, this publication is a single-host
publication; the declaration's pre-registered promotion condition
(overall PASS + bad 0 + byte-identical determinism runs + fail-closed
battery) was fully met on this host. A sibling-lane independent
reproduction (independent build from the published recipe + second-host
byte reproduction of the published outputs) remains open and is the
natural corroboration task for the next execution.

## Reproduction

```sh
cd research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123
python3 scripts/check_transcriptions_y22.py        # transcription byte-equality (repo-root discovery via AGENTS.md)
python3 scripts/preflight_c1d_y22.py               # C1d preflight gate (~5 s)
python3 census_rows.py                             # regenerate census.txt (~65 s; SHA pin above)
python3 verify_y22_universal.py C11ordered         # census part 1 (~23 s)
python3 verify_y22_universal.py C11canonical      # census part 2 (~25 s)
python3 verify_y22_universal.py                    # staged 12-check battery (~42 s, keep audit.json as audit-part1-12checks.json)
python3 verify_y22_universal.py C1 C1b C1d C2 C2b C3 C4 C4t C7 C8 C9 C11 C11r C12   # full 14-check battery (~42 s)
```

Note: the bare `verify_y22_universal.py` invocation (no arguments) runs
the STAGED 12-check battery only (C11/C11r excluded) in this edition;
the full 14-check battery always requires the explicit 14-check
argument list above (running `C11` alone only validates and merges the
census parts). census.txt is not part of the published edition:
regenerate it with `census_rows.py` and check the SHA-256 pin above
(C11r is FAIL-CLOSED if census.txt is missing).

## Interpretation

Same trust boundary as the y=5..y=21 machines: option decomposition +
closed-form mex identity + finite-type confluence over the
free-coordinate box, anchored to raw engines, to the proved y=21
family (K1248, the B-child, series-first proved B-child), and to the
x=22 multiset merger (21,22)==(22,21). Finite comparison is finite
observation; the machine's PASS is mechanical evidence for the universal
claim, and the 14-check audit (C1d published slice anchors at the y=22
rows + census_rows.py third-implementation ledger + C11r, plus
byte-identical determinism runs) is the basis on which K1256 has been
promoted observed -> proved in this dir. The standard 11x11 empty
board, the two-stone roots {49,60}/{59,60}, S2 {59,60} and classes
1/2/4 remain UNKNOWN and are unrelated to this family. Three or more
tokens, y>=23 families, fixed-width and q-point stabilization length
are out of scope.
