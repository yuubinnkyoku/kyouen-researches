---
id: K1233
title: "2トークン残余ゲーム y=14族のパラメトリック閉形式の全称証明（全z>=0・全x>=14・全R>=0）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "two-token y=14 parametric closed-form fit, P14-fit"
  - "cand14 fitting and box-out spot verification (fitting stage, pre-promotion; first-draft zero-correction agreement on all 74,834 probe points, zero corrections; even-y template extrapolation from the published FINAL cand12)"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（マージ行 x<=z-15 と回帰計15,558比較に使用）
- type: extends
  target: K1152
  note: y=12族全称閉形式（K1152）の次の偶数y族。cand14初稿はy=12出版最終構造cand12（修正後の族式）のY+2外挿で生成し、probe 74,834点に一発一致（y=12 fitがy=10暫定構造seedで240点修正を要したのと対照的・偶数y族でも「出版最終構造seedは修正不要」という工芸的観察が確定）
- type: extends
  target: K1231
  note: y=13族全称閉形式（K1231）の次族。横断法則（pin格子統一式・pin mod 4クラスのy回転・th連続整数掃引・pinスロット=th-1）のy=14テストが本fitの主眼で、宣言ノートに事前登録した予想がすべてfit levelで一致
- type: depends_on
  target: "K1141"
  note: y=10族全称（偶数y族の比較対象・pin行数5/6/7・z-odd th型 2k/掃引/掃引の偶数y族系列の基点）
- type: depends_on
  target: "K1234"
  note: 全称証明part1（正本検証器12チェック・overall PASS 6,377,860点・3回byte-identical）とpart2（本項昇格段階・同一単一オーナー宣言配下の工程記録）
- type: generalizes
  target: K0999
  note: z=8・y>=9一様全Grundy分類のy=14行は本項の特殊例（転写アンカーA8uとしてC1d照合）
- type: generalizes
  target: K1000
  note: z=8・y>=9一様全Grundy分類（K0999の証明範囲）のy=14行は本項の特殊例
- type: generalizes
  target: K1001
  note: z=9・y>=9一様全Grundy分類のy=14行は本項の特殊例（転写アンカーA9uとして照合）
- type: generalizes
  target: K1011
  note: z=10・y>=9一様全Grundy分類のy=14行は本項の特殊例（転写アンカーA10uとして照合）
- type: generalizes
  target: K1065
  note: z=15・y>=6族のy=14行は本項の特殊例（published closed formを転写アンカーA15uとして照合）
- type: generalizes
  target: K1077
  note: z=16・y>=6族のy=14行は特殊例（転写アンカーA16uとして照合）
- type: generalizes
  target: K1087
  note: z=17・y>=6族のy=14行は特殊例（転写アンカーA17uとして照合）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/README.md
  role: proof
  note: 正本監査段階の実験記録（機械構成・転写照合・part1 12チェック+part2 C1d/C11r 14チェック結果表・bounded-memoization twin設計・3回決定性・fail-closed 5件・再現コマンド・observed→proved昇格判定・CI step不登録の理由）
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/verify_y14_universal.py
  role: verifier
  note: 正本検証器（part2正本・SHA-256 6ac219cf…・51,537 bytes・1,317行・純stdlib・seed固定・sorted keys・14チェック構成。part1出版正本はcommit 677ced40系の4ecdec11…・37,439 bytes・12チェック）
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/scripts/preflight_c1d_y14.py
  role: verifier
  note: C1dアンカー組み込み前のfail-closed事前検証（anchor×H_ordered×H_canonical×cand14の4方照合13,824点＋低R縮約9,636点・不一致0・z別2,160/2,192/2,224/2,384/2,416/2,448・2回byte-identical）
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/census_rows.py
  role: verifier
  note: z=0..79・x=14..70・R=0..x+z+16の生tuple二重再帰census第三実装（4,560行449,160点・値0点224,566・状態計算misses 7,146,027・LRU上限1.6M明示キャップ・約14.2秒・maxrss 639,424KB）
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/output/audit.json
  role: data
  note: part2フル14チェック監査正本（3,674 bytes・SHA-256 b91e88a0…・total_points 6,965,866・total_bad 0・3実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/output/census.txt
  role: data
  note: census行表正本（824,003 bytes・4,560行＋空行80・SHA-256 baad513c…・C11rでcand14から再導出して全行照合・不一致0・tailアサート全行成立）
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/output/preflight-c1d-y14.json
  role: data
  note: 事前検証結果正本（13,824+9,636点・不一致0・SHA-256 c7369b4c…）
