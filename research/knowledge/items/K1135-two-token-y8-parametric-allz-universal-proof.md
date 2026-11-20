---
id: K1135
title: 2トークン残余ゲーム y=8族のパラメトリック閉形式の全称証明（全z>=0・全x>=8・全R>=0）
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token y=8 parametric all-z universal proof, P8]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・Theorem T・単一トークン閉形式のraw anchorに使用する
- type: depends_on
  target: K1131
  note: B子（y=7子）の評価にy=7パラメトリック全z全称閉形式cand7を使用する（x=8合流子も同一）。cand7は出版検証器verify_y7_universal.py（SHA-256 9200b591...）からの逐語転写で対称的に確認
- type: generalizes
  target: K0888
  note: z=6・y=8境界切片は本項の特殊例
- type: generalizes
  target: K0996
  note: z=8・y=8境界切片は特殊例
- type: generalizes
  target: K0998
  note: z=9・y=8境界切片は特殊例
- type: generalizes
  target: K1010
  note: z=10・y=8境界切片は特殊例
- type: generalizes
  target: K1065
  note: z=15・y>=6族のy=8行は本項の特殊例（published closed formを転写アンカーとして照合）
- type: generalizes
  target: K1077
  note: z=16・y>=6族のy=8行は特殊例（転写アンカーとして照合）
- type: generalizes
  target: K1087
  note: z=17・y>=6族のy=8行は特殊例（転写アンカーとして照合）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y8-parametric-allz-proof-20261120/report.md
  role: proof
  note: z偶奇別T/Pパラメトリック集合表による全称定理と、マージ系（対角線下・y=8の全称昇格でマージ命題はy=1..8確定）・選択肢分解・恒等式・型機械（K1127/K1131予想どおり2y+2=18の±18/±19がtight、4族連続tight（y=5:12,y=6:14,y=7:16,y=8:18）・3予想連続的中）による証明構成、出版切片転写アンカー（z=15/16/17のy=8特殊化・縮退セル・mergeセル・低R縮約R<=z+6のy=8行照合）、tail開始式x+z+y+1のy=2..8確定、基底点8点・pin格子公式pin=2y+((x-y)+z)/2のy=5..8統一・対角行格子規則y=2..8全z一致の横断観察
- path: research/experiments/vertical-fiber-two-token-y8-parametric-allz-proof-20261120/verify_y8_universal.py
  role: verifier
  note: 12チェック5,625,155照合点（マージ系1,558,050点・tail系330,477点）・不一致0・実現型73,685・3回実行（同一cwd 2回＋別cwd別ディレクトリ別HOME 1回）でaudit.json byte-identical・純Python約58秒・seed 20261123
- path: research/experiments/vertical-fiber-two-token-y8-parametric-allz-proof-20261120/census_rows.py
  role: verifier
  note: z=0..79・x=8..70・R<=x+z+12の生二重再帰センサス、461,160点・エンジン状態数4,239,932・tail一致・census.txtはcand8表と461,160点全一致（独立照合）
- path: research/experiments/vertical-fiber-two-token-y8-parametric-allz-proof-20261120/output/audit.json
  role: data
  note: 検証器の決定論的監査出力（固定seed・ソート済みキー・SHA-256 06694603262c4d5d6b6533b2882ba19c4b3fbf9c9c6f4f86faf72968c7a5b8ea）
- path: research/experiments/vertical-fiber-two-token-y8-parametric-allz-proof-20261120/output/census.txt
  role: data
  note: センサスの決定論的行表出力（SHA-256 a91cd4386783d3f5aab2b094481364a4f07c8866d66d1684d01b7a5e12ef273d）
- path: research/log/2026-11-20-two-token-y8-parametric-allz-proof.md
  role: log
  note: 単一オーナー宣言の確認、y=8族の選定・導出（probe 167,280点の初回適合mismatch 0・誤り行なし）・出版記録、次に開くもの
- path: research/log/2026-11-20-two-token-y8-parametric-allz-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-20T07:44:44Z・K1131完成後に先行出版）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,8)、全z>=0・全x>=8・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand8）で完全分類する。
  K0888(z=6)/K0996(z=8)/K0998(z=9)/K1010(z=10)のy=8行と
  K1065/K1077/K1087（z=15,16,17のy>=6族）のy=8行は本項の特殊例であり、
  z>=18（z=18,y=8を含む）のy=8行も主張に含まれる（以後のy=8スライス出版は不要）。
  系としてx<=z-9（S=x+8<z-1）の全R行が単一トークン値single_token(x+8,z,R)
  に一致するマージ命題のy=8版が全称に昇格する（マージ命題はy=1..8で全称確定）。
  tail R>=x+z+9=(x+z+y+1)の(x+8) mod 2も全称に含む。
