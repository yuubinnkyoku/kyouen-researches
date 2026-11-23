---
id: K1246
title: "2トークン残余ゲーム y=20族パラメトリック閉形式候補 cand20 の fitting と box 外 spot 検証（observed・全称は未証明）"
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases:
  - "two-token y=20 parametric closed-form fit, P20-fit"
  - "cand20 fitting and out-of-box spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 105,710 probe points; even-y mechanical translation from the published FINAL cand18, the promoted-universal y=18 table with Y=18->20; reverse rename verified byte-identical to the published cand18 code in both directions)"
  - "seed law 8th consecutive one-shot test passed (cand11->13 / cand12->14 / cand13->15 / cand14->16 / cand15->17 / cand16->18 / cand17->19 / cand18->20, even-y pair series 12->14->16->18->20 proven-seed translation no.2 since cand11->13); FIRST family reaching 10 pin rows on BOTH parities (odd z d≡0 mod 4 {-16..20}, even z d≡2 mod 4 {-18..18}); most out-of-box pin rows in the series (4 rows, first family with 2 on EACH parity side, covered by spot deep raw-value checks (37,21)/(33,21)/(38,20)/(34,20)); FIRST 21-row th sweep 21..41; 4-row k=Y census {Y-2,Y}/{Y-1}/{Y} same shape as y=16/18; 6th consecutive family with zero in-box merge rows (full out-of-box merge regression 18,219 bad 0); K0913 z=6,y=20 proven-slice cross-check bad 0; total 165,061 comparison points bad 0"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（box外マージ回帰18,219比較・境界行(43,22)/(42,21)のspot照合に使用。y=20ではbox z<=30内にマージ行は存在せずz>=42が必要）
- type: extends
  target: K1242
  note: seed。cand20初稿は出版cand18（K1242 promoted・全称確定）のY=18→20機械翻訳（Y定数・in_T20/in_P20/cand20/b20 rename・docstring・行内コメント値の再計算のみでコード本体は全式Y式で1行も変わらず・逆renameが出版cand18コード本体とbyte同一になることを両方向で機械検証）で生成し、probe 105,710点に一発一致。seedが全称証明済み族なのはcand11→13（K1143 proved当时）以来2度目
- type: extends
  target: K1243
  note: 隣接奇数y族（y=19・observed→proved済み・2トークン族の全称y=1..19完結）の次の族（第20族）。y=20全称段階のB子は出版cand19（K1243 proved）の逐語転写（x=20合流子{19,20}≡{20,19}でy=19族x=19行と同一状態）の予定（全称は本項の範囲外・別宣言が必要）
- type: extends
  target: K1238
  note: even-y統一テンプレートの第6データ点（偶数y族式〔z-odd I行k=floor((d+3y+2)/4)連続掃引・base行同式floor((d+3y+1)/4)・偶z I行k=floor((d+3y-1)/4)・pin格子統一式・pin行数y/2両偶奇・単一band則・tail x奇行〕のy=20でのfit level継続観測）
- type: extends
  target: K1143
  note: 「pinスロット=th-1」（奇z）と偶z 2k+1 slot則の行型比較基点（y=11..19の9族連続に続き10族目として両偶奇10 pin行すべてで算術的に成立）
- type: related
  target: K0913
  note: z=6,y=20証明済み切片（全称証明）との交差検証。probe生値のz=6行26行（x=20..45・R<=x+48）をK0913出版署名（ラダー{1,3,5}・pin(20,6)@43・pin(24,6)@45・掃引x=27でR∈{47,49,51,53}・定常R=47）とtail族式のz=6適用に対して機械再検査してbad 0。cand20は証明済み境界z=6とfit levelで完全一致（独立裏付け・全称ではない・2レーンの相互補強の記録）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/report.md
  role: proof
  note: fit段階の正本記録（105,710 probe点一発一致・box内tail assertion 23,870点・box外spot 41,054点（全10奇z pin行・全10偶z pin行の個別行選択・4 box外pin行(37,21)/(33,21)/(38,20)/(34,20)のR<=130生値照合・全選択行にx>=20機械preflight assert）・merge回帰18,219比較・tail raw 78点・K0913交差検証・事前予想の判定表・y=12..19横断則・fail-closed 15変種（有効改ざん12種全検出・no-op 3種の正直記録）・誠実記録2点（飽和連続数ラベル・deep 44行のハンドオフ再構成）・実行環境フルリセット1回の記録）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/cand20.py
  role: verifier
  note: 閉形式の正本cand20（in_T20値2表・in_P20値1表・Y=20・Y==20ハードassert）とprobe全点照合（105,710点・mismatch 0・overlap 0・初稿一発一致）。出版cand18のY=18→20機械翻訳でコード本体は1行も変わっていない（逆rename byte同一を両方向機械検証）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/probe_y20.py
  role: verifier
  note: 生二重再帰probe（正準降順multiset memoization・z=0..30・x=20..z+39・R<=x+z+40を超えるx+z+42=2y+2拡張cap・1,085行105,710点を書き出す決定論的生成器・約13秒）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/spot_y20.py
  role: verifier
  note: box外spot（全10奇z pin行・全10偶z pin行を個別行選択したdeep rows R<=130・bigz z=31..40・x=y=20 edge・far d∈{40,51,62}・tail raw・merge回帰18,219・LRU cap 1.5M決定的退避・264.6秒〔3全実行264.6/270.6/262.2で全ブロック数値一致〕）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/make_audit_y20.py
  role: verifier
  note: 監査生成器（pin格子観測ゲート〔box内可観測8+8行〕・box幾何独立再計算ゲート（宣言機械事前算出1,085行/105,710点と厳密照合）・逐行整合性ゲート〔x>=20・d再計算・merge flag・RLE長x+z+42〕・in-box tail assertion・in-box merge 0行ゲート・偶z対角値1 census・fail-closed・4実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/output/audit.json
  role: data
  note: fit監査正本（SHA-256 63f0fad3…71ddd・自己文書化・probe/spot/merge/tail数値・sha256ピン〔probe_rows 88981b77…62262〕・宣言commit cc20473c記録・K0913交差検証bad 0・4 box外pin行〔2+2〕の族初と誠実記録2点の記録）
