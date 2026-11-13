---
id: K0792
title: "幅56・57・58の円点数の完全決定 P(56)=P(57)=P(58)=32 — 32点プラトーがw=58まで継続 — P(w)は全幅6..58で決定済み・level 17の復活点は(58,83]に狭窄・g4会計はw=65で飽和"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "幅w固定・長さm可変（全m≧1）の標準整数格子の円の格子点数: P(56)=P(57)=P(58)=32（全称・等号付き）。帰結としてP(w)はw=6..58の全幅で決定済み。level 17の復活点は(58,83]（K0785のP(83)≧34）。P(59)..P(82)はopen（P∈[32, 2⌈w/2⌉−4]）。g0会計のg4類サイズ引数はw≦64で有効・w=65で飽和"
evidence: "数学的証明（K0790 streaming機の直接拡張・maximal mask列の分割実行）。w=56: 2,752 mask・7チャンク・ノード計3,714,156。w=57: 2,880 mask・12チャンク・ノード計5,045,586。w=58: 2,997 mask・11チャンク（2チャンクはノード上限で分割）・ノード計6,951,209。いずれもleaves=0・生残0でlevel 17 全滅 ⟹ d+s≦16 ⟹ P≦32。g0≧2形はconvention B classMax（g2 uodd 8・g3 11..12・g4+ 類サイズ14/15・全て<17）。下界: 2210円の全32点（v-span 94≦2(w−1), w≧49）。K0789の素数冪法49/121/343はリーフ証明書として装備したが不発。制御: w=26 L=12 S* ちょうど1生残（K0782/K0784/K0788/K0790一致）・2210 witnessはw=49..67で全32点・ノード成長×1.36..1.38/w（K0790則どおり）"
solution:
  board: 幅w固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: P(56)=P(57)=P(58)=32 は全称・全 m≧1・全安全局面
  conditions: 連続整数行
  verification: [mathematical-proof]
  certificate: 窓マスク完備候補生成（mod 9×11）+ 16法bit-set DFS level 17 全滅（maximal mask 分割実行）+ 素数冪リーフ証明書（不発）+ g0≧2 convention-B classMax 会計 + 2210 witness 下界
  independent_check: S* 制御・2210 per-w 再計数・ノード成長則（×1.36..1.38/w・w57→58で5.05M→6.95M）・g0会計値のK0788/K0790からの連続性
  note: "w=57の重い帯はmask 700..950に局在・w=58では700..920に加えて中間帯1050..2500も重い（チャンク分割はノード上限ベースで冪等）。インライン素数冪法はper-nodeコスト×12で逆効果（負の観測）・リーフ証明書が適切。g4類サイズ引数はw=65で⌈65/4⌉=17=Lに飽和し、w≧65にはg4形のclassMax精密化が必要"
relations:
- type: depends_on
  target: K0790
  note: streaming 分類機・意味論・2210 witness の直接拡張。32 プラトーを w=55 から w=58 へ延長
- type: depends_on
  target: K0789
  note: 素数冪法（49/121/343）をリーフ証明書として統合。w=56..58 では不発だが w 増大時の保険
- type: supports
  target: K0785
  note: level 17 復活点を (55,83] から (58,83] に狭窄
artifacts:
- path: research/experiments/width56-level-classification-20261113/scripts/width56_level_classify.ts
  role: verifier
  note: 分割実行対応 streaming 分類機（決定的・依存なし・素数冪リーフ証明書装備）
- path: research/experiments/width56-level-classification-20261113/output/width56_level_classify.json
  role: data
  note: 全数値の機械出力（chunks・g0 会計・witness・w56/w57/w58 完走）
- path: research/experiments/width56-level-classification-20261113/reports/width56-level-classification.md
  role: proof
  note: 定理・証明骨子・制御・g4 飽和・限界
- path: research/log/2026-11-13-width56-level-classification.md
  role: log
  note: 判断・教訓・レジューム
---

## 命題（証明済み・全称・等号付き）

1. **P(56) = P(57) = P(58) = 32**（幅 w の連続整数行・全 m ≥ 1・標準整数格子）。
   - 上界: level 17 全滅（w=56: maximal mask 2,752・ノード計 3,714,156・
     w=57: 2,880・5,045,586・w=58: 2,997・6,951,209・いずれも leaves=0）⟹ d+s ≤ 16 ⟹ P ≤ 32。
     g0 ≥ 2 形は convention B classMax（g2 uodd 8・g3 11..12・g4+ 14/15）全て < 17。
   - 下界: 2210 円の全 32 点（v-span 94 ≤ 2(w−1)）。
2. **帰結**: **P(w) は全幅 w = 6..58 で決定済み**
   （16 プラトー 12..21・跳躍 22..25・24 プラトー 26..42・漸増 43..48・32 プラトー 49..58）。
3. **level 17 の復活点は (58, 83] に狭窄**（K0785 の P(83) ≥ 34 と合わせ）。

## 制御

- w=26 L=12 は S* ちょうど 1 生残（K0782/K0784/K0788/K0790 と完全一致）。
- 2210 witness は w=49..67 で全 32 点。
- ノード成長 ×1.36..1.38/w（3,714,156 → 5,045,586 → 6,951,209・K0790 則どおり）。

## 構造的観察

- **g4 会計の飽和**: g4 類サイズ引数（⌈w/4⌉ < 17）は w ≤ 64 で有効。
  w=65 で 17 = L に達し、w ≥ 65 の level 17 全滅には g4 形の
  mod 法 classMax 精密化が必要。g2=8・g3=11..13 は w=67 まで余裕。
- **素数冪法はリーフ証明書が最適**: DFS へのインライン化は
  per-node コスト約12倍で枝刈り利得を上回る（w=57 mask 700..740 での
  比較実験・負の観測）。
- **重い帯は局在しつつ幅を広げる**: w=57 は mask 700..950 に局在、
  w=58 は 700..920 に加えて中間帯 1050..2500 も一貫して重い
  （ノード上限チャンク分割で完走・分類はマスク単位で冪等）。

## 限界

- 標準整数格子限定。任意間隔平行行には主張しない。
- P(59)..P(82) は open。w=59 は推定 ~9.4M ノード（×1.36 則）で
  分割キャンペーンで数セッション完了見込み。g0 会計は w ≤ 64 まで有効。
