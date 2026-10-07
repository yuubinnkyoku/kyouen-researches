---
id: K0355
title: 11×11 reply27の保存済みexact結果から復元したcache frontier
kind: computation
status: computed
topics: [square-outcomes, search-methods, verification, provenance]
aliases: []
relations:
  - type: depends_on
    target: K0002
    note: 先手視点のWIN/LOSSと奇数石AND・偶数石ORの規約
  - type: depends_on
    target: K0007
    note: exact勝敗の意味は順位付きAND/OR証明の健全性に従う
artifacts:
  - path: research/experiments/n11-boundary-recovery-20261006/README.md
    role: source
    note: 回収範囲、手順、結論と限界
  - path: research/experiments/n11-boundary-recovery-20261006/output/reply27-current-s5.cache
    role: data
    note: 統合したcanonical exact s5 cache 2,648件
  - path: research/experiments/n11-boundary-recovery-20261006/output/recovery-receipt.json
    role: manifest
    note: 入力ごとの行数、判定数、node合計、SHA-256、衝突数0
  - path: research/experiments/n11-boundary-recovery-20261006/output/shared-s6-summary.json
    role: data
    note: s6 16件、親子relation 66件の監査要約
  - path: research/experiments/n11-boundary-recovery-20261006/output/reply27-class-1297036692816953344-0-s5.cache
    role: data
    note: 対象s4 classの105 canonical s5 LOSS境界
  - path: research/experiments/n11-boundary-recovery-20261006/output/recovered-cardinality.json
    role: data
    note: cache-aware cardinality、LP dual、整数被覆結果
  - path: research/experiments/n11-boundary-recovery-20261006/output/recovered-repair.json
    role: data
    note: 初期2,648-entry snapshotでの13 class修復target計算。後続cacheでの再最適化値ではない
  - path: research/experiments/n11-boundary-recovery-20261006/output/local-completion81-summary.json
    role: data
    note: 81対象のlocal cold run集計、76 LOSS・5 UNKNOWN・526,111,188 paid nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/local-completion81.csv
    role: source
    note: 81対象の保存済みexact replay rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/next-local5-s6-boundary.csv
    role: data
    note: 5 unresolved childrenのため生成して保存したs6 boundary input。solver replay未実施
  - path: research/experiments/n11-boundary-recovery-20261006/output/next-local5-s6-meta.json
    role: manifest
    note: 上記未実行boundaryの5親metadata
  - path: research/experiments/n11-boundary-recovery-20261006/output/model-hard2-independent-check.json
    role: manifest
    note: Actions run 37339663025の169 s6結果に対するsaved-raw-only独立境界・incidence・replay監査
  - path: research/experiments/n11-boundary-recovery-20261006/output/model-hard2-derived-s5.cache
    role: data
    note: 2つのs5親をWINとするmodel-hard2からの派生cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-model-hard2-s5.cache
    role: data
    note: 中間snapshotのcanonical exact s5 cache 2,732件
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-model-hard2-receipt.json
    role: manifest
    note: 中間snapshotのsourceごとの件数・verdict・hashと衝突0
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-model-hard2-cardinality.json
    role: data
    note: 中間2,732-entry cacheでのclass数・secured vertices・dual-tight minimum cover
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-model-hard2-repair.json
    role: data
    note: 中間snapshotでの13-class repair、UNKNOWN s5 union 1,237
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-model-hard2-repair-targets.csv
    role: data
    note: 2,732-entry中間snapshotで再計算したrepair対象
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/model-hard2-reply27-model-hard2-s6-proof-result.json
    role: source
    note: run 37339663025の保存済み169 s6 replay集計
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/model-hard2-reply27-model-hard2-s6-proof-model-hard2-s5.cache
    role: source
    note: run 37339663025から保存されたs5親へのexact派生cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/model-hard2-reply27-model-hard2-materialized-hard2-meta.json
    role: source
    note: run 37339663025の169 s6 boundaryと親relation metadata
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/model-hard2-reply27-model-hard2-materialized-hard2-s6.csv
    role: source
    note: run metadataから独立したcanonical s6 boundary materialization
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/model-hard2-reply27-model-hard2-s6-0-out.csv
    role: source
    note: run 37339663025 saved exact replay shard 0
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/model-hard2-reply27-model-hard2-s6-1-out.csv
    role: source
    note: run 37339663025 saved exact replay shard 1
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/model-hard2-reply27-model-hard2-s6-2-out.csv
    role: source
    note: run 37339663025 saved exact replay shard 2
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/model-hard2-reply27-model-hard2-s6-3-out.csv
    role: source
    note: run 37339663025 saved exact replay shard 3
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/verify_model_hard2_results.py
    role: verifier
    note: 保存rawだけからcanonical boundary・parent incidence・replay legalityと親伝播を検査
  - path: research/experiments/n11-boundary-recovery-20261006/output/next2-model8.csv
    role: source
    note: 対象classのmodel8候補入力。順位は探索順の提案でありverdictではない
  - path: research/experiments/n11-boundary-recovery-20261006/output/next2-model8-summary.json
    role: data
    note: model8が選んだ8件のexact LOSS、19,867,831 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next2-model8-s5.cache
    role: data
    note: model8選択分の8 exact LOSS cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/next2-model8-sources.json
    role: manifest
    note: model8選択分のsolver sourceと件数・hash
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next2-model8-out.csv
    role: source
    note: model8選択分の保存済みreplay CSV
  - path: research/experiments/n11-boundary-recovery-20261006/output/next2-completion82-summary.json
    role: data
    note: 残る82件すべてLOSS、301,036,761 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next2-completion82-s5.cache
    role: data
    note: 残る82件のexact LOSS cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/next2-completion82-sources.json
    role: manifest
    note: 残82件のsolver sourceと件数・hash
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next2-completion82-out.csv
    role: source
    note: 残る82件の保存済みexact replay CSV
  - path: research/experiments/n11-boundary-recovery-20261006/output/next2-boundary-verification.log
    role: log
    note: class geometryのcanonical 100子とcoverage 56,64,90,96の検査結果
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next2-s5.cache
    role: data
    note: 当時のcheckpoint。canonical exact s5 cache 2,822件 (WIN 65, LOSS 2,757)
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next2-receipt.json
    role: manifest
    note: next2 source別の件数・verdict・node数・hash、衝突0
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next2-cardinality.json
    role: data
    note: 2,822-entry checkpointでのclass数、secured vertices、minimum coverとdual
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next2-repair.json
    role: data
    note: 2,822-entry checkpointでの12-class repair。additiveとdistinct UNKNOWN s5 unionは各1,147
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/pre-recovery-s5.cache
    role: source
    note: Actions run 37334644565の保存済み基準cache
  - path: research/experiments/n11-frontier-selection-20261005/output/reply27-best-class-model8-s5.cache
    role: source
    note: 保存済みmodel8 exact cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/pre-recovery-stats.json
    role: source
    note: Actions run 37334644565のcache統計
  - path: research/experiments/n11-frontier-selection-20261005/output/reply27-current-shared16-s6.json
    role: source
    note: shared s6 probeと親候補のmetadata
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/shared-s6-0.csv
    role: source
    note: Actions run 37336924568の保存済みshared s6 replay shard 0
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/shared-s6-1.csv
    role: source
    note: Actions run 37336924568の保存済みshared s6 replay shard 1
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/shared-s6-2.csv
    role: source
    note: Actions run 37336924568の保存済みshared s6 replay shard 2
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/shared-s6-3.csv
    role: source
    note: Actions run 37336924568の保存済みshared s6 replay shard 3
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/completion86-0.csv
    role: source
    note: Actions run 37337141197の保存済みcompletion86 replay shard 0
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/completion86-1.csv
    role: source
    note: Actions run 37337141197の保存済みcompletion86 replay shard 1
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/completion86-2.csv
    role: source
    note: Actions run 37337141197の保存済みcompletion86 replay shard 2
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/completion86-3.csv
    role: source
    note: Actions run 37337141197の保存済みcompletion86 replay shard 3
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/completion86-4.csv
    role: source
    note: Actions run 37337141197の保存済みcompletion86 replay shard 4
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/completion86-5.csv
    role: source
    note: Actions run 37337141197の保存済みcompletion86 replay shard 5
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/completion86-6.csv
    role: source
    note: Actions run 37337141197の保存済みcompletion86 replay shard 6
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/completion86-7.csv
    role: source
    note: Actions run 37337141197の保存済みcompletion86 replay shard 7
  - path: research/experiments/n11-frontier-selection-20261005/scripts/derive_shared_s6_witness_cache.py
    role: verifier
    note: s6 metadataの安全性、D4正規化、親子relationをgeometryから監査しLOSS witnessを派生
  - path: research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py
    role: verifier
    note: canonical key、exact verdict、重複と衝突を監査してcacheを統合
  - path: research/experiments/n11-frontier-selection-20261005/scripts/verify_reply27_loss_class_cache.py
    role: verifier
    note: 指定s4 classの全canonical s5境界がLOSSであることを検査
  - path: research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py
    role: solver
    note: cache条件下の有限class coverとrational LP dualを計算
  - path: research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py
    role: solver
    note: 追加class修復targetを最適化
  - path: research/experiments/n11-boundary-recovery-20261006/output/hard9-source-manifest.json
    role: manifest
    note: Actions run 37269759034の816 s6 rows。729 WIN、81 LOSS、6 UNKNOWN、901,901,494 nodes。判定値は保存solver出力として扱う
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-derived-s5.cache
    role: source
    note: hard9の81 LOSS s6から派生した9件のs5 LOSS
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-0.csv
    role: source
    note: hard9 Actions run 37269759034 saved replay shard 0
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-0.meta.json
    role: source
    note: hard9 shard 0 boundary metadata
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-0.out
    role: source
    note: hard9 shard 0 solver result rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-1.csv
    role: source
    note: hard9 Actions run 37269759034 saved replay shard 1
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-1.meta.json
    role: source
    note: hard9 shard 1 boundary metadata
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-1.out
    role: source
    note: hard9 shard 1 solver result rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-2.csv
    role: source
    note: hard9 Actions run 37269759034 saved replay shard 2
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-2.meta.json
    role: source
    note: hard9 shard 2 boundary metadata
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-2.out
    role: source
    note: hard9 shard 2 solver result rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-3.csv
    role: source
    note: hard9 Actions run 37269759034 saved replay shard 3
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-3.meta.json
    role: source
    note: hard9 shard 3 boundary metadata
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-3.out
    role: source
    note: hard9 shard 3 solver result rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard9-s6-VERIFIED.txt
    role: manifest
    note: saved hard9 shard boundary verification marker
  - path: research/experiments/n11-boundary-recovery-20261006/output/s6-reverse-audit.json
    role: manifest
    note: 固定9-source reverse pass。36 safe s5 parents、25既知LOSSと1 new LOSS、conflictなし
  - path: research/experiments/n11-boundary-recovery-20261006/output/s6-reverse-loss-s5.cache
    role: data
    note: 9-source passで派生した1 new s5 LOSS
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/derive_all_saved_s6_loss_parents.py
    role: verifier
    note: 保存済みs6 LOSSの全canonical s5 parentを列挙し、safe geometryとsource consistencyを監査
  - path: research/experiments/n11-boundary-recovery-20261006/output/pre-hard9-reverse-s5.cache
    role: data
    note: hard9 reverse前checkpoint。2,831 entries、WIN 65、LOSS 2,766
  - path: research/experiments/n11-boundary-recovery-20261006/output/pre-hard9-reverse-receipt.json
    role: manifest
    note: 2,831-entry pre-hard9 reverse checkpoint source receipt
  - path: research/experiments/n11-boundary-recovery-20261006/output/s6-reverse-hard9-audit.json
    role: manifest
    note: 13-source監査。1,000 unique s6 keys (907 WIN、87 LOSS、6 UNKNOWN-only)。442 safe s5 parents中347がreply27関連、185 LOSS既知、162 new LOSS
  - path: research/experiments/n11-boundary-recovery-20261006/output/s6-reverse-hard9-loss-s5.cache
    role: data
    note: hard9を加えたreverse passで得た162 new s5 LOSS
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-hard9-reverse-s5.cache
    role: data
    note: 2,993-entry checkpoint、WIN 65、LOSS 2,928。pre-hard9 2,831から162 LOSSを追加
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-hard9-reverse-receipt.json
    role: manifest
    note: hard9 reverse後の2,993-entry source receipt、conflict 0
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-model8.csv
    role: source
    note: class (1153202979717779456, 0) のheuristic model8 exact-replay targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-model8.json
    role: manifest
    note: model8のfeature/ranking manifest。順位はheuristicでありverdictではない
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-model8-summary.json
    role: data
    note: 8 targetsすべてLOSS、19,329,773 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-model8-s5.cache
    role: data
    note: model8 8 LOSS cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-model8-sources.json
    role: manifest
    note: model8 solver raw source digestとverdict summary
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next3-model8-out.csv
    role: source
    note: model8 8件の保存済み exact replay rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-remaining.csv
    role: data
    note: class (1153202979717779456, 0) のmodel8後の残余83 targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-completion83-summary.json
    role: data
    note: 83 targetsで82 LOSS、1 UNKNOWN、352,645,468 nodes。UNKNOWNは未解決境界のまま
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-completion83-sources.json
    role: manifest
    note: 83-target local completionのsource receipt
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-completion83-s5.cache
    role: data
    note: 82 exact LOSSのsubset cache
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/complete_class_local.py
    role: verifier
    note: supplied target set内のexact s5 completion runner。class statusはboundary scopeを限定して報告
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next3-completion83-out.csv
    role: source
    note: 83 target exact replay rows (82 LOSS、1 UNKNOWN)
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-saved-s6-summary.json
    role: manifest
    note: 保存済みs6 replayから作ったreverse parentと各境界statusのsummary。solver verdictを独立証明しない
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-saved-s6-derived-s5.cache
    role: data
    note: 保存済みs6 LOSSから導出したs5 cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-hard1-s6-boundary.csv
    role: data
    note: parent (1297318167659941888, 0) のindependently verified 86-child s6 boundary
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-hard1-s6-meta.json
    role: manifest
    note: 86-child s6 boundary metadata, independently matched to CSV and runtime geometry
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-hard1-s6-2m-summary.json
    role: data
    note: "adaptive completion of 86 hard1 s6 children: 85 WIN and one UNKNOWN, 32,291,732 nodes"
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next3-hard1-s6-2m-out.csv
    role: source
    note: 86-row adaptive hard1 cohort replay output
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-hard1-hard-s6-target.csv
    role: source
    note: focused replay input for the remaining key (1297320366683197440, 0)
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next3-hard1-hard-s6-15m-out.csv
    role: source
    note: focused 15M-budget replay; LOSS in 4,508,377 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-hard1-hard-s6-15m-source.json
    role: manifest
    note: focused replay source digest, budget, node count, and LF copy receipt
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-hard1-loss-witness-audit.json
    role: verifier
    note: runtime geometry verified full s6 boundary, solver LOSS witness, and reverse point deletion to parent
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/verify_next3_hard1_loss_witness.py
    role: verifier
    note: audits full 86-child boundary and witness incidence; accepts saved solver verdict without reproving game outcome
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-hard1-derived-s5.cache
    role: data
    note: LOSS propagated from the audited s6 witness to s5 parent (1297318167659941888, 0)
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-boundary-verification.log
    role: verifier
    note: direct runtime geometry verifier confirms all 98 class children LOSS
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next3-hard1-s5.cache
    role: data
    note: 3,076-entry checkpoint after hard1 parent LOSS; 65 WIN and 3,011 LOSS
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next3-hard1-receipt.json
    role: manifest
    note: 3,076-entry checkpoint source receipt, conflict 0
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next3-completion-s5.cache
    role: data
    note: checkpoint 3,075 canonical exact s5 entries、WIN 65、LOSS 3,010、conflict 0
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next3-completion-receipt.json
    role: manifest
    note: 3,075-entry snapshot source rows、verdict counts、node totals、SHA-256
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next3-completion-cardinality.json
    role: data
    note: 3,075-entry snapshot; class counts 19 LOSS, 131 WIN, 3,234 UNKNOWN; cover and rational dual both 12
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next3-completion-repair.json
    role: data
    note: "repair work plan: 12 classes/1,056 unknown s5 additive work; exact-15 option 1,101. Scheduling only"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next3-completion-repair.csv
    role: data
    note: 12-class repair's 1,056 remaining unique unknown s5 targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/next3-partial-boundary-audit.json
    role: verifier
    note: historical partial audit of 98 s5 children, 97 LOSS and 1 UNKNOWN before hard1 completion
  - path: research/experiments/n11-boundary-recovery-20261006/reports/reply27-geometry-cache.md
    role: source
    note: optional geometry cache A/B timings, equality checks, and trust boundary
  - path: research/experiments/n11-boundary-recovery-20261006/output/geometry-cache-ab-summary.json
    role: manifest
    note: geometry cache A/Bの機械可読receipt
  - path: research/experiments/n11-frontier-selection-20261005/scripts/reply27_geometry_cache.py
    role: verifier
    note: optional geometry cache generator/loader; performance aid only, not proof evidence
  - path: research/experiments/n11-boundary-recovery-20261006/output/saved-s6-extra-source-manifest.json
    role: manifest
    note: provenance and digests for additional saved Actions artifacts and s5-only exclusions
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard2-shard0.csv
    role: source
    note: recovered s6 shard 0 from Actions run 37320154141
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard2-shard1.csv
    role: source
    note: recovered s6 shard 1 from Actions run 37320154141
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard2-shard2.csv
    role: source
    note: recovered s6 shard 2 from Actions run 37320154141
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/hard2-shard3.csv
    role: source
    note: recovered s6 shard 3 from Actions run 37320154141
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/shared-round2-shard0.csv
    role: source
    note: recovered s6 shard 0 from Actions run 37339357570
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/shared-round2-shard1.csv
    role: source
    note: recovered s6 shard 1 from Actions run 37339357570
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/shared-round2-shard2.csv
    role: source
    note: recovered s6 shard 2 from Actions run 37339357570
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/shared-round2-shard3.csv
    role: source
    note: recovered s6 shard 3 from Actions run 37339357570
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next32-shard0.csv
    role: source
    note: recovered s6 shard 0 from failed Actions run 37339329716
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next32-shard1.csv
    role: source
    note: recovered s6 shard 1 from failed Actions run 37339329716
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next32-shard2.csv
    role: source
    note: recovered s6 shard 2 from failed Actions run 37339329716
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next32-shard3.csv
    role: source
    note: recovered s6 shard 3 from failed Actions run 37339329716
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/tight15-s5-shard0.csv
    role: source
    note: s5-only result rows from run 37309880974, excluded from s6 source union
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/tight15-s5-shard1.csv
    role: source
    note: s5-only result rows from run 37309880974, excluded from s6 source union
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/tight15-s5-shard2.csv
    role: source
    note: s5-only result rows from run 37309880974, excluded from s6 source union
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/tight15-s5-shard3.csv
    role: source
    note: s5-only result rows from run 37309880974, excluded from s6 source union
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/tight-shared-s5-shard0.csv
    role: source
    note: s5-only result rows from run 37319166001, excluded from s6 source union
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/tight-shared-s5-shard1.csv
    role: source
    note: s5-only result rows from run 37319166001, excluded from s6 source union
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/tight-shared-s5-shard2.csv
    role: source
    note: s5-only result rows from run 37319166001, excluded from s6 source union
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/tight-shared-s5-shard3.csv
    role: source
    note: s5-only result rows from run 37319166001, excluded from s6 source union
  - path: research/experiments/n11-boundary-recovery-20261006/output/all-saved-s6-expanded-audit.json
    role: verifier
    note: expanded 27-source audit with exact geometry checks and source scope
  - path: research/experiments/n11-boundary-recovery-20261006/output/all-saved-s6-expanded-loss-s5.cache
    role: data
    note: 75 new canonical s5 LOSS parents from expanded saved s6 rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next3-expanded-s5.cache
    role: data
    note: expanded 3,150-entry checkpoint, WIN 65 and LOSS 3,085
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next3-expanded-receipt.json
    role: manifest
    note: expanded checkpoint source counts, verdict totals, conflicts, and digests
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next3-expanded-cardinality.json
    role: data
    note: 3,150-entry finite class counts and dual-tight minimum cover
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next3-expanded-repair.json
    role: data
    note: 11-class additive/unique UNKNOWN s5 work 1,008; exact-15 option 1,092
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next3-expanded-repair.csv
    role: data
    note: 1,008 remaining unknown s5 work targets for the selected 11-class repair
  - path: research/experiments/n11-boundary-recovery-20261006/output/next4-model8.csv
    role: source
    note: 8 heuristic scheduling probes selected from the 84 unknown children; scores are not verdicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/next4-model8.json
    role: manifest
    note: model inputs, feature/training provenance, boundary checks, reproduction commands, and output hash
  - path: research/experiments/n11-boundary-recovery-20261006/output/next4-model8-summary.json
    role: data
    note: 8 selected replay results, all LOSS, 37,538,116 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next4-model8-s5.cache
    role: data
    note: exact cache for the 8 selected LOSS children
  - path: research/experiments/n11-boundary-recovery-20261006/output/next4-model8-sources.json
    role: manifest
    note: individual raw replay hashes and combined output digest
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next4-model8-out.csv
    role: source
    note: combined saved raw replays for the 8 model-selected children
  - path: research/experiments/n11-boundary-recovery-20261006/output/next4-remaining76.csv
    role: source
    note: the 76 rows left after removing the 8 model-selected targets, original order preserved
  - path: research/experiments/n11-boundary-recovery-20261006/output/next4-completion76-summary.json
    role: data
    note: 76 remaining supplied targets, all LOSS, 283,661,853 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next4-completion76-s5.cache
    role: data
    note: exact cache for the 76 remaining LOSS children
  - path: research/experiments/n11-boundary-recovery-20261006/output/next4-completion76-sources.json
    role: manifest
    note: individual raw replay hashes, target scope, and combined output digest
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next4-completion76-out.csv
    role: source
    note: combined saved raw replays for the remaining 76 children
  - path: research/experiments/n11-boundary-recovery-20261006/output/next4-boundary-verification.log
    role: verifier
    note: direct 100-child canonical boundary and coverage check for s4 class (1152921504766230528, 0)
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next4-s5.cache
    role: data
    note: historical merged canonical exact s5 checkpoint with 3,234 entries, WIN 65 and LOSS 3,169
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next4-receipt.json
    role: manifest
    note: source hashes, counts, nodes, and zero conflict for the merged 3,234-entry cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next4-cardinality.json
    role: data
    note: historical 3,234-cache finite class counts, secured vertices, and dual-tight minimum cover 10
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next4-repair.json
    role: data
    note: repair schedule for the 3,234-entry cache; UNKNOWN positions remain unproved
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next4-repair.csv
    role: data
    note: selected repair targets under the 3,234-entry cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next4-ranking.json
    role: data
    note: next heuristic target ranking under the 3,234-entry cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next4-best-class.csv
    role: source
    note: 87 UNKNOWN children of the next ranked class (1306043891937574912, 0)
  - path: research/experiments/n11-boundary-recovery-20261006/output/next5-model8.json
    role: manifest
    note: model inputs, features, training provenance, reproduction commands, and output hash for scheduling probes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next5-model8.csv
    role: source
    note: eight heuristic scheduling targets from the 87 UNKNOWN children; model scores are not verdicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/next5-remaining79.csv
    role: source
    note: 79 remaining target rows after removing the eight model probes, preserving order
  - path: research/experiments/n11-boundary-recovery-20261006/output/next5-model8-summary.json
    role: data
    note: supplied eight saved replays, all LOSS, 39,499,200 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next5-model8-sources.json
    role: manifest
    note: per-replay source hashes and combined output digest for the eight supplied targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next5-model8-out.csv
    role: source
    note: combined raw saved exact replays for the eight model-selected targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/next5-model8-s5.cache
    role: data
    note: exact s5 verdict cache for the eight model-selected LOSS targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/next5-completion79-summary.json
    role: data
    note: supplied 79 remaining target replays, all LOSS, 343,456,905 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next5-completion79-sources.json
    role: manifest
    note: per-replay hashes and combined output digest for the 79 supplied targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next5-completion79-out.csv
    role: source
    note: combined raw saved exact replays for the remaining 79 targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/next5-completion79-s5.cache
    role: data
    note: exact s5 verdict cache for the 79 remaining LOSS targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/next5-boundary-verification.log
    role: verifier
    note: direct geometry verifier for all 103 canonical children and coverage vertices 67, 75, 103, 105
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next5-s5.cache
    role: data
    note: historical merged canonical exact s5 cache with 3,321 entries, WIN 65 and LOSS 3,256
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next5-receipt.json
    role: manifest
    note: source counts, node totals, hashes, and zero conflicts for the merged cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next5-cardinality.json
    role: data
    note: "historical 3,321-entry class counts: 22 LOSS, 131 WIN, 3,231 UNKNOWN; secured 88/119 and dual-tight cover 9"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next5-repair.json
    role: data
    note: repair scheduling only; additive/unique union 837 for nine classes and exact-15 additive 1,049, union 1,048
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next5-repair.csv
    role: source
    note: nine-class UNKNOWN repair targets under the historical 3,321-entry cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next5-ranking.json
    role: data
    note: heuristic ranking under the 3,321-entry cache; scores are scheduling only
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next5-best-class.csv
    role: source
    note: 93 UNKNOWN children for the next ranked target (1297036967560609796, 0)
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-model8.json
    role: manifest
    note: next6 heuristic probe generation provenance; model scores are scheduling only
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-model8.csv
    role: source
    note: eight heuristic probe targets from class (1297036967560609796, 0)
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-remaining85.csv
    role: source
    note: remaining supplied targets after the eight next6 probes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-model8-summary.json
    role: data
    note: supplied eight replay results, all LOSS, 27,919,379 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-model8-sources.json
    role: manifest
    note: individual replay hashes and combined digest for next6 model probes
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next6-model8-out.csv
    role: source
    note: combined raw exact replay rows for the eight next6 probes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-model8-s5.cache
    role: data
    note: exact s5 cache for eight next6 model probes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-completion85-summary.json
    role: data
    note: 83 LOSS and 2 UNKNOWN among 85 supplied targets, 401,091,716 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-completion85-sources.json
    role: manifest
    note: individual replay hashes and target scope for next6 completion85
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next6-completion85-out.csv
    role: source
    note: raw exact replay rows for the 85 supplied targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-completion85-s5.cache
    role: data
    note: cache of LOSS results from the next6 completion85 cohort
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-hard-s5.csv
    role: source
    note: pre-completion input selecting the two UNKNOWN s5 parents for focused s6 work
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-hard-s6-summary.json
    role: data
    note: "adaptive s6 cohort summary: 179 WIN, 2 UNKNOWN from 181 positions, 61,142,979 nodes"
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-hard-s6-sources.json
    role: manifest
    note: adaptive s6 replay inputs, saved source hashes, and per-position outputs
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next6-hard-s6-out.csv
    role: source
    note: combined adaptive s6 replay rows for the two remaining parents
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-focused15m-summary.json
    role: data
    note: focused retries of the two unresolved s6 targets, both LOSS, 11,521,978 nodes total
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-focused15m-sources.json
    role: manifest
    note: individual focused s6 retry source hashes and combined output digest
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next6-focused15m-out.csv
    role: source
    note: saved raw output for the two focused s6 retries
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next6-partial-s5.cache
    role: data
    note: historical intermediate pre-s6 cache; 3,412 entries before six audited LOSS parents were merged
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next6-partial-receipt.json
    role: manifest
    note: historical intermediate receipt before focused s6 propagation and complete boundary audit
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-expanded-s6-audit.json
    role: verifier
    note: 29-source geometry audit with 1,467 unique canonical s6 keys and no conflicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-expanded-loss-s5.cache
    role: data
    note: six new s5 LOSS parents derived from audited saved s6 LOSS witnesses
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-hard-boundary-audit.json
    role: verifier
    note: full 90- and 91-child s5 parent geometry audits and propagation of focused s6 LOSS results
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-hard-derived-s5.cache
    role: data
    note: two LOSS children derived from focused s6 results after parent geometry audit
  - path: research/experiments/n11-boundary-recovery-20261006/output/next6-boundary-verification.log
    role: verifier
    note: full 103-child canonical LOSS boundary verification for class (1297036967560609796, 0), coverage 22, 32, 58, 62
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next6-s5.cache
    role: data
    note: merged canonical exact s5 cache with 3,418 entries, WIN 65 and LOSS 3,353
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next6-receipt.json
    role: manifest
    note: source counts, node totals, hashes, and zero conflicts for the merged cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next6-cardinality.json
    role: data
    note: 3,418-cache class counts 23 LOSS, 131 WIN, 3,230 UNKNOWN; secured 92/119 and dual-tight cover 8
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next6-repair.json
    role: data
    note: eight-class repair additive/unique work 744; exact-15 additive 1,052, unique union 1,048
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next6-repair.csv
    role: source
    note: eight-class UNKNOWN s5 targets under the 3,418-entry cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next6-ranking.json
    role: data
    note: heuristic ranking under the 3,418-entry cache; scores are scheduling only
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next6-best-class.csv
    role: source
    note: 95 UNKNOWN children for next ranked target (1301540292310335488, 0)
  - path: research/experiments/n11-boundary-recovery-20261006/output/next7-model8.json
    role: manifest
    note: model feature and training provenance plus reproduction instructions for next7 scheduling probes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next7-model8.csv
    role: source
    note: eight heuristic probe targets from class (1301540292310335488, 0)
  - path: research/experiments/n11-boundary-recovery-20261006/output/next7-model8-summary.json
    role: data
    note: eight supplied replay results, all LOSS, 37,732,931 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next7-model8-sources.json
    role: manifest
    note: individual raw replay hashes and combined digest for next7 model probes
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next7-model8-out.csv
    role: source
    note: raw exact replay rows for the eight model-selected targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/next7-model8-s5.cache
    role: data
    note: exact s5 LOSS cache for the eight next7 model probes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next7-completion87.csv
    role: source
    note: 87 remaining supplied targets after removing eight model probes, original order preserved
  - path: research/experiments/n11-boundary-recovery-20261006/output/next7-completion87-summary.json
    role: data
    note: 87 supplied replays, all LOSS, 396,976,088 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next7-completion87-sources.json
    role: manifest
    note: individual raw replay hashes and combined output digest for next7 completion
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next7-completion87-out.csv
    role: source
    note: raw exact replay rows for the remaining 87 targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/next7-completion87-s5.cache
    role: data
    note: exact s5 LOSS cache for the 87 completion targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/next7-boundary-verification.log
    role: verifier
    note: direct verifier for the full 111-child canonical LOSS boundary of class (1301540292310335488, 0), coverage 78, 86, 92, 94
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next7-s5.cache
    role: data
    note: merged canonical exact s5 cache with 3,513 entries, WIN 65 and LOSS 3,448
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next7-receipt.json
    role: manifest
    note: source rows, node totals, hashes, and zero conflicts for the merged next7 cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next7-local-cardinality.json
    role: data
    note: 3,513-cache counts 24 LOSS, 131 WIN, 3,229 UNKNOWN; secured 96/119 and dual-tight cover 7
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next7-local-repair.json
    role: data
    note: seven-class repair additive/unique work 649; exact-15 additive 1,131, unique 1,126
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next7-repair.csv
    role: source
    note: seven-class UNKNOWN s5 repair targets under the 3,513-entry cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next7-local-ranking.json
    role: data
    note: heuristic target ranking under the 3,513-entry cache; scores are scheduling only
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next7-best-class.csv
    role: source
    note: 97 UNKNOWN children for next ranked target (1297599642636648448, 0)
  - path: research/experiments/n11-boundary-recovery-20261006/output/next8-source-receipt.json
    role: manifest
    note: saved Actions run 37401759541 replay source rows and hashes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next8-summary.json
    role: data
    note: "supplied 97-child class result: 96 LOSS, one UNKNOWN, zero conflicts"
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next8-completion-out.csv
    role: source
    note: preserved raw completion replay rows from saved Actions artifacts
  - path: research/experiments/n11-boundary-recovery-20261006/output/next8-hard-s6-meta.json
    role: manifest
    note: saved hard6 s6 source metadata and target provenance
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next8-hard-s6-out.csv
    role: source
    note: preserved raw hard6 s6 replay rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/next8-hard-s6-result.json
    role: data
    note: "hard6 geometry audit: 100 children, 98 WIN and two LOSS, no UNKNOWN"
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next8-hard-s6-witness.out
    role: source
    note: saved exact LOSS witness replay for the hard6 parent
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next8-hard-s6-derived-s5.cache
    role: data
    note: LOSS s5 parent derived from the saved hard6 LOSS witness after geometry audit
  - path: research/experiments/n11-boundary-recovery-20261006/output/next8-exact-s5.cache
    role: data
    note: exact s5 cache reconstructed from saved next8 Actions outputs
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next8-s5.cache
    role: data
    note: 3,610-entry Actions checkpoint before expanded reverse propagation
  - path: research/experiments/n11-boundary-recovery-20261006/output/next8-expanded-s6-audit.json
    role: verifier
    note: expanded saved-s6 source audit deriving four new exact s5 LOSS parents
  - path: research/experiments/n11-boundary-recovery-20261006/output/next8-expanded-s6-derived-s5.cache
    role: data
    note: four new s5 LOSS parents from next8 expanded reverse propagation
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next8-expanded-s5.cache
    role: data
    note: intermediate 3,614-entry cache after the four derived LOSS parents
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next8-cardinality.json
    role: data
    note: Actions checkpoint counts 25 LOSS, 131 WIN, 3,228 UNKNOWN; secured 100/119 and dual-tight cover 6
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next8-repair.json
    role: data
    note: repair estimates at the 3,610-entry Actions checkpoint
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next8-ranking.json
    role: data
    note: heuristic ranking at the 3,610-entry Actions checkpoint; scheduling only
  - path: research/experiments/n11-boundary-recovery-20261006/output/next10-xserver-targets.csv
    role: source
    note: 100-child exact replay targets for class (5908722711110107136, 0)
  - path: research/experiments/n11-boundary-recovery-20261006/output/next10-xserver-summary.json
    role: data
    note: "Xserver exact replay result: all 100 children LOSS, 289,895,608 nodes"
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next10-xserver-replay.csv
    role: source
    note: preserved exact replay rows for the 100-child target class
  - path: research/experiments/n11-boundary-recovery-20261006/output/next10-xserver-s5.cache
    role: data
    note: exact s5 LOSS cache for the next10 100-child completion
  - path: research/experiments/n11-boundary-recovery-20261006/output/next9-next10-source-receipt.json
    role: manifest
    note: saved Actions run IDs, original source hashes, and normalized archive hashes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next9-summary.json
    role: data
    note: "104-child class result: 96 LOSS, three WIN, five UNKNOWN before hard-s6 propagation"
  - path: research/experiments/n11-boundary-recovery-20261006/output/next9-exact-s5.cache
    role: data
    note: exact s5 results from saved next9 Actions output
  - path: research/experiments/n11-boundary-recovery-20261006/output/next9-hard-s6-meta.json
    role: manifest
    note: saved hard-s6 targets and metadata for resolving one s5 child
  - path: research/experiments/n11-boundary-recovery-20261006/output/next9-hard-s6-out.csv
    role: source
    note: exact replay rows for the 91-child hard-s6 boundary
  - path: research/experiments/n11-boundary-recovery-20261006/output/next9-hard-s6-parent-win-receipt.json
    role: verifier
    note: direct geometry verification that all 91 legal canonical children WIN, deriving s5 parent WIN
  - path: research/experiments/n11-boundary-recovery-20261006/output/next9-hard-s6-parent-win.cache
    role: data
    note: the derived exact s5 WIN parent from the complete hard-s6 boundary
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next10-expanded-s5.cache
    role: data
    note: historical expanded checkpoint with 3,796 entries, 69 WIN and 3,727 LOSS
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next10-expanded-receipt.json
    role: manifest
    note: source hashes, row counts, and zero conflicts for the expanded 3,796-entry checkpoint
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next10-expanded-cardinality.json
    role: data
    note: historical 3,796-entry counts and dual-tight minimum cover
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next10-expanded-repair.json
    role: data
    note: historical five-class and exact-15 repair estimates at the 3,796-entry checkpoint
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next10-expanded-repair.csv
    role: source
    note: historical finite repair target list at the 3,796-entry checkpoint
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next10-expanded-ranking.json
    role: data
    note: historical heuristic ranking at the 3,796-entry checkpoint; scheduling only
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next10-expanded-best-class.csv
    role: source
    note: 108-child next target with three known LOSS and 105 UNKNOWN
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-batch-sources.json
    role: manifest
    note: run 37404904661 replay source hashes and archive integrity details
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-batch-targets.csv
    role: source
    note: 473 selected repair5 exact replay targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/repair5-batch-out.csv
    role: source
    note: "combined exact replay rows: 410 LOSS, 19 WIN, and 44 UNKNOWN"
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-batch-exact-s5.cache
    role: data
    note: exact s5 cache for the 473 Actions repair5 replay targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-batch-action-summary.json
    role: data
    note: selected class outcomes and full canonical boundary counts after the batch
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-batch-action-merged-s5.cache
    role: data
    note: merged Actions checkpoint with 4,221 exact s5 entries
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-batch-action-cardinality.json
    role: data
    note: 4,221-entry finite frontier counts and dual-tight minimum cover
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-batch-action-repair.json
    role: data
    note: repair estimates for the 4,221-entry Actions checkpoint
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-batch-action-ranking.json
    role: data
    note: heuristic ranking for the 4,221-entry Actions checkpoint
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-repair5-expanded-s5.cache
    role: data
    note: expanded merged cache with 4,225 exact entries and zero conflicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-repair5-expanded-receipt.json
    role: manifest
    note: final source counts, hashes, and verdict conflict check for the 4,225-entry cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-repair5-expanded-cardinality.json
    role: data
    note: final class counts and dual-tight minimum cover at 4,225 entries
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-repair5-expanded-repair.json
    role: data
    note: four-class repair additive/unique 304; exact-15 additive 1,231 and unique 1,221
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-repair5-expanded-ranking.json
    role: data
    note: final heuristic ranking; top target has two UNKNOWN children
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-repair5-expanded-best-class.csv
    role: source
    note: top ranked class (1873497444986126592, 0), 106 known LOSS and two UNKNOWN
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-hard2-adaptive2m-summary.json
    role: data
    note: "adaptive 2M s6 result: 137 WIN, 56 UNKNOWN, no LOSS across 193 new replays"
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-hard2-adaptive2m-sources.json
    role: manifest
    note: source hashes and provenance for the adaptive 195-child s6 boundary
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-hard2-adaptive2m-hard-s6.csv
    role: source
    note: 56 remaining UNKNOWN s6 targets for the two unresolved s5 parents
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/repair5-hard2-adaptive2m-out.csv
    role: source
    note: combined replay rows for the 193 new adaptive s6 results
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-parent-a-focused15m-summary.json
    role: data
    note: parent A focused exact replay summary, 9 rows and nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-parent-a-focused15m-sources.json
    role: manifest
    note: parent A focused replay source hashes and provenance
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/repair5-parent-a-focused15m-out.csv
    role: source
    note: parent A focused saved exact replay rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-parent-a-final33-s6-audit.json
    role: manifest
    note: parent A 33-source saved-s6 canonical audit
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-parent-a-final33-target-audit.json
    role: manifest
    note: parent A target-specific saved-s6 boundary and derived LOSS audit
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-parent-a-independent-audit.json
    role: manifest
    note: independent audit of parent A source and boundary evidence
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-parent-a-expanded-s5.cache
    role: data
    note: intermediate canonical s5 cache after parent A propagation
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-parent-a-expanded-receipt.json
    role: manifest
    note: intermediate parent A cache receipt
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-parent-b-focused15m-summary.json
    role: data
    note: parent B focused exact replay summary, 7 rows and nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-parent-b-focused15m-sources.json
    role: manifest
    note: parent B focused replay source hashes and provenance
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/repair5-parent-b-focused15m-out.csv
    role: source
    note: parent B focused saved exact replay rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-parent-b-final34-s6-audit.json
    role: manifest
    note: 34-source reverse audit, 1,849 unique s6 keys and no conflicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-parent-b-final34-target-audit.json
    role: manifest
    note: parent B target-specific saved-s6 boundary and derived LOSS audit
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-parent-b-independent-audit.json
    role: manifest
    note: independent audit of parent B source and boundary evidence
  - path: research/experiments/n11-boundary-recovery-20261006/output/repair5-parent-b-full108-verifier.log
    role: log
    note: direct geometry verifier confirms all 108 children of the LOSS class
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-parent-b-expanded-s5.cache
    role: data
    note: final canonical s5 cache, 4,243 exact entries
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-parent-b-expanded-receipt.json
    role: manifest
    note: final source counts, hashes, and zero-conflict receipt for 4,243 entries
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-parent-b-expanded-cardinality.json
    role: data
    note: final finite class counts and dual-tight three-class minimum cover
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-parent-b-expanded-repair.json
    role: data
    note: final repair work estimates under the 4,243-entry cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-parent-b-expanded-repair.csv
    role: data
    note: final three-class repair target set
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-parent-b-expanded-ranking.json
    role: data
    note: final ranked scheduling target and finite boundary summary
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-parent-b-expanded-best-class.csv
    role: data
    note: final target boundary with 3 known LOSS and 108 UNKNOWN children
  - path: research/experiments/n11-boundary-recovery-20261006/output/next12-boundary-audit.json
    role: manifest
    note: geometry audit for the next12 target as prepared against the 4,243-entry cache before probe execution
  - path: research/experiments/n11-boundary-recovery-20261006/output/next12-model8.json
    role: manifest
    note: eight scheduling probes; model scores are not verdicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/next12-run-model8-summary.json
    role: data
    note: next12 model-probe replay summary, 3 LOSS and 5 UNKNOWN
  - path: research/experiments/n11-boundary-recovery-20261006/output/next12-run-model8-sources.json
    role: manifest
    note: next12 model-probe replay provenance and source hashes
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next12-run-model8-out.csv
    role: source
    note: eight saved exact replay rows for next12 model probes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next12-run-hard5-adaptive15m-summary.json
    role: data
    note: adaptive hard-parent s6 summary; one LOSS parent, one WIN parent, three UNKNOWN
  - path: research/experiments/n11-boundary-recovery-20261006/output/next12-run-hard5-adaptive15m-sources.json
    role: manifest
    note: adaptive hard-parent source hashes and replay provenance
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next12-run-hard5-adaptive15m-out.csv
    role: source
    note: 423 saved exact s6 replay rows; verdicts are trusted saved results
  - path: research/experiments/n11-boundary-recovery-20261006/output/next12-hard5-adaptive15m-expanded-s6-audit.json
    role: manifest
    note: expanded 35-source audit with 2,272 unique canonical s6 keys and zero conflicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/next12-hard5-adaptive15m-target-audit.json
    role: manifest
    note: target-specific boundary audit with one LOSS, one WIN, and three UNKNOWN parents
  - path: research/experiments/n11-boundary-recovery-20261006/output/next12-run-parent-win-independent-audit.json
    role: manifest
    note: independent geometry and replay legality audit of the saved 91-child parent WIN; not an independent reproof of solver values
  - path: research/experiments/n11-boundary-recovery-20261006/output/next12-hard5-adaptive15m-expanded-s5.cache
    role: data
    note: ten s5 LOSS parents derived by LOSS-only reverse propagation
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next12-expanded-s5.cache
    role: data
    note: final expanded cache with 4,257 exact s5 keys
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next12-expanded-receipt.json
    role: manifest
    note: final receipt with 89 WIN, 4,168 LOSS, and zero conflicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next12-expanded-cardinality.json
    role: data
    note: finite class counts and dual-tight minimum cover under final cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next12-expanded-repair.json
    role: data
    note: finite UNKNOWN-class repair work under final cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next12-expanded-repair.csv
    role: data
    note: final finite repair target rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next12-expanded-ranking.json
    role: data
    note: final ranked scheduling target and finite boundary summary
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next12-expanded-best-class.csv
    role: data
    note: ranked boundary with four known LOSS and 104 UNKNOWN children
  - path: research/experiments/n11-boundary-recovery-20261006/output/next13-run-model8-independent-audit.json
    role: manifest
    note: independent geometry, source, legal-count, AND-polarity and boundary audit for six saved exact probe rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/next13-run-model8-summary.json
    role: data
    note: six completed exact probes, 3 WIN and 3 LOSS; two scheduled probes were not dispatched
  - path: research/experiments/n11-boundary-recovery-20261006/output/next13-run-model8-sources.json
    role: manifest
    note: next13 saved-probe source hashes and provenance
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next13-run-model8-out.csv
    role: source
    note: six saved exact next13 replay rows; 57,081,707 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next13-run-model8-new-exact-s5.cache
    role: data
    note: six new exact verdicts for next13 probes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next13-saved-s6-summary.json
    role: data
    note: saved s6 source audit and LOSS-only s5 parent derivation summary
  - path: research/experiments/n11-boundary-recovery-20261006/output/next13-saved-s6-derived-s5.cache
    role: data
    note: exact s5 LOSS parents derived from saved s6 sources
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next13-expanded-s5.cache
    role: data
    note: historical expanded cache with 4,263 exact s5 keys
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next13-expanded-receipt.json
    role: manifest
    note: final receipt with 92 WIN, 4,171 LOSS, and zero conflicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next13-expanded-cardinality.json
    role: data
    note: finite class counts and dual-tight minimum cover under current cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next13-expanded-repair.json
    role: data
    note: finite UNKNOWN-class repair estimates under current cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next13-repair.csv
    role: data
    note: selected finite repair targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next13-finite-independent-audit.json
    role: manifest
    note: independent arithmetic audit of all class statuses, secured coverage, four-class cover and rational dual
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next13-expanded-ranking.json
    role: data
    note: historical ranked class and finite boundary summary
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next13-best-class.csv
    role: data
    note: ranked 57-child boundary with six known LOSS and 51 UNKNOWN
  - path: research/experiments/n11-boundary-recovery-20261006/output/next14-run-model8-independent-audit.json
    role: manifest
    note: independent saved-source, geometry, and complete-boundary audit for next14 exact probes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next14-run-model8-summary.json
    role: data
    note: seven completed exact probes, five LOSS and two WIN; one scheduled probe not dispatched
  - path: research/experiments/n11-boundary-recovery-20261006/output/next14-run-model8-sources.json
    role: manifest
    note: next14 replay provenance and source hashes
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next14-run-model8-out.csv
    role: source
    note: seven saved exact next14 replay rows, 44,039,611 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next14-run-model8-new-exact-s5.cache
    role: data
    note: seven exact verdicts from the next14 probe run
  - path: research/experiments/n11-boundary-recovery-20261006/output/next14-saved-s6-summary.json
    role: data
    note: saved s6 source summary and derived s5 parent results
  - path: research/experiments/n11-boundary-recovery-20261006/output/next14-saved-s6-derived-s5.cache
    role: data
    note: exact s5 losses derived from saved s6 evidence
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next14-expanded-s5.cache
    role: data
    note: current expanded cache with 4,270 exact s5 entries
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next14-expanded-merge.json
    role: manifest
    note: source merge report for the 4,270-entry expanded cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next14-expanded-receipt.json
    role: manifest
    note: final cache receipt with 94 WIN, 4,176 LOSS, and zero conflicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next14-expanded-cardinality.json
    role: data
    note: finite class counts and dual-tight minimum cover under current cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next14-expanded-repair.json
    role: data
    note: finite UNKNOWN-class repair work under current cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next14-repair.csv
    role: data
    note: selected finite repair targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next14-finite-independent-audit.json
    role: manifest
    note: independent arithmetic audit of all class statuses, secured coverage, four-class cover and rational dual
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next14-expanded-ranking.json
    role: data
    note: current ranked scheduling target and finite boundary summary
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next14-best-class.csv
    role: data
    note: ranked boundary with four known LOSS and 104 UNKNOWN children
  - path: research/experiments/n11-boundary-recovery-20261006/output/next15-hard3-adaptive15m-summary.json
    role: data
    note: "hard3 adaptive s6 run summary: 162 exact replays, 157 WIN and 5 LOSS"
  - path: research/experiments/n11-boundary-recovery-20261006/output/next15-hard3-adaptive15m-sources.json
    role: manifest
    note: individual replay hashes and source provenance for hard3 s6 run
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next15-hard3-adaptive15m-out.csv
    role: source
    note: archived hard3 exact s6 replay rows, 89,196,422 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next15-hard3-independent-boundary-audit.json
    role: manifest
    note: independent complete safe s6 geometry and parent outcomes for the three hard3 parents
  - path: research/experiments/n11-boundary-recovery-20261006/output/next15-s6-propagation-independent-audit.json
    role: manifest
    note: post-run independent source-hash, replay-binding, AND propagation, and reverse LOSS audit; solver outcomes are not re-proved
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next15-finite-independent-audit.json
    role: manifest
    note: independent finite class-status, coverage, four-class cover, and rational-dual arithmetic audit
  - path: research/experiments/n11-boundary-recovery-20261006/output/next15-hard-s6-summary.json
    role: data
    note: reused saved s6 audit summary; it records zero saved UNKNOWN rows eligible for retry
  - path: research/experiments/n11-boundary-recovery-20261006/output/next15-expanded-s6-audit.json
    role: manifest
    note: expanded 36-source reverse audit, canonical s6 keys and LOSS-only s5 parent derivation
  - path: research/experiments/n11-boundary-recovery-20261006/output/next15-combined-s5-independent-audit.json
    role: manifest
    note: independent consistency check of combined s5 cache and class boundary
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next15-expanded-s5.cache
    role: data
    note: current expanded cache with 4,385 exact keys; SHA-256 8a199081c83868ef931f6ef2e9a8b3d02ce2988b86893984abc6d5d3843f4b59
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next15-expanded-merge.json
    role: manifest
    note: merge receipt with 95 WIN, 4,290 LOSS, and zero conflicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next15-expanded-receipt.json
    role: manifest
    note: final class-verdict and finite-frontier source receipt
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next15-expanded-cardinality.json
    role: data
    note: final finite class statuses and dual-tight minimum cover
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next15-expanded-repair.json
    role: data
    note: final finite repair scheduling work
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next15-repair.csv
    role: data
    note: final finite repair target rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next15-expanded-ranking.json
    role: data
    note: final ranked class and scheduling boundary
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next15-best-class.csv
    role: data
    note: ranked class boundary with seven known LOSS and 91 UNKNOWN children
  - path: research/experiments/n11-boundary-recovery-20261006/output/next16-run-model8-summary.json
    role: data
    note: "next16 supplied-target run summary: 2 WIN, 1 LOSS, 1 UNKNOWN, four not dispatched"
  - path: research/experiments/n11-boundary-recovery-20261006/output/next16-run-model8-sources.json
    role: manifest
    note: raw replay and source byte hashes for next16 supplied-target run
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next16-run-model8-out.csv
    role: source
    note: four dispatched replay rows with three exact and one UNKNOWN, totaling 43,173,440 nodes
  - path: research/experiments/n11-boundary-recovery-20261006/output/next16-run-model8-independent-audit.json
    role: manifest
    note: independent geometry, cache-delta and source audit; exact solver verdicts are not re-proved
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next16-finite-independent-audit.json
    role: manifest
    note: independent finite class-status, coverage, cover and dual arithmetic audit
  - path: research/experiments/n11-boundary-recovery-20261006/output/next16-run-model8-new-exact-s5.cache
    role: data
    note: three durable exact s5 rows from four dispatched model targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/next16-saved-s6-summary.json
    role: data
    note: separate audit of previously saved s6 sources; next16 derived-cache delta was empty
  - path: research/experiments/n11-boundary-recovery-20261006/output/next16-saved-s6-derived-s5.cache
    role: data
    note: LOSS-only s5 parent derivations from saved exact s6 rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next16-expanded-s5.cache
    role: data
    note: "historical 4,388-entry cache checkpoint with 97 WIN and 4,291 LOSS; SHA-256 ddc997e18480ed9ceb669148dcc46166eae1bb6ae9ec08d07e4954d6aa91c081"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next16-expanded-receipt.json
    role: manifest
    note: next16 cache merge receipt, exact source hashes and zero conflicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next16-expanded-cardinality.json
    role: data
    note: 3,384 class statuses, secured coverage, minimum additional cover and rational dual
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next16-expanded-repair.json
    role: data
    note: finite repair scheduling results for the 4,388-entry snapshot
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next16-repair.csv
    role: data
    note: selected finite repair targets for next16 cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next16-expanded-ranking.json
    role: data
    note: ranked next class scheduling target; not a verdict
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next16-best-class.csv
    role: data
    note: target boundary for the top ranked class
  - path: research/experiments/n11-boundary-recovery-20261006/output/next17-run-model8-summary.json
    role: data
    note: next17 model8 s5 supplied-target run summary
  - path: research/experiments/n11-boundary-recovery-20261006/output/next17-run-model8-sources.json
    role: manifest
    note: next17 model8 source and raw replay hashes
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next17-run-model8-out.csv
    role: source
    note: next17 model8 exact s5 replay rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/next17-run-model8-independent-audit.json
    role: manifest
    note: independent source, target geometry and cache-delta audit; solver outcomes are trusted
  - path: research/experiments/n11-boundary-recovery-20261006/output/next17-completion93-summary.json
    role: data
    note: next17 completion93 s5 run summary
  - path: research/experiments/n11-boundary-recovery-20261006/output/next17-completion93-sources.json
    role: manifest
    note: next17 completion93 source and replay hashes
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next17-completion93-out.csv
    role: source
    note: next17 completion93 exact s5 replay rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/next17-hard5-adaptive15m-summary.json
    role: data
    note: adaptive s6 run summary for five s5 parents
  - path: research/experiments/n11-boundary-recovery-20261006/output/next17-hard5-adaptive15m-sources.json
    role: manifest
    note: adaptive s6 raw replay and source hashes
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/next17-hard5-adaptive15m-out.csv
    role: source
    note: 214 new s6 child replays, 200 WIN and 14 LOSS
  - path: research/experiments/n11-boundary-recovery-20261006/output/next17-hard5-independent-boundary-audit.json
    role: manifest
    note: geometry audit for the five full s6 parent boundaries
  - path: research/experiments/n11-boundary-recovery-20261006/output/next17-s6-propagation-independent-audit.json
    role: manifest
    note: independent source hashes, complete geometry and reverse propagation; solver values are inputs
  - path: research/experiments/n11-boundary-recovery-20261006/output/next17-full110-class-verification.json
    role: manifest
    note: direct geometry verification of the full 110-child LOSS class
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-expanded-s5.cache
    role: data
    note: "current 4,515-entry cache with 97 WIN and 4,418 LOSS; SHA-256 2fa27a15625af7449ca8f3fa21e683ba2e13a5d4deb99f8919d02ea61b59c82c"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-expanded-receipt.json
    role: manifest
    note: next17 cache merge receipt and zero-conflict accounting
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-expanded-cardinality.json
    role: data
    note: finite class statuses, secured vertices, and minimum cover/dual
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-expanded-repair.json
    role: data
    note: finite repair schedule for the next17 cache snapshot
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-expanded-repair.csv
    role: data
    note: materialized next17 repair targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-expanded-ranking.json
    role: data
    note: next17 ranked class scheduling target
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-expanded-best-class.csv
    role: data
    note: ranked target boundary
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-finite-independent-audit.json
    role: manifest
    note: independent arithmetic audit of class statuses, secured coverage, and matching cover/dual bounds
  - path: research/experiments/n11-boundary-recovery-20261006/output/next18-model8.csv
    role: data
    note: "next18 model8 probe schedule; eight supplied s5 targets for the ranked class"
  - path: research/experiments/n11-boundary-recovery-20261006/output/next18-full-unknown-targets.csv
    role: data
    note: "next18 full 99-child UNKNOWN target boundary"
  - path: research/experiments/n11-boundary-recovery-20261006/output/next18-prior-s5-unknown-audit.json
    role: manifest
    note: "archive-scope audit proving the 99 children have no prior same-budget UNKNOWN replay"
  - path: research/experiments/n11-boundary-recovery-20261006/output/next18-saved-s6-summary.json
    role: manifest
    note: "target-specific saved-37-source s6 audit; all 99 parents UNKNOWN, no new exact rows"
  - path: research/experiments/n11-boundary-recovery-20261006/output/next18-saved-s6-derived-s5.cache
    role: data
    note: "empty derived cache from the next18 saved-s6 target audit"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-probe9-prior-s5-replay-audit.json
    role: manifest
    note: "probe9の過去exact/raw replayと同budget UNKNOWNの再利用監査"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-probe9-saved-s6-sources.json
    role: manifest
    note: "probe9と92親のsaved s6 source/hash manifest"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-probe9-saved-s6-summary.json
    role: manifest
    note: "saved s6とのprobe9 intersectionとderived s5 verdict監査"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-probe9-sources.json
    role: manifest
    note: "9件probe exact replayのsource、node、hash記録"
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/post-next17-dual-tight-92-probe9-out.csv
    role: source
    note: "probe9の9 exact LOSS raw replay rows"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-probe9-summary.json
    role: data
    note: "probe9: 9 LOSS、0 WIN、0 UNKNOWN、21,927,853 nodes"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-probe9-new-exact-s5.cache
    role: data
    note: "probe9から統合する9 canonical s5 LOSS"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-probe9-merge-receipt.json
    role: manifest
    note: "probe9 exact deltaとbase 4,515-entry cacheの衝突なしmerge receipt"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-probe9-merged-s5.cache
    role: data
    note: "probe9後の4,524-entry exact s5 cache"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-residual-s5-history-audit.json
    role: manifest
    note: "残り83件の再利用可能exact結果と同budget UNKNOWN履歴監査"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-residual83.csv
    role: source
    note: "probe9を除いた83 canonical s5 targets"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-residual83-sources.json
    role: manifest
    note: "83件exact replayのsource、node、hash記録"
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/post-next17-dual-tight-92-residual83-out.csv
    role: source
    note: "83件completionのraw replay rows"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-residual83-summary.json
    role: data
    note: "83件: 81 LOSS・2 UNKNOWN・0 WIN、343,344,159 nodes"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-residual83-new-exact-s5.cache
    role: data
    note: "83件replayから統合する81 canonical s5 LOSS"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-residual83-merge-receipt.json
    role: manifest
    note: "residual83 exact deltaとprobe9後cacheの衝突なしmerge receipt"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-residual83-merged-s5.cache
    role: data
    note: "residual83後、s6導出WINを加える前の4,605-entry exact s5 cache"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-saved-s6-summary.json
    role: manifest
    note: "92 targetsと38-source saved s6 exact evidenceのintersection監査"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-s6-unresolved-boundary.csv
    role: source
    note: "残る2 UNKNOWN s5親の完全162-child canonical s6 boundary"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-s6-unresolved-boundary-meta.json
    role: manifest
    note: "162 s6 childrenとparent incidenceのgeometry metadata"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-s6-unresolved-sources.json
    role: manifest
    note: "focused s6 replayのsaved source/hash manifest"
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/post-next17-dual-tight-92-s6-unresolved-out.csv
    role: source
    note: "160 exact s6 WIN raw replay rows"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-s6-unresolved-summary.json
    role: data
    note: "160 s6 WIN、48,281,975 nodes; one parent 80/80 WIN, one 80/82 with two unexecuted"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-s6-unresolved-final-audit.json
    role: manifest
    note: "38-source s6 cache intersection, parent outcomes, and derived s5 WIN audit"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-s6-unresolved-final-derived-s5.cache
    role: data
    note: "80/80 exact WIN s6 boundaryから導出した1件のcanonical s5 WIN"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-final-saved-s6-sources.json
    role: manifest
    note: "all saved s6 sources including the 160 new exact rows; source hashes and verdict totals"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-win-witness-geometry-audit.json
    role: verifier
    note: "independent geometry check of full 95-child s4 boundary and 80/80 exact WIN s6 witness"
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_92_win_witness.py
    role: verifier
    note: "rebuilds and checks the s4/s5/s6 witness geometry and cache consistency"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-final-merged-s5.cache
    role: data
    note: "final canonical exact cache: 4,606 entries, WIN 98, LOSS 4,508, no conflicts"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-final-merge-receipt.json
    role: manifest
    note: "source cache merge receipt for the final 4,606-entry exact cache"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-final-cardinality.json
    role: data
    note: "recomputed 3,384-class status, 113/119 secured vertices, minimum cover 3 and matching rational dual"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-final-repair.json
    role: data
    note: "new additive-optimal three-class repair and exact distinct union size for that selected repair"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-final-repair.csv
    role: data
    note: "distinct UNKNOWN s5 targets in the recomputed additive repair"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-final-ranking.json
    role: data
    note: "dual-tight selected-class ranking; next class has 92 UNKNOWN s5 children"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-final-ranking-sources.json
    role: manifest
    note: "hash manifest for cache, repair/cardinality inputs, geometry and ranking scripts, and generated targets"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-artifact-hashes.json
    role: manifest
    note: "SHA-256 inventory for the 51 saved dual-tight-92 result, source, audit, and helper files"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-92-final-next-targets.csv
    role: data
    note: "next exact replay schedule for class (10376293541461626880, 131072), 92 UNKNOWN s5 targets"
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py
    role: source
    note: "rebuilds exact geometry and materializes only the selected dual-tight scheduling candidates"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-raw-history-audit.json
    role: manifest
    note: "hash-validated scan of 872 saved CSV replay files; no matching exact row or same-budget UNKNOWN"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-saved-s6-audit.json
    role: manifest
    note: "complete saved-s6 intersection for the 92 UNKNOWN s5 targets; all remain UNKNOWN and no s5 verdict is derived"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-saved-s6-derived-s5.cache
    role: data
    note: "empty exact s5 delta from the saved-s6 boundary audit"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8.csv
    role: source
    note: "eight lowest-legal-count UNKNOWN s5 inputs for the next dual-tight class; order is scheduling only"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-rank1-probe8.csv
    role: source
    note: "latest-main duplicate schedule with the same eight canonical s5 keys already replayed in the probe8 batch"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-sources.json
    role: manifest
    note: "probe solver, cache, audit, input, and raw-result source hashes"
  - path: research/experiments/n11-boundary-recovery-20261006/output/raw/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-out.csv
    role: source
    note: "eight exact s5 replays: seven LOSS and one WIN, 33,123,142 nodes"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-new-exact-s5.cache
    role: data
    note: "eight new exact s5 verdicts from the low-cost probe"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-summary.json
    role: data
    note: "probe counts, nodes, and source-bound output hashes"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-runner-summary.json
    role: source
    note: "local exact replay runner summary"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-merge-receipt.json
    role: manifest
    note: "exact s5 cache merge receipt with zero verdict conflicts"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-merged-s5.cache
    role: data
    note: "current exact s5 cache after adding the eight audited probe rows; 4,614 entries"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-geometry-audit.json
    role: verifier
    note: "full 103-child s4 geometry and exact s5 WIN witness incidence audit; class is WIN"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-cardinality.json
    role: data
    note: "recomputed 3,384-class status, secured vertices, integer cover and rational dual"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-repair.json
    role: data
    note: "reoptimized additive three-class repair and distinct UNKNOWN s5 union"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-repair-targets.csv
    role: data
    note: "distinct UNKNOWN s5 targets in the reoptimized repair"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-next-ranking.json
    role: data
    note: "recomputed dual-tight candidate ranking after the WIN class was excluded"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-next-targets.csv
    role: data
    note: "next 92 UNKNOWN s5 targets for class (1297036692683751424, 16384)"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-next-ranking-sources.json
    role: manifest
    note: "hash bindings for the recomputed repair, cardinality, geometry, and ranking inputs"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-artifact-hashes.json
    role: manifest
    note: "SHA-256 inventory of the 35 probe, cache, audit, ranking, solver-source, and helper files"
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/audit_s5_raw_history.py
    role: verifier
    note: "checks exact replay history and same-budget UNKNOWN rows over fixed CSV search roots"
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/prepare_dual_tight_probe.py
    role: source
    note: "selects only cache-, saved-s6-, and raw-history-cleared targets"
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/collect_dual_tight_probe.py
    role: verifier
    note: "validates and collects per-root exact probe outputs into durable CSV and cache artifacts"
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_s4_win.py
    role: verifier
    note: "rebuilds the complete canonical s5 boundary and checks exact WIN witness parent incidence"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-unknown2-s5-parents.csv
    role: source
    note: "two remaining UNKNOWN s5 parents isolated for complete s6-boundary evaluation"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-run/summary.json
    role: data
    note: "172-key complete s6 union; 163 exact WIN and 2 UNKNOWN replays; 7 children left unstarted after s4 WIN"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-raw-all.csv
    role: source
    note: "all 165 new replay rows, including the two UNKNOWN results"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-raw-exact.csv
    role: source
    note: "163 exact s6 WIN replay rows; no s6 LOSS was found"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-exact-s6.cache
    role: data
    note: "new canonical exact s6 cache; UNKNOWN rows excluded"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-sources.json
    role: manifest
    note: "hash bindings for all 497 per-target run files, raw outputs, saved audits, and solver source"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-interim-merged-s5.cache
    role: data
    note: "base s5 cache merged with the s6-derived WIN before reverse-incidence audit"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-interim-merge-receipt.json
    role: manifest
    note: "conflict-free pre-propagation merge used as the reverse audit comparison cache"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-reverse-audit.json
    role: verifier
    note: "349 canonical s6 audit; 26 reply27 LOSS parents all duplicate known cache rows; zero conflicts or new LOSS"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-reverse-loss-s5.cache
    role: data
    note: "empty new s5 LOSS delta; no LOSS s6 witness was produced"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-final-merged-s5.cache
    role: data
    note: "current exact s5 cache after one s6-derived exact WIN; 4,715 entries"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-final-merge-receipt.json
    role: manifest
    note: "three-source exact cache merge with WIN 102, LOSS 4,613, conflict 0"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-geometry-audit.json
    role: verifier
    note: "complete 96-child s4 geometry; 94 LOSS, 1 WIN, 1 UNKNOWN; verifies the s5 WIN has all 85 exact s6 children WIN"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-cardinality.json
    role: data
    note: "recomputed all 3,384 classes, secured vertices, minimum cover, and rational dual"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-repair.json
    role: data
    note: "reoptimized three-class repair with 284 distinct UNKNOWN s5 targets"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-repair-targets.csv
    role: data
    note: "materialized UNKNOWN s5 union of the current additive-optimal repair"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-repair-ranking-input.json
    role: source
    note: "schema adapter for exact cache-aware repair ranking"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-ranking.json
    role: data
    note: "re-ranked dual-tight repair after the s4 WIN class was excluded"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-next-targets.csv
    role: data
    note: "next ranked class (10448491872987906048, 0), 92 UNKNOWN s5 children"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-ranking-sources.json
    role: manifest
    note: "source hashes for exact cache, repair, cardinality, geometry libraries, and ranking outputs"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-artifact-hashes.json
    role: manifest
    note: "36-file SHA-256 inventory with nested 497-file run manifest"
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_s4_win_from_s6.py
    role: verifier
    note: "independently rebuilds s4, s5, and s6 boundaries for an s6-derived exact s5 WIN"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-rank1-10448491872987906048-0-raw-history-audit-20261008.json
    role: manifest
    note: "1,470 CSV history scan for the rank-1 92 UNKNOWN s5 targets; no prior exact or same-budget UNKNOWN rows"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-rank1-10448491872987906048-0-saved-s6-37source-summary-20261008.json
    role: manifest
    note: "full target-boundary audit against the 37-source saved s6 corpus; all 92 s5 parents remain UNKNOWN"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-rank1-10448491872987906048-0-saved-s6-37source-derived-s5-20261008.cache
    role: data
    note: "empty exact s5 delta from the 37-source saved s6 audit; no verdict derived"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-rank1-10448491872987906048-0-saved-s6-37source-full-20261008.json.gz
    role: data
    note: "complete canonical s6 child records for the 37-source target audit"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-rank1-10448491872987906048-0-saved-s6-10source-summary-20261008.json
    role: manifest
    note: "supplemental 10-source s6 audit; nine sources overlap the 37-source corpus and one is additional; all 92 parents remain UNKNOWN"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-rank1-10448491872987906048-0-saved-s6-10source-derived-s5-20261008.cache
    role: data
    note: "empty exact s5 delta from the supplemental saved s6 audit; no verdict derived"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-rank1-10448491872987906048-0-saved-s6-10source-full-20261008.json.gz
    role: data
    note: "complete canonical s6 child records for the supplemental source audit"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-rank1-10448491872987906048-0-audit-artifact-hashes-20261008.json
    role: manifest
    note: "SHA-256 and size inventory for rank-1 raw-history and saved-s6 audits, their inputs, and verifier scripts"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-1297036692683751424-16384-probe8.csv
    role: data
    note: "incoming main schedule; canonical keys and order matched the already completed local input"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-geometry-reaudit-20261008.json
    role: manifest
    note: "complete 110-child geometry re-audit for class (1297036692683751424,16384), exact WIN witness verified"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-probe8-geometry-reaudit-20261008.json
    role: manifest
    note: "complete 98-child geometry re-audit for class (10448351685255364608,0), exact WIN witness verified"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-geometry-reaudit-20261008.json
    role: manifest
    note: "complete 96-child geometry and s6 witness audit for class (10448351169859289088,0)"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-reconciled-checkpoint-artifact-hashes-20261008.json
    role: manifest
    note: "valid 673-file SHA-256 inventory, including raw replay inputs/outputs/logs and experiment scripts"
