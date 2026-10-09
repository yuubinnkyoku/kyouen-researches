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
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-rank1-10448491872987906048-0-probe8-geometry-audit.json
    role: verifier
    note: 99-child complete boundary; exact WIN witness and legal parent incidence for class (10448491872987906048, 0)
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-next-dual-tight-10448351136036421632-0-completion84-geometry-audit.json
    role: verifier
    note: 98-child complete boundary; exact WIN witness and collateral reply27 parent status audit
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-next-dual-tight-10448351136036421632-0-completion84-merged-s5.cache
    role: data
    note: updated canonical exact s5 cache with 4,762 entries and zero conflicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-next-dual-tight-10448351136036421632-0-completion84-merge-receipt.json
    role: manifest
    note: probe8 plus early-stopped completion84 exact replay merge receipt
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-next-dual-tight-10448351136036421632-0-completion84-summary.json
    role: source
    note: 33 exact LOSS, one exact WIN, one UNKNOWN, and 49 not-dispatched completion targets
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-next-dual-tight-10448351136036421632-0-completion84-raw-all.csv
    role: source
    note: all started completion84 s5 replay rows, including the budget-limited UNKNOWN
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-next-dual-tight-10448351136036421632-0-completion84-cardinality.json
    role: data
    note: complete 3,384-class status, secured vertices, integer cover, and rational dual at 4,762 cache entries
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-next-dual-tight-10448351136036421632-0-completion84-repair.json
    role: data
    note: reoptimized 3-class additive repair with 283 distinct UNKNOWN s5 children
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-after-completion84-next-dual-tight-ranking.json
    role: data
    note: current rank-1 scheduling target after exact WIN witnesses removed two repair candidates
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-next-after-completion84-10448351135499550752-0-raw-history-audit.json
    role: manifest
    note: 91-target history audit; no exact replay, same-budget UNKNOWN, or cache hit
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-next-after-completion84-10448351135499550752-0-saved-s6-37source-summary.json
    role: manifest
    note: 37-source saved-s6 target audit; all 91 parents remain UNKNOWN
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-next-after-completion84-10448351135499550752-0-saved-s6-10source-summary.json
    role: manifest
    note: supplemental 10-source saved-s6 target audit; zero new exact s5 results
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-next-after-completion84-10448351135499550752-0-probe8-manifest.json
    role: manifest
    note: audited low-legal-count probe8 schedule for the next dual-tight class; not yet dispatched
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-dual-tight-proof-checkpoint-artifact-hashes-20261008.json
    role: manifest
    note: SHA-256 inventory of 77 new raw, exact, cache, geometry, and frontier artifacts
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-raw-all.csv
    role: source
    note: Eight scheduled probe outcomes with exact LOSS/WIN and UNKNOWN retained
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-raw-exact.csv
    role: source
    note: Seven exact solver replay rows used as verdict evidence
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-exact-targets.csv
    role: source
    note: Exact subset bound to the geometry audit; UNKNOWN excluded
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-new-exact-s5.cache
    role: data
    note: Seven direct exact s5 verdicts from probe8
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-summary.json
    role: data
    note: One WIN, six LOSS, one UNKNOWN; 58,511,040 nodes including the UNKNOWN budget
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-run-manifest.json
    role: manifest
    note: Solver, runner, schedule, raw outputs, and per-target hashes
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-merged-s5.cache
    role: data
    note: Updated exact s5 cache with 4,769 rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-merge-receipt.json
    role: manifest
    note: Merge receipt reports 106 WIN, 4,663 LOSS, and zero conflicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-geometry-audit.json
    role: verifier
    note: Full 102-child boundary and exact WIN witness geometry audit
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-geometry-input-summary.json
    role: data
    note: Exact-only probe subset and raw/cache hashes for the geometry verifier
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-geometry-input-sources.json
    role: manifest
    note: Inputs and source hashes bound to the exact replay subset
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-cardinality.json
    role: data
    note: Recomputed all-class status, minimum cover, and rational LP dual
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-repair.json
    role: data
    note: Reoptimized three-class repair and distinct UNKNOWN s5 union
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-10448351135499550752-0-probe8-repair-targets.csv
    role: data
    note: Current cache-aware repair target materialization
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-dual-tight-ranking.json
    role: data
    note: Re-ranked dual-tight repair candidates after the verified WIN
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-dual-tight-targets.csv
    role: data
    note: Updated UNKNOWN target boundary for the next rank-1 repair class
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-dual-tight-sources.json
    role: manifest
    note: Source hashes for current dual-tight rank and target list
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-b20949a5-next-after-completion84-probe8-artifact-hashes-20261008.json
    role: manifest
    note: SHA-256 inventory for outputs, inputs, and preserved .local raw solver files
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-raw-history-audit.json
    role: manifest
    note: 91-target audit across 1,719 CSVs with zero cache/exact/same-budget UNKNOWN hits
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-saved-s6-38source-summary.json
    role: manifest
    note: 38-source saved-s6 audit leaves all 91 parents UNKNOWN and derives no exact s5
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-saved-s6-38source-derived-s5.cache
    role: data
    note: Empty exact s5 delta from the saved-s6 audit
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-saved-s6-38source-full.json.gz
    role: source
    note: Complete saved-s6 boundary detail for all 91 current candidate parents
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8.csv
    role: source
    note: Audited eight-position low-legal-count schedule; order is not verdict evidence
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-manifest.json
    role: manifest
    note: Probe schedule, solver/source, and input hashes; 5 dispatched after early WIN
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-raw-all.csv
    role: source
    note: Five exact results and three not-dispatched scheduled rows retained
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-raw-exact.csv
    role: source
    note: Five direct exact s5 replay rows
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-exact-targets.csv
    role: source
    note: Exact probe subset bound to the full-boundary geometry verifier
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-new-exact-s5.cache
    role: data
    note: Two exact WIN and three exact LOSS results from this probe
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-summary.json
    role: data
    note: 5 exact rows, 27,772,825 nodes, with no UNKNOWN result
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-run-manifest.json
    role: manifest
    note: Per-target inputs, exact rows, raw solver outputs, and hash receipts
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-merged-s5.cache
    role: data
    note: Merged exact s5 cache with 4,774 entries
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-merge-receipt.json
    role: manifest
    note: Exact cache merge receipt with zero verdict conflicts
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-geometry-audit.json
    role: verifier
    note: Complete 99-child s4 boundary and both WIN witness geometry audits
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-geometry-input-summary.json
    role: data
    note: Exact-only probe subset and raw/cache hashes supplied to the verifier
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-geometry-input-sources.json
    role: manifest
    note: Geometry verifier inputs and hashes, including both pre-dispatch audits
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-cardinality.json
    role: data
    note: Updated all-class status, 119-vertex cover minimum, and rational LP dual
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-repair.json
    role: data
    note: Reoptimized three-class repair after the two exact WIN witnesses
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-rank1-10448386319871639552-0-probe8-repair-targets.csv
    role: data
    note: Current cache-aware repair target materialization
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-after-probe8-dual-tight-ranking.json
    role: data
    note: Re-ranked dual-tight repair classes after the verified WIN
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-after-probe8-dual-tight-targets.csv
    role: data
    note: UNKNOWN s5 boundary for the next current rank-1 class
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-after-probe8-dual-tight-sources.json
    role: manifest
    note: Source hashes for the current ranking and selected repair target
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-046db787-dual-tight-probe8-artifact-hashes-20261008.json
    role: manifest
    note: SHA-256 inventory for outputs, inputs, and ignored .local raw solver files
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-after-probe8-dual-tight-ranking.json
    role: data
    note: "Saved checkpoint artifact; see the matching run and audit manifest"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-after-probe8-dual-tight-sources.json
    role: data
    note: "Saved checkpoint artifact; see the matching run and audit manifest"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-after-probe8-dual-tight-targets.csv
    role: data
    note: "Saved checkpoint artifact; see the matching run and audit manifest"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-cardinality.json
    role: data
    note: "All-class status, six uncovered vertices, integer cover minimum, and rational dual"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-exact-targets.csv
    role: source
    note: "Exact-completed subset supplied to the full-boundary geometry verifier"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-geometry-audit.json
    role: verifier
    note: "Complete 100-child s4 boundary and four legal WIN witness checks"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-geometry-input-sources.json
    role: manifest
    note: "Geometry verifier source hashes, including target audits and local raw outputs"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-geometry-input-summary.json
    role: data
    note: "Exact-only inputs and hashes supplied to the complete boundary verifier"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-manifest.json
    role: manifest
    note: "Source-bound schedule; two same-budget UNKNOWN keys excluded"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-merge-receipt.json
    role: manifest
    note: "Cache merge receipt with zero verdict conflicts"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-merged-s5.cache
    role: data
    note: "Merged exact s5 cache with 4,780 entries"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-new-exact-s5.cache
    role: data
    note: "Four exact WIN and two exact LOSS rows from this probe"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-raw-all.csv
    role: source
    note: "Completed exact outputs from the probe; two scheduled keys were not dispatched"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-raw-exact.csv
    role: source
    note: "Six exact solver replay rows"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-repair-targets.csv
    role: data
    note: "Distinct UNKNOWN s5 positions in the reoptimized repair union"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-repair.json
    role: data
    note: "Reoptimized three-class repair with 284 distinct UNKNOWN s5 positions"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-run-manifest.json
    role: manifest
    note: "Per-target raw output/input hashes, exact rows, and undispatched status"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8-summary.json
    role: data
    note: "Probe run summary with four WIN, two LOSS, and 47,436,351 nodes"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-probe8.csv
    role: source
    note: "Eight low-legal-count targets; probe order is scheduling metadata only"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-raw-history-audit.json
    role: manifest
    note: "1,735-CSV audit; two distinct same-budget UNKNOWN keys excluded from 89 ready children"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-saved-s6-38source-derived-s5.cache
    role: data
    note: "No exact s5 delta was derived from saved s6 results"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-saved-s6-38source-full.json.gz
    role: source
    note: "Full saved-s6 parent-child intersection details"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-rank1-10448351135499550784-0-saved-s6-38source-summary.json
    role: manifest
    note: "All 91 s5 parents remain UNKNOWN after the 38-source saved-s6 intersection"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-7e1caa96-dual-tight-probe8-artifact-hashes-20261008.json
    role: manifest
    note: "SHA-256 inventory for outputs, solver/source inputs, and preserved .local run evidence"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-after-probe8-dual-tight-ranking.json
    role: data
    note: "Reoptimized dual-tight repair ranking after this exact WIN"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-after-probe8-dual-tight-sources.json
    role: manifest
    note: "Source hashes for the updated ranking and UNKNOWN s5 target list"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-after-probe8-dual-tight-targets.csv
    role: data
    note: "UNKNOWN s5 boundary for the next ranked dual-tight class"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-cardinality.json
    role: data
    note: "All-class status, 119-vertex cover minimum, and rational LP dual"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-exact-targets.csv
    role: source
    note: "Exact-completed subset supplied to the complete geometry verifier"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-geometry-audit.json
    role: verifier
    note: "Complete 101-child boundary and two legal WIN witness checks"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-geometry-input-sources.json
    role: manifest
    note: "Geometry verifier source hashes, including all raw run files"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-geometry-input-summary.json
    role: data
    note: "Exact-only inputs and hashes supplied to the full-boundary verifier"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-manifest.json
    role: manifest
    note: "Source-bound schedule with same-budget UNKNOWN excluded"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-merge-receipt.json
    role: manifest
    note: "Exact cache merge receipt with zero verdict conflicts"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-merged-s5.cache
    role: data
    note: "Merged exact s5 cache with 4,786 entries"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-new-exact-s5.cache
    role: data
    note: "Two exact WIN and four exact LOSS results"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-raw-all.csv
    role: source
    note: "Completed exact outputs; two scheduled keys were not dispatched"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-raw-exact.csv
    role: source
    note: "Six exact solver replay rows"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-repair-targets.csv
    role: data
    note: "Distinct UNKNOWN s5 positions in the reoptimized repair union"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-repair.json
    role: data
    note: "Reoptimized three-class repair with 286 distinct UNKNOWN s5 positions"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-run-manifest.json
    role: manifest
    note: "Per-target inputs, outputs, hashes, and undispatched status"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8-summary.json
    role: data
    note: "Probe summary with two WIN, four LOSS, 35,250,655 nodes"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-probe8.csv
    role: source
    note: "Eight low-legal-count targets; order is scheduling metadata only"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-raw-history-audit.json
    role: manifest
    note: "1,753-CSV audit; one same-budget UNKNOWN key excluded from 91 ready children"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-saved-s6-38source-derived-s5.cache
    role: data
    note: "No exact s5 delta was derived from saved s6 results"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-saved-s6-38source-full.json.gz
    role: source
    note: "Full saved-s6 parent-child intersection details"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-rank1-10448351135499550976-0-saved-s6-38source-summary.json
    role: manifest
    note: "The 38-source saved-s6 intersection derives no exact s5 verdict for 92 parents"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-f390d290-dual-tight-probe8-artifact-hashes-20261008.json
    role: manifest
    note: "SHA-256 inventory for outputs, source inputs, and preserved .local run evidence"
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-after-probe8-dual-tight-ranking.json
    role: data
    note: "Reoptimized dual-tight repair ranking after this exact s5 WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-after-probe8-dual-tight-sources.json
    role: manifest
    note: "Source hashes for the current dual-tight ranking and UNKNOWN boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-after-probe8-dual-tight-targets.csv
    role: data
    note: "UNKNOWN s5 boundary for the next ranked dual-tight class."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-cardinality.json
    role: data
    note: "All-class statuses, 119-vertex cover minimum, and rational LP dual after merge."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-dual-tight-repair-input.json
    role: data
    note: "Schema adapter that preserves the selected additive repair rows verbatim."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-exact-targets.csv
    role: source
    note: "Seven exact completed s5 rows supplied to the geometry verifier; UNKNOWN omitted."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-geometry-audit.json
    role: verifier
    note: "Complete 100-child boundary and the safe canonical legal WIN witness."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-geometry-input-sources.json
    role: manifest
    note: "Hashed geometry, cache, audit, solver, and preserved raw inputs."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-geometry-input-summary.json
    role: data
    note: "Exact-only counts and hashes normalized from the completion-run collector."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-manifest.json
    role: manifest
    note: "Source-bound schedule for eight probes selected from 93 ready children."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-merge-receipt.json
    role: manifest
    note: "Exact cache merge receipt; opposite verdict conflicts are zero."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-merged-s5.cache
    role: data
    note: "Merged exact s5 cache with 4,793 entries."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-new-exact-s5.cache
    role: data
    note: "Seven new exact s5 rows: six LOSS and one WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-raw-all.csv
    role: source
    note: "All eight solver outcomes, including the one UNKNOWN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-raw-exact.csv
    role: source
    note: "Seven exact solver replay rows."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-repair-targets.csv
    role: data
    note: "Distinct UNKNOWN s5 positions in the reoptimized repair union."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-repair.json
    role: data
    note: "Reoptimized three-class repair after the exact WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-run-manifest.json
    role: manifest
    note: "Per-target solver inputs, outputs, hashes, and statuses."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8-summary.json
    role: data
    note: "Probe summary with six LOSS, one WIN, one UNKNOWN, and node counts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-probe8.csv
    role: source
    note: "Eight scheduled probes; order is scheduling metadata only."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-raw-history-audit.json
    role: manifest
    note: "1,771-CSV audit; 93 ready, with no prior exact or same-budget UNKNOWN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-saved-s6-derived-s5.cache
    role: data
    note: "No exact s5 verdict was derived from saved s6 results."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-saved-s6-full.json.gz
    role: source
    note: "Full saved-s6 parent-child intersection details."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-rank1-10412322338480590848-0-saved-s6-summary.json
    role: manifest
    note: "Saved-s6 audit leaves all 93 target parents UNKNOWN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-3bafea55-dual-tight-probe8-artifact-hashes-20261008.json
    role: manifest
    note: "SHA-256 inventory for current outputs, sources, and preserved .local raw evidence."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-after-probe8-dual-tight-ranking.json
    role: data
    note: "Reoptimized dual-tight repair ranking after this exact s5 WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-after-probe8-dual-tight-sources.json
    role: manifest
    note: "Source hashes for the updated ranking and UNKNOWN s5 boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-after-probe8-dual-tight-targets.csv
    role: data
    note: "UNKNOWN s5 boundary for the next ranked dual-tight class."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-cardinality.json
    role: data
    note: "All 3,384 class statuses, 119-vertex cover minimum, and rational LP dual."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-dual-tight-repair-input.json
    role: data
    note: "Schema adapter preserving selected additive repair rows verbatim."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-exact-targets.csv
    role: source
    note: "Eight exact completed s5 targets supplied to the geometry verifier."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-geometry-audit.json
    role: verifier
    note: "Complete 105-child boundary and one safe canonical legal WIN witness."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-geometry-input-sources.json
    role: manifest
    note: "Hashed geometry, cache, audit, solver, and preserved raw inputs."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-geometry-input-summary.json
    role: data
    note: "Exact-only counts and hashes normalized from the completion-run collector."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-manifest.json
    role: manifest
    note: "Source-bound schedule for eight probes selected from 92 ready children."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-merge-receipt.json
    role: manifest
    note: "Exact cache merge receipt with zero verdict conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-merged-s5.cache
    role: data
    note: "Merged exact s5 cache with 4,801 entries."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-new-exact-s5.cache
    role: data
    note: "Eight exact new s5 rows: seven LOSS and one WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-raw-all.csv
    role: source
    note: "All eight exact solver replay rows."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-raw-exact.csv
    role: source
    note: "Eight exact solver replay rows."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-repair-targets.csv
    role: data
    note: "Distinct UNKNOWN s5 positions in the recomputed repair union."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-repair.json
    role: data
    note: "Reoptimized three-class repair after the exact WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-run-manifest.json
    role: manifest
    note: "Per-target solver inputs, outputs, hashes, and statuses."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8-summary.json
    role: data
    note: "Probe summary with seven LOSS, one WIN, zero UNKNOWN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-probe8.csv
    role: source
    note: "Eight scheduled probes; order is scheduling metadata only."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-raw-history-audit.json
    role: manifest
    note: "1,793-CSV audit; all 92 children ready, no prior exact or same-budget UNKNOWN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-saved-s6-derived-s5.cache
    role: data
    note: "No exact s5 verdict was derived from saved s6 results."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-saved-s6-full.json.gz
    role: source
    note: "Full saved-s6 parent-child intersection details."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-rank1-1297036692816920704-0-saved-s6-summary.json
    role: manifest
    note: "Saved-s6 audit leaves all 92 target parents UNKNOWN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-fc77fecf-dual-tight-probe8-artifact-hashes-20261008.json
    role: manifest
    note: "SHA-256 inventory for current outputs, sources, and preserved .local raw evidence."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-bdbdea7c-rank1-10412322338480586760-0-final-merged-s5.cache
    role: data
    note: "Exact s5 cache after the 2026-10-08 probe and complete s6 WIN boundary; 4,809 entries, conflict 0."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-bdbdea7c-rank1-10412322338480586760-0-s4-win-geometry-audit.json
    role: manifest
    note: "Full geometry verification of the 100-child class WIN boundary and the complete 83-child s6 WIN witness."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-bdbdea7c-rank1-10412322338480586760-0-cardinality.json
    role: data
    note: "Recomputed 3,384-class status, 113 secured vertices, three-class integer cover, and matching rational dual."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-bdbdea7c-rank1-10412322338480586760-0-repair.json
    role: data
    note: "Reoptimized three-class repair with 288 distinct UNKNOWN s5 positions."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-bdbdea7c-rank1-10412322338480586760-0-dual-tight-ranking.json
    role: manifest
    note: "Ranked next target from the updated exact cache; scheduling order only."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d9583782-rank1-10448355533546061824-0-raw-history-audit.json
    role: manifest
    note: "Audit of 2,090 replay CSVs; 94 UNKNOWN s5 targets, zero prior exact, two same-budget UNKNOWN excluded, 93 dispatch-ready."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d9583782-rank1-10448355533546061824-0-augmented-s6-source-audit.json
    role: manifest
    note: "Hash-validated union of the 38-source saved s6 corpus and the 83-child exact WIN boundary, with zero conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d9583782-rank1-10448355533546061824-0-saved-s6-summary.json
    role: manifest
    note: "Regenerated all 94 target s6 boundaries against the augmented saved corpus; all remain UNKNOWN, with no derivations or conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d9583782-rank1-10448355533546061824-0-probe8.csv
    role: source
    note: "Eight low-legal-count targets selected from the 93 audited dispatch-ready s5 positions; schedule only, not yet dispatched."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d9583782-rank1-10448355533546061824-0-probe8-manifest.json
    role: manifest
    note: "Hashes and dispatch settings for the audited eight-position probe."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d9583782-rank1-10448355533546061824-0-augment-s6-audit.py
    role: verifier
    note: "Builds an augmented hash-attested s6 source audit from the saved corpus and verified exact-WIN boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d9583782-build-reply27-artifact-inventory.py
    role: verifier
    note: "Verifies and inventories the checkpoint artifacts and all source paths recorded by their manifests."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d9583782-reply27-checkpoint-artifact-hashes-20261008.json
    role: manifest
    note: "SHA-256 inventory for the exact class result, audits, prepared probe, and source files."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448355533546061824-0-probe8-raw-all.csv
    role: source
    note: "All eight completed raw replay rows, including the UNKNOWN row."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448355533546061824-0-probe8-summary.json
    role: data
    note: "Exact verdict counts, nodes, and UNKNOWN-row accounting."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448355533546061824-0-probe8-sources.json
    role: manifest
    note: "Hash-bound solver, per-target raw/input/log, cache, and output provenance."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448355533546061824-0-probe8-merge-receipt.json
    role: manifest
    note: "Exact cache merge counts and hashes; zero conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448355533546061824-0-probe8-new-exact-s5.cache
    role: data
    note: "Seven newly collected exact s5 outcomes; UNKNOWN excluded."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448355533546061824-0-probe8-merged-s5.cache
    role: data
    note: "Merged exact s5 cache with 4,816 entries and zero conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448355533546061824-0-s4-win-geometry-audit.json
    role: verifier
    note: "Full canonical boundary and exact-WIN witness legality audit."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448355533546061824-0-cardinality.json
    role: data
    note: "All-class status, secured vertices, minimum cover, and rational dual."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448355533546061824-0-repair.json
    role: data
    note: "Reoptimized three-class repair and UNKNOWN s5 union."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448355533546061824-0-dual-tight-ranking.json
    role: manifest
    note: "Reoptimized next-target ranking; scheduling order only."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-reply27-optimization-environment.json
    role: manifest
    note: "Python, NumPy, and SciPy versions used for finite cover and ranking calculations."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448351135500075008-0-raw-history-audit.json
    role: manifest
    note: "2,120-CSV audit; one same-budget UNKNOWN key excluded; 93 ready."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448351135500075008-0-saved-s6-summary.json
    role: manifest
    note: "All 94 parents remain UNKNOWN after saved-s6 intersection; no derived results/conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448351135500075008-0-probe8.csv
    role: source
    note: "Eight audited next-target positions, scheduling input only."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448351135500075008-0-probe8-manifest.json
    role: manifest
    note: "Hash-bound schedule excludes the same-budget UNKNOWN key."
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_probe_preflight.py
    role: verifier
    note: "Runs main's fail-closed audit binding against the exact scheduled target file."
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/audit_probe_preflight.py
    role: verifier
    note: "Main's fail-closed binding requires the raw-history and saved-s6 audits to cover identical keys/cache/target hashes."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448351135500075008-0-probe8-raw-history-audit.json
    role: manifest
    note: "Probe-specific 2,121-CSV audit: all eight scheduled keys have no prior exact or same-budget UNKNOWN rows."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448351135500075008-0-probe8-saved-s6-summary.json
    role: manifest
    note: "Probe-specific saved-s6 intersection: all eight parents remain UNKNOWN; no derived result or conflict."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448351135500075008-0-probe8-saved-s6-derived-s5.cache
    role: data
    note: "Zero-row s5 delta for the exact eight-key probe boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448351135500075008-0-probe8-saved-s6-full.json.gz
    role: source
    note: "Compressed full boundary details for the eight exact probe parents."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-rank1-10448351135500075008-0-probe8-preflight.json
    role: manifest
    note: "Passes main's fail-closed probe binding: eight ready targets, eight saved-s6 UNKNOWN parents, zero conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d538a68-reply27-checkpoint-artifact-hashes-20261008.json
    role: manifest
    note: "SHA-256 inventory for the exact result, audits, status, repair, and next-target schedule."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-probe8-raw-all.csv
    role: source
    note: "All eight scheduled replay rows; each is exact LOSS."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-probe8-raw-exact.csv
    role: source
    note: "Exact solver replay rows for the eight scheduled s5 children."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-probe8-new-exact-s5.cache
    role: data
    note: "Eight new exact s5 LOSS rows; no UNKNOWN values are cached."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-probe8-merged-s5.cache
    role: data
    note: "Merged canonical exact cache with 4,824 entries: 118 WIN and 4,706 LOSS."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-probe8-summary.json
    role: manifest
    note: "Eight exact LOSS rows, 40,659,042 exact nodes, and class remains UNKNOWN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-probe8-runner-summary.json
    role: manifest
    note: "Runner records all eight scheduled rows completed with no UNKNOWN or undispatched target."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-probe8-merge-receipt.json
    role: manifest
    note: "Base plus exact delta merge; zero duplicate verdicts and zero conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-probe8-sources.json
    role: manifest
    note: "Hash-bound solver, source, runner, inputs, per-target raw files, and merge outputs."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-class-boundary-audit.json
    role: manifest
    note: "Geometry reconstructs all 103 canonical s5 children: 17 exact LOSS and 86 UNKNOWN."
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py
    role: verifier
    note: "Rebuilds a complete canonical s5 boundary and propagates only exact cached verdicts."
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/collect_dual_tight_completed_probe.py
    role: source
    note: "Original collector retained unchanged to preserve hashes in previously committed source manifests."
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/collect_dual_tight_completed_probe_v2.py
    role: verifier
    note: "Corrects subset-only all-LOSS collection and records the actual dispatch main commit."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-reply27-cardinality.json
    role: manifest
    note: "Recomputed all 3,384 classes and exact integer-cover/rational-dual minima."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-repair.json
    role: manifest
    note: "Reoptimized three-class repair with 280 distinct UNKNOWN s5 children."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-repair-targets.csv
    role: source
    note: "Cache-aware distinct UNKNOWN s5 repair union, scheduling input only."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-dual-tight-ranking.json
    role: manifest
    note: "Re-ranked dual-tight repair; rank 1 remains class (10448351135500075008,0)."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-dual-tight-ranking-sources.json
    role: manifest
    note: "Hashes for current exact cache, repair, cardinality, and ranking geometry sources."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-dual-tight-targets.csv
    role: source
    note: "The current rank-1 class's 86 unresolved canonical s5 children."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-dual-tight-targets-raw-history-audit.json
    role: manifest
    note: "2,150-CSV audit: one distinct same-budget UNKNOWN key is excluded; 85 targets are dispatch-ready."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-dual-tight-targets-saved-s6-summary.json
    role: manifest
    note: "All 86 current s5 parents remain UNKNOWN against the hash-validated 39-source saved-s6 corpus."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-dual-tight-targets-saved-s6-derived-s5.cache
    role: data
    note: "No s5 verdicts derived from the saved-s6 intersection."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-dual-tight-targets-saved-s6-full.json.gz
    role: source
    note: "Compressed complete s6 boundary audit details for all 86 unresolved s5 parents."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-probe8-next.csv
    role: source
    note: "Eight low-legal-count positions selected from the 85 audit-ready UNKNOWN children."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-probe8-next-manifest.json
    role: manifest
    note: "Binds the next eight-key work order to target, cache, audit, solver, and runner hashes."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-probe8-next-raw-history-audit.json
    role: manifest
    note: "Probe-specific raw audit: eight ready keys, no exact rows, same-budget UNKNOWN rows, or conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-probe8-next-saved-s6-summary.json
    role: manifest
    note: "Probe-specific saved-s6 audit: all eight parents UNKNOWN, zero derivations and conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-rank1-10448351135500075008-0-probe8-next-preflight.json
    role: manifest
    note: "Main fail-closed validator passed for exactly the scheduled eight targets."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-build-reply27-artifact-inventory.py
    role: source
    note: "Builds the current checkpoint's artifact and manifested-source SHA-256 inventory."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-c1bf7dc3-reply27-checkpoint-artifact-hashes-20261008.json
    role: manifest
    note: "Current checkpoint inventory with hashes for all proof artifacts and their manifested sources."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-probe8-next-collected-raw-all.csv
    role: source
    note: Eight scheduled solver rows, including one UNKNOWN retained only as raw evidence.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-probe8-next-collected-summary.json
    role: manifest
    note: Probe verdict counts, node totals, UNKNOWN key, and cache binding.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-probe8-next-collected-new-exact-s5.cache
    role: data
    note: Seven exact LOSS rows from the bounded probe.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-probe8-next-collected-merged-s5.cache
    role: data
    note: Merged exact s5 cache, 4,831 unique rows with zero conflicts.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-probe8-next-collected-merge-receipt.json
    role: manifest
    note: Base/delta/cache counts, verdicts, conflicts, and SHA-256.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-probe8-next-collected-sources.json
    role: manifest
    note: Solver, runner, scheduled input, and raw-output source hashes.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-probe8-next-class-boundary-audit.json
    role: verifier
    note: "Complete 103-child class boundary: 24 LOSS, zero WIN, 79 UNKNOWN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-dual-tight-cardinality.json
    role: data
    note: Recomputed all 3,384 class statuses, secured vertices, integer cover, and rational dual.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-dual-tight-repair.json
    role: data
    note: Reoptimized three-class repair with 273 distinct UNKNOWN s5 children.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-dual-tight-ranking.json
    role: data
    note: Dual-tight repair class ranking after the exact cache merge.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-dual-tight-ranking-sources.json
    role: manifest
    note: Hashes for ranking inputs, helper sources, and generated targets.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-remaining79-raw-history-audit.json
    role: manifest
    note: "History audit of all 79 UNKNOWN children: 77 ready, two blocked keys, five same-budget UNKNOWN rows."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-remaining79-saved-s6-summary.json
    role: manifest
    note: Hash-validated 39-source audit of all 79 parents; all UNKNOWN, no derivations or conflicts.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-remaining79-saved-s6-full.json.gz
    role: source
    note: Full saved-s6 canonical boundary details for all 79 remaining parents.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-remaining79-probe8-next.csv
    role: source
    note: Eight-key low-legal-count schedule from the 77 audit-ready UNKNOWN children.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-remaining79-probe8-next-manifest.json
    role: manifest
    note: Binds scheduled keys and solver/cache/audit source hashes.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-remaining79-probe8-next-raw-history-audit.json
    role: manifest
    note: "Probe-specific raw audit: all eight keys ready with no exact, same-budget UNKNOWN, or conflict."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-remaining79-probe8-next-saved-s6-summary.json
    role: manifest
    note: "Probe-specific saved-s6 audit: all eight parents UNKNOWN with zero derivations or conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-rank1-10448351135500075008-0-remaining79-probe8-next-preflight.json
    role: verifier
    note: Main fail-closed validator passed for exactly the scheduled eight targets.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-build-reply27-artifact-inventory.py
    role: source
    note: Checkpoint inventory builder bound to this dispatch main and artifact prefix.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-6609f521-reply27-checkpoint-artifact-hashes-20261008.json
    role: manifest
    note: 77-artifact and 2,353-source inventory with zero missing paths or hash mismatches.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-10448351135500075008-0-probe8-next-collected-raw-all.csv
    role: source
    note: Eight scheduled solver rows, seven exact LOSS and one exact WIN.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-10448351135500075008-0-probe8-next-collected-summary.json
    role: manifest
    note: Probe verdict counts, node totals, and exact cache binding.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-10448351135500075008-0-probe8-next-collected-new-exact-s5.cache
    role: data
    note: Seven exact LOSS rows and one exact WIN row from the probe.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-10448351135500075008-0-probe8-next-collected-merged-s5.cache
    role: data
    note: Merged exact s5 cache with 4,839 unique rows and zero conflicts.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-10448351135500075008-0-probe8-next-collected-merge-receipt.json
    role: manifest
    note: Base/delta/cache counts, verdicts, conflicts, and SHA-256.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-10448351135500075008-0-probe8-next-collected-sources.json
    role: manifest
    note: Solver, runner, input, raw-output and main-at-dispatch bindings.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-10448351135500075008-0-class-boundary-audit.json
    role: verifier
    note: Full canonical boundary has 31 LOSS, one WIN, and 71 UNKNOWN children.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-10448351135500075008-0-class-win-geometry-audit-v2.json
    role: verifier
    note: Verifies the exact WIN witness is safe, canonical, and a legal child of the complete boundary.
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_s4_win_v2.py
    role: verifier
    note: Backward-compatible geometry audit for both collector source-manifest layouts.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-10448351135500075008-0-class-win-geometry-audit.json
    role: source
    note: Superseded first-pass report, preserved but excluded from proof; use the v2 geometry audit.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-dual-tight-cardinality.json
    role: data
    note: Recomputed all 3,384 class statuses, secured vertices, integer cover, and rational dual.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-dual-tight-repair.json
    role: data
    note: Reoptimized three-class repair with 289 distinct UNKNOWN s5 children.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-dual-tight-repair-targets.csv
    role: source
    note: UNKNOWN-only s5 targets from the updated repair.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-dual-tight-ranking.json
    role: data
    note: Re-ranked dual-tight repair after incorporating the exact WIN child.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-dual-tight-ranking-targets.csv
    role: source
    note: The 95 UNKNOWN s5 children of the current rank-1 class.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-dual-tight-ranking-sources.json
    role: manifest
    note: Hashes for ranking inputs, helper sources, and generated targets.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-1297036692683882496-0-unknown95-raw-history-audit.json
    role: manifest
    note: History audit of all 95 UNKNOWN children; no exact rows, same-budget UNKNOWN, or conflicts.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-1297036692683882496-0-unknown95-saved-s6-summary.json
    role: manifest
    note: Hash-validated 39-source audit of all 95 parents; all UNKNOWN with no derivation or conflict.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-1297036692683882496-0-unknown95-saved-s6-derived-s5.cache
    role: data
    note: Empty exact derivation cache from the 95-parent saved-s6 audit.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-1297036692683882496-0-unknown95-saved-s6-full.json.gz
    role: source
    note: Full s6 boundary details for the 95 remaining s5 parents.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-1297036692683882496-0-unknown95-probe8-next.csv
    role: source
    note: Eight-key probe schedule from the 95 audit-ready UNKNOWN children.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-1297036692683882496-0-unknown95-probe8-next-manifest.json
    role: manifest
    note: Binds scheduled keys and solver/cache/audit source hashes.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-1297036692683882496-0-unknown95-probe8-next-raw-history-audit.json
    role: manifest
    note: "Probe-specific raw audit: eight keys ready, with no exact, same-budget UNKNOWN, or conflict."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-1297036692683882496-0-unknown95-probe8-next-saved-s6-summary.json
    role: manifest
    note: "Probe-specific saved-s6 audit: all eight parents UNKNOWN, zero derivations and conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-1297036692683882496-0-unknown95-probe8-next-saved-s6-derived-s5.cache
    role: data
    note: Empty exact cache derived from the scheduled eight saved-s6 boundaries.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-1297036692683882496-0-unknown95-probe8-next-saved-s6-full.json.gz
    role: source
    note: Full saved-s6 boundary details for the scheduled eight targets.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-1297036692683882496-0-unknown95-probe8-next-preflight.json
    role: verifier
    note: Main fail-closed validator passed for exactly the scheduled eight targets.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-rank1-10448351135500075008-0-preflight.json
    role: manifest
    note: Hash-bound preflight for the preceding probe against main commit 10eaf37b.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-build-reply27-artifact-inventory.py
    role: source
    note: Checkpoint inventory builder with explicit superseded-audit exclusion.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-10eaf37b-reply27-checkpoint-artifact-hashes-20261008.json
    role: manifest
    note: 116-artifact and 2,419-source inventory with zero missing paths and hash mismatches.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692683882496-0-preflight.json
    role: manifest
    note: "Preflight of the eight scheduled keys before fetching and dispatching from main 951a5619."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692683882496-0-probe8-next-collected-raw-all.csv
    role: source
    note: "Eight exact replay rows for class (1297036692683882496,0): seven LOSS and one WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692683882496-0-probe8-next-collected-raw-exact.csv
    role: source
    note: "Raw exact solver replay rows retained for direct result verification."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692683882496-0-probe8-next-collected-exact-targets.csv
    role: source
    note: "Exact target rows copied from the audited eight-key schedule."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692683882496-0-probe8-next-collected-new-exact-s5.cache
    role: data
    note: "Seven exact s5 LOSS rows and one exact s5 WIN row from the new probe."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692683882496-0-probe8-next-collected-merged-s5.cache
    role: data
    note: "Merged exact s5 cache with 4,847 rows, 120 WIN, 4,727 LOSS, and zero conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692683882496-0-probe8-next-collected-merge-receipt.json
    role: manifest
    note: "Base/delta merge counts, verdicts, nodes, hashes, and zero-conflict receipt."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692683882496-0-probe8-next-collected-summary.json
    role: manifest
    note: "Probe verdict counts, node total, dispatch main, and exact cache binding."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692683882496-0-probe8-next-collected-runner-summary.json
    role: manifest
    note: "Bounded runner completion summary; the class stopped on its first exact WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692683882496-0-probe8-next-collected-sources.json
    role: manifest
    note: "Hashes for schedule, raw replay, cache, solver, runner, solver source, and dispatch main."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692683882496-0-class-boundary-audit.json
    role: verifier
    note: "Rebuilt all 100 canonical s5 children: 12 LOSS, one WIN, and 87 UNKNOWN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692683882496-0-class-win-geometry-audit-v2.json
    role: verifier
    note: "Binds raw/cache/source hashes and verifies the exact WIN s5 is safe, canonical, and a legal child."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-reply27-cardinality.json
    role: data
    note: "Recomputed all 3,384 class statuses, secured vertices, integer cover, and rational LP dual."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-reply27-repair.json
    role: data
    note: "Reoptimized the three-class repair; its distinct UNKNOWN s5 union contains 291 positions."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-reply27-repair-targets.csv
    role: source
    note: "UNKNOWN-only target rows materialized by the updated repair optimization."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-reply27-repair-sample.csv
    role: source
    note: "Small audit sample from the updated repair classes."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-dual-tight-ranking-repair-input.json
    role: manifest
    note: "Schema adapter copies the additive-optimum repair rows without changing verdicts or optimization."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-dual-tight-ranking.json
    role: data
    note: "Re-ranked the selected dual-tight repair classes after incorporating the exact WIN child."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-dual-tight-ranking-targets.csv
    role: source
    note: "The 95 UNKNOWN s5 children of the refreshed rank-1 class."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-dual-tight-ranking-sources.json
    role: manifest
    note: "Hashes for the exact cache, repair, cardinality, ranking helper sources, and generated targets."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692682702976-128-raw-history-audit.json
    role: manifest
    note: "2,241-CSV audit found no prior exact verdict or conflict; one key has two same-budget UNKNOWN observations."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692682702976-128-saved-s6-summary.json
    role: manifest
    note: "Hash-validated 39-source s6 audit leaves all 95 target parents UNKNOWN with zero derivations or conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692682702976-128-saved-s6-derived-s5.cache
    role: data
    note: "Empty exact s5 derivation cache from the full 95-parent saved-s6 audit."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692682702976-128-saved-s6-full.json.gz
    role: source
    note: "Full saved-s6 child-boundary details for all 95 UNKNOWN s5 parents."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692682702976-128-probe8-next.csv
    role: source
    note: "Eight-key probe schedule selected from the 94 dispatch-ready UNKNOWN children."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692682702976-128-probe8-next-manifest.json
    role: manifest
    note: "Binds the eight scheduled keys, exact cache, solver, source hashes, and full-target audits."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692682702976-128-probe8-next-raw-history-audit.json
    role: manifest
    note: "Probe-specific raw-history audit: eight ready keys, no exact/same-budget UNKNOWN rows or conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692682702976-128-probe8-next-saved-s6-summary.json
    role: manifest
    note: "Probe-specific saved-s6 audit leaves all eight parents UNKNOWN and derives no exact rows."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692682702976-128-probe8-next-saved-s6-derived-s5.cache
    role: data
    note: "Empty exact derivation cache for the scheduled eight saved-s6 boundaries."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692682702976-128-probe8-next-saved-s6-full.json.gz
    role: source
    note: "Full saved-s6 child-boundary details for the scheduled eight targets."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692682702976-128-preflight.json
    role: verifier
    note: "Main fail-closed preflight passed for eight exact scheduled keys: 8 ready, 0 blocked, 0 conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-build-reply27-artifact-inventory.py
    role: source
    note: "Checkpoint inventory builder for the 951a5619 dispatch checkpoint and all manifest-bound sources."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-reply27-checkpoint-artifact-hashes-20261008.json
    role: manifest
    note: "Checkpoint artifact and manifested-source hashes; zero missing paths or mismatches."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-collect-s6-descent-evidence.py
    role: verifier
    note: "Archives and audits the exact 83-child s6 descent."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-augment-saved-s6-source-audit.py
    role: verifier
    note: "Adds the new hash-attested s6 rows to the validated saved-s6 source union."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-parent.csv
    role: data
    note: "Single unresolved s5 parent sent to complete canonical s6 boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-raw-all.csv
    role: source
    note: "83 exact s6 replay rows covering the complete canonical boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-exact-s6.cache
    role: data
    note: "Exact s6 cache, 83 WIN and zero LOSS."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-derived-s5.cache
    role: data
    note: "Single exact s5 WIN derived from the complete all-WIN s6 boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-runner-summary.json
    role: data
    note: "Complete-boundary solver run summary and node count."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-receipt.json
    role: manifest
    note: "Collection receipt for the complete s6 boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-sources.json
    role: manifest
    note: "Hash-bound source and per-child raw evidence manifest."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-win-geometry-audit.json
    role: verifier
    note: "Independent complete s5/s6 geometry and reverse-incidence audit."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-updated-class-boundary-audit.json
    role: verifier
    note: "All 102 canonical s5 children verify the s4 class as WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-merged-s5.cache
    role: data
    note: "Merged exact s5 cache after the s6-derived witness."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-merge-receipt.json
    role: manifest
    note: "Exact cache merge receipt with zero conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-cardinality.json
    role: data
    note: "Recomputed all-class cardinality and rational dual."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-selected31-repair.json
    role: data
    note: "Reoptimized repair and distinct UNKNOWN s5 union."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-dual-tight-ranking.json
    role: data
    note: "Dual-tight next-class ranking after exact cache merge."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-next-target-unknowns.csv
    role: data
    note: "Ranked class UNKNOWN s5 targets."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-augmented-saved-s6-source-audit.json
    role: manifest
    note: "40-source saved-s6 union including the new exact descent."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-next-raw-history-audit.json
    role: verifier
    note: "Raw replay and same-budget audit for the initial 95-key target."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-next-augmented-saved-s6-summary.json
    role: verifier
    note: "Saved-s6 intersection for the 95 candidate s5 parents."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-next-augmented-saved-s6-full.json.gz
    role: source
    note: "Full saved-s6 child-boundary details for the candidate parents."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-ready.csv
    role: data
    note: "Audited eight-key probe schedule."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-ready-manifest.json
    role: manifest
    note: "Schedule and input source hashes."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-ready-preflight.json
    role: verifier
    note: "Fail-closed preflight for the exact eight-key schedule."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-raw-all.csv
    role: source
    note: "Eight exact s5 LOSS replay rows, 29,685,506 nodes."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-new-exact-s5.cache
    role: data
    note: "Exact s5 LOSS delta from the first eight-key batch."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-merged-s5.cache
    role: data
    note: "Exact cache after the first eight-key batch."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-merge-receipt.json
    role: manifest
    note: "First batch exact cache merge receipt."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-sources.json
    role: manifest
    note: "First batch source/raw hashes and per-target results."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-class-boundary-audit.json
    role: verifier
    note: "Full canonical s5 boundary after the first batch."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-cardinality.json
    role: data
    note: "All-class exact status and cover after the first batch."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-repair.json
    role: data
    note: "Repair optimization after the first batch."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-dual-tight-ranking.json
    role: data
    note: "Re-ranked repair classes after the first batch."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-next-raw-history-audit.json
    role: verifier
    note: "Fresh raw-history audit for the remaining 87 candidate keys."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-next-augmented-saved-s6-summary.json
    role: verifier
    note: "Saved-s6 audit for the remaining 87 candidate keys."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-ready.csv
    role: data
    note: "Second audited eight-key probe schedule."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-ready-manifest.json
    role: manifest
    note: "Second schedule and source hashes."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-ready-preflight.json
    role: verifier
    note: "Fail-closed preflight for the second exact eight-key schedule."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-raw-all.csv
    role: source
    note: "Second batch exact s5 LOSS replay rows, 27,060,139 nodes."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-new-exact-s5.cache
    role: data
    note: "Exact s5 LOSS delta from the second batch."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-merged-s5.cache
    role: data
    note: "Current exact s5 cache after both batches."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-merge-receipt.json
    role: manifest
    note: "Second batch exact cache merge receipt."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-sources.json
    role: manifest
    note: "Second batch source/raw hashes and per-target results."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-class-boundary-audit.json
    role: verifier
    note: "Full canonical 104-child class boundary: 25 LOSS / 0 WIN / 79 UNKNOWN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-cardinality.json
    role: data
    note: "All-class cardinality and LP dual after both batches."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-repair.json
    role: data
    note: "Reoptimized repair after both batches."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-dual-tight-ranking.json
    role: data
    note: "Ranked next target after both batches."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-build-reply27-artifact-inventory.py
    role: verifier
    note: "Checkpoint inventory builder."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-update-checkpoint-records.py
    role: verifier
    note: "Updates K0355 and the dated reply27 resume log."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-aa90bb5b-reply27-checkpoint-artifact-hashes-20261008.json
    role: manifest
    note: "205 artifact files and 2,702 manifested sources; no missing or mismatched hashes."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-build-reply27-artifact-inventory.py
    role: verifier
    note: "Validates the prior checkpoint at its recorded Git source and inventories the refreshed audit."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-update-checkpoint-records.py
    role: verifier
    note: "Updates K0355 and the dated reply27 resume log."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-rank1-10448351135499567104-0-raw-history-audit-15m.json
    role: verifier
    note: "79 remaining s5 children: 2,585 CSVs scanned, no exact result or same-budget UNKNOWN, all dispatch-ready."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-rank1-10448351135499567104-0-saved-s6-summary.json
    role: verifier
    note: "Hash-validated saved-s6 intersection for all 79 children; all UNKNOWN, no derivation or conflict."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-rank1-10448351135499567104-0-saved-s6-full.json.gz
    role: source
    note: "Complete saved-s6 child-boundary audit details for the 79 remaining s5 parents."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-rank1-10448351135499567104-0-saved-s6-derived-s5.cache
    role: data
    note: "No s5 verdicts derive from the saved-s6 intersection."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-rank1-10448351135499567104-0-probe8.csv
    role: data
    note: "Eight-target low-legal-count schedule; order is scheduling only."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-rank1-10448351135499567104-0-probe8-manifest.json
    role: manifest
    note: "Probe schedule bound to target, cache, raw/s6 audits, solver and runner hashes."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-rank1-10448351135499567104-0-probe8-raw-history-audit-15m.json
    role: verifier
    note: "Exact eight-key raw-history audit with requested 15M budget recorded in the file."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-rank1-10448351135499567104-0-probe8-saved-s6-summary.json
    role: verifier
    note: "Exact eight-key saved-s6 intersection; all UNKNOWN and no new exact result."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-rank1-10448351135499567104-0-probe8-saved-s6-full.json.gz
    role: source
    note: "Complete saved-s6 child-boundary details for the scheduled eight parents."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-rank1-10448351135499567104-0-probe8-saved-s6-derived-s5.cache
    role: data
    note: "No s5 verdicts derive from the scheduled eight saved-s6 boundaries."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-rank1-10448351135499567104-0-probe8-preflight.json
    role: verifier
    note: "Latest-main fail-closed preflight: eight ready, zero blocked, zero conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9b6362d4-reply27-checkpoint-artifact-hashes-20261008.json
    role: manifest
    note: "Prior and current checkpoint artifacts, current/historical source hashes, and 79-key preflight inventory."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-current-exact-s5-v2.cache
    role: data
    note: "Current 4,922-row canonical s5 exact cache: 121 WIN, 4,801 LOSS, no conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-current-exact-s5-v2-merge-receipt.json
    role: manifest
    note: "Audited union of the prior 4,871 rows and 51 reverse-derived s5 LOSS rows."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-s6-reverse-integration-audit-v2.json
    role: verifier
    note: "Geometry audit of 13 exact s6 LOSS rows, 51 safe canonical parent incidences, and merged cache."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-combined-saved-s6-source-audit.json
    role: manifest
    note: "41 hash-validated s6 sources, 3,043 canonical keys, no verdict conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-current-cardinality.json
    role: data
    note: "Recomputed status of all 3,384 s4 classes and the integer/LP cover certificates."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-current-repair.json
    role: data
    note: "Reoptimized three-class repair with 275 distinct unknown s5 children."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-current-repair-targets.csv
    role: data
    note: "Class repair candidates from the current exact cache."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-current-ranking.json
    role: data
    note: "Current ranking; ordering is a work heuristic, not a verdict."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-current-ranking-targets.csv
    role: data
    note: "Canonical unknown s5 children for the rank-1 class."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-rank1-10448351135499567104-0-raw-history-audit.json
    role: verifier
    note: "79-child exact-cache/raw-history audit at a 15,000,000-node budget."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-rank1-10448351135499567104-0-saved-s6-summary.json
    role: verifier
    note: "Complete saved-s6 intersection for all 79 rank-1 unknown s5 parents; no verdict derived."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-rank1-10448351135499567104-0-saved-s6-full.json.gz
    role: data
    note: "Canonical s6 boundary details underlying the saved-s6 intersection."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-rank1-10448351135499567104-0-saved-s6-derived-s5.cache
    role: data
    note: "Empty derivation cache: no target s5 verdict follows from saved s6 results."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-reply27-geometry-v1.json.gz
    role: data
    note: "Reusable canonical s4/s5 geometry index, 3,384 classes and 6,871 edges."
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/verify_post9dcb_s6_reverse_integration.py
    role: verifier
    note: "Reproducible audit for reverse s6-to-s5 integration and combined saved-s6 source history."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-build-reply27-artifact-inventory.py
    role: verifier
    note: "Builds a hash inventory and validates referenced sources for this checkpoint."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-reply27-checkpoint-artifact-hashes-20261009.json
    role: manifest
    note: "Checkpoint output hashes and 2,611 source hashes; zero missing or mismatched references."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-5dfabf84-s7-witness-class-boundary-audit.json
    role: verifier
    note: "Complete s5-to-s6-to-s7 geometry audit for an exact s4 WIN witness."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-5dfabf84-s7-witness-merged-s5.cache
    role: data
    note: "Exact s5 cache after the all-WIN s6 boundary derivation."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-5dfabf84-s7-witness-next-probe8-adaptive-merge-receipt.json
    role: manifest
    note: "Hash-bound early-stop merge for an adaptive s5 probe; exact rows only."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-5dfabf84-s7-witness-next-probe8-adaptive-geometry-audit.json
    role: verifier
    note: "Full geometry and legal-child audit for the early exact s5 WIN class."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-5dfabf84-class-88-probe8-completed-merged-s5.cache
    role: data
    note: "Exact s5 cache after the eight LOSS rows in the 88-child class follow-up."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-5dfabf84-class-88-probe8-completed-boundary-audit.json
    role: verifier
    note: "Complete 103-child s4 geometry audit after exact probe merges."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-5dfabf84-augmented-saved-s6-source-audit.json
    role: manifest
    note: "Hash-validated saved s6 source union used for reuse and reverse-incidence checks."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-5dfabf84-hard-s5-unknown-saved-s6-full.json.gz
    role: data
    note: "Complete canonical s6 boundary for the remaining hard s5 parent."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-5dfabf84-local-s5-s6-evidence-audit-after-class88.json
    role: verifier
    note: "Read-only reconciliation of preserved local exact rows against cache and saved-s6 evidence."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-inputs.csv
    role: source
    note: "All 87 canonical legal s6 targets dispatched for the hard s5 parent."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-raw-exact.csv
    role: source
    note: "Aggregate of all 87 exact s6 solver replay rows; per-position raw CSVs are retained under output/raw."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-exact-s6.cache
    role: data
    note: "87 exact s6 WIN rows from the complete boundary, with no UNKNOWN propagation."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-sources.json
    role: manifest
    note: "Per-row hashes and source paths for solver inputs, raw outputs, executable, and boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-summary.json
    role: data
    note: "87 exact s6 WIN rows, 28,266,655 nodes, and complete-boundary s5 WIN derivation."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-augmented-s6-source-audit.json
    role: verifier
    note: "All 87 new s6 results revalidated with the existing hash-attested saved-s6 corpus."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-parent-boundary-full.json.gz
    role: verifier
    note: "Independent complete-boundary audit: all 87 canonical s6 children of the s5 parent are exact WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-class-win-geometry-audit.json
    role: verifier
    note: "Geometry verifies the s5 all-WIN witness as a legal child and classifies its full s4 boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-class-boundary-audit.json
    role: verifier
    note: "Independent audit of the complete 103-child s4 class boundary after the WIN witness."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-local-s5-s6-evidence-audit-after-hard-descent.json
    role: verifier
    note: "All preserved local exact s5/s6 rows match the exact cache and hash-validated saved-s6 sources."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-history-audit.json
    role: verifier
    note: "Full s6 boundary history intersection confirms the 87 exact WIN rows and no blocked retry."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-merged-s5.cache
    role: data
    note: "Current merged exact s5 cache after the complete s6-to-s5 WIN derivation."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-merge-receipt.json
    role: manifest
    note: "Exact s5 cache merge receipt; no verdict conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-cardinality.json
    role: data
    note: "All 3,384 class statuses, 119-vertex cover minimum, rational dual, and tightness."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-repair.json
    role: data
    note: "Reoptimized three-class additive repair and distinct UNKNOWN s5 union."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-ranking.json
    role: data
    note: "Re-ranked dual-tight repair candidates; ordering is scheduling only."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-ranking-sources.json
    role: manifest
    note: "Input hash manifest for the current dual-tight repair ranking."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-next-target-class-boundary-audit.json
    role: verifier
    note: "Complete geometry audit for the newly selected 105-child next class."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-next-target-unknowns.csv
    role: data
    note: "96 exact-cache UNKNOWN s5 children of the next dual-tight class."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-next-target-raw-history-audit.json
    role: verifier
    note: "Raw replay audit for all 96 candidate children: 2 same-or-higher-budget UNKNOWN rows, 95 ready."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-next-target-saved-s6-full.json.gz
    role: data
    note: "Complete saved-s6 boundary intersections for all 96 candidate s5 parents."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-probe8.csv
    role: source
    note: "Eight low-legal-count probe targets from the 95 replay-ready s5 parents."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-probe8-schedule.json
    role: manifest
    note: "Probe schedule and exclusions; ranking is not a verdict."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-probe8-preflight.json
    role: verifier
    note: "Strict preflight passed for all eight probe targets with zero blocked keys or conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-probe8-raw-history-audit.json
    role: verifier
    note: "Exact eight-key raw replay history audit; all eight were ready with zero conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-probe8-saved-s6-summary.json
    role: verifier
    note: "Saved-s6 intersection for the exact scheduled eight-key probe; all remain UNKNOWN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-next-target-saved-s6-summary.json
    role: verifier
    note: "Saved-s6 intersection for all 96 next-class UNKNOWN parents; no new s5 result was derivable."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-derived-s5.cache
    role: data
    note: "One exact s5 WIN derived only after all 87 canonical s6 children were exact WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-next-targets.csv
    role: source
    note: "Reoptimized top dual-tight class UNKNOWN s5 children."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-hard-s5-s6-descent-v2-repair-targets.csv
    role: source
    note: "Reoptimized additive repair target union; UNKNOWN positions only."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-38613e2-reply27-checkpoint-artifact-hashes-v3-20261009.json
    role: manifest
    note: "Hash inventory for the reply27 checkpoint outputs and every manifested raw or local source."
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/audit_local_s6_boundary_history.py
    role: verifier
    note: "Rebuilds one safe canonical s6 boundary and reconciles saved and local solver history."
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/materialize_s6_descent_evidence.py
    role: verifier
    note: "Copies exact s6 raw outputs without replacing local evidence and builds a source hash manifest."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1173099-reply27-checkpoint-artifact-hashes-20261009.json
    role: manifest
    note: Latest post-1173099 reply27 checkpoint inventory; covers the new probe, s6 descent, saved-s7 intersection, raw rows, summaries, and source hashes.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1173099-dual-tight-10448351135499552768-0-probe8-merged-s5.cache
    role: data
    note: Current exact s5 cache snapshot, 4,954 entries (125 WIN, 4,829 LOSS; conflict 0).
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1173099-dual-tight-10448351135499552768-0-probe8-class-boundary-audit.json
    role: verifier
    note: Geometry reconstruction of all 105 canonical s5 children of the current s4 class.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1173099-dual-tight-10448351135499552768-0-probe8-s6-descent-summary.json
    role: data
    note: "Exact s6 descent for four UNKNOWN s5 parents: 333 WIN, 14 UNKNOWN, no LOSS and no reverse-propagated LOSS."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1173099-dual-tight-probe8-s6-s7-saved-intersection.json
    role: verifier
    note: Geometry-checked full 1,090-key s7 boundary for the 14 unresolved s6 children; saved exact intersection empty, so all remain UNKNOWN.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc8-reply27-checkpoint-artifact-hashes-20261009.json
    role: manifest
    note: Hash inventory for the 2199bcc8 reply27 checkpoint and its raw/local source evidence.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc8-s5-10448351135499552768-128-s7-witness-merged-s5.cache
    role: data
    note: Exact s5 cache after merging one geometry-verified S7-derived WIN row; 4,962 entries, conflict 0.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc8-s5-10448351135499552768-128-s7-witness-class-boundary-audit.json
    role: verifier
    note: Verifies the complete 90-child s6 boundary and exact s5 WIN witness in the 105-child reply27 s4 class.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc8-s5-10448351135499552768-128-s6-descent-summary.json
    role: data
    note: 87 new exact s6 replays; 84 WIN and 3 UNKNOWN, with UNKNOWN retained for S7 descent.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc8-s5-10448351135499552768-128-s7-witness-sources.json
    role: source
    note: Hash-bound raw inputs and exact S7 LOSS witness replays copied from preserved local results.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc8-repair-after-s7-class-win-cardinality.json
    role: data
    note: Recomputed exact class statuses, minimum class cover, and rational LP dual after the new s5 WIN.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc8-repair-after-s7-class-win-refined-repair.json
    role: data
    note: Reoptimized three-class repair with 292 distinct UNKNOWN s5 positions.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc8-repair-after-s7-class-win-ranking.json
    role: data
    note: Dual-tight repair ranking after removing the newly WIN class from eligible targets.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc-s6-1297318167661510656-33554433-probe15m-raw.csv
    role: source
    note: Exact S6 WIN replay preserved on main; 15M budget, 3,014,767 nodes.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc-s6-1297318167661510656-33554433-probe15m-target.csv
    role: data
    note: Canonical S6 replay target paired with the exact raw result.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-s6-source-manifest.json
    role: manifest
    note: Hash-bound provenance for the newly audited exact S6 replay.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-augmented-s6-source-audit.json
    role: manifest
    note: Hash-validated saved S6 corpus extended by the new exact row; conflict count 0.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-s5-10449477035406395392-0-target.csv
    role: data
    note: Geometry-audit target for the complete canonical S6 boundary of the held S5 parent.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-s6-boundary-audit-summary.json
    role: verifier
    note: "Full geometry boundary audit: 88 exact WIN, 1 UNKNOWN, no derived S5 verdict."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-s6-boundary-audit-full.json.gz
    role: data
    note: Compressed audit with all 89 canonical S6 children and their source rows.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-derived-s5.cache
    role: data
    note: Empty derived delta; the incomplete boundary does not classify the S5 parent.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-cardinality.json
    role: data
    note: Recomputed 3,384-class status, minimum cover, and rational dual from the accepted cache.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-audit-v5.json
    role: manifest
    note: Reconciliation report documenting the unsupported upstream S5 WIN row and current frontier.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-merge-receipt-v5.json
    role: manifest
    note: Records that no S5 row was derived or merged.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-artifact-hashes-v5.json
    role: manifest
    note: SHA-256 inventory for reconciliation evidence and inputs.
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-exact-s6.cache
    role: data
    note: "Hash-validated exact S6 cache: 3,574 unique rows (3,414 WIN, 160 LOSS), conflict 0."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-s6-cache-merge-receipt.json
    role: manifest
    note: "Exact S6 cache merge receipt; one new exact WIN row versus the previous audited corpus."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-audit-v6.json
    role: manifest
    note: "Reconciliation report including the materialized exact S6 cache and unchanged proof frontier."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-d0ed156-reconciliation-20261009-artifact-hashes-v6.json
    role: manifest
    note: "SHA-256 inventory including the exact S6 cache and its merge receipt."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc-s6-10449477035406395392-16777216-probe15m-target.csv
    role: source
    note: "Exact S6 replay input for the child that closed the held S5 boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc-s6-10449477035406395392-16777216-probe15m-raw.csv
    role: source
    note: "Saved exact S6 WIN replay row, archived on main."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc-s6-10449477035406395392-16777216-probe15m-audit.json
    role: manifest
    note: "Upstream replay audit with raw and target hashes."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-s6-source-manifest.json
    role: manifest
    note: "Hash-bound manifest for the newly archived exact S6 replay."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-augmented-s6-source-audit.json
    role: manifest
    note: "Rehydrated saved S6 corpus with the new replay; 653 sources, no conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-exact-s6.cache
    role: data
    note: "Exact S6 cache: 3,575 rows, 3,415 WIN and 160 LOSS, no conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-s6-cache-merge-receipt.json
    role: manifest
    note: "Records the one-row exact S6 WIN cache delta."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-s5-10449477035406395392-0-s6-boundary-audit-summary.json
    role: verifier
    note: "Complete 89-child S6 boundary audit; all children are exact WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-s5-10449477035406395392-0-s6-boundary-audit-full.json.gz
    role: data
    note: "Full geometry-generated S6 boundary and child verdict audit."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-s5-10449477035406395392-0-derived-s5.cache
    role: data
    note: "Exact S5 WIN derived only from the complete all-WIN S6 boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-exact-s5.cache
    role: data
    note: "Merged exact S5 cache after resolving the held upstream WIN row: 4,964 rows, no conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-s5-merge-receipt.json
    role: manifest
    note: "S5 cache merge receipt ties the derived row to the complete S6 boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-s5-s4-parent-incidence-audit.json
    role: verifier
    note: "Audits the exact S5 WIN incidence into all three reply27 s4 classes."
  - path: research/experiments/n11-boundary-recovery-20261006/scripts/audit_reconciled_s5_s4_parent_incidence.py
    role: verifier
    note: "Reproducible geometry check for the S5 WIN and its complete reply27 s4 parent boundaries."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-s4-10449477035406393344-0-boundary-audit.json
    role: verifier
    note: "Complete canonical s5 boundary for one reply27 s4 parent; exact WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-s4-10448351135499552768-0-boundary-audit.json
    role: verifier
    note: "Complete canonical s5 boundary for one reply27 s4 parent; exact WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-s4-1297318167661510656-0-boundary-audit.json
    role: verifier
    note: "Complete canonical s5 boundary for one reply27 s4 parent; exact WIN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-cardinality.json
    role: data
    note: "Recomputed full 3,384-class status, secured vertices, minimum cover, and rational dual."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-cover.json
    role: data
    note: "Integer repair optimization under the reconciled exact S5 cache."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-additive-targets.csv
    role: source
    note: "Distinct UNKNOWN S5 roots in the additive repair schedule."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-repair-refined.json
    role: data
    note: "Reoptimized three-class repair and distinct UNKNOWN S5 union."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-repair-ranking-targets.csv
    role: source
    note: "Current rank-1 UNKNOWN S5 target list; scheduling only."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-repair-ranking.json
    role: data
    note: "Current dual-tight repair ranking; scheduling only."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-repair-ranking-sources.json
    role: manifest
    note: "Hashes for the repair ranking inputs and generator."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-audit-v8.json
    role: manifest
    note: "Final reconciliation report; the upstream WIN row is now geometry-supported."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-reconciliation-20261009-artifact-hashes-v8.json
    role: manifest
    note: "36-file SHA-256 inventory for the reconciled checkpoint, with no missing paths or mismatches."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-unknown-s5-targets.csv
    role: source
    note: "The 96 currently UNKNOWN canonical s5 children rebuilt from the complete class boundary."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-boundary-audit.json
    role: verifier
    note: "Complete geometry audit of all 105 canonical s5 children against the latest accepted exact cache."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-raw-history-second.json
    role: manifest
    note: "Current-cache raw replay history for the full 96-key UNKNOWN boundary; same-budget UNKNOWN remains excluded."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-saved-s6-summary.json
    role: manifest
    note: "Full saved-exact-s6 intersection for all 96 UNKNOWN s5 parents; no exact s5 verdict was derived."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-probe8.csv
    role: source
    note: "Eight exact-key low-legal-count s5 probes selected from the audited ready subset."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-probe8-manifest.json
    role: manifest
    note: "Probe schedule and source hashes; scheduling order carries no verdict."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-probe8-strict-preflight.json
    role: manifest
    note: "Strict exact-cache, replay-history, saved-s6, budget, and geometry-bound preflight for the eight targets."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-probe8-raw.csv
    role: source
    note: "Preserved raw exact solver replay rows: eight exact LOSS, 36,228,485 nodes."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-probe8-exact-s5.cache
    role: data
    note: "Eight exact s5 LOSS rows from the probe, before cache integration."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-probe8-sources.json
    role: manifest
    note: "Hashes and source bindings for target, cache, solver, runner, raw rows, and preserved per-root outputs."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-merged-exact-s5.cache
    role: data
    note: "Zero-conflict merge of the 4,964-row base cache with eight exact s5 LOSS rows."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-merge-receipt.json
    role: manifest
    note: "Exact s5 cache merge receipt; 4,972 unique rows and zero verdict conflicts."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-merged-boundary-audit.json
    role: verifier
    note: "Full 105-child class boundary after merge: 17 LOSS, zero WIN, and 88 UNKNOWN."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-cardinality.json
    role: data
    note: "Recomputed all 3,384 s4 classes, secured vertices, integer cover, and rational dual."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-repair.json
    role: data
    note: "Reoptimized three-class repair after merging the eight exact LOSS rows."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-ranking.json
    role: data
    note: "Recomputed repair ranking; rank-1 scheduling target only."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-ranking-targets.csv
    role: source
    note: "UNKNOWN s5 children for the recomputed scheduling ranking."
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-1001d051-next-class-10448351135499550722-0-artifact-hashes.json
    role: manifest
    note: "29-artifact and 31-source SHA-256 inventory; no missing paths or hash mismatches."
