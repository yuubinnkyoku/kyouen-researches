# N11 reply27 saved-result recovery

This experiment records saved-result recovery and audit, followed by local finite searches and cache-conditioned frontier calculations. The initial recovery stage preserved exact results from failed GitHub Actions runs without recomputing them; by then `origin/main` had independently received equivalent cache recovery and an s6 normalization fix. Later local finite searches, saved s6 reverse propagation, and frontier calculations are recorded with their replay inputs and receipts; none completes the empty-board terminal proof.

## Recovered evidence

- Baseline run `37334644565` supplied 2,529 canonical exact s5 results: 63 WIN and 2,466 LOSS. The saved model8 cache adds 8 new LOSS results (its 14 rows include 6 overlapping entries), and the 86-root completion run `37337141197` contributes 86 LOSS results over 361,568,619 reported nodes.
- Shared run `37336924568` contains 16 exact s6 results: 10 WIN, 6 LOSS, and 0 UNKNOWN. Its metadata has 66 parent-child relations across 65 candidate parents. Thirteen of the sixteen s6 metadata keys were noncanonical. The audit independently checked board safety, D4 normalization, and each parent relation by deleting one point from a safe s6 position and regenerating the geometry. Only the six LOSS results were used to derive 25 s5 LOSS witnesses.
- The merged cache contains 2,648 canonical exact s5 results: 63 WIN and 2,585 LOSS, with zero conflicts. The 86 replay rows were all LOSS; their count and total nodes were recomputed from the preserved raw shard CSVs and recorded in [recovery-receipt.json](output/recovery-receipt.json).
- The complete 105-child canonical s5 boundary of s4 class `(1297036692816953344, 0)` is LOSS, checked by `verify_reply27_loss_class_cache.py`.
- Under this finite cache, the 3,384 s4 classes classify as 129 WIN, 18 LOSS, and 3,237 UNKNOWN. The cache secures 72/119 root vertices, leaving 47. The minimum additional class cover is 13; a rational LP dual of 13 matches the integer optimum. The additive 13-class repair targets 1,227 distinct UNKNOWN s5 positions.

### Follow-up finite results

