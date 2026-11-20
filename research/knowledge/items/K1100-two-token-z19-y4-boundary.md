---
id: K1100
title: 2トークン残余ゲーム z=19・y=4境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - two-token z19 y4 boundary slice full Grundy classification
relations:
- type: depends_on
  target: K0832
  note: 2トークン再帰、単一トークン閉形式、一般tailを使う
- type: depends_on
  target: K1098
  note: B子 H(R-1;(x,3);19) の全x分類
- type: depends_on
  target: K1083
  note: C子 1 xor H(R-1;(x,4);18) の全x分類
artifacts:
- path: research/experiments/vertical-fiber-two-token-z19-y4-boundary-20261120/report.md
  role: proof
  note: T/P閉形式、A/B/C署名帯表、高さのみ領域とpin鋭性、交叉観察
- path: research/experiments/vertical-fiber-two-token-z19-y4-boundary-20261120/verify_z19_y4.py
  role: verifier
  note: 二つの直接再帰、K1098/K1083子アンカー、署名帯・mex、帰納閉包、単一トークン縮約、tailを監査
- path: research/experiments/vertical-fiber-two-token-z19-y4-boundary-20261120/output/audit.json
  role: data
  note: 945,926検査・不一致0・三実行でbyte-identical
- path: research/log/2026-11-20-two-token-z19-y4-boundary.md
  role: log
  note: 導出、署名帯表の設計、全称証明、監査、限界と次候補
- path: research/log/2026-11-20-two-token-z19-y4-single-owner-note.md
  role: log
  note: 着手前の単一オーナー宣言（commit 056c00bd23）
---

# 2トークン残余ゲーム z=19・y=4境界切片の全Grundy分類

全 x>=4・全 R>=0 で H(R;(x,4);19) を閉形式で全称分類する。
B子は K1098（z=19,y=3）、C子は 1⊕K1083（z=18,y=4）、x=4 は多重集合 (3,4) 合流の帰納基底。

## 主結果（値2の位置 T_x）

- x<=14（S=x+4<=18<z）: 高さのみ行 O[1,q_o(x+4)]（全Rで単一トークン値に一致）。
- 対角行 x=15（S=z）: ラダー上端 23 = 2y+q_o(z−y)（交差式の8実例目）。
- 通常ラダー O[1,19]=O[1,z]（x>=16）。
- 前倒し単点 x=19（25）・x=23=z+y（27）。d=x−y∈{15=z−4, 19=z} は y=3 と同一で、
  d の活性値が y に依らない交叉観察（d+z≡2 mod 4・r=2y+(d+z)/2）。
- 掃引行 x=24=z+y+1: O[27,47]=O[2y+z,S+z]。定常pin 27=2y+z は x>=25=z+y+2。

## 値1の位置 P_x

基底点 {20,22,24,26}（[z+1,z+2y−1]=[20,26] の偶点・ちょうど y 点。z=19 族で
y=2（K1052）・y=3（K1098）に続き3連続確認）。途中行は [20,∞) から零点
{21,23,...} を除く形。x>=25 は {20,22,24,26}∪O[29,q_o(x+23)]∪(奇数行tail [x+24,∞))。
tail は R>=x+24=S+z+1 で (x+4) mod 2。

## 高さのみ領域とpin鋭性

単一トークン値を v(s,z,R) とすると、x<=14（S<z）の全行で H(R;(x,3);19)=v(x+4,19,R)
が全Rで一致（S<z候補命題の3実例目）。x=15..22 の最大初期一致区間は 24,23,24,25,24,25,26,27。
x>=23（=z+y）で R<=26=pin−1 が一様成立し、R=27=2y+z で鋭い反例（親2・単一0、
一般形 R<=pin−1 の4実例目・開始行 x=z+y は y=3 と同一形式）。

## 証明の範囲

全称性は x外帰納と、1<=R<=x+23 を覆す記号的A/B/C署名帯表（静的22行 x=4..25＋x>=26アフィン帯）による。
有限監査945,926件は証明そのものではなく、再帰実装・子アンカー・帯表転写・mexの独立照合である
（検証器SHA-256 09cc65208d4696a73354455ac348e2f4054fca34e74ecacbb9eaa5b434d56b3f・監査正本SHA-256
1669d20a2fbe94b44bb5783e2f9a9a1c20c63daf125ad12182d024576fe3e8cc・3実行byte-identical）。
本項は z=19,y=4 に限り、z=19,y>=5、全z一般化、標準二次元盤には主張を拡張しない。
S<z高さのみ・対角行上端・低R一様境界・基底点y点仮説・d活性値のy非依存は一般zでは未証明の観察。

## 採番の履歴

push直前の最新main再取得で K1100 の3点確認（slug 404・README grep・list_commits）を行い、
並走レーン（y=2パラメトリック K1099・n11残余・「two-token merge below diagonal」宣言）と
衝突しないことを確認して採番した。
