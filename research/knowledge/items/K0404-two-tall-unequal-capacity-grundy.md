---
id: K0404
title: 異容量二高列上位2列ゲームの終局石数と完全Grundy公式
kind: proposition
status: proved
topics:
- variants
- grundy
- maximal-safe
- strategy-length
aliases: []
relations:
- type: depends_on
  target: K0403
  note: 上位2列終局分類を利用
artifacts:
- path: research/experiments/capacity-two-tall-20261010/README.md
  role: proof
  note: 終局分類・Grundy公式の全称証明
- path: research/experiments/capacity-two-tall-20261010/verify_labelled.py
  role: verifier
  note: ラベル付き状態の再帰mex
- path: research/experiments/capacity-two-tall-20261010/labelled-output.txt
  role: data
  note: ラベル付き監査
- path: research/experiments/capacity-two-tall-20261010/verify_quotient.py
  role: verifier
  note: 圧縮状態の独立逆順mex
- path: research/experiments/capacity-two-tall-20261010/quotient-output.txt
  role: data
  note: 圧縮監査
scope: 容量(r,s,1^k)の抽象上位2列制約ゲーム
evidence: 全パラメータ証明とラベル付き・圧縮状態の独立mex監査。
---

容量 `(r,s,1,...,1)`（`r>=2`, `1<=s<=r`, 短列数k>=1）の抽象列占有ゲームで上位2占有数和をr以下とする。終局石数集合は `{r,r+k}`、間のk−1サイズは全て欠番。

高列占有数をa,b、短列合計をt、総石数をNとする。`(a,b,t)=(r,0,0)`（s=rなら `(0,r,0)` も）でg=0。k奇数なら `(r−1,0,0)`（対称な場合も）でg=2。それ以外は `g=(r+k−N) mod2`。従って全局面g<=2、k偶数なら最大値1、奇数なら2。

全称証明は終局分類、共通終局サイズの偶奇、残る高列軸上のmex帰納による。ラベル付き・圧縮状態の2つの有限mex検査は独立監査。標準幾何盤への移送は主張しない。s=1の一高列族を含む。