- A local cold run with six workers processed the 81 remaining s5 targets of the then-ranked class `(1298162592590594048, 0)`. It returned 76 LOSS, 5 UNKNOWN, and 0 WIN in 526,111,188 paid nodes. The five unresolved positions were retained as targets; no deeper solver run was made for them.
- Saved results from model-hard2 Actions run `37339663025` contain all 169 canonical s6 boundary positions, each WIN. The saved-raw-only audit independently matched the boundary and parent incidence (86 and 84 children), checked every replay position for safety, canonicality, and legality, and verified that both s5 parents are WIN. Each parent is a WIN child of s4 class `(1298162592590594048, 0)`, so either one certifies that class as WIN. The audited 169 replay verdicts are accepted as saved solver results; the audit independently checks their geometry, coverage, and parent propagation.
- The intermediate merged cache, after the local run and model-hard2 results, has 2,732 canonical exact s5 entries: 65 WIN, 2,667 LOSS, and zero conflicts. Its cardinality result classifies 18 s4 classes LOSS, 131 WIN, and 3,235 UNKNOWN; it secures 72/119 root vertices and leaves 47. The minimum additional class cover is 13 and matches the rational LP dual. Reoptimized 13-class repair has an UNKNOWN s5 union of 1,237 (additive objective 1,237); the initial 1,227 union applies only to the earlier 2,648-entry snapshot.
- The 100-child class `(1297036693756510208, 0)` is now completely LOSS. Its original 10 known children were joined by eight model8-selected LOSS results (19,867,831 nodes) and 82 additional LOSS results (301,036,761 nodes). `verify_reply27_loss_class_cache.py` checked that the cache contains the full 100-child canonical boundary and that its coverage is vertices 56, 64, 90, and 96.
- The 2,822-entry checkpoint, after this class completion, contains 65 WIN and 2,757 LOSS, with zero conflicts. Its cardinality result has 19 LOSS, 131 WIN, and 3,234 UNKNOWN classes; 76/119 root vertices are secured, leaving 43. The minimum additional class cover is 12, matching the rational LP dual. The 12-class repair's additive and distinct UNKNOWN s5 union counts are both 1,147.
- A hard9 saved replay manifest records 816 s6 rows from run `37269759034`: 729 WIN, 81 LOSS, 6 UNKNOWN, and 901,901,494 nodes. The solver verdicts are accepted as saved outputs; the manifest checks row identity, shard coverage, exact-key counts, parity, verdict totals, and derived s5 recurrence. Across the fixed nine saved sources plus four supplied hard9 shards, the geometry audit found 1,000 unique canonical s6 keys (907 WIN, 87 LOSS, and 6 UNKNOWN-only). UNKNOWN results were not propagated. Their LOSS witnesses had 442 canonical safe s5 parents, 347 relevant to reply27; 185 LOSS parents were already known and 162 were new. The preceding nine-source pass had 36 parents, 25 known LOSS and one new LOSS. Merging the 162 new LOSS entries with the 2,831-entry pre-hard9 checkpoint produced 2,993 exact s5 entries (65 WIN, 2,928 LOSS, no conflicts).
- At the then-current 3,075-entry checkpoint, class `(1153202979717779456, 0)` had 97 LOSS and one UNKNOWN among 98 canonical s5 children. The [partial-boundary audit](output/next3-partial-boundary-audit.json) regenerated all 98 children directly from geometry and confirmed coverage vertices 12, 20, 48, and 50. The saved 86-child s6 boundary for parent `(1297318167659941888, 0)` was input only at that checkpoint.
- The historical `post-next3-completion-s5.cache` checkpoint had 3,075 exact s5 entries (65 WIN, 3,010 LOSS, zero conflicts), cardinality 19 LOSS/131 WIN/3,234 UNKNOWN, secured 76/119 vertices, minimum cover and rational LP dual 12, and repair costs 1,056 for the 12-class repair and 1,101 for exact-15. These work counts are not class proofs. The saved hard9 raw shards, reverse audit, and merge receipt preserve their provenance.
- The later hard1 s6 completion used an 86-child adaptive cohort: 85 WIN and one UNKNOWN in 32,291,732 nodes. A focused 15,000,000-budget retry of the remaining key `(1297320366683197440, 0)` returned LOSS in 4,508,377 nodes. The [hard1 witness audit](output/next3-hard1-loss-witness-audit.json) independently regenerated the full boundary, matched metadata and CSV, checked safe canonical legal counts, and verified witness incidence and reverse point deletion to parent `(1297318167659941888, 0)`. It accepts the saved solver verdict and does not independently prove the s6 game value. The [direct class-boundary log](output/next3-boundary-verification.log) confirms all 98 s5 children of `(1153202979717779456, 0)` are LOSS over coverage 12, 20, 48, and 50. The intermediate post-hard1 cache has 3,076 entries (65 WIN, 3,011 LOSS, no conflicts).
- Three additional saved runs contributed 218 raw s6 rows and 200 new canonical keys: hard2 run `37320154141` (170 rows), shared-round2 run `37339357570` (16), and failed next32 run `37339329716` (32). The tight15 and tight-shared artifacts contain s5 rows only and were excluded from the s6 union because their results already occur in the 3,075 snapshot. Across the 27-source audit, there are 1,286 unique canonical s6 keys (1,167 WIN, 113 LOSS, six UNKNOWN-only), with no verdict conflicts. LOSS witnesses yield 590 safe canonical s5 parents, 447 reply27-related; 372 LOSS parents were already known and 75 are new. The expanded merge produces [post-next3-expanded-s5.cache](output/post-next3-expanded-s5.cache) with 3,150 exact entries (65 WIN, 3,085 LOSS, no conflicts); [saved-s6-extra-source-manifest.json](output/saved-s6-extra-source-manifest.json), [all-saved-s6-expanded-audit.json](output/all-saved-s6-expanded-audit.json), and [post-next3-expanded-receipt.json](output/post-next3-expanded-receipt.json) preserve the input and audit scope.
- At this expanded checkpoint, cardinality classifies 20 s4 classes LOSS, 131 WIN, and 3,233 UNKNOWN, with 80/119 root vertices secured and 39 remaining. Minimum additional class cover and rational dual are both 11. The 11-class repair schedule has additive/unique UNKNOWN s5 work 1,008; exact-15 has 1,092. These are work estimates, not class proofs. The machine-readable calculations are [post-next3-expanded-cardinality.json](output/post-next3-expanded-cardinality.json) and [post-next3-expanded-repair.json](output/post-next3-expanded-repair.json).
- The 3,150-entry checkpoint is now historical. For s4 class `(1152921504766230528, 0)`, the next4 model ranking selected eight of 84 UNKNOWN s5 children as scheduling probes; all eight saved exact replays returned LOSS in 37,538,116 nodes. The remaining 76 were also LOSS in 283,661,853 nodes. The [model8 record](output/next4-model8.json), [probe rows](output/next4-model8.csv), [completion summary](output/next4-completion76-summary.json), [source hashes](output/next4-completion76-sources.json), and [saved replays](output/raw/next4-model8-out.csv) / [remaining replays](output/raw/next4-completion76-out.csv) retain the evidence. The [direct boundary verification](output/next4-boundary-verification.log) regenerated all 100 canonical s5 children and checked coverage vertices 23, 24, 30, and 31; the class is LOSS under these saved solver outcomes.
- Merging those 84 LOSS results produces [post-next4-s5.cache](output/post-next4-s5.cache): 3,234 exact entries (65 WIN, 3,169 LOSS, no conflicts). At this cache, cardinality reports 21 LOSS, 131 WIN, and 3,232 UNKNOWN s4 classes; 84/119 root vertices are secured and 35 remain. Minimum additional class cover and rational LP dual are both 10. The 10-class repair schedule has additive/distinct UNKNOWN s5 work 924; exact-15 has 1,054. These are scheduling counts, not proofs of the UNKNOWN classes. See [receipt](output/post-next4-receipt.json), [cardinality](output/post-next4-cardinality.json), [repair](output/post-next4-repair.json), and [repair targets](output/post-next4-repair.csv).
- The then-next ranked target was class `(1306043891937574912, 0)`: 16 known LOSS and 87 UNKNOWN among 103 canonical children, with new coverage vertices 67, 75, 103, and 105. It was subsequently completed as described below; the [ranking](output/post-next4-ranking.json) and [target list](output/post-next4-best-class.csv) document scheduling only.
- The 3,234-entry checkpoint is now historical. The next5 model selected eight of the 87 UNKNOWN children of class `(1306043891937574912, 0)`; all eight saved replays are LOSS in 39,499,200 nodes. The remaining 79 are also LOSS in 343,456,905 nodes. Together with the prior 16 known LOSS children, the [direct boundary verifier](output/next5-boundary-verification.log) checks all 103 canonical s5 children as LOSS, with coverage vertices 67, 75, 103, and 105. The [model inputs and provenance](output/next5-model8.json), [eight model targets](output/next5-model8.csv), [remaining targets](output/next5-remaining79.csv), [model summary and replay manifest](output/next5-model8-summary.json) / [sources](output/next5-model8-sources.json), [completion summary and replay manifest](output/next5-completion79-summary.json) / [sources](output/next5-completion79-sources.json), and [raw replay CSVs](output/raw/next5-model8-out.csv) / [remaining replays](output/raw/next5-completion79-out.csv) preserve these exact supplied-target results. The class is LOSS under these saved solver outcomes and independent boundary geometry checks.
- The 3,321-entry checkpoint is now historical. Merging the 87 new LOSS results yields [post-next5-s5.cache](output/post-next5-s5.cache): 3,321 exact entries (65 WIN, 3,256 LOSS, zero conflicts); the [receipt](output/post-next5-receipt.json) records source hashes and counts. Cardinality reports 22 LOSS, 131 WIN, and 3,231 UNKNOWN classes; 88/119 root vertices are secured and 31 remain. Minimum additional class cover and rational LP dual are both 9. The 9-class repair schedule has additive/unique UNKNOWN s5 work 837; exact-15 has additive 1,049 and distinct union 1,048. These are scheduling counts, not proofs of the UNKNOWN classes. See [cardinality](output/post-next5-cardinality.json), [repair](output/post-next5-repair.json), and [repair targets](output/post-next5-repair.csv).
- Under the now-historical 3,321-entry cache, the next6 target was class `(1297036967560609796, 0)`: 10 known LOSS and 93 UNKNOWN among 103 canonical children, with new coverage vertices 22, 32, 58, and 62. The [ranking](output/post-next5-ranking.json) and [target list](output/post-next5-best-class.csv) were scheduling only.
- The next6 finite search completed class `(1297036967560609796, 0)`. Eight model-selected targets were LOSS in 27,919,379 nodes; of the remaining 85, 83 were LOSS in 401,091,716 nodes and two were UNKNOWN. The separate 181-position s6 adaptive batch returned 179 WIN and two UNKNOWN in 61,142,979 nodes; focused retries returned LOSS for both unresolved positions in 4,832,571 and 6,689,407 nodes. The 29-source expanded s6 audit contains 1,467 unique canonical keys (1,346 WIN, 115 LOSS, six UNKNOWN-only, no conflicts); its 602 safe parents include 455 reply27-related parents, of which 449 LOSS results were already known and six were new. The [hard-parent geometry audit](output/next6-hard-boundary-audit.json) checked full 90- and 91-child parent boundaries and propagated the two saved LOSS results. The [direct class verifier](output/next6-boundary-verification.log) confirms all 103 canonical s5 children of class `(1297036967560609796, 0)` are LOSS, with coverage vertices 22, 32, 58, and 62. The [next6 model record and target lists](output/next6-model8.json) / [selected targets](output/next6-model8.csv) / [remaining targets](output/next6-remaining85.csv), replay summaries and source manifests, [expanded s6 audit](output/next6-expanded-s6-audit.json), and [saved raw replay rows](output/raw/next6-model8-out.csv), [completion85](output/raw/next6-completion85-out.csv), [adaptive s6](output/raw/next6-hard-s6-out.csv), and [focused retries](output/raw/next6-focused15m-out.csv) preserve this finite result. The solver verdicts remain exact saved/local outputs; the audit independently checks their geometry and propagation.
- Merging the six new LOSS parents from the audited expanded s6 results with the partial 3,412-entry cache produces [post-next6-s5.cache](output/post-next6-s5.cache): 3,418 exact entries (65 WIN, 3,353 LOSS, zero conflicts). The [receipt](output/post-next6-receipt.json) records its source hashes. Cardinality reports 23 LOSS, 131 WIN, and 3,230 UNKNOWN classes; 92/119 root vertices are secured and 27 remain. The minimum additional class cover and rational LP dual are both 8. The 8-class repair schedule has additive/unique UNKNOWN s5 work 744; exact-15 has additive 1,052 and distinct union 1,048. These are scheduling counts, and UNKNOWN classes remain unproved. See [cardinality](output/post-next6-cardinality.json) and [repair](output/post-next6-repair.json).
- The next ranked target under the 3,418-entry cache is class `(1301540292310335488, 0)`: 16 known LOSS and 95 UNKNOWN among 111 canonical children, with new coverage vertices 78, 86, 92, and 94. The [ranking](output/post-next6-ranking.json) and [target list](output/post-next6-best-class.csv) guide scheduling only; no verdict is inferred.
- Three of six separate cold residual mex cross-checks completed (120, 158, and 192 seconds). They are not adopted into the production cache; the cross-check set is incomplete.

