---
id: K0797
title: "convention B g0会計の有効範囲は拡張法でw≤84に延長 — g4形は壁でなく真の壁はg3形（類サイズ29）— P(65)..P(84)の決定に必要な非標準形前提が復活点下界83をちょうどカバー"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "標準整数格子の幅w固定・長さm可変の円点数決定に使うconvention B g0会計（非標準形除外のclassMax < 17要求）の有効範囲。w=65..84で有効・w=85..87で不成立。P(w)の値そのものは決定しない（標準形DFSは別実行）。"
evidence: "有限完全検査（数学的証明）。全g0形（g2..g5・類サイズ≥17）について33法（BASE18+EXTRA+BIG・最大343）の全(a,u)対走査でclassMaxを直接法と増分sweepの2実装で計算し一致。制御: K0788/K0792/K0794のbase18既知値（w36:6/8・w42:7/10・w48:7/11・w64:8/13）を完全再現・sweep≡direct・g3 size29の失敗はwitness (a,u)=(0,1) mod 31の17点生存で明示。"
solution:
  board: 幅w固定長m可変の標準整数格子（証明方法論の有効範囲）
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: level 17 全滅 ⟹ P(w) ≤ 32 論法の非標準形（g0 ≥ 2）側の前提が全w ≤ 84で正当
  conditions: 連続整数行
  verification: [mathematical-proof, finite-verification]
  certificate: 全 (a,u) 全数走査による classMax = min_m max_{a,u} #{t ∈ 類: a − 4g0²t² − ut ∈ QR(m)} < 17 の機械検証（2実装一致）
  independent_check: 直接法と増分sweepの一致・既知会計値（K0788/K0792/K0794）の完全再現・失敗側witnessの明示
  note: "K0794の『g4形のclassMax精密化が唯一の壁』は訂正: g4形はu奇制限（g0偶⟹q奇）と係数64でclassMax 5..9に自明に切り下がり、真の壁はg3形（類サイズ29 = w85..87でclassMax=17・全法で不変）。g2形はm=32/64のu奇制限付きで類サイズ43までclassMax=10に強化。P(65)..P(84)はopenのまま（標準形16法DFSの実行コストが長期レーン対象・w=64で33.2Mノード×1.3/w成長）。"
relations:
- type: depends_on
  target: K0788
  note: convention B g0会計（classMax・u奇制限・類変数t）の定式化をそのまま使用
- type: depends_on
  target: K0794
  note: K0794レジューム(1)への回答。会計有効範囲をw≤64からw≤84に延長し、『g4が唯一の壁』の帰結を訂正（真の壁はg3）
- type: supports
  target: K0785
  note: 会計有効範囲がK0785のlevel 17復活点下界83をちょうどカバー — w=83,84のlevel 17分類は会計上は正当化可能（DFSコストは別）
artifacts:
- path: research/experiments/g0-accounting-extended-20261113/scripts/g0_accounting_extended.ts
  role: verifier
  note: 33法・全(a,u)走査・sweep/direct 2実装・制御込み・単独実行で完走
- path: research/experiments/g0-accounting-extended-20261113/output/g0_accounting_extended.json
  role: data
  note: 会計表 w=65..85・フロンティア84・base18のみ78・g3 size29失敗witness
- path: research/experiments/g0-accounting-extended-20261113/reports/g0-accounting-extended.md
  role: proof
  note: 定理・意味論（P(w)を決定しない点を明記）・制御・数表
- path: research/log/2026-11-13-g0-accounting-extended.md
  role: log
  note: 実行記録・教訓・レジューム
---

# K0797: g0 会計の有効範囲 w ≤ 84 — g4 は壁でなく壁は g3

- id: K0797
- status: proved
- date: 2026-11-13
- scope: P(w) ≤ 32 論法の非標準形前提（convention B g0 会計）の有効範囲

## 命題（証明済み）

1. **convention B g0 会計（全 g0 ≥ 2 形で classMax < 17）は拡張法リスト
   （BASE18 ∪ EXTRA{49,121,53..83,32,64,81,125,169} ∪ BIG{343,89..139,128,243,289}・計33法）のもとで
   w = 65..84 の全幅で有効**。基底18法のみなら w ≤ 78。
2. **w = 85..87 では不成立**: g3 形の類サイズが 29 に達し、全法で
   classMax = 17（最良法でも witness (a,u) = (0,1) mod 31 が17点を生存させる）。
3. **g4 形は壁ではない**: classMax は 5..9。g0 = 4 は偶数なので分子 q は奇 →
   偶数法で u奇制限が正当、係数 4·16 = 64 と合わせて類サイズ 17..22 を自明に切る。
   K0794 の「w=65 で g4 類サイズ天井が飽和し g4 精密化が唯一の壁」は、
   類サイズの自明天井としては正しいが classMax の意味では誤り。
4. **g2 形は大幅強化**: m = 32/64（u奇制限付き）で類サイズ 43（w=85）まで classMax = 10。

## 意味論（過大主張の防止）

- この結果は「level 17 全滅 ⟹ d+s ≤ 16 ⟹ P(w) ≤ 32」の**非標準形側の前提**を
  w ≤ 84 で正当化する。**P(65)..P(84) の値は決定していない**。
  標準形側の 16法 bit-set DFS は w=64 で 33.2M ノード・約 ×1.3/w で成長し、
  個別幅の分類は長期レーン対象。
- K0785（P(83) ≥ 34）と合わせ、会計有効範囲は level 17 復活点の下界 83 を
  ちょうどカバーする。復活点は (64, 83] のまま。

## 証明の骨格

- classMax(類, 4g0², uOdd) = min over m of max over (a,u) of
  #{t ∈ 類: a − 4g0²t² − u t ∈ QR(m)}。QR(m) は x² mod m（x = 0..m−1）の全列挙で
  厳密（0込み・合成法も正確）。classMax < 17 ⟹ 17点行集合（g0 形）は
  どの (a,u) でもどこかの法で死ぬ。
- 類は連続 t = 0..⌈w/g0⌉−1（u は全区間走査で剰余類 r の依存を吸収）。
- 計算は増分 sweep（s を 1..sMax で一括）と直接法の 2 実装で一致確認。
- 制御: K0788 (w36: 6/8・w42: 7/10・w48: 7/11)・K0792 (w56: 8/11)・K0794 (w64: 8/13)
  の base18 値を完全再現。sweep ≡ direct（g2_m16_s32 = 8・g3_m49_s28 = 16）。
  失敗側は witness 明示で誤殺でないことを確認。

## 主要数値（combined 33 法）

- w=65: g2=8(33)・g3=12(22)・g4=5(17) → 有効
- w=78: g2=9・g3=16(26)・g4=6 → 有効（g3 は m=23）
- w=79..81: g3=**16**(27)（m=49）→ 有効
- w=82..84: g3=**16**(28)（m=49・343でも16）→ 有効
- w=85: g3=**17**(29) → 不成立（全法・witness (0,1) mod 31）

## 限界

- w ≥ 85 は会計不成立（g3）。g3 size 29 以上を切るには合同式以外の手法が必要。
- P(65)..P(84) は open（P ∈ [32, 2⌈w/2⌉−4]）。標準形 DFS の実行が別途必要。

## resume

1. w=65..72 程度の標準形 level 17 DFS キャンペーン（会計は正当化済み・ノード推定
   w=65 ~43M・長期レーン候補・分類できればP(w)=32が確定）。
2. g3 形 size ≥ 29 を切る非合同式手法の探索（楕円曲線的・Vieta的）。
3. M_{w,q} 表（K0795）は本件では不変（P(w)の値が変わらないため）。
