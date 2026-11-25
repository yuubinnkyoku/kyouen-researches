# 単一オーナー宣言: 六行band surgery レーン（(6,5) 6×31・(6,6) 6×25・(6,7) 6×22、機会 am: (5,4) 6×41）— 2026-11-21 高速レーン

- 宣言時刻: 2026-11-21T18:4xZ（push前に最終HEAD再取得のうえ、HEAD `b1a38144` に対して本宣言を push する）
- オーナー: 本高速レーン実行（自実行セッション）。対象は下記の固定幅 witness band 延伸のみで、
  他レーンの claims（n11 S5 probe 各class・fourthcost/fifth-cost・K1058 inversive/arc系・s12/s13）には一切触れない。
- branch / PR は作らず main に直接反映する（AGENTS.md 規約）。

## 目的

短時間〜中時間で厳密な新結果を増やす。現行の (w,q) band 上端（真のfrontier）について、
下界を 1 幅ずつでも伸ばす witness を、采用済みの bounded-edit surgery 手法
（K1209 five-row-q4 m40 レーンと同一の機械的手続きの (w,q) 一般化）で探索する。

## 現状の前線（着手時点での私はこの読みで作業する）

- **(6,5)**: CSV/K0815 により witness band は 6×30 まで実在（下界 31）。真のfrontier = **6×31**。
  なお K1209 の「true frontier m=29」は s6x28q5_rowY0 という古い seed に対する per-seed 記述で、
  K0815 の 6×29/6×30 witness（宣言より前から公刊）と比べて band 上端が古い。本レーンで正規の手続きとして
  6×31 を攻める（seed は 6×30 の 3 同型類: `extend6-deep-removal-20261114/output/w65_30.json` ×2 +
  `encoding-symmetry-kissat-20261114/output/L2_c630_def.json`）。
- **(6,6)**: CSV 下界 24（6×23 witness ×8+9）。ただし K1209 レーンの R(S) census が
  `witnesses/s6x24q6.json`（6×23 witness の +1 シフト配置、29石、rows [5,4,5,5,5,5]) の
  `witness_widths=[24,24]` を既に公刊しており、6×24 witness が実在することから有効下界は 25。
  本レーンは (i) 8+1 個の 6×23 配置について埋め込みオフセット全数census（両側strip被覆）を行い
  6×24 を witness とする配置を全数特定、(ii) 真のfrontier **6×25** を surgery で攻める。
  種 seed = census で 6×24 witness と認定された配置（最低1件は公刊済み）。
- **(6,7)**: 下界 22（6×21 witness、`six-row-q7-m21-class-split-20261114/output/w67_21.json`）。
  真のfrontier = **6×22**（kissat class {2} 単発 5.04M conflicts INDET のみ、非不在）。
- **(5,4)（機会）**: K1209 の 16 個の幅40 witness から **6×41** を surgery。
- n11 標準盤・二石root・S2・class 1/2/4 は本レーン非接触。

## 手法

1. **R(S)・全埋め込みcensus（完全列挙）**: seed 配置の x-offset 全パターン（幅の広い盤に収まる全置き方）の
   both-edge strip 被覆を `append_criterion.py`（Fraction、公刊のまま流用）で判定し、
   「新石ゼロで target 幅の witness になる置き方」があれば即 下界更新。
2. **bounded-edit surgery**: 手順1が陰性の 場合のみ。`surgery_gen.js`
   （公刊 `surgery.js` の曲線エンジン verbatim 流用・(w,q,m) と base リストを一般化・1 call = 1 foreground process・
   base ごとの checkpoint で再開可能）で D4 像 × edit 予算 {single-move, rem2add1, rem2add2} の決定的全列挙。
   石数保存: 全 target で seed は w(q−1)−1 石であり witness も ≤ w(q−1)−1 石から純増加は不可能。

## 受入条件

1. **検証**: census による下界更新・surgery による新 witness のいずれも、
   ≥2（本レーンでは3系統）の独立整数実装で safe + maximal + 行欠損 を検証してから出版する:
   (a) surgery benchmark の発見時全盤面検証（整数曲線census）・(b) `append_criterion.py`（Fraction）・
   (c) 新規 `det_q_verify.py`（一般q の determinant 零判定のみ・曲線方程式非形成）。
   負対照（石移動 tamper で rc=1 拒否）と正対照（既知 seed の再検証・q=4 での m40 witness）を含める。
2. **主張の範囲**: 下界のみの値更新。上界（K0318 代入の U 値）は一切不変。
   census は置き方全体に対する完全列挙として主張するが、surgery の陰性は
   「bounded-edit 近傍（≤2 removals / ≤2 additions of the seed の D4 像）における非発見」の限定非不在のみで、
   target 幅の witness 不在は主張しない。checked 数・候補数・実行秒数を勝敗として読まない。
3. **mwq_stabilization.csv は更新しない**（K1201/K1209 前例。下界更新は K item + bullet に記録）。
4. **競合運用**: 各 push の前に必ず最新 main を再取得し、衝突・同時書き込み・取得失敗が起きたら
   無理に押し進めず記録して本レーンを中断する（次回実行に回す）。
5. n11 の行・root・UNKNOWN 状態は一切読み書きしない。REFUTED-D10 は LOSS 証明ではない。

出版物: `research/experiments/six-row-band-surgery-20261121/`（scripts + witnesses + output + README）、
K item（新規採番は push 直前の3点確認）、knowledge README bullet 1行、session log。
