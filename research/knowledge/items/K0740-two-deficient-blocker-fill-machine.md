---
id: K0740
title: "two_deficient_pair_runner: 5×m・q=7 の2行欠損 occupancy クラスを完全列挙する機械"
kind: method
status: active
topics: [rectangles, variants, maximal-safe, verification]
aliases: []
relations:
- type: depends_on
  target: K0727
  note: blocker-obligation-fill DFS の2行欠損への一般化（census・伝播・葉fillは同一）
- type: depends_on
  target: K0726
  note: "blocker候補曲線census（5×19: 7点円8本・8点円87本）"
- type: supports
  target: K0332
  note: M_{5,7}=19 の確定に必要な複数行欠損クラスの否定キャンペーンの中核機械
- type: verifies
  target: K0302
  note: 全分岐版が5×18で第3 witnessを発見し独立検証で確認（石分岐の健全性の実証）
artifacts:
- path: research/experiments/five-row-q7-m19-20261110/scripts/two_deficient_pair_runner.ts
  role: source
  note: 機械本体。M/Y0/Y1/START/NODE_CAP を設定してスライス実行
- path: research/log/2026-11-11-five-row-multi-deficient-machine.md
  role: log
  note: 開発・制御・第3 witness・5×19 pair {0,1} 初スライスの記録
---

# two_deficient_pair_runner（2行欠損クラス完全列挙機械）

K0727 の blocker-obligation-fill DFS を、2行が ≤5 石・他行ちょうど6石の
occupancy クラス（欠損行ペア Y0,Y1）に一般化したハイブリッド機械:

- 外側ケース = 欠損行 Y0 の石列 S0 の鏡映代表（canonical 順。単一行キャンペーンと同一列挙）。
- 内側 = Y0 の空点への blocker 割当 + 欠損行 Y1 の各点の「石/空+blocker」分岐。
  葉で非欠損行をちょうど6石に fill する。
- 欠損行ペアは行鏡映で6代表: {0,1}≡{3,4}, {0,2}≡{2,4}, {1,2}≡{2,3},
  {0,3}≡{1,4}, {1,3}, {0,4}。

soundness/completeness: 欠損行の空点 p の blocker は p を含む危険曲線上の
ちょうど6石だが、p の行は ≤5 石で blocker になれず、他の行は p を含まない。
従って blocker は census 円に限り、blocker 割当の全列挙で完備する。
石/空の全分岐が欠損行の全点を決定する。行cap（欠損行5・他行6）・
円石数 ≤6・円飽和伝播・行飽和伝播は K0727 と同一。

検証済みの制御（詳細はlog）:
- **全分岐版の陽性対照**: 欠損行 Y0 の石も分岐する版（単一行欠損設定）が 5×18 で
  既知2個と鏡映非同値の**第3 witness（行0 {0,1,5,13,17}・29石・(5,6,6,6,6)）を発見**。
  全89曲線の独立censusで安全・全61空点blocker付きで極大（独立検証 PASS）。
- S0 事前決定なしの2行全分岐は爆発（600kノードで葉なし）→ ハイブリッド設計が必要。
- 5×18・pair {0,1}・S0={5,8,12,14,17}: 17,511ノード完走・witness 0。
- 5×19・pair {0,1} 初スライス: idx 0..117 全 witness 0、平均 ~5.1kノード/case
  （最大 28,488）。1ペアクラス ≈ 72スライス（600k）、6代表で計 ~430スライスの見込み。

限界:
- 本機械の監査は K0727 の 5×8 全候補照合（614,656候補 vs 759証人）ほど深くない。
  陽性対照（第3 witness の発見・独立検証）と S0 既知ケースでの単一完走は PASS。
  5×19 での witness 0 報告の確定前に、小盤での直接全列挙照合を推奨。
- witnesses は blocker 割当の異なる枝で同一配置を重複計上しうる（0件は「不存在」を意味する）。
- 複数行欠損の全ペアクラス完了前に M_{5,7} の値は確定しない。
