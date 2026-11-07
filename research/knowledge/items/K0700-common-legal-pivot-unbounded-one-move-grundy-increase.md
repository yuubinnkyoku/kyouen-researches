---
id: K0700
title: 共通合法点を持つ有限整数盤で通常値1から一手で2の任意冪へ増加し、値0からの増加も非有界
kind: proposition
status: proved
topics: [grundy, residual-games, geometry, variants]
aliases: []
relations:
- type: depends_on
  target: K0692
  note: 共通pivot付き二点辺の通常値閉形式で一手前g1を確定
- type: depends_on
  target: K0683
  note: 純三点族を一辺一占有アンカーの有限整数点盤へ実現
- type: depends_on
  target: K0108
  note: 残余ゲーム同型と自由点の通常xor則
artifacts:
- path: research/experiments/common-pivot-unbounded-one-move-jump-20261108/proof.md
  role: proof
  note: 既知コグラフ構成への帰属・再証明、初期値1、無界増加、整数盤サイズ公式
- path: research/experiments/common-pivot-unbounded-one-move-jump-20261108/verify.py
  role: verifier
  note: 記号option集合・別グラフ再帰・生subset・整数座標の四点組を比較
- path: research/experiments/common-pivot-unbounded-one-move-jump-20261108/output/audit.json
  role: certificate
  note: k0..3のグラフとk1/2の一手前後・1764安全状態、6/34点の整数盤
- path: research/experiments/common-pivot-unbounded-one-move-jump-20261108/output/audit_with_free.json
  role: certificate
  note: 自由点付きも含む6/7/34/35点の具体的整数盤と全共円四点組
- path: research/log/2026-11-08-cograph-geometric-unbounded-gaps.md
  role: log
  note: 完全核表から既知グラフ構成の幾何学的帰結へ移った経緯
scope: q4完全指摘通常プレイ。指定安全占有を持つ有限整数点盤。全禁止四点組が一つの合法点cを共有し、初期残余辺は全て三点。盤はkに依存して増大する。標準全正方形格子盤と空盤開始は含まない。
evidence: Bodlaender–Kratschの既知コグラフHkを再証明し、リンクグラフの子値集合とK0692で初期g1を導出。K0683による全kの整数実現。有限監査では二つのゲーム実装と四つの整数座標盤が一致。
---

任意k≥1について、有限整数点盤と安全局面S、合法点cが存在して

\[
g(S)=1,\qquad g(S\cup\{c\})=2^k.
\]

全共円・共線禁止四点組はcを共有し、初期の全極小残余辺は三点集合である。
合法点数は3^k+1、占有アンカー数はE_k=3^(k−1)(3^k−1)、
総盤点数は3^k+1+E_k。
自由点一個を加えた族では初期g=0、一手後g=2^k+1。
従って通常値0または1から、一手での上昇量を任意に大きくできる。

リンクは既知のコグラフH_0=K_1、H_k=(H_{k−1}⊔H_{k−1})∨H_{k−1}。
子値集合は正確に0..2^k−1で、g(H_k)=2^k。
外側への初手値はK0692の閉形式から0と2だけになり、
全初手値集合{0,2,2^k}のmexが1と決まる。
根のg≤3という制約は、子のgを一様には制限しない。

グラフ構成は[既存論文の補題21](https://webdoc.sub.gwdg.de/ebook/serien/ah/UU-CS/2000-42.pdf)に基づく。
その非有界性を新発見とは主張しない。
[帰属・全称証明・サイズ公式・再現資料](../../experiments/common-pivot-unbounded-one-move-jump-20261108/proof.md)を保存した。
有限計算からの外挿ではなく、帰納と幾何実現による無限族の証明である。
標準全正方形盤での非有界性K0327、ミゼール補助値の非有界性K0696、盤サイズの最小性は未確定のまま。
