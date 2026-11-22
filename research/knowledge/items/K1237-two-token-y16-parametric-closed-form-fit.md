---
id: K1237
title: "2トークン残余ゲーム y=16族のパラメトリック閉形式の全称証明（全z>=0・全x>=16・全R>=0）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "two-token y=16 parametric closed-form fit, P16-fit"
  - "cand16 fitting and out-of-box spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 74,741 probe points; even-y template mechanical translation from the published FINAL cand14, the promoted-universal y=14 table with Y=14->16)"
  - "seed law 4th consecutive one-shot test passed (cand11->13 / cand12->14 / cand13->15 / cand14->16); first 17-row th-consecutive-integer sweep (17..33); first both-parity 8-row pin lattice (y/2 count law 4th data point y=10:5/12:6/14:7/16:8); first even-y family with merge rows entirely out-of-box (zero in-box merge rows)"
  - "universal proof completed (2026-11-22, part1+part2 under single-owner declaration 432664f7): observed -> proved via the 14-check canonical audit at 6,916,256 comparison points bad 0, C1d published-slice anchors preflighted 4-way (13,140+9,504 pts), census_rows.py third implementation consumed by C11r (446,600 pts); clip window 2y+2=34 tight, 12-family streak y=5..16; merge proposition now universal through y=1..16"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（box 外マージ回帰14,910比較・境界行spot照合に使用・y=16ではbox内マージ行0行のため全称段階のマージ系x<=z-17が初の全域生エンジン錨止め）
- type: extends
  target: K1233
  note: y=14族全称閉形式（K1233・昇格済み）の次の偶数y族。cand16初稿はy=14出版最終構造cand14（全称証明済み）のY+2機械翻訳で生成し、probe 74,741点に一発一致（cand12→cand14に続き偶数y seed法則2連続目・全体で4連続一発一致）。コード本体はY定数・関数名・y固有コメント以外は正本cand14と同一構造（Y正規化差分比較で確認）
- type: extends
  target: K1235
  note: y=15族全称閉形式（K1235・昇格済み）の次族。全称段階のB子は出版cand15の逐語転写（x=16合流子{15,16}≡{16,15}）で、B子逐語連鎖cand9..cand15（7リンク）うち証明済みB子はcand10/cand12..cand15（5リンク）。y=15のband_base/band_int分離（奇y族）とy=16の単一band則（偶y族）の対照がy=16 fitで再確認
- type: extends
  target: K1152
  note: y=12族全称閉形式（偶数y族式系列の基点）。z-odd I帯k=floor((d+3y+2)/4)・th連続整数掃引・偶z I帯k=floor((d+3y-1)/4)の偶数y族式がy=12→14→16で3族連続成立
- type: extends
  target: K1141
  note: y=10族（偶数y行型の基点・x奇行のtail・値1無限帯）。y=16も同じ行型反転（y偶=tail x奇行）で一致
- type: depends_on
  target: K1236
  note: y=15全称part2（系列上の直前工程）で確定した「横断法則y>=15一般補題化レーン」に本全称は偶数y系列第4データ点（y=10/12/14/16）を供給（pin行数y/2・pin mod-4回転・17行掃引・単一band則）。clip窓2y+2 tight判定は本検証器のC4tで12族連続（y=5..16）に伸長
- type: depends_on
  target: K1239
  note: 全称証明part1（正本検証器12チェック・overall PASS 6,331,848点・3回byte-identical・出版実験dirの組立・監査・fail-closed）とpart2（本項昇格段階・C1d事前検証+census第三実装C11r・同一単一オーナー宣言 432664f7 配下の工程記録）
- type: generalizes
  target: K0999
  note: z=8・y>=9一様全Grundy分類のy=16行は本項の特殊例（転写アンカーA8uとしてC1d照合）
- type: generalizes
  target: K1000
  note: z=8・y>=9一様全Grundy分類（K0999の証明範囲）のy=16行は本項の特殊例
- type: generalizes
  target: K1001
  note: z=9・y>=9一様全Grundy分類のy=16行は本項の特殊例（転写アンカーA9uとして照合）
- type: generalizes
  target: K1011
  note: z=10・y>=9一様全Grundy分類のy=16行は本項の特殊例（転写アンカーA10uとして照合）
- type: generalizes
  target: K1065
  note: z=15・y>=6族のy=16行は本項の特殊例（published closed formを転写アンカーA15uとして照合）
- type: generalizes
  target: K1077
  note: z=16・y>=6族のy=16行は特殊例（転写アンカーA16uとして照合）
