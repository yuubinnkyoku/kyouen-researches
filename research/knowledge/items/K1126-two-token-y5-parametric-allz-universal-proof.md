---
id: K1126
title: 2トークン残余ゲーム y=5族のパラメトリック閉形式の全称証明（全z>=0・全x>=5・全R>=0）
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token y=5 parametric all-z universal proof, P5]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・Theorem T・単一トークン閉形式のraw anchorに使用する
- type: depends_on
  target: K1112
  note: B子（y=4子）の評価にy=4パラメトリック全z全称閉形式cand4を使用する（x=5合流子も同一）。導出の過程でK1112実験レポートのマージ行P表の偶奇ラベル反転を検出しerratumコミットで修正した
- type: generalizes
  target: K0884
  note: z=6・y=5切片は本項の特殊例
- type: generalizes
  target: K0981
  note: z=7・y=5切片は特殊例
- type: generalizes
  target: K0991
  note: z=8・y=5切片は特殊例
- type: generalizes
  target: K0992
  note: z=9・y=5切片は特殊例
- type: generalizes
  target: K1007
  note: z=10・y=5切片は特殊例
- type: generalizes
  target: K1037
  note: z=11・y=5切片は特殊例
- type: generalizes
  target: K1043
  note: z=12・y=5切片は特殊例
- type: generalizes
  target: K1045
  note: z=13・y=5切片は特殊例
- type: generalizes
  target: K1047
  note: z=14・y=5切片は特殊例
- type: generalizes
  target: K1049
  note: z=15・y=5切片は特殊例
- type: generalizes
  target: K1074
  note: z=16・y=5切片は特殊例（published closed form を逐語アンカーとして照合）
- type: generalizes
  target: K1080
  note: z=17・y=5切片は特殊例（逐語アンカーとして照合）
- type: generalizes
  target: K1092
  note: z=18・y=5切片は特殊例（逐語アンカーとして照合）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y5-parametric-allz-proof-20261120/report.md
  role: proof
  note: z偶奇別T/Pパラメトリック集合表による全称定理と、マージ系（対角線下・y=5の全称昇格でマージ命題はy=1..5確定）・選択肢分解・恒等式・型機械（y=4のclip窓±12/番兵±13を再利用した初の族）による証明構成、出版切片アンカー、tail開始式x+z+y+1のy=2..5確定、対角行上端格子規則r=z+y-[2(z-y)≡0 mod 4]の横断確認
- path: research/experiments/vertical-fiber-two-token-y5-parametric-allz-proof-20261120/verify_y5_universal.py
  role: verifier
  note: 12チェック5,456,418照合点（マージ系1,655,267点）・不一致0・実現型27,182・2回実行＋別cwdでaudit.json byte-identical・純Python約45秒
- path: research/experiments/vertical-fiber-two-token-y5-parametric-allz-proof-20261120/census_rows.py
  role: verifier
  note: z=0..79・x=5..70・R<=x+z+12の生二重再帰センサス、475,200点・エンジン状態数2,879,588・tail一致・別cwd byte-identical
- path: research/experiments/vertical-fiber-two-token-y5-parametric-allz-proof-20261120/output/audit.json
  role: data
  note: 検証器の決定論的監査出力（固定seed・ソート済みキー・SHA-256 838e1e5dce9619660d9add4a138f8f05a6e9536cc886ad5826c18cb0cf58a3b0）
- path: research/experiments/vertical-fiber-two-token-y5-parametric-allz-proof-20261120/output/census.txt
  role: data
  note: センサスの決定論的行表出力（SHA-256 617751ba9fa6f8eed62028b2e7e1a3c0477bb3ed1777c07bc7e20e7eaba67559）
- path: research/log/2026-11-20-two-token-y5-parametric-allz-proof.md
  role: log
  note: 最新main・単一オーナー・並走状況の確認、y=5族の選定・導出・出版済み切片との差分化・出版記録、K1112レポートのマージ行P表偶奇ラベルerratumの記録
