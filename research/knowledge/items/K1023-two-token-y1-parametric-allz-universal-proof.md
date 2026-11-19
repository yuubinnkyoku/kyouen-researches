---
id: K1023
title: 2トークン残余ゲーム y=1族のパラメトリック閉形式の全称証明（全z>=1・全x>=1・全R>=0・z=0基底付き）
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token y=1 parametric all-z universal proof, P1]
relations:
- type: depends_on
  target: K0832
  note: B子の評価に単一トークン閉形式single_tokenを使用する
- type: generalizes
  target: K1022
  note: K1022はz>=6限定の独立証明。本項は全z>=1とz=0基底cand0へ拡張し、別構成（型機械）で証明。両検証器の相互クロスチェック（104万点・不一致0）済み
- type: generalizes
  target: K0877
  note: z=6・y=1切片は本項の特殊例
- type: generalizes
  target: K0977
  note: z=7・y=1切片は特殊例
- type: generalizes
  target: K0983
  note: z=8・y=1切片は特殊例
- type: generalizes
  target: K0985
  note: z=9・y=1切片は特殊例
- type: generalizes
  target: K1003
  note: z=10・y=1切片は特殊例
- type: generalizes
  target: K1012
  note: z=11・y=1切片は特殊例
- type: generalizes
  target: K1016
  note: z=12・y=1切片は特殊例
- type: generalizes
  target: K1017
  note: z=13・y=1切片は特殊例
- type: generalizes
  target: K1018
  note: z=14・y=1切片は特殊例
- type: generalizes
  target: K1020
  note: z=15・y=1切片は特殊例
artifacts:
- path: research/experiments/vertical-fiber-two-token-y1-parametric-allz-proof-20261119/report.md
  role: proof
  note: z帰納（z=0基底→z=1→z>=2一括）と型機械（6差分族±8窓・3パリティ・x=1ビット）による全称証明。K1022（z>=6並走証明）との独立性と厳密な拡張関係も明記
- path: research/experiments/vertical-fiber-two-token-y1-parametric-allz-proof-20261119/verify_p1_universal.py
  role: verifier
  note: 23チェック・1,875,269照合点・不一致0・2回実行でbyte-identical・純Python約5秒
- path: research/experiments/vertical-fiber-two-token-y1-parametric-allz-proof-20261119/cross_check_k1022.py
  role: verifier
  note: 並走K1022検証器（z>=6・census由来）との相互クロスチェック。5チェック1,043,065点・不一致0・z=1..5とz=0はK1022素エンジンが直接照合
- path: research/experiments/vertical-fiber-two-token-y1-parametric-allz-proof-20261119/output/audit.json
  role: data
  note: 決定論的監査出力（固定seed・ソート済みキー）
- path: research/experiments/vertical-fiber-two-token-y1-parametric-allz-proof-20261119/output/cross_check_k1022.json
  role: data
  note: クロスチェック監査出力（決定論的・5チェック全PASS）
- path: research/log/2026-11-19-two-token-y1-parametric-allz-universal-proof.md
  role: log
  note: センサス予想P1の全称化の選定・導出・監査・K1022並走出版との差分化・接続
scope: >-
  κ=1残余ゲームH(R;(x,1);z)の2トークン族。z>=1・x>=1・R>=0の全整数点で
  H(R;(x,1);z)=cand(z,x,R)が成り立つことを主張する。candは2026-11-19
  パラメトリックセンサスで公表されたz偶奇別のT/P集合表（閉形式）である。
  基底としてz=0スライスの閉形式cand0（本項で初導出）も同じく全x>=1・全R>=0で証明する。
  K1022（z>=6・y=1・並走レーン）は本項の主張の部分集合であり、本項はその
  z=1..5の隙間とz=0基底を埋める厳密な拡張である。
