---
id: K1138
title: 2トークン残余ゲーム y=9族のパラメトリック閉形式の全称証明（全z>=0・全x>=9・全R>=0）
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token y=9 parametric all-z universal proof, P9, cand9 fitting and box-out spot verification (fitting stage)]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・Theorem T・単一トークン閉形式のraw anchorに使用する
- type: depends_on
  target: K1135
  note: B子（y=8子）の評価にy=8パラメトリック全z全称閉形式cand8を使用する（x=9合流子(8,9)≡(9,8)も同一）。cand8は出版検証器verify_y8_universal.py（SHA-256 bcad4148...）からの逐語転写で対称的に確認
- type: generalizes
  target: K0999
  note: z=8・y=9境界切片は本項の特殊例（転写アンカーA8y9として照合）
- type: generalizes
  target: K1000
  note: z=8・y>=9一様全Grundy分類のy=9行は本項の特殊例（転写アンカーとして照合）
- type: generalizes
  target: K1001
  note: z=9・y>=9一様全Grundy分類のy=9行は本項の特殊例（転写アンカーA9y9として照合）
- type: generalizes
  target: K1002
  note: z=10・y>=6一様Grundy定理のy=9行は本項の特殊例（転写アンカーA10y9として照合）
- type: generalizes
  target: K1011
  note: z=10・y>=9一様全Grundy分類のy=9行は本項の特殊例（転写アンカーとして照合）
- type: generalizes
  target: K1065
  note: z=15・y>=6族のy=9行は本項の特殊例（published closed formを転写アンカーA15y9として照合）
- type: generalizes
  target: K1077
  note: z=16・y>=6族のy=9行は特殊例（転写アンカーA16y9として照合）
- type: generalizes
  target: K1087
  note: z=17・y>=6族のy=9行は特殊例（転写アンカーA17y9として照合）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-proof-20261120/report.md
  role: proof
  note: z偶奇別T/Pパラメトリック集合表による全称定理と、マージ系（対角線下・y=9の全称昇格でマージ命題はy=1..9確定）・選択肢分解・恒等式・型機械（K1135予想どおり2y+2=20の±20/±21がtight、5族連続tight（y=5:12,y=6:14,y=7:16,y=8:18,y=9:20）・4予想連続的中）による証明構成、出版切片転写アンカー（z=8/9/10/15/16/17のy=9特殊化・低R縮約R<=z+6のy=9行照合）、tail開始式x+z+y+1のy=2..9確定、基底点9点・pin格子公式pin=z+(d+3y)/2のy=5..9統一・対角行格子規則y=2..9全z一致・偶z pin行d範囲シフト（y=8の[-y+2,y-2]→y=9の[-y+4,y+2]）の横断観察
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-proof-20261120/verify_y9_universal.py
  role: verifier
  note: 12チェック5,742,841照合点（マージ系1,526,072点・tail系302,657点）・不一致0・実現型95,844・全走型96,500・3回実行（同一cwd 2回＋別cwd別HOME env -i隔離1回）でaudit.json byte-identical・純Python約66〜70秒・seed 20261123
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-proof-20261120/census_rows.py
  role: verifier
  note: z=0..79・x=9..70・R<=x+z+12の生二重再帰センサス、456,320点（4,960行）・エンジン状態数4,682,179・値0点数227,416・tailアサート全行成立・約17.4秒
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-proof-20261120/output/audit.json
  role: data
  note: 検証器の決定論的監査出力（固定seed・ソート済みキー・SHA-256 f12c17b1158cd42a5000725d3acb98eeb5110f9e1cb402d3b95957fbe3697053）
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-proof-20261120/output/census.txt
  role: data
  note: センサスの決定論的行表出力4,960行（SHA-256 1904c550779837af8bfd659309c05abdd03c8f8abe04afa7d5a2301d4758a953・844,176 bytes）
- path: research/log/2026-11-20-two-token-y9-parametric-allz-proof.md
  role: log
  note: 宣言の確認・JS予備検査からの仕様引継ぎ・正本監査・出版記録（K1138昇格・新規採番なし）、次に開くもの
- path: research/log/2026-11-20-y9-universal-machine-js-preflight.md
  role: log
  note: 正本実装に先立つJSサンドボックス予備検査（12チェック仕様確定・seed 20261123・全bad=0・期待点数一致）