These are finite cache and class results. Under the fixed first-player proposition, if s4 LOSS results cover all 119 third-move choices, then each s3 odd-stone AND node is LOSS and the s2 OR node `{60,27}` is LOSS. This establishes the refutation branch where the second player answers the central first move 60 with 27; it does not show that the empty root is a loss, because other first moves still require analysis. The 11x11 empty root and `{60,27}` outcome remain UNKNOWN in the current record, and no terminal AND/OR proof is complete. The six evidence-recovery regression tests and 33 knowledge tests passed.

## Reproduction from the preserved files

Run from the repository root. Recovery merge and direct geometry checks use the Python standard library. For cardinality, repair, and ranking scripts, use an isolated environment such as `uv run --no-project --with scipy --with numpy python ...`; this avoids changing the project environment.

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

The `output/` files are the recovered normalized results, summaries, and raw shard evidence. The raw completion CSVs and shared-s6 CSVs preserve the saved replay rows used above; `raw/pre-recovery-s5.cache` and `raw/pre-recovery-stats.json` preserve the baseline cache and its run statistics. `recovery-receipt.json` records the initial source counts, verdicts, node totals, and digests. `local-completion81-summary.json`, `raw/local-completion81.csv`, `post-model-hard2-s5.cache`, `post-model-hard2-receipt.json`, `post-model-hard2-cardinality.json`, and `post-model-hard2-repair.json` record the follow-up finite results. The five unresolved s5 targets and their s6 boundary inputs were generated and preserved at that historical stage. `model-hard2-independent-check.json` and `scripts/verify_model_hard2_results.py` preserve the saved-raw-only audit; the raw materialization metadata, boundary, four replay shards, and derived s5 cache are under `output/raw/`.

