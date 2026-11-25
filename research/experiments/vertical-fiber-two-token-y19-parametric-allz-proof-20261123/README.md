# Vertical fiber: two-token y=19 parametric family, all-z universal verifier (single-edition 14-check machine)

Experiment dir: `vertical-fiber-two-token-y19-parametric-allz-proof-20261123`
Family: `H(R;(x,19);z)`, all `z >= 0`, all `x >= 19`, all `R >= 0`.
Claim under audit: K1243 (`cand19`, published fit, status **observed** at
machine-build time, **promoted proved by this run**) equals `H` everywhere,
with corollaries

- merge below the diagonal: `x <= z-20  =>  H == single_token(x+19,z,R)` (K0832),
- tail: `R >= x+z+20  =>  H == (x+19) % 2`.

Single-owner declaration note:
[2026-11-23-y19-universal-verifier-single-owner-note.md](../../log/2026-11-23-y19-universal-verifier-single-owner-note.md)
(commit `da6c1f5f`, observed HEAD-before-push `6f5419b5`, published BEFORE
the machine ran; no competing y=19 universal declaration existed then or at
publication). Under the declaration this machine is registered as the
**single-edition 14-check** variant of the published y=13..y=18
part1/part2 procedure: the verifier is built in full form (the part1-style
12 checks plus `C1d` published-slice anchors and the independent
census-ledger consumer `C11r`) from the start, and executed in stages --
transcription check -> C1d preflight gate -> census generation -> 12-check
battery (kept as `output/audit-part1-12checks.json`) -> full 14-check
battery (`output/audit.json`). On overall PASS with byte-identical
determinism runs and the fail-closed battery, the declaration promotes
K1243 observed -> proved (same K item, the
K1141/K1152/K1231/K1233/K1235/K1237/K1240/K1242 precedent); the machine
item is recorded as **K1245**.

## Machine composition (verify_y19_universal.py)

`verify_y19_universal.py` (52,631 bytes, SHA-256
`76525717875ceb6d7bc1f4e628cc95066a3591a134120ee4d1bf3743babd7294`,
single edition, 14 checks: C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/
C12) assembles three transcription blocks, each delimited by explicit
`# @@TRANSCRIPTION-*-START@@/END@@` markers and machine-verified against
the published bytes by `scripts/check_transcriptions_y19.py`
(SHA-256 `56a999bdf93fd93adda4aa8f373eb0f974fb915bef4d17c19e0c0b358175bb60`,
structural anchors, no line numbers):

- **engine block** (1,957 bytes): `mex` / `H_ordered` / `H_canonical` /
  `q_odd` / `single_token`, verbatim from the published
  `verify_y18_universal.py` part2 (commit `d29acbd8`, SHA-256
  `8ddd0c2f...`; provenance chain
  K1138/K1141/K1143/K1152/K1231/K1233/K1235/K1237/K1242 unchanged);
- **cand18 block** (3,307 bytes): the B-child of every y=19 point and the
  x=19 merger child value, verbatim from the published y=18 machine's
  `cand18` block with the block-local word-boundary rename `Y -> Y18`
  (two-source byte-equality: it equals BOTH the published
  `verify_y18_universal.py` cand18 block modulo the rename AND the
  published `cand18.py` of the K1242 fit experiment (commit `9e898f45`)
  modulo the rename; its universal proof is K1242, promoted proved by
  the K1244 machine; its y=19-scope usage (B-child x>=19 rows, A-child
  x=19 merger) is inside its published universal domain x >= 18);
- **cand19 block** (3,411 bytes): the claim under test, verbatim from the
  published `cand19.py` of the K1243 fit experiment (commit `eaea0f6a`),
  fit driver omitted.

Check result: `output/transcriptions-check-y19.json` -- engine equal,
cand18 two-source equal with the two published sources byte-agreeing,
cand19 equal, overall PASS (also re-run on the isolated determinism
tree).