- path: research/log/2026-11-20-two-token-y9-parametric-allz-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-20T08:41:00Z。fit・JS予備検査・正本監査・census・出版の全工程を保持）
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-fit-20261120/report.md
  role: data
  note: cand9のz偶奇別T/P集合表全文（pin統一式・偶z対角行の値1全欠如・偶z pin行d範囲の+2シフト〔y=8の[-y+2,y-2]→y=9の[-y+4,y+2]〕・奇z d=y行の値1追加点z+19=2y+z+1を含む）とfitting段階の検証規模の記録
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-fit-20261120/cand9.py
  role: verifier
  note: 閉形式の正本cand9（in_T9値2表・in_P9値1表・Y=9）とprobe_rows.txt全点照合（73,811点・mismatch 0・T/P重複 0）。正本検証器は本ファイルを逐語転写
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-fit-20261120/probe_y9.py
  role: data
  note: 生二重再帰probeエンジン（順序保持・降順正準形メモ化・z=0..30・x=9..z+27・R<=x+z+26・1,054行RLE生成）
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-fit-20261120/spot9.py
  role: verifier
  note: box外spot照合25,376点（深R<=130・z=31..40・x=y=9エッジz=9..40・d<=52・bad 0）
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-fit-20261120/output/audit.json
  role: data
  note: fitting段階の実行監査（統計・SHA-256・再生コマンド・probe_rows.txtは公開せず決定論的再生可能の注記）
- path: research/log/2026-11-20-two-token-y9-parametric-fit.md
  role: log
  note: 宣言の確認・導出経緯・出版記録（K1137競合検出とK1138への再採番を含む）・次に開くもの（12チェック監査）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,9)、全z>=0・全x>=9・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand9）で完全分類する。
  K0999(z=8)・K1001(z=9)・K1002/K1011(z=10)のy=9行と
  K1065/K1077/K1087（z=15,16,17のy>=6族）のy=9行は本項の特殊例であり、
  z>=18（z=18,y=9を含む）のy=9行も主張に含まれる（以後のy=9スライス出版は不要）。
  系としてx<=z-10（S=x+9<z-1）の全R行が単一トークン値single_token(x+9,z,R)
  に一致するマージ命題のy=9版が全称に昇格する（マージ命題はy=1..9で全称確定）。
  tail R>=x+z+10=(x+z+y+1)の(x+9) mod 2も全称に含む。
evidence: >-
  証明はK1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135と同型の3部構成。
  (1) 選択肢分解：A子=H(R-1;(x-1,9);z)（x>=10）、B子=K1135のy=8全称閉形式
  cand8、C子=1 xor cand9(z-1,x,R-1)。x=9では2つのトークン減少手が同一多重集合
  (8,9)≡(9,8)子に合流しA≡B=cand8(z,9,R-1)のz行x=9になる。分解が素再帰の
  選択肢値集合と一致することをraw二重再帰で錨止めする（C3・1,035点）。
  単一トークン閉形式・y=8子・x=9合流子もraw錨（C1b・43,692点）。cand8は
  出版検証器（K1135・SHA-256 bcad4148...）からの逐語転写。(2) 恒等式：
  cand9(z,x,R)=mex{A,B,C}（子は閉形式評価・Cはz外帰納）がR帰納の本体で、
  z=0..48×x=9..56×R<=x+z+40の226,968点（マージ・tail系込み）、
  深部tail z∈{60,72,84,96,108,120,240,400}の9,330点、z=0..120×x=9..120×
  R<=x+z+16の1,904,056点で直接照合。(3) 型機械：型=(x==9,z==0,z%2,x%2,
  R%2,6差分族w0..w5の±20窓±21番兵)、自由座標(v0,v1,v3)=±60ボックスで
  実現型95,844個を完全列挙し、型内confluenceと証人恒等式を機械検証
  （630,822点・identity_bad 0・confluence_bad 0）。clip窓はK1135出版時の
  予想どおり2y+2=20の±20/±21がtight（±19/±20では中間帯下端R-z=2y+2=20が
  番兵20と衝突してconfluence違反5,355件〔identityは不変〕。族式候補2y+2は
  y=5:12,y=6:14,y=7:16,y=8:18,y=9:20で5族連続tight・予想4連続的中）。
  ボックス外新規型ゼロをv空間シェル掃引922,890点
  （|v|∈[61,64]∪[89,92]∪[117,120]）、境界多様体727,077点
  （z∈{0..5,29..31,59..61,299..301,999..1001,2999,3000}・dx∈[-21,13]・
  tail窓[x+z+10,x+z+12]明示照合）、seeded遠方probe 200,000点（z,x<=3000・
  R<=9000・seed 20261123・tail境界x+z+10を跨ぐ窓）、深グリッド掃引（全走型
  96,500・新規型0・confluence不一致0）で確認。既出版のz=8（K0999/K1000）・
  z=9（K1001）・z=10（K1002/K1011）・z=15/16/17（K1065/K1077/K1087）を
  転写しy=9特殊化（z>=15はY=2y=18・S=x+9引数変換・tail最優先・過渡セルは
  y=9では2y+d>17で全て消滅）と全一致（C1d・アンカー131,370点・6切片×
  21,895・x=9..159・R<=x+61）・これら切片の低R単一トークン縮約R<=z+6も
  y=9行で照合（z=15,16,17でR<=21,22,23・9,966点・不一致0）。生エンジン
  直接照合C1がz=0..14・x=9..29・R<=x+z+46の22,995点、深z生censusアンカー
  C11がz=0..79・x=9..70・R<=x+z+12の912,640点（両エンジン・cache clear
  エンジン間）。監査計5,742,841照合点（マージ系1,526,072点・tail系
  302,657点・それぞれ不一致0）・全チェック不一致0・同一cwd 2回＋別cwd別
  HOME env -i 1回の計3回実行でaudit.json byte-identical
  （SHA-256 f12c17b1...）。加えてcensus_rows.pyがz=0..79・x=9..70・
  R<=x+z+12の456,320点（4,960行）で生順序保持再帰の行構造（Thue-Morse指数・
  T・P・tail）を抽出しtailアサートR>=x+z+10の(x+9) mod 2が全行成立、
  エンジン状態数4,682,179・値0点数227,416。有限監査は転写・実装照合であり、
  全称性は選択肢分解の健全性・正確なmex恒等式・有限型空間の完全性
  （K1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135と同一trust境界）による。
