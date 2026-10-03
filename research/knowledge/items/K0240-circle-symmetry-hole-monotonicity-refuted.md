---
id: K0240
title: 円の対称群が大きいほど窓スペクトルの穴が増える単調性は偽
kind: proposition
status: refuted
topics:
- geometry
aliases:
- B468
relations: []
artifacts:
- path: research/verification/round4-circle-windows.md
  role: source
  note: 窓スペクトルの全分類定理と対称性単調性の反例
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round4_circle_windows.json
  role: data
  note: 反例円と窓スペクトルの厳密データ
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round4_circle_windows.py
  role: verifier
  note: 格子対称群と窓スペクトルの独立計算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B468の原文
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 円の対称群が大きいほど窓スペクトルの穴が増える単調性は偽

完全格子円Cの全格子点集合Pについて、整数位置の軸平行正方形窓で実現できる点数集合をA(P)とし、その穴数をH(P)とする。格子対称性をPを保つZ²の等長写像群の位数sで測る。

同じ完全点数m=12、同じ最小収容正方形幅D=21でも、中心(0,0)・半径二乗100の円はs=8で穴なし。一方、中心(1/2,0)・半径二乗425/4の円はs=4で穴{7,9,11}を持つ。より対称な円の方が穴が少ないため、「対称群が大きいほど穴が多い」という単調性は反証される。

一般分類では穴数は `H=(m/4)·1_E` と完全に記述でき、対称群位数だけでは決まらない。母集団を別途指定した統計的相関を研究することは可能だが、母集団未指定の「傾向」は正本の数学命題として残さない。
