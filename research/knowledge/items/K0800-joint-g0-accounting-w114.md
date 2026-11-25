---
id: K0800
title: "convention B g0会計の合同フロンティアはjoint合同証明書でw≤114に延伸 — K0797のg3壁(size29)は単一法解析のアーティファクト — p-チェーン補題で33法は34個の最大素数冪に無損失簡約"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "convention B g0会計（非標準形除外・level 17全滅⟹P(w)≤32論法の前提）の合同証明書による有効範囲。joint全滅でw≤114・単一法でw≤84(K0797)。g3 size39..44(w=115..132)はopen。P(w)の値そのものは決定しない。"
evidence: "有限完全検査（数学的証明）。正しい会計量はjoint通過数|∩_m Pass_m(a,u)|（同一(a,u)で同じ行tが全法通過）でありmin_m count_mではない。g3 size29は法対{19,23}で全滅（独立ブルートフォース437²=190,969対・直接QR評価でmax=16@(0,77)・DFS nodes 17,550一致）。size30..38は{19,23,29,31}で全滅（DFS 65,776..10,031,034 nodes・BFS交差実装で一致・消滅は法31直後）。他g0形(g2,g4..g8・w≤132全size)は単一法で有効。p-チェーン補題(v∈QR(p^k)⟹v∈QR(p^j))で33法を34個の互いに素な最大素数冪に無損失簡約。"
solution:
  board: 幅w固定長m可変の標準整数格子（証明方法論の有効範囲）
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: level 17 全滅 ⟹ P(w) ≤ 32 論法の非標準形（g0 ≥ 2）側の前提が全 w ≤ 114 で正当
  conditions: 連続整数行
  verification: [mathematical-proof, exhaustive-enumeration]
  certificate: 全 (a,u)（coprime CRT独立走査）で joint 生存数 #{t: ∀m∈証明書, a−4g0²t²−ut∈QR(m)} ≤ 16 の機械検証（DFS・BFS・ブルートフォース3経路一致）
  independent_check: DFS ≡ BFS ≡ 直接ブルートフォース（size29）・K0797既知値再現（s27:16@343・s28:16・s29:17@31）・K0797失敗witness (0,1)@31 s29の17行生存再現（誤殺でないことの確認）・cm49≡cm343
  note: "K0797の『w≥85は会計不成立（g3）・合同式以外の手法が必要』は訂正: 単一法classMax=17でもjoint証明書は存在した。正しい会計量はjoint通過数で、単一法classMax<17は1法証明書の特別例。ただしK0785(P(83)≥34)によりlevel 17 extinctionはw≥83で偽なので、P(w)への実務的寄与はw≤82で尽きる。本結果の価値は方法論的（合同証明書の到達限界精密化・法リスト冗長性発見・K0797見立ての訂正）。g3 size39..44(w=115..132)はDFS予算内(120M/25M nodes, depth 6)でopen。"
relations:
- type: depends_on
  target: K0788
  note: convention B g0会計（classMax・u奇制限・類変数t）の定式化をそのまま使用
- type: depends_on
  target: K0797
  note: K0797レジューム(2)「g3 size≥29を切る非合同式手法」への回答。単一法フロンティアw≤84をjoint合同証明書でw≤114に延伸し「合同式以外の手法が必要」限界記述を訂正
- type: supports
  target: K0785
  note: 会計上の正当化範囲がw≤114に拡大（level 17復活点下界83を超えてカバー・P(w)実務上の寄与はw≤82）
artifacts:
- path: research/experiments/joint-g0-accounting-20261113/scripts/joint_g0_accounting.ts
  role: verifier
  note: MODS coprime DFS + BFS交差検証 + 制御込み・CFG.forms で per-form 実行（16MiBサンドボックス対応）
- path: research/experiments/joint-g0-accounting-20261113/output/joint_g0_accounting.json
  role: data
  note: 単一法MODS表（g2..g8・g3 s27..44）・joint証明書（s29:{19,23}・s30..38:{19,23,29,31}）・BFS交差・制御（ブルートフォース s29 max=16@(0,77)・cm49≡cm343・witness31=17）
