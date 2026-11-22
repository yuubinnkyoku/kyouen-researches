---
id: K1235
title: "2トークン残余ゲーム y=15族のパラメトリック閉形式のfitting（全z>=0・全x>=15・全R>=0・有限fit段階）"
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases:
  - "two-token y=15 parametric closed-form fit, P15-fit"
  - "cand15 fitting and box-out spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 74,865 probe points; odd-y template extrapolation from the published FINAL cand13, the promoted-universal y=13 table)"
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
  note: y=14全称part1と同一監査系列の次段階候補（verify_y15_universal.py・別宣言必要・clip窓2y+2=32の11族連続tight候補）。本fitは全称段階を範囲外と明示
artifacts:
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
  分類する命題のfitting段階（有限probe box+box外spot+回帰でHenry一致・
  status observed）。全称証明（正本検証器14チェック体制・型機械・census・
  C1d published アンカー）は次段階・別宣言。系としてx<=z-16
  （S=x+15<z-1）の全R行が単一トークン値single_token(x+15,z,R)に一致する
  マージ命題のy=15版（fit level）とtail R>=x+z+16=(x+z+y+1)の(x+15) mod 2
  （fit level）を含む。標準11×11の空盤・二石root・S2 {59,60}・class 1/2/4は
  範囲外かつUNKNOWNのまま。3トークン以上・y>=16族・固定幅・q点版も範囲外。
evidence: >-
  有限fit（全称ではない）: probe生二重再帰（y=11..y=14出版と同一の降順正準形
  エンジン）box z=0..30・x=15..z+29・R<=x+z+32（=2y+2・y=14出版の宣言済み
  convention継承）930行74,865点で、cand15初稿（y=13出版最終構造cand13の
  Y+2外挿・宣言ノート事前登録の奇数y族式）が一発完全一致（修正0・mismatch 0・
  T/P重複0・値頻度 0:36,770/1:28,846/2:9,249・値3なし）。box内tail assertion
  （R>=x+z+16→(x+15) mod 2）15,810点bad 0。box内マージ行は事前宣言どおり
  0行（y=15ではx<=z-16にz>=31が必要）。box外spot 39,215点bad 0（deep 15行
  4810点で全8奇z pin行{-13,-9,-5,-1,3,7,11,15}・全7偶z pin行{-11,-7,-3,1,5,9,13}
  を個別に生値検証・両対角・非pin I/base行・d=15飽和行・掃引d=16両偶奇・定常
  base/I・マージ境界(31,15)/(32,16)・bigz z=31..40×27d・x=y=15エッジ・大
  d{32,43,54}・**全選択行にx>=15の機械assert**）。merge回帰（cand15 vs
  K0832 single_token・z∈{31,38,45,52,62,75}・x=15..z-16・R<=x+z+31）14,325
  比較bad 0。tail raw回帰84点bad 0。合計128,489点比較・全bad 0。決定性:
  probe_rows.txt同一cwd/別cwd/隔離tree/cwd/HOME+PYTHONHASHSEED=randomの3回
  再生成でbyte-identical（SHA-256 2c7b72ad…）・audit.json 3回実行byte-identical
  （SHA-256 5c329dd4…）。fail-closed 5種（probe 1点値改ざん・pin位置値改ざん・
  Y定数改ざん・pin mod4クラス改ざん・probe_rows.txt欠落）を隔離dirで実施し
  全て捕捉・復元後auditはbaselineとbyte-identical。trust境界: 全称性は選択肢
  分解の健全性・mex恒等式・有限型空間の完全性（K1023→K1234と同一の機械分類）に
  依存し、本項は有限観察の機械的証拠のみを主張する。横断観察（fit level）:
  pin統一式pin=z+(d+45)/2・o_pin∈[16,30]が11族目・奇z 8行（(y+1)/2=8の初
  8行族・y=11/13/15で6→7→8確定）・偶z 7行（(y-1)/2・5→6→7確定）・「pin
  スロット=th-1」がy=11..15の5族連続（全8 pin行でth(d)-1=o_pin(d)が格子・
  算術両面で成立・偶zは2k(d)+1=o_pin(d)）・base行k=floor((d+46)/4)がy=10..15
  6族連続・偶z I行k=floor((d+44)/4)がy=11..15 5族連続・th=2k+1ペア反復（奇y）
  掃引（偶y）の偶奇分離15族目・偶z対角行値1全欠如8族目候補・最終pin行
  d=y=15のI[31)型10族目候補・band下端2y+2=32・clip窓2y+2=32（11族連続tight
  候補・全称段階C4tで判定）・tail開始族式x+z+y+1の15族目・基底点y点仮説の
  15例目・初稿一発一致3連続（11→13・12→14・13→15）で「出版最終構造seed
  法則」が偶奇両系列で2回ずつ確定。
