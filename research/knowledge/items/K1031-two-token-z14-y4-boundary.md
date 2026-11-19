---
id: K1031
title: 2トークン残余ゲーム z=14・y=4境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z14 y4 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1030
  note: B子の評価とx=4帰納基底にz=14・y=3境界切片を使用する
- type: depends_on
  target: K1027
  note: C子の評価にz=13・y=4境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z14-y4-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z14-y4-boundary-20261119/verify_z14_y4.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、B/Cアンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z14-y4-boundary-20261119/output/audit.json
  role: data
  note: 13,825,029照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/experiments/vertical-fiber-two-token-z14-y4-boundary-20261119/census_z14_y4.py
  role: verifier
  note: x=4..45・R=0..x+45の生二再帰センサス（二エンジン一致・閉形式一致・tail）で行表を第三導出から照合する
- path: research/experiments/vertical-fiber-two-token-z14-y4-boundary-20261119/output/census.txt
  role: data
  note: センサスの決定論的出力（二回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z14-y4-boundary.md
  role: log
  note: 最新main確認、z=14・y=4切片の選定・証明・監査・次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=14、y=4、
  全x>=4・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=4では二つのトークン減少手が同じ(3,4);14多重集合子に
  合流し、K1030のx=4行を帰納基底として使う。x>=5ではA子を帰納仮説、
  B子をK1030のz=14,y=3全称公式、C子を1 xor K1027のz=13,y=4全称公式で
  評価する。全R>=1はreport.mdの過渡行x=4..20と定常行x>=21（奇数）・
  x>=22（偶数）のA/B/C署名帯表（帯構造は行偶奇で完全共通・上端のみ
  入替）が互いに素に被覆し、mex表から本文のT/Pが得られる。K0832から
  R<=15の高さのみ縮約とR>=x+19の一般tailも従う。独立監査は順序保持・
  降順正準化の二直接再帰、B/Cアンカー、署名帯、mex、Theorem T、縮約、
  tail、散点を含む13,825,029照合で不一致0、二回実行byte-identical
  （別プロセス・別cwd実行でも同一sha256）。加えて生二再帰センサス
  （x=4..45・R=0..x+45）が行表・tailを第三導出から照合して0不一致。
  有限監査は転写・実装照合であり、全称性はx外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \(x\ge4\)、\(R\ge0\) について、\(H(R;(x,4);14)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le15\) で単一トークン
\(x+4\) へ縮約し、高残容量は \(R\ge x+19\) で \((x+4)\bmod2\) となる。

値2位置はx=4でO[1,7]、x=5,6でO[1,9]、x=7,8でO[1,11]、x=9でO[1,13]、
x=10（h=z孤立上端）でO[1,17]
（上端17=q_odd(2y+(d+z)/2)=q_odd(18)でd=6=x-y、d+z=20≡0 (mod 4)。
偶数zではq_odd型のh=z行孤立上端としてK1028のx=12上端15に続く2例目）、
x=11,13,14,15,17,18でO[1,13]、x=12でO[1,13]∪{19}
（前倒し点19=d格子値2y+(d+z)/2=8+11でd=8=x-y、d+z≡2 (mod 4)）、
x=16でO[1,13]∪{21}（前倒し点21、d=12、d+z≡2 (mod 4)。y=3では
1点+d=z行端点だったのが、y=4ではd=8とd=12の両格子点が孤立前倒しに）、
x=19の掃引行でO[1,13]∪O[23,37]=O[1,z-1]∪O[pin,x+y+z]、
x≥20でO[1,13]∪{23}に定着する（pin=23=2y+z+1・偶数zラダーO[1,z-1]）。
値1位置は偶数x<=10で空、奇数x=5,7,9でI[x+5,∞)、x=11,13で
{15,17}∪I[19,∞)、x=12で{15,17}、x=14で{15,17,19}、x=15,17で
{15,17,19}∪I[21,∞)、x=16で{15,17,19}、x=18で{15,17,19,21}、
奇数x>=19で{15,17,19,21}∪E[24,x+17]∪I[x+19,∞)、
偶数x>=20で{15,17,19,21}∪E[24,x+18]（有限）。
値1基底点は{15,17,19,21}={z+1,z+3,z+5,z+7}でy点仮説の4点型かつ
**偶数zでは初例**（K1027の{14,16,18,20}の偶数z対応）、中間帯は
z+2y+2=24から偶奇z追従の偶数帯で現れる。無限I帯はy=3とは逆に奇数x行
のみで、これはtail R>=x+19の値(x+4) mod 2が奇数行で1だからである
（「I帯はtail値1の行にだけ現れる」一般則の2例目の確認）。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。x=4では二つのトークン減少手が
同じ(3,4);14多重集合子に合流し、K1030のx=4行を帰納基底として使う。
x>=5ではA子を帰納仮説、B子をK1030、C子を1⊕K1027で評価する。
R<=15はK0832の高さのみ縮約、R>=x+19はK0832の一般tailで閉じる。
独立監査は13,825,029照合・不一致0・二回実行byte-identical
（検証器SHA-256 `b4e7cb094cc79754e6443c4b82973c6b52633c6a942b83bdcc2af447319927ed`、
ハッシュ除外フィールドSHA-256 `f27476e599884b1cabce6e52ac53b45e076bc64bbedfe552fd74d5defccb21dd`、
audit.json全文SHA-256 `c47c61dbab15e6c7f538df71411d892df8c51f444269a1f94b064678b4224869`）。
別プロセス・別cwd実行でも同一sha256。生二再帰センサス（x=4..45）も
行表・閉形式・tailを第三導出から照合して0不一致
（census.txt SHA-256 `5743e31e8ebb5d76a8b0f6cae3959af38d93a4c385baaa9bd1599d6f39641502`）。
有限監査は転写・実装照合であり、全称性は帰納証明が担う。

## 未解決

z=14・y≥6（C子z=13,y=6未出版）、z=15・y≥6（C子z=14,y=6未出版）、z≥16・y≥2、y≥2族の一般化、値1基底点y点仮説
{z+1,z+3,...,z+2y-1}の一般証明、標準二次元盤の固定幅・q点安定化長。