- path: research/log/2026-11-23-y20-two-token-skeleton-single-owner-note.md
  role: log
  note: fit段階の単一オーナー宣言ノート（commit cc20473c・probe実行前に出版・事前横断予想の全記録・対抗宣言チェック・box幾何1,085行/105,710点・総比較点165,061の出版前機械算出・逆rename両方向検証の事前登録）
- path: research/log/2026-11-23-two-token-y20-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・宣言・経緯・誠実記録3点・出版記録・次段階）
---

## 命題（候補・有限範囲で確定・全称は未証明）

すべての z>=0・x>=20・R>=0 に対して H(R;(x,20);z) = cand20。ここで cand20 は
z 偶奇別のパラメトリック T/P 集合表（`cand20.py` が正本・Y=20・偶数 y 型で値1無限帯は
x 奇行・d = x-z・off = R-z）であり、出版 cand18（K1242 promoted）の Y=18→20 機械翻訳に等しい
（コード本体 1 行も変わらず・逆 rename byte 同一を両方向で機械検証済み）。

本項は fit 段階（status observed）であり、全称証明（正本検証器・型機械・clip 窓 tight 判定・
census を含む verify_y20_universal.py）は範囲外・別宣言が必要である。

## 対象範囲（fit 段階の有限証拠）

- probe box: z=0..30・x=20..z+39・R<=x+z+42（=2y+2）の生二重再帰 1,085 行・105,710 点
  （cand20 全点一致・mismatch 0・T/P 重複 0・値頻度 0:52,068/1:43,045/2:10,597・値 3 なし）
- box 内 tail assertion R>=x+z+21→(x+20) mod 2: 23,870 点 bad 0
- box 内マージ行 0 行（y=20 では x<=z-21 に z>=42 が必要・6 族連続）
- box 外 spot 41,054 点 bad 0（deep 44 行/5,720 点〔全 20 pin 行の個別行選択・4 box 外 pin 行
  (37,21)/(33,21)/(38,20)/(34,20) の R<=130 生値照合〕・bigz 240 行/28,800 点・edge 25 行/4,050 点・
  far 18 行/2,484 点・全選択行 x>=20 機械 assert）
- tail raw 回帰 6 行 78 点 bad 0・merge 回帰 18,219 比較 bad 0
  （z∈{42,49,56,63,73,86}・x=20..z-22・R<=x+z+41）・マージ境界行 (43,22)/(42,21) 生値一致
- K0913（z=6,y=20 証明済み切片）との交差再検査 26 行 bad 0
- 合計 165,061 点比較・不一致 0

## 現在の根拠

上記有限範囲の全点照合（宣言ノート cc20473c の事前横断予想全項目が fit level で一致・修正 0）、
probe_rows.txt 4 回再生成 byte-identical（SHA-256 88981b77…62262）・
audit.json 4 実行 byte-identical（SHA-256 63f0fad3…71ddd）・spot 3 全実行の数値一致・
fail-closed バッテリ 15 変種で有効改ざん 12 種全検出（no-op 3 種は電池設計の誤りとして
正直記録し有効版で再検出）・出版最終構造 seed 法則 8 連続一発一致
（偶数 y 系列 12→14→16→18→20・証明済み seed 外挿は cand11→13 以来 2 度目）。
決定性の再生成は実行環境フルリセット 1 回をはさんで実施されており、出版数値は
すべてリセット後の再生成正本由来である（report・audit に記録）。

## 構造（y=20 で新たに観測された族初構造・fit level）

- pin 行数 y/2=10 が両偶奇とも 10 行に達する初の族（奇z d≡0 mod 4{-16,...,20}・
  偶z d≡2 mod 4{-18,...,18}・box 外 pin 4 行〔2+2〕は系列最多かつ両側 2 行同時は系列初）
- 奇z I 帯行 th 21..41 の初の 21 行連続掃引（偶数 y 族の掃引長線形則 6 データ点目）
- k=Y=20 飽和 census 4 行 {Y-2,Y}/{Y-1}/{Y}（y=16/18 と同一の偶数族 4 行形状・
  奇数族 3 行形状 y=17/19 との偶奇分離の継続）
- 偶z 対角行の値 1 全欠如 13 族目候補・band 下端 2y+2=42 の 8 データ点目・
  偶数 y 単一 band 則の 6 連続目の観測（y=10/12/14/16/18/20）

## 限界・範囲外の明示

本項は有限 fitting と spot 検証のみであり、y=20 の全称（A子・B子 出版 cand19 逐語転写・
C子・型機械 clip 窓 2y+2=42 の tight 判定〔16 族目候補〕・census）は含まない。
seed 法則・横断族式の全称は一般補題化レーンの対象であり、本項はその偶数 y 系列第 6 データ点
（fit level）として寄与する。
標準 11×11 の空盤勝敗・二石 root・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま一切言及しない。
3 トークン以上・y>=21 族・固定幅・q 点版安定化長・fold 系・n11 batch 系（Part BL 系）・
inversive arc 系（K1250/K1251/K1252/K1253）は対象外。
