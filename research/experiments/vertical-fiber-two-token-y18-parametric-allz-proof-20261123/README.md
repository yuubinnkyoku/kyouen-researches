# Vertical fiber: two-token y=18 parametric family, all-z universal verifier (part 1 + part 2)

Experiment dir: `vertical-fiber-two-token-y18-parametric-allz-proof-20261123`
Family: `H(R;(x,18);z)`, all `z >= 0`, all `x >= 18`, all `R >= 0`.
Claim under audit: K1242 (`cand18`, published fit, status **observed** at
part-1 publication, **promoted proved by part 2**) equals `H` everywhere, with corollaries

- merge below the diagonal: `x <= z-19  =>  H == single_token(x+18,z,R)` (K0832),
- tail: `R >= x+z+19  =>  H == (x+18) % 2`.

Single-owner declaration note:
[2026-11-23-y18-universal-verifier-single-owner-note.md](../../log/2026-11-23-y18-universal-verifier-single-owner-note.md)
(commit `1d46f883`, observed HEAD `c15b1c3f`, published BEFORE the verifier
run; the y=19 fit lane had declared a separate universal for y=19 only),
published BEFORE the verifier run. Scope: part 1
(12 checks, this commit) + part 2 (C1d published-slice anchors +
census_rows.py third implementation + C11r), which promotes
K1242 observed -> proved on overall PASS. Part 2 is executed and
published in this same dir (same single-owner declaration continuation,
same procedure as the y=10/y=12/y=13/y=14/y=15/y=16/y=17 stages).

## Machine composition (verify_y18_universal.py)

`verify_y18_universal.py` (38,212 bytes, SHA-256 `14373419...`, 961 lines,
12 checks) assembles three transcription blocks, each delimited by explicit
`# @@TRANSCRIPTION-*-START@@/END@@` markers and machine-verified against the
published bytes by `scripts/check_transcriptions_y18.py`
(SHA-256 `80fc9c31...`, structural anchors, no line numbers; the published
machines carry @@TRANSCRIPTION markers since y=17, so the published-y=17-side
extractions cut at the END marker lines):

- **engine block** (1,957 bytes): `mex` / `H_ordered` / `H_canonical` /
  `q_odd` / `single_token`, verbatim from the published
  `verify_y17_universal.py` part2 (SHA-256 `4253cf29...`, commit `ab23d120`;
  provenance chain K1138/K1141/K1143/K1152/K1231/K1233/K1235/K1237
  unchanged);
- **cand17 block** (3,465 bytes): the B-child of every y=18 point and the
  x=18 merger child value, verbatim from the published y=17 machine's
  `cand17` block with the block-local word-boundary rename `Y -> Y17`
  (two-source byte-equality: it equals BOTH the published
  `verify_y17_universal.py` cand17 block modulo the rename AND the published
  `cand17.py` of the K1240 fit experiment (commit `6ca80e0e`) modulo the
  rename; its universal proof is K1240, promoted proved by the K1241
  part1/part2 machine; its y=18-scope usage (x >= 18 rows) is inside its
  published universal domain x >= 17);
- **cand18 block** (3,211 bytes): the claim under test, verbatim from the
  published `cand18.py` of the K1242 fit experiment (commit `9e898f45`),
  fit driver omitted.

No assembly/builder script is published (the y=13..y=17 procedure): the
published ground truth of the transcription is the marker check above, and
every block is re-anchored against the raw engines by the machine's own
C1/C1b (engine and cand17) and C1 (cand18). Check result:
`output/transcriptions-check-y18.json` -- engine equal, cand17 two-source
equal and the two sources byte-agree, cand18 equal, overall PASS (also
re-run on the isolated determinism tree).

