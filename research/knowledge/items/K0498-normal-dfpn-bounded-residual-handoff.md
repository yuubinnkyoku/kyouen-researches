---
id: K0498
title: 通常df-pnの固定終盤26局面で残余quota128・閾値6は約51–52%短縮し、深い3局面では未発火だった
kind: computation
status: observed
topics: [residual-games, search-methods, verification, statistics]
aliases: []
relations:
- type: depends_on
  target: K0497
  note: 事前選択したquota128・閾値6と固定した26+3局面を再調整せず使用
- type: depends_on
  target: K0496
  note: 有限P/N評価、確定結果だけのmemo、quota切れUNKNOWN時の通常探索復帰
artifacts:
- path: cpp/solvers/kyouen_dfpn_root.cpp
  role: solver
  note: 通常df-pnの直接残余handoff、root quota reset、共有work node上限とroot計数
- path: cpp/tests/test_kyouen_residual_dfpn.cpp
  role: verifier
  note: 両手番、直接handoff、quota reset/切れ、cache安全性、0上限、exact handoffとの合計上限
- path: research/experiments/residual-dfpn-integration-20261021/integration.py
  role: verifier
  note: 通常CLI、独立4×4幾何と終盤期待値、既定OFF、TT再利用、不正budget/mode拒否
- path: research/experiments/residual-dfpn-integration-20261021/protocol.json
  role: manifest
  note: 固定入力・source/binary hash、2万/10万上限、設定、反復、watchdog規則
- path: research/experiments/residual-dfpn-integration-20261021/records.json
  role: data
  note: 全348根評価の入力ID、結果、node計数、残余使用数、探索/process時間
- path: research/experiments/residual-dfpn-integration-20261021/comparison.md
  role: data
  note: 3反復の局面ごとの中央値合計と全比較表
- path: research/experiments/residual-dfpn-integration-20261021/verify_outputs.py
  role: verifier
  note: 固定入力・source provenance、全raw行の占有mask・勝敗・node/quotaと再集計
- path: research/experiments/residual-dfpn-integration-20261021/test_protocol.py
  role: verifier
  note: 局面違い、誤答、重複、予算超過、quota変更、時計混入、新規深い勝敗を拒否する8テスト
- path: research/experiments/residual-dfpn-integration-20261021/README.md
  role: log
  note: node定義、事前プロトコル、CLI、回帰、結果と適用限界
---

## 実装と境界

通常df-pnのフレーム初回処理時に、expandより前に残余評価を直接適用する。
`--exact-legal`を有効にしなくても以下を明示指定して使える。

```text
--residual-exact-legal=6 --residual-evaluator=outcome --residual-outcome-budget=128
```

各通常探索rootの開始時にquotaとPN計数をリセットする。確定した固定先手勝敗だけをPnTTに置き、
UNKNOWNなら通常expandへ戻る。残量0以降はそのrootでP/Nを再試行しない。
既存exact handoffの内部でも同じrootのquotaを共有する。

通常探索用の`--node-budget=N`を追加した。work nodeはdf-pnスタック処理の1反復、または
内部exact探索の1 board nodeを各1として合計する。PN kernel呼出しは別枠であり、expansion数とも異なる。
既定はnode上限なし、明示0はworkを許可しない。exact replay/quant等での混用は拒否する。
例外でも通常探索の予算scopeを終了させ、後の独立exact replayへ上限を漏らさない。

通常/UBSanで、両手番の直接handoff、quotaのrootごとのreset、部分UNKNOWN後の通常証明、
確定cache汚染の防止、0 node上限、既存exact handoffとの合計上限を検査した。
合計上限7ではdf-pn反復1とexact board nodes6で停止した。
CLIでも既定OFF、既知4×4空盤の後手勝ち、低quota、同rootのTT再利用、独立幾何からの
両手番終盤期待値、不正なnode budget/modeを確認した。既存exact replay/proof DAG回帰も通過。

## 固定比較

K0497の既知26局面と以前からの深い3局面を使い、今回新しいholdoutとは呼ばない。
quota128・閾値6を再調整せず、各根fresh process/solver/TT、共有cacheなし、各3反復で比較した。
以下は局面ごとの探索時間中央値の合計で、初期化を含まない。

| 対象 | work node上限 | OFF | 明示ON | UNKNOWN (OFF / ON) |
|---|---:|---:|---:|---:|
| 終盤26局面 | 20,000 | 14.171 ms | 6.925 ms | 0 / 0 |
| 終盤26局面 | 100,000 | 14.038 ms | 6.718 ms | 0 / 0 |
| 深い3局面 | 20,000 | 664.375 ms | 687.183 ms | 3 / 3 |
| 深い3局面 | 100,000 | 2929.270 ms | 3095.168 ms | 3 / 3 |

終盤は51.1% / 52.1%短縮し、work nodesは両上限とも4458→1262、expansionsは1805→243。
PN呼出し合計は462、handoff内のUNKNOWN返却は0で、全既知局面の勝敗が全設定・反復で一致した。

深い3局面の残余呼出しは両上限とも0、PN quota128も未使用だった。
そのため、深い探索で残余評価の効果やquota切れの性能を確認したことにはならない。
通常df-pnで切替が発火しない範囲では、観測された探索時間はONが3.4% / 5.7%長かった。
訪問数・expansion数も同一であり、この差をkernel計算の費用とは呼ばない。
条件確認の費用と測定揺らぎを含む単一hostの観測で、統計的な優劣は主張しない。

29×2設定×2上限×3反復の348根評価で、全行のwork nodes = df-pn反復 + exact board nodes、
上限、占有mask、期待勝敗、PN quota使用数/残量、時計OFFを検査した。
今回の比較ではexact handoffは無効なのでexact board nodesは全て0。
watchdog打ち切りは0で、深いUNKNOWNは全て指定node上限まで進んだ。新しい深い勝敗確定はない。

## 採用範囲

通常探索から明示指定できる実験的機能として接続した。今回の終盤コーパスでは効果を確認したが、
深いrootの改善は確認できず、既定residual gateはOFFを維持する。
1根あたり約0.5秒の初期化は別途必要で、起動からのwall時間の短縮率ではない。
以前のexact replayのboard node予算と今回のwork node上限は異なる指標なので直接比較しない。
未検査の初期局面での性能や11×11空盤の解決を意味しない。CIでは小さい回帰と保存資料の再検査だけを実行する。
