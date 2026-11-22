---
id: K1231
title: "2トークン残余ゲーム y=13族のパラメトリック閉形式の全称証明（全z>=0・全x>=13・全R>=0）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "two-token y=13 parametric all-z universal proof, P13"
  - "cand13 fitting and box-out spot verification (fitting stage, pre-promotion; first-draft agreement on all 72,664 probe points, zero corrections)"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・Theorem T・単一トークン閉形式のraw anchor（C1b・merge corollary x<=z-14→single_token(x+13,z,R)）に使用する
- type: depends_on
  target: K1143
  note: cand13初稿をy=11族表cand11（y=13と同じy奇型）の族法則Y+2外挿で生成した（初稿はprobe 72,664点に一発一致・y=12の240点修正と対照的）。B子の逐語転写元ではない（B子は出版cand12）
- type: extends
  target: K1152
  note: y=12族全称閉形式（K1152）のy=13版。B子=出版cand12（検証器にy=12正本機械のcand12ブロックをブロック内Y→Y12改名のみで逐語転写・x=13合流子(12,13)≡(13,12)も同一）。全称証明済み族（K1152）をB子に逐語転写するのは3例目
- type: depends_on
  target: "K1232"
  note: "全称証明part1（正本検証器12チェック・overall PASS 6,353,143点・3回byte-identical）とpart2（本項昇格段階・同一単一オーナー宣言配下の工程記録）"
- type: generalizes
  target: K0999
  note: z=8・y>=9一様全Grundy分類のy=13行は本項の特殊例（転写アンカーA8uとしてC1d照合）
- type: generalizes
  target: K1000
  note: z=8・y>=9一様全Grundy分類（K0999の証明範囲）のy=13行は本項の特殊例
- type: generalizes
  target: K1001
  note: z=9・y>=9一様全Grundy分類のy=13行は本項の特殊例（転写アンカーA9uとして照合）
- type: generalizes
  target: K1011
  note: z=10・y>=9一様全Grundy分類のy=13行は本項の特殊例（転写アンカーA10uとして照合）
- type: generalizes
  target: K1065
  note: z=15・y>=6族のy=13行は本項の特殊例（published closed formを転写アンカーA15uとして照合）
- type: generalizes
  target: K1077
  note: z=16・y>=6族のy=13行は特殊例（転写アンカーA16uとして照合）
- type: generalizes
  target: K1087
  note: z=17・y>=6族のy=13行は特殊例（転写アンカーA17uとして照合）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/README.md
  role: proof
  note: 正本監査段階の実験記録（機械構成・転写照合・part1 12チェック+part2 C1d/C11r 14チェック結果表・bounded-memoization twin設計・3回決定性・fail-closed 5件・再現コマンド・observed→proved昇格判定・CI step不登録の理由）
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/verify_y13_universal.py
  role: verifier
  note: 正本検証器（part2正本・SHA-256 079b49ad…50,865 bytes・1,314行・純stdlib・seed固定・sorted keys・14チェック構成。part1出版正本はcommit ee3b6f73のb73d9aaa…36,457 bytes・12チェック）
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/scripts/preflight_c1d_y13.py
  role: verifier
  note: C1dアンカー組み込み前のfail-closed事前検証（anchor×H_ordered×H_canonical×cand13の4方照合14,157点＋低R縮約9,702点・不一致0・2回byte-identical）
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/census_rows.py
  role: verifier
  note: z=0..79・x=13..70・R=0..x+z+15の生tuple二重再帰census第三実装（4,640行450,080点・値0点224,203・状態計算misses 6,630,827・LRU上限1.6M明示キャップ・約15秒・maxrss約557MB）
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/output/audit.json
  role: data
  note: part2フル14チェック監査正本（3,673 bytes・SHA-256 2f5f56c0…・total_points 6,942,579・total_bad 0・3実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/output/census.txt
  role: data
  note: census行表正本（4,640行＋空行80・829,622 bytes・SHA-256 505f05bf…・C11rでcand13から再導出して全行照合・不一致0）
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/output/preflight-c1d-y13.json
  role: data
  note: 事前検証結果正本（14,157+9,702点・不一致0・SHA-256 a9307d33…）
- path: research/log/2026-11-22-y13-parametric-allz-proof-part1.md
  role: log
  note: part1（12チェック6,353,143点全PASS・3回byte-identical・昇格はpart2まで行わない）
