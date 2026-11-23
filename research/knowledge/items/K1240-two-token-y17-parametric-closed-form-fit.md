---
id: K1240
title: "2トークン残余ゲーム y=17族のパラメトリック閉形式の全称候補（全z>=0・全x>=17・全R>=0・fit段階では有限観測）"
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases:
  - "two-token y=17 parametric closed-form fit, P17-fit"
  - "cand17 fitting and out-of-box spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 86,552 probe points; odd-y template mechanical translation from the published FINAL cand15, the promoted-universal y=15 table with Y=15->17)"
  - "seed law 5th consecutive one-shot test passed (cand11->13 / cand12->14 / cand13->15 / cand14->16 / cand15->17, odd-y series 11->13->15->17); FIRST 9-pin-row family (y-odd count law (y+1)/2 reaches 9); third consecutive family with zero in-box merge rows"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（box外マージ回帰15,495比較・境界行(35,17)/(36,18)のspot照合に使用。y=17ではbox内マージ行0行・z>=35が必要）
- type: extends
  target: K1235
  note: y=15族全称閉形式（K1235・昇格済み）の次の奇数y族。cand17初稿はy=15出版最終構造cand15（全称証明済み）のY+2機械翻訳（Y定数15→17・関数名変更のみ・コード本体は全式Y式で1行も変わらず）で生成し、probe 86,552点に一発一致（cand13→cand15に続き奇数y seed法則3連続目・全体で5連続一発一致）
- type: extends
  target: K1237
  note: y=16族全称閉形式（K1237・昇格済み）の次族。次段階全称検証器のB子は出版cand16の逐語転写（x=17合流子{16,17}≡{17,16}・B子逐語連鎖cand9..cand15の次リンク候補）。y=16全称で確定したマージ命題y=1..16全称の次（y=17版はfit level）
- type: extends
  target: K1143
  note: y=11族の奇数y型比較対象（th=2k+1ペア反復型・x偶行のtail・pin行数(y±1)/2系列の基点）。y=17でpin行数は奇z 9行・偶z 8行に到達（4点目）
- type: depends_on
  target: K1238
  note: 偶数y統一テンプレート機械検証の陰性対照知見（テンプレートは偶y特化・y=17は非適用）と整合: 本fitのseedは奇数y系列（cand13/cand15系列テンプレート）で、単一Yパラメトリック奇数yコードがy=13/15/17で再生するかは本fitの一致が新データ点
artifacts:
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/report.md
  role: proof
  note: fit段階の正本記録（86,552 probe点一発一致・box内tail assertion 18,848点・box外spot 41,465点（全選択行にx>=17機械assert・cand17.py selfcheckにも全行assert）・merge回帰15,495比較・tail raw 84点・事前予想の判定表・y=6..17横断則・fail-closed 8種と誠実記録〔z-odd pin d=-15のbox内到達不可能性を監査生成器自体のFAIL-CLOSEDで捕捉しゲート修正+spot生値照合に委任〕）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/cand17.py
  role: verifier
  note: 閉形式の正本cand17（in_T17値2表・in_P17値1表・Y=17・全行x>=17 assert）とprobe全点照合（86,552点・mismatch 0・overlap 0・初稿一発一致）。全称検証器は本ファイルを逐語転写
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/probe_y17.py
  role: verifier
  note: 生二重再帰probe（正準降順multiset memoization・z=0..30・x=17..z+33・R<=x+z+36=2y+2・992行86,552点を書き出す決定論的生成器・約8秒）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/spot_y17.py
  role: verifier
  note: box外spot（deep rows・bigz・edge・far d・tail raw・merge回帰・LRU cap 1.5M決定的退避・177秒・bad 0）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/make_audit_y17.py
  role: verifier
  note: 監査生成器（pin格子観測ゲート・box幾何独立再計算ゲート〔行欠落・注入・重複を含む改ざんを捕捉〕・in-box tail assertion・in-box merge 0行ゲート・fail-closed・3実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/output/audit.json
  role: data
  note: fit監査正本（SHA-256 c5593987…・自己文書化・probe/spot/merge/tail数値・sha256ピン・宣言commit eeeb1a8e+訂正amendment 82653b6f記録・z-odd pin d=-15 box内到達不可能性の誠実記録）
