---
id: K1112
title: 2トークン残余ゲーム y=4族のパラメトリック閉形式の全称証明（全z>=0・全x>=4・全R>=0）
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token y=4 parametric all-z universal proof, P4]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・Theorem T・単一トークン閉形式のraw anchorに使用する
- type: depends_on
  target: K1104
  note: B子（y=3子）の評価にy=3パラメトリック全z全称閉形式cand3を使用する（x=4合流子も同一）
- type: generalizes
  target: K0880
  note: z=6・y=4切片は本項の特殊例
- type: generalizes
  target: K0980
  note: z=7・y=4切片は特殊例
- type: generalizes
  target: K0987
  note: z=8・y=4切片は特殊例
- type: generalizes
  target: K0990
  note: z=9・y=4切片は特殊例
- type: generalizes
  target: K1006
  note: z=10・y=4切片は特殊例
- type: generalizes
  target: K1015
  note: z=11・y=4切片は特殊例
- type: generalizes
  target: K1024
  note: z=12・y=4切片は特殊例
- type: generalizes
  target: K1027
  note: z=13・y=4切片は特殊例
- type: generalizes
  target: K1031
  note: z=14・y=4切片は特殊例
- type: generalizes
  target: K1048
  note: z=15・y=4切片は特殊例
- type: generalizes
  target: K1064
  note: z=16・y=4切片は特殊例（published closed form を逐語アンカーとして照合）
- type: generalizes
  target: K1076
  note: z=17・y=4切片は特殊例（逐語アンカーとして照合）
- type: generalizes
  target: K1083
  note: z=18・y=4切片は特殊例（逐語アンカーとして照合）
- type: generalizes
  target: K1100
  note: z=19・y=4切片は特殊例（逐語アンカーとして照合）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y4-parametric-allz-proof-20261120/report.md
  role: proof
  note: z偶奇別T/Pパラメトリック集合表による全称定理と、マージ系（対角線下・y=4の全称昇格）・選択肢分解・恒等式・型機械（clip窓±12/番兵±13への拡大が必要だった方法論的発見）による証明構成、出版切片アンカー、tail 開始式 x+z+y+1 の y=2..4 確定
- path: research/experiments/vertical-fiber-two-token-y4-parametric-allz-proof-20261120/verify_y4_universal.py
  role: verifier
  note: 13チェック5,058,763照合点（マージ系1,991,409点）・不一致0・実現型27,722・2回実行＋別cwdでaudit.json byte-identical・純Python約43秒
- path: research/experiments/vertical-fiber-two-token-y4-parametric-allz-proof-20261120/census_rows.py
  role: verifier
  note: z=0..79・x=4..70・R<=x+z+12の生二重再帰センサス、479,720点・エンジン状態数2,414,940・tail一致・別cwd byte-identical
- path: research/experiments/vertical-fiber-two-token-y4-parametric-allz-proof-20261120/output/audit.json
  role: data
  note: 検証器の決定論的監査出力（固定seed・ソート済みキー・SHA-256 c2151805db9db4c3a3062d293d97fbe664033b44291d65b6b33c80d52d329788）
- path: research/experiments/vertical-fiber-two-token-y4-parametric-allz-proof-20261120/output/census.txt
  role: data
  note: センサスの決定論的行表出力（SHA-256 7633c04779881dc2b661d299cd56411f6c04a2ea3ba233ed2885f918a7b6d8b5）
- path: research/log/2026-11-20-two-token-y4-parametric-allz-proof.md
  role: log
  note: 最新main・単一オーナー・並走状況の確認、y=4族の選定・導出・出版済み切片との差分化・出版記録、K1104実験dirのroot誤配置修復記録
- path: research/log/2026-11-20-two-token-y4-parametric-allz-single-owner-note.md
  role: log
  note: 単一オーナー宣言＋予備観察（先行出版・着手時HEAD確認済み）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,4)、全z>=0・全x>=4・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式）で完全分類する。
  K0880/K0980/K0987/K0990/K1006/K1015/K1024/K1027/K1031/K1048/K1064/K1076/K1083/K1100の
  固定z切片（z=6..19）は本項の特殊例であり、z>=20のy=4切片も主張に含まれる
  （以後のy=4スライス出版は不要）。
  系としてx<=z-5（S=x+4<z）の全R行が単一トークン値single_token(x+4,z,R)
  に一致するマージ命題のy=4版が全称に昇格する。tail R>=x+z+5=(x+z+y+1)の
  (x+4) mod 2も全称に含む。
