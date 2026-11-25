---
id: K1235
title: "2トークン残余ゲーム y=15族のパラメトリック閉形式の全称証明（全z>=0・全x>=15・全R>=0）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "two-token y=15 parametric closed-form fit, P15-fit"
  - "cand15 fitting and box-out spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 74,865 probe points; odd-y template extrapolation from the published FINAL cand13, the promoted-universal y=13 table)"
  - "universal proof completed (2026-11-22, part1+part2 under single-owner declaration c34a19ff): observed -> proved via the 14-check canonical audit at 6,935,639 comparison points bad 0, C1d published-slice anchors preflighted 4-way (13,485+9,570 pts), census_rows.py third implementation consumed by C11r (448,000 pts); clip window 2y+2=32 tight, 11-family streak y=5..15; merge proposition now universal through y=1..15"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（マージ行 x<=z-16 の回帰計14,325比較・境界行spot照合に使用）
- type: extends
  target: K1231
  note: y=13族全称閉形式（K1231・昇格済み）の次の奇数y族。cand15初稿はy=13出版最終構造cand13（全称証明済み）のY+2外挿で生成し、probe 74,865点に一発一致（cand11→cand13に続き奇数y seed法則2連続・全体で3連続一発一致）
- type: extends
  target: K1233
  note: y=14族全称閉形式（K1233・昇格済み）の次族。次段階の全称検証器のB子は出版cand14の逐語転写（x=15合流子{14,15}≡{15,14}）。pin行数増加則（奇z 6→7→8・偶z 5→6→7）と「pinスロット=th-1」5族連続が本fitの主眼で、宣言ノートに事前登録した予想がすべてfit levelで一致
- type: extends
  target: K1143
  note: y=11族の奇数y型比較対象（th=2k+1ペア反復型・x偶行のtail・pin行数(y±1)/2系列の基点）
- type: depends_on
  target: K1234
  note: y=14全称part1系列（K1234 part1+K1233 part2 昇格）の次族として本項の全称part1を組立（verify_y15_universal.py・母体はy=14 part2正本 6ac219cf…・単一オーナー宣言 c34a19ff・clip窓2y+2=32は11族連続tightと確定）
- type: depends_on
  target: K1236
  note: 全称証明part1（正本検証器12チェック・overall PASS 6,349,309点・3回byte-identical）とpart2（本項昇格段階・同一単一オーナー宣言 c34a19ff 配下の工程記録）
- type: generalizes
  target: K0999
  note: z=8・y>=9一様全Grundy分類のy=15行は本項の特殊例（転写アンカーA8uとしてC1d照合）
- type: generalizes
  target: K1000
  note: z=8・y>=9一様全Grundy分類（K0999の証明範囲）のy=15行は本項の特殊例
- type: generalizes
  target: K1001
  note: z=9・y>=9一様全Grundy分類のy=15行は本項の特殊例（転写アンカーA9uとして照合）
- type: generalizes
  target: K1011
  note: z=10・y>=9一様全Grundy分類のy=15行は本項の特殊例（転写アンカーA10uとして照合）
- type: generalizes
  target: K1065
  note: z=15・y>=6族のy=15行は本項の特殊例（published closed formを転写アンカーA15uとして照合）
- type: generalizes
  target: K1077
  note: z=16・y>=6族のy=15行は特殊例（転写アンカーA16uとして照合）
