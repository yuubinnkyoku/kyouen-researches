# five-row-q5-m24-class-split-20261115

IN FLIGHT (claim) — 高速レーン。`four-six-row-q4-q5-witness-search-20261114`（前レーン）と
`four-six-row-q4-q5-band-extension-20261115`（同族バンド延伸レーン）が残した (5,5) 前線
**5×24** を K0821/K0834 プロトコル（row-mirror 正準 19 クラスの class-split SAT・
k × minpos 完全分解）で解決する。

- 実行方針: sat3.js（five-row-q7-m22-class-split-20261114/scripts/ と同一機・byte-identical）
  + kissat 4.0.4 official prebuilt linux-amd64（md5 3a5eba830aa6008a604fcc9bbe99a325・不変）。
  19 正準クラスを 260s 予算で sweep し、INDET クラスは krow(k=0..3) 分解・
  k=3 は minpos=0..11（m=24 の音牢 H 分割: 左端石列 P、`min(x1,23-xk) <= 11`）で完全分解。
  SAT なら witness を js verifyConfig + Python Fraction の 2 系統検証し下界更新、
  全 UNSAT なら witness-free 幅 24 を記録（不在主張は m=24 限り）。
- 制御: 5×23 q=5 class-split 陽性対照（m=23 witness 再発見）・
  既知閾値 kissat コントロール（(3,4) m=23 SAT 66,895 bit-exact 等）。
- 較正: sat3 ≡ sat2 DIMACS バイト一致対照（(5,23,5)/(5,24,5 rowY=0) は前レーン較正済みの同一機）。

着手時点の境界（main 38b0dcda 時点）:

| family | 現在 | 前線 | 上界 |
|---|---|---|---|
| (5,5) | witness 帯 m=5..23・M ∈ [24, 336] | m=24（def-mode OR 90s/699k INDET のみ） | K0318 U=336 |

## スコープ

有限機械検証まで。SAT はその幅の欠損極大安全配置の存在証明（witness 有限証拠）。
INDET は cap 到達であり不在を意味しない。上界（K0318 substitution）は不変。