The prior target `(1297036693756510208, 0)` was completed and verified LOSS as described above. Its preserved model8 ranking and reproduction commands below document target selection only; ranking scores are not win/loss evidence. The subsequent `(1153202979717779456, 0)` class was at 97 LOSS and one UNKNOWN child at the historical 3,075 checkpoint; it is now fully LOSS as described above.

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

### Historical reproduction: saved s6 reverse pass and 3,075-entry checkpoint

The reverse script reads its fixed nine curated replay sources and the four explicitly supplied hard9 shards. It checks saved s6 geometry and one-ply parents, and propagates LOSS only. The audit does not re-prove solver verdicts and makes no repository-wide source-scan claim.

```sh
python research/experiments/n11-boundary-recovery-20261006/scripts/derive_all_saved_s6_loss_parents.py \
  --current-cache research/experiments/n11-boundary-recovery-20261006/output/pre-hard9-reverse-s5.cache \
  --extra-replay research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-0.out hard9-shard0-run37269759034 \
  --extra-replay research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-1.out hard9-shard1-run37269759034 \
  --extra-replay research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-2.out hard9-shard2-run37269759034 \
  --extra-replay research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-3.out hard9-shard3-run37269759034 \
  --out /tmp/s6-reverse-hard9-loss-s5.cache \
  --audit-out /tmp/s6-reverse-hard9-audit.json

python research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py \
  --cache research/experiments/n11-boundary-recovery-20261006/output/post-hard9-reverse-s5.cache \
  --replay research/experiments/n11-boundary-recovery-20261006/output/raw/next3-completion83-out.csv \
  --out /tmp/post-next3-completion-s5.cache \
  --summary-out /tmp/post-next3-completion-receipt.json

uv run --no-project --with scipy --with numpy python \
  research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py \
  --s5-cache /tmp/post-next3-completion-s5.cache \
  --out /tmp/post-next3-completion-cardinality.json

uv run --no-project --with scipy --with numpy python \
  research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py \
  --extra-s5-cache /tmp/post-next3-completion-s5.cache \
  --out /tmp/post-next3-completion-repair.json \
  --targets-out /tmp/post-next3-completion-repair.csv
```

