---
id: K0406
title: 一高列と単位容量短列からなる全上位hゲームのGrundy値
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
  note: 上位h終局分類を共有
artifacts:
- path: research/experiments/capacity-unequal-one-tall-all-h-20261010/README.md
  role: proof
  note: 任意hの全Grundy値の証明
- path: research/experiments/capacity-unequal-one-tall-all-h-20261010/verify_one_tall_full.py
  role: verifier
  note: ラベル付き・商状態の独立mex
- path: research/experiments/capacity-unequal-one-tall-all-h-20261010/audit.json
  role: data
  note: 有限監査digest
scope: h>=2,r>=h,k>=h−1の容量(r,1^k)上位hゲーム
evidence: 全パラメータの閉形式Grundy証明と独立直接mex監査。
---

容量 `(r,1,...,1)` の抽象ゲームで上位h列占有数和をr以下とする。`h>=2`, `r>=h`, 短列数k>=h−1。高列占有ell、使用短列数aについて `b=h−1`, `u=k−b`, `T=r+u`, `E(a)=r−2b+1+a` と置く。

u偶数なら `g(ell,a)=(r−ell−a) mod2`。u奇数ならa>=bで `g=(T−ell−a) mod2`。a<bでは `ell=E(a)` でg=2、ell<E(a)なら `(E(a)−ell) mod2`、ell>E(a)なら `(r−ell−a) mod2`。E(a)<0なら例外点はない。全安全局面でg<=2、値2はu奇数の場合かつその場合に限り実現する。終局石数集合は `{r,T}`。

短列の交換可能性で二変数状態へ商を取り、領域ごとにmex帰納する。有限直接mex監査は補助検証。標準二次元盤全体への一般化ではない。