scope: >-
  Latest computed checkpoint extends main `41c081bff38a2fe4498fd3a1725dcf63a4945446` with eight exact s5 LOSS rows. The merged exact s5 cache has 4,972 rows (128 WIN / 4,844 LOSS / conflict 0).
  All 3,384 s4 classes classify as 29 LOSS / 231 WIN / 3,124 UNKNOWN; secured third moves remain 113/119 and 6 remain. Minimum additional class cover and rational LP dual are both 3 (dual-tight).
  The reoptimized three-class repair has 284 distinct UNKNOWN s5 positions. The active class `(10448351135499550722,0)` has 105 canonical s5 children: 17 LOSS / 0 WIN / 88 UNKNOWN. Its one same-budget-UNKNOWN child remains excluded; 87 unresolved children are ready for fresh 15M exact replay.
  The re-ranked global repair target is `(1585267068834414720,0)` with 99 UNKNOWN children and coverage `{38,77,87}`; ranking is scheduling only. Finish the in-progress class path before selecting a new class.
  `{60,27}` and the 11×11 empty-board winner remain UNKNOWN.
evidence: >-
  The strict-preflighted eight-target probe returned eight exact LOSS at a 15,000,000-node budget, totaling 36,228,485 nodes. Raw rows, cache delta, runner summary, solver inputs, and per-root hashes are preserved in the probe source manifest.
  Geometry rebuilt the complete 105-child boundary after merge and confirmed 17 exact LOSS, no exact WIN, and 88 UNKNOWN. The class remains UNKNOWN. No new S6 exact results or reverse-propagated LOSS were produced.
  The full saved-S6 intersection for the 96 pre-probe UNKNOWN children derived zero s5 verdicts. Raw history scanned 4,672 CSV files and found two same-budget UNKNOWN records for one excluded key; the eight scheduled keys have zero exact hits, same-budget UNKNOWN rows, or conflicts.
  Cache cardinality and the rational LP dual were recomputed: 29 LOSS / 231 WIN / 3,124 UNKNOWN classes, 113/119 secured vertices, minimum cover 3 equals dual 3. Repair was reoptimized to 3 classes and 284 distinct UNKNOWN s5.
  Inventory `post-1001d051-next-class-10448351135499550722-0-artifact-hashes.json` verifies 29 artifacts and 31 manifested sources with no missing paths or SHA-256 mismatches.
  All results are finite exact-search/cache evidence. `{60,27}` and the 11×11 empty board remain UNKNOWN.
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

