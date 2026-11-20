---
id: K1152
title: 2トークン残余ゲーム y=12族のパラメトリック閉形式候補 cand12 の fitting と box 外 spot 検証（全z>=0・全x>=12・全R>=0 は未証明）
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases: [two-token y=12 parametric closed-form fit, P12 fitting stage, cand12 fitting and box-out spot verification]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式のraw anchor・マージ行回帰に使用する
- type: depends_on
  target: K1143
  note: y=11族fit出版表（比例子の行型・band構造・偶z対角行の値1全欠如）をfit予想表の生成に使用。次段階の全称監査ではB子（y=11子）として出版 cand11 を使う（x=12合流子(11,12)equiv(12,11)・正本監査は本fitと独立の宣言）
- type: extends
  target: K1141
  note: y=10族全称閉形式cand10（z偶奇別T/P表の構造・pin統一式・base/band/pin格子の族法則）をy=12のfit表の構造シードとし、偶y型の12族目として系列観察を延長する
artifacts:
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-fit-20261120/report.md
  role: data
  note: cand12のz偶奇別T/P集合表全文（奇z I帯 th=ceil((d+3y+1)/2) の連続整数掃引と pin スロット (d+3y)/2=th-1 の mod 4 衝突構造・偶z base k=(d+3y+1)/4 と I 帯 k=(d+3y-1)/4・偶z pin 6行の初例・偶z対角行の値1全欠如5族連続・最終pin行 d=y の I[2y+z+1) 型6族連続・初期不一致240点の修正記録）とfitting段階の検証規模の記録
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-fit-20261120/cand12.py
  role: verifier
  note: 閉形式の正本cand12（in_T12値2表・in_P12値1表・Y=12）とprobe全点照合（71,672点・mismatch 0・overlap 0・SHA-256 79e588b3...）。正本検証器は本ファイルを逐語転写する
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-fit-20261120/probe_y12.py
  role: verifier
  note: 生二重再帰probe（z=0..30・x=12..z+28・R<=x+z+26・992行・71,672点・約3.4秒・probe_rows.txtは未出版で決定論的再生・SHA-256 fdfd903d...）
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-fit-20261120/spot_y12.py
  role: verifier
  note: box外spot 26,272点bad 0＋tail raw回帰84点0（約18.4秒・SHA-256 777c1f07...）
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-fit-20261120/output/audit.json
  role: data
  note: probe・spot・merge・tailの監査数値とSHA-256・再生コマンド
- path: research/log/2026-11-20-two-token-y12-parametric-fit.md
  role: log
  note: fit段階の宣言確認・初稿240点不一致の行型抽出による修正経緯・出版記録
- path: research/log/2026-11-20-y12-two-token-skeleton-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-20T14:25:00Z・commit fe93c969・fitから出版まで保持・正本監査は範囲外宣言）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,12)。本項は有限fitting段階であり、
  probe box（z=0..30・x=12..z+28・R<=x+z+26・71,672点）とbox外spot
  （深R<=130・大z=31..40・x=y=12エッジ・大d<=52・26,272点）・merge回帰
  （16,542比較）・tail raw回帰（84点）の合計114,570点比較で
  H(R;(x,12);z)=cand12(z,x,R)（z偶奇別パラメトリックT/P集合表）を確認した
  ものである。全z>=0・全x>=12・全R>=0の全称は次段階の12チェック監査で
  判定する。マージ行x<=z-13が単一トークン閉形式single_token(x+12,z,R)に
  一致するマージ命題のy=12版・tail R>=x+z+13=(x+z+y+1)の(x+12) mod 2は
  fittingレベルで回帰済み。
evidence: >-
  (1)生二重再帰probe（K1138/K1141/K1143と同一正準降順多重集合エンジン）を
  z=0..30について走らせ、行ごとのT/P offset構造を全dについて抽出した。
  (2)y=10族表（K1141・全称証明済み）とy=11族表（K1143・fit出版）からの
  外挿初稿は71,672点中240点の不一致（すべてz偶数行）とT/P重複48を示し、
  行型抽出・生decodeで修正（偶z base k は (d+33)//4 から (d+37)//4、
  偶z I 帯は k=(d+35)//4・th=2k+1、奇z I 帯は th=ceil((d+37)/2) の
  連続整数掃引で pin スロット (d+36)/2=th-1 を d≡0 (mod 4) で値2 pin・
  d≡2 (mod 4) で b_k 上端に割り当て）して probe 全点一致
  （mismatch 0・T/P重複 0・値頻度0:35,102/1:26,780/2:9,790・値3なし）。
  (3)box外spot 26,272点（深R<=130・大z=31..40のpin/対角/掃引/定常行・
  x=y=12エッジz=12..40・大d∈{30,41,52}・マージ行(30,12)）で生エンジンと
  直接照合してbad 0。tailは spot 内 d>=13 の6行×R∈[x+z+13, x+z+26]
  84点でraw値 (x+12) mod 2 全一致。(4)マージ行x<=z-13: probe 1,428点＋
  box外回帰16,542比較でK0832単一トークン形式と不一致0。
  全体で114,570点比較・不一致0。probe_rows.txtは別cwd再生成でbyte-identical、
  監査JSONは3実行でbyte-identical。すべてのスクリプトは決定論的・
  純Python標準ライブラリのみ。全称性の機械監査（選択肢分解・恒等式
  グリッド・型confluence・census）は次段階。
---

## 命題・範囲