### Reproduce the hard1 witness and expanded 3,150-entry snapshot

The [hard1 audit](output/next3-hard1-loss-witness-audit.json) reconstructs the 86-child s6 boundary from runtime geometry and independently checks the stored metadata, replay row, legal count, and parent relation. The focused replay is preserved in [next3-hard1-hard-s6-target.csv](output/next3-hard1-hard-s6-target.csv) and [raw/next3-hard1-hard-s6-15m-out.csv](output/raw/next3-hard1-hard-s6-15m-out.csv); the s6 LOSS remains a saved solver result.

```sh
python research/experiments/n11-boundary-recovery-20261006/scripts/verify_next3_hard1_loss_witness.py \
  --raw research/experiments/n11-boundary-recovery-20261006/output/raw/next3-hard1-hard-s6-15m-out.csv \
  --parent research/experiments/n11-boundary-recovery-20261006/output/next3-hard1-s5.csv \
  --meta research/experiments/n11-boundary-recovery-20261006/output/next3-hard1-s6-meta.json \
  --boundary research/experiments/n11-boundary-recovery-20261006/output/next3-hard1-s6-boundary.csv \
  --audit-out /tmp/next3-hard1-loss-witness-audit.json \
  --cache-out /tmp/next3-hard1-derived-s5.cache

python research/experiments/n11-frontier-selection-20261005/scripts/verify_reply27_loss_class_cache.py \
  --class-lo 1153202979717779456 --class-hi 0 --expected-children 98 --allow-extra \
  --cache research/experiments/n11-boundary-recovery-20261006/output/post-next3-expanded-s5.cache
```

To repeat the 27-source reverse audit, read only the manifest entries designated `caller_supplied_extra` and pass them explicitly. This prevents the fixed curated source set from being mistaken for a repository-wide scan. The loop below builds those explicit `--extra-replay PATH PROVENANCE` pairs from the preserved manifest (Windows separators are normalized for cross-platform use):