## 2026-10-08 03:36 JST dual-tight WIN checkpoint

At the start of this continuation, HEAD and fetched origin/main were both `ba3b51388b2f943f890f5f61cc2a857fd6ac2c56`; no incoming commits were found. Reused the saved 4,715-entry exact s5 cache and re-ranked the dual-tight repair before any new dispatch.

Class `(10448491872987906048,0)` had 99 canonical s5 children, seven known LOSS, and 92 UNKNOWN. The low-legal-count probe scheduled eight; five were dispatched and all exact: three LOSS and two WIN, totaling 35,507,222 nodes. The full-boundary geometry audit verified both safe canonical WIN witnesses and their legal class incidence. The complete boundary is 10 LOSS, two WIN, and 87 UNKNOWN; this class is WIN, so its other children were not explored. A witness also changes reply27 class `(1299288493570129920,0)` from UNKNOWN to WIN.

Reoptimized repair selected class `(10448351136036421632,0)` next: 98 canonical children, six known LOSS, and 92 UNKNOWN. Before the probe, the exact-cache intersection, a raw-history scan of 1,599 CSVs, and both the 37-source and supplemental 10-source saved-s6 audits found no reusable verdict, same-budget UNKNOWN, or conflict. The two s6 source sets overlap on nine paths, form a 38-path union, and have no path/hash mismatch. The first eight targets all returned exact LOSS (33,683,635 nodes). After merging and re-ranking, the class had 14 known LOSS and 84 UNKNOWN; a fresh 1,621-CSV history audit and both saved-s6 audits again found zero reusable exact results and zero same-budget UNKNOWN rows.

