---
id: K1127
title: 2トークン残余ゲーム y=6族のパラメトリック閉形式の全称証明（全z>=0・全x>=6・全R>=0）
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token y=6 parametric all-z universal proof, P6]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・Theorem T・単一トークン閉形式のraw anchorに使用する
- type: depends_on
  target: K1126
  note: B子（y=5子）の評価にy=5パラメトリック全z全称閉形式cand5を使用する（x=6合流子も同一）。cand5は出版検証器verify_y5_universal.py（SHA-256 3392a8f1...）からの逐語転写でbyte照合済み
- type: generalizes
  target: K0993
  note: z=8・y=6境界切片は本項の特殊例
- type: generalizes
  target: K0994
  note: z=9・y=6境界切片は特殊例
- type: generalizes
  target: K1008
  note: z=10・y=6境界切片は特殊例
- type: generalizes
  target: K1055
  note: z=11・y>=6一様全Grundy分類のy=6行は本項の特殊例（y>=7行は範囲外）
- type: generalizes
  target: K1056
  note: z=12・y>=6族のy=6行は特殊例（y>=7行は範囲外）
- type: generalizes
  target: K1061
  note: z=13・y>=6族のy=6行は特殊例（y>=7行は範囲外）
- type: generalizes
  target: K1062
  note: z=14・y>=6族のy=6行は特殊例（y>=7行は範囲外）
- type: generalizes
  target: K1065
  note: z=15・y>=6族のy=6行は特殊例（published closed formを転写アンカーとして照合）
- type: generalizes
  target: K1077
  note: z=16・y>=6族のy=6行は特殊例（転写アンカーとして照合）
- type: generalizes
  target: K1087
  note: z=17・y>=6族のy=6行は特殊例（転写アンカーとして照合）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y6-parametric-allz-proof-20261120/report.md
  role: proof
  note: z偶奇別T/Pパラメトリック集合表による全称定理と、マージ系（対角線下・y=6の全称昇格でマージ命題はy=1..6確定）・選択肢分解・恒等式・型機械（y=5の±12/±13から広げ直した±14/±15・特徴距離R-z=2y+2=14が番兵衝突の原因）による証明構成、出版切片アンカー、tail開始式x+z+y+1のy=2..6確定、基底点6点・前倒しpin格子公式pin=2y+((x-y)+z)/2〔(x-y)+z≡2 mod 4〕のy=5,6統一の横断観察
- path: research/experiments/vertical-fiber-two-token-y6-parametric-allz-proof-20261120/verify_y6_universal.py
  role: verifier
  note: 12チェック5,531,469照合点（マージ系1,621,917点・tail系360,923点）・不一致0・実現型39,383・4回実行（同一cwd 2回＋別cwd＋再構築後新規環境）でaudit.json byte-identical・純Python約45秒
- path: research/experiments/vertical-fiber-two-token-y6-parametric-allz-proof-20261120/census_rows.py
  role: verifier
  note: z=0..79・x=6..70・R<=x+z+12の生二重再帰センサス、470,600点・エンジン状態数3,338,636・tail一致・別cwd byte-identical
- path: research/experiments/vertical-fiber-two-token-y6-parametric-allz-proof-20261120/output/audit.json
  role: data
  note: 検証器の決定論的監査出力（固定seed・ソート済みキー・SHA-256 ed05163929c0199dcabe46219a77189f7f4890cefc85e83755df58fe11bdd0d7）
- path: research/experiments/vertical-fiber-two-token-y6-parametric-allz-proof-20261120/output/census.txt
  role: data
  note: センサスの決定論的行表出力（SHA-256 f69be2b45a4b19c7959fbb9798ef8de3dd1f9157feab8659e7879c813066bbe1）
- path: research/log/2026-11-20-two-token-y6-parametric-allz-proof.md
  role: log
  note: 単一オーナー宣言の確認、y=6族の選定・導出・検証器の消失と出版済み素材からの全再構築（cand6のwide fit再現・census byte-identical再現）・出版記録、次に開くもの
- path: research/log/2026-11-20-two-token-y6-parametric-allz-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-20T06:02:16.073Z・K1126完成直後に先行出版）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,6)、全z>=0・全x>=6・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand6）で完全分類する。
  K0993/K0994/K1008（z=8,9,10のy=6境界切片）とK1055/K1056/K1061/K1062/K1065/
  K1077/K1087（z=11..17のy>=6族）のy=6行は本項の特殊例であり、
  z>=18のy=6行も主張に含まれる（z=18,y=6の切片出版を含め、以後のy=6スライス
  出版は不要）。系としてx<=z-7（S=x+6<z）の全R行が単一トークン値
  single_token(x+6,z,R)に一致するマージ命題のy=6版が全称に昇格する
  （マージ命題はy=1..6で全称確定）。tail R>=x+z+7=(x+z+y+1)の(x+6) mod 2も
  全称に含む。
