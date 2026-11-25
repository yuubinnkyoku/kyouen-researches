# n11 central-reply closure class 10661 exact-S5 probe batch 17 (Part AU, 2026-11-22)

Batch 17 of the central-reply 19-root closure grind (K0415/K0417 line).
単一オーナー宣言 (note Part AU amendment, 宣言コミットはstatus.logに記録)
に基づく**宣言+scaffold**出版。実行 (probes) は宣言後に別セッションが
最新main確認のうえ着手する。verdictは本scaffoldでは一切消費しない。

## 対象クラス

- graph class index **10661**, mask `[1152921505697431552, 0]`,
  Part AS reaudit closure-candidate表 **rank 14** (unknown_now 52)。
- 選定理由 (機械検証済み): rank 1 (class 23101) は未着手q043-q052の
  10キー+未採用q042保持でin-flight。rank 2-13 (16757, 20421, 16371,
  30345, 12264, 5473, 2634, 8785, 1518, 8106, 16930, 5830) はいずれも
  unconsumed closure WIN子 (b018/d002/e002/f017/g018/j033/h045/z003/
  n005/n006/p002/p003/r001/r002) を費用子に持ち全LOSS閉包ルート反駁済み
  (route statement・閉鎖不可)。**rank 14 class 10661は反駁証拠のない
  最初の候補**。
- グループ: closure (24,30) + (24,90) (first-seen (24,30),
  groups_served 2・機械再計算一致)。class cost 53子中52子が未確定
  (graph status unknown(1)・機械検証)。

## バッチキー (52キー・すべて機械導出・機械検査)

- 出典: Part AS reaudit probe-worklist (sha256 `1c96df05…`,
  publication済み正本) の `serving_class == 10661` 行52件、
  probe_order 600..651 (連続・昇順・機械検証)。
- key ids: **u001..u052** (= これまでの b/c/d/e/f/g/h/j/m/z/n/p/q/r/t
  と無衝突)。
- gates (すべてfail-closed・`scripts/make_batch17_keys.py` が再実行毎に
  検査): canonical BASE cache (`be9cb24e…`, 6,120行) に**0/52 hits**、
  quarantine 0/52、canonical-safe形式 52/52、`mask_to_index` ==
  worklist s5_index 52/52、全s5_indexがclass 10661のgraph cost子、
  未採用q042 WIN子 (s5 745184) はキーに不在、**batch 1..16全キー
  (813キー・16ファイルsha固定取得) と重複0**、Board(11)による
  legal再計算がworklist legal値と52/52一致 (legal 72..97)。
- maker 3回実行・byte一致 (batch-keys.json sha256
  `db762175272206aa53622f30addc1267d534e8a3e576f70c6a084f21392645d2`、
  52枚のinput CSV集合もbyte一致)。

## 実行protocol (事前登録・実行セッションが遵守)

- pinned replica `jsreplay.js` (sha256 `84585617…` = batch-14正本の
  byte-copy)。2-pass fresh cold、budget **15,000,000**、
  1 solver / 1 row / 1 process、publish=ALL、workerは最大2。
- 実行前にpublished two-target-design 4行のval-gateを本環境で再現
  (node数一致必須・kit `input/val-gate` 手順)。
- 停止規則: (1) determinism mismatch → 即時HARD-STOP (rc=42) 以後の
  キー着手不可。(2) WIN (result 1) → 即時HALT (rc=45)。当該rawは誠実
  ラベルで記録しbatch停止。**WINは本レーンでは採用しない** (verdict
  不消費・scrutiny owner待ち)。(3) budget枯渇 (result 0) → honest
  UNKNOWN。15M同条件の再探索は禁止。
- 消費規則: 2-pass一致かつresult 2 (LOSS) のキーのみ、fail-closed union
  merger (`90711961…`) によるincrement cache候補として後続のadoption
  Part (宣言別) で計上してよい。本batch単体ではroot被覆・クラス閉鎖・
  第三手securedの主張をしない (判定は後続のrefresh再実行+独立監査)。

## verdict消費の範囲とguards

- 本scaffoldは**いかなるverdictも消費しない**。canonical cacheは
  6,120行 (`be9cb24e…`) 不変。