scope: "The finite reply27 frontier through the verified dd9db22af87dbcf65ced44631544e5596c4227e8 checkpoint: exact s5 cache 4,715 entries, all 3,384 s4 classes, saved s5/s6 boundary audits, current repair, and target-specific audit for the next 92 UNKNOWN s5 children."
evidence: "Exact solver verdicts only; canonical geometry and complete s4/s5/s6 boundaries are independently rebuilt. Exact s6 LOSS alone may propagate to safe canonical s5 parents; UNKNOWN/WIN do not. Three processed classes have complete geometry-verified exact WIN witnesses, including one s5 WIN derived from all 85/85 exact WIN s6 children. Cache has 4,715 entries (WIN 102, LOSS 4,613, conflict 0); s4 status is LOSS 29, WIN 187, UNKNOWN 3,168, with 113/119 secured. Minimum additional classes and rational LP dual are both 3; the current repair covers 284 distinct UNKNOWN s5 children. {60,27} and empty-board status remain UNKNOWN."
---

# 11×11 reply27の保存済みexact結果から復元したcache frontier

この項目は、失敗したActions runからのexact結果回収・監査と、その後のlocal finite searchおよびcache条件下のfrontier計算を記録する。初期回収段階では保存済み結果を再計算せずに永続化し、別の作業時点で`origin/main`にも同等のcache回収と正規化修正が到着していた。後続のlocal search結果は個別の保存済みreplayとsummaryに対応する有限計算であり、空盤の終端証明とは区別する。

