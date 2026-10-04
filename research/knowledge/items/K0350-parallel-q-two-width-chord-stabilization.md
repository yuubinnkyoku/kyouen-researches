---
id: K0350
title: 任意のw本の平行線のq=2w版は同和弦energyで満容量安定化する
kind: proposition
status: proved
topics: [rectangles, geometry, variants, grundy]
aliases: []
relations:
- type: depends_on
  target: K0342
  note: 外部行対の同和弦予算の鋭い上界E_r
- type: generalizes
  target: K0070
  note: w=3,q=6の十分長さ21を任意の平行線・実数候補座標で保証。真の値9は一般化しない
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
