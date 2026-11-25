---
id: K1131
title: 2トークン残余ゲーム y=7族のパラメトリック閉形式の全称証明（全z>=0・全x>=7・全R>=0）
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token y=7 parametric all-z universal proof, P7]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・Theorem T・単一トークン閉形式のraw anchorに使用する
- type: depends_on
  target: K1127
  note: B子（y=6子）の評価にy=6パラメトリック全z全称閉形式cand6を使用する（x=7合流子も同一）。cand6は出版検証器verify_y6_universal.py（SHA-256 2d75a817...）からの逐語転写でbyte照合済み
- type: generalizes
  target: K0887
  note: z=6・y=7境界切片は本項の特殊例
- type: generalizes
  target: K0976
  note: z=7・y>=4一様全Grundy分類のy=7行は本項の特殊例
- type: generalizes
  target: K0995
  note: z=8・y=7境界切片は特殊例
- type: generalizes
  target: K0997
  note: z=9・y=7境界切片は特殊例
- type: generalizes
  target: K1009
  note: z=10・y=7境界切片は特殊例
- type: generalizes
  target: K1055
  note: z=11・y>=6一様全Grundy分類のy=7行は本項の特殊例
- type: generalizes
  target: K1056
  note: z=12・y>=6族のy=7行は特殊例
- type: generalizes
  target: K1061
  note: z=13・y>=6族のy=7行は特殊例
- type: generalizes
  target: K1062
  note: z=14・y>=6族のy=7行は特殊例
- type: generalizes
  target: K1065
  note: z=15・y>=6族のy=7行は特殊例（published closed formを転写アンカーとして照合）
- type: generalizes
  target: K1077
  note: z=16・y>=6族のy=7行は特殊例（転写アンカーとして照合）
- type: generalizes
  target: K1087
  note: z=17・y>=6族のy=7行は特殊例（転写アンカーとして照合）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y7-parametric-allz-proof-20261120/report.md
  role: proof
  note: z偶奇別T/Pパラメトリック集合表による全称定理と、マージ系（対角線下・y=7の全称昇格でマージ命題はy=1..7確定）・選択肢分解・恒等式・型機械（K1127予想どおり2y+2=16の±16/±17がtight、3族連続tightで2予想連続的中）による証明構成、出版切片転写アンカー（z=15/16/17のy=7特殊化・低R縮約R<=z+6のy=7行照合）、tail開始式x+z+y+1のy=2..7確定、基底点7点・前倒しpin格子公式pin=2y+((x-y)+z)/2のy=5..7統一の横断観察
- path: research/experiments/vertical-fiber-two-token-y7-parametric-allz-proof-20261120/verify_y7_universal.py
  role: verifier
  note: 12チェック5,594,132照合点（マージ系1,589,081点・tail系359,738点）・不一致0・実現型54,762・3回実行（同一cwd 2回＋別cwd別プロセス1回）でaudit.json byte-identical・純Python約49秒・seed 20261123
- path: research/experiments/vertical-fiber-two-token-y7-parametric-allz-proof-20261120/census_rows.py
  role: verifier
  note: z=0..79・x=7..70・R<=x+z+12の生二重再帰センサス、465,920点・エンジン状態数3,792,084・tail一致・別cwd byte-identical
- path: research/experiments/vertical-fiber-two-token-y7-parametric-allz-proof-20261120/output/audit.json
  role: data
  note: 検証器の決定論的監査出力（固定seed・ソート済みキー・SHA-256 a9893a15cd1a25587e875c8a923b19506acc6265a83f69cb336d38213a123f93）
- path: research/experiments/vertical-fiber-two-token-y7-parametric-allz-proof-20261120/output/census.txt
  role: data
  note: センサスの決定論的行表出力（SHA-256 b161142e3f36ff56b61fc2428a16b966cf6af3cb4be74017a201a8f1242677cd）
- path: research/log/2026-11-20-two-token-y7-parametric-allz-proof.md
  role: log
  note: 単一オーナー宣言の確認、y=7族の選定・導出（fit・唯一の修正行の記録）・出版記録、次に開くもの
- path: research/log/2026-11-20-two-token-y7-parametric-allz-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-20T07:02Z・K1127完成直後に先行出版）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,7)、全z>=0・全x>=7・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand7）で完全分類する。
  K0887(z=6)/K0976(z=7)/K0995/K0997/K1009(z=8,9,10)のy=7行と
  K1055/K1056/K1061/K1062/K1065/K1077/K1087（z=11..17のy>=6族）のy=7行は
  本項の特殊例であり、z>=18（z=18,y=7を含む）のy=7行も主張に含まれる
  （以後のy=7スライス出版は不要）。系としてx<=z-8（S=x+7<z）の全R行が
  単一トークン値single_token(x+7,z,R)に一致するマージ命題のy=7版が全称に
  昇格する（マージ命題はy=1..7で全称確定）。tail R>=x+z+8=(x+z+y+1)の
  (x+7) mod 2も全称に含む。