The completion run scheduled those 84 residual UNKNOWN children with four workers and a 15,000,000-node budget per target. It started 35 targets before an exact WIN appeared: 33 exact LOSS, one exact WIN, one UNKNOWN, and 49 not dispatched. Exact rows used 176,500,060 nodes; the UNKNOWN used its 15,000,000-node budget. The exact witness `(1297036692682719232,134217729)` was verified by independently rebuilding the complete 98-child canonical s5 boundary and checking its legal parent incidence. The final boundary has 47 LOSS, one WIN, and 50 UNKNOWN; class `(10448351136036421632,0)` is WIN. The remaining targets were stopped. This run added no exact s6 results and no reverse-propagated s5 LOSS; the budget-limited UNKNOWN was not retried.

Together the two resolved classes added 47 unique exact s5 rows (44 LOSS and three WIN). The final exact cache has 4,762 entries (105 WIN, 4,657 LOSS, conflict 0), SHA-256 `646ade4242704de54011316fd69d357e56236f2fea63b1ad5c8d9b55ccbb632f`. Recomputing all 3,384 classes gives 29 LOSS, 192 WIN, and 3,163 UNKNOWN. Secured third moves remain 113/119, with six remaining. Minimum additional classes remains three and the rational LP dual is three; dual-tight is true. The reoptimized three-class repair has 283 distinct UNKNOWN s5 positions, with selected class unknown counts 99, 93, and 91.

