---
id: K1002
title: 2トークン残余ゲーム z=10・y>=6一様Grundy定理
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z10 y-ge6 uniform Grundy theorem]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームのA/B/C再帰、Grundy上界、一般tail、高さのみ縮約を使う
- type: depends_on
  target: K1008
  note: y=6行の全称分類（agree監査で本式と不一致0点）
- type: depends_on
  target: K1009
  note: y=7行の全称分類（agree監査で本式と不一致0点）
- type: depends_on
  target: K1010
  note: y=8行の全称分類（K1011検証器の双転写恒等・公式再生で本式と一致）
- type: depends_on
  target: K1011
  note: y>=9領域の一様全称分類。K1002の式はK1011の主定理式と同一
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
- path: research/experiments/vertical-fiber-two-token-z10-y-ge9-proof-20261119/report.md
  role: proof
  note: y>=9領域のy強帰納+x外帰納による全称証明（K1011）。式はK1002と同一
- path: research/experiments/vertical-fiber-two-token-z10-y-ge9-proof-20261119/verify_z10_y_ge9_proof.py
  role: verifier
  note: 7,657,856検査・不一致0。K1002census転写との恒等照合を含む
- path: research/log/2026-11-19-vertical-fiber-two-token-z10-y-ge9-proof.md
  role: log
  note: z=10,y>=9一様証明とK1002 proved昇格の記録
scope: >-
  κ=1残余ゲームの2トークン族H(R;(x,y);10)、全x>=y>=6・全R>=0について、
  本文と証明報告に記したT/P/tail式が成り立つ定理。
evidence: >-
  証明は3つの領域の併せ技である。(1) R<=11はK0832の高さのみ縮約と単一トークン
  閉形式から全x>=y>=6で全称分類済み（値2は{1,3,5,7,9}、値1は{11}、他は0）。
  R>=S+11=x+y+11はK0832の一般tailでH=S mod 2。(2) 行y=6,7,8は各切片定理
  （K1008・K1009・K1010）で全R分類済みで、agree監査（y=6は総2,073,300点・
  y=7は総2,073,257点、いずれも不一致0点）、K1010検証器統合監査のK1002整合グリッド
  （2,050,797照合・x<=2000・0<=R<=x+24・不一致0）およびK1011検証器の双転写恒等・
  公式再生（y=8、57,135+55,670点）により本式と機械一致する。(3) y>=9は
  K1011が同一式をy強帰納と各行内x外帰納、(y,d)パラメトリック署名帯表で
  全称証明した（独立監査7,657,856検査・不一致0・二回実行byte-identical）。
  y=1..5は本項の適用域外で、各切片定理（K1003..K1007）が全称性を担う（y=5の
  対角線h=z行2点例外を含まない）。これによりz=10の2トークン族は全y>=1で
  全称分類済み。
---

## 命題・範囲

z=10の2トークン残余ゲームで、全 \(x\ge y\ge6\)、全 \(R\ge0\) に対するGrundy値0/1/2の一様閉形式である。値2位置は基本ラダー \(\{1,3,5,7,9\}\) に、d=0,4,8の前倒し点、d=11の掃引奇数帯、d>=12の定常点 \(2y+11\) を加えた集合。値1位置はdの偶奇・小さいdの過渡帯で場合分けされ、tailは \(R\ge x+y+11\) で \((x+y)\bmod2\)。完全な式は証明報告を正本とする。

## 証明の構成

全x>=y>=6ではS=x+y>=12である。3領域に分けて閉じる。

1. **低残容量帯 R<=11**: K0832の高さ縮約定理からH(R;(x,y);10)=v(S,10,R)（vは単一トークン値）となる。q(10)=9より、R=1,3,5,7,9で値2、R=0,2,4,6,8,10で値0、R=11で値1。本式との一致は低R帯証明報告で全d区分について証明済み。
2. **高R tail R>=S+11**: K0832の一般tailからH=S mod 2。
3. **中間帯 12<=R<=S+10**: 行ごとに閉じる。y=6,7,8は各切片定理（K1008・K1009・K1010）の全称証明とagree監査・双転写恒等で本式と一致する。y>=9はK1011が本式と同一の閉形式をy強帰納と各行内x外帰納、(y,d)パラメトリックA/B/C署名帯表、K0832 Theorem Tで全称証明した。

従って全x>=y>=6・全R>=0で本式が成り立つ。

## 境界行との関係

y=6は本主張域の第1行で、agree_k1002_y6.py照合（総2,073,300点）で不一致ちょうど0点。y=7は第2行で、agree_k1002_y7.py照合（総2,073,257点）で不一致ちょうど0点。y=8はK1010の定理式そのものが本式のy=8制限であり、K1010検証器統合監査のK1002整合グリッド（2,050,797照合・不一致0）とK1011検証器の双転写恒等（x=8..300・57,135点）・公式再生（55,670点）で機械保証する。y=5はh=z行（x+y=10）の対角線例外 (5,11),(5,13) のため本式の適用域外（K1007がy=5行の全称分類を担い、適用域をy>=6に限定する根拠も全称的に確定済み）。y=1..4もそれぞれの切片定理（K1003..K1006）が全称性を担う。

## 現在の根拠と限界

本項のstatusはprovedである。根拠は低R帯全称証明・K0832一般tail・y=6..8切片定理のagree照合・K1011のy>=9一様全称証明であり、有限センサスや直接再帰の一致は補助的な独立監査にとどまる。標準二次元盤の固定幅・q点版の真の安定化長への転送は未証明。z>=11の族の分類、全高さを統合する2トークン値2位置の一般式は未解決のまま。
