# Part AW: closure class 23101 batch-14 residual 10 keys q043..q052 exact-S5 probe (2026-11-22)

Part AW (single-owner, declared before execution as note amendment commit
`da131f10`). Batch-14 (Part AQ takeover) halted at its pre-registered
WIN-HALT rule on q042 (2-pass node-exact WIN, 9,149,084 nodes), leaving the
last 10 keys q043..q052 unprobed. Part AT/AS/AU resumes list them as the open
closure item for rank-1 class 23101. This experiment enumerates them.

## Scope and non-contact

- Part AV (batch-17 class 10661 adoption + reaudit, declaration commit
  `340abef3`) is in flight under its own declaration: this Part touches no
  batch-17 artifact, no canonical cache, no refresh output.
- Verdict consumption: ZERO. No row is consumed into the canonical cache
  here (LOSS adoption is a separately declared adoption Part, Part AS/AV
  style, based on the post-AV 6,172-row canonical base).
- The 15 unconsumed closure WINs (b018/d002/e002/f017/g018/j033/h045/z003/
  n005/n006/p002/p003/r001/r002/q042) stay unconsumed; the q042 adoption
  decision stays with the scrutiny owner (C++ second implementation gate
  pin `9193f5b6...`).

## Machine gates (`scripts/make_residual_keys.py`, 3 runs byte-identical)

- G1 batch-14 batch-keys.json sha `dfde0e90...` holds exactly q001..q052 of
  class 23101 (mask `[1152921504892059648, 16]`).
- G2 residual ids == {q043..q052}, probe_order 580..589, s5_index set ==
  {745455..745457, 745459..745465}; the unadopted q042 WIN s5 745184 is not
  in the set.
- G3 every input CSV byte-equals the published batch-14 file (per-file sha
  pins from the batch-14 MANIFEST, publication commit `7b211d38`) and its
  (lo,hi,legal) agree with the batch-keys row.
- G4 canonical 6,120-row cache sha `be9cb24e...`: 0/10 hits.
- G5 quarantine registry sha `81d23160...`: 0/10 hits.
- G6 batch-17 batch-keys sha `db762175...` (class 10661, 52 keys): s5_index
  intersection with the residual set is empty.
- G7 published batch-14 status.log probed set == {q001..q042} (with the
  `q042 WIN-HALT` stop row) and the published batch-14 row-audit records
  `unprobed_keys == [q043..q052]` - the residual set is exactly the
  published key-set complement.

Outputs: `input/batch-keys.json` (10 keys, sha256 `d4fada68...`) and
`input/residual-keys-manifest.json` (sha256 `d2cb3322...`).

## Execute

- Pinned replica `scripts/jsreplay.js` sha256 `84585617...` (byte-copy of the
  published replica). 2-pass fresh cold, budget 15,000,000, 1 solver / 1
  row / 1 process, worker max 2.
- val-gate (run on this host BEFORE the first probe, 4/4 node-exact vs the
  published two-target-design anchors): at2m 0/2,000,000 x2, 15m
  `(2, 3651923)` / `(2, 5040200)`, forbidden quadruples 95670.
- Stop rules (pre-registered): determinism mismatch -> HARD-STOP rc=42;
  exhaustion -> honest UNKNOWN (no same-condition re-probe); WIN -> honest
  `WIN-CONTINUE` label and the batch CONTINUES, verdict NOT consumed (Part AW
  deviation from batch-14/16/17, declared: the class 23101 all-LOSS closure
  route is already refuted by the published q042 WIN, so halting buys no
  route information and full enumeration minimizes the class unknown count
  on every branch).
- Honesty record: execution drove `runbatch.sh` in 2-key parallel foreground
  pairs (worker 2) rather than through the `runwave.sh` wrapper; the wave
  wrapper (published here, same protocol) was not needed at this size. No
  host interruption occurred in this run (zero truncated passes), so the
  truncation guard in runbatch.sh never fired.

## Results

**10/10 keys LOSS (result 2), WIN 0, exhaustion 0, mismatch 0.** All rows
2-pass fresh-cold node-exact. Total nodes 23,252,550/pass (range 557,594 ..
8,353,244).

| key | s5_index | result | nodes |
|-----|----------|--------|-------|
| q043 | 745455 | 2 | 2,573,254 |
| q044 | 745456 | 2 | 1,855,550 |
| q045 | 745457 | 2 | 1,028,674 |
| q046 | 745459 | 2 | 1,101,099 |
| q047 | 745460 | 2 | 557,594 |
| q048 | 745461 | 2 | 2,860,377 |
| q049 | 745462 | 2 | 8,353,244 |
| q050 | 745463 | 2 | 2,178,945 |
| q051 | 745464 | 2 | 1,451,266 |
| q052 | 745465 | 2 | 1,292,547 |

`output/row-audit.json` (schema
`n11-centralreply-closure-class23101-batch14residual-rowaudit-v1`, sha256
`6b40b131...`) re-verifies every row mechanically from the raws: both
passes carry `# replay_done`, p1==p2 node-exact on all fields, within
budget, result 2, input/batch-keys/status agreement. 3 runs byte-identical.

## Interpretation guard

Route statement only, no closure/coverage/secured claim here: the batch-14
key set of class 23101 is now fully enumerated on this lane's evidence
(42 rows published by Part AQ + 10 rows here), every q-row resolved except
the unconsumed q042 WIN. Nothing is consumed into the canonical cache by
this Part, and class 23101's canonical classification is unchanged until a
separately declared adoption Part merges the 10 LOSS rows (on the post-AV
canonical base). The standard 11x11 empty board, the 19 central-reply
roots, class 23101 and all 10 keys remain UNKNOWN at every point of this
experiment. Nodes are bookkeeping, never verdicts.
