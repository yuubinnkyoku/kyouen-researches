---
id: K1233
title: "2トークン残余ゲーム y=14族パラメトリック閉形式のfitting（有限一致・初稿一発0修正・全称は次段階）"
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases:
  - "two-token y=14 parametric closed-form fit, P14-fit"
  - "cand14 fitting (first-draft zero-correction agreement on all 74,834 probe points; even-y template extrapolation from the published FINAL cand12)"
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
artifacts:
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
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,14)、有限fit範囲 z=0..30・x=14..z+29・R<=x+z+30
  ＋box外spot・merge/tail回帰の計122,829点比較。cand14(z,x,R)のz偶奇別T/P集合表が
  上記有限範囲で生二重再帰エンジン・K0832単一トークン形式と完全一致（mismatch 0・
  T/P重複 0）。全z>=0・全x>=14・全R>=0の全称主張は含まない（次段階の正本監査対象）。
  y=14は偶数y族（y=10/y=12と同型）で値1無限帯・tailはx奇の行。系としてfit levelの
  マージ命題y=14版（x<=z-15）とtail値(x+14) mod 2・横断族法則のy=14順位
  （pin格子統一式・pin行数y/2=7両偶奇初例・z-odd th連続整数掃引2族目・
  「pinスロット=th-1」4族連続・base行k=floor((d+3y+1)/4) 5族連続・偶z I帯k=floor((d+3y-1)/4)
  4族連続・偶z対角行値1全欠如7族連続候補・最終pin行I[2y+z+1)型9族的確定・band下端2y+2=30）
  を含む。
evidence: >-
  単一オーナー宣言（2026-11-22T18:42:55Z・commit e3a856ad・probe実行前に事前出版し、
  pin格子統一式のy=14適用・pin mod 4クラス回転・th連続整数掃引・k定数族式・対角cap・
  基底点・tail/marge族式をすべて予想として事前登録）の下で実行した有限fit。
  (1) probe（生二重再帰・降順正準形メモ化・y=11/12/13と同一の正本エンジン）:
  z=0..30・x=14..z+29・R<=x+z+30（2y+2=30拡張・宣言済み）の961行74,834点。
  cand14初稿（y=12出版最終構造cand12のY+2外挿・宣言通りの族式）が**修正0で全点一致**、
  T/P重複0・値頻度 0:36,711/1:28,593/2:9,530・値3なし。y=12 fitの240点修正・
  y=11/y=13の一発一致と対照する偶数y族初の系列テストで、出版最終構造seedの外挿が
  偶数yでも一発一致。(2) box内assertion: tail領域 R>=x+z+15 の15,376点が値(x+14) mod 2
  に全一致（y=12/y=13のcap x+z+26では観測できなかった深帯をbox内で直接確認）・
  マージ領域 x<=z-15 の222点がsingle_token(x+14,z,R)に全一致。(3) box外spot 32,017点
  bad 0（深R<=130代表15行・大z=31..40×23d・x=y=14エッジ・大d∈{30,41,52}）・
  merge回帰15,336比較0・tail raw回帰84点0。(4) 決定性: probe_rows.txt別cwd再生成
  byte-identical・audit 2回実行byte-identical・fail-closedモデル。
  誠実記録: spot深行の初回選択に定義域x>=14未満の(19,13)（{13,14}はy=13族x=14行で
  生値1が正しい）が混入し該当1点のみbadになったが、出版前に(21,15)へ修正し以後の
  全実行はbad 0。合計122,829点比較・不一致0。全称性は含まない。
---

## 命題・範囲

有限fit範囲（z=0..30・x=14..z+29・R<=x+z+30・box外spot・merge/tail回帰の計122,829点比較）で
H(R;(x,14);z) = cand14(z,x,R)（status: observed）。正本は
[実験dir](../../experiments/vertical-fiber-two-token-y14-parametric-allz-fit-20261122/report.md)
で、`cand14.py` が閉形式の正本実装。全称主張（全z>=0・全x>=14・全R>=0）は範囲外で、
次段階の正本監査（verify_y14_universal.py・12チェック・型機械 clip 窓 2y+2=30〔10族連続
tight候補〕・census）で判定する。