- path: research/log/2026-11-23-y17-two-token-skeleton-single-owner-note.md
  role: log
  note: fit段階の単一オーナー宣言ノート（commit eeeb1a8e・probe実行前に出版・事前横断予想12項目の全記録・対抗宣言チェック・box内マージ行0行とd>=18 tail 19点深の事前明記・点数算術訂正amendment 82653b6f）
- path: research/log/2026-11-23-two-token-y17-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・経緯・出版記録・次段階）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,17)、全z>=0・全x>=17・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand17）で
  分類する命題。現段階の証拠は有限fit（probe z=0..30・x=17..z+33・
  R<=x+z+36の992行86,552点・box内tail assertion 18,848点）とbox外spot
  41,465点・merge回帰15,495比較・tail raw 84点の観測のみで、全称は未証明
  （verify_y17_universal.pyの正本監査・型機械・censusは別宣言が必要）。
  系としてx<=z-18の単一トークン一致マージ命題y=17版とtail
  R>=x+z+18の(x+17) mod 2を含む（fit level）。標準11×11の空盤・二石root・
  S2 {59,60}・class 1/2/4は範囲外かつUNKNOWNのまま。3トークン以上・
  y>=18族・固定幅・q点版も範囲外。
evidence: >-
  fit段階の証拠（2026-11-23出版・単一オーナー宣言 eeeb1a8e 配下）:
  (1) 初稿一発一致: cand17初稿は出版cand15（K1235全称・Y=15）のY+2機械翻訳で、
  probe box全点に修正0（mismatch 0・overlap 0・値頻度 0:42,568 / 1:34,200 /
  2:9,784・値3なし）。seed法則5連続目（奇数y系列3連続目）。
  (2) 構造則の確定: 基底点17点{z+1,..,z+33}・z-odd I帯k=floor((d+3y+1)/4)
  th=2k+1ペア反復・同式base行・z-even I帯k=floor((d+3y-1)/4)・z-even base行
  同式・pin格子統一式pin=z+(d+51)/2（奇z 9行d≡1 (mod 4)・偶z 8行d≡3 (mod 4)・
  FIRST 9-pin-row family・「pinスロット=th-1」7族連続候補・最終pin行d=17=yの
  I[35)型12族目候補）・対角cap z+16/z+17・偶z対角値1全欠如10族目候補・
  掃引d=18・定常pin z+34/z+35・band下端2y+2=36・tail開始x+z+18値(x+17) mod 2。
  (3) 回帰: マージ命題y=17版（K0832単一トークン）15,495比較不一致0・旧来の
  境界行(35,17)/(36,18)の生値一致・tail raw 84点一致。
  (4) 決定性・fail-closed: probe_rows.txt 3回再生成（同一cwd2回+隔離
  tree/cwd/HOME+env -i+PYTHONHASHSEED=random1回）byte-identical
  （SHA-256 248d5249…）・audit.json 3実行byte-identical（c5593987…）・
  fail-closed 8種全捕捉（probe値改ざん・pin値改ざん・Y定数改ざん17→16
  〔mismatch 3,764〕・pin mod4クラス改ざん・probe行欠落（幾何ゲート）・
  重複行注入（幾何ゲート）・z-odd pin d=-15 box内到達不可能性の監査生成器
  FAIL-CLOSED〔誠実記録・ゲートをbox内可観測8行に修正しd=-15をspot
  deep row (33,18)生値照合に委任〕・復元byte-identical）。
---

## 命題・範囲

すべての z>=0・x>=17・R>=0 に対して H(R;(x,17);z) = cand17(z,x,R) が成り立つ
（**status: observed・fit段階・全称は未証明**）。正本は
[実験dir](../../experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/report.md)
で、cand17.py が閉形式の正本実装である。本項の証拠は
(1) probe box（z=0..30・x=17..z+33・R<=x+z+36）生二重再帰 992 行 86,552 点の
全点一致（初稿一発・修正 0・T/P 重複 0）、(2) box 内 tail assertion
R>=x+z+18 → (x+17) mod 2 の 18,848 点一致、(3) box 外 spot 41,465 点
（全 9 奇z pin 行・全 8 偶z pin 行を個別行として選択した deep rows・bigz
z=31..40・x=y=17 edge・far d∈{34,45,56}）、(4) merge 回帰 15,495 比較
（K0832 単一トークン閉形式）+ 境界行 (35,17)/(36,18) の生値一致、
(5) tail raw 84 点、の計 143,596 点比較不一致 0 である。

