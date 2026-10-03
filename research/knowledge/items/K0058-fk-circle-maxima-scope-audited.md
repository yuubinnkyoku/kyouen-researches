---
id: K0058
title: F-Kの最大円点数表は半整数中心走査としてのみ採用する
kind: verification
status: verified
topics:
- geometry
- provenance
aliases:
- F-K
relations: []
artifacts:
- path: research/findings.md
  role: source
  note: F-Kの原記述と最大円点数表
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/analysis/explore_circle_formula_and_collinear.py
  role: solver
  note: 倍化中心i2,j2を整数走査する実装で、中心は半整数格子に限られる
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round4-circle-windows.md
  role: source
  note: 一般有理中心を含む後続の円窓解析
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
evidence: explore_circle_formula_and_collinear.pyのmax_circle_points_for_boardはcenter_x2,center_y2を整数で走査するため、中心座標は1/2刻みに限定される。
---

# F-Kの最大円点数表は半整数中心走査としてのみ採用する

F-Kは有限盤上の「最大円点数」を述べていたが、再現スクリプトの中心走査は倍化座標 i2,j2 を整数で動かす方式であり、扱う中心は整数・半整数中心に限られる。任意の有理中心を全列挙する探索ではない。

したがって、F-Kの数値表は**その走査族における最大値**としては資料に残すが、「全ての円を通じた有限盤上の最大値」としては採用しない。F-K本文内にもn=8..24で16という例示とn=8..11で12という列の不一致があり、元記述の全称的な読み方には追加根拠が必要である。

後続の `round4-circle-windows.md` は一般有理中心を含む円上格子点の窓スペクトルを解析しているが、F-Kのn=2..31最大値表を全有理中心について再証明するものではない。ここでの監査結論は確定しており、残る「真の有限盤最大円点数」の問題とは分離する。