The new rank-1 target is `(10448351135499550752,0)`: 102 canonical children, 11 known LOSS, and 91 UNKNOWN, covering `{55,65,104}` with dual vertex 104. Its target-specific raw-history scan covered 1,697 CSVs and found no exact rows, same-or-higher-budget UNKNOWN, or conflict. The 37-source and supplemental 10-source saved-s6 audits left all 91 UNKNOWN and derived no exact result. An eight-position low-legal-count schedule is saved but has not been dispatched; it is a work order only.

The 77-file inventory [post-ba3b5138 checkpoint hashes](../../experiments/n11-boundary-recovery-20261006/output/post-ba3b5138-dual-tight-proof-checkpoint-artifact-hashes-20261008.json) has working-tree SHA-256 `1cdc9a5305f4509f5c8d826d6007960398e407c50241b8637727d45d481fc2da` and Git-blob SHA-256 `f6d7a58a9d8875f482f2f934efbcebd60077ebaa4830717bce977a0a72d2680b`. `{60,27}` remains UNKNOWN. The 11×11 empty board remains UNKNOWN.

## 2026-10-08 04:01 JST dual-tight probe8 WIN checkpoint

Fetched and verified `origin/main` at `b20949a5ad91aadf4ddc7f56023429c7650dd154` before dispatch. No same-target solver process or pre-existing output directory was found. The saved 8-target schedule for `(10448351135499550752,0)` was bound to its manifest and rechecked against the exact solver binary, solver source, runner, and cache hashes. The complete boundary had 102 canonical s5 children, with 11 exact LOSS and 91 UNKNOWN before the probe.

