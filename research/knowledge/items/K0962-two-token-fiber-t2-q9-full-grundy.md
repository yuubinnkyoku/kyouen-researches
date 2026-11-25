---
id: K0962
title: t=2・q=9純ファイバーゲームの全Grundy分類
kind: proposition
status: proved
topics: [variants, grundy, residual-games]
aliases: [pure fiber t2 q9 all-safe Grundy]
relations:
- type: depends_on
  target: K0832
  note: 各ファイバー次数上限2の厳密占有縮約と飽和鎖分離を使う
- type: generalizes
  target: K0957
  note: 同じ純ファイバー族の禁止点数をq=8からq=9へ拡張する
artifacts:
- path: research/experiments/vertical-fiber-t2-q9-grundy-20261118/report.md
  role: proof
  note: 全幅・全高さの閉形式、奇数高さ残余表285セルの切り詰め証明
- path: research/experiments/vertical-fiber-t2-q9-grundy-20261118/verify_t2_q9.py
  role: verifier
  note: 残余再帰・正準多重集合・ラベル付き占有ベクトルの三重照合
- path: research/experiments/vertical-fiber-t2-q9-grundy-20261118/output/audit.json
  role: data
  note: 56組・2,158,926ラベル状態・8,848正準状態、残余17,298照合、不一致0
- path: research/log/2026-11-18-vertical-fiber-t2-q9-grundy.md
  role: log
  note: q=8既存成果との重複確認、q=9全分類の証明・監査・限界
date: 2026-11-18
scope: >-
  底面跡制約なしの純ファイバーゲーム。幅w>=1、高さm>=2、次数上限t=2、禁止点数q=9。安全条件はΣ_b min(c_b,2)<=8。
evidence: >-
  2石以上の各ファイバーを独立鎖として分離し、残余状態(e,ell,R)へ縮約。m偶数ではH_0=min(R,2e+ell) mod 2。m奇数ではR<=8によりe,ellをRで切り詰めた285セル表が全状態を覆う。紙上の切り詰め帰納と完全表で全称証明。56パラメータ組の独立二方式監査は2,158,926ラベル状態・8,848正準状態・不一致0。
---

## 命題・範囲

全ての安全占有ベクトルcのGrundy値は、証明報告の飽和鎖xorと残余値H_p(e,ell,R)の式で完全に決まる。特に最大Grundy値は

\[
\max G=3\iff(m\text{ が奇数かつ }w\ge5),
\]

それ以外では1である。値3の最小幅・高さは(w,m)=(5,3)、証人は(3,3,2,1,0)。

## 現在の根拠と限界

全称性はK0832の占有縮約、飽和鎖分離、偶数高さの固定終局手数、奇数高さの残余表285セルの完全性による。有限監査は幅1..8・高さ2..8の56組、2,158,926ラベル状態と8,848正準状態、残余17,298照合で不一致0。有限監査は全称性の根拠ではなく、全称性は切り詰め補題と明示表による。

本項目は底面跡制約なしの抽象純ファイバーゲームに限る。標準二次元盤の固定幅・q点安定化長や標準4×m・q=8の定理とは別問題である。
