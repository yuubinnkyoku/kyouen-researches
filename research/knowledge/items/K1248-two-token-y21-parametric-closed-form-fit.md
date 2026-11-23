---
id: K1248
title: "2トークン残余ゲーム y=21族パラメトリック閉形式候補 cand21 の fitting と box 外 spot 検証（observed・全称は未証明）"
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases:
  - "two-token y=21 parametric closed-form fit, P21-fit"
  - "cand21 fitting and out-of-box spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 112,530 probe points; odd-y mechanical translation from the published FINAL cand19, the universally proved y=19 table (K1243), Y=19->21; reverse rename verified byte-identical to the published cand19 code in both directions)"
  - "seed law 9th consecutive one-shot test passed (odd-y pair series 11->13->15->17->19->21 5-for-5; THIRD consecutive proved-seed extrapolation after cand11->13 via K1143 and cand18->20 via K1242); z-odd pin rows reach 11 in a single parity for the first time ((y+1)/2=11, d==1 mod 4 {-19..21}); FIVE out-of-box pin rows (3 z-odd + 2 z-even, both series-firsts; raw-verified by spot deep rows (41,22)/(37,22)/(33,22)/(38,21)/(34,21)); 7th consecutive family with zero in-box merge rows (out-of-box merge regression 117 rows / 17,835 comparisons bad 0); 3-row k=Y census {20,21,21} odd-family shape (y=17 {16,17,17}, y=19 {18,19,19}); K0914 z=6,y=21 PROVED-slice three-way cross-check: raw probe vs proved T_21/P_21 boxes vs cand21 on ALL 2,268 in-box slice points bad 0; total 177,304 comparison points bad 0"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（box外マージ回帰117行17,835比較・境界行(43,21)/(44,22)のspot照合に使用。y=21ではbox z<=30内にマージ行は存在せずz>=43が必要・7族連続のbox内マージ0行）
- type: extends
  target: K1243
  note: seed。cand21初稿は出版cand19（K1243 proved・全称確定）のY=19→21機械翻訳（Y定数・in_T21/in_P21/cand21/b21 rename・docstring・行内コメント値の再計算のみでコード本体は全式Y式で1行も変わらず・逆renameが出版cand19コード本体とbyte同一になることを両方向で機械検証）で生成し、probe 112,530点に一発一致。証明済みseed外挿は3連続目（cand11→13〔K1143 proved当时〕・cand18→20〔K1242 proved〕・cand19→21）。2トークン族全称はy=1..19完結→y=21は第21族のfit段階
- type: extends
  target: K1246
  note: 隣接偶数y族（y=20・fit level observed）との対比データ点。pin mod-4クラス交代（y=19: 3/1・y=20: 0/2・y=21: 1/3）・box外pin個数系列（y=20の2+2→y=21の3+2）・k=Y census偶奇形状分離（y=20の4行→y=21の3行）・band下端系列42→44。y=21全称段階のB子は出版cand20の逐語転写（x=21合流子{20,21}≡{21,20}）だがcand20は全称未証明のためy=20全称audit（別宣言）に連鎖する
- type: extends
  target: K1240
  note: 奇数y族3行k=Y census形状の第3データ点（y=17 {16,17,17}・y=19 {18,19,19}・y=21 {20,21,21}・奇数y族式z-odd I行k=floor((d+3y+1)/4)のペア反復th・z-odd base同式・偶z I行k=floor((d+3y-1)/4)・band_base/band_int分離・tail x偶行のy=21 fit level継続観測）
- type: extends
  target: K1143
  note: 「pinスロット=th-1」（奇z I行）と偶z base行2k+1 slot則（y=11..20の10族連続に続き11族目として奇z 11 pin行・偶z 10 pin行すべてで算術的に成立）