すべての z>=0・x>=12・R>=0 に対して H(R;(x,12);z) = cand12(z,x,R) が成り立つ、
という全称命題の fitting 段階の観察（status: observed）。本項の正本は
[実験dirのreport.md](../../experiments/vertical-fiber-two-token-y12-parametric-allz-fit-20261120/report.md)
で、cand12.py が閉形式の正本実装である。検証は有限（probe box＋box外spot
＋回帰・合計114,570点比較・不一致0）であり、全称証明ではない。

y=12 は y 偶族（y=10 と同型）で、値1無限帯・tail は x 奇の行。構造は
y=10（K1141・全称証明済み）と pin 格子の d シフト（d≡y (mod 4) 奇z・
d≡y+2 (mod 4) 偶z・pin=z+(d+3y)/2）・k 定数の引き上げを除いて同一
（ladder・対角cap z+y-[z≡y mod 2]（奇z z+12/偶z z+11）・pin格子
奇z {-8,-4,0,4,8,12} の6行・偶z {-10,-6,-2,2,6,10} の6行（偶z側6行は本族が初例）・
掃引行 d=y+1=13 の帯 O[2y+z, x+z+y]（奇z偶offset）/O[2y+z+1, x+z+y]（偶z奇offset）・
定常pin 2y+z（奇z）/2y+z+1（偶z）（z+24/z+25）・基底点 y 点 {z+1,...,z+23}・
band下端 2y+2=26・tail開始 x+z+y+1=x+z+13・マージ境界 x<=z-(y+1)=z-13・
最終pin行 d=y の I[2y+z+1) 型・偶z対角行の値1全欠如（y=8..12 で5族連続））。
y=12 特有の構造発見は奇z I 帯行の
**th(d)=ceil((d+3y+1)/2)=ceil((d+37)/2) が d=-12..12 を 2 ずつ走るごとに
13,14,15,...,25 の連続整数を 1 回ずつ通る**ことと、
**pin スロット (d+3y)/2 = th-1 の交替**（d≡0 mod 4: 偶offset の値2 pin・
d=-12 の対角cap も同 slot・d≡2 mod 4: 奇offset の b_k 上端点（値1））で、
これにより z 奇数 pin 行・最終 pin 行・対角行の T/P 重複が 0 になる。

## 現在の根拠と限界

根拠は (i) probe box 992 行・71,672 点の生二重再帰との全点一致
（mismatch 0・T/P 重複 0）・(ii) box 外 spot 26,272 点 bad 0
（z<=40・d<=52・x=12 エッジ・R<=z+130・マージ行深R）・(iii) マージ行回帰
1,428＋16,542 比較不一致 0（K0832 単一トークン形式）・(iv) tail 回帰
13,888＋84 点、の114,570点比較である。限界: 全称性（任意 z・任意 x>=12・
任意 R）は未証明。次段階の 12 チェック監査（A子=H(R-1;(x-1,12);z)・
B子=出版 cand11 逐語転写・C子=1 xor cand12(z-1,x,R-1)・x=12 合流子
(11,12)≡(12,11)・型機械 clip 窓 2y+2=26 の tight 判定（y=5..10 の
tight 継続の7族目候補）・census z=0..79・x=12..70）で判定する。
3 トークン以上・y>=13 族・固定幅・q点版安定化長・標準 11×11 の勝敗は
範囲外。REFUTED-D10 型の実験とは異なり LOSS 証明を含まない。

## 横断観察（y=2..12・y=12 は fitting レベル）

- tail 開始族式 x+z+y+1 が y=2..12 の 11 族連続（y=12 は fit レベル）。
  tail 値 (x+y) mod 2・値1無限帯と tail の x 偶奇が y 偶奇で決まり
  y 偶族（y=10/12）は x 奇の行・y 奇族（y=9/11）は x 偶の行。
- 基底点 y 点仮説 {z+1,..,z+2y-1} が 12 例目（y=1..12・y=12 は fit レベル）。
- pin 統一式 pin=z+(d+3y)/2〔d≡y (mod 4)（奇z）・d≡y+2 (mod 4)（偶z）〕が
  **8 族連続**（y=5..12・y=12 は fit レベル）。pin 行 d 範囲は
  奇z [−y+4, y]（y 偶: 6/8/10/12 の4族）・偶z [−y+2, y−2]（y 偶: 6/8/10/12 の4族）。
  偶z pin 6 行は y=12 が初例（y=11 は 5 行）。
- base 行の base rank が k(d)=floor((d+3y+1)/4) で y=10/11/12 の全 base 行
  （z 偶奇・行型反転込み）で同一。偶z I 帯行 k(d)=floor((d+3y-1)/4) が
  y=11/12 の 2 族で同一（y=10 は floor((d+3y+3)/4)、y=10 は d=y で飽和・
  y=11/12 は飽和なし）。
- 対角行上端格子規則 cap=z+y-[z≡y (mod 2)] が y=12 の全 probe z で成立。
- clip 窓族式候補 2y+2（y=5..10 で 6 族連続 tight）の y=12 値 26 が band 下端
  として出現。±26/番兵±27 の tight 判定は次段階の型機械で行う。
- 偶 z 対角行の値1全欠如が 5 族連続。最終 pin 行 d=y の I[2y+z+1) 型が
  6 族連続（y=6/8/9/10/11/12）。
- 奇 z I 帯 th: y=10 は 2k（pin は th-2 型）・y=11 は 2k+1・y=12 は
  ceil((d+3y+1)/2)（連続整数掃引・pin は th-1 型）。y=11/12 は
  「pin スロット=th-1」型に揃っており、y=13 fit での追完が横断型の判定材料。
