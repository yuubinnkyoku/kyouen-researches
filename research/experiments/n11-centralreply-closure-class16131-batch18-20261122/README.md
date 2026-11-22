# n11 central-reply closure class 16131 exact-S5 probe batch 18 (Part AY, 2026-11-22)

Batch 18 of the central-reply 19-root closure grind (K0415/K0417 line).
単一オーナー宣言 (note Part AY amendment, 宣言コミットはstatus.logに記録)
に基づく**宣言+scaffold**出版。実行 (probes) は宣言後に
(Part AYプロトコルどおり本セッションを含む後続セッションが) 最新main確認のうえ
着手する。verdictは本scaffoldでは一切消費しない。

## base独立性 (本パケットの重要な性質)

本scaffoldの正本baseは**published** canonical exact-S5 verdict cache
(6,120行, sha256 `be9cb24e…`, Part AS adoptionの出力・main上の正本)。
Part AV (batch-17 adoption, 宣言のみで未出版) の成果物は一切読まない。
class 16131のunknown費用子53件はpublished baseから
(graph + cache + update8 receipts による機械再導出で) 完全に定まり、
Part AVの出版可否に依存しない: batch-17キーはclass 10661の費用子であり
16131の費用子と交わらないため、両base (6,120/6,172行) で
16131のunknown集合は同一53件になる (この事実自体もmakerの機械導出による)。

## 対象クラス

- graph class index **16131**, mask `[1154047404513693696, 64]`,
  published base再導出closure-candidate表 (候補809クラス) **rank 15**
  (unknown_now 53)。
- 選定理由 (機械検証済み・`scripts/make_batch18_keys.py` selection gate):
  rank 1-13 (23101, 16757, 20421, 16371, 30345, 12264, 5473,
  2634, 8785, 1518, 8106, 16930, 5830) はいずれも再導出unknown費用子と
  15 unconsumed closure WIN子 (b018/d002/e002/f017/g018/j033/h045/z003/
  n005/n006/p002/p003/r001/r002/q042) の交差が非空で全LOSS閉包ルート反駁済み
  (route statement・閉鎖不可)。rank 14 (class 10661, unknown 52) は
  WIN交差をもたないが、**52 unknown子すべてがpublished batch-17 packet
  (52キー・2-pass LOSS行52) ですでにprobe済み** (adoptionは別宣言Part AVが
  保留中・同budget再probeは規則上禁止)。
  **rank 15 class 16131は反駁証拠がなく・既probe子を持たない最初の候補**
  (unknown子と15-WINの交差空・18 published packet 875行との重複0・機械検証)。
  次点はrank 16 class 16513 (unknown 53)。
- グループ: closure (12,50)+(12,70)+(48,20)+(48,72)+(48,100)
  (first-seen (12,50), groups_served 5・機械再計算一致)。class cost 53子すべてが
  未確定 (graph status unknown(1)・機械検証)。

## バッチキー (53キー・すべて機械導出・機械検査)

- 出典: **graph cost子 ∩ canonical不在** (published 6,120行 cache +
  update8 receipts) の機械再導出。**worklist転写ゼロ**。s5_index昇順に
  v001..v053 を付番 (AV reaudit worklist由来のprobe_order 600..652順と
  同一順序・同一集合であることを本レーンで機械照合済み:
  key_id→(lo,hi,s5,legal,membership) 53/53同一)。
- key ids: **v001..v053** (b/c/d/e/f/g/h/j/m/z/n/p/q/r/t/u接頭辞と無衝突;
  batch 1-18で一意)。
- gates (すべてfail-closed・`scripts/make_batch18_keys.py` が再実行毎に検査):
  canonical BASE cache (published 6,120行・sha pinned) に**0/53 hits**、
  quarantine 0/53、canonical-safe形式 53/53、`mask_to_index` ==
  導出s5_index 53/53、全s5_indexがclass 16131のgraph cost子、
  **15 unconsumed closure WIN子はキーに不在 (全15子をpublished batch
  packetから再導出しgraph mask_to_indexで照合・canonical不在もgate)**、
  **batch 1..17 + batch-14 residual全キー (18 packet・875行・18ファイルsha固定取得)
  と重複0** (cross-packet共有位置14簿記は記録・batch-18キーとの重複は0)、
  Board(11)によるlegal再計算53/53 (legal 74..97・値はworklist由来でなく
  Board再導出)、membership_class_count もgraph cost関係から再導出53/53。
- maker 3回実行・byte一致 (batch-keys.json sha256 MANIFESTに記録・
  53枚のinput CSVもbyte一致・全書き込みファイルのre-read durability gate込み)。

## 実行protocol (事前登録・実行セッションが遵守)

- pinned replica `jsreplay.js` (sha256 `84585617…` = batch-17正本の
  byte-copy)。2-pass fresh cold、budget **15,000,000**、
  1 solver / 1 row / 1 process、publish=ALL、workerは最大2。
- 実行前にpublished two-target-design 4行のval-gateを本環境で再現
  (node数一致必須・kit `output/val-gate` と同じ4行)。
- 停止規則: (1) determinism mismatch → 即時HARD-STOP (rc=42) 以後の
  キー着手不可。(2) WIN (result 1) → 即時HALT (rc=45)。当該rawは誠実
  ラベルで記録しbatch停止。**WINは本レーンでは採用しない** (verdict
  不消費・scrutiny owner待ち)。(3) budget枯渇 (result 0) → honest UNKNOWN。
  15M同条件の再探索は禁止。
- 消費規則: 2-pass一致かつresult 2 (LOSS) のキーのみ、後続の別宣言
  adoption Partでsha-pinned fail-closed union merger (`90711961…`) 経由で
  canonical計上の候補とする (採用まで本batch単体ではroot被覆・クラス閉鎖・
  第三手securedの主張をしない)。15 unconsumed closure WINはscrutiny owner
  (C++第二実装 gate pin `9193f5b6…`) 待ち・不変。
- 資源: 各wave後にknowledge kitミラーへの退避・repoへのcheckpoint pushは
  小分けに行う。CPU並列は最大2 worker。
- 並走との不接触: Part AV (batch-17 class 10661 adoption+reaudit) の
  成果物 (cache 6,172行・reaudit出力) には本Partは一切書き込まない・
  読まない。Part AV出版後も本batchキーとの重複は0 (機械検証済み)。

## Interpretation guard

標準11×11空盤・19 central-reply roots・class 16131 (unknown 53子)・
全53キー・他の全classは本scaffoldのどの時点でもUNKNOWNのまま。
nodes数・legal数・probe countは簿記であって勝敗ではない。閉鎖・被覆・
secured主張は一切しない (reaudit + 独立監査の仕事)。
