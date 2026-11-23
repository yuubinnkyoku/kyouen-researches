# Vertical fiber: two-token y=17 parametric family, all-z universal verifier (part 1 + part 2)

Experiment dir: `vertical-fiber-two-token-y17-parametric-allz-proof-20261123`
Family: `H(R;(x,17);z)`, all `z >= 0`, all `x >= 17`, all `R >= 0`.
Claim under audit: K1240 (`cand17`, published fit, status **observed** at
part-1 publication, **promoted proved by part 2**) equals `H` everywhere,
with corollaries

- merge below the diagonal: `x <= z-18  =>  H == single_token(x+17,z,R)` (K0832),
- tail: `R >= x+z+18  =>  H == (x+17) % 2`.

Single-owner declaration note:
[2026-11-23-y17-universal-verifier-single-owner-note.md](../../log/2026-11-23-y17-universal-verifier-single-owner-note.md)
(commit `b099a974`, observed HEAD `3efab5b9`, counter-declaration grep clean:
"y=17 universal" 0 commits, `verify_y17_universal` only fit-lane references,
proof experiment dir absent, K1241 free), published BEFORE the verifier run
(note blob `8cd9a627`, fetch-back byte-identical). Scope: part 1
(12 checks, commit `33e0a062`) + part 2 (C1d published-slice anchors +
census_rows.py third implementation + C11r), which promotes
K1240 observed -> proved on overall PASS. Part 2 is executed and
published in this same dir (same single-owner declaration continuation,
same procedure as the y=10/y=12/y=13/y=14/y=15/y=16 stages).

## Machine composition (verify_y17_universal.py)

`verify_y17_universal.py` (37,970 bytes, SHA-256 `2110ecbb...`, 956 lines,
12 checks) assembles three transcription blocks, each delimited by explicit
`# @@TRANSCRIPTION-*-START@@/END@@` markers and machine-verified against the
published bytes by `scripts/check_transcriptions_y17.py`
(SHA-256 `ac40c03c...`, structural anchors, no line numbers):

- **engine block** (1,957 bytes): `mex` / `H_ordered` / `H_canonical` /
  `q_odd` / `single_token`, verbatim from the published
  `verify_y16_universal.py` part2 (SHA-256 `bdf4fe04...`, commit `b706b214`;
  provenance chain K1138/K1141/K1143/K1152/K1231/K1233/K1235 unchanged);
- **cand16 block** (3,298 bytes): the B-child of every y=17 point and the
  x=17 merger child value, verbatim from the published y=16 machine's
  `cand16` block with the block-local word-boundary rename `Y -> Y16`
  (two-source byte-equality: it equals BOTH the published
  `verify_y16_universal.py` block modulo the rename AND the published
  `cand16.py` of the K1237 fit experiment modulo the rename; its universal
  proof is K1237; its y=17-scope usage (x >= 17 rows) is inside its
  published universal domain x >= 16);
- **cand17 block** (3,379 bytes): the claim under test, verbatim from the
  published `cand17.py` of the K1240 fit experiment (commit `6ca80e0e`),
  fit driver omitted.

No assembly/builder script is published (the y=13..y=16 part-2-style
procedure): the published ground truth of the transcription is the marker
check above, and every block is re-anchored against the raw engines by the
machine's own C1/C1b (engine and cand16) and C1 (cand17). Check result:
`output/transcriptions-check-y17.json` -- engine equal, cand16 two-source
equal, cand17 equal, overall PASS (also re-run on the isolated
determinism tree).

Machine swaps relative to the published y=16 machine: merger row x==17 with
A-child `cand16(z,17,R-1)` (multiset (16,17)==(17,16), the y=16 family x=17
row), B-child `cand16(z,x,R-1)`, C-child `1 xor cand17(z-1,x,R-1)`;
clip window `2y+2 = 36` / sentinel 37; census box `z=0..79, x=17..70,
R<=x+z+18` (80*54 = 4,320 rows, 440,640 points per engine); merge
`x<=z-18`; tail `(x+17)%2` at `R >= x+z+18`; C12 deep grid `R<=x+z+19`;
C8 keeps the x=16 rows as closed-form extension-consistency rows only
(no raw claim below x=17), exactly as the x=15 rows did in the y=16
machine, and the deep-tail window check uses the proved cand16 (K1237)
tail claim `R>=x+z+17 => (x+16)%2` at x>=16; C7 seed 20261172 (the
y=14 seed 20261142 / y=15 seed 20261152 / y=16 seed 20261162 series).

