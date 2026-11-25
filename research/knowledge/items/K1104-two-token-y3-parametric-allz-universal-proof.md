---
id: K1104
title: 2トークン残余ゲーム y=3族のパラメトリック閉形式の全称証明（全z>=0・全x>=3・全R>=0）
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token y=3 parametric all-z universal proof, P3]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・Theorem T・単一トークン閉形式のraw anchorに使用する
- type: depends_on
  target: K1099
  note: B子（y=2子）の評価にy=2パラメトリック全z全称閉形式cand2を使用する（x=3合流子も同一）
- type: generalizes
  target: K0879
  note: z=6・y=3切片は本項の特殊例
- type: generalizes
  target: K0979
  note: z=7・y=3切片は特殊例
- type: generalizes
  target: K0986
  note: z=8・y=3切片は特殊例
- type: generalizes
  target: K0989
  note: z=9・y=3切片は特殊例
- type: generalizes
  target: K1005
  note: z=10・y=3切片は特殊例
- type: generalizes
  target: K1014
  note: z=11・y=3切片は特殊例
- type: generalizes
  target: K1021
  note: z=12・y=3切片は特殊例
- type: generalizes
  target: K1026
  note: z=13・y=3切片は特殊例
- type: generalizes
  target: K1030
  note: z=14・y=3切片は特殊例
- type: generalizes
  target: K1034
  note: z=15・y=3切片は特殊例
- type: generalizes
  target: K1050
  note: z=16・y=3切片は特殊例
- type: generalizes
  target: K1067
  note: z=17・y=3切片は特殊例
- type: generalizes
  target: K1078
  note: z=18・y=3切片は特殊例（candidate_T/Pを逐語アンカーとして照合）
- type: generalizes
  target: K1098
  note: z=19・y=3切片は特殊例（candidate_T/Pを逐語アンカーとして照合）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y3-parametric-allz-proof-20261120/report.md
  role: proof
  note: z偶奇別T/Pパラメトリック集合表による全称定理と、マージ系（対角線下・y=3の全称昇格）・選択肢分解・恒等式・型機械による証明構成、出版切片アンカー、基底点・pin偶奇分離・掃引帯・tailの全z一般化
- path: research/experiments/vertical-fiber-two-token-y3-parametric-allz-proof-20261120/verify_y3_universal.py
  role: verifier
  note: 12チェック3,777,544照合点（マージ系1,818,314点）・不一致0・実現型10,850・2回実行＋別cwdでaudit.json byte-identical・純Python約19秒
- path: research/experiments/vertical-fiber-two-token-y3-parametric-allz-proof-20261120/census_rows.py
  role: verifier
  note: z=0..80・x=3..70・R<=x+z+12の生二重再帰センサス、492,966点で両エンジンと閉形式の三方一致・マージ行262,956点・tail一致・別cwd byte-identical
- path: research/experiments/vertical-fiber-two-token-y3-parametric-allz-proof-20261120/output/audit.json
  role: data
  note: 検証器の決定論的監査出力（固定seed・ソート済みキー・SHA-256 dcb163958d0abec06b36dd163b392c9a844c2973b91efb85b6cae44b7ae57a1b）
- path: research/experiments/vertical-fiber-two-token-y3-parametric-allz-proof-20261120/output/census.txt
  role: data
  note: センサスの決定論的行表出力（SHA-256 860d60a3f0636e806bdcdade317d3813d905643c96a11be2121d0b94a58e548b）
- path: research/log/2026-11-20-two-token-y3-parametric-allz-proof.md
  role: log
  note: 最新main・単一オーナー・並走状況の確認、y=3族の選定・導出・出版済み切片との差分化・出版記録
- path: research/log/2026-11-20-two-token-y3-parametric-allz-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit b7a9f7c6a3・先行出版）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,3)、全z>=0・全x>=3・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式）で完全分類する。
  K0879/K0979/K0986/K0989/K1005/K1014/K1021/K1026/K1030/K1034/K1050/K1067/K1078/K1098の
  固定z切片（z=6..19）は本項の特殊例であり、z>=20のy=3切片も主張に含まれる。
  系としてx<=z-4（S=x+3<z）の全R行が単一トークン値single_token(x+3,z,R)
  に一致するマージ命題のy=3版が全称に昇格する。
evidence: >-
  証明は3部構成。(1) 選択肢分解：A子=H(R-1;(x-1,3);z)（x>=4）、
  B子=K1099のy=2全称閉形式cand2、C子=1 xor cand3(z-1,x,R-1)。x=3では
  2つのトークン減少手が同一多重集合(2,3)子に合流しA≡B=K1099のx=3行に
  なる。この分解が素再帰の選択肢値集合と一致することをraw二重再帰
  （順序保持・降順正準化）で錨止めする（C3・1,652点）。単一トークン
  閉形式・y=2子・x=3合流子もraw錨（C1b・108,949点）。(2) 恒等式：
  cand3(z,x,R)=mex{A,B,C}（子は閉形式評価・Cはz外帰納）がR帰納の本体で、
  z=0..48×x=3..56×R<=x+z+40の247,401点、深部tail z∈{60,..,400}の10,350点、
  z=0..120×x=3..120×R<=x+z+16の1,963,225点等で直接照合する。
  (3) 型機械：型=(x==3,z==0,z%2,x%2,R%2,6差分族w0..w5の±8窓±9番兵)、
  自由座標(v0,v1,v3)=±60ボックスで実現型10,850個を完全列挙し、
  型内confluenceと証人恒等式を機械検証（656,609点）。ボックス外新規型
  ゼロをv空間シェル掃引936,714点（max|v|∈[61,64]∪[89,92]∪[117,120]）、
  境界多様体393,902点（z∈{0..5,29..31,59..61,299..301,999..1001,2999,3000}）、
  seeded遠方probe 200,000点（z,x<=3000・R<=9000・seed 20261120）、
  深グリッド掃引で確認した。既出版のz=18（K1078）・z=19（K1098）の
  candidate候補を逐語転写して各5,239点全一致（C1d）。生エンジン直接照合
  C1がz=0..14・x=3..26・R<=x+z+45の24,300点。監査計3,777,544照合点
  （マージ系1,818,314点）・全チェック不一致0・2回実行＋別cwd別ディレクトリで
  audit.json byte-identical。加えて生二重再帰センサスcensus_rows.pyが
  z=0..80・x=3..70・R<=x+z+12の492,966点で両エンジン・閉形式の三者一致、
  マージ行262,956点のsingle_token一致、tail R>=x+z+4の(x+3)mod2を確認し、
  census.txtもbyte-identical再生する。有限監査は転写・実装照合であり、
  全称性は選択肢分解の健全性・正確なmex恒等式・有限型空間の完全性
  （K1023/K1099と同一trust境界）による。
