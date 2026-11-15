# anchored window-SAT 導入 — 作業記録 2026-11-15

高速レーン(共円・固定幅)の1セッション記録。

## 経緯・判断

- 目標は (8,9) 帯の frontier 8x29(M_{8,9} ∈ [29,984]、witness 帯 8x9..8x28)。
  環境に kissat/gcc/git が無く(node22 + python3 stdlib のみ)、
  純JS CDCL fastsat(~1k conflicts/s)では全幅 def-mode は 230s INDET の
  kissat に遠く及ばないと判断。
- 前回の診断から: m=27/28 witness の空列append + 1-2手surgery は全失敗。
  m=29 右端セル (28,3) を通るcensus曲線は5本のみ(円4本 {1,1,1,3}石 + 行3 7石)で、
  blocking circle(8石)への到達は構造的に遠い。→ 局所surgeryではなく
  「凍結prefix + 自由window」で系統的に掃く方法を導入した
  (anchored window-SAT、`anchored-window-sat-frontiers-20261115`)。
- 3つの前線に適用: (8,9) 8x29(主対象)、(4,5) 4x21、(5,5) 5x24(後二者は
  band-extension レーンの掃引宣言と重複しないよう window-scan のみに限定)。
- 判定の区別: window UNSAT = 条件付き局所閉包(不在主張ではない)。
  vacuity check を全实例に付し、今回の全实例は non-vacuous。
  正制御(w4x20/w5x23 の既知witness再発見、js+py 2系統検証)で
  pipeline を較正してから本番を実施。

## 得られたもの

- (8,9) 8x29: w28 anchor × off{0,±1} × window1..8列の8实例全UNSAT
  (各~130-160 conflicts)。+1列append を含む「列0..27 一致」witness は不存在。
- (4,5) 4x21: 75实例全UNSAT(w16..w20 anchors、自由最大10列)。
- (5,5) 5x24: 60实例全UNSAT(w22/w23 anchors、自由最大6列)。
- honest negative: fastsat は (4,5) m=20 既知SATクラスさえ 60s で解けない
  (42-51k conflicts)。全幅class-split掃引はこの環境外。

## 失敗・未達

- 8x29 の決着(SAT/UNSAT)には到達せず。次候補: SA witness search の q=9 移植、
  w27/w26 anchors の window(def-mode base)。
- (8,9) class-split に必要な「行ちょうどk石」符号化(totalizer 逆利用)は
  `classsplit.js` として実装したが、fastsat の速度でrunning cost が合わず
  本番掃引は断念(制御のみ記録)。

## 引き継ぎ

- 実験dir `research/experiments/anchored-window-sat-frontiers-20261115/`
  (README に方法・較正・非重複方針・次の一手)。
- window-SAT は他ファミリーの前線にもそのまま使える安価な条件付け
  (实例あたり< 1s)。ただし結果は常に「凍結prefix条件付き」であることと、
  vacuity check を省かないことを守る。