## 保存結果と計算

基準run `37334644565` の初期snapshotはcanonical s5が2,529件（WIN 63、LOSS 2,466）。保存済みmodel8 cacheは追加でLOSSを8件増やし、shared s6 run `37336924568` は16件（WIN 10、LOSS 6、UNKNOWN 0）を含む。shared s6 metadataは66の親子relation、65の親候補を記録している。16キー中13キーがnoncanonicalだったため、各盤面の安全性、D4正規化、およびsafe s6から一点削除して得る親子relationを独立にgeometryから検証した。6つのLOSS s6結果から25件のs5 LOSS witnessを派生した。

失敗したcompletion86 run `37337141197` の保存CSVを監査し、86件すべてLOSS、合計361,568,619 nodesと確認した。基準cache、model8、shared s6派生分、completion86の結果を衝突なく統合した初期snapshotは2,648件（WIN 63、LOSS 2,585、conflict 0）。Actions run `37338193154` から独立に再構成されたcurrent cacheと全2,648行が一致した。s4 class `(1297036692816953344, 0)` のcanonical s5境界105件はすべてLOSSで、`verify_reply27_loss_class_cache.py` により検査した。

初期2,648-entry snapshotでs4 classはWIN 129、LOSS 18、UNKNOWN 3,237。root verticesは119個中72個がsecuredで47個がremaining。残りを覆う最小追加class数は13で、rational LP dualの値13と整数被覆の最適値13が一致した。初期13-class repairのUNKNOWN s5 unionは1,227件（加法目的値も1,227）。rank上位のtarget `(1298162592590594048, 0)` は101子の内訳が既知LOSS 12、UNKNOWN 89で、vertices 70、72、100、108をcoverした。

