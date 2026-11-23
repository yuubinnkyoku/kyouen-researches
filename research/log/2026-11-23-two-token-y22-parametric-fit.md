# y=22 two-token パラメトリック閉形式 fit 実行記録（2026-11-23・高速レーン）

## 選定

- 前回の resume 指定どおり **y=22 two-token 族 fit**（y21 fit log の次候補列挙が指名する
  「y=22 族 fit（seed cand20・K1246 promoted・偶数 y 系列第 6 ペア目候補）」への応答）。
  y=1..21 の 2 トークン族全称は K1248 proved（K1255 機体）で完結しており、本族は
  **全称証明済み範囲の外の最初の族**である。
- 対抗宣言の確認: 宣言 push 直前の最新 main 再取得で y=22 関連コミット 0 件・
  K1256 は items/README ともに空番・実験 dir と fit log パスは 404 を機械確認
  （宣言ノートに記録・宣言時点は GitHub API 無認証枠枯渇のためraw 非存在確認中心）。
  並走レーン（inversive arc K1250-1253・K1252 proved 昇格・K1254/GX-M・n11 Part BU・
  y21 全称 K1255）はすべて非接触。Commit A push 直前 HEAD `24037c3e`
  （K1252 campaign summary・2026-11-23T11:27Z・非接触）。

## 宣言（publish-then-execute・単一オーナー）

- 宣言ノート: `research/log/2026-11-23-y22-two-token-skeleton-single-owner-note.md`
  commit `c0baada6e68bcd1f323a0fac4bafbb1db051593c`（probe 実行前に出版・
  fetch-back byte 検証済み・SHA-256 b552094d38cc545c4a5e76958549306a68de661b12bdc33909928f465f1d6cce・
  13,959 bytes）。
- 宣言内容: seed は cand20（K1246 promoted・出版最終構造）の Y=20→22 機械翻訳・
  逆 rename 両方向 byte 検証の事前登録・probe box z=0..30・x=22..z+43・
  R<=x+z+46 = 2y+2（1,147 行/119,567 点・出版前機械算出）・値ヒストグラム予想
  0:58,950/1:49,478/2:11,139（cand22 意味論のみで機械算出）・spot 幾何
  （deep 46 行/5,980・bigz 240/30,240・edge 25/4,100・far 18/2,628・tail raw 78・
  merge 123 行/19,449）・総比較点 182,042・マージ行の box 内 0 行（z>=46 必要・
  8 族連続）・pin 格子（奇z d≡2 mod4 の 11 行・偶z d≡0 mod4 の 11 行・
  **両偶奇同時 11 pin 行は系列初**・box 外 pin は各偶奇 3 行ずつ計 6 行で**ともに系列初**）・
  k=Y census 4 行・K0915 z=6,y=22 証明済み切片との三点照合の予定。
- 誠実な宣言前開示（宣言ノートに明示済み）: 宣言確定前に chunk driver 実機確認のため
  deep ブロック 1 回（46 行/5,980 点・bad 0）のみ実行した。宣言数値はすべて
  smoke 実行より先に cand22 意味論とループ幾何のみから機械算出済みで、
  smoke 結果は宣言値に未反映。「一発一致」の主張は宣言後の全電池について行う。

## 実行と結果（すべて決定論的・正本は実験dir + K item）

実験dir: `research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/`
（9 ファイル・Commit A `3b69574e`・9 ファイルとも commit-pinned raw fetch-back byte 検証済み）。

- cand22 初稿（出版 cand20〔K1246 promoted〕の Y=20→22 機械翻訳・Y 定数・docstring・
  rename（in_T22/in_P22/cand22/b22）・行内コメント値 5 件の再計算のみでコード本体は全式 Y 式で
  1 行も不改変・**逆 rename（22→20 戻し）が出版 cand20 コード本体と byte 同一になることを
  両方向で機械検証**・`translate_y22.py`・機械翻訳偶数 y 連鎖 12→14→16→18→20→22 の第 6 リンク）:
  **probe 1,147 行 119,567 点に一発完全一致**（修正 0・mismatch 0・T/P 重複 0・
  値頻度 0:58,950/1:49,478/2:11,139 が宣言の事前機械予想と厳密一致・値 3 なし）。
  **出版最終構造 seed 法則 10 連続一発一致**（偶数 y 系列 12→14→16→18→20→22 の 6 連続・
  奇数 y 系列 5 連続）。**証明済み seed 外挿 4 連続目**
  （cand11→13〔K1143〕・cand18→20〔K1242〕・cand19→21〔K1243〕・cand20→22〔K1246〕）。
