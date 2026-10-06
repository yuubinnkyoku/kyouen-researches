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
- Under the then-current 3,418-entry cache, the next7 target was class `(1301540292310335488, 0)`: 16 known LOSS and 95 UNKNOWN among 111 canonical children, with new coverage vertices 78, 86, 92, and 94. The [ranking](output/post-next6-ranking.json) and [target list](output/post-next6-best-class.csv) were for scheduling only.
- The next7 run completed class `(1301540292310335488, 0)`. Eight model-selected UNKNOWN children returned LOSS in 37,732,931 nodes; the remaining 87 returned LOSS in 396,976,088 nodes. Together with the 16 previously known LOSS children, the [direct boundary verifier](output/next7-boundary-verification.log) confirms all 111 canonical s5 children are LOSS, with coverage vertices 78, 86, 92, and 94. The [model record](output/next7-model8.json), [probe list](output/next7-model8.csv), [completion targets](output/next7-completion87.csv), [model summary and source manifest](output/next7-model8-summary.json) / [sources](output/next7-model8-sources.json), [completion summary and source manifest](output/next7-completion87-summary.json) / [sources](output/next7-completion87-sources.json), and [raw model replays](output/raw/next7-model8-out.csv) / [remaining replays](output/raw/next7-completion87-out.csv) preserve the exact supplied-target outputs. Merging these 95 LOSS results with the 3,418-entry baseline yields [post-next7-s5.cache](output/post-next7-s5.cache), 3,513 entries (65 WIN, 3,448 LOSS, zero conflicts); see the [receipt](output/post-next7-receipt.json). At the resulting 3,513-entry cache, cardinality reports 24 LOSS, 131 WIN, and 3,229 UNKNOWN classes; 96/119 root vertices are secured and 23 remain. Minimum additional cover and rational LP dual are both 7. Repair work is 649 additive/unique for seven classes; exact-15 is 1,131 additive and 1,126 distinct. The next heuristic target is `(1297599642636648448, 0)`, with 9 known LOSS and 97 UNKNOWN among 106 children and new coverage vertices 59, 61, 89, and 97. Links: [receipt](output/post-next7-receipt.json), [cardinality](output/post-next7-local-cardinality.json), [repair](output/post-next7-local-repair.json), [ranking](output/post-next7-local-ranking.json), [target list](output/post-next7-best-class.csv). These are finite frontier and scheduling results; remaining UNKNOWN classes are not proved.
- Saved Actions run `37401759541` supplied the 97 not-yet-known s5 children for `(1297599642636648448, 0)`: 96 LOSS and one UNKNOWN in 385,400,242 nodes. The separate [hard6 source](output/next8-hard-s6-meta.json) covers a 100-child s6 boundary with 98 WIN and two LOSS; the saved LOSS witness plus the other exact rows implies the s5 parent LOSS. Geometry audit regenerated that boundary with no conflicts or UNKNOWN. The [saved-source receipt](output/next8-source-receipt.json), [completion summary](output/next8-summary.json), [raw completion rows](output/raw/next8-completion-out.csv), [hard6 audit result](output/next8-hard-s6-result.json), [raw hard6 rows](output/raw/next8-hard-s6-out.csv), and [witness replay](output/raw/next8-hard-s6-witness.out) retain these inputs. The resulting [Actions checkpoint](output/post-next8-s5.cache) has 3,610 rows (65 WIN, 3,545 LOSS, no conflicts); direct verification confirms all 106 children LOSS with coverage vertices 59, 61, 89, and 97. At this checkpoint cardinality is 25 LOSS, 131 WIN, and 3,228 UNKNOWN; 100/119 root vertices are secured, 19 remain, and the minimum cover equals its rational dual at 6. This is the saved Actions checkpoint; expanded reverse propagation is recorded separately when its audit finishes.
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

### Reproduce the next4 class result and historical cache

