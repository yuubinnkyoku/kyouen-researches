# y=21 two-token パラメトリック閉形式 fit 実行記録（2026-11-23・高速レーン）

## 選定

- 前回の resume 指定どおり **y=21 two-token 族 fit**（y20 fit log の次候補列挙が指名する
  「y=21 族 fit（seed cand19・K1243 proved・奇数 y 系列第 5 ペア目候補）」への応答）。
- 対抗宣言の確認: GitHub code search で `cand21 repo:yuubinnkyoku/kyouen-researches` 0 件・
  直近コミットに y=21/y21 系 fit は 0 件・既存 `y21` hit は K0914（z=6,y=21 証明済み切片・2026-11-17 出版）
  のみで fit とは非接触（むしろ交差検証素材）。並走レーン（inversive arc K1250-1253・n11 Part BP・
  3トークン K1247 仮採番・横断法則一般補題化）はすべて非接触。
- K 番号 K1248 は items の最新 main で未使用を確認（K1240..K1246・K1250..K1253 のみ・K1247 は
  3トークンレーンの仮採番・K1249 も空き）。

## 宣言（probe 実行前に先行出版）

- commit `2d3aeac2498be83cdcbf989074eaaf58506609fc`（`research/log/2026-11-23-y21-two-token-skeleton-single-owner-note.md`）。
  觀測 HEAD-before-push `ed25d68e2a13d40b95ba95a111310bf66cb50beee`（非接触）。
- 宣言内容: seed は cand19（K1243 proved・全称確定）の Y=19→21 機械翻訳・逆 rename 両方向 byte 検証の事前登録・
  probe box z=0..30・x=21..z+41・R<=x+z+44（1,116 行/112,530 点・出版前機械算出）・
  spot 幾何（deep 44 行/5,720・bigz 280/34,510・edge 25/4,075・far 18/2,556・tail raw 78・merge 117 行/17,835）・
  総比較点 177,304・値ヒストグラム予想 0:55,466/1:46,196/2:10,868（cand21 意味論のみ・raw エンジンは宣言前に
  1 度も未実行）・pin 格子（奇z d≡1 mod4 の 11 行 {-19..21}〔11 は系列初〕・偶z d≡3 mod4 の 10 行
  {-17..19}・box 外 5 行〔3+2〕は合計・単一側とも系列初）・k=Y census 3 行・K0914 z=6 交差検査の予定。
- fetch-back: commit-pinned raw で byte 一致確認（SHA-256 260c8543f072badb…）。

## 実行と結果（すべて決定論的・正本は実験dir）

- cand21 初稿（出版最終構造 cand19〔K1243 proved〕の Y=19→21 機械翻訳・コード本体は Y 定数と docstring・
  関数名（in_T19→in_T21 等の rename）以外は 1 行も不改変・**逆 rename（21→19 戻し）が出版 cand19 コード本体と
  byte 同一になることを両方向で機械検証**）: **probe 1,116 行 112,530 点に一発完全一致**
  （修正 0・mismatch 0・T/P 重複 0・値頻度 0:55,466/1:46,196/2:10,868 が宣言の事前機械予想と厳密一致・
  値 3 なし・約 16.3 秒→参考値）。
  **出版最終構造 seed 法則 9 連続一発一致**（奇数 y 系列 11→13→15→17→19→21 の 5 連続・全体 9 連続）。
  **証明済み seed 外挿 3 連続目**（cand11→13〔K1143 当時 proved〕・cand18→20〔K1242 proved〕・cand19→21〔K1243 proved〕）。
- box 内 tail assertion（R>=x+z+22→(x+21) mod 2）: **25,668 点 bad 0**（R cap x+z+44 で 1 行あたり 23 点深・
  宣言の事前機械算出と厳密一致）。box 内マージ行: **0 行**（宣言の事前導出どおり・**7 族連続**）。
- box 内 pin census（監査 fail-closed gate）: box 内可観測の奇z 8 行・偶z 8 行すべて、全 128 pin 位置で値 2 を
  in-box 観測（R=z+(d+63)/2 ちょうど）。値ヒストグラム gate も宣言予想と完全一致で PASS。
