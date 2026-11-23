# y=19 two-token パラメトリック閉形式 fit 実行記録（2026-11-23・高速レーン）

## 選定

K1242 fit 出版が指摘した次候補の第一位として、**y=19 族 fit** を着手した。
理由: (a) 出版最終構造 seed 法則の**第7テスト**・奇数 y ペア系列（11→13→15→17→19）は
**第4ペア目**で、横断法則一般補題化レーンの跳躍リスク評価の最優先材料、
(b) 奇z pin 行数 (y+1)/2 が**10 行に達する初の族**（y=17 で 9 行の次の行数則判定点）、
(c) 奇z pin 行数 (y+1)/2=10・box 外 pin 行 3 行・複数箇所の k=Y 到達・偶z base 上端の飽和成否・
  band_base/band_int 分離の y=19 継続など新規構造判定を多数含む
  （結果として: 宣言の偶z base 行域記述に行域算術の誤りが残っており、fit の機械 census がこれを捕捉・訂正した。
  判定点としての価値は「宣言 meta と族式の不一致を機械が検出するか」にもあったことになる）、
(d) y=16/17/18 に続き box 内マージ行 0 行が 5 族連続するかの判定材料、
(e) 単独で完結して出版可能（宣言→fit→spot→監査→item→README、K1242 と同型）、
(f) 宣言時点の main に y=19 族着手・対抗宣言が存在しないことを確認済み（観測 HEAD
fa789e27・list_commits 100 件で y19 系コミット 0・K1243 は空番を 404 で 2 回確認）。
K番号は K1243（宣言ノートで名指し後、items push 直前に最新 main で再確認予定）。

## 宣言（probe 実行前に先行出版）

- 宣言ノート: [2026-11-23-y19-two-token-skeleton-single-owner-note.md](2026-11-23-y19-two-token-skeleton-single-owner-note.md)
  （commit `c15b1c3f`・probe 実行前に出版・事前横断予想を全登録）
- 事前横断予想（seed cand17〔K1240 promoted・全称確定〕の Y+2 機械翻訳初稿で修正 0 を予想・
  基底点 19 点・マージ行 x<=z-20〔**y=19 では box 内マージ行 0 行・z>=39 が必要、事前明記**〕・
  pin 格子統一式 pin=z+(d+57)/2 ∈[20,38]・奇z 10 行 d≡3 (mod 4) {-17,...,19}・偶z 9 行 d≡1 (mod 4)
  {-15,...,17}・**初の 10 行 pin 行と box 外 pin 3 行（奇z d=-17/d=-13 の 1 側 2 行は族初）の
  spot deep row (37,20)/(33,20)/(34,19) への委任を事前設計**・「pin スロット=th-1」/偶z 2k+1 slot
  9 族目候補・最終 pin 行 d=19=y の I[39,inf) 型 14 族目候補・奇z I 行 k=floor((d+58)/4)・
  th 2k+1 ペア反復（奇数 y 型）・偶z I 行 k=floor((d+56)/4) 8 族目候補・奇z base d=18 飽和 k=Y の
  「2 箇所 k=Y は族初」・偶z base 行域「17 行・d∈[-17,17]・上端 d=17 非飽和」（y=17 との対照を予想）・
  掃引 d=20・定常 pin z+38/z+39・band 下端 2y+2=40・**band_base/band_int 分離（奇数 y 型）**・tail 開始 x+z+20 値
  (x+19) mod 2）を probe 実行前に全部登録した。判定結果: **族式・閉形式は全項目 fit level で一致（修正 0）**したが、
  **宣言の偶z base 行域記述（17 行・[-17,17]・上端非飽和・2 箇所 k=Y 族初）は fit の機械 census により訂正**
  （実態: 19 行・d∈[-17,19]・上端 d=19=Y で k=Y 飽和・k=Y は 3 行で出版 y=17 と同型。amendment を出版・後述）。