The probe completed all eight scheduled replays: six exact LOSS, one exact WIN, and one UNKNOWN. Exact verdict rows used 43,511,040 nodes; the UNKNOWN used its 15,000,000-node budget, for 58,511,040 total. The exact WIN witness is s5 `(10448351135499550752,262144)` at 13,006,632 nodes. The remaining 83 class children were not dispatched; no s6 descent or reverse-propagated LOSS was performed.

The independent geometry verifier rebuilt all 102 canonical children and checked the witness is safe, canonical, and a legal child of the target class. The complete boundary is 17 LOSS / 1 WIN / 84 UNKNOWN, so `(10448351135499550752,0)` is exact WIN. The witness also changes reachable reply27 class `(5800636320187416576,0)` from UNKNOWN to WIN. The verified audit records one additional legal parent class that was already WIN before this probe.

Merged cache: 4,769 exact s5 rows, WIN 106 / LOSS 4,663 / conflicts 0; SHA-256 `435c3ec1ff05dfe6debed7d3db0135a9219c41580aef3e66eaccc819afb24943`. Recomputed all 3,384 s4 classes: LOSS 29 / WIN 194 / UNKNOWN 3,161. Secured third moves remain 113/119, with six remaining. Minimum additional class cover is 3; rational LP dual is 3 and dual-tight is true, with positive dual weights on vertices 77, 100, and 104. The reoptimized repair has three classes and 283 distinct UNKNOWN s5 positions.

The next rank-1 repair class is `(10448386319871639552,0)`: 99 canonical s5 children, eight known LOSS, 91 UNKNOWN, coverage `{103,104,105}`, dual vertex 104. Ranking is work order only; the target must pass cache/raw-history/saved-s6 audits before any dispatch. The 17-file output inventory plus solver/source and preserved `.local` run hashes is `post-b20949a5-next-after-completion84-probe8-artifact-hashes-20261008.json`, working-tree and Git-blob SHA-256 are both `87ffd2c02a61ac13d3268a147a717d9599d46317d42f5c587ef8b2bdd961eba3`.

`{60,27}` remains UNKNOWN. The 11×11 empty board remains UNKNOWN.

## 2026-10-08 04:34 JST dual-tight probe8 WIN checkpoint

