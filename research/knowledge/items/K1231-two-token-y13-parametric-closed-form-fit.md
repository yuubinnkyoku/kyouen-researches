---
id: K1231
title: 2トークン残余ゲーム y=13族のパラメトリック閉形式候補 cand13 の fitting と box 外 spot 検証（全z>=0・全x>=13・全R>=0 は未証明
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases: [two-token y=13 parametric closed-form fit, P13 fitting stage, cand13 fitting and box-out spot verification]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・Theorem T・単一トークン閉形式のraw anchor・マージ行回帰に使用する
- type: depends_on
  target: K1143
  note: y=11族fit表cand11（y=13と同じy奇型の直接テンプレート）の族法則をY+2外挿してcand13初稿を生成した。初稿はprobe 72,664点に一発一致（修正0・y=12は240点修正を要したのと対照的）
- type: extends
  target: K1152
  note: y=12族全称閉形式（K1152）が次段階の横断型判定材料として指名した「y=13 fitでの追完」（pinスロット=th-1型・y奇族の行型）にfitレベルで回答する。次段階の全称監査ではB子（y=12子）として出版検証器verify_y12_universal.pyのcand12を逐語転写して使う（x=13合流子(12,13)equiv(13,12)も同一）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261122/report.md
  role: data
  note: cand13のz偶奇別T/P集合表全文（S=x+13偶奇のy奇型・奇z 7行/偶z 6行のpin格子・偶z対角行の値1全欠如6族連続・最終pin行d=yのI[2y+z+1)型7族連続候補・band下端2y+2=28・pin格子統一式o_pin=(d+3y)/2の横断再現）とfitting段階の検証規模の記録
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261122/cand13.py
  role: verifier
  note: 閉形式の正本cand13（in_T13値2表・in_P13値1表・Y=13）とprobe全点照合（72,664点・mismatch 0・overlap 0・SHA-256 cb903c56...）。正本検証器は本ファイルを逐語転写する
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261122/probe_y13.py
  role: verifier
  note: 生二重再帰probe（z=0..30・x=13..z+29・R<=x+z+26・992行・72,664点・紘5.1秒・probe_rows.txtは未出版で決定論的再生・SHA-256 c98f0032...）
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261122/spot_y13.py
  role: verifier
  note: box外spot 31,750点bad 0＋merge回帰17,277比較不一致0＋tail raw回帰84点0（終22.4秒・SHA-256 3846f746...）
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261122/output/audit.json
  role: data
  note: probe・spot・merge・tailの監査数値とSHA-256・再生コマンド
- path: research/log/2026-11-22-two-token-y13-parametric-fit.md
  role: log
  note: fit段階の宣言確認・y=11族表からの外挿初稿一発一致の経繵・出版記録（初出版後にcommit-pinned fetch-backで検出した転写スリップ5箇所の修正コミット76a4f28を含む）
- path: research/log/2026-11-22-y13-two-token-skeleton-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-22T17:01:05Z・commit d3404db8・fitから全称証明段階まで保持）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,13)。本項は有限fitting段階であり、
  probe box（z=0..30・x=13..z+29・R<=x+z+26・72,664点）とbox外spot
  （深R<=130・大z=31..40・x=y=13エッジ・大d<=52・31,750点）・merge回帰
  （17,277比較）・tail raw回帰（84点）の合計121,775点比較で
  H(R;(x,13);z)=cand13(z,x,R)（z偶奇別パラメトリックT/P集合表）を確認した
  ものである。全z>=0・全x>=13・全R>=0の全称は次段階の12チェック監査で
  判定する。マージ行x<=z-14が単一トークン閉形式single_token(x+13,z,R)に
  一致するマージ命題のy=13版・tail R>=x+z+14=(x+z+y+1)の(x+13) mod 2は
  fittingレベルで回帰済み。
evidence: >-
  (1)生二重再帰probe（K1138/K1141/K1143/K1152系列と同一正準降順多重集合
  エンジン）をz=0..30について走らせ、行ごとのT/P offset構造を全dについて
  抽出した。(2)y=11族表（K1143・fit・y=13と同じy奇型）とy=10/y=12族
  （K1141/K1152）の族法則から、統一pin格子式o_pin=(d+3y)/2∈[y+1,2y]・
  o_pin≡z+1 (mod 2)を中心にy=13予想表をcand13.pyに実装し、probe全点照合で
  72,664点・mismatch 0・T/P重複0（初稿から一発一致・値頻度
  0:35,581/1:27,281/2:9,802・値3なし）。(3)box外spot 31,750点
  （深R<=130の代表15行・大z=31..40×代表22 d・x=y=13エッジz=13..40・
  大d∈{30,41,52}）で生エンジンと直接照合してbad 0。(4)マージ行x<=z-14:
  probe 690点＋box外回帰17,277比較でK0832単一トークン形式と不一致0。
  tailはprobe 12,766点＋raw回帰84点で値(x+13) mod 2全一致。全体で
  121,775点比較・不一致0。すべてのスクリプトは決定論的・純Python
  標準ライブラリのみ。全称性の機械監査（選択肢分解・恒等式グリッド・
  型confluence・census）は次段階。
---

## 命題・範囲

すべての z>=0・x>=13・R>=0 に対して H(R;(x,13);z) = cand13(z,x,R) が成り立つ、
という全称命題の fitting 段階の観察（status: observed）。本項の正本は
[実験dirのreport.md](../../experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261122/report.md)
で、cand13.py が閉形式の正本実装である。検証は有限（probe box＋box外spot
＋回帰・合計121,775点比較・不一致0）であり、全称証明ではない。