---

## 命題・範囲

すべての z>=0、x>=3、R>=0 に対して H(R;(x,3);z)=cand3(z,x,R) が成り立つ。
cand3 は z 偶奇別のパラメトリック T/P 集合表（report.md に全文掲載）で、
値2位置はマージ行 O[1, q_odd(x+3)]（x<=z-4）、対角行・過渡行の
O[1, z±定数]、掃引行 x=z+4 の O[z+6, 2z+7]（奇z）/O[z+7, 2z+7]（偶z）、
定常pin {z+6}（奇z）/ z+7（偶z）に整理される。値1位置は基底点
{z+1, z+3, z+5}（y=3 で y 点仮説の全 z 確定）、中間帯 O_z[z+8, x+z+3]、
偶数x行の無限帯 I[x+z+4, ∞) で、tail R>=x+z+4 は (x+3) mod 2。
z=0..3 でも例外行なし。奇数 z では前倒し孤立pin {z+4} が x=z-1 行に
現れる（y=2 にはなかった x<z 側の pin）。

## マージ系（対角線下・y=3 の全称昇格）

x<=z-4（S=x+3<z）の全行で H(R;(x,3);z)=single_token(x+3,z,R)（全R）。
行全体が z 非依存になる。K1101 が y∈{1,2} で全称証明し、y>=3 を
有限センサス観察（2トークン y=1..40・z<=40・348,270点・不一致0）に
とどめていたマージ命題の y=3 版が、本項の閉形式から系として全称に
昇格した（監査上も 1,818,314 点で独立照合・不一致 0）。

## 出版切片との関係

y=3 固定z境界切片 K0879(z=6), K0979(z=7), K0986(z=8), K0989(z=9),
K1005(z=10), K1014(z=11), K1021(z=12), K1026(z=13), K1030(z=14),
K1034(z=15), K1050(z=16), K1067(z=17), K1078(z=18), K1098(z=19) は
本項の z 行の特殊例である。K1078/K1098 の candidate 関数は検証器に
逐語転写して全点一致を確認した。z>=20 の y=3 行は本項が直接分類する
ため、以後の y=3 スライス出版は不要。z<=5 の y=3 行は C1 の
raw 直接照合（z=0..14 グリッド）に含まれる。

## 導かれる構造（全z確定・y=1..3 横断観察）

- 値1基底点 {z+1,z+3,z+5} は y 点仮説の y=3 版が全 z>=0 で成立
  （y 個の基底点: y=1 は {z+1}・y=2 は {z+1,z+3}・y=3 は 3 点）。
- pin の偶奇分離: 奇数 z は前倒し pin 2y+z-2（x=z-1 行）と pin 2y+z
  （x=z+3 行・掃引起点・定常）、偶数 z は前倒し pin 2y+z-1（x=z+1 行）
  ・定常 pin 2y+z+1 の分離。y=2 の前倒し pin が現れる行位置は
  x=z+y-2 に一般化して現れる（y=2: x=z、y=3: x=z+1）。
- 掃引行 x=z+y+1 とその帯 O[2y+z, 2z+2y+1]（奇z）/O[2y+z+1, 2z+2y+1]（偶z）。
- tail 開始は x+z+2y-2 で、y=2 の x+z+2y-1 と異なる。y=3 で初めて
  y=2 のパターンから外れるため、tail 開始の一般式は y=4 の全称表が決め手。
- 対角行（S=z・偶z）は O[1, z+2y-3] 連続上端で値1なし。

これらの横断法則は y=1..3 の全称表からの観察であり、y>=4 での
一般証明は含意しない。

## 現在の根拠と限界

全称性は (i) 選択肢分解の健全性（raw錨）・(ii) 正確な mex 恒等式の有限
グリッド照合と型ごとの機械検査・(iii) 実現型空間の有限性（ボックス完全
列挙＋シェル・多様体・遠方probe・深掃引で新規型ゼロ）に基づく。
K1023/K1099 と同一の trust 境界にあり、Lean 形式化ではない。H の定義は
K0832、B子の評価は K1099（さらに K1023）に依存する。y>=4 族、基底点
y 点仮説と d+z 剰余格子規則の一般証明、tail 開始の一般式、3トークン以上、
低R縮約の一般化、固定幅・q点版安定化長、11×11 は範囲外。
