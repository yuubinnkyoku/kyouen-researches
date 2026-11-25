---
id: K1099
title: 2トークン残余ゲーム y=2族のパラメトリック閉形式の全称証明（全z>=0・全x>=2・全R>=0）
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token y=2 parametric all-z universal proof, P2]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・Theorem T・単一トークン閉形式のraw anchorに使用する
- type: depends_on
  target: K1023
  note: B子・x=2のA子の評価にy=1パラメトリック全z全称公式cand/cand0を使用する
- type: generalizes
  target: K0878
  note: z=6・y=2切片は本項の特殊例
- type: generalizes
  target: K1004
  note: z=10・y=2切片は特殊例
- type: generalizes
  target: K1013
  note: z=11・y=2切片は特殊例
- type: generalizes
  target: K1019
  note: z=12・y=2切片は特殊例
- type: generalizes
  target: K1025
  note: z=13・y=2切片は特殊例
- type: generalizes
  target: K1028
  note: z=14・y=2切片は特殊例
- type: generalizes
  target: K1032
  note: z=15・y=2切片は特殊例
- type: generalizes
  target: K1042
  note: z=16・y=2切片は特殊例
- type: generalizes
  target: K1044
  note: z=17・y=2切片は特殊例
- type: generalizes
  target: K1051
  note: z=18・y=2切片は特殊例
- type: generalizes
  target: K1052
  note: z=19・y=2切片は特殊例
- type: generalizes
  target: K1053
  note: z=20・y=2切片は特殊例
- type: generalizes
  target: K1054
  note: z=21・y=2切片は特殊例
artifacts:
- path: research/experiments/vertical-fiber-two-token-y2-parametric-allz-proof-20261120/report.md
  role: proof
  note: z偶奇別T/Pパラメトリック集合表による全称定理と、選択肢分解・恒等式・型機械による証明構成、出版切片アンカー、基底点・pin偶奇分離・掃引帯・tailの全z一般化
- path: research/experiments/vertical-fiber-two-token-y2-parametric-allz-proof-20261120/verify_p2_universal.py
  role: verifier
  note: 12チェック4,573,605照合点・不一致0・実現型11,090・2回実行＋別cwdでaudit.json byte-identical・純Python約21秒
- path: research/experiments/vertical-fiber-two-token-y2-parametric-allz-proof-20261120/census_rows.py
  role: verifier
  note: z=0..80・x=2..70・R<=x+z+12の生二重再帰センサス、497,421点で両エンジンと閉形式の三者一致・tail一致・別cwd byte-identical
- path: research/experiments/vertical-fiber-two-token-y2-parametric-allz-proof-20261120/output/audit.json
  role: data
  note: 検証器の決定論的監査出力（固定seed・ソート済みキー・SHA-256 84198f02bfcd2a5efc9610b6207359d87a87790e591c1e7109c900c72ca5a397）
- path: research/experiments/vertical-fiber-two-token-y2-parametric-allz-proof-20261120/output/census.txt
  role: data
  note: センサスの決定論的行表出力（SHA-256 e007bc784f1da2c352c2081a6aaea27c9cd0f57aba11074a5064ea59795f7129）
- path: research/log/2026-11-20-two-token-y2-parametric-allz-proof.md
  role: log
  note: 最新main・単一オーナー・並走状況の確認、y=2族の選定・導出・出版済み切片との差分化・出版記録
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,2)、全z>=0・全x>=2・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式）で完全分類する。
  K0878/K1004/K1013/K1019/K1025/K1028/K1032/K1042/K1044/K1051/K1052/K1053/K1054の
  固定z切片（z=6..21）は本項の特殊例であり、z>=22のy=2切片も主張に含まれる。