## Part 1 results (overall PASS, 3 byte-identical runs)

12 checks (C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12):
total comparison points **6,343,825**, total bad **0**, types **457,645**
(type-count series clip 28/30/32/34 -> 36:
y=13: 234,180 -> y=14: 281,912 -> y=15: 335,658 -> y=16: 394,686 ->
y=17: 457,645). Per-check: C1 23,370 / C1b 42,565 / C2 221,235 /
C2b 19,404 / C3 1,275 / C4 590,634 / C4t 590,634 (probe, not in bad) /
C7 200,000 / C8 1,014,174 / C9 903,114 / C11 881,280 / C12 1,856,140.

Corollaries: merge `x<=z-18 => H == single_token(x+17,z,R)` at 1,182,632
points bad 0 (first full raw-engine anchoring of the y=17 merge region -
the y=17 probe box is the third consecutive family with zero in-box merge
rows; the census box first contains merge rows at z=35, per the
declaration prediction); tail `R>=x+z+18 => H == (x+17)%2` at 193,096
points bad 0. In-check corollary counts: C2 merge 11,340 + tail 54,782;
census 119,025 + 4,320 per engine.

C4t tightness probe: clip 35 (2y+1) has **1,300 confluence violations,
first (60,98,98)** - so the clip window `2y+2 = 36` is **tight**, the 13th
consecutive family (y=5..17:
12/14/16/18/20/22/24/26/28/30/32/34/36), continuing the pattern that the
first violation walks with the band bottom (y=13: clip 27 (60,90,90);
y=14: clip 29 (60,92,92); y=15: clip 31 (60,94,94); y=16: clip 33
(60,96,96); y=17: clip 35 (60,98,98)), exactly as pre-registered in the
declaration note.

## C11 census: bounded-memoization twins

Same design as y=12..y=16 (this host is a ~1.0 GiB cgroup machine, the
same class as the y=15/y=16 census hosts): each raw engine runs as its own
command (`C11ordered` / `C11canonical`, ~17 s each) through a
bounded-memoization twin (the published engine's own code object rebound
into a shallow copy of the module globals, LRU cap 1,600,000; memoization
of a deterministic pure function is transparent and LRU eviction is
deterministic under the fixed census visit order). Box `z=0..79,
x=17..70, R=0..x+z+18` (54 x-rows per z): 440,640 points per engine,
bad 0; merge corollary 119,025 points bad 0; tail corollary 4,320 points
(one R per row) bad 0. The `C11` mode validates both part files
fail-closed (engine field, box string, cache cap, recomputed expected
counts 440,640 / 119,025 / 4,320) and merges them.

## Honest record: the "obvious" merger tamper is NOT a bug (extension-consistency observation)

