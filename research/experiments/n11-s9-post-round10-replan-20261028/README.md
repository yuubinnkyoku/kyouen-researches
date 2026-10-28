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