この候補のremaining 81 s5位置をlocal cold runで調べ、76 LOSS・5 UNKNOWN・0 WIN、paid nodes合計526,111,188を得た。残る5 UNKNOWNは続けてsolverに渡さず、生成済みの5親境界入力だけを保存した。

Actions run `37339663025` のmodel-hard2はcanonical s6境界169件をすべてWINと報告した。`verify_model_hard2_results.py --saved-raw-only` は独立に構成した境界とcanonical key・parent incidenceが一致すること（親の子数86と84）、全replayがsafe・canonical・legalであること、欠落・重複がないこと、両s5親が全子WINによりWINとなることを検査した。s5親はそれぞれ86/86、84/84がWINで、WIN判定値は保存されたActions exact solverの出力に基づく。この証拠でclass `(1298162592590594048, 0)` はWIN。

中間cacheは2,732件（WIN 65、LOSS 2,667、conflict 0）。当時のs4 classはLOSS 18、WIN 131、UNKNOWN 3,235、secured vertices 72/119、remaining 47で、最小追加class数13がrational LP dualと一致した。中間13-class repairのUNKNOWN s5 unionは1,237件。最初の2,648-entry snapshotにおける1,227 unionとは別の値である。

続くclass `(1297036693756510208, 0)` はcanonical s5境界100件を全てLOSSと判定した。既知LOSS 10件に、model8で選んだ8件（19,867,831 nodes）と残る82件（301,036,761 nodes）のexact LOSSを加えた。`verify_reply27_loss_class_cache.py` は幾何から100子の境界とcoverage vertices 56, 64, 90, 96を再構成し、全境界がLOSSであることを検査した。