Machine swaps relative to the published y=17 machine: merger row x==18 with
A-child `cand17(z,18,R-1)` (multiset (17,18)==(18,17), the y=17 family
x=18 row), B-child `cand17(z,x,R-1)`, C-child `1 xor cand18(z-1,x,R-1)`;
clip window `2y+2 = 38` / sentinel 39; census box `z=0..79, x=18..70,
R<=x+z+19` (80*53 = 4,240 rows, 438,840 points per engine); merge
`x<=z-19`; tail `(x+18)%2` at `R >= x+z+19`; C12 deep grid `R<=x+z+20`;
C8 keeps the x=17 rows as closed-form extension-consistency rows only
(no raw claim below x=18), exactly as the x=16 rows did in the y=17
machine, and the deep-tail window check uses the proved cand17 (K1240)
tail claim `R>=x+z+18 => (x+17)%2` at x>=17; C7 seed 20261182 (the
y=14 seed 20261142 / y=15 seed 20261152 / y=16 seed 20261162 / y=17
seed 20261172 series).

## Part 1 results (overall PASS, 3 byte-identical runs)

12 checks (C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12):
total comparison points **6,354,790**, total bad **0**, types **523,398**
(type-count series (final 12-check registry): y=14: 281,912 ->
y=15: 335,658 -> y=16: 394,686 -> y=17: 457,645 -> y=18: 523,398).
Per-check: C1 23,940 / C1b 43,296 / C2 225,449 / C2b 19,492 / C3 1,305 /
C4 585,189 / C4t 585,189 (probe, not in bad) / C7 200,000 /
C8 1,035,729 / C9 900,534 / C11 877,680 / C12 1,856,987.

Corollaries: merge `x<=z-19 => H == single_token(x+18,z,R)` at 1,121,822
points bad 0 (the census merge rows are first non-empty at z=37, the 4th
consecutive family whose probe box contained zero merge rows; per the
declaration, the in-box merge coverage starts at z>=37 census rows and
the C2/C7/C8/C9/C12 sweeps cover the region beyond); tail
`R>=x+z+19 => H == (x+18)%2` at 192,210 points bad 0. In-check corollary
counts: C2 merge 8,580 + tail 54,782; census 110,682 + 4,240 per engine.

C4t tightness probe: clip 37 (2y+1) has **1,012 confluence violations,
first (60,100,100)** - so the clip window `2y+2 = 38` is **tight**, the
14th consecutive family (y=5..18:
12/14/16/18/20/22/24/26/28/30/32/34/36/38), continuing the pattern that the
first violation walks with the band bottom (y=13: clip 27 (60,90,90);
y=14: clip 29 (60,92,92); y=15: clip 31 (60,94,94); y=16: clip 33
(60,96,96); y=17: clip 35 (60,98,98); y=18: clip 37 (60,100,100)), the
6th observation of the walking first-violation, exactly as pre-registered
in the declaration note (violations > 0 -> tight confirmed).

## C11 census: bounded-memoization twins

Same design as y=12..y=17 (this host is a ~1.0 GiB cgroup machine, the
same class as the y=15/y=16/y=17 census hosts): each raw engine runs as
its own command (`C11ordered` / `C11canonical`, ~19 s each) through a
bounded-memoization twin (the published engine's own code object rebound
into a shallow copy of the module globals, LRU cap 1,600,000;
memoization of a deterministic pure function is transparent and LRU
eviction is deterministic under the fixed census visit order). Box
`z=0..79, x=18..70, R=0..x+z+19` (53 x-rows per z): 438,840 points per
engine, bad 0; merge corollary 110,682 points bad 0; tail corollary 4,240
points (one R per row) bad 0. The `C11` mode validates both part files
fail-closed (engine field, box string, cache cap, recomputed expected
counts 438,840 / 110,682 / 4,240) and merges them.

