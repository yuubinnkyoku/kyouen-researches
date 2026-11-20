# 2026-11-20 six-row q5/q6 frontier — 単一オーナー宣言（高速レーン）

- 2026-11-20 13:25Z: (6,5) 6×20・(6,6) 6×16 の行欠損極大 SAT 前線掃引
  （sat2.js def-mode + kissat 4.0.4・rowY 分割含む・延伸幅含む）を
  research/experiments/six-row-q5-q6-frontier-20261120 で着手する。
  repo検索（README・log・experiments・直近commits）時点で未着手・未宣言を確認。
  他レーンは 4×22（m22 batchD/E・four-row-q5-m22-class-split）を所有中であり、
  本レーンはそれに触れない。
- 現在の境界: M_{6,5} ∈ [20, 658]（K0808・U=658 は K0318 代入）・
  M_{6,6} ∈ [16, 495]。
- 着手時点の観測最大K番号: K1145（最終K番号はpush直前に3点確認で採番）。