当時の2,822-entry checkpointはWIN 65、LOSS 2,757、conflict 0。s4 classはLOSS 19、WIN 131、UNKNOWN 3,234、secured vertices 76/119、uncovered 43。最小追加class数は12でrational LP dual値12と整数被覆最適値12が一致し、12-class repairのadditive UNKNOWN s5数とdistinct unionはいずれも1,147だった。これはそのcheckpointでの作業量であり、UNKNOWN classをLOSSと証明するものではない。

その後、Actions run `37269759034` のhard9 saved replay 816件（WIN 729、LOSS 81、UNKNOWN 6、901,901,494 nodes）を取り込み、13-source auditは1,000 unique s6 keys（WIN 907、LOSS 87、UNKNOWN-only 6）を集計した。UNKNOWNは親へ伝播しない。s6 LOSSから列挙された442 canonical safe s5 parentsのうち347はreply27関連で、185 LOSS parentは既知、162が新規LOSSとなった。先行する9-source reverse passは36 parentsを含み、25は既知LOSS、1件を追加した。これにより2,831-entry checkpointは2,993 entries（WIN 65、LOSS 2,928、conflict 0）となった。

当時のclass `(1153202979717779456, 0)` はmodel8の8 LOSS（19,329,773 nodes）と残る83 targetsの82 LOSS・1 UNKNOWN（352,645,468 nodes）を合わせて97 LOSS・1 UNKNOWNだった。partial auditは98 canonical s5 childrenをdirect geometryから再生成したが、classはその時点では未確定だった。親 `(1297318167659941888, 0)` の86-child s6 boundaryもsolver前の保存入力だった。当時の3,075-entry checkpointはWIN 65、LOSS 3,010、conflict 0で、class countsはLOSS 19、WIN 131、UNKNOWN 3,234、secured vertices 76/119、minimum cover/dual 12、12-class additive/unique UNKNOWN s5 work 1,056、exact-15 option 1,101だった。