The 84 model-selected positions and the remaining 76 inputs are preserved in [next4-model8.csv](output/next4-model8.csv) and [next4-remaining76.csv](output/next4-remaining76.csv). The model's feature sources, top-eight scores, training overlap, and reproduction commands are recorded in [next4-model8.json](output/next4-model8.json). Scores are scheduling heuristics only. The 8 and 76 solver outputs, per-file original hashes, combined digests, and exact s5 cache are preserved in the linked summaries and source manifests above.

The verifier checks that all 100 canonical children are exact LOSS in the merged cache:

```sh
python research/experiments/n11-frontier-selection-20261005/scripts/verify_reply27_loss_class_cache.py \
  --class-lo 1152921504766230528 --class-hi 0 --expected-children 100 --allow-extra \
  --cache research/experiments/n11-boundary-recovery-20261006/output/post-next4-s5.cache
```

The 3,234-entry finite frontier outputs are [post-next4-cardinality.json](output/post-next4-cardinality.json), [post-next4-repair.json](output/post-next4-repair.json), and [post-next4-ranking.json](output/post-next4-ranking.json). Their UNKNOWN class and repair counts are scheduling results under this exact cache, not terminal game proofs.

### Reproduce the next5 class result and historical cache

The next5 model8 and remaining79 CSVs are scheduling inputs only; saved replay verdicts are preserved in the linked summary and source manifests. The verifier checks the full canonical 103-child boundary against the merged cache:

```sh
python research/experiments/n11-frontier-selection-20261005/scripts/verify_reply27_loss_class_cache.py \
  --class-lo 1306043891937574912 --class-hi 0 --expected-children 103 --allow-extra \
  --cache research/experiments/n11-boundary-recovery-20261006/output/post-next5-s5.cache
```

The 3,321-entry finite frontier outputs are [post-next5-cardinality.json](output/post-next5-cardinality.json), [post-next5-repair.json](output/post-next5-repair.json), and [post-next5-ranking.json](output/post-next5-ranking.json). At that historical checkpoint, the next target was `(1297036967560609796, 0)` with 10 known LOSS and 93 UNKNOWN children; ranking was for scheduling only.

### Reproduce the next6 s6 propagation and frontier

The post-next6 cache and frontier above are the historical 3,418-entry snapshot. The next7 model8 targets and completion87 targets resolve class `(1301540292310335488, 0)` LOSS across all 111 canonical children. That historical merged cache has 3,513 entries (65 WIN, 3,448 LOSS); its finite counts and target ranking are summarized below.

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

### Reproduce the next7 class result and merged cache

The model and completion source manifests preserve raw replay hashes and combined LF output digests. Recreate the merged cache without rerunning the solver, then verify the full class boundary:

```sh
python research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py \
  --cache research/experiments/n11-boundary-recovery-20261006/output/post-next6-s5.cache \
  --cache research/experiments/n11-boundary-recovery-20261006/output/next7-model8-s5.cache \
  --cache research/experiments/n11-boundary-recovery-20261006/output/next7-completion87-s5.cache \
  --out /tmp/post-next7-s5.cache \
  --summary-out /tmp/post-next7-receipt.json

python research/experiments/n11-frontier-selection-20261005/scripts/verify_reply27_loss_class_cache.py \
  --class-lo 1301540292310335488 --class-hi 0 --expected-children 111 --allow-extra \
  --cache /tmp/post-next7-s5.cache
```

The stored next7 raw outputs are exact solver evidence. This merge and geometry check verify source consistency and the complete class boundary without recomputing those results. At this historical 3,513-entry next7 snapshot, cardinality is 24 LOSS, 131 WIN, and 3,229 UNKNOWN classes; 96/119 vertices are secured, minimum cover/dual are 7, and repair work is 649 for the seven-class set (exact-15: 1,131 additive, 1,126 distinct). Its next ranked target was `(1297599642636648448, 0)` with 9 known LOSS and 97 UNKNOWN children; scores guide scheduling only.

