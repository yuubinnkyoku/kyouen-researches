---
id: K0769
title: 形状クラスCNFのモデル集合は完全対の仮定 B_d で互いに素に分割され、全 d の UNSAT はクラス UNSAT と同値
kind: proposition
status: proved
topics: [geometry, maximum-safe, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0712
  note: 固定原点・一完全対の還元
- type: depends_on
  target: K0771
  note: 辺リスト完全性（前提(1)）
- type: depends_on
  target: K0770
  note: 捨て規則 (ii) の和条件（前提(2)）
- type: depends_on
  target: K0772
  note: 基数符号化の範囲限定検証（前提(3)）
artifacts:
- path: research/log/2026-11-10-a2647-113-candidate-b-proof-omp.md
  role: proof
  note: 第1部の分割・健全性・完全性の証明と §1.7 の前提一覧。証明の記述であり Lean 形式化ではない
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/search_shape_class_assump.py
  role: solver
  note: assumption 掃引の実装（SAT 側は復号点を全 928,389 辺と照合）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/search_shape_class.py
  role: solver
  note: "#B = c の cardinality 制約と対ごと exactly-one の本体"
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w7-assump-2647-1322-full100k.json
  role: data
  note: 分割の適用記録 (1,323 d)
scope: c=1 の形状クラスCNF一般。分割と同値性は論理命題として述べ、ソルバ実行への応用は前提(4) に依存する部分を分離する。
evidence: 符号化定義からの論理的導出。前提(1)(2) は K0771/K0770 で証明済み、(3) は K0772 で範囲限定の検証済み。(4) は K0737 の未解決の問い。
---

## 命題

c=1 のクラス CNF は `#B = 1` と両立禁止節 `[-B_i,-B_j]` を持ち、任意のモデルで
真となる B 変数はちょうど 1 つ存在する。したがってモデル集合は
`M_d = {M ⊨ CNF : B_d}` により `M_1,…,M_h` へ互いに素に分割され、
`CNF = ⋁_d (CNF ∧ B_d)`。よって決定的な（UNKNOWN を返さない）ソルバ呼び出しの下で、
「すべての d∈{1..h} で CNF ∧ B_d が UNSAT」⇔「CNF が UNSAT」。

健全性は assumption が一時的な単位節追加にすぎないことから従う。
SAT 側の主張は復号した点集合を生成済み全 928,389 辺と直接照合する自己検証を持つ
（符号化の健全性に依存しない）。c=0 では分割が空になり、掃引は
`assumptions=[]` の 1 クエリ = クラスCNF そのもの。
UNKNOWN が 1 つでも残る d 範囲については何も主張しない。

## 前提との切り分け

- 前提(4)（ソルバ健全性）はこの論理命題の一部ではないため `proved` を妨げないが、
  **応用（掃引の UNSAT からクラス UNSAT を出す段）は依然 assumption-UNSAT に依存する**。
- 捨て規則に関する同値の記述では、和 0 の四点集合が禁止四点集合より真に広い
  （p=17 で 140 対 30、p=43 で 2870 対 239）ため、「禁止 ⇒ 和 0」の **⇒ としてのみ** 述べる。
  双条件は偽である。
