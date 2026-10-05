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
    note: 13 class、1,227 UNKNOWN s5位置の修復target計算
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
scope: Actions run 37334644565、37336924568、37337141197に保存された11×11 reply27 exact s5/s6結果と、それらを使う有限frontier計算
evidence: 既存のexact replay結果を回収し、canonicality・安全性・D4親子geometry・verdict衝突を監査して統合。失敗runの保存済み結果の再計算ではない
---

# 11×11 reply27の保存済みexact結果から復元したcache frontier

この項目は、失敗したActions runに保存されていたexact結果を再計算せず回収・監査・永続化した有限計算を記録する。別の作業時点で`origin/main`には同等のcache回収と正規化修正が到着していたため、ここではその時点で得た証跡と監査範囲を記録する。新しい探索結果の主張ではない。

## 保存結果と計算

基準run `37334644565` のcacheはcanonical s5が2,529件（WIN 63、LOSS 2,466）。保存済みmodel8 cacheは追加でLOSSを8件増やし、shared s6 run `37336924568` は16件（WIN 10、LOSS 6、UNKNOWN 0）を含む。shared s6 metadataは66の親子relation、65の親候補を記録している。16キー中13キーがnoncanonicalだったため、各盤面の安全性、D4正規化、およびsafe s6から一点削除して得る親子relationを独立にgeometryから検証した。6つのLOSS s6結果から25件のs5 LOSS witnessを派生した。

失敗したcompletion86 run `37337141197` の保存CSVを監査し、86件すべてLOSS、合計361,568,619 nodesと確認した。基準cache、model8、shared s6派生分、completion86の結果を衝突なく統合したcacheは2,648件（WIN 63、LOSS 2,585、conflict 0）。Actions run `37338193154` から独立に再構成されたcurrent cacheと全2,648行が一致した。s4 class `(1297036692816953344, 0)` のcanonical s5境界105件はすべてLOSSで、`verify_reply27_loss_class_cache.py` により検査した。

この有限cacheでs4 classはWIN 129、LOSS 18、UNKNOWN 3,237。root verticesは119個中72個がsecuredで47個がremaining。残りを覆う最小追加class数は13で、rational LP dualの値13と整数被覆の最適値13が一致する。13-class repairのUNKNOWN s5 unionは1,227件（加法目的値も1,227）。次にrankされたtargetは`(1298162592590594048, 0)`で、101子の内訳は既知LOSS 12、UNKNOWN 89、coverageはvertices 70、72、100、108である。これらは計算対象の最小スケジュールであり、UNKNOWN classをLOSSと証明するものではない。

11×11空盤面と`{60,27}` rootはUNKNOWNのままで、終端までのAND/OR証明は未完了。cold cross-checkおよびテストは親作業で継続中のため、成功したとは記録しない。

再現CLI、保存入力、raw shard、receiptへのリンクは[実験README](../../experiments/n11-boundary-recovery-20261006/README.md)を参照。
