# n11 ultra-cheap one-unknown batch stage-1 sweep: single-owner declaration

**Declaration (publish-then-execute).** This lane declares single-owner
execution of the four published one-unknown ultra-cheap S5 keys
(the class-completion candidates of kit
`research/experiments/n11-ultra-cheap-class-census-20261127`, run json
sha256 `a60716ac...`, whose legal/geometry facts were dual-implementation
pre-derived in kit `research/experiments/n11-ultra-cheap-legal-precheck-20261127`,
run json sha256 `89fd85ac...`).  As of this declaration, the latest main
(checked at commit `f4e65734`, 2026-11-27T19:28:42Z; an earlier check at
`6bf68e4b`, 19:26:31Z, found the same) contains no claim of these keys:
the census kit machine-checked them absent from all fifteen claim sets
(focus 35, cert 38, third 39, fourth 41, fifth 44, sixth 43, seventh 42,
eighth 43, ninth 45, tenth 44, eleventh 46, twelfth 51, sbd 101,
parked 2, parked 4) and the 2-entry quarantine registry, and no later
commit claims them.

## Batch definition

Canonical head of record basis: `1e2eeda2...` (eleventh-cost k01 adoption,
6,890 rows WIN 208 / LOSS 6,682).  Runner: Node.js replica
`jsreplay.js`, byte-clone of the published pin
`845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
(tenth-cost kit lineage), `--n=11 --memo=22 --only=5`, cold solver per row,
no shared TT.

Probe order (class_index ascending, per the legal-precheck table):

| key id | class_index | S5 key (lo:hi) | legal | s5_index |
|---|---|---|---|---|
| u01 | 1849 | 1153485622925590528:0 | 88 | 81011 |
| u02 | 2251 | 1297036830121656320:131074 | 80 | 93815 |
| u03 | 16371 | 1153202979851993088:272 | 78 | 550879 |
| u04 | 23101 | 1152921505747697664:1032 | 85 | 745184 |

## Protocol (eleventh-batch template `n11-eleventhcost-batch-stage1-2m-20261127`)

1. Stage-1 sweep: each key u01..u04 at `--exact-replay-budget=2000000`,
   two cold passes (p1/p2) per key, node-identity required.
2. Escalation (only for keys still UNKNOWN at 2M): `--exact-replay-budget=15000000`
   two cold passes per key, executed in declared order u01..u04 with the
   standing WIN-stopping rule active: the first key that resolves WIN(1)
   suppresses the 15M escalation of the remaining keys (they stay
   UNKNOWN at 2M; parking/L50M only under a future declaration).
   LOSS(2) resolutions do not stop the ladder.
3. No other key is run at any budget in this Part.  The twelfth-cost
   sweep (single-owner declaration `f6d29d16`) is not touched.

## Pre-declaration calibration (disclosed)

One 50,000-budget cold run of u01 was executed before this declaration
for mechanical sanity only: `replay,0,5,88,0,50000,0,50000` —
result 0 (INDET), no verdict information, legal count 88 derived by the
runner and matched the input row (fail-closed on mismatch).  No other
pre-declaration run of any batch key exists.

## Publication note (disclosed)

The first wave-A push attempt raced a parallel session's commit
(the GitHub API returned "Reference cannot be updated" against a main
head that moved 6bf68e4b -> f4e65734 during the attempt); the identical
payload was re-pushed against the fresh head.  No content changed.

## Pillar policy

All rows produced here are single-implementation.  Any WIN row requires
the C++ second-implementation scrutiny gate and third-implementation
corroboration (separate Parts) before adoption; a LOSS row requires the
same standing pillars before canonical adoption.  A resolved key would
complete its class (Board-verified free_now at adoption time), but
nothing is adopted by this Part: the verdict is NOT consumed, no class
closure is claimed, nodes are bookkeeping and never evidence of WIN or
LOSS.

## Meaning and non-meaning

The standard 11x11 empty board: UNKNOWN.  All 19 central-reply roots:
UNKNOWN.  The two-stone root {60,27} and its remaining third moves
100/108: UNKNOWN.  All closure classes: UNKNOWN.

This lane runs without access to the user's computer (scheduled task);
publication via the GitHub API only.
