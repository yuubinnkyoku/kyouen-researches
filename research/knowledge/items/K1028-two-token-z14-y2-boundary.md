---
id: K1028
title: 2トークン残余ゲーム z=14・y=2境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z14 y2 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1018
  note: B子の評価とx=2帰納基底にz=14・y=1境界切片を使用する
- type: depends_on
  target: K1025
  note: C子の評価にz=13・y=2境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z14-y2-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z14-y2-boundary-20261119/verify_z14_y2.py
  role: verifier
  note: 順序保持・正準化の二直接再帰、B/Cアンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z14-y2-boundary-20261119/output/audit.json
  role: data
  note: 13,813,282照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/experiments/vertical-fiber-two-token-z14-y2-boundary-20261119/census_z14_y2.py
  role: verifier
  note: x=2..45・R=0..x+45の生二再帰センサス（二エンジン一致・閉形式全行照合・tail）で行表を第三導出から照合する
- path: research/experiments/vertical-fiber-two-token-z14-y2-boundary-20261119/output/census.txt
  role: data
  note: センサスの決定論的出力（二回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z14-y2-boundary.md
  role: log
  note: 最新main確認、y=2切片の選定・証明・監査・次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=14、y=2、
  全x>=2・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=2では二つのトークン減少手が同じ(1,2);14≡(2,1);14
  多重集合子に合流し、K1018のx=2行を帰納基底として使う。x>=3では
  A子を帰納仮説、B子をK1018のz=14,y=1全称公式、C子を1 xor K1025の
  z=13,y=2全称公式で評価する。全R>=1はreport.mdの過渡行x=2..18と
  定常行x>=19奇数/x>=20偶数のA/B/C署名帯表が互いに素に被覆し、
  mex表から本文のT/Pが得られる。K0832からR<=15の高さのみ縮約と
  R>=x+17の一般tailも従う。独立監査は順序保持・正準化の二直接再帰、
  B/Cアンカー、署名帯、mex、Theorem T、縮約、tail、散点を含む
  13,813,282照合で不一致0、二回実行byte-identical（別プロセス2回でも
  byte-identical）。加えて生二再帰センサス（x=2..45・R=0..x+45）が
  行表・閉形式・tailを第三導出から照合して0不一致。有限監査は転写・
  実装照合であり、全称性はx外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \\(x\\ge2\\)、\\(R\\ge0\\) について、\\(H(R;(x,2);14)\\) のGrundy値0/1/2を
report.mdの \\(T(x),P(x)\\) で完全分類する。低残容量は \\(R\\le15\\) で単一トークン
\\(x+2\\) へ縮約し、高残容量は \\(R\\ge x+17\\) で \\((x+2)\\bmod2\\) となる。

値2位置はx=2で\\{1,3\\}、x=3,4でO[1,5]、x=5,6でO[1,7]、x=7,8でO[1,9]、
x=9,10でO[1,11]、x=11でO[1,13]、x=12（高さx+y=z行）でO[1,15]
（上端15=q_odd(2y+(d+z)/2)=q_odd(16)、d=10、d+z≡0 (mod 4)。偶数zでは
h=z行の孤立上端として現れるK1016のx=11上端13・K1018のx=13上端15と同型）、
x=13でO[1,13]、x=14でO[1,13]∪\\{17\\}（前倒し点17=d格子点2y+(d+z)/2、
d=12=x-y、d+z≡2 (mod 4)）、x=15,16でO[1,13]、x=17の掃引行で
O[1,13]∪O[19,33]=O[1,z-1]∪O[pin,x+y+z]、x≥18でO[1,13]∪\\{19\\}に定着する
（pin=19=2y+z+1・偶数zラダーO[1,z-1]）。
値1位置は偶数x≤12で空、x∈\\{3,5,7,9,11\\}でI[x+3,∞)、x=13,15で\\{15\\}∪I[17,∞)
（中間帯形成前の先駆I帯）、x=14で\\{15\\}、x=16で\\{15,17\\}、
奇数x≥17で\\{15,17\\}∪E[20,x+15]∪I[x+17,∞)、
偶数x≥18で\\{15,17\\}∪E[20,x+16]。値1基底点は
\\{15,17\\}=\\{z+1,z+3\\}（y=1の1点に続き、値1基底点がy点になる仮説の2例目で
K1019の\\{13,15\\}と同じ偶数z型）、中間帯は z+2y+2=20 から偶奇z追従の偶数帯、
無限I帯は奇数x行のみでtail R≥x+17の値 \\((x+2)\\bmod2\\) と一致する。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。x=2では二つのトークン減少手が
同一の(1,2);14≡(2,1);14多重集合子に合流し、K1018のx=2行を帰納基底として使う。
B子はK1018、C子はK1025の全称定理であり、低R縮約・一般tail・Theorem Tは
K0832から従う。前倒し点はx=14の17（d格子点 \\(2y+(d+z)/2\\)、\\(d=12=x-y\\)、
\\(d+z\\equiv2\\pmod4\\)、cross-z監査logのd格子法則どおり）。x=16は偶数帯署名
123/1交互の疑似掃引前行、x=17掃引行、x=18は偶数帯02/1交互の移行行で、
x≥19奇数/x≥20偶数で署名帯は定常化する。両子K1018・K1025のverifyスクリプトは
repoに存在しCIで監査済み。有限監査は二直接再帰・子アンカー・署名帯・mex等の
転写を照合するもので、証明そのものではない。

z=15のy=2（B子はK1020・C子は1 xor本項で着手可能）、z=13のy>=5
（B子は出版済みだがC子(12,5)が未出版）、y>=2族のパラメトリック機械化、
値1基底点のy点仮説の一般証明、標準二次元盤の固定幅・q点版安定化長は未解決。