---

## 命題・範囲

すべての z>=0、x>=9、R>=0 に対して H(R;(x,9);z)=cand9(z,x,R) が成り立つ。
cand9 は z 偶奇別のパラメトリック T/P 集合表（report.md に全文掲載・
fit 実験dirの cand9.py が正本）で、
値2位置はマージ行 O[1, q_odd(x+9)]（x<=z-10）、対角行 x=z-9 の
O[1, z+8]（奇z）/O[1, z+9]（偶z）（格子規則 r=z+y-[2(z-y)≡0 mod 4] の
y=9 値）、前倒しpin格子行（奇z d∈{-7,-3,1,5,9}→pin z+10,z+12,z+14,z+16,
z+18、偶z d∈{-5,-1,3,7,11}→pin z+11,z+13,z+15,z+17,z+19・pin=z+(d+3y)/2
〔(x-y)+z≡2 mod 4〕）、掃引行 x=z+10 の O[z+18, x+z+9]（奇z）/
O[z+19, x+z+9]（偶z）、定常pin {z+18}（奇z）/{z+19}（偶z）（2y+z／2y+z+1）
に整理される。値1位置は基底点 {z+1,...,z+17}（y=9 は y 点仮説の全z確定・
y=1..9 連続 9 例）、中間帯 O_z[z+20, x+z+9]（奇 z では定常pin z+18 を
明示的に除外）、無限帯・tail は偶数 x 行（y 奇の y=1,3,5,7 型）である。
tail R>=x+z+10 の (x+9) mod 2 も全称に含む。z=0..8 でも例外行なし。
奇 z の pin 行 d=9 は値1点 z+19（2y+z+1）を追加する（y=6 d=7・y=8 d=8 と
同じ最終pin行パターン）。偶 z の対角行（d=-9）は値1を一切持たない
（y=8 偶z d=-8 と同型）。

## マージ系（対角線下・y=9 の全称昇格）

x<=z-10（S=x+9<z-1）の全行で H(R;(x,9);z)=single_token(x+9,z,R)（全R）。
行全体が z 非依存になる。K1101 が y∈{1,2} で全称証明し、y=3..8 が
K1104/K1112/K1126/K1127/K1131/K1135 で全称昇格済みのマージ命題の y=9 版が
本項の閉形式から系として全称に昇格した（監査上も 1,526,072 点で独立照合・
不一致 0）。これでマージ命題は y=1..9 で全称確定。y=9 では S=x+9 の偶奇が
x と逆のため、値1無限帯は x 偶の行（奇数 y 型・マージ行では I[x+8,∞)）。

## 出版切片との関係

y=9 行を含む固定z切片 K0999/K1000(z=8)・K1001(z=9)・K1002/K1011(z=10) と
z=15,16,17 の y>=6 一様族 K1065/K1077/K1087 の y=9 行は本項の特殊例である。
これらの published closed form は検証器に転写して y=9 特殊化（z>=15 は
Y=2y=18・S=x+9 引数変換・tail 最優先・過渡セルは y=9 では消滅）と全点一致
を確認した（C1d・131,370点）・低R単一トークン縮約 R<=z+6 の y=9 行も直接
照合（z=15,16,17 で R<=21,22,23・不一致 0）。z>=18 の y=9 行は本項が直接
分類するため、z=18,y=9 切片を含む以後の y=9 スライス出版は不要。
z<=14 の y=9 行は C1 の raw 直接照合と C11 生censusアンカー（z=0..79）に
含まれる。