- type: generalizes
  target: K1087
  note: z=17・y>=6族のy=16行は特殊例（転写アンカーA17uとして照合）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/README.md
  role: proof
  note: 正本監査段階の実験記録（機械構成・転写照合・part1 12チェック+part2 C1d/C11r 14チェック結果表・bounded-memoization twin設計・3回決定性・fail-closed part1 5種+part2 6種・誠実事故記録〔builder末尾リテラル→census bad 147,972検出→出版前修正〕・再現コマンド・observed→proved昇格判定・解釈規約）
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/verify_y16_universal.py
  role: verifier
  note: 正本検証器（part2正本・SHA-256 bdf4fe04…・51,691 bytes・純stdlib・seed固定・sorted keys・14チェック構成。part1出版正本はcommit 23e1c22e/432664f7系の検証器SHA 79e21b2d…・37,042 bytes・12チェック・part2はpart1 byteのin-place拡張〔y=13/y=14/y=15 part2手続き〕で12 part1チェック本体はbyte不変）
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/scripts/preflight_c1d_y16.py
  role: verifier
  note: C1dアンカー組み込み前のfail-closed事前検証（anchor×H_ordered×H_canonical×cand16の4方照合13,140点＋低R縮約9,504点・不一致0・z別2,055/2,085/2,115/2,265/2,295/2,325・2回byte-identical〔1回は隔離側〕）
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/census_rows.py
  role: verifier
  note: z=0..79・x=16..70・R=0..x+z+18の生tuple二重再帰census第三実装（4,400行446,600点・値0点223,295・状態計算misses 8,193,227・LRU上限1.6M明示キャップ〔メモリ上限host適応〕・約20秒）
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/output/audit.json
  role: data
  note: part2フル14チェック監査正本（SHA-256 9748ff5c…・total_points 6,916,256・total_bad 0・型394,686・3実行byte-identical。part1 12チェック正本はSHA 7b5acc8c…）
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/output/census.txt
  role: data
  note: census行表正本（817,944 bytes・4,400行＋空行80・SHA-256 f0b1a960…・C11rでcand16から再導出して全行照合・不一致0・tailアサート全行成立）
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/output/preflight-c1d-y16.json
  role: data
  note: 事前検証結果正本（13,140+9,504点・不一致0・SHA-256 efb24340…）
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/output/published_run.txt
  role: log
  note: 実行記録（part1: builder組立・run1-3 transcript・fail-closed 5種〔T5a/T5b含む〕・誠実事故記録。part2: preflight・census・14チェックrun1-3・fail-closed 6種・出版ファイルSHA一覧）
- path: research/log/2026-11-22-y16-universal-verifier-part1.md
  role: log
  note: part1（12チェック6,331,848点全PASS・3回byte-identical・昇格はpart2まで行わない）
- path: research/log/2026-11-22-y16-universal-verifier-part2.md
  role: log
  note: part2（C1d事前検証・census第三実装・14チェック監査6,916,256点・3回byte-identical・K1237 observed→proved昇格・出版記録）
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-fit-20261122/report.md
  role: proof
  note: fit段階の正本記録（74,741 probe点一発一致・box内tail assertion 16,182点・box外spot 35,825点（全spot行にx>=16機械assert）・merge回帰14,910比較・tail raw 84点・事前予想の判定表・y=6..16族表記述・fail-closed 7変種と誠実記録）
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-fit-20261122/cand16.py
  role: verifier
  note: 閉形式の正本cand16（in_T16値2表・in_P16値1表・Y=16・commit 33e1c22e）とprobe全点照合（74,741点・mismatch 0・overlap 0・初稿一発一致）。全称検証器は本ファイルを逐語転写
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-fit-20261122/output/audit.json
  role: data
  note: fit監査正本（自己文書化・probe/spot/merge/tail数値・sha256ピン・事前宣言commit e0fbd99d記録・box内マージ行0行の事前宣言を明記）
- path: research/log/2026-11-22-y16-two-token-skeleton-single-owner-note.md
  role: log
  note: fit段階の単一オーナー宣言ノート（commit e0fbd99d・probe実行前に出版・事前横断予想16項目の全記録・対抗宣言チェック・box内マージ行0行の事前明記）
