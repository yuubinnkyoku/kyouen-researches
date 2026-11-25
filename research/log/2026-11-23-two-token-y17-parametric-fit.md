# y=17 two-token パラメトリック閉形式 fit 実行記録（2026-11-23・高速レーン）

## 選定

前回実行のレジューム（y=16 fit 出版・K1237・commit 時点で12番目の y 族 fit 完了）が指名した
次候補の比較を行い、**y=17 族 fit** を着手した。理由: (a) 奇数 y 系列の第3Seed法則テスト
（cand11→13→15→17）と seed 法則全体では5番目の一発一致テストであり、横断法則一般補題化
レーンの最優先材料（「直前の出版最終構造から機械外挿して一発一致する」が偶奇双方で何族
続くかは跳躍リスクの核心）、(b) pin 行数則 (y+1)/2 が初めて 9 に達する最初の族で、
「pinスロット=th-1」「最終pin行 d=y の I[2y+z+1) 型」の系列判定の4点目、
(c) y=15・y=16 に続き box 内マージ行 0 行が3族連続するかの判定材料、
(d) 単独で完結して出版可能（宣言→fit→spot→監査→item→README、K1235/K1237 と同型）、
(e) 直近コミットに y=17 族着手なし（tree走査で z6-y17-boundary 系コミットのみhit・
対抗宣言なし）を確認済み。K番号は K1240（K1239 まで使用済み・items に y=17 族項目なし）。

## 宣言（probe実行前に先行出版）

- 宣言ノート: [2026-11-23-y17-two-token-skeleton-single-owner-note.md](2026-11-23-y17-two-token-skeleton-single-owner-note.md)
  （commit `eeeb1a8e`・probe 実行前に出版・事前横断予想12項目を全登録）
- 事前横断予想（seed cand15〔K1235 全称昇格済み〕の Y+2 機械翻訳初稿で修正0を予想・
  基底点17点・マージ行 x<=z-18〔**y=17では box 内マージ行0行・z>=35 が必要、事前明記**〕・
  pin 格子統一式 pin=z+(d+51)/2∈[18,34]・奇z 9行 d≡1 (mod 4) {-15,...,17}〔**初の9 pin
  行族**〕・偶z 8行 d≡3 (mod 4) {-13,...,15}・「pinスロット=th-1」7族目候補・最終pin行
  d=17=y の I[35) 型12族目候補・掃引 d=18・定常 pin z+34/z+35・band 下端 2y+2=36・
  tail 開始 x+z+18 値 (x+17) mod 2・d>=18 tail 19点深）を probe 実行前に全部登録し、
  **全項目 fit level で一致**した。
- 宣言 box: z=0..30・x=17..z+33・R<=x+z+36（=2y+2・y=14/15/16 出版の宣言済み
  convention を継承）。宣言ノートの点数算術誤り（81,902→86,552・box 定義は不変）は
  amendment `82653b6f` で訂明記録した。

## 実行と結果（すべて決定論的・正本は実験dir）

- cand17 初稿（出版最終構造 cand15〔K1235 全称昇格済み〕の Y+2 機械翻訳・コード本体は
  Y 定数と関数名以外は1行も不改変）:
  **probe 992行 86,552点に一発完全一致**（修正0・mismatch 0・T/P重複0・値頻度
  0:42,568/1:34,200/2:9,784・値3なし・約8.2秒）。
  **出版最終構造 seed 法則 5 連続**（cand11→13・cand13→15・cand15→17〔奇数 y 系列〕・
  cand12→14・cand14→16〔偶数 y 系列〕）。
- box 内 tail assertion（R>=x+z+18→(x+17) mod 2）: **18,848点 bad 0**（x 偶行は値0・
  band 区切り確認）。box 内マージ行: **0行**（宣言の事前明記どおり・3族連続）。
- box 内 pin census（監査 fail-closed gate）: 奇z 8行・偶z 8行すべて値2で in-box 観測。
  偶z対角行値1 census: 計数0。
- box 外 spot（`spot_y17.py`・LRU cap 1.5M・177秒）: **41,465点 bad 0**。
  特に全9奇z pin行（d=-15 は box 内到達不可能のため deep row (33,18) 生値照合に委任・
  R=51 pin 値2を含む）・全8偶z pin行・両偶奇対角・掃引 d=18・band 下端 36・
  マージ境界・tail raw 84点を生値検証し、**全選択行に x>=17 の機械 assert を実装**。
- merge 回帰 cand17 vs K0832（z∈{35,40,47,54,64,77}・x<=z-18・R<=x+z+35）**15,495比較
  bad 0**（3族連続の全面 box 外マージ回帰）。旧来の境界行 (35,17)/(36,18) 生値一致。
- 決定性: probe_rows.txt 3回再生成（同一cwd 2回+隔離 tree/cwd/HOME + PYTHONHASHSEED=random）
  すべて byte-identical（SHA-256 248d5249…）。audit.json 3実行 byte-identical
  （SHA-256 c5593987…）。合計 143,596点比較・不一致0。
- fail-closed 改ざん試験: **8変種すべて検出**（probe値・pin値・Y定数 17→16〔mismatch
  3,764〕・pin mod4クラス・probe行欠落（幾何ゲート）・重複行注入（幾何ゲート）・
  **z-odd pin d=-15 の box 内到達不可能性**（監査生成器自体の FAIL-CLOSED が捕捉 →
  ゲートを box 内可観測8行に修正し d=-15 を spot deep row (33,18) 生値照合に委任・
  誠実記録として audit.json/report に記載）・復元 byte-identical）。

## 出版

- Commit A: 実験dir `research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/`
  （report.md・cand17.py・probe_y17.py・spot_y17.py・make_audit_y17.py・output/audit.json）
- Commit B: 本item K1240 + 本fit log
- Commit C: knowledge README 末尾bullet追記
- 各 push 直前に最新 main HEAD を再取得し commit message に観測 HEAD を記録。

## 次段階（本実行の範囲外・別宣言）

- y=17 全称（verify_y17_universal.py・A子 H(R-1;(x-1,17);z)〔x=17 行は合流子
  {16,17}≡{17,16} で cand16(z,17,R-1)〕・B子 出版 cand16 逐語転写・C子 1xor
  cand17(z-1,x,R-1)・型機械 clip 窓 2y+2=36 tight 判定〔13族目候補〕・census）
- y>=6 横断法則の一般補題化レーン（偶奇揃って各4データ点・seed法則5連続が材料）
- fast lane の他候補: y=18 族 fit・REMO 3枝 cap≤15 r=3 sweep 等
