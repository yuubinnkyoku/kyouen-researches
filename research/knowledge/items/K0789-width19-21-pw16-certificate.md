---
id: K0789
title: "幅19..21の円点数の完全決定 P(19)=P(20)=P(21)=16 — 基底18法生残16集合が素数冪（11²・7³）のみで全滅 — K0778の条件付き上界を無条件等号に強化・P(w)は全幅6..48で決定済みに"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "幅w固定・長さm可変（全m≧1）の標準整数格子の円の格子点数: P(19)=P(20)=P(21)=16（全称・等号付き・有界半径探索に非依存）。帰結としてP(w)はw=6..48の全幅で決定済み（K0778/K0782/K0784/K0788との合体）"
evidence: "数学的証明（K0072 Vieta + K0763-K0767 会計 + K0778/K0784 と同一枠組み・第五独立実装）。P≧17 ⟹ d≧8・d+s≧9 点行。標準形の9部分集合は全法 m で証明書 ∃(a,u) mod m: a−4i²−ui ∈ QR0(m) を通過（A・e は奇素数冪 mod で自由・偶数法は上位集合で健全）。基底18法の k=9 完備掃引（C(w,9)・窓マスク制限なし）で生残 w=19: 2・w=20: 8・w=21: 16 集合（K0778/K0784 の記録と三重一致・全数保持）。拡張法掃引（素数53..343・素数冪121,125,128,169,256,289,343等）で全16集合が法 121=11² または 343=7³ のみで全滅（無条件）。w=19/20 の全候補は w=21 の16集合に含まれ同一掃引で全滅。g0≧2 形は convention B classMax: g2 = 6..7・g3 = 5・g4+ 類サイズ≦6、全て <9（A と B は数値一致）。下界: 130 円 (2x−11)²+(2y−11)²=130 が w=17..21 でちょうど16点（行{0,1,2,4,7,9,10,11}・全2重行）。制御: 実在 witness の行集合（130円・50円・650円 S*）は拡張法全60法で証明書通過（誤殺なしの直接検証）"
solution:
  board: 幅w固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: P(19)=P(20)=P(21)=16 は全称・全 m≧1・全安全局面
  conditions: 連続整数行
  verification: [mathematical-proof]
  certificate: 基底18法 k=9 完備生残列挙 + 拡張法（素数冪 11²・7³）無条件全滅 + g0≧2 convention-B classMax 会計 + 130円下界
  independent_check: "生残数の三重一致（w17/18: 0・w19: 2 with S1 文字一致・w20: 8・w21: 16 = K0784 命題4）・実在3 witness の拡張法全通過・perMod 内訳の総和検算（293,914+16=293,930）"
  note: "素数掃引で死なず素数冪で死ぬ候補の初例。level 分類の標準法リストに素数冪を加める価値の根拠。P(21) は K0784 の最後の open（∈{16,17,18}）であった"
relations:
- type: supports
  target: K0784
  note: 命題4（P(21) open）を閉鎖。w=21 level 9 の生残16集合を拡張法で全滅させ P(21)=16 を確定。P(w) の全幅決定（6..48）の最後の欠片
- type: supports
  target: K0778
  note: w=19,20 の条件付き上界 P≦18（R≦2×10⁷ 有限観測）を無条件の等号 P=16 に強化。w=19 の生残2集合・w=20 の8集合は w=21 の16集合に含まれ素数冪掃引で全滅
- type: depends_on
  target: K0072
  note: Vieta 整数化・合同証明書・接点行≦2 の枠組み
- type: depends_on
  target: K0788
  note: g0≧2 証明書の convention B（類変数 t に係数 4g0²）の正当性。本項目の classMax 会計は B で実施
artifacts:
- path: research/experiments/width19-21-pw16-certificate-20261113/scripts/width19_21_pw16_certificate.ts
  role: verifier
  note: 生残列挙・拡張法掃引・g0会計・witness の単独再現（決定的・STAGE 分割・依存なし）
- path: research/experiments/width19-21-pw16-certificate-20261113/output/width19_21_pw16_certificate.json
  role: data
  note: 全数値の機械出力（生残集合・killedBy・classMax・witness・perMod）
- path: research/experiments/width19-21-pw16-certificate-20261113/reports/width19-21-pw16-certificate.md
  role: proof
  note: 定理・証明骨子・制御・構造観察・限界
- path: research/log/2026-11-13-width19-21-pw16-certificate.md
  role: log
  note: 判断・教訓・レジューム
---

## 命題（証明済み・全称・等号付き）

1. **P(19) = P(20) = P(21) = 16**（幅 w の連続整数行・全 m ≥ 1・標準整数格子）。
   下界: 130 円 (2x−11)²+(2y−11)² = 130（行 {0,1,2,4,7,9,10,11}・16 点・w=17..21 でちょうど 16）。
   上界: P ≥ 17 ⟹ d+s ≥ 9 点行だが、
   - 標準形: 基底 18 法で生き残る 9 行集合は w=19: 2・w=20: 8・w=21: 16 集合のみで、
     **全てが法 121 = 11² または 343 = 7³ の証明書で無条件に死ぬ**。
   - g0 ≥ 2 形: convention B classMax は g2 = 6..7・g3 = 5・g4+ 類サイズ ≤ 6 < 9。
   よって d+s ≤ 8 → P ≤ 16。
2. **帰結**: K0778/K0782/K0784/K0788 と合わせ、**P(w) は全幅 w = 6..48 で決定済み**。
   16 プラトー w=12..21・24 プラトー w=26..42・跳躍帯 w=43..48（26,28,28,30,30,32）。

## 証明の骨子

- K0072 Vieta + K0763-K0767 会計（接点行 s ≤ 2・P = 2d+s・d ≥ 8 → C ∈ Z）。
- 標準形の証明書は任意の奇素数冪で必要条件（A mod m は N 自由により自由・
  e mod m は 4D 自由により自由。偶数法では自由 (a,u) が真に上位集合で健全）。
- 基底 18 法の k=9 完備掃引（C(w,9)・K0784 の窓マスク制限すら使わない上位集合）
  で生残を全数保持して列挙し、拡張法で掃引。**殺し手は全て 121 か 343**。
- w=19/20 の候補は全て w=21 の 16 集合に含まれるため同一掃引で閉じる。

## 制御

- 生残数三重一致（K0778 の 0/0/2/8・K0784 の 16・S1 の文字一致）。
- 実在 3 witness（130・50・650 円）の行集合は拡張法全 60 法で通過（誤殺検証）。
- perMod 総和検算: 293,914 殺し + 16 生残 = 293,930 = C(21,9) ✓。

## 構造的観察

- **素数冪の情報**: 基底法の素因数（11・7）の冪が独立な制約を与える。
  K0784 の「S* は全素数で通過」と対称的で、候補の生死は素数冪で決まることがある。
  level 分類の法リストに素数冪（p²・p³）を標準装備する価値の根拠。
  （「全素数通過 ⟹ 実在」ではない。方向性のみ。）

## 限界

- 標準整数格子限定。任意間隔平行行には主張しない。
- 次の open は w=49+ の跳躍（level 18 分類・11050 円族・K0785 の 48 行 span と
  P(83) ≥ 34 の突き合わせ）。
