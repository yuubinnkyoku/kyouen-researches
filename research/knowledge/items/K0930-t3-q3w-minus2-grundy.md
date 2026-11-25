---
id: K0930
title: t=3・q=3w−2純ファイバーゲームの全安全局面Grundy分類
kind: proposition
status: proved
topics: [variants, grundy]
aliases: []
relations:
- type: depends_on
  target: K0832
  note: 厳密占有縮約と飽和ファイバー鎖分離を用いる。対象は底面跡制約なしの純ファイバーゲーム。
artifacts:
- path: research/experiments/vertical-fiber-t3-q3w-minus2-grundy-20261118/report.md
  role: proof
  note: 残余三変数再帰、偶奇高さの閉形式、全場合表による強帰納証明
- path: research/experiments/vertical-fiber-t3-q3w-minus2-grundy-20261118/verify_t3_q3w_minus2.py
  role: verifier
  note: 偶数・奇数残余mexとラベル付き・正準盤面再帰の独立照合
- path: research/experiments/vertical-fiber-t3-q3w-minus2-grundy-20261118/output/audit.json
  role: data
  note: 残余71,866状態・盤面51,756状態、計123,622照合。不一致0、二回実行byte-identical
- path: research/log/2026-11-18-vertical-fiber-t3-q3w-minus2.md
  role: log
  note: 最新main・既存境界結果との照合、証明・監査・限界
scope: >-
  底面跡制約なし、ファイバー数w>=1、高さm>=1、次数閾値t=3、禁止点数q=3w-2の純ファイバーゲーム。全安全占有ベクトルのGrundy値を分類する。
evidence: >-
  m>=3では飽和ファイバーの残り鎖をXOR分離し、未飽和占有数0,1,2の個数(e0,e1,e2)へ縮約する。安全性はL=3e0+2e1+e2>=3と同値。m奇数は全残余プレイ長L-3からH=(L-3) mod 2。m偶数は残余mex再帰の全場合表（e0=0、e0=1、e0>=2とe2-e0の分割）を用い、閉形式をL強帰納で証明する。m=1,2は独立鎖または固定終局長で別処理する。有限監査は残余71,866状態と盤面51,756状態の計123,622照合で不一致0だが、全称性の根拠は再帰表と強帰納である。
date: 2026-11-18
tags: [vertical-fiber, t3, q3w-minus2, grundy, universal-proof]
---

# K0930: t=3・q=3w−2の全Grundy分類

## 命題・範囲

底面跡制約なし、\(w\ge1,m\ge1\)、\(t=3\)、\(q=3w-2\) の純ファイバーゲームを扱う。安全条件は
\[
\sum_i\min(c_i,3)\le3w-3.
\]
全安全占有ベクトルのGrundy値は、証明記録の閉形式で完全に決まる。

## 現在の根拠と限界

飽和鎖分離と残余mex再帰に基づく全称証明。有限監査は二つの盤面再帰と偶奇残余再帰の照合であり、全称性そのものとは区別する。底面跡制約付きの部分族、標準二次元共円ゲーム、固定幅安定化長には結論を拡張しない。
