---
id: K0763
title: "幅6整数格子の円は全mで最大8格子点 — P(6)=8の全称証明とq=9..12の行分離公式 M_{6,q}=q−1"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "6つの連続整数行（6×m・全m≥1）上の円の格子点数は高々8（8点円の実在で等号成立）。系として幅6・q≥9では行を跨ぐ禁止q点集合が存在せず g(S)=(6·min(m,q−1)−|S|) mod2・M_{6,q}=q−1"
evidence: "数学的証明（mod9剰余分類による二重行数上界 d≤4 の独立再現 + 接点行があれば二重行は高々3という初等的整数論的新証明）。有限制御は全て機械検証済み"
solution:
  board: 幅6固定長m可変の標準整数格子
  level: strong
  outcome: unconditional
  classification: [all-safe-grundy]
  coverage: 幅6・q≥9は全m≥1・全安全局面
  conditions: 連続整数行・q≥9（円の上界はqに依らず全称）
  verification: [mathematical-proof]
  certificate: mod9剰余分類 + mod3によるt=3排除 + (a−u)(a+u)=3の一意分解
  independent_check: 端末例x²+y²=25（7点）での代数の端末確認・census再現
  note: "q=9,10,11,12が新規確定。q≥13はK0025と重複（整合）"
relations:
- type: depends_on
  target: K0072
  note: 二重行数上界 d≤4（6連続行）のmod9中核を独立に再現して使用。行公式の枠組みも同じ
- type: depends_on
  target: K0760
  note: 8点円の実在（census・再現一致）により上界の等号成立を保証
- type: depends_on
  target: K0001
  note: 行分離帰結の行公式はK0072と同一の行ゲーム導出
- type: supports
  target: K0332
  note: 幅6の安定化長はq≥9で確定（M_{6,q}=q−1）。M_{6,7}はm≥20のままopen
- type: extends
  target: K0025
  note: q>2w（q≥13）を幅6のq=9..12まで拡張
artifacts:
- path: research/experiments/width6-circle-eight-point-20261112/reports/width6-circle-eight-point-bound.md
  role: proof
  note: 定理・系・全証明段階の記録
- path: research/experiments/width6-circle-eight-point-20261112/scripts/width6_circle_bound.ts
  role: verifier
  note: mod9分類・接点補題制御・端末例・census再現の全機械検証
- path: research/experiments/width6-circle-eight-point-20261112/output/width6_circle_bound.json
  role: data
  note: 全制御の実行結果
- path: research/log/2026-11-12-width6-circle-eight-point-proof.md
  role: log
  note: 判断・教訓・レジューム
---

## 命題（証明済み・全称）

1. **P(6) = 8**: 6つの連続整数行からなる任意の整数格子（6×m、全 m ≥ 1）上で、
   任意の円が含む格子点数は高々 8。8点円は実在（6×13で102本・K0760一致）し等号は達成される。
   K0760の「m ≤ 70 で9点円なし」という有限観測を全 m の全称定理に昇格。
2. **系（q ≥ 9）**: 幅6・q ≥ 9 では、円は ≤ 8 < q 点、非水平直線は ≤ 6 < q 点しか
   持たないため行を跨ぐ禁止 q 点集合が存在せず、各 row 直線は容量 q−1 の独立成分となる。
   全 m ≥ 1・全安全局面 S で

   g(S) = (6·min(m, q−1) − |S|) mod 2,　M_{6,q} = q−1。

   新規に確定するのは **q = 9, 10, 11, 12**（q ≥ 13 は K0025 の q > 2w で既にカバーと整合）。

## 証明の骨子

- 円 x²+y²+Cx+Dy+N=0 の行 y の格子点は x²+Cx+(y²+Dy+N)=0 の整数根。
  点数 P = 2d + s（d = 二重点行、s = 接点行、s ≤ 2）。
- **d ≤ 4**: 6連続行に5二重行あれば連続二重行ペアがあり、判別式差の整数性から
  D ∈ ℤ・M := C²−4N ∈ ℤ に帰着（Vieta還着）。disc(y) = M−4y²−4Dy が正の平方数
  ⟹ mod9でQR(9)={0,1,4,7}。剰余分類（M,D,k 全9³通り）で6連続行中QR行は高々4。
  K0072 中核の w=6 場合の独立再現。
- **d = 4 ∧ s ≥ 1 の排除（本項目の新しい要素）**: 接点 (x₀,y₀) は C = −2x₀（偶）を強制し、
  二重行 y では disc(y)/4 = t·(y₀+y+D) = s² ∈ ℤ（t = y₀−y）。D = e/f 既約とすると
  f | t（gcd(h,f)=1、h=2fy₀+e）。4つの相異なる非零 t ∈ [−5,5] ⟹ f ∈ {1,2}。
  - f = 2: 二重行は ±2, ±4 全部必要だが t=2 と t=−2 から (h−4) と −(h+4) が
    両方正の平方数になり a²+b² = −8 で矛盾。
  - f = 1: t(g−t) = s² > 0（g = 2y₀+D）。符号論で4つの t は同符号、鏡映で
    t ∈ {1..5}・g > 5。**t = 3 は mod 3 により t = 1,2,4,5 の全てと非両立**
    （g−1≡2、e²≡2、u²≡2、v²≡2 (mod 3)）。残る4倍集合 {1,2,4,5} は (1,4)、
    すなわち a²−u²=3 ⟹ (a−u)(a+u)=3 ⟹ g=5 の一意分解を含み、g>5 と矛盾。
- よって P ≤ max(8, 2·3+2) = 8。実在より等号。

## 機械検証

mod9剰余分類（worst 4 行）、f=1 接点条件の |g| ≤ 10⁶ で「4つの t が平方」0件
（最大3・t=3の共存も0件）、f=2 の両方正平方数 0件、d=5 スポットチェック（|M|,|D|≤600）0件、
端末例 x²+y²=25（行0,3,4二重+行5接点=7点、代数 g=10・t={1,2,5} と一致）、
census 再現（6×13=116・6×16=176、K0760完全一致）。

## 限界・スコープ

- 標準整数格子（連続6行）の定理。任意間隔平行行・w≠6 には主張しない。
  同手法の一般化（接点補題の w≠6 版・二重行剰余分類の w≠6 版）は未解析。
- 7/8点円の個数漸近（K0760の~26/m線形観測）は有限事実のまま。
- q = 7, 8 は 7/8 点円が実在するため対象外。M_{6,7} は m ≥ 20 のまま open（K0761）。
  ただし本定理により、6×m の q=7 危険曲線が**全 m で**7点円・8点円・行直線に限ることが
  証明レベルで確定し、census方式の完全性（9点円の探索不要）が全 m で保証された。