- 宣言 box: z=0..30・x=19..z+37・R<=x+z+40（**=2y+2。y=18 fit の x+z+38 から R cap を
  さらに +2 拡張し、band 下端 2y+2=40 を box 内で直接観測する新 convention**・
  7 データ点目 28/30/32/34/36/38/40）。点数 99,107・行 1,054 は**宣言ノートの出版前に機械算出して
  記載**したため amendment 不使用（y=17 の点数算術誤り訂正 82653b6f の教訓を適用）。
- 宣言の観測 HEAD は fa789e27（K1242 出版完了時点）。対抗 y19 宣言なしを list_commits 100 件で確認。

## 実行と結果（すべて決定論的・正本は実験dir）

- cand19 初稿（出版最終構造 cand17〔K1240 promoted・全称確定〕の Y+2 機械翻訳・
  コード本体は Y 定数と関数名以外は 1 行も不改変）:
  **probe 1,054 行 99,107 点に一発完全一致**（修正 0・mismatch 0・T/P 重複 0・値頻度
  0:48,800/1:39,981/2:10,326・値 3 なし・約 9.6 秒）。
  **出版最終構造 seed 法則 7 連続**（cand11→13・cand13→15・cand15→17・cand17→19〔奇・4 連続〕・
  cand12→14・cand14→16・cand16→18〔偶・3 連続〕）。
- box 内 tail assertion（R>=x+z+20→(x+19) mod 2）: **22,134 点 bad 0**（R cap x+z+40 で
  1 行あたり 21 点深・偶行 tail の直接 box 内確認）。box 内マージ行: **0 行**
  （宣言の事前明記どおり・5 族連続）。
- box 内 pin census（監査 fail-closed gate）: box 内可観測の奇z 8 行・偶z 8 行すべて値 2 で
  in-box 観測。偶z 対角行値 1 census: 計数 0（12 族目候補）。
- box 外 spot（`spot_y19.py`・LRU cap 1.5M・230.0 秒・正本 docstring 修正後の再実行で点数同一）: **44,597 点 bad 0**。
  特に**全 10 奇z pin 行・全 9 偶z pin 行を個別行として選択**し、**3 box 外 pin 行
  (37,20) d=-17・(33,20) d=-13・(34,19) d=-15 は full R<=130 生値照合で pin R 値 2 を
  含めて確認**（box 外 pin 3 行・1 側 2 行の族初の事前委任設計どおり・行数則 10/9 の直接検証）。
  両対角・奇z skew 行・偶z I 行（d=0・d=18 端点）・base 行（奇z d=18 飽和行・偶z d=17 非飽和行）・
  掃引 d=20 両偶奇・定常行両偶奇・マージ境界 (41,21)/(40,20) も全行選択。
  全選択行に x>=19 の機械 preflight assert を実装（y17/y18 と同じ gate）。
- merge 回帰 cand19 vs K0832（z∈{39,46,53,60,70,83}・x=19..z-21・R<=x+z+39）**16,665 比較 bad 0**
  （5 族連続の全面 box 外マージ回帰）。境界行 (41,21)/(40,20) の生値一致も spot deep 内で確認。
- tail raw 回帰: 6 行 78 点 bad 0。
- 決定性: probe_rows.txt 4 回再生成（同一 cwd 3 回 + 隔離 tree/cwd/HOME + env -i +
  PYTHONHASHSEED=random）すべて byte-identical（SHA-256 2a57d075…855a8）。
  audit.json 4 実行 byte-identical（SHA-256 a1ddd7f1…65b14・docstring 修正後に取り直し）。
  合計 **160,447 点比較・不一致 0**（99,107 + 44,597 + 78 + 16,665）。