- path: research/log/2026-11-22-y14-universal-verifier-part1.md
  role: log
  note: part1（12チェック6,377,860点全PASS・3回byte-identical・昇格はpart2まで行わない）
- path: research/log/2026-11-22-y14-parametric-allz-proof-part2.md
  role: log
  note: part2（C1d事前検証・census第三実装・14チェック監査・3回byte-identical・K1233 observed→proved昇格・出版記録）
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-fit-20261122/report.md
  role: proof
  note: fit段階の正本記録（74,834 probe点一発一致・box外spot 32,017点・merge回帰15,336比較・tail raw 84点・box内tail assertion 15,376点・事前予想の判定表・y=6..14族表記述）
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-fit-20261122/cand14.py
  role: verifier
  note: 閉形式の正本cand14（in_T14値2表・in_P14値1表・Y=14）とprobe全点照合（74,834点・mismatch 0・overlap 0・初稿一発一致）。次段階の正本検証器は本ファイルを逐語転写する
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-fit-20261122/probe_y14.py
  role: verifier
  note: 生二重再帰probe（z=0..30・x=14..z+29・R<=x+z+30・961行・74,834点・約5.5秒・別cwd再生成byte-identical・R上限の2y+2=30拡張は宣言済み）
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-fit-20261122/spot_y14.py
  role: verifier
  note: box外spot 32,017点bad 0＋merge回帰15,336比較0＋tail raw回帰84点0（約92秒・LRU cap 1.5M決定的退避・深行選択の初期誤りと修正の誠実記録つき）
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-fit-20261122/make_audit_y14.py
  role: verifier
  note: 決定的audit生成器（fail-closed: mismatch/overlap/tail_bad/mg_bad/偶z対角値1/pin格子観測が非ゼロならauditを書かない・2回実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-fit-20261122/output/audit.json
  role: data
  note: fit監査正本（自己文書化・probe/spot/merge/tail数値・sha256ピン・事前宣言commit e3a856ad記録）
- path: research/log/2026-11-22-y14-two-token-skeleton-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-22T18:42:55Z・commit e3a856ad・probe実行前に出版・事前横断予想の全記録を含む）
- path: research/log/2026-11-22-two-token-y14-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・経緯・誠実記録・出版記録）
- path: research/experiments/vertical-fiber-two-token-y14-parametric-fit-second-verification-20261122/README.md
  role: proof
  note: 独立第二検証（同一毎時タスクの別実行レーン・fit出版は対抗宣言18:42:55Zに19秒差で譲渡済み・第二レーンの宣言・fit出版はmainになし）。独立導出したcand14の生probe 90,049点（K1233 probe box外の17,137点を含む相補box・z=0..33・x=14..z+30・R<=x+z+28）対K1233出版cand14 mismatch 0・K1233出版probe_y14.py再生成74,834点（行SHA同一633f17cc…）対第二レーンcand14 mismatch 0・両実装の判定等価グリッド2,241,162点 mismatch 0・Y定数改ざんfail-closed捕捉・overall PASS（second_verification.json SHA-256 04b72214…）。y=14生probe行表の初出版も本dir
- path: research/experiments/vertical-fiber-two-token-y14-parametric-fit-second-verification-20261122/y14_second_verification.py
  role: verifier
  note: 第二検証の正本検証器（V1-V4・決定的・純stdlib・K1233出版dir引数取り・fetch-back版で再実行PASS・second_verification.json byte-identical）
- path: research/log/2026-11-22-y14-fit-second-verification.md
  role: log
  note: 第二検証の実行記録（二重並走の解決・譲渡経緯・box相補性・K1171/K1231併存のmaintainer判定事項記録・trust境界）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,14)、全z>=0・全x>=14・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand14）で
  完全分類する。K0999/K1000（z=8）・K1001（z=9）・K1011（z=10）の
  y=14行とK1065/K1077/K1087（z=15,16,17のy>=6族）のy=14行は本項の特殊例
  であり、z>=18（z=18,y=14を含む）のy=14行も主張に含まれる（以後のy=14
  スライス出版は不要）。系としてx<=z-15（S=x+14<z-1）の全R行が単一
  トークン値single_token(x+14,z,R)に一致するマージ命題のy=14版が全称に
  昇格する（マージ命題はy=1..14で全称確定）。tail
  R>=x+z+15=(x+z+y+1)の(x+14) mod 2も全称に含む。