evidence: >-
  証明は3部構成。(1) 選択肢分解：A子=H(R-1;(x-1,2);z)（x>=3）、
  B子=K1023のy=1全称閉形式（z=0はcand0）、C子=1 xor cand2(z-1,x,R-1)。
  x=2では2つのトークン減少手が同一多重集合(1,2)子に合流しA≡B=K1023の
  x=2行になる。この分解が素再帰の選択肢値集合と一致することをraw二重再帰
  （順序保持・降順正準化）で錨止めする。単一トークン閉形式とy=1子もraw錨。
  (2) 恒等式：cand2(z,x,R)=mex{A,B,C}（子は閉形式評価）がR帰納の本体で、
  z=0..48×x=2..56×R<=x+z+40の250,635点、z<=400の深部tail 10,294点、
  z=0..120×x=2..120×R<=x+z+16の1,972,663点等で直接照合する。
  (3) 型機械：型=(x==2,z==0,z%2,x%2,R%2,6差分族w0..w5の±8窓±9番兵)、
  自由座標(v0,v1,v3)=±60ボックスで実現型11,090個を完全列挙し、
  型内confluence（値と子値列の一定性）と証人恒等式を機械検証。ボックス外
  新規型ゼロをv空間シェル掃引938,934点（max|v|∈[61,120]）、境界多様体
  394,085点（z∈{0..5,29..31,59..61,299..301,999..1001,2999,3000}）、
  seeded遠方probe 200,000点（z,x<=3000・R<=9000）で確認した。既出版の
  z=16（K1042）・z=17（K1044）census候補を逐語転写して各5,292点全一致。
  監査計4,573,605照合点・全チェック不一致0・2回実行＋別cwd別ディレクトリで
  audit.json byte-identical。加えて生二重再帰センサスcensus_rows.pyが
  z=0..80・x=2..70・R<=x+z+12の497,421点で両エンジン・閉形式の三者一致と
  tail R>=x+z+3の(x+2)mod2を確認し、census.txtもbyte-identical再生する。
  有限監査は転写・実装照合であり、全称性は選択肢分解の健全性・正確なmex
  恒等式・有限型空間の完全性（K1023と同一trust境界）による。
---

## 命題・範囲

すべての z>=0、x>=2、R>=0 に対して H(R;(x,2);z)=cand2(z,x,R) が成り立つ。
cand2 は z 偶奇別のパラメトリック T/P 集合表（report.md に全文掲載）で、
値2位置はラダー O[1,2⌈x/2⌉+1]、境界帯 O[1,z±1]、掃引行 x=z+3 の
O[2y+z^(±),2z+5]、定常pin {2y+z+z%2...} に整理される。値1位置は
基底点 {z+1,z+3}、中間帯 O_z[z+6,x+z+3±1]、奇数x行の無限帯
I[x+z+4,∞) で、tail R>=x+z+3 は (x+2) mod 2。z=0,1,2 でも例外行なし。

## 出版切片との関係

y=2 固定z境界切片 K0878(z=6), K1004(z=10), K1013(z=11), K1019(z=12),
K1025(z=13), K1028(z=14), K1032(z=15), K1042(z=16), K1044(z=17),
K1051(z=18), K1052(z=19), K1053(z=20), K1054(z=21) は本項の z 行の
特殊例である。K1042/K1044 の census 候補関数は検証器に逐語転写して
全点一致を確認した。K1054 が「次の一手」としていた z=22・y=2 切片を含む
全 z>=22 の y=2 行は本項が直接分類するため、以後の y=2 スライス出版は不要。
K1019..K1054 の「y>=2族の一般化」の課題は y=2 に限って解決した。

## 導かれる構造（全z確定）

- 値1基底点 {z+1,z+3} は y 点仮説の y=2 版が全 z>=0 で成立
  （z=12..21 の10連続観測の全 z 拡張。x=z-1行とx=z行は {z+1} のみに変形）。
- pin の偶奇分離：奇数 z は x=z-2 行の連続上端 z+2 と x=z+2 行の pin 2y+z が
  d+z≡2 (mod 4) 側で合流、偶数 z は上端 2y+z-3・前倒しpin 2y+z-1（x=z行）・
  定常pin 2y+z+1 の3点分離（K1042/K1051/K1053 記述の全 z 確定）。
- 掃引行 x=z+y+1 とその帯 O[2y+z,2z+5]（奇数z）/O[2y+z+1,2z+5]（偶数z）。
- tail 開始 x+2y-1。

## 現在の根拠と限界

全称性は (i) 選択肢分解の健全性（raw錨）・(ii) 正確な mex 恒等式の有限
グリッド照合と型ごとの機械検査・(iii) 実現型空間の有限性（ボックス完全
列挙＋シェル・多様体・遠方probe・深掃引で新規型ゼロ）に基づく。
K1023 と同一の trust 境界にあり、Lean 形式化ではない。H の定義は K0832、
B子の評価は K1023 に依存する。y=3 以降の族、y>=2 の基底点仮説と d+z 剰余
格子規則の一般証明、低R高さのみ縮約の一般化、固定幅・q点版安定化長、
11×11 は範囲外。