Recompute the historical next7 finite frontier from the merged cache:

```sh
uv run --no-project --with scipy --with numpy python \
  research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py \
  --s5-cache /tmp/post-next7-s5.cache --out /tmp/post-next7-local-cardinality.json

uv run --no-project --with scipy --with numpy python \
  research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py \
  --extra-s5-cache /tmp/post-next7-s5.cache \
  --out /tmp/post-next7-local-repair.json \
  --targets-out /tmp/post-next7-repair.csv

uv run --no-project --with scipy --with numpy python \
  research/experiments/n11-frontier-selection-20261005/scripts/rank_reply27_completion_classes.py \
  --repair-json /tmp/post-next7-local-repair.json \
  --extra-s5-cache /tmp/post-next7-s5.cache \
  --geometry-cache .local/n11/reply27-geometry-v1.json.gz \
  --targets-out /tmp/post-next7-best-class.csv \
  --out /tmp/post-next7-local-ranking.json
```

### Reproduce the saved next8 Actions checkpoint

Run `37401759541` supplied 96 LOSS replays and one UNKNOWN among the 97 previously unresolved children. The exact cache also includes the LOSS s5 parent derived from the separately audited hard6 s6 witness; no UNKNOWN verdict is propagated. Merge the saved rows with the next7 local checkpoint and check the complete target boundary:

```sh
python research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py \
  --cache research/experiments/n11-boundary-recovery-20261006/output/post-next7-s5.cache \
  --cache research/experiments/n11-boundary-recovery-20261006/output/next8-exact-s5.cache \
  --out /tmp/post-next8-s5.cache

python research/experiments/n11-frontier-selection-20261005/scripts/verify_reply27_loss_class_cache.py \
  --class-lo 1297599642636648448 --class-hi 0 --expected-children 106 --allow-extra \
  --cache /tmp/post-next8-s5.cache
```

The [source receipt](output/next8-source-receipt.json), [raw completion rows](output/raw/next8-completion-out.csv), [hard6 metadata](output/next8-hard-s6-meta.json), [hard6 raw rows](output/raw/next8-hard-s6-out.csv), and [saved witness](output/raw/next8-hard-s6-witness.out) preserve the exact inputs. The [hard6 audit summary](output/next8-hard-s6-result.json) reports 98 WIN and two LOSS across its 100-child boundary; geometry audit plus the exact LOSS witness supports the derived parent LOSS. The merged Actions checkpoint has 3,610 rows (65 WIN, 3,545 LOSS), and the target boundary has all 106 children LOSS with coverage `{59,61,89,97}`. Its finite counts are 25 LOSS, 131 WIN, 3,228 UNKNOWN; secured vertices 100/119, with minimum cover and rational dual both 6. Expanded reverse propagation is a later snapshot.

Next9's saved exact outputs concern class `(10376293541461626880, 64)`. The [summary](output/next9-summary.json) reports 102 replay rows (94 LOSS, three WIN, five UNKNOWN; 567,396,507 nodes) and a complete 104-child boundary with 96 LOSS, three WIN, five UNKNOWN, so the s4 class is WIN. A separate [hard-s6 metadata set](output/next9-hard-s6-meta.json) and [91-row replay](output/next9-hard-s6-out.csv) reports all 91 children WIN (29,531,979 nodes); the [geometry receipt](output/next9-hard-s6-parent-win-receipt.json) verifies that this resolves one more s5 child to WIN. Four children remain UNKNOWN and were not solved. The [source receipt](output/next9-next10-source-receipt.json) preserves run identities and replay hashes.

