---
id: K1141
title: 2トークン残余ゲーム y=10族のパラメトリック閉形式の全称証明（全z>=0・全x>=10・全R>=0）
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token y=10 parametric all-z universal proof, P10, cand10 fitting and box-out spot verification (fitting stage)]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・Theorem T・単一トークン閉形式のraw anchorに使用する
- type: depends_on
  target: K1138
  note: B子（y=9子）の評価にy=9パラメトリック全z全称閉形式cand9を使用する（x=10合流子(9,10)≡(10,9)も同一）。cand9は出版検証器verify_y9_universal.py（SHA-256 299acb6a...）からの逐語転写。B子にy=9全称閉形式を使う初の族
- type: generalizes
  target: K0999
  note: z=8・y=9境界切片は本項のK1000一様形の特殊例である（K1000との関係で間接的に被覆される）
- type: generalizes
  target: K1000
  note: z=8・y>=9一様全Grundy分類のy=10行は本項の特殊例（転写アンカーA8uとして照合）
- type: generalizes
  target: K1001
  note: z=9・y>=9一様全Grundy分類のy=10行は本項の特殊例（転写アンカーA9uとして照合）
- type: generalizes
  target: K1002
  note: z=10・y>=6一様Grundy候補のy=10行は本項の特殊例（転写アンカーA10uとして照合）
- type: generalizes
  target: K1011
  note: z=10・y>=9一様全Grundy分類（K1002候補の証明範囲）のy=10行は特殊例（転写アンカーとして照合）
- type: generalizes
  target: K1065
  note: z=15・y>=6族のy=10行は本項の特殊例（published closed formを転写アンカーA15uとして照合）
- type: generalizes
  target: K1077
  note: z=16・y>=6族のy=10行は特殊例（転写アンカーA16uとして照合）
- type: generalizes
  target: K1087
  note: z=17・y>=6族のy=10行は特殊例（転写アンカーA17uとして照合）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y10-parametric-allz-proof-20261120/report.md
  role: proof
  note: z偶奇別T/Pパラメトリック集合表による全称定理と、マージ系（対角線下・y=10の全称昇格でマージ命題はy=1..10確定）・選択肢分解・恒等式・型機械（clip 2y+2=22の±22/±23がtight、6族連続tight（y=5:12,y=6:14,y=7:16,y=8:18,y=9:20,y=10:22）・5予想連続的中）による証明構成、part2 published切片転写アンカーC1d（z=8/9/10/15/16/17のy=10特殊化・組み込み前生両エンジン事前検証・低R縮約R<=z+6のy=10行照合）、独立census、tail開始式x+z+y+1のy=2..10確定、基底点10点・pin格子公式pin=z+(d+3y)/2のy=5..10統一・対角行格子規則y=2..10全z一致の横断観察
- path: research/experiments/vertical-fiber-two-token-y10-parametric-allz-proof-20261120/verify_y10_universal.py
  role: verifier
  note: 13機械チェック（C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12）6,406,346照合点（マージ系1,494,591点・tail系274,835点）・不一致0実現型121,461・全走型123,543・3回実行（同一cwd 2回＋別cwd隔離copy 1回）でaudit.json byte-identical、純Python約75秒、seed 20261130、part2正本SHA-256 f9169449...
- path: research/experiments/vertical-fiber-two-token-y10-parametric-allz-proof-20261120/census_rows.py
  role: verifier
  note: z=0..79・x=10..70・R<=x+z+12の生二重再帰センサス、451,400点（4,880行）・エンジン状態数5,118,827・値0点数225,680・tailアサート全行成立・約18.4秒・cand10独立照合451,400点不一致0
- path: research/experiments/vertical-fiber-two-token-y10-parametric-allz-proof-20261120/output/audit.json
  role: data
  note: 検証器の決定論的監査出力（固定seed・ソート済みキー・part2正本SHA-256 41b7a315...）
- path: research/experiments/vertical-fiber-two-token-y10-parametric-allz-proof-20261120/output/census.txt
  role: data
  note: センサスの決定論的行表出力4,880行＋空行80（SHA-256 7aec116d...・831,928 bytes）
