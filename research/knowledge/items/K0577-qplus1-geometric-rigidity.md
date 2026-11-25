---
id: K0577
title: 平面上のq+1点では共円・共線の禁止q点組数は0・1・q+1のみで全局面Grundy値は偶奇で決まる
kind: proposition
status: proved
topics: [geometry, variants, grundy, first-moves, maximal-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0576
  note: 余補一型の抽象禁止集合族の閉公式。幾何によって禁止組数を0・1・Nに制限する
- type: depends_on
  target: K0002
  note: 通常・misèreのmex定義
artifacts:
- path: research/experiments/qplus1-geometric-rigidity-20261031/proof.md
  role: proof
  note: 3点共有の直線・円の一意性、全局面偶奇則、整数格子の三構成の無界証明
- path: research/experiments/qplus1-geometric-rigidity-20261031/verify_geometry.py
  role: verifier
  note: 4×4格子の全12376個の5点・6点集合の整数行列式検査、q=4..10の三構成
scope: 実平面の相異なるN=q+1点、q≥4、共円または共線q点組禁止、全安全局面の通常・misère
evidence: 異なる二つの禁止q点組の共通q−1≥3点による幾何学的全称証明。4×4整数格子の全12376点集合を行列式検算し、q=4..10の三構成を確認。
---

# 平面q+1点の共円・共線禁止ゲームの全局面偶奇則

相異なるN=q+1個（q≥4）の実平面点からq点が同一直線または同一円に載る組を禁止すると、禁止組数fは**0・1・N**のいずれかに限られる。どのfも全q≥4で整数格子上に実現できる。

全安全局面Sの終局石数は、f=0ならL=N、f=1ならL=N−1、f=NならL=N−2に固定される。通常Grundy値はg(S)=(L−|S|) mod2、misère補助値はh(S)=1−g(S)。すべての合法初手は通常版で同じ勝敗分類になり、misèreでは逆転する。

証明は、異なる二つの禁止q点組がq−1≥3点を共有するため同じ直線・円上にあり、和集合である全N点もその曲線上に載ることによる。数学的全称証明と三つの整数格子構成はproof.mdを参照。

4×4格子の全5点組4368件（q=4）・全6点組8008件（q=5）の整数行列式検査で、f=0,1,N以外は0件。q=4..10の整数構成も検算済み。

この定理は総点数がちょうどq+1の盤に限る。大きな盤の任意の残余q+1合法点への無条件適用はしない。