Machine swaps relative to the published y=18 machine: merger row x==19
with A-child `cand18(z,19,R-1)` (multiset (18,19)==(19,18), the y=18
family x=19 row; the canonical-order treatment follows the y=14
confluence incident lesson, applied as in the y=18 machine), B-child
`cand18(z,x,R-1)`, C-child `1 xor cand19(z-1,x,R-1)`; clip window
`2y+2 = 40` / sentinel 41; census box `z=0..79, x=19..70,
R<=x+z+20` (80*52 = 4,160 rows, 436,800 points per engine); merge
`x<=z-20`; tail `(x+19)%2` at `R >= x+z+20`; C12 deep grid
`R<=x+z+21`; C8 keeps the x=18 rows as closed-form
extension-consistency rows only (no raw claim below x=19), exactly as
the x=17 rows did in the y=18 machine, and the deep-tail window check
uses the proved cand18 (K1242) tail claim `R>=x+z+19 => (x+18)%2` at
x>=18; C7 seed 20261192 (the y=15 seed 20261152 / y=16 seed 20261162 /
y=17 seed 20261172 / y=18 seed 20261182 series).

## Staged run results (all stages rc=0, all bad 0)

Executed in the declaration's pre-registered staged order on this host
(Linux x86_64, ~1.0 GiB cgroup class, the same class as the
y=15..y=18 census hosts); the wall times below are per stage.

1. **Transcription check PASS** (`scripts/check_transcriptions_y19.py`):
   engine 1,957 bytes / cand18 3,307 bytes (two-source, renamed) /
   cand19 3,411 bytes all equal, 0.06 s.
2. **C1d preflight gate PASS** (`scripts/preflight_c1d_y19.py`,
   SHA-256 `9bc154eedec94f43d558a16c24a519d71bf5768ab259a13ad4df694490f55421`):
   published fixed-z slice anchors (z0 in {8,9,10,15,16,17}, x=19..45,
   R=1..x+z0+30) 4-way checked
   (anchor x H_ordered x H_canonical x cand19): **12,069 points bad 0**
   (per z 1,890/1,917/1,944/2,079/2,106/2,133) + published low-R
   single-token reduction R<=z+6 (z0=15/16/17, x=19..159):
   **9,306 points bad 0**; wall 3.1 s;
   `output/preflight-c1d-y19.json` (SHA-256
   `1cfabdcf8d44269f9fe71de8c7b6414da2e0964db00ff4a14ae07118ca321e04`).
   The preflight anchor block is byte-verbatim from the published y=18
   preflight (itself the y=10/y=12 chain). The y=10 precedent (this gate
   caught a 170-point evaluation-order bug in the first K1087
   transcription) is why this stage exists; here the 4-way check agreed
   on the first run.
3. **Census ledger generation** (`census_rows.py`, third implementation
   y=19 edition, SHA-256
   `e4eed3960b9825440f45ded8b7f70c5fe7d430d2cd038ce56a742e8ae4a9086e`,
   XMIN=19 / XMAX=70 / RBUF=21 / ZHI=80, LRU cap 1,600,000):
   `output/census.txt` (809,842 bytes, 4,160 rows + 80 blank separators,
   SHA-256 `07213ab195eb958473d471aa25f1a36476aad0610569e059130b97e7a369656c`):
   **440,960 points**, zero-value points 219,556, engine states
   (LRU misses) 9,806,027, ~21 s; the tail assert
   `R>=x+z+20 => (x+19)%2` held on every row.
4. **Census parts PASS** (`C11ordered` / `C11canonical`,
   bounded-memoization twins of the verbatim raw engines, LRU cap
   1,600,000, separate commands): each engine **436,800 points bad 0**,
   merge corollary per engine 102,459 bad 0, tail per engine 4,160 bad 0;
   `output/census-ordered.json` (SHA-256
   `df767357477f8461ece22081dd29921d327b59d26a4d29509cd26137f3853b24`) /
   `output/census-canonical.json` (SHA-256
   `afdf9e607ea2215485d88c2b8dec808717283883c632fcc94e5102f254f769c8`).
   The `C11` mode validates both parts fail-closed (engine field, box
   string `z=0..79, x=19..70, R=0..x+z+20`, cache cap, recomputed
   expected counts 436,800 / 102,459 / 4,160) and merges them.
