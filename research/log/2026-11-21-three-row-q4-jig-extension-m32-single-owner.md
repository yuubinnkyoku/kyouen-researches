# 単一オーナー宣言: 3行 q=4 列挙閉包レーン m≥32 治具拡張（wsearch35 系）

- 宣言時刻: 2026-11-21T10:39Z
- 宣言時 HEAD: `49221227f0df3676b8cea2260462ec63ce98ebc8`
- 前段: ext28plus 拡張（宣言 `e9c3cd86`・part1 `9bb34ec6`・part2 `d173632f`）で
  P(28), P(29), P(30), P(31) が列挙閉包で確定済み・witness-free 幅 {24..31}・
  M_{3,4} ∈ [24, 69]（K0024 上界）・残る不確定幅 32..68 の 37 幅。
- 本宣言の対象: pinned wsearch34.js（md5 526cf1c3・m≤31 上限）を m≥32 で動かすための
  治具拡張レーン。**pinned 原版（wsearch34.js・md5 526cf1c3・dx34.js・md5 b02235a9・
  sat.js md5 0cc6021a ほか 7 scripts）は 1 byte も変更しない**。新規ツールは別名で出版する。

## 新規ツール（本セッションで構築・検証済みのもの）

1. **wsearch35.js**: wsearch34.js の全 bitmask を (lo, hi) int32 2-limb 表現へ
   忠実分割した版（4 ≤ m ≤ 62・bit index x は x<31 で lo・x≥31 で hi bit x−31）。
   表索引体系・判定式は wsearch34 と同一（lo/hi それぞれに同一式を適用）。
   d > 32 deep カットは全 m で sound のまま（family witness は
   W(s)|W(t)|{s,t} で defn を被覆し各 W(s) は C(6,2)=15 bit 以下なので
   |defn| ≤ 32 は必要条件・近似ではない）。
2. **wsearch35b.js**: 同一意味論の BigInt 版（BigInt64Array 表・4 ≤ m ≤ 62）。
   mask 機構が limb と独立なので、**m ≥ 32 で hi-limb コードが稼働する初回の
   二重メカニズム交差検証**に使う（m ≤ 31 では hi limb は恒等的に 0 であり
   m ≤ 31 のバッテリーだけでは hi-limb を検証できないため）。

## 検証バッテリー（宣言時点で完了）

- 計数等価 wsearch35 ≡ wsearch34（ms を除く JSON が同一）: m=4..8 × Y∈{0,1,2} 15件・
  m=9..12 × Y∈{0,1,2} 12件。
- stdout 全行 byte 等価（--examples=9999・ms 正規化）: (m,Y) = (4,0),(4,1),(5,0),
  (6,2),(7,1),(8,0),(9,2),(10,0),(13,1),(16,2),(20,0),(21,1),(22,2) の13件
  （witness 行を含む）。
- 陽性対照: m=23 Y=0 全域（configs 3,136,441・safe 2,352,504・a2=2・witness 石座標
  byte 一致 ext28plus control_m23_Y0.txt）。Y=1（a2=4）・Y=2（a2=2）は既刊計数と一致。
- 大域対照: m=28 Y=0 全域（configs 10,732,176・safe 8,511,828・a*=0）既刊正本生 raw
  と計数一致（実行 185.7s・pinned 比で 1.34 倍）。
- wsearch35b ≡ wsearch35: m=23 Y=0 全域（計数+witness byte 一致）。
- **hi-limb 二重メカニズム交差検証（m=32）**: Y=0 ia[0,300)（configs 1,488,000・
  safe 1,274,673・a*=0）・Y=0 ia[4660,4960)（tail・safe 1,327,342）・
  Y=1 ia[1240,1540)（mid）の3区間で 35 と 35b が byte 一致
  （残り: Y=2 の 1 区間は完了後に実施）。

## m=32 family 掃引の宣言時点での状態

- 分割: nSub = C(32,3) = 4,960 を ia 4 chunk〔0,1240)〔1240,2480)〔2480,3720)〔3720,4960)
  （exactly-once・各 chunk configs = C(32,3)²/4 = 6,150,400）。
- 完了 11/12 chunk・**a0 = a1 = a2 = 0 全 chunk**: 各 (Y, chunk) の safe は
  Y=0: 5,137,846 / 4,990,345 / 4,878,024 / 5,122,495・Y=1: 同一列・
  Y=2: 5,137,846 / 4,990,345 / 4,878,024 + 〔3720,4960) 未実行
  （10:35Z 頃より実行環境が一時停止しており、復帰後に再実行・決定性により計数は同一。
  ms は環境依存の参考値: Y0 153.7/159.6/156.0/164.4s・Y1 175.9/160.1/155.9/168.8s・
  Y2 153.0/163.2/141.0s/chunk）。
- 念のため部分整合の確認済み:〔0,880) probe（configs 4,364,800・safe 3,659,546・a*=0）
  は chunk c0〔0,1240) の部分区間であり、計数は c0〔0,1240)（configs 6,150,400・safe 5,137,846）と整合。

## 受入条件（本レーンの出版は以下を満たす場合のみ）

1. pinned 原版 7 scripts（md5 台帳どおり）は非変更。wsearch35.js / wsearch35b.js /
   m=32 出力・集計器は別名の新規ファイルとしてのみ出版し、既存出版 output は
   1 byte も変更しない（実験 README への追記は append のみ）。
2. 出版は part 分割・各回 fetch-back byte 照合。他レーンの並走 push とは
   ファイル非接触で運用し、push 競合・取得失敗時は無理せず記録して次回へ。
3. m=32 family の「掃引完了」主張は集計器（agg_chunks 方式の機械検査）で
   〔0,4960) の exactly-once 分割・configs 和 = C(32,3)² = 24,601,600/Y・
   全 chunk a*=0・二重メカニズム区間一致を検査してから行う。
4. **P(32)（m=32 witness-free）の主張は family 12 chunk 完了 + fast 13プロファイル
   （dx34 fast の m≥32 移植版・m≤31 での ≡ 既刊 dx34 fast 全数バッテリーつき）+
   crossing-supply 補題 closure の m=32 版（closure_check.py の m≥32 動作確認）
   がすべて揃った後に限る**。それ以前は「(m=32, Y, family) 掃引は witness 0」を
   observation としてのみ記録する。
5. K1183 の更新は P(32) が確定した場合のみ（witness-free 幅 {24..32}・残る 33..68 の
   36 幅・M_{3,4} ∈ [24,69] 不変・P の幅単調性は未証明の明記）。
   family のみ完了の場合は本レーンの log/K 番号採番をせず session log に留める。
6. frontier レーン（SAT・records.jsonl）には接触しない。標準 11×11 空盤・二石root
   {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は本レーンと無関係で UNKNOWN のまま。
   nodes/solved/conflicts 計数を勝敗として読まない・REFUTED-D10 は LOSS 証明ではない。

## 次の実行可能課題（着手前に最新 main 再取得）

1. Y2 chunk〔3720,4960) の実行（環境復帰後・単一 foreground）+ Y2 hi-limb 二重回検。
2. dx34 fast path の m≥32 移植版（dx35）の構築とバッテリー
   （m=4..12 selftest ≡ dx34 fast・m=13..31 の既刊 dx_sweep 計数列との一致・
   その後 m=32 fast 13プロファイル掃引）。
3. closure_check.py の m=32 実行確認（41/41 closed 予想・算術のみ）。
4. 集計・検証経由での P(32) 確定 → part1（ツール+battery+m=32 出力集計）・
   part2（K1183 更新 + session log）出版。
