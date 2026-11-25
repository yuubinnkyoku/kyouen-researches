---
id: K0496
title: 予算付きP/N残余探索は固定826局面で独立oracleと一致しkernel呼出しを84%削減した
kind: computation
status: observed
topics: [residual-games, search-methods, verification, statistics]
aliases: []
relations:
- type: depends_on
  target: K0493
  note: 閉形式とSG保存圧縮を再利用し、通常手番のP/Nを求める
- type: depends_on
  target: K0495
  note: completion索引を使う同じ残余構築と固定52+3局面で比較
artifacts:
- path: cpp/solvers/kyouen_residual_micro.hpp
  role: solver
  note: 完全な局面上の短絡P/N再帰、有限quota、専用memoとUNKNOWN
- path: cpp/solvers/kyouen_dfpn_root.cpp
  role: solver
  note: 根全体で共有するP/N quotaと枯渇時の通常探索への復帰
- path: cpp/tests/test_kyouen_residual_micro.cpp
  role: verifier
  note: 独立subset oracle 107427状態、2068小clutter、低予算と部分memo再利用
- path: cpp/tests/test_kyouen_residual_outcome.cpp
  role: verifier
  note: UNKNOWNの盤面cache汚染防止、quota reset、native fallbackと確定TT再利用
- path: research/experiments/residual-outcome-search-20261021/README.md
  role: log
  note: 事前プロトコル、正しさと予算の境界、再現手順、適用範囲
- path: research/experiments/residual-outcome-search-20261021/oracle.json
  role: certificate
  note: 保存826局面を別実装subset-mexの70347状態で検査した期待値
- path: research/experiments/residual-outcome-search-20261021/budget-audit.json
  role: certificate
  note: 9種類の有限予算と部分memo再利用で確定値の一致を検査
- path: research/experiments/residual-outcome-search-20261021/comparison.md
  role: data
  note: kernelの7反復、盤面5設定の3反復、初期化を除く中央値合計
- path: research/experiments/residual-outcome-search-20261021/protocol.json
  role: manifest
  note: 入力とsolverのSHA-256、実装commit、設定・quota・反復・順序
- path: research/experiments/residual-outcome-search-20261021/integration.py
  role: verifier
  note: 低quota復帰、独立proof DAG検査、UNKNOWNと不正併用の拒否
- path: research/experiments/residual-outcome-search-20261021/verify_outputs.py
  role: verifier
  note: 独立oracle再計算、各保存行の勝敗・予算・quota検査と再集計
---

## 対象と結果

P/Nは通常手番に対する勝敗とする。局面全体を再帰し、Pの子が見つかればNとして打ち切る。
既存の閉形式とSG保存圧縮は利用するが、成分のP/Nをboolean xorする操作はしない。
SG memoとは別のP/N memoに確定値だけを格納する。各呼出しはmemo/閉形式hitを含めて
1 quotaを消費し、枯渇ならUNKNOWN。元の先手に対する勝敗には圧縮前のstone数を用いる。

保存済み11×11残余826局面について、別実装subset-mex oracleの70,347状態から
期待値を再計算し、P/Nの確定値が全て一致した。fresh memo、順序を交互にした7反復で、
局面ごとの中央値合計は次の通り（単一hostの観測）。

| 指標 | 完全SG | P/N |
|---|---:|---:|
| kernel呼出し | 96,570 | 15,210 |
| memo件数 | 14,410 | 4,764 |
| kernel時間 | 152.022 ms | 25.121 ms |

呼出しは84.2%、kernel時間は83.5%削減した。533/826局面で時間が短くなった。
全ての局面で速くなるという主張ではない。

## 予算とcacheの有限検査

独立subset oracleの107,427安全状態と2,068小clutterで通常SGとの一致を確認した。
予算0/1/2、閉形式無効、部分memo再利用、64ビット境界も検査し、通常/UBSan buildで完了。

保存826局面でも0/1/2/8/32/128/512/2048/100000呼出しをfresh memoで検査した。
全ての確定値が独立期待値と一致し、部分memoを再利用した再試行でも全826局面が正しく確定。
512呼出しでこの残余826局面は全て解けた。ただし盤面rootでは複数handoffが発生するため、
盤面root全体で512が十分であるとは意味しない。

盤面側では1 replay root全体でP/N quotaを共有し、枯渇後は通常探索へ復帰する。
予算切れのrootを同じsolverで再試行すると、確定TTに汚染されず通常探索と同じ154 nodesで
4×4空盤の後手勝ちを再現した。quotaの根ごとのresetと、本当に確定したTTの再利用も確認。
quota0/1/2/10/100000のCLI、shadow照合、独立DAG検査、禁止併用の拒否も検査した。

## 盤面探索全体の固定比較

K0495と同じ既知52局面と深い3局面、各根5000 board nodes、P/N quota100000、
共有cacheなし、fresh solver、5設定を3反復した。計825根評価で52局面は全て独立期待値と一致、
深い3局面は全設定・全反復UNKNOWNだった。値は局面ごとの探索時間中央値の合計。

| 対象 | OFF | SG6 | PN6 | SG12 | PN12 |
|---|---:|---:|---:|---:|---:|
| 既知52局面 | 7.336 ms | 6.426 ms | 6.476 ms | 9.615 ms | 7.361 ms |
| 深い3局面 | 26.769 ms | 97.899 ms | 87.840 ms | 3500.310 ms | 524.817 ms |

既知52局面のPN12はSG12より23.4%短い。PN6とSG6はほぼ同程度。
深い3局面のPN12では各根でquotaを使い切り通常探索へ復帰したため、SG12との85.0%の時間差を
短絡P/N再帰だけの効果と解釈しない。PN6にはquota枯渇がなく、SG6より10.3%短かったが、
OFFの約3.3倍かかる。UNKNOWN数は改善しなかった。

## 採用範囲と限界

`--residual-evaluator=outcome --residual-outcome-budget=N` の実験的選択肢として提供する。
既定evaluatorはGrundy、既定handoffはOFFを維持する。SG成分共有cacheとは併用せず、
証明書captureと残余shortcutの併用禁止も維持する。shadowの追加SG検査はP/N quotaの対象外。

quotaはkernel呼出しの回数上限でありwall時間上限ではない。外側board budgetとは別枠。
各根約0.5秒の初期化を探索時間から除いているため、起動からのwall時間の削減率ではない。
比較は固定コーパス・単一hostの観測であり、未解決盤全体での性能や11×11空盤の解決を意味しない。