Fetched and verified latest `main` at `046db7873c2895e5ceba80ec0e416c71f937e0bd` before dispatch. Candidate `(10448386319871639552,0)` had 99 canonical s5 children (8 LOSS, 91 UNKNOWN). The raw-history audit covered 1,719 CSV files and found zero reusable exact results, same-budget UNKNOWN rows, or conflicts. The combined 38-source saved-s6 audit left all 91 UNKNOWN and derived no exact s5 result.

The eight-position probe dispatched five targets before exact WIN: three exact LOSS and two exact WIN, using 27,772,825 nodes; the remaining three were not dispatched. Full geometry rebuilt the 99-child boundary and confirmed both WIN witnesses `(10448386319871639552,8)` and `(10449512219778482176,0)` are safe canonical legal children. The class boundary is 11 LOSS / 2 WIN / 86 UNKNOWN, so the class is exact WIN. The witnesses also close classes `(10376328725833711616,8)` and `(1306325366914154496,0)` as WIN. No s6 descent or reverse-propagated LOSS occurred.

Merged cache: 4,774 exact s5 rows (108 WIN, 4,666 LOSS, conflicts 0), SHA-256 `3300c3b2970679bab56558696edb255fc7b7ee8de1acde904b2c008542e22906`. Recomputing all 3,384 s4 classes gives 29 LOSS / 197 WIN / 3,158 UNKNOWN; secured vertices remain 113/119, with six remaining. Minimum additional class cover and rational LP dual are both 3, dual-tight. The reoptimized repair has three classes and 283 distinct UNKNOWN s5 positions. Next rank-1 target is `(10448351135499550784,0)`: 100 canonical children, 9 known LOSS, 91 UNKNOWN, coverage `{44,54,104}`, dual vertex 104; audit it before dispatch.

The 23-file output inventory `post-046db787-dual-tight-probe8-artifact-hashes-20261008.json` has working-tree SHA-256 `0befa0bee4d5eaf17704578c43ec473fc3d2c8a2d98d3289b5fe12cec554a5e8`; it also records input, solver/source, and preserved `.local` raw-run hashes. `{60,27}` and the 11×11 empty board remain UNKNOWN.

## 2026-10-08 05:07 JST dual-tight probe8 WIN checkpoint

Fetched latest main and verified `HEAD == origin/main == 7e1caa9693d25d09285e476c6b7781880eb2d0f3` before dispatch. Candidate `(10448351135499550784,0)` had 100 canonical s5 children (9 LOSS, 91 UNKNOWN). The 1,735-CSV raw-history audit found two distinct same-budget UNKNOWN children, which were excluded; 89 targets remained dispatch-ready. The 38-source saved-s6 audit left all 91 parents UNKNOWN and derived no exact s5 verdict.

The eight-target probe completed six rows before stopping after exact WIN: four exact WIN, two exact LOSS, 47,436,351 nodes; two scheduled children were not dispatched. Independent geometry rebuilt the complete 100-child boundary and verified all four witnesses `(1297036692682702864,65)`, `(10448351135499550784,64)`, `(10448351135499616320,0)`, and `(10448352235011178560,0)` as safe canonical legal children. The class boundary is 11 LOSS / 4 WIN / 85 UNKNOWN, so the class is exact WIN. Three other reachable reply27 classes also changed from UNKNOWN to WIN. No s6 descent or reverse-propagated LOSS occurred.

Merged exact s5 cache: 4,780 entries (112 WIN, 4,668 LOSS, conflicts 0), SHA-256 `95ce0a20d3fc83327b9f0f9ce52f4180ec34e877b773cade2f5121d519eaabfe`. Recomputed all 3,384 s4 classes: LOSS 29 / WIN 201 / UNKNOWN 3,154. Secured third moves remain 113/119, with six remaining. Minimum additional class cover and rational LP dual are both 3, dual-tight. The reoptimized repair has three classes and 284 distinct UNKNOWN s5 positions. Next rank-1 class is `(10448351135499550976,0)`: 101 canonical children, 9 known LOSS, 92 UNKNOWN, coverage `{22,32,104}`, dual vertex 104; audit it before dispatch.

The 23-file output inventory `post-7e1caa96-dual-tight-probe8-artifact-hashes-20261008.json` has working-tree SHA-256 `dc3c2e3047b16018f30ee9b2b8f0ee6db0a5280a371d0404d2092c8794f9aa9f` and records source hashes for 41 inputs, including preserved `.local` solver files. `{60,27}` and the 11×11 empty board remain UNKNOWN.

## 2026-10-08 05:29 JST dual-tight probe8 WIN checkpoint

Fetched latest main and verified `HEAD == origin/main == f390d2900fb1a50a2da173e185c0dca6684ef2e5` before dispatch. Candidate `(10448351135499550976,0)` had 101 canonical s5 children (9 LOSS, 92 UNKNOWN). The 1,753-CSV raw-history audit found one distinct same-budget UNKNOWN child, which was excluded; 91 keys remained dispatch-ready. The 38-source saved-s6 audit left all 92 parents UNKNOWN and derived no exact s5 verdict.

The eight-target probe completed six rows before exact WIN stop: two exact WIN and four exact LOSS, using 35,250,655 nodes; two targets were not dispatched. Full geometry rebuilt the 101-child boundary and confirmed witnesses `(1152921504606912512, 17733517312)` and `(1297036692682702852, 67108865)` are safe canonical legal children. The class boundary is 13 LOSS / 2 WIN / 86 UNKNOWN, so the class is exact WIN. No s6 descent or reverse-propagated LOSS occurred.

Merged cache: 4,786 exact s5 rows (114 WIN, 4,672 LOSS, conflicts 0), SHA-256 `55d1468ce93a00fd86d02111a8aafcaeebee5e515daec0ddc50282209d1043ec`. Recomputed all 3,384 s4 classes: LOSS 29 / WIN 202 / UNKNOWN 3,153. Secured third moves remain 113/119, with six remaining. Minimum additional class cover and rational LP dual are both 3, dual-tight. The reoptimized repair has three classes and 286 distinct UNKNOWN s5 positions. Next rank-1 class is `(10412322338480590848,0)`: 100 canonical children, 7 known LOSS, 93 UNKNOWN, coverage `{100,108,115}`, dual vertex 100; audit it before dispatch.

The 23-file output inventory `post-f390d290-dual-tight-probe8-artifact-hashes-20261008.json` has working-tree SHA-256 `7aa39463401d2f156609a3c3dd62cda82ddc06f9c251d1f0b67f8999c3dee42d` and records 41 source/raw entries, including preserved `.local` solver files. `{60,27}` and the 11×11 empty board remain UNKNOWN.

## 2026-10-08 12:46 JST cache checkpoint and next-target audit

At resumption, the working tree was at `f689f75bb209ded990cd44a130c691c4e895e90f` and `origin/main` had advanced to `d9583782388019fb96e5191491a281f4a672542d`. The incoming commits changed capacity/K0072 research and generated views only, with no overlap in reply27 or the local evidence. Fast-forwarded to `d9583782`; prior `.local` and raw evidence were preserved.

The exact result from the preceding local checkpoint is class `(10412322338480586760,0)`: its complete canonical s5 boundary has 14 LOSS, one exact WIN, and 85 UNKNOWN. The exact WIN s5 witness `(10414574138294272008,0)` has all 83 canonical s6 children exact WIN. Geometry verification confirms the complete class boundary and legal incidence; class exploration stopped after the WIN. No exact s6 LOSS was found, so reverse-propagated LOSS is zero.

Merged exact s5 cache: 4,809 entries (WIN 117, LOSS 4,692, conflict 0), SHA-256 `5c78d9f9b73cc0271160974eb0d9cb69935de36c7a183a5c48e4151d0bbffa58`. Recomputed all 3,384 classes: LOSS 29 / WIN 209 / UNKNOWN 3,146. Secured vertices remain 113/119, leaving six. Minimum additional class cover and rational LP dual are both 3, dual-tight. The reoptimized repair has three classes and 288 distinct UNKNOWN s5 positions.

Re-ranking selects `(10448355533546061824,0)` next: 102 canonical s5 children, eight known LOSS and 94 UNKNOWN, coverage `{14,18,104}` with dual vertex 104. A new raw-history scan of 2,090 CSV files found no exact rows or conflicts, but found two same-budget UNKNOWN records for `(1297036692683751424,16385)`; that key is excluded, leaving 93 dispatch-ready. The s6 audit hash-validates the original 38-source corpus plus the new complete 83-child exact WIN boundary (39 source files, 2,890 unique canonical keys: 2,697 WIN, 147 LOSS, 46 UNKNOWN-only, conflict 0). Across the candidate's 94 complete s6 boundaries, no s5 verdict was derivable; all 94 remain UNKNOWN. An eight-target low-legal-count probe is prepared from the ready set but has not been dispatched.

The artifact inventory is `post-d9583782-reply27-checkpoint-artifact-hashes-20261008.json` (SHA-256 `ab753e7598b7a3c85d04e02fea824fd1d9972a101673c0c9e59477a1ae767fef`; 136 output artifacts, 2,147 manifested source files, zero missing or hash mismatches). `{60,27}` remains UNKNOWN; the 11×11 empty board remains UNKNOWN.

## 2026-10-08 13:08 JST dual-tight probe8 WIN checkpoint

Fetched `origin/main` at `d538a68a85ece7d90b2b677e18447176acad9906`; it was already the local `main` tip and had no incoming changes. Preserved `.local` and the existing test-temp directories. The scheduled eight-target probe for `(10448355533546061824,0)` completed all eight rows: six exact LOSS, one exact WIN, and one UNKNOWN, using 61,615,851 total nodes. The UNKNOWN row remains raw evidence and is excluded from the exact cache.

Geometry rebuilt the complete 102-child canonical s5 boundary and verified the exact WIN witness `(10449481433452904448,0)` is safe, canonical, and a legal child. The boundary is 14 LOSS / 1 WIN / 87 UNKNOWN, so the s4 class is WIN. The witness also changes reachable class `(1153202979717791744,0)` from UNKNOWN to WIN; another reachable parent was already WIN. No s6 descent or reverse-propagated LOSS occurred.

The merged exact cache is 4,816 rows (WIN 118 / LOSS 4,698 / conflict 0), SHA-256 `16ec4e94d965e77866ba3c78275ed37c9f9fc5ddfeec4cc56e2d9300f0a15adf`. Recomputed all 3,384 classes: LOSS 29 / WIN 211 / UNKNOWN 3,144; secured 113/119 and six remain. Minimum additional class cover and rational LP dual are both 3, dual-tight. The reoptimized repair has three classes and 288 distinct UNKNOWN s5 positions. The new rank-1 class `(10448351135500075008,0)` has 103 children, nine known LOSS, 94 UNKNOWN, coverage `{23,31,104}`, and dual vertex 104.

Before its next dispatch, a 2,120-CSV raw-history audit found two same-budget UNKNOWN rows for the same key `(1152921504607961088,570425344)`; that key is excluded, leaving 93 ready. The hash-validated 39-source saved-s6 intersection checked all 94 s5 boundaries and derived zero results; every parent remains UNKNOWN and there are no conflicts. An eight-target low-legal-count schedule is saved but not yet dispatched.

After main advanced to `42375bed` with a fail-closed preflight binding, repeated both audits on the exact eight-key schedule. The 2,121-CSV probe-specific raw audit found zero prior exact rows, same-budget UNKNOWN rows, or conflicts; all eight are ready. The same 39-source saved-s6 audit checked those exact eight parents: all remain UNKNOWN, with zero derivations/conflicts. `verify_dual_tight_probe_preflight.py` passed the main validator against the identical target and cache hashes. The probe remains scheduled but undispatched.

Checkpoint inventory `post-d538a68-reply27-checkpoint-artifact-hashes-20261008.json` has SHA-256 `e034ac96df04fdcbcf26e91295f3d2f20f1c7aba9c3f25713b7df1034459f0df` and covers 176 artifacts plus 2,213 manifested sources, with zero missing paths or hash mismatches. `{60,27}` remains UNKNOWN; the 11×11 empty board remains UNKNOWN.


## 2026-10-08 13:59 JST dual-tight probe8 LOSS checkpoint

At the start, `HEAD == origin/main == 6609f5213f141f22753e91ba16676b0a07b08f1d`; `git fetch origin main` succeeded with no incoming commit. No matching solver process was present before dispatch. The saved eight-target schedule for `(10448351135500075008,0)` had passed its hash-bound raw-history/saved-s6 preflight against this main commit.

The bounded probe completed all eight s5 rows: seven exact LOSS and one UNKNOWN, with 66,569,568 total nodes. Exact rows used 51,569,568 nodes; the single UNKNOWN used its 15,000,000-node budget and remains raw-only. There was no exact WIN, s6 solver result, or reverse-propagated LOSS. Geometry rebuilt the full 103-child canonical boundary as 24 LOSS / 0 WIN / 79 UNKNOWN, so the s4 class remains UNKNOWN.