## 主要構造（fit で確定した構造則・有限範囲）

y=17 は奇数 y 族（y=9/11/13/15 と同型）で、値1無限帯・tail は x 偶の行。
基底点 17 点 {z+1,...,z+33}・マージ行 x<=z-18（box 内 0 行・3 族連続）・
奇z I 帯行 k(d)=floor((d+3y+1)/4)・th=2k+1 ペア反復型（y 偶族掃引型との
偶奇分離 17 族目）・偶z I 帯行 k=floor((d+3y-1)/4)（7 族目候補）・
base 行 k=floor((d+3y+1)/4)（8 族目候補・偶z d=17 で k=17=Y 飽和）・
pin 格子統一式 pin=z+(d+3y)/2（o_pin∈[18,34]・奇z 9 行 d≡1 (mod 4)
{-15,...,17}・偶z 8 行 d≡3 (mod 4) {-13,...,15}・**初の 9 pin 行族**・
「pin スロット=th-1」7 族目・最終 pin 行 d=17=y の I[2y+z+1)=I[35) 型
12 族目候補）・掃引行 d=18・定常 pin z+34（奇z）/z+35（偶z）・
band 下端 2y+2=36・tail 開始 x+z+18・tail 値 (x+17) mod 2・
偶z 対角行 d=-17 の値 1 全欠如（10 族目候補）・対角 cap z+16/z+17
（奇 y 族式の向き）。標準の信頼境界（選択肢分解・mex 恒等式・有限型空間）
は y=5..16 出版系列と同一の機械分類に依存し、全称段階で初めて検証される。

## fit の工芸的観察（fitting なしの一発一致）

**初稿一発一致（修正 0）**: cand17 初稿は y=15 の出版最終構造（cand15・K1235
全称昇格済み）を seed とした Y+2 機械翻訳（Y 定数の差し替えと関数名変更のみ）で、
probe 86,552 点に修正 0 で一致。「直前の出版最終構造 seed による外挿が一発一致する」
は **5 連続**（cand11→13・cand13→15・cand15→17〔奇〕・cand12→14・cand14→16〔偶〕）
となり、横断法則一般補題化レーンの主要リスク（族式の y 依存跳躍）をさらに低減した。
y=15・y=16 に続き 3 族連続の「box 内マージ行 0 行」族でもあり、事前宣言どおり
マージ回帰は全面 box 外。宣言ノートの点数算術誤り（81,902 → 86,552）は
amendment 82653b6f で訂明記録した。

## 誠実記録（z-odd pin d=-15 の box 内観測可能性境界）

初回の監査生成は FAIL-CLOSED した: 事前登録した奇z pin 格子 9 行のうち
d=-15 は宣言 box（z<=30・x>=17）では幾何学的に到達不可能（x=z-15>=17 は
z>=32 を要求）であり、in-box 観測は 8 行までしか存在しない。これは fail-closed
設計が想定どおり機能した捕捉であり、ゲートを box 内可観測 8 行に修正し、
9 行目（d=-15）を spot deep row (33,18) の生値全点照合（R<=130 bad 0・
pin R=51 値 2）に明示委任して本 fit で全 9 行を検証した。経緯は
output/audit.json（in_box_observability_note）と report が正本。

## 解釈規約・次段階

有限 fit は有限観測の機械的証拠であり全称主張ではない。全称段階
（verify_y17_universal.py・A子 H(R-1;(x-1,17);z)〔x=17 行は合流子{16,17}≡
{17,16} で cand16(z,17,R-1)〕・B子 出版 cand16 逐語転写・C子 1 xor
cand17(z-1,x,R-1)・型機械 clip 窓 2y+2=36 の tight 判定〔13 族目候補〕・
census）は**別の単一オーナー宣言が必要**。標準 11×11 空盤・二石 root
{49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
3 トークン以上・y>=18 族・固定幅・q 点版安定化長は範囲外。
