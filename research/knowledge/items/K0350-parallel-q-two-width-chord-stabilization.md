---
id: K0350
title: 任意のw本の平行線のq=2w版は同和弦energyで満容量安定化する
kind: proposition
status: proved
topics:
- rectangles
- geometry
- variants
- grundy
aliases: []
relations:
- type: depends_on
  target: K0342
  note: 外部行対の同和弦予算の鋭い上界E_r
- type: supports
  target: K0331
  note: 標準五行の八点円の四行構造と組合せて全称末尾101、必要有限証明255件を得る
artifacts:
- path: research/experiments/q58-chord-tail-20261005/proof.md
  role: proof
  note: 任意平行線q=2wの全称上界と標準五行q8の末尾101
- path: research/experiments/q58-chord-tail-20261005/scripts/reduce_manifest.py
  role: verifier
  note: 旧510件の独立検査receiptに照合して255件のCNFを再生成・hash確認
- path: research/experiments/q58-chord-tail-20261005/output/reduced-manifest.json
  role: manifest
  note: 既存独立DRAT検査済みm16..100の255件を抽出。SATを新実行した記録ではない
- path: research/experiments/three-parallel-q6-17-20261018/proof.md
  role: proof
  note: 三平行線q6の任意実数候補で17点十分。四円同時通過の組合せ必要条件と有限正規形検査
- path: research/experiments/three-parallel-q6-17-20261018/verify.py
  role: verifier
  note: 混合型182候補と例外四円組のPython整数完全列挙
- path: research/experiments/three-parallel-q6-17-20261018/audit_independent.cpp
  role: verifier
  note: 独立C++整数完全列挙
- path: research/experiments/three-parallel-q6-17-20261018/verify_e13.py
  role: verifier
  note: E13の5005個の等差正規形、3族の記号候補、有理数候補のPython完全検査
- path: research/experiments/three-parallel-q6-17-20261018/audit_e13_independent.cpp
  role: verifier
  note: E13の独立C++完全検査
- path: research/experiments/three-parallel-lines-q6-20261018/proof.md
  role: proof
  note: 二点和衝突の16上界と任意配置の21候補点定理の全称証明
- path: research/experiments/three-parallel-lines-q6-20261018/verify.py
  role: verifier
  note: 整数行列式による独立幾何監査と二点和上界検算
- path: research/experiments/three-parallel-lines-q6-20261018/results.json
  role: data
  note: 252集合・63504組・36盤・324局面の有限監査結果
- path: research/experiments/three-parallel-q6-19-20261018/proof.md
  role: proof
  note: 任意三平行線q6の21から19への改善、有限記号帰着による全称証明
- path: research/experiments/three-parallel-q6-19-20261018/verify.py
  role: verifier
  note: 16円の1820四組を有理数で全検査、弦energyの有限標本監査
- path: research/experiments/three-parallel-q6-19-20261018/audit_independent.cpp
  role: verifier
  note: 1820四組の独立した整数演算による全検査
- path: research/experiments/three-parallel-q6-19-20261018/audit.json
  role: data
  note: Python検証器の実行結果
scope: w≥3本の任意の平行直線上に各m個の異なる候補点、q=2wの円・直線禁止通常プレイ。
evidence: 弦対充填の全称証明。q8五行の有限部分は既存の独立検査済み証明を再利用。
---


# 任意のw本の平行線のq=2w版は同和弦energyで満容量安定化する

w≥3、q=2w、r=2w−1とし、各行にm個の任意の異なる候補実数座標を置く。
同和弦energyの鋭い上界をE_rとすると、`m≥r+E_r` なら全極大安全配置はwr石になり、
全安全局面で `g(S)=(wr−|S|) mod2`。

不足対象行を塞ぐ円は対象行一石と各外部行二石を持つ。
外部の `C(w−1,2)` 個の同和弦対を使い、全予算は `C(w−1,2)E_r`。
従ってその円はE_r本以下で、占有点込みの利用不能点はr−1+E_r点以下。

w=3,q=6で十分長さ21、w=4,q=8で十分長さ54を与える。
既知の標準整数格子の真の値9と11を、任意平行線へ拡張したとは主張しない。
標準q=2w,w≥5ではK0072の分離定理がさらに強い。

別の帰結として標準五行q8は八点円が四行に二点ずつなので、外部三弦の充填で全称末尾101を得る。
既存M5,8=16の証明に必要な有限排除はm16..100の255件へ減り、旧510件の検査済み証拠から再利用できる。

## 2026-10-20 追加資料の監査境界

添付に任意三平行線の21候補の再証明、および19・17候補への改善案がある。今回の統合では全称証明の監査を完了していないため、改善値は未採用（needs-review）。上記の既存21候補十分という結論を維持する。原文と各版は取込元ZIPおよび統合manifestで追跡できる。

追加の同一命題資料: `K0441-three-arbitrary-parallel-lines-q6-21-sites.md`。詳細と独立証人・検算範囲は追加artifactを参照。原文は取込元ZIPに保存。
