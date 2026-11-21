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