y=13 は y 奇族（y=9/y=11 と同型）で、値1無限帯・tail は x 偶の行。構造は
y=11（K1143）の Y+2 平行移動が概ねそのまま成立する。主要構造は
ladder（奇z 奇R O[1,z]／偶z 奇R O[1,z-1]）・マージ行 x<=z-14 の
O[1, q_odd(x+13)]・対角行 d=-13 の cap=z+y-[z≡y (mod 2)]（奇z 偶offset
[2,z+12]／偶z 奇offset [1,z+13]）・pin格子（統一式 pin=z+o_pin・o_pin=(d+3y)/2∈[14,26]・
o_pin≡z+1 (mod 2)・奇z 偶o_pin で d∈{-11,-7,-3,1,5,9,13} の7行〔y奇族初の7行〕・
偶z 奇o_pin で d∈{-9,-5,-1,3,7,11} の6行）・掃引行 d=14 の帯
O[2y+z, x+z+y]（奇z 偶offset）／O[2y+z+1, x+z+y]（偶z 奇offset）・定常行
d>=15 の定常pin z+26（奇z）／z+27（偶z）・基底点 13 点 {z+1,...,z+25}・
band下端 2y+2=28・tail開始 x+z+y+1=x+z+14・マージ境界 x<=z-(y+1)=z-14・
最終pin行 d=y の I[2y+z+1) 型・偶z対角行の値1全欠如（y=8..12 に続き6族連続）。
奇z の全行の base rank は k(d)=floor((d+40)/4)=floor((d+3y+1)/4) の単一式で統一され
（th=2k+1・y=11 と同一族式・飽和は d=12 でちょうど k=13 に到達し不要）、
偶z は base 行が同一式・I 帯行が k(d)=floor((d+38)/4)=floor((d+3y-1)/4) の別式
（y=11/12 と同一族式）。

## 現在の根拠と限界

根拠は (i) probe box 992 行・72,664 点の生二重再帰との全点一致
（mismatch 0・T/P 重複 0）・(ii) box 外 spot 31,750 点 bad 0
（z<=40・d<=52・x=13 エッジ・R<=z+130）・(iii) マージ行回帰 690+17,277
比較不一致 0（K0832 単一トークン形式）・(iv) tail 回帰 12,766+84 点、の
121,775 点比較である。限界: 全称性（任意 z・任意 x>=13・任意 R）は未証明。
次段階の 12 チェック監査（A子=H(R-1;(x-1,13);z)・B子=K1152 の cand12
逐語転写〔B子に全称証明済みの y=12 を使う初の族〕・C子=1 xor cand13(z-1,x,R-1)・
x=13 合流子 (12,13)≡(13,12)・型機械 clip 窓 2y+2=28 の tight 判定
〔y=5..12 の8族連続 tight の9族目候補〕・census z=0..79・x=13..70）で判定する。
3 トークン以上・y>=14 族・固定幅・q点版安定化長・標準 11×11 の勝敗は範囲外。
REFUTED-D10 型の実験とは異なり LOSS 証明を含まない。

## 横断観察（y=2..13・y=13 は fitting レベル）

- tail 開始族式 x+z+y+1 が y=2..13 の 12 族連続（y=13 は fit レベル）。
- 基底点 y 点仮説 {z+1,..,z+2y-1} が 13 例目（y=1..13・y=13 は fit レベル）。
- pin 格子統一式 o_pin=(d+3y)/2∈[y+1,2y]・o_pin≡z+1 (mod 2) が
  y=10/y=11/y=12 の出版 pin 行集合をすべて正確に再現し、y=13 では
  奇z 7行／偶z 6行を与える（奇y 族の偶z pin 行数 (y-1)/2 が y=11 の5行から
  6行に増えた初例）。y 奇族では pin 行 d が奇数。
- 「pin スロット = th-1」型（奇z pin 行で pin が off=2k=th-1 をちょうど占有）が
  y=11/y=12/y=13 の 3 族連続（K1152 が指名した横断型の問いに fit レベルで回答）。
  偶z 側は pin が base 行上端 2k-1 の +2 位置（2k+1）に載る slot 則が
  y=11/y=12/y=13 の 3 族で同一。
- 対角行上端格子規則 cap=z+y-[z≡y (mod 2)] が y=13 の全 probe z で成立
  （両偶奇・y=2..12 全称＋y=13 fit）。
- clip 窓族式候補 2y+2（y=5..12 で 8 族連続 tight）の y=13 値 28 が band 下端
  として出現。±28/番兵±29 の tight 判定は次段階の型機械で行う。
- 偶 z 対角行の値1全欠如が 6 族連続。最終 pin 行 d=y の I[2y+z+1) 型が
  7 族連続候補（y=6/8/9/10/11/12/13）。
- base 行 rank 族式 k(d)=floor((d+3y+1)/4) が y=10/11/12/13 の 4 族で全 base 行
  （z 偶奇・行型反転込み）同一。偶 z I 帯行 k(d)=floor((d+3y-1)/4) が
  y=11/12/13 の 3 族同一。奇 z th 則 2k+1 が奇 y 族 3 例目
  （y 偶奇が th 則を決める観察）。
- 初稿一発一致が y=11 に続き 2 例目（y=12 は 240 点修正・y=10 は手順外）。
  奇数 y 族のテンプレート外挿が過剰修正なく Y+2 に伸びるという工芸的観察。