- path: research/experiments/joint-g0-accounting-20261113/reports/joint-g0-accounting.md
  role: proof
  note: 定理・p-チェーン補題・joint会計量の定式・意味論（P(w)非決定・実務的寄与w≤82）・3経路独立検証・open（g3 s39..44）・レジューム
- path: research/log/2026-11-13-joint-g0-accounting.md
  role: log
  note: 実行記録・教訓（1<<32 wraparoundバグ・LAWS→MODS coprime切替）・レジューム
---

# K0800: joint g0 会計 — 合同フロンティア w ≤ 114・g3壁は単一法のアーティファクト

- id: K0800
- status: proved
- date: 2026-11-13
- scope: P(w) ≤ 32 論法の非標準形前提（convention B g0 会計）の合同証明書による有効範囲

## 命題（証明済み）

1. **正しい joint 会計量**: 17点行集合（g0 形）が合同証明書から逃れるには
   同一の整数 (a,u) のもとで**同じ行 t が全ての法を通過**する必要がある。
   会計量は J(a,u) = #{t ∈ 類: ∀m, a − 4g0²t² − ut ∈ QR(m)} であり、
   min_m count_m ではない（法ごとに通過行集合が異なる）。
   単一法 classMax < 17（K0797）は 1 法証明書の特別例。
2. **joint 全滅**: g3 形 size 29（w=85..87）は法対 {19,23} で、size 30..38
   （w=88..114）は {19,23,29,31} で全 (a,u) が J ≤ 16。K0797 の「g3壁」は
   単一法解析のアーティファクトだった。他の全 g0 形は w ≤ 132 まで単一法で有効。
3. **p-チェーン補題（無損失簡約）**: v ∈ QR(p^k) ⟹ v ∈ QR(p^j)（j<k）。
   法リストは各素数の最大冪のみに簡約できる。K0797 の 33 法のうち
   5,7,8,9,11,13,16,17,25,27,32,49,64,81 は冗長。簡約後 34 個の互いに素な
   最大冪集合 {19,23,29,31,37,41,43,47,53,...,139,121,125,128,169,243,289,343}。

## 意味論（過大主張の防止）

- 「level 17 全滅 ⟹ P(w) ≤ 32」の**非標準形側の前提**が w ≤ 114 で正当化。
  **P(w) の値は決定していない**（標準形 DFS は別件）。
- K0785（P(83) ≥ 34）により level 17 extinction は w ≥ 83 で偽。P(w) への
  実務的寄与は w ≤ 82 で尽きる。本結果の価値は方法論的:
  合同証明書の到達限界精密化・法リスト冗長性・K0797 限界記述の訂正。

## 証明の骨格

- coprime 法集合のもと (a,u) は法ごとに独立（CRT）。DFS で法を 1 個ずつ追加し
  survivor（部分 (a,u) クラス × 生き残り行ビットマスク）を枝刈り。
- 3 経路独立検証: DFS・BFS（走査順不同）・size 29 はビットマスク無しの
  直接 QR ブルートフォース（437² = 190,969 対・max = 16 @ (0,77)）が一致。
- 制御: K0797 既知値再現（s27: 16@343・s28: 16・s29: 17@31）・
  K0797 失敗 witness (0,1)@31 の 17 行生存再現（単一法解析が実生存を測っていた
  ことの確認）・cm49 ≡ cm343 = [16,16,17]。

## 限界

- **g3 size 39..44（w=115..132）は open**（DFS 予算 120M/25M nodes・depth 6 到達で
  未解決）。深い素数冪（361, 529, 841, 961）や meet-in-the-middle が延伸候補。
- 標準形 level 17 DFS のコストは不変（長期レーン）。

## resume

1. g3 size 39..44 の joint 延伸（深い素数冪・pairwise meet-in-the-middle）。
2. 標準形 level 17 DFS キャンペーン（w=65..72・前提は w ≤ 114 まで強化済み）。
3. K0797 への更新注記（本項目が限界記述を訂正）。
