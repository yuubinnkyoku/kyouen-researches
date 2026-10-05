# N11 reply27 saved-result recovery

This record recovers, audits, and preserves saved exact results from failed GitHub Actions runs without recomputing them. The recorded runs are baseline cache run `37334644565`, shared s6 run `37336924568`, and completion86 run `37337141197`. This is an evidence-recovery record, not a new search result. By the time this record was prepared, `origin/main` had independently received equivalent cache recovery and an s6 normalization fix; the details here document this recovery's inputs and audit.

## Recovered evidence

- Baseline run `37334644565` supplied 2,529 canonical exact s5 results: 63 WIN and 2,466 LOSS. The saved model8 cache adds 8 new LOSS results (its 14 rows include 6 overlapping entries), and the 86-root completion run `37337141197` contributes 86 LOSS results over 361,568,619 reported nodes.
- Shared run `37336924568` contains 16 exact s6 results: 10 WIN, 6 LOSS, and 0 UNKNOWN. Its metadata has 66 parent-child relations across 65 candidate parents. Thirteen of the sixteen s6 metadata keys were noncanonical. The audit independently checked board safety, D4 normalization, and each parent relation by deleting one point from a safe s6 position and regenerating the geometry. Only the six LOSS results were used to derive 25 s5 LOSS witnesses.
- The merged cache contains 2,648 canonical exact s5 results: 63 WIN and 2,585 LOSS, with zero conflicts. The 86 replay rows were all LOSS; their count and total nodes were recomputed from the preserved raw shard CSVs and recorded in [recovery-receipt.json](output/recovery-receipt.json).
- The complete 105-child canonical s5 boundary of s4 class `(1297036692816953344, 0)` is LOSS, checked by `verify_reply27_loss_class_cache.py`.
- Under this finite cache, the 3,384 s4 classes classify as 129 WIN, 18 LOSS, and 3,237 UNKNOWN. The cache secures 72/119 root vertices, leaving 47. The minimum additional class cover is 13; a rational LP dual of 13 matches the integer optimum. The additive 13-class repair targets 1,227 distinct UNKNOWN s5 positions.

These computations do not prove an UNKNOWN class to be LOSS. The 11x11 empty root and the `{60,27}` root remain UNKNOWN, and a terminal AND/OR proof is incomplete. The 13-class cover is a minimum target schedule under the supplied cache, not a solved-game certificate. The six evidence-recovery regression tests and 33 knowledge tests passed. A separate cold replay with residual mex cross-checks is ongoing; this recovery record does not claim it has completed.

## Reproduction from the preserved files

Run from the repository root. The recovery merge and geometry checks use the Python standard library. Only the cardinality and repair optimization scripts require SciPy; install it in the active environment with `uv pip install scipy` before those steps.

First derive s5 witnesses from the saved shared-s6 shards, checking their metadata against geometry:

```sh
python research/experiments/n11-frontier-selection-20261005/scripts/derive_shared_s6_witness_cache.py \
  --meta research/experiments/n11-frontier-selection-20261005/output/reply27-current-shared16-s6.json \
  --replay 'research/experiments/n11-boundary-recovery-20261006/output/raw/shared-s6-*.csv' \
  --cache-out /tmp/shared-s6-derived-s5.cache \
  --summary-out /tmp/shared-s6-summary.json
```

Merge the baseline, model8, derived witnesses, and saved completion replay rows. The merger checks canonical safe keys and rejects conflicts:

```sh
python research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py \
  --cache research/experiments/n11-boundary-recovery-20261006/output/raw/pre-recovery-s5.cache \
  --cache research/experiments/n11-frontier-selection-20261005/output/reply27-best-class-model8-s5.cache \
  --cache research/experiments/n11-boundary-recovery-20261006/output/shared-s6-derived-s5.cache \
  --replay 'research/experiments/n11-boundary-recovery-20261006/output/raw/completion86-*.csv' \
  --out /tmp/reply27-current-s5.cache \
  --summary-out /tmp/recovery-receipt.json
```

Verify the completed class and compute the cache-aware frontier and repair:

```sh
python research/experiments/n11-frontier-selection-20261005/scripts/verify_reply27_loss_class_cache.py \
  --class-lo 1297036692816953344 --class-hi 0 --expected-children 105 \
  --cache research/experiments/n11-boundary-recovery-20261006/output/reply27-class-1297036692816953344-0-s5.cache

python research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py \
  --s5-cache /tmp/reply27-current-s5.cache \
  --out /tmp/recovered-cardinality.json

python research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py \
  --extra-s5-cache /tmp/reply27-current-s5.cache \
  --out /tmp/recovered-repair.json \
  --targets-out /tmp/recovered-repair-targets.csv
```

## Preserved files

The `output/` files are the recovered normalized results, summaries, and raw shard evidence. The raw completion CSVs and shared-s6 CSVs preserve the saved replay rows used above; `raw/pre-recovery-s5.cache` and `raw/pre-recovery-stats.json` preserve the baseline cache and its run statistics. `recovery-receipt.json` records per-source row counts, verdicts, node totals, and SHA-256 digests.