5. **Staged 12-check battery PASS** (the declaration's stage before the
   full battery; kept as `output/audit-part1-12checks.json`, SHA-256
   `636172413d227ece965595714807117fe017c32b6a4e97badd25e681cf09c846`):
   C1 24,510 / C1b 44,027 / C1d 136,206 / C2 229,663 / C2b 19,580 /
   C3 1,335 / C4 579,657 / C4t 579,657 (probe, not in bad) /
   C7 200,000 / C8 1,057,317 / C9 897,930 / C12 1,857,471;
   **total_points 5,627,353, total_bad 0**, types 590,877; wall 37.4 s.
   Merge corollary at this stage: 857,191 points bad 0; tail corollary
   184,200 points bad 0.
6. **Full 14-check battery PASS** (C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/
   C9/C11/C11r/C12 in one command, `output/audit.json`, SHA-256
   `59b6fded9fa3d0a153ba0949d5f770304c5a255e3cb0f43516050653ae7acd6a`):
   **total_points 6,941,913, total_bad 0, types 590,877** (the
   declared arithmetic: 12-check subtotal 6,364,747 + C1d 136,206 +
   C11r 440,960); C11 873,600 (both engines merged), C11r 440,960 over
   4,160 rows; merge corollary **1,062,109 points bad 0**; tail
   corollary **192,520 points bad 0**; wall 37.1 s.

Type-count series (final 14-check registry, clip 2y+2): y=14: 281,912 ->
y=15: 335,658 -> y=16: 394,686 -> y=17: 457,645 -> y=18: 523,398 ->
**y=19: 590,877**.

### C4t tightness probe: clip 39 has 770 confluence violations, first (60,102,102)

The clip window `2y+2 = 40` is **tight**, the 15th consecutive family
(y=5..19:
12/14/16/18/20/22/24/26/28/30/32/34/36/38/40), continuing the pattern
that the first violation walks with the band bottom (y=13: clip 27
(60,90,90); y=14: clip 29 (60,92,92); y=15: clip 31 (60,94,94);
y=16: clip 33 (60,96,96); y=17: clip 35 (60,98,98); y=18: clip 37
(60,100,100); **y=19: clip 39 (60,102,102)**), the 7th observation of
the walking first-violation series -- exactly as pre-registered in the
declaration note (violations > 0 -> tight confirmed; the declaration
predicted both the >0 and the (60,102,102) first violation, and the
machine matched both).

## Honest record: declaration predictions vs. machine measurements

