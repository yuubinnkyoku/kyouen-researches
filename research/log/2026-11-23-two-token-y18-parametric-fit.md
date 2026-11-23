# y=18 two-token パラメトリック閉形式 fit 実行記録（2026-11-23・高速レーン）

## 選定

K1240 fit 出版の part2 レジュームが指名した次候補の第一位として、**y=18 族 fit** を着手した。
理由: (a) K1238 偶数 y 統一テンプレート（単一 Y パラメトリックコードで y=10/12/14/16 出版 4 族の
再生を機械検証済み）の**第5 even-y データ点**であり、テンプレートの外挿範囲外の y で唯一
機械可能な次の検証材料、(b) seed 法則全体では第6テスト・偶数 y ペア系列（12→14→16→18）は
第3ペア目で、横断法則一般補題化レーンの跳躍リスク評価の最優先材料、
(c) y 偶族の pin 行数 y/2 が両偶奇とも 9 行に揃う初の族（y=16 で 8 行揃いの次の判定点）で
「偶z pin 行が初めて 9 行に達する」宣言済みの主要行数則判定、
(d) y=15/16/17 に続き box 内マージ行 0 行が 4 族連続するかの判定材料、
(e) 単独で完結して出版可能（宣言→fit→spot→監査→item→README、K1240 と同型）、
(f) 宣言時点の main に y=18 族着手・対抗宣言が存在しないことを確認済み（観測 HEAD
60de44ed・n11 長期レーン Part BG/BH は非接触）。K番号は K1242（K1241 まで使用済み・
items の push 直前に最新 main で再確認）。

## 宣言（probe 実行前に先行出版）

- 宣言ノート: [2026-11-23-y18-two-token-skeleton-single-owner-note.md](2026-11-23-y18-two-token-skeleton-single-owner-note.md)
  （commit `738ab049`・probe 実行前に出版・事前横断予想を全登録）
- 事前横断予想（seed cand16〔K1237 全称昇格済み〕の Y+2 機械翻訳初稿で修正 0 を予想・
  基底点 18 点・マージ行 x<=z-19〔**y=18 では box 内マージ行 0 行・z>=38 が必要、事前明記**〕・
  pin 格子統一式 pin=z+(d+54)/2∈[19,36]・奇z 9 行 d≡2 (mod 4) {-14,...,18}・偶z 9 行 d≡0 (mod 4)
  {-16,...,16}・**両最低 pin 行 d=-14/d=-16 がともに box 内到達不可能（両偶奇 box 外 pin 行の初の族・
  spot deep row (33,19)/(36,20) への委任を事前設計**}・「pin スロット=th-1」8 族目候補・最終 pin 行
  d=18=y の I[37,inf) 型 13 族目候補・奇z I 行 k=floor((d+56)/4)・th 連続整数 19..37 の**初の 19 行掃引**・
  base 行 k=floor((d+55)/4) 9 族目候補・偶z I 行 k=floor((d+53)/4) 8 族目候補・d=18 飽和 5 族連続候補・
  掃引 d=19・定常 pin z+36/z+37・band 下端 2y+2=38・tail 開始 x+z+19 値 (x+18) mod 2・偶y 単一 band 則）を
  probe 実行前に全部登録し、**全項目 fit level で一致**した。
- 宣言 box: z=0..30・x=18..z+35・R<=x+z+38（=2y+2・y=14..17 出版の宣言済み convention を継承・
  d-cap 2y-1 は y=15/17 convention に揃えた）。点数 92,721・行 1,023 は**宣言ノートの出版前に機械算出して
  記載**したため amendment 不使用（y=17 の点数算術誤り訂正 82653b6f の教訓を適用）。
- 宣言の観測 HEAD（60de44ed）の直後に n11 長期レーンの session log commit（cac1e5cc）が挟まったが
  非接触（本 fit の作業領域と重複なし）であり、宣言の有効性に影響しない。

## 実行と結果（すべて決定論的・正本は実験dir）

- cand18 初稿（出版最終構造 cand16〔K1237 全称昇格済み・K1238 テンプレート正本〕の Y+2 機械翻訳・
  コード本体は Y 定数と関数名以外は 1 行も不改変）:
  **probe 1,023 行 92,721 点に一発完全一致**（修正 0・mismatch 0・T/P 重複 0・値頻度
  0:45,620/1:37,046/2:10,055・値 3 なし・約 9.8 秒）。
  **出版最終構造 seed 法則 6 連続**（cand11→13・cand13→15・cand15→17〔奇〕・cand12→14・
  cand14→16・cand16→18〔偶・偶数 y 系列 3 連続〕）。
