---
id: K0058
title: F-K旧走査は半整数中心に限定、n≤112の全中心最大値は後続計算で確定
kind: verification
status: verified
topics:
- geometry
- provenance
aliases:
- F-K
relations:
- type: depends_on
  target: K0307
  note: n≤112の全中心最大値は後続完全計算を参照
artifacts:
- path: research/archive/hypothesis-ledgers/findings.md
  role: source
  note: F-Kの原記述と最大円点数表
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/analysis/explore_circle_formula_and_collinear.py
  role: solver
  note: 倍化中心i2,j2を整数走査する実装で、中心は半整数格子に限られる
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/reports/round4-circle-windows.md
  role: source
  note: 一般有理中心を含む後続の円窓解析
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/geometry/reports/theory-audit-20261003.md
  role: source
  note: 後続の全中心n=2..112完全計算は旧走査とは別の根拠
evidence: explore_circle_formula_and_collinear.pyのmax_circle_points_for_boardはcenter_x2,center_y2を整数で走査するため、中心座標は1/2刻みに限定される。
---

# F-K旧走査は半整数中心に限定、n≤112の全中心最大値は後続計算で確定

旧F-Kの再現スクリプトは倍化中心座標を整数走査するため、半整数中心に限る。この旧走査だけでは任意の円を対象とする有限盤最大値の根拠にならない。

後続の全中心アンカー列挙により、n=2..112の真の最大値はK0307で完全計算された。n=8..11は12点、n=12..24は16点であり、F-Kの旧「8..24で16」という例示は誤りである。

旧artifactの走査範囲に関する監査は有効なまま保持する。n≤112はもはや未解決ではなく、全nへの最大点数公式や幅17..31の無限帯等号は後続有限結果を越える問題である。