The merged exact cache has 4,831 rows (WIN 118 / LOSS 4,713 / conflict 0), SHA-256 `a61595bf71f857c9d4815a0815c793a9223e8345b4d817ac39907651aede79c0`. Recomputed all 3,384 s4 classes: LOSS 29 / WIN 211 / UNKNOWN 3,144; secured vertices remain 113/119 with six remaining. Minimum additional classes and rational LP dual are both 3 (dual-tight). The reoptimized repair has 273 distinct UNKNOWN s5 children. The current rank-1 class is still `(10448351135500075008,0)`, with 79 UNKNOWN s5 children.

The 79-child raw-history audit scanned 2,180 CSV files and found no exact verdicts or conflicts. Two distinct keys have five same-budget UNKNOWN observations total; those keys remain excluded, leaving 77 dispatch-ready children. A hash-validated 39-source saved-s6 audit covered all 79 complete canonical s6 boundaries and derived no s5 verdict; every parent remains UNKNOWN. An eight-key schedule from the ready set was prepared. Its probe-specific 2,181-CSV audit found no exact result, same-budget UNKNOWN, or conflict; the saved-s6 audit leaves all eight UNKNOWN, and the fail-closed preflight passes with 8 ready / 0 blocked / 0 conflicts. The schedule is not yet dispatched.

Inventory `post-6609f521-reply27-checkpoint-artifact-hashes-20261008.json` records 77 artifacts and 2,353 manifested sources, with zero missing paths or hash mismatches; SHA-256 is `afc47e33f785c6c4d63871d412101d7c9e360cc4864c522e8374ce1cee5252d8`. `{60,27}` and the 11×11 empty board remain UNKNOWN.

## 2026-10-08 14:20 JST dual-tight probe8 WIN checkpoint

Before dispatch, `HEAD == origin/main == 10eaf37b847f7d4817bcde260298cfcfbe78f587`; fetch found no incoming commit and no same-target process or run directory existed. The schedule for rank-1 class `(10448351135500075008,0)` was hash-bound to the exact cache, raw-history audit, saved-s6 audit, solver, and runner.

All eight scheduled s5 children completed: seven exact LOSS and one exact WIN, using 41,991,333 nodes. The exact WIN witness is `(1152921504606912512,9160359936)`. Full geometry rebuilt all 103 canonical children and verified the witness is safe, canonical, and a legal child of the s4 class. The boundary is 31 LOSS / 1 WIN / 71 UNKNOWN, so the class is WIN. Its 71 unexplored siblings were not dispatched. No s6 solver result or reverse-propagated LOSS was produced.

The merged exact cache has 4,839 rows (WIN 119 / LOSS 4,720 / conflict 0), SHA-256 `6bb60cebe435fe18fe45f834c0752d23515128d2d27d2ac81900c02a7fec3a04`. Recomputed all 3,384 classes: LOSS 29 / WIN 213 / UNKNOWN 3,142; secured vertices remain 113/119, six remain. Minimum additional classes and rational dual are both 3 (dual-tight). The reoptimized repair has 289 distinct UNKNOWN s5 children.

The new rank-1 class is `(1297036692683882496,0)`: 100 canonical s5 children, five known LOSS and 95 UNKNOWN, covering `{67,75,100,108}`. Its raw-history audit scanned 2,210 CSV files and found no exact, same-budget UNKNOWN, or conflicts. The hash-validated 39-source saved-s6 audit left all 95 parents UNKNOWN and derived no result. An eight-key schedule from those 95 ready targets passes exact-key raw-history/saved-s6 preflight (8 ready / 0 blocked / 0 conflicts); it is not yet dispatched.

To preserve the earlier verifier source hash recorded by existing artifacts, the historical v1 verifier was restored and the v2-manifest-compatible checker was added as a separate `verify_dual_tight_s4_win_v2.py`. The v2 geometry audit is the accepted witness report. A first-pass report is retained but explicitly excluded from the verified artifact set.

Inventory `post-10eaf37b-reply27-checkpoint-artifact-hashes-20261008.json` has 116 verified artifacts and 2,419 manifested sources, zero missing paths or hash mismatches; SHA-256 is `b64a942c09148f3c6e28327904aa20be314aa0d924680d3485e3def75608363a`. `{60,27}` and the 11×11 empty board remain UNKNOWN.

## 2026-10-09 05:10 JST dual-tight probe8 LOSS and s6 boundary audit

At the start, `HEAD == origin/main == 1173099dbed01b905a8cb80281beb2696f61bb93`; `git fetch origin main` found no incoming commit. No same-target solver process was present before the next exact dispatches. The rank-1 dual-tight class `(10448351135499552768,0)` had 105 canonical s5 children, 9 exact LOSS and 96 UNKNOWN. Its eight-target 15M probe returned 4 exact LOSS and 4 UNKNOWN, 91,173,808 total nodes. The full geometry audit now verifies 13 LOSS / 0 WIN / 92 UNKNOWN; the class remains UNKNOWN.

The four UNKNOWN s5 probe parents had complete canonical s6 boundaries of 89, 89, 87, and 89 children, with 354 parent-child incidences and 348 unique s6 keys. Saved exact s6 reuse contributed one WIN. The 347 new 2M s6 replays returned 333 WIN and 14 UNKNOWN, using 145,483,366 nodes. There were no exact s6 LOSS rows, no s5 rows derived, and no reverse-propagated LOSS. A geometry-generated union of the 14 unresolved s6 parents had 1,090 canonical s7 children. A scan of 4,710 files under `research/experiments` and `.local/n11` found zero matching exact s7 rows and zero conflicts; all 14 remain UNKNOWN. No s7 solver replay was dispatched.

The merged exact s5 cache is 4,954 entries (125 WIN / 4,829 LOSS / conflict 0). Recomputed all 3,384 s4 classes: 29 LOSS / 226 WIN / 3,129 UNKNOWN; secured third moves 113/119, six remain. Minimum additional class cover is 3 and matches rational dual 3. The additive-optimal repair is three classes and 288 distinct UNKNOWN s5 positions. Re-ranking still selects `(10448351135499552768,0)` with 92 UNKNOWN s5 children. Inventory `post-1173099-reply27-checkpoint-artifact-hashes-20261009.json` covers 405 artifacts and 1,355 manifested sources, with no missing paths or hash mismatches (SHA-256 `4321d32a308a3303db8c8556a5787e900d50f0c027be678ebb52dc8f52b468a0`). `{60,27}` and the 11×11 empty board remain UNKNOWN.
## 2026-10-09 07:13 JST latest-main S6 reconciliation hold

Fetched and fast-forwarded `main` to `d0ed156ca6a7c6c596d08da518d5c32b911ae8ba`. The incoming S6 replay for `(1297318167661510656,33554433)` is an exact WIN at 15,000,000 nodes (3,014,767 nodes). Its hash-bound source and target are preserved on main; an independent geometry audit added it to the saved S6 corpus with zero conflicts.

For the upstream S5 row `(10449477035406395392,0)`, the complete canonical S6 boundary has 89 children: 88 exact WIN, zero exact LOSS, and one UNKNOWN. The remaining child `(10449477035406395392,16777216)` has only a saved 2,000,000-budget UNKNOWN; the saved S7 intersection has no exact witness. The S5 parent therefore remains UNKNOWN, and no S5 row was derived or merged. The upstream WIN row is held out as unverified; no opposing exact verdict is asserted.

Using the accepted pre-delta cache (4,963 rows: 127 WIN / 4,836 LOSS, conflict 0), recomputation gives 29 LOSS / 230 WIN / 3,125 UNKNOWN classes, secured 113/119 vertices, minimum additional cover 3 equal to rational dual 3, dual-tight, and 292 distinct UNKNOWN s5 positions in the three-class repair. Rank 1 remains `(10448351135499550722,0)` with 96 UNKNOWN s5 children. These figures exclude the held upstream row and are unchanged by the new S6 result.

Materialized the hash-validated exact S6 cache from the saved source audit: 3,574 unique exact rows (3,414 WIN / 160 LOSS, conflict 0), with one new exact WIN row versus the prior corpus. Cache SHA-256 is `b0b9c608a9abab455dcbcdca97fa5c1492c10854159d28b8883cac61ce0ebb21`; the cache merge receipt records the source audit and delta.

Because the upstream S5 WIN row is not supported by a complete all-WIN S6 boundary, cache merge, further solver dispatch, commit, and push are on hold. Reconciliation report `post-d0ed156-reconciliation-20261009-audit-v6.json` has SHA-256 `14cab1dffb5843a52a12fb4fc33e1f33f43a1ec37bee93d2ebb3e1f665d8a9b2`; its artifact inventory SHA-256 is `0dc7e80962ad428ab7b3344928069379c44ce97b6f7992311a1f89dc35f6b7bc`. `{60,27}` and the 11×11 empty board remain UNKNOWN.

## 2026-10-09 09:21 JST S6 reconciliation and exact S5 WIN checkpoint

`git fetch origin main`取得後、incoming commit `1001d051ab23e0c5130c42260bb4249fbd73a15d`の3 artifactを確認し、作業中の証拠を保ったままfast-forwardした。開始時にreply27 solver processはなかった。

main追加のS6 `(10449477035406395392,16777216)` は15,000,000 budgetでexact WIN、2,607,291 nodes。raw・target・auditのhashをmanifest化し、653 sourceの保存済みS6 corpusへ追加、geometry/legal auditを再検証した。exact S6 cacheは3,575 rows (WIN 3,415 / LOSS 160, conflict 0)。

S5 `(10449477035406395392,0)` の完全canonical S6 boundaryは89 childrenすべてexact WIN。したがってS5 AND位置はexact WINであり、previously held upstream rowと一致する。S5の3つのreply27 s4 parentを点削除geometryから列挙し、各完全canonical s5 boundaryを再生成して、target incidenceとclass WINを検査した。affected classes are `(10449477035406393344,0)`, `(10448351135499552768,0)`, and `(1297318167661510656,0)`; no remaining siblings were dispatched.

Accepted exact s5 cacheは4,964 rows (WIN 128 / LOSS 4,836 / conflict 0)。3,384 class statuses are LOSS 29 / WIN 231 / UNKNOWN 3,124; secured vertices 113/119, remaining 6. Minimum class cover and rational dual are both 3, dual-tight; reoptimized repair has 3 classes and 292 distinct UNKNOWN s5. Rank 1 is `(10448351135499550722,0)`, 105 children with 9 LOSS / 96 UNKNOWN. Ranking is scheduling only.

Reconciliation report `post-1001d051-reconciliation-20261009-audit-v8.json` and 36-file inventory `post-1001d051-reconciliation-20261009-artifact-hashes-v8.json` preserve the source hashes and geometry checks. The inventory SHA-256 is `6e33054121ac86f9ab6ef779adf79fc5111e6ebf3d4e6631f363dadacf082b46`. `{60,27}` and the 11×11 empty board remain UNKNOWN.

## 2026-10-09 checkpoint after dual-tight probe8 LOSS

Starting from fetched main `41c081bff38a2fe4498fd3a1725dcf63a4945446`, refreshed the target boundary, current raw-history audit, and saved-S6 intersection against the accepted 4,964-row exact cache. The full 105-child s4 boundary `(10448351135499550722,0)` had 9 exact LOSS, 0 WIN, and 96 UNKNOWN s5 children. Across 4,672 CSV replay sources, raw history found two 15M-budget UNKNOWN rows for one canonical key; that key was excluded. The full saved-S6 audit derived no exact s5 verdict. Strict preflight passed for eight fresh targets.

All eight probes returned exact LOSS, totaling 36,228,485 nodes. No exact WIN was found, so the active class remains in progress. Merging the raw rows gives 4,972 exact s5 rows (128 WIN / 4,844 LOSS / conflict 0), SHA-256 `4c8584febd0e6615169acca38a424c4973bb735ccf4474b48a6a6fae6ce8ec3b`. Full geometry verifies the active class at 17 LOSS / 0 WIN / 88 UNKNOWN; its remaining one previously budget-exhausted key stays blocked.

Recomputed all 3,384 s4 classes: 29 LOSS / 231 WIN / 3,124 UNKNOWN; secured 113/119, six remain. Integer minimum cover 3 equals the rational dual 3 (dual-tight). Reoptimized three-class repair has 284 distinct UNKNOWN s5 positions. The global rank-1 repair target is now `(1585267068834414720,0)` with 99 UNKNOWN; this is scheduling only. Continue the active class first: 87 remaining children are ready for exact replay, and one same-budget UNKNOWN must descend through its complete s6 boundary. Inventory `post-1001d051-next-class-10448351135499550722-0-artifact-hashes.json` contains 29 outputs and 31 source files, with zero missing paths or hash mismatches (SHA-256 `4c86d03b633044d875414362f92e37ec2774c8ece90642bd6a03d09d7201611a`). `{60,27}` and the 11×11 empty board remain UNKNOWN.