The declaration note pre-computed every check point count, the
preflight boxes, the census geometry, the C11r row/point counts, the
12-check subtotal, the 14-check total, the C4t first violation and the
C11r tail-flip probe count with `predict_y19_counts.py` (loop geometry
only, no game evaluation), and cross-validated that function against
the published y=18 part2 audit (all 14 check counts of commit
`d29acbd8`'s audit reproduced exactly) BEFORE this machine ran. Every
single declared prediction matched the machine measurement exactly
(preflight 12,069 + 9,306; C1d 136,206 = 126,900 + 9,306; census
4,160 rows / 436,800 per engine / 102,459 merge per engine / 4,160 tail
per engine; C11r 440,960; 12-check subtotal 6,364,747; total
6,941,913; C4t violations > 0 with first (60,102,102)). Unlike the
y=18 part1 census-merge prediction slip (105,651 vs. the machine's
110,682), no amendment was needed at any stage of this run. The build
of the machine itself went through count-asserted builder corrections
before any battery ran (local build only, never published); all
published bytes are the final builds.

## Determinism (4 byte-identical full audits)

run1 (canonical cwd) -> run2 (same-cwd rerun, fresh process) ->
run3 (isolated tree/cwd/HOME under `env -i`, PATH pinned,
`PYTHONHASHSEED=random`, with the FULL pipeline regenerated on the
isolated side: transcription check, preflight, census_rows.py, both
census parts, and the full 14-check command) -> run4 (isolated-side
second full battery). `output/audit.json`, `census.txt`,
`census-ordered.json`, `census-canonical.json`,
`preflight-c1d-y19.json`, `transcriptions-check-y19.json` all
byte-identical across the runs (the isolated regeneration reproduces
every published byte from scratch).

## Fail-closed battery (12 probes, all caught; scratch tree only)

Exercised on a scratch copy of the canonical tree; the canonical tree's
outputs were byte-verified against the isolated regeneration afterwards
and no tampered byte was published:

1. census.txt missing: FAIL-CLOSED "census.txt is missing; run
   census_rows.py first", rc=1;
2. census.txt data-row deleted: FAIL-CLOSED "census rows 4159 != 4160",
   rc=1;
3. duplicate census-row injection: FAIL-CLOSED "duplicate census row
   (0,19)", rc=1;
4. census.txt P-set one-digit tamper: C11r bad 1, overall FAIL, rc=1;
5. census.txt T-set tamper: C11r bad 1, overall FAIL, rc=1;
6. C11r tail flip `(x+19)` -> `(x+20)` on a tampered verifier copy:
   C11r bad 4,160 (every row; the declaration predicted exactly the
   row count), overall FAIL, rc=1;
7. anchor mis-binding `(16, A16u) -> (16, A10u)` on a tampered verifier
   copy: C1d bad 1,743, overall FAIL, rc=1;
8. low-R reference shift `R -> R+1` on a tampered verifier copy: C1d
   bad 9,306 (every low-R point independently mismatches, the exact
   low-R box size), overall FAIL, rc=1;
9. corollary merge boundary tamper `x<=z-20 -> x<=z-19` on a tampered
   verifier copy: merge corollary bad > 0, overall FAIL, rc=1;
10. type-machine clip window tamper `CLIP, SENT = 40, 41 -> 38, 39`:
    C4 confluence violations, bad 2,520, overall FAIL, rc=1;
11. in_P19 tail parity flip (x even -> x odd) on a tampered verifier
    copy: C1 bad 2,449 / C2 bad 23,478 / tail corollary bad 11,466,
    overall FAIL, rc=1;
12. in_P19 band_base parity tamper on a tampered verifier copy: C1 bad
    935 / C2 bad 23,211, overall FAIL, rc=1.

Baseline bytes restored and cmp'd clean against the build bytes after
every probe.

## Promotion decision

With the full 14-check audit PASS (6,941,913 comparison points, bad 0),
the fail-closed pre-verified C1d anchors, the independent
third-implementation census ledger consumed by C11r, 4 byte-identical
audit runs (2 same-cwd + 2 isolated, one a full isolated regeneration),
and the fail-closed battery all caught, **K1243 is promoted observed ->
proved** (same K item, no new numbering, the
K1141/K1152/K1231/K1233/K1235/K1237/K1240/K1242 precedent; the machine
item is K1245). The corollaries are fixed as universal claims in the
same scope: the merge proposition's y=19 edition
`x<=z-20 => H == single_token(x+19,z,R)` and the tail value
`R>=x+z+20 => H == (x+19)%2`, so **the merge proposition now holds
universally through y=1..19**. The B-child of the y=19 family is the
verbatim cand18 (K1242, proved), extending the B-child verbatim chain
to cand9..cand18 and the proved-B-child usage to cand10/cand12..cand18.
The two-token universal series is complete through y=19 (K1242 existed
as the y=18 endpoint; K1243 extends it by one family).

## Reproduction

```sh
cd research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123
python3 scripts/check_transcriptions_y19.py        # transcription byte-equality (repo-root discovery via AGENTS.md)
python3 scripts/preflight_c1d_y19.py               # C1d preflight gate (~3 s)
python3 census_rows.py                             # regenerate output/census.txt (~21 s)
python3 verify_y19_universal.py C11ordered         # census part 1 (~19 s)
python3 verify_y19_universal.py C11canonical       # census part 2 (~22 s)
python3 verify_y19_universal.py C1 C1b C1d C2 C2b C3 C4 C4t C7 C8 C9 C11 C11r C12   # full 14-check battery (~37 s)
```

## Interpretation

Same trust boundary as the y=5..y=18 machines: option decomposition +
closed-form mex identity + finite-type confluence over the
free-coordinate box, anchored to raw engines, to the proved y=18
family (K1242, the B-child), and to the x=19 multiset merger
(18,19)==(19,18). Finite comparison is finite observation; the
machine's PASS is mechanical evidence for the universal claim, and the
14-check audit (C1d published slice anchors at the y=19 rows +
census_rows.py third-implementation ledger + C11r, plus byte-identical
determinism runs) is the basis on which K1243 has been promoted
observed -> proved in this dir. The standard 11x11 empty board, the
two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain
UNKNOWN and are unrelated to this family. Three or more tokens,
y>=20 families, fixed-width and q-point stabilization length are out
of scope.