- type: generalizes
  target: K1087
  note: z=17・y>=6族のy=15行は特殊例（転写アンカーA17uとして照合）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/README.md
  role: proof
  note: 正本監査段階の実験記録（機械構成・転写照合・part1 12チェック+part2 C1d/C11r 14チェック結果表・bounded-memoization twin設計・3回決定性・fail-closed 5件・再現コマンド・observed→proved昇格判定・CI step不登録の理由・解釈規約）
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/verify_y15_universal.py
  role: verifier
  note: 正本検証器（part2正本・SHA-256 a39e7ab1…・51,491 bytes・1,313行・純stdlib・seed固定・sorted keys・14チェック構成。part1出版正本はcommit 45f3ccfd系の583252cc…・37,381 bytes・942行・12チェック）
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/scripts/preflight_c1d_y15.py
  role: verifier
  note: C1dアンカー組み込み前のfail-closed事前検証（anchor×H_ordered×H_canonical×cand15の4方照合13,485点＋低R縮約9,570点・不一致0・z別2,108/2,139/2,170/2,325/2,356/2,387・2回byte-identical）
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/census_rows.py
  role: verifier
  note: z=0..79・x=15..70・R=0..x+z+16の生tuple二重再帰census第三実装（4,480行448,000点・値0点223,127・状態計算misses 7,666,827・LRU上限1.6M明示キャップ・約16秒・maxrss 639,524KB）
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/output/audit.json
  role: data
  note: part2フル14チェック監査正本（3,675 bytes・SHA-256 401be383…・total_points 6,935,639・total_bad 0・型335,658・3実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/output/census.txt
  role: data
  note: census行表正本（824,466 bytes・4,480行＋空行80・SHA-256 1465a011…・C11rでcand15から再導出して全行照合・不一致0・tailアサート全行成立）
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/output/preflight-c1d-y15.json
  role: data
  note: 事前検証結果正本（13,485+9,570点・不一致0・SHA-256 cd67d3fe…）
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/output/published_run.txt
  role: log
  note: 実行記録（part1: builder組立・smoke spot 6種・run1-3 transcript・fail-closed 3種・環境。part2: preflight・census・14チェックrun1-3・fail-closed 5種・出版ファイルSHA一覧）
- path: research/log/2026-11-22-y15-universal-verifier-part1.md
  role: log
  note: part1（12チェック6,349,309点全PASS・3回byte-identical・昇格はpart2まで行わない）
- path: research/log/2026-11-22-y15-parametric-allz-proof-part2.md
  role: log
  note: part2（C1d事前検証・census第三実装・14チェック監査・3回byte-identical・K1235 observed→proved昇格・出版記録）
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-fit-20261122/report.md
  role: proof
  note: fit段階の正本記録（74,865 probe点一発一致・box内tail assertion 15,810点・box外spot 39,215点（全8奇z pin行・全7偶z pin行を個別検証・x>=15機械guardつき）・merge回帰14,325比較・tail raw 84点・事前予想の判定表・y=6..15族表記述・fail-closed 5種と誠実記録）
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-fit-20261122/cand15.py
  role: verifier
  note: 閉形式の正本cand15（in_T15値2表・in_P15値1表・Y=15・SHA-256 f61997dd…）とprobe全点照合（74,865点・mismatch 0・overlap 0・初稿一発一致）。次段階の正本検証器は本ファイルを逐語転写する
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-fit-20261122/probe_y15.py
  role: verifier
  note: 生二重再帰probe（z=0..30・x=15..z+29・R<=x+z+32〔=2y+2・y=14出版convention継承〕・930行・74,865点・約5.9秒・同一cwd/別cwd/隔離の3回再生成でbyte-identical・probe_rows.txt SHA-256 2c7b72ad…）
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-fit-20261122/spot_y15.py
  role: verifier
  note: box外spot 39,215点bad 0＋merge回帰14,325比較0＋tail raw回帰84点0（約121秒・LRU cap 1.5M決定的退避・**全選択行にx>=15機械assert**でy=14のspot事故の再発を構造的に排除・マージ境界行(31,15)/(32,16)はbox内マージ行0行の事前宣言に対する生値補完）
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-fit-20261122/make_audit_y15.py
  role: verifier
  note: 決定的audit生成器（fail-closed: mismatch/overlap/tail_bad/偶z対角値1/奇z8行・偶z7行pin格子観測不完全ならauditを書かない・3回実行byte-identical〔同一cwd2回+隔離tree/cwd/HOME+PYTHONHASHSEED=random〕）
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-fit-20261122/output/audit.json
  role: data
  note: fit監査正本（自己文書化・probe/spot/merge/tail数値・sha256ピン・事前宣言commit 26a1ad28記録・box内マージ行0行の事前宣言を明記・SHA-256 5c329dd4…）
