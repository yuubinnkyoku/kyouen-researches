# n11 central-reply closure class 12643 exact-S5 probe batch 21 (Part BJ, 2026-11-23)

Batch 21 of the central-reply 19-root closure grind (K0415/K0417 line).
単一オーナー宣言 (note Part BJ amendment, 宣言コミット `2bf5d529`・
note blob `23ea8560bbd191d8c1ba0408a8dc5637d999e17b`・preflight込み) に基づく
**宣言+scaffold+実行+出版 (publish-then-execute)**。verdictは本Partでは
一切消費しない。

## base独立性

本scaffoldの正本baseは**published adopted** canonical exact-S5 verdict cache
(**6,235行, sha256 `f6649fe3…`**, Part BI batch-20 53-LOSS adoptionの出力・
main上の正本)。probe worklist等の非公開成果物は一切読まない
(キー導出はgraph + adopted cache + update8 receiptsのみ)。
class 12643のunknown費用子53件はpublished baseから機械再導出で完全に定まる。

## 対象クラス (機械検証済み)

- graph class index **12643**, mask `[1152921504606847088, 0]`,
  adopted base再導出closure-candidate表 **rank 17** (unknown_now 53)。
  Part BI採用によりclass 12457が候補表から退出 (808→807行) した結果の
  繰り上げ (機械分類delta・宣言通り)。
- **rank 17 class 12643がpublished-table順で最初のroute-alive候補**
  (unknown費用子53・19 unconsumed closure WIN子との交差0・既知子は
  {137694: LOSS} のみ・graph cost 54子)。ranks 1..16はすべて反駁証拠保持
  (19-WIN intersection、または既知WIN費用子: class 5830 はreceipt WIN子
  {126017,131631,162106,197665,206386} 5件・class 5687 は既知WIN子
  {209644})。rank 1 class 23101のunknown境界は {745184}のみ (q042 WIN行)。
- runner-up rank 18 class 25835・backup rank 19 class 31600も同様に
  route-alive機械検証済み (将来のbatch候補)。
- グループ: (4,5)+(4,6)+(5,4)+(5,6)
  (first-seen (4,5), groups_served 4・機械再計算一致)。
- **NEW gate (batch-21 maker)**: 再導出rank表 (807行) がpublished Part BI
  refresh reaudit closure表 (`d57a7609…`) と**全807行で一致**することを
  検査 (prose転写ゼロ)。さらに**batch-20採用tie**: published batch-20
  packet x001..x053の53位置がすべてadopted base cacheでLOSS(2)であること・
  class 12457のunknown境界が採用後ゼロであることを機械検査
  (Part BI adoptionをpacket→cacheのbyte関係でpin)。

## バッチキー (53キー・すべて機械導出・機械検査)

- 出典: **graph cost子 ∩ canonical不在** (published 6,235行 cache +
  update8 receipts) の機械再導出。**worklist転写ゼロ**。
  s5_index昇順に a001..a053 を付番。
- key ids: **a001..a053** (b/c/d/e/f/g/h/j/m/z/n/p/q/r/t/u/v/w/x接頭辞と
  無衝突; batch 1-21で一意)。
- gates (すべてfail-closed・`scripts/make_batch21_keys.py` が実行毎に検査):
  adopted BASE cache (published 6,235行・sha pinned) に**0/53 hits**、
  quarantine 0/53、canonical-safe形式 53/53、`mask_to_index` ==
  導出s5_index 53/53、全s5_indexがclass 12643のgraph cost子、
  **19 unconsumed closure WIN子はキーに不在**、
  **batch 1..20 + 各residual全キー (21 packet・1,034行・sha固定取得→
  1,020 unique; 14重複位置は各2 packet間) と重複0**、
  Board(11)によるlegal再計算53/53 (legal 74..96・Board再導出・宣言通り)、
  membership_class_count もgraph cost関係から再導出53/53、
  ranks 1..16の反駁証拠列挙・route-alive gate (12643/25835/31600)。
- maker 3回実行・byte一致 (batch-keys.json sha256
  `1f9346a7027e95b162f27b933bddec05151473d87ab7ed35832619026ae6759d`・
  53枚のinput CSVもbyte一致)。開発中のpin手転写事故 (batch-6/batch-12の
  PRIOR_BATCHES sha 2件) はfail-closed sha gateがすべて捕捉・published
  batch-20 makerからのbyte-copyで修復 (誠実記録)。

## 実行protocol (事前登録・実行前に出版)

- pinned replica `jsreplay.js` (sha256 `84585617…` = batch-19/20正本の
  byte-copy)。2-pass fresh cold、budget **15,000,000**、
  1 solver / 1 row / 1 process、publish=ALL、workerは最大2。
