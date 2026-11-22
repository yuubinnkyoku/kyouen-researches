# n11 sixth-cost: third-implementation verdict re-verification (2026-11-21)

## What this is

A **third, independent implementation** (`third_impl.js`: non-df-pn AND/OR minimax with a
D4-canonical completion memo, slab TT of 2^22 entries) used for **verdict-level**
re-verification of sixth-cost k02 exclusive-probe row
`1297036692683751424:68157440` (5-stone, legal 87, corpus/fresh-replica WIN at
15M budget) plus its parked pair and the four legacy two-target-design replay rows.
This run is an alternative strengthening to the C++ second-implementation gate for the
owner's adoption decision. **It consumes or changes no corpus verdict. All
pre-existing gates are untouched. 11x11 empty-board remains UNKNOWN (no new claim).**

## Root cause of the earlier third-impl WIN->LOSS flips (fixed here)

The pre-fix third implementation agreed with the replica on every LOSS row but
returned LOSS on **all 158** WIN calibration rows. Cause: the kid-enumeration scratch
(`KID_IMG/KID_M/KID_CB/KID_CNT`) was a single global set. During a node's child
loop, the first child's `solve()` recursion ran its OWN grandkid enumeration into the
same global buffers, overwriting the images/canonical bases/move indices of every
not-yet-visited sibling. Sibling canonical keys were then computed from grandkid
leftovers, poisoning TT lookups/stores across the search. Because a LOSS proof needs
only one bad child (it fires early, often before deep recursion returns) while a WIN
proof must visit *every* child, the corruption systematically destroyed WIN proofs
while sparing LOSS proofs. The bug was in the verifier's memory management, never in
the game rules, legality, or value semantics.

Fix: per-depth (`stones`-indexed) kid scratch pools (`KIDPOOL`); plus two
replica-parity improvements (canonical-key child dedup; TT-status-first child
ordering) and a derived-down legal-mask pass (verified per node by `--verify-legal=1`
against a from-scratch `legalOf`). No rule or semantics change.

## Validation of the fixed implementation

- `verify_tbl.js`: forbidden-quad count 95,670 == replica `buildCompletionTable()`;
  195,044 random triples: my TBL danger set == replica `wob`, **0 mismatches**.
- `--verify-legal=1` witness runs (l1, k02): derived legal masks node-identical to
  from-scratch legality at every visited node.
- Determinism: every anchor row run 2-4x, identical `result/expansion/ttHits` counts.

## Witness results (all verdicts agree with the corpus / 15M replica)

| row (lo:hi, legal) | corpus/replica | third_impl (runs) | expansions | wall |
|---|---|---|---|---|
| k02 `1297036692683751424:68157440`, 87 | WIN | **WIN** x4 (a,b,g,v) | 9,106,337 | ~27-47s |
| parked-L `1297036830122704896:67108864`, 91 | LOSS | **LOSS** x2 | 26,488,700 | ~79s |
| parked-W `10376294091217440768:33554432`, 94 | WIN | **WIN** x2 | 37,613,359 | ~112s |
| legacy W1 `10376293541461626880:67109120`, 87 | WIN | **WIN** x3 (w1a,b,w1) | 11,663,909 | ~35s |
| legacy W2 `10376293541461626880:131328`, 80 | WIN | **WIN** x2 | 7,583,990 | ~22s |
| legacy W3 `10376293541461622792:65600`, 89 | WIN | **WIN** x2 | 10,898,228 | ~31s |
| legacy L `13019119616:16448`, 116 | LOSS | **LOSS** x2 | 7,660,602 | ~23s |

Negative controls (fail-closed input gates): `out/witness/out-ng1.txt` (declared legal
88 vs derived 87 -> GATE_FAIL), `out/witness/out-ng2.txt` (declared stones 6 ->
GATE_FAIL). Runlimit/depth-guard paths return result 0 (UNKNOWN), never a verdict.

## Bank re-calibration sample (probe-13 cache, 55s cap)

`out/bank-fixed-A/`: 16 rows completed, **14 agree, 0 disagree**, 2 inconclusive
(wall runlimit at 55s, recorded as result 0). A 12s-cap first pass (20 rows) was
fully inconclusive and is not counted as evidence; its files were superseded.
Full-band recalibration (140+ remaining rows at ~30-120s each) is deferred to
follow-up runs of this lane; the anchors above already cover the pre-registered scope.

## Honest constraints recorded

- Mid-session the sandbox environment was **reset** (work tree deleted). The script
  was rebuilt from the documented design and re-validated (quad count, 195k-triple
  table equality, and identical expansion counts on every witness row vs the
  pre-reset fixed runs, e.g. w1 11,663,909), proving semantic equivalence.
