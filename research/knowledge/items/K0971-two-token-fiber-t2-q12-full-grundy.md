---
id: K0971
title: t=2・q=12純ファイバーゲームの全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [t=2 q=12 pure-fiber all-Grundy classification]
relations:
- type: depends_on
  target: K0832
  note: 飽和鎖分離、残余ゲームへの縮約、一般最大値定理を使用する
artifacts:
- path: research/experiments/vertical-fiber-t2-q12-grundy-20261118/report.md
  role: proof
  note: 全幅・全高さの全Grundy分類、650セル表、切り詰め補題、最大値の系
- path: research/experiments/vertical-fiber-t2-q12-grundy-20261118/verify_t2_q12.py
  role: verifier
  note: 表・残余再帰・正準状態・ラベル付き状態の独立再帰mex監査
- path: research/experiments/vertical-fiber-t2-q12-grundy-20261118/output/audit.json
  role: data
  note: 72,009正準状態、54,225ラベル状態、240,000残余照合、R<=256の有限規則走査
- path: research/log/2026-11-18-vertical-fiber-t2-q12-grundy.md
  role: log
  note: 最新main・既存q=8..11成果との重複確認、q=12分類の証明・監査・限界
scope: >-
  底面跡制約なし・次数上限t=2・禁止点数q=12の純ファイバーゲーム。
  全幅w>=1、全高さm>=2、全安全占有局面のGrundy値を分類する。
evidence: >-
  飽和ファイバー鎖をXOR分離し、偶数高さは固定終局手数、奇数高さは
  H1(e,ell,R)=H1(min(e,R),min(ell,R),R) の切り詰め補題でR<=11の
  650セル完全表へ縮約する。独立有限監査は正準72,009状態・ラベル54,225状態、
  残余240,000照合で不一致0。全称性は有限標本ではなく分離・補題・完全表による。
---
## 命題

安全条件は \(\sum_b\min(c_b,2)\le11\)。飽和ファイバー数 \(s\)、単独石ファイバー数 \(\ell\)、空ファイバー数 \(e\)、残余容量 \(R=11-2s-\ell\) とし、飽和鎖のGrundy XORを \(X\) とする。全安全局面で

\[
G(c)=X\oplus H_{m\bmod2}(e,\ell,R)
\]

が成立する。偶数高さでは \(H_0=\min(R,2e+\ell)\bmod2\)。奇数高さでは \(R\le11\) の650セル完全表で全値が決まる。全表・証明・監査はartifactの証明報告を参照。

最大Grundy値は奇数高さかつ幅7以上で3、それ以外で1。この最大値条件はK0832の一般定理の特殊化であり、本項の新規部分はq=12の全局面分類である。

\(R\le256\) の有限走査では値2位置に簡潔な規則候補が現れたが、全 \(R\) の定理には昇格させていない。