evidence: >-
  証明は3部構成。(1) z>=1での子分解：A子=H(R-1;(x-1,1);z)（x>=2のみ）、
  B子=K0832のsingle_token(x,z+1,R-1)、C子=1 xor H(R-1;(x,1);z-1)。x=1では
  2つのトークン手が単一トークン子single_token(1,z+1,R-1)に合流し、この
  選択肢存在ビットが機械で唯一の絶対読みである。(2) z帰納：z=0はcand0、
  z=1のC子は1 xor cand0、z>=2のC子は1 xor cand(z-1,x,R-1)で、帰納仮定の
  もと各スライスの恒等式は型ごとの有限検査に帰着する。(3) 型機械：
  z>=2は3パリティと6差分族w0=x-z,w1=R-x,w2=R-z,w3=R-x-z,w4=R-2x,w5=R-2z
  （±8窓・±9番兵）とx=1ビット、z=1/z=0は(x,R)絶対クリップ族で型空間が
  有限化され、実現型は全て列挙ボックス内に証人を持つ（実現型10750/5458/4994、
  証人境界補題: 釘8・番兵9・鎖長3で|v|<=45<ボックス60）。シフト閉鎖補題は
  子の読みが親の型のみから決まること（閾値|t|<=6対窓±8・番兵±9、最大
  シフト±2、マージン1）を保証する。監査は23チェック1,875,269点で全てok・
  不一致0：素エンジン二種アンカー、z=7..12深アンカー、公開切片K1018/K1020
  公式一致、z=1..40公式恒等式グリッド129,600点、型ごとの恒等式と証人対
  confluence 6,275対、seed遠方probe 200k点（z,x<=3000・R<=9000）、境界多様体
  probe 11,686点、z=0/z=1 probe 120k点（x<=5000・R<=15000）、v空間シェル
  掃引33,710点（|v|∈[61,120]・箱外新規型0）、リング掃引600,000点
  （x<=300・R<=1000・箱外新規型0）。2回実行でaudit.jsonはbyte-identical。
  さらに独立導出のK1022検証器（z>=6・census由来・別レーン）との相互
  クロスチェック5チェック1,043,065点で不一致0：閉形式一致2チェック
  （z=6..80×x<=60が780,750点・遠方z probe 253,860点）、およびK1022の
  素再帰エンジン2種による本項拡張領域の直接照合（z=1..5が5,875点・
  z=0基底が1,425点・z=0広域が1,155点、全てcand/cand0==両エンジン）。
  相手検証器も本環境でV0..V7全体をpassしaudit.jsonをbyte同一再生した。
---

## 命題・範囲

K1023は2トークン残余ゲームのy=1族について、パラメトリックセンサス
（2026-11-19・実験vertical-fiber-two-token-y1-parametric-census-20261119）が
予想したConjecture P1を全称証明する：全てのz>=1・x>=1・R>=0に対し
H(R;(x,1);z)=cand(z,x,R)。candはz偶奇別のT/P集合表（T集合で値2、P集合で値1、
他は0）であり、z=6..15の各スライス定理K0877,K0977,K0983,K0985,K1003,K1012,
K1016,K1017,K1018,K1020は本項の特殊例になる。あわせてz=0基底スライスの
閉形式cand0（x=1: P0={1}；x奇>=3: P0={1}∪E[4,x+1]; x偶>=2:
P0={1}∪E[4,x]∪I[x+2,∞)；x>=2: T0={3}；R=0で0）を同時に全称証明する。

## K1022との関係

並走レーンが同じ閉形式をz>=6限定でK1022として出版した（census由来・
signature-band構成）。本項はz>=1全体とz=0基底を別構成（型機械）で証明する
厳密な拡張であり、重複しない。両クローズドフォームはz=6..80×x<=60・
遠方zで全点一致（104万点超・不一致0）、本項のみが主張する拡張領域z=1..5
とz=0はK1022検証器の素再帰エンジン2種と直接照合して一致した
（cross_check_k1022.py・5チェック全PASS）。

## 現在の根拠と限界

全称性の根拠は、(i) 子分解が選択肢とゲーム定義の一致であり素再帰アンカーで確認、
(ii) z帰納が標準の強帰納法、(iii) 各帰納段階の本体が有限型空間の完全走査である
（全実現型で恒等式照合・不一致0、証人対confluence不一致0）、の3点である。
シフト閉鎖補題（設計原理: 全閉形式の読みは閾値|t|<=6の比較で窓±8・番兵±9と
最大シフト±2でマージン1）は証人対confluenceと90万点超のprobe・シェル・
リング掃引で機械確認した。証人境界補題は釘8・番兵9・鎖長3による|v|<=45の
連鎖証明で、列挙ボックス60は33%の余裕を持ち、ボックス45→60で実現型集合が
同一（10750型）であることが追加の安定性証拠、シェル掃引[61,120]・リング
掃引・遠方probe（9000/15000規模・新規型0）が同補題の機械証拠である。
cand0の導出は独立のz=0センサスと素エンジン照合で二重確認し、さらにK1022
検証器の素再帰エンジン2種（H_ordered・H_canonical）とも一致した。
未解決の残務：y>=2族の同型機械化、11×11・固定幅・q点版安定化長は本項の範囲外（高速レーン外 or 別レーン）。height-only縮約P2（R<=z+1）はK0832でκ=1の一般多重集合について全称証明済みであり、本項のy=1族にも適用できる。
