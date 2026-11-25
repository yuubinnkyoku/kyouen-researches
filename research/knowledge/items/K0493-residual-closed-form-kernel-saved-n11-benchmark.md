---
id: K0493
title: 監査済み残余ゲームの構造別評価は保存済み11×11由来826局面で再帰呼出数を約21%削減
kind: computation
status: observed
topics: [residual-games, grundy, search-methods, verification, statistics]
aliases: []
relations:
- type: depends_on
  target: K0483
  note: 二禁止集合の全安全局面Grundy閉公式
- type: depends_on
  target: K0465
  note: ヒマワリ型禁止集合のGrundy閉公式
- type: depends_on
  target: K0460
  note: 道・閉路のGrundy再帰と成分xor
- type: depends_on
  target: K0344
  note: 既存の残余ゲーム圧縮との併用
artifacts:
- path: cpp/solvers/kyouen_residual_micro.hpp
  role: solver
  note: 構造認識・厳密評価と適用外の完全再帰
- path: cpp/solvers/kyouen_dfpn_root.cpp
  role: solver
  note: 既存残余ゲートへの統合と適用回数の記録
- path: cpp/tests/test_kyouen_residual_micro.cpp
  role: verifier
  note: 独立占有部分集合DP・通常/共有/構造別評価OFFとの全局面照合
- path: research/experiments/residual-closed-forms-20261021/README.md
  role: log
  note: 再現手順・比較条件・信頼境界
- path: research/experiments/residual-closed-forms-20261021/bench.cpp
  role: verifier
  note: rootごとにmemoを空にするOFF/ONの7回交互測定
- path: research/experiments/residual-closed-forms-20261021/run.py
  role: source
  note: 保存済み826残余状態の再ラベルと全件測定
- path: research/experiments/residual-closed-forms-20261021/benchmark.csv
  role: data
  note: 全826局面の一致値・呼出数・memo数・時間中央値
- path: research/experiments/residual-closed-forms-20261021/summary.json
  role: data
  note: 測定集計と入力SHA-256
- path: research/experiments/residual-closed-forms-20261021/integration.py
  role: verifier
  note: 16保存局面の独立Python mexとdf-pn4モードの勝敗照合
- path: research/experiments/residual-closed-forms-20261021/integration-summary.json
  role: data
  note: 旧版・新版・共有版・照合版の全確定勝敗と証明収集ガード
scope: 保存済み11×11由来826局面（合法点18以下）の残余Grundy評価と、選択16局面のdf-pn統合。標準11×11空盤の解決・一般の速度保証は対象外。
evidence: 独立占有集合DPによる107427安全局面の一致と2068小超グラフ回帰。保存済み826残余状態は構造別評価OFF/ONで全Grundy値が一致。時間はroot別7回中央値の合計による観測。
---

自由点、禁止集合が2本以下、ヒマワリ型、最大次数2の二点禁止グラフを認識し、監査済み定理に基づく厳密値を共有残余評価器へ追加した。適用外は既存の対称点圧縮・成分分割・完全mex再帰を使う。64点までの道は有限再帰で直接計算し、閉路と非干渉成分をxorする。

保存済み826状態をすべて再評価したところ、Grundy値は全件一致し、再帰呼出数は122720から96570（約21.3%減）、memo登録数は23646から14410（約39.1%減）。730状態で呼出数が減った。これは同じ保存コーパスに対する有限の比較結果であり、全局面での改善率ではない。

時間の観測値と機械条件はsummary.jsonに保存。kernel単体の時間とdf-pn全体の探索時間を区別する。新しい構造認識にはコストもあり、すべての局面で高速化するとは主張しない。

選択した16終盤局面は独立Pythonの直接mexと、旧版・新版・共有キャッシュ版・照合版の元先手固定視点の確定勝敗を比較する。深いS5 rootの予算内UNKNOWNと、この終盤検査の確定結果を混同しない。証明DAG収集と残余ショートカットの併用禁止は維持した。

標準11×11の空盤勝敗、最適な残余評価ゲート、大規模探索全体の高速化は未確定。
