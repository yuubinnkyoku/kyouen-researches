---
id: K1152
title: "2トークン残余ゲーム y=12族のパラメトリック閉形式の全称証明（全z>=0・全x>=12・全R>=0）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "two-token y=12 parametric all-z universal proof, P12"
  - "cand12 fitting and box-out spot verification (fitting stage, pre-promotion)"
  - "cand12 fitting probe (992 rows 71,672 pts) with row-form correction of the 240-point even-z mismatch"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・Theorem T・単一トークン閉形式のraw anchor（C1b・merge corollary x<=z-13→single_token(x+12,z,R)）に使用する
- type: depends_on
  target: K1143
  note: B子（y=11子）の評価にy=11族出版表cand11を使用する（x=12合流子(11,12)≡(12,11)も同一）。cand11は正本検証器にy=11正本から102行逐語転写。B子に先行出版族の閉形式を逐語転写する構成はy=10（B=cand9）・y=11（B=cand10）・y=12（B=cand11）の3連
- type: extends
  target: K1141
  note: y=10族全称閉形式cand10（偶数y型の構造系列・マージ/tail/clip窓/pin格子の族法則）のy=12版
- type: depends_on
  target: "K1162"
  note: "全称証明part1（正本検証器12チェック・overall PASS 6,311,993点・3回byte-identical）とpart2（本項昇格段階・同一単一オーナー宣言配下の工程記録）"
- type: generalizes
  target: K0999
  note: z=8・y>=9一様全Grundy分類のy=12行は本項の特殊例（転写アンカーA8uとしてC1d照合）
- type: generalizes
  target: K1000
  note: z=8・y>=9一様全Grundy分類（K0999の証明範囲）のy=12行は本項の特殊例
- type: generalizes
  target: K1001
  note: z=9・y>=9一様全Grundy分類のy=12行は本項の特殊例（転写アンカーA9uとして照合）
- type: generalizes
  target: K1011
  note: z=10・y>=9一様全Grundy分類のy=12行は本項の特殊例（転写アンカーA10uとして照合）
- type: generalizes
  target: K1065
  note: z=15・y>=6族のy=12行は本項の特殊例（published closed formを転写アンカーA15uとして照合）
- type: generalizes
  target: K1077
  note: z=16・y>=6族のy=12行は特殊例（転写アンカーA16uとして照合）
- type: generalizes
  target: K1087
  note: z=17・y>=6族のy=12行は特殊例（転写アンカーA17uとして照合）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/README.md
  role: proof
  note: 正本監査段階の実験記録（機械構成・転写照合・part1 12チェック+part2 C1d/C11r 14チェック結果表・bounded-memoization twin設計と前身試行のOOM/timeout実験事実・3回決定性・fail-closed 5件・再現コマンド・observed→proved昇格判定）
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/verify_y12_universal.py
  role: verifier
  note: 正本検証器（part2正本・SHA-256 e2092976…49,295 bytes・純stdlib・seed固定・sorted keys・14チェック構成。part1出版正本はcommit 60622f35のf73614f7…36,170 bytes・12チェック）
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/scripts/preflight_c1d_y12.py
  role: verifier
  note: C1dアンカー組み込み前のfail-closed事前検証（anchor×H_ordered×H_canonical×cand12の4方照合14,484点＋低R縮約9,768点・不一致0・2回byte-identical）
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/census_rows.py
  role: verifier
  note: z=0..79・x=12..70・R=0..x+z+14の生tuple二重再帰census第三実装（4,720行450,760点・値0点225,361・状態計算misses 6,121,227・LRU上限1.6M明示キャップ・約13秒）
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/output/audit.json
  role: data
  note: part2フル14チェック監査正本（3,673 bytes・SHA-256 6bca3fa2…・total_points 6,902,613・total_bad 0・3実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/output/census.txt
  role: data
  note: census行表正本（4,720行＋空行80・828,655 bytes・SHA-256 67e48cbe…・C11rでcand12から再導出して全行照合・不一致0）
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/output/preflight-c1d-y12.json
  role: data
  note: 事前検証結果正本（14,484+9,768点・不一致0・SHA-256 7562b8dd…）