- path: research/log/2026-11-20-y10-parametric-allz-proof-part1.md
  role: log
  note: part1（12チェック6,265,496点全PASS・3回byte-identical・昇格はpart2で）
- path: research/log/2026-11-20-y10-parametric-allz-proof-part2.md
  role: log
  note: part2（C1d事前検証と転写バグ捕捉・census・3回byte-identical・K1141 observed→proved昇格・出版記録）
- path: research/log/2026-11-20-y10-two-token-skeleton-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-20T10:25:00Z・fit・preflight・正本監査part1/part2・昇格出版の全工程を保持）
- path: research/experiments/vertical-fiber-two-token-y10-parametric-allz-fit-20261120/report.md
  role: data
  note: cand10のz偶奇別T/P集合表全文（pin統一式の6族連続・偶z対角行の値1全欠如〔3族連続〕・最終pin行d=yの値1帯I[z+2y+1)〔4族連続〕・掃引帯の偶奇がoffset基準である点〔y=10で顕在化〕・奇z/偶zのpin行d範囲が互いに逆に寄る遷移を含む）とfitting段階の検証規模の記録
- path: research/experiments/vertical-fiber-two-token-y10-parametric-allz-fit-20261120/cand10.py
  role: verifier
  note: 閉形式の正本cand10（in_T10値2表・in_P10値1表・Y=10）とprobe全点照合（72,261点・mismatch 0・SHA-256 7c08e065...）。正本検証器は本ファイルを逐語転写
- path: research/log/2026-11-20-two-token-y10-parametric-allz-fit.md
  role: log
  note: fit段階の宣言確認・導出経緯（T初稿255点不一致の原因=掃引帯の偶奇基準）・出版記録
- path: research/experiments/vertical-fiber-two-token-y10-universal-machine-preflight-20261120/report.md
  role: data
  note: 正本実装前のJS/Python予備検査（C2a-C2d/C3/C1b/C1c・出版K1138二重cand9転写の意味同一性308,484点）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,10)、全z>=0・全x>=10・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand10）で
  完全分類する。K0999/K1000（z=8）・K1001（z=9）・K1002/K1011（z=10）の
  y=10行とK1065/K1077/K1087（z=15,16,17のy>=6族）のy=10行は本項の特殊例
  であり、z>=18（z=18,y=10を含む）のy=10行も主張に含まれる（以後のy=10
  スライス出版は不要）。系としてx<=z-11（S=x+10<z-1）の全R行が単一
  トークン値single_token(x+10,z,R)に一致するマージ命題のy=10版が全称に
  昇格する（マージ命題はy=1..10で全称確定）。tail R>=x+z+11=(x+z+y+1)の
  (x+10) mod 2も全称に含む。
