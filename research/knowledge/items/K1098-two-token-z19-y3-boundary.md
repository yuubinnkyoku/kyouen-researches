---
id: K1098
title: 2トークン残余ゲーム z=19・y=3境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - two-token z19 y3 boundary slice full Grundy classification
relations:
- type: depends_on
  target: K0832
  note: 2トークン再帰、単一トークン閉形式、一般tailを使う
- type: depends_on
  target: K1052
  note: B子 H(R-1;(x,2);19) の全x分類
- type: depends_on
  target: K1078
  note: C子 1 xor H(R-1;(x,3);18) の全x分類
artifacts:
- path: research/experiments/vertical-fiber-two-token-z19-y3-boundary-20261120/report.md
  role: proof
  note: T/P閉形式、偶奇別A/B/C署名帯表、低R縮約と「高さのみ」領域、交叉観察
- path: research/experiments/vertical-fiber-two-token-z19-y3-boundary-20261120/verify_z19_y3.py
  role: verifier
  note: 二つの直接再帰、子アンカー、署名帯・mex、帰納閉包、単一トークン縮約、tailを監査
- path: research/experiments/vertical-fiber-two-token-z19-y3-boundary-20261120/output/audit.json
  role: data
  note: 885,500検査・不一致0・三実行でbyte-identical
- path: research/log/2026-11-20-two-token-z19-y3-boundary.md
  role: log
  note: 導出、署名帯表の設計、全称証明、監査、限界と次候補
- path: research/log/2026-11-20-two-token-z19-y3-single-owner-note.md
  role: log
  note: 対象と依存を固定した単一オーナー宣言
scope: >-
  κ=1残余ゲーム H(R;(x,3);19) の2トークン族。全x>=3、全R>=0。
  Grundy値0/1/2を報告のT_x/P_xで完全分類する。
evidence: >-
  B子はK1052、C子は1 xor K1078、A子はx外帰納。x=3ではA/Bが同じ多重集合
  (2,3)に合流する。1<=R<=x+22を過渡22行（x=3..24）とx>=25の偶奇別アフィン署名帯で
  一意被覆し、mexがT/P式に一致する。R=0は終局、R>=x+23はK0832一般tail。
  x<=15（S=x+y<z）は全行が単一トークン値に完全一致、x=16..21は行別の最大初期区間、
  x>=22でR<=24が一様で、R=25=2y+z（pin）の鋭い反例を持つ。
---

## 命題

全ての \(x\ge3\)、\(R\ge0\) について、\(H(R;(x,3);19)\) のGrundy値0/1/2は
報告の \(T_x,P_x\) で完全分類される。高Rでは
\[
R\ge x+23\implies H(R;(x,3);19)=(x+3)\bmod2.
\]

値1の基底点は \(x\ge21\) で
\[
\{20,22,24\}=\{z+1,z+3,z+5\}
\]
のちょうど3点に定着する（y=3族では z=18（K1078）と z=19（本項）の2例連続で、
\(\{z+1,\dots,z+2y-1\}\) の y 点仮説のとおり x=z+y で完成する）。値2の定常pinは
\(25=2y+z\)（奇数z型）、掃引行は \(x=23=z+y+1\) で \(O[25,45]=O[2y+z,S+z]\) に
広がり、x>=24で一点25へ戻る。前倒し単点は x=18 と x=22（\(d=15,19\equiv3\ (4)\)、
\(d+z\equiv2\ (4)\)、\(r=2y+(d+z)/2\)）、対角行 \(x=16\)（\(S=z\)）はラダー上端21。

## 高さのみ領域と低R縮約

単一トークン値を \(v(s,z,R)\) とする。

- \(x\le15\)（\(S=x+y\le18<z\)）の全行で \(H(R;(x,3);19)=v(x+3,19,R)\) が全\(R\ge0\)で
  一致する。K1078（z=18,y=3, x≤14）でも同一構造が確認済みで、
  「\(S<z\Rightarrow H(R;(x,y);z)=v(x+y,z,R)\)」は一般未証明の候補命題になる。
- \(x\ge22\) では \(R\le24\) が一様に成立し、\(R=25=2y+z\)（pin）で親2・単一トークン0の
  鋭い反例を持つ。K1092（偶数z: R≤28=z+2y、pin=29）と対称で、一般形
  \(R\le\mathrm{pin}-1\) の3実例目である。x=16..21の行別最大初期区間は 22,23,22,23,24,25。

## 証明の範囲

全称性はx外帰納と、1<=R<=x+22を覆す記号的A/B/C署名帯表（過渡22行＋x≥25アフィン帯）による。
有限監査885,500件は証明そのものではなく、再帰実装・子アンカー・帯表転写・mexの独立照合である。
本項はz=19,y=3の切片に限り、z=19,y>=4、全z一般化、標準二次元盤の固定幅・q点版安定化長には
主張を拡張しない。対角行上端 \(2y+q_o(z-y)\)（7切片交叉観察）と低R一様境界 \(R\le\mathrm{pin}-1\) は
一般 z では未証明の観察として報告に記録する。

## 採番の履歴

本項はpush直前の最新main再取得で、並走のN11レーンが K1097（残余72行 safe8 pool 第4ラウンド再解決）
を出版済みであることを検出したため、AGENTS.md規約「衝突側が再採番」に従い K1097 から K1098 に
再採番した。導出・監査の実体は変更なく、検証器docstringとタイトルの番号修正のみを行い、
監査正本を3実行で再生成した（byte-identical）。
