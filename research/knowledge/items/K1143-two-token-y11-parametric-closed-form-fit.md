---
id: K1143
title: 2トークン残余ゲーム y=11族のパラメトリック閉形式候補 cand11 の fitting と box 外 spot 検証（全z>=0・全x>=11・全R>=0 は未証明）
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases: [two-token y=11 parametric closed-form fit, P11 fitting stage, cand11 fitting and box-out spot verification]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・Theorem T・単一トークン閉形式のraw anchor・マージ行回帰に使用する
- type: depends_on
  target: K1141
  note: y=10族全称閉形式cand10の構造（族法則一式・y偶奇による行型反転）をfit予想表の生成に使用。次段階の全称監査ではB子（y=10子）として出版検証器verify_y10_universal.pyの逐語転写cand10を使う（x=11合流子(10,11)equiv(11,10)も同一）
- type: extends
  target: K1138
  note: y=9族（y奇型）の族法則（値1無限帯・tailがx偶の行・pin d≡y mod 4・偶z対角行の値1全欠如）をy=11のfit表が引き継ぎ、2トークン族の系列観察を11族目に延長する
artifacts:
- path: research/experiments/vertical-fiber-two-token-y11-parametric-allz-fit-20261120/report.md
  role: data
  note: cand11のz偶奇別T/P集合表全文（S=x+11偶奇反転のy奇型・奇z 6行/偶z 5行のpin格子・偶z対角行の値1全欠如4族連続・最終pin行d=yのI[2y+z+1)型5族連続支援・band下端2y+2=24・y=10全称表との構造同一性観察）とfitting段階の検証規模の記録
- path: research/experiments/vertical-fiber-two-token-y11-parametric-allz-fit-20261120/cand11.py
  role: verifier
  note: 閉形式の正本cand11（in_T11値2表・in_P11値1表・Y=11）とprobe全点照合（70,680点・mismatch 0・overlap 0・SHA-256 8a083400...）。正本検証器は本ファイルを逐語転写する
- path: research/experiments/vertical-fiber-two-token-y11-parametric-allz-fit-20261120/probe_y11.py
  role: verifier
  note: 生二重再帰probe（z=0..30・x=11..z+27・R<=x+z+26・992行・70,680点・約4.8秒・probe_rows.txtは未出版で決定論的再生・SHA-256 ef40fae8...）
- path: research/experiments/vertical-fiber-two-token-y11-parametric-allz-fit-20261120/spot_y11.py
  role: verifier
  note: box外spot 28,238点bad 0＋merge回帰26,015比較不一致0＋tail raw回帰84点0（約21.8秒・SHA-256 07ed055b...）
- path: research/experiments/vertical-fiber-two-token-y11-parametric-allz-fit-20261120/output/audit.json
  role: data
  note: probe・spot・merge・tailの監査数値とSHA-256・再生コマンド
- path: research/log/2026-11-20-two-token-y11-parametric-fit.md
  role: log
  note: fit段階の宣言確認・全行構造抽出の経緯（初稿一発一致）・出版記録
- path: research/log/2026-11-20-y11-two-token-skeleton-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-20T11:58:00Z・commit ed778278・fitから全称証明段階まで保持）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,11)。本項は有限fitting段階であり、
  probe box（z=0..30・x=11..z+27・R<=x+z+26・70,680点）とbox外spot
  （深R・大z=31..40・x=y=11エッジ・大d<=52・28,238点）・merge回帰
  （26,015比較）・tail raw回帰（84点）の合計125,017点比較で
  H(R;(x,11);z)=cand11(z,x,R)（z偶奇別パラメトリックT/P集合表）を確認した
  ものである。全z>=0・全x>=11・全R>=0の全称は次段階の12チェック監査で
  判定する。マージ行x<=z-12が単一トークン閉形式single_token(x+11,z,R)に
  一致するマージ命題のy=11版・tail R>=x+z+12=(x+z+y+1)の(x+11) mod 2は
  fittingレベルで回帰済み。
evidence: >-
  (1)生二重再帰probe（K1138/K1141と同一正準降順多重集合エンジン）をz=0..30
  について走らせ、行ごとのT/P offset構造を全dについて抽出した。
  (2)y=10族表（K1141・全称証明済み）をS=x+11偶奇反転のもとでy=11に写した
  予想表をcand11.pyに実装し、probe全点照合で70,680点・mismatch 0・T/P重複 0
  （初稿から一発一致・値頻度0:34,618/1:26,301/2:9,761・値3なし）。
  (3)box外spot 28,238点（深R<=130・大z=31..40のpin/対角/掃引/定常行・
  x=y=11エッジz=11..40・大d∈{30,41,52}）で生エンジンと直接照合してbad 0。
  (4)マージ行x<=z-12: probe 2,412点＋box外回帰26,015比較でK0832単一トークン
  形式と不一致0。tailはprobe 14,880点＋raw回帰84点で値(x+11) mod 2全一致。
  全体で125,017点比較・不一致0。すべてのスクリプトは決定論的・純Python
  標準ライブラリのみ。全称性の機械監査（選択肢分解・恒等式グリッド・
  型confluence・census）は次段階。