The next10 Xserver exact replay completed class `(5908722711110107136, 0)`: all 100 canonical children are LOSS, totaling 289,895,608 nodes, with coverage `{34,42,82}` and no conflicts. The [target list](output/next10-xserver-targets.csv), [summary](output/next10-xserver-summary.json), [raw replay rows](output/raw/next10-xserver-replay.csv), and [exact cache](output/next10-xserver-s5.cache) preserve this finite result. Its replay verdicts are exact solver evidence; geometry auditing checks the complete boundary. The 3,792-entry Actions fold and 3,796-entry expanded cache are historical checkpoints; their frontier outputs remain linked at [post-next10-expanded-cardinality.json](output/post-next10-expanded-cardinality.json), [repair](output/post-next10-expanded-repair.json), and [ranking](output/post-next10-expanded-ranking.json). At the historical repair5 batch checkpoint, run `37404904661`, returned 473 raw rows: 410 LOSS, 19 WIN, and 44 UNKNOWN, totaling 3,136,880,721 nodes. All 102 canonical children of class `(1297036692816920608, 0)` are LOSS, with coverage `{5,55,57,63,65}`. Class `(1873497444986126592, 0)` remains UNKNOWN with 106 LOSS and two UNKNOWN among 108 children. Three other selected classes are WIN, with 42 UNKNOWN children left unsolved. The [raw source manifest](output/repair5-batch-sources.json), [targets](output/repair5-batch-targets.csv), [combined replay rows](output/raw/repair5-batch-out.csv), and [batch summary](output/repair5-batch-action-summary.json) preserve the saved outputs. The Actions merge has 4,221 entries (88 WIN, 4,133 LOSS); expanded saved-s6 results produce the latest [4,225-entry cache](output/post-repair5-expanded-s5.cache), 88 WIN and 4,137 LOSS, zero conflicts. Historical cardinality there was 27 LOSS, 161 WIN, 3,196 UNKNOWN; 106/119 root vertices are secured, 13 remain, and minimum cover/rational dual are both 4. Four-class repair additive/unique work is 304; exact-15 is 1,231 additive and 1,221 distinct. At that historical checkpoint, the ranked class `(1873497444986126592, 0)` had 106 known LOSS and two UNKNOWN among 108 children, coverage `{49,88,98}`. See the [merge receipt](output/post-repair5-expanded-receipt.json), [cardinality](output/post-repair5-expanded-cardinality.json), [repair](output/post-repair5-expanded-repair.json), [ranking](output/post-repair5-expanded-ranking.json), and [target list](output/post-repair5-expanded-best-class.csv). Ranking guides scheduling only; the two UNKNOWN children remain unresolved.

The following adaptive 2M s6 cohort processed 193 new rows from a 195-child boundary: 137 WIN, 56 UNKNOWN, zero LOSS, and 179,743,467 nodes. Its [summary](output/repair5-hard2-adaptive2m-summary.json), [source manifest](output/repair5-hard2-adaptive2m-sources.json), [56 remaining UNKNOWN targets](output/repair5-hard2-adaptive2m-hard-s6.csv), and [combined replay rows](output/raw/repair5-hard2-adaptive2m-out.csv) preserve the input and results. Parent `(1152921506758524928, 536871040)` remains UNKNOWN with 83 WIN and 14 UNKNOWN among 97 children; parent `(1152921504612089856, 536871040)` remains UNKNOWN with 56 WIN and 42 UNKNOWN among 98 children. This cohort added no s5 cache verdicts: it had no LOSS result and neither parent had all children WIN.

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


### Current expanded frontier after parent A/B recovery

The focused parent-A and parent-B cohorts, their 33-source and 34-source saved-s6 audits, and target-specific geometry receipts are linked in the artifact inventory above. Parent A `(1152921506758524928, 536871040)` and parent B `(1152921504612089856, 536871040)` are both LOSS. The 34-source audit has 1,849 unique canonical s6 keys (1,678 WIN, 125 LOSS, 46 UNKNOWN-only, no conflicts); LOSS-only reverse propagation adds exact s5 LOSS parents. Direct verification confirms all 108 canonical children of `(1873497444986126592, 0)` are LOSS.

