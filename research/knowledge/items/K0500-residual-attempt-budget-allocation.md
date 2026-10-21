---
id: K0500
title: 根の残余予算128を1回32へ分配しても新規6局面の深い勝敗確定や実用的な探索量削減は確認できない
kind: computation
status: observed
topics: [residual-games, search-methods, verification, statistics]
aliases: []
relations:
- type: depends_on
  target: K0499
  note: 閾値18と、初回の難しい残余局面でroot quotaを使い切る観測
- type: depends_on
  target: K0496
  note: bounded P/Nの確定結果だけを採用し、UNKNOWNは通常探索へ戻す
artifacts:
- path: cpp/solvers/kyouen_dfpn_root.cpp
  role: solver
  note: 明示的な1回上限、root残量の実使用精算、canonical board再試行抑制、rootごとのreset
- path: cpp/tests/test_kyouen_residual_attempt.cpp
  role: verifier
  note: 予算・再試行・cache安全性と、独立幾何・部分集合DPによる全安全4×4局面照合
- path: research/experiments/residual-attempt-allocation-20261022/cli_test.py
  role: verifier
  note: 上限1/8/32/1000、quota0、同根再利用、既定互換性、不正modeの拒否
- path: research/experiments/residual-attempt-allocation-20261022/protocol.json
  role: manifest
  note: 事前固定の配分候補、新規6局面、入力とsource/binary hash、選択規則
- path: research/experiments/residual-attempt-allocation-20261022/training.json
  role: data
  note: 既存9局面、4設定、各3反復の全108評価
- path: research/experiments/residual-attempt-allocation-20261022/selection.json
  role: manifest
  note: 確認前にcommitした1回32ノードの選択とtraining hash
- path: research/experiments/residual-attempt-allocation-20261022/confirmation.json
  role: data
  note: 新規6局面、3設定、2上限、各3反復の全108評価
- path: research/experiments/residual-attempt-allocation-20261022/late.json
  role: data
  note: 既知終盤26局面と3設定の全78正しさ検査
- path: research/experiments/residual-attempt-allocation-20261022/study.py
  role: verifier
  note: 独立幾何、入力、全組合せ、raw行、root/attempt予算、選択順序と再集計
- path: research/experiments/residual-attempt-allocation-20261022/test_study.py
  role: verifier
  note: 誤局面、予算・試行計数・上限違反、時計混入、新規勝敗、選択順序の11テスト
- path: research/experiments/residual-attempt-allocation-20261022/comparison.md
  role: data
  note: 固定比較全表、P/N使用数、通常探索量、時間と限界
---

## 方式と正しさの境界

通常df-pnで以下を明示すると、1回の残余P/N評価へ渡す予算をroot残量と32の小さい方にする。

```text
--residual-exact-legal=18 --residual-evaluator=outcome
--residual-outcome-budget=128 --residual-attempt-budget=32
```

実際に使ったkernel node数だけroot残量から差し引く。
上限指定時は、同じroot中で同じD4-canonical boardを再試行しない。
この集合は通常df-pnと内部native exactで共有し、root開始時にquota・計数とともに消去する。
UNKNOWNは勝敗TTへ保存せず、通常探索を続ける。SG shadow crosscheckには適用しない。
対称な向きでも探索順は異なり得るので、再試行抑制は探索方針であり、有限予算の探索結果が同一という主張ではない。

capの省略は従来通りroot残量全体を使い、再試行抑制もしない。
CLIの明示0、負数、不正値、SG評価やstandalone exact replay等との組合せは拒否する。

独立した整数行列式で禁止4点集合を作り、占有部分集合の直接P/N DPを計算した。
4×4盤の全安全5,811局面を、fresh solver/TT、cap1とcap32で各1回、計11,622評価し、
元の手番に対応する固定先手勝敗が全て一致した。通常・UBSanの両方で確認した。
別途、root quota保存・reset、1回上限より小さい残量、両手番の確定、UNKNOWN後の通常証明、
native exactとの重複試行抑制、解決済みTT再利用時の計数resetも検査した。

## 事前固定した比較

K0499の深い9局面を調整用に再利用し、閾値18、root quota128、2万workを固定した。
OFF・従来方式・cap8・cap32を各3反復で比較し、候補8/32からUNKNOWN根数、
展開数中央値合計、探索時間中央値合計、capの順で最小化して32を選んだ。
全設定で9根UNKNOWN、通常180,000 work・88,002展開と同一だった。
P/N使用数は従来512、cap8が216、cap32が352で、発火した調整用の評価は全てUNKNOWNだった。
選択は展開数が同値のため時間によるものであり、探索量の改善を示さない。

確認用6局面はseed2026102202で調整前に生成した安全な5石配置で、調整用とのD4重複を除いた。
入力を調整前、選択を確認前にcommitした。各評価はfresh process/TT、native exactなし、
memo=18、wall guard30秒、profile OFF。以下は各局面の3反復中央値の合計で、初期化は含まない。

| 確認6局面のwork上限 | OFF | 従来128一括 | 1回32へ分配 | 根UNKNOWN |
|---|---:|---:|---:|---:|
| 20,000 | 1488.856 ms | 1518.065 ms | 1489.420 ms | 全設定6/6 |
| 100,000 | 7041.559 ms | 6984.226 ms | 6948.509 ms | 全設定6/6 |

2万workでの展開合計はOFFが58,750、従来58,748、分配58,749だった。
従来は5回発火してP/N384 nodes、分配は12回発火して同384 nodes。
10万workではOFFが287,550、従来287,551、分配287,549展開だった。
従来は9回発火してP/N768 nodes、分配は21回発火して672 nodes。
より多くの局面を評価でき、10万workでP/N使用数は従来より12.5%減ったが、
根の新規確定や実用的な通常探索量削減は確認できない。
時間は単一hostの観測であり、小さな差の統計的優劣は主張しない。
重複試行の抑制回数は今回の深い比較では全て0で、その機構による効果を確認した比較ではない。

## 監査と採用範囲

既知終盤26局面はOFF・従来方式・選択候補の全78評価で既知勝敗と一致した。
単一反復の回帰であり、新しいholdoutや速度の根拠として使わない。
調整108、確認108、終盤78の全294根評価について、入力mask・手番、通常work、
root quota、各回の最大使用数、試行数、UNKNOWN数、時計OFF、全組合せと再集計を検査した。
watchdogは0件で、新しい深い根の勝敗確定はない。
CLI回帰、11件のプロトコル検査、既存の独立proof DAG回帰も通過した。

明示指定できる実験的な配分機能として保持する。既定の残余評価OFFを維持し、
K0497/K0498の終盤向けquota128・閾値6の推奨設定を置き換えない。
今回の標本では閾値拡大と固定予算の分配だけによる深い探索の改善は確認できず、
追加の配分調整を有効策として採用する根拠はない。