---

## 命題・範囲

すべての z>=0・x>=15・R>=0 に対して H(R;(x,15);z) = cand15(z,x,R)
（**status: observed・有限fit段階・全称は未証明**）。正本は
[実験dir](../../experiments/vertical-fiber-two-token-y15-parametric-allz-fit-20261122/report.md)
で、cand15.py が閉形式の正本実装、probe_y15.py が生エンジン、
spot_y15.py が box 外検証器、output/audit.json が監査正本である。
128,489 点比較（一致0不一致）は有限 probe box＋box 外 spot＋回帰に基づく
fit level の証拠であり、全称（全 z・全 x・全 R）を主張しない。
全称段階（verify_y15_universal.py・B子=出版cand14逐語転写〔x=15合流子
{14,15}≡{15,14}〕・A子合流の正準順序注意〔y=14 fit の spot 事故の実証済み
再発防止策として本fitは全spot行に x>=15 機械assertを組み込み済み〕・型機械
clip窓 2y+2=32 の 11 族 tight 候補判定・census）は別宣言が必要。

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
（8族目候補）。

## fitの工芸的観察

**初稿一発一致（修正0）**: cand15 初稿は y=13 の出版最終構造（cand13・K1231
全称昇格済み）を seed とした Y+2 外挿で、probe 74,865 点に一致するまで修正を
要さなかった。「直前の出版最終構造 seed による外挿が一発一致する」が
奇数 y 2 連続（cand11→cand13・cand13→cand15）・偶数 y 1 回（cand12→cand14）の
3 連続となり、y>=16 への族構造則一般化（横断法則の一般補題化レーン）の主要
リスク（族式の y 依存跳躍）がさらに低減した。修正を要しやすい領域（y=12 の
修正 echo: z 偶数行の k 定数・I 帯開始、z 奇数 pin 衝突）は本 fit ではすべて
初期構造のままで一致した。

## 全称昇格に必要な次段階（範囲外）

verify_y15_universal.py の監査体制（A子・B子=出版cand14逐語転写・C子・型機械
clip 2y+2=32〔11 族 tight 候補〕・census・C1d published アンカー）は
y=1..14 出版系列と同一の手続きで、着手には新規単一オーナー宣言が必要
（本項の fit 宣言 26a1ad28 は全称段階を保持範囲外と明記）。標準 11×11 空盤・
二石 root・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。

## 横断観察（fit level・全称ではない）

- tail 開始族式 x+z+y+1 が y=15 で一致（15 族目・y<=14 は全称/証明済み）。
- 基底点 y 点仮説 {z+1,..,z+2y-1} が 15 例目。
- pin 統一式 pin=z+(d+3y)/2 が 11 族目。y 奇族 pin 行数 (y+1)/2〔奇z〕/
  (y-1)/2〔偶z〕が y=11/13/15 の 3 点で増加則として確定（初の 8 行族）。
- 「pin スロット=th-1」が y=11..15 の **5 族連続**（y<=14 は全称確定・y=15 fit）。
  偶z の 2k+1 slot 則も 5 族連続。
- base 行 k(d)=floor((d+3y+1)/4) が y=10..15 **6 族連続**。偶z I 帯行
  k(d)=floor((d+3y-1)/4) が y=11..15 **5 族連続**。
- th 連続整数掃引〔偶y〕と 2k+1 ペア反復〔奇y〕の偶奇分離が明白（y=12/14
  掃引・y=11/13/15 反復）。
- 偶z 対角行の値1全欠如が **8 族連続候補**（y=8..15・うち y<=13 全称・
  y=14 別証明済み・y=15 fit）。最終 pin 行 d=y の I[2y+z+1) 型が **10 族目候補**
  （y=15 で初めて奇z pin 上端が d=y）。
- band 下端 2y+2 と clip 窓 2y+2 が y=15 で 32（clip tight 判定は全称段階）。
- 初稿一発一致が 3 連続（11→13・12→14・13→15）。y=12 の 240 点修正は
  暫定構造 seed・修正後の出版最終構造は以後の族で全て修正不要。