- fail-closed 改ざん試験: **最終正本に対して 10 変種すべて検出**（probe 値・pin 値・Y 定数 19→18〔ハード assert〕・
  監査 census の pin mod4 クラス〔誤クラス格子の実挙列挙〕・probe 行欠落（幾何ゲート）・重複行注入（幾何ゲート）・
  meta d 改ざん・merge flag 改ざん（逐行整合性ゲート）・band 下端改ざん〔mm=264〕・RLE 長改ざん（同ゲート）。
  各変種は正本から新規 copy した隔離 dir で実施〔`__pycache__` が存在し得ない状態から開始 + `-B` +
  `PYTHONDONTWRITEBYTECODE`〕・clean control 2 回（前後）rc=0 で audit.json 出版正本と byte-identical。
  **y18 で得たキャッシュ衛生規則を最初から適用**し、stale-pyc 検出漏れは今回も不発生・10/10 を確定。
- **誠実記録: 宣言の偶z base 行域記述の誤りを fit census が捕捉・出版前に訂正**。
  cand19 のコード通り機械 census すると偶z 生残 d 域は [-18,19] で偶z base 行は d 奇 19 行・d∈[-17,19]・
  **上端 d=19=Y は k=Y 飽和**（y=17 の d=17・y=18 の d=18 と同型）。宣言の「17 行・[-17,17]・上端非飽和・
  2 箇所 k=Y 族初」は行域算術の誤りで、正しくは 3 行の k=Y（出版 y=17 の d=16/d=17/d=17 と同型）。行クラス
  z 偶 d=19 は probe box 内（z=0..30 全偶z 行・z=0/x=19 と z=2/x=21 の生値が b_19 19 点と完全一致）と
  spot bigz d=19 行（z=31..40）で生値検証済み。**族式そのものは probe 99,107 点に修正 0** で、Y+2 機械翻訳
  コードは最初から正しかった（宣言 meta の帳簿づけのみが誤り）。これに伴い (a) cand19.py の docstring・コメントを
  行域実態に合わせて修正（コード本体は 1 文字も不改変・selfcheck mm=0・値ヒストグラム同一で再確認）、(b) spot を
  再実行（44,597 点 bad 0・点数同一・230.0 秒）、(c) 監査を再生成して決定性を取り直し（4 実行 byte-identical・
  SHA-256 a1ddd7f1…65b14）、(d) fail-closed 電池 10/10 を最終正本に再適用、(e) 宣言の訂正として
  amendment ノートを出版する（y=17 の点数算術誤り訂正 82653b6f と同じ運用手順・今回は出版前捕捉）。

## 出版

- Commit A: 実験dir `research/experiments/vertical-fiber-two-token-y19-parametric-allz-fit-20261123/`
  （report.md・cand19.py・probe_y19.py・spot_y19.py・make_audit_y19.py・output/audit.json）
- Commit B: item K1243 + 本fit log + 宣言amendmentノート
  （2026-11-23-y19-decl-z-even-base-bookkeeping-amendment.md）
- Commit C: knowledge README 末尾bullet追記
- 各 push 直前に最新 main HEAD を再取得し commit message に観測 HEAD を記録。

## 次段階（本実行の範囲外・別宣言）

- y=19 全称（verify_y19_universal.py・A子 H(R-1;(x-1,19);z)〔x=19 行は合流子 {18,19}≡{19,18} で
  cand18(z,19,R-1)〕・B子 出版 cand18 逐語転写・C子 1 xor cand19(z-1,x,R-1)・型機械 clip 窓
  2y+2=40 tight 判定〔15 族目候補〕・census）
- 横断法則の一般補題化レーンが最有力（seed 法則 7 連続・pin 行数則 (y±1)/2 が 10/9 で両偶奇
  4 データ点・band 下端 2y+2 の 7 データ点・band_base/band_int 分離の奇数 y 3 連続・
  2 箇所 k=Y という y=19 新形態の族式化）
- fast lane の他候補: y=20 族 fit（**注意: y=20 は偶数 y で seed は cand18〔K1242・observed〕で
  あって cand19 ではない。observed seed からの外挿は seed law の主張形式を変えるため
  宣言で明示的に区別する必要がある**）・REMO 3 枝 cap<=15 r=3 sweep 等
