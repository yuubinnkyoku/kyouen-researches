# Part EI 単一オーナー宣言 (2026-11-25): batch-39 loss-only canonical adoption (publish-then-execute)

単一オーナー: n11中央応答 長期レーン (本セッションは Part EH batch-39
(class 30484 fresh 50キー probe) の drive・監査・README/MANIFEST・完了log出版まで
完走した同一実行 (`7a687cda` が本実行の最終出版)。
対抗宣言なし: 着手前に最新mainを再取得し (observed HEAD `7a687cda` =
Part EH完了log・2026-11-25T10:21:45Z)、機械検索で "Part EI" 0件・
"batch-39" + adoption 走査 2件 = いずれも Part EH 自身の宣言/kit commits
(`20d17137` / `dc86a313`) で adoption Part は存在しないことを確認。
push時にもHEADを再取得して同一チェックを実施する。並走hourly実行との
同時着手はpush競合チェックが防ぐ。

## 1. レジューム経緯と選定根拠

Part EH が closure class 30484 (rank 20) の fresh 50キー batch-39 を完走し
(`research/experiments/n11-centralreply-closure-class30484-batch39-20261125/`・
完了log `7a687cda`)、**46 LOSS honest行**が adoption 可能 raw として出版
済み (2-pass fresh-cold node-exact @15M・全 fetch-back byte検証・
batch-audit.json `5a2b67cb…`・status.log `08d70bb7`)。これらを canonical
merged chain に loss-only 採用する adoption Part を本章で宣言する。

Part EF (batch-38, class 30345) は別レーン単一オーナーで inc6
(ai044..ai049) がまだ出版されておらず、batch-38 側の LOSS 行 adoption は
EF 完了後の別 Part である。よって本 Part は **batch-39 の46行のみ**を
採用対象とし、EF 所有キー (claim-reserved ai044/ai048 を含む batch-38
targets) には一切触れない。

## 2. スコープ (loss-only・採用対象の厳密な定義)

採用対象は batch-39 honest label LOSS の46行 (aj001..aj050 から
aj030/aj039 (EXHAUSTED) と aj049/aj050 (WIN) を除いた46キー・
worklist probe_order 540..584, 587..591)。各行は

`s5verdict,<lo>,<hi>,5,2,<nodes>`

の1行増分として SSOT = published batch-39 raws
(`output/raw/aj*.p1.out`・p1/p2 node-exact・budget 15,000,000・order=0
fresh-cold) から機械導出する。SSOT 照合 pin: `batch-audit.json`
`5a2b67cb…` (schema n11-centralreply-closure-batch39-audit-v1) +
`output/status.log` `08d70bb7…` + `input/batch-keys-b39.json`
`5e25b550…` + `sources/canonical-cache-fc3e4ac9.cache` pins。

**採用しない行 (不変のまま)**:

- aj049 / aj050 (WIN `15000000,1,4998452` / `15000000,1,1871594`):
  **不消費**・adoption は scrutiny-owner C++ 第二実装 gate `9193f5b6…`
  専権 (本環境に C++ コンパイラなし)。
- aj030 / aj039 (EXHAUSTED `15000000,0,15000000`): honest UNKNOWN・
  同一条件 (15M・order=0・fresh-cold) の再探索禁止。高budgetでの再probeは
  別宣言必須。
- claim-reserved 2子 (probe_order 585/586 = batch-38 ai044/ai048):
  Part EF 所有・本 Part は pair レベルでも触れない。

## 3. 手法 (publish-then-execute・次回以降の実行が拘束される内容)

実験dir (次回): `research/experiments/n11-centralreply-closure-batch39-adoption-20261125/`
(最終名は次回の観察済みHEAD時の命名規約に従う)。

- **BASE**: canonical merged chain `fc3e4ac9…` (6,666行・s5verdict・
  Part EE af034loss1 adoption 後の最新)。実行時に、より新しい merged
  canonical cache が出版されている場合 (例: batch-38 adoption Part) は
  **BASE を最新の published merged chain に rebase し採用前後の両 pin を
  記録する (chain fork 禁止・単一 lineage)**。
- **merger**: pinned fail-closed merger `90711961…` の byte-clone 専権
  (改変禁止)。merger selftest 必須・merge 3回実行で byte-identical・
  merge-audit (全行unique・dup_elided 計数) ×3 同一sha。
- **maker (新規 fork・fail-closedモデルは Part EE `772c3c45…` /
  Part EC `a6a416ed…` 型)**: ゲート案 (実装時に確定・ここで事前登録):
  G-SSOT: batch-39 raws 46行の byte pin + honest label 照合 (LOSS である
  こと・EXH/WIN が混入しないこと) / G-accounting: 52子 = 2 claim-reserved
  + 46 LOSS + 2 EXH + 2 WIN の会計 / G-base: BASE pin 照合・46 pair が
  BASE に存在しないこと (Part EH audit A9 で機械済み・再検証) /
  G-winloss-conflict: 増分 vs BASE で WIN/LOSS conflict 0 /
  G-quarantine: 46 pair が quarantine `81d23160…` 非衝突 /
  G-fresh-increment: 増分が BASE の行と重複しない。
  maker 3x byte-identical・宣言済み battery ≥ 6 tamper fail-closed + control。
- **outputs (実行フェーズ)**: increment 46行・increments-manifest
  (schema b39loss-increments-manifest-v1 系・NODES/BUDGET pins 付与)・
  merged cache (BASE+46 = 6,712行想定・行数は実行時に機械確定)・
  merge-audit。**refresh reaudit wave** (Part EE fork `01937f23…` 型の
  refresh + extractor): closure-classes / per-root-coverage /
  decomp-deltas / refresh-summary 再導出 (class 30484 の unknown 構成変化
  は**reaudit の機械導出待ち・本宣言はいかなる数値も予告しない**)。
  metrics (worklist regen新規sha等) は bookkeeping。
- **停止規則**: merge非同一sha・conflict検出・maker fail → HARD-STOP・
  曖昧継続禁止。出版は fetch-back byte検証後のみ。kit出版と実行は
  2実行に分割可 (宣言 → kit出版 → 実行)。

## 4. 本宣言が今すぐ行わないこと

本宣言 commit は log のみで・canonical cache への書き込み・kit出版・
merge 実行を含まない (実行は宣言を拾った次回以降の hourly 実行が単一
オーナーとして行う)。**採用が完了するまで class 30484 の unknown_now は
不変であり・採用完了後も closure 判定は reaudit 導出分のみ**。

## 5. UNKNOWN担保・不接触

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 30484 は本 Part の実行・出版のどの時点でも
UNKNOWNのまま。** nodes数を勝敗や距離として読まない。被覆・閉鎖・
secured coverage・root勝敗の主張は一切しない。WIN 行の採用・closure
判定・free/excluded 判定は scrutiny owner C++ gate 通過後の別 Part 専権。

- BASE `fc3e4ac9…` は宣言時点で read-only 不変 (本宣言は何も書かない)。
- batch 1..38 各published dir・Part EE/EF/EG/EH 出版物 read-only 不接触。
  Part EF (batch-38 inc6待ち) は別オーナー・ai044/ai048 を含め一切触れない。