## 導かれる構造（y=2..9 全称表からの横断観察）

- 値1基底点 y 点仮説 {z+1,..,z+2y-1} が y=9 で全 z>=0 確定（y=1..9 で
  連続 9 例。y>=10 は予想）。
- tail 開始式 x+z+y+1 が y=2..9 の 8 族連続で全称確定。tail 値 (x+y) mod 2
  も 8 族連続（y 奇で値1無限帯が偶数x行・y 偶で奇数x行）。
- マージ行の境界 x<=z-y-1 が y=1..9 の 9 族で確定（y=9: x<=z-10）。
  マージ命題（K1101）は y=1..9 で全称確定。
- 掃引行 x=z+y+1・帯 O[2y+z, x+z+y]（y=9: O[z+18, x+z+9]）・中間帯
  O_z[2y+z+2, x+z+y]・定常pin 2y+z（奇z）/2y+z+1（偶z）は y=2..9 共通の族式。
- 前倒しpin格子公式 pin=z+(d+3y)/2〔pin行の(x-y)+z≡2 mod 4・pin行のdは
  d≡y(mod 4)（奇z）・d≡y+2(mod 4)（偶z）〕が y=5..9 の 5 族で統一。
  pin 行数は y=9 で初めて奇z・偶zとも 5 行（y=8 は4/4）。偶 z pin 行の
  d 範囲は y=9 で [-y+4, y+2] にシフト（y=7:[-y+4,y-2]・y=8:[-y+2,y-2]）。
  一般証明は今後の課題。
- 対角行上端格子規則 r=z+y-[2(z-y)≡0 mod 4] が y=9 の全 z で成立
  （y=2..9 の 8 族の全称表で全 z 一致。y>=10 は予想）。
- 型機械の clip 窓は K1135 出版時の予想どおり ±20/±21（2y+2）が tight に
  確定（±19/±20 では中間帯下端 R-z=2y+2=20 が番兵と衝突して confluence
  違反 5,355 件〔identity は不変〕。族式候補 2y+2 は y=5..9 と 5 族連続
  tight・予想 4 連続的中）。
- pin 行の追加値1点 2y+z+1：y=9 奇z の d=9 行の z+19 は y=6 の d=7 行
  （K1127）・y=8 の d=8 行（K1135）と同じ最終pin行パターン（3 族連続）。

これらの横断法則は y=2..9 の全称表からの観察であり、y>=10 での一般証明を
含意しない。

## fitting 段階の記録（observed → proved の経緯）

本項は 2026-11-20 に fitting（probe box 73,811 点＋box 外 spot 25,376 点＝
99,187 点・mismatch 0）として status observed で出版された後、同日の
12チェック正本監査（上記 evidence・5,742,841 照合点）により observed から
proved に昇格した。fitting 段階の生probe・pin統一式の実測事実（偶 z pin 行
d 範囲の +2 シフト・偶 z 対角行の値1全欠如・奇 z d=y 行の値1追加点 z+19 は
閉形式にそのまま含まれ、正本監査で全 z・全 x・全 R で確定した。

## 現在の根拠と限界

全称性は (i) 選択肢分解の健全性（raw錨）・(ii) 正確な mex 恒等式の有限グリッド
照合と型ごとの機械検査・(iii) 実現型空間の有限性（ボックス完全列挙＋シェル・
多様体・遠方probe・深掃引で新規型ゼロ）に基づく。K1023/K1099/K1104/K1112/
K1126/K1127/K1131/K1135 と同一の trust 境界にあり、Lean 形式化ではない。
H の定義は K0832、B子の評価は K1135（さらに K1131・K1127・K1126・K1112・
K1104・K1099・K1023）に依存する。y>=10 族、基底点 y 点仮説と前倒しpin格子
公式・対角行格子規則の一般証明、clip 窓一般式の補題化、低R単一トークン縮約
R<=z+6 の全 z 一般化、3トークン以上、固定幅・q点版安定化長、11×11 は範囲外。
REFUTED-D10 型の実験とは異なり LOSS 証明を含まず、標準 11×11 盤面の各種
パラメータの値は本項では UNKNOWN のまま。

## 採番記録

作業中仮番号 K1137 で出版を試みたが、push 直前の README 実ファイル再取得で
並走の n11 residual29 レーンが items/K1137-n11-residual29-win8-cert-extract-root00000000000200003800200008180000.md
を先行出版済みであることを検出し、AGENTS.md 再採番規約により次の空き番号
K1138 へ再採番した（K1135〔仮番号K1133〕と同じ手続き・first-published-priority）。
全称証明への昇格にあたり、AGENTS.md「同じ命題の status や証拠の更新は、
原則として同じ K 項目を更新する」に従い新規採番なしで本項を proved 昇格した。
