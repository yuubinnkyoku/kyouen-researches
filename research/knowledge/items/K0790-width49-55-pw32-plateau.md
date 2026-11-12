---
id: K0790
title: "幅49..55の円点数の完全決定 P(49)=…=P(55)=32 — 32点プラトーがw=55まで平らに継続 — P(w)は全幅6..55で決定済み・level 17の復活点は(55,83]に特定"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "幅w固定・長さm可変（全m≧1）の標準整数格子の円の格子点数: P(49)=P(50)=…=P(55)=32（全称・等号付き）。帰結としてP(w)はw=6..55の全幅で決定済み（K0778/K0782/K0784/K0788/K0789との合体）。w=56+はopen（P∈[32, 2⌈w/2⌉−4]）・level 17の復活点は(55,83]（K0785のP(83)≧34による）"
evidence: "数学的証明（K0784/K0788 と同一構造・streaming bitset DFS・第三実装系）。各w=49..55でlevel 17（17点行集合）が窓マスク完備列挙のもと全滅（ノード 368,728/529,364/739,255/1,057,876/1,437,558/1,915,406/2,644,771・leaves=0）⟹ d+s≦16 ⟹ P≦32。g0≧2形はconvention B classMax（g2 uodd 7..8・g3 11・g4+ 類サイズ≦14）全て<17。下界: 2210円の全32点（v-span 94≦2(w−1), w≧49）→P≧32。制御: 2210 witnessのper-w点数26/28/28/30/30/32（w=43..48）はK0786記録と完全一致・g0会計の数値はK0788のw=36..48記録と単調接続・streaming機はK0788の制御済み実装と同一"
solution:
  board: 幅w固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: P(49)..P(55)=32 は全称・全 m≧1・全安全局面
  conditions: 連続整数行
  verification: [mathematical-proof]
  certificate: 窓マスク完備候補生成（mod 9×11）+ 16法bit-set DFS level 17 全滅 + g0≧2 convention-B classMax 会計 + 2210 witness 下界
  independent_check: 2210 per-w 再計数が K0786 と一致・ノード数の単調成長則（×1.36/w）・g0 会計値の K0788 からの連続性
  note: "32プラトーはw=43..48の漸増帯（K0788）の後、w=49から平らになる。level 17の復活点は(55,83]に絞り込まれた（K0785のP(83)≧34）。11050円は本幅では16..20点で疎ら"
relations:
- type: depends_on
  target: K0788
  note: streaming level 分類機・convention B g0 会計・2210 witness の直接拡張。w=43..48 の跳躍帯に続き 32 を平らに延長
- type: depends_on
  target: K0784
  note: level 全滅原理・窓マスク候補生成・意味論
- type: supports
  target: K0785
  note: P(83)≧34 により level 17 復活点を (55,83] に特定。w=49..55 では 11050 円族は脅威にならない（16..20点）
artifacts:
- path: research/experiments/width49-55-level-classification-20261113/scripts/width49_55_level_classify.ts
  role: verifier
  note: streaming 分類・g0 会計・2210 witness の単独再現（決定的・TARGETS 分割実行・依存なし）
- path: research/experiments/width49-55-level-classification-20261113/output/width49_55_level_classify.json
  role: data
  note: 全数値の機械出力（nodes・g0 会計・witness per-w）
- path: research/experiments/width49-55-level-classification-20261113/reports/width49-55-level-classification.md
  role: proof
  note: 定理・証明骨子・制御・ノード成長則・限界
- path: research/log/2026-11-13-width49-55-level-classification.md
  role: log
  note: 判断・教訓・レジューム
---

## 命題（証明済み・全称・等号付き）

1. **P(49) = P(50) = … = P(55) = 32**（幅 w の連続整数行・全 m ≥ 1・標準整数格子）。
   - 上界: level 17 全滅（streaming・ノード数 368,728..2,644,771・leaves=0）
     ⟹ d+s ≤ 16 ⟹ P ≤ 32。g0 ≥ 2 形は convention B classMax
     （g2 uodd 7..8・g3 11・g4+ ≤ 14）全て < 17。
   - 下界: 2210 円の全 32 点（v-span 94 ≤ 2(w−1)・w ≥ 49）。
2. **帰結**: **P(w) は全幅 w = 6..55 で決定済み**
   （16 プラトー 12..21（K0778/K0789）・18..24 の跳躍 22..25（K0784）・
   24 プラトー 26..42（K0784/K0788）・漸増 43..48（K0788）・32 プラトー 49..55）。
3. **level 17 の復活点は (55, 83] に特定**: K0785 の P(83) ≥ 34 は
   d+s ≥ 17 を与え、level 17 が w=83 で生きていることを含意。
   w=56..82 の二分探索は各 ~10⁸ ノードで長期レーン対象
   （K0789 の素数冪拡張法を窓マスク掃引に入れると枝刈りが強まる可能性）。

## 制御

- 2210 witness の per-w 点数は K0786 の 26/28/28/30/30/32 と完全一致。
- g0 会計の数値（g2 7..8・g3 11）は K0788 の w=36..48 の記録に単調接続。
- streaming 機は K0788 の制御済み実装（w=26 L=12 S* 1 生残ほか）と同一。

## 構造的観察

- ノード数は ×1.36/w で成長（49→55 で 7.2 倍）。全滅のまま伸びる限り
  プラトーが延びる。復活点の予測には witness 側の探索（34 点円族の
  最小行スパン）が鍵。
- 11050 円（r₂ = 48・v-span 420）は w=49..83 で 16..20 点しか収まらない。
  K0785 の P(83) ≥ 34 の witness は別円族（要確認）。

## 限界

- 標準整数格子限定。任意間隔平行行には主張しない。
- w=56+ は open（P ∈ [32, 2⌈w/2⌉−4]）。P(56)..P(82) の決定と
  復活点の特定が次の課題。
