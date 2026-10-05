# N11 reply27 saved-result recovery

This record recovers, audits, and preserves saved exact results from failed GitHub Actions runs without recomputing them. The recorded runs are baseline cache run `37334644565`, shared s6 run `37336924568`, and completion86 run `37337141197`. This is an evidence-recovery record, not a new search result. By the time this record was prepared, `origin/main` had independently received equivalent cache recovery and an s6 normalization fix; the details here document this recovery's inputs and audit.

## Recovered evidence

- Baseline run `37334644565` supplied 2,529 canonical exact s5 results: 63 WIN and 2,466 LOSS. The saved model8 cache adds 8 new LOSS results (its 14 rows include 6 overlapping entries), and the 86-root completion run `37337141197` contributes 86 LOSS results over 361,568,619 reported nodes.
- Shared run `37336924568` contains 16 exact s6 results: 10 WIN, 6 LOSS, and 0 UNKNOWN. Its metadata has 66 parent-child relations across 65 candidate parents. Thirteen of the sixteen s6 metadata keys were noncanonical. The audit independently checked board safety, D4 normalization, and each parent relation by deleting one point from a safe s6 position and regenerating the geometry. Only the six LOSS results were used to derive 25 s5 LOSS witnesses.
- The merged cache contains 2,648 canonical exact s5 results: 63 WIN and 2,585 LOSS, with zero conflicts. The 86 replay rows were all LOSS; their count and total nodes were recomputed from the preserved raw shard CSVs and recorded in [recovery-receipt.json](output/recovery-receipt.json).
- The complete 105-child canonical s5 boundary of s4 class `(1297036692816953344, 0)` is LOSS, checked by `verify_reply27_loss_class_cache.py`.
- Under this finite cache, the 3,384 s4 classes classify as 129 WIN, 18 LOSS, and 3,237 UNKNOWN. The cache secures 72/119 root vertices, leaving 47. The minimum additional class cover is 13; a rational LP dual of 13 matches the integer optimum. The additive 13-class repair targets 1,227 distinct UNKNOWN s5 positions.

### Follow-up finite results

- A local cold run with six workers processed the 81 remaining s5 targets of the then-ranked class `(1298162592590594048, 0)`. It returned 76 LOSS, 5 UNKNOWN, and 0 WIN in 526,111,188 paid nodes. The five unresolved positions were retained as targets; no deeper solver run was made for them.
- Saved results from model-hard2 Actions run `37339663025` contain all 169 canonical s6 boundary positions, each WIN. The saved-raw-only audit independently matched the boundary and parent incidence (86 and 84 children), checked every replay position for safety, canonicality, and legality, and verified that both s5 parents are WIN. Each parent is a WIN child of s4 class `(1298162592590594048, 0)`, so either one certifies that class as WIN. The audited 169 replay verdicts are accepted as saved solver results; the audit independently checks their geometry, coverage, and parent propagation.
- The latest merged cache, after the local run and model-hard2 results, has 2,732 canonical exact s5 entries: 65 WIN, 2,667 LOSS, and zero conflicts. The post-model-hard2 cardinality result classifies 18 s4 classes LOSS, 131 WIN, and 3,235 UNKNOWN; it secures 72/119 root vertices and leaves 47. The minimum additional class cover remains 13 and matches the rational LP dual. Reoptimized 13-class repair has an UNKNOWN s5 union of 1,237 (additive objective 1,237); the initial 1,227 union applies only to the earlier 2,648-entry snapshot.
- The 100-child class `(1297036693756510208, 0)` is now completely LOSS. Its original 10 known children were joined by eight model8-selected LOSS results (19,867,831 nodes) and 82 additional LOSS results (301,036,761 nodes). `verify_reply27_loss_class_cache.py` checked that the cache contains the full 100-child canonical boundary and that its coverage is vertices 56, 64, 90, and 96.
- The latest cache, after this class completion, contains 2,822 canonical exact s5 entries: 65 WIN and 2,757 LOSS, with zero conflicts. The updated cardinality result has 19 LOSS, 131 WIN, and 3,234 UNKNOWN classes; 76/119 root vertices are secured, leaving 43. The minimum additional class cover is 12, matching the rational LP dual. The 12-class repair's additive and distinct UNKNOWN s5 union counts are both 1,147.
- Three of six separate cold residual mex cross-checks completed (120, 158, and 192 seconds). They are not adopted into the production cache; the cross-check set is incomplete.