その後、86-child hard1 s6 cohortを2,000,000 budgetで処理し85 WIN・1 UNKNOWN、32,291,732 nodesを記録した。唯一残ったs6 key `(1297320366683197440, 0)` を15,000,000 budgetでfocused retryしLOSS、4,508,377 nodesとなった。`verify_next3_hard1_loss_witness.py` はsolver verdictを再証明せず、full 86-child boundary、metadata/CSV一致、safe canonical legal-count、LOSS witnessの境界所属、reverse point deletionによるs5 parent incidenceを独立geometryで検査し、parent `(1297318167659941888, 0)` のLOSSを導いた。これでclass `(1153202979717779456, 0)` の98 canonical s5 childrenはすべてLOSSとなり、runtime geometryのdirect boundary verifierもcoverage `{12,20,48,50}` と共に確認した。post-hard1 checkpointは3,076 entries（WIN 65、LOSS 3,011、conflict 0）。

追加saved sourceはActions runs `37320154141` (170 s6 rows)、`37339357570` (16 rows)、failed run `37339329716` (32 rows) の218 raw rowsで、200 new canonical keysだった。tight15とtight-shared artifactsはs5 rowsのみで既存3,075 cacheに含まれるためexpanded s6 source unionから除外した。expanded 27-source auditは1,286 unique canonical s6 keys（1,167 WIN、113 LOSS、6 UNKNOWN-only、conflict 0）を記録。113 LOSSから590 safe canonical s5 parentsを列挙し、そのうち447はreply27関連、372は既知LOSS、75はnew LOSSだった。hard1 parentもこの75件に含まれる。3,075 checkpointへ75 LOSSをmergeしたexpanded snapshotは3,150 entries（WIN 65、LOSS 3,085、conflict 0）。Cardinalityでs4 classはLOSS 20、WIN 131、UNKNOWN 3,233、secured 80/119。minimum additional class coverとrational dualはいずれも11。repair scheduleは11-class additive/unique 1,008 unknown s5 work、exact-15 option 1,092であり、未確定classesの証明ではない。

その後、s4 class `(1152921504766230528, 0)` のnext4 finite searchを完了した。3150-cacheから抽出した84 UNKNOWN s5子のうち8 model-ranked位置は全てLOSS（37,538,116 nodes）、残る76も全てLOSS（283,661,853 nodes）だった。`next4-boundary-verification.log` はsafe canonicalな全100子境界、coverage `{23,24,30,31}`、cache中の100 LOSSをdirect geometryで確認した。判定は保存済みexact solver出力と境界監査に基づく有限class結果である。

統合cache [post-next4-s5.cache](../../experiments/n11-boundary-recovery-20261006/output/post-next4-s5.cache) は3,234件（WIN 65、LOSS 3,169、conflict 0）。[receipt](../../experiments/n11-boundary-recovery-20261006/output/post-next4-receipt.json) は3150-cacheとnext4両replay sourceのhash・件数を記録する。cardinalityはs4 class 21 LOSS、131 WIN、3,232 UNKNOWN、secured 84/119、remaining 35を返した。minimum additional class cover 10はrational LP dual 10と一致。repair scheduleのadditive/unique UNKNOWN s5 unionは924、exact-15 optionは1,054で、いずれも探索作業量でありUNKNOWN classの証明ではない。次のheuristic対象`(1306043891937574912, 0)`は103子のうち既知LOSS 16、UNKNOWN 87、coverage vertices `{67,75,103,105}`。`next4-model8.json`と`post-next4-ranking.json`に入力・hash・再現手順を保存した。

この103-child classは、next5 model8で選んだ8 UNKNOWN子（39,499,200 nodes）と残る79子（343,456,905 nodes）がすべてLOSSとなり、既知16 LOSSと合わせて全103 canonical childrenがLOSS。`next5-boundary-verification.log`はcoverage `{67,75,103,105}` と共に直接境界を検査した。保存されたexact solver結果を前提とする有限class判定であり、モデルranking自体を勝敗根拠とはしない。

当時のpost-next5 cacheは3,321 entries（WIN 65、LOSS 3,256、conflict 0）。s4 classはLOSS 22、WIN 131、UNKNOWN 3,231、secured 88/119、remaining 31。最小追加class coverとrational LP dualは9で一致した。repair scheduleは9-class additive/unique UNKNOWN s5 union 837、exact-15 additive 1,049・unique 1,048。これらは当時の探索作業量であり、現在のcache値ではない。
当時の3,321-entry cacheでの次候補は`(1297036967560609796, 0)`で、103子中10 LOSS・93 UNKNOWN、coverage vertices `{22,32,58,62}`。`post-next5-ranking.json`と`post-next5-best-class.csv`はtarget scheduling用で、model/rankingから勝敗を推定しない。


next6では8 model probesがLOSS（27,919,379 nodes）、remaining85が83 LOSS・2 UNKNOWN（401,091,716 nodes）。181-position adaptive s6 cohortは179 WIN・2 UNKNOWN、61,142,979 nodes。focused retriesは2件ともLOSS、4,832,571と6,689,407 nodesだった。29-source expanded auditは1,467 unique canonical s6 keys（1,346 WIN、115 LOSS、6 UNKNOWN-only、conflict 0）を検査し、602 safe parents中455 reply27-related、449既知LOSSと6 new LOSSを確認。hard-boundary auditは90・91-child両parentをgeometryから再生成し、focused LOSSを伝播した。これによりclass `(1297036967560609796, 0)` の全103 canonical s5 childrenがLOSSとなり、direct verifierはcoverage `{22,32,58,62}` を確認した。