The post-parent-B 4,243-entry cache and next12 4,257-entry cache are historical checkpoints. Next12's probe and adaptive hard-s6 audits established class `(1152921513197830144, 536870912)` as WIN; three of its five hard parents remained UNKNOWN and no completion100 run was started. Next13 completed six of eight scheduled probes (three WIN, three LOSS; 57,081,707 nodes); two probes were not dispatched, and the other 96 children were not run. Independent source and geometry auditing confirms the complete 108-child boundary and that the six exact rows make class `(1298162592589545600, 0)` WIN.

The historical cache was [post-next13-expanded-s5.cache](output/post-next13-expanded-s5.cache): 4,263 entries (92 WIN, 4,171 LOSS), zero conflicts. Its finite counts were 28 LOSS, 167 WIN, 3,189 UNKNOWN classes; 109/119 vertices secured, 10 remaining, and minimum cover/rational dual both 4. Four-class repair was 344 additive/unique; exact-15 was 1,361 additive and 1,319 unique. Its ranked boundary `(10376293541595840512, 64)` had 6 known LOSS and 51 UNKNOWN among 57 children, coverage `{57,63,70,72}`, with new vertices `{70,72}`. The independent finite audit at [post-next13-finite-independent-audit.json](output/post-next13-finite-independent-audit.json) checks all 3,384 class statuses, 109-vertex coverage, the four-class cover, and its matching rational dual. See the [receipt](output/post-next13-expanded-receipt.json), [cardinality](output/post-next13-expanded-cardinality.json), [repair](output/post-next13-expanded-repair.json), [ranking](output/post-next13-expanded-ranking.json), and [target list](output/post-next13-best-class.csv). Ranking and UNKNOWN repair counts are scheduling results, not proofs. The empty-board and `{60,27}` outcomes remain UNKNOWN; terminal AND/OR proof is incomplete.

The historical cache was [post-next12-expanded-s5.cache](output/post-next12-expanded-s5.cache): 4,257 entries (89 WIN, 4,168 LOSS), zero conflicts. Its finite counts were 28 LOSS, 163 WIN, 3,193 UNKNOWN classes; 109/119 vertices secured, 10 remaining, and minimum cover/rational dual both 3. Three-class repair was 308 additive/unique; exact-15 was 1,360 additive and 1,341 unique. Its ranked boundary `(1298162592589545600, 0)` has 4 known LOSS and 104 UNKNOWN among 108 children, coverage `{70,72,77,87}`. See the final [receipt](output/post-next12-expanded-receipt.json), [cardinality](output/post-next12-expanded-cardinality.json), [repair](output/post-next12-expanded-repair.json), [ranking](output/post-next12-expanded-ranking.json), and [target list](output/post-next12-expanded-best-class.csv). Ranking and UNKNOWN repair counts are scheduling results, not proofs. Empty-board and `{60,27}` remain UNKNOWN; terminal AND/OR proof is incomplete.


### Current next14 expanded frontier

The next14 run completed seven of eight scheduled probes: five LOSS and two WIN, totaling 44,039,611 nodes. One scheduled probe was not dispatched, and no completion43 run followed. The independent source and geometry audit checks the full 57-child boundary and confirms class `(10376293541595840512, 64)` WIN; no additional class work was run.

The historical expanded cache was [post-next14-expanded-s5.cache](output/post-next14-expanded-s5.cache): 4,270 entries (94 WIN, 4,176 LOSS), no conflicts. Its finite counts were 28 LOSS, 170 WIN, 3,186 UNKNOWN; 109/119 vertices secured, 10 remaining, and minimum cover/rational dual both 4. Four-class repair was 379 additive/unique; exact-15 was 1,403 additive and 1,361 unique. The best ranked class `(1297036692682702984, 0)` had 108 children, 4 known LOSS and 104 UNKNOWN, coverage `{33,43,77,87}`. The independent finite audit at [post-next14-finite-independent-audit.json](output/post-next14-finite-independent-audit.json) checks all class statuses, 109-vertex coverage, the four-class cover and matching rational dual. See the [merge](output/post-next14-expanded-merge.json), [receipt](output/post-next14-expanded-receipt.json), [cardinality](output/post-next14-expanded-cardinality.json), [repair](output/post-next14-expanded-repair.json), [ranking](output/post-next14-expanded-ranking.json), and [target list](output/post-next14-best-class.csv). The ranking is for scheduling only. Empty-board and `{60,27}` remain UNKNOWN; terminal AND/OR proof is incomplete.


