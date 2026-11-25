---
id: K0776
title: "幅w≧19整数格子の円点数上界P(w)≦2⌈w/2⌉（偶数wでは≦w）— w≧19半密度証明書のQR₀混合点行解釈の監査完了と行分離公式の無限族拡大"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "19個以上の連続整数行（w×m・全m≧1）上の円の格子点数はP(w)≦2⌈w/2⌉（w偶ならP(w)≦w・w奇ならP(w)≦w+1）。特にP(19),P(20)≦20（下界16）。K0767のw=15..18と合わせP(w)≦2⌈w/2⌉は全w≧15で成立（w=15で等号・開始幅は最良）。系として全w≧19・q>2⌈w/2⌉で g(S)=(w·min(m,q−1)−|S|) mod2・M_{w,q}=q−1（新規q領域 q∈(2⌈w/2⌉, w+⌈w/2⌉] は各wにつき⌊w/2⌋個の無限族）"
evidence: "数学的証明（K0072のw≧19半密度証明書がQRに0を含み点行混合集合に有効であることの第三実装監査 + P≦2(d+s)会計 + 非Vietaは『最大独立集合は交代＝純パリティ』の組合せ論と接点行積分性による標準形帰着で証明書に接続）。監査は3素数のwindow bitmask全列挙・周期713は713類型×min-span全列挙で独立再現（L=18の10>9・L=26の14という既知の擬似反例も再現）"
solution:
  board: 幅w≧19固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: P(w)上界はw≧19で全称・系は該当(w,q)で全m≧1・全安全局面
  conditions: 連続整数行・系はq>2⌈w/2⌉（q>wは自動）
  verification: [mathematical-proof]
  certificate: 法毎有限剰余除外（QR₀混合・w=19,20は11·19·23・w=21..26は11·23·31・w≧27は23·31周期713）+ 交代独立集合引数 + 接点行標準形帰着
  independent_check: 第三実装（per-prime (n,c) bitmask全走査・周期713は類型×min-span）。221=13·17は0なしでは192になるため従来報告値自体がQR₀計算である追加証拠
  note: "P(19),P(20)の真値∈{16..20}はopen。witness探索（原始sum-of-two-squares族・R≦10¹¹・619,574候補）では17..22行窓の17点以上は不存在（最大16=R=130）— 有界な負の観測であり全称主張ではない"
relations:
- type: depends_on
  target: K0072
  note: w≧19半密度証明書（4807 CRT・11·23·31・周期713）のQR₀混合妥当性を監査して点行上界d+s≦⌈w/2⌉として昇格
- type: depends_on
  target: K0767
  note: P≦2(d+s)会計・QR₀解釈・非Vietaカスケード（接点行積分性）・w=15..18のP≦2⌈w/2⌉（本項目と合わせ全w≧15）
- type: depends_on
  target: K0025
  note: 行分離公式 g(S)=(w·min(m,q−1)−|S|) mod2・M_{w,q}=q−1 の導出枠組み
- type: generalizes
  target: K0025
  note: 新規(w,q)は q∈(2⌈w/2⌉, w+⌈w/2⌉]（K0025のq>2wとK0072のq>w+⌈w/2⌉の間の全帯）
- type: supports
  target: K0332
  note: "安定化長M_{w,q}=q−1の無限族拡大（例: w=19:q=21..29・w=30:q=31..45・w=100:q=101..150）"
artifacts:
- path: research/experiments/width19-plus-half-density-mixed-20261112/reports/width19-plus-circle-point-max.md
  role: proof
  note: 定理・証明・系表・witness探索の記録
- path: research/experiments/width19-plus-half-density-mixed-20261112/scripts/width19_plus_mixed_audit.ts
  role: verifier
  note: 監査3セグメント+witness探索の単独再現（MODE切替）
- path: research/experiments/width19-plus-half-density-mixed-20261112/output/width19_plus_mixed_audit.json
  role: data
  note: 監査全数値の機械出力
- path: research/experiments/width19-plus-half-density-mixed-20261112/output/circle_witness_search.json
  role: data
  note: witness探索の機械出力（制御・最大16）
- path: research/log/2026-11-12-width19-plus-half-density-mixed.md
  role: log
  note: 判断・教訓・レジューム
---

## 命題（証明済み・全称）

1. **P(w) ≤ 2⌈w/2⌉（w ≥ 19・全 m ≥ 1）**: 偶数 w では P(w) ≤ w、奇数 w では P(w) ≤ w+1。
   従来の K0072 上界 w+⌈w/2⌉（≈1.5w）から ≈w/2 改善。特に **P(19), P(20) ≤ 20**（従来 29/30）。
   下界 16（K0767 witness）より P(19), P(20) ∈ {16..20}。