evidence: >-
  証明はK1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138/K1141/K1152/K1231と同型の
  3部構成で、fit段階（122,829点の有限観察・初稿一発一致・独立第二検証レーンによる同一閉形式の
  独立二導出〔判定等価2,241,162点〕）に正本監査part1（12チェック・commit 677ced40/94069d48/
  9050d4f6系）とpart2（C1d+census・本出版）が続きobserved→provedに昇格した。
  (1) 選択肢分解: A子=cand14(z,x-1,R-1)（x=14は合流子(13,14)≡(14,13)で
  cand13(z,14,R-1)）・B子=出版cand13（K1231全称のy=13族をブロック内Y→Y13改名のみで
  逐語転写）・C子=1 xor cand14(z-1,x,R-1)。分解が素再帰の選択肢値集合と一致することを
  raw二重再帰で錨止めする（C3・1,185点・両生エンジンC1 22,230点・単一トークン/B子/
  x=14合流子C1b 42,447点）。(2) 恒等式: 閉形式格子C2 222,705点・深tail行C2b 19,140点・
  深格子C12 1,864,368点・seeded遠方probe C7 200,000点（seed 20261142・z,x<=3000）・
  境界多様体C8 993,021点（dx∈[-30,17]・tail窓 [x+z+15,x+z+17]）・vシェルC9 910,710点・
  生censusアンカーC11 889,200点（両エンジン・bounded-memoization twin・part merge
  fail-closed）。(3) 型機械: clip窓2y+2=30・番兵31で281,912型の(value, sorted子)完全収束
  （C4 606,427点・C4時点248,232型・confluence_bad 0）。C4t tightness probeでclip 29（2y+1）
  は2,480点の収束違反（最初(60,92,92)）がありclip 2y+2=30がtight・2y+2 clip tightは
  10族連続（y=5..14: 12/14/16/18/20/22/24/26/28/30）。merge corollary
  x<=z-15→single_token(x+14,z,R) 1,370,848点・tail corollary R>=x+z+15→(x+14) mod 2
  212,713点・それぞれ不一致0。part2(C1d): published uniform closed form 6切片
  （K0999/K1000・K1001・K1011・K1065・K1077・K1087）のアンカーA8u..A17uをy=13 part2
  正本検証器からverbatim抽出し、組み込み前に出版アンカー×H_ordered×H_canonical×cand14の
  4方照合（13,824点+低R縮約9,636点）で事前検証してから組み込み、x=14..159・R<=x+61・
  R<=z+6の138,846点でy=14行vs cand14を照合・不一致0。part2(C11r): census_rows.py
  第三実装（z=0..79・x=14..70・R=0..x+z+16・4,560行449,160点・LRU上限1.6M明示キャップ）
  の行ごとのThue-Morse指数・T/P集合・tailをcand14から再導出して全行照合・不一致0・
  fail-closed。監査計6,965,866照合点・全チェック不一致0・同一cwd 2回+
  隔離tree/cwd/HOME+PYTHONHASHSEED=random（census・preflight再生成含む）1回の3実行で
  audit.jsonとcensus.txtがbyte-identical（SHA-256 audit b91e88a0…・census.txt
  baad513c…）。census part改ざん・merge corollary改ざん・part欠落・census.txt改ざん
  （P集合1桁）・census.txt欠落の5種fail-closed検査を出版前に実施し全て捕捉。
  fit段階の誠実記録（spot深行の初回誤選択(19,13)→出版前に(21,15)へ修正し以後の全実行
  bad 0）と独立第二検証（実験dir commit dc0a7cfc・SV log commit 04f1b30e・同一毎時
  タスクの別実行レーンが独立導出したcand14との双方向生値照合90,049+74,834点・判定等価
  2,241,162点・不一致0）はfit実験dir/第二検証dirが正本。有限監査は転写・実装照合であり、
  全称性は選択肢分解の健全性・正確なmex恒等式・有限型空間の完全性
  （K1023→K1231 と同一trust境界）による。
---

## 命題・範囲