- box 内 tail assertion（R>=x+z+23 → (x+22) mod 2）: **27,528 点 bad 0**
  （R cap x+z+46 = 2y+2 で 1 行あたり 24 点深・宣言の事前機械算出と厳密一致）。
  box 内マージ行: **0 行**（宣言の事前導出どおり・**8 族連続**）。
- box 内 pin census（監査 fail-closed gate）: box 内可観測の奇z 8 行・偶z 8 行すべて、
  全 pin 位置 R=z+(d+66)/2 で値 2 を in-box 観測。値ヒストグラム gate も宣言予想と完全一致。
- box 外 spot（`spot_y22.py`・LRU cap 1.5M）: **43,026 点 bad 0**
  （deep 46 行/5,980・bigz 240 行/30,240・edge 25 行/4,100・far 18 行/2,628・
  全選択行 x>=22 の機械 preflight assert）。
  **全 11 奇z pin 行・全 11 偶z pin 行を個別行として選択**し、
  **6 box 外 pin 行 (41,23) d=-18〔R=z+24=65〕・(37,23) d=-14〔R=63〕・(33,23) d=-10〔R=61〕・
  (42,22) d=-20〔R=65〕・(38,22) d=-16〔R=63〕・(34,22) d=-12〔R=61〕は full R<=130 生値照合で
  pin 位置込み bad 0**（各偶奇 3 行・ともに系列初の事前委任設計どおり）。
  両対角・奇z skew（d=-20/-8）・skew 飽和 d=20（k=Y）・base 行（奇z d=21 飽和・偶z d=22 上端飽和・
  d=-21/d=0）・偶z I 行・掃引 d=23 両偶奇・定常行両偶奇・マージ境界 (45,22)/(46,23)〔x=z-23〕も全行選択。
- merge 回帰 cand22 vs K0832（z∈{46,53,60,67,77,90}・x=22..z-24・R<=x+z+45 = 2y+1）
  **123 行 19,449 比較 bad 0**（宣言の事前機械算出と厳一致・7 族連続に続く全面 box 外マージ回帰）。
- **K0915（z=6,y=22 証明済み切片・全称証明）三点照合**: K0915 出版値2表 T_22(x)・値1表 P_22(x) を
  監査生成器に機械転写し、probe box 内 z=6 切片（x=22..49・R<=x+52）**全 2,450 点**で
  ①生 probe 値 vs 証明済み分類・②cand22 vs 証明済み分類がともに **bad 0**（fail-closed gate）。
  ラダー {1,3,5}・pin (22,6)@47〔d=16〕・(26,6)@49〔d=20〕・掃引 x=29 の {51,53,55,57}・
  定常 R=51〔=z+2y+1〕・tail R>=x+29 → (x+22) mod 2 が宣言予想・K0915 出版表・生値で完全一致
  （宣言電池の総点 182,042 には含めない 3 方向独立整合・2 レーンの相互補強）。
- **系列初達成 3 件（y=12..y=22 横断）**: ①**両偶奇が同時に 11 pin 行**（y=21 の単一偶奇 11 に続き
  偶数 y 族で初の奇z 側 11 到達でもある）②**各偶奇側 box 外 pin 3 行・合計 6 行は系列最多**
  （y=17: 1・y=18: 1+1・y=19: 2+1・y=20: 2+2・y=21: 3+2 → y=22: 3+3）③**初の 23 行 th 連続整数掃引
  23..45**（y=12 15 行 13..27・…・y=20 21 行 21..41 に続き掃引長 +2 の偶数族法則 6 データ点目）。
  このほか偶z 対角値1欠如は 15 族目候補・band 下端 2y+2=46 は 10 データ点目・
  基底点 22 点は 22 例目候補・tail 開始 x+z+23 は 22 族目候補・pin スロット則
  （奇z th-1・偶z 2k+1）は 12 族目候補・k=Y census は偶数族 4 行形状
  {20,22}/{21}/{22} の 4 データ点目（y=16/18/20 と同型）。
- 合計 **182,042 点比較・不一致 0**（probe 119,567 + spot 43,026 + tail raw 78 + merge 19,449・
  宣言の事前機械算出と全数値一致）。
- 決定性: probe_rows.txt は宣言後 **6 回再生で byte 同一**（SHA-256 2380c95100402ac7…・
  リセット前 3 回 + 出版参照からの再構成後 3 回〔うち 1 回は隔離 tree/cwd/HOME + env -i +
  PYTHONHASHSEED=random〕・キャッシュ統計も同一）。audit.json は最終版 **3 回再生 byte 同一**
  （SHA-256 fecfc248…15b905b）。