- path: research/log/2026-11-22-y15-two-token-skeleton-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-22T20:04:00Z・commit 26a1ad28・probe実行前に出版・事前横断予想12項目の全記録を含む・対抗宣言チェック・box内マージ行0行の事前明記）
- path: research/log/2026-11-22-two-token-y15-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・経緯・誠実記録〔env -i PATH・stale pyc〕・出版記録・次段階）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,15)、全z>=0・全x>=15・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand15）で
  分類する命題の全称証明（status proved・2026-11-22 part2出版でobserved→
  provedに昇格・正本検証器14チェック体制・型機械・census・C1d published
  アンカー・単一オーナー宣言 c34a19ff 配下のpart1+part2）。系として
  x<=z-16（S=x+15<z-1）の全R行が単一トークン値single_token(x+15,z,R)に一致する
  マージ命題のy=15版とtail R>=x+z+16=(x+z+y+1)の(x+15) mod 2を含む
  （マージ命題はy=1..15で全称確定）。標準11×11の空盤・二石root・S2 {59,60}・
  class 1/2/4は範囲外かつUNKNOWNのまま。3トークン以上・y>=16族・固定幅・
  q点版も範囲外。
evidence: >-
  証明はK1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138/K1141/K1152/K1231/K1233と
  同型の3部構成で、fit段階（128,489点の有限観察・初稿一発一致）に正本監査part1
  （12チェック・commit 45f3ccfd/e8559457/8519ba7e系）とpart2（C1d+census・本出版）が
  続きobserved→provedに昇格した。
  (1) 選択肢分解: A子=cand15(z,x-1,R-1)（x=15は合流子(14,15)≡(15,14)で
  cand14(z,15,R-1)）・B子=出版cand14（K1233全称のy=14族をブロック内Y→Y14改名
  〔24箇所count-assert〕のみで逐語転写）・C子=1 xor cand15(z-1,x,R-1)。分解が
  素再帰の選択肢値集合と一致することをraw二重再帰で錨止めする（C3・1,215点・
  両生エンジンC1 22,515点・単一トークン/B子/x=15合流子C1b 43,228点）。
  (2) 恒等式: 閉形式格子C2 218,834点・深tail行C2b 19,228点・深格子C12 1,853,357点・
  seeded遠方probe C7 200,000点（seed 20261152・z,x<=3000）・境界多様体C8 993,180点
  （dx∈[-30,17]・tail窓 [x+z+16,x+z+18]）・vシェルC9 908,202点・生censusアンカー
  C11 887,040点（両エンジン・bounded-memoization twin・part merge fail-closed）。
  (3) 型機械: clip窓2y+2=32・番兵33で335,658型の(value, sorted子)完全収束
  （C4 601,255点・C4時点279,619型・confluence_bad 0）。C4t tightness probeで
  clip 31（2y+1）は2,030点の収束違反（最初(60,94,94)）がありclip 2y+2=32がtight・
  2y+2 clip tightは11族連続（y=5..15: 12/14/16/18/20/22/24/26/28/30/32）。merge
  corollary x<=z-16→single_token(x+15,z,R) 1,304,870点（y=15ではfit probe box
  z=0..30にマージ行が存在しないため本機が初の全域raw anchor）・tail corollary
  R>=x+z+16→(x+15) mod 2 195,917点・それぞれ不一致0。part2(C1d): published
  uniform closed form 6切片（K0999/K1000・K1001・K1011・K1065・K1077・K1087）の
  アンカーA8u..A17uをy=14 part2正本検証器からverbatim抽出し、組み込み前に出版
  アンカー×H_ordered×H_canonical×cand15の4方照合（13,485点+低R縮約9,570点）で
  事前検証してから組み込み、x=15..159・R<=x+61・R<=z+6の138,330点でy=15行vs
  cand15を照合・不一致0。part2(C11r): census_rows.py第三実装（z=0..79・x=15..70・
  R=0..x+z+16・4,480行448,000点・値0点223,127・LRU上限1.6M明示キャップ）の行ごとの
  Thue-Morse指数・T/P集合・tailをcand15から再導出して全行照合・不一致0・
  fail-closed。監査計6,935,639照合点・全チェック不一致0・同一cwd 2回+
  隔離tree/cwd/HOME+PYTHONHASHSEED=random（census・preflight・両census partの
  再生成を含む）1回の3実行でaudit.jsonとcensus.txtがbyte-identical
  （SHA-256 audit 401be383…・census.txt 1465a011…）。census part改ざん・merge
  corollary改ざん・part欠落・census.txt改ざん（P集合1桁）・census.txt欠落の5種
  fail-closed検査を出版前に実施し全て捕捉。fit段階の誠実記録（y=14 fit のspot
  事故知見を踏まえた全spot行のx>=15機械assertなど）はfit実験dirが正本。
  有限監査は転写・実装照合であり、全称性は選択肢分解の健全性・正確なmex恒等式・
  有限型空間の完全性（K1023→K1234 と同一trust境界）による。
