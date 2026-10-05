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
    note: latest merged canonical exact s5 cache with 3,234 entries, WIN 65 and LOSS 3,169
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next4-receipt.json
    role: manifest
    note: source hashes, counts, nodes, and zero conflict for the merged 3,234-entry cache
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next4-cardinality.json
    role: data
    note: 3,234-cache finite class counts, secured vertices, and dual-tight minimum cover 10
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
scope: Actions runs 37334644565、37336924568、37337141197、37339663025、37269759034、37320154141、37339357570、37339329716の保存済み11×11 reply27 exact s5/s6結果、local completion、expanded saved-s6 reverse propagation、および3,234-entry checkpoint下のfinite frontier計算
evidence: 保存済みexact solver verdictを前提として、canonicality・安全性・D4親子geometry・境界coverage・verdict衝突を監査。LOSS s6だけからs5 parent LOSSを派生しUNKNOWNは伝播しない。hard1 witnessと98-child class境界、next4の100-child class境界をruntime geometryで直接検査し、3,234-entry checkpointでclass countsとdual-tight finite coverを計算。UNKNOWN classは未証明で、geometry cacheは性能用でproofではない
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

勝敗規約は、位置の真偽値が「先手固定視点で最終的に先手が勝つ」であり、偶数石OR・奇数石ANDである（[K0002](K0002-grundy-and-first-move-conventions.md)、`cpp/solvers/kyouen_dfpn_root.cpp`）。従って、ある初手の後のs4 LOSSが全119の第三手選択をcoverすれば、各s3 odd AND位置はLOSSとなり、s2 `{60,27}` のOR位置もLOSSとなる。これは後手が中央初手60に27で応じることで中央初手を破る方向の証拠であり、中央初手60の勝ちを示すものではない。空盤の勝敗は他の初手も検査しないと決まらない。

この時点では空盤面勝敗と`{60,27}` outcomeは未確定で、終端までのAND/OR証明は未完了。別のcold residual mex cross-checkは6件中3件（120、158、192秒）で停止し、production結果には採用していない。6件完了とは主張しない。6つのevidence-recovery regression testsと33 knowledge testsは成功済み。

再現CLI、保存入力、raw shard、receiptへのリンクは[実験README](../../experiments/n11-boundary-recovery-20261006/README.md)を参照。