- box 外 spot（`spot_y21.py`・LRU cap 1.5M・run1 全実行 302.5 秒）: **46,861 点 bad 0**
  （deep 44 行/5,720・bigz 280 行/34,510・edge 25 行/4,075・far 18 行/2,556・全選択行 x>=21 の機械 preflight assert）。
  特に**全 11 奇z pin 行・全 10 偶z pin 行を個別行として選択**し、**5 box 外 pin 行
  (41,22) d=-19〔R=63〕・(37,22) d=-15〔R=61〕・(33,22) d=-11〔R=59〕・(38,21) d=-17〔R=61〕・
  (34,21) d=-13〔R=59〕は full R<=130 生値照合で pin 位置込み bad 0**
  （box 外 pin 5 行〔3+2〕の族初の事前委任設計どおり・奇z 11 行の行数則の直接検証）。
  両対角・奇z skew 行・base 行（奇z d=20 飽和・偶z d=21 飽和）・偶z I 行・掃引 d=22 両偶奇・定常行両偶奇・
  マージ境界 (43,21)/(44,22)〔x=z-22〕も全行選択。
- merge 回帰 cand21 vs K0832（z∈{43,50,57,64,74,87}・x=21..z-23・R<=x+z+43=2y+1）
  **117 行 17,835 比較 bad 0**（z=43 は interior 0 行で machine-observable な emptiness。
  7 族連続の全面 box 外マージ回帰）。境界行 (43,21)/(44,22) の生値一致も spot deep 内で確認。
- tail raw 回帰: 6 行 78 点 bad 0（d∈{23,24,25}・R∈[x+z+22,x+z+35)）。
- **K0914（z=6,y=21 証明済み切片）交差検査（三点照合に強化）**: K0914 report.md の出版値2表 T_21(x)・
  値1表 P_21(x) を監査生成器に機械転写し、probe box 内 z=6 切片（x=21..47・R<=x+50）**全 2,268 点**で
  ①生 probe 値 vs 証明済み分類・②cand21 vs 証明済み分類の両方が **bad 0**（fail-closed gate）。
  ラダー {1,3,5}・pin (21,6)@45〔d=15〕・(25,6)@47〔d=19〕・掃引 x=28 で R∈{49,51,53,55}・定常 R=49・
  tail R>=x+28→(x+21) mod 2 が宣言予想・K0914 出版表・生値で完全一致
  （宣言の「補助的」交差検査を全点照合に強化して実施・宣言電池の総点 177,304 には含めない・
  fit は observed のままであるが raw エンジン・証明系・fit の 3 方向独立整合として 2 レーンの相互補強）。
- 決定性: probe_rows.txt 3 回再生成（同一 cwd 2 回・隔離 tree/cwd/HOME＋env -i＋PYTHONHASHSEED=random 1 回）
  すべて byte-identical（SHA-256 bd9482c7…1c6cbf0）。
  audit.json 最終版（cand21 docstring 確定後）4 回実行すべて byte-identical
  （SHA-256 b61e6581…e2982。初期版 3 回も生成器同一でピン内容は sha256 フィールドのみ相違）。
  **spot は run1 全実行に加え run2/run3 をブロック別再実行で 3 実行とし、全ブロック集計・
  LRU CacheInfo 行（hits/misses/currsize）まで完全一致**（相違は wallclock のみ）。
  合計 **177,304 点比較・不一致 0**（probe 112,530 + spot 46,861 + tail raw 78 + merge 17,835・
  宣言の事前機械算出と全数値一致）。