- 15 unconsumed closure WIN (b018/d002/e002/f017/g018/j033/h045/z003/
  n005/n006/p002/p003/r001/r002/q042) は採用判断 scrutiny owner
  (C++第二実装 gate pin `9193f5b6…`) 待ち・不変。
- **標準11×11空盤・19 central-reply roots・class 10661 (unknown 52子)・
  全52キーはどの時点でもUNKNOWNのまま。nodes数・legal数を勝敗として
  読まない。**
- 並走との不接触: 本バッチキーは19-root closure grind由来で、{60,27}系
  レーン (sixth-cost, s4bd, thirdimpl bank, win7/win8 chains) のclaim
  集合と機械的にdisjoint (batch 1-16重複0で担保)。同一スコープ
  (batch-17 / class 10661) の対抗宣言が既にmainにある場合は本scaffoldを
  破棄して着手しない。

## ファイル

- `input/batch-keys.json` — 52キー正本 (schema
  `n11-centralreply-closure-class10661-batch17-input-v1`,
  sha256 `db762175…`)。
- `input/u001..u052.input.csv` — solver target行
  (`target,0,5,lo,hi,legal,0,0,0,0,0`) 52枚。
- `scripts/make_batch17_keys.py` — scaffold maker (全gate内蔵・3回
  byte一致)。
- `README.md` / `status.log` / `MANIFEST-sha256.txt` — 本宣言正本。

## 実行結果 (Part AU execution session, 2026-11-22)

宣言 (`adc4358a`) + scaffold (`62b60a07`) のとおり、宣言後の別セッション
(本execution host) が最新mainで対抗宣言を確認のうえ実行した。

- **結果: 52/52キーすべて LOSS (result 2)**。2-pass fresh-cold
  node-exact・budget 15,000,000・WIN 0・枯損 0・mismatch 0。
  総ノード数 **196,536,452/pass** (nodes range 1,651,860 .. 14,967,263。
  u031が14,967,263 nodesで予算直下でLOSS確定)。
- val-gate: 実行直前に本hostで4/4 node-exact (at2m 0/2,000,000 x2・
  15m (2,3651923)/(2,5040200)・禁止四角 95,670)。`output/val-gate/`。
- host event (誠実記録): 実行中にsandbox環境リセットが4回発生し、
  書きかけのpassファイル5個 (u017.p2, u018.p2, u027.p2, u031.p2, u033.p2)
  が不完全断片化した。完全性ガードが `# replay_done` 不在を検出して
  `output/raw-truncated-hostevent/` に退避し、該当passをfresh coldで
  再実行した。断片はどれもverdict行を持たず、完了済みrowの再探索は
  一切行っていない (batch-16と同種のhost event)。
- row-audit.json (schema `n11-centralreply-closure-class10661-batch17-rowaudit-v1`):
  全52行をrawから機械再検証 (p1==p2 node-exact・budget内・result 2・
  input行照合・status.log照合)。
- verdict消費: **ゼロ**。52 LOSS行のcanonical計上は別宣言のadoption Part
  (fail-closed merger `90711961...` 経由) で行う。canonical cacheは
  6,120行 `be9cb24e...` 不変。**標準11x11空盤・19 central-reply roots・
  class 10661・全キーはどの時点でもUNKNOWNのまま。nodes数を勝敗として
  読まない。**
- バッチ実績: 完走17バッチ目。clean全LOSSバッチは
  23963/10324/8784/10687 に次ぐ**5バッチ目** (WIN-HALT 11本 + batch-14
  もWIN-HALTのため、完走バッチ内訳は11+1 WIN-HALT + 5 clean)。
- 実行runnerのscaffold差分 (開示): `scripts/runbatch.sh` はpublished
  batch-16正本のbyte-copyに、15M枯損行 (jsreplayは枯損時もexit 0) を
  PASSと誤記録しないhonest exhaustionラベルを1箇所加えた
  (本バッチでは枯損0のため未発火・shaはMANIFEST固定)。
  `scripts/runwave.sh` は2-key wave (2-core host・宣言済みworker最大2)。
  `scripts/jsreplay.js` はpin `84585617...` のbyte-copy (MANIFEST固定)。
