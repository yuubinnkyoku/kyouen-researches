---
id: K1092
title: 2トークン残余ゲーム z=18・y=5境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - two-token z18 y5 boundary slice full Grundy classification
  - originally assigned K1089 before concurrent main integration renumbering
relations:
- type: depends_on
  target: K0832
  note: 2トークン再帰、単一トークン閉形式、一般tailを使う
- type: depends_on
  target: K1083
  note: B子 H(R-1;(x,4);18) の全x分類
- type: depends_on
  target: K1080
  note: C子 1 xor H(R-1;(x,5);17) の全x分類
artifacts:
- path: research/experiments/vertical-fiber-two-token-z18-y5-boundary-20261120/report.md
  role: proof
  note: T/P閉形式、全Rの偶奇別A/B/C署名帯表、低R縮約の鋭い境界
- path: research/experiments/vertical-fiber-two-token-z18-y5-boundary-20261120/verify_z18_y5.py
  role: verifier
  note: 二つの直接再帰、子アンカー、署名帯・mex、帰納閉包、単一トークン縮約、tailを監査
- path: research/experiments/vertical-fiber-two-token-z18-y5-boundary-20261120/output/audit.json
  role: data
  note: 946,283検査・不一致0・三実行でbyte-identical
- path: research/log/2026-11-20-two-token-z18-y5-boundary.md
  role: log
  note: 導出、署名帯表の訂正、全称証明、監査、限界
- path: research/log/2026-11-20-two-token-z18-y5-single-owner.md
  role: log
  note: 対象と依存を固定した単一オーナー宣言
scope: >-
  κ=1残余ゲーム H(R;(x,5);18) の2トークン族。全x>=5、全R>=0。
  Grundy値0/1/2を報告のT_x/P_xで完全分類する。
evidence: >-
  B子はK1083、C子は1 xor K1080、A子はx外帰納。x=5ではA/Bが同じ多重集合
  (4,5)に合流する。1<=R<=x+23を過渡21行とx>=26の偶奇別アフィン署名帯で
  一意被覆し、mexがT/P式に一致する。R=0は終局、R>=x+24はK0832一般tail。
  高さのみ縮約はx=5..12で全R、x=13..24で行別の最大初期区間、
  x>=25でR<=28=z+2yに成立し、R=29で各xの鋭い反例を持つ。
---

## 命題

全ての \(x\ge5\)、\(R\ge0\) について、\(H(R;(x,5);18)\) のGrundy値0/1/2は
報告の \(T_x,P_x\) で完全分類される。高Rでは
\[
R\ge x+24\implies H(R;(x,5);18)=(x+5)\bmod2.
\]

値1の基底点は \(x\ge23\) で
\[
\{19,21,23,25,27\}=\{z+1,z+3,z+5,z+7,z+9\}
\]
のちょうど5点に定着する。値2の定常pinは \(29=2y+z+1\)、掃引行は
\(x=24=z+y+1\) で \(O[29,47]\) に広がり、x>=25で一点29へ戻る。

## 高さのみ縮約の鋭い初期区間

単一トークン値を \(v(s,z,R)=H(R;(s);z)\) とする。全 \(x\ge25\) で
\[
\boxed{R\le28=z+2y\implies H(R;(x,5);18)=v(x+5,18,R)}
\]
が成立し、R=29では親が2、単一トークンが1となるため一様境界は鋭い。
x=5..12は全Rで一致し、x=13..24の最大初期区間は報告に示した行別表の通り。

## 証明の範囲

全称性はx外帰納と、1<=R<=x+23を覆う記号的A/B/C署名帯表による。
有限監査946,283件は証明そのものではなく、再帰実装・子アンカー・帯表転写・mexの独立照合である。
本項はz=18,y=5の切片に限り、z=18,y>=6一様族、全z一般化、標準二次元盤の固定幅・q点版安定化長には主張を拡張しない。


## 採番の履歴

本項は並走中に一度K1089として作成されたが、N11レーンのK1089が先にmainへ反映され、その後K1090も別のN11項目に使われたため、重複IDを避けて現行IDをK1092とした。証明report・検証器・監査JSONは元のbytesを保持し、検証器のSHA-256 pinも変更していない。