- box 内 tail assertion（R>=x+z+19→(x+18) mod 2）: **20,460 点 bad 0**（1 行 20 点深・R cap 2y+2 の成果）。
  box 内マージ行: **0 行**（宣言の事前明記どおり・4 族連続）。
- box 内 pin census（監査 fail-closed gate）: box 内可観測の奇z 8 行・偶z 8 行すべて値 2 で in-box 観測。
  偶z 対角行値 1 census: 計数 0（11 族目候補）。
- box 外 spot（`spot_y18.py`・LRU cap 1.5M・190.9 秒）: **40,383 点 bad 0**。
  特に全 9 奇z pin 行・全 9 偶z pin 行を個別行として選択し、**両 box 外最低 pin 行 (33,19) d=-14・
  (36,20) d=-16 は full R<=130 生値照合で pin R 値 2 を含めて確認**（両偶奇 box 外 pin 行の初の族の
  事前委任設計どおり）。全選択行に x>=18 の機械 preflight assert を実装し、この gate が初稿の
  bigz d=-16@z=31 選択（x=15<18）を live で拒否した（誠実記録）。
- merge 回帰 cand18 vs K0832（z∈{38,45,52,59,69,82}・x=18..z-20・R<=x+z+37）**16,989 比較 bad 0**
  （4 族連続の全面 box 外マージ回帰）。境界行 (39,20)/(38,19) の生値一致も spot deep 内で確認。
- tail raw 回帰: 6 行 84 点 bad 0。
- 決定性: probe_rows.txt 3 回再生成（同一 cwd 2 回 + 隔離 tree/cwd/HOME + PYTHONHASHSEED=random）
  すべて byte-identical（SHA-256 e80ca337…4429）。audit.json 3 実行 byte-identical
  （SHA-256 b0d9c4be…7468）。合計 **150,177 点比較・不一致 0**（92,721 + 40,383 + 84 + 16,989）。
- fail-closed 改ざん試験: **10 変種すべて検出**（probe 値・pin 値・Y 定数 18→17〔ハード assert〕・
  pin mod4 クラス〔監査が欠落 7 行を列挙〕・probe 行欠落（幾何ゲート）・重複行注入（幾何ゲート）・
  meta d 改ざん（逐行整合性ゲート・本族新設）・merge flag 改ざん（同ゲート）・band 下端改ざん
  〔mm=511〕・RLE 長改ざん（逐行整合性ゲート）・復元 byte-identical・clean control rc=0）。
- 誠実記録 3 件（いずれも fail-closed 設計・検証手続きが live で効いた実例）:
  (a) spot 初稿の bigz d 選択が preflight assert に拒否され 25 値に修正、
  (b) 監査初稿の pin_counts tuple キー JSON クラッシュが電池の clean control で「3 回同一クラッシュ」と
  判明し原因除去（byte-identical 3 実行を改めて確定）、
  (c) 改ざん電池初回実行で同一秒内・同一サイズの改ざんが stale `__pycache__` に握り潰され V3/V9 のみ
  検出漏れ。`__pycache__` purge・`-B`・`PYTHONDONTWRITEBYTECODE` のキャッシュ衛生で 10/10 を確定。
  「byte-identical N 回」型の検証主張にはバイトコードキャッシュ衛生が必須という運用正則を得た。

## 出版

- Commit A: 実験dir `research/experiments/vertical-fiber-two-token-y18-parametric-allz-fit-20261123/`
  （report.md・cand18.py・probe_y18.py・spot_y18.py・make_audit_y18.py・output/audit.json）
- Commit B: 本item K1242 + 本fit log
- Commit C: knowledge README 末尾bullet追記
- 各 push 直前に最新 main HEAD を再取得し commit message に観測 HEAD を記録。

## 次段階（本実行の範囲外・別宣言）

- y=18 全称（verify_y18_universal.py・A子 H(R-1;(x-1,18);z)〔x=18 行は合流子 {17,18}≡{18,17} で
  cand17(z,18,R-1)〕・B子 出版 cand17 逐語転写・C子 1 xor cand18(z-1,x,R-1)・型機械 clip 窓
  2y+2=38 tight 判定〔14 族目候補〕・census）
- 横断法則の一般補題化レーンが最有力（seed 法則 6 連続・even-y 統一テンプレート 5 データ点・
  pin 行数則両偶奇 4 データ点・掃引長 15/17/19 行の線形増加・band 下端 2y+2 の 6 データ点の材料）
- fast lane の他候補: y=19 族 fit・REMO 3 枝 cap<=15 r=3 sweep 等
