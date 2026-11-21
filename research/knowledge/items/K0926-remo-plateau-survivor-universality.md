---
id: K0926
title: プラトー全称化 E6U、S(C,r) = S(C,C) = P(C)（すべての C >= 1, r >= C）。補題CAS（零石カスケード）と合流カップリングによる全称証明で、K0919 E6 の有限観察（C <= 24 機械）を解決し、P(C) を r 非依存の普遍関数として正当化。系として有界 witness 窓 [1,r-1] の生存者列は P(1..r-1) で、K0925 有界 witness 予想は窓形式「Q(r) の各真約数 d に対し C in [1,r-1] で S(C+d,r) != P(C) が存在」と同値。
kind: proposition
status: proved
topics: [variants, multiplayer, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0859
- type: depends_on
  target: K0919
- type: depends_on
  target: K0925
- type: related
  target: K0924
artifacts:
- path: research/experiments/remo-plateau-universality-20261117/report.md
  role: proof
  note: "K0919実験E6の有限観察「プラトー S(C,r) は r>=C で一定」を補題CAS（零石カスケード）と正準状態K_C合流により全称証明する実験レポート（定理E6U）"
- path: research/experiments/remo-plateau-universality-20261117/verify_plateau_universality.py
  role: verifier
  note: "補題CASと定理E6Uの機械検証器（stdlibのみ・決定的・--no-cacheで全再計算・r=2..40×C=1..r-1全数で違反0）"
- path: research/experiments/remo-plateau-universality-20261117/output/plateau_universality_audit.json
  role: data
  note: "監査正本（sha256 ef83446f…・4,748 bytes・pure ASCII・二重実行でbyte同一）"
date: 2026-11-17
tags: [remo, uniform-board, counting-recursion, survivor, plateau, universal-proof]
---

# K0926: プラトー全称化 E6U

K0859 定理Dの数え上げ再帰（一様盤・零リセット）の run (C,r) について、K0919 実験E6 は「プラトー S(C,r) は r >= C で一定」を C <= 24 の機械観察として残していた。本項目はこれを全称証明で解決する。

## 補題CAS（零石カスケード・全称・証明つき）

1 <= C <= r-1 の run (C,r) は、フェーズ1で石 C 個を P_0..P_{C-1} に1個ずつ配って敗者 P_C、フェーズ 2..r-C は ell=0 の零石カスケードで P_{C+1}..P_{r-1} を順に除去し（各フェーズで turn = C mod k = C が C < k により成立し li = C が上側の0石プレイヤーを指す）、フェーズ r-C の後に正準状態 K_C = (active=[0..C-1], 全石数1, 手番0) に到達する。C=1 は生存者 P_0 で即終端。機械検証: r=2..40 × C=1..r-1 全数で違反0。

## 定理E6U（全称・証明つき）

すべての C >= 1, r >= C に対して **S(C,r) = S(C,C) = P(C)**。

証明は合流カップリング: C <= r-1 のとき run (C,r) はフェーズ r-C で、run (C,r+1) はフェーズ r-C+1 で同一の正準状態 K_C に到達し（両カスケードはそれぞれ P_{C+1}..P_{r-1}、P_{C+1}..P_{r} を除去）、以降の展開は (active, counts, turn) のみで決まり同一。よって S(C,r) = S(C,r+1)、r に関する帰納で全 r >= C へ。機械検証: COUPLE r=2..60 × C=1..r-1 全数（合流状態と以降の (k,ell,li,loser) 列の完全一致）+ E6U r=2..60 × C <= min(r-1,40) 全数 + r in {61,97,128}。

## 系

1. P(C) は r 非依存の普遍関数として正当化され、C >= 2 で P(C) = 正準状態 K_C からの生存者という特徴づけを得る。P(1) = 0。
2. 有界 witness 窓 [1,r-1] の生存者列はちょうど P(1..r-1) であり、K0925 有界 witness 予想は「Q(r) の各真約数 d に対し C in [1,r-1] で S(C+d,r) != P(C) となるものが存在」と同値に書き直せる（r=2..24 全真約数で機械確認、WITCONN・欠落0。r <= 32 は K0925 wit_max_sv データから継承）。
3. Witness の値は d mod r 単独では決まらない（d=Q/m 型の h*=1 集中は K0925 どおりだが、一般の d に対する単純閉形式なし。本項目は閉形式を主張しない）。

## 検証

`verify_plateau_universality.py`（stdlibのみ・決定的）の6チェック PIN / CAS / COUPLE / E6U / TWIN / WITCONN 全合格。監査 `plateau_universality_audit.json` は二重実行（うち1回 --no-cache 全再計算）で byte 同一（sha256 `ef83446fd64ad65c4cfb307f13dae8e6b8c0e641872ffb89a13990134b0c5221`）。

## 限界

一様盤・零リセットの K0859 再帰限定（非一様盤には一切言及しない）。P(C) の閉形式は主張しない。有界 witness 予想・素数予想は未解決のまま。
