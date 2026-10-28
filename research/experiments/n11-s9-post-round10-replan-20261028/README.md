# N11 round10: certificate-only 83-edge candidate replan

The previous fixed conditional 14-root frontier has **548** S8 edges,
of which **465** are secured by independent terminal evidence and **83**
remain unproved. These are conditional obligations, not a new two-stone
or empty-board verdict.

`replan.js` does not run a large root search. It independently replays
the fixed round10 S9 certificate with 3×3 and 4×4 integer geometry,
including forged-witness rejection, checks the round9/round10 hash
chain and the fixed WIN8 lift, and reconstructs the previous 890 eligible
S9 classes from the existing round7 inventory. It derives the complete
canonical S9-parent closure of round10's LOSS10 witnesses and excludes
all round10 selected/now-proved S9 classes. It also discards candidates
that no longer touch any of the 83 unproved S8 edges, then performs
deterministic incidence-dominance pruning and bounded greedy/exchange
selection for at most 32 S9 classes.

Run from repository root:

```sh
node research/experiments/n11-s9-post-round10-replan-20261028/replan.js
```

The [bounded workflow](https://github.com/yuubinnkyoku/kyouen-researches/actions/workflows/n11-s9-post-round10-replan.yml)
has a 15-minute limit and publishes the exact JSON result as an artifact.
Once a result is independently confirmed, freeze it in `next-plan.json`.
The script will then reject any subsequent mismatch against that file.
No terminal verdict is inferred from potential coverage or incomplete
search statistics.

**Standard 11×11 empty-board winner: UNKNOWN.**

## Frozen result (independently verified)

[CI run 40670592328](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40670592328)
**PASS**. The round10 certificate has 8 WIN9 and 24 LOSS9; 231 terminal
leaves were checked under each integer geometry. Of the previous **890**
eligible S9 classes, **41** are removed by certified round10 results
(including 9 extra LOSS9 parents), and **140** no longer touch any of the
83 outstanding S8 edges. Thus **709** remain, of which **96** survive
incidence-dominance pruning. The next **32** candidates have **40**
potential S8 hits and **822** legal S10 children.

The exact ordered selection and SHA-256 are frozen in `next-plan.json`.
Future runs check this file against a complete reconstruction. This
reduces redundant future exploration; it does not establish any new
S8 WIN or close a two-stone root.

## Independent next-batch preflight

[CI 40671305642](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40671305642)
**PASS**. `audit_next_batch.js` checks the complete legal-child boundary
and reverse incidences under two independent integer geometries and
rejects altered or duplicate selections. The 32 chosen roots have
**822 ordered S10 children and 822 distinct S10 classes**; their
**288 S8 reverse incidences are also all distinct**. Thus within-batch
S10 terminal cache sharing saves **zero** leaves if all are visited.
The fixed counts are in `preflight.json`. Cross-batch reuse and
first-LOSS9 short-circuiting are not included in this measurement.
