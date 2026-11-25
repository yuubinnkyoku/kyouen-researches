# five-row-q6-m23-longcap-20261115

IN FLIGHT — 高速レーン。(5,6) 前線 **5×23** の残り class-split サブインスタンスを
拡張 cap で走査する（five-row-q6-m22-witness-20261115 の resume 継続）。

## 計画（このレーンが走査する範囲）

- class {0} krow=0:4 minpos=0..2: 前回 220s INDET（3,343,593 / 3,369,340 / 3,686,541 conflicts）
  を**拡張 cap（--time=1200 以上・決着まで）**で再走査。SAT なら 5×23 witness で
  witness帯 m=15..23 拡大・M_{5,6} ∈ [24, 249]。UNSAT なら当該サブインスタンスの
  決定的除外。INDET なら拡張後の conflicts を記録。
- class {0} krow=0:4 minpos=3..11（未走査）・krow=0:3 minpos=1..・k2/k1/k0 分解を
  cap 250s で走査し難度プロファイルを記録。
- 陽性対照 5×21 {0}（期待 SAT 330,743）・witness較正 5×22 {0}k4p0
  （期待 SAT 3,126,820）を環境較正として実行・bit-exact 検証。

飽くまで有限サブインスタンスの走査であり、5×23 全体の不在主張ではない。
既知の seed 近傍 surgery 負記録（1,416 / 552,000 構成・0件）とは独立。

## 状態

- IN FLIGHT（実行中）。着地時に records/report/summary を更新。
