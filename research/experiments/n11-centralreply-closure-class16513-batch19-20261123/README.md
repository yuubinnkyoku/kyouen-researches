# n11 central-reply closure class 16513 exact-S5 probe batch 19 (Part BE, 2026-11-23)

Batch 19 of the central-reply 19-root closure grind (K0415/K0417 line).
単一オーナー宣言 (note Part BE amendment, 宣言コミット `2dbb6714`・
status.logに記録) に基づく**宣言+scaffold+実行**出版。
verdictは本Partでは一切消費しない。

## base独立性

本scaffoldの正本baseは**published** canonical exact-S5 verdict cache
(6,182行, sha256 `0b594f7e…`, Part BC batch-14residual 10-LOSS adoptionの
出力・main上の正本)。probe worklist等の非公開成果物は一切読まない
(キー導出はgraph + published cache + update8 receiptsのみ)。
class 16513のunknown費用子53件はpublished baseから機械再導出で完全に定まる。

## 対象クラス

- graph class index **16513**, mask `[1153202980657299456, 67108864]`,
  published base再導出closure-candidate表 (候補808クラス) **rank 15**
  (unknown_now 53)。
- 選定理由 (機械検証済み・`scripts/make_batch19_keys.py` selection gate):
  rank 1-14 (23101, 16757, 20421, 16371, 30345, 12264, 5473,
  2634, 8785, 1518, 8106, 16930, 5830, 16131) はいずれも再導出unknown費用子と
  **17 unconsumed closure WIN子** (b018/d002/e002/f017/g018/j033/h045/z003/
  n005/n006/p002/p003/r001/r002/q042/v001/v002) の交差が非空
  (rank 1 class 23101のunknown集合は {745184} = 未採用q042 WIN行のみ)。
  **rank 15 class 16513は反駁証拠がなく・既probe子を持たない最初の候補**
  (unknown子と17-WINの交差空・batch 1..18 + residual全19 packet
  928行・914位置との重複0・機械検証)。次点 (runner-up) はrank 16
  class 5687 (unknown 53・WIN交差0・同様にclean)。
- グループ: closure (24,50)+(24,70)+(24,96)+(48,30)+(48,90)
  (first-seen (24,50), groups_served 5・機械再計算一致)。
  class cost 53子すべてが未確定 (graph status unknown(1)・機械検証)。

## バッチキー (53キー・すべて機械導出・機械検査)

- 出典: **graph cost子 ∩ canonical不在** (published 6,182行 cache +
  update8 receipts) の機械再導出。**worklist転写ゼロ**。
  s5_index昇順に w001..w053 を付番。
- key ids: **w001..w053** (b/c/d/e/f/g/h/j/m/z/n/p/q/r/t/u/v接頭辞と
  無衝突; batch 1-19で一意)。
- gates (すべてfail-closed・`scripts/make_batch19_keys.py` が実行毎に検査):
  canonical BASE cache (published 6,182行・sha pinned) に**0/53 hits**、
  quarantine 0/53、canonical-safe形式 53/53、`mask_to_index` ==
  導出s5_index 53/53、全s5_indexがclass 16513のgraph cost子、
  **17 unconsumed closure WIN子はキーに不在** (全17子をpublished batch
  packet 19ファイルから再導出しgraph mask_to_indexで照合・canonical不在もgate)、
  **batch 1..18 + batch-14 residual全キー (19 packet・928行・19ファイルsha固定取得)
  と重複0** (cross-packet共有位置14簿記は記録・batch-19キーとの重複は0)、
  Board(11)によるlegal再計算53/53 (legal 73..95・Board再導出)、
  membership_class_count もgraph cost関係から再導出53/53。
- maker 3回実行・byte一致 (batch-keys.json sha256
  `9609aaf3…`・53枚のinput CSVもbyte一致・全書き込みファイルのre-read
  durability gate込み)。なお開発中にbatch-11 packet pinの1文字typoを
  makerのsha gateが捕捉・修正した事実は誠実記録 (gateが設計どおりに
  働いたことの実証)。