- 停止規則 (事前登録): (1) determinism mismatch → 即時HARD-STOP (rc=42)。
  (2) WIN (result 1) → 即時HALT (rc=45)。WINは本レーンでは採用しない
  (verdict不消費・scrutiny owner待ち)。(3) budget枯渇 (result 0) →
  honest UNKNOWN。15M同条件の再探索は禁止。
- 実行環境の制約のため、本hostではpublished `runbatch.sh` (byte-pinned
  `f591f8c2…`) を「残キー奇偶分割2 worker・~260秒有界foreground起動」の
  driver (`scripts/drive_batch21.sh`・同梱・batch意味論は持たない) から起動
  (drive 1回)。完了passは再実行されず、中断断片はpublished completeness
  guard (`# replay_done` 検査) がfresh coldで再実行する。
- val-gate: 実行前に本hostで4/4 node-exact再現
  (at2m 0/2,000,000 x2・15m (2,3,651,923)/(2,5,040,200)・禁止四角95,670 x4・
  `# replay_done` x4)。published batch-20 val-gate基線
  (`*.published-baseline.out` として同梱) とnode数完全一致 (wall_s除外)。

## 実行結果 (2026-11-23, pre-registered WIN-HALT・4/53完走・verdict不消費)

- drive 1起動・**a003でWIN (result 1, two-pass node-exact,
  nodes 5,021,280) → 事前登録WIN-HALT (rc=45) が発動しbatch停止**。
- 完了 (two-pass node-exact・`# replay_done` x8) は4キー:
  **a001 LOSS (result 2, nodes 2,392,778)**・
  **a002 LOSS (result 2, nodes 6,755,079)**・
  **a003 WIN (result 1, nodes 5,021,280)**・
  **a004 LOSS (result 2, nodes 4,151,964)**。
  (a002はp1/p2がbyte同一・wall_s 67/67。a003のp1/p2はnode-exact。
  status.logにPASS判定行+WIN-HALT行の両方を記録 [`runbatch.sh` の
  出力順序どおり])。
- **a003のWINはhonest labelのみ**。本レーンでは採用しない
  (scrutiny owner C++第二実装 gate `9193f5b6…` のまま・verdict不消費)。
- **a006はUNPROBED**: 第2workerがtimeout killされた時点でp1完了
  (single pass・bookkeeping result 2, nodes 8,008,743・**単一passは
  証拠ではない**)・p2は`# replay_done`を持たないtruncated断片
  (`output/raw/a006.p2.out`・headersのみ)。
  両ファイルとも証拠として採らない。将来の継続 (batch-21 residual) が
  published completeness guard経由でfresh cold再実行する (完了passの
  再実行ゼロというguard設計)。
- 残り**49キー (a005..a053) はUNPROBED (fresh・再probe禁止規則非該当)**。
- loss 3・win 1・exhausted 0・mismatch 0。
- row audit PASS (`scripts/row_audit_batch21_win_halt.py`):
  `output/row-audit-winhalt.json` (sha256 `5bb403ad…`) 3回byte一致・
  completed 4・LOSS 3・WIN 1・fragment (a006) unprobed検査込み・
  unprobed 49キーへのstatus.log verdict行不存在も機械検査。
- route statement (条件付き・verdictではない): a003 (s5 115192,
  key (10412339930666631168,4)) はclass 12643の費用子でclosure候補クラスの
  unconsumed closure WIN子 20番目に相当する簿記候補 (19既存 + a003・
  すべてscrutiny owner待ち)。よって将来のbatch選定ではclass 12643の
  all-LOSS closureルートはrefutation evidenceを1件持ち、次batchは
  runner-up **rank 18 class 25835** (route-alive機械検証済み) が
  published-table順の首位候補となる (条件付き・本Partは選定しない)。
  3 LOSS行 (a001/a002/a004) は**採用候補にすぎない** (消費は別宣言
  adoption Partがpinned fail-closed merger `90711961…`で実行)。
- 消費: **ゼロ**。canonical cache 6,235行 `f6649fe3…` は書き込みゼロ。
  19 unconsumed closure WIN候補 (b018/d002/e002/f017/g018/j033/h045/
  z003/n005/n006/p002/p003/r001/r002/q042/v001/v002/w001/w002) は
  読み書きとも非接触。Part BH (batch-19 residual `de1383a7`) ・
  y18/y19 fast lane・K1058系は非接触。

## Interpretation guard

標準11×11空盤・19 central-reply roots・二石root・S2 {59,60}・
class 1/2/4・class 12643 (54子・53キーすべて含む)・その他全classは本Partの
どの時点でも**UNKNOWNのまま**。nodes数・legal数・probe countは簿記であって
勝敗ではない。閉鎖・被覆・secured主張は一切しない。