- The pre-reset session's bugged-impl calibration data (158/158 WIN flips) is
  **negative evidence about the fixed bug**, not about the corpus; the replica
  reproduced all four legacy rows and k02 independently (15M budget).
- Repo visibility: the repo was private/inaccessible to unauthenticated fetches
  during this session (404 on raw/api); publication used the GitHub App
  `push_files` path; byte-exact fetch-back verification was not possible while
  `get_file_contents` kept failing (known instability); MANIFEST.sha256 pins every
  published artifact instead.

## Reproduce

```
node third_impl.js --lo=1297036692683751424 --hi=68157440 --stones=5 --legal=87 \
  --row=k02 --cap=400000000 --wallcap=270 --memo-power=22
# third,k02,5,87,87,1,9106337,4991527,<wall>,...,clean,quads=95670,...
node verify_tbl.js          # replica-vs-mine triple table sweep
python3 run_bank.py <probe-13 cache> out/bank 240 --wins all --loss-sample 40 --wallcap 55
```

Requires Node.js; the pinned replica (`jsreplay.js`, sha256
`845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`) is referenced
from the lane kit, not modified.

## Bank full-band recalibration (2026-11-21 follow-up, same lane)

Declared in `research/log/2026-11-21-n11-thirdimpl-bank-full-recalibration-single-owner-note.md`
(commit `451e0fe8`). This closes the deferred first follow-up item of this lane:
the full-band calibration of the fixed third implementation against the published
probe-13 chain cache (`merged-exact-s5-after-js-probe-13.cache`, sha256
`60e0dc34...`, 5,756 s5verdict rows, stones 5).

- Bank set: all 158 WIN rows + a 40-row LOSS sample (`run_bank.py --wins all
  --loss-sample 40 --wallcap 90`). The 14 clean-agreed rows of `out/bank-fixed-A`
  were seed-copied (same fixed implementation; not re-proven); both sample
  wall-inconclusive rows resolved clean WIN here (58.99s / 54.71s); one row
  (`10448351135499550786_0`) needed an escalated 240s cap (94.11s clean WIN; its
  aborted 90s batch attempt is preserved as a comment inside its file).
- **Result: 198/198 rows agree verdict-level with the cache rows (158 WIN + 40
  LOSS sample). 0 disagreements, 0 gate fails, 0 unresolved rows.**
- Calibration before the batch (C1): `verify_tbl.js` 95,670 == replica 95,670
  quads and 195,044 triples with 0 mismatches; anchor w1
  `10376293541461626880:67109120` reproduced WIN(1) with expansions 11,663,909 /
  ttHits 6,284,843 / ttOverwrites 7,469,605, identical to the published
  fixed-implementation values on this host (33.80s wall).
- Determinism spot checks (fresh reruns): `10376293541461622792:65600` (WIN,
  10,898,228 / 5,964,726 / 6,703,924) and `13019119616:16448` (LOSS, 7,660,602 /
  3,951,175 / 3,466,722), byte-identical to the batch fields and to the published
  legacy witness values.
- Verdicts unconsumed, no cache increment, no class/coverage statement; the
  delegated C++ second-implementation gate is unchanged. Node/expansion counts are
  never read as verdicts. **The standard 11x11 empty board, the two-stone root
  {60,27}, and third moves {100,108} remain UNKNOWN.**

### Publication byte-fidelity audit and repair (same follow-up)

Unauthenticated raw fetches had been unavailable to the `ea73c3e3` session, whose
log left its MANIFEST pins "pending a later byte-exact fetch-back". Fetches work
again, so this session ran that deferred audit and found, honestly recorded:

1. Every text file pushed by that session lost exactly ONE trailing newline at
   publication (repo bytes end without the final `\n`; the MANIFEST pins and the
   canonical lane-kit copies end with it; the content is otherwise identical and
   the stripped byte is semantically inert for every format involved).
2. The per-file raw outputs were never pushed: `out/witness/*.txt` (18 files) and
   `out/bank-fixed-A/*.txt` (16 files) were claimed in the Artifacts section, but
   only the two concatenated summaries exist in the repo.

Repairs applied in this follow-up (all with byte-exact fetch-back): the five
non-README stripped files were re-published with the canonical kit bytes (restoring
the final newline so repo bytes equal the pre-existing MANIFEST pins); the 34
missing witness/bank-fixed-A raw files were published from the lane-kit canonical
copies after machine-verification against the pinned summary blocks line-for-line
(34/34 found verbatim in the pinned summaries); this README appendix was appended
(the README.md MANIFEST line is updated accordingly); and MANIFEST.sha256 was
regenerated to enumerate every published artifact of this experiment dir including
all raw rows.