- path: research/log/2026-11-22-two-token-y16-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・経緯・出版記録・次段階）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,16)、全z>=0・全x>=16・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand16）で
  分類する命題の全称証明（status proved・2026-11-22 part2出版でobserved→
  provedに昇格・正本検証器14チェック体制・型機械・census・C1d published
  アンカー・単一オーナー宣言 432664f7 配下のpart1+part2）。系として
  x<=z-17（S=x+16<z-1）の全R行が単一トークン値single_token(x+16,z,R)に一致する
  マージ命題のy=16版とtail R>=x+z+17の(x+16) mod 2を含む（マージ命題は
  y=1..16で全称確定）。標準11×11の空盤・二石root・S2 {59,60}・
  class 1/2/4は範囲外かつUNKNOWNのまま。3トークン以上・y>=17族・固定幅・
  q点版も範囲外。
evidence: >-
  証明はK1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138/K1141/K1152/K1231/K1233/K1235と
  同型の3部構成で、fit段階（125,560点の有限観察・初稿一発一致）に正本監査part1
  （12チェック・commit 66667771/c6cf6cb4/4fa30547系）とpart2（C1d+census・本出版）が
  続きobserved→provedに昇格した。
  (1) 選択肢分解: A子=cand16(z,x-1,R-1)（x=16は合流子(15,16)≡(16,15)で
  cand15(z,16,R-1)）・B子=出版cand15（K1235全称のy=15族逐語転写〔ブロック内
  Y→Y15改名・count-assert〕・x=16行の合流子値も兼ねる）・C子=1 xor cand16(z-1,x,R-1)。
  分解が素再帰の選択肢値集合と一致することをraw二重再帰で錨止めする（C3・1,245点・
  両生エンジンC1 22,800点・単一トークン/B子/x=16合流子C1b 41,834点）。
  (2) 恒等式: 閉形式格子C2 217,021点・深tail行C2b 19,316点・深格子C12 1,854,930点・
  seeded遠方probe C7 200,000点（seed 20261162・z,x<=3000）・境界多様体C8 992,652点
  （dx∈[-30,17]・x=15行は拡張整合行のみで生主張外〔y=15機のx=14行と同じ規約〕）・
  vシェルC9 905,670点・生censusアンカーC11 884,400点（両エンジン442,200点ずつ・
  bounded-memoization twin・LRU cap 1.6M・本hostはメモリ上限が強くunbounded掃引は
  OOM停止を確認済みのため全rawアンカーをtwin経由・part merge fail-closed）。
  (3) 型機械: clip窓2y+2=34・番兵35で394,686型の(value, sorted子)完全収束
  （C4 595,990点・C4時点309,141型・confluence_bad 0）。C4t tightness probeで
  clip 33（2y+1）は1,638点の収束違反（最初(60,96,96)）がありclip 2y+2=34がtight・
  2y+2 clip tightは12族連続（y=5..16: 12/14/16/18/20/22/24/26/28/30/32/34）。
  merge corollary x<=z-17→single_token(x+16,z,R) 1,243,466点（y=16ではfit probe box
  z=0..30にマージ行が存在しないため本機が初の全域raw anchor）・tail corollary
  R>=x+z+17→(x+16) mod 2 193,300点・それぞれ不一致0。part2(C1d): published
  uniform closed form 6切片（K0999/K1000・K1001・K1011・K1065・K1077・K1087）の
  アンカーA8u..A17uをy=15 part2正本検証器からverbatim抽出し、組み込み前に出版
  アンカー×H_ordered×H_canonical×cand16の4方照合（13,140点+低R縮約9,504点）で
  事前検証してから組み込み、x=16..159・R<=x+61・R<=z+6の137,808点でy=16行vs
  cand16を照合・不一致0。part2(C11r): census_rows.py第三実装（z=0..79・x=16..70・
  R=0..x+z+18・4,400行446,600点・値0点223,295・LRU上限1.6M明示キャップ）の行ごとの
  Thue-Morse指数・T/P集合・tailをcand16から再導出して全行照合・不一致0・
  fail-closed（重複行・欠落行・rows!=80*55・末尾改行欠落はFAIL-CLOSED）。
  監査計6,916,256照合点・全チェック不一致0・同一cwd 2回+
  隔離tree/cwd/HOME+PYTHONHASHSEED=random（preflight・census・両census partの
  再生成を含む）1回の3実行でaudit.jsonとcensus.txtがbyte-identical
  （SHA-256 audit 9748ff5c…・census.txt f0b1a960…）。part1 fail-closed 6種
  （census part points改ざん・part欠落・merge corollary bad改ざん・box field改ざん・
  cand16ブロックY定数改ざん16→17〔C1 903 bad〕・B子Y15改ざん15→16〔C1b 777 bad〕）
  とpart2 fail-closed 6種（census part points改ざん・canonical part欠落・
  corollary merge界改ざんx<=z-17→-16〔merge bad 200〕・census.txt P集合1桁改ざん・
  census.txt欠落・重複行注入）を出版前に実施し全て捕捉。
  part1の誠実事故記録（出版前の初回C11orderedがbad 147,972・原因はbuilder rename
  未到達の末尾リテラル(x,15)・修正後に全面再実行でbad 0・badバイトは未出版）は
  published_run.txtと実験READMEが正本。有限監査は転写・実装照合であり、全称性は
  選択肢分解の健全性・正確なmex恒等式・有限型空間の完全性（K1023→K1239 と同一
  trust境界）による。