- fail-closed 改ざんバッテリ（正本から独立 copy した隔離 dir・`-B`＋`PYTHONDONTWRITEBYTECODE`・
  検出条件 = 監査生成器が非零 exit かつ audit.json 不書出し）:
  **20 変種試行・有効改ざん 16 種すべて検出**（probe 値改ざん〔mm〕・z=6 生値改ざん 27 行〔mm+K0914 gate〕・
  行欠落/重複注入の幾何ゲート・RLE 長+1・merge flag 改ざん・meta x<21・meta d 不整合の逐行整合性ゲート・
  cand band 延長〔後述の no-op〕・tail 開始シフト mm=310・pin 格子シフト mm=128+ov=64・
  steady pin (5,28,47) への T/P overlap ov=1 分離検出・Y 定数 21→19〔audit の assert〕・
  audit 側改ざん4種〔K0914 転写表 R=45→46・ヒストグラム予想 55,466→55,467・box 幾何 range 改変・
  tail 深度ゲート 23→22 反転〕・pin 格子リストに非存在行 d=-11 要求）。
  **no-op 2 種は正直記録**: (a) band_base 上端 x+Y→x+Y+1 拡張は値レベルの真の no-op
  （x 奇行は境界 off パリティ非到達・x 偶行は tail と同値・検証は spot/bigz が担う範囲）、
  (b) T/P overlap 第1案は tail 変数を使わない I 帯行分岐へのパッチで実効なし → steady 行 pin 位置へ
  設計し直し ov=1 で分離検出。CONTROL（無改ざん・欠落ファイルなし）は audit.json を書く
  第1回の run で probe_y21.py のコピー入れ忘れによる harness バグで CONTROL が偽 FAIL した点も
  正直に記録する（修正後 CONTROL PASS・各変種はゲート到達前に失敗していなかったことを再確認）。

## 誠実記録（帳簿づけ 4 点）

1. **probe_y21.py docstring の box 点数訂正**: 作業草案の probe docstring に旧草案値 110,148 が残存していた。
   engine 出力（112,530）・宣言ノート（112,530）・audit の box 幾何ゲート独立再計算（1,116 行/112,530 点）は
   すべて一致しており、実効内容への影響はない。公開版では 112,530 に修正した。
2. **sandbox 制約と spot 再実行方式**: 単一 foreground 実行の上限 300 秒に対し spot 全実行は 302.5 秒、
   かつバックグラウンドプロセスは環境リセットで消滅した（run2 第1次試みは出力ゼロ）。run2/run3 は
   出版 `spot_y21.py` の main() を一意マーカーでバイトスライスしたブロック別再実行（`spot_chunk_rerun.py`）で
   実施し、全ブロック集計・LRU CacheInfo 行が run1 と完全一致した。H_canonical は純関数であり
   （出版監査の決定的 LRU 退避論証と同一根拠）、値レベル決定性は chunk 化で損なわれない。
3. **改ざんバッテリの no-op 2 種と harness バグ 1 件**: 上記のとおり正直記録・再設計で検出確認。
4. **秒数の性質**: probe_seconds 16.3・spot_seconds 302.5 は reference run の固定値（host 依存・
   audit.json には pinned として記録・再生成の実測は probe 13.8/14.0 秒）。

宣言ノートの事前横断予想は**全項目が修正なしで確認**され、amendment は不要
（y19 の行域算術訂正のような修正対象は ZeRO 件であった）。

## 出版

- Commit A: 実験dir `research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/`
  （report.md・cand21.py・probe_y21.py・spot_y21.py・make_audit_y21.py・spot_chunk_rerun.py・output/audit.json の 7 ファイル）
- Commit B: item K1248（fit item・status observed）+ 本 fit log
- Commit C: knowledge README の K1246 bullet 直後に K1248 bullet 追記
- 各 push 直前に最新 main HEAD を再取得し commit message に観測 HEAD を記録。

## 次段階（本実行の範囲外・別宣言）

- y=21 全称（verify_y21_universal.py・A子 H(R-1;(x-1,21);z)〔x=21 行は合流子 {20,21}≡{21,20} で
  cand20(z,21,R-1)〕・B子 出版 cand20 逐語転写（**cand20 は K1246 observed・全称未証明のため
  y=20 全称 audit が先行条件候補・両方別宣言**）・C子 1 xor cand21(z-1,x,R-1)・
  型機械 clip 窓 2y+2=44〔sentinels ±45〕の tight 判定・census）。K1249 は空き。
- 横断法則一般補題化レーン: 奇数 y 系列 5 ペア・偶数 y 系列 4 ペアの seed 法則データ点提供。
