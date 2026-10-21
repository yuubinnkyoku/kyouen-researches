---
id: K0497
title: 事前選択した残余quota128・閾値6は新規26局面でOFFより20.8%速く、固定深い3局面でも数値採用条件を満たした
kind: computation
status: observed
topics: [residual-games, search-methods, verification, statistics]
aliases: []
relations:
- type: depends_on
  target: K0496
  note: 根全体で有限quotaを共有するP/N評価と枯渇時の通常探索復帰
- type: depends_on
  target: K0495
  note: 同じcompletion索引による残余構築を利用
- type: depends_on
  target: K0494
  note: 既存train26局面を再利用し、新規確認用26局面とは分離
artifacts:
- path: research/experiments/residual-quota-calibration-20261021/protocol.json
  role: manifest
  note: 測定前の固定seed・入力hash・binary hash・設定・予算・選択/確認規則
- path: research/experiments/residual-quota-calibration-20261021/fixtures.json
  role: data
  note: 既存調整26局面とD4非重複の新規26局面、独立期待値
- path: research/experiments/residual-quota-calibration-20261021/prepare.py
  role: verifier
  note: 新規局面の選択、独立幾何とsubset-mex、旧826局面とのD4非重複
- path: research/experiments/residual-quota-calibration-20261021/selection.json
  role: manifest
  note: 調整用データだけで選び、確認測定前にcommitした候補
- path: research/experiments/residual-quota-calibration-20261021/calibrate.py
  role: verifier
  note: 予算・quota・勝敗の検査、調整だけの選択とcommit前の確認起動拒否
- path: research/experiments/residual-quota-calibration-20261021/summary.json
  role: data
  note: 固定候補の新規確認と深い局面の結果、採用条件判定と選択commit
- path: research/experiments/residual-quota-calibration-20261021/comparison.md
  role: data
  note: 局面ごとの3反復中央値を合計した全比較表
- path: research/experiments/residual-quota-calibration-20261021/verify_outputs.py
  role: verifier
  note: 入力・独立期待値・全720根評価・候補選択・採用条件の再集計
- path: research/experiments/residual-quota-calibration-20261021/test_protocol.py
  role: verifier
  note: 確認データ混入拒否、UNKNOWN優先、中央値、採用条件など9テスト
- path: research/experiments/residual-quota-calibration-20261021/README.md
  role: log
  note: 事前プロトコル、再現手順、適用範囲と採用判断
---

## 事前固定と独立確認

K0494の調整用26局面だけでquota128/512/2048 × legal閾値6/12の6候補を調整した。
対照OFFと合わせ7設定を3反復し、候補の選択はUNKNOWN数、局面ごとの探索時間中央値の合計、
quota、閾値の辞書式最小とした。OFFは対照として別に保持し、候補間の選択には含めない。

確認用26局面はseed2026102107の512ランダム合法対局から、legal=6..18 × occupied parityの
各層をtrial順・対局の時間順の最初で選び、同一trialから1局面に制限した。
既存826局面とのD4重複を除き、別実装の行列式による合法点・極小残余辺族の検査と、
独立subset-mexの5150状態による勝敗照合を完了した。勝敗や時間による選別はしていない。

候補はquota128・閾値6。selection.jsonと調整結果を
ac421eddcae38667fb7fd7975b5a224f41ff68d8でcommitしてから新規確認の時間測定を開始した。
確認結果による候補の再選択はしていない。

## 観測結果

各根fresh solver/memo、共有cacheなし、外側5000 board nodes。3反復の局面ごとの中央値を合計。
時間は初期化を除く探索時間である。

| 対象 | OFF | quota128・閾値6 | UNKNOWN (OFF / 候補) |
|---|---:|---:|---:|
| 調整26局面 | 3.781 ms | 2.932 ms | 0 / 0 |
| 新規確認26局面 | 4.748 ms | 3.761 ms | 0 / 0 |
| 既存の深い3局面 | 30.432 ms | 29.900 ms | 3 / 3 |

新規確認では20.8%短縮し、既知の全勝敗は全設定・反復で期待値に一致した。
深い3局面では1.7%短い点推定だが、差は合計0.532 msと小さく、統計的な優位性は主張しない。
各根のPN呼出しは128で合計384。1根はhandoff内でquota切れUNKNOWNを返し、
他の2根も残量ゼロになった後は通常探索に戻る。新たな深い勝敗確定はなかった。

調整時の閾値6では3予算とも259 kernel calls・枯渇ゼロであり、同じ仕事量だった。
候補の名目上の最小時間から128を選んだが、この予算間の時間差には測定揺らぎも含まれる。
quota128が全入力で最適という結論ではない。

調整546、新規確認156、深い局面18の計720根評価を、入力hash、期待勝敗、board budget、
quota保存則、中央値、調整だけの候補選択まで再検査した。

## 採用条件と範囲

事前条件は、誤答ゼロ、UNKNOWN数が増えない、新規確認の探索時間がOFFより小さい、
深い3局面の探索時間がOFF以下、の全て。この固定比較では全条件を満たした。
bounded exact replayの明示指定として次を採用する。

```text
--residual-exact-legal=6 --residual-evaluator=outcome --residual-outcome-budget=128
```

通常探索の既定handoff OFFと既定Grundyは変更しない。今回の採用は固定局面・外側5000 nodesでの
明示設定に限る。quotaは各根全体のkernel呼出し数であり、board nodesやwall時間上限とは別枠。
1根あたり約0.5秒の初期化も別途必要。他の外側予算、通常df-pn探索全体、未検査の初期局面への
性能一般化や11×11空盤の解決を意味しない。