evidence: >-
  証明はK1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138と同型の3部構成。
  (1) 選択肢分解：A子=H(R-1;(x-1,10);z)（x>=11）、B子=K1138のy=9全称閉形式
  cand9、C子=1 xor cand10(z-1,x,R-1)。x=10では2つのトークン減少手が同一
  多重集合(9,10)≡(10,9)子に合流しA≡B=cand9(z,10,R-1)のz行x=10になる。
  分解が素再帰の選択肢値集合と一致することをraw二重再帰で錨止めする
  （C3・1,065点）。単一トークン閉形式・y=9子・x=10合流子もraw錨
  （C1b・42,473点）。cand9は出版検証器（K1138・SHA-256 299acb6a...）から
  の逐語転写。(2) 恒等式：cand10(z,x,R)=mex{A,B,C}（子は閉形式評価・
  Cはz外帰納）がR帰納の本体で、z=0..48×x=10..56×R<=x+z+40の223,391点
  （マージ・tail系込み）、深部tail z∈{60,72,84,96,108,120,240,400}の
  18,700点、z=0..120×x=10..120×R<=x+z+16の1,893,771点で直接照合。
  (3) 型機械：型=(x==10,z==0,z%2,x%2,R%2,6差分族w0..w5の±22窓±23番兵)、
  自由座標(v0,v1,v3)=±60ボックスで実現型121,461個を完全列挙し、型内
  confluenceと証人恒等式を機械検証（626,145点・identity_bad 0・
  confluence_bad 0）。clip窓は2y+2=22の±22/±23がtight（clip 21では
  confluence違反4,736件〔identity不変〕・初違反(z=60,x=84,R=84)・中間帯
  下端R-z=2y+2=22が番兵22と衝突する型。族式候補2y+2はy=5:12,y=6:14,
  y=7:16,y=8:18,y=9:20,y=10:22で6族連続tight・予想5連続的中）。
  ボックス外新規型ゼロをv空間シェル掃引920,502点
  （|v|∈[61,64]∪[89,92]∪[117,120]）、境界多様体788,454点
  （z∈{0..5,29..31,59..61,299..301,999..1001,2999,3000}・dx∈[-23,14]・
  tail窓[x+z+11,x+z+13]明示照合）、seeded遠方probe 200,000点（z,x<=3000・
  R<=9000・seed 20261130・tail境界x+z+11を跨ぐ窓）、深グリッド掃引（全走型
  123,543・新規型0・confluence不一致0）で確認。既出版のz=8（K0999/K1000）・
  z=9（K1001）・z=10（K1002/K1011）・z=15/16/17（K1065/K1077/K1087）を
  転写しy=10特殊化を照合（C1d・140,850点=アンカー130,950点〔x=10..159・
  R<=x+61〕＋低R単一トークン縮約R<=z+6のy=10行9,900点〔z=15,16,17で
  R<=21,22,23〕・不一致0）。アンカー組み込み前にy=10行を生両エンジンで
  事前検証（各切片x=10..45・R<=x+z0+30の計15,336点でH_ordered/
  H_canonical/cand10三者一致。この事前検証がK1087転写初稿の評価順バグ
  〔170点不一致〕を捕捉・修正、出版正本は修正後のみ）。生エンジン直接照合
  C1がz=0..14・x=10..29・R<=x+z+46の22,050点、深z生censusアンカーC11が
  z=0..79・x=10..70・R<=x+z+12の902,800点（両エンジン・cache clear
  エンジン間）。監査計6,406,346照合点（マージ系1,494,591点・tail系
  274,835点・それぞれ不一致0）・全チェック不一致0・同一cwd 2回＋別cwd
  隔離copy 1回の計3回実行でaudit.json byte-identical（SHA-256 41b7a315...）。
  加えてcensus_rows.pyがz=0..79・x=10..70・R<=x+z+12の451,400点（4,880行）
  で生tuple二重再帰の行構造（Thue-Morse指数・T・P・tail）を抽出しtail
  アサートR>=x+z+11の(x+10) mod 2が全行成立、エンジン状態数5,118,827、
  値0点数225,680、census.txtは閉形式cand10との独立照合で451,400点
  不一致0（第三実装）。有限監査は転写・実装照合であり、全称性は選択肢
  分解の健全性・正確なmex恒等式・有限型空間の完全性
  （K1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138と同一trust境界）
  による。
---

## 命題・範囲