- path: research/log/2026-11-22-y13-parametric-allz-proof-part2.md
  role: log
  note: part2（C1d事前検証・census第三実装・14チェック監査・3回byte-identical・K1231 observed→proved昇格・出版記録）
- path: research/log/2026-11-22-y13-universal-verifier-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-22T17:59:40Z・commit 7196cbd5・part1+part2保持・K1231 fitレーン宣言〔d3404db8〕と矛盾なし）
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261122/report.md
  role: data
  note: cand13のz偶奇別T/P集合表全文（S=x+13偶奇のy奇型・奇z 7行/偶z 6行のpin格子・偶z対角行の値1全欠如6族連続・最終pin行d=yのI[2y+z+1)型7族連続候補・band下端2y+2=28・pin格子統一式o_pin=(d+3y)/2の横断再現）とfitting段階の検証規模の記録
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261122/cand13.py
  role: verifier
  note: 閉形式の正本cand13（in_T13値2表・in_P13値1表・Y=13）とprobe全点照合（72,664点・mismatch 0・初稿一発一致）。正本検証器は本ファイルを逐語転写する
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261122/probe_y13.py
  role: verifier
  note: 生二重再帰probe（z=0..30・x=13..z+29・R<=x+z+26・992行・72,664点・約5.1秒）
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261122/spot_y13.py
  role: verifier
  note: box外spot 31,750点bad 0＋merge回帰17,277比較不一致0＋tail raw回帰84点0（約22.4秒）
- path: research/log/2026-11-22-two-token-y13-parametric-fit.md
  role: log
  note: fit段階の宣言確認・y=11族表からの外挿初稿一発一致の経緯・出版記録（初出版後の転写スリップ修正コミット76a4f28を含む）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,13)、全z>=0・全x>=13・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand13）で
  完全分類する。K0999/K1000（z=8）・K1001（z=9）・K1011（z=10）の
  y=13行とK1065/K1077/K1087（z=15,16,17のy>=6族）のy=13行は本項の特殊例
  であり、z>=18（z=18,y=13を含む）のy=13行も主張に含まれる（以後のy=13
  スライス出版は不要）。系としてx<=z-14（S=x+13<z-1）の全R行が単一
  トークン値single_token(x+13,z,R)に一致するマージ命題のy=13版が全称に
  昇格する（マージ命題はy=1..13で全称確定）。tail
  R>=x+z+14=(x+z+y+1)の(x+13) mod 2も全称に含む。
evidence: >-
  証明はK1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138/K1141/K1152と同型の
  3部構成で、fit段階（121,775点の有限観察・初稿一発一致）に正本監査part1
  （12チェック・commit ee3b6f73/5014e9d5/c6880c0d）とpart2（C1d+census・本出版）が続き
  observed→provedに昇格した。(1) 選択肢分解: A子=cand13(z,x-1,R-1)
  （x=13は合流子(12,13)≡(13,12)でcand12(z,13,R-1)）・B子=出版cand12
  （先行出版のy=12族全称閉形式をブロック内Y→Y12改名のみで逐語転写）・
  C子=1 xor cand13(z-1,x,R-1)。分解が素再帰の選択肢値集合と一致することをraw二重再帰で
  錨止めする（C3・1,155点・両生エンジンC1 21,945点・単一トークン/B子/x=13合流子
  C1b 42,041点）。(2) 恒等式: 閉形式格子C2 226,527点・深tail行C2b 19,052点・
  深格子C12 1,862,190点・seeded遠方probe C7 200,000点（seed 20261132）・
  境界多様体C8 953,151点（dx∈[-28,17]・B子tail窓アンカー付き）・vシェルC9
  913,194点・生censusアンカーC11 890,880点（両エンジン・bounded-memoization
  twin・part merge fail-closed）。(3) 型機械: clip窓2y+2=28・番兵±29で
  234,180型の(value, sorted子)完全収束（C4 611,504点・confluence_bad 0）。
  C4t tightness probeでclip 27は2,987点の収束違反（最初(60,90,90)）があり
  clip 2y+2=28がtight・2y+2 clip tightは9族連続
  （y=5..13: 12/14/16/18/20/22/24/26/28）。merge corollary
  x<=z-14→single_token(x+13,z,R) 1,391,747点・tail corollary
  R>=x+z+14→(x+13) mod 2 217,342点・それぞれ不一致0。part2(C1d):
  published uniform closed form 6切片（K0999/K1000・K1001・K1011・
  K1065・K1077・K1087）のアンカーA8u..A17uをy=12 part2正本検証器から
  verbatim抽出し、組み込み前に4方照合（14,157点+低R縮約9,702点）
  で事前検証してから組み込み、x=13..159・R<=x+61・R<=z+6の139,356点で
  y=13行vs cand13を照合・不一致0。part2(C11r): census_rows.py第三実装
  （z=0..79・x=13..70・R=0..x+z+15・4,640行450,080点・LRU上限1.6M明示
  キャップ）の行ごとのThue-Morse指数・T/P集合・tailをcand13から再導出
  して全行照合・不一致0・fail-closed。監査計6,942,579照合点・全チェック
  不一致0・同一cwd 2回+隔離tree/cwd/HOME+PYTHONHASHSEED=random（census
  再生成含む）1回の3実行でaudit.jsonとcensus.txtがbyte-identical
  （SHA-256 audit 2f5f56c0…・census.txt 505f05bf…）。census part改ざん・
  corollary改ざん・欠落・census.txt改ざん（P集合1桁）・census.txt欠落の5種
  fail-closed検査を出版前に実施し全て捕捉。有限監査は転写・実装照合であり、
  全称性は選択肢分解の健全性・正確なmex恒等式・有限型空間の完全性
  （K1023→K1152 と同一trust境界）による。