```sh
python - <<'PY'
import json, subprocess
from pathlib import Path
manifest = Path("research/experiments/n11-boundary-recovery-20261006/output/all-saved-s6-expanded-audit.json")
data = json.loads(manifest.read_text(encoding="utf-8"))
args = [
    "python", "research/experiments/n11-boundary-recovery-20261006/scripts/derive_all_saved_s6_loss_parents.py",
    "--current-cache", "research/experiments/n11-boundary-recovery-20261006/output/post-next3-completion-s5.cache",
    "--out", "/tmp/all-saved-s6-expanded-loss-s5.cache",
    "--audit-out", "/tmp/all-saved-s6-expanded-audit.json",
]
for source in data["sources"]:
    if source["source_kind"] == "caller_supplied_extra" and source["status"] == "included":
        path = source["path"].replace("\\", "/")
        args += ["--extra-replay", path, source["provenance"]]
subprocess.run(args, check=True)
PY

python research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py \
  --cache research/experiments/n11-boundary-recovery-20261006/output/post-next3-completion-s5.cache \
  --cache /tmp/all-saved-s6-expanded-loss-s5.cache \
  --out /tmp/post-next3-expanded-s5.cache \
  --summary-out /tmp/post-next3-expanded-receipt.json

uv run --no-project --with scipy --with numpy python \
  research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py \
  --s5-cache /tmp/post-next3-expanded-s5.cache --out /tmp/post-next3-expanded-cardinality.json

uv run --no-project --with scipy --with numpy python \
  research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py \
  --extra-s5-cache /tmp/post-next3-expanded-s5.cache \
  --out /tmp/post-next3-expanded-repair.json \
  --targets-out /tmp/post-next3-expanded-repair.csv
```

### Reproduce the next4 class result and current cache

The 84 model-selected positions and the remaining 76 inputs are preserved in [next4-model8.csv](output/next4-model8.csv) and [next4-remaining76.csv](output/next4-remaining76.csv). The model's feature sources, top-eight scores, training overlap, and reproduction commands are recorded in [next4-model8.json](output/next4-model8.json). Scores are scheduling heuristics only. The 8 and 76 solver outputs, per-file original hashes, combined digests, and exact s5 cache are preserved in the linked summaries and source manifests above.

The verifier checks that all 100 canonical children are exact LOSS in the merged cache:

```sh
python research/experiments/n11-frontier-selection-20261005/scripts/verify_reply27_loss_class_cache.py \
  --class-lo 1152921504766230528 --class-hi 0 --expected-children 100 --allow-extra \
  --cache research/experiments/n11-boundary-recovery-20261006/output/post-next4-s5.cache
```

The 3,234-entry finite frontier outputs are [post-next4-cardinality.json](output/post-next4-cardinality.json), [post-next4-repair.json](output/post-next4-repair.json), and [post-next4-ranking.json](output/post-next4-ranking.json). Their UNKNOWN class and repair counts are scheduling results under this exact cache, not terminal game proofs.

### Reproduce the next5 class result and current cache

The next5 model8 and remaining79 CSVs are scheduling inputs only; saved replay verdicts are preserved in the linked summary and source manifests. The verifier checks the full canonical 103-child boundary against the merged cache:

```sh
python research/experiments/n11-frontier-selection-20261005/scripts/verify_reply27_loss_class_cache.py \
  --class-lo 1306043891937574912 --class-hi 0 --expected-children 103 --allow-extra \
  --cache research/experiments/n11-boundary-recovery-20261006/output/post-next5-s5.cache
```

The 3,321-entry finite frontier outputs are [post-next5-cardinality.json](output/post-next5-cardinality.json), [post-next5-repair.json](output/post-next5-repair.json), and [post-next5-ranking.json](output/post-next5-ranking.json). At that historical checkpoint, the next target was `(1297036967560609796, 0)` with 10 known LOSS and 93 UNKNOWN children; ranking was for scheduling only.

### Reproduce the next6 s6 propagation and frontier

The full class audit confirms that `(1297036967560609796, 0)` is LOSS across all 103 canonical children, with coverage vertices 22, 32, 58, and 62. The merged [post-next6-s5.cache](output/post-next6-s5.cache) has 3,418 entries (65 WIN, 3,353 LOSS, no conflicts). Cardinality reports 23 LOSS, 131 WIN, 3,230 UNKNOWN, 92/119 secured vertices, and a minimum cover of 8 matching its rational dual. Repair cost is 744 additive/unique for eight classes; exact-15 is 1,052 additive and 1,048 unique. The latest ranking selects `(1301540292310335488, 0)` (16 known LOSS, 95 UNKNOWN of 111; coverage 78, 86, 92, 94). These work counts and ranking do not prove the remaining UNKNOWN classes.