---

## 命題・範囲

すべての z>=0・x>=11・R>=0 に対して H(R;(x,11);z) = cand11(z,x,R) が成り立つ、
という全称命題の fitting 段階の観察（status: observed）。本項の正本は
[実験dirのreport.md](../../experiments/vertical-fiber-two-token-y11-parametric-allz-fit-20261120/report.md)
で、cand11.py が閉形式の正本実装である。検証は有限（probe box＋box外spot
＋回帰・合計125,017点比較・不一致0）であり、全称証明ではない。

y=11 は y 奇族（y=9 と同型）で、値1無限帯・tail は x 偶の行。構造は
y=10（K1141・全称証明済み）と S=x+y 偶奇による行型反転と pin 格子の
d≡y (mod 4) シフトを除いて同一（ladder・対角cap z+y-[z≡y mod 2]（奇z
z+10/偶z z+11）・pin格子 pin=z+(d+33)/2（奇z d≡3・6行{-9,..,11}・偶z
d≡1・5行{-7,..,9}）・掃引行d=y+1=12の帯O[2y+z,x+z+y]（奇z偶offset）
/O[2y+z+1,x+z+y]（偶z奇offset）・定常pin 2y+z（奇z）/2y+z+1（偶z）
（z+22/z+23）・基底点 y 点 {z+1,...,z+21}・band下端 2y+2=24・tail開始
x+z+y+1=x+z+12・マージ境界 x<=z-(y+1)=z-12・最終pin行 d=y の
I[2y+z+1) 型・偶z対角行の値1全欠如（y=8/9/10に続き4族連続））。
奇zの全行の base rank は k(d)=floor((d+34)/4) の単一式で統一され
（y=10にあった最終th行の飽和がない）、偶zは base 行が同一式・I 帯行が
k(d)=floor((d+32)/4) の別式。

## 現在の根拠と限界

根拠は (i) probe box 992 行・70,680 点の生二重再帰との全点一致
（mismatch 0・T/P 重複 0）・(ii) box 外 spot 28,238 点 bad 0
（z<=40・d<=52・x=11 エッジ・R<=z+130）・(iii) マージ行回帰 2,412+26,015
比較不一致 0（K0832 単一トークン形式）・(iv) tail 回帰 14,880+84 点、の
125,017 点比較である。限界: 全称性（任意 z・任意 x>=11・任意 R）は未証明。
次段階の 12 チェック監査（A子=H(R-1;(x-1,11);z)・B子=K1141 の cand10
逐語転写・C子=1 xor cand11(z-1,x,R-1)・x=11 合流子 (10,11)≡(11,10)・
型機械 clip 窓 2y+2=24 の tight 判定・census z=0..79・x=11..70）で判定する。
3 トークン以上・y>=12 族・固定幅・q点版安定化長・標準 11×11 の勝敗は範囲外。
REFUTED-D10 型の実験とは異なり LOSS 証明を含まない。

## 横断観察（y=2..11・y=11 は fitting レベル）

- tail 開始族式 x+z+y+1 が y=2..11 の 10 族連続（y=11 は fit レベル）。
- 基底点 y 点仮説 {z+1,..,z+2y-1} が 11 例目（y=1..11・y=11 は fit レベル）。
- pin 統一式 pin=z+(d+3y)/2〔d≡y (mod 4)（奇z）・d≡y+2 (mod 4)（偶z）〕が
  7 族連続（y=5..11・y=11 は fit レベル）。y 奇族では pin 行 d が奇数。
- 対角行上端格子規則 cap=z+y-[z≡y (mod 2)] が y=11 の全 probe z で成立
  （両偶奇・y=2..10 全称＋y=11 fit）。
- clip 窓族式候補 2y+2（y=5..10 で 6 族連続 tight）の y=11 値 24 が band 下端
  として出現。±24/番兵±25 の tight 判定は次段階の型機械で行う。
- 偶 z 対角行の値1全欠如が 4 族連続。最終 pin 行 d=y の I[2y+z+1) 型が
  5 族連続（y=6/8/9/10/11）。