evidence: >-
  証明はK1023/K1099/K1104/K1112/K1126と同型の3部構成。(1) 選択肢分解：
  A子=H(R-1;(x-1,6);z)（x>=7）、B子=K1126のy=5全称閉形式cand5、
  C子=1 xor cand6(z-1,x,R-1)。x=6では2つのトークン減少手が同一多重集合
  (5,6)≡(6,5)子に合流しA≡B=cand5のz行x=6になる。分解が素再帰の選択肢値
  集合と一致することをraw二重再帰で錨止めする（C3・1,365点）。
  単一トークン閉形式・y=5子・x=6合流子もraw錨（C1b・47,261点）。cand5は
  出版検証器（K1126・SHA-256 3392a8f1...）からの逐語転写でbyte照合済み。
  (2) 恒等式：cand6(z,x,R)=mex{A,B,C}（子は閉形式評価・Cはz外帰納）が
  R帰納の本体で、z=0..48×x=6..56×R<=x+z+40の237,405点（マージ・tail系込み）、
  深部tail z∈{60,72,84,96,108,120,240,400}の9,194点、z=0..120×x=6..120×
  R<=x+z+16の1,934,185点で直接照合。(3) 型機械：型=(x==6,z==0,z%2,x%2,
  R%2,6差分族w0..w5の±14窓±15番兵)、自由座標(v0,v1,v3)=±60ボックスで
  実現型39,383個を完全列挙し、型内confluenceと証人恒等式を機械検証
  （644,215点）。clip窓はy=5機械（±12/±13）を広げ直した±14/±15
  （±13/±14では中間帯下端R-z=2y+2=14が番兵14と衝突しconfluence違反。
  窓の広げ直しが必要になった初の族。必要clip半径の族式候補2y+2）。
  ボックス外新規型ゼロをv空間シェル掃引929,910点
  （max|v|∈[61,64]∪[89,92]∪[117,120]）、境界多様体498,387点
  （z∈{0..5,29..31,59..61,299..301,999..1001,2999,3000}・dx∈[-15,8]・
  tail窓明示照合）、seeded遠方probe 200,000点（z,x<=3000・R<=9000・
  seed 20261122）、深グリッド掃引で確認。既出版のz=15（K1065）・z=16（K1077）・
  z=17（K1087）のy>=6一様全Grundy分類をY=2y=12・S=x+6引数変換・tail最優先
  で転写しy=6特殊化と各22,099点全一致（C1d・計66,297点）。生エンジン直接
  照合C1がz=0..14・x=6..26・R<=x+z+46の22,050点、深z生censusアンカーC11が
  z=0..79・x=6..70・R<=x+z+12の941,200点（両エンジン×閉形式・マージ・tail系込み）。
  監査計5,531,469照合点（マージ系1,621,917点・tail系360,923点）・
  全チェック不一致0・同一cwd 2回＋別cwd＋全成果再構築後の新規環境1回の計4回
  実行でaudit.json byte-identical。加えてcensus_rows.pyがz=0..79・x=6..70・
  R<=x+z+12の470,600点で生順序保持再帰の行構造（Thue-Morse指数・T・P・
  tail）を抽出しtailアサートR>=x+z+7が全行成立、census.txtもbyte-identical
  再生する。有限監査は転写・実装照合であり、全称性は選択肢分解の健全性・
  正確なmex恒等式・有限型空間の完全性（K1023/K1099/K1104/K1112/K1126と同一
  trust境界）による。
---

## 命題・範囲

すべての z>=0、x>=6、R>=0 に対して H(R;(x,6);z)=cand6(z,x,R) が成り立つ。
cand6 は z 偶奇別のパラメトリック T/P 集合表（report.md に全文掲載）で、
値2位置はマージ行 O[1, q_odd(x+6)]（x<=z-7）、対角行 x=z-6 の
O[1, z+6]（奇z）/O[1, z+5]（偶z）、前倒しpin格子行（奇z d∈{-2,2,6}→pin
z+9+d/2、偶z d∈{-4,0,4}→pin z+9+d/2）、掃引行 x=z+7 の
O[z+12, x+z+6]（奇z）/O[z+13, x+z+6]（偶z）、定常pin {z+12}（奇z）/
{z+13}（偶z）に整理される。値1位置は基底点 {z+1,...,z+11}（y=6で y 点
仮説の全z確定・y=1..6連続6例）、中間帯 O_z[z+14, x+z+6]、奇数x行の無限帯
（y=6は偶数yなので値1無限帯・tailともに奇数x行に出る）である。
tail R>=x+z+7 の (x+6) mod 2 も全称に含む。z=0..5 でも例外行なし。