### Historical next15 expanded frontier

Next15 hard3 audited the prior 35-source saved-s6 collection and found zero overlap with the 296-child boundary, then completed 162 new exact replays (157 WIN, 5 LOSS; 89,196,422 nodes). Across the 296-child union boundary, 134 children remained unseen and unresolved when a parent WIN stopped further work; they were not saved UNKNOWN replay outputs. No saved UNKNOWN rows were eligible for retry, and new rows had zero overlap with prior exact rows. The archived summary field `saved_unknown_boundary_count` is mislabeled and counts the unresolved boundary, including unseen keys. See the [run summary](output/next15-hard3-adaptive15m-summary.json), [source manifest](output/next15-hard3-adaptive15m-sources.json), [raw exact rows](output/raw/next15-hard3-adaptive15m-out.csv), and [pre-boundary geometry audit](output/next15-hard3-independent-boundary-audit.json). The [post-run s6 propagation audit](output/next15-s6-propagation-independent-audit.json) independently checks source hashes, replay bindings, AND propagation, and reverse LOSS derivation without re-proving solver outcomes. One s5 parent had a complete 99-child s6 boundary with all 99 WIN; the other two parents were LOSS. The single s5 WIN is sufficient to establish class `(1297036692682702984, 0)` as WIN. The separate 36-source reverse audit adds 13 s5 LOSS parents from saved exact LOSS s6 rows. The [finite snapshot audit](output/post-next15-finite-independent-audit.json) independently verifies all class statuses, secured coverage, the four-class cover, and its rational dual.

The historical cache was [post-next15-expanded-s5.cache](output/post-next15-expanded-s5.cache): 4,385 entries (95 WIN, 4,290 LOSS), zero conflicts, SHA-256 `8a199081c83868ef931f6ef2e9a8b3d02ce2988b86893984abc6d5d3843f4b59`. Its finite counts were 28 LOSS, 172 WIN, 3,184 UNKNOWN classes; 109/119 vertices secured, 10 remaining, and minimum cover/rational dual both 4. Four-class repair was 377 additive/unique; exact-15 was 1,399 additive and 1,358 unique. The ranked class `(1586392968741257216, 0)` had 98 children, 7 known LOSS and 91 UNKNOWN, coverage `{38,70,72}`. See the [merge](output/post-next15-expanded-merge.json), [receipt](output/post-next15-expanded-receipt.json), [cardinality](output/post-next15-expanded-cardinality.json), [repair](output/post-next15-expanded-repair.json), [ranking](output/post-next15-expanded-ranking.json), and [target list](output/post-next15-best-class.csv). These are historical finite frontier and scheduling results.

### Historical next16 expanded frontier

Next16 started from the next15 cache. Of eight model8 targets, four were dispatched; three produced new exact rows (two WIN and one LOSS) and one was UNKNOWN, totaling 43,173,440 nodes. Four targets were not dispatched. The complete 98-child boundary audit confirms class `(1586392968741257216, 0)` WIN from the exact WIN witnesses. The supplied targets had zero overlap with the previous exact cache. An independent audit checks source hashes, boundary geometry, and cache delta while treating saved solver outcomes as inputs, not re-proving them. The saved-s6 target audit before replay found all 91 targets UNKNOWN and produced an empty derived cache. No new s6 search was run for next16. See the [run summary](output/next16-run-model8-summary.json), [sources](output/next16-run-model8-sources.json), [raw rows](output/raw/next16-run-model8-out.csv), [independent run audit](output/next16-run-model8-independent-audit.json), and [saved-s6 summary](output/next16-saved-s6-summary.json).

