---
id: K0434
title: 整数座標四点の行列式と分母を払った円・直線方程式の同値
kind: proposition
status: proved
topics: [rules, geometry, formalization]
aliases: []
relations: []
artifacts:
- path: Kyouen/IntegerGeometry.lean
  role: lean
  note: 全称同値定理、盤面座標の単射性、ForbiddenFourへの接続。Lean 4.35.0で検査。
- path: Kyouen/FormalizationChecks.lean
  role: lean
  note: 共円・共線・非共円例と主要定理の公理一覧
scope: 整数座標四点a,b,c,dでa≠b。ForbiddenFourについては六組すべての相異性も保存。
evidence: Lean核で検査した全称証明。実数型上の幾何オブジェクトとの接続は含まない。
---

# 整数座標の行列式と円・直線方程式

`Kyouen/IntegerGeometry.lean` の `determinant_zero_iff` は、整数座標四点 `a,b,c,d` と `a≠b` に対し、既存ルールと同じ行列式が0であることと、次のどちらかの方程式が全四点で成立することの同値を証明する。

- 円：整数 `scale,cx,cy,radiusSq` が存在し、`scale≠0`, `radiusSq≥0`、かつ `(scale*x-cx)^2+(scale*y-cy)^2=radiusSq`。
- 直線：整数 `A,B,C` が存在し、`A≠0` または `B≠0`、かつ `A*x+B*y+C=0`。

円は通常の中心 `(cx/scale,cy/scale)`、半径の二乗 `radiusSq/scale^2` の式から分母を払った表現である。
Lean内ではこの整数の二乗距離方程式を `OnCircle` の定義に用い、実数型・平方根・ユークリッド距離は導入していない。

証明は第一点を原点へ平行移動し、外積が非零なら中心の分子と分母を明示構成する。
第一・第二・第三点が共線でも、第四点との外積による分岐を行う。両外積が0なら第一・第二点を通る直線を構成する。
逆方向は持ち上げた座標 `(x²+y²,x,y,1)` の線形従属から導く。

`rule_determinant` はこの行列式が `SquareBoard.determinant4` と定義的に同じことを証明する。
さらに盤面の行商・剰余からなる座標写像 `boardPoint` が単射であることを証明し、`forbiddenFour_iff` により六組の相異性を保ったまま既存の `ForbiddenFour` と上の円・直線方程式を接続した。

これは有限例の観測ではなく全整数座標に対する核検査済み証明である。具体証明書の局所条件検査や9×9の勝敗は、この同値から直接には得られない。