すべての z>=0・x>=14・R>=0 に対して H(R;(x,14);z) = cand14(z,x,R) が成り立つ
（status: proved・2026-11-22 part2出版でobserved→provedに昇格）。正本は
[実験dir](../../experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/README.md)
で、verify_y14_universal.py（part2正本 SHA-256 6ac219cf…）が正本検証器、
cand14.py が閉形式の正本実装である。全称監査は part1（12チェック・
[part1 log](../log/2026-11-22-y14-universal-verifier-part1.md)）と part2
（C1d出版切片アンカー+census第三実装・
[part2 log](../log/2026-11-22-y14-parametric-allz-proof-part2.md)）の2段階で、
14チェック総6,965,866照合点・全bad 0・3実行byte-identical。

y=14 は偶数 y 族（y=10/y=12 と同型）で、値1無限帯・tail 値1 は x 奇の行。主要構造は
ラダー（奇z 奇R O[1,z]／偶z 奇R O[1,z-1]）・マージ行 x<=z-15 の O[1, q_odd(x+14)]・
対角行 d=-14 の cap=z+14-[z≡14 mod 2]=[z+14]（奇z）/[z+13]（偶z）（奇z 偶offset [2,14]・
偶z 奇offset [1,13]）・pin格子（統一式 pin=z+(d+42)/2・o_pin∈[15,28]・o_pin≡z+1 (mod 2)・
奇z d≡y≡2 (mod 4) {-10,-6,-2,2,6,10,14} の7行〔偶y族式 y/2=7 の両偶奇初例〕・
偶z d≡y+2≡0 (mod 4) {-12,-8,-4,0,4,8,12} の7行・**y=12 の d≡0 から d≡2 への
mod 4 クラス回転が格子統一式・行数則を保ったまま成立〔偶数y族で回転テストされた初例〕**）・
奇z I帯行（d 偶 15 行・対角込）の k(d)=floor((d+44)/4)=floor((d+3y+2)/4)・
th(d)=2k+[d≡y (mod 4)]（**連続整数掃引 15..29**・偶数y族式の2族目・pin行が th-1=2k を
ちょうど占有〔「pinスロット=th-1」4族連続・y=14は全称確定・mod 4回転後も成立の初例〕・skew行 d≡0 mod 4
は th=2k で slot=2k-1 が b_k 上端点と一致）・base行 k(d)=floor((d+43)/4)
（y=10..13 4族同一式の5族目）・偶z I帯行 k(d)=floor((d+41)/4)=floor((d+3y-1)/4)
（y=11..13 3族同一式の4族目・th=2k+1）・偶z pin は base行偶d の 2k+1 位置
（y=11..13 に続き4族目）・掃引行 d=15 の帯（奇z 偶offset [2y+z, x+z+y]／偶z 奇offset
[2y+z+1, x+z+y]）・定常行 d>=16 の定常pin z+28（奇z）／z+29（偶z）・基底点14点
{z+1,...,z+27}・band下端 2y+2=30・tail開始 x+z+15・最終pin行 d=14=y の I[2y+z+1)=I[29)型
（pin off 28 は定常pinと同値）・偶z対角行の値1全欠如（y=8..14 に続き 7 族連続で全称確定）。

## fitの工芸的観察

**初稿一発一致（修正0）**: cand14 初稿は y=12 の出版最終構造（cand12・修正後の族式）を
seed とした Y+2 外挿で、probe 74,834 点に一致するまで修正を要さなかった。y=12 fit は
y=10 の暫定構造 seed で 240 点の修正（z 偶数行 k 定数・I 帯開始、z 奇数 pin 衝突）を
要したが、その修正で確定した族式が y=14 ではそのまま正しかった。これにより
「直前の出版最終構造 seed による外挿は一発一致する」（奇数 y: cand11→cand13、
偶数 y: cand12→cand14）が偶奇両系列で確定し、y>=15 族への一般化レーンの主要リスク
（族式のy依存跳躍）が低減した。

## 全称昇格の根拠

