---
id: K0957
title: t=2・q=8純ファイバーゲームの全Grundy分類
kind: proposition
status: proved
topics: [variants, grundy, residual-games]
aliases: [pure fiber t2 q8 all-safe Grundy]
relations:
- type: depends_on
  target: K0832
  note: 各ファイバー次数上限2の厳密占有縮約と鎖分離を使う
artifacts:
- path: research/experiments/vertical-fiber-t2-q8-grundy-20261118/report.md
  role: proof
  note: 全幅・全高さの閉形式、奇数高さ残余表204セルの有限閉鎖証明
- path: research/experiments/vertical-fiber-t2-q8-grundy-20261118/verify_t2_q8.py
  role: verifier
  note: 残余再帰・正準多重集合・ラベル付き占有ベクトルの三重照合
- path: research/experiments/vertical-fiber-t2-q8-grundy-20261118/output/audit.json
  role: data
  note: 56組・833,819ラベル状態・5,383正準状態、残余7,056照合、不一致0
- path: research/log/2026-11-18-vertical-fiber-t2-q8-grundy.md
  role: log
  note: 既存q=3..7成果と標準4×m・q=8定理を区別し、q=8純ファイバー全分類を証明・監査した判断記録
scope: >-
  底面跡制約なしの純ファイバーゲーム。幅w>=1、高さm>=2、次数上限t=2、禁止点数q=8。安全条件はΣ_b min(c_b,2)<=7。
evidence: >-
  2石以上の各ファイバーを独立鎖として分離し、残余状態(e,ell,R)へ縮約。m偶数ではH_0=min(R,2e+ell) mod 2。m奇数ではR<=7によりe,ellをRで切り詰めた204セル表が全状態を覆う。紙上の切り詰め帰納と完全表で全称証明。56パラメータ組の独立二方式監査は833,819ラベル状態・5,383正準状態・不一致0。
---

## 命題・範囲

全ての安全占有ベクトル c のGrundy値は、証明報告の鎖xorと残余値 H_p(e,ell,R) の式で完全に決まる。特に最大Grundy値は

\[
\max G=3\iff (m\text{ が奇数かつ }w\ge5),
\]
それ以外では1である。値3の最小幅・高さは (w,m)=(5,3)、証人は (3,2,1,1,0)。

## 現在の根拠と限界

全称性はK0832の占有縮約、飽和鎖分離、偶数高さの固定終局手数、奇数高さの残余表204セルの完全性による。有限監査は幅1..8・高さ2..8の56組、833,819ラベル状態と5,383正準状態で不一致0。標準4×m・q=8の定理K0077とは別の抽象純ファイバー結果であり、標準二次元盤へ主張を移さない。
