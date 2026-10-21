---
id: K0494
title: 固定52局面の残余切替閾値比較ではOFFが最速で、深い3局面のUNKNOWN数も改善しなかった
kind: computation
status: observed
topics: [residual-games, search-methods, verification, statistics]
aliases: []
relations:
- type: depends_on
  target: K0493
  note: 監査済み構造別残余評価器を用いた探索全体での閾値比較
artifacts:
- path: cpp/solvers/kyouen_dfpn_root.cpp
  role: solver
  note: 初期化と探索を分離するマイクロ秒計測、既存CSV列は維持
- path: research/experiments/residual-gate-calibration-20261021/README.md
  role: log
  note: 事前選択規則・結果・既定値維持の判断と適用限界
- path: research/experiments/residual-gate-calibration-20261021/protocol.json
  role: manifest
  note: 入力SHA-256・閾値・予算・反復数・選択規則
- path: research/experiments/residual-gate-calibration-20261021/fixtures.json
  role: data
  note: 調整用26と確認用26局面、独立subset-mexの期待値
- path: research/experiments/residual-gate-calibration-20261021/run.py
  role: verifier
  note: OFF/6/8/10/12の固定予算・3回反復比較と整合性検査
- path: research/experiments/residual-gate-calibration-20261021/measurements.csv
  role: data
  note: 全780測定の勝敗・ノード数・初期化/探索時間・残余計数
- path: research/experiments/residual-gate-calibration-20261021/summary.json
  role: data
  note: 調整用・確認用の時間中央値の和とUNKNOWN数
- path: research/experiments/residual-gate-calibration-20261021/stress.py
  role: verifier
  note: 既存の深いS5三局面を各5000ノードで補助比較
- path: research/experiments/residual-gate-calibration-20261021/stress-summary.json
  role: data
  note: 5閾値・3局面の予算内結果と探索時間、各1回
- path: research/experiments/residual-gate-calibration-20261021/verify_outputs.py
  role: verifier
  note: 入力hash・独立期待値・rawからの全再集計を検索再実行なしで検査
- path: research/experiments/residual-gate-calibration-20261021/test_protocol.py
  role: verifier
  note: 確認用からの情報混入と矛盾した測定の棄却に対する6回帰
- path: research/experiments/residual-gate-calibration-20261021/environment.json
  role: manifest
  note: コンパイラ・実装revision・バイナリとsourceのhash
scope: 保存済み11×11局面から合法手数6..18・手番偶奇別に選んだ52局面、予算5000、各設定3回、共有cacheなし。補助の既存S5三局面は同予算で各1回。全盤・全予算の最適設定は主張しない。
evidence: 調整用26と異なるtrialの確認用26を測定前に固定。独立占有部分集合mexの計8301状態を再計算し期待勝敗を保存。全780測定で確定勝敗が一致、UNKNOWNは0。設定選択は調整用だけで行いOFFを選択、確認用でもOFFが最速。深い3局面は全閾値でUNKNOWN。
---

残余評価へ切り替える合法手数の閾値をOFF（0）・6・8・10・12で比較した。局面ごとにsolverとmemoを新規作成し、共有cacheは使わず、各rootの予算を5000に固定した。3反復の実行順をずらし、root別時間中央値の和で比較した。

| 閾値 | 調整用26局面の探索時間合計 ms | 確認用26局面の探索時間合計 ms | 全52局面の探索ノード数 | UNKNOWN |
|---|---:|---:|---:|---:|
| OFF | 3.403 | 3.483 | 1097 | 0 |
| 6 | 18.245 | 19.990 | 153 | 0 |
| 8 | 13.887 | 20.088 | 82 | 0 |
| 10 | 10.143 | 15.354 | 38 | 0 |
| 12 | 10.210 | 14.658 | 26 | 0 |

ノード数は減っても、この標本では切替によって探索時間が増えた。調整用のみで選ぶ事前規則はOFFを選び、確認用でも同じ結論になった。現在の既定値 `residual_exact_legal=0` を維持し、6〜12への引上げは行わない。

別途、既存CIとK0493の深いS5三局面を各5000ノードで再評価した。全閾値で3局面ともUNKNOWN、実行ノード数は合計15000だった。探索時間の合計はOFF約0.029秒に対し、6/8/10/12で約2.469/3.815/5.806/8.212秒。ただし各1回の補助測定であり、精密な速度比や将来の証明到達率は主張しない。

探索時間には盤面側の処理、残余集合の構築、構造認識、Grundy評価が含まれる。初期化時間は別記録した。52局面の初期化合計は約27秒で、行全体の時間では初期化の揺らぎが支配的なため、数msの探索差を行全体の確実な速度差とは扱わない。

残余側の再帰作業は親探索のノード予算に含まれず、Grundy値全体を求める一方、通常探索は勝敗を短絡して判定できる。従って同じ親ノード予算・少ない親ノード数を、同じ計算量や高速化と読み替えない。残余構築とGrundy評価のどちらが支配的かの時間分解はまだ行っていない。

K0493の評価器単体の改善と矛盾しない。今回の結果は、この固定標本・実装・予算での切替費用を含む観測である。標準11×11空盤の勝敗や、すべての局面に最適な閾値は未確定。
