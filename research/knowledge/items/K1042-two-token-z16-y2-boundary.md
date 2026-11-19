---
id: K1042
title: 2トークン残余ゲーム z=16・y=2境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z16 y2 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1023
  note: B子の評価とx=2帰納基底にy=1パラメトリック全z全称公式（z=16行）を使用する
- type: depends_on
  target: K1032
  note: C子の評価に1⊕(z=15・y=2境界切片)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z16-y2-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z16-y2-boundary-20261119/verify_z16_y2.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、B/Cアンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z16-y2-boundary-20261119/output/audit.json
  role: data
  note: 13,821,278照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/experiments/vertical-fiber-two-token-z16-y2-boundary-20261119/census_z16_y2.py
  role: verifier
  note: x=2..45・R=0..x+45の生二再帰センサス（二エンジン一致・閉形式一致・tail）で行表を第三導出から照合する
- path: research/experiments/vertical-fiber-two-token-z16-y2-boundary-20261119/output/census.txt
  role: data
  note: センサスの決定論的出力（二回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z16-y2-boundary.md
  role: log
  note: 最新main確認、K番号再採番と環境リセットからの再構築経緯、証明・監査・次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=16、y=2、
  全x>=2・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=2では二つのトークン減少手が同じ(1,2);16多重集合子に
  合流し、K1023のz=16行を帰納基底として使う。x>=3ではA子を帰納仮説、
  B子をK1023のy=1パラメトリック全称公式（z=16）、C子を1 xor K1032の
  z=15,y=2全称公式で評価する。全R>=1はreport.mdの過渡行x=2..20と
  定常行x>=21のA/B/C署名帯表（帯構造は行偶奇で完全共通・上端のみ
  入替）が互いに素に被覆し、mex表から本文のT/Pが得られる。K0832から
  R<=17の高さのみ縮約とR>=x+19の一般tailも従う。独立監査は順序保持・
  降順正準化の二直接再帰、B/Cアンカー、署名帯、mex、Theorem T、縮約、
  tail、散点を含む13,821,278照合で不一致0、二回実行byte-identical
  （別プロセス・別cwd実行でも同一sha256）。加えて生二再帰センサス
  （x=2..45・R=0..x+45）が行表・閉形式・tailを第三導出から照合して0不一致。
  有限監査は転写・実装照合であり、全称性はx外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \\(x\\ge2\\)、\\(R\\ge0\\) について、\\(H(R;(x,2);16)\\) のGrundy値0/1/2を
report.mdの \\(T(x),P(x)\\) で完全分類する。低残容量は \\(R\\le17\\) で単一トークン
\\(x+2\\) へ縮約し、高残容量は \\(R\\ge x+19\\) で \\((x+2)\\bmod2\\) となる。

値2位置はx=2で{1,3}、x=3,4でO[1,5]、x=5,6でO[1,7]、x=7,8でO[1,9]、
x=9,10でO[1,11]、x=11,12でO[1,13]、x=13,15,17,18でO[1,15]、
x=14（h=z行）でO[1,17]（孤立上端17=q_odd(2y+(d+z)/2)=q_odd(18)。
d=12=x-y、d+z=28≡0 (mod 4)。偶数z型h=z行孤立上端としてK1028のz=14・x=12
上端15（q_odd(16)）・K1031のz=14・y=4・x=10上端17に続く3例目）、
x=16でO[1,15]∪{19}（前倒しd格子点19=2y+(d+z)/2=4+15、d=14、
d+z=30≡2 (mod 4)。K1028のz=14・x=14前倒し点17と同じx=z行の型で偶数zでは
2例目。奇数zではこの点がx=z+yのpin行に現れるのと対照的にラダーpin
2y+z+1=21と分離）、x=19の掃引行でO[1,15]∪O[21,37]=O[1,z]∪O[pin,x+y+z]、
x≥20でO[1,15]∪{21}に定着する（pin=21=2y+z+1・偶数zラダーO[1,z]）。
値1位置は偶数x<=14で空、奇数x=3,5,7,9,11,13でI[x+3,∞)、x=15,17で
{17,19}∪I[20,∞)、x=16で{17}、x=18で{17,19}、奇数x>=19で
{17,19}∪E[22,x+19]∪I[x+20,∞)、偶数x>=20で{17,19}∪E[22,x+18]（有限）。
値1基底点は{17,19}={z+1,z+3}でy点仮説の2点型5例目
（K1019の{13,15}・K1025の{14,16}・K1028の{15,17}・K1032の{16,18}に続き、
y=2ではz=12..16の5連続・偶数zでは3例目）、値1中間帯は
z+2y+2=22開始で偶奇がzに追従する偶数位置帯、無限I帯は奇数x行のみで
tail R>=x+19の値(x+2) mod 2が1になる行と一致する
（「I帯はtail値1の行にだけ現れる」一般則のy=2・偶数z型確認）。

## 現在の根拠と限界

全称性はx外帰納と、全R（1<=R<=x+17=tail-1）を覆う明示的なA/B/C署名帯表・mex対応表による。
x=2では二つのトークン減少手が同じ(1,2);16多重集合子に合流し、K1023のz=16行を帰納基底として使う。
x>=3ではA子を帰納仮説、B子をK1023、C子を1⊕K1032で評価する。
R<=17はK0832の高さのみ縮約、R>=x+19はK0832の一般tailで閉じる。
独立監査は13,821,278照合・不一致0・二回実行byte-identical
（検証器SHA-256 `c65176514c5d8d163a892c8a278a16b8d5a59e140009eef44f315f3c4b4842a5`、
ハッシュ除外フィールドSHA-256 `f1ba8670834c1a9bcb3ae142d67ff0f33c9263748e8cc88d616a1fdaeb512ea0`、
audit.json全文SHA-256 `e5b47fc87f95873ed182106006ccdb1b540e72e18622bc8811f0e61689fcc7b2`）。
別プロセス・別cwd実行でも同一sha256。生二再帰センサス（x=2..45）も
行表・閉形式・tailを第三導出から照合して0不一致
（census.txt SHA-256 `c78c365f84eb93b386fd4f026452589b3d186399136cb200dc80804c509e8a59`）。
有限監査は転写・実装照合であり、全称性は帰納証明が担う。

本項でも、h=z行上端のq_odd丸め（d+z≡0 mod 4）とx=z行前倒し点（d+z≡2 mod 4）が
同一スライス内に分離して現れる偶数z構造（K1028のz=14と同型）を確認した。
d+z mod 4による2値格子規則の一般証明は未解決のまま。

## 未解決

z=16のy=3（B=K1023・C=1⊕K1034で両子出版済み）、z=17のy=2（B=K1023・C=1⊕本項）、
y≥2族の一般化、値1基底点y点仮説{z+1,z+3,...,z+2y-1}の一般証明、
h=z行孤立上端とx=z行前倒し点のd+z mod 4格子規則の一般証明、
標準二次元盤の固定幅・q点安定化長。