すべての z>=0、x>=10、R>=0 に対して H(R;(x,10);z)=cand10(z,x,R) が成り立つ。
cand10 は z 偶奇別のパラメトリック T/P 集合表（proof 実験dir の report.md に
全文掲載・fit 実験dirの cand10.py が正本）で、値2位置はマージ行
O[1, q_odd(x+10)]（x<=z-11）、対角行 d=-10 の O[1, z+10]（奇z）/O[1, z+9]
（偶z）（格子規則 r=z+y-[2(z-y)≡0 mod 4] の y=10 値）、前倒しpin格子行
（奇z d∈{-6,-2,2,6,10}→pin z+12,z+14,z+16,z+18,z+20・偶z
d∈{-8,-4,0,4,8}→pin z+11,z+13,z+15,z+17,z+19・pin=z+(d+3y)/2）、掃引行
d=11 の O_z[z+20, x+z+10]（奇z）/O_z[z+21, x+z+10]（偶z）（偶奇基準は
R≡z mod 2 の offset 基準）。定常pin {z+20}（奇z）/{z+21}（偶z）
（2y+z／2y+z+1）に整理される。値1位置は基底点 {z+1,z+3,...,z+19} の
10点（y=10 は y 点仮説の全z確定・y=1..10 連続 10 例）、中間帯
O_z[z+22, x+z+10]（下端 z+2y+2）、無限帯・tail は奇数 x 行（偶数 y 型・
y=9 の逆）である。tail R>=x+z+11=(x+z+y+1) の (x+10) mod 2 も全称に含む。
z=0..9 でも例外行なし。奇 z の pin 行 d=10（d=y）は値1帯
bk ∪ {z+21} ∪ I[z+22]（追加点 z+21=2y+z+1・偶数 y では初の例）。
偶 z の対角行（d=-10）は値1を一切持たない（y=8/y=9 と同じ型・3族連続）。

## マージ系（対角線下・y=10 の全称昇格）

x<=z-11（S=x+10<z-1）の全行で H(R;(x,10);z)=single_token(x+10,z,R)
（全R）。行全体が z 非依存になる。K1101 が y∈{1,2} で全称証明し、
y=3..9 が K1104/K1112/K1126/K1127/K1131/K1135/K1138 で全称昇格済みの
マージ命題の y=10 版が本項の閉形式から系として全称に昇格した（監査上も
1,494,591 点で独立照合・不一致 0）。これでマージ命題は y=1..10 で
全称確定した。y=10 では S=x+10 の偶奇が x と一致するため、値1無限帯は
x 奇の行（偶数 y 型・マージ行では x 奇のみ I[x+11,∞)）。

## 出版切片との関係

y=10 行を含む固定z切片 K1000（z=8・y>=9）・K1001（z=9・y>=9）・
K1002/K1011（z=10）と z=15,16,17 の y>=6 一様族 K1065/K1077/K1087 の
y=10 行は本項の特殊例である。これらの published closed form
（uniform (x,y,r) 形）は検証器に転写して y=10 特殊化と全点一致を確認した
（C1d・140,850点・組み込み前の生両エンジン事前検証15,336点込みで
不一致0）・低R単一トークン縮約 R<=z+6 の y=10 行も直接照合（z=15,16,17
で R<=21,22,23・不一致 0）。z>=18 の y=10 行は本項が直接分類するため、
z=18,y=10 切片を含む以後の y=10 スライス出版は不要。z<=14 の y=10 行は
C1 の raw 直接照合と C11 生censusアンカー（z=0..79）に含まれる。

## 導かれる構造（y=2..10 全称表からの横断観察）

- 値1基底点 y 点仮説 {z+1,..,z+2y-1} が y=10 で全 z>=0 確定（y=1..10 で
  連続 10 例。y>=11 は予想）。
- tail 開始式 x+z+y+1 が y=2..10 の 9 族連続で全称確定。tail 値 (x+y) mod 2
  も 9 族連続（y 奇で値1無限帯が偶数x行・y 偶で奇数x行）。
- マージ行の境界 x<=z-y-1 が y=1..10 の 10 族で確定（y=10: x<=z-11）。
  マージ命題（K1101）は y=1..10 で全称確定。
- 掃引行 x=z+y+1・帯 O_z[2y+z, x+z+y]（y=10: O_z[z+20, x+z+10]・offset基準）・
  中間帯下端 z+2y+2（y=10: z+22）・定常pin 2y+z（奇z）/2y+z+1（偶z）は
  族式どおり（y=10 で掃引帯の偶奇が offset 基準であることが初めて顕在化）。
- 前倒しpin格子公式 pin=z+(d+3y)/2〔pin行の(x-y)+z≡2 mod 4・pin行のdは
  d≡y(mod 4)（奇z）・d≡y+2(mod 4)（偶z）〕が y=5..10 の 6 族で統一。
  pin 行数は y=9/y=10 とも 5/5。偶 z pin 行の d 範囲は y=9 [-y+4,y+2]
  → y=10 [-y+2,y-2]（y=8 形へ復帰）・奇 z は y=9 [-y+2,y] → y=10
  [-y+4,y]。pin 行 d 範囲の一般族式はなく、一般証明は今後の課題。