- type: related
  target: K0914
  note: z=6,y=21証明済み切片（全称証明・A/B/C選択肢署名表＋Theorem T＋一般tail定理）との交差検証。宣言で補助的と事前登録し、実行では出版T_21(x)/P_21(x)表を監査生成器へ転写してprobe box内z=6切片（x=21..47・R<=x+50）全2,268点の三点照合（生probe値vs証明済み分類・cand21 vs証明済み分類）をfail-closed gateで実施しbad 0。ラダー{1,3,5}・pin(21,6)@45・(25,6)@47・掃引x=28の{49,51,53,55}・定常R=49・tail R>=x+28→(x+21) mod 2が宣言予想・K0914出版表・生値で完全一致（独立裏付け・全称ではない・2レーンの相互補強の記録）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/report.md
  role: proof
  note: fit段階の正本記録（112,530 probe点一発一致・box内tail assertion 25,668点・box外spot 46,861点（全11奇z pin行・全10偶z pin行の個別行選択・5 box外pin行(41,22)/(37,22)/(33,22)/(38,21)/(34,21)のR<=130生値照合・全選択行にx>=21機械preflight assert）・merge回帰117行/17,835比較・tail raw 78点・K0914三点交差検証2,268点bad 0・事前横断予想の判定表（全項目一致・amendment不要）・誠実記録4点（probe docstring点数訂正110,148→112,530・sandbox制約下のspotブロック別再実行・改ざんバッテリno-op 2種の正直記録・pinned秒数）・y=12..21横断判定）
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/cand21.py
  role: verifier
  note: 閉形式の正本cand21（in_T21値2表・in_P21値1表・Y=21）とprobe全点照合（112,530点・mismatch 0・overlap 0・初稿一発一致）。出版cand19のY=19→21機械翻訳でコード本体は1行も変わっていない（逆rename byte同一を両方向で機械検証・結果docstring差し替え後に再検証PASS）
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/probe_y21.py
  role: verifier
  note: 生二重再帰probe（正準降順multiset memoization・z=0..30・x=21..z+41・R<=x+z+44=2y+2拡張cap・1,116行112,530点を書き出す決定論的生成器・3回再生成byte-identical incl. 隔離tree+env -i+PYTHONHASHSEED=random）
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/spot_y21.py
  role: verifier
  note: box外spot（全11奇z pin行・全10偶z pin行を個別行選択したdeep rows R<=130・bigz z=31..40・x=y=21 edge・far d∈{42,53,64}・tail raw・merge回帰117行/17,835・LRU cap 1.5M決定的退避・run1全実行302.5秒）
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/make_audit_y21.py
  role: verifier
  note: 監査生成器（pin格子観測ゲート〔box内可観測8+8行〕・box幾何独立再計算ゲート（宣言機械事前算出1,116行/112,530点と厳密照合）・値ヒストグラム事前予想等価ゲート{0:55466,1:46196,2:10868}・逐行整合性ゲート〔x>=21・d再計算・merge flag・RLE長x+z+44〕・in-box tail depth 23点/行25,668点ゲート・in-box merge 0行ゲート・偶z対角値1 census（box内幾何学的vacuityを明記）・K0914出版T_21/P_21表転写によるz=6切片全2,268点三点照合fail-closedゲート・fail-closed・最終版4回実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/spot_chunk_rerun.py
  role: verifier
  note: spot決定性再実行driver（sandboxの単一実行300秒上限と環境リセット下で、出版spot_y21.pyのmain()を一意マーカーでバイトスライスしdeep/bigz/edge/far/tailmergeの各ブロックをexec再実行。run2/run3で全ブロック集計・LRU CacheInfo行がrun1と完全一致）
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/output/audit.json
  role: data
  note: fit監査正本（SHA-256 b61e6581…e2982・自己文書化・probe/spot/merge/tail数値・sha256ピン〔probe_rows bd9482c7…1c6cbf0・cand21 10d8e495…・probe_y21 8f79a9ef…・spot_y21 04440247…〕・宣言commit 2d3aeac2記録・K0914三点照合2,268点bad 0・5 box外pin行〔3+2〕の族初と誠実記録の記録）
- path: research/log/2026-11-23-y21-two-token-skeleton-single-owner-note.md
  role: log
  note: fit段階の単一オーナー宣言ノート（commit 2d3aeac2・probe実行前に出版・事前横断予想の全記録・対抗宣言チェック・box幾何1,116行/112,530点・総比較点177,304の出版前機械算出・逆rename両方向検証の事前登録）
- path: research/log/2026-11-23-two-token-y21-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・宣言・経緯・誠実記録4点・出版記録・次段階）
---

## 命題（候補・有限範囲で確定・全称は未証明）

すべての z>=0・x>=21・R>=0 に対して H(R;(x,21);z) = cand21。ここで cand21 は
z 偶奇別のパラメトリック T/P 集合表（`cand21.py` が正本・Y=21・**奇数 y 型で値1無限帯・tail は x 偶行**・
d = x-z・off = R-z）であり、出版 cand19（K1243 proved）の Y=19→21 機械翻訳に等しい
（コード本体 1 行も変わらず・逆 rename byte 同一を両方向で機械検証済み）。