evidence: >-
  証明はK1023/K1099/K1104/K1112/K1126/K1127と同型の3部構成。(1) 選択肢分解：
  A子=H(R-1;(x-1,7);z)（x>=8）、B子=K1127のy=6全称閉形式cand6、
  C子=1 xor cand7(z-1,x,R-1)。x=7では2つのトークン減少手が同一多重集合
  (6,7)≡(7,6)子に合流しA≡B=cand6のz行x=7になる。分解が素再帰の選択肢値
  集合と一致することをraw二重再帰で錨止めする（C3・1,188点）。
  単一トークン閉形式・y=6子・x=7合流子もraw錨（C1b・46,086点）。cand6は
  出版検証器（K1127・SHA-256 2d75a817...）からの逐語転写でbyte照合済み。
  (2) 恒等式：cand7(z,x,R)=mex{A,B,C}（子は閉形式評価・Cはz外帰納）が
  R帰納の本体で、z=0..48×x=7..56×R<=x+z+40の233,975点（マージ・tail系込み）、
  深部tail z∈{60,72,84,96,108,120,240,400}の9,242点、z=0..120×x=7..120×
  R<=x+z+16の1,924,263点で直接照合。(3) 型機械：型=(x==7,z==0,z%2,x%2,
  R%2,6差分族w0..w5の±16窓±17番兵)、自由座標(v0,v1,v3)=±60ボックスで
  実現型54,762個を完全列挙し、型内confluenceと証人恒等式を機械検証
  （639,859点）。clip窓はK1127出版時の予想どおり2y+2=16の±16/±17がtight
  （±15/±16では中間帯下端R-z=2y+2=16が番兵16と衝突。族式候補2y+2は
  y=5:12,y=6:14,y=7:16で3族連続tight・2予想連続的中）。
  ボックス外新規型ゼロをv空間シェル掃引927,594点
  （max|v|∈[61,64]∪[89,92]∪[117,120]）、境界多様体581,526点
  （z∈{0..5,29..31,59..61,299..301,999..1001,2999,3000}・dx∈[-17,10]・
  tail窓[x+z+8,x+z+10]明示照合）、seeded遠方probe 200,000点（z,x<=3000・
  R<=9000・seed 20261123・tail境界を跨ぐ窓）、深グリッド掃引で確認。
  既出版のz=15（K1065）・z=16（K1077）・z=17（K1087）のy>=6一様全Grundy
  分類をY=2y=14・S=x+7引数変換・tail最優先で転写しy=7特殊化と全一致
  （C1d・x=7..159・R<=x+61の66,096点）・これら切片の低R単一トークン縮約
  R<=z+6もy=7行で照合（10,098点）。生エンジン直接照合C1がz=0..14・x=7..27・
  R<=x+z+46の22,365点、深z生censusアンカーC11がz=0..79・x=7..70・R<=x+z+12
  の931,840点（両エンジン×閉形式・マージ・tail系込み）。
  監査計5,594,132照合点（マージ系1,589,081点・tail系359,738点）・
  全チェック不一致0・同一cwd 2回＋別cwd別プロセス1回の計3回実行で
  audit.json byte-identical。加えてcensus_rows.pyがz=0..79・x=7..70・
  R<=x+z+12の465,920点で生順序保持再帰の行構造（Thue-Morse指数・T・P・
  tail）を抽出しtailアサートR>=x+z+8が全行成立、census.txtもbyte-identical
  再生する。有限監査は転写・実装照合であり、全称性は選択肢分解の健全性・
  正確なmex恒等式・有限型空間の完全性（K1023/K1099/K1104/K1112/K1126/
  K1127と同一trust境界）による。
---

## 命題・範囲

すべての z>=0、x>=7、R>=0 に対して H(R;(x,7);z)=cand7(z,x,R) が成り立つ。
cand7 は z 偶奇別のパラメトリック T/P 集合表（report.md に全文掲載）で、
値2位置はマージ行 O[1, q_odd(x+7)]（x<=z-8）、対角行 x=z-7 の
O[1, z+6]（奇z）/O[1, z+7]（偶z）（格子規則 r=z+y-[2(z-y)≡0 mod 4] の
y=7 値）、前倒しpin格子行（奇z d∈{-5,-1,3,7}→pin z+14+(d-7)/2、
偶z d∈{-3,1,5}→pin z+14+(d-7)/2）、掃引行 x=z+8 の
O[z+14, x+z+7]（奇z）/O[z+15, x+z+7]（偶z）、定常pin {z+14}（奇z）/
{z+15}（偶z）に整理される。値1位置は基底点 {z+1,...,z+13}（y=7 で y 点
仮説の全z確定・y=1..7 連続 7 例）、中間帯 O_z[z+16, x+z+7]、無限帯・tail
は偶数x行（y 奇の y=1,3,5 型に戻る）である。tail R>=x+z+8 の (x+7) mod 2
も全称に含む。z=0..5 でも例外行なし。

