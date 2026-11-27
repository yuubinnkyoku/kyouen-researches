# 2026-11-27 高速レーン: 7行・q=4 幅69 完全two-edit近傍掃引 (局所負)

単一オーナー宣言: `research/log/2026-11-27-seven-row-q4-band-m69-single-owner.md`
(宣言 2026-11-27T05:45Z・宣言時 HEAD `b782b8468b5e0a0336b6bc74a9c617c905ca108c`)。

## 背景

`seven-row-q4-witness-band-60plus-20261121` の完結時点で witness 帯は m=4..68
(M_{7,4} ∈ [69,1929]・前線 7×69) で、幅69は w68 witness 基底1つの fresh 2-for-2
近傍で 0 件 (`stats_69.json`) のみ。出版済み `sweep69.js`/`sweep69h.js` 手順の
全199基底掃引は未実行・未出版だった。

## 成果

1. **fresh 2-for-2 全199基底完全掃引 (幅69)**: 426,099,795 row-capacity 候補 / 43,009,353 safe / **0 safe maximal
   row-deficient** (199/199 基底・rcc 全件 2,141,205)。
2. **holes 2-for-2 全199基底完全掃引 (幅69)**: 435,695,973 候補 /
   45,368,697 safe / **0 safe maximal row-deficient** (holes safe は
   fresh の基底ごと上位集合 199/199)。fresh ∪ holes で「高々2削除・高々2追加・
   最終20石」近傍が完全枯渇 (1-swap 最終状態は holes の refill で被覆)。
3. **D4鏡像×並進 census (K1211手順・全199基底×4鏡像×dx=0..199)**: 並進被覆
   最大幅は **67** (w65 系基底)。幅69を被覆する純並進 witness なし。
4. **M_{7,4} ∈ [69,1929] 不変** (下界・上界とも不変・csv 不更新)。
   前線は 7×69 のまま。幅69全体の不在主張はしない (edit distance >= 3 swap
   の構成は除外されていない)。

## 検証 (全て機械実行・`output/w69/calibration.json` all_pass)

- 較正: base53@7×57 fresh = pinned 値 1,436,643/60,921/2 完全一致。
  w68 witness 基底@幅69 = 出版 `stats_69` 値 2,141,205/199,290/0 完全一致。
- 陽性対照: 幅68 fresh で w65 基底 23個中ちょうど3個が各1件の maximum を持ち、
  3件とも出版の唯一の幅68 witness と同一 (出版主張の完全再現)。
- 決定性: 幅69 fresh 3基底の再実行が results.jsonl と 3/3 計数一致。
  census 再実行は stdout byte 同一。
- tamper: 基底1石移動・1石削除はともに fail-closed (`unsafe base`)。
  全199 fresh 記録が rcc=2,141,205・maximal=0 で 0/199 逸脱。

## 正直開示

- (a) 採引ドライバ (`sweep69run.js`/`sweep69hrun.js`) は出版 `sweep69.js`/
  `sweep69h.js` の列挙・Board・record schema と同一手順の resume-safe 再実装
  (start index の代わりに sig-based resume)。列挙本体 `enum_two.js` は出版の
  byte-clone (sha256 `ab58c34a…`) で改変なし。
- (b) census 初版は全 cell に対する verify 全呼びで wall 超過 (1回の実行環境
  reset で作業 tree を喪失・knowledge mount `_7row-w69/` に再構築して継続)。
  解析的交点計算 (直線×行は高々1点・円×行は判別式) に改修後に 199基底全走査。
- (c) 7×69 盤は x鏡像 (x→68−x)・y鏡像で不変のため、199基底の掃引は
  dx=0 のD4鏡像の近傍も暗黙に被覆する (census は dx≠0 の並進のみが新規)。
- (d) 幅68 の w68 witness 基底自身の fresh 幅68 近傍は maximal=3 (出版物には
  基底として未登載のため矛盾なし・出版の「w65 3基底から同一 witness」主張と
  陽性対照で整合確認済み)。
- (e) 全成果は有限機械列挙であって数論的証明ではない。勝敗・被覆の主張なし。

## 次の実行可能課題

- 幅69 witness: 3-swap 近傍 (帰納的手法の拡張が必要で本環境の wall では
  完全列挙不可)・seeded SA (K0827 の sa42..53 手順の幅69版)・frontier breadth
  拡大。witness が見つかれば M_{7,4} ∈ [70,1929] に更新。
- 標準 11×11 空盤・二石 root {60,27}・第三手 {100,108}・S2・closure class は
  本レーンと無関係で全時点 UNKNOWN・verdict 不消費。

## 追記: 幅69 seeded SA 負記録 (2026-11-27 同セッション)

出版済み `search_seeded.js`（seven-row-q4-band-42-56-20261115・改変なし・
sha256 は実験キット README 参照）を 7×69 盤 (q=4) で実行した。
seed は幅68 witness（`witnesses_68.json`・20石）そのまま。

- seed 1 (budget 260s): best **21石**（w68 witness + (68,6)・iters 87,747）。
- seeds 5, 7 (budget 900s each): ともに best **21石**（同一配置・
  iters 160,236 / 157,243・改善イベント 0・rejects 0）。
- 曲線census 1,161,122 本・build 12.3s（単走時）〜74s（並走時）。

3走とも 20石への降下なし（maximalize が (68,6) を埋めて 21石から
始まり、SA は一度も 20石以下に到達しなかった）。ヒューリスティック
探索の未発見記録であり、7×69 witness の不在主張ではない。次の候補は
3-for-3 近傍・frontier breadth 拡大・別 seed（幅65 witness 群）・
holes 幅70 掃引の先送り判断材料。

実行生ログ: `output/w69/sa/seed{1,5,7}.jsonl`（seed1 は stdout 全量、
seed5/7 は改善なしで最終行のみ）。seeds 2,3,4,6 は6並走起動時に
環境上限で沈黙消失（出力なし・計上しない）。
