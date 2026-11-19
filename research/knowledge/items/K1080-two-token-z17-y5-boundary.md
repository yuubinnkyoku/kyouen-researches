---
id: K1080
title: 2トークン残余ゲーム z=17・y=5境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z17 y5 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約と一般tailを使用する
- type: depends_on
  target: K1076
  note: B子の評価とx=5基底の多重集合合流にz=17・y=4切片を使用する
- type: depends_on
  target: K1074
  note: C子の評価に1 xor (z=16・y=5切片)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z17-y5-boundary-20261120/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z17-y5-boundary-20261120/verify_z17_y5.py
  role: verifier
  note: 二方式の親再帰、二子アンカー、署名帯、帰納ステップ閉包、深域帯端点、tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z17-y5-boundary-20261120/census_z17_y5.py
  role: verifier
  note: 着手をトークン値ごとに列挙する明示dict memoの第三独立実装
- path: research/experiments/vertical-fiber-two-token-z17-y5-boundary-20261120/output/audit.json
  role: data
  note: 16,407,681照合・不一致0の決定論的監査結果（二cwd・三実行でbyte-identical）
- path: research/experiments/vertical-fiber-two-token-z17-y5-boundary-20261120/output/census.txt
  role: data
  note: 第三実装censusのx=5..45行写真と閉形式照合（2,706点一致）
- path: research/log/2026-11-20-vertical-fiber-two-token-z17-y5-boundary.md
  role: log
  note: 単一オーナー宣言、最新main・依存定理・未解決範囲の確認、証明・監査・次の着手候補
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=17、y=5、
  全x>=5・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=5では二つのトークン減少手が同じ多重集合(4,5)に合流し、
  B子はK1076のx=5行、C子は1 xor K1074のx=5行で閉じる。x>=6では
  A子を帰納仮説、B子をK1076、C子を1 xor K1074で評価する。
  全1<=R<=x+22はreport.mdの静的行x=5..24・偶奇別一般行のA/B/C署名帯表が
  互いに素に被覆し、mex表からT/Pが得られる。R>=x+23はK0832の一般tailで
  親値(x+5) mod 2に閉じる。R<=18の高さのみ縮約もK0832から従う。
  独立監査は親二直接再帰13356点、K1076/K1074子アンカー21664点、
  集合型vs述語型転写59052点、署名帯構造的被覆182行と署名帯スキャン19656点、
  帰納閉包掃引( x<=5000)12612375点、tail 4095点、高さのみ縮約2094点、
  深域アフィン3599568点、深域帯端点67609点、固定seed散点8000点の合計
  16407681照合で不一致0。三実行・二cwdでaudit.jsonがbyte-identical。
  第三実装census(明示dict memo・値ごとの着手列挙)がx=5..45の2706点を再導出し
  閉形式と完全一致。audit.jsonのverifier_sha256はコミット済み検証器の正確な
  バイト列のSHA-256で、byte-pin不整合は構成上生じない。
---

## 命題・範囲

全ての \\(x\\ge5\\)、\\(R\\ge0\\) について、\\(H(R;(x,5);17)\\) のGrundy値0/1/2を
report.mdの \\(T(x),P(x)\\) で完全分類する。低残容量は \\(R\\le18\\) で単一トークン
\\(x+5\\) へ縮約し、高残容量は \\(R\\ge x+23\\) で \\((x+5)\\bmod2\\) となる。

値2は初期ラダー \\(O[1,2\\lfloor x/2\\rfloor+5]\\)（x=5..11）からz=17ラダー
\\(O[1,17]\\) へ移り、x=12の対角行（\\(x+y=z\\)、q型）で \\(O[1,21]\\)、
x=14・x=18に前倒し点23・25、x=22にpin 27=2y+z、x=23の掃引帯 \\(O[27,45]\\) を経て、
x>=24で \\(O[1,17]\\cup\\{27\\}\\) に定着する。

値1の基底点はx>=21で \\(\\{18,20,22,24,26\\}=\\{z+1,z+3,\\ldots,z+2y-1\\}\\) の
ちょうどy=5点に定着する。pinは \\(27=2y+z\\)（奇数z）、掃引行は \\(x=z+y+1=23\\)、
署名の一行遅れ例外行は \\(x=24\\)（[30,46]:12）。

## 現在の根拠と限界

全称性はx外帰納と、全Rを互いに素に覆うA/B/C署名帯表による。B子はK1076、
C子はK1074の全称定理であり、低R縮約・一般tailはK0832から従う。
有限監査は証明そのものではない。前倒し格子 \\(2y+(d+z)/2\\) はd=9・13で出現し
d=1・5では同じ合同条件を満たしても出現しない（出現条件は未解決）。
高さのみ縮約の一様境界の観察値 \\(R\\le22=z+y\\) はK1076・K1078・K1074・K1077と
z+y型で整合するが一般式は未証明、最初の反例は \\(H(23;(12,5);17)=1\\) 対
\\(v_{\\rm single}(17,17,23)=2\\)。z=17・y>=6一様族（B=本項、C=1 xor K1077）と
z=18・y=4（B=K1078、C=1 xor K1076）が次の候補（着手前に単一オーナー宣言を必須）。
標準二次元盤の固定幅・q点版安定化長、値1基底点y点仮説の全z一般証明、
前倒し格子の出現条件、q型上端の一般式も未解決。