evidence: >-
  証明はK1023/K1099/K1104/K1112/K1126/K1127/K1131と同型の3部構成。
  (1) 選択肢分解：A子=H(R-1;(x-1,8);z)（x>=9）、B子=K1131のy=7全称閉形式
  cand7、C子=1 xor cand8(z-1,x,R-1)。x=8では2つのトークン減少手が同一多重集合
  (7,8)≡(8,7)子に合流しA≡B=cand7(z,8,R-1)のz行x=8になる。分解が素再帰の
  選択肢値集合と一致することをraw二重再帰で錨止めする（C3・1,224点）。
  単一トークン閉形式・y=7子・x=8合流子もraw錨（C1b・44,886点）。
  cand7は出版検証器（K1131・SHA-256 9200b591...）からの逐語転写。
  (2) 恒等式：cand8(z,x,R)=mex{A,B,C}（子は閉形式評価・Cはz外帰納）が
  R帰納の本体で、z=0..48×x=8..56×R<=x+z+40の230,496点（マージ・tail系込み）、
  深部tail z∈{60,72,84,96,108,120,240,400}の9,282点、z=0..120×x=8..120×
  R<=x+z+16の1,914,220点で直接照合。(3) 型機械：型=(x==8,z==0,z%2,x%2,
  R%2,6差分族w0..w5の±18窓±19番兵)、自由座標(v0,v1,v3)=±60ボックスで
  実現型73,529個を完全列挙し、型内confluenceと証人恒等式を機械検証
  （635,394点）。clip窓はK1127/K1131出版時の予想どおり2y+2=18の±18/±19が
  tight（±17/±18では中間帯下端R-z=2y+2=18が番兵18と衝突。族式候補2y+2は
  y=5:12,y=6:14,y=7:16,y=8:18で4族連続tight・3予想連続的中）。
  ボックス外新規型ゼロをv空間シェル掃引925,254点
  （max|v|∈[61,64]∪[89,92]∪[117,120]）、境界多様体643,475点
  （z∈{0..5,29..31,59..61,299..301,999..1001,2999,3000}・dx∈[-19,11]・
  tail窓[x+z+9,x+z+11]明示照合）、seeded遠方probe 200,000点（z,x<=3000・
  R<=9000・seed 20261123・tail境界を跨ぐ窓）、深グリッド掃引（全走型73,685）
  で確認。既出版のz=15（K1065）・z=16（K1077）・z=17（K1087）のy>=6一様全
  Grundy分類をY=2y=16・S=x+8引数変換・tail最優先で転写しy=8特殊化と全一致
  （C1d・x=8..159・R<=x+61）・これら切片の低R単一トークン縮約R<=z+6も
  y=8行で照合（z=15,16,17でR<=21,22,23）。生エンジン直接照合C1がz=0..14・
  x=8..28・R<=x+z+46の22,680点、深z生censusアンカーC11がz=0..79・x=8..70・
  R<=x+z+12の922,320点（両エンジン×閉形式・マージ・tail系込み）。
  監査計5,625,155照合点（マージ系1,558,050点・tail系330,477点・それぞれ
  不等0）・全チェック不一致0・同一cwd 2回＋別cwd別ディレクトリ別HOME 1回の
  計3回実行でaudit.json byte-identical。加えてcensus_rows.pyがz=0..79・
  x=8..70・R<=x+z+12の461,160点で生順序保持再帰の行構造（Thue-Morse指数・
  T・P・tail）を抽出しtailアサートR>=x+z+9が全行成立、census.txtのT/P
  全リストがcand8表と461,160点完全一致を独立照合で確認。有限監査は転写・
  実装照合であり、全称性は選択肢分解の健全性・正確なmex恒等式・有限型空間
  の完全性（K1023/K1099/K1104/K1112/K1126/K1127/K1131と同一trust境界）に
  よる。
---

## 命題・範囲

すべての z>=0、x>=8、R>=0 に対して H(R;(x,8);z)=cand8(z,x,R) が成り立つ。
cand8 は z 偶奇別のパラメトリック T/P 集合表（report.md に全文掲載）で、
値2位置はマージ行 O[1, q_odd(x+8)]（x<=z-9）、対角行 x=z-8 の
O[1, z+8]（奇z）/O[1, z+7]（偶z）（格子規則 r=z+y-[2(z-y)≡0 mod 4] の
y=8 値）、前倒しpin格子行（奇z d∈{-4,0,4,8}→pin z+10,z+12,z+14,z+16、
偶z d∈{-6,-2,2,6}→pin z+9,z+11,z+13,z+15・pin=2y+((x-y)+z)/2〔(x-y)+z≡2
mod 4〕）、掃引行 x=z+9 の O[z+16, x+z+8]（奇z）/O[z+17, x+z+8]（偶z）、
定常pin {z+16}（奇z）/{z+17}（偶z）（2y+z／2y+z+1）に整理される。
値1位置は基底点 {z+1,...,z+15}（y=8 で y 点仮説の全z確定・y=1..8 連続 8 例）、
中間帯 O_z[z+18, x+z+8]、無限帯・tail は奇数 x 行（y 偶の y=2,4,6 型）である。
tail R>=x+z+9 の (x+8) mod 2 も全称に含む。z=0..5 でも例外行なし。
y=8 は x=z+8 の pin 行（奇z）が値1点 z+17 を追加する（2y+z+1）。

