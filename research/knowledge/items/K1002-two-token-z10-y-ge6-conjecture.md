---
id: K1002
title: 2トークン残余ゲーム z=10・y>=6一様Grundy式候補
kind: proposition
status: conjectured
topics: [grundy, residual-games]
aliases: [two-token z10 y-ge6 uniform Grundy conjecture]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームのA/B/C再帰、Grundy上界、一般tailを使う候補式
artifacts:
- path: research/experiments/vertical-fiber-two-token-z10-y-ge6-census-20261119/report.md
  role: data
  note: z=10・y>=6のT/P/tail一様候補と有限監査・低y境界例外
- path: research/experiments/vertical-fiber-two-token-z10-y-ge6-census-20261119/verify_z10_y_ge6_census.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰と候補式を比較する有限検証器
- path: research/experiments/vertical-fiber-two-token-z10-y-ge6-census-20261119/output/audit.json
  role: data
  note: 227,562直接照合・20,079 tail照合・不一致0・2回byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z10-y-ge6-census.md
  role: log
  note: z=10の有限センサスと次の帰納証明課題
- path: research/experiments/vertical-fiber-two-token-z10-low-r-proof-20261119/report.md
  role: proof
  note: K0832の高さ縮約・単一トークン閉形式からR<=11の全称分類を導き、候補式との一致を全d区分で証明
- path: research/log/2026-11-19-vertical-fiber-two-token-z10-low-r-proof.md
  role: log
  note: K1002の重複回避確認、低R全称証明、残る中間帯の特定
scope: >-
  κ=1残余ゲームの2トークン族H(R;(x,y);10)、全x>=y>=6・全R>=0について、
  本文と証明報告に記したT/P/tail式が成り立つという予想。全称証明は未取得。
evidence: >-
  K0832の高さ縮約R<=z+1と単一トークン閉形式から、全x>=y>=6でR=0..11を
  全称分類した。値2は{1,3,5,7,9}、値1は{11}、その他は0であり、K1002の
  T/P候補式と全d区分で一致する。K0832の一般tail R>=S+11も既証明なので、
  未証明なのは12<=R<=S+10のみ。別途、y=6..28、d=x-y=0..96、
  0<=R<=x+y+19の227,562点で順序保持と降順正準化の二直接mex再帰が候補式と
  一致し不一致0。tail offset 0..8は20,079点で一致。値2位置13,317点、
  偶数親114,333点・奇数親113,229点でTheorem T上界違反0。検証器内2回と
  別プロセス再実行の監査JSONはbyte-identical。y=1..5の境界走査では不一致が
  22,16,11,7,2件で、y=5は対角線d=0のR=11,13だけが候補から外れる。
  中間帯の全称性は未証明であり、K1002のstatusはconjecturedのまま。
---

## 命題・範囲

候補はz=10の2トークン残余ゲームで、全 \(x\ge y\ge6\)、全 \(R\ge0\) に対するGrundy値0/1/2の一様閉形式である。値2位置は基本ラダー \(\{1,3,5,7,9\}\) に、d=0,4,8の前倒し点、d=11の掃引奇数帯、d>=12の定常点 \(2y+11\) を加えた集合。値1位置はdの偶奇・小さいdの過渡帯で場合分けされ、tailは \(R\ge x+y+11\) で \((x+y)\bmod2\)。完全な式は証明報告を正本とする。

## 全称証明済み部分：低残容量帯

全x>=y>=6ではS=x+y>=12である。K0832の高さ縮約定理から、R<=11=z+1なら
H(R;(x,y);10)=v(S,10,R)（vは単一トークン値）となる。単一トークン閉形式では
1<=10<=S-1、q(10)=9なので、R=1,3,5,7,9で値2、R=0,2,4,6,8,10で値0、
R=11で値1を得る。K1002のT/P候補式との一致もdの全4区分で証明した。
詳細は低R帯証明報告を参照。

またK0832の一般tailからR>=S+11ではH=S mod 2である。従って全域予想で
残る未証明範囲は12<=R<=S+10に限られる。

## 現在の根拠と限界

有限格子で二種類の直接再帰と候補式が一致し、z=7,8,9で観察された前倒し格子・掃引行・定常ピン止め則もz=10で再現した。低R帯と高R tailは全称的に証明済みだが、中間帯の全称性は未証明である。y=5の対角線にはR=11,13の例外があるため、y>=5へ無条件に延長することもできない。K1007がy=5切片の全称式を証明し、その付属照合（agree_k1002_y5.py、総2,073,342点）により候補とのy=5上の不一致が対角線(x,R)=(5,11),(5,13)の2点に全行・全R帯で確定した（候補のd=0前倒し格子点15=2y+5は実測も値2。h=x+y=z行はy>=6ではx+y>=12>10で定義域に現れず、y>=6適用域限定の根拠が全称的に確定）。y=1..4の不一致集合の全称的確定（K1003..K1006の既証明式と候補の照合）は今後の課題。K1008がy=6切片の全称式を証明し、その付属照合（agree_k1002_y6.py、総2,073,300点）により候補とのy=6上の不一致が全行・全R帯でちょうど0点に確定した（y=6は本候補の主張域y>=6の第1行で、候補のリーディング行が全称定理になった。未証明中間帯は12<=R<=S+10のy>=7のみに縮小）。K1009がy=7切片の全称式を証明し、その付属照合（agree_k1002_y7.py、総2,073,257点）により候補とのy=7上の不一致も全行・全R帯でちょうど0点に確定した（候補の最初の2行y=6,y=7が全称定理化。未証明中間帯は12<=R<=S+10のy>=8のみに縮小）。

次の課題は、低yの橋渡しを明示したうえで、A/B/C署名帯表とy強帰納・x外帰納により中間帯12<=R<=S+10を閉じること。z=10の全Grundy分類は依然として未解決である。
