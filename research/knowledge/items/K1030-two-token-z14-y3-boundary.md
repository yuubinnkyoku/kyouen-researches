---
id: K1030
title: 2トークン残余ゲーム z=14・y=3境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z14 y3 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1028
  note: B子の評価とx=3帰納基底にz=14・y=2境界切片を使用する
- type: depends_on
  target: K1026
  note: C子の評価にz=13・y=3境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z14-y3-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z14-y3-boundary-20261119/verify_z14_y3.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、B/Cアンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z14-y3-boundary-20261119/output/audit.json
  role: data
  note: 13,819,399照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/experiments/vertical-fiber-two-token-z14-y3-boundary-20261119/census_z14_y3.py
  role: verifier
  note: x=3..45・R=0..x+45の生二再帰センサス（二エンジン一致・閉形式一致・tail）で行表を第三導出から照合する
- path: research/experiments/vertical-fiber-two-token-z14-y3-boundary-20261119/output/census.txt
  role: data
  note: センサスの決定論的出力（二回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z14-y3-boundary.md
  role: log
  note: 最新main確認、z=14・y=3切片の選定・証明・監査・次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=14、y=3、
  全x>=3・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=3では二つのトークン減少手が同じ(2,3);14多重集合子に
  合流し、K1028のx=3行を帰納基底として使う。x>=4ではA子を帰納仮説、
  B子をK1028のz=14,y=2全称公式、C子を1 xor K1026のz=13,y=3全称公式で
  評価する。全R>=1はreport.mdの過渡行x=3..19と定常行x>=20（奇偶共通構造・
  帯上端のみ行偶奇でx+16/x+17入替）のA/B/C署名帯表が互いに素に被覆し、
  mex表から本文のT/Pが得られる。K0832からR<=15の高さのみ縮約と
  R>=x+18の一般tailも従う。独立監査は順序保持・降順正準化の二直接再帰、
  B/Cアンカー、署名帯、mex、Theorem T、縮約、tail、散点を含む
  13,819,399照合で不一致0、二回実行byte-identical（別プロセス・別cwd
  実行でも同一sha256）。加えて生二再帰センサス（x=3..45・R=0..x+45）が
  行表・tailを第三導出から照合して0不一致。有限監査は転写・実装照合であり、
  全称性はx外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \(x\ge3\)、\(R\ge0\) について、\(H(R;(x,3);14)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le15\) で単一トークン
\(x+3\) へ縮約し、高残容量は \(R\ge x+18\) で \((x+3)\bmod2\) となる。

値2位置はx=3で{1,3,5}、x=4,5でO[1,7]、x=6,7でO[1,9]、x=8,9でO[1,11]、
x=10でO[1,13]、x=11（高さx+y=z行）でO[1,17]
（上端17=d格子値2y+(d+z)/2=6+11でd=8=x-y、d+z≡2 (mod 4)。偶数zではh=z行の
孤立上端として現れるK1016のx=11上端13・K1018のx=13上端15・K1028のx=12上端15
に続く4例目）、x=12,13,14,16,17でO[1,13]、x=15でO[1,13]∪{19}
（前倒し点19=d格子値2y+(d+z)/2=6+13でd=12=x-y・K1028のx=14前倒し17と同じ
d=12格子）、x=18の掃引行でO[1,13]∪O[21,35]=O[1,z-1]∪O[pin,x+y+z]、
x≥19でO[1,13]∪{21}に定着する（pin=21=2y+z+1・偶数zラダーO[1,z-1]）。
値1位置は奇数x<=11で空、偶数x<=10でI[x+4,∞)、x=12で{15}∪I[17,∞)、
x=13,15で{15,17}、x=14,16で{15,17}∪I[19,∞)、x=17で{15,17,19}、
x=18で{15,17,19}∪E[22,34]∪I[36,∞)、奇数x>=19で{15,17,19}∪E[22,x+17]、
偶数x>=20で{15,17,19}∪E[22,x+18]∪I[x+19,∞)。
値1基底点は{15,17,19}={z+1,z+3,z+5}でy点仮説の3点型の2例目・偶数zでは
初例（K1026の{14,16,18}の偶数z対応）、中間帯はz+2y+2=22から偶奇z追従の
偶数帯で現れ、無限I帯は偶数x行のみでtail R>=x+18の値\((x+3)\bmod2\)
=1と一致する。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。x=3では二つのトークン減少手が
同一の(3,2);14多重集合子に合流し、K1028のx=3行を帰納基底として使う。
B子はK1028、C子はK1026の全称定理であり、低R縮約・一般tail・Theorem Tは
K0832から従う。署名帯の定常化はx>=20偶数/x>=21奇数（x=16は偶数帯署名023の
疑似掃引前行、x=17は偶数帯123/1交互の前行、x=18掃引行、x=19は偶数帯02が
E[22,x+17]まで続く移行行）。定常行（x>=20）の署名帯構造は行偶奇で完全共通で、
帯の上端だけが行の偶奇でx+16/x+17に入れ替わる。これはK1028の監査で
観察された「署名帯はR<=x+16でなくR<=x+17まで機械照合可能・x>=19で奇偶共通
構造」の精緻化と整合し、今回の掃引行+1系列（掃引x=z+y+1=18、帯域R<=x+17=S、
tail R>=x+18）で一般化が機械確認された。両子K1028・K1026のverifyスクリプトは
repoに存在しCIで監査済み。有限監査は二直接再帰・子アンカー・署名帯・mex等の
転写を照合するもので、証明そのものではない。

z=14のy=4（B子=本項・C子=1 xor K1027で着手可能）、z=15のy=2
（B子=K1020・C子=1 xor K1028で着手可能）、z=13のy>=5
（C子(z=12,y=5)が未出版）、y>=4族のパラメトリック機械化、値1基底点のy点仮説
の一般証明、標準二次元盤の固定幅・q点版安定化長は未解決。
