---
id: K1044
title: 2トークン残余ゲーム z=17・y=2境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z17 y2 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1023
  note: B子の評価とx=2帰納基底にy=1パラメトリック全z全称公式（z=17行）を使用する
- type: depends_on
  target: K1042
  note: C子の評価に1⊕(z=16・y=2境界切片)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z17-y2-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表（隙間なし被覆）による全称証明
- path: research/experiments/vertical-fiber-two-token-z17-y2-boundary-20261119/verify_z17_y2.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、B/Cアンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z17-y2-boundary-20261119/output/audit.json
  role: data
  note: 13,834,273照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/experiments/vertical-fiber-two-token-z17-y2-boundary-20261119/census_z17_y2.py
  role: verifier
  note: x=2..45・R=0..x+45の生二再帰センサス（二エンジン一致・閉形式一致・tail）で行表を第三導出から照合する
- path: research/experiments/vertical-fiber-two-token-z17-y2-boundary-20261119/output/census.txt
  role: data
  note: センサスの決定論的出力（二回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z17-y2-boundary.md
  role: log
  note: 最新main確認、並走のK1043採番観測、証明・監査・次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=17、y=2、
  全x>=2・全R>=0。Grundy値0/1/2を完全分類する。
---

## 命題・範囲

すべての \(x\ge2\)、\(R\ge0\) について、\(H(R;(x,2);17)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le18\) で単一トークン
\(x+2\) へ縮約し、高残容量は \(R\ge x+20\) で \((x+2)\bmod2\) となる。

値2位置はx=2で{1,3}、x=3,4でO[1,5]、x=5,6でO[1,7]、x=7,8でO[1,9]、
x=9,10でO[1,11]、x=11,12でO[1,13]、x=13,14でO[1,15]、
x=15（h=z行）でO[1,19]（連続上端19=2y+(d+z)/2=4+15。
d=13=x-y、d+z=30≡2 (mod 4)。奇数のためq_odd丸めが働かずK1032のz=15・x=13上端17=4+13
と同じ「d+z≡2で上端が連続帯に伸びる」奇数z型。偶数z型K1042のx=14上端
q_odd(18)=17=z+1孤立（d+z=28≡0）と対照的なd+z mod 4の2値格子規則の実例）、
x=16,17,18でO[1,17]、x=19（pin行x=z+y）でO[1,17]∪{21}
（pin=21=2y+z・奇数zラダーO[1,z]。K1032のpin 2y+z=32に続き奇数z型2例目）、
x=20の掃引行でO[1,17]∪O[21,39]=O[1,z]∪O[pin,x+y+z]、
x≥21でO[1,17]∪{21}に定着する。
値1位置は偶数x<=14で空、奇数x=3,5,7,9,11,13でI[x+3,∞)、x=15で
{18,20}∪I[21,∞)、x=16で{18}、x=17で{18,20}∪I[21,∞)、x=18で{18,20}、
x=19で{18,20}∪I[22,∞)、x=20で{18,20}、奇数x>=21で
{18,20}∪O[23,x+20]∪I[x+21,∞)、偶数x>=22で{18,20}∪O[23,x+19]（有限）。
値1基底点は{18,20}={z+1,z+3}でy点仮説の2点型6例目
（K1019の{13,15}・K1025の{14,16}・K1028の{15,17}・K1032の{16,18}・
K1042の{17,19}に続き、y=2ではz=12..17の6連続・奇数zではz=13,15に続き3例目）、
値1中間帯はz+2y+2=23開始で偶奇がzに追従する奇数位置帯、
無限I帯は奇数x行のみでtail R>=x+20の値(x+2) mod 2が1になる行と一致する
（「I帯はtail値1の行にだけ現れる」一般則のy=2・奇数z型確認）。

## 現在の根拠と限界

全称性はx外帰納と、全R（1<=R<=x+19=tail-1）を覆う明示的なA/B/C署名帯表・mex対応表による。
x=2では二つのトークン減少手が同じ(1,2);17多重集合子に合流し、K1023のz=17行を帰納基底として使う。
x>=3ではA子を帰納仮説、B子をK1023、C子を1⊕K1042（z=16,y=2全称公式）で評価する。
R<=18はK0832の高さのみ縮約、R>=x+20はK0832の一般tailで閉じる。
署名帯表は各行R=1..x+19を完全被覆しtailのR>=x+20に直結するため、
z=16型の隙間行（被覆<=x+17・tail>=x+19・隙間R=x+18）と異なり被覆とtailの間に
隙間行がない。閉形式帯は共通head
[(1,1,17,"01"),(0,2,16,"23"),(0,18,18,"02"),(1,19,19,"1"),(0,20,20,"02"),
(1,21,21,"01"),(0,22,22,"123")]に、奇数行(1,23,x+18,"0"),(0,24,x+19,"1")、
偶数行(1,23,x+19,"0"),(0,24,x+18,"1")が続く。静的表はx=2..22（x=15はh=z行・
x=21は偶帯署名"12"移行行）、定常は奇数x>=23・偶数x>=24（帯構造は行偶奇で
完全共通・帯上端のみx+18/x+19入替）。
独立監査は13,834,273照合・不一致0・二回実行byte-identical
（検証器SHA-256 `06c11ff4a77530746e150d166fd727a0e971f799a7d82f11ea260a917c822222`、
ハッシュ除外フィールドSHA-256 `cf3f061a0fde67847cef2e4fef1951173a11e6dcf682894ce13e7c7257ef59a3`、
audit.json全文SHA-256 `6bc527166a67d6c7a2609e9559b45f6b7459b955b5fc894109cdda083c1a694f`）。
別プロセス・別cwd実行でも同一sha256。生二再帰センサス（x=2..45）も
行表・閉形式・tailを第三導出から照合して0不一致
（census.txt SHA-256 `1c8e8417d6916520bef8ce900e0c3f71bc1ba4105f6ab7ecc2a19486bc4193b6`）。
有限監査は転写・実装照合であり、全称性は帰納証明が担う。

本項でも、h=z行上端がd+z≡2 (mod 4)でq_odd丸めなしの連続帯2y+(d+z)/2となる
奇数z構造（K1032に続き2例目）を確認した。d+z mod 4による2値格子規則
（≡2→2y+(d+z)/2連続、≡0→z+1孤立）の一般証明は未解決のまま。

## 未解決

z=18・y=2（B子K1023・C子1⊕K1044で両子出版済み）、z=17・y=3（B子K1044・C子1⊕K1050で両子出版済み・着手可能）、y≥2族の一般化、値1基底点y点仮説{z+1,z+3,...,z+2y-1}の一般証明（y=2ではz=12..17の6連続）、h=z行上端とpin前置のd+z mod 4格子規則の一般証明、標準二次元盤の固定幅・q点安定化長。