---

## 命題・範囲

すべての z>=0・x>=15・R>=0 に対して H(R;(x,15);z) = cand15(z,x,R) が成り立つ
（**status: proved・2026-11-22 part2出版でobserved→provedに昇格**）。正本は
[実験dir](../../experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/README.md)
で、verify_y15_universal.py（part2正本 SHA-256 a39e7ab1…）が正本検証器、
cand15.py が閉形式の正本実装である。全称監査は part1（12チェック・
[part1 log](../log/2026-11-22-y15-universal-verifier-part1.md)）と part2
（C1d出版切片アンカー+census第三実装・
[part2 log](../log/2026-11-22-y15-parametric-allz-proof-part2.md)）の2段階で、
14チェック総6,935,639照合点・全bad 0・3実行byte-identical。
part1 の機械構成は B子=出版cand14逐語転写〔x=15合流子{14,15}≡{15,14}〕・
A子合流の正準順序注意〔y=14 fit の spot 事故の実証済み再発防止策として本fitは
全spot行に x>=15 機械assertを組み込み済み〕・型機械 clip窓 2y+2=32。

y=15 は奇数 y 族（y=9/11/13 と同型）で、値1無限帯・tail 値1 は x 偶の行。
主要構造はラダー（奇z 奇R O[1,z]／偶z 奇R O[1,z-1]）・マージ行 x<=z-16 の
O[1, q_odd(x+15)]（y=15ではprobe box内マージ行0行・事前宣言どおり）・対角行
d=-15 の cap=z+15-[z≡15 (mod 2)]即ち奇z 偶offset [2,14]／偶z 奇offset [1,15]
（奇y族向き）・pin格子（統一式 pin=z+(d+45)/2・o_pin∈[16,30]・o_pin≡z+1
(mod 2)・奇z d≡3 (mod 4) {-13,-9,-5,-1,3,7,11,15} の**8行**〔y奇族式
(y+1)/2 が 6→7→8 で到達した初の8行族〕・偶z d≡1 (mod 4) {-11,-7,-3,1,5,9,13}
の7行〔(y-1)/2 が 5→6→7〕・最終pin行 d=15=y が初めて奇z pin 上端の I 行
（I[2y+z+1)=I[31) 型・pin z+30 は直後の定常 pin と同値））・奇z I帯行（d 奇
16 行・対角込）k(d)=floor((d+46)/4)=floor((d+3y+1)/4)（base行と同一族式・
3族目）・th=2k+1（ペア反復型・y 偶族掃引型との偶奇分離）・pin行で pin が
off=2k=th-1 をちょうど占有（「pinスロット=th-1」5族連続・8行すべてで
th(d)-1=o_pin(d) が算術的に恰好）・base行 k=floor((d+46)/4)（6族目）・偶z
I帯行 k(d)=floor((d+44)/4)=floor((d+3y-1)/4)（5族目・th=2k+1）・偶z pin は
base行（奇d）の 2k+1 位置（7行すべてで 2k(d)+1=o_pin(d)）・掃引行 d=16 の帯
（奇z 偶offset [z+30, x+z+15]／偶z 奇offset [z+31, x+z+15]）・定常行 d>=17 の
定常pin z+30（奇z）／z+31（偶z）・基底点15点 {z+1,...,z+29}・band下端
2y+2=32・tail開始 x+z+16・tail値 (x+15) mod 2・偶z対角行の値1全欠如
（8族連続で確定・y=8..15）。

## fitの工芸的観察