## マージ系（対角線下・y=6 の全称昇格）

x<=z-7（S=x+6<z）の全行で H(R;(x,6);z)=single_token(x+6,z,R)（全R）。
行全体が z 非依存になる。K1101 が y∈{1,2} で全称証明し、K1104 が y=3 を・
K1112 が y=4 を・K1126 が y=5 を全称昇格させたマージ命題の y=6 版が本項の
閉形式から系として全称に昇格した（監査上も 1,621,917 点で独立照合・
不一致 0）。これでマージ命題は y=1..6 で全称確定。y=6 では S=x+6 の偶奇が
x と同じため、値1無限帯は x 奇の行（偶数 y の y=2,4 型）。

## 出版切片との関係

y=6 固定z切片 K0993(z=8), K0994(z=9), K1008(z=10)（y=6境界切片）と
K1055(z=11), K1056(z=12), K1061(z=13), K1062(z=14), K1065(z=15),
K1077(z=16), K1087(z=17)（y>=6一様族）の y=6 行は本項の z 行の特殊例である。
K1065/K1077/K1087 の published closed form は検証器に転写して y=6 特殊化と
全点一致を確認した（C1d・各 x=6..159・R<=x+61 の 22,099点）。z>=18 の
y=6 行は本項が直接分類するため、z=18,y=6 切片を含む以後の y=6 スライス
出版は不要。z<=14 の y=6 行は C1 の raw 直接照合と C11 生censusアンカー
（z=0..79）に含まれる。

## 導かれる構造（y=2..6 全称表からの横断観察）

- 値1基底点 y 点仮説 {z+1,..,z+2y-1} が y=6 で全 z>=0 確定（y=1..6 で
  全称表中の連続 6 例。y>=7 は予想）。
- tail 開始式 x+z+y+1 が y=2..6 の 5 族連続で全称確定。tail 値 (x+y) mod 2
  も 5 族連続。マージ行の値1無限帯は x+y 奇の行。
- 掃引行 x=z+y+1 と帯 O[2y+z, 2z+2y+1]（奇z）/O[2y+z+1, 2z+2y+1]（偶z）・
  中間帯 O_z[2y+z+2, x+z+y]・定常pin 2y+z（奇z）/2y+z+1（偶z）は
  y=2..6 共通の族式。
- **前倒しpin格子公式（本項で新たに統一）**: pin行 x は (x-y)+z≡2 (mod 4)
  を満たし、pin値は pin=2y+((x-y)+z)/2 で与えられる。偶奇z別のばらばらの
  記録を過去の族（y=6 は奇z 3pin・偶z 3pin、y=5 は奇z 3pin・偶z 2pin）から
  統一する。pin行の d は d≡y (mod 4)（奇z）・d≡y+2 (mod 4)（偶z）に乗る。
  y<=6 の観察・一般証明は今後の課題。
- 対角行上端格子規則 r=z+y-[2(z-y)≡0 mod 4] が y=6 の全 z で成立
  （y=2..6 の 5 族の全称表で全 z 一致。y>=7 は予想）。
- 型機械の clip 窓は y=6 で広げ直した ±14/±15 が確定（特徴距離 R-z=2y+2=
  14 が ±13/±14 では番兵と衝突。必要 clip 半径の族式候補 2y+2・
  y=2:6, y=3:8, y=5:12, y=6:14 が tight、y=4 の ±12 は余裕付き）。

これらの横断法則は y=2..6 の全称表からの観察であり、y>=7 での一般証明を
含意しない。

## 現在の根拠と限界

全称性は (i) 選択肢分解の健全性（raw錨）・(ii) 正確な mex 恒等式の有限グリッド
照合と型ごとの機械検査・(iii) 実現型空間の有限性（ボックス完全列挙＋シェル・
多様体・遠方probe・深掃引で新規型ゼロ）に基づく。K1023/K1099/K1104/K1112/
K1126 と同一の trust 境界にあり、Lean 形式化ではない。H の定義は K0832、
B子の評価は K1126（さらに K1112・K1104・K1099・K1023）に依存する。y>=7 族、
基底点 y 点仮説と前倒しpin格子公式・対角行格子規則の一般証明、clip 窓一般式
の補題化、3トークン以上、固定幅・q点版安定化長、11×11 は範囲外。