y=14 は偶数 y 族（y=10/y=12 と同型）で、値1無限帯・tail 値1 は x 奇の行。主要構造は
ラダー（奇z 奇R O[1,z]／偶z 奇R O[1,z-1]）・マージ行 x<=z-15 の O[1, q_odd(x+14)]・
対角行 d=-14 の cap=z+14-[z≡14 mod 2]=[z+14]（奇z）/[z+13]（偶z）（奇z 偶offset [2,14]・
偶z 奇offset [1,13]）・pin格子（統一式 pin=z+(d+42)/2・o_pin∈[15,28]・o_pin≡z+1 (mod 2)・
奇z d≡y≡2 (mod 4) {-10,-6,-2,2,6,10,14} の7行〔偶y族式 y/2=7 の両偶奇初例〕・
偶z d≡y+2≡0 (mod 4) {-12,-8,-4,0,4,8,12} の7行・**y=12 の d≡0 から d≡2 への
mod 4 クラス回転が格子統一式・行数則を保ったまま成立〔偶数y族で回転テストされた初例〕**）・
奇z I帯行（d 偶 15 行・対角込）の k(d)=floor((d+44)/4)=floor((d+3y+2)/4)・
th(d)=2k+[d≡y (mod 4)]（**連続整数掃引 15..29**・偶数y族式の2族目・pin行が th-1=2k を
ちょうど占有〔「pinスロット=th-1」4族連続・mod 4回転後も成立の初例〕・skew行 d≡0 mod 4
は th=2k で slot=2k-1 が b_k 上端点と一致）・base行 k(d)=floor((d+43)/4)
（y=10..13 4族同一式の5族目）・偶z I帯行 k(d)=floor((d+41)/4)=floor((d+3y-1)/4)
（y=11..13 3族同一式の4族目・th=2k+1）・偶z pin は base行偶d の 2k+1 位置
（y=11..13 に続き4族目）・掃引行 d=15 の帯（奇z 偶offset [2y+z, x+z+y]／偶z 奇offset
[2y+z+1, x+z+y]）・定常行 d>=16 の定常pin z+28（奇z）／z+29（偶z）・基底点14点
{z+1,...,z+27}・band下端 2y+2=30・tail開始 x+z+15・最終pin行 d=14=y の I[2y+z+1)=I[29)型
（pin off 28 は定常pinと同値）・偶z対角行の値1全欠如7族連続候補。

## fitの工芸的観察

**初稿一発一致（修正0）**: cand14 初稿は y=12 の出版最終構造（cand12・修正後の族式）を
seed とした Y+2 外挿で、probe 74,834 点に一致するまで修正を要さなかった。y=12 fit は
y=10 の暫定構造 seed で 240 点の修正（z 偶数行 k 定数・I 帯開始、z 奇数 pin 衝突）を
要したが、その修正で確定した族式が y=14 ではそのまま正しかった。これにより
「直前の出版最終構造 seed による外挿は一発一致する」（奇数 y: cand11→cand13、
偶数 y: cand12→cand14）が偶奇両系列で確定し、y>=15 族への一般化レーンの主要リスク
（族式のy依存跳躍）が低減した。

## trust 境界

本成果は有限 fitting と spot 検証であり全称定理ではない。cand14 が全 z>=0・全 x>=14・
全 R>=0 で成り立つという主張は次段階の 12 チェック監査（A子=H(R-1;(x-1,14);z)・
B子=K1231 の出版 cand13 逐語転写〔x=14 合流子 (13,14)≡(14,13)〕・C子=1 xor
cand14(z-1,x,R-1)・型機械 clip 窓 2y+2=30 の tight 判定〔10 族連続候補〕・
census z=0..79・x=14..70）で判定する。A子の x=14 行は {13,14} の正準順序で
y=13 族 x=14 行と同一状態になる点（本 fit の spot 深行誤選択が実証）に留意。
3 トークン以上・y>=15 族・固定幅・q 点版安定化長・標準 11×11 の勝敗は範囲外。