The part-1 fail-closed battery (below) includes a merger-row tamper probe
designed as `A = cand17(z,16,R-1)` (the y=17 formula's below-domain row).
This tamper produced **bad 0 on the whole C2 grid**: the y=17 closed form
evaluated at its x=16 extension row coincides with the y=16 family's
x=17 row over the entire audited grid. This is expected rather than
miraculous: both rows describe the same multiset {16,17}
((16,17)==(17,16)), all table features are (S=x+y, d, o, parity)-
parametric, and both give S=33 with identical merge/tail/pin laws shifted
one family. We record it as an honest extension-consistency observation
(the property C8 relies on for its x=16 identity rows), and we replaced
the probe with the genuine canonical-order bug `A = cand16(z,16,R-1)`
(the y=16 family's x=16 row, multiset {16,16}), which IS caught (see
below).

## Determinism and fail-closed (part 1)

Three runs of the full 12-check battery (each regenerating both census
parts first), byte-identical across `output/audit.json`
(SHA-256 `301f7690...`), `output/census-ordered.json`
(`12234496...`), `output/census-canonical.json` (`1ca205a5...`):
run 1 and run 2 in the same cwd (fresh processes), run 3 on an isolated
tree/cwd/HOME under `env -i` with `PYTHONHASHSEED=random` (transcription
check also re-run PASS on the isolated side). No clock, fixed seed,
sorted audit keys.

Fail-closed battery (each on a scratch copy, then publication tree
byte-verified untouched):

- T1 cand17 block Y constant 17 -> 16: C1 bad **1,243**, rc=1 (caught);
- T2 in_T17 z-odd pin mod-4 class 0 -> 2: C1 bad **28**, rc=1 (caught);
- T5b genuine x=17 merger canonical-order bug `A = cand16(z,16,R-1)`
  (multiset {16,16}): C2 bad **2,209**, rc=1 (caught);
- T5 as-designed `A = cand17(z,16,R-1)` (same multiset): bad 0 - recorded
  as the extension-consistency observation above, not a machine defect;
- T3 census part points 440,640 -> 440,641: FAIL-CLOSED
  `census points 440641 != 440640`, rc=1 (caught);
- T4 census-canonical.json removed: FAIL-CLOSED missing-part message,
  rc=1 (caught).

## Part 2: C1d published-slice anchors + census_rows.py consumer (2026-11-23 added; promotes K1240 observed -> proved)

The promotion stage left open by part 1, executed with the same procedure
that promoted the y=10/y=12/y=13/y=14/y=15/y=16 machines
(K1141/K1152/K1231/K1233/K1235/K1237, K1239 part1/part2). The C1d anchor
block (anchor functions A8u..A17u) is the published y=16 part-2 canonical
verifier's anchor block **verbatim** (commit `b706b214`, SHA-256
`bdf4fe04...`; its universal proof domain covers the y=17 rows reached
here; its own chain runs back through the y=15/y=14/y=12 machines to the
y=10 part2 verifier and the published z-slice verifiers), with only the
provenance header rewritten from the y=17 preflight measurements
(12,789/9,438, cand17).

### C1d (published fixed-z slice anchors at the y=17 rows: 137,280 points, bad 0)

`scripts/preflight_c1d_y17.py` (SHA-256 `fc1d4ec0...`, generated from the
published y=16 preflight with count-asserted y=17 scan constants)
fail-closed pre-verification BEFORE the machine body ran: the published
uniform closed forms (z=8: K0999/K1000, z=9: K1001, z=10: K1011,
z=15/16/17: K1065/K1077/K1087) 4-way checked
(anchor x H_ordered x H_canonical x cand17) on z0 in {8,9,10,15,16,17},
x=17..45, R=1..x+z0+30: **12,789 points bad 0** (per z: 2,001 / 2,030 /
2,059 / 2,204 / 2,233 / 2,262), plus the published low-R single-token
reduction R<=z+6 on the z0=15/16/17 y=17 rows
(cand17 vs single_token(x+17,z0,R)): **9,438 points bad 0**; wall ~3 s;
2 runs byte-identical (one on the isolated side);
`output/preflight-c1d-y17.json` (SHA-256 `c8e0e0a9...`; the file is the
pretty-printed canonical byte, stdout is the same JSON compacted).
The y=10 precedent (this stage caught a 170-point evaluation-order bug in
the first K1087 transcription) is why this stage exists; here the anchors
are a verbatim re-transcription, and the 4-way check agreed on the first
run. Machine C1d then sweeps 6 z0 x x=17..159 x R=1..x+61 (**127,842
points**) plus the lowR rows (9,438): total **137,280, bad 0**.

### C11r (independent census ledger consumer: 444,960 points, bad 0, fail-closed)

`census_rows.py` (the third implementation; y=17 edition, SHA-256
`1188bcd1...`) writes `output/census.txt` (817,882 bytes, 4,320 rows + 80
blank separators, SHA-256 `597370b4...`): z=0..79, x=17..70, per-row
Thue-Morse index, value-2 support T, value-1 support P (explicit R lists)
and tail flag: **444,960 points**, zero-value points 221,578, engine states
(LRU misses) 8,725,227, LRU cap 1,600,000 explicit (the memory-capped-host
adaptation, mirroring the published y=12..y=16 editions on the same
class of host); the tail assert `R>=x+z+18 => (x+17)%2` held on every
row. Wall ~18 s. C11r re-derives every row from cand17 and compares idx/
T/P/tail (duplicate or missing rows, rows != 80*54 = 4,320, missing
trailing newline are FAIL-CLOSED): 444,960 points **bad 0**, 4,320 rows.

### Part-2 full audit (14 checks, overall PASS, total_points 6,926,065, bad 0)