2. **全 w ≥ 15 での統一**: K0767 の w=15..18（P ≤ 16,16,18,18）と合わせ
   **P(w) ≤ 2⌈w/2⌉ は全 w ≥ 15 で成立**。w=15 で等号（P(15)=16）なので w ≥ 15 は最良
   （w=12..14 では P=16 > 2⌈w/2⌉）。
3. **系（行分離公式・無限族）**: w ≥ 19 かつ q > 2⌈w/2⌉ なら（q > w は自動）、行を跨ぐ禁止
   q 点集合は存在せず、全 m ≥ 1・全安全局面で g(S) = (w·min(m,q−1) − |S|) mod 2、M_{w,q} = q−1。
   新規 (w,q): **w=19: 21..29、w=20: 21..30、w=21: 23..32、w=22: 23..33、w=23: 25..35、
   w=24: 25..36、w=25: 27..38、w=26: 27..39、w=27: 29..41、w=28: 29..42、w=29: 31..44、
   w=30: 31..45**、一般に q ∈ (2⌈w/2⌉, w+⌈w/2⌉]（各 w につき ⌊w/2⌋ 個・全 w ≥ 19）。

## 証明の骨子

- **会計**: P = 2d+s ≤ 2(d+s)（接点行 ≤ 2・盤外クリッピングは減少のみ）。
- **Vieta ケース**: 全点行で R−(2y+D)² ∈ QR₀(p)（0込み・接点行は0）。K0072 の w ≥ 19 証明書
  （w=19,20: mod 11·19·23 → 最大10、w=21..26: mod 11·23·31 → 11,11,11,12,12,13、
  w ≥ 27: mod 23·31 周期713 → 期中最大221・全区間 ⌈w/2⌉ 以下）が QR₀ のまま点行混合集合に有効
  → d+s ≤ ⌈w/2⌉ → P ≤ 2⌈w/2⌉。
- **非 Vieta ケース**: 二重行は独立集合 → d ≤ ⌈w/2⌉、等号は交代（純パリティ）のみ。
  d ≤ ⌈w/2⌉−1 → P ≤ 2⌈w/2⌉。d = ⌈w/2⌉ ∧ s ≥ 1 → 接点行は反対パリティ →
  (y−y_t)·U ∈ ℤ（奇差）→ U, A ∈ ℤ（標準形）→ 証明書（(A,U) ⟷ (N,C) 全単射）より
  d+s ≤ ⌈w/2⌉ → 矛盾 → s = 0 → P = 2⌈w/2⌉。

## 監査（第三実装）

- 3素数の window bitmask（per-prime (n,c) ∈ (ℤ/p)² 全走査）AND 最大 popcount を直接計算。
- 周期713: 全 (c₂₃,c₃₁) 並進は (n₂₃,n₃₁) の base pattern 回転と等価 → 713類型 × min-span
  全列挙で全 L = 27..442 を監査（violations 0・L=26 の 14 を再現）。
- 従来報告の 221 = 13·17 は QR₀ のみで出る値（0 なしでは 192）— 従来証明書が 0 込みであることの
  追加証拠。元 script の `{x*x % p}` も確認済み。
- w=713k+r の合成論法は max 値不変のためそのまま。

## witness 探索（有界・負の観測・全称主張ではない）

原始 sum-of-two-squares 族（R = 2^a·∏p^e、p ≡ 1 mod 4 ≤ 149、Σe ≤ 8、R ≤ 10¹¹、
619,574候補・全 (D,C) パリティ族）で 12/17..22 行窓の最大点数を探索:
**17点以上は不存在（最大 16 = R=130 の K0767 witness・制御再現 ✓）**。
P(19)=20 / P(17)=18 の witness はこの族の R ≤ 10¹¹ には存在しない。
未探索: 4分整数中心 D（行座標間隔8で疎）、R > 10¹¹、Σe > 8。D=1/2 型中心は格子点を持たない
ことを 2進パリティで確認。

## 限界・スコープ

- 標準整数格子の定理。任意間隔平行行には主張しない。
- P(w) = 2⌈w/2⌉ の達成（w ≥ 19 で等号円の存在）は未解決。
- K0767 の残候補（w=17/18 の真値、Vieta 9行・混合パリティ9集合・g=2形10行）は未監査のまま。