当時のpost-next6 cacheは3,418 entries（WIN 65、LOSS 3,353、conflict 0）。s4 classはLOSS 23、WIN 131、UNKNOWN 3,230、secured 92/119、remaining 27。最小追加class coverとrational LP dualは8で一致した。8-class repair additive/unique UNKNOWN s5 workは744、exact-15 additiveは1,052・uniqueは1,048。これらは当時の作業量である。

当時の3,418-entry cache下の次候補は`(1301540292310335488, 0)`で、111子中16 LOSS・95 UNKNOWN、coverage vertices `{78,86,92,94}`。`post-next6-ranking.json`と`post-next6-best-class.csv`はscheduling用で、勝敗の根拠ではない。

next7の8 model probesがLOSS（37,732,931 nodes）、残り87もLOSS（396,976,088 nodes）。以前からの16 LOSSを合わせ、`next7-boundary-verification.log`は全111 canonical s5 childrenをLOSSと確認しcoverage `{78,86,92,94}` を記録した。統合cacheは3,513 entries（WIN 65、LOSS 3,448、conflict 0）。s4 classはLOSS 24、WIN 131、UNKNOWN 3,229、secured 96/119、remaining 23。最小追加class coverとrational LP dualは7で一致する。7-class repair additive/unique UNKNOWN s5 workは649、exact-15 additiveは1,131・uniqueは1,126。これらは作業量で、UNKNOWN classの証明ではない。次のheuristic対象`(1297599642636648448, 0)`は106子中既知LOSS 9、UNKNOWN 97、coverage `{59,61,89,97}`。rankingはtarget scheduling用で勝敗根拠ではない。

保存済みActions run `37401759541` からclass `(1297599642636648448, 0)` の97未確定s5子を回収した。raw replayは96 LOSS・1 UNKNOWN、385,400,242 nodes。別のsaved hard6 sourceは100-child s6 boundaryを98 WIN・2 LOSS・0 UNKNOWN、75,090,722 nodesで完了し、独立のLOSS witnessは7,364,518 nodes。geometry auditはhard6 parentを確認し、LOSS witnessから当該s5 parent LOSSを派生した。これで既知9 LOSSに96 replay LOSSと派生1 LOSSが加わり、direct verifierは全106 canonical children LOSS、coverage `{59,61,89,97}`、conflict 0を確認。保存cache checkpointは3,610 entries（WIN 65、LOSS 3,545）。その時点のs4 classはLOSS 25、WIN 131、UNKNOWN 3,228、secured 100/119、remaining 19、minimum additional coverとrational dualは6で一致した。これはsaved Actions checkpointであり、expanded reverse propagationの追加結果は別snapshotとして記録する。

Xserver exact replayはclass `(5908722711110107136, 0)` の100 canonical s5 childrenを全てLOSSと判定し、合計289,895,608 nodesを記録した。`next10-xserver-summary.json` はcoverage `{34,42,82}`、重複・conflictなしを報告する。これは保存済みexact結果とdirect geometry確認に基づく有限class結果であり、最終統合frontierはexpanded reverse propagationを含む後続snapshotで扱う。

next8のexpanded saved-s6 auditは3,610-entry Actions cacheから4つの新しいs5 LOSS parentを派生し、3,614-entry intermediate cacheを作った。next9 run `37403922028` の102 saved replay rowsは94 LOSS・3 WIN・5 UNKNOWN、567,396,507 nodes。source summaryは104-child boundaryを96 LOSS・3 WIN・5 UNKNOWNとし、classはWINと報告する。さらにrun `37404268447` の91-child hard-s6 boundaryは全てWIN（29,531,979 nodes）で、geometry receiptに従って1つのs5 parent WINを導いた。残る4 UNKNOWN childは解決していない。

next10 fold Actions checkpointは3,792 entries（WIN 69、LOSS 3,723、conflict 0）。当時s4 classはLOSS 26、WIN 137、UNKNOWN 3,221、secured 103/119、remaining 16、minimum additional coverとrational dualは5で一致した。next8から続くreverse auditを含む当時のexpanded cacheは3,796 entries（WIN 69、LOSS 3,727、conflict 0）。そのsnapshotのrepair additive/uniqueは473、exact-15 additive 1,301・unique 1,296。target `(10376293541461622792, 64)` は108子中既知LOSS 3・UNKNOWN 105、coverage `{70,72,77,87}`。これらは当時のsnapshot値である。

Actions repair5 batch run `37404904661` は473 raw replay rowsで、410 LOSS・19 WIN・44 UNKNOWN、合計3,136,880,721 nodesを返した。対象class `(1297036692816920608, 0)` の102 canonical childrenは全てLOSS、coverage `{5,55,57,63,65}`。別class `(1873497444986126592, 0)` は108子中106 LOSS・2 UNKNOWNだった。さらに3つの選択class `(1152921788208906240, 0)`、`(10376293541461622792, 64)`、`(10448351135499554816, 0)` はWINだが、そこに残る42 UNKNOWN childは探索しなかった。Actions mergeは4,221 entries（WIN 88、LOSS 4,133、conflict 0）。当時のexpanded cacheは4,225 entries（WIN 88、LOSS 4,137、conflict 0）。当時のcardinalityはLOSS 27、WIN 161、UNKNOWN 3,196、secured 106/119、remaining 13、minimum cover/rational dual 4。4-class repair additive/unique workは304、exact-15 additive 1,231・unique 1,221。当時のheuristic target `(1873497444986126592, 0)` は108子中106 LOSS・2 UNKNOWN、coverage `{49,88,98}`。これはfinite frontierであり、残るUNKNOWNの証明ではない。

次のadaptive 2M s6 cohortは195-child boundaryから193 replay rowsを新規実行し、137 WIN・56 UNKNOWN・0 LOSS、179,743,467 nodesを記録した。s5 parent `(1152921506758524928, 536871040)` は97子中83 WIN・14 UNKNOWN、parent `(1152921504612089856, 536871040)` は98子中56 WIN・42 UNKNOWNで、どちらもUNKNOWNのまま。LOSS replayがなく、両親の全子WINも揃わないため、このcohortはs5 exact cacheを増やさなかった。探索対象を閉じたとは主張しない。

勝敗規約は、位置の真偽値が「先手固定視点で最終的に先手が勝つ」であり、偶数石OR・奇数石ANDである（[K0002](K0002-grundy-and-first-move-conventions.md)、`cpp/solvers/kyouen_dfpn_root.cpp`）。従って、ある初手の後のs4 LOSSが全119の第三手選択をcoverすれば、各s3 odd AND位置はLOSSとなり、s2 `{60,27}` のOR位置もLOSSとなる。これは後手が中央初手60に27で応じることで中央初手を破る方向の証拠であり、中央初手60の勝ちを示すものではない。空盤の勝敗は他の初手も検査しないと決まらない。

この時点では空盤面勝敗と`{60,27}` outcomeは未確定で、終端までのAND/OR証明は未完了。別のcold residual mex cross-checkは6件中3件（120、158、192秒）で停止し、production結果には採用していない。6件完了とは主張しない。6つのevidence-recovery regression testsと33 knowledge testsは成功済み。

再現CLI、保存入力、raw shard、receiptへのリンクは[実験README](../../experiments/n11-boundary-recovery-20261006/README.md)を参照。


parent A/B focused audits closed two previously unresolved s5 parents. Parent A `(1152921506758524928, 536871040)` has 97 children; its final 33-source saved-s6 audit and focused replay establish LOSS. Parent B `(1152921504612089856, 536871040)` has 98 children; the 34-source audit contains 1,849 unique canonical s6 keys (1,678 WIN, 125 LOSS, 46 UNKNOWN-only, no conflicts), and focused replay plus saved-s6 propagation establishes LOSS. The direct verifier checks all 108 canonical children of `(1873497444986126592, 0)` as LOSS. These are finite exact-result and geometry-audit conclusions, not a proof of the empty-board outcome.

The 4,243-entry post-parent-B cache, 4,257-entry next12 cache, and 4,263-entry next13 cache are historical checkpoints. Next14 completed seven of eight scheduled probes (five LOSS, two WIN; 44,039,611 nodes); one scheduled probe was not dispatched, and the 43 remaining class children were not run. Independent audit verifies the saved results and full 57-child boundary, confirming class `(10376293541595840512, 64)` as WIN. No further work was run on that class.

The historical cache `post-next14-expanded-s5.cache` contained 4,270 entries (94 WIN, 4,176 LOSS), with zero conflicts. Its finite counts were 28 LOSS, 170 WIN, and 3,186 UNKNOWN; 109/119 vertices were secured, 10 remained, and minimum cover/rational dual was 4. Four-class repair was 379 additive/unique; exact-15 was 1,403 additive and 1,361 unique. The ranked class `(1297036692682702984, 0)` had 108 children, 4 known LOSS and 104 UNKNOWN, coverage `{33,43,77,87}`. These values are a historical checkpoint.

The historical cache `post-next13-expanded-s5.cache` contained 4,263 exact entries (92 WIN, 4,171 LOSS), with zero conflicts. Its finite class counts were 28 LOSS, 167 WIN, and 3,189 UNKNOWN; 109/119 root vertices were secured, 10 remained, and minimum cover equaled the rational dual at 4. Four-class repair work was 344 additive/unique UNKNOWN s5 entries; exact-15 was 1,361 additive and 1,319 unique. Its ranked target `(10376293541595840512, 64)` had 57 children, 6 known LOSS and 51 UNKNOWN, with coverage `{57,63,70,72}` and new vertices `{70,72}`. These finite results and target rankings are scheduling evidence, not terminal proofs. The empty-board and `{60,27}` outcomes remain UNKNOWN; terminal AND/OR proof is incomplete.

The historical expanded cache `post-next12-expanded-s5.cache` contained 4,257 entries (89 WIN, 4,168 LOSS), with zero conflicts. Its finite class counts were 28 LOSS, 163 WIN, and 3,193 UNKNOWN; 109/119 root vertices were secured, and minimum cover equaled the rational dual at 3. Three-class repair work was 308 additive/unique UNKNOWN s5 entries; exact-15 was 1,360 additive and 1,341 unique. Its ranked target `(1298162592589545600, 0)` had 108 children, 4 known LOSS and 104 UNKNOWN, with coverage `{70,72,77,87}`. These finite counts and ranked repair targets are scheduling results, not terminal proofs. Empty-board and `{60,27}` remain UNKNOWN; terminal AND/OR proof is incomplete.


Next15 hard3 audited the prior saved-s6 collection (zero overlap with the new boundary) and completed 162 new exact replays (157 WIN, 5 LOSS; 89,196,422 nodes). Of the three hard s5 parents, one had a complete 99-child s6 boundary with all 99 WIN, deriving one s5 WIN; the other two parents were LOSS. This single s5 WIN establishes the enclosing class `(1297036692682702984, 0)` as WIN. 134 previously unsearched s6 boundary positions remained unresolved at run end and were not dispatched after the class was resolved. The archived summary field `saved_unknown_boundary_count` is mislabeled: it counts unresolved positions, including keys absent from saved exact inputs. No saved UNKNOWN rows were eligible for retry, and new replay rows had zero overlap with prior exact source rows. The 36-source expanded audit derives 13 new s5 LOSS parents without propagating UNKNOWN.

The historical expanded cache `post-next15-expanded-s5.cache` contained 4,385 exact entries (95 WIN, 4,290 LOSS), zero conflicts; SHA-256 `8a199081c83868ef931f6ef2e9a8b3d02ce2988b86893984abc6d5d3843f4b59`. Its finite counts were 28 LOSS, 172 WIN, and 3,184 UNKNOWN classes; 109/119 vertices secured, 10 remained, and minimum cover/rational dual was 4. Four-class repair was 377 additive/unique; exact-15 was 1,399 additive and 1,358 unique. The ranked class `(1586392968741257216, 0)` had 98 children, 7 known LOSS and 91 UNKNOWN, coverage `{38,70,72}`. These are historical finite scheduling results.

Next16 began from that cache. Of eight supplied model8 targets, four were dispatched; three produced new exact rows (two WIN and one LOSS) and one was UNKNOWN, totaling 43,173,440 nodes. Four targets were not dispatched. A complete 98-child geometry audit established the enclosing class `(1586392968741257216, 0)` as WIN from the exact WIN witnesses. The supplied model targets had zero overlap with the prior exact cache. The independent run audit checks source hashes, geometry, and cache delta, while treating saved solver verdicts as inputs rather than re-proving them. The saved-s6 target audit before replay found all 91 targets UNKNOWN and produced an empty derived cache. No new s6 search was run for next16.

The historical expanded cache `post-next16-expanded-s5.cache` contained 4,388 exact entries (97 WIN, 4,291 LOSS), zero conflicts; SHA-256 `ddc997e18480ed9ceb669148dcc46166eae1bb6ae9ec08d07e4954d6aa91c081`. Its finite class counts were 28 LOSS, 175 WIN, and 3,181 UNKNOWN; 109/119 vertices secured, 10 remained, and minimum cover/rational dual was 4. Four-class repair was 385 additive/unique; exact-15 was 1,401 additive and 1,375 unique. The ranked class `(1298162592589545480, 0)` had 110 children, 8 known LOSS and 102 UNKNOWN, coverage `{33,43,70,72}`. These were historical scheduling results.

Next17 model8 returned eight exact s5 LOSS rows (54,975,108 nodes). Its completion93 run returned 89 LOSS and 4 UNKNOWN s5 rows (656,185,414 nodes). The hard5 adaptive s6 boundary contained 493 children: 3 previously saved WIN keys and 214 new exact replays (200 WIN, 14 LOSS; 190,725,964 nodes), with 276 unseen children not dispatched. No saved UNKNOWN child rows were eligible for retry. The five s5 parents were classified LOSS through exact child witnesses. The independent propagation audit checks source hashes, full geometry, and reverse propagation while treating solver values as inputs; the direct verifier confirms the full 110-child class is LOSS.