- path: research/log/2026-11-20-two-token-y5-parametric-allz-single-owner-note.md
  role: log
  note: 単一オーナー宣言＋横断法則6候補のy=5検証関門（先行出版・着手時HEAD ef18cc3566）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,5)、全z>=0・全x>=5・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式）で完全分類する。
  K0884/K0981/K0991/K0992/K1007/K1037/K1043/K1045/K1047/K1049/K1074/K1080/K1092の
  固定z切片（z=6..18）は本項の特殊例であり、z>=19のy=5行も主張に含まれる
  （z=19,y=5の切片出版を含め、以後のy=5スライス出版は不要）。
  系としてx<=z-6（S=x+5<z）の全R行が単一トークン値single_token(x+5,z,R)
  に一致するマージ命題のy=5版が全称に昇格する（マージ命題はy=1..5で全称確定）。
  tail R>=x+z+6=(x+z+y+1)の(x+5) mod 2も全称に含む。
evidence: >-
  証明はK1023/K1099/K1104/K1112と同型の3部構成。(1) 選択肢分解：A子=H(R-1;(x-1,5);z)
  （x>=6）、B子=K1112のy=4全称閉形式cand4、C子=1 xor cand5(z-1,x,R-1)。x=5では
  2つのトークン減少手が同一多重集合(4,5)≡(5,4)子に合流しA≡B=cand4のz行x=5になる。
  分解が素再帰の選択肢値集合と一致することをraw二重再帰で錨止めする
  （C3・1,568点）。単一トークン閉形式・y=4子・x=5合流子もraw錨（C1b・48,411点）。
  (2) 恒等式：cand5(z,x,R)=mex{A,B,C}（子は閉形式評価・Cはz外帰納）がR帰納の本体で、
  z=0..48×x=5..56×R<=x+z+40の240,786点（マージ・tail系込み）、深部tail
  z∈{60,..,400}の10,104点、z=0..120×x=5..120×R<=x+z+16の1,943,986点等で直接照合。
  (3) 型機械：型=(x==5,z==0,z%2,x%2,R%2,6差分族w0..w5の±12窓±13番兵)、
  自由座標(v0,v1,v3)=±60ボックスで実現型27,182個を完全列挙し、型内confluenceと
  証人恒等式を機械検証（648,460点）。clip窓はy=4機械（K1112）の±12/±13をそのまま
  再利用（前の族の窓を再利用した初例。y=5の特徴距離R-z最大12・R-2z=11がクリップ内）。
  ボックス外新規型ゼロをv空間シェル掃引932,202点
  （max|v|∈[61,64]∪[89,92]∪[117,120]）、境界多様体415,266点（z∈{0..5,29..31,
  59..61,299..301,999..1001,2999,3000}・dx∈[-13,6]・tail窓明示照合）、seeded遠方
  probe 200,000点（z,x<=3000・R<=9000・seed 20261122）、深グリッド掃引で確認。
  既出版のz=16（K1074）・z=17（K1080）・z=18（K1092）のpublished closed formを
  逐語転写して各14,210点全一致（C1d・計42,630点）。生エンジン直接照合C1が
  z=0..14・x=5..26・R<=x+z+45の22,605点、深z生censusアンカーC11が
  z=0..79・x=5..70・R<=x+z+12の950,400点（両エンジン×閉形式・マージ・tail系込み）。
  監査計5,456,418照合点（マージ系1,655,267点）・全チェック不一致0・
  2回実行＋別cwd別ディレクトリでaudit.json byte-identical。加えて
  census_rows.pyがz=0..79・x=5..70・R<=x+z+12の475,200点で生順序保持再帰の行構造
  （Thue-Morse指数・T・P・tail）を抽出しtailアサートR>=x+z+6が全行成立、
  census.txtもbyte-identical再生する。有限監査は転写・実装照合であり、
  全称性は選択肢分解の健全性・正確なmex恒等式・有限型空間の完全性
  （K1023/K1099/K1104/K1112と同一trust境界）による。
---

## 命題・範囲

すべての z>=0、x>=5、R>=0 に対して H(R;(x,5);z)=cand5(z,x,R) が成り立つ。
cand5 は z 偶奇別のパラメトリック T/P 集合表（report.md に全文掲載）で、
値2位置はマージ行 O[1, q_odd(x+5)]（x<=z-6）、対角行 x=z-5 の
O[1, z+4]（奇z）/O[1, z+5]（偶z）、過渡行の O[1, z±定数]、掃引行 x=z+6 の
O[z+10, 2z+11]（奇z）/O[z+11, 2z+11]（偶z）、定常pin {z+10}（奇z）/ z+11
（偶z）に整理される。値1位置は基底点 {z+1,z+3,z+5,z+7,z+9}（y=5 で y 点仮説の
全 z 確定）、中間帯 O_z[z+12, x+z+5]、偶数x行の無限帯 I[x+z+6, ∞) で、
tail R>=x+z+6 は (x+5) mod 2。y=5 では値1無限帯が偶数x行に戻る（tail 値式
(x+y) mod 2 が y 偶で反転するため）。z=0..5 でも例外行なし。

