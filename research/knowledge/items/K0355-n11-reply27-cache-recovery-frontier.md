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
    note: 最新cacheで再計算したrepair対象
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
    note: 最新canonical exact s5 cache 2,822件 (WIN 65, LOSS 2,757)
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next2-receipt.json
    role: manifest
    note: next2 source別の件数・verdict・node数・hash、衝突0
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next2-cardinality.json
    role: data
    note: 最新cacheでのclass数、secured vertices、minimum coverとdual
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next2-repair.json
    role: data
    note: 最新12-class repair。additiveとdistinct UNKNOWN s5 unionは各1,147
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
scope: Actions run 37334644565、37336924568、37337141197、37339663025の保存済み11×11 reply27 exact s5/s6結果、local completion81/next2有限計算、およびそれらを使うfinite frontier
evidence: 保存済みexact replayとlocal cold replayを統合し、canonicality・安全性・D4親子geometry・境界coverage・verdict衝突を監査。model-hard2の勝敗値自体はActions exact solverの保存結果として受け入れ、raw-only監査で境界と親への伝播を検査。next2 classの100 canonical s5全子がLOSSであることはclass境界verifierで検査
---

# 11×11 reply27の保存済みexact結果から復元したcache frontier

この項目は、失敗したActions runに保存されていたexact結果を再計算せず回収・監査・永続化した有限計算を記録する。別の作業時点で`origin/main`には同等のcache回収と正規化修正が到着していたため、ここではその時点で得た証跡と監査範囲を記録する。新しい探索結果の主張ではない。

## 保存結果と計算

基準run `37334644565` の初期snapshotはcanonical s5が2,529件（WIN 63、LOSS 2,466）。保存済みmodel8 cacheは追加でLOSSを8件増やし、shared s6 run `37336924568` は16件（WIN 10、LOSS 6、UNKNOWN 0）を含む。shared s6 metadataは66の親子relation、65の親候補を記録している。16キー中13キーがnoncanonicalだったため、各盤面の安全性、D4正規化、およびsafe s6から一点削除して得る親子relationを独立にgeometryから検証した。6つのLOSS s6結果から25件のs5 LOSS witnessを派生した。

失敗したcompletion86 run `37337141197` の保存CSVを監査し、86件すべてLOSS、合計361,568,619 nodesと確認した。基準cache、model8、shared s6派生分、completion86の結果を衝突なく統合した初期snapshotは2,648件（WIN 63、LOSS 2,585、conflict 0）。Actions run `37338193154` から独立に再構成されたcurrent cacheと全2,648行が一致した。s4 class `(1297036692816953344, 0)` のcanonical s5境界105件はすべてLOSSで、`verify_reply27_loss_class_cache.py` により検査した。

初期2,648-entry snapshotでs4 classはWIN 129、LOSS 18、UNKNOWN 3,237。root verticesは119個中72個がsecuredで47個がremaining。残りを覆う最小追加class数は13で、rational LP dualの値13と整数被覆の最適値13が一致した。初期13-class repairのUNKNOWN s5 unionは1,227件（加法目的値も1,227）。rank上位のtarget `(1298162592590594048, 0)` は101子の内訳が既知LOSS 12、UNKNOWN 89で、vertices 70、72、100、108をcoverした。

この候補のremaining 81 s5位置をlocal cold runで調べ、76 LOSS・5 UNKNOWN・0 WIN、paid nodes合計526,111,188を得た。残る5 UNKNOWNは続けてsolverに渡さず、生成済みの5親境界入力だけを保存した。

Actions run `37339663025` のmodel-hard2はcanonical s6境界169件をすべてWINと報告した。`verify_model_hard2_results.py --saved-raw-only` は独立に構成した境界とcanonical key・parent incidenceが一致すること（親の子数86と84）、全replayがsafe・canonical・legalであること、欠落・重複がないこと、両s5親が全子WINによりWINとなることを検査した。s5親はそれぞれ86/86、84/84がWINで、WIN判定値は保存されたActions exact solverの出力に基づく。この証拠でclass `(1298162592590594048, 0)` はWIN。

中間cacheは2,732件（WIN 65、LOSS 2,667、conflict 0）。当時のs4 classはLOSS 18、WIN 131、UNKNOWN 3,235、secured vertices 72/119、remaining 47で、最小追加class数13がrational LP dualと一致した。中間13-class repairのUNKNOWN s5 unionは1,237件。最初の2,648-entry snapshotにおける1,227 unionとは別の値である。

続くclass `(1297036693756510208, 0)` はcanonical s5境界100件を全てLOSSと判定した。既知LOSS 10件に、model8で選んだ8件（19,867,831 nodes）と残る82件（301,036,761 nodes）のexact LOSSを加えた。`verify_reply27_loss_class_cache.py` は幾何から100子の境界とcoverage vertices 56, 64, 90, 96を再構成し、全境界がLOSSであることを検査した。

最新cacheは2,822件（WIN 65、LOSS 2,757、conflict 0）。s4 classはLOSS 19、WIN 131、UNKNOWN 3,234、secured vertices 76/119、uncovered 43。最小追加class数は12でrational LP dual値12と整数被覆最適値12が一致する。12-class repairのadditive UNKNOWN s5数とdistinct unionはいずれも1,147。これは追加作業の対象範囲を表し、UNKNOWN classをLOSSと証明するものではない。次の探索順を選ぶrankingと再開手順は実験・引継ぎlogに保存する。

勝敗規約は、位置の真偽値が「先手固定視点で最終的に先手が勝つ」であり、偶数石OR・奇数石ANDである（[K0002](K0002-grundy-and-first-move-conventions.md)、`cpp/solvers/kyouen_dfpn_root.cpp`）。従って、ある初手の後のs4 LOSSが全119の第三手選択をcoverすれば、各s3 odd AND位置はLOSSとなり、s2 `{60,27}` のOR位置もLOSSとなる。これは後手が中央初手60に27で応じることで中央初手を破る方向の証拠であり、中央初手60の勝ちを示すものではない。空盤の勝敗は他の初手も検査しないと決まらない。

この時点では空盤面勝敗と`{60,27}` outcomeは未確定で、終端までのAND/OR証明は未完了。別のcold residual mex cross-checkは6件中3件（120、158、192秒）で停止し、production結果には採用していない。6件完了とは主張しない。6つのevidence-recovery regression testsと33 knowledge testsは成功済み。

再現CLI、保存入力、raw shard、receiptへのリンクは[実験README](../../experiments/n11-boundary-recovery-20261006/README.md)を参照。