The current expanded cache is [post-next17-expanded-s5.cache](../../experiments/n11-boundary-recovery-20261006/output/post-next17-expanded-s5.cache): 4,515 entries (97 WIN, 4,418 LOSS), zero conflicts; SHA-256 `2fa27a15625af7449ca8f3fa21e683ba2e13a5d4deb99f8919d02ea61b59c82c`. Finite class counts are 29 LOSS, 175 WIN, and 3,180 UNKNOWN; 113/119 vertices are secured, 6 remain, and minimum cover/rational dual are both 3. Three-class repair is 283 additive/unique UNKNOWN s5 entries; exact-15 is 1,399 additive and 1,363 unique. The best ranked class `(1585267068834414720, 0)` has 104 children, 5 known LOSS and 99 UNKNOWN, coverage `{38,77,87}`. See the [receipt](../../experiments/n11-boundary-recovery-20261006/output/post-next17-expanded-receipt.json), [cardinality](../../experiments/n11-boundary-recovery-20261006/output/post-next17-expanded-cardinality.json), [repair](../../experiments/n11-boundary-recovery-20261006/output/post-next17-expanded-repair.json), [ranking](../../experiments/n11-boundary-recovery-20261006/output/post-next17-expanded-ranking.json), [target list](../../experiments/n11-boundary-recovery-20261006/output/post-next17-expanded-best-class.csv), and [independent finite audit](../../experiments/n11-boundary-recovery-20261006/output/post-next17-finite-independent-audit.json). UNKNOWN classes, empty-board outcome, and `{60,27}` remain unresolved.

Next18 preparation is complete for the ranked class `(1585267068834414720, 0)`. The target-specific audit against the 37-source saved-s6 collection found all 99 UNKNOWN parents with zero new exact derivations and zero conflicts. An archive-scope audit of 187 raw replay CSVs found no prior same-budget (>=15,000,000 nodes) UNKNOWN row among the 99 children, so every child is a fresh completion target. The supplied model8 schedule ranks eight of the 99 children by the frozen structural WIN model; the model orders exploration only and is never used as proof. The full 99-child target boundary and the eight probe targets are disjoint-complete: the probe eight plus the remaining 91 reproduce the full boundary. No solver execution for next18 had started when this checkpoint was committed.

## 2026-10-07 dual-tight 92 probe and exact WIN witness

The saved probe9 schedule was run after the prior exact-result, same-budget UNKNOWN, and saved-s6 intersection audits. All nine s5 positions returned exact LOSS (21,927,853 nodes). The remaining 83 were then run once at 15,000,000 nodes per target: 81 exact LOSS and two UNKNOWN (343,344,159 nodes), with no WIN. Those two UNKNOWN s5 parents had a complete generated s6 boundary of 80 and 82 children, 162 unique children total; all were previously unseen in the 38-source saved collection.

The focused s6 run returned 160 exact WIN rows (48,281,975 nodes). One s5 parent has all 80/80 canonical s6 children exact WIN, so that s5 is exact WIN. Its enclosing s4 class `(10452854735126921216, 0)` is therefore exact WIN, and class exploration stopped. The other s5 parent remains UNKNOWN with 80/82 s6 children exact WIN and two children not dispatched. No s6 LOSS was found and no reverse-propagated s5 LOSS came from this focused s6 run. The independent geometry audit checks the complete 95-child canonical s5 boundary: 93 exact LOSS, one exact WIN witness, one UNKNOWN; the class is WIN. This is an exact finite class conclusion, not a result for `{60,27}` or the empty board.

The merged exact s5 cache now has 4,606 entries (WIN 98, LOSS 4,508, conflict 0). The 3,384 s4 classes classify as 29 LOSS, 178 WIN, and 3,177 UNKNOWN. Secured third moves remain 113/119, leaving 6. The minimum additional class cover remains 3, matching rational LP dual value 3; the new additive-optimal three-class repair has 284 distinct UNKNOWN s5 children. Its selected dual-tight classes have 92, 93, and 99 UNKNOWN children. The next schedule is class `(10376293541461626880, 131072)`, with 103 canonical s5 children, 11 known LOSS, 92 UNKNOWN, covering dual-positive vertex 100. This ranking is only a work order. `{60,27}` and the 11×11 empty board remain UNKNOWN.

## 2026-10-07 18:31 JST dual-tight repair probe WIN

The next ranked class `(10376293541461626880, 131072)` was audited before dispatch. Its 92 UNKNOWN s5 targets had zero intersection with the 4,606-entry exact cache, zero reusable exact rows among 2,808 saved canonical s6 positions, and no matching replay rows or same-budget UNKNOWN results in 872 scanned CSV files. The saved-s6 boundary audit derived zero new s5 verdicts.

The eight lowest-legal-count targets were replayed once with a 15,000,000-node budget each. All eight completed exact: seven LOSS and one WIN, totaling 33,123,142 nodes. The exact WIN witness is s5 `(10376293541461626880, 131328)`. Geometry rebuilding confirms the complete 103-child canonical s5 boundary, its safe legal parent incidence, and 18 LOSS / 1 WIN / 84 UNKNOWN after merging. The class is therefore exact WIN; the other 84 class children were not explored. The same s5 witness is also a legal child of two other reply27 s4 classes that were UNKNOWN, so those two classes became WIN as well; a third reply27 parent class was already WIN.

The merged exact s5 cache is 4,614 entries (WIN 99, LOSS 4,515, conflict 0), SHA-256 `0570894f50e76d024ccdeb225db8653f80e2b2b1fb119a8449145db77e659f10`. The 3,384 s4 classes are 29 LOSS, 180 WIN, and 3,175 UNKNOWN. Secured third moves remain 113/119, leaving 6. Minimum additional class cover and rational LP dual are both 3. The additive-optimal three-class repair has 284 distinct UNKNOWN s5 targets. Reoptimization selects `(1297036692683751424, 16384)` as the next dual-tight class: 110 canonical children, 18 known LOSS, 92 UNKNOWN, coverage `{14,18,100,108}`. This is a schedule only.

The raw replays, zero-row saved-s6 delta, cache merge, complete class geometry audit, cardinality, repair, ranking, and source hashes are listed in [the probe8 artifact inventory](../../experiments/n11-boundary-recovery-20261006/output/post-next17-dual-tight-repair-10376293541461626880-131072-probe8-artifact-hashes.json). `{60,27}` and the 11×11 empty board remain UNKNOWN.


## 2026-10-07 22:18 JST dual-tight s6 boundary continuation

開始時の `main` / `origin/main` は `f8dc62e8c94c911e6f9696b3bf41c94004e6c2f5`。直前のclass `(10448351169859289088,0)` は96 canonical s5 childで、exact LOSS 94・UNKNOWN 2。残ったs5 parent `(10448351169859289088,4)` と `(10448351135499551232,32768)` の完全canonical s6境界をgeometryから再生成した。保存済みexact s6とのintersectionは0で、同budget UNKNOWNの再実行はしていない。

adaptive exact s6 replayは165件をdispatchし、163 WIN・2 UNKNOWN、0 LOSS、計51,759,637 nodes。parent `(10448351169859289088,4)` は完全85-child s6境界がすべてexact WINとなり、s5 WINを導出した。もう一方は79 exact WIN・2 exact UNKNOWN・7未dispatchでs5 UNKNOWNのまま。s4 classがWINになった後の未実行childは停止した。raw、exact s6 cache、497 run filesのhash manifestを保存した。

全safe canonical s5 parentへのreverse-incidence監査は10 sourceで349 canonical s6 key（341 WIN・6 LOSS・2 UNKNOWN）。reply27関連parent26件は既知LOSSとの重複のみで、新規LOSSは0、conflict 0。UNKNOWNを伝播していない。exact s5 cacheは4,715件（WIN102・LOSS4,613・conflict0）。完全96-child s4 boundaryは94 LOSS・1 WIN・1 UNKNOWN。WIN witnessのreverse incidenceにより、reply27 reachableな3 classがUNKNOWNからWINへ変わったことも監査した。

再計算frontierは29 LOSS・187 WIN・3,168 UNKNOWN、secured 113/119、remaining 6、minimum additional classes 3 = rational LP dual 3、dual-tight true。repairは3 class・284 distinct UNKNOWN s5。rank1は `(10448491872987906048,0)`、99 canonical child中LOSS 7・UNKNOWN 92、coverage `{81,83,104}`、dual vertex 104。これは探索順序のみ。`{60,27}` と11×11 empty boardはUNKNOWN。

SHA-256 inventory: [s6 descent artifact hashes](../../experiments/n11-boundary-recovery-20261006/output/post-f8dc62e-dual-tight-1297036692683751424-16384-probe8-nextclass-next-probe8-second-next-s6-unknown2-artifact-hashes.json)。

## 2026-10-08 01:10 JST rank-1 pre-dispatch audit

On the available local snapshot at `f8dc62e8c94c911e6f9696b3bf41c94004e6c2f5`, audited the next ranked class `(10448491872987906048,0)`: 99 canonical s5 children, 7 known LOSS, and 92 UNKNOWN. The target-specific raw-history scan covered 1,470 CSV files. It found no cache hits, prior exact replay rows, same-or-higher-budget UNKNOWN rows, or verdict conflicts, leaving 92 locally dispatch-ready targets.

Audited all canonical s6 children against the 37-source saved corpus and the supplemental 10-source reverse audit. The supplemental set overlaps 9 source files with the 37-source set and contributes one additional source, with no path/hash mismatch. Both audits leave all 92 s5 parents UNKNOWN, derive no exact s5 row, and report zero cache conflicts. The combined 38-source union therefore provides no reusable s6 verdict for these parents. This is a coverage audit of saved evidence; it does not change the local exact cache or s4 frontier.

The target-specific hash inventory is `post-f8dc62e-rank1-10448491872987906048-0-audit-artifact-hashes-20261008.json` (SHA-256 `34c11879c19a839d30a06a06a31ac7990dab24c7b15666b6c46a538ab8e9943c`). The remote `main` could not be verified because DNS resolution for `github.com` failed, so no solver target was dispatched and no commit/push was made. The rank and dispatch-ready count are scheduling information, not a verdict. `{60,27}` and the empty board remain UNKNOWN.

## 2026-10-08 02:25 JST exact-result reconciliation and checkpoint

Fetched origin/main successfully. HEAD, origin/main, and FETCH_HEAD agree at dd9db22af87dbcf65ced44631544e5596c4227e8; there were no newer commits to integrate. The incoming main schedule post-next17-dual-tight-repair-1297036692683751424-16384-probe8.csv has the same eight canonical s5 keys in the same order as the already completed local input. Those exact results were reused; no replay was repeated.

The completed class (1297036692683751424,16384) produced four exact s5 LOSS rows and one exact s5 WIN row in the scheduled probe, totaling 21,033,044 exact nodes. One other row completed UNKNOWN, one run was interrupted, and one target was not dispatched. Complete geometry rebuilding verified all 110 canonical children. After merge the class has 22 LOSS, one WIN, and 87 UNKNOWN children, so it is exact WIN and its remaining targets were stopped.

The completed class (10448351685255364608,0) produced four exact s5 LOSS rows and one exact s5 WIN row, totaling 21,317,933 exact nodes. Two runs were interrupted and one target was not dispatched. Its complete 98-child geometry audit confirms the exact WIN witness; the merged class has nine LOSS, one WIN, and 88 UNKNOWN children, so exploration stopped.

For class (10448351169859289088,0), the two saved probe batches supplied 16 exact LOSS rows. The residual 76-target completion produced 74 exact LOSS and two UNKNOWN rows. The two UNKNOWN s5 parents were descended through their full canonical s6 boundaries: 165 exact s6 rows yielded 163 WIN, two UNKNOWN, and zero LOSS (51,759,637 nodes). One s5 parent has all 85/85 canonical s6 children exact WIN and is therefore exact WIN. The other remains UNKNOWN with 79 exact WIN s6 children, two UNKNOWN, and seven unstarted children; class exploration stopped after the first WIN witness. The full 96-child s4 geometry audit reports 94 LOSS, one WIN, one UNKNOWN. No s6 LOSS was found, so reverse-propagated s5 LOSS is zero.

Across the three classes, 100 direct exact s5 rows were added (98 LOSS, two WIN), plus one s5 WIN derived from the complete 85-child s6 boundary. The final cache contains 4,715 unique rows (WIN 102, LOSS 4,613, conflict 0). The three new witnesses also update collateral s4 classes; recomputation over all 3,384 classes gives LOSS 29, WIN 187, UNKNOWN 3,168. Secured third moves are 113/119, with six remaining. The integer repair minimum and rational LP dual are both three, with 284 distinct UNKNOWN s5 children in the reoptimized repair.

The current rank-1 target remains (10448491872987906048,0): 99 canonical children, seven known LOSS, and 92 UNKNOWN. Its 1,470-CSV raw-history audit found no prior exact row, same-or-higher-budget UNKNOWN, or conflict; the 38-source saved-s6 audit found no reusable exact verdict and derived no s5 result. The 92 remain UNKNOWN and are eligible for a fresh probe after this checkpoint is pushed. The valid 673-file artifact inventory is post-f8dc62e-dual-tight-reconciled-checkpoint-artifact-hashes-20261008.json, working-tree SHA-256 1a7d6dfda6562b535a711f8dcef798edd7b1bd6d67b477a8269e322d9899942b; Git blob SHA-256 22afe44dabc248e53d3a780103285890194e0afeaae12c1085e488abfa83018f. {60,27} remains UNKNOWN; the 11x11 empty board remains UNKNOWN.