## マージ系（対角線下・y=5 の全称昇格）

x<=z-6（S=x+5<z）の全行で H(R;(x,5);z)=single_token(x+5,z,R)（全R）。
行全体が z 非依存になる。K1101 が y∈{1,2} で全称証明し、K1104 が y=3 を・
K1112 が y=4 を全称昇格させたマージ命題の y=5 版が本項の閉形式から系として
全称に昇格した（監査上も 1,655,267 点で独立照合・不一致 0）。これでマージ命題は
y=1..5 で全称確定。マージ行の値1無限帯は S=x+5 奇すなわち x 偶の行に出る
（y=4 の x 奇と逆で、S の偶奇に統一される）。

## 出版切片との関係

y=5 固定z境界切片 K0884(z=6), K0981(z=7), K0991(z=8), K0992(z=9),
K1007(z=10), K1037(z=11), K1043(z=12), K1045(z=13), K1047(z=14), K1049(z=15),
K1074(z=16), K1080(z=17), K1092(z=18) は本項の z 行の特殊例である。
K1074/K1080/K1092 の published closed form は検証器に逐語転写して全点一致を
確認した（C1d・各 x=5..120・R<=x+60 の 14,210点）。z>=19 の y=5 行は本項が
直接分類するため、z=19,y=5 切片を含む以後の y=5 スライス出版は不要。
z<=15 の y=5 行は C1 の raw 直接照合と C11 生censusアンカー（z=0..79）に
含まれる。

## 導かれる構造（y=2..5 全称表からの横断観察）

- 値1基底点 y 点仮説 {z+1,..,z+2y-1} が y=5 で全 z>=0 確定（y=1..5 で全称表中
  の連続 5 例。y>=6 は予想）。
- tail 開始式 x+z+y+1 が y=2..5 の 4 族連続で全称確定。tail 値 (x+y) mod 2 も
  4 族連続。マージ行の値1無限帯は S=x+y 奇の行（x+y の偶奇に統一）。
- 掃引行 x=z+y+1 と帯 O[2y+z, 2z+2y+1]（奇z）/O[2y+z+1, 2z+2y+1]（偶z）、
  中間帯 O_z[2y+z+2, x+z+y]、定常pin 2y+z（奇z）/2y+z+1（偶z）は
  y=2..5 共通の族式。
- pin の構造変化: 奇数zの前倒しpin 2y+z-2 は行 x=z+y-4 に現れ（y=3,4,5 の
  3 族連続）、y=5 では内側 {2y+z-4} at x=z+y-8・外側 {2y+z} at x=z+y が加わり
  3 つに増える。偶数zは R=2y+z-3 at x=z+y-6・R=2y+z-1 at x=z+y-2 が
  y=4,5 の 2 族連続。
- 対角行 x=z-y の連続上端が格子規則 r = z+y - [2(z-y)≡0 (mod 4)] で統一される
  （y=2..5 の全称表で全 z 一致。y=5: 奇z 上端 z+4・偶z 上端 z+5。y>=6 は未証明）。
- 型機械の clip 窓は y=5 で y=4 の ±12/±13 の再利用が確定（前の族の窓を
  再利用した初例。特徴距離の最大がクリップ窓内に収まることの補題化は未解決）。

これらの横断法則は y=2..5 の全称表からの観察であり、y>=6 での一般証明を
含意しない。

## 現在の根拠と限界

全称性は (i) 選択肢分解の健全性（raw錨）・(ii) 正確な mex 恒等式の有限グリッド
照合と型ごとの機械検査・(iii) 実現型空間の有限性（ボックス完全列挙＋シェル・
多様体・遠方probe・深掃引で新規型ゼロ）に基づく。K1023/K1099/K1104/K1112 と同一の
trust 境界にあり、Lean 形式化ではない。H の定義は K0832、B子の評価は K1112
（さらに K1104・K1099・K1023）に依存する。y>=6 族、基底点 y 点仮説と対角行格子
規則の一般証明、clip 窓一般式の補題化、3トークン以上、固定幅・q点版安定化長、
11×11 は範囲外。
