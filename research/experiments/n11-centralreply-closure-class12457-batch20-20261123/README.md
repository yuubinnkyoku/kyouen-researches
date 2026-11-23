# n11 central-reply closure class 12457 exact-S5 probe batch 20 (Part BG, 2026-11-23)

Batch 20 of the central-reply 19-root closure grind (K0415/K0417 line).
単一オーナー宣言 (note Part BG amendment, 宣言コミット `b4c4ac2d`・
note blob `becd61ac0dce24c89abb98091382a1541be90a7d`・status.logに記録) に基づく
**宣言+scaffold+実行+出版**。verdictは本Partでは一切消費しない。

## base独立性

本scaffoldの正本baseは**published** canonical exact-S5 verdict cache
(6,182行, sha256 `0b594f7e…`, Part BC batch-14residual 10-LOSS adoptionの
出力・main上の正本)。probe worklist等の非公開成果物は一切読まない
(キー導出はgraph + published cache + update8 receiptsのみ)。
class 12457のunknown費用子53件はpublished baseから機械再導出で完全に定まる。

## 対象クラス (selection correction込み・機械検証済み)

- graph class index **12457**, mask `[1152921504606847268, 0]`,
  published base再導出closure-candidate表 **rank 17** (unknown_now 53)。
- **選定訂正の誠実記録**: batch-19 READMEの次候補指針 (rank 16 class 5687) は
  既知WIN費用子 s5 209644 (update8 receipt verdict 1) を持ち、published
  Part BC refresh rule (`d6bb2374…`: 既知WIN費用子を持つclassはexcluded) により
  all-LOSS閉包ルートが既に反駁されている (route-dead・機械検証)。
  **rank 17 class 12457がpublished-table順で最初のroute-alive候補**
  (unknown費用子53・19 unconsumed closure WIN子との交差0・既知子は
  {126899: LOSS} のみ・graph cost 54子)。
- runner-up rank 18 class 12643・backups 25835/31600も同様にroute-alive機械検証済み
  (将来のbatch候補)。
- グループ: (2,5)+(2,8)+(5,2)+(5,8)
  (first-seen (2,5), groups_served 4・機械再計算一致)。
- class cost 54子のうち既知子 {126899: LOSS} 1件を除く53子すべてが未確定
  (graph status unknown(1)・機械検証)。

## バッチキー (53キー・すべて機械導出・機械検査)

- 出典: **graph cost子 ∩ canonical不在** (published 6,182行 cache +
  update8 receipts) の機械再導出。**worklist転写ゼロ**。
  s5_index昇順に x001..x053 を付番。
- key ids: **x001..x053** (b/c/d/e/f/g/h/j/m/z/n/p/q/r/t/u/v/w接頭辞と
  無衝突; batch 1-20で一意)。
- gates (すべてfail-closed・`scripts/make_batch20_keys.py` が実行毎に検査):
  canonical BASE cache (published 6,182行・sha pinned) に**0/53 hits**、
  quarantine 0/53、canonical-safe形式 53/53、`mask_to_index` ==
  導出s5_index 53/53、全s5_indexがclass 12457のgraph cost子、
  **19 unconsumed closure WIN子はキーに不在**、
  **batch 1..19 + 各residual全キー (20 packet・981行・sha固定取得→
  967 unique; 14重複位置は各2 packet間) と重複0**、
  Board(11)によるlegal再計算53/53 (legal 76..96・Board再導出)、
  membership_class_count もgraph cost関係から再導出53/53、
  ranks 1..16の反駁証拠列挙・route-alive gate (12457/12643/25835/31600)。
- maker 3回実行・byte一致 (batch-keys.json sha256
  `efb40b1bb7a43595bb8d014a31af2b878c404be86b8f9d5abc717eb176d1ed51`・
  53枚のinput CSVもbyte一致)。開発中のPRIOR_BATCHES pinの落字事故は公開
  batch-19 maker (mk19.py) からのbyte-copyで修復し、batch-19 packet pinが
  MANIFEST published値 `9609aaf3…` と一致することを検証済み (誠実記録)。

