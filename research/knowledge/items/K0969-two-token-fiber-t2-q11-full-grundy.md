---
id: K0969
title: t=2・q=11純ファイバーゲームの全Grundy分類
kind: proposition
status: proved
topics: [variants, grundy, residual-games]
aliases: [pure fiber t2 q11 all-safe Grundy]
relations:
- type: depends_on
  target: K0832
  note: ファイバー占有縮約と飽和鎖分離を使う
- type: generalizes
  target: K0964
  note: 同じ純ファイバー族の禁止点数をq=10からq=11へ拡張する
artifacts:
- path: research/experiments/vertical-fiber-t2-q11-grundy-20261118/report.md
  role: proof
  note: 全幅・全高さのGrundy公式、奇数高さ残余表506セル、最大値の最小幅証明
- path: research/experiments/vertical-fiber-t2-q11-grundy-20261118/verify_t2_q11.py
  role: verifier
  note: 残余再帰・正準占有多重集合・ラベル付き占有ベクトルの独立照合
- path: research/experiments/vertical-fiber-t2-q11-grundy-20261118/output/audit.json
  role: data
  note: 56組・正準27,976状態・ラベル1,157,725状態・残余140,800照合、不一致0、2回byte-identical
- path: research/log/2026-11-18-vertical-fiber-t2-q11-grundy.md
  role: log
  note: q=10既存成果との差分、全称証明・独立監査・限界
scope: >-
  底面跡制約なしの純ファイバーゲーム。幅w>=1、高さm>=2、次数上限t=2、禁止点数q=11。安全条件はΣ_b min(c_b,2)<=10。
evidence: >-
  2石以上の各ファイバーを独立鎖として分離し、残余状態(e,ell,R)へ縮約。m偶数ではH_0=min(R,2e+ell) mod 2。m奇数ではR<=10によりe,ellをRで切り詰めた506セル表が全状態を覆う。紙上の切り詰め帰納と完全表で全称証明。最大Grundy値はm奇数かつw>=6で3、それ以外1。有限監査は正準27,976状態・ラベル1,157,725状態・残余140,800照合で不一致0、2回byte-identical。
---

## 命題・範囲

全ての安全占有ベクトルcのGrundy値は、証明報告の飽和鎖xorと残余値H_p(e,ell,R)の式で完全に決まる。特に

\[
\max G=3\iff(m\text{ が奇数かつ }w\ge6),
\]

それ以外では1である。値3の最小幅・高さは(w,m)=(6,3)、証人は(3,2,2,2,1,0)。

## 現在の根拠と限界

全称性はK0832の占有縮約、飽和鎖分離、偶数高さの固定終局手数、奇数高さの切り詰め補題と506セル表の完全性による。有限監査は幅1..8・高さ2..9の56組の正準状態27,976件、44組のラベル付き状態1,157,725件、残余直接照合140,800件で不一致0。有限監査は全称性の根拠ではなく、全称性は上記の数学的証明による。

本項目は底面跡制約なしの抽象純ファイバー族に限る。標準二次元盤の固定幅・q点安定化長や標準4×m・q=8の定理とは別問題である。