## マージ系（対角線下・y=8 の全称昇格）

x<=z-9（S=x+8<z-1）の全行で H(R;(x,8);z)=single_token(x+8,z,R)（全R）。
行全体が z 非依存になる。K1101 が y∈{1,2} で全称証明し、y=3..7 を
K1104/K1112/K1126/K1127/K1131 が全称昇格させたマージ命題の y=8 版が本項の
閉形式から系として全称に昇格した（監査上も 1,558,050 点で独立照合・
不一致 0）。これでマージ命題は y=1..8 で全称確定。y=8 では S=x+8 の偶奇が
x と一致するため、値1無限帯は x 奇の行（偶数 y 型）。

## 出版切片との関係

y=8 行を含む固定z切片 K0888(z=6)・K0996(z=8)・K0998(z=9)・K1010(z=10) と
z=15,16,17 の y>=6 一様族 K1065/K1077/K1087 の y=8 行は本項の特殊例である。
K1065/K1077/K1087 の published closed form は検証器に転写して y=8 特殊化
（Y=2y=16・S=x+8 引数変換・tail 最優先・z=16 の (8,0) 縮退セルと z=17 の
S=16 merge セルを出版どおり特殊化）と全点一致を確認した（C1d・
x=8..159・R<=x+61のアンカー照合）・低R単一トークン縮約 R<=z+6 の y=8 行も
直接照合（z=15,16,17 で R<=21,22,23・不一致 0）。z>=18 の y=8 行は本項が
直接分類するため、z=18,y=8 切片を含む以後の y=8 スライス出版は不要。
z<=14 の y=8 行は C1 の raw 直接照合と C11 生censusアンカー（z=0..79）に含まれる。

## 導かれる構造（y=2..8 全称表からの横断観察）

- 値1基底点 y 点仮説 {z+1,..,z+2y-1} が y=8 で全 z>=0 確定（y=1..8 で
  連続 8 例。y>=9 は予想）。
- tail 開始式 x+z+y+1 が y=2..8 の 7 族連続で全称確定。tail 値 (x+y) mod 2
  も 7 族連続（y 奇で値1無限帯が偶数x行・y 偶で奇数x行）。
- マージ行の境界 x<=z-y-1 が y=1..8 の 8 族で確定（y=8: x<=z-9）。
  マージ命題（K1101）は y=1..8 で全称確定。
- 掃引行 x=z+y+1・帯 O[2y+z, x+z+y]（y=8: O[z+16, x+z+8]）・中間帯
  O_z[2y+z+2, x+z+y]・定常pin 2y+z（奇z）/2y+z+1（偶z）は y=2..8 共通の族式。
- 前倒しpin格子公式 pin=2y+((x-y)+z)/2〔pin行の(x-y)+z≡2 mod 4・pin行のdは
  d≡y(mod 4)（奇z）・d≡y+2(mod 4)（偶z）〕が y=5..8 の 4 族で統一
  （y=8 は奇z d≡0・偶z d≡2）。
- 対角行上端格子規則 r=z+y-[2(z-y)≡0 mod 4] が y=8 の全 z で成立
  （y=2..8 の 7 族の全称表で全 z 一致。y>=9 は予想）。
- 型機械の clip 窓は K1127/K1131 の予想どおり ±18/±19（2y+2）が tight に
  確定（±17/±18 では中間帯下端 R-z=2y+2=18 が番兵と衝突。族式候補 2y+2 は
  y=5:12・y=6:14・y=7:16・y=8:18 と 4 族連続 tight・3 予想連続的中）。
- pin 行の追加値1点 2y+1+z：y=8 奇z の d=8 行の z+17 は y=6 の d=7 行
  （K1127）に対応する y 偶型の位置。

これらの横断法則は y=2..8 の全称表からの観察であり、y>=9 での一般証明を
含意しない。

## 現在の根拠と限界

全称性は (i) 選択肢分解の健全性（raw錨）・(ii) 正確な mex 恒等式の有限グリッド
照合と型ごとの機械検査・(iii) 実現型空間の有限性（ボックス完全列挙＋シェル・
多様体・遠方probe・深掃引で新規型ゼロ）に基づく。K1023/K1099/K1104/K1112/
K1126/K1127/K1131 と同一の trust 境界にあり、Lean 形式化ではない。H の定義は
K0832、B子の評価は K1131（さらに K1127・K1126・K1112・K1104・K1099・K1023）に
依存する。y>=9 族、基底点 y 点仮説と前倒しpin格子公式・対角行格子規則の
一般証明、clip 窓一般式の補題化、3トークン以上、固定幅・q点版安定化長、
11×11 は範囲外。REFUTED-D10 型の実験とは異なり LOSS 証明を含まず、
標準 11×11 盤面の各種パラメータの値は本項では UNKNOWN のまま。