(i) fit段階: probe box 961 行・74,834 点の生二重再帰との全点一致（初稿一発一致）
＋box外spot 32,017点＋merge/tail回帰の計122,829点比較・不一致0・独立第二検証レーンに
よる同一閉形式の独立二導出（双方向生値照合90,049+74,834点・判定等価2,241,162点・
不一致0・Y定数改ざんfail-closed捕捉）。
(ii) part1正本監査12チェック 6,377,860 点・全bad 0（生両エンジン錨・
B子=x=14合流子錨・恒等式格子・型機械〔clip 2y+2=30 tight・10族連続〕・
遠方probe・境界多様体・vシェル・bounded-memoization twinの生censusアンカー・深格子）・
3実行byte-identical。
(iii) part2: C1d 138,846点（published 6切片のy=14行アンカー・組み込み前
4方事前検証13,824+9,636点つき）・C11r 449,160点（census_rows.py第三実装の全行を
cand14から再導出照合）・フル14チェック監査 6,965,866点・全bad 0・
3実行byte-identical・fail-closed検査5種捕捉。
マージ命題の y=14 版（x<=z-15）と tail 値 (x+14) mod 2 は全称系として昇格
（corollary照合 1,370,848/212,713点・それぞれ不一致0）。
有限監査は転写・実装照合であり、全称性は選択肢分解の健全性・正確なmex
恒等式・有限型空間の完全性（K1023→K1231 と同一trust境界）による。
3 トークン以上・y>=15 族・固定幅・q 点版安定化長・標準 11×11 の勝敗は範囲外。
REFUTED-D10 型の実験とは異なり LOSS 証明を含まない。

## 横断観察（y=1..14・y=14 は全称確定）

- tail 開始族式 x+z+y+1 が y=2..14 の **13 族連続**（y=14 は全称確定）。
  tail 値 (x+y) mod 2・値1無限帯と tail の x 偶奇が y 偶奇で決まり
  y 偶族（y=10/12/14）は x 奇の行。
- 基底点 y 点仮説 {z+1,..,z+2y-1} が 14 例目（y=1..14・y=14 は全称確定）。
- pin 統一式 pin=z+(d+3y)/2〔d≡y (mod 4)（奇z）・d≡y+2 (mod 4)（偶z）〕が
  y=5..14 の **10 族連続**（y=14 は全称確定）。y=14 の pin 行 d 範囲は
  奇z {-10,-6,-2,2,6,10,14}・偶z {-12,-8,-4,0,4,8,12} の各 7 行
  （偶 y 族式 y/2=7 の両偶奇 7 行初例が全称確定。y=12 の d≡0 から d≡2 への
  mod 4 クラス回転が偶数 y 族で成立した初例も全称側で確定）。
- 「pin スロット=th-1」型（奇z pin 行で pin が off=2k=th-1 をちょうど占有）が
  y=11/y=12/y=13/y=14 の **4 族連続で全称確定**（K1152 が指名した横断型の問いに全称で
  回答）。偶z側は pin が base 行上端 2k-1 の +2 位置（2k+1）に載る slot 則が 4 族同一。
- base 行の base rank が k(d)=floor((d+3y+1)/4) で y=10/11/12/13/14 の全 base 行
  （z 偶奇・行型反転込み）で同一（5 族）。偶z I 帯行 k(d)=floor((d+3y-1)/4) が
  y=11/12/13/14 の 4 族で同一。奇 z 連続整数掃引 th=2k+[d≡y (mod 4)] が偶数 y 族
  2 例目（y=12 に続き全称確定）。
- 対角行上端格子規則 cap=z+y-[z≡y (mod 2)] が y=14 で全称確定
  （C1d相当のpublished切片と全チェックの全zで一致）。
- clip 窓族式候補 2y+2 が **10 族連続 tight**（y=5..14:
  12/14/16/18/20/22/24/26/28/30・y=14 は C4t clip 29 の 2,480 違反で tight 確定）。
- 偶 z 対角行の値1全欠如が **7 族連続で全称確定**（y=8..14）。最終 pin 行
  d=y の I[2y+z+1) 型が 9 族的確定（y=6/8/9/10/11/12/13/14・y=14 は全称確定）。
- B 子に先行出版族の閉形式を逐語転写する構成: cand9（y=10 の B 子）・
  cand10（y=11 の B 子・K1141 全称）・cand11（y=12 の B 子・K1143）・
  cand12（y=13 の B 子・K1152 全称）・cand13（y=14 の B 子・K1231 全称）で 5 連
  （全称証明済み族を B 子に使うのは cand10・cand12・cand13）。
- 初稿一発一致が y=11/13/14 の 3 例（y=12 は 240 点修正・y=10 は手順外）。
  偶数 y 族のテンプレート外挿が過剰修正なく Y+2 に伸び、出版最終構造 seed の外挿が
  偶奇両系列で一発一致することが全称確定を経て証拠の裏付けを得た。