C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12 in one command: C1d
137,280 and C11r 444,960 added to part 1's 6,343,825:
total_points **6,926,065**, total_bad **0**, types **457,645**. Merge
corollary 1,182,632 and tail 193,096 unchanged, bad 0. C4t consistent
with part 1 (1,300 violations at clip 35, first (60,98,98)). Wall 35.4 s
(run 1); the C11ordered/C11canonical parts rerun in the part-2 session
reproduce the part-1 published bytes (`12244496...`/`1ca205a5...`).
`output/audit.json` (part-2 stage wording, SHA-256 `fd4b7d8c...`) is the
canonical audit of record; `verify_y17_universal.py` is now the part-2
edition (SHA-256 `4253cf29...`), whose part-1 twelve check bodies are
byte-invariant against the published part-1 byte (diff-verified: only the
anchor block, check_C1d/check_C11r, the STAGE docstring and the main()
registry/dispatch changed).

### Part-2 determinism (3 runs byte-identical) and fail-closed (6 probes)

run1 (same cwd) -> run2 (same-cwd rerun) -> run3 (isolated tree/cwd/HOME +
`env -i` with pinned PATH + `PYTHONHASHSEED=random`, transcription
check, preflight, census_rows.py and BOTH census parts regenerated on the
isolated side): audit.json, census.txt, census-ordered.json,
census-canonical.json, preflight-c1d-y17.json,
transcriptions-check-y17.json all byte-identical; census.txt
byte-identical across 2 census_rows.py runs (1 main-tree + 1 isolated).

Fail-closed exercised on a scratch tree, all caught before publication:
(1) census part points tamper 440,640 -> 440,641 (FAIL-CLOSED), (2) census
canonical part missing (FAIL-CLOSED), (3) corollary merge bound tamper
x<=z-18 -> x<=z-17 (fake C2 on a tampered verifier copy: merge bad 176,
overall FAIL, rc=1), (4) census.txt P-set one-digit tamper (C11r bad 1,
FAIL, no PASS output), (5) census.txt missing (FAIL-CLOSED), (6)
census.txt duplicate-row injection (FAIL-CLOSED "duplicate census row
(0,17)"). Baseline bytes restored and cmp'd clean after every probe; the
canonical-tree outputs were byte-verified against the isolated
regeneration afterwards and no tampered byte was published.

### Promotion decision

With the full 14-check audit PASS, the fail-closed pre-verified C1d
anchors, the independent third-implementation census (C11r), and three
byte-identical audit runs (2 same-cwd + 1 isolated regeneration),
**K1240 is promoted observed -> proved**
(same K item, no new numbering, the K1141/K1152/K1231/K1233/K1235/K1237
precedent). The corollaries are fixed as universal claims in the same
scope: the merge proposition's y=17 edition `x<=z-18 => H ==
single_token(x+17,z,R)` and the tail value `R>=x+z+18 => H == (x+17)%2`,
so the merge proposition now holds universally through y=1..17. The
B-child of the y=17 family is the verbatim cand16 (K1237, proved),
extending the B-child verbatim chain to cand9..cand16 and the
proved-B-child usage to cand10/cand12..cand16.

## Reproduction

```sh
cd research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123
python3 scripts/check_transcriptions_y17.py        # transcription byte-equality (repo-root discovery via AGENTS.md)
python3 scripts/preflight_c1d_y17.py               # C1d preflight (~3 s)
python3 census_rows.py                             # third-implementation census (~18 s)
python3 verify_y17_universal.py C11ordered         # census part 1 (~17 s)
python3 verify_y17_universal.py C11canonical       # census part 2 (~17 s)
python3 verify_y17_universal.py C1 C1b C1d C2 C2b C3 C4 C4t C7 C8 C9 C11 C11r C12   # full part-2 (~35 s)
```

## Interpretation

Same trust boundary as the y=5..y=16 machines: option decomposition +
closed-form mex identity + finite-type confluence over the free-coordinate
box, anchored to raw engines, to the proved y=16 family (K1237, the
B-child), and to the x=17 multiset merger. Finite comparison is finite
observation; the machine's PASS is mechanical evidence for the universal
claim, and the part-2 stage (C1d published slice anchors at the y=17
rows + census_rows.py third-implementation ledger + C11r, plus three
byte-identical audit runs) is the basis on which K1240 is promoted
observed -> proved in this dir. The standard 11x11 empty board, the
two-stone roots
{49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain UNKNOWN and are
unrelated to this family. Three or more tokens, y>=18 families, fixed-width
and q-point stabilization length are out of scope.