Honest record: the declaration note's precomputed census merge corollary
per-engine prediction was 105,651 (an arithmetic slip in the declaration
note's own precomputation); the machine's independently recomputed
formula value **110,682** governs, matches both census parts, and is the
value carried in `output/census-*.json` and the audit. Every other
declared prediction (all eleven check point counts, the part-1 total
6,354,790, the census per-engine points 438,840, the tail row counts
4,240, the C1d/preflight boxes for part 2) matched exactly.

## Honest record: the assembled-machine region-splice defect (caught before publication)

The first assembled build of this machine (pinned-source builder, run
locally, never published) had a region-splice off-by-one: after inserting
the new B-child (cand17) block, the candidate-region cut point was
searched from the head of the file and hit the B-child's newly inserted
CAND17-END marker, leaving the template's old cand17 candidate region in
place AFTER the new cand18 block. The old region's module-level `Y = 17`
then reassigned the global `Y`, so the transcribed cand18 tables evaluated
with Y=17 (every feature shifted by one family). The machine's own C1
caught it immediately: 1,229 of 23,940 points mismatched, with mismatch
signature exactly one family shift (pins at `z+2Y+1` with Y=17 instead of
`z+2Y+1` with Y=18, etc.). Fixed in the builder (marker-position-anchored
cut + structural uniqueness asserts: each transcription marker exactly
once, exactly one module-level `Y =` assignment, closed-form definition
counts, helper redefinition counts 3/2/2). The transcription checker
passed both before and after (its first-marker extraction was correct in
both states), which is why the builder now also asserts marker
uniqueness. Published bytes are the fixed build; no defective byte
reached publication, and the census/audit/fail-closed batteries below
were all run on the fixed build only.

## Determinism and fail-closed (part 1)

Three runs of the full 12-check battery (each regenerating both census
parts first), byte-identical across `output/audit.json`
(SHA-256 `c090be81...`), `output/census-ordered.json`
(`af284ab7...`), `output/census-canonical.json`
(`9c817177...`): run 1 and run 2 in the same cwd (fresh processes),
run 3 on an isolated tree/cwd/HOME under `env -i` with
`PYTHONHASHSEED=random`, with the transcription check AND both census
parts regenerated on the isolated side (all byte-identical). No clock,
fixed seed, sorted audit keys.

Fail-closed battery (each on a scratch copy, then publication tree
byte-verified untouched; 9 probes, all caught or honestly accounted):

- T1 census-ordered.json box field tamper `R<=x+z+19` -> `R<=x+z+18`:
  FAIL-CLOSED "census part box mismatch", rc=1 (caught);
- T2 census-canonical.json removed: FAIL-CLOSED missing-part message,
  rc=1 (caught);
- T3 cand18 band bottom tamper `2 * Y + 2` -> `2 * Y` (in the candidate
  block): C2 bad > 0, overall FAIL, rc=1 (caught);
- T4 cand18 z-even steady pin tamper `z + 2 * Y + 1` -> `z + 2 * Y - 1`:
  C2 bad > 0, overall FAIL, rc=1 (caught);
- T5 corollary merge boundary tamper `x <= z - 19` -> `x <= z - 18`:
  merge corollary bad > 0, overall FAIL, rc=1 (caught);
- T6 type machine clip window tamper `CLIP, SENT = 38, 39` -> `36, 37`:
  C4 confluence violations > 0, overall FAIL, rc=1 (caught);
- T7 C1b merger multiset tamper `(18,17)` -> `(18,16)`: C1b bad > 0,
  overall FAIL, rc=1 (caught);
- T8 opts18 merger-row A-child tamper `cand17(z,18,R-1)` ->
  `cand18(z,18,R-1)`: C3/C2 bad > 0, overall FAIL, rc=1 (caught);
- T9 deep-tail window boundary probe, as designed
  `(x+z+19, x+z+20, x+z+21)` -> `(x+z+18, ...)`: bad 0 -- recorded as an
  extension-consistency observation, not a machine defect: the window
  point `R = x+z+18` lies INSIDE the published cand17 (K1240, proved)
  tail claim `R>=x+z+18 => (x+17)%2`, so consistency at 18 is exactly
  what the proved family predicts; shifting the window to the true
  boundary outside the claim, `(x+z+17, ...)`, IS caught (40 bad, rc=1).

## Part 2: C1d published-slice anchors + census_rows.py consumer (2026-11-23 added; promotes K1242 observed -> proved)

The promotion stage left open by part 1 (pre-declared in the
single-owner note), executed with the same procedure that promoted the
y=10/y=12/y=13/y=14/y=15/y=16/y=17 machines
(K1141/K1152/K1231/K1233/K1235/K1237/K1240). The C1d anchor block (anchor
functions A8u..A17u) is the published y=17 part-2 canonical verifier's
anchor block **verbatim** (commit `ab23d120`, SHA-256 `4253cf29...`; its
universal proof domain covers the y=18 rows reached here; its own chain
runs back through the y=16/y=15/y=14/y=12 machines to the y=10 part2
verifier and the published z-slice verifiers), with only the provenance
header rewritten from the y=18 preflight measurements (12,432/9,372,
cand18).

### C1d (published fixed-z slice anchors at the y=18 rows: 136,746 points, bad 0)

`scripts/preflight_c1d_y18.py` (SHA-256 `1d21c6ab...`, generated from
the published y=17 preflight with count-asserted y=18 scan constants)
fail-closed pre-verification BEFORE the machine body ran: the published
uniform closed forms (z=8: K0999/K1000, z=9: K1001, z=10: K1011,
z=15/16/17: K1065/K1077/K1087) 4-way checked
(anchor x H_ordered x H_canonical x cand18) on z0 in {8,9,10,15,16,17},
x=18..45, R=1..x+z0+30: **12,432 points bad 0** (per z: 1,946 / 1,974 /
2,002 / 2,142 / 2,170 / 2,198), plus the published low-R single-token
reduction R<=z+6 on the z0=15/16/17 y=18 rows
(cand18 vs single_token(x+18,z0,R)): **9,372 points bad 0**; wall ~3 s;
3 runs byte-identical (2 same-cwd + 1 isolated regeneration);
`output/preflight-c1d-y18.json` (SHA-256 `89cb9541...`; the file is the
pretty-printed canonical byte, stdout is the same JSON compacted). The
y=10 precedent (this stage caught a 170-point evaluation-order bug in
the first K1087 transcription) is why this stage exists; here the
anchors are a verbatim re-transcription, and the 4-way check agreed on
the first run. Machine C1d then sweeps 6 z0 x x=18..159 x R=1..x+61
(**127,374 points**) plus the lowR rows (9,372): total **136,746, bad 0**.

### C11r (independent census ledger consumer: 443,080 points, bad 0, fail-closed)

`census_rows.py` (the third implementation; y=18 edition, SHA-256
`1cd71004...`) writes `output/census.txt` (810,453 bytes, 4,240 rows + 80
blank separators, SHA-256 `8e239f52...`): z=0..79, x=18..70, per-row
Thue-Morse index, value-2 support T, value-1 support P (explicit R lists)
and tail flag: **443,080 points**, zero-value points 221,548, engine states
(LRU misses) 9,262,827, LRU cap 1,600,000 explicit (the memory-capped-host
adaptation, mirroring the published y=12..y=17 editions on the same class
of host); the tail assert `R>=x+z+19 => (x+18)%2` held on every row. Wall
~18 s. C11r re-derives every row from cand18 and compares idx/T/P/tail
(duplicate or missing rows, rows != 80*53 = 4,240, missing trailing
newline are FAIL-CLOSED): 443,080 points **bad 0**, 4,240 rows.

### Part-2 full audit (14 checks, overall PASS, total_points 6,934,616, bad 0)

C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12 in one command: C1d
136,746 and C11r 443,080 added to part 1's 6,354,790: total_points
**6,934,616**, total_bad **0**, types **523,398**. Merge corollary
1,121,822 and tail 192,210 unchanged, bad 0. C4t consistent with part 1
(1,012 violations at clip 37, first (60,100,100)). Wall 36.1 s (run 1);
the C11ordered/C11canonical parts rerun in the part-2 session reproduce
the part-1 published bytes (`af284ab7...`/`9c817177...`).
`output/audit.json` (part-2 stage wording, SHA-256 `a636c187...`) is the
canonical audit of record; `verify_y18_universal.py` is now the part-2
edition (52,177 bytes, SHA-256 `8ddd0c2f...`), whose part-1 twelve check
bodies are byte-invariant against the published part-1 byte
(diff-verified: only the anchor block, check_C1d/check_C11r, the STAGE
docstring, the C1b/C1d/C11r docstring lines and the main() registry/
dispatch changed).

### Part-2 determinism (3 runs byte-identical) and fail-closed (8 probes)

run1 (same cwd) -> run2 (same-cwd rerun) -> run3 (isolated tree/cwd/HOME
+ `env -i` with pinned PATH + `PYTHONHASHSEED=random`, transcription
check, preflight, census_rows.py and BOTH census parts regenerated on
the isolated side): audit.json, census.txt, census-ordered.json,
census-canonical.json, preflight-c1d-y18.json,
transcriptions-check-y18.json all byte-identical.

Fail-closed exercised on a scratch tree, all caught before publication:
(1) census.txt missing (FAIL-CLOSED "census.txt is missing; run
census_rows.py first", rc=1), (2) census.txt data-row deleted
(FAIL-CLOSED "census rows 4239 != 4240", rc=1), (3) duplicate census-row
injection (FAIL-CLOSED "duplicate census row (0,18)", rc=1), (4)
census.txt P-set one-digit tamper (C11r bad 1, FAIL, rc=1), (5)
census.txt T-set tamper (C11r bad 1, FAIL, rc=1), (6) C11r tail flip
(x+18)->(x+19) on a tampered verifier copy (C11r bad 4,240 = every row,
FAIL, rc=1), (7) anchor mis-binding (16, A16u) -> (16, A10u) on a
tampered verifier copy (C1d bad 1,756, FAIL, rc=1), (8) low-R reference
shift R -> R+1 (C1d bad 9,372 = every low-R point independently
mismatches, FAIL, rc=1). Baseline bytes restored and cmp'd clean against
the build bytes after every probe; the canonical-tree outputs were
byte-verified against the isolated regeneration afterwards and no
tampered byte was published.

### Promotion decision

With the full 14-check audit PASS, the fail-closed pre-verified C1d
anchors, the independent third-implementation census (C11r), and three
byte-identical audit runs (2 same-cwd + 1 isolated regeneration),
**K1242 is promoted observed -> proved** (same K item, no new numbering,
the K1141/K1152/K1231/K1233/K1235/K1237/K1240 precedent). The corollaries
are fixed as universal claims in the same scope: the merge proposition's
y=18 edition `x<=z-19 => H == single_token(x+18,z,R)` and the tail value
`R>=x+z+19 => H == (x+18)%2`, so the merge proposition now holds
universally through y=1..18. The B-child of the y=18 family is the
verbatim cand17 (K1240, proved), extending the B-child verbatim chain to
cand9..cand17 and the proved-B-child usage to cand10/cand12..cand17.


## Reproduction

```sh
cd research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123
python3 scripts/check_transcriptions_y18.py        # transcription byte-equality (repo-root discovery via AGENTS.md)
python3 scripts/preflight_c1d_y18.py               # C1d preflight gate (part 2, ~3 s)
python3 census_rows.py                             # regenerate output/census.txt (~18 s)
python3 verify_y18_universal.py C11ordered         # census part 1 (~19 s)
python3 verify_y18_universal.py C11canonical       # census part 2 (~19 s)
python3 verify_y18_universal.py C1 C1b C1d C2 C2b C3 C4 C4t C7 C8 C9 C11 C11r C12   # full part-2 (~36 s)
```

## Interpretation

Same trust boundary as the y=5..y=17 machines: option decomposition +
closed-form mex identity + finite-type confluence over the free-coordinate
box, anchored to raw engines, to the proved y=17 family (K1240, the
B-child), and to the x=18 multiset merger (17,18)==(18,17). Finite
comparison is finite observation; the machine's PASS is mechanical
evidence for the universal claim, and the part-2 stage (C1d published
slice anchors at the y=18 rows + census_rows.py third-implementation
ledger + C11r, plus three byte-identical audit runs) is the basis on
which K1242 has been promoted observed -> proved in this dir. The standard
11x11 empty board, the two-stone roots {49,60}/{59,60}, S2 {59,60} and
classes 1/2/4 remain UNKNOWN and are unrelated to this family. Three or
more tokens, y>=19 families, fixed-width and q-point stabilization length
are out of scope.