## マージ系（対角線下・y=7 の全称昇格）

x<=z-8（S=x+7<z）の全行で H(R;(x,7);z)=single_token(x+7,z,R)（全R）。
行全体が z 非依存になる。K1101 が y∈{1,2} で全称証明し、K1104 が y=3 を・
K1112 が y=4 を・K1126 が y=5 を・K1127 が y=6 を全称昇格させたマージ命題の
y=7 版が本項の閉形式から系として全称に昇格した（監査上も 1,589,081 点で
独立照合・不一致 0）。これでマージ命題は y=1..7 で全称確定。y=7 では
S=x+7 の偶奇が x と逆のため、値1無限帯は x 偶の行（奇数 y 型）。

## 出版切片との関係

y=7 行を含む固定z切片 K0887(z=6)・K0976(z=7, y>=4)・K0995(z=8)・
K0997(z=9)・K1009(z=10) と z=11..17 の y>=6 一様族 K1055/K1056/K1061/
K1062/K1065/K1077/K1087 の y=7 行は本項の z 行の特殊例である。
K1065/K1077/K1087 の published closed form は検証器に転写して y=7 特殊化と
全点一致を確認した（C1d・各 x=7..159・R<=x+61 の 66,096 点・これら切片の
低R単一トークン縮約 R<=z+6 の y=7 行も 10,098 点で照合）。z>=18 の
y=7 行は本項が直接分類するため、z=18,y=7 切片を含む以後の y=7 スライス
出版は不要。z<=10 の y=7 行は C1 の raw 直接照合と C11 生censusアンカー
（z=0..79）に含まれる。

## 導かれる構造（y=2..7 全称表からの横断観察）

- 値1基底点 y 点仮説 {z+1,..,z+2y-1} が y=7 で全 z>=0 確定（y=1..7 で
  連続 7 例。y>=8 は予想）。
- tail 開始式 x+z+y+1 が y=2..7 の 6 族連続で全称確定。tail 値 (x+y) mod 2
  も 6 族連続（y 奇で値1無限帯が偶数x行・y 偶で奇数x行）。
- マージ行の境界 x<=z-y-1 が y=1..7 の 7 族で確定（y=7: x<=z-8）。
  マージ命題（K1101）は y=1..7 で全称確定。
- 掃引行 x=z+y+1・帯 O[2y+z, 2z+2y+1]（奇z）/O[2y+z+1, 2z+2y+1]（偶z）・
  中間帯 O_z[2y+z+2, x+z+y]・定常pin 2y+z（奇z）/2y+z+1（偶z）は
  y=2..7 共通の族式。
- **前倒しpin格子公式**: pin行 x は (x-y)+z≡2 (mod 4) を満たし、pin値は
  pin=2y+((x-y)+z)/2。y=5,6,7 の 3 族で同一格子公式（pin行の d は
  d≡y (mod 4)（奇z）・d≡y+2 (mod 4)（偶z）。y=7 は奇z d≡3・偶z d≡1）。
  y>=8 への一般証明は今後の課題。
- 対角行上端格子規則 r=z+y-[2(z-y)≡0 mod 4] が y=7 の全 z で成立
  （y=2..7 の 6 族の全称表で全 z 一致。y>=8 は予想）。
- 型機械の clip 窓は K1127 の予想どおり ±16/±17（2y+2）が tight に確定
  （±15/±16 では中間帯下端 R-z=2y+2=16 が番兵と衝突。族式候補 2y+2 は
  y=5:12・y=6:14・y=7:16 と 3 族連続 tight・2 予想連続的中）。
- 値1無限帯の偶奇は z によらず S=x+y の偶奇のみで決まる（y=7 でも
  行クラス表の対称性からの素朴外拡は d=3 偶z 行で破れる。x 偶行規則で
  説明される）。

これらの横断法則は y=2..7 の全称表からの観察であり、y>=8 での一般証明を
含意しない。

## 現在の根拠と限界

全称性は (i) 選択肢分解の健全性（raw錨）・(ii) 正確な mex 恒等式の有限グリッド
照合と型ごとの機械検査・(iii) 実現型空間の有限性（ボックス完全列挙＋シェル・
多様体・遠方probe・深掃引で新規型ゼロ）に基づく。K1023/K1099/K1104/K1112/
K1126/K1127 と同一の trust 境界にあり、Lean 形式化ではない。H の定義は
K0832、B子の評価は K1127（さらに K1126・K1112・K1104・K1099・K1023）に
依存する。y>=8 族、基底点 y 点仮説と前倒しpin格子公式・対角行格子規則の
一般証明、clip 窓一般式の補題化、3トークン以上、固定幅・q点版安定化長、
11×11 は範囲外。