These are finite cache and class results. Under the fixed first-player proposition, if s4 LOSS results cover all 119 third-move choices, then each s3 odd-stone AND node is LOSS and the s2 OR node `{60,27}` is LOSS. This establishes the refutation branch where the second player answers the central first move 60 with 27; it does not show that the empty root is a loss, because other first moves still require analysis. The 11x11 empty root and `{60,27}` outcome remain unresolved in the current record, and no terminal AND/OR proof is complete. The six evidence-recovery regression tests and 33 knowledge tests passed.

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

The `output/` files are the recovered normalized results, summaries, and raw shard evidence. The raw completion CSVs and shared-s6 CSVs preserve the saved replay rows used above; `raw/pre-recovery-s5.cache` and `raw/pre-recovery-stats.json` preserve the baseline cache and its run statistics. `recovery-receipt.json` records the initial source counts, verdicts, node totals, and digests. `local-completion81-summary.json`, `raw/local-completion81.csv`, `post-model-hard2-s5.cache`, `post-model-hard2-receipt.json`, `post-model-hard2-cardinality.json`, and `post-model-hard2-repair.json` record the follow-up finite results. The five unresolved s5 targets and their s6 boundary inputs were generated and preserved; no solver run was made for them. `model-hard2-independent-check.json` and `scripts/verify_model_hard2_results.py` preserve the saved-raw-only audit; the raw materialization metadata, boundary, four replay shards, and derived s5 cache are under `output/raw/`.

The prior next target `(1297036693756510208, 0)` has since been completed and verified LOSS as described above. Its preserved model8 ranking and reproduction commands below document target selection only; ranking scores are not win/loss evidence. A newer ranking is still in progress and is not recorded here.

The initial receipt records the 14-row model8 source at commit `d9040460`; that repository path later gained more rows. Its exact original bytes are preserved in `output/raw/pre-recovery-model8-s5.cache`, matching SHA-256 `bbaca07f1930e18228c210e17e560cd0f196db17eaf5251fea8c2d195b64f654`. Read the initial receipt against this snapshot when auditing that source, rather than the later appended source path.

### Reproduce the next-class model ranking

The preserved `next2-model8.csv` is an eight-position scheduling input for class `(1297036693756510208, 0)`. Recreate its structural features and ranking from the saved 2,238-row training cache and the 90-row unknown target list as follows. The temporary candidate-cache verdicts are placeholders used only by the feature extractor; model scores are not game verdicts.

```sh
mkdir -p /tmp/next2-model8
python - <<'PY'
import csv, json
from pathlib import Path

targets = Path("research/experiments/n11-boundary-recovery-20261006/output/post-model-hard2-best-class.csv")
rows = list(csv.reader(targets.open(newline="", encoding="utf-8")))
keys = [[int(row[3]), int(row[4])] for row in rows]
assert len(keys) == 90
with open("/tmp/next2-model8/candidates.cache", "w", encoding="utf-8") as f:
    f.write("# feature extraction placeholders only\n")
    for lo, hi in keys:
        f.write(f"s5verdict,{lo},{hi},5,2,0\n")
with open("/tmp/next2-model8/class-map.json", "w", encoding="utf-8") as f:
    json.dump({"classes": [{"key": [1297036693756510208, 0],
                              "unknown_children": keys}]}, f, indent=2)
    f.write("\n")
PY

c++ -std=c++20 -O3 -DNDEBUG \
  research/experiments/n11-literature-transfer-20261005/scripts/extract_s5_features.cpp \
  -o /tmp/next2-model8/extract_s5_features
/tmp/next2-model8/extract_s5_features \
  research/experiments/n11-boundary-recovery-20261006/output/raw/next2-model-training-s5.cache \
  > /tmp/next2-model8/train-features.csv
/tmp/next2-model8/extract_s5_features /tmp/next2-model8/candidates.cache \
  > /tmp/next2-model8/candidate-features.csv

uv run --no-project --with numpy --with scipy python \
  research/experiments/n11-literature-transfer-20261005/scripts/score_reply27_model_probes.py \
  --train /tmp/next2-model8/train-features.csv \
  --candidates /tmp/next2-model8/candidate-features.csv \
  --class-map /tmp/next2-model8/class-map.json --per-class 8 \
  --out /tmp/next2-model8/model8.json \
  --probes-out /tmp/next2-model8/model8.csv
cmp /tmp/next2-model8/model8.csv \
  research/experiments/n11-boundary-recovery-20261006/output/next2-model8.csv
```