## 実行protocol (事前登録・実行前に出版)

- pinned replica `jsreplay.js` (sha256 `84585617…` = batch-17/18正本の
  byte-copy)。2-pass fresh cold、budget **15,000,000**、
  1 solver / 1 row / 1 process、publish=ALL、workerは最大2。
- 停止規則: (1) determinism mismatch → 即時HARD-STOP (rc=42)。
  (2) WIN (result 1) → 即時HALT (rc=45)。当該rawは誠実ラベルで記録し
  batch停止。**WINは本レーンでは採用しない** (verdict不消費・scrutiny
  owner待ち)。(3) budget枯渇 (result 0) → honest UNKNOWN。15M同条件の
  再探索は禁止。
- 実行環境の制約のため、本hostではpublished `runbatch.sh` (byte-pinned
  `f591f8c2…`) を「残キー奇偶分割2 worker・~260秒有界foreground起動」の
  driver (`scripts/drive_batch19.sh`・同梱・batch意味論は持たない) から
  起動した。完了passは再実行されず、中断断片はpublished completeness guard
  (`# replay_done` 検査) がfresh coldで再実行する。
- val-gate: 実行直前に本hostで4/4 node-exact再現
  (at2m 0/2,000,000 x2・15m (2,3,651,923)/(2,5,040,200)・禁止四角95,670 x4)。

## 実行結果 (2026-11-23, WIN-HALTによる停止・verdict不消費)

事前登録のWIN-HALT規則により、batch-19は最初のwaveで停止した
(batch-18と同一の停止パターン)。

- **w001: WIN (result 1)**・2-pass fresh cold node-exact
  (p1=p2=6,639,780 nodes・budget 15,000,000内・legal 84・
  `# replay_done` x2・s5 63802・keys 1153202980791517184/67108864・
  wall_s 67/67)。**採用しない** (verdict不消費・scrutiny owner C++ gate
  `9193f5b6…` 待ち)。holder (cost子graph関係): class 1363 (unknown),
  16513 (unknown)。
- **w002: WIN (result 1)**・2-pass node-exact (p1=p2=7,738,714 nodes・
  legal 89・`# replay_done` x2・s5 109169・keys
  10376575017512075264/67108864・wall_s 81/67)。同WIN-HALT。
  holder: class 2901 (unknown), 16513 (unknown)。
  両キーは対抗する2 workerが独立に最初のキーとして完了したもの
  (排他制御上の問題なし・rawはworker毎に分離)。
- **2/53キーprobe済み・51キー未着手 (fresh)**。未着手キーは一度も
  実行されていないため15M再探索禁止規則には該当しない
  (将来のPartが同じbatchを継続できる)。
- host interruptionなし (truncated pass 0)。
- 消費: **ゼロ**。unconsumed closure WIN候補は17+2=**19**
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/
  r002/q042/v001/v002/**w001/w002**)、すべてscrutiny owner待ち。
- route statement (条件付き・verdictではない): class 16513の費用子に
  WINが1つでも採用されれば、class 16513の全子LOSS閉包ルートは反駁
  される。**class 16513 (残51子)・標準11×11空盤・19 rootsは本時点で
  UNKNOWNのまま。**
- 本時点の2 WIN行はgrepベースの機械検証 (p1==p2 node-exact・budget内・
  `# replay_done`・status.log整合・キー一致) 済み。row-audit
  (`scripts/row_audit_batch19.py`) はbatch完走時点 (残51キーの継続Part)
  に全行機械検証する。

## Interpretation guard

標準11×11空盤・19 central-reply roots・class 16513 (unknown 53子)・
全53キー・他の全classは本Partのどの時点でもUNKNOWNのまま。
nodes数・legal数・probe countは簿記であって勝敗ではない。閉鎖・被覆・
secured主張は一切しない (reaudit + 独立監査の仕事)。
