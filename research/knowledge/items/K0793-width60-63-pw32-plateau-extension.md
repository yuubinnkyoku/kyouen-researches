---
id: K0793
title: "幅60..63の円点数の完全決定 P(60)=…=P(63)=32 — 32点プラトーがw=63まで継続 — P(w)は全幅6..63で決定済み・level 17の復活点は(63,83]に狭窄・ノード成長則は×1.27へ漸減"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "幅w固定・長さm可変（全m≧1）の標準整数格子の円の格子点数: P(60)=P(61)=P(62)=P(63)=32（全称・等号付き）。帰結としてP(w)はw=6..63の全幅で決定済み（32プラトーはw=49..63）。level 17の復活点は(63,83]（K0785のP(83)≧34）。P(64)..P(82)はopen。g0会計はw≦64まで有効"
evidence: "数学的証明（K0790/K0792 streaming機の直接拡張・ノード上限チャンクの関数化）。w=60: maximal mask 3,171個・11チャンク・ノード計12,055,719。w=61: 3,206個・14チャンク・ノード計15,726,739。w=62: 3,242個・17チャンク・ノード計20,012,983。w=63: 3,278個・22チャンク・ノード計25,418,908。いずれもleaves=0・生残0でlevel 17全滅 ⟹ d+s≦16 ⟹ P≦32。g0≧2形はconvention B classMax（K0792数表: w60 g2 8/g3 12/g4 15・w61..63 g2 8/g3 13/g4 16・全て<17）。下界: 2210円の全32点（v-span 94≦2(w−1), w≧49）。制御: w=26 L=12 S* ちょうど1生残（K0782/K0784/K0788/K0790/K0792一致）。ノード成長 ×1.288..1.305..1.272..1.270/w（×1.36則から漸減）・maximal mask数は+35/wでほぼ線形"
solution:
  board: 幅w固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: P(60)=…=P(63)=32 は全称・全 m≧1・全安全局面
  conditions: 連続整数行
  verification: [mathematical-proof]
  certificate: 窓マスク完備候補生成（mod 9×11）+ 16法bit-set DFS level 17 全滅（ノード上限1.2Mチャンク・lastDone冪等再開・2チャンク/実行）+ g0≧2 convention-B classMax 会計 + 2210 witness 下界
  independent_check: S* 制御・ノード成長則（×1.27..1.31・w59→63で9.36M→25.42M）・mask数成長（+35/w）・g0会計値のK0792数表からの連続性
  note: "重い帯は上端~1300で安定し下端がwとともに沈む（w60: 736..1586 → w63: 434..1314・約2/3のmaskがノード上限チャンク消化）。w=64 は現g0会計（g4=16<17）で証明可能な最後の幅・推定~32Mノード。w=65 でg4類サイズ⌈65/4⌉=17=Lに飽和し、w≧65にはg4形classMax精密化が必要"
relations:
- type: depends_on
  target: K0792
  note: streaming 機・意味論・g0 会計数表・2210 witness の直接拡張。32 プラトーを w=59 から w=63 へ延長・ノード上限チャンクを関数化
- type: depends_on
  target: K0790
  note: 分類機・mod 9×11 maximal mask 候補生成・×1.36 成長則（本項目で×1.27..1.31 への漸減を観測）
- type: supports
  target: K0785
  note: level 17 復活点を (59,83] から (63,83] に狭窄
artifacts:
- path: research/experiments/width60-63-level-classification-20261113/scripts/width60_63_level_classify.ts
  role: verifier
  note: ノード上限チャンク対応 streaming 分類機（classify が lastDone を返す・決定的・依存なし）
- path: research/experiments/width60-63-level-classification-20261113/output/width60_63_level_classify.json
  role: data
  note: 全数値の機械出力（chunks・g0 会計・witness・w60..w63 完走）
- path: research/experiments/width60-63-level-classification-20261113/reports/width60-63-level-classification.md
  role: proof
  note: 定理・証明骨子・制御・重い帯の下界側拡大・g4 有効期限
- path: research/log/2026-11-13-width60-63-level-classification.md
  role: log
  note: 判断・教訓・レジューム
---

## 命題（証明済み・全称・等号付き）

1. **P(60) = P(61) = P(62) = P(63) = 32**（幅 w の連続整数行・全 m ≥ 1・標準整数格子）。
   - 上界: level 17 全滅（w=60: 3,171 mask・12,055,719 ノード・
     w=61: 3,206・15,726,739・w=62: 3,242・20,012,983・
     w=63: 3,278・25,418,908・いずれも leaves=0）⟹ d+s ≤ 16 ⟹ P ≤ 32。
     g0 ≥ 2 形は convention B classMax（w60: g2 8/g3 12/g4 15・
     w61..63: g2 8/g3 13/g4 16・全て < 17）。
   - 下界: 2210 円の全 32 点（v-span 94 ≤ 2(w−1)）。
2. **帰結**: **P(w) は全幅 w = 6..63 で決定済み**
   （16 プラトー 12..21・跳躍 22..25・24 プラトー 26..42・漸増 43..48・
   32 プラトー 49..63）。
3. **level 17 の復活点は (63, 83] に狭窄**（K0785 の P(83) ≥ 34 と合わせ）。

## 制御

- w=26 L=12 は S* ちょうど 1 生残（K0782/K0784/K0788/K0790/K0792 と完全一致）。
- ノード成長: 9,361,851 (w59) → 12,055,719 (w60) → 15,726,739 (w61)
  → 20,012,983 (w62) → 25,418,908 (w63)。×1.288/×1.305/×1.272/×1.270
  （×1.36 則からの漸減）。
- maximal mask 数: 3,087 → 3,171 → 3,206 → 3,242 → 3,278（ほぼ +35/w）。

## 構造的観察

- **重い帯の下界側への拡大**: heavy band の上端は ~1300 で安定し、
  下端は w=60 の 736 から w=63 の 434 へ沈む。w=63 では約2/3の mask が
  ノード上限チャンクで消化された。局在性は完全に崩れた方向。
- **g0 会計の有効期限**: w=64 が現会計（g4=16 < 17）で証明可能な
  最後の幅（推定 ~32M ノード・×1.27 則）。w=65 で g4 類サイズ 17 = L に飽和。
- **運用**: ノード上限チャンクを classify 関数に組み込み lastDone を
  返す方式で、2 チャンク/実行が w=63 まで全て安定。

## 限界

- 標準整数格子限定。任意間隔平行行には主張しない。
- P(64)..P(82) は open（P ∈ [32, 2⌈w/2⌉−4]）。w=64 は ~32M ノードの
  分割キャンペーン対象。w ≥ 65 は g4 形 classMax 精密化が前提。