- sandbox 制約と spot 再実行: 単一 foreground 実行上限 300 秒に対し spot 全実行は超過のため、
  出版 `spot_y22.py` の main() を一意マーカーでバイトスライスした
  **`spot_chunk_rerun_y22.py` で 3 バッテリー全実行**（deep/bigz/edge/far/tailmerge 各ブロックの
  点数・bad・LRU CacheInfo が全バッテリーで完全一致・wall 合計 336〜340 秒・
  pinned 秒数 337.0）。H_canonical は純関数で決定的 LRU 退避論証と同一根拠。
- fail-closed 改ざんバッテリ（`tamper_battery_y22.py`）: **20 変種すべて caught**
  （leak 0・no-op 0・各改ざんの ANCHOR EFFECTIVENESS assert 事前検証で実効性保証・
  監査生成器は非零 exit かつ audit.json 不書出しで検出・復元 byte 検証済み）。
  battery 終了後の restore 再実行が最終成果物（cand22.py 確定版・audit.json 確定 sha）を再生成。

## 誠実記録（帳簿づけ 5 点・正本は report.md）

1. **宣言前 deep smoke の開示**（宣言ノート明示済み・上記「宣言」節）。
2. **sandbox リセットからの再構成**: 宣言出版（c0baada6）後、実行中の 300s タイムアウトで
   実行環境がリセットされローカル作業ファイルを喪失。全成果物は出版参照
   （cand20.py・probe_y21.py・spot_y21.py・spot_chunk_rerun.py 他）から同一の事前宣言手続きで
   再生成し、再生成 probe が旧 probe_rows.txt と byte 同一（sha 2380c951…）を再現して検証した。
   出版ファイルは再構成パイプライン由来で、宣言済み数値は旧ローカル状態に依存しない。
3. **K0915 転写トラップ**: P_22(x>=29 奇) の tail 下端 O[x+30,∞) を一時 x+31 と誤転写した際、
   三点照合ゲートがまさに境界点 11 点（R=x+30・x=29..49 奇）だけを検出して fail-close した
   （修正後全 2,450 点一致）。fail-closed 設計の作動実例。
4. **spot 秒数の性質**: pinned 337.0 秒は chunk 実行 5 ブロックの wall 合計（host 依存の参考値・
   単一フル実行は sandbox cap 超過のため chunk 実行で記録）。
5. **対抗宣言確認手段の限界**: 宣言時点で GitHub API 無認証枠枯渇。最新コミット一覧・
   予測可能パスの raw 非存在確認・items コミット確認に限定（宣言ノートに明示・
   push 直前再取得で y22 関連 0 件を機械確認）。

宣言ノートの事前横断予想は**全項目が修正なしで確認**され、amendment は不要
（判定表は report.md・全 18 行一致）。

## 出版

- Commit A `3b69574e`: 実験dir 9 ファイル（report.md・cand22.py・probe_y22.py・spot_y22.py・
  spot_chunk_rerun_y22.py・make_audit_y22.py・translate_y22.py・tamper_battery_y22.py・
  output/audit.json）。commit-pinned raw fetch-back で 9 ファイルとも byte 検証
  （audit.json 記載の sha256 ピンと一致）。
- Commit B: item K1256（fit item・status observed）+ 本 fit log。
- Commit C: knowledge README に K1256 bullet 追記。
- 各 push 直前に最新 main HEAD を再取得（Commit A 直前 HEAD `24037c3e`・非接触を確認）。

## 次段階（本実行の範囲外・別宣言）

- y=22 全称（verify_y22_universal.py・単一オーナー宣言。
  A子 H(R-1;(x-1,22);z)〔x=22 行は合流子 {21,22}≡{22,21} で cand21(z,21,R-1)〕・
  **B子 出版 cand21 逐語転写（系列初の全称確定済み B-child・K1248 proved）**・
  C子 1 xor cand22(z-1,x,R-1)・型機械 clip 窓 2y+2=46〔sentinels ±47〕・census・part1/part2）。
- y=23 fit の seed は cand21（K1248 proved）で、証明済み seed 外挿の 5 連続目候補。
- 横断法則一般補題化レーン: 偶数 y 6 ペア・seed 法則 10 連続・pin 行数 (y+2)/2 と y/2 の
  初の同時 11 行・box 外 pin 3+3・23 行掃引の偶数族データ点提供。