**初稿一発一致（修正0）**: cand15 初稿は y=13 の出版最終構造（cand13・K1231
全称昇格済み）を seed とした Y+2 外挿で、probe 74,865 点に一致するまで修正を
要さなかった。「直前の出版最終構造 seed による外挿が一発一致する」が
奇数 y 2 連続（cand11→cand13・cand13→cand15）・偶数 y 1 回（cand12→cand14）の
3 連続となり、y>=16 への族構造則一般化（横断法則の一般補題化レーン）の主要
リスク（族式の y 依存跳躍）がさらに低減した。修正を要しやすい領域（y=12 の
修正 echo: z 偶数行の k 定数・I 帯開始、z 奇数 pin 衝突）は本 fit ではすべて
初期構造のままで一致した。

## 全称昇格の根拠

(i) fit段階: probe box 930行・74,865点の生二重再帰との全点一致（初稿一発一致）＋
box外spot 39,215点（x>=15機械assertつき）＋merge/tail回帰の計128,489点比較・
不一致0。
(ii) part1正本監査12チェック 6,349,309点・全bad 0（生両エンジン錨・
B子=x=15合流子錨・K0832単一トークン/B子/x=15合流子C1b・恒等式格子・型機械
〔clip 2y+2=32 tight・11族連続・y奇族初の8 pin行族〕・seeded遠方probe・境界
多様体・vシェル・bounded-memoization twinの生censusアンカー・深格子）・
3実行byte-identical。
(iii) part2: C1d 138,330点（published 6切片のy=15行アンカー・組み込み前
4方事前検証13,485+9,570点つき）・C11r 448,000点（census_rows.py第三実装の
全行をcand15から再導出照合・不一致0）・フル14チェック監査 6,935,639点・
全bad 0・3実行byte-identical（同一cwd 2回＋隔離tree/cwd/HOME+
PYTHONHASHSEED=random・隔離側でpreflight・census・両census partを再生成）・
fail-closed検査5種捕捉。
マージ命題の y=15 版（x<=z-16 → single_token(x+15,z,R)）と tail 値 (x+15) mod 2 は
全称系として昇格（corollary照合 1,304,870/195,917点・それぞれ不一致0）。
**マージ命題は y=1..15 で全称確定**（2トークン族の全称は y=1..15 が揃った）。
有限監査は転写・実装照合であり、全称性は選択肢分解の健全性・正確なmex
恒等式・有限型空間の完全性（K1023→K1234 と同一trust境界）による。
3トークン以上・y>=16族・固定幅・q点版安定化長・標準11×11の勝敗は範囲外。
標準 11×11 空盤・二石 root・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。

## 横断観察（y=15 は全称確定後の観察）

- tail 開始族式 x+z+y+1 が **15 族連続**（y=1..15 全称確定）。
- 基底点 y 点仮説 {z+1,..,z+2y-1} が 15 例目。
- pin 統一式 pin=z+(d+3y)/2 が 11 族目。y 奇族 pin 行数 (y+1)/2〔奇z〕/
  (y-1)/2〔偶z〕が y=11/13/15 の 3 点で増加則として確定（初の 8 行族）。
- 「pin スロット=th-1」が y=11..15 の **5 族連続**（y<=14 全称確定・y=15 も本昇格で
  全称確定）。偶z の 2k+1 slot 則も 5 族連続。
- base 行 k(d)=floor((d+3y+1)/4) が y=10..15 **6 族連続**。偶z I 帯行
  k(d)=floor((d+3y-1)/4) が y=11..15 **5 族連続**。
- th 連続整数掃引〔偶y〕と 2k+1 ペア反復〔奇y〕の偶奇分離が明白（y=12/14
  掃引・y=11/13/15 反復）。
- 偶z 対角行の値1全欠如が **8 族連続で確定**（y=8..15）。最終 pin 行 d=y の
  I[2y+z+1) 型が **10 族目**（y=15 で初めて奇z pin 上端が d=y）。
- band 下端 2y+2 と clip 窓 2y+2 が y=15 で 32・**clip tight が 11 族連続で確定**
  （y=5..15: 12/14/16/18/20/22/24/26/28/30/32・最初違反がband下端とともに歩く
  (60,90,90)/(60,92,92)/(60,94,94) の3点観測）。
- B子逐語転写構成が cand9..cand14 の **6 連**（全称証明済み族を B 子に使うのは
  cand10/cand12/cand13/cand14 の 4 例）。
- 初稿一発一致が 3 連続（11→13・12→14・13→15）。y=12 の 240 点修正は
  暫定構造 seed・修正後の出版最終構造は以後の族で全て修正不要。