---

## 命題・範囲

すべての z>=0・x>=13・R>=0 に対して H(R;(x,13);z) = cand13(z,x,R) が成り立つ
（status: proved・2026-11-22 part2出版でobserved→provedに昇格）。正本は
[実験dir](../../experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/README.md)
で、verify_y13_universal.py（part2正本 SHA-256 079b49ad…）が正本検証器、
cand13.py が閉形式の正本実装である。全称監査は part1（12チェック・
[part1 log](../log/2026-11-22-y13-parametric-allz-proof-part1.md)）と part2
（C1d出版切片アンカー+census第三実装・
[part2 log](../log/2026-11-22-y13-parametric-allz-proof-part2.md)）の2段階で、
14チェック総6,942,579照合点・全bad 0・3実行byte-identical。

y=13 は y 奇族（y=9/y=11 と同型）で、値1無限帯・tail は x 偶の行。構造は
y=11（K1143）の Y+2 平行移動が概ねそのまま成立する。主要構造は
ladder（奇z 奇R O[1,z]／偶z 奇R O[1,z-1]）・マージ行 x<=z-14 の
O[1, q_odd(x+13)]・対角行 d=-13 の cap=z+13-[z≡1]（奇z 偶offset [2,z+12]／
偶z 奇offset [1,z+13]）・pin格子（統一式 pin=z+o_pin・o_pin=(d+3y)/2∈[14,26]・
o_pin≡z+1 (mod 2)・奇z 偶o_pin で d∈{-11,-7,-3,1,5,9,13} の7行〔y奇族初の7行〕・
偶z 奇o_pin で d∈{-9,-5,-1,3,7,11} の6行〔y奇族の偶z pin 行数 (y-1)/2 が y=11 の
5行から6行に増えた初例〕）・掃引行 d=14 の帯 O[2y+z, x+z+y]（奇z 偶offset）／
O[2y+z+1, x+z+y]（偶z 奇offset）・定常行 d>=15 の定常pin z+26（奇z）／z+27（偶z）・
基底点 13 点 {z+1,...,z+25}・band下端 2y+2=28・tail開始 x+z+y+1=x+z+14・
マージ境界 x<=z-(y+1)=z-14・最終pin行 d=y の I[2y+z+1) 型・偶z対角行の値1全欠如
（y=8..13 に続き6族連続で全称確定）。奇z の全行の base rank は
k(d)=floor((d+40)/4)=floor((d+3y+1)/4) の単一式で統一され（th=2k+1・y=11 と
同一族式）、偶z は base 行が同一式・I 帯行が k(d)=floor((d+38)/4)=floor((d+3y-1)/4)
の別式（y=11/12 と同一族式）。y=13 特有の工芸的観察は cand13 初稿が y=11 族表の
Y+2 外挿で probe 72,664 点に一発一致したこと（y=12 は 240 点修正を要したのと対照的）。

## 全称昇格の根拠