---

## 命題・範囲

すべての z>=0・x>=16・R>=0 に対して H(R;(x,16);z) = cand16(z,x,R) が成り立つ
（**status: proved・2026-11-22 part2出版でobserved→provedに昇格**）。正本は
[実験dir](../../experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/README.md)
で、verify_y16_universal.py（part2正本 SHA-256 bdf4fe04…）が正本検証器、
cand16.py が閉形式の正本実装である。全称監査は part1（12チェック・
[part1 log](../log/2026-11-22-y16-universal-verifier-part1.md)）と part2
（C1d出版切片アンカー+census第三実装・
[part2 log](../log/2026-11-22-y16-universal-verifier-part2.md)）の2段階で、
14チェック総6,916,256照合点・全bad 0・3実行byte-identical。
part1 の機械構成は B子=出版cand15逐語転写〔x=16合流子{15,16}≡{16,15}〕・
型機械 clip窓 2y+2=34・メモリ上限host向けのcensus bounded-memoization twin。

y=16 は偶数 y 族（y=10/12/14 と同型）で、値1無限帯・tail 値1 は x 奇の行。
主要構造は pin格子（統一式 pin=z+(d+48)/2・o_pin∈[17,32]・奇z d≡0 (mod 4)
{-12,-8,-4,0,4,8,12,16} の8行・偶z d≡2 (mod 4) {-14,-10,-6,-2,2,6,10,14}
の8行〔y/2 行数則第4点・**両偶奇 8 行の初例**〕・最終pin行 d=16=y が偶y族で
初めて上端に到達し I[33) 型・「pinスロット=th-1」6族連続）・奇z I帯行
k(d)=floor((d+50)/4)=floor((d+3y+2)/4)・th が 17..33 の**連続整数 17 行掃引の
初例**・偶z I帯行 k=floor((d+47)/4)（6族目・th=2k+1・偶z pinスロット=2k+1）・
base行 k=floor((d+49)/4)（7族目）・偶z base d=16 で飽和 k=16・掃引行 d=17・
定常pin z+32（奇z）/z+33（偶z）・band下端 2y+2=34・**偶y族単一band則**
（y=15のband_base/band_int分離との対照）・tail開始 x+z+17・tail値 (x+16)
mod 2・偶z対角行 d=-16 の値1全欠如（9族目）・マージ行 x<=z-17 の
O[1, q_odd(x+16)]・基底点16点 {z+1,...,z+31}。

## 昇格判定（part2）

フル14チェック監査PASS（6,916,256点・bad 0）・fail-closed事前検証済みのC1d
出版切片アンカー137,808点照合・独立第三実装census 446,600点のC11r全行照合・
3回byte-identical実行（1回は隔離tree/cwd/HOME+PYTHONHASHSEED=random・部品は
隔離側再生成）により、**K1237はobserved→provedに昇格**（同一K項目・採番なし・
K1141/K1152/K1231/K1233/K1235と同一のpart1/part2手続き）。系のマージ命題
y=16版 `x<=z-17 => H == single_token(x+16,z,R)` とtail値 `(x+16) mod 2`
は同一スコープの全称命題として確定し、マージ命題は y=1..16 で全称確定。
B子逐語連鎖は cand9..cand15（7リンク）に拡大した。

## fitの工芸的観察（歴史・全称段階の前に）

**初稿一発一致（修正0）**: cand16 初稿は y=14 の出版最終構造（cand14・K1233
全称昇格済み）を seed とした Y+2 機械翻訳で、probe 74,741 点に修正0で一致。
「直前の出版最終構造 seed による外挿が一発一致する」は4連続
（cand11→13・cand13→15〔奇〕・cand12→14・cand14→16〔偶〕）となり、
横断法則一般補題化レーンの主要リスク（族式の y 依存跳躍）をさらに低減した。
初の「box内マージ行0行」族でもあり、事前宣言どおりマージ回帰は全面 box 外、
全称段階の merge corollary 1,243,466 点が初の全域生エンジン錨止めとなった。
