---
id: K0499
title: 深いdf-pnの閾値6未発火は合法手数17以上で説明され、閾値18の独立確認でも根の新規確定はなかった
kind: computation
status: observed
topics: [residual-games, search-methods, verification, statistics]
aliases: []
relations:
- type: depends_on
  target: K0498
  note: 通常df-pnの残余handoffと共有work上限、以前の深い3局面
- type: depends_on
  target: K0496
  note: quota内の確定P/Nだけを採用し、UNKNOWNは通常探索へ戻す
artifacts:
- path: cpp/solvers/kyouen_dfpn_root.cpp
  role: solver
  note: residual-profile指定時だけの未解決stage-0合法手数分布とroot差分出力
- path: cpp/tests/test_kyouen_residual_dfpn.cpp
  role: verifier
  note: 既知両手番、解決済みTT除外、profile OFF、予算と例外後の回帰
- path: research/experiments/residual-gate-frontier-20261022/protocol.json
  role: manifest
  note: 閾値候補、事前固定6局面、入力とsource/binary hash、選択規則
- path: research/experiments/residual-gate-frontier-20261022/diagnostic.json
  role: data
  note: 旧3局面の10万work時の合法手数分布
- path: research/experiments/residual-gate-frontier-20261022/training.json
  role: data
  note: 旧3局面、8設定、各3反復の全72評価
- path: research/experiments/residual-gate-frontier-20261022/selection.json
  role: manifest
  note: 確認前にcommitした閾値18の選択とtraining hash
- path: research/experiments/residual-gate-frontier-20261022/confirmation.json
  role: data
  note: 新規6局面、3設定、2上限、各3反復の全108評価と選択commit
- path: research/experiments/residual-gate-frontier-20261022/late.json
  role: data
  note: 既知終盤26局面と3設定の全78正しさ検査
- path: research/experiments/residual-gate-frontier-20261022/study.py
  role: verifier
  note: 入力固定、選択順序、raw行、全組合せ、予算、独立幾何と再集計の検査
- path: research/experiments/residual-gate-frontier-20261022/test_study.py
  role: verifier
  note: 局面違い、新規勝敗、ヒストグラム範囲・重複・過大計数、時計混入、quota変更の拒否
- path: research/experiments/residual-gate-frontier-20261022/cli_profile.py
  role: verifier
  note: 同根を連続処理してprofileが次rootへ漏れないことを確認
- path: research/experiments/residual-gate-frontier-20261022/comparison.md
  role: data
  note: 固定比較全表、時間と探索量、適用限界
---

## 未発火の診断

K0498の深い3局面を残余OFF・10万workで各1回計測した。
未解決stage-0フレームの訪問は各50,002回で、合法手数の最小値は17・17・18、
最大値は93・86・95だった。閾値6で残余評価が発火しないことを直接説明する。
合法手数24以下の訪問は396・436・114回、48以下は24,470・28,442・20,009回だった。
再訪を含む計数であり、ユニーク局面数ではない。解決済みTTフレームは除外する。

この分布は明示的な`--residual-profile`指定時だけ記録する。
時間比較ではprofileをOFFにし、全行でbuild/structure/grundy時計が0であることも検査した。

## 事前固定した調整と確認

旧3局面を2万workで、OFFと閾値6/12/18/24/32/48/64、各3反復で比較した。
P/N quotaは全設定で各根128。通常workとは別枠である。
閾値12以上からUNKNOWN根数、局面ごとの探索時間中央値合計、閾値の順で選び、18を選択した。
全設定で根は3件ともUNKNOWN、work合計60,000、展開合計29,220と同一だった。
閾値18は2根でquota切れ、24以上は3根ともquota切れだった。
時間だけによる候補選択であり、探索量の改善を示すものではない。

確認用6局面はseed20261022で安全な5石配置を生成し、旧3局面とD4同値を除外した。
入力を調整前に、選択結果を確認前にcommitした。確認局面は独立の整数行列式で安全性と合法手数を再検査した。
各評価はfresh process/TT、native exact handoffなし、memo=18、wall guard30秒で行った。
以下は各局面の3反復中央値の合計で、初期化時間は含まない。

| 確認6局面のwork上限 | OFF | 閾値6 | 閾値18 | 根UNKNOWN |
|---|---:|---:|---:|---:|
| 20,000 | 1636.312 ms | 1564.214 ms | 1575.638 ms | 全設定6/6 |
| 100,000 | 6993.853 ms | 7141.079 ms | 7388.822 ms | 全設定6/6 |

2万workでは全設定120,000 work・58,782展開と同じだった。
閾値18は2根で発火し、どちらもquota切れだった。
10万workでは全設定600,000 work、展開はOFF/閾値6が287,643、閾値18が287,641だった。
閾値18は合計8回発火し、6根ともquotaを使い切った。少数の部分局面確定による2展開の差はあるが、
根の新規確定や実用的な探索量削減は確認できない。10万workでの時間はOFFより約5.6%長かった。
単一hostの観測であり、時間差を統計的な優劣とはしない。

## 検証と採用範囲

既知終盤26局面はOFF・閾値6・閾値18の全78評価で既知勝敗と一致した。
新しいholdoutとは呼ばず、各1反復なので速度の比較には使わない。
診断3、調整72、確認108、終盤78の全261評価で入力mask、手番、work計数、quota、
結果、profile有無、全組合せと再集計を検査した。watchdogは0件で、新しい深い勝敗確定はない。
通常・UBSanのC++回帰、CLIのroot差分、8件のプロトコル拒否テスト、既存の独立proof DAG回帰も通過した。

既定の残余評価はOFFを維持し、K0497/K0498の明示的なquota128・閾値6を置き換えない。
閾値を広げるだけで深い探索が改善するという根拠は得られなかった。
深い探索の次の検討では、初回の難しい残余局面にquota全量を費やす配分を見直す余地があるが、
その方式の効果は本比較では未検証である。