The historical cache was [post-next16-expanded-s5.cache](output/post-next16-expanded-s5.cache): 4,388 entries (97 WIN, 4,291 LOSS), zero conflicts; SHA-256 `ddc997e18480ed9ceb669148dcc46166eae1bb6ae9ec08d07e4954d6aa91c081`. Its finite counts were 28 LOSS, 175 WIN, 3,181 UNKNOWN; 109/119 vertices secured, 10 remaining, and minimum cover/rational dual both 4. Four-class repair was 385 additive/unique; exact-15 was 1,401 additive and 1,375 unique. The ranked class `(1298162592589545480, 0)` had 110 children, 8 known LOSS and 102 UNKNOWN, coverage `{33,43,70,72}`. See the [receipt](output/post-next16-expanded-receipt.json), [cardinality](output/post-next16-expanded-cardinality.json), [repair](output/post-next16-expanded-repair.json), [ranking](output/post-next16-expanded-ranking.json), [target list](output/post-next16-best-class.csv), and [independent finite audit](output/post-next16-finite-independent-audit.json). These are historical scheduling results.

### Current next17 expanded frontier

Next17 model8 returned eight exact s5 LOSS rows (54,975,108 nodes). Its completion93 run returned 89 LOSS and 4 UNKNOWN s5 rows (656,185,414 nodes). The hard5 adaptive s6 boundary contained 493 children: 3 previously saved WIN keys and 214 new exact replays (200 WIN, 14 LOSS; 190,725,964 nodes), with 276 unseen children not dispatched. No saved UNKNOWN child rows were eligible for retry. The five s5 parents were classified LOSS through exact child witnesses. The independent propagation audit checks source hashes, full geometry, and reverse propagation while treating solver values as inputs; the direct verifier confirms the full 110-child class is LOSS. See the model8 [summary](output/next17-run-model8-summary.json), [sources](output/next17-run-model8-sources.json), [raw rows](output/raw/next17-run-model8-out.csv), [independent audit](output/next17-run-model8-independent-audit.json), completion93 [summary](output/next17-completion93-summary.json) and [raw rows](output/raw/next17-completion93-out.csv), hard5 adaptive [summary](output/next17-hard5-adaptive15m-summary.json), [raw rows](output/raw/next17-hard5-adaptive15m-out.csv), [propagation audit](output/next17-s6-propagation-independent-audit.json), and [full class verification](output/next17-full110-class-verification.json).

The current cache is [post-next17-expanded-s5.cache](output/post-next17-expanded-s5.cache): 4,515 entries (97 WIN, 4,418 LOSS), zero conflicts; SHA-256 `2fa27a15625af7449ca8f3fa21e683ba2e13a5d4deb99f8919d02ea61b59c82c`. Finite class counts are 29 LOSS, 175 WIN, 3,180 UNKNOWN; 113/119 vertices secured, 6 remaining, and minimum cover/rational dual both 3. Three-class repair is 283 additive/unique UNKNOWN s5 entries; exact-15 is 1,399 additive and 1,363 unique. The best ranked class `(1585267068834414720, 0)` has 104 children, 5 known LOSS and 99 UNKNOWN, coverage `{38,77,87}`. See the [receipt](output/post-next17-expanded-receipt.json), [cardinality](output/post-next17-expanded-cardinality.json), [repair](output/post-next17-expanded-repair.json), [ranking](output/post-next17-expanded-ranking.json), [target list](output/post-next17-expanded-best-class.csv), and [independent finite audit](output/post-next17-finite-independent-audit.json). UNKNOWN classes, empty-board outcome, and `{60,27}` remain unresolved.