evidence: >-
  証明はK1023/K1099/K1104と同型の3部構成。(1) 選択肢分解：A子=H(R-1;(x-1,4);z)
  （x>=5）、B子=K1104のy=3全称閉形式cand3、C子=1 xor cand4(z-1,x,R-1)。x=4では
  2つのトークン減少手が同一多重集合(3,4)子に合流しA≡B=cand3のz行x=4になる。
  分解が素再帰の選択肢値集合と一致することをraw二重再帰で錨止めする
  （C3・1,470点）。単一トークン閉形式・y=3子・x=4合流子もraw錨（C1b・107,592点）。
  (2) 恒等式：cand4(z,x,R)=mex{A,B,C}（子は閉形式評価・Cはz外帰納）がR帰納の本体で、
  z=0..48×x=4..56×R<=x+z+40の244,118点（マージ・tail系込み）、深部tail
  z∈{60,..,400}の10,398点、z=0..120×x=4..120×R<=x+z+16の1,953,666点等で直接照合。
  (3) 型機械：型=(x==4,z==0,z%2,x%2,R%2,6差分族w0..w5の±12窓±13番兵)、
  自由座標(v0,v1,v3)=±60ボックスで実現型27,722個を完全列挙し、型内confluenceと
  証人恒等式を機械検証（652,592点）。clip窓はy=3機械（±8/±9）の直踏みでは
  合流違反が系統的に出る（y=4の特徴距離: 偶z定常pin R-z=9・掃引帯下端2y+z+2
  のR-z=10・C子掃引上端R-2z=11）ため±12/±13に拡大した（違反witnessは
  x-z=10とx-z=12の同型崩壊対）。ボックス外新規型ゼロをv空間シェル掃引934,470点
  （max|v|∈[61,64]∪[89,92]∪[117,120]）、境界多様体393,713点（z∈{0..5,29..31,
  59..61,299..301,999..1001,2999,3000}・tail窓明示照合）、seeded遠方probe 200,000点
  （z,x<=3000・R<=9000・seed 20261121）、深グリッド掃引で確認。既出版の
  z=16（K1064）・z=17（K1076）・z=18（K1083）・z=19（K1100）のpublished closed form
  を逐語転写して各14,391点全一致（C1d・計57,564点）。生エンジン直接照合C1が
  z=0..14・x=4..26・R<=x+z+45の23,460点、深z生censusアンカーC11が
  z=0..79・x=4..70・R<=x+z+12の479,720点（両エンジン×閉形式・マージ243,746点・
  tail全点）。監査計5,058,763照合点（マージ系1,991,409点）・全チェック不一致0・
  2回実行＋別cwd別ディレクトリでaudit.json byte-identical。加えて
  census_rows.pyがz=0..79・x=4..70・R<=x+z+12の479,720点で生順序保持再帰の行構造
  （Thue-Morse指数・T・P・tail）を抽出しtailアサートR>=x+z+5が全行成立、
  census.txtもbyte-identical再生する。有限監査は転写・実装照合であり、
  全称性は選択肢分解の健全性・正確なmex恒等式・有限型空間の完全性
  （K1023/K1099/K1104と同一trust境界）による。
---

## 命題・範囲

すべての z>=0、x>=4、R>=0 に対して H(R;(x,4);z)=cand4(z,x,R) が成り立つ。
cand4 は z 偶奇別のパラメトリック T/P 集合表（report.md に全文掲載）で、
値2位置はマージ行 O[1, q_odd(x+4)]（x<=z-5）、対角行 x=z-4 の
O[1, z+4]（奇z）/O[1, z+3]（偶z）、過渡行の O[1, z±定数]、掃引行 x=z+5 の
O[z+8, 2z+9]（奇z）/O[z+9, 2z+9]（偶z）、定常pin {z+8}（奇z）/ z+9（偶z）に
整理される。値1位置は基底点 {z+1,z+3,z+5,z+7}（y=4 で y 点仮説の全 z 確定）、
中間帯 O_z[z+10, x+z+4]、奇数x行の無限帯 I[x+z+5, ∞) で、tail R>=x+z+5 は
(x+4) mod 2。y=4 では値1無限帯が奇数x行に反転する（tail 値式 (x+y) mod 2 が
y 偶で反転するため）。z=0..4 でも例外行なし。