(i) fit段階: probe box 992 行・72,664 点の生二重再帰との全点一致（初稿一発一致）
＋box外spot 31,750点＋merge/tail回帰の計121,775点比較・不一致0。
(ii) part1正本監査12チェック 6,353,143 点・全bad 0（生両エンジン錨・
B子=x=13合流子錨・恒等式格子・型機械〔clip 2y+2=28 tight・9族連続〕・
遠方probe・境界多様体・vシェル・bounded-memoization twinの生census
アンカー・深格子）・3実行byte-identical。
(iii) part2: C1d 139,356点（published 6切片のy=13行アンカー・組み込み前
4方事前検証つき）・C11r 450,080点（census_rows.py第三実装の全行を
cand13から再導出照合）・フル14チェック監査 6,942,579点・全bad 0・
3実行byte-identical・fail-closed検査5種捕捉。
マージ命題の y=13 版（x<=z-14）と tail 値 (x+13) mod 2 は全称系として昇格
（corollary照合 1,391,747/217,342点・それぞれ不一致0）。
有限監査は転写・実装照合であり、全称性は選択肢分解の健全性・正確なmex
恒等式・有限型空間の完全性（K1023→K1152 と同一trust境界）による。
3 トークン以上・y>=14 族・固定幅・q 点版安定化長・標準 11×11 の勝敗は範囲外。
REFUTED-D10 型の実験とは異なり LOSS 証明を含まない。

## 横断観察（y=1..13・y=13 は全称確定）

- tail 開始族式 x+z+y+1 が y=2..13 の 12 族連続（y=13 は全称確定）。
  tail 値 (x+y) mod 2・値1無限帯と tail の x 偶奇が y 偶奇で決まり
  y 奇族（y=9/11/13）は x 偶の行。
- 基底点 y 点仮説 {z+1,..,z+2y-1} が 13 例目（y=1..13・y=13 は全称確定）。
- pin 統一式 pin=z+(d+3y)/2〔d≡y (mod 4)（奇z）・d≡y+2 (mod 4)（偶z）〕が
  y=5..13 の **9 族連続**（y=13 は全称確定）。y=13 の pin 行 d 範囲は
  奇z {-11,-7,-3,1,5,9,13} の7行・偶z {-9,-5,-1,3,7,11} の6行（y 奇族の偶z pin
  行数 (y-1)/2 が 6 行に増えた初例が全称確定。y 奇族では pin 行 d が奇数）。
- 「pin スロット=th-1」型（奇z pin 行で pin が off=2k=th-1 をちょうど占有）が
  y=11/y=12/y=13 の **3 族連続で全称確定**（K1152 が指名した横断型の問いに全称で
  回答）。偶z側は pin が base 行上端 2k-1 の +2 位置（2k+1）に載る slot 則が
  3 族で同一。
- base 行の base rank が k(d)=floor((d+3y+1)/4) で y=10/11/12/13 の全 base 行
  （z 偶奇・行型反転込み）で同一。偶z I 帯行 k(d)=floor((d+3y-1)/4) が
  y=11/12/13 の 3 族で同一。奇 z th 則 2k+1 が奇 y 族 3 例目
  （y 偶奇が th 則を決める観察が全称側でも維持）。
- 対角行上端格子規則 cap=z+y-[z≡y (mod 2)] が y=13 で全称確定
  （C1d相当のpublished切片と全チェックの全zで一致）。
- clip 窓族式候補 2y+2 が **9 族連続 tight**（y=5..13: 12/14/16/18/20/22/24/26/28・
  y=13 は C4t clip 27 の 2,987 違反で tight 確定）。
- 偶 z 対角行の値1全欠如が **6 族連続で全称確定**（y=8..13）。最終 pin 行
  d=y の I[2y+z+1) 型が 8 族的確定（y=6/8/9/10/11/12/13・y=13 は全称確定）。
- B 子に先行出版族の閉形式を逐語転写する構成: cand9（y=10 の B 子）・
  cand10（y=11 の B 子・K1141 全称）・cand11（y=12 の B 子・K1143）・
  cand12（y=13 の B 子・K1152 全称）で 4 連（全称証明済み族を B 子に使うのは
  cand10・cand12）。
- 初稿一発一致が y=11 に続き 2 例目（y=12 は 240 点修正・y=10 は手順外）。
  奇数 y 族のテンプレート外挿が過剰修正なく Y+2 に伸びるという工芸的観察が
  全称確定を経て証拠の裏付けを得た。