- path: research/log/2026-11-20-y12-parametric-allz-proof-part1.md
  role: log
  note: part1（12チェック6,311,993点全PASS・3回byte-identical・昇格はpart2まで行わない）
- path: research/log/2026-11-20-y12-parametric-allz-proof-part2.md
  role: log
  note: part2（C1d事前検証・census第三実装・14チェック監査・3回byte-identical・K1152 observed→proved昇格・出版記録）
- path: research/log/2026-11-20-y12-universal-verifier-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-20T17:03:31Z・K1152 fitレーンは自宣言で全称段階を保持範囲外と明示）
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-fit-20261120/report.md
  role: data
  note: cand12のz偶奇別T/P集合表全文（奇z I帯 th=ceil((d+3y+1)/2) の連続整数掃引・pinスロット (d+3y)/2=th-1 のmod 4衝突構造・偶z pin 6行の初例・初期不一致240点の修正記録）とfitting段階の検証規模の記録
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-fit-20261120/cand12.py
  role: verifier
  note: 閉形式の正本cand12（in_T12値2表・in_P12値1表・Y=12）とprobe全点照合（71,672点・mismatch 0・SHA-256 79e588b3…）。正本検証器は本ファイルを逐語転写する
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-fit-20261120/probe_y12.py
  role: verifier
  note: 生二重再帰probe（z=0..30・x=12..z+28・R<=x+z+26・992行・71,672点・SHA-256 fdfd903d…）
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-fit-20261120/spot_y12.py
  role: verifier
  note: box外spot 26,272点bad 0＋tail raw回帰84点0（SHA-256 777c1f07…）
- path: research/log/2026-11-20-two-token-y12-parametric-fit.md
  role: log
  note: fit段階の宣言確認・初稿240点不一致の行型抽出による修正経緯・出版記録
- path: research/log/2026-11-20-y12-two-token-skeleton-single-owner-note.md
  role: log
  note: fit段階の単一オーナー宣言ノート（宣言2026-11-20T14:25:00Z・2026-11-20T14:25:00Z commit fe93c969）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,12)、全z>=0・全x>=12・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand12）で
  完全分類する。K0999/K1000（z=8）・K1001（z=9）・K1011（z=10）の
  y=12行とK1065/K1077/K1087（z=15,16,17のy>=6族）のy=12行は本項の特殊例
  であり、z>=18（z=18,y=12を含む）のy=12行も主張に含まれる（以後のy=12
  スライス出版は不要）。系としてx<=z-13（S=x+12<z-1）の全R行が単一
  トークン値single_token(x+12,z,R)に一致するマージ命題のy=12版が全称に
  昇格する（マージ命題はy=1..12で全称確定〔y=11版はK1143 part2待ち〕）。
  tail R>=x+z+13=(x+z+y+1)の(x+12) mod 2も全称に含む。