## マージ系（対角線下・y=4 の全称昇格）

x<=z-5（S=x+4<z）の全行で H(R;(x,4);z)=single_token(x+4,z,R)（全R）。
行全体が z 非依存になる。K1101 が y∈{1,2} で全称証明し、K1104 が y=3 を
全称昇格させ、y>=4 を有限センサス観察にとどめていたマージ命題の y=4 版が
本項の閉形式から系として全称に昇格した（監査上も 1,991,409 点で独立照合・
不一致 0）。これでマージ命題は y=1..4 まで全称確定（y=1,2 は
K1101・y=3 は K1104 の系）。

## 出版切片との関係

y=4 固定z境界切片 K0880(z=6), K0980(z=7), K0987(z=8), K0990(z=9),
K1006(z=10), K1015(z=11), K1024(z=12), K1027(z=13), K1031(z=14),
K1048(z=15), K1064(z=16), K1076(z=17), K1083(z=18), K1100(z=19) は
本項の z 行の特殊例である。K1064/K1076/K1083/K1100 の published closed form
は検証器に逐語転写して全点一致を確認した（C1d・各 x=4..120・R<=x+60 の
14,391点）。z>=20 の y=4 行は本項が直接分類するため、以後の y=4 スライス出版は
不要。z<=15 の y=4 行は C1 の raw 直接照合と C11 生censusアンカー（z=0..79）に
含まれる。

## 導かれる構造（y=2..4 全称表からの横断観察）

- 値1基底点 y 点仮説 {z+1,..,z+2y-1} が y=4 で全 z>=0 確定（y=1..4 で全称表中
  の連続 4 例。y>=5 は予想）。
- tail 開始式 x+z+y+1 が y=2,3,4 の 3 族連続で全称確定（K1104 の未解決
  「tail 開始の一般式は y=4 の全称表が決め手」が y=2..4 帯で決着）。
  tail 値 (x+y) mod 2 も 3 族連続。
- 掃引行 x=z+y+1 と帯 O[2y+z, 2z+2y+1]（奇z）/O[2y+z+1, 2z+2y+1]（偶z）、
  中間帯 O_z[2y+z+2, x+z+y]、定常pin 2y+z（奇z）/2y+z+1（偶z）は
  y=2,3,4 共通の族式候補。
- pin の構造変化: 奇数zの前倒しpin 2y+z-2 は行 x=z+y-4 に現れ（y=3: x=z-1・
  y=4: x=z）、偶数zの y=4 は前倒しpinが2つ（{z+5} at x=z-2・{z+7} at x=z+2）
  に増える。偶z対角行の連続上端は z+2y-5→z+3 の定数崩れ（y 非依存の初反例）。
- 型機械の clip 窓は特徴距離 2y+z+2 に従って広がる（y=3: ±8/9・y=4: ±12/13）。

これらの横断法則は y=2..4 の全称表からの観察であり、y>=5 での一般証明を
含意しない。

## 現在の根拠と限界

全称性は (i) 選択肢分解の健全性（raw錨）・(ii) 正確な mex 恒等式の有限グリッド
照合と型ごとの機械検査・(iii) 実現型空間の有限性（ボックス完全列挙＋シェル・
多様体・遠方probe・深掃引で新規型ゼロ）に基づく。K1023/K1099/K1104 と同一の
trust 境界にあり、Lean 形式化ではない。H の定義は K0832、B子の評価は K1104
（さらに K1099・K1023）に依存する。y>=5 族、基底点 y 点仮説と d+z 剰余格子
規則の一般証明、clip 窓一般式の補題化、3トークン以上、固定幅・q点版安定化長、
11×11 は範囲外。