本項は fit 段階（status observed）であり、全称証明（正本検証器・型機械・census を含む
verify_y21_universal.py・B子は出版cand20の逐語転写〔cand20は全称未証明のためy=20全称に連鎖〕）は
範囲外・別宣言が必要である。

## 対象範囲（fit 段階の有限証拠）

- probe box: z=0..30・x=21..z+41・R<=x+z+44（=2y+2）の生二重再帰 1,116 行・112,530 点
  （cand21 全点一致・mismatch 0・T/P 重複 0・値頻度 0:55,466/1:46,196/2:10,868・値 3 なし）
- box 内 tail assertion R>=x+z+22→(x+21) mod 2: 25,668 点 bad 0
- box 内マージ行 0 行（y=21 では x<=z-22 に z>=43 が必要・7 族連続）
- box 外 spot 46,861 点 bad 0（deep 44 行/5,720 点〔全 21 pin 行の個別行選択・5 box 外 pin 行
  (41,22)/(37,22)/(33,22)/(38,21)/(34,21) の R<=130 生値照合〕・bigz 280 行/34,510 点・edge 25 行/4,075 点・
  far 18 行/2,556 点・全選択行 x>=21 機械 assert）
- tail raw 回帰 6 行 78 点 bad 0・merge 回帰 117 行 17,835 比較 bad 0
  （z∈{43,50,57,64,74,87}・x=21..z-23・R<=x+z+43）・マージ境界行 (43,21)/(44,22) 生値一致
- K0914（z=6,y=21 証明済み切片）との三点交差再検査 2,268 点 bad 0（fail-closed gate）
- 合計 177,304 点比較・不一致 0（宣言ノートの出版前機械算出と全数値一致）

## 現在の根拠

上記有限範囲の全点照合（宣言ノート 2d3aeac2 の事前横断予想全項目が fit level で一致・修正 0・amendment 不要）、
probe_rows.txt 3 回再生成 byte-identical（SHA-256 bd9482c7…1c6cbf0・内1回は隔離tree+env -i+PYTHONHASHSEED=random）、
audit.json 最終版 4 回実行 byte-identical（SHA-256 b61e6581…e2982）、spot は run1 全実行（302.5 秒）+
run2/run3 ブロック別再実行（出版スクリプトの main() バイトスライス・sandbox 制約のため）の 3 実行で
全ブロック集計・LRU CacheInfo 行が完全一致、fail-closed バッテリ 20 変種で有効改ざん 16 種全検出
（no-op 2 種は正直記録し有効版で再設計検出）、出版最終構造 seed 法則 9 連続一発一致
（奇数 y 系列 11→13→15→17→19→21 の 5 連続・証明済み seed 外挿 3 連続目）。

## 構造（y=21 で新たに観測された族初構造・fit level）

- 奇z pin 行数 (y+1)/2 = 11 が単一偶奇側で系列初の到達点（d≡1 (mod 4) {-19,-15,-11,-7,-3,1,5,9,13,17,21}）
- box 外 pin 行 5 行（奇z 3 行 d=-19/-15/-11〔z>=41/37/33〕＋偶z 2 行 d=-17/-13〔z>=38/34〕）は
  合計も単一偶奇側 3 行も系列初（y=17: 1・y=18: 1+1・y=19: 2+1・y=20: 2+2）
- 偶z base 上端 d=21=Y 飽和の 6 族連続（y=16..21）・奇z base d=Y-1=20 飽和の 8 族連続（y=14..21）
- k=Y=21 census 3 行 {20,21,21} の奇数族 3 行形状（y=17/19 と同型・偶数族 4 行形状との偶奇分離継続）
- band 下端 2y+2=44 の 9 データ点目・偶z 対角行の値 1 全欠如 14 族目候補
  （spot deep (42,21) 全行照合が正本証拠・probe box は d>=-9 のみで box 内対角行は幾何学的に存在しない）

## 限界・範囲外の明示

本項は有限 fitting と spot 検証のみであり、y=21 の全称は含まない（B子 cand20 逐語転写は
cand20 が全称未証明のため y=20 全称 audit に連鎖する・両方別宣言必須）。
seed 法則・横断族式の全称は一般補題化レーンの対象であり、本項はその奇数 y 系列第 5 ペア目の
fit level データ点として寄与する。
標準 11×11 の空盤勝敗・二石 root・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま一切言及しない。
3 トークン系（K1247 仮採番レーン）・y>=22 族・固定幅・q 点版安定化長・fold 系・n11 batch 系・
inversive arc 系（K1250/K1251/K1252/K1253）は対象外。