## 実行protocol (事前登録・実行前に出版)

- pinned replica `jsreplay.js` (sha256 `84585617…` = batch-17/18/19正本の
  byte-copy)。2-pass fresh cold、budget **15,000,000**、
  1 solver / 1 row / 1 process、publish=ALL、workerは最大2。
- 停止規則: (1) determinism mismatch → 即時HARD-STOP (rc=42)。
  (2) WIN (result 1) → 即時HALT (rc=45)。WINは本レーンでは採用しない
  (verdict不消費・scrutiny owner待ち)。(3) budget枯渇 (result 0) →
  honest UNKNOWN。15M同条件の再探索は禁止。
- 実行環境の制約のため、本hostではpublished `runbatch.sh` (byte-pinned
  `f591f8c2…`) を「残キー奇偶分割2 worker・~260秒有界foreground起動」の
  driver (`scripts/drive_batch20.sh`・同梱・batch意味論は持たない) から
  反復起動した (7回)。完了passは再実行されず、中断断片はpublished
  completeness guard (`# replay_done` 検査) がfresh coldで再実行する。
- val-gate: 実行前に本hostで4/4 node-exact再現
  (at2m 0/2,000,000 x2・15m (2,3,651,923)/(2,5,040,200)・禁止四角95,670 x4・
  `# replay_done` x4)。published batch-19 val-gate基線とnode数完全一致。

## 実行結果 (2026-11-23, 53/53完走・verdict不消費)

- drive 7起動・最終起動は両worker rc=0で全キー完遂。53/53キー
  **PASS (p1==p2 node-exact, budget 15,000,000内, `# replay_done` x106)**。
- **53ラベルすべて result=2 (LOSS, pinned contract通り)**: honest labels
  として記録しただけで**採用候補にすぎない** (消費は別宣言adoption Partが
  pinned fail-closed mergerで実行; canonical cache 6,182行 `0b594f7e…` は
  書き込みゼロ)。
- WIN 0 (WIN-HALT規則不発動)・exhausted 0 (15M再探索禁止規則に該当なし)・
  mismatch 0。
- host interruption: 14 truncated-retry eventsを誠実記録 (timeout killに
  よる断片は`output/raw/*.truncated.*.out`として保存・fresh cold再実行済み)。
- row audit PASS (`scripts/row_audit_batch20.py` `3197c4dc…`):
  `output/row-audit.json` (sha256 `1dcb7fb8…`) 53 pass rows・LOSS 53・
  WIN 0・exhausted 0・mismatches 0・input `efb40b1b…`照合済み。
- 簿記注記: driveのPROGRESS表示が最終時に54/53となるのはstatus.logの
  文書ヘッダ行の "PASS" tokenをkey id誤拾いする既知の表示アーティファクト
  (実キー53行のeach-once・一意性は機械検証済み)。
- route statement (条件付き・verdictではない): class 12457の54子のうち
  残る未確定子は本Part以降ゼロ (既知{126899 LOSS} + probe 53 = 54)。
  53 LOSS行が将来のadoption Partで採用されればclass 12457の全子LOSS
  閉包ルートが確定する。**本Partは採用しない。**
- 消費: **ゼロ**。19 unconsumed closure WIN候補 (b018/d002/e002/f017/
  g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042/v001/v002/
  w001 (s5 63802)/w002 (s5 109169)) は読み書きとも非接触
  (scrutiny owner C++ gate `9193f5b6…`のまま)。

## Interpretation guard

標準11×11空盤・19 central-reply roots・class 12457 (54子)・全53キー・
他の全classは本Partのどの時点でも**UNKNOWNのまま**。
nodes数・legal数・probe countは簿記であって勝敗ではない。閉鎖・被覆・
secured主張は一切しない (reaudit + 独立監査 + adoption Partの仕事)。