evidence: >-
  証明はK1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138/K1141と同型の
  3部構成で、fit段階（114,570点の有限観察）に正本監査part1（12チェック・
  commit 60622f35/258cd7b0/1093e075）とpart2（C1d+census・本出版）が続き
  observed→provedに昇格した。(1) 選択肢分解: A子=cand12(z,x-1,R-1)
  （x=12は合流子(11,12)≡(12,11)でcand11(z,12,R-1)）・B子=出版cand11
  （先行出版のy=11族fit表を102行逐語転写）・C子=1 xor cand12(z-1,x,R-1)。
  分解が素再帰の選択肢値集合と一致することをraw二重再帰で錨止めする
  （C3・1,125点・両生エンジンC1 21,660点・単一トークン/B子/x=12合流子
  C1b 41,666点）。(2) 恒等式: 閉形式格子C2 224,273点・深tail行C2b
  18,964点・深格子C12 1,872,838点・seeded遠方probe C7 200,000点
  （seed 20261132）・境界多様体C8 890,765点・vシェルC9 915,654点・
  生censusアンカーC11 892,080点（両エンジン・bounded-memoization
  twin・part merge fail-closed）。(3) 型機械: clip窓2y+2=26・番兵±27で
  191,789型の(value, sorted子)完全収束（C4 616,484点・confluence_bad 0）。
  C4t tightness probeでclip 25は3,540点の収束違反（最初(60,88,88)）があり
  clip 2y+2=26がtight・2y+2 clip tightは8族連続
  （y=5..12: 12/14/16/18/20/22/24/26）。merge corollary
  x<=z-13→single_token(x+12,z,R) 1,417,623点・tail corollary
  R>=x+z+13→(x+12) mod 2 232,510点・それぞれ不一致0。part2(C1d):
  published uniform closed form 6切片（K0999/K1000・K1001・K1011・
  K1065・K1077・K1087）のアンカーA8u..A17uをy=10 part2正本検証器から
  238行verbatim抽出し、組み込み前に4方照合（14,484点+低R縮約9,768点）
  で事前検証してから組み込み、x=12..159・R<=x+61・R<=z+6の139,860点で
  y=12行vs cand12を照合・不一致0。part2(C11r): census_rows.py第三実装
  （z=0..79・x=12..70・R=0..x+z+14・4,720行450,760点・LRU上限1.6M明示
  キャップ）の行ごとのThue-Morse指数・T/P集合・tailをcand12から再導出
  して全行照合・不一致0・fail-closed。監査計6,902,613照合点・全チェック
  不一致0・同一cwd 2回+隔離tree/cwd/HOME+PYTHONHASHSEED=random（census
  再生成含む）1回の3実行でaudit.jsonとcensus.txtがbyte-identical
  （SHA-256 audit 6bca3fa2…・census.txt 67e48cbe…）。census part改ざん・
  corollary改ざん・欠落・census.txt改ざん（P集合1桁）の5種fail-closed
  検査を出版前に実施し全て捕捉。有限監査は転写・実装照合であり、全称性は
  選択肢分解の健全性・正確なmex恒等式・有限型空間の完全性
  （K1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138/K1141と同一
  trust境界）による。
---

## 命題・範囲

すべての z>=0・x>=12・R>=0 に対して H(R;(x,12);z) = cand12(z,x,R) が成り立つ
（status: proved・2026-11-20 part2出版でobserved→provedに昇格）。正本は
[実験dir](../../experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/README.md)
で、verify_y12_universal.py（part2正本 SHA-256 e2092976…）が正本検証器、
cand12.py が閉形式の正本実装である。全称監査は part1（12チェック・
[part1 log](../log/2026-11-20-y12-parametric-allz-proof-part1.md)）と part2
（C1d出版切片アンカー+census第三実装・
[part2 log](../log/2026-11-20-y12-parametric-allz-proof-part2.md)）の2段階で、
14チェック総6,902,613照合点・全bad 0・3実行byte-identical。

y=12 は y 偶族（y=10 と同型）で、値1無限帯・tail は x 奇の行。構造は
y=10（K1141）と pin 格子の d シフト・k 定数の引き上げを除いて同一
（ladder・対角cap z+y-[z≡y mod 2]（奇z z+12/偶z z+11）・pin格子
奇z {-8,-4,0,4,8,12} の6行・偶z {-10,-6,-2,2,6,10} の6行（偶z側6行は本族が
全称確定した初例）・掃引行 d=y+1=13 の帯・定常pin 2y+z（奇z）/2y+z+1（偶z）
（z+24/z+25）・基底点12点 {z+1,...,z+23}・band下端 2y+2=26・tail開始
x+z+y+1=x+z+13・マージ境界 x<=z-(y+1)=z-13・最終pin行 d=y の I[2y+z+1) 型・
偶z対角行の値1全欠如（y=8..12 で5族連続全称確定））。
y=12 特有の構造は奇z I 帯行の
th(d)=ceil((d+3y+1)/2)=ceil((d+37)/2) が d=-12..12 を 2 ずつ走るごとに
13,14,15,...,25 の連続整数を 1 回ずつ通ることと、
pin スロット (d+3y)/2 = th-1 の交替（d≡0 mod 4: 偶offset の値2 pin・
d=-12 の対角cap も同 slot・d≡2 mod 4: 奇offset の b_k 上端点（値1））で、
これにより z 奇数 pin 行・最終 pin 行・対角行の T/P 重複が 0 になる
（y=11/y=12 は pin=th-1 型・y=10 は th-2 型）。