- 対角行上端格子規則 r=z+y-[2(z-y)≡0 mod 4] が y=10 の全 z で成立
  （y=2..10 の 9 族の全称表で全 z 一致。y>=11 は予想）。
- 型機械の clip 窓は K1135 出版時の予想系列どおり ±22/±23（2y+2）が
  tight に確定（clip 21 では中間帯下端 R-z=2y+2=22 が番兵 22 と衝突して
  confluence 違反 4,736 件〔identity は不変〕。族式候補 2y+2 は
  y=5..10 と 6 族連続 tight・予想 5 連続的中）。
- pin 行の追加値1点 2y+z+1：y=10 奇z の d=10 行の z+21 は y=6 の d=7 行
  （K1127）・y=8 の d=8 行（K1135）・y=9 の d=9 行（K1138）と同じ最終
  pin 行パターン（4 族連続・y=10 は偶数 y 初例）。

これらの横断法則は y=2..10 の全称表からの観察であり、y>=11 での
成立を含意しない。

## fitting 段階の記録（observed → proved の経緯）

本項は 2026-11-20 に fitting（probe box 72,261 点＋box 外 spot 27,318 点＝
99,579 点・mismatch 0・skeleton survey からの fit lane）として status
observed で出版された後、同日に正本監査 part1（12チェック
6,265,496 照合点・3回 byte-identical）を経て part2（C1d 140,850 点・
census 451,400 点・全機械計 6,406,346 照合点・3回 byte-identical）により
observed から proved に昇格した（AGENTS.md「同じ命題の status や証拠の
更新は同じ K 項目」・新規採番なし）。fitting 段階の生probe・pin統一式の
実測事実（掃引帯の偶奇が offset 基準・偶 z pin 行 d 範囲の復帰・最終
pin 行 d=y の値1帯 b10∪I[z+2y+1)）は閉形式にそのまま含まれ、正本監査で
全 z・全 x・全 R で確定した。

## 現在の根拠と限界

全称性は (i) 選択肢分解の健全性（raw錨）・(ii) 正確な mex 恒等式の有限
グリッド照合と型ごとの機械検査・(iii) 実現型空間の有限性（ボックス完全
列挙＋シェル・多様体・遠方probe・深掃引で新規型ゼロ）に基づく。
K1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138 と同一の trust 境界に
あり、Lean 形式化ではない。H の定義は K0832、B子の評価は K1138（さらに
K1135..K1023）に、C1d アンカー切片の正しさは K0999/K1000/K1001/K1002/
K1011/K1065/K1077/K1087 に依存する。y>=11 族、基底点 y 点仮説と前倒し
pin格子公式・対角行格子規則・clip 窓一般式の一般証明、pin 行 d 範囲の
族式化、低R単一トークン縮約 R<=z+6 の全 z 一般化、3トークン以上、固定幅・
q点版安定化長、11×11 は範囲外。REFUTED-D10 型の実験とは異なり LOSS 証明を
含まず、標準 11×11 盤面の各種パラメータの値は本項では UNKNOWN のまま。

## 採番記録

作業中仮番号 K1140 で出版を試みたが、push 直前の README 実ファイル再取得で並走の
n11 fold24 レーンが commit fc4c18fdd（後に 456b48449 で schema 整備）で
items/K1140-n11-residual29-win8-receipt-fold-root438000000818.md
（WIN8-D10 receipt fold・fold24）を先行出版済みであることを検出し、AGENTS.md
再採番規約（first-published-priority・K1135〔仮番号K1133〕・K1138〔仮番号K1137〕と
同じ手続き）により次の空き番号 K1141 へ再採番した。push 直前の items 系コミット
再取得で K1140 が n11 の item に使用済み・K1141 未使用を確認済み。
