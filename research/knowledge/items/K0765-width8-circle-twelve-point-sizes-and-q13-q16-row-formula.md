---
id: K0765
title: "幅8整数格子の円は全mでP(8)=12・可能サイズ{7,8,10,12}・9以上は偶数のみ — 素数オフセット補題とq=13..16の行分離公式"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "8つの連続整数行（8×m・全m≥1）上の円の格子点数は高々12で、可能な点数は7,8,10,12のみ（9以上の奇数と14は全mで不存在）。系として幅8・q≥13で g(S)=(8·min(m,q−1)−|S|) mod2・M_{8,q}=q−1"
evidence: "数学的証明（mod9剰余分類 d≤6 + K0763/K0764接点補題のw=8拡張 + 素数オフセット補題: t=p≡3 mod 4 は全二重行と非両立）。witness (2x−7)²+(2y−7)²=50 は8×8で12点"
solution:
  board: 幅8固定長m可変の標準整数格子
  level: strong
  outcome: unconditional
  classification: [all-safe-grundy]
  coverage: 幅8・q≥13は全m≥1・全安全局面
  conditions: 連続整数行・q≥13（円の構造定理はqに依らず全称）
  verification: [mathematical-proof]
  certificate: mod9剰余分類 + 素数オフセット補題(p=7) + K0764のw=7ペア排除の再利用
  independent_check: witness円の直接列挙・census(8×8/8×11)・t=7共存0件の有限検証
  note: "q=13..16が新規確定。q≥17はK0025と重複（整合）"
relations:
- type: depends_on
  target: K0072
  note: 二重行数上界のmod9枠組み（8連続行版を本項目で独立計算）
- type: depends_on
  target: K0763
  note: 接点補題（f|t・符号論）の原形
- type: depends_on
  target: K0764
  note: w=7 の非両立ペア排除((1,3),(2,3),(3,4),(3,5),(1,4),(5,6))をt∈{1..6}に再利用
- type: depends_on
  target: K0025
  note: 行分離公式の枠組み。本項目はP≤2wの自明円上界をP(8)=12に改良して閾値をq>16からq>12へ下げる
- type: supports
  target: K0332
  note: 幅8の安定化長はq≥13で確定。M_{8,q}(q≤12)はopen
artifacts:
- path: research/experiments/width8-circle-twelve-point-20261112/reports/width8-circle-twelve-point.md
  role: proof
  note: 定理・系・証明・素数オフセット補題・P(w)データ列の記録
- path: research/experiments/width8-circle-twelve-point-20261112/scripts/width8_circle_bound.ts
  role: verifier
  note: witness列挙・mod9分類・素数補題制御・f=2・2接点・censusの機械検証
- path: research/experiments/width8-circle-twelve-point-20261112/output/width8_circle_bound.json
  role: data
  note: 全制御の実行結果
- path: research/log/2026-11-12-width6-circle-eight-point-proof.md
  role: log
  note: 本セッションの判断・教訓・レジューム（幅6/7/8共用）
---

## 命題（証明済み・全称）

1. **P(8) = 12**: 8つの連続整数行からなる任意の整数格子（8×m、全 m ≥ 1）上で、
   円の格子点数は高々 12。可能な点数は 7, 8, 10, 12 のみで、
   **9・11・13（9以上の奇数）と 14 は全 m で存在しない**。
2. **接点補題（w=8 版）**: 盤内接点行を持つ円の二重行は高々 3。
   よってサイズ ≥ 9 の円はすべて接点なし・偶数点数。
   witness: (2x−7)²+(2y−7)²=50 は 8×8 で 12 点（6二重行 {0,1,3,4,6,7}・接点なし）。
3. **素数オフセット補題**: 接点付きフレーム（t(g−t) = s²）で t = p が素数のとき
   g ≡ 0 (mod p)。他の二重行 t'（1 ≤ t' ≤ p−1）は t'(g−t') ≡ −t'² (mod p) が平方数
   であることを要求し、これは −1 ∈ QR(p)、すなわち **p ≡ 1 (mod 4) と同値**。
   p = 7 では t=7 が全二重行と非両立（w=8 で決定的）。
4. **系（q ≥ 13）**: 円 ≤ 12 < q、非水平直線 ≤ 8 < q により行を跨ぐ禁止 q 点集合なし。
   全 m ≥ 1・全安全局面 S で

   g(S) = (8·min(m, q−1) − |S|) mod 2,　M_{8,q} = q−1（q = 13..16 が新規）。

## 証明の骨子

- d ≤ 6: mod9 剰余分類（8連続行 worst 6、9³ 通り）。
- 接点補題: f | t（K0763）。4+ 二重行は f=1 で t ∈ {1..7}。
  t=7 は素数補題で孤立 → {1..6} から 4つ → K0764 の w=7 ペア排除で全滅。
  f=2 は同符号 {2,4,6} ≤ 3、f≥3 は符号論で ✗。
- 13/14: 13 = 6+接点 ✗、14 = d=7 ✗（mod9）/ 2接点（g=7→二重行0、g=6→{3}）✗。

## 機械検証

witness 12点直接列挙、mod9 worst 6、|g| ≤ 10⁶ で最大 3・t=7 共存 0 件、
f=2 最大 2、2接点 g=7→0/g=6→{3}、census 8×8 = 86（12点円は witness のみ）・
8×11 = 213。サイズ集合 {7,8,10,12}。

## P(w) のデータ列・限界

- **P(6)=8, P(7)=10, P(8)=12**（K0763/K0764/本項目）: P(w) = w+2 が w=6,7,8 で成立、
  いずれも「9以上は偶数のみ」構造。K0025 の P ≤ 2w を sharp化。
  **w = 9..14 の P(w) は open**（K0072 の w ≥ 15 上界 P ≤ w+⌈w/2⌉ と接続する中間帯）。
- 幅8の q ≤ 12 occupancy プログラムは未開拓（非水平8点直線も危険曲線）。