## 全称昇格の根拠

(i) fit段階: probe box 992 行・71,672 点（初稿240点不一致の行型修正後）
＋box外spot 26,272点＋merge/tail回帰の計114,570点比較・不一致0。
(ii) part1正本監査12チェック 6,311,993 点・全bad 0（生両エンジン錨・
B子=x=12合流子錨・恒等式格子・型機械〔clip 2y+2=26 tight・8族連続〕・
遠方probe・境界多様体・vシェル・bounded-memoization twinの生census
アンカー・深格子）・3実行byte-identical。
(iii) part2: C1d 139,860点（published 6切片のy=12行アンカー・組み込み前
4方事前検証つき）・C11r 450,760点（census_rows.py第三実装の全行を
cand12から再導出照合）・フル14チェック監査 6,902,613点・全bad 0・
3実行byte-identical・fail-closed検査5種捕捉。
マージ命題の y=12 版（x<=z-13）と tail 値 (x+12) mod 2 は全称系として昇格
（corollary照合 1,417,623/232,510点・それぞれ不一致0）。
有限監査は転写・実装照合であり、全称性は選択肢分解の健全性・正確なmex
恒等式・有限型空間の完全性（K1023→K1141 と同一trust境界）による。
3 トークン以上・y>=13 族・固定幅・q 点版安定化長・標準 11×11 の勝敗は
範囲外。REFUTED-D10 型の実験とは異なり LOSS 証明を含まない。

## 横断観察（y=1..12・y=12 は全称確定）

- tail 開始族式 x+z+y+1 が y=2..12 の 11 族連続（y=12 は全称確定）。
  tail 値 (x+y) mod 2・値1無限帯と tail の x 偶奇が y 偶奇で決まり
  y 偶族（y=10/12）は x 奇の行・y 奇族（y=9/11）は x 偶の行。
- 基底点 y 点仮説 {z+1,..,z+2y-1} が 12 例目（y=1..12・y=12 は全称確定）。
- pin 統一式 pin=z+(d+3y)/2〔d≡y (mod 4)（奇z）・d≡y+2 (mod 4)（偶z）〕が
  **8 族連続**（y=5..12・y=12 は全称確定）。pin 行 d 範囲は
  奇z [−y+4, y]（y 偶: 6/8/10/12 の4族）・偶z [−y+2, y−2]（y 偶: 6/8/10/12 の4族）。
  偶z pin 6 行は y=12 が全称確定した初例（y=11 は 5 行）。
- base 行の base rank が k(d)=floor((d+3y+1)/4) で y=10/11/12 の全 base 行
  （z 偶奇・行型反転込み）で同一。偶z I 帯行 k(d)=floor((d+3y-1)/4) が
  y=11/12 の 2 族で同一（y=10 は floor((d+3y+3)/4)、y=10 は d=y で飽和・
  y=11/12 は飽和なし）。
- 対角行上端格子規則 cap=z+y-[z≡y (mod 2)] が y=12 で全称確定（C1d相当の
  published切片と全チェックの全zで一致）。
- clip 窓族式候補 2y+2 が **8 族連続 tight**（y=5..12: 12/14/16/18/20/22/24/26・
  y=12 は C4t clip 25 の 3,540 違反で tight 確定）。
- 偶 z 対角行の値1全欠如が 5 族連続（y=8..12・y=12 は全称確定）。最終 pin 行
  d=y の I[2y+z+1) 型が 7 族的確定へ（y=6/8/9/10/11/12・y=12 は全称確定）。
- 奇 z I 帯 th: y=10 は 2k（pin は th-2 型）・y=11 は 2k+1・y=12 は
  ceil((d+3y+1)/2)（連続整数掃引・pin は th-1 型）。y=11/12 は
  「pin スロット=th-1」型に揃っており、y=13 fit での追完が横断型の判定材料。
