---
id: K0932
title: t=3・q=3w−3純ファイバーゲームの全安全局面Grundy分類
kind: proposition
status: proved
topics: [variants, grundy]
aliases: []
relations:
- type: depends_on
  target: K0832
  note: 垂直ファイバーの厳密占有縮約と飽和鎖分離を用いる。底面跡制約なしの純ファイバー部分族。
artifacts:
- path: research/experiments/vertical-fiber-t3-q3w-minus3-grundy-20261118/report.md
  role: proof
  note: 偶奇高さの残余Grundy閉形式、境界全列挙、強帰納証明
- path: research/experiments/vertical-fiber-t3-q3w-minus3-grundy-20261118/verify_t3_q3w_minus3.py
  role: verifier
  note: 残余mexとラベル付き・正準盤面再帰の独立照合
- path: research/experiments/vertical-fiber-t3-q3w-minus3-grundy-20261118/output/audit.json
  role: data
  note: 残余61,560状態、盤面67,015状態/方式、最大値32組。不一致0。
- path: research/log/2026-11-18-vertical-fiber-t3-q3w-minus3.md
  role: log
  note: 最新main・既存K0832/K0930との照合、境界反例、証明・監査・次課題
scope: >-
  底面跡制約なし、ファイバー数w>=2、高さm>=1、次数閾値t=3、禁止点数q=3w-3の純ファイバーゲーム。全安全占有ベクトルのGrundy値を分類する。
evidence: >-
  m>=3では飽和ファイバーの残り鎖をXOR分離し、未飽和占有数0,1,2の個数(e0,e1,e2)に縮約する。L=3e0+2e1+e2>=4。奇数mはH=(L-4) mod 2。偶数mはL=4..7の境界表とL>=8のH=e1 mod 2をL強帰納で証明する。m=1,2は独立鎖または固定終局長で別処理する。有限監査は残余61,560状態と盤面67,015状態/方式、最大値32組で不一致0だが、全称性の根拠は残余再帰と帰納証明である。
date: 2026-11-18
tags: [vertical-fiber, t3, q3w-minus3, grundy, universal-proof]
---

# K0932：t=3・q=3w−3の全Grundy分類

## 命題・範囲

底面跡制約なし、\(w\ge2,m\ge1\)、\(t=3\)、\(q=3w-3\) の純ファイバーゲームを扱う。安全条件は
\[
\sum_i\min(c_i,3)\le3w-4.
\]
全安全占有ベクトルのGrundy値は、対応する証明報告の閉形式で完全に決まる。

## 現在の根拠と限界

飽和鎖分離と残余mex再帰に基づく全称証明。有限監査は二方式の盤面再帰と偶奇残余再帰の照合であり、全称性そのものとは区別する。底面跡制約付きの部分族、標準二次元共円ゲーム、固定幅安定化長には結論を拡張しない。