The saved 29-source audit enumerates the fixed curated sources plus the explicitly included extras. Recreate its reverse propagation by using only `caller_supplied_extra` entries from the manifest; this keeps the source scope explicit:

```sh
python - <<'PY'
import json, subprocess
from pathlib import Path
root = "research/experiments/n11-boundary-recovery-20261006/output/"
manifest = json.loads(Path(root + "next6-expanded-s6-audit.json").read_text(encoding="utf-8"))
args = ["python", "research/experiments/n11-boundary-recovery-20261006/scripts/derive_all_saved_s6_loss_parents.py",
        "--current-cache", root + "post-next6-partial-s5.cache",
        "--out", "/tmp/next6-expanded-loss-s5.cache",
        "--audit-out", "/tmp/next6-expanded-s6-audit.json"]
for source in manifest["sources"]:
    if source["source_kind"] == "caller_supplied_extra" and source["status"] == "included":
        args += ["--extra-replay", source["path"].replace("\\", "/"), source["provenance"]]
subprocess.run(args, check=True)
PY

python research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py \
  --cache research/experiments/n11-boundary-recovery-20261006/output/post-next6-partial-s5.cache \
  --cache /tmp/next6-expanded-loss-s5.cache \
  --out /tmp/post-next6-s5.cache \
  --summary-out /tmp/post-next6-receipt.json

python research/experiments/n11-frontier-selection-20261005/scripts/verify_reply27_loss_class_cache.py \
  --class-lo 1297036967560609796 --class-hi 0 --expected-children 103 --allow-extra \
  --cache /tmp/post-next6-s5.cache
```

The separate hard-parent audit can be regenerated from the preserved target CSV and expanded source audit:

```sh
python research/experiments/n11-boundary-recovery-20261006/scripts/audit_saved_s6_targets.py \
  --targets research/experiments/n11-boundary-recovery-20261006/output/next6-hard-s5.csv \
  --saved-audit research/experiments/n11-boundary-recovery-20261006/output/next6-expanded-s6-audit.json \
  --current-cache research/experiments/n11-boundary-recovery-20261006/output/post-next6-partial-s5.cache \
  --summary-out /tmp/next6-hard-boundary-audit.json \
  --cache-out /tmp/next6-hard-derived-s5.cache
```

Recompute finite class counts and repair estimates under the merged cache with the existing frontier scripts and an isolated SciPy environment. Add `--geometry-cache .local/n11/reply27-geometry-v1.json.gz` when that optional local performance index is available; the direct class verifier above checks geometry independently.

```sh
uv run --no-project --with scipy --with numpy python \
  research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py \
  --s5-cache /tmp/post-next6-s5.cache --out /tmp/post-next6-cardinality.json

uv run --no-project --with scipy --with numpy python \
  research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py \
  --extra-s5-cache /tmp/post-next6-s5.cache \
  --out /tmp/post-next6-repair.json \
  --targets-out /tmp/post-next6-repair.csv
```

```sh
uv run --no-project --with scipy --with numpy python \
  research/experiments/n11-frontier-selection-20261005/scripts/rank_reply27_completion_classes.py \
  --repair-json /tmp/post-next6-repair.json \
  --extra-s5-cache /tmp/post-next6-s5.cache \
  --geometry-cache .local/n11/reply27-geometry-v1.json.gz \
  --targets-out /tmp/post-next6-best-class.csv \
  --out /tmp/post-next6-ranking.json
```

### Optional geometry index

The optional reply27 geometry index is a performance cache. Generate it explicitly, then pass `--geometry-cache` to the cardinality, repair, or ranking script to reuse it. Omitting that flag retains the original cold build. The cached geometry is not proof evidence; independent proof checks must continue to construct or check the boundary directly. The measured cold/warm comparison and trust scope are recorded in [reply27-geometry-cache.md](reports/reply27-geometry-cache.md).

```sh
python research/experiments/n11-frontier-selection-20261005/scripts/reply27_geometry_cache.py generate \
  --out .local/n11/reply27-geometry-v1.json.gz

uv run --no-project --with scipy --with numpy python \
  research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py \
  --s5-cache research/experiments/n11-boundary-recovery-20261006/output/post-next3-completion-s5.cache \
  --geometry-cache .local/n11/reply27-geometry-v1.json.gz \
  --out /tmp/cardinality-warm.json
```
