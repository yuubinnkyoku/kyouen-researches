# Reply=27 hard-s5 boundary closure

Date: 2026-10-05

**11×11 empty board remains UNKNOWN.**

This report records an exact sharded boundary proof for the fixed two-stone root
`{first=60, reply=27}`.  It concerns only nine difficult five-stone positions
left after the earlier 15M-node replay over the 2,262-target selected frontier.

## Boundary construction

`materialize_reply27_hard9_s6.py` regenerates the nine canonical s5 roots and
their complete legal canonical s6 boundary directly from board geometry.

- hard s5 roots: **9**
- distinct canonical s6 children: **816**
- distinct-parent multiplicity: **808×1 parent, 8×2 parents**

No outcome is assigned by the materializer.

## Exact proof

Workflow:

`.github/workflows/n11-hard9-s6-boundary-sharded.yml`

Observed successful run:

`37269759034` at head `93b7120afa`.

The 816 s6 roots were split into four independent shards and cold exact-replayed
with a 10M-node cap per root.  The verify job rejects conflicting duplicate
verdicts and reconstructs every parent s5 result from the complete canonical
boundary.

Exact s6 results:

- WIN: **729**
- LOSS: **81**
- UNKNOWN @10M: **6**
- total exact nodes: **901,901,494**
- verdict conflicts: **0**

The six unresolved s6 positions do not leave any parent s5 unresolved: every
parent containing one of them also has an exact LOSS child.

## Nine s5 results

At five stones the fixed first-player proposition is an AND node, so one LOSS
s6 child proves the s5 LOSS; if every canonical s6 child is WIN, the s5 is WIN.

| index | canonical s5 | children | WIN | LOSS | UNKNOWN | verdict |
|---:|---|---:|---:|---:|---:|---|
| 0 | `1152921504742115328:536870912` | 92 | 90 | 2 | 0 | LOSS |
| 1 | `3602879701897445376:134217728` | 89 | 85 | 4 | 0 | LOSS |
| 2 | `10520408729537478660:67108864` | 88 | 88 | 0 | 0 | **WIN** |
| 3 | `10520408729538527232:16384` | 94 | 79 | 15 | 0 | LOSS |
| 4 | `10520408729541689344:0` | 103 | 50 | 47 | 6 | LOSS |
| 5 | `10520408729554255872:32768` | 77 | 75 | 2 | 0 | LOSS |
| 6 | `10520408730615414784:0` | 100 | 99 | 1 | 0 | LOSS |
| 7 | `10520408730619609088:0` | 90 | 89 | 1 | 0 | LOSS |
| 8 | `10520408746717347840:8` | 91 | 82 | 9 | 0 | LOSS |

Therefore the nine difficult s5 roots are completely classified:

`LOSS 8 / WIN 1 / UNKNOWN 0`.

The derived cache is materialized as:

`research/experiments/n11-frontier-selection-20261005/output/reply27-hard9-s5.cache`

and can be regenerated from the archived workflow artifacts with
`derive_hard9_s5_cache.py`.

## Meaning for the selected 31-class frontier

Before this boundary solve, the completed 15M-node s5 replay had left seven
selected s4 classes unresolved because they contained these nine hard s5 roots.
The boundary result resolves those remaining child questions.  In particular,
the sole hard-s5 WIN is a decisive WIN witness for its parent s4 class; the
other eight hard s5 are exact LOSS material.

This result alone is **not** a proof that reply=27 is LOSS.  The original
31-class structural cover contains classes that were proved WIN and therefore
must be replaced by other classes.  The next step is a cache-aware repair cover
over all 3,384 canonical s4 classes.

## Verification boundary

The archived artifact `hard9-s6-boundary-proof` contains the four replay
outputs, four target shards, geometry metadata and `VERIFIED.txt`.  The verify
job checks:

1. exactly 816 expected canonical s6 keys are present;
2. no duplicate key has conflicting exact verdicts;
3. all nine parent child sets are reconstructed from the saved incidence map;
4. each s5 verdict follows only from exact child verdicts.

No pn/dn value, unfinished search count, or sampling rate is interpreted as a
game outcome.
