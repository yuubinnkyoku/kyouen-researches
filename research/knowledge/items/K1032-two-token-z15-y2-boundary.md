---
id: K1032
title: 2トークン残余ゲーム z=15・y=2境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z15 y2 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1020
  note: B子の評価とx=2帰納基底にz=15・y=1境界切片を使用する
- type: depends_on
  target: K1028
  note: C子の評価に1⊕(z=14・y=2境界切片)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z15-y2-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z15-y2-boundary-20261119/verify_z15_y2.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、B/Cアンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z15-y2-boundary-20261119/output/audit.json
  role: data
  note: 13,820,279照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/experiments/vertical-fiber-two-token-z15-y2-boundary-20261119/census_z15_y2.py
  role: verifier
  note: x=2..45・R=0..x+45の生二再帰センサス（二エンジン一致・閉形式一致・tail）で行表を第三導出から照合する
- path: research/experiments/vertical-fiber-two-token-z15-y2-boundary-20261119/output/census.txt
  role: data
  note: センサスの決定論的出力（二回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z15-y2-boundary.md
  role: log
  note: 最新main確認、z=15・y=2切片の選定・証明・監査・次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=15、y=2、
  全x>=2・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=2では二つのトークン減少手が同じ(1,2);15多重集合子に
  合流し、K1020のx=2行を帰納基底として使う。x>=3ではA子を帰納仮説、
  B子をK1020のz=15,y=1全称公式、C子を1 xor K1028のz=14,y=2全称公式で
  評価する。全R>=1はreport.mdの過渡行x=2..19と定常行x>=20（偶数）・
  x>=21（奇数）のA/B/C署名帯表（帯構造は行偶奇で完全共通・上端のみ
  入替）が互いに素に被覆し、mex表から本文のT/Pが得られる。K0832から
  R<=16の高さのみ縮約とR>=x+18の一般tailも従う。独立監査は順序保持・
  降順正準化の二直接再帰、B/Cアンカー、署名帯、mex、Theorem T、縮約、
  tail、散点を含む13,820,279照合で不一致0、二回実行byte-identical
  （別プロセス・別cwd実行でも同一sha256）。加えて生二再帰センサス
  （x=2..45・R=0..x+45）が行表・閉形式・tailを第三導出から照合して0不一致。
  有限監査は転写・実装照合であり、全称性はx外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \\(x\\ge2\\)、\\(R\\ge0\\) について、\\(H(R;(x,2);15)\\) のGrundy値0/1/2を
report.mdの \\(T(x),P(x)\\) で完全分類する。低残容量は \\(R\\le16\\) で単一トークン
\\(x+2\\) へ縮約し、高残容量は \\(R\\ge x+18\\) で \\((x+2)\\bmod2\\) となる。

値2位置はx=2で{1,3}、x=3,4でO[1,5]、x=5,6でO[1,7]、x=7,8でO[1,9]、
x=9,10でO[1,11]、x=11,12でO[1,13]、x=13（h=z行）でO[1,17]
（孤立上端17=2y+(d+z)/2=4+13でd=11=x-y、d+z=26≡2 (mod 4)。
奇数zのh=z行孤立上端としてK1025のz=13・x=11上端15（d=9・d+z=22≡2）に続く
2例目）、x=14,15,16でO[1,15]、x=17でO[1,15]∪{19}
（前倒し点19=d格子値2y+(d+z)/2=4+15=2y+z=pinに一致・d=15・d+z≡2 (mod 4)・
掃引行の1行手前）、x=18の掃引行でO[1,15]∪O[19,35]=O[1,z]∪O[pin,x+y+z]、
x≥19でO[1,15]∪{19}に定着する（pin=19=2y+z・奇数zラダーO[1,z]）。
値1位置は偶数x<=12で空、奇数x=3,5,7,9,11でI[x+3,∞)、x=13,15で
{16}∪I[18,∞)、x=14で{16}、x=16で{16,18}、x=17で{16,18}∪I[20,∞)、
x=18で{16,18}、奇数x>=19で{16,18}∪O[21,x+16]∪I[x+18,∞)、
偶数x>=20で{16,18}∪O[21,x+17]（有限）。
値1基底点は{16,18}={z+1,z+3}でy点仮説の2点型3例目
（K1019の{13,15}・K1025の{14,16}に続き、奇数zでは2例目）、値1中間帯は
z+2y+2=21開始で偶奇がzに追従する奇数位置帯、無限I帯は奇数x行のみで
tail R>=x+18の値(x+2) mod 2が1になる行と一致する
（「I帯はtail値1の行にだけ現れる」一般則の確認）。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。x=2では二つのトークン減少手が
同じ(1,2);15多重集合子に合流し、K1020のx=2行を帰納基底として使う。
x>=3ではA子を帰納仮説、B子をK1020、C子を1⊕K1028で評価する。
R<=16はK0832の高さのみ縮約、R>=x+18はK0832の一般tailで閉じる。
独立監査は13,820,279照合・不一致0・二回実行byte-identical
（検証器SHA-256 `7eae4c0701f5bccc8bec932ae48ccf172716f937fe63a047024315bb03f8079d`、
ハッシュ除外フィールドSHA-256 `5c6c417459ea3c49829f7088dbfa3ab156cbc755566ccfe588dd3709391ad0f2`、
audit.json全文SHA-256 `89a383101009e3d814682e6f759bfd8d8e4f52d3a348775611cbde52f813e828`）。
別プロセス・別cwd実行でも同一sha256。生二再帰センサス（x=2..45）も
行表・閉形式・tailを第三導出から照合して0不一致
（census.txt SHA-256 `83c6303f0e8ab3ab2932217a7eb7930e3fbde376b292098dd8a4b8db92ac60b1`）。
有限監査は転写・実装照合であり、全称性は帰納証明が担う。

## 未解決

z=15のy=3（B=本項・C=1⊕K1030で両子出版済み）、z=13・z=14のy=5
（C子(12,5)未出版で着手不能）、y≥2族の一般化、値1基底点y点仮説
{z+1,z+3,...,z+2y-1}の一般証明、標準二次元盤の固定幅・q点安定化長。
